#!/usr/bin/env python3
"""Correctifs nécessaires pour exécuter une politique ToddlerBot en boucle fermée.

⚠ CE MODULE S'EXÉCUTE AVEC LE VENV AMONT, PAS CELUI DU PROJET.
   Voir `decisions/0004-code-amont-dans-le-depot.md`.
   Interpréteur attendu : ~/upstream/toddlerbot/.venv/bin/python
   (Python 3.12, MuJoCo 3.3.4). `require_upstream_env()` le vérifie et
   arrête le programme sinon — ne pas contourner ce garde-fou.

═══════════════════════════════════════════════════════════════════════
 LES DEUX CORRECTIFS, ET POURQUOI ILS SONT PIÉGEUX
═══════════════════════════════════════════════════════════════════════

Le point commun des deux, et la raison d'être de ce fichier :

        AUCUN DES DEUX NE LÈVE D'ERREUR.

Pas d'exception, pas de dimension incompatible, pas d'avertissement, pas
même une ligne sur stderr. Le robot démarre, fait quelques pas crédibles,
et tombe. Tout pousse à soupçonner la physique, le modèle ou les poids —
c'est-à-dire à chercher exactement là où le problème n'est pas.

───────────────────────────────────────────────────────────────────────
 CORRECTIF 1 — `obs.time` est l'horloge murale, pas le temps simulé
───────────────────────────────────────────────────────────────────────

SYMPTÔME
    Le robot est effondré (z ≈ 0,02 m) *avant même* que la marche
    commence. La phase de mise en pose semble n'avoir jamais eu lieu.

CAUSE
    `MuJoCoSim.get_observation()` renseigne `obs.time` depuis
    `time.monotonic()` — soit, en pratique, plusieurs milliers de
    secondes (7473 s lors du diagnostic du 2026-09-20).

    Or `MJXPolicy.step()` teste :

        if obs.time < self.time_start:      # time_start = prep_duration = 7 s
            ...interpoler vers la pose de départ...

    Avec 7473 > 7, la condition est fausse dès le premier pas : la mise
    en pose est **entièrement sautée** et la politique pilote un robot
    qui n'a jamais rejoint sa pose de référence.

POURQUOI L'AMONT NE LE VOIT PAS
    `run_policy.py` compense par `obs.time -= start_time`, puis ajoute
    `time_until_next_step`, défini comme :

        max(start_time + control_dt * step_idx - step_end, 0)

    Ce terme est **clampé à zéro dès que la boucle est plus lente que le
    temps réel**. En interactif l'amont dort pour tenir la cadence, donc
    l'horloge murale suit le temps simulé et tout va bien. En rendu hors
    écran — ~0,9 s par image chez nous — on est massivement plus lent, le
    terme s'annule, et `obs.time` redevient l'horloge murale.

CORRECTIF
    `obs.time = sim.data.time`. Chaque `sim.step()` avance d'exactement
    un `control_dt`, donc le temps simulé est la grandeur juste — et il
    est déterministe, contrairement à l'horloge.

───────────────────────────────────────────────────────────────────────
 CORRECTIF 2 — la pose de référence n'est pas celle de l'entraînement
───────────────────────────────────────────────────────────────────────

SYMPTÔME
    Correctif 1 appliqué, la mise en pose tient (z = 0,309 m jusqu'à
    t = 7 s) et le robot **démarre correctement** — puis tombe après deux
    pas, vers t ≈ 9 s.

CAUSE
    La politique n'émet pas des angles absolus mais des *corrections*
    autour d'une pose de référence :

        motor_target = default_motor_pos + action_scale × action

    Si `default_motor_pos` n'est pas celle autour de laquelle la
    politique a appris, ses corrections s'ajoutent à une référence fausse
    et la démarche diverge. Rien ne le signale : les dimensions sont
    bonnes, les valeurs sont plausibles.

    `toddlerbot/policies/walk.py` contient le correctif — **en
    commentaire**, précédé de :

        # NOTE: Uncomment if using a checkpoint trained with the new
        #       crouched default_motor_pos.

    Le checkpoint `walk_rsl_20251226_114612` est de ceux-là. Sans ce
    bloc, `default_motor_pos` vient de `robot.yml` et ne correspond pas.

CORRECTIF
    `crouched_policy_class()` ci-dessous réactive ce bloc par
    sous-classe, sans modifier le dépôt amont (qui doit rester au SHA
    ancré par la fiche 0002).

MESURES (2026-09-20, 18 s de marche, vx commandé = 0,10 m/s)
    pose `robot.yml`  : tombe,  z min 0,013, +0,42 m
    pose accroupie    : debout, z min 0,281, +1,91 m → 0,106 m/s
    pose accroupie, commande nulle : debout, +0,004 m en 18 s
        → marche sur place sans dériver : la signature d'un
          asservissement réel, et non d'une trajectoire rejouée.

⚠ CHAQUE POLITIQUE A SA PROPRE POSE DE RÉFÉRENCE. Ce qui vaut pour
  `walk` ne vaut pas forcément pour `get_up`, `crawl_*` ou `climb_*` :
  les neuf autres politiques n'ont jamais été exécutées.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Pose accroupie du bloc commenté de `toddlerbot/policies/walk.py`, dans
# l'ordre de `robot.motor_ordering` (30 moteurs). Ces valeurs sont des
# angles articulaires amont, pas des cotes YXOR : la règle 1 ne s'y
# applique pas, elles ne dérivent pas de H.
CROUCHED_MOTOR_POS = [
    0.0, 0.85, 0.0, 0.0,                              # neck_yaw, neck_pitch, waist_1, waist_2
    -0.67, 0.0, 0.0, -1.02, 0.0, -0.49,               # jambe gauche
    0.67, 0.0, 0.0, 1.02, 0.0, 0.49,                  # jambe droite
    0.174533, 0.087266, 1.570796, -0.523599,
    -1.570796, -1.36, 0.0,                            # bras gauche
    -0.174533, 0.087266, -1.570796, -0.523599,
    1.570796, 1.36, 0.0,                              # bras droit
]

EXPECTED_PYTHON = (3, 12)
EXPECTED_MUJOCO = "3.3.4"
DEFAULT_ROOT = Path.home() / "upstream" / "toddlerbot"


def upstream_root() -> Path:
    """Racine du dépôt amont : $TODDLERBOT_ROOT, sinon ~/upstream/toddlerbot."""
    return Path(os.environ.get("TODDLERBOT_ROOT", DEFAULT_ROOT)).expanduser()


def require_upstream_env(chdir: bool = True) -> Path:
    """Garde-fou : refuse de continuer si l'interpréteur n'est pas le bon.

    Remplace une règle déclarative par une vérification exécutée (fiche
    0004). Sans cela, lancer ce fichier avec le venv YXOR donnerait soit
    un `ImportError`, soit — bien pire — une mesure faite avec MuJoCo
    3.13.0 au lieu de 3.3.4, sans que rien ne le signale.

    `chdir` est nécessaire : le code amont ouvre ses ressources par
    chemins relatifs (`motion/…`, `toddlerbot/descriptions/…`).
    """
    root = upstream_root()

    def die(msg: str) -> None:
        sys.exit(
            f"\n[sim/upstream] {msg}\n\n"
            f"  Ce fichier s'exécute avec le venv AMONT, pas celui du projet.\n"
            f"    correct : {root}/.venv/bin/python <script>\n"
            f"    faux    : .venv/bin/python <script>   (venv YXOR, MuJoCo 3.13.0)\n\n"
            f"  Voir decisions/0004-code-amont-dans-le-depot.md\n"
        )

    if sys.version_info[:2] != EXPECTED_PYTHON:
        die(f"Python {'.'.join(map(str, sys.version_info[:2]))} détecté, "
            f"{'.'.join(map(str, EXPECTED_PYTHON))} attendu.")
    if not root.is_dir():
        die(f"Dépôt amont introuvable : {root}\n"
            f"  Définir TODDLERBOT_ROOT si l'emplacement diffère.")
    if chdir:
        os.chdir(root)
    try:
        import mujoco
    except ImportError:
        die("MuJoCo absent de cet interpréteur.")
    if mujoco.__version__ != EXPECTED_MUJOCO:
        die(f"MuJoCo {mujoco.__version__} détecté, {EXPECTED_MUJOCO} attendu "
            f"(c'est la version sur laquelle les mesures ont été prises).")
    try:
        import toddlerbot  # noqa: F401
    except ImportError:
        die("Paquet `toddlerbot` non importable : la pile amont n'est pas installée.")
    return root


def simulated_time_obs(sim):
    """CORRECTIF 1 — observation dont `time` est le temps simulé.

    À appeler à la place de `sim.get_observation()` dans toute boucle qui
    ne tourne pas en temps réel (rendu hors écran, traitement par lots).
    """
    obs = sim.get_observation()
    obs.time = sim.data.time
    return obs


def crouched_policy_class(base_cls):
    """CORRECTIF 2 — sous-classe imposant la pose de référence accroupie.

    Réactive le bloc commenté de `walk.py` sans toucher au dépôt amont,
    qui doit rester au SHA ancré par la fiche 0002.
    """
    import numpy as np

    pose = np.array(CROUCHED_MOTOR_POS, dtype=np.float32)

    class CrouchedPolicy(base_cls):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if pose.shape[0] != self.default_motor_pos.shape[0]:
                raise ValueError(
                    f"pose accroupie de taille {pose.shape[0]}, "
                    f"{self.default_motor_pos.shape[0]} moteurs attendus"
                )
            self.default_motor_pos = pose.copy()
            self.default_action = self.default_motor_pos[self.action_mask]
            self.ref_motor_pos = self.default_motor_pos.copy()

    CrouchedPolicy.__name__ = f"Crouched{base_cls.__name__}"
    return CrouchedPolicy


if __name__ == "__main__":
    root = require_upstream_env()
    import mujoco
    print(f"[sim/upstream] environnement conforme")
    print(f"  racine amont : {root}")
    print(f"  Python {'.'.join(map(str, sys.version_info[:3]))} | MuJoCo {mujoco.__version__}")
