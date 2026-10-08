"""Pilote SysML v2 : model/yxor.sysml est À JOUR (engendré depuis params/) et VALIDE (OpenSysML), erreur vue.

    YXOR_SYSML=<chemin du binaire OpenSysML> .venv/bin/python -m unittest tests.test_sysml -v

Créé le 2026-10-08. Le validateur (OpenSysML, Open-MBEE, Apache-2.0) n'est pas dans le
dépôt : sans la variable YXOR_SYSML, la validation SAUTE et le dit ; la mise à jour se
teste toujours.
"""
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import sysml as SY  # noqa: E402


class Sysml(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.txt = SY.engendrer()

    def test_a_jour(self):
        self.assertEqual(self.txt, SY.SORTIE.read_text(encoding="utf-8"), "relancer : scripts/sysml.py --ecrire")

    def test_rien_a_la_main(self):
        # chaque axe de joints.yaml, chaque profil et chaque tâche apparaissent ; un ajout dans params/ se verrait
        for a in SY.axes():
            self.assertIn(f"part def {a} :> Articulation;", self.txt)
        for nom in ("Kit", "Lab", "Home", "Pro"):
            self.assertIn(f"variant part {nom.lower()} : YXOR_{nom};", self.txt)

    @unittest.skipUnless(SY.validateur(), "validateur OpenSysML absent (variable YXOR_SYSML) : validation SAUTÉE")
    def test_valide_et_erreur_vue(self):
        code, sortie = SY.valider(self.txt)
        self.assertEqual(code, 0, sortie)
        faux = self.txt.replace("attribute a : Real;", "attribute a : TypeInexistant;", 1)
        code2, _ = SY.valider(faux)
        self.assertNotEqual(code2, 0)                            # une référence non résolue : vue
        faux2 = self.txt.replace("package Axes {", "package Axes {{", 1)
        self.assertNotEqual(SY.valider(faux2)[0], 0)              # une erreur de syntaxe : vue


if __name__ == "__main__":
    unittest.main()
