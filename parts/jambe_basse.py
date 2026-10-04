#!/usr/bin/env python3
"""Jambe basse de S en plaques planes : pied, cheville (1 axe, fiche 0068), tibia, genou.

    .venv/bin/python parts/jambe_basse.py                 # pièces, DXF, plans A4, STEP, contrôles, masse
    .venv/bin/python parts/jambe_basse.py --collisions    # + balayage des butées (lent, ~1 min)
    .venv/bin/python parts/jambe_basse.py --rendu         # + image de contrôle (MuJoCo, hors écran)

Créé le 2026-10-03. Intention de Jeremy (2026-10-02) : passer à la pratique,
carton d'abord, puis la même chose en découpe 2D métal. Ce n'est pas une
décision d'architecture : c'est une maquette, et un banc d'essai du « tout
en 2D ».

═══════════════════════════════════════════════════════════════════════
 CE QUE LE CODE DESSINE (jambe GAUCHE ; x avant, y gauche, z haut)
═══════════════════════════════════════════════════════════════════════

  pied        (fiche 0068 : cheville SANS roulis, 5 axes par jambe) une
              semelle élargie (écart ANSUR du squelette) et une CHAPE qui
              enjambe le tibia, comme celle du genou : une entretoise sur la
              sortie du RS00, un montant extérieur boulonné dessus, un montant
              intérieur en pivot, tous deux tenonnés dans la semelle.
  tibia       CAISSON : deux plaques latérales (⟂ y) et deux parois (⟂ x)
              tenonnées dans des mortaises. La plaque intérieure tient le
              STATOR du RS00 de la cheville par l'arrière ; l'extérieure a une
              ouverture pour sa sortie en bas et porte la bride du RS02 du
              genou en haut.
  genou       la CHAPE du RS02 : une entretoise sur la sortie, une plaque
              avant boulonnée dessus, une plaque arrière en pivot, et un
              dessus tenonné qui recevra la cuisse.
  factices    (carton seulement) des factices RONDS aux cotes des RS00 et RS02
              (STEP officiels) : disques avant et arrière percés, un DISQUE
              ROTOR libre dans la face avant, tenu par un axe M3 traversant,
              et une BANDE de papier fort enroulée sur les disques. Les
              boîtes carrées du 2026-10-03 limitaient la maquette à ±5°.

Un TENON est une languette qui dépasse du bord d'une plaque ; une MORTAISE
est la fente qui le reçoit ; une ENCOCHE est une mortaise ouverte sur un
bord. Aucun angle rentrant ne reste vif : chaque coin rentrant d'un tenon,
d'une mortaise ou d'une encoche est dégagé par un cercle de rayon
`rayon_interieur_min` du réglage centré sur le coin (« os de chien »), ce
qui laisse le tenon carré entrer à fond.

═══════════════════════════════════════════════════════════════════════
 D'OÙ VIENNENT LES COTES
═══════════════════════════════════════════════════════════════════════

  · les AXES : le squelette (params/squelette.yaml, scripts/squelette.py),
    écarts ANSUR de la cheville compris — une seule cinématique pour tous
    les réglages ;
  · les longueurs d'échelle : H_S × ratios (règle 1) ;
  · les moteurs et leurs perçages : params/actionneurs.yaml (cotes_montage),
    les vis : params/hardware.yaml (règle 2) ;
  · l'épaisseur, le rayon, le trou minimal : le réglage (hardware.yaml) ;
  · le voile et le jeu : squelette.ecarts_cheville (le plus fort des voiles
    déclarés ; jeu PROPOSÉ) ; la largeur d'un tenon : 2 × voile (PROPOSÉ).

FACES ET PHASES (lues le 2026-10-03 dans les STEP officiels, params/
actionneurs.yaml) : la fixation du boîtier du RS00 est sur la face AVANT,
avec la sortie ; le tibia tient donc le RS00 par l'ARRIÈRE (4 × M3 sur Ø38,
`motif_stator` du squelette). Le RS02 se fixe par l'avant (9 × M3 sur Ø73).
Les trous de centrage ne sont pas dessinés.

Un trou plus petit que le minimum découpable du réglage n'est PAS découpé :
il est MARQUÉ (calque POINTAGE du DXF, croix sur le plan A4), à pointer puis
percer au foret. Ne produit pas de relevé `.origines.yaml` : pas de page sur
le site. Sorties dans exports/parts/ (préfixe jambe_basse_) et
exports/jambe_basse/ (rendu).
"""
from __future__ import annotations

import argparse
import importlib.util
import math
import sys
import time
from pathlib import Path

import build123d as bd
import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import procedes as PROC  # noqa: E402
import squelette as SQ  # noqa: E402
from plan_decoupe import ZONE_PLANCHE, ecrire_planches_a4, polylignes_depuis_face  # noqa: E402

NOM = "jambe_basse"
SORTIE = REPO / "exports" / "parts"
RENDU = REPO / "exports" / NOM
REGLAGES = ("cutter_cartonplume_5", "operateur_cn_alu_3")
REGLAGE_CARTON = "cutter_cartonplume_5"   # le seul qui reçoit les factices et le plan A4
ECART_PLAN = 4.0          # non-cote: espace entre deux pièces sur une planche A4
CROIX = 1.5               # non-cote: demi-branche d'une croix de pointage
VOL_MIN = 0.5             # non-cote: mm³ ; une intersection plus petite est un artefact numérique
PAS_DEG = 5               # non-cote: pas du balayage des butées
DELTA = 0.05              # non-cote: mm ; rayon de sondage autour d'un sommet
EP_BANDE = 0.3            # non-cote: représentation 3D du papier de la bande, sans effet sur les plans
RECOUVREMENT = 10.0       # non-cote: languette de recouvrement d'une bande de papier, collée ou scotchée


def lire(nom: str) -> dict:
    return yaml.safe_load((REPO / "params" / nom).read_text(encoding="utf-8"))


def val(x):
    return x["valeur"] if isinstance(x, dict) else x


# ─────────────────────────────────────────────────────── primitives 2D
def rect(x0, x1, y0, y1):
    return bd.Pos((x0 + x1) / 2, (y0 + y1) / 2) * bd.Rectangle(x1 - x0, y1 - y0)


def disque(cx, cy, r):
    return bd.Pos(cx, cy) * bd.Circle(r)


def os_de_chien(coins, r):
    """Un cercle de rayon r sur chaque coin rentrant : aucun angle vif ne reste."""
    out = None
    for x, y in coins:
        c = disque(x, y, r)
        out = c if out is None else out + c
    return out


def degagement(centres, r):
    """Dégagement en T : cercle de rayon r TANGENT au bord qu'on veut garder droit.

    Un cercle centré sur le coin (os_de_chien) mord sur les deux bords : à la
    racine d'un tenon de 3 mm, il laisse un crochet de 1 mm (contrôle du voile,
    2026-10-03). Ici le centre est décalé d'un rayon le long de l'autre bord :
    le tenon, ou la paroi d'une encoche, reste entier.
    """
    return os_de_chien(centres, r)


def motif(cm: dict, cle: str, vis: dict, cx=0.0, cy=0.0) -> list[tuple]:
    """Les trous de passage d'un motif publié (n vis sur un cercle), premier trou à `phase_deg`.

    Phase lue dans le STEP officiel (params/actionneurs.yaml, 2026-10-03) ;
    0° si elle manque. Une plaque vue de l'autre face voit le motif en miroir :
    tous les motifs de ce fichier sont posés dans le repère de leur plaque.
    """
    m = cm.get(cle)
    if not m or "diametre_percage" not in m:
        return []
    r, d = m["diametre_percage"] / 2, vis[m["vis"]]["passage"]
    a0 = math.radians(m.get("phase_deg") or 0.0)
    return [(cx + r * math.cos(a0 + 2 * math.pi * i / m["nombre"]),
             cy + r * math.sin(a0 + 2 * math.pi * i / m["nombre"]), d) for i in range(m["nombre"])]


def rayon_motif(cm, cle, vis, voile):
    """Rayon d'une plaque qui couvre un motif avec un voile autour des trous."""
    m = cm[cle]
    return m["diametre_percage"] / 2 + vis[m["vis"]]["passage"] / 2 + voile


# Plans de pose : une esquisse dessinée dans XY, extrudée de e vers +Z, est
# posée par une Location. Chacun occupe [a, a + e] le long de sa normale.
def plan_y(y0, e):
    return bd.Location(bd.Plane(origin=(0, y0 + e, 0), x_dir=(1, 0, 0), z_dir=(0, -1, 0)))


def plan_x(x0):   # u = y, v = z
    return bd.Location(bd.Plane(origin=(x0, 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0)))


def plan_z(z0):   # u = x, v = y
    return bd.Location(bd.Plane(origin=(0, 0, z0), x_dir=(1, 0, 0), z_dir=(0, 0, 1)))


class Plaque:
    """Une pièce plane : esquisse (XY), trous, poses (une par exemplaire)."""

    def __init__(self, nom, esquisse, trous, poses, groupes, role, factice=False):
        self.nom, self.esq, self.trous, self.poses = nom, esquisse, trous, poses
        self.groupes = groupes if isinstance(groupes, list) else [groupes] * len(poses)
        self.role, self.factice = role, factice

    def finir(self, e, d_min):
        """Découpe les trous découpables, MARQUE les autres. Rend la face finale."""
        self.coupes = [t for t in self.trous if t[2] >= d_min - 1e-9]
        self.marques = [t for t in self.trous if t[2] < d_min - 1e-9]
        f = self.esq
        for x, y, d in self.coupes:
            f = f - disque(x, y, d / 2)
        self.face = f
        faces = f.faces()
        if len(faces) != 1:
            raise ValueError(f"{self.nom} : {len(faces)} morceaux au lieu d'une pièce d'un seul tenant")
        self.solide = bd.extrude(f, amount=e)
        bb = faces[0].bounding_box()
        self.dims = (bb.size.X, bb.size.Y, e)
        return self


# ─────────────────────────────────────────────────────── géométrie
def donnees(rid: str) -> dict:
    """Toutes les entrées, lues dans params/ : rien n'est écrit ici en millimètres."""
    hw = PROC.charger()
    r = PROC.reglage(rid, hw)
    e = r["epaisseur"]
    r_min = PROC.rayon_interieur_min(e, r.get("rayon_interieur_min_machine"))
    d_min = r.get("trou_decoupe_min") or 2 * r_min
    ec = SQ.ecarts_cheville()
    an = lire("anthropometry.yaml")
    H = an["tailles"]["S"]["H_m"]
    cat = lire("actionneurs.yaml")["candidats"]
    cfg = lire("configuration_S.yaml")["jambes"]
    m_cheville, m_genou = cfg["ankle_pitch"], cfg["knee"]
    return dict(rid=rid, reg=r, hw=hw, vis=hw["vis"], e=e, r=r_min, d_min=d_min,
                v=ec["voile_mm"], j=ec["jeu_mm"], t=2 * ec["voile_mm"],
                z_p=ec["hauteur_axe_cheville"] * 1000, W_pied=ec["largeur_pied"] * 1000,
                T=SQ.longueur({"tibia": 1.0}, an["ratios"], H) * 1000, H=H,
                c0=cat[m_cheville]["cotes_montage"], c2=cat[m_genou]["cotes_montage"],
                m_cheville=m_cheville, m_genou=m_genou, cat=cat, ec=ec,
                ec_brut=lire("squelette.yaml")["ecarts_ansur"]["cheville"])


def geometrie(g: dict) -> dict:
    """Les grandeurs dérivées, en mm, nommées une fois. Cheville sans roulis (fiche 0068)."""
    e, j, v, r, t = g["e"], g["j"], g["v"], g["r"], g["t"]
    c0, c2, vis = g["c0"], g["c2"], g["vis"]
    L0, R0 = val(c0["longueur"]), c0["diametre_corps"] / 2
    L2, R2 = val(c2["longueur"]), c2["diametre_corps"] / 2
    Rb2 = (c2.get("diametre_bride") or c2["diametre_corps"]) / 2
    z_p = g["z_p"]
    z_k = z_p + g["T"]
    r_so0 = rayon_motif(c0, "sortie", vis, v)            # entretoise et montant sur la sortie du RS00
    r_so2 = rayon_motif(c2, "sortie", vis, v)            # idem RS02
    r_br2 = rayon_motif(c2, "fixation_boitier", vis, v)  # plaque sous la bride du RS02
    G = dict(L0=L0, R0=R0, L2=L2, R2=R2, Rb2=Rb2, z_p=z_p, z_k=z_k,
             r_tb=g["ec"]["r_plaque_mm"],               # bas des plaques du tibia, autour du tangage
             r_so0=r_so0, r_so2=r_so2, r_br2=r_br2,
             rotor0=2 * r_so0, rotor2=2 * r_so2,
             y_te=L0 / 2 + j,                            # face intérieure de la plaque extérieure du tibia
             y_ti=-L0 / 2 - e,                           # plaque intérieure = plaque du STATOR du RS00
             h_dessus=max(r_br2, Rb2) + j)
    # parois du caisson : entre le RS00 du tangage (fixe dans le tibia) et la bride du genou
    G["zw0"] = z_p + R0 + j
    G["zw1"] = z_k - Rb2 - j
    Hw = G["zw1"] - G["zw0"]
    marge = t / 2 + 2 * r + v                            # du centre d'un tenon au bord de la paroi
    G["zm"] = (G["zw0"] + marge, G["zw1"] - marge)
    if Hw < 2 * marge + t:
        raise ValueError(f"paroi du tibia trop courte ({Hw:.1f} mm) pour deux tenons")
    z_bas_mortaise = G["zm"][0] - t / 2 - r
    demi_largeur = G["r_tb"] + (r_br2 - G["r_tb"]) * (z_bas_mortaise - z_p) / g["T"]   # tangente intérieure : prudent
    G["x_w"] = demi_largeur - v - r - e / 2
    return G


def plaques_structure(g, G) -> list[Plaque]:
    e, j, v, r, t, vis = g["e"], g["j"], g["v"], g["r"], g["t"], g["vis"]
    c0, c2 = g["c0"], g["c2"]
    L0, R0, z_p, z_k = G["L0"], G["R0"], G["z_p"], G["z_k"]
    axe = vis["M3"]["passage"]           # axe de maquette : une vis M3 traversante
    P = []

    # ── pied : une CHAPE qui enjambe le tibia (fiche 0068) ───────────────
    # Semelle : longueur ANSUR, largeur = écart ANSUR du squelette (la chape
    # enjambe le tibia), axe de cheville à 25 % de la longueur depuis le talon
    # (HYPOTHÈSE, malléole humaine), coins arrondis au quart de la largeur
    # ANSUR (choix, comme la semelle d'apprentissage). Plus de creux : il
    # croiserait les mortaises des montants.
    an = lire("anthropometry.yaml")
    Lp = SQ.longueur({"pied_longueur": 1.0}, an["ratios"], g["H"]) * 1000
    Wa = SQ.longueur({"pied_largeur": 1.0}, an["ratios"], g["H"]) * 1000
    W = g["W_pied"]
    semelle = bd.Sketch() + bd.Pos(Lp / 4, 0) * bd.RectangleRounded(Lp, W, 0.25 * Wa)
    y_me = G["y_te"] + e + j                                    # montant extérieur : [y_me, y_me + e]
    y_mi = G["y_ti"] - j - e                                    # montant intérieur (pivot)
    for y0 in (y_me, y_mi):
        semelle = semelle - rect(-t / 2, t / 2, y0, y0 + e) - os_de_chien(
            [(-t / 2, y0), (t / 2, y0), (-t / 2, y0 + e), (t / 2, y0 + e)], r)
    P.append(Plaque("pied_semelle", semelle, [], [plan_z(0)], "pied", "semelle élargie (écart ANSUR), deux mortaises"))

    def montant():
        s = disque(0, z_p, G["r_so0"]) + rect(-G["r_so0"], G["r_so0"], e, z_p)
        s = s + rect(-t / 2, t / 2, 0, e)                       # tenon vers la semelle
        return s - degagement([(-t / 2 - r, e), (t / 2 + r, e)], r)
    P.append(Plaque("pied_entretoise", disque(0, z_p, G["r_so0"]),
                    motif(c0, "sortie", vis, 0, z_p) + [(0, z_p, axe)],
                    [plan_y(G["y_te"], e)], "pied", "sur la sortie du RS00, dans l'ouverture du tibia"))
    P.append(Plaque("pied_montant_exterieur", montant(), motif(c0, "sortie", vis, 0, z_p) + [(0, z_p, axe)],
                    [plan_y(y_me, e)], "pied", "sur l'entretoise (rondelles : jeu axial)"))
    P.append(Plaque("pied_montant_interieur", montant(), [(0, z_p, axe)],
                    [plan_y(y_mi, e)], "pied", "pivot de la cheville (palier à reprendre)"))

    # ── tibia ─────────────────────────────────────────────────────────
    profil = bd.Sketch() + bd.make_hull((disque(0, z_p, G["r_tb"]) + disque(0, z_k, G["r_br2"])).edges())
    mort = None
    for xw in (-G["x_w"], G["x_w"]):
        for zm in G["zm"]:
            x0, x1, y0, y1 = xw - e / 2, xw + e / 2, zm - t / 2, zm + t / 2
            m = rect(x0, x1, y0, y1) + os_de_chien([(x0, y0), (x0, y1), (x1, y0), (x1, y1)], r)
            mort = m if mort is None else mort + m
    ext = profil - mort - disque(0, z_k, G["rotor2"] / 2 + j) - disque(0, z_p, G["rotor0"] / 2 + j)
    P.append(Plaque("tibia_exterieur", ext, motif(c2, "fixation_boitier", vis, 0, z_k),
                    [plan_y(G["y_te"], e)], "tibia", "ouverture de la cheville en bas, bride du RS02 en haut"))
    face_stator = g["ec_brut"]["motif_stator"]                 # l'arrière du RS00 (STEP officiel)
    P.append(Plaque("tibia_interieur", profil - mort,
                    motif(c0, face_stator, vis, 0, z_p) + [(0, z_p, axe), (0, z_k, axe)],
                    [plan_y(G["y_ti"], e)], "tibia", "stator du RS00 de la cheville ; pivot du genou"))
    ya, yb = G["y_ti"] + e, G["y_te"]                            # faces intérieures du caisson
    paroi = rect(ya, yb, G["zw0"], G["zw1"])
    for zm in G["zm"]:
        paroi = paroi + rect(yb, yb + e, zm - t / 2, zm + t / 2) + rect(ya - e, ya, zm - t / 2, zm + t / 2)
        paroi = paroi - degagement([(yb, zm - t / 2 - r), (yb, zm + t / 2 + r),
                                    (ya, zm - t / 2 - r), (ya, zm + t / 2 + r)], r)
    P.append(Plaque("tibia_paroi", paroi, [], [plan_x(-G["x_w"] - e / 2), plan_x(G["x_w"] - e / 2)],
                    "tibia", "paroi du caisson (avant et arrière)"))

    # ── chape du genou ────────────────────────────────────────────────
    hd = G["h_dessus"]
    rc = max(G["r_so2"], t / 2 + r + v)
    P.append(Plaque("genou_entretoise", disque(0, z_k, G["rotor2"] / 2),
                    motif(c2, "sortie", vis, 0, z_k) + [(0, z_k, axe)],
                    [plan_y(G["y_te"], e)], "cuisse", "sur la sortie du RS02, dans l'ouverture du tibia"))

    def chape():
        s = disque(0, z_k, rc) + rect(-rc, rc, z_k, z_k + hd)
        s = s + rect(-t / 2, t / 2, z_k + hd, z_k + hd + e)
        return s - degagement([(-t / 2 - r, z_k + hd), (t / 2 + r, z_k + hd)], r)
    y_av = G["y_te"] + e + j
    y_ar = G["y_ti"] - j - e
    P.append(Plaque("genou_chape_avant", chape(), motif(c2, "sortie", vis, 0, z_k) + [(0, z_k, axe)],
                    [plan_y(y_av, e)], "cuisse", "sur l'entretoise (rondelles : jeu axial)"))
    P.append(Plaque("genou_chape_arriere", chape(), [(0, z_k, axe)],
                    [plan_y(y_ar, e)], "cuisse", "pivot du genou (palier à reprendre)"))
    dessus = rect(-rc, rc, y_ar - r - v, y_av + e + r + v)
    for y0 in (y_ar, y_av):
        dessus = dessus - rect(-t / 2, t / 2, y0, y0 + e) - os_de_chien(
            [(-t / 2, y0), (-t / 2, y0 + e), (t / 2, y0), (t / 2, y0 + e)], r)
    P.append(Plaque("genou_chape_dessus", dessus, [], [plan_z(z_k + hd)], "cuisse",
                    "dessus de la chape, recevra la cuisse"))
    return P


class Bande(Plaque):
    """Bande de papier fort enroulée sur les disques d'un factice : plate sur le plan,
    demi-cylindre (ou cylindre) dans l'assemblage. Matière non inscrite à hardware.yaml :
    c'est un gabarit de forme, sans effort ; il n'a ni rayon rentrant ni voile à tenir."""

    def __init__(self, nom, longueur, largeur, r, angle, poses, groupes, role):
        super().__init__(nom, rect(0, longueur, 0, largeur), [], poses, groupes, role, factice=True)
        self.r, self.angle, self.largeur = r, angle, largeur

    def finir(self, e, d_min):
        self.coupes, self.marques, self.face = [], [], self.esq
        bb = self.esq.faces()[0].bounding_box()
        self.dims = (bb.size.X, bb.size.Y, EP_BANDE)
        coque = bd.Cylinder(self.r + EP_BANDE, self.largeur) - bd.Cylinder(self.r, self.largeur)
        if self.angle < 360:
            coque = coque & bd.Pos(0, self.r * 2, 0) * bd.Box(self.r * 4, self.r * 4, self.largeur * 2)
        self.solide = coque
        return self


def plaques_factices(g, G) -> list[Plaque]:
    """Factices RONDS des RS00 (×2) et du RS02 : disques aux diamètres réels + bandes enroulées.

    Remplace le 2026-10-04 les boîtes carrées, dont les coins (rayon √2 fois celui
    du moteur) limitaient la maquette à ±5° au tangage et au roulis.
      face_avant    anneau au diamètre de la face avant, motif du boîtier s'il y est ;
      disque_rotor  la sortie, à son diamètre réel (STEP), libre dans l'anneau,
                    tenue par l'axe M3 ;
      epaulement    (RS02) disque au changement de diamètre (Ø78,5 -> Ø65) ;
      face_arriere  disque arrière, motif arrière et axe ;
      bande_*       papier fort, enroulé sur les disques ; coupé en deux s'il est
                    plus long que la planche A4.
    """
    e, j, vis = g["e"], g["j"], g["vis"]
    axe = vis["M3"]["passage"]
    zl, _ = ZONE_PLANCHE
    moteurs = [  # (id, cotes, centre, axe, x_dir, groupe stator, groupe rotor)
        (g["m_cheville"], g["c0"], (0, 0, G["z_p"]), (0, 1, 0), (1, 0, 0), "tibia", "pied"),
        (g["m_genou"], g["c2"], (0, G["y_te"] - G["L2"] / 2, G["z_k"]), (0, 1, 0), (1, 0, 0), "tibia", "cuisse"),
    ]
    par_nom: dict[str, Plaque] = {}

    def ajouter(pl, poses, grp):
        if pl.nom not in par_nom:
            par_nom[pl.nom] = pl
        par_nom[pl.nom].poses += poses
        par_nom[pl.nom].groupes += [grp] * len(poses)

    for mid, cm, centre, ax, xd, g_st, g_ro in moteurs:
        L = val(cm["longueur"])
        Dav = cm.get("diametre_bride") or cm["diametre_corps"]          # section avant
        Dar = cm["diametre_corps"]                                       # section arrière
        lav = cm.get("longueur_bride") or L                              # longueur de la section avant
        rotor = cm.get("diametre_sortie") or (cm.get("bossage_avant") or {}).get("diametre") \
            or 2 * rayon_motif(cm, "sortie", vis, g["v"])
        avant = [t for k in ("fixation_boitier",) if (cm.get(k) or {}).get("face") == "avant"
                 for t in motif(cm, k, vis)]
        arriere = [t for k in ("fixation_boitier", "arriere") if (cm.get(k) or {}).get("face") == "arriere"
                   for t in motif(cm, k, vis)]
        loc = bd.Location(bd.Plane(origin=centre, x_dir=xd, z_dir=ax))
        P = lambda nom, esq, trous: Plaque(f"factice_{mid}_{nom}", esq, trous, [], [], f"factice rond {mid.upper()}", factice=True)
        ajouter(P("face_avant", disque(0, 0, Dav / 2) - disque(0, 0, rotor / 2 + j), avant),
                [loc * bd.Location((0, 0, L / 2 - e))], g_st)
        ajouter(P("disque_rotor", disque(0, 0, rotor / 2), motif(cm, "sortie", vis) + [(0, 0, axe)]),
                [loc * bd.Location((0, 0, L / 2 - e))], g_ro)
        ajouter(P("face_arriere", disque(0, 0, Dar / 2), arriere + [(0, 0, axe)]),
                [loc * bd.Location((0, 0, -L / 2))], g_st)
        troncons = [(Dav, lav, L / 2 - lav / 2, "avant")]
        if lav < L - 1e-6:
            ajouter(P("epaulement", disque(0, 0, Dav / 2), [(0, 0, axe)]),
                    [loc * bd.Location((0, 0, L / 2 - lav))], g_st)
            troncons.append((Dar, L - lav, -lav / 2, "arriere"))
        for D, larg, zc, quoi in troncons:
            tour = math.pi * D
            n = 1 if tour + RECOUVREMENT <= zl - 2 else 2
            for i in range(n):
                b = Bande(f"factice_{mid}_bande_{quoi}" + (f"_{i + 1}" if n > 1 else ""),
                          tour / n + RECOUVREMENT, larg, D / 2, 360 / n, [], [], f"bande, papier fort ({mid.upper()})")
                rot = bd.Location((0, 0, 0), (0, 0, 1), 180 * i)
                ajouter(b, [loc * bd.Location((0, 0, zc)) * rot], g_st)
    return list(par_nom.values())


def moteurs_cylindres(g, G) -> list[tuple]:
    """Volumes réels (cylindres aux cotes publiées) : (nom, solide, groupe)."""
    out = []
    for nom, cm, centre, ax, grp in (
            ("rs00_cheville", g["c0"], (0, 0, G["z_p"]), (0, 1, 0), "tibia"),
            ("rs02_genou", g["c2"], (0, G["y_te"] - G["L2"] / 2, G["z_k"]), (0, 1, 0), "tibia")):
        L, D = val(cm["longueur"]), cm["diametre_corps"]
        loc = bd.Location(bd.Plane(origin=centre, z_dir=ax))
        lb = cm.get("longueur_bride")
        if lb:   # RS02 : Ø78,5 sur 28 mm à l'avant, puis le corps (STEP officiel, 2026-10-03)
            cyl = (bd.Pos(0, 0, L / 2 - lb / 2) * bd.Cylinder(cm["diametre_bride"] / 2, lb)
                   + bd.Pos(0, 0, -lb / 2) * bd.Cylinder(D / 2, L - lb))
        else:
            cyl = bd.Cylinder(D / 2, L)
        out.append((nom, cyl.moved(loc), grp))
    return out


# ─────────────────────────────────────────────────────── contrôles 2D
def voile(face, v: float, dedans) -> list[str]:
    """Les bandes de matière plus minces que v.

    Pour chaque paire de bords qui ne se touchent pas, la plus courte distance
    entre eux. C'est une bande de MATIÈRE si le milieu du segment est dans la
    pièce (sinon c'est une fente vide), et une vraie ÉPAISSEUR si le segment
    est perpendiculaire à l'un des deux bords (sinon il coupe un angle
    saillant, dont la distance n'est pas un voile). Remplace l'ouverture
    morphologique par build123d.offset, qui abandonne EN SILENCE le décalage
    d'un trou quand il échoue (constaté le 2026-10-03).
    """
    aretes = [ed for w in [face.outer_wire(), *face.inner_wires()] for ed in w.edges()]
    sommets = [{(round(x.X, 4), round(x.Y, 4)) for x in ed.vertices()} for ed in aretes]
    boites = [ed.bounding_box() for ed in aretes]
    out, vus = [], set()
    for i in range(len(aretes)):
        for k in range(i + 1, len(aretes)):
            if sommets[i] & sommets[k]:
                continue
            bi, bk = boites[i], boites[k]
            if (bi.min.X - bk.max.X > v or bk.min.X - bi.max.X > v
                    or bi.min.Y - bk.max.Y > v or bk.min.Y - bi.max.Y > v):
                continue
            d = aretes[i].distance_to(aretes[k])
            if d >= v - 1e-3:          # non-cote: 1 µm, égalité numérique
                continue
            p, q = aretes[i].closest_points(aretes[k])
            m = (p + q) * 0.5
            seg = (q - p).normalized()
            # de la matière des DEUX côtés du segment : un segment couché le
            # long d'un bord (flanc de tenon) n'est pas une bande de matière
            if not (dedans(m.X - seg.Y * DELTA, m.Y + seg.X * DELTA)
                    and dedans(m.X + seg.Y * DELTA, m.Y - seg.X * DELTA)):
                continue
            normal = any(abs(seg.dot(ed.tangent_at(ed.param_at_point(pt)))) < 0.5
                         for ed, pt in ((aretes[i], p), (aretes[k], q)))
            if not normal:
                continue
            cle = (round(m.X), round(m.Y))
            if cle not in vus:
                vus.add(cle)
                out.append(f"voile {d:.2f} < {v} mm en ({m.X:.1f}, {m.Y:.1f})")
    return out


def controler(pl: Plaque, g: dict) -> list[str]:
    """Règles du réglage sur la pièce RÉELLEMENT dessinée (pas sur ses intentions).

    · trou : chaque trou découpé >= trou minimal (les autres sont marqués) ;
    · rayon : tout arc RENTRANT (centre hors matière) >= rayon minimal, hors
      trous ronds (règle du trou) ; aucun sommet rentrant vif ;
    · voile : aucune bande de matière plus mince que le voile déclaré (voile()).
    """
    fautes = []
    e, r_min, v = g["e"], g["r"], g["reg"].get("voile_min")
    face = pl.face.faces()[0]
    sol = pl.solide

    def dedans(x, y):
        return sol.is_inside(bd.Vector(x, y, e / 2))
    for x, y, d in pl.coupes:
        if d < g["d_min"] - 1e-9:
            fautes.append(f"trou Ø{d} < {g['d_min']}")
    for w in [face.outer_wire(), *face.inner_wires()]:
        for ed in w.edges():
            if ed.geom_type == bd.GeomType.CIRCLE and not ed.is_closed:
                c, m = ed.arc_center, ed @ 0.5
                vers = (c - m).normalized() * DELTA
                rentrant = not dedans(m.X + vers.X, m.Y + vers.Y)
                if rentrant and ed.radius < r_min - 1e-6:
                    fautes.append(f"arc rentrant R{ed.radius:.2f} < {r_min} en ({m.X:.1f}, {m.Y:.1f})")
        for vx in w.vertices():
            n = 16
            frac = sum(dedans(vx.X + DELTA * math.cos(2 * math.pi * i / n),
                              vx.Y + DELTA * math.sin(2 * math.pi * i / n)) for i in range(n)) / n
            if frac > 0.6:
                fautes.append(f"angle rentrant vif en ({vx.X:.1f}, {vx.Y:.1f})")
    if v:
        fautes += voile(face, v, dedans)
    return fautes


# ─────────────────────────────────────────────────────── sorties
def ecrire_dxf(pl: Plaque, chemin: Path):
    import ezdxf
    exp = bd.ExportDXF(unit=bd.Unit.MM)
    exp.add_layer("DECOUPE")
    exp.add_shape(pl.face.faces()[0], layer="DECOUPE")
    exp.write(str(chemin))
    doc = ezdxf.readfile(str(chemin))
    if pl.marques:
        doc.layers.add("POINTAGE", color=1)
        msp = doc.modelspace()
        for x, y, d in pl.marques:
            msp.add_point((x, y), dxfattribs={"layer": "POINTAGE"})
            msp.add_line((x - CROIX, y), (x + CROIX, y), dxfattribs={"layer": "POINTAGE"})
            msp.add_line((x, y - CROIX), (x, y + CROIX), dxfattribs={"layer": "POINTAGE"})
    doc.saveas(str(chemin))
    return doc.header.get("$INSUNITS")


def ranger_a4(pieces: list[tuple]) -> list[dict]:
    """Rangement en étagères. `pieces` : (nom, contours, marques). Rend les feuilles."""
    zl, zh = ZONE_PLANCHE
    items = []
    for nom, cont, marq in pieces:
        xs = [p[0] for c in cont for p in c]
        ys = [p[1] for c in cont for p in c]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        tourne = w > zl or (h > w and h <= zl)
        if tourne:
            cont = [[(-y, x) for x, y in c] for c in cont]
            marq = [(-y, x, d) for x, y, d in marq]
            w, h = h, w
        if w > zl or h > zh:
            raise ValueError(f"{nom} ({w:.1f} x {h:.1f} mm) ne tient pas sur une planche A4 ({zl} x {zh})")
        xs = [p[0] for c in cont for p in c]
        ys = [p[1] for c in cont for p in c]
        items.append((nom, cont, marq, min(xs), min(ys), w, h))
    items.sort(key=lambda it: -it[6])
    feuilles, f, x, y, hl = [], None, 0.0, 0.0, 0.0
    for nom, cont, marq, x0, y0, w, h in items:
        if f is None:
            f, x, y, hl = dict(traits=[], croix=[], etiquettes=[]), 0.0, 0.0, 0.0
        if x + w > zl:                                # nouvelle étagère
            x, y, hl = 0.0, y + hl + ECART_PLAN, 0.0
        if y + h > zh:                                # nouvelle feuille
            feuilles.append(f)
            f, x, y, hl = dict(traits=[], croix=[], etiquettes=[]), 0.0, 0.0, 0.0
        dx, dy = x - x0, y - y0
        f["traits"] += [[(px + dx, py + dy) for px, py in c] for c in cont]
        for mx, my, _ in marq:
            f["croix"] += [[(mx + dx - CROIX, my + dy), (mx + dx + CROIX, my + dy)],
                           [(mx + dx, my + dy - CROIX), (mx + dx, my + dy + CROIX)]]
        f["etiquettes"].append((x + 1.0, y + h / 2, nom.replace("factice_", "")))
        x += w + ECART_PLAN
        hl = max(hl, h)
    if f is not None:
        feuilles.append(f)
    return feuilles


def placer(pl: Plaque):
    return [(f"{pl.nom}#{i + 1}" if len(pl.poses) > 1 else pl.nom, pl.solide.moved(loc), grp)
            for i, (loc, grp) in enumerate(zip(pl.poses, pl.groupes))]


# ─────────────────────────────────────────────────────── butées
def balayer(solides: list[tuple], G: dict, butees: dict) -> dict:
    """Pour chaque articulation, sur sa plage (joints.yaml), les autres à zéro :
    quelles pièces se pénètrent ? Rend la plage libre autour de zéro et la
    première collision de chaque côté.
    """
    axes = {"knee": (bd.Axis((0, 0, G["z_k"]), (0, 1, 0)), -1, {"cuisse"}),
            "ankle_pitch": (bd.Axis((0, 0, G["z_p"]), (0, 1, 0)), -1, {"tibia", "cuisse"})}
    out = {}
    for art, (axe, signe, mobiles) in axes.items():
        if art not in butees:
            continue
        lo, hi = butees[art]
        mob = [s for s in solides if s[2] in mobiles]
        fix = [s for s in solides if s[2] not in mobiles]

        def collisions(q):
            res = []
            for nm, sm, _ in mob:
                smq = sm.rotate(axe, signe * q) if q else sm
                bm = smq.bounding_box()
                for nf, sf, _ in fix:
                    bf = sf.bounding_box()
                    if (bm.max.X < bf.min.X or bf.max.X < bm.min.X or bm.max.Y < bf.min.Y
                            or bf.max.Y < bm.min.Y or bm.max.Z < bf.min.Z or bf.max.Z < bm.min.Z):
                        continue
                    inter = smq & sf
                    vol = sum(s.volume for s in inter.solids()) if inter else 0.0
                    if vol > VOL_MIN:
                        res.append((nm, nf, vol))
            return res
        rest = collisions(0)
        libre, premiere = {}, {}
        for sens, borne in (("+", hi), ("-", lo)):
            q, dernier = 0, 0
            pas = PAS_DEG if borne > 0 else -PAS_DEG
            libre[sens], premiere[sens] = borne, None
            for q in range(pas, int(borne) + (1 if pas > 0 else -1), pas):
                c = collisions(q)
                if c:
                    libre[sens], premiere[sens] = dernier, (q, c)
                    break
                dernier = q
            if borne == 0:
                libre[sens] = 0
        out[art] = dict(butees=(lo, hi), repos=rest, libre=(libre["-"], libre["+"]), premiere=premiere)
    return out


# ─────────────────────────────────────────────────────── rendu
def rendre(solides: list[tuple], png: Path):
    """Image de contrôle : chaque solide en maillage, MuJoCo hors écran."""
    import os
    os.environ.setdefault("MUJOCO_GL", "egl")
    import mujoco
    sys.path.insert(0, str(REPO / "sim"))
    from render import write_png
    RENDU.mkdir(parents=True, exist_ok=True)
    for f in RENDU.glob("*.stl"):
        f.unlink()
    coul = {"pied": ".85 .75 .55 1", "liaison": ".55 .7 .9 1", "tibia": ".8 .8 .82 1", "cuisse": ".95 .6 .4 1",
            "moteur": ".2 .45 .85 1"}
    assets, geoms = [], []
    for i, (nm, s, grp) in enumerate(solides):
        f = RENDU / f"m{i:02d}.stl"
        bd.export_stl(s, str(f))
        assets.append(f'<mesh name="m{i}" file="{f.name}" scale=".001 .001 .001"/>')
        c = coul["moteur"] if nm.startswith("rs0") or "factice" in nm and "rotor" not in nm else coul[grp]
        geoms.append(f'<geom type="mesh" mesh="m{i}" rgba="{c}" contype="0" conaffinity="0"/>')
    xml = (f'<mujoco><compiler meshdir="{RENDU}"/><visual><global offwidth="1600" offheight="1200"/></visual>'
           f'<asset>{"".join(assets)}</asset><worldbody><light pos="0 -.6 .8" dir="0 .6 -.8"/>'
           f'<light pos=".5 .5 .8" dir="-.5 -.5 -.8"/>'
           f'<geom type="plane" size=".4 .4 .01" rgba=".92 .92 .9 1"/>{"".join(geoms)}</worldbody></mujoco>')
    m = mujoco.MjModel.from_xml_string(xml)
    d = mujoco.MjData(m)
    mujoco.mj_forward(m, d)
    images = []
    r = mujoco.Renderer(m, height=900, width=800)
    try:
        for az, el, z, dist in ((130, -15, 0.12, 0.62), (220, -15, 0.12, 0.62), (90, -8, 0.05, 0.30)):
            cam = mujoco.MjvCamera()
            cam.lookat[:] = [0, 0, z]
            cam.distance, cam.azimuth, cam.elevation = dist, az, el
            r.update_scene(d, camera=cam)
            images.append(r.render())
    finally:
        r.close()
    import numpy as np
    img = np.concatenate(images, axis=1)
    write_png(str(png), img.tobytes(), img.shape[1], img.shape[0])


# ─────────────────────────────────────────────────────── principal
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--collisions", action="store_true", help="balayer les butées de joints.yaml (lent)")
    ap.add_argument("--rendu", action="store_true", help="image de contrôle (MuJoCo, EGL)")
    a = ap.parse_args(argv)
    SORTIE.mkdir(parents=True, exist_ok=True)
    jo = lire("joints.yaml")
    butees = {j["nom"]: (j["articulation"]["min"], j["articulation"]["max"]) for j in jo["jambes"]
              if j["nom"] in ("knee", "ankle_pitch")}
    bilan = {}
    code = 0
    for rid in REGLAGES:
        g = donnees(rid)
        G = geometrie(g)
        P = plaques_structure(g, G)
        if rid == REGLAGE_CARTON:
            P += plaques_factices(g, G)
        for pl in P:
            pl.finir(g["e"], g["d_min"])
        print(f"\n  ── réglage {rid} : épaisseur {g['e']} mm, rayon rentrant {g['r']} mm, "
              f"trou découpable ≥ Ø{g['d_min']:g}, voile {g['reg'].get('voile_min') or 'non déclaré'}"
              f"{'' if g['reg'].get('voile_min') else ' (non contrôlé)'}")
        print(f"     axes : cheville à {G['z_p']:.1f} mm du sol, genou à {G['z_k']:.1f} ; pied {g['W_pied']:.1f} mm de large")
        print("     | Pièce | Qté | Dimensions (mm) | Trous découpés | Trous marqués | Rôle |")
        print("     | --- | ---: | --- | ---: | ---: | --- |")
        fautes_tot = {}
        for pl in P:
            u, v_, e = pl.dims
            print(f"     | {pl.nom} | {len(pl.poses)} | {u:.1f} × {v_:.1f} × {e:g} | {len(pl.coupes)} "
                  f"| {len(pl.marques)} | {pl.role} |")
            unites = ecrire_dxf(pl, SORTIE / f"{NOM}_{pl.nom}_{rid}.dxf")
            if unites != 4:
                print(f"     ✗ {pl.nom} : DXF sans millimètres ($INSUNITS = {unites})")
                code = 1
            f = [] if isinstance(pl, Bande) else controler(pl, g)   # papier : ni rayon ni voile
            if f:
                fautes_tot[pl.nom] = f
        n_struct = sum(len(p.poses) for p in P if not p.factice)
        n_fact = sum(len(p.poses) for p in P if p.factice)
        print(f"     {n_struct} plaques de structure, {n_fact} plaques de factices, "
              f"{sum(len(p.marques) * len(p.poses) for p in P)} trous à pointer puis percer")
        if fautes_tot:
            print(f"     ✗ règles du réglage NON respectées ({sum(len(x) for x in fautes_tot.values())}) :")
            for nm, ff in fautes_tot.items():
                for x in ff:
                    print(f"         {nm} : {x}")
        else:
            print("     ✓ trou, rayon rentrant" + (", voile" if g["reg"].get("voile_min") else "")
                  + " : conformes sur toutes les pièces")
        # assemblage STEP
        solides = [s for pl in P for s in placer(pl)]
        if rid != REGLAGE_CARTON:
            solides += moteurs_cylindres(g, G)
        comp = bd.Compound(children=[s.moved(bd.Location()) for _, s, _ in solides])
        for ch, (nm, _, _) in zip(comp.children, solides):
            ch.label = nm
        bd.export_step(comp, str(SORTIE / f"{NOM}_assemblage_{rid}.step"), unit=bd.Unit.MM)
        print(f"     -> {NOM}_assemblage_{rid}.step ({len(solides)} solides), {len(P)} DXF")
        # plan A4 (carton)
        if rid == REGLAGE_CARTON:
            pieces = []
            for pl in P:
                cont = polylignes_depuis_face(pl.face.faces()[0])
                pieces += [(pl.nom, cont, pl.marques)] * len(pl.poses)
            feuilles = ranger_a4(pieces)
            from empreinte import empreinte as _emp
            n = ecrire_planches_a4(feuilles, SORTIE / f"{NOM}_{rid}_planA4.pdf",
                                   "YXOR - jambe basse S, carton plume 5 mm",
                                   [f"{len(pieces)} pieces (structure et factices), echelle 1:1. "
                                    f"Commit {_emp()} : verifier avant de couper.",
                                    "Maquette de FORME : ne jamais la mettre sous tension. "
                                    "Assemblage : tenons, vis M3 traversantes, rondelles.",
                                    "BANDES des factices : papier fort (pas de carton plume), "
                                    "enroulees sur les disques, languette de 10 mm."])
            print(f"     -> {NOM}_{rid}_planA4.pdf : {n} feuilles A4 ({len(pieces)} pièces)")
            bilan["feuilles"] = n
        # masse (aluminium)
        dens = lire("hardware.yaml")["matieres"][g["reg"]["matiere"]].get("densite")
        if dens:
            m = sum(pl.solide.volume * len(pl.poses) for pl in P if not pl.factice) * dens / 1000
            m_seg = {}
            for pl in P:
                if not pl.factice:
                    for grp in pl.groupes:
                        m_seg[grp] = m_seg.get(grp, 0) + pl.solide.volume * dens / 1000
            bilan["masse"] = (m, m_seg)
            print(f"     masse des plaques (densité {dens} g/cm³) : {m:.0f} g par jambe basse — "
                  + ", ".join(f"{k} {v:.0f} g" for k, v in m_seg.items()))
            import analyser_marche as AM
            if not AM.SERIE.exists():
                # construction Docker : exports/ n'y est pas ; le DIRE plutôt que planter
                print(f"     comparaison au modèle de S SAUTÉE : série de marche absente ({AM.SERIE.name})")
            else:
                sq = SQ.construire()
                part = sq["segs"]["left_tibia"]["masse"] + sq["segs"]["left_pied"]["masse"]
                print(f"     part du modèle de S pour le tibia et le pied (Winter × structure "
                      f"{sq['m_struct']:.3f} kg) : {part * 1000:.0f} g ; rapport {m / (part * 1000):.1f}")
                bilan["part"] = part * 1000
        if a.collisions:
            t0 = time.time()
            res = balayer(solides, G, butees)
            print(f"     butées (joints.yaml) — balayage tous les {PAS_DEG}°, les autres articulations à 0 "
                  f"({time.time() - t0:.0f} s) :")
            for art, r_ in res.items():
                print(f"       {art} : butées {r_['butees'][0]:g}..{r_['butees'][1]:g}° ; "
                      f"libre {r_['libre'][0]:g}..{r_['libre'][1]:g}°"
                      + (f" ; AU REPOS : {[(x[0], x[1]) for x in r_['repos']]}" if r_["repos"] else ""))
                for sens, pc in r_["premiere"].items():
                    if pc:
                        q, c = pc
                        print(f"         à {q:+d}° : " + " ; ".join(f"{x} / {y} ({vol:.0f} mm³)" for x, y, vol in c[:4]))
            bilan.setdefault("collisions", {})[rid] = res
        if a.rendu:
            png = RENDU / f"{NOM}_{rid}.png"
            rendre(solides, png)
            print(f"     -> {png.relative_to(REPO)}")
    return code


if __name__ == "__main__":
    sys.exit(main())
