> **v1, méthode corrigée : voir `docs/choix-famille-actionneurs.md`.** Ce document n'est plus régénéré ni tenu à jour. Trois défauts de méthode y ont été corrigés le 30-09-2026 au soir (relecture externe) : un éliminatoire de taille qui contredisait la démarche inversée, une capacité en valeur unique, et une comparaison de modèles au lieu de familles. Il est gardé pour la trace, tel qu'il a été produit.

# Choix de la classe d'actionneur de S — comparatif multicritère

**Engendré** par `.venv/bin/python scripts/selection_multicritere.py --ecrire`, le 2026-09-30. Ne pas éditer à la main : le régénérer. Aucune fiche, aucun achat proposé (CLAUDE.md, règle d'achat c) : c'est un comparatif demandé, qui prépare une décision de Jeremy.

Sources : `params/actionneurs.yaml` (catalogue et `comparatif_S`, chaque valeur sourcée, version de fiche et sha256), `params/criteres_selection.yaml` (grilles écrites **avant** le calcul, poids **proposés, à fixer par Jeremy**, jugements justifiés), `params/budget.yaml` (taux BCE). Statuts : les notes sont **calculées** depuis le catalogue, sauf celles marquées **JUGEMENT**.

---

## 1 — Les candidats

| Candidat | Continu retenu (N·m) | Condition | En blocage | Pointe | Masse (g) | Tension | Prix HT (CHF) | H_max à marge 1,5 | H_max avec le nominal publié |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RobStride RS05 | 1,60 | à 100 rpm, plaque aluminium 70 × 70 mm, 2,4 Apk | 1,20 | 5,50 | 191,0 | 48 V | 91,82 | **0,54 m** | 0,57 m |
| RobStride EduLite 05 | 1,80 | à 100 rpm, plaque de dissipation aluminium 70 × 70 mm, 25 °C, 48 V, enroulement limité à 135 °C | — | 6,00 | 242,0 | 48 V | 66,78 | **0,54 m** | 0,54 m |
| Feetech STS3250 | 1,57 | non précisée | — | 4,90 | 74,5 | 12 V | — | **0,60 m** | 0,60 m |
| Damiao DM-J4310-2EC V1.2 | 3,50 | non précisée ; à 3,5 N·m, 120 rpm, 24 V, le moteur passe de ~32 °C à ~99 °C en ~310 s (courbe constructeur) : ce n'est PAS un régime établi | — | 12,50 | 306,0 | 24 V | 125,84 | **0,67 m** | 0,67 m |
| SteadyWin GIM4310-10 (driver GDZ34) | 1,63 | non précisée | — | 7,98 | 227,0 | 24 V | 161,08 | **0,53 m** | 0,53 m |
| MyActuator RMD-X2-P28-7-E (« X2-7 ») | 2,50 | à 142 rpm, 3 A ; condition thermique non précisée | — | 7,00 | 260,0 | 24 V | — | **0,61 m** | 0,61 m |
| CubeMars AK45-10 V3.0 KV75 | 2,50 | à 120 rpm, 1,9 A ; condition thermique non précisée | — | 7,00 | 262,0 | 24 V | 130,13 | **0,61 m** | 0,61 m |
| Dynamixel XM430-W210 (référence) *(référence)* | — | non précisée | — | 3,00 | 82,0 | 12 V | 250,69 | **0,53 m** | 0,53 m |

**Couple continu retenu** : celui publié sur la **plus petite plaque de dissipation**, sinon le nominal. Cette règle a été **modifiée le 2026-09-30** en remplissant le catalogue, avant tout calcul de note : la version initiale (« en blocage s'il est publié ») aurait pénalisé RobStride, seul fabricant à publier une valeur en blocage. Voir `criteres_selection.yaml`.

---

## 2 — Éliminatoires

| Candidat | H_max ≥ 0,55 m | Télémétrie (position, couple ou courant, température) | État |
| --- | --- | --- | --- |
| RobStride RS05 | éliminé | admis | **éliminé** |
| RobStride EduLite 05 | éliminé | admis | **éliminé** |
| Feetech STS3250 | admis | admis | **admis** |
| Damiao DM-J4310-2EC V1.2 | admis | admis | **admis** |
| SteadyWin GIM4310-10 (driver GDZ34) | éliminé | admis | **éliminé** |
| MyActuator RMD-X2-P28-7-E (« X2-7 ») | admis | admis | **admis** |
| CubeMars AK45-10 V3.0 KV75 | admis | admis | **admis** |
| Dynamixel XM430-W210 (référence) | non évaluable | admis | **non évaluable** (référence, hors classement) |

Un **éliminé** ne peut pas gagner, quels que soient les poids. Un **non évaluable** reste classé, et son manque est affiché.

**⚠ Éliminations qui tiennent à la condition de mesure.** RobStride RS05 : 0,54 m avec 1,60 N·m (à 100 rpm, plaque aluminium 70 × 70 mm, 2,4 Apk), mais 0,57 m avec son nominal publié. La règle retient la plus petite plaque publiée (§ 1) : c'est elle qui élimine. Sous l'autre lecture, ces candidats seraient admis. **C'est une élimination de justesse, qui dépend d'une convention**, et non d'une impossibilité.

---

## 3 — Notes et score

| Critère | Poids (proposé) | RobStride RS05 | RobStride EduLite 05 | Feetech STS3250 | Damiao DM-J4310-2EC V1.2 | SteadyWin GIM4310-10 (driver GDZ34) | MyActuator RMD-X2-P28-7-E (« X2-7 ») | CubeMars AK45-10 V3.0 KV75 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| capacite | 20 | 0 | 0 | 1 | 3 | 0 | 1 | 1 |
| cout | 20 | 3 | 4 | 0 | 3 | 2 | 0 | 2 |
| continuite | 15 | 5 | 5 | 0 | 2 | 2 | 2 | 2 |
| fiabilite_fournisseur | 15 | 3 | 3 | 1 | 2 | 2 | 3 | 1 |
| robustesse | 10 | 3 | 3 | 1 | 3 | 3 | 5 | 5 |
| masse | 5 | 4 | 3 | 5 | 2 | 3 | 2 | 2 |
| ouverture | 5 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| tension_securite | 5 | 2 | 2 | 5 | 4 | 4 | 4 | 4 |
| disponibilite | 5 | 3 | 3 | 1 | 4 | 4 | 1 | 2 |
| **score /5** | | **2,65** (éliminé) | **2,80** (éliminé) | **1,10** | **2,70** | **1,95** (éliminé) | **1,90** | **2,05** |

### Justification de chaque note

**RobStride RS05**

- capacite = 0 — H_max 0,54 m avec 1,60 N·m continu (à 100 rpm, plaque aluminium 70 × 70 mm, 2,4 Apk) → 0, −1 dissipation/condition → 0
- cout = 3 — 91,82 CHF HT (110.0 USD, Seeed Studio)
- continuite = 5 — bus CAN ; protocole = M/L (robstride_can) ; 48 V
- fiabilite_fournisseur = 3 — garantie écrite 12 mois ; UE non ; CH non
- robustesse = 3 — JUGEMENT — planétaire à pignons acier 7,75:1, protections documentées (surchauffe, surintensité, blocage) ; réversibilité non publiée → 3 selon la grille, strictement
- masse = 4 — 191,0 g
- ouverture = 2 — protocole public oui ; SDK libre non établi ; firmware libre non
- tension_securite = 2 — 48 V
- disponibilite = 3 — Seeed Studio

**RobStride EduLite 05**

- capacite = 0 — H_max 0,54 m avec 1,80 N·m continu (à 100 rpm, plaque de dissipation aluminium 70 × 70 mm, 25 °C, 48 V, enroulement limité à 135 °C) → 0, −1 dissipation/condition → 0
- cout = 4 — 66,78 CHF HT (80.0 USD, Seeed Studio)
- continuite = 5 — bus CAN ; protocole = M/L (robstride_can) ; 48 V
- fiabilite_fournisseur = 3 — garantie écrite 12 mois ; UE non ; CH non
- robustesse = 3 — JUGEMENT — 9:1, protections documentées comme le RS05 ; type de réducteur et réversibilité non publiés par le constructeur → 3
- masse = 3 — 242,0 g
- ouverture = 2 — protocole public oui ; SDK libre non établi ; firmware libre non
- tension_securite = 2 — 48 V
- disponibilite = 3 — Seeed Studio

**Feetech STS3250**

- capacite = 1 — H_max 0,60 m avec 1,57 N·m continu (condition non précisée) → 2, −1 dissipation/condition → 1
- cout = 0 — prix inconnu → 0 par prudence
- continuite = 0 — bus non CAN ; protocole ≠ M/L (feetech_ttl) ; 12 V
- fiabilite_fournisseur = 1 — garantie écrite non trouvée ; UE non ; CH non
- robustesse = 1 — JUGEMENT — servo à engrenages, rapport annoncé 1:345 (non vérifié) ; la protection se déclenche vers 25 kg·cm selon un essai tiers → fragile au blocage prolongé
- masse = 5 — 74,5 g
- ouverture = 2 — protocole public oui ; SDK libre non établi ; firmware libre non
- tension_securite = 5 — 12 V
- disponibilite = 1 — non vérifié : OpenELAB 73,99 USD ; Alibaba 38,05 CHF

**Damiao DM-J4310-2EC V1.2**

- capacite = 3 — H_max 0,67 m avec 3,50 N·m continu (non précisée ; à 3,5 N·m, 120 rpm, 24 V, le moteur passe de ~32 °C à ~99 °C en ~310 s (courbe constructeur) : ce n'est PAS un régime établi) → 4, −1 dissipation/condition → 3
- cout = 3 — 125,84 CHF HT (158.0 EUR, Eckstein GmbH (DE))
- continuite = 2 — bus CAN ; protocole ≠ M/L (damiao_can) ; 24 V
- fiabilite_fournisseur = 2 — garantie écrite non trouvée ; UE Eckstein GmbH (DE) ; CH non
- robustesse = 3 — JUGEMENT — 10:1, codes d'erreur documentés (surchauffe MOS et bobinage) ; type d'engrenage et réversibilité non publiés → 3
- masse = 2 — 306,0 g
- ouverture = 2 — protocole public oui ; SDK libre non établi ; firmware libre non
- tension_securite = 4 — 24 V
- disponibilite = 4 — Eckstein GmbH (DE)

**SteadyWin GIM4310-10 (driver GDZ34)**

- capacite = 0 — H_max 0,53 m avec 1,63 N·m continu (non précisée) → 0, −1 dissipation/condition → 0
- cout = 2 — 161,08 CHF HT (169.95 EUR, OpenELAB (localisation DE))
- continuite = 2 — bus CAN ; protocole ≠ M/L (steadywin_can) ; 24 V
- fiabilite_fournisseur = 2 — garantie écrite non trouvée ; UE OpenELAB (localisation DE) ; CH non
- robustesse = 3 — JUGEMENT — planétaire acier 10:1, défauts documentés ; réversibilité non publiée → 3
- masse = 3 — 227,0 g
- ouverture = 2 — protocole public oui ; SDK libre non établi ; firmware libre non
- tension_securite = 4 — 24 V
- disponibilite = 4 — OpenELAB (localisation DE)

**MyActuator RMD-X2-P28-7-E (« X2-7 »)**

- capacite = 1 — H_max 0,61 m avec 2,50 N·m continu (à 142 rpm, 3 A ; condition thermique non précisée) → 2, −1 dissipation/condition → 1
- cout = 0 — prix inconnu → 0 par prudence
- continuite = 2 — bus CAN ; protocole ≠ M/L (myactuator_can) ; 24 V
- fiabilite_fournisseur = 3 — garantie écrite 12 mois ; UE non ; CH non
- robustesse = 5 — JUGEMENT — planétaire 28,17:1 (< 50:1), couple de réversibilité publié 0,4 N·m, protections documentées (blocage, surchauffe…) → 5
- masse = 2 — 260,0 g
- ouverture = 2 — protocole public oui ; SDK libre non établi ; firmware libre non
- tension_securite = 4 — 24 V
- disponibilite = 1 — non vérifié : A2V (France) selon l'étude externe ; Eckstein et OpenELAB selon des résumés

**CubeMars AK45-10 V3.0 KV75**

- capacite = 1 — H_max 0,61 m avec 2,50 N·m continu (à 120 rpm, 1,9 A ; condition thermique non précisée) → 2, −1 dissipation/condition → 1
- cout = 2 — 130,13 CHF HT (155.9 USD, CubeMars)
- continuite = 2 — bus CAN ; protocole ≠ M/L (cubemars_can) ; 24 V
- fiabilite_fournisseur = 1 — garantie écrite non trouvée ; UE non ; CH non
- robustesse = 5 — JUGEMENT — planétaire 10:1, couple de réversibilité publié 0,1 N·m, codes d'erreur (surchauffe, blocage…) → 5
- masse = 2 — 262,0 g
- ouverture = 2 — protocole public oui ; SDK libre non établi ; firmware libre non
- tension_securite = 4 — 24 V
- disponibilite = 2 — CubeMars (direct)

**Dynamixel XM430-W210 (référence)** (référence)

- capacite = 0 — H_max 0,53 m avec — N·m continu (condition non précisée) → 0 ; continu inconnu → 0
- cout = 1 — 250,69 CHF HT (264.5 EUR, Generation Robots (FR))
- continuite = 0 — bus non CAN ; protocole ≠ M/L (dynamixel_p2) ; 12 V
- fiabilite_fournisseur = 2 — garantie écrite non trouvée ; UE Generation Robots (FR), Reichelt (DE) ; CH non
- robustesse = 1 — JUGEMENT — servo à engrenages 212,6:1 ; la garantie annoncée exclut les engrenages usés et les moteurs brûlés → 1
- masse = 5 — 82,0 g
- ouverture = 4 — protocole public oui ; SDK libre oui ; firmware libre non
- tension_securite = 5 — 12 V
- disponibilite = 4 — Generation Robots (FR), Reichelt (DE)

---

## 4 — Sensibilité

Vainqueur aux poids proposés : **Damiao DM-J4310-2EC V1.2**.

| Poids modifié | × 0,5 | × 1,5 |
| --- | --- | --- |
| capacite | Damiao DM-J4310-2EC V1.2 | Damiao DM-J4310-2EC V1.2 |
| cout | Damiao DM-J4310-2EC V1.2 | Damiao DM-J4310-2EC V1.2 |
| continuite | Damiao DM-J4310-2EC V1.2 | Damiao DM-J4310-2EC V1.2 |
| fiabilite_fournisseur | Damiao DM-J4310-2EC V1.2 | Damiao DM-J4310-2EC V1.2 |
| robustesse | Damiao DM-J4310-2EC V1.2 | Damiao DM-J4310-2EC V1.2 |
| masse | Damiao DM-J4310-2EC V1.2 | Damiao DM-J4310-2EC V1.2 |
| ouverture | Damiao DM-J4310-2EC V1.2 | Damiao DM-J4310-2EC V1.2 |
| tension_securite | Damiao DM-J4310-2EC V1.2 | Damiao DM-J4310-2EC V1.2 |
| disponibilite | Damiao DM-J4310-2EC V1.2 | Damiao DM-J4310-2EC V1.2 |

**18 variations sur 18** laissent le vainqueur inchangé.

Fréquence de victoire sur 1 000 jeux de poids tirés au hasard (Dirichlet α = 1, graine 20260930) :

| Candidat | Victoires | Fréquence |
| --- | ---: | ---: |
| Damiao DM-J4310-2EC V1.2 | 789 | 78,9 % |
| MyActuator RMD-X2-P28-7-E (« X2-7 ») | 97 | 9,7 % |
| CubeMars AK45-10 V3.0 KV75 | 70 | 7,0 % |
| Feetech STS3250 | 44 | 4,4 % |

## 5 — Verdict

**Classement ROBUSTE.** Damiao DM-J4310-2EC V1.2 gagne toutes les variations ±50 % et 78,9 % des tirages aléatoires (seuil : 60 %).

## 6 — Ce que ce comparatif ne dit pas

- **Les poids sont proposés, pas décidés.** La sensibilité dit seulement si le classement en dépend.
- **Toutes les tailles sont des plafonds optimistes** : la marche de référence était écrêtée (cadrage § 3).
- **Aucun couple continu n'est mesuré dans la condition du robot.** Chaque valeur est celle du constructeur, sur sa plaque ou sans condition précisée ; le banc la mesurera.
- **Les prix sont hors TVA suisse et hors port** ; un prix inconnu vaut 0 dans la note de coût, par prudence.
- **Les données marquées non vérifiées** dans le catalogue ne comptent pas comme établies.
- **⚠ Damiao DM-J4310-2EC V1.2 : son couple continu n'est pas un régime établi.** Condition publiée : « non précisée ; à 3,5 N·m, 120 rpm, 24 V, le moteur passe de ~32 °C à ~99 °C en ~310 s (courbe constructeur) : ce n'est PAS un régime établi ». La grille ne retire qu'un point pour une condition non précisée ; sa capacité (0,67 m) est donc probablement **surestimée**. C'est le vainqueur nominal : c'est le premier point à vérifier au banc.
