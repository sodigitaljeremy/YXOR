#!/usr/bin/env python3
"""Squelette de YXOR S (v3, 26 DDL depuis la fiche 0068) : un MJCF minimal engendré depuis params/.

    .venv/bin/python scripts/squelette.py            # MJCF + tableau
    .venv/bin/python scripts/squelette.py --rendu    # + image de contrôle (EGL, hors écran)

Créé le 2026-10-03. Lit :
  params/squelette.yaml       articulations, segments, positions (ratios)
  params/anthropometry.yaml   H_S (tailles.S.H_m), ratios ANSUR, fractions de masse
  params/joints.yaml          axes (noms identiques, règle 3)
  params/configuration_S.yaml actionneur des jambes (fiche 0067), hypothèse v3
  params/actionneurs.yaml     masse et encombrement des actionneurs (cotes_montage)
et la masse du modèle de S (choix_actionneurs.evaluer_configuration, v3).

Écrit exports/squelette/yxor_s_v3.xml (règle 4 : engendré, jamais suivi).

Les corps sont des boîtes et des capsules dimensionnées par les ratios ANSUR,
plus un cylindre par actionneur à ses cotes publiées. AUCUNE géométrie
ToddlerBot. Répartition des masses (HYPOTHÈSE, dite) : chaque actionneur à
son articulation ; la charge utile dans le tronc ; le supplément de
structure RS02 avec l'actionneur RS02 ; le reste (structure, mise à
l'échelle) réparti par les fractions de Winter. Le total égale, par
construction, la masse du modèle de S.

Ce n'est pas une CAO : c'est un squelette de vérification (cinématique,
masses, chargement dans MuJoCo).
"""
from __future__ import annotations

import argparse
import math
import os
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import choix_actionneurs as C  # noqa: E402
import dimensionnement as D  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
P = REPO / "params"
SORTIE = REPO / "exports" / "squelette"
COTES = {"left": 1.0, "right": -1.0}


def lire(nom: str) -> dict:
    return yaml.safe_load((P / nom).read_text(encoding="utf-8"))


def longueur(expr: dict, ratios: dict, H: float, ecarts: dict | None = None) -> float:
    """Σ ratio × coefficient × H, en mètres ; un terme `ecart.<nom>` vaut l'écart calculé (m)."""
    total = 0.0
    for k, c in (expr or {}).items():
        if k.startswith("ecart."):
            total += (ecarts or ecarts_cheville())[k.split(".", 1)[1]] * c
        else:
            total += ratios[k]["valeur"] * c * H
    return total


def ecarts_cheville() -> dict:
    """Les écarts ANSUR de la cheville et du pied (params/squelette.yaml, ecarts_ansur), en mètres.

    MODIFIÉ le 2026-10-04 (fiche 0068, cheville sans roulis). Le tibia tient le
    stator du RS00 du tangage ; la chape du pied (sortie) l'enjambe :
      r_plaque_tibia = max(R0 ; motif_stator + demi-passage + voile ;
                           entretoise de sortie + jeu + voile)
      hauteur_axe_cheville = e_max + jeu + r_plaque_tibia
      largeur_pied = 2 × (face extérieure du montant + rayon rentrant + voile)
    à l'épaisseur la plus forte des réglages listés.
    """
    import procedes as PROC
    ea = lire("squelette.yaml")["ecarts_ansur"]
    ec = ea["cheville"]
    cm = D.charger_catalogue()["candidats"][ec["actionneur"]]["cotes_montage"]
    hw = PROC.charger()
    regs = [PROC.reglage(r, hw) for r in ec["reglages"]]
    e_max = max(r["epaisseur"] for r in regs)
    r_rent = max(PROC.rayon_interieur_min(r["epaisseur"], r.get("rayon_interieur_min_machine")) for r in regs)
    voiles = [r["voile_min"] for r in regs if r.get("voile_min") is not None]
    if not voiles:
        raise ValueError("aucun voile minimal déclaré pour les réglages de la cheville")
    v, jeu = max(voiles), ec["jeu_mm"]["valeur"]
    pas = lambda m: cm[m]["diametre_percage"] / 2 + hw["vis"][cm[m]["vis"]]["passage"] / 2 + v
    r_sortie = pas("sortie")                                     # entretoise et montant sur la sortie
    R0, L0 = cm["diametre_corps"] / 2, D.val(cm["longueur"])
    r_plaque = max(R0, pas(ec["motif_stator"]), r_sortie + jeu + v)
    y_montant = L0 / 2 + 2 * jeu + 2 * e_max                     # face extérieure du montant extérieur
    largeur = 2 * (y_montant + r_rent + v)
    return dict(hauteur_axe_cheville=(e_max + jeu + r_plaque) / 1000, largeur_pied=largeur / 1000,
                e_max_mm=e_max, jeu_mm=jeu, r_plaque_mm=r_plaque, r_sortie_mm=r_sortie, voile_mm=v)


def construire(H: float | None = None) -> dict:
    """Le squelette résolu : corps, articulations, masses. Rien n'est écrit."""
    sq, an, jo = lire("squelette.yaml"), lire("anthropometry.yaml"), lire("joints.yaml")
    cfg, cat = lire("configuration_S.yaml"), D.charger_catalogue()
    H = H or an["tailles"]["S"]["H_m"]
    R = an["ratios"]
    EC = ecarts_cheville()
    axes = {j["nom"]: j["articulation"]["axe"] for g in ("jambes", "bras", "taille", "nuque") for j in jo[g]}
    masse_totale = C.evaluer_configuration(H, True)["masse"]
    v3 = cfg["hypothese_v3"]["haut_du_corps"]
    sup_rs02 = D.val(cfg["structure_rs02_supplement_g"]) / 1000
    charge = C.lire(C.EXIGENCES)["charge_utile"]["valeur_kg"]

    def actionneur(a):
        return cfg["jambes"][a["actionneur"]["config"]] if "config" in a["actionneur"] else v3["actionneur"]

    # articulations, dédoublées pour les côtés
    arts = []
    for a in sq["articulations"]:
        cotes = list(COTES) if a.get("cote") else [None]
        for c in cotes:
            nom = f"{c}_{a['nom']}" if c else a["nom"]
            par = a["parent"]
            if par not in sq["segments"]:                       # parent = une articulation
                pa = next(x for x in sq["articulations"] if x["nom"] == par)
                par = f"{c}_{par}" if (c and pa.get("cote")) else par
            pos = [longueur(a["position"].get(k), R, H, EC) for k in "xyz"]
            if c == "right":
                pos[1] = -pos[1]
            ax = {"x": [1, 0, 0], "y": [0, 1, 0], "z": [0, 0, 1]}[a.get("axe") or axes[a["nom"]]]
            if c == "right":                                    # symétrie de joints.yaml : (-x, +y, -z)
                ax = [-ax[0], ax[1], -ax[2]]
            seg = a.get("vers")
            corps = (f"{c}_{seg}" if c and seg else seg) or (f"{nom}_corps")
            arts.append(dict(nom=nom, base=a["nom"], parent_art=par, pos=pos, axe=ax, corps=corps,
                             segment=seg, cote=c, actionneur=actionneur(a),
                             provisoire=bool(a.get("nom_provisoire"))))
    # corps « porteur » de chaque articulation parent
    corps_de = {x["nom"]: x["corps"] for x in arts}
    for x in arts:
        x["parent_corps"] = corps_de.get(x["parent_art"], x["parent_art"])

    # masses : actionneurs, supplément RS02, charge utile, structure (Winter)
    m_act = sum(D.val(cat["candidats"][x["actionneur"]]["masse_g"]) / 1000 for x in arts)
    m_sup = sup_rs02 * sum(1 for x in arts if x["actionneur"] == "rs02")
    m_struct = masse_totale - m_act - m_sup - charge
    fw = {k: (v["valeur"] if isinstance(v, dict) else v) for k, v in an["masses"].items()}
    segs = {}
    for nom, s in sq["segments"].items():
        double = any(x["segment"] == nom and x["cote"] for x in arts)
        frac = sum(fw[k] * c for k, c in s["masse_winter"].items())
        for c in (list(COTES) if double else [None]):
            segs[f"{c}_{nom}" if c else nom] = dict(base=nom, spec=s, cote=c,
                                                   masse=m_struct * frac + (charge if s.get("porte_charge_utile") else 0.0))
    return dict(H=H, arts=arts, segs=segs, R=R, cat=cat, ecarts=EC, masse_totale=masse_totale,
                m_act=m_act, m_sup=m_sup, m_struct=m_struct, charge=charge, sup_rs02=sup_rs02)


def mjcf(sq: dict) -> str:
    """Le MJCF : un corps par articulation (ou par segment porté), masses par géométrie."""
    H, R, cat = sq["H"], sq["R"], sq["cat"]
    enfants: dict[str, list] = {}
    for x in sq["arts"]:
        enfants.setdefault(x["parent_corps"], []).append(x)
    f = lambda v: f"{v:.5f}"

    def geom_segment(nom):
        s = sq["segs"][nom]
        sp, m = s["spec"], s["masse"]
        if sp["forme"] == "capsule":
            L, r = longueur(sp["longueur"], R, H), longueur(sp["rayon"], R, H)
            return f'<geom type="capsule" fromto="0 0 0 0 0 {f(-L)}" size="{f(r)}" mass="{f(m)}" rgba=".75 .75 .8 1"/>'
        d = {k: longueur(sp["dims"][k], R, H) for k in "xyz"}
        # pied : semelle posée au sol, sous l'axe du roulis (écart ANSUR, squelette.yaml)
        cz = {"tronc": d["z"] / 2, "tete": d["z"] / 2, "main": -d["z"] / 2,
              "pied": -sq["ecarts"]["hauteur_axe_cheville"] + d["z"] / 2}.get(s["base"], 0.0)
        if s["base"] == "pied":                    # écart ANSUR : la chape du pied enjambe le tibia
            d["y"] = sq["ecarts"]["largeur_pied"]
        cx = longueur({"pied_longueur": 0.25}, R, H) if s["base"] == "pied" else 0.0
        return (f'<geom type="box" pos="{f(cx)} 0 {f(cz)}" size="{f(d["x"]/2)} {f(d["y"]/2)} {f(d["z"]/2)}" '
                f'mass="{f(m)}" rgba=".75 .75 .8 1"/>')

    def geom_actionneur(x):
        c = cat["candidats"][x["actionneur"]]
        cm = c["cotes_montage"]
        r = cm["diametre_corps"] / 2000
        L = D.val(cm["longueur"]) / 1000 if isinstance(cm["longueur"], dict) else cm["longueur"] / 1000
        a = [v * L / 2 for v in x["axe"]]
        m = D.val(c["masse_g"]) / 1000 + (sq["sup_rs02"] if x["actionneur"] == "rs02" else 0.0)
        coul = {"rs02": ".85 .35 .2 1", "rs00": ".2 .45 .85 1", "rs05": ".25 .7 .35 1"}[x["actionneur"]]
        return (f'<geom type="cylinder" fromto="{f(-a[0])} {f(-a[1])} {f(-a[2])} {f(a[0])} {f(a[1])} {f(a[2])}" '
                f'size="{f(r)}" mass="{f(m)}" rgba="{coul}"/>')

    def corps(x, ind):
        p = x["pos"]
        lignes = [f'{ind}<body name="{x["corps"]}" pos="{f(p[0])} {f(p[1])} {f(p[2])}">',
                  f'{ind}  <joint name="{x["nom"]}" type="hinge" axis="{x["axe"][0]} {x["axe"][1]} {x["axe"][2]}" damping="0.1"/>',
                  f"{ind}  {geom_actionneur(x)}"]
        if x["segment"]:
            lignes.append(f"{ind}  {geom_segment(x['corps'])}")
        for e in enfants.get(x["corps"], []):
            lignes += corps(e, ind + "  ")
        lignes.append(f"{ind}</body>")
        return lignes

    # bassin : hanche (0,5 cheville_hauteur sous le bassin), cuisse, tibia, puis
    # les deux écarts de la cheville à la place de `cheville_hauteur` (ANSUR)
    ec = sq["ecarts"]
    z0 = (longueur({"cuisse": 1.0, "tibia": 1.0, "cheville_hauteur": 0.5}, R, H)
          + ec["hauteur_axe_cheville"])
    corps_lignes = []
    for e in enfants.get("bassin", []):
        corps_lignes += corps(e, "      ")
    return "\n".join([
        '<mujoco model="yxor_s_v3">',
        "  <!-- Engendré par scripts/squelette.py depuis params/ : ne pas éditer. Aucune géométrie ToddlerBot. -->",
        '  <option gravity="0 0 -9.81"/>',
        '  <visual><global offwidth="1600" offheight="1200"/></visual>',
        '  <worldbody>',
        '    <light pos="0 -1 2" dir="0 .5 -1"/>',
        '    <geom name="sol" type="plane" size="2 2 .1" rgba=".92 .92 .9 1"/>',
        f'    <body name="bassin" pos="0 0 {f(z0)}">',
        '      <freejoint name="racine"/>',
        f"      {geom_segment('bassin')}",
        *corps_lignes,
        "    </body>",
        "  </worldbody>",
        "</mujoco>", ""])


def rendre(xml_path: Path, png: Path) -> None:
    os.environ.setdefault("MUJOCO_GL", "egl")
    import mujoco
    sys.path.insert(0, str(REPO / "sim"))
    from render import write_png
    m = mujoco.MjModel.from_xml_path(str(xml_path))
    d = mujoco.MjData(m)
    mujoco.mj_forward(m, d)
    cam = mujoco.MjvCamera()
    cam.lookat[:] = [0, 0, 0.32]
    cam.distance, cam.azimuth, cam.elevation = 1.35, 140, -12
    r = mujoco.Renderer(m, height=900, width=1200)
    try:
        r.update_scene(d, camera=cam)
        img = r.render()
    finally:
        r.close()
    write_png(str(png), img.tobytes(), 1200, 900)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--rendu", action="store_true", help="image de contrôle, hors écran (EGL)")
    a = ap.parse_args(argv)
    sq = construire()
    SORTIE.mkdir(parents=True, exist_ok=True)
    xml = SORTIE / "yxor_s_v3.xml"
    xml.write_text(mjcf(sq), encoding="utf-8")
    print(f"  H_S = {sq['H']} m ; {len(sq['arts'])} articulations ; masse du modèle de S (v3) {sq['masse_totale']:.3f} kg"
          f" = actionneurs {sq['m_act']:.3f} + supplément RS02 {sq['m_sup']:.3f} + charge utile {sq['charge']:.3f}"
          f" + structure {sq['m_struct']:.3f}")
    print(f"  -> {xml.relative_to(REPO)}")
    ec, ch = sq["ecarts"], longueur({"cheville_hauteur": 1.0}, sq["R"], sq["H"])
    allong = ec["hauteur_axe_cheville"] - ch
    print(f"  écart ANSUR à la cheville : axe à {ec['hauteur_axe_cheville']*1000:.1f} mm du sol (ANSUR : {ch*1000:.1f} mm) ; "
          f"jambe allongée de {allong*1000:.1f} mm, hauteur {sq['H'] + allong:.3f} m au lieu de {sq['H']} m ; "
          f"pied large de {ec['largeur_pied']*1000:.1f} mm (ANSUR {longueur({'pied_largeur': 1.0}, sq['R'], sq['H'])*1000:.1f})")
    print("| Articulation | Actionneur | Segment porté | Longueur (m) |")
    print("| --- | --- | --- | ---: |")
    for x in sq["arts"]:
        seg = x["segment"]
        L = ""
        if seg:
            sp = lire("squelette.yaml")["segments"][seg]
            dims = [sp["longueur"]] if "longueur" in sp else list(sp["dims"].values())
            L = f"{max(longueur(e, sq['R'], sq['H']) for e in dims):.3f}"
        print(f"| {x['nom']}{' (nom provisoire)' if x['provisoire'] else ''} | {x['actionneur']} | {seg or '—'} | {L} |")
    if a.rendu:
        png = SORTIE / "yxor_s_v3.png"
        rendre(xml, png)
        print(f"  -> {png.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
