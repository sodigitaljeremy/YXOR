#!/usr/bin/env python3
"""Masse de la structure en plaques, segment par segment, en six variantes.

    .venv/bin/python scripts/structure_plaques.py          # tableau par segment et par variante

Versé dans le dépôt le 2026-10-07. Règle de Jeremy du même jour (« Je valide :
toute étude citée dans une décision ou réutilisée par un calcul vit dans le
dépôt, avec un test. »). RECONSTRUCTION de deux études de session jamais
versées, retrouvées dans la transcription de la session (accès accordé par
Jeremy le 2026-10-07, ce dossier seulement) :
  · etude_s.py (2026-10-03, 23 h) et evidable.py : masse réaliste en plaques ;
  · etude_s_c.py (2026-10-04, 20 h 33) : la même, la jambe basse étant celle
    de la fiche 0068 (cheville sans roulis). Sorties d'alors : v3 pleine
    3,92 kg, évidée 50 % + 2 mm 1,85 kg (le test les compare).

MÉTHODE (celle des études d'origine, inchangée) :
  · jambe basse : la CAO ACTUELLE (parts/jambe_basse.py), plaques alu 3 mm,
    sans la chape du genou (comptée avec la cuisse) ;
  · autres segments : même architecture (caissons, liaisons à 90°, boîtes),
    aux longueurs ANSUR à H_S. Aires par formules, ÉTALONNÉES sur la CAO : le
    caisson sur le tibia et la liaison sur la cheville A/B/C de l'option (a),
    qui n'existe plus que dans l'historique (commit 0b5e304, extrait par
    `git archive` dans un dossier temporaire, avec les paramètres d'alors) ;
  · évidement : plafonné, plaque par plaque, par la part RÉELLEMENT évidable
    (points à au moins un voile de tout bord, trou ou mortaise), mesurée sur la
    CAO ; une seule poche par plaque, sans nervure : borne HAUTE ;
  · 2 mm : sur les plaques peu chargées (tronc, tête, bras, avant-bras,
    mains) ; épaisseur NON confirmée chez l'opérateur.
HYPOTHÈSES d'origine, conservées et dites : boîte évidable à 50 % ; trous des
boîtes 5 % (K_BOITE) ; vis, paliers, câbles et pince non comptés ; plaques
dimensionnées pour RS00, RS02 et RS05 (cotes du catalogue), quel que soit
l'actionneur choisi ensuite.

Mesures CAO mises en cache dans exports/etudes/ (ignoré, régénérable), par
empreinte des sources : la mesure d'évidement prend une à deux minutes.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import math
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
CACHE = REPO / "exports" / "etudes" / "structure_cao.json"
COMMIT_A = "0b5e304"        # dernière CAO de la jambe basse à cheville (a), liaison A/B/C (2026-10-04)
REGLAGE = "operateur_cn_alu_3"
DENS = 2.70e-3              # non-cote: g/mm³, alu (GLEICH, registre ; hardware.yaml la porte aussi)
VARIANTES = [("pleine 3 mm", 0.0, False), ("évidée 30 %", 0.30, False), ("évidée 50 %", 0.50, False),
             ("2 mm peu chargées", 0.0, True), ("évidée 30 % + 2 mm", 0.30, True), ("évidée 50 % + 2 mm", 0.50, True)]
K_BOITE = 0.95              # HYPOTHÈSE d'origine : trous de fixation des boîtes, 5 %
EVID_BOITE = 0.50           # HYPOTHÈSE d'origine : faces portant des moteurs, entre liaison et paroi
EP_MINCE = 2.0              # non-cote: épaisseur des plaques peu chargées (mm), PROPOSÉE, non confirmée


def lire(nom):
    return yaml.safe_load((REPO / "params" / nom).read_text(encoding="utf-8"))


# ─────────────────────────────── mesure CAO ─────────────────────────────
def evidable(jb, pas=1.5) -> dict:
    """Par plaque : masse (g), part évidable (points à ≥ un voile de tout bord), aire. Grille de `pas` mm."""
    import build123d as bd
    from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape
    from OCP.gp import gp_Pnt
    g = jb.donnees(REGLAGE)
    G = jb.geometrie(g)
    out = {}
    for pl in jb.plaques_structure(g, G):
        pl.finir(g["e"], g["d_min"])
        f = pl.face.faces()[0]
        bord = bd.Compound([f.outer_wire(), *f.inner_wires()])
        bb = f.bounding_box()
        n_in = n_ok = 0
        x = bb.min.X + pas / 2
        while x < bb.max.X:
            y = bb.min.Y + pas / 2
            while y < bb.max.Y:
                if pl.solide.is_inside(bd.Vector(x, y, g["e"] / 2)):
                    n_in += 1
                    d = BRepExtrema_DistShapeShape(BRepBuilderAPI_MakeVertex(gp_Pnt(x, y, 0)).Vertex(), bord.wrapped)
                    if d.Value() >= g["v"]:
                        n_ok += 1
                y += pas
            x += pas
        out[pl.nom] = dict(evidable=n_ok / n_in, masse_g=pl.solide.volume * len(pl.poses) * DENS, aire=f.area)
    return out


def _module(racine: Path):
    """parts/jambe_basse.py de l'arbre `racine`, importé avec SES paramètres (un import par arbre)."""
    for m in ("jambe_basse", "squelette", "dimensionnement", "procedes", "plan_decoupe", "choix_actionneurs",
              "analyser_marche"):
        sys.modules.pop(m, None)
    sys.path[:0] = [str(racine / "parts"), str(racine / "scripts")]
    try:
        return importlib.import_module("jambe_basse")
    finally:
        del sys.path[:2]


def _empreinte() -> str:
    h = hashlib.sha256(COMMIT_A.encode())
    for f in ("parts/jambe_basse.py", "params/hardware.yaml", "params/actionneurs.yaml", "params/squelette.yaml",
              "params/anthropometry.yaml"):
        h.update((REPO / f).read_bytes())
    return h.hexdigest()[:16]


def mesures_cao(rafraichir=False) -> dict:
    """{'c': plaques de la CAO actuelle, 'a': plaques de la CAO (a) du commit 0b5e304, 'g_a': cotes (a)}."""
    emp = _empreinte()
    if CACHE.exists() and not rafraichir:
        d = json.loads(CACHE.read_text(encoding="utf-8"))
        if d.get("empreinte") == emp:
            return d
    with tempfile.TemporaryDirectory() as tmp:
        arch = Path(tmp) / "a.tar"
        with arch.open("wb") as fh:
            subprocess.run(["git", "archive", COMMIT_A, "parts", "scripts", "params"], cwd=REPO, stdout=fh, check=True)
        with tarfile.open(arch) as t:
            t.extractall(Path(tmp) / "a", filter="data")
        jba = _module(Path(tmp) / "a")
        ga = jba.donnees(REGLAGE)
        Ga = jba.geometrie(ga)
        mesure_a = evidable(jba)
        g_a = dict(T=ga["T"], e=ga["e"], j=ga["j"], v=ga["v"], y_te=Ga["y_te"], L0=Ga["L0"])
    jbc = _module(REPO)
    d = dict(empreinte=emp, c=evidable(jbc), a=mesure_a, g_a=g_a)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(d, indent=1, ensure_ascii=False), encoding="utf-8")
    return d


# ─────────────────────────────── formules ───────────────────────────────
def hull(r1, r2, L):
    return math.pi * (r1 ** 2 + r2 ** 2) / 2 + L * (r1 + r2)


def caisson(r1, r2, L, w_int):
    return dict(cote=2 * hull(r1, r2, L), paroi=2 * w_int * max(L - r1 - r2, 0))


def liaison(r1, r2):
    return dict(liaison=3.57 * r1 ** 2 + 3.57 * r2 ** 2 + (r1 + r2) ** 2)


def boite(a, b, c):
    return dict(boite=2 * (a * b + b * c + c * a))


def modele(cao=None) -> dict:
    """Étalonnages, parts évidables et segments (aires en mm², à H_S)."""
    cao = cao or mesures_cao()
    an, cat, hw = lire("anthropometry.yaml"), lire("actionneurs.yaml")["candidats"], lire("hardware.yaml")
    H = an["tailles"]["S"]["H_m"]
    R = lambda k: an["ratios"][k]["valeur"] * H * 1000
    ga = cao["g_a"]
    e, j, v = ga["e"], ga["j"], ga["v"]
    rho_e = DENS * e
    vis = hw["vis"]

    def rplat(cid, motif):
        cm = cat[cid]["cotes_montage"]
        m = cm[motif]
        r = m["diametre_percage"] / 2 + vis[m["vis"]]["passage"] / 2 + v
        return max(cm["diametre_corps"] / 2 if motif != "sortie" else 0, r)

    r00_st, r00_so = rplat("rs00", "arriere"), rplat("rs00", "sortie")
    r02_st, r02_so = rplat("rs02", "fixation_boitier"), rplat("rs02", "sortie")
    r05_st, r05_so = rplat("rs05", "arriere"), rplat("rs05", "sortie")
    L05 = cat["rs05"]["cotes_montage"]["longueur"]["valeur"]
    A, C = cao["a"], cao["c"]
    # étalonnages sur la CAO (a) : tibia (caisson) et liaison de cheville A/B/C
    m_tib = sum(A[k]["masse_g"] for k in ("tibia_exterieur", "tibia_interieur", "tibia_paroi"))
    w_tib = ga["y_te"] - (-ga["L0"] / 2 - e - j)
    k_caisson = m_tib / (rho_e * sum(caisson(r00_so, r02_st, ga["T"], w_tib).values()))
    m_lia = sum(A[k]["masse_g"] for k in ("cheville_A", "cheville_B", "cheville_C"))
    k_liaison = m_lia / (rho_e * liaison(r00_st, r00_st)["liaison"])
    pond = lambda ks: sum(A[k]["evidable"] * A[k]["masse_g"] for k in ks) / sum(A[k]["masse_g"] for k in ks)
    evid = dict(cote=pond(["tibia_exterieur", "tibia_interieur"]), paroi=A["tibia_paroi"]["evidable"],
                liaison=pond(["cheville_A", "cheville_B", "cheville_C"]), boite=EVID_BOITE)
    w_cuisse = 2 * (e + j) + w_tib + e
    seg = {   # nom : (nombre, aires par catégorie, ou "cao" ; peu chargé)
        "jambe basse (CAO actuelle, sans chape)": (2, "cao", False),
        "cuisse (caisson + 2 entretoises)": (2, {**caisson(r02_so, r02_so, R("cuisse"), w_cuisse),
                                                  "entretoise": 2 * math.pi * r02_so ** 2}, False),
        "hanche (2 liaisons)": (2, {"liaison": liaison(r00_so, r02_st)["liaison"] + liaison(r02_so, r02_st)["liaison"]}, False),
        "bassin (boîte)": (1, boite(R("largeur_bassin") + 2 * r00_st, 2 * r00_st + 2 * v,
                                     cat["rs00"]["cotes_montage"]["longueur"]["valeur"] + 2 * e + 2 * j), False),
        "tronc (boîte)": (1, boite(0.8 * R("largeur_epaules"), max(1.5 * R("pied_largeur"), 2 * r05_st + 2 * e),
                                    R("tronc_hauteur")), True),
        "tête (boîte)": (1, boite(0.9 * R("tete_hauteur"), 0.8 * R("tete_hauteur"), R("tete_hauteur")), True),
        "taille (liaison RS05)": (1, liaison(r05_st, r05_st), False),
        "épaule (liaison RS05)": (2, liaison(r05_st, r05_st), False),
        "bras (caisson)": (2, caisson(r05_so, r05_st, R("bras"), L05 + e + j), True),
        "avant-bras (caisson)": (2, caisson(r05_so, r05_so, R("avant_bras"), L05 + e + j), True),
        "poignet (liaison RS05)": (2, liaison(r05_st, r05_st), False),
        "main (caisson, pince non comptée)": (2, caisson(r05_so, r05_st, R("main_longueur"), L05 + e + j), True),
        "cou (liaison RS05)": (1, liaison(r05_st, r05_st), False),
        # ajouts pour les autres ensembles (même méthode)
        "axe RS05 de plus (liaison)": (1, liaison(r05_st, r05_st), False),
        "roulis de cheville (liaison RS00, 2 jambes)": (2, liaison(r00_st, r00_st), False),
    }
    jb = {k: x for k, x in C.items() if not k.startswith("genou")}
    return dict(seg=seg, jb=jb, rho_e=rho_e, evid=evid, H_S=H, e=e,
                K=dict(cote=k_caisson, paroi=k_caisson, liaison=k_liaison, boite=K_BOITE, entretoise=1.0))


V1 = ["jambe basse (CAO actuelle, sans chape)", "cuisse (caisson + 2 entretoises)", "hanche (2 liaisons)",
      "bassin (boîte)", "tronc (boîte)", "tête (boîte)"]
V3 = V1 + ["taille (liaison RS05)", "épaule (liaison RS05)", "bras (caisson)", "avant-bras (caisson)",
           "poignet (liaison RS05)", "main (caisson, pince non comptée)", "cou (liaison RS05)"]


def masse_segment(m, nom, f_evid, deux_mm) -> float:
    """Masse (g) du segment, toutes ses occurrences."""
    n, spec, leger = m["seg"][nom]
    ep = EP_MINCE / m["e"] if (deux_mm and leger) else 1.0
    if spec == "cao":
        return n * sum(x["masse_g"] * (1 - min(f_evid, x["evidable"])) for x in m["jb"].values())
    tot = 0.0
    for c, aire in spec.items():
        ev = 0.0 if c == "entretoise" else min(f_evid, m["evid"][c])
        tot += m["K"][c] * m["rho_e"] * aire * (1 - ev) * ep
    return n * tot


def variante(nom):
    return next(v for v in VARIANTES if v[0] == nom)


def structure(m, nom_variante, segments=V3, n_rs05_de_plus=0, roulis_cheville=False) -> float:
    """Masse (kg) d'une structure, à H_S. `n_rs05_de_plus` : axes du haut au-delà de la v3 (négatif : en moins)."""
    _, f, d2 = variante(nom_variante)
    g = sum(masse_segment(m, s, f, d2) for s in segments)
    g += n_rs05_de_plus * masse_segment(m, "axe RS05 de plus (liaison)", f, d2)
    if roulis_cheville:
        g += masse_segment(m, "roulis de cheville (liaison RS00, 2 jambes)", f, d2)
    return g / 1000


def main() -> int:
    m = modele()
    print(f"  étalonnage (CAO (a), commit {COMMIT_A}) : caisson k = {m['K']['cote']:.2f}, liaison k = "
          f"{m['K']['liaison']:.2f} ; évidable : côté {m['evid']['cote']:.0%}, paroi {m['evid']['paroi']:.0%}, "
          f"liaison {m['evid']['liaison']:.0%}, boîte {m['evid']['boite']:.0%} (hypothèse)")
    print(f"  {len(m['jb'])} plaques de jambe basse (CAO actuelle), {len(m['seg'])} segments")
    print("\n  | Segment | n | pleine 3 mm (g) | évidée 50 % + 2 mm (g) |\n  | --- | ---: | ---: | ---: |")
    for s in m["seg"]:
        print(f"  | {s} | {m['seg'][s][0]} | {masse_segment(m, s, 0, False):.0f} | {masse_segment(m, s, 0.5, True):.0f} |")
    print("\n  | Variante | v1 (kg) | v3 (kg) |\n  | --- | ---: | ---: |")
    for nv, _, _ in VARIANTES:
        print(f"  | {nv} | {structure(m, nv, V1):.2f} | {structure(m, nv):.2f} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
