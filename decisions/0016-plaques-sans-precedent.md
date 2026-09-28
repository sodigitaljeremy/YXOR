# 0016 — L'architecture en plaques n'a aucun précédent open source

Date : 2026-09-28
Statut : acceptée
Amende : `0015-architecture-plaques-entretoises.md`

> **Note de procédure.** La règle 5 interdit de réécrire une fiche après
> coup. La 0015 n'est pas modifiée : elle reçoit un renvoi vers
> celle-ci, qui porte la correction.

## Ce qui était faux

La demande à l'origine de la fiche 0015 justifiait l'architecture en
plaques et entretoises par trois exemples : **Solo et Bolt** de l'Open
Dynamic Robot Initiative, et **Upkie**.

**Les trois sont imprimés en 3D.** Vérifié :

| Projet | Constat | Source |
| --- | --- | --- |
| ODRI Solo / Bolt | « mostly **3D printed** and off-the-shelves components » ; « two-part **3D printed** shell structures » ; STL fournis pour la structure | dépôt `open_robot_actuator_hardware` |
| Upkie | impression **PETG**, couches 0,2 mm, remplissage 15 à 30 %, sur Prusa i3 MK3S+ | dépôt `upkie/upkie_parts` et wiki de construction |

**Aucun des trois n'est construit en plaques découpées.**

### Ce que la fiche 0015 avait échappé

**La justification par l'exemple n'y figure pas.** Vérifié : ni Solo, ni
Bolt, ni Upkie, ni l'ODRI n'apparaissent dans le dépôt. La fiche 0015
raisonne uniquement à partir de la contrainte — pas d'imprimante, trois
procédés de découpe accessibles — et cette chaîne est intacte.

Ce qui manquait n'est donc pas une justification fausse à retirer, mais
un **constat absent à ajouter**.

## Décision

### 1. La décision de la fiche 0015 est maintenue

L'architecture en plaques et entretoises reste **imposée par l'absence
d'imprimante 3D** (fiche 0014), et par rien d'autre. Elle ne se justifie
par aucun précédent, et n'en a jamais eu besoin : c'est une contrainte
subie, pas un choix d'architecture.

### 2. Constat ajouté : aucun précédent accessible

> **Aucun projet de robot open source accessible ne construit sa
> structure par découpe 2D en plaques et entretoises.** Les trois
> références comparables impriment en 3D.

Ce constat n'invalide pas la décision. Il en **chiffre le coût** :

- **Rien à copier.** Chaque liaison, chaque montage de roulement, chaque
  fixation d'actionneur est à inventer et à valider.
- **Rien à comparer.** Aucune pièce de référence face à laquelle juger
  la nôtre — or c'est précisément ce que Jeremy cherchait pour
  apprendre à évaluer une pièce.
- **Aucune erreur connue.** Un précédent apporte surtout la liste des
  pièges déjà rencontrés par d'autres. Ici il n'y en a pas.

Ce coût doit être **visible** au moment de décider d'acheter ou non une
imprimante. Il n'est pas tranché ici.

### 3. Ce qui reste vrai de la fiche 0015

Tout le reste : la topologie tient au niveau `articulation`, 19 des 30
`actionnement` passent en découpe 2D, la bielle `neck_pitch` est le cas
d'école de la pièce plate, un modèle paramétrique produit un DXF par
couple machine-matériau, et l'épaisseur pilote la géométrie
d'assemblage.

## Conséquences

- Toute affirmation sur un projet tiers doit être **vérifiée à sa
  source** avant d'entrer dans une fiche. Celle-ci ne l'était pas ; elle
  n'a pas contaminé le dépôt parce qu'elle n'a pas été reprise, mais rien
  ne l'aurait empêché.
- La question « acheter une imprimante 3D ? » est **ouverte et
  instruite**, non tranchée. Voir le journal du 2026-09-28.
