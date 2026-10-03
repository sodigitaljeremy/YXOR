#!/usr/bin/env python3
"""Plan de découpe imprimable A4, à l'échelle 1:1, à scotcher sur la matière.

Module réutilisable par toute pièce. Se lance avec le venv DU PROJET.

Pourquoi un PDF et non une image : un PDF porte ses dimensions en points
typographiques, donc une imprimante peut le rendre à l'échelle exacte. Un
PNG n'a pas d'échelle — il a une résolution, ce qui n'est pas la même
chose et se traduit par une pièce fausse.

⚠ Le piège réel n'est pas le format mais le PILOTE D'IMPRESSION : presque
  tous proposent « ajuster à la page », qui réduit de 3 à 5 %. Une semelle
  de 137 mm sortirait à 131 mm sans qu'aucun message n'apparaisse — et la
  pièce serait fausse de 4 %.
  D'où le RÉGLET DE CONTRÔLE imprimé sur chaque plan : on le mesure au
  pied à coulisse AVANT de couper. S'il ne fait pas exactement 100,0 mm,
  le tirage est à refaire à 100 %, sans mise à l'échelle.
"""
from __future__ import annotations

import zlib
from pathlib import Path

MM = 72.0 / 25.4          # points typographiques par millimètre
A4_L, A4_H = 210.0, 297.0  # mm — norme ISO 216


def _echap(t: str) -> str:
    for k, v in _TRANSLIT.items():
        t = t.replace(k, v)
    return t.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


# Le jeu WinAnsi ne contient ni tiret cadratin, ni guillemets typographiques,
# ni espace insécable : sans translittération ils s'impriment en « ? » sur la
# feuille. Corrigé ici plutôt que d'imposer une saisie appauvrie aux appelants.
_TRANSLIT = {"\u2014": "-", "\u2013": "-", "\u2026": "...", "\u00a0": " ",
             "\u2019": "'", "\u2018": "'", "\u201c": '"', "\u201d": '"',
             "\u00d7": "x", "\u2264": "<=", "\u2265": ">=", "\u00b1": "+/-"}


def _latin(t: str) -> bytes:
    for k, v in _TRANSLIT.items():
        t = t.replace(k, v)
    return t.encode("latin-1", "replace")


def polylignes_depuis_face(face, tol_corde: float = 0.05) -> list[list[tuple]]:
    """Discrétise les contours d'une face en polylignes (mm).

    `tol_corde` borne l'écart entre la corde et la vraie courbe. À 0,05 mm
    l'écart est très en dessous de ce qu'un cutter tenu à la main peut
    suivre : la polyligne n'est pas une approximation gênante ici.
    """
    import math
    contours = []
    for fil in [face.outer_wire(), *face.inner_wires()]:
        pts: list[tuple] = []
        for arete in fil.edges():
            longueur = arete.length
            # une corde de flèche `tol` sur un rayon `r` couvre un angle
            # 2*acos(1 - tol/r) ; on majore simplement par la longueur
            n = max(2, min(400, int(math.ceil(longueur / max(tol_corde, 1e-3) ** 0.5))))
            for i in range(n + 1):
                v = arete @ (i / n)
                p = (round(v.X, 4), round(v.Y, 4))
                if not pts or p != pts[-1]:
                    pts.append(p)
        if pts and pts[0] != pts[-1]:
            pts.append(pts[0])
        contours.append(pts)
    return contours


def ecrire_plan_a4(contours, chemin, titre, lignes_info, marge=15.0, fleche=None):
    """Écrit le plan A4. `contours` en mm, origine quelconque : recentré.

    `fleche` = (angle_deg, texte) pour un matériau ANISOTROPE. Sans elle,
    déclarer un sens de fibre dans un relevé ne sert à rien : au moment
    de poser le plan sur la matière, personne ne sait comment l'orienter.
    """
    xs = [p[0] for c in contours for p in c]
    ys = [p[1] for c in contours for p in c]
    larg, haut = max(xs) - min(xs), max(ys) - min(ys)
    if larg > A4_L - 2 * marge or haut > A4_H - 2 * marge - 60:
        raise ValueError(f"la pièce ({larg:.1f} x {haut:.1f} mm) ne tient pas "
                         f"sur une A4 avec {marge} mm de marge")
    # recentrée horizontalement, posée sous le bandeau de titre
    dx = (A4_L - larg) / 2 - min(xs)
    dy = A4_H - marge - 52 - haut - min(ys)

    ops: list[str] = []
    def txt(x, y, s, taille=9):
        ops.append("BT /F1 %.1f Tf %.4f %.4f Td (%s) Tj ET"
                   % (taille, x * MM, y * MM, _echap(s)))

    ops.append("1 J 1 j")                      # bouts et raccords arrondis
    ops.append("0 0 0 RG 0.6 w")               # trait de coupe : noir, 0,6 pt
    for c in contours:
        ops.append(f"{(c[0][0]+dx)*MM:.4f} {(c[0][1]+dy)*MM:.4f} m")
        for x, y in c[1:]:
            ops.append(f"{(x+dx)*MM:.4f} {(y+dy)*MM:.4f} l")
        ops.append("h S")

    # ── flèche de sens de matière, si le matériau est orienté ──────────
    if fleche:
        import math as _m
        ang, texte = fleche
        yf = dy + min(ys) - 16.0
        xc, lf = A4_L / 2, 34.0
        ca, sa = _m.cos(_m.radians(ang)), _m.sin(_m.radians(ang))
        x1, y1 = xc - lf / 2 * ca, yf - lf / 2 * sa
        x2, y2 = xc + lf / 2 * ca, yf + lf / 2 * sa
        ops.append("1.1 w")
        ops.append(f"{x1*MM:.4f} {y1*MM:.4f} m {x2*MM:.4f} {y2*MM:.4f} l S")
        for d in (150, -150):                       # les deux barbes
            bx = x2 + 6.0 * _m.cos(_m.radians(ang + d))
            by = y2 + 6.0 * _m.sin(_m.radians(ang + d))
            ops.append(f"{x2*MM:.4f} {y2*MM:.4f} m {bx*MM:.4f} {by*MM:.4f} l S")
        ops.append("0.6 w")
        txt(xc - lf / 2, yf - 9.5, texte, 9)

    # ── réglet de contrôle : 100 mm exactement, gradué tous les 10 mm ──
    y0 = marge + 24
    x0 = (A4_L - 100.0) / 2
    ops.append("0.4 w")
    ops.append(f"{x0*MM:.4f} {y0*MM:.4f} m {(x0+100)*MM:.4f} {y0*MM:.4f} l S")
    for i in range(11):
        h = 4.0 if i % 5 == 0 else 2.0
        x = x0 + i * 10.0
        ops.append(f"{x*MM:.4f} {y0*MM:.4f} m {x*MM:.4f} {(y0+h)*MM:.4f} l S")

    txt(marge, A4_H - marge - 6, titre, 14)
    y = A4_H - marge - 20
    for l in lignes_info:
        txt(marge, y, l, 8.5)
        y -= 10.5
    txt(x0, y0 - 9, "REGLET DE CONTROLE — doit mesurer exactement 100,0 mm", 8)
    txt(x0, y0 - 18.5,
        "Sinon : reimprimer a 100 %, sans « ajuster a la page ». Verifier AVANT de couper.", 7.5)

    flux = zlib.compress(_latin("\n".join(ops)))
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %.4f %.4f] "
        b"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>"
        % (A4_L * MM, A4_H * MM),
        b"<< /Length %d /Filter /FlateDecode >>\nstream\n" % len(flux) + flux + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
    ]
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    pos = []
    for i, o in enumerate(objs, 1):
        pos.append(len(out))
        out += b"%d 0 obj\n" % i + o + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    for p in pos:
        out += b"%010d 00000 n \n" % p
    out += (b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n"
            % (len(objs) + 1, xref))
    Path(chemin).parent.mkdir(parents=True, exist_ok=True)
    Path(chemin).write_bytes(bytes(out))
    return larg, haut


# ═══════════════════════════════════════════════════════════════════════
#  SCHÉMA COTÉ EN SVG — même source de contours que le plan A4
# ═══════════════════════════════════════════════════════════════════════
#
#  Le geste emprunté à McMaster-Carr : le dessin porte des lettres, le
#  tableau porte les mêmes. Le lien entre la forme et la valeur est
#  immédiat, sans légende ni renvoi.
#
#  Le LETTRAGE n'est pas l'ordre du fichier : un mécanicien lit du
#  général au particulier. L'ordre est donc hors-tout, puis cotes
#  dérivées, puis cotes de procédé — c'est `ordonner_cotes` qui le fixe,
#  une fois pour toutes les pièces à venir.

RANGS = ("hors_tout", "derivee", "procede")


def ordonner_cotes(cotes: list[dict]) -> list[dict]:
    """Trie par rang de lecture et attribue les lettres A, B, C…"""
    rang_de = {r: i for i, r in enumerate(RANGS)}
    tri = sorted(cotes, key=lambda c: (rang_de.get(c.get("rang"), 99),
                                       cotes.index(c)))
    for i, c in enumerate(tri):
        c["lettre"] = chr(ord("A") + i) if i < 26 else f"A{i}"
    return tri


def _fmt(v) -> str:
    return f"{v:.2f}".rstrip("0").rstrip(".").replace(".", ",")


# Les repères d'annotation ne sont plus des NOMBRES publiés par la pièce,
# mais des FORMES LINÉAIRES sur ses cotes : x = somme(coefficient x cote).
# Toutes le sont, sans exception — un repère est toujours « une fraction de
# la longueur » ou « la demi-largeur moins une marge ».
#
# Motif : ces repères étaient recopiés en dur dans web/simulateur.js. Les
# publier en coefficients supprime la recopie au lieu de la surveiller :
# les deux dessinateurs évaluent la MÊME déclaration.
BASES_TRACE = ("L", "W", "r_ext", "r_int", "ep", "largeur_creux", "un")


def evaluer_trace(trace: dict, cotes: dict) -> dict:
    """Remplace chaque forme linéaire par sa valeur, pour ces cotes-ci."""
    base = dict(cotes)
    base["un"] = 1.0
    out = {}
    for cle, v in trace.items():
        if not isinstance(v, dict):
            out[cle] = v                      # `type`, et tout scalaire
            continue
        inconnues = set(v) - set(BASES_TRACE)
        if inconnues:
            raise ValueError(f"repère « {cle} » : base inconnue {inconnues}")
        out[cle] = round(sum(base[b] * c for b, c in v.items()), 4)
    return out


def svg_schema(contours, cotes, largeur_px=560, valeurs=None) -> str:
    """Schéma coté, en SVG inline. Unités du dessin : millimètres.

    L'axe Y du SVG descend, celui de la pièce monte : les ordonnées sont
    donc niées. On ne passe pas par un `scale(1,-1)`, qui retournerait
    aussi les textes.
    """
    xs = [p[0] for c in contours for p in c]
    ys = [p[1] for c in contours for p in c]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    L, H = x1 - x0, y1 - y0
    ech = max(L, H)
    tp = ech * 0.030                          # taille de texte
    tr = ech * 0.0045                         # épaisseur de trait
    # Une cote qui ne se trace pas (l'épaisseur, par exemple : elle est
    # perpendiculaire à la feuille) devient une NOTE sous le dessin. Le bas
    # de la vue est agrandi d'autant, sinon la note sort du cadre.
    notes = [c for c in cotes if (c.get("trace") or {}).get("type") == "note"]
    mg = ech * 0.09                           # marges gauche et haut
    md = ech * 0.13                           # marge droite
    mb = md + len(notes) * tp * 1.55          # marge basse, notes comprises
    vb = (x0 - mg, -(y1 + mg), L + mg + md, H + mg + mb)

    o = [f'<svg viewBox="{vb[0]:.3f} {vb[1]:.3f} {vb[2]:.3f} {vb[3]:.3f}" '
         f'width="100%" style="max-width:{largeur_px}px" '
         f'xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="schéma coté de la pièce">',
         f'<g fill="none" stroke="currentColor" stroke-width="{tr*2:.4f}" '
         f'stroke-linejoin="round" stroke-linecap="round">']
    for c in contours:
        d = "M " + " L ".join(f"{x:.3f} {-y:.3f}" for x, y in c) + " Z"
        o.append(f'<path d="{d}"/>')
    o.append("</g>")

    o.append(f'<g stroke="currentColor" stroke-width="{tr:.4f}" fill="none" '
             f'opacity="0.62">')
    lignes_txt = []

    def fleche(x, y, dx, dy):
        import math
        a = math.atan2(dy, dx)
        s = ech * 0.014
        for d in (2.6, -2.6):
            o.append(f'<path d="M {x:.3f} {-y:.3f} L '
                     f'{x - s*math.cos(a+d):.3f} {-(y - s*math.sin(a+d)):.3f}"/>')

    def etiquette(x, y, lettre, valeur, ancre="middle", dessous=False):
        # Un renvoi qui descend emmène son texte vers le BAS : posé au-dessus,
        # il retomberait sur la ligne de cote hors-tout, qui passe juste là.
        dy_txt = tp * 0.95 if not dessous else -tp * 1.15
        lignes_txt.append(
            f'<circle cx="{x:.3f}" cy="{-y:.3f}" r="{tp*0.62:.3f}" '
            f'fill="currentColor" opacity="0.14" stroke="none"/>'
            f'<text x="{x:.3f}" y="{-y + tp*0.34:.3f}" text-anchor="middle" '
            f'font-size="{tp*0.78:.3f}" font-weight="700" '
            f'fill="currentColor" stroke="none">{lettre}</text>'
            f'<text x="{x:.3f}" y="{-y - dy_txt:.3f}" text-anchor="{ancre}" '
            f'font-size="{tp*0.74:.3f}" fill="currentColor" opacity="0.72" '
            f'stroke="none">{valeur}</text>')

    for c in cotes:
        t = c.get("trace") or {}
        if valeurs:
            t = evaluer_trace(t, valeurs)
        typ, lettre = t.get("type"), c["lettre"]
        val = f"{_fmt(c['valeur'])}"
        if typ == "cote_h":
            a, b = t["x1"], t["x2"]
            yl = y0 - md * 0.58
            for x in (a, b):
                o.append(f'<path d="M {x:.3f} {-y0:.3f} L {x:.3f} {-(yl - ech*0.012):.3f}"/>')
            o.append(f'<path d="M {a:.3f} {-yl:.3f} L {b:.3f} {-yl:.3f}"/>')
            fleche(a, yl, 1, 0); fleche(b, yl, -1, 0)
            etiquette((a + b) / 2, yl, lettre, val)
        elif typ == "cote_v":
            a, b = t["y1"], t["y2"]
            xl = x1 + md * 0.55
            for y in (a, b):
                o.append(f'<path d="M {x1:.3f} {-y:.3f} L {xl + ech*0.012:.3f} {-y:.3f}"/>')
            o.append(f'<path d="M {xl:.3f} {-a:.3f} L {xl:.3f} {-b:.3f}"/>')
            fleche(xl, a, 0, 1); fleche(xl, b, 0, -1)
            etiquette(xl, (a + b) / 2, lettre, val)
        elif typ == "cote_v_int":
            x, a, b = t["x"], t["y1"], t["y2"]
            o.append(f'<path d="M {x:.3f} {-a:.3f} L {x:.3f} {-b:.3f}"/>')
            fleche(x, a, 0, 1); fleche(x, b, 0, -1)
            etiquette(x, (a + b) / 2, lettre, val)
        elif typ == "rayon":
            px, py = t["x"], t["y"]
            lx, ly = px + t.get("dx", ech * 0.10), py + t.get("dy", ech * 0.10)
            o.append(f'<path d="M {px:.3f} {-py:.3f} L {lx:.3f} {-ly:.3f}"/>')
            etiquette(lx, ly, lettre, "R " + val,
                      dessous=t.get("dy", 0) < 0)
    for i, c in enumerate(notes):
        yn = y0 - md - tp * (1.0 + i * 1.55)
        lignes_txt.append(
            f'<circle cx="{x0 + tp*0.62:.3f}" cy="{-yn:.3f}" r="{tp*0.62:.3f}" '
            f'fill="currentColor" opacity="0.14" stroke="none"/>'
            f'<text x="{x0 + tp*0.62:.3f}" y="{-yn + tp*0.34:.3f}" '
            f'text-anchor="middle" font-size="{tp*0.78:.3f}" font-weight="700" '
            f'fill="currentColor" stroke="none">{c["lettre"]}</text>'
            f'<text x="{x0 + tp*1.55:.3f}" y="{-yn + tp*0.30:.3f}" '
            f'font-size="{tp*0.74:.3f}" fill="currentColor" opacity="0.72" '
            f'stroke="none">{c["libelle"]} {_fmt(c["valeur"])} '
            f'(hors du plan de la vue)</text>')
    o.append("</g>")
    o.append("".join(lignes_txt))
    o.append("</svg>")
    return "".join(o)


# ═══════════════════════════════════════════════════════════════════════
#  PLANCHES A4 — plusieurs pièces, plusieurs feuilles, un seul PDF
# ═══════════════════════════════════════════════════════════════════════
#
#  Ajouté le 2026-10-03 (jambe basse en carton). `ecrire_plan_a4` pose UNE
#  pièce sous un bandeau de 52 mm : une plaque de tibia de 201 mm n'y tient
#  pas. Ici le bandeau est réduit, chaque feuille porte son réglet de
#  100 mm, et la zone utile est publiée (ZONE_PLANCHE) pour que l'appelant
#  range ses pièces dedans. Les traits sont des traits de COUPE ; les croix
#  de pointage sont des segments ouverts, plus fins, et la légende le dit.

MARGE_PLANCHE = 10.0                    # mm, bord de feuille
BANDEAU_PLANCHE = 38.0                  # mm, titre + 2 lignes d'information
PIED_PLANCHE = 36.0                     # mm, réglet et sa légende
ZONE_PLANCHE = (A4_L - 2 * MARGE_PLANCHE,
                A4_H - 2 * MARGE_PLANCHE - BANDEAU_PLANCHE - PIED_PLANCHE)


def ecrire_planches_a4(feuilles, chemin, titre, lignes_info):
    """Un PDF de N pages A4. `feuilles` : liste de dict

        traits      polylignes fermées, à COUPER (mm, origine en bas à gauche
                    de la zone utile, ZONE_PLANCHE)
        croix       segments [(x1, y1), (x2, y2)] : à POINTER puis percer
        etiquettes  [(x, y, texte)]

    Lève si un point sort de la zone utile : une pièce rognée à l'impression
    serait une pièce fausse sans que rien ne le signale.
    """
    zx0, zy0 = MARGE_PLANCHE, MARGE_PLANCHE + PIED_PLANCHE
    zl, zh = ZONE_PLANCHE
    pages = []
    n = len(feuilles)
    for k, f in enumerate(feuilles, 1):
        for c in f.get("traits", []) + f.get("croix", []):
            for x, y in c:
                if not (-1e-6 <= x <= zl + 1e-6 and -1e-6 <= y <= zh + 1e-6):
                    raise ValueError(f"feuille {k} : point ({x:.1f}, {y:.1f}) hors de la zone "
                                     f"utile {zl:.0f} x {zh:.0f} mm")
        ops = ["1 J 1 j"]

        def txt(x, y, s, taille=9):
            ops.append("BT /F1 %.1f Tf %.4f %.4f Td (%s) Tj ET"
                       % (taille, x * MM, y * MM, _echap(s)))

        ops.append("0 0 0 RG 0.6 w")
        for c in f.get("traits", []):
            ops.append(f"{(c[0][0]+zx0)*MM:.4f} {(c[0][1]+zy0)*MM:.4f} m")
            for x, y in c[1:]:
                ops.append(f"{(x+zx0)*MM:.4f} {(y+zy0)*MM:.4f} l")
            ops.append("h S")
        ops.append("0.35 w")
        for (x1, y1), (x2, y2) in f.get("croix", []):
            ops.append(f"{(x1+zx0)*MM:.4f} {(y1+zy0)*MM:.4f} m {(x2+zx0)*MM:.4f} {(y2+zy0)*MM:.4f} l S")
        for x, y, s in f.get("etiquettes", []):
            txt(x + zx0, y + zy0, s, 6.5)
        # réglet de contrôle, 100 mm, comme ecrire_plan_a4
        y0 = MARGE_PLANCHE + 20
        x0 = (A4_L - 100.0) / 2
        ops.append("0.4 w")
        ops.append(f"{x0*MM:.4f} {y0*MM:.4f} m {(x0+100)*MM:.4f} {y0*MM:.4f} l S")
        for i in range(11):
            h = 4.0 if i % 5 == 0 else 2.0
            x = x0 + i * 10.0
            ops.append(f"{x*MM:.4f} {y0*MM:.4f} m {x*MM:.4f} {(y0+h)*MM:.4f} l S")
        txt(x0, y0 - 7, "REGLET DE CONTROLE — doit mesurer exactement 100,0 mm ; "
            "sinon reimprimer a 100 %", 7.5)
        txt(x0, y0 - 14, "Trait plein : couper.  Croix : pointer, puis percer au foret.", 7.5)
        txt(MARGE_PLANCHE, A4_H - MARGE_PLANCHE - 6, f"{titre} — feuille {k}/{n}", 12)
        y = A4_H - MARGE_PLANCHE - 17
        for l in lignes_info:
            txt(MARGE_PLANCHE, y, l, 7.5)
            y -= 8.5
        pages.append(zlib.compress(_latin("\n".join(ops))))

    # objets : 1 catalogue, 2 pages, 3 police, puis (page, contenu) par feuille
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [%s] /Count %d >>"
            % (b" ".join(b"%d 0 R" % (4 + 2 * i) for i in range(n)), n),
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"]
    for i, flux in enumerate(pages):
        objs.append(b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %.4f %.4f] "
                    b"/Resources << /Font << /F1 3 0 R >> >> /Contents %d 0 R >>"
                    % (A4_L * MM, A4_H * MM, 5 + 2 * i))
        objs.append(b"<< /Length %d /Filter /FlateDecode >>\nstream\n" % len(flux)
                    + flux + b"\nendstream")
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    pos = []
    for i, o in enumerate(objs, 1):
        pos.append(len(out))
        out += b"%d 0 obj\n" % i + o + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    for p in pos:
        out += b"%010d 00000 n \n" % p
    out += (b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n"
            % (len(objs) + 1, xref))
    Path(chemin).parent.mkdir(parents=True, exist_ok=True)
    Path(chemin).write_bytes(bytes(out))
    return n
