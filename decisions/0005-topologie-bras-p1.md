# 0005 — Topologie du bras en P1 : celle de ToddlerBot

Date : 2026-09-28
Espèce : close
État : amendée
Statut : acceptée
Amendée par : `0011-origine-litterature.md` — l'emprunt dimensionnel (H) est adossé au même palier P1 que l'emprunt topologique traité ici.

## Contexte

Le journal du 2026-09-20 relevait un écart entre `params/joints.yaml` et
le modèle amont. Les comptes concordent — 7 degrés de liberté par bras,
30 au total — mais le **découpage diffère**, et la question a été laissée
ouverte. Elle se tranche ici.

### L'écart, précisément

| `params/joints.yaml` | Amont `toddlerbot_2xc` |
| --- | --- |
| `shoulder_pitch` | `shoulder_pitch` |
| `shoulder_roll` | `shoulder_roll` |
| `shoulder_yaw` | `shoulder_yaw_drive` |
| `elbow` | `elbow_roll` |
| **`wrist_yaw`** | **`elbow_yaw_drive`** |
| `wrist_pitch` | `wrist_pitch_drive` |
| `wrist_roll` | `wrist_roll` |

Cinq lignes ne diffèrent que par le nom. **Une seule est un véritable
écart de structure** : le degré de liberté en *lacet* (rotation autour de
l'axe long du membre) est placé au **poignet** par `joints.yaml`, et au
**coude** par l'amont.

### Pourquoi la position de cet axe n'est pas un détail

Un « lacet » sur un bras, c'est la rotation du segment autour de son
propre axe — le geste qui tourne la paume vers le haut puis vers le bas.
Chez l'humain il se produit le long de l'avant-bras ; un robot doit
choisir une articulation précise où le loger. Ce choix a trois
conséquences mécaniques :

1. **Inertie.** Le moteur qui produit ce mouvement pèse. Placé au coude,
   sa masse est plus proche de l'épaule ; placé au poignet, elle est à
   l'extrémité du bras. Or l'inertie d'un segment en rotation croît avec
   le **carré** de la distance à l'axe : déplacer la même masse deux fois
   plus loin quadruple son effet résistant. Un moteur au poignet rend
   donc le bras nettement plus lourd à lancer et à arrêter, et exige plus
   de couple à l'épaule.
2. **Espace atteignable.** À nombre de degrés de liberté égal, l'ensemble
   des orientations que la main peut prendre n'est pas le même selon
   l'endroit où le lacet est placé.
3. **Encombrement.** Un moteur au poignet doit tenir dans un volume plus
   petit, ce qui contraint le choix de servomoteur — et la quincaillerie
   ne suit pas `H` (règle 2).

## Options examinées

| Option | Écartée pour |
| --- | --- |
| Conserver l'anatomie de `joints.yaml` (lacet au poignet) | Rend le modèle YXOR structurellement incompatible avec l'amont, donc avec ses politiques et ses mouvements |
| Découpage hybride | Cumule les inconvénients : incompatible avec l'amont *et* sans justification anatomique propre |
| Adopter la topologie amont | Retenue |

## Décision

**YXOR adopte pour le palier P1 la topologie articulaire de ToddlerBot.**
Le degré de liberté en lacet du bras est donc porté par le **coude**
(`elbow_yaw`), et non par le poignet (`wrist_yaw`).

### Motif

Modifier la topologie maintenant changerait **d'un seul coup** cinq
choses qui ne peuvent plus être démêlées ensuite :

- la **morphologie** — la forme et la répartition des segments ;
- la **cinématique** — les positions atteignables et les singularités ;
- les **inerties** — donc les couples requis et le dimensionnement des
  servomoteurs ;
- l'**espace d'action** — l'ordre et le sens des 30 commandes ;
- la **compatibilité des politiques** apprises.

Ce dernier point n'est pas théorique. Sur les dix politiques
téléchargées (fiche 0003), **neuf pilotent les bras** — leur
`action_parts` vaut `['leg', 'arm', 'waist', 'neck']` ; seule `walk` est
en jambes seules. Changer la topologie du bras invaliderait donc neuf
politiques sur dix, et il n'existe aucun moyen de les réentraîner ici :
cela exige un GPU distant.

Or la phase 2 vise l'inverse : **apprendre en modifiant des nombres, pas
la structure.** Un ratio que l'on change, dont on observe l'effet, et que
l'on compare — cela suppose que tout le reste soit tenu constant. Toucher
à la topologie avant d'avoir cette base de comparaison, c'est renoncer à
mesurer quoi que ce soit.

Adopter la topologie amont, c'est donc acheter une **référence
fonctionnelle** — un robot qui marche, dont on sait qu'il marche — contre
un renoncement temporaire à une anatomie propre.

### Ce que devient `params/joints.yaml`

Le fichier change de statut, et cela doit être dit sans ambiguïté :

> `params/joints.yaml` décrit désormais la **topologie ToddlerBot adoptée
> en P1**, et **non l'anatomie cible de YXOR**.

Ce n'est pas une description de ce que le projet veut construire à terme,
mais de ce sur quoi il s'appuie pour apprendre. La règle 3 continue de
s'appliquer pleinement : ces noms font foi de façon identique dans la
CAO, l'URDF et le code de contrôle.

**Réévaluable en P2**, et à ce moment seulement — quand une base de
comparaison existera et qu'un écart de topologie pourra être mesuré au
lieu d'être supposé.

## Conséquences

- `wrist_yaw` disparaît de la nomenclature YXOR en P1 ; `elbow_yaw`
  apparaît. Le compte reste de 7 degrés de liberté par bras.
- La **correspondance précise des axes** entre les deux nomenclatures
  n'est **pas** tranchée par cette fiche. Elle sera établie par
  extraction depuis le modèle amont épinglé, jamais par recopie ni par
  supposition — les butées de `joints.yaml` sont encore toutes à `null`,
  et une butée fausse produit une marche qui fonctionne en simulation et
  casse le robot réel.
- Cette décision est **liée au SHA d'ancrage** de la fiche 0002
  (`e337f3b177b4b53abff70b31d1695a7b66cc6d2e`) : elle décrit la topologie
  de ce commit-là.
- Le document de plan d'action (`docs/02-plan-action.md`) reste
  **absent** du dépôt. La description de la phase 2 retenue ici est celle
  énoncée par Jeremy le 2026-09-28 ; elle devra être confrontée au plan
  lorsqu'il sera récupéré.
