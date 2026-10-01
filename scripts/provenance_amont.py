#!/usr/bin/env python3
"""Provenance des valeurs d'origine ToddlerBot (amont) : les compter, et le dire.

    .venv/bin/python scripts/provenance_amont.py

Créé le 2026-10-01 (refonte R4). Remplace l'audit de TOUTES les valeurs
(archive/scripts/audit_origines.py) par ce qui touche la licence : la
mécanique amont est sous CC BY-NC-SA 4.0 (fiche 0061), et aucune géométrie
amont n'entre dans une pièce YXOR. La question juridique sur les valeurs
numériques reste ouverte (fiche 0010 § 4) : ce contrôle en tient
l'inventaire, il ne la tranche pas.

Lit params/origines.yaml, réduit aux règles qui concernent l'amont. Pour
chaque fichier déclaré, la PREMIÈRE règle qui correspond à un chemin
l'emporte (les règles `propre` de joints.yaml en exceptent des valeurs).

Échoue si :
  · un fichier déclaré est absent ;
  · une règle `amont` ne correspond plus à aucune valeur (clé renommée :
    la provenance se perdrait en silence) ;
  · le total est nul.
Les cotes des pièces (parts/*.origines.yaml) d'origine `amont` sont
comptées à part : la fiche 0061 n'en admet aucune géométrie.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
DECLARATION = REPO / "params" / "origines.yaml"


def aplatir(noeud, prefixe: str = "") -> list[tuple[str, object]]:
    """Arbre YAML → [(chemin, feuille)] ; un élément de liste à `id` est adressé par son id."""
    out = []
    if isinstance(noeud, dict):
        for k, v in noeud.items():
            out += aplatir(v, f"{prefixe}.{k}" if prefixe else str(k))
    elif isinstance(noeud, list):
        for i, v in enumerate(noeud):
            cle = v.get("id") if isinstance(v, dict) else None
            out += aplatir(v, f"{prefixe}.{cle}" if cle else f"{prefixe}[{i}]")
    else:
        out.append((prefixe, noeud))
    return out


def correspond(motif: str, chemin: str) -> bool:
    """`*` = un segment, `**` = zéro ou plusieurs segments (index de liste ignorés)."""
    chemin = re.sub(r"\[\d+\]", "", chemin)
    rx = re.escape(motif)
    rx = rx.replace(r"\*\*\.", "(?:[^.]+\\.)*").replace(r"\.\*\*", "(?:\\.[^.]+)*")
    rx = rx.replace(r"\*\*", ".*").replace(r"\*", "[^.]+")
    return re.fullmatch(rx, chemin) is not None


def inventaire(declaration: dict, params: Path, parts: Path) -> tuple[dict, list]:
    """Renvoie ({fichier: nombre de valeurs amont}, fautes)."""
    comptes, fautes = {}, []
    for nom, d in (declaration.get("fichiers") or {}).items():
        f = params / nom
        if not f.exists():
            fautes.append(f"params/{nom} : déclaré mais absent")
            continue
        regles = d.get("regles") or []
        touches = [0] * len(regles)
        n = 0
        for chemin, _ in aplatir(yaml.safe_load(f.read_text(encoding="utf-8")) or {}):
            i = next((k for k, r in enumerate(regles) if correspond(r["motif"], chemin)), None)
            if i is None:
                continue
            touches[i] += 1
            n += regles[i].get("origine") == "amont"
        for r, t in zip(regles, touches):
            if r.get("origine") == "amont" and t == 0:
                fautes.append(f"params/{nom} : la règle amont « {r['motif']} » ne correspond plus à rien")
        comptes[f"params/{nom}"] = n
    for f in sorted(parts.glob("*.origines.yaml")):
        cotes = (yaml.safe_load(f.read_text(encoding="utf-8")) or {}).get("cotes") or []
        comptes[f"parts/{f.name}"] = sum(1 for c in cotes if c.get("origine") == "amont")
    if not sum(comptes.values()):
        fautes.append("aucune valeur d'origine amont trouvée : la déclaration ne voit plus rien")
    return comptes, fautes


def main(argv=None) -> int:
    decl = yaml.safe_load(DECLARATION.read_text(encoding="utf-8"))
    comptes, fautes = inventaire(decl, REPO / "params", REPO / "parts")
    total = sum(comptes.values())
    print(f"   provenance amont : {total} valeurs d'origine ToddlerBot dans {len(comptes)} fichiers — "
          + ", ".join(f"{k} {v}" for k, v in comptes.items()))
    if fautes:
        print("\n✗ PROVENANCE AMONT :")
        for f in fautes:
            print(f"   {f}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
