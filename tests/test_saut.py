"""Saut selon la profondeur d'accroupi : l'étude redonne la phase 3a à 40°, et un défaut se voit.

    .venv/bin/python -m unittest tests.test_saut -v

Créé le 2026-10-08 (lot 4a septies, règle 9 : l'étude vit dans le dépôt avec un test).
"""
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import exigences_physiques as EP  # noqa: E402
import saut as SA  # noqa: E402


class Saut(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cap, cls.an, cls.lignes = EP.tout()
        cls.R = {k: v["valeur"] for k, v in cls.an["ratios"].items()}
        cls.jambe = EP.lire("exigences_S.yaml")["releve"]["repartition_jambes"]["valeur"]
        cls.alpha = EP.lire("exigences_S.yaml")["releve"]["inclinaison_tibia_deg"]["valeur"]

    def test_meme_calcul_que_la_phase_3a(self):
        b = SA.besoins_saut(0.55, 10, self.alpha, self.R, self.jambe)
        for art in SA.ARTS:
            l = next(x for x in self.lignes if x["tache"] == "saut_vertical" and x["niveau"] == 10
                     and x["articulation"] == art and abs(x["H"] - 0.55) < 1e-9)
            self.assertAlmostEqual(b["art"][art]["w"], l["omega"])
            self.assertAlmostEqual(b["art"][art]["tau_kg"], l["a"])

    def test_plus_profond_plus_lent(self):
        w = [SA.besoins_saut(0.6, 10, a, self.R, self.jambe)["art"]["knee"]["w"] for a in SA.ALPHAS]
        self.assertEqual(w, sorted(w, reverse=True))           # un accroupi plus profond allonge la poussée

    def test_robstride_trop_lent_vu(self):
        b = SA.besoins_saut(0.6, 10, 40, self.R, self.jambe)
        rapide = [dict(id="x", pointe=36.0, w=100.0)]
        lent = [dict(id="x", pointe=36.0, w=1.0)]
        self.assertGreater(SA.tient(b, rapide, 1.5)["M_max"], 0.0)
        self.assertEqual(SA.tient(b, lent, 1.5)["M_max"], 0.0)
