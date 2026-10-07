Voici l’étude arrêtée au **7 octobre 2026**. J’ai privilégié, dans l’ordre, les documents fabricants, les documentations officielles de projets, puis les revendeurs ; lorsqu’une donnée n’est pas publiée de façon vérifiable, je mets **« non trouvé »** plutôt que de l’estimer.

## 1. Résumé en 10 lignes

1. Pour une architecture commune aux RobStride RS00/02/03/04/05/06, le meilleur compromis est une batterie Li-ion **13S : 46,8 V nominal / 54,6 V pleine charge** ; elle laisse une marge utile sous la limite RobStride de 60 V. Le **RS01 est l’exception**, limité à 48 V, et impose plutôt 11S ou un rail dédié. [GitHub](https://github.com/RobStride/Product_Information/?utm_source=chatgpt.com)  
2. Un pack **14S Li-ion atteint 58,8 V chargé** : électriquement admissible pour les modèles 60 V, mais trop proche de 60 V pour absorber confortablement la régénération et les surtensions. Je ne le choisirais pas pour YXOR.  
3. Les Feetech doivent être alimentés par des rails DC/DC séparés : selon le modèle, environ **6 V, 7,4–8,4 V ou 12 V** ; la famille STS n’a pas une tension unique.  
4. Pour YXOR Lab, des **21700 haute puissance**, particulièrement Molicel P45B, sont plus cohérentes que des batteries d’outillage ou un gros LiFePO4 : 4,5 Ah, 45 A, 3,6 V, avec une densité annoncée de 242 Wh/kg. [Molicel](https://www.molicel.com/product/inr-21700-p45b/?utm_source=chatgpt.com)  
5. Les LiPo RC offrent un rapport puissance/masse remarquable, mais leur absence habituelle de BMS intégré et leur vulnérabilité mécanique les rendent moins attrayantes dans un humanoïde qui tombe.  
6. Les batteries 18 V d’outillage sont très intéressantes pour les prototypes, bancs et sous-systèmes, mais leur mise en série et leurs mécanismes de protection propriétaires en font un choix médiocre pour le pack principal d’un humanoïde final.  
7. Pour le calcul embarqué, **Jetson Orin Nano Super 8 GB** est déjà largement suffisant pour marche + vision + voix ; **Orin NX 16 GB** est, à mon avis, le meilleur point d’équilibre pour YXOR Lab et constitue aussi un excellent calculateur temps réel/vision pour le grand YXOR. [NVIDIA Developer](https://developer.nvidia.com/blog/?p=93942\&utm_source=chatgpt.com)  
8. Pour un LLM local plus ambitieux sur le grand robot, AGX Orin 64 GB est plus pertinent ; Thor est extrêmement puissant, mais ses **2070 TFLOPS FP4 sparse ne sont absolument pas comparables aux 275 TOPS INT8 d’Orin**. [NVIDIA](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson/back-to-school/?utm_source=chatgpt.com)  
9. Les RobStride actuels doivent être dimensionnés comme **CAN 2.0 à 1 Mbit/s** tant que RobStride ne documente pas explicitement CAN-FD pour le modèle/firmware considéré. À 27 axes × 500 Hz avec commande + feedback, le calcul conduit à environ **4 bus au minimum absolu, 6 bus recommandés**. [GitHub](https://github.com/cloudhan/robstride_docs/blob/main/RS06.md?utm_source=chatgpt.com)  
10. Pour les deux robots, je recommande une architecture à **batterie centrale protégée mécaniquement dans le torse, BMS + fusible + contacteur + précharge + arrêt d’urgence matériel + gestion de l’énergie régénérative**, avec des rails séparés moteurs / compute / servos.

---

# 2. Tensions

## 2.1 RobStride

La fiche officielle RobStride datée du **13 juillet 2026**, toujours publiée dans le dépôt constructeur en octobre 2026, donne ceci. [GitHub](https://github.com/RobStride/Product_Information/?utm_source=chatgpt.com)

| Actionneur | Tension nominale | Plage constructeur | Li-ion envisageable | Commentaire |
|---|---:|---:|---|---|
| RS00 | 48 V | **24–60 V** | 7S à 14S théoriquement ; **12S/13S préférables** | 13S = 46,8/54,6 V |
| RS01 | 36 V | **24–48 V** | jusqu’à **11S** | 12S = 50,4 V chargé → hors spécification |
| RS02 | 48 V | **24–60 V** | idem RS00 | 13S recommandé |
| RS02-IP67 | 48 V | **24–60 V** | idem |  |
| RS03 | 48 V | **15–60 V** | 5S à 14S théoriquement | 13S recommandé |
| RS04 | 48 V | **15–60 V** | idem |  |
| RS05 | 48 V | **15–60 V** | idem |  |
| RS06 | 48 V | **15–60 V** | idem | manuel : max 60 V |

Le manuel RS06 donne en outre **1 Mbit/s CAN**, une tension de travail 48 V et un maximum admissible de 60 V. [GitHub](https://github.com/cloudhan/robstride_docs/blob/main/RS06.md?utm_source=chatgpt.com)

### Comparaison des packs Li-ion

| Pack | Nominal | Pleine charge | RobStride 60 V | Mon jugement |
|---|---:|---:|---|---|
| 11S | 39,6 V | 46,2 V | Oui | nécessaire si RS01 sur le même rail |
| 12S | 43,2 V | 50,4 V | Oui | très confortable |
| **13S** | **46,8 V** | **54,6 V** | **Oui** | **meilleur compromis** |
| 14S | 50,4 V | 58,8 V | Oui nominalement | trop peu de marge avant 60 V |
| 15S | 54,0 V | 63,0 V | **Non** | à proscrire |

Les tensions ci-dessus découlent des tensions usuelles **3,6 V nominal / 4,2 V pleine charge par cellule** des cellules Li-ion citées plus bas.

### Pourquoi je préfère 13S à 14S

Le problème n’est pas uniquement la tension de batterie statique. Un humanoïde possède des actionneurs réversibles : lors d’une décélération, d’une descente ou d’un impact, ils peuvent **régénérer de l’énergie vers le bus DC**.

Avec :

- 13S → 54,6 V chargé : marge de **5,4 V** jusqu’à 60 V ;
- 14S → 58,8 V chargé : marge de seulement **1,2 V**.

RobStride publie d’ailleurs un **discharge module / module de décharge** dans sa gamme d’accessoires, signe que la gestion de l’énergie régénérative fait bien partie de l’architecture prévue. [GitHub](https://github.com/RobStride/Product_Information/?utm_source=chatgpt.com)

Pour YXOR, je prévoirais donc **13S + absorption/résistance de freinage ou circuit de clamp**, et non simplement un BMS.

---

## 2.2 Feetech

La tension dépend fortement du SKU.

| Servo | Tension documentée | Alimentation YXOR conseillée |
|---|---:|---|
| SCS0009 | **4–7,4 V** | rail 6 V |
| SCS15-C022 | **4–8,4 V** | rail 7,4–8,0 V |
| STS3032 | **4,8–6 V** | rail 6 V |
| STS3215 7,4 V | variante 7,4 V | rail adapté au SKU |
| STS3215 12 V | jusqu’à env. **12,6 V** selon version | rail 12 V |

Feetech documente par exemple SCS0009 jusqu’à 7,4 V, SCS15 jusqu’à 8,4 V et STS3032 à 4,8–6 V. Les STS3215 existent notamment en variantes 7,4 V et 12 V. [Feetech](https://www.feetechrc.com/6v-23kg-serial-bus-steering-gear_65522.html?utm_source=chatgpt.com)

**Conclusion : ne jamais raccorder directement les Feetech au bus 46–55 V.**

Je ferais :

**13S batterie →**
- bus puissance RobStride 46,8 V nominal ;
- DC/DC 12 V ;
- DC/DC 7,4–8 V ;
- éventuellement DC/DC 6 V ;
- rail calculateur séparé.

---

## 2.3 À propos des « 60 V de sécurité »

Il faut être prudent avec le raccourci « <60 V = sans danger ». Les seuils SELV/PELV varient selon :

- AC ou DC ;
- conditions sèches/humides ;
- accessibilité des parties conductrices ;
- norme produit applicable.

Pour YXOR, **rester en dessous de 60 V DC est néanmoins une excellente décision d’architecture**, notamment parce que RobStride a lui-même fixé 60 V comme maximum pour la majorité de sa gamme. Cela ne dispense absolument pas de protection contre court-circuit, arc, incendie ou courant de centaines d’ampères.

---

# 3. Batteries

Quelques valeurs de densité ci-dessous sont des **calculs** à partir des dimensions, masses et énergies publiées ; elles sont identifiées comme telles.

## 3.1 Cellules cylindriques et packs représentatifs

| Produit | Famille / chimie | Tension / capacité | Wh | Décharge continue / pointe | Masse | Volume | Wh/kg | Wh/L | BMS | UN 38.3 | Prix / revendeur | Source |
|---|---|---:|---:|---|---:|---:|---:|---:|---|---|---|---|
| **Molicel INR-21700-P45B** | 21700 Li-ion INR | 3,6 V / 4,5 Ah | 16,2 | **45 A** / non trouvé | ≤69 g | cyl. Ø21,6×70,2 mm | fabricant **242** | fabricant **643** | non | certificat disponible | prix courant UE variable ; NKON distribue le modèle | fabricant | :chatgpt-content-reference{index="9"} |
| Murata US21700VTC6A | 21700 NCA | 3,6 V / 4,1 Ah | 14,76 | **40 A** / non trouvé | 67,5 g | Ø21,55×70 mm max | ≈219 calculé | ≈578 calculé | non | documents transport fabricant disponibles | revendeur 2026 : non trouvé dans les résultats vérifiés | fabricant | :chatgpt-content-reference{index="10"} |
| Murata US18650VTC6 | 18650 NCA | 3,6 V / 3,12 Ah | 11,23 | **30 A** / non trouvé | 46,6 g | ≈Ø18×65 mm | ≈241 | ≈679 | non | fabricant publie documentation transport | non trouvé | fabricant | :chatgpt-content-reference{index="11"} |
| Samsung INR18650-30Q | 18650 NMC/NCA selon documentation commerciale | 3,6 V / 3 Ah | 10,8 | **15 A** / non trouvé | ≈46 g | ≈18,3×64,9 mm | ≈235 | ≈633 | non | document UN38.3 proposé par revendeur | **≈€2,65**, NKON, relevé 2026 | revendeur | données NKON relevées lors de la recherche |
| LG INR21700-M50LT | 21700 Li-ion énergie | ≈3,69 V / 5 Ah | ≈18,45 | ≈14,4 A / non trouvé | ≈68,5 g | ≈21,44×70,8 mm | ≈269 | ≈722 | non | non trouvé ici | NKON : modèle référencé ; prix actuel non trouvé | revendeur |
| Tattu 6S 10 Ah 30C | LiPo pouch RC | **22,2 V / 10 Ah** | **222** | **300 A théorique à 30C** / pointe non trouvée | **1357 g** | 175×65×58 mm | ≈164 | ≈336 | non trouvé | non trouvé sur page produit | **€214,99**, Tattu EU | fabricant/revendeur |
| Tattu 6S 12 Ah 30C | LiPo | 22,2 V / 12 Ah | 266,4 | 360 A théorique à 30C | 1544 g | 192×72×54 mm | ≈173 | ≈357 | non trouvé | non trouvé | **€239,99** | fabricant/revendeur |
| Tattu 6S 16 Ah 30C | LiPo | 22,2 V / 16 Ah | 355,2 | 480 A théorique à 30C | 1974 g | 190×76×65 mm | ≈180 | ≈378 | non trouvé | non trouvé | **€309,99** | fabricant/revendeur |

Pour les Tattu, le courant en ampères résulte simplement de `capacité Ah × 30C`; il ne faut **pas** interpréter cela comme une mesure indépendante garantissant qu’un pack peut réellement soutenir ce courant thermiquement pendant une longue durée. Les valeurs C du monde RC sont notoirement difficiles à comparer entre fabricants.

### Mon classement pour YXOR

Pour une batterie principale de humanoïde :

**P45B > VTC6A > LiPo RC > cellules énergie type M50LT**, si l’objectif principal est le rapport puissance/masse.

La P45B est particulièrement intéressante parce que Molicel publie directement **45 A et 242 Wh/kg / 643 Wh/L**, plutôt que de devoir reconstruire ces données depuis un revendeur. [Molicel](https://www.molicel.com/product/inr-21700-p45b/?utm_source=chatgpt.com)

---

# 3.2 Batteries d’outillage

| Produit | Chimie | Tension | Wh | Décharge cont./pointe | Masse | Dimensions | Wh/kg | Wh/L | BMS | UN38.3 | Prix / CH-UE |
|---|---|---:|---:|---|---:|---|---:|---:|---|---|---|
| Makita BL1860B | Li-ion | 18 V, 6 Ah | 108 | **non trouvé** | ≈700 g | ≈113×75×62 mm | ≈154 | ≈206 | électronique interne présente, architecture exacte non publiée | non trouvé | Galaxus CH ; prix capturé : non trouvé |
| DeWalt DCB184 | Li-ion | 18 V, 5 Ah | 90 | **non trouvé** | ≈620 g | non trouvé de façon certaine pour la révision standard | ≈145 | non trouvé | protection pack/outil ; détails non trouvés | non trouvé | Galaxus CH |
| Bosch ProCORE18V 8.0Ah | Li-ion | 18 V, 8 Ah | 144 | **non trouvé** | **955 g** | **77×117×70 mm** | ≈151 | ≈228 | **Battery Management System annoncé** | non trouvé | distribution Bosch CH/UE ; prix actuel non trouvé |

Bosch documente explicitement sa gestion de batterie et les dimensions/poids du ProCORE18V 8 Ah. Les courants de décharge numériques réels ne sont en revanche pas publiés comme une spécification utilisateur comparable à celle d’une P45B ; je ne les déduis donc pas des claims marketing de puissance.

### Peut-on les utiliser en robotique ?

**Oui, mais je distinguerais trois usages.**

Très bon :
- banc d’essai ;
- robot d’apprentissage ;
- rail calculateur ;
- prototype rapidement échangeable ;
- outils et accessoires embarqués.

Moyen :
- petit robot roulant ;
- manipulateur relativement lent.

Peu intéressant pour YXOR final :
- architecture de traction principale haute puissance ;
- mise en série non officiellement prévue ;
- régénération provenant d’actionneurs ;
- accès aux protections internes parfois propriétaire ;
- capacité à absorber un courant de recharge régénératif rarement spécifiée.

Des **adaptateurs mécaniques électriques Makita/DeWalt/Bosch/Milwaukee → fils ou XT60/XT90** existent sur le marché, mais nombre d’entre eux ne sont que des adaptateurs passifs. Un adaptateur ne recrée pas nécessairement les fonctions que l’outil échange avec le pack.

Et surtout :

- deux batteries « 18 V » en série → ≈36 V nominal et **≈42 V pleines** ;
- trois packs 5S → ≈54 V nominal mais **63 V pleines**.

Donc **3 × packs 18 V Li-ion en série dépasseraient 60 V**.

Je déconseille cette solution pour YXOR.

---

# 3.3 LiFePO4

Un exemple industriel 2026 particulièrement bien documenté est le **Victron Lithium SuperPack NG**.

La version 51,2 V / 100 Ah lancée après le premier trimestre 2026 fournit :

- **51,2 V** ;
- **100 Ah** ;
- **5120 Wh** ;
- **200 A maximum continu** ;
- ≈**41 kg** ;
- **871 × 198 × 173 mm** ;
- BMS intégré ;
- IP65 ;
- UN 38.3 ;
- cellules IEC 62619 / UL1973 / UL9540A selon documentation, batterie IEC62619 encore indiquée « pending ». [Victron Energy](https://www.victronenergy.com/media/pg/Lithium_SuperPack_NG/en/technical-data.html?utm_source=chatgpt.com)

Cela donne environ :

- **125 Wh/kg** ;
- **172 Wh/L**.

C’est un excellent exemple du compromis : sécurité/cycles très intéressants, mais densité massique beaucoup plus faible qu’une cellule haute performance.

Pour un humanoïde 10 kg, un pack de ce type est évidemment hors échelle. Pour YXOR 35–40 kg, je considérerais plutôt un **pack LiFePO4 custom compact**, pas cette batterie Victron elle-même.

### Tension LiFePO4 custom

Avec ≈3,2 V nominal et ≈3,65 V chargé par cellule :

- 14S : 44,8 V nominal / ≈51,1 V chargé ;
- **15S : 48,0 V / ≈54,75 V** ;
- 16S : 51,2 V / ≈58,4 V.

Comme en Li-ion, je préfère **15S à 16S** pour garder une réserve sous 60 V en cas de régénération.

---

# 3.4 Expédition en Suisse

Il faut distinguer la batterie **installée dans un équipement** d’une batterie expédiée seule.

Pour le transport aérien, les règles IATA/ICAO deviennent encore plus restrictives en 2026 : à partir du **1er janvier 2026**, les batteries Li-ion emballées avec un équipement et certains véhicules à batterie doivent être présentés au transport à un état de charge réduit, sauf approbation spécifique. [IATA](https://www.iata.org/contentassets/05e6d8742b0047259bf3a700bc9d42b9/lithium-battery-guidance-document.pdf?dm_t=0%2C0%2C0%2C0%2C0\&utm_source=chatgpt.com)

Pour un gros pack YXOR :

- ne pas partir du principe qu’un colis postal normal est admissible ;
- UN 38.3 est nécessaire au transport commercial, mais **UN 38.3 n’est pas une certification générale de sécurité d’utilisation** ;
- au-delà des seuils simplifiés type 100 Wh, passer par un transporteur acceptant les marchandises dangereuses/ADR-IATA ;
- batterie prototype custom sans rapport UN38.3 : expédition commerciale beaucoup plus compliquée.

Pour le robot final, j’intégrerais la transportabilité **dès la définition du pack**, idéalement avec modules démontables.

---

# 4. Sécurité batterie dans un robot qui tombe

C’est ici que je serais plus conservateur que sur un drone ou une voiture RC.

IEC 62133-2 couvre notamment des essais de **vibration et choc** pour batteries lithium portables et les abus raisonnablement prévisibles. [IEC Webstore](https://webstore.iec.ch/en/publication/70017?utm_source=chatgpt.com) IEC 62619 concerne les batteries lithium pour applications industrielles. [IEC Webstore](https://webstore.iec.ch/en/publication/69308?utm_source=chatgpt.com)

ISO 10218-1:2025 constitue une excellente référence de démarche de réduction des risques pour robots industriels, mais **les robots de service accessibles au public sont explicitement hors de son domaine d’application**. Il faut donc l’utiliser comme source de principes, pas affirmer que YXOR est « conforme ISO 10218 » sans analyser son cas d’usage. [ISO](https://www.iso.org/standard/73933.html?utm_source=chatgpt.com)

### Architecture que je recommande

Pour la batterie :

- pack placé **dans le torse, près du centre de masse** ;
- jamais directement derrière une coque externe susceptible de recevoir le premier impact ;
- coque structurelle + **zone sacrificielle/de déformation** autour du pack ;
- aucune vis, angle ou pièce de structure pointue orientée vers une cellule ;
- espace entre cellules et enveloppe ;
- séparateurs électriques et mécaniques entre cellules ;
- tenue mécanique des cellules indépendamment des conducteurs électriques ;
- capteurs de température répartis à l’intérieur du pack ;
- évent vers l’extérieur du robot, **loin du visage et du calculateur** ;
- pas de pack LiPo pouch exposé à la compression d’une armature.

Électriquement :

**cellules → fusible primaire → service disconnect → BMS → contacteur principal → précharge → bus moteurs.**

Et trois fonctions distinctes :

1. **BMS** : sous/surtension cellule, température, courant, équilibrage.
2. **Fusible** : dernier rempart passif contre le court-circuit.
3. **Contacteur / arrêt d’urgence** : isolation physique de la puissance des actionneurs.

L’arrêt d’urgence ne devrait donc pas être un simple message ROS.

Je conserverais éventuellement un petit rail auxiliaire qui reste alimenté quelques secondes pour :

- journaliser la faute ;
- sauvegarder ;
- couper proprement Linux.

Mais la puissance moteur doit pouvoir être interrompue **sans logiciel**.

### Régénération

C’est particulièrement important avec RobStride.

Si le BMS coupe la charge pendant qu’un actionneur régénère, le bus peut monter très rapidement. Il faut une stratégie explicitement définie :

- batterie capable d’absorber le courant ;
- BMS permettant la charge ;
- résistance/module de décharge ;
- seuil de clamp ;
- limitation logicielle de régénération en complément.

**Le BMS ne remplace pas un absorbeur de surtension.**

---

# 5. Calculateurs

Un détail essentiel : NVIDIA emploie différentes conventions de performance.

- Orin : généralement **INT8 TOPS**, et NVIDIA indique souvent la valeur **avec sparsité**.
- Hailo-8/8L : INT8 TOPS.
- Hailo-10H : **INT4 TOPS**.
- Thor : NVIDIA met en avant les **FP4 TFLOPS sparse**.

Ces nombres ne doivent donc **jamais être placés sur le même graphique comme s’ils représentaient la même chose**.

## 5.1 NVIDIA Jetson — gamme commercialisée en 2026

| Produit | Module / porteuse réaliste | Masse | Puissance | CPU | Accélérateur | IA | Mémoire | CAN | Prix public courant |
|---|---|---:|---|---|---|---|---|---|---|
| Orin Nano 4 GB | module **69,6×45 mm** / carrier devkit ≈100×79 mm | module : non trouvé ; kit ≈175 g pour plateforme Nano devkit documentée | modes à partir de 7 W | 6× Cortex-A78AE | 512 CUDA + Tensor | jusqu’à **34 INT8 TOPS sparse /17 dense en Super selon variante** | 4 GB LPDDR5 | **1 contrôleur sur module** | **$249 module** environ selon gamme 2026 ; prix exact actuel à vérifier au distributeur |
| Orin Nano 8 GB | idem | idem | jusqu’à **25 W Super** | 6×A78AE | 1024 CUDA, 32 Tensor | **67 sparse / 33 dense INT8 TOPS** | **8 GB**, 102 GB/s | 1 | **$399 module** |
| **Orin Nano Super Dev Kit** | ≈100×79 mm carrier | ≈175 g, plateforme dev kit | **7–25 W** module | 6×A78AE | 1024 CUDA +32 Tensor | **67 INT8 TOPS sparse /33 dense** | 8 GB | contrôleur CAN dans SOM ; transceiver à prévoir | **$399** |
| Orin NX 8 GB | **69,6×45 mm** / carrier custom 100×80 mm possible | non trouvé | jusqu’à ~25/40 W selon modes 2026 | 6×A78AE | 1024 CUDA + DLA | jusqu’à env. **117 sparse /58 dense** suivant Super/mode | 8 GB | CAN sur SOM | **$649** |
| **Orin NX 16 GB** | 69,6×45 mm | non trouvé | jusqu’à **40 W Super** | **8×A78AE** | 1024 CUDA + DLA | **157 sparse /78 dense INT8 TOPS** | **16 GB** | CAN | **$999** |
| AGX Orin 32 GB | **100×87 mm** | non trouvé module | **15–40 W** | 8×A78AE | Ampere +2×DLA | **200 INT8 sparse TOPS** | 32 GB | **2×CAN** | **$1,799** en liste NVIDIA 2026 |
| **AGX Orin 64 GB** | **100×87 mm** | module non trouvé | **15–60 W** | 12×A78AE | 2048 CUDA +64 Tensor +2 DLA | **275 sparse /138 dense INT8 TOPS** | **64 GB LPDDR5** | **2×CAN** | **$2,999 module** |
| AGX Orin Industrial | 100×87 mm | non trouvé | **15–75 W** | 12×A78AE | Ampere | **248 TOPS** | 64 GB ECC | CAN | **$3,199** |
| AGX Orin Dev Kit | module AGX + carrier | masse publiée ≈872,5 g selon FAQ matériel NVIDIA | jusqu’à 60 W module | 12×A78AE | idem 64GB | 275 INT8 TOPS | 64 GB | CAN exposé | **$3,499** |
| Thor T4000 | **100×87 mm** | non trouvé | **40–70 W** | 12× Arm Neoverse V3AE | Blackwell | **1200 TFLOPS FP4 sparse / 600 dense FP4 ou sparse INT8** | 64 GB | plusieurs CAN selon configuration | **$2,999 module** |
| Thor T5000 | **100×87 mm** | non trouvé | **40–130 W** | **14× Neoverse V3AE** | 2560 CUDA Blackwell, Tensor 5e gen | **2070 TFLOPS FP4 sparse /1035 dense FP4 ou sparse INT8** | **128 GB LPDDR5X**, 273 GB/s | jusqu’à 4 CAN module | **$4,999 module** |
| **AGX Thor Dev Kit** | **243,19×112,40×56,88 mm** | non trouvé | jusqu’à 130 W module | 14×V3AE | T5000 | 2070 FP4 TFLOPS sparse | 128 GB | **2 connecteurs CAN** | **$5,499** au marketplace NVIDIA oct. 2026 |

Les performances Orin Nano/NX et leurs modes Super sont documentées par NVIDIA. [NVIDIA Developer](https://developer.nvidia.com/blog/?p=93942\&utm_source=chatgpt.com)  
AGX Orin 64 est donné à **275 TOPS sparse et 138 TOPS dense INT8**, 100×87 mm, 15–60 W. [NVIDIA Developer](https://developer.nvidia.com/sites/default/files/akamai/Jetson_AGX_Orin_Developer_Kit_RG_0.pdf?utm_source=chatgpt.com)  
Les prix actuels des trois kits principaux sont **$399 Nano Super, $3,499 AGX Orin et $5,499 Thor** sur le Marketplace NVIDIA relevé en octobre 2026. [NVIDIA Marketplace](https://marketplace.nvidia.com/en-us/enterprise/robotics-edge/?location=ES\&product=jetson_nano\&utm_source=chatgpt.com)

### « repos / typique / maximum »

NVIDIA publie surtout des **modes de puissance**, pas une consommation universelle « idle / typique ». La consommation réelle dépend énormément :

- clocks ;
- GPU/DLA actifs ;
- périphériques ;
- NVMe ;
- caméras ;
- modèle.

Je refuse donc de fabriquer une valeur « idle ». Dans le tableau, les W indiqués sont les **enveloppes/modes officiellement documentés**.

---

# 5.2 Raspberry Pi + Hailo

| Produit | Calcul | Mémoire IA | Performance annoncée | Interface | Prix de lancement/courant |
|---|---|---:|---:|---|---:|
| Raspberry Pi 5 | CPU BCM2712, 4× Cortex-A76 2,4 GHz | mémoire système Pi | CPU uniquement | PCIe 2.0×1, USB3, 2×MIPI ; **pas de CAN natif avec transceiver** | dépend RAM |
| AI Kit | Hailo-8L | pas mémoire LLM dédiée | **13 TOPS INT8** | PCIe | **$70 historique**, désormais arrêté |
| AI HAT+ 13 TOPS | Hailo-8L | — | **13 TOPS INT8** | PCIe | **$70** |
| AI HAT+ 26 TOPS | Hailo-8 | — | **26 TOPS INT8** | PCIe | **$110** |
| **AI HAT+ 2** | **Hailo-10H** | **8 GB dédiée** | **40 TOPS INT4** | PCIe | **$200** |

Raspberry Pi indique que l’ancien AI Kit n’est plus en production et recommande les AI HAT+. L’AI HAT+2 ajoute Hailo-10H, **40 TOPS INT4 et 8 GB de mémoire**, et vise aussi des workloads génératifs jusqu’à environ 6B paramètres. [Raspberry Pi](https://www.raspberrypi.com/documentation/accessories/ai-hat-plus.html?utm_source=chatgpt.com)

Attention encore une fois :

**40 TOPS INT4 Hailo-10H ≠ 40 TOPS INT8 Orin.**

---

# 5.3 Interfaces et logiciel

### Jetson

Très favorable à ton stack :

- CUDA ;
- cuDNN ;
- TensorRT ;
- TensorRT-LLM ;
- ONNX Runtime avec backend CUDA/TensorRT ;
- Isaac ;
- DeepStream ;
- ROS 2 sous Ubuntu/JetPack.

NVIDIA documente également Ollama, llama.cpp, vLLM, MLC et TensorRT-LLM sur Orin Nano Super. [NVIDIA Developer](https://developer.nvidia.com/blog/?p=93942\&utm_source=chatgpt.com)

### Raspberry Pi/Hailo

Très bon pour :

- détection ;
- segmentation ;
- pose ;
- vision multi-flux.

Mais ce n’est pas un petit CUDA universel. Les modèles destinés au Hailo passent normalement par la chaîne de compilation/runtime Hailo.

---

# 6. Niveaux d’IA embarquée

| Niveau | Besoin | Minimum raisonnable | Choix que je ferais | Exemple réel |
|---|---|---|---|---|
| **a. marche ONNX 50 Hz** | petit MLP + état robot | Raspberry Pi 5 ou mini-PC N95 | Pi5 si seulement locomotion ; Orin Nano si architecture future | Berkeley Humanoid Lite fonctionne avec **Intel N95**, CAN à 250 Hz ; politique biped publiée à 50 Hz dans la documentation/projet |
| **b. + vision** | détection + suivi personne | Pi5 + AI HAT+ 13 TOPS | **Orin Nano Super 8GB** | ToddlerBot utilise Orin NX avec vision stéréo temps réel |
| **c. + voix locale** | ASR + TTS + vision + locomotion | Orin Nano Super 8GB | **Orin NX 16GB** | ToddlerBot embarque microphones, haut-parleur et Orin NX |
| **d. + LLM local** | LLM quantifié + vision/voix | Orin Nano Super pour petit modèle | **NX16 pour 3–8B ; AGX Orin 64 pour marge supérieure** | NVIDIA démontre Orin Nano Super jusqu’à Llama 3.1 8B |

NVIDIA indique explicitement qu’Orin Nano Super peut exécuter des modèles allant jusqu’à **Llama 3.1 8B**. [NVIDIA Developer](https://developer.nvidia.com/blog/?p=93942\&utm_source=chatgpt.com)

### Tokens/s

Je n’ai pas trouvé, dans les sources constructeur suffisamment propres retenues ici, **un chiffre unique et reproductible de tokens/s pour chacun de ces Jetson** qui soit comparable à modèle, quantification, contexte et runtime identiques.

Je préfère donc écrire :

**tokens/s : non trouvé sous forme de benchmark constructeur comparable.**

C’est beaucoup plus rigoureux qu’annoncer « 15 t/s » ou « 30 t/s » sans préciser :

- modèle ;
- Q4/Q8/FP16 ;
- prompt processing vs génération ;
- contexte ;
- TensorRT-LLM vs llama.cpp ;
- clocks ;
- puissance.

### Pour ton cas concret

Je positionnerais :

- marche seule : **<1 TOPS nécessaire en pratique pour beaucoup de politiques MLP**, le CPU peut suffire ;
- locomotion + deux caméras + perception : Nano Super ;
- perception + voix + SLAM + ROS2 : **NX 16GB** ;
- LLM local utile dans le robot : **NX16 minimum raisonnable**, AGX64 si tu veux aller nettement plus loin.

---

# 7. Cartes de bus

## 7.1 CAN / CAN-FD

| Produit | Canaux | CAN / FD | Débit | Dimensions | Masse | Linux | Prix |
|---|---:|---|---:|---|---:|---|---:|
| Kvaser Leaf Light v2 | 1 | CAN 2.0 | **1 Mbit/s** | **165×35×17 mm** | **112 g** | oui | **$463**, désormais EOL |
| Seeed MCP2518FD HAT | **2** | CAN-FD | **8 Mbit/s** | non trouvé dans page commerciale | non trouvé | Raspberry Pi/Linux | **$69**, stock 2026 |
| Waveshare 2-CH CAN-FD HAT | **2** | CAN-FD MCP2518FD | FD | **65×56,5 mm** | **40 g** | SocketCAN/Linux via SPI | prix : non trouvé dans source capturée |
| PEAK PCAN-USB FD | 1 | CAN-FD | jusqu’à ≈12 Mbit/s data selon configuration | non trouvé ici | non trouvé | oui | prix actuel vérifié : non trouvé |
| Jetson Orin Nano/NX SOM | contrôleur intégré | CAN | dépend SOM | intégré | — | SocketCAN | compris |
| AGX Orin SOM | **2** | CAN | intégré | — | — | SocketCAN | compris |
| Thor T5000 | jusqu’à plusieurs contrôleurs | CAN | intégré | — | — | Linux | compris |

Kvaser documente 1 canal, Linux, 40–1000 kbit/s et 112 g. [Pim Kvaser](https://pim.kvaser.com/var/assets/Datasheet/73-30130-00685-0/00685-0_Kvaser%20Leaf%20Light%20v2_Letter.pdf?utm_source=chatgpt.com)  
Seeed vend toujours son HAT 2 canaux MCP2518FD à **$69** et jusqu’à 8 Mbit/s. [Seeed Studio](https://www.seeedstudio.com/CAN-BUS-FD-HAT-for-Raspberry-Pi-p-4742.html?utm_source=chatgpt.com)  
Le Waveshare équivalent fait **65×56,5 mm et 40 g**. [Waveshare](https://www.waveshare.com/wiki/2-CH_CAN_FD_HAT?utm_source=chatgpt.com)

### Attention au CAN intégré

Un contrôleur CAN dans un SoC **n’est pas un port CAN complet**.

Il faut généralement encore :

- transceiver CAN physique ;
- protections ESD ;
- éventuellement isolation galvanique ;
- terminaison 120 Ω ;
- connectique.

Je ne remplacerais donc pas six bus de puissance avec « une broche CAN du Jetson ».

---

## 7.2 Feetech / Dynamixel

| Adaptateur | Bus | Débit | Dimensions | Masse | Linux | Prix |
|---|---|---:|---|---:|---|---:|
| Feetech FE-URT-2 | TTL + RS485 | max exact : non trouvé dans la source retenue | **55,8×36,6×11,5 mm** | **12,5 g** | port série USB | prix : non trouvé |
| **ROBOTIS U2D2** | TTL + RS485 + UART | **6 Mbit/s max** | **48×18×14,9 mm** | **9 g** | oui | **$36,92** |

U2D2 est très bien documenté et n’alimente pas les servos lui-même : alimentation servo séparée obligatoire. [ROBOTIS Docs](https://docs.robotis.com/docs/parts/interface/u2d2/?utm_source=chatgpt.com)

Pour Feetech, je privilégierais naturellement l’interface constructeur pour développement, puis à terme une UART native avec transceiver half-duplex propre sur la carte YXOR.

---

# 7.3 Combien de CAN pour 27 axes à 500 Hz ?

C’est probablement le résultat le plus important de toute cette étude.

RobStride documente :

- **CAN 2.0** ;
- **1 Mbit/s** ;
- trames jusqu’à **8 octets**. [GitHub](https://github.com/cloudhan/robstride_docs/blob/main/RS06.md?utm_source=chatgpt.com)

### Étape 1 — commandes

27 articulations × 500 commandes/s :

**27 × 500 = 13 500 trames/s**

### Étape 2 — feedback

Si chaque articulation renvoie un état à 500 Hz également :

**13 500 TX + 13 500 RX = 27 000 trames/s**

### Étape 3 — taille d'une trame

Pour une trame CAN 2.0 étendue de 8 octets, suivant le framing exact, on est autour de **≈130 bits avant worst-case bit stuffing/inter-frame overhead**.

Prenons deux bornes :

- idéal : 131 bits ;
- budget conservateur : ≈150 bits/trame.

### Charge réseau

Idéal :

**27 000 × 131 = 3 537 000 bit/s**

Conservateur :

**27 000 × 150 = 4 050 000 bit/s**

Or un canal = 1 000 000 bit/s maximum brut.

Donc :

### minimum mathématique absolu

`ceil(3,537 / 1) = 4 bus`

Mais quatre bus seraient proches de la saturation.

Si on vise **≤70 % d’occupation** :

`4,05 / 0,70 = 5,79`

→ **6 canaux CAN**

### Recommandation YXOR Lab

Je créerais **6 segments** :

1. jambe gauche ;
2. jambe droite ;
3. bras gauche ;
4. bras droit ;
5. bassin/torse ;
6. réserve / autres articulations.

Cela donne aussi une excellente isolation des fautes.

Si finalement les retours ne sont envoyés qu’à 250 Hz ou que tous les 27 axes ne sont pas RobStride, tu pourras réduire le besoin.

### Et si RobStride CAN-FD est confirmé ?

Alors il faudra refaire le calcul à partir :

- de la vraie vitesse arbitration ;
- de la vitesse data ;
- du protocole exact ;
- du firmware utilisé.

Mais **je ne construirais pas l’architecture autour d’un CAN-FD supposé**, puisque la documentation constructeur actuelle retrouvée indique CAN 2.0/1 Mbit/s.

---

# 8. Humanoïdes réels comparables

| Robot | Calculateur | Batterie | Bus / architecture | Source / qualité |
|---|---|---|---|---|
| **ToddlerBot** | **Jetson Orin NX 16 GB recommandé** | installé dans le torse ; spécification précise non trouvée dans source capturée | détails servo bus à vérifier dans BOM/PCB | documentation officielle projet |
| **Berkeley Humanoid Lite** | **Intel N95 mini-PC** | **6S 4 Ah LiPo**, ≈30 min selon documentation/papier synthétisé | **4× CAN 2.0 1 Mbit/s**, un bus par membre ; actionneurs/IMU ≈250 Hz | projet/papier |
| **LeRobot Humanoid** | non trouvé de façon suffisamment fiable dans les sources retenues | non trouvé | non trouvé | informations publiques encore incomplètes |
| **BRIDGE** | non trouvé publiquement au 7/10/2026 | non trouvé | non trouvé | site projet : code/tutorial « coming soon » |
| **Booster T1** | **Jetson AGX Orin 200 TOPS + Intel i7-1370P** documentés fabricant | **10,5 Ah**, tension non trouvée dans source fabricant retenue | ports de communication publiés ; bus moteur interne : non trouvé | fabricant |
| **Unitree G1** | documentation de laboratoires utilisateurs : **Jetson Orin NX** sur certaines configurations | source indépendante : **13S, 46,8 V nominal, 54,6 V chargé, 9 Ah ≈421 Wh** | bus moteur interne détaillé publiquement : non trouvé | documentation laboratoire, pas fiche constructeur |

ToddlerBot recommande explicitement **Jetson Orin NX 16 GB**, et son site annonce une estimation Foundation Stereo embarquée à **10 Hz** sur ce calculateur. [Hshi74](https://hshi74.github.io/toddlerbot/software/02_jetson_orin.html?utm_source=chatgpt.com)

Berkeley Humanoid Lite est particulièrement instructif pour YXOR : 22 axes, mini-PC N95 et architecture **multi-CAN**, plutôt qu’un CAN partagé par tout le robot. [GitHub](https://github.com/hybridrobotics/berkeley-humanoid-lite?utm_source=chatgpt.com)

BRIDGE, publié en 2026, mesure **88 cm, 12,5 kg, possède 21 DoF actifs et revendique ≈$1,5k de coût plateforme**, mais les codes et tutoriels sont encore annoncés « coming soon » au moment de la consultation ; je n’invente donc ni batterie ni calculateur. [Google Sites](https://sites.google.com/view/bridgerobot/home?utm_source=chatgpt.com)

### Un précédent particulièrement intéressant : Unitree G1

La documentation de laboratoire trouvée donne **13S / 46,8 V / 54,6 V pleine charge / 9 Ah**.

C’est exactement la topologie de tension que je privilégie pour YXOR.

Ce n’est pas une preuve que 13S est « universel », mais c’est une validation intéressante qu’un humanoïde de taille comparable peut fonctionner autour d’un bus **≈48 V nominal avec une vraie marge sous 60 V**.

---

# 9. Recommandation YXOR Lab — 10 kg / 27 axes

## Architecture électrique

### Batterie principale

Mon choix n°1 :

**13S1P Molicel P45B**, si l’autonomie est secondaire.

Calcul à partir des données fabricant :

- 13 × 3,6 = **46,8 V nominal** ;
- 13 × 4,2 = **54,6 V chargé** ;
- 13 × 4,5 Ah × 3,6 V = **210,6 Wh** ;
- masse cellules ≤13 × 69 g = **897 g** ;
- courant cellule annoncé = **45 A continu**. [Molicel](https://www.molicel.com/product/inr-21700-p45b/?utm_source=chatgpt.com)

Il faudra ajouter :

- BMS ;
- busbars ;
- câblage ;
- contacteur ;
- fusible ;
- enclosure.

Donc masse réelle pack >897 g.

Si les tests montrent que les pointes de courant ou l’autonomie sont insuffisantes :

### 13S2P P45B

- **46,8 V** ;
- **54,6 V max** ;
- **421,2 Wh** ;
- cellules ≤**1,794 kg** ;
- capacité 9 Ah ;
- courant théorique issu du rating cellules : **90 A continu**.

Je préférerais commencer avec **13S1P instrumenté**, mesurer réellement le courant, puis passer à 2P si besoin, plutôt que surdimensionner avant de disposer d’un profil énergétique réel.

### Exception RS01

Si YXOR Lab contient des RS01, je ferais l’un des choix suivants :

- supprimer le RS01 au profit du RS02 lorsque possible ;
- adopter 11S pour l’ensemble ;
- ou créer un rail converti ≤48 V pour le RS01.

Je préfère **uniformiser les actionneurs autour d’un bus 13S**.

---

## Compute

### Ma préférence : **Jetson Orin NX 16GB**

Pourquoi plutôt que Nano Super :

- marge mémoire ;
- 157 TOPS sparse /78 dense en Super ;
- 16 GB ;
- 40 W max module ;
- DLA ;
- bon écosystème ROS2/CUDA/TensorRT ;
- encore petit : SOM 69,6×45 mm. [NVIDIA Developer](https://developer.nvidia.com/embedded/jetson-modules/?utm_source=chatgpt.com)

Pour une version économique :

**Orin Nano Super 8GB**, $399 et 7–25 W, est déjà très impressionnant. [NVIDIA](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/nano-super-developer-kit/?trk=article-ssr-frontend-pulse_little-text-block\&utm_source=chatgpt.com)

### Rails

Je viserais :

- 46,8 V bus moteurs ;
- DC/DC **12 V** compute/peripherals ;
- rail 7,4/8 V Feetech ;
- rail 6 V si STS3032/SCS bas voltage ;
- éventuellement 5 V isolé pour microcontrôleurs.

---

# 10. Recommandation YXOR final — 35 à 40 kg

Ici, le dimensionnement change complètement.

## Batterie

Je resterais malgré tout sur :

### **13S Li-ion**

Un exemple conservateur de pack :

**13S4P P45B**

dérivé des données fabricant :

- 52 cellules ;
- 46,8 V nominal ;
- 54,6 V plein ;
- **18 Ah** ;
- **842,4 Wh** ;
- masse cellules ≤ **3,588 kg** ;
- capacité théorique de courant = **180 A continus** si chaque cellule reste dans son rating de 45 A. [Molicel](https://www.molicel.com/product/inr-21700-p45b/?utm_source=chatgpt.com)

Le pack fini pèsera davantage.

Pour une machine 35–40 kg faisant :

- marche dynamique ;
- course ;
- saut ;
- relevé ;
- poussée/port de charges ;

je trouve cet ordre de grandeur bien plus crédible qu’une batterie d’outillage.

Mais je ne figerais **ni 4P ni le calibre BMS** sans mesurer ou simuler :

- puissance mécanique ;
- rendement actionneurs ;
- courant d’appel ;
- simultanéité des couples ;
- régénération ;
- autonomie requise.

## Alternative sécurité : 15S LiFePO4

À considérer si tu privilégies :

- durée de vie ;
- sécurité thermique ;
- cycles ;
- robustesse,

au détriment de la masse et du volume.

Je choisirais plutôt **15S ≈48 V nominal /54,75 V chargé** que 16S ≈58,4 V chargé.

---

## Calculateur

Je verrais deux architectures.

### Architecture raisonnable

**Orin NX 16GB**

pour :

- locomotion ;
- perception ;
- SLAM ;
- détection ;
- voix ;
- ROS2 ;
- contrôle haut niveau.

Un petit MCU/SoC temps réel séparé peut superviser :

- watchdog ;
- E-stop ;
- power sequencing ;
- CAN ;
- sécurité.

### Architecture IA ambitieuse

**AGX Orin 64GB**

si tu veux simultanément :

- plusieurs caméras ;
- VLM ;
- modèle de langage local ;
- ASR/TTS ;
- perception 3D ;
- planification.

275 INT8 TOPS sparse, 64 GB et 15–60 W restent raisonnables à l’échelle d’un humanoïde 35–40 kg. [NVIDIA Developer](https://developer.nvidia.com/sites/default/files/akamai/Jetson_AGX_Orin_Developer_Kit_RG_0.pdf?utm_source=chatgpt.com)

### Thor ?

Je le réserverais à une version ultérieure.

Le T5000 peut consommer jusqu’à **130 W**, et le dev kit lui-même mesure **243×112×57 mm environ**. Pour YXOR v1, tu paierais :

- beaucoup plus ;
- une masse/thermique supérieures ;
- une complexité énergétique plus grande,

pour une puissance de calcul que la locomotion n’exige absolument pas.

Thor devient intéressant si YXOR évolue réellement vers un humanoïde « embodied foundation model » faisant du VLA/VLM lourd en local.

---

# 11. Ce que je changerais dans ton architecture actuelle

Je fixerais dès maintenant ces interfaces :

```text
                           ┌───────── DC/DC → 12 V → Jetson / capteurs
                           │
13S Li-ion                 ├───────── DC/DC → 7.4–8 V → Feetech
46.8 V nom / 54.6 V max   │
        │                  ├───────── DC/DC → 6 V → petits Feetech
        │                  │
      fuse                 └───────── auxiliaires
        │
 service disconnect
        │
       BMS
        │
 main contactor
        │
    precharge
        │
   DC POWER BUS
        │
        ├── CAN segment 1 → jambe G
        ├── CAN segment 2 → jambe D
        ├── CAN segment 3 → bras G
        ├── CAN segment 4 → bras D
        ├── CAN segment 5 → bassin / torse
        └── CAN segment 6 → spare / autres axes
        │
 regeneration clamp /
 RobStride discharge module
```

Et je séparerais conceptuellement **trois chaînes de sécurité** :

**software control ≠ safety controller ≠ battery protection**.

Aucune panne de ROS, Linux, Jetson ou CAN ne devrait empêcher l’arrêt matériel de la puissance.

---

# 12. Comparaison finale des familles de batteries

| Famille | Puissance spécifique | Énergie spécifique | Robustesse aux chocs | BMS | Intégration YXOR |
|---|---|---|---|---|---|
| **21700 haute puissance** | excellente | excellente | bonne si enclosure bien conçue | à concevoir | **★★★★★** |
| 18650 haute puissance | très bonne | très bonne | bonne | à concevoir | ★★★★☆ |
| LiPo RC | exceptionnelle | bonne | **moins favorable aux perforations/compression** | généralement externe | ★★★☆☆ |
| Outillage 18 V | bonne | moyenne | excellente mécaniquement | intégré/propriétaire | ★★☆☆☆ principal ; ★★★★★ prototype |
| LiFePO4 | bonne | faible/moyenne | excellente intrinsèquement | souvent très bon | ★★★☆☆ humanoïde léger ; ★★★★☆ si sécurité prime |

Pour YXOR, je choisirais donc **des cellules cylindriques 21700 de puissance** et j’investirais l’effort d’ingénierie dans un vrai pack robotique.

---

# 13. Registre des sources principales

J’ai utilisé prioritairement les sources suivantes, consultées/vérifiées en **octobre 2026** :

1. **RobStride — Product Information / spécifications RS 2026-07-13**, constructeur : plages de tension, couples, masses, prix et gamme RS00–RS06. [GitHub](https://github.com/RobStride/Product_Information/?utm_source=chatgpt.com)  
2. **RobStride RS06 documentation** : 48 V nominal, 60 V maximum, CAN 1 Mbit/s. [GitHub](https://github.com/cloudhan/robstride_docs/blob/main/RS06.md?utm_source=chatgpt.com)  
3. **Molicel P45B**, constructeur : 3,6 V, 4,5 Ah, 45 A, dimensions et densités énergétiques. [Molicel](https://www.molicel.com/product/inr-21700-p45b/?utm_source=chatgpt.com)  
4. **Murata cylindrical Li-ion catalogue et VTC6A datasheet**, constructeur. [Murata Manufacturing Co., Ltd.](https://www.murata.com/en-us/products/batteries/cylindrical?utm_source=chatgpt.com)  
5. **Victron SuperPack NG 2026**, constructeur : BMS, courants, dimensions, masses, UN38.3 et standards. [Victron Energy](https://www.victronenergy.com/media/pg/Lithium_SuperPack_NG/en/technical-data.html?utm_source=chatgpt.com)  
6. **NVIDIA Jetson Orin Nano/NX Super**, constructeur. [NVIDIA Developer](https://developer.nvidia.com/blog/?p=93942\&utm_source=chatgpt.com)  
7. **NVIDIA Jetson AGX Orin**, constructeur : 275/138 TOPS INT8, 100×87 mm, 15–60 W, interfaces. [NVIDIA Developer](https://developer.nvidia.com/sites/default/files/akamai/Jetson_AGX_Orin_Developer_Kit_RG_0.pdf?utm_source=chatgpt.com)  
8. **NVIDIA Marketplace**, octobre 2026 : prix actuels des kits Nano Super, AGX Orin et Thor. [NVIDIA Marketplace](https://marketplace.nvidia.com/en-us/enterprise/robotics-edge/?location=ES\&product=jetson_nano\&utm_source=chatgpt.com)  
9. **NVIDIA Thor**, constructeur ; performances FP4 à distinguer des TOPS INT8 Orin. [NVIDIA](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson/back-to-school/?utm_source=chatgpt.com)  
10. **Raspberry Pi / Hailo** : AI Kit, AI HAT+, AI HAT+2, performances et positionnement. [Raspberry Pi](https://www.raspberrypi.com/documentation/accessories/ai-hat-plus.html?utm_source=chatgpt.com)  
11. **Kvaser Leaf**, constructeur : CAN classique, dimensions, masse, Linux et prix/EOL. [Kvaser](https://kvaser.com/product/kvaser-leaf-light-hs-v2/?utm_source=chatgpt.com)  
12. **Seeed 2-channel CAN-FD HAT**, fabricant/revendeur : deux canaux, 8 Mbit/s, $69. [Seeed Studio](https://www.seeedstudio.com/CAN-BUS-FD-HAT-for-Raspberry-Pi-p-4742.html?utm_source=chatgpt.com)  
13. **Waveshare 2-CH CAN-FD HAT**, fabricant : MCP2518FD, 65×56,5 mm, 40 g. [Waveshare](https://www.waveshare.com/wiki/2-CH_CAN_FD_HAT?utm_source=chatgpt.com)  
14. **ROBOTIS U2D2**, constructeur : TTL/RS485, 6 Mbit/s, 48×18×14,9 mm, 9 g, Linux, $36,92. [ROBOTIS Docs](https://docs.robotis.com/docs/parts/interface/u2d2/?utm_source=chatgpt.com)  
15. **IEC 62133-2:2017+A1:2021**, IEC : sécurité des batteries lithium portables, incluant essais mécaniques. [IEC Webstore](https://webstore.iec.ch/en/publication/70017?utm_source=chatgpt.com)  
16. **ISO 10218-1:2025**, ISO : sécurité robotique industrielle et limites explicites du scope vis-à-vis des robots de service. [ISO](https://www.iso.org/standard/73933.html?utm_source=chatgpt.com)  
17. **IATA Lithium Battery Guidance**, règles 2026 sur état de charge au transport aérien. [IATA](https://www.iata.org/contentassets/05e6d8742b0047259bf3a700bc9d42b9/lithium-battery-guidance-document.pdf?dm_t=0%2C0%2C0%2C0%2C0\&utm_source=chatgpt.com)  
18. **ToddlerBot**, documentation officielle : Orin NX 16GB et perception stéréo embarquée. [GitHub](https://github.com/hshi74/toddlerbot/blob/main/docs/sections/01_hardware.rst?utm_source=chatgpt.com)  
19. **Berkeley Humanoid Lite**, dépôt/documentation et synthèse technique : N95, architecture multi-CAN, batterie LiPo. [GitHub](https://github.com/hybridrobotics/berkeley-humanoid-lite?utm_source=chatgpt.com)  
20. **BRIDGE**, site officiel du projet : 88 cm, 12,5 kg, 21 DoF, ≈$1,5k ; détails électroniques encore non publiés. [Google Sites](https://sites.google.com/view/bridgerobot/home?utm_source=chatgpt.com)  

## Conclusion d’ingénierie

Pour **YXOR Lab**, ma baseline serait désormais très claire :

**13S Li-ion P45B → ≈46,8 V, Orin NX 16 GB, 6 CAN 2.0 segmentés, Feetech sur DC/DC séparés, contacteur + précharge + BMS + fusible + dissipateur régénératif.**

Pour **YXOR final**, je conserverais volontairement **la même famille électrique et logicielle** :

**13S4P environ, même bus ≈48 V, même protocole CAN segmenté, même distribution auxiliaire, puis AGX Orin 64 GB seulement si les fonctions IA le justifient.**

C’est particulièrement intéressant pour ta stratégie YXOR : le petit robot peut effectivement devenir un **banc d’apprentissage architectural du grand**, plutôt qu’un prototype utilisant des batteries, bus et compute totalement différents.