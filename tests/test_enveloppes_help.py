"""`enveloppes_actionneurs.py --help` doit afficher l'aide et N'ÉCRIRE RIEN.

    .venv/bin/python -m unittest tests.test_enveloppes_help -v

Audit du 2026-09-30 (docs/etat-des-lieux-2026-09-30.md, § 8, bas) : le
script ignorait ses arguments. `--help` lançait la simulation complète et
réécrivait deux fichiers d'exports/. Vu échouer avant la correction (journal
du 2026-09-30, lot de cohérence, point 8).
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import enveloppes_actionneurs as E  # noqa: E402


class AideSansEffet(unittest.TestCase):
    def test_help_n_ecrit_rien(self):
        ancien = E.SORTIE
        with tempfile.TemporaryDirectory() as d:
            E.SORTIE = Path(d) / "actionneurs"
            try:
                with self.assertRaises(SystemExit) as fin:
                    E.main(["--help"])
                self.assertEqual(fin.exception.code, 0)
                self.assertFalse(E.SORTIE.exists() and any(E.SORTIE.iterdir()),
                                 "--help a écrit dans le dossier de sortie")
            finally:
                E.SORTIE = ancien


if __name__ == "__main__":
    unittest.main()
