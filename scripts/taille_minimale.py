#!/usr/bin/env python3
"""Taille minimale GÉOMÉTRIQUE : les moteurs entrent-ils dans les segments ?

    .venv/bin/python scripts/taille_minimale.py      # les ensembles du 2026-10-04, RobStride

Versé dans le dépôt le 2026-10-07 (règle de Jeremy du même jour : toute étude
réutilisée par un calcul vit dans le dépôt, avec un test). RECONSTRUCTION des
études de session hmin.py et hmin_ecart.py du 2026-10-04 (19 h 30 à 19 h 55),
jamais versées, retrouvées dans la transcription de la session (accès accordé
par Jeremy le 2026-10-07). Leurs formules sont reprises telles quelles ; seule
la description des moteurs est généralisée à tout actionneur du marché.

DEUX LECTURES de « taille minimale » (celles du 2026-10-04) :
  · proportions ANSUR strictes : tout le robot grandit jusqu'à ce que la chaîne
    la plus serrée tienne : H_min = max(besoin / ratio ANSUR) ;
  · AVEC ÉCARTS (comme la cheville du squelette) : les proportions restent
    celles de H, seules les chaînes VERTICALES qui débordent s'allongent ; la
    hauteur réelle vaut H + Σ dépassements. Bras et largeurs s'allongent ou
    s'élargissent sans changer H (hypothèse d'origine).
La lecture segment par segment n'est pas exploitable (1,4 à 2,4 m, constat du
2026-10-04) : les segments sont regroupés en chaînes par membre.

CONVENTIONS (mm) : plaques e, jeu j, voile v. Moteur : rayon d'ENVELOPPE R (bride
comprise), longueur L, plaque de stator r_st, plaque de sortie r_so. Sans
plan coté (marché, RS06, RS03) : r_st = R, r_so = R/2 + v (HYPOTHÈSE d'origine).
Servo en boîtier : R = moitié de sa plus grande cote, L = sa plus grande cote
(HYPOTHÈSE, prudente : orientation inconnue).

HYPOTHÈSES d'origine, conservées : la taille (articulation du buste) est logée
au centre, à côté des lacets de hanche, au-dessus des roulis de hanche ; le
volume de l'électronique, de la batterie et du contenu de la tête est compté
NUL (le tronc réel sera plus long) ; cardan des bielles (b) : 10 mm de demi-
hauteur, non vérifié.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
VERTICALES = ("jambe", "tronc", "cou + tête")
OPTIONS_6 = ("a", "b", "d")                   # cheville à 2 axes : empilée, bielles, concourante
CARDAN = 10.0                                 # non-cote: HYPOTHÈSE d'origine, demi-hauteur du cardan (b), non vérifiée


def lire(nom):
    return yaml.safe_load((REPO / "params" / nom).read_text(encoding="utf-8"))


def conventions() -> dict:
    """e, j, v : plaques alu 3 mm de l'opérateur CN, jeu et voile (params, comme le 2026-10-04)."""
    import procedes as PROC
    hw = PROC.charger()
    r = PROC.reglage("operateur_cn_alu_3", hw)
    jeu = lire("squelette.yaml")["ecarts_ansur"]["cheville"]["jeu_mm"]["valeur"]
    return dict(e=r["epaisseur"], j=jeu, v=r["voile_min"], vis=hw["vis"])


def moteur_catalogue(c: dict, cv: dict) -> dict:
    """Un candidat du catalogue : cotes de montage si elles existent (formules du 2026-10-04), sinon Ø × L."""
    cm = c.get("cotes_montage")
    if cm:
        val = lambda x: x.get("valeur") if isinstance(x, dict) else x
        R = (cm.get("diametre_bride") or cm["diametre_corps"]) / 2
        pas = lambda k: cm[k]["diametre_percage"] / 2 + cv["vis"][cm[k]["vis"]]["passage"] / 2 + cv["v"]
        st = "arriere" if cm.get("arriere") else "fixation_boitier"
        return dict(R=R, L=val(cm["longueur"]), r_st=max(cm["diametre_corps"] / 2, pas(st)), r_so=pas("sortie"), cote=True)
    d = c.get("dimensions_mm")
    return moteur_dims(d.get("valeur") if isinstance(d, dict) else d, cv)


def moteur_dims(dims, cv: dict) -> dict | None:
    """Depuis « Ø57 × 51 » (cylindre) ou « 45 × 25 × 35 » (boîtier) ; None si illisible."""
    if not dims:
        return None
    s = str(dims).replace(",", ".").split(";")[0].strip()
    nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", s)]
    if not nums:
        return None
    if s.startswith("Ø") and len(nums) >= 2:
        R, L = nums[0] / 2, nums[1]
    else:
        R, L = max(nums) / 2, max(nums)
    return dict(R=R, L=L, r_st=R, r_so=R / 2 + cv["v"], cote=False)


def cheville(opt, ap, ar, cv):
    """(hauteur de l'axe supérieur de cheville, longueur ajoutée au tibia), formules du 2026-10-04."""
    e, j, v = cv["e"], cv["j"], cv["v"]
    if opt == "c":                                           # 1 axe (fiche 0068)
        return e + j + max(ap["R"], ap["r_st"], ap["r_so"] + j + v), 0.0
    if opt == "a":                                           # empilée
        z_r = e + j + max(ar["R"], ar["r_st"])
        return z_r + ar["R"] + ap["R"] + 2 * j + e, 0.0
    if opt == "d":                                           # concourante, pied à plat
        return max(ap["R"], ar["R"]) + j, 0.0
    if opt == "b":                                           # bielles : deux moteurs empilés dans le tibia
        return e + j + CARDAN, 2 * ap["R"] + j + e + 2 * ar["R"] + j
    raise ValueError(opt)


def chaines(ens: dict, A: dict, opt: str, RA: dict, cv: dict) -> dict:
    """{chaîne: (besoin mm, ratio ANSUR)}. `A` : moteur par rôle ; `ens` : cheville (5|6), taille (axes), bras (5|7), pince."""
    e, j = cv["e"], cv["j"]
    ap = A["ankle_pitch"]
    ar = A.get("ankle_roll", ap)
    K, P, Rr, Y = A["knee"], A["hip_pitch"], A["hip_roll"], A["hip_yaw"]
    Ut, Ub, Uc = A["tronc"], A["bras"], A["cou"]
    h_ank, tib_plus = cheville(opt if ens["cheville"] == 6 else "c", ap, ar, cv)
    seg_cheville = h_ank
    seg_tibia = ap["R"] + j + K["R"] + tib_plus
    seg_cuisse = K["R"] + j + P["R"]
    d_pr = P["R"] + Rr["R"] + 2 * j + e                      # tangage -> roulis de hanche
    hanche = d_pr + Rr["R"] + j + e + Y["L"] + e             # roulis -> lacet vertical -> plaque du bassin
    n_t = ens["taille"]
    if not n_t:
        taille = 0.0
    elif ens.get("taille_concourante"):
        # VARIANTE (phase 4a ter, PROPOSÉE) : axes CONCOURANTS, comme la cheville (d). Les moteurs des axes
        # horizontaux (roulis, tangage) sont déportés le long de LEURS axes, de part et d'autre du point de
        # concours : ils occupent UN étage (2 R + jeu + plaque) au lieu d'en empiler un par axe ; le lacet reste
        # vertical, sous eux. Il faut en échange de la LARGEUR et de la PROFONDEUR dans le tronc (non vérifiées).
        taille = Ut["L"] + j + e + ((2 * Ut["R"] + j + e) if n_t > 1 else 0.0)   # un seul étage, plaque comprise
    else:                                                    # empilée (2026-10-04)
        taille = Ut["L"] + j + e + (n_t - 1) * (2 * Ut["R"] + j + e)
    bassin_taille = max(hanche, d_pr + Rr["R"] + j + taille)
    epaule_haut = Ut["R"] + j + e                            # moteur de tangage d'épaule sous l'acromion
    tronc = bassin_taille + e + epaule_haut
    cou = Uc["L"] + 2 * j + e + Uc["R"]
    d_sh = 2 * Ub["R"] + 2 * j + e
    lacet = Ub["L"] + j + e
    bras = d_sh + Ub["R"] + j + (lacet if ens["bras"] == 7 else 0) + Ub["R"]
    avant_bras = Ub["R"] + j + (lacet if ens["bras"] == 7 else 0) + Ub["R"]
    main = Ub["R"] + j + lacet + (2 * Ub["R"] if ens["pince"] else 0)
    return {
        "jambe": (seg_cheville + seg_tibia + seg_cuisse, RA["hauteur_hanche"]),
        "tronc": (tronc, RA["tronc_hauteur"]),
        "cou + tête": (cou + Uc["R"] + e, RA["cou_hauteur"] + RA["tete_hauteur"]),
        "bras complet": (bras + avant_bras + main, RA["bras"] + RA["avant_bras"] + RA["main_longueur"]),
        "bassin (largeur)": (2 * (max(P["R"], Rr["R"], K["R"]) + j + e), RA["largeur_bassin"]),
    }


def h_min_ansur(ch: dict) -> tuple[float, str]:
    """Proportions strictes : la plus petite H (m) où toutes les chaînes tiennent, et la chaîne limitante."""
    lim = max(ch, key=lambda k: ch[k][0] / ch[k][1])
    return ch[lim][0] / ch[lim][1] / 1000, lim


def hauteur_avec_ecarts(ch: dict, H: float) -> tuple[float, dict]:
    """Avec écarts : hauteur réelle (m) d'un robot aux proportions de H, et les dépassements (mm) des verticales."""
    exc = {k: max(0.0, ch[k][0] - ch[k][1] * H * 1000) for k in VERTICALES}
    return H + sum(exc.values()) / 1000, {k: x for k, x in exc.items() if x > 0}


def evaluer(ens: dict, A: dict, H: float, RA: dict, cv: dict) -> dict:
    """La meilleure option de cheville (hauteur réelle la plus basse) ; les deux lectures."""
    best = None
    for opt in (OPTIONS_6 if ens["cheville"] == 6 else ("c",)):
        ch = chaines(ens, A, opt, RA, cv)
        Hr, exc = hauteur_avec_ecarts(ch, H)
        Ha, lim = h_min_ansur(ch)
        r = dict(option=opt, H_reel=Hr, depassements=exc, H_min_ansur=Ha, limitante_ansur=lim,
                 tient_ansur=Ha <= H + 1e-9, chaines=ch)
        if best is None or Hr < best["H_reel"] - 1e-12:
            best = r
    return best


# ────────────────────── reproduction du 2026-10-04 ──────────────────────
# Ensembles calculés le 2026-10-04 (hmin.py) : 33 et 29 (taille 3), 27, 26.
ENSEMBLES_0410 = {
    33: dict(cheville=6, taille=3, bras=7, pince=True),
    29: dict(cheville=6, taille=3, bras=5, pince=True),
    27: dict(cheville=6, taille=1, bras=5, pince=True),
    26: dict(cheville=5, taille=2, bras=5, pince=True),
}
# Actionneurs retenus le 2026-10-04 (hmin_ecart.py, plus petits qui passaient le couple) ; résultats d'alors :
# 27 -> 0,613 m (tronc +12,9 mm), 26 -> 0,664 m (tronc +63,9 mm), ANSUR stricte 0,642 et 0,809 m.
JAMBE_0410 = {27: dict(hip_pitch="rs00", hip_roll="rs02", hip_yaw="rs02", knee="rs02", ankle_pitch="rs00", ankle_roll="rs05"),
              26: dict(hip_pitch="rs00", hip_roll="rs02", hip_yaw="rs00", knee="rs02", ankle_pitch="rs00")}
ATTENDU_0410 = {27: (0.613, 0.642), 26: (0.664, 0.809)}


def moteurs_robstride(jambe: dict, cv: dict) -> dict:
    cat = lire("actionneurs.yaml")["candidats"]
    A = {k: moteur_catalogue(cat[v], cv) for k, v in jambe.items()}
    u = moteur_catalogue(cat["rs05"], cv)
    A.update(tronc=u, bras=u, cou=u)
    return A


def gain_taille_concourante(cv, RA, H=0.60) -> list[dict]:
    """Tronc et hauteur réelle, taille empilée ou concourante, pour les ensembles à taille de 2 ou 3 axes."""
    out = []
    for k, jb in ((29, JAMBE_0410[27]), (33, JAMBE_0410[27]), (26, JAMBE_0410[26])):
        ens = ENSEMBLES_0410[k]
        A = moteurs_robstride(jb, cv)
        r_e = evaluer(ens, A, H, RA, cv)
        r_c = evaluer(dict(ens, taille_concourante=True), A, H, RA, cv)
        te, tc = r_e["chaines"]["tronc"][0], r_c["chaines"]["tronc"][0]
        out.append(dict(ensemble=k, taille=ens["taille"], tronc_empile=te, tronc_concourant=tc, gain=te - tc,
                        H_empile=r_e["H_reel"], H_concourant=r_c["H_reel"], ansur=RA["tronc_hauteur"] * H * 1000))
    return out


def main() -> int:
    cv = conventions()
    RA = {k: x["valeur"] for k, x in lire("anthropometry.yaml")["ratios"].items()}
    cfg = lire("configuration_S.yaml")["jambes"]
    jambes = {**JAMBE_0410, "26 (configuration_S)": {("hip_yaw" if k == "hip_yaw_drive" else k): v for k, v in cfg.items()}}
    print(f"  conventions : plaques {cv['e']:g} mm, jeu {cv['j']:g} mm, voile {cv['v']:g} mm ; haut du corps en RS05")
    print("\n  | Ensemble | Jambes | Option | Hauteur réelle à 0,60 (avec écarts) | Dépassements (mm) | H min ANSUR stricte |")
    print("  | ---: | --- | --- | ---: | --- | ---: |")
    for k, jb in jambes.items():
        r = evaluer(ENSEMBLES_0410[int(str(k)[:2])], moteurs_robstride(jb, cv), 0.60, RA, cv)
        print(f"  | {k} | {', '.join(f'{a} {b}' for a, b in jb.items())} | ({r['option']}) | {r['H_reel']:.3f} m | "
              f"{', '.join(f'{a} +{x:.0f}' for a, x in r['depassements'].items()) or '—'} | "
              f"{r['H_min_ansur']:.3f} m ({r['limitante_ansur']}) |"
              + (f" 2026-10-04 : {ATTENDU_0410[k][0]} / {ATTENDU_0410[k][1]} m" if k in ATTENDU_0410 else ""))
    print("\n  Taille à axes CONCOURANTS (variante PROPOSÉE, pour le final) : tronc nécessaire (mm), RS05 au buste")
    print("  | Ensemble | Axes de taille | Empilée | Concourante | Gain | Hauteur réelle à 0,60 : empilée → concourante |")
    print("  | ---: | ---: | ---: | ---: | ---: | --- |")
    for g in gain_taille_concourante(cv, RA):
        print(f"  | {g['ensemble']} | {g['taille']} | {g['tronc_empile']:.0f} | {g['tronc_concourant']:.0f} | "
              f"−{g['gain']:.0f} | {g['H_empile']:.3f} → {g['H_concourant']:.3f} m (ANSUR {g['ansur']:.0f} mm) |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
