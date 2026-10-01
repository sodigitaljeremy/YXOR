"""LIENS-BRUTS.md liste exactement les fichiers suivis par Git.

    .venv/bin/python -m unittest tests.test_liens_bruts -v

Le nombre de lignes de liens égale le nombre de fichiers suivis, et ce sont
les mêmes chemins. Échoue si un fichier a été ajouté ou retiré sans
régénération (scripts/regenerer.py, ou scripts/liens_bruts.py seul).
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import liens_bruts as L  # noqa: E402


@unittest.skipUnless((L.REPO / ".git").exists(), "pas de dépôt git")
class LiensBruts(unittest.TestCase):
    def test_une_ligne_par_fichier_suivi(self):
        lignes = [l for l in L.CIBLE.read_text(encoding="utf-8").splitlines() if l.startswith(L.BASE)]
        suivis = L.suivis()
        self.assertEqual(len(lignes), len(suivis))
        self.assertEqual(sorted(l[len(L.BASE):] for l in lignes), suivis)


if __name__ == "__main__":
    unittest.main()
