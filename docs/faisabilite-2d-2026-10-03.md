# Faisabilité « tout en 2D » du robot S — 2026-10-03

**Rapport, rien n'est implémenté ni décidé.**

**Intention de Jeremy** (2026-10-02, ses mots) : « je veux absolument que
l'on passe à la pratique et que l'on commence à modéliser et concevoir le
robot complet (jambes, tronc, bras, cou, tête) ». D'abord en « full 2D
(full carton) », puis en découpe 2D métal. Ce n'est pas une décision
d'architecture : ce rapport en établit la faisabilité.

**Bases du rapport :**

- le squelette `params/squelette.yaml`, à H_S = 0,60 m (v3, 28 DDL,
  hypothèse) ;
- la configuration des jambes de la fiche 0067 ;
- les cotes de montage des RS00, RS02 et RS05 (`params/actionneurs.yaml`,
  `cotes_montage`, plans cotés relus) ;
- les réglages `cutter_cartonplume_5` et `operateur_cn_alu_3`
  (`params/hardware.yaml`).

**Vocabulaire :**

- une **chape** est un étrier en U : deux plaques parallèles reliées par
  des entretoises, qui tiennent un axe des deux côtés ;
- une **équerre** relie deux plaques à 90° ;
- la **torsion** est la rotation d'un segment sur son propre axe sous un
  couple : c'est le défaut typique des structures en plaques.

## 1 — Ce que disent les chiffres, avant tout dessin

1. **Les trous de fixation des actionneurs ne se découpent pas dans le
   carton plume de 5 mm.**
   - Le passage d'une vis M3 fait 3,4 mm (`hardware.yaml`, `vis.M3`).
   - Le plus petit trou découpable vaut 2 × 2,5 = 5 mm (rayon minimal
     0,5 × épaisseur).
   - Les 23 trous des trois gabarits sont donc à **pointer, puis reprendre
     au foret**.

   En aluminium de 3 mm chez l'opérateur, un trou de 3,4 mm est au-dessus
   du minimum déclaré (3 mm). Mais la contradiction entre son rayon
   minimal de 2,0 mm et ce trou de 3 mm reste ouverte (`hardware.yaml`,
   `contradiction_trou_rond`).
2. **Une plaque au diamètre de l'actionneur n'a presque pas de matière
   autour des trous.**

   | Actionneur | Trou → bord | Diamètre de plaque minimal (bord de 6 mm) |
   | --- | ---: | ---: |
   | RS00 | 1,8 mm | 65,4 mm |
   | RS02 | 1,05 mm | 88,4 mm |
   | RS05 | 0,55 mm | 56,9 mm |

   Le voile minimal déclaré par l'opérateur est de 6 mm. Les plaques de
   fixation doivent donc **déborder** l'actionneur, ce qui fait la colonne
   de droite.
3. **La phase angulaire des motifs de trous n'est pas inscrite au
   catalogue.** Les gabarits placent le premier trou à 0°. Il faut la
   relever sur l'actionneur ou sur le plan avant toute découpe.
4. **Trois axes au même point, à la hanche et à la cheville.**
   - À la hanche : lacet en RS00 Ø57 × 51, roulis et tangage en RS02
     Ø78,5. À la cheville : deux RS00.
   - Le squelette les place au même point : leurs volumes se recouvrent
     (169 contacts entre géométries au repos dans MuJoCo).
   - Il faudra des **décalages** entre axes. Ils allongeront les segments
     et déplaceront le centre de masse.
5. **Les bras traversent les hanches.**
   - Avec la largeur d'épaules d'ANSUR (0,2328 × H = 140 mm), les bras
     pendent à ±70 mm.
   - Les RS02 de hanche s'étendent jusqu'à ±100 mm.
   - Il faut des épaules plus larges que l'anthropométrie, ou des bras
     déportés vers l'extérieur.
6. **L'avant-bras et la main sont trop courts pour leurs actionneurs.**
   - L'avant-bras fait 91 mm. Il porte le tangage et le roulis du
     poignet : deux RS05 de Ø46 × 44.
   - La main fait 66 mm et porte la pince, un RS05 de plus.
   - L'empilement ne tient pas dans ces longueurs.
7. **La structure ne pèse que 1,6 kg dans le modèle de S en v3**, contre
   7,3 kg d'actionneurs (`scripts/squelette.py`).
   - C'est la structure imprimée de ToddlerBot, mise à l'échelle.
   - Une structure en plaques d'aluminium sera probablement plus lourde.
     Il faudra la peser sur une CAO, puis recalculer la grille de S.

## 2 — Segment par segment

| Segment | Longueur à 0,60 m | Plaques et entretoises ? | Fixation de l'actionneur | Ne passe pas en 2D | Torsion, trous à reprendre |
| --- | ---: | --- | --- | --- | --- |
| Pied | 92 mm | **oui** : semelle et contre-plaque, entretoises | chape en U sous la cheville, sur la sortie du RS00 du roulis | — | contre-plaque peu sollicitée ; trous M3 au foret (carton) |
| Tibia | 136 mm | **oui** : deux plaques parallèles, entretoises | carter du RS02 du genou boulonné sur une plaque (9 × M3 sur Ø73) ; sortie sur l'autre | logement de roulement côté opposé à la sortie : palier rapporté, alésage repris | segment long, en torsion à cause des chapes : entretoises rapprochées et plaques fermées en caisson |
| Cuisse | 149 mm | **oui** : comme le tibia | RS02 du tangage de hanche en haut ; sortie du RS02 du genou en bas | idem (paliers) | **torsion maximale** : le couple de hanche et la réaction du sol s'y croisent ; caisson fermé recommandé |
| Bassin | largeur 122 mm | **en partie** : plaque supérieure et flancs à 90° | lacet de hanche (RS00) à axe vertical, puis roulis et tangage (RS02) à axes horizontaux | les **trois axes perpendiculaires** demandent des plaques à 90° : équerres vissées, assemblage à tenons et mortaises, ou pliage (R 5 mm déclaré, 5754 seulement) ; MEVITA y a recouru au soudage | jonctions à 90° : maillon faible ; aucun collage structurel (CLAUDE.md) |
| Tronc | 183 mm | **oui** : boîte de plaques et entretoises | lacet et roulis de taille (RS05) en bas, cou en haut, épaules sur les flancs | — | boîte fermée, rigide ; logement de la charge utile (1,2 kg) |
| Épaule | — | **en partie** | tangage puis roulis d'épaule (2 RS05 à axes perpendiculaires) | même problème que le bassin : axes à 90° | équerres ; déport latéral à prévoir (§ 1, point 5) |
| Bras | 115 mm | **oui** : deux plaques | RS05 du roulis d'épaule en haut, RS05 du coude en bas | — | court, peu exposé à la torsion |
| Avant-bras et main | 91 et 66 mm | **oui**, mais trop courts | deux RS05 du poignet et un RS05 de pince | la **pince** est un mécanisme (crémaillère ou bielles), pas une plaque : non traitée ici | longueurs à revoir (§ 1, point 6) |
| Cou | 31 mm | **en partie** | lacet et tangage du cou (2 RS05 à axes perpendiculaires) | axes à 90° : équerre | — |
| Tête | 78 mm | **oui** : boîte | sur la sortie du RS05 du tangage du cou | caméra : support à concevoir | — |

**Lecture.**

- **Les segments simples** (pied, tibia, cuisse, bras, tronc, tête) se
  font bien en plaques et entretoises. L'actionneur est boulonné par son
  carter sur une plaque, et sa sortie l'est sur la plaque du segment
  suivant.
- **Les liaisons à deux ou trois axes perpendiculaires** (bassin, épaules,
  cou, chevilles) demandent des assemblages à 90°. C'est le point dur du
  « tout en 2D ».
- **Le carton plume** vérifie les formes et les débattements. Il ne porte
  aucun couple d'un RS02 : il ne doit **jamais** être mis sous tension.

## 3 — Précédents open source LUS

| Projet | Lu | Ce qu'il en dit |
| --- | --- | --- |
| **MEVITA** (JSK, Université de Tokyo, Humanoids 2025), [page](https://haraduka.github.io/mevita-hardware/), [dépôt](https://github.com/haraduka/mevita) (licence MIT, API GitHub), [arXiv 2508.17684](https://arxiv.org/abs/2508.17684) | page, README, article (p. 1 à 4), le 2026-10-03 | Bipède de 19,8 kg, 5 axes par jambe, actionneurs CubeMars AK70-10 et AK10-9. **18 pièces métalliques uniques**, dont **4 en tôle soudée** : base, hip1, hip2, support de moteur du mollet. Tôle A5052, pièces usinées en A7075, inox SUS304 pour certaines tôles. La base fait 300 × 320 × 150 mm d'un seul tenant. **Le précédent le plus proche : il n'est pas « tout plat »**, il plie et il soude, précisément aux hanches. |
| **ToddlerBot** (arXiv 2502.00893v1) | au registre, lu le 2026-10-01 | Conception « entirely 3D-printed » (p. 1) : aucune plaque. Ce n'est pas un précédent 2D, et sa géométrie n'entre pas dans YXOR (fiche 0061). |
| **Lynxmotion BRAT** (équerres en aluminium plié) | **non lu** : page en 403, protection anti-robot | Seulement un résumé de moteur de recherche (équerres « Servo Erector Set », 3 axes par jambe) : non retenu. |

## 4 — Ce que cela suggère (PROPOSÉ, non décidé)

1. **Commencer en carton** par la jambe seule, pied → cuisse, qui passe en
   2D, avec des actionneurs factices : volumes `actionneur_*.step`,
   gabarits de perçage `actionneur_*_gabarit_*.dxf`.
2. **Traiter les liaisons à axes perpendiculaires comme une question à
   part** :
   - équerres vissées ou tenons-mortaises en 2D pur ;
   - ou pliage (5754 H111 seulement en 3 mm, R 5 mm) ;
   - ou pièce usinée (fraiseuse de l'opérateur, rayons d'outil inconnus).

   À trancher avant le métal.
3. **Revoir dans le squelette** les longueurs d'avant-bras et de main, la
   largeur d'épaules et les décalages des axes de hanche et de cheville,
   avant tout dessin du haut du corps.
4. **Peser une première structure en aluminium** et remplacer l'hypothèse
   de 1,6 kg dans la grille de S.

## 5 — Ce qui n'est pas fait

- **Aucune pièce de structure n'est dessinée** : seuls des actionneurs
  factices le sont.
- **La pince n'est pas étudiée.**
- **FreeCAD n'est pas installé** sur cette machine. Rien n'a été installé,
  et l'ouverture des STEP dans FreeCAD n'est pas vérifiée.
- **Le squelette ignore les butées articulaires et les collisions entre
  corps** : il vérifie la cinématique et les masses, pas l'encombrement.
