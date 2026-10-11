"""Parcours guidé du Kit (scripts/kit_parcours.py, PROPOSÉ) : règle de réemploi, batterie sous 100 Wh, rapport à jour.

    .venv/bin/python -m unittest tests.test_kit_parcours -v

Créé le 2026-10-11 (règle 9 ; règle de réemploi de la fiche 0076 : tout durable se fixe de façon démontable,
colle et agrafes seulement entre deux pièces de structure).
"""
import copy
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import kit_parcours as KP  # noqa: E402


class Parcours(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.res, cls.fautes = KP.tout()

    def test_regle_de_reemploi(self):
        self.assertEqual(self.fautes, [])
        for r in self.res:
            for i in r["items"]:
                if i["classe"] == "DURABLE":
                    self.assertNotIn(i["fixation"], ("colle", "agrafes"), i["nom"])

    def test_defaut_vu(self):
        # défaut simulé : un servo collé, une plaque vissée par une agrafe… le contrôle le voit
        faux = copy.deepcopy(self.res)
        faux[1]["items"][0]["fixation"] = "colle"
        self.assertTrue(KP.regle_violee(faux))

    def test_batterie_sous_100_wh(self):
        for r in self.res:
            if r["E_Wh"]:
                self.assertLess(r["E_Wh"], KP.LIMITE_WH, r["nom"])

    def test_reemploi_croit(self):
        # chaque étape après la première réemploie une partie de ce qui a été acheté avant
        for r in self.res[2:]:
            self.assertGreater(r["part_reemploi"], 0.0, r["nom"])

    def test_rapport_a_jour(self):
        self.assertEqual(KP.rapport(self.res, self.fautes), KP.DOC.read_text(encoding="utf-8"),
                         "relancer : scripts/kit_parcours.py --ecrire")


if __name__ == "__main__":
    unittest.main()
