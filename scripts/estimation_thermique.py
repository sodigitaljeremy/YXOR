#!/usr/bin/env python3
"""Estimation thermique du Damiao J4310 V1.2 : un k estimé AU BUREAU, sans achat.

    .venv/bin/python scripts/estimation_thermique.py

Venv DU PROJET. C'est une ESTIMATION, pas une mesure : son résultat ne va
PAS dans params/mesures.yaml. Rapport : docs/estimation-thermique-j4310.md.

Données (constructeur, dépôt github.com/dmBots/DM-J4310-2EC, commit 034e06552a) :
  test-data/performance-curves/V1.2/温升_3.5Nm.png   -> exports/thermique/temp_rise_3.5Nm.png
  test-data/performance-curves/V1.2/温升.png         -> exports/thermique/temp_rise.png
Les images vivent dans exports/ (ignoré) ; leur empreinte est vérifiée.
Les télécharger :
  gh api "repos/dmBots/DM-J4310-2EC/contents/<chemin encodé>" --jq .content | base64 -d

═══════════════════════════════════════════════════════════════════════
 LA MÉTHODE
═══════════════════════════════════════════════════════════════════════

1. NUMÉRISER. La courbe est rouge ; les graduations de l'axe vertical
   aussi (30 à 110 °C) : elles étalonnent l'axe. Les lignes de grille
   verticales étalonnent le temps. Un point tous les 5 s.
2. EXCLURE LE PLATEAU. Les deux courbes plafonnent à 99 °C, à 3,5 comme
   à 3,2 N·m : ce palier commun ressemble à la limite de protection
   (≤ 100 °C recommandé, manuel V1.4 p. 7), pas à un équilibre. Il est
   retiré avant l'ajustement.
3. AJUSTER T(t) = T0 + ΔT (1 − e^(−t/τ)), départ libre, puis départ
   imposé à l'ambiante (20, 25, 30 °C : l'ambiante de l'essai n'est pas
   publiée ; la courbe T-N du manuel est à 25 °C).
4. EN TIRER LE COUPLE CONTINU. Pertes ∝ couple² :
       couple_continu = C_essai × √((T_lim − T_amb) / (T∞ − T_amb))
   et k = couple_continu / 3,5 N·m.

PROPRE AU J4310 (précisé le 2026-10-01, refonte R6). Ce script estime le
couple continu du Damiao J4310 à partir de ses courbes constructeur ; il
ne concerne pas le RS00 retenu pour S (fiche 0065). De params/banc.yaml,
il ne lit que l'écart sous la protection (10 °C).

UN SEUL SEUIL THERMIQUE (2026-09-30, 22 h 30). T_lim est celui du
protocole de banc : la protection du constructeur (params/actionneurs.yaml,
dm_j4310_48v.protection_thermique_C, 100 °C) moins l'écart du protocole
(params/banc.yaml, seuil_thermique, 10 °C), soit 90 °C. L'écart était dans
params/criteres_selection.yaml jusqu'à la refonte R3 (2026-10-01).
Avant, l'estimation prenait 100 °C et le protocole arrêtait à 90 °C : le
continu mesuré aurait été ~7 % sous l'estimé, par construction.

`estimer()` était lu par scripts/selection_multicritere.py, archivé à la
refonte R3 (2026-10-01) ; il reste exécutable seul, pour information.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.optimize import curve_fit

REPO = Path(__file__).resolve().parents[1]
DOSSIER = REPO / "exports" / "thermique"
COURBES = {
    "temp_rise_3.5Nm.png": dict(couple=3.5, x0=210.0, x_fin=722.0, t_fin=300.0,
                                sha256="2c3bb34fa5034990b760b95a2faacf152174acdf1c24061198d148e04d84dda7"),
    "temp_rise.png": dict(couple=3.2, x0=219.0, x_fin=773.0, t_fin=700.0,
                          sha256="bb65aa2049ed5ef617070a59f7dd2b8146f5fd22826e2b856e81b9359d409278"),
}
NOMINAL_NM = 3.5        # manuel V1.4, p. 7
ACTIONNEUR = "dm_j4310_48v"
AMBIANTES = (20.0, 25.0, 30.0)
PLATEAU_C = 98.5


def numeriser(chemin: Path, c: dict):
    a = np.asarray(Image.open(chemin).convert("RGB")).astype(int)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    rouge = (R > 180) & (G < 110) & (B < 110)
    rangs = np.where(rouge[:, 197])[0]                   # graduations, à gauche de l'épine
    grp = []
    for y in rangs:
        (grp[-1].append(y) if grp and y - grp[-1][-1] <= 1 else grp.append([y]))
    ty = sorted(np.mean(g) for g in grp)
    if len(ty) != 9:
        raise SystemExit(f"{chemin.name} : {len(ty)} graduations trouvées, 9 attendues")
    py = np.polyfit(ty, list(range(110, 29, -10)), 1)
    px = np.polyfit([c["x0"], c["x_fin"]], [0.0, c["t_fin"]], 1)
    pts = [(np.polyval(px, x), np.polyval(py, 74 + np.where(rouge[74:533, x])[0].mean()))
           for x in range(202, 799) if rouge[74:533, x].any()]
    t = np.array([p[0] for p in pts]); T = np.array([p[1] for p in pts])
    g = np.arange(np.ceil(t.min() / 5) * 5, t.max(), 5)
    return g, np.interp(g, t, T)


def modele(t, T0, D, tau):
    return T0 + D * (1 - np.exp(-t / tau))


def seuil_thermique() -> tuple[float, str]:
    """T_lim du protocole : protection constructeur − écart du protocole. Lu, jamais écrit ici."""
    import yaml
    cat = yaml.safe_load((REPO / "params" / "actionneurs.yaml").read_text(encoding="utf-8"))
    ca = yaml.safe_load((REPO / "params" / "banc.yaml").read_text(encoding="utf-8"))["seuil_thermique"]
    # Les courbes sont celles du J4310 : SA protection (ACTIONNEUR), pas celle
    # de l'actionneur du banc, le RS00 depuis la refonte R6 (2026-10-01).
    prot = cat["candidats"][ACTIONNEUR]["protection_thermique_C"]["valeur"]
    ecart = ca["ecart_sous_protection_C"]["valeur"]
    return float(prot - ecart), f"protection {prot:g} °C − {ecart:g} °C du protocole"


class ImagesAbsentes(RuntimeError):
    pass


def estimer(bavard: bool = False) -> dict:
    """Numérise, ajuste, et rend la fourchette de k au seuil du protocole.

    Lève ImagesAbsentes si les courbes manquent ou ont changé : pas de repli
    silencieux sur une valeur recopiée.
    """
    t_lim, t_lim_src = seuil_thermique()
    manquants = [n for n in COURBES if not (DOSSIER / n).exists()]
    if manquants:
        raise ImagesAbsentes(f"images absentes de {DOSSIER.relative_to(REPO)} : {', '.join(manquants)} "
                             "— voir la docstring de scripts/estimation_thermique.py")
    say = print if bavard else (lambda *a, **k: None)
    say(f"  seuil thermique : {t_lim:g} °C ({t_lim_src})")
    lignes = []
    for nom, c in COURBES.items():
        chemin = DOSSIER / nom
        sha = hashlib.sha256(chemin.read_bytes()).hexdigest()
        if sha != c["sha256"]:
            raise ImagesAbsentes(f"{nom} : sha256 {sha[:12]}… ≠ attendu {c['sha256'][:12]}… — la courbe a changé")
        t, T = numeriser(chemin, c)
        ip = next(i for i in range(len(T)) if (T[i:] >= PLATEAU_C).all())
        tf, Tf = t[:ip], T[:ip]
        say(f"\n  {nom} — {c['couple']} N·m, 120 rpm, 24 V ; {len(tf)} points, plateau exclu dès {t[ip]:.0f} s")
        fits = []
        p, cov = curve_fit(modele, tf, Tf, p0=(25, 80, 200), maxfev=20000)
        fits.append(("départ libre", p, np.sqrt(np.diag(cov))))
        for Ta in AMBIANTES:
            p2, cov2 = curve_fit(lambda x, D, tau: modele(x, Ta, D, tau), tf, Tf, p0=(80, 200), maxfev=20000)
            fits.append((f"départ {Ta:g} °C", (Ta, *p2), np.sqrt(np.diag(cov2))))
        for lib, p_, e_ in fits:
            Tinf = p_[0] + p_[1]
            rms = np.sqrt(np.mean((modele(tf, *p_) - Tf) ** 2))
            for Ta in AMBIANTES:
                if lib.startswith("départ ") and lib != "départ libre" and not lib.startswith(f"départ {Ta:g} "):
                    continue
                if Tinf <= Ta:
                    continue
                cc = c["couple"] * np.sqrt((t_lim - Ta) / (Tinf - Ta))
                lignes.append((nom, c["couple"], lib, Ta, p_[1], p_[2], Tinf, rms, cc, cc / NOMINAL_NM))
                say(f"    {lib:14s} ambiante {Ta:4.0f} °C : ΔT {p_[1]:5.1f}  τ {p_[2]:4.0f} s  T∞ {Tinf:6.1f} °C  "
                    f"rms {rms:4.2f}  -> continu {cc:4.2f} N·m, k = {cc / NOMINAL_NM:4.2f}")
    ks = [float(l[-1]) for l in lignes]
    return dict(k_bas=round(min(ks), 2), k_haut=round(max(ks), 2), k_mediane=round(float(np.median(ks)), 2),
                n=len(ks), t_lim=t_lim, t_lim_source=t_lim_src, lignes=lignes)


def main() -> int:
    try:
        r = estimer(bavard=True)
    except ImagesAbsentes as e:
        print(e)
        return 1
    print(f"\n  k estimé : {r['k_bas']:.2f} à {r['k_haut']:.2f} (médiane {r['k_mediane']:.2f}), sur {r['n']} combinaisons "
          f"(2 courbes × ajustements × ambiantes), au seuil de {r['t_lim']:g} °C")
    print("  ESTIMATION, pas une mesure : ne va pas dans params/mesures.yaml.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
