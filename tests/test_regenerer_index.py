"""regenerer.py doit échouer quand un contrôle échoue.

    .venv/bin/python -m unittest tests.test_regenerer_index -v

Adapté le 2026-10-01 (refonte R2) : il visait `index_fiches`, archivé
avec les fiches (archive/scripts/index_fiches.py, archive/tests/). Il vise
désormais `controle_depot`, qui reste dans la régénération (règle 4,
registre 0030). L'invariant est le même : un contrôle en échec ne passe
pas la commande unique en vert (audit de la nuit du 2026-09-29, § 8 C3).

Construit le site pour de bon (`--site-seulement`, dans `site/`, ignoré).
Seul `controle_depot.main` est remplacé, par un échec simulé.
"""
import contextlib
import io
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import regenerer  # noqa: E402


class RegenererRespecteControleDepot(unittest.TestCase):
    def test_echec_d_un_controle_fait_echouer_la_regeneration(self):
        with mock.patch.object(regenerer.controle_depot, "main", return_value=1), \
                contextlib.redirect_stdout(io.StringIO()):
            rc = regenerer.main(["--site-seulement"])
        self.assertNotEqual(rc, 0, "controle_depot a échoué, regenerer a rendu 0")


if __name__ == "__main__":
    unittest.main()
