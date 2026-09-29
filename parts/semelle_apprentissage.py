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
import json
import sys
from pathlib import Path

import build123d as bd
import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from plan_decoupe import ecrire_plan_a4, polylignes_depuis_face  # noqa: E402
import profil  # noqa: E402

NOM = "semelle_apprentissage"

# Placements des lignes de repère du schéma. Ce ne sont PAS des cotes de
# la pièce : ils positionnent des annotations sur un dessin. Déclarés
# comme tels pour que l'audit ne les compte pas comme des cotes muettes.
COS45 = 0.7071          # non-cote: cos 45°, point de tangence sur un congé
AXE = 0.0               # non-cote: axe de symétrie longitudinal
REP_CONGE_X = 0.06      # non-cote: décalage du repère, en fraction de la longueur
REP_CONGE_Y = 0.20      # non-cote: décalage du repère, en fraction de la largeur
REP_RINT_X = 0.24       # non-cote: abscisse du repère de rayon intérieur
REP_RINT_DX = 0.05      # non-cote: décalage du repère de rayon intérieur
REP_RINT_DY = 0.26      # non-cote: décalage du repère de rayon intérieur
REP_RINT_MARGE = 0.2    # non-cote: écart au bord pour poser le repère
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
        v = round(H_m * 1000.0 * r["valeur"], 4)  # non-cote: conversion mètre -> millimètre
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

    # non-cote: le 2 répartit le resserrement également sur les deux flancs
    profondeur = round((W - W * ratio) / 2.0, 4)      # par côté
    re_ = c.choix("ratio_etendue_creux", ratio_etendue,
                  "choix de projet — aucune source anthropométrique")
    etendue = round(L * re_, 4)                        # longueur du creux
    # rayon du cercle qui creuse le flanc : segment circulaire de corde
    # `etendue` et de flèche `profondeur`
    # non-cote: constantes de la formule du rayon d'un segment circulaire
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
                # non-cote: demi-largeur, le flanc est à W/2 de l'axe
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
    defaut = yaml.safe_load((REPO / "params/hardware.yaml").read_text("utf-8")
                            ).get("procede_defaut", "cutter_carton")
    ap.add_argument("--procede", default=defaut,
                    help=f"couple machine-matériau ; défaut lu dans hardware.yaml "
                         f"(actuellement {defaut})")
    ap.add_argument("--coins", type=float, default=0.25,
                    help="congé des coins, en fraction de la largeur")
    ap.add_argument("--etendue", type=float, default=0.50,
                    help="longueur du creux, en fraction de la longueur")
    ap.add_argument("--cannelures", type=float, default=0.0,
                    help="angle des cannelures par rapport à la LONGUEUR de la pièce, "
                         "en degrés. 0 = le long de la pièce (recommandé). "
                         "Sans effet si le matériau est isotrope.")
    a = ap.parse_args(argv)

    c = Cotes()
    try:
        piece, d = construire(c, a.palier, a.resserrement, a.procede,
                              a.coins, a.etendue)
    except ValueError as err:
        # Message net plutôt qu'une trace : ce n'est pas un bug, c'est le
        # garde-fou de la fiche 0015 qui refuse une cote non mesurée.
        print(f"\n  ARRÊT — {err}\n")
        print(f"  Le procédé « {a.procede} » n'a pas toutes ses cotes.")
        print("  Renseignez-les dans params/hardware.yaml après mesure,")
        print("  puis relancez. Voir le protocole au journal du 2026-09-28.")
        return 2
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
    contours = polylignes_depuis_face(face)

    # --- LA SECONDE IMPLÉMENTATION, ET SON GARDE-FOU ------------------
    # Le navigateur ne peut pas exécuter build123d : la simulation en
    # direct (fiche 0023) recalcule la forme analytiquement. Deux
    # implémentations de la même chose divergent toujours, et celle-ci
    # divergerait en restant plausible. On les confronte ici, à chaque
    # régénération, dans les DEUX sens : l'un vérifie la forme, l'autre
    # vérifie qu'aucun morceau n'a été oublié.
    an_d = profil.cotes(d["H"], c.anthro["ratios"]["pied_longueur"]["valeur"],
                        c.anthro["ratios"]["pied_largeur"]["valeur"],
                        a.resserrement, a.coins, a.etendue, d["ep"])
    # non-cote: même seuil d'égalité numérique
    ecarts_cotes = [(k, d[k], an_d[k]) for k in ("L", "W", "r_ext", "R",
                                                 "profondeur", "largeur_creux")
                    if abs(d[k] - an_d[k]) > 1e-4]
    # Le simulateur applique la règle « rayon intérieur = 0,5 x épaisseur »
    # (CLAUDE.md). Si la donnée du procédé ne la suit pas, le navigateur
    # dessinerait autre chose que la pièce. On le dit ici, pas plus tard.
    # non-cote: 1e-4 est le seuil d'égalité de deux nombres, pas une cote
    if abs(an_d["r_int"] - d["r_int"]) > 1e-4:
        ecarts_cotes.append(("r_int (0,5 x épaisseur)", d["r_int"], an_d["r_int"]))
    # non-cote: finesse d'échantillonnage de la confrontation
    an_c = profil.contour(an_d, n_arc=400)
    ecart = max(profil.hausdorff(an_c, contours[0]),
                profil.hausdorff(contours[0], an_c))
    ctrl.append((f"contour analytique conforme au noyau CAO "
                 f"({ecart:.4f} mm <= {profil.TOLERANCE_MM})",
                 ecart <= profil.TOLERANCE_MM and not ecarts_cotes))
    if ecarts_cotes:
        print("\n  ⚠ COTES DIVERGENTES entre le noyau CAO et le calcul analytique :")
        for k, v1, v2 in ecarts_cotes:
            print(f"      {k} : CAO {v1} / analytique {v2}")

    # --- plan A4 ---
    print("\n  contrôles :")
    for lib, ok in ctrl:
        print(f"    {'OK ' if ok else 'ÉCHEC'}  {lib}")

    stamp = datetime.date.today().isoformat()
    mat = c.hw["materiaux"].get(c.hw["procedes"][a.procede]["materiau"], {})
    anisotrope = bool(mat.get("anisotrope"))
    fleche = None
    if anisotrope:
        # Sans flèche sur le plan, déclarer un sens de fibre ne sert à
        # rien : au moment de scotcher la feuille sur la matière, rien ne
        # dit comment l'orienter. Deux pièces du même DXF à 90° l'une de
        # l'autre ne sont pas la même pièce.
        c.choix("orientation_cannelures_deg", a.cannelures,
                "angle des cannelures par rapport à la longueur de la pièce")
        fleche = (a.cannelures,
                  f"SENS DES CANNELURES ({a.cannelures:.0f} deg) — aligner avant de couper")
    larg, haut = ecrire_plan_a4(
        contours, SORTIE / f"{base}_planA4.pdf",
        f"YXOR — semelle d'apprentissage",
        [f"Palier {a.palier} (H = {d['H']} m)    matiere : {a.procede}    "
         f"epaisseur {d['ep']:.1f} mm",
         f"Hors-tout {d['L']:.2f} x {d['W']:.2f} mm    "
         f"resserrement {d['ratio']:.2f} -> {d['largeur_creux']:.2f} mm au creux",
         f"Rayon interieur minimal {d['r_int']:.1f} mm    "
         f"conges exterieurs {d['r_ext']:.2f} mm",
         (f"Materiau ANISOTROPE : orienter la feuille selon la fleche ci-dessous."
          if anisotrope else
          "Materiau isotrope : l'orientation de la feuille est indifferente."),
         f"Genere le {stamp} — ne pas coter sur ce plan, il fait foi par sa geometrie"],
        fleche=fleche)
    print(f"\n  plan A4 : {larg:.2f} x {haut:.2f} mm sur 210 x 297")

    # --- cotes du schéma : la pièce déclare, le générateur dessine ---
    # Le `rang` fixe l'ordre de LECTURE, pas l'ordre du fichier : hors-tout
    # d'abord, puis les cotes dérivées, puis celles du procédé. Les lettres
    # sont attribuées par le générateur, une règle pour toutes les pièces.
    L2, W2 = d["L"] / 2, d["W"] / 2
    Wc2 = d["largeur_creux"] / 2
    rc = d["r_ext"]
    # Chaque cote du schéma DÉCLARE la clé du relevé qui la gouverne. Sans
    # elle, le site devrait rapprocher le dessin du registre en devinant
    # d'après le libellé — un lien qui casse sans rien dire le jour où un
    # libellé change. Quand deux clés concourent (la largeur au creux vient
    # de la largeur ET du resserrement), on déclare celle qui répond à
    # « pourquoi ce nombre-là » : le choix, pas la grandeur qu'il module.
    kp = f"procedes.{a.procede}"
    schema = [
        ("hors_tout", "longueur", d["L"], "ratios.pied_longueur",
         {"type": "cote_h", "x1": -L2, "x2": L2}),
        ("hors_tout", "largeur", d["W"], "ratios.pied_largeur",
         {"type": "cote_v", "y1": -W2, "y2": W2}),
        ("derivee", "largeur au creux", d["largeur_creux"], "ratio_resserrement",
         {"type": "cote_v_int", "x": AXE, "y1": -Wc2, "y2": Wc2}),
        ("derivee", "congé extérieur", rc, "ratio_coins",
         {"type": "rayon", "x": round(L2 - rc + rc * COS45, 4),
          "y": round(W2 - rc + rc * COS45, 4),
          "dx": round(d["L"] * REP_CONGE_X, 4),
          "dy": round(d["W"] * REP_CONGE_Y, 4)}),
        ("procede", "rayon intérieur minimal", d["r_int"],
         f"{kp}.rayon_interieur_min",
         {"type": "rayon", "x": round(-d["L"] * REP_RINT_X, 4),
          "y": round(-W2 + REP_RINT_MARGE, 4),
          "dx": round(-d["L"] * REP_RINT_DX, 4),
          "dy": round(-d["W"] * REP_RINT_DY, 4)}),
        ("procede", "épaisseur", d["ep"], f"{kp}.epaisseur", {"type": "note"}),
    ]
    # Garde-fou : une clé déclarée qui n'existe pas dans le relevé est un
    # défaut, pas un tiret à afficher.
    connues = {r["cle"] for r in c.releve}
    for _, lib, _, cle, _ in schema:
        if cle not in connues:
            raise SystemExit(f"schéma : la cote « {lib} » déclare la clé "
                             f"« {cle} », absente du relevé. Clés relevées : "
                             + ", ".join(sorted(connues)))

    # --- relevé, lu par scripts/audit_origines.py ET scripts/regenerer.py ---
    # La pièce publie ses propres métadonnées : elle seule les connaît.
    # L'application ne fait que les lire — elle ne crée aucune donnée.
    proc = c.hw["procedes"][a.procede]
    lignes = ["# Relevé d'origines — GÉNÉRÉ, ne pas éditer à la main.",
              f"# Pièce : {NOM}   palier {a.palier}   procédé {a.procede}",
              f"# Généré le {stamp} par parts/{NOM}.py", "",
              "piece:",
              f"  nom: {NOM}",
              f"  titre: \"Semelle d'apprentissage\"",
              f"  base_fichier: {base}",
              f"  palier: {a.palier}",
              f"  procede: {a.procede}",
              f"  machine: \"{proc['machine'] or 'non déterminé'}\"",
              f"  lieu: \"{proc['lieu'] or 'non déterminé'}\"",
              f"  materiau: {proc['materiau']}",
              f"  epaisseur_mm: {d['ep']}",
              f"  rayon_interieur_min_mm: {d['r_int']}",
              f"  saignee_mm: {proc['saignee'] if proc['saignee'] is not None else 'null'}",
              f"  voile_min_mm: {proc['voile_min'] if proc['voile_min'] is not None else 'null'}",
              f"  fixation: \"{proc['fixation']}\"",
              f"  anisotrope: {'true' if anisotrope else 'false'}",
              (f"  orientation_cannelures_deg: {a.cannelures}" if anisotrope
               else "  orientation_cannelures_deg: null"),
              f"  longueur_mm: {d['L']}",
              f"  largeur_mm: {d['W']}",
              f"  volume_mm3: {round(piece.volume, 1)}",
              f"  role: >",
              "    Pièce d'apprentissage. Ne remplace rien, ne s'interface avec rien.",
              "    C'est le prototype de la méthode : un modèle, un paramètre",
              "    d'épaisseur, un DXF par couple machine-matériau.",
              "", "cotes_schema:"]
    for rang, lib, valeur, cle, trace in schema:
        lignes += [f"  - rang: {rang}",
                   f"    libelle: \"{lib}\"",
                   f"    cle: {cle}",
                   f"    valeur: {valeur}",
                   f"    trace: {{{', '.join(f'{k}: {v}' for k, v in trace.items())}}}"]
    # ── ce que le navigateur a le droit de faire bouger ───────────────
    # La pièce déclare ses paramètres réglables ET une RÉFÉRENCE : les
    # cotes et un échantillon de contour calculés ici, en Python. Le
    # simulateur se contrôle contre eux au chargement. S'il ne les
    # retrouve pas, il se désactive au lieu de dessiner du faux.
    N_ARC_REF = 48          # non-cote: finesse d'échantillonnage du contour
    reference = profil.contour(an_d, n_arc=N_ARC_REF)
    parametres = [
        dict(nom="H", libelle="taille du robot", unite=" m", valeur=d["H"],
             mini=0.30, maxi=2.00, pas=0.01,   # non-cote: bornes du curseur de simulation
             cible=f"params/anthropometry.yaml  ->  paliers.{a.palier}"),
        dict(nom="r_pied_long", libelle="ratio longueur de pied", unite="",
             valeur=c.anthro["ratios"]["pied_longueur"]["valeur"],
             mini=0.10, maxi=0.22, pas=0.001,   # non-cote: bornes du curseur de simulation
             cible="params/anthropometry.yaml  ->  ratios.pied_longueur.valeur"),
        dict(nom="r_pied_larg", libelle="ratio largeur de pied", unite="",
             valeur=c.anthro["ratios"]["pied_largeur"]["valeur"],
             mini=0.030, maxi=0.090, pas=0.001,   # non-cote: bornes du curseur de simulation
             cible="params/anthropometry.yaml  ->  ratios.pied_largeur.valeur"),
        dict(nom="resserrement", libelle="resserrement à la taille", unite="",
             valeur=a.resserrement, mini=0.40, maxi=0.98, pas=0.01,   # non-cote: bornes du curseur
             cible=f"argument de la pièce  ->  --resserrement"),
        dict(nom="coins", libelle="congé des coins", unite="",
             valeur=a.coins, mini=0.02, maxi=0.49, pas=0.01,   # non-cote: bornes du curseur
             cible="argument de la pièce  ->  --coins"),
        dict(nom="etendue", libelle="étendue du creux", unite="",
             valeur=a.etendue, mini=0.15, maxi=0.90, pas=0.01,   # non-cote: bornes du curseur
             cible="argument de la pièce  ->  --etendue"),
        dict(nom="ep", libelle="épaisseur du matériau", unite=" mm",
             valeur=d["ep"], mini=0.5, maxi=25.0, pas=0.1,   # non-cote: bornes du curseur
             cible=f"params/hardware.yaml  ->  procedes.{a.procede}.epaisseur"),
    ]
    lignes += ["", "simulation:",
               "  tolerance_mm: " + str(profil.TOLERANCE_MM),
               "  parametres:"]
    for pa in parametres:
        lignes.append("    - " + json.dumps(pa, ensure_ascii=False))
    lignes += ["  reference:",
               f"    n_arc: {N_ARC_REF}",
               "    cotes: " + json.dumps(an_d, ensure_ascii=False),
               "    contour: " + json.dumps(
                   [[round(x, 4), round(y, 4)] for x, y in reference])]

    lignes += ["", "cotes:"]
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
