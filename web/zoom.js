/* Zoom du dessin seul — fiche 0025.
 *
 * Le zoom de page fonctionne déjà : le `viewport` ne porte pas
 * `user-scalable=no`. Mais il agrandit TOUTE la mise en page — on perd
 * la colonne, on défile dans les deux axes, et on ne retrouve plus le
 * tableau qui accompagne le dessin.
 *
 * Ici on ne touche qu'au `viewBox` du SVG. Le dessin est vectoriel :
 * agrandir ne dégrade rien, contrairement à une image.
 *
 * `touch-action: none` est posé en CSS sur le cadre. Sans lui, le
 * navigateur prend le geste pour faire défiler la page et le dessin ne
 * bouge jamais — c'est le piège classique, et il est silencieux.
 */
(function () {
  "use strict";

  var MINI = 1, MAXI = 20;          // facteurs d'agrandissement extrêmes

  function equiper(boite) {
    var svg = boite.querySelector("svg");
    if (!svg || boite.dataset.zoom === "1") return;
    boite.dataset.zoom = "1";

    var vb0 = svg.getAttribute("viewBox").split(/\s+/).map(parseFloat);
    var vb = vb0.slice();

    function poser() {
      svg.setAttribute("viewBox", vb.map(function (n) {
        return Math.round(n * 1000) / 1000;
      }).join(" "));
      var f = vb0[2] / vb[2];
      boite.querySelector(".zr").disabled = f <= MINI + 1e-9;
    }
    /* Échelle : combien d'unités de dessin par pixel d'écran. */
    function parPixel() {
      return vb[2] / (svg.clientWidth || boite.clientWidth || 1);
    }
    /* Zoome autour d'un point de l'écran, pour que ce point ne bouge
       pas — sinon le dessin fuit sous le doigt. */
    function zoomer(k, cx, cy) {
      var f = vb0[2] / vb[2];
      k = Math.max(MINI / f, Math.min(MAXI / f, k));
      var r = boite.getBoundingClientRect();
      var ux = vb[0] + (cx - r.left) / r.width * vb[2];
      var uy = vb[1] + (cy - r.top) / r.height * vb[3];
      vb[0] = ux - (ux - vb[0]) / k;
      vb[1] = uy - (uy - vb[1]) / k;
      vb[2] /= k;
      vb[3] /= k;
      poser();
    }
    function glisser(dx, dy) {
      var k = parPixel();
      vb[0] -= dx * k;
      vb[1] -= dy * k;
      poser();
    }

    var cmd = document.createElement("div");
    cmd.className = "zoomcmd";
    cmd.innerHTML = '<button type="button" class="zm" aria-label="Réduire">−</button>'
      + '<button type="button" class="zp" aria-label="Agrandir">+</button>'
      + '<button type="button" class="zr" aria-label="Vue entière">⟲</button>';
    boite.appendChild(cmd);

    var r = boite.getBoundingClientRect;
    function centre() {
      var b = boite.getBoundingClientRect();
      return [b.left + b.width / 2, b.top + b.height / 2];
    }
    cmd.querySelector(".zp").onclick = function () {
      var c = centre(); zoomer(1.5, c[0], c[1]);
    };
    cmd.querySelector(".zm").onclick = function () {
      var c = centre(); zoomer(1 / 1.5, c[0], c[1]);
    };
    cmd.querySelector(".zr").onclick = function () {
      vb = vb0.slice(); poser();
    };

    /* Un seul doigt glisse, deux doigts pincent. Les événements
       « pointer » couvrent souris, doigt et stylet d'un coup. */
    var actifs = {}, ecart0 = 0, milieu0 = null;
    function liste() {
      return Object.keys(actifs).map(function (k) { return actifs[k]; });
    }
    boite.addEventListener("pointerdown", function (ev) {
      if (ev.target.closest(".zoomcmd")) return;
      boite.setPointerCapture(ev.pointerId);
      actifs[ev.pointerId] = { x: ev.clientX, y: ev.clientY };
      var l = liste();
      if (l.length === 2) {
        ecart0 = Math.hypot(l[0].x - l[1].x, l[0].y - l[1].y);
        milieu0 = [(l[0].x + l[1].x) / 2, (l[0].y + l[1].y) / 2];
      }
    });
    boite.addEventListener("pointermove", function (ev) {
      var p = actifs[ev.pointerId];
      if (!p) return;
      ev.preventDefault();
      var l = liste();
      if (l.length === 1) {
        glisser(ev.clientX - p.x, ev.clientY - p.y);
      } else if (l.length === 2) {
        p.x = ev.clientX; p.y = ev.clientY;
        l = liste();
        var ec = Math.hypot(l[0].x - l[1].x, l[0].y - l[1].y);
        if (ecart0 > 0 && ec > 0) zoomer(ec / ecart0, milieu0[0], milieu0[1]);
        ecart0 = ec;
        return;
      }
      p.x = ev.clientX; p.y = ev.clientY;
    });
    function lacher(ev) {
      delete actifs[ev.pointerId];
      if (liste().length < 2) { ecart0 = 0; milieu0 = null; }
    }
    boite.addEventListener("pointerup", lacher);
    boite.addEventListener("pointercancel", lacher);
    boite.addEventListener("wheel", function (ev) {
      ev.preventDefault();
      zoomer(ev.deltaY < 0 ? 1.18 : 1 / 1.18, ev.clientX, ev.clientY);
    }, { passive: false });

    poser();
  }

  window.equiperZoom = function () {
    var b = document.querySelectorAll(".svgbox");
    for (var i = 0; i < b.length; i++) equiper(b[i]);
  };
  document.addEventListener("DOMContentLoaded", window.equiperZoom);
})();
