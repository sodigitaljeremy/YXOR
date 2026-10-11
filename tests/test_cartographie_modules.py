"""Cartographie des modules (scripts/cartographie_modules.py) : réemploi juste, rapport à jour.

    .venv/bin/python -m unittest tests.test_cartographie_modules -v

Créé le 2026-10-11 (règle 9 ; fiche 0077 : réemploi maximal, une seule batterie pour le Kit et le Lab).
"""
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import cartographie_modules as C  # noqa: E402


def item(prod, n, prix, module="petits axes"):
    return dict(nom=prod, produit=prod, n=n, prix=prix, classe="DURABLE", module=module)


class Cartographie(unittest.TestCase):
    def test_reemploi_par_produit(self):
        ms = [dict(nom="K1", gamme="Kit", items=[item("sts3215", 2, 20.0)]),
              dict(nom="K2", gamme="Kit", items=[item("sts3215", 3, 20.0), item("rpi5", 1, 150.0, "cerveau")]),
              dict(nom="L", gamme="Lab", items=[item("sts3215", 1, 20.0), item("j3011", 1, 500.0, "cerveau")])]
        p = C.parcourir(ms)
        self.assertEqual(p[1]["deja"], 40.0)              # 2 servos déjà achetés, le 3e est neuf
        self.assertEqual(p[1]["neuf"], 170.0)
        self.assertEqual(p[2]["deja"], 20.0)
        self.assertEqual(p[2]["entre_cat"], 20.0)         # acheté dans le Kit (Initiation), réemployé dans le Lab
        self.assertEqual(p[2]["invest"], 40 + 170 + 500)          # 2 servos, puis 1 servo + Pi 5, puis le Jetson

    def test_defaut_vu(self):
        # défaut simulé : un produit sans identifiant n'est jamais compté comme réemployé
        ms = [dict(nom="K1", gamme="Kit", items=[item(None, 1, 10.0)]),
              dict(nom="K2", gamme="Kit", items=[item(None, 1, 10.0)])]
        self.assertEqual(C.parcourir(ms)[1]["deja"], 0.0)

    def test_rapport_a_jour(self):
        self.assertEqual(C.rapport(*C.tout()), C.DOC.read_text(encoding="utf-8"),
                         "relancer : scripts/cartographie_modules.py --ecrire")


if __name__ == "__main__":
    unittest.main()
