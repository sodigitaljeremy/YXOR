#!/usr/bin/env python3
"""Régénère TOUT : les pièces, puis le site statique.

    .venv/bin/python scripts/regenerer.py
    .venv/bin/python scripts/regenerer.py --site-seulement

Commande unique. Le Dockerfile n'appelle que celle-ci : ce qui tourne en
production est exactement ce que vous pouvez lancer chez vous.

═══════════════════════════════════════════════════════════════════════
 CE GÉNÉRATEUR NE CRÉE AUCUNE DONNÉE
═══════════════════════════════════════════════════════════════════════

Il lit le dépôt et le projette. Chaque valeur affichée par le site vient
d'un fichier du dépôt ou d'un relevé produit par une pièce. Deux sources
de vérité finiraient par diverger : il n'y en a qu'une.

Conçu pour TRENTE pièces, pas pour une :

  · build123d n'est importé QU'UNE FOIS. Les pièces sont appelées dans le
    même interpréteur, jamais par trente sous-processus. L'import coûte
    quelques secondes ; le payer trente fois serait absurde.
  · La liste est filtrable côté navigateur, sans rechargement.
  · Chaque pièce est indépendante : une qui échoue est signalée et les
    autres sont produites quand même.
"""
from __future__ import annotations

import argparse
import datetime
import html
import importlib.util
import json
import re
import shutil
import sys
import traceback
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from plan_decoupe import ordonner_cotes, svg_schema, polylignes_depuis_face  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
PARTS = REPO / "parts"
WEB = REPO / "web"
SITE = REPO / "site"
EXPORTS = REPO / "exports" / "parts"



# Refonte R4 (2026-10-01) : l'audit de toutes les valeurs, les règles de
# nullité et le contrôle des règles déclaratives sont archivés
# (archive/scripts/). Restent les contrôles qui protègent le robot.
import controle_articulations
import controle_depot
import liens_bruts
import procedes as PROC
import provenance_amont
import pages
from pages import (  # les gabarits vivent dans pages.py (fiche 0024)
    FORMATS, page_piece, page_atelier, page_index, page_etat,
    page_provenance, etat_procede, e, val)




















# ──────────────────────────────────────────────────── exécution des pièces
def executer_pieces() -> list[str]:
    """Exécute chaque parts/*.py dans CE processus. Renvoie les échecs.

    `exports/parts/` est VIDÉ d'abord. Sans cela, un fichier engendré sous
    un nom qui n'existe plus survit et continue de s'ouvrir : le 2026-09-29,
    la migration des procédés a renommé la base de `..._cutter_carton` à
    `..._cutter_cartonplume_5`, et les anciens DXF sont restés là, valides
    en apparence. Un fichier périmé qui s'ouvre est pire qu'un fichier
    absent : rien ne signale qu'il ne correspond plus à rien.
    """
    if EXPORTS.exists():
        n = 0
        for f in EXPORTS.iterdir():
            if f.is_file():
                f.unlink(); n += 1
        if n:
            print(f"  exports/parts/ vidé ({n} fichier(s) de la passe précédente)")
    scripts = sorted(p for p in PARTS.glob("*.py") if not p.name.startswith("_"))
    echecs = []
    if not scripts:
        print("  aucune pièce dans parts/")
        return echecs
    sys.path.insert(0, str(REPO / "scripts"))
    for s in scripts:
        print(f"  · {s.name}", end=" ", flush=True)
        try:
            spec = importlib.util.spec_from_file_location(f"piece_{s.stem}", s)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            code = mod.main([]) if hasattr(mod, "main") else 0
            print("ok" if code == 0 else f"code {code}")
            if code != 0:
                echecs.append(s.name)
        except Exception:
            print("ÉCHEC")
            traceback.print_exc(limit=3)
            echecs.append(s.name)
    return echecs


def lire_releves() -> list[dict]:
    pieces = []
    for f in sorted(PARTS.glob("*.origines.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        p = d.get("piece") or {}
        if not p.get("nom"):
            print(f"  ⚠ {f.name} sans bloc `piece:` — ignoré")
            continue
        p["cotes"] = d.get("cotes") or []
        p["_schema"] = ordonner_cotes(d.get("cotes_schema") or [])
        p["_simulation"] = d.get("simulation")
        p["fichiers"] = {}
        base = p.get("base_fichier", p["nom"])
        for ext, _, _ in FORMATS:
            src = EXPORTS / (f"{base}_planA4.pdf" if ext == "pdf" else f"{base}.{ext}")
            if src.exists():
                p["fichiers"][ext] = src
        pieces.append(p)
    return pieces


# ────────────────────────────────────────────────────────────── gabarits
# Les échecs vivent dans pages.ECHECS : c'est le bandeau qui les lit.
# En garder une copie ici donnerait deux listes et un bandeau muet.


































def lire_provenance() -> dict:
    """{fichier: nombre de valeurs amont}, pour les pages ; le contrôle est plus bas."""
    decl = yaml.safe_load(provenance_amont.DECLARATION.read_text(encoding="utf-8"))
    comptes, _ = provenance_amont.inventaire(decl, REPO / "params", PARTS)
    return comptes


BALISES_VIDES = {"meta", "link", "br", "hr", "img", "input", "source"}


def controler_css() -> list[str]:
    """Une feuille de style cassée ne lève AUCUNE erreur.

    Le navigateur abandonne silencieusement la règle fautive — ou tout ce
    qui suit, selon la faute — et la page s'affiche, simplement fausse.
    Même motif que les six faux verts : un système qui échoue en silence.

    Trois fautes détectées, et ce sont celles qui coupent la suite :

      1. accolades déséquilibrées — un `{` non fermé avale tout le reste ;
      2. profondeur > 1 hors `@media` — une règle imbriquée par accident,
         qui s'équilibre pourtant et passe un simple comptage ;
      3. commentaire non fermé — `/*` sans `*/` mange la fin du fichier.

    Ce contrôle n'est PAS un validateur CSS : il ne juge ni les
    propriétés ni les valeurs. Il vérifie que le fichier est
    STRUCTURELLEMENT analysable jusqu'au bout — c'est-à-dire que la
    dernière règle a autant de chances de s'appliquer que la première.
    """
    f = WEB / "style.css"
    if not f.exists():
        return ["web/style.css est absent"]
    brut = f.read_text(encoding="utf-8")
    if brut.count("/*") != brut.count("*/"):
        return [f"style.css : {brut.count('/*')} commentaires ouverts pour "
                f"{brut.count('*/')} fermés — tout ce qui suit le dernier "
                f"`/*` non fermé est ignoré"]
    sans = re.sub(r"/\*.*?\*/", "", brut, flags=re.S)
    if sans.count("{") != sans.count("}"):
        return [f"style.css : {sans.count('{')} accolades ouvrantes pour "
                f"{sans.count('}')} fermantes"]
    fautes, prof = [], 0
    dans_media = False
    for i, l in enumerate(sans.splitlines(), 1):
        if "@media" in l or "@supports" in l:
            dans_media = True
        for c in l:
            if c == "{":
                prof += 1
            elif c == "}":
                prof -= 1
                if prof < 0:
                    fautes.append(f"style.css ligne {i} : accolade fermante "
                                  f"en trop")
                    prof = 0
                if prof == 0:
                    dans_media = False
        if prof > 1 and not dans_media:
            fautes.append(f"style.css ligne {i} : règle imbriquée dans une "
                          f"autre hors @media — profondeur {prof}")
    if prof != 0:
        fautes.append(f"style.css : {prof} bloc(s) jamais fermé(s) — le "
                      f"reste de la feuille est ignoré par le navigateur")
    return fautes


def controler_html() -> list[str]:
    """Vérifie que les balises se referment, et dans l'ordre.

    Motif : un `div` laissé ouvert fait remonter tout ce qui suit dans le
    conteneur précédent — c'est ainsi que la vue 3D s'est retrouvée
    par-dessus le tableau des origines, sur mobile, le 2026-09-29. Le
    navigateur ne proteste pas : il referme silencieusement et affiche
    une page fausse.

    Ce contrôle ne remplace PAS un écran. Il attrape les fautes de
    STRUCTURE, pas celles de mise en page : une colonne trop large ou un
    texte illisible passeront toujours. C'est la limite de la règle 6,
    et elle est là.
    """
    pages_vues = sorted(SITE.rglob("*.html"))
    if not pages_vues:
        # Un contrôle qui n'a rien à contrôler PASSE, et son message
        # rassure : « balises équilibrées sur toutes les pages » — sur
        # zéro page. C'est le faux vert le plus simple à produire.
        return ["aucune page HTML à contrôler : le site n'a pas été "
                "engendré, ou SITE pointe ailleurs"]
    defauts = []
    for f in pages_vues:
        t = re.sub(r"<(script|style|svg)\b.*?</\1>", "",
                   f.read_text(encoding="utf-8"), flags=re.S)
        pile = []
        for m in re.finditer(r"<(/?)([a-zA-Z][\w-]*)([^>]*)>", t):
            fin, nom, reste = m.group(1), m.group(2).lower(), m.group(3)
            if nom in BALISES_VIDES or reste.rstrip().endswith("/"):
                continue
            if not fin:
                pile.append(nom)
            elif pile and pile[-1] == nom:
                pile.pop()
            else:
                defauts.append(f"{f.relative_to(SITE)} : </{nom}> inattendu")
                break
        else:
            if pile:
                defauts.append(f"{f.relative_to(SITE)} : jamais fermé — "
                               + ", ".join(f"<{b}>" for b in pile))
    return defauts


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--site-seulement", action="store_true",
                    help="ne pas réexécuter les pièces")
    ap.add_argument("--tolerer-echecs", action="store_true",
                    help="publier malgré une pièce en échec ; chaque page portera "
                         "alors un bandeau rouge nommant ce qui manque")
    a = ap.parse_args(argv)

    t0 = datetime.datetime.now()
    echecs = []
    if not a.site_seulement:
        print("1. Régénération des pièces (build123d importé une seule fois)")
        echecs = executer_pieces()
    else:
        print("1. Pièces non réexécutées (--site-seulement)")

    # ── ÉCHEC DUR PAR DÉFAUT, et voici pourquoi ──────────────────────
    # Une construction Docker qui échoue ne met pas le site hors ligne :
    # Coolify laisse tourner le conteneur précédent. Échouer dur ne coûte
    # donc AUCUNE disponibilité — et évite de remplacer un site juste par
    # un site amputé qui se tait. C'est le contraire d'un compromis.
    # `--tolerer-echecs` publie quand même, mais alors chaque page crie
    # ce qui manque : on ne publie jamais une omission silencieuse.
    if echecs and not a.tolerer_echecs:
        print(f"\n✗ ARRÊT : {len(echecs)} pièce(s) en échec — {', '.join(echecs)}")
        print("  Le site n'est PAS reconstruit. Le déploiement précédent reste en ligne.")
        print("  Pour publier malgré tout : --tolerer-echecs (bandeau rouge sur chaque page).")
        return 1
    pages.ECHECS[:] = echecs

    print("\n2. Lecture des relevés")
    pieces = lire_releves()
    print(f"   {len(pieces)} pièce(s)")

    print("\n3. Provenance amont")
    prov = lire_provenance()
    print(f"   {sum(prov.values())} valeurs d'origine ToddlerBot dans {len(prov)} fichiers")

    # contours et procédé : lus une fois, pour le schéma et les voyants
    hw = yaml.safe_load((REPO / "params/hardware.yaml").read_text("utf-8"))
    an = yaml.safe_load((REPO / "params/anthropometry.yaml").read_text("utf-8"))
    jo = yaml.safe_load((REPO / "params/joints.yaml").read_text("utf-8"))
    import build123d as _bd
    for p in pieces:
        p["_procede"] = PROC.reglages(hw).get(p.get("reglage"), {})
        p["besoins_procede"] = p.get("besoins_procede")
        p["_contours"] = []
        st = p["fichiers"].get("step")
        if st:
            try:
                f = _bd.import_step(str(st)).faces().sort_by(_bd.Axis.Z)[0]
                p["_contours"] = polylignes_depuis_face(f)
            except Exception as err:
                print(f"   ⚠ contours illisibles pour {p['nom']} : {err}")

    print("\n4. Construction du site")
    if SITE.exists():
        shutil.rmtree(SITE)
    (SITE / "assets").mkdir(parents=True)
    (SITE / "fichiers").mkdir()
    (SITE / "data").mkdir()
    for f in ("style.css", "viewer.js", "simulateur.js", "zoom.js"):
        shutil.copy2(WEB / f, SITE / "assets" / f)

    for p in pieces:
        for f in p["fichiers"].values():
            shutil.copy2(f, SITE / "fichiers" / f.name)
        for dossier, gab in (("piece", page_piece), ("atelier", page_atelier)):
            d = SITE / dossier / p["nom"]
            d.mkdir(parents=True)
            (d / "index.html").write_text(gab(p), encoding="utf-8")

    (SITE / "index.html").write_text(page_index(pieces, prov), encoding="utf-8")
    (SITE / "etat").mkdir()
    (SITE / "etat" / "index.html").write_text(page_etat(pieces, prov, hw, an, jo),
                                              encoding="utf-8")
    (SITE / "provenance").mkdir()
    (SITE / "provenance" / "index.html").write_text(page_provenance(prov), encoding="utf-8")
    (SITE / "data" / "pieces.json").write_text(json.dumps(
        [{k: (str(v) if isinstance(v, Path) else
              {kk: str(vv) for kk, vv in v.items()} if k == "fichiers" else v)
          for k, v in p.items() if not k.startswith("_")} for p in pieces],
        ensure_ascii=False, indent=2), encoding="utf-8")
    (SITE / "data" / "provenance.json").write_text(json.dumps(prov, ensure_ascii=False, indent=2),
                                                   encoding="utf-8")

    # Règle 4, sur TOUT le dépôt — pas seulement sur les répertoires
    # ignorés. C'est la classe de trou, pas le trou (fiche 0024 §4).
    if controle_depot.main() != 0:
        return 1
    # Index des liens bruts GitHub (LIENS-BRUTS.md, 2026-10-01) : réécrit
    # seulement si la liste des fichiers suivis change.
    if liens_bruts.main() != 0:
        return 1
    # Les trois contrôles qui protègent le robot (refonte R4, 2026-10-01).
    if provenance_amont.main() != 0:
        return 1
    if controle_articulations.main() != 0:
        return 1
    # Rayon intérieur minimal = max(0,5 x épaisseur, limite de machine) :
    # sur chaque réglage, puis sur le plus petit rayon rentrant de chaque pièce.
    rayon = PROC.controler_rayon() + PROC.controler_pieces(pieces)
    if rayon:
        print("\n✗ RAYON INTÉRIEUR MINIMAL :")
        for r_ in rayon:
            print(f"   {r_}")
        return 1
    print(f"   rayon intérieur minimal conforme sur {len(PROC.reglages())} réglages "
          f"et {len(pieces)} pièce(s)")
    # L'index des fiches (index_fiches.py) est archivé depuis la refonte
    # R2 du 2026-10-01 : archive/scripts/index_fiches.py.

    mauvais_css = controler_css()
    if mauvais_css:
        print("\n✗ FEUILLE DE STYLE INANALYSABLE :")
        for m in mauvais_css:
            print(f"   {m}")
        print("  Un CSS cassé ne lève aucune erreur : la page s'affiche,")
        print("  simplement fausse.")
        return 1
    n_regles = len(re.findall(r"\{", re.sub(r"/\*.*?\*/", "",
                   (WEB / "style.css").read_text(encoding="utf-8"), flags=re.S)))
    print(f"   feuille de style : {n_regles} règles, structure analysable")

    mal = controler_html()
    if mal:
        print("\n✗ STRUCTURE HTML INVALIDE :")
        for d in mal:
            print(f"   {d}")
        print("  Une balise non fermée déplace le contenu qui suit.")
        return 1
    print(f"   structure HTML : {len(list(SITE.rglob('*.html')))} pages, "
          "balises équilibrées")

    n_f = sum(1 for _ in SITE.rglob("*") if _.is_file())
    taille = sum(f.stat().st_size for f in SITE.rglob("*") if f.is_file())
    dt = (datetime.datetime.now() - t0).total_seconds()
    print(f"   {n_f} fichiers, {taille/1024:.0f} ko")
    print(f"\nTerminé en {dt:.1f} s.")
    if echecs:
        print(f"⚠ publié MALGRÉ {len(echecs)} échec(s) : {', '.join(echecs)}")
        print("  Chaque page porte un bandeau rouge les nommant.")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
