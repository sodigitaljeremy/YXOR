"""Le critère du § 4 du protocole de banc donne ses trois verdicts.

    .venv/bin/python -m unittest tests.test_critere_banc -v

Outillé le 2026-10-01, avant toute mesure. Des mesures FICTIVES, écrites
dans un fichier TEMPORAIRE (jamais dans params/mesures.yaml), remplacent le
continu au blocage publié du RS00 (3,6 N·m). Le plus faible des deux
exemplaires est retenu.
"""
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import choix_actionneurs as C  # noqa: E402

CIBLE = ["candidats.rs00.couple_continu_Nm.blocage"]


def fichier(*valeurs) -> Path:
    d = Path(tempfile.mkdtemp())
    mes = {f"fictive_{i}": {"grandeur": "continu au blocage, RS00 (FICTIF, test)", "valeur": v,
                            "unite": "N·m", "incertitude": 0.05, "type_incertitude": "resolution",
                            "n": 1, "actionneur": "rs00", "alimente": CIBLE}
           for i, v in enumerate(valeurs)}
    (d / "mesures.yaml").write_text(yaml.safe_dump({"mesures": mes}), encoding="utf-8")
    return d / "mesures.yaml"


class CritereBanc(unittest.TestCase):
    def test_sans_mesure_pas_de_verdict(self):
        self.assertIsNone(C.verdict_banc(fichier())["verdict"])

    def test_s_confirme(self):
        self.assertEqual(C.verdict_banc(fichier(3.4, 3.5))["verdict"], "S confirmé")

    def test_repli(self):
        # 2,5 N·m : milieu de la bande de repli (2,35-2,65) depuis le retrait des
        # servos ToddlerBot du haut du corps (fiche 0067, 2026-10-02) ; était 2,8.
        self.assertEqual(C.verdict_banc(fichier(2.5, 3.5))["verdict"], "repli à 0,55 m")

    def test_famille_rouverte(self):
        self.assertEqual(C.verdict_banc(fichier(2.0, 3.5))["verdict"], "famille rouverte")

    def test_le_plus_faible_est_retenu(self):
        r = C.verdict_banc(fichier(3.5, 2.0))
        self.assertEqual(r["retenu"], 2.0)
        self.assertEqual(r["verdict"], "famille rouverte")

    def test_le_depot_reel_n_a_pas_de_mesure(self):
        self.assertIsNone(C.verdict_banc()["verdict"])


if __name__ == "__main__":
    unittest.main()
