#!/usr/bin/env python3
"""Marches et relevé simulés, rendus SANS DIMENSION et combinables (phase 3b, fiche 0069).

    .venv/bin/python scripts/simulations_marche.py            # résumé
    .venv/bin/python scripts/simulations_marche.py --ecrire   # rapport, courbes, table de résultats

Créé le 2026-10-06. ÉTUDE, aucune décision. Lit les séries de exports/simulations/
(ignoré, régénérable) :
  · toddlerbot_marche_vx*.csv + .json   sim/upstream/enregistrer_marche.py (venv amont)
  · toddlerbot_releve.csv               sim/upstream/enregistrer_releve.py (venv amont)
  · t1_marche_vx*.csv / g1_marche_vx*.csv + .json   politiques ONNX de MuJoCo Playground
    (Apache-2.0) jouées sur CPU par un script de session, onnxruntime hors du dépôt.

SIMILITUDE DYNAMIQUE (nombre de Froude) : à Fr = v/√(g·H) égal, deux robots
semblables marchent de la même façon ; le temps se met à l'échelle en √(H/g), le
couple en M·g·H. D'où :
    couple sans dimension      τ* = τ / (M·g·H)
    vitesse angulaire          ω* = ω · √(H/g)
    puissance                  P* = P / (M·g·√(g·H))
Rendu à une taille H : τ = τ*·g·H · M, soit la forme a·M + b de la phase 3a
(a = τ*·g·H, b = 0), combinable par le maximum (exigences_physiques.combiner).

LIMITE ÉCRITE : la similitude suppose des robots géométriquement semblables, aux
masses réparties de même ; T1, G1 et ToddlerBot ne le sont pas exactement. Un
niveau de marche dont le Froude dépasse celui de toutes les marches
enregistrées n'est PAS couvert (dit, jamais extrapolé).
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
SIM = REPO / "exports" / "simulations"
DOC = REPO / "docs" / "simulations-marche-2026-10.md"
SVG = REPO / "docs" / "simulations-marche-2026-10.svg"
CSV_OUT = REPO / "exports" / "exigences" / "simulations.csv"
G = 9.80665                                   # non-cote: pesanteur normale (m/s²)
TYPES = ["hip_yaw", "hip_roll", "hip_pitch", "knee", "ankle_pitch", "ankle_roll"]
SEUIL = 0.98                                  # non-cote: même seuil que analyser_marche.SEUIL_ECRETAGE
COUL = {"ToddlerBot": "#2a78d6", "Booster T1": "#eb6834", "Unitree G1": "#1baf7a"}   # 3 premières teintes de la palette de référence


def type_de(nom: str):
    n = nom.lower()
    for t in TYPES:
        if t in n or t.replace("_", "_") in n:
            return t
    return None


def lire(chemin: Path, saute: int = 1):
    with chemin.open(encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    tete, data = rows[0], [[float(x) for x in r] for r in rows[1:]]
    taus = [(i, h[4:]) for i, h in enumerate(tete) if h.startswith("tau:")]
    vits = {h[4:]: i for i, h in enumerate(tete) if h.startswith("vit:")}
    return tete, data, taus, vits


def profil(chemin: Path, M: float, H: float, borne=None, sat_tb=None) -> dict:
    """Par type d'articulation (deux côtés réunis) : τ* efficace et pointe, ω* et P* pointe, saturation."""
    tete, data, taus, vits = lire(chemin)
    t = [r[0] for r in data]
    out = {}
    for i, nom in taus:
        ty = type_de(nom)
        if ty is None:
            continue
        tau = [r[i] for r in data]
        vit = [r[vits[nom]] for r in data]
        pw = [abs(a * b) for a, b in zip(tau, vit)]
        bmax = max(abs(borne[nom][0]), abs(borne[nom][1])) if borne is not None and nom in borne else 0.0
        if bmax > 0:                                      # une borne nulle = pas de borne dans le modèle
            sat = sum(1 for x in tau if abs(x) >= SEUIL * bmax) / len(tau)
        elif sat_tb is not None:
            sat = sat_tb.get(nom)
        else:
            sat = None
        o = out.setdefault(ty, dict(rms=[], pk=[], w=[], p=[], sat=[], serie=[]))
        o["rms"].append(math.sqrt(sum(x * x for x in tau) / len(tau)) / (M * G * H))
        o["pk"].append(max(abs(x) for x in tau) / (M * G * H))
        o["w"].append(max(abs(x) for x in vit) * math.sqrt(H / G))
        o["p"].append(max(pw) / (M * G * math.sqrt(G * H)))
        if sat is not None:
            o["sat"].append(sat)
        if nom.lower().startswith("left"):
            o["serie"] = [(tt * math.sqrt(G / H), x / (M * G * H)) for tt, x in zip(t, tau)]
    res = {}
    for ty, o in out.items():
        res[ty] = dict(rms=max(o["rms"]), pointe=max(o["pk"]), omega=max(o["w"]), puissance=max(o["p"]),
                       saturation=max(o["sat"]) if o["sat"] else None, serie=o["serie"])
    return res


def saturation_tb(chemin: Path) -> dict:
    """ToddlerBot : part du temps à ≥ 98 % de la borne couple-vitesse de ses servos (même règle que analyser_marche)."""
    import analyser_marche as AM
    M = AM.modeles_amont()
    tete, data, taus, vits = lire(chemin)
    out = {}
    for i, nom in taus:
        if nom not in M["moteur"]:
            continue
        p = M["bornes"][M["moteur"][nom][0]]
        n = 0
        for r in data:
            t, v = r[i], r[vits[nom]]
            lim = AM.limite_moteur(p, v) if t * v >= 0 else p["tau_brake_max"]
            n += abs(t) >= AM.SEUIL_ECRETAGE * lim
        out[nom] = n / len(data)
    return out


def charger():
    """Les marches retenues (vitesse la plus haute tenue) et le relevé ; ce qui manque est dit."""
    import analyser_marche as AM
    cat = yaml.safe_load((REPO / "params" / "actionneurs.yaml").read_text(encoding="utf-8"))
    H_TB = cat["reference_toddlerbot"]["hauteur_m"]["valeur"]
    marches, manque = {}, []
    for robot, motif in (("ToddlerBot", "toddlerbot_marche_vx*.json"), ("Booster T1", "t1_marche_vx*.json"),
                         ("Unitree G1", "g1_marche_vx*.json")):
        essais = []
        for j in sorted(SIM.glob(motif)):
            m = json.loads(j.read_text(encoding="utf-8"))
            m["csv"] = j.with_suffix(".csv")
            m.setdefault("H", H_TB)
            essais.append(m)
        if not essais:
            manque.append(f"{robot} : aucune série ({motif}) dans exports/simulations/")
            continue
        tenus = [e for e in essais if not e["chute"]]
        # la plus haute vitesse MESURÉE parmi les essais sans chute
        e = max(tenus, key=lambda e: e["v"])
        sat_tb = saturation_tb(e["csv"]) if robot == "ToddlerBot" else None
        e["profil"] = profil(e["csv"], e["M"], e["H"], borne=e.get("forcerange"), sat_tb=sat_tb)
        e["Fr"] = e["v"] / math.sqrt(G * e["H"])
        e["essais"] = [(x.get("vx_commande", x.get("vx")), x["v"], x["chute"]) for x in essais]
        marches[robot] = e
    releve = None
    f = SIM / "toddlerbot_releve.csv"
    if f.exists():
        M_TB = cat["reference_toddlerbot"]["masse_totale_kg"]["valeur"]
        releve = dict(M=M_TB, H=H_TB, profil=profil(f, M_TB, H_TB, sat_tb=saturation_tb(f)))
    else:
        manque.append("relevé ToddlerBot : exports/simulations/toddlerbot_releve.csv absent")
    return marches, releve, manque


def prudente(marches: dict) -> dict:
    """Référence prudente (0064) : par articulation, le PLUS EXIGEANT des robots, séparément pour l'efficace et la pointe."""
    ref = {}
    for ty in TYPES:
        cands = [(r, e["profil"][ty]) for r, e in marches.items() if ty in e["profil"]]
        if not cands:
            continue
        r_rms = max(cands, key=lambda c: c[1]["rms"])
        r_pk = max(cands, key=lambda c: c[1]["pointe"])
        ref[ty] = dict(rms=r_rms[1]["rms"], rms_de=r_rms[0], pointe=r_pk[1]["pointe"], pointe_de=r_pk[0])
    return ref


def lignes_combinables(marches, releve, cap) -> list[dict]:
    """Forme a·M + b (b = 0) par tâche, niveau, H, articulation : même table que la phase 3a."""
    from exigences_physiques import HS
    out = []
    frs = {r: e["Fr"] for r, e in marches.items()}
    for v in cap["taches"]["marche_sol_plat"]["niveaux"]:
        for H in HS:
            fr = v / math.sqrt(G * H)
            couvrants = [r for r, f in frs.items() if f >= fr - 1e-9]
            for ty in TYPES:
                vals = [marches[r]["profil"][ty]["pointe"] for r in couvrants if ty in marches[r]["profil"]]
                if vals:
                    out.append(dict(tache="marche_sol_plat", niveau=v, H=H, articulation=ty, a=max(vals) * G * H, b=0.0,
                                    aP=0.0, bP=0.0, omega=None,
                                    note=f"Fr {fr:.3f} ; pointe sans dimension, plus exigeant de {', '.join(couvrants)}"))
    if releve:
        for niv in cap["taches"]["releve"]["niveaux"]:
            for H in HS:
                for ty, p in releve["profil"].items():
                    out.append(dict(tache="releve_simule", niveau=niv, H=H, articulation=ty, a=p["pointe"] * G * H, b=0.0,
                                    aP=0.0, bP=0.0, omega=None,
                                    note="ToddlerBot get_up (départ sur le ventre), pointe sans dimension"))
    return out


def couverture(marches, cap):
    from exigences_physiques import HS
    fmax = max(e["Fr"] for e in marches.values()) if marches else 0
    out = {}
    for v in cap["taches"]["marche_sol_plat"]["niveaux"]:
        hs = [H for H in HS if v / math.sqrt(G * H) <= fmax + 1e-9]
        out[v] = (min(hs) if hs else None)
    return fmax, out


def svg(marches) -> str:
    PW, PH, ML, MT, GX, GY, ncol = 300, 150, 44, 34, 40, 50, 3      # non-cote: mise en page en px
    W = ML + ncol * PW + (ncol - 1) * GX + 16
    Ht = MT + 2 * (PH + GY) + 10
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Ht}" width="100%" role="img" '
         'aria-label="Couple sans dimension au cours de la marche, trois robots, par articulation">',
         "<style>:root{--s:#fcfcfb;--t1:#0b0b0b;--t2:#52514e;--g:#e4e3df}"
         "@media (prefers-color-scheme: dark){:root{--s:#1a1a19;--t1:#fff;--t2:#c3c2b7;--g:#33332f}}"
         "text{font:10px system-ui,sans-serif;fill:var(--t2)} .t{fill:var(--t1);font-weight:600;font-size:11px}"
         ".grid{stroke:var(--g)}</style>", f'<rect width="{W}" height="{Ht}" fill="var(--s)"/>',
         f'<text x="{ML}" y="16" class="t">τ/(M·g·H), jambe gauche, sur 20 unités de temps √(H/g) — '
         + " ; ".join(f'<tspan fill="{COUL[r]}">■</tspan> {r}' for r in marches) + "</text>"]
    for i, ty in enumerate(TYPES):
        cx, cy = ML + (i % ncol) * (PW + GX), MT + (i // ncol) * (PH + GY)
        series = {r: [p for p in e["profil"].get(ty, {}).get("serie", []) if p[0] - e["profil"][ty]["serie"][0][0] <= 20]
                  for r, e in marches.items() if ty in e["profil"]}
        ym = max((abs(y) for s in series.values() for _, y in s), default=0.01) * 1.1
        o.append(f'<text x="{cx}" y="{cy - 6}" class="t">{ty}</text>')
        for gy in (-ym / 1.1, 0, ym / 1.1):
            Y = cy + PH / 2 - gy / ym * PH / 2
            o.append(f'<line class="grid" x1="{cx}" y1="{Y:.1f}" x2="{cx + PW}" y2="{Y:.1f}"/>'
                     f'<text x="{cx - 3}" y="{Y + 3:.1f}" text-anchor="end">{gy:.3f}</text>')
        for r, s in series.items():
            if not s:
                continue
            t0 = s[0][0]
            pts = " ".join(f"{cx + (t - t0) / 20 * PW:.1f},{cy + PH / 2 - y / ym * PH / 2:.1f}" for t, y in s)
            o.append(f'<polyline fill="none" stroke="{COUL[r]}" stroke-width="1.5" points="{pts}"><title>{r} — {ty}</title></polyline>')
    o.append("</svg>")
    return "\n".join(o)


def rapport(marches, releve, manque, cap) -> str:
    ref = prudente(marches)
    f3 = lambda v: "—" if v is None else f"{v:.3f}"
    pc = lambda v: "—" if v is None else f"{100 * v:.0f} %"
    L = ["# Marches et relevé simulés, sans dimension (octobre 2026)", "",
         "**Engendré** par `.venv/bin/python scripts/simulations_marche.py --ecrire`. Ne pas éditer à la main. "
         "**Étude, aucune décision** (phase 3b de la stratégie de la fiche 0069). Aucun entraînement : des "
         "politiques pré-entraînées jouées sur CPU.", "",
         "## Marches enregistrées", "",
         "| Robot | Masse (kg) | H (m) | Essais (commande → mesurée, chute) | Retenue | Froude |", "| --- | ---: | ---: | --- | --- | ---: |"]
    for r, e in marches.items():
        es = " ; ".join(f"{c} → {v:.2f}{' CHUTE' if ch else ''}" for c, v, ch in e["essais"])
        L.append(f"| {r} | {e['M']:.2f} | {e['H']:.3f} | {es} | {e['v']:.2f} m/s | {e['Fr']:.3f} |")
    L += ["", "Masse : somme des corps du modèle MuJoCo. H : sommet du robot debout dans le modèle (T1, G1), 0,56 m "
          "pour ToddlerBot (référence de calcul). Chaque marche dure 15 s après une mise en route (3 s pour T1 et G1).", "",
          "## Comparaison par articulation (τ* = τ/(M·g·H))", "",
          "| Articulation | ToddlerBot efficace / pointe | T1 efficace / pointe | G1 efficace / pointe | Saturation TB / T1 / G1 | **Référence prudente** efficace / pointe |",
          "| --- | --- | --- | --- | --- | --- |"]
    for ty in TYPES:
        cell = lambda r: (f"{f3(marches[r]['profil'][ty]['rms'])} / {f3(marches[r]['profil'][ty]['pointe'])}"
                          if r in marches and ty in marches[r]["profil"] else "—")
        sat = " / ".join(pc(marches[r]["profil"][ty]["saturation"]) if r in marches and ty in marches[r]["profil"] else "—"
                         for r in ("ToddlerBot", "Booster T1", "Unitree G1"))
        rf = ref.get(ty)
        L.append(f"| {ty} | {cell('ToddlerBot')} | {cell('Booster T1')} | {cell('Unitree G1')} | {sat} | "
                 + (f"**{f3(rf['rms'])}** ({rf['rms_de']}) / **{f3(rf['pointe'])}** ({rf['pointe_de']})" if rf else "—") + " |")
    L += ["", "Saturation : part du temps où le couple atteint 98 % de sa borne. ToddlerBot : borne couple-vitesse de "
          "ses servos (`analyser_marche`) ; T1 et G1 : borne de couple fixe du modèle (`forcerange`). Les deux "
          "définitions diffèrent : à comparer avec prudence.", "",
          f"![Couple sans dimension, trois marches]({SVG.name})", "",
          "## Couverture des niveaux de marche (similitude de Froude)", ""]
    fmax, cv = couverture(marches, cap)
    L.append(f"Froude le plus haut enregistré : {fmax:.3f}. Un niveau de vitesse v n'est couvert qu'aux tailles où "
             "v/√(g·H) ne dépasse pas ce Froude :")
    L.append("")
    for v, hmin in cv.items():
        L.append(f"- {v:g} m/s : " + (f"couvert à partir de H = {hmin:.2f} m" if hmin else "**non couvert** sur 0,50–1,40 m"))
    L += ["", "## Relevé (ToddlerBot, politique get_up)", ""]
    if releve:
        L += ["Départ au sol, **sur le ventre** (axe avant du torse vers le bas dans la première image de la référence). "
              "Couples à la taille de ToddlerBot (3,45 kg, 0,56 m) et sans dimension :", "",
              "| Articulation | Pointe (N·m) | Efficace (N·m) | τ* pointe | Saturation |", "| --- | ---: | ---: | ---: | ---: |"]
        for ty, p in releve["profil"].items():
            k = releve["M"] * G * releve["H"]
            L.append(f"| {ty} | {p['pointe'] * k:.2f} | {p['rms'] * k:.2f} | {p['pointe']:.3f} | {pc(p['saturation'])} |")
    L += ["", "## Ce qui n'a pas tourné", ""] + ([f"- {m}" for m in manque] or ["- rien"])
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ecrire", action="store_true")
    a = ap.parse_args(argv)
    marches, releve, manque = charger()
    if not marches:
        print("  SAUTÉ : aucune série dans exports/simulations/ (exports/ n'est ni suivi ni copié dans l'image)")
        return 0
    cap = yaml.safe_load((REPO / "params" / "capacites.yaml").read_text(encoding="utf-8"))
    print(f"  {len(marches)} marches ({', '.join(marches)}), relevé : {'oui' if releve else 'non'}")
    if a.ecrire:
        DOC.write_text(rapport(marches, releve, manque, cap), encoding="utf-8")
        SVG.write_text(svg(marches), encoding="utf-8")
        lignes = lignes_combinables(marches, releve, cap)
        CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
        with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(lignes[0]))
            w.writeheader()
            w.writerows(lignes)
        print(f"  -> {DOC.relative_to(REPO)}, {SVG.relative_to(REPO)}, {CSV_OUT.relative_to(REPO)} ({len(lignes)} lignes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
