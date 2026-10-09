"""Marcher lentement (scripts/marche_lente.py) et règle de statut d'actionneur (scripts/lab_leger.py).

    .venv/bin/python -m unittest tests.test_marche_lente -v

Créé le 2026-10-09 (prompt « le blocage en vitesse disparaît-il en marchant lentement ? »).
"""
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import marche_lente as ML  # noqa: E402


class MarcheLente(unittest.TestCase):
    def test_vitesse_genou_baisse_avec_la_marche(self):
        # borne « la plus lente au-dessus » : 0,30 m/s → G1 (0,547 m/s) ; 0,15 et 0,10 m/s → ToddlerBot (0,196 m/s)
        w = {v: ML.besoins_marche(v, "plus_lente")["knee"]["w"] for v in (0.10, 0.15, 0.30)}
        self.assertLess(w[0.15], w[0.30])
        # 0,10 = 0,15 : la MÊME marche simulée sert de borne (aucune marche plus lente n'existe) ; pas une baisse ratée
        self.assertEqual(w[0.10], w[0.15])
        self.assertEqual(ML.besoins_marche(0.10, "plus_lente")["source"], ML.besoins_marche(0.15, "plus_lente")["source"])

    def test_regle_explorateur_reprend_les_marches_rapides(self):
        # à 0,15 m/s, la règle de l'explorateur garde le G1 : mêmes vitesses requises qu'à 0,30 m/s (le soupçon, vérifié)
        a, b = ML.besoins_marche(0.15, "explorateur"), ML.besoins_marche(0.30, "explorateur")
        for ax in ML.JAMBE:
            self.assertEqual(a[ax]["w"], b[ax]["w"])

    def test_aucune_donnee_aux_vitesses_etudiees(self):
        for v in ML.VITESSES:
            self.assertIsNone(ML.besoins_marche(v, "donnee"))       # null, statut INCONNU : pas d'interpolation
        self.assertEqual(ML.verdict_robot(ML.actionneurs()[0], None, 1.5, True), "INCONNU (aucune donnée)")

    def test_sts3250_avant_correction_inconnu(self):
        sts = next(a for a in ML.actionneurs(corrige=False) if a["id"] == "sts3250")
        self.assertIsNone(sts["w"])
        need = ML.besoins_marche(0.15, "plus_lente")["knee"]
        self.assertEqual(ML.verdict(sts, need, 1.5)["statut"], "INCONNU")         # jamais « tient »
        sts_c = next(a for a in ML.actionneurs() if a["id"] == "sts3250")
        self.assertIsNotNone(sts_c["w"])

    def test_regle_lab_leger(self):
        # dans un processus à part : lab_leger prolonge la grille des hauteurs à l'import (exigences_physiques.HS)
        import subprocess
        code = ("import sys; sys.path.insert(0, 'scripts'); import lab_leger as LL; "
                "r = dict(statut='INCONNU', non_couvertes=[], inconnues=['vitesse à vide de sts3250']); "
                "e = dict(r, inconnues=['prix de HPD Power Bleeding Module (regeneration)']); "
                "print(LL.tient(r), LL.tient(e))")
        out = subprocess.run([sys.executable, "-c", code], cwd=REPO, capture_output=True, text=True, check=True).stdout
        self.assertEqual(out.split(), ["False", "True"])


if __name__ == "__main__":
    unittest.main()
