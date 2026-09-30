"""Enregistre une marche ToddlerBot : couples ET vitesses d'actionneur, sans rendu.

⚠ S'EXÉCUTE AVEC LE VENV AMONT (Python 3.12 / MuJoCo 3.3.4), pas celui du
  projet — il importe `toddlerbot`. Voir
  `decisions/0004-code-amont-dans-le-depot.md`. Le garde-fou de
  `toddlerbot_fixes.require_upstream_env()` arrête le programme sinon.

    ~/upstream/toddlerbot/.venv/bin/python sim/upstream/enregistrer_marche.py
    ~/upstream/toddlerbot/.venv/bin/python sim/upstream/enregistrer_marche.py \\
        --vx 0.10 --secondes 15 --sortie exports/actionneurs/marche_15s.csv

Même boucle que `replay_policy.py` — mêmes deux correctifs, même politique,
même commande — sans la vidéo. `replay_policy.py` ne journalise que les
couples ; les exigences d'actionnement demandent aussi les VITESSES, d'où
ce script. La série sort dans `exports/` (ignoré) : elle se régénère.

Échantillonnage : un relevé par pas de CONTRÔLE (50 Hz), après la mise en
pose. Une pointe plus brève que 20 ms entre deux relevés n'est pas vue.

Analyse : `scripts/analyser_marche.py`, avec le venv DU PROJET.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from toddlerbot_fixes import (  # noqa: E402
    crouched_policy_class,
    require_upstream_env,
    simulated_time_obs,
)

REPO = Path(__file__).resolve().parents[2]


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--robot", default="toddlerbot_2xc")
    p.add_argument("--policy", default="walk")
    p.add_argument("--ckpt", default="toddlerbot_2xc_walk_rsl_20251226_114612")
    p.add_argument("--vx", type=float, default=0.10)
    p.add_argument("--secondes", type=float, default=15.0)
    p.add_argument("--sortie", default="exports/actionneurs/marche_15s.csv",
                   help="relatif à la racine du dépôt YXOR")
    return p.parse_args(argv)


def main(argv=None) -> int:
    a = parse_args(argv)
    sortie = (REPO / a.sortie).resolve()
    require_upstream_env()          # garde-fou + cd vers la racine amont

    import numpy as np
    import mujoco
    from toddlerbot.sim.robot import Robot
    from toddlerbot.sim.mujoco_sim import MuJoCoSim

    mod = __import__(f"toddlerbot.policies.{a.policy}", fromlist=["*"])
    base = next(v for k, v in vars(mod).items()
                if k.endswith("Policy") and isinstance(v, type) and v.__module__ == mod.__name__)
    cls = crouched_policy_class(base)
    robot = Robot(a.robot)
    sim = MuJoCoSim(robot, vis_type="")
    cmd = np.zeros(8, dtype=np.float32)
    cmd[5] = a.vx
    policy = cls(name=a.policy, robot=robot,
                 init_motor_pos=sim.get_observation().motor_pos,
                 path=a.ckpt, fixed_command=cmd)

    total = int((policy.prep_duration + a.secondes) / sim.control_dt)
    noms = [mujoco.mj_id2name(sim.model, mujoco.mjtObj.mjOBJ_ACTUATOR, i)
            for i in range(sim.model.nu)]
    lignes, base_pos = [], []
    for _ in range(total):
        obs = simulated_time_obs(sim)                 # CORRECTIF 1
        _, cible = policy.step(obs, sim)
        sim.set_motor_target(cible)
        sim.step()
        if sim.data.time < policy.prep_duration:
            continue
        lignes.append([sim.data.time, *sim.data.actuator_force.tolist(),
                       *sim.data.actuator_velocity.tolist()])
        base_pos.append(sim.data.qpos[:3].copy())

    sortie.parent.mkdir(parents=True, exist_ok=True)
    with sortie.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["temps_s"] + [f"tau:{n}" for n in noms] + [f"vit:{n}" for n in noms])
        w.writerows(lignes)

    P = np.array(base_pos)
    duree = lignes[-1][0] - lignes[0][0]
    zmin = float(P[:, 2].min())
    print(f"{len(lignes)} pas de contrôle, {len(noms)} actionneurs, dt {sim.control_dt} s")
    print(f"avance {P[-1, 0] - P[0, 0]:+.3f} m en {duree:.2f} s "
          f"=> {(P[-1, 0] - P[0, 0]) / duree:+.4f} m/s (commandé {a.vx})")
    print(f"z torse min {zmin:.3f} m -> chute : {'OUI' if zmin < 0.20 else 'non'}")
    gears = sorted(set(sim.model.actuator_gear[:, 0].tolist()))
    print(f"gear des actionneurs : {gears}")
    print(f"-> {sortie}")
    return 1 if zmin < 0.20 else 0


if __name__ == "__main__":
    sys.exit(main())
