# 0001 — ToddlerBot comme base de départ

Date : 2026-09-20
Espèce : historique
État : appliquée
Statut : acceptée

## Contexte

Le projet vise un humanoïde bipède autonome. Partir d'une feuille blanche
représenterait plusieurs années avant le premier pas. Une base open source
existante permet d'apprendre par modification plutôt que par création.

## Options examinées

| Option | Écartée pour |
| --- | --- |
| Open Duck Mini | Anatomie de canard, non transférable vers un humanoïde |
| Berkeley Humanoid Lite | Actionneurs imprimés jugés trop fragiles par ses auteurs |
| Unitree | Produit commercial, mécanique fermée |
| Asimov 1 | Paquet de reconstruction incomplet, échelle P3 |
| ToddlerBot | Retenue |

## Décision

ToddlerBot (Stanford). 0,56 m, 3,4 kg, 30 DDL actifs, nomenclature sous 6000 $.

Motifs : anatomie humanoïde réelle, pile logicielle entièrement Python
installable par pip, chaîne complète documentée du jumeau numérique au
déploiement, projet activement maintenu, robustesse reconnue.

## Conséquences

- Le code amont est sous licence MIT ; les fichiers mécaniques sont sous
  **CC BY-NC-SA 4.0**. Apprendre, modifier et publier sont
  permis ; vendre un dérivé ne l'est pas.

  *Corrigé le 2026-09-30 : la licence était désignée « Creative Commons
  non commerciale », sans sa clause SA.* Ligne exacte du README amont au
  commit `e337f3b` (`README.md:167`) :

  > The ToddlerBot design (Onshape document, STL files, etc.) is released
  > under the [...] CC BY-NC-SA [...], which allows you to use and build
  > upon our work non-commercially.

  **Conséquence de la clause SA** : un dérivé doit être publié sous la
  même licence, donc **aucune géométrie amont n'entre dans une pièce
  YXOR**. Si une géométrie amont y entrait, la pièce hériterait de la
  licence NC-SA.

  **Question juridique ouverte, sans avis ici** (fiche 0010 §4) : les
  valeurs numériques extraites de l'amont (butées, rapports, axes)
  sont-elles couvertes par la licence ?
- À réévaluer seulement si une exploitation commerciale devient un objectif.
- Le palier P1 est fixé à H = 0,56 m par cette décision.