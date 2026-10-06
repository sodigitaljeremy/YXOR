#!/usr/bin/env python3
"""Affirmations périmées encore présentes dans les fichiers VIVANTS — outil de clôture.

    .venv/bin/python scripts/controle_contradictions.py

Versé dans le dépôt le 2026-10-06 (décision de Jeremy, réponse du jour à la
question de Claude : « OUI, les verser »). La version de session (10 motifs)
a été perdue avec le dossier temporaire ; ces motifs sont RECONSTRUITS depuis
les corrections consignées dans les fiches et le journal, chacun avec sa
source.

Fichiers vivants : suivis par Git, hors `archive/`, `journal/`, `decisions/`
(une fiche ne se réécrit pas), `docs/sources/` (rapports versés tels quels),
les instantanés datés (`*-AAAA-MM-JJ*`, `*-AAAA-MM*`), `LIENS-BRUTS.md` et ce
script. Une ligne qui CITE l'ancien texte (barré, « était », « corrigé »,
« remplacé », « ancien », « fausse ») est écartée, et comptée.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# (motif, ce qui est périmé, source de la correction)
MOTIFS = [
    # la licence amont citée AVEC sa version mais sans SA ; « CC BY-NC » seul désigne une famille de licences
    (r"CC BY-NC(?!-SA)\s*4\.0", "licence amont citée sans la clause SA", "CLAUDE.md, corrigé le 2026-09-30"),
    (r"[Pp]rocédé unique\s*:?\s*la découpe 2D", "la découpe 2D n'est plus le procédé unique", "fiches 0050 et 0060"),
    (r"[Cc]oncevoir au plus contraignant", "le carton n'est plus le cas de conception", "fiche 0060"),
    (r"RS00 sur les 12 articulations", "répartition remplacée par les jambes mixtes", "fiche 0067, qui remplace la 0065"),
    (r"fixation du boîtier du RS00[^.]*face arrière", "la fixation du boîtier du RS00 est à l'AVANT", "STEP officiel, journal du 2026-10-03"),
    (r"(LeRobot Humanoid[^.]*n'existe pas|aucun humanoïde LeRobot)", "le LeRobot Humanoid existe", "journal du 2026-10-06"),
    (r"[Ii]l y a une imprimante 3D", "aucune imprimante 3D vérifiée", "fiche 0059"),
    (r"pytest -", "les tests tournent sous unittest", "CLAUDE.md, Environnement"),
    (r"ankle_roll\s*:\s*rs00", "pas de roulis de cheville pour S", "fiche 0068"),
    (r"S\s*:\s*12 degrés de liberté|6 axes par jambe pour S", "S a 5 axes par jambe", "fiche 0068"),
]
CITATION = re.compile(r"~~|\bétait\b|[Cc]orrigé|[Rr]emplac|\bancien|\bfausse?\b|[Pp]érimé|disait")
EXCLUS = ("archive/", "journal/", "decisions/", "docs/sources/", "LIENS-BRUTS.md", "scripts/controle_contradictions.py",
          "tests/test_controles_cloture.py")
DATE = re.compile(r"-20\d\d-\d\d")


def chercher(fichiers: list[tuple[str, str]]) -> tuple[list[str], list[str]]:
    """(contradictions, citations écartées) pour des couples (chemin, texte)."""
    trouvees, citees = [], []
    for chemin, txt in fichiers:
        for k, ligne in enumerate(txt.splitlines(), 1):
            for motif, quoi, src in MOTIFS:
                if re.search(motif, ligne):
                    (citees if CITATION.search(ligne) else trouvees).append(f"{chemin}:{k} — {quoi} ({src})")
    return trouvees, citees


def vivants() -> list[tuple[str, str]]:
    sortie = subprocess.run(["git", "ls-files"], cwd=REPO, capture_output=True, text=True).stdout.split()
    out = []
    for f in sortie:
        if f.startswith(EXCLUS) or DATE.search(f) or not f.endswith((".md", ".yaml", ".py", ".txt")):
            continue
        out.append((f, (REPO / f).read_text(encoding="utf-8", errors="replace")))
    return out


def main() -> int:
    fs = vivants()
    if not fs:
        print("   contradictions : SAUTÉ, aucun fichier suivi (pas de dépôt git ici)")
        return 0
    trouvees, citees = chercher(fs)
    print(f"   contradictions : {len(MOTIFS)} motifs cherchés dans {len(fs)} fichiers vivants ; "
          f"{len(trouvees)} trouvées ; {len(citees)} citations de l'ancien texte écartées")
    for t in trouvees:
        print(f"     ✗ {t}")
    return 1 if trouvees else 0


if __name__ == "__main__":
    sys.exit(main())
