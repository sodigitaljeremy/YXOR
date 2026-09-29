# 0031 — La rigidité en torsion se calcule, elle ne se stocke pas

Date : 2026-09-29
Espèce : historique
État : appliquée
Statut : **acceptée** — correction chiffrée.
Amende : `0022-soudure-instruction.md`.

## Ce qui était imprécis

La fiche 0022 affirmait qu'un caisson fermé gagne « un à deux ordres de
grandeur » de rigidité en torsion sur un U ouvert. **Présenter cela comme
un facteur est faux** : ce n'est pas une constante, c'est une fonction de
la section. Le retour extérieur a raison.

**Mais il ne faut pas l'affaiblir non plus.** Calculé, le chiffre réel
est plus élevé que ce que la 0022 annonçait.

## Le calcul, et d'où il sort

Pour une paroi mince, la constante de torsion de Saint-Venant vaut :

- **section fermée**, formule de Bredt-Batho : `J = 4·Am²·t / s`
- **section ouverte** (fendue) : `J = s·t³ / 3`

où `Am` est l'aire délimitée par la **ligne moyenne** de la paroi et `s`
le périmètre de cette même ligne. La rigidité en torsion est `G·J/L` :
tout le rapport passe donc par `J`.

L'intuition derrière les deux formules : dans une section **fermée**, le
couple est repris par un **flux de cisaillement qui fait le tour** — la
matière travaille sur tout le pourtour. Fendez la section, ce tour est
rompu ; il ne reste que la faible résistance de chaque paroi tordue
individuellement, qui varie comme `t³` et s'effondre dès que la tôle est
mince.

## Section 40 × 60 mm, tôle de 2 mm

Ligne moyenne 38 × 58 mm, donc `Am = 2204 mm²`, `s = 192 mm`.

| | J |
| --- | ---: |
| fermé | **202 401 mm⁴** |
| ouvert (fendu) | **512 mm⁴** |
| **rapport** | **395 ×** |

**Environ 400 fois, soit 2,6 ordres de grandeur.** La fiche 0022
annonçait « un à deux » : c'était **une sous-estimation**, pas une
exagération.

## La formulation à vérifier : elle est juste

> « Pour une paroi mince, le rapport fermé sur ouvert croît comme le
> carré du rapport périmètre/épaisseur. »

Algébriquement :

```
J_fermé / J_ouvert = 12·Am² / (s²·t²) = 12·(Am/s²)² · (s/t)²
```

Le facteur `(s/t)²` y est bien, et **la formulation est exacte à forme
constante**. Vérifié numériquement sur le cas ci-dessus : compacité
`c = Am/s² = 0,05979`, donc `12c² = 0,04289`, et `0,04289 × 96² = 395,3`
— le rapport calculé directement.

Le coefficient `12c²` dépend en revanche de **la forme** de la section,
pas de sa taille. Une section compacte gagne plus qu'une section aplatie.

## Pourquoi cela ne peut pas être une constante

Même épaisseur de 2 mm, sections différentes :

| Section | Rapport |
| --- | ---: |
| 25 × 25 | 99 × |
| 20 × 120 | 183 × |
| 40 × 40 | 271 × |
| **40 × 60** | **395 ×** |
| 80 × 120 | 1 654 × |

Même section 40 × 60, épaisseurs différentes :

| Épaisseur | Rapport |
| --- | ---: |
| 1 mm | 1 654 × |
| 2 mm | 395 × |
| 3 mm | 168 × |
| 5 mm | 55 × |

**De 55 à 1 654 sur ces seuls cas.** Stocker « le facteur » dans
`params/` serait exactement la faute que la règle 1 interdit : figer en
constante ce qui est une fonction.

## Ce qui est décidé

1. **Aucun facteur de torsion n'entre dans `params/`.** Le jour où une
   pièce en aura besoin, elle calculera `J` depuis sa propre section.
2. Une note de calcul, le moment venu, sera de **nature `tenue`** au sens
   de la fiche 0013 — elle ne dérive pas de `H`, et la règle 1 ne s'y
   applique pas.
3. La fiche 0022 reste telle quelle, avec un renvoi vers celle-ci. Elle
   n'est pas réécrite (règle 5).

## Deux réserves, qui vont dans le même sens

**Le calcul suppose le gauchissement libre.** Si les extrémités sont
bridées, une section ouverte reprend une part du couple par flexion
différentielle de ses parois, et son comportement réel est meilleur que
`J` seul ne le dit. Le rapport ci-dessus est donc une **borne haute**
pour une poutre courte et encastrée.

**Mais un U boulonné est pire qu'une section ouverte monolithique.** Les
plaques d'un U assemblé par vis **glissent l'une sur l'autre** dès que le
couple dépasse le frottement sous tête. Le calcul ci-dessus les suppose
d'un seul tenant. Le vrai U du projet est donc **en dessous** du `J`
ouvert calculé.

Les deux réserves ne s'annulent pas, elles portent sur des situations
différentes. Aucune ne change l'ordre de grandeur.

## Ce qui n'est pas corrigé, parce que ce n'était pas faux

La fiche 0022 dit que l'aluminium **T6 perd son revenu dans la zone
chauffée** et y retombe vers T4, soit environ la moitié de sa limite
d'élasticité. C'était **déjà donné comme non vérifié**, dans une fiche
dont le statut est « instruction, sans décision ». Ce n'est pas une
erreur à corriger : c'est une prudence à conserver telle quelle.
