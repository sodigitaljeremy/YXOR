#!/usr/bin/env python3
"""Rendu hors écran d'un modèle MJCF vers un PNG, sans fenêtre.

Usage : python sim/render.py <modele.xml> <sortie.png> [largeur hauteur]

Force MUJOCO_GL=egl : le contexte OpenGL est créé sans serveur
d'affichage, donc utilisable en SSH, dans un script de contrôle
automatique, ou quand la fenêtre interactive ne fonctionne pas.
C'est l'outil des « rendus de contrôle » exigés par CLAUDE.md.

Aucune dépendance d'image : le PNG est écrit avec la stdlib.
La taille maximale est bornée par offwidth/offheight dans la
section <visual><global> du modèle.
"""
import os

os.environ.setdefault("MUJOCO_GL", "egl")  # à poser AVANT l'import de mujoco

import struct
import sys
import zlib

import mujoco


def write_png(path: str, pixels: bytes, width: int, height: int) -> None:
    """Écrit un PNG RGB 8 bits (encodeur minimal, zlib de la stdlib)."""
    # Chaque ligne est préfixée par l'octet 0 = « aucun filtre ».
    raw = b"".join(
        b"\x00" + pixels[y * width * 3 : (y + 1) * width * 3]
        for y in range(height)
    )

    def chunk(tag: bytes, payload: bytes) -> bytes:
        return (
            struct.pack(">I", len(payload)) + tag + payload
            + struct.pack(">I", zlib.crc32(tag + payload))
        )

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", header))
        f.write(chunk(b"IDAT", zlib.compress(raw)))
        f.write(chunk(b"IEND", b""))


def main() -> None:
    if len(sys.argv) not in (3, 5):
        sys.exit("usage : render.py <modele.xml> <sortie.png> [largeur hauteur]")
    width, height = (
        (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) == 5 else (1280, 720)
    )
    model = mujoco.MjModel.from_xml_path(sys.argv[1])
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)  # met à jour les positions sans avancer le temps
    renderer = mujoco.Renderer(model, height=height, width=width)
    renderer.update_scene(data)
    image = renderer.render()  # numpy (hauteur, largeur, 3), RGB
    write_png(sys.argv[2], image.tobytes(), width, height)
    renderer.close()
    print(f"écrit : {sys.argv[2]} ({width}x{height})")


if __name__ == "__main__":
    main()
