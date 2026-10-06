# Loi de masse : isométrique (H³) et allométrique (H^b)

**Engendré** par `.venv/bin/python scripts/loi_masse.py --ecrire`. Ne pas éditer à la main. **Étude, aucune décision** : la loi H³ reste celle des calculs existants ; l'allométrique est une VARIANTE (`params/lois_masse.yaml`, `dimensionnement.masse` avec `exposant`).

## Ajustement sur les bipèdes

Jeu de données robomechanics/robot-dataset (commit 3699af27, sans licence déclarée : hors du dépôt, au registre). bipèdes : types « full biped » et « lower biped » ; Tesla Optimus (« biped ») exclu par les auteurs, hybrides drone exclus. Variable : total_length_inm (longueur totale du corps, assimilée à H).

| Sélection | n | b | IC 95 % | A (kg) | R² |
| --- | ---: | ---: | --- | ---: | ---: |
| bipèdes | 31 | **1.995** | [1.814 ; 2.176] | 17.74 | 0.946 |
| humanoïdes complets seuls | 21 | 2.273 | [1.750 ; 2.796] | — | 0.813 |

Comparaison : fit_summary_powerlaw.txt du même dépôt : full biped b = 2,265 (n = 17), lower biped b = 1,957 (n = 10) ; leurs n diffèrent des nôtres (lignes exclues faute de données). Article : Oke et al., « Allometric Scaling Laws for Bipedal Robots », arXiv:2603.22560 (v5, 2026-09-21) : « bipedal robot mass generally scales with the length squared ».

L'intervalle EXCLUT 3 : sur les bipèdes recensés, la masse croît nettement moins vite que H³. Les humanoïdes complets seuls (n plus petit) ont un intervalle plus large, qui exclut encore 3 de justesse.

## Masse et couple au genou selon la loi

Référence : YXOR Lab = squelette actuel, 9.80 kg à 0.60 m (modèle de S, v3) ; le final = mêmes proportions agrandies. Couple au genou : référence prudente de la phase 3b, pointe τ* = 0.143 (Unitree G1), efficace τ* = 0.063 (Unitree G1), τ = τ*·M·g·H.

| Loi | H (m) | Masse (kg) | Genou, pointe (N·m) | Genou, efficace (N·m) |
| --- | ---: | ---: | ---: | ---: |
| isométrique (H³) | 0.6 | 9.8 | 8.2 | 3.6 |
| isométrique (H³) | 0.8 | 23.2 | 26.0 | 11.5 |
| isométrique (H³) | 1.0 | 45.4 | 63.6 | 28.1 |
| isométrique (H³) | 1.2 | 78.4 | 131.9 | 58.3 |
| allométrique b bas (1.814) | 0.6 | 9.8 | 8.2 | 3.6 |
| allométrique b bas (1.814) | 0.8 | 16.5 | 18.5 | 8.2 |
| allométrique b bas (1.814) | 1.0 | 24.8 | 34.7 | 15.3 |
| allométrique b bas (1.814) | 1.2 | 34.5 | 58.0 | 25.6 |
| allométrique b central (1.995) | 0.6 | 9.8 | 8.2 | 3.6 |
| allométrique b central (1.995) | 0.8 | 17.4 | 19.5 | 8.6 |
| allométrique b central (1.995) | 1.0 | 27.2 | 38.1 | 16.8 |
| allométrique b central (1.995) | 1.2 | 39.1 | 65.7 | 29.1 |
| allométrique b haut (2.176) | 0.6 | 9.8 | 8.2 | 3.6 |
| allométrique b haut (2.176) | 0.8 | 18.3 | 20.5 | 9.1 |
| allométrique b haut (2.176) | 1.0 | 29.8 | 41.7 | 18.5 |
| allométrique b haut (2.176) | 1.2 | 44.3 | 74.5 | 32.9 |

## Réserve sur la loi de couple

Oke et al. (arXiv:2603.22560, résumé LU le 2026-10-06) trouvent que le couple nécessaire pour marcher suit τ ∝ m·L. Ce résultat vient de **deux bipèdes de morphologie quasi passive**, reconstruits en simulation 3D et mis à l'échelle de 0,02 à 1,2 m. Un robot entièrement actionné comme YXOR, qui ne s'appuie pas sur sa dynamique naturelle, n'est pas garanti de suivre la même loi. L'actionnement par la seule hanche de ces marcheurs n'est PAS vérifié dans le résumé (article complet non lu). La phase 3b rend déjà ses couples en τ/(M·g·H), donc proportionnels à m·L ; c'est la même hypothèse, à confirmer sur YXOR lui-même.
