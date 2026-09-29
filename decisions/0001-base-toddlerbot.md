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
  Creative Commons **non commerciale**. Apprendre, modifier et publier sont
  permis ; vendre un dérivé ne l'est pas.
- À réévaluer seulement si une exploitation commerciale devient un objectif.
- Le palier P1 est fixé à H = 0,56 m par cette décision.