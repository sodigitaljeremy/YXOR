"""index_fiches doit lire « Remplacée par » et refuser un remplacement non réciproque.

    .venv/bin/python -m unittest tests.test_index_remplacee -v

Fiche 0054 (2026-09-30) : une fiche acceptée ne se réécrit plus, elle est
remplacée. L'ancienne porte `Remplacée par : MMMM`, la nouvelle
`Remplace : NNNN`. Un remplacement annoncé d'un seul côté est une faute :
l'index doit la REFUSER, pas l'afficher. Vu échouer avant l'implémentation
(journal du 2026-09-30).
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import index_fiches  # noqa: E402

ANCIENNE = """# 0001 — Ancienne

Date : 2026-09-28
Espèce : historique
État : appliquée
Statut : appliquée
Remplacée par : `0002-nouvelle.md` — le monde a changé.
"""
NOUVELLE = """# 0002 — Nouvelle

Date : 2026-09-30
Espèce : gouvernante
État : acceptée
Statut : acceptée
Remplace : `0001-ancienne.md`
"""


class Remplacements(unittest.TestCase):
    def _construire(self, fiches: dict):
        ancien = index_fiches.DEC
        with tempfile.TemporaryDirectory() as d:
            for nom, texte in fiches.items():
                (Path(d) / nom).write_text(texte, encoding="utf-8")
            index_fiches.DEC = Path(d)
            try:
                return index_fiches.construire()
            finally:
                index_fiches.DEC = ancien

    def test_remplacee_par_est_lue(self):
        d = index_fiches.entete(ANCIENNE)
        self.assertIn("0002", " ".join(d.get("remplacee") or []))

    def test_index_affiche_le_remplacement(self):
        t, mauvais = self._construire({"0001-ancienne.md": ANCIENNE, "0002-nouvelle.md": NOUVELLE})
        self.assertEqual(mauvais, [])
        ligne = next(l for l in t.splitlines() if l.startswith("| [0001]"))
        self.assertIn("0002", ligne)

    def test_remplacement_non_reciproque_refuse(self):
        seule = ANCIENNE.replace("Remplacée par : `0002-nouvelle.md` — le monde a changé.\n", "")
        _, mauvais = self._construire({"0001-ancienne.md": seule, "0002-nouvelle.md": NOUVELLE})
        self.assertTrue(any("0001" in m and "0002" in m for m in mauvais),
                        "un « Remplace » sans « Remplacée par » en face passe")


if __name__ == "__main__":
    unittest.main()
