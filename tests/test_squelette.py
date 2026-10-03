"""Le squelette de S (v3) se charge dans MuJoCo, compte 28 articulations et pèse la masse du modèle de S.

    .venv/bin/python -m unittest tests.test_squelette -v

Créé le 2026-10-03. Le MJCF est engendré EN MÉMOIRE (scripts/squelette.py).
"""
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import analyser_marche as AM  # noqa: E402


@unittest.skipUnless(AM.SERIE.exists(), "série de marche absente (exports/ non suivi) : masse de S non calculable")
class Squelette(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import mujoco
        import squelette as SQ
        cls.sq = SQ.construire()
        cls.m = mujoco.MjModel.from_xml_string(SQ.mjcf(cls.sq))
        cls.mujoco = mujoco

    def test_28_articulations(self):
        charnieres = [i for i in range(self.m.njnt) if self.m.jnt_type[i] == self.mujoco.mjtJoint.mjJNT_HINGE]
        self.assertEqual(len(charnieres), 28)

    def test_masse_du_modele_de_S(self):
        self.assertAlmostEqual(sum(self.m.body_mass), self.sq["masse_totale"], delta=0.01 * self.sq["masse_totale"])

    def test_noms_de_joints_yaml(self):
        import yaml
        jo = yaml.safe_load((REPO / "params" / "joints.yaml").read_text(encoding="utf-8"))
        noms = {j["nom"] for g in ("jambes", "bras", "taille", "nuque") for j in jo[g]}
        for x in self.sq["arts"]:
            if not x["provisoire"]:
                self.assertIn(x["base"], noms, x["nom"])


if __name__ == "__main__":
    unittest.main()
