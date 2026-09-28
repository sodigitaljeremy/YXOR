/* Visualiseur STL — WebGL brut, aucune dépendance, aucun CDN.
 *
 * Pourquoi pas three.js : le site doit se reconstruire à l'identique dans
 * dix ans. Une bibliothèque tierce, c'est une version à épingler, une
 * empreinte à vérifier et un téléchargement à la construction — trois
 * façons d'échouer. Ici il n'y a rien à récupérer.
 *
 * Le STL est ce que le navigateur affiche ; le STEP reste l'échange. */
(function () {
  "use strict";

  function parseSTL(buf) {
    const dv = new DataView(buf);
    // Un STL ASCII commence par "solid", mais un binaire aussi parfois :
    // on se fie à la taille, seul critère sûr. 84 + 50*n octets.
    const n = dv.getUint32(80, true);
    if (84 + n * 50 !== buf.byteLength) throw new Error("STL non binaire ou corrompu");
    const pos = new Float32Array(n * 9), nor = new Float32Array(n * 9);
    for (let i = 0; i < n; i++) {
      const o = 84 + i * 50;
      const nx = dv.getFloat32(o, true), ny = dv.getFloat32(o + 4, true), nz = dv.getFloat32(o + 8, true);
      for (let v = 0; v < 3; v++) {
        const p = o + 12 + v * 12, k = i * 9 + v * 3;
        pos[k] = dv.getFloat32(p, true);
        pos[k + 1] = dv.getFloat32(p + 4, true);
        pos[k + 2] = dv.getFloat32(p + 8, true);
        nor[k] = nx; nor[k + 1] = ny; nor[k + 2] = nz;
      }
    }
    return { pos, nor, count: n * 3 };
  }

  // --- algèbre minimale, colonnes majeures comme WebGL l'attend ---
  const M = {
    perspective(fovy, asp, near, far) {
      const f = 1 / Math.tan(fovy / 2), d = near - far;
      return [f / asp,0,0,0, 0,f,0,0, 0,0,(far+near)/d,-1, 0,0,2*far*near/d,0];
    },
    lookAt(e, c, up) {
      const z = M.norm([e[0]-c[0], e[1]-c[1], e[2]-c[2]]);
      const x = M.norm(M.cross(up, z)), y = M.cross(z, x);
      return [x[0],y[0],z[0],0, x[1],y[1],z[1],0, x[2],y[2],z[2],0,
              -M.dot(x,e), -M.dot(y,e), -M.dot(z,e), 1];
    },
    cross(a,b){return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]];},
    dot(a,b){return a[0]*b[0]+a[1]*b[1]+a[2]*b[2];},
    norm(a){const l=Math.hypot(a[0],a[1],a[2])||1;return [a[0]/l,a[1]/l,a[2]/l];},
    mul(a,b){const o=new Array(16);for(let i=0;i<4;i++)for(let j=0;j<4;j++){let s=0;
      for(let k=0;k<4;k++)s+=a[k*4+j]*b[i*4+k];o[i*4+j]=s;}return o;},
    translate(x,y,z){return [1,0,0,0, 0,1,0,0, 0,0,1,0, x,y,z,1];}
  };

  const VS = `attribute vec3 p; attribute vec3 n;
    uniform mat4 mvp, mv; varying vec3 vn, vp;
    void main(){ vn = mat3(mv)*n; vp = (mv*vec4(p,1.0)).xyz; gl_Position = mvp*vec4(p,1.0); }`;
  const FS = `precision mediump float; varying vec3 vn, vp; uniform vec3 col;
    void main(){
      vec3 N = normalize(vn);
      if (!gl_FrontFacing) N = -N;
      vec3 L1 = normalize(vec3(0.4, 0.7, 0.8));
      vec3 L2 = normalize(vec3(-0.6, -0.3, 0.4));
      float d = 0.72*max(dot(N,L1),0.0) + 0.26*max(dot(N,L2),0.0) + 0.26;
      vec3 V = normalize(-vp);
      float s = pow(max(dot(reflect(-L1,N),V),0.0), 24.0)*0.18;
      gl_FragColor = vec4(col*d + vec3(s), 1.0);
    }`;

  function compile(gl, src, type) {
    const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
    return s;
  }

  window.visualiseurSTL = function (canvas, url, message) {
    const gl = canvas.getContext("webgl", { antialias: true, alpha: false });
    if (!gl) { message("Votre navigateur ne gère pas WebGL."); return; }

    const prog = gl.createProgram();
    gl.attachShader(prog, compile(gl, VS, gl.VERTEX_SHADER));
    gl.attachShader(prog, compile(gl, FS, gl.FRAGMENT_SHADER));
    gl.linkProgram(prog); gl.useProgram(prog);

    let geo = null, centre = [0,0,0], rayon = 1;
    let theta = -0.9, phi = 1.05, zoom = 2.6, drag = null;

    fetch(url).then(r => {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.arrayBuffer();
    }).then(buf => {
      const g = parseSTL(buf);
      let lo = [1e9,1e9,1e9], hi = [-1e9,-1e9,-1e9];
      for (let i = 0; i < g.pos.length; i += 3)
        for (let k = 0; k < 3; k++) {
          lo[k] = Math.min(lo[k], g.pos[i+k]); hi[k] = Math.max(hi[k], g.pos[i+k]);
        }
      centre = [(lo[0]+hi[0])/2, (lo[1]+hi[1])/2, (lo[2]+hi[2])/2];
      rayon = Math.max(1e-6, Math.hypot(hi[0]-lo[0], hi[1]-lo[1], hi[2]-lo[2]) / 2);
      const bp = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, bp);
      gl.bufferData(gl.ARRAY_BUFFER, g.pos, gl.STATIC_DRAW);
      const bn = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, bn);
      gl.bufferData(gl.ARRAY_BUFFER, g.nor, gl.STATIC_DRAW);
      geo = { bp, bn, count: g.count };
      message(null);
      requestAnimationFrame(dessiner);
    }).catch(e => message("Géométrie indisponible : " + e.message));

    function dessiner() {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const w = canvas.clientWidth, h = canvas.clientHeight;
      if (canvas.width !== w*dpr || canvas.height !== h*dpr) {
        canvas.width = w*dpr; canvas.height = h*dpr;
      }
      gl.viewport(0, 0, canvas.width, canvas.height);
      gl.enable(gl.DEPTH_TEST);
      gl.clearColor(0.08, 0.09, 0.11, 1);
      gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      if (!geo) return;

      const d = rayon * zoom;
      const eye = [d*Math.sin(phi)*Math.cos(theta), d*Math.sin(phi)*Math.sin(theta), d*Math.cos(phi)];
      const view = M.lookAt(eye, [0,0,0], [0,0,1]);
      const model = M.translate(-centre[0], -centre[1], -centre[2]);
      const mv = M.mul(view, model);
      const proj = M.perspective(0.9, Math.max(w/h, 1e-6), rayon*0.02, rayon*60);
      const mvp = M.mul(proj, mv);

      gl.uniformMatrix4fv(gl.getUniformLocation(prog,"mvp"), false, new Float32Array(mvp));
      gl.uniformMatrix4fv(gl.getUniformLocation(prog,"mv"), false, new Float32Array(mv));
      gl.uniform3f(gl.getUniformLocation(prog,"col"), 0.85, 0.78, 0.62);

      const ap = gl.getAttribLocation(prog,"p"), an = gl.getAttribLocation(prog,"n");
      gl.bindBuffer(gl.ARRAY_BUFFER, geo.bp); gl.enableVertexAttribArray(ap);
      gl.vertexAttribPointer(ap, 3, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, geo.bn); gl.enableVertexAttribArray(an);
      gl.vertexAttribPointer(an, 3, gl.FLOAT, false, 0, 0);
      gl.drawArrays(gl.TRIANGLES, 0, geo.count);
    }

    function pointe(e) {
      const t = e.touches ? e.touches[0] : e;
      return { x: t.clientX, y: t.clientY };
    }
    function debut(e) { drag = pointe(e); }
    function bouge(e) {
      if (!drag) return;
      const p = pointe(e);
      theta -= (p.x - drag.x) * 0.01;
      phi = Math.max(0.05, Math.min(Math.PI - 0.05, phi - (p.y - drag.y) * 0.01));
      drag = p; e.preventDefault(); requestAnimationFrame(dessiner);
    }
    function fin() { drag = null; }
    canvas.addEventListener("mousedown", debut);
    window.addEventListener("mousemove", bouge);
    window.addEventListener("mouseup", fin);
    canvas.addEventListener("touchstart", debut, { passive: true });
    canvas.addEventListener("touchmove", bouge, { passive: false });
    canvas.addEventListener("touchend", fin);
    canvas.addEventListener("wheel", e => {
      zoom = Math.max(1.2, Math.min(12, zoom * (1 + Math.sign(e.deltaY) * 0.12)));
      e.preventDefault(); requestAnimationFrame(dessiner);
    }, { passive: false });
    window.addEventListener("resize", () => requestAnimationFrame(dessiner));
  };
})();
