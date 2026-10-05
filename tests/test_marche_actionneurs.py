"""Le marché des actionneurs reste à l'écart de la grille de S, et son rapport est à jour.

    .venv/bin/python -m unittest tests.test_marche_actionneurs -v

Créé le 2026-10-05 (phase 1 de la fiche 0069). Le bloc `marche` de
params/actionneurs.yaml est HORS de `candidats` : s'il les recouvrait, k_bas,
le dimensionnement et la grille de S changeraient sans que rien ne le dise.
"""
import sys
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import marche_actionneurs as MA  # noqa: E402


def defauts(cat: dict) -> list[str]:
    m = cat.get("marche") or {}
    fam = set(m.get("familles_logicielles") or {})
    out = [f"{i} : à la fois dans candidats et dans marche" for i in m.get("actionneurs", {}) if i in cat["candidats"]]
    out += [f"{i} : famille « {a.get('famille_logicielle')} » inconnue"
            for i, a in (m.get("actionneurs") or {}).items() if a.get("famille_logicielle") not in fam]
    if "equivalent_Nm" in yaml.safe_dump(m):
        out.append("un équivalent N·m est DÉCLARÉ : il doit se calculer (règle de saisie)")
    return out


class Marche(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cat = yaml.safe_load(MA.CAT.read_text(encoding="utf-8"))

    def test_marche_present_et_a_l_ecart(self):
        self.assertGreater(len(self.cat["marche"]["actionneurs"]), 0)
        self.assertEqual(defauts(self.cat), [])

    def test_defauts_vus(self):
        import copy
        c = copy.deepcopy(self.cat)
        i = next(iter(c["marche"]["actionneurs"]))
        c["candidats"][i] = {}
        c["marche"]["actionneurs"][i]["famille_logicielle"] = "inconnue"
        c["marche"]["actionneurs"][i]["couple_blocage_Nm"] = {"valeur": 1, "equivalent_Nm": 0.1}
        self.assertEqual(len(defauts(c)), 3)

    def test_rapport_a_jour(self):
        fam, rows = MA.charger()
        md, svg = MA.doc(fam, rows)
        self.assertEqual(md, MA.DOC.read_text(encoding="utf-8"), "relancer : scripts/marche_actionneurs.py --ecrire")
        self.assertEqual(svg, MA.SVG.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
