#!/usr/bin/env python3
"""Index des fiches de décision — ENGENDRÉ, jamais saisi.

    .venv/bin/python scripts/index_fiches.py

23 fiches, sept renvois d'amendement croisés, et rien qui donnait la
carte : on ne savait pas, en parcourant `decisions/`, laquelle avait été
infirmée par une autre. Le titre de la 0016 affirmait même l'inverse de
ce que la fiche disait d'elle-même.

L'index est engendré depuis les en-têtes, donc il ne peut pas vieillir
séparément. Le régénérer fait partie de `regenerer.py`.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEC = REPO / "decisions"
CIBLE = DEC / "index.md"


def entete(texte: str) -> dict:
    lignes = texte.split("\n")
    titre = lignes[0].lstrip("# ").strip() if lignes else ""
    def champ(nom):
        m = re.search(rf"^{nom}\s*:\s*(.+)$", texte, re.M | re.I)
        return re.sub(r"\*\*|`", "", m.group(1)).strip() if m else ""
    return dict(titre=titre, statut=champ("Statut"), date=champ("Date"),
                amende=champ("Amende"), amendee=champ("Amendée par"))


def construire() -> str:
    fiches = sorted(f for f in DEC.glob("*.md") if f.name != "index.md")
    out = ["# Index des fiches de décision", "",
           "**Engendré** par `scripts/index_fiches.py` — ne pas éditer à la",
           "main. Le régénérer fait partie de `scripts/regenerer.py`.", "",
           "Une fiche n'est jamais réécrite (règle 5) : elle est *amendée*",
           "par une autre, et le renvoi figure dans son en-tête. La colonne",
           "« amendée par » est donc la plus importante du tableau — c'est",
           "elle qui dit ce qu'il ne faut plus croire.", "",
           "| # | Titre | Statut | Date | Amendée par |",
           "| --- | --- | --- | --- | --- |"]
    sans_date, amendees = [], []
    for f in fiches:
        d = entete(f.read_text(encoding="utf-8"))
        num = f.name[:4]
        titre = d["titre"]
        titre = titre[len(num):].lstrip(" —-") if titre.startswith(num) else titre
        if not d["date"]:
            sans_date.append(num)
        am = d["amendee"]
        if am:
            amendees.append(num)
            am = re.sub(r"^(\d{4})[^ ]*\.md\s*—?\s*", r"**\1** — ", am)
            am = am[:88] + ("…" if len(am) > 88 else "")
        out.append(f"| [{num}]({f.name}) | {titre} | {d['statut'][:34]} | "
                   f"{d['date'] or '—'} | {am or ''} |")
    out += ["", f"**{len(fiches)} fiches.** {len(amendees)} amendée(s) par une "
                f"autre : {', '.join(amendees) or 'aucune'}."]
    if sans_date:
        out.append(f"\n⚠ Sans ligne `Date:` : {', '.join(sans_date)}.")
    return "\n".join(out) + "\n"


def main() -> int:
    t = construire()
    ancien = CIBLE.read_text(encoding="utf-8") if CIBLE.exists() else ""
    CIBLE.write_text(t, encoding="utf-8")
    n = t.count("\n| [")
    print(f"   index des fiches : {n} entrées"
          + ("" if t == ancien else "  (mis à jour)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
