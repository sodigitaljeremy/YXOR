#!/usr/bin/env python3
"""Lecture des sources documentaires — un registre, pas un moteur de recherche.

    .venv/bin/python scripts/source.py --liste
    .venv/bin/python scripts/source.py --cite forget2018 "température"
    .venv/bin/python scripts/source.py --lire forget2018 108-112

═══════════════════════════════════════════════════════════════════════
 CE QUE CET OUTIL N'EST PAS
═══════════════════════════════════════════════════════════════════════

Ce n'est pas un index vectoriel, et c'est délibéré. Huit documents ne
sont pas un problème de recherche.

Un fragment sémantique **ne cite pas une page**, et il ne dit pas ce
qu'il a omis. Le chapitre 5 de `forget2018` a été lu en entier ; c'est
cette lecture continue qui a permis de corriger une distinction — trois
régions de fonctionnement, pas quatre — qu'un découpage en morceaux
aurait détruite : les deux étiquettes surnuméraires désignaient des
MODES d'exploitation, ce qui ne se voit que dans le paragraphe suivant.

`--cite` sert à trouver OÙ lire. C'est `--lire` qui lit.

═══════════════════════════════════════════════════════════════════════
 L'EMPREINTE EST VÉRIFIÉE AVANT TOUTE LECTURE
═══════════════════════════════════════════════════════════════════════

Une citation « p. 97 » ne vaut que pour l'exemplaire lu. Deux tirages
n'ont pas la même pagination, un PDF recompressé non plus — il y a
d'ailleurs un dossier `pdf24_compressed` à côté des originaux, avec les
mêmes titres et d'autres empreintes.

Si l'empreinte a changé, cet outil REFUSE de lire et le dit. Il ne lit
pas « quand même en avertissant » : un avertissement se survole, et la
citation partirait dans une fiche.

═══════════════════════════════════════════════════════════════════════
 CONFIDENTIALITÉ
═══════════════════════════════════════════════════════════════════════

Les exemplaires vivent dans un dossier qui contient aussi des documents
personnels sans rapport avec le projet. **On n'explore jamais ce
dossier.** Cet outil n'ouvre que les chemins nommés dans
`sources.local.yaml` — il ne liste rien, ne cherche aucun fichier, et
n'accepte aucun chemin en argument.

Le numéro de page est celui du PDF, obtenu page par page. `pdftotext`
séparerait les pages par `\\f` et il faudrait les compter ; pypdf les
donne directement, ce qui supprime une source d'erreur de décalage.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
REGISTRE = REPO / "params" / "sources.yaml"
CHEMINS = REPO / "sources.local.yaml"


class SourceRefusee(RuntimeError):
    """Levée plutôt que d'avertir : un avertissement se survole."""


def registre() -> dict:
    return (yaml.safe_load(REGISTRE.read_text(encoding="utf-8")) or {}).get("sources", {})


def chemins() -> dict:
    if not CHEMINS.exists():
        return {}
    return (yaml.safe_load(CHEMINS.read_text(encoding="utf-8")) or {}).get("chemins", {})


def empreinte(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return "sha256:" + h.hexdigest()


def ouvrir(sid: str):
    """Rend (fiche_du_registre, PdfReader) — ou lève, en disant pourquoi."""
    reg, ch = registre(), chemins()
    if sid not in reg:
        raise SourceRefusee(
            f"source « {sid} » inconnue du registre. "
            f"Connues : {', '.join(sorted(reg))}")
    if sid not in ch:
        raise SourceRefusee(
            f"source « {sid} » sans chemin local. L'ajouter à "
            f"{CHEMINS.name}, qui n'est pas versionné.")
    p = Path(ch[sid])
    if not p.exists():
        raise SourceRefusee(f"exemplaire introuvable : {p}")
    attendue = reg[sid].get("empreinte")
    obtenue = empreinte(p)
    if attendue != obtenue:
        raise SourceRefusee(
            f"EMPREINTE DIFFÉRENTE pour « {sid} ».\n"
            f"       registre : {attendue}\n"
            f"       fichier  : {obtenue}\n"
            f"  Ce n'est pas l'exemplaire lu. Une citation de page ne vaudrait\n"
            f"  rien : la pagination peut différer d'un tirage à l'autre.\n"
            f"  Soit remettre le bon fichier, soit relire et mettre à jour le\n"
            f"  registre — y compris l'état de lecture.")
    from pypdf import PdfReader
    return reg[sid], PdfReader(str(p))


def _texte(page) -> str:
    return re.sub(r"[ \t]+", " ", page.extract_text() or "")


def cmd_liste() -> int:
    reg, ch = registre(), chemins()
    etats = {"lu": "LU", "partiel": "partiel", "non_lu": "non lu"}
    print(f"\n  {len(reg)} sources au registre\n")
    print(f"  {'identifiant':<20} {'état':<9} {'p.':>5}  titre")
    print("  " + "─" * 76)
    for sid, d in reg.items():
        dispo = "" if sid in ch and Path(ch[sid]).exists() else "  ⚠ exemplaire absent"
        print(f"  {sid:<20} {etats.get(d.get('lecture'), '?'):<9} "
              f"{d.get('pages') or '?':>5}  {(d.get('titre') or '')[:44]}{dispo}")
        if d.get("lu"):
            print(f"  {'':<20} {'':<9} {'':>5}  lu : {d['lu']}")
    print("\n  Un `non lu` est une information, pas un oubli : aucune")
    print("  affirmation du dépôt ne peut s'en réclamer.")
    n = sum(1 for s in reg if s not in ch or not Path(ch[s]).exists())
    if n:
        print(f"\n  ⚠ {n} exemplaire(s) absent(s) : compléter {CHEMINS.name}.")
    return 0


def cmd_cite(sid: str, motif: str, avant: int = 0, apres: int = 0) -> int:
    d, pdf = ouvrir(sid)
    rx = re.compile(motif, re.I)
    trouves = 0
    print(f"\n  {d['auteurs']}, « {d['titre'] } », {d['editeur']}"
          + (f", {d['annee']}" if d.get("annee") else ""))
    print(f"  motif : {motif}\n")
    for i, page in enumerate(pdf.pages):
        lignes = _texte(page).split("\n")
        for j, l in enumerate(lignes):
            if not rx.search(l):
                continue
            trouves += 1
            print(f"  ── p. {i + 1}")
            for k in range(max(0, j - avant), min(len(lignes), j + apres + 1)):
                marque = ">" if k == j else " "
                print(f"   {marque} {lignes[k].strip()}")
    if not trouves:
        print("  aucun passage.")
        return 1
    print(f"\n  {trouves} passage(s). Le numéro de page est celui du PDF.")
    print(f"  Pour lire autour : --lire {sid} <page>-<page>")
    return 0


def cmd_lire(sid: str, intervalle: str) -> int:
    d, pdf = ouvrir(sid)
    m = re.fullmatch(r"(\d+)(?:-(\d+))?", intervalle)
    if not m:
        raise SourceRefusee("intervalle attendu : `108` ou `108-112`")
    a = int(m.group(1))
    b = int(m.group(2) or a)
    if not (1 <= a <= b <= len(pdf.pages)):
        raise SourceRefusee(f"hors bornes : le document a {len(pdf.pages)} pages")
    # En-tête directement recopiable dans une fiche.
    print(f"\n> {d['auteurs']}, *{d['titre']}*, {d['editeur']}"
          + (f", {d['annee']}" if d.get("annee") else "")
          + f", p. {a}" + (f"-{b}" if b != a else "") + " (pagination PDF).")
    print(f"> Empreinte vérifiée : {d['empreinte'][:23]}…")
    print(f"> Droits : {' '.join((d.get('droits') or '').split())[:88]}\n")
    for i in range(a - 1, b):
        print(f"───────────────────────────── p. {i + 1} ─────")
        print(re.sub(r"\n{3,}", "\n\n", _texte(pdf.pages[i])))
    print("\n  ⚠ Ce texte est SOUS DROITS pour la plupart des sources.")
    print("  Une fiche en tire une VALEUR et une RÉFÉRENCE, jamais le texte.")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--liste", action="store_true")
    ap.add_argument("--cite", nargs=2, metavar=("ID", "MOTIF"))
    ap.add_argument("--lire", nargs=2, metavar=("ID", "PAGES"))
    ap.add_argument("--avant", type=int, default=0, help="lignes de contexte avant")
    ap.add_argument("--apres", type=int, default=2, help="lignes de contexte après")
    a = ap.parse_args(argv)
    try:
        if a.liste:
            return cmd_liste()
        if a.cite:
            return cmd_cite(a.cite[0], a.cite[1], a.avant, a.apres)
        if a.lire:
            return cmd_lire(a.lire[0], a.lire[1])
    except SourceRefusee as err:
        print(f"\n✗ {err}\n")
        return 1
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
