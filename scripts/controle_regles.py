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

═══════════════════════════════════════════════════════════════════════
 ET LA QUATRIÈME : LE FOURRE-TOUT QUI NE PEUT PAS ÉCHOUER
═══════════════════════════════════════════════════════════════════════

Un motif `**` qui capte tout un fichier rend `non_qualifie` INATTEIGNABLE
pour ce fichier. L'audit y sort vert par construction, quoi qu'on y
écrive. Ce n'est pas une règle morte — c'est l'inverse : une règle trop
vivante, qui avale ce qu'elle devrait laisser signaler.

Mesuré le 2026-09-29 : 755 valeurs sur 1431, soit **54 % de l'audit**,
étaient couvertes par deux motifs `**` seuls. Le chiffre « 0 non
qualifiée » était donc à moitié vide de sens.

Un fourre-tout reste parfois le bon choix — un fichier ENGENDRÉ n'a pas
à être qualifié ligne à ligne. Mais alors il doit être **assumé**, pas
subi : `fourre_tout: true` sur la règle, et un motif écrit.
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


SEUIL_FOURRE_TOUT = 0.50      # au-delà, un joker doit être assumé


def controler_absorption(fichier: str) -> list[str]:
    """Un motif qui capte plus de la moitié d'un fichier doit le dire.

    Sinon le vert de l'audit ne vaut rien pour ce fichier : aucune valeur
    ne peut y ressortir `non_qualifie`, quoi qu'on y écrive.
    """
    fautes = []
    for cible, regles in _regles(fichier).items():
        if cible == "piece":
            continue
        cles = _cles_du_fichier(cible)
        if not cles:
            continue
        for r in regles:
            if "**" not in r["motif"]:
                continue
            n = sum(1 for c in cles
                    if next((x for x in regles if correspond(x["motif"], c)), None) is r)
            part = n / len(cles)
            if part < SEUIL_FOURRE_TOUT or r.get("fourre_tout"):
                continue
            fautes.append(
                f"{fichier} / {cible} : « {r['motif'] } » capte {n} valeurs "
                f"sur {len(cles)} ({part:.0%}) — `non_qualifie` est "
                f"INATTEIGNABLE pour ce fichier. Affiner le motif, ou "
                f"assumer le fourre-tout avec `fourre_tout: true`")
    return fautes


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


def controler_rayon() -> list[str]:
    """`rayon_interieur_min == 0,5 x epaisseur`, sur TOUTE la table.

    CLAUDE.md pose la règle, et la pièce la vérifiait — pour le seul
    réglage qu'elle employait. Les cinq autres n'étaient contrôlés par
    rien : une valeur fausse y aurait attendu la première pièce qui s'en
    serait servie, c'est-à-dire le moment où elle aurait coûté une pièce.

    Un réglage IMPOSSIBLE est sauté : ses cotes n'ont pas de sens. Un
    réglage dont l'épaisseur est inconnue l'est aussi — la règle ne dit
    rien tant qu'on ne connaît pas son membre de droite, et c'est
    `nullites.yaml` qui porte ce `se_deduira`.
    """
    fautes = []
    for rid, r in PROC.reglages().items():
        if r.get("valide") is False:
            continue
        ep, ri = r.get("epaisseur"), r.get("rayon_interieur_min")
        if ep is None or ri is None:
            continue
        if abs(ri - 0.5 * ep) > 1e-9:
            fautes.append(
                f"hardware.yaml / {rid} : rayon_interieur_min = {ri} mm, "
                f"or 0,5 x epaisseur = {0.5 * ep} mm (CLAUDE.md). "
                f"Un rayon rentrant trop faible déchire la matière.")
    return fautes


def main() -> int:
    total, fautes = 0, []
    for f in ("origines.yaml", "nullites.yaml"):
        n = sum(len(r) for r in _regles(f).values())
        total += n
        fautes += controler(f) + controler_absorption(f)
    fautes += controler_rayon()
    if fautes:
        print(f"\n✗ RÈGLES DÉFECTUEUSES — {len(fautes)} sur {total} :")
        for x in fautes:
            print(f"   {x}")
        print("\n  Une règle qui ne s'applique jamais est un garde-fou qu'on")
        print("  croit avoir ; un motif qui avale tout rend le vert sans valeur.")
        print("  Corriger, ou assumer explicitement.")
        return 1
    print(f"   règles déclaratives : {total} motifs, tous atteints ; "
          f"rayon minimal conforme sur {len(PROC.reglages())} réglages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
