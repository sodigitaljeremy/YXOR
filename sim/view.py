#!/usr/bin/env python3
"""Ouvre le viewer interactif MuJoCo sur un modèle MJCF.

Usage : python sim/view.py <modele.xml>

Nécessite une session graphique. Souris : clic gauche = orbite,
clic droit = translation, molette = zoom ; Espace = pause ;
double-clic puis Ctrl+clic droit = appliquer une force à un corps.

Sur cette machine le rendu OpenGL est logiciel (llvmpipe) :
suffisant pour inspecter une pièce ou une pose, lent sur une
scène chargée.
"""
import sys

import mujoco
import mujoco.viewer


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage : view.py <modele.xml>")
    model = mujoco.MjModel.from_xml_path(sys.argv[1])
    data = mujoco.MjData(model)
    # Boucle bloquante : simulation active + interface, jusqu'à
    # fermeture de la fenêtre.
    mujoco.viewer.launch(model, data)


if __name__ == "__main__":
    main()
