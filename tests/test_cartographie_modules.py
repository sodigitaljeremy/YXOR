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

    def test_alias_nom_identifiant(self):
        # le Kit nomme ses pièces, l'explorateur les identifie : le Pi 5 du Kit doit être reconnu dans le Lab
        ms = [dict(nom="K", gamme="Kit", items=[item("Raspberry Pi 5 8GB", 1, 150.0, "cerveau")]),
              dict(nom="L", gamme="Lab", items=[dict(item("rpi5_8gb", 1, 150.0, "cerveau"), nom="Raspberry Pi 5 8GB")])]
        self.assertEqual(C.parcourir(ms)[1]["deja"], 150.0)

    def test_nomenclature_alignee(self):
        its = [item("orion_jr2", 1, 587.6, "énergie"), item("molicel_p50b", 3, 8.4, "énergie"),
               item("pololu_d42v55f5", 1, 33.6, "énergie"), item("ws_2ch_can_fd_hat", 2, 39.2, "bus"),
               dict(item("maytech_mts2009as", 1, 74.2, "énergie"), nom="anti-spark switch 300A 20-85V")]
        its[1]["nom"] = "INR-21700-P50B (pack 3S1P)"
        out = {i["produit"] for i in C.corriger_aligne(its)}
        self.assertNotIn("orion_jr2", out)
        self.assertNotIn("maytech_mts2009as", out)        # défaut vu le 2026-10-11 : « 85V » contenait « 5V »
        self.assertNotIn("ws_2ch_can_fd_hat", out)
        self.assertTrue({"molicel_p50b", "pololu_d42v55f5"} <= out)
        self.assertTrue(any(str(p).startswith("bms3s:") for p in out))

    def test_bms_prudent(self):
        # la recommandation « 50 % en continu » du vendeur ramène ses BMS de 40 A à 20 A, sous les 23,7 A du Kit
        for b in C.bms_3s_tous():
            if "40A" in b["nom"] and "generique" in b["nom"] and "HW-552" not in b["nom"]:
                self.assertEqual(b["I"], 20.0)
        self.assertGreaterEqual(C.bms_3s(C.I_UNIQUE)["I"], C.I_UNIQUE)

    def test_tension_sts3250(self):
        L = "\n".join(C.rapport_3s(13.2))
        self.assertRegex(L, r"STS3250 12 V .*\*\*dépassée de 0,6 V\*\*")

    def test_rapport_a_jour(self):
        self.assertEqual(C.document(C.tout()), C.DOC.read_text(encoding="utf-8"),
                         "relancer : scripts/cartographie_modules.py --ecrire")


if __name__ == "__main__":
    unittest.main()
