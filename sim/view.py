#!/usr/bin/env python3
"""Ouvre le viewer interactif MuJoCo sur un modèle MJCF.

Usage : python sim/view.py <modele.xml>

Nécessite une session graphique. Souris : clic gauche = orbite,
clic droit = translation, molette = zoom ; Espace = pause ;
double-clic puis Ctrl+clic droit = appliquer une force à un corps.

Sur cette machine le rendu OpenGL est logiciel (llvmpipe, aucun GPU
exposé à WSL2) : suffisant pour inspecter une pièce ou une pose, lent
sur une scène chargée.

Les ombres coûtent ici l'essentiel du temps d'image : elles sont
calculées dans une carte d'ombre 4096x4096 par source lumineuse,
indépendamment de la taille de la fenêtre. Mesure du 2026-09-20 sur
humanoid.xml en 1280x720 : 10,7 FPS ombres comprises, 57 FPS sans.
Si le viewer rame, décocher « Shadow » (section Rendering) dans les
panneaux latéraux — Tab et Shift-Tab les affichent.
"""
import sys

import mujoco
import mujoco.viewer


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage : view.py <modele.xml>")
    try:
        model = mujoco.MjModel.from_xml_path(sys.argv[1])
    except ValueError as err:
        sys.exit(f"modèle illisible : {err}")
    data = mujoco.MjData(model)
    # Boucle bloquante : simulation active + interface, jusqu'à
    # fermeture de la fenêtre.
    mujoco.viewer.launch(model, data)


if __name__ == "__main__":
    main()
