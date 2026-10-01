# 0048 — Tailles Banc, S, M, L, XL ; premier robot S

Date : 2026-09-30
Espèce : gouvernante
État : acceptée
Statut : **acceptée** — décidée par Jeremy le 2026-09-30. **Non appliquée dans les paramètres** : les paliers P1/P2/P3 restent en place (question ouverte 8 du cadrage).
Découle de : `0047-demarche-inversee.md`

## La décision

Les tailles de YXOR sont définies **par classe d'actionneur de jambe** :
Banc, S, M, L, XL. La hauteur de chaque taille est un ordre de grandeur,
que le calcul de la fiche 0047 affine. **Le premier robot est S.**

## Où est le raisonnement

`docs/cadrage.md`, § 6 : le tableau des tailles, la justification du
premier robot S, et les arguments sur la classe de S. Le § 10 donne
l'échelle des capacités, le § 8 l'actionneur maison. Le registre (§ 12)
donne les alternatives écartées (P1/P2/P3 à hauteur fixe, premier robot
M) et la condition de réouverture.

## Ce qui reste ouvert

- **La classe de S** (EduLite 05, RS05 ou STS3250) n'est pas choisie :
  cadrage § 6, question ouverte 2, après l'étude des fournisseurs (§ 9).
- **Les paliers d'`anthropometry.yaml` ne sont pas modifiés.** Leur
  remplacement se fera par une fiche qui remplace la décision des
  paliers sans la réécrire (question ouverte 8).
