# Estimation thermique du Damiao J4310 V1.2 — au bureau, sans achat

**Statut : ESTIMATION, pas une mesure.** Rédigé le 2026-09-30. Rien de ce
document n'est inscrit dans `params/mesures.yaml` : une estimation tirée
d'une courbe numérisée n'est pas un acte de mesure (fiche 0041).
Régénérer : `.venv/bin/python scripts/estimation_thermique.py`.

Statuts : **V** = lu ou calculé (script versionné) ; **Déd** = raisonnement.

---

## 1 — La question

Dans le comparatif des familles, **k** est le rapport entre le couple
continu réel d'un actionneur et son nominal publié. Pour le J4310, la
condition de mesure du nominal (3,5 N·m) n'est pas publiée : k y est une
**hypothèse**, balayée de 1,0 à 0,3. La famille Damiao gagne tant que
**k ≥ 0,50** (`docs/choix-famille-actionneurs.md`).

Peut-on estimer k **sans acheter d'actionneur**, à partir de ce que
Damiao publie ?

> **Mise à jour du 2026-09-30, 22 h 30.** Les tableaux ci-dessous ont été
> calculés au seuil de **100 °C**, la protection recommandée. Le script
> prend désormais **le seuil du protocole de banc** : 100 °C moins
> 10 °C, soit **90 °C**. C'est un seul seuil pour l'estimation et pour la
> mesure, lu dans `params/`.
>
> À 90 °C, **k ≈ 0,86–0,95** (médiane 0,90), au lieu de 0,92–1,02.
> Décoté au blocage, il vaut **0,53–0,81**, au lieu de 0,57–0,87.
>
> Le comparatif lit ces valeurs à la source
> (`estimation_thermique.estimer()`) : plus rien n'est recopié. Le
> texte ci-dessous est conservé tel quel.

---

## 2 — Les données

| Donnée | Valeur | Source |
| --- | --- | --- |
| Courbe d'échauffement à **3,5 N·m**, 120 rpm, 24 V | 330 s | `test-data/performance-curves/V1.2/温升_3.5Nm.png`, sha256 `2c3bb34f…4dda7` (**V**) |
| Courbe d'échauffement à **3,2 N·m**, 120 rpm, 24 V | 700 s | `test-data/performance-curves/V1.2/温升.png`, sha256 `bb65aa20…409278` (**V**) |
| Dépôt constructeur | github.com/dmBots/DM-J4310-2EC, commit `034e06552a` (2026-07-08) | **V** |
| Couple nominal | 3,5 N·m, 120 rpm | manuel V1.4, p. 7 (**V**) |
| Résistance de phase | ~580 mΩ | manuel V1.4, p. 7 (**V**) |
| Courant de phase nominal | 4,9 A à 24 V (amplitude ou valeur efficace : non précisé) | manuel V1.4, p. 7 (**V**) |
| Constante de couple | **aucune valeur numérique** : le manuel donne une formule (p. 9) | **V** |
| Protection moteur | configurable, **≤ 100 °C recommandé** ; pilote coupé à 120 °C | manuel V1.4, p. 7 (**V**) |

Les paramètres électriques viennent du manuel de la **V1.2**. Ceux du wiki
Seeed (0,85 Ω, 0,945 N·m/A, 3,7 A) concernent la **V1.1** : ils ne sont
pas utilisés. La constante de couple implicite de la V1.2, 3,5 / 4,9 ≈
0,71 N·m/A, est différente, et c'est cohérent : ce n'est pas la même
révision (**Déd**).

**L'ambiante de l'essai n'est pas publiée.** La courbe couple-vitesse du
même manuel est à 25 °C ; l'estimation balaie 20, 25 et 30 °C.

---

## 3 — La méthode

1. **Numériser** (**V**). La courbe est rouge, et les graduations de l'axe
   des températures aussi (30 à 110 °C) : elles étalonnent l'axe, avec
   un résidu de 0,05 °C. Les lignes de grille verticales étalonnent le
   temps. Un point tous les 5 s : 64 et 138 points.
2. **Exclure le plateau** (**Déd**). Les deux courbes plafonnent à
   **99 °C**, à 3,5 N·m (dès 310 s) comme à 3,2 N·m (dès 600 s). Deux
   couples différents ne donnent pas la même température d'équilibre. Ce
   palier ressemble à la limite de protection du bobinage (≤ 100 °C) ou à
   une coupure de l'essai. Il est retiré avant l'ajustement.
3. **Ajuster** T(t) = T0 + ΔT (1 − e^(−t/τ)), avec un départ libre, puis
   un départ imposé à l'ambiante.
4. **En tirer le couple continu** (hypothèse de la consigne : pertes ∝
   couple²) : couple_continu = C_essai × √((100 − T_amb) / (T∞ − T_amb)),
   puis k = couple_continu / 3,5.

---

## 4 — Résultats (**V**, sortie du script)

| Courbe | Ajustement | τ (s) | T∞ (°C) | Écart moyen (°C) | Couple continu (N·m) | **k** |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 3,5 N·m | départ libre (30 °C) | 128 | 103,3 | 0,95 | 3,42–3,43 | **0,98** |
| 3,5 N·m | départ 20 °C | 92 | 97,4 | 2,30 | 3,56 | **1,02** |
| 3,5 N·m | départ 25 °C | 107 | 99,8 | 1,47 | 3,51 | **1,00** |
| 3,5 N·m | départ 30 °C | 127 | 103,0 | 0,95 | 3,43 | **0,98** |
| 3,2 N·m | départ libre (37 °C) | 171 | 98,4 | 1,15 | 3,23–3,24 | **0,92–0,93** |
| 3,2 N·m | départ 20 °C | 110 | 94,2 | 3,39 | 3,32 | **0,95** |
| 3,2 N·m | départ 25 °C | 123 | 95,1 | 2,60 | 3,31 | **0,95** |
| 3,2 N·m | départ 30 °C | 139 | 96,3 | 1,82 | 3,29 | **0,94** |

**k estimé : 0,92 à 1,02, médiane 0,96** (12 combinaisons).

---

## 5 — Ce que cela veut dire, et ce que cela ne veut pas dire

**Ce que la courbe dit (Déd).** À 3,5 N·m, le moteur tend vers **100 à
103 °C**, avec une constante de temps de 110 à 130 s. À 310 s, il a déjà
fait l'essentiel de sa montée. **Le nominal de 3,5 N·m est donc, dans la
condition de l'essai, à peu près le couple que le moteur tient à
l'équilibre sous sa limite de protection.** C'est la définition même d'un
couple continu.

**Correction d'une affirmation antérieure.** Le catalogue
(`params/actionneurs.yaml`, condition du J4310) et la modification datée
du 2026-09-30 disent que « 3,5 N·m n'est PAS un régime établi ».
**L'ajustement montre le contraire** : la montée est presque achevée à
310 s, vers une asymptote qui tombe à la limite de protection. La courbe
**suffisait** à le voir ; elle avait été lue trop vite. Le catalogue n'est
pas corrigé ici : c'est à décider.

*Mise à jour du 2026-09-30, nuit* : **correction validée par Jeremy et
appliquée** au catalogue, avec l'ancien texte conservé en commentaire
daté. `archive/docs/choix-classe-S.md` (v1, figé) garde l'ancienne formulation :
c'est une archive.

**Ce que la courbe ne dit pas.**

- **La condition de l'essai** : rotation à 120 rpm, sans rien sur le
  montage (plaque, dissipateur), à une ambiante non publiée. k = 0,96 est
  un rapport **dans cette condition**, pas au rotor bloqué.
- **Le blocage** : un robot debout travaille près du blocage. En
  appliquant au J4310 les rapports blocage / nominal publiés par RobStride
  (0,62 à 0,86), le k en blocage serait de l'ordre de **0,57 à 0,88**
  (0,92 × 0,62 à 1,02 × 0,86). C'est une **hypothèse sur une
  hypothèse** : rien ne garantit qu'un Damiao se comporte comme un
  RobStride.
- **La proportionnalité au couple² n'est qu'à moitié vérifiée.** Passer
  de 3,2 à 3,5 N·m devrait multiplier l'échauffement par (3,5/3,2)² =
  1,20 ; les ajustements libres donnent 1,07. Une partie des pertes ne
  suit pas le couple (fer, frottements, à vitesse constante), ce qui
  élargit la fourchette.
- **Le capteur** est la température « moteur » du pilote, sans précision
  sur son emplacement (bobinage ou carte).

**Vérification d'ordre de grandeur (Déd).** Pertes Joule à 3,5 N·m :
3 × 0,58 Ω × I², soit **21 à 42 W** selon que 4,9 A est une amplitude ou
une valeur efficace. Résistance thermique : ΔT / P ≈ 1,9 à 3,7 K/W.
Capacité thermique : τ / R_th ≈ **35 à 70 J/K**, soit environ 80 à 160 g
d'aluminium. C'est plausible pour la partie active d'un moteur de 306 g.
L'ordre de grandeur tient.

---

## 6 — Le RS05 : même calcul impossible

**RobStride ne publie pas de courbe température-temps.** Le PDF du
2026-09-17 publie :

- une **courbe couple-vitesse à l'équilibre thermique**, sur plaque de
  150 × 150 mm (p. 28) : 1,78 à 1,85 N·m selon la vitesse. Elle donne
  **directement** le couple continu, sans avoir à le déduire ;
- un **tableau de surcharge au blocage** (p. 29) : 1,2 N·m nominal au
  blocage.

**Il n'y a donc rien à estimer pour le RS05** : ses deux valeurs utiles
sont publiées. C'est précisément l'asymétrie que k corrige dans le
comparatif.

---

## 7 — Conséquence pour le comparatif (Déd)

| | Valeur |
| --- | --- |
| Bascule de famille (comparatif) | k ≈ **0,49** (Damiao au-dessus, RobStride-RS05 en dessous) |
| k estimé du J4310, dans la condition de l'essai | **0,92 à 1,02** |
| k en blocage, si le J4310 se comportait comme un RobStride | 0,57 à 0,88 |

**Les deux estimations sont au-dessus de la bascule.** Aucune ne vaut une
mesure, mais elles vont dans le même sens que la borne plausible tirée des
données RobStride (0,619) : **la famille Damiao reste devant**. Le banc
**vérifiera** ce k ; il est peu probable qu'il le départage.
