#!/usr/bin/env python3
"""Pilote SysML v2 : ENGENDRE model/yxor.sysml depuis params/ (rien n'est saisi à la main dans le .sysml).

    .venv/bin/python scripts/sysml.py            # résumé
    .venv/bin/python scripts/sysml.py --ecrire   # model/yxor.sysml

Créé le 2026-10-08. ESSAI, aucune décision : le YAML reste la SOURCE DE VÉRITÉ ;
le .sysml en est une VUE, engendrée, à côté (pilote proposé par les rapports de
méthodologie du 2026-10-06). Contenu :
  · les axes (params/joints.yaml) et les ensembles d'axes de l'explorateur ;
  · les capacités et leurs niveaux (params/capacites.yaml) ;
  · la gamme (fiche 0073) : Kit, Lab, Home et Pro, VARIANTES d'une même famille,
    chacune avec le niveau visé de chaque capacité (vide si à définir) ;
  · les exigences chiffrées du profil lab : par articulation et par tâche,
    couple ≥ a·M + b (phases 3a et 3b, à la hauteur visée H_S de
    anthropometry.yaml ; M, la masse du robot, reste un paramètre) ;
    l'autonomie et le niveau d'IA ; et leur traçabilité capacité → exigence → axe.
"""
from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
SORTIE = REPO / "model" / "yxor.sysml"
GROUPES = ("jambes", "bras", "taille", "nuque")


def lire(nom):
    import marche_composants as MC
    return MC.lire(nom)


def ident(x) -> str:
    """Un identifiant SysML sûr depuis une valeur de niveau (0.6 → n0_6 ; « depuis le dos » → depuis_le_dos)."""
    s = str(x).strip().lower()
    s = (s.replace("é", "e").replace("è", "e").replace("ê", "e").replace("à", "a").replace("ç", "c")
         .replace("+", "plus").replace(".", "_").replace(",", "_"))
    s = re.sub(r"[^a-z0-9_]+", "_", s).strip("_")
    return ("n" + s) if not s or s[0].isdigit() else s


def nombre(x: float) -> str:
    return f"{x:.6g}" if abs(x) >= 1e-12 else "0.0"


def axes() -> list[str]:
    jo = lire("joints.yaml")
    return [j["nom"] for g in GROUPES for j in (jo.get(g) or [])]


def non_retenus() -> list[str]:
    return [j["nom"] for j in (lire("joints.yaml").get("amont_non_retenus") or [])]


def exigences_lab(H: float) -> dict:
    """{(tâche, niveau): {axe: (a, b)}} du profil lab à la taille H : phase 3a (calcul direct) et 3b (marche)."""
    import explorateur as X
    import exigences_physiques as EP
    import simulations_marche as SM
    cap, an, lignes = EP.tout()
    marches, releve, _ = SM.charger()
    T = X.table_besoins(lignes, marches, releve, cap)
    cible = X.cible_defaut(cap, "lab")
    out = {}
    for t, niv in X.paires(cible):
        e = T.get((round(H, 2), t, niv))
        if not e:
            continue
        for ax, d in e.items():
            if d["pk"]:
                a, b = max(d["pk"], key=lambda ab: ab[0] * 10 + ab[1])          # l'entrée la plus exigeante à 10 kg
                out.setdefault((t, niv), {})[ax] = (a, b)
    return out


def engendrer() -> str:
    import explorateur as X
    cap = lire("capacites.yaml")
    an = lire("anthropometry.yaml")
    H = an["tailles"]["S"]["H_m"]
    tous = axes()
    L = ["// ENGENDRÉ par `.venv/bin/python scripts/sysml.py --ecrire` depuis params/ : NE PAS ÉDITER À LA MAIN.",
         "// Pilote SysML v2 (2026-10-08). Le YAML reste la source de vérité ; ce fichier en est une vue.",
         "package YXOR {", "",
         "    doc /* Gamme YXOR (fiche 0073) : Kit, Lab, Home et Pro, variantes d'une même famille. */", "",
         "    // ── Axes (params/joints.yaml, règle 3 : mêmes noms partout) ──",
         "    package Axes {",
         "        part def Articulation;"]
    for a in tous:
        L.append(f"        part def {a} :> Articulation;")
    L += ["    }", "",
          "    // ── Ensembles d'axes de l'explorateur (scripts/explorateur.py, ENSEMBLES) ──",
          "    package Ensembles {", "        private import Axes::*;"]
    for k, e in X.ENSEMBLES.items():
        L.append(f"        part def Ensemble{k} {{")
        L.append(f"            doc /* {sum(e['axes'].values())} axes. {e['source']} */")
        for a, n in e["axes"].items():
            if a in tous:
                L.append(f"            part {a} : Axes::{a}[{n}];")
            elif a in non_retenus():
                L.append(f"            part {a} : Articulation[{n}];   // dans joints.yaml, « amont_non_retenus » (fiche 0068)")
            else:
                L.append(f"            part {a} : Articulation[{n}];   // nom provisoire, absent de joints.yaml")
        L.append("        }")
    L += ["    }", "",
          "    // ── Capacités et niveaux (params/capacites.yaml) ──",
          "    package Capacites {"]
    for t, d in cap["taches"].items():
        L.append(f"        enum def Niveau_{t} {{")
        L.append(f"            doc /* {d['capacite']} ; grandeur : {d['grandeur']} ({d['unite']}). */")
        for n in d["niveaux"]:
            L.append(f"            enum {ident(n)};")
        L.append("        }")
    L += ["    }", "",
          "    // ── La gamme : quatre variantes d'une même famille (fiche 0073 ; profils de params/capacites.yaml) ──",
          "    package Gamme {", "        private import Capacites::*;",
          "        part def ModeleYXOR {", "            doc /* Ce que tout modèle de la gamme partage : la famille. */"]
    for t in cap["taches"]:
        L.append(f"            attribute {t} : Niveau_{t}[0..*];")
    L += ["        }"]
    for nom, p in cap["profils"].items():
        L.append(f"        part def YXOR_{nom.capitalize()} :> ModeleYXOR {{")
        L.append(f"            doc /* {p.get('decide', '')} */")
        taches = p.get("taches") or {}
        if not taches:
            L.append("            // capacités À DÉFINIR avec Jeremy")
        for t, v in taches.items():
            if v is None:
                L.append(f"            // {t} : niveau à balayer (phase 4b)")
                continue
            ns = [f"Niveau_{t}::{ident(n)}" for n in (v if isinstance(v, list) else [v])]
            L.append(f"            attribute :>> {t} = {ns[0] if len(ns) == 1 else '(' + ', '.join(ns) + ')'};")
        L.append("        }")
    L += ["        variation part def Gamme {",
          "            doc /* Les quatre modèles de la gamme (fiche 0073). */"]
    for nom in cap["profils"]:
        L.append(f"            variant part {nom} : YXOR_{nom.capitalize()};")
    L += ["        }", "    }", ""]
    # exigences chiffrées du Lab
    ex = exigences_lab(H)
    lab = cap["profils"]["lab"]["taches"]
    L += [f"    // ── Exigences chiffrées du profil lab, à H = {nombre(H)} m (anthropometry.yaml, tailles.S) ──",
          "    package ExigencesLab {", "        private import ScalarValues::*;",
          "        requirement def CoupleArticulation {",
          "            doc /* Couple de POINTE requis : τ ≥ a·M + b pour chaque tâche (M, masse du robot, en kg ;",
          "                   a en N·m/kg, b en N·m) ; la marge de la fiche 0051 s'applique en plus. */",
          "            attribute a : Real;", "            attribute b : Real;", "        }"]
    for (t, niv), par_axe in ex.items():
        for ax, (a, b) in sorted(par_axe.items()):
            nom = f"couple_{ax}_{t}_{ident(niv)}"
            L += [f"        requirement {nom} : CoupleArticulation {{",
                  f"            doc /* capacité {t} = {niv} ; axe {ax}. */",
                  f"            attribute :>> a = {nombre(a)};", f"            attribute :>> b = {nombre(b)};", "        }"]
    hyp = lire("puissance.yaml")["hypotheses"]
    cyc = cap["taches"]["autonomie"]["cycle"]["definition"]
    L += ["        requirement def Autonomie {", f"            doc /* {cyc} */", "            attribute minutes : Real;", "        }",
          f"        requirement autonomie_lab : Autonomie {{ attribute :>> minutes = {nombre(float(lab['autonomie']))}; }}",
          "        requirement def IAEmbarquee {", "            attribute niveau : String;", "        }",
          f"        requirement ia_lab : IAEmbarquee {{ attribute :>> niveau = \"{lab['ia_embarquee']}\"; }}",
          "    }", "",
          "    // ── Traçabilité : chaque exigence de couple se rattache à son axe (dépendance exigence → axe) ──",
          "    package Tracabilite {", "        private import Axes::*;", "        private import ExigencesLab::*;"]
    for (t, niv), par_axe in ex.items():
        for ax in sorted(par_axe):
            if ax in tous:
                L.append(f"        dependency ExigencesLab::couple_{ax}_{t}_{ident(niv)} to Axes::{ax};")
    L += ["    }", "}", ""]
    _ = math, hyp
    return "\n".join(L)


def validateur() -> Path | None:
    """Le binaire OpenSysML (Open-MBEE, Apache-2.0), désigné par la variable YXOR_SYSML ; None s'il est absent.
    Il n'est PAS dans le dépôt (binaire, règle 4) ni installé hors du dossier de session : le contrôle saute alors,
    et le dit."""
    import os
    c = os.environ.get("YXOR_SYSML")
    return Path(c) if c and Path(c).is_file() else None


def valider(texte: str) -> tuple[int, str] | None:
    """(code de retour, sortie) d'OpenSysML sur un texte SysML ; None sans validateur. Code 0 : aucune erreur."""
    import os
    import subprocess
    import tempfile
    v = validateur()
    if v is None:
        return None
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "yxor.sysml"
        f.write_text(texte, encoding="utf-8")
        env = dict(os.environ, HOME=d, XDG_CACHE_HOME=d)
        r = subprocess.run([str(v), "-validate", str(f)], capture_output=True, text=True, env=env, timeout=120)
        return r.returncode, (r.stdout + r.stderr)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ecrire", action="store_true")
    a = ap.parse_args(argv)
    txt = engendrer()
    n_req = txt.count("requirement couple_")
    print(f"  SysML : {len(txt.splitlines())} lignes ; {len(axes())} axes ; {n_req} exigences de couple")
    v = valider(txt)
    print("  validation OpenSysML : SAUTÉE (variable YXOR_SYSML absente : binaire hors du dépôt)" if v is None
          else f"  validation OpenSysML : code {v[0]} ({'aucune erreur' if v[0] == 0 else 'ERREURS'})")
    if v and v[0]:
        print(v[1][-2000:])
    if a.ecrire:
        SORTIE.parent.mkdir(exist_ok=True)
        SORTIE.write_text(txt, encoding="utf-8")
        print(f"  -> {SORTIE.relative_to(REPO)}")
    return 1 if v and v[0] else 0


if __name__ == "__main__":
    sys.exit(main())
