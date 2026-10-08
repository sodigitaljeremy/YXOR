#!/usr/bin/env python3
"""Étude de YXOR Kit : structure en carton, modules successifs, couples, servos, masse, coût, réutilisation au Lab.

    .venv/bin/python scripts/kit.py            # résumé
    .venv/bin/python scripts/kit.py --ecrire   # docs/kit-etude-2026-10.md

Créé le 2026-10-08 (prompt « Étude de YXOR Kit »). DÉCIDÉ (fiche 0074, Jeremy) :
modules successifs ; mêmes dimensions, taille et composants que le Lab ; carton ;
outils du ménage. PROPOSÉ : les niveaux (params/capacites.yaml, profils.kit.modules)
et toutes les hypothèses de params/kit.yaml. Rien n'est choisi ni acheté (fiche 0066).

Méthode :
  · STRUCTURE : une coque fermée (boîte) par segment du squelette (params/squelette.yaml,
    ratios × H_S) ; les segments qui logent un servo ont une section d'au moins
    l'encombrement du plus grand servo Feetech + deux parois ; masse = aire × masse
    surfacique du carton × facteur de renforts. Dimensionnée dès le niveau 0 pour le niveau 3.
  · COUPLES : le MAXIMUM de (a) l'explorateur (tables des phases 3a et 3b, τ = a·M + b à la
    masse M du Kit à ce niveau) et (b) un calcul statique direct sur les masses réelles
    (bras tendu à l'horizontale, tête basculée) ; marge de la fiche 0051 en plus.
  · SERVOS : le plus léger servo Feetech qui passe (même règle que l'explorateur : pointe,
    continu, vitesse ramenée à la tension d'alimentation, plage de tension) ; la masse et le
    choix se recalculent jusqu'à se stabiliser.
  · S'IL N'Y A PAS de Feetech : le plus léger RobStride qui passe (le niveau 4, avancé).
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
DOC = REPO / "docs" / "kit-etude-2026-10.md"
G = 9.80665
UNIQUES = ("bassin", "tronc", "tete")                     # les autres segments vont par paire (gauche, droite)
COTES = {"hip_yaw", "hip_roll", "hip_pitch", "knee", "ankle_pitch", "shoulder_pitch", "shoulder_roll",
         "shoulder_yaw", "elbow_roll", "elbow_yaw", "wrist_pitch", "wrist_roll"}


def lire(nom):
    import marche_composants as MC
    return MC.lire(nom)


def f1(x, n=1):
    return "—" if x is None else f"{x:,.{n}f}".replace(",", " ").replace(".", ",")


def contexte() -> dict:
    an = lire("anthropometry.yaml")
    kit = lire("kit.yaml")
    return dict(an=an, kit=kit, cap=lire("capacites.yaml"), sq=lire("squelette.yaml"),
                H=kit["lab"]["H_m"], rallonge=kit["lab"]["hauteur_reelle_m"] - kit["lab"]["H_m"],
                R={k: v["valeur"] for k, v in an["ratios"].items()},
                marge=lire("actionneurs.yaml")["dimensionnement"]["marge"],
                taux=lire("budget.yaml")["taux_de_change"])


def modules(ctx) -> list[dict]:
    return ctx["cap"]["profils"]["kit"]["modules"]


# ─────────────────────────────── carton ─────────────────────────────────
def carton_reference(ctx) -> dict:
    """La matière de référence de params/kit.yaml, depuis params/hardware.yaml (valeurs MESURÉES, 2026-09-29)."""
    nom = ctx["kit"]["structure"]["carton_reference"]
    m = lire("hardware.yaml")["matieres"][nom]
    return dict(id=nom, sigma=m["masse_surfacique"] * 1000.0, e=m["epaisseur"], source="mesuré (params/mesures.yaml)")


def cartons(ctx) -> list[dict]:
    """La référence mesurée, puis les produits de params/cartons.yaml (étude de marché du 2026-10-08) dont
    l'épaisseur et la masse surfacique sont lues."""
    out = [carton_reference(ctx)]
    p = REPO / "params" / "cartons.yaml"
    if p.exists():
        for pid, c in (lire("cartons.yaml").get("produits") or {}).items():
            s, e = c.get("masse_surfacique_g_m2"), c.get("epaisseur_mm")
            if s and e:
                out.append(dict(id=pid, sigma=float(s), e=float(e), source=f"marché ({c.get('famille')})"))
    return out


def classement_cartons(ctx, aire_m2: float) -> dict:
    """Critères PROPOSÉS de params/kit.yaml (cartons) : éliminatoires, puis rang par e²/σ (proxy de la rigidité en
    flexion par masse), masse de la structure, prix. `aire_m2` : aire de carton du Kit, renforts compris."""
    cr = ctx["kit"]["cartons"]["eliminatoires"]
    cands = [dict(carton_reference(ctx), famille="ondule_double", prix_m2=None, dispo="récupération (carton mesuré)",
                  nom="carton ondulé double de récupération, mesuré le 2026-09-29")]
    for pid, c in (lire("cartons.yaml").get("produits") or {}).items():
        cands.append(dict(id=pid, nom=c.get("nom"), famille=c["famille"], sigma=c.get("masse_surfacique_g_m2"),
                          e=c.get("epaisseur_mm"), prix_m2=(c.get("prix") or {}).get("par_m2_CHF"),
                          dispo=str(c.get("dispo_suisse") or ""), source="marché"))
    retenus, elimines, a_peser = [], [], []
    for c in cands:
        pourquoi = None
        if c["famille"] not in cr["familles_papier"] and c["id"] not in cr["papier_hors_famille"]:
            pourquoi = "pas en filière papier mono-matière"
        elif c["id"] in cr["simple_face"]:
            pourquoi = "simple face : pas un panneau"
        elif c["dispo"].lower().startswith("non établi"):
            pourquoi = "disponibilité en Suisse non établie"
        elif c["dispo"].lower().startswith("non"):
            pourquoi = "pas disponible en Suisse"
        if pourquoi:
            elimines.append(dict(c, pourquoi=pourquoi))
        elif not (c["sigma"] and c["e"]):
            a_peser.append(c)
        else:
            c["proxy"] = c["e"] ** 2 / c["sigma"]
            c["masse"] = aire_m2 * c["sigma"] / 1000.0
            c["prix"] = aire_m2 * c["prix_m2"] if c["prix_m2"] else None
            retenus.append(c)
    retenus.sort(key=lambda c: (-c["proxy"], c["masse"], c["prix"] if c["prix"] is not None else 1e9))
    return dict(retenus=retenus, elimines=elimines, a_peser=a_peser)


# ─────────────────────────────── structure ──────────────────────────────
def longueur(expr: dict, R: dict, H: float) -> float:
    return sum(R[k] * c for k, c in (expr or {}).items()) * H


def segments(ctx, carton: dict, D_servo_m: float) -> dict:
    """{segment: dict(a, b, L, n, aire_m2, masse_kg)} ; a, b : section ; L : longueur ; n : nombre."""
    H, R, st = ctx["H"], ctx["R"], ctx["kit"]["structure"]
    e = carton["e"] / 1000.0
    out = {}
    for nom, s in ctx["sq"]["segments"].items():
        if s["forme"] == "boite":
            a, b, L = (longueur(s["dims"][k], R, H) for k in ("x", "y", "z"))
        else:
            a = b = 2 * longueur(s["rayon"], R, H)
            L = longueur(s["longueur"], R, H)
        if nom == "tronc":
            a = R[st["profondeur_tronc"]] * H
            L += ctx["rallonge"]                          # le tronc du Lab, allongé pour son électronique
        if nom in st["segments_a_servo"]:
            a, b = max(a, D_servo_m + 2 * e), max(b, D_servo_m + 2 * e)
        aire = 2 * (a * b + a * L + b * L)
        out[nom] = dict(a=a, b=b, L=L, n=1 if nom in UNIQUES else 2, aire=aire,
                        masse=aire * carton["sigma"] / 1000.0 * st["facteur_renforts"])
    return out


def masse_structure(segs: dict) -> float:
    return sum(s["masse"] * s["n"] for s in segs.values())


def pivots(ctx) -> int:
    """Nombre d'axes du squelette (le Lab) : un pivot chacun au niveau 0 (noms provisoires compris)."""
    return sum(2 if a.get("cote") else 1 for a in ctx["sq"]["articulations"])


# ─────────────────────────────── servos ─────────────────────────────────
def feetech(ctx, var: dict) -> list[dict]:
    """Servos Feetech du marché versé, vitesse ramenée à la tension d'alimentation, compatibilité de plage."""
    import explorateur as X
    import systeme_electrique as SE
    par, _, _ = X.catalogue()
    out = []
    cand = lire("actionneurs.yaml")["candidats"]
    for a in par.get("feetech", []):
        v, note = a["vitesse"], None
        s60 = ((cand.get(a["id"]) or {}).get("vitesse_s_par_60deg") or {}).get("valeur")
        if v is None and s60:                         # la fiche candidate (2026-09-30) la donne : page web sans copie
            v, note = (math.pi / 3) / s60, "vitesse de la fiche candidate (actionneurs.yaml, page web sans copie)"
        f = SE.facteur_vitesse(a["v_ref"], var)
        out.append(dict(a, compat=SE.compatibilite(a["plage_servo"], var), note_vitesse=note,
                        vitesse=v * f if v and f else None))
    return out


def robstride(var: dict) -> list[dict]:
    import explorateur as X
    import systeme_electrique as SE
    par, _, _ = X.catalogue()
    return [dict(a, compat=SE.compatibilite(a["plage"], var),
                 vitesse=a["vitesse"] * SE.facteur_vitesse(a["v_ref"], var) if a["vitesse"] else None)
            for a in par.get("robstride", [])]


def choisir(acts: list[dict], need: dict, marge: float) -> dict:
    """Parmi ceux qui passent (règle de l'explorateur, `passe`) : le MOINS d'inconnues d'abord (peu de références
    mal connues : réparabilité), puis le plus léger. Le couple de pointe « seul le blocage est publié » est commun
    à TOUS les Feetech : il ne départage pas, mais il est rendu."""
    import explorateur as X
    ok = [a for a in acts if X.passe(a, need, marge)]
    if not ok:
        return dict(best=None, inconnues=[])
    inc = lambda a: [i for i in X.inconnues_de(a, need) if "seul le blocage" not in i]
    best = min(ok, key=lambda a: (len(inc(a)), a["masse"] if a["masse"] is not None else 1e9))
    return dict(best=best, inconnues=X.inconnues_de(best, need) + ([best["note_vitesse"]] if best.get("note_vitesse") else []))


def le_plus_fort(acts: list[dict]) -> dict | None:
    ok = [a for a in acts if a.get("compat") is not False]
    return max(ok, key=lambda a: a["pointe"]) if ok else None


# ─────────────────────────────── couples ────────────────────────────────
_T = None


def table():
    global _T
    if _T is None:
        import explorateur as X
        import exigences_physiques as EP
        import simulations_marche as SM
        cap, an, lignes = EP.tout()
        m, r, _ = SM.charger()
        _T = X.table_besoins(lignes, m, r, cap)
    return _T


def statique(ctx, segs: dict, m_servo: dict, m_tete_kg: float) -> dict:
    """Couples STATIQUES (N·m) sur les masses réelles : bras tendu à l'horizontale ; tête basculée."""
    H, R = ctx["H"], ctx["R"]
    Lb, Lab, Lm = R["bras"] * H, R["avant_bras"] * H, R["main_longueur"] * H
    mb, mab, mm = segs["bras"]["masse"], segs["avant_bras"]["masse"], segs["main"]["masse"]
    m_coude = m_servo.get("elbow_roll", 0.0)
    coude = G * (mab * Lab / 2 + mm * (Lab + Lm / 2))
    epaule = G * (mb * Lb / 2 + m_coude * Lb + mab * (Lb + Lab / 2) + mm * (Lb + Lab + Lm / 2))
    ang = math.radians(ctx["kit"]["statique"]["tete_basculee_deg"])
    levier_tete = R["cou_hauteur"] * H + R["tete_hauteur"] * H / 2
    cou = G * (segs["tete"]["masse"] + m_tete_kg) * levier_tete * math.sin(ang)
    return {"shoulder_pitch": epaule, "shoulder_roll": epaule, "elbow_roll": coude, "neck_pitch": cou}


def debout(ctx, M: float) -> dict:
    """Couples STATIQUES pour tenir debout, genoux légèrement fléchis (params/kit.yaml, debout), à la masse M."""
    import exigences_physiques as EP
    H, R = ctx["H"], ctx["R"]
    al = math.radians(ctx["kit"]["debout"]["inclinaison_tibia_deg"])
    F = M * G / 2
    genou = F * R["tibia"] * H * math.sin(al)
    return {"knee": genou, "hip_pitch": genou, "ankle_pitch": F * EP.HYP["levier_cheville_frac"][0] * R["pied_longueur"] * H}


def besoins_module(ctx, mod: dict, M: float, stat: dict) -> dict:
    """Par axe motorisé du module : pointe, continu, vitesse (le maximum de l'explorateur et du statique)."""
    import explorateur as X
    vise = mod.get("vise") or {}
    b = X.besoins(table(), ctx["H"], vise, M) if vise else {}
    out = {}
    for ax in mod["motorises"]:
        e = dict(b.get(ax) or dict(pk=0.0, c=0.0, w=0.0))
        s = stat.get(ax, 0.0)
        e["pk"], e["c"] = max(e["pk"], s), max(e["c"], s)
        e["source"] = ("statique" if s >= (b.get(ax) or {}).get("pk", 0.0) and s > 0 else "explorateur") \
            if (s or b.get(ax)) else "aucune tâche ne charge cet axe"
        out[ax] = e
    return out


# ─────────────────────────────── composants ─────────────────────────────
def composants_fixes(ctx, option: str) -> dict:
    """Calculateur, adaptateur série, pack, convertisseur, chaîne : {rôle: dict(nom, n, masse_kg, prix, source)}."""
    import marche_composants as MC
    import systeme_electrique as SE
    kit, taux = ctx["kit"], ctx["taux"]
    o = kit["alimentation"][option]
    var = SE.variante(o["S"], coupure=lire("puissance.yaml")["tension_retenue"]["coupure_V_par_cellule"])
    out = {}
    hyp = lire("puissance.yaml")["hypotheses"]
    if "calculateur" in o:
        c = SE.choisir_calculateur(SE.options_calculateur(), o["calculateur"], hyp)["best"]
        out["calculateur"] = dict(nom=c["nom"], n=1, masse=(c["masse"] or 0) / 1000 if c["masse"] else None,
                                  prix=c["prix"], source="calculateurs.yaml (même règle que le Lab)", id=c["id"])
    else:
        P = lire("calculateurs.yaml")["marche"]["produits"]
        for role, pid in (("calculateur", o["calculateur_id"]), ("carte_ia", o["carte_ia_id"])):
            p = P[pid]
            out[role] = dict(nom=p.get("nom", pid), n=1, masse=MC.num(MC.v(p, "masse_ensemble")),
                             prix=MC.chf(p.get("prix"), taux), source="calculateurs.yaml", id=pid)
    a = SE.adaptateur_serie()
    out["adaptateur_serie"] = dict(nom=a["nom"], n=1, masse=a["masse"] / 1000, prix=a["prix"], source="bus.yaml", id=a["id"])
    cells = SE.cellules_21700()
    if o["cellule"] == "lab":                         # la cellule du pack du Lab : ses cellules s'y ajoutent
        cel = next(c for c in cells if c["id"] == kit["lab"]["cellule"])
    else:
        cel = min(cells, key=lambda c: (c["m"], c["prix"] or 1e9))      # la plus légère (règle de l'explorateur)
    n = o["S"] * o["P"]
    out["pack"] = dict(nom=f"{o['S']}S{o['P']}P {cel['nom']}", n=n, masse=cel["m"] * hyp["facteur_pack_masse"]["valeur"],
                       prix=cel["prix"], source=f"batteries.yaml ; masse × {hyp['facteur_pack_masse']['valeur']} (pack)",
                       id=cel["id"], E_Wh=n * cel["E"] * hyp["energie_au_dessus_de_la_coupure"]["3.0"])
    comps = SE.composants(lire("puissance.yaml"))
    rail = "12" if o["S"] > 3 else "5"
    d = SE.composant(comps, "dcdc", Vout=float(rail), Vin=(var["Vfin"], var["Vmax"]), var=var,
                     ordre=("volume", "masse", "prix"))
    out[f"convertisseur_{rail}V"] = _maillon(d, f"rail {rail} V")
    for m in lire("puissance.yaml")["chaine_compacte"]:
        if m.get("categorie") and m["maillon"] in ("fusible", "bms", "anti_etincelle") and o["S"] != 12:
            out[m["maillon"]] = dict(nom=f"{m['maillon']} {o['S']}S (hors du marché versé, qui vise le 12S)", n=1,
                                     masse=None, prix=None, source="—")
            continue
        if m.get("categorie") and m["maillon"] in ("fusible", "bms", "anti_etincelle"):
            r = SE.composant(comps, m["categorie"], Vin=(var["Vfin"], var["Vmax"]), var=var, ordre=("volume", "masse", "prix"))
            out[m["maillon"]] = _maillon(r, m["role"])
    return dict(items=out, var=var)


def _maillon(r: dict, role: str) -> dict:
    b = r["best"]
    if b is None:
        return dict(nom=f"aucun ({role})", n=1, masse=None, prix=None, source="puissance.yaml", inconnues=r["inconnues"])
    return dict(nom=b["nom"], n=1, masse=b["masse"] / 1000 if b["masse"] else None, prix=b["prix"],
                source="puissance.yaml (courant NON vérifié : celui du Kit n'est pas calculé)", id=b["id"],
                inconnues=r["inconnues"])


def interactif(ctx, option: str) -> dict:
    """Niveau 2 : caméra, micro, haut-parleur, écran. Sans marché relevé : null, et dit."""
    import marche_composants as MC
    out = {}
    for role in ctx["kit"]["interactif_sans_marche"]:
        out[role] = dict(nom=f"{role} (aucun marché relevé)", n=1, masse=None, prix=None, source="—")
    if option == "minimale":
        p = lire("calculateurs.yaml")["marche"]["produits"]["rpi_ai_camera"]
        out["camera"] = dict(nom=p.get("nom", "rpi_ai_camera"), n=1, masse=MC.num(MC.v(p, "masse_ensemble")),
                             prix=MC.chf(p.get("prix"), ctx["taux"]), source="calculateurs.yaml", id="rpi_ai_camera")
    return out


def somme(items, champ) -> tuple[float, int]:
    """(somme des valeurs connues, nombre d'inconnues) ; masse et prix × n."""
    s, inc = 0.0, 0
    for x in items:
        if x.get(champ) is None:
            inc += 1
        else:
            s += x[champ] * x["n"]
    return s, inc


# ─────────────────────────────── étude ──────────────────────────────────
def etude(option: str = "aligne_lab", carton: dict | None = None, robstride_si_besoin: bool = False) -> dict:
    """`robstride_si_besoin` : un axe dont le visé ne tient pas en Feetech prend le plus léger RobStride qui le
    tient (12S, comme le Lab), et la masse se recalcule avec lui (« ce qu'il faudrait », bouclé)."""
    ctx = contexte()
    import systeme_electrique as SE
    rs = robstride(SE.variante(12, coupure=3.0))
    carton = carton or carton_reference(ctx)
    fixes = composants_fixes(ctx, option)
    var_servo = (dict(S=0, Vfin=float(ctx["kit"]["servos"]["rail_V"]), Vmax=float(ctx["kit"]["servos"]["rail_V"]))
                 if option == "aligne_lab" else fixes["var"])
    ft = feetech(ctx, var_servo)
    D = max(a["D"] for a in ft if a["D"]) / 1000.0
    segs = segments(ctx, carton, D)
    mods = modules(ctx)
    inter = interactif(ctx, option)
    m_servo = {}                               # masse du servo retenu par axe (pour le statique et le total)
    choix = {}
    for _ in range(8):                        # point fixe : masse ↔ servos
        niveaux, M = [], 0.0
        ancien = dict(m_servo)
        for mod in mods:
            items = []
            if mod["niveau"] == 0:
                items.append(dict(nom="structure en carton", n=1, masse=masse_structure(segs), prix=None,
                                  source=f"{carton['id']} ({carton['source']})"))
                items.append(dict(nom=f"pivots (vis traversante, écrou, rondelles larges) × {pivots(ctx)}",
                                  n=1, masse=None, prix=None, source="hardware.yaml (masse et prix non relevés)"))
            if mod["niveau"] == 1:
                items += list(fixes["items"].values())
            if mod["niveau"] == 2:
                items += list(inter.values())
            n_ax = {ax: (2 if ax in COTES else 1) for ax in mod["motorises"]}
            for ax, n in n_ax.items():
                s = choix.get(ax)
                nom = s["best"]["id"] if s and s["best"] else "servo à choisir"
                fam = s["best"]["famille"] if s and s["best"] else "feetech"
                items.append(dict(nom=f"{ax} : {nom}", n=n, masse=m_servo.get(ax), prix=s["best"]["prix"]
                                  if s and s["best"] else None, source=f"actionneurs.yaml (marché {fam})", axe=ax,
                                  famille=fam))
            M += somme(items, "masse")[0]
            niveaux.append(dict(mod=mod, items=items, M=M))
        m_tete = sum(x["masse"] or 0.0 for x in inter.values() if x["nom"].startswith(("camera", "ecran")))
        stat = statique(ctx, segs, m_servo, m_tete)
        res = {}
        for nv in niveaux:
            mod = nv["mod"]
            if not mod["motorises"]:
                continue
            bes = besoins_module(ctx, mod, nv["M"], stat)
            deb = debout(ctx, nv["M"])
            for ax, need in bes.items():
                d = deb.get(ax, 0.0)
                need_d = dict(pk=d, c=d, w=0.0, source="debout statique")
                if d > need["pk"]:
                    need = dict(need, pk=d, c=max(need["c"], d))
                r = choisir(ft, need, ctx["marge"])
                rd = choisir(ft, need_d, ctx["marge"]) if ax in deb else r
                tient_vise = r["best"] is not None
                if not tient_vise and robstride_si_besoin:
                    r = choisir(rs, need, ctx["marge"])
                elif not tient_vise:
                    r = rd                                 # le vise ne tient pas : au moins tenir debout ?
                res[ax] = dict(need=need, need_d=need_d if ax in deb else None, niveau=mod["niveau"], M=nv["M"],
                               tient_vise=tient_vise, tient_debout=rd["best"] is not None, **r)
                if r["best"]:
                    m_servo[ax] = r["best"]["masse"]
                else:
                    m_servo[ax] = max((a["masse"] for a in ft if a["masse"]), default=0.0)
        choix = res
        if m_servo == ancien:
            break
    # le niveau 3 en servos : sinon, ce qu'il faudrait
    for ax, r in choix.items():
        if not r["tient_vise"]:
            r["alternative"] = choisir(rs, r["need"], ctx["marge"])
    return dict(ctx=ctx, option=option, carton=carton, segs=segs, niveaux=niveaux, choix=choix,
                stat=stat, fixes=fixes, D=D, plus_fort=le_plus_fort(ft), var_servo=var_servo)


def bilan(e: dict) -> list[dict]:
    """Par niveau : masse et coût (connus), nombre d'inconnues, cumul."""
    out, Mc, Pc = [], 0.0, 0.0
    for nv in e["niveaux"]:
        m, im = somme(nv["items"], "masse")
        p, ip = somme(nv["items"], "prix")
        Mc, Pc = Mc + m, Pc + p
        out.append(dict(niveau=nv["mod"]["niveau"], nom=nv["mod"]["nom"], masse=m, inc_m=im, prix=p, inc_p=ip,
                        M_cumul=Mc, P_cumul=Pc))
    return out


# ─────────────────────────────── réutilisation ──────────────────────────
def reutilisation(e: dict) -> list[dict]:
    """Chaque composant du Kit au passage au Lab : gardé, remplacé ou recyclé (règles PROPOSÉES, écrites ici)."""
    sort = []
    lab = e["ctx"]["kit"]["lab"]
    lab_feetech = {"neck_yaw", "neck_pitch"} if lab["petits_axes"] == "feetech" else set()   # le cou du Lab
    for nv in e["niveaux"]:
        for x in nv["items"]:
            nom = x["nom"]
            if nom.startswith("structure"):
                s, why = "recyclé", "le Lab est en aluminium ; carton en filière papier (si sans colle ni ruban)"
            elif nom.startswith("pivots"):
                s, why = "gardé en partie", "vis traversante et écrou : même règle de fixation au Lab ; longueurs à revoir"
            elif x.get("axe") in lab_feetech:
                s, why = "gardé", "le Lab met aussi le cou en Feetech (si le même modèle tient au Lab : à vérifier)"
            elif x.get("axe", "").startswith("neck"):
                s, why = "remplacé", f"le cou du Lab est en {lab['petits_axes']} dans sa meilleure solution ; gardé s'il passe en Feetech"
            elif x.get("famille") == "robstride":
                s, why = "gardé (à vérifier)", ("actionneur RobStride, la famille du Lab : il reprend un axe du Lab qui "
                                                "lui convient (le Lab met des RS00 hors du roulis et du tangage de hanche "
                                                "et du genou, fiche 0067)")
            elif x.get("axe"):
                s, why = "remplacé", "le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté"
            elif nom == e["fixes"]["items"]["adaptateur_serie"]["nom"] and lab["petits_axes"] != "feetech":
                s, why = "remplacé", f"adaptateur série Feetech ; le Lab prend des {lab['petits_axes']} (autre adaptateur)"
            elif e["option"] == "aligne_lab" and x.get("source", "").startswith("puissance.yaml"):
                s, why = "gardé (à vérifier)", ("même catégorie que la chaîne du Lab, choisie ici sans le courant : le "
                                                "Lab peut en retenir un autre, plus gros")
            elif e["option"] == "aligne_lab":
                s, why = "gardé", "acheté d'emblée comme celui du Lab (fiche 0074)"
                if x["nom"].startswith(("microphone", "haut_parleur")):
                    s, why = "gardé (non requis)", "le Lab vise « + vision » ; la voix reste possible"
                if "12S1P" in nom:
                    why = "les cellules du Kit sont la moitié du pack 12S2P du Lab (risque : appairer des cellules d'âges différents)"
            else:
                s, why = "recyclé", "option minimale : le Lab prend un autre calculateur et un pack 12S"
            sort.append(dict(nom=nom, n=x["n"], prix=x["prix"], statut=s, pourquoi=why, niveau=nv["mod"]["niveau"]))
    return sort


def part_reutilisee(rows: list[dict], sur: bool = False) -> tuple[float, float]:
    """(coût CONNU gardé, coût CONNU total). `sur` : sans les « gardé (à vérifier) »."""
    tot = sum((r["prix"] or 0) * r["n"] for r in rows)
    ok = lambda st: st.startswith("gardé") and not (sur and "vérifier" in st)
    gard = sum((r["prix"] or 0) * r["n"] for r in rows if ok(r["statut"]))
    return gard, tot


# ─────────────────────────────── rapport ────────────────────────────────
def rapport(e: dict, e_min: dict, variantes: list[tuple[dict, float]], e_rs: dict) -> str:
    ctx = e["ctx"]
    H = ctx["H"]
    L = ["# YXOR Kit : modules, masses, couples et réutilisation (2026-10)", "",
         "**Engendré** par `.venv/bin/python scripts/kit.py --ecrire`. Ne pas éditer à la main. DÉCIDÉ (fiche 0074, "
         "Jeremy, 2026-10-08) : modules successifs, mêmes dimensions, taille et composants que le Lab, carton, outils "
         "du ménage. **PROPOSÉ** : les niveaux (`params/capacites.yaml`, `profils.kit.modules`) et les hypothèses "
         "(`params/kit.yaml`). Rien n'est choisi ni acheté (fiche 0066).", "",
         f"**Le Lab d'aujourd'hui** ({ctx['kit']['lab']['source']}) : jambe à H = {f1(H, 2)} m, hauteur réelle "
         f"{f1(ctx['kit']['lab']['hauteur_reelle_m'], 3)} m (seul le tronc s'allonge), {f1(ctx['kit']['lab']['masse_kg'])} kg. "
         "Le Kit prend ce squelette : même silhouette, mêmes longueurs. La taille du Lab n'est pas décidée (fiche "
         f"0047 : c'est une sortie de l'explorateur) ; le Kit la suivra. Marge {f1(ctx['marge'])} sur le couple "
         "(fiche 0051).", ""]
    # structure
    c = e["carton"]
    L += ["## Structure en carton", "",
          f"Carton de référence : **{c['id']}**, {f1(c['sigma'], 0)} g/m², {f1(c['e'])} mm ({c['source']}). Coques "
          f"fermées par segment ; section des segments à servo ≥ {f1(e['D'] * 1000)} mm (plus grand servo Feetech) "
          f"+ deux parois ; × {f1(ctx['kit']['structure']['facteur_renforts'])} pour les renforts.", "",
          "| Segment | Nombre | Section (mm) | Longueur (mm) | Aire (dm²) | Masse unitaire (g) |",
          "| --- | ---: | --- | ---: | ---: | ---: |"]
    for nom, s in e["segs"].items():
        L.append(f"| {nom} | {s['n']} | {f1(s['a'] * 1000, 0)} × {f1(s['b'] * 1000, 0)} | {f1(s['L'] * 1000, 0)} | "
                 f"{f1(s['aire'] * 100, 2)} | {f1(s['masse'] * 1000, 0)} |")
    L += ["", f"**Structure : {f1(masse_structure(e['segs']) * 1000, 0)} g.** Selon le carton (même géométrie) :", "",
          "| Carton | Masse surfacique (g/m²) | Épaisseur (mm) | Structure (g) | Source |", "| --- | ---: | ---: | ---: | --- |"]
    for cv, m in variantes:
        L.append(f"| {cv['id']} | {f1(cv['sigma'], 0)} | {f1(cv['e'])} | {f1(m * 1000, 0)} | {cv['source']} |")
    # classement
    aire = sum(x["aire"] * x["n"] for x in e["segs"].values()) * ctx["kit"]["structure"]["facteur_renforts"]
    cl = classement_cartons(ctx, aire)
    L += ["", "## Classement des cartons (critères PROPOSÉS, `params/kit.yaml`)", "",
          f"Aire de carton du Kit, renforts compris : {f1(aire, 2)} m². Éliminatoires : filière papier mono-matière ; "
          "un panneau (pas un simple face) ; disponible en Suisse. Rang : e²/σ (proxy de la rigidité en flexion par "
          "masse, que les essais remplaceront), puis masse, puis prix. **Rien n'est choisi.**", "",
          "| Rang | Carton | Famille | e (mm) | σ (g/m²) | e²/σ | Structure (g) | Prix structure (CHF) | Disponibilité |",
          "| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |"]
    for i, c in enumerate(cl["retenus"], 1):
        L.append(f"| {i} | {c['id']} | {c['famille']} | {f1(c['e'])} | {f1(c['sigma'], 0)} | {f1(c['proxy'], 4)} | "
                 f"{f1(c['masse'] * 1000, 0)} | {f1(c['prix'], 0)} | {c['dispo'][:60]} |")
    L += ["", "**À peser** (épaisseur ou masse surfacique non publiée ; protocole `docs/protocole-carton.md`) : "
          + ", ".join(f"{c['id']} ({f1(c['prix_m2'], 2)} CHF/m²)" for c in cl["a_peser"]) + ".", "",
          "**Éliminés** : " + " ; ".join(f"{c['id']} ({c['pourquoi']})" for c in cl["elimines"]) + "."]
    # niveaux
    for ee, titre in ((e, "option « alignée sur le Lab »"), (e_min, "option « minimale »")):
        o = ctx["kit"]["alimentation"][ee["option"]]
        pk = ee["fixes"]["items"]["pack"]
        cal = ee["fixes"]["items"]["calculateur"]
        L += ["", f"## Modules, masse et coût : {titre}", "", o["description"] + f". Énergie du pack au-dessus de la "
              f"coupure : {f1(pk['E_Wh'], 0)} Wh ; calculateur : {cal['nom']}.", "",
              "| Niveau | Module | Masse (kg) | Coût (CHF HT) | Inconnues (masse / prix) | Masse cumulée (kg) | Coût cumulé (CHF) |",
              "| ---: | --- | ---: | ---: | --- | ---: | ---: |"]
        for b in bilan(ee):
            L.append(f"| {b['niveau']} | {b['nom']} | {'≥ ' if b['inc_m'] else ''}{f1(b['masse'], 2)} | "
                     f"{'≥ ' if b['inc_p'] else ''}{f1(b['prix'], 0)} | {b['inc_m']} / {b['inc_p']} | "
                     f"{f1(b['M_cumul'], 2)} | {f1(b['P_cumul'], 0)} |")
        L += ["", "<details><summary>Composants par niveau</summary>", "",
              "| Niveau | Composant | Nombre | Masse unitaire (g) | Prix unitaire (CHF HT) | Source |",
              "| ---: | --- | ---: | ---: | ---: | --- |"]
        for nv in ee["niveaux"]:
            for x in nv["items"]:
                L.append(f"| {nv['mod']['niveau']} | {x['nom']} | {x['n']} | "
                         f"{f1(x['masse'] * 1000 if x['masse'] is not None else None, 0)} | {f1(x['prix'], 2)} | {x['source']} |")
        L += ["", "</details>"]
    # couples
    L += ["", "## Couples et servos (option alignée : servos sur le rail 12 V)", "",
          "Besoin = maximum de l'explorateur (à la masse du Kit au niveau du module) et du statique direct ; "
          f"le servo doit tenir besoin × {f1(ctx['marge'])}. Statique : bras tendu à l'horizontale, tête basculée de "
          f"{ctx['kit']['statique']['tete_basculee_deg']}°.", "",
          "| Niveau | Axe | Masse M (kg) | Pointe requise (N·m) | Continu requis (N·m) | Vitesse (rad/s) | Origine | "
          "Le visé tient ? | Debout tient ? | Servo Feetech | Inconnues |",
          "| ---: | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- |"]
    for ax, r in e["choix"].items():
        n = r["need"]
        b = r["best"]
        deb = "—" if r["need_d"] is None else ("oui" if r["tient_debout"] else "**non**")
        L.append(f"| {r['niveau']} | {ax} | {f1(r['M'], 2)} | {f1(n['pk'], 3)} | {f1(n['c'], 3)} | {f1(n['w'])} | "
                 f"{n['source']} | {'oui' if r['tient_vise'] else '**non**'} | {deb} | "
                 f"{b['id'] + ' (' + f1(b['pointe'], 2) + ' N·m)' if b else '**aucun**'} | "
                 f"{'; '.join(r['inconnues']) or '—'} |")
    L += ["", "« Le visé » : les capacités du module (`vise`), statique compris ; « debout » : le statique seul "
          f"(tibia incliné de {ctx['kit']['debout']['inclinaison_tibia_deg']}°, PROPOSÉ). Quand le visé ne tient pas, "
          "le servo indiqué est celui qui tient debout."]
    pf = e["plus_fort"]
    sans = [ax for ax, r in e["choix"].items() if not r["tient_vise"]]
    L += [""]
    if sans:
        L += [f"**Le visé ne tient pas en Feetech** : {', '.join(sans)}. Le plus fort Feetech compatible du marché versé est "
              f"{pf['id']} ({f1(pf['pointe'], 2)} N·m de pointe, {f1(pf['continu'], 2)} N·m en continu, "
              f"{f1(pf['vitesse'])} rad/s au rail). **Ce qu'il faudrait** (le plus léger RobStride qui passe, en 12S "
              "coupé à 3,0 V, comme le Lab) :", "",
              "| Axe | Pointe × marge (N·m) | Continu × marge (N·m) | Vitesse (rad/s) | RobStride | Masse (g) | Prix (CHF HT) |",
              "| --- | ---: | ---: | ---: | --- | ---: | ---: |"]
        for ax in sans:
            r = e["choix"][ax]
            a = (r.get("alternative") or {}).get("best")
            L.append(f"| {ax} | {f1(r['need']['pk'] * ctx['marge'], 2)} | {f1(r['need']['c'] * ctx['marge'], 2)} | "
                     f"{f1(r['need']['w'])} | {a['id'] if a else 'aucun'} | {f1(a['masse'] * 1000 if a else None, 0)} | "
                     f"{f1(a['prix'] if a else None, 0)} |")
    else:
        L.append("Tous les axes motorisés ont un servo Feetech qui tient (sur ce qui est connu).")
    # niveau 3 qui marche : RobStride là où le Feetech ne tient pas, masse rebouclée
    L += ["", "### Niveau 3 qui marche : RobStride là où aucun Feetech ne tient (masse recalculée)", "",
          "| Niveau | Masse cumulée (kg) | Coût cumulé (CHF HT) | Inconnues (masse / prix) |", "| ---: | ---: | ---: | --- |"]
    for b in bilan(e_rs):
        L.append(f"| {b['niveau']} | {f1(b['M_cumul'], 2)} | {f1(b['P_cumul'], 0)} | {b['inc_m']} / {b['inc_p']} |")
    L += ["", "| Axe | Pointe requise (N·m) | Continu requis (N·m) | Vitesse (rad/s) | Actionneur |",
          "| --- | ---: | ---: | ---: | --- |"]
    for ax, r in e_rs["choix"].items():
        if r["niveau"] == 3:
            b = r["best"]
            L.append(f"| {ax} | {f1(r['need']['pk'], 3)} | {f1(r['need']['c'], 3)} | {f1(r['need']['w'])} | "
                     f"{b['id'] if b else '**aucun**'} |")
    # réutilisation
    for ee, titre in ((e, "option alignée"), (e_rs, "option alignée, jambes RobStride là où il le faut"),
                      (e_min, "option minimale")):
        rows = reutilisation(ee)
        g, t = part_reutilisee(rows)
        gs, _ = part_reutilisee(rows, sur=True)
        L += ["", f"## Réutilisation Kit → Lab : {titre}", "",
              f"**Part du coût CONNU du Kit réutilisée dans le Lab : {f1(100 * gs / t if t else None, 0)} % sûrs, "
              f"{f1(100 * g / t if t else None, 0)} % si les maillons « à vérifier » coïncident** ({f1(gs, 0)} à "
              f"{f1(g, 0)} CHF sur {f1(t, 0)} CHF ; les composants sans prix ne comptent pas).", "",
              "| Niveau | Composant | Nombre | Prix total (CHF) | Au Lab | Pourquoi |", "| ---: | --- | ---: | ---: | --- | --- |"]
        for r in rows:
            L.append(f"| {r['niveau']} | {r['nom']} | {r['n']} | {f1((r['prix'] or 0) * r['n'] if r['prix'] is not None else None, 0)} | "
                     f"**{r['statut']}** | {r['pourquoi']} |")
    return "\n".join(L) + "\n"


def tout() -> tuple[dict, dict, list, dict]:
    e = etude("aligne_lab")
    e_min = etude("minimale")
    e_rs = etude("aligne_lab", robstride_si_besoin=True)
    ctx = e["ctx"]
    variantes = [(c, masse_structure(segments(ctx, c, e["D"]))) for c in cartons(ctx)]
    return e, e_min, variantes, e_rs


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ecrire", action="store_true")
    a = ap.parse_args(argv)
    e, e_min, var, e_rs = tout()
    txt = rapport(e, e_min, var, e_rs)
    for ee in (e, e_min, e_rs):
        print(f"  {ee['option']} :", " ; ".join(f"N{b['niveau']} {f1(b['M_cumul'], 2)} kg {f1(b['P_cumul'], 0)} CHF"
                                              for b in bilan(ee)))
    sans = [ax for ax, r in e["choix"].items() if not r["tient_vise"]]
    deb = [ax for ax, r in e["choix"].items() if not r["tient_debout"]]
    print(f"  visé sans Feetech : {', '.join(sans) or 'aucun'} ; debout sans Feetech : {', '.join(deb) or 'aucun'}")
    for ee in (e, e_min):
        g, t = part_reutilisee(reutilisation(ee))
        gs, _ = part_reutilisee(reutilisation(ee), sur=True)
        print(f"  réutilisé au Lab ({ee['option']}) : {f1(100 * gs / t if t else None, 0)} à {f1(100 * g / t if t else None, 0)} %")
    if a.ecrire:
        DOC.write_text(txt, encoding="utf-8")
        print(f"  -> {DOC.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
