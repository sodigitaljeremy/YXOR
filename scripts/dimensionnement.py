#!/usr/bin/env python3
"""Dimensionnement INVERSE : quelle taille maximale pour une classe d'actionneur ?

    .venv/bin/python scripts/dimensionnement.py
    .venv/bin/python scripts/dimensionnement.py --marge 1.3
    .venv/bin/python scripts/dimensionnement.py --markdown     # tableaux du rapport

Venv DU PROJET. Lit :
  params/actionneurs.yaml             le catalogue des classes candidates
  params/budget.yaml                  les postes de coût (section budget)
  exports/actionneurs/marche_15s.csv  la marche P1, via scripts/analyser_marche.py

═══════════════════════════════════════════════════════════════════════
 POURQUOI À L'ENVERS
═══════════════════════════════════════════════════════════════════════

Les paliers P1/P2/P3 fixaient la taille EN ENTRÉE, puis on cherchait
l'actionneur. Or les actionneurs se vendent par classes discrètes, et le
couple requis croît comme la masse × la taille. C'est donc la classe qui
FIXE la taille maximale. Ce script ne choisit rien : il dit, pour chaque
classe et chaque configuration, jusqu'où elle porte.

═══════════════════════════════════════════════════════════════════════
 LE MODÈLE — ET CE QU'IL SUPPOSE
═══════════════════════════════════════════════════════════════════════

Référence : ToddlerBot, H0 = 0,56 m, M0 = sa masse (lue dans le MJCF).

  masse(H)       = S0 · (H/H0)³  +  Σ masse réelle des 12 actionneurs de jambe
                   S0 = M0 − masse des 12 Dynamixel de jambe de ToddlerBot
                   (tout le reste — structure, haut du corps, électronique —
                   est mis à l'échelle en similitude géométrique)
  couple(H)      = couple_P1 · masse(H)/M0 · H/H0
                   (gravité m·g·L et inertie I·α suivent tous deux m·L
                   sous une allure de Froude — voir le rapport)
  vitesse(H)     = vitesse_P1 · (H/H0)^−½

Contraintes, par articulation de jambe j de classe c :
  marge · RMS_j(H)    ≤ couple continu de c     (sautée si null — et DITE)
  marge · pointe_j(H) ≤ couple de pointe de c
  vitesse_j(H)        ≤ vitesse de c            (borne BASSE sur H)

LA BOUCLE SUR LA MASSE. Le couple dépend de la masse, qui dépend de H.
L'itération naïve H ← f(masse(H)) DIVERGE : masse ∝ H³, donc
H_{k+1} ∝ 1/H_k³, et la dérivée vaut −3. La contrainte, elle, est
MONOTONE en H : on résout donc par dichotomie jusqu'à 0,1 mm, et chaque
évaluation recalcule la masse exacte à ce H. La masse rapportée est la
masse convergée à H_max.

ÉCRÊTAGE. Si un actionneur de ToddlerBot a touché sa borne pendant la
marche P1, son couple enregistré est une BORNE BASSE du besoin : la
taille calculée pour cette articulation est un PLAFOND OPTIMISTE. Le
script le signale ligne à ligne.

═══════════════════════════════════════════════════════════════════════
 LE CONTRÔLE DE COHÉRENCE
═══════════════════════════════════════════════════════════════════════

Le calcul doit retrouver deux robots qui marchent, dans leur classe, à
marge 1 (un robot qui existe n'a pas de marge à prouver) :
  ToddlerBot, 0,56 m, ses Dynamixel (bornes du modèle de simulation amont)
  Zeroth-01,  0,48 m, Feetech STS3250 (catalogue)
S'il ne les retrouve pas, le script SORT EN ERREUR et ne produit rien.

⚠ Le contrôle ToddlerBot est presque tautologique : la marche P1 a été
  simulée AVEC ces bornes, donc elle ne peut pas les dépasser. Il vérifie
  l'arithmétique (identité à H0, boucle de masse), pas la physique.
  Zeroth-01 est le seul contrôle indépendant.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyser_marche as AM  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
CATALOGUE = REPO / "params" / "actionneurs.yaml"
BUDGET = REPO / "params" / "budget.yaml"

JAMBE = ("hip_pitch", "hip_roll", "hip_yaw_drive", "knee", "ankle_pitch", "ankle_roll")
H_BAS, H_HAUT, TOL = 0.05, 5.0, 1e-4


# ─────────────────────────────── données ────────────────────────────────

def val(champ):
    """Valeur d'un champ du catalogue : {valeur: …} ou scalaire."""
    return champ.get("valeur") if isinstance(champ, dict) else champ


def charger_catalogue(chemin: Path = CATALOGUE) -> dict:
    return yaml.safe_load(chemin.read_text(encoding="utf-8"))


def vitesse_rad_s(c: dict) -> float | None:
    """La vitesse se CALCULE depuis l'unité d'origine du constructeur."""
    if val(c.get("vitesse_a_vide_rpm")) is not None:
        return val(c["vitesse_a_vide_rpm"]) * 2 * math.pi / 60
    if val(c.get("vitesse_s_par_60deg")) is not None:
        return (math.pi / 3) / val(c["vitesse_s_par_60deg"])
    return None


def classe_catalogue(cat: dict, cid: str) -> dict:
    c = cat["candidats"][cid]
    m = val(c["masse_g"])
    return dict(id=cid, nom=c["nom"],
                continu=val(c["couple_continu_Nm"]), pointe=val(c["couple_pointe_Nm"]),
                vitesse=vitesse_rad_s(c), masse=m / 1000 if m is not None else None)


def classes_dynamixel(analyse: dict, cat: dict) -> dict:
    """Les bornes du modèle de SIMULATION amont, par modèle Dynamixel.

    Continu = null : ROBOTIS ne publie pas de couple continu, et le modèle
    de simulation n'en a pas. Pointe = `tau_brake_max`, la plus haute borne
    que la simulation laisse atteindre.
    """
    masses = cat["reference_toddlerbot"]["masse_dynamixel_g"]
    out = {}
    for a in analyse["actionneurs"]:
        m = a["modele"]
        out[m] = dict(id=m, nom=f"Dynamixel {m} (modèle de simulation amont)",
                      continu=None, pointe=a["tau_brake_max"], vitesse=a["q_dot_max"],
                      masse=(val(masses[m]) / 1000) if val(masses.get(m)) is not None else None)
    return out


def besoins_p1(analyse: dict) -> dict:
    """Par actionneur de jambe : pointe, RMS, vitesse, écrêtage, modèle P1."""
    return {a["nom"]: a for a in analyse["actionneurs"] if a["zone"] == "jambes"}


def type_de(nom: str) -> str:
    return nom.split("_", 1)[1]            # left_hip_roll -> hip_roll


# ─────────────────────────────── modèle ─────────────────────────────────

def masse(H: float, ref: dict, config: dict, besoins: dict) -> float:
    """masse(H) = S0·(H/H0)³ + Σ masse réelle des actionneurs de jambe."""
    return ref["S0"] * (H / ref["H0"]) ** 3 + sum(config[type_de(n)]["masse"] for n in besoins)


def ratios(H: float, ref: dict, config: dict, besoins: dict, marge: float) -> dict:
    """Par actionneur : exigence / capacité pour chaque contrainte (≤ 1 = tenu)."""
    m = masse(H, ref, config, besoins)
    k_couple = (m / ref["M0"]) * (H / ref["H0"])
    k_vit = (H / ref["H0"]) ** -0.5
    out = {}
    for n, b in besoins.items():
        c = config[type_de(n)]
        out[n] = dict(
            rms=(marge * b["rms"] * k_couple / c["continu"]) if c["continu"] else None,
            pointe=marge * b["pointe"] * k_couple / c["pointe"],
            vitesse=(b["vit_pointe"] * k_vit / c["vitesse"]) if c["vitesse"] else None)
    return out


def h_max_couple(ref, config, besoins, marge, noms=None) -> tuple[float | None, int]:
    """Plus grand H tel que toutes les contraintes de COUPLE tiennent.

    Monotone croissant en H : dichotomie. Renvoie (H, itérations) ;
    H = None si même H_BAS ne tient pas.
    """
    noms = noms or list(besoins)

    def tient(H):
        r = ratios(H, ref, config, besoins, marge)
        return all(r[n]["pointe"] <= 1 and (r[n]["rms"] is None or r[n]["rms"] <= 1)
                   for n in noms)

    if not tient(H_BAS):
        return None, 0
    if tient(H_HAUT):
        return H_HAUT, 0
    lo, hi, it = H_BAS, H_HAUT, 0
    while hi - lo > TOL:
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if tient(mid) else (lo, mid)
        it += 1
    return lo, it


def h_min_vitesse(ref, config, besoins, noms=None) -> float:
    """Plus petit H tel que la vitesse requise tienne (elle décroît avec H)."""
    noms = noms or list(besoins)
    h = 0.0
    for n in noms:
        b, c = besoins[n], config[type_de(n)]
        if c["vitesse"]:
            # vitesse_P1·(H/H0)^−½ ≤ v  ⇔  H ≥ H0·(vitesse_P1/v)²
            h = max(h, ref["H0"] * (b["vit_pointe"] / c["vitesse"]) ** 2)
    return h


def evaluer(ref, config, besoins, marge) -> dict:
    """H_max de la configuration, par articulation et pour le robot."""
    manque = sorted({type_de(n) for n in besoins
                     if config[type_de(n)]["pointe"] is None or config[type_de(n)]["masse"] is None})
    if manque:
        return dict(indetermine=f"pointe ou masse inconnue pour : {', '.join(manque)}")
    H, it = h_max_couple(ref, config, besoins, marge)
    h_min = h_min_vitesse(ref, config, besoins)
    par_art = {}
    for t in JAMBE:
        noms = [n for n in besoins if type_de(n) == t]
        h_t, _ = h_max_couple(ref, config, besoins, marge, noms)
        r = ratios(H, ref, config, besoins, marge) if H else {}
        par_art[t] = dict(
            H_max=h_t, classe=config[t]["id"],
            rms_verifie=config[t]["continu"] is not None,
            vitesse_verifiee=config[t]["vitesse"] is not None,
            ecrete=any(besoins[n]["ecretage_moteur"] + besoins[n]["ecretage_frein"] > 0
                       for n in noms),
            limitante=bool(H and h_t is not None and abs(h_t - H) < 2 * TOL))
    return dict(H_max=H, iterations=it, H_min_vitesse=h_min,
                faisable=H is not None and H >= h_min,
                masse=masse(H, ref, config, besoins) if H else None,
                par_articulation=par_art,
                limitantes=[t for t, v in par_art.items() if v["limitante"]])


def reference(cat: dict, analyse: dict) -> dict:
    rt = cat["reference_toddlerbot"]
    M0 = val(rt["masse_totale_kg"])
    besoins = besoins_p1(analyse)
    masses = rt["masse_dynamixel_g"]
    m_jambes = sum(val(masses[b["modele"]]) for b in besoins.values()) / 1000
    return dict(H0=val(rt["hauteur_m"]), M0=M0, S0=M0 - m_jambes, m_jambes_P1=m_jambes)


def config_homogene(classe: dict) -> dict:
    return {t: classe for t in JAMBE}


def config_mixte(lourde: dict, legere: dict, articulations_lourdes) -> dict:
    return {t: (lourde if t in articulations_lourdes else legere) for t in JAMBE}


def config_toddlerbot(analyse: dict, dyn: dict) -> dict:
    """Chaque articulation avec SON modèle Dynamixel (identique gauche/droite)."""
    b = besoins_p1(analyse)
    return {t: dyn[b[f"left_{t}"]["modele"]] for t in JAMBE}


# ────────────────────────── contrôle de cohérence ───────────────────────

def controle_coherence(cat: dict, analyse: dict, ref: dict) -> list[str]:
    """Le calcul doit retrouver les robots de référence dans leur classe.

    Renvoie la liste des échecs — vide si tout tient. Marge 1 : un robot
    qui existe et qui marche n'a pas de marge à démontrer.
    """
    besoins = besoins_p1(analyse)
    dyn = classes_dynamixel(analyse, cat)
    echecs, rapport = [], []
    for rid, r in cat["controle_coherence"].items():
        H_ref = val(r["hauteur_m"])
        if r["classe"] == "toddlerbot":
            config = config_toddlerbot(analyse, dyn)
        else:
            config = config_homogene(classe_catalogue(cat, r["classe"]))
        ev = evaluer(ref, config, besoins, marge=1.0)
        if "indetermine" in ev:
            echecs.append(f"{rid} : indéterminé — {ev['indetermine']}")
            continue
        tol = val(cat["dimensionnement"]["tolerance_coherence_m"])
        ok = ev["H_max"] is not None and ev["H_max"] >= H_ref - tol and ev["H_min_vitesse"] <= H_ref
        rapport.append((rid, H_ref, ev))
        if not ok:
            echecs.append(
                f"{rid} : {H_ref:.2f} m attendu dans sa classe, le calcul donne "
                f"H_max = {ev['H_max'] if ev['H_max'] is None else round(ev['H_max'], 3)} m "
                f"(H_min vitesse {ev['H_min_vitesse']:.3f} m)")
    controle_coherence.rapport = rapport
    return echecs


# ─────────────────────────────── budget ─────────────────────────────────

def chf(prix: dict, taux: dict) -> float | None:
    """Conversion par les taux de référence BCE, tous exprimés POUR 1 EUR.

    Le taux croisé X -> CHF se calcule (CHF/EUR ÷ X/EUR) : il ne se déclare
    pas, sinon il divergerait des deux taux publiés.
    """
    v, dev = val(prix.get("valeur")), prix.get("devise")
    if v is None or dev is None:
        return None
    # Un prix relevé TTC étranger (ex. TVA allemande 19 %) est ramené HORS
    # TVA : c'est la TVA SUISSE qui s'applique ensuite, pas les deux.
    if prix.get("tva_incluse"):
        v = v / (1 + prix["tva_incluse"])
    if dev == "CHF":
        return v
    par_eur = taux["par_eur"]
    if val(par_eur.get(dev)) is None or val(par_eur.get("CHF")) is None:
        return None
    return v * val(par_eur["CHF"]) / val(par_eur[dev])


def couts(cat: dict, bud: dict, config: dict) -> dict:
    """Coût TTC par phase ; None dès qu'un poste est inconnu, et on dit lequel."""
    taux = bud["taux_de_change"]
    tva = val(bud["tva_ch"])
    imprevus = val(bud["marge_imprevus"])
    classes = {t: config[t]["id"] for t in JAMBE}
    lourde = max(set(classes.values()), key=lambda c: val(cat["candidats"][c]["couple_pointe_Nm"]) or 0)
    legere = min(set(classes.values()), key=lambda c: val(cat["candidats"][c]["couple_pointe_Nm"]) or 0)
    out = {}
    for pid, ph in bud["phases"].items():
        total, inconnus = 0.0, []
        for p in ph["postes"]:
            q = p["quantite"]
            if p["poste"].startswith("actionneur:"):
                quel = p["poste"].split(":", 1)[1]
                if quel == "jambes":
                    lignes = [((classes[t], cat["candidats"][classes[t]]["prix"]), 2) for t in JAMBE]
                else:
                    # `actionneur:<id>` : une classe PRÉCISE du catalogue,
                    # indépendante de la configuration (le banc proposé).
                    cid = quel if quel in cat["candidats"] else {"lourde": lourde, "legere": legere}[quel]
                    lignes = [((cid, cat["candidats"][cid]["prix"]), q)]
                for (cid, prix), n in lignes:
                    c = chf(prix, taux)
                    if c is None:
                        inconnus.append(f"prix {cat['candidats'][cid]['nom']}")
                    else:
                        total += c * n
            else:
                nom = p["poste"]
                if nom == "adaptateur_bus":
                    tout_ttl = all(c == "sts3250" for c in classes.values())
                    nom = "adaptateur_ttl" if tout_ttl else "adaptateur_can"
                e = bud["structure"] if nom == "structure" else bud["electronique"].get(nom)
                c = chf(e["prix"], taux) if e else None
                if c is None:
                    inconnus.append(nom)
                    continue
                total += c * q
        ht = total * (1 + imprevus)
        out[pid] = dict(ht_connu=total, avec_imprevus=ht, ttc=ht * (1 + tva),
                        inconnus=sorted(set(inconnus)))
    return out


# ─────────────────────────────── sortie ─────────────────────────────────

def configurations(cat: dict) -> list[tuple[str, dict]]:
    # Les candidats du seul comparatif S (`comparatif_seulement`) sont
    # traités par scripts/selection_multicritere.py, pas ici.
    ids = [i for i, c in cat["candidats"].items() if not c.get("comparatif_seulement")]
    cls = {i: classe_catalogue(cat, i) for i in ids}
    confs = [(f"homogène {cls[i]['nom']}", config_homogene(cls[i])) for i in ids]
    lourdes = cat["dimensionnement"]["articulations_lourdes"]
    for h in ids:
        for l in ids:
            ph, pl = cls[h]["pointe"], cls[l]["pointe"]
            if h != l and ph is not None and pl is not None and ph > pl:
                confs.append((f"mixte {cls[h]['nom']} / {cls[l]['nom']}",
                              config_mixte(cls[h], cls[l], lourdes)))
    return confs


def configurations_nommees(cat: dict) -> list[tuple[str, str, dict]]:
    """Les configurations nommées du catalogue (publiées au cadrage § 5)."""
    out = []
    for cid, c in (cat.get("configurations_nommees") or {}).items():
        lourde = classe_catalogue(cat, c["lourde"])
        legere = classe_catalogue(cat, c["legere"])
        out.append((cid, c["libelle"], config_mixte(lourde, legere, c["articulations_lourdes"])))
    return out


def f(x, n=2):
    return "—" if x is None else f"{x:.{n}f}".replace(".", ",")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--marge", type=float, default=None,
                    help="défaut : dimensionnement.marge de params/actionneurs.yaml")
    ap.add_argument("--markdown", action="store_true")
    a = ap.parse_args(argv)

    cat = charger_catalogue()
    bud = yaml.safe_load(BUDGET.read_text(encoding="utf-8"))
    if not AM.SERIE.exists():
        print(f"série absente : {AM.SERIE}\n  la régénérer : ~/upstream/toddlerbot/.venv/bin/python "
              "sim/upstream/enregistrer_marche.py")
        return 1
    analyse = AM.analyser(AM.SERIE)
    ref = reference(cat, analyse)
    marge = a.marge if a.marge is not None else val(cat["dimensionnement"]["marge"])

    echecs = controle_coherence(cat, analyse, ref)
    print(f"  référence : H0 {ref['H0']} m, M0 {ref['M0']:.3f} kg, dont 12 Dynamixel de jambe "
          f"{ref['m_jambes_P1']:.3f} kg -> S0 {ref['S0']:.3f} kg")
    print(f"  contrôle de cohérence ({len(cat['controle_coherence'])} robots, marge 1) :")
    for rid, H_ref, ev in controle_coherence.rapport:
        print(f"    {rid:12s} attendu {H_ref:.2f} m -> H_max {f(ev['H_max'], 3)} m, "
              f"H_min vitesse {f(ev['H_min_vitesse'], 3)} m, masse {f(ev['masse'])} kg, "
              f"limitantes {', '.join(ev['limitantes']) or '—'}")
    if echecs:
        print("\n✗ CONTRÔLE DE COHÉRENCE ÉCHOUÉ — aucun dimensionnement produit :")
        for e in echecs:
            print(f"    {e}")
        return 1

    besoins = besoins_p1(analyse)
    confs = configurations(cat)
    print(f"\n  {len(confs)} configurations, marge {marge} (décidée : fiche 0051)\n")
    lignes = []
    for nom, conf in confs:
        ev = evaluer(ref, conf, besoins, marge)
        lignes.append((nom, conf, ev))
        if "indetermine" in ev:
            print(f"  {nom:48s} indéterminé — {ev['indetermine']}")
            continue
        ec = [t for t in ev["limitantes"] if ev["par_articulation"][t]["ecrete"]]
        print(f"  {nom:48s} H_max {f(ev['H_max'], 3)} m  masse {f(ev['masse'])} kg  "
              f"H_min {f(ev['H_min_vitesse'], 3)}  limitée par {', '.join(ev['limitantes'])}"
              + ("  ⚠ PLAFOND OPTIMISTE (écrêté)" if ec else ""))
    nommees = []
    print()
    for cid, lib, conf in configurations_nommees(cat):
        ev = evaluer(ref, conf, besoins, marge)
        nommees.append((lib, conf, ev))
        print(f"  [{cid}] {lib}\n      H_max {f(ev.get('H_max'), 3)} m  masse {f(ev.get('masse'))} kg  "
              f"limitée par {', '.join(ev.get('limitantes') or [])}")
    if a.markdown:
        imprimer_markdown(cat, bud, lignes, marge, ref)
        imprimer_cadrage(lignes, nommees, marge)
    return 0


def _classes_de(conf) -> str:
    vus = []
    for t in JAMBE:
        c = conf[t]
        if c["id"] not in [v["id"] for v in vus]:
            vus.append(c)
    return " ; ".join(f"{c['nom'].replace('RobStride ', '').replace('Feetech ', '').replace('CubeMars ', '')} "
                      f"{f(c['continu'], 1) if c['continu'] is not None else 'null'} / {f(c['pointe'], 1)}"
                      for c in vus)


def imprimer_cadrage(lignes, nommees, marge):
    """Le tableau du cadrage § 5 — engendré, jamais recopié à la main."""
    print("\n### TABLEAU_CADRAGE\n")
    print(f"| Configuration (marge {f(marge, 1)}) | Continu / pointe (N·m) | Taille maximale | "
          "Masse convergée | Articulation limitante |")
    print("| --- | --- | ---: | ---: | --- |")
    rangs = [(n, c, e) for n, c, e in lignes if n.startswith("homogène")] + nommees
    for nom, conf, ev in rangs:
        if "indetermine" in ev:
            print(f"| {nom} | {_classes_de(conf)} | — | — | indéterminé |")
            continue
        print(f"| {nom} | {_classes_de(conf)} | {f(ev['H_max'])} m | {f(ev['masse'], 1)} kg | "
              f"{', '.join(ev['limitantes'])} |")
    print("\nToutes ces tailles sont des **plafonds optimistes** : le roulis de hanche, "
          "et d'autres articulations de jambe, étaient écrêtés dans la marche de référence.")


def imprimer_markdown(cat, bud, lignes, marge, ref):
    print("\n### TABLEAU_TAILLES\n")
    print("| Configuration | H max (m) | Masse convergée (kg) | H min vitesse (m) | Articulation limitante | Plafond optimiste ? | Contrainte RMS vérifiée ? |")
    print("| --- | ---: | ---: | ---: | --- | --- | --- |")
    for nom, conf, ev in lignes:
        if "indetermine" in ev:
            print(f"| {nom} | — | — | — | indéterminé : {ev['indetermine']} | — | — |")
            continue
        lim = ev["limitantes"]
        ec = any(ev["par_articulation"][t]["ecrete"] for t in lim)
        rms = all(ev["par_articulation"][t]["rms_verifie"] for t in JAMBE)
        vit = all(ev["par_articulation"][t]["vitesse_verifiee"] for t in JAMBE)
        print(f"| {nom} | {f(ev['H_max'])} | {f(ev['masse'], 1)} | "
              f"{f(ev['H_min_vitesse']) if vit else '**non vérifiable**'} | "
              f"{', '.join(lim)} | {'**oui**' if ec else 'non'} | {'oui' if rms else '**non** (continu inconnu)'} |")
    print("\n### TABLEAU_ARTICULATIONS\n")
    print("| Configuration | " + " | ".join(JAMBE) + " |")
    print("| --- | " + " | ".join("---:" for _ in JAMBE) + " |")
    for nom, conf, ev in lignes:
        if not nom.startswith("homogène") or "indetermine" in ev:
            continue
        cells = []
        for t in JAMBE:
            p = ev["par_articulation"][t]
            cells.append(f"{f(p['H_max'])}{' ⚠' if p['ecrete'] else ''}")
        print(f"| {nom} | " + " | ".join(cells) + " |")
    print("\n### TABLEAU_COUTS\n")
    print("| Configuration | H max (m) | " + " | ".join(f"{ph} TTC (CHF)" for ph in bud["phases"]) + " | Postes inconnus |")
    print("| --- | ---: | " + " | ".join("---:" for _ in bud["phases"]) + " | --- |")
    for nom, conf, ev in lignes:
        if "indetermine" in ev:
            continue
        c = couts(cat, bud, conf)
        inc = sorted({i for v in c.values() for i in v["inconnus"]})
        def cellule(x):
            if x["inconnus"] and x["ht_connu"] == 0:
                return "inconnu"
            s = f"{x['ttc']:,.0f}".replace(",", " ")
            return f"≥ {s}" if x["inconnus"] else s
        print(f"| {nom} | {f(ev['H_max'])} | " + " | ".join(cellule(c[p]) for p in bud["phases"])
              + f" | {', '.join(inc) or '—'} |")


if __name__ == "__main__":
    sys.exit(main())
