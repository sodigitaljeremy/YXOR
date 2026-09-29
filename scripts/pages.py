#!/usr/bin/env python3
"""Gabarits du site — tout le HTML, et rien d'autre.

═══════════════════════════════════════════════════════════════════════
 POURQUOI CE FICHIER EXISTE
═══════════════════════════════════════════════════════════════════════

`regenerer.py` faisait 933 lignes, dont **62 % de gabarit HTML**. Ce
n'était pas un mélange de couches — sa structure restait linéaire — mais
le HTML et la logique partageaient la même relecture, et c'est la partie
qu'on relit le moins.

Un seul découpage, pas cinq (fiche 0024, § « ce que je ne recommande
pas ») : d'un côté ce qui produit des chaînes, de l'autre ce qui
orchestre et ce qui contrôle. Le verdict dessinable/coupable vient ici
parce qu'il n'est consommé que par des pages ; l'y laisser évite un
troisième module dont l'unique raison d'être serait de casser un cycle
d'imports.

Ce module ne lit aucun fichier de `params/` de sa propre initiative,
à deux exceptions déclarées en tête : les règles de nullité et le
document matériel, qu'il faut pour résoudre une condition à l'affichage.
"""
from __future__ import annotations

import datetime
import html
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SITE = REPO / "site"

sys.path.insert(0, str(REPO / "scripts"))
from plan_decoupe import ordonner_cotes, svg_schema  # noqa: E402,F401
import nullites as NU  # noqa: E402
import procedes as PROC  # noqa: E402

# `ECHECS` est renseigné par regenerer.py avant l'engendrement : le
# bandeau rouge des pages en dépend. Une liste, pas un import croisé.
ECHECS: list[str] = []


def commit() -> str:
    """L'empreinte du commit d'où ce site est engendré.

    En construction Docker : `YXOR_COMMIT`, passé par Coolify. En local :
    `git rev-parse`. Sinon « inconnu » — dit, jamais deviné.

    Sert à une chose : qu'un site périmé se reconnaisse. Le 2026-09-29,
    une construction a échoué quatre heures, l'ancien conteneur a continué
    de servir, et un plan de découpe faux a failli être coupé. La date
    seule ne suffit pas : elle est celle de la GÉNÉRATION, donc du dernier
    déploiement RÉUSSI, et un site périmé affiche une date plausible.
    """
    import os
    import subprocess
    v = os.environ.get("YXOR_COMMIT", "").strip()
    if v and v != "inconnu":
        return v
    try:
        r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                           capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            return r.stdout.strip()
    except Exception:
        pass
    return "inconnu"


COMMIT = commit()

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
REGLES_NUL = NU.charger()
# Document complet : les conditions `si: {chemin: ...}` de la fiche
# 0033 s'y résolvent, la machine n'étant plus une clé sœur.
HW_DOC = PROC.charger()
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
def _chemin_nul(r: dict, cle: str) -> str:
    """Le chemin RÉEL de la cote, dans les quatre tables.

    L'épaisseur vient de la matière, la saignée du réglage. Le chargeur
    les met à plat, mais les motifs de nullites.yaml visent la vraie
    table : se tromper ici ferait taire une règle sans que rien ne le
    dise — et la valeur ressortirait en rouge « à mesurer » alors qu'elle
    se déduit.
    """
    if cle in PROC.CLES_MATIERE:
        return f"matieres.{r.get('matiere')}.{cle}"
    return f"reglages.{r.get('id')}.{cle}"
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
        st = NU.etat(REGLES_NUL.get("hardware.yaml", []),
                     _chemin_nul(p, k), p, document=HW_DOC)
        if st["etat"] != NU.SANS_OBJET:
            out.append((k, st["etat"]))
    return out
def etat_procede(p: dict, nom: str = "*", besoins: list | None = None) -> dict:
    """Deux niveaux, jamais un voyant unique.

    Un réglage déclaré IMPOSSIBLE n'est ni dessinable ni coupable, et ce
    n'est pas un manque : c'est un fait. On le distingue par `impossible`.
    """
    if p.get("valide") is False:
        return dict(dessinable=False, coupable=False, impossible=True,
                    manque_dessin=[], manque_coupe=[])
    md = _manque(p, CLES_DESSIN)
    # Fiche 0037 : une pièce n'est bloquée que par ce dont ELLE a besoin.
    # Sans liste déclarée, on retombe sur l'ancien comportement — toutes
    # les cotes de coupe du réglage — pour qu'un relevé ancien ne devienne
    # pas coupable par le simple fait d'être muet.
    cles_coupe = CLES_COUPE if besoins is None else tuple(
        k for k in CLES_COUPE if k in besoins)
    mc = _manque(p, cles_coupe)
    if p.get("machine_nom") is None:
        mc.insert(0, ("moyen de découpe", NU.A_MESURER))
    return dict(dessinable=not md, coupable=not (md or mc), impossible=False,
                manque_dessin=md, manque_coupe=md + mc,
                sans_besoin=besoins is not None and not mc and bool(
                    _manque(p, CLES_COUPE)))
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
    st = NU.etat(regles, cle, voisines or {}, document=HW_DOC)
    return nul(st["etat"], st["parce_que"])
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
<footer>Site engendré depuis le dépôt YXOR le {datetime.date.today().isoformat()},
au commit <code class="sha">{e(COMMIT[:12])}</code>.
Comparer&nbsp;: <code>git rev-parse --short=12 HEAD</code>. S'ils diffèrent,
<b>cette page est périmée</b> — le déploiement a échoué et l'ancien
conteneur sert encore.
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
def repli(etiquette: str, contenu: str) -> str:
    """Le même contenu, replié SOUS la ligne au lieu d'être à côté.

    Sous 620 px, les colonnes de prose (nature, source, motif) quittent
    leur colonne et passent sous la valeur. Le tableau tombe à trois
    colonnes, donc dans l'écran, et RIEN n'est perdu : le texte est
    toujours là, ailleurs. C'est le seul compromis qui ne sacrifie ni la
    comparaison verticale — raison d'être d'un tableau de cotes — ni le
    contenu.
    """
    return (f'<span class="repli"><b>{e(etiquette)}</b> {contenu}</span>')
def table_cotes(cotes) -> str:
    if not cotes:
        return '<p class="src">Aucune cote relevée.</p>'
    lignes = []
    for c in cotes:
        o = c.get("origine") or "non_qualifie"
        n = c.get("nature") or "sans_objet"
        nat = e(LIB_NATURE.get(n, n))
        src = val(c.get("source"),
                  ind="<span class='ind'>source absente</span>")
        lignes.append(
            f"<tr><td><code>{e(c.get('cle'))}</code>"
            + repli("nature", nat) + repli("source", src) + "</td>"
            f'<td class="num">{val(c.get("valeur"))}</td>'
            f"<td>{badge(o)}</td>"
            f'<td class="nat pliable">{nat}</td>'
            f'<td class="src pliable">{src}</td></tr>')
    return ('<div class="defile"><table><thead><tr><th>Cote</th>'
            "<th>Valeur</th><th>Origine</th>"
            '<th class="pliable">Nature</th><th class="pliable">Source</th>'
            "</tr></thead><tbody>"
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
def cotes_ref(p) -> dict:
    """Les cotes de référence, telles que la pièce les a publiées.

    Elles servent à évaluer les repères du schéma, qui sont déclarés en
    coefficients et non en millimètres (fiche 0026).
    """
    return ((p.get("_simulation") or {}).get("reference") or {}).get("cotes") or {}
def bloc_simulation(p) -> str:
    """Le bac à sable : calculer n'est pas stocker (fiche 0023).

    La pièce publie ses paramètres réglables ET une référence calculée en
    Python. Le script de la page se contrôle contre elle au chargement et
    se désactive s'il ne la retrouve pas : sans navigateur ici, c'est la
    seule garde entre un portage faux et un dessin faux.
    """
    sim = p.get("_simulation")
    if not sim:
        return ""
    # `</` est échappé dans le JSON en ligne : une chaîne contenant
    # « </script> » refermerait la balise et livrerait le reste en HTML.
    # Rien n'en contient aujourd'hui ; c'est pour le jour où.
    # Le schéma lettré part avec la simulation : c'est lui qui porte les
    # repères, et c'est lui qui donne les lettres.
    sim = dict(sim, schema=p["_schema"])
    return (f"""
<h2>Simuler une autre taille</h2>
<p class="sous">Le dépôt reste la seule source de vérité. Rien de ce qui est
calculé ici n'est envoyé, ni stocké : recharger la page rend les valeurs du
dépôt. Pour figer une valeur, il faut modifier le dépôt et régénérer.</p>
<div class="carte" id="sim"><p class="src">Simulation indisponible :
JavaScript est désactivé. Les valeurs ci-dessus restent celles du dépôt.</p></div>
<script src="/assets/simulateur.js"></script>
<script>simulateur({json.dumps(sim, ensure_ascii=False).replace("</", "<\\/")},
  {{hote: document.getElementById('sim')}});</script>""")
def schema_ou_rien(p) -> str:
    """Le schéma, ou la raison de son absence — jamais une exception.

    En mode `--tolerer-echecs`, un relevé peut survivre à la pièce qui
    l'a produit : le fichier reste sur le disque, mais le contour n'a pas
    été recalculé. Faire planter l'engendrement ici viderait de son sens
    le mode qui existe pour publier malgré un échec.
    """
    if not p.get("_contours"):
        return ('<p class="ind" style="padding:22px">Schéma indisponible : '
                "la pièce n'a pas pu être exécutée lors de cette "
                "régénération. Les valeurs ci-dessous viennent du dernier "
                "relevé déposé et peuvent être périmées.</p>")
    return svg_schema(p["_contours"], p["_schema"], valeurs=cotes_ref(p))


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
    ep = etat_procede(p.get("_procede") or {},
                      besoins=p.get("besoins_procede"))
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
    <div class="svgbox">{schema_ou_rien(p)}</div>
    <p class="zoomaide">Pincer pour agrandir, glisser pour déplacer.
    C'est un dessin technique : il doit pouvoir être lu de près.</p>
    <script src="/assets/zoom.js"></script>
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

{bloc_simulation(p)}

<h2>D'où vient chaque cote</h2>
<p class="sous">Rangées par ce qu'elles appellent à faire, non par étiquette.</p>
{note}
{bloc_rangs(p["cotes"])}
{legende()}

<h2>Fabrication</h2>
<dl class="fiche">
  <dt>Matériau</dt><dd class="txt">{val(p.get('materiau'))}</dd>
  <dt>Machine</dt><dd class="txt">{val(p.get('machine'))}</dd>
  <dt>Lieu</dt><dd class="txt">{val(p.get('lieu'))}</dd>
  <dt>Saignée</dt><dd class="num">{val(p.get('saignee_mm'),' mm')}</dd>
  <dt>Voile minimal</dt><dd class="num">{val(p.get('voile_min_mm'),' mm')}</dd>
  <dt>Fixation</dt><dd class="txt">{val(p.get('fixation'))}</dd>
  <dt>Anisotrope</dt><dd class="txt">{'oui' if p.get('anisotrope') else 'non'}</dd>
  <dt>Cannelures</dt><dd class="txt">{val(
      p.get('orientation_cannelures_deg'), '°',
      regles=REGLES_NUL.get('piece', []),
      cle='orientation_cannelures_deg', voisines=p)}</dd>
  <dt>Palier</dt><dd class="txt">{val(p.get('palier'))}</dd>
  <dt>Volume</dt><dd class="num">{val(p.get('volume_mm3'),' mm³')}</dd>
</dl>
<script src="/assets/viewer.js"></script>
<script>visualiseurSTL(document.getElementById('vue'),
  {json.dumps('/fichiers/' + p["fichiers"]["stl"].name) if 'stl' in p["fichiers"] else 'null'},
  m => document.getElementById('msg').textContent = m || '');</script>
""", fil=e(ecourter(p.get("role", ""))))
def page_atelier(p) -> str:
    dxf = p["fichiers"].get("dxf")
    ep = etat_procede(p.get("_procede") or {},
                      besoins=p.get("besoins_procede"))
    # La distinction dessinable / coupable doit être ICI aussi : c'est la
    # page que l'opérateur ouvre, et c'est là que la confondre coûterait
    # une pièce ratée.
    if ep["coupable"] and ep.get("sans_besoin"):
        # Troisième cas (fiche 0037) : prêt MALGRÉ un réglage incomplet.
        # Il doit dire POURQUOI, sinon on croira à une régression du
        # contrôle — un verdict qui s'adoucit sans s'expliquer inquiète
        # à juste titre.
        manque = ", ".join(e(m.replace("_", " "))
                           for m, _ in _manque(p.get("_procede") or {}, CLES_COUPE))
        verdict = ('<div class="ok-bloc"><b>Prêt à couper.</b> '
                   f"Le procédé n'a pas toutes ses valeurs — il manque "
                   f"<b>{manque}</b> — mais <b>cette pièce ne s'en sert pas</b> : "
                   "elle ne s'emboîte avec rien, et n'a aucun voile étroit. "
                   "La saignée compte quand deux pièces s'ajustent ; ici, "
                   "couper sur le trait suffit.</div>")
    elif ep["coupable"]:
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
<div class="sha-atelier">
  <div class="sha-lbl">Version de ce plan</div>
  <div class="sha-val">{e(COMMIT[:12])}</div>
  <p>Comparer avec <code>git rev-parse --short=12 HEAD</code> avant de couper.
  <b>S'ils diffèrent, ce plan est périmé</b> : le déploiement a échoué et
  le site sert encore l'ancienne version. La date ne suffit pas à le dire —
  c'est celle du dernier déploiement <i>réussi</i>.</p>
</div>
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
        f"<tr><td>{badge(o)}"
        + repli("définition", e(LIB_ORIGINE.get(o, (o, ''))[1]))
        + f"</td><td class='num'>{n}</td>"
        f"<td class='num'>{100*n/total:.1f} %</td>"
        f"<td class='src pliable'>{e(LIB_ORIGINE.get(o,(o,''))[1])}</td></tr>"
        for o, n in sorted(audit["origines"].items(), key=lambda kv: -kv[1]))
    nat = "".join(f"<tr><td>{e(LIB_NATURE.get(k,k))}</td><td class='num'>{v}</td></tr>"
                  for k, v in sorted(audit["natures"].items(), key=lambda kv: -kv[1]))
    return page("Traçabilité des cotes", f"""
<p class="sous">Toute cote du projet porte une origine — d'où vient le nombre — et une
nature — ce qui le détermine. Cet inventaire ne dit pas ce qu'il faut en conclure.</p>
<div class="barre">{segs}</div>
<div class="carte"><div class="defile"><table><thead><tr><th>Origine</th><th>Valeurs</th><th>Part</th>
<th class="pliable">Définition</th></tr></thead><tbody>{lignes}</tbody></table></div></div>
<h2>Par nature</h2>
<div class="carte"><div class="defile"><table><tbody>{nat}</tbody></table></div></div>
<div class="note">Les cotes d'origine <b>amont</b> viennent de ToddlerBot, dont la mécanique
est publiée en licence non commerciale. Leur inventaire est un fait, pas un avis juridique.</div>""")
def page_etat(pieces, audit, hw, an, jo) -> str:
    # Tout est DÉRIVÉ : les null de hardware.yaml, les verifie:false de
    # anthropometry.yaml, les confiance de joints.yaml. Rien n'est saisi,
    # donc rien ne peut se désynchroniser.
    lignes = []
    for nom, pr in PROC.reglages(hw).items():
        st = etat_procede(pr, nom)
        manque = ", ".join(
            f'<span class="{NU.CLS[et]}">{e(m.replace("_", " "))}</span>'
            for m, et in st["manque_coupe"]) or "—"
        if st["impossible"]:
            # Ni dessinable ni coupable, mais ce n'est PAS un manque :
            # c'est un fait établi. L'afficher comme « non, non, — » le
            # ferait lire « incomplet », soit l'inverse de ce qu'on sait.
            motif = prose(" ".join((pr.get("motif") or "").split()))
            lignes.append(
                f"<tr><td><code>{e(nom)}</code>"
                + repli("matériau", val(pr.get("materiau")))
                + repli("pourquoi", motif) + "</td>"
                f'<td class="txt pliable">{val(pr.get("materiau"))}</td>'
                f'<td class="txt" colspan="2"><span class="so">impossible</span></td>'
                f'<td class="src pliable">{motif}</td></tr>')
            continue
        lignes.append(
            f"<tr><td><code>{e(nom)}</code>"
            + repli("matériau", val(pr.get("materiau")))
            + repli("manque", manque) + "</td>"
            f'<td class="txt pliable">{val(pr.get("materiau"))}</td>'
            f'<td class="txt"><span class="v {"ok" if st["dessinable"] else "no"}">'
            f'{"oui" if st["dessinable"] else "non"}</span></td>'
            f'<td class="txt"><span class="v {"ok" if st["coupable"] else "no"}">'
            f'{"oui" if st["coupable"] else "non"}</span></td>'
            f'<td class="src pliable">{manque}</td></tr>')

    # Le tri se fait sur la DÉCLARATION de la fiche 0020, plus sur le
    # préfixe du nom de la clé. L'ancien filtre triait juste pour la
    # mauvaise raison, et aurait laissé passer tout champ de prose
    # nommé autrement.
    par_etat = {NU.A_MESURER: {}, NU.SE_DEDUIRA: {}}
    # `reglages` est une LISTE indexée par un `id` écrit à la main
    # (fiche 0026) : elle ne se balaie pas comme les tables. L'oublier
    # ferait disparaître toutes les saignées du compte « à mesurer » —
    # le chiffre resterait affiché, simplement faux et rassurant.
    a_balayer = [(f, nom, d) for f in ("machines", "materiaux", "matieres")
                 for nom, d in (hw.get(f) or {}).items()]
    a_balayer += [("reglages", r["id"], r) for r in (hw.get("reglages") or [])]
    for fam, nom, d in a_balayer:
            for k, v in d.items():
                if v is not None:
                    continue
                st = NU.etat(REGLES_NUL.get("hardware.yaml", []),
                             f"{fam}.{nom}.{k}", d, document=hw)
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
            f"<tr><td><code>{e(k)}</code>"
            + (repli("pourquoi", prose(m)) if avec_motif else "")
            + repli("où", e(', '.join(v)))
            + f"</td><td class='num'>{len(v)}</td>"
            + (f"<td class='src pliable'>{prose(m)}</td>" if avec_motif else "")
            + f"<td class='src pliable'>{e(', '.join(v))}</td></tr>"
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
<div class="carte"><div class="defile"><table><thead><tr><th>Procédé</th>
<th class="pliable">Matériau</th>
<th>Dessiner</th><th>Couper</th><th class="pliable">Manque pour couper</th></tr></thead>
<tbody>{"".join(lignes)}</tbody></table></div></div>

<h2>À mesurer <span class="cpt">{len(amesurer)} valeurs</span></h2>
<p class="sous">Rien ne les empêche : personne ne les a relevées.</p>
<div class="carte"><div class="defile"><table><thead><tr><th>Clé</th>
<th>Nombre</th><th class="pliable">Où</th></tr></thead>
<tbody>{lm}</tbody></table></div></div>

<h2>Se déduira <span class="cpt">{len(deduites)} valeurs</span></h2>
<p class="sous">Absentes, mais <b>pas à mesurer</b> : elles dérivent d'un
autre champ, lui-même absent. Les compter avec les précédentes gonflerait
le travail restant de {round(100 * len(deduites) / max(1, len(amesurer) + len(deduites)))} %.</p>
<div class="carte"><div class="defile"><table><thead><tr><th>Clé</th>
<th>Nombre</th><th class="pliable">Pourquoi</th>
<th class="pliable">Où</th></tr></thead>
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
