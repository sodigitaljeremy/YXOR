"""Le contrôle de provenance amont sait échouer.

    .venv/bin/python -m unittest tests.test_provenance_amont -v

Refonte R4 (2026-10-01). Une règle amont qui ne correspond plus à rien
(clé renommée) ou un fichier déclaré absent doit faire échouer le contrôle ;
la déclaration réelle doit trouver des valeurs amont, et aucune faute.
"""
import copy
import sys
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import provenance_amont as P  # noqa: E402


class ProvenanceAmont(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.decl = yaml.safe_load(P.DECLARATION.read_text(encoding="utf-8"))

    def inv(self, decl):
        return P.inventaire(decl, REPO / "params", REPO / "parts")

    def test_declaration_reelle(self):
        comptes, fautes = self.inv(self.decl)
        self.assertEqual(fautes, [])
        self.assertGreater(sum(comptes.values()), 0)

    def test_regle_morte(self):
        d = copy.deepcopy(self.decl)
        d["fichiers"]["anthropometry.yaml"]["regles"][0]["motif"] = "H_renomme"
        _, fautes = self.inv(d)
        self.assertTrue(any("H_renomme" in f for f in fautes), fautes)

    def test_fichier_absent(self):
        d = copy.deepcopy(self.decl)
        d["fichiers"]["absent.yaml"] = {"regles": [{"motif": "**", "origine": "amont"}]}
        _, fautes = self.inv(d)
        self.assertTrue(any("absent.yaml" in f for f in fautes), fautes)

    def test_rien_d_amont(self):
        _, fautes = self.inv({"fichiers": {}})
        self.assertTrue(fautes)


if __name__ == "__main__":
    unittest.main()
