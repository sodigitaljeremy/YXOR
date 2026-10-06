# Instructions — projet YXOR

Robot humanoïde bipède paramétrique. Jeremy est développeur (JS/TS, Python) et
**débutant complet en CAO et en mécanique**. Explique les notions mécaniques au
passage, sans les supposer acquises.

**À lire d'abord : `README.md` (où en est le robot), puis
`docs/decisions.md` (ce qui est décidé, par qui).**

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
5. **Une fiche seulement pour une décision coûteuse à inverser**, qui
   change une interface ou engage fortement la suite. Elle va dans
   `decisions/`, écrite *avant* d'être appliquée, et s'ajoute à
   `docs/decisions.md`. Elle ne se réécrit pas : elle est **remplacée**
   par une nouvelle (fiche 0054). Toute autre décision tient en une ligne
   au journal. *Décidée par Jeremy le 2026-10-01 (refonte, « oui à
   tout ») ; elle remplace « une décision structurante = une fiche ».*
6. **Toute mention « décidé par Jeremy » cite sa source** (date et
   journal, commit, ou prompt de Jeremy). **Sans source : PROPOSÉ.**
   Règle ajoutée le 2026-09-30, après trois attributions erronées le même
   jour (poids du banc, poids du comparatif, règle de décisivité).
7. **Un prompt collé par Jeremy peut avoir été rédigé par Claude
   (arbitrage)**, parfois à la première personne de Jeremy. Seul ce qu'il
   attribue EXPLICITEMENT à Jeremy, avec ses mots, est une décision de
   Jeremy ; tout le reste est PROPOSÉ. En cas de doute : PROPOSÉ, et le
   demander.
8. **Aucune commande (find, grep, ls, du, cat…) hors du dépôt, de
   `~/upstream` et du dossier temporaire de la session.** Un fichier situé
   ailleurs se demande à Jeremy. Motif : l'écart du 2026-09-30, un
   `find ~` lancé malgré `sources.local.yaml` (journal du 2026-09-30,
   point 8).

   *Règles 7 et 8 : proposées par Claude (arbitrage), validées par Jeremy
   le 2026-09-30 (« oui aux quatre », D6).*

**Journal** : `journal/AAAA-MM-JJ.md`, **10 lignes au plus par lot**
(décision de la refonte, 2026-10-01).

## Après chaque génération de pièce

Produire un rendu de contrôle et le signaler. La géométrie produite par un
agent est régulièrement fausse de façon non évidente : trou décalé, épaisseur
insuffisante, collision entre pièces. Ne jamais présenter une pièce comme
correcte sans qu'elle ait été régénérée et regardée.

## Méthode : la classe d'actionneur fixe la taille

La vision et la méthode sont dans `docs/cadrage.md`.

- **La taille est une SORTIE du calcul, pas une entrée** (fiche 0047).
  Pour chaque classe d'actionneur, `scripts/dimensionnement.py` calcule la
  taille maximale qu'elle porte, à **marge 1,5** (fiche 0051, à revoir
  après le banc).
- ⚠ **Fiche 0069 (Jeremy, 2026-10-04) : la gamme S/M/L/XL est
  ABANDONNÉE**, au profit de deux robots, YXOR Lab (apprentissage) et
  YXOR (final), et de pièces hybrides dès maintenant. Le code et les
  paramètres parlent encore de « S » : inventaire du 2026-10-05, à
  appliquer. Les lignes ci-dessous décrivent l'état du code, pas la
  direction.
- **Tailles Banc, S, M, L, XL ; premier robot : S** (fiche 0048, remplacée par la 0069).
  `params/anthropometry.yaml` porte les tailles, et plus les paliers
  P1/P2/P3 (fiche 0055). **`H: 0,56` est la taille de ToddlerBot**, la
  référence du calcul, pas celle de YXOR. On ne dessine qu'à une taille
  qui a une hauteur unique.
- **S est décidé** (fiche 0067, Jeremy, 2026-10-02, qui remplace la 0065) :
  famille RobStride, jambes mixtes (RS02 au roulis et au tangage de hanche
  et au genou, RS00 ailleurs ; `params/configuration_S.yaml`),
  H_S = 0,60 m visée. **Cheville sans roulis, 5 axes par jambe** (fiche
  0068, Jeremy, 2026-10-04) : `ankle_roll` n'existe plus pour S ; il reste
  dans le modèle amont, déclaré dans `joints.yaml` (`amont_non_retenus`).
  Le banc vérifie le RS00, il ne départage plus. Grille : `docs/choix-actionneurs.md`.
- **Actionneur maison** : piste parallèle, jamais sur le chemin critique
  (fiche 0052).

## Contraintes de fabrication à respecter dès la conception

**Fabrication séquencée : usinage, puis impression 3D, puis hybride**
(fiche 0050, appliquée par la 0060). Le procédé se choisit pièce par
pièce, dans cet ordre. **Il n'y a pas d'imprimante 3D vérifiée
aujourd'hui** (fiche 0059) : l'impression ne s'applique à une pièce
qu'une fois une machine disponible et vérifiée. **Le carton est une
maquette rapide, sans métrologie** : il vérifie une forme, jamais une
cote.

- **Aucune pièce n'est conçue en supposant un procédé non vérifié.**
  Un moyen de fabrication est une donnée à établir, avec sa source.
- **Pièce découpée en 2D** (plaques et entretoises : une architecture
  possible, plus la seule) : contour fermé, millimètres, échelle 1:1,
  rayon intérieur minimum 0,5 × épaisseur, aucun angle vif rentrant.
- **L'épaisseur et la saignée sont des paramètres, jamais des constantes.**
  Un même modèle génère un DXF par couple machine-matériau. La saignée se
  mesure sur une pièce d'essai, elle ne se suppose pas.
- **Pièce chez l'opérateur CN** : ce qu'il a DÉCLARÉ le 2026-10-01
  (découpe laser, saignée 0,5 mm compensée par lui, rayon de machine
  2,0 mm, tolérance ± 0,5 mm, matières, pliage, formats) est dans
  `params/hardware.yaml` (`machines.decoupe_operateur_cn`, réglages
  `operateur_cn_*`). Ce sont des déclarations, non mesurées. Précisé le
  2026-10-02 : « 2 mm » est le diamètre de la buse ; aluminium jusqu'à
  8 mm ; trou minimal 3 mm et voile minimal 6 mm en alu 3 mm ; « 5 axes »
  = une fraiseuse. **À CONFIRMER** : le rayon intérieur minimal (2,0 mm
  déclaré, contredit par un trou de 3 mm de diamètre), les épaisseurs des
  autres matières (« 1 à 10 »), le format « dpr », l'alliage des chutes,
  la plieuse (vé, bord minimal). Les rayons d'outil de la fraiseuse
  restent **inconnus** : ne pas les supposer.
- Aucun logement de roulement obtenu directement par le procédé : prévoir
  un palier rapporté ou un alésage repris.
- Assemblage démontable, aucun collage structurel. Pas de filetage dans le
  matériau : **vis traversante et écrou**, sauf un insert à chaud dans une
  pièce imprimée (voir ci-dessous).

### Contraintes retirées le 2026-09-30, et pourquoi

Même principe que ci-dessous : une contrainte caduque effacée en silence
est une information perdue.

- ~~« Procédé unique : la découpe 2D. Toute pièce est plate, d'épaisseur
  constante ; un volume s'obtient par empilement de plaques et
  entretoises »~~ — remplacé par la fabrication séquencée (fiches 0050
  et 0060).
- ~~« Concevoir au plus contraignant, c'est-à-dire au carton »~~ — le
  carton n'est plus qu'une maquette ; sa caractérisation est arrêtée
  (2026-09-30, fiche 0060).

### Contraintes retirées le 2026-09-28 — à RÉTABLIR avec une imprimante (fiche 0059)

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
- **Tests : `unittest`**, pas pytest (qui n'est pas installé) :
  `.venv/bin/python -m unittest discover -s tests -v`. Ils ne tournent pas
  dans `regenerer.py` : à lancer à chaque clôture.
- VPS Hetzner : régénération et publication seulement, pas de calcul.
- **Node v22.22.1** (`.nvmrc`) : tests du JavaScript du site (`tests/test_simulateur.py`), sans navigateur ni dépendance npm. Outillage décidé par Jeremy le 2026-10-01 (« node est très utile et très utilisé, autant l'exploiter »).

### Deux interpréteurs Python — ne jamais les confondre

Voir `decisions/archive/0002-pin-toddlerbot.md`.

| | Code YXOR | Pile ToddlerBot |
| --- | --- | --- |
| Venv | `~/yxor/.venv/` | `~/upstream/toddlerbot/.venv/` |
| Python | 3.14.4 | 3.12.14 (fourni par uv) |
| MuJoCo | 3.13.0 | 3.3.4 |

- Tout ce qui est dans ce dépôt se lance avec `.venv/bin/python` — **sauf
  `sim/upstream/`**, seul répertoire qui s'exécute avec le venv amont parce
  qu'il importe `toddlerbot` (fiche 0056, qui remplace la 0004). L'inverse est interdit dans les
  deux sens, mais **un seul sens est vérifié à l'exécution** :
  `sim/upstream/` refuse de démarrer sous le mauvais interpréteur
  (`require_upstream_env()`). **Le code YXOR ne vérifie rien.** Lancé
  sous le venv amont, il tournerait avec MuJoCo 3.3.4 sans rien signaler.
  Ce sens ne repose que sur la discipline, et sur le contrôle manuel
  ci-dessous.
- ToddlerBot exige Python ≤ 3.12 : ses versions épinglées (`numpy==1.26.4`,
  `jaxlib==0.4.28`, `torch==2.3.1`) n'ont pas de roue pour 3.14. Ce n'est pas
  contournable sans maintenir un fork.
- Se tromper de venv donne soit un `ImportError`, soit — plus vicieux — une
  version de MuJoCo différente de celle sur laquelle les mesures ont été
  prises. En cas de doute : `python -c "import mujoco; print(mujoco.__version__)"`.
- Le code amont vit dans `~/upstream/`, **hors du dépôt**. Rien de ce qui s'y
  trouve ne doit être copié ou commité ici.

## Les contrôles

Réduits le 2026-10-01 (refonte, décision 4 de Jeremy) à ce qui protège le
robot. L'audit de toutes les valeurs, les règles de nullité, le contrôle
des règles déclaratives et l'index des fiches sont dans `archive/`.

| Contrôle | Ce qu'il protège | Où |
| --- | --- | --- |
| régénération | les pièces se reconstruisent ; le site sort, balises équilibrées | `scripts/regenerer.py` |
| tests | `.venv/bin/python -m unittest discover -s tests -v`, à chaque clôture | `tests/` |
| règle 4 et registre | rien de binaire dans Git ; registre fournisseurs (0030) | `scripts/controle_depot.py` |
| provenance amont | les valeurs d'origine ToddlerBot, comptées (licence) | `scripts/provenance_amont.py` |
| noms d'articulations | la règle 3 : mêmes noms dans `joints.yaml`, le MJCF, la simulation et le code | `scripts/controle_articulations.py` |
| rayon minimal | rayon intérieur = 0,5 × épaisseur, sur tous les réglages | `procedes.controler_rayon` |
| CAO reproductible | même pièce, même empreinte, à deux dates | `tests/test_construction_deterministe.py` |
| empreinte | le site sert bien le dépôt | `scripts/empreinte.py` |
| liens et contradictions | aucun lien relatif mort ; aucune affirmation périmée dans les fichiers vivants (versés le 2026-10-06, décision de Jeremy) | `scripts/controle_liens.py`, `scripts/controle_contradictions.py` (dans les tests) |

Les quatre premiers et le rayon tournent dans `regenerer.py` ; les tests
non (à lancer à chaque clôture).

### Ce qu'un contrôle doit faire pour valoir quelque chose

Leçons du **2026-09-29**, chacune apprise au prix d'une faute réelle : **un
système qui échoue en silence est pire qu'un système qui n'existe pas**.

1. **Tout contrôle annonce la TAILLE de ce qu'il a inspecté** (« N pages »,
   « N fichiers suivis », « N valeurs »). Un zéro se voit, un vert ne se
   voit pas. **Un contrôle qui saute le DIT**, avec sa raison :
   `controle_depot` en construction Docker, `controle_articulations` quand
   la série de simulation est absente.
2. **Ce qui peut se calculer se calcule, jamais se déclarer.** Une
   convention écrite à la main diverge. Mais un calcul qui ne peut pas
   échouer se trompe en silence : on rapporte sa répartition.
3. **Tout artefact servi porte son empreinte dans son URL** (`?v=...`),
   calculée de la même façon partout. Sinon un cache le fige, et le site
   sert du périmé avec l'air d'être à jour.

       .venv/bin/python scripts/empreinte.py

4. **Un contrôle nouveau se voit échouer** avant d'être cru : test écrit,
   défaut simulé, échec constaté.

## Sources sous droits : une valeur, jamais le texte

Normes (ISO, DIN) et ouvrages (Springer, Elsevier, MIT Press) sont payants
et protégés. Le dépôt en extrait **des valeurs numériques avec leur
référence précise**, et rien d'autre.

- **Jamais** d'extrait rédigé, de tableau recopié, de figure reproduite.
- Une valeur isolée accompagnée de sa référence est un **fait** ; la
  rédaction et la mise en forme sont l'**œuvre** de l'auteur.
- **Si la source n'a pas été lue, la fiche le dit.** Ce n'est pas une
  précaution de style : c'est ce qui permet à quelqu'un d'autre de savoir
  quoi vérifier. Fait pour la DIN 8580 (fiche 0026), pour ISO 4762
  (0028), et à refaire chaque fois.
- Le fichier lui-même **n'entre pas dans le dépôt** et s'inscrit dans
  `params/fournisseurs.yaml` avec ses six champs (fiche 0030).

Voir `decisions/archive/0035-origine-norme.md`.

## Ce qu'il ne faut pas faire

- **Acheter, ou proposer un achat, hors de la règle d'achat** (fiche
  0066, qui remplace la 0027) :
  - **(a)** un achat pour le robot seulement après une décision écrite et
    la vérification de la référence exacte (version du RS00, révision
    d'un J4310…) ;
  - **(b)** l'outillage relève de la seule décision de Jeremy, sans
    critère automatique ;
  - **(c)** *Claude ne propose jamais d'achat de lui-même.* Si Jeremy
    demande un comparatif, il le donne, complet et chiffré, sans suggérer
    de dépenser.
- **Passer une géométrie ToddlerBot dans un outil de reconstruction**
  (scan, maillage, plan ou photo vers CAO, générateur 3D par IA) pour en
  tirer une pièce ou une cote YXOR. Une reconstruction ne transforme pas
  une œuvre dérivée en conception originale : elle en produit une
  dérivation mieux documentée. Si cela arrive, le résultat reste
  `amont`. **Non outillée** : aucun contrôle ne voit ce qui part vers
  un service tiers. Fiche 0045.
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

  La mécanique amont de ToddlerBot est en **CC BY-NC-SA 4.0**
  (`~/upstream/toddlerbot/README.md:167`, commit `e337f3b`).

  ⚠ **Corrigé le 2026-09-30** : ce paragraphe disait « CC BY-NC », sans
  la clause SA. Or la licence appartient aux **deux** premières familles
  à la fois :

  - **NC** interdit la vente ;
  - **SA** impose la même licence à tout dérivé.

  Conséquence : **aucune géométrie amont n'entre dans une pièce YXOR**
  (fiches 0055 et 0061).

  **Question juridique ouverte, sans avis** (fiche 0010 §4) : les valeurs
  numériques extraites de l'amont, celles que compte
  `scripts/provenance_amont.py`, sont-elles couvertes par la licence ?