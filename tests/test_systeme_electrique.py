"""Système électrique : tension (12S / 13S), énergie, batterie, calculateur, bus, place ; branchement dans l'explorateur.

    .venv/bin/python -m unittest tests.test_systeme_electrique -v

Créé le 2026-10-07 (phase 4a quinquies). Chaque contrôle est vu ÉCHOUER sur un
cas fait exprès.
"""
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import systeme_electrique as SE  # noqa: E402

HYP = SE.lire("puissance.yaml")["hypotheses"]


class Tension(unittest.TestCase):
    def test_variantes(self):
        v12, v13 = SE.variante(12), SE.variante(13)
        self.assertAlmostEqual(v12["Vmax"], 50.4)
        self.assertAlmostEqual(v13["Vfin"], 32.5)

    def test_compatibilite(self):
        v13 = SE.variante(13)
        self.assertTrue(SE.compatibilite((24.0, 60.0), v13))
        self.assertFalse(SE.compatibilite((24.0, 48.0), v13))          # RS01 : 54,6 V > 48 V, vu
        self.assertIsNone(SE.compatibilite(None, v13))                 # plage non publiée : INCONNU, jamais supposé

    def test_vitesse_a_la_coupure(self):
        self.assertAlmostEqual(SE.facteur_vitesse(48.0, SE.variante(12)), 30.0 / 48.0)
        self.assertIsNone(SE.facteur_vitesse(None, SE.variante(12)))


class Batterie(unittest.TestCase):
    def cell(self, i, E, I, m, prix=1.0):
        return dict(id=i, nom=i, E=E, I=I, m=m, vol=0.02, prix=prix)

    def test_la_plus_legere_qui_tient_aussi_le_courant(self):
        legere_faible = self.cell("a", 15.0, 5.0, 0.060)                 # légère mais 5 A
        lourde_forte = self.cell("b", 15.0, 45.0, 0.070)
        v = SE.variante(13)
        r = SE.batterie([legere_faible, lourde_forte], v, 100.0, 1500.0, HYP)    # 1500 W / 32,5 V = 46 A
        # a : P = max(1, 46/5 → 10) → 130 cellules ; b : P = 2 → 26 cellules : b est la plus légère
        self.assertEqual(r["best"]["id"], "b")
        r2 = SE.batterie([legere_faible, lourde_forte], v, 100.0, 50.0, HYP)
        self.assertEqual(r2["best"]["id"], "a")                          # sans pointe forte, la légère gagne

    def test_donnee_absente_ecartee(self):
        r = SE.batterie([dict(self.cell("x", 15.0, None, 0.07))], SE.variante(12), 50.0, 100.0, HYP)
        self.assertIsNone(r["best"])
        self.assertEqual(r["ecartees"], ["x"])


class Calculateur(unittest.TestCase):
    def test_modele_de_langage(self):
        o = [dict(id="h8", nom="Pi + Hailo-8", accel=True, llm=False, mem=16, prix=200, masse=50, pmax=10, v12=True),
             dict(id="h10", nom="Pi + Hailo-10H", accel=True, llm=True, mem=16, prix=400, masse=60, pmax=12, v12=True)]
        r = SE.choisir_calculateur(o, "+ modèle de langage local", HYP)
        self.assertEqual(r["best"]["id"], "h10")                         # le Hailo-8, moins cher, est refusé
        self.assertEqual(SE.choisir_calculateur(o, "+ vision", HYP)["best"]["id"], "h8")

    def test_verifiable_d_abord(self):
        o = [dict(id="a", nom="a", accel=True, llm=True, mem=8, prix=100, masse=None, pmax=10, v12=True),
             dict(id="b", nom="b", accel=True, llm=True, mem=8, prix=150, masse=40, pmax=10, v12=True)]
        self.assertEqual(SE.choisir_calculateur(o, "+ vision", HYP)["best"]["id"], "b")


class Bus(unittest.TestCase):
    ADAPT = [dict(id="hat", nom="HAT 2 canaux", canaux=2, linux=True, masse=40, prix=40, famille="can_spi"),
             dict(id="usb", nom="USB 1 canal", canaux=1, linux=True, masse=20, prix=60, famille="can_usb")]

    def test_hat_seulement_sur_raspberry(self):
        j = SE.choisir_bus(4, 2, self.ADAPT, None, "jetson")
        r = SE.choisir_bus(4, 0, self.ADAPT, None, "rpi")
        self.assertEqual(j["can"]["id"], "usb")
        self.assertEqual((r["can"]["id"], r["can"]["unites"]), ("hat", 2))

    def test_canaux(self):
        self.assertEqual(SE.canaux_can(27, 500, True)["canaux"], 7)
        self.assertEqual(SE.canaux_can(27, 250, False)["canaux"], 3)


class Place(unittest.TestCase):
    R = dict(largeur_epaules=0.2328, profondeur_poitrine=0.147, tronc_hauteur=0.3052)

    def test_allongement(self):
        p = SE.place_tronc(self.R, 0.6, 0.1, HYP)
        self.assertEqual(p["allonge_m"], 0.0)
        q = SE.place_tronc(self.R, 0.6, p["dispo_L"] + 1.0, HYP)          # 1 L de trop
        larg, prof = 0.2328 * 0.6, 0.147 * 0.6
        self.assertAlmostEqual(q["allonge_m"], 0.001 / (larg * prof * HYP["remplissage_tronc"]["valeur"]))


class Chaine(unittest.TestCase):
    def c(self, **k):
        base = dict(id="x", nom="x", categorie="regeneration", I=None, V=None, Vout=None, Vin=[], S=None, seuil=None,
                    bidir=None, certif="", texte="", masse=10.0, volume=0.01, prix=10.0)
        return dict(base, **k)

    def test_regeneration_seuil(self):
        m = [self.c(id="module", seuil=53.5)]
        self.assertIsNotNone(SE.composant(m, "regeneration", var=SE.variante(12))["best"])     # 50,4 V < 53,5 V
        self.assertIsNone(SE.composant(m, "regeneration", var=SE.variante(13))["best"])        # 54,6 V : viderait le pack
        self.assertIsNone(SE.composant([self.c(id="resistances")], "regeneration", var=SE.variante(12))["best"])

    def test_bms_et_contacteur(self):
        b = [self.c(id="b13", categorie="bms", S=(13, 13)), self.c(id="b820", categorie="bms", S=(8, 20), prix=50.0)]
        self.assertEqual(SE.composant(b, "bms", var=SE.variante(12))["best"]["id"], "b820")
        k = [self.c(id="mos", categorie="contacteur", texte="n'accepte pas de courant inverse", prix=1.0),
             self.c(id="relais", categorie="contacteur", bidir=True, prix=50.0)]
        self.assertEqual(SE.composant(k, "contacteur", var=SE.variante(12))["best"]["id"], "relais")

    def test_fusible_et_porte_fusible(self):
        f = [self.c(id="porte", nom="porte-fusible MEGA", categorie="fusible", prix=1.0),
             self.c(id="fus", nom="fusible MEGA", categorie="fusible", prix=5.0)]
        self.assertEqual(SE.composant(f, "fusible", var=SE.variante(13))["best"]["id"], "fus")
        self.assertEqual(SE.composant(f, "porte_fusible", var=SE.variante(13))["best"]["id"], "porte")

    def test_porte_fusible_du_meme_format(self):
        # ajouté le 2026-10-08 : un fusible MIDI ne va pas dans un porte-fusible MEGA (vu dans le rapport du jour)
        comps = [self.c(id="midi", nom="fusible MIDI 58V", categorie="fusible", I=60.0, V=58.0, prix=5.0),
                 self.c(id="pmega", nom="porte-fusible MEGA", categorie="fusible", volume=0.25, prix=1.0),
                 self.c(id="pmidi", nom="porte-fusible MIDI", categorie="fusible", volume=0.05, prix=9.0)]
        el = dict(hyp=HYP, var=SE.variante(12, coupure=3.0), calc=None, f_can=250, etendue=True, adapt=[], serie=None,
                  cells=[], comps=comps, chaine="compacte",
                  pui=dict(chaine_compacte=[{"maillon": "fusible", "categorie": ["fusible"]}],
                           choix_maillons={"marge_courant": 1.5, "ordre": ["prix"]}))
        r = SE.dimensionner(el, Place.R, {}, {}, [], 10.0, 0.6, 0.6, {}, 0, dict(el, Pm={}, P3a={}, cible={}))
        porte = dict(r["chaine"])["porte_fusible"]["best"]
        self.assertEqual(porte["id"], "pmidi")                  # le MEGA, moins cher, est refusé

    def test_dcdc_couvre_tout_le_pack(self):
        d = [self.c(id="36-72", categorie="dcdc", Vout=12.0, Vin=[36.0, 72.0], prix=1.0),
             self.c(id="12-60", categorie="dcdc", Vout=12.0, Vin=[12.0, 60.0], prix=60.0)]
        v = SE.variante(12)
        self.assertEqual(SE.composant(d, "dcdc", Vout=12.0, Vin=(v["Vfin"], v["Vmax"]))["best"]["id"], "12-60")


class Explorateur(unittest.TestCase):
    """La variante de tension écarte un actionneur hors plage et ramène les vitesses à la coupure."""

    def test_variante_appliquee(self):
        import explorateur as X
        ctx = dict(act={"robstride": [dict(id="rs01", plage=(24.0, 48.0), v_ref=36.0, vitesse=10.0, masse=0.3, pointe=17,
                                           continu=6, prix=100, geo=None, par_blocage=False, D=None)],
                        "feetech": []}, cible={"ia_embarquee": None}, cap=None, struct={"charge": 1.2})
        a = dict(ctx["act"]["robstride"][0])
        v = SE.variante(13)
        a2 = dict(a, compat=SE.compatibilite(a["plage"], v), vitesse=a["vitesse"] * SE.facteur_vitesse(a["v_ref"], v))
        self.assertFalse(X.passe(a2, dict(pk=1.0, c=0.0, w=0.0), 1.5))   # hors plage : refusé quel que soit le couple
        self.assertTrue(X.passe(dict(a2, compat=True), dict(pk=1.0, c=0.0, w=0.0), 1.5))
        self.assertAlmostEqual(a2["vitesse"], 10.0 * 32.5 / 36.0)


if __name__ == "__main__":
    unittest.main()
