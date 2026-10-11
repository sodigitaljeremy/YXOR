#!/usr/bin/env python3
"""Parcours guidé du Kit (PROPOSÉ, non décidé) : nomenclature, coût, réemploi, alimentation, couples, outillage.

    .venv/bin/python scripts/kit_parcours.py            # résumé
    .venv/bin/python scripts/kit_parcours.py --ecrire   # docs/kit-parcours-2026-10.md

Créé le 2026-10-11. Décidé (fiche 0076, mots de Jeremy) : le Kit en parcours guidé, étape par étape ; le réemploi
(« monter et démonter chaque composant et les remonter dans n'importe quelles variantes des modèles YXOR Kit et YXOR
Lab ») ; préconiser sans imposer ; l'outillage du Kit. PROPOSÉ : les étapes (params/kit_parcours.yaml).

Règles de calcul :
  · coût en BORNE BASSE (CHF HT) : la somme des prix CONNUS ; un composant sans prix relevé compte pour 0 et il est
    COMPTÉ comme inconnu ; structure en carton de récupération : 0 CHF ;
  · réemploi depuis les étapes précédentes : pour chaque durable, les exemplaires déjà achetés à une étape
    antérieure (le plus grand nombre possédé jusque-là) ; part = leur coût ÷ le coût des durables de l'étape ;
  · réemployable dans le Lab (PROPOSÉ) : jusqu'à `lab_feetech_max` servos Feetech (petits axes du Lab, fiche 0075),
    l'adaptateur série (Feetech), les cellules de la cellule du Lab ; le reste « à vérifier » ou « non » ;
  · couples : statique (kit.py : tête basculée, bras tendu, debout), besoin ÷ couple CONTINU publié du servo ;
    roue : INCONNU (rayon de roue et résistance au roulement absents du dépôt) ;
  · alimentation : bloc 12 V dimensionné au pire cas (servos au blocage + calculateur, kit.bloc_secteur) ; batterie
    vérifiée sous 100 Wh (limite postale suisse, docs/catalogue-composants-yxor.md : à vérifier).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
DOC = REPO / "docs" / "kit-parcours-2026-10.md"
LIMITE_WH = 100.0                    # non-cote: batterie de moins de 100 Wh (prompt du 2026-10-11)
P_RPI_W = 25.0                       # non-cote: alimentation 5 V 5 A du Raspberry Pi 5 (calculateurs.yaml, note « capacité de la source »)


def lire(nom):
    import marche_composants as MC
    return MC.lire(nom)


def f1(x, n=1):
    return "—" if x is None else f"{x:,.{n}f}".replace(",", " ").replace(".", ",")


def marche_parcours() -> dict:
    p = REPO / "params" / "kit_parcours_marche.yaml"
    return lire("kit_parcours_marche.yaml") if p.exists() else {}


# ─────────────────────────────── nomenclature ───────────────────────────
def resoudre(ref: str, ctx: dict) -> dict:
    """{nom, prix (CHF HT ou None), masse (kg ou None), source} d'une référence de params/."""
    import marche_composants as MC
    import systeme_electrique as SE
    import explorateur as X
    taux = lire("budget.yaml")["taux_de_change"]
    genre, _, cle = ref.partition(":")
    if genre == "servo":
        a = next(a for a in X.catalogue()[0]["feetech"] if a["id"] == cle)
        return dict(nom=cle, prix=a["prix"], masse=a["masse"], source="actionneurs.yaml")
    if genre == "calc":
        p = lire("calculateurs.yaml")["marche"]["produits"][cle]
        m = MC.num(MC.v(p, "masse_ensemble"))
        return dict(nom=p.get("nom", cle), prix=MC.chf(p.get("prix"), taux), masse=m / 1000 if m else None,
                    source="calculateurs.yaml")
    if genre == "capteur":
        p = next(p for p in lire("capteurs.yaml")["produits"] if p["nom"] == cle)
        pr = p.get("prix") or {}
        return dict(nom=cle, prix=MC.chf(dict(valeur=pr.get("valeur"), devise=pr.get("devise"),
                                              tva_incluse=pr.get("tva_incluse")), taux) if pr.get("valeur") else None,
                    masse=(p.get("masse_g") or 0) / 1000 or None, source=f"capteurs.yaml ({pr.get('vendeur')})")
    if genre == "cellule":
        cid = lire("kit.yaml")["lab"]["cellule"] if cle == "lab" else cle
        c = next(c for c in SE.cellules_21700() if c["id"] == cid)
        return dict(nom=c["nom"], prix=c["prix"], masse=c["m"], source="batteries.yaml (cellule du Lab)", E=c["E"])
    if genre == "batterie":
        p = lire("batteries.yaml")["marche"]["produits"][cle]
        return dict(nom=p.get("nom", cle), prix=MC.chf(p.get("prix"), taux),
                    masse=(MC.num(MC.v(p, "masse_g")) or 0) / 1000 or None, source="batteries.yaml",
                    E=MC.num(MC.v(p, "energie_Wh")))
    if ref == "adaptateur_serie":
        a = SE.adaptateur_serie()
        return dict(nom=a["nom"], prix=a["prix"], masse=a["masse"] / 1000, source="bus.yaml")
    if genre == "dcdc":
        r = SE.composant(SE.composants(lire("puissance.yaml")), "dcdc", Vout=float(cle), Vin=(9.0, 12.6),
                         ordre=("volume", "masse", "prix"))
        b = r["best"]
        return dict(nom=b["nom"] if b else f"convertisseur {cle} V (aucun au marché)", prix=b and b["prix"],
                    masse=b["masse"] / 1000 if b and b["masse"] else None, source="puissance.yaml")
    if ref == "bloc_12v":
        return dict(nom="bloc secteur 12 V (dimensionné à l'étape)", prix=None, masse=None, source="kit_marche.yaml",
                    bloc=True)
    if genre in ("bride", "projet"):
        mp = marche_parcours()
        liste = mp.get("brides" if genre == "bride" else "projets") or []
        x = next((b for b in liste if b.get("cle") == cle), None)
        if not x:
            return dict(nom=f"{genre} {cle} (non relevé)", prix=None, masse=None, source="—")
        return dict(nom=x.get("nom", cle), prix=x.get("prix_chf"), masse=(x.get("masse_g") or 0) / 1000 or None,
                    source="kit_parcours_marche.yaml")
    if genre == "structure":
        return dict(nom=f"carton ({cle})", prix=0.0, masse=None, source="carton de récupération : 0 CHF")
    return dict(nom=cle, prix=None, masse=None, source="aucun marché relevé")


def nombres_kit() -> dict:
    """Servos du robot debout (kit.py, option progressive) : {id: nombre}, axes de côté comptés deux fois."""
    import kit as K
    e = K.etude("progressive")
    out = {}
    for ax, r in e["choix"].items():
        if r["best"]:
            out[r["best"]["id"]] = out.get(r["best"]["id"], 0) + (2 if ax in K.COTES else 1)
    return out


def etapes() -> list[dict]:
    """Les étapes, nomenclature résolue (prix, masse) et nombres « kit » remplacés."""
    nk = nombres_kit()
    out = []
    for et in lire("kit_parcours.yaml")["etapes"]:
        items = []
        for it in et["nomenclature"]:
            it = dict(it)
            if it["n"] == "kit":
                it["n"] = nk.get(it["ref"].split(":")[1], 0)
            items.append(it)
        n_serv = sum(i["n"] for i in items if i["ref"].startswith("servo:") and isinstance(i["n"], int))
        for it in items:
            if it["n"] == "servos":
                it["n"] = n_serv
        items = [dict(it, **resoudre(it["ref"], {})) for it in items if it["n"]]
        out.append(dict(et, items=items, n_servos=n_serv))
    return out


# ─────────────────────────────── calculs par étape ──────────────────────
def courant_pire(items) -> float:
    """Pire cas sur le rail 12 V : tous les servos au blocage (kit_marche.yaml) + calculateur à sa capacité (A)."""
    import kit as K
    ctx = K.contexte()
    I = 0.0
    for it in items:
        if it["ref"].startswith("servo:"):
            I += it["n"] * (K.courant_blocage(ctx, it["ref"].split(":")[1]) or 0.0)
        if it["ref"].startswith("calc:rpi5"):
            I += P_RPI_W / 12.0
    return I


def chiffrer(ets: list[dict]) -> list[dict]:
    import kit as K
    ctxK = K.contexte()
    marge = lire("kit.yaml")["alimentation"]["progressive"]["marge_courant_secteur"]
    regle = lire("kit_parcours.yaml")["regle_reemploi"]
    possede = {}                                        # (ref, produit) → plus grand nombre possédé jusque-là
    res = []
    for et in ets:
        items = et["items"]
        for it in items:
            if it.get("bloc"):
                b = K.bloc_secteur(ctxK, courant_pire(items) * marge, True)
                it.update(nom=b["nom"], prix=b["prix"], source=b["source"])
        dur = [i for i in items if i["classe"] == "DURABLE"]
        st = [i for i in items if i["classe"] == "STRUCTURE"]
        cout = lambda xs: sum((i["prix"] or 0.0) * i["n"] for i in xs)
        inconnus = [i["nom"] for i in dur if i["prix"] is None]
        cle = lambda i: (i["ref"], i["nom"])            # le PRODUIT (un bloc plus fort n'est pas le même bloc)
        reemploi = sum((i["prix"] or 0.0) * min(i["n"], possede.get(cle(i), 0)) for i in dur)
        # réemployable dans le Lab (PROPOSÉ)
        lab_ft, lab = regle["lab_feetech_max"], 0.0
        for i in dur:
            if i["ref"].startswith("servo:") and lab_ft > 0:
                k = min(i["n"], lab_ft)
                lab_ft -= k
                lab += (i["prix"] or 0.0) * k
            elif i["ref"] in ("adaptateur_serie", "cellule:lab"):
                lab += (i["prix"] or 0.0) * i["n"]
        E = sum(i.get("E", 0) * i["n"] for i in items if i["ref"].startswith("cellule:"))
        res.append(dict(et, cout_durable=cout(dur), cout_structure=cout(st), inconnus=inconnus,
                        part_reemploi=reemploi / cout(dur) if cout(dur) else None,
                        part_lab=lab / cout(dur) if cout(dur) else None, E_Wh=E or None,
                        I_pire=courant_pire(items), couples=couples(et, ctxK)))
        for i in dur:
            possede[cle(i)] = max(possede.get(cle(i), 0), i["n"])
    return res


def couples(et, ctxK) -> list[dict]:
    """Couples statiques requis et marge (couple continu publié ÷ besoin) des servos de l'étape."""
    import kit as K
    import explorateur as X
    segs = K.segments(ctxK, K.carton_reference(ctxK), 0.0452)
    cam = next((i["masse"] for i in et["items"] if i["ref"].startswith("capteur:")), None) or 0.0
    st = K.statique(ctxK, segs, {}, cam)
    cat = {a["id"]: a for a in X.catalogue()[0]["feetech"]}
    out = []
    axes = [ax for i in et["items"] for ax in (i.get("axes") or [])]
    sid = next((i["ref"].split(":")[1] for i in et["items"] if i["ref"].startswith("servo:")), None)
    for ax in axes:
        if ax == "roue":
            out.append(dict(axe=ax, besoin=None, servo=sid, marge=None,
                            note="INCONNU : rayon de roue et résistance au roulement absents du dépôt"))
        elif ax in st:
            c = cat[sid]["continu"]
            out.append(dict(axe=ax, besoin=st[ax], servo=sid, marge=c / st[ax] if st[ax] > 0 else None, note="statique"))
        else:
            out.append(dict(axe=ax, besoin=0.0, servo=sid, marge=None, note="aucun couple statique (lacet)"))
    if et["n"] == 5:                                     # debout : kit.py, masse du robot debout
        e = K.etude("progressive")
        M = K.bilan(e)[3]["M_cumul"]
        deb = K.debout(ctxK, M)
        for ax, need in deb.items():
            r = e["choix"].get(ax)
            if r and r["best"]:
                out.append(dict(axe=ax, besoin=need, servo=r["best"]["id"], marge=r["best"]["continu"] / need,
                                note=f"debout, robot de {f1(M, 2)} kg"))
    return out


def regle_violee(ets) -> list[str]:
    """Règle de réemploi : un durable se fixe de façon démontable ; colle et agrafes seulement en structure."""
    r = lire("kit_parcours.yaml")["regle_reemploi"]
    fautes = []
    for et in ets:
        for i in et["items"]:
            ok = r["fixations_durables"] if i["classe"] == "DURABLE" else r["fixations_structure"]
            if i["fixation"] not in ok:
                fautes.append(f"étape {et['n']} : {i['nom']} ({i['classe']}) fixé par « {i['fixation']} »")
    return fautes


# ─────────────────────────────── rapport ────────────────────────────────
INTERFACES = [
    ("motif de trous", "boîtier STS3215 : trous autotaraudeurs « B-PA2.0 » (dessus) et « PA3.0X5 » (dessous), non cotés "
     "par Feetech (hardware.yaml, servos) ; le motif des brides relevées (kit_parcours_marche.yaml) ; un pas de grille "
     "à choisir (par exemple celui des brides, pour que structure, brides et Lab partagent les mêmes trous)"),
    ("famille de vis", "M2 (autotaraudeuses du boîtier), M3 (palonnier : « M3×6 » sur le plan Feetech), M4 (pivots du "
     "niveau 0) ; ISO métriques, peu de références (vision-produit, PROPOSÉ)"),
    ("câble de servo", "connecteur « 5264 / 2,54 mm, 3 broches » (plan Feetech : GND, V, signal), chaînable d'un servo "
     "à l'autre ; longueurs à choisir"),
    ("connecteur d'alimentation", "prise DIN 4 broches des blocs Mean Well GST (kit_marche.yaml) ; jack 5,5 × 2,5 du bloc "
     "12 V 10 A ; XT30 ou XT60 (usage courant, non relevé au dépôt) côté batterie"),
    ("rail de tension", "12 V : STS3215-C018 (4 à 14 V) et STS3250 (6 à 12 V) ; 7,4 V : STS3215-C001 ; pack 3S (9 à "
     "12,6 V à la coupure de 3,0 V) dans la plage du C018, PAS dans celle du STS3250 à pleine charge (12,6 > 12 V)"),
    ("bus", "série TTL demi-duplex (une ligne signal), 1 Mbit/s par défaut (actionneurs.yaml) ; adaptateur USB (bus.yaml)"),
    ("protocole", "protocole série Feetech (STS/SCS, identifiants 0 à 253) ; bibliothèques SCServo / STservo ; tables "
     "de LeRobot (source secondaire, actionneurs.yaml)"),
]


def rapport(res, fautes) -> str:
    mp = marche_parcours()
    L = ["# Le parcours guidé du Kit (2026-10)", "",
         "**Engendré** par `.venv/bin/python scripts/kit_parcours.py --ecrire`. **Les étapes sont PROPOSÉES, non "
         "décidées.** Décidé par Jeremy (fiche 0076) : le parcours guidé, le réemploi, préconiser sans imposer, "
         "l'outillage du Kit. Méthode : en tête de `scripts/kit_parcours.py`.", "",
         "## Par étape", "",
         "| Étape | Coût durable (CHF HT, borne basse) | Coût structure | Durables sans prix | Réemploi depuis les étapes "
         "précédentes | Réemployable dans le Lab | Alimentation | Pire courant 12 V (A) | Énergie du pack (Wh) | Marge la plus juste |",
         "| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | --- |"]
    for r in res:
        mg = [c for c in r["couples"] if c["marge"] is not None]
        juste = min(mg, key=lambda c: c["marge"]) if mg else None
        L.append(f"| {r['n']}. {r['nom']} | ≥ {f1(r['cout_durable'], 0)} | {f1(r['cout_structure'], 0)} | "
                 f"{len(r['inconnus'])} | {f1(r['part_reemploi'] and 100 * r['part_reemploi'], 0)} % | "
                 f"{f1(r['part_lab'] and 100 * r['part_lab'], 0)} % | {r['alimentation']} | {f1(r['I_pire'])} | "
                 f"{f1(r['E_Wh'], 1)} | " + (f"{juste['axe']} ({juste['servo']}) ×{f1(juste['marge'], 2)}" if juste else "—")
                 + " |")
    L += ["", "Marge : couple CONTINU publié du servo ÷ couple statique requis ; la marge de la fiche 0051 vaut 1,5. "
          "Réemploi : coût des durables déjà achetés à une étape précédente ÷ coût des durables de l'étape.", ""]
    for r in res:
        L += [f"## Étape {r['n']} : {r['nom']}", "", r["but"] + ".", "",
              f"Alimentation : {r['alimentation']}. Outillage (celui du Kit seulement) : {', '.join(r['outillage'])}"
              + " (le tournevis : ajouté par Jeremy le 2026-10-11, fiche 0077)." , "",
              "| Composant | Nombre | Classe | Fixation | Prix unitaire (CHF HT) | Source |",
              "| --- | ---: | --- | --- | ---: | --- |"]
        for i in r["items"]:
            L.append(f"| {i['nom']} | {i['n']} | {i['classe']} | {i['fixation']} | {f1(i['prix'], 2)} | {i['source']} |")
        if r["couples"]:
            L += ["", "| Axe | Servo | Couple requis (N·m) | Marge (continu ÷ requis) | Note |", "| --- | --- | ---: | ---: | --- |"]
            for c in r["couples"]:
                L.append(f"| {c['axe']} | {c['servo']} | {f1(c['besoin'], 3)} | {f1(c['marge'], 2)} | {c['note']} |")
        if r.get("variante_locale"):
            L += ["", "Variante IA « locale » : + " + ", ".join(resoudre(v["ref"], {})["nom"] for v in r["variante_locale"])
                  + f" ({f1(resoudre(r['variante_locale'][0]['ref'], {})['prix'], 0)} CHF HT). Variante « réseau » : rien "
                  "de plus sur le robot (le modèle tourne ailleurs)."]
        if r.get("variante_bras"):
            p = resoudre(r["variante_bras"], {})
            L += ["", f"Variante bras : {p['nom']} ({f1(p['prix'], 0)} CHF HT, {p['source']})."]
        if r.get("variante_batterie"):
            p = resoudre(r["variante_batterie"], {})
            L += ["", f"Variante batterie d'outillage : {p['nom']}, {f1(p.get('E'), 0)} Wh, {f1(p['prix'], 0)} CHF HT ; "
                  "sa tension (18 V) dépasse la plage du STS3215 (14 V) : un convertisseur 12 V en plus."]
        L.append("")
    L += ["## Règle de réemploi", "",
          "Tout durable se fixe de façon démontable (vis, écrou, insert, clip, connecteur) ; colle et agrafes seulement "
          "entre deux pièces de structure. " + ("**Respectée** sur toutes les étapes (test)." if not fautes
                                                else "**Violée** : " + " ; ".join(fautes)), ""]
    L += ["## Vérifié sur des sources (relevé du 2026-10-11, `params/kit_parcours_marche.yaml`)", ""]
    for cle, titre in (("rotation_continue", "Rotation continue du STS3215"), ("brides", "Brides métalliques du commerce"),
                       ("projets", "Projets ouverts"), ("ia_locale", "IA locale sur Raspberry Pi 5")):
        L.append(f"- **{titre}** : " + ("; ".join(str(x.get("resume") or x.get("nom")) for x in (mp.get(cle) or []))
                                         or "non relevé (null)"))
    L += ["", "## Interfaces communes à fixer plus tard (rien n'est décidé)", "",
          "| Interface | Options compatibles avec le STS3215 et ses brides |", "| --- | --- |"]
    for n, o in INTERFACES:
        L.append(f"| {n} | {o} |")
    return "\n".join(L) + "\n"


def tout():
    res = chiffrer(etapes())
    return res, regle_violee(res)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ecrire", action="store_true")
    a = ap.parse_args(argv)
    res, fautes = tout()
    for r in res:
        print(f"  {r['n']} {r['nom']} : durable ≥ {r['cout_durable']:.0f} CHF ({len(r['inconnus'])} sans prix), "
              f"réemploi {100 * (r['part_reemploi'] or 0):.0f} %, Lab {100 * (r['part_lab'] or 0):.0f} %, "
              f"pire {r['I_pire']:.1f} A, pack {r['E_Wh'] or 0:.0f} Wh")
    print(f"  règle de réemploi : {len(fautes)} faute(s)")
    if a.ecrire:
        DOC.write_text(rapport(res, fautes), encoding="utf-8")
        print(f"  -> {DOC.relative_to(REPO)}")
    return 1 if fautes else 0


if __name__ == "__main__":
    sys.exit(main())
