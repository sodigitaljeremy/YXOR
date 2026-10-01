"""La tension d'une configuration de banc = la tension COMMUNE de ses modèles.

    .venv/bin/python -m unittest tests.test_tension_banc -v

Lot F, 2026-10-01. Depuis le lot E (429126e), le document du banc disait
« L'option à deux finalistes tourne à 12 V » pour EduLite 05 + RS05,
deux actionneurs 48 V : la fonction renvoyait la variable de boucle de
la DERNIÈRE configuration (Feetech, 12 V) au lieu de la tension de la
paire. Une tension de configuration se CALCULE depuis les plages publiées
de ses modèles ; elle n'est jamais une valeur par défaut ni une
déclaration. Ce test vérifie TOUTES les configurations du comparatif.
Vu échouer avant la correction (journal du 2026-10-01, lot F).
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import analyser_marche as AM  # noqa: E402
import selection_multicritere as S  # noqa: E402


@unittest.skipUnless(AM.SERIE.exists() and AM.DEFAULT_YML.exists(),
                     "marche P1 ou données amont absentes — régénérer avec "
                     "sim/upstream/enregistrer_marche.py")
class TensionDesConfigurations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = S.calculer(cartes=False)
        cls.opts, _, _, cls.fin = S.options_banc(cls.r)

    def test_chaque_configuration_a_la_tension_commune_de_ses_modeles(self):
        cat = self.r["cat"]
        for o in self.opts:
            plages = [S.plage_tension(cat["candidats"][m]) for m in set(o["ids"])]
            attendue = S.tension_commune(plages)
            self.assertIsNotNone(attendue, f"{o['id']} : aucune tension commune à ses modèles")
            self.assertEqual(o["tension"], attendue, f"{o['id']} : {o['tension']} V au lieu de {attendue} V")

    def test_la_paire_de_finalistes_annonce_sa_propre_tension(self):
        paire = next(o for o in self.opts if o["id"] == "deux_finalistes")
        self.assertEqual(self.fin[5], paire["tension"],
                         f"le document annoncerait {self.fin[5]} V pour une paire à {paire['tension']} V")


if __name__ == "__main__":
    unittest.main()
