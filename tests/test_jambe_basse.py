"""Jambe basse en plaques : les contrôles 2D se voient échouer, les trous suivent le réglage, la cheville ne se chevauche plus.

    .venv/bin/python -m unittest tests.test_jambe_basse -v

Créé le 2026-10-03. Chaque contrôle de parts/jambe_basse.py (voile, rayon
rentrant) est d'abord vu ÉCHOUER sur une pièce fautive faite exprès, puis
passer sur une pièce saine (CLAUDE.md, « un contrôle nouveau se voit échouer »).
"""
import importlib.util
import sys
import unittest
from pathlib import Path

import build123d as bd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
_spec = importlib.util.spec_from_file_location("jambe_basse", REPO / "parts" / "jambe_basse.py")
JB = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(JB)


def plaque_test(esquisse, trous=()):
    pl = JB.Plaque("essai", esquisse, list(trous), [bd.Location()], "essai", "essai")
    return pl.finir(3.0, 3.0)


G_ALU = {"e": 3.0, "r": 2.0, "d_min": 3.0, "reg": {"voile_min": 6.0}}


class ControlesSeVoientEchouer(unittest.TestCase):
    def test_voile_trop_mince_detecte(self):
        # trou Ø3,4 à 3 mm du bord : bande de 3 - 1,7 = 1,3 mm < 6
        pl = plaque_test(JB.rect(0, 40, 0, 40), [(20, 3.0, 3.4)])
        self.assertTrue(any("voile" in f for f in JB.controler(pl, G_ALU)))

    def test_voile_suffisant_passe(self):
        pl = plaque_test(JB.rect(0, 40, 0, 40), [(20, 20, 3.4)])
        self.assertEqual(JB.controler(pl, G_ALU), [])

    def test_fente_vide_n_est_pas_un_voile(self):
        # deux bords à 3 mm l'un de l'autre, mais séparés par du VIDE (encoche)
        pl = plaque_test(JB.rect(0, 40, 0, 40) - JB.rect(18.5, 21.5, 30, 41)
                         - JB.degagement([(18.5, 30 + 2.0), (21.5, 30 + 2.0)], 2.0))
        self.assertEqual([f for f in JB.controler(pl, G_ALU) if "voile" in f], [])

    def test_angle_rentrant_vif_detecte(self):
        # un L sans congé : un angle rentrant vif
        pl = plaque_test(JB.rect(0, 40, 0, 10) + JB.rect(0, 10, 0, 40))
        self.assertTrue(any("angle rentrant vif" in f for f in JB.controler(pl, G_ALU)))

    def test_arc_rentrant_trop_petit_detecte(self):
        # encoche demi-ronde de rayon 1 < 2
        pl = plaque_test(JB.rect(0, 40, 0, 40) - JB.disque(20, 40, 1.0))
        self.assertTrue(any("arc rentrant" in f for f in JB.controler(pl, G_ALU)))

    def test_degagement_en_t_laisse_le_tenon_entier(self):
        # un tenon de 12 x 3 sous une plaque, dégagé : ni angle vif, ni crochet
        s = JB.rect(-20, 20, 3, 30) + JB.rect(-6, 6, 0, 3) - JB.degagement([(-8, 3), (8, 3)], 2.0)
        self.assertEqual(JB.controler(plaque_test(s), G_ALU), [])


class TrousSuiventLeReglage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = {}
        for rid in JB.REGLAGES:
            g = JB.donnees(rid)
            G = JB.geometrie(g)
            P = JB.plaques_structure(g, G)
            for pl in P:
                pl.finir(g["e"], g["d_min"])
            cls.p[rid] = (g, G, P)

    def test_carton_marque_les_petits_trous(self):
        g, _, P = self.p[JB.REGLAGE_CARTON]
        self.assertGreater(sum(len(pl.marques) for pl in P), 0)
        for pl in P:
            for _, _, d in pl.coupes:
                self.assertGreaterEqual(d, g["d_min"], pl.nom)

    def test_alu_decoupe_les_trous_de_vis(self):
        g, _, P = self.p["operateur_cn_alu_3"]
        self.assertEqual(sum(len(pl.marques) for pl in P), 0)

    def test_meme_cinematique_pour_les_deux_reglages(self):
        Gs = [self.p[r][1] for r in JB.REGLAGES]
        for k in ("z_p", "z_k"):
            self.assertAlmostEqual(Gs[0][k], Gs[1][k], places=6, msg=k)

    def test_aucune_collision_au_repos(self):
        g, G, P = self.p["operateur_cn_alu_3"]
        sol = [s for pl in P for s in JB.placer(pl)] + JB.moteurs_cylindres(g, G)
        res = JB.balayer(sol, G, {"knee": (0, 0), "ankle_pitch": (0, 0)})
        for art, r in res.items():
            self.assertEqual(r["repos"], [], art)


class Cheville(unittest.TestCase):
    """Cheville sans roulis (fiche 0068) : un seul axe, au-dessus de la semelle."""

    def test_plus_de_roulis(self):
        jo = JB.lire("joints.yaml")
        self.assertNotIn("ankle_roll", {j["nom"] for j in jo["jambes"]})
        self.assertNotIn("ankle_roll", JB.lire("configuration_S.yaml")["jambes"])
        self.assertIn("ankle_roll", {x["nom"] for x in jo["amont_non_retenus"]})

    def test_plaque_du_tibia_passe_au_dessus_de_la_semelle(self):
        import squelette as SQ
        ec = SQ.ecarts_cheville()
        mid = JB.lire("squelette.yaml")["ecarts_ansur"]["cheville"]["actionneur"]
        cm = JB.lire("actionneurs.yaml")["candidats"][mid]["cotes_montage"]
        self.assertGreaterEqual(ec["r_plaque_mm"], cm["diametre_corps"] / 2)
        self.assertAlmostEqual(ec["hauteur_axe_cheville"] * 1000,
                               ec["e_max_mm"] + ec["jeu_mm"] + ec["r_plaque_mm"], places=6)


if __name__ == "__main__":
    unittest.main()
