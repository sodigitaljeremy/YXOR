# Choix de la famille d'actionneurs — comparatif multicritère v2

**Engendré** par `.venv/bin/python scripts/selection_multicritere.py --ecrire`, le 2026-10-01. Ne pas éditer à la main. **C'est le document de décision** : il remplace `docs/choix-classe-S.md` (v1, conservé, méthode corrigée). Aucune fiche, aucun achat proposé (CLAUDE.md, règle d'achat c) : il prépare un choix de Jeremy.

**Ce qui a changé depuis la v1** (relecture externe du 30-09-2026 ; chaque changement est daté dans `params/criteres_selection.yaml`, section `modifications`) :

1. **La taille n'est plus éliminatoire** : c'est une sortie de la démarche inversée (fiche 0047). Elle est notée. Seule la télémétrie élimine.
2. **La capacité est un intervalle.** Taille *optimiste* (le nominal publié le plus favorable) et *prudente* (en blocage si publié ; sinon la plus petite plaque publiée ; sinon — condition non précisée — le nominal × **k**). k est une **hypothèse**, balayée de 1,0 à 0,5.
3. **On compare des familles S → M → L**, pas des modèles. La continuité se mesure dans chaque famille, et un membre absent est un **trou**, affiché.

Poids : **décidés par Jeremy le 2026-09-30 (~23 h)**, validés tels quels après avoir été d'abord attribués à tort (`criteres_selection.yaml`, `modifications`) (capacité 18, continuité 18, coût 15, fiabilité 15, robustesse 12, disponibilité 7, masse, ouverture, tension 5 chacun). Marge : 1,5 (fiche 0051). Toutes les tailles sont des **plafonds optimistes** : la marche de référence était écrêtée (cadrage § 3).

> **Réserve de Jeremy, question OUVERTE** : « il manque des critères de comparaison essentiels » (Jeremy, 2026-09-30 (~23 h), en réponse à docs/arbitrage-2026-09-30.md). OUVERT — à instruire avant tout nouveau calcul de famille.

---

## 1 — Les familles

| Famille | S : prudent (k = 0,3) – optimiste | M | L | Jambes S (TTC CHF) | Jambes M | Jambes L | Continuité | Trous |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| RobStride (RS05 → RS02 → RS06) | 0,48–0,54 m | 0,79–0,80 m | 0,81–0,91 m | ≥ 1 846 | ≥ 2 481 | ≥ 3 091 | 5/5 | — |
| RobStride, variante S = EduLite 05 (EL05 → RS02 → RS06) | 0,27–0,54 m | 0,79–0,80 m | 0,81–0,91 m | ≥ 1 472 | ≥ 2 481 | ≥ 3 091 | 5/5 | — |
| Damiao (J4310 V1.2 48 V → J8006 V1.1 → J4340 V1.1) | 0,38–0,67 m | 0,47–0,80 m | 0,66–0,99 m | ≥ 2 469 | ≥ 3 141 | ≥ 2 543 | 5/5 | — |
| CubeMars (AK45-10 V3 → AK80-9 V3 → AK10-9 V3) | 0,33–0,61 m | 0,53–0,78 m | 0,60–1,03 m | ≥ 2 417 | ≥ 6 452 | ≥ 9 179 | 5/5 | — |
| MyActuator (X2-7 → [trou] → X4-36) | 0,33–0,61 m | **TROU** | 0,62–0,95 m | ≥ 4 717 | — | ≥ 5 457 | 2/5 | M |
| RobStride, variante S = RS00 (RS00 → RS02 → RS06) | 0,67–0,75 m | 0,79–0,80 m | 0,81–0,91 m | ≥ 2 033 | ≥ 2 481 | ≥ 3 091 | 5/5 | — |
| HighTorque (HTDW-4438-30 → HTDW-5036-02 → HTDW-6036-02) | 0,30–0,57 m | 0,50–0,80 m | 0,53–0,89 m | ≥ 2 830 | ≥ 2 830 | ≥ 3 203 | 3/5 | — |

Tailles en mètres, à marge 1,5, configuration homogène de chaque membre. « Prudent » est calculé à la borne basse de l'hypothèse k ; pour RobStride, c'est la valeur **en blocage** publiée, qui ne dépend pas de k. Jambes = phase `jambes_v1` de `params/budget.yaml` (12 actionneurs, électronique connue, imprévus et TVA) ; « ≥ » : la structure n'est pas chiffrée.

**Prix.** Chaque membre est chiffré au prix **revendeur** quand il a été relevé (pour RobStride : Seeed, hors taxe) ; sinon au prix du catalogue. Plus aucun membre de famille n'est chiffré au seul prix constructeur en yuans.

### Membres, trous et alternatives

**RobStride (RS05 → RS02 → RS06)**

- S : RobStride RS05 — clé : RobStride Dynamics RS05 · rév. non publiée · 48 V · firmware non publié — pointe 5,5 N·m ; continu optimiste 1,60 N·m, prudent 1,20 N·m (en blocage (publié)) ; 48 V, plage (15, 60)
- M : RobStride RS02 — clé : RobStride Dynamics RS02 · rév. non publiée · 48 V · firmware non publié — pointe 17,0 N·m ; continu optimiste 7,00 N·m, prudent 6,00 N·m (en blocage (publié)) ; 48 V, plage (15, 60)
- L : RobStride RS06 — clé : RobStride Dynamics RS06 · rév. non publiée · 48 V · firmware non publié — pointe 36,0 N·m ; continu optimiste 11,00 N·m, prudent 8,00 N·m (en blocage (publié)) ; 48 V, plage (15, 60)
- continuité : bus CAN sur les 3 ; protocole commun oui ; tension commune 48 V ; trous : aucun

**RobStride, variante S = EduLite 05 (EL05 → RS02 → RS06)**

- S : RobStride EduLite 05 — clé : RobStride Dynamics EduLite 05 (EL05) · rév. non publiée · 48 V · firmware non publié — pointe 5,5 N·m ; continu optimiste 1,80 N·m, prudent 1,80 N·m (aucune valeur en blocage publiée : nominal × k (1,0)) ; 48 V, plage (48, 48)
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
- M : CubeMars AK80-9 V3.0 KV100 — clé : CubeMars AK80-9 KV100 · rév. V3.0 · 48 V · firmware non publié — pointe 18,0 N·m ; continu optimiste 9,00 N·m, prudent 9,00 N·m (aucune valeur en blocage publiée : nominal × k (1,0)) ; 48 V, plage (18, 52)
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

**RobStride, variante S = RS00 (RS00 → RS02 → RS06)**

- S : RobStride RS00 — clé : RobStride Dynamics RS00 · rév. non publiée · 48 V · firmware non publié — pointe 14,0 N·m ; continu optimiste 5,00 N·m, prudent 3,60 N·m (en blocage (publié)) ; 48 V, plage (24, 60)
- M : RobStride RS02 — clé : RobStride Dynamics RS02 · rév. non publiée · 48 V · firmware non publié — pointe 17,0 N·m ; continu optimiste 7,00 N·m, prudent 6,00 N·m (en blocage (publié)) ; 48 V, plage (15, 60)
- L : RobStride RS06 — clé : RobStride Dynamics RS06 · rév. non publiée · 48 V · firmware non publié — pointe 36,0 N·m ; continu optimiste 11,00 N·m, prudent 8,00 N·m (en blocage (publié)) ; 48 V, plage (15, 60)
- continuité : bus CAN sur les 3 ; protocole commun oui ; tension commune 48 V ; trous : aucun
- note : variante de la famille RobStride : seul le membre S change. RS00 (pointe 14 N·m) est plus proche de la plage M que de la plage S visée (5-7 N·m)

**HighTorque (HTDW-4438-30 → HTDW-5036-02 → HTDW-6036-02)**

- S : HighTorque HTDW-4438-30-NE (HTDW-4530-02-DNE) — clé : HighTorque Robotics HTDW-4438-30-NE · rév. non publiée · 24 V · firmware non publié — pointe 10,0 N·m ; continu optimiste 2,00 N·m, prudent 2,00 N·m (aucune valeur en blocage publiée : nominal × k (1,0)) ; 24 V, plage (12, 50.4)
- M : HighTorque HTDW-5036-02-DNE — clé : HighTorque Robotics HTDW-5036-02-DNE · rév. non publiée · 24 V · firmware non publié — pointe 21,0 N·m ; continu optimiste 6,00 N·m, prudent 6,00 N·m (aucune valeur en blocage publiée : nominal × k (1,0)) ; 24 V, plage (12, 50.4)
- L : HighTorque HTDW-6036-02-DNE — clé : HighTorque Robotics HTDW-6036-02-DNE · rév. non publiée · 24 V · firmware non publié — pointe 36,0 N·m ; continu optimiste 10,00 N·m, prudent 10,00 N·m (aucune valeur en blocage publiée : nominal × k (1,0)) ; 24 V, plage (12, 50.4)
- alternatives : S = htdw_5047_36
- continuité : bus CAN sur les 3 ; protocole commun non établi ; tension commune 48 V ; trous : aucun
- note : M et L classés sur leur couple de BLOCAGE momentané (21 et 36 N·m), seul publié : ce n'est pas une pointe au sens des autres familles. HTDW-5047-36 (fiche 2024, absente du site constructeur) en S alternatif. D'autres membres existent (5036-02-CNE, 6036-02-CNE, HTPU-6035-04-CNE, 5022-02-DNE) ; non portés.

---

## 2 — Notes (membre S, et continuité de famille) à k = 1,0

Les critères autres que la continuité se notent sur le **membre S**, le premier robot.

| Critère | Poids (fixé) | RobStride | RobStride, variante S = EduLite 05 EL05 | Damiao | CubeMars | MyActuator | RobStride, variante S = RS00 | HighTorque |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| capacite | 18 | 1 | 2 | 5 | 4 | 4 | 5 | 3 |
| cout | 15 | 3 | 4 | 2 | 2 | 1 | 3 | 2 |
| continuite | 18 | 5 | 5 | 5 | 5 | 2 | 5 | 3 |
| fiabilite_fournisseur | 15 | 3 | 3 | 1 | 1 | 3 | 3 | 1 |
| robustesse | 12 | 3 | 3 | 3 | 5 | 5 | 3 | 3 |
| masse | 5 | 4 | 3 | 2 | 2 | 2 | 2 | 3 |
| ouverture | 5 | 2 | 2 | 2 | 2 | 2 | 2 | 0 |
| tension_securite | 5 | 2 | 2 | 2 | 4 | 4 | 2 | 4 |
| disponibilite | 7 | 3 | 3 | 3 | 2 | 1 | 3 | 3 |
| **score /5** | | **2,95** | **3,23** | **3,12** | **3,21** | **2,75** | **3,57** | **2,45** |

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

**RobStride, variante S = RS00 (RS00 → RS02 → RS06)**

- capacite = 5 — taille PRUDENTE 0,67 m (3,60 N·m, en blocage (publié)) → 5 ; optimiste 0,75 m (5,00 N·m)
- cout = 3 — 104,34 CHF HT (125.0 USD, Seeed Studio)
- continuite = 5 — bus CAN sur les 3 ; protocole commun oui ; tension commune 48 V ; trous : aucun
- fiabilite_fournisseur = 3 — garantie écrite 12 mois ; UE non ; CH non
- robustesse = 3 — JUGEMENT — 10:1, protections documentées (surchauffe 135/145 °C, surintensité, blocage) ; « planétaire » écrit seulement par le revendeur, réversibilité non publiée → 3, comme l'EduLite 05
- masse = 2 — 330,0 g
- ouverture = 2 — protocole public oui ; SDK libre non établi ; firmware libre non
- tension_securite = 2 — 48 V
- disponibilite = 3 — Seeed Studio

**HighTorque (HTDW-4438-30 → HTDW-5036-02 → HTDW-6036-02)**

- capacite = 3 — taille PRUDENTE 0,57 m (2,00 N·m, aucune valeur en blocage publiée : nominal × k (1,0)) → 3 ; optimiste 0,57 m (2,00 N·m)
- cout = 2 — 157,76 CHF HT (189.0 USD, Seeed Studio)
- continuite = 3 — bus CAN sur les 3 ; protocole commun non établi ; tension commune 48 V ; trous : aucun
- fiabilite_fournisseur = 1 — garantie écrite non trouvée ; UE non ; CH non
- robustesse = 3 — JUGEMENT — planétaire 30:1 (fiche constructeur), codes de défaut surchauffe et surtension documentés ; réversibilité annoncée sans chiffre → 3
- masse = 3 — 237,0 g
- ouverture = 0 — protocole public non/inconnu ; SDK libre non établi ; firmware libre non
- tension_securite = 4 — 24 V
- disponibilite = 3 — Seeed Studio

---

## 3 — La dimension « données » : le vainqueur pour chaque k

| k | Famille gagnante (poids fixés) | Tient ±50 % | Tirages quelconques gagnés |
| ---: | --- | --- | ---: |
| 1,0 | RobStride, variante S = RS00 (RS00 → RS02 → RS06) | oui, toutes | 34,2 % |
| 0,9 | RobStride, variante S = RS00 (RS00 → RS02 → RS06) | oui, toutes | 40,7 % |
| 0,8 | RobStride, variante S = RS00 (RS00 → RS02 → RS06) | oui, toutes | 44,5 % |
| 0,7 | RobStride, variante S = RS00 (RS00 → RS02 → RS06) | oui, toutes | 48,1 % |
| 0,6 | RobStride, variante S = RS00 (RS00 → RS02 → RS06) | oui, toutes | 52,6 % |
| 0,5 | RobStride, variante S = RS00 (RS00 → RS02 → RS06) | oui, toutes | 55,1 % |
| 0,4 | RobStride, variante S = RS00 (RS00 → RS02 → RS06) | oui, toutes | 55,1 % |
| 0,3 | RobStride, variante S = RS00 (RS00 → RS02 → RS06) | oui, toutes | 55,1 % |

**Verdict à k = 1,0.** **Aux poids décidés par Jeremy : RobStride, variante S = RS00 (RS00 → RS02 → RS06)** — il **tient toutes les variations ±50 %**. Sur 1 000 jeux de poids **quelconques**, il gagne 34,2 % des tirages ; « CubeMars (AK45-10 V3 → AK80-9 V3 → AK10-9 V3) » en gagne 27,4 %. Cette dernière mesure dit seulement qu'**un autre principe de pondération** que celui de Jeremy choisirait autrement : elle n'affaiblit pas le choix fait avec le sien.

**Verdict à la borne basse (k = 0,3).** **Aux poids décidés par Jeremy : RobStride, variante S = RS00 (RS00 → RS02 → RS06)** — il **tient toutes les variations ±50 %**. Sur 1 000 jeux de poids **quelconques**, il gagne 55,1 % des tirages ; « RobStride (RS05 → RS02 → RS06) » en gagne 18,1 %. Cette dernière mesure dit seulement qu'**un autre principe de pondération** que celui de Jeremy choisirait autrement : elle n'affaiblit pas le choix fait avec le sien.


**Aucune bascule entre k = 1,0 et 0,5** : le vainqueur ne dépend pas de l'hypothèse k.

---

## 3 bis — Ce que les données disent de k

Un seul fabricant publie à la fois un couple nominal (en rotation, sur plaque) **et** un couple en blocage : RobStride (PDF du 17-09-2026). Leur rapport est une mesure constructeur de ce que k représente — pour **ses** actionneurs, dans **ses** conditions.

| Actionneur | Blocage (N·m) | Nominal (N·m) | Blocage / nominal |
| --- | ---: | ---: | ---: |
| RobStride RS05 | 1,2 | 1,6 | **0,750** |
| RobStride RS02 | 6,0 | 7,0 | **0,857** |
| RobStride RS06 | 8,0 | 11,0 | **0,727** |
| RobStride RS03 | 13,0 | 21,0 | **0,619** |
| RobStride RS00 | 3,6 | 5,0 | **0,720** |
| **moyenne** | | | **0,735** |

**Aucune bascule entre k = 1,0 et 0,5** : quelle que soit la valeur de k dans cette plage, le vainqueur ne change pas.

*Réserve* : ces rapports sont ceux d'un fabricant, pour une condition de blocage qu'il définit. Rien ne garantit qu'un Damiao ou un CubeMars se comporte pareil.

### k au blocage du J4310 : une hypothèse sur une hypothèse

L'estimation thermique (`scripts/estimation_thermique.py`, lue à la source) donne, **en rotation** à 120 rpm et 24 V, dans la condition de l'essai constructeur, **au seuil thermique du protocole (90 °C : protection 100 °C − 10 °C du protocole)**, **k ≈ 0,86–0,95**. Un robot debout travaille près du blocage. En décotant cette estimation par les rapports blocage / nominal de RobStride ci-dessus (0,619 à 0,857), le k du J4310 **au blocage** serait de l'ordre de **0,53–0,81** (0,86 × 0,619 à 0,95 × 0,857).

---

## 3 ter — k en deux dimensions : information, ne change pas le verdict

*PROPOSÉ par Claude (arbitrage, 2026-10-01), d'après l'audit externe ChatGPT du 2026-10-01.* Le balayage du § 3 applique **le même k** à tous les actionneurs sans valeur en blocage. Ici, **k du J4310 (lignes) et k de l'EduLite 05 (colonnes)** sont balayés séparément, de 1,0 à 0,5 par pas de 0,05. Le RS05 garde sa valeur en blocage publiée. Lettre = famille gagnante aux poids décidés : **D** Damiao (J4310 V1.2 48 V → J8006 V1.1 → J4340 V1.1), **E** RobStride, variante S = EduLite 05 (EL05 → RS02 → RS06), **R** RobStride (RS05 → RS02 → RS06), **C** CubeMars (AK45-10 V3 → AK80-9 V3 → AK10-9 V3), **M** MyActuator (X2-7 → [trou] → X4-36), **Z** RobStride, variante S = RS00 (RS00 → RS02 → RS06), **H** HighTorque (HTDW-4438-30 → HTDW-5036-02 → HTDW-6036-02).

**Les autres candidats sans valeur en blocage suivent le plus petit des deux k.**

| k J4310 \ k EL05 | 1,00 | 0,95 | 0,90 | 0,85 | 0,80 | 0,75 | 0,70 | 0,65 | 0,60 | 0,55 | 0,50 |
| ---: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 1,00 | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z |
| 0,95 | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z |
| 0,90 | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z |
| 0,85 | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z |
| 0,80 | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z |
| 0,75 | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z |
| 0,70 | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z |
| 0,65 | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z |
| 0,60 | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z |
| 0,55 | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z |
| 0,50 | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z |

**Les autres candidats sans valeur en blocage restent à k = 1,0 (leur cas le plus favorable).**

| k J4310 \ k EL05 | 1,00 | 0,95 | 0,90 | 0,85 | 0,80 | 0,75 | 0,70 | 0,65 | 0,60 | 0,55 | 0,50 |
| ---: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 1,00 | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z |
| 0,95 | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z |
| 0,90 | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z |
| 0,85 | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z |
| 0,80 | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z |
| 0,75 | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z |
| 0,70 | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z |
| 0,65 | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z |
| 0,60 | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z |
| 0,55 | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z |
| 0,50 | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z | Z |

**Lecture, par rapport à la borne basse plausible de k (0,619).** La carte « min » est la lecture prudente. La carte « 1,0 » montre ce que donnerait l'hypothèse la plus favorable accordée aux autres fabricants : un **artefact** de cette hypothèse, pas un résultat.

- **RobStride avec RS00** gagne sur 121 cases sur 121 : k J4310 de 0,50 à 1,00, k EL05 de 0,50 à 1,00.

---

## 3 quater — Deux scores, technique et approvisionnement : PROPOSITION

*PROPOSÉ par Claude (arbitrage, 2026-10-01), d'après l'audit externe ChatGPT du 2026-10-01.* **Le verdict retenu reste celui du § 3**, au score unique. Ici, les mêmes notes sont séparées en deux scores, avec les poids décidés **renormalisés dans chaque groupe** :

- **technique** : capacite 18, continuite 18, robustesse 12, masse 5, ouverture 5, tension_securite 5 (somme 63) ;
- **approvisionnement, daté** : cout 15, fiabilite_fournisseur 15, disponibilite 7 (somme 37). Prix, garanties et revendeurs relevés le 30-09 et le 01-10-2026 : ce score **vieillit**, le technique beaucoup moins.

| k | Classement technique | Classement approvisionnement |
| ---: | --- | --- |
| 1,0 | CubeMars 4,16 > Damiao 3,90 > RobStride, variante S = RS00 3,90 > MyActuator 3,30 > RobStride, variante S = EduLite 05 EL05 3,13 > RobStride 2,92 > HighTorque 2,84 | RobStride, variante S = EduLite 05 EL05 3,41 > RobStride 3,00 > RobStride, variante S = RS00 3,00 > MyActuator 1,81 > Damiao 1,78 > HighTorque 1,78 > CubeMars 1,59 |
| 0,9 | RobStride, variante S = RS00 3,90 > CubeMars 3,87 > Damiao 3,62 > RobStride, variante S = EduLite 05 EL05 3,13 > MyActuator 3,02 > RobStride 2,92 > HighTorque 2,56 | RobStride, variante S = EduLite 05 EL05 3,41 > RobStride 3,00 > RobStride, variante S = RS00 3,00 > MyActuator 1,81 > Damiao 1,78 > HighTorque 1,78 > CubeMars 1,59 |
| 0,8 | RobStride, variante S = RS00 3,90 > CubeMars 3,87 > Damiao 3,62 > MyActuator 3,02 > RobStride 2,92 > RobStride, variante S = EduLite 05 EL05 2,84 > HighTorque 2,56 | RobStride, variante S = EduLite 05 EL05 3,41 > RobStride 3,00 > RobStride, variante S = RS00 3,00 > MyActuator 1,81 > Damiao 1,78 > HighTorque 1,78 > CubeMars 1,59 |
| 0,7 | RobStride, variante S = RS00 3,90 > CubeMars 3,59 > Damiao 3,33 > RobStride 2,92 > RobStride, variante S = EduLite 05 EL05 2,84 > MyActuator 2,73 > HighTorque 2,27 | RobStride, variante S = EduLite 05 EL05 3,41 > RobStride 3,00 > RobStride, variante S = RS00 3,00 > MyActuator 1,81 > Damiao 1,78 > HighTorque 1,78 > CubeMars 1,59 |
| 0,6 | RobStride, variante S = RS00 3,90 > CubeMars 3,30 > Damiao 3,05 > RobStride 2,92 > RobStride, variante S = EduLite 05 EL05 2,56 > MyActuator 2,44 > HighTorque 2,27 | RobStride, variante S = EduLite 05 EL05 3,41 > RobStride 3,00 > RobStride, variante S = RS00 3,00 > MyActuator 1,81 > Damiao 1,78 > HighTorque 1,78 > CubeMars 1,59 |
| 0,5 | RobStride, variante S = RS00 3,90 > Damiao 3,05 > CubeMars 3,02 > RobStride 2,92 > RobStride, variante S = EduLite 05 EL05 2,56 > MyActuator 2,16 > HighTorque 1,98 | RobStride, variante S = EduLite 05 EL05 3,41 > RobStride 3,00 > RobStride, variante S = RS00 3,00 > MyActuator 1,81 > Damiao 1,78 > HighTorque 1,78 > CubeMars 1,59 |

L'approvisionnement ne dépend pas de k : ses notes ne lisent ni la capacité ni la thermique. Une famille en tête des deux classements à la fois est robuste à la séparation ; sinon, le choix dépend du poids relatif des deux groupes, qui n'est pas décidé.

---

## 4 — Les candidats S hors famille, pour mémoire

| Candidat | Clé de révision | Taille prudente – optimiste (k = 1,0) | Score /5 | État |
| --- | --- | --- | ---: | --- |
| RobStride RS00 | RobStride Dynamics RS00 · rév. non publiée · 48 V · firmware non publié | 0,67–0,75 m | 3,57 | admis |
| RobStride EduLite 05 | RobStride Dynamics EduLite 05 (EL05) · rév. non publiée · 48 V · firmware non publié | 0,54–0,54 m | 3,23 | admis |
| Damiao DM-J4310-2EC V1.2 | Damiao (DM) DM-J4310-2EC · rév. V1.2 · 24 V · firmware non publié | 0,67–0,67 m | 3,05 | admis |
| RobStride RS05 | RobStride Dynamics RS05 · rév. non publiée · 48 V · firmware non publié | 0,48–0,54 m | 2,95 | admis |
| Damiao DM-J4310-2EC V1.2 (48 V) | Damiao (DM) DM-J4310-2EC · rév. V1.2 · 48 V · firmware non publié | 0,67–0,67 m | 2,76 | admis |
| MyActuator RMD-X2-P28-7-E (« X2-7 ») | MyActuator RMD-X2-P28-7-E · rév. non publiée · 24 V · firmware non publié | 0,61–0,61 m | 2,75 | admis |
| CubeMars AK40-10 V3.0 KV170 (référence) | CubeMars AK40-10 KV170 · rév. V3.0 · 24 V · firmware non publié | 0,50–0,50 m | 2,68 | admis (référence) |
| CubeMars AK45-10 V3.0 KV75 | CubeMars AK45-10 KV75 · rév. V3.0 · 24 V · firmware non publié | 0,61–0,61 m | 2,67 | admis |
| Xiaomi CyberGear (référence) | Xiaomi CyberGear · rév. non publiée · 24 V · firmware non publié | 0,70–0,70 m | 2,62 | admis (référence) |
| SteadyWin GIM4310-10 (driver GDZ34) | SteadyWin GIM4310-10 (driver GDZ34) · rév. non publiée · 24 V · firmware non publié | 0,53–0,53 m | 2,41 | admis |
| HighTorque HTDW-4438-30-NE (HTDW-4530-02-DNE) | HighTorque Robotics HTDW-4438-30-NE · rév. non publiée · 24 V · firmware non publié | 0,57–0,57 m | 2,27 | admis |
| HighTorque HTDW-5047-36-NE | HighTorque Robotics HTDW-5047-36-NE · rév. non publiée · 24 V · firmware non publié | 0,70–0,70 m | 2,14 | admis |
| Dynamixel XM430-W210 (référence) | ROBOTIS XM430-W210 · rév. non publiée · 12 V · firmware non publié | 0,53–0,53 m | 1,55 | admis (référence) |
| Dynamixel XM430-W350 (référence) | ROBOTIS XM430-W350-T / -R · rév. non publiée · 12 V · firmware non publié | 0,58–0,58 m | 1,55 | admis (référence) |
| Feetech STS3250 | Feetech STS3250 · rév. non publiée · 12 V · firmware non publié | 0,60–0,60 m | 1,48 | admis |

Leur continuité est celle de la v2 (intrinsèque) seulement s'ils appartiennent à une famille ; les autres (Feetech STS3250, SteadyWin GIM4310-10, Dynamixel XM430) sont listés pour mémoire.

---

## 5 — Questions ouvertes

- **Ce que S doit porter** (calculateur, batterie, IMU) n'est pas chiffré : c'était la vraie contrainte derrière le seuil retiré (cadrage, question 13).
- **Les trous de gamme** sont-ils rédhibitoires, ou comblables par un modèle hors famille ?
- **La sensibilité aux poids** reste affichée : les poids sont fixés, mais un classement qui ne tiendrait qu'à eux mériterait d'être su.

### Limite du membre L de Damiao — question ouverte, à rouvrir AVANT L

- **Le membre L retenu, Damiao DM-J4340-2EC V1.1 (48 V), a une réduction de 40:1** (manuel V1.3, p. 7). Sa réversibilité n'est **pas publiée** ; un rapport aussi élevé la rend **probablement faible**. *Réversible* veut dire qu'un effort extérieur sur la sortie fait tourner le moteur : c'est ce qui laisse une jambe **encaisser un choc** (pied qui touche le sol) en cédant un peu, au lieu de le transmettre intact aux dents du réducteur. Pour une jambe, un réducteur peu réversible est **défavorable**.
- **Alternative dans la même famille : Damiao DM-J8009-2EC (alternative L)**, 896 g (manuel V1.1, p. 6), contre 362 g : plus lourd ; sa réduction n'est pas publiée.
- **La robustesse n'a été notée que sur le membre S** (Damiao DM-J4310-2EC V1.2 (48 V)) : ce comparatif ne dit rien de celle du membre L. C'est une **question ouverte pour L, à rouvrir avant de concevoir L**. Elle est **sans effet sur S** : ni la note, ni le choix de famille pour S n'en dépendent.

## 6 — Ce que ce comparatif ne dit pas

- **Aucun couple continu n'est mesuré dans la condition du robot.** k est une hypothèse ; le banc la remplacera par une mesure.
- **Les prix** sont ceux relevés le 30-09-2026, hors port ; plusieurs viennent de revendeurs.
- **Les données marquées non vérifiées** dans le catalogue ne comptent pas comme établies.
