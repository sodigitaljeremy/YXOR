"""Explorateur : maximum par articulation, plus petit actionneur vérifiable, robustesse à la bande de b, INCONNU.

    .venv/bin/python -m unittest tests.test_explorateur -v

Créé le 2026-10-07. Le contrôle du maximum est vu ÉCHOUER sur un cas faussé
(somme au lieu du maximum) ; tout se joue sur un contexte construit ici, sans
CAO ni séries de simulation.
"""
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import explorateur as X  # noqa: E402

H = 0.6
# deux tâches sur le même axe : le maximum n'est PAS la somme
T = {(H, "marche_sol_plat", 0.3): {"knee": dict(pk=[(0.5, 0.0)], c=[(0.2, 0.0)], w=[3.0])},
     (H, "saut_vertical", 5): {"knee": dict(pk=[(0.3, 1.0)], c=[], w=[5.0])}}
PROFIL = {"marche_sol_plat": 0.3, "saut_vertical": 5}


def act(i, masse, pointe, continu=None, vitesse=50.0, prix=100.0, D=50.0, par_blocage=False):
    return dict(id=i, masse=masse, pointe=pointe, continu=continu, vitesse=vitesse, prix=prix, D=D,
                par_blocage=par_blocage)


def ctx(acts, ex=None, mmin=None):
    return dict(T=T, act={"f": acts, "p": [act("servo", 0.01, 1.0, 0.5)]}, marge=1.5, jeu=2.0, memo={},
                ex=ex or dict(bas=2.0, central=2.0, haut=2.0, iso=3.0),
                struct=dict(m_struct_S=1.0, k=1.0, H_S=0.6, charge=0.0),
                C={H: mmin or {}}, R={"hauteur_hanche": 0.5, "cuisse": 0.25, "tibia": 0.23, "largeur_bassin": 0.2,
                                     "bras": 0.19, "avant_bras": 0.15})


class Maximum(unittest.TestCase):
    def test_maximum_par_articulation(self):
        b = X.besoins(T, H, PROFIL, 10.0)
        self.assertAlmostEqual(b["knee"]["pk"], max(0.5 * 10, 0.3 * 10 + 1))
        self.assertEqual(X.verifier_maximum(b, T, H, PROFIL, 10.0), [])

    def test_maximum_fausse_vu_echouer(self):
        b = X.besoins(T, H, PROFIL, 10.0, combine=lambda x, y: x + y)       # somme : FAUX
        ecarts = X.verifier_maximum(b, T, H, PROFIL, 10.0)
        self.assertTrue(any(e.startswith("knee.pk") for e in ecarts), ecarts)


class Choix(unittest.TestCase):
    def test_plus_petit_verifiable(self):
        acts = [act("a", 0.1, 5.0), act("b", 0.2, 20.0, prix=None), act("c", 0.3, 20.0)]
        need = dict(pk=10.0, c=0.0, w=0.0)
        self.assertEqual(X.choisir(acts, need, 1.5), 2)                    # b passe mais sans prix : c, vérifiable

    def test_repli_inconnu(self):
        acts = [act("a", 0.1, 5.0), act("b", 0.2, 20.0, prix=None)]
        self.assertEqual(X.choisir(acts, dict(pk=10.0, c=0.0, w=0.0), 1.5), 1)


class Evaluation(unittest.TestCase):
    ENS = {"knee": 2}

    def test_faisable(self):
        r = X.evaluer(ctx([act("a", 0.1, 100.0, 100.0)]), self.ENS, H, "f", "p", PROFIL)
        self.assertEqual(r["statut"], "faisable", r)

    def test_donnee_absente_inconnu(self):
        r = X.evaluer(ctx([act("a", 0.1, 100.0, None)]), self.ENS, H, "f", "p", PROFIL)
        self.assertEqual(r["statut"], "INCONNU")
        self.assertIn("couple continu de a", r["inconnues"])

    def test_robuste_a_la_bande(self):
        # à H = 2 × H_S : M = 2 kg au b central (besoin 1,5 × 1,6 = 2,4 N·m), 8 kg au b haut (1,5 × 4 = 6 N·m) ; pointe 5
        T2 = {(1.2, t, n): v for (h, t, n), v in T.items()}
        c = ctx([act("a", 0.0, 5.0, 9.0)], ex=dict(bas=1.0, central=1.0, haut=3.0, iso=3.0))
        c["T"], c["C"] = T2, {1.2: {}}
        r = X.evaluer(c, self.ENS, 1.2, "f", "p", PROFIL)
        self.assertEqual(r["statut"], "infaisable", r)
        c2 = ctx([act("a", 0.0, 5.0, 9.0)], ex=dict(bas=1.0, central=1.0, haut=1.0, iso=3.0))
        c2["T"], c2["C"] = T2, {1.2: {}}
        self.assertEqual(X.evaluer(c2, self.ENS, 1.2, "f", "p", PROFIL)["statut"], "faisable")

    def test_masse_minimale(self):
        r = X.evaluer(ctx([act("a", 0.1, 100.0, 100.0)], mmin={("saut_vertical", 5): 50.0}),
                      self.ENS, H, "f", "p", PROFIL)
        self.assertEqual(r["statut"], "infaisable")


class Ensembles(unittest.TestCase):
    def test_nombres_d_axes(self):
        self.assertEqual({k: sum(e["axes"].values()) for k, e in X.ENSEMBLES.items()}, {25: 25, 26: 26, 27: 27, 29: 29})

    def test_pareto(self):
        s = lambda c, m, n: dict(statut="faisable", cout=c, M=m, E=m, ncap=n)
        front = X.pareto([s(1, 1, 1), s(2, 2, 1), s(2, 2, 2), s(1, 1, 1)])
        self.assertEqual(sorted((p["cout"], p["ncap"]) for p in front), [(1, 1), (2, 2)])


if __name__ == "__main__":
    unittest.main()
