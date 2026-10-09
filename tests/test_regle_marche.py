"""Option --regle-marche de l'explorateur (2026-10-09) : avec « explorateur » (défaut), les sorties sont IDENTIQUES à
celles du commit cc340fd ; avec « plus_lente », la marche la plus lente au moins aussi rapide, sans interpolation.

    .venv/bin/python -m unittest tests.test_regle_marche -v
"""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import exigences_physiques as EP  # noqa: E402
import explorateur as X  # noqa: E402
import marche_lente as ML  # noqa: E402
import simulations_marche as SM  # noqa: E402
import systeme_electrique as SE  # noqa: E402

COMMIT = "cc340fd"


def ancien(nom):
    """Le module `nom` tel qu'il était au commit cc340fd (lu dans Git, chargé sous un autre nom)."""
    src = subprocess.run(["git", "show", f"{COMMIT}:scripts/{nom}.py"], cwd=REPO, capture_output=True, text=True,
                         check=True).stdout
    d = Path(tempfile.mkdtemp())
    f = d / f"{nom}_{COMMIT}.py"
    f.write_text(src, encoding="utf-8")
    spec = importlib.util.spec_from_file_location(f.stem, f)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class RegleMarche(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cap, cls.an, cls.lignes = EP.tout()
        cls.m, cls.r, _ = SM.charger()

    def test_defaut_identique_a_cc340fd(self):
        Xo, SEo = ancien("explorateur"), ancien("systeme_electrique")
        self.assertEqual(X.table_besoins(self.lignes, self.m, self.r, self.cap),
                         Xo.table_besoins(self.lignes, self.m, self.r, self.cap))
        self.assertEqual(SE.table_puissance(self.m, self.cap, EP.HS), SEo.table_puissance(self.m, self.cap, EP.HS))
        # une solution complète (le Lab actuel), même statut, même masse, même coût
        c_new = X.contexte(profil="lab", S=12, f_can=250, coupure=3.0, chaine="compacte")
        c_old = Xo.contexte(profil="lab", S=12, f_can=250, coupure=3.0, chaine="compacte")
        for H in (0.65, 0.85):
            a = X.evaluer(c_new, 27, H, "robstride", "feetech", c_new["cible"])
            b = Xo.evaluer(c_old, 27, H, "robstride", "feetech", c_old["cible"])
            self.assertEqual((a["statut"], a.get("M"), a.get("cout"), a.get("violees")),
                             (b["statut"], b.get("M"), b.get("cout"), b.get("violees")))

    def test_plus_lente_une_seule_marche_ou_aucune(self):
        frs = {k: e["Fr"] for k, e in self.m.items()}
        self.assertEqual(ML.selection(frs, 0.15, 0.60, "plus_lente"), ["ToddlerBot"])
        self.assertEqual(len(ML.selection(frs, 0.15, 0.60, "explorateur")), 3)
        self.assertEqual(ML.selection(frs, 5.0, 0.60, "plus_lente"), [])              # aucune : null, pas d'interpolation
        with self.assertRaises(ValueError):
            ML.selection(frs, 0.15, 0.60, "interpolee")

    def test_plus_lente_baisse_les_vitesses(self):
        T1 = X.table_besoins(self.lignes, self.m, self.r, self.cap, "explorateur")
        T2 = X.table_besoins(self.lignes, self.m, self.r, self.cap, "plus_lente")
        w = lambda T: max(T[(0.6, "marche_sol_plat", 0.3)]["knee"]["w"])
        self.assertLessEqual(w(T2), w(T1))


if __name__ == "__main__":
    unittest.main()
