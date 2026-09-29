# Instructions — projet YXOR

Robot humanoïde bipède paramétrique. Jeremy est développeur (JS/TS, Python) et
**débutant complet en CAO et en mécanique**. Explique les notions mécaniques au
passage, sans les supposer acquises.

## Règles non négociables

1. **Aucune cote en dur.** Toute dimension structurelle dérive de `H` et d'un
   ratio défini dans `params/anthropometry.yaml`. Une valeur en millimètres
   écrite directement dans le code d'une pièce est un bug.
   **Restreinte aux cotes de nature `echelle`** (fiche 0013) : une épaisseur de
   paroi, un diamètre d'axe ou une nervure ne dérivent PAS de `H` mais d'une
   charge, d'un matériau et d'un procédé. Les y faire dériver linéairement
   sous-dimensionnerait les grandes tailles sans qu'aucune erreur n'apparaisse.
2. **Sauf la quincaillerie.** Les cotes liées aux vis, roulements, inserts et
   servomoteurs sont fixes et viennent de `params/hardware.yaml`. Elles ne
   suivent jamais `H`.
3. **Noms d'articulations stables.** Ceux de `params/joints.yaml`, identiques
   dans la CAO, l'URDF et le code de contrôle. Jamais de variante locale.
4. **Rien de binaire dans Git.** Les STEP, STL, DXF, URDF et rendus vont dans
   `exports/`, qui est ignoré. Ils se régénèrent.
5. **Une décision structurante = une fiche** dans `decisions/`, écrite *avant*
   d'être appliquée. Jamais réécrite après coup.

## Après chaque génération de pièce

Produire un rendu de contrôle et le signaler. La géométrie produite par un
agent est régulièrement fausse de façon non évidente : trou décalé, épaisseur
insuffisante, collision entre pièces. Ne jamais présenter une pièce comme
correcte sans qu'elle ait été régénérée et regardée.

## Contraintes de fabrication à respecter dès la conception

**Procédé unique : la découpe 2D.** Il n'y a pas d'imprimante 3D
(fiche 0014). Architecture en plaques et entretoises (fiche 0015).

- **Toute pièce est plate**, d'épaisseur constante, issue d'un profil
  découpé. Un volume s'obtient par empilement de plaques et entretoises,
  jamais par une pièce massive.
- Pièce découpée : contour fermé, millimètres, échelle 1:1, rayon intérieur
  minimum 0,5 × épaisseur, aucun angle vif rentrant.
- Aucun logement de roulement obtenu directement par découpe : prévoir un
  palier rapporté ou un alésage repris.
- Assemblage démontable, aucun collage structurel. Pas de filetage dans le
  matériau : **vis traversante et écrou**.
- **Concevoir au plus contraignant**, c'est-à-dire au carton. Les trois
  procédés accessibles sont le cutter (carton), le laser de fablab
  (contreplaqué) et la découpe métal (aluminium). Un dessin qui ne passe
  pas en carton interdit l'itération rapide, qui est le principal acquis
  de cette architecture.
- **L'épaisseur et la saignée sont des paramètres, jamais des constantes.**
  Un même modèle génère un DXF par couple machine-matériau. La saignée se
  mesure sur une pièce d'essai, elle ne se suppose pas.

### Contraintes retirées le 2026-09-28, et pourquoi

Conservées ici : une contrainte caduque effacée en silence est une
information perdue, et rien ne signalerait son retour si une imprimante
était acquise.

- ~~« Pièce imprimée : tient dans 256 × 256 mm »~~ — c'était le volume
  d'une machine qui n'existe pas. **À rétablir telle quelle** si une
  imprimante est acquise, en vérifiant le volume réel de la machine.
- ~~« Filetage dans le plastique : insert à chaud, jamais taraudage
  direct »~~ — un insert à chaud se pose dans du thermoplastique imprimé.
  Ni le contreplaqué, ni le carton, ni l'aluminium n'en acceptent. Reste
  vraie pour toute pièce imprimée future.

## Environnement

- PC portable **sans carte graphique**, sous **WSL2** (Ubuntu 26.04). WSLg
  ouvre bien une fenêtre, mais n'expose aucun GPU : le rendu est logiciel
  (llvmpipe). Prévoir un rendu hors écran pour tout ce qui est répétitif.
- Entraînement par renforcement : jamais en local, toujours sur GPU distant.
- VPS Hetzner : régénération et publication seulement, pas de calcul.

### Deux interpréteurs Python — ne jamais les confondre

Voir `decisions/0002-pin-toddlerbot.md`.

| | Code YXOR | Pile ToddlerBot |
| --- | --- | --- |
| Venv | `~/yxor/.venv/` | `~/upstream/toddlerbot/.venv/` |
| Python | 3.14.4 | 3.12.14 (fourni par uv) |
| MuJoCo | 3.13.0 | 3.3.4 |

- Tout ce qui est dans ce dépôt se lance avec `.venv/bin/python` — **sauf
  `sim/upstream/`**, seul répertoire qui s'exécute avec le venv amont parce
  qu'il importe `toddlerbot` (fiche 0004). L'inverse est interdit dans les
  deux sens, et les deux sens sont vérifiés à l'exécution : `sim/upstream/`
  refuse de démarrer sous le mauvais interpréteur.
- ToddlerBot exige Python ≤ 3.12 : ses versions épinglées (`numpy==1.26.4`,
  `jaxlib==0.4.28`, `torch==2.3.1`) n'ont pas de roue pour 3.14. Ce n'est pas
  contournable sans maintenir un fork.
- Se tromper de venv donne soit un `ImportError`, soit — plus vicieux — une
  version de MuJoCo différente de celle sur laquelle les mesures ont été
  prises. En cas de doute : `python -c "import mujoco; print(mujoco.__version__)"`.
- Le code amont vit dans `~/upstream/`, **hors du dépôt**. Rien de ce qui s'y
  trouve ne doit être copié ou commité ici.

## Ce qu'il ne faut pas faire

- Proposer d'acheter du matériel avant la phase 6 du plan d'action.
- Avancer sur une phase suivante tant que la précédente n'est pas sortie.
- Introduire une dépendance **copyleft fort** (GPL, AGPL, CERN-OHL-S) dans le
  cœur du projet.

  ⚠ **Corrigé le 2026-09-29** (fiche 0029). Cette règle avait été écrite en
  croyant CERN-OHL-S non commerciale. **Elle ne l'est pas** : vendre est
  permis. Ce qu'elle impose est la **réciprocité** — publier les sources de
  tout dérivé sous la même licence. La règle tient donc toujours, mais pour
  le bon motif : ce n'est pas la vente qui serait empêchée, c'est le fait de
  garder nos propres plans fermés.

  **Deux familles à ne jamais confondre :**

  | Famille | Exemples | Vendre ? | Garder fermé ? |
  | --- | --- | --- | --- |
  | non commerciale | CC BY-NC, CC BY-NC-SA | **non** | — |
  | copyleft, réciproque | GPL, AGPL, CERN-OHL-S | **oui** | **non** |
  | permissive | MIT, Apache-2.0, BSD, ISC | oui | oui |

  La mécanique amont de ToddlerBot est en **CC BY-NC** : c'est la première
  famille, celle qui interdit la vente. C'est elle, et non la seconde, qui
  pèse sur les 1121 cotes d'origine `amont`.