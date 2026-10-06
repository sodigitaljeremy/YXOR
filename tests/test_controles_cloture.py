"""Outils de clôture : liens morts et contradictions, vus ÉCHOUER puis passer.

    .venv/bin/python -m unittest tests.test_controles_cloture -v

Créé le 2026-10-06 (décision de Jeremy du même jour : les verser dans scripts/).
"""
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import controle_contradictions as CC  # noqa: E402
import controle_liens as CL  # noqa: E402


class Liens(unittest.TestCase):
    def test_lien_mort_vu(self):
        n, morts = CL.liens_morts([(Path("docs/x.md"), "voir [là](inexistant-zzz.md) et [ici](decisions.md)")])
        self.assertEqual(n, 2)
        self.assertEqual(len(morts), 1)

    def test_code_et_web_ignores(self):
        n, morts = CL.liens_morts([(Path("docs/x.md"), "`[a](b.md)` [w](https://x.y) [ancre](#t) [c](…)")])
        self.assertEqual((n, morts), (0, []))

    def test_depot_sans_lien_mort(self):
        n, morts = CL.liens_morts(CL.fichiers_suivis())
        self.assertGreater(n, 0)
        self.assertEqual(morts, [])


class Contradictions(unittest.TestCase):
    def test_affirmation_perimee_vue(self):
        t, c = CC.chercher([("README.md", "La mécanique amont est en CC BY-NC 4.0.")])
        self.assertEqual(len(t), 1)

    def test_citation_ecartee(self):
        t, c = CC.chercher([("README.md", "Ce paragraphe disait « CC BY-NC 4.0 », corrigé le 2026-09-30.")])
        self.assertEqual((len(t), len(c)), (0, 1))

    def test_depot_sans_contradiction(self):
        t, _ = CC.chercher(CC.vivants())
        self.assertEqual(t, [], t)


if __name__ == "__main__":
    unittest.main()
