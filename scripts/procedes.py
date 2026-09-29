#!/usr/bin/env python3
"""Chargeur des quatre tables de `hardware.yaml` — fiches 0026 et 0033.

    .venv/bin/python scripts/procedes.py          # inventaire

═══════════════════════════════════════════════════════════════════════
 POURQUOI UN CHARGEUR PLUTÔT QUE DES ACCÈS DIRECTS
═══════════════════════════════════════════════════════════════════════

Un réglage référence une machine, un procédé et une matière ; la matière
référence à son tour un matériau. Quatre tables, trois jointures.

Faite dans chaque pièce, cette jointure serait écrite autant de fois
qu'il y a de pièces — et divergerait. Faite ici, elle est écrite une
fois, et **elle échoue bruyamment** : une référence cassée lève au
chargement, elle ne rend pas un `None` qui se propagerait en silence
jusqu'à une cote fausse.

C'est le troisième point de la fiche 0033 : « écrire le chargeur avant la
donnée ; une jointure faite deux fois est une divergence en attente ».
"""
from __future__ import annotations
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
HARDWARE = REPO / "params" / "hardware.yaml"


# Cotes qui appartiennent à la MATIÈRE, non au réglage. Le chargeur les
# met à plat pour la commodité, mais un relevé doit citer leur vraie
# provenance : deux réglages sur la même tôle ne portent pas deux
# épaisseurs indépendantes.
CLES_MATIERE = ("epaisseur", "epaisseur_mesuree", "masse_surfacique")


class ReglageInconnu(KeyError):
    """Levée plutôt que de rendre None : un None se propage, pas une erreur."""


def charger(chemin: Path | None = None) -> dict:
    return yaml.safe_load((chemin or HARDWARE).read_text(encoding="utf-8")) or {}


def _exige(table: dict, cle, nom_table: str, contexte: str):
    if cle not in table:
        raise ReglageInconnu(
            f"{contexte} référence {nom_table}.{cle}, qui n'existe pas. "
            f"Connues : {', '.join(sorted(map(str, table)))}")
    return table[cle]


def reglages(hw: dict | None = None) -> dict[str, dict]:
    """Les réglages RÉSOLUS, indexés par leur `id`.

    Chaque entrée porte, à plat, ce dont une pièce a besoin : la machine
    et son lieu, le procédé et son rang DIN, la matière, son matériau et
    son épaisseur. La pièce n'a plus aucune jointure à faire.
    """
    hw = hw if hw is not None else charger()
    machines = hw.get("machines") or {}
    procedes = hw.get("procedes") or {}
    matieres = hw.get("matieres") or {}
    materiaux = hw.get("materiaux") or {}

    out: dict[str, dict] = {}
    for r in hw.get("reglages") or []:
        rid = r.get("id")
        if not rid:
            raise ReglageInconnu("un réglage de hardware.yaml n'a pas d'`id`. "
                                 "L'id est écrit à la main, jamais déduit "
                                 "d'une position (fiche 0026).")
        if rid in out:
            raise ReglageInconnu(f"deux réglages portent l'id « {rid} »")
        ctx = f"reglages.{rid}"
        ma = _exige(machines, r["machine"], "machines", ctx)
        pr = _exige(procedes, r["procede"], "procedes", ctx)
        mt = _exige(matieres, r["matiere"], "matieres", ctx)
        mx = _exige(materiaux, mt["materiau"], "materiaux",
                    f"matieres.{r['matiere']}")

        d = dict(r)
        d.update(
            machine_nom=ma.get("nom"),
            lieu=ma.get("lieu"),
            pilotage=ma.get("pilotage"),
            procede_din=pr.get("din"),
            procede_nom=pr.get("nom_fr"),
            enleve_matiere=pr.get("enleve_matiere"),
            materiau=mt.get("materiau"),
            forme=mt.get("forme"),
            epaisseur=mt.get("epaisseur"),
            epaisseur_mesuree=mt.get("epaisseur_mesuree"),
            masse_surfacique=mt.get("masse_surfacique"),
            anisotrope=bool(mx.get("anisotrope")),
        )
        out[rid] = d
    return out


def reglage(rid: str, hw: dict | None = None) -> dict:
    tous = reglages(hw)
    if rid not in tous:
        raise ReglageInconnu(
            f"réglage « {rid} » inconnu. Connus : {', '.join(sorted(tous))}")
    d = tous[rid]
    if d.get("valide") is False:
        raise ReglageInconnu(
            f"réglage « {rid} » déclaré IMPOSSIBLE : "
            + " ".join((d.get("motif") or "sans motif").split()))
    return d


def defaut(hw: dict | None = None) -> str:
    hw = hw if hw is not None else charger()
    return hw.get("reglage_defaut") or ""


def main() -> int:
    hw = charger()
    tous = reglages(hw)
    print(f"  {len(hw.get('machines') or {})} machines · "
          f"{len(hw.get('procedes') or {})} procédés · "
          f"{len(hw.get('matieres') or {})} matières · "
          f"{len(tous)} réglages")
    print(f"  défaut : {defaut(hw)}\n")
    for rid, d in tous.items():
        etat = "possible" if d.get("valide") else "IMPOSSIBLE"
        print(f"  {rid:<24} {etat:<11} {d['machine_nom'] or '?':<22} "
              f"DIN {d['procede_din']}  {d['materiau']} "
              f"{d['forme']} {d['epaisseur'] if d['epaisseur'] is not None else '?'}")
        if not d.get("valide"):
            print(f"{'':>26} -> {' '.join((d.get('motif') or '').split())[:72]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
