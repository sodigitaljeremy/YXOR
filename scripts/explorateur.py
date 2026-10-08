#!/usr/bin/env python3
"""Explorateur de solutions, appliqué à YXOR Lab (phase 4a, fiche 0069).

    .venv/bin/python scripts/explorateur.py            # résumé
    .venv/bin/python scripts/explorateur.py --ecrire   # docs/explorateur-lab-2026-10.md + .svg

Créé le 2026-10-07. ÉTUDE, aucune décision d'architecture.

UNE SOLUTION = (ensemble d'axes, H, famille du corps, famille des petits axes,
profil de capacités). Pour chacune :

  1. besoin par axe = le MAXIMUM des tâches du profil (couple de pointe, couple
     continu, vitesse), à la vraie masse M de la solution, depuis les tables
     a·M + b des phases 3a (exigences_physiques) et 3b (simulations_marche) :
     rien n'est recalculé par profil ; `verifier_maximum` le recontrôle ;
  2. actionneur par axe = le plus PETIT (masse) de la famille qui passe, à la
     marge de la fiche 0051 ; la masse dépend du choix et le choix de la
     masse : point fixe ;
  3. ROBUSTESSE (loi de masse DÉCIDÉE par Jeremy le 2026-10-07, params/
     lois_masse.yaml) : le choix doit tenir au b bas, central ET haut, et avec
     la structure centrale (évidée 50 % + 2 mm) ET haute (pleine 3 mm) : six
     cas ; H³ est rapporté comme borne pessimiste, sans filtrer ;
  4. statut : faisable / infaisable (contraintes violées, listées) / INCONNU
     (données manquantes, listées comme mesures à faire). Une donnée absente
     n'est JAMAIS estimée : elle rend la solution INCONNUE.

Front de Pareto (tri maison, sans dépendance : réponse de Jeremy du
2026-10-07, « Non, Pareto maison ») sur coût, masse, énergie de chute, nombre
de capacités tenues et nombre de capacités VOULUES couvertes, parmi les
solutions faisables.

PROFIL CIBLE : les capacités voulues, `profils` de params/capacites.yaml (`lab`,
DÉCIDÉ par Jeremy le 2026-10-07, par défaut ; `final` avec --profil final). Un ensemble sans les axes d'une capacité voulue est marqué
« ne couvre pas » (la capacité est listée) au lieu d'être comparé à égalité ;
une capacité voulue mais non calculée reste INCONNUE, listée.

Révisé le 2026-10-07 après-midi (phase 4a bis) : place et structure par les
études reconstruites (scripts/taille_minimale.py, scripts/structure_plaques.py) ;
profil cible ; H de 0,50 à 0,90 m. Puis (phase 4a ter) : profil lab décidé ;
couples, masse et centre de gravité à la HAUTEUR RÉELLE, par itération.

HYPOTHÈSES, toutes PROPOSÉES par Claude et écrites ici (aucune cachée) :
  · ENSEMBLES : 26 = squelette v3 ; 27 et 29 = ceux calculés le 2026-10-04
    (taille_minimale.ENSEMBLES_0410) ; 25 n'a JAMAIS été calculé (le prompt du
    2026-10-04 le citait seulement) : reconstruit, le 26 sans roulis de taille ;
  · PLACE : taille minimale géométrique (scripts/taille_minimale.py), lecture
    AVEC ÉCARTS : la hauteur réelle vaut H + dépassements des chaînes
    verticales ; la lecture ANSUR stricte est rapportée (tient / ne tient pas).
    couples, masse et centre de gravité à la hauteur réelle (itération) ;
  · STRUCTURE : segment par segment (scripts/structure_plaques.py), à H_S,
    selon l'ensemble, puis × (H / H_S)^b ;
  · RÉGIME : les tâches tenues (charge, saisie, poussée, buste, tête) se
    comparent au couple CONTINU ; les gestes brefs (saut, relevé, gestes) au
    couple de POINTE ; la marche aux deux (REGIME) ;
  · un axe absent de l'ensemble est RIGIDE : la structure reprend son couple ;
  · énergie de chute = M·g·h, h = hauteur de hanche ANSUR × hauteur RÉELLE ;
  · coût = Σ prix des actionneurs seulement (structure non chiffrée) ;
  · la marche est toujours dans le profil (niveau le plus bas au moins) : un
    bipède qui ne marche pas n'est pas une solution.
"""
from __future__ import annotations

import argparse
import itertools
import math
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import exigences_physiques as EP  # noqa: E402

DOC = REPO / "docs" / "explorateur-lab-2026-10.md"
SVG = REPO / "docs" / "explorateur-lab-2026-10.svg"
G = 9.80665                                    # non-cote: pesanteur normale (m/s²)
H_LAB = [h for h in EP.HS if 0.50 - 1e-9 <= h <= 0.90 + 1e-9]   # non-cote: plage du prompt (m), 4a bis
STRUCT_CAS = {"central": "évidée 50 % + 2 mm", "haute": "pleine 3 mm"}     # prompt de la phase 4a bis
BANDE = ("bas", "central", "haut")

# ─────────────────────────────── ensembles ──────────────────────────────
JAMBE5 = ["hip_yaw", "hip_roll", "hip_pitch", "knee", "ankle_pitch"]
BRAS5 = ["shoulder_pitch", "shoulder_roll", "elbow_roll", "wrist_pitch", "wrist_roll"]


def _ens(jambe, taille):
    d = {j: 2 for j in jambe + BRAS5 + ["gripper"]}
    d.update({j: 1 for j in taille + ["neck_yaw", "neck_pitch"]})
    return d


ENSEMBLES = {
    25: dict(axes=_ens(JAMBE5, ["waist_yaw"]),
             source="JAMAIS calculé le 2026-10-04 (seulement cité par le prompt d'alors) : le 26 sans roulis de taille"),
    26: dict(axes=_ens(JAMBE5, ["waist_yaw", "waist_roll"]),
             source="squelette v3 (params/squelette.yaml, fiche 0068 : 5 axes par jambe)"),
    27: dict(axes=_ens(JAMBE5 + ["ankle_roll"], ["waist_yaw"]),
             source="fiche 0069 (proposition de Claude) et étude du 2026-10-04 : jambes 6 × 2, taille 1, bras 5 × 2, pinces, cou 2"),
    29: dict(axes=_ens(JAMBE5 + ["ankle_roll"], ["waist_yaw", "waist_roll", "waist_pitch"]),
             source="étude du 2026-10-04 (« 29, bras 5 ») : le 27 avec la taille à 3 axes"),
}
PETITS_AXES = {"neck_yaw", "neck_pitch", "neck_roll", "gripper"}
NOMS = {"pince": "gripper"}     # capacites.yaml dit « pince », squelette.yaml « gripper » : le même axe (noms_a_creer)

# ─────────────────────────────── tâches ─────────────────────────────────
REGIME = {"marche_sol_plat": "les deux", "releve": "pointe", "releve_simule": "pointe", "saut_vertical": "pointe",
          "gestes_pointage": "pointe", "saisie": "continu", "charge_lourde": "continu", "poussee": "continu",
          "buste": "continu", "tete": "continu"}
OPTIONNELLES = ["releve", "saut_vertical", "gestes_pointage", "saisie", "charge_lourde", "poussee", "buste", "tete"]
SANS_CALCUL = {
    "sol_irregulier": "simulation de marche sur obstacles de 2 et 4 cm : non faite",
    "pente": "simulation de marche en pente de 5 et 10° : non faite",
    "course": "aucune politique de course (phase 3b) : rien à mettre à l'échelle",
    "mains_a_doigts": "aucun ensemble du Lab n'a de doigts",
    "visage": "masse, prix et place d'un écran ou de micro-servos : non relevés",
}
# Axes qu'une capacité VOULUE exige au-delà de son calcul. PROPOSÉ par Claude (2026-10-07) : le roulis de
# cheville pour le sol irrégulier (exemple du prompt) ; des doigts pour la main. La pente et la course n'en
# exigent pas (des robots à 5 axes par jambe courent : fiche 0068, H1).
AXES_CIBLE = {"sol_irregulier": ["ankle_roll"], "mains_a_doigts": ["doigts"]}


def cible_defaut(cap, profil="lab") -> dict:
    """Le profil cible de params/capacites.yaml (`profils`). `lab` : DÉCIDÉ par Jeremy le 2026-10-07 ; `final` :
    fiche 0069, niveaux non fixés (null) pris ici au plus bas, à balayer en phase 4b."""
    t = cap["profils"][profil]["taches"]
    return {k: (v if v is not None else cap["taches"][k]["niveaux"][0]) for k, v in t.items()}


def non_couvertes(axes, cible) -> list[str]:
    """Capacités voulues dont l'ensemble n'a pas les axes."""
    return sorted({t for t, niv in paires(cible) if any(a not in axes for a in axes_requis(t, niv) + AXES_CIBLE.get(t, []))},
                  key=list(cible).index)


def paires(profil):
    """(tâche, niveau) d'un profil ; un niveau peut être une LISTE (le relevé du profil lab : dos et ventre)."""
    for t, v in profil.items():
        for n in (v if isinstance(v, list) else [v]):
            yield t, n


def axes_requis(tache, niveau):
    """Axes sans lesquels la capacité n'existe pas (elle EST ces axes) ; les autres axes absents sont rigides."""
    if tache == "buste":
        return ["waist_yaw"] if niveau == "lacet seul" else ["waist_yaw", "waist_roll", "waist_pitch"]
    if tache == "tete":
        return ["neck_yaw", "neck_pitch"] + (["neck_roll"] if niveau == 3 else [])
    if tache == "saisie":
        return ["gripper"]
    return []


def lire(nom):
    import marche_composants as MC
    return MC.lire(nom)


# ─────────────────────────────── besoins ────────────────────────────────
def table_besoins(lignes_ep, marches, releve, cap) -> dict:
    """{(H, tâche, niveau): {axe: {pk: [(a, b)], c: [(a, b)], w: [ω]}}} : les entrées BRUTES, avant le maximum."""
    T = {}

    def ajouter(H, t, niv, art, a, b, kind, w=None):
        e = T.setdefault((round(H, 2), t, niv), {}).setdefault(NOMS.get(art, art), dict(pk=[], c=[], w=[]))
        e[kind].append((a, b))
        if w:
            e["w"].append(w)

    for l in lignes_ep:
        kind = "c" if REGIME[l["tache"]] == "continu" else "pk"
        ajouter(l["H"], l["tache"], l["niveau"], l["articulation"], l["a"], l["b"], kind, l.get("omega"))
    frs = {r: e["Fr"] for r, e in marches.items()}
    for v in cap["taches"]["marche_sol_plat"]["niveaux"]:
        for H in EP.HS:
            couvrants = [r for r, f in frs.items() if f >= v / math.sqrt(G * H) - 1e-9]
            for r in couvrants:
                for ty, p in marches[r]["profil"].items():
                    ajouter(H, "marche_sol_plat", v, ty, p["pointe"] * G * H, 0.0, "pk", p["omega"] * math.sqrt(G / H))
                    ajouter(H, "marche_sol_plat", v, ty, p["rms"] * G * H, 0.0, "c")
    # Qui marche à v marche aussi plus lentement : un niveau reprend les entrées des niveaux inférieurs
    # (sinon, moins de robots couvrent un Froude plus haut et le besoin BAISSERAIT avec la vitesse).
    niv_m = cap["taches"]["marche_sol_plat"]["niveaux"]
    for H in EP.HS:
        for i, v in enumerate(niv_m):
            haut = T.get((round(H, 2), "marche_sol_plat", v))
            for w in niv_m[:i]:
                bas = T.get((round(H, 2), "marche_sol_plat", w))
                if haut is None or bas is None:
                    continue
                for ax, e in bas.items():
                    h = haut.setdefault(ax, dict(pk=[], c=[], w=[]))
                    for k in ("pk", "c", "w"):
                        h[k] += [x for x in e[k] if x not in h[k]]
    if releve:
        for niv in cap["taches"]["releve"]["niveaux"]:
            for H in EP.HS:
                for ty, p in releve["profil"].items():
                    ajouter(H, "releve", niv, ty, p["pointe"] * G * H, 0.0, "pk", p["omega"] * math.sqrt(G / H))
    return T


def besoins(T, H, profil, M, combine=max) -> dict:
    """Par axe : pointe, continu, vitesse = le MAXIMUM des tâches du profil, à la masse M."""
    out = {}
    for t, niv in paires(profil):
        for ax, e in T.get((round(H, 2), t, niv), {}).items():
            o = out.setdefault(ax, dict(pk=0.0, c=0.0, w=0.0))
            for k in ("pk", "c"):
                for a, b in e[k]:
                    o[k] = combine(o[k], a * M + b)
            for w in e["w"]:
                o["w"] = combine(o["w"], w)
    return out


def verifier_maximum(bes, T, H, profil, M) -> list[str]:
    """Contrôle INDÉPENDANT de `besoins` : chaque valeur doit être le maximum des entrées brutes."""
    ecarts = []
    axes = {ax for t, niv in paires(profil) for ax in T.get((round(H, 2), t, niv), {})} | set(bes)
    for ax in axes:
        ent = [T.get((round(H, 2), t, niv), {}).get(ax) for t, niv in paires(profil)]
        ent = [e for e in ent if e]
        for k in ("pk", "c", "w"):
            vals = [w for e in ent for w in e["w"]] if k == "w" else [a * M + b for e in ent for a, b in e[k]]
            attendu, obtenu = max(vals, default=0.0), bes.get(ax, {}).get(k, 0.0)
            if abs(obtenu - attendu) > 1e-9 * max(1.0, abs(attendu)):
                ecarts.append(f"{ax}.{k} : {obtenu:.4g} au lieu du maximum {attendu:.4g}")
    return ecarts


# ─────────────────────────────── actionneurs ────────────────────────────
def diametre(dims):
    """Ø du corps (mm) : la première cote d'un « Ø… » ; pour un boîtier, la plus grande cote (prudent)."""
    if not dims:
        return None
    s = str(dims).replace(",", ".").split(";")[0].strip()
    nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", s)]
    if not nums:
        return None
    return nums[0] if s.startswith("Ø") else max(nums)


def num(x):
    return float(x) if isinstance(x, (int, float)) and not isinstance(x, bool) else None


def catalogue():
    """{famille: [actionneurs triés par masse]} ; ceux sans AUCUN couple publié sont écartés, et comptés."""
    import dimensionnement as D
    import marche_actionneurs as MA
    taux = lire("budget.yaml")["taux_de_change"]
    import taille_minimale as TM
    fam, rows = MA.charger()
    cv = TM.conventions()
    cand = lire("actionneurs.yaml")["candidats"]
    import marche_composants as MC
    plages = {}
    for f in set(r["famille"] for r in rows if r["famille"]):
        plages.update({x["id"]: (x["min"], x["max"]) if x["min"] is not None else None for x in MC.plages(f)})
    par, ecartes = {}, []
    for r in rows:
        couple = r["pointe"] or r["blocage"]
        if not couple:
            ecartes.append(r["id"])
            continue
        v, m = num(r["vitesse"]), num(r["masse"])
        par.setdefault(r["famille"], []).append(dict(
            id=r["id"], pointe=float(couple), par_blocage=not r["pointe"], continu=num(r["continu"]),
            vitesse=v * 2 * math.pi / 60 if v else None, masse=m / 1000 if m else None,
            prix=EP.prix_chf(r["prix"], taux, D), D=diametre(r["dims"]), famille=r["famille"],
            v_ref=num(r["tension"]), plage=plages.get(r["id"]),
            plage_servo=plages.get(r["id"]) or plages.get(r["id"].replace("sts3", "st3", 1)),
            geo=TM.moteur_catalogue(cand[r["id"]], cv) if r["id"] in cand else TM.moteur_dims(r["dims"], cv)))
    for l in par.values():
        l.sort(key=lambda a: (a["masse"] is None, a["masse"] or 0.0, a["pointe"]))
    return par, ecartes, fam


def passe(a, need, marge) -> bool:
    """Les critères CONNUS sont tenus (un critère inconnu ne fait ni passer ni échouer : il est rendu)."""
    if a.get("compat") is False:                       # plage de tension dépassée par la variante 12S / 13S
        return False
    if a["pointe"] < marge * need["pk"]:
        return False
    if need["c"] > 0 and a["continu"] is not None and a["continu"] < marge * need["c"]:
        return False
    if need["w"] > 0 and a["vitesse"] is not None and a["vitesse"] < need["w"]:
        return False
    return True


def choisir(acts, need, marge, depuis=0, cotes=False):
    """Indice du plus PETIT actionneur (à partir de `depuis`) qui passe de façon VÉRIFIABLE (aucune donnée
    manquante) ; à défaut, du plus petit qui passe sur ce qui est connu (solution alors INCONNUE) ; None si aucun."""
    repli = None
    for i in range(depuis, len(acts)):
        a = acts[i]
        if not passe(a, need, marge):
            continue
        if not inconnues_de(a, need) and not (cotes and a.get("geo") is None):
            return i
        if repli is None:
            repli = i
    return repli


def inconnues_de(a, need) -> list[str]:
    out = []
    if a["par_blocage"] and need["pk"] > 0:
        out.append(f"couple de pointe de {a['id']} (seul le blocage est publié)")
    if need["c"] > 0 and a["continu"] is None:
        out.append(f"couple continu de {a['id']}")
    if need["w"] > 0 and a["vitesse"] is None:
        out.append(f"tension de référence de la vitesse de {a['id']}" if a.get("v_ref_inconnue") else
                   f"vitesse à vide de {a['id']}")
    if "compat" in a and a["compat"] is None:
        out.append(f"plage de tension de {a['id']}")
    if a["masse"] is None:
        out.append(f"masse de {a['id']}")
    if a["prix"] is None:
        out.append(f"prix de {a['id']}")
    return out


# ─────────────────────────────── contexte ───────────────────────────────
def structures() -> dict:
    """Structure à H_S (kg) par ensemble et par cas (central, haute) : scripts/structure_plaques.py."""
    import structure_plaques as SP
    m = SP.modele()
    out = {}
    for k, e in ENSEMBLES.items():
        n_haut = sum(n for a, n in e["axes"].items() if a not in JAMBE5 + ["ankle_roll"])
        for cas, var in STRUCT_CAS.items():
            out[(k, cas)] = SP.structure(m, var, SP.V3, n_rs05_de_plus=n_haut - 16, roulis_cheville="ankle_roll" in e["axes"])
    return dict(par_ensemble=out, H_S=m["H_S"], modele=m, charge=lire("exigences_S.yaml")["charge_utile"]["valeur_kg"])


def electrique(ctx, S, f_can, etendue, coupure=None) -> dict:
    """Variante de tension S (12 ou 13) appliquée aux actionneurs du CORPS (sur le bus moteurs), et données du système
    électrique (phase 4a quinquies). Les petits axes sont sur des rails régulés : non concernés."""
    import systeme_electrique as SE
    pui = SE.lire("puissance.yaml")
    hyp = pui["hypotheses"]
    var = SE.variante(S, coupure=coupure)
    for fam in EP.CORPS:
        ctx["act"][fam] = [dict(a, compat=SE.compatibilite(a["plage"], var),
                                vitesse=(a["vitesse"] * SE.facteur_vitesse(a["v_ref"], var))
                                if a["vitesse"] and SE.facteur_vitesse(a["v_ref"], var) else None,
                                v_ref_inconnue=SE.facteur_vitesse(a["v_ref"], var) is None)
                           for a in ctx["act"].get(fam, [])]
    import simulations_marche as SM
    marches, _, _ = SM.charger()
    opts = SE.options_calculateur()
    niveau = ctx["cible"].get("ia_embarquee")
    ctx["struct"]["charge"] = hyp["imu_cablage_kg"]["valeur"]
    return dict(S=S, var=var, hyp=hyp, pui=pui, f_can=f_can, etendue=etendue, cible=ctx["cible"],
                comps=SE.composants(pui) if (pui.get("marche") or {}).get("produits") else None,
                Pm=SE.table_puissance(marches, ctx["cap"], EP.HS), P3a=SE.table_pointe_3a(EP.tout()[2]),
                cells=SE.cellules_21700(), calc=SE.choisir_calculateur(opts, niveau, hyp) if niveau else None,
                adapt=SE.adaptateurs_can(), serie=SE.adaptateur_serie(), niveau_ia=niveau)


def contexte(struct=None, cible=None, profil="lab", S=None, f_can=500, etendue=True, coupure=None) -> dict:
    import simulations_marche as SM
    cap, an, lignes = EP.tout()
    marches, releve, manque = SM.charger()
    lm = lire("lois_masse.yaml")
    ex = dict(lm["variantes"]["allometrique"]["exposant"], iso=lm["variantes"]["isometrique"]["exposant"])
    par, ecartes, fams = catalogue()
    sq = lire("squelette.yaml")
    import taille_minimale as TM
    ctx = dict(cap=cap, an=an, R={k: v["valeur"] for k, v in an["ratios"].items()}, cv=TM.conventions(),
                cible=cible or cible_defaut(cap, profil), profil=profil,
                T=table_besoins(lignes, marches, releve, cap), manque=manque,
                C={H: EP.contraintes(H, cap, an) for H in EP.HS}, ex=ex, decision=lm.get("retenue"),
                act=par, ecartes=ecartes, fams=fams, struct=struct or structures(),
                marge=lire("actionneurs.yaml")["dimensionnement"]["marge"],
                jeu=sq["ecarts_ansur"]["cheville"]["jeu_mm"]["valeur"],
                fr_max=max((e["Fr"] for e in marches.values()), default=0.0), memo={})
    if S:
        ctx["elec"] = electrique(ctx, S, f_can, etendue, coupure)
    return ctx


def masse_structure(ctx, ens, H, b, cas="central"):
    s = ctx["struct"]
    return s["par_ensemble"][(ens, cas)] * (H / s["H_S"]) ** b


CAS = [(b, c) for b in BANDE for c in STRUCT_CAS]           # six cas de masse : b × structure
TRONC_ROLE = {"tronc": ("waist_yaw", "waist_roll", "waist_pitch", "shoulder_pitch", "shoulder_roll"),
              "bras": tuple(BRAS5), "cou": ("neck_yaw", "neck_pitch", "neck_roll")}


def place(ctx, axes, choix, H):
    """Taille minimale géométrique (taille_minimale) pour les actionneurs choisis ; None et les cotes manquantes."""
    import taille_minimale as TM
    manque = sorted({c["id"] for c in choix.values() if c.get("geo") is None})
    if manque:
        return None, [f"cotes de {i}" for i in manque]
    A = {r: choix[r]["geo"] for r in ("hip_yaw", "hip_roll", "hip_pitch", "knee", "ankle_pitch", "ankle_roll") if r in choix}
    if any(r not in A for r in ("hip_yaw", "hip_roll", "hip_pitch", "knee", "ankle_pitch")):
        return None, ["place : jambe incomplète dans l'ensemble"]
    for role, noms in TRONC_ROLE.items():
        geos = [choix[a]["geo"] for a in noms if a in choix]
        A[role] = max(geos, key=lambda g: (g["R"], g["L"])) if geos else A["hip_roll"]
    ens = dict(cheville=6 if "ankle_roll" in axes else 5, taille=sum(1 for a in axes if a.startswith("waist")),
               bras=5, pince="gripper" in axes)
    return TM.evaluer(ens, A, H, ctx["R"], ctx["cv"]), []


# ─────────────────────────────── évaluation ─────────────────────────────
def grille_haut(H):
    """Le pas de la grille des besoins (exigences_physiques.HS) immédiatement au-dessus de H : prudent."""
    return next((h for h in EP.HS if h >= H - 1e-9), None)


def grille_bas(H):
    return max((h for h in EP.HS if h <= H + 1e-9), default=EP.HS[0])


def evaluer(ctx, ens, H, fc, fp, profil) -> dict | None:
    """Une solution. None si le profil demande un axe que l'ensemble n'a pas (capacité sans objet).

    H fixe les PROPORTIONS (ANSUR) ; la place peut allonger des chaînes : la hauteur RÉELLE H_r ≥ H. Les
    couples sont lus à la hauteur réelle (pas supérieur de la grille, Ht), la structure grandit avec H_r, et
    l'on recommence (choix → place → H_r) jusqu'à ce que Ht ne bouge plus (phase 4a ter)."""
    axes = ENSEMBLES[ens]["axes"]
    for t, niv in paires(profil):
        if any(a not in axes for a in axes_requis(t, niv)):
            return None
    fam_de = {a: (fp if a in PETITS_AXES else fc) for a in axes}
    acts = {a: ctx["act"].get(fam_de[a], []) for a in axes}
    violees = [f"{a} : famille {fam_de[a]} vide au catalogue" for a in axes if not acts[a]]
    if violees:
        return dict(statut="infaisable", violees=violees, inconnues=[])
    idx = {a: 0 for a in axes}
    Ht, Hr, pl, manque_place, iterations = H, H, None, [], 0
    m_el, el = 0.0, None                                     # système électrique (phase 4a quinquies)
    axes_corps = {a: n for a, n in axes.items() if a not in PETITS_AXES}
    for iterations in range(1, 16):                          # hauteur réelle ↔ couples ↔ choix ↔ place ↔ électrique
        mfix = (lambda b, c="central", Hm=Hr, me=m_el:
                masse_structure(ctx, ens, Hm, ctx["ex"][b], c) + ctx["struct"]["charge"] + me)
        M = {}
        for _ in range(40):                                  # point fixe : masse ↔ choix, à Ht
            change = False
            for b, c in CAS:
                M[(b, c)] = mfix(b, c) + sum(n * (acts[a][idx[a]]["masse"] or 0.0) for a, n in axes.items())
                bes = besoins(ctx["T"], Ht, profil, M[(b, c)])
                for a in axes:
                    need = bes.get(a, dict(pk=0.0, c=0.0, w=0.0))
                    cle = (fam_de[a], idx[a], round(need["pk"], 3), round(need["c"], 3), round(need["w"], 2))
                    if cle not in ctx["memo"]:
                        ctx["memo"][cle] = choisir(acts[a], need, ctx["marge"], idx[a], True)
                    i = ctx["memo"][cle]
                    if i is None:
                        violees.append(f"{a} : aucun {fam_de[a]} ne tient (pointe {need['pk']:.2f}, continu "
                                       f"{need['c']:.2f} N·m, ω {need['w']:.1f} rad/s, b {b}, structure {c}, "
                                       f"hauteur réelle {f1(Hr, 3)} m, marge {ctx['marge']})")
                        return dict(statut="infaisable", violees=violees, inconnues=[])
                    if i > idx[a]:
                        idx[a], change = i, True
            if not change:
                break
        choix = {a: acts[a][idx[a]] for a in axes}
        pl, manque_place = place(ctx, axes, choix, H)        # taille minimale géométrique, aux proportions de H
        Hr = pl["H_reel"] if pl else H
        m_el_n = m_el
        if "elec" in ctx:
            import systeme_electrique as SE
            el = SE.dimensionner(ctx["elec"], ctx["R"], ctx["cible"], axes_corps,
                                 [choix[a] for a in axes if a in PETITS_AXES], max(M.values()), Ht, Hr, profil,
                                 sum(axes_corps.values()), ctx["elec"])
            if el["place"]:
                Hr += el["place"]["allonge_m"]               # le tronc s'allonge si l'électronique n'y tient pas
            m_el_n = el["masse"] if el["masse"] is not None else el["masse_connue"]
        Ht_n = grille_haut(Hr)
        if Ht_n is None:
            return dict(statut="infaisable", inconnues=[],
                        violees=[f"hauteur réelle {f1(Hr, 3)} m au-delà de la grille des besoins ({EP.HS[-1]} m)"])
        if abs(Ht_n - Ht) < 1e-9 and abs(m_el_n - m_el) < 1e-3:
            break
        Ht, m_el = Ht_n, m_el_n
    inconnues = list(manque_place) + (el["inconnues"] if el else [])
    for t, niv in paires(profil):
        if (round(Ht, 2), t, niv) not in ctx["T"]:
            inconnues.append(f"{t} {niv} : aucun besoin calculé à {f1(Ht, 2)} m"
                             + (" (Froude au-delà des marches simulées)" if t == "marche_sol_plat" else ""))
    bes = {k: besoins(ctx["T"], Ht, profil, M[k]) for k in CAS}
    Hc = grille_bas(Hr)
    for k in CAS:                                             # masses minimales (équilibre, frottement)
        for t, niv in paires(profil):
            mmin = ctx["C"].get(Hc, {}).get((t, niv))
            if mmin and M[k] < mmin:
                violees.append(f"{t} {niv} : M = {M[k]:.1f} kg < {mmin:.1f} kg (équilibre ou frottement, "
                               f"b {k[0]}, structure {k[1]})")
    for a, c in choix.items():
        need = {k: max(bes[x].get(a, {}).get(k, 0.0) for x in CAS) for k in ("pk", "c", "w")}
        inconnues += inconnues_de(c, need)
    inconnues = list(dict.fromkeys(inconnues))
    prix = [c["prix"] for c in choix.values()]
    cout_act = sum(n * choix[a]["prix"] for a, n in axes.items()) if None not in prix else None
    cout = cout_act if el is None else (cout_act + el["prix"] if cout_act is not None and el["prix"] is not None else None)
    # borne pessimiste H³ : le même choix tient-il ?
    mc = M[("central", "central")]
    M_iso = mfix("iso") + mc - mfix("central")
    b_iso = besoins(ctx["T"], Ht, profil, M_iso)
    tient_iso = all(c["pointe"] >= ctx["marge"] * b_iso.get(a, {}).get("pk", 0)
                    and (c["continu"] is None or c["continu"] >= ctx["marge"] * b_iso.get(a, {}).get("c", 0))
                    for a, c in choix.items())
    statut = "infaisable" if violees else ("INCONNU" if inconnues else "faisable")
    nc = non_couvertes(axes, ctx["cible"])
    return dict(statut=statut, violees=violees, inconnues=inconnues, choix=choix, M=mc, elec=el, cout_actionneurs=cout_act,
                M_bande=(min(M.values()), max(M.values())), M_iso=M_iso, tient_iso=tient_iso, cout=cout,
                E=mc * G * ctx["R"]["hauteur_hanche"] * Hr, ncap=len(profil),
                H_reel=Hr if pl else None, H_couples=Ht, iterations=iterations, place=pl, non_couvertes=nc,
                n_couvertes=len(ctx["cible"]) - len(nc),
                cap_inconnues=[t for t in ctx["cible"] if t in SANS_CALCUL and t not in nc],
                n_axes=sum(axes.values()), besoins=bes[("central", "central")])


def niveau_bas(cap, t):
    return cap["taches"][t]["niveaux"][0]


CHAMPS_LEGERS = ("statut", "ncap", "cout", "cout_actionneurs", "M", "E", "H_reel", "H_couples", "non_couvertes",
                 "n_couvertes")


def _interner(xs) -> tuple:
    return tuple(sys.intern(x) for x in xs or ())


def leger(r: dict, **cle) -> dict:
    """Une solution réduite à ce que servent le classement, les comptes et le graphique (ajouté le 2026-10-08) : les
    textes des données manquantes sont PARTAGÉS (internés), le détail (actionneurs, système électrique) est jeté et
    se retrouve en réévaluant la solution (`complet`), le calcul étant déterministe."""
    el = r.get("elec")
    d = {c: r.get(c) for c in CHAMPS_LEGERS}
    d.update(cle, inconnues=_interner(r.get("inconnues")), leger=True,
             elec={"inconnues": _interner(el["inconnues"]), "prix_connu": el.get("prix_connu")} if el else None)
    return d


def complet(ctx, x: dict) -> dict:
    """La solution complète (réévaluée) d'un enregistrement léger."""
    if not x.get("leger"):
        return x
    r = evaluer(ctx, x["ens"], x["H"], x["fc"], x["fp"], x["profil"])
    return dict(r, ens=x["ens"], H=x["H"], fc=x["fc"], fp=x["fp"], profil=x["profil"])


def explorer(ctx, ensembles=None, hs=None, corps=None, petits=None, garder_leger=False):
    """Toutes les solutions : chaque sous-ensemble des tâches optionnelles VOULUES, au niveau de la cible.

    Un niveau plus haut ne change pas le nombre de capacités tenues et coûte au
    moins autant : il ne peut pas être sur le front. Il est chiffré à part
    (`cout_capacites`)."""
    cap, cible = ctx["cap"], ctx["cible"]
    base = {"marche_sol_plat": cible.get("marche_sol_plat", niveau_bas(cap, "marche_sol_plat"))}
    opt = [t for t in OPTIONNELLES if t in cible]
    out = []
    for k in range(len(opt) + 1):
        for sub in itertools.combinations(opt, k):
            profil = dict(base, **{t: cible[t] for t in sub})
            for ens in (ensembles or ENSEMBLES):
                for H in (hs or H_LAB):
                    for fc in (corps or EP.CORPS):
                        for fp in (petits or EP.PETITS):
                            r = evaluer(ctx, ens, H, fc, fp, profil)
                            if r:
                                cle = dict(ens=ens, H=H, fc=fc, fp=fp, profil=profil)
                                out.append(leger(r, **cle) if garder_leger else dict(r, **cle))
    return out


def pareto(sols):
    """Non dominées sur (coût ↓, masse ↓, énergie de chute ↓, capacités tenues ↑, voulues couvertes ↑), faisables."""
    f = [s for s in sols if s["statut"] == "faisable"]
    obj = lambda s: (s["cout"], s["M"], s["E"], -s["ncap"], -s.get("n_couvertes", 0))
    f.sort(key=obj)
    front = []
    for s in f:
        v = obj(s)
        domine = False
        for p in front:
            w = obj(p)
            if all(x <= y for x, y in zip(w, v)) and w != v:
                domine = True
                break
            if w == v:
                domine = True                                # doublon exact : un seul représentant
                break
        if not domine:
            front.append(s)
    return front


def meilleure(ctx, profil, corps=None):
    """La solution faisable la moins chère pour un profil, sur tout l'espace ; et la plus petite H faisable."""
    best, hmin, n_inc, raisons, n_eval, viol = None, None, 0, Counter(), 0, Counter()
    best_inc = None              # sans faisable : la meilleure dont les seules inconnues sont celles, COMMUNES, du système électrique
    for ens in ENSEMBLES:
        for H in H_LAB:
            for fc in (corps or EP.CORPS):
                for fp in EP.PETITS:
                    r = evaluer(ctx, ens, H, fc, fp, profil)
                    if not r:
                        continue
                    n_eval += 1
                    viol.update({re.sub(r"\d+(?:[.,]\d+)?", "#", v) for v in r["violees"]})
                    if r["statut"] == "faisable":
                        r = dict(r, ens=ens, H=H, fc=fc, fp=fp, profil=profil)
                        if best is None or (r["cout"], r["M"]) < (best["cout"], best["M"]):
                            best = r
                        hr = r["H_reel"] or H
                        hmin = hr if hmin is None else min(hmin, hr)
                    elif r["statut"] == "INCONNU":
                        n_inc += 1
                        raisons.update(r["inconnues"])
                        if not set(r["inconnues"]) - set((r.get("elec") or {}).get("inconnues") or []):
                            r = dict(r, ens=ens, H=H, fc=fc, fp=fp, profil=profil, cout=cout_borne(r), borne=True)
                            if best_inc is None or (r["cout"], r["M"]) < (best_inc["cout"], best_inc["M"]):
                                best_inc = r
    if best is None and best_inc is not None:
        best = best_inc
    return dict(best=best, hmin=hmin, n_inc=n_inc, raisons=raisons, n_eval=n_eval, viol=viol)


def cout_borne(x):
    """Coût total si connu ; sinon sa part CONNUE (actionneurs + éléments chiffrés du système électrique) : une borne basse."""
    if x.get("cout") is not None:
        return x["cout"]
    return (x.get("cout_actionneurs") or 0.0) + ((x.get("elec") or {}).get("prix_connu") or 0.0)


def cout_capacites(ctx):
    """Pour chaque tâche CALCULÉE du profil cible, chaque niveau jusqu'au niveau visé : la meilleure solution, et
    l'écart au niveau inférieur (au premier niveau : la marche seule, au niveau du profil)."""
    cap, cible = ctx["cap"], ctx["cible"]
    base = {"marche_sol_plat": cible.get("marche_sol_plat", niveau_bas(cap, "marche_sol_plat"))}
    ref = meilleure(ctx, base)
    out = []
    for t in ["marche_sol_plat"] + [x for x in OPTIONNELLES if x in cible]:
        niv = cap["taches"][t]["niveaux"]
        vise = cible[t] if isinstance(cible[t], list) else [cible[t]]
        haut = max(niv.index(v) for v in vise)
        prec = None if t == "marche_sol_plat" else ref
        for n in niv[:haut + 1]:
            profil = ({"marche_sol_plat": n} if t == "marche_sol_plat" else dict(base, **{t: n}))
            r = meilleure(ctx, profil)
            out.append(dict(tache=t, niveau=n, res=r, prec=prec))
            prec = r
    return ref, out


# ─────────────────────────────── sorties ────────────────────────────────
def f1(x, n=1):
    return "—" if x is None else f"{x:,.{n}f}".replace(",", " ").replace(".", ",")


def resume_choix(s):
    vu = {}
    for a, c in s["choix"].items():
        vu.setdefault(c["id"], []).append(a)
    return " ; ".join(f"{i} : {', '.join(v)}" for i, v in vu.items())


def classement(front):
    return sorted(front, key=lambda s: (len(s.get("non_couvertes", [])), -s["ncap"], s["cout"], s["M"]))


def blocantes(sols, n=10):
    """Données inconnues, rangées par le nombre de solutions INCONNUES qu'elles bloquent ; « seule » = l'unique manque."""
    tot, seules = Counter(), Counter()
    for s in sols:
        if s["statut"] == "INCONNU":
            tot.update(s["inconnues"])
            if len(s["inconnues"]) == 1:
                seules.update(s["inconnues"])
    return [(k, v, seules[k]) for k, v in tot.most_common(n)]


PAL = ["#cfe0f8", "#9ec5f4", "#7db1ee", "#5b9ce8", "#3f88df", "#2a78d6", "#205fb3", "#174f9a", "#0f3a73"]   # une teinte, ordonnée


def svg(front, ctx_sols) -> str:
    W, Hh, ML, MB, MT, MR = 760, 420, 64, 46, 40, 150                 # non-cote: mise en page en px
    pts = [s for s in ctx_sols if s["statut"] == "faisable"]
    if not front:
        return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 40"><text x="10" y="24">'
                'aucune solution faisable</text></svg>')
    xs = [s["cout"] for s in pts] or [0, 1]
    ys = [s["M"] for s in pts] or [0, 1]
    x0, x1 = 0, max(xs) * 1.05
    y0, y1 = 0, max(ys) * 1.05
    X = lambda v: ML + (v - x0) / (x1 - x0) * (W - ML - MR)
    Y = lambda v: Hh - MB - (v - y0) / (y1 - y0) * (Hh - MB - MT)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}" width="100%" role="img" '
         'aria-label="Front de Pareto de YXOR Lab : coût des actionneurs et masse, par nombre de capacités tenues">',
         "<style>:root{--s:#fcfcfb;--t1:#0b0b0b;--t2:#52514e;--g:#e4e3df;--ctx:#d6d5cf}"
         "@media (prefers-color-scheme: dark){:root{--s:#1a1a19;--t1:#fff;--t2:#c3c2b7;--g:#33332f;--ctx:#45443f}}"
         "text{font:11px system-ui,sans-serif;fill:var(--t2)} .t{fill:var(--t1);font-weight:600;font-size:12px}"
         ".grid{stroke:var(--g)} .ctx{fill:var(--ctx)}</style>",
         f'<rect width="{W}" height="{Hh}" fill="var(--s)"/>',
         f'<text x="{ML}" y="20" class="t">YXOR Lab : front de Pareto (coût, masse, énergie de chute, capacités) — '
         f'{len(front)} solutions sur {len(pts)} faisables</text>']
    for k in range(6):
        gx, gy = x0 + k * (x1 - x0) / 5, y0 + k * (y1 - y0) / 5
        o.append(f'<line class="grid" x1="{X(gx):.1f}" y1="{MT}" x2="{X(gx):.1f}" y2="{Hh - MB}"/>'
                 f'<text x="{X(gx):.1f}" y="{Hh - MB + 14}" text-anchor="middle">{gx:,.0f}</text>'.replace(",", " "))
        o.append(f'<line class="grid" x1="{ML}" y1="{Y(gy):.1f}" x2="{W - MR}" y2="{Y(gy):.1f}"/>'
                 f'<text x="{ML - 6}" y="{Y(gy) + 4:.1f}" text-anchor="end">{gy:.0f}</text>')
    o.append(f'<text x="{(ML + W - MR) / 2}" y="{Hh - 8}" text-anchor="middle">coût des actionneurs (CHF HT)</text>'
             f'<text x="16" y="{(MT + Hh - MB) / 2}" transform="rotate(-90 16 {(MT + Hh - MB) / 2})" '
             'text-anchor="middle">masse, b central (kg)</text>')
    for s in pts[:: max(1, len(pts) // 3000)]:
        o.append(f'<circle class="ctx" cx="{X(s["cout"]):.1f}" cy="{Y(s["M"]):.1f}" r="2"/>')
    nmax = max(s["ncap"] for s in front)
    for s in sorted(front, key=lambda s: s["ncap"]):
        col = PAL[min(len(PAL) - 1, s["ncap"] - 1 + (len(PAL) - nmax))]
        o.append(f'<circle cx="{X(s["cout"]):.1f}" cy="{Y(s["M"]):.1f}" r="4.5" fill="{col}" stroke="var(--s)" '
                 f'stroke-width="1.5"><title>{s["ens"]} axes, H {s["H"]:.2f} m, {s["fc"]} + {s["fp"]}, '
                 f'{s["ncap"]} capacités, {s["cout"]:.0f} CHF, {s["M"]:.1f} kg</title></circle>')
    for k, n in enumerate(range(1, nmax + 1)):
        col = PAL[min(len(PAL) - 1, n - 1 + (len(PAL) - nmax))]
        y = MT + 10 + k * 18
        o.append(f'<circle cx="{W - MR + 20}" cy="{y}" r="4.5" fill="{col}"/>'
                 f'<text x="{W - MR + 30}" y="{y + 4}">{n} capacité{"s" if n > 1 else ""}</text>')
    o.append(f'<circle class="ctx" cx="{W - MR + 20}" cy="{MT + 10 + nmax * 18}" r="2"/>'
             f'<text x="{W - MR + 30}" y="{MT + 14 + nmax * 18}">faisable, dominée</text>')
    o.append("</svg>")
    return "\n".join(o)


def rapport(ctx, sols, front, ref, caps, nverif, duree, runs=None, top0=None) -> str:
    s_ = ctx["struct"]
    ex = ctx["ex"]
    stat = Counter(s["statut"] for s in sols)
    L = ["# Explorateur : YXOR Lab", "",
         "**Engendré** par `.venv/bin/python scripts/explorateur.py --ecrire`. Ne pas éditer à la main. "
         "**Étude, aucune décision d'architecture** (phases 4a et 4a bis, fiche 0069).", "",
         "## Loi de masse", "",
         f"DÉCIDÉE par Jeremy le 2026-10-07 (`params/lois_masse.yaml`, `retenue`) : {ctx['decision']['decide']}", "",
         f"Une solution n'est **faisable** que si elle tient aux trois exposants b = {f1(ex['bas'], 3)}, "
         f"{f1(ex['central'], 3)} et {f1(ex['haut'], 3)}, chacun avec la structure centrale "
         f"(« {STRUCT_CAS['central']} ») ET haute (« {STRUCT_CAS['haute']} ») : six cas. La masse est donnée au b "
         f"central, structure centrale ; la bande couvre les six cas. H³ (b = {ex['iso']:g}) est rapporté comme "
         "borne pessimiste, sans filtrer.", "",
         "## Profil cible", "",
         (f"Profil **{ctx['profil']}** de `params/capacites.yaml`"
          + (" : DÉCIDÉ par Jeremy le 2026-10-07 (ses mots y sont cités). " if ctx["profil"] == "lab" else
             " (fiche 0069 ; niveaux non fixés pris au plus bas). "))
         + "Capacités voulues : "
         + ", ".join(f"{t} {' et '.join(map(str, n)) if isinstance(n, list) else n}" for t, n in ctx["cible"].items())
         + ". Axes exigés au-delà du calcul (PROPOSÉ) : "
         + ", ".join(f"{t} → {', '.join(a)}" for t, a in AXES_CIBLE.items()) + ".", "",
         "| Ensemble | Ne couvre pas | Voulues non calculées (INCONNUES) |", "| ---: | --- | --- |"]
    for k, e in ENSEMBLES.items():
        nc = non_couvertes(e["axes"], ctx["cible"])
        L.append(f"| {k} | {', '.join(nc) or '—'} | {', '.join(t for t in ctx['cible'] if t in SANS_CALCUL and t not in nc)} |")
    L += ["",
         "## Entrées et hypothèses", "",
         "- Besoins : tables a·M + b des phases 3a (`exigences_physiques`) et 3b (`simulations_marche`, "
         "référence prudente : par axe, le robot le plus exigeant parmi ceux dont la marche couvre le Froude). "
         "Par axe, le **maximum** des tâches du profil, à la vraie masse de la solution ; "
         f"`verifier_maximum` l'a recontrôlé sur {nverif} solutions.",
         f"- Marge : {f1(ctx['marge'])} sur les couples (fiche 0051). La vitesse à vide doit couvrir la vitesse de pointe, sans marge.",
         "- Structure : segment par segment (`scripts/structure_plaques.py`, reconstruction des études du "
         "2026-10-03 et 04 : caissons, liaisons à 90°, boîtes, étalonnés sur la CAO), à "
         f"{f1(s_['H_S'], 2)} m, puis × (H / {f1(s_['H_S'], 2)})^b. Par ensemble (kg, centrale / haute) : "
         + " ; ".join(f"{k} : {f1(s_['par_ensemble'][(k, 'central')], 2)} / {f1(s_['par_ensemble'][(k, 'haute')], 2)}"
                      for k in ENSEMBLES)
         + f". Charge utile {f1(s_['charge'])} kg (PROPOSÉE, `exigences_S.yaml`).",
         "- Régimes : charge, saisie, poussée, buste et tête au couple **continu** ; saut, relevé et gestes au "
         "couple de **pointe** ; la marche aux deux.",
         "- Place : taille minimale géométrique (`scripts/taille_minimale.py`, reconstruction de l'étude du "
         "2026-10-04), lecture AVEC ÉCARTS : les chaînes verticales qui débordent (jambe, tronc, cou et tête) "
         "s'allongent, la hauteur RÉELLE vaut H + dépassements ; la lecture ANSUR stricte est rapportée. **Couples à "
         "la hauteur réelle** (phase 4a ter) : lus au pas supérieur de la grille (5 cm, prudent) au-dessus de la "
         "hauteur réelle, structure à la hauteur réelle, masse minimale au pas inférieur ; itération (choix → place → "
         "hauteur) jusqu'à stabilité. Le robot allongé est traité comme un robot proportionné à sa hauteur réelle : "
         "centre de gravité et bras de levier y grandissent tous, ce qui majore les couples (prudent). Cheville à 2 "
         "axes : la meilleure des options (a), (b), (d).",
         "- Un axe absent de l'ensemble est rigide. Coût = actionneurs seuls (CHF HT, taux BCE de `budget.yaml`). "
         "Énergie de chute = M·g·(hauteur de hanche ANSUR × hauteur réelle).",
         f"- Actionneurs sans aucun couple publié, écartés : {len(ctx['ecartes'])}.", "",
         "| Ensemble | Axes | Source |", "| ---: | ---: | --- |"]
    for k, e in ENSEMBLES.items():
        L.append(f"| {k} | {sum(e['axes'].values())} | {e['source']} |")
    L += ["", "Familles du corps : " + ", ".join(EP.CORPS) + " ; petits axes (cou, pinces) : " + ", ".join(EP.PETITS)
          + ". L'invariant « famille RobStride » de la fiche 0069 n'est PAS appliqué ici : l'explorateur montre ce "
          "qu'il coûte.", "",
          "## Bilan", "",
          f"{len(sols)} solutions évaluées en {duree:.0f} s : {stat['faisable']} faisables, {stat['infaisable']} "
          f"infaisables, {stat['INCONNU']} INCONNUES. Par famille du corps :", "",
          "| Famille | Faisables | Infaisables | INCONNUES |", "| --- | ---: | ---: | ---: |"]
    for fc in EP.CORPS:
        c = Counter(s["statut"] for s in sols if s["fc"] == fc)
        L.append(f"| {fc} | {c['faisable']} | {c['infaisable']} | {c['INCONNU']} |")
    L += ["", "## Front de Pareto", "", f"![Front de Pareto]({SVG.name})", "",
          f"{len(front)} solutions non dominées (coût, masse, énergie de chute, capacités tenues, capacités voulues "
          "couvertes)."
          + (f" **Toutes sont à H = {f1(H_LAB[0], 2)} m, la borne BASSE de la plage du prompt** : plus petit est moins "
             "cher et plus léger tant que tout tient ; la plage n'a pas été étendue en dessous."
             if front and all(abs(s["H"] - H_LAB[0]) < 1e-9 for s in front) else ""), "",
          "## Les 5 meilleures solutions", "",
          "Classement PROPOSÉ : le moins de capacités voulues NON couvertes, puis le plus de capacités tenues, puis le "
          "moins cher, puis le plus léger, parmi le front. H = échelle des proportions ; « réelle » = avec les écarts.", ""]
    top = classement(front)[:5]
    L += table_top(top, detail=True)
    L += ["", "## Coût de chaque capacité", "",
          "Pour chaque tâche calculée du profil, et chaque niveau jusqu'au niveau visé : la solution faisable la moins "
          "chère sur tout l'espace (ensembles, H, familles), avec la marche au niveau du profil ; l'écart est pris au "
          "niveau inférieur (au premier niveau : à la marche seule). « H min » = la plus petite hauteur RÉELLE où une solution est faisable.", "",
          "**Lecture** : « le plus petit actionneur » est le plus LÉGER, pas le moins cher. Un niveau plus exigeant "
          "peut donc coûter MOINS (un actionneur plus lourd mais meilleur marché devient le plus petit qui passe) : "
          "un écart négatif n'est pas une erreur de calcul, c'est le prix de la légèreté.", ""]
    L += table_caps(ref, caps)
    L += ["", "## Données INCONNUES les plus bloquantes", "",
          "Rangées par le nombre de solutions INCONNUES où elles manquent ; « seule » = solutions qui deviendraient "
          "décidables avec cette seule donnée.", "", "| Donnée manquante | Solutions | Seule |", "| --- | ---: | ---: |"]
    for k, v, s1 in blocantes(sols, 12):
        L.append(f"| {k} | {v} | {s1} |")
    L += ["", "Hors calcul pour toute solution (capacités jamais « tenues » ici) :", ""]
    L += [f"- **{t}** : {r}" for t, r in SANS_CALCUL.items()]
    L += ["- **structure** : seule la jambe basse est dessinée ; les autres segments sont estimés par des formules "
          "étalonnées sur elle ; l'évidement est une borne haute ; l'alu 2 mm n'est pas confirmé chez l'opérateur.",
          "- **place** : volume de l'électronique et de la batterie dans le tronc compté NUL ; cardan des bielles (b) "
          "supposé ; servos en boîtier pris dans leur plus grande cote."]
    if ctx["manque"]:
        L += [f"- **séries** : {m}" for m in ctx["manque"]]
    if runs:
        L += section_electrique(ctx, runs, top0)
    return "\n".join(L) + "\n"


def section_electrique(ctx, runs, top0) -> list[str]:
    """Phases 4a quinquies et sexies : 12S (décidé) × 250 / 500 Hz × coupure, niveaux d'autonomie et d'IA, CAN, place."""
    import systeme_electrique as SE
    hyp = ctx["elec"]["hyp"]
    L = ["", "## Système électrique : 12S, 250 / 500 Hz, tension de coupure en variante (phases 4a quinquies et sexies)", "",
         "Contexte DÉCIDÉ : fiches 0070 (batterie), 0071 (Lab : autonomie 30 min sur le cycle 40 s de marche + 20 s "
         "debout, IA « commande + vision ») et 0072 (Jeremy, 2026-10-08 : « Je retiens le 12S pour les deux robots, sur "
         "les chiffres de l'explorateur du 7 octobre. »). La tension de COUPURE (seuil d'arrêt) est étudiée en variante : "
         "2,5, 3,0 et 3,2 V par cellule. Tout le reste est PROPOSÉ (`params/puissance.yaml`) :", "",
         f"- puissance électrique = puissance mécanique MOYENNE de la marche simulée (phase 3b, |τ·ω|, le robot le plus "
         f"exigeant qui couvre le Froude) ÷ rendement BAS {f1(hyp['rendement_actionneurs']['bas'])} (bande "
         f"{f1(hyp['rendement_actionneurs']['bas'])}–{f1(hyp['rendement_actionneurs']['haut'])}), sur 40 s de 60 ; debout, "
         "puissance mécanique nulle et pertes de maintien NON comptées (sous-estimation, dite) ; plus le calculateur ;",
         f"- énergie = puissance moyenne × autonomie ÷ {f1(hyp['fraction_utilisable']['valeur'])} (part utilisable) ; "
         "courant de pointe = Σ des pointes par axe (marche simulée et tâches directes du profil) ÷ rendement bas ÷ "
         "tension de COUPURE ;",
         f"- batterie : la composition S × P de cellules 21700 la plus LÉGÈRE du marché versé qui fournit l'énergie et "
         f"dont le courant CONTINU publié tient la pointe ; masse × {f1(hyp['facteur_pack_masse']['valeur'])}, volume des "
         f"cylindres ÷ π/4 × {f1(hyp['facteur_pack_volume']['valeur'])} ;",
         "- tension : chaque RobStride doit accepter le pack de la coupure à la pleine charge (plage publiée) ; sa vitesse "
         "à vide est ramenée à la tension de COUPURE, proportionnellement (hypothèse écrite ; fiche à 48 V) : ×"
         + " ; ×".join(f"{SE.variante(12, coupure=c)['Vfin'] / 48:.3f} à {f1(c)} V" for c in (2.5, 3.0, 3.2))
         + " ; énergie au-dessus de la coupure : " + " ; ".join(
             f"{f1(float(k))} V : {f1(v * 100, 0)} %" for k, v in hyp["energie_au_dessus_de_la_coupure"].items() if k != "statut")
         + " de l'énergie nominale (PROPOSÉ, prudent : courbe de décharge non lue numériquement) ;",
         "- calculateur : le moins cher qui convient au niveau d'IA (critères PROPOSÉS : "
         + " ; ".join(f"{k} : accélérateur {'oui' if v['accelerateur'] else 'non'}, ≥ {v['memoire_GB']} GB"
                      + (", modèles de langage" if v.get("modele_de_langage") else "")
                      for k, v in hyp["niveaux_ia"].items() if isinstance(v, dict))
         + "), carte porteuse comprise, alimenté par le rail 12 V (Raspberry Pi : 12 → 5 V) ;",
         "- bus : canaux CAN au calcul écrit (`docs/marche-bus-2026-10.md`), au-delà de ceux du calculateur par "
         "l'adaptateur le moins cher à pilote Linux principal ; un adaptateur série Feetech ;",
         "- chaîne de puissance et rails : `params/puissance.yaml` (cellules → fusible → sectionneur → BMS → contacteur → "
         "précharge → bus moteurs ; absorbeur de régénération ; arrêt d'urgence matériel ; rails 12, 7,4, 6 et 5 V). "
         "Masses et cotes non publiées : BORNES PROPOSÉES majorantes (`bornes_proposees`, justifiées une par une) ; une "
         "solution qui en use est marquée « bornes proposées », jamais « vérifiée » ;",
         "- batterie : cellules NEUVES d'un distributeur identifié seulement (récupération, occasion, marque masquée "
         "écartées) ;",
         f"- place : batterie, calculateur, cartes et convertisseurs dans {f1(hyp['remplissage_tronc']['valeur'] * 100, 0)} % "
         "du tronc (largeur d'épaules × profondeur de poitrine × hauteur du tronc, ANSUR, à la hauteur réelle) ; ce qui "
         "dépasse ALLONGE le tronc (même lecture « avec écarts » que la place des moteurs).", ""]
    if top0:
        x = top0[0]
        L += [f"**Référence, méthode de 14 h 05 recalculée (sans système électrique, charge utile forfaitaire de 1,2 kg)** : "
              f"{x['ens']} axes, {f1(x['H'], 2)} → {f1(x['H_reel'], 3)} m, {f1(x['M'])} kg, {f1(x['cout'], 0)} CHF "
              "(actionneurs seuls).", ""]
    # coupure × tâches rapides, meilleure RobStride (ajouté le 2026-10-08)
    L += ["### Tension de coupure et tâches rapides (meilleure solution RobStride pour chaque tâche, marche au niveau "
          "du profil)", "",
          "| Fréquence | Coupure (V/cellule) | " + " | ".join(n for n, _ in TACHES_COUPURE) + " |",
          "| ---: | ---: | " + " | ".join("---" for _ in TACHES_COUPURE) + " |"]
    for (S, f, c), R in runs.items():
        cell = []
        for nom, _ in TACHES_COUPURE:
            r = (R.get("taches_rs") or {}).get(nom) or {}
            b = r.get("best")
            if b:
                cell.append(f"tient : {b['ens']} axes, {f1(b['H_reel'], 3)} m réels, {f1(b['M'])} kg, "
                            f"{('≥ ' if b.get('borne') else '') + f1(b['cout'], 0)} CHF")
            else:
                top = r.get("viol", Counter()).most_common(1)
                cell.append("NE TIENT PAS" + (f" ({top[0][0][:90]})" if top else "")
                            if not r.get("n_inc") else f"INCONNU ({r['raisons'].most_common(1)[0][0][:80]})")
        L.append(f"| {f} Hz | {f1(c)} | " + " | ".join(cell) + " |")
    L.append("")
    for (S, f, c), R in runs.items():
        st = R["stat"]
        bas = all(abs(x["H"] - H_LAB[0]) < 1e-9 for x in R["top"]) if R["top"] else None
        L += [f"### {S}S, {f} Hz, coupure {f1(c)} V", "",
              f"{R['n']} solutions : {st['faisable']} faisables, {st['infaisable']} infaisables, {st['INCONNU']} "
              f"INCONNUES ; front de {R['front_n']}. "
              + ("Le front RESTE à la borne basse H = 0,50 m (proportions) ; la hauteur RÉELLE est en colonne."
                 if bas else "Le front QUITTE la borne basse H = 0,50 m." if bas is False else ""), "",
              ENTETE_ELEC[0], ENTETE_ELEC[1]] + [ligne_elec(x) for x in R["top"]]
        L += ["", "Meilleures solutions **RobStride** (famille des deux robots, fiche 0069), avec leurs capacités tenues :", "",
              ENTETE_ELEC[0], ENTETE_ELEC[1]] + [ligne_elec(x) for x in R["rs"]]
        L += [""] + [f"- RobStride n° {i} : {', '.join(x['profil'])} ; manque du profil : "
                     + (", ".join(t for t in ctx["cible"] if t not in x["profil"] and t not in ("autonomie", "ia_embarquee")) or "—")
                     for i, x in enumerate(R["rs"], 1)]
        b0 = R.get("base_niveaux")
        if b0 and (b0.get("elec") or {}).get("volumes"):
            el0, pl0 = b0["elec"], b0["elec"]["place"]
            L += ["", f"Volume électronique de la meilleure RobStride ({b0['ens']} axes, H {f1(b0['H'], 2)}) : "
                  f"{f1(el0['volume_connu'], 2)} L requis pour {f1(pl0['dispo_L'], 2)} L disponibles"
                  + (" (volume partiel : des cotes manquent)" if pl0.get("partielle") else "")
                  + f" ; le tronc s'allonge de {f1(pl0['allonge_m'] * 1000, 0)} mm.", "",
                  "| Élément | Volume (L) | Part |", "| --- | ---: | ---: |"]
            tot = el0["volume_connu"] or 1.0
            for nom, v in sorted(el0["volumes"], key=lambda t: -(t[1] or 0)):
                L.append(f"| {nom} | {f1(v, 3)} | {f1((v or 0) / tot * 100, 0)} % |")
        if R["niveaux"]:
            L += ["", f"Coût de chaque niveau d'autonomie et d'IA, pour la meilleure solution RobStride ({b0['ens']} axes, "
                  f"H {f1(b0['H'], 2)}, {b0['fc']} + {b0['fp']}, même profil) :", "",
                  "| Tâche | Niveau | Masse (kg) | Coût TOTAL (CHF HT) | Batterie | Calculateur | Hauteur réelle (m) | Statut |",
                  "| --- | --- | ---: | ---: | --- | --- | ---: | --- |"]
            for n in R["niveaux"]:
                r = n["r"] or {}
                el = r.get("elec") or {}
                b = el.get("batterie")
                L.append(f"| {n['tache']} | {n['niveau']} | {f1(r.get('M'))} | "
                         f"{(f1(r['cout'], 0) if r.get('cout') is not None else '≥ ' + f1(cout_borne(r), 0)) if r.get('statut') else '—'} | "
                         + (f"{b['S']}S{b['P']}P {f1(b['E'], 0)} Wh" if b else "—")
                         + f" | {(el.get('calc') or {}).get('nom', '—')} | {f1(r.get('H_reel'), 3)} | {r.get('statut', '—')} |")
        L.append("")
    # verrou de vitesse : RobStride à la coupure contre le saut du profil (calculé)
    niv = ctx["cible"].get("saut_vertical")
    if niv is not None:
        L += ["### Vitesse des RobStride à la tension de coupure", ""]
        for (S, f, c), R in runs.items():
            if f != VARIANTES[0][1]:
                continue
            vmax, besoin = R["vitesse"]["vmax"], R["vitesse"]["besoin"]
            L.append(f"- {S}S, coupure {f1(c)} V : le plus rapide des RobStride compatibles, {vmax[0]}, tourne à {f1(vmax[1])} rad/s à la "
                     f"coupure ; le saut de {niv} cm demande jusqu'à {f1(besoin)} rad/s à H = {f1(H_LAB[0], 2)} m (borne "
                     "haute : rampe linéaire). " + ("Le saut est donc HORS de portée des RobStride dans cette variante."
                                                   if vmax and besoin and vmax[1] < besoin else "Il passe.") if vmax and besoin
                     else f"- {S}S, coupure {f1(c)} V : non calculable")
        L += ["", "Deux hypothèses rendent ce verrou prudent : la vitesse à vide prise à la tension de COUPURE (et non "
              "nominale), et la vitesse du saut en rampe linéaire. Elles sont écrites ; c'est à Jeremy de dire si l'une "
              "doit être assouplie.", ""]
    L += ["### Canaux CAN (27 axes ; 23 sur CAN, le cou et les pinces étant en Feetech)", "",
          "| Fréquence | Protocole | 27 axes | 23 axes |", "| ---: | --- | ---: | ---: |"]
    for f in (250, 500):
        for et, nom in ((False, "MIT (trame standard)"), (True, "privé (trame étendue)")):
            L.append(f"| {f} Hz | {nom} | {SE.canaux_can(27, f, et)['canaux']} | {SE.canaux_can(23, f, et)['canaux']} |")
    return L


def table_top(top, detail=False):
    L = ["| # | Ensemble | H → réelle (m) | Corps + petits | Masse (kg) [bande] | H³ (kg) | Coût (CHF) | Chute (J) "
         "| Capacités tenues | Ne couvre pas |",
         "| ---: | ---: | --- | --- | --- | --- | ---: | ---: | --- | --- |"]
    for i, s in enumerate(top, 1):
        caps = ", ".join(t for t in s["profil"])
        L.append(f"| {i} | {s['ens']} | {f1(s['H'], 2)} → {f1(s['H_reel'], 3)} | {s['fc']} + {s['fp']} | {f1(s['M'])} "
                 f"[{f1(s['M_bande'][0])} ; {f1(s['M_bande'][1])}] | {f1(s['M_iso'])} "
                 f"({'tient' if s['tient_iso'] else 'ne tient pas'}) | {f1(s['cout'], 0)} | {f1(s['E'], 0)} | "
                 f"{s['ncap']} : {caps} | {', '.join(s['non_couvertes']) or '—'} |")
    if detail:
        for i, s in enumerate(top, 1):
            pl = s["place"]
            L += ["", f"**{i}.** statut {s['statut']} ; actionneurs : {resume_choix(s)}.",
                  f"Place : cheville ({pl['option']}), dépassements "
                  f"{', '.join(f'{k} +{v:.0f} mm' for k, v in pl['depassements'].items()) or 'aucun'} ; proportions "
                  f"ANSUR strictes : {'tient' if pl['tient_ansur'] else 'ne tient pas'} (il faudrait "
                  f"{f1(pl['H_min_ansur'], 3)} m, limité par : {pl['limitante_ansur']}).",
                  "Capacités voulues INCONNUES (non calculées) : " + (", ".join(s["cap_inconnues"]) or "aucune") + "."]
    return L


def table_caps(ref, caps):
    L = ["| Tâche | Niveau | Coût (CHF) | + CHF | Masse (kg) | + kg | Hauteur réelle de la moins chère | H min réelle | Note |",
         "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |"]
    b0 = ref["best"]
    L.append(f"| marche seule (référence) | {b0['profil']['marche_sol_plat'] if b0 else '—'} | "
             f"{('≥ ' if b0 and b0.get('borne') else '') + f1(b0 and b0['cout'], 0)} | — | {f1(b0 and b0['M'])} | — | {f1(b0 and b0['H_reel'], 3)} | "
             f"{f1(ref['hmin'], 3)} | |")
    for c in caps:
        r = c["res"]
        b = r["best"]
        p = c["prec"]["best"] if c["prec"] else None
        d = lambda k, n: (f"{'+' if b[k] >= p[k] else '−'}{f1(abs(b[k] - p[k]), n)}" if b and p else "—")
        note = ""
        if not b:
            if r["n_eval"] == 0:
                note = "aucun ensemble n'a les axes requis"
            elif r["n_inc"]:
                top = r["raisons"].most_common(1)[0][0]
                note = f"aucune faisable ; {r['n_inc']} INCONNUES (surtout : {top})"
            else:
                note = f"infaisable partout ({r['n_eval']} essais ; surtout : {r['viol'].most_common(1)[0][0]})"
        elif c["prec"] and not p:
            note = "niveau inférieur sans solution faisable"
        if b and b.get("borne"):
            note = (note + " ; " if note else "") + "≥ : chaîne de puissance incomplètement chiffrée"
        L.append(f"| {c['tache']} | {c['niveau']} | {('≥ ' if b and b.get('borne') else '') + f1(b and b['cout'], 0)} | {d('cout', 0)} | {f1(b and b['M'])} | "
                 f"{d('M', 1)} | {f1(b and b['H_reel'], 3)} | {f1(r['hmin'], 3)} | {note} |")
    return L


# 12S DÉCIDÉ (fiche 0072, Jeremy, 2026-10-08) ; 250 / 500 Hz × coupure 2,5 / 3,0 / 3,2 V par cellule (lot 4a sexies)
VARIANTES = [(12, f, c) for f in (250, 500) for c in (2.5, 3.0, 3.2)]
REFERENCE = (12, 500, 2.5)                                # PROPOSÉ : la variante détaillée (coût de chaque tâche)
TACHES_COUPURE = [("saut 5 cm", {"saut_vertical": 5}), ("saut 10 cm", {"saut_vertical": 10}),
                  ("gestes 2 m/s", {"gestes_pointage": 2.0})]


def classement_large(sols, n=5):
    """Les meilleures FAISABLES (front) ; complétées, s'il en manque, par les meilleures INCONNUES (marquées)."""
    top = classement(pareto(sols))[:n]
    if len(top) < n:
        inc = [x for x in sols if x["statut"] == "INCONNU"]
        borne = lambda x: x["cout"] if x["cout"] is not None else (x.get("cout_actionneurs") or 0) + ((x.get("elec") or {}).get("prix_connu") or 0)
        # les données manquantes du SYSTÈME ÉLECTRIQUE sont communes à toutes les solutions (même chaîne) : on départage
        # par celles qui sont PROPRES à la solution (actionneurs, place), puis par le coût connu
        propres = lambda x: len(set(x["inconnues"]) - set((x.get("elec") or {}).get("inconnues") or []))
        inc.sort(key=lambda x: (len(x.get("non_couvertes", [])), -x["ncap"], propres(x), x.get("cout_actionneurs") is None,
                                borne(x), x["M"]))
        top += inc[:n - len(top)]
    return top


def niveaux_elec(ctx, s) -> list[dict]:
    """La même solution (ensemble, H, familles, profil), réévaluée à chaque niveau d'autonomie et d'IA."""
    import systeme_electrique as SE
    cap, out = ctx["cap"], []
    for t in ("autonomie", "ia_embarquee"):
        for n in cap["taches"][t]["niveaux"]:
            c2 = dict(ctx, cible=dict(ctx["cible"], **{t: n}), memo={})
            el = dict(ctx["elec"], cible=c2["cible"])
            if t == "ia_embarquee":
                el["calc"] = SE.choisir_calculateur(SE.options_calculateur(), n, el["hyp"])
            c2["elec"] = el
            out.append(dict(tache=t, niveau=n, r=evaluer(c2, s["ens"], s["H"], s["fc"], s["fp"], s["profil"])))
    return out


def ligne_elec(s) -> str:
    el = s.get("elec") or {}
    b, c = el.get("batterie"), el.get("calc")
    cout = f1(s["cout"], 0) if s["cout"] is not None else "≥ " + f1((s.get("cout_actionneurs") or 0) + (el.get("prix_connu") or 0), 0)
    return (f"| {s['ens']} | {f1(s['H'], 2)} → {f1(s['H_reel'], 3)} | {s['fc']} + {s['fp']} | {f1(s['M'])} | {cout} | "
            f"{f1(s.get('cout_actionneurs'), 0)} | "
            + (f"{b['nom']} {b['S']}S{b['P']}P, {f1(b['E'], 0)} Wh, {f1(b['masse'], 2)} kg" if b else "—")
            + f" | {(c or {}).get('nom', '—')} | {el.get('n_can', '—')} | {s['statut']}"
            + (" (bornes proposées)" if el.get("bornes") else "") + " |")


ENTETE_ELEC = ("| Ensemble | H → réelle (m) | Corps + petits | Masse (kg) | Coût TOTAL (CHF HT) | dont actionneurs | "
               "Batterie | Calculateur | Canaux CAN | Statut |",
               "| ---: | --- | --- | ---: | ---: | ---: | --- | --- | ---: | --- |")


def vitesse_robstride(ctx) -> dict:
    """Le plus rapide des RobStride compatibles (vitesse à la coupure) et le besoin du saut du profil à la borne basse."""
    niv = ctx["cible"].get("saut_vertical")
    rs = [(a["id"], a["vitesse"]) for a in ctx["act"].get("robstride", []) if a["vitesse"] and a.get("compat")]
    besoin = max((w for (h, t, n), e in ctx["T"].items() if t == "saut_vertical" and n == niv and abs(h - H_LAB[0]) < 1e-9
                  for ax in e.values() for w in ax["w"]), default=None) if niv is not None else None
    return dict(vmax=max(rs, key=lambda x: x[1]) if rs else None, besoin=besoin)


def _executer(tache, cible, profil) -> dict:
    """Une exécution dans un processus : ne rend que ce qui sert au rapport (solutions complètes du haut du classement,
    comptes ; les solutions légères de la variante de référence, pour le bilan, le graphique et les inconnues)."""
    t1 = time.time()
    genre, S, f, c = tache
    ctx = (contexte(cible=cible, profil=profil) if genre == "reference"
           else contexte(cible=cible, profil=profil, S=S, f_can=f, coupure=c))
    sols = explorer(ctx, garder_leger=True)
    top = [complet(ctx, x) for x in classement_large(sols)]
    out = dict(n=len(sols), top=top, stat=Counter(x["statut"] for x in sols), front_n=len(pareto(sols)))
    if genre == "variante":
        rs = [complet(ctx, x) for x in classement_large([x for x in sols if x["fc"] == "robstride"], 3)]
        base = rs[0] if rs else (top[0] if top else None)
        marche = {"marche_sol_plat": ctx["cible"]["marche_sol_plat"]}
        out.update(rs=rs, niveaux=niveaux_elec(ctx, base) if base else [], base_niveaux=base, vitesse=vitesse_robstride(ctx),
                   taches_rs={nom: meilleure(ctx, dict(marche, **t), corps=["robstride"]) for nom, t in TACHES_COUPURE})
        if (S, f, c) == REFERENCE:
            out["sols"] = sols
    out["duree"] = time.time() - t1
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ecrire", action="store_true")
    ap.add_argument("--profil", default="lab", choices=["lab", "final"], help="profil de params/capacites.yaml")
    ap.add_argument("--cible", help="capacités voulues, « tâche[=niveau],… » (remplace le profil)")
    ap.add_argument("--sans-electrique", action="store_true", help="méthode de 14 h 05 : sans système électrique")
    a = ap.parse_args(argv)
    t0 = time.time()
    cible = None
    if a.cible:
        cap = lire("capacites.yaml")
        defaut = cible_defaut(cap, a.profil)
        cible = {}
        for x in a.cible.split(","):
            t, _, n = x.strip().partition("=")
            niv = cap["taches"][t]["niveaux"]
            cible[t] = next((v for v in niv if str(v) == n), None) if n else defaut[t]
            if cible[t] is None:
                ap.error(f"niveau « {n} » inconnu pour {t} : {niv}")
    # référence sans système électrique et variantes : un processus chacune (2026-10-08 : 8 cœurs)
    import concurrent.futures as CF
    import multiprocessing as MP
    taches = [("reference", None, None, None)] + [("variante", S, f, c) for S, f, c in VARIANTES]
    resultats = {}
    with CF.ProcessPoolExecutor(max_workers=min(len(taches), os.cpu_count() or 1),
                                mp_context=MP.get_context("fork")) as pool:
        futurs = {pool.submit(_executer, t, cible, a.profil): t for t in taches}
        for fu in CF.as_completed(futurs):
            t = futurs[fu]
            resultats[t] = fu.result()
            print(f"  {t[0]} {t[1] or ''}{'S' if t[1] else ''} {t[2] or ''}{' Hz' if t[2] else ''} {t[3] or ''}{' V' if t[3] else ''} : "
                  f"terminée en {resultats[t]['duree']:.0f} s", flush=True)
    top0 = resultats[("reference", None, None, None)]["top"]
    print(f"  sans système électrique (méthode de 14 h 05) : {resultats[('reference', None, None, None)]['n']} solutions ; "
          "meilleure : " + (f"{top0[0]['ens']} axes, {top0[0]['H']:.2f} → {top0[0]['H_reel']:.3f} m, {top0[0]['M']:.1f} kg, "
                            f"{top0[0]['cout']:.0f} CHF" if top0 else "aucune"))
    if a.sans_electrique:
        return 0
    runs = {}
    for S, f, c in VARIANTES:
        R = runs[(S, f, c)] = resultats[("variante", S, f, c)]
        st = R["stat"]
        print(f"\n  {S}S, {f} Hz, coupure {c} V : {R['n']} solutions ({st['faisable']} faisables, {st['infaisable']} "
              f"infaisables, {st['INCONNU']} INCONNUES) en {R['duree']:.0f} s ; front {R['front_n']}")
        print("  " + ENTETE_ELEC[0] + "\n  " + ENTETE_ELEC[1])
        for x in R["top"]:
            print("  " + ligne_elec(x))
        print("  meilleures RobStride (fiche 0069) :")
        for x in R["rs"]:
            print("  " + ligne_elec(x) + f" capacités : {', '.join(x['profil'])}")
    R = runs[REFERENCE]
    sols = R["sols"]
    ctx = contexte(cible=cible, profil=a.profil, S=REFERENCE[0], f_can=REFERENCE[1], coupure=REFERENCE[2])
    front = [complet(ctx, x) for x in pareto(sols)]
    nverif, fautes = 0, []
    for x in front + [complet(ctx, y) for y in [y for y in sols if y["statut"] != "infaisable"][:: 97]]:
        if "besoins" in x:
            fautes += verifier_maximum(x["besoins"], ctx["T"], x["H_couples"], x["profil"], x["M"])
            nverif += 1
    ref, caps = cout_capacites(ctx)
    print(f"\n  maximum vérifié sur {nverif} solutions : {len(fautes)} écart(s)")
    print("\n".join(table_caps(ref, caps)))
    print("\n  | Donnée manquante | Solutions | Seule |")
    for k, v, s1 in blocantes(sols, 10):
        print(f"  | {k} | {v} | {s1} |")
    if a.ecrire:
        DOC.write_text(rapport(ctx, sols, front, ref, caps, nverif, time.time() - t0, runs=runs, top0=top0),
                       encoding="utf-8")
        SVG.write_text(svg(front, sols), encoding="utf-8")
        print(f"  -> {DOC.relative_to(REPO)}, {SVG.relative_to(REPO)}")
    return 1 if fautes else 0


if __name__ == "__main__":
    sys.exit(main())
