"""Le contrôle des noms d'articulations sait échouer.

    .venv/bin/python -m unittest tests.test_controle_articulations -v

Refonte R4 (2026-10-01). Un nom renommé d'un seul côté — dans joints.yaml
ou dans le code — doit faire échouer le contrôle ; les données réelles du
dépôt doivent le passer.
"""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import controle_articulations as C  # noqa: E402


class NomsArticulations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.joints = C.lire("joints.yaml")
        cls.amont = C.lire("upstream_joints.generated.yaml")
        cls.code = C.noms_du_code()

    def test_depot_reel_coherent(self):
        _, fautes = C.comparer(self.joints, self.amont, self.code, None)
        self.assertEqual(fautes, [])

    def test_moteur_renomme_dans_joints(self):
        j = copy.deepcopy(self.joints)
        j["jambes"][3]["actionnement"]["moteurs"] = ["left_genou"]
        _, fautes = C.comparer(j, self.amont, self.code, None)
        self.assertTrue(any("left_genou" in f for f in fautes), fautes)

    def test_nom_inconnu_dans_le_code(self):
        code = dict(self.code, **{"essai": ["genou"]})
        _, fautes = C.comparer(self.joints, self.amont, code, None)
        self.assertTrue(any("genou" in f for f in fautes), fautes)

    def test_colonne_de_serie_inconnue(self):
        _, fautes = C.comparer(self.joints, self.amont, self.code, ["left_genou"])
        self.assertTrue(fautes)


class NomsSquelette(unittest.TestCase):
    def test_squelette_reel(self):
        _, fautes = C.controler_squelette(C.lire("joints.yaml"), C.lire("squelette.yaml"))
        self.assertEqual(fautes, [])

    def test_nom_inconnu_refuse(self):
        sq = copy.deepcopy(C.lire("squelette.yaml"))
        sq["articulations"][3]["nom"] = "genou"
        _, fautes = C.controler_squelette(C.lire("joints.yaml"), sq)
        self.assertTrue(any("genou" in f for f in fautes), fautes)


if __name__ == "__main__":
    unittest.main()
