#!/usr/bin/env python3
"""Mesurer les pages pour de bon — Chromium sans interface.

    .venv/bin/pip install -r requirements-dev.txt
    .venv/bin/python -m playwright install chromium
    .venv/bin/python scripts/verifier_pages.py

═══════════════════════════════════════════════════════════════════════
 POURQUOI
═══════════════════════════════════════════════════════════════════════

Deux jours durant, l'audit mobile a reposé sur un modèle calculé depuis
le contenu : largeur estimée à 7,2 px par caractère, plus 20 px de marge
par cellule. **Ce modèle était faux au moins une fois** — il ignorait que
`overflow-wrap: anywhere` coupe une clé longue, ce qui m'a fait annoncer
trois débordements inexistants.

Un modèle qu'on ne confronte jamais dérive sans le dire. Celui-ci est
désormais confronté : ce script mesure ce que le navigateur fait
réellement.

═══════════════════════════════════════════════════════════════════════
 DÉVELOPPEMENT SEULEMENT
═══════════════════════════════════════════════════════════════════════

Ni `requirements.txt`, ni le Dockerfile. Chromium pèse ~150 Mo et n'a
rien à faire dans une image qui produit des DXF. Les captures vont dans
`exports/`, donc hors Git.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SITE = REPO / "site"
SORTIE = REPO / "exports" / "pages"

LARGEURS = [390, 768, 1280]        # téléphone, tablette, bureau
WCAG_MIN = 24                      # WCAG 2.2 § 2.5.8, niveau AA
PLATEFORME_MIN = 44                # Apple HIG / Material


def pages() -> list[Path]:
    return sorted(SITE.rglob("*.html"))


MESURES = """() => {
  const doc = document.documentElement;
  const tables = [...document.querySelectorAll('table')].map((t, i) => ({
    i, colonnes: Math.max(...[...t.rows].map(r => r.cells.length)),
    largeur: Math.round(t.getBoundingClientRect().width),
    scrollLargeur: Math.round(t.scrollWidth),
    conteneur: t.parentElement ? Math.round(t.parentElement.clientWidth) : 0,
    deborde: t.scrollWidth > (t.parentElement ? t.parentElement.clientWidth : 0) + 1,
  }));
  const sel = 'a, button, summary, input, [role=button]';
  const cibles = [...document.querySelectorAll(sel)].map(el => {
    const r = el.getBoundingClientRect();
    return {
      quoi: el.tagName.toLowerCase() + (el.className ? '.' + String(el.className).split(' ')[0] : ''),
      texte: (el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 24),
      h: Math.round(r.height), w: Math.round(r.width),
    };
  }).filter(c => c.h > 0);
  return {
    largeurDoc: doc.scrollWidth,
    largeurVue: doc.clientWidth,
    hauteur: doc.scrollHeight,
    deborde: doc.scrollWidth > doc.clientWidth + 1,
    tables, cibles,
    curseurs: document.querySelectorAll('input[type=range]').length,
  };
}"""


def verifier() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("\n✗ playwright absent. Installer :")
        print("   .venv/bin/pip install -r requirements-dev.txt")
        print("   .venv/bin/python -m playwright install chromium\n")
        return 1
    if not pages():
        print("\n✗ aucune page dans site/ : lancer d'abord regenerer.py\n")
        return 1

    SORTIE.mkdir(parents=True, exist_ok=True)
    rapport, fautes = {}, []

    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        for largeur in LARGEURS:
            ctx = nav.new_context(viewport={"width": largeur, "height": 900},
                                  device_scale_factor=2)
            pg = ctx.new_page()
            erreurs_js: list[str] = []
            pg.on("pageerror", lambda e: erreurs_js.append(str(e)))
            for f in pages():
                nom = str(f.relative_to(SITE)).replace("/", "_").removesuffix(".html")
                pg.goto(f.as_uri(), wait_until="networkidle")
                m = pg.evaluate(MESURES)
                m["erreurs_js"] = list(erreurs_js)
                erreurs_js.clear()
                rapport.setdefault(nom, {})[largeur] = m
                pg.screenshot(path=str(SORTIE / f"{nom}_{largeur}.png"),
                              full_page=True)

                # ── ce qui est un DÉFAUT, pas une observation ──────────
                if m["deborde"]:
                    fautes.append(f"{nom} @{largeur} : la PAGE déborde "
                                  f"({m['largeurDoc']} px pour {m['largeurVue']})")
                for t in m["tables"]:
                    if t["deborde"]:
                        fautes.append(
                            f"{nom} @{largeur} : tableau {t['i']} "
                            f"({t['colonnes']} col.) déborde son conteneur — "
                            f"{t['scrollLargeur']} px pour {t['conteneur']}")
                if m["erreurs_js"]:
                    fautes.append(f"{nom} @{largeur} : erreur JS — "
                                  f"{m['erreurs_js'][0][:90]}")
                if largeur == LARGEURS[0]:
                    for c in m["cibles"]:
                        if c["h"] < WCAG_MIN:
                            fautes.append(
                                f"{nom} @{largeur} : cible {c['h']} px "
                                f"< {WCAG_MIN} (WCAG) — {c['quoi']} "
                                f"« {c['texte']} »")
            ctx.close()

        # ── les sept curseurs, actionnés pour de bon ──────────────────
        piece = next((f for f in pages() if f.parent.name == "semelle_apprentissage"
                      and "atelier" not in str(f)), None)
        if piece:
            ctx = nav.new_context(viewport={"width": 390, "height": 900})
            pg = ctx.new_page()
            err: list[str] = []
            pg.on("pageerror", lambda e: err.append(str(e)))
            pg.goto(piece.as_uri(), wait_until="networkidle")
            curs = pg.query_selector_all("input[type=range]")
            print(f"\n  curseurs trouvés : {len(curs)}")
            for i, c in enumerate(curs):
                nom = c.get_attribute("data-n")
                mini = float(c.get_attribute("min"))
                maxi = float(c.get_attribute("max"))
                avant = pg.eval_on_selector("#simsvg", "e => e.innerHTML.length")
                # on pousse à mi-course puis au maximum : le dessin doit
                # changer, et aucune erreur ne doit apparaître
                for v in ((mini + maxi) / 2, maxi):
                    c.evaluate("(e, v) => { e.value = v; "
                               "e.dispatchEvent(new Event('input', {bubbles:true})); }", v)
                apres = pg.eval_on_selector("#simsvg", "e => e.innerHTML.length")
                bandeau = pg.eval_on_selector("#simb", "e => e.className")
                etat = "OK " if apres != avant and "actif" in bandeau else "FIGÉ"
                if etat == "FIGÉ":
                    fautes.append(f"curseur « {nom} » : le schéma ne change pas "
                                  f"ou le bandeau ne s'allume pas")
                print(f"    {etat} {nom:<14} {mini} → {maxi}   "
                      f"svg {avant} → {apres} car.")
                c.evaluate("e => { e.value = e.defaultValue; "
                           "e.dispatchEvent(new Event('input', {bubbles:true})); }")
            pg.screenshot(path=str(SORTIE / "simulateur_390.png"), full_page=True)
            if err:
                fautes.append(f"simulateur : erreur JS — {err[0][:90]}")
            ctx.close()
        nav.close()

    (SORTIE / "mesures.json").write_text(
        json.dumps(rapport, ensure_ascii=False, indent=2), encoding="utf-8")

    # ── rapport ───────────────────────────────────────────────────────
    print(f"\n  {len(pages())} pages × {len(LARGEURS)} largeurs, "
          f"mesurées dans Chromium\n")
    print(f"  {'page':<34} {'largeur':>8} {'doc':>6} {'haut.':>7} {'tableaux'}")
    print("  " + "─" * 74)
    for nom, par_l in rapport.items():
        for largeur, m in par_l.items():
            t = ", ".join(f"{x['colonnes']}c/{x['scrollLargeur']}px"
                          + ("!" if x["deborde"] else "") for x in m["tables"]) or "—"
            print(f"  {nom:<34} {largeur:>8} {m['largeurDoc']:>6} "
                  f"{m['hauteur']:>7}  {t[:30]}")

    m390 = [c for nom, p in rapport.items() for c in p[390]["cibles"]]
    if m390:
        sous_wcag = sum(1 for c in m390 if c["h"] < WCAG_MIN)
        sous_plat = sum(1 for c in m390 if c["h"] < PLATEFORME_MIN)
        print(f"\n  cibles tactiles à 390 px : {len(m390)} mesurées, "
              f"{sous_wcag} sous {WCAG_MIN} px (WCAG), "
              f"{sous_plat} sous {PLATEFORME_MIN} px (plateformes)")

    print(f"\n  captures : exports/pages/  ({len(list(SORTIE.glob('*.png')))} images)")
    if fautes:
        print(f"\n✗ {len(fautes)} DÉFAUT(S) :")
        for f in dict.fromkeys(fautes):
            print(f"   {f}")
        return 1
    print("\n  aucun débordement, aucune cible sous le seuil WCAG, "
          "aucune erreur JS.")
    return 0


if __name__ == "__main__":
    sys.exit(verifier())
