> **Source externe, non vérifiée par le dépôt ; les marqueurs de référence ChatGPT n'ont pas d'URL résolue.**
>
> Étude fournisseurs rédigée par ChatGPT le 30-09-2026, versée telle quelle
> le même jour. Le texte ci-dessous n'est ni corrigé ni reformulé. Les
> écarts avec `params/actionneurs.yaml` sont relevés au journal du
> 2026-09-30, pas ici. Synthèse : `docs/cadrage.md`, § 9.

---

J’ai repris l’étude au niveau **fabricant + chaîne d’approvisionnement**, et le résultat est assez tranché sur le critère spécifique de YXOR.

**À la date du 30 septembre 2026, RobStride est le seul des dix fabricants pour lequel j’ai pu vérifier une gamme actuelle qui tombe pratiquement exactement sur les trois paliers que nous cherchons : 5,5 → 17 → 36 N·m en pointe, tout en restant dans la même famille RS et sur le même bus CAN.** En revanche, ce n’est pas encore le fournisseur le plus rassurant sur la stabilité documentaire, le firmware et le SAV européen.

Toutes les pages sans date de publication explicite ci-dessous ont été vérifiées le **30/09/2026**. Quand une information importante n’a pas pu être établie, je mets volontairement **« non trouvé »**.

## 1. Résultat global pour YXOR

| Fabricant | ≈5–6 N·m | ≈17 N·m | ≈36 N·m | Même bus / logiciel | Même famille mécanique | Docs/ouverture | Approvisionnement UE/CH | Verdict YXOR |
|---|---:|---:|---:|---|---|---|---|---|
| **RobStride** | **RS05 5,5** | **RS01/02 17** | **RS06 36** | **Oui, CAN 1 Mbit/s ; même famille de protocoles** | Famille cohérente, **brides différentes** | Très bon, mais jeune | Moyen | **Meilleur chemin 0,6→0,9 m** |
| **CubeMars** | AK45-10 V3 7 | AK80-9 V3 22 | pas exact ; 29→53 | Globalement oui, mais générations V2/V3 | Non | Très bon | Bon | Excellent plan B |
| **MyActuator** | ≈7 | 20 ancien, désormais discontinué | X4-36 = 36 | **CAN commun très mature** | Non | Très bon | **Très bon en France** | Très rassurant industriellement, gamme moins adaptée |
| **Damiao** | ≈7 | ≈12–20 selon modèle/rév. | pas proprement 36 | Oui dans la famille MIT/CAN, avec nuances | Non | Bon | Moyen/faible | Intéressant mais moins stable |
| **Unitree** | non trouvé | non trouvé proche | IM6014 31,7–34,4 | **Non garanti entre générations** | Non | Moyen/bon | **Excellent CH pour robots**, moteurs moins clair | Mauvais chemin pour les 3 tailles |
| **SteadyWin** | 5,6–8 | ≈17–18 suivant variante | ≈41+ | CAN, mais drivers/firmwares différents | Non | Bon | Moyen | Techniquement intéressant, plus risqué logiciellement |
| **ROBOTIS** | ≈5 continu | ≈10–25 continu | ≈45 continu | **Excellent : Protocol 2.0** | Non | **Excellent** | **Très bon UE** | Le plus mature, mais mal adapté masse/couple |
| **Feetech** | non | non dans même famille | non | Non | Non | Correct petit servo | Bon UE | À écarter pour les jambes YXOR |
| **mjbots** | non | QDD100 historique ≈16 | non | Excellent CAN-FD/moteus | Non | **Exceptionnellement ouvert** | Direct USA | Pas de gamme actuelle adaptée |
| **ODrive** | dépend du moteur/réducteur | idem | idem | **Oui côté contrôleur** | À concevoir soi-même | Logiciel excellent, firmware récent fermé | **Très bon, entrepôt UE** | Alternative d'architecture, pas équivalent aux QDD intégrés |

Pour RobStride, les chiffres proviennent de la spécification officielle du **13 juillet 2026** : RS05 = 5,5 N·m, RS01/RS02 = 17 N·m, RS06 = 36 N·m. La même documentation fournit les manuels et fichiers STEP de RS00 à RS06 ainsi que CANopen, OTA et accessoires de bus. :chatgpt-content-reference{index="1"}

Le point important est que **« même famille mécanique » ne veut pas dire « même bride interchangeable »**. RS05 fait 46×46×44 mm tandis que RS06 fait 88×88×49 mm ; les géométries de montage évoluent avec la taille. Je n’ai trouvé **aucun des dix fabricants** répondant simultanément aux trois couples et à une bride physiquement identique. :chatgpt-content-reference{index="2"}

---

# 2. RobStride — le candidat naturel pour YXOR

### Gamme

C'est ici que le cas est exceptionnellement propre :

- **YXOR 0,6 m : RS05 — 5,5 N·m peak, 191 g**
- **YXOR 0,8 m : RS01 ou RS02 — 17 N·m peak, ~380–405 g**
- **YXOR 0,9 m : RS06 — 36 N·m peak, 621 g**

Le catalogue officiel courant confirme ces trois paliers et un **CAN à 1 Mbit/s**. :chatgpt-content-reference{index="3"}

C'est de très loin la correspondance la plus propre avec notre cahier des charges.

### Mais : stabilité des spécifications à surveiller

Ton exemple RS02 était tout à fait pertinent.

Une documentation RS02 antérieure donne **6 N·m nominal / 17 N·m peak**, tandis que la spécification officielle du 13/07/2026 donne désormais **7 N·m nominal / 17 N·m peak**. La page actuelle du RS02-IP67 affiche encore **6 N·m nominal**, alors que le tableau officiel 2026 du dépôt donne 7 N·m. :chatgpt-content-reference{index="4"}

Même phénomène sur le RS05 :

- site fabricant actuel : **1,6 N·m nominal** ;
- spécification du 13/07/2026 : **1,8 N·m nominal**. :chatgpt-content-reference{index="5"}

Donc je classe la **stabilité documentaire comme moyenne**, et non excellente.

Ce n'est pas seulement cosmétique : le changelog firmware RS02 documente des corrections du coefficient Kp/Kd, du PDO CANopen, de la courbe de couple, du reporting, ainsi qu'un changement matériel supprimant une résistance CAN de 240 Ω sur les lots ultérieurs. La release du **27 février 2025** avait également corrigé la précision du retour de couple RS02 et aligné son protocole sur les autres moteurs. :chatgpt-content-reference{index="6"}

C'est exactement le genre de PCN/revision history que nous devons figer dans YXOR.

### Documentation

Très bonne désormais :

- manuels individuels ;
- STEP RS00→RS06 ;
- protocole ;
- CANopen ;
- outil OTA ;
- CAN hub ;
- power board ;
- discharge module. :chatgpt-content-reference{index="7"}

C'est nettement mieux qu'il y a encore un an.

### Ouverture

Le protocole est documenté et plusieurs implémentations open source existent. MotorBridge supporte actuellement toute la gamme RS00–RS06 à la fois via le protocole CAN privé RobStride et via **CiA402/CANopen**. :chatgpt-content-reference{index="8"}

En revanche :

**firmware moteur complet open source sous licence clairement identifiée : non trouvé.**

Il faut donc distinguer *protocole ouvert/documenté* de *actionneur totalement open hardware/open firmware*.

### Écosystème / pièges logiciels

Un problème intéressant a été documenté dans LeRobot en 2026 : son backend « RobStride » utilisait en réalité un framing similaire à Damiao et ne communiquait pas correctement avec le matériel RobStride réel. Le problème concernait **l'intégration LeRobot**, pas une panne des moteurs. :chatgpt-content-reference{index="9"}

Cela confirme l'intérêt pour YXOR de **posséder notre propre HAL moteur**, plutôt que de dépendre directement d'un wrapper tiers.

### SAV / garantie

Un manuel officiel RobStride indique :

- 7 jours retour ;
- 7–15 jours remplacement dans certaines conditions ;
- réparation gratuite 15–365 jours ;
- **garantie 1 an**. :chatgpt-content-reference{index="10"}

Attention : ce texte est construit autour du droit et du SAV chinois. Je n'ai pas trouvé de réseau SAV RobStride officiellement établi en Suisse.

Le fabricant renvoie actuellement vers **Amazon et Seeed** pour commander. :chatgpt-content-reference{index="11"}

**Distributeur officiel suisse RobStride : non trouvé.**

**Centre RMA RobStride UE explicitement identifié : non trouvé.**

C'est le principal défaut de RobStride aujourd'hui.

### Pérennité

Aucune annonce d'EOL RS00–RS06 trouvée.

Au contraire, RS05/RS06 et le dépôt de documentation ont encore reçu des mises à jour en 2026. La gamme paraît donc en expansion plutôt qu'en fin de vie. :chatgpt-content-reference{index="12"}

**Confiance : élevée sur la compatibilité gamme/bus, moyenne sur la stabilité long terme et le SAV.**

---

# 3. CubeMars / T-Motor

CubeMars est probablement aujourd'hui le concurrent le plus sérieux si l'on privilégie **maturité produit + documentation + historique dans les robots dynamiques** plutôt que l'adéquation exacte aux trois couples.

La génération AK V3 est très bien documentée. L'AK45-10 V3, par exemple, est donnée pour **7 N·m peak, 262 g**, CAN, MIT + Servo, double encodeur ; CubeMars publie firmware/outil, manuel et STEP avec des dates de mise à jour allant jusqu'au **13 août 2026**. :chatgpt-content-reference{index="13"}

Mais la progression est moins propre :

- AK45-10 V3 : **7 N·m** ;
- AK80-9 V3 : **22 N·m** ;
- AK70-9 V3 : classe ~29 N·m ;
- AK10-9 V3 : **53 N·m**. :chatgpt-content-reference{index="14"}

Il n'y a donc pas le joli **5,5 / 17 / 36** de RobStride.

### Stabilité

CubeMars a plusieurs générations simultanées. Le catalogue actuel contient encore AK10-9 **V2 et V3**, avec des caractéristiques différentes ; les drivers communautaires sont obligés d'encoder séparément des profils V1, V1.1 et V2. :chatgpt-content-reference{index="15"}

Ce n'est pas nécessairement mauvais : au contraire, les versions sont généralement clairement nommées. Mais il faut stocker **model + hardware version + firmware version** dans la configuration YXOR.

### Ouverture

CAN/MIT documentés et nombreux drivers communautaires.

**Firmware embarqué entièrement open source : non trouvé.**

**Licence d'un SDK fabricant complet couvrant toute la pile : non trouvé.**

### SAV

CubeMars publie une politique datée du **14 mai 2025** :

- moteurs garantis **365 jours** ;
- RMA annoncé jusqu'à cinq jours ouvrés de traitement ;
- produit défectueux remplacé, ou avoir si indisponible/discontinué. :chatgpt-content-reference{index="16"}

C'est plus clair que chez beaucoup de fabricants chinois.

RobotShop Europe commercialise les AK et gère une infrastructure de retour aux Pays-Bas ; la disponibilité de certains AK reste toutefois « restocking/on demand », sans ETA ferme. :chatgpt-content-reference{index="17"}

**Suisse : revendeur spécialisé officiel d'actionneurs CubeMars identifié : non trouvé.**

### YXOR

Très bon choix industriel, mais il nous obligerait à **surdimensionner ou changer davantage les paliers moteurs**.

**Confiance : élevée.**

---

# 4. MyActuator

MyActuator est le fabricant qui m'inspire le plus confiance après ROBOTIS sur la **continuité protocolaire**.

Le téléchargement officiel propose aujourd'hui :

- protocole CAN **V4.4 — 20/05/2026** ;
- manuel X-Series V4 — septembre 2026 ;
- modèles 2D/3D ;
- anciennes générations encore documentées. :chatgpt-content-reference{index="18"}

C'est excellent en matière de traçabilité.

### Gamme

Il existe notamment :

- X6-7 ;
- X8-20 ;
- X4-36 ;
- et de nombreux modèles plus puissants. :chatgpt-content-reference{index="19"}

À première vue cela ressemble presque au triplet souhaité.

Mais problème : le **RMD-X8-P6-20 a reçu une annonce officielle de discontinuation** et MyActuator indique le X8-P9-32 comme remplaçant. :chatgpt-content-reference{index="20"}

C'est précisément pourquoi il ne faut pas seulement comparer des fiches produit.

### Ouverture

Protocoles publics et nombreuses implémentations communautaires.

Le SDK C++/Python communautaire RMD est sous licence MIT et dispose d'un historique significatif ; ce n'est toutefois pas le firmware du moteur. :chatgpt-content-reference{index="21"}

**Firmware embarqué source : non trouvé.**

### Distribution

C'est ici que MyActuator devient très intéressant pour YXOR-France : **A2V**, acteur français de la motorisation, distribue réellement des RMD et affiche du stock sur plusieurs références. :chatgpt-content-reference{index="22"}

**Distributeur officiel suisse identifié : non trouvé.**

### Pérennité

MyActuator est paradoxalement rassurant précisément parce qu'il **annonce les fins de série** au lieu de laisser simplement disparaître les produits. L'EOL X8-20 et son remplaçant sont explicitement documentés. :chatgpt-content-reference{index="23"}

**Confiance : élevée.**

Pour une entreprise voulant acheter et maintenir des robots plusieurs années, MyActuator est probablement plus rassurant que RobStride. Pour **notre triplet précis**, RobStride reste meilleur.

---

# 5. DAMIAO

Damiao dispose d'une gamme impressionnante et d'un écosystème en très forte croissance.

Le dépôt constructeur expose des SDK Python/C++, routines CAN, documentation MIT et outils. Le code courant connaît notamment DM4310, DM4340, DM6006, DM8006, DM8009, etc. :chatgpt-content-reference{index="24"}

Le très intéressant OpenArm et le reBot B601-DM de Seeed donnent désormais des exemples open source réels utilisant les DM4310 et DM4340. Le BOM reBot du **25 avril 2026** précise DM4310 V4 ×4 + DM4340P V4 ×3. :chatgpt-content-reference{index="25"}

### Attention aux chiffres

Les tables de SDK indiquent par exemple des **TMAX logiciels** de 10, 28, 12/20/40/54 N·m selon modèle/révision. Cela ne doit pas automatiquement être interprété comme un couple mécanique peak garanti par datasheet. Certaines versions du SDK elles-mêmes contiennent des valeurs différentes pour DM6006/DM8006. :chatgpt-content-reference{index="26"}

Pour notre étude fournisseur, c'est donc un **signal négatif de stabilité documentaire**.

### Gamme YXOR

Une classe basse autour de 7–10 N·m existe, puis plusieurs modèles 12–28 N·m, puis 40–54 N·m.

**Triplet vérifié ≈5–6 / 17 / 36 : non trouvé.**

### Ouverture

Très bons SDK/examples/protocole.

Mais l'outil constructeur DMTool reste propriétaire, et je n'ai pas trouvé de **firmware moteur complet sous licence open source**.

### UE/CH

Seeed constitue aujourd'hui le canal international le plus visible.

**Distributeur Damiao spécialisé Suisse : non trouvé.**

**RMA local suisse : non trouvé.**

**Garantie fabricant explicite en mois/années : non trouvée dans les sources officielles consultées.**

**Confiance : moyenne.**

---

# 6. Unitree

Unitree est un cas un peu différent.

Son ancien `unitree_actuator_sdk` est sous **BSD-3-Clause** et connaît GO-M8010-6, A1 et B1. Mais le code montre explicitement des différences internes : A1 à 4,8 Mbaud, B1 à 6 Mbaud, structures de messages distinctes GO vs A1/B1. :chatgpt-content-reference{index="27"}

Donc :

> même marque ≠ même protocole binaire.

Et le SDK contient également des bibliothèques compilées `libUnitreeMotorSDK_*.so`, donc l'ouverture n'est pas totale malgré la licence du wrapper. :chatgpt-content-reference{index="28"}

Le nouvel IM6014 fournit :

- 31,7 N·m dans un sens de couple/vitesse ;
- 34,4 N·m dans l'autre ;
- 535 g ;
- RS485 multipoint 4/6 Mbit/s ;
- double encodeur ;
- **garantie seulement 3 mois**. :chatgpt-content-reference{index="29"}

La nouvelle branche logiciel moteur continue aussi d'évoluer : `Unitree-Motor-Assistant` était encore mise à jour le **18 septembre 2026**. :chatgpt-content-reference{index="30"}

### Suisse : gros avantage

Il existe désormais un véritable partenaire officiel suisse :




Il se présente comme **Official Swiss partner of Unitree**, avec lab à Zürich, support, intégration et garantie sur les plateformes Unitree. :chatgpt-content-reference{index="33"}

Mais je n'ai pas trouvé de preuve que Synoptic stocke ou assure le SAV **des moteurs Unitree nus** tels que l'IM6014.

### Gamme YXOR

Classe ≈5–6 : **non trouvée**.

Classe ≈17 : **non trouvée correspondant à notre besoin**.

Classe ≈36 : IM6014 s'en approche très bien.

Donc ce n'est pas une architecture évolutive pour nos trois robots.

**Confiance : élevée sur ce constat.**

---

# 7. SteadyWin

SteadyWin est beaucoup plus intéressant qu'il n'y paraît.

Le GIM4310-10 existe par exemple en versions :

- 7,98 N·m stall avec GDZ34 ;
- **5,6 N·m stall avec GDS34**. :chatgpt-content-reference{index="34"}

La famille GIM6010 couvre ensuite des couples plus élevés ; le GIM6010-36 actuel affiche **41 ou 51,5 N·m stall** selon driver, pour 17,4–18 N·m nominal. :chatgpt-content-reference{index="35"}

Donc le catalogue permet clairement de faire évoluer la puissance.

### Le problème : driver/firmware

Les variantes changent entre GDZ34, GDS34, GDS68, GDS6, GDZ468H...

Et les historiques officiels montrent une évolution assez rapide du logiciel. Pour le GIM6010-8 :

- manuel rev 2.0 : 09/01/2025 ;
- rev 2.1 : 07/03/2025 ;
- rev 2.2 : 22/05/2025 ;
- firmware du 20/08/2025 corrige notamment sous/surtension et optimise MIT. :chatgpt-content-reference{index="36"}

C'est plutôt bon en transparence, mais cela signifie que je ne peux pas écrire **« même logiciel garanti sur tous les modèles »**.

### Documentation

Très bonne côté :

- manuels ;
- anciens manuels ;
- firmwares ;
- dessins 2D ;
- modèles 3D. :chatgpt-content-reference{index="37"}

### Europe

OpenELAB commercialise les GIM. Pour le GIM6010-36, la page vérifiée le 30/09/2026 indique expédition Chine **5–10 jours ouvrés** et possibilité de faire importer par leur structure UE ; leur politique de garantie/retour est datée du **17 juillet 2026**. :chatgpt-content-reference{index="38"}

**Revendeur suisse SteadyWin : non trouvé.**

**Confiance : moyenne.**

---

# 8. ROBOTIS

Si cette étude portait seulement sur la **qualité de l'écosystème**, ROBOTIS serait probablement la référence.

DYNAMIXEL Protocol 2.0 est officiellement commun aux familles **Y, P, X et MX(2.0)**. :chatgpt-content-reference{index="39"}

Le SDK officiel est Apache-2.0, avec plusieurs centaines de forks/stars et une longue histoire de maintenance. En 2026, les issues et mises à jour continuent d'être traitées. :chatgpt-content-reference{index="40"}

C'est aussi l'un des rares fabricants à avoir une vraie documentation de maintenance : remplacement de gears, calibration, diagnostic des moteurs brûlés/engrenages endommagés, etc. :chatgpt-content-reference{index="41"}

### Mais pour YXOR

La P-Series donne approximativement :

- PH42 : **5,1 N·m continu** ;
- PM54 : ≈10 N·m continu ;
- PH54-100 : ≈25,3 N·m continu ;
- PH54-200 : ≈44,7 N·m continu.

Ce ne sont pas des classes **5/17/36 peak** comparables aux petits QDD chinois ; elles sont sensiblement plus lourdes et sont spécifiées différemment. :chatgpt-content-reference{index="42"}

Techniquement, le même logiciel pourrait traverser les tailles. Mécaniquement et énergétiquement, ce n'est pas le robot que nous sommes en train de concevoir.

### Distribution

Generation Robots en France distribue DYNAMIXEL-P et apporte un vrai interlocuteur UE. :chatgpt-content-reference{index="43"}

**Fournisseur suisse disposant clairement du stock P-Series : non trouvé.**

**Confiance : très élevée.**

---

# 9. Feetech

Feetech est très intéressant dans le monde SO-ARM / petits humanoïdes, mais sa gamme se fragmente dès que le couple monte.

Le STS3215 actuel :

- ≈2,94 N·m stall à 12 V ;
- 1 N·m nominal environ ;
- bus série half-duplex jusqu'à 1 Mbit/s. :chatgpt-content-reference{index="44"}

Les modèles beaucoup plus puissants existent, mais passent dans d'autres familles, en RS485, CAN ou PWM selon modèle.

Donc :

**gamme 5 / 17 / 36 N·m avec même protocole : non trouvée.**

### Ouverture

Un dépôt Feetech public expose le SDK Python et indique provenir du dépôt officiel. :chatgpt-content-reference{index="45"}

Firmware embarqué ouvert : **non trouvé**.

### Communauté

L'énorme avantage est l'adoption dans les bras LeRobot/SO-ARM.

L'inconvénient est qu'on trouve aussi des retours de gears arrachés ou électroniques endommagées lorsque les STS3215 sont maintenus au stall. Ce sont **des témoignages individuels, pas un taux de panne statistique** ; il ne faut donc pas en tirer une estimation de fiabilité.

### Europe

RobotShop Europe vend activement Feetech, avec infrastructure SAV/retours à Venlo aux Pays-Bas. Au 30/09/2026, le STS3215 12 V était annoncé en réapprovisionnement sans ETA disponible. :chatgpt-content-reference{index="46"}

**Distributeur officiel suisse : non trouvé.**

**Confiance : élevée sur l'inadéquation à YXOR.**

---

# 10. mjbots / moteus

mjbots est presque l'opposé de Unitree : petit fabricant, mais **ouverture technique exemplaire**.

Le dépôt moteus contient :

- firmware ;
- designs PCB ;
- client software ;
- outils ;
- documentation ;

le tout essentiellement sous **Apache-2.0**. :chatgpt-content-reference{index="47"}

L'API Python/C++ reste activement développée — un exemple a encore un copyright **2026**. :chatgpt-content-reference{index="48"}

Le QDD100 utilise **CAN-FD 5 Mbit/s** et le même firmware moteus. :chatgpt-content-reference{index="49"}

Mais le problème est commercial :

au 30/09/2026, le **QDD100 beta 3 et son dev kit sont sold out**, tandis que le cœur actuel de l'offre mjbots est surtout constitué des contrôleurs moteus r4/c1/n1/x1. :chatgpt-content-reference{index="50"}

Et mjbots est extrêmement transparent : sa propre fiche QDD100 prévient que le produit est **beta**, que le hardware peut être peu fiable et que firmware/documentation n'ont pas encore été largement éprouvés. La garantie reste d'un an. :chatgpt-content-reference{index="51"}

Historiquement, le QDD100 Beta 2 était passé de 12,5 à **16 N·m peak** ; l'histoire de développement montre justement que mjbots mesurait et publiait les écarts entre couple théorique et couple réel. :chatgpt-content-reference{index="52"}

C'est un fabricant que j'apprécierais beaucoup pour un robot expérimental **ultra-open**, mais pas pour standardiser aujourd'hui YXOR 0.6/0.8/0.9.

**Confiance : élevée.**

---

# 11. ODrive

ODrive doit être mis dans une catégorie différente.

Ce n'est pas vraiment une gamme de **joint actuators intégrés** : tu choisis contrôleur, moteur, encodeur et éventuellement réducteur.

Cela apporte pourtant un avantage conceptuel énorme : **on peut garder le même logiciel et changer la motorisation indépendamment**.

Les ODrive Pro, S1 et Micro supportent tous CAN ; Pro/S1 partagent la nouvelle architecture firmware. :chatgpt-content-reference{index="53"}

Mais il y a eu un changement philosophique important :

- ancien ODrive v3.x : firmware open source ;
- Pro/S1/Micro : firmware actuel **non public**, éventuellement disponible sous NDA. :chatgpt-content-reference{index="54"}

Le v3.6 est officiellement **NRND / approaching end of life**, et ODrive recommande S1. C'est l'une des politiques de lifecycle les plus claires de cette comparaison. :chatgpt-content-reference{index="55"}

### Europe

Très gros avantage : ODrive exploite directement un **entrepôt aux Pays-Bas** pour l'UE. :chatgpt-content-reference{index="56"}

Garantie officielle :

**1 an**, réparation/remplacement/remboursement ; retours 30 jours pour produit neuf. :chatgpt-content-reference{index="57"}

### Pour YXOR

Si nous décidions un jour de développer **notre propre QDD YXOR**, ODrive redeviendrait extrêmement intéressant.

Pour la version actuelle où nous voulons acheter un actionneur intégré, il ajoute énormément de travail :

motor + reducer + housing + dual encoder + bearings + thermal design + cabling.

**Confiance : très élevée.**

---

# 12. Le critère réellement décisif : peut-on conserver le logiciel ?

Sur ce point, je découperais la question en quatre niveaux :

| Niveau de compatibilité | 0,6 → 0,8 → 0,9 m |
|---|---|
| Bus physique identique | RobStride : **oui, CAN** |
| Framing/protocole identique | RobStride : **oui en restant sur une même option protocolaire** |
| API/HAL identique | **Oui**, si YXOR possède son driver |
| Paramètres identiques | **Non** : limites torque/current/speed/thermal propres à chaque modèle |
| Connecteur exactement identique | **à ne pas supposer** |
| Bride exactement identique | **non** |
| Même tension nominale | RS05/RS02/RS06 peuvent être organisés autour de **48 V** ; RS01 est plutôt 36 V, donc je choisirais **RS02 plutôt que RS01** pour YXOR-0.8. :chatgpt-content-reference{index="58"} |

Et c'est la raison pour laquelle je choisirais **RS02 et non RS01 pour la classe 17 N·m**.

Cela donne :

**RS05 → RS02 → RS06**

avec :

**48 V → 48 V → 48 V**

et :

**CAN 1 Mbit/s → CAN 1 Mbit/s → CAN 1 Mbit/s**. :chatgpt-content-reference{index="59"}

C'est une propriété remarquablement intéressante pour YXOR.

---

# 13. Ma recommandation pour YXOR

Je partirais donc aujourd'hui sur cette architecture :

**YXOR-0.6**
→ RobStride **RS05 — 5,5 N·m / 191 g**

**YXOR-0.8**
→ RobStride **RS02 — 17 N·m / ≈400 g**

**YXOR-0.9**
→ RobStride **RS06 — 36 N·m / 621 g**

Le logiciel YXOR ne devrait toutefois **jamais connaître directement `RS05`, `RS02` ou `RS06`**.

Je créerais une abstraction :

```text
YXOR Joint API
     │
     ├── enable()
     ├── disable()
     ├── setPosition()
     ├── setVelocity()
     ├── setTorque()
     ├── setImpedance(kp, kd)
     ├── getState()
     └── getFaults()
            │
            ▼
     RobStrideBackend
            │
     ┌──────┼──────┐
     RS05   RS02   RS06
```

et les seules différences seraient dans un fichier de description :

```yaml
rs05:
  peak_torque: 5.5
  rated_torque: 1.6 # valeur à figer selon révision achetée
  voltage: 48
  protocol: robstride_can

rs02:
  peak_torque: 17
  rated_torque: 6.0 # à valider par lot/firmware
  voltage: 48
  protocol: robstride_can

rs06:
  peak_torque: 36
  rated_torque: 11
  voltage: 48
  protocol: robstride_can
```

Je stockerais surtout pour **chaque actionneur physique** :

`manufacturer + model + HW revision + FW revision + serial + spec revision`.

Ce détail paraît bureaucratique aujourd'hui ; avec les changements RS02 déjà constatés, il pourrait nous éviter énormément de problèmes dans deux ans.

---

# 14. Et je prévoirais mécaniquement la migration dès le premier YXOR

Je **ne dessinerais pas la jambe 0,6 m directement autour de la bride RS05**.

Je mettrais une interface YXOR :

```text
Structure de jambe
       │
       ▼
┌─────────────────┐
│ YXOR Joint Mount│   ← interface mécanique YXOR stable
└────────┬────────┘
         │
    Adapter plate
         │
 ┌───────┴────────┐
 RS05 / RS02 / RS06
```

Ainsi :

> **notre bride reste stable ; celle du fournisseur peut changer.**

C'est beaucoup plus important à long terme que d'essayer de trouver trois moteurs physiquement interchangeables.

---

# 15. Ce qui me ferait abandonner RobStride

Il y a cinq éléments précis qui pourraient renverser cette conclusion.

**1. Les essais thermiques RS05 échouent.**  
5,5 N·m est un **peak**, pas un couple que nous pouvons demander continuellement. Si notre simulation de marche montre qu'un genou reste fréquemment >2 N·m, le RS05 peut devenir trop petit.

**2. Les couples mesurés ne correspondent pas aux fiches.**  
Avant de figer YXOR-0.6, je veux un banc de test réel avec au moins **3 exemplaires RS05**, mesure courant→couple et échauffement.

**3. RobStride continue à modifier les caractéristiques sans PCN propre.**  
La transition 6→7 N·m et 1,6→1,8 N·m n'est pas grave techniquement ; elle est grave en termes de configuration management.

**4. Aucun canal SAV UE/CH crédible n'émerge.**  
Si YXOR devient un produit vendu, la différence entre envoyer un moteur en Chine et avoir un RMA France/Allemagne/Suisse devient décisive.

**5. CubeMars ou MyActuator sort une gamme 2027 correspondant réellement à ≈5 / 17 / 36 N·m.**  
Avec la maturité de leurs réseaux et de leurs procédures, ils pourraient alors dépasser RobStride.

---

## Conclusion

Pour **un prototype YXOR open source de 0,6 m qui doit devenir une famille 0,6 → 0,8 → 0,9 m**, mon choix à la date du **30 septembre 2026** est donc :

**RobStride RS05 → RS02 → RS06.**

Pas parce que RobStride est aujourd'hui le fabricant le plus mature — **ROBOTIS est plus mature**, CubeMars est plus éprouvé, MyActuator a une meilleure continuité documentaire et un meilleur accès français — mais parce que RobStride est actuellement le seul à résoudre presque parfaitement **notre problème précis de scaling** : **5,5 → 17 → 36 N·m, 48 V, CAN, même écosystème logiciel.** :chatgpt-content-reference{index="60"}

Je mets mon niveau de confiance à **moyen-élevé** : très élevé sur l'existence de cette gamme et sa compatibilité logique actuelle ; seulement moyen sur la stabilité des fiches, le recul terrain et la chaîne SAV européenne.

Et surtout, je considère **la décision fournisseur encore réversible** : l'architecture YXOR devrait explicitement séparer **interface mécanique, HAL moteur et protocole fabricant**, afin que changer de RobStride vers CubeMars/MyActuator/ODrive plus tard ne signifie jamais réécrire le robot.
