"""Rayon intérieur minimal = max(0,5 x épaisseur, limite de machine du réglage).

    .venv/bin/python -m unittest tests.test_rayon_min -v

Créé le 2026-10-01 (21 h). La limite de machine déclarée par l'opérateur CN
(2,0 mm) n'était lue par aucun code : en aluminium de 3 mm, une pièce aux
congés de 1,5 mm passait tout au vert, et aurait été infaisable.
"""
import copy
import sys
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import procedes as P  # noqa: E402


class RayonInterieurMin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hw = P.charger()

    def test_regle(self):
        self.assertEqual(P.rayon_interieur_min(5.0), 2.5)             # carton plume : matière
        self.assertEqual(P.rayon_interieur_min(3.0, 2.0), 2.0)        # alu 3 mm : la machine l'emporte
        self.assertEqual(P.rayon_interieur_min(6.0, 2.0), 3.0)        # 6 mm : la matière l'emporte
        self.assertIsNone(P.rayon_interieur_min(None, 2.0))

    def test_reglage_alu_3_a_1_5_refuse(self):
        hw = copy.deepcopy(self.hw)
        r = next(x for x in hw["reglages"] if x["id"] == "operateur_cn_alu_3")
        r["rayon_interieur_min"] = 1.5
        fautes = P.controler_rayon(hw)
        self.assertTrue(any("operateur_cn_alu_3" in f for f in fautes), fautes)

    def test_piece_alu_3_conge_1_5_refusee(self):
        fautes = P.controler_pieces([{"nom": "essai", "reglage": "operateur_cn_alu_3",
                                      "rayon_rentrant_min_mm": 1.5}], self.hw)
        self.assertTrue(any("essai" in f for f in fautes), fautes)
        self.assertEqual(P.controler_pieces([{"nom": "essai", "reglage": "operateur_cn_alu_3",
                                              "rayon_rentrant_min_mm": 2.0}], self.hw), [])

    def test_depot_reel(self):
        self.assertEqual(P.controler_rayon(), [])
        releves = [yaml.safe_load(f.read_text(encoding="utf-8"))["piece"]
                   for f in sorted((REPO / "parts").glob("*.origines.yaml"))]
        self.assertTrue(releves)
        self.assertEqual(P.controler_pieces(releves), [])


if __name__ == "__main__":
    unittest.main()
