#!/usr/bin/env python3
"""Saut vertical selon la profondeur d'accroupi : course, couple et vitesse par articulation ; tient-il en RobStride ?

    .venv/bin/python scripts/saut.py            # tableau
    .venv/bin/python scripts/saut.py --ecrire   # docs/saut-accroupi-2026-10.md

Créé le 2026-10-08 (lot 4a septies, point 3). ÉTUDE : le profil ne change pas,
Jeremy décidera. Le modèle est celui de la phase 3a CORRIGÉE le 2026-10-08
(exigences_physiques.geometrie_saut) : accroupi au tibia incliné de alpha, hanche
à l'aplomb de la cheville ; course de poussée d = jambe tendue − accroupie ;
poussée à accélération constante (durée 2d/v) ; vitesse angulaire en rampe
linéaire (pointe = 2 × moyenne) ; force par jambe M·g·(1 + h/d) × répartition ;
bras de levier inchangés (genou : tibia·sin α ; hanche : |tibia·sin α − cuisse|,
majorant ; cheville : moitié du pied). L'inclinaison balayée (30, 40, 50, 60°)
est une HYPOTHÈSE PROPOSÉE.

TIENT-IL ? Pour chaque articulation, le RobStride le plus FORT dont la vitesse à vide,
ramenée à la tension de coupure DÉCIDÉE (12S, 3,0 V par cellule : fiches 0072 et
journal du 2026-10-08), couvre la vitesse de pointe ; la masse maximale du robot
est alors M_max = pointe ÷ (marge × couple par kg). Le saut tient si la masse du
robot est sous le plus petit M_max des trois articulations.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import exigences_physiques as EP  # noqa: E402

DOC = REPO / "docs" / "saut-accroupi-2026-10.md"
ALPHAS = (30, 40, 50, 60)          # non-cote: inclinaisons du tibia balayées (°), PROPOSÉES (prompt du 2026-10-08)
HAUTEURS = (5, 10)                 # non-cote: sauts du profil (cm)
TAILLES = (0.55, 0.60)             # non-cote: tailles du prompt (m)
ARTS = ("knee", "hip_pitch", "ankle_pitch")


def besoins_saut(H: float, h_cm: float, alpha_deg: float, R: dict, jambe: float) -> dict:
    """Course, durée, et par articulation : couple par kg de robot (N·m/kg) et vitesse de pointe (rad/s)."""
    a = math.radians(alpha_deg)
    L = {k: R[k] * H for k in ("cuisse", "tibia", "pied_longueur")}
    g = EP.geometrie_saut(L["cuisse"], L["tibia"], a)
    h = h_cm / 100
    v = math.sqrt(2 * EP.G * h)
    tp = 2 * g["d"] / v
    fpk = EP.G * (1 + h / g["d"]) * jambe
    lev = {"knee": L["tibia"] * math.sin(a), "hip_pitch": abs(L["tibia"] * math.sin(a) - L["cuisse"]),
           "ankle_pitch": EP.HYP["levier_cheville_frac"][0] * L["pied_longueur"]}
    dth = {"knee": g["knee"], "hip_pitch": g["hip_pitch"],
           "ankle_pitch": a + math.radians(EP.HYP["extension_cheville_deg"][0])}
    return dict(d=g["d"], tp=tp, v=v, art={k: dict(tau_kg=fpk * lev[k], w=2 * dth[k] / tp) for k in ARTS})


def robstride(S=12, coupure=3.0) -> list[dict]:
    """RobStride compatibles avec le pack, vitesse ramenée à la coupure (même règle que l'explorateur)."""
    import explorateur as X
    import systeme_electrique as SE
    par, _, _ = X.catalogue()
    var = SE.variante(S, coupure=coupure)
    out = []
    for a in par.get("robstride", []):
        f = SE.facteur_vitesse(a["v_ref"], var)
        if SE.compatibilite(a["plage"], var) and a["vitesse"] and f:
            out.append(dict(id=a["id"], pointe=a["pointe"], w=a["vitesse"] * f))
    return out


def tient(b: dict, rs: list[dict], marge: float) -> dict:
    """Par articulation : le RobStride le plus fort assez rapide, et la masse maximale du robot qu'il permet."""
    out = {}
    for k, x in b["art"].items():
        ok = [r for r in rs if r["w"] >= x["w"]]
        best = max(ok, key=lambda r: r["pointe"]) if ok else None
        out[k] = dict(rs=best and best["id"], M_max=best["pointe"] / (marge * x["tau_kg"]) if best else 0.0)
    out["M_max"] = min(v["M_max"] for v in out.values())
    return out


def tableau() -> list[dict]:
    cap, an, _ = EP.tout()
    R = {k: v["valeur"] for k, v in an["ratios"].items()}
    jambe = EP.lire("exigences_S.yaml")["releve"]["repartition_jambes"]["valeur"]
    marge = EP.lire("actionneurs.yaml")["dimensionnement"]["marge"]
    rs = robstride()
    lignes = []
    for H in TAILLES:
        for al in ALPHAS:
            for h in HAUTEURS:
                b = besoins_saut(H, h, al, R, jambe)
                lignes.append(dict(H=H, alpha=al, h=h, b=b, t=tient(b, rs, marge)))
    return lignes, rs, marge


def f1(x, n=1):
    return "—" if x is None else f"{x:,.{n}f}".replace(",", " ").replace(".", ",")


def rapport(lignes, rs, marge) -> str:
    L = ["# Saut vertical selon la profondeur d'accroupi (2026-10)", "",
         "**Engendré** par `.venv/bin/python scripts/saut.py --ecrire`. Ne pas éditer à la main. **Étude, aucune "
         "décision** : le profil du Lab ne change pas (saut 10 cm, décidé le 2026-10-07) ; Jeremy décidera.", "",
         "Modèle (phase 3a corrigée le 2026-10-08) : accroupi au tibia incliné de α, hanche à l'aplomb de la cheville ; "
         "course de poussée = jambe tendue − accroupie ; accélération constante ; vitesse angulaire en rampe linéaire "
         "(pointe = 2 × moyenne) ; force par jambe M·g·(1 + h/d) × répartition ; bras de levier : genou tibia·sin α, "
         "hanche |tibia·sin α − cuisse| (majorant), cheville moitié du pied. Inclinaisons balayées : PROPOSÉES.", "",
         f"RobStride en 12S coupé à 3,0 V par cellule (décidé), vitesse à vide × 36 / 48 : "
         + " ; ".join(f"{r['id']} {f1(r['pointe'], 0)} N·m, {f1(r['w'])} rad/s" for r in sorted(rs, key=lambda r: r['pointe']))
         + f". Marge {f1(marge)} sur le couple (fiche 0051). M_max : masse du robot au-delà de laquelle le RobStride le "
           "plus fort ASSEZ RAPIDE ne tient plus la pointe.", "",
         "| H (m) | Tibia (°) | Saut (cm) | Course (mm) | Poussée (ms) | Genou N·m/kg, rad/s | Hanche N·m/kg, rad/s | "
         "Cheville N·m/kg, rad/s | M_max (kg) et limite |",
         "| ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- |"]
    for x in lignes:
        b, t = x["b"], x["t"]
        a = b["art"]
        lim = min(("knee", "hip_pitch", "ankle_pitch"), key=lambda k: t[k]["M_max"])
        L.append(f"| {f1(x['H'], 2)} | {x['alpha']} | {x['h']} | {f1(b['d'] * 1000, 0)} | {f1(b['tp'] * 1000, 0)} | "
                 + " | ".join(f"{f1(a[k]['tau_kg'], 3)}, {f1(a[k]['w'])} ({t[k]['rs'] or 'aucun assez rapide'})"
                              for k in ARTS)
                 + f" | **{f1(t['M_max'])}** ({lim}) |")
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ecrire", action="store_true")
    a = ap.parse_args(argv)
    lignes, rs, marge = tableau()
    print(rapport(lignes, rs, marge))
    if a.ecrire:
        DOC.write_text(rapport(lignes, rs, marge), encoding="utf-8")
        print(f"  -> {DOC.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
