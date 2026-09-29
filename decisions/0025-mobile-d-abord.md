# 0025 — Le site en mobile d'abord

Date : 2026-09-29
Statut : **proposée** — rien n'est codé.

Deux lecteurs : vous sur votre téléphone, votre cousin sur le sien, à
l'atelier. Référence de travail : **390 px de large**.

## Ce qui est mesuré

Largeur minimale de chaque tableau, contenu réel compris :

| Page | Tableau | Colonnes | Largeur | Verdict |
| --- | --- | ---: | ---: | --- |
| pièce | origines d'un rang | 5 | **~1 022 px** | 2,6 x l'écran |
| état | « se déduira » | 4 | ~836 px | 2,1 x |
| état | « ce que je peux faire » | 5 | ~726 px | 1,9 x |
| traçabilité | par origine | 4 | ~541 px | 1,4 x |
| pièce | cotes lettrées | 4 | ~519 px | 1,3 x |
| état | « à mesurer » | 3 | ~521 px | 1,3 x |
| **pièce** | **Fabrication** | **2** | **~422 px** | **1,1 x** |
| état / traçabilité | deux colonnes | 2 | 227 / 321 px | tiennent |

**Sept tableaux sur neuf débordent.**

## Défaut 1 — « Fixation » déborde : la cause est trouvée

Ce n'est pas un problème de largeur. C'est une **classe mal nommée
appliquée à du texte** :

```
td.num { text-align:right; font-variant-numeric:tabular-nums;
         white-space:nowrap }
```

Le tableau Fabrication met `class="num"` sur **toutes** ses valeurs, y
compris « vis traversante + rondelles larges des deux côtés » — 49
caractères. `white-space:nowrap` **interdit le retour à la ligne**, la
cellule réclame ~370 px, et l'en-tête de gauche est écrasé jusqu'à
disparaître.

Correction : `nowrap` ne doit valoir que pour les vraies valeurs
numériques. Séparer `.num` (aligné à droite, chiffres tabulaires,
insécable) de `.txt` (aligné à gauche, qui se replie). C'est une ligne de
CSS et une passe sur le générateur.

## Défaut 2 — un tableau à cinq colonnes doit-il rester un tableau ?

**Je tranche : cela dépend du tableau, et le critère est mesurable.**

La question n'est pas « tableau ou cartes ». C'est : **ce tableau
a-t-il une colonne qu'on parcourt verticalement ?**

- Si **oui**, le tableau existe pour permettre cette comparaison. La
  détruire, c'est détruire le tableau. Exemple : la colonne *Origine* du
  tableau des cotes — on la balaie pour voir combien sont `amont`. C'est
  tout l'objet de la page.
- Si **non**, ce n'est pas un tableau : c'est **une fiche déguisée**.
  Le tableau Fabrication oppose « Machine » à « Volume » — comparer ces
  deux lignes entre elles n'a aucun sens. Personne n'a jamais lu cette
  colonne de haut en bas.

| Tableau | Colonne parcourue ? | Décision |
| --- | --- | --- |
| Fabrication (pièce) | non — c'est une fiche | **empiler**, perte nulle |
| Cotes lettrées | oui — la lettre et la valeur | rester tableau |
| Origines par rang | oui — l'origine | rester tableau |
| « Ce que je peux faire » | oui — Dessiner / Couper | rester tableau |
| « À mesurer », « Se déduira » | oui — le nombre | rester tableau |
| Traçabilité par origine | oui — la part | rester tableau |

### Ce qu'on perd à empiler, chiffré

| Page | En tableau | Empilé | Facteur |
| --- | ---: | ---: | ---: |
| pièce | ~1 056 px | ~2 520 px | **x2,4** |
| état | ~792 px | ~1 942 px | **x2,5** |
| traçabilité | ~396 px | ~854 px | x2,2 |

Empiler **tout** multiplierait la hauteur des pages par deux et demi, et
supprimerait la comparaison verticale — qui est la raison d'être d'un
tableau de cotes. **Je le déconseille.**

### Ce que je propose à la place : réduire les colonnes, pas la forme

Pour les tableaux qui doivent rester des tableaux, sous 620 px :

- garder **les colonnes qu'on parcourt** — clé, valeur, origine ;
- **replier les colonnes de prose** (*Nature*, *Source*, *Pourquoi*,
  *Où*) **sous la ligne**, en seconde ligne de la même cellule, en
  petit — pas dans une colonne ;
- le tableau tient alors en **trois colonnes**, donc dans l'écran, et
  **rien n'est perdu** : la prose est toujours là, simplement sous la
  valeur au lieu d'être à côté.

C'est déjà ce que fait le tableau des cotes lettrées, où la clé est
affichée sous le libellé. La recette est connue et fonctionne.

Le conteneur défilant reste, mais en **filet de sécurité**, plus comme
mécanisme principal : vous avez raison qu'un tableau qui défile sur 390
px est illisible, parce qu'on perd la colonne d'en-tête en défilant.

## Défaut 3 — le schéma doit-il être zoomable ? Oui

C'est un **dessin technique lu sur un écran de poche** : la question ne
se discute pas. Deux précisions.

Le zoom de page **fonctionne déjà** — le `viewport` ne porte pas
`user-scalable=no`, vérifié. Mais il zoome *toute la mise en page* : on
perd la colonne, on se met à défiler dans les deux axes, et on ne
retrouve plus le tableau qui accompagne le dessin.

Ce qu'il faut est un zoom **du dessin seul**. Le SVG est vectoriel et
engendré par nous : il suffit de manipuler son `viewBox` au pincement et
au glissement. ~40 lignes, aucune dépendance, et la qualité ne se dégrade
pas — contrairement à une image.

Proposé : le schéma devient pinçable sur place, avec un bouton
« plein écran » qui l'ouvre seul, et un bouton de remise à zéro. Le
`touch-action` doit être posé explicitement sur le cadre du dessin,
sinon le navigateur intercepte le geste pour défiler la page.

## Défaut 4 — les cibles tactiles

Mesuré, hauteur effective :

| Élément | Hauteur | WCAG 2.5.8 (24 px) | Plateformes (44/48 px) |
| --- | ---: | --- | --- |
| liens de navigation | **~21 px** | **échoue** | échoue |
| curseur du simulateur | ~16-20 px (défaut) | **échoue** | échoue |
| bouton « Revenir aux valeurs » | ~34 px | passe | échoue |
| liens de téléchargement | ~37 px | passe | échoue |
| en-tête de rang dépliable | ~39 px | passe | échoue |
| bouton « Télécharger le DXF » | ~54 px | passe | passe |

**Deux échecs francs**, dont la navigation — présente sur toutes les
pages. Proposé : 44 px de hauteur minimale pour tout élément tactile,
curseurs compris ; c'est le seuil des plateformes, pas le minimum
d'accessibilité, et sur un dessin technique manipulé en atelier avec les
mains sales, le minimum ne suffit pas.

## Ordre proposé

1. `.num` / `.txt` — corrige « Fixation », une ligne de CSS.
2. Cibles tactiles à 44 px — CSS seul, aucun risque.
3. Fabrication empilé — c'est une fiche, pas un tableau.
4. Colonnes de prose repliées sous la ligne, sous 620 px.
5. Zoom du schéma.
6. Les sept curseurs à éprouver sur votre téléphone — je ne peux pas les
   essayer d'ici, et je ne prétendrai pas le contraire.

## La limite, encore

Aucun de ces défauts n'était visible depuis cette machine : ni
navigateur, ni écran. Les largeurs ci-dessus sont **calculées** à partir
du contenu réel, pas observées. Elles localisent le problème ; elles ne
remplacent pas votre téléphone.
