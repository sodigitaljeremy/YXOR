"""La colonne D&C de ratios_ansur doit montrer Drillis & Contini, pas le YAML.

    .venv/bin/python -m unittest tests.test_ratios_ansur -v

Audit de la nuit du 2026-09-29, § 8 H7 : la colonne « D&C » lisait
l'`anthropometry.yaml` ACTUEL, qui porte ANSUR depuis la fiche 0034.
L'écart affiché valait 0 % par construction : la comparaison était
perdue sans que rien ne le dise. Vu échouer avant la correction (journal
du 2026-09-30).

Lit les CSV ANSUR II locaux (fiche 0030) ; ils ne sont pas dans le dépôt.
"""
import contextlib
import io
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import ratios_ansur  # noqa: E402


class ColonneDrillisContini(unittest.TestCase):
    def test_la_colonne_dc_porte_la_valeur_historique(self):
        sortie = io.StringIO()
        sys.argv = ["ratios_ansur.py"]
        with contextlib.redirect_stdout(sortie):
            ratios_ansur.main()
        ligne = next(l for l in sortie.getvalue().splitlines()
                     if l.strip().startswith("pied_longueur"))
        champs = ligne.split()
        # pied_longueur  ANSUR  σ  n  D&C  écart  %
        self.assertEqual(champs[4], "0.152",
                         f"colonne D&C ≠ valeur historique 0.152 : {ligne!r}")


if __name__ == "__main__":
    unittest.main()
