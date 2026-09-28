#!/usr/bin/env python3
"""Extrait axes et butées des 30 articulations depuis le modèle amont épinglé.

Usage :
    .venv/bin/python scripts/import_upstream_limits.py
    .venv/bin/python scripts/import_upstream_limits.py --check   # ne réécrit pas

Se lance avec le venv DU PROJET (`.venv/bin/python`). Le dépôt amont est
lu comme une SOURCE DE DONNÉES — le MJCF est un fichier, pas du code
importé — donc ce script n'entre pas dans le carve-out `sim/upstream/`
de la fiche 0004. Vérifié le 2026-09-28 : MuJoCo 3.13.0 et 3.3.4 rendent
des axes et des butées identiques sur ce modèle.

Voir `decisions/0006-fichier-genere-commite.md` : le fichier produit est
commité, par exception au principe de la règle 4, parce qu'il dérive
d'un dépôt externe et ne serait pas régénérable si celui-ci disparaissait.

═══════════════════════════════════════════════════════════════════════
 POURQUOI LE VECTEUR D'AXE, ET NON L'ÉTIQUETTE
═══════════════════════════════════════════════════════════════════════

Les noms amont et ceux de `params/joints.yaml` se contredisent : l'amont
appelle `elbow_roll` une articulation que `joints.yaml` déclare sur
l'axe y — or dans la convention usuelle (x avant, y gauche, z haut),
« roll » désigne une rotation autour de x, pas de y.

Une étiquette est une intention ; seul le vecteur dit ce que fait
réellement l'articulation. Ce script n'extrait donc aucun nom d'axe : il
extrait des **composantes numériques**, et laisse la lecture
anatomique à qui sait dans quel repère il se place.

Deux repères sont produits pour chaque articulation, parce qu'ils
répondent à deux questions différentes :

  axe_corps  — l'axe tel qu'écrit dans le MJCF, exprimé dans le repère
               du corps porteur. C'est la donnée brute, non interprétée.

  axe_monde  — le même axe exprimé dans le repère du monde, à la pose
               par défaut du modèle. C'est LUI qui répond à « autour de
               quel axe physique cela tourne-t-il », parce que le corps
               porteur est lui-même orienté dans l'espace : un axe
               « y » écrit dans un corps tourné de 90° ne pointe pas
               dans la direction y du robot.

Aucune valeur n'est recopiée, aucune n'est inventée.
"""
from __future__ import annotations

import argparse
import datetime
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = Path.home() / "upstream" / "toddlerbot"
PINNED_SHA = "e337f3b177b4b53abff70b31d1695a7b66cc6d2e"   # fiche 0002
ROBOT = "toddlerbot_2xc"
OUT = REPO / "params" / "upstream_joints.generated.yaml"

# Groupes YXOR, déduits du nom amont. Sert uniquement à ordonner la
# sortie de façon lisible ; n'altère aucune valeur extraite.
GROUPS = [
    ("jambes", ("hip", "knee", "ankle")),
    ("bras", ("shoulder", "elbow", "wrist")),
    ("taille", ("waist",)),
    ("nuque", ("neck",)),
]


def upstream_root() -> Path:
    import os
    return Path(os.environ.get("TODDLERBOT_ROOT", DEFAULT_ROOT)).expanduser()


def head_sha(root: Path) -> str:
    out = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                         capture_output=True, text=True, check=True)
    return out.stdout.strip()


def group_of(name: str) -> str:
    for g, keys in GROUPS:
        if any(k in name for k in keys):
            return g
    return "autre"


def fmt_vec(v: np.ndarray) -> str:
    """Vecteur en liste YAML, zéros négatifs normalisés."""
    return "[" + ", ".join(f"{0.0 if abs(c) < 1e-12 else c:+.6f}" for c in v) + "]"


def _stem(name: str) -> str | None:
    """Racine d'un nom d'actionneur de transmission, sinon None.

    `neck_yaw_drive` -> `neck_yaw` ; `neck_pitch_act` -> `neck_pitch` ;
    `waist_act_1` -> `waist`. Un nom sans ces suffixes désigne un
    actionnement direct : le moteur EST l'articulation.
    """
    m = re.match(r"^(.*?)_(?:drive|act)(?:_\d+)?$", name)
    return m.group(1) if m else None


def extract(root: Path):
    import mujoco
    xml = root / "toddlerbot" / "descriptions" / ROBOT / "scene.xml"
    m = mujoco.MjModel.from_xml_path(str(xml))
    d = mujoco.MjData(m)
    mujoco.mj_forward(m, d)          # pose par défaut, pour les axes en repère monde

    def info(j: int) -> dict:
        b = int(m.jnt_bodyid[j])
        axis_body = np.asarray(m.jnt_axis[j], dtype=float)
        axis_world = np.asarray(d.xmat[b], dtype=float).reshape(3, 3) @ axis_body
        limited = bool(m.jnt_limited[j])
        lo, hi = (np.degrees(m.jnt_range[j]) if limited else (None, None))
        return dict(
            nom=mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_JOINT, j),
            corps=mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_BODY, b),
            axe_corps=axis_body, axe_monde=axis_world,
            limited=limited, min_deg=lo, max_deg=hi,
        )

    # --- les 30 actionneurs ---
    actuators, act_jids, stems = [], set(), {}
    for a in range(m.nu):
        act = mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_ACTUATOR, a)
        if int(m.actuator_trntype[a]) != int(mujoco.mjtTrn.mjTRN_JOINT):
            raise RuntimeError(f"{act}: transmission non gérée "
                               f"(trntype={int(m.actuator_trntype[a])})")
        j = int(m.actuator_trnid[a, 0])
        if int(m.jnt_type[j]) != int(mujoco.mjtJoint.mjJNT_HINGE):
            raise RuntimeError(f"{act}: joint non rotoïde")
        act_jids.add(j)
        st = _stem(act)
        r = info(j)
        r.update(actionneur=act, groupe=group_of(act),
                 transmission="parallele" if st else "direct")
        actuators.append(r)
        if st:
            stems.setdefault(st, []).append(act)

    # --- les articulations : direct = le moteur lui-même ; parallèle = la
    #     sortie passive de la liaison. Le rattachement est DÉRIVÉ des noms,
    #     jamais codé en dur.
    joints = [dict(r, role="articulation", actionne_par=[r["actionneur"]])
              for r in actuators if r["transmission"] == "direct"]

    for j in range(m.njnt):
        if int(m.jnt_type[j]) != int(mujoco.mjtJoint.mjJNT_HINGE) or j in act_jids:
            continue
        r = info(j)
        n = r["nom"]
        role, by = "bielle", []
        for st, acts in stems.items():
            if len(acts) == 1:
                # une transmission, une sortie : nom exact ou suffixe _driven
                if n == st or n == f"{st}_driven":
                    role, by = "articulation", list(acts)
            else:
                # plusieurs moteurs pour un même ensemble (taille) : préfixe
                if n.startswith(f"{st}_"):
                    role, by = "articulation", list(acts)
        r.update(role=role, actionne_par=by, groupe=group_of(n),
                 transmission="parallele")
        joints.append(r)

    arts = [r for r in joints if r["role"] == "articulation"]
    bielles = [r for r in joints if r["role"] == "bielle"]
    return m, actuators, arts, bielles



def check_mirror(arts) -> list[str]:
    """Vérifie que gauche et droite sont bien images l'une de l'autre.

    Sans cette garantie, `params/joints.yaml` ne pourrait pas porter un
    seul jeu de butées par articulation : il faudrait les deux côtés.

    Sous une réflexion sagittale (plan xz), un vecteur AXIAL — un axe de
    rotation — se transforme en (-wx, +wy, -wz), et non comme un vecteur
    ordinaire. Comparer les butées sans tenir compte de ce signe fait
    conclure à tort à une asymétrie.
    """
    def mirror(a): return np.array([-a[0], a[1], -a[2]])
    idx = {r["nom"]: r for r in arts}
    anomalies = []
    for n, l in idx.items():
        if not n.startswith("left_"):
            continue
        r = idx.get("right_" + n[5:])
        if r is None:
            anomalies.append(f"{n} : pas de contrepartie droite")
            continue
        if not (l["limited"] and r["limited"]):
            continue
        mL = mirror(np.asarray(l["axe_monde"]))
        aR = np.asarray(r["axe_monde"])
        if np.allclose(aR, mL, atol=1e-6):
            exp = (l["min_deg"], l["max_deg"])
        elif np.allclose(aR, -mL, atol=1e-6):
            exp = (-l["max_deg"], -l["min_deg"])
        else:
            anomalies.append(f"{n[5:]} : axe droit ni miroir ni opposé du gauche")
            continue
        if abs(r["min_deg"] - exp[0]) > 1e-6 or abs(r["max_deg"] - exp[1]) > 1e-6:
            anomalies.append(
                f"{n[5:]} : butées droites {r['min_deg']:+.1f}/{r['max_deg']:+.1f}, "
                f"miroir attendu {exp[0]:+.1f}/{exp[1]:+.1f}")
    return anomalies


def render(actuators, arts, bielles, sha: str, mujoco_version: str) -> str:
    now = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
    L, A = [], None
    A = L.append
    A("# ╔══════════════════════════════════════════════════════════════════╗")
    A("# ║  FICHIER GÉNÉRÉ — NE PAS ÉDITER À LA MAIN                        ║")
    A("# ╚══════════════════════════════════════════════════════════════════╝")
    A("#")
    A(f"# Commit amont : {sha}")
    A("# Épinglé par  : decisions/0002-pin-toddlerbot.md")
    A(f"# Modèle       : toddlerbot/descriptions/{ROBOT}/scene.xml")
    A(f"# Extrait le   : {now}")
    A(f"# Par          : scripts/import_upstream_limits.py (MuJoCo {mujoco_version})")
    A("#")
    A("# Commité par exception au principe de la règle 4, parce qu'il dérive")
    A("# d'un dépôt externe et ne serait pas régénérable si celui-ci")
    A("# disparaissait — voir decisions/0006-fichier-genere-commite.md.")
    A("#")
    A("# ── Deux sections, et il ne faut surtout pas les confondre ──────────")
    A("#")
    A("# actionneurs  : les 30 MOTEURS. C'est ce que la commande pilote.")
    A("# articulations: les 30 DEGRÉS DE LIBERTÉ du squelette. C'est ce que")
    A("#                params/joints.yaml décrit.")
    A("#")
    A("# Quand l'actionnement est direct, les deux coïncident. Quand il passe")
    A("# par une liaison parallèle, ils DIFFÈRENT — et les butées aussi :")
    A("# le moteur de taille tourne de ±268°, le torse ne pivote que de ±90°.")
    A("# Remplir joints.yaml depuis la section `actionneurs` donnerait donc")
    A("# des butées fausses d'un facteur 3. Utiliser `articulations`.")
    A("#")
    A("# bielles      : pièces internes des liaisons parallèles. Ni moteurs")
    A("#                ni degrés de liberté anatomiques. Listées pour")
    A("#                l'exhaustivité, à ignorer pour la nomenclature.")
    A("#")
    A("# axe_corps : axe de rotation dans le repère du CORPS porteur (donnée")
    A("#             brute du MJCF, non interprétée).")
    A("# axe_monde : le même axe dans le repère du MONDE, à la pose par")
    A("#             défaut. C'est celui-ci qui dit autour de quel axe")
    A("#             PHYSIQUE l'articulation tourne.")
    A("#             Repère : x avant, y gauche, z haut.")
    A("#             Un signe négatif inverse le sens positif, pas l'axe.")
    A("# min/max   : butées en degrés, telles qu'écrites dans le modèle.")
    A("#")
    A(f"# {len(actuators)} actionneurs, {len(arts)} articulations, {len(bielles)} bielles.")
    A("")
    A("source:")
    A("  depot: https://github.com/hshi74/toddlerbot")
    A(f"  commit: {sha}")
    A(f"  robot: {ROBOT}")
    A("")

    def block(rows, key_name, extra):
        for g, _ in GROUPS + [("autre", ())]:
            sel = [r for r in rows if r["groupe"] == g]
            if not sel:
                continue
            A(f"  # --- {g} ---")
            for r in sel:
                A(f"  - nom: {r[key_name]}")
                for k, v in extra(r):
                    A(f"    {k}: {v}")
                A(f"    corps: {r['corps']}")
                A(f"    axe_corps: {fmt_vec(r['axe_corps'])}")
                A(f"    axe_monde: {fmt_vec(r['axe_monde'])}")
                if r["limited"]:
                    A(f"    min: {r['min_deg']:+.4f}")
                    A(f"    max: {r['max_deg']:+.4f}")
                else:
                    A("    min: null   # non bornée dans le modèle")
                    A("    max: null")

    A("actionneurs:")
    block(actuators, "actionneur", lambda r: [("transmission", r["transmission"])])
    A("")
    A("articulations:")
    block(arts, "nom", lambda r: [("transmission", r["transmission"]),
                                  ("actionne_par", "[" + ", ".join(r["actionne_par"]) + "]")])
    A("")
    A("bielles:")
    block(bielles, "nom", lambda r: [])
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--check", action="store_true",
                   help="vérifie sans réécrire (sortie non nulle si le fichier diffère)")
    p.add_argument("--allow-sha-mismatch", action="store_true",
                   help="extraire même si l'amont n'est pas sur le commit épinglé")
    args = p.parse_args(argv)

    root = upstream_root()
    if not root.is_dir():
        sys.exit(f"dépôt amont introuvable : {root}\n"
                 f"  définir TODDLERBOT_ROOT si l'emplacement diffère")

    sha = head_sha(root)
    if sha != PINNED_SHA:
        msg = (f"l'amont est sur {sha}\n"
               f"  mais la fiche 0002 épingle {PINNED_SHA}\n"
               f"  Les butées extraites ne correspondraient pas au robot mesuré.")
        if not args.allow_sha_mismatch:
            sys.exit("REFUS : " + msg + "\n  (--allow-sha-mismatch pour forcer)")
        print("AVERTISSEMENT : " + msg, file=sys.stderr)

    import mujoco
    m, actuators, arts, bielles = extract(root)
    if len(actuators) != 30:
        sys.exit(f"REFUS : {len(actuators)} actionneurs extraits, 30 attendus")
    anomalies = check_mirror(arts)
    if anomalies:
        sys.exit("REFUS : symétrie gauche/droite rompue —\n  "
                 + "\n  ".join(anomalies)
                 + "\n  joints.yaml ne peut plus porter un seul jeu de butées.")
    if len(arts) != 30:
        sys.exit(f"REFUS : {len(arts)} articulations dérivées, 30 attendues "
                 f"(le rattachement moteur→articulation a échoué)")
    text = render(actuators, arts, bielles, sha, mujoco.__version__)

    if args.check:
        if not OUT.exists():
            print(f"{OUT.relative_to(REPO)} : absent")
            return 1
        # on ignore la ligne de date, qui change à chaque exécution
        def strip_date(s): return "\n".join(l for l in s.splitlines()
                                            if not l.startswith("# Extrait le"))
        same = strip_date(OUT.read_text(encoding="utf-8")) == strip_date(text)
        print(f"{OUT.relative_to(REPO)} : {'à jour' if same else 'DIFFÈRE du modèle amont'}")
        return 0 if same else 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"écrit : {OUT.relative_to(REPO)}")
    print(f"  commit amont : {sha}")
    print(f"  {len(actuators)} actionneurs, {len(arts)} articulations, "
          f"{len(bielles)} bielles")
    print(f"  dont {sum(1 for r in arts if r['transmission'] == 'parallele')} "
          f"articulations à liaison parallèle")
    print("  symétrie gauche/droite : vérifiée")
    return 0


if __name__ == "__main__":
    sys.exit(main())
