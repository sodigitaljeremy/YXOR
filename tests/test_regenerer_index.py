"""regenerer.py doit échouer quand index_fiches échoue.

    .venv/bin/python -m unittest tests.test_regenerer_index -v

Audit de la nuit du 2026-09-29, § 8 C3 : le code de retour
d'`index_fiches.main()` était ignoré. Une fiche hors convention passait
la commande unique en vert. Vu échouer avant la correction (journal du
2026-09-30).

Construit le site pour de bon (`--site-seulement`, dans `site/`, ignoré).
Seul `index_fiches.main` est remplacé, par un échec simulé : l'index
réel n'est ni lu ni réécrit.
"""
import contextlib
import io
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import regenerer  # noqa: E402


class RegenererRespecteIndexFiches(unittest.TestCase):
    def test_echec_de_l_index_fait_echouer_la_regeneration(self):
        with mock.patch.object(regenerer.index_fiches, "main", return_value=1), \
                contextlib.redirect_stdout(io.StringIO()):
            rc = regenerer.main(["--site-seulement"])
        self.assertNotEqual(rc, 0, "index_fiches a échoué, regenerer a rendu 0")


if __name__ == "__main__":
    unittest.main()
