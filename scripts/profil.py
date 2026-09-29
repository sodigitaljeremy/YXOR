#!/usr/bin/env python3
"""Contour de la semelle, calculé SANS noyau CAO.

═══════════════════════════════════════════════════════════════════════
 POURQUOI CE FICHIER EXISTE, ET LE DANGER QU'IL PORTE
═══════════════════════════════════════════════════════════════════════

Le navigateur ne peut pas exécuter build123d. Pour recalculer un schéma
en direct dans la page, il faut une SECONDE implémentation de la forme.

Deux implémentations de la même chose divergent. Toujours. Et celle-ci
divergerait de la pire façon : le dessin resterait plausible, seulement
faux de deux dixièmes.

D'où la règle que ce fichier impose : **la version analytique est
vérifiée contre la version build123d à chaque régénération**, et la
pièce refuse de se produire si l'écart dépasse la tolérance. La
divergence reste possible ; elle ne peut plus être silencieuse.

═══════════════════════════════════════════════════════════════════════
 LA FORME, EN GÉOMÉTRIE ÉLÉMENTAIRE
═══════════════════════════════════════════════════════════════════════

Un rectangle L x W, ses quatre coins arrondis au rayon `r_ext`, deux
cercles de rayon `R` soustraits sur les flancs pour creuser la taille,
et les quatre raccords ainsi créés adoucis au rayon `r_int`.

Un CONGÉ (fillet) est un raccord en arc de cercle entre deux bords. Un
angle rentrant vif concentre l'effort et déchire le carton ; l'arc
répartit. C'est pourquoi le procédé impose un rayon minimal.

Deux longueurs se déduisent, et il vaut la peine de voir d'où :

  * Le cercle soustrait coupe le bord droit (y = W/2) en x = ± e/2, où
    `e` est l'étendue du creux. Ce n'est pas une coïncidence : R est
    justement défini comme le rayon du segment circulaire de corde `e`
    et de flèche `p`, donc R = (e²/4 + p²) / 2p, d'où 2Rp - p² = e²/4.

  * Le centre d'un congé r_int est à `r_int` du bord droit, donc en
    y = W/2 - r_int, et à R + r_int du centre du cercle creusé, puisque
    la matière est À L'EXTÉRIEUR de ce cercle. Il vient

        xf = racine( p x (2R + 2 r_int - p) )

    et xf > e/2 : le congé mord sur le bord droit, comme attendu.
"""
from __future__ import annotations
import math

TOLERANCE_MM = 0.05          # écart maximal admis avec build123d


def cotes(H_m: float, r_pied_long: float, r_pied_larg: float,
          ratio_resserrement: float, ratio_coins: float,
          ratio_etendue: float, epaisseur: float) -> dict:
    """Toutes les cotes, depuis H et les ratios. Millimètres.

    Une seule règle de nature `procede` est appliquée ici : le rayon
    intérieur minimal vaut 0,5 x l'épaisseur (CLAUDE.md). Les autres
    cotes sont de nature `echelle` et dérivent de H (règle 1).
    """
    L = round(H_m * 1000.0 * r_pied_long, 4)
    W = round(H_m * 1000.0 * r_pied_larg, 4)
    r_ext = round(W * ratio_coins, 4)
    p = round((W - W * ratio_resserrement) / 2.0, 4)      # par flanc
    e = round(L * ratio_etendue, 4)
    r_int = round(0.5 * epaisseur, 4)
    R = round((e ** 2 / 4.0 + p ** 2) / (2.0 * p), 4) if p > 0 else 0.0
    return dict(L=L, W=W, r_ext=r_ext, profondeur=p, etendue=e,
                R=R, r_int=r_int, ep=epaisseur,
                largeur_creux=round(W * ratio_resserrement, 4))


def diagnostic(d: dict) -> list[str]:
    """Ce qui rend la forme impossible. Dit, jamais tu."""
    m = []
    if d["profondeur"] <= 0:
        m.append("resserrement à 1 : il n'y a plus de creux, "
                 "donc plus d'angle rentrant à exercer")
    elif d["R"] < d["r_int"]:
        m.append(f"le creux a un rayon de {d['R']:.2f} mm, sous le minimum "
                 f"{d['r_int']:.2f} mm du procédé : infaisable")
    if d["r_ext"] > d["W"] / 2:
        m.append(f"congé de coin {d['r_ext']:.2f} mm > demi-largeur "
                 f"{d['W']/2:.2f} mm")
    if 2 * d["r_ext"] > d["L"]:
        m.append("les congés de coin se rejoignent sur la longueur")
    if d["profondeur"] >= d["W"] / 2:
        m.append("le creux traverse la pièce de part en part")
    xf2 = d["profondeur"] * (2 * d["R"] + 2 * d["r_int"] - d["profondeur"])
    if xf2 > 0 and math.sqrt(xf2) > d["L"] / 2 - d["r_ext"]:
        m.append("le congé du creux déborde sur le congé de coin")
    return m


def _distance_au_segment(p, a, b) -> float:
    px, py = p
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def hausdorff(A, B) -> float:
    """Plus grand écart d'un point de A au contour B.

    Mesuré point-à-SEGMENT, pas point-à-point : sinon on mesurerait la
    densité d'échantillonnage et non la forme. Les deux sens doivent être
    contrôlés — un contour qui oublierait un creux resterait proche dans
    un sens et pas dans l'autre.
    """
    return max(min(_distance_au_segment(p, B[i], B[(i + 1) % len(B)])
                   for i in range(len(B))) for p in A)


def aire(contour) -> float:
    """Aire algébrique du contour, par la formule du lacet.

    ⚠ ELLE MESURE CE QUE HAUSDORFF NE VOIT PAS : l'ORDRE des points.

    Un contour dont les points sont tous à leur place mais parcourus dans
    le désordre reste à distance nulle du bon contour — Hausdorff compare
    des ENSEMBLES. Son aire, elle, s'effondre : le 2026-09-30, un contour
    à 0,0022 mm du noyau CAO avait une aire de 3605,90 mm² au lieu de
    6300,49, parce que le bas était parcouru à l'envers et que la boucle
    se refermait en huit.

    Le défaut a été trouvé par une MESURE PHYSIQUE — il fallait l'aire
    pour convertir 4 g en masse surfacique — et non par un contrôle.
    Celui-ci existe désormais.
    """
    n = len(contour)
    return abs(sum(contour[i][0] * contour[(i + 1) % n][1]
                   - contour[(i + 1) % n][0] * contour[i][1]
                   for i in range(n))) / 2.0


def _arc(cx, cy, r, a0, a1, n):
    """Échantillonne un arc. `a1` peut être inférieur à `a0` : on tourne
    alors dans l'autre sens. Le premier point est omis — il appartient au
    tronçon précédent, et le dupliquer casserait le DXF."""
    return [(cx + r * math.cos(a0 + (a1 - a0) * i / n),
             cy + r * math.sin(a0 + (a1 - a0) * i / n))
            for i in range(1, n + 1)]


def contour(d: dict, n_arc: int = 48) -> list[tuple[float, float]]:
    """Le contour fermé, en polyligne, sens direct.

    Lève ValueError si la forme est impossible : mieux vaut pas de dessin
    qu'un dessin faux.
    """
    mauvais = diagnostic(d)
    if mauvais:
        raise ValueError(mauvais[0])

    L, W, re_, R, p, ri = (d["L"], d["W"], d["r_ext"], d["R"],
                           d["profondeur"], d["r_int"])
    x0, y0 = L / 2.0, W / 2.0
    yc = y0 - p + R                       # centre du cercle creusé, en haut
    xf = math.sqrt(p * (2 * R + 2 * ri - p))
    yf = y0 - ri                          # centre d'un congé de creux

    # Point de tangence entre le congé et le cercle creusé : sur la droite
    # qui joint les deux centres, à R du centre du cercle.
    def tangence(sx):
        dx, dy = sx * xf - 0.0, yf - yc
        n = math.hypot(dx, dy)            # vaut R + ri, par construction
        return (R * dx / n, yc + R * dy / n)

    pts: list[tuple[float, float]] = [(x0, -y0 + re_)]

    def bord(sy):
        """Un bord long (haut si sy=+1), de droite à gauche puis retour."""
        s = []
        # coin, du flanc vers le bord long
        s += _arc(x0 - re_, sy * (y0 - re_), re_, 0.0, sy * math.pi / 2, n_arc // 3)
        s.append((xf, sy * y0))
        # congé du creux, côté droit
        tx, ty = tangence(+1)
        a0 = math.atan2(sy * y0 - sy * yf, xf - xf) if False else math.pi / 2
        a1 = math.atan2(sy * ty - sy * yf, tx - xf)
        s += _arc(xf, sy * yf, ri, sy * a0, sy * a1, n_arc // 3)
        # le creux lui-même, de droite à gauche
        txl, tyl = tangence(-1)
        b0 = math.atan2(sy * ty - sy * yc, tx)
        b1 = math.atan2(sy * tyl - sy * yc, txl)
        s += _arc(0.0, sy * yc, R, sy * b0, sy * b1, n_arc)
        # congé du creux, côté gauche
        c0 = math.atan2(sy * tyl - sy * yf, txl + xf)
        s += _arc(-xf, sy * yf, ri, sy * c0, sy * math.pi / 2, n_arc // 3)
        s.append((-xf, sy * y0))
        s.append((-(x0 - re_), sy * y0))
        # coin, du bord long vers le flanc
        s += _arc(-(x0 - re_), sy * (y0 - re_), re_, sy * math.pi / 2, math.pi,
                  n_arc // 3)
        return s

    pts.append((x0, y0 - re_))
    haut = bord(+1)
    pts += haut
    pts.append((-x0, -(y0 - re_)))      # flanc gauche, de haut en bas
    # Le bas est le miroir du haut. Le miroir (x,y) -> (-x,-y) le parcourt
    # DÉJÀ de gauche à droite : le renverser en plus faisait repartir du
    # coin bas-DROIT alors qu'on se trouve en bas à GAUCHE, et le contour
    # se refermait en huit.
    #
    # La forme restait juste point par point — écart de Hausdorff 0,0022 mm
    # contre le noyau CAO — mais son AIRE valait 3605,90 mm² au lieu de
    # 6300,49. Hausdorff mesure une distance point-à-ensemble : il est
    # aveugle à l'ordre. Trouvé le 2026-09-30, en calculant l'aire pour
    # une masse surfacique. C'est une mesure PHYSIQUE qui a révélé le
    # défaut, pas un contrôle.
    pts += [(-x, -y) for x, y in haut]
    return pts
