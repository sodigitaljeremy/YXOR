"""L'empreinte doit changer quand requirements.txt ou le Dockerfile change.

    .venv/bin/python -m unittest tests.test_empreinte -v

Audit de la nuit du 2026-09-29, § 8 H10 : une montée de version de
build123d laissait l'empreinte intacte, alors que le site produit
pouvait différer. Ce test prouve que le contrôle sait ÉCHOUER : il a été
lancé et vu échouer avant la correction (journal du 2026-09-30).
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import empreinte  # noqa: E402


class EmpreinteCouvreLaConstruction(unittest.TestCase):
    def test_requirements_et_dockerfile_changent_l_empreinte(self):
        with tempfile.TemporaryDirectory() as d:
            racine = Path(d)
            for rep in ("params", "parts", "scripts", "web"):
                (racine / rep).mkdir()
                (racine / rep / "f.txt").write_text(rep)
            (racine / "requirements.txt").write_text("build123d==0.13.0\n")
            (racine / "Dockerfile").write_text("FROM python:3.14-slim\n")

            ancien = empreinte.REPO
            empreinte.REPO = racine
            try:
                e0 = empreinte.empreinte()
                (racine / "requirements.txt").write_text("build123d==0.14.0\n")
                e1 = empreinte.empreinte()
                (racine / "Dockerfile").write_text("FROM python:3.15-slim\n")
                e2 = empreinte.empreinte()
            finally:
                empreinte.REPO = ancien

        self.assertNotEqual(e0, e1, "requirements.txt ignoré par l'empreinte")
        self.assertNotEqual(e1, e2, "Dockerfile ignoré par l'empreinte")


if __name__ == "__main__":
    unittest.main()
