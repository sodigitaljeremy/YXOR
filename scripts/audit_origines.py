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

# Fichiers qui DÉCLARENT des règles sur les cotes, sans en porter aucune.
# Les auditer reviendrait à demander l'origine d'un motif de chemin de clé
# ou d'une phrase d'explication : la question n'a pas de sens. La liste est
# nommée plutôt que testée au cas par cas, pour que la prochaine addition
# soit une ligne et non une exception de plus.
FICHIERS_DECLARATIFS = {
    "origines.yaml",    # origine et nature des cotes (fiches 0010, 0013)
    "nullites.yaml",    # pourquoi une valeur est absente (fiche 0020)
    "fournisseurs.yaml",# provenance des fichiers tiers (fiche 0030)
    "sources.yaml",     # registre des documents lus (fiche 0040)
    "mesures.yaml",     # actes de mesure et incertitudes (fiche 0041)
}

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

    SAUF s'ils portent un `id` : ils sont alors adressés par cet id,
    `reglages.cutter_cartonplume_5.saignee`. La fiche 0026 l'avait promis
    — « le chargeur en fait un dictionnaire, et les motifs s'écrivent
    reglages.<id>.saignee » — mais seul le chargeur le faisait.

    Deux conventions de chemin pour la même donnée, c'est une règle morte
    en attente : six motifs de `origines.yaml` visaient `reglages.*.id`
    et n'ont jamais correspondu à `reglages[0].id`. Le fourre-tout
    `reglages.**` les remplaçait en silence, et un identifiant écrit à la
    main était compté comme une MESURE.
    """
    out: list[tuple[str, object]] = []
    if isinstance(noeud, dict):
        for k, v in noeud.items():
            out += aplatir(v, f"{prefixe}.{k}" if prefixe else str(k))
    elif isinstance(noeud, list):
        for i, v in enumerate(noeud):
            cle = v.get("id") if isinstance(v, dict) else None
            out += aplatir(v, f"{prefixe}.{cle}" if cle else f"{prefixe}[{i}]")
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
            if f.name in FICHIERS_DECLARATIFS:
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
                # Ne lire QUE le bloc `cotes:`. Le bloc `cotes_schema:`
                # déclare des cotes de DESSIN — lettre, tracé, valeur — et
                # non des cotes d'origine : ses `valeur` ressortaient
                # « non qualifiées » et gonflaient le compte de 13.
                if not chemin.startswith("cotes[") or not chemin.endswith(".valeur"):
                    continue
                base = chemin[: -len(".valeur")]
                out.append(dict(
                    fichier=f"parts/{f.name}", chemin=base, valeur=valeur,
                    origine=plat.get(f"{base}.origine", NON_QUALIFIE),
                    source=plat.get(f"{base}.source"),
                    nature=plat.get(f"{base}.nature"),
                    note=plat.get(f"{base}.note"), motif=None))
        return out


class LitterauxPieces(Source):
    """Littéraux numériques nus dans parts/**/*.py — cotes intraçables.

    Une valeur écrite en dur viole la règle 1 et n'a aucune origine.
    Les petits entiers (indices, comptes) sont ignorés : seuls les
    nombres qui ressemblent à des cotes sont signalés.
    """
    nom = "parts/ (littéraux)"
    # ⚠ N'exempter QUE des entiers. `2.0 in {0,1,2,3,-1}` vaut True en
    # Python — 2.0 == 2 — si bien qu'un flottant comme 2.0, qui peut
    # parfaitement être une cote en millimètres, se faisait exempter en
    # silence. Un flottant est toujours inventorié.
    IGNORES = {0, 1, 2, 3, -1}
    # Un littéral qui n'est PAS une cote doit le DIRE, avec sa raison.
    # Marqueur : `# non-cote: <raison>` en fin de ligne. Il n'exempte pas
    # en silence — la ligne est inventoriée comme non-cote déclarée, donc
    # visible dans l'audit. Un blanc-seing muet serait pire que le défaut
    # qu'il masque.
    # Accepté en fin de ligne OU sur la ligne juste au-dessus : une
    # expression longue reste lisible sans commentaire à rallonge.
    MARQUEUR = re.compile(r"#\s*non-cote\s*:\s*(.+?)\s*$")

    def disponible(self) -> bool:
        return PARTS.is_dir() and any(PARTS.rglob("*.py"))

    def cotes(self) -> list[dict]:
        out = []
        for f in sorted(PARTS.rglob("*.py")):
            texte = f.read_text(encoding="utf-8")
            lignes = texte.splitlines()
            try:
                arbre = ast.parse(texte)
            except SyntaxError as err:
                # ⚠ NE JAMAIS IGNORER EN SILENCE. Un fichier de pièce qui
                # ne s'analyse plus voyait ses littéraux DISPARAÎTRE de
                # l'inventaire : le total baissait et `--strict` passait,
                # sur un fichier cassé. C'est l'inverse de ce que l'audit
                # doit faire. Une erreur d'analyse est un défaut, pas un
                # motif d'exclusion.
                out.append(dict(
                    fichier=str(f.relative_to(REPO)),
                    chemin=f"ligne {err.lineno}", valeur="—",
                    origine=NON_QUALIFIE, nature=None, motif=None, source=None,
                    note=f"FICHIER NON ANALYSABLE : {err.msg}. "
                         f"Ses cotes sont invisibles pour l'audit."))
                continue
            # Positions syntaxiques qui ne peuvent PAS porter une cote :
            #   round(x, 4)      -> précision d'arrondi
            #   a < 1e-6         -> seuil de comparaison
            #   default=0.25     -> valeur par défaut, déclarée et visible
            # Filtrer sur la POSITION, jamais sur la valeur : filtrer sur la
            # valeur reviendrait à décider qu'un nombre « a l'air » d'une cote.
            exempts = set()
            for n in ast.walk(arbre):
                if isinstance(n, ast.Call):
                    fonc = n.func
                    if isinstance(fonc, ast.Name) and fonc.id == "round" and len(n.args) > 1:
                        exempts.add(id(n.args[1]))
                    for kw in n.keywords:
                        if kw.arg == "default":
                            exempts.add(id(kw.value))
                if isinstance(n, ast.Compare):
                    for cmp_ in [n.left, *n.comparators]:
                        exempts.add(id(cmp_))
            for n in ast.walk(arbre):
                if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
                    if isinstance(n.value, bool):
                        continue
                    if isinstance(n.value, int) and n.value in self.IGNORES:
                        continue
                    if id(n) in exempts:
                        continue
                    voisines = [lignes[i] for i in (n.lineno - 1, n.lineno - 2)
                                if 0 <= i < len(lignes)]
                    m = next((mm for l in voisines
                              if (mm := self.MARQUEUR.search(l))), None)
                    if m:
                        out.append(dict(
                            fichier=str(f.relative_to(REPO)),
                            chemin=f"ligne {n.lineno}", valeur=repr(n.value),
                            origine="propre", nature="sans_objet", motif=None,
                            source=f"non-cote déclarée : {m.group(1)}",
                            note=None))
                        continue
                    out.append(dict(
                        fichier=str(f.relative_to(REPO)),
                        chemin=f"ligne {n.lineno}", valeur=repr(n.value),
                        origine=NON_QUALIFIE, motif=None,
                        source=None,
                        nature=None,
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

    # Une source qui s'escamote fait baisser le total sans un mot, et
    # --strict passe d'autant plus facilement. Elle doit se signaler.
    for nom in inactives:
        print(f"  ⚠ SOURCE INACTIVE : {nom} — aucune donnée collectée. "
              "Le total ci-dessus est d'autant plus bas.")
    if inactives:
        print()

    par_origine: dict[str, int] = {}
    for c in cotes:
        par_origine[c["origine"]] = par_origine.get(c["origine"], 0) + 1

    print("═" * 78)
    print(" AUDIT DE L'ORIGINE DES COTES — inventaire, pas avis juridique")
    print("═" * 78)
    num = sum(1 for c in cotes
              if isinstance(c["valeur"], (int, float))
              and not isinstance(c["valeur"], bool))
    print(f"\n{len(cotes)} valeurs inventoriées, dont {num} NUMÉRIQUES.")
    print("  Le reste est de la prose, des booléens et des nuls : ils ont une")
    print("  origine, mais ce ne sont pas des cotes.\n")
    largeur = max((len(o) for o in par_origine), default=10)
    for o in list(ORIGINES) + [NON_QUALIFIE]:
        if o in par_origine:
            n = par_origine[o]
            barre = "█" * max(1, round(40 * n / len(cotes)))
            marque = "  <-- risque de licence amont" if o == "amont" else ""
            print(f"  {o:<{largeur}}  {n:4d}  {barre}{marque}")

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
