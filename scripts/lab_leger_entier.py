#!/usr/bin/env python3
"""Le Lab léger ENTIER avec la règle de marche « plus_lente » (PROPOSÉE, NON adoptée ; aucune décision).

    .venv/bin/python scripts/lab_leger_entier.py      # tableaux (repris dans docs/lab-leger-2026-10.md)

Créé le 2026-10-09. La règle « plus_lente » (marche_lente.selection) retient, pour une vitesse, la marche simulée la
plus lente au moins aussi rapide ; elle n'est PAS adoptée : elle attend une fiche de décision de Jeremy (elle touche
la fiche 0064). L'explorateur garde « explorateur » par défaut (option --regle-marche).

Profil : lab_leger (relevé, gestes 0,5 m/s, tête à 2 axes, IA « + vision », autonomie 20 min), marche à 0,10, 0,15
et 0,196 m/s (la vitesse de la marche ToddlerBot ramenée à 0,60 m), marges 1,5 et 1,0, H de 0,35 à 0,65 m.
Configurations IMPOSÉES (prompt du 2026-10-09), par axe (`act_axe` de explorateur.evaluer) :
  A. jambes STS3250 (vitesse de sa fiche candidate), tous les autres axes STS3215 (12 V) ; rail 12 V (pack 3S) ;
     structure carton puis alu 2 mm évidé ;
  B. jambes RS05 ou EduLite05 (le plus léger qui passe), autres axes STS3215 ; pack 12S (coupure 3,0 V) ;
     structure alu 2 mm évidé puis carton. Approximation dite : les STS3215 des bras sont comptés par
     l'explorateur comme des axes du corps (canaux CAN surestimés).
« Tient » : règle de lab_leger.tient (une donnée critique d'actionneur manquante donne INCONNU).
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import lab_leger as LL  # noqa: E402  (prolonge la grille des hauteurs, ici seulement)
import explorateur as X  # noqa: E402

VITESSES = (0.10, 0.15, 0.196)        # non-cote: vitesses de marche étudiées (prompt du 2026-10-09)
MARGES = (1.5, 1.0)                   # non-cote: fiche 0051 ; repère des robots qui marchent
JAMBE5 = ("hip_yaw", "hip_roll", "hip_pitch", "knee", "ankle_pitch")
REGLE = "plus_lente"
f1 = LL.f1


def act_axe(ctx, jambes: list[dict]) -> dict:
    """Axe → liste d'actionneurs permise : `jambes` aux cinq axes de jambe, le STS3215 (12 V) partout ailleurs."""
    sts3215 = [a for a in X.catalogue()[0]["feetech"] if a["id"] == "sts3215_c018"]
    tous = {a for e in X.ENSEMBLES.values() for a in e["axes"]}
    return {a: (jambes if a in JAMBE5 else sts3215) for a in tous}


def configs(ctx_alu):
    st = {"carton": LL.structure_carton(ctx_alu), "alu 2 mm évidé": LL.structure_alu2()}
    return [("A", "feetech", "carton", st["carton"]), ("A", "feetech", "alu 2 mm évidé", st["alu 2 mm évidé"]),
            ("B", "robstride", "alu 2 mm évidé", st["alu 2 mm évidé"]), ("B", "robstride", "carton", st["carton"])]


def contexte(fam, struct, v, marge):
    ctx = LL.contexte(fam, struct, v, marge, regle=REGLE)
    jambes = ([a for a in ctx["act"]["feetech"] if a["id"] == "sts3250"] if fam == "feetech"
              else ctx["act"]["robstride"])
    ctx["act_axe"] = act_axe(ctx, jambes)
    return ctx


def marges(ctx, s) -> list[tuple]:
    """Par axe : (axe, actionneur, pointe ÷ requis, continu ÷ requis, vitesse ÷ requise), les plus justes d'abord
    (rapport du couple ÷ marge, ou de la vitesse)."""
    b = X.besoins(ctx["T"], s["H_couples"], s["profil"], s["M_bande"][1])
    out = []
    for a, c in s["choix"].items():
        n = b.get(a)
        if not n:
            continue
        r_pk = c["pointe"] / n["pk"] if n["pk"] > 0 else None
        r_c = c["continu"] / n["c"] if n["c"] > 0 and c["continu"] is not None else None
        r_w = c["vitesse"] / n["w"] if n["w"] > 0 and c["vitesse"] is not None else None
        juste = min(x for x in (r_pk and r_pk / ctx["marge"], r_c and r_c / ctx["marge"], r_w) if x is not None) \
            if any(x is not None for x in (r_pk, r_c, r_w)) else None
        out.append((a, c["id"], r_pk, r_c, r_w, juste))
    return sorted((x for x in out if x[5] is not None), key=lambda x: x[5])


def autonomie(ctx, s) -> float | None:
    """Minutes que le pack CHOISI tient au cycle de marche du profil : énergie du pack × part utilisable × part
    au-dessus de la coupure de 3,0 V (puissance.yaml) ÷ puissance électrique moyenne (même calcul que l'explorateur,
    à l'envers ; le pack est dimensionné pour 20 min au moins)."""
    el = s.get("elec") or {}
    en, bat = el.get("energie") or {}, el.get("batterie") or {}
    hyp = ctx["elec"]["hyp"]
    fc = float(hyp["energie_au_dessus_de_la_coupure"]["3.0"])
    E, p = bat.get("E"), en.get("p_elec_moy")
    return 60.0 * E * hyp["fraction_utilisable"]["valeur"] * fc / p if E and p else None   # E : énergie du PACK (Wh)


def etude() -> dict:
    LL.avec_015()
    ctx_alu = X.contexte(struct=None, cible=LL.cible(0.3), S=None)
    out = {}
    for nom, fam, st_nom, st in configs(ctx_alu):
        for marge in MARGES:
            for v in VITESSES:
                ctx = contexte(fam, st, v, marge)
                ok = []
                for ens in X.ENSEMBLES:
                    for H in LL.HS_ETUDE:
                        r = X.evaluer(ctx, ens, H, fam, "feetech", ctx["cible"])
                        if r and LL.tient(r):
                            ok.append(dict(r, ens=ens, H=H, fc=fam, fp="feetech", profil=ctx["cible"]))
                if not ok:
                    out[(nom, st_nom, marge, v)] = None
                    continue
                s = min(ok, key=lambda s: (s["H"], s["H_reel"], X.cout_borne(s)))
                g, t, quoi = LL.part_kit(s)
                out[(nom, st_nom, marge, v)] = dict(
                    H=s["H"], H_reel=s["H_reel"], M=s["M"], cout=X.cout_borne(s), partiel=s["cout"] is None,
                    chute=LL.chute(ctx, s), autonomie=autonomie(ctx, s), statut=s["statut"], marges=marges(ctx, s)[:2],
                    kit=100 * g / t if t else None, jambes=sorted({c["id"] for a, c in s["choix"].items() if a in JAMBE5}))
    return out


def autres_profils() -> dict:
    """Ce que la règle changerait pour le Lab actuel (Home candidat) et le Kit, sans régénérer leurs documents."""
    import kit as K
    out = {}
    for regle in ("explorateur", REGLE):
        ctx = X.contexte(profil="lab", S=12, f_can=250, coupure=3.0, chaine="compacte", regle_marche=regle)
        sols = []
        for H in (0.65, 0.70, 0.75, 0.80, 0.85):
            r = X.evaluer(ctx, 27, H, "robstride", "feetech", ctx["cible"])
            if r and r["statut"] != "infaisable":
                sols.append((H, r))
        H0, r0 = (sols[0] if sols else (None, None))
        out[("home", regle)] = None if r0 is None else dict(H=H0, H_reel=r0["H_reel"], M=r0["M"],
                                                            cout=X.cout_borne(r0), statut=r0["statut"])
        # le Kit (option progressive) : ses tâches (tête, gestes, debout) n'utilisent pas la marche
        import exigences_physiques as EP
        import simulations_marche as SM
        cap, an, lignes = EP.tout()
        m, rr, _ = SM.charger()
        K._T = X.table_besoins(lignes, m, rr, cap, regle)
        e = K.etude("progressive")
        b = K.bilan(e)[-1]
        out[("kit", regle)] = dict(M=b["M_cumul"], cout=b["P_cumul"],
                                   servos=sorted({r["best"]["id"] for r in e["choix"].values() if r["best"]}))
    K._T = None
    return out


def sections(e: dict, autres: dict) -> list[str]:
    L = ["## Robot entier, règle plus_lente", "",
         "**La règle « plus_lente » n'est PAS adoptée** : elle attend une fiche de décision de Jeremy (elle touche la fiche "
         "0064). L'explorateur garde « explorateur » par défaut (`--regle-marche`, test de non-régression contre le "
         "commit cc340fd). Méthode et configurations imposées : en tête de `scripts/lab_leger_entier.py`.", "",
         "| Config | Structure | Marge | Marche (m/s) | Plus petite H → réelle (m) | Masse (kg) | Coût (CHF) | Chute (J) | "
         "Autonomie (min) | Jambes | Axes les plus justes (pointe ÷ requis, continu ÷ requis, vitesse ÷ requise) | Kit réutilisé |",
         "| --- | --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- | --- | ---: |"]
    for (nom, st, marge, v), x in e.items():
        if x is None:
            L.append(f"| {nom} | {st} | {f1(marge)} | {f1(v, 3)} | **ne tient à aucune H** de {f1(LL.HS_ETUDE[0], 2)} à "
                     f"{f1(LL.HS_ETUDE[-1], 2)} m | — | — | — | — | — | — | — |")
            continue
        mg = "; ".join(f"{a} {i} ({f1(p, 2)}, {f1(c, 2)}, {f1(w, 2)})" for a, i, p, c, w, _ in x["marges"])
        L.append(f"| {nom} | {st} | {f1(marge)} | {f1(v, 3)} | {f1(x['H'], 2)} → {f1(x['H_reel'], 3)} | {f1(x['M'])} | "
                 f"{'≥ ' if x['partiel'] else ''}{f1(x['cout'], 0)} | {f1(x['chute'], 0)} | {f1(x['autonomie'], 0)} | "
                 f"{', '.join(x['jambes'])} | {mg} | {f1(x['kit'], 0)} % |")
    L += ["", "Lecture : « — » en hauteur réelle (configuration B) : les cotes de l'EduLite05 ne sont pas publiées, la place "
          "(taille minimale géométrique) ne se calcule pas ; l'énergie de chute, qui en dépend, non plus. À 0,196 m/s, "
          "la plus petite H est plus grande qu'à 0,15 : sous H ≈ 0,60 m, la marche ToddlerBot mise à l'échelle va moins "
          "vite que 0,196 m/s, et la règle passe alors au G1 (0,55 m/s à 0,60 m), bien plus exigeant. Une hauteur réelle "
          "très supérieure à H (0,45 → 0,826 m) vient de la place : les servos ne tiennent pas dans les proportions ANSUR "
          "d'un robot de 0,45 m, les chaînes s'allongent.", "",
          "### Ce que la règle changerait ailleurs (documents NON régénérés)", "",
          "| Profil | Règle « explorateur » (en vigueur) | Règle « plus_lente » |", "| --- | --- | --- |"]
    for prof, lib in (("home", "Lab actuel, en « Home candidat » (ensemble 27, RobStride + Feetech, 12S, plus petite H)"),
                      ("kit", "Kit, option progressive")):
        cells = []
        for regle in ("explorateur", REGLE):
            x = autres[(prof, regle)]
            if x is None:
                cells.append("aucune H ne tient")
            elif prof == "home":
                cells.append(f"H {f1(x['H'], 2)} → {f1(x['H_reel'], 3)} m, {f1(x['M'])} kg, ≥ {f1(x['cout'], 0)} CHF, {x['statut']}")
            else:
                cells.append(f"{f1(x['M'], 2)} kg, {f1(x['cout'], 0)} CHF, servos {', '.join(x['servos'])}")
        L.append(f"| {lib} | " + " | ".join(cells) + " |")
    L.append("")
    return L


def autres_profils_isoles() -> dict:
    """autres_profils() dans un PROCESSUS À PART : l'étude ajoute des niveaux de marche (0,10 à 0,196 m/s) qui changent
    les besoins du Lab (constaté le 2026-10-08) ; le Lab et le Kit doivent être lus sans eux."""
    import json
    import subprocess
    code = ("import sys, json; sys.path.insert(0, 'scripts'); import lab_leger_entier as E; "
            "print(json.dumps({'|'.join(k): v for k, v in E.autres_profils().items()}))")
    out = subprocess.run([sys.executable, "-c", code], cwd=REPO, capture_output=True, text=True, check=True).stdout
    return {tuple(k.split("|")): v for k, v in json.loads(out.strip().splitlines()[-1]).items()}


def main() -> int:
    autres = autres_profils_isoles()
    print("\n".join(sections(etude(), autres)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
