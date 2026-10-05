# Marché des actionneurs, octobre 2026

**Engendré** par `.venv/bin/python scripts/marche_actionneurs.py --ecrire` depuis `params/actionneurs.yaml` (`candidats` et `marche`). Ne pas éditer à la main. Cartographie, **aucune décision** (phase 1 de la stratégie de la fiche 0069). Chaque valeur a sa source dans le catalogue ; une case vide est une valeur NON LUE, jamais une estimation.

211 actionneurs : 28 déjà au catalogue, 183 ajoutés le 2026-10-05 ; 10 familles.

## Familles (même bus, même protocole, même logiciel)

Une famille est l'invariant de la fiche 0069 entre YXOR Lab et YXOR : on peut changer de modèle à l'intérieur d'une famille sans changer le bus, le protocole ni le logiciel.

| Famille | Bus | Protocole | Logiciel | Actionneurs |
| --- | --- | --- | --- | ---: |
| **RobStride** | CAN 2.0 / CAN FD (RS01 : CAN 2.0 seul), 1 Mbit/s | protocole CAN privé RobStride (trames étendues, types 0–25), CANopen DS402, protocole « MIT » ; bascule de pr… | « upper computer » (logiciel de réglage Windows) au centre de téléchargement de www.robstride.com, avec l'ada… | 10 |
| **Damiao** | CAN 2.0 1 Mbit/s (J3507, J43xx, J6006, J8006, J8009, J100xx) ; CAN FD jusqu'à 5 Mbit/s (J6216L/P, JH11/14/17,… | protocole CAN Damiao : modes MIT, position-vitesse, vitesse, hybride force-position ; CSP/CSV/CST en plus sur… | DMTool (outil de réglage) : https://github.com/dmBots/motor-debugging-tool ; exemples C/C++/Python/Matlab/C# … | 28 |
| **SteadyWin** | CAN (≤ 1 Mbit/s, trame standard) ; RS485/RS232 selon le driver (GDZ : « CAN & RS485 » au tableau ; GDS/GDM : … | « SteadyWin Motor Driver Protocol Specification » rev2.2 (commandes 0x81–0xC1, CAN/RS485) ; driver GDM : prot… | MotorWizard 2.1.0 (steadywin_motorwizard_2.1.0.241015.exe) et MotorTool V2.5, page Support https://steadywin.… | 47 |
| **CubeMars** | CAN 1 Mbit/s (+ UART pour le réglage) | deux modes : servo (protocole CAN CubeMars, trames étendues) et force control « MIT » (trames standard, posit… | « Upper Computer » CubeMars : V3.2.3 pour la génération AK 3.0 (https://www.cubemars.com/data/cms/202606/ak-s… | 21 |
| **MyActuator** | EtherCAT & CAN BUS (V4 / V4.1 / RH, suffixe « E ») ; CAN seul (suffixe « C ») ; RS485 (suffixe « R », ex. X8-… | « CAN BUS Motor Motion Protocol V4.4 » (260425 ; CAN 1 Mbps, RS485 115200 bps à 2,5 Mbps, p. 3 du texte extra… | MYACTUATOR Setup Software V4.0 (20250704) : https://www.myactuator.com/downloads-setupsoftware ; SDK-240913 e… | 32 |
| **HighTorque** | CAN FD / CAN, 5 Mbit/s (fiches Module0602E/0603E) | protocole HighTorque fdcan, https://book.hightorque.cn/fdcanProtocolAnalysis (non ouvert) | HIGH TORQUE Motor Debugging Assistant (https://book.hightorque.cn/HIGHTORQUEMotorDebuggingAssistantUsermanual… | 14 |
| **Encos** | CAN 1 Mbit/s (tableaux revendeur) ; EtherCAT via adaptateur EtherCAT/CAN | protocole CAN Encos, implémenté par encos_driver | https://github.com/EncosTech/encos_driver (MIT, sauf plugin EtherCAT GPL-3.0-or-later), https://github.com/En… | 20 |
| **Unitree** | RS-485 (A1, B1, GO-M8010-6, IM6014) ; TTL demi-duplex (servos YS-342026) | protocole Unitree propriétaire | https://github.com/unitreerobotics/unitree_actuator_sdk (BSD-3-Clause, bibliothèques précompilées ; exemples … | 6 |
| **Feetech** | TTL half-duplex asynchrone, un fil de signal, multipoint par ID (0-253) | Protocole série propriétaire Feetech (paquets numériques) ; STS = capteur magnétique 12 bits (4096 pas), SCS … | — | 16 |
| **ROBOTIS Dynamixel** | TTL half-duplex multipoint (séries XL/XC/XM335) ; RS-485 ou TTL selon suffixe -R/-T (XM430/XH430) | DYNAMIXEL Protocol 2.0 | DYNAMIXEL Wizard 2.0, DYNAMIXEL SDK, DYNAMIXEL Workbench (menu SOFTWARE de l'e-Manual) | 16 |

Raisons sociales et sources complètes : `params/actionneurs.yaml`, `marche.familles_logicielles`.

Sans famille rattachée : cybergear.

## Couple en pointe et masse

![Couple en pointe selon la masse, par famille](marche-actionneurs-2026-10.svg)

Chaque panneau montre une famille en couleur et le reste du marché en gris. Les diagonales sont des couples massiques constants (10, 30 et 100 N·m/kg) : plus un point est haut à masse égale, plus l'actionneur est « fort pour son poids ». Un cercle VIDE est un couple au blocage, tracé faute de pointe publiée (servos, HighTorque, SteadyWin). Le couple en POINTE flatte : le couple continu et le couple au blocage, plus bas, sont dans le tableau.

## Tous les actionneurs

| Actionneur | Famille | Pointe (N·m) | Continu (N·m) | Blocage (N·m) | Masse (g) | N·m/kg (pointe) | Cotes | STEP | Prix | CH/UE |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| CubeMars AK40-10 V3.0 KV170 (référence) | CubeMars | 4.1 | 1.3 | — | 190 | 21.6 | Ø53 × 40,2 | oui | 135.9 USD | — |
| CubeMars AK40-10 KV170 (génération AK 2.0) | CubeMars | 4.1 | 1.3 | — | 200 | 20.5 | Ø53 × 37 | oui | 140.95 EUR | oui |
| CubeMars AK45-10 V3.0 KV75 | CubeMars | 7 | 2.5 | — | 262 | 26.7 | Ø53 × 45,2 | oui | 162.95 EUR | oui |
| CubeMars AK45-10 KV75 (génération AK 2.0) | CubeMars | 7 | 2.5 | — | 260 | 26.9 | Ø53 × 43 | oui | 159.96 EUR | oui |
| CubeMars AK60-6 V3.0 KV80 | CubeMars | 9 | 3 | — | 380 | 23.7 | Ø79 × 43 | oui | 276.99 EUR | oui |
| CubeMars AK60-6 V1.1 KV140 | CubeMars | 9 | 3 | — | 368 | 24.5 | Ø79 × 39,5 | oui | 298.9 USD | — |
| CubeMars AKA60-6 KV80 | CubeMars | 9 | 3 | — | 460 | 19.6 | Ø80 × 51,2 | oui | 298.9 USD | — |
| CubeMars AK80-6 KV100 | CubeMars | 12 | 6 | — | 485 | 24.7 | Ø98 × 38,5 | oui | 592.95 EUR | oui |
| CubeMars AK80-9 V3.0 KV100 | CubeMars | 18 | 9 | — | 490 | 36.7 | — | oui | 479.9 USD | — |
| CubeMars AK45-36 KV80 (génération AK 2.0) | CubeMars | 24 | 8 | — | 340 | 70.6 | Ø55 × 54 | oui | 185.9 USD | — |
| CubeMars AK45-36 V3.0 KV80 | CubeMars | 24 | 8 | — | 349 | 68.8 | Ø55 × 56,5 | oui | 185.9 USD | — |
| CubeMars AK70-10 KV100 | CubeMars | 24.8 | 8.3 | — | 621 | 39.9 | Ø89 × 50,25 | oui | 517.95 EUR | oui |
| CubeMars AK80-8 KV60 | CubeMars | 25 | 10 | — | 570 | 43.9 | Ø98 × 43,9 | oui | 559.35 EUR | oui |
| CubeMars AK70-9 V3.0 KV60 (alternative L, sous la plage) | CubeMars | 29.2 | 8.5 | — | 540 | 54.1 | — | oui | 398.9 USD | — |
| CubeMars AK10-9 V2.0 KV60 | CubeMars | 48 | 18 | — | 960 | 50 | Ø98 × 61,7 | oui | 798.9 USD | — |
| CubeMars AK10-9 V3.0 KV60 | CubeMars | 53 | 18 | — | 940 | 56.4 | — | oui | 789.0 EUR | oui |
| CubeMars AKA10-9 KV60 | CubeMars | 53 | 18 | — | 1.06e+03 | 50 | Ø100 × 70 | oui | 798.9 USD | — |
| CubeMars AK60-39 V3.0 KV80 | CubeMars | 72 | 24 | — | 750 | 96 | Ø79 × 67 | oui | 448.9 USD | — |
| CubeMars AKH70-16 V1.0 KV41 (arbre creux) | CubeMars | 78 | 26 | — | 879 | 88.7 | Ø90 × 60,5 | oui | 598.9 USD | — |
| CubeMars AK80-64 KV80 | CubeMars | 120 | 48 | — | 850 | 141 | Ø98 × 61,9 | oui | 999.95 EUR | oui |
| CubeMars AKH70-48 V1.0 KV41 (arbre creux) | CubeMars | 222 | 74 | — | 1.4e+03 | 159 | Ø90 × 81,5 | oui | 698.9 USD | — |
| Damiao DM-H3510 (moteur-roue, entraînement direct) | Damiao | 0.45 | 0.18 | — | — | — | Ø42 × 31,5 | oui | 51.95 EUR | oui |
| Damiao DM-J3507-2EC | Damiao | 3 | 0.8 | — | 150 | 20 | Ø46 × 37,9 | oui | 124.95 EUR | oui |
| Damiao DM-J4310-2EC V1.1 | Damiao | 7 | 3 | — | 306 | 22.9 | Ø57 × 46 | oui | — | oui |
| Damiao DM-JH11-51-2EC (harmonique) | Damiao | 7.8 | 3.2 | — | 345 | 22.6 | Ø52 × 60 | oui | — | oui |
| Damiao DM-JH11-101-2EC (harmonique) | Damiao | 10.5 | 4.8 | — | 345 | 30.4 | Ø52 × 60 | oui | — | oui |
| Damiao DM-J6006-2EC | Damiao | 12 | 4 | — | 335 | 35.8 | Ø76 × 36,5 | oui | 243.0 EUR | oui |
| Damiao DM-J4310-2EC V1.2 | Damiao | 12.5 | 3.5 | — | 306 | 40.8 | Ø57 × 46 | oui | 158.0 EUR | oui |
| Damiao DM-J4310-2EC V1.2 (48 V) | Damiao | 12.5 | 3.5 | — | 306 | 40.8 | — | oui | 140.95 EUR | oui |
| Damiao DM-J4310P-2EC | Damiao | 12.5 | 3.5 | — | 330 | 37.9 | Ø57 × 49,05 | oui | 182.0 EUR | oui |
| Damiao DM-JH14-51-2EC (harmonique) | Damiao | 18 | 5.4 | — | 775 | 23.2 | Ø70 × 70 | oui | — | oui |
| Damiao DM-J8006-2EC V1.1 | Damiao | 20 | 8 | — | 559 | 35.8 | — | oui | 214.0 USD | oui |
| Damiao DM-JH17-51-2EC (harmonique) | Damiao | 24 | 16 | — | 985 | 24.4 | Ø80 × 70 | oui | — | oui |
| Damiao DM-J4340-2EC (sans indice, avant V1.1) | Damiao | 27 | 9 | — | 362 | 74.6 | Ø57 × 53,3 | — | — | oui |
| Damiao DM-J4340P-2EC (sans indice) | Damiao | 27 | 9 | — | 381 | 70.9 | Ø57 × 56,5 | — | — | oui |
| Damiao DM-JH14-101-2EC (harmonique) | Damiao | 28 | 7.8 | — | 775 | 36.1 | Ø70 × 70 | oui | — | oui |
| Damiao DM-J4340-2EC V1.1 (48 V) | Damiao | 40 | 12 | — | 362 | 110 | — | oui | 166.0 USD | oui |
| Damiao DM-J8009-2EC (alternative L) | Damiao | 40 | 20 | — | 896 | 44.6 | — | oui | 419.0 EUR | oui |
| Damiao DM-J4340P-2EC V1.1 | Damiao | 40 | 12 | — | 381 | 105 | Ø57 × 56,5 | oui | — | oui |
| Damiao DM-J8009P-2EC (sans indice) | Damiao | 40 | 20 | — | 963 | 41.5 | Ø98 × 61,7 | oui | — | oui |
| Damiao DM-J8009P-2EC V1.1 | Damiao | 40 | 20 | — | 950 | 42.1 | Ø98 × 61,7 | — | — | oui |
| Damiao DM-J6216L-2EC | Damiao | 45 | 10 | — | 740 | 60.8 | Ø67 × 62,5 | oui | — | oui |
| Damiao DM-J6216P-2EC | Damiao | 48 | 10 | — | 740 | 64.9 | Ø67 × 62,5 | oui | — | oui |
| Damiao DM-JH17-101-2EC (harmonique) | Damiao | 54 | 24 | — | 985 | 54.8 | Ø80 × 70 | oui | — | oui |
| Damiao DM-J6248P-2EC | Damiao | 97 | 30 | — | 628 | 154 | Ø76 × 62,5 | oui | — | oui |
| Damiao DM-J10010L-2EC | Damiao | 120 | 40 | — | 1.37e+03 | 87.5 | Ø120 × 53 | oui | 298.0 EUR | oui |
| Damiao DM-J10010-2EC | Damiao | 150 | 40 | — | 1.48e+03 | 101 | Ø112 (hors tout 120) × 62 | oui | — | oui |
| Damiao DM-J8520P-2EC | Damiao | 192 | 35 | — | — | — | Ø90 × 70 | oui | — | oui |
| Damiao DM-J10422P-2EC | Damiao | 400 | 100 | — | 2.7e+03 | 148 | Ø110 × 89,9 | oui | — | oui |
| DYNAMIXEL XL330-M077-T | ROBOTIS Dynamixel | — | — | 0.215 | 18 | — | 20.0 × 34.0 × 26.0 | oui | 40.2  | oui |
| DYNAMIXEL XL330-M288-T | ROBOTIS Dynamixel | — | — | 0.52 | 18 | — | 20.0 × 34.0 × 26.0 | oui | 40.2  | oui |
| DYNAMIXEL XC330-M181-T | ROBOTIS Dynamixel | — | — | 0.6 | 23 | — | 20.0 × 34.0 × 26.0 | oui | 110.4  | oui |
| DYNAMIXEL XC330-M288-T | ROBOTIS Dynamixel | — | — | 0.93 | 23 | — | 20.0 × 34.0 × 26.0 | oui | 110.4  | oui |
| DYNAMIXEL XC330-T181-T | ROBOTIS Dynamixel | — | — | 0.76 | 23 | — | 20.0 × 34.0 × 26.0 | oui | 110.4  | oui |
| DYNAMIXEL XC330-T288-T | ROBOTIS Dynamixel | — | — | 0.92 | 23 | — | 20.0 × 34.0 × 26.0 | oui | 110.4  | oui |
| DYNAMIXEL XM335-T323-T | ROBOTIS Dynamixel | — | — | 1.03 | 27 | — | 19.0 × 35.0 × 22.0 | oui | 174.0  | oui |
| DYNAMIXEL XL430-W250-T | ROBOTIS Dynamixel | — | — | 1.4 | 57.2 | — | 28.5 × 46.5 × 34 | oui | 36.0  | oui |
| DYNAMIXEL XC430-W150-T | ROBOTIS Dynamixel | — | — | 1.6 | 65 | — | 28.5 × 46.5 × 34 | oui | 131.94  | oui |
| DYNAMIXEL XC430-W240-T | ROBOTIS Dynamixel | — | — | 1.9 | 65 | — | 28.5 × 46.5 × 34 | oui | 131.94  | oui |
| DYNAMIXEL 2XL430-W250-T | ROBOTIS Dynamixel | — | — | 1.4 | 98.2 | — | 36 × 46.5 × 36 | oui | 152.16  | oui |
| DYNAMIXEL 2XC430-W250-T | ROBOTIS Dynamixel | — | — | 1.8 | 102 | — | 36 × 46.5 × 36 | oui | 304.2  | oui |
| DYNAMIXEL XH430-W210-T | ROBOTIS Dynamixel | — | — | 2.5 | 82 | — | 28.5 × 46.5 × 34 | oui | 411.0  | oui |
| DYNAMIXEL XH430-W350-T | ROBOTIS Dynamixel | — | — | 3.4 | 82 | — | 28.5 × 46.5 × 34 | oui | 411.0  | oui |
| Dynamixel XM430-W210 (référence) | ROBOTIS Dynamixel | 3 | — | 3 | 82 | 36.6 | — | oui | 317.4  | oui |
| Dynamixel XM430-W350 (référence) | ROBOTIS Dynamixel | 4.1 | — | 4.1 | 82 | 50 | 28,5 × 46,5 × 34 | oui | 317.4  | oui |
| ENCOS EC-A2806-P2-36 | Encos | 12 | 3 | — | 162 | 74.1 | Ø44 × 44 | oui | 625.0 USD | — |
| ENCOS EC-A4310-P2-36 | Encos | 36 | 12 | — | 382 | 94.2 | Ø56 × 60.5 | oui | 700.0 USD | — |
| ENCOS EC-A4310-P2-36H | Encos | 36 | 12 | — | 414 | 87 | Ø60 × 59.5 | oui | 750.0 USD | — |
| ENCOS EC-A6408-P2-16H | Encos | 45 | 14 | — | 800 | 56.2 | Ø88 × 60 | — | 1125.0 USD | — |
| ENCOS EC-A3814-H14-107 | Encos | 60 | 20 | — | 434 | 138 | Ø53 × 78.5 | oui | 1375.0 USD | — |
| ENCOS EC-A6408-P2-25 | Encos | 60 | 20 | — | 625 | 96 | Ø88 × 59.5 | oui | 875.0 USD | — |
| ENCOS EC-A6408-P2-30.25H | Encos | 70 | 20 | — | 846 | 82.7 | Ø88 × 65 | oui | 1000.0 USD | — |
| ENCOS EC-A4315-P2-36 | Encos | 75 | 25 | — | 485 | 155 | Ø56 × 69.5 | oui | 750.0 USD | — |
| ENCOS EC-A5013-H17-100 | Encos | 90 | 30 | — | 630 | 143 | Ø63 × 81.5 | oui | 1500.0 USD | — |
| ENCOS EC-A8112-P1-18 | Encos | 90 | 30 | — | 868 | 104 | Ø105 × 53 | oui | 1000.0 USD | — |
| ENCOS EC-A8112-P1-18H | Encos | 90 | 30 | — | 883 | 102 | Ø105 × 53 | oui | 1250.0 USD | — |
| ENCOS EC-A6416-P2-25 | Encos | 120 | 40 | — | 805 | 149 | Ø88 × 67.5 | oui | 925.0 USD | — |
| ENCOS EC-A6013-H20-100 | Encos | 130 | 40 | — | 906 | 143 | Ø73 × 84 | oui | 1750.0 USD | — |
| ENCOS EC-A8116-P1-18 | Encos | 130 | 40 | — | 961 | 135 | Ø105 × 57 | oui | 1125.0 USD | — |
| ENCOS EC-A8116-P1-18H | Encos | 130 | 40 | — | 968 | 134 | Ø105 × 57 | oui | 1375.0 USD | — |
| ENCOS EC-A6416-P2-30.25H | Encos | 132 | 25 | — | 1.01e+03 | 130 | Ø88 × 73.9 | — | 1125.0 USD | — |
| ENCOS EC-A10020-P1-12 | Encos | 150 | 50 | — | 1.37e+03 | 109 | Ø124 × 60 | oui | 1250.0 USD | — |
| ENCOS EC-A13715-P1-12.67 | Encos | 320 | 110 | — | 2.7e+03 | 119 | Ø170 × 73 | oui | 2250.0 USD | — |
| ENCOS EC-A10020-P2-24 | Encos | 330 | 100 | — | 2.21e+03 | 149 | Ø124 × 85 | oui | 2250.0 USD | — |
| ENCOS EC-A13720-P1-11.4 | Encos | 380 | 120 | — | 3.16e+03 | 120 | Ø170 × 84.5 | oui | 2370.0 USD | — |
| Feetech STS3215 12 V (ST-3215-C018) | Feetech | — | — | 2.94 | 55 | — | 45.2 × 24.7 × 35 | — | 26.45  | oui |
| Feetech STS3215 7,4 V (ST-3215-C001) | Feetech | — | — | 1.62 | 55 | — | 45.2 × 24.7 × 35 | — | 24.35  | oui |
| Feetech STS3032 (ST-3032-C001) | Feetech | — | — | 0.441 | 20.6 | — | 32 × 12 × 27.5 | — | 37.24  | oui |
| Feetech STS3032 double axe (ST-3032-C036) | Feetech | — | — | 0.441 | 20.6 | — | 32 × 12 × 27.5 | — | 39.25  | oui |
| Feetech STS3036 boîtier plastique (ST-3036-C001) | Feetech | — | — | 0.441 | 17.7 | — | 32 × 12 × 27.5 | — | — | — |
| Feetech SCS0009 (SC-0090-C013) | Feetech | — | — | 0.226 | 13.2 | — | 23.2 × 12 × 25.5 | — | 12.95  | oui |
| Feetech SCS15 (SCS15-C022) | Feetech | — | — | 1.39 | 58.2 | — | 40.2 × 20.2 × 40 | — | — | — |
| Feetech SCS2332 (SC-2332-C001) | Feetech | — | — | 0.441 | 26 | — | 32 × 12 × 27.5 | — | — | — |
| Feetech HL-2909-C001 (série HLS, 12 V, force contrôlée) | Feetech | — | — | 0.873 | 22.5 | — | 34 × 20 × 23 | — | — | — |
| Feetech HL-2915-C001 (série HLS, 12 V, force contrôlée) | Feetech | — | — | 1.39 | 27.8 | — | 34 × 20 × 23 | — | — | — |
| Feetech HD-1910-C001 (4,8 V, « Open Source Duck Robot ») | Feetech | — | — | 0.883 | 21 | — | 34 × 20 × 23 | — | — | — |
| Feetech SC-0002-C001 (2 g) | Feetech | — | — | 0.0686 | 4.8 | — | 16.7 × 8.3 × 17.2 (PDF) ; page 16.05 × 8.2 × 17 → retenu le PDF (plus grand) | — | — | — |
| Feetech SC-0037-C001 (3,7 g) | Feetech | — | — | 0.177 | 6.1 | — | 20.19 × 8.5 × 17.4 | — | — | — |
| Feetech SC-0043-C001 (4,3 g) | Feetech | — | — | 0.216 | 6.6 | — | 20.3 × 8.5 × 19.39 | — | — | — |
| Feetech SC-0005-C001 (5 g) | Feetech | — | — | 0.177 | 8.8 | — | 21.6 × 11.7 × 20.5 | — | — | — |
| Feetech STS3250 | Feetech | 4.9 | 1.57 | 4.9 | 74.5 | 65.8 | 45,22 × 24,72 × 35 | — | — | — |
| HTDW-4438-30-NE-JC (HTDW-4530-02-CNE) | HighTorque | — | 2 | 10 | 237 | — | 44 × 44 × 44,9 | oui | 199.0 USD | — |
| HTDW-5022-02-DNE | HighTorque | — | 3.5 | 13 | 322 | — | 50 × 50 × 47,4 | oui | 189.0 USD | — |
| HTDW-5036-02-CNE | HighTorque | — | 6 | 21 | 345 | — | 50 × 50 × 52,4 | oui | 199.0 USD | — |
| HTDW-6036-02-CNE | HighTorque | — | 10 | 36 | 570 | — | 60 × 60 × 56 | oui | 229.0 USD | — |
| HTDW-7535-02-CNE | HighTorque | — | 18 | 60 | 850 | — | 86 × 86 × 56 (boîte STEP) | oui | 309.0 USD | — |
| HTPU-6035-04-CNE | HighTorque | — | 10 | 36 | 558 | — | 115 × 61,9 × 37 | oui | 279.0 USD | — |
| HTPU-7033-04-CNE | HighTorque | — | 20 | 50 | 808 | — | 141,5 × 71,5 × 36,9 | oui | 339.0 USD | — |
| HTPW-7507-02-DNE | HighTorque | — | 4 | 12 | 390 | — | 86 × 86 × 35 (boîte STEP) | oui | 189.0 USD | — |
| HTCP-4531-06-CYC | HighTorque | — | 2 | 10 | 237 | — | 44 × 44 × 44,9 | oui | 259.0 USD | — |
| HTCP-5031-06-CYC | HighTorque | — | 4 | 16 | 385 | — | 50 × 50 × 53 | oui | 259.0 USD | — |
| HighTorque HTDW-4438-30-NE (HTDW-4530-02-DNE) | HighTorque | 10 | 2 | 10 | 237 | 42.2 | 44 × 44 × 43,4 | oui | 209.95 EUR | oui |
| HighTorque HTDW-5047-36-NE | HighTorque | 16 | 4 | 24 | 305 | 52.5 | 50 × 50 × 47 | — | — | — |
| HighTorque HTDW-5036-02-DNE | HighTorque | 21 | 6 | 21 | 323 | 65 | — | oui | 189.0 USD | — |
| HighTorque HTDW-6036-02-DNE | HighTorque | 36 | 10 | 36 | 565 | 63.7 | — | oui | 219.0 USD | — |
| MyActuator RMD-X2-P9-3-C (« X2-3 ») | MyActuator | 3 | 0.9 | — | 230 | 13 | — | — | — | — |
| MyActuator RMD-X2-P28-7-E (« X2-7 ») | MyActuator | 7 | 2.5 | 3.75 | 260 | 26.9 | Ø44 × 63,5 | oui | 299.95 EUR | oui |
| MyActuator RMD-X6-P6-7-C-N (« X6-7 », ex-RMD-X6 1:6 V2) | MyActuator | 7 | 3.5 | — | 350 | 20 | Ø76 × 38 | oui | — | oui |
| MyActuator RMD-X2-P28-7-C-Lite (« X2-7-L ») | MyActuator | 7 | 2.5 | — | 260 | 26.9 | — | — | — | — |
| MyActuator RMD-X6-P8-8-C-N (« X6-8 », ex-RMD-X6 1:8 V3) | MyActuator | 8 | 4.5 | — | 490 | 16.3 | Ø79 × 44,5 | oui | — | oui |
| MyActuator RMD-X4-P12-10-E (« X4-10 ») | MyActuator | 10 | 4 | 5.2 | 330 | 30.3 | Ø55 × 55,5 | oui | 299.95 EUR | oui |
| MyActuator RMD-X4-P12-10-E-L (« X4-10-L ») | MyActuator | 10 | 4 | — | 330 | 30.3 | 55 × 55,5 | oui | — | — |
| MyActuator EPS-RH-14-50-E-N-D (« RH-14 », harmonique 50:1, sans frein) | MyActuator | 14 | 5.5 | — | 780 | 17.9 | — | — | — | — |
| MyActuator RMD-X8-P9-25-C-N (« X8-25 », ex-RMD-X8 Pro 1:9 V2) | MyActuator | 25 | 10 | — | 710 | 35.2 | Ø98 × 51 | oui | — | oui |
| MyActuator EPS-RH-17-50-E-N-D (« RH-17 », harmonique 50:1, sans frein) | MyActuator | 27 | 17.5 | — | 1.11e+03 | 24.3 | — | — | — | — |
| MyActuator EPS-RH-14-100-E-N-D (« RH-14 », harmonique 100:1, sans frein) | MyActuator | 28 | 11 | 16.5 | 780 | 35.9 | Ø70 × 81,7 | oui | — | — |
| MyActuator RMD-X4-P36-36-E-L (« X4-36-L ») | MyActuator | 30 | 7.5 | 36 | 360 | 83.3 | 55 × 61 | oui | — | — |
| MyActuator RMD-X8-P9-32-R (« X8-32 ») | MyActuator | 32 | 8 | 15.6 | 550 | 58.2 | Ø96 × 41,2 | oui | — | — |
| MyActuator RMD-X4-P36-36-E (« X4-36 ») | MyActuator | 34 | 10.5 | 17.2 | 360 | 94.4 | — | oui | 349.95 EUR | oui |
| MyActuator RMD-X10-P7-40-C-N (« X10-40 », ex-RMD-X10 1:7 V3) | MyActuator | 40 | 12 | — | 1.15e+03 | 34.8 | Ø122 × 53 | oui | — | oui |
| MyActuator RMD-X6-P36-40-C-N (« X6-40 », ex-RMD-X6-S2 1:36 V2) | MyActuator | 40 | 18 | — | 590 | 67.8 | Ø76 × 60,5 | oui | — | oui |
| MyActuator EPS-RH-20-50-E-N-D (« RH-20 », harmonique 50:1, sans frein) | MyActuator | 40 | 25 | — | 1.45e+03 | 27.6 | — | — | — | — |
| MyActuator RMD-X6-P20-50-E-L (« X6-50-L ») | MyActuator | 45 | 9 | 50 | 780 | 57.7 | 80 × 63,5 | oui | — | — |
| MyActuator RMD-X5-P25-50-E (« X5-50 ») | MyActuator | 45 | 14.5 | — | 750 | 60 | — | — | — | — |
| MyActuator EPS-RH-17-100-E-N-D (« RH-17 », harmonique 100:1, sans frein) | MyActuator | 54 | 35 | 52.5 | 1.11e+03 | 48.6 | Ø80 × 90,2 | oui | — | — |
| MyActuator RMD-X6-P20-60-E (« X6-60 ») | MyActuator | 60 | 20 | 30 | 820 | 73.2 | Ø80 × 67,5 | oui | 427.95 EUR | oui |
| MyActuator EPS-RH-25-50-E-N-D (« RH-25 », harmonique 50:1, sans frein) | MyActuator | 78.5 | 54 | — | 2.42e+03 | 32.4 | — | — | — | — |
| MyActuator EPS-RH-20-100-E-N-D (« RH-20 », harmonique 100:1, sans frein) | MyActuator | 80 | 50 | 75 | 1.45e+03 | 55.2 | Ø90 × 82,9 | oui | — | — |
| MyActuator RMD-X10-P35-100-C-N (« X10-100 », ex-RMD-X10-S2 1:35 V3) | MyActuator | 100 | 50 | — | 1.7e+03 | 58.8 | Ø122 × 74 | oui | — | oui |
| MyActuator EPS-RH-32-50-E-N-D (« RH-32 », harmonique 50:1, sans frein) | MyActuator | 114 | 75 | — | 4.32e+03 | 26.5 | — | — | — | — |
| MyActuator RMD-X8-P20-120-E (« X8-120 ») | MyActuator | 120 | 43 | 64.5 | 1.4e+03 | 85.7 | Ø96 × 76 | oui | 559.95 EUR | oui |
| MyActuator RMD-X8-P20-150-E-03 (« X8-150 ») | MyActuator | 120 | 20 | 150 | 1.33e+03 | 90.2 | 96 × 71 | oui | — | — |
| MyActuator EPS-RH-25-100-E-N-D (« RH-25 », harmonique 100:1, sans frein) | MyActuator | 157 | 108 | 162 | 2.42e+03 | 64.9 | Ø110 × 89,5 | oui | 1399.95 EUR | oui |
| MyActuator RMD-X10-P20-200-E (« X10-200 ») | MyActuator | 170 | 43 | 200 | 1.64e+03 | 104 | 124 × 63,5 | oui | — | — |
| MyActuator EPS-RH-32-100-E-N-D (« RH-32 », harmonique 100:1, sans frein) | MyActuator | 229 | 150 | 195 | 4.32e+03 | 53 | Ø142 × 108,4 | oui | — | — |
| MyActuator RMD-X12-P20-320-E (« X12-320 ») | MyActuator | 320 | 85 | 150 | 2.37e+03 | 135 | Ø124 × 85 | oui | 979.95 EUR | oui |
| MyActuator RMD-X15-P20-450-E (« X15-450 ») | MyActuator | 450 | 145 | 218 | 3.5e+03 | 129 | Ø166 × 90 | oui | 1377.95 EUR | oui |
| RobStride EduLite 05 | RobStride | 5.5 | 1.8 | 1.1 | 242 | 22.7 | — | oui | 80.0 USD | oui |
| RobStride RS05 | RobStride | 5.5 | 1.6 | 1.2 | 191 | 28.8 | Ø46 × 44 | oui | 121.99 USD | oui |
| RobStride RS00 | RobStride | 14 | 5 | 3.6 | 330 | 42.4 | Ø57 × 51 | oui | 598 CNY | oui |
| RobStride RS02 | RobStride | 17 | 6 | 6 | 380 | 44.7 | Ø78,5 × 41,5 | oui | 160.99 USD | oui |
| RobStride RS01 | RobStride | 17 | 6 | 6 | 380 | 44.7 | Ø78,5 × 41,5 | oui | 137.95 EUR | oui |
| RobStride RS02-IP67 | RobStride | 17 | 6 | 6 | 490 | 34.7 | Ø81 × 48 | oui | 219.95 EUR | oui |
| RobStride RS06 | RobStride | 36 | 11 | 8 | 621 | 58 | Ø82 × 49 | oui | 210.0 USD | oui |
| RobStride 10P (RS10P) | RobStride | 42 | 14 | 9.5 | 460 | 91.3 | Ø57 × 60,6 | oui | 199.95 EUR | oui |
| RobStride RS03 | RobStride | 60 | 20 | 13 | 900 | 66.7 | Ø98 × 54,1 | oui | 225.0 USD | oui |
| RobStride RS04 | RobStride | 120 | 35 | 28.5 | 1.42e+03 | 84.5 | Ø120 × 55,7 | oui | 254.95 EUR | oui |
| SteadyWin GIM3505-8, driver GDS34, 24 V | SteadyWin | — | 0.65 | 1.27 | 97 | — | Ø43 × 30 | oui | 154.95 EUR | oui |
| SteadyWin GIM3505-8, driver GDZ34, 24 V | SteadyWin | — | 0.67 | 1.79 | 97 | — | Ø43 × 30 | oui | 167.95 EUR | oui |
| SteadyWin GIM3505-9, driver non nommé, 24 V | SteadyWin | — | 0.71 | 1.95 | 132 | — | Ø45 × 36.1 | oui | — | oui |
| SteadyWin GIM3505-36, driver non nommé, 24 V | SteadyWin | — | 3.12 | 8.01 | 177 | — | Ø45 × 44.1 | oui | — | oui |
| SteadyWin GIM3510-8, driver GDZ34, 24 V | SteadyWin | — | 1 | 6.28 | 260 | — | Ø46 × 51.5 | oui | 164.95 EUR | oui |
| SteadyWin GIM3510-64, driver GDZ34, 24 V | SteadyWin | — | 9 | 50 | 507 | — | Ø46 × 77.5 | oui | 200.95 EUR | oui |
| SteadyWin GIM4305-10, driver GDZ34, 24 V | SteadyWin | — | 1.05 | 3.82 | 150 | — | Ø53 × 32 | oui | — | oui |
| SteadyWin GIM4305-10, driver GDS34, 24 V | SteadyWin | — | 1 | 3.47 | 150 | — | Ø53 × 32 | oui | — | oui |
| SteadyWin GIM4310-10, driver GDS34, 24 V | SteadyWin | — | 2.05 | 5.6 | 227 | — | Ø53 × 38 | oui | 200.95 EUR | oui |
| SteadyWin GIM4310-36, driver GDZ34, 24 V | SteadyWin | — | 6.24 | 25.4 | 310 | — | Ø55 × 47 | oui | 195.95 EUR | oui |
| SteadyWin GIM4310-36, driver GDS34, 24 V | SteadyWin | — | 7.38 | 20.2 | 310 | — | Ø55 × 47 | oui | 200.95 EUR | oui |
| SteadyWin GIM4310-40, driver GDZ4-40, 24 V | SteadyWin | — | 8.5 | 30.6 | 364 | — | Ø57 × 56 | oui | 168.95 EUR | oui |
| SteadyWin GIM4315-8, driver GDZ468, 24 V | SteadyWin | — | 1.6 | 14.2 | 372 | — | Ø57 × 58 | oui | 85.95 EUR | oui |
| SteadyWin GIM6010-6, driver GDS6, 24 V | SteadyWin | — | 3.3 | 8 | 318 | — | Ø76 × 35 | oui | 198.95 EUR | oui |
| SteadyWin GIM6010-6, driver GDS6, 48 V | SteadyWin | — | 3 | 6.92 | 318 | — | Ø76 × 35 | oui | 198.95 EUR | oui |
| SteadyWin GIM6010-6, driver GDZ468H, 48 V | SteadyWin | — | 1.8 | 8.86 | 318 | — | Ø76 × 35 | oui | 210.95 EUR | oui |
| SteadyWin GIM6010-8, driver GDS68, 24 V | SteadyWin | — | 5 | 11 | 388 | — | Ø80 × 40 | oui | 100.95 EUR | oui |
| SteadyWin GIM6010-8, driver GDS68, 48 V | SteadyWin | — | 4.6 | 17.9 | 388 | — | Ø80 × 40 | oui | 100.95 EUR | oui |
| SteadyWin GIM6010-8, driver GDZ468H, 48 V | SteadyWin | — | 5.4 | 17.2 | 388 | — | Ø80 × 40 | oui | — | oui |
| SteadyWin GIM6010-36, driver GDS6, 48 V | SteadyWin | — | 18 | 41 | 574 | — | Ø76 × 56.5 | oui | 262.95 EUR | oui |
| SteadyWin GIM6010-36, driver GDZ468H, 48 V | SteadyWin | — | 17.4 | 51.5 | 574 | — | Ø76 × 56.5 | oui | 274.95 EUR | oui |
| SteadyWin GIM6010-48, driver GDS68, 24 V | SteadyWin | — | 30 | 66 | 777 | — | Ø80 × 67.5 | oui | — | oui |
| SteadyWin GIM6010-48, driver GDZ468, 24 V | SteadyWin | — | 27 | 55.9 | 777 | — | Ø80 × 67.5 | oui | 225.95 EUR | oui |
| SteadyWin GIM8108-6, driver GDS810, 48 V | SteadyWin | — | 5.46 | 18.2 | 567 | — | Ø96 × 41.5 | oui | 220.95 EUR | oui |
| SteadyWin GIM8108-8, driver GDS68, 48 V | SteadyWin | — | 7.5 | 22 | 396 | — | Ø92 × 55 | oui | 124.95 EUR | oui |
| SteadyWin GIM8108-8, driver GDZ468, 24 V | SteadyWin | — | 6.6 | 18.3 | 396 | — | Ø92 × 55 | oui | 168.95 EUR | oui |
| SteadyWin GIM8108-8, driver GDZ468H, 48 V | SteadyWin | — | 6.71 | 23.1 | 396 | — | Ø92 × 55 | oui | — | oui |
| SteadyWin GIM8108-9, driver GDS810, 48 V | SteadyWin | — | 8.19 | 27.4 | 567 | — | Ø96 × 41.5 | oui | 220.95 EUR | oui |
| SteadyWin GIM8108-36, driver GDS810, 48 V | SteadyWin | — | 32.8 | 110 | 760 | — | Ø96 × 57 | oui | 282.95 EUR | oui |
| SteadyWin GIM8108-48, driver GDS68, 48 V | SteadyWin | — | 45 | 132 | 780 | — | Ø92 × 73 | oui | — | oui |
| SteadyWin GIM8108-48, driver GDZ468, 36 V | SteadyWin | — | 45 | 132 | 780 | — | Ø92 × 73 | oui | — | oui |
| SteadyWin GIM8115-6, driver GDS810, 24 V | SteadyWin | — | 7.6 | 22 | 705 | — | Ø96 × 48.5 | oui | 251.95 EUR | oui |
| SteadyWin GIM8115-6, driver GDS810, 48 V | SteadyWin | — | 9.1 | 38 | 705 | — | Ø96 × 48.5 | oui | 251.95 EUR | oui |
| SteadyWin GIM8115-6, driver GDM810, 24 V | SteadyWin | — | 8.4 | 31 | 705 | — | Ø96 × 48.5 | oui | — | oui |
| SteadyWin GIM8115-6, driver GDM810, 48 V | SteadyWin | — | 7.5 | 36 | 705 | — | Ø96 × 48.5 | oui | — | oui |
| SteadyWin GIM8115-9, driver GDS810, 24 V | SteadyWin | — | 13 | 40 | 705 | — | Ø96 × 48.5 | oui | 251.95 EUR | oui |
| SteadyWin GIM8115-9, driver GDS810, 48 V | SteadyWin | — | 13.8 | 46 | 705 | — | Ø96 × 48.5 | oui | 251.95 EUR | oui |
| SteadyWin GIM8115-9, driver GDM810, 24 V | SteadyWin | — | 12.9 | 45 | 705 | — | Ø96 × 48.5 | oui | — | oui |
| SteadyWin GIM8115-9, driver GDM810, 48 V | SteadyWin | — | 13.5 | 39 | 705 | — | Ø96 × 48.5 | oui | — | oui |
| SteadyWin GIM8115-36, driver GDS810, 24 V | SteadyWin | — | 45.6 | 132 | 960 | — | Ø96 × 64 | oui | — | oui |
| SteadyWin GIM8115-36, driver GDS810, 48 V | SteadyWin | — | 54 | 228 | 960 | — | Ø96 × 64 | oui | — | oui |
| SteadyWin GIM8115-36, driver GDM810, 24 V | SteadyWin | — | 50.4 | 186 | 960 | — | Ø96 × 64 | oui | — | oui |
| SteadyWin GIM8115-36, driver GDM810, 48 V | SteadyWin | — | 45 | 216 | 960 | — | Ø96 × 64 | oui | — | oui |
| SteadyWin GIM10015-9, driver GDS810, 24 V | SteadyWin | — | 30 | 62.1 | 1.37e+03 | — | Ø122 × 57.5 | oui | — | oui |
| SteadyWin GIM10015-9, driver GDZ810, 48 V | SteadyWin | — | 20.5 | 112 | 1.37e+03 | — | Ø122 × 57.5 | oui | — | oui |
| SteadyWin GIM10015-10, driver non nommé, 48 V | SteadyWin | — | 25 | 45 | — | — | Ø120 × 50.6 | oui | — | oui |
| SteadyWin GIM4310-10 (driver GDZ34) | SteadyWin | 7.98 | 1.63 | 7.98 | 227 | 35.2 | Ø53 × 38 | oui | 169.95 EUR | oui |
| Unitree Brushless Digital Servo YS-342026-S288 (plastique) | Unitree | — | — | 0.6 | 19.5 | — | 20 × 34 × 26 | — | 29.0 USD | — |
| Unitree Brushless Digital Servo YS-342026-J288 (métal) | Unitree | — | — | 1.5 | — | — | — | — | 60.0 USD | — |
| Unitree GO-M8010-6 | Unitree | 23.7 | — | — | 530 | 44.7 | 96,5 × 92,5 × 42,3 | — | 700.0 EUR | oui |
| Unitree IM6014 (N6014B-12.6) | Unitree | 31.7 | — | — | 535 | 59.3 | Ø65 × 60 | — | 269.0 USD | — |
| Unitree A1 Motor | Unitree | 33.5 | — | — | 605 | 55.4 | — | — | 500.0 USD | — |
| Unitree B1 Motor (page constructeur « Super Robot Waterproof Joints B1-16 ») | Unitree | 140 | — | — | 1.74e+03 | 80.5 | — | — | 3000.0 USD | oui |
| Xiaomi CyberGear (référence) | xiaomi | 12 | 4 | — | 317 | 37.9 | Ø80,5 × 36,5 | — | 179.0 USD | — |

## Ce qui manque

Nombre d'actionneurs sans la donnée, sur 211 :

| Donnée | Manquante pour | Lesquels |
| --- | ---: | --- |
| couple en pointe | 87 | gim3505_8_gds34_24v, gim3505_8_gdz34_24v, gim3505_9_driver_inconnu_24v, gim3505_36_driver_inconnu_24v, gim3510_8_gdz34_24v, gim3510_64_gdz34_24v, gim4305_10_gdz34_24v, gim4305_10_gds34_24v, gim4310_10_gds34_24v, gim4310_36_gdz34_24v, gim4310_36_gds34_24v, gim4310_40_gdz4_40_24v, … |
| couple continu | 37 | xm430_w210, xm430_w350, unitree_go_m8010_6, unitree_a1_motor, unitree_b1_motor, unitree_im6014, unitree_ys_342026_s288, unitree_ys_342026_j288, xl330_m077, xl330_m288, xc330_m181, xc330_m288, … |
| couple au blocage | 89 | ak70_10, dm_j4310, ak45_10_v3, dm_j8006, dm_j4340, dm_j8009, ak80_9_v3, ak10_9_v3, ak70_9_v3, dm_j4310_48v, cybergear, ak40_10_v3, … |
| masse | 4 | dm_j8520p, dm_h3510, gim10015_10_driver_inconnu_48v, unitree_ys_342026_j288 |
| cotes (Ø × L) | 23 | edulite05, xm430_w210, dm_j8006, dm_j4340, dm_j8009, ak80_9_v3, ak10_9_v3, ak70_9_v3, x4_36, dm_j4310_48v, htdw_5036_02_dne, htdw_6036_02_dne, … |
| motifs de fixation | 73 | xm430_w210, htdw_5047_36, cybergear, xm430_w350, gim3505_8_gds34_24v, gim3505_8_gdz34_24v, gim3505_9_driver_inconnu_24v, gim3505_36_driver_inconnu_24v, gim3510_8_gdz34_24v, gim3510_64_gdz34_24v, gim4305_10_gdz34_24v, gim4305_10_gds34_24v, … |
| STEP officiel | 37 | sts3250, htdw_5047_36, cybergear, dm_j4340_v10, dm_j4340p_v10, dm_j8009p_v11, x2_3, x2_7_l, x5_50, rh_14_50, rh_17_50, rh_20_50, … |
| prix | 72 | dm_j4310_v11, dm_j4340_v10, dm_j4340p_v10, dm_j4340p_v11, dm_j6216l, dm_j6216p, dm_j6248p, dm_j8009p, dm_j8009p_v11, dm_j8520p, dm_j10010, dm_j10422p, … |
| disponibilité CH/UE | 79 | sts3250, ak80_9_v3, ak70_9_v3, htdw_5047_36, htdw_5036_02_dne, htdw_6036_02_dne, cybergear, ak40_10_v3, ak60_39_v3, ak10_9_v2, ak45_36, ak45_36_v3, … |
| garantie | 115 | dm_j4310, gim4310_10, dm_j8006, dm_j4340, dm_j8009, dm_j4310_48v, htdw_4438_30, htdw_5047_36, htdw_5036_02_dne, htdw_6036_02_dne, cybergear, dm_j3507, … |
