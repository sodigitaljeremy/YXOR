/* Simulation en direct — fiche 0023.
 *
 * ═══════════════════════════════════════════════════════════════════
 *  CALCULER N'EST PAS STOCKER
 * ═══════════════════════════════════════════════════════════════════
 *  Rien de ce qui est calculé ici n'est enregistré nulle part : ni
 *  serveur, ni stockage local, ni cookie. Recharger la page efface tout
 *  et rend les valeurs du dépôt. Le dépôt reste la seule source de
 *  vérité — c'est la règle de la fiche 0018, et elle n'est pas
 *  contournée par le fait que le calcul ait lieu dans le navigateur.
 *
 * ═══════════════════════════════════════════════════════════════════
 *  CE FICHIER EST UNE SECONDE IMPLÉMENTATION
 * ═══════════════════════════════════════════════════════════════════
 *  scripts/profil.py calcule la même forme, et c'est LUI qui fait foi.
 *  Deux implémentations divergent toujours. Celle-ci se contrôle donc,
 *  au chargement, contre une référence calculée en Python et déposée
 *  dans la page. Si elle ne la retrouve pas, elle SE DÉSACTIVE : mieux
 *  vaut pas de simulation qu'une simulation fausse.
 */
(function () {
  "use strict";

  var r4 = function (x) { return Math.round(x * 1e4) / 1e4; };

  /* ── mêmes formules que scripts/profil.py, dans le même ordre ────── */
  function cotes(p) {
    var L = r4(p.H * 1000 * p.r_pied_long);
    var W = r4(p.H * 1000 * p.r_pied_larg);
    var r_ext = r4(W * p.coins);
    var prof = r4((W - W * p.resserrement) / 2);
    var e = r4(L * p.etendue);
    /* rayon intérieur minimal : max(0,5 x épaisseur, limite de machine du
       réglage). La limite arrive dans les données de la page (ref.fixes) ;
       absente, elle est ignorée. Même règle que procedes.rayon_interieur_min. */
    var r_int = r4(Math.max(0.5 * p.ep, p.r_int_machine || 0));
    var R = prof > 0 ? r4((e * e / 4 + prof * prof) / (2 * prof)) : 0;
    return { L: L, W: W, r_ext: r_ext, profondeur: prof, etendue: e, R: R,
             r_int: r_int, ep: p.ep, largeur_creux: r4(W * p.resserrement) };
  }

  function diagnostic(d) {
    var m = [];
    if (d.profondeur <= 0)
      m.push("resserrement à 1 : il n'y a plus de creux, donc plus d'angle "
           + "rentrant à exercer");
    else if (d.R < d.r_int)
      m.push("le creux a un rayon de " + d.R.toFixed(2) + " mm, sous le "
           + "minimum " + d.r_int.toFixed(2) + " mm du procédé : infaisable");
    if (d.r_ext > d.W / 2)
      m.push("congé de coin " + d.r_ext.toFixed(2) + " mm > demi-largeur "
           + (d.W / 2).toFixed(2) + " mm");
    if (2 * d.r_ext > d.L) m.push("les congés de coin se rejoignent sur la longueur");
    if (d.profondeur >= d.W / 2) m.push("le creux traverse la pièce de part en part");
    var xf2 = d.profondeur * (2 * d.R + 2 * d.r_int - d.profondeur);
    if (xf2 > 0 && Math.sqrt(xf2) > d.L / 2 - d.r_ext)
      m.push("le congé du creux déborde sur le congé de coin");
    return m;
  }

  function arc(cx, cy, r, a0, a1, n) {   /* premier point omis, comme en Python */
    var s = [];
    for (var i = 1; i <= n; i++) {
      var a = a0 + (a1 - a0) * i / n;
      s.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]);
    }
    return s;
  }

  function contour(d, nArc) {
    if (diagnostic(d).length) return null;
    nArc = nArc || 48;
    var L = d.L, W = d.W, re = d.r_ext, R = d.R, p = d.profondeur, ri = d.r_int;
    var x0 = L / 2, y0 = W / 2;
    var yc = y0 - p + R;
    var xf = Math.sqrt(p * (2 * R + 2 * ri - p));
    var yf = y0 - ri;
    var n3 = Math.floor(nArc / 3);

    function tangence(sx) {
      var dx = sx * xf, dy = yf - yc, n = Math.hypot(dx, dy);
      return [R * dx / n, yc + R * dy / n];
    }
    function bord(sy) {
      var s = [], t = tangence(1), tl = tangence(-1);
      s = s.concat(arc(x0 - re, sy * (y0 - re), re, 0, sy * Math.PI / 2, n3));
      s.push([xf, sy * y0]);
      var a1 = Math.atan2(sy * t[1] - sy * yf, t[0] - xf);
      s = s.concat(arc(xf, sy * yf, ri, sy * Math.PI / 2, sy * a1, n3));
      var b0 = Math.atan2(sy * t[1] - sy * yc, t[0]);
      var b1 = Math.atan2(sy * tl[1] - sy * yc, tl[0]);
      s = s.concat(arc(0, sy * yc, R, sy * b0, sy * b1, nArc));
      var c0 = Math.atan2(sy * tl[1] - sy * yf, tl[0] + xf);
      s = s.concat(arc(-xf, sy * yf, ri, sy * c0, sy * Math.PI / 2, n3));
      s.push([-xf, sy * y0]);
      s.push([-(x0 - re), sy * y0]);
      s = s.concat(arc(-(x0 - re), sy * (y0 - re), re, sy * Math.PI / 2, Math.PI, n3));
      return s;
    }
    var pts = [[x0, -y0 + re], [x0, y0 - re]];
    var haut = bord(1);
    pts = pts.concat(haut);
    pts.push([-x0, -(y0 - re)]);
    /* Le miroir (x,y) -> (-x,-y) parcourt DÉJÀ le bas de gauche à droite.
       Le renverser en plus faisait repartir du coin bas-droit alors qu'on
       est en bas à gauche : le contour se refermait en huit. La forme
       restait juste point par point, l'aire non — 3605,90 mm² au lieu de
       6300,49. Corrigé le 2026-09-30, côté Python et ici. */
    pts = pts.concat(haut.map(function (q) { return [-q[0], -q[1]]; }));
    return pts;
  }

  /* ── dessin : même langage que scripts/plan_decoupe.svg_schema ───── */
  function echappe(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");
  }

  /* La cote affichée sous une lettre est celle que la pièce a DÉCLARÉE,
     par son nom de grandeur. On ne devine rien d'après le libellé. */
  function valeurCote(c, d) {
    return d[c.grandeur];
  }

  var fmt = function (v) {
    return (Math.round(v * 100) / 100).toString().replace(".", ",");
  };

  /* ── évaluation des repères : MÊME déclaration que scripts/plan_decoupe
     Les coefficients viennent du relevé de la pièce. Aucune constante de
     placement n'est écrite ici — c'était la duplication non gardée que
     l'audit du 2026-09-29 a trouvée (fiche 0024 §2). */
  var BASES = ["L", "W", "r_ext", "r_int", "ep", "largeur_creux", "un"];

  function evaluerTrace(trace, d) {
    var base = {}, k;
    for (k in d) if (d.hasOwnProperty(k)) base[k] = d[k];
    base.un = 1;
    var out = {};
    for (k in trace) {
      if (!trace.hasOwnProperty(k)) continue;
      var v = trace[k];
      if (typeof v !== "object" || v === null) { out[k] = v; continue; }
      var somme = 0, b;
      for (b in v) if (v.hasOwnProperty(b)) somme += (base[b] || 0) * v[b];
      out[k] = Math.round(somme * 1e4) / 1e4;
    }
    return out;
  }

  function dessiner(d, pts, schema) {
    var ech = Math.max(d.L, d.W);
    var tp = ech * 0.030, tr = ech * 0.0045;
    var mg = ech * 0.09, md = ech * 0.13;
    var notes = schema.filter(function (c) {
      return (c.trace || {}).type === "note";
    });
    var mb = md + notes.length * tp * 1.55;
    var x0 = -d.L / 2, y1 = d.W / 2, y0 = -d.W / 2, x1 = d.L / 2;
    var o = ['<svg viewBox="' + (x0 - mg) + ' ' + (-(y1 + mg)) + ' '
      + (d.L + mg + md) + ' ' + (d.W + mg + mb) + '" width="100%" '
      + 'xmlns="http://www.w3.org/2000/svg" role="img" '
      + 'aria-label="schéma simulé">'];
    o.push('<g fill="none" stroke="currentColor" stroke-width="' + (tr * 2)
      + '" stroke-linejoin="round">');
    o.push('<path d="M ' + pts.map(function (q) {
      return q[0].toFixed(3) + " " + (-q[1]).toFixed(3);
    }).join(" L ") + ' Z"/></g>');

    var txt = [];
    function etiq(x, y, lettre, valeur, dessous, ancre) {
      var dy = dessous ? -tp * 1.15 : tp * 0.95;
      txt.push('<circle cx="' + x + '" cy="' + (-y) + '" r="' + tp * 0.62
        + '" fill="currentColor" opacity="0.14"/>'
        + '<text x="' + x + '" y="' + (-y + tp * 0.34) + '" text-anchor="middle" '
        + 'font-size="' + tp * 0.78 + '" font-weight="700" fill="currentColor">'
        + lettre + '</text>'
        + '<text x="' + x + '" y="' + (-y - dy) + '" text-anchor="'
        + (ancre || "middle") + '" font-size="' + tp * 0.74
        + '" fill="currentColor" opacity="0.72">' + valeur + '</text>');
    }
    o.push('<g stroke="currentColor" stroke-width="' + tr
      + '" fill="none" opacity="0.62">');

    var iNote = 0;
    schema.forEach(function (c) {
      var t = evaluerTrace(c.trace || {}, d), L = c.lettre;
      var v = fmt(valeurCote(c, d));
      if (t.type === "cote_h") {
        var yl = y0 - md * 0.58;
        [t.x1, t.x2].forEach(function (x) {
          o.push('<path d="M ' + x + ' ' + (-y0) + ' L ' + x + ' '
            + (-(yl - ech * 0.012)) + '"/>');
        });
        o.push('<path d="M ' + t.x1 + ' ' + (-yl) + ' L ' + t.x2 + ' ' + (-yl) + '"/>');
        etiq((t.x1 + t.x2) / 2, yl, L, v);
      } else if (t.type === "cote_v") {
        var xl = x1 + md * 0.55;
        [t.y1, t.y2].forEach(function (y) {
          o.push('<path d="M ' + x1 + ' ' + (-y) + ' L ' + (xl + ech * 0.012)
            + ' ' + (-y) + '"/>');
        });
        o.push('<path d="M ' + xl + ' ' + (-t.y1) + ' L ' + xl + ' ' + (-t.y2) + '"/>');
        etiq(xl, (t.y1 + t.y2) / 2, L, v);
      } else if (t.type === "cote_v_int") {
        o.push('<path d="M ' + t.x + ' ' + (-t.y1) + ' L ' + t.x + ' '
          + (-t.y2) + '"/>');
        etiq(t.x, (t.y1 + t.y2) / 2, L, v);
      } else if (t.type === "rayon") {
        var lx = t.x + t.dx, ly = t.y + t.dy;
        o.push('<path d="M ' + t.x + ' ' + (-t.y) + ' L ' + lx + ' '
          + (-ly) + '"/>');
        etiq(lx, ly, L, "R " + v, t.dy < 0);
      } else if (t.type === "note") {
        var yn = y0 - md - tp * (1 + iNote * 1.55);
        iNote++;
        txt.push('<circle cx="' + (x0 + tp * 0.62) + '" cy="' + (-yn) + '" r="'
          + tp * 0.62 + '" fill="currentColor" opacity="0.14"/>'
          + '<text x="' + (x0 + tp * 0.62) + '" y="' + (-yn + tp * 0.34)
          + '" text-anchor="middle" font-size="' + tp * 0.78
          + '" font-weight="700" fill="currentColor">' + L + '</text>'
          + '<text x="' + (x0 + tp * 1.55) + '" y="' + (-yn + tp * 0.30)
          + '" font-size="' + tp * 0.74 + '" fill="currentColor" opacity="0.72">'
          + echappe(c.libelle) + " " + v + ' (hors du plan de la vue)</text>');
      }
    });
    o.push('</g>');
    o.push(txt.join(""));
    o.push('</svg>');
    return o.join("");
  }

  /* ── auto-contrôle : retrouve-t-on la référence Python ? ─────────── */
  /* Les données fixes (non réglables) de la page, ajoutées aux paramètres. */
  function avecFixes(p, ref) {
    var k, f = ref.fixes || {};
    for (k in f) if (f.hasOwnProperty(k)) p[k] = f[k];
    return p;
  }

  function verifier(ref, tol) {
    var p = {}, i;
    for (i = 0; i < ref.parametres.length; i++)
      p[ref.parametres[i].nom] = ref.parametres[i].valeur;
    avecFixes(p, ref);
    var d = cotes(p), pire = 0, cle;
    for (cle in ref.reference.cotes) {
      if (!ref.reference.cotes.hasOwnProperty(cle)) continue;
      pire = Math.max(pire, Math.abs(d[cle] - ref.reference.cotes[cle]));
    }
    if (pire > 1e-3)
      return "les cotes recalculées s'écartent de " + pire.toFixed(4)
           + " mm de la référence du dépôt";
    var c = contour(d, ref.reference.n_arc);
    if (!c) return "le contour de référence est jugé infaisable";
    var R0 = ref.reference.contour;
    if (c.length !== R0.length)
      return "le contour recalculé a " + c.length + " points au lieu de "
           + R0.length;
    var e = 0;
    for (i = 0; i < c.length; i++)
      e = Math.max(e, Math.abs(c[i][0] - R0[i][0]), Math.abs(c[i][1] - R0[i][1]));
    if (e > tol)
      return "le contour recalculé s'écarte de " + e.toFixed(4)
           + " mm de la référence du dépôt (tolérance " + tol + ")";
    return null;
  }

  window.simulateur = function (ref, elements) {
    var tol = ref.tolerance_mm || 0.05;
    var faute = verifier(ref, tol);
    if (faute) {
      elements.hote.innerHTML = '<div class="alerte"><b>SIMULATION '
        + 'DÉSACTIVÉE.</b><br>Le calcul de cette page ne retrouve pas la '
        + 'géométrie engendrée par le dépôt : ' + faute + '.<br>Les valeurs '
        + 'affichées plus haut restent celles du dépôt et font foi.</div>';
      return;
    }

    var etat = {}, i;
    for (i = 0; i < ref.parametres.length; i++)
      etat[ref.parametres[i].nom] = ref.parametres[i].valeur;
    avecFixes(etat, ref);
    var depart = JSON.parse(JSON.stringify(etat));

    var html = ['<div class="simbandeau" id="simb"></div><div class="reglages">'];
    ref.parametres.forEach(function (pa) {
      html.push('<label><span class="rl">' + pa.libelle + '</span>'
        + '<input type="range" data-n="' + pa.nom + '" min="' + pa.mini
        + '" max="' + pa.maxi + '" step="' + pa.pas + '" value="' + pa.valeur + '">'
        + '<output data-o="' + pa.nom + '"></output></label>');
    });
    html.push('</div><div class="svgbox" id="simsvg"></div>');
    html.push('<div id="simcotes"></div>');
    html.push('<button type="button" id="simraz">Revenir aux valeurs du dépôt</button>');
    html.push('<div id="simyaml"></div>');
    elements.hote.innerHTML = html.join("");

    var boiteSvg = document.getElementById("simsvg");
    var boiteCotes = document.getElementById("simcotes");
    var bandeau = document.getElementById("simb");
    var boiteYaml = document.getElementById("simyaml");

    function rendre() {
      var d = cotes(etat), mauvais = diagnostic(d), modifie = false, k;
      for (k in etat) if (etat[k] !== depart[k]) modifie = true;

      ref.parametres.forEach(function (pa) {
        var o = elements.hote.querySelector('[data-o="' + pa.nom + '"]');
        o.textContent = etat[pa.nom] + pa.unite;
        o.className = etat[pa.nom] !== depart[pa.nom] ? "modif" : "";
      });

      bandeau.className = "simbandeau" + (modifie ? " actif" : "");
      bandeau.innerHTML = modifie
        ? "<b>Simulation — non enregistrée.</b> Ces valeurs n'existent que "
          + "dans cette page : rien n'est envoyé, rien n'est stocké, et "
          + "recharger rend celles du dépôt. Le dépôt reste la seule source "
          + "de vérité."
        : "Valeurs du dépôt. Déplacez un curseur pour simuler.";

      if (mauvais.length) {
        boiteSvg.innerHTML = '<p class="ind" style="padding:20px">Forme '
          + 'impossible : ' + echappe(mauvais[0]) + '.</p>';
      } else {
        boiteSvg.innerHTML = dessiner(d, contour(d, 48), ref.schema);
        // le SVG est refait à chaque mouvement de curseur : le zoom doit
        // être réinstallé, sinon il ne s'applique qu'au tout premier.
        boiteSvg.dataset.zoom = "";
        if (window.equiperZoom) window.equiperZoom();
      }

      /* Les lettres et les libellés viennent du dépôt, pas d'une liste
         recopiée ici : ajouter une cote à la pièce la fait apparaître. */
      boiteCotes.innerHTML = '<table class="schema"><tbody>'
        + ref.schema.map(function (c) {
            return '<tr><td class="lettre">' + echappe(c.lettre) + '</td><td>'
              + echappe(c.libelle) + '</td><td class="num">'
              + fmt(valeurCote(c, d)) + " mm</td></tr>";
          }).join("") + "</tbody></table>";

      if (!modifie) { boiteYaml.innerHTML = ""; return; }
      var lignes = [];
      ref.parametres.forEach(function (pa) {
        if (etat[pa.nom] === depart[pa.nom]) return;
        lignes.push(pa.cible + "\n    " + depart[pa.nom] + "  ->  " + etat[pa.nom]);
      });
      boiteYaml.innerHTML = '<p class="sous">Pour <b>figer</b> cette '
        + 'simulation, modifiez le dépôt puis régénérez. Rien ici ne le '
        + 'fera à votre place :</p><pre class="yaml">'
        + echappe(lignes.join("\n\n")) + "\n\n"
        + "puis :  python scripts/regenerer.py</pre>";
    }

    elements.hote.addEventListener("input", function (ev) {
      var n = ev.target.getAttribute("data-n");
      if (!n) return;
      etat[n] = parseFloat(ev.target.value);
      rendre();
    });
    document.getElementById("simraz").addEventListener("click", function () {
      ref.parametres.forEach(function (pa) {
        etat[pa.nom] = pa.valeur;
        elements.hote.querySelector('[data-n="' + pa.nom + '"]').value = pa.valeur;
      });
      rendre();
    });
    rendre();
  };
})();
