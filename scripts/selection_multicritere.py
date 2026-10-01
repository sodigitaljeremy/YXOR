#!/usr/bin/env python3
"""Sélection multicritère : classe d'actionneur de S, puis composition du banc.

    .venv/bin/python scripts/selection_multicritere.py            # résumé
    .venv/bin/python scripts/selection_multicritere.py --ecrire   # engendre les deux documents

Venv DU PROJET. Lit :
  params/actionneurs.yaml          catalogue et faits du comparatif (comparatif_S)
  params/criteres_selection.yaml   éliminatoires, grilles 0–5, poids, jugements
  params/budget.yaml               TVA, imprévus, taux, adaptateur CAN, alimentation
  la marche P1, via scripts/dimensionnement.py (H_max par candidat)

Engendre :
  docs/choix-classe-S.md
  docs/comparatif-banc.md

═══════════════════════════════════════════════════════════════════════
 LA MÉTHODE
═══════════════════════════════════════════════════════════════════════

1. ÉLIMINATOIRES. Un candidat qui échoue est ÉLIMINÉ et ne peut pas
   gagner, quels que soient les poids. Une donnée manquante ne l'élimine
   pas : il est « non évaluable », c'est affiché, et il reste classé.
2. NOTES 0–5, par des grilles écrites AVANT le calcul
   (criteres_selection.yaml). Chaque note est « calculée » depuis le
   catalogue ou « jugement », et sa justification est imprimée. Une note
   manquante vaut 0 par prudence.
3. SCORE = moyenne des notes pondérée par les poids. Leur STATUT est lu
   dans criteres_selection.yaml : un poids n'est dit « fixé » que si son
   statut commence par « fixé » ou « DÉCIDÉ ». Au 2026-09-30 (~23 h),
   ceux de la classe S et des familles sont DÉCIDÉS par Jeremy, validés
   tels quels après avoir été d'abord attribués à tort ; ceux du banc
   restent proposés.
4. SENSIBILITÉ. Chaque poids ±50 %, un à la fois ; puis 1 000 jeux de
   poids tirés au hasard (Dirichlet α = 1, graine fixe). On compte qui
   gagne. Le classement est ROBUSTE si le vainqueur nominal gagne toutes
   les variations ±50 % et au moins 60 % des tirages ; sinon, les
   candidats sont trop proches pour que l'analyse tranche.

Aucun achat n'est proposé : c'est un comparatif demandé (CLAUDE.md,
règle d'achat c).
"""
from __future__ import annotations

import argparse
import datetime
import random
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyser_marche as AM  # noqa: E402
import dimensionnement as D  # noqa: E402
import estimation_thermique as ET  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
CRITERES = REPO / "params" / "criteres_selection.yaml"
DOC_S_V1 = REPO / "docs" / "choix-classe-S.md"          # v1, figé : n'est plus régénéré
DOC_FAMILLE = REPO / "docs" / "choix-famille-actionneurs.md"
DOC_BANC = REPO / "docs" / "comparatif-banc.md"
BANC = REPO / "params" / "banc.yaml"          # configurations du banc, source unique

val = D.val


def f(x, n=2):
    return "—" if x is None else f"{x:.{n}f}".replace(".", ",")


# ───────────────────────────── grilles ──────────────────────────────────

def seuils(x, bornes, notes, defaut=0):
    """Première borne atteinte (x ≤ borne) → note ; None → défaut."""
    if x is None:
        return defaut
    for b, n in zip(bornes, notes):
        if x <= b:
            return n
    return notes[-1] if len(notes) > len(bornes) else defaut


def note_capacite(H, seuils_m):
    """Grille lue dans criteres_selection.yaml (`capacite.seuils_m`) — jamais recopiée ici."""
    if H is None:
        return 0
    for s, n in seuils_m:
        if H >= s:
            return n
    return 0


def note_cout(chf):
    return 0 if chf is None else seuils(chf, (60, 90, 130, 200, 300), (5, 4, 3, 2, 1), 0)


def note_masse(g):
    return 0 if g is None else seuils(g, (150, 200, 250, 350, 500), (5, 4, 3, 2, 1), 0)


def note_tension(v):
    return 0 if v is None else seuils(v, (12, 24, 36, 48), (5, 4, 3, 2), 1)


# ───────────────────────────── données S ────────────────────────────────

def intervalle_continu(c: dict, k: float) -> dict:
    """Couple continu OPTIMISTE et PRUDENT (règle unifiée du 2026-09-30, v3).

    optimiste : le nominal publié le plus favorable (hors blocage) ;
    prudent   : EN BLOCAGE si publié ; sinon le nominal × k, pour TOUT
                candidat, qu'une plaque soit publiée ou non — un robot
                debout travaille près du blocage.
    k est une HYPOTHÈSE balayée, jamais une valeur mesurée.
    """
    cc = c["couple_continu_Nm"]
    opts = [dict(valeur=val(cc), plaque_mm=cc.get("plaque_mm"), condition=cc.get("condition"))]
    opts += [dict(valeur=a.get("valeur"), plaque_mm=a.get("plaque_mm"), condition=a.get("condition"))
             for a in (cc.get("autres_conditions") or [])]
    bloque = lambda o: bool(o["condition"]) and "BLOCAGE" in o["condition"]
    rot = [o for o in opts if o["valeur"] is not None and not bloque(o)]
    if not rot:
        return dict(optimiste=None, prudent=None, base_prudente="continu inconnu", k_applique=False)
    optimiste = max(o["valeur"] for o in rot)
    blocage = next((o for o in opts if bloque(o) and o["valeur"] is not None), None)
    if blocage:
        return dict(optimiste=optimiste, prudent=blocage["valeur"], base_prudente="en blocage (publié)",
                    k_applique=False)
    return dict(optimiste=optimiste, prudent=optimiste * k,
                base_prudente=f"aucune valeur en blocage publiée : nominal × k ({f(k, 1)})", k_applique=True)


def rapports_blocage(cat) -> list[dict]:
    """Ce que les données disent de k : blocage / nominal, là où les deux sont publiés."""
    out = []
    for cid, c in cat["candidats"].items():
        iv = intervalle_continu(c, 1.0)
        if iv["prudent"] is not None and not iv["k_applique"] and iv["optimiste"]:
            out.append(dict(id=cid, nom=c["nom"], blocage=iv["prudent"], nominal=iv["optimiste"],
                            rapport=iv["prudent"] / iv["optimiste"]))
    return out


def h_max_avec(cat, cid, continu, ref, besoins, marge):
    """H_max, en configuration homogène, avec un couple continu imposé."""
    cl = D.classe_catalogue(cat, cid)
    cl["continu"] = continu
    ev = D.evaluer(ref, D.config_homogene(cl), besoins, marge)
    return (None, None) if "indetermine" in ev else (ev["H_max"], ev)


def prix_chf(cat, cid, bud):
    fs = cat.get("comparatif_S", {}).get(cid, {})
    p = fs.get("prix_revendeur") or cat["candidats"][cid]["prix"]
    return D.chf(p, bud["taux_de_change"]), p


def k_de(k, cid: str) -> float:
    """k peut être un nombre (le même pour tous) ou un dict {id: k, "_defaut": k}.

    Le dict sert à la carte en deux dimensions (2026-10-01, information) :
    k du J4310 et k de l'EduLite 05 balayés séparément. Avec un nombre, le
    calcul est exactement celui d'avant.
    """
    if isinstance(k, dict):
        return k.get(cid, k.get("_defaut", 1.0))
    return k


def evaluer_S(cat, crit, bud, analyse, ref, k=1.0):
    """Faits, éliminatoires et notes de chaque candidat S (et référence)."""
    marge = val(cat["dimensionnement"]["marge"])
    besoins = D.besoins_p1(analyse)
    cs = cat["comparatif_S"]
    ML = [cs.get(i, {}).get("famille_protocole") or
          ("robstride_can" if cat["candidats"][i]["fabricant"].startswith("RobStride") else None)
          for i in crit["classe_S"]["continuite_vers"]]
    jug = crit["classe_S"]["jugements"]
    out = []
    for cid in cs["candidats"] + cs["references"]:
        c, fs = cat["candidats"][cid], cs[cid]
        iv = intervalle_continu(c, k_de(k, cid))
        H, ev = h_max_avec(cat, cid, iv["prudent"], ref, besoins, marge)
        H_opt, _ = h_max_avec(cat, cid, iv["optimiste"], ref, besoins, marge)
        ev = ev or {}
        cr = dict(valeur=iv["prudent"], condition=iv["base_prudente"], blocage=None,
                  plaque_mm=None, optimiste=iv["optimiste"], k_applique=iv["k_applique"])
        classe = D.classe_catalogue(cat, cid)
        H_nominal = H_opt
        # La taille n'élimine plus : elle est seulement notée (capacité).
        elim_cap = "notée, non éliminatoire"
        tel = fs["telemetrie"]
        champs = [tel.get(k) for k in ("position", "couple_ou_courant", "temperature")]
        elim_tel = "éliminé" if False in champs else ("non évaluable" if None in champs else "admis")
        # Depuis le 2026-09-30 (soir), la taille n'est PLUS éliminatoire
        # (criteres_selection.yaml, `modifications`) : c'est une sortie de
        # la démarche inversée, notée par le critère de capacité. Seule la
        # télémétrie élimine.
        etat = elim_tel
        # ── notes ──
        n, j = {}, {}
        n["capacite"] = note_capacite(H, crit["classe_S"]["ponderes"]["capacite"]["seuils_m"]) if cr["valeur"] is not None else 0
        j["capacite"] = (f"taille PRUDENTE {f(H)} m ({f(cr['valeur'])} N·m, {cr['condition']}) → "
                         f"{n['capacite']} ; optimiste {f(H_opt)} m ({f(cr['optimiste'])} N·m)"
                         if cr["valeur"] is not None else "couple continu inconnu → 0")
        chf, p = prix_chf(cat, cid, bud)
        n["cout"] = note_cout(chf)
        j["cout"] = (f"{f(chf)} CHF HT ({p.get('valeur')} {p.get('devise')}, {p.get('vendeur')})"
                     if chf is not None else "prix inconnu → 0 par prudence")
        fam = fs["famille_protocole"]
        pts = (2 if fam.endswith("_can") else 0) + (2 if fam in ML else 0) + \
              (1 if val(c["tension_V"]) == 48 else 0)
        n["continuite"] = pts
        j["continuite"] = (f"bus {'CAN' if fam.endswith('_can') else 'non CAN'} ; protocole "
                           f"{'= M/L' if fam in ML else '≠ M/L'} ({fam}) ; {val(c['tension_V'])} V")
        g, d = val(fs["garantie_mois"]), fs["distribution"]
        if g and g >= 12 and d.get("suisse"):
            nf = 5
        elif g and g >= 12 and d.get("ue"):
            nf = 4
        elif g and g >= 12:
            nf = 3
        elif (g and g < 12) or d.get("ue"):
            nf = 2
        elif c.get("fabricant"):
            nf = 1
        else:
            nf = 0
        n["fiabilite_fournisseur"] = nf
        j["fiabilite_fournisseur"] = (f"garantie écrite {g if g else 'non trouvée'}"
                                      f"{' mois' if g else ''} ; UE {d.get('ue') or 'non'} ; CH {d.get('suisse') or 'non'}")
        jr = jug["robustesse"][cid]
        n["robustesse"], j["robustesse"] = jr["note"], "JUGEMENT — " + jr["justification"]
        n["masse"] = note_masse(val(c["masse_g"]))
        j["masse"] = f"{f(val(c['masse_g']), 1)} g"
        o = fs["ouverture"]
        n["ouverture"] = (2 if o.get("protocole_public") else 0) + (2 if o.get("sdk_libre") else 0) + \
                         (1 if o.get("firmware_libre") else 0)
        j["ouverture"] = (f"protocole public {'oui' if o.get('protocole_public') else 'non/inconnu'} ; "
                          f"SDK libre {'oui' if o.get('sdk_libre') else 'non établi'} ; firmware libre "
                          f"{'oui' if o.get('firmware_libre') else 'non'}")
        n["tension_securite"] = note_tension(val(c["tension_V"]))
        j["tension_securite"] = f"{val(c['tension_V'])} V"
        if d.get("suisse"):
            nd = 5
        elif d.get("ue"):
            nd = 4
        elif d.get("international") and "direct" not in d["international"]:
            nd = 3
        elif d.get("international"):
            nd = 2
        elif d.get("non_verifie"):
            nd = 1
        else:
            nd = 0
        n["disponibilite"] = nd
        j["disponibilite"] = (d.get("suisse") or d.get("ue") or d.get("international")
                              or ("non vérifié : " + d["non_verifie"] if d.get("non_verifie") else "inconnu"))
        out.append(dict(id=cid, nom=c["nom"], reference=bool(c.get("reference")),
                        H=H, H_nominal=H_nominal, H_opt=H_opt, k=k, masse_robot=ev.get("masse"),
                        limitantes=ev.get("limitantes", []), continu=cr, prix_chf=chf,
                        elim_capacite=elim_cap, elim_telemetrie=elim_tel, etat=etat,
                        notes=n, justif=j, tension=val(c["tension_V"]),
                        famille=fam, pointe=classe["pointe"], masse_g=val(c["masse_g"])))
    return out


# ─────────────────────────────── familles ───────────────────────────────

TAILLES = ("S", "M", "L")


def plage_tension(c: dict):
    """Plage publiée ; à défaut, la seule tension nominale."""
    v = val(c.get("tension_plage_V") or {})
    if v:
        return tuple(v)
    tv = val(c["tension_V"])
    return (tv, tv) if tv is not None else None


def tension_commune(plages):
    """Une tension qui entre dans toutes les plages (48 V de préférence)."""
    if not plages or any(p_ is None for p_ in plages):
        return None
    lo, hi = max(p_[0] for p_ in plages), min(p_[1] for p_ in plages)
    if lo > hi:
        return None
    return 48 if lo <= 48 <= hi else (24 if lo <= 24 <= hi else lo)


def evaluer_familles(cat, crit, bud, analyse, ref, cands_S, k):
    """Chaque famille S → M → L : tailles, coûts, continuité intrinsèque, trous.

    Les critères autres que la continuité sont ceux du MEMBRE S (le premier
    robot), repris de evaluer_S au même k.
    """
    marge = val(cat["dimensionnement"]["marge"])
    besoins = D.besoins_p1(analyse)
    par_id = {c["id"]: c for c in cands_S}
    out = []
    for fid, fam in cat["familles"].items():
        tailles = {}
        for tl in TAILLES:
            mid = fam.get(tl)
            if not mid:
                tailles[tl] = None
                continue
            c = cat["candidats"][mid]
            iv = intervalle_continu(c, k_de(k, mid))
            Hp, evp = h_max_avec(cat, mid, iv["prudent"], ref, besoins, marge)
            Ho, _ = h_max_avec(cat, mid, iv["optimiste"], ref, besoins, marge)
            # Même base de prix que la note de coût : le prix REVENDEUR s'il
            # est relevé (comparatif_S), sinon celui du catalogue.
            cat_prix = cat
            pr = c.get("prix_revendeur") or (cat.get("comparatif_S", {}).get(mid) or {}).get("prix_revendeur")
            if pr and pr.get("valeur") is not None:
                cat_prix = dict(cat, candidats=dict(cat["candidats"], **{mid: dict(c, prix=pr)}))
            cout = D.couts(cat_prix, bud, D.config_homogene(D.classe_catalogue(cat_prix, mid)))
            tailles[tl] = dict(id=mid, nom=c["nom"], H_prud=Hp, H_opt=Ho, iv=iv,
                               pointe=val(c["couple_pointe_Nm"]), tension=val(c["tension_V"]),
                               plage=plage_tension(c), bus=c["bus"], masse_robot=(evp or {}).get("masse"),
                               jambes=cout["jambes_v1"], haut=cout["haut_du_corps_v2"])
        presents = [x for x in tailles.values() if x]
        trous = [tl for tl, x in tailles.items() if not x]
        can = bool(presents) and all("CAN" in x["bus"] for x in presents)
        proto = bool(fam.get("protocole_commun", {}).get("valeur"))
        commune = tension_commune([x["plage"] for x in presents])
        cont = max(0, (2 if can else 0) + (2 if proto else 0) + (1 if commune else 0) - len(trous))
        S = par_id[fam["S"]]
        notes = dict(S["notes"], continuite=cont)
        justif = dict(S["justif"], continuite=(
            f"bus {'CAN sur les 3' if can else 'NON commun'} ; protocole commun "
            f"{'oui' if proto else 'non établi'} ; tension commune "
            f"{str(commune) + ' V' if commune else 'aucune'} ; trous : {', '.join(trous) or 'aucun'}"))
        out.append(dict(id=fid, nom=fam["nom"], tailles=tailles, trous=trous, notes=notes,
                        justif=justif, etat=S["etat"], reference=False, S=S, can=can, proto=proto,
                        tension_commune=commune, alternatives=fam.get("alternatives") or {},
                        note_famille=fam.get("note")))
    return out


# ─────────────────────────── score et sensibilité ───────────────────────

def score(notes: dict, poids: dict) -> float:
    tot = sum(poids.values())
    return sum(poids[k] * notes.get(k, 0) for k in poids) / tot


def classables(cands):
    """Un ÉLIMINÉ ne peut pas gagner ; une référence n'est pas classée."""
    return [c for c in cands if c["etat"] != "éliminé" and not c.get("reference")]


def vainqueur(cands, poids):
    cl = classables(cands)
    if not cl:
        return None
    return max(cl, key=lambda c: (score(c["notes"], poids), c["id"]))["id"]


def sensibilite(cands, poids, sens):
    nominal = vainqueur(cands, poids)
    var = []
    for k in poids:
        for fac in (1 - sens["variation_poids"], 1 + sens["variation_poids"]):
            p = dict(poids, **{k: poids[k] * fac})
            var.append((k, fac, vainqueur(cands, p)))
    rng = random.Random(sens["graine"])
    gagnes = {}
    for _ in range(sens["tirages"]):
        tirage = [rng.gammavariate(1.0, 1.0) for _ in poids]
        p = dict(zip(poids, tirage))
        w = vainqueur(cands, p)
        gagnes[w] = gagnes.get(w, 0) + 1
    tous_pm = all(w == nominal for _, _, w in var)
    freq = gagnes.get(nominal, 0) / sens["tirages"]
    robuste = tous_pm and freq >= sens["seuil_robuste"]
    return dict(nominal=nominal, variations=var, gagnes=gagnes, freq=freq,
                tous_pm=tous_pm, robuste=robuste)


# ─────────────────────────────── banc ───────────────────────────────────

def options_banc(r):
    """Options du banc, construites sur le résultat des FAMILLES (point 3).

    Vainqueur : le membre S de la famille gagnante à k = 1,0. Finalistes :
    les membres S des deux familles qui gagnent de part et d'autre du seuil
    k ; à défaut de bascule, les deux premières familles à k = 1,0.
    """
    cat, bud, crit = r["cat"], r["bud"], r["crit"]
    b = crit["banc"]
    taux, tva, imp = bud["taux_de_change"], val(bud["tva_ch"]), val(bud["marge_imprevus"])
    pays_liv = bud.get("livraison") or ["CH"]
    tva_de = lambda pays: val(bud[f"tva_{pays.lower()}"])
    elec = bud["electronique"]
    jr = b["ponderes"]["risque"]["jugements_par_option"]
    fams = {fm["id"]: fm for fm in r["fams"]}
    cat_fam = cat["familles"]
    gagnant = r["fam_balayage"][0]["sens"]["nominal"]
    if r["fam_seuil"]:
        fa, fb = r["fam_seuil"]["gagnant"], r["fam_seuil"]["nouveau"]
    else:
        tri = sorted(r["fams"], key=lambda x: -score(x["notes"], r["poids"]))
        fa, fb = tri[0]["id"], tri[1]["id"]
    S_id = cat_fam[gagnant]["S"]
    seuil = r["fam_seuil"]["garde"] if r["fam_seuil"] else None

    def info(cid):
        c = cat["candidats"][cid]
        chf, _ = prix_chf(cat, cid, bud)
        return dict(id=cid, nom=c["nom"], prix=chf, plage=plage_tension(c), tension=val(c["tension_V"]),
                    can="CAN" in c["bus"])

    def cout(ids, tension):
        ht, manquants = 0.0, []
        for i_ in ids:
            x = info(i_)
            if x["prix"] is None:
                manquants.append(f"prix {x['nom']}")
            else:
                ht += x["prix"]
        can = all(info(i_)["can"] for i_ in ids)
        a = D.chf(elec["adaptateur_can" if can else "adaptateur_ttl"]["prix"], taux)
        (manquants.append("adaptateur") if a is None else None)
        ht += a or 0
        cle = {48: "alimentation_48V", 24: "alimentation_24V"}.get(tension)
        al = D.chf(elec[cle]["prix"], taux) if cle and cle in elec else None
        (manquants.append(f"alimentation {tension} V") if al is None else None)
        ht += al or 0
        # TTC par pays de livraison (budget.yaml, `livraison`) : la note de
        # coût se prend sur le PREMIER pays ; les autres sont affichés.
        return {pays: ht * (1 + imp) * (1 + tva_de(pays)) for pays in pays_liv}, manquants

    def appr(modeles: dict):
        """Apprentissages, CALCULÉS depuis les exemplaires par modèle (params/banc.yaml).

        Corrigé le 2026-10-01 (audit externe) : la dispersion entre
        exemplaires exige AU MOINS 2 exemplaires d'un MÊME modèle ; trois
        modèles à un exemplaire n'en mesurent aucune. Avant : « n ≥ 3 et
        même modèle », déclaré à la main par option.
        """
        n = sum(modeles.values())
        bus = {("CAN" if info(m)["can"] else "TTL") for m in modeles}
        meme_bus = len(bus) == 1
        pts = {"protocole": True, "thermique": True,
               "bus_multi_adresses": n >= 2 and meme_bus,
               "segment_2ddl": n >= 2 and meme_bus,
               "dispersion": max(modeles.values()) >= 2}
        return sum(pts.values()), [k for k, v in pts.items() if v]

    # Configurations LUES dans params/banc.yaml (source unique, 2026-10-01).
    confs = yaml.safe_load(BANC.read_text(encoding="utf-8"))["banc"]["configurations"]
    SA, SB = cat_fam[fa]["S"], cat_fam[fb]["S"]
    choix = []
    for fid, sid in ((fa, SA), (fb, SB)):
        var = cat_fam[fid].get("S_variante_48V")
        choix.append([sid] + ([var] if var else []))
    paire, tension_paire = None, None
    for cible in (48, 24):
        a_ = next((x for x in choix[0] if (pl := info(x)["plage"]) and pl[0] <= cible <= pl[1]), None)
        b_ = next((x for x in choix[1] if (pl := info(x)["plage"]) and pl[0] <= cible <= pl[1]), None)
        if a_ and b_:
            paire, tension_paire = [a_, b_], cible
            break
    resolus = {"@S_gagnant": S_id}
    if paire:
        resolus.update({"@S_finaliste_A": paire[0], "@S_finaliste_B": paire[1]})
    vs = info(S_id)
    opts = []
    for oid, cf in confs.items():
        if not cf.get("comparatif"):
            continue
        if any(m.startswith("@") and m not in resolus for m in cf["modeles"]):
            continue          # pas de paire de finalistes à une même tension
        modeles = {resolus.get(m, m): q for m, q in cf["modeles"].items()}
        ids = [m for m, q in modeles.items() for _ in range(q)]
        # Tension CALCULÉE : la tension commune des plages publiées de ses
        # modèles (48 V de préférence). Jamais déclarée, jamais par défaut
        # (bug du lot E : 12 V annoncés pour une paire 48 V ; lot F).
        tension = tension_commune([info(m)["plage"] for m in modeles])
        if tension is None:
            continue          # modèles sans tension commune : configuration impossible, non affichée
        nom = " + ".join(f"{q} × {info(m)['nom']}" for m, q in modeles.items())
        if oid == "deux_finalistes":
            nom += f" ({tension} V)"
        elif oid == "qualification":
            nom = f"qualification : {nom} (48 V)"
        elif cf.get("libelle"):
            nom += f" ({cf['libelle']})"
        o = dict(id=oid, nom=nom, ids=ids, modeles=modeles, tension=tension, appr=appr(modeles),
                 statut=cf.get("statut"))
        # Notes de transfert : JUGEMENT, inchangées (2026-09-30).
        if oid in ("un_vainqueur", "deux_vainqueurs", "trois_vainqueurs"):
            o.update(transfert=3 if seuil else 5,
                     transfert_j=(f"JUGEMENT : 5 si k ≥ {f(seuil)} (sa famille gagne), 1 sinon ; "
                                  "k inconnu tant que le banc ne l'a pas mesuré → 3")
                                 if seuil else "exactement le modèle retenu pour S → 5")
        elif oid == "deux_finalistes":
            o.update(transfert=5, finalistes=True,
                     transfert_j="JUGEMENT : quel que soit k, le modèle S de la famille gagnante est sur le banc → 5")
        elif oid == "qualification":
            o.update(transfert=5, transfert_j=("JUGEMENT : les modèles S des deux familles en tête sont sur le "
                                               "banc, quel que soit k → 5"))
        elif oid == "feetech":
            o.update(transfert=1, transfert_j="autre fabricant, autre bus (TTL) que tous les finalistes → 1")
        else:
            o.update(transfert=1, transfert_j="configuration sans jugement de transfert écrit → 1 par prudence")
        opts.append(o)
    inc_toutes = b.get("inconnues_decisives") or {}
    # Une inconnue « decisive_si: bascule_dans_la_plage_plausible » ne compte que
    # si la bascule de k tombe au-dessus du plus petit rapport blocage / nominal
    # publié (borne basse plausible de k). Sinon, la mesurer ne change rien.
    rb = rapports_blocage(cat)
    borne_basse = min(x["rapport"] for x in rb) if rb else None
    k_bascule = r["fam_seuil"]["k"] if r["fam_seuil"] else None
    decisives = {}
    for nom_i, d in inc_toutes.items():
        if d.get("decisive_si") == "bascule_dans_la_plage_plausible":
            ok = k_bascule is not None and borne_basse is not None and k_bascule >= borne_basse
            d = dict(d, _decisive=ok, _pourquoi=(
                f"bascule k ≈ {f(k_bascule)} " + ("≥" if ok else "<") + f" borne basse plausible {f(borne_basse, 3)}"
                if k_bascule is not None else "aucune bascule dans le balayage"))
        elif isinstance(d.get("decisive_si"), dict) and "famille_gagne_dans_la_plage_plausible" in d["decisive_si"]:
            # Règle étendue (2026-09-30, nuit) : l'inconnue ne départage que des
            # membres de ces familles ; elle compte si l'une d'elles gagne en un
            # point du balayage situé dans la plage plausible (k ≥ borne basse).
            cibles = set(d["decisive_si"]["famille_gagne_dans_la_plage_plausible"])
            plage = [b_ for b_ in r["fam_balayage"] if borne_basse is not None and b_["k"] >= borne_basse]
            gagnes = sorted({b_["sens"]["nominal"] for b_ in plage})
            ok = bool(cibles & set(gagnes))
            d = dict(d, _decisive=ok, _pourquoi=(
                f"dans la plage plausible (k de {f(max(b_['k'] for b_ in plage), 1)} à {f(min(b_['k'] for b_ in plage), 1)}, "
                f"≥ {f(borne_basse, 3)}), la famille gagnante est toujours {', '.join(gagnes)} ; "
                + ("une famille concernée y gagne" if ok else f"aucune de ces familles ({', '.join(sorted(cibles))}) n'y gagne")
                if plage else "aucun point du balayage dans la plage plausible"))
        else:
            d = dict(d, _decisive=True, _pourquoi="toujours comptée")
        decisives[nom_i] = d
    inc = {k_: d for k_, d in decisives.items() if d["_decisive"]}

    def tranchees(ids):
        s = set(ids)
        out = []
        for nom_i, d in inc.items():
            reg = d["tranchee_si"]
            if ("contient_un" in reg and s & set(reg["contient_un"])) or \
               ("contient_tous" in reg and set(reg["contient_tous"]) <= s):
                out.append(nom_i)
        return out

    for o in opts:
        o["couts"], o["manquants"] = cout(o["ids"], o["tension"])
        o["cout"] = o["couts"][pays_liv[0]]
        o["tranchees"] = tranchees(o["ids"])
        part = len(o["tranchees"]) / len(inc) if inc else 0
        nd = 5 if inc and part >= 1 else (3 if part >= 0.5 else (2 if part > 0 else 0))
        o["notes"] = dict(valeur_decision=nd, apprentissage=o["appr"][0], transfert_S=o["transfert"],
                          cout=0 if o["manquants"] else seuils(o["cout"], (250, 400, 600, 900, 1300), (5, 4, 3, 2, 1), 0),
                          risque=jr[o["id"]]["note"])
        o["risque_j"] = jr[o["id"]]["justification"]
        o["etat"], o["reference"] = "admis", False
    pb = {k: v["poids"] for k, v in b["ponderes"].items()}
    r["_inconnues"] = decisives
    return opts, pb, sensibilite(opts, pb, crit["classe_S"]["sensibilite"]), (fa, fb, SA, SB, paire, tension_paire)


# L'estimation thermique du J4310 n'est plus recopiée ici (2026-09-30, 22 h 30) :
# `calculer()` la lit à la source, scripts/estimation_thermique.estimer(), au seuil
# thermique du protocole. Sans les images d'exports/thermique/, le script s'arrête
# et le dit (il ne tourne pas en construction Docker).

CRIT_S = ("capacite", "cout", "continuite", "fiabilite_fournisseur", "robustesse",
          "masse", "ouverture", "tension_securite", "disponibilite")


def verdict_texte(s, nom, fixes: bool) -> str:
    """Verdict. Poids FIXÉS : le vainqueur est une décision ; on dit s'il tient à ±50 %
    (tenue locale) et, pour information seulement, ce que donnent des poids quelconques."""
    n = sum(1 for *_, w in s["variations"] if w == s["nominal"])
    tir = f"{f(100 * s['freq'], 1)} %"
    if fixes:
        tenue = ("il **tient toutes les variations ±50 %**" if s["tous_pm"]
                 else f"il **ne tient que {n} variations ±50 % sur {len(s['variations'])}**")
        autre = max(((w, k_) for w, k_ in s["gagnes"].items() if w != s["nominal"]), key=lambda x: x[1], default=None)
        info = (f" Sur 1 000 jeux de poids **quelconques**, il gagne {tir} des tirages"
                + (f" ; « {nom.get(autre[0], autre[0])} » en gagne {f(100 * autre[1] / sum(s['gagnes'].values()), 1)} %"
                   if autre else "")
                + ". Cette dernière mesure dit seulement qu'**un autre principe de pondération** que "
                "celui de Jeremy choisirait autrement : elle n'affaiblit pas le choix fait avec le sien.")
        return f"**Aux poids décidés par Jeremy : {nom[s['nominal']]}** — {tenue}.{info}"
    if s["robuste"]:
        return f"**Classement ROBUSTE** : {nom[s['nominal']]}."
    return (f"**Options trop proches pour que l'analyse tranche** : {nom[s['nominal']]} en tête aux poids "
            "proposés — le choix dépend des poids, que Jeremy fixera.")


def doc_banc(r, opts, pb, sb, finalistes, date) -> str:
    fa, fb, SA, SB, paire, tension = finalistes
    cat = r["cat"]
    nomf = {fm["id"]: fm["nom"] for fm in r["fams"]}
    L = []
    A = L.append
    fixes = all(v.get("statut", "").startswith(("fixé", "DÉCIDÉ")) for v in r["crit"]["banc"]["ponderes"].values())
    inc = r.get("_inconnues") or {}
    A("# Comparatif du banc d'essai — v3\n")
    A(f"**Engendré** par `.venv/bin/python scripts/selection_multicritere.py --ecrire`, le {date}, "
      "après le comparatif des familles (`docs/choix-famille-actionneurs.md`). Aucun achat n'est "
      "proposé : ce comparatif prépare le choix de Jeremy (cadrage § 6 et § 13, question 12).\n")
    kd = inc.get("k_damiao")
    verif = bool(inc) and not any(d["_decisive"] for d in inc.values())
    if verif:
        A("> **Banc de VÉRIFICATION, pas de départage.** Aucune des inconnues n'est décisive (règle "
          "étendue du 2026-09-30, `criteres_selection.yaml`) : dans la plage plausible de k, aucune "
          "mesure du banc ne peut changer la décision de famille. Le banc **vérifie** une décision que "
          "les données publiées portent déjà ; il ne la prend pas. La valeur de décision (poids "
          f"{r['crit']['banc']['ponderes']['valeur_decision']['poids']}) vaut donc **0 pour toutes les "
          "options** : elle ne départage plus rien, et le classement se fait sur les autres critères.\n")
    if r["fam_seuil"] and kd is not None and not kd["_decisive"]:
        sf = r["fam_seuil"]
        A(f"**Où en est la décision.** Le choix de famille bascule à **k ≈ {f(sf['garde'])}** : au-dessus, "
          f"**{nomf[sf['gagnant']]}** ; en dessous, **{nomf[sf['nouveau']]}**. Mais cette bascule est "
          f"**sous la borne basse plausible de k** ({kd['_pourquoi']}) : si le Damiao se comporte comme les "
          "actionneurs RobStride, dont les rapports blocage / nominal sont publiés, **la famille est déjà "
          "décidée par les données**. La mesure de son k reste une **vérification**, pas un départage : "
          "elle n'est plus comptée comme décisive."
          + (" Il en va de même des deux inconnues propres à RobStride : elles ne comptent que si cette "
             "famille gagne, ce qui n'arrive que sous la bascule.\n" if verif
             else " La valeur du banc vient des autres inconnues.\n"))
    elif r["fam_seuil"]:
        sf = r["fam_seuil"]
        A(f"**Pourquoi ce banc compte.** Le choix de famille bascule au seuil **k ≈ {f(sf['garde'])}** : "
          f"au-dessus, **{nomf[sf['gagnant']]}** ; en dessous, **{nomf[sf['nouveau']]}**. k est le "
          "rapport entre le couple continu réel des actionneurs « condition non précisée » et leur "
          "nominal publié. **Il ne se décide pas, il se mesure** — c'est le rôle premier du banc.\n")
    A("---\n\n## 1 — Les options\n")
    pays_liv = r["bud"].get("livraison") or ["CH"]
    A("| Option | Inconnues décisives tranchées | Ce qu'elle apprend | Transfert à S | "
      + " | ".join(f"Coût TTC {p_}" for p_ in pays_liv) + " | Postes non chiffrés | Risque |")
    A("| --- | --- | --- | --- | " + " | ".join("---:" for _ in pays_liv) + " | --- | --- |")
    n_dec = sum(1 for d in inc.values() if d["_decisive"])
    for o in opts:
        A(f"| {o['nom']} | " + (f"{len(o['tranchees'])}/{n_dec} : {', '.join(o['tranchees']) or 'aucune'}"
                                if n_dec else "— (aucune n'est décisive)") + " | "
          f"{o['appr'][0]}/5 : {', '.join(o['appr'][1])} | {o['transfert']} — {o['transfert_j']} | "
          + " | ".join(f"{'≥ ' if o['manquants'] else ''}{f(o['couts'][p_], 0)} CHF" for p_ in pays_liv)
          + f" | {', '.join(o['manquants']) or '—'} | "
          f"{o['notes']['risque']} — {o['risque_j']} |")
    A("\nCoût TTC = (actionneurs + adaptateur + alimentation) × (1 + imprévus 15 %, provisoire) × "
      "(1 + TVA du pays de livraison : " + ", ".join(
          f"{p_} {f(100 * val(r['bud'][f'tva_{p_.lower()}']), 1)} %" for p_ in pays_liv)
      + f"). **Livraison possible en {' et en '.join(pays_liv)}** (`budget.yaml`, `livraison`) ; la note de "
      f"coût se prend sur {pays_liv[0]}. Tout est en CHF (taux BCE). Port, droits de douane et frais de "
      "dédouanement sont **inconnus**, non comptés. Alimentations : Mean Well RSP-320-24 (24 V) ou RSP-500-48 (48 V), Reichelt. "
      "Un poste non chiffré met la note de coût à 0.\n")
    A("**Adaptateur USB-CAN** : candleLight de Linux Automation (54,74 € TTC, vérifié), **prototype "
      "non conforme CE** selon son fabricant. **Alternative : CANable 2.0** (Openlight Labs), 35 USD "
      "**non vérifié** (page inaccessible), conformité CE **inconnue** ; livré avec le firmware slcan "
      "(**GPL-3.0**), compatible candleLight_fw (**MIT**) mais **sans CAN FD** sur la 2.0 ; licence "
      "du matériel non nommée.\n")
    if paire:
        A(f"**L'option à deux finalistes** tourne à **{tension} V**, pour une seule alimentation : "
          + " ; ".join(f"{cat['candidats'][x]['nom']}" for x in paire) + ". "
          + ("Le prix de la variante 48 V du Damiao n'est pas connu : son coût est donc incomplet.\n"
             if any(cat["candidats"][x]["prix"].get("valeur") is None for x in paire) else "\n"))
    if inc:
        A("**Les inconnues décisives** (règles écrites avant le calcul, `criteres_selection.yaml`) :\n")
        for k_, d in inc.items():
            A(f"- `{k_}` — {d['question']} — **{'décisive' if d['_decisive'] else 'NON décisive'}** "
              f"({d['_pourquoi']})")
        A("\nLa valeur de décision se note en **proportion** des inconnues décisives que l'option tranche.\n")
    A("---\n\n## 2 — Notes et score\n")
    A(f"| Critère | Poids ({'fixé par Jeremy' if fixes else 'proposé'}) | " + " | ".join(o["nom"] for o in opts) + " |")
    A("| --- | ---: | " + " | ".join("---:" for _ in opts) + " |")
    for k_ in pb:
        A(f"| {k_} | {pb[k_]} | " + " | ".join(str(o["notes"][k_]) for o in opts) + " |")
    A("| **score /5** | | " + " | ".join(f"**{f(score(o['notes'], pb))}**" for o in opts) + " |")
    nom = {o["id"]: o["nom"] for o in opts}
    A("\n## 3 — Sensibilité\n")
    A(f"Vainqueur aux poids proposés : **{nom[sb['nominal']]}**. "
      f"{sum(1 for *_, w in sb['variations'] if w == sb['nominal'])} variations ±50 % sur "
      f"{len(sb['variations'])} le laissent en tête.\n")
    A("| Option | Victoires sur 1 000 tirages |")
    A("| --- | ---: |")
    for w, k_ in sorted(sb["gagnes"].items(), key=lambda x: -x[1]):
        A(f"| {nom.get(w, w)} | {k_} |")
    A("\n## 4 — Verdict\n")
    A(verdict_texte(sb, nom, fixes) + "\n")
    s_max = max(score(o["notes"], pb) for o in opts)
    ex = [o for o in opts if abs(score(o["notes"], pb) - s_max) < 1e-9]
    if len(ex) > 1:
        A(f"**{len(ex)} options EX ÆQUO à {f(s_max)}** : " + " ; ".join(o["nom"] for o in ex)
          + f". « {nom[sb['nominal']]} » n'est en tête **que par l'ordre alphabétique de son "
          "identifiant**, qui départage les égalités dans le script : c'est un artefact d'écriture, "
          "pas un résultat. **À ces poids, le comparatif ne classe pas ces options entre elles.**\n")
    jumeaux = {}
    for o in opts:
        jumeaux.setdefault(tuple(o["notes"][k_] for k_ in pb), []).append(o)
    for grp in (g for g in jumeaux.values() if len(g) > 1):
        A("**Notes IDENTIQUES sur tous les critères** : " + " ; ".join(o["nom"] for o in grp)
          + ". **Aucun jeu de poids ne peut les séparer** : dans les tirages du § 3, les victoires "
          "comptées à l'une appartiennent à toutes, l'identifiant départageant l'égalité.\n")
    if verif:
        A("**Une note de jugement que la règle étendue interroge, et qui n'est PAS corrigée ici** "
          "(elle n'a pas été demandée) : le transfert à S des options « × Damiao » vaut 3 parce que "
          "« k inconnu tant que le banc ne l'a pas mesuré ». Si k n'est plus décisif, le J4310 est le "
          "modèle S de la famille retenue dans toute la plage plausible, et cette note serait 5. "
          "C'est à Jeremy de le décider ; le changement doit être daté avant d'être appliqué.\n")
    k_seul = [x for x in (SA, SB) if intervalle_continu(cat["candidats"][x], 0.5)["k_applique"]]
    if k_seul and verif:
        A("**Ce que chaque option vérifie.** L'hypothèse k ne touche que les actionneurs dont la "
          "condition de mesure n'est pas publiée : ici **"
          + ", ".join(cat["candidats"][x]["nom"] for x in k_seul)
          + "**. Mesurer son couple continu en blocage **vérifie** que k reste au-dessus de la bascule "
          "(critère d'abandon : `docs/protocole-banc.md`). Les options à plusieurs modèles ajoutent une "
          "comparaison directe dans la même condition, sans départager la famille.\n")
    elif k_seul:
        A("**Ce que chaque option tranche.** L'hypothèse k ne touche que les actionneurs dont la "
          "condition de mesure n'est pas publiée : ici **"
          + ", ".join(cat["candidats"][x]["nom"] for x in k_seul)
          + "**. Mesurer son couple continu réel **suffit à trancher le seuil**, et les options "
          "« × vainqueur » le font. L'option à deux finalistes ajoute la vérification de l'autre "
          "finaliste **dans la même condition** : la comparaison devient directe, au lieu de "
          "s'appuyer sur sa fiche.\n")
    ca = r.get("critere")
    if ca and ca["sans_objet"]:
        nomf_ = {fm["id"]: fm["nom"] for fm in r["fams"]}
        A("### Critère d'abandon — SANS OBJET à ce jour (" + ca["statut"] + ")\n")
        A(f"La famille de **{ca['nom']}** ({nomf_.get(ca['famille'], ca['famille'])}) **ne gagne à aucun k "
          "du balayage** : gagnants " + ", ".join(nomf_[g] for g in ca["gagnants"]) + ". Un critère "
          "d'abandon dit quand rouvrir un choix ; il n'y a pas de choix à rouvrir pour cet actionneur. "
          "Le seuil de 1,75 N·m de `docs/protocole-banc.md` § 2 bis ne repose plus sur rien. Le seuil "
          f"thermique unique reste {f(ca['t_lim'], 0)} °C ({ca['t_lim_source']}).\n")
    elif ca:
        e_ = r["estimation"]
        rb_ = rapports_blocage(cat)
        rmin_, rmax_ = min(x["rapport"] for x in rb_), max(x["rapport"] for x in rb_)
        A("### Critère d'abandon — CALCULÉ, " + ca["statut"] + "\n")
        A(f"> Si le couple continu de **{ca['nom']}** (clé : {ca['cle']}), mesuré **au blocage** sur la "
          f"plaque de 70 × 70 mm, à l'équilibre sous **{f(ca['t_lim'], 0)} °C** de bobinage "
          f"({ca['t_lim_source']}), est inférieur à **{f(ca['seuil'])} N·m**, le choix de famille est "
          "**rouvert**.\n")
        A(f"- **D'où vient ce seuil** : garde de la bascule k = {f(ca['k_garde'])} (dernier k où la famille "
          f"recommandée gagne ; l'autre gagne dès {f(ca['k_bascule'])}) × nominal publié {f(ca['nominal'], 1)} "
          f"N·m. La bascule est connue au centième : le seuil est **entre {f(ca['seuil_bas'])} et "
          f"{f(ca['seuil'])} N·m** ; la valeur haute est retenue, la plus exigeante pour la famille recommandée.")
        A(f"- **Un seul seuil thermique**, {f(ca['t_lim'], 0)} °C, pour la mesure ET pour l'estimation "
          f"(`scripts/estimation_thermique.py`) : k estimé {f(e_['k_bas'])}–{f(e_['k_haut'])} en rotation ; "
          f"décoté par les rapports blocage / nominal RobStride ({f(rmin_, 3)}–{f(rmax_, 3)}) : "
          f"**{f(e_['k_bas'] * rmin_)}–{f(e_['k_haut'] * rmax_)} au blocage** (hypothèse sur hypothèse), soit "
          f"{f(e_['k_bas'] * rmin_ * ca['nominal'])}–{f(e_['k_haut'] * rmax_ * ca['nominal'])} N·m contre "
          f"{f(ca['seuil'])} N·m.")
        A("- **Réserve** : les valeurs RobStride (en blocage, publiées) portent le seuil thermique de leur "
          "constructeur, pas celui du protocole ; l'estimation vient des courbes **24 V** (le manuel donne "
          "les mêmes couples à 48 V). Le texte de `docs/protocole-banc.md` § 2 bis (1,75 N·m) est antérieur "
          "à ce calcul.\n")
    A("---\n\n## 5 — Protocole de mesure : les couples continus en condition IDENTIQUE\n")
    A("**Le protocole complet, avec sa section SÉCURITÉ** (alimentation à limitation de courant, "
      "arrêt d'urgence matériel, limites logicielles, bras de levier, chauffe au rotor bloqué, ce "
      "qu'on ne fait jamais seul) et la consignation de chaque mesure dans `params/mesures.yaml` : "
      "`docs/protocole-banc.md` (*proposé*). Résumé :\n")
    A("But : remplacer l'hypothèse k par une mesure, sur les deux finalistes, **dans la même "
      "condition**. Les fiches ne sont pas comparables entre elles : plaques différentes, ou condition "
      "non précisée. Ce protocole est **proposé**, pas décidé.\n")
    A("1. **Même montage.** Chaque actionneur est fixé sur la **même plaque d'aluminium de 70 × 70 mm** "
      "(la plus petite condition publiée, celle du RS05 et de l'EduLite 05). L'épaisseur et la "
      "matière sont notées. La plaque est posée sur le même support isolant.")
    A("2. **Même alimentation**, à la même tension (celle de l'option), et le même bus CAN au même "
      "débit.")
    A("3. **Rotor bloqué**, par un bras de levier sur un dynamomètre ou une balance, longueur notée. "
      "Le couple **réel** est lu sur le dynamomètre, et le couple **déclaré** par la télémétrie : leur "
      "écart est lui-même une mesure. *Le blocage est la condition la plus proche d'un robot qui tient "
      "debout ; une mesure en rotation demanderait un frein, et n'est pas prévue ici.*")
    A("4. **Mêmes paliers de couple**, par ordre croissant, sur les deux actionneurs : le continu "
      "publié le plus bas des deux, puis des paliers de 10 % au-dessus, jusqu'au seuil k × nominal "
      "à départager.")
    A("5. **Même durée** : chaque palier est tenu jusqu'à l'équilibre thermique (variation < 1 °C sur "
      "5 min), ou au plus 30 min, ou jusqu'à 10 °C sous la protection thermique du constructeur.")
    A("6. **Relevés** à 1 Hz : température bobinage et driver (télémétrie), température du boîtier "
      "(thermocouple), courant, couple réel. La **température ambiante** est notée au début et à la "
      "fin de chaque palier.")
    A("7. **Résultat** : le plus haut couple tenu à l'équilibre sous la limite thermique est le "
      "**continu mesuré**, dans cette condition. Divisé par le nominal publié, il donne le **k "
      "mesuré** de chaque actionneur, à reporter dans le catalogue comme une mesure (fiche 0041) :")
    A("   il " + ("**vérifie** la décision de famille (critère d'abandon écrit avant la mesure, "
                 "`docs/protocole-banc.md`).\n" if verif else "départage les finalistes au seuil du § 1.\n"))
    A("---\n\n## 6 — Ce que ce comparatif ne dit pas\n")
    A(f"- Les poids du banc sont **{'fixés par Jeremy' if fixes else 'proposés'}** ; les notes de "
      "transfert et de risque sont de **jugement**, justifiées ligne par ligne.")
    A("- L'option Feetech n'a **ni prix vérifié ni alimentation 12 V chiffrée** : son coût est "
      "inconnu.")
    A("- La mesure au rotor bloqué ne dit rien du rendement en rotation ; elle compare les deux "
      "finalistes entre eux, dans la même condition.")
    A("- **La dispersion entre exemplaires** exige au moins **2 exemplaires d'un même modèle** : trois "
      "modèles à un exemplaire n'en mesurent aucune (corrigé le 2026-10-01, audit externe). Deux "
      "exemplaires donnent un ordre de grandeur (`docs/protocole-banc.md` § 2 ter) ; l'étude externe du "
      "30-09 en demandait au moins 3 (§ 15.2). Configurations : `params/banc.yaml`, composition **non "
      "décidée**.")
    return "\n".join(L) + "\n"


def _seuil_fin(evalue, balayage, cle_nominal):
    """Affine au centième le k où le vainqueur change (None si aucun)."""
    gagnant = balayage[0]["sens"]["nominal"]
    bascule = next((b_["k"] for b_ in balayage if b_["sens"]["nominal"] != gagnant), None)
    if bascule is None:
        return None, None
    haut = max(b_["k"] for b_ in balayage if b_["k"] > bascule)
    kk = haut
    while kk > bascule + 1e-9:
        kk = round(kk - 0.01, 2)
        w = evalue(kk)
        if w != gagnant:
            return bascule, dict(k=kk, garde=round(kk + 0.01, 2), gagnant=gagnant, nouveau=w)
    return bascule, None


# Deux scores (PROPOSITION, 2026-10-01) : les mêmes notes, les poids décidés
# renormalisés dans chaque groupe. Le verdict retenu reste le score unique.
GROUPE_TECH = ("capacite", "continuite", "robustesse", "masse", "ouverture", "tension_securite")
GROUPE_APPRO = ("cout", "fiabilite_fournisseur", "disponibilite")
K2_PAS = [round(1.0 - 0.05 * i, 2) for i in range(11)]          # 1,00 → 0,50
K2_CODES = {"damiao": "D", "robstride_el05": "E", "robstride": "R", "cubemars": "C", "myactuator": "M"}


def carte_k2(cat, crit, bud, analyse, ref, poids, autres: str) -> list:
    """Gagnant des familles pour k_J4310 × k_EL05 balayés SÉPARÉMENT (information).

    2026-10-01, lot E (PROPOSÉ par Claude, arbitrage) : le RS05 garde sa
    valeur en blocage publiée. Les AUTRES candidats sans valeur en blocage
    (CubeMars, MyActuator…) suivent `autres` : « min » (le plus petit des
    deux k : aucun autre n'est supposé meilleur que les deux balayés) ou
    « 1.0 » (leur cas le plus favorable). Ne change pas le verdict.
    """
    out = []
    for kj in K2_PAS:
        ligne = []
        for ke in K2_PAS:
            k = {"dm_j4310_48v": kj, "edulite05": ke, "_defaut": min(kj, ke) if autres == "min" else 1.0}
            cs = evaluer_S(cat, crit, bud, analyse, ref, k)
            ligne.append(vainqueur(evaluer_familles(cat, crit, bud, analyse, ref, cs, k), poids))
        out.append(ligne)
    return out


def calculer(cartes: bool = True):
    cat = D.charger_catalogue()
    crit = yaml.safe_load(CRITERES.read_text(encoding="utf-8"))
    bud = yaml.safe_load(D.BUDGET.read_text(encoding="utf-8"))
    analyse = AM.analyser(AM.SERIE)
    ref = D.reference(cat, analyse)
    poids = {k: v["poids"] for k, v in crit["classe_S"]["ponderes"].items()}
    sens_cfg = crit["classe_S"]["sensibilite"]
    # DIMENSION DONNÉES : pour chaque hypothèse k sur les couples continus
    # « non précisés », les candidats S ET les familles, chacun avec sa
    # sensibilité aux poids.
    balayage, fam_balayage = [], []
    for kk in crit["classe_S"]["ponderes"]["capacite"]["k_non_precisee"]:
        ck = evaluer_S(cat, crit, bud, analyse, ref, kk)
        balayage.append(dict(k=kk, cands=ck, sens=sensibilite(ck, poids, sens_cfg)))
        fk = evaluer_familles(cat, crit, bud, analyse, ref, ck, kk)
        fam_balayage.append(dict(k=kk, fams=fk, sens=sensibilite(fk, poids, sens_cfg)))
    cands, sens = balayage[0]["cands"], balayage[0]["sens"]     # k = 1,0 : référence
    bascule, seuil_fin = _seuil_fin(
        lambda kk: vainqueur(evaluer_S(cat, crit, bud, analyse, ref, kk), poids), balayage, "cands")
    fam_bascule, fam_seuil = _seuil_fin(
        lambda kk: vainqueur(evaluer_familles(cat, crit, bud, analyse, ref,
                                              evaluer_S(cat, crit, bud, analyse, ref, kk), kk), poids),
        fam_balayage, "fams")
    # Les tailles « prudentes » de référence pour l'affichage : k le plus bas
    # du balayage (borne basse de l'hypothèse).
    fams_bas = fam_balayage[-1]["fams"]
    estimation = ET.estimer()
    ca_cfg = crit["banc"]["critere_abandon"]
    c_ab = cat["candidats"][ca_cfg["actionneur"]]
    nominal_ab = val(c_ab["couple_continu_Nm"])
    critere = None
    # Le critère n'a de sens que si la bascule oppose la famille dont
    # l'actionneur est le membre S (celle qui gagne au-dessus) à une autre.
    # Sinon, il est déclaré SANS OBJET, et dit pourquoi — jamais calculé à vide.
    fam_de_l_actionneur = next((fid for fid, fm in cat["familles"].items()
                                if fm.get("S") == ca_cfg["actionneur"]), None)
    gagnants = sorted({b_["sens"]["nominal"] for b_ in fam_balayage})
    if fam_seuil and fam_seuil["gagnant"] != fam_de_l_actionneur:
        critere = dict(sans_objet=True, nom=c_ab["nom"], famille=fam_de_l_actionneur, gagnants=gagnants,
                       statut=ca_cfg["statut"], t_lim=estimation["t_lim"], t_lim_source=estimation["t_lim_source"])
    elif fam_seuil:
        critere = dict(sans_objet=False, actionneur=ca_cfg["actionneur"], nom=c_ab["nom"], cle=D.cle_revision(c_ab),
                       nominal=nominal_ab, k_garde=fam_seuil["garde"], k_bascule=fam_seuil["k"],
                       seuil=round(fam_seuil["garde"] * nominal_ab, 2),
                       seuil_bas=round(fam_seuil["k"] * nominal_ab, 2),
                       t_lim=estimation["t_lim"], t_lim_source=estimation["t_lim_source"],
                       statut=ca_cfg["statut"])
    # `cartes=False` : les tests s'en passent (deux fois 121 évaluations).
    cartes_k2 = ({a_: carte_k2(cat, crit, bud, analyse, ref, poids, a_) for a_ in ("min", "1.0")}
                 if cartes else {})
    return dict(cartes_k2=cartes_k2, estimation=estimation, critere=critere, cat=cat, crit=crit, bud=bud, ref=ref, analyse=analyse, poids=poids,
                cands=cands, sens=sens, S_id=sens["nominal"], balayage=balayage,
                bascule=bascule, seuil_fin=seuil_fin, fam_balayage=fam_balayage,
                fam_bascule=fam_bascule, fam_seuil=fam_seuil, fams=fam_balayage[0]["fams"],
                fams_bas=fams_bas, marge=val(cat["dimensionnement"]["marge"]))


def tableau_familles(r) -> list[str]:
    """Le tableau des familles : S/M/L prudent (k bas) – optimiste, coûts, continuité."""
    kbas = r["fam_balayage"][-1]["k"]
    bas = {x["id"]: x for x in r["fams_bas"]}
    L = [f"| Famille | S : prudent (k = {f(kbas, 1)}) – optimiste | M | L | Jambes S (TTC CHF) | Jambes M | Jambes L | Continuité | Trous |",
         "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |"]
    for fm in r["fams"]:
        cells = []
        for tl in TAILLES:
            x, xb = fm["tailles"][tl], bas[fm["id"]]["tailles"][tl]
            cells.append("**TROU**" if not x else f"{f(xb['H_prud'])}–{f(x['H_opt'])} m")
        jam = []
        for tl in TAILLES:
            x = fm["tailles"][tl]
            if not x:
                jam.append("—")
            else:
                j_ = x["jambes"]
                jam.append(f"{'≥ ' if j_['inconnus'] else ''}{j_['ttc']:,.0f}".replace(",", " "))
        L.append(f"| {fm['nom']} | " + " | ".join(cells) + " | " + " | ".join(jam)
                 + f" | {fm['notes']['continuite']}/5 | {', '.join(fm['trous']) or '—'} |")
    return L


def frontieres_k2(carte, borne) -> str:
    """Décrit, en phrases calculées, où le gagnant change sur la carte « min »."""
    lignes = []
    noms = {"damiao": "Damiao", "robstride_el05": "RobStride avec EduLite 05", "robstride": "RobStride avec RS05",
            "cubemars": "CubeMars", "myactuator": "MyActuator"}
    for fam in sorted({w for l in carte for w in l}):
        cases = [(kj, ke) for kj, l in zip(K2_PAS, carte) for ke, w in zip(K2_PAS, l) if w == fam]
        kj_min, kj_max = min(c[0] for c in cases), max(c[0] for c in cases)
        ke_min, ke_max = min(c[1] for c in cases), max(c[1] for c in cases)
        lignes.append(f"- **{noms.get(fam, fam)}** gagne sur {len(cases)} cases sur {len(K2_PAS) ** 2} : "
                      f"k J4310 de {f(kj_min)} à {f(kj_max)}, k EL05 de {f(ke_min)} à {f(ke_max)}.")
    # frontière EL05 seule, à k J4310 = 0,80 (milieu de la plage plausible) : où l'EL05 cesse de gagner
    for kj_ref in (0.80,):
        l = carte[K2_PAS.index(kj_ref)]
        chg = [(K2_PAS[i], K2_PAS[i + 1], l[i], l[i + 1]) for i in range(len(l) - 1) if l[i] != l[i + 1]]
        for k1, k2, w1, w2 in chg:
            pos = "AU-DESSUS de" if k2 >= borne else ("SOUS" if k1 < borne else "À CHEVAL sur")
            lignes.append(f"- À k J4310 = {f(kj_ref)} : le gagnant passe de {noms.get(w1, w1)} à {noms.get(w2, w2)} "
                          f"entre k EL05 = {f(k1)} et {f(k2)}, **{pos} la borne plausible {f(borne, 3)}** : dans "
                          "la plage plausible, k de l'EduLite 05 change la décision.")
    return "\n".join(lignes)


def doc_familles(r, date) -> str:
    nom_k2 = {fm["id"]: fm["nom"] for fm in r["fams"]}
    pd = r["poids"]
    poids, crit = r["poids"], r["crit"]
    L = []
    A = L.append
    A("# Choix de la famille d'actionneurs — comparatif multicritère v2\n")
    A(f"**Engendré** par `.venv/bin/python scripts/selection_multicritere.py --ecrire`, le {date}. "
      "Ne pas éditer à la main. **C'est le document de décision** : il remplace "
      "`docs/choix-classe-S.md` (v1, conservé, méthode corrigée). Aucune fiche, aucun achat "
      "proposé (CLAUDE.md, règle d'achat c) : il prépare un choix de Jeremy.\n")
    A("**Ce qui a changé depuis la v1** (relecture externe du 30-09-2026 ; chaque changement est "
      "daté dans `params/criteres_selection.yaml`, section `modifications`) :\n")
    A("1. **La taille n'est plus éliminatoire** : c'est une sortie de la démarche inversée "
      "(fiche 0047). Elle est notée. Seule la télémétrie élimine.")
    A("2. **La capacité est un intervalle.** Taille *optimiste* (le nominal publié le plus "
      "favorable) et *prudente* (en blocage si publié ; sinon la plus petite plaque publiée ; "
      "sinon — condition non précisée — le nominal × **k**). k est une **hypothèse**, balayée de "
      "1,0 à 0,5.")
    A("3. **On compare des familles S → M → L**, pas des modèles. La continuité se mesure dans "
      "chaque famille, et un membre absent est un **trou**, affiché.\n")
    fixes_hdr = all(v.get("statut", "").startswith(("fixé", "DÉCIDÉ")) for v in r["crit"]["classe_S"]["ponderes"].values())
    q_ = (r["crit"]["classe_S"].get("questions_ouvertes") or {}).get("criteres_manquants")
    A("Poids : " + ("**décidés par Jeremy le 2026-09-30 (~23 h)**, validés tels quels après avoir été "
                    "d'abord attribués à tort (`criteres_selection.yaml`, `modifications`)" if fixes_hdr else
                    "**PROPOSÉS, appliqués, NON validés par Jeremy**")
      + " (capacité 18, continuité 18, coût 15, fiabilité 15, "
      "robustesse 12, disponibilité 7, masse, ouverture, tension 5 chacun). Marge : 1,5 (fiche 0051). "
      "Toutes les tailles "
      "sont des **plafonds optimistes** : la marche de référence était écrêtée (cadrage § 3).\n")
    if q_:
        A(f"> **Réserve de Jeremy, question OUVERTE** : « {q_['texte']} » ({q_['auteur']}). "
          f"{q_['statut']}.\n")
    A("---\n\n## 1 — Les familles\n")
    L.extend(tableau_familles(r))
    A("\nTailles en mètres, à marge 1,5, configuration homogène de chaque membre. « Prudent » est "
      "calculé à la borne basse de l'hypothèse k ; pour RobStride, c'est la valeur **en blocage** "
      "publiée, qui ne dépend pas de k. Jambes = phase `jambes_v1` de `params/budget.yaml` "
      "(12 actionneurs, électronique connue, imprévus et TVA) ; « ≥ » : la structure n'est pas "
      "chiffrée.\n")
    sans_rev = [fm_t["nom"] for fm in r["fams"] for fm_t in fm["tailles"].values()
                if fm_t and not (r["cat"]["candidats"][fm_t["id"]].get("prix_revendeur")
                                 or (r["cat"].get("comparatif_S", {}).get(fm_t["id"]) or {}).get("prix_revendeur"))
                and r["cat"]["candidats"][fm_t["id"]]["prix"].get("devise") == "CNY"]
    A("**Prix.** Chaque membre est chiffré au prix **revendeur** quand il a été relevé (pour RobStride : "
      "Seeed, hors taxe) ; sinon au prix du catalogue. "
      + ("Restent au seul prix constructeur en yuans, donc sous-estimés : " + ", ".join(sorted(set(sans_rev))) + ".\n"
         if sans_rev else "Plus aucun membre de famille n'est chiffré au seul prix constructeur en yuans.\n"))
    A("### Membres, trous et alternatives\n")
    for fm in r["fams"]:
        A(f"**{fm['nom']}**\n")
        for tl in TAILLES:
            x = fm["tailles"][tl]
            if not x:
                A(f"- {tl} : **TROU** de gamme.")
                continue
            iv = x["iv"]
            A(f"- {tl} : {x['nom']} — clé : {D.cle_revision(r['cat']['candidats'][x['id']])} — pointe {f(x['pointe'], 1)} N·m ; continu optimiste "
              f"{f(iv['optimiste'])} N·m, prudent {f(iv['prudent'])} N·m ({iv['base_prudente']}) ; "
              f"{x['tension']} V, plage {x['plage'] if x['plage'] else 'inconnue'}")
        if fm["alternatives"]:
            A(f"- alternatives : " + "; ".join(f"{k_} = {', '.join(v)}" for k_, v in fm["alternatives"].items()))
        A(f"- continuité : {fm['justif']['continuite']}")
        if fm["note_famille"]:
            A(f"- note : {fm['note_famille'].strip()}")
        A("")
    A("---\n\n## 2 — Notes (membre S, et continuité de famille) à k = 1,0\n")
    A("Les critères autres que la continuité se notent sur le **membre S**, le premier robot.\n")
    fams = r["fams"]
    A(f"| Critère | Poids ({'fixé' if fixes_hdr else 'proposé'}) | " + " | ".join(fm["nom"].split(" (")[0] + (" EL05" if "el05" in fm["id"] else "") for fm in fams) + " |")
    A("| --- | ---: | " + " | ".join("---:" for _ in fams) + " |")
    for k_ in CRIT_S:
        A(f"| {k_} | {poids[k_]} | " + " | ".join(str(fm["notes"][k_]) for fm in fams) + " |")
    A("| **score /5** | | " + " | ".join(f"**{f(score(fm['notes'], poids))}**" for fm in fams) + " |")
    A("\n### Justification de chaque note\n")
    for fm in fams:
        A(f"**{fm['nom']}**\n")
        for k_ in CRIT_S:
            A(f"- {k_} = {fm['notes'][k_]} — {fm['justif'][k_]}")
        A("")
    A("---\n\n## 3 — La dimension « données » : le vainqueur pour chaque k\n")
    A(f"| k | Famille gagnante (poids {'fixés' if fixes_hdr else 'proposés'}) | Tient ±50 % | Tirages quelconques gagnés |")
    A("| ---: | --- | --- | ---: |")
    nom = {fm["id"]: fm["nom"] for fm in fams}
    for b_ in r["fam_balayage"]:
        s_ = b_["sens"]
        A(f"| {f(b_['k'], 1)} | {nom[s_['nominal']]} | "
          f"{'oui, toutes' if s_['tous_pm'] else 'NON, pas toutes'} | {f(100 * s_['freq'], 1)} % |")
    fixes_f = all(v.get("statut", "").startswith(("fixé", "DÉCIDÉ")) for v in crit["classe_S"]["ponderes"].values())
    A("\n**Verdict à k = 1,0.** " + verdict_texte(r["fam_balayage"][0]["sens"], nom, fixes_f))
    A("\n**Verdict à la borne basse (k = " + f(r["fam_balayage"][-1]["k"], 1) + ").** "
      + verdict_texte(r["fam_balayage"][-1]["sens"], nom, fixes_f) + "\n")
    if r["fam_seuil"]:
        sf = r["fam_seuil"]
        A(f"\n**Seuil de bascule : {nom[sf['gagnant']]} gagne jusqu'à k = {f(sf['garde'])} ; "
          f"{nom[sf['nouveau']]} gagne dès k = {f(sf['k'])}.**\n")
        A("En clair : le classement dépend du rapport entre le couple continu **réel** des "
          "actionneurs « condition non précisée » et leur nominal publié. **C'est ce rapport que le "
          "banc doit mesurer**, dans une condition identique pour les deux finalistes "
          "(`docs/comparatif-banc.md`).\n")
    else:
        A("\n**Aucune bascule entre k = 1,0 et 0,5** : le vainqueur ne dépend pas de l'hypothèse k.\n")
    A("---\n\n## 3 bis — Ce que les données disent de k\n")
    rb = rapports_blocage(r["cat"])
    A("Un seul fabricant publie à la fois un couple nominal (en rotation, sur plaque) **et** un "
      "couple en blocage : RobStride (PDF du 17-09-2026). Leur rapport est une mesure constructeur de "
      "ce que k représente — pour **ses** actionneurs, dans **ses** conditions.\n")
    A("| Actionneur | Blocage (N·m) | Nominal (N·m) | Blocage / nominal |")
    A("| --- | ---: | ---: | ---: |")
    for x in rb:
        A(f"| {x['nom']} | {f(x['blocage'], 1)} | {f(x['nominal'], 1)} | **{f(x['rapport'], 3)}** |")
    moy = sum(x["rapport"] for x in rb) / len(rb) if rb else None
    A(f"| **moyenne** | | | **{f(moy, 3)}** |\n")
    if r["fam_seuil"] and moy is not None:
        sf = r["fam_seuil"]
        cote = "AU-DESSUS" if moy > sf["garde"] else ("SOUS" if moy < sf["k"] else "AU NIVEAU")
        A(f"**Position par rapport au seuil de bascule (k ≈ {f(sf['garde'])}) : la moyenne RobStride, "
          f"{f(moy, 3)}, est {cote} du seuil.** "
          + ("Si les actionneurs sans valeur en blocage se comportaient comme ceux de RobStride, "
             f"le vainqueur serait « {nomf_[sf['gagnant']] if (nomf_ := {fm['id']: fm['nom'] for fm in r['fams']}) else ''} »"
             if moy >= sf["k"] else
             f"Si les actionneurs sans valeur en blocage se comportaient comme ceux de RobStride, "
             f"le vainqueur serait « {nomf_[sf['nouveau']] if (nomf_ := {fm['id']: fm['nom'] for fm in r['fams']}) else ''} »")
          + f" — mais l'écart entre les quatre rapports ({f(min(x['rapport'] for x in rb), 3)} à "
          f"{f(max(x['rapport'] for x in rb), 3)}) couvre le seuil : **les données constructeur ne "
          "tranchent pas, le banc tranchera.**\n" if min(x["rapport"] for x in rb) < sf["garde"] < max(x["rapport"] for x in rb)
          else ".\n")
    elif moy is not None:
        A("**Aucune bascule entre k = 1,0 et 0,5** : quelle que soit la valeur de k dans cette plage, "
          "le vainqueur ne change pas.\n")
    A("*Réserve* : ces rapports sont ceux d'un fabricant, pour une condition de blocage qu'il définit. "
      "Rien ne garantit qu'un Damiao ou un CubeMars se comporte pareil.\n")
    if rb:
        kr_bas, kr_haut = r["estimation"]["k_bas"], r["estimation"]["k_haut"]
        rmin, rmax = min(x["rapport"] for x in rb), max(x["rapport"] for x in rb)
        kb_bas, kb_haut = kr_bas * rmin, kr_haut * rmax
        A("### k au blocage du J4310 : une hypothèse sur une hypothèse\n")
        A(f"L'estimation thermique (`scripts/estimation_thermique.py`, lue à la source) donne, **en rotation** à "
          f"120 rpm et 24 V, dans la condition de l'essai constructeur, **au seuil thermique du protocole "
          f"({f(r['estimation']['t_lim'], 0)} °C : {r['estimation']['t_lim_source']})**, "
          f"**k ≈ {f(kr_bas)}–{f(kr_haut)}**. Un robot "
          "debout travaille près du blocage. En décotant cette estimation par les rapports blocage / "
          f"nominal de RobStride ci-dessus ({f(rmin, 3)} à {f(rmax, 3)}), le k du J4310 **au blocage** "
          f"serait de l'ordre de **{f(kb_bas)}–{f(kb_haut)}** ({f(kr_bas)} × {f(rmin, 3)} à "
          f"{f(kr_haut)} × {f(rmax, 3)}).\n")
        fam_dm = next((fid for fid, fm_ in r["cat"]["familles"].items()
                       if fm_.get("S") == r["crit"]["banc"]["critere_abandon"]["actionneur"]), None)
        if r["fam_seuil"] and fam_dm not in (r["fam_seuil"]["gagnant"], r["fam_seuil"]["nouveau"]):
            A(f"**La bascule (k ≈ {f(r['fam_seuil']['k'])}) n'oppose pas la famille de cet actionneur** : "
              "situer cette fourchette par rapport à elle ne décide rien. Elle reste une information "
              "sur le J4310, pas un argument de choix.\n")
        elif r["fam_seuil"]:
            sf = r["fam_seuil"]
            pos = ("**toujours au-dessus de la bascule**" if kb_bas > sf["garde"]
                   else "**à cheval sur la bascule**" if kb_haut >= sf["k"] else "**sous la bascule**")
            A(f"Cette fourchette est {pos} (k ≈ {f(sf['k'])}). **C'est une hypothèse sur une "
              "hypothèse** : une courbe numérisée, puis le comportement d'un autre fabricant. Elle ne "
              "vaut pas une mesure ; elle dit seulement que les deux estimations disponibles vont dans "
              "le même sens que la borne plausible.\n")
    A("---\n\n## 3 ter — k en deux dimensions : information, ne change pas le verdict\n")
    A("*PROPOSÉ par Claude (arbitrage, 2026-10-01), d'après l'audit externe ChatGPT du 2026-10-01.* "
      "Le balayage du § 3 applique **le même k** à tous les actionneurs sans valeur en blocage. Ici, "
      "**k du J4310 (lignes) et k de l'EduLite 05 (colonnes)** sont balayés séparément, de 1,0 à 0,5 par "
      "pas de 0,05. Le RS05 garde sa valeur en blocage publiée. Lettre = famille gagnante aux poids "
      "décidés : " + ", ".join(f"**{v}** {nom_k2.get(k_, k_)}" for k_, v in K2_CODES.items()) + ".\n")
    for a_, titre in (("min", "Les autres candidats sans valeur en blocage suivent le plus petit des deux k"),
                      ("1.0", "Les autres candidats sans valeur en blocage restent à k = 1,0 (leur cas le plus favorable)")):
        A(f"**{titre}.**\n")
        A("| k J4310 \\ k EL05 | " + " | ".join(f(x) for x in K2_PAS) + " |")
        A("| ---: | " + " | ".join(":-:" for _ in K2_PAS) + " |")
        for kj, ligne in zip(K2_PAS, r["cartes_k2"][a_]):
            A(f"| {f(kj)} | " + " | ".join(K2_CODES.get(w, "?") for w in ligne) + " |")
        A("")
    rb2 = rapports_blocage(r["cat"])
    borne2 = min(x["rapport"] for x in rb2) if rb2 else None
    A(f"**Lecture, par rapport à la borne basse plausible de k ({f(borne2, 3)}).** La carte « min » "
      "est la lecture prudente. La carte « 1,0 » montre ce que donnerait l'hypothèse la plus favorable "
      "accordée aux autres fabricants : un **artefact** de cette hypothèse, pas un résultat.\n")
    A(frontieres_k2(r["cartes_k2"]["min"], borne2))
    cases_d = [kj for kj, l in zip(K2_PAS, r["cartes_k2"]["min"]) for w in l if w == "damiao"]
    if cases_d:
        e2 = r["estimation"]
        rmin2, rmax2 = min(x["rapport"] for x in rb2), max(x["rapport"] for x in rb2)
        A(f"- **Damiao ne gagne qu'à k J4310 ≥ {f(min(cases_d))}.** L'estimation thermique (au seuil "
          f"de {f(e2['t_lim'], 0)} °C) donne {f(e2['k_bas'])}–{f(e2['k_haut'])} **en rotation**, et "
          f"{f(e2['k_bas'] * rmin2)}–{f(e2['k_haut'] * rmax2)} **au blocage** (hypothèse sur hypothèse). "
          "La zone Damiao est donc à la limite haute, ou au-delà, de ce que les données laissent attendre.")
    A("")
    A("---\n\n## 3 quater — Deux scores, technique et approvisionnement : PROPOSITION\n")
    A("*PROPOSÉ par Claude (arbitrage, 2026-10-01), d'après l'audit externe ChatGPT du 2026-10-01.* "
      "**Le verdict retenu reste celui du § 3**, au score unique. Ici, les mêmes notes sont séparées en "
      "deux scores, avec les poids décidés **renormalisés dans chaque groupe** :\n")
    A("- **technique** : " + ", ".join(f"{k_} {pd[k_]}" for k_ in GROUPE_TECH) + f" (somme {sum(pd[k_] for k_ in GROUPE_TECH)}) ;")
    A("- **approvisionnement, daté** : " + ", ".join(f"{k_} {pd[k_]}" for k_ in GROUPE_APPRO)
      + f" (somme {sum(pd[k_] for k_ in GROUPE_APPRO)}). Prix, garanties et revendeurs relevés le 30-09 "
      "et le 01-10-2026 : ce score **vieillit**, le technique beaucoup moins.\n")
    A("| k | Classement technique | Classement approvisionnement |")
    A("| ---: | --- | --- |")
    nomc = {fm["id"]: fm["nom"].split(" (")[0] + (" EL05" if "el05" in fm["id"] else "") for fm in r["fams"]}
    for b_ in r["fam_balayage"]:
        if b_["k"] < 0.5 - 1e-9:
            continue
        cl = {}
        for g_, grp in (("t", GROUPE_TECH), ("a", GROUPE_APPRO)):
            pg = {k_: pd[k_] for k_ in grp}
            tri = sorted(b_["fams"], key=lambda x: -score(x["notes"], pg))
            cl[g_] = " > ".join(f"{nomc[x['id']]} {f(score(x['notes'], pg))}" for x in tri)
        A(f"| {f(b_['k'], 1)} | {cl['t']} | {cl['a']} |")
    A("\nL'approvisionnement ne dépend pas de k : ses notes ne lisent ni la capacité ni la thermique. "
      "Une famille en tête des deux classements à la fois est robuste à la séparation ; sinon, le choix "
      "dépend du poids relatif des deux groupes, qui n'est pas décidé.\n")
    A("---\n\n## 4 — Les candidats S hors famille, pour mémoire\n")
    A("| Candidat | Clé de révision | Taille prudente – optimiste (k = 1,0) | Score /5 | État |")
    A("| --- | --- | --- | ---: | --- |")
    for c in sorted(r["cands"], key=lambda c: -score(c["notes"], poids)):
        A(f"| {c['nom']} | {D.cle_revision(r['cat']['candidats'][c['id']])} | {f(c['H'])}–{f(c['H_opt'])} m | "
          f"{f(score(c['notes'], poids))} | {c['etat']}"
          f"{' (référence)' if c['reference'] else ''} |")
    A("\nLeur continuité est celle de la v2 (intrinsèque) seulement s'ils appartiennent à une famille ; "
      "les autres (Feetech STS3250, SteadyWin GIM4310-10, Dynamixel XM430) sont listés pour mémoire.\n")
    A("---\n\n## 5 — Questions ouvertes\n")
    A("- **Ce que S doit porter** (calculateur, batterie, IMU) n'est pas chiffré : c'était la "
      "vraie contrainte derrière le seuil retiré (cadrage, question 13).")
    A("- **Les trous de gamme** sont-ils rédhibitoires, ou comblables par un modèle hors famille ?")
    A("- **La sensibilité aux poids** reste affichée : "
      + ("les poids sont fixés, mais un " if fixes_hdr else "les poids ne sont pas fixés par Jeremy, et un ")
      + "classement qui ne tiendrait qu'à eux mériterait d'être su.\n")
    cat_ = r["cat"]
    fd = cat_["familles"].get("damiao") or {}
    if fd.get("L") in cat_["candidats"] and "dm_j8009" in cat_["candidats"]:
        cL, c8 = cat_["candidats"][fd["L"]], cat_["candidats"]["dm_j8009"]
        red = val(cL.get("reduction") or {})
        A("### Limite du membre L de Damiao — question ouverte, à rouvrir AVANT L\n")
        A(f"- **Le membre L retenu, {cL['nom']}, a une réduction de {f(red, 0)}:1** "
          f"({cL['reduction']['source']}). Sa réversibilité n'est **pas publiée** ; un rapport aussi "
          "élevé la rend **probablement faible**. *Réversible* veut dire qu'un effort extérieur sur la "
          "sortie fait tourner le moteur : c'est ce qui laisse une jambe **encaisser un choc** (pied "
          "qui touche le sol) en cédant un peu, au lieu de le transmettre intact aux dents du "
          "réducteur. Pour une jambe, un réducteur peu réversible est **défavorable**.")
        A(f"- **Alternative dans la même famille : {c8['nom']}**, {f(val(c8['masse_g']), 0)} g "
          f"({c8['masse_g']['source']}), contre {f(val(cL['masse_g']), 0)} g : plus lourd ; sa réduction "
          "n'est pas publiée.")
        A(f"- **La robustesse n'a été notée que sur le membre S** ({cat_['candidats'][fd['S']]['nom']}) : ce comparatif ne dit "
          "rien de celle du membre L. C'est une **question ouverte pour L, à rouvrir avant de "
          "concevoir L**. Elle est **sans effet sur S** : ni la note, ni le choix de famille pour S "
          "n'en dépendent.\n")
    A("## 6 — Ce que ce comparatif ne dit pas\n")
    A("- **Aucun couple continu n'est mesuré dans la condition du robot.** k est une hypothèse ; le "
      "banc la remplacera par une mesure.")
    A("- **Les prix** sont ceux relevés le 30-09-2026, hors port ; plusieurs viennent de revendeurs.")
    A("- **Les données marquées non vérifiées** dans le catalogue ne comptent pas comme établies.")
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ecrire", action="store_true", help="engendre les documents")
    a = ap.parse_args(argv)
    if not AM.SERIE.exists():
        print(f"série absente : {AM.SERIE}\n  la régénérer : ~/upstream/toddlerbot/.venv/bin/python "
              "sim/upstream/enregistrer_marche.py")
        return 1
    r = calculer()
    print("\n  FAMILLES (tailles en m, S/M/L prudent à k bas – optimiste)\n")
    for ligne in tableau_familles(r):
        print("  " + ligne)
    print("\n  vainqueur par k :")
    nom = {fm["id"]: fm["nom"] for fm in r["fams"]}
    for b_ in r["fam_balayage"]:
        s_ = b_["sens"]
        print(f"    k = {f(b_['k'], 1)} : {nom[s_['nominal']]:58s} ±50 % {'tient' if s_['tous_pm'] else 'NE tient PAS':12s} "
              f"tirages quelconques {f(100 * s_['freq'], 1):>5} %")
    if r["fam_seuil"]:
        sf = r["fam_seuil"]
        print(f"  SEUIL k : {nom[sf['gagnant']]} jusqu'à k = {f(sf['garde'])} ; {nom[sf['nouveau']]} dès k = {f(sf['k'])}")
    else:
        print("  SEUIL k : aucune bascule entre 1,0 et 0,5")
    rb = rapports_blocage(r["cat"])
    print("\n  rapports blocage / nominal publiés (RobStride) :")
    for x in rb:
        print(f"    {x['nom']:24s} {f(x['blocage'], 1):>5} / {f(x['nominal'], 1):>5} = {f(x['rapport'], 3)}")
    print(f"    moyenne {f(sum(x['rapport'] for x in rb) / len(rb), 3)}")
    e_ = r["estimation"]
    print(f"\n  estimation thermique J4310 (seuil {e_['t_lim']:g} °C, {e_['t_lim_source']}) : "
          f"k {f(e_['k_bas'])}–{f(e_['k_haut'])} en rotation")
    if r["critere"] and r["critere"]["sans_objet"]:
        print(f"  critère d'abandon : SANS OBJET — la famille de {r['critere']['nom']} ne gagne à aucun k "
              f"(gagnants : {', '.join(r['critere']['gagnants'])})")
    elif r["critere"]:
        ca = r["critere"]
        print(f"  critère d'abandon ({ca['statut']}) : {ca['nom']} au blocage < {f(ca['seuil'])} N·m "
              f"(bascule {f(ca['k_bascule'])}–{f(ca['k_garde'])} × {f(ca['nominal'], 1)} N·m ; "
              f"{f(ca['seuil_bas'])}–{f(ca['seuil'])})")
    opts, pb, sb, fin = options_banc(r)
    fixes_b = all(v.get("statut", "").startswith(("fixé", "DÉCIDÉ")) for v in r["crit"]["banc"]["ponderes"].values())
    print(f"\n  banc (poids {'fixés' if fixes_b else 'PROPOSÉS'}) : {next(o['nom'] for o in opts if o['id'] == sb['nominal'])} ; "
          f"±50 % : {'tient toutes' if sb['tous_pm'] else 'NE tient PAS toutes'} ; tirages quelconques {f(100 * sb['freq'], 1)} %")
    for o in opts:
        print(f"    {o['nom']:70s} score {f(score(o['notes'], pb))}  coût " + " / ".join(f"{p_} {'≥ ' if o['manquants'] else ''}{f(v_, 0)}" for p_, v_ in o["couts"].items()) + " CHF")
    if a.ecrire:
        date = datetime.date.today().isoformat()
        DOC_FAMILLE.write_text(doc_familles(r, date), encoding="utf-8")
        DOC_BANC.write_text(doc_banc(r, opts, pb, sb, fin, date), encoding="utf-8")
        print(f"  -> {DOC_FAMILLE.relative_to(REPO)}, {DOC_BANC.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
