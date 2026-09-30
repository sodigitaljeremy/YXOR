# 0061 — Trois familles de licences ; la conception de ToddlerBot est dans deux

Date : 2026-09-30
Espèce : gouvernante
État : appliquée
Statut : **appliquée** — lot de cohérence validé par Jeremy le 2026-09-30 (~23 h), point 4. CLAUDE.md et le README portent déjà ce texte.
Remplace : `0029-familles-de-licences.md`

## Pourquoi remplacer la 0029

La 0029 classe correctement CERN-OHL-S : elle est **réciproque, pas non
commerciale**. Mais son corps dit que la mécanique de ToddlerBot est en
**« CC BY-NC »**, donc dans la seule famille non commerciale. La licence
amont est **CC BY-NC-SA 4.0** (`~/upstream/toddlerbot/README.md:167`,
commit `e337f3b`). C'est corrigé dans CLAUDE.md et dans la 0001, mais la
0029 garde l'erreur.

## La décision

1. **Trois familles**, comme dans la 0029 :

   | Famille | Vendre | Garder fermé |
   | --- | --- | --- |
   | non commerciale (NC) | non | — |
   | copyleft, réciproque (SA, GPL, CERN-OHL-S) | oui | non |
   | permissive (MIT, Apache-2.0, CERN-OHL-P) | oui | oui |

   Il faut y ajouter la **réciprocité faible**, que la 0029 citait sans
   la classer : CERN-OHL-W, LGPL. Il faut republier ses modifications de
   l'œuvre, pas son produit entier.
2. **La conception de ToddlerBot, CC BY-NC-SA 4.0, relève de DEUX
   familles** :
   - **NC**, qui interdit la vente d'un dérivé ;
   - **SA**, qui impose la même licence à tout dérivé.
3. **Conséquence, inchangée** : aucune géométrie amont n'entre dans une
   pièce YXOR. Les fichiers qui portent des valeurs extraites sont
   signalés dans le README (« Provenance et licences »). L'audit compte
   **1 124 valeurs `amont`** (2026-09-30).
4. **La règle « pas de copyleft fort dans le cœur » vise les
   dépendances**, pas la licence que Jeremy donne à son propre travail.
5. **Non tranché** : la couverture des valeurs numériques extraites
   (0010 § 4), et la licence propre de YXOR (fiche 0053 : aucune pour
   l'instant).
