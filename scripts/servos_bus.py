#!/usr/bin/env python3
"""Familles de petits servos à bus : comparaison, et le Lab léger tiendrait-il avec l'une d'elles ? (AUCUNE décision)

    .venv/bin/python scripts/servos_bus.py            # tableaux
    .venv/bin/python scripts/servos_bus.py --ecrire   # docs/servos-bus-2026-10.md

Créé le 2026-10-09. Question de Jeremy (2026-10-08, ses mots) : « Pourquoi choisir du Feetech ? Car ce sont les
actionneurs les moins chers du marché ? »

Données : params/servos_bus.yaml (Hiwonder, Waveshare, Kondo, HerkuleX, Lynxmotion, Futaba, UBTECH ; versé le
2026-10-09) et le catalogue de l'explorateur pour Feetech et Dynamixel (params/actionneurs.yaml). Couple : celui
AU BLOCAGE (seul publié partout) ; vitesse à vide à la tension de la fiche ; prix en CHF HT (taux BCE du budget ;
une devise sans taux n'est pas convertie, et c'est dit).

Point 3 (calcul DIRECT, sans l'explorateur) : les besoins de la marche à 0,3 m/s du Lab léger, à la configuration
de docs/lab-leger-2026-10.md (H = 0,60 m, 3,4 kg ; tables des phases 3a et 3b, `explorateur.besoins`), × la marge
1,5 (fiche 0051) pour le couple ; vitesse de pointe sans marge. Un servo « tient » un axe si son couple au blocage
≥ 1,5 × pointe, sa vitesse ≥ la vitesse requise, et son couple continu ≥ 1,5 × continu QUAND il est publié.
La masse du robot ne change pas avec la famille (approximation : dite).
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
DOC = REPO / "docs" / "servos-bus-2026-10.md"
H_LEGER, M_LEGER = 0.60, 3.45        # non-cote: la configuration du rapport lab-leger (Feetech, carton, 0,60 m, 3,4 kg)
JAMBE = ("hip_yaw", "hip_roll", "hip_pitch", "knee", "ankle_pitch")


def lire(nom):
    import marche_composants as MC
    return MC.lire(nom)


def f1(x, n=1):
    return "—" if x is None else f"{x:,.{n}f}".replace(",", " ").replace(".", ",")


def modeles() -> list[dict]:
    """Tous les modèles, au même format : id, famille, blocage (N·m), continu (N·m ou None), vitesse (rad/s, à la
    tension de la fiche), tension, masse (kg), prix (CHF HT ou None), prix_brut (texte)."""
    import marche_composants as MC
    import explorateur as X
    taux = lire("budget.yaml")["taux_de_change"]
    out = []
    for m in lire("servos_bus.yaml")["modeles"]:
        cb = m.get("couple_blocage") or {}
        cc = m.get("couple_continu") or {}
        v = m.get("vitesse_vide") or {}
        w = (math.pi / 3) / v["s_60deg"] if v.get("s_60deg") else (v["rpm"] * 2 * math.pi / 60 if v.get("rpm") else None)
        p = m.get("prix") or {}
        pv = p.get("valeur_ht") if p.get("valeur_ht") is not None else p.get("valeur")
        prix = MC.chf(dict(valeur=pv, devise=p.get("devise"), tva_incluse=False if p.get("valeur_ht") is not None
                           else p.get("tva_incluse")), taux) if pv is not None else None
        out.append(dict(id=m["modele"], famille=m["famille"], blocage=cb.get("N_m"), continu=cc.get("N_m"),
                        vitesse=w, tension=v.get("tension_V") or cb.get("tension_V"), masse=(m.get("masse_g") or 0) / 1000
                        or None, prix=prix, prix_brut=f"{pv} {p.get('devise')}" if pv is not None else None))
    par, _, _ = X.catalogue()
    cand = lire("actionneurs.yaml")["candidats"]
    for fam in ("feetech", "dynamixel"):
        for a in par[fam]:
            w = a["vitesse"]
            s60 = ((cand.get(a["id"]) or {}).get("vitesse_s_par_60deg") or {}).get("valeur")
            if w is None and s60:                      # STS3250 : fiche candidate (page web sans copie), comme kit.py
                w = (math.pi / 3) / s60
            out.append(dict(id=a["id"], famille=fam.capitalize(), blocage=a["pointe"], continu=a["continu"],
                            vitesse=w, tension=a["v_ref"], masse=a["masse"], prix=a["prix"], prix_brut=None))
    return out


def familles(ms) -> dict:
    """Par famille : le meilleur couple par gramme et par franc (au blocage), le plus fort, le plus rapide, la part de
    modèles dont le couple continu est publié, les retours de fiabilité et les robots qui marchent."""
    info = {f["famille"]: f for f in (lire("servos_bus.yaml").get("familles") or [])}
    out = {}
    for fam in dict.fromkeys(m["famille"] for m in ms):
        xs = [m for m in ms if m["famille"] == fam]
        pg = [m["blocage"] / (m["masse"] * 1000) for m in xs if m["blocage"] and m["masse"]]
        pf = [m["blocage"] / m["prix"] for m in xs if m["blocage"] and m["prix"]]
        fi = info.get(fam, {})
        out[fam] = dict(n=len(xs), Nm_par_g=max(pg) if pg else None, Nm_par_CHF=max(pf) if pf else None,
                        plus_fort=max((m["blocage"] or 0) for m in xs), plus_rapide=max((m["vitesse"] or 0) for m in xs),
                        prix_min=min((m["prix"] for m in xs if m["prix"]), default=None),
                        continu_publie=sum(1 for m in xs if m["continu"]), sans_prix=sum(1 for m in xs if m["prix"] is None),
                        fiabilite=len(fi.get("fiabilite") or []), robots=[r.get("nom") for r in (fi.get("robots") or [])])
    return out


def besoins_leger() -> dict:
    """Besoins par axe de jambe, à (H_LEGER, M_LEGER), profil lab_leger (marche 0,3 m/s) : calcul direct sur les tables."""
    import exigences_physiques as EP
    import explorateur as X
    import simulations_marche as SM
    cap, an, lignes = EP.tout()
    m, r, _ = SM.charger()
    T = X.table_besoins(lignes, m, r, cap)
    return {a: v for a, v in X.besoins(T, H_LEGER, cap["profils"]["lab_leger"]["taches"], M_LEGER).items() if a in JAMBE}


def tient(m, need, marge) -> dict:
    ok_c = m["blocage"] is not None and m["blocage"] >= marge * need["pk"]
    ok_v = m["vitesse"] is not None and m["vitesse"] >= need["w"]
    ok_cc = None if m["continu"] is None else m["continu"] >= marge * need["c"]
    return dict(couple=ok_c, vitesse=ok_v, continu=ok_cc, tout=ok_c and ok_v and ok_cc is not False)


def point3(ms, bes, marge) -> dict:
    """Par famille et par axe : un modèle qui tient ? Sinon ce qui manque (couple ou vitesse)."""
    out = {}
    for fam in dict.fromkeys(m["famille"] for m in ms):
        xs = [m for m in ms if m["famille"] == fam]
        par_axe = {}
        for a, need in bes.items():
            ok = [m for m in xs if tient(m, need, marge)["tout"]]
            if ok:
                par_axe[a] = ("oui", min(ok, key=lambda m: m["masse"] or 9)["id"])
            else:
                fort = [m for m in xs if tient(m, need, marge)["couple"]]
                vite = [m for m in xs if tient(m, need, marge)["vitesse"]]
                par_axe[a] = ("non", "ni couple ni vitesse" if not fort and not vite else
                              ("vitesse" if fort and not any(tient(m, need, marge)["vitesse"] for m in fort) else "couple"))
        out[fam] = dict(axes=par_axe, tient=all(v[0] == "oui" for v in par_axe.values()))
    return out


def rapport(ms, fams, bes, p3) -> str:
    L = ["# Les familles de petits servos à bus (2026-10)", "",
         "**Engendré** par `.venv/bin/python scripts/servos_bus.py --ecrire`. **Étude, AUCUNE décision, aucun achat.** "
         "Question de Jeremy (2026-10-08) : « Pourquoi choisir du Feetech ? Car ce sont les actionneurs les moins chers "
         "du marché ? » Méthode et limites : en tête de `scripts/servos_bus.py`.", "",
         "## Par famille", "",
         "Couple : AU BLOCAGE (le seul publié partout) ; vitesse à vide à la tension de la fiche ; prix en CHF HT. "
         "« Continu publié » : nombre de modèles dont le fabricant publie un couple continu ou nominal.", "",
         "| Famille | Modèles | N·m par 100 g (meilleur) | N·m par 10 CHF (meilleur) | Le plus fort (N·m) | Le plus rapide (rad/s) | "
         "Prix le plus bas (CHF) | Continu publié | Sans prix CHF | Retours de fiabilité | Robots qui marchent (relevés) |",
         "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |"]
    for fam, x in fams.items():
        L.append(f"| {fam} | {x['n']} | {f1(x['Nm_par_g'] and 100 * x['Nm_par_g'], 2)} | "
                 f"{f1(x['Nm_par_CHF'] and 10 * x['Nm_par_CHF'], 2)} | {f1(x['plus_fort'], 2)} | {f1(x['plus_rapide'])} | "
                 f"{f1(x['prix_min'], 0)} | {x['continu_publie']}/{x['n']} | {x['sans_prix']} | {x['fiabilite'] or '—'} | "
                 f"{', '.join(x['robots']) or '—'} |")
    L += ["", "Retours de fiabilité et robots : relevés par l'agent (`params/servos_bus.yaml`, `familles`) pour les "
          "familles nouvelles ; pour Feetech et Dynamixel, non relevés dans ce lot (« — » ne veut pas dire « aucun »).", "",
          f"## Le Lab léger tiendrait-il avec une autre famille ? (marge 1,5, H = {f1(H_LEGER, 2)} m, {f1(M_LEGER, 2)} kg)", "",
          "| Axe | Pointe requise × 1,5 (N·m) | Continu requis × 1,5 (N·m) | Vitesse requise (rad/s) |", "| --- | ---: | ---: | ---: |"]
    for a, n in bes.items():
        L.append(f"| {a} | {f1(1.5 * n['pk'], 2)} | {f1(1.5 * n['c'], 2)} | {f1(n['w'])} |")
    L += ["", "| Famille | " + " | ".join(bes) + " | Tient tout ? |", "| --- | " + " | ".join("---" for _ in bes) + " | --- |"]
    for fam, x in p3.items():
        L.append(f"| {fam} | " + " | ".join(f"{v[0]} ({v[1]})" for v in x["axes"].values())
                 + f" | **{'oui' if x['tient'] else 'non'}** |")
    L += ["", "« non (vitesse) » : des modèles ont le couple, aucun d'eux la vitesse ; « non (couple) » : le couple manque.", ""]
    p1 = point3(ms, bes, 1.0)
    L += ["## Et à la marge 1,0 (repère : celle d'un robot qui marche déjà)", "",
          "Familles qui tiendraient tous les axes de jambe : **" + (", ".join(f for f, x in p1.items() if x["tient"]) or "aucune")
          + "**. Feetech : " + ", ".join(f"{a} {v[0]} ({v[1]})" for a, v in p1["Feetech"]["axes"].items()) + ".", "",
          "**Correction de docs/lab-leger-2026-10.md** (non régénéré : pas de relance de l'explorateur dans ce lot). Son "
          "seul résultat positif, « Feetech en carton tient à la marge 1,0 », reposait sur la vitesse INCONNUE du STS3250 "
          "dans le catalogue de l'explorateur (une donnée manquante ne fait pas échouer un choix). Avec la vitesse de sa "
          "fiche candidate (0,133 s/60°, soit 7,9 rad/s à 12 V, `params/actionneurs.yaml`), le genou (14 rad/s) et la "
          "cheville (18 rad/s) ne tiennent pas : ce résultat ne vaut pas.", ""]
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ecrire", action="store_true")
    a = ap.parse_args(argv)
    ms = modeles()
    fams = familles(ms)
    bes = besoins_leger()
    p3 = point3(ms, bes, 1.5)
    txt = rapport(ms, fams, bes, p3)
    print(txt)
    if a.ecrire:
        DOC.write_text(txt, encoding="utf-8")
        print(f"  -> {DOC.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
