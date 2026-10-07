"""Études reconstruites du 2026-10-03 et 04 : elles redonnent les chiffres d'alors, et un écart se voit.

    .venv/bin/python -m unittest tests.test_etudes_reconstruites -v

Créé le 2026-10-07 (règle de Jeremy du même jour : toute étude réutilisée par un
calcul vit dans le dépôt, avec un test). Chiffres d'alors, relevés dans la
transcription de la session :
  · taille minimale (hmin_ecart.py, 2026-10-04) : 27 axes 0,613 m avec écarts,
    0,642 m en proportions strictes ; 26 axes 0,664 m et 0,809 m ;
  · structure (etude_s_c.py, 2026-10-04) : v3 pleine 3 mm 3,92 kg, évidée 50 % +
    2 mm 1,85 kg (la reconstruction donne 1,86 : largeur de la cuisse, écrit).
La structure demande la CAO (une minute la première fois, puis le cache de
exports/) et `git archive` du commit 0b5e304 : sans eux, le test SAUTE et le dit.
"""
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import structure_plaques as SP  # noqa: E402
import taille_minimale as TM  # noqa: E402


class TailleMinimale(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cv = TM.conventions()
        cls.RA = {k: x["valeur"] for k, x in TM.lire("anthropometry.yaml")["ratios"].items()}

    def ev(self, k, jambe=None):
        return TM.evaluer(TM.ENSEMBLES_0410[k], TM.moteurs_robstride(jambe or TM.JAMBE_0410[k], self.cv), 0.60,
                          self.RA, self.cv)

    def test_chiffres_du_2026_10_04(self):
        for k, (h_ecart, h_ansur) in TM.ATTENDU_0410.items():
            r = self.ev(k)
            self.assertAlmostEqual(r["H_reel"], h_ecart, delta=0.0006, msg=k)
            self.assertAlmostEqual(r["H_min_ansur"], h_ansur, delta=0.0006, msg=k)
            self.assertEqual(r["limitante_ansur"], "tronc")

    def test_moteur_plus_gros_vu(self):
        # un RS02 au tangage de hanche (au lieu du RS00) allonge le tronc du 26 : 0,675 m, plus 0,664
        jb = dict(TM.JAMBE_0410[26], hip_pitch="rs02")
        r = self.ev(26, jb)
        self.assertGreater(r["H_reel"], TM.ATTENDU_0410[26][0] + 0.005)

    def test_lecture_des_cotes(self):
        self.assertEqual(TM.moteur_dims("Ø57 × 51", self.cv)["R"], 28.5)
        self.assertEqual(TM.moteur_dims("45,2 × 24,7 × 35", self.cv)["L"], 45.2)
        self.assertIsNone(TM.moteur_dims(None, self.cv))


def _archive_ok():
    return subprocess.run(["git", "cat-file", "-e", SP.COMMIT_A], cwd=REPO).returncode == 0


@unittest.skipUnless(_archive_ok(), f"commit {SP.COMMIT_A} absent (clone superficiel ?) : étalonnage impossible")
class Structure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = SP.modele()

    def test_chiffres_du_2026_10_04(self):
        self.assertAlmostEqual(SP.structure(self.m, "pleine 3 mm"), 3.92, delta=0.02)
        self.assertAlmostEqual(SP.structure(self.m, "évidée 50 % + 2 mm"), 1.85, delta=0.02)

    def test_etalonnage(self):
        self.assertAlmostEqual(self.m["K"]["cote"], 0.92, delta=0.01)
        self.assertAlmostEqual(self.m["K"]["liaison"], 0.92, delta=0.01)

    def test_ordre_des_variantes_et_ecart_vu(self):
        v = [SP.structure(self.m, n) for n, _, _ in SP.VARIANTES]
        self.assertEqual(v[0], max(v))                      # la pleine est la plus lourde
        self.assertEqual(v[-1], min(v))                     # évidée 50 % + 2 mm la plus légère
        # un axe de plus et le roulis de cheville alourdissent ; un étalonnage faussé se voit
        self.assertGreater(SP.structure(self.m, "pleine 3 mm", n_rs05_de_plus=1, roulis_cheville=True), v[0])
        faux = dict(self.m, K=dict(self.m["K"], cote=2 * self.m["K"]["cote"]))
        self.assertGreater(SP.structure(faux, "pleine 3 mm") - v[0], 0.5)


if __name__ == "__main__":
    unittest.main()
