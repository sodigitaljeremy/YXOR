"""Étude « lab léger » (scripts/lab_leger.py) : rapport à jour ; le niveau 0,15 m/s reste DANS le processus de l'étude.

    .venv/bin/python -m unittest tests.test_lab_leger -v

Créé le 2026-10-08 (règle 9). Aucune décision : le profil `lab_leger` est un candidat PROPOSÉ.
"""
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


class LabLeger(unittest.TestCase):
    def test_rapport_a_jour_et_grille_intacte(self):
        # un processus à part : l'étude prolonge la grille et ajoute 0,15 m/s dans SON processus seulement
        code = ("import sys; sys.path.insert(0, 'scripts'); import lab_leger as LL; r, h = LL.tout(); "
                "open(sys.argv[1], 'w', encoding='utf-8').write(LL.rapport(r, h))")
        out = REPO / "exports" / "lab_leger_test.md"
        out.parent.mkdir(exist_ok=True)
        subprocess.run([sys.executable, "-c", code, str(out)], cwd=REPO, check=True)
        self.assertEqual(out.read_text(encoding="utf-8"), (REPO / "docs" / "lab-leger-2026-10.md").read_text(encoding="utf-8"),
                         "relancer : scripts/lab_leger.py --ecrire")
        import yaml
        cap = yaml.safe_load((REPO / "params" / "capacites.yaml").read_text(encoding="utf-8"))
        self.assertNotIn(0.15, cap["taches"]["marche_sol_plat"]["niveaux"])   # la grille commune n'a pas bougé
        self.assertIn("lab_leger", cap["profils"])


if __name__ == "__main__":
    unittest.main()
