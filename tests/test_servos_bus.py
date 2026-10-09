"""Familles de servos à bus (scripts/servos_bus.py) : rapport à jour ; le calcul du point 3 sait dire oui et non.

    .venv/bin/python -m unittest tests.test_servos_bus -v

Créé le 2026-10-09 (règle 9). Étude, aucune décision.
"""
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import servos_bus as SB  # noqa: E402


class ServosBus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ms = SB.modeles()
        cls.bes = SB.besoins_leger()

    def test_rapport_a_jour(self):
        txt = SB.rapport(self.ms, SB.familles(self.ms), self.bes, SB.point3(self.ms, self.bes, 1.5))
        self.assertEqual(txt, SB.DOC.read_text(encoding="utf-8"), "relancer : scripts/servos_bus.py --ecrire")

    def test_un_servo_fictif_qui_tient(self):
        # défaut inverse simulé : un servo assez fort ET assez rapide fait passer sa famille
        fort = dict(id="fictif", famille="Fictive", blocage=50.0, continu=None, vitesse=50.0, tension=12, masse=0.1,
                    prix=10.0, prix_brut=None)
        p3 = SB.point3(self.ms + [fort], self.bes, 1.5)
        self.assertTrue(p3["Fictive"]["tient"])
        lent = dict(fort, famille="Lente", vitesse=1.0)
        self.assertFalse(SB.point3([lent], self.bes, 1.5)["Lente"]["tient"])

    def test_toutes_les_familles(self):
        fams = {m["famille"] for m in self.ms}
        for f in ("Hiwonder", "Waveshare", "Kondo", "HerkuleX", "Feetech", "Dynamixel"):
            self.assertIn(f, fams)


if __name__ == "__main__":
    unittest.main()
