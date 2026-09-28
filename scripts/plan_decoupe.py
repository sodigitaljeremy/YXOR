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
