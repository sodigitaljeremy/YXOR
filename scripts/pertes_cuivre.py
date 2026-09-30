#!/usr/bin/env python3
"""Pertes cuivre par candidat, sur la marche de référence — INFORMATION, pas un critère.

    .venv/bin/python scripts/pertes_cuivre.py
    .venv/bin/python scripts/pertes_cuivre.py --taille 0.55

Venv DU PROJET. Écrit le 2026-10-01 pour la famille G des critères
manquants (docs/criteres-manquants.md). Ce script ne note rien : il
calcule, et il dit ce qui manque.

═══════════════════════════════════════════════════════════════════════
 LE CALCUL
═══════════════════════════════════════════════════════════════════════

1. La marche de référence (exports/actionneurs/marche_15s.csv, ToddlerBot,
   15 s) donne le couple de chaque articulation de jambe à chaque pas.
2. Ce couple est mis à l'échelle de la taille H, comme dans
   scripts/dimensionnement.py : couple(H) = couple_P1 · masse(H)/M0 · H/H0,
   la masse comptant les 12 actionneurs du candidat à leur masse RÉELLE.
3. Le courant de phase : I = |couple| / Kt, avec Kt ramené à la SORTIE
   du réducteur.
   - Kt publié : utilisé s'il est donné côté sortie. S'il est donné côté
     moteur, il est multiplié par la réduction (rendement ignoré, et dit).
   - Sinon, Kt IMPLICITE = couple nominal ÷ courant nominal publiés. Cela
     suppose un couple proportionnel au courant jusqu'au nominal, et le
     drapeau le dit.
4. La perte cuivre dépend de ce que le constructeur appelle « courant » :
   - s'il s'agit d'une AMPLITUDE (transformée de Park à amplitude
     conservée) : P = 3/2 · R_phase · I² ;
   - s'il s'agit d'une VALEUR EFFICACE par phase : P = 3 · R_phase · I².
   Si la fiche le précise (RobStride : N·m/A efficace), une seule valeur ;
   sinon les DEUX bornes, qui diffèrent d'un facteur 2.
   Une résistance ligne-ligne est divisée par 2 (moteur en étoile, supposé).
5. Énergie = Σ articulations ∫ P dt ; puissance moyenne = énergie ÷ durée.

Ce que ce calcul ne dit pas : les pertes fer et mécaniques, le rendement
du réducteur, la montée de R avec la température (≈ +0,4 %/K pour le
cuivre, soit +30 % à 100 °C), et une autre allure que la marche droite.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyser_marche as AM  # noqa: E402
import dimensionnement as D  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
SORTIE = REPO / "exports" / "actionneurs" / "pertes_cuivre.json"
CANDIDATS = ("rs05", "edulite05", "dm_j4310_48v", "gim4310_10", "x2_7", "ak45_10_v3", "sts3250")


def num(champ):
    v = (champ or {}).get("valeur") if isinstance(champ, dict) else champ
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def parametres(cat: dict, cid: str) -> dict:
    """R_phase et Kt de sortie, lus dans la collecte (jamais déclarés ici)."""
    col = (cat.get("collecte_criteres_manquants") or {}).get("candidats", {}).get(cid) or {}
    c = cat["candidats"][cid]
    drapeaux = []
    R = num(col.get("G_resistance_ohm"))
    conv_R = str((col.get("G_resistance_convention") or {}).get("valeur") or "")
    if R is not None and "ligne" in conv_R:
        R = R / 2
        drapeaux.append("R ligne-ligne ÷ 2 (étoile supposée)")
    kt = num(col.get("G_kt"))
    cote = str((col.get("G_kt_cote") or {}).get("valeur") or "")
    conv = str((col.get("G_kt_convention_courant") or {}).get("valeur") or "non précisé")
    red = num(col.get("G_reduction")) or num(c.get("reduction"))
    c_nom, i_nom = num(c.get("couple_continu_Nm")), num(col.get("G_courant_nominal_A"))
    source_kt = None
    if kt is not None:
        source_kt = "publié"
        if "moteur" in cote:
            if red is None:
                kt, source_kt = None, None
                drapeaux.append("Kt côté moteur, réduction inconnue")
            else:
                kt = kt * red
                drapeaux.append(f"Kt moteur × réduction {red:g} (rendement ignoré)")
        elif "sortie" not in cote:
            drapeaux.append("côté du Kt non précisé : supposé SORTIE")
        # Cohérence : Kt × courant nominal doit redonner le couple nominal.
        # Le courant nominal est publié en crête (Apk) chez RobStride : il
        # est ramené en efficace (÷ √2) si Kt est donné par ampère efficace.
        if kt is not None and c_nom and i_nom:
            i_ref = i_nom / 2 ** 0.5 if "efficace" in conv else i_nom
            r_ = kt * i_ref / c_nom
            drapeaux.append(f"contrôle : Kt × I_nominal = {kt * i_ref:.2f} N·m pour {c_nom:g} N·m publiés")
            # Un Kt publié qui ne redonne pas le couple nominal à ±25 % est
            # incohérent avec sa propre fiche : il n'est PAS utilisé.
            if not 0.8 <= r_ <= 1.25:
                drapeaux.append(f"Kt publié INCOHÉRENT (×{r_:.2f}) : écarté, Kt implicite utilisé")
                kt = None
    if kt is None and c_nom and i_nom:
        kt, source_kt = c_nom / i_nom, "IMPLICITE (couple nominal ÷ courant nominal)"
        conv = "non précisé"   # celle du courant nominal, que la fiche ne dit pas
    manque = [n for n, v in (("R", R), ("Kt", kt)) if v is None]
    return dict(R=R, kt=kt, source_kt=source_kt, convention=conv, drapeaux=drapeaux, manque=manque)


def calculer(H: float) -> dict:
    cat = D.charger_catalogue()
    analyse = AM.analyser(AM.SERIE)
    ref = D.reference(cat, analyse)
    besoins = D.besoins_p1(analyse)
    jambes = sorted(besoins)
    with AM.SERIE.open(encoding="utf-8") as fh:
        lignes = list(csv.DictReader(fh))
    t = [float(l["temps_s"]) for l in lignes]
    duree = t[-1] - t[0]
    out = dict(taille_m=H, duree_s=duree, n_pas=len(t), articulations=len(jambes), candidats={})
    for cid in CANDIDATS:
        p = parametres(cat, cid)
        cl = D.classe_catalogue(cat, cid)
        res = dict(nom=cat["candidats"][cid]["nom"], **p)
        if p["manque"] or cl["masse"] is None:
            res["statut"] = "non calculable : " + ", ".join(p["manque"] + (["masse"] if cl["masse"] is None else []))
            out["candidats"][cid] = res
            continue
        m = D.masse(H, ref, D.config_homogene(cl), besoins)
        f = m / ref["M0"] * H / ref["H0"]
        e = 0.0          # ∫ R I² dt, sommé sur les articulations
        for a in jambes:
            col = f"tau:{a}"
            for k in range(1, len(t)):
                i = abs(float(lignes[k][col])) * f / p["kt"]
                e += p["R"] * i * i * (t[k] - t[k - 1])
        # Convention du courant publiée : une seule valeur ; sinon les deux bornes.
        facteurs = ({"efficace": 3.0} if "efficace" in p["convention"] else
                    {"amplitude": 1.5} if ("crête" in p["convention"] or "amplitude" in p["convention"]) else
                    {"amplitude": 1.5, "efficace": 3.0})
        res.update(statut="calculé", masse_robot_kg=round(m, 3), facteur_couple=round(f, 4),
                   energie_J={k: round(v * e, 1) for k, v in facteurs.items()},
                   puissance_moyenne_W={k: round(v * e / duree, 2) for k, v in facteurs.items()})
        out["candidats"][cid] = res
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--taille", type=float, default=0.55,
                    help="taille H en mètres (défaut 0,55 : bas de la fourchette de S, cadrage § 6)")
    a = ap.parse_args(argv)
    if not AM.SERIE.exists():
        print(f"série absente : {AM.SERIE} — la régénérer avec sim/upstream/enregistrer_marche.py")
        return 1
    r = calculer(a.taille)
    print(f"\n  Pertes cuivre, 12 actionneurs de jambe, marche de référence mise à l'échelle de H = {a.taille:g} m")
    print(f"  ({r['n_pas']} pas, {r['duree_s']:.1f} s). INFORMATION, pas un critère.\n")
    print(f"  {'candidat':32s} {'R (Ω)':>7s} {'Kt (N·m/A)':>11s}  {'P moy. amplitude':>17s}  {'P moy. efficace':>16s}")
    for cid, c in r["candidats"].items():
        if c["statut"] != "calculé":
            print(f"  {c['nom'][:32]:32s}  {c['statut']}")
            continue
        pm = c["puissance_moyenne_W"]
        col = lambda k: f"{pm[k]:14.2f} W" if k in pm else f"{'—':>16s}"
        print(f"  {c['nom'][:32]:32s} {c['R']:7.3f} {c['kt']:11.3f}  {col('amplitude')}  {col('efficace')}"
              + (f"   Kt {c['source_kt']}" if c['source_kt'] != 'publié' else "")
              + ("   ⚠ " + " ; ".join(c["drapeaux"]) if c["drapeaux"] else ""))
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  -> {SORTIE.relative_to(REPO)}")
    print("  Une seule colonne : convention publiée. Deux colonnes : convention non précisée (facteur 2).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
