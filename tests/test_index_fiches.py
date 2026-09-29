"""index_fiches doit lire TOUTES les lignes « Amendée par » d'une fiche.

    .venv/bin/python -m unittest tests.test_index_fiches -v

Audit de la nuit du 2026-09-29, § 8 C4 : seule la première était lue. La
0015 en porte deux (0042 et 0016), et l'amendement par la 0016
disparaissait de la colonne que l'index dit « la plus importante ». Vu
échouer avant la correction (journal du 2026-09-30).
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import index_fiches  # noqa: E402

FICHE = """# 9999 — Fiche d'essai

Date : 2026-09-30
Espèce : close
État : amendée
Statut : acceptée
Amendée par : `0042-premiere.md` — premier amendement.
Amendée par : `0016-seconde.md` — second amendement.
"""


class ToutesLesLignesAmendeePar(unittest.TestCase):
    def test_deux_amendements_sont_lus(self):
        am = index_fiches.entete(FICHE)["amendee"]
        texte = " ".join(am) if isinstance(am, list) else am
        self.assertIn("0042", texte)
        self.assertIn("0016", texte, "le second « Amendée par » est perdu")


if __name__ == "__main__":
    unittest.main()
