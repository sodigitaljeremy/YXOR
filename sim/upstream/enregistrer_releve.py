"""Enregistre le RELEVÉ de ToddlerBot (politique get_up) : couples et vitesses d'actionneur, sans rendu.

⚠ S'EXÉCUTE AVEC LE VENV AMONT (Python 3.12 / MuJoCo 3.3.4), pas celui du
  projet — il importe `toddlerbot` (fiche 0056). Le garde-fou
  `toddlerbot_fixes.require_upstream_env()` arrête le programme sinon.

    ~/upstream/toddlerbot/.venv/bin/python sim/upstream/enregistrer_releve.py

Créé le 2026-10-06 (phase 3b de la fiche 0069). Même initialisation que
`run_policy.py --init_from_ref` de l'amont : le robot est posé dans la
PREMIÈRE IMAGE de la référence de mouvement `get_up` (au sol), tenu 1 s, puis
la politique joue l'épisode entier. Correctif 1 seulement (temps simulé) ; le
correctif 2 (pose accroupie) est propre à la marche.

Un relevé par pas de contrôle (50 Hz). Sortie dans `exports/` (ignoré).
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from toddlerbot_fixes import require_upstream_env, simulated_time_obs  # noqa: E402

REPO = Path(__file__).resolve().parents[2]


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--robot", default="toddlerbot_2xc")
    p.add_argument("--ckpt", default="toddlerbot_2xc_get_up_rsl_20260214_145222")
    p.add_argument("--sortie", default="exports/simulations/toddlerbot_releve.csv")
    a = p.parse_args(argv)
    sortie = (REPO / a.sortie).resolve()
    require_upstream_env()

    import mujoco
    from toddlerbot.policies.get_up import GetUpPolicy
    from toddlerbot.reference.get_up_ref import GetUpReference
    from toddlerbot.sim.mujoco_sim import MuJoCoSim
    from toddlerbot.sim.robot import Robot

    robot = Robot(a.robot)
    sim = MuJoCoSim(robot, vis_type="")
    policy = GetUpPolicy(name="get_up", robot=robot, init_motor_pos=sim.get_observation().motor_pos, path=a.ckpt)

    # pose initiale : première image de la référence (comme --init_from_ref de l'amont)
    mr = getattr(policy, "motion_ref", None) or GetUpReference(robot, policy.control_dt)   # pas gardée par la politique
    q0 = mr.motion_ref["qpos"][0]
    act0 = (mr.motion_ref["action"][0] if mr.motion_ref.get("action") is not None
            else q0[mr.q_start_idx + mr.mj_motor_indices])
    sim.set_qpos(q0)
    sim.data.qvel[:] = 0.0
    sim.set_motor_target(act0)
    policy.init_motor_pos = act0.copy()
    if hasattr(policy, "ref_motor_pos"):
        policy.ref_motor_pos = act0.copy()
    policy.prep_duration = 0.0
    if hasattr(policy, "is_prepared"):
        policy.is_prepared = True
    policy.time_start = 0.0
    for _ in range(10):
        mujoco.mj_forward(sim.model, sim.data)
    for _ in range(int(1.0 / policy.control_dt)):
        sim.data.qvel[:] = 0.0
        sim.set_motor_target(act0)
        sim.step()

    noms = [mujoco.mj_id2name(sim.model, mujoco.mjtObj.mjOBJ_ACTUATOR, i) for i in range(sim.model.nu)]
    z0 = float(sim.data.qpos[2])
    lignes, zs = [], []
    t0 = sim.data.time
    n = int(policy.num_frames) + int(2.0 / policy.control_dt)     # l'épisode, puis 2 s debout
    for _ in range(n):
        obs = simulated_time_obs(sim)
        _, cible = policy.step(obs, sim)
        sim.set_motor_target(cible)
        sim.step()
        lignes.append([sim.data.time - t0, float(sim.data.qpos[2]), *sim.data.actuator_force.tolist(),
                       *sim.data.actuator_velocity.tolist()])
        zs.append(float(sim.data.qpos[2]))
    sortie.parent.mkdir(parents=True, exist_ok=True)
    with sortie.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["temps_s", "z_torse_m"] + [f"tau:{x}" for x in noms] + [f"vit:{x}" for x in noms])
        w.writerows(lignes)
    print(f"{len(lignes)} pas de contrôle ({lignes[-1][0]:.2f} s), {len(noms)} actionneurs")
    print(f"z torse : départ {z0:.3f} m, fin {zs[-1]:.3f} m, max {max(zs):.3f} m")
    print(f"-> {sortie}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
