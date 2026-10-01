"""La charge utile fixe ne change pas la référence quand elle la reproduit.

    .venv/bin/python -m unittest tests.test_charge_utile -v

Refonte R3 (2026-10-01) : l'électronique de ToddlerBot est retirée de la
part mise à l'échelle (H³), et la charge utile de YXOR ajoutée en masse
FIXE (dimensionnement.reference_charge). À H0, avec une charge utile égale
à l'électronique retirée, la masse doit être EXACTEMENT celle d'avant ;
au-delà de H0, retirer de la part mise à l'échelle doit alléger le robot.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import analyser_marche as AM  # noqa: E402
import dimensionnement as D  # noqa: E402


class ChargeUtile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cat = D.charger_catalogue()
        cls.besoins = D.besoins_p1(AM.analyser(AM.SERIE))
        cls.ref = D.reference(cls.cat, AM.analyser(AM.SERIE))
        cls.conf = D.config_homogene(D.classe_catalogue(cls.cat, "rs00"))

    def test_identite_a_H0(self):
        rc = D.reference_charge(self.ref, 0.6, 0.6)
        H0 = self.ref["H0"]
        self.assertAlmostEqual(D.masse(H0, rc, self.conf, self.besoins),
                               D.masse(H0, self.ref, self.conf, self.besoins), places=12)

    def test_charge_fixe_au_dela_de_H0(self):
        rc = D.reference_charge(self.ref, 0.6, 0.6)
        self.assertLess(D.masse(0.60, rc, self.conf, self.besoins),
                        D.masse(0.60, self.ref, self.conf, self.besoins))


if __name__ == "__main__":
    unittest.main()
