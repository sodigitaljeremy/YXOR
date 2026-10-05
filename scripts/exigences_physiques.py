#!/usr/bin/env python3
"""Exigences physiques par tâche, niveau et taille : calculs directs (phase 3a, fiche 0069).

    .venv/bin/python scripts/exigences_physiques.py            # résumé
    .venv/bin/python scripts/exigences_physiques.py --ecrire   # rapport, courbes, table de résultats

Créé le 2026-10-05. ÉTUDE, aucune décision. Pour chaque tâche de
params/capacites.yaml qui ne demande PAS de simulation (et le relevé, en
quasi statique), pour chaque niveau et pour H de 0,50 à 1,40 m (pas 0,05) :
couple et puissance nécessaires par articulation sollicitée.

FORME DES RÉSULTATS (point 5 du prompt) : chaque tâche est calculée SEULE, et
chaque couple est rangé sous la forme LINÉAIRE en la masse du robot M :

    τ(tâche, niveau, H, articulation) = a · M + b      (a en N·m/kg, b en N·m)

`a` porte ce qui grandit avec le robot (son propre poids, ses segments),
`b` ce qui n'en dépend pas (la charge, la force de poussée). L'explorateur
(phase 4) combine un profil de capacités par le MAXIMUM, articulation par
articulation, avec la VRAIE masse de chaque solution, sans rien recalculer :
`combiner()`. Les courbes du rapport utilisent une masse de référence (loi
écrite ci-dessous) seulement pour être tracées.

LOIS ET HYPOTHÈSES (toutes écrites, aucune cachée) :
  · longueurs : ratios ANSUR de params/anthropometry.yaml × H (bras de levier ∝ H) ;
  · masses des segments : fractions de Winter (params/anthropometry.yaml) × M ;
    leur centre de masse au MILIEU du segment (hypothèse) ;
  · masse de référence des courbes : M(H) = M_TB × (H / H_TB)³, ToddlerBot
    (3,454 kg à 0,56 m, params/actionneurs.yaml, référence de calcul :
    décision 3) — l'étude S du 2026-10-04 pesait 2,3 fois plus à 0,61 m :
    c'est pourquoi les résultats sont rangés en a·M + b ;
  · rendement : NON appliqué. Les puissances sont MÉCANIQUES, à la sortie de
    l'actionneur ; la puissance électrique demande le rendement de chaque
    actionneur, qui n'est pas publié uniformément (phase 4) ;
  · g = 9,80665 m/s².
  Hypothèses propres à chaque tâche : dans HYP, avec leur statut.
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
DOC = REPO / "docs" / "exigences-physiques-2026-10.md"
SVG = REPO / "docs" / "exigences-physiques-2026-10.svg"
CSV = REPO / "exports" / "exigences" / "taches.csv"
G = 9.80665                       # non-cote: pesanteur normale (m/s²)
HS = [round(0.50 + 0.05 * i, 2) for i in range(19)]      # non-cote: grille de H, 0,50 à 1,40 m

# Hypothèses des tâches : valeur, statut. PROPOSÉES par Claude (2026-10-05),
# sauf mention ; toutes à remplacer par une mesure ou une simulation.
HYP = {
    "poussee_saut_frac": (0.25, "course de poussée du saut = 25 % de la hauteur de hanche (accroupi → extension)"),
    "inclinaison_tibia_deg": (None, "accroupi du saut et du relevé : params/exigences_S.yaml (releve.inclinaison_tibia_deg)"),
    "levier_cheville_frac": (0.5, "au saut, la réaction du sol passe à mi-longueur du pied devant la cheville"),
    "extension_cheville_deg": (20, "au saut, la cheville s'étend de 20° au-delà de l'angle d'accroupi"),
    "distance_charge_m": (0.30, "charge lourde : à 30 cm du torse (niveau CONFIRMÉ par Jeremy le 2026-10-05)"),
    "frottement": (0.5, "coefficient de frottement pince/objet et pied/sol"),
    "levier_pince_frac": (0.5, "levier du doigt de la pince = moitié de la longueur de main"),
    "acceleration_geste_s": (0.2, "geste rapide : vitesse atteinte en 0,2 s"),
    "inclinaison_buste_deg": (30, "buste incliné de 30° (roulis ou tangage)"),
    "part_tronc_au_dessus_taille": (0.5, "la moitié de la masse du tronc (Winter) est au-dessus de la taille"),
    "marge_avant_pied_frac": (0.5, "équilibre : le centre de pression ne dépasse pas la moitié avant du pied"),
}


def lire(nom):
    return yaml.safe_load((REPO / "params" / nom).read_text(encoding="utf-8"))


_REF = {}


def ref_masse(H):
    """M(H) = M_TB × (H/H_TB)³ ; la référence est lue UNE fois (le catalogue est gros)."""
    if not _REF:
        rt = lire("actionneurs.yaml")["reference_toddlerbot"]
        _REF.update(M=rt["masse_totale_kg"]["valeur"], H=rt["hauteur_m"]["valeur"])
    return _REF["M"] * (H / _REF["H"]) ** 3


# ─────────────────────────────── tâches ─────────────────────────────────
def calculer(H: float, cap: dict, an: dict, rel: dict) -> list[dict]:
    """Toutes les lignes (tâche, niveau, articulation) à la taille H : a, b, puissance (aP, bP), ω."""
    R = {k: v["valeur"] for k, v in an["ratios"].items()}
    W = {k: (v["valeur"] if isinstance(v, dict) else v) for k, v in an["masses"].items()}
    L = {k: R[k] * H for k in ("cuisse", "tibia", "bras", "avant_bras", "main_longueur", "hauteur_hanche",
                               "tronc_hauteur", "tete_hauteur", "pied_longueur", "cheville_hauteur")}
    alpha = math.radians(rel["inclinaison_tibia_deg"]["valeur"])
    jambe = rel["repartition_jambes"]["valeur"]
    out = []

    def ligne(t, niv, art, a, b, aP=0.0, bP=0.0, w=None, note=""):
        out.append(dict(tache=t, niveau=niv, H=H, articulation=art, a=a, b=b, aP=aP, bP=bP, omega=w, note=note))

    # saut vertical : M·g·(1 + h/d) pendant la course d, en accroupi
    d = HYP["poussee_saut_frac"][0] * L["hauteur_hanche"]
    for h_cm in cap["taches"]["saut_vertical"]["niveaux"]:
        h = h_cm / 100
        v = math.sqrt(2 * G * h)
        fpk = G * (1 + h / d) * jambe                      # force par jambe, par kg de M
        tp = 2 * d / v                                       # durée de poussée (accélération constante)
        lev = {"knee": L["tibia"] * math.sin(alpha),
               "hip_pitch": abs(L["tibia"] * math.sin(alpha) - L["cuisse"]),
               "ankle_pitch": HYP["levier_cheville_frac"][0] * L["pied_longueur"]}
        dth = {"knee": math.pi / 2 + alpha, "hip_pitch": math.pi / 2,
               "ankle_pitch": alpha + math.radians(HYP["extension_cheville_deg"][0])}
        for art in ("hip_pitch", "knee", "ankle_pitch"):
            w = 2 * dth[art] / tp                            # vitesse angulaire de pointe (rampe linéaire)
            ligne("saut_vertical", h_cm, art, fpk * lev[art], 0.0, fpk * lev[art] * w, 0.0, w,
                  f"poussée {tp * 1000:.0f} ms ; puissance = borne haute (couple max × vitesse max)")

    # charge lourde à 30 cm du torse, tronc droit, jambes tendues
    dc = HYP["distance_charge_m"][0]
    m_bras, m_ab = W["bras"] + W["avant_bras"] + W["main"], W["avant_bras"] + W["main"]
    for mc in cap["taches"]["charge_lourde"]["niveaux"]:
        lev_coude = min(dc, L["avant_bras"] + L["main_longueur"] / 2)
        ligne("charge_lourde", mc, "shoulder_pitch", m_bras * G * dc / 2, mc * G * dc / 2)
        ligne("charge_lourde", mc, "elbow_roll", m_ab * G * L["avant_bras"] / 2, mc * G * lev_coude / 2)
        ligne("charge_lourde", mc, "waist_pitch", 0.0, mc * G * dc)
        for art in ("hip_pitch", "knee", "ankle_pitch"):
            ligne("charge_lourde", mc, art, 0.0, mc * G * dc / 2,
                  note="équilibre : M ≥ m·(d/x − 1), x = moitié avant du pied (voir contraintes)")

    # saisie bras tendu à l'horizontale, objet à mi-main
    Lb, La, Lm = L["bras"], L["avant_bras"], L["main_longueur"]
    mu, lp = HYP["frottement"][0], HYP["levier_pince_frac"][0] * Lm
    for mo in cap["taches"]["saisie"]["niveaux"]:
        ligne("saisie", mo, "shoulder_pitch",
              G * (W["bras"] * Lb / 2 + W["avant_bras"] * (Lb + La / 2) + W["main"] * (Lb + La + Lm / 2)),
              mo * G * (Lb + La + Lm / 2))
        ligne("saisie", mo, "elbow_roll", G * (W["avant_bras"] * La / 2 + W["main"] * (La + Lm / 2)),
              mo * G * (La + Lm / 2))
        ligne("saisie", mo, "wrist_pitch", G * W["main"] * Lm / 2, mo * G * Lm / 2)
        ligne("saisie", mo, "pince", 0.0, mo * G / (2 * mu) * lp, note="serrage à deux mors, frottement μ")

    # relevé, phase finale quasi statique (accroupi profond, comme le T5 de la grille)
    for niv in cap["taches"]["releve"]["niveaux"]:
        ligne("releve", niv, "knee", G * jambe * L["tibia"] * math.sin(alpha), 0.0,
              note="phase finale (accroupi) seulement ; les phases au sol demandent la simulation")
        ligne("releve", niv, "hip_pitch", G * jambe * abs(L["tibia"] * math.sin(alpha) - L["cuisse"]), 0.0)

    # poussée horizontale, mains à hauteur d'épaule, bras tendus
    h_ep = L["hauteur_hanche"] + L["tronc_hauteur"]
    h_ge = L["tibia"] + L["cheville_hauteur"]
    h_ta = L["hauteur_hanche"] + 0.5 * L["tronc_hauteur"]
    for F in cap["taches"]["poussee"]["niveaux"]:
        ligne("poussee", F, "ankle_pitch", 0.0, F * h_ep / 2, note=f"frottement : M ≥ F / (μ·g)")
        ligne("poussee", F, "knee", 0.0, F * (h_ep - h_ge) / 2)
        ligne("poussee", F, "hip_pitch", 0.0, F * (h_ep - L["hauteur_hanche"]) / 2)
        ligne("poussee", F, "waist_pitch", 0.0, F * (h_ep - h_ta), note="bras tendus : épaule et coude non chargés")

    # gestes : bras rigide (tige), vitesse du bout atteinte en t_a
    La_tot = Lb + La + Lm
    ta = HYP["acceleration_geste_s"][0]
    for vt in cap["taches"]["gestes_pointage"]["niveaux"]:
        w = vt / La_tot
        I_par_kg = m_bras * La_tot ** 2 / 3
        ligne("gestes_pointage", vt, "shoulder_pitch", I_par_kg * w / ta + m_bras * G * La_tot / 2, 0.0,
              I_par_kg * w / ta * w, 0.0, w, f"énergie cinétique ½·I·ω² = {0.5 * I_par_kg * w * w:.3g} J par kg de M")

    # buste incliné de θ
    th = math.radians(HYP["inclinaison_buste_deg"][0])
    m_haut = HYP["part_tronc_au_dessus_taille"][0] * W["tronc"] + W["tete_et_cou"] + 2 * m_bras
    for niv in cap["taches"]["buste"]["niveaux"]:
        if "roulis" in str(niv):
            for art in ("waist_roll", "waist_pitch"):
                ligne("buste", niv, art, m_haut * G * 0.5 * L["tronc_hauteur"] * math.sin(th), 0.0)
        ligne("buste", niv, "waist_yaw", 0.0, 0.0, note="lacet : pas de couple statique (inertie seulement)")

    # tête à l'horizontale (pire cas)
    for niv in cap["taches"]["tete"]["niveaux"]:
        arts = ["neck_pitch"] + (["neck_roll"] if niv == 3 else [])
        for art in arts:
            ligne("tete", niv, art, W["tete_et_cou"] * G * 0.5 * L["tete_hauteur"], 0.0,
                  note="masse « tête et cou » de Winter : majorant")
    return out


def contraintes(H, cap, an):
    """Masses minimales imposées par l'équilibre (charge) et le frottement (poussée)."""
    xmax = HYP["marge_avant_pied_frac"][0] * an["ratios"]["pied_longueur"]["valeur"] * H
    dc, mu = HYP["distance_charge_m"][0], HYP["frottement"][0]
    out = {}
    for mc in cap["taches"]["charge_lourde"]["niveaux"]:
        out[("charge_lourde", mc)] = max(0.0, mc * (dc / xmax - 1))
    for F in cap["taches"]["poussee"]["niveaux"]:
        out[("poussee", F)] = F / (mu * G)
    return out


def tout(cap=None):
    cap = cap or lire("capacites.yaml")
    an, rel = lire("anthropometry.yaml"), lire("exigences_S.yaml")["releve"]
    lignes = [l for H in HS for l in calculer(H, cap, an, rel)]
    return cap, an, lignes


def combiner(lignes: list[dict], profil: dict, H: float, M: float) -> dict:
    """Couple requis par articulation pour un PROFIL {tâche: niveau}, à (H, M) : le MAXIMUM des tâches."""
    req = {}
    for l in lignes:
        if abs(l["H"] - H) < 1e-9 and l["tache"] in profil and l["niveau"] == profil[l["tache"]]:
            req[l["articulation"]] = max(req.get(l["articulation"], 0.0), l["a"] * M + l["b"])
    return req


# ─────────────────────────────── familles ───────────────────────────────
CORPS = ["robstride", "damiao", "steadywin", "cubemars", "myactuator", "hightorque", "encos", "unitree"]
PETITS = ["feetech", "dynamixel"]


def prix_chf(p, taux, D):
    """Prix en CHF HT. Tolère la forme des servos (devise dans `unite`, HT dans `prix_HT_EUR`) ;
    un taux de TVA inconnu (`tva_incluse: true`) garde le prix TTC, le plus prudent."""
    if not isinstance(p, dict) or not isinstance(p.get("valeur"), (int, float)):
        return None
    q = dict(p)
    if isinstance(q.get("prix_HT_EUR"), (int, float)):
        q = dict(valeur=q["prix_HT_EUR"], devise="EUR", tva_incluse=0.0)
    if not q.get("devise") and q.get("unite"):
        q["devise"] = str(q["unite"]).split()[0].upper()
    if isinstance(q.get("tva_incluse"), bool) or q.get("tva_incluse") is None:
        q["tva_incluse"] = 0.0
    try:
        return D.chf(q, taux)
    except (KeyError, TypeError):
        return None


def familles():
    import marche_actionneurs as MA
    import dimensionnement as D
    taux = yaml.safe_load((REPO / "params" / "budget.yaml").read_text(encoding="utf-8"))["taux_de_change"]
    fam, rows = MA.charger()
    out = {}
    for f in CORPS + PETITS:
        rs = [r for r in rows if r["famille"] == f]
        def rng(k):
            v = [r[k] for r in rs if isinstance(r[k], (int, float))]
            return (min(v), max(v)) if v else None
        prix = []
        for r in rs:
            c = prix_chf(r["prix"], taux, D)
            if c is not None:
                prix.append(c)
        pointes = [r["pointe"] or r["blocage"] for r in rs if (r["pointe"] or r["blocage"])]
        out[f] = dict(nom=fam.get(f, {}).get("nom", f).split(" (")[0], n=len(rs),
                      pointe=(min(pointes), max(pointes)) if pointes else None,
                      pointe_par_blocage=sum(1 for r in rs if not r["pointe"] and r["blocage"]),
                      blocage=rng("blocage"), continu=rng("continu"), masse=rng("masse"),
                      prix=(min(prix), max(prix)) if prix else None, n_prix=len(prix),
                      lab=any(5 <= p <= 20 for p in pointes), final60=any(p >= 60 for p in pointes),
                      final120=any(p >= 120 for p in pointes),
                      trous=sum(1 for r in rs if not r["pointe"]) , sans_continu=sum(1 for r in rs if not r["continu"]))
    return out


# ─────────────────────────────── sorties ────────────────────────────────
PALIERS = ["#9ec5f4", "#5b9ce8", "#2a78d6", "#174f9a"]   # une teinte, du clair au foncé (niveaux ordonnés)


def courbes_svg(lignes, cap):
    import itertools
    panneaux = []
    for (t, art), grp in itertools.groupby(sorted(lignes, key=lambda l: (l["tache"], l["articulation"])),
                                           key=lambda l: (l["tache"], l["articulation"])):
        grp = list(grp)
        if all(abs(l["a"]) < 1e-12 and abs(l["b"]) < 1e-12 for l in grp):
            continue
        panneaux.append((t, art, grp))
    ncol, PW, PH, ML, MT, GX, GY = 4, 210, 150, 44, 34, 40, 56     # non-cote: mise en page en px
    W = ML + ncol * PW + (ncol - 1) * GX + 16
    Ht = MT + math.ceil(len(panneaux) / ncol) * (PH + GY) + 10
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Ht}" width="100%" role="img" '
         'aria-label="Couple nécessaire selon la taille H, par tâche et par articulation">',
         "<style>:root{--s:#fcfcfb;--t1:#0b0b0b;--t2:#52514e;--g:#e4e3df}"
         "@media (prefers-color-scheme: dark){:root{--s:#1a1a19;--t1:#fff;--t2:#c3c2b7;--g:#33332f}}"
         "text{font:10px system-ui,sans-serif;fill:var(--t2)} .t{fill:var(--t1);font-weight:600;font-size:11px}"
         ".grid{stroke:var(--g)}</style>", f'<rect width="{W}" height="{Ht}" fill="var(--s)"/>',
         f'<text x="{ML}" y="16" class="t">Couple nécessaire (N·m) selon H (m), masse M(H) = ToddlerBot × (H/0,56)³ ; '
         f'du clair au foncé : niveaux croissants</text>']
    for i, (t, art, grp) in enumerate(panneaux):
        cx, cy = ML + (i % ncol) * (PW + GX), MT + (i // ncol) * (PH + GY)
        niveaux = list(dict.fromkeys(l["niveau"] for l in grp))
        ys = [l["a"] * ref_masse(l["H"]) + l["b"] for l in grp]
        ym = max(ys) * 1.08 or 1
        X = lambda h: cx + (h - HS[0]) / (HS[-1] - HS[0]) * PW
        Y = lambda v: cy + PH - v / ym * PH
        o.append(f'<text x="{cx}" y="{cy - 6}" class="t">{t.replace("_", " ")} · {art}</text>')
        for gy in (0, ym / 2 / 1.08, ym / 1.08):
            o.append(f'<line class="grid" x1="{cx}" y1="{Y(gy):.1f}" x2="{cx + PW}" y2="{Y(gy):.1f}"/>'
                     f'<text x="{cx - 3}" y="{Y(gy) + 3:.1f}" text-anchor="end">{gy:.3g}</text>')
        for h in (0.5, 1.0, 1.4):
            o.append(f'<text x="{X(h):.1f}" y="{cy + PH + 12}" text-anchor="middle">{h:g}</text>')
        # niveaux à courbe IDENTIQUE : une seule courbe, étiquettes réunies (relevé dos/ventre, tête 2/3 axes)
        courbes = {}
        for niv in niveaux:
            cle = tuple(round(l["a"] * ref_masse(l["H"]) + l["b"], 9) for l in grp if l["niveau"] == niv)
            courbes.setdefault(cle, []).append(niv)
        niveaux = [" = ".join(str(n) for n in ns) for ns in courbes.values()]
        reps = [ns[0] for ns in courbes.values()]
        for k, (niv, rep) in enumerate(zip(niveaux, reps)):
            pts = [(X(l["H"]), Y(l["a"] * ref_masse(l["H"]) + l["b"])) for l in grp if l["niveau"] == rep]
            col = PALIERS[min(k + (len(PALIERS) - len(niveaux)), len(PALIERS) - 1)]
            o.append(f'<polyline fill="none" stroke="{col}" stroke-width="2" points="'
                     + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'"><title>{t} {niv} — {art}</title></polyline>')
            x, y = pts[-1]
            o.append(f'<text x="{x - 2:.1f}" y="{y - 3:.1f}" text-anchor="end">{niv}</text>')
    o.append("</svg>")
    return "\n".join(o)


def rapport(cap, an, lignes, fams, refs):
    f3 = lambda v: "—" if v is None else f"{v:.3g}"
    rg = lambda r: "—" if not r else f"{r[0]:.3g} – {r[1]:.3g}"
    L = ["# Exigences physiques par tâche, niveau et taille (octobre 2026)", "",
         "**Engendré** par `.venv/bin/python scripts/exigences_physiques.py --ecrire`. Ne pas éditer à la main. "
         "**Étude, aucune décision** (phase 3a de la stratégie de la fiche 0069). Capacités et niveaux : "
         "`params/capacites.yaml`, confirmés par Jeremy le 2026-10-05.", "",
         "## 1 — Familles d'actionneurs : plages couvertes", "",
         "Depuis `params/actionneurs.yaml` (`candidats` et `marche`). Pointe : la pointe publiée, à défaut le "
         "blocage. **Lab** : au moins un modèle entre 5 et 20 N·m ; **final** : au moins un modèle ≥ 60 N·m "
         "(≥ 120 entre parenthèses). Ces deux ordres de grandeur viennent du prompt (Lab : étude du 2026-10-04 ; "
         "final : « ordre de grandeur Unitree G1 », NON lu) : ils seront recalculés en phase 3b.", "",
         "| Famille | Modèles | Pointe (N·m) | Continu publié (N·m) | Masse (g) | Prix (CHF HT) | Lab | Final ≥ 60 (≥ 120) | Sans pointe | Sans continu |",
         "| --- | ---: | --- | --- | --- | --- | --- | --- | ---: | ---: |"]
    for groupe, ids in (("corps", CORPS), ("petits axes", PETITS)):
        for f in ids:
            x = fams[f]
            L.append(f"| {x['nom']} ({groupe}) | {x['n']} | {rg(x['pointe'])}"
                     + (f" ({x['pointe_par_blocage']} au blocage)" if x['pointe_par_blocage'] else "")
                     + f" | {rg(x['continu'])} | "
                     f"{rg(x['masse'])} | {rg(x['prix'])} ({x['n_prix']}) | {'oui' if x['lab'] else 'non'} | "
                     f"{'oui' if x['final60'] else 'non'} ({'oui' if x['final120'] else 'non'}) | {x['trous']} | {x['sans_continu']} |")
    deux = [fams[f]["nom"] for f in CORPS if fams[f]["lab"] and fams[f]["final60"]]
    L += ["", f"Familles du corps qui couvrent à la fois le Lab et le final (≥ 60 N·m) : **{', '.join(deux) or 'aucune'}**.", "",
          "**PROPOSITION** (Claude, non écrite dans une fiche) : remplacer l'invariant « une famille » de la 0069 par "
          "« **une famille corps + une famille petits axes** ». Aucune famille du corps ne descend aux couples des "
          "doigts, du visage ou d'un petit cou (≤ 1 N·m, quelques grammes) : seuls les servos de bus (Feetech, "
          "Dynamixel) y sont. Garder une seule famille obligerait à des actionneurs de corps surdimensionnés au "
          "bout des bras et dans la tête.", "",
          "## 2 — Couple nécessaire selon H, par tâche et par articulation", "",
          f"![Couple nécessaire selon H]({SVG.name})", "",
          "Chaque résultat est rangé sous la forme **τ = a·M + b** (M : masse du robot ; `b` : la charge ou la force, "
          "indépendante du robot). Un profil de capacités se combine par le **maximum** par articulation, avec la "
          "vraie masse de chaque solution (`combiner()`), sans recalcul. Les courbes utilisent la masse de "
          "référence M(H) = 3,454 kg × (H/0,56)³ (ToddlerBot, décision 3) ; l'étude S du 2026-10-04 pesait 2,3 fois "
          "plus à 0,61 m : la part `a·M` s'en trouverait multipliée d'autant.", "",
          "### Lois et hypothèses", "",
          "- Longueurs : ratios ANSUR × H (bras de levier ∝ H). Masses : fractions de Winter × M, centre de masse "
          "au milieu de chaque segment. Masse de référence des courbes ∝ H³.",
          "- Rendement : non appliqué ; les puissances sont mécaniques (à la sortie de l'actionneur).",
          "- Saut : force M·g·(1 + h/d) pendant une course de poussée d, durée 2d/√(2gh) ; couples dans "
          "l'accroupi ; puissance = couple maximal × vitesse maximale (borne haute)."]
    for k, (v, txt) in HYP.items():
        L.append(f"- `{k}` = {v if v is not None else '(voir texte)'} : {txt}. PROPOSÉ par Claude, à remplacer.")
    L += ["", "### Masses minimales imposées (équilibre, frottement)", "", "| Tâche | Niveau | H = 0,60 m | H = 1,00 m | H = 1,40 m |",
          "| --- | --- | ---: | ---: | ---: |"]
    c = {H: contraintes(H, cap, an) for H in (0.6, 1.0, 1.4)}
    for k in c[0.6]:
        L.append(f"| {k[0].replace('_', ' ')} | {k[1]} | {c[0.6][k]:.1f} kg | {c[1.0][k]:.1f} kg | {c[1.4][k]:.1f} kg |")
    L += ["", "Charge lourde : le robot doit peser au moins m·(d/x − 1) pour que la charge ne le fasse pas basculer "
          "en avant (x : moitié avant du pied), **buste droit** : c'est une borne PESSIMISTE, car se pencher en "
          "arrière déplace le centre de gravité du robot et réduit cette masse (à chiffrer en simulation). "
          "Poussée : M ≥ F/(μ·g) pour ne pas glisser.", "",
          "### Trois courbes clés (masse de référence)", "", "| H (m) | M réf. (kg) | Genou, saut 30 cm (N·m) | "
          "Épaule, charge 10 kg (N·m) | Hanche, relevé (N·m) |", "| ---: | ---: | ---: | ---: | ---: |"]
    for H in (0.5, 0.6, 0.8, 1.0, 1.2, 1.4):
        M = ref_masse(H)
        g = lambda t, n, a: next(l["a"] * M + l["b"] for l in lignes
                                 if abs(l["H"] - H) < 1e-9 and l["tache"] == t and l["niveau"] == n and l["articulation"] == a)
        L.append(f"| {H:.2f} | {M:.1f} | {g('saut_vertical', 30, 'knee'):.1f} | {g('charge_lourde', 10, 'shoulder_pitch'):.1f} "
                 f"| {g('releve', 'depuis le dos', 'hip_pitch'):.1f} |")
    L += ["", "Non chiffré ici : marche, sol irrégulier, pente, course (simulation, phase 3b) ; mains à doigts et "
          "visage (un nombre d'actionneurs, pas un couple) ; lacet du buste et de la tête (inertie seulement).", "",
          "## 3 — Références simulables (marche, course)", ""]
    L += refs or ["(inventaire non disponible)"]
    return "\n".join(L) + "\n"


def refs_md():
    src = REPO / "params" / "references_simulables.yaml"
    if not src.exists():
        return None
    r = yaml.safe_load(src.read_text(encoding="utf-8"))
    L = ["Depuis `params/references_simulables.yaml` (lu le 2026-10-05).", "",
         "| Référence | Licence du modèle | Politique pré-entraînée téléchargeable | Faire tourner ici (CPU) | Entraîner |",
         "| --- | --- | --- | --- | --- |"]
    for x in r["references"]:
        L.append(f"| {x['nom']} | {x['licence']} | {x['politique']} | {x['inference']} | {x['entrainement']} |")
    return L


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ecrire", action="store_true")
    a = ap.parse_args(argv)
    cap, an, lignes = tout()
    print(f"  {len(lignes)} lignes (tâche × niveau × H × articulation), {len(HS)} tailles")
    if a.ecrire:
        CSV.parent.mkdir(parents=True, exist_ok=True)
        with CSV.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(lignes[0]))
            w.writeheader()
            w.writerows(lignes)
        DOC.write_text(rapport(cap, an, lignes, familles(), refs_md()), encoding="utf-8")
        SVG.write_text(courbes_svg(lignes, cap), encoding="utf-8")
        print(f"  -> {DOC.relative_to(REPO)}, {SVG.relative_to(REPO)}, {CSV.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
