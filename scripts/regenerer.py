#!/usr/bin/env python3
"""Régénère TOUT : les pièces, puis le site statique.

    .venv/bin/python scripts/regenerer.py
    .venv/bin/python scripts/regenerer.py --site-seulement

Commande unique. Le Dockerfile n'appelle que celle-ci : ce qui tourne en
production est exactement ce que vous pouvez lancer chez vous.

═══════════════════════════════════════════════════════════════════════
 CE GÉNÉRATEUR NE CRÉE AUCUNE DONNÉE
═══════════════════════════════════════════════════════════════════════

Il lit le dépôt et le projette. Chaque valeur affichée par le site vient
d'un fichier du dépôt ou d'un relevé produit par une pièce. Deux sources
de vérité finiraient par diverger : il n'y en a qu'une.

Conçu pour TRENTE pièces, pas pour une :

  · build123d n'est importé QU'UNE FOIS. Les pièces sont appelées dans le
    même interpréteur, jamais par trente sous-processus. L'import coûte
    quelques secondes ; le payer trente fois serait absurde.
  · La liste est filtrable côté navigateur, sans rechargement.
  · Chaque pièce est indépendante : une qui échoue est signalée et les
    autres sont produites quand même.
"""
from __future__ import annotations

import argparse
import datetime
import html
import importlib.util
import json
import re
import shutil
import sys
import traceback
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from plan_decoupe import ordonner_cotes, svg_schema, polylignes_depuis_face  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
PARTS = REPO / "parts"
WEB = REPO / "web"
SITE = REPO / "site"
EXPORTS = REPO / "exports" / "parts"

ORIGINES = ["propre", "litterature", "catalogue", "mesure", "amont", "ambigu"]
LIB_ORIGINE = {
    "propre": ("propre", "dérivée de H et d'un ratio du projet"),
    "litterature": ("littérature", "publication scientifique ou norme — personne ne la possède"),
    "catalogue": ("catalogue", "fiche technique d'un constructeur"),
    "mesure": ("mesure", "relevée sur un objet physique"),
    "amont": ("amont", "vient de ToddlerBot — porte le risque de licence"),
    "ambigu": ("ambigu", "ne se range dans aucune origine — volontairement non tranché"),
    "non_qualifie": ("non qualifié", "aucune déclaration : c'est un défaut"),
}
LIB_NATURE = {
    "echelle": "échelle — dérive de H (règle 1)",
    "tenue": "tenue — charge, matériau, coefficient",
    "interface": "interface — quincaillerie (règle 2)",
    "procede": "procédé — moyen de fabrication",
    "sans_objet": "sans objet — n'est pas une cote",
}
FORMATS = [("dxf", "DXF", "découpe 2D"), ("step", "STEP", "échange CAO"),
           ("stl", "STL", "affichage 3D"), ("pdf", "PDF", "plan A4 à imprimer")]

INDET = '<span class="ind">non déterminé</span>'

# Fiche 0020 : un `null` a trois sens, pas un. La condition qui les
# distingue est LUE dans params/nullites.yaml, jamais écrite ici.
import nullites as NU
REGLES_NUL = NU.charger()


def prose(txt: str) -> str:
    """Échappe, puis rend `ceci` en <code>ceci</code>.

    Les motifs de nullites.yaml NOMMENT le champ dont ils dépendent : sans
    cette conversion, le lecteur voit des accents graves au lieu d'un
    identifiant, et l'identifiant est justement l'information.
    """
    out, morceaux = [], e(txt).split("`")
    for i, m in enumerate(morceaux):
        out.append(f"<code>{m}</code>" if i % 2 and i < len(morceaux) - 1 else m)
    return "".join(out)


def nul(etat: str, motif: str = "") -> str:
    """Une valeur absente se DIT, et dit pourquoi elle est absente."""
    t = f' title="{e(motif)}"' if motif else ""   # attribut : pas de balise
    return f'<span class="{NU.CLS[etat]}"{t}>{NU.LIB[etat]}</span>'

# ── Hiérarchie du tableau d'origines ──────────────────────────────────
# Pas l'ordre des étiquettes : l'ACTION que chacune appelle. On balaie
# pour savoir quoi faire, pas pour lire une taxonomie.
RANGS_COTES = [
    (1, "À traiter", "r1",
     "un défaut, ou une valeur encore absente"),
    (2, "Emprunté", "r2",
     "vient de ToddlerBot — porte le risque de licence"),
    (3, "Établi", "r3",
     "sourcé : rien à en faire"),
]

# Ce qu'exige chaque niveau. DESSINER et COUPER PROPREMENT ne demandent
# pas les mêmes valeurs — un DXF dessinable mais non coupable a l'air
# complet, et c'est précisément le piège.
CLES_DESSIN = ("epaisseur", "rayon_interieur_min")
CLES_COUPE = ("saignee", "voile_min")


def rang_cote(c) -> int:
    o = c.get("origine") or "non_qualifie"
    if o in ("non_qualifie", "ambigu"):
        return 1
    if o == "mesure" and not c.get("source"):
        return 1
    if o == "amont":
        return 2
    return 3


def _manque(p: dict, cles, prefixe="") -> list:
    """Ce qui MANQUE, quelle qu'en soit la raison.

    Piège écarté ici : « à mesurer » et « manquant » ne sont pas la même
    chose. Le rayon intérieur minimal de la découpe métal se déduira du
    moyen — il n'est donc pas à MESURER — mais il manque quand même, et
    sans lui on ne peut pas dessiner. Le confondre avec « rien à faire »
    ferait afficher « dessinable » une pièce qu'on ne peut pas dessiner.

    Seul `sans_objet` sort de la liste : là, il n'y a rien, pas même en
    attente.
    """
    out = []
    for k in cles:
        if p.get(k) is not None:
            continue
        st = NU.etat(REGLES_NUL.get("hardware.yaml", []), f"{prefixe}{k}", p)
        if st["etat"] != NU.SANS_OBJET:
            out.append((k, st["etat"]))
    return out


def etat_procede(p: dict, nom: str = "*") -> dict:
    """Deux niveaux, jamais un voyant unique."""
    pre = f"procedes.{nom}."
    md = _manque(p, CLES_DESSIN, pre)
    mc = _manque(p, CLES_COUPE, pre)
    if p.get("machine") is None:
        mc.insert(0, ("machine", NU.A_MESURER))
    return dict(dessinable=not md, coupable=not (md or mc),
                manque_dessin=md, manque_coupe=md + mc)


def e(x) -> str:
    return html.escape(str(x), quote=True)


def val(x, unite="", ind=INDET, regles=None, cle="", voisines=None) -> str:
    """Jamais une case vide : une valeur absente se DIT, et dit pourquoi.

    Sans `regles`, on retombe sur « non déterminé » — le défaut de la
    fiche 0020 : l'absence de déclaration ressort en rouge.
    """
    if not (x is None or x == "" or x == "null"):
        return f"{e(x)}{unite}"
    if regles is None:
        return ind
    st = NU.etat(regles, cle, voisines or {})
    return nul(st["etat"], st["parce_que"])


# ──────────────────────────────────────────────────── exécution des pièces
def executer_pieces() -> list[str]:
    """Exécute chaque parts/*.py dans CE processus. Renvoie les échecs."""
    scripts = sorted(p for p in PARTS.glob("*.py") if not p.name.startswith("_"))
    echecs = []
    if not scripts:
        print("  aucune pièce dans parts/")
        return echecs
    sys.path.insert(0, str(REPO / "scripts"))
    for s in scripts:
        print(f"  · {s.name}", end=" ", flush=True)
        try:
            spec = importlib.util.spec_from_file_location(f"piece_{s.stem}", s)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            code = mod.main([]) if hasattr(mod, "main") else 0
            print("ok" if code == 0 else f"code {code}")
            if code != 0:
                echecs.append(s.name)
        except Exception:
            print("ÉCHEC")
            traceback.print_exc(limit=3)
            echecs.append(s.name)
    return echecs


def lire_releves() -> list[dict]:
    pieces = []
    for f in sorted(PARTS.glob("*.origines.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        p = d.get("piece") or {}
        if not p.get("nom"):
            print(f"  ⚠ {f.name} sans bloc `piece:` — ignoré")
            continue
        p["cotes"] = d.get("cotes") or []
        p["_schema"] = ordonner_cotes(d.get("cotes_schema") or [])
        p["fichiers"] = {}
        base = p.get("base_fichier", p["nom"])
        for ext, _, _ in FORMATS:
            src = EXPORTS / (f"{base}_planA4.pdf" if ext == "pdf" else f"{base}.{ext}")
            if src.exists():
                p["fichiers"][ext] = src
        pieces.append(p)
    return pieces


# ────────────────────────────────────────────────────────────── gabarits
ECHECS: list[str] = []      # rempli avant la construction du site


def bandeau() -> str:
    """Si l'on publie malgré un échec, la page doit le CRIER.

    Un site amputé qui se tait ment par omission. Celui-ci nomme ce qui
    manque, sur chaque page, en rouge, avant tout autre contenu.
    """
    if not ECHECS:
        return ""
    lst = ", ".join(f"<code>{e(x)}</code>" for x in ECHECS)
    return (f'<div class="alerte"><b>SITE INCOMPLET — {len(ECHECS)} pièce(s) '
            f"n'ont pas pu être produites :</b> {lst}. "
            "Elles ne figurent nulle part sur ce site. Les autres pages sont à jour, "
            "mais <b>cet inventaire n'est pas complet</b>.</div>")


def ecourter(txt: str, n: int = 240) -> str:
    """Coupe sur une frontière de MOT, jamais au milieu.

    Le site affichait « un paramètre d'épaisseur, u ». Un texte coupé en
    plein mot se lit comme un bogue — et c'en était un.
    """
    txt = " ".join(str(txt).split())
    if len(txt) <= n:
        return txt
    return txt[:n].rsplit(" ", 1)[0].rstrip(" ,;:.") + "…"


def page(titre, corps, fil=None, cls="") -> str:
    nav = ('<nav><a href="/">Pièces</a><a href="/etat/">État du projet</a>'
           '<a href="/tracabilite/">Traçabilité</a></nav>')
    return f"""<!doctype html><html lang="fr"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(titre)} — YXOR</title><link rel="stylesheet" href="/assets/style.css">
</head><body><header><div class="wrap">
<h1>{e(titre)}</h1><p class="sous">{fil or 'YXOR — robot humanoïde bipède paramétrique'}</p>
{nav}</div></header><div class="wrap {cls}">{bandeau()}{corps}
<footer>Site engendré depuis le dépôt YXOR le {datetime.date.today().isoformat()}.
Il ne contient aucune donnée propre : chaque valeur vient d'un fichier du dépôt.
Régénérer&nbsp;: <code>python scripts/regenerer.py</code></footer>
</div></body></html>"""


def badge(origine) -> str:
    lib, _ = LIB_ORIGINE.get(origine, (origine, ""))
    cls = origine if origine in ORIGINES else "manque"
    return f'<span class="badge b-{cls}">{e(lib)}</span>'


def table_schema(cotes_schema, cotes_origine) -> str:
    """Tableau lettré, dans l'ordre de lecture du schéma.

    Chaque lettre du dessin est une ligne du tableau : c'est le lien
    direct entre la forme et la valeur, sans légende ni renvoi.
    """
    if not cotes_schema:
        return ""
    # La pièce DÉCLARE la clé de chaque cote : on ne devine rien d'après le
    # libellé. Une clé absente du relevé s'affiche comme un manque visible.
    par_cle = {str(c.get("cle", "")): c for c in cotes_origine}
    lignes = []
    for c in cotes_schema:
        src = par_cle.get(str(c.get("cle", "")))
        o, cle = (src or {}).get("origine"), c.get("cle", "")
        lignes.append(
            f'<tr><td class="lettre">{e(c["lettre"])}</td>'
            f'<td>{e(c.get("libelle", ""))}<br><span class="src">'
            f'<code>{e(cle)}</code></span></td>'
            f'<td class="num">{val(c.get("valeur"), " mm")}</td>'
            f'<td>{badge(o) if o else badge("non_qualifie")}</td></tr>')
    return ('<div class="defile"><table class="schema">'
            "<thead><tr><th></th><th>Cote</th>"
            "<th>Valeur</th><th>Origine</th></tr></thead><tbody>"
            + "".join(lignes) + "</tbody></table></div>")


def table_cotes(cotes) -> str:
    if not cotes:
        return '<p class="src">Aucune cote relevée.</p>'
    lignes = []
    for c in cotes:
        o = c.get("origine") or "non_qualifie"
        n = c.get("nature") or "sans_objet"
        lignes.append(
            f"<tr><td><code>{e(c.get('cle'))}</code></td>"
            f'<td class="num">{val(c.get("valeur"))}</td>'
            f"<td>{badge(o)}</td>"
            f'<td class="nat">{e(LIB_NATURE.get(n, n))}</td>'
            f'<td class="src">{val(c.get("source"), ind="<span class=\'ind\'>source absente</span>")}</td></tr>')
    return ('<div class="defile"><table><thead><tr><th>Cote</th>'
            "<th>Valeur</th><th>Origine</th>"
            "<th>Nature</th><th>Source</th></tr></thead><tbody>"
            + "".join(lignes) + "</tbody></table></div>")


def legende() -> str:
    items = "".join(f"<div>{badge(o)} <span class=\"src\">{e(LIB_ORIGINE[o][1])}</span></div>"
                    for o in ORIGINES)
    return f'<div class="grille" style="gap:7px;margin-top:14px">{items}</div>'


def bloc_rangs(cotes) -> str:
    """Trois rangs, rails colorés, compte dans le titre.

    Un rang VIDE reste affiché avec « 0 cote ». Un rang absent se lirait
    « sans objet » ; un rang à zéro se lit « rien à traiter » — et c'est
    l'information qu'on veut voir en premier.
    """
    out = []
    for num, titre, cls, desc in RANGS_COTES:
        sel = [c for c in cotes if rang_cote(c) == num]
        n = len(sel)
        # Le rang 1 à zéro n'est pas un vide : c'est un RÉSULTAT. Il garde
        # son rail, qui passe au vert, et le dit en toutes lettres. Un rang
        # qui s'effacerait en devenant vide effacerait la bonne nouvelle.
        quitte = num == 1 and not sel
        corps = table_cotes(sel) if sel else (
            '<p class="vide">Rien à traiter : aucune cote en défaut, '
            "aucune valeur absente.</p>" if quitte else
            '<p class="vide">Rien dans ce rang.</p>')
        ouvert = " open" if (num <= 2 or not sel) else ""
        out.append(
            f'<details class="rang {cls}{" quitte" if quitte else ""}"{ouvert}>'
            f'<summary>'
            f'<span class="rnum">{num}</span>'
            f"<span class=\"rtitre\">{e(titre)}</span>"
            f'<span class="rcpt">{n} cote{"s" if n > 1 else ""}</span>'
            f'<span class="rdesc">{e(desc)}</span>'
            f"</summary>{corps}</details>")
    return "".join(out)


def page_piece(p) -> str:
    dl = "".join(
        f'<a href="/fichiers/{e(f.name)}" download>{e(lib)}'
        f'<span class="fmt">{e(desc)}</span></a>'
        for ext, lib, desc in FORMATS if (f := p["fichiers"].get(ext)))
    amont = sum(1 for c in p["cotes"] if c.get("origine") == "amont")
    note = (f'<div class="note"><b>{amont} cote(s) d\'origine amont.</b> '
            "Elles viennent de ToddlerBot, dont la mécanique est publiée en licence "
            "non commerciale. Inventaire, pas avis juridique — fiche 0010.</div>"
            if amont else "")
    ep = etat_procede(p.get("_procede") or {})
    voyant = (f'<span class="v {"ok" if ep["dessinable"] else "no"}">'
              f'{"dessinable" if ep["dessinable"] else "non dessinable"}</span> '
              f'<span class="v {"ok" if ep["coupable"] else "no"}">'
              f'{"coupable" if ep["coupable"] else "non coupable"}</span>')
    return page(p.get("titre") or p["nom"], f"""
<div class="specs">
  <span><b>{val(p.get('materiau'))}</b> {val(p.get('epaisseur_mm'),' mm')}</span>
  <span>{val(p.get('machine'))}</span>
  <span>{val(p.get('longueur_mm'))} × {val(p.get('largeur_mm'))} mm</span>
  <span>{voyant}</span>
</div>

<div class="grille g2">
  <div class="carte">
    <h2 style="margin-top:0">Schéma coté</h2>
    <div class="svgbox">{svg_schema(p["_contours"], p["_schema"])}</div>
    {table_schema(p["_schema"], p["cotes"])}
  </div>
  <div class="carte">
    <h2 style="margin-top:0">Géométrie</h2>
    <canvas id="vue"></canvas>
    <div class="msg" id="msg">Chargement…</div>
    <p class="src">Glisser pour tourner, molette pour zoomer. Le STL est ce que
    le navigateur affiche ; le STEP reste l'échange.</p>
    <h2>Téléchargements</h2><div class="dl">{dl or '<p class="src">Aucun.</p>'}</div>
    <p style="margin-top:12px"><a href="/atelier/{e(p['nom'])}/">Fiche atelier →</a></p>
  </div>
</div>

<h2>D'où vient chaque cote</h2>
<p class="sous">Rangées par ce qu'elles appellent à faire, non par étiquette.</p>
{note}
{bloc_rangs(p["cotes"])}
{legende()}

<h2>Fabrication</h2>
<div class="carte"><div class="defile"><table><tbody>
  <tr><th>Matériau</th><td class="num">{val(p.get('materiau'))}</td></tr>
  <tr><th>Machine</th><td class="num">{val(p.get('machine'))}</td></tr>
  <tr><th>Lieu</th><td class="num">{val(p.get('lieu'))}</td></tr>
  <tr><th>Saignée</th><td class="num">{val(p.get('saignee_mm'),' mm')}</td></tr>
  <tr><th>Voile minimal</th><td class="num">{val(p.get('voile_min_mm'),' mm')}</td></tr>
  <tr><th>Fixation</th><td class="num">{val(p.get('fixation'))}</td></tr>
  <tr><th>Anisotrope</th><td class="num">{'oui' if p.get('anisotrope') else 'non'}</td></tr>
  <tr><th>Cannelures</th><td class="num">{val(
      p.get('orientation_cannelures_deg'), '°',
      regles=REGLES_NUL.get('piece', []),
      cle='orientation_cannelures_deg', voisines=p)}</td></tr>
  <tr><th>Palier</th><td class="num">{val(p.get('palier'))}</td></tr>
  <tr><th>Volume</th><td class="num">{val(p.get('volume_mm3'),' mm³')}</td></tr>
</tbody></table></div></div>
<script src="/assets/viewer.js"></script>
<script>visualiseurSTL(document.getElementById('vue'),
  {json.dumps('/fichiers/' + p["fichiers"]["stl"].name) if 'stl' in p["fichiers"] else 'null'},
  m => document.getElementById('msg').textContent = m || '');</script>
""", fil=e(ecourter(p.get("role", ""))))


def page_atelier(p) -> str:
    dxf = p["fichiers"].get("dxf")
    ep = etat_procede(p.get("_procede") or {})
    # La distinction dessinable / coupable doit être ICI aussi : c'est la
    # page que l'opérateur ouvre, et c'est là que la confondre coûterait
    # une pièce ratée.
    if ep["coupable"]:
        verdict = ('<div class="ok-bloc"><b>Prêt à couper.</b> '
                   "Toutes les valeurs du procédé sont renseignées.</div>")
    else:
        manque = ", ".join(e(m.replace("_", " ")) for m, _ in ep["manque_coupe"])
        verdict = (f'<div class="att"><b>NE PAS COUPER ENCORE.</b><br>'
                   f"Le dessin est juste, mais il manque : <b>{manque}</b>.<br>"
                   "Ces valeurs ne sont pas « sans objet » : elles sont à mesurer. "
                   "Un fichier dessinable n\'est pas un fichier coupable.</div>")
    # Le verdict passe EN TÊTE : il doit être lu avant les cotes, pas après.
    return page(p.get("titre") or p["nom"], f"""
{verdict}
<div class="bloc">
  <p class="lbl">Matière</p><p class="spec"><b>{val(p.get('materiau'))}</b></p>
  <p class="lbl">Épaisseur</p><p class="spec"><b>{val(p.get('epaisseur_mm'),' mm')}</b></p>
  <p class="lbl">Outil</p><p class="spec">{val(p.get('machine'))}</p>
</div>
<div class="bloc">
  <p class="lbl">Dimensions hors-tout</p>
  <p class="spec"><b>{val(p.get('longueur_mm'))} × {val(p.get('largeur_mm'))}</b> mm</p>
  <p class="lbl">Rayon minimal dans les angles rentrants</p>
  <p class="spec"><b>{val(p.get('rayon_interieur_min_mm'),' mm')}</b></p>
  <p class="lbl" style="margin-top:14px">Aucun angle vif rentrant.
  Contour fermé, échelle 1:1.</p>
</div>
{'<div class="bloc"><p class="lbl">Sens des cannelures</p><p class="spec"><b>'
 + val(p.get('orientation_cannelures_deg'),'°') +
 '</b> par rapport à la longueur</p><p class="lbl">Matière ORIENTÉE : la flèche '
 'du plan A4 doit être alignée avant de couper.</p></div>'
 if p.get('anisotrope') else ''}
{f'<a class="gros" href="/fichiers/{e(dxf.name)}" download>Télécharger le DXF</a>' if dxf
  else '<div class="att">Pas de DXF disponible.</div>'}
<div class="bloc"><p class="lbl">Fixation prévue</p>
<p class="spec">{val(p.get('fixation'))}</p></div>
<p style="margin-top:20px"><a href="/piece/{e(p['nom'])}/">← Fiche complète</a></p>
""", fil="Fiche atelier — découpe", cls="atelier")


def page_index(pieces, audit) -> str:
    items = "".join(f"""<li data-t="{e((p.get('titre','') + ' ' + p['nom'] + ' ' +
        str(p.get('materiau',''))).lower())}">
      <div class="t"><a href="/piece/{e(p['nom'])}/">{e(p.get('titre') or p['nom'])}</a></div>
      <div class="m">{val(p.get('materiau'))} · {val(p.get('epaisseur_mm'),' mm')} ·
        {val(p.get('longueur_mm'))} × {val(p.get('largeur_mm'))} mm ·
        <a href="/atelier/{e(p['nom'])}/">vue atelier</a></div></li>""" for p in pieces)
    n = len(pieces)
    return page("Pièces", f"""
<p class="sous">{n} pièce{'s' if n > 1 else ''} engendrée{'s' if n > 1 else ''} depuis le dépôt.</p>
<input type="search" id="q" placeholder="Filtrer…" autocomplete="off">
<ul class="pieces" id="liste">{items or '<li>Aucune pièce.</li>'}</ul>
<script>
const q=document.getElementById('q'), li=[...document.querySelectorAll('#liste li')];
q.addEventListener('input',()=>{{const v=q.value.trim().toLowerCase();
  li.forEach(x=>x.hidden = v && !(x.dataset.t||'').includes(v));}});
</script>
<h2>Où en est le projet</h2>
<p class="sous">{audit['total']} valeurs inventoriées, dont
{audit['origines'].get('amont', 0)} d'origine amont.</p>
<p><a href="/etat/">État du projet — ce qu'il reste à faire →</a></p>
<p><a href="/tracabilite/">Traçabilité des cotes →</a></p>""")


def page_tracabilite(audit) -> str:
    total = max(audit["total"], 1)
    segs = "".join(
        f'<div style="width:{100*audit["origines"].get(o,0)/total:.3f}%;'
        f'background:var(--o-{o})"></div>' for o in ORIGINES if audit["origines"].get(o))
    lignes = "".join(
        f"<tr><td>{badge(o)}</td><td class='num'>{n}</td>"
        f"<td class='num'>{100*n/total:.1f} %</td>"
        f"<td class='src'>{e(LIB_ORIGINE.get(o,(o,''))[1])}</td></tr>"
        for o, n in sorted(audit["origines"].items(), key=lambda kv: -kv[1]))
    nat = "".join(f"<tr><td>{e(LIB_NATURE.get(k,k))}</td><td class='num'>{v}</td></tr>"
                  for k, v in sorted(audit["natures"].items(), key=lambda kv: -kv[1]))
    return page("Traçabilité des cotes", f"""
<p class="sous">Toute cote du projet porte une origine — d'où vient le nombre — et une
nature — ce qui le détermine. Cet inventaire ne dit pas ce qu'il faut en conclure.</p>
<div class="barre">{segs}</div>
<div class="carte"><div class="defile"><table><thead><tr><th>Origine</th><th>Valeurs</th><th>Part</th>
<th>Définition</th></tr></thead><tbody>{lignes}</tbody></table></div></div>
<h2>Par nature</h2>
<div class="carte"><div class="defile"><table><tbody>{nat}</tbody></table></div></div>
<div class="note">Les cotes d'origine <b>amont</b> viennent de ToddlerBot, dont la mécanique
est publiée en licence non commerciale. Leur inventaire est un fait, pas un avis juridique.</div>""")


def page_etat(pieces, audit, hw, an, jo) -> str:
    # Tout est DÉRIVÉ : les null de hardware.yaml, les verifie:false de
    # anthropometry.yaml, les confiance de joints.yaml. Rien n'est saisi,
    # donc rien ne peut se désynchroniser.
    lignes = []
    for nom, pr in hw["procedes"].items():
        st = etat_procede(pr, nom)
        manque = ", ".join(
            f'<span class="{NU.CLS[et]}">{e(m.replace("_", " "))}</span>'
            for m, et in st["manque_coupe"]) or "—"
        lignes.append(
            f"<tr><td><code>{e(nom)}</code></td>"
            f'<td class="num">{val(pr.get("materiau"))}</td>'
            f'<td class="num"><span class="v {"ok" if st["dessinable"] else "no"}">'
            f'{"oui" if st["dessinable"] else "non"}</span></td>'
            f'<td class="num"><span class="v {"ok" if st["coupable"] else "no"}">'
            f'{"oui" if st["coupable"] else "non"}</span></td>'
            f'<td class="src">{manque}</td></tr>')

    # Le tri se fait sur la DÉCLARATION de la fiche 0020, plus sur le
    # préfixe du nom de la clé. L'ancien filtre triait juste pour la
    # mauvaise raison, et aurait laissé passer tout champ de prose
    # nommé autrement.
    par_etat = {NU.A_MESURER: {}, NU.SE_DEDUIRA: {}}
    for fam in ("procedes", "materiaux"):
        for nom, d in hw[fam].items():
            for k, v in d.items():
                if v is not None:
                    continue
                st = NU.etat(REGLES_NUL.get("hardware.yaml", []),
                             f"{fam}.{nom}.{k}", d)
                if st["etat"] == NU.SANS_OBJET:
                    continue
                # Groupé par (clé, motif) : deux champs de même nom
                # peuvent être absents pour des raisons DIFFÉRENTES. Le
                # rayon intérieur minimal se déduit de l'épaisseur au
                # cutter, du moyen de découpe au métal. Les fondre
                # afficherait la mauvaise raison pour l'un des deux.
                g = (k, st["parce_que"])
                par_etat[st["etat"]].setdefault(g, []).append(f"{fam}.{nom}")

    def tableau(grp, avec_motif=False):
        return "".join(
            f"<tr><td><code>{e(k)}</code></td><td class='num'>{len(v)}</td>"
            + (f"<td class='src'>{prose(m)}</td>" if avec_motif else "")
            + f"<td class='src'>{e(', '.join(v))}</td></tr>"
            for (k, m), v in sorted(grp.items(), key=lambda kv: (-len(kv[1]), kv[0])))

    amesurer = [c for v in par_etat[NU.A_MESURER].values() for c in v]
    deduites = [c for v in par_etat[NU.SE_DEDUIRA].values() for c in v]
    lm = tableau(par_etat[NU.A_MESURER])
    ld = tableau(par_etat[NU.SE_DEDUIRA], avec_motif=True)

    nv = [k for k, v in an["ratios"].items()
          if isinstance(v, dict) and v.get("verifie") is False]
    conf = {}
    for g in ("jambes", "bras", "taille", "nuque"):
        for j in jo.get(g, []):
            c = (j.get("materiel") or {}).get("confiance", "?")
            conf[c] = conf.get(c, 0) + 1
    lc = "".join(f"<tr><td>{badge('propre' if k=='documentee' else 'ambigu')} "
                 f"<code>{e(k)}</code></td><td class='num'>{v}</td></tr>"
                 for k, v in sorted(conf.items(), key=lambda kv: -kv[1]))

    return page("État du projet", f"""
<p class="sous">Entièrement dérivé du dépôt : aucune de ces lignes n'est saisie.</p>

<h2>Ce que je peux faire aujourd'hui</h2>
<p class="sous">Dessiner et couper proprement n'exigent pas les mêmes valeurs.
Un fichier dessinable mais non coupable a l'air complet : c'est le piège.</p>
<div class="carte"><div class="defile"><table><thead><tr><th>Procédé</th><th>Matériau</th>
<th>Dessiner</th><th>Couper</th><th>Manque pour couper</th></tr></thead>
<tbody>{"".join(lignes)}</tbody></table></div></div>

<h2>À mesurer <span class="cpt">{len(amesurer)} valeurs</span></h2>
<p class="sous">Rien ne les empêche : personne ne les a relevées.</p>
<div class="carte"><div class="defile"><table><thead><tr><th>Clé</th>
<th>Nombre</th><th>Où</th></tr></thead><tbody>{lm}</tbody></table></div></div>

<h2>Se déduira <span class="cpt">{len(deduites)} valeurs</span></h2>
<p class="sous">Absentes, mais <b>pas à mesurer</b> : elles dérivent d'un
autre champ, lui-même absent. Les compter avec les précédentes gonflerait
le travail restant de {round(100 * len(deduites) / max(1, len(amesurer) + len(deduites)))} %.</p>
<div class="carte"><div class="defile"><table><thead><tr><th>Clé</th>
<th>Nombre</th><th>Pourquoi</th><th>Où</th></tr></thead>
<tbody>{ld}</tbody></table></div></div>

<h2>Non vérifié <span class="cpt">{len(nv)} sur {len(an['ratios'])}</span></h2>
<div class="carte"><p class="src">Ratios de <code>anthropometry.yaml</code> dont
l'attribution est établie mais <b>dont les valeurs n'ont pas pu être confrontées
à la source</b> : la figure 4.1 de Winter est un graphique, aucun de ces nombres
n'apparaît dans le texte.</p>
<p class="src"><code>{e(', '.join(nv))}</code></p></div>

<h2>Confiance sur le matériel amont</h2>
<div class="carte"><div class="defile"><table><tbody>{lc}</tbody></table></div>
<p class="src" style="margin-top:10px">Le MJCF <b>représente</b>, il ne
<b>décrit</b> pas. Une confiance déduite du modèle n'est pas une source
matérielle.</p></div>

<h2>Traçabilité</h2>
<div class="carte"><p class="src">{audit['total']} valeurs inventoriées,
dont <b>{audit['origines'].get('amont', 0)}</b> d'origine amont.
<a href="/tracabilite/">Détail →</a></p></div>
""")


def lancer_audit() -> dict:
    sys.path.insert(0, str(REPO / "scripts"))
    import audit_origines as A
    cotes = []
    for s in A.SOURCES:
        if s.disponible():
            cotes += s.cotes()
    o, n = {}, {}
    for c in cotes:
        k = c.get("origine") or "non_qualifie"
        o[k] = o.get(k, 0) + 1
        k2 = c.get("nature") or "non déclarée"
        n[k2] = n.get(k2, 0) + 1
    return {"total": len(cotes), "origines": o, "natures": n}


BALISES_VIDES = {"meta", "link", "br", "hr", "img", "input", "source"}


def controler_html() -> list[str]:
    """Vérifie que les balises se referment, et dans l'ordre.

    Motif : un `div` laissé ouvert fait remonter tout ce qui suit dans le
    conteneur précédent — c'est ainsi que la vue 3D s'est retrouvée
    par-dessus le tableau des origines, sur mobile, le 2026-09-29. Le
    navigateur ne proteste pas : il referme silencieusement et affiche
    une page fausse.

    Ce contrôle ne remplace PAS un écran. Il attrape les fautes de
    STRUCTURE, pas celles de mise en page : une colonne trop large ou un
    texte illisible passeront toujours. C'est la limite de la règle 6,
    et elle est là.
    """
    defauts = []
    for f in sorted(SITE.rglob("*.html")):
        t = re.sub(r"<(script|style|svg)\b.*?</\1>", "",
                   f.read_text(encoding="utf-8"), flags=re.S)
        pile = []
        for m in re.finditer(r"<(/?)([a-zA-Z][\w-]*)([^>]*)>", t):
            fin, nom, reste = m.group(1), m.group(2).lower(), m.group(3)
            if nom in BALISES_VIDES or reste.rstrip().endswith("/"):
                continue
            if not fin:
                pile.append(nom)
            elif pile and pile[-1] == nom:
                pile.pop()
            else:
                defauts.append(f"{f.relative_to(SITE)} : </{nom}> inattendu")
                break
        else:
            if pile:
                defauts.append(f"{f.relative_to(SITE)} : jamais fermé — "
                               + ", ".join(f"<{b}>" for b in pile))
    return defauts


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--site-seulement", action="store_true",
                    help="ne pas réexécuter les pièces")
    ap.add_argument("--tolerer-echecs", action="store_true",
                    help="publier malgré une pièce en échec ; chaque page portera "
                         "alors un bandeau rouge nommant ce qui manque")
    a = ap.parse_args(argv)

    t0 = datetime.datetime.now()
    echecs = []
    if not a.site_seulement:
        print("1. Régénération des pièces (build123d importé une seule fois)")
        echecs = executer_pieces()
    else:
        print("1. Pièces non réexécutées (--site-seulement)")

    # ── ÉCHEC DUR PAR DÉFAUT, et voici pourquoi ──────────────────────
    # Une construction Docker qui échoue ne met pas le site hors ligne :
    # Coolify laisse tourner le conteneur précédent. Échouer dur ne coûte
    # donc AUCUNE disponibilité — et évite de remplacer un site juste par
    # un site amputé qui se tait. C'est le contraire d'un compromis.
    # `--tolerer-echecs` publie quand même, mais alors chaque page crie
    # ce qui manque : on ne publie jamais une omission silencieuse.
    if echecs and not a.tolerer_echecs:
        print(f"\n✗ ARRÊT : {len(echecs)} pièce(s) en échec — {', '.join(echecs)}")
        print("  Le site n'est PAS reconstruit. Le déploiement précédent reste en ligne.")
        print("  Pour publier malgré tout : --tolerer-echecs (bandeau rouge sur chaque page).")
        return 1
    ECHECS[:] = echecs

    print("\n2. Lecture des relevés")
    pieces = lire_releves()
    print(f"   {len(pieces)} pièce(s)")

    print("\n3. Audit d'origine")
    audit = lancer_audit()
    print(f"   {audit['total']} valeurs — " +
          ", ".join(f"{k} {v}" for k, v in sorted(audit["origines"].items(), key=lambda x: -x[1])))

    # contours et procédé : lus une fois, pour le schéma et les voyants
    hw = yaml.safe_load((REPO / "params/hardware.yaml").read_text("utf-8"))
    an = yaml.safe_load((REPO / "params/anthropometry.yaml").read_text("utf-8"))
    jo = yaml.safe_load((REPO / "params/joints.yaml").read_text("utf-8"))
    import build123d as _bd
    for p in pieces:
        p["_procede"] = hw["procedes"].get(p.get("procede"), {})
        p["_contours"] = []
        st = p["fichiers"].get("step")
        if st:
            try:
                f = _bd.import_step(str(st)).faces().sort_by(_bd.Axis.Z)[0]
                p["_contours"] = polylignes_depuis_face(f)
            except Exception as err:
                print(f"   ⚠ contours illisibles pour {p['nom']} : {err}")

    print("\n4. Construction du site")
    if SITE.exists():
        shutil.rmtree(SITE)
    (SITE / "assets").mkdir(parents=True)
    (SITE / "fichiers").mkdir()
    (SITE / "data").mkdir()
    for f in ("style.css", "viewer.js"):
        shutil.copy2(WEB / f, SITE / "assets" / f)

    for p in pieces:
        for f in p["fichiers"].values():
            shutil.copy2(f, SITE / "fichiers" / f.name)
        for dossier, gab in (("piece", page_piece), ("atelier", page_atelier)):
            d = SITE / dossier / p["nom"]
            d.mkdir(parents=True)
            (d / "index.html").write_text(gab(p), encoding="utf-8")

    (SITE / "index.html").write_text(page_index(pieces, audit), encoding="utf-8")
    (SITE / "etat").mkdir()
    (SITE / "etat" / "index.html").write_text(page_etat(pieces, audit, hw, an, jo),
                                              encoding="utf-8")
    (SITE / "tracabilite").mkdir()
    (SITE / "tracabilite" / "index.html").write_text(page_tracabilite(audit), encoding="utf-8")
    (SITE / "data" / "pieces.json").write_text(json.dumps(
        [{k: (str(v) if isinstance(v, Path) else
              {kk: str(vv) for kk, vv in v.items()} if k == "fichiers" else v)
          for k, v in p.items() if not k.startswith("_")} for p in pieces],
        ensure_ascii=False, indent=2), encoding="utf-8")
    (SITE / "data" / "audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2),
                                              encoding="utf-8")

    mal = controler_html()
    if mal:
        print("\n✗ STRUCTURE HTML INVALIDE :")
        for d in mal:
            print(f"   {d}")
        print("  Une balise non fermée déplace le contenu qui suit.")
        return 1
    print("   structure HTML : balises équilibrées sur toutes les pages")

    n_f = sum(1 for _ in SITE.rglob("*") if _.is_file())
    taille = sum(f.stat().st_size for f in SITE.rglob("*") if f.is_file())
    dt = (datetime.datetime.now() - t0).total_seconds()
    print(f"   {n_f} fichiers, {taille/1024:.0f} ko")
    print(f"\nTerminé en {dt:.1f} s.")
    if echecs:
        print(f"⚠ publié MALGRÉ {len(echecs)} échec(s) : {', '.join(echecs)}")
        print("  Chaque page porte un bandeau rouge les nommant.")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
