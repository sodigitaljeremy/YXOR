"""Explorateur : maximum par articulation, plus petit actionneur vérifiable, robustesse (b × structure), INCONNU,
place, profil cible.

    .venv/bin/python -m unittest tests.test_explorateur -v

Créé le 2026-10-07 ; révisé le même jour (phase 4a bis : place et structure des
études reconstruites, six cas de masse, profil cible). Le contrôle du maximum
est vu ÉCHOUER sur un cas faussé (somme au lieu du maximum) ; tout se joue sur
un contexte construit ici, sans CAO ni séries de simulation.
"""
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import explorateur as X  # noqa: E402
import taille_minimale as TM  # noqa: E402

H = 0.6
# deux tâches sur le même axe : le maximum n'est PAS la somme
T = {(H, "marche_sol_plat", 0.3): {"knee": dict(pk=[(0.5, 0.0)], c=[(0.2, 0.0)], w=[3.0])},
     (H, "saut_vertical", 5): {"knee": dict(pk=[(0.3, 1.0)], c=[], w=[5.0])}}
PROFIL = {"marche_sol_plat": 0.3, "saut_vertical": 5}
CV = TM.conventions()
RA = {k: x["valeur"] for k, x in TM.lire("anthropometry.yaml")["ratios"].items()}
PETIT = TM.moteur_dims("Ø20 × 20", CV)                 # tient partout à 0,60 m
JAMBE = ["hip_yaw", "hip_roll", "hip_pitch", "knee", "ankle_pitch"]
ENS_TEST = 99


def act(i, masse, pointe, continu=None, vitesse=50.0, prix=100.0, geo=PETIT, par_blocage=False):
    return dict(id=i, masse=masse, pointe=pointe, continu=continu, vitesse=vitesse, prix=prix, D=20.0, geo=geo,
                par_blocage=par_blocage)


def ctx(acts, ex=None, mmin=None, struct=1.0, struct_haute=1.0, cible=None):
    return dict(T=T, act={"f": acts, "p": [act("servo", 0.01, 1.0, 0.5)]}, marge=1.5, memo={}, cv=CV, R=RA,
                ex=ex or dict(bas=2.0, central=2.0, haut=2.0, iso=3.0), cible=cible or {},
                struct=dict(par_ensemble={(ENS_TEST, "central"): struct, (ENS_TEST, "haute"): struct_haute},
                            H_S=0.6, charge=0.0),
                C={H: mmin or {}, 1.2: {}})


class Base(unittest.TestCase):
    def setUp(self):
        X.ENSEMBLES[ENS_TEST] = dict(axes={a: 2 for a in JAMBE} | {"waist_yaw": 1}, source="test")

    def tearDown(self):
        X.ENSEMBLES.pop(ENS_TEST, None)


class Maximum(unittest.TestCase):
    def test_maximum_par_articulation(self):
        b = X.besoins(T, H, PROFIL, 10.0)
        self.assertAlmostEqual(b["knee"]["pk"], max(0.5 * 10, 0.3 * 10 + 1))
        self.assertEqual(X.verifier_maximum(b, T, H, PROFIL, 10.0), [])

    def test_maximum_fausse_vu_echouer(self):
        b = X.besoins(T, H, PROFIL, 10.0, combine=lambda x, y: x + y)       # somme : FAUX
        ecarts = X.verifier_maximum(b, T, H, PROFIL, 10.0)
        self.assertTrue(any(e.startswith("knee.pk") for e in ecarts), ecarts)


class Choix(unittest.TestCase):
    def test_plus_petit_verifiable(self):
        acts = [act("a", 0.1, 5.0), act("b", 0.2, 20.0, prix=None), act("c", 0.3, 20.0)]
        self.assertEqual(X.choisir(acts, dict(pk=10.0, c=0.0, w=0.0), 1.5), 2)   # b sans prix : c, vérifiable

    def test_repli_inconnu(self):
        acts = [act("a", 0.1, 5.0), act("b", 0.2, 20.0, prix=None)]
        self.assertEqual(X.choisir(acts, dict(pk=10.0, c=0.0, w=0.0), 1.5), 1)

    def test_cotes_manquantes_non_verifiable(self):
        acts = [act("a", 0.1, 20.0, geo=None), act("b", 0.2, 20.0)]
        self.assertEqual(X.choisir(acts, dict(pk=1.0, c=0.0, w=0.0), 1.5, cotes=True), 1)


class Evaluation(Base):
    def test_faisable(self):
        r = X.evaluer(ctx([act("a", 0.1, 100.0, 100.0)]), ENS_TEST, H, "f", "p", PROFIL)
        self.assertEqual(r["statut"], "faisable", r)
        self.assertAlmostEqual(r["H_reel"], H)                # petits moteurs : aucun écart

    def test_donnee_absente_inconnu(self):
        r = X.evaluer(ctx([act("a", 0.1, 100.0, None)]), ENS_TEST, H, "f", "p", PROFIL)
        self.assertEqual(r["statut"], "INCONNU")
        self.assertIn("couple continu de a", r["inconnues"])

    def test_robuste_a_la_bande_de_b(self):
        # à 2 × H_S : M = 2 kg au b central (besoin 1,5 × 1,6 = 2,4 N·m), 8 kg au b haut (1,5 × 4 = 6 N·m) ; pointe 5
        T2 = {(1.2, t, n): v for (h, t, n), v in T.items()}
        for haut, attendu in ((3.0, "infaisable"), (1.0, "faisable")):
            c = ctx([act("a", 0.0, 5.0, 9.0)], ex=dict(bas=1.0, central=1.0, haut=haut, iso=3.0))
            c["T"] = T2
            self.assertEqual(X.evaluer(c, ENS_TEST, 1.2, "f", "p", PROFIL)["statut"], attendu, haut)

    def test_robuste_a_la_structure_haute(self):
        # structure centrale 1 kg : besoin 1,5 × 0,5 × 1 = 0,75 N·m ; haute 8 kg : 1,5 × 0,5 × 8 = 6 N·m ; pointe 5
        ok = X.evaluer(ctx([act("a", 0.0, 5.0, 9.0)], struct=1.0, struct_haute=1.0), ENS_TEST, H, "f", "p", PROFIL)
        ko = X.evaluer(ctx([act("a", 0.0, 5.0, 9.0)], struct=1.0, struct_haute=8.0), ENS_TEST, H, "f", "p", PROFIL)
        self.assertEqual((ok["statut"], ko["statut"]), ("faisable", "infaisable"))

    def test_masse_minimale(self):
        r = X.evaluer(ctx([act("a", 0.1, 100.0, 100.0)], mmin={("saut_vertical", 5): 50.0}), ENS_TEST, H, "f", "p", PROFIL)
        self.assertEqual(r["statut"], "infaisable")

    def test_couples_a_la_hauteur_reelle(self):
        # gros moteurs : le tronc s'allonge ; les couples doivent être lus au-dessus de la hauteur réelle
        gros = TM.moteur_dims("Ø120 × 60", CV)
        c = ctx([act("a", 0.1, 100.0, 100.0, geo=gros)])
        c["T"] = {(round(h, 2), t, n): v for h in X.EP.HS for (_, t, n), v in T.items()}
        r = X.evaluer(c, ENS_TEST, H, "f", "p", PROFIL)
        self.assertGreaterEqual(r["H_couples"], r["H_reel"] - 1e-9)
        self.assertGreater(r["H_couples"], H)
        self.assertGreaterEqual(r["iterations"], 2)
        # et un actionneur qui tient à H mais pas à la hauteur réelle devient infaisable
        T4 = {(round(h, 2), "marche_sol_plat", 0.3): {"knee": dict(pk=[(10.0 * h, 0.0)], c=[], w=[])} for h in X.EP.HS}
        juste = 1.5 * 10.0 * H * (1.0 + 0.1 * 10 + 0.0) + 0.5               # tient à H, pas au-dessus
        c2 = ctx([act("a", 0.1, juste, 100.0, geo=gros)])
        c2["T"] = T4
        r2 = X.evaluer(c2, ENS_TEST, H, "f", "p", {"marche_sol_plat": 0.3})
        self.assertEqual(r2["statut"], "infaisable", r2.get("violees"))

    def test_place_gros_moteurs_allongent(self):
        gros = TM.moteur_dims("Ø120 × 60", CV)
        r = X.evaluer(ctx([act("a", 0.1, 100.0, 100.0, geo=gros)]), ENS_TEST, H, "f", "p", PROFIL)
        self.assertGreater(r["H_reel"], H + 0.05)
        self.assertFalse(r["place"]["tient_ansur"])


class Cible(unittest.TestCase):
    def test_profil_lab(self):
        cap = X.lire("capacites.yaml")
        c = X.cible_defaut(cap, "lab")
        self.assertEqual(c["releve"], ["depuis le dos", "depuis le ventre"])
        self.assertNotIn("charge_lourde", c)                  # réservé au final (Jeremy, 2026-10-07)
        nc = {k: X.non_couvertes(e["axes"], c) for k, e in X.ENSEMBLES.items() if k != ENS_TEST}
        self.assertEqual(nc[25], ["sol_irregulier"])          # pas de roulis de cheville
        self.assertEqual(nc[27], [])
        self.assertEqual(nc[29], [])

    def test_profil_final(self):
        cap = X.lire("capacites.yaml")
        nc = X.non_couvertes(X.ENSEMBLES[27]["axes"], X.cible_defaut(cap, "final"))
        self.assertEqual(nc, ["mains_a_doigts", "buste"])

    def test_niveaux_en_liste(self):
        T3 = dict(T)
        T3[(H, "releve", "dos")] = {"knee": dict(pk=[(0.1, 0.0)], c=[], w=[])}
        T3[(H, "releve", "ventre")] = {"knee": dict(pk=[(0.9, 0.0)], c=[], w=[])}
        b = X.besoins(T3, H, {"releve": ["dos", "ventre"]}, 10.0)
        self.assertAlmostEqual(b["knee"]["pk"], 9.0)          # le maximum des deux positions
        self.assertEqual(X.verifier_maximum(b, T3, H, {"releve": ["dos", "ventre"]}, 10.0), [])

    def test_pareto_ne_compare_pas_a_egalite(self):
        s = lambda c, nc: dict(statut="faisable", cout=c, M=c, E=c, ncap=1, n_couvertes=nc)
        front = X.pareto([s(1, 10), s(2, 12)])                  # plus cher, mais couvre plus : sur le front
        self.assertEqual(len(front), 2)


class Ensembles(unittest.TestCase):
    def test_nombres_d_axes(self):
        self.assertEqual({k: sum(e["axes"].values()) for k, e in X.ENSEMBLES.items() if k != ENS_TEST},
                         {25: 25, 26: 26, 27: 27, 29: 29})

    def test_pareto(self):
        s = lambda c, m, n: dict(statut="faisable", cout=c, M=m, E=m, ncap=n)
        front = X.pareto([s(1, 1, 1), s(2, 2, 1), s(2, 2, 2), s(1, 1, 1)])
        self.assertEqual(sorted((p["cout"], p["ncap"]) for p in front), [(1, 1), (2, 2)])


if __name__ == "__main__":
    unittest.main()


class Leger(unittest.TestCase):
    """Ajouté le 2026-10-08 : les solutions légères se classent comme les complètes, et `complet` les rend à l'identique."""

    def test_classement_identique(self):
        ctx = X.contexte(S=12, f_can=250)
        args = dict(ensembles=[27, 25], hs=[0.5, 0.6], corps=["robstride", "cubemars"], petits=["feetech"])
        pleins = X.explorer(ctx, **args)
        legers = X.explorer(ctx, garder_leger=True, **args)
        cle = lambda xs: [(x["ens"], x["H"], x["fc"], x["fp"], tuple(x["profil"])) for x in xs]
        self.assertEqual(cle(X.classement_large(pleins)), cle(X.classement_large(legers)))
        self.assertEqual(len(X.pareto(pleins)), len(X.pareto(legers)))
        x = X.classement_large(legers)[0]
        y = X.classement_large(pleins)[0]
        z = X.complet(ctx, x)
        self.assertEqual((z["M"], z["cout"], z["H_reel"], z["inconnues"]), (y["M"], y["cout"], y["H_reel"], y["inconnues"]))

    def test_leger_vu_echouer(self):
        r = dict(statut="INCONNU", ncap=2, cout=None, cout_actionneurs=10.0, M=1.0, E=1.0, H_reel=0.5, H_couples=0.5,
                 non_couvertes=[], n_couvertes=1, inconnues=["a"], elec=None)
        x = X.leger(r, ens=27, H=0.5, fc="f", fp="p", profil={})
        self.assertNotIn("choix", x)
        x["inconnues"] = ("b",)                                  # une inconnue faussée change le classement : vu
        self.assertNotEqual(X.leger(r, ens=27, H=0.5, fc="f", fp="p", profil={})["inconnues"], x["inconnues"])
