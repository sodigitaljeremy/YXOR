"""Plans du niveau 0 du Kit (parts/kit_niveau0.py) : pièces d'un seul tenant, contrôles 2D et 3D qui voient un
défaut simulé, tuilage des grandes pièces.

    .venv/bin/python -m unittest tests.test_kit_niveau0 -v

Créé le 2026-10-08. Le contrôle 3D complet tourne dans la pièce elle-même (scripts/regenerer.py) ; ici, un
caisson seul, pour voir le contrôle échouer (CLAUDE.md : « un contrôle nouveau se voit échouer »).
"""
import importlib.util
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
_spec = importlib.util.spec_from_file_location("kit_niveau0", REPO / "parts" / "kit_niveau0.py")
K = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(K)


def exclus(a, b):
    n0 = ("bouchon" in a or "serrage" in a, "bouchon" in b or "serrage" in b)
    return (n0[0] and b.startswith("servo")) or (n0[1] and a.startswith("servo"))


class Niveau0(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g = K.donnees()

    def caisson(self, W):
        g, e = self.g, self.g["e"]
        c = K.Caisson("t", (0, 50, 200), K.vneg(K.Z), K.Y, 150, W, 2 * (g["Bw"] / 2 + g["vo"] + 2 * e), g)
        c.logement("flanc", 1, 20, 0.0, "a", 1, "knee")
        c.cloisons.append(100)
        pls = [p.finir(g) for p in c.plaques()]
        sol = [(f"{p.nom}{k}", s) for p in pls for k, s in enumerate(p.solides())]
        return c, pls, sol

    def test_juste_sans_defaut(self):
        g = self.g
        c, pls, sol = self.caisson(g["int_servo"] + 2 * g["e"])
        self.assertEqual(K.interferences(sol + c.servos(), exclus), [])
        for p in pls:
            self.assertEqual(K.controler_2d(K.polylignes_depuis_face(p.face.faces()[0]), g["r"]), [], p.nom)

    def test_servo_trop_large_vu(self):
        g = self.g
        c, _, sol = self.caisson(g["int_servo"] + 2 * g["e"] - 8)        # le servo ne tient plus entre les flancs
        self.assertTrue(any("servo" in x for x in K.interferences(sol + c.servos(), exclus)))

    def test_tenon_sans_mortaise_vu(self):
        orig = K.mortaise
        try:
            K.mortaise = lambda es, axe, c, b0, g: None if axe == "a" else orig(es, axe, c, b0, g)   # mortaises le long de u oubliées
            c, _, sol = self.caisson(self.g["int_servo"] + 2 * self.g["e"])
        finally:
            K.mortaise = orig
        self.assertTrue(K.interferences(sol, exclus))

    def test_angle_vif_vu(self):
        # défaut simulé : une fenêtre sans os de chien a quatre angles rentrants vifs
        g = self.g
        es = K.Esquisse(K.rect(0, 100, 0, 60))
        es.retirer(K.rect(30, 70, 20, 40))
        f = es.face()
        self.assertTrue(K.controler_2d(K.polylignes_depuis_face(f.faces()[0]), g["r"]))

    def test_tuiles(self):
        zl, zh = K.ZONE_PLANCHE
        grand = [[(0, 0), (zl * 1.5, 0), (zl * 1.5, zh * 0.5), (0, zh * 0.5)]]
        feuilles, tuilees = K.ranger([("grand", grand, "a")], 10.0)
        self.assertEqual(len(tuilees), 1)
        self.assertEqual(len(feuilles), 2)

    def test_notice_a_jour(self):
        txt = K.NOTICE.read_text(encoding="utf-8")
        self.assertIn("Engendrée", txt)
        self.assertIn("aucune interpénétration en 3D", txt)                    # la dernière régénération était propre


if __name__ == "__main__":
    unittest.main()
