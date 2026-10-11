# Le parcours guidé du Kit (2026-10)

**Engendré** par `.venv/bin/python scripts/kit_parcours.py --ecrire`. **Les étapes sont PROPOSÉES, non décidées.** Décidé par Jeremy (fiche 0076) : le parcours guidé, le réemploi, préconiser sans imposer, l'outillage du Kit. Méthode : en tête de `scripts/kit_parcours.py`.

## Par étape

| Étape | Coût durable (CHF HT, borne basse) | Coût structure | Durables sans prix | Réemploi depuis les étapes précédentes | Réemployable dans le Lab | Alimentation | Pire courant 12 V (A) | Énergie du pack (Wh) | Marge la plus juste |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | --- |
| 0. maquette carton | ≥ 0 | 0 | 1 | — % | — % | aucune | 0,0 | — | — |
| 1. tête de bureau | ≥ 120 | 0 | 2 | 0 % | 39 % | secteur 12 V | 5,4 | — | neck_pitch (sts3215_c018) ×39,06 |
| 2. tête qui parle | ≥ 329 | 0 | 3 | 36 % | 14 % | secteur 12 V | 7,5 | — | neck_pitch (sts3215_c018) ×28,18 |
| 3. buste à bras | ≥ 619 | 0 | 3 | 49 % | 14 % | secteur 12 V | 23,7 | — | shoulder_pitch (sts3215_c018) ×13,40 |
| 4. base à roues | ≥ 691 | 0 | 7 | 83 % | 16 % | batterie de moins de 100 Wh (3S1P de la cellule du Lab) ; variante batterie d'outillage | 29,1 | 52,5 | shoulder_pitch (sts3215_c018) ×13,40 |
| 5. jambes | ≥ 1 055 | 0 | 5 | 65 % | 11 % | batterie de moins de 100 Wh (3S1P de la cellule du Lab) | 56,4 | 52,5 | ankle_pitch (sts3250) ×2,10 |

Marge : couple CONTINU publié du servo ÷ couple statique requis ; la marge de la fiche 0051 vaut 1,5. Réemploi : coût des durables déjà achetés à une étape précédente ÷ coût des durables de l'étape.

## Étape 0 : maquette carton

le robot entier en carton, passif : poses, proportions, montage, noms d'axes (plans du niveau 0).

Alimentation : aucune. Outillage (celui du Kit seulement) : cutter, feuille, imprimante, cartons, règle, équerre, agrafeuse, pistolet à colle.

| Composant | Nombre | Classe | Fixation | Prix unitaire (CHF HT) | Source |
| --- | ---: | --- | --- | ---: | --- |
| carton (niveau0) | 1 | STRUCTURE | tenon | 0,00 | carton de récupération : 0 CHF |
| vis M4, écrous à frein, rondelles larges (pivots) | 38 | DURABLE | écrou | — | aucun marché relevé |

## Étape 1 : tête de bureau

deux STS3215 en pan-tilt, une caméra, un adaptateur USB, branchée sur un PC.

Alimentation : secteur 12 V. Outillage (celui du Kit seulement) : cutter, feuille, imprimante, cartons, règle, équerre, pistolet à colle ; et un tournevis ou une clé pour les vis M2 à M4 : HORS de la liste du 2026-10-09 (« cutter, feuille, imprimante, cartons, agrafeuse, règle, équerre, pistolet à colle »), à confirmer par Jeremy.

| Composant | Nombre | Classe | Fixation | Prix unitaire (CHF HT) | Source |
| --- | ---: | --- | --- | ---: | --- |
| sts3215_c018 | 2 | DURABLE | vis | 21,07 | actionneurs.yaml |
| bride métallique pour STS3215 (place de marché, sans marque reconnue) | 2 | DURABLE | vis | 24,09 | kit_parcours_marche.yaml |
| caméra USB (la Camera Module 3 se branche sur un Raspberry Pi, pas sur un PC) | 1 | DURABLE | vis | — | aucun marché relevé |
| Bus Servo Adapter (A) (SKU 25514) | 1 | DURABLE | vis | 4,17 | bus.yaml |
| Mean Well LRS-150F-12, alimentation à découpage « enclosed » (12.5 A) | 1 | DURABLE | connecteur | 25,35 | kit_marche.yaml ; sur la table, hors du robot ; dispo : ab Lager, Lieferzeit: 3 - 4 Werktage |
| vis M2 et M3 (brides, palonniers) | 1 | DURABLE | vis | — | aucun marché relevé |
| carton (tete) | 1 | STRUCTURE | colle | 0,00 | carton de récupération : 0 CHF |

| Axe | Servo | Couple requis (N·m) | Marge (continu ÷ requis) | Note |
| --- | --- | ---: | ---: | --- |
| neck_yaw | sts3215_c018 | 0,000 | — | aucun couple statique (lacet) |
| neck_pitch | sts3215_c018 | 0,025 | 39,06 | statique |

## Étape 2 : tête qui parle

micro, haut-parleur, Raspberry Pi 5 ; variantes IA « réseau » (le modèle tourne ailleurs) et « locale » (sur le Pi, avec ou sans AI HAT+ 2).

Alimentation : secteur 12 V. Outillage (celui du Kit seulement) : cutter, feuille, imprimante, cartons, règle, équerre, pistolet à colle ; et un tournevis ou une clé pour les vis M2 à M4 : HORS de la liste du 2026-10-09 (« cutter, feuille, imprimante, cartons, agrafeuse, règle, équerre, pistolet à colle »), à confirmer par Jeremy.

| Composant | Nombre | Classe | Fixation | Prix unitaire (CHF HT) | Source |
| --- | ---: | --- | --- | ---: | --- |
| sts3215_c018 | 2 | DURABLE | vis | 21,07 | actionneurs.yaml |
| bride métallique pour STS3215 (place de marché, sans marque reconnue) | 2 | DURABLE | vis | 24,09 | kit_parcours_marche.yaml |
| Raspberry Pi Camera Module 3 (standard) | 1 | DURABLE | vis | 29,90 | capteurs.yaml (Bastelgarage.ch) |
| Raspberry Pi 5 8GB | 1 | DURABLE | vis | 146,07 | calculateurs.yaml |
| D42V55F5 (5V, 6A Step-Down Voltage Regulator) | 1 | DURABLE | vis | 33,65 | puissance.yaml |
| Bus Servo Adapter (A) (SKU 25514) | 1 | DURABLE | vis | 4,17 | bus.yaml |
| microphone USB | 1 | DURABLE | clip | — | aucun marché relevé |
| haut-parleur et amplificateur | 1 | DURABLE | vis | — | aucun marché relevé |
| Mean Well LRS-150F-12, alimentation à découpage « enclosed » (12.5 A) | 1 | DURABLE | connecteur | 25,35 | kit_marche.yaml ; sur la table, hors du robot ; dispo : ab Lager, Lieferzeit: 3 - 4 Werktage |
| vis M2 et M3 | 1 | DURABLE | vis | — | aucun marché relevé |
| carton (tete) | 1 | STRUCTURE | colle | 0,00 | carton de récupération : 0 CHF |

| Axe | Servo | Couple requis (N·m) | Marge (continu ÷ requis) | Note |
| --- | --- | ---: | ---: | --- |
| neck_yaw | sts3215_c018 | 0,000 | — | aucun couple statique (lacet) |
| neck_pitch | sts3215_c018 | 0,035 | 28,18 | statique |

Variante IA « locale » : + Raspberry Pi AI HAT+ 2 (167 CHF HT). Variante « réseau » : rien de plus sur le robot (le modèle tourne ailleurs).

## Étape 3 : buste à bras

la tête sur un buste, deux bras de trois axes (variante : un bras SO-101).

Alimentation : secteur 12 V. Outillage (celui du Kit seulement) : cutter, feuille, imprimante, cartons, règle, équerre, pistolet à colle ; et un tournevis ou une clé pour les vis M2 à M4 : HORS de la liste du 2026-10-09 (« cutter, feuille, imprimante, cartons, agrafeuse, règle, équerre, pistolet à colle »), à confirmer par Jeremy.

| Composant | Nombre | Classe | Fixation | Prix unitaire (CHF HT) | Source |
| --- | ---: | --- | --- | ---: | --- |
| sts3215_c018 | 8 | DURABLE | vis | 21,07 | actionneurs.yaml |
| bride métallique pour STS3215 (place de marché, sans marque reconnue) | 8 | DURABLE | vis | 24,09 | kit_parcours_marche.yaml |
| Raspberry Pi Camera Module 3 (standard) | 1 | DURABLE | vis | 29,90 | capteurs.yaml (Bastelgarage.ch) |
| Raspberry Pi 5 8GB | 1 | DURABLE | vis | 146,07 | calculateurs.yaml |
| D42V55F5 (5V, 6A Step-Down Voltage Regulator) | 1 | DURABLE | vis | 33,65 | puissance.yaml |
| Bus Servo Adapter (A) (SKU 25514) | 1 | DURABLE | vis | 4,17 | bus.yaml |
| microphone USB | 1 | DURABLE | clip | — | aucun marché relevé |
| haut-parleur et amplificateur | 1 | DURABLE | vis | — | aucun marché relevé |
| Alimentation à découpage 12 V 30 A 360 W S-360-12 (30 A) | 1 | DURABLE | connecteur | 43,90 | kit_marche.yaml ; sur la table, hors du robot ; AUCUN bloc FERMÉ relevé ne tient ce courant : bornier 230 V à raccorder soi-même ; dispo : Ausverkauft (épuisé le 2026-10-08) |
| vis M2 et M3 | 1 | DURABLE | vis | — | aucun marché relevé |
| carton (buste) | 1 | STRUCTURE | colle | 0,00 | carton de récupération : 0 CHF |

| Axe | Servo | Couple requis (N·m) | Marge (continu ÷ requis) | Note |
| --- | --- | ---: | ---: | --- |
| neck_yaw | sts3215_c018 | 0,000 | — | aucun couple statique (lacet) |
| neck_pitch | sts3215_c018 | 0,035 | 28,18 | statique |
| shoulder_pitch | sts3215_c018 | 0,073 | 13,40 | statique |
| shoulder_roll | sts3215_c018 | 0,073 | 13,40 | statique |
| elbow_roll | sts3215_c018 | 0,018 | 53,78 | statique |

Variante bras : SO-101 (SO-ARM100 / SO-101) (102 CHF HT, kit_parcours_marche.yaml).

## Étape 4 : base à roues

le buste sur une base à deux roues motrices (STS3215 en rotation continue), batterie, manette.

Alimentation : batterie de moins de 100 Wh (3S1P de la cellule du Lab) ; variante batterie d'outillage. Outillage (celui du Kit seulement) : cutter, feuille, imprimante, cartons, règle, équerre, pistolet à colle ; et un tournevis ou une clé pour les vis M2 à M4 : HORS de la liste du 2026-10-09 (« cutter, feuille, imprimante, cartons, agrafeuse, règle, équerre, pistolet à colle »), à confirmer par Jeremy.

| Composant | Nombre | Classe | Fixation | Prix unitaire (CHF HT) | Source |
| --- | ---: | --- | --- | ---: | --- |
| sts3215_c018 | 10 | DURABLE | vis | 21,07 | actionneurs.yaml |
| bride métallique pour STS3215 (place de marché, sans marque reconnue) | 10 | DURABLE | vis | 24,09 | kit_parcours_marche.yaml |
| Raspberry Pi Camera Module 3 (standard) | 1 | DURABLE | vis | 29,90 | capteurs.yaml (Bastelgarage.ch) |
| Raspberry Pi 5 8GB | 1 | DURABLE | vis | 146,07 | calculateurs.yaml |
| D42V55F5 (5V, 6A Step-Down Voltage Regulator) | 1 | DURABLE | vis | 33,65 | puissance.yaml |
| Bus Servo Adapter (A) (SKU 25514) | 1 | DURABLE | vis | 4,17 | bus.yaml |
| microphone USB | 1 | DURABLE | clip | — | aucun marché relevé |
| haut-parleur et amplificateur | 1 | DURABLE | vis | — | aucun marché relevé |
| INR-21700-P50B | 3 | DURABLE | clip | 8,44 | batteries.yaml (cellule du Lab) |
| BMS 3S | 1 | DURABLE | vis | — | aucun marché relevé |
| roues motrices et roue folle | 3 | DURABLE | vis | — | aucun marché relevé |
| roulements | 2 | DURABLE | insert | — | aucun marché relevé |
| manette sans fil | 1 | DURABLE | connecteur | — | aucun marché relevé |
| vis M2 et M3 | 1 | DURABLE | vis | — | aucun marché relevé |
| carton (base) | 1 | STRUCTURE | colle | 0,00 | carton de récupération : 0 CHF |

| Axe | Servo | Couple requis (N·m) | Marge (continu ÷ requis) | Note |
| --- | --- | ---: | ---: | --- |
| neck_yaw | sts3215_c018 | 0,000 | — | aucun couple statique (lacet) |
| neck_pitch | sts3215_c018 | 0,035 | 28,18 | statique |
| shoulder_pitch | sts3215_c018 | 0,073 | 13,40 | statique |
| shoulder_roll | sts3215_c018 | 0,073 | 13,40 | statique |
| elbow_roll | sts3215_c018 | 0,018 | 53,78 | statique |
| roue | sts3215_c018 | — | — | INCONNU : rayon de roue et résistance au roulement absents du dépôt |

Variante batterie d'outillage : Makita BL1850B 18 V 5,0 Ah LXT (197280-8), 90 Wh, 62 CHF HT ; sa tension (18 V) dépasse la plage du STS3215 (14 V) : un convertisseur 12 V en plus.

## Étape 5 : jambes

le robot entier qui tient debout (le niveau « debout » de l'étude du 8 octobre) ; les servos des roues deviennent des servos de jambe.

Alimentation : batterie de moins de 100 Wh (3S1P de la cellule du Lab). Outillage (celui du Kit seulement) : cutter, feuille, imprimante, cartons, règle, équerre, pistolet à colle ; et un tournevis ou une clé pour les vis M2 à M4 : HORS de la liste du 2026-10-09 (« cutter, feuille, imprimante, cartons, agrafeuse, règle, équerre, pistolet à colle »), à confirmer par Jeremy.

| Composant | Nombre | Classe | Fixation | Prix unitaire (CHF HT) | Source |
| --- | ---: | --- | --- | ---: | --- |
| sts3215_c018 | 17 | DURABLE | vis | 21,07 | actionneurs.yaml |
| sts3250 | 2 | DURABLE | vis | — | actionneurs.yaml |
| bride métallique pour STS3215 (place de marché, sans marque reconnue) | 19 | DURABLE | vis | 24,09 | kit_parcours_marche.yaml |
| Raspberry Pi Camera Module 3 (standard) | 1 | DURABLE | vis | 29,90 | capteurs.yaml (Bastelgarage.ch) |
| Raspberry Pi 5 8GB | 1 | DURABLE | vis | 146,07 | calculateurs.yaml |
| D42V55F5 (5V, 6A Step-Down Voltage Regulator) | 1 | DURABLE | vis | 33,65 | puissance.yaml |
| Bus Servo Adapter (A) (SKU 25514) | 1 | DURABLE | vis | 4,17 | bus.yaml |
| microphone USB | 1 | DURABLE | clip | — | aucun marché relevé |
| haut-parleur et amplificateur | 1 | DURABLE | vis | — | aucun marché relevé |
| INR-21700-P50B | 3 | DURABLE | clip | 8,44 | batteries.yaml (cellule du Lab) |
| BMS 3S | 1 | DURABLE | vis | — | aucun marché relevé |
| vis M2, M3 et M4 | 1 | DURABLE | vis | — | aucun marché relevé |
| carton (niveau0) | 1 | STRUCTURE | tenon | 0,00 | carton de récupération : 0 CHF |

| Axe | Servo | Couple requis (N·m) | Marge (continu ÷ requis) | Note |
| --- | --- | ---: | ---: | --- |
| knee | sts3215_c018 | 0,383 | 2,56 | debout, robot de 3,05 kg |
| hip_pitch | sts3215_c018 | 0,383 | 2,56 | debout, robot de 3,05 kg |
| ankle_pitch | sts3250 | 0,745 | 2,10 | debout, robot de 3,05 kg |

## Règle de réemploi

Tout durable se fixe de façon démontable (vis, écrou, insert, clip, connecteur) ; colle et agrafes seulement entre deux pièces de structure. **Respectée** sur toutes les étapes (test).

## Vérifié sur des sources (relevé du 2026-10-11, `params/kit_parcours_marche.yaml`)

- **Rotation continue du STS3215** : existe : mode 1 « Constant speed » (WheelMode), registre Operating_Mode adresse 33, valeur 1, consigne de vitesse adresse 46 ; vitesse maximale propre au mode 1 NON publiée (null) ; lecture de la position en mode 1 : une source tierce seulement (à vérifier au banc)
- **Brides métalliques du commerce** : aucune bride de marque reconnue (Feetech, Waveshare, Hiwonder, Seeed) ; 4 offres de places de marché US, SANS cotes ni motif de trous ; prix retenu (le plus haut lu pour une bride seule, fiche 0064) : 28,86 USD (AliExpress) ; RCmall 19,99 USD les 2 (aluminium ou plastique : contradiction) ; 90,86 USD écarté (aberrant) ; disponibilité CH/UE inconnue
- **Projets ouverts** : SO-101 (TheRobotStudio) : Apache-2.0 (LICENSE lu) ; 12 STS3215 la paire meneur + suiveur (C001, C044, C046) ; 229,88 USD la paire, 121,94 USD le suiveur seul, hors impression 3D ; bras fixe; LeKiwi : Apache-2.0 (LICENSE lu) ; 3 STS3215 aux roues (mode rotation continue) + 12 pour les bras ; 482 USD publiés ; roulage NON vérifié; Reachy Mini (Pollen Robotics) : logiciel Apache-2.0, MATÉRIEL « CC BY-SA-NC » selon le README (non commercial) ; 9 Dynamixel ; 399 / 499 USD; Open Duck Mini (apirrone) : Apache-2.0 (LICENSE lu) ; 14 STS3215 ; 398 EUR publiés ; marche NON vérifiée (vidéos non visionnées)
- **IA locale sur Raspberry Pi 5** : LLM sur Pi 5 8 GB (Geerling) : Qwen2.5 1.5B 11,41 jetons/s (CPU) contre 6,86 (AI HAT+ 2) ; Llama 3.2 3B 5,55 contre 2,66 ; premier jeton 2039 ms (CPU) contre 320 ms (HAT, source Raspberry Pi) ; quantification inconnue sauf Q4_K_M (Stratosphere). Voix : whisper.cpp encode 30 s d'audio en 1,1 s (tiny), 2,5 s (base), 8,3 s (small), mesure de 2023 ; Vosk, Whisper sur Hailo-10H : null

## Interfaces communes à fixer plus tard (rien n'est décidé)

| Interface | Options compatibles avec le STS3215 et ses brides |
| --- | --- |
| motif de trous | boîtier STS3215 : trous autotaraudeurs « B-PA2.0 » (dessus) et « PA3.0X5 » (dessous), non cotés par Feetech (hardware.yaml, servos) ; le motif des brides relevées (kit_parcours_marche.yaml) ; un pas de grille à choisir (par exemple celui des brides, pour que structure, brides et Lab partagent les mêmes trous) |
| famille de vis | M2 (autotaraudeuses du boîtier), M3 (palonnier : « M3×6 » sur le plan Feetech), M4 (pivots du niveau 0) ; ISO métriques, peu de références (vision-produit, PROPOSÉ) |
| câble de servo | connecteur « 5264 / 2,54 mm, 3 broches » (plan Feetech : GND, V, signal), chaînable d'un servo à l'autre ; longueurs à choisir |
| connecteur d'alimentation | prise DIN 4 broches des blocs Mean Well GST (kit_marche.yaml) ; jack 5,5 × 2,5 du bloc 12 V 10 A ; XT30 ou XT60 (usage courant, non relevé au dépôt) côté batterie |
| rail de tension | 12 V : STS3215-C018 (4 à 14 V) et STS3250 (6 à 12 V) ; 7,4 V : STS3215-C001 ; pack 3S (9 à 12,6 V à la coupure de 3,0 V) dans la plage du C018, PAS dans celle du STS3250 à pleine charge (12,6 > 12 V) |
| bus | série TTL demi-duplex (une ligne signal), 1 Mbit/s par défaut (actionneurs.yaml) ; adaptateur USB (bus.yaml) |
| protocole | protocole série Feetech (STS/SCS, identifiants 0 à 253) ; bibliothèques SCServo / STservo ; tables de LeRobot (source secondaire, actionneurs.yaml) |
