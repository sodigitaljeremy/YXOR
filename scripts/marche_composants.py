#!/usr/bin/env python3
"""Marché des batteries, des calculateurs et des cartes de bus : valeurs dérivées, tension, canaux CAN, rapports.

    .venv/bin/python scripts/marche_composants.py            # résumé (tension, canaux CAN, pertinents)
    .venv/bin/python scripts/marche_composants.py --ecrire   # docs/marche-{batteries,calculateurs,bus}-2026-10.md + .svg

Créé le 2026-10-07. DONNÉES SEULEMENT : aucune intégration à l'explorateur, aucun
achat (fiche 0066). Contexte DÉCIDÉ (fiche 0070, Jeremy, 2026-10-07) : les deux
robots fonctionnent entièrement sur batterie ; le calculateur n'est pas décidé
(préférence de Jeremy pour NVIDIA Jetson, comparaison chiffrée demandée).

Lit params/batteries.yaml, params/calculateurs.yaml et params/bus.yaml (bloc
`marche`, même méthode que le marché des actionneurs : une valeur non lue est
null, et un TROU, compté). Tout ce qui se calcule se CALCULE ici, jamais ne se
déclare : énergie (V × Ah) quand elle n'est pas publiée, volume depuis les cotes,
densités, prix en CHF HT (taux BCE de params/budget.yaml), TOPS par watt et par
franc, nombre de cellules en série admissible, canaux CAN.
"""
from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
DOCS = {k: REPO / "docs" / f"marche-{k}-2026-10.md" for k in ("batteries", "calculateurs", "bus")}
SVGS = {k: REPO / "docs" / f"marche-{k}-2026-10.svg" for k in ("batteries", "calculateurs")}


def lire(nom):
    return yaml.safe_load((REPO / "params" / nom).read_text(encoding="utf-8"))


def v(p: dict, champ: str):
    """La valeur d'un champ {valeur: …} ; None si absente ou non lue."""
    x = p.get(champ)
    if isinstance(x, dict):
        x = x.get("valeur")
    return x


def num(x):
    if isinstance(x, bool) or x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    m = re.match(r"^\s*(-?\d+(?:[.,]\d+)?)", str(x))
    return float(m.group(1).replace(",", ".")) if m else None


def chf(prix, taux):
    """Prix en CHF HT (exigences_physiques.prix_chf : TVA retirée si son taux est connu, sinon TTC, prudent)."""
    import dimensionnement as D
    import exigences_physiques as EP
    if not isinstance(prix, dict) or num(prix.get("valeur")) is None:
        return None
    q = dict(prix, valeur=num(prix["valeur"]))
    if q.get("devise") not in (None, "CHF") and q["devise"] not in taux["par_eur"] and q["devise"] != "EUR":
        return None                                            # devise sans taux BCE au budget : non convertie, dit
    return EP.prix_chf(q, taux, D)


def volume_l(dims) -> float | None:
    """Volume (L) depuis {diametre, hauteur}, {longueur, largeur, hauteur}, « Ø21 × 70 » ou « 138 × 47 × 50 »."""
    if isinstance(dims, dict):
        d, h = num(dims.get("diametre")), num(dims.get("hauteur"))
        if d and h:
            return math.pi * (d / 2) ** 2 * h / 1e6
        L_, l_ = num(dims.get("longueur")), num(dims.get("largeur"))
        if L_ and l_ and h:
            return L_ * l_ * h / 1e6
        dims = dims.get("valeur")
    if not dims:
        return None
    s = str(dims).replace(",", ".")
    n = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", s.split(";")[0])]
    if "Ø" in s and len(n) >= 2:
        return math.pi * (n[0] / 2) ** 2 * n[1] / 1e6
    if len(n) >= 3:
        return n[0] * n[1] * n[2] / 1e6
    return None


# ─────────────────────────────── batteries ──────────────────────────────
def batteries(bat=None, taux=None) -> list[dict]:
    bat = bat or lire("batteries.yaml")
    taux = taux or lire("budget.yaml")["taux_de_change"]
    out = []
    for pid, p in (bat["marche"].get("produits") or {}).items():
        V, Ah = num(v(p, "tension_nominale_V")), num(v(p, "capacite_Ah"))
        E_pub = num(v(p, "energie_Wh"))
        E = E_pub if E_pub is not None else (V * Ah if V and Ah else None)
        m = num(v(p, "masse_g"))
        vol = volume_l(p.get("dimensions_mm"))
        out.append(dict(id=pid, nom=p.get("nom", pid), famille=p.get("famille"), chimie=v(p, "chimie"),
                        V=V, Vmax=num(v(p, "tension_max_V")), Ah=Ah, E=E, E_calculee=E_pub is None and E is not None,
                        I=num(v(p, "courant_continu_A")), Ipk=num(v(p, "courant_pointe_A")),
                        m=m / 1000 if m else None, vol=vol,
                        Wh_kg=E / (m / 1000) if E and m else None, Wh_L=E / vol if E and vol else None,
                        prix=chf(p.get("prix"), taux), dispo=v(p, "disponibilite_ch_ue"),
                        bms=v(p, "bms"), un383=v(p, "certifications"), p=p))
    return out


def chimie(bat, nom) -> dict:
    c = (bat.get("chimies") or {}).get(nom) or {}
    return {k: num(v(c, k)) for k in ("tension_nominale_V", "tension_max_V", "tension_min_V")}


def plages(famille: str) -> list[dict]:
    """Plage de tension de fonctionnement publiée, produit par produit (None si non relevée).

    RobStride : params/actionneurs.yaml (`tension_plage_V`, sinon la note « plage a–b V » de `tension_V` ; en
    cas de désaccord, la plus prudente retenue par le catalogue, fiche 0064). Feetech : params/bus.yaml
    (`tensions_feetech`, fiches lues le 2026-10-07)."""
    if famille == "feetech":
        return [dict(id=k, min=num(x.get("min_V")), max=num(x.get("max_V")), source=x.get("source"))
                for k, x in (lire("bus.yaml").get("tensions_feetech") or {}).items()]
    cat = lire("actionneurs.yaml")
    m = cat["marche"]
    comp = m.get("complements") or {}
    out = []
    for src in (cat["candidats"], m.get("actionneurs") or {}):
        for cid, c in src.items():
            c = dict(c, **(comp.get(cid) or {}))
            if (c.get("famille_logicielle") or (m.get("rattachement") or {}).get(cid)) != famille:
                continue
            tp = c.get("tension_plage_V") or {}
            pl = [tuple(num(x) for x in tp["valeur"])] if isinstance(tp.get("valeur"), list) and len(tp["valeur"]) == 2 else []
            # la note de `tension_V` peut citer une autre plage (README) : on réunit tout, la plus ÉTROITE gagne (0064)
            pl += [(num(a), num(b)) for a, b in re.findall(r"(\d+(?:[.,]\d+)?)\s*[–-]\s*(\d+(?:[.,]\d+)?)\s*V",
                                                           str((c.get("tension_V") or {}).get("note") or ""))]
            lo, hi = (max(x for x, _ in pl), min(y for _, y in pl)) if pl else (None, None)
            out.append(dict(id=cid, min=lo, max=hi, source=(tp.get("source") or (c.get("tension_V") or {}).get("source"))))
    return out


def groupes(pl: list[dict]) -> dict:
    """{(min, max): [ids]} ; les produits sans plage relevée sous la clé None."""
    g = {}
    for x in pl:
        g.setdefault((x["min"], x["max"]) if x["min"] is not None and x["max"] is not None else None, []).append(x["id"])
    return g


def tableau_tension(bat, plages_rs: dict, seuil=60.0, s_range=range(6, 17)) -> list[dict]:
    """Par chimie et par nombre de cellules en série S : tensions du pack (min, nominale, max) ; compatible avec chaque
    plage d'actionneurs (Vmin pack ≥ min et Vmax pack ≤ max) ; marge sous le seuil de 60 V."""
    out = []
    for ch in ("li_ion", "lifepo4"):
        c = chimie(bat, ch)
        if None in c.values():
            out.append(dict(chimie=ch, S=None, manque=[k for k, x in c.items() if x is None]))
            continue
        for S in s_range:
            lo, no, hi = S * c["tension_min_V"], S * c["tension_nominale_V"], S * c["tension_max_V"]
            ok = {k: lo >= k[0] and hi <= k[1] for k in plages_rs if k}
            out.append(dict(chimie=ch, S=S, Vmin=lo, Vnom=no, Vmax=hi, ok=ok, marge_seuil=seuil - hi,
                            regen_ok=hi <= seuil - CRITERES["marge_regeneration_V"]))
    return out


# ─────────────────────────────── calculateurs ───────────────────────────
def calculateurs(cal=None, taux=None) -> list[dict]:
    cal = cal or lire("calculateurs.yaml")
    taux = taux or lire("budget.yaml")["taux_de_change"]
    out = []
    for pid, p in (cal["marche"].get("produits") or {}).items():
        t = p.get("tops") or {}
        pw = p.get("puissance_W") or {}
        tops, pmax = num(t.get("valeur")), num(v(pw, "max")) if isinstance(pw, dict) else None
        dense = (t.get("dense_ou_sparse") or "inconnu")
        prix = chf(p.get("prix"), taux)
        can = p.get("can_integre") or {}
        out.append(dict(id=pid, nom=p.get("nom", pid), famille=p.get("famille"), tops=tops,
                        precision=t.get("precision"), dense=dense, pmax=pmax, prepos=num(v(pw, "repos")),
                        ptyp=num(v(pw, "typique")), masse=num(v(p, "masse_g")), prix=prix,
                        can=can.get("valeur"), can_n=can.get("canaux"),
                        tops_w=tops / pmax if tops and pmax else None, tops_chf=tops / prix if tops and prix else None,
                        comparable=dense == "dense" and "INT8" in str(t.get("precision") or "").upper(), p=p))
    return out


# ─────────────────────────────── bus ────────────────────────────────────
def bits_trame(tr: dict, etendue=True, octets=8, ifs="prudente") -> dict | None:
    """Bits d'une trame de données CAN 2.0 au PIRE bourrage, depuis les longueurs de champ LUES (bus.yaml, trame_can :
    spécification Bosch CAN 2.0 de 1991, contre-lue par TI SLOA101B).

    Bourrage (Bosch p. 60) : après 5 bits égaux, un bit complémentaire, du SOF à la fin de la séquence CRC. Le bit
    inséré ouvre la suite suivante : au pire, un bit de bourrage au 5e bit puis tous les 4 bits, soit
    ⌊(n − 1) / 4⌋ bits pour n bits bourrables. Le maximum n'est pas publié : il se CALCULE.
    Intertrame : Bosch 3 bits, TI 7 bits ; « prudente » = la plus longue (fiche 0064)."""
    g = lambda k: num(v(tr, k))
    champs = dict(sof=g("sof_bits"), id=g("identifiant_etendu_bits") if etendue else g("identifiant_standard_bits"),
                  srr_ide=(g("srr_bits_etendue") + g("ide_bits")) if etendue else 0.0, rtr=g("rtr_bits"),
                  controle=g("champ_controle_bits"), crc=g("crc_sequence_bits"))
    fixe = dict(crc_delim=g("crc_delimiteur_bits"), ack=g("ack_bits"), eof=g("eof_bits"),
                ifs=max(g("intertrame_intermission_bits"), g("intertrame_ti_bits")) if ifs == "prudente"
                else g("intertrame_intermission_bits"))
    if None in champs.values() or None in fixe.values():
        return None
    bourrable = sum(champs.values()) + 8 * octets
    stuff = math.floor((bourrable - 1) / 4)
    return dict(bourrable=bourrable, stuff=stuff, fixe=sum(fixe.values()), ifs=fixe["ifs"],
                total=bourrable + stuff + sum(fixe.values()))


def canaux_can(n_axes, f_hz, trames_par_axe, bits, debit, charge_max) -> dict:
    besoin = n_axes * f_hz * trames_par_axe * bits                # bit/s
    return dict(besoin=besoin, par_canal=debit * charge_max, canaux=math.ceil(besoin / (debit * charge_max)))


def bus(b=None, taux=None) -> list[dict]:
    b = b or lire("bus.yaml")
    taux = taux or lire("budget.yaml")["taux_de_change"]
    return [dict(id=pid, nom=p.get("nom", pid), famille=p.get("famille"), canaux=v(p, "canaux"), fd=v(p, "can_fd"),
                 debit=v(p, "debit"), hote=v(p, "interface_hote"), linux=v(p, "pilote_linux"), masse=num(v(p, "masse_g")),
                 cotes=v(p, "dimensions_mm"), prix=chf(p.get("prix"), taux), p=p)
            for pid, p in (b["marche"].get("produits") or {}).items()]


# ─────────────────────────────── pertinence (PROPOSÉE) ──────────────────
# Critères PROPOSÉS par Claude le 2026-10-07, à confirmer par Jeremy : ils ne décident rien, ils trient.
CRITERES = dict(
    robots_kg=(10.0, 35.0),
    part_batterie=0.15,          # non-cote: PROPOSÉ, budget de masse de la batterie = 15 % de la masse du robot
    marge_regeneration_V=5.0,    # non-cote: PROPOSÉ, pleine charge ≤ 60 V − 5 V : le freinage fait monter le bus
    p_max_W={10.0: 25.0, 35.0: 75.0},   # non-cote: PROPOSÉ, plafond de puissance du calculateur
)


def s_cellule(p, bat) -> tuple[str, int | None]:
    """Chimie de référence et nombre de cellules en série d'un produit (1 pour une cellule ; V / V_nom sinon)."""
    ch = str(v(p, "chimie") or "").lower()
    ref = "lifepo4" if ("lifepo4" in ch or "lfp" in ch) else "li_ion"
    vn = chimie(bat, ref)["tension_nominale_V"]
    V = num(v(p, "tension_nominale_V"))
    if str(p.get("famille", "")).startswith("cellule"):
        return ref, 1
    return ref, (round(V / vn) if V and vn else None)


def serie_max(p) -> int | None:
    """Limite de mise en série publiée (notes lues), ou None."""
    txt = " ".join(str((x or {}).get("note") or "") for x in p.values() if isinstance(x, dict)).lower()
    if "série interdite" in txt:
        return 1
    m = re.search(r"max\.?\s*(\d+)\s*batteries en série", txt)
    return int(m.group(1)) if m else None


def composer(b: dict, bat: dict, budget_kg: float, vmin: float, vhaut: float) -> dict | None:
    """La meilleure batterie faite de ce produit : n en série (dans [vmin, vhaut]) × m en parallèle (dans le budget)."""
    ref, S = s_cellule(b["p"], bat)
    c = chimie(bat, ref)
    if not S or not b["m"] or not b["E"] or None in c.values():
        return None
    n_ok = [n for n in range(1, 40) if n * S * c["tension_min_V"] >= vmin and n * S * c["tension_max_V"] <= vhaut]
    lim = serie_max(b["p"])
    n_ok = [n for n in n_ok if lim is None or n <= lim]
    if not n_ok:
        return None
    n = max(n_ok)
    m = math.floor(budget_kg / (n * b["m"]) + 1e-9)
    if m < 1:
        return None
    k = n * m
    return dict(n=n, m=m, S=n * S, unites=k, E=k * b["E"], masse=k * b["m"], Vmax=n * S * c["tension_max_V"],
                I=(m * b["I"]) if b["I"] else None, prix=(k * b["prix"]) if b["prix"] else None, ref=ref)


def pertinentes_batteries(bs, bat, Mr, vmin, n=10):
    budget = CRITERES["part_batterie"] * Mr
    vhaut = 60.0 - CRITERES["marge_regeneration_V"]
    out = []
    for b in bs:
        c = composer(b, bat, budget, vmin, vhaut)
        if c:
            out.append(dict(b, comp=c))
    out.sort(key=lambda x: (-x["comp"]["E"], x["comp"]["prix"] or 1e12))
    return out[:n], budget, vhaut


def combinaisons_rpi(cs):
    """Raspberry Pi 5 (8 GB) + chaque carte d'IA : puissances et prix ADDITIONNÉS (aucune valeur estimée)."""
    rpi = [c for c in cs if c["famille"] == "rpi" and "8" in c["nom"] and "5" in c["nom"]]
    out = []
    for r in rpi[:1]:
        for a in (c for c in cs if c["famille"] == "rpi_ia"):
            pm = (r["pmax"] + a["pmax"]) if r["pmax"] and a["pmax"] else None
            pr = (r["prix"] + a["prix"]) if r["prix"] and a["prix"] else None
            out.append(dict(a, id=f"{r['id']}+{a['id']}", nom=f"{r['nom']} + {a['nom']}", famille="rpi+ia", pmax=pm,
                            prix=pr, can=r["can"], tops_w=a["tops"] / pm if a["tops"] and pm else None,
                            tops_chf=a["tops"] / pr if a["tops"] and pr else None))
    return out


def dense(c):
    """TOPS INT8 dense comparables : la valeur GPU dense publiée, ou le chiffre affiché s'il est INT8 dense."""
    d = num(v(c["p"], "tops_gpu_int8_dense"))
    return d if d is not None else (c["tops"] if c["comparable"] else None)


def pertinents_calculateurs(cs, Mr, n=8):
    cap = CRITERES["p_max_W"][Mr]
    cand = [c for c in cs + combinaisons_rpi(cs) if c["famille"] in ("jetson_module", "jetson_kit", "rpi+ia")
            and (c["pmax"] is None or c["pmax"] <= cap) and "annonc" not in str(c["p"].get("statut") or "")
            and "FIN DE PRODUCTION" not in str(v(c["p"], "statut") or "")]
    # d'abord ce qui est comparable (INT8 dense) ; puis le chiffre affiché ; une puissance non publiée est DITE
    cand.sort(key=lambda c: (dense(c) is None, -(dense(c) or 0), -(c["tops"] or 0), c["prix"] or 1e12))
    return cand[:n], cap


# ─────────────────────────────── canaux CAN ─────────────────────────────
F_HZ = 500                     # non-cote: fréquence de commande demandée par le prompt du 2026-10-07 (Hz)
CHARGE_MAX = 0.7               # non-cote: PROPOSÉ, charge maximale d'un bus CAN (marge de 30 % pour les retards et erreurs)


def calcul_can(b=None) -> dict:
    """Canaux CAN pour 27 axes (et pour les 23 axes RobStride du 27 : cou et pinces sont des Feetech, en série)."""
    b = b or lire("bus.yaml")
    pr = b.get("protocole_robstride") or {}
    debit = 1e6 if "1 Mbit" in str(v(pr, "debit_can_defaut")) else None
    trames = 2 if "oui" in str(v(pr, "une_reponse_par_commande")).lower() or v(pr, "une_reponse_par_commande") is True else None
    out = dict(debit=debit, trames_par_axe=trames, f=F_HZ, charge=CHARGE_MAX, cas=[])
    for nom, etendue in (("protocole privé (trame étendue 29 bits)", True), ("protocole MIT (trame standard 11 bits)", False)):
        bt = bits_trame(b["trame_can"], etendue)
        for n_axes in (27, 23):
            if bt and debit and trames:
                c = canaux_can(n_axes, F_HZ, trames, bt["total"], debit, CHARGE_MAX)
                c100 = canaux_can(n_axes, F_HZ, trames, bt["total"], debit, 1.0)
                out["cas"].append(dict(protocole=nom, axes=n_axes, bits=bt, **c, canaux_100=c100["canaux"]))
    return out


# ─────────────────────────────── rapports ───────────────────────────────
def f1(x, n=1):
    return "—" if x is None else f"{x:,.{n}f}".replace(",", " ").replace(".", ",")


ENTETE = ("**Engendré** par `.venv/bin/python scripts/marche_composants.py --ecrire`. Ne pas éditer à la main. "
          "**Données seulement** : aucune intégration à l'explorateur, aucun achat (fiche 0066). Contexte DÉCIDÉ "
          "(fiche 0070, Jeremy, 2026-10-07) : « Les deux robots, YXOR Lab et YXOR, fonctionnent entièrement sur "
          "batterie. Je préfère NVIDIA Jetson, mais je veux une comparaison chiffrée avec le Raspberry Pi 5 et ses "
          "cartes d'IA. » Sources lues le 2026-10-07, téléchargées hors du dépôt, inscrites à "
          "`params/fournisseurs.yaml` (non redistribuables) ; une valeur non lue est un trou (—), jamais estimée.")


def trous(rows, champs):
    return {lib: sum(1 for r in rows if r[k] is None) for k, lib in champs}


def svg_nuage(points, titre, xl, yl, logx=False, logy=False, diag=None) -> str:
    """Nuage de points, une teinte par famille (au plus 4 + gris), échelles éventuellement logarithmiques."""
    W, H, ML, MB, MT, MR = 780, 440, 64, 46, 40, 190                   # non-cote: mise en page en px
    pts = [p for p in points if p["x"] and p["y"]]
    if not pts:
        return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 40"><text x="10" y="24">aucun point</text></svg>'
    fx = (lambda x: math.log10(x)) if logx else (lambda x: x)
    fy = (lambda y: math.log10(y)) if logy else (lambda y: y)
    xs, ys = [fx(p["x"]) for p in pts], [fy(p["y"]) for p in pts]
    x0, x1 = min(xs), max(xs)
    y0, y1 = min(ys), max(ys)
    dx, dy = (x1 - x0) or 1, (y1 - y0) or 1
    x0, x1, y0, y1 = x0 - 0.05 * dx, x1 + 0.05 * dx, y0 - 0.05 * dy, y1 + 0.05 * dy
    X = lambda x: ML + (fx(x) - x0) / (x1 - x0) * (W - ML - MR)
    Y = lambda y: H - MB - (fy(y) - y0) / (y1 - y0) * (H - MB - MT)
    fams = list(dict.fromkeys(p["famille"] for p in pts))
    COUL = ["#2a78d6", "#eb6834", "#1baf7a", "#a34fc2", "#c9a227", "#8a8984", "#d14a7c"]   # palette de référence
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{titre}">',
         "<style>:root{--s:#fcfcfb;--t1:#0b0b0b;--t2:#52514e;--g:#e4e3df}"
         "@media (prefers-color-scheme: dark){:root{--s:#1a1a19;--t1:#fff;--t2:#c3c2b7;--g:#33332f}}"
         "text{font:11px system-ui,sans-serif;fill:var(--t2)} .t{fill:var(--t1);font-weight:600;font-size:12px}"
         ".grid{stroke:var(--g)}</style>", f'<rect width="{W}" height="{H}" fill="var(--s)"/>',
         f'<text x="{ML}" y="20" class="t">{titre}</text>']
    for k in range(6):
        gx, gy = x0 + k * (x1 - x0) / 5, y0 + k * (y1 - y0) / 5
        vx, vy = (10 ** gx if logx else gx), (10 ** gy if logy else gy)
        o.append(f'<line class="grid" x1="{X(vx):.1f}" y1="{MT}" x2="{X(vx):.1f}" y2="{H - MB}"/>'
                 f'<text x="{X(vx):.1f}" y="{H - MB + 14}" text-anchor="middle">{vx:.3g}</text>'
                 f'<line class="grid" x1="{ML}" y1="{Y(vy):.1f}" x2="{W - MR}" y2="{Y(vy):.1f}"/>'
                 f'<text x="{ML - 6}" y="{Y(vy) + 4:.1f}" text-anchor="end">{vy:.3g}</text>')
    o.append(f'<text x="{(ML + W - MR) / 2}" y="{H - 8}" text-anchor="middle">{xl}</text>'
             f'<text x="14" y="{(MT + H - MB) / 2}" transform="rotate(-90 14 {(MT + H - MB) / 2})" text-anchor="middle">{yl}</text>')
    for p in pts:
        c = COUL[fams.index(p["famille"]) % len(COUL)]
        o.append(f'<circle cx="{X(p["x"]):.1f}" cy="{Y(p["y"]):.1f}" r="4.5" fill="{c}" stroke="var(--s)" stroke-width="1.5">'
                 f'<title>{p["nom"]} : {p["x"]:.3g} ; {p["y"]:.3g}</title></circle>')
    for k, fa in enumerate(fams):
        y = MT + 10 + k * 18
        o.append(f'<circle cx="{W - MR + 18}" cy="{y}" r="4.5" fill="{COUL[k % len(COUL)]}"/>'
                 f'<text x="{W - MR + 28}" y="{y + 4}">{fa.replace("_", " ")}</text>')
    o.append("</svg>")
    return "\n".join(o)


def rapport_batteries(bat, bs) -> str:
    rs = plages("robstride")
    g = groupes(rs)
    ft = groupes(plages("feetech"))
    tab = tableau_tension(bat, g)
    cles = [k for k in g if k]
    L = ["# Marché des batteries (2026-10)", "", ENTETE, "",
         f"{len(bs)} produits, {len(bat['marche']['sources'])} sources. Constantes de chimie lues (V par cellule : "
         "nominale / fin de charge / coupure) : " + " ; ".join(
             f"{ch} {f1(chimie(bat, ch)['tension_nominale_V'], 2)} / {f1(chimie(bat, ch)['tension_max_V'], 2)} / "
             f"{f1(chimie(bat, ch)['tension_min_V'], 2)}" for ch in ("li_ion", "lifepo4", "lipo")) + ".", "",
         "## Tension : combien de cellules en série", "",
         "Plages de fonctionnement PUBLIÉES des RobStride (la plus étroite de chaque produit, fiche 0064) : "
         + " ; ".join(f"{a:g}–{b:g} V : {', '.join(ids)}" for (a, b), ids in ((k, g[k]) for k in cles))
         + (f" ; non relevée : {', '.join(g[None])}" if None in g else "") + ". La protection de surtension des "
         "RobStride est à 60 V (manuel RS00, p. 28 et 73) et le freinage renvoie de l'énergie dans le bus : marge de "
         f"régénération PROPOSÉE de {f1(CRITERES['marge_regeneration_V'], 0)} V sous 60 V. Le seuil réglementaire de "
         "« très basse tension » (60 V continu, souvent cité) n'a PAS été lu dans une norme ici.", "",
         "| Chimie | S | V min | V nominale | V pleine charge | Marge sous 60 V | "
         + " | ".join(f"{a:g}–{b:g} V" for a, b in cles) + " | Marge de régénération |",
         "| --- | ---: | ---: | ---: | ---: | ---: | " + " | ".join(":-:" for _ in cles) + " | :-: |"]
    for r in tab:
        if r.get("S"):
            L.append(f"| {r['chimie']} | {r['S']} | {f1(r['Vmin'])} | {f1(r['Vnom'])} | {f1(r['Vmax'])} | "
                     f"{f1(r['marge_seuil'])} | " + " | ".join("oui" if r["ok"][k] else "non" for k in cles)
                     + f" | {'oui' if r['regen_ok'] else 'non'} |")
    L += ["", "Feetech (petits axes, rail séparé par convertisseur, ou petit pack 2S) : "
          + " ; ".join(f"{a:g}–{b:g} V : {', '.join(ids)}" for (a, b), ids in ((k, ft[k]) for k in ft if k))
          + (f" ; non relevée : {', '.join(ft[None])}" if None in ft else "") + ".", "",
          "## Les produits", "",
          "Énergie : publiée, sinon CALCULÉE (V nominale × Ah, marquée *). Densités calculées depuis la masse et les "
          "cotes. CHF HT : taux BCE de `budget.yaml` ; un prix TTC sans taux connu reste TTC (prudent).", "",
          "| Produit | Famille | V | Ah | Wh | A continu | g | Wh/kg | Wh/L | CHF HT | Disponibilité CH/UE |",
          "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |"]
    for b in sorted(bs, key=lambda x: (x["famille"], -(x["Wh_kg"] or 0))):
        L.append(f"| {b['nom']} | {b['famille']} | {f1(b['V'])} | {f1(b['Ah'], 2)} | {f1(b['E'], 1)}{'*' if b['E_calculee'] else ''} | "
                 f"{f1(b['I'], 0)} | {f1(b['m'] and b['m'] * 1000, 0)} | {f1(b['Wh_kg'], 0)} | {f1(b['Wh_L'], 0)} | "
                 f"{f1(b['prix'], 2)} | {str(b['dispo'] or '—')[:60]} |")
    vmin = max(k[0] for k in cles if k[1] >= 60) if cles else 24.0
    for Mr in CRITERES["robots_kg"]:
        top, budget, vh = pertinentes_batteries(bs, bat, Mr, vmin)
        L += ["", f"## Les 10 plus pertinentes pour un robot de {f1(Mr, 0)} kg", "",
              f"Critères PROPOSÉS : budget de masse {f1(CRITERES['part_batterie'] * 100, 0)} % du robot ({f1(budget, 2)} kg de "
              f"cellules ou de packs, sans boîtier ni câblage) ; tension du pack entre {f1(vmin, 0)} V (coupure) et "
              f"{f1(vh, 0)} V (pleine charge) ; le plus d'énergie, puis le moins cher. Limites de mise en série publiées "
              "respectées.", "",
              "| # | Produit | Montage | S | Wh | kg | V pleine charge | A continu | CHF HT |",
              "| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
        for i, b in enumerate(top, 1):
            c = b["comp"]
            L.append(f"| {i} | {b['nom']} | {c['n']} série × {c['m']} parallèle | {c['S']} | {f1(c['E'], 0)} | "
                     f"{f1(c['masse'], 2)} | {f1(c['Vmax'])} | {f1(c['I'], 0)} | {f1(c['prix'], 0)} |")
    L += ["", "## Envoi vers la Suisse", ""]
    for k, r in (bat.get("regles_envoi_ch") or {}).items():
        L.append(f"- **{r.get('transporteur', k)}** : {r.get('resume')} (source `{r.get('source')}`)")
    t = trous(bs, (("E", "énergie"), ("m", "masse"), ("vol", "cotes"), ("I", "courant continu"), ("prix", "prix")))
    L += ["", "## Trous", "", " ; ".join(f"{k} : {n}" for k, n in t.items()) + f" (sur {len(bs)}).", "",
          f"![Énergie et masse]({SVGS['batteries'].name})"]
    return "\n".join(L) + "\n"


def rapport_calculateurs(cal, cs) -> str:
    meta = cal.get("meta") or {}
    L = ["# Marché des calculateurs (2026-10)", "", ENTETE, "",
         f"{len(cs)} produits, {len(cal['marche']['sources'])} sources.", "", "## Mises en garde sur les TOPS", ""]
    L += [f"- {m}" for m in meta.get("mises_en_garde_tops") or []]
    L += ["", "Seuls les TOPS **INT8 dense** se comparent : colonne « dense ». Le chiffre affiché par le fabricant est "
          "donné à côté, avec sa précision.", "", "## Les produits", "",
          "| Produit | Famille | TOPS dense | TOPS affichés (précision) | W max | TOPS/W | CHF HT | TOPS/CHF | CAN intégré |",
          "| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | --- |"]
    for c in sorted(cs, key=lambda x: (x["famille"], -(x["tops"] or 0))):
        d = dense(c)
        L.append(f"| {c['nom']} | {c['famille']} | {f1(d, 0)} | {f1(c['tops'], 0)} ({c['precision'] or '—'}) | "
                 f"{f1(c['pmax'], 0)} | {f1(d / c['pmax'] if d and c['pmax'] else None, 2)} | {f1(c['prix'], 0)} | "
                 f"{f1(d / c['prix'] if d and c['prix'] else None, 3)} | "
                 f"{'oui' if c['can'] is True else ('non' if c['can'] is False else '—')}"
                 f"{(' (' + str(c['can_n']) + ')') if c['can_n'] else ''} |")
    for Mr in CRITERES["robots_kg"]:
        top, cap = pertinents_calculateurs(cs, Mr)
        L += ["", f"## Les plus pertinents pour un robot de {f1(Mr, 0)} kg", "",
              f"Critères PROPOSÉS : puissance maximale ≤ {f1(cap, 0)} W (ou non publiée, DIT) ; produits en vente "
              "(annoncés et fin de production exclus) ; classés par TOPS INT8 dense, puis TOPS affichés, puis prix. Un "
              "MODULE Jetson seul exige une carte porteuse (famille « porteuse » ci-dessus), NON comptée dans son prix "
              "ni dans sa masse.", "",
              "| # | Produit | TOPS dense | TOPS affichés | W max | CHF HT | CAN intégré |",
              "| ---: | --- | ---: | --- | ---: | ---: | --- |"]
        for i, c in enumerate(top, 1):
            L.append(f"| {i} | {c['nom']} | {f1(dense(c), 0)} | {f1(c['tops'], 0)} ({c['precision'] or '—'}) | "
                     f"{f1(c['pmax'], 0) if c['pmax'] else 'non publiée'} | {f1(c['prix'], 0)} | "
                     f"{'oui' if c['can'] is True else ('non' if c['can'] is False else '—')} |")
    L += ["", "## Marché en 2026", ""] + [f"- {m}" for m in meta.get("contexte_marche_2026") or []]
    L += ["", "## Trous", ""] + [f"- {m}" for m in meta.get("trous") or []]
    L += ["", f"![TOPS par watt et par franc]({SVGS['calculateurs'].name})"]
    return "\n".join(L) + "\n"


def rapport_bus(b, rows, can) -> str:
    pr = b.get("protocole_robstride") or {}
    L = ["# Marché des cartes de bus (2026-10)", "", ENTETE, "",
         f"{len(rows)} produits, {len(b['marche']['sources'])} sources.", "", "## Protocole CAN des RobStride", ""]
    for k, x in pr.items():
        if isinstance(x, dict):
            L.append(f"- **{k.replace('_', ' ')}** : {x.get('valeur') if x.get('valeur') is not None else '— (non lu)'}"
                     f"{(' — ' + str(x.get('note'))[:220]) if x.get('note') else ''}")
    L += ["", "## Combien de canaux CAN pour 27 axes à 500 Hz", "",
          "Calcul écrit : une commande et une réponse par axe et par cycle (protocole RobStride), 8 octets chacune ; "
          "trame au PIRE bourrage (un bit inséré au plus tous les 4 bits, du SOF à la fin du CRC), intertrame la plus "
          f"longue des deux lues ; débit {f1((can['debit'] or 0) / 1e6, 0)} Mbit/s (défaut RobStride, CAN-FD non "
          f"documenté) ; charge maximale PROPOSÉE {f1(can['charge'] * 100, 0)} %. Le 27 axes de la fiche 0069 compte 4 "
          "petits axes (cou 2, pinces 2) en Feetech sur bus série : 23 axes sur CAN.", "",
          "| Protocole | Axes | Bits par trame (bourrables + bourrage + fixes) | Débit nécessaire | Canaux à 100 % | "
          f"Canaux à {f1(can['charge'] * 100, 0)} % |", "| --- | ---: | --- | ---: | ---: | ---: |"]
    for c in can["cas"]:
        bt = c["bits"]
        L.append(f"| {c['protocole']} | {c['axes']} | {bt['total']} ({bt['bourrable']} + {bt['stuff']} + {bt['fixe']}) | "
                 f"{f1(c['besoin'] / 1e6, 2)} Mbit/s | {c['canaux_100']} | **{c['canaux']}** |")
    L += ["", "## Les produits", "",
          "| Produit | Famille | Canaux | CAN-FD | Interface | Pilote Linux | g | CHF HT |",
          "| --- | --- | --- | --- | --- | --- | ---: | ---: |"]
    for r in sorted(rows, key=lambda x: x["famille"] or ""):
        L.append(f"| {r['nom']} | {r['famille']} | {r['canaux'] if r['canaux'] is not None else '—'} | "
                 f"{r['fd'] if r['fd'] is not None else '—'} | {str(r['hote'] or '—')[:40]} | {str(r['linux'] or '—')[:50]} | "
                 f"{f1(r['masse'], 0)} | {f1(r['prix'], 0)} |")
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ecrire", action="store_true")
    a = ap.parse_args(argv)
    bat, cal, b = lire("batteries.yaml"), lire("calculateurs.yaml"), lire("bus.yaml")
    bs, cs, rows = batteries(bat), calculateurs(cal), bus(b)
    can = calcul_can(b)
    print(f"  marché : {len(bs)} batteries, {len(cs)} calculateurs, {len(rows)} cartes de bus ; "
          f"{len(bat['marche']['sources']) + len(cal['marche']['sources']) + len(b['marche']['sources'])} sources")
    for c in can["cas"]:
        print(f"  CAN {c['protocole']}, {c['axes']} axes à {F_HZ} Hz : {c['bits']['total']} bits/trame, "
              f"{c['besoin'] / 1e6:.2f} Mbit/s -> {c['canaux']} canaux à {can['charge']:.0%} ({c['canaux_100']} à 100 %)")
    if a.ecrire:
        DOCS["batteries"].write_text(rapport_batteries(bat, bs), encoding="utf-8")
        DOCS["calculateurs"].write_text(rapport_calculateurs(cal, cs), encoding="utf-8")
        DOCS["bus"].write_text(rapport_bus(b, rows, can), encoding="utf-8")
        SVGS["batteries"].write_text(svg_nuage([dict(x=r["m"] and r["m"] * 1000, y=r["E"], nom=r["nom"], famille=r["famille"])
                                                for r in bs], "Énergie (Wh) selon la masse (g), échelles logarithmiques",
                                               "masse (g)", "énergie (Wh)", logx=True, logy=True), encoding="utf-8")
        pts = [dict(x=dense(c) / c["prix"] if dense(c) and c["prix"] else None,
                    y=dense(c) / c["pmax"] if dense(c) and c["pmax"] else None, nom=c["nom"], famille=c["famille"])
               for c in cs]
        SVGS["calculateurs"].write_text(svg_nuage(pts, "TOPS INT8 dense par watt (vertical) et par franc HT (horizontal)",
                                                  "TOPS dense par CHF HT", "TOPS dense par W"), encoding="utf-8")
        for k in DOCS:
            print(f"  -> {DOCS[k].relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
