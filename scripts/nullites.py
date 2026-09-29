#!/usr/bin/env python3
"""Pourquoi une valeur est absente — fiche 0020.

Trois états, un seul par défaut. `a_mesurer` est le défaut : un `null`
non déclaré ressort en rouge, comme `non_qualifie` dans l'audit. L'oubli
se voit, il ne se tait pas.

La condition est lue dans `params/nullites.yaml`. Le code n'en connaît
aucune : la fiche 0018 interdit à l'application de créer de la donnée,
et une condition écrite en dur dans le générateur en serait une.
"""
from __future__ import annotations
from pathlib import Path
import yaml

from audit_origines import correspond          # un seul moteur de motifs

REPO = Path(__file__).resolve().parent.parent
A_MESURER, SANS_OBJET, SE_DEDUIRA = "a_mesurer", "sans_objet", "se_deduira"

LIB = {
    A_MESURER:  "non déterminé",
    SANS_OBJET: "sans objet",
    SE_DEDUIRA: "se déduira",
}
CLS = {A_MESURER: "ind", SANS_OBJET: "so", SE_DEDUIRA: "der"}


def charger(chemin: Path | None = None) -> dict[str, list[dict]]:
    p = chemin or (REPO / "params" / "nullites.yaml")
    doc = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return {f: (d or {}).get("regles", [])
            for f, d in (doc.get("fichiers") or {}).items()}


def etat(regles: list[dict], chemin: str, voisines: dict) -> dict:
    """État d'une valeur nulle, et le motif à afficher.

    `voisines` : les clés SŒURS de la valeur, où se résout la condition.
    C'est la limite assumée de la fiche 0020 : une condition ne regarde
    pas plus loin que la fratrie.
    """
    for r in regles:
        if not correspond(r["motif"], chemin):
            continue
        si = r.get("si")
        if si is not None:
            if si["cle"] not in voisines:
                continue                       # condition inapplicable ici
            if voisines[si["cle"]] != si.get("vaut"):
                continue
        return dict(etat=r.get("etat", A_MESURER),
                    parce_que=" ".join((r.get("parce_que") or "").split()))
    return dict(etat=A_MESURER, parce_que="")


if __name__ == "__main__":                     # inventaire, pour vérifier
    import sys
    regles = charger()
    hw = yaml.safe_load((REPO / "params" / "hardware.yaml").read_text("utf-8"))
    total = {}
    for fam in ("procedes", "materiaux", "actionneurs"):
        for nom, d in (hw.get(fam) or {}).items():
            if not isinstance(d, dict):
                continue
            for k, v in d.items():
                if v is not None:
                    continue
                st = etat(regles["hardware.yaml"], f"{fam}.{nom}.{k}", d)
                total.setdefault(st["etat"], []).append(f"{fam}.{nom}.{k}")
    for k in (A_MESURER, SE_DEDUIRA, SANS_OBJET):
        v = total.get(k, [])
        print(f"{LIB[k]:>15} : {len(v):>2}")
        for c in v:
            print(f"{'':>17} {c}")
    sys.exit(0)
