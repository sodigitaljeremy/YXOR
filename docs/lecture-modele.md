# Lecture du modèle humanoïde d'exemple de MuJoCo

Fichier étudié : `sim/models/humanoid.xml`, copié tel quel depuis le dépôt
officiel MuJoCo (version 3.13.0, licence Apache-2.0). C'est le modèle de
démonstration de DeepMind, proche de notre cible en nombre d'articulations.
Pour le regarder : `python sim/view.py sim/models/humanoid.xml` (fenêtre)
ou `python sim/render.py sim/models/humanoid.xml exports/humanoid.png`.

## Vocabulaire, pour partir de zéro

- **Degré de liberté (DDL)** : un mouvement indépendant possible. Une porte
  a 1 DDL (elle pivote autour de ses gonds). Une épaule humaine en a 3.
- **Liaison pivot** (`hinge` dans MuJoCo) : rotation autour d'un seul axe,
  comme un gond. Toutes les articulations de ce modèle sont des pivots ;
  une articulation à 3 DDL (hanche) est simplement trois pivots empilés
  au même endroit, chacun avec son axe.
- **Axe de rotation** : donné par un vecteur `(x y z)` dans le repère du
  segment parent. `0 0 1` = axe vertical (le mouvement est une rotation
  « vue de dessus »). Le signe fixe le sens positif (règle de la main
  droite : pouce le long de l'axe, les doigts donnent le sens +).
- **Butées** (`range`, en degrés) : les deux angles extrêmes autorisés.
  Comme un coude humain : il plie beaucoup dans un sens, presque pas
  dans l'autre.
- **Articulation libre** (`freejoint`) : les 6 DDL du corps entier dans
  l'espace (3 translations + 3 rotations). Personne ne les « actionne » :
  c'est la gravité et les contacts qui les font bouger.
- **Actionneur** (`motor`, attribut `gear`) : le moteur qui applique un
  couple sur un pivot. `gear` est un facteur d'échelle du couple : la
  hanche en flexion a `gear=120`, la cheville `20` — les moteurs des
  jambes sont bien plus « forts » que ceux des bras, comme chez nous.

## Inventaire des articulations

21 pivots actionnés + 1 articulation libre (racine) = **27 DDL**, dont
21 commandés. Le squelette : torse → tête (fixe), deux bras à 3 DDL,
et vers le bas abdomen → bassin → deux jambes à 6 DDL.

Convention du modèle : x vers l'avant, y vers la gauche, z vers le haut
(la même que notre `params/joints.yaml`).

### Tronc (3 DDL)

| Nom | Axe | Butées | Mouvement humain |
| --- | --- | --- | --- |
| `abdomen_z` | z (vertical) | −45° / +45° | torsion du buste (regarder derrière soi sans bouger les pieds) |
| `abdomen_y` | y (transversal) | −75° / +30° | se pencher en avant (beaucoup) / se cambrer en arrière (peu) |
| `abdomen_x` | x (avant-arrière) | −35° / +35° | inclinaison latérale du buste |

### Jambe (6 DDL chacune, suffixes `_right` / `_left`)

| Nom | Axe | Butées | Mouvement humain |
| --- | --- | --- | --- |
| `hip_x_*` | x | −30° / +10° | écarter la jambe sur le côté (abduction) / la serrer (adduction) |
| `hip_z_*` | z | −60° / +35° | rotation de la jambe, pointe de pied vers l'intérieur ou l'extérieur |
| `hip_y_*` | y | −150° / +20° | lever le genou vers la poitrine (flexion) / tendre la jambe en arrière |
| `knee_*` | −y | −160° / +2° | plier le genou. Un seul sens utile : les +2° évitent un blocage numérique au voisinage de la jambe tendue |
| `ankle_y_*` | y | −50° / +50° | pointe de pied vers le bas (flexion plantaire) / vers le tibia (flexion dorsale) |
| `ankle_x_*` | oblique `(±1 0 ±0.5)` | −50° / +50° | rouler le pied vers l'intérieur / l'extérieur (inversion / éversion). L'axe est volontairement incliné, comme l'articulation sous-talienne réelle |

À noter : un **tendon** `hamstring_*` couple hanche et genou (comme nos
ischio-jambiers, muscles qui traversent les deux articulations) — plier
la hanche jambe tendue est limité, ce qui est très réaliste et purement
« gratuit » en simulation.

### Bras (3 DDL chacun)

| Nom | Axe | Butées | Mouvement humain |
| --- | --- | --- | --- |
| `shoulder1_*` | oblique `(±2 1 ±1)` | −85° / +60° | épaule, composante « lever le bras devant soi » |
| `shoulder2_*` | oblique `(0 −1 ±1)` | −85° / +60° | épaule, composante « écarter le bras du corps » |
| `elbow_*` | oblique `(0 −1 ±1)` | −100° / +50° | plier le coude |

Les axes d'épaule ne sont **pas** alignés sur x/y/z : deux pivots obliques
suffisent ici à couvrir l'essentiel de l'espace atteignable avec un DDL de
moins. C'est un raccourci de simulation, pas un choix mécanique réaliste.

### Ce que le modèle n'a pas

Pas de nuque (tête soudée au torse), pas de poignet, pas de main, pas de
troisième DDL d'épaule. Les axes des côtés gauche et droit sont inversés
en miroir (`hip_z_right` = `0 0 1`, `hip_z_left` = `0 0 −1`) : une même
commande positive produit un mouvement symétrique.

## Écarts avec `params/joints.yaml`

| Sujet | Humanoid MuJoCo | YXOR |
| --- | --- | --- |
| Total actionné | 21 DDL | 30 DDL |
| Nommage hanche | `hip_x/z/y` (par axe) | `hip_roll/yaw/pitch` (par mouvement) — même décomposition, autre vocabulaire |
| Épaule | 2 DDL, axes obliques | 3 DDL orthogonaux (`shoulder_pitch/roll/yaw`) |
| Poignet | absent | 3 DDL (`wrist_yaw/pitch/roll`) |
| Taille | 3 DDL (`abdomen_x/y/z`) | 2 DDL (`waist_yaw/roll`) — pas de flexion avant-arrière chez nous |
| Nuque | absente | 2 DDL (`neck_yaw/pitch`) |
| Cheville roll | axe oblique réaliste | axe x pur (`ankle_roll`) |
| Genou | pivot direct + tendon de couplage | pivot à liaison parallèle (moteur déporté), sans couplage |
| Suffixes | `_right`/`_left` en fin de nom | identique ✓ |
| Repère | x avant, y gauche, z haut | identique ✓ |

Deux points à garder en tête pour la suite :

1. **Les butées de ce modèle ne sont pas les nôtres.** `joints.yaml`
   l'impose : elles viendront de l'URDF ToddlerBot. Celles ci-dessus
   servent seulement d'ordre de grandeur plausible.
2. **La convention de miroir gauche/droite** (axes inversés ou non entre
   les deux côtés) n'est pas encore tranchée dans `joints.yaml`. Il
   faudra la fixer avant d'écrire l'URDF, sinon les signes des commandes
   seront incohérents entre CAO, simulation et contrôle.
