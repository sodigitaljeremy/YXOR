#!/usr/bin/env python3
"""Semelle d'apprentissage — première pièce YXOR.

    .venv/bin/python parts/semelle_apprentissage.py
    .venv/bin/python parts/semelle_apprentissage.py --palier P1 --resserrement 0.6

Se lance avec le venv DU PROJET (règle des deux interpréteurs).

═══════════════════════════════════════════════════════════════════════
 CE QU'ELLE EST, ET CE QU'ELLE N'EST PAS
═══════════════════════════════════════════════════════════════════════

Elle ne remplace rien et ne s'interface avec rien. Ce n'est pas une pièce
de robot : c'est le **prototype de la méthode** — un modèle, un paramètre
d'épaisseur, un DXF par couple machine-matériau.

Ce qu'elle exerce, et pourquoi chaque point compte :

  règle 1        toute cote d'échelle dérive de H et d'un ratio
  nature         echelle / procede séparées (fiche 0013)
  origine        chaque cote tracée (fiche 0010), relevé déposé
  rayon interne  0,5 x épaisseur — le resserrement en crée quatre
  angle rentrant aucun ne reste vif : c'est le but du resserrement
  DXF            millimètres, échelle 1:1, contour fermé
  plan A4        imprimable, avec réglet de contrôle

⚠ UN RECTANGLE ARRONDI N'AURAIT EXERCÉ NI LE RAYON INTERNE NI L'ANGLE
  RENTRANT : il n'a que des angles convexes. D'où le resserrement, qui
  n'est pas décoratif — il est la raison d'être de la forme.
"""
from __future__ import annotations

import argparse
import datetime
import sys
from pathlib import Path

import build123d as bd
import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from plan_decoupe import ecrire_plan_a4, polylignes_depuis_face  # noqa: E402

NOM = "semelle_apprentissage"
SORTIE = REPO / "exports" / "parts"


# ─────────────────────────────────────────────────── accès aux paramètres
class Cotes:
    """Contrat des fiches 0010 et 0013 : l'origine vient de l'accesseur.

    Chaque appel inscrit la cote au relevé. Un littéral nu dans le code
    d'une pièce n'y figurerait pas — et l'audit le signalerait.
    """

    def __init__(self):
        self.anthro = yaml.safe_load((REPO / "params/anthropometry.yaml").read_text("utf-8"))
        self.hw = yaml.safe_load((REPO / "params/hardware.yaml").read_text("utf-8"))
        self.releve: list[dict] = []

    def _note(self, cle, valeur, origine, nature, source):
        self.releve.append(dict(cle=cle, valeur=valeur, origine=origine,
                                nature=nature, source=source))
        return valeur

    def echelle(self, cle_ratio: str, H_m: float) -> float:
        """Cote d'échelle : H x ratio. Règle 1. En millimètres."""
        r = self.anthro["ratios"][cle_ratio]
        v = round(H_m * 1000.0 * r["valeur"], 4)
        return self._note(f"ratios.{cle_ratio}", v, "litterature", "echelle",
                          f"{r['source']} (x H)")

    def procede(self, proc: str, cle: str) -> float:
        p = self.hw["procedes"][proc]
        v = p[cle]
        if v is None:
            raise ValueError(f"procedes.{proc}.{cle} vaut null — à mesurer "
                             f"avant d'en dépendre (fiches 0014, 0015)")
        return self._note(f"procedes.{proc}.{cle}", v, "mesure", "procede",
                          f"hardware.yaml, procédé {proc}")

    def choix(self, nom: str, valeur, motif: str):
        """Choix de projet assumé : ni dérivé, ni sourcé ailleurs."""
        return self._note(nom, valeur, "propre", "echelle", motif)


# ──────────────────────────────────────────────────────────── géométrie
def construire(c: Cotes, palier: str, resserrement: float, proc: str,
               ratio_coins: float, ratio_etendue: float):
    H = c._note(f"paliers.{palier}", c.anthro["paliers"][palier],
                "amont" if palier == "P1" else "propre", "echelle",
                "taille publiée de ToddlerBot (fiche 0011)" if palier == "P1"
                else "choix de projet (fiche 0011)")

    L = c.echelle("pied_longueur", H)
    W = c.echelle("pied_largeur", H)
    ep = c.procede(proc, "epaisseur")
    r_int = c.procede(proc, "rayon_interieur_min")
    rc = c.choix("ratio_coins", ratio_coins,
                 "choix libre : aucune règle ne contraint un congé convexe")
    r_ext = round(W * rc, 4)
    ratio = c.choix("ratio_resserrement", resserrement,
                    "choix de projet — aucune source anthropométrique")

    profondeur = round((W - W * ratio) / 2.0, 4)      # par côté
    re_ = c.choix("ratio_etendue_creux", ratio_etendue,
                  "choix de projet — aucune source anthropométrique")
    etendue = round(L * re_, 4)                        # longueur du creux
    # rayon du cercle qui creuse le flanc : segment circulaire de corde
    # `etendue` et de flèche `profondeur`
    R = round((etendue ** 2 / 4.0 + profondeur ** 2) / (2.0 * profondeur), 4)
    if R < r_int:
        raise ValueError(f"le creux a un rayon de {R} mm, sous le minimum "
                         f"{r_int} mm du procédé")

    with bd.BuildPart() as piece:
        with bd.BuildSketch() as esq:
            bd.Rectangle(L, W)
            bd.fillet(esq.vertices(), radius=r_ext)     # congés convexes
            # les deux creux de flanc, qui créent les angles RENTRANTS
            for signe in (1, -1):
                with bd.Locations((0, signe * (W / 2.0 - profondeur + R))):
                    bd.Circle(R, mode=bd.Mode.SUBTRACT)
            # aucun angle vif rentrant : congés au minimum du procédé
            bd.fillet(esq.vertices(), radius=r_int)
        bd.extrude(amount=ep)

    return piece.part, dict(H=H, L=L, W=W, ep=ep, r_int=r_int, r_ext=r_ext,
                            ratio=ratio, profondeur=profondeur, R=R,
                            largeur_creux=round(W * ratio, 4))


# ──────────────────────────────────────────────────────────────── sorties
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--palier", default="P2", choices=["P1", "P2", "P3"])
    ap.add_argument("--resserrement", type=float, default=0.70)
    ap.add_argument("--procede", default="cutter_carton")
    ap.add_argument("--coins", type=float, default=0.25,
                    help="congé des coins, en fraction de la largeur")
    ap.add_argument("--etendue", type=float, default=0.50,
                    help="longueur du creux, en fraction de la longueur")
    a = ap.parse_args(argv)

    c = Cotes()
    piece, d = construire(c, a.palier, a.resserrement, a.procede,
                          a.coins, a.etendue)
    SORTIE.mkdir(parents=True, exist_ok=True)
    base = f"{NOM}_{a.palier}_{a.procede}"

    print(f"Semelle d'apprentissage — palier {a.palier}, procédé {a.procede}\n")
    print(f"  longueur        {d['L']:8.2f} mm   = H x ratio pied_longueur")
    print(f"  largeur         {d['W']:8.2f} mm   = H x ratio pied_largeur")
    print(f"  largeur au creux{d['largeur_creux']:8.2f} mm   = largeur x {d['ratio']}")
    print(f"  profondeur creux{d['profondeur']:8.2f} mm   par flanc")
    print(f"  rayon du creux  {d['R']:8.2f} mm   (minimum procédé {d['r_int']})")
    print(f"  congés convexes {d['r_ext']:8.2f} mm")
    print(f"  épaisseur       {d['ep']:8.2f} mm")
    print(f"  volume          {piece.volume:8.1f} mm3")

    # --- STEP / STL ---
    bd.export_step(piece, str(SORTIE / f"{base}.step"), unit=bd.Unit.MM)
    bd.export_stl(piece, str(SORTIE / f"{base}.stl"))

    # --- DXF : la face plate, contour fermé, millimètres ---
    face = piece.faces().sort_by(bd.Axis.Z)[0]
    exp = bd.ExportDXF(unit=bd.Unit.MM)
    exp.add_shape(face)
    exp.write(str(SORTIE / f"{base}.dxf"))

    # --- contrôles, avant de prétendre que c'est bon ---
    import ezdxf
    doc = ezdxf.readfile(str(SORTIE / f"{base}.dxf"))
    unites = doc.header.get("$INSUNITS")
    ents = list(doc.modelspace())
    bb = piece.bounding_box()
    ctrl = [("DXF en millimètres ($INSUNITS = 4)", unites == 4),
            ("contour non vide", len(ents) > 0),
            ("longueur conforme", abs(bb.size.X - d["L"]) < 1e-6),
            ("largeur conforme", abs(bb.size.Y - d["W"]) < 1e-6),
            ("épaisseur conforme", abs(bb.size.Z - d["ep"]) < 1e-6),
            ("tient sur une A4", d["L"] < 180 and d["W"] < 180)]
    print("\n  contrôles :")
    for lib, ok in ctrl:
        print(f"    {'OK ' if ok else 'ÉCHEC'}  {lib}")

    # --- plan A4 ---
    contours = polylignes_depuis_face(face)
    stamp = datetime.date.today().isoformat()
    larg, haut = ecrire_plan_a4(
        contours, SORTIE / f"{base}_planA4.pdf",
        f"YXOR — semelle d'apprentissage",
        [f"Palier {a.palier} (H = {d['H']} m)    matiere : {a.procede}    "
         f"epaisseur {d['ep']:.1f} mm",
         f"Hors-tout {d['L']:.2f} x {d['W']:.2f} mm    "
         f"resserrement {d['ratio']:.2f} -> {d['largeur_creux']:.2f} mm au creux",
         f"Rayon interieur minimal {d['r_int']:.1f} mm    "
         f"conges exterieurs {d['r_ext']:.2f} mm",
         f"Genere le {stamp} — ne pas coter sur ce plan, il fait foi par sa geometrie"])
    print(f"\n  plan A4 : {larg:.2f} x {haut:.2f} mm sur 210 x 297")

    # --- relevé d'origines, lu par scripts/audit_origines.py ---
    lignes = ["# Relevé d'origines — GÉNÉRÉ, ne pas éditer à la main.",
              f"# Pièce : {NOM}   palier {a.palier}   procédé {a.procede}",
              f"# Généré le {stamp} par parts/{NOM}.py", "", "cotes:"]
    for r in c.releve:
        lignes += [f"  - cle: {r['cle']}",
                   f"    valeur: {r['valeur']}",
                   f"    origine: {r['origine']}",
                   f"    nature: {r['nature']}",
                   f"    source: \"{r['source']}\""]
    (REPO / "parts" / f"{NOM}.origines.yaml").write_text("\n".join(lignes) + "\n", "utf-8")
    print(f"  relevé : parts/{NOM}.origines.yaml  ({len(c.releve)} cotes)")
    print(f"\n  sorties dans exports/parts/ : .step .stl .dxf _planA4.pdf")
    return 0 if all(ok for _, ok in ctrl) else 1


if __name__ == "__main__":
    sys.exit(main())
