#!/usr/bin/env python3
"""Noms d'articulations : les mêmes partout (CLAUDE.md, règle 3).

    .venv/bin/python scripts/controle_articulations.py

Créé le 2026-10-01 (refonte R4). Une comparaison de LISTES, rien d'autre :

  1. les moteurs de params/joints.yaml (côté droit déduit du gauche) ==
     les actionneurs du MJCF amont (params/upstream_joints.generated.yaml) ;
  2. les articulations référencées par joints.yaml == celles du MJCF ;
  3. les noms écrits dans le code et les paramètres (dimensionnement.JAMBE,
     articulations lourdes, relevé de params/exigences_S.yaml) existent
     parmi les moteurs de jambe ;
  4. les colonnes de la série de simulation existent parmi les actionneurs
     du MJCF — SAUTÉ, et dit, si la série n'est pas là (construction Docker).

YXOR n'a pas encore d'URDF ni de MJCF propre (`robot/` est vide) : le
modèle de référence est celui de ToddlerBot. Le contrôle annonce la TAILLE
de chaque liste comparée ; une liste vide est une faute.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
REPO = Path(__file__).resolve().parents[1]
P = REPO / "params"
GROUPES = ("jambes", "bras", "taille", "nuque")


def sans_cote(n: str) -> str:
    return re.sub(r"^(left|right)_", "", n)


def miroir(noms) -> set:
    out = set(noms)
    out |= {"right_" + n[len("left_"):] for n in noms if n.startswith("left_")}
    return out


def lire(nom: str) -> dict:
    return yaml.safe_load((P / nom).read_text(encoding="utf-8"))


def comparer(joints: dict, amont: dict, code: dict[str, list], serie: list | None) -> tuple[list, list]:
    """Renvoie (lignes du rapport, fautes). Toutes les entrées sont des données."""
    lignes, fautes = [], []
    mot = miroir([m for g in GROUPES for j in joints.get(g, []) for m in j["actionnement"]["moteurs"]])
    art = miroir([j["articulation"]["source"].split("/")[-1] for g in GROUPES for j in joints.get(g, [])])
    u_act = {a["nom"] for a in amont.get("actionneurs", [])}
    u_art = {a["nom"] for a in amont.get("articulations", [])}
    jambe = {sans_cote(m) for j in joints.get("jambes", []) for m in j["actionnement"]["moteurs"]}
    for titre, a, b in (("moteurs joints.yaml / actionneurs MJCF", mot, u_act),
                        ("articulations joints.yaml / articulations MJCF", art, u_art)):
        lignes.append(f"{titre} : {len(a)} / {len(b)}")
        if not a or not b:
            fautes.append(f"{titre} : liste vide")
        for n in sorted(a - b):
            fautes.append(f"{titre} : « {n} » absent du MJCF")
        for n in sorted(b - a):
            fautes.append(f"{titre} : « {n} » du MJCF absent de joints.yaml")
    lignes.append(f"moteurs de jambe (sans côté) : {len(jambe)}")
    for ou, noms in code.items():
        lignes.append(f"{ou} : {len(noms)} noms")
        if not noms:
            fautes.append(f"{ou} : liste vide")
        for n in noms:
            if n not in jambe:
                fautes.append(f"{ou} : « {n} » n'est pas un moteur de jambe de joints.yaml")
    if serie is None:
        lignes.append("série de simulation : SAUTÉ (fichier absent : exports/ n'est ni suivi ni copié dans l'image)")
    else:
        lignes.append(f"série de simulation : {len(serie)} actionneurs")
        for n in serie:
            if n not in u_act:
                fautes.append(f"série de simulation : « {n} » absent du MJCF")
    return lignes, fautes


def noms_du_code() -> dict[str, list]:
    import dimensionnement as D
    cat, ex = lire("actionneurs.yaml"), lire("exigences_S.yaml")
    out = {"dimensionnement.JAMBE": list(D.JAMBE),
           "actionneurs.yaml dimensionnement.articulations_lourdes":
               list(cat["dimensionnement"]["articulations_lourdes"]),
           "exigences_S.yaml releve.articulations": list(ex["releve"]["articulations"]),
           "configuration_S.yaml jambes": list(lire("configuration_S.yaml")["jambes"])}
    for cid, c in (cat.get("configurations_nommees") or {}).items():
        if c.get("articulations_lourdes"):
            out[f"configurations_nommees.{cid}"] = list(c["articulations_lourdes"])
    return out


def controler_squelette(joints: dict, squelette: dict) -> tuple[str, list]:
    """Les articulations de params/squelette.yaml portent les noms de joints.yaml (règle 3).

    Un nom absent de joints.yaml n'est admis que marqué `nom_provisoire`, et il
    est ANNONCÉ (2026-10-03 : la pince n'a pas encore de nom stable).
    """
    noms = {j["nom"] for g in GROUPES for j in joints.get(g, [])}
    arts = squelette.get("articulations") or []
    prov = [a["nom"] for a in arts if a.get("nom_provisoire")]
    fautes = [f"squelette.yaml : « {a['nom']} » absent de joints.yaml (et non marqué nom_provisoire)"
              for a in arts if a["nom"] not in noms and not a.get("nom_provisoire")]
    if not arts:
        fautes.append("squelette.yaml : aucune articulation")
    return (f"squelette.yaml : {len(arts)} articulations décrites (côté gauche et centre), "
            f"dont {len(prov)} à nom provisoire ({', '.join(prov) or '—'})"), fautes


def noms_serie() -> list | None:
    import analyser_marche as AM
    if not AM.SERIE.exists():
        return None
    import dimensionnement as D
    return sorted(D.besoins_p1(AM.analyser(AM.SERIE)))


def main(argv=None) -> int:
    lignes, fautes = comparer(lire("joints.yaml"), lire("upstream_joints.generated.yaml"),
                              noms_du_code(), noms_serie())
    l_sq, f_sq = controler_squelette(lire("joints.yaml"), lire("squelette.yaml"))
    lignes.append(l_sq)
    fautes += f_sq
    print("   noms d'articulations — " + " ; ".join(lignes))
    if fautes:
        print("\n✗ NOMS D'ARTICULATIONS INCOHÉRENTS :")
        for f in fautes:
            print(f"   {f}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
