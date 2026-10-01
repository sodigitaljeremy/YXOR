"""Un candidat ÉLIMINÉ ne peut pas gagner, quels que soient ses notes et les poids.

    .venv/bin/python -m unittest tests.test_selection -v

`scripts/selection_multicritere.py` : un éliminatoire qui échoue retire
le candidat du classement. Ce test donne à un candidat éliminé la note
maximale partout et vérifie qu'il ne gagne ni aux poids proposés, ni
dans aucune variation ±50 %, ni dans aucun des 1 000 tirages. Vu échouer
quand le filtre est neutralisé (journal du 2026-09-30).
"""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import analyser_marche as AM  # noqa: E402
import selection_multicritere as S  # noqa: E402


@unittest.skipUnless(AM.SERIE.exists() and AM.DEFAULT_YML.exists(),
                     "marche P1 ou données amont absentes — régénérer avec "
                     "sim/upstream/enregistrer_marche.py")
class UnElimineNeGagneJamais(unittest.TestCase):
    def test_elimine_avec_notes_parfaites_ne_gagne_pas(self):
        r = S.calculer()
        cands = copy.deepcopy(r["cands"])
        cible = next(c for c in cands if not c["reference"])
        cible["etat"] = "éliminé"
        cible["notes"] = {k: 5 for k in r["poids"]}
        sens = S.sensibilite(cands, r["poids"], r["crit"]["classe_S"]["sensibilite"])
        self.assertNotEqual(sens["nominal"], cible["id"], "l'éliminé gagne aux poids proposés")
        self.assertTrue(all(w != cible["id"] for *_, w in sens["variations"]),
                        "l'éliminé gagne une variation ±50 %")
        self.assertNotIn(cible["id"], sens["gagnes"], "l'éliminé gagne des tirages aléatoires")


if __name__ == "__main__":
    unittest.main()
