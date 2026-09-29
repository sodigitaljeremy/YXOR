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


# Fiche 0036 : cinq espèces, six états. Une convention écrite à la main
# diverge — celle des lignes `Date:` l'a fait sur quatre fiches d'affilée.
# Celle-ci est donc REFUSÉE si elle sort de la liste.
ESPECES = ("gouvernante", "historique", "close", "veille", "abandonnee",
           "proposition")
ETATS = ("proposée", "acceptée", "appliquée", "amendée", "abandonnée",
         "archivée", "veille", "instruction")

PARCOURS = [
    ("0010", "le contrat du projet : tout le reste en découle"),
    ("0013", "la règle 1 restreinte à son domaine — lue seule, elle fait "
             "sous-dimensionner les grandes tailles"),
    ("0020", "les trois états de la valeur absente, qui traversent tout"),
    ("0026", "la structure de hardware.yaml en quatre tables"),
    ("0033", "et pourquoi l'épaisseur y est un champ, pas une clé"),
    ("0018", "le site est une projection du dépôt, il ne stocke rien"),
    ("0015", "le seul choix d'architecture MÉCANIQUE — le reste est méthode"),
]


def entete(texte: str) -> dict:
    lignes = texte.split("\n")
    titre = lignes[0].lstrip("# ").strip() if lignes else ""
    def champ(nom):
        m = re.search(rf"^{nom}\s*:\s*(.+)$", texte, re.M | re.I)
        return re.sub(r"\*\*|`", "", m.group(1)).strip() if m else ""
    return dict(titre=titre, statut=champ("Statut"), date=champ("Date"),
                espece=champ("Espèce"), etat=champ("État"),
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
           "## Par où commencer", "",
           "Sept fiches suffisent avant d'écrire une ligne. Les autres se",
           "lisent quand leur question se pose.", ""]
    for num, pourquoi in PARCOURS:
        f = next((x for x in fiches if x.name.startswith(num)), None)
        if f:
            out.append(f"{len(out) and ''}1. [{num}]({f.name}) — {pourquoi}")
    out += ["",
           "| # | Titre | Espèce | État | Date | Amendée par |",
           "| --- | --- | --- | --- | --- | --- |"]
    sans_date, amendees, mauvais = [], [], []
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
        if d["espece"] and d["espece"] not in ESPECES:
            mauvais.append(f"{num} : espèce « {d['espece']} » hors liste")
        if d["etat"] and d["etat"] not in ETATS:
            mauvais.append(f"{num} : état « {d['etat']} » hors liste")
        if not d["espece"]:
            mauvais.append(f"{num} : sans ligne `Espèce:`")
        if d["etat"] == "amendée" and not d["amendee"]:
            mauvais.append(f"{num} : état « amendée » sans `Amendée par`")
        out.append(f"| [{num}]({f.name}) | {titre} | {d['espece'] or '—'} | "
                   f"{d['etat'] or '—'} | {d['date'] or '—'} | {am or ''} |")
    out += ["", f"**{len(fiches)} fiches.** {len(amendees)} amendée(s) par une "
                f"autre : {', '.join(amendees) or 'aucune'}."]
    if sans_date:
        out.append(f"\n⚠ Sans ligne `Date:` : {', '.join(sans_date)}.")
    return "\n".join(out) + "\n", mauvais


def main() -> int:
    # `decisions/` n'est PAS copié dans l'image Docker : le site ne sert
    # aucune fiche. Ce script est une tâche de MAINTENANCE DU DÉPÔT, pas
    # de construction du site — et l'avoir câblé dans `regenerer.py` sans
    # y penser a cassé le déploiement pendant quatre heures.
    #
    # On saute, et ON LE DIT. Un saut muet est le faux vert qu'on vient
    # de corriger six fois.
    if not DEC.is_dir():
        print("   index des fiches IGNORÉ : pas de decisions/ ici "
              "(construction Docker)")
        return 0
    t, mauvais = construire()
    if mauvais:
        print("\n✗ CONVENTION DES FICHES VIOLÉE :")
        for m in mauvais:
            print(f"   {m}")
        print("  Espèces : " + ", ".join(ESPECES))
        print("  États   : " + ", ".join(ETATS))
        return 1
    ancien = CIBLE.read_text(encoding="utf-8") if CIBLE.exists() else ""
    CIBLE.write_text(t, encoding="utf-8")
    n = t.count("\n| [")
    print(f"   index des fiches : {n} entrées"
          + ("" if t == ancien else "  (mis à jour)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
