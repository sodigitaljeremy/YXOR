#!/usr/bin/env python3
"""Capacités -> tâches en niveaux : contrôle des noms, rapport engendré.

    .venv/bin/python scripts/capacites.py            # contrôle et résumé
    .venv/bin/python scripts/capacites.py --ecrire   # docs/capacites-niveaux.md

Créé le 2026-10-05 (phase 2 de la stratégie de la fiche 0069). Lit
params/capacites.yaml. Rien n'est chiffré : les niveaux sont des valeurs à
BALAYER en phase 3, et budget et masse sont des SORTIES (principe de Jeremy,
en tête du fichier de paramètres).

Contrôle (règle 3) : chaque articulation sollicitée est un nom de
params/joints.yaml ou un nom de `noms_a_creer`, ANNONCÉ.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
CAP = REPO / "params" / "capacites.yaml"
DOC = REPO / "docs" / "capacites-niveaux.md"


def lire(p: Path) -> dict:
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def noms_joints() -> set:
    j = lire(REPO / "params" / "joints.yaml")
    return {x["nom"] for g in ("jambes", "bras", "taille", "nuque") for x in j[g]}


def controler(cap: dict, joints: set) -> tuple[list[str], list[str]]:
    """(fautes, noms à créer réellement employés)."""
    a_creer = set(cap.get("noms_a_creer") or {})
    fautes, employes = [], set()
    if not cap.get("taches"):
        fautes.append("capacites.yaml : aucune tâche")
    for tid, t in (cap.get("taches") or {}).items():
        if t.get("methode") not in (cap.get("methodes") or {}):
            fautes.append(f"{tid} : méthode « {t.get('methode')} » inconnue")
        if len(t.get("niveaux") or []) < 2:
            fautes.append(f"{tid} : moins de deux niveaux, rien à balayer")
        for n in t.get("sollicite") or []:
            if n in joints:
                continue
            if n in a_creer:
                employes.add(n)
            else:
                fautes.append(f"{tid} : « {n} » n'est ni dans joints.yaml ni dans noms_a_creer (règle 3)")
    fautes += controler_profils(cap)
    return fautes, sorted(employes)


def niveaux_de(v) -> list:
    """Un niveau de profil : une valeur, une liste de valeurs, ou null (à balayer)."""
    return [] if v is None else (list(v) if isinstance(v, list) else [v])


def controler_profils(cap: dict) -> list[str]:
    """Profils (ajouté le 2026-10-07) : tâches et niveaux existants ; lab ⊂ final ; réservé au final hors du lab."""
    fautes, taches = [], cap.get("taches") or {}
    pr = cap.get("profils") or {}
    for nom in ("lab", "final"):
        if nom not in pr:
            fautes.append(f"profil « {nom} » absent")
    for nom, p in pr.items():
        for t, v in {**(p.get("taches") or {}), **(p.get("reserve_au_final") or {})}.items():
            if t not in taches:
                fautes.append(f"profil {nom} : tâche « {t} » inconnue")
                continue
            for n in niveaux_de(v):
                if n not in taches[t]["niveaux"]:
                    fautes.append(f"profil {nom} : niveau « {n} » inconnu pour {t} ({taches[t]['niveaux']})")
    if "lab" in pr and "final" in pr:
        lab, fin = pr["lab"].get("taches") or {}, pr["final"].get("taches") or {}
        fautes += [f"profil lab : {t} absent du final (le Lab est un sous-ensemble)" for t in lab if t not in fin]
        for t, v in (pr["lab"].get("reserve_au_final") or {}).items():
            if t in lab and (v is None or set(niveaux_de(v)) & set(niveaux_de(lab[t]))):   # null : la tâche entière
                fautes.append(f"profil lab : {t} {v} est réservé au final mais retenu pour le Lab")
    return fautes


def doc(cap: dict) -> str:
    def niv(t):
        u = t.get("unite")
        return " / ".join(f"{x:g}" if isinstance(x, (int, float)) else str(x) for x in t["niveaux"]) \
            + (f" {u}" if u and u != "—" else "")
    L = ["# Capacités de YXOR : tâches et niveaux à balayer", "",
         "**Engendré** par `.venv/bin/python scripts/capacites.py --ecrire` depuis `params/capacites.yaml`. "
         "Ne pas éditer à la main. Données seulement, **aucune décision**, rien de chiffré (phase 2 de la "
         "stratégie de la fiche 0069).", "",
         "**Principe de Jeremy** (2026-10-05, ses mots) : « Je ne veux plus \"fixer\" de budget, je veux "
         "calculer le budget en fonction des contraintes et de ce qu'il est réellement possible de faire » ; "
         "« je veux arbitrer avec des vrais chiffres et non des estimations ». Budget et masse sont des "
         "SORTIES de l'explorateur, jamais des filtres.", "",
         "Les capacités sont celles de la fiche 0069. **Capacités et niveaux CONFIRMÉS par Jeremy le "
         "2026-10-05**, ses mots : « Je confirme la stratégie telle que reformulée par Claude, les capacités que j'ai cochées, et les niveaux proposés dans params/capacites.yaml ». Les articulations sollicitées et les méthodes restent **PROPOSÉES "
         "par Claude** ; † = niveaux ajoutés par Claude le 2026-10-05 pour une capacité cochée qui n'en avait "
         "pas (confirmés avec les autres). *En italique* : un axe qui n'existe pas encore dans "
         "`params/joints.yaml` (nom à créer).", "",
         "| Tâche | Grandeur | Niveaux à balayer | Articulations sollicitées | Méthode (phase 3) |",
         "| --- | --- | --- | --- | --- |"]
    joints = noms_joints()
    for tid, t in cap["taches"].items():
        arts = ", ".join(n if n in joints else f"*{n}*" for n in t["sollicite"])
        L.append(f"| {t['capacite']}{' †' if t.get('ajoute_dans_ce_lot') else ''}"
                 f"{' ‡ **PROPOSÉE**' if t.get('proposee') else ''} | {t['grandeur']} | "
                 f"{niv(t)} | {arts or '—'} | {t['methode']} |")
    if any(t.get("proposee") for t in cap["taches"].values()):
        L += ["", "‡ **PROPOSÉE** par Claude le 2026-10-07, À CONFIRMER par Jeremy : hors de la confirmation du "
              "2026-10-05. Cycle d'autonomie proposé : "
              + cap["taches"]["autonomie"]["cycle"]["definition"] + "."]
    pr = cap.get("profils") or {}
    if pr:
        f = lambda v: "à balayer" if v is None else " et ".join(str(x) for x in niveaux_de(v))
        L += ["", "## Profils cibles", "",
              "**YXOR Lab : DÉCIDÉ par Jeremy le 2026-10-07**, ses mots : « Je retiens pour YXOR Lab : marche sur sol "
              "plat 0,6 m/s, sol irrégulier 2 cm, pente 5°, relevé sur le dos et sur le ventre, saut 10 cm, gestes 2 m/s, "
              "saisie 0,2 kg, poussée 20 N, buste en lacet seul, tête à 2 axes, visage sur écran. Réservé au final : "
              "inclinaison du buste, port de charges lourdes, course, mains à doigts. » YXOR (final) : les capacités de "
              "la fiche 0069, niveaux à balayer (phase 4b).", "",
              "| Tâche | YXOR Lab | YXOR (final) |", "| --- | --- | --- |"]
        lab, fin = pr["lab"]["taches"], pr["final"]["taches"]
        res = pr["lab"].get("reserve_au_final") or {}
        for t in cap["taches"]:
            l_ = f(lab[t]) if t in lab else ("réservé au final" if t in res else "—")
            L.append(f"| {t.replace('_', ' ')} | {l_} | {f(fin[t]) if t in fin else '—'} |")
    L += ["", "## Méthodes", ""] + [f"- **{k}** : {v}." for k, v in cap["methodes"].items()]
    L += ["", "## Noms d'axes à créer (PROPOSÉS, hors de `joints.yaml`)", ""]
    L += [f"- *{k}* ({v['groupe']}) : {v['note']}." for k, v in cap["noms_a_creer"].items()]
    L += ["", "## Sorties de l'explorateur, pour chaque solution", "",
          "| Sortie | Unité | Formule |", "| --- | --- | --- |"]
    L += [f"| {k.replace('_', ' ')} | {v['unite']} | {v['formule']} |" for k, v in cap["sorties_explorateur"].items()]
    n = 1
    for t in cap["taches"].values():
        n *= len(t["niveaux"])
    n_txt = f"{n:,}".replace(",", " ")                  # séparateur de milliers à la française
    L += ["", f"Balayage complet : {len(cap['taches'])} tâches, produit des niveaux = {n_txt} combinaisons "
          "de capacités (avant le choix des axes et des actionneurs)."]
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ecrire", action="store_true")
    a = ap.parse_args(argv)
    cap = lire(CAP)
    fautes, employes = controler(cap, noms_joints())
    nn = sum(len(t["niveaux"]) for t in cap["taches"].values())
    print(f"  {len(cap['taches'])} tâches, {nn} niveaux ; noms à créer employés : {', '.join(employes) or '—'}")
    for f in fautes:
        print(f"  ✗ {f}")
    if a.ecrire and not fautes:
        DOC.write_text(doc(cap), encoding="utf-8")
        print(f"  -> {DOC.relative_to(REPO)}")
    return 1 if fautes else 0


if __name__ == "__main__":
    sys.exit(main())
