#!/usr/bin/env python3
"""Actionneurs factices RS00, RS02, RS05 : encombrement et gabarit de perçage.

    .venv/bin/python parts/actionneurs_factices.py

Créé le 2026-10-03. Pour chaque actionneur de la configuration de S (fiche
0067) et de l'hypothèse v3 :
  · un volume factice (STEP) : le corps à son diamètre et sa longueur,
    plus la bride si elle est publiée ;
  · un GABARIT DE PERÇAGE côté carter (DXF, par réglage) : le contour
    extérieur et les trous de passage des vis de fixation, sur leur cercle.

TOUTES les cotes viennent de params/ (règle 2, quincaillerie) :
`candidats.<id>.cotes_montage` (plans cotés du registre, lus le 2026-10-02
et le 2026-10-03) et `vis.<M>.passage` de params/hardware.yaml. Aucune cote
inventée : l'ouverture centrale (passage du rotor) n'est PAS dessinée, son
diamètre n'étant publié pour aucun des trois modèles.

Un trou plus petit que le minimum du réglage n'est pas découpable : il est
dessiné, signalé, et sera à pointer puis reprendre au foret.

Ne produit pas de relevé `.origines.yaml` : ce ne sont pas des pièces du
robot, et elles n'ont pas de page sur le site. Sorties dans exports/parts/.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import procedes as PROC  # noqa: E402

import build123d as bd  # noqa: E402

SORTIE = REPO / "exports" / "parts"
REGLAGES = ("cutter_cartonplume_5", "operateur_cn_alu_3")


def lire(nom: str) -> dict:
    return yaml.safe_load((REPO / "params" / nom).read_text(encoding="utf-8"))


def val(x):
    return x["valeur"] if isinstance(x, dict) else x


def modeles() -> list[str]:
    cfg = lire("configuration_S.yaml")
    ids = list(dict.fromkeys(list(cfg["jambes"].values()) + [cfg["hypothese_v3"]["haut_du_corps"]["actionneur"]]))
    return sorted(ids)


def factice(cm: dict) -> bd.Part:
    """Le volume : corps (et bride si publiée), axe Z, face avant en Z = 0."""
    L, d = val(cm["longueur"]), cm["diametre_corps"]
    with bd.BuildPart() as p:
        bd.Cylinder(d / 2, L, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MAX))
        if cm.get("diametre_bride"):
            # épaisseur de bride : non publiée ; le volume s'en tient au corps,
            # la bride n'est que dans le gabarit (diamètre seul).
            pass
    return p.part


def gabarit(cm: dict, vis: dict, ep: float) -> tuple[bd.Part, list[dict]]:
    """Plaque Ø extérieur, trous de passage sur le cercle de fixation du carter."""
    fx = cm["fixation_boitier"]
    D_ext = cm.get("diametre_bride") or cm["diametre_corps"]
    trou = vis[fx["vis"]]["passage"]
    r_cercle = fx["diametre_percage"] / 2
    trous = []
    with bd.BuildPart() as p:
        with bd.BuildSketch():
            bd.Circle(D_ext / 2)
            a0 = math.radians(fx.get("phase_deg") or 0.0)   # STEP officiel, 2026-10-03
            for i in range(fx["nombre"]):
                a = a0 + 2 * math.pi * i / fx["nombre"]
                x, y = r_cercle * math.cos(a), r_cercle * math.sin(a)
                with bd.Locations((x, y)):
                    bd.Circle(trou / 2, mode=bd.Mode.SUBTRACT)
                trous.append(dict(x=round(x, 4), y=round(y, 4), d=trou))
        bd.extrude(amount=ep)
    return p.part, trous


def main(argv=None) -> int:
    cat = lire("actionneurs.yaml")["candidats"]
    vis = lire("hardware.yaml")["vis"]
    SORTIE.mkdir(parents=True, exist_ok=True)
    fautes = 0
    for cid in modeles():
        cm = cat[cid].get("cotes_montage")
        if not cm:
            print(f"  ✗ {cid} : cotes de montage absentes du catalogue — non dessiné")
            fautes += 1
            continue
        corps = factice(cm)
        bd.export_step(corps, str(SORTIE / f"actionneur_{cid}.step"), unit=bd.Unit.MM)
        print(f"  {cid} : volume Ø{cm['diametre_corps']} × {val(cm['longueur'])} mm "
              f"({cm['source']}) -> actionneur_{cid}.step")
        for rid in REGLAGES:
            r = PROC.reglage(rid)
            ep = r["epaisseur"]
            plaque, trous = gabarit(cm, vis, ep)
            face = plaque.faces().sort_by(bd.Axis.Z)[0]
            exp = bd.ExportDXF(unit=bd.Unit.MM)
            exp.add_shape(face)
            nom = f"actionneur_{cid}_gabarit_{rid}.dxf"
            exp.write(str(SORTIE / nom))
            d_min = r.get("trou_decoupe_min") or 2 * (PROC.rayon_interieur_min(ep, r.get("rayon_interieur_min_machine")) or 0)
            petits = [t for t in trous if t["d"] < d_min - 1e-9]
            print(f"    {rid} (ép. {ep} mm) : {len(trous)} trous Ø{trous[0]['d']} sur Ø"
                  f"{cm['fixation_boitier']['diametre_percage']} -> {nom}"
                  + (f" ; ⚠ {len(petits)} trou(s) sous le minimum découpable Ø{d_min:g} : pointer, "
                     "puis reprendre au foret" if petits else ""))
    return 1 if fautes else 0


if __name__ == "__main__":
    sys.exit(main())
