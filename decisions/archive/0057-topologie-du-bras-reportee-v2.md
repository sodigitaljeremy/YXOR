# 0057 — Topologie du bras : celle de la référence ToddlerBot, décision YXOR reportée à la v2

Date : 2026-09-30
Espèce : gouvernante
État : appliquée
Statut : **appliquée** — lot de cohérence validé par Jeremy le 2026-09-30 (~23 h), point 4. `params/joints.yaml` n'est pas modifié.
Remplace : `0005-topologie-bras-p1.md`

## Pourquoi remplacer la 0005

La 0005 adoptait la topologie de ToddlerBot, avec le lacet au coude
(`elbow_yaw`), **« pour le palier P1 »**, « réévaluable en P2 ». Or :

- les paliers n'existent plus (fiche 0055) ;
- **les bras ne font pas partie de la v1** : la v1 compte 12 degrés de
  liberté, les jambes seules (cadrage § 11).

## La décision

1. **`params/joints.yaml` garde la topologie de ToddlerBot**, avec le lacet
   au coude. C'est celle du **modèle de simulation de référence** : ses
   politiques et ses mouvements en dépendent. Les noms d'articulations
   ne changent pas (règle 3).
2. **La topologie des bras de YXOR sera décidée à la v2**, quand les bras
   entreront au programme (cadrage § 11 : 3 degrés de liberté par bras,
   2 au cou). Le déclencheur de « réévaluable en P2 » devient donc « la
   v2 ».
3. Les motifs de la 0005 restent vrais **pour la référence**. On ne change
   pas la topologie sans changer d'un coup la morphologie, la
   cinématique, les politiques et les masses.
