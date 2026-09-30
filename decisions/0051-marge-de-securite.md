# 0051 — Marge de sécurité de 1,5 sur le couple, à revoir après le banc

Date : 2026-09-30
Espèce : gouvernante
État : appliquée
Statut : **appliquée** — décidée par Jeremy le 2026-09-30 ; c'est la valeur par défaut de `dimensionnement.marge` dans `params/actionneurs.yaml`.

## La décision

Un actionneur doit pouvoir fournir **1,5 fois** le couple requis, pour le
couple continu (RMS) comme pour la pointe. Cette valeur n'est plus
provisoire. **Elle sera revue quand le banc aura mesuré le comportement
réel d'un actionneur**, thermique compris.

## Où est le raisonnement

`docs/cadrage.md`, § 4 : ce qu'est la marge, pourquoi il en faut une et
ce qu'elle coûte en taille. Le registre (§ 12) donne les alternatives
écartées (1,0 et 2,0) et la condition de réouverture : les résultats du
banc.

## Ce qui l'applique

`params/actionneurs.yaml`, `dimensionnement.marge: 1.5`, lu par
`scripts/dimensionnement.py`. Le commentaire de la clé disait « choix de
Jeremy à valider » ; il dit désormais « décidé ». L'option `--marge`
permet toujours d'explorer une autre valeur, sans changer la décision.

Ce n'est **pas une norme** : aucune norme n'a été consultée pour cette
valeur.
