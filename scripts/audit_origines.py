#!/usr/bin/env python3
"""Répond à une seule question : quelles cotes viennent de ToddlerBot ?

    .venv/bin/python scripts/audit_origines.py            # rapport lisible
    .venv/bin/python scripts/audit_origines.py --amont    # seulement l'amont
    .venv/bin/python scripts/audit_origines.py --strict   # échoue si non qualifié
    .venv/bin/python scripts/audit_origines.py --json     # sortie machine

Se lance avec le venv DU PROJET. Ne lit que des fichiers.

Voir decisions/0010-origine-des-cotes.md.

⚠ CE SCRIPT NE REND AUCUN AVIS JURIDIQUE. Il produit un inventaire de ce
  qui vient de l'amont. Ce qu'il faut en conclure n'est pas de son
  ressort — ni du mien.

═══════════════════════════════════════════════════════════════════════
 CONÇU POUR COUVRIR parts/ DEMAIN
═══════════════════════════════════════════════════════════════════════

L'audit interroge des SOURCES, chacune sachant énumérer ses cotes sous
la forme (chemin, valeur, origine, source, note). Aujourd'hui une seule
source est branchée — les YAML de `params/`. Demain, `parts/` s'ajoutera
sans toucher au reste : il suffira d'implémenter une nouvelle classe et
de l'inscrire dans SOURCES.

Deux collecteurs sont déjà écrits pour `parts/` et restent inertes tant
que le dossier est vide :

  RelevesPieces  lit les `parts/<nom>.origines.yaml` déposés par chaque
                 pièce (contrat fixé par la fiche 0010 §5).
  LitterauxPieces repère les littéraux numériques nus dans `parts/**/*.py`
                 — une cote écrite en dur viole la règle 1 ET n'a aucune
                 origine. Signalés `non_qualifie`.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PARAMS = REPO / "params"
PARTS = REPO / "parts"
DECLARATION = PARAMS / "origines.yaml"

ORIGINES = ("propre", "catalogue", "litterature", "amont", "mesure", "ambigu")
NATURES = ("echelle", "tenue", "interface", "procede")   # fiche 0013
NON_QUALIFIE = "non_qualifie"


# ────────────────────────────────────────────────────────────── lecture
# Un premier jet utilisait un lecteur YAML maison. Il perdait
# l'imbrication des listes et découpait mal les blocs `>` multilignes :
# des cotes amont ressortaient `non_qualifie` sans que rien ne le
# signale. Exactement le faux silencieux que ce projet traque. PyYAML
# est donc une dépendance assumée (MIT).

import yaml


def aplatir(noeud, prefixe: str = "") -> list[tuple[str, object]]:
    """Aplatit un arbre YAML en [(chemin.de.cle, valeur_feuille)].

    Les éléments de liste reçoivent un index : `jambes[0].articulation.axe`.
    """
    out: list[tuple[str, object]] = []
    if isinstance(noeud, dict):
        for k, v in noeud.items():
            out += aplatir(v, f"{prefixe}.{k}" if prefixe else str(k))
    elif isinstance(noeud, list):
        for i, v in enumerate(noeud):
            out += aplatir(v, f"{prefixe}[{i}]")
    else:
        out.append((prefixe, noeud))
    return out


def lire_yaml_plat(path: Path) -> list[tuple[str, object]]:
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    return aplatir(doc) if doc is not None else []


def lire_declaration(path: Path) -> dict[str, list[dict]]:
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {f: (d or {}).get("regles", []) for f, d in (doc.get("fichiers") or {}).items()}


def correspond(motif: str, chemin: str) -> bool:
    """`*` = un segment, `**` = zéro ou plusieurs segments."""
    chemin = re.sub(r"\[\d+\]", "", chemin)
    # `**.` et `.**` peuvent couvrir ZÉRO segment : le point qui les suit ou
    # les précède est donc optionnel, sinon `**.articulation.**` raterait un
    # chemin qui commence par `articulation`.
    rx = re.escape(motif)
    rx = rx.replace(r"\*\*\.", "(?:[^.]+\\.)*").replace(r"\.\*\*", "(?:\\.[^.]+)*")
    rx = rx.replace(r"\*\*", ".*").replace(r"\*", "[^.]+")
    return re.fullmatch(rx, chemin) is not None


# ────────────────────────────────────────────────────────────── sources

class Source:
    nom = "?"
    def cotes(self) -> list[dict]:
        raise NotImplementedError
    def disponible(self) -> bool:
        return True


class ParamsYaml(Source):
    """Les fichiers de params/, qualifiés par params/origines.yaml."""
    nom = "params/"

    def cotes(self) -> list[dict]:
        decl = lire_declaration(DECLARATION)
        out = []
        for f in sorted(PARAMS.glob("*.yaml")):
            if f.name == "origines.yaml":
                continue
            regles = decl.get(f.name, [])
            for chemin, valeur in lire_yaml_plat(f):
                trouve = next((r for r in regles if correspond(r["motif"], chemin)), None)
                out.append(dict(
                    fichier=f"params/{f.name}", chemin=chemin, valeur=valeur,
                    origine=(trouve or {}).get("origine") or NON_QUALIFIE,
                    source=(trouve or {}).get("source"),
                    note=(trouve or {}).get("note"),
                    nature=(trouve or {}).get("nature"),
                    motif=(trouve or {}).get("motif")))
        return out


class RelevesPieces(Source):
    """parts/<nom>.origines.yaml — relevé déposé par chaque pièce.

    Contrat fixé par la fiche 0010 §5. Inerte tant que parts/ est vide.
    """
    nom = "parts/ (relevés)"

    def disponible(self) -> bool:
        return PARTS.is_dir() and any(PARTS.glob("*.origines.yaml"))

    def cotes(self) -> list[dict]:
        out = []
        for f in sorted(PARTS.glob("*.origines.yaml")):
            plat = dict(lire_yaml_plat(f))
            for chemin, valeur in plat.items():
                if not chemin.endswith(".valeur"):
                    continue
                base = chemin[: -len(".valeur")]
                out.append(dict(
                    fichier=f"parts/{f.name}", chemin=base, valeur=valeur,
                    origine=plat.get(f"{base}.origine", NON_QUALIFIE),
                    source=plat.get(f"{base}.source"),
                    note=plat.get(f"{base}.note"), motif=None))
        return out


class LitterauxPieces(Source):
    """Littéraux numériques nus dans parts/**/*.py — cotes intraçables.

    Une valeur écrite en dur viole la règle 1 et n'a aucune origine.
    Les petits entiers (indices, comptes) sont ignorés : seuls les
    nombres qui ressemblent à des cotes sont signalés.
    """
    nom = "parts/ (littéraux)"
    IGNORES = {0, 1, 2, 3, -1}

    def disponible(self) -> bool:
        return PARTS.is_dir() and any(PARTS.rglob("*.py"))

    def cotes(self) -> list[dict]:
        out = []
        for f in sorted(PARTS.rglob("*.py")):
            try:
                arbre = ast.parse(f.read_text(encoding="utf-8"))
            except SyntaxError:
                continue
            for n in ast.walk(arbre):
                if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
                    if isinstance(n.value, bool) or n.value in self.IGNORES:
                        continue
                    out.append(dict(
                        fichier=str(f.relative_to(REPO)),
                        chemin=f"ligne {n.lineno}", valeur=repr(n.value),
                        origine=NON_QUALIFIE, motif=None,
                        source=None,
                        note="littéral numérique nu : viole la règle 1 et n'a aucune origine"))
        return out


SOURCES: list[Source] = [ParamsYaml(), RelevesPieces(), LitterauxPieces()]


# ─────────────────────────────────────────────────────────────── rapport

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--amont", action="store_true", help="ne lister que l'origine amont")
    p.add_argument("--strict", action="store_true", help="sortie non nulle si non qualifié")
    p.add_argument("--json", action="store_true", help="sortie machine")
    args = p.parse_args(argv)

    cotes, inactives = [], []
    for s in SOURCES:
        if s.disponible():
            cotes += s.cotes()
        else:
            inactives.append(s.nom)

    if args.json:
        json.dump(cotes, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 0

    par_origine: dict[str, int] = {}
    for c in cotes:
        par_origine[c["origine"]] = par_origine.get(c["origine"], 0) + 1

    print("═" * 78)
    print(" AUDIT DE L'ORIGINE DES COTES — inventaire, pas avis juridique")
    print("═" * 78)
    print(f"\n{len(cotes)} valeurs inventoriées.\n")
    largeur = max((len(o) for o in par_origine), default=10)
    for o in list(ORIGINES) + [NON_QUALIFIE]:
        if o in par_origine:
            n = par_origine[o]
            barre = "█" * max(1, round(40 * n / len(cotes)))
            marque = "  <-- risque de licence amont" if o == "amont" else ""
            print(f"  {o:<{largeur}}  {n:4d}  {barre}{marque}")
    if inactives:
        print(f"\n  sources inactives (pas encore de données) : {', '.join(inactives)}")

    par_nature: dict[str, int] = {}
    for c in cotes:
        n = c.get("nature") or "NON DÉCLARÉE"
        par_nature[n] = par_nature.get(n, 0) + 1
    print("\n" + "─" * 78)
    print(" NATURE — ce qui détermine la cote, donc quelle règle s'applique")
    print("─" * 78)
    REGLE = {"echelle": "règle 1 : dérive de H",
             "tenue": "note de calcul obligatoire",
             "interface": "règle 2 : ne suit jamais H",
             "procede": "contraintes de fabrication",
             "sans_objet": "pas une cote — nomenclature, prose, empreintes"}
    for n in list(NATURES) + ["sans_objet"]:
        if n in par_nature:
            print(f"  {n:14s} {par_nature[n]:5d}   {REGLE.get(n,'')}")
    manquant = [c for c in cotes if c.get("nature") is None]
    if manquant:
        print(f"  {'NON DÉCLARÉE':14s} {len(manquant):5d}   <-- défaut : nature à déclarer")

    amont = [c for c in cotes if c["origine"] == "amont"]
    print("\n" + "─" * 78)
    print(f" COTES D'ORIGINE AMONT — {len(amont)} valeurs")
    print("─" * 78)
    par_fichier: dict[str, list] = {}
    for c in amont:
        par_fichier.setdefault(c["fichier"], []).append(c)
    for f, lst in sorted(par_fichier.items(), key=lambda kv: -len(kv[1])):
        print(f"\n  {f}  —  {len(lst)} valeurs")
        motifs: dict[str, int] = {}
        for c in lst:
            motifs[c["motif"] or "(sans motif)"] = motifs.get(c["motif"] or "(sans motif)", 0) + 1
        for m, n in sorted(motifs.items(), key=lambda kv: -kv[1]):
            ex = next(c for c in lst if (c["motif"] or "(sans motif)") == m)
            print(f"      {n:4d}  {m}")
            if ex["source"]:
                print(f"            source : {ex['source'][:90]}")

    if args.amont:
        return 0

    nq = [c for c in cotes if c["origine"] == NON_QUALIFIE]
    if nq:
        print("\n" + "─" * 78)
        print(f" NON QUALIFIÉ — {len(nq)} valeurs. C'est un défaut à corriger.")
        print("─" * 78)
        for c in nq[:25]:
            print(f"  {c['fichier']:42s} {c['chemin']}")
        if len(nq) > 25:
            print(f"  … et {len(nq)-25} autres")

    amb = [c for c in cotes if c["origine"] == "ambigu"]
    if amb:
        print("\n" + "─" * 78)
        print(f" AMBIGU — {len(amb)} valeurs, volontairement non tranchées")
        print("─" * 78)
        vus = set()
        for c in amb:
            if c["motif"] in vus:
                continue
            vus.add(c["motif"])
            print(f"  {c['motif']}")
            if c["note"]:
                print(f"      {c['note'][:100]}")

    print("\n" + "═" * 78)
    print(" Cet inventaire ne dit pas ce qu'il faut en conclure.")
    print(" Voir decisions/0010 §4 : la portée juridique n'est pas tranchée ici.")
    print("═" * 78)

    return 1 if (args.strict and nq) else 0


if __name__ == "__main__":
    sys.exit(main())
