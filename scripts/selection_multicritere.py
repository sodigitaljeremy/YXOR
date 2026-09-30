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
3. SCORE = moyenne des notes pondérée par les poids. Ceux de la classe S
   et des familles sont FIXÉS par Jeremy (2026-09-30) ; ceux du banc
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

REPO = Path(__file__).resolve().parents[1]
CRITERES = REPO / "params" / "criteres_selection.yaml"
DOC_S_V1 = REPO / "docs" / "choix-classe-S.md"          # v1, figé : n'est plus régénéré
DOC_FAMILLE = REPO / "docs" / "choix-famille-actionneurs.md"
DOC_BANC = REPO / "docs" / "comparatif-banc.md"

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


def note_capacite(H):
    if H is None or H < 0.55:
        return 0
    for s, n in ((0.70, 5), (0.65, 4), (0.61, 3), (0.58, 2), (0.55, 1)):
        if H >= s:
            return n


def note_cout(chf):
    return 0 if chf is None else seuils(chf, (60, 90, 130, 200, 300), (5, 4, 3, 2, 1), 0)


def note_masse(g):
    return 0 if g is None else seuils(g, (150, 200, 250, 350, 500), (5, 4, 3, 2, 1), 0)


def note_tension(v):
    return 0 if v is None else seuils(v, (12, 24, 36, 48), (5, 4, 3, 2), 1)


# ───────────────────────────── données S ────────────────────────────────

def intervalle_continu(c: dict, k: float) -> dict:
    """Couple continu OPTIMISTE et PRUDENT (criteres_selection.yaml, 2026-09-30 soir).

    optimiste : le nominal publié le plus favorable (hors blocage) ;
    prudent   : en blocage si publié ; sinon la plus petite plaque
                publiée ; sinon (condition non précisée) le nominal × k.
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
    plaques = [o for o in rot if o["plaque_mm"]]
    if blocage:
        return dict(optimiste=optimiste, prudent=blocage["valeur"], base_prudente="en blocage",
                    k_applique=False)
    if plaques:
        pl = min(plaques, key=lambda o: o["plaque_mm"])
        return dict(optimiste=optimiste, prudent=pl["valeur"],
                    base_prudente=f"plus petite plaque publiée ({pl['plaque_mm']} mm)", k_applique=False)
    return dict(optimiste=optimiste, prudent=optimiste * k,
                base_prudente=f"condition non précisée : nominal × k ({f(k, 1)})", k_applique=True)


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
        iv = intervalle_continu(c, k)
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
        n["capacite"] = note_capacite(H) if cr["valeur"] is not None else 0
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
            iv = intervalle_continu(c, k)
            Hp, evp = h_max_avec(cat, mid, iv["prudent"], ref, besoins, marge)
            Ho, _ = h_max_avec(cat, mid, iv["optimiste"], ref, besoins, marge)
            # Même base de prix que la note de coût : le prix REVENDEUR s'il
            # est relevé (comparatif_S), sinon celui du catalogue.
            cat_prix = cat
            pr = (cat.get("comparatif_S", {}).get(mid) or {}).get("prix_revendeur")
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
        return ht * (1 + imp) * (1 + tva), manquants

    def appr(n, meme_modele, meme_bus):
        pts = {"protocole": True, "thermique": True,
               "bus_multi_adresses": n >= 2 and meme_bus,
               "segment_2ddl": n >= 2 and meme_bus,
               "dispersion": n >= 3 and meme_modele}
        return sum(pts.values()), [k for k, v in pts.items() if v]

    opts = []
    vs = info(S_id)
    t_v = tension_commune([vs["plage"]]) or vs["tension"]
    for n, cle in ((1, "un_vainqueur"), (2, "deux_vainqueurs"), (3, "trois_vainqueurs")):
        opts.append(dict(id=cle, nom=f"{n} × {vs['nom']}", ids=[S_id] * n, tension=vs["tension"],
                         appr=appr(n, True, True), transfert=3,
                         transfert_j=(f"JUGEMENT : 5 si k ≥ {f(seuil)} (sa famille gagne), 1 sinon ; "
                                      "k inconnu tant que le banc ne l'a pas mesuré → 3")
                                     if seuil else "exactement le modèle retenu pour S → 5"))
        if not seuil:
            opts[-1]["transfert"] = 5
    # 1 × finaliste A + 1 × finaliste B, MÊME TENSION (48 V de préférence)
    SA, SB = cat_fam[fa]["S"], cat_fam[fb]["S"]
    choix = []
    for fid, sid in ((fa, SA), (fb, SB)):
        var = cat_fam[fid].get("S_variante_48V")
        choix.append([sid] + ([var] if var else []))
    paire, tension = None, None
    for cible in (48, 24):
        a_ = next((x for x in choix[0] if (pl := info(x)["plage"]) and pl[0] <= cible <= pl[1]), None)
        b_ = next((x for x in choix[1] if (pl := info(x)["plage"]) and pl[0] <= cible <= pl[1]), None)
        if a_ and b_:
            paire, tension = [a_, b_], cible
            break
    if paire:
        opts.append(dict(id="deux_finalistes",
                         nom=f"1 × {info(paire[0])['nom']} + 1 × {info(paire[1])['nom']} ({tension} V)",
                         ids=paire, tension=tension, appr=appr(2, False, True), transfert=5,
                         transfert_j=("JUGEMENT : quel que soit k, le modèle S de la famille gagnante est "
                                      "sur le banc → 5"),
                         finalistes=True))
    opts.append(dict(id="feetech", nom="2 × Feetech STS3250 (banc d'apprentissage)",
                     ids=["sts3250", "sts3250"], tension=12, appr=appr(2, True, True), transfert=1,
                     transfert_j="autre fabricant, autre bus (TTL) que tous les finalistes → 1"))
    for o in opts:
        o["cout"], o["manquants"] = cout(o["ids"], o["tension"])
        o["notes"] = dict(apprentissage=o["appr"][0], transfert_S=o["transfert"],
                          cout=0 if o["manquants"] else seuils(o["cout"], (250, 400, 600, 900, 1300), (5, 4, 3, 2, 1), 0),
                          risque=jr[o["id"]]["note"])
        o["risque_j"] = jr[o["id"]]["justification"]
        o["etat"], o["reference"] = "admis", False
    pb = {k: v["poids"] for k, v in b["ponderes"].items()}
    return opts, pb, sensibilite(opts, pb, crit["classe_S"]["sensibilite"]), (fa, fb, SA, SB, paire, tension)


CRIT_S = ("capacite", "cout", "continuite", "fiabilite_fournisseur", "robustesse",
          "masse", "ouverture", "tension_securite", "disponibilite")


def doc_banc(r, opts, pb, sb, finalistes, date) -> str:
    fa, fb, SA, SB, paire, tension = finalistes
    cat = r["cat"]
    nomf = {fm["id"]: fm["nom"] for fm in r["fams"]}
    L = []
    A = L.append
    A("# Comparatif du banc d'essai — v2\n")
    A(f"**Engendré** par `.venv/bin/python scripts/selection_multicritere.py --ecrire`, le {date}, "
      "après le comparatif des familles (`docs/choix-famille-actionneurs.md`). Aucun achat n'est "
      "proposé : ce comparatif prépare le choix de Jeremy (cadrage § 6 et § 13, question 12).\n")
    if r["fam_seuil"]:
        sf = r["fam_seuil"]
        A(f"**Pourquoi ce banc compte.** Le choix de famille bascule au seuil **k ≈ {f(sf['garde'])}** : "
          f"au-dessus, **{nomf[sf['gagnant']]}** ; en dessous, **{nomf[sf['nouveau']]}**. k est le "
          "rapport entre le couple continu réel des actionneurs « condition non précisée » et leur "
          "nominal publié. **Il ne se décide pas, il se mesure** — c'est le rôle premier du banc.\n")
    A("---\n\n## 1 — Les options\n")
    A("| Option | Ce qu'elle apprend | Transfert à S | Coût TTC CH | Postes non chiffrés | Risque |")
    A("| --- | --- | --- | ---: | --- | --- |")
    for o in opts:
        A(f"| {o['nom']} | {o['appr'][0]}/5 : {', '.join(o['appr'][1])} | {o['transfert']} — {o['transfert_j']} | "
          f"{'≥ ' if o['manquants'] else ''}{f(o['cout'], 0)} CHF | {', '.join(o['manquants']) or '—'} | "
          f"{o['notes']['risque']} — {o['risque_j']} |")
    A("\nCoût TTC CH = (actionneurs + adaptateur + alimentation) × (1 + imprévus 15 %, provisoire) × "
      "(1 + TVA 8,1 %). Alimentations : Mean Well RSP-320-24 (24 V) ou RSP-500-48 (48 V), Reichelt. "
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
    A("---\n\n## 2 — Notes et score\n")
    A("| Critère | Poids (proposé) | " + " | ".join(o["nom"] for o in opts) + " |")
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
    A(f"**{'Classement ROBUSTE' if sb['robuste'] else 'Options trop proches pour que l analyse tranche'.replace('l analyse', 'l’analyse')}** "
      f": {nom[sb['nominal']]}"
      + (" — le choix dépend des poids, que Jeremy fixera." if not sb["robuste"] else ".") + "\n")
    k_seul = [x for x in (SA, SB) if intervalle_continu(cat["candidats"][x], 0.5)["k_applique"]]
    if k_seul:
        A("**Ce que chaque option tranche.** L'hypothèse k ne touche que les actionneurs dont la "
          "condition de mesure n'est pas publiée : ici **"
          + ", ".join(cat["candidats"][x]["nom"] for x in k_seul)
          + "**. Mesurer son couple continu réel **suffit à trancher le seuil**, et les options "
          "« × vainqueur » le font. L'option à deux finalistes ajoute la vérification de l'autre "
          "finaliste **dans la même condition** : la comparaison devient directe, au lieu de "
          "s'appuyer sur sa fiche.\n")
    A("---\n\n## 5 — Protocole de mesure : les couples continus en condition IDENTIQUE\n")
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
    A("   il départage les finalistes au seuil du § 1.\n")
    A("---\n\n## 6 — Ce que ce comparatif ne dit pas\n")
    A("- Les poids, les notes de transfert et de risque sont **proposés** ou de **jugement**, et "
      "justifiés ligne par ligne.")
    A("- L'option Feetech n'a **ni prix vérifié ni alimentation 12 V chiffrée** : son coût est "
      "inconnu.")
    A("- La mesure au rotor bloqué ne dit rien du rendement en rotation ; elle compare les deux "
      "finalistes entre eux, dans la même condition.")
    A("- Le banc à trois exemplaires répond à la demande de l'étude externe (« au moins 3 », § 15.2) "
      "pour la dispersion entre exemplaires.")
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


def calculer():
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
    return dict(cat=cat, crit=crit, bud=bud, ref=ref, analyse=analyse, poids=poids,
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


def doc_familles(r, date) -> str:
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
    A("Poids : **fixés par Jeremy le 30-09-2026** (capacité 18, continuité 18, coût 15, fiabilité 15, "
      "robustesse 12, disponibilité 7, masse, ouverture, tension 5 chacun). Marge : 1,5 (fiche 0051). "
      "Toutes les tailles "
      "sont des **plafonds optimistes** : la marche de référence était écrêtée (cadrage § 3).\n")
    A("---\n\n## 1 — Les familles\n")
    L.extend(tableau_familles(r))
    A("\nTailles en mètres, à marge 1,5, configuration homogène de chaque membre. « Prudent » est "
      "calculé à la borne basse de l'hypothèse k ; pour RobStride, c'est la valeur **en blocage** "
      "publiée, qui ne dépend pas de k. Jambes = phase `jambes_v1` de `params/budget.yaml` "
      "(12 actionneurs, électronique connue, imprévus et TVA) ; « ≥ » : la structure n'est pas "
      "chiffrée.\n")
    A("**Prix : une base inégale, dite.** Chaque membre est chiffré au prix **revendeur** quand il a "
      "été relevé ; sinon au prix du catalogue. Pour **RS02 et RS06**, seul le prix **constructeur en "
      "yuans** est connu (hors export, port et douane) : leurs coûts M et L sont donc **sous-estimés** "
      "face aux autres familles, chiffrées chez des revendeurs.\n")
    A("### Membres, trous et alternatives\n")
    for fm in r["fams"]:
        A(f"**{fm['nom']}**\n")
        for tl in TAILLES:
            x = fm["tailles"][tl]
            if not x:
                A(f"- {tl} : **TROU** de gamme.")
                continue
            iv = x["iv"]
            A(f"- {tl} : {x['nom']} — pointe {f(x['pointe'], 1)} N·m ; continu optimiste "
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
    A("| Critère | Poids (fixé) | " + " | ".join(fm["nom"].split(" (")[0] + (" EL05" if "el05" in fm["id"] else "") for fm in fams) + " |")
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
    A("| k | Famille gagnante | Tirages gagnés | Variations ±50 % | Verdict |")
    A("| ---: | --- | ---: | --- | --- |")
    nom = {fm["id"]: fm["nom"] for fm in fams}
    for b_ in r["fam_balayage"]:
        s_ = b_["sens"]
        A(f"| {f(b_['k'], 1)} | {nom[s_['nominal']]} | {f(100 * s_['freq'], 1)} % | "
          f"{'toutes' if s_['tous_pm'] else 'PAS toutes'} | {'ROBUSTE' if s_['robuste'] else 'trop proches'} |")
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
    A("---\n\n## 4 — Les candidats S hors famille, pour mémoire\n")
    A("| Candidat | Taille prudente – optimiste (k = 1,0) | Score /5 | État |")
    A("| --- | --- | ---: | --- |")
    for c in sorted(r["cands"], key=lambda c: -score(c["notes"], poids)):
        A(f"| {c['nom']} | {f(c['H'])}–{f(c['H_opt'])} m | {f(score(c['notes'], poids))} | {c['etat']}"
          f"{' (référence)' if c['reference'] else ''} |")
    A("\nLeur continuité est celle de la v2 (intrinsèque) seulement s'ils appartiennent à une famille ; "
      "les autres (Feetech STS3250, SteadyWin GIM4310-10, Dynamixel XM430) sont listés pour mémoire.\n")
    A("---\n\n## 5 — Questions ouvertes\n")
    A("- **Ce que S doit porter** (calculateur, batterie, IMU) n'est pas chiffré : c'était la "
      "vraie contrainte derrière le seuil retiré (cadrage, question 13).")
    A("- **Les trous de gamme** sont-ils rédhibitoires, ou comblables par un modèle hors famille ?")
    A("- **La sensibilité aux poids** reste affichée pour mémoire : les poids sont fixés, mais un "
      "classement qui ne tiendrait qu'à eux mériterait d'être su.\n")
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
        print(f"    k = {f(b_['k'], 1)} : {nom[s_['nominal']]:58s} tirages {f(100 * s_['freq'], 1):>5} % "
              f"-> {'ROBUSTE' if s_['robuste'] else 'trop proches'}")
    if r["fam_seuil"]:
        sf = r["fam_seuil"]
        print(f"  SEUIL k : {nom[sf['gagnant']]} jusqu'à k = {f(sf['garde'])} ; {nom[sf['nouveau']]} dès k = {f(sf['k'])}")
    else:
        print("  SEUIL k : aucune bascule entre 1,0 et 0,5")
    opts, pb, sb, fin = options_banc(r)
    print(f"\n  banc : {next(o['nom'] for o in opts if o['id'] == sb['nominal'])} ; tirages "
          f"{f(100 * sb['freq'], 1)} % -> {'ROBUSTE' if sb['robuste'] else 'trop proches'}")
    for o in opts:
        print(f"    {o['nom']:70s} score {f(score(o['notes'], pb))}  coût {'≥ ' if o['manquants'] else ''}{f(o['cout'], 0)} CHF")
    if a.ecrire:
        date = datetime.date.today().isoformat()
        DOC_FAMILLE.write_text(doc_familles(r, date), encoding="utf-8")
        DOC_BANC.write_text(doc_banc(r, opts, pb, sb, fin, date), encoding="utf-8")
        print(f"  -> {DOC_FAMILLE.relative_to(REPO)}, {DOC_BANC.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
