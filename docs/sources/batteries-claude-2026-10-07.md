# YXOR — Batteries, calculateurs et bus : recherche (Claude, 7 octobre 2026)

**Origine : Claude (claude.ai, recherche web).** Source secondaire, à recouper avec l'étude de Claude Code, qui reste la référence. Recherche ciblée (une dizaine de sources lues). Les valeurs **vérifiées** ont leur lien au § 9 ; ce qui n'a pas été lu est marqué **non vérifié ici** ou **non trouvé**.

## 1. Résumé en 10 lignes

1. **Tension** : les RobStride RS00 et RS02 acceptent 24 à 60 V (nominal 48 V), les RS03, RS04 et EduLite05 15 à 60 V. La fenêtre commune est **24 à 60 V**.
2. **Batterie conseillée : 12S ou 13S en Li-ion** (43 à 47 V nominal, 50 à 55 V pleine charge), sous le seuil de 60 V avec une marge pour les pics de régénération. **Éviter le 14S** (58,8 V pleine charge, trop près de 60 V).
3. **Les batteries d'outillage 18 V sont sous le minimum de 24 V** des RS00 et RS02 : il en faudrait deux en série (36 V).
4. **Les servos Feetech ont leur propre tension** (6 à 8,4 V, ou une version 12 V) : il faut un convertisseur depuis la batterie principale.
5. **Couple continu Feetech : une valeur existe.** Le STS3215 est annoncé à 6,5 kg·cm continu à 6 V (revendeurs ; fiche du fabricant à lire).
6. **Cellule de référence** : Molicel P45B (21700, 16,2 Wh, 45 A continu, 70 g, 242 Wh/kg) ou P50B (18 Wh, 60 A, 71 g, 260 Wh/kg).
7. **Calculateurs** : NVIDIA a relevé ses prix Jetson en juillet 2026 (jusqu'à +101 %). Orin Nano Super devkit à 399 $, Orin NX 16 Go à 999 $, Thor devkit à 5 499 $.
8. **Raspberry Pi 5 + AI HAT+ 2** (Hailo-10H, 40 TOPS en INT4, 8 Go de mémoire, 130 $) vise désormais les modèles de langage et la vision. **Les TOPS ne sont pas comparables** entre fabricants (INT4, INT8 sparse, FP4 sparse).
9. **CAN** : les Jetson Orin Nano et NX ont 1 contrôleur CAN FD intégré, l'AGX Orin et Thor en ont 2 ; il faut ajouter un transceiver. Le Raspberry Pi n'en a aucun. Pour 24 axes RobStride, il faut **3 à 8 bus**, selon la fréquence de commande.
10. **Envoi postal en Suisse** : colis autorisé jusqu'à **100 Wh par batterie**. Un pack de robot (200 Wh et plus) ne s'envoie pas par colis ordinaire.

## 2. Tensions

| Élément | Tension acceptée | Source |
| --- | --- | --- |
| RobStride RS00, RS02, RS02-IP67 | 24 à 60 V, nominal 48 V | revendeur reprenant les données officielles (vérifié) |
| RobStride RS03, RS04, EduLite05 | 15 à 60 V, nominal 48 V | idem (vérifié) |
| RobStride RS01 | 24 à 48 V, nominal 36 V | idem (vérifié) |
| RobStride RS05, RS06 | plage **non trouvée** ici | à lire dans les manuels |
| Feetech STS3215 (C001) | 6 à 8,4 V (nominal 7,4 V) | revendeur (vérifié) |
| Feetech STS3215 12 V (C018) | 4 à 14 V | revendeur (vérifié) |
| Jetson Orin NX (module) | 5 à 20 V | distributeur (vérifié) |

**Nombre de cellules en série** (calcul, Li-ion NMC : 3,6 V nominal, 4,2 V plein ; coupure prudente vers 3,0 V) :

| Configuration | Nominal | Plein | Vide (3,0 V/cellule) | Verdict pour RobStride |
| --- | --- | --- | --- | --- |
| 10S | 36 V | 42 V | 30 V | correct, plus de marge, moins de puissance |
| **12S** | **43,2 V** | **50,4 V** | **36 V** | **recommandé** |
| **13S** | **46,8 V** | **54,6 V** | **39 V** | **recommandé** (le plus proche du nominal 48 V) |
| 14S | 50,4 V | 58,8 V | 42 V | déconseillé : 1,2 V de marge sous 60 V |
| LiFePO4 15S | 48 V | 54,75 V | 37,5 V | correct, plus lourd |
| 2 × outillage 18 V | 36 V | 42 V | 30 V | possible, deux packs |

**Point de vigilance** : en freinage, les moteurs **renvoient** de l'énergie dans le bus et font monter la tension. Plus on part près de 60 V, plus il faut une protection contre ces surtensions (résistance de freinage ou BMS qui l'accepte).

## 3. Batteries

| Produit | Famille | Tension | Wh | Décharge continue | Masse | Wh/kg | Wh/L | BMS | Revendeur CH/UE | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Molicel P45B | cellule 21700 | 3,6 V | 16,2 | 45 A | 70 g | 242 | 643 | non (cellule) | non trouvé ici | fiche fabricant (vérifié) |
| Molicel P50B | cellule 21700 | 3,6 V | 18,0 | 60 A | 71 g | 260 | 714 | non | non trouvé ici | fiche fabricant (vérifié) |
| Makita BL1850B | outillage 18 V | 18 V | 90 | non trouvé | 0,60 kg | 150 | \~170 (113 × 75 × 62 mm) | protection intégrée | Distrelec Suisse | revendeurs (vérifié) |
| Samsung, Sony/Murata, LG (21700) | cellules | — | — | — | — | — | — | — | — | **non lus ici** |
| Packs LiPo (drone) | LiPo | — | — | — | — | — | — | rarement | — | **non lus ici** |
| DeWalt, Bosch, Milwaukee | outillage | — | — | — | — | — | — | — | — | **non lus ici** |

**Ordres de grandeur de packs** (calcul à partir des fiches, cellules seules, sans boîtier ni BMS ; ajouter environ 20 à 35 % de masse pour un pack réel, hypothèse à vérifier) :

| Pack | Cellules | Énergie | Masse des cellules | Courant continu |
| --- | --- | --- | --- | --- |
| 12S1P P45B | 12 | 194 Wh | 0,84 kg | 45 A (≈ 1,9 kW) |
| 13S1P P50B | 13 | 234 Wh | 0,92 kg | 60 A |
| 12S2P P45B | 24 | 389 Wh | 1,68 kg | 90 A |
| 2 × Makita BL1850B en série | — | 180 Wh | 1,2 kg | non trouvé |

La durée de fonctionnement dépend de la puissance moyenne du robot, qui viendra des phases 3a et 3b : elle n'est pas estimée ici.

## 4. Sécurité de la batterie dans un robot qui tombe

Bonnes pratiques (connaissances générales, **non vérifiées ici** sur une norme précise) : un BMS qui coupe en surintensité, en surtension, en sous-tension et en température ; des cellules calées dans un boîtier rigide, loin des zones d'impact (le tronc plutôt que les jambes) ; une coupure physique de la puissance, accessible, indépendante du logiciel ; un fusible principal ; un ventre ou un dos du robot qui protège le pack en cas de chute ; ne jamais recharger un pack qui a subi un choc sans inspection. La certification **UN 38.3** concerne le transport.

**Envoi en Suisse (vérifié)** : La Poste accepte les batteries lithium jusqu'à 100 Wh en colis à l'intérieur du pays, mais refuse les batteries défectueuses et celles de vélo électrique. À l'international, une batterie doit être installée dans l'appareil, avec au plus 20 Wh par cellule et 100 Wh par batterie. **Conséquence** : acheter des cellules et monter le pack soi-même passe par la poste ; un pack de robot complet de 200 Wh et plus, non.

## 5. Calculateurs

Prix : relevé de juillet 2026, prix module « 1KU+ » (par 1 000) ou devkit (vérifié). Puissance de calcul : **chiffres du fabricant, non comparables entre eux**.

| Produit | Calcul annoncé | Type | Puissance | Mémoire | CAN intégré | Prix (juillet 2026) |
| --- | --- | --- | --- | --- | --- | --- |
| Jetson Orin Nano 4 Go | 34 TOPS (Super) | INT8 sparse | 7 à 25 W | 4 Go | 1 contrôleur | 349 $ (module) |
| Jetson Orin Nano 8 Go | 67 TOPS (Super) | INT8 sparse | 7 à 25 W | 8 Go | 1 | 399 $ (module) ; **devkit Super 399 $** |
| Jetson Orin NX 8 Go | 117 TOPS (Super) | INT8 sparse | 10 à 40 W | 8 Go | 1 | 649 $ |
| Jetson Orin NX 16 Go | 157 TOPS (Super) | INT8 sparse | 10 à 40 W | 16 Go | 1 | 999 $ |
| Jetson AGX Orin 32 Go | 200 TOPS | INT8 sparse | 15 à 40 W | 32 Go | 2 | 1 799 $ |
| Jetson AGX Orin 64 Go | 275 TOPS | INT8 sparse | 15 à 60 W | 64 Go | 2 | 2 999 $ ; devkit 3 499 $ |
| Jetson T4000 (Thor) | 1 200 TFLOPS | FP4 sparse | non trouvé | 64 Go | 2 | 2 999 $ |
| Jetson T5000 (Thor) | 2 070 TFLOPS | FP4 sparse | 40 à 130 W | non lu | 2 | 4 999 $ ; devkit 5 499 $ |
| Raspberry Pi 5 + AI HAT+ (Hailo-8L) | 13 TOPS | non précisé | \~1,5 W (puce) | celle du Pi | aucun | non lu |
| Raspberry Pi 5 + AI HAT+ (Hailo-8) | 26 TOPS | non précisé | \~3,5 W (puce) | celle du Pi | aucun | non lu |
| **Raspberry Pi 5 + AI HAT+ 2 (Hailo-10H)** | 40 TOPS | **INT4** | \~4,5 W (puce) | **8 Go dédiés** | aucun | **130 $** (carte seule), sortie le 15 janvier 2026 |

**Cotes** : le module Orin NX mesure 69,6 × 45 mm, avec 1 CAN, 3 UART et une entrée 5 à 20 V (vérifié) ; il faut y ajouter une carte porteuse, dont les cotes dépendent du fabricant (**non lues ici**). Prix d'un Raspberry Pi 5 : **non lu ici**.

**Pourquoi les TOPS ne se comparent pas** : 40 TOPS en INT4 (Hailo) ne valent pas 67 TOPS en INT8 sparse (Jetson), et les TFLOPS FP4 sparse de Thor sont encore une autre unité. Selon un revendeur, les 40 TOPS de l'AI HAT+ 2 ne la rendent d'ailleurs pas nettement plus rapide que la version à 26 TOPS en vision classique.

## 6. Niveaux d'IA embarquée

| Niveau | Calculateur minimal plausible | Preuve |
| --- | --- | --- |
| (a) Commande de la marche (ONNX, 50 Hz) | un simple processeur suffit | vérifié dans le dépôt : politiques jouées sur CPU ; Berkeley Humanoid Lite marche avec un Intel N95 |
| (b) + vision | Raspberry Pi 5 + AI HAT+, ou Jetson Orin Nano | détection YOLOv8 à 60 images/s et plus sur les cartes Hailo (revendeur) |
| (c) + voix locale | Jetson Orin Nano ou NX, ou Pi 5 + AI HAT+ 2 | **non vérifié ici** |
| (d) + modèle de langage local | Pi 5 + AI HAT+ 2 (modèles jusqu'à \~6 milliards de paramètres, selon un revendeur), Jetson Orin NX 16 Go ou AGX Orin | vitesses en tokens/s : **non trouvées ici** |

## 7. Cartes de bus

**CAN intégré à Jetson (vérifié)** : les Orin Nano et NX ont un contrôleur, l'AGX Orin et Thor en ont deux. Il faut un **transceiver 3,3 V** externe. Le CAN FD monte à 15 Mbit/s sur Orin et à 8 Mbit/s sur Thor.

**Adaptateurs** (CAN USB, CAN FD sur SPI, cartes HAT pour Raspberry Pi, adaptateur série Feetech FE-URT-1) : **non lus ici**, à couvrir par l'étude de Claude Code. LeRobot Humanoid utilise un adaptateur CAN FD à deux canaux avec un Raspberry Pi 5 (source de presse).

**Combien de bus CAN pour 24 axes RobStride ?** Calcul **PROPOSÉ**, hypothèses à vérifier dans le manuel RobStride :

- bus CAN 2.0 à 1 Mbit/s ; trame étendue de 8 octets ≈ 130 bits avec le bourrage, soit ≈ 130 µs ;
- par axe et par cycle : une commande et une réponse, soit ≈ 260 µs ;
- charge de bus visée : 50 % au plus.

| Fréquence de commande | Période | Axes par bus (50 %) | Bus pour 24 axes |
| --- | --- | --- | --- |
| 500 Hz | 2 ms | 3 à 4 | **6 à 8** |
| 200 Hz | 5 ms | 9 à 10 | **3** |
| 50 Hz (politique seule) | 20 ms | > 24 | 1 |

Les RobStride ferment leur boucle de position et de couple à l'intérieur du moteur (mode « MIT », à vérifier) : une commande à 200 Hz suffit sans doute. C'est la fréquence à fixer, car elle décide du nombre de bus. Le CAN FD (plus de données par trame, débit plus élevé) réduirait le nombre de bus, **si** les RobStride le gèrent.

## 8. Exemples de robots réels

| Robot | Calculateur | Batterie | Bus | Source |
| --- | --- | --- | --- | --- |
| Berkeley Humanoid Lite | Intel N95 | non lu ici | CAN | inventaire de Claude Code du 2026-10-05 |
| LeRobot Humanoid | Raspberry Pi 5 | non lu ici | CAN FD, 2 canaux | presse (vérifiée le 2026-10-06) |
| ToddlerBot, BRIDGE, Booster T1, Unitree G1 | **non vérifié ici** | — | — | — |

## 9. Recommandations (PROPOSÉES, aucune décision)

**YXOR Lab (≈ 10 kg)**

- Batterie : pack **12S ou 13S Li-ion en 21700** à haut débit (Molicel), 1P ou 2P selon l'autonomie, monté dans le tronc, avec BMS et coupure physique. Les batteries d'outillage restent une piste de secours (2 × 18 V en série, packs protégés, faciles à acheter en Suisse), à vérifier sur leur courant de décharge.
- Calculateur : deux voies à chiffrer par l'explorateur. **Jetson Orin Nano 8 Go** (ta préférence, CUDA, 1 CAN intégré, 399 $) ou **Raspberry Pi 5 + AI HAT+ 2** (modèles de langage locaux, environ 130 $ plus le Pi, aucun CAN). La hausse des prix NVIDIA de juillet 2026 réduit l'avantage de Jetson.
- Bus : 3 bus CAN à 200 Hz, plus 1 bus série Feetech ; un convertisseur de tension pour les Feetech.

**YXOR final (≈ 35 kg)**

- Batterie : 13S, en 2P à 4P selon l'autonomie ; un pack de plusieurs centaines de Wh, qui ne s'envoie pas par la poste.
- Calculateur : **Jetson AGX Orin** ou **Thor T4000** si un modèle de langage doit tourner à bord ; Orin NX sinon.
- Sécurité : coupure de puissance indépendante du calculateur et du bus, impérative à cette masse.

## 10. Registre des sources

| Source | Type | Lien |
| --- | --- | --- |
| Tableau des paramètres RobStride (revendeur OpenELAB, données dites officielles) | revendeur | https://openelab.io/fr/products/robstride00-qdd-14n-m-integrated-joint-motor-module |
| STS3215 (Core Electronics, Sigmanortec, RobotShop) | revendeurs | https://core-electronics.com.au/feetech-sts3215-smart-servo.html |
| Molicel P45B, fiche technique | fabricant | https://www.imrbatteries.com/content/molicel\_p45b.pdf |
| Molicel P50B, fiche technique | fabricant | https://www.fsaeonline.com/content/Molicel-TDS--INR-21700-P50B-80122.pdf |
| Makita BL1850B (Bauhaus, Distrelec Suisse) | revendeurs | https://www.distrelec.ch/en/power-tool-battery-18v-5ah-90wh-makita-bl1850b/p/30468582 |
| Hausse des prix Jetson, juillet 2026 | presse spécialisée (CNX Software) | https://cnx-software.com/2026/07/22/nvidia-increases-the-price-of-jetson-modules-and-devkits-by-up-to-101 |
| Comparatif des modules Jetson | intégrateur (Connect Tech) | https://connecttech.com/jetson/jetson-module-comparison/ |
| Module Orin NX (cotes, CAN, tension) | distributeur (Farnell) | https://es.farnell.com/nvidia/900-13767-0010-000/som-8gb-arm-cortex-a78ae-v8-2/dp/4200231 |
| CAN sur Jetson (Orin, Thor) | documentation NVIDIA | https://docs.nvidia.com/jetson/archives/r38.2/DeveloperGuide/HR/ControllerAreaNetworkCan.html |
| Raspberry Pi AI HAT+ 2 | revendeurs (SparkFun, buyzero) | https://www.sparkfun.com/raspberry-pi-ai-hat-2.html |
| Marchandises dangereuses, Poste suisse | transporteur | https://www.post.ch/fr/expedier-des-colis/marchandises-dangereuses/marchandises-dangereuses-suisse |

**Non ouverts ou non trouvés** : plages de tension des RS05 et RS06 ; fiches Samsung, Sony/Murata et LG ; packs LiPo ; DeWalt, Bosch et Milwaukee ; prix du Raspberry Pi 5 ; cartes porteuses Jetson ; adaptateurs CAN et série ; vitesses des modèles de langage en tokens/s ; calculateurs et batteries de ToddlerBot, BRIDGE, T1 et G1 ; fiche officielle Feetech du couple continu.
