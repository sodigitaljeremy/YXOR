Les chiffres ci-dessous viennent des fiches fabricants, des pages produits et des articles publiés consultés en octobre 2026. Une case « non trouvé » signifie que la source consultée ne la donne pas. Les TOPS NVIDIA (INT8 sparse, ou FP4 sparse sur Thor) et les TOPS Hailo (INT8 ou INT4) ne sont pas comparables.

## 1. Résumé

Les RobStride RS00, RS02 à RS06 acceptent jusqu’à 60 V, avec un nominal à 48 V. Le RS01 s’arrête à 48 V et se nominalise à 36 V. Un pack 12S lithium-ion (43,2 V nominal, 50,4 V plein) alimente les 48 V sans dépasser 60 V. Un 13S (54,6 V plein), comme sur le Unitree G1, reste sous 60 V mais laisse peu de marge à la régénération. Un 14S plein à 58,8 V est trop proche de la butée.

Les Feetech STS3215 7,4 V (ST-3215-C001) sont spécifiés 4 à 7,4 V, protection au-dessus de 8 V. La variante 12 V (C018) accepte 6 à 12 V. Il faut un rail séparé, pas le bus 48 V.

Sous la directive basse tension 2014/35/UE, le seuil d’application commence à 75 V DC. La très basse tension IEC 61140 reste de 120 V DC. Le plafond utile ici est donc le 60 V des actionneurs, pas la norme électrique.

Pour 10 kg, un pack 6S à 12S sur cellules 21700 (Molicel P50B, Samsung 50S) avec BMS et boîtier est le meilleur compromis. Pour 35 kg, un pack sur mesure 12S ou 13S, BMS industriel et coupure d’urgence. Les batteries d’outillage 18 V ne conviennent pas telles quelles aux RobStride 48 V.

La marche ONNX à 50 Hz tient sur un Orin Nano Super ou un Raspberry Pi 5. La vision et la voix locales demandent un Orin NX 16 Go. Un modèle de langage local utile commence à l’AGX Orin 64 Go. Thor (T4000/T5000) est en vente, mais en FP4 sparse et à 40–130 W.

À 1 Mbit/s en CAN 2.0 étendu, 27 axes à 500 Hz en commande et retour demandent environ 6 bus. Quatre bus, un par membre, suffisent si l’on accepte une charge plus faible ou du CAN-FD.

## 2. Tensions

| Actionneur | Tension nominale | Plage | Protection surtension | Source |
|---|---|---|---|---|
| RobStride RS00 | 48 V | 24–60 V | 60 V max. driver | Manuel RS00 et README GitHub, spec 13 juil. 2026  |
| RS01 | 36 V | 24–48 V | non trouvé au-delà de 48 V | README RobStride, spec 13 juil. 2026  |
| RS02, RS02-IP67 | 48 V | 24–60 V | 60 V | idem  |
| RS03, RS04, RS05, RS06 | 48 V | 15–60 V | 60 V | idem  |
| Feetech STS3215 7,4 V (C001) | 6 / 7,4 V | entrée nominale 4–7,4 V | > 8 V | PDF Feetech hébergé Seeed  |
| STS3215 12 V (C018) | 12 V | 6–12 V | > 14 V | PDF Feetech, 28 avr. 2024  |
| STS3032 | 6 V typique | 4–7,4 V | non trouvé | Fiche distributeur DiGi  |
| SCS2332 | 6 V | 4–8,4 V indiqué | > 9 V ou < 4 V | PDF produit Feetech  |

Le bus RobStride documenté est du CAN 2.0 à 1 Mbit/s, trames étendues. Le CAN-FD n’est pas confirmé dans les manuels consultés. 

Packs compatibles, cellule NMC/NCA 4,2 V pleine :

- 10S : 36,0 / 42,0 V. Tient sur RS01. Sous-alimente un 48 V.
- 11S : 39,6 / 46,2 V. Dernier pack sûr pour un RS01.
- 12S : 43,2 / 50,4 V. Cible pour RS00 et RS02–RS06.
- 13S : 46,8 / 54,6 V. Choix Unitree G1. Encore sous 60 V.
- 14S : 50,4 / 58,8 V. Marge de 1,2 V, insuffisante si le moteur renvoie du courant.
- 15S : 54,0 / 63,0 V. Interdit sur ces RobStride.

LiFePO4, 3,65 V pleine : 15S = 48,0 / 54,75 V. 16S = 51,2 / 58,4 V. Un Feetech 7,4 V se nourrit par un convertisseur 6 à 7,4 V. Un 2S (8,4 V) déclenche la protection 8 V du C001.

La directive 2014/35/UE vise les équipements de 75 à 1 500 V DC. L’ELV IEC 61140 est à 50 V AC / 120 V DC. Le 60 V est la limite fabricant, pas le seuil légal de sécurité électrique.

## 3. Batteries

| Produit | Famille | Tension | Wh | Décharge continu / pointe | Masse | Volume | Wh/kg | Wh/L | BMS | UN 38.3 | Prix | Revendeur CH/UE | Source |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Molicel INR21700-P50B | 21700 NMC | 3,6 V (2,5–4,2) | 18 | 60 A, coupure 80 °C / ~90 A 3 s (revendeur) | ~70 g | 21,55 × 70,15 mm | 265 fabricant, 257 base Voltt | 714 fabricant | non | non trouvé | 13,99 € TTC, 10 sept. 2026 | ERC Market (UE) | Fiche Molicel  |
| Samsung INR21700-50S | 21700 NMC | 3,6 V | 18 typ. | 25 A sans coupure thermique, 45 A avec coupure 80 °C. Revendeur : 35 A | 72 g max | Ø 21,25 × 70,62 mm | ~250 | non trouvé | non | non trouvé | 4,50 € TTC, 6 oct. 2026 | thebatteryshop.eu | Spec Samsung SDI nov. 2019  |
| Murata US18650VTC6 | 18650 NMC | 3,6 V | 11,23 | 30 A / pointe non trouvée | 46,6 g | 17,19 cm³ | 241 | ~653 | non | non trouvé | non trouvé | non trouvé | Base Voltt / About:Energy  |
| Tattu 6S 22 000 mAh 25C | LiPo drone | 22,2 V (6S) | 488 | 25C soit 550 A annoncé / 50C annoncé | 2 429–2 490 g | 207 × 91 × 64 mm | ~196 | ~420 | non, équilibreur JST | non trouvé | 246 USD, page Foxtech | Foxtech FPV | Fiche vendeur  |
| Makita BL1860B | Outillage 18 V, 5S Li-ion | 18 V | 108 | non publié | 0,66 kg | 110 mm de long | ~164 | non trouvé | oui, Star Protection | non trouvé. 108 Wh, donc au-dessus du seuil postal 100 Wh | non trouvé | Makita, Galaxus, Distrelec | Makita Australie  |
| DeWalt DCB546 FlexVolt | 18/54 V, 15 cellules | 18 V (6 Ah) ou 54 V (2 Ah) | 108 | non publié | 1,0–1,06 kg | 123 × 82 × 91 mm | ~102 | ~117 | oui, jauge | transport cap = 3 × 36 Wh, revendiqué hors classe 9 | non trouvé | DeWalt, revendeurs UE | Fiche DeWalt et Power Tool World  |
| EVE LF280K | LiFePO4 prismatique | 3,2 V (2,5–3,65) | 896 | 140 A (0,5C) / 280 A (1C, 25 °C) | 5 490 g | 173,7 × 71,7 × 204,6 mm | 163 | ~350 | non | non trouvé sur la fiche vendeur | 235 € les 4 cellules, juil. 2025 | paircycle (DE) | Fiche vendeur  |

Les taux C des LiPo sont des annonces fabricant. Les essais indépendants donnent souvent moins en continu. Les batteries d’outillage ont un BMS et un boîtier antichoc, mais le courant continu n’est pas publié. Des adaptateurs XT60 existent pour une seule batterie. Mettre deux ou trois packs en série contourne le BMS, empêche l’équilibrage et peut dépasser 60 V en 3 × 18 V. Ce n’est pas une architecture recommandée.

La Poste suisse, manuel marchandises dangereuses d’août 2026, autorise les lithium-ion jusqu’à 100 Wh en colis national sous le service marchandises dangereuses. Au-dessus de 100 Wh, les batteries d’e-bike et packs équivalents sont interdites au colis. Les batteries endommagées sont interdites. À l’international, seules les batteries installées dans l’appareil passent, dans la limite UPU de 4 cellules ou 2 batteries. 

## 4. Calculateurs

| Produit | Cotes module / porteuse | Masse | W repos / typique / max | CPU | Accélérateur | TOPS (type) | Mémoire | CAN intégré | Prix | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| Orin Nano Super, kit | module 69,6 × 45 mm. Kit 100 × 79 × 21 mm | 0,176 kg sans emballage | non trouvé / mode 7–25 W / 25 W | 6 cœurs A78AE, 1,7 GHz | Ampere 1024 CUDA, 32 Tensor | 67 INT8 sparse | 8 Go LPDDR5, 102 Go/s | 1 contrôleur MTTCAN sur la puce. Broches J17 sur la carte de référence | 249 USD | NVIDIA, fiche SKU déc. 2024  |
| Orin Nano 4 Go | même format | non trouvé | 7–15 W, Super jusqu’à 25 W | 6 cœurs A78AE | 512 CUDA, 16 Tensor | 34 INT8 sparse | 4 Go | 1, comme ci-dessus | non trouvé | Page NVIDIA Orin  |
| Orin NX 8 / 16 Go | 69,6 × 45 mm, carte tierce | non trouvé | 10–40 W | 8 cœurs A78AE | 1024 CUDA, 32 Tensor | 117 / 157 INT8 sparse | 8 / 16 Go | 1 MTTCAN | non trouvé | Guide CAN NVIDIA r36.5.2  |
| AGX Orin 32 Go | kit type H01 107 × 106 × 71 mm | non trouvé | 15–40 W | 8 cœurs A78AE | 1792 CUDA, 56 Tensor | 200 INT8 sparse | 32 Go, 204,8 Go/s | 2 | 1 449 USD HT, Seeed, 24 août 2026 | Seeed  |
| AGX Orin 64 Go, kit | 110 × 110 × 71,65 mm | non trouvé | 15–60 W | 12 cœurs A78AE | 2048 CUDA, 64 Tensor | 275 INT8 sparse, 138 dense | 64 Go | 2, header 40 broches | 3 499 USD | NVIDIA Marketplace et datasheet kit  |
| AGX Orin Industrial | même module | non trouvé | 15–60 W | 12 cœurs | 2048 CUDA | 248 INT8 sparse | 64 Go | 2 | non trouvé | Page NVIDIA  |
| Jetson T4000 (Thor) | module 100 × 87 mm | non trouvé | 40 W à non trouvé | 12 cœurs Neoverse-V3AE | Blackwell 1536 CUDA | 1200 TFLOPS FP4 sparse | 64 Go LPDDR5X | 4 CAN sur la famille Thor | non trouvé | Page produit NVIDIA, reprise sept. 2026  |
| AGX Thor kit / T5000 | 243 × 112 × 57 mm | non trouvé | 40–130 W | 14 cœurs Neoverse-V3AE, 2,6 GHz | Blackwell 2560 CUDA | 2070 TFLOPS FP4 sparse. 1035 FP8 sur fiche Seeed | 128 Go, 273 Go/s | 4 CAN module. 2 headers CAN sur le kit | 5 899 USD HT, Seeed, 2 sept. 2026 | Spec kit et Seeed  |
| Orin Nano 2 | annoncé, même format | non trouvé | 15 W annoncé | 8 cœurs Arm | non détaillé | 78, type non précisé | 8 Go | non trouvé | non en vente. Attendu S1 2027 | Annonce NVIDIA 25 août 2026  |
| Raspberry Pi 5 + AI HAT+ | Pi 5 : non trouvé ici. HAT au format Pi | non trouvé | non trouvé / Hailo-8 ~2,5 W typ. / non trouvé | 4 cœurs A76 | Hailo-8L ou Hailo-8 | 13 ou 26 TOPS INT8 | RAM du Pi 5 | non. SPI ou USB | non trouvé | Doc Raspberry Pi  |
| Pi 5 + AI HAT+ 2 | HAT Pi 5 | non trouvé | Hailo-10H 2,5 W typ. | 4 cœurs A76 | Hailo-10H | 40 TOPS INT4, ~20 INT8 | 8 Go sur le HAT | non | 130 USD, source secondaire | Annonce Pi 15 janv. 2026  |

L’AI Kit (Hailo-8L, 13 TOPS) n’est plus produit. CUDA, TensorRT et ONNX Runtime sont sur JetPack pour Orin. Thor passe par JetPack 7, pile distincte. Hailo a son compilateur. Pas de CUDA. ROS 2 tourne sur les deux, sans être un chiffre de fiche.

Disponibilité suisse : kits Orin chez Distrelec, Mouser et Farnell. Le kit Nano Super est listé en Allemagne dès 479 € au 7 oct. 2026, fiche Geizhals qui mélange le 4 Go. 

## 5. Niveaux d’IA embarquée

| Niveau | Minimum qui suffit | Exemple publié | Limite |
|---|---|---|---|
| (a) Marche ONNX, 50 Hz | Orin Nano Super, ou Pi 5 seul. ToddlerBot fait tourner la politique sur le CPU de l’Orin NX | ToddlerBot, politique (512, 256, 128), 50 Hz, CPU de l’Orin NX 16 Go  | Un MLP de marche est petit. Le goulot est le bus et la latence, pas les TOPS |
| (b) + vision, détection et suivi | Orin NX 16 Go | ToddlerBot : Foundation Stereo à 10 Hz sur Orin NX 16 Go . Pi 5 + Hailo-8 tient YOLO, pas une stéréo lourde | Hailo-8 : 26 TOPS INT8, vision seulement |
| (c) + voix locale | Orin NX 16 Go | Unitree G1 : Orin NX 16 Go, 4 micros. Booster T1 : AGX Orin 32 Go, 6 micros  | Whisper small en INT8 tient sur NX. Un gros modèle de voix sature le 8 Go du Nano |
| (d) LLM local | AGX Orin 64 Go pour 7B–8B quantifié. HAT+ 2 seulement pour 1–1,5 milliard | Hailo-10H : Qwen2 1,5B à 9,45 tok/s, Llama 3.2 1B vers 6–7 tok/s  | 7B en 4 bits demande ~5 Go de poids plus le cache. Le Nano 8 Go est trop juste. Thor n’a pas de tok/s publié ici |

## 6. Cartes de bus et calcul CAN

| Carte | Canaux | Débit | Cotes | Masse | Prix | Linux | Source |
|---|---|---|---|---|---|---|---|
| CANable 2.0 | 1 | CAN 2.0 jusqu’à 1 Mbit/s. FD en bêta slcan | non trouvé | non trouvé | 35 USD | slcand, SocketCAN | Openlight Labs  |
| Innomaker USB2CAN-X2 | 2, isolés 3 kV | 20 kbit/s–1 Mbit/s, CAN 2.0 | non trouvé | non trouvé | 89 USD, août 2026 | SocketCAN natif | Innomaker  |
| Waveshare USB-CAN-FD-B | 2, isolés 3 kV | 100 kbit/s–5 Mbit/s, FD | 104 × 70 × 25 mm | non trouvé | non trouvé | API propriétaire, pas SocketCAN. 20 000 trames/s reçues, 5 000 envoyées par canal | Wiki Waveshare  |
| MTTCAN Jetson | 1 sur NX/Nano, 2 sur AGX Orin, 4 annoncés sur Thor | classique jusqu’à 1 Mbit/s, FD data jusqu’à 15 Mbit/s | intégré | 0 | inclus | SocketCAN, driver mttcan | Guide NVIDIA r36.5.2  |
| Feetech bus TTL | 1 bus demi-duplex, ID 0–253 | 38 400 bit/s à 1 Mbit/s | adaptateur USB FE-URT-1 | non trouvé | non trouvé | SDK Feetech, utilisé par LeRobot | Fiche STS3215  |

Calcul pour 27 axes à 500 Hz. Une trame étendue de 8 octets, avec bourrage et espace intertrame, compte environ 150 bits. À 1 Mbit/s, le plafond est de 6 667 trames/s. À 70 % de charge utile, il reste environ 4 670 trames/s.

- Commande seule : 27 × 500 = 13 500 trames/s, soit 13 500 / 4 670 ≈ 2,9 bus. Trois bus au minimum, quatre en pratique.
- Commande et retour : 27 000 trames/s, soit 5,8 bus. Six au minimum, huit si l’on groupe par membre.

Le CAN-FD à 5 Mbit/s en phase data divise ce besoin par environ trois, à condition que les moteurs le supportent. Les manuels consultés ne le confirment pas. Berkeley Humanoid Lite répartit 22 axes sur 4 bus CAN à 1 Mbit/s, un par membre. 

## 7. Robots publiés

ToddlerBot, Stanford, CoRL 2025 : 30 degrés de liberté, Jetson Orin NX 16 Go, politique à 50 Hz sur le CPU. Batterie 4S LiPo 2 000 mAh, 215 g, ou 4 cellules 21700 de 5 000 mAh, 330 g. Bus 14–19 V, moteurs en TTL 12 V, arrêt d’urgence sur le rail moteurs. 

Berkeley Humanoid Lite : 0,8 m, 16 kg, 22 degrés de liberté, 4 bus CAN 2.0 à 1 Mbit/s, adaptateur USB-CAN. Politique ONNX à 25 Hz. Calculateur et tension de batterie non trouvés dans les pages lues. La ligne compute du BOM secondaire est à 129 USD. 

LeRobot : le robot documenté est le bras SO-101, 6 STS3215, bus TTL, 5 V pour la variante 7,4 V ou 12 V pour la variante 12 V. Pas d’humanoïde bipède sourcé ici. 

BRIDGE : aucun humanoïde publié sous ce nom n’a été vérifié dans les sources consultées.

Booster T1 : 1,18 m, environ 30 kg, 23 degrés de liberté, AGX Orin 200 TOPS (module 32 Go), option Intel i7-1370P, batterie 10,5 Ah, tension non trouvée, 2 h de marche. 

Unitree G1 : batterie 13S, 46,8 V nominal, 54,6 V de charge max, 9 000 mAh, 421,2 Wh, 120 × 80 × 182 mm, BMS Unitree, coupure à 39 V. Calculateur de développement Jetson Orin NX 16 Go. Sortie VBAT 58 V / 5 A sur la carte. 

## 8. Recommandations

Pour le YXOR Lab, 10 kg et 27 axes. Pack 12S de cellules P50B ou 50S, 2P, soit environ 430 Wh et 1,7 kg de cellules, BMS avec coupure sur choc et surintensité, boîtier aluminium ventilé séparé des articulations. Rail Feetech 7,4 V par convertisseur isolé. Calculateur : Orin Nano Super pour la marche, Orin NX 16 Go si caméra. Quatre bus CAN, un par membre, à 1 Mbit/s. Arrêt d’urgence qui ouvre le rail puissance, pas seulement un arrêt logiciel.

Pour le YXOR final, 35–40 kg. Même 12S ou un 13S si tous les moteurs acceptent 54,6 V, donc pas de RS01. Viser 600–900 Wh. Éviter le LiPo souple sans caisson. Un LiFePO4 15S est plus stable à la chute mais plus lourd, environ 160 Wh/kg contre 250. AGX Orin 64 Go si un modèle de langage local est requis. Thor seulement si le budget thermique de 40 W minimum est acceptable. Coupure d’urgence câblée, deux contacteurs, BMS avec détection de choc.

## 9. Registre des sources

Fiches fabricant : manuels RobStride (GitHub, spec 13 juil. 2026), PDF STS3215 Seeed et Feetech C018, Molicel P50B, Samsung SDI 50S (nov. 2019), NVIDIA Jetson (pages produit, datasheet kit, guide CAN r36.5.2), Raspberry Pi AI HAT+, Unitree G1 batterie, Booster T1, DeWalt DCB546, Makita BL1860B.

Articles : ToddlerBot, arXiv 2502.00893. Berkeley Humanoid Lite, documentation projet.

Revendeurs, à distinguer des fiches : ERC Market, thebatteryshop.eu, Foxtech, paircycle, Seeed, Openlight, Innomaker, Waveshare, Geizhals.

Réglementation : Poste suisse, manuel marchandises dangereuses, août 2026. Directive 2014/35/UE et IEC 61140 pour les seuils de tension.