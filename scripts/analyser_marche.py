#!/usr/bin/env python3
"""Analyse d'une marche enregistrée : couples, vitesses, écrêtage, par actionneur.

    .venv/bin/python scripts/analyser_marche.py
    .venv/bin/python scripts/analyser_marche.py --serie exports/actionneurs/marche_15s.csv

Venv DU PROJET. La série vient de `sim/upstream/enregistrer_marche.py`
(venv amont) ; elle vit dans `exports/` et se régénère.

Les modèles de moteur et leurs bornes sont LUS dans les données amont au
commit épinglé, comme source de données, jamais importés comme code —
même statut que `import_upstream_limits.py` :

  toddlerbot/descriptions/default.yml          section `motors` : moteur -> modèle
                                               section `actuators` : bornes par modèle
  toddlerbot/descriptions/toddlerbot_2xc/*.xml classe de chaque articulation

═══════════════════════════════════════════════════════════════════════
 L'ÉCRÊTAGE, OU POURQUOI UNE POINTE PEUT MENTIR
═══════════════════════════════════════════════════════════════════════

La simulation amont borne le couple (`toddlerbot/sim/motor_control.py`) :
en moteur, `tau_max` jusqu'à `q_dot_tau_max` puis une pente jusqu'à
`tau_q_dot_max` à `q_dot_max` ; en freinage, `tau_brake_max`. Un couple
enregistré ne peut donc PAS dépasser ces bornes. Quand il les atteint, la
pointe mesurée est la borne du moteur simulé, pas le besoin de la marche :
une BORNE BASSE du besoin. Ce script compte ces échantillons, par
actionneur, pour que personne ne prenne une borne pour une mesure.
Le comptage utilise la vitesse relevée APRÈS le pas : il est approché.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
AMONT = Path(os.environ.get("TODDLERBOT_ROOT", Path.home() / "upstream/toddlerbot"))
DESC = AMONT / "toddlerbot" / "descriptions"
DEFAULT_YML = DESC / "default.yml"
MJCF = DESC / "toddlerbot_2xc" / "toddlerbot_2xc.xml"
SERIE = REPO / "exports" / "actionneurs" / "marche_15s.csv"
SORTIE = REPO / "exports" / "actionneurs" / "marche_analyse.json"

SEUIL_ECRETAGE = 0.99       # fraction de la borne à partir de laquelle on compte


def zone(nom: str) -> str:
    if nom.startswith("neck"):
        return "cou"
    if nom.startswith("waist"):
        return "taille"
    if any(k in nom for k in ("hip", "knee", "ankle")):
        return "jambes"
    return "bras"


def modeles_amont() -> dict:
    """Moteur -> modèle, bornes par modèle, classe MJCF — avec les lignes."""
    texte = DEFAULT_YML.read_text(encoding="utf-8")
    lignes = texte.splitlines()
    doc = yaml.safe_load(texte)
    moteur, courant, section = {}, None, None
    bornes_ligne: dict[str, dict[str, int]] = {}
    for i, l in enumerate(lignes, 1):
        if re.match(r"^[a-z_]+:\s*$", l):
            section = l.rstrip(":").strip()
        m = re.match(r"^    ([A-Za-z0-9_\-]+):\s*$", l)
        if m:
            courant = m.group(1)
        m = re.match(r"^        motor:\s*(\S+)", l)
        if m and section == "motors":
            moteur[courant] = (m.group(1), i)
        m = re.match(r"^        (tau_max|q_dot_max|tau_q_dot_max|q_dot_tau_max|tau_brake_max):", l)
        if m and section == "actuators":
            bornes_ligne.setdefault(courant, {})[m.group(1)] = i
    xml = MJCF.read_text(encoding="utf-8").splitlines()
    classe = {}
    for i, l in enumerate(xml, 1):
        for m in re.finditer(r'<joint [^>]*?name="([^"]+)"', l):
            for k in range(i, min(i + 4, len(xml) + 1)):
                c = re.search(r'class="([^"]+)"', xml[k - 1])
                if c:
                    classe[m.group(1)] = (c.group(1), k)
                    break
    return dict(moteur=moteur, bornes=doc["actuators"], bornes_ligne=bornes_ligne,
                classe=classe)


def limite_moteur(p: dict, vit: float) -> float:
    """Borne en moteur à la vitesse |vit| (courbe de motor_control.py)."""
    av = abs(vit)
    if av <= p["q_dot_tau_max"]:
        return p["tau_max"]
    pente = (p["tau_q_dot_max"] - p["tau_max"]) / (p["q_dot_max"] - p["q_dot_tau_max"])
    return max(p["tau_max"] + pente * (av - p["q_dot_tau_max"]), 0.0)


def lire_serie(chemin: Path):
    with chemin.open(encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    tete = rows[0]
    data = [[float(x) for x in r] for r in rows[1:]]
    noms = [h[4:] for h in tete if h.startswith("tau:")]
    if not noms or not data:
        raise SystemExit(f"série vide ou sans colonnes tau: — {chemin}")
    return tete, data, noms


def analyser(chemin: Path = SERIE) -> dict:
    tete, data, noms = lire_serie(chemin)
    M = modeles_amont()
    n = len(noms)
    res = []
    for j, nom in enumerate(noms):
        tau = [r[1 + j] for r in data]
        vit = [r[1 + n + j] for r in data]
        mod, l_mot = M["moteur"][nom]
        p = M["bornes"][mod]
        ec_m = sum(1 for t, v in zip(tau, vit)
                   if t * v >= 0 and abs(t) >= SEUIL_ECRETAGE * limite_moteur(p, v))
        ec_f = sum(1 for t, v in zip(tau, vit)
                   if t * v < 0 and abs(t) >= SEUIL_ECRETAGE * p["tau_brake_max"])
        cl, l_cl = M["classe"].get(nom, (None, None))
        res.append(dict(
            nom=nom, zone=zone(nom), modele=mod, ligne_default_yml=l_mot,
            classe_mjcf=cl, ligne_mjcf=l_cl,
            tau_max=p["tau_max"], tau_brake_max=p["tau_brake_max"], q_dot_max=p["q_dot_max"],
            pointe=max(abs(x) for x in tau),
            rms=math.sqrt(sum(x * x for x in tau) / len(tau)),
            vit_pointe=max(abs(x) for x in vit),
            puiss_pointe=max(abs(t * v) for t, v in zip(tau, vit)),
            ecretage_moteur=ec_m, ecretage_frein=ec_f, n=len(tau)))
    return dict(serie=str(chemin.relative_to(REPO) if chemin.is_relative_to(REPO) else chemin),
                pas=len(data), t0=data[0][0], t1=data[-1][0],
                bornes_ligne=M["bornes_ligne"], actionneurs=res)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--serie", default=str(SERIE))
    a = ap.parse_args(argv)
    chemin = Path(a.serie)
    if not chemin.is_absolute():
        chemin = REPO / chemin
    if not chemin.exists():
        print(f"série absente : {chemin}\n  la régénérer : ~/upstream/toddlerbot/.venv/bin/python "
              "sim/upstream/enregistrer_marche.py")
        return 1
    r = analyser(chemin)
    concordants = sum(1 for x in r["actionneurs"] if x["classe_mjcf"] == x["modele"])
    print(f"  {r['pas']} pas, {len(r['actionneurs'])} actionneurs ; modèle default.yml "
          f"= classe MJCF pour {concordants}/{len(r['actionneurs'])}")
    print(f"  {'actionneur':26s} {'modèle':11s} {'pointe':>7} {'RMS':>7} {'ω pk':>6} {'écrêté':>8}")
    for x in r["actionneurs"]:
        e = x["ecretage_moteur"] + x["ecretage_frein"]
        print(f"  {x['nom']:26s} {x['modele']:11s} {x['pointe']:7.3f} {x['rms']:7.3f} "
              f"{x['vit_pointe']:6.2f} {e:4d}/{x['n']}")
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  -> {SORTIE.relative_to(REPO)}")
    return 0 if concordants == len(r["actionneurs"]) else 1


if __name__ == "__main__":
    sys.exit(main())
