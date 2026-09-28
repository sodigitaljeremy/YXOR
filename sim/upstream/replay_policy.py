#!/usr/bin/env python3
"""Rejoue une politique ToddlerBot en boucle fermée et écrit une vidéo.

⚠ S'EXÉCUTE AVEC LE VENV AMONT (Python 3.12 / MuJoCo 3.3.4), pas celui du
  projet. Voir `decisions/0004-code-amont-dans-le-depot.md`. Le garde-fou
  de `toddlerbot_fixes.require_upstream_env()` arrête le programme sinon.

Usage :
    ~/upstream/toddlerbot/.venv/bin/python sim/upstream/replay_policy.py \
        --ckpt toddlerbot_2xc_walk_rsl_20251226_114612 \
        --vx 0.10 --seconds 6 --out exports/video/walk.mp4

Applique les deux correctifs documentés dans `toddlerbot_fixes.py` :
sans eux le robot tombe, **sans qu'aucune erreur ne soit levée**.

Réglages de rendu : le rendu est logiciel (llvmpipe, aucun GPU sous WSL2).
Mesures du 2026-09-20 sur cette scène, en 960×540 :
    ombres 4096 + MSAA 4 (défaut du modèle) : 2980 ms/image
    ombres  512 + MSAA 0                    :  962 ms/image
    sans ombres + MSAA 0                    :  358 ms/image
C'est l'anticrénelage qui domine ici (~1,5 s), devant les ombres (~0,6 s).
D'où les défauts ci-dessous : ombres réduites plutôt que supprimées —
l'ombre portée est ce qui permet de juger le contact au sol.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from toddlerbot_fixes import (  # noqa: E402
    crouched_policy_class,
    require_upstream_env,
    simulated_time_obs,
)

REPO = Path(__file__).resolve().parents[2]   # racine du dépôt YXOR


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ckpt", default="toddlerbot_2xc_walk_rsl_20251226_114612",
                   help="nom du dossier sous <amont>/ckpts/")
    p.add_argument("--policy", default="walk", help="module de politique amont")
    p.add_argument("--robot", default="toddlerbot_2xc")
    p.add_argument("--vx", type=float, default=0.10, help="vitesse avant commandée (m/s)")
    p.add_argument("--vy", type=float, default=0.0)
    p.add_argument("--wz", type=float, default=0.0, help="vitesse de lacet (rad/s)")
    p.add_argument("--seconds", type=float, default=6.0, help="durée filmée après mise en pose")
    p.add_argument("--out", default="exports/video/replay.mp4",
                   help="chemin de sortie, relatif à la racine du dépôt YXOR")
    p.add_argument("--width", type=int, default=640)
    p.add_argument("--height", type=int, default=480)
    p.add_argument("--fps", type=int, default=20)
    p.add_argument("--shadowsize", type=int, default=1024,
                   help="0 pour couper les ombres (le plus rapide)")
    p.add_argument("--no-crouched", action="store_true",
                   help="désactiver le correctif 2 (le robot tombera, sans erreur)")
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    require_upstream_env()          # garde-fou + cd vers la racine amont

    import numpy as np
    import mujoco
    import imageio.v2 as imageio
    from toddlerbot.sim.robot import Robot
    from toddlerbot.sim.mujoco_sim import MuJoCoSim

    mod = __import__(f"toddlerbot.policies.{args.policy}", fromlist=["*"])
    base = next(v for k, v in vars(mod).items()
                if k.endswith("Policy") and isinstance(v, type) and v.__module__ == mod.__name__)
    cls = base if args.no_crouched else crouched_policy_class(base)
    print(f"politique : {cls.__name__}  (correctif 2 {'DÉSACTIVÉ' if args.no_crouched else 'actif'})")

    robot = Robot(args.robot)
    sim = MuJoCoSim(robot, vis_type="")
    cmd = np.zeros(8, dtype=np.float32)
    cmd[5], cmd[6], cmd[7] = args.vx, args.vy, args.wz
    policy = cls(name=args.policy, robot=robot,
                 init_motor_pos=sim.get_observation().motor_pos,
                 path=args.ckpt, fixed_command=cmd)

    # Réglages purement visuels : aucun effet sur la physique.
    sim.model.vis.quality.offsamples = 0
    sim.model.vis.quality.shadowsize = max(args.shadowsize, 1)
    r = mujoco.Renderer(sim.model, height=args.height, width=args.width)
    r.scene.flags[mujoco.mjtRndFlag.mjRND_SHADOW] = 1 if args.shadowsize else 0

    def camera(lookat):
        c = mujoco.MjvCamera()
        mujoco.mjv_defaultFreeCamera(sim.model, c)
        c.lookat[:] = lookat
        c.distance, c.elevation, c.azimuth = 1.3, -12, 140
        return c

    every = max(1, round((1.0 / args.fps) / sim.control_dt))
    total = int((policy.prep_duration + args.seconds) / sim.control_dt)
    print(f"{total} pas de contrôle ({policy.prep_duration:.0f} s de mise en pose "
          f"+ {args.seconds:.0f} s filmées), une image tous les {every} pas")

    frames, rtimes, log = [], [], []
    t_phys = 0.0
    for step in range(total):
        obs = simulated_time_obs(sim)          # CORRECTIF 1
        _, motor_target = policy.step(obs, sim)
        sim.set_motor_target(motor_target)
        t0 = time.perf_counter()
        sim.step()
        t_phys += time.perf_counter() - t0

        if sim.data.time < policy.prep_duration:
            continue
        log.append((sim.data.time, *(float(v) for v in sim.data.qpos[:3])))
        if step % every:
            continue
        base_pos = sim.data.qpos[:3]
        r.update_scene(sim.data, camera=camera([base_pos[0], base_pos[1], 0.18]))
        t0 = time.perf_counter()
        frames.append(r.render())
        rtimes.append(time.perf_counter() - t0)
    r.close()

    L = np.array(log)
    dx, dy = L[-1, 1] - L[0, 1], L[-1, 2] - L[0, 2]
    dur = L[-1, 0] - L[0, 0]
    zmin = L[:, 3].min()
    fell = zmin < 0.20
    print("\n--- résultat ---")
    print(f"avance x        : {dx:+.3f} m en {dur:.1f} s => {dx/dur:+.4f} m/s "
          f"(commandé {args.vx:.2f})")
    print(f"dérive y        : {dy:+.3f} m")
    print(f"z torse         : début {L[0,3]:.3f} | min {zmin:.3f} | fin {L[-1,3]:.3f}")
    print(f"chute           : {'OUI' if fell else 'non — debout du début à la fin'}")
    print(f"physique        : {t_phys:.1f} s pour {total*sim.control_dt:.0f} s simulées "
          f"=> x{total*sim.control_dt/t_phys:.2f} temps réel")

    out = REPO / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    imageio.mimwrite(out, frames, fps=args.fps, codec="libx264",
                     quality=7, macro_block_size=1)
    rt = np.array(rtimes)
    print(f"rendu           : médian {np.median(rt)*1000:.0f} ms/image, total {rt.sum():.0f} s")
    print(f"-> {out}  ({len(frames)} images, {len(frames)/args.fps:.1f} s, "
          f"{out.stat().st_size/1e6:.1f} Mo)")
    return 1 if fell else 0


if __name__ == "__main__":
    sys.exit(main())
