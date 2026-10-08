#!/usr/bin/env python3
"""Système électrique d'une solution : tension, énergie, batterie, calculateur, bus, chaîne de puissance, place.

    .venv/bin/python scripts/systeme_electrique.py      # canaux CAN à 250 et 500 Hz ; variantes 12S / 13S

Créé le 2026-10-07 (phase 4a quinquies). Appelé par l'explorateur pour chaque
solution ; ÉTUDE, aucune décision. Contexte DÉCIDÉ : fiches 0070 (batterie) et
0071 (autonomie 30 / 60 min, cycle 40 s de marche + 20 s debout, IA « commande
+ vision » / « modèle de langage local » ; 12S ou 13S « sur les chiffres »).
Architecture, rendements, facteurs de pack, critères d'IA : PROPOSÉS, dans
params/puissance.yaml. Une donnée absente n'est jamais estimée : elle est
rendue dans `inconnues`.
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import marche_composants as MC  # noqa: E402

G = 9.80665                                     # non-cote: pesanteur normale (m/s²)
V_RAIL_CALC = 12.0                              # non-cote: rail du calculateur (prompt du 2026-10-07 : convertisseur 12 V)


def lire(nom):
    import marche_composants as MC
    return MC.lire(nom)


def nombres(x) -> list[float]:
    return [float(a.replace(",", ".")) for a in re.findall(r"\d+(?:[.,]\d+)?", str(x or ""))]


# ─────────────────────────────── tension ────────────────────────────────
def variante(S: int, bat=None, coupure=None) -> dict:
    """Pack Li-ion de S cellules en série : tensions de coupure (fin de décharge), nominale, pleine charge.
    `coupure` (V par cellule) : seuil d'arrêt étudié en variante (2026-10-08) ; absent, la coupure de la fiche."""
    c = MC.chimie(bat or lire("batteries.yaml"), "li_ion")
    vc = coupure if coupure is not None else c["tension_min_V"]
    return dict(S=S, Vfin=S * vc, Vnom=S * c["tension_nominale_V"], Vmax=S * c["tension_max_V"], coupure=vc)


def compatibilite(plage, var) -> bool | None:
    """Le pack reste-t-il dans la plage publiée de l'actionneur, de la coupure à la pleine charge ? None : plage inconnue."""
    if plage is None or None in plage:
        return None
    return var["Vfin"] >= plage[0] - 1e-9 and var["Vmax"] <= plage[1] + 1e-9


def facteur_vitesse(v_ref, var) -> float | None:
    """HYPOTHÈSE écrite (prompt du 2026-10-07) : vitesse à vide ∝ tension ; ramenée à la tension de FIN de décharge.
    `v_ref` : tension à laquelle la fiche donne la vitesse (48 V pour les RobStride). None si inconnue."""
    return var["Vfin"] / v_ref if v_ref else None


# ─────────────────────────────── énergie ────────────────────────────────
def table_puissance(marches: dict, cap: dict, HS) -> dict:
    """{(H, v): {type: (p_moy*, p_pointe*)}} : marche, le plus exigeant des robots qui couvrent le Froude, niveaux
    inférieurs compris (même règle que les couples)."""
    frs = {r: e["Fr"] for r, e in marches.items()}
    niv = cap["taches"]["marche_sol_plat"]["niveaux"]
    out = {}
    for H in HS:
        for i, v in enumerate(niv):
            tab = {}
            for w in niv[:i + 1]:
                for r, f in frs.items():
                    if f < w / math.sqrt(G * H) - 1e-9:
                        continue
                    for ty, p in marches[r]["profil"].items():
                        pm, pk = p.get("puissance_moy"), p.get("puissance")
                        a, b = tab.get(ty, (0.0, 0.0))
                        tab[ty] = (max(a, pm or 0.0), max(b, pk or 0.0))
            if tab:
                out[(round(H, 2), v)] = tab
    return out


def table_pointe_3a(lignes_ep) -> dict:
    """{(H, tâche, niveau): {axe: (aP, bP)}} : puissances de pointe des tâches directes (phase 3a)."""
    out = {}
    for l in lignes_ep:
        if l.get("aP") or l.get("bP"):
            out.setdefault((round(l["H"], 2), l["tache"], l["niveau"]), {})[l["articulation"]] = (l["aP"], l["bP"])
    return out


def energie(ctx, axes: dict, M: float, Ht: float, profil: dict, p_calc_W, p_aux_W, hyp, var=None) -> dict:
    """Puissance moyenne du cycle, énergie pour l'autonomie visée, courant de pointe (au rendement BAS)."""
    cible = ctx["cible"]
    v = cible.get("marche_sol_plat")
    unite = M * G * math.sqrt(G * Ht)                                 # W par unité de P*
    tab = ctx["Pm"].get((round(Ht, 2), v))
    if tab is None:
        return dict(inconnues=[f"puissance de marche à {Ht:.2f} m (Froude au-delà des marches simulées)"])
    eta = hyp["rendement_actionneurs"]["bas"]
    p_mec = sum(n * tab.get(a, (0.0, 0.0))[0] for a, n in axes.items()) * unite
    # pointe : par axe, le maximum des tâches du profil (marche simulée, 3a), puis la SOMME des axes (prudent)
    pk = {}
    for a, n in axes.items():
        x = tab.get(a, (0.0, 0.0))[1] * unite
        for t, niv in ((t, n_) for t, vv in profil.items() for n_ in (vv if isinstance(vv, list) else [vv])):
            ab = ctx["P3a"].get((round(Ht, 2), t, niv), {}).get(a)
            if ab:
                x = max(x, ab[0] * M + ab[1])
        pk[a] = n * x
    inconnues = []
    if p_calc_W is None:
        inconnues.append("puissance du calculateur")
    fixe = (p_calc_W or 0.0) + (p_aux_W or 0.0)
    cycle = hyp.get("cycle_marche_s", 40.0), hyp.get("cycle_debout_s", 20.0)
    p_moy = (cycle[0] * p_mec / eta) / (cycle[0] + cycle[1]) + fixe          # debout : 0 mécanique (dit)
    minutes = cible.get("autonomie")
    fc = 1.0
    if var is not None:                                 # énergie au-dessus de la coupure (PROPOSÉ, puissance.yaml)
        tab = hyp.get("energie_au_dessus_de_la_coupure") or {}
        fc = next((float(v) for k, v in tab.items() if k != "statut" and abs(float(k) - var["coupure"]) < 1e-6), None)
        if fc is None:
            return dict(inconnues=[f"énergie au-dessus d'une coupure de {var['coupure']} V"])
    E = p_moy * minutes / 60.0 / hyp["fraction_utilisable"]["valeur"] / fc if minutes else None
    return dict(p_mec_marche=p_mec, p_elec_moy=p_moy, E_Wh=E, P_pointe=sum(pk.values()) / eta + fixe,
                autonomie_min=minutes, inconnues=inconnues)


# ─────────────────────────────── batterie ───────────────────────────────
# Ajouté le 2026-10-08 (prompt du lot 4a sexies) : « Seules les cellules neuves d'un distributeur identifié sont
# retenues. » Mentions lues dans les notes du marché qui EXCLUENT une offre :
EXCLUSIONS_CELLULES = (("reclaimed", "cellules de récupération"), ("récupération", "cellules de récupération"),
                       ("occasion", "occasion"), ("marque masquée", "marque masquée : identité du fabricant non garantie"))


def exclusion_cellule(b: dict) -> str | None:
    """La raison d'écarter l'offre retenue d'une cellule (récupération, occasion, marque masquée), ou None."""
    p = b["p"]
    txt = " ".join(str(x) for x in (p.get("prix") or {}, p.get("disponibilite_ch_ue"))).lower()
    return next((r for m, r in EXCLUSIONS_CELLULES if m in txt), None)


def cellules_21700(bat=None, taux=None, ecartees=None) -> list[dict]:
    """Les cellules 21700 NEUVES d'un distributeur identifié ; les autres sont rangées dans `ecartees` avec leur raison."""
    out = []
    for b in MC.batteries(bat, taux):
        if b["famille"] != "cellule_21700":
            continue
        r = exclusion_cellule(b)
        if r is None and b["prix"] is not None and not (b["p"].get("prix") or {}).get("vendeur"):
            r = "distributeur non identifié"
        if r and ecartees is not None:
            ecartees[b["id"]] = r
        if not r:
            out.append(b)
    return out


def batterie(cells, var, E_Wh, P_pointe_W, hyp) -> dict:
    """La composition S × P la plus LÉGÈRE qui fournit l'énergie ET le courant de pointe (au courant CONTINU publié)."""
    S = var["S"]
    I = P_pointe_W / var["Vfin"]                                     # courant au plus bas de la décharge : prudent
    best, ecartees = None, []
    for c in cells:
        if not (c["E"] and c["I"] and c["m"] and c["vol"]):
            ecartees.append(c["id"])
            continue
        P = max(1, math.ceil(E_Wh / (S * c["E"]) - 1e-9), math.ceil(I / c["I"] - 1e-9))
        m = S * P * c["m"] * hyp["facteur_pack_masse"]["valeur"]
        if best is None or m < best["masse"]:
            vol = S * P * c["vol"] / (math.pi / 4) * hyp["facteur_pack_volume"]["valeur"]
            best = dict(id=c["id"], nom=c["nom"], S=S, P=P, masse=m, volume=vol, E=S * P * c["E"], I=P * c["I"],
                        prix=(S * P * c["prix"]) if c["prix"] else None, I_requis=I)
    inc = [] if best and best["prix"] is not None else ([f"prix de la cellule {best['id']}"] if best else [])
    return dict(best=best, ecartees=ecartees, inconnues=inc if best else ["aucune cellule 21700 complète au marché"])


# ─────────────────────────────── calculateur ────────────────────────────
def memoire_GB(p) -> float | None:
    n = nombres(MC.v(p, "memoire") or p.get("nom"))
    m = re.search(r"(\d+)\s*GB", str(MC.v(p, "memoire") or p.get("nom")))
    return float(m.group(1)) if m else (n[0] if n else None)


def plage_V(p):
    n = nombres(MC.v(p, "tension_alimentation"))
    return (min(n), max(n)) if len(n) >= 2 else ((n[0], n[0]) if n else None)


def prix_produit(p, taux):
    return MC.chf(p.get("prix_ue"), taux) if p.get("prix_ue") else MC.chf(p.get("prix"), taux)


def options_calculateur(cal=None, taux=None, compl=None) -> list[dict]:
    """Modules Jetson + porteuse 12 V, kits Jetson, Raspberry Pi 5 (+ carte d'IA). Rien n'est estimé."""
    cal = cal or lire("calculateurs.yaml")
    taux = taux or lire("budget.yaml")["taux_de_change"]
    P = cal["marche"]["produits"]
    compl = compl or {}

    def val(pid, champ):
        x = (compl.get(pid) or {}).get(champ)
        return MC.num(MC.v({"x": x}, "x")) if x is not None else MC.num(MC.v(P[pid], champ))

    def vendu(p):
        st = str(MC.v(p, "statut") or p.get("statut") or "")
        return "annonc" not in st and "FIN DE PRODUCTION" not in st

    out = []
    porteuses = [k for k, p in P.items() if p["famille"] == "porteuse"]
    for mid, m in P.items():
        if not vendu(m):
            continue
        pw = (m.get("puissance_W") or {})
        pmax = MC.num(MC.v(pw, "max"))
        if m["famille"] == "jetson_module":
            for cid in porteuses:
                c = P[cid]
                acc = str(MC.v(c, "modules_acceptes") or "")
                if not any(f in m["nom"] and f in acc for f in ("Orin Nano", "Orin NX")):
                    continue
                pl = plage_V(c)
                out.append(dict(id=f"{mid}+{cid}", nom=f"{m['nom']} + {c['nom']}", accel=True, llm=True, mem=memoire_GB(m),
                                volume=MC.volume_l(MC.v(c, "cotes_porteuse") or MC.v(c, "cotes_module")), type="jetson",
                                prix=_somme(prix_produit(m, taux), prix_produit(c, taux)),
                                masse=_somme(val(mid, "masse_module"), val(cid, "masse_ensemble")),
                                pmax=pmax, can=c["can_integre"].get("canaux") if c["can_integre"].get("valeur") else 0,
                                v12=(pl[0] <= V_RAIL_CALC <= pl[1]) if pl else None, rail="12", porteuse=cid))
        elif m["famille"] == "jetson_kit":
            pl = plage_V(m)
            out.append(dict(id=mid, nom=m["nom"], accel=True, llm=True, mem=memoire_GB(m), prix=prix_produit(m, taux),
                            volume=MC.volume_l(MC.v(m, "cotes_porteuse") or MC.v(m, "cotes_module")), type="jetson",
                            masse=val(mid, "masse_ensemble"), pmax=pmax,
                            can=m["can_integre"].get("canaux") if m["can_integre"].get("valeur") else None,
                            v12=(pl[0] <= V_RAIL_CALC <= pl[1]) if pl else None, rail="12", porteuse=None))
        elif m["famille"] == "rpi" and "cm5" not in mid:
            base = dict(mem=memoire_GB(m), can=0, v12=True, rail="5", porteuse=None, type="rpi",
                        volume=MC.volume_l(MC.v(m, "cotes_porteuse") or MC.v(m, "cotes_module")))
            out.append(dict(base, id=mid, nom=m["nom"], accel=False, llm=False, prix=prix_produit(m, taux),
                            masse=val(mid, "masse_ensemble"),
                            pmax=pmax))
            for aid, a in P.items():
                if a["famille"] == "rpi_ia" and vendu(a) and "camera" not in aid:
                    pa = MC.num(MC.v(a.get("puissance_W") or {}, "max"))
                    # Hailo-10H (AI HAT+ 2) : présenté par Raspberry Pi pour les modèles de langage (rapports secondaires,
                    # marché du 2026-10-07) ; les Hailo-8 / 8L, pour la vision seulement
                    out.append(dict(base, id=f"{mid}+{aid}", nom=f"{m['nom']} + {a['nom']}", accel=True,
                                    llm=aid == "rpi_ai_hat_plus_2",
                                    prix=_somme(prix_produit(m, taux), prix_produit(a, taux)),
                                    masse=_somme(val(mid, "masse_ensemble"), val(aid, "masse_ensemble")),
                                    pmax=_somme(pmax, pa)))
    return out


def _somme(*x):
    return None if any(a is None for a in x) else sum(x)


def choisir_calculateur(options, niveau, hyp) -> dict:
    """Le MOINS CHER qui convient au niveau d'IA (critères PROPOSÉS) et vérifiable ; à défaut, le moins cher sur ce
    qui est connu, et ce qui manque."""
    crit = hyp["niveaux_ia"][niveau]
    ok = [o for o in options if (o["accel"] or not crit["accelerateur"]) and (o["mem"] or 0) >= crit["memoire_GB"]
          and o["v12"] is not False and (o["llm"] or not crit.get("modele_de_langage"))]
    manque = lambda o: [k for k, lib in (("prix", "prix"), ("masse", "masse"), ("pmax", "puissance max"),
                                         ("v12", "tension d'entrée 12 V")) if o[k] is None]
    sur = sorted((o for o in ok if not manque(o)), key=lambda o: o["prix"])
    if sur:
        return dict(best=sur[0], inconnues=[], n=len(ok))
    conn = sorted((o for o in ok if o["prix"] is not None), key=lambda o: o["prix"])
    if conn:
        return dict(best=conn[0], inconnues=[f"{lib} de {conn[0]['nom']}" for lib in manque(conn[0])], n=len(ok))
    return dict(best=None, inconnues=[f"aucun calculateur chiffré pour « {niveau} »"], n=len(ok))


# ─────────────────────────────── bus ────────────────────────────────────
def variantes_adaptateur(pid, p, taux) -> list[dict]:
    """Un adaptateur CAN, ou ses variantes « 1, 2 ou 4 canaux » au prix de chacune."""
    ch, pr = MC.v(p, "canaux"), p.get("prix") or {}
    masse = max(nombres(MC.v(p, "masse_g")), default=None)                       # la plus lourde : prudent
    vol = MC.volume_l(MC.v(p, "cotes_mm"))
    pm = MC.v(p, "pilote_mainline")
    linux_ok = None if pm is None else (pm is True or str(pm).lower().startswith("oui"))   # None : pilote non nommé
    m = re.findall(r"(\d+[.,]\d+|\d+)\s*\((\d+)", str(pr.get("valeur")))
    if m:
        return [dict(id=f"{pid}_{n}ch", nom=f"{p['nom']} ({n} canaux)", canaux=int(n), linux=linux_ok, masse=masse,
                     famille=p["famille"], volume=vol,
                     prix=MC.chf(dict(pr, valeur=float(x.replace(",", "."))), taux)) for x, n in m]
    n = nombres(ch)
    return [dict(id=pid, nom=p["nom"], canaux=int(n[0]) if n else None, linux=linux_ok, masse=masse, famille=p["famille"],
                 volume=vol,
                 prix=MC.chf(pr, taux))]


def adaptateurs_can(b=None, taux=None, canhub=None) -> list[dict]:
    b = b or lire("bus.yaml")
    taux = taux or lire("budget.yaml")["taux_de_change"]
    out = []
    for pid, p in b["marche"]["produits"].items():
        # M.2 / miniPCIe : un emplacement libre sur le calculateur n'est relevé nulle part (PROPOSÉ : non retenus)
        if p["famille"] in ("can_usb", "can_spi") and not pid.startswith("_") and "jetson" not in pid:
            out += variantes_adaptateur(pid, p, taux)
    if canhub:
        out.append(dict(canhub, linux=canhub.get("linux")))
    return [a for a in out if a["canaux"]]


def choisir_bus(n_can: int, can_calc, adapt, serie, type_calc="jetson") -> dict:
    """Canaux CAN manquants (au-delà de ceux du calculateur) par le type d'adaptateur le moins cher ; un bus série.
    Les cartes SPI au format HAT ne se montent que sur un Raspberry Pi (PROPOSÉ) ; l'USB va partout."""
    adapt = [a for a in adapt if a.get("famille") != "can_spi" or type_calc == "rpi"]
    reste = max(0, n_can - (can_calc or 0))
    inc = [] if can_calc is not None else ["nombre de canaux CAN du calculateur"]
    best = None
    if reste:
        for a in adapt:
            if a["linux"] is False:
                continue
            k = math.ceil(reste / a["canaux"])
            cout = k * a["prix"] if a["prix"] is not None else None
            cle = (cout is None or a["masse"] is None or a["linux"] is None, cout if cout is not None else 1e12)
            if best is None or cle < best["cle"]:
                best = dict(a, unites=k, cout=cout, masse_tot=(k * a["masse"]) if a["masse"] is not None else None, cle=cle,
                            volume_tot=(k * a["volume"]) if a.get("volume") is not None else None)
        if best is None:
            inc.append("aucun adaptateur CAN avec pilote Linux principal")
        else:
            inc += [f"{x} de {best['nom']}" for x, y in (("prix", best["cout"]), ("masse", best["masse_tot"]),
                                                          ("pilote Linux", best["linux"])) if y is None]
    s = serie
    if s:
        inc += [f"{x} de {s['nom']}" for x in ("prix", "masse") if s.get(x) is None]
    if best and best.get("volume_tot") is None:
        inc.append(f"cotes de {best['nom']}")
    return dict(can=best, reste=reste, serie=s, inconnues=inc, volume=(best or {}).get("volume_tot", 0.0) if best else 0.0,
                prix=_somme(best["cout"] if best else 0.0, (s or {}).get("prix", 0.0)),
                masse=_somme(best["masse_tot"] if best else 0.0, (s or {}).get("masse", 0.0)))


def adaptateur_serie(b=None, taux=None) -> dict | None:
    """Le moins cher des adaptateurs série Feetech dont le prix et la masse sont lus."""
    b = b or lire("bus.yaml")
    taux = taux or lire("budget.yaml")["taux_de_change"]
    c = [dict(id=k, nom=p["nom"], prix=MC.chf(p.get("prix"), taux), masse=MC.num(MC.v(p, "masse_g")))
         for k, p in b["marche"]["produits"].items() if p["famille"] == "serie_feetech"]
    c = [x for x in c if x["prix"] is not None and x["masse"] is not None]
    return min(c, key=lambda x: x["prix"]) if c else None


def canaux_can(axes_can: int, f_hz: float, etendue: bool, b=None) -> dict:
    b = b or lire("bus.yaml")
    bt = MC.bits_trame(b["trame_can"], etendue)
    return MC.canaux_can(axes_can, f_hz, 2, bt["total"], 1e6, MC.CHARGE_MAX)


# ─────────────────────────────── place ──────────────────────────────────
def place_tronc(R: dict, H_reel: float, volume_L: float, hyp) -> dict:
    """Volume disponible dans le tronc (ANSUR, à la hauteur réelle) ; s'il manque, le tronc s'allonge d'autant."""
    larg, prof, haut = R["largeur_epaules"] * H_reel, R["profondeur_poitrine"] * H_reel, R["tronc_hauteur"] * H_reel
    f = hyp["remplissage_tronc"]["valeur"]
    dispo = larg * prof * haut * f * 1000                                       # L
    exces = max(0.0, volume_L - dispo)
    return dict(dispo_L=dispo, requis_L=volume_L, allonge_m=exces / 1000 / (larg * prof * f))


def main() -> int:
    b = lire("bus.yaml")
    print("  Canaux CAN (1 Mbit/s, commande + réponse par axe, pire bourrage, charge ≤ 70 %) :")
    for f in (250, 500):
        for et, nom in ((False, "MIT, trame standard"), (True, "privé, trame étendue")):
            for n in (27, 23):
                c = canaux_can(n, f, et, b)
                print(f"    {f} Hz, {nom}, {n} axes : {c['besoin'] / 1e6:.2f} Mbit/s -> {c['canaux']} canaux")
    for S in (12, 13):
        v = variante(S)
        print(f"  {S}S : {v['Vfin']:.1f} V (coupure) / {v['Vnom']:.1f} V / {v['Vmax']:.1f} V ; vitesses ×{v['Vfin'] / 48:.3f} (fiche à 48 V)")
    return 0


if __name__ == "__main__":
    sys.exit(main())


# ─────────────────────────────── chaîne de puissance ────────────────────
CHAMPS_I = ("courant_continu", "courant_nominal", "courant_a", "courant_continu_A", "courant_nominal_A", "calibre_A")
CHAMPS_V = ("tension_dc_nominale", "tension_dc_max", "tension_max", "tension_dc_V", "tension_max_V")


def _premier(p, champs):
    """La première valeur lue ; pour une plage « 6 ~ 12 » ou une liste « 125 / 200 », le premier nombre (le plus bas :
    prudent pour un courant admissible)."""
    for c in champs:
        x = MC.num(MC.v(p, c))
        if x is not None:
            return x
    return None


def _texte(p) -> str:
    return " ".join(str((x or {}).get("note") or "") + " " + str((x or {}).get("valeur") or "")
                    for x in p.values() if isinstance(x, dict)).lower()


def composants(pui: dict, taux=None) -> list[dict]:
    taux = taux or lire("budget.yaml")["taux_de_change"]
    bornes = pui.get("bornes_proposees") or {}
    out = []
    for pid, p in ((pui.get("marche") or {}).get("produits") or {}).items():
        # bornes PROPOSÉES (majorantes) : seulement là où la valeur lue est null ; chaque usage est noté
        utilisees = []
        for champ, bo in (bornes.get(pid) or {}).items():
            cle = "tension_max" if champ == "tension_max_V" else champ
            if MC.v(p, cle) is None:
                p = dict(p, **{cle: {"valeur": bo["valeur"], "note": "BORNE PROPOSÉE : " + bo["justification"]}})
                utilisees.append(f"{champ} de {p.get('nom', pid)}")
        Vs = nombres(MC.v(p, "tension_service"))
        V = _premier(p, CHAMPS_V)
        ns = nombres(MC.v(p, "nombre_s"))
        out.append(dict(id=pid, nom=p.get("nom", pid), categorie=p.get("categorie"), I=_premier(p, CHAMPS_I),
                        V=V if V is not None else (max(Vs) if Vs else None),
                        Vout=MC.num(MC.v(p, "sortie_v")), Vin=nombres(MC.v(p, "entree_v")),
                        S=(min(ns), max(ns)) if ns else None, seuil=MC.num(MC.v(p, "seuil_declenchement_48v")),
                        bidir=MC.v(p, "bidirectionnel"), certif=str(MC.v(p, "certification_securite") or ""),
                        texte=_texte(p), masse=MC.num(MC.v(p, "masse_g")), bornes=utilisees,
                        volume=MC.volume_l(p.get("dimensions_mm")), prix=MC.chf(p.get("prix"), taux)))
    return out


def admissible(x, categorie, var) -> bool:
    """Filtres propres à chaque maillon (écrits, PROPOSÉS) ; une valeur non lue ne fait PAS échouer (elle est rendue)."""
    if categorie == "bms" and x["S"] and not (x["S"][0] <= var["S"] <= x["S"][1]):
        return False                                   # BMS : le nombre de cellules en série de la variante
    if categorie == "contacteur" and (x["bidir"] is False or "courant inverse" in x["texte"]):
        return False                                   # le freinage renvoie du courant : il doit passer dans les deux sens
    if categorie == "arret_urgence" and x["certif"].lower().startswith("aucune"):
        return False                                   # un relais radio sans liaison surveillée n'est pas un arrêt d'urgence
    if categorie == "regeneration" and (x["seuil"] is None or not (var["Vmax"] < x["seuil"] <= 60.0)):
        return False                                   # un absorbeur sans seuil publié n'en est pas un (résistances seules) ;
        #                                                sous la pleine charge il viderait le pack ; au-delà de 60 V : trop tard
    porte = "porte-fusible" in x["nom"].lower() or "holder" in x["nom"].lower()
    if categorie == "fusible" and porte:
        return False                                   # le fusible ; son porte-fusible est le maillon suivant
    if categorie == "porte_fusible":
        return porte
    return True


def composant(comps, categorie, I=None, V=None, Vout=None, Vin=None, var=None) -> dict:
    """Le moins cher de la catégorie dont les valeurs LUES tiennent I (A), V (V), la sortie Vout et l'entrée Vin ;
    vérifiable d'abord, sinon le moins cher sur ce qui est connu (et ce qui manque)."""
    cat_marche = "fusible" if categorie == "porte_fusible" else categorie
    c = [x for x in comps if x["categorie"] == cat_marche and (var is None or admissible(x, categorie, var))]
    if Vout is not None:
        c = [x for x in c if x["Vout"] is None or abs(x["Vout"] - Vout) < 0.6]
    if Vin is not None:                                # une tension, ou la plage (coupure, pleine charge) du pack
        lo, hi = (Vin, Vin) if not isinstance(Vin, tuple) else Vin
        c = [x for x in c if not x["Vin"] or (min(x["Vin"]) <= lo and hi <= max(x["Vin"]))]
    c = [x for x in c if (I is None or x["I"] is None or x["I"] >= I) and (V is None or x["V"] is None or x["V"] >= V)]

    def manque(x):
        m = [lib for k, lib in (("prix", "prix"), ("masse", "masse"), ("volume", "cotes")) if x[k] is None]
        m += (["courant"] if I is not None and x["I"] is None else []) + (["tension"] if V is not None and x["V"] is None else [])
        m += (["tension de sortie"] if Vout is not None and x["Vout"] is None else [])
        m += (["seuil de déclenchement"] if categorie == "regeneration" and x["seuil"] is None else [])
        return m
    sur = sorted((x for x in c if not manque(x)), key=lambda x: x["prix"])
    if sur:
        return dict(best=sur[0], inconnues=[])
    conn = sorted((x for x in c if x["prix"] is not None), key=lambda x: x["prix"]) or c
    if conn:
        return dict(best=conn[0], inconnues=[f"{m} de {conn[0]['nom']} ({categorie})" for m in manque(conn[0])])
    return dict(best=None, inconnues=[f"{categorie} : aucun produit au marché qui convienne"])


def rail_servo(plage) -> str | None:
    """Rail (6, 7,4 ou 12 V) qui tient dans la plage publiée d'un servo ; le plus bas (moins de courant de fuite)."""
    if not plage or None in plage:
        return None
    for r in ("6", "7.4", "12"):
        if plage[0] <= float(r) <= plage[1]:
            return r
    return None


# ─────────────────────────────── dimensionnement ────────────────────────
def dimensionner(el: dict, R: dict, cible: dict, axes_corps: dict, petits: list, M: float, Ht: float, Hr: float,
                 profil: dict, n_can_axes: int, ctx_tables: dict) -> dict:
    """Le système électrique d'une solution. `el` : contexte électrique ; `petits` : actionneurs des petits axes."""
    hyp, var = el["hyp"], el["var"]
    inc = []
    calc = (el["calc"] or {}).get("best")
    inc += (el["calc"] or {}).get("inconnues", []) if el["calc"] else ["niveau d'IA absent du profil"]
    # bus
    n_can = canaux_can(n_can_axes, el["f_can"], el["etendue"])["canaux"]
    bus = choisir_bus(n_can, (calc or {}).get("can"), el["adapt"], el["serie"] if petits else None,
                      (calc or {}).get("type", "jetson"))
    inc += bus["inconnues"]
    # énergie
    en = energie(ctx_tables, axes_corps, M, Ht, profil, (calc or {}).get("pmax"), 0.0, hyp, var)
    inc += en["inconnues"]
    bat = batterie(el["cells"], var, en["E_Wh"], en["P_pointe"], hyp) if en.get("E_Wh") else dict(best=None, inconnues=[])
    inc += bat["inconnues"]
    b = bat["best"]
    # chaîne de puissance et rails
    comps = el.get("comps")
    chaine, rails = [], {}
    if not comps:
        inc.append("chaîne de puissance : marché non versé (params/puissance.yaml, bloc marche)")
    else:
        I = b["I_requis"] if b else None
        for m in el["pui"]["chaine"]:
            if m.get("categorie"):
                chaine.append((m["maillon"], composant(comps, m["categorie"], I=I, V=var["Vmax"], var=var)))
                if m["categorie"] == "fusible":
                    chaine.append(("porte_fusible", composant(comps, "porte_fusible", I=I, V=var["Vmax"], var=var)))
        chaine.append(("regeneration", composant(comps, "regeneration", V=var["Vmax"], var=var)))
        chaine.append(("arret_urgence", composant(comps, "arret_urgence", var=var)))
        rails = {"12": composant(comps, "dcdc", Vout=12.0, Vin=(var["Vfin"], var["Vmax"]))}
        if (calc or {}).get("rail") == "5":
            rails["5"] = composant(comps, "dcdc", Vout=5.0, Vin=12.0)
        for r in sorted({rail_servo(a.get("plage_servo")) for a in petits} - {None}):
            if r != "12":
                rails[r] = composant(comps, "dcdc", Vout=float(r), Vin=(var["Vfin"], var["Vmax"]))
        if any(rail_servo(a.get("plage_servo")) is None for a in petits):
            inc.append("plage de tension d'un servo des petits axes : rail non choisi")
        for _, x in chaine + list(rails.items()):
            inc += x["inconnues"]
    elems, vus = [], set()
    for _, x in chaine + list(rails.items()):            # un même produit (XT90-S : sectionneur ET précharge) compte une fois
        if x["best"] and x["best"]["id"].replace("_precharge", "") not in vus:
            vus.add(x["best"]["id"].replace("_precharge", ""))
            elems.append(x["best"])
    # sommes (une valeur inconnue rend la somme inconnue, et c'est dit plus haut)
    masse = _somme(b["masse"] if b else None, (calc or {}).get("masse") and calc["masse"] / 1000,
                   bus["masse"] / 1000 if bus["masse"] is not None else None,
                   *[(x["masse"] / 1000) if x["masse"] is not None else None for x in elems])
    prix = _somme(b["prix"] if b else None, (calc or {}).get("prix"), bus["prix"], *[x["prix"] for x in elems])
    if any(x["best"] is None for _, x in chaine + list(rails.items())):
        prix = None                                      # un maillon manque (absorbeur en 13S…) : le coût n'est qu'une borne
    if (calc or {}).get("volume") is None and calc:
        inc.append(f"cotes de {calc['nom']}")
    connu = lambda xs: sum(x for x in xs if x is not None)
    volumes = ([("batterie", b["volume"] if b else None), ("calculateur", (calc or {}).get("volume")),
                ("cartes CAN", bus.get("volume"))]
               + [(f"{x['categorie']} : {x['nom'][:40]}", x["volume"]) for x in elems])
    volume = _somme(*[v for _, v in volumes])
    volume_connu = connu([v for _, v in volumes])
    prix_connu = connu([b["prix"] if b else None, (calc or {}).get("prix"), bus["prix"]] + [x["prix"] for x in elems])
    # place : sur le volume complet s'il est connu ; sinon sur sa part CONNUE (borne basse de l'allongement, dite)
    pl = place_tronc(R, Hr, volume if volume is not None else volume_connu, hyp)
    pl["partielle"] = volume is None
    return dict(calc=calc, bus=bus, n_can=n_can, energie=en, batterie=b, chaine=chaine, rails=rails, masse=masse,
                masse_connue=sum(x for x in [b and b["masse"], (calc or {}).get("masse") and calc["masse"] / 1000,
                                               bus["masse"] and bus["masse"] / 1000] + [x["masse"] / 1000 for x in elems
                                                                                        if x["masse"] is not None] if x),
                volume=volume, prix=prix, place=pl, volume_connu=volume_connu, prix_connu=prix_connu, volumes=volumes,
                bornes=[b for x in elems for b in x.get("bornes", [])],
                inconnues=list(dict.fromkeys(inc)))
