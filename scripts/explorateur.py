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
     lois_masse.yaml) : le choix doit tenir au b bas, central ET haut ; H³ est
     rapporté comme borne pessimiste, sans filtrer ;
  4. statut : faisable / infaisable (contraintes violées, listées) / INCONNU
     (données manquantes, listées comme mesures à faire). Une donnée absente
     n'est JAMAIS estimée : elle rend la solution INCONNUE.

Front de Pareto (tri maison, sans dépendance : réponse de Jeremy du
2026-10-07, « Non, Pareto maison ») sur coût, masse, énergie de chute et nombre
de capacités tenues, parmi les solutions faisables.

HYPOTHÈSES, toutes PROPOSÉES par Claude et écrites ici (aucune cachée) :
  · ENSEMBLES : 26 = squelette v3 (params/squelette.yaml) ; 27 = fiche 0069
    (proposition de Claude) ; 25 et 29 RECONSTRUITS, l'étude de session du
    2026-10-04 n'ayant jamais été versée (voir ENSEMBLES) ;
  · PLACE : l'étude H_min du 2026-10-04 n'a pas été versée non plus. Règle
    SIMPLIFIÉE à la place : deux actionneurs aux deux bouts d'un segment ne se
    chevauchent pas, (Ø_a + Ø_b)/2 + jeu ≤ longueur ANSUR × H (PLACE) ;
  · STRUCTURE : masse Winter de la structure du modèle de S × facteur des
    plaques (masse CAO des plaques alu de la jambe basse / part Winter du
    tibia et du pied : UN seul segment mesuré), puis × (H / H_S)^b ;
  · RÉGIME : les tâches tenues (charge, saisie, poussée, buste, tête) se
    comparent au couple CONTINU ; les gestes brefs (saut, relevé, gestes) au
    couple de POINTE ; la marche aux deux (REGIME) ;
  · un axe absent de l'ensemble est RIGIDE : la structure reprend son couple ;
  · énergie de chute = M·g·h, h = hauteur de hanche ANSUR × H ;
  · coût = Σ prix des actionneurs seulement (structure non chiffrée) ;
  · la marche est toujours dans le profil (niveau le plus bas au moins) : un
    bipède qui ne marche pas n'est pas une solution.
"""
from __future__ import annotations

import argparse
import itertools
import math
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
H_LAB = [h for h in EP.HS if 0.50 - 1e-9 <= h <= 0.80 + 1e-9]   # non-cote: plage du prompt (m)
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
             source="RECONSTRUIT (étude du 2026-10-04 non versée) : v3 sans le roulis de taille"),
    26: dict(axes=_ens(JAMBE5, ["waist_yaw", "waist_roll"]),
             source="squelette v3 (params/squelette.yaml, fiche 0068 : 5 axes par jambe)"),
    27: dict(axes=_ens(JAMBE5 + ["ankle_roll"], ["waist_yaw"]),
             source="fiche 0069 (proposition de Claude) : jambes 6 × 2, taille 1, bras 5 × 2, pinces, cou 2"),
    29: dict(axes=_ens(JAMBE5 + ["ankle_roll"], ["waist_yaw", "waist_roll", "waist_pitch"]),
             source="RECONSTRUIT (étude du 2026-10-04 non versée) : le 27 avec la taille à 3 axes"),
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
# lignes de place : (segment ANSUR, axe à un bout, axe à l'autre bout)
PLACE = [("largeur_bassin", "hip_yaw", "hip_yaw"), ("cuisse", "hip_pitch", "knee"), ("tibia", "knee", "ankle_pitch"),
         ("bras", "shoulder_roll", "elbow_roll"), ("avant_bras", "elbow_roll", "wrist_pitch")]

A_PLACE = {x for _, a, b in PLACE for x in (a, b)}


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
    return yaml.safe_load((REPO / "params" / nom).read_text(encoding="utf-8"))


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
    for t, niv in profil.items():
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
    axes = {ax for t, niv in profil.items() for ax in T.get((round(H, 2), t, niv), {})} | set(bes)
    for ax in axes:
        ent = [T.get((round(H, 2), t, niv), {}).get(ax) for t, niv in profil.items()]
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
    fam, rows = MA.charger()
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
            prix=EP.prix_chf(r["prix"], taux, D), D=diametre(r["dims"])))
    for l in par.values():
        l.sort(key=lambda a: (a["masse"] is None, a["masse"] or 0.0, a["pointe"]))
    return par, ecartes, fam


def passe(a, need, marge) -> bool:
    """Les critères CONNUS sont tenus (un critère inconnu ne fait ni passer ni échouer : il est rendu)."""
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
        if not inconnues_de(a, need) and not (cotes and a["D"] is None):
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
        out.append(f"vitesse à vide de {a['id']}")
    if a["masse"] is None:
        out.append(f"masse de {a['id']}")
    if a["prix"] is None:
        out.append(f"prix de {a['id']}")
    return out


# ─────────────────────────────── contexte ───────────────────────────────
def facteur_plaques() -> dict:
    """Masse CAO des plaques alu de la jambe basse / part Winter du tibia et du pied (≈ 22 s de CAO)."""
    sys.path.insert(0, str(REPO / "parts"))
    import jambe_basse as J
    import squelette as SQ
    rid = "operateur_cn_alu_3"
    g = J.donnees(rid)
    Gm = J.geometrie(g)
    P = J.plaques_structure(g, Gm)
    for pl in P:
        pl.finir(g["e"], g["d_min"])
    dens = J.lire("hardware.yaml")["matieres"][g["reg"]["matiere"]]["densite"]
    m = sum(pl.solide.volume * len(pl.poses) for pl in P) * dens / 1e6          # kg
    sq = SQ.construire()
    part = sq["segs"]["left_tibia"]["masse"] + sq["segs"]["left_pied"]["masse"]
    return dict(k=m / part, plaques_kg=m, part_kg=part, m_struct_S=sq["m_struct"], H_S=sq["H"], charge=sq["charge"],
                reglage=rid)


def contexte(struct=None) -> dict:
    import simulations_marche as SM
    cap, an, lignes = EP.tout()
    marches, releve, manque = SM.charger()
    lm = lire("lois_masse.yaml")
    ex = dict(lm["variantes"]["allometrique"]["exposant"], iso=lm["variantes"]["isometrique"]["exposant"])
    par, ecartes, fams = catalogue()
    sq = lire("squelette.yaml")
    return dict(cap=cap, an=an, R={k: v["valeur"] for k, v in an["ratios"].items()},
                T=table_besoins(lignes, marches, releve, cap), manque=manque,
                C={H: EP.contraintes(H, cap, an) for H in H_LAB}, ex=ex, decision=lm.get("retenue"),
                act=par, ecartes=ecartes, fams=fams, struct=struct or facteur_plaques(),
                marge=lire("actionneurs.yaml")["dimensionnement"]["marge"],
                jeu=sq["ecarts_ansur"]["cheville"]["jeu_mm"]["valeur"],
                fr_max=max((e["Fr"] for e in marches.values()), default=0.0), memo={})


def masse_structure(ctx, H, b):
    s = ctx["struct"]
    return s["m_struct_S"] * s["k"] * (H / s["H_S"]) ** b


# ─────────────────────────────── évaluation ─────────────────────────────
def evaluer(ctx, ens, H, fc, fp, profil) -> dict | None:
    """Une solution. None si le profil demande un axe que l'ensemble n'a pas (capacité sans objet)."""
    axes = ENSEMBLES[ens]["axes"] if isinstance(ens, int) else ens
    for t, niv in profil.items():
        if any(a not in axes for a in axes_requis(t, niv)):
            return None
    fam_de = {a: (fp if a in PETITS_AXES else fc) for a in axes}
    acts = {a: ctx["act"].get(fam_de[a], []) for a in axes}
    inconnues, violees = [], []
    for t, niv in profil.items():
        if (round(H, 2), t, niv) not in ctx["T"]:
            inconnues.append(f"{t} {niv} : aucun besoin calculé à H = {f1(H, 2)} m"
                             + (" (Froude au-delà des marches simulées)" if t == "marche_sol_plat" else ""))
    for a in axes:
        if not acts[a]:
            violees.append(f"{a} : famille {fam_de[a]} vide au catalogue")
    if violees:
        return dict(statut="infaisable", violees=violees, inconnues=inconnues)
    mfix = lambda b: masse_structure(ctx, H, ctx["ex"][b]) + ctx["struct"]["charge"]
    idx = {a: 0 for a in axes}
    M = {}
    for _ in range(40):                                      # point fixe : masse ↔ choix
        change = False
        for b in BANDE:
            M[b] = mfix(b) + sum(n * (acts[a][idx[a]]["masse"] or 0.0) for a, n in axes.items())
            bes = besoins(ctx["T"], H, profil, M[b])
            for a in axes:
                need = bes.get(a, dict(pk=0.0, c=0.0, w=0.0))
                cle = (fam_de[a], idx[a], round(need["pk"], 3), round(need["c"], 3), round(need["w"], 2), a in A_PLACE)
                if cle not in ctx["memo"]:
                    ctx["memo"][cle] = choisir(acts[a], need, ctx["marge"], idx[a], a in A_PLACE)
                i = ctx["memo"][cle]
                if i is None:
                    violees.append(f"{a} : aucun {fam_de[a]} ne tient (pointe {need['pk']:.2f}, continu "
                                   f"{need['c']:.2f} N·m, ω {need['w']:.1f} rad/s, b {b}, marge {ctx['marge']})")
                    return dict(statut="infaisable", violees=violees, inconnues=inconnues)
                if i > idx[a]:
                    idx[a], change = i, True
        if not change:
            break
    choix = {a: acts[a][idx[a]] for a in axes}
    bes = {b: besoins(ctx["T"], H, profil, M[b]) for b in BANDE}
    for b in BANDE:                                           # masses minimales (équilibre, frottement)
        for t, niv in profil.items():
            mmin = ctx["C"].get(H, {}).get((t, niv))
            if mmin and M[b] < mmin:
                violees.append(f"{t} {niv} : M = {M[b]:.1f} kg < {mmin:.1f} kg (équilibre ou frottement, b {b})")
    for seg, x, y in PLACE:                                   # place (règle simplifiée)
        if x in choix and y in choix:
            da, db = choix[x]["D"], choix[y]["D"]
            if da is None or db is None:
                inconnues += [f"cotes de {c['id']}" for c in (choix[x], choix[y]) if c["D"] is None]
            elif (da + db) / 2 + ctx["jeu"] > ctx["R"][seg] * H * 1000:
                violees.append(f"place : {x}/{y} (Ø{da:g}, Ø{db:g}) ne tiennent pas sur {seg} "
                               f"({ctx['R'][seg] * H * 1000:.0f} mm)")
    for a, c in choix.items():
        need = {k: max(bes[b].get(a, {}).get(k, 0.0) for b in BANDE) for k in ("pk", "c", "w")}
        inconnues += inconnues_de(c, need)
    inconnues = list(dict.fromkeys(inconnues))
    prix = [c["prix"] for c in choix.values()]
    cout = sum(n * choix[a]["prix"] for a, n in axes.items()) if None not in prix else None
    # borne pessimiste H³ : le même choix tient-il ?
    M_iso = mfix("iso") + M["central"] - mfix("central")
    b_iso = besoins(ctx["T"], H, profil, M_iso)
    tient_iso = all(c["pointe"] >= ctx["marge"] * b_iso.get(a, {}).get("pk", 0)
                    and (c["continu"] is None or c["continu"] >= ctx["marge"] * b_iso.get(a, {}).get("c", 0))
                    for a, c in choix.items())
    statut = "infaisable" if violees else ("INCONNU" if inconnues else "faisable")
    return dict(statut=statut, violees=violees, inconnues=inconnues, choix=choix, M=M["central"],
                M_bande=(M["bas"], M["haut"]) if H >= ctx["struct"]["H_S"] else (M["haut"], M["bas"]),
                M_iso=M_iso, tient_iso=tient_iso, cout=cout,
                E=M["central"] * G * ctx["R"]["hauteur_hanche"] * H, ncap=len(profil),
                n_axes=sum(axes.values()), besoins=bes["central"])


def niveau_bas(cap, t):
    return cap["taches"][t]["niveaux"][0]


def explorer(ctx, ensembles=None, hs=None, corps=None, petits=None):
    """Toutes les solutions : chaque sous-ensemble des tâches optionnelles, au niveau le plus bas.

    Un niveau plus haut ne change pas le nombre de capacités tenues et coûte au
    moins autant : il ne peut pas être sur le front. Il est chiffré à part
    (`cout_capacites`)."""
    cap = ctx["cap"]
    base = {"marche_sol_plat": niveau_bas(cap, "marche_sol_plat")}
    out = []
    for k in range(len(OPTIONNELLES) + 1):
        for sub in itertools.combinations(OPTIONNELLES, k):
            profil = dict(base, **{t: niveau_bas(cap, t) for t in sub})
            for ens in (ensembles or ENSEMBLES):
                for H in (hs or H_LAB):
                    for fc in (corps or EP.CORPS):
                        for fp in (petits or EP.PETITS):
                            r = evaluer(ctx, ens, H, fc, fp, profil)
                            if r:
                                out.append(dict(r, ens=ens, H=H, fc=fc, fp=fp, profil=profil))
    return out


def pareto(sols):
    """Non dominées sur (coût ↓, masse ↓, énergie de chute ↓, capacités ↑), parmi les faisables."""
    f = [s for s in sols if s["statut"] == "faisable"]
    f.sort(key=lambda s: (s["cout"], s["M"], s["E"], -s["ncap"]))
    front = []
    for s in f:
        v = (s["cout"], s["M"], s["E"], -s["ncap"])
        domine = False
        for p in front:
            w = (p["cout"], p["M"], p["E"], -p["ncap"])
            if all(x <= y for x, y in zip(w, v)) and w != v:
                domine = True
                break
            if w == v:
                domine = True                                # doublon exact : un seul représentant
                break
        if not domine:
            front.append(s)
    return front


def meilleure(ctx, profil):
    """La solution faisable la moins chère pour un profil, sur tout l'espace ; et la plus petite H faisable."""
    best, hmin, n_inc, raisons, n_eval, viol = None, None, 0, Counter(), 0, Counter()
    for ens in ENSEMBLES:
        for H in H_LAB:
            for fc in EP.CORPS:
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
                        hmin = H if hmin is None else min(hmin, H)
                    elif r["statut"] == "INCONNU":
                        n_inc += 1
                        raisons.update(r["inconnues"])
    return dict(best=best, hmin=hmin, n_inc=n_inc, raisons=raisons, n_eval=n_eval, viol=viol)


def cout_capacites(ctx):
    """Pour chaque tâche et niveau : la meilleure solution, et l'écart au niveau inférieur (0 = tâche absente)."""
    cap = ctx["cap"]
    base = {"marche_sol_plat": niveau_bas(cap, "marche_sol_plat")}
    ref = meilleure(ctx, base)
    out = []
    for t in ["marche_sol_plat"] + OPTIONNELLES:
        prec = None if t == "marche_sol_plat" else ref
        for niv in cap["taches"][t]["niveaux"]:
            profil = dict(base, **{t: niv})
            r = meilleure(ctx, profil)
            out.append(dict(tache=t, niveau=niv, res=r, prec=prec))
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
    return sorted(front, key=lambda s: (-s["ncap"], s["cout"], s["M"]))


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


def rapport(ctx, sols, front, ref, caps, nverif, duree) -> str:
    s_ = ctx["struct"]
    ex = ctx["ex"]
    stat = Counter(s["statut"] for s in sols)
    L = ["# Explorateur : YXOR Lab", "",
         "**Engendré** par `.venv/bin/python scripts/explorateur.py --ecrire`. Ne pas éditer à la main. "
         "**Étude, aucune décision d'architecture** (phase 4a, fiche 0069).", "",
         "## Loi de masse", "",
         f"DÉCIDÉE par Jeremy le 2026-10-07 (`params/lois_masse.yaml`, `retenue`) : {ctx['decision']['decide']}", "",
         f"Une solution n'est **faisable** que si elle tient aux trois exposants b = {f1(ex['bas'], 3)}, "
         f"{f1(ex['central'], 3)} et {f1(ex['haut'], 3)}. La masse est donnée au b central. H³ (b = {ex['iso']:g}) "
         "est rapporté comme borne pessimiste, sans filtrer.", "",
         "## Entrées et hypothèses", "",
         "- Besoins : tables a·M + b des phases 3a (`exigences_physiques`) et 3b (`simulations_marche`, "
         "référence prudente : par axe, le robot le plus exigeant parmi ceux dont la marche couvre le Froude). "
         "Par axe, le **maximum** des tâches du profil, à la vraie masse de la solution ; "
         f"`verifier_maximum` l'a recontrôlé sur {nverif} solutions.",
         f"- Marge : {f1(ctx['marge'])} sur les couples (fiche 0051). La vitesse à vide doit couvrir la vitesse de pointe, sans marge.",
         f"- Structure : {f1(s_['m_struct_S'], 3)} kg (part Winter du modèle de S, {f1(s_['H_S'], 2)} m) × facteur des plaques "
         f"**{f1(s_['k'], 2)}** (plaques alu de la jambe basse, CAO, {s_['plaques_kg'] * 1000:.0f} g, contre "
         f"{s_['part_kg'] * 1000:.0f} g de part Winter du tibia et du pied), puis × (H / {f1(s_['H_S'], 2)})^b. "
         "**Un seul segment mesuré** : le facteur est étendu à toute la structure (hypothèse). "
         f"Charge utile {f1(s_['charge'])} kg (PROPOSÉE, `exigences_S.yaml`).",
         "- Régimes : charge, saisie, poussée, buste et tête au couple **continu** ; saut, relevé et gestes au "
         "couple de **pointe** ; la marche aux deux.",
         f"- Place (règle SIMPLIFIÉE, l'étude H_min du 2026-10-04 n'a pas été versée) : (Ø_a + Ø_b)/2 + "
         f"{ctx['jeu']:g} mm ≤ longueur ANSUR × H, sur "
         + ", ".join(f"{seg} ({x}/{y})" for seg, x, y in PLACE) + ".",
         "- Un axe absent de l'ensemble est rigide. Coût = actionneurs seuls (CHF HT, taux BCE de `budget.yaml`). "
         "Énergie de chute = M·g·(hauteur de hanche ANSUR × H).",
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
          f"{len(front)} solutions non dominées (coût, masse, énergie de chute, nombre de capacités tenues)."
          + (f" **Toutes sont à H = {f1(H_LAB[0], 2)} m, la borne BASSE de la plage du prompt** : plus petit est moins "
             "cher et plus léger tant que tout tient ; la plage n'a pas été étendue en dessous."
             if front and all(abs(s["H"] - H_LAB[0]) < 1e-9 for s in front) else ""), "",
          "## Les 5 meilleures solutions", "",
          "Classement PROPOSÉ : le plus de capacités, puis le moins cher, puis le plus léger, parmi le front.", ""]
    L += table_top(classement(front)[:5], detail=True)
    L += ["", "## Coût de chaque capacité", "",
          "Pour chaque tâche et chaque niveau : la solution faisable la moins chère sur tout l'espace (ensembles, H, "
          "familles), avec la marche au niveau le plus bas ; l'écart est pris au niveau inférieur (au premier "
          "niveau : à la marche seule). « H min » = la plus petite taille où une solution est faisable.", "",
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
    L += [f"- **structure** : facteur des plaques mesuré sur un seul segment ; les autres segments (cuisse, bassin, "
          "tronc, bras) restent à dessiner pour être pesés."]
    if ctx["manque"]:
        L += [f"- **séries** : {m}" for m in ctx["manque"]]
    return "\n".join(L) + "\n"


def table_top(top, detail=False):
    L = ["| # | Ensemble | H (m) | Corps + petits | Masse (kg) [bande] | H³ (kg) | Coût (CHF) | Chute (J) | Capacités |",
         "| ---: | ---: | ---: | --- | --- | --- | ---: | ---: | --- |"]
    for i, s in enumerate(top, 1):
        caps = ", ".join(t for t in s["profil"])
        L.append(f"| {i} | {s['ens']} | {f1(s['H'], 2)} | {s['fc']} + {s['fp']} | {f1(s['M'])} [{f1(s['M_bande'][0])} ; "
                 f"{f1(s['M_bande'][1])}] | {f1(s['M_iso'])} ({'tient' if s['tient_iso'] else 'ne tient pas'}) | "
                 f"{f1(s['cout'], 0)} | {f1(s['E'], 0)} | {s['ncap']} : {caps} |")
    if detail:
        for i, s in enumerate(top, 1):
            L += ["", f"**{i}.** statut {s['statut']} ; actionneurs : {resume_choix(s)}.",
                  "Reste INCONNU : " + ("; ".join(SANS_CALCUL) + " (capacités non calculées) ; "
                                         "facteur de structure sur un seul segment ; place par la règle simplifiée.")]
    return L


def table_caps(ref, caps):
    L = ["| Tâche | Niveau | Coût (CHF) | + CHF | Masse (kg) | + kg | H de la moins chère | H min | Note |",
         "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |"]
    b0 = ref["best"]
    L.append(f"| marche seule (référence) | {b0['profil']['marche_sol_plat'] if b0 else '—'} | "
             f"{f1(b0 and b0['cout'], 0)} | — | {f1(b0 and b0['M'])} | — | {f1(b0 and b0['H'], 2)} | "
             f"{f1(ref['hmin'], 2)} | |")
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
        L.append(f"| {c['tache']} | {c['niveau']} | {f1(b and b['cout'], 0)} | {d('cout', 0)} | {f1(b and b['M'])} | "
                 f"{d('M', 1)} | {f1(b and b['H'], 2)} | {f1(r['hmin'], 2)} | {note} |")
    return L


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ecrire", action="store_true")
    a = ap.parse_args(argv)
    t0 = time.time()
    ctx = contexte()
    if not ctx["T"]:
        print("  explorateur SAUTÉ : aucune table de besoins")
        return 0
    sols = explorer(ctx)
    duree = time.time() - t0
    front = pareto(sols)
    nverif, fautes = 0, []
    for s in front + [x for x in sols if x["statut"] != "infaisable"][:: 97]:
        if "besoins" in s:
            fautes += verifier_maximum(s["besoins"], ctx["T"], s["H"], s["profil"], s["M"])
            nverif += 1
    ref, caps = cout_capacites(ctx)
    stat = Counter(s["statut"] for s in sols)
    print(f"  explorateur : {len(sols)} solutions ({stat['faisable']} faisables, {stat['infaisable']} infaisables, "
          f"{stat['INCONNU']} INCONNUES) en {duree:.0f} s ; front {len(front)} ; maximum vérifié sur {nverif} : "
          f"{len(fautes)} écart(s) ; structure × {ctx['struct']['k']:.2f}")
    for f in fautes[:5]:
        print(f"     ✗ {f}")
    print("\n".join(table_top(classement(front)[:5])))
    print()
    print("\n".join(table_caps(ref, caps)))
    print("\n  | Donnée manquante | Solutions | Seule |")
    for k, v, s1 in blocantes(sols, 10):
        print(f"  | {k} | {v} | {s1} |")
    if a.ecrire:
        DOC.write_text(rapport(ctx, sols, front, ref, caps, nverif, duree), encoding="utf-8")
        SVG.write_text(svg(front, sols), encoding="utf-8")
        print(f"  -> {DOC.relative_to(REPO)}, {SVG.relative_to(REPO)}")
    return 1 if fautes else 0


if __name__ == "__main__":
    sys.exit(main())
