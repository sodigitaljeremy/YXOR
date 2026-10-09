"""Marchés versés le 2026-10-09 (capteurs, temps réel, chargeurs 12S, Hailo-8 M.2, actionneurs complémentaires) :
chaque source citée existe au registre (params/fournisseurs.yaml) ; le relevé d'actionneurs n'entre pas dans le calcul.

    .venv/bin/python -m unittest tests.test_marches_complements -v
"""
import sys
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))


def lire(nom):
    return yaml.safe_load((REPO / "params" / nom).read_text(encoding="utf-8"))


def sources(x):
    if isinstance(x, dict):
        for k, v in x.items():
            if k == "source" and isinstance(v, str) and v.startswith("marche_"):
                yield v
            else:
                yield from sources(v)
    elif isinstance(x, list):
        for v in x:
            yield from sources(v)


class Complements(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reg = set(lire("fournisseurs.yaml")["fichiers"])
        cls.blocs = {"capteurs": lire("capteurs.yaml"), "temps_reel": lire("temps_reel.yaml"),
                     "chargeurs_12s": lire("puissance.yaml")["chargeurs_12s"],
                     "hailo_m2": lire("calculateurs.yaml")["hailo_m2"],
                     "releve_2026_10_09": lire("actionneurs.yaml")["marche"]["releve_2026_10_09"]}

    def test_sources_au_registre(self):
        for nom, b in self.blocs.items():
            ids = list(sources(b))
            self.assertTrue(ids, f"{nom} : aucune source citée")
            manque = [i for i in ids if i not in self.reg]
            self.assertEqual(manque, [], f"{nom} : sources absentes du registre")

    def test_defaut_vu(self):
        faux = {"produits": [{"sources": [{"source": "marche_capt_inexistante"}]}]}
        self.assertTrue([i for i in sources(faux) if i not in self.reg])

    def test_releve_hors_du_calcul(self):
        import explorateur as X
        par, _, _ = X.catalogue()
        ids = {a["id"] for v in par.values() for a in v}
        self.assertEqual(sum(len(v) for v in par.values()), 211)
        self.assertFalse(any("xm540" in i or "hej" in i for i in ids))


if __name__ == "__main__":
    unittest.main()
