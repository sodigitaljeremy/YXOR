"""Le contrôle de cohérence du dimensionnement doit savoir ÉCHOUER.

    .venv/bin/python -m unittest tests.test_dimensionnement_coherence -v

`scripts/dimensionnement.py` refuse de produire un résultat s'il ne
retrouve pas les robots de référence (ToddlerBot, Zeroth-01) dans leur
classe. Un contrôle qui ne peut pas échouer ne contrôle rien : ce test
lui fournit deux références IMPOSSIBLES et exige qu'il les refuse, puis
vérifie qu'il accepte les vraies.

Lit la marche P1 régénérable (`exports/actionneurs/marche_15s.csv`) et
les données amont. Si elles manquent, le test est SAUTÉ et le dit.
"""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import analyser_marche as AM  # noqa: E402
import dimensionnement as D  # noqa: E402


@unittest.skipUnless(AM.SERIE.exists() and AM.DEFAULT_YML.exists(),
                     "marche P1 ou données amont absentes — régénérer avec "
                     "sim/upstream/enregistrer_marche.py")
class ControleDeCoherence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cat = D.charger_catalogue()
        cls.analyse = AM.analyser(AM.SERIE)
        cls.ref = D.reference(cls.cat, cls.analyse)

    def test_refuse_un_robot_trop_grand_pour_sa_classe(self):
        cat = copy.deepcopy(self.cat)
        cat["controle_coherence"]["zeroth01"]["hauteur_m"]["valeur"] = 3.0
        echecs = D.controle_coherence(cat, self.analyse, self.ref)
        self.assertTrue(any("zeroth01" in e for e in echecs),
                        f"un Zeroth-01 de 3 m en STS3250 est passé : {echecs}")

    def test_refuse_une_classe_trop_faible(self):
        cat = copy.deepcopy(self.cat)
        cat["candidats"]["sts3250"]["couple_pointe_Nm"]["valeur"] = 0.1
        echecs = D.controle_coherence(cat, self.analyse, self.ref)
        self.assertTrue(any("zeroth01" in e for e in echecs),
                        f"un STS3250 de 0,1 N·m a porté Zeroth-01 : {echecs}")

    def test_accepte_les_vraies_references(self):
        self.assertEqual(D.controle_coherence(self.cat, self.analyse, self.ref), [])


if __name__ == "__main__":
    unittest.main()
