#!/usr/bin/env python3
"""Aperçu PNG d'un schéma SVG engendré, pour le regarder sans navigateur.

Motif : la machine n'a pas de carte graphique, pas de navigateur, et aucun
rasteriseur SVG installé. Or CLAUDE.md interdit de présenter une pièce comme
correcte sans l'avoir REGARDÉE. Ce script ne prétend pas être un moteur SVG :
il ne lit que les primitives que `plan_decoupe.svg_schema` écrit — des `path`
en M/L, des `circle`, des `text`. C'est assez pour voir un repère de cote qui
sort du cadre, deux étiquettes qui se chevauchent, ou une cote absente.

    .venv/bin/python scripts/apercu_svg.py <fichier.html|.svg> <sortie.png>
"""
from __future__ import annotations
import re, sys, pathlib
from PIL import Image, ImageDraw

def rasteriser(svg: str, largeur: int = 1100) -> Image.Image:
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    x0, y0, w, h = vb
    k = largeur / w
    img = Image.new("RGB", (largeur, max(1, round(h * k))), "#12151b")
    d = ImageDraw.Draw(img)
    X = lambda x: (x - x0) * k
    Y = lambda y: (y - y0) * k

    for m in re.finditer(r'<path[^>]*\bd="([^"]+)"', svg):
        pts, cur = [], None
        for tok in re.finditer(r'([MLZ])|(-?\d+(?:\.\d+)?)', m.group(1)):
            if tok.group(1):
                cur = tok.group(1)
                if cur == "Z" and len(pts) > 1:
                    d.line([pts[-1], pts[0]], fill="#e6edf3", width=2)
            else:
                pts.append(float(tok.group(2)))
        xy = [(X(pts[i]), Y(pts[i + 1])) for i in range(0, len(pts) - 1, 2)]
        if len(xy) > 1:
            d.line(xy, fill="#e6edf3", width=2)

    for m in re.finditer(r'<circle cx="([-\d.]+)" cy="([-\d.]+)" r="([\d.]+)"', svg):
        cx, cy, r = (float(g) for g in m.groups())
        d.ellipse([X(cx) - r * k, Y(cy) - r * k, X(cx) + r * k, Y(cy) + r * k],
                  outline="#58a6ff", width=2)

    for m in re.finditer(r'<text ([^>]*)>(.*?)</text>', svg):
        at = dict(re.findall(r'(\w[\w-]*)="([^"]+)"', m.group(1)))
        tx, ty = X(float(at["x"])), Y(float(at["y"]))
        txt = re.sub(r"&[a-z]+;", "?", m.group(2))
        if at.get("text-anchor") == "middle":
            tx -= d.textlength(txt) / 2
        d.text((tx, ty - 7), txt, fill="#58a6ff")
    return img

if __name__ == "__main__":
    src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    t = src.read_text(encoding="utf-8")
    svgs = re.findall(r"<svg.*?</svg>", t, re.S)
    if not svgs:
        sys.exit(f"aucun <svg> dans {src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    rasteriser(svgs[0]).save(dst)
    print(f"{dst} — {len(svgs)} schéma(s) trouvé(s), le premier rastérisé")
