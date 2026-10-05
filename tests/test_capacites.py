"""Capacités en niveaux : noms d'axes contrôlés (règle 3), rapport à jour.

    .venv/bin/python -m unittest tests.test_capacites -v

Créé le 2026-10-05. Le contrôle est d'abord vu ÉCHOUER sur des défauts faits
exprès (nom inventé, méthode inconnue, un seul niveau).
"""
import copy
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import capacites as CA  # noqa: E402


class Capacites(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cap = CA.lire(CA.CAP)
        cls.joints = CA.noms_joints()

    def test_conforme(self):
        fautes, employes = CA.controler(self.cap, self.joints)
        self.assertEqual(fautes, [])
        self.assertIn("ankle_roll", employes)          # non retenu pour S (0068), annoncé

    def test_defauts_vus(self):
        c = copy.deepcopy(self.cap)
        t = c["taches"]["marche_sol_plat"]
        t["sollicite"].append("genou_gauche")
        t["methode"] = "intuition"
        c["taches"]["tete"]["niveaux"] = [2]
        fautes, _ = CA.controler(c, self.joints)
        self.assertEqual(len(fautes), 3, fautes)

    def test_rapport_a_jour(self):
        self.assertEqual(CA.doc(self.cap), CA.DOC.read_text(encoding="utf-8"),
                         "relancer : scripts/capacites.py --ecrire")


if __name__ == "__main__":
    unittest.main()
