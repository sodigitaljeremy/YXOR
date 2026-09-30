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
    ("0060", "la fabrication : la découpe 2D n'est plus le procédé unique "
             "(remplace la 0015, depuis la 0050)"),
    ("0054", "une fiche acceptée ne se réécrit plus : elle est remplacée"),
]


def entete(texte: str) -> dict:
    lignes = texte.split("\n")
    titre = lignes[0].lstrip("# ").strip() if lignes else ""
    def champ(nom):
        m = re.search(rf"^{nom}\s*:\s*(.+)$", texte, re.M | re.I)
        return re.sub(r"\*\*|`", "", m.group(1)).strip() if m else ""
    # TOUTES les lignes « Amendée par », pas la première seulement : la
    # 0015 en porte deux, et la seconde disparaissait de l'index jusqu'au
    # 2026-09-30 (audit de la nuit, § 8 C4).
    amendee = [re.sub(r"\*\*|`", "", m).strip() for m in
               re.findall(r"^Amendée par\s*:\s*(.+)$", texte, re.M | re.I)]
    # Fiche 0054 : une fiche acceptée ne se réécrit plus, elle est
    # REMPLACÉE. L'ancienne porte « Remplacée par », la nouvelle « Remplace ».
    remplacee = [re.sub(r"\*\*|`", "", m).strip() for m in
                 re.findall(r"^Remplacée par\s*:\s*(.+)$", texte, re.M | re.I)]
    remplace = re.findall(r"\b(\d{4})\b", champ("Remplace"))
    return dict(titre=titre, statut=champ("Statut"), date=champ("Date"),
                espece=champ("Espèce"), etat=champ("État"),
                amende=champ("Amende"), amendee=amendee,
                remplacee=remplacee, remplace=remplace)


def construire() -> str:
    fiches = sorted(f for f in DEC.glob("*.md") if f.name != "index.md")
    out = ["# Index des fiches de décision", "",
           "**Engendré** par `scripts/index_fiches.py` — ne pas éditer à la",
           "main. Le régénérer fait partie de `scripts/regenerer.py`.", "",
           "Une fiche acceptée n'est jamais réécrite (règle 5, fiche 0054) :",
           "elle est *remplacée* par une autre, ou *amendée*, et le renvoi",
           "figure dans son en-tête. Les colonnes « remplacée par » et",
           "« amendée par » sont donc les plus importantes du tableau — ce",
           "sont elles qui disent ce qu'il ne faut plus croire.", "",
           "## Par où commencer", "",
           "Huit fiches suffisent avant d'écrire une ligne. Les autres se",
           "lisent quand leur question se pose.", ""]
    for num, pourquoi in PARCOURS:
        f = next((x for x in fiches if x.name.startswith(num)), None)
        if f:
            out.append(f"{len(out) and ''}1. [{num}]({f.name}) — {pourquoi}")
    out += ["",
           "| # | Titre | Espèce | État | Date | Remplacée par | Amendée par |",
           "| --- | --- | --- | --- | --- | --- | --- |"]
    sans_date, amendees, remplacees, mauvais = [], [], [], []
    entetes = {f.name[:4]: entete(f.read_text(encoding="utf-8")) for f in fiches}
    # Réciprocité (fiche 0054) : « Remplace : NNNN » exige que NNNN dise
    # « Remplacée par » cette fiche, et inversement. Sinon : REFUS.
    for num, d in entetes.items():
        for cible in d["remplace"]:
            en_face = entetes.get(cible)
            if en_face is None:
                mauvais.append(f"{num} : « Remplace {cible} », fiche {cible} introuvable")
            elif not any(r.startswith(num) for r in en_face["remplacee"]):
                mauvais.append(f"{num} : « Remplace {cible} », mais {cible} ne dit pas « Remplacée par {num} »")
        for r in d["remplacee"]:
            src = r[:4]
            if src in entetes and num not in entetes[src]["remplace"]:
                mauvais.append(f"{num} : « Remplacée par {src} », mais {src} ne dit pas « Remplace {num} »")
    for f in fiches:
        d = entetes[f.name[:4]]
        num = f.name[:4]
        titre = d["titre"]
        titre = titre[len(num):].lstrip(" —-") if titre.startswith(num) else titre
        if not d["date"]:
            sans_date.append(num)
        am = ""
        if d["amendee"]:
            amendees.append(num)
            morceaux = []
            for x in d["amendee"]:
                x = re.sub(r"^(\d{4})[^ ]*\.md\s*—?\s*", r"**\1** — ", x)
                morceaux.append(x[:88] + ("…" if len(x) > 88 else ""))
            am = "<br>".join(morceaux)
        rp = ""
        if d["remplacee"]:
            remplacees.append(num)
            rp = "<br>".join(
                (lambda x: x[:88] + ("…" if len(x) > 88 else ""))(re.sub(r"^(\d{4})[^ ]*\.md\s*—?\s*", r"**\1** — ", x))
                for x in d["remplacee"])
        if d["espece"] and d["espece"] not in ESPECES:
            mauvais.append(f"{num} : espèce « {d['espece']} » hors liste")
        if d["etat"] and d["etat"] not in ETATS:
            mauvais.append(f"{num} : état « {d['etat']} » hors liste")
        if not d["espece"]:
            mauvais.append(f"{num} : sans ligne `Espèce:`")
        if d["etat"] == "amendée" and not d["amendee"]:
            mauvais.append(f"{num} : état « amendée » sans `Amendée par`")
        etat = d['etat'] or '—'
        if d["remplacee"]:
            etat = f"**remplacée** (était : {etat})"
        out.append(f"| [{num}]({f.name}) | {titre} | {d['espece'] or '—'} | "
                   f"{etat} | {d['date'] or '—'} | {rp} | {am or ''} |")
    out += ["", f"**{len(fiches)} fiches.** {len(remplacees)} remplacée(s) : "
                f"{', '.join(remplacees) or 'aucune'}. {len(amendees)} amendée(s) par une "
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
