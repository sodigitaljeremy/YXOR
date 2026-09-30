# 0059 — Pas d'imprimante 3D aujourd'hui ; l'impression est l'étape 2 de la fabrication

Date : 2026-09-30
Espèce : gouvernante
État : acceptée
Statut : **acceptée** — lot de cohérence validé par Jeremy le 2026-09-30 (~23 h), point 4. Rien n'est imprimé : aucune machine.
Remplace : `0014-pas-d-imprimante-3d.md`

## Pourquoi remplacer la 0014

Sa décision 1 dit : « L'impression 3D sort du périmètre de conception
tant qu'aucune machine n'est disponible ». La fabrication séquencée
(0050) fait de l'impression **l'étape 2** : usinage, puis impression,
puis hybride.

## La décision

1. **Le fait tient** : le dépôt ne connaît **aucune imprimante 3D
   disponible et vérifiée**. Une mention « Jeremy en achète une cette
   semaine » (0027, `hardware.yaml`) n'est confirmée nulle part.
2. **L'impression 3D rentre dans le périmètre**, comme **deuxième étape**
   de la 0050. Elle **ne s'applique à une pièce** que lorsqu'une machine
   est disponible et vérifiée : c'est le déclencheur.
3. **À ce moment-là**, les contraintes retirées le 2026-09-28 sont
   **rétablies**, en vérifiant la machine réelle :
   - le volume utile de la machine, et non plus 256 × 256 mm ;
   - un insert à chaud dans le thermoplastique, jamais de taraudage
     direct.

   Elles sont gardées dans CLAUDE.md.
4. **Les décisions 2 et 4 de la 0014 sont maintenues** :
   - aucune pièce n'est conçue en supposant un procédé non vérifié ;
   - ToddlerBot est la référence de **simulation**, pas de construction.
