"""Marchés des batteries, calculateurs et cartes de bus : calculs dérivés, tension, canaux CAN, sources, rapports.

    .venv/bin/python -m unittest tests.test_marche_composants -v

Créé le 2026-10-07. Chaque contrôle est vu ÉCHOUER sur un défaut fait exprès ; le
bourrage CAN est vérifié par une simulation bit à bit, indépendante de la formule.
"""
import copy
import sys
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import marche_composants as MC  # noqa: E402


def bourrage_simule(n):
    """Pire cas : la suite qui provoque le plus de bits insérés sur n bits bourrables (simulation de la règle Bosch)."""
    meilleure = 0
    for depart in range(1, 6):                     # longueur de la première suite (le reste alterne au pire)
        bits, b, k = [], 0, depart
        while len(bits) < n:
            bits += [b] * k
            b, k = 1 - b, 4
        bits = bits[:n]
        ins, run, prec = 0, 0, None
        for x in bits:
            run = run + 1 if x == prec else 1
            prec = x
            if run == 5:                           # bit complémentaire inséré, il ouvre une nouvelle suite
                ins, prec, run = ins + 1, 1 - x, 1
        meilleure = max(meilleure, ins)
    return meilleure


class Can(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b = MC.lire("bus.yaml")

    def test_bourrage_formule_egale_simulation(self):
        for n in (98, 118, 50, 5, 6):
            self.assertEqual((n - 1) // 4, bourrage_simule(n), n)

    def test_trames(self):
        self.assertEqual(MC.bits_trame(self.b["trame_can"], True)["total"], 164)     # 118 + 29 + 17
        self.assertEqual(MC.bits_trame(self.b["trame_can"], False)["total"], 139)    # 98 + 24 + 17

    def test_champ_fausse_vu(self):
        t = copy.deepcopy(self.b["trame_can"])
        t["crc_sequence_bits"]["valeur"] = None
        self.assertIsNone(MC.bits_trame(t, True))                                      # non lu : pas de calcul
        t = copy.deepcopy(self.b["trame_can"])
        t["eof_bits"]["valeur"] = 10
        self.assertNotEqual(MC.bits_trame(t, True)["total"], 164)

    def test_canaux(self):
        c = MC.canaux_can(27, 500, 2, 164, 1e6, 0.7)
        self.assertAlmostEqual(c["besoin"], 27 * 500 * 2 * 164)
        self.assertEqual(c["canaux"], 7)


class Tension(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bat = MC.lire("batteries.yaml")
        cls.g = MC.groupes(MC.plages("robstride"))

    def test_li_ion(self):
        t = {r["S"]: r for r in MC.tableau_tension(self.bat, self.g) if r["chimie"] == "li_ion" and r.get("S")}
        self.assertTrue(t[13]["ok"][(24.0, 60.0)] and t[13]["regen_ok"])
        self.assertTrue(t[14]["ok"][(24.0, 60.0)])
        self.assertFalse(t[14]["regen_ok"])                    # 58,8 V : 1,2 V sous la protection de 60 V
        self.assertFalse(t[15]["ok"][(24.0, 60.0)])

    def test_plage_la_plus_etroite(self):
        rs = {x["id"]: x for x in MC.plages("robstride")}
        self.assertEqual((rs["rs02"]["min"], rs["rs02"]["max"]), (24.0, 60.0))   # README 24–60 plutôt que 15–60
        self.assertEqual((rs["rs01"]["min"], rs["rs01"]["max"]), (24.0, 48.0))

    def test_constante_faussee_vue(self):
        b = copy.deepcopy(self.bat)
        b["chimies"]["li_ion"]["tension_max_V"]["valeur"] = 4.35
        t = {r["S"]: r for r in MC.tableau_tension(b, self.g) if r["chimie"] == "li_ion" and r.get("S")}
        self.assertFalse(t[13]["regen_ok"])


class Batteries(unittest.TestCase):
    def test_volume(self):
        self.assertAlmostEqual(MC.volume_l({"diametre": 21.0, "hauteur": 70.0}), 0.024245, places=5)
        self.assertAlmostEqual(MC.volume_l({"valeur": "100 x 50 x 20"}), 0.1)
        self.assertIsNone(MC.volume_l(None))

    def test_serie_interdite_respectee(self):
        bat = MC.lire("batteries.yaml")
        b = dict(id="x", E=100.0, m=1.0, I=10.0, prix=10.0, p={"famille": "lifepo4", "chimie": {"valeur": "LiFePO4"},
                 "tension_nominale_V": {"valeur": 12.8}, "bms": {"valeur": "oui", "note": "SÉRIE INTERDITE"}})
        self.assertIsNone(MC.composer(b, bat, 10.0, 24.0, 55.0))              # 4S seul : sous 24 V, et pas de série
        b["p"]["bms"]["note"] = ""
        self.assertIsNotNone(MC.composer(b, bat, 10.0, 24.0, 55.0))


class Sources(unittest.TestCase):
    def sources_citees(self, d):
        out = set()
        def walk(x):
            if isinstance(x, dict):
                for k, val in x.items():
                    if k in ("source", "fiche") and isinstance(val, str) and val.startswith("marche_"):
                        out.add(val)
                    else:
                        walk(val)
            elif isinstance(x, list):
                for val in x:
                    walk(val)
        walk({k: val for k, val in d.items() if k != "marche"})
        walk(d["marche"]["produits"])
        return out

    def manquantes(self, d, registre):
        return sorted(s for s in self.sources_citees(d) if s not in d["marche"]["sources"] or s not in registre)

    def test_toute_source_citee_existe_et_est_au_registre(self):
        reg = yaml.safe_load((REPO / "params" / "fournisseurs.yaml").read_text(encoding="utf-8"))["fichiers"]
        for nom in ("batteries.yaml", "calculateurs.yaml", "bus.yaml"):
            d = MC.lire(nom)
            self.assertEqual(self.manquantes(d, reg), [], nom)
        d = copy.deepcopy(MC.lire("bus.yaml"))
        next(iter(d["marche"]["produits"].values()))["prix"]["source"] = "marche_bus_inventee"
        self.assertEqual(self.manquantes(d, reg), ["marche_bus_inventee"])          # vu échouer


class Rapports(unittest.TestCase):
    def test_a_jour(self):
        bat, cal, b = MC.lire("batteries.yaml"), MC.lire("calculateurs.yaml"), MC.lire("bus.yaml")
        self.assertEqual(MC.rapport_batteries(bat, MC.batteries(bat)), MC.DOCS["batteries"].read_text(encoding="utf-8"))
        self.assertEqual(MC.rapport_calculateurs(cal, MC.calculateurs(cal)), MC.DOCS["calculateurs"].read_text(encoding="utf-8"))
        self.assertEqual(MC.rapport_bus(b, MC.bus(b), MC.calcul_can(b)), MC.DOCS["bus"].read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
