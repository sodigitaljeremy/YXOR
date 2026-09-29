#!/usr/bin/env python3
"""Une règle qui ne correspond à rien — le garde-fou qu'on croit avoir.

    .venv/bin/python scripts/controle_regles.py

═══════════════════════════════════════════════════════════════════════
 POURQUOI
═══════════════════════════════════════════════════════════════════════

`origines.yaml` déclare 43 règles, `nullites.yaml` 13. Rien ne disait
qu'une seule d'entre elles correspondait à quelque chose.

Une règle morte ne se signale jamais : elle ne lève pas, elle ne
s'affiche pas, elle est simplement ignorée. Et elle est pire qu'une règle
absente — parce qu'on la lit, on la croit appliquée, et on construit
dessus. C'est exactement la faute de la « phase 6 » (fiche 0027), portée
au niveau du motif.

Trois façons pour une règle de mourir, et les trois sont détectées :

  1. son motif ne correspond à AUCUNE clé du fichier visé — faute de
     frappe, ou renommage d'une table (la migration du 2026-09-29 aurait
     pu en laisser six) ;
  2. elle est MASQUÉE par une règle plus générale placée avant elle :
     `origines.yaml` et `nullites.yaml` prennent le PREMIER motif qui
     correspond, donc une règle précise écrite après un joker ne sert
     jamais ;
  3. elle vise un fichier qui n'existe plus.

Le cas 2 est le plus vicieux : la règle correspond, elle est simplement
inatteignable. Aucun test de correspondance seul ne la trouve.
"""
from __future__ import annotations
import sys
from pathlib import Path

import yaml

from audit_origines import correspond, lire_yaml_plat
import procedes as PROC

REPO = Path(__file__).resolve().parent.parent
PARAMS = REPO / "params"


def _cles_du_fichier(nom: str) -> list[str]:
    f = PARAMS / nom
    if not f.exists():
        return []
    return [c for c, _ in lire_yaml_plat(f)]


def _regles(fichier: str) -> dict[str, list[dict]]:
    doc = yaml.safe_load((PARAMS / fichier).read_text(encoding="utf-8")) or {}
    return {f: (d or {}).get("regles", [])
            for f, d in (doc.get("fichiers") or {}).items()}


# `piece` n'est pas un fichier de params/ : c'est le bloc `piece:` des
# relevés déposés par les pièces. Ses clés se lisent ailleurs.
def _cles_des_pieces() -> list[str]:
    out = []
    for f in sorted((REPO / "parts").glob("*.origines.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        out += list((d.get("piece") or {}).keys())
    return out


def _valeur(doc, chemin: str):
    cur = doc
    for seg in chemin.split("."):
        if not isinstance(cur, dict) or seg not in cur:
            return _ABSENT
        cur = cur[seg]
    return cur


_ABSENT = object()


def _condition_possible(regle: dict, cible: str, chemin: str) -> bool:
    """La condition `si:` de cette règle tient-elle pour CETTE clé ?

    Sans condition, la règle gagne dès qu'elle correspond. Avec une
    condition, il faut la résoudre sur la donnée réelle — sinon on
    déclarerait masquée une règle qui s'applique parfaitement.
    """
    si = regle.get("si")
    if si is None:
        return True
    if cible == "piece":
        return True                       # résolue ailleurs, hors de portée
    doc = yaml.safe_load((PARAMS / cible).read_text(encoding="utf-8")) or {}
    if "chemin" in si:
        return _valeur(doc, si["chemin"]) == si.get("vaut")

    # Condition sur une clé SŒUR. Il faut la résoudre sur la MÊME forme de
    # donnée que celle qu'emploie l'exécution, sinon on mesure autre chose
    # que ce qui tourne : un réglage brut n'a pas de champ `epaisseur`,
    # elle vient de la matière et n'apparaît qu'après jointure. Évaluer la
    # règle sur le YAML brut la déclarerait morte alors qu'elle s'applique.
    parent = _valeur(doc, chemin.rsplit(".", 1)[0]) if "." in chemin else doc
    if chemin.startswith("reglages."):
        rid = chemin.split(".")[1]
        parent = PROC.reglages(doc).get(rid, parent)
    if not isinstance(parent, dict) or si["cle"] not in parent:
        return False
    return parent[si["cle"]] == si.get("vaut")


def controler(fichier: str) -> list[str]:
    fautes = []
    for cible, regles in _regles(fichier).items():
        cles = _cles_des_pieces() if cible == "piece" else _cles_du_fichier(cible)
        if not cles:
            fautes.append(f"{fichier} : le bloc « {cible} » ne vise aucune "
                          f"clé existante — fichier absent ou vide")
            continue
        # Pour chaque clé, quelle règle GAGNE : la première qui correspond
        # ET dont la condition tient. Ignorer les conditions ferait crier
        # au loup — une règle `si:` ne masque rien, puisqu'elle ne gagne
        # pas toujours. Un contrôle qui se trompe finit ignoré.
        gagnantes = set()
        for c in cles:
            for i, r in enumerate(regles):
                if not correspond(r["motif"], c):
                    continue
                if _condition_possible(r, cible, c):
                    gagnantes.add(i)
                    break
        for i, r in enumerate(regles):
            if i in gagnantes:
                continue
            motif = r["motif"]
            correspondants = [c for c in cles if correspond(motif, c)]
            if not correspondants:
                fautes.append(f"{fichier} / {cible} : le motif « {motif} » ne "
                              f"correspond à aucune clé")
            else:
                # Elle correspond mais ne gagne jamais : une règle placée
                # AVANT la capte. On nomme la coupable, sinon la faute est
                # illisible.
                for j, autre in enumerate(regles[:i]):
                    if correspond(autre["motif"], correspondants[0]):
                        fautes.append(
                            f"{fichier} / {cible} : le motif « {motif} » est "
                            f"MASQUÉ par « {autre['motif']} », déclaré avant "
                            f"lui — il ne s'applique jamais")
                        break
    return fautes


def main() -> int:
    total, fautes = 0, []
    for f in ("origines.yaml", "nullites.yaml"):
        n = sum(len(r) for r in _regles(f).values())
        total += n
        fautes += controler(f)
    if fautes:
        print(f"\n✗ RÈGLES MORTES — {len(fautes)} sur {total} :")
        for x in fautes:
            print(f"   {x}")
        print("\n  Une règle qui ne s'applique jamais est un garde-fou qu'on")
        print("  croit avoir. La corriger, ou la retirer en le disant.")
        return 1
    print(f"   règles déclaratives : {total} motifs, tous atteints")
    return 0


if __name__ == "__main__":
    sys.exit(main())
