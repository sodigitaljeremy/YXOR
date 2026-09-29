# 0027 — La règle de la « phase 6 » n'a jamais eu de référent

Date : 2026-09-29
Statut : **proposée** — je ne tranche pas. Deux options, ma préférence
dite, la décision vous revient.

## Le constat

`CLAUDE.md` porte, depuis le premier jour :

> Proposer d'acheter du matériel avant la **phase 6 du plan d'action**.
> *(dans « Ce qu'il ne faut pas faire »)*

**Le plan d'action n'existe pas.** `README.md` y renvoyait
(`docs/02-plan-action.md`) ; le fichier n'a jamais été écrit. `docs/` ne
contient que `glossaire.md` et `lecture-modele.md`.

La règle est donc **inapplicable et invérifiable** : ni vous ni moi ne
pouvons dire où nous en sommes. Elle a pourtant produit un effet réel —
je m'y suis référé plusieurs fois pour ne rien proposer à l'achat. J'ai
obéi à un critère dont je ne pouvais pas constater l'état.

C'est la même faille que `site/` commité le jour où la fiche 0018
l'interdisait, prise par l'autre bout : là, une règle vraie que rien ne
vérifiait ; ici, une règle que rien ne peut vérifier.

## Ce que la règle protégeait réellement

Avant de la retirer ou de la réécrire, il faut nommer ce qu'elle
empêchait. À la relecture du journal, deux choses, qui n'ont rien à voir
entre elles :

1. **Acheter avant de savoir quoi acheter.** Le projet a passé une
   semaine à établir que les actionneurs ne pouvaient pas être
   dimensionnés sans enveloppes de couple. Acheter un servo au jugé
   aurait gaspillé l'argent **et** figé un choix.
2. **Que je propose des achats.** C'est un risque propre à un assistant :
   proposer une dépense est facile, et flatteur. La règle me musèle.

Ces deux protections sont légitimes. Les perdre serait un recul.

## Option A — retirer la règle

On constate qu'elle n'a pas de référent et on l'efface, en conservant la
trace barrée comme pour les contraintes de fabrication retirées.

**Pour** : honnête ; une règle invérifiable ne tient pas, et la garder
entretient l'illusion d'un garde-fou.

**Contre** : on perd les deux protections ci-dessus, et notamment la
seconde, qui ne dépend d'aucune phase.

## Option B — la reformuler sur un critère vérifiable dans le dépôt

Remplacer la phase par une condition que `regenerer.py` peut constater.
Proposition de rédaction :

> **Ne rien proposer à l'achat tant que la pièce concernée n'est pas
> `coupable`.** Une pièce est `coupable` quand toutes les cotes de son
> procédé sont renseignées — c'est le verdict que le site affiche déjà,
> et qu'un contrôle peut refuser.
>
> Corollaire : **l'achat est proposé par Jeremy, jamais par l'assistant.**
> Cette seconde phrase ne dépend d'aucun état du dépôt et reste vraie en
> toutes circonstances.

**Pour** : le critère est déjà calculé, déjà affiché, déjà outillé
(`etat_procede`). Il dit exactement ce que la phase voulait dire —
« ne pas acheter avant de savoir » — mais **pièce par pièce**, ce qui est
plus fin qu'une phase globale. Et la seconde phrase sauve la protection 2
sans dépendre de rien.

**Contre** : ne couvre que le matériel lié à une pièce. Une imprimante 3D
n'est liée à aucune pièce.

## Le cas qui se présente maintenant

Vous êtes sur le point d'acheter une imprimante 3D. Aucune des deux
options ne vous l'interdit, et je ne cherche pas à ce qu'elle vous
l'interdise — ce n'est pas mon rôle. Deux faits, sans avis :

- La fiche 0014 constate qu'il n'y a pas d'imprimante, et **CLAUDE.md
  conserve, barrées, les deux contraintes à rétablir le jour où il y en
  aurait une** : le volume de 256 × 256 mm (à vérifier sur la machine
  réelle) et l'insert à chaud plutôt que le taraudage direct. Elles ont
  été écrites pour ce jour-là.
- La DIN 8580:2022 range l'impression en **groupe principal 1**
  (*Urformen durch additive Fertigung*), quand toute l'architecture
  actuelle vit en **groupe 3** (*Trennen*). Ce n'est pas un procédé de
  plus : c'est un second groupe principal. La fiche 0015 et l'architecture
  en plaques seraient à réinstruire, pas à amender.

## Ma préférence, et pourquoi

**L'option B.** Retirer la règle serait propre mais ferait disparaître la
protection 2, qui n'a rien à voir avec les phases et qui est la seule à
me viser directement. La reformulation la conserve, et remplace un
critère fantôme par un critère que la machine sait constater.

**Mais c'est votre décision, pas la mienne** — c'est une règle qui
organise votre argent et mon comportement, pas une question technique.
