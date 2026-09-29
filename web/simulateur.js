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
    var r_int = r4(0.5 * p.ep);
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
    var bas = haut.map(function (q) { return [-q[0], -q[1]]; }).reverse().slice(1);
    pts = pts.concat(bas);
    pts.push([x0, -(y0 - re)]);
    return pts;
  }

  /* ── écart d'un contour à l'autre, point à SEGMENT ───────────────── */
  function distSeg(q, a, b) {
    var dx = b[0] - a[0], dy = b[1] - a[1], L2 = dx * dx + dy * dy;
    var t = L2 === 0 ? 0 : Math.max(0, Math.min(1,
      ((q[0] - a[0]) * dx + (q[1] - a[1]) * dy) / L2));
    return Math.hypot(q[0] - (a[0] + t * dx), q[1] - (a[1] + t * dy));
  }
  function ecart(A, B) {
    var pire = 0;
    for (var i = 0; i < A.length; i++) {
      var d = Infinity;
      for (var j = 0; j < B.length; j++)
        d = Math.min(d, distSeg(A[i], B[j], B[(j + 1) % B.length]));
      pire = Math.max(pire, d);
    }
    return pire;
  }

  /* ── dessin : même langage que scripts/plan_decoupe.svg_schema ───── */
  var fmt = function (v) {
    return (Math.round(v * 100) / 100).toString().replace(".", ",");
  };

  function dessiner(d, pts) {
    var ech = Math.max(d.L, d.W);
    var tp = ech * 0.030, tr = ech * 0.0045;
    var mg = ech * 0.09, md = ech * 0.13, mb = md + tp * 1.55;
    var x0 = -d.L / 2, y1 = d.W / 2, y0 = -d.W / 2, x1 = d.L / 2;
    var o = ['<svg viewBox="' + (x0 - mg) + ' ' + (-(y1 + mg)) + ' '
      + (d.L + mg + md) + ' ' + (d.W + mg + mb) + '" width="100%" '
      + 'style="max-width:560px" xmlns="http://www.w3.org/2000/svg" '
      + 'role="img" aria-label="schéma simulé">'];
    o.push('<g fill="none" stroke="currentColor" stroke-width="' + (tr * 2)
      + '" stroke-linejoin="round">');
    o.push('<path d="M ' + pts.map(function (q) {
      return q[0].toFixed(3) + " " + (-q[1]).toFixed(3);
    }).join(" L ") + ' Z"/></g>');

    var txt = [];
    function etiq(x, y, lettre, valeur, dessous) {
      var dy = dessous ? -tp * 1.15 : tp * 0.95;
      txt.push('<circle cx="' + x + '" cy="' + (-y) + '" r="' + tp * 0.62
        + '" fill="currentColor" opacity="0.14"/>'
        + '<text x="' + x + '" y="' + (-y + tp * 0.34) + '" text-anchor="middle" '
        + 'font-size="' + tp * 0.78 + '" font-weight="700" fill="currentColor">'
        + lettre + '</text>'
        + '<text x="' + x + '" y="' + (-y - dy) + '" text-anchor="middle" '
        + 'font-size="' + tp * 0.74 + '" fill="currentColor" opacity="0.72">'
        + valeur + '</text>');
    }
    o.push('<g stroke="currentColor" stroke-width="' + tr + '" fill="none" opacity="0.62">');
    var yl = y0 - md * 0.58;                                    /* A */
    o.push('<path d="M ' + x0 + ' ' + (-y0) + ' L ' + x0 + ' ' + (-(yl - ech * 0.012)) + '"/>');
    o.push('<path d="M ' + x1 + ' ' + (-y0) + ' L ' + x1 + ' ' + (-(yl - ech * 0.012)) + '"/>');
    o.push('<path d="M ' + x0 + ' ' + (-yl) + ' L ' + x1 + ' ' + (-yl) + '"/>');
    etiq(0, yl, "A", fmt(d.L));
    var xl = x1 + md * 0.55;                                    /* B */
    o.push('<path d="M ' + x1 + ' ' + (-y1) + ' L ' + (xl + ech * 0.012) + ' ' + (-y1) + '"/>');
    o.push('<path d="M ' + x1 + ' ' + (-y0) + ' L ' + (xl + ech * 0.012) + ' ' + (-y0) + '"/>');
    o.push('<path d="M ' + xl + ' ' + (-y0) + ' L ' + xl + ' ' + (-y1) + '"/>');
    etiq(xl, 0, "B", fmt(d.W));
    var wc = d.largeur_creux / 2;                               /* C */
    o.push('<path d="M 0 ' + wc + ' L 0 ' + (-wc) + '"/>');
    etiq(0, 0, "C", fmt(d.largeur_creux));
    var cx = x1 - d.r_ext + d.r_ext * 0.7071;                   /* D */
    var cy = y1 - d.r_ext + d.r_ext * 0.7071;
    var dx = cx + d.L * 0.06, dy2 = cy + d.W * 0.20;
    o.push('<path d="M ' + cx + ' ' + (-cy) + ' L ' + dx + ' ' + (-dy2) + '"/>');
    etiq(dx, dy2, "D", "R " + fmt(d.r_ext));
    var ex = -d.L * 0.24, ey = y0 + 0.2;                        /* E */
    var ex2 = ex - d.L * 0.05, ey2 = ey - d.W * 0.26;
    o.push('<path d="M ' + ex + ' ' + (-ey) + ' L ' + ex2 + ' ' + (-ey2) + '"/>');
    etiq(ex2, ey2, "E", "R " + fmt(d.r_int), true);
    o.push('</g>');
    var yn = y0 - md - tp;                                      /* F, en note */
    txt.push('<circle cx="' + (x0 + tp * 0.62) + '" cy="' + (-yn) + '" r="'
      + tp * 0.62 + '" fill="currentColor" opacity="0.14"/>'
      + '<text x="' + (x0 + tp * 0.62) + '" y="' + (-yn + tp * 0.34)
      + '" text-anchor="middle" font-size="' + tp * 0.78
      + '" font-weight="700" fill="currentColor">F</text>'
      + '<text x="' + (x0 + tp * 1.55) + '" y="' + (-yn + tp * 0.30)
      + '" font-size="' + tp * 0.74 + '" fill="currentColor" opacity="0.72">'
      + 'épaisseur ' + fmt(d.ep) + ' (hors du plan de la vue)</text>');
    o.push(txt.join(""));
    o.push('</svg>');
    return o.join("");
  }

  /* ── auto-contrôle : retrouve-t-on la référence Python ? ─────────── */
  function verifier(ref, tol) {
    var p = {}, i;
    for (i = 0; i < ref.parametres.length; i++)
      p[ref.parametres[i].nom] = ref.parametres[i].valeur;
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

    function echappe(s) {
      return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");
    }

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
        boiteSvg.innerHTML = dessiner(d, contour(d, 48));
      }

      var l = [["A", "longueur", d.L, "mm"], ["B", "largeur", d.W, "mm"],
               ["C", "largeur au creux", d.largeur_creux, "mm"],
               ["D", "congé extérieur", d.r_ext, "mm"],
               ["E", "rayon intérieur minimal", d.r_int, "mm"],
               ["F", "épaisseur", d.ep, "mm"]];
      boiteCotes.innerHTML = '<div class="defile"><table class="schema"><tbody>'
        + l.map(function (r) {
            return '<tr><td class="lettre">' + r[0] + '</td><td>' + r[1]
              + '</td><td class="num">' + fmt(r[2]) + " " + r[3] + "</td></tr>";
          }).join("") + "</tbody></table></div>";

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
