# 0047 — Démarche inversée : la classe d'actionneur fixe la taille

Date : 2026-09-30
Espèce : gouvernante
État : appliquée
Statut : **appliquée** — décidée par Jeremy le 2026-09-30 ; outillée par `scripts/dimensionnement.py`.

## La décision

On ne choisit plus une taille pour chercher ensuite des actionneurs.
Pour chaque **classe d'actionneur**, on calcule la **taille maximale**
qu'elle peut porter. La taille devient une **sortie** du calcul.

## Où est le raisonnement

**Dans le cadrage, pas ici** : `docs/cadrage.md`, § 2.1 (pourquoi la
taille en entrée était une erreur) et § 3 (la chaîne de calcul et ses
limites). Le registre (§ 12) donne l'alternative écartée : des tailles
humaines fixées a priori.

## Ce qui l'applique

- `scripts/dimensionnement.py` : le calcul inverse, la boucle sur la
  masse, le contrôle de cohérence qui refuse de conclure s'il échoue ;
- `tests/test_dimensionnement_coherence.py` : la preuve que ce contrôle
  sait échouer ;
- `docs/dimensionnement-par-actionneur.md` : les résultats du
  2026-09-30.

## Ce qu'elle ne fait pas

Elle ne touche pas aux paliers P1/P2/P3 d'`anthropometry.yaml`. Leur
remplacement est la **question ouverte 8** du cadrage (§ 13) ; voir
aussi la fiche 0048.

Écrite **après** l'application (commit `00af03a`) : le calcul a été
demandé et livré avant que la décision soit consignée. C'est dit plutôt
que maquillé.
