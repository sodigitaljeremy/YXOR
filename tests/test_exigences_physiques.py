"""Exigences physiques : combinaison par le maximum, monotonie, rapport à jour.

    .venv/bin/python -m unittest tests.test_exigences_physiques -v

Créé le 2026-10-05 (phase 3a). La monotonie est d'abord vue ÉCHOUER sur une
table faussée exprès.
"""
import copy
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import exigences_physiques as EP  # noqa: E402


def non_monotones(lignes):
    """Couples (à M fixé) qui DÉCROISSENT quand le niveau ou H augmente : des défauts."""
    out, M = [], 10.0
    idx = {}
    for l in lignes:
        idx[(l["tache"], l["articulation"], l["niveau"], l["H"])] = l["a"] * M + l["b"]
    for (t, art, niv, H), v in idx.items():
        if not isinstance(niv, (int, float)):
            continue
        for (t2, a2, n2, H2), v2 in idx.items():
            if (t2, a2) == (t, art) and isinstance(n2, (int, float)) and n2 >= niv and H2 >= H and v2 < v - 1e-9:
                out.append((t, art, niv, H, n2, H2))
    return out


class Exigences(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cap, cls.an, cls.lignes = EP.tout()

    def test_combiner_prend_le_maximum(self):
        prof = {"saut_vertical": 30, "releve": "depuis le dos", "charge_lourde": 10}
        r = EP.combiner(self.lignes, prof, 1.0, 20.0)
        attendu = max(l["a"] * 20 + l["b"] for l in self.lignes if abs(l["H"] - 1.0) < 1e-9
                      and l["articulation"] == "knee" and l["tache"] in prof and l["niveau"] == prof[l["tache"]])
        self.assertAlmostEqual(r["knee"], attendu)
        self.assertIn("shoulder_pitch", r)            # vient de la seule charge

    def test_monotone(self):
        self.assertEqual(non_monotones(self.lignes), [])

    def test_monotonie_defaut_vu(self):
        faux = copy.deepcopy(self.lignes)
        for l in faux:
            if l["tache"] == "saut_vertical" and l["niveau"] == 30:
                l["a"] *= 0.1
        self.assertGreater(len(non_monotones(faux)), 0)

    def test_saut_geometrie_coherente(self):
        # ajouté le 2026-10-08 : la course de poussée est celle que donne la cinématique directe des deux segments
        import math
        L1, L2, a = 0.1238, 0.1134, math.radians(40)
        g = EP.geometrie_saut(L1, L2, a)
        hanche_accroupie = L2 * math.cos(a) + L1 * math.cos(g["beta"])
        self.assertAlmostEqual(L2 * math.sin(a) - L1 * math.sin(g["beta"]), 0.0)          # hanche à l'aplomb
        self.assertAlmostEqual(g["d"], L1 + L2 - hanche_accroupie)
        w = [l["omega"] for l in self.lignes if l["tache"] == "saut_vertical" and l["niveau"] == 10
             and l["articulation"] == "knee" and abs(l["H"] - 0.5) < 1e-9][0]
        self.assertAlmostEqual(w, 37.0, delta=0.1)                                          # 49,4 avant la correction
        self.assertLess(w, 49.0)

    def test_rapport_a_jour(self):
        md = EP.rapport(self.cap, self.an, self.lignes, EP.familles(), EP.refs_md())
        self.assertEqual(md, EP.DOC.read_text(encoding="utf-8"), "relancer : scripts/exigences_physiques.py --ecrire")
        self.assertEqual(EP.courbes_svg(self.lignes, self.cap), EP.SVG.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
