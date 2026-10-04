# Choix de l'actionneur de S — faits, approvisionnement, exigences

**Engendré** par `.venv/bin/python scripts/choix_actionneurs.py --ecrire`, le 2026-10-04. Ne pas éditer à la main. Aucun score, aucun poids : chaque exigence donne **PASS**, **FAIL**, **UNKNOWN** (l'information manque) ou **TESTED** (mesuré au banc). Les règles de verdict sont dans `params/exigences_S.yaml`.

**Décision** (fiche [0065](../decisions/0065-s-robstride-rs00.md), Jeremy, 2026-10-01) : famille RobStride, RS00 sur les 12 articulations de jambe, **H_S = 0,60 m visée**. Cette grille en vérifie la condition (a).

---

## 0 — Configuration retenue (fiches 0067 et 0068) : RS02 au roulis et au tangage de hanche et au genou, RS00 au lacet de hanche et à la cheville ; 5 axes par jambe

Répartition lue dans `params/configuration_S.yaml`. v1 : buste fixe. v3 : HYPOTHÈSE de haut du corps (masse seulement ; couple des bras non vérifié). Supplément de structure des logements RS02 : hypothèse, compté dans la masse. **Besoins écartés** de la marche de référence (fiche 0068) : left_ankle_roll, right_ankle_roll ; leur effort n'est reporté sur aucun autre axe (hypothèse non vérifiée).

| Version | H | Masse | T1 | T2 | T4 | T5 | H_max prudent | Limitante | Actionneurs (CHF HT) |
| --- | ---: | ---: | :-: | :-: | :-: | :-: | ---: | --- | ---: |
| v1, buste fixe | 0,60 m | 6,75 kg | PASS | PASS | PASS | PASS | 0,804 m | ankle_pitch | 1224 |
| v3, haut 16 × rs05 | 0,60 m | 9,80 kg | PASS | PASS | PASS | PASS | 0,684 m | ankle_pitch | 2693 |
| v1, buste fixe | 0,55 m | 6,38 kg | PASS | PASS | PASS | PASS | 0,804 m | ankle_pitch | 1224 |
| v3, haut 16 × rs05 | 0,55 m | 9,44 kg | PASS | PASS | PASS | PASS | 0,684 m | ankle_pitch | 2693 |

## 1 — Grille technique à H_S = 0,60 m, charge utile 1,2 kg, marge 1,5

| Candidat | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 | T9 |
| --- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| RobStride RS05 | FAIL | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS |
| RobStride EduLite 05 | FAIL | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS |
| Feetech STS3250 | UNKNOWN | PASS | PASS | UNKNOWN | PASS | PASS | UNKNOWN | UNKNOWN | FAIL |
| Damiao DM-J4310-2EC V1.2 | UNKNOWN | PASS | PASS | UNKNOWN | PASS | PASS | UNKNOWN | UNKNOWN | FAIL |
| Damiao DM-J4310-2EC V1.2 (48 V) | UNKNOWN | PASS | PASS | UNKNOWN | PASS | PASS | PASS | PASS | PASS |
| SteadyWin GIM4310-10 (driver GDZ34) | FAIL | PASS | PASS | FAIL | PASS | PASS | UNKNOWN | PASS | FAIL |
| MyActuator RMD-X2-P28-7-E (« X2-7 ») | UNKNOWN | PASS | PASS | UNKNOWN | PASS | PASS | PASS | PASS | UNKNOWN |
| CubeMars AK45-10 V3.0 KV75 | UNKNOWN | PASS | PASS | UNKNOWN | PASS | PASS | PASS | UNKNOWN | PASS |
| RobStride RS00 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HighTorque HTDW-4438-30-NE (HTDW-4530-02-DNE) | UNKNOWN | PASS | PASS | UNKNOWN | PASS | PASS | UNKNOWN | UNKNOWN | UNKNOWN |
| HighTorque HTDW-5047-36-NE | PASS | PASS | PASS | PASS | PASS | PASS | UNKNOWN | UNKNOWN | UNKNOWN |
| Dynamixel XM430-W210 (référence) | UNKNOWN | FAIL | PASS | FAIL | PASS | PASS | UNKNOWN | UNKNOWN | FAIL |
| Xiaomi CyberGear (référence) | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | FAIL |
| CubeMars AK40-10 V3.0 KV170 (référence) | FAIL | FAIL | PASS | FAIL | PASS | PASS | UNKNOWN | UNKNOWN | FAIL |
| Dynamixel XM430-W350 (référence) | UNKNOWN | PASS | PASS | UNKNOWN | PASS | PASS | PASS | UNKNOWN | FAIL |

- **T1** — couple efficace des 12 articulations de jambe à H_S, marge, charge utile comprise — PASS avec le couple PRUDENT (en blocage s'il est publié ; sinon nominal × k_bas, le plus petit rapport blocage/nominal publié au catalogue) ; UNKNOWN s'il ne passe qu'avec le nominal ; FAIL sinon ; UNKNOWN si aucun continu n'est publié
- **T2** — couple de pointe des 12 articulations à H_S, marge, charge utile comprise — PASS ou FAIL
- **T3** — vitesse requise à H_S — PASS si la taille minimale imposée par la vitesse ≤ H_S (vitesse publiée À VIDE, donc optimiste) ; UNKNOWN si la vitesse n'est pas publiée
- **T4** — charge utile — PASS si T1 et T2 passent aussi avec la borne haute de la sensibilité ; UNKNOWN s'ils ne passent qu'avec la valeur de travail ; FAIL s'ils ne passent pas avec elle
- **T5** — relevé depuis l'accroupi profond (section `releve`)
- **T6** — télémétrie : position, couple ou courant, température (faits du comparatif)
- **T7** — seuil de protection thermique publié (catalogue `protection_thermique_C`, sinon une température lue dans `collecte_criteres_manquants.E_protections`)
- **T8** — chien de garde de communication (collecte `E_watchdog`, sinon « TIMEOUT » dans le détail de télémétrie du comparatif)
- **T9** — bus CAN et protocole commun à une famille S → M → L publiée

*k_bas = 0,619*, le plus petit rapport blocage / nominal publié au catalogue : rs03 0,619, rs00 0,720, rs06 0,727, rs05 0,750, rs02 0,857.

## 2 — Masse du robot à H_S, selon la charge utile (RS00 homogène)

| Charge utile | Masse du robot | T1 | T2 | T5 |
| ---: | ---: | :-: | :-: | :-: |
| 0,8 kg | 5,69 kg | PASS | PASS | PASS |
| 1,2 kg | 6,09 kg | PASS | PASS | PASS |
| 1,6 kg | 6,49 kg | PASS | PASS | PASS |

Modèle : `masse(H) = (S0 − m_élec − m_haut) · (H/H0)³ + charge utile + Σ actionneurs`. S0 = 2,876 kg (M0 − 12 Dynamixel de jambe) ; m_élec = 0,600 kg, l'électronique de ToddlerBot comprise dans M0 (`params/exigences_S.yaml`) ; m_haut = 0,987 kg, ses 20 servos du haut du corps, CALCULÉS depuis le modèle amont (`dimensionnement.masse_haut_du_corps_amont`) et retirés depuis la fiche 0067 : la v1 a un buste fixe. Tous deux sont retirés de la part mise à l'échelle.

## 3 — Relevé depuis l'accroupi profond (T5)

- Posture : accroupi profond : pieds à plat, cuisse horizontale, tibia incliné vers l'avant ; centre de masse à la verticale des chevilles (équilibre quasi statique).
- Tibia incliné de **40°** vers l'avant (hypothèse de Claude Code, non sourcée : ordre de grandeur d'une flexion dorsale de cheville en accroupi ; à remplacer par les butées articulaires de YXOR).
- Répartition : 0,5 par jambe (hypothèse : appui symétrique sur les deux jambes).
- Masse portée : la masse TOTALE du robot (prudent : les tibias et les pieds ne chargent pas le genou).
- Longueurs : cuisse et tibia = ratios ANSUR II de params/anthropometry.yaml × H_S (plus longs que ceux de ToddlerBot, donc plus défavorables).
- Verdict : PASS si marge × couple ≤ couple de pointe ; le couple tenu en continu (blocage ou nominal) est affiché pour information : un relevé dure quelques secondes.

| Candidat | Masse (kg) | Cuisse / tibia (m) | Genou (N·m) | Hanche (N·m) | Marge × max | Pointe | Continu prudent | T5 |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | :-: |
| RobStride RS05 | 4,70 | 0,149 / 0,136 | 2,01 | 1,41 | 3,02 | 5,5 | 1,20 | PASS |
| RobStride EduLite 05 | 5,21 | 0,149 / 0,136 | 2,23 | 1,56 | 3,35 | 5,5 | 1,11 | PASS |
| Feetech STS3250 | 3,53 | 0,149 / 0,136 | 1,51 | 1,06 | 2,27 | 4,9 | 0,97 | PASS |
| Damiao DM-J4310-2EC V1.2 | 5,85 | 0,149 / 0,136 | 2,51 | 1,75 | 3,76 | 12,5 | 2,17 | PASS |
| Damiao DM-J4310-2EC V1.2 (48 V) | 5,85 | 0,149 / 0,136 | 2,51 | 1,75 | 3,76 | 12,5 | 2,17 | PASS |
| SteadyWin GIM4310-10 (driver GDZ34) | 5,06 | 0,149 / 0,136 | 2,17 | 1,52 | 3,25 | 8,0 | 1,01 | PASS |
| MyActuator RMD-X2-P28-7-E (« X2-7 ») | 5,39 | 0,149 / 0,136 | 2,31 | 1,61 | 3,46 | 7,0 | 1,55 | PASS |
| CubeMars AK45-10 V3.0 KV75 | 5,41 | 0,149 / 0,136 | 2,32 | 1,62 | 3,48 | 7,0 | 1,55 | PASS |
| RobStride RS00 | 6,09 | 0,149 / 0,136 | 2,61 | 1,82 | 3,91 | 14,0 | 3,60 | PASS |
| HighTorque HTDW-4438-30-NE (HTDW-4530-02-DNE) | 5,16 | 0,149 / 0,136 | 2,21 | 1,55 | 3,32 | 10,0 | 1,24 | PASS |
| HighTorque HTDW-5047-36-NE | 5,84 | 0,149 / 0,136 | 2,50 | 1,75 | 3,75 | 16,0 | 2,48 | PASS |
| Dynamixel XM430-W210 (référence) | 3,61 | 0,149 / 0,136 | 1,55 | 1,08 | 2,32 | 3,0 | — | PASS |
| Xiaomi CyberGear (référence) | 5,96 | 0,149 / 0,136 | 2,55 | 1,79 | 3,83 | 12,0 | 2,48 | PASS |
| CubeMars AK40-10 V3.0 KV170 (référence) | 4,69 | 0,149 / 0,136 | 2,01 | 1,40 | 3,01 | 4,1 | 0,80 | PASS |
| Dynamixel XM430-W350 (référence) | 3,61 | 0,149 / 0,136 | 1,55 | 1,08 | 2,32 | 4,1 | — | PASS |

Sensibilité à l'angle du tibia, RS00 : 30° → genou 2,03 N·m, hanche 2,40 N·m ; 40° → genou 2,61 N·m, hanche 1,82 N·m ; 50° → genou 3,11 N·m, hanche 1,32 N·m.

## 4 — Faits techniques

| Candidat | Clé de révision | Nominal (N·m) | Blocage (N·m) | Pointe (N·m) | Masse (g) | Vitesse à vide (rpm) | Tension / plage (V) | Réduction | Bus | Protection (°C) | Taille max prudente – optimiste (m) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- | ---: | --- |
| RobStride RS05 | RobStride Dynamics RS05 · rév. non publiée · 48 V · firmware non publié | 1,60 | 1,20 | 5,5 | 191 | 480 | 48 (15,0–60,0) | 7,75 | CAN 2.0 / CAN FD | 135 | 0,49 – 0,57 |
| RobStride EduLite 05 | RobStride Dynamics EduLite 05 (EL05) · rév. non publiée · 48 V · firmware non publié | 1,80 | — | 5,5 | 242 | 430 | 48 | 9,00 | CAN 2.0 | — | 0,43 – 0,58 |
| Feetech STS3250 | Feetech STS3250 · rév. non publiée · 12 V · firmware non publié | 1,57 | — | 4,9 | 74 | 75 | 12 | — | TTL série half-duplex asynchrone | — | 0,52 – 0,64 |
| Damiao DM-J4310-2EC V1.2 | Damiao (DM) DM-J4310-2EC · rév. V1.2 · 24 V · firmware non publié | 3,50 | — | 12,5 | 306 | 200 | 24 (20,0–28,0) | 10,00 | CAN 2.0B | — | 0,60 – 0,76 |
| Damiao DM-J4310-2EC V1.2 (48 V) | Damiao (DM) DM-J4310-2EC · rév. V1.2 · 48 V · firmware non publié | 3,50 | — | 12,5 | 306 | 450 | 48 (20,0–58,0) | 10,00 | CAN 2.0B | 100 | 0,60 – 0,76 |
| SteadyWin GIM4310-10 (driver GDZ34) | SteadyWin GIM4310-10 (driver GDZ34) · rév. non publiée · 24 V · firmware non publié | 1,63 | — | 8,0 | 227 | 212 | 24 | 10,00 | CAN | — | 0,41 – 0,56 |
| MyActuator RMD-X2-P28-7-E (« X2-7 ») | MyActuator RMD-X2-P28-7-E · rév. non publiée · 24 V · firmware non publié | 2,50 | — | 7,0 | 260 | 178 | 24 (20,0–55,0) | 28,17 | CAN 1 Mbit/s | — | 0,52 – 0,67 |
| CubeMars AK45-10 V3.0 KV75 | CubeMars AK45-10 KV75 · rév. V3.0 · 24 V · firmware non publié | 2,50 | — | 7,0 | 262 | 180 | 24 | 10,00 | CAN 1 Mbit/s | — | 0,52 – 0,67 |
| RobStride RS00 | RobStride Dynamics RS00 · rév. non publiée · 48 V · firmware non publié | 5,00 | 3,60 | 14,0 | 330 | 315 | 48 (24,0–60,0) | 10,00 | CAN 2.0 | 135 | 0,76 – 0,87 |
| HighTorque HTDW-4438-30-NE (HTDW-4530-02-DNE) | HighTorque Robotics HTDW-4438-30-NE · rév. non publiée · 24 V · firmware non publié | 2,00 | — | 10,0 | 237 | 160 | 24 (12,0–50,4) | 30,00 | CAN FD / CAN | — | 0,46 – 0,61 |
| HighTorque HTDW-5047-36-NE | HighTorque Robotics HTDW-5047-36-NE · rév. non publiée · 24 V · firmware non publié | 4,00 | — | 16,0 | 305 | 60 | 24 (12,0–48,0) | 36,00 | CAN FD / CAN | — | 0,64 – 0,80 |
| Dynamixel XM430-W210 (référence) | ROBOTIS XM430-W210 · rév. non publiée · 12 V · firmware non publié | — | — | 3,0 | 82 | 77 | 12 | 212,60 | TTL ou RS485 | — | 0,55 – 0,55 |
| Xiaomi CyberGear (référence) | Xiaomi CyberGear · rév. non publiée · 24 V · firmware non publié | 4,00 | — | 12,0 | 317 | 296 | 24 (16,0–28,0) | 7,75 | CAN 2.0 | 75 | 0,64 – 0,80 |
| CubeMars AK40-10 V3.0 KV170 (référence) | CubeMars AK40-10 KV170 · rév. V3.0 · 24 V · firmware non publié | 1,30 | — | 4,1 | 190 | 435 | 24 | 10,00 | CAN | — | 0,37 – 0,51 |
| Dynamixel XM430-W350 (référence) | ROBOTIS XM430-W350-T / -R · rév. non publiée · 12 V · firmware non publié | — | — | 4,1 | 82 | 46 | 12 (10,0–14,8) | 353,50 | TTL ou RS485 | 80 | 0,63 – 0,63 |

Tailles maximales en configuration homogène, avec la charge utile de 1,2 kg. La vitesse est À VIDE ; sous charge, l'actionneur tourne moins vite.

## 5 — Approvisionnement (daté : il vieillit)

| Candidat | A1 | A2 | A3 | A4 |
| --- | :-: | :-: | :-: | :-: |
| RobStride RS05 | PASS | UNKNOWN | PASS | UNKNOWN |
| RobStride EduLite 05 | PASS | UNKNOWN | PASS | UNKNOWN |
| Feetech STS3250 | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Damiao DM-J4310-2EC V1.2 | PASS | PASS | UNKNOWN | UNKNOWN |
| Damiao DM-J4310-2EC V1.2 (48 V) | PASS | UNKNOWN | UNKNOWN | UNKNOWN |
| SteadyWin GIM4310-10 (driver GDZ34) | PASS | PASS | UNKNOWN | UNKNOWN |
| MyActuator RMD-X2-P28-7-E (« X2-7 ») | PASS | UNKNOWN | PASS | UNKNOWN |
| CubeMars AK45-10 V3.0 KV75 | PASS | UNKNOWN | UNKNOWN | UNKNOWN |
| RobStride RS00 | PASS | UNKNOWN | PASS | PASS |
| HighTorque HTDW-4438-30-NE (HTDW-4530-02-DNE) | PASS | UNKNOWN | UNKNOWN | UNKNOWN |
| HighTorque HTDW-5047-36-NE | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Dynamixel XM430-W210 (référence) | PASS | PASS | UNKNOWN | UNKNOWN |
| Xiaomi CyberGear (référence) | PASS | UNKNOWN | PASS | UNKNOWN |
| CubeMars AK40-10 V3.0 KV170 (référence) | PASS | UNKNOWN | PASS | UNKNOWN |
| Dynamixel XM430-W350 (référence) | PASS | PASS | UNKNOWN | UNKNOWN |

- **A1** — prix relevé et daté
- **A2** — revendeur en Suisse ou dans l'UE identifié (sinon UNKNOWN : livraison non vérifiée)
- **A3** — garantie écrite du constructeur ≥ 12 mois
- **A4** — stock vérifié (« en stock » relevé sur la page du vendeur) ; sinon UNKNOWN

| Candidat | Prix | Vendeur | Relevé le | Revendeur CH / UE | Garantie (mois) |
| --- | ---: | --- | --- | --- | ---: |
| RobStride RS05 | 110,00 USD | Seeed Studio | 2026-09-30 | — | 12 |
| RobStride EduLite 05 | 80,00 USD | Seeed Studio | 2026-09-30 | — | 12 |
| Feetech STS3250 | —  | — | 2026-09-30 | — | — |
| Damiao DM-J4310-2EC V1.2 | 158,00 EUR | Eckstein GmbH (DE) | 2026-09-30 | Eckstein GmbH (DE) | — |
| Damiao DM-J4310-2EC V1.2 (48 V) | 140,95 EUR | OpenELAB | 2026-09-30 | — | — |
| SteadyWin GIM4310-10 (driver GDZ34) | 169,95 EUR | OpenELAB (localisation DE) | 2026-09-30 | OpenELAB (localisation DE) | — |
| MyActuator RMD-X2-P28-7-E (« X2-7 ») | 299,95 EUR | OpenELAB | 2026-09-30 | — | 12 |
| CubeMars AK45-10 V3.0 KV75 | 155,90 USD | CubeMars | 2026-09-30 | — | — |
| RobStride RS00 | 125,00 USD | Seeed Studio | 2026-10-01 | — | 12 |
| HighTorque HTDW-4438-30-NE (HTDW-4530-02-DNE) | 189,00 USD | Seeed Studio | 2026-10-01 | — | — |
| HighTorque HTDW-5047-36-NE | —  | — | 2026-10-01 | — | — |
| Dynamixel XM430-W210 (référence) | 264,50 EUR | Generation Robots (FR) | 2026-09-30 | Generation Robots (FR), Reichelt (DE) | — |
| Xiaomi CyberGear (référence) | 179,00 USD | AIFitLab (HK) | 2026-10-01 | — | 12 |
| CubeMars AK40-10 V3.0 KV170 (référence) | 135,90 USD | CubeMars | 2026-10-01 | — | 12 |
| Dynamixel XM430-W350 (référence) | 264,50 EUR | Generation Robots (FR) | 2026-10-01 | Generation Robots (FR), Reichelt (DE) | — |

## 6 — Banc : le critère du § 4 du protocole

Écrit AVANT la mesure (`docs/protocole-banc.md`, § 4). Le plus faible des continus au blocage MESURÉS du RS00 remplace la valeur publiée ; T1, T2, T4 et T5 sont relancés à H_S puis à la hauteur de repli. Verdict : « S confirmé », « repli à 0,55 m » ou « famille rouverte ». La valeur publiée reste au catalogue, intacte.

**Aucune mesure au blocage du RS00 dans `params/mesures.yaml` : pas de verdict.** Valeur publiée : 3,6 N·m (PDF RobStride du 2026-09-17, p. 5).


## 7 — Ce que ce document ne dit pas

- **Les besoins de couple viennent de la marche de ToddlerBot**, dont plusieurs articulations touchaient leur borne : ce sont des **minimums**.
- **La charge utile est une hypothèse** (PROPOSÉ par Claude (arbitrage), prompt R3 du 2026-10-01 : ordre de grandeur, à remplacer par les composants réels).
- **Le relevé est quasi statique** : il ignore l'accélération et le choc de la chute elle-même.
- **T7, T8 et A4 lisent du texte** quand le fait n'est pas structuré (règles dans `params/exigences_S.yaml`). La collecte du 2026-10-01 ne couvre pas les candidats ajoutés au lot H.
- Les références *(réf.)* sont listées pour comparaison ; elles ne sont pas candidates.
