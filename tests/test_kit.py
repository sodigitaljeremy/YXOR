"""Étude de YXOR Kit (scripts/kit.py) : rapport à jour, Lab recopié encore vrai, modules contrôlés, défauts vus.

    .venv/bin/python -m unittest tests.test_kit -v

Créé le 2026-10-08 (prompt « Étude de YXOR Kit » ; règle 9 : toute étude citée vit dans le dépôt, avec un test).
"""
import copy
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import capacites as C  # noqa: E402
import kit as K  # noqa: E402
import marche_composants as MC  # noqa: E402


class Kit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e, cls.e_min, cls.var, cls.e_pg = K.tout()
        cls.ctx = cls.e["ctx"]

    def test_rapport_a_jour(self):
        self.assertEqual(K.rapport(self.e, self.e_min, self.var, self.e_pg), K.DOC.read_text(encoding="utf-8"),
                         "relancer : scripts/kit.py --ecrire")

    def test_lab_recopie_toujours_vrai(self):
        # params/kit.yaml recopie une SORTIE de l'explorateur : si l'explorateur change, ce test le dit
        lab = self.ctx["kit"]["lab"]
        doc = (REPO / "docs" / "explorateur-lab-2026-10.md").read_text(encoding="utf-8")
        self.assertIn(lab["ligne"], doc)
        for v in (f"{lab['H_m']:.2f}".replace(".", ","), f"{lab['hauteur_reelle_m']:.3f}".replace(".", ","),
                  f"{lab['masse_kg']:.1f}".replace(".", ","), lab["petits_axes"]):
            self.assertIn(v, lab["ligne"])

    def test_modules_controles(self):
        cap = copy.deepcopy(MC.lire("capacites.yaml"))
        self.assertEqual(C.controler_profils(cap), [])
        m = cap["profils"]["kit"]["modules"][1]
        m["motorises"].append("genou")                           # un nom hors de joints.yaml (règle 3)
        m["vise"]["tete"] = 7                                     # un niveau inexistant
        fautes = C.controler_profils(cap)
        self.assertTrue(any("genou" in f for f in fautes) and any("« 7 »" in f for f in fautes), fautes)

    def test_structure_suit_le_carton(self):
        c = K.carton_reference(self.ctx)
        m1 = K.masse_structure(K.segments(self.ctx, c, self.e["D"]))
        m2 = K.masse_structure(K.segments(self.ctx, dict(c, sigma=2 * c["sigma"]), self.e["D"]))
        self.assertAlmostEqual(m2, 2 * m1)
        self.assertGreater(m1, 0)

    def test_aucun_servo_qui_ne_tient_pas(self):
        # défaut simulé : un besoin hors de portée ne trouve AUCUN servo (pas de choix par défaut silencieux)
        ft = K.feetech(self.ctx, dict(S=0, Vfin=12.0, Vmax=12.0))
        self.assertIsNone(K.choisir(ft, dict(pk=100.0, c=0.0, w=0.0), 1.5)["best"])
        r = K.choisir(ft, dict(pk=0.1, c=0.05, w=0.0), 1.5)["best"]
        self.assertTrue(r and r["pointe"] >= 0.15)

    def test_classement_cartons(self):
        aire = 1.0
        cl = K.classement_cartons(self.ctx, aire)
        elim = {c["id"] for c in cl["elimines"]}
        self.assertIn("kapa_line_5mm_modulor", elim)               # sandwich mousse : pas mono-matière papier
        self.assertIn("forex_classic_3mm_modulor", elim)
        prox = [c["proxy"] for c in cl["retenus"]]
        self.assertEqual(prox, sorted(prox, reverse=True))
        self.assertTrue(all(c["sigma"] and c["e"] for c in cl["retenus"]))

    def test_progressive_secteur(self):
        # fiche 0075 : bloc secteur aux niveaux 1 et 2, batterie au niveau 3 seulement
        sc = self.e_pg["secteur"]
        self.assertGreater(sc["I_need"], sc["I_servos"])                      # la marge s'applique
        n1 = [x for x in self.e_pg["niveaux"][1]["items"]]
        self.assertFalse(any("12S1P" in x["nom"] for x in n1))                 # pas de batterie au niveau 1
        self.assertTrue(any("12S1P" in x["nom"] for x in self.e_pg["niveaux"][3]["items"]))
        self.assertTrue(any(x.get("hors_robot") for x in n1))                  # le bloc, sur la table
        # défaut simulé : un courant inatteignable ne trouve aucun bloc, et le dit
        b = K.bloc_secteur(self.ctx, 1000.0, True)
        self.assertIsNone(b["prix"])
        self.assertIn("aucun bloc", b["nom"])

    def test_debout_et_statique_croissent(self):
        d1, d2 = K.debout(self.ctx, 2.0), K.debout(self.ctx, 4.0)
        for ax in d1:
            self.assertAlmostEqual(d2[ax], 2 * d1[ax])


if __name__ == "__main__":
    unittest.main()
