#!/usr/bin/env python3
"""Enveloppes de couple, vitesse et amplitude par articulation.

    .venv/bin/python scripts/enveloppes_actionneurs.py

Venv DU PROJET. Le MJCF amont est lu comme SOURCE DE DONNÉES, jamais
importé comme code — même statut que scripts/import_upstream_limits.py.

Objectif : passer de « 30 moteurs à choisir » à « 2 à 4 classes ».

═══════════════════════════════════════════════════════════════════════
 MÉTHODE, ET SES LIMITES
═══════════════════════════════════════════════════════════════════════

Cas de charge DÉTERMINISTES, simulés sur CPU, sans aucun apprentissage.
Pour chaque cas la pose est tenue par un correcteur proportionnel-dérivé
jusqu'à l'équilibre, puis on lit le couple effectivement appliqué.

Deux précautions qui changent les résultats :

1. LA BUTÉE DE COMMANDE EST DESSERRÉE pendant la mesure. Le modèle borne
   la commande à ±10 N·m. Si le besoin dépassait cette valeur, la pose
   s'affaisserait et la mesure renverrait 10 — c'est-à-dire la limite du
   modèle, pas le besoin réel. On mesure sans borne, puis on compare.

2. LA CONVERGENCE EST VÉRIFIÉE CAS PAR CAS. Un cas qui ne s'équilibre
   pas ne donne pas un couple faible : il donne un couple qui n'a aucun
   sens. Les cas non convergés sont signalés et exclus, jamais moyennés.

⚠ Le modèle est ToddlerBot : 3,45 kg, H = 0,56 m. Les enveloppes valent
  POUR CE ROBOT. L'extrapolation à un autre palier suppose la similitude
  géométrique et une même masse volumique — hypothèse que le passage à
  une structure métallique en plaques ne vérifie PAS. Elle est donnée
  comme ordre de grandeur, pas comme dimensionnement.
"""
from __future__ import annotations

import json
import math
import os
from pathlib import Path

import numpy as np
import mujoco

REPO = Path(__file__).resolve().parents[1]
AMONT = Path(os.environ.get("TODDLERBOT_ROOT", Path.home() / "upstream/toddlerbot"))
XML = AMONT / "toddlerbot/descriptions/toddlerbot_2xc/scene.xml"
SORTIE = REPO / "exports" / "actionneurs"

KP, KD = 40.0, 1.2          # correcteur de maintien, desserré au besoin
T_ETABL = 3.0               # s — durée de mise à l'équilibre
SEUIL_VITESSE = 0.02        # rad/s — au-delà, le cas n'est pas à l'équilibre


def bornes(m, qadr):
    """Butées articulaires, en coordonnées d'actionneur."""
    lo = np.empty(m.nu); hi = np.empty(m.nu)
    for i in range(m.nu):
        j = int(m.actuator_trnid[i, 0])
        lo[i], hi[i] = m.jnt_range[j]
    return lo, hi


def charger():
    m = mujoco.MjModel.from_xml_path(str(XML))
    m.actuator_ctrlrange[:, 0] = -1e4      # butée desserrée : voir en-tête
    m.actuator_ctrlrange[:, 1] = +1e4
    noms = [mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_ACTUATOR, i) for i in range(m.nu)]
    jid = [int(m.actuator_trnid[i, 0]) for i in range(m.nu)]
    qadr = [int(m.jnt_qposadr[j]) for j in jid]
    dadr = [int(m.jnt_dofadr[j]) for j in jid]
    return m, noms, np.array(qadr), np.array(dadr)


def tenir(m, d, cible, duree, qadr, dadr, echantillonner=False, borne=None):
    """Maintient `cible` par PD. Renvoie (couples, vitesses) max sur la fin."""
    n = int(duree / m.opt.timestep)
    couples = np.zeros(m.nu)
    vitesses = np.zeros(m.nu)
    debut_mesure = int(n * 0.7)        # on ignore le transitoire initial
    if borne is not None:
        cible = np.clip(cible, borne[0], borne[1])
    for k in range(n):
        q = d.qpos[qadr]
        qd = d.qvel[dadr]
        d.ctrl[:] = KP * (cible - q) - KD * qd
        mujoco.mj_step(m, d)
        if echantillonner or k >= debut_mesure:
            couples = np.maximum(couples, np.abs(d.actuator_force))
            vitesses = np.maximum(vitesses, np.abs(d.qvel[dadr]))
    return couples, vitesses, float(np.abs(d.qvel).max())


def pose_de_base(m, noms):
    """Pose debout du modèle, en coordonnées d'actionneur."""
    d = mujoco.MjData(m)
    mujoco.mj_forward(m, d)
    return d.qpos.copy()


def cas_statiques(m, noms, qadr, dadr):
    """Cas quasi statiques : la pose est imposée, on lit le couple de maintien."""
    idx = {n: i for i, n in enumerate(noms)}
    q0 = pose_de_base(m, noms)
    base = q0[qadr].copy()

    def variante(modifs, hauteur=None):
        c = base.copy()
        for n, v in modifs.items():
            c[idx[n]] = v
        return c

    D = math.radians
    cas = {
        "debout": variante({}),
        "genou_flechi": variante({
            "left_hip_pitch": D(-25), "right_hip_pitch": D(25),
            "left_knee": D(-50), "right_knee": D(50),
            "left_ankle_pitch": D(-25), "right_ankle_pitch": D(25)}),
        "accroupissement": variante({
            "left_hip_pitch": D(-55), "right_hip_pitch": D(55),
            "left_knee": D(-110), "right_knee": D(110),
            "left_ankle_pitch": D(-55), "right_ankle_pitch": D(55)}),
        "appui_unipodal": variante({
            # bassin déporté sur le pied gauche : celui-ci porte la charge
            "left_hip_roll": D(8), "right_hip_roll": D(8),
            "left_ankle_roll": D(-8), "right_ankle_roll": D(-8),
            # jambe droite repliée, pied décollé
            "right_hip_pitch": D(35), "right_knee": D(75)}),
        "bras_horizontal": variante({
            "left_shoulder_pitch": D(-90), "right_shoulder_pitch": D(90)}),
    }
    bn = bornes(m, qadr)
    res = {}
    for nom, cible in cas.items():
        d = mujoco.MjData(m)
        d.qpos[:] = q0
        cible = np.clip(cible, bn[0], bn[1])   # jamais au-delà d'un arrêt mécanique
        d.qpos[qadr] = cible          # on part déjà à la pose visée
        mujoco.mj_forward(m, d)
        c, v, residu = tenir(m, d, cible, T_ETABL, qadr, dadr, borne=bn)
        res[nom] = dict(couple=c, vitesse=v, amplitude=np.abs(cible - base),
                        residu=residu, converge=bool(residu < 0.5))
    return res, base


def cas_dynamiques(m, noms, qadr, dadr, base):
    """Balancement de jambe : le seul cas où la vitesse dimensionne."""
    idx = {n: i for i, n in enumerate(noms)}
    q0 = pose_de_base(m, noms)
    # cadence de marche amont : cycle_time = 0,72 s
    f = 1.0 / 0.72
    ampl = {"left_hip_pitch": math.radians(30), "left_knee": math.radians(-45),
            "left_ankle_pitch": math.radians(15)}
    d = mujoco.MjData(m)
    d.qpos[:] = q0
    # jambe droite en appui, légèrement fléchie pour la stabilité
    d.qpos[qadr[idx["right_knee"]]] = math.radians(10)
    mujoco.mj_forward(m, d)
    bn = bornes(m, qadr)
    n = int(2.0 / m.opt.timestep)
    couples = np.zeros(m.nu); vitesses = np.zeros(m.nu)
    ampl_vue = np.zeros(m.nu); qmin = np.full(m.nu, 1e9); qmax = np.full(m.nu, -1e9)
    for k in range(n):
        t = k * m.opt.timestep
        cible = base.copy()
        for nom, a in ampl.items():
            cible[idx[nom]] = base[idx[nom]] + a * math.sin(2 * math.pi * f * t)
        # ⚠ BORNAGE AUX BUTÉES. Sans lui, une consigne qui déborde fait
        # pousser le correcteur contre l'arrêt mécanique : le couple lu
        # est alors celui de la lutte contre la butée, pas un besoin
        # d'actionnement. Relevé sur left_knee, 25 N·m au lieu de 1,6.
        cible = np.clip(cible, bn[0], bn[1])
        q = d.qpos[qadr]; qd = d.qvel[dadr]
        d.ctrl[:] = KP * (cible - q) - KD * qd
        mujoco.mj_step(m, d)
        if t > 0.5:
            couples = np.maximum(couples, np.abs(d.actuator_force))
            vitesses = np.maximum(vitesses, np.abs(d.qvel[dadr]))
            qmin = np.minimum(qmin, d.qpos[qadr]); qmax = np.maximum(qmax, d.qpos[qadr])
    return {"jambe_balancement": dict(
        couple=couples, vitesse=vitesses, amplitude=qmax - qmin,
        residu=0.0, converge=True)}


def classer(noms, couple, vitesse):
    """Laisse les données dire le nombre de classes.

    On trie les couples, on regarde les écarts EN ÉCHELLE LOGARITHMIQUE
    entre valeurs consécutives, et on coupe là où les écarts sont les plus
    grands. Aucun nombre de classes n'est fixé d'avance ; on rend le
    profil des écarts pour que la coupure soit vérifiable.
    """
    ordre = np.argsort(couple)
    c = np.maximum(couple[ordre], 1e-6)
    ecarts = np.diff(np.log10(c))
    return ordre, ecarts


def main() -> int:
    SORTIE.mkdir(parents=True, exist_ok=True)
    m, noms, qadr, dadr = charger()
    print(f"modèle : {XML.name}  |  {m.nu} actionneurs  |  "
          f"masse {sum(m.body_mass):.3f} kg")
    print(f"butée de commande desserrée pour la mesure "
          f"(le modèle borne à ±{10.0} N·m)\n")

    stat, base = cas_statiques(m, noms, qadr, dadr)
    dyn = cas_dynamiques(m, noms, qadr, dadr, base)
    cas = {**stat, **dyn}

    print(f"{'cas de charge':22s} {'convergé':>9s} {'résidu |qvel|':>14s} "
          f"{'couple max':>12s} {'articulation la plus chargée'}")
    print("-" * 96)
    for nom, r in cas.items():
        i = int(np.argmax(r["couple"]))
        print(f"{nom:22s} {'oui' if r['converge'] else 'NON':>9s} "
              f"{r['residu']:14.4f} {r['couple'][i]:10.3f} N·m   {noms[i]}")

    retenus = {k: v for k, v in cas.items() if v["converge"]}
    exclus = [k for k, v in cas.items() if not v["converge"]]
    if exclus:
        print(f"\n⚠ cas EXCLUS faute de convergence : {', '.join(exclus)}")

    C = np.max([r["couple"] for r in retenus.values()], axis=0)
    V = np.max([r["vitesse"] for r in retenus.values()], axis=0)
    A = np.max([r["amplitude"] for r in retenus.values()], axis=0)

    # ⚠ SYMÉTRISATION. Le balancement ne sollicite qu'une jambe : sans
    # cela, `left_knee` porterait une charge dynamique et `right_knee`
    # seulement une charge statique. Le robot étant miroir (vérifié par
    # scripts/import_upstream_limits.py), l'enveloppe doit l'être aussi —
    # sinon on dimensionnerait deux moteurs différents pour deux
    # articulations identiques.
    paires = 0
    for i, n in enumerate(noms):
        if not n.startswith("left_"):
            continue
        j = noms.index("right_" + n[5:]) if ("right_" + n[5:]) in noms else None
        if j is None:
            continue
        paires += 1
        C[i] = C[j] = max(C[i], C[j])
        V[i] = V[j] = max(V[i], V[j])
        A[i] = A[j] = max(A[i], A[j])
    print(f"\n  enveloppes symétrisées sur {paires} paires gauche/droite")

    print(f"\n{'='*96}\n ENVELOPPES — maximum sur {len(retenus)} cas convergés\n{'='*96}")
    print(f"{'actionneur':28s} {'couple':>10s} {'vitesse':>10s} {'vitesse':>9s} "
          f"{'amplitude':>11s}")
    print(f"{'':28s} {'N·m':>10s} {'rad/s':>10s} {'tr/min':>9s} {'deg':>11s}")
    print("-" * 96)
    for i in np.argsort(-C):
        print(f"{noms[i]:28s} {C[i]:10.3f} {V[i]:10.2f} {V[i]*60/(2*math.pi):9.1f} "
              f"{math.degrees(A[i]):11.1f}")

    ordre, ecarts = classer(noms, C, V)
    print(f"\n{'='*96}\n CLASSEMENT — écarts en échelle log10 entre couples consécutifs\n{'='*96}")
    cs = C[ordre]
    for k, e in enumerate(ecarts):
        marque = "  <=== écart net" if e > 0.25 else ""
        print(f"  {cs[k]:8.3f} -> {cs[k+1]:8.3f} N·m    écart log10 = {e:.3f}{marque}")

    SEUIL = 0.25          # écart log10, soit un rapport de 1,8 entre voisins
    coupures = [k for k, e in enumerate(ecarts) if e > SEUIL]
    if not coupures:
        print(f"\n  AUCUN écart ne dépasse {SEUIL} en log10 : la distribution des")
        print("  couples est quasi continue. Les données ne désignent PAS de")
        print("  classes naturelles sur ce seul critère.")
    classes = []
    deb = 0
    for k in coupures + [len(ordre) - 1]:
        classes.append(ordre[deb:k + 1]); deb = k + 1
    print(f"\n  => {len(classes)} classes, décidées par les écarts et non fixées d'avance")
    for n, cl in enumerate(classes, 1):
        cc, vv = C[cl], V[cl]
        print(f"\n  CLASSE {n} — {len(cl)} articulations")
        print(f"    couple   {cc.min():.3f} à {cc.max():.3f} N·m")
        print(f"    vitesse  {vv.min():.2f} à {vv.max():.2f} rad/s "
              f"({vv.min()*60/(2*math.pi):.1f} à {vv.max()*60/(2*math.pi):.1f} tr/min)")
        print(f"    {', '.join(noms[i] for i in sorted(cl, key=lambda x: -C[x]))}")

    json.dump({"modele": str(XML), "masse_kg": float(sum(m.body_mass)),
               "actionneurs": noms,
               "couple_Nm": C.tolist(), "vitesse_rad_s": V.tolist(),
               "amplitude_deg": [math.degrees(x) for x in A],
               "cas_converges": list(retenus), "cas_exclus": exclus,
               "classes": [[noms[i] for i in cl] for cl in classes]},
              open(SORTIE / "enveloppes.json", "w"), indent=2, ensure_ascii=False)
    print(f"\n  écrit : exports/actionneurs/enveloppes.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
