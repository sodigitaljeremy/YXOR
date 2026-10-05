#!/usr/bin/env python3
"""Cartographie du marché des actionneurs : rapport et graphique, CALCULÉS depuis params/.

    .venv/bin/python scripts/marche_actionneurs.py            # résumé
    .venv/bin/python scripts/marche_actionneurs.py --ecrire   # docs/marche-actionneurs-2026-10.md + .svg

Créé le 2026-10-05 (phase 1 de la stratégie de la fiche 0069 : cartographie,
aucune décision). Lit params/actionneurs.yaml :
  · `candidats`        les actionneurs déjà au catalogue (grille de S) ;
  · `marche`           les familles logicielles et les actionneurs ajoutés le
                       2026-10-05, au même format, HORS de `candidats` pour
                       qu'aucun calcul existant (k_bas, dimensionnement, grille
                       de S) ne change ;
  · `marche.complements` les champs ajoutés aux candidats existants.

Rien n'est estimé : une valeur absente est un TROU, compté et listé.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
CAT = REPO / "params" / "actionneurs.yaml"
DOC = REPO / "docs" / "marche-actionneurs-2026-10.md"
SVG = REPO / "docs" / "marche-actionneurs-2026-10.svg"
KGCM = 0.0980665                      # non-cote: kg·cm -> N·m (g = 9,80665 m/s²)


def val(x):
    return x.get("valeur") if isinstance(x, dict) else x


def nm(x):
    """Couple en N·m depuis une valeur du catalogue (unité d'origine conservée)."""
    if not isinstance(x, dict) or x.get("valeur") is None:
        return None
    v = x["valeur"]
    if isinstance(v, list):
        # tableau (couple selon la durée tenue, ou plusieurs tensions) : la plus
        # PETITE valeur, la plus prudente (fiche 0064)
        nums = [e if isinstance(e, (int, float)) else
                next((e[k] for k in ("couple_Nm", "Nm", "valeur") if isinstance(e, dict) and e.get(k) is not None), None)
                for e in v]
        nums = [n for n in nums if isinstance(n, (int, float))]
        if not nums:
            return None
        v = min(nums)
    if not isinstance(v, (int, float)):
        return None
    u = (x.get("unite") or "N·m").replace(" ", "").lower()
    return float(v) * KGCM if u in ("kg·cm", "kgf·cm", "kgcm", "kg.cm") else float(v)


def blocage(c):
    b = nm(c.get("couple_blocage_Nm"))
    if b is not None:
        return b
    for a in (c.get("couple_continu_Nm") or {}).get("autres_conditions") or []:
        if "BLOCAGE" in (a.get("condition") or "").upper():
            return a.get("valeur")
    return None


def charger():
    cat = yaml.safe_load(CAT.read_text(encoding="utf-8"))
    m = cat.get("marche") or {}
    fam = m.get("familles_logicielles") or {}
    comp = m.get("complements") or {}
    rows = []
    for src, d in (("catalogue", cat["candidats"]), ("marché", m.get("actionneurs") or {})):
        for cid, c in d.items():
            c = dict(c, **(comp.get(cid) or {}))
            f = c.get("famille_logicielle") or (m.get("rattachement") or {}).get(cid)
            rows.append(dict(id=cid, src=src, nom=c.get("nom", cid), famille=f,
                             pointe=nm(c.get("couple_pointe_Nm")), continu=nm(c.get("couple_continu_Nm")),
                             blocage=blocage(c), masse=val(c.get("masse_g")),
                             vitesse=val(c.get("vitesse_a_vide_rpm")), dims=val(c.get("dimensions_mm")),
                             fixation=val(c.get("fixation")), step=c.get("step_officiel"),
                             prix=c.get("prix_revendeur") or c.get("prix") or c.get("prix_constructeur"),
                             dispo=val(c.get("disponibilite_ch_ue")), garantie=val(c.get("garantie")),
                             tension=val(c.get("tension_V")), bus=c.get("bus")))
    return fam, rows


TROUS = (("pointe", "couple en pointe"), ("continu", "couple continu"), ("blocage", "couple au blocage"),
         ("masse", "masse"), ("dims", "cotes (Ø × L)"), ("fixation", "motifs de fixation"),
         ("step", "STEP officiel"), ("prix", "prix"), ("dispo", "disponibilité CH/UE"), ("garantie", "garantie"))


def trous(rows):
    return {lib: [r["id"] for r in rows if r[k] in (None, "", {})] for k, lib in TROUS}


# ─────────────────────────────── graphique ──────────────────────────────
# Petits multiples (un panneau par famille) : un nuage de points ne sépare
# pas plus de trois teintes (règle de la palette de référence) ; chaque
# panneau a UNE teinte, le reste du marché en gris pour le contexte.
# Échelles logarithmiques ; diagonales de couple massique (N·m/kg).
def svg(fam_ids, fam, rows):
    PW, PH, ML, MB, MT, GAP = 290, 230, 46, 36, 30, 34           # non-cote: mise en page en px
    ncol = 3
    W = ML + ncol * PW + (ncol - 1) * (GAP + 20) + 16                 # largeur CALCULÉE : 980 en dur coupait la 3e colonne
    nrow = math.ceil(len(fam_ids) / ncol)
    H = MT + nrow * (PH + MB + GAP) + 40
    xm, xM, ym, yM = 2, 8000, 0.02, 600                          # non-cote: bornes des axes (g, N·m)
    lx = lambda v: math.log10(v)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" '
         f'aria-label="Couple en pointe en fonction de la masse, un panneau par famille d\'actionneurs">',
         "<style>",
         ":root{--s:#fcfcfb;--t1:#0b0b0b;--t2:#52514e;--g:#e4e3df;--ctx:#c9c8c2;--a:#2a78d6;}",
         "@media (prefers-color-scheme: dark){:root{--s:#1a1a19;--t1:#ffffff;--t2:#c3c2b7;--g:#33332f;--ctx:#55544f;--a:#3987e5;}}",
         "text{font:11px system-ui,sans-serif;fill:var(--t2)} .t{fill:var(--t1);font-weight:600;font-size:12px}",
         ".grid{stroke:var(--g);stroke-width:1} .diag{stroke:var(--g);stroke-dasharray:3 3}",
         ".ctx{fill:var(--ctx)} .pt{fill:var(--a);stroke:var(--s);stroke-width:2}",
         ".bl{fill:var(--s);stroke:var(--a);stroke-width:2}",
         "</style>", f'<rect width="{W}" height="{H}" fill="var(--s)"/>',
         f'<text x="{ML}" y="18" class="t">Couple en pointe (N·m) selon la masse (g), échelles log — '
         f'diagonales : 10, 30, 100 N·m/kg ; cercle vide = couple au blocage (pointe non publiée)</text>']
    # couple tracé : la POINTE publiée ; à défaut le couple au BLOCAGE (cercle vide),
    # seul publié par plusieurs familles (servos, HighTorque, SteadyWin)
    pts = [dict(r, y=r["pointe"] or r["blocage"], plein=bool(r["pointe"])) for r in rows
           if (r["pointe"] or r["blocage"]) and r["masse"]]
    for i, fid in enumerate(fam_ids):
        cx, cy = ML + (i % ncol) * (PW + GAP + 20), MT + 10 + (i // ncol) * (PH + MB + GAP)
        X = lambda v: cx + (lx(v) - lx(xm)) / (lx(xM) - lx(xm)) * PW
        Y = lambda v: cy + PH - (lx(v) - lx(ym)) / (lx(yM) - lx(ym)) * PH
        court = (fam[fid]["nom"] if fid in fam else fid).split(" (")[0]
        n_f = sum(1 for r in pts if r["famille"] == fid)
        o.append(f'<text x="{cx}" y="{cy - 6}" class="t">{court} ({n_f})</text>')
        for gx in (10, 100, 1000):
            o.append(f'<line class="grid" x1="{X(gx):.1f}" y1="{cy}" x2="{X(gx):.1f}" y2="{cy + PH}"/>'
                     f'<text x="{X(gx):.1f}" y="{cy + PH + 14}" text-anchor="middle">{gx}</text>')
        for gy in (0.1, 1, 10, 100):
            o.append(f'<line class="grid" x1="{cx}" y1="{Y(gy):.1f}" x2="{cx + PW}" y2="{Y(gy):.1f}"/>'
                     f'<text x="{cx - 4}" y="{Y(gy) + 4:.1f}" text-anchor="end">{gy:g}</text>')
        # diagonales et points DÉCOUPÉS au cadre du panneau : aucun point ne déborde chez le voisin
        o.append(f'<clipPath id="c{i}"><rect x="{cx}" y="{cy}" width="{PW}" height="{PH}"/></clipPath>'
                 f'<g clip-path="url(#c{i})">')
        for k in (10, 30, 100):                               # N·m/kg : couple = k × masse(g)/1000
            m0, m1 = max(xm, ym * 1000 / k), min(xM, yM * 1000 / k)
            o.append(f'<line class="diag" x1="{X(m0):.1f}" y1="{Y(k * m0 / 1000):.1f}" '
                     f'x2="{X(m1):.1f}" y2="{Y(k * m1 / 1000):.1f}"/>')
        for r in pts:
            if r["famille"] != fid:
                o.append(f'<circle class="ctx" cx="{X(r["masse"]):.1f}" cy="{Y(r["y"]):.1f}" r="3"/>')
        for r in pts:
            if r["famille"] == fid:
                o.append(f'<circle class="{"pt" if r["plein"] else "bl"}" cx="{X(r["masse"]):.1f}" cy="{Y(r["y"]):.1f}" r="5">'
                         f'<title>{r["nom"]} : {r["y"]:g} N·m ({"pointe" if r["plein"] else "blocage"}), '
                         f'{r["masse"]:g} g</title></circle>')
        o.append("</g>")
    o.append("</svg>")
    return "\n".join(o)


def doc(fam, rows):
    fam_ids = [f for f in fam if any(r["famille"] == f for r in rows)]
    sans = [r["id"] for r in rows if r["famille"] not in fam]
    T = trous(rows)
    L = ["# Marché des actionneurs, octobre 2026", "",
         "**Engendré** par `.venv/bin/python scripts/marche_actionneurs.py --ecrire` depuis "
         "`params/actionneurs.yaml` (`candidats` et `marche`). Ne pas éditer à la main. "
         "Cartographie, **aucune décision** (phase 1 de la stratégie de la fiche 0069). Chaque valeur a sa "
         "source dans le catalogue ; une case vide est une valeur NON LUE, jamais une estimation.", "",
         f"{len(rows)} actionneurs : {sum(r['src'] == 'catalogue' for r in rows)} déjà au catalogue, "
         f"{sum(r['src'] == 'marché' for r in rows)} ajoutés le 2026-10-05 ; {len(fam_ids)} familles.", "",
         "## Familles (même bus, même protocole, même logiciel)", "",
         "Une famille est l'invariant de la fiche 0069 entre YXOR Lab et YXOR : on peut changer de modèle "
         "à l'intérieur d'une famille sans changer le bus, le protocole ni le logiciel.", "",
         "| Famille | Bus | Protocole | Logiciel | Actionneurs |", "| --- | --- | --- | --- | ---: |"]
    def court(v, n=110):
        v = " ".join(str(val(v) or "—").split()).replace("|", "/")
        return v if len(v) <= n else v[:n - 1] + "…"
    for f in fam_ids:
        x = fam[f]
        L.append(f"| **{x['nom'].split(' (')[0]}** | {court(x.get('bus'))} | {court(x.get('protocole'))} | "
                 f"{court(x.get('logiciel'))} | {sum(r['famille'] == f for r in rows)} |")
    L += ["", "Raisons sociales et sources complètes : `params/actionneurs.yaml`, `marche.familles_logicielles`."]
    if sans:
        L += ["", f"Sans famille rattachée : {', '.join(sans)}."]
    L += ["", "## Couple en pointe et masse", "",
          f"![Couple en pointe selon la masse, par famille]({SVG.name})", "",
          "Chaque panneau montre une famille en couleur et le reste du marché en gris. Les diagonales "
          "sont des couples massiques constants (10, 30 et 100 N·m/kg) : plus un point est haut à masse "
          "égale, plus l'actionneur est « fort pour son poids ». Un cercle VIDE est un couple au blocage, "
          "tracé faute de pointe publiée (servos, HighTorque, SteadyWin). Le couple en POINTE flatte : le couple "
          "continu et le couple au blocage, plus bas, sont dans le tableau.", "",
          "## Tous les actionneurs", "",
          "| Actionneur | Famille | Pointe (N·m) | Continu (N·m) | Blocage (N·m) | Masse (g) | N·m/kg (pointe) "
          "| Cotes | STEP | Prix | CH/UE |",
          "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- |"]
    f2 = lambda v: "—" if v is None else f"{v:.3g}"
    for r in sorted(rows, key=lambda r: (str(r["famille"]), r["pointe"] or 0)):
        pm = (r["pointe"] / r["masse"] * 1000) if r["pointe"] and r["masse"] else None
        pr = r["prix"]
        prs = f"{val(pr)} {pr.get('devise', '')}" if isinstance(pr, dict) and val(pr) is not None else "—"
        L.append(f"| {r['nom']} | {fam.get(r['famille'], {}).get('nom', r['famille'] or '—').split(' (')[0]} | {f2(r['pointe'])} | "
                 f"{f2(r['continu'])} | {f2(r['blocage'])} | {f2(r['masse'])} | {f2(pm)} | {r['dims'] or '—'} | "
                 f"{'oui' if r['step'] else '—'} | {prs} | {'oui' if r['dispo'] else '—'} |")
    L += ["", "## Ce qui manque", "",
          "Nombre d'actionneurs sans la donnée, sur " + str(len(rows)) + " :", "",
          "| Donnée | Manquante pour | Lesquels |", "| --- | ---: | --- |"]
    for lib, ids in T.items():
        L.append(f"| {lib} | {len(ids)} | {', '.join(ids) if len(ids) <= 12 else ', '.join(ids[:12]) + ', …'} |")
    return "\n".join(L) + "\n", svg(fam_ids, fam, rows)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ecrire", action="store_true")
    a = ap.parse_args(argv)
    fam, rows = charger()
    print(f"  {len(rows)} actionneurs ({sum(r['src'] == 'marché' for r in rows)} ajoutés au marché), "
          f"{len(fam)} familles logicielles")
    for lib, ids in trous(rows).items():
        print(f"    trou « {lib} » : {len(ids)}")
    if a.ecrire:
        md, s = doc(fam, rows)
        DOC.write_text(md, encoding="utf-8")
        SVG.write_text(s, encoding="utf-8")
        print(f"  -> {DOC.relative_to(REPO)}, {SVG.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
