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



# Fiche 0020 : un `null` a trois sens, pas un. La condition qui les
# distingue est LUE dans params/nullites.yaml, jamais écrite ici.
import controle_depot
import controle_regles
import index_fiches
import nullites as NU
import procedes as PROC
import pages
from pages import (  # les gabarits vivent dans pages.py (fiche 0024)
    FORMATS, page_piece, page_atelier, page_index, page_etat,
    page_tracabilite, etat_procede, e, val)




















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


































def lancer_audit() -> dict:
    sys.path.insert(0, str(REPO / "scripts"))
    import audit_origines as A
    cotes = []
    for s in A.SOURCES:
        if s.disponible():
            cotes += s.cotes()
    o, n = {}, {}
    for c in cotes:
        k = c.get("origine") or "non_qualifie"
        o[k] = o.get(k, 0) + 1
        k2 = c.get("nature") or "non déclarée"
        n[k2] = n.get(k2, 0) + 1
    return {"total": len(cotes), "origines": o, "natures": n}


BALISES_VIDES = {"meta", "link", "br", "hr", "img", "input", "source"}


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

    print("\n3. Audit d'origine")
    audit = lancer_audit()
    print(f"   {audit['total']} valeurs — " +
          ", ".join(f"{k} {v}" for k, v in sorted(audit["origines"].items(), key=lambda x: -x[1])))

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

    (SITE / "index.html").write_text(page_index(pieces, audit), encoding="utf-8")
    (SITE / "etat").mkdir()
    (SITE / "etat" / "index.html").write_text(page_etat(pieces, audit, hw, an, jo),
                                              encoding="utf-8")
    (SITE / "tracabilite").mkdir()
    (SITE / "tracabilite" / "index.html").write_text(page_tracabilite(audit), encoding="utf-8")
    (SITE / "data" / "pieces.json").write_text(json.dumps(
        [{k: (str(v) if isinstance(v, Path) else
              {kk: str(vv) for kk, vv in v.items()} if k == "fichiers" else v)
          for k, v in p.items() if not k.startswith("_")} for p in pieces],
        ensure_ascii=False, indent=2), encoding="utf-8")
    (SITE / "data" / "audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2),
                                              encoding="utf-8")

    # Règle 4, sur TOUT le dépôt — pas seulement sur les répertoires
    # ignorés. C'est la classe de trou, pas le trou (fiche 0024 §4).
    if controle_depot.main() != 0:
        return 1
    # Ne lit que params/, qui EST copié dans l'image : ce contrôle vaut
    # aussi en construction Docker, contrairement aux deux voisins.
    if controle_regles.main() != 0:
        return 1
    index_fiches.main()

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
