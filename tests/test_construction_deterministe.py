"""Deux régénérations à deux dates différentes donnent la même empreinte.

    .venv/bin/python -m unittest tests.test_construction_deterministe -v

Lot A.9, 2026-09-30. Le relevé d'origines de la semelle portait sa date
de génération. Il est engendré à chaque construction et il est haché par
`empreinte.py` : l'empreinte dépendait donc du JOUR de la construction,
et une image construite après minuit UTC ne concordait plus avec le
poste. Vu échouer avant la correction (journal du 2026-09-30).

Lance `regenerer.py` deux fois, en entier (environ 1 min), sous deux
fausses dates système. Les dates sont dans le futur, parce que
`controle_depot` refuse un journal daté après « aujourd'hui ». Les
fichiers suivis que la régénération réécrit sont remis à leur état
initial, que le test passe ou échoue.
"""
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PY = sys.executable
RELEVES = sorted((REPO / "parts").glob("*.origines.yaml"))

LANCEUR = """
import datetime, runpy, sys
class FausseDate(datetime.date):
    @classmethod
    def today(cls):
        return cls({a}, {m}, {j})
datetime.date = FausseDate
sys.argv = ["regenerer.py"]
runpy.run_path("scripts/regenerer.py", run_name="__main__")
"""


def regenerer_le(a, m, j) -> str:
    r = subprocess.run([PY, "-c", LANCEUR.format(a=a, m=m, j=j)], cwd=REPO,
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise AssertionError(f"regenerer a échoué au {a}-{m}-{j} :\n{r.stdout[-2000:]}{r.stderr[-2000:]}")
    return subprocess.run([PY, "scripts/empreinte.py"], cwd=REPO,
                          capture_output=True, text=True, check=True).stdout.strip()


class ConstructionDeterministe(unittest.TestCase):
    def test_meme_empreinte_a_deux_dates(self):
        avant = {f: f.read_bytes() for f in RELEVES}
        try:
            e1 = regenerer_le(2027, 1, 1)
            e2 = regenerer_le(2027, 6, 15)
        finally:
            for f, contenu in avant.items():
                f.write_bytes(contenu)
        self.assertEqual(e1, e2, "l'empreinte dépend de la date de construction")


if __name__ == "__main__":
    unittest.main()
