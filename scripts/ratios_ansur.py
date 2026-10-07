#!/usr/bin/env python3
"""Ratios anthropométriques recalculés depuis ANSUR II (2012).

    .venv/bin/python scripts/ratios_ansur.py            # tableau lisible
    .venv/bin/python scripts/ratios_ansur.py --yaml     # bloc à recopier

═══════════════════════════════════════════════════════════════════════
 POURQUOI REMPLACER DRILLIS & CONTINI
═══════════════════════════════════════════════════════════════════════

Les quatorze ratios de `anthropometry.yaml` viennent de la figure 4.1 de
Winter. C'est un GRAPHIQUE : aucun de ces nombres n'apparaît dans le
texte, et la source primaire (Office of Vocational Rehabilitation, 1966)
n'est pas accessible. Le fichier les porte depuis le début avec
`verifie: false` — quatorze fois.

ANSUR II est l'inverse : 93 mesures directes sur 6 068 personnes, en CSV,
recalculables. On ne croit plus un graphique sur parole, on calcule.

═══════════════════════════════════════════════════════════════════════
 LES DEUX RÉSERVES, QUI NE SONT PAS DES DÉTAILS
═══════════════════════════════════════════════════════════════════════

1. **Population militaire, explicitement non représentative.** Des
   soldats américains en activité, sélectionnés sur des critères
   physiques, d'âge très resserré. Ce n'est pas la population générale,
   et l'enquête elle-même le dit. Un robot dimensionné là-dessus est
   proportionné comme un militaire de 2012, pas comme un humain moyen.

2. **ANSUR II ne donne QUE des longueurs.** Les masses segmentaires ne
   se mesurent pas sur un vivant : elles viennent de dissections. Elles
   restent chez Dempster (via Winter tab. 4.1), et cette séparation doit
   rester visible — c'était déjà la faute corrigée par la fiche 0012,
   où le fichier annonçait « Drillis & Contini » pour tout.

Deux ratios ne sont pas dérivables non plus : la hauteur de tête et la
hauteur de cou. ANSUR mesure le tragion et la cervicale, pas le menton
ni le vertex sur la même verticale. Ils restent chez D&C, et le disent.

═══════════════════════════════════════════════════════════════════════
 CE QUE LE SCRIPT NE FAIT PAS
═══════════════════════════════════════════════════════════════════════

Il **n'écrit pas** `anthropometry.yaml`. Il produit un bloc à recopier.
Remplacer quatorze cotes d'échelle est une décision, pas un effet de
bord : c'est la même règle que la simulation du navigateur (fiche 0023)
— calculer n'est pas enregistrer.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import statistics as stats
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CACHE = REPO / "exports" / "ansur"        # hors Git : engendré, régénérable

# Les CSV publics, tels que publiés. Voir params/fournisseurs.yaml pour la
# provenance complète et les conditions (fiche 0030).
SOURCES = {
    "male": "https://raw.githubusercontent.com/senihberkay/US-Army-ANSUR-II/"
            "master/ANSUR%20II%20MALE%20Public.csv",
    "female": "https://raw.githubusercontent.com/senihberkay/US-Army-ANSUR-II/"
              "master/ANSUR%20II%20FEMALE%20Public.csv",
}

STATURE = "stature"

# ── Correspondance ratio -> mesures ANSUR ────────────────────────────
#
# Chaque entrée est une SOUSTRACTION de colonnes, additionnées avec leur
# signe. `None` marque un ratio non dérivable d'ANSUR : il reste chez
# Drillis & Contini, et le dit.
#
# Les points de repère sont ceux de l'anthropométrie classique :
#   trochanterion  le grand trochanter — le relief du fémur sous la
#                  hanche, qui sert de repère à l'articulation
#   tibiale        le plateau du tibia, donc le genou
#   malléole       la saillie de la cheville
#   acromion       la pointe de l'épaule
#   radiale        la tête du radius, donc le coude
#   stylion        l'apophyse styloïde du radius, donc le poignet
RATIOS: dict[str, tuple[list[tuple[str, int]] | None, str]] = {
    "hauteur_hanche":   ([("trochanterionheight", +1)],
                         "hauteur du grand trochanter"),
    "cuisse":           ([("trochanterionheight", +1), ("tibialheight", -1)],
                         "trochanter moins tibiale : le fémur"),
    "tibia":            ([("tibialheight", +1), ("lateralmalleolusheight", -1)],
                         "tibiale moins malléole : la jambe"),
    "pied_longueur":    ([("footlength", +1)], "mesure directe"),
    "pied_largeur":     ([("footbreadthhorizontal", +1)], "mesure directe"),
    "cheville_hauteur": ([("lateralmalleolusheight", +1)],
                         "hauteur de la malléole latérale"),
    "largeur_epaules":  ([("biacromialbreadth", +1)], "d'un acromion à l'autre"),
    "largeur_bassin":   ([("hipbreadth", +1)], "mesure directe, debout"),
    "tronc_hauteur":    ([("acromialheight", +1), ("trochanterionheight", -1)],
                         "épaule moins hanche — DIRECTE ici, dérivée chez D&C"),
    "bras":             ([("acromionradialelength", +1)],
                         "acromion à radiale : le bras"),
    "avant_bras":       ([("radialestylionlength", +1)],
                         "radiale à stylion : l'avant-bras"),
    "main_longueur":    ([("handlength", +1)], "mesure directe"),
    "profondeur_poitrine": ([("chestdepth", +1)],
                         "mesure directe : profondeur de la poitrine (ajoutée le 2026-10-07, place dans le tronc)"),
    "tete_hauteur":     (None,
                         "ANSUR mesure le tragion et la cervicale, pas le "
                         "menton ni le vertex sur la même verticale"),
    "cou_hauteur":      (None,
                         "même raison : aucune mesure ANSUR n'isole le cou"),
}


def telecharger(nom: str, url: str) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / f"{nom}.csv"
    if f.exists() and f.stat().st_size > 100_000:
        return f
    print(f"  téléchargement de {nom}…", flush=True)
    with urllib.request.urlopen(url, timeout=180) as r:
        f.write_bytes(r.read())
    return f


def empreinte(f: Path) -> str:
    return hashlib.sha256(f.read_bytes()).hexdigest()


def lire(f: Path) -> list[dict]:
    with f.open(encoding="latin-1") as fh:
        return list(csv.DictReader(fh))


def ratio_par_sujet(lignes: list[dict], formule) -> list[float]:
    """Le ratio est calculé SUJET PAR SUJET, puis moyenné.

    Et non : moyenne des mesures divisée par moyenne des statures. Les
    deux diffèrent, et seule la première a un sens — on veut la
    proportion d'un corps, pas la proportion d'un corps moyen qui
    n'existe pas. L'écart-type obtenu décrit alors la dispersion des
    PROPORTIONS, ce qui est précisément ce qu'on cherche à savoir.
    """
    out = []
    for r in lignes:
        try:
            s = float(r[STATURE])
            v = sum(signe * float(r[col]) for col, signe in formule)
        except (KeyError, ValueError):
            continue
        if s > 0:
            out.append(v / s)
    return out


def calculer() -> dict:
    jeux = {}
    for nom, url in SOURCES.items():
        f = telecharger(nom, url)
        jeux[nom] = (lire(f), empreinte(f))

    res = {}
    for cle, (formule, note) in RATIOS.items():
        if formule is None:
            res[cle] = dict(derivable=False, note=note)
            continue
        par_sexe, tous = {}, []
        for sexe, (lignes, _) in jeux.items():
            v = ratio_par_sujet(lignes, formule)
            par_sexe[sexe] = dict(moyenne=stats.fmean(v),
                                  ecart_type=stats.stdev(v), n=len(v))
            tous += v
        res[cle] = dict(derivable=True, note=note,
                        moyenne=stats.fmean(tous),
                        ecart_type=stats.stdev(tous),
                        n=len(tous), par_sexe=par_sexe,
                        formule=" ".join(f"{'+' if s > 0 else '-'}{c}"
                                         for c, s in formule))
    res["_empreintes"] = {n: e for n, (_, e) in jeux.items()}
    res["_effectifs"] = {n: len(l) for n, (l, _) in jeux.items()}
    return res


# ═══════════════════════════════════════════════════════════════════════
#  DRILLIS & CONTINI — FIGÉES, parce que le YAML ne les porte plus
# ═══════════════════════════════════════════════════════════════════════
#
# Jusqu'au 2026-09-30, la colonne « D&C » lisait `anthropometry.yaml`.
# Depuis la fiche 0034, ce fichier porte ANSUR : la colonne affichait
# ANSUR sous l'étiquette D&C, et l'écart valait 0 % PAR CONSTRUCTION
# (audit de la nuit du 2026-09-29, § 8 H7).
#
# Valeurs relevées dans l'historique git, telles qu'elles étaient avant le
# remplacement : `git show 9c7eef5:params/anthropometry.yaml`, bloc
# `ratios`. Source déclarée à l'époque : « D&C fig. 4.1 » — Drillis &
# Contini (1966), via Winter, figure 4.1 — avec `verifie: false` sur
# chaque ligne. La figure est un GRAPHIQUE : l'attribution est établie,
# les valeurs ne le sont pas. Elles restent donc une comparaison, pas une
# référence. `tronc_hauteur` et `cou_hauteur` étaient DÉRIVÉES par
# soustraction (0,818 − 0,530 et 1 − 0,130 − 0,818), pas publiées.
DRILLIS_CONTINI = {
    "hauteur_hanche": 0.530, "cuisse": 0.245, "tibia": 0.246,
    "pied_longueur": 0.152, "pied_largeur": 0.055, "cheville_hauteur": 0.039,
    "largeur_epaules": 0.259, "largeur_bassin": 0.191, "tronc_hauteur": 0.288,
    "bras": 0.186, "avant_bras": 0.146, "main_longueur": 0.108,
    "tete_hauteur": 0.130, "cou_hauteur": 0.052,
}


def afficher(res: dict, anciens: dict | None = None) -> None:
    eff = res["_effectifs"]
    print(f"\n  ANSUR II — {eff['male']} hommes + {eff['female']} femmes "
          f"= {sum(eff.values())} sujets\n")
    print(f"  {'ratio':<20} {'ANSUR':>8} {'σ':>7} {'n':>6}   "
          f"{'D&C':>7} {'écart':>8}")
    print("  " + "─" * 62)
    for cle, d in res.items():
        if cle.startswith("_"):
            continue
        if not d["derivable"]:
            print(f"  {cle:<20} {'—':>8} {'':>7} {'':>6}   "
                  f"{(anciens or {}).get(cle, ''):>7}   NON DÉRIVABLE")
            continue
        anc = (anciens or {}).get(cle)
        ecart = f"{100*(d['moyenne']-anc)/anc:+.1f} %" if anc else ""
        print(f"  {cle:<20} {d['moyenne']:>8.4f} {d['ecart_type']:>7.4f} "
              f"{d['n']:>6}   {anc if anc else '—':>7} {ecart:>8}")
    print("\n  σ = écart-type des PROPORTIONS entre sujets, pas des mesures.")


def en_yaml(res: dict) -> str:
    eff = res["_effectifs"]
    out = [
        "# ── ANSUR II (2012) — engendré par scripts/ratios_ansur.py ──",
        f"# {eff['male']} hommes + {eff['female']} femmes = {sum(eff.values())} sujets.",
        "# RÉSERVE 1 : population militaire américaine, explicitement non",
        "#   représentative de la population générale.",
        "# RÉSERVE 2 : ANSUR ne donne que des LONGUEURS. Les masses restent",
        "#   chez Dempster (dissections) — voir le bloc `masses`.",
        "ratios:",
    ]
    for cle, d in res.items():
        if cle.startswith("_"):
            continue
        if not d["derivable"]:
            out += [f"  {cle}:",
                    "    valeur: null   # À CONSERVER de Drillis & Contini",
                    f"    source: \"D&C fig. 4.1 — non dérivable d'ANSUR II\"",
                    "    verifie: false",
                    f"    note: >",
                    f"      {d['note']}"]
            continue
        out += [f"  {cle}:",
                f"    valeur: {d['moyenne']:.4f}",
                f"    source: \"ANSUR II 2012, {d['formule']} / stature\"",
                "    verifie: true",
                f"    ecart_type: {d['ecart_type']:.4f}",
                f"    effectif: {d['n']}",
                f"    note: \"{d['note']}\""]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--yaml", action="store_true",
                    help="produit le bloc YAML à recopier, sans rien écrire")
    a = ap.parse_args()
    res = calculer()
    if a.yaml:
        print(en_yaml(res))
        return 0
    afficher(res, DRILLIS_CONTINI)
    print("\n  empreintes des CSV employés :")
    for n, e in res["_empreintes"].items():
        print(f"    {n:<8} sha256:{e[:32]}…")
    print("\n  Ce script N'ÉCRIT PAS anthropometry.yaml. `--yaml` produit le")
    print("  bloc à recopier : remplacer quatorze cotes est une décision.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
