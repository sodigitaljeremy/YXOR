# Choix de la famille d'actionneurs — comparatif multicritère v2

**Engendré** par `.venv/bin/python scripts/selection_multicritere.py --ecrire`, le 2026-09-30. Ne pas éditer à la main. **C'est le document de décision** : il remplace `docs/choix-classe-S.md` (v1, conservé, méthode corrigée). Aucune fiche, aucun achat proposé (CLAUDE.md, règle d'achat c) : il prépare un choix de Jeremy.

**Ce qui a changé depuis la v1** (relecture externe du 30-09-2026 ; chaque changement est daté dans `params/criteres_selection.yaml`, section `modifications`) :

1. **La taille n'est plus éliminatoire** : c'est une sortie de la démarche inversée (fiche 0047). Elle est notée. Seule la télémétrie élimine.
2. **La capacité est un intervalle.** Taille *optimiste* (le nominal publié le plus favorable) et *prudente* (en blocage si publié ; sinon la plus petite plaque publiée ; sinon — condition non précisée — le nominal × **k**). k est une **hypothèse**, balayée de 1,0 à 0,5.
3. **On compare des familles S → M → L**, pas des modèles. La continuité se mesure dans chaque famille, et un membre absent est un **trou**, affiché.

Poids : **PROPOSÉS, appliqués, NON validés par Jeremy** (réponse du 2026-09-30 ; ils avaient été enregistrés à tort comme fixés par lui) (capacité 18, continuité 18, coût 15, fiabilité 15, robustesse 12, disponibilité 7, masse, ouverture, tension 5 chacun). Marge : 1,5 (fiche 0051). Toutes les tailles sont des **plafonds optimistes** : la marche de référence était écrêtée (cadrage § 3).

---

## 1 — Les familles

| Famille | S : prudent (k = 0,3) – optimiste | M | L | Jambes S (TTC CHF) | Jambes M | Jambes L | Continuité | Trous |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| RobStride (RS05 → RS02 → RS06) | 0,48–0,54 m | 0,79–0,80 m | 0,81–0,91 m | ≥ 1 846 | ≥ 2 481 | ≥ 3 091 | 5/5 | — |
| RobStride, variante S = EduLite 05 (EL05 → RS02 → RS06) | 0,27–0,54 m | 0,79–0,80 m | 0,81–0,91 m | ≥ 1 472 | ≥ 2 481 | ≥ 3 091 | 5/5 | — |
| Damiao (J4310 V1.2 48 V → J8006 V1.1 → J4340 V1.1) | 0,38–0,67 m | 0,47–0,80 m | 0,66–0,99 m | ≥ 2 469 | ≥ 3 141 | ≥ 2 543 | 5/5 | — |
| CubeMars (AK45-10 V3 → AK80-9 V3 → AK10-9 V3) | 0,33–0,61 m | 0,53–0,84 m | 0,60–1,03 m | ≥ 2 417 | ≥ 6 452 | ≥ 9 179 | 5/5 | — |
| MyActuator (X2-7 → [trou] → X4-36) | 0,33–0,61 m | **TROU** | 0,62–0,95 m | ≥ 4 717 | — | ≥ 5 457 | 2/5 | M |

Tailles en mètres, à marge 1,5, configuration homogène de chaque membre. « Prudent » est calculé à la borne basse de l'hypothèse k ; pour RobStride, c'est la valeur **en blocage** publiée, qui ne dépend pas de k. Jambes = phase `jambes_v1` de `params/budget.yaml` (12 actionneurs, électronique connue, imprévus et TVA) ; « ≥ » : la structure n'est pas chiffrée.

**Prix.** Chaque membre est chiffré au prix **revendeur** quand il a été relevé (pour RobStride : Seeed, hors taxe) ; sinon au prix du catalogue. Plus aucun membre de famille n'est chiffré au seul prix constructeur en yuans.

### Membres, trous et alternatives

**RobStride (RS05 → RS02 → RS06)**

- S : RobStride RS05 — clé : RobStride Dynamics RS05 · rév. non publiée · 48 V · firmware non publié — pointe 5,5 N·m ; continu optimiste 1,60 N·m, prudent 1,20 N·m (en blocage (publié)) ; 48 V, plage (15, 60)
- M : RobStride RS02 — clé : RobStride Dynamics RS02 · rév. non publiée · 48 V · firmware non publié — pointe 17,0 N·m ; continu optimiste 7,00 N·m, prudent 6,00 N·m (en blocage (publié)) ; 48 V, plage (15, 60)
- L : RobStride RS06 — clé : RobStride Dynamics RS06 · rév. non publiée · 48 V · firmware non publié — pointe 36,0 N·m ; continu optimiste 11,00 N·m, prudent 8,00 N·m (en blocage (publié)) ; 48 V, plage (15, 60)
- continuité : bus CAN sur les 3 ; protocole commun oui ; tension commune 48 V ; trous : aucun

**RobStride, variante S = EduLite 05 (EL05 → RS02 → RS06)**

- S : RobStride EduLite 05 — clé : RobStride Dynamics EduLite 05 (EL05) · rév. non publiée · 48 V · firmware non publié — pointe 6,0 N·m ; continu optimiste 1,80 N·m, prudent 1,80 N·m (aucune valeur en blocage publiée : nominal × k (1,0)) ; 48 V, plage (48, 48)
- M : RobStride RS02 — clé : RobStride Dynamics RS02 · rév. non publiée · 48 V · firmware non publié — pointe 17,0 N·m ; continu optimiste 7,00 N·m, prudent 6,00 N·m (en blocage (publié)) ; 48 V, plage (15, 60)
- L : RobStride RS06 — clé : RobStride Dynamics RS06 · rév. non publiée · 48 V · firmware non publié — pointe 36,0 N·m ; continu optimiste 11,00 N·m, prudent 8,00 N·m (en blocage (publié)) ; 48 V, plage (15, 60)
- continuité : bus CAN sur les 3 ; protocole commun oui ; tension commune 48 V ; trous : aucun
- note : variante de la famille RobStride : seul le membre S change

**Damiao (J4310 V1.2 48 V → J8006 V1.1 → J4340 V1.1)**

- S : Damiao DM-J4310-2EC V1.2 (48 V) — clé : Damiao (DM) DM-J4310-2EC · rév. V1.2 · 48 V · firmware non publié — pointe 12,5 N·m ; continu optimiste 3,50 N·m, prudent 3,50 N·m (aucune valeur en blocage publiée : nominal × k (1,0)) ; 48 V, plage (20, 58)
- M : Damiao DM-J8006-2EC V1.1 — clé : Damiao (DM) DM-J8006-2EC · rév. V1.1 · 24 V · firmware non publié — pointe 20,0 N·m ; continu optimiste 8,00 N·m, prudent 8,00 N·m (aucune valeur en blocage publiée : nominal × k (1,0)) ; 24 V, plage (15, 52)
- L : Damiao DM-J4340-2EC V1.1 (48 V) — clé : Damiao (DM) DM-J4340-2EC · rév. V1.1 · 48 V · firmware non publié — pointe 40,0 N·m ; continu optimiste 12,00 N·m, prudent 12,00 N·m (aucune valeur en blocage publiée : nominal × k (1,0)) ; 48 V, plage (20, 58)
- alternatives : L = dm_j8009
- continuité : bus CAN sur les 3 ; protocole commun oui ; tension commune 48 V ; trous : aucun
- note : J4310 et J4340 ont une variante 48 V ; J8006 est donné 24 V, « supporte 24–48 V »

**CubeMars (AK45-10 V3 → AK80-9 V3 → AK10-9 V3)**

- S : CubeMars AK45-10 V3.0 KV75 — clé : CubeMars AK45-10 KV75 · rév. V3.0 · 24 V · firmware non publié — pointe 7,0 N·m ; continu optimiste 2,50 N·m, prudent 2,50 N·m (aucune valeur en blocage publiée : nominal × k (1,0)) ; 24 V, plage (24, 24)
- M : CubeMars AK80-9 V3.0 KV100 — clé : CubeMars AK80-9 KV100 · rév. V3.0 · 48 V · firmware non publié — pointe 22,0 N·m ; continu optimiste 9,00 N·m, prudent 9,00 N·m (aucune valeur en blocage publiée : nominal × k (1,0)) ; 48 V, plage (18, 52)
- L : CubeMars AK10-9 V3.0 KV60 — clé : CubeMars AK10-9 KV60 · rév. V3.0 · 48 V · firmware non publié — pointe 53,0 N·m ; continu optimiste 18,00 N·m, prudent 18,00 N·m (aucune valeur en blocage publiée : nominal × k (1,0)) ; 48 V, plage (18, 52)
- alternatives : L = ak70_9_v3
- continuité : bus CAN sur les 3 ; protocole commun oui ; tension commune 24 V ; trous : aucun
- note : AK70-9 V3 (29,2 N·m) sous la plage L : AK10-9 V3 (53 N·m) retenu ; AK45-10 V3 sans variante 48 V trouvée

**MyActuator (X2-7 → [trou] → X4-36)**

- S : MyActuator RMD-X2-P28-7-E (« X2-7 ») — clé : MyActuator RMD-X2-P28-7-E · rév. non publiée · 24 V · firmware non publié — pointe 7,0 N·m ; continu optimiste 2,50 N·m, prudent 2,50 N·m (aucune valeur en blocage publiée : nominal × k (1,0)) ; 24 V, plage (20, 55)
- M : **TROU** de gamme.
- L : MyActuator RMD-X4-P36-36-E (« X4-36 ») — clé : MyActuator RMD-X4-P36-36-E · rév. non publiée · 24 V · firmware non publié — pointe 34,0 N·m ; continu optimiste 10,50 N·m, prudent 10,50 N·m (aucune valeur en blocage publiée : nominal × k (1,0)) ; 24 V, plage (20, 55)
- continuité : bus CAN sur les 3 ; protocole commun non établi ; tension commune 48 V ; trous : M
- note : TROU en M : le catalogue 2026 (sha256 0faddc54…) saute de X4-10 (10 N·m) à X8-32 (32 N·m, RS485 seulement). Le X8-20 n'y figure plus, sans annonce d'arrêt trouvée ; « remplacé par X8-32 » n'est écrit nulle part (l'étude externe l'affirmait). Le X8-25 (V2, 48 V, 25 N·m) est encore présenté mais absent du catalogue 2026.

---

## 2 — Notes (membre S, et continuité de famille) à k = 1,0

Les critères autres que la continuité se notent sur le **membre S**, le premier robot.

| Critère | Poids (proposé) | RobStride | RobStride, variante S = EduLite 05 EL05 | Damiao | CubeMars | MyActuator |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| capacite | 18 | 1 | 2 | 5 | 4 | 4 |
| cout | 15 | 3 | 4 | 2 | 2 | 1 |
| continuite | 18 | 5 | 5 | 5 | 5 | 2 |
| fiabilite_fournisseur | 15 | 3 | 3 | 1 | 1 | 3 |
| robustesse | 12 | 3 | 3 | 3 | 5 | 5 |
| masse | 5 | 4 | 3 | 2 | 2 | 2 |
| ouverture | 5 | 2 | 2 | 2 | 2 | 2 |
| tension_securite | 5 | 2 | 2 | 2 | 4 | 4 |
| disponibilite | 7 | 3 | 3 | 3 | 2 | 1 |
| **score /5** | | **2,95** | **3,23** | **3,12** | **3,21** | **2,75** |

### Justification de chaque note

**RobStride (RS05 → RS02 → RS06)**

- capacite = 1 — taille PRUDENTE 0,48 m (1,20 N·m, en blocage (publié)) → 1 ; optimiste 0,54 m (1,60 N·m)
- cout = 3 — 91,82 CHF HT (110.0 USD, Seeed Studio)
- continuite = 5 — bus CAN sur les 3 ; protocole commun oui ; tension commune 48 V ; trous : aucun
- fiabilite_fournisseur = 3 — garantie écrite 12 mois ; UE non ; CH non
- robustesse = 3 — JUGEMENT — planétaire à pignons acier 7,75:1, protections documentées (surchauffe, surintensité, blocage) ; réversibilité non publiée → 3 selon la grille, strictement
- masse = 4 — 191,0 g
- ouverture = 2 — protocole public oui ; SDK libre non établi ; firmware libre non
- tension_securite = 2 — 48 V
- disponibilite = 3 — Seeed Studio

**RobStride, variante S = EduLite 05 (EL05 → RS02 → RS06)**

- capacite = 2 — taille PRUDENTE 0,54 m (1,80 N·m, aucune valeur en blocage publiée : nominal × k (1,0)) → 2 ; optimiste 0,54 m (1,80 N·m)
- cout = 4 — 66,78 CHF HT (80.0 USD, Seeed Studio)
- continuite = 5 — bus CAN sur les 3 ; protocole commun oui ; tension commune 48 V ; trous : aucun
- fiabilite_fournisseur = 3 — garantie écrite 12 mois ; UE non ; CH non
- robustesse = 3 — JUGEMENT — 9:1, protections documentées comme le RS05 ; type de réducteur et réversibilité non publiés par le constructeur → 3
- masse = 3 — 242,0 g
- ouverture = 2 — protocole public oui ; SDK libre non établi ; firmware libre non
- tension_securite = 2 — 48 V
- disponibilite = 3 — Seeed Studio

**Damiao (J4310 V1.2 48 V → J8006 V1.1 → J4340 V1.1)**

- capacite = 5 — taille PRUDENTE 0,67 m (3,50 N·m, aucune valeur en blocage publiée : nominal × k (1,0)) → 5 ; optimiste 0,67 m (3,50 N·m)
- cout = 2 — 133,59 CHF HT (140.95 EUR, OpenELAB)
- continuite = 5 — bus CAN sur les 3 ; protocole commun oui ; tension commune 48 V ; trous : aucun
- fiabilite_fournisseur = 1 — garantie écrite non trouvée ; UE non ; CH non
- robustesse = 3 — JUGEMENT — même mécanique et même manuel V1.4 que la variante 24 V : 10:1, codes d'erreur documentés ; type d'engrenage et réversibilité non publiés → 3 (ajouté le 2026-09-30, 22 h 30)
- masse = 2 — 306,0 g
- ouverture = 2 — protocole public oui ; SDK libre non établi ; firmware libre non
- tension_securite = 2 — 48 V
- disponibilite = 3 — OpenELAB

**CubeMars (AK45-10 V3 → AK80-9 V3 → AK10-9 V3)**

- capacite = 4 — taille PRUDENTE 0,61 m (2,50 N·m, aucune valeur en blocage publiée : nominal × k (1,0)) → 4 ; optimiste 0,61 m (2,50 N·m)
- cout = 2 — 130,13 CHF HT (155.9 USD, CubeMars)
- continuite = 5 — bus CAN sur les 3 ; protocole commun oui ; tension commune 24 V ; trous : aucun
- fiabilite_fournisseur = 1 — garantie écrite non trouvée ; UE non ; CH non
- robustesse = 5 — JUGEMENT — planétaire 10:1, couple de réversibilité publié 0,1 N·m, codes d'erreur (surchauffe, blocage…) → 5
- masse = 2 — 262,0 g
- ouverture = 2 — protocole public oui ; SDK libre non établi ; firmware libre non
- tension_securite = 4 — 24 V
- disponibilite = 2 — CubeMars (direct)

**MyActuator (X2-7 → [trou] → X4-36)**

- capacite = 4 — taille PRUDENTE 0,61 m (2,50 N·m, aucune valeur en blocage publiée : nominal × k (1,0)) → 4 ; optimiste 0,61 m (2,50 N·m)
- cout = 1 — 284,29 CHF HT (299.95 EUR, OpenELAB)
- continuite = 2 — bus CAN sur les 3 ; protocole commun non établi ; tension commune 48 V ; trous : M
- fiabilite_fournisseur = 3 — garantie écrite 12 mois ; UE non ; CH non
- robustesse = 5 — JUGEMENT — planétaire 28,17:1 (< 50:1), couple de réversibilité publié 0,4 N·m, protections documentées (blocage, surchauffe…) → 5
- masse = 2 — 260,0 g
- ouverture = 2 — protocole public oui ; SDK libre non établi ; firmware libre non
- tension_securite = 4 — 24 V
- disponibilite = 1 — non vérifié : A2V (France) selon l'étude externe ; Eckstein et OpenELAB selon des résumés

---

## 3 — La dimension « données » : le vainqueur pour chaque k

| k | Famille gagnante (poids proposés) | Tient ±50 % | Tirages quelconques gagnés |
| ---: | --- | --- | ---: |
| 1,0 | RobStride, variante S = EduLite 05 (EL05 → RS02 → RS06) | NON, pas toutes | 30,6 % |
| 0,9 | RobStride, variante S = EduLite 05 (EL05 → RS02 → RS06) | oui, toutes | 38,2 % |
| 0,8 | RobStride, variante S = EduLite 05 (EL05 → RS02 → RS06) | NON, pas toutes | 25,0 % |
| 0,7 | RobStride, variante S = EduLite 05 (EL05 → RS02 → RS06) | oui, toutes | 29,1 % |
| 0,6 | RobStride (RS05 → RS02 → RS06) | NON, pas toutes | 46,1 % |
| 0,5 | RobStride (RS05 → RS02 → RS06) | NON, pas toutes | 53,2 % |
| 0,4 | RobStride (RS05 → RS02 → RS06) | NON, pas toutes | 57,0 % |
| 0,3 | RobStride (RS05 → RS02 → RS06) | NON, pas toutes | 57,0 % |

**Verdict à k = 1,0.** **Options trop proches pour que l'analyse tranche** : RobStride, variante S = EduLite 05 (EL05 → RS02 → RS06) en tête aux poids proposés — le choix dépend des poids, que Jeremy fixera.

**Verdict à la borne basse (k = 0,3).** **Options trop proches pour que l'analyse tranche** : RobStride (RS05 → RS02 → RS06) en tête aux poids proposés — le choix dépend des poids, que Jeremy fixera.


**Seuil de bascule : RobStride, variante S = EduLite 05 (EL05 → RS02 → RS06) gagne jusqu'à k = 0,68 ; RobStride (RS05 → RS02 → RS06) gagne dès k = 0,67.**

En clair : le classement dépend du rapport entre le couple continu **réel** des actionneurs « condition non précisée » et leur nominal publié. **C'est ce rapport que le banc doit mesurer**, dans une condition identique pour les deux finalistes (`docs/comparatif-banc.md`).

---

## 3 bis — Ce que les données disent de k

Un seul fabricant publie à la fois un couple nominal (en rotation, sur plaque) **et** un couple en blocage : RobStride (PDF du 17-09-2026). Leur rapport est une mesure constructeur de ce que k représente — pour **ses** actionneurs, dans **ses** conditions.

| Actionneur | Blocage (N·m) | Nominal (N·m) | Blocage / nominal |
| --- | ---: | ---: | ---: |
| RobStride RS05 | 1,2 | 1,6 | **0,750** |
| RobStride RS02 | 6,0 | 7,0 | **0,857** |
| RobStride RS06 | 8,0 | 11,0 | **0,727** |
| RobStride RS03 | 13,0 | 21,0 | **0,619** |
| **moyenne** | | | **0,738** |

**Position par rapport au seuil de bascule (k ≈ 0,68) : la moyenne RobStride, 0,738, est AU-DESSUS du seuil.** Si les actionneurs sans valeur en blocage se comportaient comme ceux de RobStride, le vainqueur serait « RobStride, variante S = EduLite 05 (EL05 → RS02 → RS06) » — mais l'écart entre les quatre rapports (0,619 à 0,857) couvre le seuil : **les données constructeur ne tranchent pas, le banc tranchera.**

*Réserve* : ces rapports sont ceux d'un fabricant, pour une condition de blocage qu'il définit. Rien ne garantit qu'un Damiao ou un CubeMars se comporte pareil.

### k au blocage du J4310 : une hypothèse sur une hypothèse

L'estimation thermique (`scripts/estimation_thermique.py`, lue à la source) donne, **en rotation** à 120 rpm et 24 V, dans la condition de l'essai constructeur, **au seuil thermique du protocole (90 °C : protection 100 °C − 10 °C du protocole)**, **k ≈ 0,86–0,95**. Un robot debout travaille près du blocage. En décotant cette estimation par les rapports blocage / nominal de RobStride ci-dessus (0,619 à 0,857), le k du J4310 **au blocage** serait de l'ordre de **0,53–0,81** (0,86 × 0,619 à 0,95 × 0,857).

**La bascule (k ≈ 0,67) n'oppose pas la famille de cet actionneur** : situer cette fourchette par rapport à elle ne décide rien. Elle reste une information sur le J4310, pas un argument de choix.

---

## 4 — Les candidats S hors famille, pour mémoire

| Candidat | Clé de révision | Taille prudente – optimiste (k = 1,0) | Score /5 | État |
| --- | --- | --- | ---: | --- |
| RobStride EduLite 05 | RobStride Dynamics EduLite 05 (EL05) · rév. non publiée · 48 V · firmware non publié | 0,54–0,54 m | 3,23 | admis |
| Damiao DM-J4310-2EC V1.2 | Damiao (DM) DM-J4310-2EC · rév. V1.2 · 24 V · firmware non publié | 0,67–0,67 m | 3,05 | admis |
| RobStride RS05 | RobStride Dynamics RS05 · rév. non publiée · 48 V · firmware non publié | 0,48–0,54 m | 2,95 | admis |
| Damiao DM-J4310-2EC V1.2 (48 V) | Damiao (DM) DM-J4310-2EC · rév. V1.2 · 48 V · firmware non publié | 0,67–0,67 m | 2,76 | admis |
| MyActuator RMD-X2-P28-7-E (« X2-7 ») | MyActuator RMD-X2-P28-7-E · rév. non publiée · 24 V · firmware non publié | 0,61–0,61 m | 2,75 | admis |
| CubeMars AK45-10 V3.0 KV75 | CubeMars AK45-10 KV75 · rév. V3.0 · 24 V · firmware non publié | 0,61–0,61 m | 2,67 | admis |
| SteadyWin GIM4310-10 (driver GDZ34) | SteadyWin GIM4310-10 (driver GDZ34) · rév. non publiée · 24 V · firmware non publié | 0,53–0,53 m | 2,41 | admis |
| Dynamixel XM430-W210 (référence) | ROBOTIS XM430-W210 · rév. non publiée · 12 V · firmware non publié | 0,53–0,53 m | 1,55 | admis (référence) |
| Feetech STS3250 | Feetech STS3250 · rév. non publiée · 12 V · firmware non publié | 0,60–0,60 m | 1,48 | admis |

Leur continuité est celle de la v2 (intrinsèque) seulement s'ils appartiennent à une famille ; les autres (Feetech STS3250, SteadyWin GIM4310-10, Dynamixel XM430) sont listés pour mémoire.

---

## 5 — Questions ouvertes

- **Ce que S doit porter** (calculateur, batterie, IMU) n'est pas chiffré : c'était la vraie contrainte derrière le seuil retiré (cadrage, question 13).
- **Les trous de gamme** sont-ils rédhibitoires, ou comblables par un modèle hors famille ?
- **La sensibilité aux poids** reste affichée : les poids ne sont pas fixés par Jeremy, et un classement qui ne tiendrait qu'à eux mériterait d'être su.

### Limite du membre L de Damiao — question ouverte, à rouvrir AVANT L

- **Le membre L retenu, Damiao DM-J4340-2EC V1.1 (48 V), a une réduction de 40:1** (manuel V1.3, p. 7). Sa réversibilité n'est **pas publiée** ; un rapport aussi élevé la rend **probablement faible**. *Réversible* veut dire qu'un effort extérieur sur la sortie fait tourner le moteur : c'est ce qui laisse une jambe **encaisser un choc** (pied qui touche le sol) en cédant un peu, au lieu de le transmettre intact aux dents du réducteur. Pour une jambe, un réducteur peu réversible est **défavorable**.
- **Alternative dans la même famille : Damiao DM-J8009-2EC (alternative L)**, 896 g (manuel V1.1, p. 6), contre 362 g : plus lourd ; sa réduction n'est pas publiée.
- **La robustesse n'a été notée que sur le membre S** (Damiao DM-J4310-2EC V1.2 (48 V)) : ce comparatif ne dit rien de celle du membre L. C'est une **question ouverte pour L, à rouvrir avant de concevoir L**. Elle est **sans effet sur S** : ni la note, ni le choix de famille pour S n'en dépendent.

## 6 — Ce que ce comparatif ne dit pas

- **Aucun couple continu n'est mesuré dans la condition du robot.** k est une hypothèse ; le banc la remplacera par une mesure.
- **Les prix** sont ceux relevés le 30-09-2026, hors port ; plusieurs viennent de revendeurs.
- **Les données marquées non vérifiées** dans le catalogue ne comptent pas comme établies.
