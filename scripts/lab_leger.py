#!/usr/bin/env python3
"""Étude : un YXOR Lab léger, pour apprendre à marcher (profil candidat `lab_leger`, PROPOSÉ ; AUCUNE décision).

    .venv/bin/python scripts/lab_leger.py            # tableau
    .venv/bin/python scripts/lab_leger.py --ecrire   # docs/lab-leger-2026-10.md

Créé le 2026-10-08. Question de Jeremy (2026-10-08, ses mots) : « Est-ce que l'étude et ce que nous avions
déterminé pour YXOR Lab ne représente-t-il pas mieux YXOR Home finalement ? Est-ce qu'il n'existerait pas une
meilleure version de YXOR Lab plus optimisée et compatible avec YXOR Kit ? »

Méthode (prompt du 2026-10-08) : l'explorateur (`explorateur.evaluer`, même règle de choix, marge 1,5) sur le
profil `lab_leger` de params/capacites.yaml, marche à 0,15 puis 0,3 m/s, autonomie 20 min (la plus exigeante des
deux), H de 0,35 à 0,65 m (grille des besoins prolongée vers le bas, DANS CE PROCESSUS seulement) :
  · familles des jambes : Feetech (autorisée au corps pour cette étude), Dynamixel, RobStride limité à ses plus
    petits modèles (RS05, EduLite05) ; petits axes en Feetech (fiche 0075) ;
  · alimentation : servos sur un rail 12 V régulé (pack 3S ; compatibilité et vitesse ramenées à 12 V) ; RobStride
    en 12S coupé à 3,0 V (fiches 0072) ; chaîne compacte ;
  · structure : plaques d'aluminium de 2 mm évidées (structure_plaques, cas « évidée 50 % + 2 mm », pris pour les
    deux cas de l'explorateur) ou CARTON (modèle de scripts/kit.py à la taille du Kit, mis à l'échelle comme
    l'explorateur, loi allométrique).
Énergie de chute = M · g · hauteur du centre de gravité (ANSUR et Winter, `explorateur.cg_ansur`) à la hauteur réelle.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import exigences_physiques as EP  # noqa: E402

HS_ETUDE = [round(0.35 + 0.05 * i, 2) for i in range(7)]          # non-cote: 0,35 à 0,65 m (prompt)
EP.HS = sorted(set(HS_ETUDE) | set(EP.HS))                         # la grille des besoins, prolongée ICI seulement
import explorateur as X  # noqa: E402

DOC = REPO / "docs" / "lab-leger-2026-10.md"
G = 9.80665
FAMILLES = {"feetech": 3, "dynamixel": 3, "robstride": 12}         # non-cote: S du pack (servos : rail 12 V)
ROBSTRIDE_PETITS = ("rs05", "edulite05")
VITESSES = (0.15, 0.3)
MARGES = (1.5, 1.0)          # non-cote: 1,5 = fiche 0051 ; 1,0 = celle des robots qui marchent (contrôle de cohérence,
#                              docs/dimensionnement-par-actionneur.md) : un REPÈRE, pas une proposition


def avec_015():
    """Le niveau 0,15 m/s ajouté à la grille DANS CE PROCESSUS (l'ajouter à params/capacites.yaml change les besoins
    du Lab : tangage de cou 0,81 → 1,05 N·m continu, Lab à 0,85 m infaisable ; constaté le 2026-10-08)."""
    lire0 = EP.lire

    def lire(nom):
        d = lire0(nom)
        if nom == "capacites.yaml":
            n = d["taches"]["marche_sol_plat"]["niveaux"]
            if 0.15 not in n:
                n.insert(0, 0.15)
        return d
    EP.lire = lire


def lire(nom):
    import marche_composants as MC
    return MC.lire(nom)


def cible(v, autonomie=20):
    t = dict(lire("capacites.yaml")["profils"]["lab_leger"]["taches"])
    t["marche_sol_plat"], t["autonomie"] = v, autonomie
    return t


def structure_carton(ctx_alu) -> dict:
    """La structure du modèle de kit.py (carton de référence, à la taille du Kit), au format de l'explorateur."""
    import kit as K
    kc = K.contexte()
    D = max(a["D"] for a in K.feetech(kc, dict(S=0, Vfin=12.0, Vmax=12.0)) if a["D"]) / 1000.0
    segs = K.segments(kc, K.carton_reference(kc), D)
    m = K.masse_structure(segs)
    s = ctx_alu["struct"]
    return dict(par_ensemble={k: m for k in s["par_ensemble"]}, H_S=kc["H"], modele=None,
                tronc={c: segs["tronc"]["masse"] for c in s["tronc"]}, charge=s["charge"])


def structure_alu2() -> dict:
    """Plaques d'alu de 2 mm évidées pour les deux cas de l'explorateur (la variante « pleine 3 mm » écartée)."""
    s = X.structures()
    return dict(s, par_ensemble={(k, c): s["par_ensemble"][(k, "central")] for (k, c) in s["par_ensemble"]},
                tronc={c: s["tronc"]["central"] for c in s["tronc"]})


def contexte(fam, struct, v, marge=None):
    import systeme_electrique as SE
    ctx = X.contexte(struct=struct, cible=cible(v), S=FAMILLES[fam], f_can=250, coupure=3.0, chaine="compacte")
    if marge is not None:
        ctx["marge"] = marge
    if fam == "robstride":
        ctx["act"]["robstride"] = [a for a in ctx["act"]["robstride"] if a["id"] in ROBSTRIDE_PETITS]
    else:                                        # rail 12 V régulé : plage et vitesse ramenées à 12 V
        rail = dict(S=0, Vfin=12.0, Vmax=12.0, coupure=3.0)
        ctx["act"][fam] = [dict(a, compat=SE.compatibilite(a["plage_servo"] or a["plage"], rail),
                                vitesse=a["vitesse"] * SE.facteur_vitesse(a["v_ref"], rail)
                                if a["vitesse"] and SE.facteur_vitesse(a["v_ref"], rail) else None,
                                v_ref_inconnue=SE.facteur_vitesse(a["v_ref"], rail) is None)
                           for a in ctx["act"].get(fam, [])]
    return ctx


def chute(ctx, r) -> float | None:
    W = {k: (x["valeur"] if isinstance(x, dict) else x) for k, x in ctx["an"]["masses"].items()}
    z, _ = X.cg_ansur(ctx["R"], W)
    return r["M"] * G * z * r["H_reel"] if r.get("H_reel") else None


def tient(r) -> bool:
    return r and r["statut"] != "infaisable" and not r.get("non_couvertes")


def explorer_famille(fam, struct, v, marge) -> list[dict]:
    ctx = contexte(fam, struct, v, marge)
    out = []
    for ens in X.ENSEMBLES:
        for H in HS_ETUDE:
            r = X.evaluer(ctx, ens, H, fam, "feetech", ctx["cible"])
            if r:
                out.append(dict(r, ens=ens, H=H, fam=fam, v=v, E_chute=chute(ctx, r) if tient(r) else None,
                                cout_b=X.cout_borne(r) if tient(r) else None,
                                calc=((r.get("elec") or {}).get("calc") or {}).get("id")
                                if isinstance((r.get("elec") or {}).get("calc"), dict) else None))
    return out


def meilleures(sols) -> dict:
    ok = [s for s in sols if tient(s)]
    if not ok:
        return {}
    petite = min(ok, key=lambda s: (s["H"], s["H_reel"], s["cout_b"]))
    moins_chere = min(ok, key=lambda s: (s["cout_b"], s["M"]))
    return dict(petite=petite, moins_chere=moins_chere, n=len(ok))


def part_kit(s) -> tuple[float, float, list[str]]:
    """Coût connu du Kit (option progressive, kit.py) qui resservirait : servos du même modèle (au plus autant que la
    solution en demande), calculateur, adaptateur série si la solution a des Feetech, cellules du même modèle."""
    import kit as K
    e = K.etude("progressive")
    besoin = {}
    for a, c in s["choix"].items():
        n = X.ENSEMBLES[s["ens"]]["axes"].get(a, 1)
        besoin[c["id"]] = besoin.get(c["id"], 0) + n
    calc = (s.get("elec") or {}).get("calc")
    calc_id = calc.get("id") if isinstance(calc, dict) else None
    feetech = any(c["famille"] == "feetech" for c in s["choix"].values())
    gard, tot, quoi, servos = 0.0, 0.0, [], {}
    for nv in e["niveaux"]:
        for x in nv["items"]:
            if x["prix"] is None:
                continue
            tot += x["prix"] * x["n"]
            if x.get("axe"):
                sid = x["nom"].split(" : ")[1]
                k = min(x["n"], besoin.get(sid, 0))
                if k:
                    besoin[sid] -= k
                    gard += x["prix"] * k
                    servos[sid] = servos.get(sid, 0) + k
            elif x.get("id") and x["id"] == calc_id:
                gard += x["prix"] * x["n"]
                quoi.append("calculateur")
            elif "Bus Servo Adapter" in x["nom"] and feetech:
                gard += x["prix"] * x["n"]
                quoi.append("adaptateur série")
    quoi = [f"{k} × {sid}" for sid, k in servos.items()] + quoi
    return gard, tot, quoi


def f1(x, n=1):
    return "—" if x is None else f"{x:,.{n}f}".replace(",", " ").replace(".", ",")


def tout():
    home = home_candidat()                      # AVANT d'ajouter 0,15 m/s à la grille : le Lab tel qu'il est
    avec_015()
    ctx_alu = X.contexte(struct=None, cible=cible(0.3), S=None)
    structs = {"alu 2 mm évidé": structure_alu2(), "carton": structure_carton(ctx_alu)}
    res = {}
    for marge in MARGES:
        for fam in FAMILLES:
            for nom, st in structs.items():
                for v in VITESSES:
                    sols = explorer_famille(fam, st, v, marge)
                    res[(marge, fam, nom, v)] = dict(n=len(sols), best=meilleures(sols), raisons=sorted(
                        {x.split(" : ")[0] for s in sols for x in s.get("violees", [])})[:4])
    return res, home


def home_candidat():
    """Le Lab actuel (fiche 0075 : petits axes Feetech) recalculé sans rien changer : profil lab, 12S, 250 Hz."""
    ctx = X.contexte(profil="lab", S=12, f_can=250, coupure=3.0, chaine="compacte")
    r = X.evaluer(ctx, 27, 0.85, "robstride", "feetech", ctx["cible"])
    return dict(r, E_chute=chute(ctx, r), cout_b=X.cout_borne(r))


REPERES = [  # (nom, hauteur m, masse kg, actionneurs, coût, marche, source) — params/references_simulables.yaml et docs
    ("ToddlerBot 2XC", 0.56, 3.4, "Dynamixel (6 axes par jambe)", None, "oui (politique publiée, rejouée ici)",
     "references_simulables.yaml"),
    ("Zeroth-01", 0.40, 2.0, "STS3250 (5 axes par jambe)", None, "non vue", "docs/dimensionnement-par-actionneur.md "
     "(~0,40 m et ~2 kg, non vérifiés)"),
    ("Berkeley Humanoid Lite", 0.80, 16.0, "actionneurs maison (6 axes par jambe)", None, "oui (politique publiée)",
     "references_simulables.yaml"),
    ("LeRobot Humanoid", None, 19.4, "RobStride RS00, RS02, RS03, RS05 (6 axes par jambe)", "< 5 000 USD (objectif)",
     "oui (politiques publiées)", "references_simulables.yaml"),
]
ABSENTS = ["Open Duck Mini v2", "BRIDGE", "Bumi"]


def lecture(res, home) -> list[str]:
    tiennent = [(m, f, st, x["best"]["petite"]) for (m, f, st, v), x in res.items() if x["best"] and v == 0.3]
    L = []
    for marge in MARGES:
        t = [x for x in tiennent if x[0] == marge]
        L.append(f"- **Marge {f1(marge)}** : " + ("aucune famille ne tient la marche entre "
                                                 f"{f1(HS_ETUDE[0], 2)} et {f1(HS_ETUDE[-1], 2)} m." if not t else
                                                 "tient : " + " ; ".join(
                                                     f"{f} en {st}, dès H = {f1(s['H'], 2)} m ({f1(s['H_reel'], 3)} m "
                                                     f"réels, {f1(s['M'])} kg, ≥ {f1(s['cout_b'], 0)} CHF, "
                                                     f"{f1(s['E_chute'], 0)} J)" for _, f, st, s in t) + "."))
    L.append(f"- **Le Lab actuel** (« Home candidat ») : {f1(home.get('H_reel'), 3)} m, {f1(home.get('M'))} kg, "
             f"≥ {f1(home['cout_b'], 0)} CHF, {f1(home['E_chute'], 0)} J à la chute.")
    return L


def rapport(res, home) -> str:
    L = ["# Un YXOR Lab léger, pour apprendre à marcher (2026-10)", "",
         "**Engendré** par `.venv/bin/python scripts/lab_leger.py --ecrire`. **Étude, AUCUNE décision** : le profil "
         "`lab_leger` (`params/capacites.yaml`) est un CANDIDAT PROPOSÉ ; il ne remplace pas le profil lab.", "",
         "Question de Jeremy (2026-10-08) : « Est-ce que l'étude et ce que nous avions déterminé pour YXOR Lab ne "
         "représente-t-il pas mieux YXOR Home finalement ? Est-ce qu'il n'existerait pas une meilleure version de YXOR "
         "Lab plus optimisée et compatible avec YXOR Kit ? »", "",
         "Profil : marche sur sol plat 0,15 ou 0,3 m/s, relevé sur le dos et sur le ventre, gestes 0,5 m/s, tête à 2 "
         "axes, IA « + vision », autonomie 20 min (la plus exigeante de 10 et 20). Hors profil : saut, poussée, saisie, "
         "sol irrégulier, pente. Méthode : en tête de `scripts/lab_leger.py`.", "",
         "## En bref", ""] + lecture(res, home) + ["",
         "## La plus petite H où la marche tient, par famille", "",
         "« Tient » : faisable ou INCONNU (bornes proposées du système électrique), toutes capacités couvertes. Coût : "
         "borne basse, CHF HT (prix connus seulement). Énergie de chute : M·g·hauteur du centre de gravité. Part du Kit : "
         "coût connu de l'option progressive (`scripts/kit.py`) qui resservirait.", "",
         "| Marge | Jambes | Structure | Marche (m/s) | H → réelle (m) | Masse (kg) | Coût (CHF) | Chute (J) | Statut | "
         "Part du Kit réutilisée | Ce qui resservirait |",
         "| ---: | --- | --- | ---: | --- | ---: | ---: | ---: | --- | ---: | --- |"]
    for (marge, fam, st, v), x in res.items():
        b = x["best"]
        if not b:
            L.append(f"| {f1(marge)} | {fam} | {st} | {f1(v, 2)} | **ne tient à aucune H** de {f1(HS_ETUDE[0], 2)} à "
                     f"{f1(HS_ETUDE[-1], 2)} m (bloquent : {', '.join(x['raisons']) or '—'}) | — | — | — | — | — | — |")
            continue
        s = b["petite"]
        g, t, quoi = part_kit(s)
        L.append(f"| {f1(marge)} | {fam} | {st} | {f1(v, 2)} | {f1(s['H'], 2)} → {f1(s['H_reel'], 3)} | {f1(s['M'])} | "
                 f"{'≥ ' if s['cout'] is None else ''}{f1(s['cout_b'], 0)} | {f1(s['E_chute'], 0)} | {s['statut']} | "
                 f"{f1(100 * g / t if t else None, 0)} % | {', '.join(quoi) or '—'} |")
    L += ["", "## La moins chère par famille (marche 0,3 m/s) : le prix de chaque famille", "",
          "| Marge | Jambes | Structure | H → réelle (m) | Masse (kg) | Coût (CHF) | Chute (J) | Actionneurs des jambes |",
          "| ---: | --- | --- | --- | ---: | ---: | ---: | --- |"]
    for (marge, fam, st, v), x in res.items():
        if v != 0.3 or not x["best"]:
            continue
        s = x["best"]["moins_chere"]
        jam = sorted({c["id"] for a, c in s["choix"].items() if a in X.JAMBES_TOUTES})
        L.append(f"| {f1(marge)} | {fam} | {st} | {f1(s['H'], 2)} → {f1(s['H_reel'], 3)} | {f1(s['M'])} | "
                 f"{'≥ ' if s['cout'] is None else ''}{f1(s['cout_b'], 0)} | {f1(s['E_chute'], 0)} | {', '.join(jam)} |")
    L += ["", "## Le Lab actuel, recalculé comme « Home candidat » (rien n'est changé)", "",
          f"Profil lab, 12S, 250 Hz, chaîne compacte, ensemble 27, H = 0,85 m, petits axes Feetech : **{home['statut']}**, "
          f"{f1(home.get('H_reel'), 3)} m réels, {f1(home.get('M'))} kg, ≥ {f1(home['cout_b'], 0)} CHF, énergie de chute "
          f"{f1(home['E_chute'], 0)} J.", "",
          "## Parmi les repères publiés (au registre ou dans les rapports)", "",
          "| Robot | Hauteur (m) | Masse (kg) | Actionneurs | Coût | Marche démontrée | Source |",
          "| --- | ---: | ---: | --- | --- | --- | --- |"]
    for nom, h, m, act, c, mar, src in REPERES:
        L.append(f"| {nom} | {f1(h, 2)} | {f1(m)} | {act} | {c or '—'} | {mar} | {src} |")
    L += ["", f"**Absents du registre et des rapports** (non placés, aucune recherche dans ce lot court) : "
          f"{', '.join(ABSENTS)}.", ""]
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ecrire", action="store_true")
    a = ap.parse_args(argv)
    res, home = tout()
    txt = rapport(res, home)
    print(txt)
    if a.ecrire:
        DOC.write_text(txt, encoding="utf-8")
        print(f"  -> {DOC.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
