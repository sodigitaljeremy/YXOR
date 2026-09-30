# 0049 — Les scripts de chiffrage sont versionnés, les séries se régénèrent

Date : 2026-09-30
Espèce : close
État : appliquée
Statut : **appliquée** — décidée par Jeremy le 2026-09-30 ; faite au commit `d6a00a0`.

## La décision

Tout script qui produit un chiffre d'exigence ou de dimensionnement vit
dans le dépôt. Les séries qu'il produit restent dans `exports/`, hors
Git, et **se régénèrent**.

## Où est le raisonnement

`docs/cadrage.md`, registre (§ 12) : refaire le calcul quand les
hypothèses changent. L'alternative écartée était de laisser les scripts
hors dépôt, comme ils l'avaient été pour le premier chiffrage de
`docs/exigences-actionnement-P2.md`.

## Ce qui l'applique

- `sim/upstream/enregistrer_marche.py` : la marche de référence. Il est
  dans `sim/upstream/` et **non dans `scripts/`**, parce qu'il importe
  `toddlerbot` et tourne avec le venv amont (fiche 0004) ;
- `scripts/analyser_marche.py` et `scripts/dimensionnement.py` ;
- la preuve de régénération : la série refaite par le script versionné
  a le même sha256 que celle de départ (`3de8ca2050a16667…`).

Écrite **après** l'application.
