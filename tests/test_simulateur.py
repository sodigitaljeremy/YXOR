"""Le simulateur du navigateur calcule comme le Python, à 0,55, 0,60 et 0,90 m.

    .venv/bin/python -m unittest tests.test_simulateur -v

Créé le 2026-10-01. `web/simulateur.js` est une SECONDE implémentation de
`scripts/profil.py` (qui fait foi). La page ne se contrôle qu'à la hauteur
du dépôt ; ce test, à trois hauteurs : le repli de S (0,55 m), S (0,60 m)
et L (0,90 m).

Le JavaScript s'exécute sous Node, sans navigateur ni dépendance npm. Le
fichier est lu tel quel ; une ligne est injectée EN MÉMOIRE avant la
fermeture de son IIFE pour exposer `cotes` et `contour`. Les paramètres
autres que H sont ceux que la page embarque (relevé de la pièce).

Sans Node, le test se SAUTE et le dit (CLAUDE.md, « Les contrôles »).
"""
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import profil  # noqa: E402

SIMULATEUR = REPO / "web" / "simulateur.js"
RELEVE = REPO / "parts" / "semelle_apprentissage.origines.yaml"
HAUTEURS = (0.55, 0.60, 0.90)
# Cas où la LIMITE DE MACHINE l'emporte (2026-10-01, 21 h) : alu 3 mm chez
# l'opérateur CN, 0,5 x 3 = 1,5 mais machine 2,0. Valeurs du réglage
# operateur_cn_alu_3 (params/hardware.yaml), lues ci-dessous.
CAS_MACHINE = ("operateur_cn_alu_3", 0.60)
TOL_COTE, TOL_CONTOUR = 0.01, 0.05      # mm
NODE = shutil.which("node")

HARNAIS = r"""
const fs = require("fs"), vm = require("vm");
const ent = JSON.parse(fs.readFileSync(0, "utf8"));
let src = fs.readFileSync(ent.chemin, "utf8");
const fin = src.lastIndexOf("})();");
if (fin < 0) throw new Error("fermeture de l'IIFE introuvable");
src = src.slice(0, fin) + "window.__cotes = cotes; window.__contour = contour;\n" + src.slice(fin);
const ctx = { window: {}, Math };
vm.createContext(ctx); vm.runInContext(src, ctx);
const d = ctx.window.__cotes(ent.params);
process.stdout.write(JSON.stringify({ cotes: d, contour: ctx.window.__contour(d, ent.n_arc) }));
"""


def parametres() -> tuple[dict, int]:
    """Paramètres de la page ET données fixes (`fixes`), comme la page les passe."""
    sim = yaml.safe_load(RELEVE.read_text(encoding="utf-8"))["simulation"]
    p = {p["nom"]: p["valeur"] for p in sim["parametres"]}
    p.update(sim.get("fixes") or {})
    return p, sim["reference"]["n_arc"]


def cas() -> list[tuple[str, dict]]:
    """(nom, paramètres) : les trois hauteurs, puis le cas de la limite de machine."""
    import procedes
    p0, _ = parametres()
    out = [(f"H = {H} m", dict(p0, H=H)) for H in HAUTEURS]
    rid, H = CAS_MACHINE
    r = procedes.reglages()[rid]
    out.append((f"{rid}, H = {H} m", dict(p0, H=H, ep=r["epaisseur"],
                                         r_int_machine=r["rayon_interieur_min_machine"])))
    return out


def comparer(chemin_js: Path = SIMULATEUR) -> dict:
    """{cas: (pire écart de cote, pire écart de contour, r_int JS, r_int Python)}."""
    _, n_arc = parametres()
    out = {}
    for nom, p in cas():
        H = p["H"]
        res = subprocess.run([NODE, "-e", HARNAIS], capture_output=True, text=True, check=True,
                             input=json.dumps({"chemin": str(chemin_js), "params": p, "n_arc": n_arc}))
        js = json.loads(res.stdout)
        py = profil.cotes(H, p["r_pied_long"], p["r_pied_larg"], p["resserrement"],
                          p["coins"], p["etendue"], p["ep"], p.get("r_int_machine"))
        kpy = profil.contour(py, n_arc=n_arc)
        e_cote = max(abs(js["cotes"][k] - py[k]) for k in py)
        if js["contour"] is None or len(js["contour"]) != len(kpy):
            e_contour = float("inf")
        else:
            e_contour = max(max(abs(a[0] - b[0]), abs(a[1] - b[1])) for a, b in zip(js["contour"], kpy))
        out[nom] = (e_cote, e_contour, js["cotes"]["r_int"], py["r_int"])
    return out


@unittest.skipUnless(NODE, "Node absent : le JavaScript du site n'est pas testé (voir .nvmrc)")
class SimulateurContrePython(unittest.TestCase):
    def test_trois_hauteurs_et_limite_de_machine(self):
        res = comparer()
        for nom, (e_cote, e_contour, _, _) in res.items():
            with self.subTest(cas=nom):
                self.assertLessEqual(e_cote, TOL_COTE, f"cote, {nom}")
                self.assertLessEqual(e_contour, TOL_CONTOUR, f"contour, {nom}")
        # la limite de machine l'emporte bien, des deux côtés
        _, _, r_js, r_py = res[f"{CAS_MACHINE[0]}, H = {CAS_MACHINE[1]} m"]
        self.assertEqual((r_js, r_py), (2.0, 2.0))


if __name__ == "__main__":
    unittest.main()
