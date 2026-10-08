#!/usr/bin/env python3
"""YXOR Kit, niveau 0 : toutes les pièces du robot en carton, planches A4 à reporter, notice de montage.

    .venv/bin/python parts/kit_niveau0.py              # pièces, contrôles, planches A4, STEP, notice
    .venv/bin/python parts/kit_niveau0.py --rendu      # + image de contrôle (MuJoCo, hors écran)

Créé le 2026-10-08 (prompt « YXOR Kit : décisions et plans du niveau 0 »). DÉCIDÉ
(fiche 0075, Jeremy) : assemblage B — tenons et mortaises, colle non porteuse
seulement, pivots par vis traversante. Matière dessinée : carton ondulé double,
3,5 mm (valeur mesurée ; consigne du prompt, pas un choix écrit par Jeremy).
Toutes les hypothèses de dessin sont dans params/kit.yaml (niveau0), PROPOSÉES.

═══════════════════════════════════════════════════════════════════════
 CE QUE LE CODE DESSINE
═══════════════════════════════════════════════════════════════════════

Chaque segment est un CAISSON, une boîte en plaques planes :
  · deux FLANCS (les plaques les plus larges, extérieures) ;
  · deux FACES, en retrait d'une épaisseur, dont les TENONS (languettes)
    traversent des MORTAISES (fentes) des flancs ;
  · des COUVERCLES (posés sur un bout, débordants) ou des CLOISONS
    (intérieures), tenonnés dans les flancs et les faces.

Une articulation est de deux sortes :
  · CHAPE : les flancs de l'enfant se prolongent en OREILLES qui encadrent le
    parent ; un pivot de chaque côté, sur le même axe ;
  · PLATEAU : l'enfant est vissé par un couvercle sur la sortie du servo du
    parent (lacets, épaule en tangage).

LOGEMENT DE SERVO (STS3215, hardware.yaml, servos) : une FENÊTRE dans la paroi
du parent, à l'aplomb de l'axe décalé de `decalage_sortie`, et une PLAQUE À
FENÊTRE intérieure à mi-hauteur du servo. Au niveau 0, la fenêtre est fermée
par un BOUCHON (pièce à sa taille, percée sur l'axe) et une PLAQUE DE SERRAGE
intérieure : la vis du pivot les serre. Au niveau 1, on retire bouchon et
plaque, on glisse le servo : rien n'est redécoupé.

Un axe passe par la sortie du servo ; les longueurs entre axes successifs sont
celles du Lab (ratios ANSUR × H du Lab, kit.yaml). Ce qui ne tient pas dans ces
longueurs (empilement des axes de hanche, hauteur de cheville, bassin) est
compté comme ÉCART et rapporté : la hauteur totale du Kit est une SORTIE.

Aucun angle rentrant vif (os de chien, dégagements tangents) ; contrôles :
une pièce d'un seul tenant, rayons rentrants, trous ; et, en 3D, aucune
interpénétration entre plaques (un tenon sans mortaise se verrait), ni entre
les servos du niveau 1 posés dans leurs logements et la structure.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import build123d as bd
import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import procedes as PROC  # noqa: E402
from plan_decoupe import ZONE_PLANCHE, ecrire_planches_a4, polylignes_depuis_face  # noqa: E402

NOM = "kit_niveau0"
SORTIE = REPO / "exports" / "parts"
RENDU = REPO / "exports" / NOM
NOTICE = REPO / "docs" / "kit-montage-niveau0.md"
ECART_PLAN = 4.0          # non-cote: espace entre deux pièces sur une planche A4
DELTA = 0.05              # non-cote: mm ; sondage autour d'un sommet
VOL_MIN = 1.0             # non-cote: mm³ ; une intersection plus petite est un artefact numérique
FLECHE = 14.0             # non-cote: longueur de la flèche des cannelures sur le gabarit
X, Y, Z = (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)


def lire(nom: str) -> dict:
    return yaml.safe_load((REPO / "params" / nom).read_text(encoding="utf-8"))


def vneg(a):
    return tuple(-x for x in a)


def vcross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def vadd(*vs):
    return tuple(sum(c) for c in zip(*vs))


def vmul(k, a):
    return tuple(k * x for x in a)


# ─────────────────────────────────────────────────────── données
def donnees() -> dict:
    """Toutes les entrées, lues dans params/ : aucune cote structurelle écrite ici (règle 1)."""
    kit = lire("kit.yaml")
    n0 = kit["niveau0"]
    hw = PROC.charger()
    reg = PROC.reglage(n0["reglage"], hw)
    e = reg["epaisseur"]
    r = PROC.rayon_interieur_min(e, reg.get("rayon_interieur_min_machine"))
    an = lire("anthropometry.yaml")
    R = {k: v["valeur"] for k, v in an["ratios"].items()}
    H = kit["kit_taille"]["H_m"] * 1000.0
    sv = hw["servos"][n0["servo"]]
    vis = hw["vis"][n0["vis_pivot"]]
    j = n0["jeu_fenetre"]
    vo = n0["voile_facteur"] * e
    g = dict(kit=kit, n0=n0, reg=reg, e=e, r=r, d_min=reg.get("trou_decoupe_min") or 2 * r, R=R, H=H,
             L={k: R[k] * H for k in R}, rallonge=(kit["kit_taille"]["hauteur_reelle_m"] - kit["kit_taille"]["H_m"]) * 1000.0,
             sv=sv, vis=vis, d=vis["passage"], j=j, vo=vo, tl=n0["tenon_longueur"], jm=n0["jeu_mortaise"],
             pas=n0["pas_tenons"], Aw=sv["A"] + j, Bw=sv["B"] + j, dec=sv["decalage_sortie"],
             pile=n0["cales_palonnier"] * e, jp=n0["jeu_pivot"], d_in=n0["profondeur_plaque_logement"] * sv["C"],
             ov=vo, rec=n0["recouvrement_plaque"], theta=math.radians(15.0), sigma=reg["masse_surfacique"])
    # servo enfoncé dans la paroi : face supérieure au ras de la face extérieure
    g["prof_servo"] = sv["C"] + sv["bossage_arriere"]
    g["int_servo"] = g["prof_servo"] - e + j            # profondeur intérieure qu'il occupe, jeu compris
    return g


# ─────────────────────────────────────────────────────── primitives 2D
def rect(x0, x1, y0, y1):
    return bd.Pos((x0 + x1) / 2, (y0 + y1) / 2) * bd.Rectangle(abs(x1 - x0), abs(y1 - y0))


def disque(cx, cy, r):
    return bd.Pos(cx, cy) * bd.Circle(r)


class Esquisse:
    """Une plaque en construction : ajouts, retraits, trous. Coordonnées (a, b) de la plaque."""

    def __init__(self, base):
        self.plus, self.moins, self.trous = [base], [], []

    def ajouter(self, s):
        self.plus.append(s)

    def retirer(self, s):
        self.moins.append(s)

    def face(self):
        f = self.plus[0]
        for s in self.plus[1:]:
            f = f + s
        for s in self.moins:
            f = f - s
        for a, b, d in self.trous:
            f = f - disque(a, b, d / 2)
        return f


def centres_tenons(a0, a1, g) -> list[float]:
    """Centres des tenons le long d'un bord [a0, a1] : un voile à chaque bout, au plus `pas` entre deux."""
    utile = (a1 - a0) - 2 * g["vo"] - g["tl"]
    if utile < 0:
        return [] if (a1 - a0) < g["tl"] + 2 * g["r"] + 2 else [(a0 + a1) / 2]
    n = 1 + int(utile // g["pas"])
    if n == 1:
        return [(a0 + a1) / 2]
    p0, p1 = a0 + g["vo"] + g["tl"] / 2, a1 - g["vo"] - g["tl"] / 2
    return [p0 + (p1 - p0) * i / (n - 1) for i in range(n)]


def tenon(es: Esquisse, axe: str, c: float, bord: float, sens: int, g):
    """Un tenon centré en c sur le bord `bord` (le long de a si axe='a'), dépassant de e dans le sens `sens`,
    avec deux dégagements tangents (aucun angle rentrant vif à sa racine)."""
    e, tl, r = g["e"], g["tl"], g["r"]
    if axe == "a":
        es.ajouter(rect(c - tl / 2, c + tl / 2, bord, bord + sens * e))
        for s in (-1, 1):
            es.retirer(disque(c + s * (tl / 2 + r), bord, r))
    else:
        es.ajouter(rect(bord, bord + sens * e, c - tl / 2, c + tl / 2))
        for s in (-1, 1):
            es.retirer(disque(bord, c + s * (tl / 2 + r), r))


def mortaise(es: Esquisse, axe: str, c: float, b0: float, g):
    """Une mortaise de longueur tl + jm (le long de a si axe='a'), de largeur e à partir de b0, os de chien."""
    e, L, r = g["e"], g["tl"] + g["jm"], g["r"]
    if axe == "a":
        x0, x1, y0, y1 = c - L / 2, c + L / 2, b0, b0 + e
    else:
        x0, x1, y0, y1 = b0, b0 + e, c - L / 2, c + L / 2
    es.retirer(rect(x0, x1, y0, y1))
    for x in (x0, x1):
        for y in (y0, y1):
            es.retirer(disque(x, y, r))


def fenetre(es: Esquisse, ca, cb, la, lb, g):
    """Une fenêtre rectangulaire centrée (ca, cb), de côtés la × lb, os de chien aux quatre coins."""
    x0, x1, y0, y1 = ca - la / 2, ca + la / 2, cb - lb / 2, cb + lb / 2
    es.retirer(rect(x0, x1, y0, y1))
    for x in (x0, x1):
        for y in (y0, y1):
            es.retirer(disque(x, y, g["r"]))


# ─────────────────────────────────────────────────────── plaques et caissons
class Plaque:
    """Une pièce plane : sa face 2D (a, b), ses poses 3D (origine, ex, ey, lo), le sens des cannelures."""

    def __init__(self, nom, corps, role, esq, poses, cannelures="a"):
        self.nom, self.corps, self.role, self.esq, self.poses = nom, corps, role, esq, poses
        self.cannelures = cannelures

    def finir(self, g):
        self.face = self.esq.face()
        fs = self.face.faces()
        if len(fs) != 1:
            raise ValueError(f"{self.nom} : {len(fs)} morceaux au lieu d'une pièce d'un seul tenant")
        self.solide = bd.extrude(self.face, amount=g["e"])
        bb = fs[0].bounding_box()
        self.dims = (bb.size.X, bb.size.Y)
        self.aire = fs[0].area
        return self

    def solides(self):
        out = []
        for O, ex, ey, lo, miroir in self.poses:
            n = vcross(ex, ey)
            pl = bd.Plane(origin=vadd(O, vmul(lo, n)), x_dir=ex, z_dir=n)
            s = self.solide.moved(bd.Location(pl))
            if miroir:
                s = s.mirror(bd.Plane.XZ)
            out.append(s)
        return out




class Caisson:
    """Repère (O, U, V), W = U × V. u ∈ [0, L] ; flancs ⟂ V aux bords v = ±W/2 (les plus larges) ; faces ⟂ W,
    en retrait de e (leur face extérieure à w = ±(Dp/2 − e)), tenonnées dans les flancs ; couvercles posés
    sur un bout (u < 0 ou u > L), débordants ; cloisons intérieures. `cote` : le caisson existe à gauche et,
    en miroir, à droite."""

    def __init__(self, nom, O, U, V, L, W, Dp, g, cote=True):
        self.nom, self.O, self.U, self.V, self.Wd = nom, O, U, V, vcross(U, V)
        self.L, self.W, self.Dp, self.g, self.cote = L, W, Dp, g, cote
        self.couv = {0: False, 1: False}
        self.cloisons = []          # positions u (bas de la plaque)
        self.oreilles = []          # dict(bout, wc, we, long) : prolongements des flancs, trou au bout
        self.logements = []         # dict(paroi, s, sa, sb, sens, vers, axe)
        self.trous = []             # (paroi, s, a, b, d)

    def p(self, u, v, w):
        return vadd(self.O, vmul(u, self.U), vmul(v, self.V), vmul(w, self.Wd))

    # extérieur des parois, dans le repère du caisson
    def paroi_ext(self, paroi):
        e = self.g["e"]
        return {"flanc": self.W / 2, "face": self.Dp / 2 - e}[paroi]

    def logement(self, paroi, s, sa, sb, sens, vers, axe):
        """Un servo dont la sortie est en (sa, sb) dans la paroi ; A le long de `sens` ('a' ou 'b') ; le corps
        du servo du côté `vers` (±1) de la sortie, le long de A."""
        g = self.g
        lg = dict(paroi=paroi, s=s, sa=sa, sb=sb, sens=sens, vers=vers, axe=axe)
        if sens == "a":
            lg["fen"] = (sa + vers * g["dec"], sb, g["Aw"], g["Bw"])
        else:
            lg["fen"] = (sa, sb + vers * g["dec"], g["Bw"], g["Aw"])
        self.logements.append(lg)
        return lg

    def _preparer(self):
        g, e, W, Dp, L = self.g, self.g["e"], self.W, self.Dp, self.L
        vi, bf = W / 2 - e, Dp / 2 - 2 * e
        self._cl = [(u0, [], None) for u0 in self.cloisons]
        self._pf = []        # plaques à fenêtre ⟂ V : (tc, v0) → mortaises dans les faces
        self._pw = []        # plaques à fenêtre ⟂ W : (tc, w0) → mortaises dans les flancs
        couv_fen = {0: [], 1: []}
        for lg in self.logements:
            ca, cb, la, lb = lg["fen"]
            if lg["paroi"] in ("flanc", "face"):
                a0 = max(0.0, ca - la / 2 - g["vo"] - g["tl"])           # la plaque reste dans le caisson
                a1 = min(L, ca + la / 2 + g["vo"] + g["tl"])
                tc = centres_tenons(a0, a1, g)
                if lg["paroi"] == "flanc":
                    v_int = lg["s"] * (W / 2 - e)                 # face intérieure du flanc
                    v0 = v_int - lg["s"] * g["d_in"] - (e if lg["s"] > 0 else 0)
                    lg["pl"] = dict(a0=a0, a1=a1, tc=tc, v0=v0)
                    self._pf.append((tc, v0))
                else:
                    w_int = lg["s"] * bf
                    w0 = w_int - lg["s"] * g["d_in"] - (e if lg["s"] > 0 else 0)
                    lg["pl"] = dict(a0=a0, a1=a1, tc=tc, w0=w0)
                    self._pw.append((tc, w0))
            else:
                couv_fen[lg["s"]].append((ca, cb, la, lb))
        # une seule plaque par couvercle, avec toutes ses fenêtres ; plus étroite (sans tenons dans les flancs)
        # si des plaques de logement de flanc occupent la même hauteur
        for k, fens in couv_fen.items():
            if not fens:
                continue
            u0 = (-e + g["d_in"]) if k == 0 else (L - g["d_in"])
            vlim = None
            for lg in self.logements:
                if lg["paroi"] == "flanc" and lg["pl"]["a0"] - e <= u0 + e and u0 <= lg["pl"]["a1"]:
                    lim = W / 2 - e - g["int_servo"] - g["jp"]            # s'arrête avant le corps du servo
                    vlim = lim if vlim is None else min(vlim, lim)
            self._cl.append((u0, fens, vlim))
        self.tf = centres_tenons(0, L, g)
        self.tcv = centres_tenons(-vi, vi, g)
        self.tcw = centres_tenons(-bf, bf, g)
        self.tfw = centres_tenons(-Dp / 2, Dp / 2, g)

    def _fenetres(self, es, paroi, s):
        for lg in self.logements:
            if lg["paroi"] == paroi and lg["s"] == s:
                fenetre(es, *lg["fen"], self.g)
        for (par, ss, a, b, d) in self.trous:
            if par == paroi and ss == s:
                es.trous.append((a, b, d))

    def _poses(self, ex, ey, lo):
        return [(self.O, ex, ey, lo, False)] + ([(self.O, ex, ey, lo, True)] if self.cote else [])

    def plaques(self) -> list[Plaque]:
        self._preparer()
        g, e, L, W, Dp = self.g, self.g["e"], self.L, self.W, self.Dp
        vi, bf = W / 2 - e, Dp / 2 - 2 * e
        out = []
        # ── flancs ⟂ V : (a, b) = (u, w)
        for s in (1, -1):
            es = Esquisse(rect(0, L, -Dp / 2, Dp / 2))
            for sg in (1, -1):
                for c in self.tf:
                    mortaise(es, "a", c, bf if sg > 0 else -bf - e, g)
            for u0, _, vl in self._cl:
                if vl is None:
                    for c in self.tcw:
                        mortaise(es, "b", c, u0, g)
            for tc, w0 in self._pw:
                for c in tc:
                    mortaise(es, "a", c, w0, g)
            for k in (0, 1):
                if self.couv[k]:
                    for c in self.tfw:
                        tenon(es, "b", c, 0 if k == 0 else L, -1 if k == 0 else 1, g)
            for o in self.oreilles:
                ub = 0 if o["bout"] == 0 else L
                sg = -1 if o["bout"] == 0 else 1
                ua = ub + sg * o["long"]
                es.ajouter(rect(min(ub, ua), max(ub, ua), o["wc"] - o["we"] / 2, o["wc"] + o["we"] / 2))
                es.ajouter(disque(ua, o["wc"], o["we"] / 2))
                es.trous.append((ua, o["wc"], g["d"]))
                for t in (-1, 1):
                    bord = o["wc"] + t * o["we"] / 2
                    if abs(bord) < Dp / 2 - 1e-6:           # racine dans le flanc : dégagement tangent
                        es.retirer(disque(ub, bord + t * g["r"], g["r"]))
            self._fenetres(es, "flanc", s)
            out.append(Plaque(f"{self.nom}.flanc{'+' if s > 0 else '-'}", self.nom, "flanc", es,
                              self._poses(self.U, self.Wd, -W / 2 if s > 0 else W / 2 - e)))
        # ── faces ⟂ W : (a, b) = (u, v)
        for s in (1, -1):
            es = Esquisse(rect(0, L, -vi, vi))
            for c in self.tf:
                for sg in (1, -1):
                    tenon(es, "a", c, sg * vi, sg, g)
            for u0, _, vl in self._cl:
                for c in (self.tcv if vl is None else centres_tenons(-vl, vl, g)):
                    mortaise(es, "b", c, u0, g)
            for tc, v0 in self._pf:
                for c in tc:
                    mortaise(es, "a", c, v0, g)
            for k in (0, 1):
                if self.couv[k]:
                    for c in self.tcv:
                        tenon(es, "b", c, 0 if k == 0 else L, -1 if k == 0 else 1, g)
            self._fenetres(es, "face", s)
            out.append(Plaque(f"{self.nom}.face{'+' if s > 0 else '-'}", self.nom, "face", es,
                              self._poses(self.U, self.V, bf if s > 0 else -bf - e)))
        # ── cloisons, dont les plaques à fenêtre des logements des couvercles ⟂ U : (a, b) = (v, w)
        n = 0
        for u0, fen, vl in self._cl:
            vv = vi if vl is None else vl
            es = Esquisse(rect(-vv, vv, -bf, bf))
            if vl is None:
                for c in self.tcw:
                    for sg in (1, -1):
                        tenon(es, "b", c, sg * vi, sg, g)
            for c in (self.tcv if vl is None else centres_tenons(-vl, vl, g)):
                for sg in (1, -1):
                    tenon(es, "a", c, sg * bf, sg, g)
            for f in fen:
                fenetre(es, *f, g)
            n += 0 if fen else 1
            nom = f"{self.nom}.plaque_logement_{'bas' if u0 < L / 2 else 'haut'}" if fen else f"{self.nom}.cloison{n}"
            out.append(Plaque(nom, self.nom, "plaque à fenêtre" if fen else "cloison", es,
                              self._poses(self.V, self.Wd, u0), cannelures="a" if W >= Dp else "b"))
        # ── plaques à fenêtre des logements des flancs et des faces
        for lg in self.logements:
            if lg["paroi"] == "couv":
                continue
            pl = lg["pl"]
            ca, cb, la, lb = lg["fen"]
            if lg["paroi"] == "flanc":
                es = Esquisse(rect(pl["a0"], pl["a1"], -bf, bf))
                for c in pl["tc"]:
                    for sg in (1, -1):
                        tenon(es, "a", c, sg * bf, sg, g)
                fenetre(es, ca, cb, la, lb, g)
                # repère (U, Wd) : n = −V ; la plaque occupe v ∈ [v0, v0 + e]
                out.append(Plaque(f"{self.nom}.{lg['axe']}.plaque", self.nom, "plaque à fenêtre", es,
                                  self._poses(self.U, self.Wd, -pl["v0"] - e)))
            elif lg["paroi"] == "face":
                es = Esquisse(rect(pl["a0"], pl["a1"], -vi, vi))
                for c in pl["tc"]:
                    for sg in (1, -1):
                        tenon(es, "a", c, sg * vi, sg, g)
                fenetre(es, ca, cb, la, lb, g)
                out.append(Plaque(f"{self.nom}.{lg['axe']}.plaque", self.nom, "plaque à fenêtre", es,
                                  self._poses(self.U, self.V, pl["w0"])))
        # ── couvercles ⟂ U : (a, b) = (v, w), débordants
        for k in (0, 1):
            if not self.couv[k]:
                continue
            ov = g["ov"]
            es = Esquisse(rect(-W / 2 - ov, W / 2 + ov, -Dp / 2 - ov, Dp / 2 + ov))
            for sg in (1, -1):
                for c in self.tfw:
                    mortaise(es, "b", c, W / 2 - e if sg > 0 else -W / 2, g)
                for c in self.tcv:
                    mortaise(es, "a", c, bf if sg > 0 else -bf - e, g)
            self._fenetres(es, "couv", k)
            out.append(Plaque(f"{self.nom}.couvercle_{'bas' if k == 0 else 'haut'}", self.nom, "couvercle", es,
                              self._poses(self.V, self.Wd, -e if k == 0 else L),
                              cannelures="a" if W >= Dp else "b"))
        # ── niveau 0 : bouchon et plaque de serrage de chaque logement
        for lg in self.logements:
            ca, cb, la, lb = lg["fen"]
            nm = f"{self.nom}.{lg['axe']}"
            b = Esquisse(rect(ca - la / 2, ca + la / 2, cb - lb / 2, cb + lb / 2))
            b.trous.append((lg["sa"], lg["sb"], g["d"]))
            ca_ = "a" if la >= lb else "b"
            out.append(Plaque(f"{nm}.bouchon", self.nom, "bouchon (niveau 0)", b, self._poses_paroi(lg, 0), ca_))
            rc = g["rec"]
            sp = Esquisse(rect(ca - la / 2 - rc, ca + la / 2 + rc, cb - lb / 2 - rc, cb + lb / 2 + rc))
            sp.trous.append((lg["sa"], lg["sb"], g["d"]))
            out.append(Plaque(f"{nm}.serrage", self.nom, "plaque de serrage (niveau 0)", sp,
                              self._poses_paroi(lg, 1), ca_))
        return out

    def _poses_paroi(self, lg, couche):
        """Dans le plan de la paroi du logement (couche 0) ou juste à l'intérieur (couche 1)."""
        e, W, Dp, L = self.g["e"], self.W, self.Dp, self.L
        p, s = lg["paroi"], lg["s"]
        if p == "flanc":                                   # n = −V
            lo = (-W / 2 if s > 0 else W / 2 - e) + couche * (e if s > 0 else -e)
            return self._poses(self.U, self.Wd, lo)
        if p == "face":                                    # n = +W
            bf = Dp / 2 - 2 * e
            lo = (bf if s > 0 else -bf - e) - couche * (e if s > 0 else -e)
            return self._poses(self.U, self.V, lo)
        lo = (-e if s == 0 else L) + couche * (e if s == 0 else -e)   # n = +U
        return self._poses(self.V, self.Wd, lo)

    def servos(self):
        """Les servos du niveau 1, posés dans leurs logements (boîtes A × B × C), pour le contrôle 3D."""
        g, e = self.g, self.g["e"]
        out = []
        for lg in self.logements:
            ca, cb, la, lb = lg["fen"]
            C = g["sv"]["C"]
            jj = g["j"] + 0.2
            if lg["paroi"] == "flanc":
                c3 = self.p(ca, lg["s"] * (self.W / 2 - C / 2), cb)
                du, dv, dw = la - jj, C, lb - jj
            elif lg["paroi"] == "face":
                c3 = self.p(ca, cb, lg["s"] * (self.Dp / 2 - e - C / 2))
                du, dv, dw = la - jj, lb - jj, C
            else:
                u = -e + C / 2 if lg["s"] == 0 else self.L + e - C / 2
                c3 = self.p(u, ca, cb)
                du, dv, dw = C, la - jj, lb - jj
            box = bd.Box(du, dv, dw).moved(bd.Location(bd.Plane(origin=c3, x_dir=self.U, z_dir=self.Wd)))
            out.append((f"servo {self.nom}.{lg['axe']}", box))
            if self.cote:
                out.append((f"servo {self.nom}.{lg['axe']} (droit)", box.mirror(bd.Plane.XZ)))
        return out


# ─────────────────────────────────────────────────────── le robot
def robot(g) -> tuple[list[Caisson], list[dict], dict]:
    """Tous les caissons, debout, jambe et bras GAUCHES (y > 0 ; le droit en miroir), et les pivots.
    Les longueurs entre axes sont celles du Lab ; les écarts sont calculés et rendus."""
    e, vo, Aw, Bw, dec, pile, jp, d_in = (g[k] for k in ("e", "vo", "Aw", "Bw", "dec", "pile", "jp", "d_in"))
    L, I = g["L"], g["int_servo"]
    ext_a = Aw / 2 - dec + vo                 # au-delà de la sortie, fenêtre le long de l'axe du segment
    ext_b = Bw / 2 + vo                       # au-delà de la sortie, fenêtre en travers

    def deg(du, dw):
        """Distance de l'axe au corps de l'enfant pour que les coins du parent passent à ±θ (PROPOSÉ)."""
        return du * math.cos(g["theta"]) + dw * math.sin(g["theta"]) + 2 * jp

    corps, piv, ec = [], [], {}
    # ── sections minimales imposées par le servo (quincaillerie) et par les voiles
    W_t, Dp_t = I + 2 * e, 2 * (Bw / 2 + vo + 2 * e)              # tibia : logements dans un flanc, A le long
    W1, Dp1 = 2 * (Aw / 2 + vo + e), I + 4 * e                    # noix de hanche 1 : roulis, face ⟂ x, A en travers
    Dp2 = I + 4 * e                                               # noix de hanche 2 : tangage, face ⟂ y
    W2 = max(2 * (Aw / 2 + vo + e), (Dp1 / 2 - e) + pile + Dp1 / 2 + jp + 2 * e)
    G_th = max((Dp2 / 2 - e) + pile + Dp2 / 2 + jp, W_t / 2 + pile + W_t / 2 + jp)
    W_th = G_th + 2 * e
    y_h = L["largeur_bassin"] / 2
    # ── y (jambe gauche) : la cuisse centrée sur la hanche ; parents côté servo vers +y
    y_th = y_h
    y_t = y_th + W_th / 2 - e - pile - W_t / 2
    y_2 = y_th + W_th / 2 - e - pile - (Dp2 / 2 - e)
    W_f = max(W_t + pile + jp + 2 * e, L["pied_largeur"])
    y_f = y_t + W_t / 2 + pile + e - W_f / 2
    # ── x : lacet de hanche en x = 0 ; noix 1 centrée dessous ; noix 2 et la jambe en découlent
    x2 = (Dp1 / 2 - e) + pile + e - W2 / 2
    x_leg = x2 - dec                                              # fenêtre de la noix 2 centrée : sortie à −dec
    y_n1 = y_h + dec                                              # roulis en y = y_h, fenêtre centrée sur la noix
    # ── z, depuis le sol
    h_f = L["cheville_hauteur"]
    z_a = e + h_f + deg(ext_a, Dp_t / 2)
    z_k = z_a + L["tibia"]
    z_p = z_k + L["cuisse"]
    d_top = deg(ext_b, W2 / 2 + dec)
    d_bot = deg(ext_a, Dp_t / 2)
    L2 = 2 * ext_b
    z_r = z_p + ext_b + deg(ext_b, W1 / 2 + dec)
    L1 = 2 * ext_b
    z_n1 = z_r + ext_b                                            # dessus de la noix 1 (sous son couvercle)
    # pied : U = Z, V = Y, W = −X ; la cheville au quart du pied depuis le talon
    Lp = L["pied_longueur"]
    x_f = x_leg + (0.5 - g["n0"]["pied_talon"]) * Lp
    pied = Caisson("pied", (x_f, y_f, e), Z, Y, h_f, W_f, Lp, g)
    pied.couv[0] = True
    wc = -(x_leg - x_f)
    we = min(Dp_t, Lp - 2 * abs(wc))
    pied.oreilles.append(dict(bout=1, wc=wc, we=we, long=z_a - (e + h_f)))
    pied.cloisons.append(h_f - 3 * e)
    corps.append(pied)
    # tibia : U = −Z, V = Y, W = X ; genou et cheville logés dans le flanc extérieur (+y)
    L_t = 2 * ext_a + L["tibia"]
    tib = Caisson("tibia", (x_leg, y_t, z_k + ext_a), vneg(Z), Y, L_t, W_t, Dp_t, g)
    tib.logement("flanc", 1, ext_a, 0.0, "a", 1, "knee")
    tib.logement("flanc", 1, ext_a + L["tibia"], 0.0, "a", -1, "ankle_pitch")
    tib.trous += [("flanc", -1, ext_a, 0.0, g["d"]), ("flanc", -1, ext_a + L["tibia"], 0.0, g["d"])]
    corps.append(tib)
    # cuisse : U = −Z, V = Y ; oreilles en haut (noix 2) et en bas (tibia)
    L_c = L["cuisse"] - d_top - d_bot
    cui = Caisson("cuisse", (x_leg, y_th, z_p - d_top), vneg(Z), Y, L_c, W_th, Dp_t, g)
    cui.oreilles += [dict(bout=0, wc=0.0, we=Dp_t, long=d_top), dict(bout=1, wc=0.0, we=Dp_t, long=d_bot)]
    cui.cloisons += [2 * e, L_c - 3 * e]
    corps.append(cui)
    # noix de hanche 2 : U = −Z, V = X (oreilles ⟂ x autour de la noix 1), W = −Y ; tangage logé face −1 (+y)
    n2 = Caisson("hanche2", (x2, y_2, z_p + ext_b), vneg(Z), X, L2, W2, Dp2, g)
    n2.logement("face", -1, L2 - ext_b, -dec, "b", 1, "hip_pitch")
    n2.trous.append(("face", 1, L2 - ext_b, -dec, g["d"]))
    # oreilles étroites : leur bout arrondi ne doit pas monter jusqu'au couvercle de la noix 1
    n2.oreilles.append(dict(bout=0, wc=-(y_h - y_2), we=2 * (ext_b - jp), long=deg(ext_b, W1 / 2 + dec)))
    corps.append(n2)
    # noix de hanche 1 : U = −Z, V = Y, W = X ; couvercle sur le servo de lacet ; roulis logé face +1 (+x)
    n1 = Caisson("hanche1", (0.0, y_n1, z_n1), vneg(Z), Y, L1, W1, Dp1, g)
    n1.couv[0] = True
    n1.logement("face", 1, ext_b, -dec, "b", 1, "hip_roll")
    n1.trous += [("face", -1, ext_b, -dec, g["d"]), ("couv", 0, y_h - y_n1, 0.0, g["d"])]
    corps.append(n1)
    # bassin : U = Z, V = Y, W = −X ; lacets de hanche (couvercle bas) et de taille (couvercle haut)
    xb = -dec
    W_b = 2 * (y_h + Bw / 2 + vo + e)
    Dp_b = 2 * (Aw / 2 + vo + 2 * e)
    L_b = g["prof_servo"] - e + jp + d_in
    z_b = z_n1 + e + pile + e
    bas = Caisson("bassin", (xb, 0.0, z_b), Z, Y, L_b, W_b, Dp_b, g, cote=False)
    bas.couv[0] = bas.couv[1] = True
    for sy in (1, -1):
        bas.logement("couv", 0, sy * y_h, xb, "b", 1, "hip_yaw" + ("" if sy > 0 else "_droit"))
    bas.logement("couv", 1, 0.0, xb, "b", 1, "waist_yaw")
    corps.append(bas)
    # tronc : U = Z, V = Y, W = −X ; épaules dans les flancs, cou dans le couvercle haut
    L_tr = L["tronc_hauteur"] + g["rallonge"]
    W_tr, Dp_tr = L["largeur_epaules"], L["profondeur_poitrine"]
    z_tr = z_b + L_b + e + pile + e
    tr = Caisson("tronc", (xb, 0.0, z_tr), Z, Y, L_tr, W_tr, Dp_tr, g, cote=False)
    tr.couv[0] = tr.couv[1] = True
    u_s = L_tr - max(0.1 * L["tronc_hauteur"], ext_b)
    for s in (1, -1):
        tr.logement("flanc", s, u_s, xb, "b", 1, "shoulder_pitch" + ("" if s > 0 else "_droit"))
    tr.logement("couv", 1, 0.0, xb, "b", 1, "neck_yaw")
    tr.trous.append(("couv", 0, 0.0, xb, g["d"]))
    tr.cloisons.append(L_tr / 2)
    corps.append(tr)
    # cou : U = Z, V = Y, W = −X ; tangage logé flanc +1
    W_nc, Dp_nc, L_nc = I + 2 * e, 2 * (Aw / 2 + vo + 2 * e), 2 * ext_b
    z_nc = z_tr + L_tr + e + pile + e
    cou = Caisson("cou", (xb, 0.0, z_nc), Z, Y, L_nc, W_nc, Dp_nc, g, cote=False)
    cou.couv[0] = True
    cou.logement("flanc", 1, ext_b, xb, "b", 1, "neck_pitch")
    cou.trous += [("flanc", -1, ext_b, xb, g["d"]), ("couv", 0, 0.0, xb, g["d"])]
    corps.append(cou)
    # tête : U = Z, V = Y, W = −X ; oreilles autour du cou
    W_hd = max(W_nc + pile + jp + 2 * e, 0.8 * L["tete_hauteur"])
    Dp_hd, L_hd = 0.9 * L["tete_hauteur"], L["tete_hauteur"]
    y_hd = W_nc / 2 + pile + e - W_hd / 2
    d_hd = deg(ext_b, Dp_nc / 2 + dec)
    z_np = z_nc + ext_b
    tete = Caisson("tete", (0.0, y_hd, z_np + d_hd), Z, Y, L_hd, W_hd, Dp_hd, g, cote=False)
    tete.couv[1] = True
    # bout arrondi des oreilles au-dessus du couvercle du tronc
    tete.oreilles.append(dict(bout=0, wc=0.0, we=min(Dp_hd, 2 * (ext_b + pile + e - jp)), long=d_hd))
    tete.cloisons.append(2 * e)
    corps.append(tete)
    # épaule : U = Y, V = Z, W = X ; couvercle sur le servo de tangage ; roulis logé face +1 (+x)
    z_s = z_tr + u_s
    W_ne, Dp_ne = 2 * (Bw / 2 + vo + e), I + 4 * e
    u_r = vo + Aw / 2 + dec
    L_ne = u_r + ext_a
    y_ne = W_tr / 2 + pile + e
    ep = Caisson("epaule", (0.0, y_ne, z_s), Y, Z, L_ne, W_ne, Dp_ne, g)
    ep.couv[0] = True
    ep.logement("face", 1, u_r, 0.0, "a", -1, "shoulder_roll")
    ep.trous += [("face", -1, u_r, 0.0, g["d"]), ("couv", 0, 0.0, 0.0, g["d"])]
    corps.append(ep)
    # bras : U = −Z, V = X, W = −Y ; coude logé face −1 (+y)
    W_br = max((Dp_ne / 2 - e) + pile + Dp_ne / 2 + jp + 2 * e, 2 * (Bw / 2 + vo + e))
    Dp_br = I + 4 * e
    x_br = (Dp_ne / 2 - e) + pile + e - W_br / 2
    y_r = y_ne + u_r
    d_s = deg(W_ne / 2, u_r + e)
    u_e = L["bras"] - d_s
    L_br = u_e + ext_a
    br = Caisson("bras", (x_br, y_r, z_s - d_s), vneg(Z), X, L_br, W_br, Dp_br, g)
    br.oreilles.append(dict(bout=0, wc=0.0, we=Dp_br, long=d_s))
    br.logement("face", -1, u_e, 0.0, "a", -1, "elbow_roll")
    br.trous.append(("face", 1, u_e, 0.0, g["d"]))
    corps.append(br)
    # avant-bras : U = −Z, V = Y, W = X ; poignet passif (lacet par le couvercle bas)
    W_ab = (Dp_br / 2 - e) + pile + Dp_br / 2 + jp + 2 * e
    Dp_ab = Dp_br
    y_ab = y_r + (Dp_br / 2 - e) + pile + e - W_ab / 2
    z_e = z_s - L["bras"]
    d_e = deg(ext_a, W_br / 2)
    c_np = g["tl"] + 2 * vo + 4 * e                              # le plus petit caisson dont les tenons tiennent
    z_w = z_e - L["avant_bras"]
    z_np_lid = z_w + c_np / 2 + e
    L_ab = (z_e - d_e) - (z_np_lid + jp + e)
    ab = Caisson("avant_bras", (x_br, y_ab, z_e - d_e), vneg(Z), Y, L_ab, W_ab, Dp_ab, g)
    ab.couv[1] = True
    ab.oreilles.append(dict(bout=0, wc=0.0, we=Dp_ab, long=d_e))
    ab.trous.append(("couv", 1, y_r - y_ab, 0.0, g["d"]))
    corps.append(ab)
    # poignet : noix passive ; main : oreilles autour d'elle
    npg = Caisson("poignet", (x_br, y_r, z_w + c_np / 2), vneg(Z), Y, c_np, c_np, c_np, g)
    npg.couv[0] = True
    npg.trous += [("flanc", 1, c_np / 2, 0.0, g["d"]), ("flanc", -1, c_np / 2, 0.0, g["d"]),
                  ("couv", 0, 0.0, 0.0, g["d"])]
    corps.append(npg)
    W_m = c_np + 2 * jp + 2 * e
    d_m = deg(c_np / 2, c_np / 2)
    L_m = L["main_longueur"] - d_m
    main_ = Caisson("main", (x_br, y_r, z_w - d_m), vneg(Z), Y, L_m, W_m, W_m, g)
    main_.couv[1] = True
    main_.oreilles.append(dict(bout=0, wc=0.0, we=2 * (c_np / 2 - jp), long=d_m))
    corps.append(main_)
    # ── pivots (notice) : nom de joints.yaml, sorte, parent, enfant, côtés
    def pv(nom, sorte, par, enf, cote, cale_idler):
        piv.append(dict(nom=nom, sorte=sorte, parent=par, enfant=enf, n=2 if cote else 1, cale_idler=cale_idler))
    pv("hip_yaw", "plateau (servo au niveau 3)", "bassin", "hanche1", True, 0.0)
    pv("hip_roll", "chape (servo au niveau 3)", "hanche1", "hanche2", True, W2 - 2 * e - (Dp1 - e + pile))
    pv("hip_pitch", "chape (servo au niveau 3)", "hanche2", "cuisse", True, G_th - (Dp2 - e + pile))
    pv("knee", "chape (servo au niveau 3)", "tibia", "cuisse", True, G_th - (W_t + pile))
    pv("ankle_pitch", "chape (servo au niveau 3)", "tibia", "pied", True, (W_f - 2 * e) - (W_t + pile))
    pv("waist_yaw", "plateau (servo au niveau 3)", "bassin", "tronc", False, 0.0)
    pv("shoulder_pitch", "plateau (servo au niveau 1)", "tronc", "epaule", True, 0.0)
    pv("shoulder_roll", "chape (servo au niveau 1)", "epaule", "bras", True, W_br - 2 * e - (Dp_ne - e + pile))
    pv("elbow_roll", "chape (servo au niveau 1)", "bras", "avant_bras", True, W_ab - 2 * e - (Dp_br - e + pile))
    pv("neck_yaw", "plateau (servo au niveau 1)", "tronc", "cou", False, 0.0)
    pv("neck_pitch", "chape (servo au niveau 1)", "cou", "tete", False, (W_hd - 2 * e) - (W_nc + pile))
    pv("wrist_roll", "plateau passif", "avant_bras", "poignet", True, 0.0)
    pv("wrist_pitch", "chape passive", "poignet", "main", True, jp)
    ec = dict(z_cheville=z_a, z_genou=z_k, z_hanche_tangage=z_p, z_hanche_roulis=z_r, z_bassin_bas=z_b - e,
              z_epaule=z_s, z_cou_tangage=z_np, z_sommet=z_np + d_hd + L_hd + e,
              largeur_bassin=W_b, hanche_y=y_h)
    return corps, piv, ec


# ─────────────────────────────────────────────────────── contrôles
def controler_2d(contours, r_min) -> list[str]:
    """Sur les polylignes de la pièce : aucun sommet rentrant VIF (deux segments longs qui tournent du côté
    rentrant) et aucun arc rentrant de rayon < r_min. Le contour extérieur et les trous ne tournent pas dans le
    même sens : le côté « matière » se déduit du signe de leur aire."""
    fautes = []
    aires = []
    for c in contours:
        a = sum(c[i][0] * c[(i + 1) % len(c)][1] - c[(i + 1) % len(c)][0] * c[i][1] for i in range(len(c))) / 2
        aires.append(a)
    ext = max(range(len(contours)), key=lambda i: abs(aires[i]))
    for k, c in enumerate(contours):
        sg = math.copysign(1, aires[k]) * (1 if k == ext else -1)     # + : matière à gauche
        n = len(c)
        run_ang, run_len = 0.0, 0.0
        for i in range(n):
            p0, p1, p2 = c[i - 1], c[i], c[(i + 1) % n]
            ax, ay, bx, by = p1[0] - p0[0], p1[1] - p0[1], p2[0] - p1[0], p2[1] - p1[1]
            la, lb = math.hypot(ax, ay), math.hypot(bx, by)
            if la < 1e-9 or lb < 1e-9:
                continue
            cr = (ax * by - ay * bx) / (la * lb)
            ang = math.asin(max(-1.0, min(1.0, cr)))
            rentrant = sg * cr < -1e-6
            if rentrant and la > 1.0 and lb > 1.0 and abs(ang) > math.radians(5):
                fautes.append(f"angle rentrant vif en ({p1[0]:.1f}, {p1[1]:.1f})")
            if rentrant and abs(ang) > 1e-3:
                run_ang += abs(ang)
                run_len += lb
            else:
                if run_ang > math.radians(30) and run_len / run_ang < 0.9 * r_min:
                    fautes.append(f"arc rentrant R{run_len / run_ang:.2f} < {r_min} près de ({p1[0]:.1f}, {p1[1]:.1f})")
                run_ang, run_len = 0.0, 0.0
    return fautes


def interferences(solides: list[tuple], exclus) -> list[str]:
    """Paires de solides qui se pénètrent (volume > VOL_MIN) ; boîtes englobantes d'abord."""
    bbs = [s.bounding_box() for _, s in solides]
    out = []
    for i in range(len(solides)):
        for k in range(i + 1, len(solides)):
            a, b = bbs[i], bbs[k]
            if (a.min.X > b.max.X or b.min.X > a.max.X or a.min.Y > b.max.Y or b.min.Y > a.max.Y
                    or a.min.Z > b.max.Z or b.min.Z > a.max.Z):
                continue
            ni, nk = solides[i][0], solides[k][0]
            if exclus(ni, nk):
                continue
            r = solides[i][1].intersect(solides[k][1])        # None, un solide ou une ShapeList
            v = 0.0 if r is None else (sum(x.volume for x in r) if isinstance(r, (list, tuple)) else r.volume)
            if v > VOL_MIN:
                out.append(f"{ni} / {nk} : {v:.0f} mm³")
    return out


# ─────────────────────────────────────────────────────── planches
def fleche(cx, cy, horiz):
    h = FLECHE / 2
    if horiz:
        return [[(cx - h, cy), (cx + h, cy)], [(cx + h - 2, cy - 1.5), (cx + h, cy), (cx + h - 2, cy + 1.5)],
                [(cx - h + 2, cy - 1.5), (cx - h, cy), (cx - h + 2, cy + 1.5)]]
    return [[(cx, cy - h), (cx, cy + h)], [(cx - 1.5, cy + h - 2), (cx, cy + h), (cx + 1.5, cy + h - 2)],
            [(cx - 1.5, cy - h + 2), (cx, cy - h), (cx + 1.5, cy - h + 2)]]


def couper_segment(p, q, x0, x1, y0, y1):
    """Liang-Barsky : la partie du segment pq dans le rectangle, ou None."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if abs(pp) < 1e-12:
            if qq < 0:
                return None
        else:
            t = qq / pp
            if pp < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
    if t0 > t1:
        return None
    return (p[0] + t0 * dx, p[1] + t0 * dy), (p[0] + t1 * dx, p[1] + t1 * dy)


def ranger(pieces, recouvrement) -> tuple[list[dict], list[str]]:
    """Étagères sur A4 ; une pièce trop grande pour une feuille est découpée en TUILES qui se recouvrent, avec
    des repères à aligner. `pieces` : (étiquette, contours, sens des cannelures 'a'|'b'). Rend (feuilles, tuilées)."""
    zl, zh = ZONE_PLANCHE
    items, grandes = [], []
    for etq, cont, can in pieces:
        xs = [p[0] for c in cont for p in c]
        ys = [p[1] for c in cont for p in c]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        tourne = w > zl or (h > w and h <= zl)
        if tourne and h <= zl:
            cont = [[(-y, x) for x, y in c] for c in cont]
            can = "b" if can == "a" else "a"
            w, h = h, w
            xs = [p[0] for c in cont for p in c]
            ys = [p[1] for c in cont for p in c]
        cont = [[(x - min(xs), y - min(ys)) for x, y in c] for c in cont]
        if w > zl or h > zh:
            grandes.append((etq, cont, can, w, h))
        else:
            items.append((etq, cont, can, w, h))
    items.sort(key=lambda it: -it[4])
    feuilles, f, x, y, hl = [], None, 0.0, 0.0, 0.0

    def neuve():
        return dict(traits=[], croix=[], etiquettes=[], fleches=[])
    for etq, cont, can, w, h in items:
        if f is None:
            f, x, y, hl = neuve(), 0.0, 0.0, 0.0
        if x + w > zl:
            x, y, hl = 0.0, y + hl + ECART_PLAN, 0.0
        if y + h > zh:
            feuilles.append(f)
            f, x, y, hl = neuve(), 0.0, 0.0, 0.0
        f["traits"] += [[(px + x, py + y) for px, py in c] for c in cont]
        cx, cy = x + w / 2, y + h / 2
        f["etiquettes"].append((x + 1.0, y + h / 2 + (4.0 if h > 14 else 0.0), etq))
        if min(w, h) > FLECHE + 4:
            f["fleches"] += fleche(cx, cy - 3.0, can == "a")
        x += w + ECART_PLAN
        hl = max(hl, h)
    if f is not None:
        feuilles.append(f)
    tuilees = []
    for etq, cont, can, w, h in grandes:
        pas_x, pas_y = zl - recouvrement, zh - recouvrement
        nx, ny = math.ceil((w - recouvrement) / pas_x), math.ceil((h - recouvrement) / pas_y)
        tuilees.append(f"{etq} : {nx} × {ny} feuilles")
        for i in range(nx):
            for k in range(ny):
                x0, y0 = i * pas_x, k * pas_y
                x1, y1 = x0 + zl, y0 + zh
                fe = neuve()
                for c in cont:
                    for a, b in zip(c, c[1:] + c[:1]):
                        s = couper_segment(a, b, x0, x1, y0, y1)
                        if s:
                            fe["traits"].append([(s[0][0] - x0, s[0][1] - y0), (s[1][0] - x0, s[1][1] - y0)])
                # repères de recouvrement : une croix (grise) au milieu de chaque coin de la bande commune
                for cxr in (x0 + recouvrement / 2, x1 - recouvrement / 2):
                    for cyr in (y0 + recouvrement / 2, y1 - recouvrement / 2):
                        fe["fleches"] += [[(cxr - x0 - 3, cyr - y0), (cxr - x0 + 3, cyr - y0)],
                                          [(cxr - x0, cyr - y0 - 3), (cxr - x0, cyr - y0 + 3)]]
                fe["etiquettes"].append((2.0, zh - 6.0, f"{etq} - tuile colonne {i + 1}/{nx}, rangee {k + 1}/{ny} ;"
                                         f" recouvrir de {recouvrement:g} mm, croix sur croix"))
                fe["fleches"] += fleche(zl / 2, zh / 2, can == "a")
                fe["tuile"] = True
                feuilles.append(fe)
    return feuilles, tuilees


# ─────────────────────────────────────────────────────── sorties
def construire(g):
    corps, piv, ec = robot(g)
    plaques = []
    for c in corps:
        for pl in c.plaques():
            plaques.append(pl.finir(g))
    # identifiants : K01, K02… dans l'ordre des corps
    for i, pl in enumerate(plaques, 1):
        pl.id = f"K{i:02d}"
    return corps, plaques, piv, ec


def rendre(solides: list[tuple], png: Path):
    """Image de contrôle : MuJoCo hors écran (même méthode que parts/jambe_basse.py)."""
    import os
    os.environ.setdefault("MUJOCO_GL", "egl")
    import mujoco
    import numpy as np
    sys.path.insert(0, str(REPO / "sim"))
    from render import write_png
    RENDU.mkdir(parents=True, exist_ok=True)
    for f in RENDU.glob("*.stl"):
        f.unlink()
    assets, geoms = [], []
    for i, (nm, s) in enumerate(solides):
        f = RENDU / f"m{i:03d}.stl"
        bd.export_stl(s, str(f))
        assets.append(f'<mesh name="m{i}" file="{f.name}" scale=".001 .001 .001"/>')
        c = ".2 .45 .85 1" if nm.startswith("servo") else (".55 .4 .25 1" if "bouchon" in nm or "serrage" in nm
                                                           else ".82 .68 .48 1")
        geoms.append(f'<geom type="mesh" mesh="m{i}" rgba="{c}" contype="0" conaffinity="0"/>')
    xml = (f'<mujoco><compiler meshdir="{RENDU}"/><visual><global offwidth="1800" offheight="1400"/></visual>'
           f'<asset>{"".join(assets)}</asset><worldbody><light pos="0 -1 1.5" dir="0 .6 -.8"/>'
           f'<light pos="1 1 1.5" dir="-.5 -.5 -.8"/>'
           f'<geom type="plane" size=".6 .6 .01" rgba=".92 .92 .9 1"/>{"".join(geoms)}</worldbody></mujoco>')
    m = mujoco.MjModel.from_xml_string(xml)
    d = mujoco.MjData(m)
    mujoco.mj_forward(m, d)
    images = []
    r = mujoco.Renderer(m, height=1000, width=700)
    try:
        for az, el in ((140, -12), (200, -12), (90, -5)):
            cam = mujoco.MjvCamera()
            cam.lookat[:] = [0, 0, 0.47]
            cam.distance, cam.azimuth, cam.elevation = 1.55, az, el
            r.update_scene(d, camera=cam)
            images.append(r.render())
    finally:
        r.close()
    img = np.concatenate(images, axis=1)
    write_png(str(png), img.tobytes(), img.shape[1], img.shape[0])


def vis_longueur(epaisseur_serree, g) -> int:
    """Longueur de vis du commerce (params/kit.yaml, niveau0) pour une épaisseur serrée (mm)."""
    besoin = epaisseur_serree + 2 * 1.0 + 0.8 * g["vis"]["diametre"] + 2.0   # non-cote: 2 rondelles, écrou, dépassement
    for L in g["n0"]["longueurs_vis"]:
        if L >= besoin:
            return L
    return g["n0"]["longueurs_vis"][-1]


def notice(g, corps, plaques, piv, ec, n_feuilles, tuilees, fautes, inter, masse_g, n_cales) -> str:
    e = g["e"]
    lab = g["kit"]["lab"]
    par = {}
    for pl in plaques:
        par.setdefault(pl.corps, []).append(pl)
    n_inst = sum(len(pl.poses) for pl in plaques)
    L = ["# YXOR Kit, niveau 0 : notice de montage", "",
         "**Engendrée** par `.venv/bin/python parts/kit_niveau0.py` : ne pas éditer à la main. Planches : "
         "`exports/parts/kit_niveau0_planchesA4.pdf` (hors de Git, règle 4 ; régénérées par `scripts/regenerer.py`).",
         "", "Décidé (fiche 0075, Jeremy, 2026-10-08) : assemblage B — tenons et mortaises, colle non porteuse "
         "seulement, pivots par vis traversante. Carton dessiné : ondulé double de "
         f"{f1(e)} mm (la valeur mesurée ; consigne du prompt, pas un choix écrit par Jeremy). Toutes les cotes de "
         "dessin non anthropométriques sont des hypothèses PROPOSÉES (`params/kit.yaml`, `niveau0`).", "",
         "## Ce que donnent les plans", "",
         f"- **{len(plaques)} gabarits, {n_inst} pièces à découper** (les pièces d'un bras ou d'une jambe se coupent "
         f"deux fois : la seconde, gabarit retourné), plus **{n_cales} cales** (rondelles de carton de "
         f"{f1(g['n0']['cale_diametre'], 0)} mm), sur **{n_feuilles} feuilles A4**"
         + (f", dont des grandes pièces en tuiles ({'; '.join(tuilees)})" if tuilees else "") + ".",
         f"- **Carton : {f1(sum(pl.aire * len(pl.poses) for pl in plaques) / 1e6, 2)} m²**, soit **{f1(masse_g, 0)} g** "
         f"à {f1(g['sigma'] * 1000, 0)} g/m² (masse surfacique mesurée), sans les chutes.",
         f"- **Hauteur du Kit : {f1(ec['z_sommet'] / 1000, 3)} m**, contre {f1(g['kit']['kit_taille']['hauteur_reelle_m'], 3)} m "
         "pour le Lab de référence (taille du Kit GELÉE en attendant Jeremy : avec les Feetech aux petits axes, fiche "
         f"0075, le Lab passe à {f1(lab['hauteur_reelle_m'], 3)} m ; `params/kit.yaml`, `kit_taille`). Les longueurs "
         "entre axes sont celles du Lab de référence ; l'écart vient des logements de servo en carton (tableau ci-dessous).",
         "- **Contrôles** : " + ("aucune faute de dessin (rayons rentrants ≥ "
                                 f"{f1(g['r'], 2)} mm, aucun angle rentrant vif, chaque pièce d'un seul tenant)"
                                 if not fautes else f"**{len(fautes)} faute(s) de dessin**")
         + " ; " + ("aucune interpénétration en 3D, servos du niveau 1 et 3 compris (un tenon sans sa mortaise, "
                    "ou un servo qui ne passerait pas, se verrait)" if not inter else
                    f"**{len(inter)} interpénétration(s)** (liste plus bas)") + ".", "",
         "## Hauteurs (axes au repos, debout)", "",
         "| Repère | Kit (mm) | Commentaire |", "| --- | ---: | --- |",
         f"| cheville | {f1(ec['z_cheville'], 0)} | ANSUR {f1(g['L']['cheville_hauteur'], 0)} : le bas du tibia doit passer au-dessus du pied |",
         f"| genou | {f1(ec['z_genou'], 0)} | cheville + tibia (Lab) |",
         f"| hanche, tangage | {f1(ec['z_hanche_tangage'], 0)} | genou + cuisse (Lab) |",
         f"| hanche, roulis | {f1(ec['z_hanche_roulis'], 0)} | trois axes de hanche empilés (chez l'humain, ils se croisent) |",
         f"| dessous du bassin | {f1(ec['z_bassin_bas'], 0)} | servo de lacet de hanche |",
         f"| épaule | {f1(ec['z_epaule'], 0)} | tronc du Lab, rallongé pour l'électronique |",
         f"| cou, tangage | {f1(ec['z_cou_tangage'], 0)} | |",
         f"| sommet | {f1(ec['z_sommet'], 0)} | |", "",
         f"Écart de largeur : le bassin fait {f1(ec['largeur_bassin'], 0)} mm (ANSUR {f1(g['L']['largeur_bassin'], 0)}), "
         "pour loger les deux servos de lacet sous les hanches, à l'écartement ANSUR.", "",
         "## Ce qu'il faut savoir avant de couper", "",
         "1. **Imprimer à 100 %**, sans « ajuster à la page ». Mesurer le réglet de 100 mm de chaque feuille : s'il ne "
         "fait pas exactement 100 mm, réimprimer.",
         "2. **Reporter** : coller la feuille sur le carton (colle en bâton, ou scotch de peintre aux coins), en "
         "alignant la **flèche grise** sur le sens des **cannelures** (les petites arches visibles sur la tranche). "
         "Une pièce coupée à 90° de la flèche plie deux à trois fois plus facilement.",
         "3. **Couper** au cutter, sur une planche ou un carton martyr, contre la règle, en deux ou trois passes "
         "légères plutôt qu'une forte. Les **mortaises** (fentes de la largeur du carton) : deux traits longs, puis "
         "les bouts. Les **petits ronds** aux coins des fentes et des fenêtres (les « os de chien ») laissent entrer "
         "un tenon carré jusqu'au fond : un coup de pointe de cutter suffit.",
         "4. **Trous de pivot** (Ø 4,5 mm) : percer au poinçon ou à la pointe d'un tournevis, puis agrandir en "
         "vissant la vis M4 à travers.",
         "5. **Grandes pièces** (tronc) : imprimées en plusieurs feuilles qui se recouvrent de "
         f"{f1(g['n0']['recouvrement_tuiles'], 0)} mm ; poser les croix grises les unes sur les autres, scotcher, "
         "puis reporter comme une seule feuille.",
         "6. **Côté droit** : les pièces des bras et des jambes se coupent deux fois ; pour la seconde, retourner le "
         "gabarit (le carton n'a pas d'endroit).", "",
         "## Montage d'un caisson (toutes les boîtes se montent pareil)", "",
         "1. Poser un **flanc** à plat.",
         "2. Enfoncer les **tenons** des deux **faces** dans les mortaises du flanc, faces debout.",
         "3. Glisser les **cloisons** et les **plaques à fenêtre** (s'il y en a) : leurs tenons entrent dans les faces "
         "et les flancs.",
         "4. Poser le second flanc par-dessus : tous les tenons dans ses mortaises.",
         "5. Poser les **couvercles** sur les bouts : les tenons des flancs et des faces les traversent.",
         "6. **Colle (non porteuse)** : un point de colle chaude sur un tenon qui dépasse, pour qu'il ne ressorte "
         "pas. Jamais entre deux pièces qui portent un effort, jamais sur un bouchon ni une plaque de serrage "
         "(ils s'enlèvent au niveau 1).", "",
         "## Logements de servo : ce qui se pose au niveau 0", "",
         "Chaque logement est une **fenêtre** dans une paroi, à la taille du servo STS3215 "
         f"({f1(g['sv']['A'], 2)} × {f1(g['sv']['B'], 2)} mm, plus {f1(g['j'], 1)} mm de jeu), et une **plaque à "
         "fenêtre** intérieure qui tiendra le servo à mi-hauteur. Au niveau 0 :",
         "- le **bouchon** (pièce à la taille de la fenêtre, percée sur l'axe) ferme la fenêtre ;",
         "- la **plaque de serrage** (un peu plus grande) se pose derrière, à l'intérieur ;",
         "- la vis du pivot traverse : oreille ou couvercle de l'enfant, deux **cales** (rondelles de carton), "
         "bouchon, plaque de serrage ; écrou à frein derrière.",
         "Au niveau 1 (ou 3), on retire la vis, le bouchon et la plaque de serrage, on glisse le servo par la "
         "fenêtre, sa sortie à l'emplacement du trou : **rien n'est redécoupé**. Les trous du palonnier "
         "se percent alors dans l'oreille, d'après le palonnier livré (non coté par Feetech).", "",
         "## Pivots", "",
         "| Articulation | Sorte | Parent → enfant | Nombre | Vis côté servo | Vis côté opposé | Cales côté opposé |",
         "| --- | --- | --- | ---: | --- | --- | --- |"]
    for p in piv:
        horn = vis_longueur(5 * e, g) if "passi" not in p["sorte"] else None
        cale = p["cale_idler"]
        n_cales = int(cale // e)
        idler = vis_longueur(2 * e + cale, g)
        cote = "—" if p["sorte"].startswith("plateau") else f"M{g['vis']['diametre']:g}×{idler}"
        L.append(f"| {p['nom']} | {p['sorte']} | {p['parent']} → {p['enfant']} | {p['n']} | "
                 f"{'M%g×%d' % (g['vis']['diametre'], horn) if horn else 'M%g×%d' % (g['vis']['diametre'], vis_longueur(2 * e, g))} | "
                 f"{cote} | {n_cales} cale(s) de carton + {f1(cale - n_cales * e, 1)} mm en rondelles"
                 + (" |" if not p["sorte"].startswith("plateau") else " |"))
    # liste à réunir (calculée)
    vis = {}
    for p in piv:
        passif = "passi" in p["sorte"]
        horn = vis_longueur(2 * e if passif else 5 * e, g)
        vis[horn] = vis.get(horn, 0) + p["n"]
        if not p["sorte"].startswith("plateau"):
            idl = vis_longueur(2 * e + p["cale_idler"], g)
            vis[idl] = vis.get(idl, 0) + p["n"]
    n_vis = sum(vis.values())
    aire = sum(pl.aire * len(pl.poses) for pl in plaques) / 1e6
    d = g["vis"]["diametre"]
    a_reunir = [
        f"carton ondulé **double cannelure** de {f1(e)} mm (cartons de déménagement de récupération) : "
        f"**{f1(aire * g['n0']['facteur_chutes'], 1)} m²** au moins ({f1(aire, 2)} m² de pièces × "
        f"{f1(g['n0']['facteur_chutes'], 1)} pour les chutes, PROPOSÉ), plats, secs, sans pli marqué ;",
        f"**{n_vis} vis M{d:g}** à tête, " + ", ".join(f"{n} × {L} mm" for L, n in sorted(vis.items()))
        + f" ; **{n_vis} écrous M{d:g} à frein** (nylstop) ; **{2 * n_vis} rondelles larges M{d:g}** ;",
        f"**{n_feuilles} feuilles A4** imprimées à 100 %, colle en bâton ou scotch de peintre pour les poser sur le carton ;",
        "outils (décidés, fiche 0074) : **cutter** (lames neuves), **règle métallique**, **équerre**, **pistolet à colle** "
        "(colle non porteuse seulement) ; un **carton martyr** ou une planche sous la coupe ; un **tournevis cruciforme** "
        "ou un poinçon pour amorcer les trous Ø 4,5 ; un tournevis ou une clé pour les vis M4."]
    L += ["", "## Ce qu'il faut réunir pour le niveau 0", ""] + [f"- {x}" for x in a_reunir]
    L += ["", "« Plateau » : l'enfant est vissé par un couvercle sur la sortie du servo (un seul pivot) ; « chape » : "
          "les oreilles de l'enfant encadrent le parent, un pivot de chaque côté, sur le même axe. Le débattement "
          "libre garanti par le dessin est de ±15° autour de la pose debout (PROPOSÉ) ; au-delà, à essayer.", "",
          "## Ordre de montage du robot", "",
          "1. **Jambes** (×2) : pied, tibia (avec ses deux bouchons), cuisse ; pivots de cheville et de genou.",
          "2. **Hanches** (×2) : noix 2 sur la cuisse (tangage), noix 1 dans les oreilles de la noix 2 (roulis).",
          "3. **Bassin** : visser chaque noix 1 sous le couvercle bas (lacets de hanche).",
          "4. **Tronc** sur le couvercle haut du bassin (lacet de taille).",
          "5. **Épaules** (×2) sur les flancs du tronc, puis **bras**, **avant-bras**, **poignet**, **main**.",
          "6. **Cou** sur le couvercle haut du tronc, puis **tête**.", "",
          "## Pièces par caisson", "",
          "| Caisson | Pièces (identifiant, nom, nombre à couper, dimensions en mm) |", "| --- | --- |"]
    for c in corps:
        pls = par.get(c.nom, [])
        L.append(f"| {c.nom} | " + " ; ".join(f"{pl.id} {pl.nom.split('.', 1)[1]} ×{len(pl.poses)} "
                                             f"({f1(pl.dims[0], 0)} × {f1(pl.dims[1], 0)})" for pl in pls) + " |")
    if fautes or inter:
        L += ["", "## Défauts relevés par les contrôles", ""] + [f"- {x}" for x in fautes + inter]
    return "\n".join(L) + "\n"


def f1(x, n=1):
    return "—" if x is None else f"{x:,.{n}f}".replace(",", " ").replace(".", ",")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--rendu", action="store_true", help="image de contrôle (MuJoCo, EGL)")
    ap.add_argument("--sans-3d", action="store_true", help="sans le contrôle d'interpénétration (rapide)")
    a = ap.parse_args(argv)
    # construction Docker (scripts/regenerer.py sur le VPS) : docs/ n'est pas dans l'image et le VPS ne calcule pas
    # (CLAUDE.md) ; la notice et le contrôle 3D SAUTENT, et le disent (le contrôle 3D tourne en local et aux tests)
    docker = not NOTICE.parent.exists()
    if docker:
        a.sans_3d = True
    g = donnees()
    corps, plaques, piv, ec = construire(g)
    SORTIE.mkdir(parents=True, exist_ok=True)
    # contrôles 2D
    fautes = []
    pieces = []
    for pl in plaques:
        cont = polylignes_depuis_face(pl.face.faces()[0])
        fautes += [f"{pl.id} {pl.nom} : {x}" for x in controler_2d(cont, g["r"])]
        for k in range(len(pl.poses)):
            pieces.append((f"{pl.id} {pl.nom}" + (f" ({'G' if k == 0 else 'D'})" if len(pl.poses) > 1 else ""),
                           cont, pl.cannelures))
    # cales (rondelles de carton) : côté servo pour chaque pivot motorisé, côté opposé selon l'écart
    n_cales = 0
    for p in piv:
        cote_servo = 0 if "passi" in p["sorte"] else g["n0"]["cales_palonnier"]
        n_cales += p["n"] * (cote_servo + int(p["cale_idler"] // g["e"]))
    cale = disque(0, 0, g["n0"]["cale_diametre"] / 2) - disque(0, 0, g["d"] / 2)
    cont_cale = polylignes_depuis_face(cale.faces()[0])
    pieces += [(f"cale {i + 1}/{n_cales}", cont_cale, "a") for i in range(n_cales)]
    # contrôle 3D : toutes les plaques posées, et les servos des niveaux 1 et 3 dans leurs logements
    solides = []
    for pl in plaques:
        for k, s in enumerate(pl.solides()):
            solides.append((f"{pl.id} {pl.nom}" + (" (droit)" if k else ""), s))
    servos = [x for c in corps for x in c.servos()]
    inter = []
    if not a.sans_3d:
        def exclus(n1, n2):
            # bouchons et plaques de serrage n'existent qu'au niveau 0, les servos qu'aux niveaux 1 et 3
            n0 = ("bouchon" in n1 or "serrage" in n1, "bouchon" in n2 or "serrage" in n2)
            sv = (n1.startswith("servo"), n2.startswith("servo"))
            return (n0[0] and sv[1]) or (n0[1] and sv[0])
        inter = interferences(solides + servos, exclus)
    # planches
    feuilles, tuilees = ranger(pieces, g["n0"]["recouvrement_tuiles"])
    from empreinte import empreinte as _emp
    n = ecrire_planches_a4(feuilles, SORTIE / f"{NOM}_planchesA4.pdf",
                           "YXOR Kit - niveau 0, carton ondule double 3,5 mm",
                           [f"{len(pieces)} pieces, echelle 1:1. Empreinte {_emp()} : verifier avant de couper.",
                            "Fleche grise = sens des cannelures. Notice : docs/kit-montage-niveau0.md.",
                            "Gabarits des bras et des jambes : couper 2 fois (le 2e retourne)."])
    comp = bd.Compound(children=[s for _, s in solides])
    bd.export_step(comp, str(SORTIE / f"{NOM}_assemblage.step"), unit=bd.Unit.MM)
    masse = sum(pl.aire * len(pl.poses) for pl in plaques) * g["sigma"] / 1000.0
    if not docker:
        NOTICE.write_text(notice(g, corps, plaques, piv, ec, n, tuilees, fautes, inter, masse, n_cales), encoding="utf-8")
    print(f"  {len(plaques)} gabarits, {len(pieces) - n_cales} pièces et {n_cales} cales, {n} feuilles A4"
          + (f" (tuiles : {'; '.join(tuilees)})" if tuilees else ""))
    print(f"  carton {sum(pl.aire * len(pl.poses) for pl in plaques) / 1e6:.2f} m², {masse:.0f} g ; "
          f"hauteur {ec['z_sommet']:.0f} mm")
    print(f"  contrôles 2D : {len(fautes)} faute(s) sur {len(plaques)} gabarits ; 3D : "
          + (("SAUTÉ (construction Docker : docs/ absent, pas de calcul sur le VPS)" if docker else "SAUTÉ (--sans-3d)")
             if a.sans_3d else f"{len(inter)} interpénétration(s) sur {len(solides)} plaques "
             f"et {len(servos)} servos"))
    for x in (fautes + inter)[:25]:
        print("    ✗ " + x)
    if a.rendu:
        png = RENDU / f"{NOM}.png"
        rendre(solides + servos, png)
        print(f"  -> {png.relative_to(REPO)}")
    print(f"  -> {NOTICE.relative_to(REPO)}" if not docker else "  notice SAUTÉE (construction Docker : docs/ absent)")
    return 1 if (fautes or inter) else 0


if __name__ == "__main__":
    sys.exit(main())
