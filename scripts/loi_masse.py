#!/usr/bin/env python3
"""Loi de masse allométrique (masse ∝ H^b) : ajustement sur les bipèdes, variantes, couple au genou.

    .venv/bin/python scripts/loi_masse.py            # ajustement et comparaison aux paramètres
    .venv/bin/python scripts/loi_masse.py --ecrire   # docs/loi-masse-2026-10.md

Créé le 2026-10-06. ÉTUDE, aucune décision ; la loi isométrique (∝ H³) reste celle
des calculs existants, l'allométrique s'y ajoute en VARIANTE (params/lois_masse.yaml).

Ajustement : log(masse) = log(A) + b·log(L), moindres carrés, intervalle de
confiance à 95 % sur b par la loi de Student à n − 2 degrés de liberté.
Données : exports/sources/robot_scaling_dataset.csv (robomechanics/robot-dataset,
sans licence déclarée : hors du dépôt, au registre). Absentes : l'ajustement SAUTE
et le dit.

Configuration de référence : YXOR Lab = le squelette actuel (masse du modèle de S,
v3, à H_S) ; le final = les mêmes proportions agrandies. Couple au genou : la
référence prudente de la phase 3b, τ = τ*·M·g·H (scripts/simulations_marche.py).
"""
from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
DONNEES = REPO / "exports" / "sources" / "robot_scaling_dataset.csv"
PARAMS = REPO / "params" / "lois_masse.yaml"
DOC = REPO / "docs" / "loi-masse-2026-10.md"
G = 9.80665                                    # non-cote: pesanteur normale (m/s²)
TAILLES = [0.6, 0.8, 1.0, 1.2]                 # non-cote: tailles du tableau demandé (m)
BIPEDES = ("full biped", "lower biped")


def nombre(x):
    s = str(x).replace(",", "").strip()
    try:
        return float(s)
    except ValueError:
        return None


def ajuster(chemin: Path = DONNEES, types=BIPEDES) -> dict | None:
    if not chemin.exists():
        return None
    import numpy as np
    from scipy import stats
    rows = list(csv.DictReader(chemin.open(encoding="utf-8-sig")))
    pts = [(nombre(r["total_length_inm"]), nombre(r["average_mass_inkg"])) for r in rows
           if r["type"].strip().lower() in types]
    pts = [(l, m) for l, m in pts if l and m]
    x, y = np.log([p[0] for p in pts]), np.log([p[1] for p in pts])
    r = stats.linregress(x, y)
    t = stats.t.ppf(0.975, len(pts) - 2)
    return dict(n=len(pts), b=r.slope, bas=r.slope - t * r.stderr, haut=r.slope + t * r.stderr,
                A=math.exp(r.intercept), R2=r.rvalue ** 2)


def reference():
    """(M0, H0) du squelette actuel, et τ* du genou (pointe, efficace) : None si les séries manquent."""
    import analyser_marche as AM
    if not AM.SERIE.exists():
        return None
    import squelette as SQ
    import simulations_marche as SM
    sq = SQ.construire()
    marches, _, _ = SM.charger()
    if not marches:
        return None
    ref = SM.prudente(marches)["knee"]
    return dict(M0=sq["masse_totale"], H0=sq["H"], pointe=ref["pointe"], pointe_de=ref["pointe_de"],
                rms=ref["rms"], rms_de=ref["rms_de"])


def table(p: dict, r: dict) -> list[dict]:
    va = p["variantes"]
    lois = [("isométrique (H³)", 3.0)] + [(f"allométrique b {k} ({v:.3f})", v)
                                          for k, v in va["allometrique"]["exposant"].items()]
    out = []
    for nom, b in lois:
        for H in TAILLES:
            M = r["M0"] * (H / r["H0"]) ** b
            out.append(dict(loi=nom, H=H, M=M, pointe=r["pointe"] * M * G * H, rms=r["rms"] * M * G * H))
    return out


def rapport(p, fit, r) -> str:
    va = p["variantes"]["allometrique"]
    L = ["# Loi de masse : isométrique (H³) et allométrique (H^b)", "",
         "**Engendré** par `.venv/bin/python scripts/loi_masse.py --ecrire`. Ne pas éditer à la main. "
         "**Étude, aucune décision** : la loi H³ reste celle des calculs existants ; l'allométrique est une "
         "VARIANTE (`params/lois_masse.yaml`, `dimensionnement.masse` avec `exposant`).", "",
         "## Ajustement sur les bipèdes", "",
         f"Jeu de données robomechanics/robot-dataset (commit 3699af27, sans licence déclarée : hors du dépôt, au "
         f"registre). {va['selection']}. Variable : {va['variable']}.", "",
         "| Sélection | n | b | IC 95 % | A (kg) | R² |", "| --- | ---: | ---: | --- | ---: | ---: |",
         f"| bipèdes | {va['n']} | **{va['exposant']['central']:.3f}** | [{va['exposant']['bas']:.3f} ; {va['exposant']['haut']:.3f}] "
         f"| {va['A_kg']:.2f} | {va['R2']:.3f} |"]
    h = va["sous_ensemble_humanoides_complets"]
    L += [f"| humanoïdes complets seuls | {h['n']} | {h['exposant']['central']:.3f} | [{h['exposant']['bas']:.3f} ; "
          f"{h['exposant']['haut']:.3f}] | — | {h['R2']:.3f} |", "",
          f"Comparaison : {va['comparaison_auteurs']}. Article : {va['article']}.", ""]
    L += ["L'intervalle EXCLUT 3 : sur les bipèdes recensés, la masse croît nettement moins vite que H³. Les "
          "humanoïdes complets seuls (n plus petit) ont un intervalle plus large, qui exclut encore 3 de justesse.", "",
          "## Masse et couple au genou selon la loi", ""]
    if r:
        L += [f"Référence : YXOR Lab = squelette actuel, {r['M0']:.2f} kg à {r['H0']:.2f} m (modèle de S, v3) ; le final "
              f"= mêmes proportions agrandies. Couple au genou : référence prudente de la phase 3b, pointe "
              f"τ* = {r['pointe']:.3f} ({r['pointe_de']}), efficace τ* = {r['rms']:.3f} ({r['rms_de']}), "
              "τ = τ*·M·g·H.", "",
              "| Loi | H (m) | Masse (kg) | Genou, pointe (N·m) | Genou, efficace (N·m) |", "| --- | ---: | ---: | ---: | ---: |"]
        for t in table(p, r):
            L.append(f"| {t['loi']} | {t['H']:.1f} | {t['M']:.1f} | {t['pointe']:.1f} | {t['rms']:.1f} |")
    else:
        L += ["SAUTÉ : séries de simulation ou de marche absentes (exports/ non suivi)."]
    L += ["", "## Réserve sur la loi de couple", "",
          "Oke et al. (arXiv:2603.22560, résumé LU le 2026-10-06) trouvent que le couple nécessaire pour marcher "
          "suit τ ∝ m·L. Ce résultat vient de **deux bipèdes de morphologie quasi passive**, reconstruits en "
          "simulation 3D et mis à l'échelle de 0,02 à 1,2 m. Un robot entièrement actionné comme YXOR, qui ne "
          "s'appuie pas sur sa dynamique naturelle, n'est pas garanti de suivre la même loi. L'actionnement par la "
          "seule hanche de ces marcheurs n'est PAS vérifié dans le résumé (article complet non lu). La phase 3b "
          "rend déjà ses couples en τ/(M·g·H), donc proportionnels à m·L ; c'est la même hypothèse, à confirmer "
          "sur YXOR lui-même."]
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ecrire", action="store_true")
    a = ap.parse_args(argv)
    p = yaml.safe_load(PARAMS.read_text(encoding="utf-8"))
    fit = ajuster()
    if fit is None:
        print("  ajustement SAUTÉ : exports/sources/robot_scaling_dataset.csv absent (hors du dépôt, au registre)")
    else:
        e = p["variantes"]["allometrique"]["exposant"]
        print(f"  bipèdes : n {fit['n']}, b {fit['b']:.3f} [{fit['bas']:.3f} ; {fit['haut']:.3f}], R² {fit['R2']:.3f} "
              f"(paramètres : {e['central']} [{e['bas']} ; {e['haut']}])")
    r = reference()
    if a.ecrire:
        DOC.write_text(rapport(p, fit, r), encoding="utf-8")
        print(f"  -> {DOC.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
