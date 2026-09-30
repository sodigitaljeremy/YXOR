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
3. SCORE = moyenne des notes pondérée par les poids (proposés, pas
   décidés).
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
DOC_S = REPO / "docs" / "choix-classe-S.md"
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

def continu_retenu(c: dict) -> dict:
    """Le couple continu sur la PLUS PETITE plaque publiée, sinon le nominal."""
    cc = c["couple_continu_Nm"]
    options = [dict(valeur=val(cc), plaque_mm=cc.get("plaque_mm"),
                    condition=cc.get("condition"), source=cc.get("source"))]
    for a in cc.get("autres_conditions") or []:
        options.append(dict(valeur=a.get("valeur"), plaque_mm=a.get("plaque_mm"),
                            condition=a.get("condition"), source=a.get("source")))
    blocage = next((o for o in options if o["condition"] and "BLOCAGE" in o["condition"]), None)
    plaques = [o for o in options if o["plaque_mm"] and o["valeur"] is not None
               and not (o["condition"] and "BLOCAGE" in o["condition"])]
    choisi = min(plaques, key=lambda o: o["plaque_mm"]) if plaques else options[0]
    return dict(choisi, blocage=blocage["valeur"] if blocage else None)


def prix_chf(cat, cid, bud):
    fs = cat.get("comparatif_S", {}).get(cid, {})
    p = fs.get("prix_revendeur") or cat["candidats"][cid]["prix"]
    return D.chf(p, bud["taux_de_change"]), p


def evaluer_S(cat, crit, bud, analyse, ref):
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
        cr = continu_retenu(c)
        classe = D.classe_catalogue(cat, cid)
        classe["continu"] = cr["valeur"]
        ev = D.evaluer(ref, D.config_homogene(classe), besoins, marge)
        H = None if "indetermine" in ev else ev["H_max"]
        # Le même calcul avec le couple NOMINAL publié (première valeur de la
        # fiche) : pour montrer ce qu'une élimination doit à la condition de
        # mesure retenue.
        cn = D.classe_catalogue(cat, cid)
        evn = D.evaluer(ref, D.config_homogene(cn), besoins, marge)
        H_nominal = None if "indetermine" in evn else evn["H_max"]
        # ── éliminatoires ──
        if cr["valeur"] is None or classe["pointe"] is None or classe["masse"] is None:
            elim_cap = "non évaluable"
        else:
            elim_cap = "admis" if H is not None and H >= crit["classe_S"]["eliminatoires"]["capacite"]["seuil_m"] else "éliminé"
        tel = fs["telemetrie"]
        champs = [tel.get(k) for k in ("position", "couple_ou_courant", "temperature")]
        elim_tel = "éliminé" if False in champs else ("non évaluable" if None in champs else "admis")
        etat = "éliminé" if "éliminé" in (elim_cap, elim_tel) else (
            "non évaluable" if "non évaluable" in (elim_cap, elim_tel) else "admis")
        # ── notes ──
        n, j = {}, {}
        base = note_capacite(H)
        corr = 1 if (cr["plaque_mm"] or not cr["condition"] or "non précisée" in (cr["condition"] or "")) else 0
        n["capacite"] = max(base - corr, 0) if cr["valeur"] is not None else 0
        j["capacite"] = (f"H_max {f(H)} m avec {f(cr['valeur'])} N·m continu "
                         f"({cr['condition'] or 'condition non précisée'}) → {base}"
                         + (f", −1 dissipation/condition → {n['capacite']}" if corr and cr['valeur'] is not None else "")
                         + ("" if cr["valeur"] is not None else " ; continu inconnu → 0"))
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
                        H=H, H_nominal=H_nominal, masse_robot=None if "indetermine" in ev else ev["masse"],
                        limitantes=ev.get("limitantes", []), continu=cr, prix_chf=chf,
                        elim_capacite=elim_cap, elim_telemetrie=elim_tel, etat=etat,
                        notes=n, justif=j, tension=val(c["tension_V"]),
                        famille=fam, pointe=classe["pointe"], masse_g=val(c["masse_g"])))
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

def options_banc(cands, S_id, second_id, cat, bud, crit):
    """Les cinq options du comparatif du banc, avec leurs notes."""
    b = crit["banc"]
    taux, tva, imp = bud["taux_de_change"], val(bud["tva_ch"]), val(bud["marge_imprevus"])
    elec = bud["electronique"]
    c_by = {c["id"]: c for c in cands}
    jr = b["ponderes"]["risque"]["jugements_par_option"]

    def cout(ids, bus):
        ht, manquants = 0.0, []
        for i in ids:
            p = c_by[i]["prix_chf"] if i in c_by else None
            if p is None:
                manquants.append(f"prix {c_by[i]['nom'] if i in c_by else i}")
            else:
                ht += p
        adapt = "adaptateur_can" if bus == "can" else "adaptateur_ttl"
        a = D.chf(elec[adapt]["prix"], taux)
        (manquants.append(adapt) if a is None else None)
        ht += a or 0
        tensions = {c_by[i]["tension"] for i in ids}
        if tensions == {48}:
            al = D.chf(elec["alimentation_48V"]["prix"], taux)
            (manquants.append("alimentation_48V") if al is None else None)
            ht += al or 0
        else:
            manquants.append(f"alimentation {'/'.join(str(t) for t in sorted(tensions))} V (non chiffrée)")
        return ht * (1 + imp) * (1 + tva), manquants

    def appr(n, meme_modele, meme_bus):
        pts = {"protocole": True, "thermique": True,
               "bus_multi_adresses": n >= 2 and meme_bus,
               "segment_2ddl": n >= 2 and meme_bus,
               "dispersion": n >= 3 and meme_modele}
        return sum(pts.values()), [k for k, v in pts.items() if v]

    bus = lambda i: "can" if c_by[i]["famille"].endswith("_can") else "ttl"
    fam_S = c_by[S_id]["famille"]
    opts = []
    for n, cle in ((1, "un_vainqueur"), (2, "deux_vainqueurs"), (3, "trois_vainqueurs")):
        ids = [S_id] * n
        opts.append(dict(id=cle, nom=f"{n} × {c_by[S_id]['nom']}", ids=ids, bus=bus(S_id),
                         appr=appr(n, True, True), transfert=5,
                         transfert_j="exactement le modèle retenu pour S"))
    if second_id:
        ids = [S_id, second_id]
        mb = bus(S_id) == bus(second_id)
        opts.append(dict(id="deux_finalistes",
                         nom=f"1 × {c_by[S_id]['nom']} + 1 × {c_by[second_id]['nom']}",
                         ids=ids, bus=bus(S_id), appr=appr(2, False, mb), transfert=3,
                         transfert_j="un seul des deux actionneurs est le modèle retenu (JUGEMENT : 3)"))
    opts.append(dict(id="feetech", nom="2 × Feetech STS3250 (banc d'apprentissage)",
                     ids=["sts3250", "sts3250"], bus="ttl", appr=appr(2, True, True),
                     transfert=5 if fam_S == c_by["sts3250"]["famille"] else 1,
                     transfert_j=("même modèle que S" if fam_S == c_by["sts3250"]["famille"]
                                  else "autre fabricant et autre protocole que S")))
    for o in opts:
        o["cout"], o["manquants"] = cout(o["ids"], o["bus"])
        o["notes"] = dict(apprentissage=o["appr"][0], transfert_S=o["transfert"],
                          cout=0 if o["manquants"] else seuils(o["cout"], (250, 400, 600, 900, 1300), (5, 4, 3, 2, 1), 0),
                          risque=jr[o["id"]]["note"])
        o["risque_j"] = jr[o["id"]]["justification"]
        o["etat"], o["reference"] = "admis", False
    return opts


# ─────────────────────────────── documents ──────────────────────────────

CRIT_S = ("capacite", "cout", "continuite", "fiabilite_fournisseur", "robustesse",
          "masse", "ouverture", "tension_securite", "disponibilite")


def doc_S(cands, crit, poids, sens, marge, date):
    L = []
    A = L.append
    A("# Choix de la classe d'actionneur de S — comparatif multicritère\n")
    A(f"**Engendré** par `.venv/bin/python scripts/selection_multicritere.py --ecrire`, "
      f"le {date}. Ne pas éditer à la main : le régénérer. Aucune fiche, aucun achat "
      "proposé (CLAUDE.md, règle d'achat c) : c'est un comparatif demandé, qui prépare "
      "une décision de Jeremy.\n")
    A("Sources : `params/actionneurs.yaml` (catalogue et `comparatif_S`, chaque valeur "
      "sourcée, version de fiche et sha256), `params/criteres_selection.yaml` (grilles "
      "écrites **avant** le calcul, poids **proposés, à fixer par Jeremy**, jugements "
      "justifiés), `params/budget.yaml` (taux BCE). Statuts : les notes sont **calculées** "
      "depuis le catalogue, sauf celles marquées **JUGEMENT**.\n")
    A("---\n\n## 1 — Les candidats\n")
    A(f"| Candidat | Continu retenu (N·m) | Condition | En blocage | Pointe | Masse (g) | Tension | Prix HT (CHF) | H_max à marge {f(marge, 1)} | H_max avec le nominal publié |")
    A("| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for c in cands:
        cr = c["continu"]
        A(f"| {c['nom']}{' *(référence)*' if c['reference'] else ''} | {f(cr['valeur'])} | "
          f"{cr['condition'] or 'non précisée'} | {f(cr['blocage'])} | {f(c['pointe'])} | "
          f"{f(c['masse_g'], 1)} | {c['tension']} V | {f(c['prix_chf'])} | **{f(c['H'])} m** | "
          f"{f(c['H_nominal'])} m |")
    A("\n**Couple continu retenu** : celui publié sur la **plus petite plaque de dissipation**, "
      "sinon le nominal. Cette règle a été **modifiée le 2026-09-30** en remplissant le "
      "catalogue, avant tout calcul de note : la version initiale (« en blocage s'il est "
      "publié ») aurait pénalisé RobStride, seul fabricant à publier une valeur en blocage. "
      "Voir `criteres_selection.yaml`.\n")
    A("---\n\n## 2 — Éliminatoires\n")
    A("| Candidat | H_max ≥ 0,55 m | Télémétrie (position, couple ou courant, température) | État |")
    A("| --- | --- | --- | --- |")
    for c in cands:
        A(f"| {c['nom']} | {c['elim_capacite']} | {c['elim_telemetrie']} | **{c['etat']}**"
          f"{' (référence, hors classement)' if c['reference'] else ''} |")
    A("\nUn **éliminé** ne peut pas gagner, quels que soient les poids. Un **non évaluable** "
      "reste classé, et son manque est affiché.\n")
    bascule = [c for c in cands if c["elim_capacite"] == "éliminé" and c["H_nominal"] and c["H_nominal"] >= 0.55]
    if bascule:
        A("**⚠ Éliminations qui tiennent à la condition de mesure.** "
          + " ; ".join(f"{c['nom']} : {f(c['H'])} m avec {f(c['continu']['valeur'])} N·m "
                       f"({c['continu']['condition']}), mais {f(c['H_nominal'])} m avec son nominal publié"
                       for c in bascule)
          + ". La règle retient la plus petite plaque publiée (§ 1) : c'est elle qui élimine. "
          "Sous l'autre lecture, ces candidats seraient admis. **C'est une élimination de "
          "justesse, qui dépend d'une convention**, et non d'une impossibilité.\n")
    A("---\n\n## 3 — Notes et score\n")
    A("| Critère | Poids (proposé) | " + " | ".join(c["nom"] for c in cands if not c["reference"]) + " |")
    A("| --- | ---: | " + " | ".join("---:" for c in cands if not c["reference"]) + " |")
    for k in CRIT_S:
        A(f"| {k} | {poids[k]} | " + " | ".join(str(c["notes"][k]) for c in cands if not c["reference"]) + " |")
    A("| **score /5** | | " + " | ".join(
        f"**{f(score(c['notes'], poids))}**" + (" (éliminé)" if c["etat"] == "éliminé" else "")
        for c in cands if not c["reference"]) + " |")
    A("\n### Justification de chaque note\n")
    for c in cands:
        A(f"**{c['nom']}**{' (référence)' if c['reference'] else ''}\n")
        for k in CRIT_S:
            A(f"- {k} = {c['notes'][k]} — {c['justif'][k]}")
        A("")
    A("---\n\n## 4 — Sensibilité\n")
    A(f"Vainqueur aux poids proposés : **{next(c['nom'] for c in cands if c['id'] == sens['nominal'])}**.\n")
    A("| Poids modifié | × 0,5 | × 1,5 |")
    A("| --- | --- | --- |")
    nom = {c["id"]: c["nom"] for c in cands}
    for k in poids:
        v = {fac: w for kk, fac, w in sens["variations"] if kk == k}
        A(f"| {k} | {nom.get(v[0.5], '—')} | {nom.get(v[1.5], '—')} |")
    A(f"\n**{sum(1 for *_, w in sens['variations'] if w == sens['nominal'])} variations sur "
      f"{len(sens['variations'])}** laissent le vainqueur inchangé.\n")
    A("Fréquence de victoire sur 1 000 jeux de poids tirés au hasard (Dirichlet α = 1, graine "
      f"{crit['classe_S']['sensibilite']['graine']}) :\n")
    A("| Candidat | Victoires | Fréquence |")
    A("| --- | ---: | ---: |")
    for w, k in sorted(sens["gagnes"].items(), key=lambda x: -x[1]):
        A(f"| {nom.get(w, w)} | {k} | {f(100 * k / crit['classe_S']['sensibilite']['tirages'], 1)} % |")
    A("\n## 5 — Verdict\n")
    if sens["robuste"]:
        A(f"**Classement ROBUSTE.** {nom[sens['nominal']]} gagne toutes les variations ±50 % "
          f"et {f(100 * sens['freq'], 1)} % des tirages aléatoires (seuil : 60 %).\n")
    else:
        A(f"**Les candidats sont trop proches pour que l'analyse tranche.** Le vainqueur nominal, "
          f"{nom[sens['nominal']]}, gagne {f(100 * sens['freq'], 1)} % des tirages aléatoires"
          f"{'' if sens['tous_pm'] else ' et perd au moins une variation ±50 %'}. "
          "Le choix dépend des poids : il revient à Jeremy de les fixer.\n")
    A("## 6 — Ce que ce comparatif ne dit pas\n")
    A("- **Les poids sont proposés, pas décidés.** La sensibilité dit seulement si le "
      "classement en dépend.")
    A("- **Toutes les tailles sont des plafonds optimistes** : la marche de référence était "
      "écrêtée (cadrage § 3).")
    A("- **Aucun couple continu n'est mesuré dans la condition du robot.** Chaque valeur est "
      "celle du constructeur, sur sa plaque ou sans condition précisée ; le banc la mesurera.")
    A("- **Les prix sont hors TVA suisse et hors port** ; un prix inconnu vaut 0 dans la note "
      "de coût, par prudence.")
    A("- **Les données marquées non vérifiées** dans le catalogue ne comptent pas comme "
      "établies.")
    fragiles = [c for c in cands if "régime établi" in (c["continu"]["condition"] or "")]
    for c in fragiles:
        A(f"- **⚠ {c['nom']} : son couple continu n'est pas un régime établi.** Condition publiée : "
          f"« {c['continu']['condition']} ». La grille ne retire qu'un point pour une condition non "
          f"précisée ; sa capacité ({f(c['H'])} m) est donc probablement **surestimée**. "
          + ("C'est le vainqueur nominal : c'est le premier point à vérifier au banc."
             if c["id"] == sens["nominal"] else ""))
    return "\n".join(L) + "\n"


def doc_banc(opts, crit, poids, sens, S_nom, second_nom, date, S_robuste=True):
    L = []
    A = L.append
    A("# Comparatif du banc d'essai\n")
    A(f"**Engendré** par `.venv/bin/python scripts/selection_multicritere.py --ecrire`, "
      f"le {date}, par la même méthode que `docs/choix-classe-S.md`. Aucun achat n'est "
      "proposé : ce comparatif prépare le choix de Jeremy (cadrage § 6 et § 13, question 12).\n")
    A(f"Les options dépendent du classement de S : vainqueur nominal **{S_nom}**, "
      f"second **{second_nom or '—'}**. Si ce classement change, ce document change.\n")
    if not S_robuste:
        A("**⚠ Ce classement de S n'est PAS robuste** (`docs/choix-classe-S.md`, § 5) : le "
          "vainqueur nominal dépend des poids. Les options « × vainqueur » ci-dessous valent "
          "donc **pour ce vainqueur-là**. Ce qui se transfère d'un vainqueur à l'autre, c'est le "
          "**nombre** d'exemplaires qu'elles recommandent, pas le modèle.\n")
    A("---\n\n## 1 — Les options\n")
    A("| Option | Ce qu'elle apprend | Transfert à S | Coût TTC CH | Postes non chiffrés | Risque |")
    A("| --- | --- | --- | ---: | --- | --- |")
    for o in opts:
        A(f"| {o['nom']} | {o['appr'][0]}/5 : {', '.join(o['appr'][1])} | {o['transfert']} — {o['transfert_j']} | "
          f"{'≥ ' if o['manquants'] else ''}{f(o['cout'], 0)} CHF | {', '.join(o['manquants']) or '—'} | "
          f"{o['notes']['risque']} — {o['risque_j']} |")
    A("\nCoût TTC CH = (actionneurs + adaptateur + alimentation du bus) × (1 + imprévus) × "
      "(1 + TVA 8,1 %). Adaptateur CAN : candleLight de Linux Automation, **prototype non "
      "conforme CE** selon son fabricant. Alimentation 48 V : Mean Well RSP-500-48. Un poste non "
      "chiffré met la note de coût à 0.\n")
    A("---\n\n## 2 — Notes et score\n")
    A("| Critère | Poids (proposé) | " + " | ".join(o["nom"] for o in opts) + " |")
    A("| --- | ---: | " + " | ".join("---:" for _ in opts) + " |")
    for k in poids:
        A(f"| {k} | {poids[k]} | " + " | ".join(str(o["notes"][k]) for o in opts) + " |")
    A("| **score /5** | | " + " | ".join(f"**{f(score(o['notes'], poids))}**" for o in opts) + " |")
    nom = {o["id"]: o["nom"] for o in opts}
    A("\n## 3 — Sensibilité\n")
    A(f"Vainqueur aux poids proposés : **{nom[sens['nominal']]}**. "
      f"{sum(1 for *_, w in sens['variations'] if w == sens['nominal'])} variations ±50 % sur "
      f"{len(sens['variations'])} le laissent en tête.\n")
    A("| Option | Victoires sur 1 000 tirages |")
    A("| --- | ---: |")
    for w, k in sorted(sens["gagnes"].items(), key=lambda x: -x[1]):
        A(f"| {nom.get(w, w)} | {k} |")
    if all(o["notes"]["cout"] == 0 for o in opts):
        A("\n**Le critère de coût ne départage rien** : aucune option n'est entièrement chiffrée "
          "(voir « Postes non chiffrés »), donc toutes ont la note 0. Le verdict repose sur les "
          "trois autres critères.\n")
    A("\n## 4 — Verdict\n")
    if sens["robuste"]:
        A(f"**Classement ROBUSTE** : {nom[sens['nominal']]}"
          + ("" if S_robuste else ", **pour ce vainqueur de S**") + ".\n")
    else:
        A("**Les options sont trop proches pour que l'analyse tranche** : le choix dépend des "
          "poids, que Jeremy fixera.\n")
    A("## 5 — Ce que ce comparatif ne dit pas\n")
    A("- Les poids et les notes de risque sont **proposés** ; la sensibilité dit si le "
      "classement en dépend.")
    A("- L'option Feetech n'a **ni prix vérifié ni alimentation 12 V chiffrée** : son coût est "
      "inconnu, sa note de coût vaut 0.")
    A("- Le banc à trois exemplaires répond à la condition « au moins 3 RS05 » de l'étude "
      "externe (§ 15.2), qui veut mesurer la dispersion entre exemplaires.")
    return "\n".join(L) + "\n"


# ─────────────────────────────── principal ──────────────────────────────

def calculer():
    cat = D.charger_catalogue()
    crit = yaml.safe_load(CRITERES.read_text(encoding="utf-8"))
    bud = yaml.safe_load(D.BUDGET.read_text(encoding="utf-8"))
    analyse = AM.analyser(AM.SERIE)
    ref = D.reference(cat, analyse)
    cands = evaluer_S(cat, crit, bud, analyse, ref)
    poids = {k: v["poids"] for k, v in crit["classe_S"]["ponderes"].items()}
    sens = sensibilite(cands, poids, crit["classe_S"]["sensibilite"])
    cl = sorted(classables(cands), key=lambda c: -score(c["notes"], poids))
    S_id = sens["nominal"]
    second = next((c["id"] for c in cl if c["id"] != S_id), None)
    opts = options_banc(cands, S_id, second, cat, bud, crit)
    pb = {k: v["poids"] for k, v in crit["banc"]["ponderes"].items()}
    sb = sensibilite(opts, pb, crit["classe_S"]["sensibilite"])
    return dict(cat=cat, crit=crit, cands=cands, poids=poids, sens=sens, S_id=S_id,
                second=second, opts=opts, pb=pb, sb=sb, marge=val(cat["dimensionnement"]["marge"]))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ecrire", action="store_true", help="engendre les deux documents")
    a = ap.parse_args(argv)
    if not AM.SERIE.exists():
        print(f"série absente : {AM.SERIE}\n  la régénérer : ~/upstream/toddlerbot/.venv/bin/python "
              "sim/upstream/enregistrer_marche.py")
        return 1
    r = calculer()
    print(f"  {len(r['cands'])} candidats S (dont {sum(c['reference'] for c in r['cands'])} référence)")
    for c in sorted(r["cands"], key=lambda c: -score(c["notes"], r["poids"])):
        print(f"    {c['nom']:42s} {c['etat']:14s} H_max {f(c['H'])} m  score {f(score(c['notes'], r['poids']))}"
              f"{'  (référence)' if c['reference'] else ''}")
    s = r["sens"]
    print(f"  vainqueur nominal : {s['nominal']} ; ±50 % : {'tous' if s['tous_pm'] else 'PAS tous'} ; "
          f"tirages : {f(100 * s['freq'], 1)} % -> {'ROBUSTE' if s['robuste'] else 'TROP PROCHES'}")
    sb = r["sb"]
    print(f"  banc : {sb['nominal']} ; tirages {f(100 * sb['freq'], 1)} % -> "
          f"{'ROBUSTE' if sb['robuste'] else 'TROP PROCHES'}")
    if a.ecrire:
        date = datetime.date.today().isoformat()
        nom = {c["id"]: c["nom"] for c in r["cands"]}
        DOC_S.write_text(doc_S(r["cands"], r["crit"], r["poids"], s, r["marge"], date), encoding="utf-8")
        DOC_BANC.write_text(doc_banc(r["opts"], r["crit"], r["pb"], sb, nom[r["S_id"]],
                                     nom.get(r["second"]), date, s["robuste"]), encoding="utf-8")
        print(f"  -> {DOC_S.relative_to(REPO)}, {DOC_BANC.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
