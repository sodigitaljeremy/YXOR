"""Marches simulées : référence prudente par articulation, couverture de Froude, rapport à jour.

    .venv/bin/python -m unittest tests.test_simulations_marche -v

Créé le 2026-10-06 (phase 3b). Les deux premiers tests portent sur des
données synthétiques (toujours exécutés) et voient le défaut ; le troisième
SAUTE, en le disant, si les séries de exports/simulations/ sont absentes.
"""
import math
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import simulations_marche as SM  # noqa: E402


def faux(rms, pk, fr=0.2):
    return dict(Fr=fr, profil={"knee": dict(rms=rms, pointe=pk, omega=0, puissance=0, saturation=None, serie=[])})


class Synthetique(unittest.TestCase):
    def test_prudente_prend_le_plus_exigeant_par_grandeur(self):
        ref = SM.prudente({"A": faux(0.05, 0.10), "B": faux(0.07, 0.08)})
        self.assertEqual((ref["knee"]["rms"], ref["knee"]["rms_de"]), (0.07, "B"))
        self.assertEqual((ref["knee"]["pointe"], ref["knee"]["pointe_de"]), (0.10, "A"))

    def test_niveau_hors_froude_non_couvert(self):
        cap = {"taches": {"marche_sol_plat": {"niveaux": [0.3, 5.0]}}}
        fmax, cv = SM.couverture({"A": faux(0.05, 0.1, fr=0.2)}, cap)
        self.assertIsNotNone(cv[0.3])
        self.assertIsNone(cv[5.0])                       # 5 m/s : Froude hors de portée sur 0,5–1,4 m
        h = cv[0.3]
        self.assertLessEqual(0.3 / math.sqrt(SM.G * h), 0.2 + 1e-9)


@unittest.skipUnless(any(SM.SIM.glob("*_marche_vx*.json")), "séries de simulation absentes (exports/ non suivi)")
class Rapport(unittest.TestCase):
    def test_rapport_a_jour(self):
        import yaml
        marches, releve, manque = SM.charger()
        cap = yaml.safe_load((REPO / "params" / "capacites.yaml").read_text(encoding="utf-8"))
        self.assertEqual(SM.rapport(marches, releve, manque, cap), SM.DOC.read_text(encoding="utf-8"),
                         "relancer : scripts/simulations_marche.py --ecrire")


if __name__ == "__main__":
    unittest.main()
