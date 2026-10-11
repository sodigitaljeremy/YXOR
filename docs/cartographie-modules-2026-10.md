# Cartographie des achats de la gamme par modules (2026-10)

**Engendré** par `.venv/bin/python scripts/cartographie_modules.py --ecrire`. Décidé (fiche 0077, Jeremy) : réemploi maximal, même entre catégories ; une seule batterie pour tous les modèles du Kit et du Lab ; (fiche 0078) quatre catégories, Kit → Initiation, Lab → Intermédiaire, Home → Avancé, Pro → Professionnelle. **Tout le reste est PROPOSÉ.** Méthode : en tête du script.

## Matrice des modules par modèle (option préconisée)

| Modèle | Catégorie | petits axes | locomotion | énergie | cerveau | IA | capteurs | bus | visserie et connectique | structure |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kit 1 (tête de bureau) | Initiation | 2 × sts3215_c018 | — | Mean Well LRS-150F-12, alimentation à découpage « enclosed » (12.5 A) | — | — | caméra USB (décidé par Jeremy, fiche 0077 : « Ok pour une caméra USB ») | Bus Servo Adapter (A) (SKU 25514) | 2 × bride métallique pour STS3215 (place de marché, sans marque reconnue), vis M2 et M3 (brides, palonniers) | carton (tete) |
| Kit 2 (tête qui parle) | Initiation | 2 × sts3215_c018 | — | D42V55F5 (5V, 6A Step-Down Voltage Regulator), Mean Well LRS-150F-12, alimentation à découpage « enclosed » (12.5 A) | Raspberry Pi 5 8GB | — | Raspberry Pi Camera Module 3 (standard), haut-parleur et amplificateur, microphone USB | Bus Servo Adapter (A) (SKU 25514) | 2 × bride métallique pour STS3215 (place de marché, sans marque reconnue), vis M2 et M3 | carton (tete) |
| Kit 3 (buste à bras) | Initiation | 8 × sts3215_c018 | — | Alimentation à découpage 12 V 30 A 360 W S-360-12 (30 A), D42V55F5 (5V, 6A Step-Down Voltage Regulator) | Raspberry Pi 5 8GB | — | Raspberry Pi Camera Module 3 (standard), haut-parleur et amplificateur, microphone USB | Bus Servo Adapter (A) (SKU 25514) | 8 × bride métallique pour STS3215 (place de marché, sans marque reconnue), vis M2 et M3 | carton (buste) |
| Kit 4 (base à roues) | Initiation | — | 10 × sts3215_c018, 2 × roulements, 3 × roues motrices et roue folle | 3 × INR-21700-P50B, BMS 3S, D42V55F5 (5V, 6A Step-Down Voltage Regulator) | Raspberry Pi 5 8GB | — | Raspberry Pi Camera Module 3 (standard), haut-parleur et amplificateur, microphone USB | Bus Servo Adapter (A) (SKU 25514), manette sans fil | 10 × bride métallique pour STS3215 (place de marché, sans marque reconnue), vis M2 et M3 | carton (base) |
| Kit 5 (jambes) | Initiation | 8 × sts3215_c018 | 2 × sts3250, 9 × sts3215_c018 | 3 × INR-21700-P50B, BMS 3S, D42V55F5 (5V, 6A Step-Down Voltage Regulator) | Raspberry Pi 5 8GB | — | Raspberry Pi Camera Module 3 (standard), haut-parleur et amplificateur, microphone USB | Bus Servo Adapter (A) (SKU 25514) | 19 × bride métallique pour STS3215 (place de marché, sans marque reconnue), vis M2, M3 et M4 | carton (niveau0) |
| Lab roulant (PROPOSÉ) | Intermédiaire | — | 10 × sts3215_c018, 2 × roulements, 3 × roues motrices et roue folle | 3 × INR-21700-P50B, BMS 3S, D42V55F5 (5V, 6A Step-Down Voltage Regulator) | Raspberry Pi 5 8GB | — | Raspberry Pi Camera Module 3 (standard), haut-parleur et amplificateur, microphone USB | Bus Servo Adapter (A) (SKU 25514), manette sans fil | 10 × bride métallique pour STS3215 (place de marché, sans marque reconnue), vis M2 et M3 | plaques d'aluminium 2 mm (prix de l'opérateur CN non relevé) |
| Lab bipède A | Intermédiaire | 2 × sts3215_c018, sts3215_c018 | 2 × sts3250 | 3 × INR-21700-P42A (pack 3S1P), D42V110F6 (6V, 11A Step-Down Voltage Regulator), GIGAVAC P115BDA MiniTACTOR (scellé herm | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | — | caméra (non comptée par l'explorateur) | Bus Servo Adapter (A) (SKU 25514), PCAN-USB (IPEH-002021) / PCAN-USB opto-decoupled (IPEH-002022) | visserie, connectique | carton (A ne tient qu'en carton ; en aluminium 2 mm, non) |
| Home candidat | Avancé | 2 × rs00, 2 × rs05, 2 × sts3215_c001, rs05, scs0009_c013, sts3250 | 2 × rs00, 2 × rs03, 2 × rs04, 2 × rs06, 2 × rs10p | 24 × INR-21700-P50B (pack 12S2P), D42V110F12 (12V, 9A Step-Down Voltage Regulator), D42V110F6 (6V, 11A Step-Down Voltage | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | — | caméra (non comptée par l'explorateur) | Bus Servo Adapter (A) (SKU 25514), PCAN-USB (IPEH-002021) / PCAN-USB opto-decoupled (IPEH-002022) | visserie, connectique | plaques d'aluminium (Home : 3D, fiche 0076) |

**Écarts à l'objectif de réemploi (calculés)** :
- cellules des modèles du Kit et du Lab : Kit 4 (base à roues) : molicel_p50b ; Kit 5 (jambes) : molicel_p50b ; Lab roulant (PROPOSÉ) : molicel_p50b ; Lab bipède A : molicel_p42a → **plusieurs cellules** : l'explorateur choisit pour le Lab bipède A la cellule la plus légère qui suffit, pas celle du Kit ; la batterie unique demande d'imposer la même (le Lab A tient avec le pack 3S1P du Kit, tableau plus bas, à la marge 1,0).
- calculateur : Kit 2 (tête qui parle) : Raspberry Pi 5 8GB ; Kit 3 (buste à bras) : Raspberry Pi 5 8GB ; Kit 4 (base à roues) : Raspberry Pi 5 8GB ; Kit 5 (jambes) : Raspberry Pi 5 8GB ; Lab roulant (PROPOSÉ) : Raspberry Pi 5 8GB ; Lab bipède A : seeed_recomputer_mini_j3011 ; Home candidat : seeed_recomputer_mini_j3011 → le Lab bipède A et le Home prennent un Jetson (choix de l'explorateur : le moins cher qui est vérifiable) ; le Pi 5 du Kit n'y est pas réemployé, sauf comme contrôleur du corps (hypothèse plus bas).

## Coûts et réemploi, en parcourant Kit → Lab → Home

| Modèle | Durables (CHF HT, borne basse) | Déjà payé par un modèle précédent | Réemploi | Entre catégories | Achat neuf | Investissement cumulé | Durables sans prix |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Kit 1 (tête de bureau) | 120 | 0 | 0 % | 0 | 120 | 120 | 2 |
| Kit 2 (tête qui parle) | 329 | 120 | 36 % | 0 | 210 | 329 | 3 |
| Kit 3 (buste à bras) | 619 | 304 | 49 % | 0 | 315 | 644 | 3 |
| Kit 4 (base à roues) | 691 | 575 | 83 % | 0 | 116 | 760 | 7 |
| Kit 5 (jambes) | 1 055 | 838 | 79 % | 0 | 217 | 977 | 5 |
| Lab roulant (PROPOSÉ) | 691 | 691 | 100 % | 691 | 0 | 977 | 7 |
| Lab bipède A | 1 904 | 320 | 17 % | 320 | 1 584 | 2 560 | 8 |
| Home candidat | 4 514 | 937 | 21 % | 937 | 3 577 | 6 137 | 6 |

« Entre catégories » : la part déjà payée dont le produit a été acheté dans une AUTRE catégorie (catégories de la fiche 0078). Le Lab bipède A ne tient qu'en carton à la marge 1,0 (lab-leger) : la nomenclature est la sienne.

## Module énergie : la batterie unique du Kit et du Lab (sous 100 Wh)

| Option | Produit | Énergie (Wh) | Masse (g) | Courant max (A) | Coût (CHF) | Suisse | Outillage | Sécurité |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| a) outillage 18 V | Makita BL1820B | 36 | 500 | — | 75 | offres CH sur Toppreise (2 offres lues) | tournevis ; adaptateur à bornes, convertisseur 12 V, coupure basse | coupure basse dans : outil (sur signal de la batterie) ; surintensité dans : outil (sur si |
| a) outillage 18 V | Makita BL1850B | 90 | 654 | — | 66 | 20 offres CH (Toppreise, 2026-10-11) | tournevis ; adaptateur à bornes, convertisseur 12 V, coupure basse | coupure basse dans : outil (sur signal de la batterie) ; surintensité dans : outil (sur si |
| a) outillage 18 V | DeWalt DCB183 | — | 350 | — | 42 | 12 offres CH (Toppreise) | tournevis ; adaptateur à bornes, convertisseur 12 V, coupure basse | coupure basse dans : outil ; surintensité dans : outil |
| a) outillage 18 V | DeWalt DCB184 | — | 620 | — | 133 | Distrelec.ch en stock ; 47 offres Toppreise | tournevis ; adaptateur à bornes, convertisseur 12 V, coupure basse | coupure basse dans : outil ; surintensité dans : outil |
| a) outillage 18 V | Bosch Professional GBA 18V 2.0Ah | — | 350 | — | 72 | 31 offres CH (Toppreise) | tournevis ; adaptateur à bornes, convertisseur 12 V, coupure basse | coupure basse dans : non lu ; surintensité dans : non lu |
| a) outillage 18 V | Bosch Professional GBA 18V 5.0Ah | — | 620 | — | 104 | 32 offres CH (Toppreise) | tournevis ; adaptateur à bornes, convertisseur 12 V, coupure basse | coupure basse dans : non lu ; surintensité dans : non lu |
| a) outillage 18 V | Bosch Professional ProCORE18V 4.0Ah | — | 515 | — | 116 | 28 offres CH (Toppreise) | tournevis ; adaptateur à bornes, convertisseur 12 V, coupure basse | coupure basse dans : non lu ; surintensité dans : non lu |
| a) outillage 18 V | Bosch Professional ProCORE18V 5.5Ah | — | — | — | — | — | tournevis ; adaptateur à bornes, convertisseur 12 V, coupure basse | coupure basse dans : non lu ; surintensité dans : non lu |
| b) pack maison 3S1P | 3S1P INR-21700-P50B | 52 | 277 | 24 | 25 | akkuteile.de (DE) : en stock le 2026-10-07 | soudure par points ou porte-cellules ; BMS ; chargeur 3S/4S (HORS de l'outillage du Kit si soudé) | BMS obligatoire ; cellules neuves seulement |
| b) pack maison 4S1P | 4S1P INR-21700-P50B | 70 | 369 | 24 | 34 | akkuteile.de (DE) : en stock le 2026-10-07 | soudure par points ou porte-cellules ; BMS ; chargeur 3S/4S (HORS de l'outillage du Kit si soudé) | BMS obligatoire ; cellules neuves seulement |
| c) USB-C (bureau) | Club 3D CAC-1914 (140 W, 1x USB-C, PD 3.1) | — | 333 | 3 | 89 | Toppreise (7 lignes) | aucun | secteur ; aucune batterie |
| c) USB-C (bureau) | Club 3D CAC-1932 (140 W PD 3.1) | — | — | — | 50 | Toppreise (14 lignes) | aucun | secteur ; aucune batterie |
| c) USB-C (bureau) | Hama 00200019 (GaN, 3 ports, PD, 5-28 V / 140 W) | — | — | — | 38 | Toppreise | aucun | secteur ; aucune batterie |
| c) USB-C (bureau) | Anker Nano Charger 100W (A2679 / B2679 avec câble) | — | — | — | 61 | Toppreise | aucun | secteur ; aucune batterie |

Repères de courant : **23,7 A** au pire à l'étape 3 du Kit (8 servos au blocage + Pi 5) ; pointe du Lab bipède A **13,2 A** (puissance de pointe de l'explorateur ÷ tension de coupure du pack 3S).

- **Courant des batteries d'outillage** : publié par aucune des huit (null) ; il ne peut donc être comparé ni aux 23,7 A ni à la pointe du Lab.
- **Où est la protection de décharge** : DeWalt : coupure dans outil, surintensité dans outil ; Makita : coupure dans outil (sur signal de la batterie), surintensité dans outil (sur signal de la batterie) ; Bosch Professional : coupure dans non lu, surintensité dans non lu. Une protection dans l'OUTIL laisse la batterie sans coupure une fois branchée au robot : il faut alors une coupure en tension basse côté robot.
- **Adaptateurs bornes vers fils** : PartsBuilt adaptateur Makita 18V avec coupure basse (« blinker board ») (3,5 A); PartsBuilt adaptateur « MilWalt » (Milwaukee et DeWalt) avec coupure basse (3,5 A); PartsBuilt « Blinker Board » 3.5 A (v8), module de coupure basse seul (3,5 A); XH-M609 module de protection de décharge 12-36 V (relais) (10,0 A).
- **Convertisseurs 12 V de 25 A ou plus** : Mean Well SD-500L-12 (19-72 V → 12 V, 40 A, 198 CHF, 14-21 V : non); Mean Well SD-1000L-12 (19-72 V → 12 V, 60 A, 354 CHF, 14-21 V : non); Mean Well SD-350B-12 (20-36 V → 12 V, 27.5 A, 119 CHF, 14-21 V : non); Mean Well DDR-480B-12 (16.8-33.6 (14.4-16.8 pendant 100 ms) V → 12 V, 33.4 A, 216 CHF, 14-21 V : non); Mean Well DDR-480C-12 (33.6-67.2 (28.8-33.6 pendant 100 ms) V → 12 V, 33.4 A, 215 CHF, 14-21 V : non); Mean Well RSD-500B-12 (16.8-33.6 V → 12 V, 35 A, 247 CHF, 14-21 V : non); Mean Well RSD-500C-12 (33.6-67.2 V → 12 V, 35 A, 253 CHF, 14-21 V : non); Victron Energy Orion 24/12-40 (ORI241240021, non isolé) (18-35 V → 12 V, 40 A, 89 CHF, 14-21 V : non). **Aucun ne couvre 14 à 21 V en entrée** (une batterie 18 V) : pour la batterie d'outillage, le convertisseur de 25 A reste null.
- **USB-C** : à 12 V, un chargeur de 140 W ne donne que 3 A (Club 3D CAC-1914) et un chargeur de 100 W lu n'a pas de niveau 12 V : en dessous du pire cas de la tête de bureau (5,4 A, servos au blocage) ; suffisant seulement si le courant réel reste sous 3 A (à mesurer) ; pas pour le buste (23,7 A).

### Le Lab bipède A, repassé avec chaque batterie (pack choisi par l'explorateur : 273 g, robot 3,59 kg)

Masse de la batterie seule : l'adaptateur, le convertisseur 12 V et la coupure basse d'une batterie d'outillage ne sont pas comptés (masses non relevées).

| Batterie | Masse (g) | Robot (kg) | Marge 1,5 | Marge 1,0 |
| --- | ---: | ---: | --- | --- |
| Makita BL1820B | 500 | 3,82 | ne tient pas (hip_roll, ankle_pitch) | tient |
| Makita BL1850B | 654 | 3,98 | ne tient pas (hip_roll, ankle_pitch) | tient |
| DeWalt DCB183 | 350 | 3,67 | ne tient pas (hip_roll, ankle_pitch) | tient |
| DeWalt DCB184 | 620 | 3,94 | ne tient pas (hip_roll, ankle_pitch) | tient |
| Bosch Professional GBA 18V 2.0Ah | 350 | 3,67 | ne tient pas (hip_roll, ankle_pitch) | tient |
| Bosch Professional GBA 18V 5.0Ah | 620 | 3,94 | ne tient pas (hip_roll, ankle_pitch) | tient |
| Bosch Professional ProCORE18V 4.0Ah | 515 | 3,84 | ne tient pas (hip_roll, ankle_pitch) | tient |
| 3S1P INR-21700-P50B | 277 | 3,60 | ne tient pas (hip_roll, ankle_pitch) | tient |
| 4S1P INR-21700-P50B | 369 | 3,69 | ne tient pas (hip_roll, ankle_pitch) | tient |

## Hypothèses entre catégories (chiffrées, NON adoptées)

### Le Home en 36 V (deux batteries 18 V en série) plutôt qu'en 12S

- **12S** : coupure 36 V, vitesse des RobStride × 0,750 de leur vitesse à 48 V ; plus petite H qui ne soit pas infaisable : 0,85 m (0,850 m réels), 18,5 kg, ≥ 4 514 CHF, INCONNU.
- **10S** : coupure 30 V, vitesse des RobStride × 0,625 de leur vitesse à 48 V ; **aucune H de 0,65 à 0,90 m ne tient** (ankle_pitch : aucun robstride ne tient; knee : aucun robstride ne tient).

Ce que cela changerait par rapport à la fiche 0072 (12S décidé par Jeremy pour le Lab et le Pro) : le pack, le BMS, la coupure et la plage des RobStride (24 à 60 V, tenue en 10S) ; la vitesse à la coupure baisse de 17 % ; à H = 0,85 m le genou ne la tient plus.

### Le Raspberry Pi 5 gardé dans le Home (contrôleur du corps), à côté d'un Jetson pour l'IA

Coût ajouté : Raspberry Pi 5 8 GB 146 CHF (déjà payé si il vient du Kit) + 2-CH CAN FD HAT 39 CHF pour le CAN. Masse et consommation du Pi 5 : non publiées (calculateurs.yaml). Le Jetson garde l'IA ; le Pi 5 porte la boucle des actionneurs (non calculé ici).

### L'IA par le réseau, sur l'ordinateur de l'utilisateur

| Modèle | Matériel | Débit (jetons/s) | Premier jeton (ms) | Source |
| --- | --- | ---: | ---: | --- |
| llama3.2:3b | Pi 5 8 GB, CPU (ollama) | 5,55 | — | Jeff Geerling |
| deepseek-r1-distill-qwen:1.5b | Pi 5 8 GB, CPU (ollama) | 10,99 | — | Jeff Geerling |
| qwen2.5-coder:1.5b | Pi 5 8 GB, CPU (ollama) | 9,77 | — | Jeff Geerling |
| qwen2.5-instruct:1.5b | Pi 5 8 GB, CPU (ollama) | 11,41 | — | Jeff Geerling |
| qwen2:1.5b | Pi 5 8 GB, CPU (ollama) | 12,47 | — | Jeff Geerling |
| qwen2.5:3b | Pi 5 (RAM non précisée), CPU (ollama) | 5,20 | — | Stratosphere Lab (CTU), Slips docs |
| llama3.2:1b-instruct | Pi 5 (RAM non précisée), CPU (ollama) | 11,22 | — | Stratosphere Lab (CTU) |
| llama3.2:3b | Pi 5 (RAM non précisée), CPU (ollama) | 4,69 | — | Stratosphere Lab (CTU) |
| qwen2.5:1.5b | Pi 5 (RAM non précisée), CPU (ollama) | 9,97 | — | Stratosphere Lab (CTU) |
| gemma3:1b | Pi 5 (RAM non précisée), CPU (ollama) | 11,53 | — | Stratosphere Lab (CTU) |
| smollm2:1.7b-instruct | Pi 5 (RAM non précisée), CPU (ollama) | 8,23 | — | Stratosphere Lab (CTU) |
| deepseek-r1:1.5b | CM5 devkit 4 GB (BCM2712, même SoC que Pi 5), CPU, ollama 0.14.2 | 9,04 | — | CNX Software |
| llama3.2:3b | Pi 5 8 GB + AI HAT+ 2 | 2,66 | — | Jeff Geerling |
| deepseek-r1-distill-qwen:1.5b | Pi 5 8 GB + AI HAT+ 2 | 6,85 | — | Jeff Geerling |
| qwen2.5-coder:1.5b | Pi 5 8 GB + AI HAT+ 2 | 8,13 | — | Jeff Geerling |
| qwen2.5-instruct:1.5b | Pi 5 8 GB + AI HAT+ 2 | 6,86 | — | Jeff Geerling |
| qwen2:1.5b | Pi 5 8 GB + AI HAT+ 2 | 8,25 | — | Jeff Geerling |
| deepseek_r1_distill_qwen:1.5b | Pi 5 2 GB + AI HAT+ 2 (hailo-ollama) | 6,72 | — | CNX Software |
| llama3.2:3b | Pi 5 2 GB + AI HAT+ 2 | 2,61 | — | CNX Software |
| qwen2.5-instruct:1.5b | Pi 5 2 GB + AI HAT+ 2 | 6,74 | — | CNX Software |
| qwen2.5-coder:1.5b | Pi 5 2 GB + AI HAT+ 2 | 8,06 | — | CNX Software |
| qwen2:1.5b | Pi 5 2 GB + AI HAT+ 2 | 5,90 | — | CNX Software |
| Llama 3.1 8B Instruct | NVIDIA GeForce RTX 3060 12 GB | 51,30 | 882 | LocalScore |
| Llama 3.1 8B Instruct | NVIDIA GeForce RTX 3060 8 GB | 37,00 | 1 010 | LocalScore |
| Llama 3.1 8B Instruct | NVIDIA GeForce RTX 4060 8 GB | 38,30 | 1 040 | LocalScore |
| Llama 3.1 8B Instruct | NVIDIA GeForce RTX 4060 Ti 16 GB | 48,30 | 619 | LocalScore |
| Llama 3.1 8B Instruct | Apple M1 (4P+4E+8GPU) 8 GB | 14,60 | 9 640 | LocalScore |
| Llama 3.1 8B Instruct | Apple M2 (4P+4E+10GPU) 8 GB | 19,40 | 7 890 | LocalScore |
| Llama 3.1 8B Instruct | Apple M3 (4P+4E+10GPU) 16 GB | 13,50 | 9 020 | LocalScore |
| Llama 3.2 1B Instruct | NVIDIA GeForce RTX 3060 12 GB | 185,00 | 232 | LocalScore |
| Llama 3.2 1B Instruct | NVIDIA GeForce RTX 4060 8 GB | 134,00 | 380 | LocalScore |
| Llama 3.2 1B Instruct | Apple M1 (4P+4E+8GPU) 8 GB | 37,90 | 2 420 | LocalScore |
| Llama 3.2 1B Instruct | Apple M2 (4P+4E+10GPU) 8 GB | 58,70 | 1 600 | LocalScore |
| Llama 3.2 1B Instruct | Apple M3 (4P+4E+10GPU) 16 GB | 67,10 | 1 410 | LocalScore |
| Llama 3.1 8B | Jetson Orin Nano 8GB, mode Super (JetPack 6.2) | 19,10 | — | MLC |
| Llama 3.2 3B | Jetson Orin Nano 8GB, mode Super (JetPack 6.2) | 43,07 | — | MLC |
| Qwen2.5 7B | Jetson Orin Nano 8GB, mode Super (JetPack 6.2) | 21,75 | — | MLC |

Coût sur le robot : réseau 0 CHF (l'ordinateur existe) ; Pi 5 seul 146 CHF ; Pi 5 + AI HAT+ 2 313 CHF ; Jetson Orin Nano Super (kit) 333 CHF. Le délai par le réseau ajoute l'aller-retour Wi-Fi : médiane d'environ 3 ms, 90e centile d'environ 20 ms, mesurés sur un réseau de campus (WiFiSeer, 2016, energie_marche.yaml) ; aucune mesure en réseau domestique relevée. Sur un ordinateur avec une carte graphique grand public, un modèle de 8 milliards de paramètres répond 3 à 10 fois plus vite que sur le Pi 5 (un modèle 2 à 5 fois plus petit) ; un Mac M1 à M3 de 8 à 16 GB attend 8 à 10 s avant le premier jeton sur ce modèle de 8 milliards (LocalScore).

## Le Lab bipède A aligné sur le Kit (prompt du 2026-10-11 ; PROPOSÉ)

Imposés : la cellule du Kit (Molicel P50B, pack 3S1P), un Raspberry Pi 5 à la place du Jetson, l'IA par le réseau. Structure : **carton** seulement ; le contreplaqué n'est pas relevé (masse surfacique null), il n'est donc pas évalué. Marche à 0,196 m/s (celle de ToddlerBot ramenée à 0,60 m).

| Marge | Tient ? | H (m) | H réelle (m) | Masse (kg) | Coût de l'explorateur (CHF, borne basse) | Statut | Pack |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| 1,5 | **oui** | 0,65 | 0,650 | 3,23 | 1 476 | INCONNU | 3S1P |
| 1,0 | **oui** | 0,65 | 0,650 | 3,23 | 1 476 | INCONNU | 3S1P |

**Statut INCONNU** : une donnée critique d'un actionneur manque (la vitesse du STS3250 n'est pas publiée) ; « tient » veut dire ici qu'aucune contrainte calculable n'est violée.

**Nomenclature corrigée : 722 CHF de durables** (borne basse, 7 durables sans prix, dont les STS3250), contre le coût de l'explorateur ci-dessus. L'explorateur garde la chaîne de puissance du 12S (BMS Orion Jr 2, anti-étincelle 300 A, contacteur, absorbeur, rail 6 V) et deux cartes CAN ; en 3S direct sur des Feetech à bus série, elles sont sans objet. Retirées ; gardés : les cellules, le 5 V du Pi 5, le fusible et son porte-fusible, l'arrêt d'urgence ; ajouté : le moins cher des BMS 3S relevés qui tient 23,7 A en continu prudent, avec un prix lu (section suivante ; il est en rupture de stock).

⚠ **Tension** : en 3S direct, le pack plein (12,6 V) dépasse la plage publiée des STS3250 (6 à 12 V) que le Lab A porte à la locomotion ; « tient » ci-dessus ne le vérifie pas (section suivante).

**Ce que le profil perd sans Jetson** : le profil `lab` demande « IA embarquée commande + vision » (Jeremy, 2026-10-07). Le Pi 5 seul ne fait à bord que la **commande** ; la vision et le langage passent par le réseau (ordinateur de l'utilisateur) : le robot en dépend, avec l'aller-retour Wi-Fi en plus. La vision locale sur le Pi 5 (ou avec l'AI HAT+ 2) n'est pas relevée. Puissance du Pi 5 comptée : 25 W, borne haute (son alimentation 5 V 5 A) ; sa masse n'est pas publiée.

### Réemploi et investissement cumulé : chaîne initiale et chaîne alignée

| Modèle | Chaîne initiale : réemploi | Investissement cumulé | Chaîne alignée : réemploi | Investissement cumulé |
| --- | ---: | ---: | ---: | ---: |
| Kit 1 (tête de bureau) | 0 % | 120 | 0 % | 120 |
| Kit 2 (tête qui parle) | 36 % | 329 | 36 % | 329 |
| Kit 3 (buste à bras) | 49 % | 644 | 49 % | 644 |
| Kit 4 (base à roues) | 83 % | 760 | 83 % | 760 |
| Kit 5 (jambes) | 79 % | 977 | 79 % | 977 |
| Lab roulant (PROPOSÉ) | 100 % | 977 | 100 % | 977 |
| Lab bipède A → aligné | 17 % | 2 560 | 77 % | 1 145 |
| Home candidat | 21 % | 6 137 | 2 % | 5 578 |

Les deux chaînes : Kit 1 à 5 → Lab roulant → Lab bipède A (initial ou aligné) → Home candidat. Un même produit n'est payé qu'une fois (au plus grand nombre possédé) ; prix manquants comptés 0 (borne basse).

## Batterie unique 3S Li-ion, en direct sur le rail des servos (relevé du 2026-10-11 ; PROPOSÉ)

Relevé : `params/batterie3s_marche.yaml` (46 sources, ids `marche_3s_*`). Pack 3S plein : **12,6 V**. Courants à tenir : **23,7 A** (pire cas de l'étape 3 du Kit) et **13,2 A** (pointe du Lab A).

### Tension maximale des servos

| Servo | Plages publiées (V) | Valeur prudente (V) | Face à un pack plein |
| --- | --- | ---: | --- |
| Feetech STS3215 12 V (ST-3215-C018) | 4 à 14,0 ; 6 à 12,6 | 12,6 | marge nulle |
| Feetech STS3250 12 V (ST-3250-C002) | 6 à 12,0 | 12,0 | **dépassée de 0,6 V** |

Tension absolue maximale : publiée par aucune source (null). Une protection existe (registre « Maximum Input Voltage » de la table mémoire STS, mise hors couple), mais son seuil d'usine n'est pas publié pour les versions 12 V. Les chargeurs 3S relevés annoncent 12,6 ± 0,2 V, soit **jusqu'à 12,8 V** si le robot reste alimenté pendant la charge.

### BMS 3S

| BMS | Zone | Courant continu prudent (A) | ≥ 23,7 A | ≥ 13,2 A | Prix (CHF) | Stock |
| --- | --- | ---: | --- | --- | ---: | --- |
| TRU COMPONENTS TC-13125656 | CH | 20,0 | **non** | oui | 4,40 | 249 Stueck, livraison annoncee jeu. 15 oct. |
| Keeppower XZD-3S1550 (PCB 3S, 4 MOS) | UE (DE), livre en Suisse | — (déclenchement 26 ± 2 A) | — | — | 4,64 | InStock (JSON-LD) |
| BMS module 3S 40A 12.6V (Enhanced), generique | UE (RO) | 20,0 | **non** | oui | — | InStock |
| BMS module 3S 40A with balance, generique | UE (RO) | 20,0 | **non** | oui | — | OutOfStock |
| BMS module 3S 60A with balance, generique | UE (RO) | — | — | — | — | OutOfStock |
| HW-552 3S 40A (notice generique) | hors UE (AU), notice seulement | 40,0 | oui | oui | — | — |
| Daly Li-ion 3S 12V 30A Common Port (materiel) | hors UE (IN) | 30,0 | oui | oui | — | Out of Stock |
| JK Smart Active Balance BMS B2A8S30P (3S-8S) | UE (NL) | 300,0 | oui | oui | 85,25 | Out of stock |

Courant prudent : la moitié de l'annoncé pour la gamme dont le vendeur recommande de ne pas dépasser 50 % en continu ; un seuil de déclenchement (Keeppower, 26 ± 2 A) n'est pas un courant continu. Prix TTC convertis (null si la devise n'a pas de taux au budget).

### Packs 3S déjà assemblés

- Auline 21700 4800 mAh 3S1P 11,1 V XT60 (hors UE (UK)) : cellules 21700 (marque non indiquee) ; BMS : aucun décrit ; courant ~10 A ; — CHF.
- Keeppower 3S1P 18650 3500 mAh 10,8 V avec BMS (UE (DE), livre en Suisse) : cellules 3 x Samsung 18650-35E (18650, PAS 21700) ; BMS : PCB/BMS Seiko 3S, 7 A ; courant 7 A ; 16,97 CHF.
- ANSMANN Li-ion battery pack 10,8 V / 3350 mAh / 3S1P (UE (DE)) : cellules 18650 (« conventional Li 18650 standard cells »), PAS 21700 ; BMS : « electronic protection circuit (BMS) » ; courant 5 A ; 61,60 CHF.

→ **Aucun pack 3S en 21700 avec BMS** relevé en Suisse ni dans l'UE ; ceux qui ont un BMS sont en 18650 et donnent 5 à 7 A, sous 13,2 A.

### Porte-cellules 21700 sans soudure

| Porte-cellules | Zone | Courant par contact (A) | ≥ 23,7 A | ≥ 13,2 A |
| --- | --- | ---: | --- | --- |
| Keystone 1121-1124 (20700/21700 cell holders) | fabricant (US) ; distributeurs Farnell/Mouser/Digikey (pages bloquees) | — | — | — |
| Electrokit Batterihallare 21700 1x clip for PCB | UE (SE) | — | — | — |
| Jiatel 21700 battery holders (gamme) | fabricant (CN), pas de revendeur UE identifie | 10,0 | **non** | **non** |
| Support d'essai 21700 (montage d'essai) | hors UE (US) | 10,0 | **non** | **non** |
| Probots 4x21700 SMD holder (FAQ revendeur) | hors UE (IN) | 5,0 | **non** | **non** |

### Chargeur 3S et bloc 12 V fermé (étapes 1 et 2 : 5,4 et 7,5 A)

- chargeur 12.6V 2A Lithium Batterieladegeraet 5.5/2.1 (Waveshare 29567) (CH, Bastelgarage) : 12,6 ± 0,2 V, 2 A, 17,90 CHF, certification non indiquée, Lagernd.
- chargeur Fuyuang (Enerpower) EP-FY1261000 / 1262000 / 1263000 (UE (DE), livre en Suisse, akkuteile.de) : 12,6 ± 0,2 V, [1, 2, 3] A, 10,33 CHF, certification UL CUL GS BS CE SAA EK PSE (liste du vendeur), InStock (JSON-LD).
- bloc 12V DC 10A Netzteil AC/DC-Adapter (BTF-Lighting) (CH, Bastelgarage) : 10,0 A (5,4 A : oui ; 7,5 A : oui), 35,90 CHF, classe d'isolation non écrite, Ausverkauft.
- bloc MEAN WELL GST120A12-R7B (CH, Conrad.ch) : 8,5 A (5,4 A : oui ; 7,5 A : oui), 43,95 CHF, classe d'isolation non écrite, Bald verfuegbar.
- bloc HN Power HNP120M-120 (CH, Conrad.ch) : 8,0 A (5,4 A : oui ; 7,5 A : oui), 57,95 CHF, classe d'isolation non écrite, 11 Stueck.
- bloc Protek PMP120-12-B1-S (CH, Conrad.ch) : 8,0 A (5,4 A : oui ; 7,5 A : oui), 99,95 CHF, classe d'isolation non écrite, 3 Stueck (solange Vorrat).

### Bilan, comparé aux batteries d'outillage 18 V (lot précédent)

- **Outillage 18 V** : courant non publié, protection dans l'OUTIL (rien ne coupe une fois branchée au robot), aucun convertisseur 14-21 V → 12 V de 25 A ou plus relevé.
- **3S Li-ion en direct** : pas de convertisseur, mais **le pack plein (12,6 V) dépasse la plage publiée du STS3250 (6 à 12 V)** et laisse une marge nulle au STS3215 C018 (valeur prudente 12,6 V) ; ni l'une ni l'autre n'est levée par une source.
- **Sans soudure** : non démontré ; aucun porte-cellules ne publie 13,2 A par contact (10 A au mieux), et aucun pack 21700 assemblé avec BMS n'est relevé en Suisse ou dans l'UE.
- **BMS** : en Suisse, un seul (20 A, sous 23,7 A) ; au-dessus, seulement des BMS en rupture ou hors UE.
- **En Suisse** : chargeur 12,6 V 2 A et blocs 12 V fermés de 8 à 10 A (Bastelgarage, Conrad.ch) disponibles ; Galaxus et Digitec n'ont pas pu être lus (accès bloqué).

