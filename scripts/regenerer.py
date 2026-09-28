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
import shutil
import sys
import traceback
from pathlib import Path

import yaml

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


def e(x) -> str:
    return html.escape(str(x), quote=True)


def val(x, unite="", ind=INDET) -> str:
    """Jamais une case vide : une valeur absente se DIT."""
    if x is None or x == "" or x == "null":
        return ind
    return f"{e(x)}{unite}"


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
        p["fichiers"] = {}
        base = p.get("base_fichier", p["nom"])
        for ext, _, _ in FORMATS:
            src = EXPORTS / (f"{base}_planA4.pdf" if ext == "pdf" else f"{base}.{ext}")
            if src.exists():
                p["fichiers"][ext] = src
        pieces.append(p)
    return pieces


# ────────────────────────────────────────────────────────────── gabarits
def page(titre, corps, fil=None, cls="") -> str:
    nav = ('<nav><a href="/">Pièces</a><a href="/tracabilite/">Traçabilité</a></nav>')
    return f"""<!doctype html><html lang="fr"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(titre)} — YXOR</title><link rel="stylesheet" href="/assets/style.css">
</head><body><header><div class="wrap">
<h1>{e(titre)}</h1><p class="sous">{fil or 'YXOR — robot humanoïde bipède paramétrique'}</p>
{nav}</div></header><div class="wrap {cls}">{corps}
<footer>Site engendré depuis le dépôt YXOR le {datetime.date.today().isoformat()}.
Il ne contient aucune donnée propre : chaque valeur vient d'un fichier du dépôt.
Régénérer&nbsp;: <code>python scripts/regenerer.py</code></footer>
</div></body></html>"""


def badge(origine) -> str:
    lib, _ = LIB_ORIGINE.get(origine, (origine, ""))
    cls = origine if origine in ORIGINES else "manque"
    return f'<span class="badge b-{cls}">{e(lib)}</span>'


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
    return ("<table><thead><tr><th>Cote</th><th>Valeur</th><th>Origine</th>"
            "<th>Nature</th><th>Source</th></tr></thead><tbody>"
            + "".join(lignes) + "</tbody></table>")


def legende() -> str:
    items = "".join(f"<div>{badge(o)} <span class=\"src\">{e(LIB_ORIGINE[o][1])}</span></div>"
                    for o in ORIGINES)
    return f'<div class="grille" style="gap:7px;margin-top:14px">{items}</div>'


def page_piece(p) -> str:
    dl = "".join(
        f'<a href="/fichiers/{e(f.name)}" download>{e(lib)}'
        f'<span class="fmt">{e(desc)}</span></a>'
        for ext, lib, desc in FORMATS if (f := p["fichiers"].get(ext)))
    compte = {}
    for c in p["cotes"]:
        o = c.get("origine") or "non_qualifie"
        compte[o] = compte.get(o, 0) + 1
    resume = " ".join(f"{badge(o)}&nbsp;{n}" for o, n in
                      sorted(compte.items(), key=lambda kv: -kv[1]))
    amont = compte.get("amont", 0)
    note = (f'<div class="note"><b>{amont} cote(s) d\'origine amont.</b> '
            "Elles viennent de ToddlerBot, dont la mécanique est publiée en licence "
            "non commerciale. Inventaire, pas avis juridique — voir la fiche 0010.</div>"
            if amont else "")
    return page(p.get("titre") or p["nom"], f"""
<h2>D'où vient chaque cote</h2>
<p class="sous">C'est le sujet de cette page. La géométrie vient après.</p>
<div class="rep" style="margin:10px 0 14px">{resume}</div>
{note}
<div class="carte">{table_cotes(p["cotes"])}{legende()}</div>

<div class="grille g2" style="margin-top:26px">
  <div class="carte">
    <h2 style="margin-top:0">Géométrie</h2>
    <canvas id="vue"></canvas>
    <div class="msg" id="msg">Chargement…</div>
    <p class="src">Glisser pour tourner, molette pour zoomer.
    Le STL est ce que le navigateur affiche ; le STEP reste l'échange.</p>
  </div>
  <div class="carte">
    <h2 style="margin-top:0">Fabrication</h2>
    <table><tbody>
      <tr><th>Hors-tout</th><td class="num">{val(p.get('longueur_mm'),' mm')} ×
          {val(p.get('largeur_mm'),' mm')} × {val(p.get('epaisseur_mm'),' mm')}</td></tr>
      <tr><th>Volume</th><td class="num">{val(p.get('volume_mm3'),' mm³')}</td></tr>
      <tr><th>Matériau</th><td class="num">{val(p.get('materiau'))}</td></tr>
      <tr><th>Machine</th><td class="num">{val(p.get('machine'))}</td></tr>
      <tr><th>Lieu</th><td class="num">{val(p.get('lieu'))}</td></tr>
      <tr><th>Rayon intérieur min.</th><td class="num">{val(p.get('rayon_interieur_min_mm'),' mm')}</td></tr>
      <tr><th>Saignée</th><td class="num">{val(p.get('saignee_mm'),' mm')}</td></tr>
      <tr><th>Voile minimal</th><td class="num">{val(p.get('voile_min_mm'),' mm')}</td></tr>
      <tr><th>Fixation</th><td class="num">{val(p.get('fixation'))}</td></tr>
      <tr><th>Palier</th><td class="num">{val(p.get('palier'))}</td></tr>
    </tbody></table>
    <h2>Téléchargements</h2><div class="dl">{dl or '<p class="src">Aucun fichier.</p>'}</div>
    <p style="margin-top:14px"><a href="/atelier/{e(p['nom'])}/">Vue atelier →</a></p>
  </div>
</div>
<script src="/assets/viewer.js"></script>
<script>visualiseurSTL(document.getElementById('vue'),
  {json.dumps('/fichiers/' + p["fichiers"]["stl"].name) if 'stl' in p["fichiers"] else 'null'},
  m => document.getElementById('msg').textContent = m || '');</script>
""", fil=e(p.get("role", "")).replace("\n", " ")[:160])


def page_atelier(p) -> str:
    dxf = p["fichiers"].get("dxf")
    manques = [lib for lib, v in
               [("la saignée", p.get("saignee_mm")), ("le voile minimal", p.get("voile_min_mm")),
                ("la machine", p.get("machine"))] if v in (None, "", "non déterminé")]
    att = (f'<div class="att"><b>À déterminer avant de couper :</b> {e(", ".join(manques))}. '
           "Ces valeurs ne sont pas connues — elles ne sont pas « sans objet », "
           "elles sont à mesurer.</div>" if manques else "")
    return page(p.get("titre") or p["nom"], f"""
<div class="bloc">
  <p class="lbl">Matière</p><p class="spec"><b>{val(p.get('materiau'))}</b></p>
  <p class="lbl">Épaisseur</p><p class="spec"><b>{val(p.get('epaisseur_mm'),' mm')}</b></p>
</div>
<div class="bloc">
  <p class="lbl">Dimensions hors-tout</p>
  <p class="spec"><b>{val(p.get('longueur_mm'))} × {val(p.get('largeur_mm'))}</b> mm</p>
  <p class="lbl">Rayon minimal dans les angles rentrants</p>
  <p class="spec"><b>{val(p.get('rayon_interieur_min_mm'),' mm')}</b></p>
  <p class="lbl" style="margin-top:14px">Aucun angle vif rentrant. Contour fermé, échelle 1:1.</p>
</div>
{att}
{f'<a class="gros" href="/fichiers/{e(dxf.name)}" download>Télécharger le DXF</a>' if dxf
  else '<div class="att">Pas de DXF disponible.</div>'}
<div class="bloc"><p class="lbl">Fixation prévue</p><p class="spec">{val(p.get('fixation'))}</p></div>
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
<h2>Traçabilité</h2>
<p class="sous">{audit['total']} valeurs inventoriées dans le dépôt.</p>
<a href="/tracabilite/">Voir le détail →</a>""")


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
<div class="carte"><table><thead><tr><th>Origine</th><th>Valeurs</th><th>Part</th>
<th>Définition</th></tr></thead><tbody>{lignes}</tbody></table></div>
<h2>Par nature</h2>
<div class="carte"><table><tbody>{nat}</tbody></table></div>
<div class="note">Les cotes d'origine <b>amont</b> viennent de ToddlerBot, dont la mécanique
est publiée en licence non commerciale. Leur inventaire est un fait, pas un avis juridique.</div>""")


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


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--site-seulement", action="store_true",
                    help="ne pas réexécuter les pièces")
    a = ap.parse_args(argv)

    t0 = datetime.datetime.now()
    echecs = []
    if not a.site_seulement:
        print("1. Régénération des pièces (build123d importé une seule fois)")
        echecs = executer_pieces()
    else:
        print("1. Pièces non réexécutées (--site-seulement)")

    print("\n2. Lecture des relevés")
    pieces = lire_releves()
    print(f"   {len(pieces)} pièce(s)")

    print("\n3. Audit d'origine")
    audit = lancer_audit()
    print(f"   {audit['total']} valeurs — " +
          ", ".join(f"{k} {v}" for k, v in sorted(audit["origines"].items(), key=lambda x: -x[1])))

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
    (SITE / "tracabilite").mkdir()
    (SITE / "tracabilite" / "index.html").write_text(page_tracabilite(audit), encoding="utf-8")
    (SITE / "data" / "pieces.json").write_text(json.dumps(
        [{k: (str(v) if isinstance(v, Path) else
              {kk: str(vv) for kk, vv in v.items()} if k == "fichiers" else v)
          for k, v in p.items()} for p in pieces],
        ensure_ascii=False, indent=2), encoding="utf-8")
    (SITE / "data" / "audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2),
                                              encoding="utf-8")

    n_f = sum(1 for _ in SITE.rglob("*") if _.is_file())
    taille = sum(f.stat().st_size for f in SITE.rglob("*") if f.is_file())
    dt = (datetime.datetime.now() - t0).total_seconds()
    print(f"   {n_f} fichiers, {taille/1024:.0f} ko")
    print(f"\nTerminé en {dt:.1f} s.")
    if echecs:
        print(f"⚠ pièces en échec : {', '.join(echecs)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
