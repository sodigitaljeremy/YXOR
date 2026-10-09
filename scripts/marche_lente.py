#!/usr/bin/env python3
"""Le blocage en vitesse du Lab léger disparaît-il en marchant lentement ? (calcul direct, AUCUNE décision)

    .venv/bin/python scripts/marche_lente.py          # tableaux (repris dans docs/lab-leger-2026-10.md)

Créé le 2026-10-09. Calculs sur les données du dépôt seulement : les trois marches simulées
(exports/simulations, `simulations_marche.charger`), les tables des phases 3a et 3b (`explorateur.besoins` pour les
tâches autres que la marche), les catalogues d'actionneurs. Ni explorateur, ni recherche.

D'OÙ VIENNENT LES BESOINS DE LA MARCHE. Chaque marche simulée a un nombre de Froude Fr = v / √(g·H) ; mise à
l'échelle d'un robot de hauteur H, elle marche à Fr·√(g·H). Il n'existe que trois marches (ToddlerBot, G1, T1) ;
aucune ne va à 0,10, 0,15 ou 0,30 m/s à H = 0,60 m. Deux lectures, sans interpolation :
  · « explorateur » : le MAXIMUM de toutes les marches au moins aussi rapides (règle de `table_besoins`) ; à 0,15 m/s
    il inclut donc le G1 à 0,55 m/s, d'où des valeurs identiques à 0,30 m/s ;
  · « la plus lente au-dessus » : la marche simulée la plus lente qui va au moins aussi vite : une BORNE HAUTE
    (hypothèse écrite : un même robot marchant plus lentement ne demande pas plus), jamais une donnée à cette vitesse.
Statut, strict : à une vitesse sans marche simulée, la donnée est null et le statut INCONNU ; avec la borne, un servo
qui passe « tient (sous la borne) », un servo qui échoue reste INCONNU (le vrai besoin peut être plus bas). Aux
vitesses des marches simulées elles-mêmes, le verdict est définitif.

Règle d'actionneur : une donnée critique manquante (vitesse, couple continu) donne INCONNU, jamais « tient ».
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
G = 9.80665
H_LEGER, M_LEGER = 0.60, 3.45        # non-cote: la configuration du rapport lab-leger (0,60 m, 3,45 kg)
VITESSES = (0.10, 0.15, 0.30)        # non-cote: vitesses de marche étudiées (prompt du 2026-10-09)
MARGES = (1.5, 1.0)                  # non-cote: fiche 0051 ; repère des robots qui marchent
JAMBE = ("hip_pitch", "hip_roll", "hip_yaw", "knee", "ankle_pitch")
EDULITE_CONTINU = 1.8                # non-cote: N·m nominal, consigne du prompt du 2026-10-09 (déjà au catalogue)


def lire(nom):
    import marche_composants as MC
    return MC.lire(nom)


def marches() -> list[dict]:
    import simulations_marche as SM
    m, _, _ = SM.charger()
    return sorted(({"nom": k, "Fr": e["Fr"], "profil": e["profil"]} for k, e in m.items()), key=lambda x: x["Fr"])


def vitesse_equivalente(sim, H=H_LEGER) -> float:
    return sim["Fr"] * math.sqrt(G * H)


def besoins_sim(sim, H=H_LEGER, M=M_LEGER) -> dict:
    """Besoins d'UNE marche simulée mise à l'échelle (H, M) : pointe et RMS × g·H·M, ω × √(g/H)."""
    out = {}
    for ty, p in sim["profil"].items():
        if ty in JAMBE:
            out[ty] = dict(pk=p["pointe"] * G * H * M, c=p["rms"] * G * H * M, w=p["omega"] * math.sqrt(G / H))
    return out


def couvrantes(v, H=H_LEGER) -> list[dict]:
    return [s for s in marches() if vitesse_equivalente(s, H) >= v - 1e-9]


def besoins_marche(v, mode, H=H_LEGER, M=M_LEGER) -> dict | None:
    """'explorateur' : maximum des marches au moins aussi rapides ; 'plus_lente' : la plus lente d'entre elles ;
    'donnee' : une marche simulée À cette vitesse (±1 %), sinon None (null, INCONNU). Rend {axe: besoin} + 'source'."""
    cs = couvrantes(v, H)
    if mode == "donnee":
        cs = [s for s in marches() if abs(vitesse_equivalente(s, H) - v) <= 0.01 * v]
        if not cs:
            return None
    if not cs:
        return None
    if mode == "plus_lente":
        cs = cs[:1]
    out = {}
    for s in cs:
        for a, b in besoins_sim(s, H, M).items():
            o = out.setdefault(a, dict(pk=0.0, c=0.0, w=0.0))
            for k in ("pk", "c", "w"):
                o[k] = max(o[k], b[k])
    out["source"] = ", ".join(f"{s['nom']} ({vitesse_equivalente(s, H):.3f} m/s)" for s in cs)
    return out


def besoins_autres(H=H_LEGER, M=M_LEGER) -> dict:
    """Les autres tâches du profil lab_leger (relevé, gestes, tête…), tables des phases 3a et 3b."""
    import exigences_physiques as EP
    import explorateur as X
    import simulations_marche as SM
    cap, an, lignes = EP.tout()
    m, r, _ = SM.charger()
    T = X.table_besoins(lignes, m, r, cap)
    prof = {t: v for t, v in cap["profils"]["lab_leger"]["taches"].items() if t != "marche_sol_plat"}
    return {a: v for a, v in X.besoins(T, H, prof, M).items() if a in JAMBE}


def total(marche: dict | None, autres: dict) -> dict | None:
    """Le maximum de la marche et des autres tâches, par axe, avec la tâche qui domine."""
    if marche is None:
        return None
    out = {}
    for a in JAMBE:
        m, o = marche.get(a, dict(pk=0, c=0, w=0)), autres.get(a, dict(pk=0, c=0, w=0))
        out[a] = {k: max(m[k], o[k]) for k in ("pk", "c", "w")}
        out[a]["domine"] = "marche" if m["pk"] >= o["pk"] else "autres tâches"
    return out


# ─────────────────────────────── actionneurs ────────────────────────────
def actionneurs(corrige=True) -> list[dict]:
    """STS3215 (12 V), STS3250 (vitesse : catalogue, null ; corrigée : fiche candidate), le plus fort de chaque autre
    famille de servos_bus.yaml (vitesse publiée), RS05 et EduLite05 (12S coupé à 3,0 V : vitesse × 36/48)."""
    import explorateur as X
    import servos_bus as SB
    par, _, _ = X.catalogue()
    cand = lire("actionneurs.yaml")["candidats"]
    out = []
    for a in par["feetech"]:
        if a["id"] in ("sts3215_c018", "sts3250"):
            w = a["vitesse"]
            s60 = ((cand.get(a["id"]) or {}).get("vitesse_s_par_60deg") or {}).get("valeur")
            if w is None and s60 and corrige:
                w = (math.pi / 3) / s60
            out.append(dict(id=a["id"], famille="Feetech", pk=a["pointe"], c=a["continu"], w=w, tension="12 V"))
    for fam in dict.fromkeys(m["famille"] for m in SB.modeles()):
        if fam in ("Feetech", "Dynamixel"):
            continue
        xs = [m for m in SB.modeles() if m["famille"] == fam and m["vitesse"] and m["blocage"]]
        if xs:
            b = max(xs, key=lambda m: m["blocage"])
            out.append(dict(id=b["id"], famille=fam, pk=b["blocage"], c=b["continu"], w=b["vitesse"],
                            tension=f"{b['tension']} V" if b["tension"] else "?"))
    import systeme_electrique as SE
    var = SE.variante(12, coupure=3.0)
    for a in par["robstride"]:
        if a["id"] in ("rs05", "edulite05"):
            c = EDULITE_CONTINU if a["id"] == "edulite05" else a["continu"]
            out.append(dict(id=a["id"], famille="RobStride", pk=a["pointe"], c=c,
                            w=a["vitesse"] * SE.facteur_vitesse(a["v_ref"], var), tension="12S, 3,0 V/cellule"))
    return out


def verdict(act: dict, need: dict, marge: float) -> dict:
    """Ratios (couple de pointe, continu, vitesse) et statut : « ne tient pas » si un critère CONNU échoue ;
    INCONNU si une donnée critique manque (vitesse, couple continu) ; sinon « tient »."""
    r_pk = act["pk"] / need["pk"] if need["pk"] > 0 else None
    r_c = (act["c"] / need["c"] if need["c"] > 0 else None) if act["c"] is not None else None
    r_w = (act["w"] / need["w"] if need["w"] > 0 else None) if act["w"] is not None else None
    echec = (r_pk is not None and r_pk < marge) or (r_c is not None and r_c < marge) or (r_w is not None and r_w < 1.0)
    manque = (act["c"] is None and need["c"] > 0) or (act["w"] is None and need["w"] > 0)
    statut = "ne tient pas" if echec else ("INCONNU" if manque else "tient")
    return dict(pk=r_pk, c=r_c, w=r_w, statut=statut)


def verdict_robot(act, besoins, marge, borne: bool) -> str:
    """Tous les axes de jambe avec le même actionneur. Avec une BORNE (pas une donnée à cette vitesse), un échec
    reste INCONNU."""
    if besoins is None:
        return "INCONNU (aucune donnée)"
    st = [verdict(act, besoins[a], marge)["statut"] for a in JAMBE]
    if "ne tient pas" in st:
        return "INCONNU (au-dessus de la borne)" if borne else "ne tient pas"
    if "INCONNU" in st:
        return "INCONNU (donnée d'actionneur manquante)"
    return "tient (sous la borne)" if borne else "tient"


def f1(x, n=1):
    return "—" if x is None else f"{x:,.{n}f}".replace(",", " ").replace(".", ",")


def etude() -> dict:
    autres = besoins_autres()
    acts = actionneurs()
    out = dict(autres=autres, acts=acts, vitesses={}, sims={})
    for v in VITESSES:
        out["vitesses"][v] = {mode: total(besoins_marche(v, mode), autres) for mode in ("explorateur", "plus_lente", "donnee")}
        out["vitesses"][v]["source"] = {mode: (besoins_marche(v, mode) or {}).get("source")
                                        for mode in ("explorateur", "plus_lente")}
    for s in marches():
        ve = vitesse_equivalente(s)
        out["sims"][s["nom"]] = dict(v=ve, besoins=total(besoins_marche(ve, "donnee"), autres))
    return out


def sections(e) -> list[str]:
    """Les sections du rapport docs/lab-leger-2026-10.md."""
    L = [f"## Marcher lentement : les besoins par articulation (H = {f1(H_LEGER, 2)} m, {f1(M_LEGER, 2)} kg)", "",
         "Les trois marches simulées, ramenées à 0,60 m : " + " ; ".join(
             f"{n} à {f1(x['v'], 3)} m/s" for n, x in e["sims"].items())
         + ". **Aucune ne va à 0,10, 0,15 ou 0,30 m/s** : à ces vitesses, la donnée est null et le statut INCONNU. "
           "Deux lectures sont montrées, sans interpolation : la règle de l'explorateur (le maximum des marches au moins "
           "aussi rapides) et la marche la plus lente au moins aussi rapide (une borne haute). Les autres tâches du profil "
           "(relevé, gestes, tête) s'ajoutent (maximum par axe).", "",
         "| Vitesse (m/s) | Lecture | Source | Genou : pointe (N·m), vitesse (rad/s) | Cheville : pointe, vitesse | "
         "Tangage de hanche : pointe, vitesse |", "| ---: | --- | --- | --- | --- | --- |"]
    for v, x in e["vitesses"].items():
        L.append(f"| {f1(v, 2)} | donnée à cette vitesse | aucune | null (INCONNU) | null (INCONNU) | null (INCONNU) |")
        for mode, lib in (("explorateur", "règle de l'explorateur"), ("plus_lente", "la plus lente au-dessus (borne)")):
            b = x[mode]
            L.append(f"| {f1(v, 2)} | {lib} | {x['source'][mode]} | " + " | ".join(
                f"{f1(b[a]['pk'], 2)}, {f1(b[a]['w'])}" for a in ("knee", "ankle_pitch", "hip_pitch")) + " |")
    b15, b30 = e["vitesses"][0.15]["explorateur"], e["vitesses"][0.30]["explorateur"]
    meme = all(abs(b15[a]["w"] - b30[a]["w"]) < 1e-9 for a in JAMBE)
    L += ["", f"**0,15 m/s reprend-elle un niveau voisin ?** Avec la règle de l'explorateur, "
          + ("OUI pour les vitesses : les vitesses requises sont identiques à celles de 0,30 m/s, parce que le maximum "
             "inclut le G1 et le T1, qui marchent bien plus vite (0,55 et 0,69 m/s à cette taille) ; seuls des couples "
             "diffèrent (ceux de ToddlerBot, plus forts à la cheville)." if meme else "non.")
          + " La borne « la plus lente au-dessus » donne, elle, les besoins de ToddlerBot (0,196 m/s) à 0,10 et 0,15 m/s.", ""]
    for marge in MARGES:
        L += [f"### Verdict par actionneur, même actionneur sur les cinq axes de jambe (marge {f1(marge)} sur le couple)", "",
              "| Actionneur | " + " | ".join(f"{f1(v, 2)} m/s (borne)" for v in e["vitesses"]) + " | "
              + " | ".join(f"{n} ({f1(x['v'], 3)} m/s, donnée)" for n, x in e["sims"].items()) + " |",
              "| --- | " + " | ".join("---" for _ in list(e["vitesses"]) + list(e["sims"])) + " |"]
        for a in e["acts"]:
            cells = [verdict_robot(a, x["plus_lente"], marge, True) for x in e["vitesses"].values()]
            cells += [verdict_robot(a, x["besoins"], marge, False) for x in e["sims"].values()]
            L.append(f"| {a['id']} ({a['famille']}, {a['tension']}) | " + " | ".join(cells) + " |")
        L.append("")
    for v, x in e["vitesses"].items():
        b = x["plus_lente"]
        L += [f"### Marges à {f1(v, 2)} m/s (borne : {x['source']['plus_lente']}) : couple de pointe / couple continu / vitesse", "",
              "Chaque case : rapport « publié ÷ requis » ; le couple doit atteindre la marge (1,5 ou 1,0), la vitesse 1,0. "
              "« — » : donnée non publiée (INCONNU).", "",
              "| Axe | Requis : pointe, continu (N·m), vitesse (rad/s) | " + " | ".join(a["id"] for a in e["acts"]) + " |",
              "| --- | --- | " + " | ".join("---" for _ in e["acts"]) + " |"]
        for ax in JAMBE:
            n = b[ax]
            cells = []
            for a in e["acts"]:
                r = verdict(a, n, 1.0)
                cells.append(f"{f1(r['pk'], 2)} / {f1(r['c'], 2)} / {f1(r['w'], 2)}")
            L.append(f"| {ax} | {f1(n['pk'], 2)}, {f1(n['c'], 2)}, {f1(n['w'])} ({n['domine']}) | " + " | ".join(cells) + " |")
        L.append("")
    return L


def main() -> int:
    print("\n".join(sections(etude())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
