#!/usr/bin/env python3
"""Choix de l'actionneur de S : faits, approvisionnement daté, grille d'exigences.

    .venv/bin/python scripts/choix_actionneurs.py            # résumé
    .venv/bin/python scripts/choix_actionneurs.py --ecrire   # docs/choix-actionneurs.md

Venv DU PROJET. Créé le 2026-10-01 (refonte R3). Remplace la notation
pondérée, archivée (archive/scripts/selection_multicritere.py) : AUCUN
score, aucun poids. Chaque exigence donne PASS, FAIL, UNKNOWN ou TESTED,
selon une règle écrite dans params/exigences_S.yaml.

Lit :
  params/actionneurs.yaml     catalogue, faits du comparatif, collecte (lu, jamais écrit)
  params/exigences_S.yaml     exigences, charge utile, hypothèses du relevé
  params/anthropometry.yaml   H_S (tailles.S), longueurs de segments
  params/mesures.yaml         mesures de banc : continu au blocage mesuré (TESTED, § 4 du protocole)
  exports/actionneurs/marche_15s.csv, via analyser_marche.py

Le dimensionnement reste dans scripts/dimensionnement.py : ce script
l'appelle à H_S, avec la charge utile en masse fixe.
"""
from __future__ import annotations

import argparse
import datetime
import math
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyser_marche as AM  # noqa: E402
import dimensionnement as D  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
EXIGENCES = REPO / "params" / "exigences_S.yaml"
ANTHRO = REPO / "params" / "anthropometry.yaml"
MESURES = REPO / "params" / "mesures.yaml"
CONFIG = REPO / "params" / "configuration_S.yaml"       # fiche 0067 : actionneur par articulation
DOC = REPO / "docs" / "choix-actionneurs.md"
G = 9.81
val = D.val


def lire(p: Path) -> dict:
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def f(x, n=2):
    return "—" if x is None else f"{x:.{n}f}".replace(".", ",")


# ─────────────────────────────── faits ───────────────────────────────────

def couples(c: dict) -> dict:
    """Nominal (le plus favorable en rotation) et blocage (le plus bas publié)."""
    cc = c["couple_continu_Nm"]
    rot = [val(cc)] if val(cc) is not None else []
    bloc = []
    for ac in cc.get("autres_conditions") or []:
        (bloc if "BLOCAGE" in (ac.get("condition") or "").upper() else rot).append(ac["valeur"])
    return dict(nominal=max(rot) if rot else None, blocage=min(bloc) if bloc else None,
                condition=cc.get("condition"))


def k_bas(cat: dict) -> tuple[float, list]:
    """Le plus petit rapport blocage / nominal publié au catalogue : CALCULÉ."""
    r = []
    for cid, c in cat["candidats"].items():
        cp = couples(c)
        if cp["nominal"] and cp["blocage"]:
            r.append((cp["blocage"] / cp["nominal"], cid))
    return min(r)[0], sorted(r)


def familles_de(cat: dict, cid: str) -> list:
    out = []
    for fid, fm in cat["familles"].items():
        if fm.get("S") == cid or cid in (fm.get("alternatives") or {}).get("S", []):
            out.append((fid, fm))
    return out


# ─────────────────────────── verdicts ────────────────────────────────────

def mesures_blocage(cid: str, chemin: Path = MESURES) -> list[dict]:
    """Les continus au blocage MESURÉS au banc pour `cid` (protocole, § 5).

    Une entrée de params/mesures.yaml compte si elle porte `actionneur: cid`
    et si son `alimente` désigne `candidats.<cid>.couple_continu_Nm.blocage`.
    Le catalogue n'est jamais réécrit : la mesure s'affiche à côté.
    """
    mes = ((yaml.safe_load(chemin.read_text(encoding="utf-8")) if chemin.exists() else {}) or {}).get("mesures") or {}
    cible = f"candidats.{cid}.couple_continu_Nm.blocage"
    return [dict(m, id=k) for k, m in mes.items()
            if (m or {}).get("actionneur") == cid and cible in (m.get("alimente") or [])]


def verdict_couple(cat, cid, H, ref_c, besoins, marge, kb, blocage_mesure=None):
    """T1 et T2, à la hauteur H, avec la référence chargée ref_c.

    `blocage_mesure` (N·m) remplace le continu prudent publié : T1 vaut
    alors TESTED s'il passe avec la mesure, FAIL sinon (protocole, § 4).
    """
    cl = D.classe_catalogue(cat, cid)
    cp = couples(cat["candidats"][cid])
    if cl["pointe"] is None or cl["masse"] is None:
        return dict(T1="UNKNOWN", T2="UNKNOWN", masse=None, detail="pointe ou masse inconnue")
    prud = cp["blocage"] if cp["blocage"] is not None else (cp["nominal"] * kb if cp["nominal"] else None)
    if blocage_mesure is not None:
        prud = blocage_mesure

    def tient(continu, quoi):
        conf = D.config_homogene(dict(cl, continu=continu))
        r = D.ratios(H, ref_c, conf, besoins, marge)
        if quoi == "rms":
            return all(x["rms"] is not None and x["rms"] <= 1 for x in r.values())
        return all(x["pointe"] <= 1 for x in r.values())

    if blocage_mesure is not None:
        t1 = "TESTED" if tient(prud, "rms") else "FAIL"
    elif cp["nominal"] is None:
        t1 = "UNKNOWN"
    elif tient(prud, "rms"):
        t1 = "PASS"
    elif tient(cp["nominal"], "rms"):
        t1 = "UNKNOWN"
    else:
        t1 = "FAIL"
    t2 = "PASS" if tient(cp["nominal"] or 1.0, "pointe") else "FAIL"
    conf = D.config_homogene(dict(cl, continu=prud))
    return dict(T1=t1, T2=t2, masse=D.masse(H, ref_c, conf, besoins), prudent=prud,
                base=("blocage MESURÉ" if blocage_mesure is not None else
                      "blocage publié" if cp["blocage"] is not None else f"nominal × k_bas ({f(kb, 3)})"),
                h_min_vit=D.h_min_vitesse(ref_c, conf, besoins) if cl["vitesse"] else None,
                vitesse_publiee=cl["vitesse"] is not None)


def releve(m_kg, H, anthro, rel, angle_deg):
    """Couples quasi statiques au genou et au tangage de hanche, par jambe."""
    L_t = anthro["ratios"]["tibia"]["valeur"] * H
    L_c = anthro["ratios"]["cuisse"]["valeur"] * H
    a = math.radians(angle_deg)
    w = m_kg * G * rel["repartition_jambes"]["valeur"]
    bras_genou = L_t * math.sin(a)                 # genou en avant de la verticale des chevilles
    bras_hanche = abs(L_t * math.sin(a) - L_c)     # cuisse horizontale : hanche en arrière du genou
    return dict(knee=w * bras_genou, hip_pitch=w * bras_hanche, L_t=L_t, L_c=L_c,
                bras_genou=bras_genou, bras_hanche=bras_hanche)


def evaluer(H: float, charge: float, mesures: Path = MESURES) -> dict:
    cat = D.charger_catalogue()
    ex, an = lire(EXIGENCES), lire(ANTHRO)
    analyse = AM.analyser(AM.SERIE)
    besoins = D.besoins_p1(analyse)
    ref = D.reference(cat, analyse)
    m_el = ex["electronique_toddlerbot"]["masse_kg"]["valeur"]
    # Retirés de la part mise à l'échelle : l'électronique ET, depuis la fiche
    # 0067 (2026-10-02), les 20 servos ToddlerBot du haut du corps (buste fixe).
    m_haut = D.masse_haut_du_corps_amont(cat, besoins)
    m_retire = m_el + m_haut
    marge = val(cat["dimensionnement"]["marge"])
    kb, rapports = k_bas(cat)
    cu = ex["charge_utile"]
    haut = max(cu["sensibilite_kg"])
    rel = ex["releve"]
    collecte = cat.get("collecte_criteres_manquants", {}).get("candidats", {})
    cs = cat["comparatif_S"]
    lignes = []
    for cid in cs["candidats"] + cs["references"]:
        c, fs = cat["candidats"][cid], cs[cid]
        v = {}
        ref_c = D.reference_charge(ref, m_retire, charge)
        mb = mesures_blocage(cid, mesures)
        bm = min(m["valeur"] for m in mb) if mb else None      # le plus faible des exemplaires
        dc = verdict_couple(cat, cid, H, ref_c, besoins, marge, kb, bm)
        v["T1"], v["T2"] = dc["T1"], dc["T2"]
        if dc.get("vitesse_publiee"):
            v["T3"] = "PASS" if dc["h_min_vit"] <= H else "FAIL"
        else:
            v["T3"] = "UNKNOWN"
        dh = verdict_couple(cat, cid, H, D.reference_charge(ref, m_retire, haut), besoins, marge, kb, bm)
        ok = ("PASS", "TESTED")
        if "FAIL" in (v["T1"], v["T2"]) or "UNKNOWN" in (v["T1"], v["T2"]):
            v["T4"] = "FAIL" if "FAIL" in (v["T1"], v["T2"]) else "UNKNOWN"
        else:
            v["T4"] = "PASS" if dh["T1"] in ok and dh["T2"] in ok else "UNKNOWN"
        pointe = val(c["couple_pointe_Nm"])
        if dc["masse"] is None or pointe is None:
            v["T5"], rv = "UNKNOWN", None
        else:
            rv = releve(dc["masse"], H, an, rel, rel["inclinaison_tibia_deg"]["valeur"])
            v["T5"] = "PASS" if marge * max(rv["knee"], rv["hip_pitch"]) <= pointe else "FAIL"
        tel = fs["telemetrie"]
        champs = [tel.get(k) for k in ("position", "couple_ou_courant", "temperature")]
        v["T6"] = "FAIL" if False in champs else ("UNKNOWN" if None in champs else "PASS")
        prot = val(c.get("protection_thermique_C") or {})
        ep = (collecte.get(cid) or {}).get("E_protections")
        ep = ep.get("valeur") if isinstance(ep, dict) else ep
        v["T7"] = "PASS" if prot is not None or (ep and re.search(r"\d+\s*°C", str(ep))) else "UNKNOWN"
        wd = (collecte.get(cid) or {}).get("E_watchdog")
        wd = wd.get("valeur") if isinstance(wd, dict) else wd
        v["T8"] = "PASS" if wd or "TIMEOUT" in (tel.get("detail") or "").upper() else "UNKNOWN"
        fams = familles_de(cat, cid)
        if not fams:
            v["T9"] = "FAIL"
        else:
            pc = [fm.get("protocole_commun", {}).get("valeur") for _, fm in fams]
            v["T9"] = ("PASS" if "CAN" in c["bus"] and True in pc else
                       "UNKNOWN" if "CAN" in c["bus"] else "FAIL")
        # approvisionnement, daté
        pr = fs.get("prix_revendeur") or c.get("prix") or {}
        v["A1"] = "PASS" if pr.get("valeur") is not None and pr.get("consulte_le") else "UNKNOWN"
        d = fs.get("distribution") or {}
        v["A2"] = "PASS" if d.get("suisse") or d.get("ue") else "UNKNOWN"
        gm = val(fs.get("garantie_mois") or {})
        v["A3"] = "UNKNOWN" if gm is None else ("PASS" if gm >= 12 else "FAIL")
        texte = " ".join(str(x.get("note") or "") for x in (fs.get("prix_revendeur") or {}, c.get("prix") or {}))
        v["A4"] = "PASS" if re.search(r"en stock|in stock", texte, re.I) else "UNKNOWN"
        lignes.append(dict(id=cid, nom=c["nom"], reference=bool(c.get("reference")), v=v, dc=dc, mesures=mb,
                           releve=rv, pointe=pointe, prix=pr, distribution=d, garantie=gm,
                           cle=D.cle_revision(c), familles=[fid for fid, _ in fams]))
    return dict(H=H, charge=charge, lignes=lignes, kb=kb, rapports=rapports, marge=marge, m_el=m_el,
                m_haut=m_haut, ref=ref, cat=cat, ex=ex, an=an, besoins=besoins)


def evaluer_configuration(H: float, v3: bool, jambes: dict | None = None) -> dict:
    """La configuration RETENUE (params/configuration_S.yaml, fiche 0067) à la hauteur H.

    Chaque articulation reçoit son actionneur, au continu prudent (blocage
    publié, sinon nominal x k_bas). Base v1 : buste fixe (servos ToddlerBot du
    haut du corps retirés). `v3` ajoute l'hypothèse de haut du corps (masse
    seulement) et le supplément de structure des logements RS02. `jambes`
    remplace la répartition, pour les tests.
    """
    cat, cfg = D.charger_catalogue(), lire(CONFIG)
    ex, an = lire(EXIGENCES), lire(ANTHRO)
    analyse = AM.analyser(AM.SERIE)
    besoins = D.besoins_p1(analyse)
    ref = D.reference(cat, analyse)
    marge = val(cat["dimensionnement"]["marge"])
    kb, _ = k_bas(cat)
    rel = ex["releve"]
    repart = dict(jambes or cfg["jambes"])
    m_retire = ex["electronique_toddlerbot"]["masse_kg"]["valeur"] + D.masse_haut_du_corps_amont(cat, besoins)
    sup = val(cfg["structure_rs02_supplement_g"]) / 1000
    fixe = sup * 2 * sum(1 for a in repart.values() if a == "rs02")
    h = cfg["hypothese_v3"]["haut_du_corps"]
    m_haut_sc = h["nombre"] * val(cat["candidats"][h["actionneur"]]["masse_g"]) / 1000 if v3 else 0.0

    def classe(cid, quoi):
        cl, cp = D.classe_catalogue(cat, cid), couples(cat["candidats"][cid])
        prud = cp["blocage"] if cp["blocage"] is not None else cp["nominal"] * kb
        return dict(cl, continu=prud if quoi == "prudent" else cp["nominal"])

    def conf(quoi):
        return {t: classe(repart[t], quoi) for t in D.JAMBE}

    def tient(rc, cf, quoi):
        r = D.ratios(H, rc, cf, besoins, marge)
        return all((x["rms"] is not None and x["rms"] <= 1) if quoi == "rms" else x["pointe"] <= 1
                   for x in r.values())

    cu = ex["charge_utile"]
    rc = D.reference_charge(ref, m_retire, cu["valeur_kg"] + m_haut_sc + fixe)
    rh = D.reference_charge(ref, m_retire, max(cu["sensibilite_kg"]) + m_haut_sc + fixe)
    cp, cn = conf("prudent"), conf("nominal")
    v = {"T1": "PASS" if tient(rc, cp, "rms") else ("UNKNOWN" if tient(rc, cn, "rms") else "FAIL"),
         "T2": "PASS" if tient(rc, cn, "pointe") else "FAIL"}
    if v["T1"] == "PASS" and v["T2"] == "PASS":
        v["T4"] = "PASS" if tient(rh, cp, "rms") and tient(rh, cn, "pointe") else "UNKNOWN"
    else:
        v["T4"] = "FAIL" if "FAIL" in (v["T1"], v["T2"]) else "UNKNOWN"
    masse = D.masse(H, rc, cp, besoins)
    rv = releve(masse, H, an, rel, rel["inclinaison_tibia_deg"]["valeur"])
    v["T5"] = "PASS" if (marge * rv["knee"] <= cp["knee"]["pointe"]
                         and marge * rv["hip_pitch"] <= cp["hip_pitch"]["pointe"]) else "FAIL"
    ev = D.evaluer(rc, cp, besoins, marge)
    bud = yaml.safe_load(D.BUDGET.read_text(encoding="utf-8"))

    def prix_chf(cid):
        c = cat["candidats"][cid]
        pr = c.get("prix_revendeur") or (cat["comparatif_S"].get(cid) or {}).get("prix_revendeur") or c.get("prix")
        return D.chf(pr, bud["taux_de_change"]) if pr and pr.get("valeur") is not None else None

    achats = [(a, 2) for a in repart.values()] + ([(h["actionneur"], h["nombre"])] if v3 else [])
    prix = [(prix_chf(cid), n) for cid, n in achats]
    return dict(H=H, v3=v3, jambes=repart, v=v, masse=masse, H_max=ev["H_max"], limitantes=ev["limitantes"],
                cout=sum(p * n for p, n in prix if p is not None), cout_incomplet=any(p is None for p, _ in prix),
                releve=rv, haut=h if v3 else None)


VERDICTS_BANC = ("S confirmé", "repli à 0,55 m", "famille rouverte")


def verdict_banc(mesures: Path = MESURES, cid: str = "rs00") -> dict:
    """Le critère du § 4 du protocole de banc, écrit AVANT la mesure.

    Sans mesure au blocage : pas de verdict. Avec : la plus faible des
    mesures remplace la valeur publiée ; T1, T2, T4 et T5 sont relancés à
    H_S puis à la hauteur de repli (params/anthropometry.yaml).
    """
    mb = mesures_blocage(cid, mesures)
    if not mb:
        return dict(verdict=None, mesures=[], par_hauteur={})
    an, ex = lire(ANTHRO), lire(EXIGENCES)
    S = an["tailles"]["S"]
    ok = ("PASS", "TESTED")
    par_h = {}
    for H in (S["H_m"], S["H_m_repli"]):
        x = next(y for y in evaluer(H, ex["charge_utile"]["valeur_kg"], mesures)["lignes"] if y["id"] == cid)
        par_h[H] = {k: x["v"][k] for k in ("T1", "T2", "T4", "T5")}
    tient = {H: all(v in ok for v in t.values()) for H, t in par_h.items()}
    verdict = (VERDICTS_BANC[0] if tient[S["H_m"]] else
               VERDICTS_BANC[1] if tient[S["H_m_repli"]] else VERDICTS_BANC[2])
    return dict(verdict=verdict, mesures=mb, retenu=min(m["valeur"] for m in mb), par_hauteur=par_h)


def h_max_charge(r: dict, cid: str, continu: float | None) -> float | None:
    cat, ref = r["cat"], D.reference_charge(r["ref"], r["m_el"] + r["m_haut"], r["charge"])
    cl = D.classe_catalogue(cat, cid)
    if cl["pointe"] is None or cl["masse"] is None:
        return None
    ev = D.evaluer(ref, D.config_homogene(dict(cl, continu=continu)), r["besoins"], r["marge"])
    return ev.get("H_max")


# ─────────────────────────────── document ────────────────────────────────

CODES = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9"]
APPRO = ["A1", "A2", "A3", "A4"]


def grille(r: dict, codes: list[str]) -> list[str]:
    L = ["| Candidat | " + " | ".join(codes) + " |", "| --- | " + " | ".join(":-:" for _ in codes) + " |"]
    for x in r["lignes"]:
        nom = x["nom"] + (" *(réf.)*" if x["reference"] and "référence" not in x["nom"] else "")
        L.append(f"| {nom} | " + " | ".join(x["v"][k] for k in codes) + " |")
    return L


def doc(r: dict, r_rep: dict | None, masses: list, date: str, vb: dict | None = None,
        conf: list | None = None) -> str:
    ex, an, cat = r["ex"], r["an"], r["cat"]
    rel = ex["releve"]
    L = []
    A = L.append
    A("# Choix de l'actionneur de S — faits, approvisionnement, exigences\n")
    A(f"**Engendré** par `.venv/bin/python scripts/choix_actionneurs.py --ecrire`, le {date}. "
      "Ne pas éditer à la main. Aucun score, aucun poids : chaque exigence donne **PASS**, "
      "**FAIL**, **UNKNOWN** (l'information manque) ou **TESTED** (mesuré au banc). Les règles de "
      "verdict sont dans `params/exigences_S.yaml`.\n")
    A("**Décision** (fiches [0067](../decisions/0067-s-jambes-mixtes-rs02-rs00.md) et "
      "[0068](../decisions/0068-s-cheville-sans-roulis.md), Jeremy, 2026-10-02 et 2026-10-04) : famille RobStride, "
      "jambes mixtes (RS02 au roulis et au tangage de hanche et au genou, RS00 ailleurs), 5 axes par jambe, **H_S = "
      f"{f(r['H'])} m visée**. Elles remplacent la 0065 (tout-RS00). La fiche 0069 abandonne la gamme : "
      "cette grille décrit S tel qu'il est au code. Elle vérifie la condition (a) de la 0065, reprise par la 0067.\n")
    A("---\n")
    if conf:
        A("## 0 — Configuration retenue (fiches 0067 et 0068) : RS02 au roulis et au tangage de hanche et au genou, "
          "RS00 au lacet de hanche et à la cheville ; 5 axes par jambe\n")
        ec = D.besoins_ecartes(AM.analyser(AM.SERIE))
        A("Répartition lue dans `params/configuration_S.yaml`. v1 : buste fixe. v3 : HYPOTHÈSE de haut du corps "
          "(masse seulement ; couple des bras non vérifié). Supplément de structure des logements RS02 : "
          "hypothèse, compté dans la masse. "
          + (f"**Besoins écartés** de la marche de référence (fiche 0068) : {', '.join(ec)} ; leur effort "
             "n'est reporté sur aucun autre axe (hypothèse non vérifiée).\n" if ec else "\n"))
        A("| Version | H | Masse | T1 | T2 | T4 | T5 | H_max prudent | Limitante | Actionneurs (CHF HT) |")
        A("| --- | ---: | ---: | :-: | :-: | :-: | :-: | ---: | --- | ---: |")
        for c in conf:
            ver = (f"v3, haut {c['haut']['nombre']} × {c['haut']['actionneur']}" if c["v3"] else "v1, buste fixe")
            A(f"| {ver} | {f(c['H'])} m | {f(c['masse'])} kg | {c['v']['T1']} | {c['v']['T2']} | {c['v']['T4']} | "
              f"{c['v']['T5']} | {f(c['H_max'], 3)} m | {', '.join(c['limitantes'])} | "
              f"{'≥ ' if c['cout_incomplet'] else ''}{c['cout']:.0f} |")
        A("")
    A(f"## 1 — Grille technique à H_S = {f(r['H'])} m, charge utile {f(r['charge'], 1)} kg, marge {f(r['marge'], 1)}\n")
    L.extend(grille(r, CODES))
    A("")
    for k, t in ex["exigences"]["technique"].items():
        A(f"- **{k}** — {t}")
    A(f"\n*k_bas = {f(r['kb'], 3)}*, le plus petit rapport blocage / nominal publié au catalogue : "
      + ", ".join(f"{cid} {f(x, 3)}" for x, cid in r["rapports"]) + ".\n")
    A("## 2 — Masse du robot à H_S, selon la charge utile (RS00 homogène)\n")
    A("| Charge utile | Masse du robot | T1 | T2 | T5 |")
    A("| ---: | ---: | :-: | :-: | :-: |")
    for cu, m, v in masses:
        A(f"| {f(cu, 1)} kg | {f(m, 2)} kg | {v['T1']} | {v['T2']} | {v['T5']} |")
    A(f"\nModèle : `masse(H) = (S0 − m_élec − m_haut) · (H/H0)³ + charge utile + Σ actionneurs`. "
      f"S0 = {f(r['ref']['S0'], 3)} kg (M0 − 12 Dynamixel de jambe) ; m_élec = {f(r['m_el'], 3)} kg, "
      "l'électronique de ToddlerBot comprise dans M0 (`params/exigences_S.yaml`) ; "
      f"m_haut = {f(r['m_haut'], 3)} kg, ses 20 servos du haut du corps, CALCULÉS depuis le modèle amont "
      "(`dimensionnement.masse_haut_du_corps_amont`) et retirés depuis la fiche 0067 : la v1 a un buste "
      "fixe. Tous deux sont retirés de la part mise à l'échelle.\n")
    A("## 3 — Relevé depuis l'accroupi profond (T5)\n")
    A(f"- Posture : {rel['posture']}.")
    A(f"- Tibia incliné de **{rel['inclinaison_tibia_deg']['valeur']}°** vers l'avant ({rel['inclinaison_tibia_deg']['source']}).")
    A(f"- Répartition : {f(rel['repartition_jambes']['valeur'], 1)} par jambe ({rel['repartition_jambes']['source']}).")
    A(f"- Masse portée : {rel['masse_portee']}.")
    A(f"- Longueurs : {rel['longueurs']}.")
    A(f"- Verdict : {rel['verdict']}.\n")
    A("| Candidat | Masse (kg) | Cuisse / tibia (m) | Genou (N·m) | Hanche (N·m) | Marge × max | Pointe | Continu prudent | T5 |")
    A("| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | :-: |")
    for x in r["lignes"]:
        rv = x["releve"]
        if not rv:
            A(f"| {x['nom']} | — | — | — | — | — | — | — | {x['v']['T5']} |")
            continue
        mx = r["marge"] * max(rv["knee"], rv["hip_pitch"])
        A(f"| {x['nom']} | {f(x['dc']['masse'])} | {f(rv['L_c'], 3)} / {f(rv['L_t'], 3)} | {f(rv['knee'])} | "
          f"{f(rv['hip_pitch'])} | {f(mx)} | {f(x['pointe'], 1)} | {f(x['dc'].get('prudent'))} | {x['v']['T5']} |")
    rs = next(x for x in r["lignes"] if x["id"] == "rs00")
    A("\nSensibilité à l'angle du tibia, RS00 : " + " ; ".join(
        f"{a}° → genou {f(releve(rs['dc']['masse'], r['H'], an, rel, a)['knee'])} N·m, hanche "
        f"{f(releve(rs['dc']['masse'], r['H'], an, rel, a)['hip_pitch'])} N·m"
        for a in [rel["inclinaison_tibia_deg"]["sensibilite"][0], rel["inclinaison_tibia_deg"]["valeur"],
                  rel["inclinaison_tibia_deg"]["sensibilite"][1]]) + ".\n")
    if r_rep:
        A(f"## 3 bis — Repli à {f(r_rep['H'])} m (un FAIL du RS00 à T1, T2 ou T5 à {f(r['H'])} m)\n")
        A("Calculé parce que la fiche 0065 le prévoit (condition a). **Rien n'est décidé ici.**\n")
        L.extend(grille(r_rep, CODES))
        A("")
    A("## 4 — Faits techniques\n")
    A("| Candidat | Clé de révision | Nominal (N·m) | Blocage (N·m) | Pointe (N·m) | Masse (g) | "
      "Vitesse à vide (rpm) | Tension / plage (V) | Réduction | Bus | Protection (°C) | Taille max prudente – optimiste (m) |")
    A("| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- | ---: | --- |")
    for x in r["lignes"]:
        c = cat["candidats"][x["id"]]
        cp = couples(c)
        pl = val(c.get("tension_plage_V") or {})
        vit = val(c.get("vitesse_a_vide_rpm") or {})
        if vit is None and val(c.get("vitesse_s_par_60deg") or {}):
            vit = 60 / (6 * val(c["vitesse_s_par_60deg"]))
        hp, ho = h_max_charge(r, x["id"], x["dc"].get("prudent")), h_max_charge(r, x["id"], cp["nominal"])
        A(f"| {x['nom']} | {x['cle']} | {f(cp['nominal'])} | {f(cp['blocage'])} | {f(x['pointe'], 1)} | "
          f"{f(val(c['masse_g']), 0)} | {f(vit, 0)} | {f(val(c['tension_V']), 0)}"
          f"{' (' + '–'.join(f(p_, 1) for p_ in pl) + ')' if pl else ''} | {f(val(c['reduction']), 2)} | "
          f"{c['bus'].split(',')[0].split('(')[0].strip()} | {f(val(c.get('protection_thermique_C') or {}), 0)} | "
          f"{f(hp)} – {f(ho)} |")
    A(f"\nTailles maximales en configuration homogène, avec la charge utile de {f(r['charge'], 1)} kg. "
      "La vitesse est À VIDE ; sous charge, l'actionneur tourne moins vite.\n")
    A("## 5 — Approvisionnement (daté : il vieillit)\n")
    L.extend(grille(r, APPRO))
    A("")
    for k, t in ex["exigences"]["approvisionnement"].items():
        A(f"- **{k}** — {t}")
    A("\n| Candidat | Prix | Vendeur | Relevé le | Revendeur CH / UE | Garantie (mois) |")
    A("| --- | ---: | --- | --- | --- | ---: |")
    for x in r["lignes"]:
        p, d = x["prix"], x["distribution"]
        A(f"| {x['nom']} | {f(p.get('valeur'))} {p.get('devise') or ''} | {p.get('vendeur') or '—'} | "
          f"{p.get('consulte_le') or '—'} | {d.get('suisse') or d.get('ue') or '—'} | {f(x['garantie'], 0)} |")
    A("\n## 6 — Banc : le critère du § 4 du protocole\n")
    A("Écrit AVANT la mesure (`docs/protocole-banc.md`, § 4). Le plus faible des continus au blocage "
      "MESURÉS du RS00 remplace la valeur publiée ; T1, T2, T4 et T5 sont relancés à H_S puis à la "
      "hauteur de repli. Verdict : « S confirmé », « repli à 0,55 m » ou « famille rouverte ». "
      "La valeur publiée reste au catalogue, intacte.\n")
    cp = couples(cat["candidats"]["rs00"])
    if not vb or not vb.get("verdict"):
        A(f"**Aucune mesure au blocage du RS00 dans `params/mesures.yaml` : pas de verdict.** "
          f"Valeur publiée : {f(cp['blocage'], 1)} N·m (PDF RobStride du 2026-09-17, p. 5).\n")
    else:
        A("| Source | Valeur (N·m) | Incertitude | Instrument | Date | Note |")
        A("| --- | ---: | --- | --- | --- | --- |")
        A(f"| publiée (catalogue) | {f(cp['blocage'], 2)} | — | — | — | PDF RobStride 2026-09-17, p. 5 |")
        for m in vb["mesures"]:
            A(f"| mesure `{m['id']}` | {f(m['valeur'], 2)} | ± {f(m.get('incertitude'), 2)} "
              f"({m.get('type_incertitude') or '—'}) | {m.get('instrument') or '—'} | {m.get('date') or '—'} | "
              f"{' '.join(str(m.get('note') or '').split())[:120]} |")
        A(f"\n**Retenu : {f(vb['retenu'], 2)} N·m** (le plus faible).\n")
        A("| Hauteur | T1 | T2 | T4 | T5 |")
        A("| ---: | :-: | :-: | :-: | :-: |")
        for H, t in vb["par_hauteur"].items():
            A(f"| {f(H)} m | {t['T1']} | {t['T2']} | {t['T4']} | {t['T5']} |")
        A(f"\n**Verdict du § 4 : {vb['verdict']}.**\n")
    A("\n## 7 — Ce que ce document ne dit pas\n")
    A("- **Les besoins de couple viennent de la marche de ToddlerBot**, dont plusieurs articulations "
      "touchaient leur borne : ce sont des **minimums**.")
    A("- **La charge utile est une hypothèse** (" + ex["charge_utile"]["statut"] + ").")
    A("- **Le relevé est quasi statique** : il ignore l'accélération et le choc de la chute elle-même.")
    A("- **T7, T8 et A4 lisent du texte** quand le fait n'est pas structuré (règles dans "
      "`params/exigences_S.yaml`). La collecte du 2026-10-01 ne couvre pas les candidats ajoutés au lot H.")
    A("- Les références *(réf.)* sont listées pour comparaison ; elles ne sont pas candidates.")
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ecrire", action="store_true", help="engendre docs/choix-actionneurs.md")
    a = ap.parse_args(argv)
    an = lire(ANTHRO)
    ex = lire(EXIGENCES)
    S = an["tailles"]["S"]
    H, H_rep = S["H_m"], S.get("H_m_repli")
    cu = ex["charge_utile"]
    r = evaluer(H, cu["valeur_kg"])
    rs = next(x for x in r["lignes"] if x["id"] == "rs00")
    masses = []
    for c_ in sorted({cu["sensibilite_kg"][0], cu["valeur_kg"], cu["sensibilite_kg"][1]}):
        rc = evaluer(H, c_)
        x = next(y for y in rc["lignes"] if y["id"] == "rs00")
        masses.append((c_, x["dc"]["masse"], x["v"]))
    echec = any(rs["v"][k] == "FAIL" for k in ("T1", "T2", "T5"))
    r_rep = evaluer(H_rep, cu["valeur_kg"]) if echec and H_rep else None
    print(f"  H_S = {H} m, charge {cu['valeur_kg']} kg, marge {r['marge']}, k_bas {r['kb']:.3f}")
    ec = D.besoins_ecartes(AM.analyser(AM.SERIE))
    if ec:
        print(f"  besoins ÉCARTÉS de la marche de référence (fiche 0068) : {', '.join(ec)} — effort non reporté (hypothèse)")
    for x in r["lignes"]:
        print(f"  {x['nom'][:44]:44s} " + " ".join(f"{k}:{x['v'][k][:4]:4s}" for k in CODES + APPRO))
    for c_, m, v in masses:
        print(f"  RS00, charge {c_} kg : masse {m:.2f} kg — T1 {v['T1']}, T2 {v['T2']}, T5 {v['T5']}")
    if r_rep:
        print(f"  FAIL du RS00 à {H} m : repli calculé à {H_rep} m")
    vb = verdict_banc()
    print(f"  banc, critère du § 4 : {vb['verdict'] or 'aucune mesure au blocage du RS00, pas de verdict'}")
    conf = [evaluer_configuration(h_, v3) for h_ in (H, H_rep) for v3 in (False, True)]
    for c in conf:
        print(f"  configuration retenue (0067, 0068), {'v3' if c['v3'] else 'v1'} à {c['H']} m : masse {c['masse']:.2f} kg, "
              + ", ".join(f"{k} {c['v'][k]}" for k in ("T1", "T2", "T4", "T5"))
              + f", H_max {c['H_max']:.3f} m ({', '.join(c['limitantes'])}), {c['cout']:.0f} CHF HT")
    if a.ecrire:
        DOC.write_text(doc(r, r_rep, masses, datetime.date.today().isoformat(), vb, conf), encoding="utf-8")
        print(f"  -> {DOC.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
