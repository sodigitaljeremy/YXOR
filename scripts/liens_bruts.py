#!/usr/bin/env python3
"""Index des liens bruts GitHub de chaque fichier suivi : LIENS-BRUTS.md.

    .venv/bin/python scripts/liens_bruts.py

Créé le 2026-10-01. Une ligne par fichier suivi par Git (`git ls-files`),
au format https://raw.githubusercontent.com/sodigitaljeremy/YXOR/main/<chemin>,
groupée par dossier, journal/ et archive/ compris. Sert à donner d'un coup
tout le dépôt à lire à un assistant extérieur.

Le fichier n'est RÉÉCRIT que si la liste des fichiers change. Un fichier
qui porterait le commit courant changerait à chaque commit, et le dépôt ne
serait jamais propre après une régénération. L'en-tête donne donc le commit
et la date de la dernière génération, c'est-à-dire de la dernière fois où
la liste a changé ; les liens visent `main`, donc l'état courant.

Sans dépôt git (construction Docker), le script le DIT et ne fait rien.
"""
from __future__ import annotations

import datetime
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CIBLE = REPO / "LIENS-BRUTS.md"
BASE = "https://raw.githubusercontent.com/sodigitaljeremy/YXOR/main/"


def suivis() -> list[str]:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=REPO, capture_output=True, text=True, check=True)
    return sorted(f for f in out.stdout.split("\0") if f)


def corps(fichiers: list[str]) -> str:
    """Les liens, groupés par dossier (premier niveau ; « racine » pour les fichiers du haut)."""
    groupes: dict[str, list[str]] = {}
    for f in fichiers:
        d = f.split("/", 1)[0] + "/" if "/" in f else "racine"
        groupes.setdefault(d, []).append(f)
    ordre = ["racine"] + sorted(k for k in groupes if k != "racine")
    L = []
    for d in ordre:
        if d not in groupes:
            continue
        L.append(f"\n## {d} ({len(groupes[d])})\n")
        L.extend(BASE + f for f in groupes[d])
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    if not (REPO / ".git").exists():
        print("   liens bruts IGNORÉS : pas de dépôt git ici (construction Docker)")
        return 0
    fichiers = suivis()
    if not fichiers:
        print("   ✗ liens bruts : aucun fichier suivi")
        return 1
    nouveau = corps(fichiers)
    ancien = CIBLE.read_text(encoding="utf-8") if CIBLE.exists() else ""
    if ancien.split("\n---\n", 1)[-1] == nouveau:
        print(f"   liens bruts : {len(fichiers)} fichiers, LIENS-BRUTS.md à jour")
        return 0
    sha = subprocess.run(["git", "rev-parse", "--short=12", "HEAD"], cwd=REPO,
                         capture_output=True, text=True).stdout.strip() or "inconnu"
    tete = (f"# Liens bruts du dépôt YXOR\n\n"
            f"Engendré par `scripts/liens_bruts.py` (appelé par `scripts/regenerer.py`).\n"
            f"Liste établie au commit `{sha}`, le {datetime.date.today().isoformat()} ; "
            f"{len(fichiers)} fichiers suivis. Les liens visent `main`, donc l'état courant.\n")
    CIBLE.write_text(tete + "\n---\n" + nouveau, encoding="utf-8")
    print(f"   liens bruts : {len(fichiers)} fichiers, LIENS-BRUTS.md réécrit (la liste a changé)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
