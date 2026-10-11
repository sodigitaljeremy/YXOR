#!/usr/bin/env python3
"""Cartographie des achats de la gamme par MODULES : réemploi entre modèles et entre catégories (aucune décision).

    .venv/bin/python scripts/cartographie_modules.py            # résumé
    .venv/bin/python scripts/cartographie_modules.py --ecrire   # docs/cartographie-modules-2026-10.md

Créé le 2026-10-11. Décidé (fiche 0077, Jeremy) : « avoir un maximum de réutilisation possible (même entre les
différentes catégories si possible) » ; « acheter une seule batterie utilisable pour tous les modèles de YXOR Kit et
YXOR Lab ». PROPOSÉ : tout le reste (modèles, options préconisées, rattachement des modèles aux catégories).

Modèles, dans l'ordre du parcours :
  · Kit, étapes 1 à 5 : scripts/kit_parcours.py (params/kit_parcours.yaml) ;
  · Lab roulant (PROPOSÉ) : les durables du Kit à l'étape 4, structure en aluminium 2 mm (fiche 0076 : Lab en 2D) ;
  · Lab bipède A : scripts/lab_leger_entier.py, configuration A (jambes STS3250, autres axes STS3215, rail 12 V),
    marche à 0,196 m/s, marge 1,0, plus petite H qui tient (carton ; en aluminium, A ne tient pas : dit) ;
  · Home candidat : le Lab actuel (ensemble 27, RobStride + Feetech, 12S, H = 0,85 m), recalculé sans rien changer.
Catégories (proposition EN ATTENTE de Jeremy, fiche 0077) : Initiation = Kit, Intermédiaire = Lab, Avancé = Home.
Réemploi : un produit (même identifiant) déjà possédé à un modèle précédent n'est pas racheté ; « déjà payé » = son
prix × le nombre déjà possédé (le plus grand nombre possédé jusque-là). Coûts en borne basse (prix connus, CHF HT).
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
DOC = REPO / "docs" / "cartographie-modules-2026-10.md"
MODULES = ("petits axes", "locomotion", "énergie", "cerveau", "IA", "capteurs", "bus", "visserie et connectique",
           "structure")
JAMBE = ("hip_yaw", "hip_roll", "hip_pitch", "knee", "ankle_pitch", "ankle_roll")
CATEGORIE = {"Kit": "Initiation", "Lab": "Intermédiaire", "Home": "Avancé"}   # PROPOSÉ, en attente (fiche 0077)


def lire(nom):
    import marche_composants as MC
    return MC.lire(nom)


def f1(x, n=1):
    if x is None:
        return "—"
    if isinstance(x, str):                       # une valeur publiée sous forme de texte (« 6,86 ou 7 ») : telle quelle
        return x
    return f"{x:,.{n}f}".replace(",", " ").replace(".", ",")


# ─────────────────────────────── classement en modules ──────────────────
def module_kit(i) -> str:
    ref, role = i["ref"], str(i.get("role", ""))
    if ref.startswith("servo:"):
        return "locomotion" if ("roue" in (i.get("axes") or []) or "jambe" in role) else "petits axes"
    if ref.startswith("bride:"):
        return "visserie et connectique"
    if ref.startswith(("cellule:", "batterie:", "dcdc:")) or ref == "bloc_12v" or "BMS" in ref:
        return "énergie"
    if ref.startswith("calc:"):
        return "IA" if "hat" in ref else "cerveau"
    if ref.startswith("capteur:") or "caméra" in ref or "microphone" in ref or "haut-parleur" in ref:
        return "capteurs"
    if ref == "adaptateur_serie" or "manette" in ref:
        return "bus"
    if ref.startswith("structure:"):
        return "structure"
    if "roue" in ref or "roulement" in ref:
        return "locomotion"
    return "visserie et connectique"


def items_kit() -> list[tuple[str, list[dict]]]:
    import kit_parcours as KP
    res, _ = KP.tout()
    out = []
    for r in res:
        if r["n"] == 0:
            continue
        its = []
        for i in r["items"]:
            if r["n"] == 5 and i["ref"].startswith("servo:"):
                # étape 5 : les servos des jambes et des bras, séparés (kit.py, axes du robot debout)
                import kit as K
                e = K.etude("progressive")
                sid = i["ref"].split(":")[1]
                n_j = sum(2 if ax in K.COTES else 1 for ax, c in e["choix"].items()
                          if c["best"] and c["best"]["id"] == sid and ax in JAMBE + ("waist_yaw",))
                if n_j:
                    its.append(dict(i, n=n_j, module="locomotion", produit=sid))
                if i["n"] - n_j > 0:
                    its.append(dict(i, n=i["n"] - n_j, module="petits axes", produit=sid))
                continue
            its.append(dict(i, module=module_kit(i), produit=i.get("nom")))
        out.append((f"Kit {r['n']} ({r['nom']})", its))
    return out


def items_solution(r, ens) -> list[dict]:
    """Une solution de l'explorateur, en modules : servos du choix (axes de l'ensemble), système électrique."""
    import explorateur as X
    out = []
    for a, c in r["choix"].items():
        n = X.ENSEMBLES[ens]["axes"].get(a, 1)
        out.append(dict(nom=c["id"], produit=c["id"], n=n, prix=c["prix"], classe="DURABLE",
                        module="locomotion" if a in JAMBE else "petits axes"))
    el = r.get("elec") or {}
    c = el.get("calc") or {}
    if c:
        out.append(dict(nom=c["nom"], produit=c["id"], n=1, prix=c.get("prix"), classe="DURABLE",
                        module="cerveau" + (" + IA" if c.get("type") == "jetson" else "")))
    b = el.get("batterie") or {}
    if b:
        out.append(dict(nom=f"{b['nom']} (pack {b['S']}S{b['P']}P)", produit=b["id"], n=b["S"] * b["P"],
                        prix=(b["prix"] / (b["S"] * b["P"])) if b.get("prix") else None, classe="DURABLE", module="énergie"))
    for m, x in (el.get("chaine") or []):
        bb = (x or {}).get("best") if isinstance(x, dict) else None
        if bb:
            out.append(dict(nom=bb["nom"], produit=bb["id"], n=1, prix=bb.get("prix"), classe="DURABLE", module="énergie"))
    for v, x in (el.get("rails") or {}).items():
        bb = (x or {}).get("best") if isinstance(x, dict) else None
        if bb:
            out.append(dict(nom=bb["nom"], produit=bb["id"], n=1, prix=bb.get("prix"), classe="DURABLE", module="énergie"))
    bus = el.get("bus") or {}
    for k in ("can", "serie"):
        x = bus.get(k)
        if isinstance(x, dict) and x.get("id"):
            out.append(dict(nom=x["nom"], produit=x["id"], n=x.get("unites", 1), prix=x.get("prix"), classe="DURABLE",
                            module="bus"))
    out.append(dict(nom="caméra (non comptée par l'explorateur)", produit=None, n=1, prix=None, classe="DURABLE",
                    module="capteurs"))
    out.append(dict(nom="visserie, connectique", produit=None, n=1, prix=None, classe="DURABLE",
                    module="visserie et connectique"))
    return out


def lab_bipede_a():
    import lab_leger_entier as LE
    import lab_leger as LL
    import explorateur as X
    LL.avec_015()
    ctx_alu = X.contexte(struct=None, cible=LL.cible(0.3), S=None)
    _, fam, st_nom, st = next(c for c in LE.configs(ctx_alu) if c[0] == "A" and c[2] == "carton")
    ctx = LE.contexte(fam, st, 0.196, 1.0)
    for H in LL.HS_ETUDE:
        for ens in X.ENSEMBLES:
            r = X.evaluer(ctx, ens, H, fam, "feetech", ctx["cible"])
            if r and LL.tient(r):
                return ctx, dict(r, ens=ens, H=H, fc=fam, fp="feetech", profil=ctx["cible"]), ens
    return ctx, None, None


def home_candidat(S=12):
    import explorateur as X
    ctx = X.contexte(profil="lab", S=S, f_can=250, coupure=3.0, chaine="compacte")
    return ctx, X.evaluer(ctx, 27, 0.85, "robstride", "feetech", ctx["cible"])


def modeles() -> list[dict]:
    out = []
    for nom, its in items_kit():
        out.append(dict(nom=nom, gamme="Kit", items=its))
    k4 = next(its for nom, its in items_kit() if nom.startswith("Kit 4"))
    out.append(dict(nom="Lab roulant (PROPOSÉ)", gamme="Lab",
                    items=[dict(i) for i in k4 if i["module"] != "structure"]
                    + [dict(nom="plaques d'aluminium 2 mm (prix de l'opérateur CN non relevé)", produit="alu2",
                            n=1, prix=None, classe="STRUCTURE", module="structure")]))
    # le Home et le Lab bipède A, chacun dans un PROCESSUS À PART (lab_leger ajoute des niveaux de marche qui
    # changent les besoins du Lab, constaté le 2026-10-08)
    out.append(dict(nom="Lab bipède A", gamme="Lab", items=_isole("lab_a")))
    out.append(dict(nom="Home candidat", gamme="Home", items=_isole("home")))
    return out


def _isole(quoi):
    import json
    import subprocess
    code = ("import sys, json; sys.path.insert(0, 'scripts'); import cartographie_modules as C; "
            f"print(json.dumps(C._items('{quoi}'), default=str))")
    out = subprocess.run([sys.executable, "-c", code], cwd=REPO, capture_output=True, text=True, check=True).stdout
    return json.loads(out.strip().splitlines()[-1])


def _items(quoi):
    if quoi == "home":
        _, r = home_candidat()
        return items_solution(r, 27) + [dict(nom="plaques d'aluminium (Home : 3D, fiche 0076)", produit="alu_home", n=1,
                                              prix=None, classe="STRUCTURE", module="structure")]
    _, r, ens = lab_bipede_a()
    return items_solution(r, ens) + [dict(nom="carton (A ne tient qu'en carton ; en aluminium 2 mm, non)", produit="carton",
                                          n=1, prix=0.0, classe="STRUCTURE", module="structure")]


def parcourir(ms) -> list[dict]:
    """Coût des durables, déjà payé par un modèle précédent, réemploi entre catégories, investissement cumulé."""
    possede, cat_de = {}, {}
    invest = 0.0
    out = []
    for m in ms:
        dur = [i for i in m["items"] if i["classe"] == "DURABLE"]
        tot = sum((i["prix"] or 0.0) * i["n"] for i in dur)
        deja, entre_cat = 0.0, 0.0
        cat = CATEGORIE[m["gamme"]]
        for i in dur:
            k = i.get("produit")
            if not k:
                continue
            reu = min(i["n"], possede.get(k, 0))
            deja += (i["prix"] or 0.0) * reu
            if reu and cat_de.get(k) and cat_de[k] != cat:
                entre_cat += (i["prix"] or 0.0) * reu
        neuf = tot - deja
        invest += neuf
        par_module = {mo: sum((i["prix"] or 0.0) * i["n"] for i in dur if i["module"].startswith(mo)) for mo in MODULES}
        out.append(dict(m, total=tot, deja=deja, neuf=neuf, entre_cat=entre_cat, invest=invest, cat=cat,
                        par_module=par_module, inconnus=sum(1 for i in dur if i["prix"] is None)))
        for i in dur:
            k = i.get("produit")
            if k:
                if possede.get(k, 0) < i["n"]:
                    cat_de.setdefault(k, cat)
                possede[k] = max(possede.get(k, 0), i["n"])
    return out


def options(m) -> dict:
    """L'option préconisée de chaque module (le plus cher d'abord), pour la matrice."""
    out = {}
    for mo in MODULES:
        its = [i for i in m["items"] if i["module"].startswith(mo)]
        if its:
            out[mo] = ", ".join(sorted({f"{i['n']} × {i['nom']}" if i["n"] > 1 else str(i["nom"]) for i in its}))[:120]
    return out


# ─────────────────────────────── énergie : la batterie unique ───────────
def options_energie() -> list[dict]:
    """Les options du module énergie (params/energie_marche.yaml, versé le 2026-10-11) + les packs 21700 de la cellule
    du Lab (batteries.yaml) : masse, Wh, courant, coût, Suisse, outillage, sécurité."""
    import systeme_electrique as SE
    p = REPO / "params" / "energie_marche.yaml"
    em = lire("energie_marche.yaml") if p.exists() else {}
    out = []
    for b in em.get("batteries_outillage") or []:
        out.append(dict(famille="a) outillage 18 V", nom=b.get("nom"), Wh=b.get("energie_Wh"), masse_g=b.get("masse_g"),
                        I=b.get("courant_max_A"), prix=b.get("prix_chf"), ch=b.get("dispo_ch"),
                        outillage="tournevis ; adaptateur à bornes, convertisseur 12 V, coupure basse",
                        securite=b.get("securite")))
    cel = next(c for c in SE.cellules_21700() if c["id"] == lire("kit.yaml")["lab"]["cellule"])
    hyp = lire("puissance.yaml")["hypotheses"]
    bms = {}
    for b in (em.get("releve") or {}).get("packs_21700") or []:      # la carte de protection limite le courant
        import re
        v = re.findall(r"\d+(?:\.\d+)?", str(b.get("surintensite_a") or ""))
        if b.get("type") == "bms" and b.get("series") and v:
            bas = float(v[0]) - (float(v[1]) if len(v) > 1 else 0.0)     # « 26 ± 2 » → 24 A (prudent)
            bms[b["series"]] = min(bms.get(b["series"], 1e9), bas)
    for S in (3, 4):
        I = min(cel["I"], bms[S]) if S in bms else cel["I"]
        out.append(dict(famille=f"b) pack maison {S}S1P", nom=f"{S}S1P {cel['nom']}", Wh=S * cel["E"],
                        masse_g=1000 * S * cel["m"] * hyp["facteur_pack_masse"]["valeur"], I=I,
                        prix=S * cel["prix"] if cel["prix"] else None, ch=cel.get("dispo"),
                        outillage="soudure par points ou porte-cellules ; BMS ; chargeur 3S/4S (HORS de l'outillage "
                                  "du Kit si soudé)", securite="BMS obligatoire ; cellules neuves seulement"))
    for u in em.get("usb_c") or []:
        out.append(dict(famille="c) USB-C (bureau)", nom=u.get("nom"), Wh=None, masse_g=u.get("masse_g"),
                        I=u.get("courant_12v_A"), prix=u.get("prix_chf"), ch=u.get("dispo_ch"), outillage="aucun",
                        securite="secteur ; aucune batterie"))
    return out


def recheck_lab_a(masses_g: list[float]) -> list[dict]:
    """Le Lab bipède A (choix d'actionneurs FIXÉ) repassé avec une autre batterie : masse M' = M − pack choisi +
    batterie ; chaque axe revérifié (explorateur.passe) aux marges 1,5 et 1,0. Dans CE processus (lab_leger)."""
    import explorateur as X
    ctx, r, ens = lab_bipede_a()
    m_pack = (r["elec"].get("batterie") or {}).get("masse") or 0.0
    en = r["elec"].get("energie") or {}
    pointe_A = en.get("P_pointe") / ctx["elec"]["var"]["Vfin"] if en.get("P_pointe") else None
    out = []
    for mg in masses_g:
        M2 = r["M_bande"][1] - m_pack + mg / 1000.0
        b = X.besoins(ctx["T"], r["H_couples"], r["profil"], M2)
        res = {}
        for marge in (1.5, 1.0):
            ko = [a for a, c in r["choix"].items() if a in b and not X.passe(c, b[a], marge)]
            res[marge] = ko
        out.append(dict(masse_g=mg, M=M2, ko=res))
    return out, m_pack, r["M_bande"][1], pointe_A


def _recheck_isole(masses):
    import json
    import subprocess
    code = ("import sys, json; sys.path.insert(0, 'scripts'); import cartographie_modules as C; "
            f"o, mp, M, I = C.recheck_lab_a({list(masses)}); print(json.dumps(dict(o=o, mp=mp, M=M, I=I), default=str))")
    out = subprocess.run([sys.executable, "-c", code], cwd=REPO, capture_output=True, text=True, check=True).stdout
    return json.loads(out.strip().splitlines()[-1])


# ─────────────────────────────── hypothèses entre catégories ───────────
def home_36v() -> dict:
    """Le Home candidat (ensemble 27, RobStride + Feetech) en 10S (deux 18 V en série, 36 V nominal, coupure 30 V)
    contre 12S (fiche 0072) : plus petite H qui ne soit pas infaisable, et facteur de vitesse des RobStride."""
    import explorateur as X
    import systeme_electrique as SE
    out = {}
    for S in (12, 10):
        ctx = X.contexte(profil="lab", S=S, f_can=250, coupure=3.0, chaine="compacte")
        var = SE.variante(S, coupure=3.0)
        res = None
        viol = []
        for H in (0.65, 0.70, 0.75, 0.80, 0.85, 0.90):
            r = X.evaluer(ctx, 27, H, "robstride", "feetech", ctx["cible"])
            if r["statut"] != "infaisable":
                res = dict(H=H, M=r["M"], cout=X.cout_borne(r), statut=r["statut"], H_reel=r["H_reel"])
                break
            viol.append(r["violees"][0].split(" (")[0])
        out[S] = dict(var=var, facteur=var["Vfin"] / 48.0, res=res, viol=viol)
    return out


def _home_36v_isole():
    import json
    import subprocess
    code = ("import sys, json; sys.path.insert(0, 'scripts'); import cartographie_modules as C; "
            "print(json.dumps({str(k): v for k, v in C.home_36v().items()}, default=str))")
    out = subprocess.run([sys.executable, "-c", code], cwd=REPO, capture_output=True, text=True, check=True).stdout
    return json.loads(out.strip().splitlines()[-1])


def pi5_dans_home() -> dict:
    import marche_composants as MC
    taux = lire("budget.yaml")["taux_de_change"]
    c = lire("calculateurs.yaml")["marche"]["produits"]
    b = lire("bus.yaml")["marche"]["produits"]
    return dict(pi5=MC.chf(c["rpi5_8gb"].get("prix"), taux), hat_can=MC.chf(b["ws_2ch_can_fd_hat"].get("prix"), taux),
                hat_can_nom=b["ws_2ch_can_fd_hat"].get("nom"))


def ia_comparaison() -> list[dict]:
    """Débits publiés (kit_parcours_marche.yaml : Pi 5 ; energie_marche.yaml : réseau et Jetson) et coût sur le robot."""
    import marche_composants as MC
    taux = lire("budget.yaml")["taux_de_change"]
    c = lire("calculateurs.yaml")["marche"]["produits"]
    pm = (lire("kit_parcours_marche.yaml").get("ia_locale") or [{}])[0].get("mesures") or []
    p = REPO / "params" / "energie_marche.yaml"
    ir = (lire("energie_marche.yaml").get("ia_reseau") or []) if p.exists() else []
    lignes = []
    for x in pm + ir:
        if x.get("source") == "raspberry.tips":           # contredit par les mesures (relevé du 2026-10-11) : écarté
            continue
        if x.get("tache", "LLM") == "LLM" and x.get("debit_tok_s"):
            lignes.append(dict(modele=x.get("modele"), materiel=x.get("materiel"), debit=x.get("debit_tok_s"),
                               premier=x.get("premier_jeton_ms"), source=x.get("source")))
    couts = dict(reseau=0.0, pi5=MC.chf(c["rpi5_8gb"].get("prix"), taux),
                 pi5_hat2=(MC.chf(c["rpi5_8gb"].get("prix"), taux) or 0) + (MC.chf(c["rpi_ai_hat_plus_2"].get("prix"), taux) or 0),
                 jetson=MC.chf(c["jetson_orin_nano_super_devkit"].get("prix"), taux))
    return lignes, couts


# ─────────────────────────────── rapport ────────────────────────────────
def rapport(par, energie, recheck, h36, pi5, ia) -> str:
    L = ["# Cartographie des achats de la gamme par modules (2026-10)", "",
         "**Engendré** par `.venv/bin/python scripts/cartographie_modules.py --ecrire`. Décidé (fiche 0077, Jeremy) : "
         "réemploi maximal, même entre catégories ; une seule batterie pour tous les modèles du Kit et du Lab. "
         "**Tout le reste est PROPOSÉ**, dont le rattachement des modèles aux catégories (« Initiation = Kit, "
         "Intermédiaire = Lab, Avancé = Home et Pro » : en attente de Jeremy). Méthode : en tête du script.", "",
         "## Matrice des modules par modèle (option préconisée)", "",
         "| Modèle | Catégorie | " + " | ".join(MODULES) + " |", "| --- | --- | " + " | ".join("---" for _ in MODULES) + " |"]
    for p in par:
        o = options(p)
        L.append(f"| {p['nom']} | {p['cat']} | " + " | ".join(o.get(m, "—") for m in MODULES) + " |")
    # contrôle de l'objectif « une seule batterie » (fiche 0077) et du réemploi du cerveau
    def prod(p, mo):
        return {i.get("produit") for i in p["items"] if i["module"].startswith(mo) and i.get("produit")}
    kit_l = [p for p in par if p["gamme"] in ("Kit", "Lab")]
    cel = {p["nom"]: {x for x in prod(p, "énergie") if "21700" in str(x) or str(x).startswith(("molicel", "samsung", "lg_"))}
           for p in kit_l}
    cel = {k: v for k, v in cel.items() if v}
    cerveaux = {p["nom"]: prod(p, "cerveau") for p in par if prod(p, "cerveau")}
    L += ["", "**Écarts à l'objectif de réemploi (calculés)** :",
          "- cellules des modèles du Kit et du Lab : " + " ; ".join(f"{k} : {', '.join(sorted(v))}" for k, v in cel.items())
          + (" → **une seule cellule**, conforme à « une seule batterie »." if len(set().union(*cel.values())) <= 1 else
             " → **plusieurs cellules** : l'explorateur choisit pour le Lab bipède A la cellule la plus légère qui suffit, "
             "pas celle du Kit ; la batterie unique demande d'imposer la même (le Lab A tient avec le pack 3S1P du Kit, "
             "tableau plus bas, à la marge 1,0)."),
          "- calculateur : " + " ; ".join(f"{k} : {', '.join(sorted(v))}" for k, v in cerveaux.items())
          + " → le Lab bipède A et le Home prennent un Jetson (choix de l'explorateur : le moins cher qui est "
            "vérifiable) ; le Pi 5 du Kit n'y est pas réemployé, sauf comme contrôleur du corps (hypothèse plus bas).", "",
          "## Coûts et réemploi, en parcourant Kit → Lab → Home", "",
          "| Modèle | Durables (CHF HT, borne basse) | Déjà payé par un modèle précédent | Réemploi | Entre catégories | "
          "Achat neuf | Investissement cumulé | Durables sans prix |", "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for p in par:
        L.append(f"| {p['nom']} | {f1(p['total'], 0)} | {f1(p['deja'], 0)} | "
                 f"{f1(100 * p['deja'] / p['total'] if p['total'] else None, 0)} % | {f1(p['entre_cat'], 0)} | "
                 f"{f1(p['neuf'], 0)} | {f1(p['invest'], 0)} | {p['inconnus']} |")
    L += ["", "« Entre catégories » : la part déjà payée dont le produit a été acheté dans une AUTRE catégorie "
          "(proposition de catégories en attente). Le Lab bipède A ne tient qu'en carton à la marge 1,0 (lab-leger) : "
          "la nomenclature est la sienne.", "",
          "## Module énergie : la batterie unique du Kit et du Lab (sous 100 Wh)", "",
          "| Option | Produit | Énergie (Wh) | Masse (g) | Courant max (A) | Coût (CHF) | Suisse | Outillage | Sécurité |",
          "| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |"]
    for e in energie:
        L.append(f"| {e['famille']} | {e['nom']} | {f1(e['Wh'], 0)} | {f1(e['masse_g'], 0)} | {f1(e['I'], 0)} | "
                 f"{f1(e['prix'], 0)} | {str(e['ch'] or '—')[:60]} | {e['outillage']} | {str(e['securite'] or '—')[:90]} |")
    em = lire("energie_marche.yaml").get("releve") or {}
    conv = [c for c in em.get("convertisseurs_12v") or [] if (c.get("courant_a") or 0) >= 25]
    L += ["", f"Repères de courant : **23,7 A** au pire à l'étape 3 du Kit (8 servos au blocage + Pi 5) ; pointe du Lab bipède A "
          f"**{f1(recheck['I'])} A** (puissance de pointe de l'explorateur ÷ tension de coupure du pack 3S).", "",
          "- **Courant des batteries d'outillage** : publié par aucune des huit (null) ; il ne peut donc être comparé ni aux "
          "23,7 A ni à la pointe du Lab.",
          "- **Où est la protection de décharge** : " + " ; ".join(
              f"{p['marque']} : coupure dans {p.get('coupure_dans') or 'non lu'}, surintensité dans "
              f"{p.get('surintensite_dans') or 'non lu'}" for p in em.get("protection") or [])
          + ". Une protection dans l'OUTIL laisse la batterie sans coupure une fois branchée au robot : il faut alors une "
            "coupure en tension basse côté robot.",
          "- **Adaptateurs bornes vers fils** : " + "; ".join(f"{a['nom']} ({f1(a.get('courant_max_a'))} A)" for a in
                                                            em.get("adaptateurs") or [] if a.get("courant_max_a")) + ".",
          "- **Convertisseurs 12 V de 25 A ou plus** : " + ("; ".join(
              f"{c['marque']} {c['modele']} ({c['entree_v']} V → 12 V, {c['courant_a']} A, {f1(c.get('prix_chf'), 0)} CHF, "
              f"14-21 V : {'oui' if c.get('couvre_14_21v') else 'non'})" for c in conv) or "aucun lu")
          + ". **Aucun ne couvre 14 à 21 V en entrée** (une batterie 18 V) : pour la batterie d'outillage, le convertisseur "
            "de 25 A reste null.",
          "- **USB-C** : à 12 V, un chargeur de 140 W ne donne que 3 A (Club 3D CAC-1914) et un chargeur de 100 W lu n'a "
          "pas de niveau 12 V : en dessous du pire cas de la tête de bureau (5,4 A, servos au blocage) ; suffisant "
          "seulement si le courant réel reste sous 3 A (à mesurer) ; pas pour le buste (23,7 A).", "",
          f"### Le Lab bipède A, repassé avec chaque batterie (pack choisi par l'explorateur : {f1(recheck['mp'] * 1000, 0)} g, "
          f"robot {f1(recheck['M'], 2)} kg)", "",
          "Masse de la batterie seule : l'adaptateur, le convertisseur 12 V et la coupure basse d'une batterie "
          "d'outillage ne sont pas comptés (masses non relevées).", "",
          "| Batterie | Masse (g) | Robot (kg) | Marge 1,5 | Marge 1,0 |", "| --- | ---: | ---: | --- | --- |"]
    for nom, x in zip(recheck.get("noms") or [""] * len(recheck["o"]), recheck["o"]):
        cel = lambda ko: "tient" if not ko else "ne tient pas (" + ", ".join(ko) + ")"
        L.append(f"| {nom} | {f1(x['masse_g'], 0)} | {f1(x['M'], 2)} | {cel(x['ko']['1.5'])} | {cel(x['ko']['1.0'])} |")
    L += ["", "## Hypothèses entre catégories (chiffrées, NON adoptées)", "",
          "### Le Home en 36 V (deux batteries 18 V en série) plutôt qu'en 12S", ""]
    for S, x in h36.items():
        r = x["res"]
        L.append(f"- **{S}S** : coupure {f1(x['var']['Vfin'], 0)} V, vitesse des RobStride × {f1(x['facteur'], 3)} de leur "
                 "vitesse à 48 V ; " + (f"plus petite H qui ne soit pas infaisable : {f1(r['H'], 2)} m ({f1(r['H_reel'], 3)} m "
                                        f"réels), {f1(r['M'])} kg, ≥ {f1(r['cout'], 0)} CHF, {r['statut']}" if r else
                                        "**aucune H de 0,65 à 0,90 m ne tient** (" + "; ".join(sorted(set(x["viol"]))) + ")") + ".")
    L += ["", "Ce que cela changerait par rapport à la fiche 0072 (12S décidé par Jeremy pour le Lab et le Pro) : le pack, "
          "le BMS, la coupure et la plage des RobStride (24 à 60 V, tenue en 10S) ; la vitesse à la coupure baisse de "
          "17 % ; à H = 0,85 m le genou ne la tient plus.", "",
          "### Le Raspberry Pi 5 gardé dans le Home (contrôleur du corps), à côté d'un Jetson pour l'IA", "",
          f"Coût ajouté : Raspberry Pi 5 8 GB {f1(pi5['pi5'], 0)} CHF (déjà payé si il vient du Kit) + {pi5['hat_can_nom']} "
          f"{f1(pi5['hat_can'], 0)} CHF pour le CAN. Masse et consommation du Pi 5 : non publiées (calculateurs.yaml). "
          "Le Jetson garde l'IA ; le Pi 5 porte la boucle des actionneurs (non calculé ici).", "",
          "### L'IA par le réseau, sur l'ordinateur de l'utilisateur", "",
          "| Modèle | Matériel | Débit (jetons/s) | Premier jeton (ms) | Source |", "| --- | --- | ---: | ---: | --- |"]
    lignes, couts = ia
    for x in lignes:
        L.append(f"| {x['modele']} | {x['materiel']} | {f1(x['debit'], 2)} | {f1(x['premier'], 0)} | {x['source']} |")
    L += ["", f"Coût sur le robot : réseau 0 CHF (l'ordinateur existe) ; Pi 5 seul {f1(couts['pi5'], 0)} CHF ; Pi 5 + AI HAT+ 2 "
          f"{f1(couts['pi5_hat2'], 0)} CHF ; Jetson Orin Nano Super (kit) {f1(couts['jetson'], 0)} CHF. Le délai par le réseau "
          "ajoute l'aller-retour Wi-Fi : médiane d'environ 3 ms, 90e centile d'environ 20 ms, mesurés sur un réseau de "
          "campus (WiFiSeer, 2016, energie_marche.yaml) ; aucune mesure en réseau domestique relevée. Sur un ordinateur "
          "avec une carte graphique grand public, un modèle de 8 milliards de paramètres répond 3 à 10 fois plus vite "
          "que sur le Pi 5 (un modèle 2 à 5 fois plus petit) ; un Mac M1 à M3 de 8 à 16 GB attend 8 à 10 s avant le "
          "premier jeton sur ce modèle de 8 milliards (LocalScore).", ""]
    return "\n".join(L) + "\n"


def tout():
    par = parcourir(modeles())
    energie = options_energie()
    bat = [e for e in energie if e["masse_g"] and not e["famille"].startswith("c)")]          # des batteries seulement
    recheck = _recheck_isole([e["masse_g"] for e in bat])
    recheck["noms"] = [e["nom"] for e in bat]
    return par, energie, recheck, _home_36v_isole(), pi5_dans_home(), ia_comparaison()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ecrire", action="store_true")
    a = ap.parse_args(argv)
    t = tout()
    for p in t[0]:
        print(f"  {p['nom']} : {p['total']:.0f} CHF, déjà payé {p['deja']:.0f}, neuf {p['neuf']:.0f}, cumul {p['invest']:.0f}")
    if a.ecrire:
        DOC.write_text(rapport(*t), encoding="utf-8")
        print(f"  -> {DOC.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
