"""La configuration retenue de S (fiche 0067) tient 0,60 m ; le RS00 au roulis de hanche ne le tient pas en v3.

    .venv/bin/python -m unittest tests.test_configuration_S -v

Créé le 2026-10-02. Configuration lue dans params/configuration_S.yaml.
"""
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import analyser_marche as AM  # noqa: E402
import choix_actionneurs as C  # noqa: E402

OK = ("PASS", "TESTED")


def tient(c, H):
    return all(c["v"][k] in OK for k in ("T1", "T2", "T5")) and c["H_max"] >= H


@unittest.skipUnless(AM.SERIE.exists(), "série de marche absente (exports/ non suivi) : grille non calculable")
class ConfigurationS(unittest.TestCase):
    H = 0.60

    def test_retenue_v1_et_v3(self):
        for v3 in (False, True):
            with self.subTest(v3=v3):
                self.assertTrue(tient(C.evaluer_configuration(self.H, v3), self.H))

    def test_rs00_au_roulis_de_hanche_tombe_en_v3(self):
        j = dict(C.lire(C.CONFIG)["jambes"], hip_roll="rs00")
        self.assertFalse(tient(C.evaluer_configuration(self.H, True, j), self.H))


if __name__ == "__main__":
    unittest.main()
