# 0054 — Une fiche acceptée ne se réécrit plus : elle est remplacée

Date : 2026-09-30
Espèce : gouvernante
État : acceptée
Statut : **acceptée** — validée par Jeremy le 2026-09-30 (~23 h), point 3 du lot de cohérence (décision D8 de `docs/arbitrage-2026-09-30.md`). Appliquée par les remplacements du même lot (point 4).

## La décision

**Une fiche acceptée ne se réécrit plus.** Quand ce qu'elle dit cesse
d'être vrai, une **nouvelle fiche la remplace** :

- la nouvelle porte, dans son en-tête, `Remplace : NNNN` ;
- l'ancienne reçoit **en tête** `Remplacée par : MMMM — raison`. **Son
  texte reste inchangé.**

## Ce qui peut encore bouger dans une fiche acceptée

**Seulement son en-tête**, parce qu'il décrit son cycle de vie (fiche
0036), pas son contenu :

- les lignes `Remplacée par` et `Amendée par` s'ajoutent ;
- la ligne `État` peut suivre le cycle de vie (proposée → acceptée →
  appliquée).

**Le corps, sous l'en-tête, ne change plus**, pas même par une section
datée ajoutée à la fin. Cette pratique, « l'amendement en ligne », a été
constatée sur 42 fiches sur 44 (`docs/etat-des-lieux-2026-09-29-nuit.md`
§ 2) et encore le 2026-09-30 (0001, 0042, 0044). **Elle cesse avec
cette fiche.**

Une fiche encore **proposée** n'est pas couverte : elle se corrige
jusqu'à son acceptation.

## Pourquoi

- **Un renvoi de ligne vers une fiche réécrite se décale** : c'est
  arrivé pour 0010 et 0011, qui pointent vers 0001.
- **Une fiche réécrite perd ce qu'elle a été** : on ne sait plus ce qui
  était cru, ni quand.
- **Une fiche corrigée ailleurs garde son erreur** : c'est le cas de 0004
  (« les deux sens ») et de 0029 (« CC BY-NC »). Le remplacement rend
  l'erreur visible là où on la lit.

## Ce qui l'outille

`scripts/index_fiches.py` lit les lignes `Remplacée par` et `Remplace`.
L'index affiche une fiche remplacée comme telle, et il **refuse** un
remplacement non réciproque : une fiche qui dit `Remplace : NNNN` alors
que NNNN ne dit pas `Remplacée par` cette fiche. Un test prouve que ce
refus sait échouer.

**Ce qui n'est PAS outillé** : rien n'empêche d'éditer le corps d'une
fiche acceptée. La règle tient par la conduite et par la relecture du
diff.
