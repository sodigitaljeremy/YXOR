"""Loi de masse : la variante n'altère pas la loi existante ; les paramètres sont ceux que l'ajustement redonne.

    .venv/bin/python -m unittest tests.test_loi_masse -v

Créé le 2026-10-06. Le contrôle de concordance est vu ÉCHOUER sur un exposant
faussé exprès ; il SAUTE, en le disant, si le CSV (hors du dépôt) est absent.
"""
import sys
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import dimensionnement as D  # noqa: E402
import loi_masse as LM  # noqa: E402


def ecarts(p, fit, tol=1e-3):
    e = p["variantes"]["allometrique"]["exposant"]
    return [k for k, v in (("central", fit["b"]), ("bas", fit["bas"]), ("haut", fit["haut"])) if abs(e[k] - v) > tol]


class Variante(unittest.TestCase):
    def test_loi_existante_inchangee_par_defaut(self):
        ref = dict(S0=2.0, H0=0.5)
        self.assertAlmostEqual(D.masse(1.0, ref, {}, {}), 2.0 * 8)                    # H³
        self.assertAlmostEqual(D.masse(1.0, dict(ref, exposant=2.0), {}, {}), 2.0 * 4)


@unittest.skipUnless(LM.DONNEES.exists(), "CSV robot-dataset absent (hors du dépôt, au registre)")
class Concordance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = yaml.safe_load(LM.PARAMS.read_text(encoding="utf-8"))
        cls.fit = LM.ajuster()

    def test_parametres_redonnes_par_l_ajustement(self):
        self.assertEqual(ecarts(self.p, self.fit), [])
        self.assertEqual(self.p["variantes"]["allometrique"]["n"], self.fit["n"])

    def test_ecart_vu(self):
        import copy
        p = copy.deepcopy(self.p)
        p["variantes"]["allometrique"]["exposant"]["central"] = 3.0
        self.assertEqual(ecarts(p, self.fit), ["central"])


if __name__ == "__main__":
    unittest.main()
