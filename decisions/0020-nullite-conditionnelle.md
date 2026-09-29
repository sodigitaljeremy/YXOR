# 0020 — Trois états de la valeur absente

Statut : **acceptée** le 2026-09-29, à la demande de Jeremy, après un
défaut constaté sur le site en ligne.

## Le défaut

La fiche de la semelle affichait, dans le tableau Fabrication :

| Anisotrope | non |
| --- | --- |
| **Cannelures** | **non déterminé** (en rouge) |

Le carton-plume est une mousse : il n'a pas de cannelures. L'orientation
des cannelures n'est pas *à mesurer*, elle **n'existe pas**. Le site
annonçait un travail à faire là où il n'y en a aucun.

C'est l'inverse exact de la distinction que le projet tient partout
ailleurs depuis la fiche 0013 — `sans_objet` n'est pas `non_qualifie`.
Le site la perdait au moment de l'afficher.

## La cause, qui est plus générale que le symptôme

`val()` traitait TOUT `null` de la même façon : « non déterminé ».
Or un `null` a au moins trois sens différents, et les confondre fait
lire à l'un ce qui n'est vrai que de l'autre.

## La décision

Un `null` affiché déclare son **état**. Trois valeurs, et une seule par
défaut :

| État | Sens | Ce qu'on en fait |
| --- | --- | --- |
| `a_mesurer` | rien ne l'empêche, personne ne l'a fait | aller mesurer |
| `sans_objet` | la notion n'existe pas ici, **à cause d'un autre champ** | rien |
| `se_deduira` | **dérive d'un autre champ**, lui-même absent | remplir l'autre |

`a_mesurer` reste le **défaut** : un `null` non déclaré ressort en rouge.
C'est le même principe que `non_qualifie` dans l'audit — l'oubli se voit,
il ne se tait pas.

## Où la condition est déclarée

Dans `params/nullites.yaml`, par motif de chemin de clé, comme
`params/origines.yaml`. **Jamais dans le code du site** : la règle de la
fiche 0018 tient, l'application ne crée aucune donnée. Elle lit une
condition écrite dans `params/`, elle ne la devine pas.

Une règle porte une condition `si: {cle: <voisine>, vaut: <valeur>}`,
résolue parmi les clés **sœurs** de la valeur nulle. C'est ce qui permet
d'écrire « sans objet **parce que** `anisotrope` vaut `false` » plutôt
que « sans objet » tout court : le motif est affiché, pas seulement
l'état.

## Ce que cela remplace

Le filtre `not str(k).startswith(("source", "note", "axe", "mesure"))`
dans `page_etat`. Il faisait le bon tri pour la mauvaise raison — sur le
préfixe du nom, pas sur la nature du champ — et il aurait laissé passer
tout champ de prose nommé autrement.

## Limite assumée

Une condition ne porte que sur une clé **sœur**, pas sur un chemin
quelconque. Les cas réels rencontrés tiennent tous dans cette forme.
Le jour où l'un n'y tiendra pas, cette limite se verra : la règle ne
correspondra pas et le champ ressortira en rouge — c'est-à-dire du bon
côté.
