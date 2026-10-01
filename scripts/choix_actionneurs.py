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
  params/mesures.yaml         mesures de banc (TESTED)
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

def verdict_couple(cat, cid, H, ref_c, besoins, marge, kb):
    """T1 et T2, à la hauteur H, avec la référence chargée ref_c."""
    cl = D.classe_catalogue(cat, cid)
    cp = couples(cat["candidats"][cid])
    if cl["pointe"] is None or cl["masse"] is None:
        return dict(T1="UNKNOWN", T2="UNKNOWN", masse=None, detail="pointe ou masse inconnue")
    prud = cp["blocage"] if cp["blocage"] is not None else (cp["nominal"] * kb if cp["nominal"] else None)

    def tient(continu, quoi):
        conf = D.config_homogene(dict(cl, continu=continu))
        r = D.ratios(H, ref_c, conf, besoins, marge)
        if quoi == "rms":
            return all(x["rms"] is not None and x["rms"] <= 1 for x in r.values())
        return all(x["pointe"] <= 1 for x in r.values())

    if cp["nominal"] is None:
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
                base="blocage publié" if cp["blocage"] is not None else f"nominal × k_bas ({f(kb, 3)})",
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


def evaluer(H: float, charge: float) -> dict:
    cat = D.charger_catalogue()
    ex, an = lire(EXIGENCES), lire(ANTHRO)
    mes = (lire(MESURES) or {}).get("mesures") or {}
    analyse = AM.analyser(AM.SERIE)
    besoins = D.besoins_p1(analyse)
    ref = D.reference(cat, analyse)
    m_el = ex["electronique_toddlerbot"]["masse_kg"]["valeur"]
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
        ref_c = D.reference_charge(ref, m_el, charge)
        dc = verdict_couple(cat, cid, H, ref_c, besoins, marge, kb)
        v["T1"], v["T2"] = dc["T1"], dc["T2"]
        if dc.get("vitesse_publiee"):
            v["T3"] = "PASS" if dc["h_min_vit"] <= H else "FAIL"
        else:
            v["T3"] = "UNKNOWN"
        dh = verdict_couple(cat, cid, H, D.reference_charge(ref, m_el, haut), besoins, marge, kb)
        if "FAIL" in (v["T1"], v["T2"]) or "UNKNOWN" in (v["T1"], v["T2"]):
            v["T4"] = "FAIL" if "FAIL" in (v["T1"], v["T2"]) else "UNKNOWN"
        else:
            v["T4"] = "PASS" if (dh["T1"], dh["T2"]) == ("PASS", "PASS") else "UNKNOWN"
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
        # TESTED : une mesure de banc pour ce candidat
        if any((m or {}).get("actionneur") == cid for m in mes.values()):
            v["T1"] = "TESTED"
        lignes.append(dict(id=cid, nom=c["nom"], reference=bool(c.get("reference")), v=v, dc=dc,
                           releve=rv, pointe=pointe, prix=pr, distribution=d, garantie=gm,
                           cle=D.cle_revision(c), familles=[fid for fid, _ in fams]))
    return dict(H=H, charge=charge, lignes=lignes, kb=kb, rapports=rapports, marge=marge, m_el=m_el,
                ref=ref, cat=cat, ex=ex, an=an, besoins=besoins)


def h_max_charge(r: dict, cid: str, continu: float | None) -> float | None:
    cat, ref = r["cat"], D.reference_charge(r["ref"], r["m_el"], r["charge"])
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


def doc(r: dict, r_rep: dict | None, masses: list, date: str) -> str:
    ex, an, cat = r["ex"], r["an"], r["cat"]
    rel = ex["releve"]
    L = []
    A = L.append
    A("# Choix de l'actionneur de S — faits, approvisionnement, exigences\n")
    A(f"**Engendré** par `.venv/bin/python scripts/choix_actionneurs.py --ecrire`, le {date}. "
      "Ne pas éditer à la main. Aucun score, aucun poids : chaque exigence donne **PASS**, "
      "**FAIL**, **UNKNOWN** (l'information manque) ou **TESTED** (mesuré au banc). Les règles de "
      "verdict sont dans `params/exigences_S.yaml`.\n")
    A("**Décision** (fiche [0065](../decisions/0065-s-robstride-rs00.md), Jeremy, 2026-10-01) : "
      "famille RobStride, RS00 sur les 12 articulations de jambe, **H_S = "
      f"{f(r['H'])} m visée**. Cette grille en vérifie la condition (a).\n")
    A("---\n")
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
    A(f"\nModèle : `masse(H) = (S0 − m_élec) · (H/H0)³ + charge utile + Σ actionneurs`. "
      f"S0 = {f(r['ref']['S0'], 3)} kg (M0 − 12 Dynamixel de jambe) ; m_élec = {f(r['m_el'], 3)} kg, "
      "l'électronique de ToddlerBot comprise dans M0, retirée de la part mise à l'échelle "
      "(source : `params/exigences_S.yaml`, `electronique_toddlerbot`).\n")
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
    A("\n## 6 — Ce que ce document ne dit pas\n")
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
    for x in r["lignes"]:
        print(f"  {x['nom'][:44]:44s} " + " ".join(f"{k}:{x['v'][k][:4]:4s}" for k in CODES + APPRO))
    for c_, m, v in masses:
        print(f"  RS00, charge {c_} kg : masse {m:.2f} kg — T1 {v['T1']}, T2 {v['T2']}, T5 {v['T5']}")
    if r_rep:
        print(f"  FAIL du RS00 à {H} m : repli calculé à {H_rep} m")
    if a.ecrire:
        DOC.write_text(doc(r, r_rep, masses, datetime.date.today().isoformat()), encoding="utf-8")
        print(f"  -> {DOC.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
