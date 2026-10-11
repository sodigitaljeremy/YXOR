# Cartographie des achats de la gamme par modules (2026-10)

**Engendré** par `.venv/bin/python scripts/cartographie_modules.py --ecrire`. Décidé (fiche 0077, Jeremy) : réemploi maximal, même entre catégories ; une seule batterie pour tous les modèles du Kit et du Lab. **Tout le reste est PROPOSÉ**, dont le rattachement des modèles aux catégories (« Initiation = Kit, Intermédiaire = Lab, Avancé = Home et Pro » : en attente de Jeremy). Méthode : en tête du script.

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
- cellules des modèles du Kit et du Lab : Kit 4 (base à roues) : INR-21700-P50B ; Kit 5 (jambes) : INR-21700-P50B ; Lab roulant (PROPOSÉ) : INR-21700-P50B ; Lab bipède A : molicel_p42a → **plusieurs cellules** : l'explorateur choisit pour le Lab bipède A la cellule la plus légère qui suffit, pas celle du Kit ; la batterie unique demande d'imposer la même (le Lab A tient avec le pack 3S1P du Kit, tableau plus bas, à la marge 1,0).
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
| Lab bipède A | 1 904 | 316 | 17 % | 316 | 1 588 | 2 564 | 8 |
| Home candidat | 4 514 | 912 | 20 % | 912 | 3 602 | 6 167 | 6 |

« Entre catégories » : la part déjà payée dont le produit a été acheté dans une AUTRE catégorie (proposition de catégories en attente). Le Lab bipède A ne tient qu'en carton à la marge 1,0 (lab-leger) : la nomenclature est la sienne.

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

