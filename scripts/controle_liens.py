#!/usr/bin/env python3
"""Liens relatifs morts dans les Markdown suivis par Git — outil de clôture.

    .venv/bin/python scripts/controle_liens.py

Versé dans le dépôt le 2026-10-06 (décision de Jeremy, réponse du jour à la
question de Claude : « OUI, les verser ») : la première version vivait dans le
dossier temporaire de la session, effacé entre deux jours.

Ignorés : `archive/`, les liens web et les ancres seules, le code (blocs et
en ligne : un exemple de lien n'est pas un lien), et la cible « … » d'une
citation élidée. Annonce le nombre de fichiers et de liens vérifiés.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def liens_morts(fichiers: list[tuple[Path, str]], racine: Path = REPO) -> tuple[int, list[str]]:
    """(liens vérifiés, liens morts) pour des couples (chemin relatif, texte)."""
    n, morts = 0, []
    for chemin, txt in fichiers:
        txt = re.sub(r"```.*?```", "", txt, flags=re.S)
        txt = re.sub(r"`[^`\n]*`", "", txt)
        for cible in re.findall(r"\]\(([^)\s]+)\)", txt):
            if re.match(r"^(https?:|mailto:|#)", cible) or cible == "…":
                continue
            n += 1
            c = cible.split("#")[0]
            if c and not ((racine / chemin).parent / c).resolve().exists():
                morts.append(f"{chemin} -> {cible}")
    return n, morts


def fichiers_suivis() -> list[tuple[Path, str]]:
    sortie = subprocess.run(["git", "ls-files", "*.md"], cwd=REPO, capture_output=True, text=True).stdout.split()
    return [(Path(f), (REPO / f).read_text(encoding="utf-8", errors="replace"))
            for f in sortie if not f.startswith("archive/")]


def main() -> int:
    fs = fichiers_suivis()
    if not fs:
        print("   liens : SAUTÉ, aucun fichier suivi (pas de dépôt git ici)")
        return 0
    n, morts = liens_morts(fs)
    print(f"   liens : {len(fs)} fichiers Markdown, {n} liens relatifs vérifiés ; morts : {len(morts)}")
    for m in morts:
        print(f"     ✗ {m}")
    return 1 if morts else 0


if __name__ == "__main__":
    sys.exit(main())
