# 0055 — ToddlerBot, référence de calcul ; les tailles remplacent les paliers

Date : 2026-09-30
Espèce : gouvernante
État : appliquée
Statut : **appliquée** — lot de cohérence validé par Jeremy le 2026-09-30 (~23 h), point 4 (D7 de `docs/arbitrage-2026-09-30.md`). Appliquée dans `params/anthropometry.yaml` et `parts/semelle_apprentissage.py`.
Remplace : `0001-base-toddlerbot.md`

## Pourquoi remplacer la 0001

Le **choix de ToddlerBot** tient toujours. En revanche, deux de ses
conséquences ne tiennent plus :

- **« Le palier P1 est fixé à H = 0,56 m »** : la démarche inversée
  (0047) et les tailles par classe (0048) font de la taille une
  **sortie** du calcul, pas une entrée.
- **La licence**, corrigée dans son corps le 2026-09-30 : c'est ce que
  la fiche 0054 interdit désormais.

## La décision

1. **ToddlerBot reste la base** : simulation, politiques, et **référence
   du dimensionnement inversé**. H0 = 0,56 m et M0 = 3,454 kg
   (`params/actionneurs.yaml`, `reference_toddlerbot`) sont les grandeurs
   que `scripts/dimensionnement.py` met à l'échelle. Les motifs du choix
   et les options écartées de la 0001 restent valables.
2. **Les paliers P1, P2 et P3 n'existent plus.** Dans
   `params/anthropometry.yaml`, ils sont remplacés par les **tailles** de
   la 0048 : S, M, L, XL. Leur hauteur est un **ordre de grandeur** (cadrage
   § 6), que le calcul de la 0047 affine. Correspondances :
   - S : 0,55 à 0,60 m (intervalle, la famille n'est pas choisie) ;
   - M : 0,80 m ;
   - L : 0,90 m ;
   - XL : plus de 1 m.
3. **La clé `H: 0,56` reste** : c'est la taille de **ToddlerBot**, d'origine
   `amont`. Ce n'est plus la taille de YXOR.
4. **Licence de la conception amont : CC BY-NC-SA 4.0.** Elle relève à la
   fois de la famille non commerciale et de la famille réciproque (fiche
   0061). Conséquence inchangée : **aucune géométrie amont n'entre dans
   une pièce YXOR.** La couverture des valeurs numériques reste une
   **question ouverte, sans avis** (0010 § 4).

## Ce que cela change

- **La semelle d'apprentissage**, dessinée au palier P2 (0,90 m), est
  désormais dessinée à la **taille L** (0,90 m) : même hauteur, même
  géométrie, 138,06 × 51,93 mm.
  - Son nom de fichier passe de `…_P2_…` à `…_L_…`.
  - L'option `--palier` devient `--taille`.
- Le P2 à 0,90 m et le P3 à 1,70 m n'avaient **aucune fiche**. Ils
  disparaissent avec les paliers, et l'ancien bloc reste en commentaire
  daté.
