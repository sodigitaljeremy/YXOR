# RECHERCHE YXOR — LOT A  
## Procédés de fabrication, matériaux, tolérances et DFM

**Date de l’étude : 2 octobre 2026.**  
**Périmètre :** YXOR, humanoïde bipède ≈ 0,60 m, ≈ 8 kg, 12 articulations motorisées, pièces structurelles principalement en tôle métallique de 1 à 6 mm.

### Convention de lecture

J’utilise les catégories demandées :

- **[M]** : mesure, capacité ou résultat publié propre à une machine, un service ou un essai donné ;
- **[E]** : règle DFM/empirique, éventuellement issue d’un industriel ;
- **[N]** : valeur ou exigence normative légalement accessible.

Pour les propriétés matière « typiques » publiées par un producteur, j’emploie **[M-produit]** afin de ne pas les confondre avec une capacité machine.

**Confiance : A** = norme/fabricant de machine/producteur matière/mesure scientifique ; **B** = service industriel documentant explicitement son DFM ; **C** = source secondaire technique.

Les citations constituent les **liens vers les URL sources**. Toutes les sources web ont été consultées le **02/10/2026**, sauf indication contraire.

---

# 1. Découpe laser — fibre et CO₂

## 1.1 Un résultat fondamental pour YXOR

Il n'existe pas de valeur universelle telle que « le laser fait une saignée de X mm » ou « le laser tient ±Y mm ».

Deux niveaux doivent être absolument séparés :

| Grandeur | Exemple publié | Interprétation |
|---|---:|---|
| Répétabilité axes AMADA ENSIS-AJe | **±0,01 mm [M]** | répétabilité du positionnement machine, **pas tolérance de pièce** |
| Positionnement/répétabilité Prima Power Platino | **0,03 / 0,03 mm [M]** | performance machine ; la précision pièce dépend notamment de la géométrie et de l'application |
| Tolérance laser Protolabs | **±0,127 mm [M/E]** | engagement propre à ce service, 0,61–6,35 mm |
| Kerf Xometry « metal laser » | **0,203–0,305 mm [E/M]** | règle propre à leur service |
| Kerf Xometry laser générique | **≈0,508 mm [E/M]** | autre périmètre du même prestataire |
| Kerf scientifique inox 304, 4 mm | environ **0,138–0,185 mm [M]** selon réglage | essai fibre 2 kW précis |

AMADA annonce par exemple ±0,01 mm de répétabilité et, suivant puissance, jusqu'à 12–25 mm d'aluminium et 8–18 mm de laiton, tout en précisant que l'épaisseur maximale dépend de la qualité matière, de l'environnement et de la configuration. :chatgpt-content-reference{index="0"} Prima Power publie 0,03 mm de précision de positionnement et de répétabilité ; sa documentation précise par ailleurs que la précision de la pièce dépend du type, de la taille, du prétraitement et des conditions d'application. :chatgpt-content-reference{index="1"}

**Conclusion DFM : une spécification de répétabilité machine ne doit jamais être inscrite comme tolérance de contour garantie sur un plan YXOR.**

---

## 1.2 Géométrie minimale documentée

Il n'a pas été trouvé de tableau primaire fabricant de machine donnant, pour chacune des combinaisons :

> 5052 / 5754 / 5083 / 6061 / 6082 / 7075 / 304 / 316 / Ti Gr.2 / Ti Gr.5 / laiton × 1 / 2 / 3 / 4 / 5 / 6 mm

un minimum universel de trou, web, slot, rayon et distance bord.

**Cette matrice exacte = non trouvé.**

En revanche, plusieurs services industriels publient leurs limites réelles :

| Paramètre | Valeur | Nature | Conditions/source | Confiance |
|---|---:|---|---|---|
| trou, slot, découpe intérieure laser | ≈ **0,5 × t** | [E] | SendCutSend ; limite obtenue par essais de fabrication | B |
| bridge/web laser | ≈ **0,5 × t** minimum | [E] | SendCutSend | B |
| détail laser | ≥ **0,5 × t** | [E] | Xometry « metal laser » | B |
| slot | ≥ **1 × t** | [E] | Protolabs | B |
| trou laser | diamètre ≳ **1 × t** | [E] | Protolabs : plus petit que t difficile | B |
| feature laser générique Xometry | ≥ **2 × t**, minimum **1,575 mm** | [E] | périmètre Xometry générique | B |
| trou→bord Protolabs, t ≤0,914 mm | **1,574 mm** | [E] | service Protolabs | B |
| trou→bord Protolabs, t >0,914 mm | **3,175 mm** | [E] | service Protolabs | B |
| notch | ≥ max(**t**, **1,016 mm**) | [E] | Protolabs | B |
| longueur notch | ≤ **5× largeur** | [E] | Protolabs | B |
| tab | ≥ max(**2t**, **3,20 mm**) | [E] | Protolabs | B |
| longueur tab | ≤ **5× largeur** | [E] | Protolabs | B |
| trou→bord Xometry | min(**2t**, **3,175 mm**) | [E] | règle propre Xometry | B |
| trou→trou Xometry | min(**6t**, **3,175 mm**) | [E] | règle propre Xometry | B |
| relief | ≥ max(**t**, **0,254 mm**) | [E] | Xometry | B |

Sources : SendCutSend indique explicitement que ses minima ≈50 % de l'épaisseur résultent de tests où les géométries sont réduites jusqu'à apparition de défauts puis légèrement augmentées pour obtenir une fabrication fiable. :chatgpt-content-reference{index="2"} Protolabs demande trous et slots ≥ épaisseur et publie ses distances au bord. :chatgpt-content-reference{index="3"} Xometry publie simultanément ses règles propres de distances et ses minima de détails. :chatgpt-content-reference{index="4"}

### Conséquence importante

Les différences **0,5t / 1t / 2t** ne sont pas des erreurs : elles correspondent à des objectifs différents :

- limite expérimentale d'un parc machine/service ;
- feature « réalisable » ;
- feature recommandée avec marge DFM ;
- niveau de qualité souhaité ;
- matériau, gaz, puissance, focus, stratégie de perçage et CAM différents.

Il serait donc faux de décréter que « le laser permet universellement 0,5t ».

---

# 1.3 Règle prudente par épaisseur pour YXOR

Voici une **enveloppe DFM de conception**, pas les limites physiques d'un laser.

| t | Trou/slot de base ≥ t | Web structurel recommandé ≥1,5t | Feature compatible avec règle très conservatrice 2t |
|---:|---:|---:|---:|
| 1 mm | 1 mm | 1,5 mm | 2 mm |
| 2 mm | 2 mm | 3 mm | 4 mm |
| 3 mm | 3 mm | 4,5 mm | 6 mm |
| 4 mm | 4 mm | 6 mm | 8 mm |
| 5 mm | 5 mm | 7,5 mm | 10 mm |
| 6 mm | 6 mm | 9 mm | 12 mm |

**Interprétation :**

- **d ≥ t** est une bonne règle DFM de départ pour les trous/slots découpés laser ; elle est plus prudente que le 0,5t démontré par certains parcs. :chatgpt-content-reference{index="5"}
- **1,5t pour les webs structurels** est une synthèse prudente : SendCutSend prouve que ~0,5t est parfois manufacturable mais des éléments aussi fins deviennent sensibles à l'échauffement, à la rigidité de la pièce et à la manutention. :chatgpt-content-reference{index="6"}
- **2t n'est pas une loi physique** ; c'est une enveloppe de compatibilité avec une recommandation Xometry plus sévère. :chatgpt-content-reference{index="7"}

Pour YXOR, les très petits perçages fonctionnels destinés à l'assemblage, aux roulements, axes ou positionnements ne devraient donc **pas être supposés finis au laser** simplement parce que leur diamètre est géométriquement réalisable.

---

# 1.4 Saignée / kerf

| Source | Procédé/conditions | Kerf | Nature |
|---|---|---:|---|
| Xometry Metal Laser | laser métal, gamme service | **0,008–0,012" = 0,203–0,305 mm** | [E/M] |
| Xometry Laser générique | service laser | **≈0,020" = 0,508 mm** | [E/M] |
| Scientific Reports 2025 | fibre, AISI 304, t=4 mm, 2 kW, N₂ 14 bar | env. **0,138–0,185 mm** selon paramètres | [M] |
| Flow waterjet pour comparaison | abrasif | **0,762–1,016 mm** | [M] |

Xometry publie explicitement 0,203–0,305 mm pour son service métal. :chatgpt-content-reference{index="8"} Sa page générale affiche toutefois ≈0,508 mm. :chatgpt-content-reference{index="9"} L'étude 2025 sur inox 304 de 4 mm confirme qu'un système fibre bien déterminé produit des valeurs sensiblement plus faibles, ce qui démontre l'influence majeure du procédé et du réglage. :chatgpt-content-reference{index="10"}

### Valeur YXOR prudente

Pour **dimensionner l'espacement de petites géométries avant connaissance du parc machine**, considérer **0,5 mm comme enveloppe conservatrice de kerf**.

Mais :

> **ne pas appliquer manuellement ±0,25 mm aux contours CAO** sans le demander au fabricant.

Un logiciel CAM industriel compense normalement la trajectoire du faisceau. La valeur importante pour le concepteur est donc moins le kerf brut que la **tolérance dimensionnelle garantie après compensation**.

---

# 1.5 Tolérances de découpe

Protolabs publie actuellement **±0,127 mm pour toutes les features laser** sur 0,61–6,35 mm dans son service dédié. :chatgpt-content-reference{index="11"} Ses autres documents de tôlerie publient également ±0,127 mm sur les trous découpés. :chatgpt-content-reference{index="12"}

Cela ne rend pas ±0,127 mm universel.

### Base YXOR

- **±0,1–0,15 mm :** atteignable chez certains services laser documentés ;
- **±0,4 à ±0,5 mm :** enveloppe beaucoup plus robuste si le parc, le matériau, la taille de pièce et la stratégie de découpe sont inconnus ;
- **H7, logements de roulement, axes précis :** ne jamais dériver de la tolérance laser générale.

**Tolérance de position spécifique, circularité, perpendicularité des petits trous, conicité exacte par alliage × épaisseur : non trouvé sous forme de matrice publique suffisamment robuste.**

ISO 9013 est précisément la norme à employer pour définir/classer la qualité géométrique des coupes thermiques plutôt que d'inventer ces valeurs. :chatgpt-content-reference{index="13"}

---

# 1.6 Petites pointes et angles aigus

Des pointes très étroites combinent :

- forte densité d'énergie ;
- très faible masse thermique ;
- petits webs résiduels ;
- risque de brûlure locale/déformation.

SendCutSend documente ce phénomène via ses minima de bridge et rapporte des risques de gauchissement sur les géométries longues et minces. :chatgpt-content-reference{index="14"}

**Angle aigu minimal universel en degrés : non trouvé.**

La bonne pratique YXOR consiste donc à appliquer les **contraintes de largeur résiduelle/web**, plutôt qu'un angle minimum arbitraire.

---

# 1.7 Micro-joints

Les micro-joints servent à maintenir de petites pièces dans la tôle pendant la découpe ; ils laissent ensuite un point d'attache à casser/ébavurer.

TRUMPF distingue également ses approches de micro-joints/nano-joints destinées à stabiliser les pièces et à limiter les marques.

**Largeur numérique universelle du micro-joint par alliage/t : non trouvé.**

Pour YXOR, leur géométrie doit rester **paramètre CAM du fabricant**, sauf accord explicite pour les modéliser dans la pièce.

---

# 1.8 Effets thermiques et HAZ

L'étude ouverte Scientific Reports 2025 sur **AISI 304, t=4 mm, fibre 2 kW, N₂ 14 bar** constitue une bonne illustration de la dépendance aux réglages :

- vitesse **1,5 m/min → HAZ moyenne ≈102 µm** ;
- vitesse **2,0 m/min → ≈56,7 µm**.

Il s'agit exclusivement de cet essai. :chatgpt-content-reference{index="15"}

L'étude expérimentale sur 6061-T6 montre également que puissance, vitesse, épaisseur et distance buse-pièce influencent fortement la température et la qualité de bord ; elle utilisait notamment un **CO₂ Bystronic Bystar 4025, 4 kW maximum, avec azote**. :chatgpt-content-reference{index="16"}

### 6061-T6 / 6082-T6 / 7075-T6

Le point essentiel n'est pas uniquement la largeur visuelle de la HAZ : ces alliages tirent leur résistance d'un état de précipitation contrôlé.

Une excursion thermique suffisante peut :

- sur-vieillir ou dissoudre localement les précipités ;
- réduire localement dureté et limite élastique ;
- produire une zone mécaniquement différente du matériau nominal.

Hydro rappelle explicitement que le traitement thermique influence la résistance locale des 6xxx et que 6082-T6 perd de la résistance dans les zones affectées par la chaleur lors d'un assemblage thermique. :chatgpt-content-reference{index="17"}

Pour **6061-T6/6082-T6/7075-T6/T651 découpés laser fibre et CO₂, t=1–6 mm**, une série primaire publique permettant de donner une HAZ mécanique en µm pour chaque combinaison a été recherchée mais :

**non trouvé.**

On ne doit surtout pas réutiliser comme « HAZ laser » une largeur publiée pour du soudage MIG/TIG ou friction stir welding.

---

# 1.9 Contraintes résiduelles et distorsion

La chauffe très localisée produit gradients thermiques et contraintes transitoires ; les géométries ouvertes, longues et étroites y sont les plus sensibles. Des travaux sur 6061-T6 montrent explicitement la relation entre température de coupe, épaisseur, puissance/vitesse et contraintes/qualité. :chatgpt-content-reference{index="18"}

**Limite chiffrée universelle de longueur/largeur garantissant absence de gauchissement : non trouvé.**

Pour YXOR, les zones les plus à surveiller seront donc :

- bras longs/minces ;
- grandes évidements d'allègement ;
- réseaux de slots ;
- ligaments près du bord ;
- pièces asymétriques fortement ajourées.

---

# 1.10 Fibre versus CO₂

TRUMPF documente directement un avantage essentiel des sources solides/fibre modernes : résistance aux réflexions de retour et découpe fiable de métaux fortement réfléchissants tels que **cuivre et laiton** ; le constructeur cite aussi les métaux non ferreux et le titane. :chatgpt-content-reference{index="19"}

| Critère | Fibre / solid-state | CO₂ |
|---|---|---|
| tôle fine métallique | généralement très performant | capable mais aujourd'hui moins dominant |
| Al/laiton/cuivre | très adapté sur systèmes modernes protégés contre back-reflection | historiquement plus délicat |
| épaisseur YXOR 1–6 mm | plage très pertinente | également possible |
| kerf | souvent plus étroit dans une configuration comparable, mais valeur universelle non trouvée | dépend optique/process |
| précision globale | dépend machine + process + tôle, pas seulement source | idem |
| énergie/maintenance | avantage généralement au fibre moderne | optique CO₂ plus complexe |
| qualité sur tôle plus épaisse | dépend puissance et procédé ; pas de seuil universel | certaines configurations restent compétitives |

**Pour 1–6 mm, aucune raison documentaire ne permet de décréter CO₂ « plus précis ».**

---

# 2. Jet d'eau et plasma — comparaison courte

## 2.1 Jet d'eau abrasif

Flow publie :

- précision jusqu'à **±0,001" = ±0,0254 mm [M]** avec ses technologies Dynamic avancées ;
- kerf typiquement **0,030–0,040" = 0,762–1,016 mm [M]** ;
- **aucune HAZ** et aucune distorsion thermique induite. :chatgpt-content-reference{index="20"}

Pour un service industriel générique, Xometry publie plutôt :

- feature minimale = **2t**, avec minimum **3,175 mm [E]** ;
- kerf ≈ **1,575 mm [M/E]** ;
- légère conicité possible. :chatgpt-content-reference{index="21"}

SendCutSend indique **1,778 mm** comme minimum courant pour des trous/cutouts waterjet. :chatgpt-content-reference{index="22"}

**Rayon interne waterjet documenté chez SendCutSend : 0,032" = 0,813 mm [M/E]** pour leur procédé. :chatgpt-content-reference{index="23"}

### Cas où il devient intéressant pour YXOR

Le waterjet prend du sens lorsque **préserver intégralement l'état thermique du matériau** est plus important qu'obtenir le kerf le plus fin, notamment pour certaines pièces T6/T651 ou titane.

---

## 2.2 Plasma

Hypertherm publie pour ses procédés :

| Procédé | Précision | Biseau | Petit trou |
|---|---:|---:|---:|
| plasma conventionnel | **≈0,76 mm [M]** | **3–5°**, parfois ~1° | — |
| plasma haute tolérance | **≈0,25 mm [M]** | **0–3°** | **≈4,76 mm [M]** | :chatgpt-content-reference{index="24"}


Le plasma possède une HAZ et des bords présentant généralement plus de taper/variation que le laser. Pour les pièces structurelles relativement petites, fines et précises de YXOR en aluminium 1–6 mm, **les données trouvées ne montrent pas d'avantage DFM général sur le laser**.

Il devient surtout pertinent si priorité est donnée au débit/coût de coupe et si les tolérances fines ne sont pas nécessaires.

---

# 3. Pliage de tôle

## 3.1 Le rayon minimal n'est pas une propriété unique de « l'aluminium »

L'Aluminum Association indique explicitement qu'il dépend de :

- alliage ;
- état métallurgique ;
- épaisseur ;
- orientation du pli par rapport au grain ;
- angle de pliage.

Ses tableaux détaillés se trouvent notamment dans l'Aluminum Design Manual et ne doivent pas être remplacés par une pseudo-règle universelle. :chatgpt-content-reference{index="25"}

---

# 3.2 5052-H32 — données particulièrement solides

Atlas publie les rayons minimaux pour un pli à **90° par rapport au sens de laminage** :

| Épaisseur documentée | Rayon intérieur min. 5052-H32 | Nature |
|---:|---:|---|
| 0,4 mm | **0t** | [E/producteur] |
| 0,8 mm | **0t** | [E/producteur] |
| 1,6 mm | **1t** | [E/producteur] |
| 3,2 mm | **1,5t** | [E/producteur] |
| 4,8 mm | **1,5t** | [E/producteur] |
| 6,0 mm | **1,5t** | [E/producteur] | :chatgpt-content-reference{index="26"}


### Base prudente YXOR

Pour simplifier le modèle DFM et ne pas dépendre de l'orientation :

**5052-H32 → Rᵢ ≥ 1,5t** sur la plage YXOR.

C'est volontairement plus conservateur que les minima documentés à faible épaisseur.

---

# 3.3 5754-H111

BIKAR publie des valeurs **informatives** adossées à EN 485-2 :

| t | R min 90° |
|---:|---:|
| 0,2–0,5 mm | **0t** |
| 0,5–1,5 mm | **0,5t** |
| 1,5–3 mm | **1t** |
| 3–6 mm | **1t** |
| 6–12,5 mm | **2t** |

Le document précise explicitement que ces rayons sont **informatifs**. :chatgpt-content-reference{index="27"}

Pour YXOR, **1,5t** constitue une enveloppe prudente simple entre 1 et 6 mm si l'on veut davantage de marge que les valeurs informatives.

### 5754-H22

Le même document mentionne H22 comme état disponible mais ne donne pas dans le tableau reproduit les mêmes rayons spécifiques.

**R/t exact 5754-H22 × 1–6 mm : non trouvé dans une source primaire gratuite satisfaisante.**

---

# 3.4 5083-H111 / H116

Hydro confirme 5083-H116 comme produit tôle/plaque et publie ses propriétés physiques. :chatgpt-content-reference{index="28"} Hydro publie également des propriétés mécaniques typiques de 5083-H111. :chatgpt-content-reference{index="29"}

Mais pour les **rayons de pliage exacts de H111/H116 en 1–6 mm**, une table primaire gratuite comparable à celle du 5052 :

**non trouvé.**

Il serait méthodologiquement incorrect de transposer automatiquement les valeurs du 5052 ou du 5754 au 5083.

---

# 3.5 6061-T6/T651

Le 6061-T6 est sensiblement moins tolérant au pliage serré que le 5052-H32.

L'Aluminum Association confirme que le rayon dépend de l'état, épaisseur et grain. :chatgpt-content-reference{index="30"} Des tableaux industriels reprenant les recommandations AA conduisent approximativement à :

- autour de **1,5t à ~1,6 mm** ;
- **2,5t à ~3,2 mm** ;
- **3t à ~4,8 mm** ;
- **3,5t à ~6,35 mm**.

Ces valeurs doivent rester classées **[E-C/B]**, pas normatives.

### Base prudente YXOR

Pour un dessin générique avant validation du plieur :

| plage | enveloppe prudente |
|---|---:|
| 1–2 mm | **R ≥ 2t** |
| 3–4 mm | **R ≥ 3t** |
| 5–6 mm | **R ≥ 3,5t** |

Ce tableau est une **synthèse conservatrice**, pas une citation de norme.

T651 est surtout courant sur plaque usinée ; sa disponibilité tôle mince exacte 1–6 mm n'a pas été suffisamment documentée dans les producteurs examinés.

---

# 3.6 6082-T6

Hydro indique :

- bonne usinabilité en T5/T6 ;
- bonne résistance à la corrosion ;
- traitements/assemblages thermiques susceptibles de réduire localement la résistance. :chatgpt-content-reference{index="31"}

La documentation primaire gratuite étudiée ne donne toutefois pas un tableau de **rayons minimaux pour tôle laminée 6082-T6 de 1 à 6 mm**.

**Valeur primaire : non trouvé.**

Des guides industriels secondaires utilisent parfois environ **6t** pour du T6 sévère. Cette valeur peut servir uniquement de **borne DFM temporaire [E-C]**, pas de valeur normative.

---

# 3.7 7075-T6/T651

La situation est encore plus restrictive.

Les services de tôlerie documentent souvent le T6 comme matériau à risque de fissuration au pliage. La littérature aéronautique secondaire conduit couramment à plusieurs épaisseurs de rayon, typiquement de l'ordre de **5–7t** selon épaisseur et orientation.

### Base YXOR

**Le LOT A ne retient pas le 7075-T6/T651 comme matériau à plier à rayon serré sans qualification spécifique.**

Une valeur universelle 1–6 mm :

**non trouvé.**

Pour la CAO générique, une pièce en 7075 devrait donc être considérée comme **usinée / plate** jusqu'à validation formelle d'un process de pliage.

---

# 3.8 Titane

TIMET donne des informations primaires particulièrement utiles.

### Grade 2 — TIMETAL 50A

Données typiques :

- rayon de pliage : **2,5t** ;
- densité : **4,51 g/cm³** ;
- E : **105–120 GPa** ;
- Rp0,2 typique : **345 MPa** ;
- Rm : **485 MPa** ;
- A : **28 %**. :chatgpt-content-reference{index="32"}

Le manuel TIMET donne cependant, pour les exigences ASTM B265 de pliage à température ambiante :

- Grade 2, t ≤0,070" ≈1,78 mm : **4t** ;
- 0,070–0,375" ≈1,78–9,53 mm : **5t**. :chatgpt-content-reference{index="33"}

C'est une divergence importante : **2,5t est une valeur typique produit, 4–5t correspond à une exigence/borne ASTM rapportée par TIMET**.

### Valeur prudente YXOR Grade 2

**Rᵢ ≥5t** si l'objectif est de couvrir 1–6 mm sans essai préalable.

---

### Ti-6Al-4V Grade 5

TIMET publie :

- density **4,42 g/cm³** ;
- E **105–120 GPa** ;
- Rp0,2 typique **980 MPa** ;
- Rm **1035 MPa** ;
- A **12 %** ;
- rayon typique sur tôle 2 mm : **5t**. :chatgpt-content-reference{index="34"}

Mais son manuel de formage, reprenant les exigences ASTM B265, donne à température ambiante :

- **9t** jusqu'à 0,070" ;
- **10t** de 0,070" à 3/8". :chatgpt-content-reference{index="35"}

### Valeur prudente YXOR Grade 5

**Rᵢ ≥10t** sans qualification particulière.

Cela montre pourquoi prendre « 5t » hors contexte aurait été dangereux.

---

# 3.9 Inox 304 / 316 et laiton

Pour 304/316, une règle industrielle générique de **~1–1,5t** existe dans de nombreux guides de press-brake, mais une matrice primaire suffisamment précise distinguant :

- nuance ;
- état de laminage ;
- sens du grain ;
- t=1…6 mm ;
- méthode de pliage

n'a pas été trouvée dans les producteurs étudiés.

**Valeur primaire exacte : non trouvé.**

Pour une CAO préliminaire YXOR, **1,5t [E]** est une enveloppe industrielle raisonnable, mais elle doit être validée avec l'outillage réel.

Pour le **laiton CuZn37**, KME publie des propriétés et des essais de pliage suivant états, mais ses données de petits rayons trouvées concernent principalement des bandes ≤0,5 mm ; elles ne justifient pas une extrapolation à 1–6 mm.

**R/t laiton courant 1–6 mm : non trouvé.**

---

# 3.10 Géométrie autour du pli

### Bend relief

SendCutSend publie :

- largeur ≥ **0,5t** ;
- profondeur ≥ **R + t + 0,020" ≈ R+t+0,508 mm**. :chatgpt-content-reference{index="36"}

### Features près du pli

Protolabs demande pour les slots :

**distance à la ligne de pli ≥4t [E]**. :chatgpt-content-reference{index="37"}

Dans un autre guide, il recommande également trous/slots à environ **4t** de tout pli/feature. :chatgpt-content-reference{index="38"}

SendCutSend relie plutôt la zone à risque à la largeur réelle de matrice : la déformation dépend donc directement du V utilisé. :chatgpt-content-reference{index="39"}

### Règle prudente YXOR

Tant que **V** n'est pas connu :

> distance feature → ligne de pli ≥ **4t**

et, une fois l'outillage connu :

> vérifier également que la feature est suffisamment en dehors de la zone d'appui de la matrice.

---

# 3.11 Bend allowance, K-factor, neutral axis

Formule de base :

\[
BA = \frac{\pi}{180}\,A(R+Kt)
\]

où :

- \(A\) = angle de pli ;
- \(R\) = rayon intérieur ;
- \(t\) = épaisseur ;
- \(K\) = position normalisée de la fibre neutre.

Le point critique :

> **K n'est pas une constante du 5052, du 6061 ou de l'inox.**

SendCutSend publie par exemple pour son **5052** des K-factors d'environ **0,37 à 0,48** suivant épaisseur/outillage. Son calculateur lie directement K, rayon effectif, V-die, bend deduction et flange minimum. :chatgpt-content-reference{index="40"}

### Base YXOR

Un **K≈0,40** peut être utilisé uniquement pour une toute première esquisse de flat pattern.

Pour une pièce à produire :

**K / BA / BD doivent être issus de la combinaison réelle matériau + épaisseur + V + poinçon + presse.**

---

# 3.12 Springback

Le manuel TIMET montre bien pourquoi le retour élastique ne peut pas être ignoré : pour le titane, il annonce typiquement une perte de **15 à 25° d'angle inclus** après formage, plus importante avec les alliages les plus résistants. :chatgpt-content-reference{index="41"}

Une valeur universelle pour aluminium/inox/laiton × t=1–6 mm :

**non trouvé.**

L'angle final doit donc être une **caractéristique de process**, pas une correction CAO arbitraire.

---

# 3.13 Sens de laminage

L'Aluminum Association confirme explicitement que le rayon minimal dépend de l'orientation du pli par rapport au grain. :chatgpt-content-reference{index="42"}

Atlas précise par exemple que ses valeurs 5052 sont données pour un pli à **90° par rapport à la direction de laminage**. :chatgpt-content-reference{index="43"}

### DFM

Pour les alliages difficiles à former — notamment T6/T651 — il est prudent de considérer que la direction de laminage **fait partie de la définition matière de la pièce**, plutôt que de laisser le nesting tourner librement la pièce sans validation.

---

# 4. Fraisage CNC 3 axes / 5 axes

## 4.1 Tolérances réalistes

Protolabs publie :

- usinage standard : **±0,005" = ±0,127 mm [M]** ;
- précision standard : **±0,002" = ±0,051 mm [M]** ;
- alésage/alésoir : jusqu'à **±0,0002" = ±0,00508 mm [M]** sur certaines capacités ;
- position entre features usinées sur la même face : **±0,051 mm [M]**. :chatgpt-content-reference{index="44"}

Sa page actuelle basée sur ISO 2768 donne aussi, pour aluminium « fine » :

- 0,5–6 mm : **±0,05 mm** ;
- >6–30 : **±0,10 mm** ;
- >30–120 : **±0,15 mm** ;
- >120–400 : **±0,20 mm**. :chatgpt-content-reference{index="45"}

### 3 axes versus 5 axes

Une règle robuste du type :

> 3 axes = ±X ; 5 axes = ±Y

**non trouvé**.

Ce serait de toute façon trompeur : la précision finale dépend plus de la machine, calibration, chaîne cinématique, serrage, longueur d'outil, thermique, stratégie CAM et nombre de reprises que du seul nombre d'axes.

Le principal avantage du 5 axes pour YXOR est souvent de **réduire les reprises/repositionnements**, pas une garantie intrinsèque d'une meilleure tolérance.

---

# 4.2 Parois, poches et rayons

Les guides industriels convergent vers les principes suivants :

| Géométrie | Base documentée | Base prudente YXOR |
|---|---:|---:|
| paroi métallique fine | ~0,5–0,8 mm possible suivant service | **≥0,8 mm**, idéalement ≥1 mm si haute |
| rapport hauteur/paroi | certains guides ≤~10:1 | **≤10:1** |
| profondeur de poche | souvent ~4× largeur/diamètre outil recommandé | **≤4D outil** sans nécessité spéciale |
| trous profonds | ~4D recommandé ; plus profond possible avec techniques dédiées | **≤4D** par défaut |
| fond mince | ~0,75–0,8 mm dans certains services | **≥0,8 mm** |
| rayon interne | nécessaire car fraise cylindrique | > rayon fraise ; laisser marge CAM |

Protolabs confirme une tolérance générale de ±0,13 mm comme base économique. :chatgpt-content-reference{index="46"}

**Rayon intérieur universel en mm : non trouvé**, puisqu'il dépend de la profondeur et du diamètre d'outil retenu.

Pour YXOR, une règle beaucoup plus utile est :

> ne jamais concevoir un rayon exactement égal au rayon théorique de la plus petite fraise envisagée ; laisser un rayon supérieur pour éviter l'engagement à 100 % dans le coin.

---

# 4.3 Alésages et H7

ISO 286-1:2010 est toujours courante en 2026 ; ISO 286-2:2010 contient les tables de déviations. :chatgpt-content-reference{index="47"}

Les tables de référence reproduites légalement par MISUMI permettent de retrouver les ordres de grandeur H7 :

| diamètre nominal | trou H7 |
|---|---:|
| ≤3 mm | **0 / +10 µm** |
| >3–6 mm | **0 / +12 µm** |
| >6–10 mm | **0 / +15 µm** |
| >10–18 mm | **0 / +18 µm** |
| >18–30 mm | **0 / +21 µm** | :chatgpt-content-reference{index="48"}


On voit immédiatement l'écart avec un usinage général à ±0,1 mm.

### Conclusion YXOR

Un logement **H7** doit être explicitement identifié comme feature fonctionnelle et traité par :

- alésoir ;
- alésage de précision ;
- interpolation circulaire qualifiée ;
- puis contrôle dimensionnel.

Il ne doit jamais hériter par défaut de la tolérance générale CNC.

Protolabs publie justement des capacités spécifiques d'alésage plus serrées que son ±0,127 mm général. :chatgpt-content-reference{index="49"}

---

# 4.4 Taraudages M2 à M6

Pour filet métrique ISO standard :

| Filetage | Pas | plage diamètre pré-usiné acceptée par Protolabs |
|---|---:|---:|
| M2 | 0,40 | **1,57–1,68 mm** |
| M2.5 | 0,45 | **2,01–2,14 mm** |
| M3 | 0,50 | **2,46–2,60 mm** |
| M4 | 0,70 | **3,24–3,42 mm** |
| M5 | 0,80 | **4,14–4,33 mm** |
| M6 | 1,00 | **4,92–5,15 mm** |

Profondeurs filetées maximales du service :

- M2 : **5,08 mm** ;
- M2.5 : **5,08 mm** ;
- M3 : **7,62 mm** ;
- M4 : **10,16 mm** ;
- M5 : **15,24 mm** ;
- M6 : **16,51 mm**. :chatgpt-content-reference{index="50"}

Guhring publie des plages comparables pour ses tarauds de coupe, par exemple M2 **1,567–1,679 mm**, M2.5 **2,013–2,138**, M3 **2,459–2,599 mm**. :chatgpt-content-reference{index="51"}

### Diamètres nominaux usuels simples

Pour la CAO YXOR, les valeurs classiques situées au cœur de ces plages sont :

| M | pré-perçage nominal pratique |
|---|---:|
| M2×0,4 | **1,6 mm** |
| M2.5×0,45 | **2,05 mm** |
| M3×0,5 | **2,5 mm** |
| M4×0,7 | **3,3 mm** |
| M5×0,8 | **4,2 mm** |
| M6×1,0 | **5,0 mm** |

Mais le diamètre optimal dépend aussi du type de taraud et du pourcentage de filet.

### Profondeur utile dans l'aluminium

Une règle structurale universelle « X×D suffit toujours dans l'aluminium » n'a pas été trouvée dans une source primaire gratuite couvrant tous les alliages/charges.

**Engagement minimal structurel garanti : non trouvé.**

Pour les trous borgnes il faut réserver de la profondeur supplémentaire :

- entrée du taraud ;
- pointe de foret ;
- copeaux ;
- portion non filetée du taraud.

Cette dimension devra passer au LOT B avec la visserie/charge réelle.

---

# 5. Tolérances et normes

## État au 02/10/2026

| Norme | État 2026 | Objet | Prix officiel observé | Remarque |
|---|---|---|---:|---|
| **ISO 2768-1:1989** | **active/courante** | tolérances générales linéaires/angulaires | **CHF 67** | confirmée 2022 |
| **ISO 2768 Ed.2** | **under publication** | remplacera 2768-1 | non encore prix final trouvé | stade 60.00 depuis 02/06/2026 |
| **ISO 2768-2:1989** | **withdrawn** | anciennes tolérances géométriques générales | — | remplacée par 22081 |
| **ISO 22081:2021** | **active**, confirmée 2026 | spécifications géométriques et de taille générales | **CHF 135** | Ed.1 |
| **ISO 9013:2017** | **active** | qualité/tolérance coupes thermiques | **CHF 159** | amendement 2024 CHF 18 |
| **ISO 1101:2017** | **active** | langage GD&T ISO | **CHF 227** | confirmée 2022 |
| **ISO 286-1:2010** | **active** | bases des ajustements | **CHF 181** | confirmée 2026 |
| **ISO 286-2:2010** | **active** | écarts/tables trous-arbres | **CHF 204** | confirmée 2021 |
| **ASME Y14.5-2018 (R2024)** | active/réaffirmée | GD&T américain | **USD 380** PDF/print selon option actuelle | édition 2018 |
| **JIS B 0405:1991** | **active** | tolérances générales | **¥1 650 JP / ¥7 260 anglais** | confirmée 20/06/2025 |
| **JIS B 0401-2:2016** | **active** | tables ajustements, identique ISO 286-2 | **¥5 390 JP** | confirmée 20/06/2025 |
| **GB/T 1804-2000** | **active**, révision décidée | tolérances générales CN | prix officiel : **non trouvé** | équivalent ISO 2768-1 |
| **ANSI H35.2 / H35.2M-2024** | active | tolérances produits aluminium | **USD 180 non-membre / 90 membre** | AA |
| **JIS H 4000:2022** | active | tôles/bandes aluminium | prix exact actuel dans cette vérification : non trouvé ici | norme produit, pas manuel DFM |
| **EN 485-2** | édition actuelle nationale selon organisme | propriétés mécaniques produits Al | texte payant | ne contient pas une règle générale de press-brake |

Sources ISO : :chatgpt-content-reference{index="52"}  
Japon/Chine : :chatgpt-content-reference{index="53"}  
ASME : :chatgpt-content-reference{index="54"}  
Aluminum Association : :chatgpt-content-reference{index="55"}

### Point crucial

Contrairement à ce que l'on rencontre encore sur de nombreux plans :

> **ISO 2768-2:1989 n'est plus courante.**

Elle a été retirée et remplacée par ISO 22081:2021. :chatgpt-content-reference{index="56"}

En revanche :

> **ISO 2768-1:1989 est toujours courante au 02/10/2026**, même si sa remplaçante, ISO 2768 édition 2, est déjà dans les dernières étapes de publication. :chatgpt-content-reference{index="57"}

---

## Prix demandés au 01/10/2026

Je n'ai pas trouvé d'archive officielle horodatée garantissant que les prix affichés **le 01/10** étaient exactement ceux visibles lors de ma consultation du **02/10/2026**.

Je ne les antidate donc pas artificiellement.

Les prix ci-dessus sont :

> **prix officiels affichés au 02/10/2026 ; valeur exacte archivée au 01/10/2026 = non trouvé.**

---

# 6. Matériaux

Les valeurs suivantes doivent être lues avec leur **état précis**. Une valeur « 6061 » sans état métallurgique n'est pas suffisante pour dimensionner YXOR.

| Matériau | ρ g/cm³ | E GPa | Rp0,2 | Rm | A | Observations documentaires |
|---|---:|---:|---:|---:|---:|---|
| **5052-H32** | ≈2,68 | ≈70 | ≥160 MPa selon produit/épaisseur documenté | 215–265 MPa | typ. ≈11 % plage t correspondante | excellent pliage/corrosion, soudable ; R min documenté 1–1,5t selon t |
| **5754-H111/O** | 2,67–2,70 | 70–70,5 | ≥80 MPa selon EN-derived table | 190–240 MPa | 14–18 % entre 0,5–6 mm | excellente formabilité/corrosion |
| **5754-H22** | ≈2,67 | ≈70,5 | exact primaire gratuit retenu : **non trouvé** | **non trouvé** | **non trouvé** | ne pas substituer H111 |
| **5083-H111** | ≈2,66 | ≈70 | Hydro typ. **165 MPa** | **275 MPa** | non trouvé dans source résumée | marin/corrosion, soudable |
| **5083-H116** | **2,66** | ≈70 | dépend épaisseur/spécification | dépend épaisseur | dépend épaisseur | état marin ; tôle/plaque documentée |
| **6061-T6** | **2,70** | **68,9** | typ. **276 MPa** ; minimum produit Hydro extrudé 240 MPa ≤6,3 mm | typ. **310 MPa** | typ. **12 %** à ~1,6 mm | bonne usinabilité/corrosion/soudabilité ; T6 thermosensible |
| **6061-T651** | ≈2,70 | ≈69 | ordre de grandeur T6/T651, dépend forme | idem | dépend forme | disponibilité exacte tôle 1–6 : non trouvé |
| **6082-T6** | **2,70** | ≈70 | ≥260 MPa dans sources Hydro/EN correspondantes | ≥310 MPa | selon produit | bonne usinabilité, pliage T6 moins favorable |
| **7075-T6/T651** | ≈2,80 | ≈71 | ≈503 MPa typique | ≈572 MPa | ≈11 % typ. selon produit | très haute résistance ; corrosion/soudage/formage moins favorables |
| **304** | ≈7,9 | ≈200 | ~230 MPa cold rolled selon état | 540–750 MPa | ~45 % | bonne formabilité/soudabilité/corrosion |
| **316** | ≈8,0 | ≈200 | ~240 MPa cold rolled selon état | 530–680 MPa | ~40 % | meilleure corrosion que 304 dans milieux chlorés |
| **Ti Grade 2** | **4,51** | **105–120** | typ. **345 MPa** | **485 MPa** | **28 %** | excellente corrosion ; formable/soudable/usinable |
| **Ti-6Al-4V Grade 5** | **4,42** | **105–120** | typ. **980 MPa** | **1035 MPa** | **12 %** | haute résistance ; nettement moins formable |
| **CuZn37 laiton** | **8,47** | **110** | très dépendant du temper | très dépendant du temper | très dépendant du temper | bonnes propriétés de formage à états doux ; ne pas donner une résistance unique |

Sources producteur : Atlas 5052 :chatgpt-content-reference{index="58"} ; Novelis/BIKAR 5754 :chatgpt-content-reference{index="59"} ; Hydro 5083/6082 :chatgpt-content-reference{index="60"} ; Hydro/AA-derived et données 6061 :chatgpt-content-reference{index="61"} ; TIMET Grade 2/5 :chatgpt-content-reference{index="62"} ; Outokumpu inox :chatgpt-content-reference{index="63"}.

UACJ au Japon fournit également des valeurs représentatives de 6061-T6 — **Rm 320 MPa, Rp0,2 270 MPa, A 12 %** dans le produit comparatif publié — utiles pour constater la cohérence de l'ordre de grandeur mais pas pour remplacer la certification du lot réel. :chatgpt-content-reference{index="64"}

---

# 6.1 Aptitude relative

| Matériau | Pliage | Usinage | Soudage | Corrosion | Laser |
|---|---|---|---|---|---|
| 5052-H32 | **très bon** | moyen | très bon | très bon | bon |
| 5754-H111 | **très bon** | moyen | très bon | très bon | bon |
| 5754-H22 | bon, mais état exact à qualifier | moyen | bon | très bon | bon |
| 5083-H111/H116 | bon | moyen | très bon | **excellent marin** | bon |
| 6061-T6 | moyen / rayon plus grand | **bon** | bon mais perte locale de T6 | bon | bon, HAZ à considérer |
| 6082-T6 | moyen à difficile pour pli serré | **très bon** | bon mais baisse résistance HAZ | bon | bon, HAZ |
| 7075-T6/T651 | **défavorable au pli serré** | **très bon** | mauvais conventionnel | moyen | découpable, état local à surveiller |
| 304 | bon | moyen | très bon | très bon | excellent |
| 316 | bon | moyen | très bon | excellent | excellent |
| Ti Grade 2 | bon avec grands rayons | moyen | bon avec process adapté | **excellent** | découpe possible |
| Ti Grade 5 | difficile à froid | moyen | spécialisé | excellent | découpe possible |
| laiton | dépend fortement temper | bon | spécialisé | bon | fibre moderne adaptée |

Ces appréciations sont **qualitatives**, pas des notes de conception.

---

# 6.2 Disponibilité tôle 1–6 mm

Une disponibilité « mondiale typique » ne peut pas être prouvée par un seul catalogue.

À titre **[M] propre à un service**, Protolabs propose par exemple :

- 5052-H32 et 6061-T6 : **0,635–6,35 mm** ;
- inox 304/316 : **0,635–6,35 mm** ;
- laiton C260 : **0,635–3,175 mm**. :chatgpt-content-reference{index="65"}

TIMET confirme la production de feuilles Grade 2 et Grade 5, mais pas sur sa page générale une grille publique exhaustive 1/2/3/4/5/6 mm. :chatgpt-content-reference{index="66"}

Hydro confirme tôle/plaque 5083-H116. :chatgpt-content-reference{index="67"}

**Disponibilité garantie de chaque épaisseur entière 1–6 mm dans chaque nuance/état demandé : non trouvé.**

---

# 6.3 MatWeb, Total Materia, MakeItFrom, AZoM

Ces bases ont été utilisées uniquement comme **contre-vérification**, pas comme source à redistribuer massivement.

Le point important pour YXOR open source est leur licence :

| Base | Usage documentaire prudent |
|---|---|
| **MatWeb** | consultation/internal use ; restrictions sur extraction/redistribution massive ; avertit également de vérifier les données avant décision d'ingénierie |
| **Total Materia** | base propriétaire/licenciée ; reproduction massive/extraction interdite |
| **MakeItFrom** | contenu propriétaire ; réutilisation automatisée/datapoints sous licence |
| **AZoM** | contenu protégé ; copie/distribution/œuvres dérivées soumises à autorisation |

Par conséquent, **la future base open source YXOR ne devrait pas être construite par aspiration/copier-coller de ces bases**.

Les données YXOR réutilisables devraient prioritairement venir de :

- producteurs ;
- normes dont la licence autorise ce qui est repris ;
- données ouvertes ;
- résultats expérimentaux originaux YXOR.

---

# 7. Tableau des divergences

| Paramètre | Matériau/t | Source A | Source B | Source C | Nature | Pourquoi divergent-elles ? | Valeur prudente YXOR |
|---|---|---|---|---|---|---|---|
| trou laser min. | métal | SendCutSend ≈0,5t | Protolabs ≥1t | Xometry général ≥2t, min1,575 | E | parc, qualité, stratégie de perçage, définition « minimum » | **≥t**, ou **2t** pour compatibilité prestataire très large |
| web min. | métal | SCS ≈0,5t | SCS conseille davantage pour robustesse | Xometry feature 2t | E | manufacturabilité vs robustesse | **≥1,5t** structurel |
| trou→bord | >0,914 mm | Protolabs 3,175 mm | Xometry min(2t,3,175) | SCS dépend matériau | E | conventions géométriques différentes | **max(1,5t ; 3,2 mm)** avant validation |
| kerf laser | métal | Xometry 0,203–0,305 | Xometry générique 0,508 | inox304 4mm labo 0,138–0,185 | M/E | source laser, puissance, gaz, matériau, focus | **0,5 mm enveloppe**, pas compensation CAO |
| tolérance laser | 1–6 mm | Protolabs ±0,127 | autres services ≈±0,127 | capacités plus larges selon pièces | M | taille, parc, inspection | **±0,4…0,5 mm** si prestataire inconnu |
| R pli 5052-H32 | ~1,6–6mm | Atlas 1–1,5t | SCS rayon outillage variable | AA dépend grain/t | E | outillage + orientation + critère fissuration | **1,5t** |
| trou→ligne pli | général | Protolabs 4t | SCS dépend demi-V | — | E | V-die différent | **≥4t**, puis vérifier V |
| K factor | 5052 | SCS ≈0,37–0,48 | valeurs génériques ≈0,4 | — | M/E | K dépend process/outillage | **ne pas figer ; 0,40 uniquement prototype CAO** |
| paroi CNC | Al | ~0,5 mm possible | ~0,8 mm recommandé | H/t≤10 typique | E | hauteur, serrage, vibration | **≥0,8 mm**, ≥1 mm si haute |
| tolérance fraisage | Al | ±0,127 standard | ±0,051 précision | ±0,005 mm alésage spécialisé | M | opérations différentes | **±0,13 général** |
| H7 | Ø3–30 | +10 à +21 µm | CNC général ±127 µm | reaming spécialisé ~µm | N/M | H7 est une classe fonctionnelle, pas tolérance machine générale | **opération dédiée + contrôle** |
| Ti Gr2 R/t | feuille | TIMET typ.2,5t | ASTM rapporté TIMET 4–5t | — | M/N-derived | « typical » vs exigence normative | **5t** |
| Ti Gr5 R/t | feuille | TIMET typ.5t sur2mm | ASTM rapporté 9–10t | — | M/N-derived | idem | **10t** |

Sources : :chatgpt-content-reference{index="68"}

---

# 8. Registre des sources retenues

**A = primaire/forte ; B = industriel DFM ; C = secondaire.**

| ID | Organisation | Pays | Type | Primaire ? | Gratuit / payant | Date doc | Fiab. | Sujet |
|---|---|---|---|---|---|---|---|---|
| S01 | ISO | international | norme | oui | payant | 1989/2026 status | A | ISO2768-1 :chatgpt-content-reference{index="69"} |
| S02 | ISO | international | norme | oui | à paraître | 2026 | A | ISO2768 Ed2 :chatgpt-content-reference{index="70"} |
| S03 | ISO | international | norme | oui | payant | 2021 | A | ISO22081 :chatgpt-content-reference{index="71"} |
| S04 | ISO | international | norme | oui | payant | 2017 | A | ISO9013 :chatgpt-content-reference{index="72"} |
| S05 | ISO | international | norme | oui | payant | 2017 | A | ISO1101 :chatgpt-content-reference{index="73"} |
| S06 | ISO | international | norme | oui | payant | 2010 | A | ISO286-1/-2 :chatgpt-content-reference{index="74"} |
| S07 | ASME | USA | norme | oui | payant | 2018/R2024 | A | Y14.5 :chatgpt-content-reference{index="75"} |
| S08 | JSA | Japon | norme | oui | payant | 1991/current | A | JIS B0405 :chatgpt-content-reference{index="76"} |
| S09 | JSA | Japon | norme | oui | payant | 2016/current | A | JIS B0401-2 :chatgpt-content-reference{index="77"} |
| S10 | SAMR | Chine | norme | oui | fiche gratuite | 2000/current | A | GB/T1804 :chatgpt-content-reference{index="78"} |
| S11 | Aluminum Association | USA | association/norme | oui | mixte | 2024 | A | H35.2 / données Al :chatgpt-content-reference{index="79"} |
| S12 | AMADA | Japon | fabricant machine | oui | gratuit | actuel | A | laser fibre :chatgpt-content-reference{index="80"} |
| S13 | Prima Power | Italie/Finlande | fabricant machine | oui | gratuit | actuel | A | précision axes laser :chatgpt-content-reference{index="81"} |
| S14 | TRUMPF | Allemagne | fabricant machine | oui | gratuit | actuel | A | fibre/métaux réfléchissants :chatgpt-content-reference{index="82"} |
| S15 | Protolabs | USA/Europe | service industriel | non machine OEM | gratuit | actuel | B | laser/sheet DFM :chatgpt-content-reference{index="83"} |
| S16 | Xometry | USA/global | service industriel | non | gratuit | actuel | B | laser DFM/kerf :chatgpt-content-reference{index="84"} |
| S17 | SendCutSend | USA | service industriel | non | gratuit | 2025–26 | B | minima mesurés/DFM :chatgpt-content-reference{index="85"} |
| S18 | Scientific Reports | international | article scientifique | oui essai | open access | 2025 | A | HAZ/kerf 304 :chatgpt-content-reference{index="86"} |
| S19 | Flow | USA | fabricant waterjet | oui | gratuit | actuel | A | waterjet :chatgpt-content-reference{index="87"} |
| S20 | Hypertherm | USA | fabricant plasma | oui | gratuit | actuel | A | plasma :chatgpt-content-reference{index="88"} |
| S21 | Atlas Steels | Australie | producteur/distributeur matière | oui/technique | gratuit | 2013 | A/B | 5052 bend :chatgpt-content-reference{index="89"} |
| S22 | BIKAR | Allemagne | producteur/distributeur | oui/EN-derived | gratuit | 2025 | A/B | 5754 :chatgpt-content-reference{index="90"} |
| S23 | Hydro | Norvège/global | producteur Al | oui | gratuit | actuel | A | 5083/6082/6061 :chatgpt-content-reference{index="91"} |
| S24 | Novelis | USA/global | producteur Al | oui | gratuit | actuel | A | 5754 :chatgpt-content-reference{index="92"} |
| S25 | UACJ | Japon | producteur Al | oui | gratuit | actuel | A | Al/6061 comparative :chatgpt-content-reference{index="93"} |
| S26 | TIMET | USA/global | producteur titane | oui | gratuit | manuel/datasheets | A | Grade2/5 :chatgpt-content-reference{index="94"} |
| S27 | Outokumpu | Finlande/global | producteur inox | oui | gratuit | actuel | A | 304/316 :chatgpt-content-reference{index="95"} |
| S28 | Protolabs CNC | USA/Europe | industriel | non OEM | gratuit | actuel | B | CNC tolérances :chatgpt-content-reference{index="96"} |
| S29 | Guhring | Allemagne | fabricant outil | oui | gratuit | actuel | A | taraudage :chatgpt-content-reference{index="97"} |
| S30 | MISUMI | Japon/global | données techniques | secondaire autorisé | gratuit | actuel/archives | B | H7 :chatgpt-content-reference{index="98"} |

### Couverture géographique

La recherche a inclus des sources américaines, canadiennes/internationales, allemandes, italiennes/finlandaises, norvégiennes, britanniques/européennes, japonaises, chinoises et australiennes, avec interrogation également des producteurs asiatiques. Je n'ai pas ajouté artificiellement de source coréenne ou indienne lorsqu'elle ne fournissait pas une donnée primaire meilleure ou différente de celles ci-dessus.

Pour les fabricants explicitement demandés **Bystronic, Mazak, LVD, Bodor, HSG et Han's Laser**, la recherche a trouvé de la documentation de gamme, mais **pas de tableau public suffisamment comparable donnant kerf + petit trou + contour tolerance pour les alliages × 1–6 mm demandés**. Ces cellules restent donc **non trouvé**, plutôt que de transformer des arguments commerciaux en données DFM.

---

# 9. DONNÉES À TRANSMETTRE AU LOT B

## 9.1 Règles laser prudentes

| t | trou/slot mini de conception | web structurel prudent | feature ultra-compatible |
|---:|---:|---:|---:|
| 1 | ≥1 mm | ≥1,5 mm | ≥2 mm |
| 2 | ≥2 mm | ≥3 mm | ≥4 mm |
| 3 | ≥3 mm | ≥4,5 mm | ≥6 mm |
| 4 | ≥4 mm | ≥6 mm | ≥8 mm |
| 5 | ≥5 mm | ≥7,5 mm | ≥10 mm |
| 6 | ≥6 mm | ≥9 mm | ≥12 mm |

Avec :

- kerf de pré-DFM : **jusqu'à ~0,5 mm**, mais ne pas appliquer de compensation dans la CAO sans information opérateur ;
- tolérance de pièce à réserver avant qualification fournisseur : **±0,4–0,5 mm** ;
- ±0,1–0,15 mm possible chez certains services documentés mais **pas présumé** ;
- trous de précision, axes et roulements → **finition CNC** ;
- micro-joints → paramètres CAM opérateur ;
- HAZ exact T6/T651 → **non trouvé**, à qualifier.

---

## 9.2 Règles de pliage prudentes

| Matériau | Rᵢ prudent à transmettre |
|---|---:|
| 5052-H32 | **≥1,5t** |
| 5754-H111 | **≥1,5t** |
| 5754-H22 | **non trouvé — qualification requise** |
| 5083-H111 | **non trouvé — qualification requise** |
| 5083-H116 | **non trouvé — qualification requise** |
| 6061-T6 | **≈2t à 3,5t selon t ; utiliser 3,5t si règle unique** |
| 6082-T6 | primaire exact **non trouvé** ; ~6t seulement borne secondaire |
| 7075-T6/T651 | **ne pas supposer pliable en conception générique** |
| inox 304 | **1,5t [E] provisoire** |
| inox 316 | **1,5t [E] provisoire** |
| Ti Grade 2 | **5t prudent** |
| Ti Grade 5 | **10t prudent** |
| laiton 1–6 mm | **non trouvé** |

Autres règles :

- feature → ligne de pli : **≥4t** avant connaissance du V ;
- bend relief : largeur **≥0,5t**, profondeur **≥R+t+0,5 mm** ;
- **K factor non figé** ;
- orientation de laminage à conserver pour alliages difficiles ;
- flat pattern final basé sur table réelle de la presse.

---

## 9.3 Règles fraisage prudentes

| Paramètre | Valeur de départ |
|---|---:|
| tolérance générale | **±0,13 mm** |
| précision ciblée | **±0,05 mm** seulement si spécifiée |
| paroi mince | **≥0,8 mm** |
| paroi haute | préférer **≥1 mm**, H/t≤~10 |
| poche profonde | **≤4D outil** de préférence |
| trou profond | **≤4D** de préférence |
| fond mince | **≥0,8 mm** |
| coin intérieur | R > rayon outil |
| H7 | opération dédiée + contrôle |
| surface standard usinée | ordre de grandeur Ra quelques µm ; valeur exacte à spécifier au fabricant |

---

## 9.4 Propriétés matières à conserver

Pour le premier modèle mécanique YXOR, les propriétés les mieux étayées sont notamment :

- 5052-H32 : ρ≈2,68 ; E≈70 GPa ; Rp0,2≥160 MPa ; Rm≈215–265 MPa ;
- 5754-H111 : ρ≈2,67 ; E≈70,5 GPa ; Rp0,2≥80 MPa ; Rm190–240 MPa ;
- 6061-T6 : ρ2,70 ; E68,9 GPa ; typ. Rp276 / Rm310 MPa ;
- 6082-T6 : ρ≈2,70 ; E≈70 ; ordre de grandeur Rp≥260/Rm≥310 MPa selon produit ;
- Ti Gr2 : ρ4,51 ; E105–120 ; typ. Rp345/Rm485/A28 ;
- Ti Gr5 : ρ4,42 ; E105–120 ; typ. Rp980/Rm1035/A12 ;
- inox 304/316 : E≈200 GPa mais masse ≈3× celle de l'aluminium.

**Pour calcul final, remplacer les typiques par les minima garantis de la spécification d'achat retenue.**

---

## 9.5 Tolérances normatives à conserver

1. **ISO 2768-1:1989 est encore courante au 02/10/2026.**
2. Sa remplaçante **ISO 2768 Ed.2 est en cours de publication**. :chatgpt-content-reference{index="99"}
3. **ISO 2768-2 est retirée** ; utiliser le cadre moderne **ISO 22081:2021** pour les spécifications géométriques générales. :chatgpt-content-reference{index="100"}
4. **ISO 1101:2017** pour la syntaxe GD&T.
5. **ISO 286-1/-2** pour les ajustements H7, etc.
6. **ISO 9013:2017+A1:2024** lorsqu'une classe de qualité de coupe thermique doit être contractualisée.

---

## 9.6 Inconnues critiques restantes

Ce sont précisément les informations que le LOT B devra confronter aux déclarations de l'opérateur :

| Domaine | Question à poser |
|---|---|
| Laser | marque + modèle exact ? |
| Laser | fibre ou CO₂ ? longueur d'onde ? |
| Laser | puissance nominale ? |
| Laser | N₂/O₂/air selon chaque matériau ? |
| Laser | diamètre de spot/faisceau au foyer ? |
| Laser | **kerf réellement mesuré**, par matériau et t ? |
| Laser | compensation kerf automatique CAM ? |
| Laser | trou minimum testé par t ? |
| Laser | web/bridge minimum testé ? |
| Laser | tolérance **pièce finie**, distincte de précision axes ? |
| Laser | perpendicularité/taper/circularité mesurés ? |
| Laser | classe ISO 9013 éventuellement garantie ? |
| Laser | HAZ/altération T6/T651 qualifiée ? |
| Laser | stratégie de micro-joints/nano-joints ? |
| Pliage | presse exacte ? |
| Pliage | **air bending, bottoming ou coining ?** |
| Pliage | V-dies disponibles par épaisseur ? |
| Pliage | rayons de poinçons disponibles ? |
| Pliage | rayon intérieur réellement obtenu par combinaison ? |
| Pliage | K-factor/BA/BD issus de coupons réels ? |
| Pliage | tolérance d'angle ? |
| Pliage | compensation springback ? |
| Pliage | règle sur sens de laminage ? |
| Pliage | accepte-t-il réellement 6061/6082/7075 T6 ? |
| CNC | modèle 3/5 axes ? |
| CNC | tolérance générale garantie ? |
| CNC | tolérance de position vraie ? |
| CNC | planéité/perpendicularité ? |
| CNC | plus petit outil standard ? |
| CNC | profondeur de poche/trou admissible ? |
| CNC | procédure H7 : alésoir, boring, interpolation ? |
| CNC | moyen de contrôle : micromètre, bore gauge, CMM ? |
| Taraudage | taraud coupant/formant ? |
| Taraudage | profondeur filet utile et clearance borgne ? |
| Matière | certificat EN 10204 / CoC / MTR fourni ? |
| Matière | nuance **et état métallurgique exacts** garantis ? |
| Matière | tolérance réelle d'épaisseur/planéité ? |

---

# Conclusion du LOT A

Trois enseignements sont particulièrement importants pour la suite de YXOR.

**1. Une machine laser moderne peut avoir une répétabilité de l'ordre de 0,01–0,03 mm sans que la pièce découpée soit garantie à ±0,01–0,03 mm.** AMADA et Prima Power l'illustrent directement. :chatgpt-content-reference{index="101"}

**2. Pour les petites géométries laser, les références sérieuses vont approximativement de 0,5t à 2t selon le niveau de garantie demandé.** Pour une architecture open source devant rester fabricable ailleurs que chez un prestataire unique, **trou/slot ≥t et web structurel ≥1,5t** constituent une bien meilleure base que l'exploitation des limites extrêmes d'une machine.

**3. Le pliage est le domaine dans lequel l'état métallurgique change le plus radicalement la conception.** 5052-H32/5754-H111 peuvent accepter des rayons relativement serrés, tandis que 6061-T6 demande beaucoup plus de rayon et que 7075-T6/T651 ou Ti-6Al-4V exigent une approche nettement plus conservatrice. Le cas TIMET est particulièrement révélateur : une valeur typique de **5t** pour le Grade 5 coexiste avec une valeur ASTM rapportée de **9–10t** suivant épaisseur ; pour YXOR, c'est donc la seconde qui doit piloter une conception réellement portable tant qu'aucun procédé n'est qualifié. :chatgpt-content-reference{index="102"}

Cette base permet maintenant de faire le **LOT B** proprement : confronter, point par point et sans préjugé, les capacités déclarées de l'opérateur aux enveloppes DFM documentées ci-dessus.





# RECHERCHE YXOR — LOT B  
## Quincaillerie, assemblages, sources industrielles et validation de l’opérateur

**Date de l’étude : 2 octobre 2026**  
**Projet : YXOR — humanoïde bipède open source, ≈0,60 m, ≈8 kg, 12 articulations.**  
**Cas prioritaire étudié ici : aluminium 3 mm découpé laser, éventuellement plié.**

Ce LOT B complète le LOT A. Je conserve les conventions **[M] mesure/capacité fabricant**, **[E] règle DFM**, **[N] norme**, **[O] déclaration opérateur**. Toutes les sources web ont été consultées le **02/10/2026** sauf indication contraire. Dans les tableaux, les citations sont les liens vers les URL sources.

---

# 1. Quincaillerie — trous de passage et ISO 273

## 1.1 ISO 273

**ISO 273:1979 — Fasteners — Clearance holes for bolts and screws** est toujours l’édition courante en octobre 2026. Elle a été réexaminée et confirmée en **2024**. Prix ISO observé : **CHF 44**. La norme définit trois séries : fine, moyenne et large/coarse. :chatgpt-content-reference{index="0"}

### Diamètres nominaux de passage

| Vis | Fine [N] | Moyenne [N] | Large [N] |
|---|---:|---:|---:|
| M2 | **2,2 mm** | **2,4 mm** | **2,6 mm** |
| M2.5 | **2,7 mm** | **2,9 mm** | **3,1 mm** |
| M3 | **3,2 mm** | **3,4 mm** | **3,6 mm** |
| M4 | **4,3 mm** | **4,5 mm** | **4,8 mm** |
| M5 | **5,3 mm** | **5,5 mm** | **5,8 mm** |
| M6 | **6,4 mm** | **6,6 mm** | **7,0 mm** |

Ces mêmes dimensions apparaissent également dans les tables métriques publiées à partir d’ASME B18.2.8. :chatgpt-content-reference{index="1"}

Pour YXOR, **M3 = Ø3,4 mm** constitue donc une valeur normative défendable si l’on choisit la **série moyenne**.

---

## 1.2 ASME/ANSI

**ASME B18.2.8-1999 (S2021)** est toujours en vigueur sous maintenance stabilisée. Prix officiel observé : **USD 39**. Elle couvre les fixations métriques M1.6 à M100 et utilise les catégories **close / normal / loose**. :chatgpt-content-reference{index="2"}

Pour M2–M6, les valeurs nominales close/normal/loose accessibles publiquement coïncident avec les séries fine/moyenne/large ci-dessus. :chatgpt-content-reference{index="3"}

---

## 1.3 Japon — JIS B 1001

**JIS B 1001:1985**, « Diameter of clearance holes and counterbores for bolts and screws », est **active**, confirmée le **21 octobre 2024**.

Prix officiel :

- japonais : **¥1 430** ;
- traduction anglaise : **¥4 400**.

La JSA indique une correspondance avec ISO 273:1979 classée **MOD**, et non « identical ». Il serait donc incorrect d’affirmer que l’ensemble du contenu est strictement identique sans consulter le texte payant. :chatgpt-content-reference{index="4"}

**Différences détaillées M2–M6 accessibles légalement gratuitement : non trouvé.**

---

## 1.4 Chine — GB/T 5277

**GB/T 5277-1985**, « Fasteners — Clearance holes for bolts and screws », est officiellement **en vigueur**, dernier réexamen le **10 janvier 2022**, conclusion : maintien en vigueur.

La plateforme nationale chinoise indique explicitement qu’elle adopte **ISO 273:1979 de façon équivalente**. :chatgpt-content-reference{index="5"}

Les valeurs ISO peuvent donc être utilisées comme référence d’équivalence pour ce périmètre.

---

## 1.5 DIN historique

Les références DIN historiques autour des trous de passage ont été progressivement harmonisées avec ISO/EN.

Une correspondance historique précisément vérifiée et toujours normative en 2026 pour chaque dimension M2–M6 : **non trouvé dans une source DIN officielle gratuite**.

---

# 2. Perçages avant taraudage M2–M6

Il faut absolument distinguer :

1. le calcul simplifié **d − pas** ;
2. le diamètre recommandé par un fabricant d’outil ;
3. le **taraud coupant** ;
4. le **taraud à refouler/former**.

## 2.1 Taraudage coupant

Guhring publie les plages suivantes :

| Filetage | Pas | d−P | Plage Guhring [M] |
|---|---:|---:|---:|
| M2 | 0,40 | **1,60 mm** | **1,567–1,679 mm** |
| M2.5 | 0,45 | **2,05 mm** | **2,013–2,138 mm** |
| M3 | 0,50 | **2,50 mm** | **2,459–2,599 mm** |
| M4 | 0,70 | **3,30 mm** | **3,242–3,422 mm** |
| M5 | 0,80 | **4,20 mm** | **4,134–4,334 mm** |
| M6 | 1,00 | **5,00 mm** | **4,917–5,153 mm** |

Guhring publie les mêmes plages sur certains tarauds carbure destinés spécifiquement aux métaux non ferreux, donc adaptés notamment à l’aluminium. :chatgpt-content-reference{index="6"}

Le très courant **Ø2,5 mm avant M3×0,5** n’est donc pas une approximation arbitraire : il se trouve au cœur d’une plage fabricant.

---

## 2.2 Pourcentage de filet

YAMAWA donne une relation permettant de relier diamètre avant taraudage et pourcentage de filet :

\[
\%\ filet =
\frac{(D-d_f)\times76,980}{P}
\]

avec :

- \(D\) = diamètre nominal ;
- \(d_f\) = diamètre du trou ;
- \(P\) = pas.

Cela démontre pourquoi « le bon foret » n’est pas nécessairement une valeur unique : on peut volontairement réduire le pourcentage de filet pour diminuer le couple de taraudage tout en maintenant une résistance suffisante. :chatgpt-content-reference{index="7"}

---

## 2.3 Taraudage par déformation

Un taraud à refouler exige un trou **plus grand** puisqu’aucun copeau n’est retiré : la matière est déplacée vers les crêtes du filet.

Exemple Guhring pour métaux non ferreux, selon série :

| Filetage | Trou de formage publié [M] |
|---|---:|
| M2 | ≈ **1,84–1,88 mm** |
| M2.5 | ≈ **2,28–2,32 mm** |
| M3 | ≈ **2,78–2,85 mm** |
| M4 | ≈ **3,68–3,76 mm** |
| M5 | ≈ **4,62–4,71 mm** |
| M6 | ≈ **5,52–5,62 mm** |

**Conséquence YXOR :**

> « M3 → trou 2,5 mm » n’est vrai que si l’on parle d’un **taraud coupant** correspondant.

Le procédé de taraudage fait donc partie des paramètres à demander à l’opérateur.

---

## 2.4 Trous borgnes

La profondeur totale doit inclure :

- filet utile ;
- chanfrein/entrée du taraud ;
- zone incomplètement filetée ;
- pointe du foret ;
- volume de copeaux pour un taraud coupant.

NASA-STD-5020B rappelle également qu’un assemblage avec écrou ou dispositif autobloquant doit laisser suffisamment de filets complètement formés pour engager la fonction de verrouillage. :chatgpt-content-reference{index="8"}

Une marge universelle en « x pas » pour tous les tarauds borgnes M2–M6 :

**non trouvé — dépend du taraud exact et de sa géométrie d’entrée.**

---

# 3. Engagement de filet dans l’aluminium

C’est l’un des résultats les plus importants de ce LOT B.

## 3.1 Il n’existe pas de « 1D » ou « 1,5D » universel

Bossard précise que la longueur minimale nécessaire dépend de la **résistance du matériau taraudé** et qu’elle doit être calculée lorsque l’on veut développer la pleine résistance de la vis. :chatgpt-content-reference{index="9"}

Ses tableaux donnent notamment :

| Aluminium de référence Bossard | Rm matériau | Classe de vis | Engagement approximatif [E] |
|---|---:|---|---:|
| AlMg3 F18 | >180 MPa | 8.8 | **2,0d** |
| AlMgSi1 F32 | >330 MPa | 8.8 | **1,4d** |
| AlMgSi1 F32 | >330 MPa | 10.9 | **1,6d** coarse |
| AlMgSi1 F32 | >330 MPa | 10.9 fine | **2,0d** |
| AlMg4.5Mn F28 | >330 MPa | 8.8 | **1,4d** |
| AlMg1 F40 | >550 MPa | 8.8 | **1,1d** |
| AlZnMgCu0.5 F50 | >550 MPa | 8.8 | **1,0d** |

Les valeurs entre crochets dans la documentation Bossard correspondent à des calculs VDI 2230 et peuvent être plus élevées ; Bossard précise qu’un calcul selon VDI 2230 est nécessaire pour une valeur exacte. :chatgpt-content-reference{index="10"}

### Lecture par familles YXOR

- les **5xxx relativement doux** peuvent exiger environ **2d** pour développer la résistance d’une vis 8.8 ;
- certains **6xxx plus résistants** sont autour de **1,4d** dans le cas documenté ;
- certains **7xxx très résistants** peuvent descendre vers **1d**.

Il serait cependant faux d’identifier automatiquement :

> « 5052 = exactement AlMg3 F18 » ou  
> « 6061-T6 = exactement AlMgSi1 F32 ».

Les états et résistances doivent être comparés au matériau réellement acheté.

---

## 3.2 Cas très concret : M3 directement dans une tôle de 3 mm

Avec une tôle de **3 mm** :

\[
L_e/d = 3/3 = 1,0D
\]

Cela signifie qu’un taraudage traversant M3 directement dans la tôle fournit géométriquement au maximum environ **1D d’engagement nominal**, et un peu moins d’engagement pleinement utile après chanfreins et filets incomplets.

C’est :

- inférieur au **1,4D** documenté par Bossard pour AlMgSi1 F32 + vis 8.8 ;
- très inférieur au **2D** donné pour AlMg3 F18 + vis 8.8. :chatgpt-content-reference{index="11"}

Ce n’est **pas** la preuve que le filetage échouera dans YXOR : charge, classe de vis, couple, fréquence de démontage et alliage sont encore inconnus.

Mais cela prouve qu’un **M3 taraudé directement dans 3 mm d’aluminium ne doit pas être considéré comme développant automatiquement la pleine résistance d’une vis 8.8**.

---

## 3.3 Gain au-delà d’une certaine longueur

Bossard signale qu’au-dessus d’environ **1,5d**, des filetages aux extrêmes de tolérance peuvent même commencer à présenter un risque de coincement.

Ce point ne signifie **pas** que la résistance plafonne universellement à 1,5d. :chatgpt-content-reference{index="12"}

Une courbe primaire généralisable donnant exactement « au-delà de Xd le gain mécanique devient négligeable » pour 5xxx/6xxx/7xxx :

**non trouvé.**

---

# 4. Couples de serrage M2–M6

## 4.1 Pourquoi un couple sans frottement ne vaut presque rien

Bossard fonde ses tableaux VDI 2230 sur :

- **90 % de Rp0,2** ;
- coefficient de frottement explicite ;
- trous de passage ISO 273 série moyenne ;
- valeurs maximales sans facteur de sécurité. :chatgpt-content-reference{index="13"}

### Classes 8.8 / 10.9 / 12.9

Valeurs Bossard, filet métrique gros.

| Vis | 8.8 µ=.14 | 10.9 µ=.14 | 12.9 µ=.14 | 8.8 µ=.10 | 10.9 µ=.10 | 12.9 µ=.10 |
|---|---:|---:|---:|---:|---:|---:|
| M2 | 0,392 | 0,550 | 0,660 | 0,317 | 0,445 | 0,535 |
| M2.5 | 0,81 | 1,13 | 1,36 | 0,65 | 0,91 | 1,09 |
| M3 | **1,41** | **1,98** | **2,37** | **1,12** | **1,58** | **1,90** |
| M4 | 3,3 | 4,8 | 5,6 | 2,6 | 3,9 | 4,5 |
| M5 | 6,5 | 9,5 | 11,2 | 5,2 | 7,6 | 8,9 |
| M6 | 11,3 | 16,5 | 19,3 | 9,0 | 13,2 | 15,4 |

**Unité : N·m [M/E Bossard/VDI].**

Pour la seule vis M6 8.8 :

- μ=0,10 → **9,0 N·m** ;
- μ=0,14 → **11,3 N·m**.

Soit environ **+25,6 %** de couple pour un simple changement de coefficient de frottement.

Ce résultat explique pourquoi « serrer une M6 à 10 N·m » sans état de surface, lubrifiant, revêtement et matériau sous tête n’est pas une spécification complète.

---

## 4.2 Inox A2/A4

Bossard publie également des tableaux classes 70 et 80 à plusieurs coefficients de frottement.

### Classe 70

| Vis | μ=.10 | μ=.20 |
|---|---:|---:|
| M2 | 0,23 | 0,35 |
| M2.5 | 0,46 | 0,72 |
| M3 | **0,80** | **1,26** |
| M4 | 1,85 | 2,90 |
| M5 | 3,60 | 5,70 |
| M6 | 6,30 | 10,0 |

### Classe 80

| Vis | μ=.10 | μ=.20 |
|---|---:|---:|
| M2 | 0,30 | 0,46 |
| M2.5 | 0,62 | 0,97 |
| M3 | **1,10** | **1,70** |
| M4 | 2,40 | 3,80 |
| M5 | 4,80 | 7,60 |
| M6 | 8,40 | 13,2 |

Dans ce tableau de dimensionnement, A2 et A4 d’une même classe mécanique utilisent les mêmes valeurs ; cela **ne signifie pas** que les matériaux sont autrement interchangeables.

### « Sec » versus « lubrifié »

Je ne transforme volontairement pas μ=.14 en « sec » et μ=.10 en « lubrifié ».

Ces termes ne définissent pas suffisamment le frottement :

- inox/inox sec peut gripper ;
- zinc, Zn-flake, anodisation, huile, MoS₂, cire ou pâte anti-seize changent fortement μ ;
- le contact sous tête compte autant que le filet.

**Table complète M2–M6 explicitement certifiée “dry” / “lubricated” pour toutes les classes demandées dans une même source primaire : non trouvé.**

---

# 5. Freinage des vis

| Solution | Vibration | Température / chimie | Démontage | Donnée quantitative disponible |
|---|---|---|---|---|
| Anaérobie type LOCTITE 243 | bonne conservation du preload avec cure correcte | plage 243 ≈ **−55 à +180 °C [M]** | démontable avec outillage | breakaway publié ≈**26 N·m sur M10 acier** ; ne pas extrapoler M3 |
| Nylstop | ajoute couple prévalent | nylon sensible à température/chimie | oui, mais réutilisation limitée | dépend norme/série |
| écrou tout métal | couple prévalent sans polymère | meilleure tenue thermique | oui | dépend série |
| Nord-Lock | verrouillage géométrique à cames | dépend matériau/revêtement choisi | oui | essais Junker publiés |
| rondelle Grower | faible face à vibration transverse | simple | oui | NASA : locking minimal voire nul |
| fil à freiner | verrouillage positif | très bonne tenue selon fil | démontage manuel | dimensionnement/application spécifique |

NASA-STD-5020B, revalidée le **5 janvier 2026**, indique explicitement que les rondelles fendues offrent **très peu, voire aucune capacité de verrouillage**, et qu’elles ne doivent pas être utilisées comme verrouillage secondaire. :chatgpt-content-reference{index="14"}

Le Fastener Design Manual NASA va encore plus loin : une rondelle hélicoïdale aplatie lors du serrage devient pratiquement équivalente à une rondelle plate pour le verrouillage. :chatgpt-content-reference{index="15"}

Nord-Lock publie des essais Junker suivant DIN 65151/ISO 16130 comparant notamment :

- écrou ordinaire ;
- rondelle fendue ;
- écrou à insert nylon ;
- double écrou ;
- système à cames.

Il s’agit de **[M] propres aux configurations d’essai**, pas d’une garantie universelle. :chatgpt-content-reference{index="16"}

### Aluminium + inox

LOCTITE 243 est prévu pour fonctionner notamment sur métaux passifs tels que l’inox et sur aluminium, sous réserve des procédures fabricant.

Pour une rondelle ou vis inox directement sur aluminium, la **compatibilité galvanique** dépend de l’électrolyte, des surfaces, revêtements et environnement. Une règle numérique universelle : **non trouvé**.

---

# 6. Rivet nuts / RIVKLE / PEM

Il ne faut surtout pas créer une règle telle que :

> « un écrou à sertir M3 nécessite toujours un trou de X mm ».

La géométrie est **spécifique à la famille du fabricant**.

---

## 6.1 PEM auto-clinch aluminium — Type CLA

Exemples officiels :

| Réf. | Filet | t mini tôle | Trou | Tolérance trou | C/L trou→bord mini | Limite dureté tôle |
|---|---|---:|---:|---:|---:|---|
| CLA-M3-1 | M3×0,5 | **1,00 mm** | **4,75 mm** | **+0,08/0** | **5,6 mm** | HRB50 / HB89 |
| CLA-M3-2 | M3×0,5 | **1,40 mm** | **4,75 mm** | **+0,08/0** | **5,6 mm** | HRB50 / HB89 |
| CLA-M4-1 | M4 | ≈1,0 mm | **5,94 mm** | +0,08 | **7,1 mm** | série CLA |
| CLA-M5-1 | M5 | ≈1,0 mm | **7,52 mm** | +0,08 | **7,9 mm** | série CLA |
| CLA-M6-1 | M6 | ≈1,4 mm | **8,75 mm** | +0,08 | **8,6 mm** | série CLA |

PEM recommande précisément les CLA aluminium pour tôles aluminium suffisamment tendres. :chatgpt-content-reference{index="17"}

### M2

Une référence CLA M2 existe et un diamètre de trou de l'ordre de **4,22 mm** apparaît dans la famille catalogue, mais la combinaison complète tôle/edge-distance n'a pas été suffisamment vérifiée dans une page primaire extraite ici :

**M2 : données complètes = non trouvé.**

---

## 6.2 RIVKLE / Böllhoff

Böllhoff donne pour ses **rivet nuts standard à fût rond** :

| Filet | Trou standard |
|---|---:|
| M3 | **5,0 mm** |
| M4 | **6,0 mm** |
| M5 | **7,0 mm** |
| M6 | **9,0 mm** | :chatgpt-content-reference{index="18"}


On observe immédiatement une divergence réelle :

- PEM CLA-M3 : **4,75 mm** ;
- RIVKLE M3 standard : **5,0 mm**.

Elle vient du **produit**, pas d'une imprécision documentaire.

Sur certaines séries aluminium RIVKLE, Böllhoff publie des plages de grip couvrant notamment :

- M3 : ~1,3–3,5 mm puis 3,5–5 mm ;
- M4 : ~1,7–3,5 puis 3,5–5 mm ;
- M5 : ~1–4 puis 4–6,5 mm ;
- M6 : ~1,7–4,5 puis 4,5–6,5 mm.

Donc une tôle 3 mm se situe dans plusieurs gammes existantes, mais **la référence exacte doit être sélectionnée avant de figer le trou CAO**.

---

## 6.3 Push-out / spin-out

PEM publie des valeurs mesurées sur certaines familles S/CLS dans du 5052-H34, avec par exemple pour des petits filetages M2–M3 des ordres de grandeur :

- push-out : quelques centaines de newtons ;
- torque-out : environ **0,9 à 1,5 N·m** selon shank et configuration.

Ce sont strictement des **[M] famille/installation**, et non des performances universelles d'un « écrou PEM ».

Pour CLA-M3 dans **l'alliage exact de YXOR**, valeur complète push-out/torque-out : **non trouvé**.

### Distance entre deux inserts

Une valeur universelle centre-à-centre PEM/RIVKLE :

**non trouvé**.

Elle dépend au minimum :

- diamètre extérieur de l'insert ;
- écoulement plastique de la tôle ;
- dureté ;
- sens de laminage ;
- procédé d'installation.

---

# 7. Goupilles

## 7.1 Normes

| Norme | Objet | Statut 2026 |
|---|---|---|
| **ISO 2338:1997** | goupilles cylindriques non trempées | current, confirmée 2023 |
| **ISO 8734:1997** | goupilles cylindriques trempées | current, confirmée 2023 |
| **ISO 8752:2009** | goupilles élastiques fendues, heavy duty | current, confirmée 2024 |

ISO 2338 et ISO 8734 étaient affichées autour de **CHF 44** lors de la recherche. Les textes complets restent protégés/payants.

---

## 7.2 Goupilles élastiques

SPIROL publie des couples trou/goupille concrets.

Exemples suivant série :

| Ø nominal | Trou recommandé [M] | Goupille libre | Cisaillement publié |
|---|---:|---:|---:|
| 3 mm | **3,00–3,10** | 3,14–3,25 | ≈4,5 kN selon matériau/série |
| 4 mm | **4,00–4,12** | selon série ≈4,16–4,60 | selon série ≈7–11 kN |
| 5 mm | **5,00–5,12** | ≈5,17–5,60 | selon série ≈17–20 kN |
| 6 mm | **6,00–6,12** | ≈6,18–6,36 | ≈16,6 kN sur exemple inox |

Le point important pour YXOR est que la goupille élastique **n'utilise pas le même concept d'ajustement qu'une goupille cylindrique rectifiée**.

---

## 7.3 Goupilles cylindriques

Pour une goupille rigide, le montage peut être :

- pressé dans un côté et glissant dans l'autre ;
- pressé dans les deux ;
- localisé par ajustement de précision.

Les fournisseurs proposent couramment des goupilles avec classes telles que **m6/h8** selon produit.

Une combinaison unique « goupille Ø4 → trou X » :

**non trouvé — elle dépend de la fonction du montage.**

Pour une articulation démontable YXOR, il faudra définir quelle pièce **localise** et quelle pièce autorise le démontage avant de choisir l'ajustement.

---

# 8. Petits roulements et ajustements

## 8.1 H7 n'est pas « le trou de roulement »

Les tableaux NTN montrent clairement :

### Bague extérieure stationnaire dans logement acier/fonte

- charge fixe : souvent **H7** ;
- charge indéterminée faible/normale : transition type **JS7/K7** ;
- charge tournante : **M7/N7/P7** suivant intensité.

Pour une bague intérieure, les classes possibles vont de g/h jusqu'à k/m/n/p suivant charge et rotation. :chatgpt-content-reference{index="19"}

### Logement aluminium

NTN avertit que les tableaux standards sont basés sur logements acier/fonte et que les alliages légers peuvent nécessiter un serrage accru, notamment en raison de la dilatation thermique. NTN documente également le risque de creep lorsqu'un logement aluminium devient trop lâche. :chatgpt-content-reference{index="20"}

---

## 8.2 Exemples de classes d'ajustement

Sur l'exemple NTN/SNR d'un roulement 6305 :

### logement

H6/H7 → jeu ; J/K → transition ; M/N/P → serrage croissant.

### arbre

g/h → plutôt jeu ; j/k → transition ; m/n/p → serrage croissant. :chatgpt-content-reference{index="21"}

La sélection dépend de :

- quelle bague tourne par rapport à la charge ;
- amplitude de charge ;
- chocs ;
- diamètre ;
- matériau logement ;
- température ;
- possibilité de déplacement axial.

---

## 8.3 Rugosité des portées

Schaeffler publie, pour diamètre de portée ≤80 mm :

| Classe dimensionnelle | Ra recommandé max |
|---|---:|
| IT7 | **1,6 µm** |
| IT6 | **0,8 µm** |
| IT5 | **0,4 µm** |
| IT4 | **0,2 µm** |

Les arbres sont recommandés rectifiés et les alésages usinés avec précision. :chatgpt-content-reference{index="22"}

---

## 8.4 H7 et petits diamètres

Comme établi au LOT A :

| Diamètre nominal | H7 |
|---|---:|
| ≤3 mm | **0 / +10 µm** |
| >3–6 | **0 / +12 µm** |
| >6–10 | **0 / +15 µm** |
| >10–18 | **0 / +18 µm** |
| >18–30 | **0 / +21 µm** |

Il est donc parfaitement possible qu'un logement Ø8 H7 soit **Ø8,000 à 8,015 mm**, mais cela ne signifie absolument pas qu'Ø8 H7 est le bon ajustement pour le roulement YXOR.

### Règle YXOR

**Roulement non sélectionné + charge non caractérisée → ajustement = non trouvé.**

---

# 9. Bibliothèques CAO et visserie paramétrique

| Projet/service | Nature | Visserie | Paramétrique | Licence / redistribution | Pertinence dépôt YXOR |
|---|---|---|---|---|---|
| FreeCAD Fasteners Workbench | WB FreeCAD | ISO/DIN/ANSI/etc. | oui | GPLv2 pour le code | bonne source générative |
| OpenSCAD MCAD | bibliothèque | nuts/bolts/threads | oui | LGPL-2.1 | génératif |
| BOSL2 | OpenSCAD | ISO metric + UTS | **oui** | BSD-2-Clause | très adaptée à génération |
| NopSCADlib | OpenSCAD | screws/inserts/vitamins | mixte paramétrique | GPL-3.0 | adaptée avec respect licence |
| CadQuery / cq_warehouse | Python CAD | fasteners paramétriques | **oui** | Apache-2.0 pour cq_warehouse | adaptée |
| build123d / bd_warehouse | Python CAD | fasteners et composants | **oui** | Apache-2.0 | adaptée |
| McMaster-Carr CAD | catalogue commercial | très vaste | modèle fournisseur | **redistribution fortement restreinte** | ne pas republier sans autorisation |
| TraceParts | catalogue | très vaste | surtout modèles catalogues | droits modèle/fabricant variables | vérifier chaque licence |
| 3D ContentCentral | catalogue | très vaste | modèles fabricants | redistribution générique : **non trouvé** | prudence |
| PARTcommunity / CADENAS | catalogue industriel | très vaste | configurable/catalogue | droits dépendants fournisseur | prudence |

BOSL2 est sous BSD-2-Clause et comprend une bibliothèque paramétrique de vis métriques/UTS. MCAD est LGPL et contient des modules de fasteners. NopSCADlib est GPL-3.0. Les bibliothèques Python build123d/cq_warehouse/bd_warehouse sont également intéressantes parce qu'elles permettent de **générer la géométrie à partir des dimensions**, plutôt que d'importer un fichier propriétaire.

### Cas McMaster-Carr

Les conditions McMaster restreignent explicitement l'utilisation et la redistribution des modèles CAD : ils sont fournis pour sélectionner/acheter les produits McMaster et ne constituent pas une bibliothèque libre à republier.

**Conséquence YXOR :** un dépôt open source devrait privilégier des géométries générées à partir de **normes/dimensions légalement utilisables**, ou des bibliothèques libres, plutôt que committer directement des STEP propriétaires de catalogues.

---

# 10. Bonnes pratiques DFM internationales

Voici les données les plus utiles trouvées en complément du LOT A.

| Source | Pays | Procédé | Exemple de règle publiée | Nature |
|---|---|---|---|---|
| Protolabs | USA/EU | sheet metal | features laser ≈±0,13 mm selon service ; distances/flexion spécifiques | M/E |
| SendCutSend | USA | laser | petits détails jusqu'à ≈0,5t selon tests service | M/E |
| OSH Cut | USA | laser | pour 5052-H32 ≈3,175 mm : trou recommandé ≈1,60 mm ; minimum ≈0,79 mm ; kerf ≈0,152 mm | M/E |
| Fictiv | USA | sheet | trou laser annoncé jusqu'à ≈0,2t ; distance pli selon t+R | E |
| Xometry | USA/global | laser | règles plus conservatrices allant jusqu'à 2t selon service | E |
| Fractory | Europe | laser | hole/cut spacing souvent ≥t | E |
| Facturee | Allemagne | fabrication | tolérances typiques laser ≈±0,1–0,2 mm publiées | E/M service |
| PCBWay | Chine | laser | ±0,1 mm annoncé ; trou min ≈0,5t sur page service ; max ≈3000×1500 | M/E |
| service australien JDL | Australie | sheet | 5052 : R recommandé 1,5–2t ; 6061-T6 ≈3t recommandé | E |
| service indien étudié | Inde | laser | kerf ≈0,1–0,3 ; trou ≥t ; tolérance ~0,1 selon service | M/E |

Exemple particulièrement parlant : OSH Cut publie pour du 5052-H32 ≈3,175 mm un trou **minimum** bien inférieur à t, mais un trou **recommandé** plus grand. Cela renforce la distinction entre :

- limite physique/expérimentale ;
- bonne pratique portable ;
- règle structurelle.

Pour YXOR open source, **la limite extrême d'un seul service n'est donc pas la bonne règle de conception générique**.

Pour la Corée, un guide de sous-traitance public donnant une matrice numérique comparable et mieux documentée que les sources ci-dessus : **non trouvé**.

---

# 11. Fabricants de machines laser

| Constructeur | Technologie trouvée | Positionnement/répétabilité publié | Kerf / min feature universel |
|---|---|---|---|
| AMADA | fibre | répétabilité axes jusqu'à **±0,01 mm** sur ENSIS-AJe | **non trouvé** |
| Bystronic | fibre | ByCut : répétabilité ≈**0,025 mm**, position ≈**0,051 mm** selon ISO 230-2 | non trouvé |
| Prima Power | fibre | ≈**0,03 / 0,03 mm** | non trouvé |
| LVD | fibre | Phoenix : répétabilité ≈**±0,025**, position ≈**±0,050 mm** | non trouvé |
| Mitsubishi Electric | fibre | certains GX : position ≈0,05/500 mm ; répétabilité ≈±0,01 | non trouvé |
| Han's Laser | fibre | certaines machines ≈±0,03 mm/m position ; ±0,02 répétabilité | non trouvé |
| HSG | fibre | certaines GX ≈±0,03 mm/m | non trouvé |
| TRUMPF | fibre/solid-state + historiques CO₂ | modèle-dépendant | matrice universelle non trouvée |
| Mazak | fibre/CO₂ selon générations | modèle-dépendant | non trouvé |
| Bodor | fibre | documentation commerciale disponible | donnée comparable suffisamment robuste : non trouvé |

AMADA publie également des capacités allant largement au-delà des 1–6 mm selon puissance et matériau. Prima et LVD publient des caractéristiques comparables. :chatgpt-content-reference{index="23"}

### Point critique

**±0,01 mm de répétabilité d'axe n'est pas ±0,01 mm sur la pièce.**

LVD le dit explicitement : la précision réelle de pièce dépend notamment :

- du type de pièce ;
- de son prétraitement ;
- de ses dimensions ;
- des conditions du process. :chatgpt-content-reference{index="24"}

Cela invalide toute tentative de comparer directement l'annonce opérateur **±0,5 mm [O]** à une répétabilité servo OEM.

---

# 12. Robots open source à structure métallique

## 12.1 MEVITA / MEVIUS

MEVITA est le précédent le plus proche trouvé du concept YXOR : le projet est explicitement présenté comme un humanoïde assemblé à partir de composants disponibles commercialement et de pièces intégrant de la **tôlerie/soudage**. Le dépôt est sous licence MIT. :chatgpt-content-reference{index="25"}

Matériau exact + épaisseurs de chaque tôle dans les fichiers consultés :

**non trouvé.**

### Leçon utile

Réduire le nombre de références structurelles en intégrant plusieurs fonctions dans des pièces de tôle est une approche déjà explorée sur un humanoïde open source.

---

## 12.2 ODRI — Solo / Bolt

ODRI publie une grande partie du hardware des actuateurs et des robots Solo/Bolt avec :

- fichiers mécaniques ;
- pièces usinées ;
- pièces imprimées ;
- hardware détaillé ;
- licences ouvertes, largement BSD-3-Clause. :chatgpt-content-reference{index="26"}

Ce n'est pas un précédent « tôle pliée » aussi direct que MEVITA, mais c'est une excellente référence de **documentation reproductible d'un robot dynamique**.

---

## 12.3 Berkeley Humanoid Lite

Le Berkeley Humanoid Lite est open source ; beaucoup de pièces structurelles sont **imprimées 3D**, pas découpées en tôle. Logiciel MIT ; d'autres assets sont notamment sous CC-BY-SA. :chatgpt-content-reference{index="27"}

Leçon utile : architecture légère, actuateurs modulaires et documentation ; **pas une source directe de règles laser aluminium**.

---

## 12.4 ToddlerBot

ToddlerBot mesure environ **0,56 m** et ≈3,4 kg dans sa publication, avec structure très largement imprimée 3D et composants du commerce. :chatgpt-content-reference{index="28"}

Très proche de YXOR en échelle, mais pas en procédé structurel.

---

## 12.5 Upkie

Upkie fournit une architecture mécanique open source et ses pièces CAO, essentiellement pour un robot à roues avec pièces imprimées/usinées selon sous-ensemble. Licence Apache-2.0 pour le dépôt principal étudié. :chatgpt-content-reference{index="29"}

---

## 12.6 Poppy

Poppy reste un précédent majeur en robotique humanoïde open hardware, mais sa structure repose fortement sur l'impression 3D.

**Conclusion documentaire :**

- **MEVITA** → référence la plus pertinente pour structure métal/tôlerie ;
- **ODRI/Bolt/Solo** → référence forte pour modules mécaniques et documentation hardware ;
- **ToddlerBot/Berkeley/Poppy** → références architecture/open-source, mais ne justifient pas des valeurs DFM de tôle YXOR.

---

# 13. Enquête Act/Cut et DPR

## Verdict : **1. IDENTIFIÉ AVEC CERTITUDE**

### 13.1 Act/Cut

Act/Cut est bien un logiciel **ALMA** de CFAO/CAM et d'imbrication pour machines de découpe/poinçonnage.

ALMA documente notamment son utilisation pour :

- laser ;
- plasma ;
- oxycoupage ;
- jet d'eau ;
- nesting ;
- programmation CN.

Sur certains clients, Act/Cut a ensuite été migré vers **Almacam Cut**, la génération actuelle. :chatgpt-content-reference{index="30"}

---

## 13.2 DPR

ALMA mentionne explicitement les **« unitary parts (DPR files) »** dans ses workflows et décrit l'import de DXF puis la création de pièces DPR. :chatgpt-content-reference{index="31"}

ALMA indique également dans son logiciel Sign :

> export de fichiers DXF ou DPR pour programmation dans Act/Cut. :chatgpt-content-reference{index="32"}


Une ancienne documentation de formation Act/Cut identifie DPR comme **format propriétaire ALMA du dessin Drafter**. La source n'est pas officielle actuelle, mais elle est cohérente avec les documents ALMA primaires. :chatgpt-content-reference{index="33"}

### Donc

**`.DPR` n'est pas une faute de frappe.**  
C'est bien un format/fichier de pièce employé par l'écosystème ALMA/Act-Cut.

La spécification interne complète du format DPR :

**non trouvé publiquement.**

---

## 13.3 DXF

DXF est explicitement documenté par ALMA comme format d'entrée/export dans le workflow Act/Cut. :chatgpt-content-reference{index="34"}

**Verdict : confirmé.**

---

## 13.4 SVG

Je n'ai pas trouvé dans la documentation ALMA officielle étudiée la preuve que **SVG est un format natif importable par la version exacte d'Act/Cut de l'opérateur**.

ALMA Sign accepte de nombreux formats graphiques et peut produire DXF/DPR, mais cela n'établit pas qu'Act/Cut lit SVG nativement. :chatgpt-content-reference{index="35"}

**SVG : non trouvé / à confirmer sur sa version.**

---

## 13.5 « 5 axes »

ALMA a également proposé **Act/Cut 3D** pour la découpe laser 5 axes. Un cas client ALMA décrit explicitement génération de trajectoires en tenant compte de la cinématique et des limites d'axes. :chatgpt-content-reference{index="36"}

Cela signifie :

> la déclaration « 5 axes » de l'opérateur pourrait parfaitement désigner une **découpe laser 3D 5 axes**, et pas un centre de fraisage 5 axes.

À ce stade : **non vérifiable**.

---

# 14. Croisement avec les déclarations de l’opérateur

| Déclaration [O] | Valeur | Comparaison documentaire | Verdict | Pourquoi / à confirmer |
|---|---:|---|---|---|
| découpe laser | — | cohérent avec Act/Cut et procédés annoncés | **COHÉRENT** | demander machine |
| rayon intérieur laser | **2 mm** | largement plausible sur tôle 3 mm ; des services publient plus petit | **CONSERVATEUR** | mesurer sur coupon |
| « peut-être moins » | <2 mm | aucune valeur chiffrée | **NON VÉRIFIABLE** | tester R0,5/1/1,5/2 |
| « diamètre faisceau » | **2 mm** | incompatible sémantiquement avec kerf 0,5 si désigne spot focalisé ; pourrait être buse ou autre diamètre | **POTENTIELLEMENT INCOHÉRENT** | demander ce que mesure exactement « 2 mm » |
| kerf | **0,5 mm** | haut mais compatible avec enveloppes service du LOT A | **COHÉRENT** | mesurer par matière/t |
| compensation kerf | opérateur | CAM industriel sait compenser le côté de coupe | **COHÉRENT** | envoyer contour nominal si confirmé |
| tolérance contour | **±0,5 mm** | plus large que de nombreux services ±0,1–0,2 | **CONSERVATEUR** | vérifier sur pièce test |
| épaisseur | 1–6 mm | plage banale pour laser métal | **COHÉRENT** | matrice matière/t |
| ailleurs 1–10 mm | contradiction apparente | peut désigner autres matières/puissances | **POTENTIELLEMENT INCOHÉRENT** | demander limites par matériau |
| aluminium | — | standard laser moderne | **COHÉRENT** | alliage/état |
| inox | — | standard | **COHÉRENT** | nuance |
| laiton | — | possible sur fibre moderne approprié | **COHÉRENT** | machine/procédé |
| titane | — | techniquement possible | **COHÉRENT** | grade/gaz/qualité |
| céramique | — | atypique pour atelier standard de tôle laser | **ÉTONNANT** | quel type de céramique et quel procédé ? |
| pliage | — | standard atelier tôle | **COHÉRENT** | presse/outillage |
| rayon intérieur pli | **5 mm** | à t=3 → R/t=1,67 ; cohérent avec 5052-H32, pas avec tous les Al | **COHÉRENT** | uniquement sous condition alliage/outillage |
| espacement pièces | **10 mm** | très supérieur au kerf et aux minima de nombreux services | **CONSERVATEUR** | probablement règle nesting/thermique/squelette |
| tôle ≥2 m | — | OEM courants ~3×1,5 ou 4×2 m | **COHÉRENT** | dimensions utiles exactes |
| alésage après découpe | — | procédé secondaire logique | **COHÉRENT** | tolérance et machine |
| « 5 axes » | — | pourrait être fraisage ou laser 3D | **NON VÉRIFIABLE** | demander procédé/machine |
| DXF | — | officiellement supporté par ALMA | **COHÉRENT** | version DXF |
| SVG | — | support natif Act/Cut non établi | **NON VÉRIFIABLE** | test d'import |
| DPR | — | format de pièce ALMA documenté | **COHÉRENT** | version exacte |
| Act/Cut | ALMA | logiciel réellement existant | **COHÉRENT** | version / post-processeur |

### Le point le plus suspect : « diamètre du faisceau 2 mm »

Il faut distinguer quatre choses :

1. **diamètre du spot focalisé** ;
2. **largeur de kerf** ;
3. **diamètre de buse** ;
4. **diamètre minimum d'un trou**.

Une buse de quelques millimètres et une saignée de quelques dixièmes sont parfaitement compatibles.

En revanche, appeler simultanément **2 mm « diamètre du faisceau »** et annoncer **0,5 mm de kerf** mérite clarification. Cela ne suffit pas à conclure que l'opérateur se trompe : il peut simplement avoir employé le mauvais terme.

---

# 15. Questions à poser à l'opérateur

## P0 — avant de dessiner une pièce

1. Quelle est **la marque et le modèle exact** de la machine de découpe ?
2. Est-ce un laser **fibre, disque/solid-state ou CO₂** ?
3. Quelle est sa **puissance nominale en kW** ?
4. Quelles sont les dimensions utiles exactes **X × Y** de la table ?
5. Pour l'aluminium 3 mm, quelles nuances avez-vous déjà coupées : **5052, 5754, 5083, 6061, 6082, 7075** ?
6. Quel est votre **plus petit trou fiable** dans aluminium 3 mm ?
7. Quelle est votre **fente minimale fiable** en 3 mm ?
8. Quel est le **web minimal fiable entre deux découpes** ?
9. Le « rayon laser 2 mm » correspond-il à un **rayon CAO intérieur minimum garanti** ?
10. Le « diamètre 2 mm » correspond-il au **spot, à la buse, au trou minimal ou autre chose** ?
11. Quelle saignée mesurez-vous réellement en aluminium 3 mm ?
12. Dois-je vous fournir **la géométrie nominale sans compensation de kerf** ?
13. La tolérance ±0,5 mm concerne-t-elle **tout contour fini** ou seulement certaines dimensions ?
14. Quels formats votre version exacte d’Act/Cut importe-t-elle directement : DXF, DWG, SVG, DPR ?
15. Quelle **version d’Act/Cut** utilisez-vous ?
16. Quelle presse plieuse utilisez-vous ?
17. Quelles ouvertures de matrice **V** avez-vous pour du 3 mm ?
18. Quel rayon de poinçon utilisez-vous ?
19. Avec aluminium 3 mm, quel **rayon intérieur réel obtenu** mesurez-vous ?

## P1 — avant de commander

20. Quel gaz utilisez-vous sur aluminium 3 mm : N₂, air ou autre ?
21. Quel diamètre de buse et quelle configuration de focus utilisez-vous ?
22. Avez-vous un tableau interne matière × épaisseur × paramètres ?
23. Les 1–10 mm s'appliquent-ils à **toutes** les matières ou seulement certaines ?
24. Quelle céramique avez-vous déjà coupée, et avec quel procédé ?
25. À quoi sert exactement la règle de **10 mm entre pièces** ?
26. Ajoutez-vous automatiquement des micro-joints ?
27. Quelle tolérance angulaire garantissez-vous après pliage ?
28. Corrigez-vous automatiquement le springback ?
29. Disposez-vous de valeurs **bend deduction/K-factor** mesurées pour votre outillage ?
30. Respectez-vous le sens de laminage pour les alliages T6 ?
31. Fournissez-vous la nuance et l'état métallurgique certifiés du matériau ?

## P2 — avant une pièce de précision

32. Le « 5 axes » est-il un **centre de fraisage 5 axes** ou un laser 3D 5 axes ?
33. Marque et modèle de cette machine ?
34. Quelle tolérance garantissez-vous sur un **alésage Ø8/Ø10/Ø12** ?
35. Pouvez-vous produire un **H7 contrôlé** ?
36. L'alésage est-il réalisé par alésoir, boring ou interpolation ?
37. Quelle circularité et quelle position vraie pouvez-vous contrôler ?
38. Quel instrument utilisez-vous : micromètre intérieur, bore gauge, CMM ?
39. Pouvez-vous reprendre des trous de goupilles après laser ?
40. Quelle rugosité Ra pouvez-vous garantir sur une portée de roulement ?

---

# 16. Coupon de calibration YXOR — aluminium 3 mm

Toutes les dimensions de cette section sont **[E — proposition expérimentale YXOR]**, et non des capacités déclarées de l’opérateur.

## 16.1 Coupon laser principal

**Plaque : 200 × 120 × 3 mm**, même nuance et même lot que les futures pièces.

### Série A — trous

Ø :

**1 / 1,5 / 2 / 2,5 / 3 / 3,2 / 3,4 / 3,6 / 4 / 5 / 6 / 8 / 10 mm**

Répéter trois fois :

- Ø2 ;
- Ø2,5 ;
- Ø3 ;
- Ø3,4 ;
- Ø4 ;
- Ø6.

Cela permet de séparer **diamètre minimum** et **répétabilité**.

### Série B — fentes

Largeur :

**1 / 1,5 / 2 / 2,5 / 3 / 3,4 / 4 / 5 mm**

Longueur : **15 mm**.

### Série C — webs / ponts

Entre deux fenêtres :

**0,5 / 0,75 / 1 / 1,25 / 1,5 / 2 / 2,5 / 3 / 4 / 5 mm**.

### Série D — trou → bord

Avec trous Ø3,4 mm, ligament réel trou/bord :

**0,5 / 1 / 1,5 / 2 / 3 / 4,5 / 6 mm**.

### Série E — rayons concaves CAO

Coins intérieurs :

**R0 / R0,25 / R0,5 / R1 / R1,5 / R2 / R3 mm**.

Cela donnera une réponse objective à « 2 mm, peut-être moins ».

### Série F — languettes

Largeur :

**1 / 1,5 / 2 / 3 / 4,5 / 6 mm**.

### Série G — angles aigus

Pointes :

**20° / 30° / 45° / 60°**.

### Série H — emboîtements

Peigne slots/tabs autour de l'épaisseur nominale :

**2,70 / 2,80 / 2,90 / 3,00 / 3,10 / 3,20 / 3,30 mm**.

Cela permet de trouver expérimentalement le jeu nécessaire pour :

- glissant ;
- positionnement serré ;
- emboîtement temporaire.

### Série I — répétabilité/position

5 trous Ø6 mm sur entraxe nominal **25,000 mm**.

Ajouter :

- carré intérieur 20×20 ;
- référence extérieure 20×20 ;
- grandes dimensions de contrôle entre datums.

### Mesure réelle du kerf

Une pièce dont le CAM compense le kerf ne permet pas de déduire directement le kerf à partir de la cote finale.

Demander soit :

- une **fente sans compensation**, si Act/Cut le permet ;
- soit conserver et mesurer **pièce + squelette correspondant**.

---

## 16.2 Coupons de pliage

Trois bandes :

**150 × 30 × 3 mm**.

Si le sens de laminage est connu :

- coupon A : pli parallèle au grain ;
- B : 45° ;
- C : perpendiculaire.

Demander un pli à **90°** avec le rayon/outillage habituel.

Ajouter des trous à :

**6 / 9 / 12 / 15 mm** de la ligne théorique de pli.

Mesurer après retour élastique :

- angle ;
- rayon intérieur ;
- longueurs de brides ;
- déplacement des trous ;
- BA/BD ;
- K-factor inversement calculé.

Ce test est bien plus utile à YXOR qu'un K-factor générique trouvé sur Internet.

---

# 17. Tableau final des divergences LOT A + LOT B

| Paramètre | Sources/valeurs observées | Nature | Domaine | Valeur prudente YXOR |
|---|---|---|---|---|
| trou laser | ≈0,2t Fictiv ; ≈0,5t SCS/PCBWay ; ≥t Protolabs/Fractory | E/M | services différents | **≥t** |
| trou Al 3 mm | services capables <3 mm | M/E | parc particulier | **3,0 mm générique** avant coupon |
| fente | ≈0,5t à ≥t | E | service | **≥3 mm** pour t=3 |
| web | ≈0,5t réalisable ; davantage conseillé structurel | E | géométrie/service | **1,5t = 4,5 mm** |
| kerf | ≈0,15 ; 0,2–0,3 ; jusqu'à ~0,5 mm | M/E/O | machine/process | **opérateur : 0,5 mm jusqu'à mesure** |
| offset kerf CAO | opérateur dit le compenser | O | Act/Cut | **0 mm d'offset manuel** si confirmé |
| contour | services ≈±0,1–0,2 ; opérateur ±0,5 | M/O | atelier | **±0,5 mm** |
| rayon laser | opérateur 2 mm ; certains services inférieur | O/M | machine | **R2 mm provisoire** |
| R pli 5052 3mm | LOT A ≈1,5t →4,5mm ; opérateur5mm | E/O | 5052-H32 | **5 mm** |
| R pli 6061 | beaucoup plus grand selon t | E | T6 | **5 mm non validé** |
| trou→pli | Fictiv ~3t ; LOT A Protolabs ~4t | E | process | **4t=12 mm** |
| K-factor | ~0,37–0,48 selon procédés ; opérateur inconnu | E/M | presse | **0,40 seulement provisoire** |
| M3 passage | ISO 3,2/3,4/3,6 | N | fine/moyenne/large | **3,4 mm moyen** |
| M3 tap drill coupant | 2,459–2,599 | M | Guhring | **2,5 mm nominal** |
| M3 tap drill formant | ≈2,78–2,85 | M | outil spécifique | dépend taraud |
| engagement M3 Al | ≈1,4–2D sur exemples Bossard | E | alliage/classe | **non universel** |
| M3 direct t=3 | 1D géométrique | calcul | tôle | vérifier arrachement |
| M6 8.8 torque | 9,0 Nm μ=.10 ;11,3 μ=.14 | E/M | Bossard | friction obligatoire |
| CLA-M3 hole | 4,75 +0,08 | M | PEM CLA | uniquement CLA |
| RIVKLE M3 | 5,0 mm | M | Böllhoff | uniquement série |
| CLA-M3 edge | C/L ≥5,6 mm | M | PEM CLA | uniquement CLA |
| bearing housing | H7 à P7 suivant charge | M/E | NTN | **pas de fit générique** |
| « faisceau 2 mm » | kerf annoncé0,5 | O | définition inconnue | **clarifier** |
| 5 axes | fraisage ou laser3D | O | machine inconnue | **clarifier** |

---

# 18. Registre final des sources LOT B

Le registre A01–A30 du LOT A reste valide et n'est pas reproduit intégralement ici. Les entrées suivantes sont celles ajoutées/utilisées pour le LOT B.

| ID | Organisation | Pays | Type | Sujet | Gratuit/payant | Prix observé | Réutilisation | Date doc | Consulté | Fiabilité |
|---|---|---|---|---|---|---:|---|---|---|---|
| B01 | ISO | international | norme | ISO273 | payant | CHF44 | copyright ISO | 1979, confirmé2024 | 02/10/26 | A :chatgpt-content-reference{index="37"} |
| B02 | JSA | Japon | norme | JIS B1001 | payant | ¥1430/¥4400 | copyright | 1985, confirmé2024 | 02/10/26 | A :chatgpt-content-reference{index="38"} |
| B03 | SAMR | Chine | norme | GB/T5277 | fiche gratuite | — | texte selon droits CN | 1985/current | 02/10/26 | A :chatgpt-content-reference{index="39"} |
| B04 | ASME | USA | norme | B18.2.8 | payant | USD39 | copyright | 1999 S2021 | 02/10/26 | A :chatgpt-content-reference{index="40"} |
| B05 | Guhring | Allemagne | outilleur | taraudage | gratuit | — | doc fabricant | actuel | 02/10/26 | A :chatgpt-content-reference{index="41"} |
| B06 | YAMAWA | Japon | outilleur | % filet | gratuit | — | doc fabricant | actuel | 02/10/26 | A |
| B07 | Bossard | Suisse | industriel | engagement filet | gratuit | — | doc technique | 2023/26 | 02/10/26 | A/B :chatgpt-content-reference{index="42"} |
| B08 | Bossard | Suisse | industriel | couples VDI2230 | gratuit | — | doc technique | 2025/26 | 02/10/26 | A/B :chatgpt-content-reference{index="43"} |
| B09 | Henkel/Loctite | Allemagne/global | fabricant | frein-filet | gratuit | — | doc fabricant | actuel | 02/10/26 | A |
| B10 | NASA | USA | institution | Fastener Design Manual | gratuit | — | US Gov public | 1990 | 02/10/26 | A :chatgpt-content-reference{index="44"} |
| B11 | NASA | USA | standard public | NASA-STD-5020B | gratuit | — | public | 2021, revalidé2026 | 02/10/26 | A :chatgpt-content-reference{index="45"} |
| B12 | Nord-Lock | Suède | fabricant | vibration | gratuit | — | doc fabricant | actuel | 02/10/26 | A/B :chatgpt-content-reference{index="46"} |
| B13 | PEM/PennEngineering | USA | fabricant | self-clinch | gratuit | — | doc fabricant | actuel | 02/10/26 | A :chatgpt-content-reference{index="47"} |
| B14 | Böllhoff | Allemagne | fabricant | RIVKLE | gratuit | — | doc fabricant | actuel | 02/10/26 | A :chatgpt-content-reference{index="48"} |
| B15 | ISO | international | norme | ISO2338 | payant | ≈CHF44 | copyright | 1997/current | 02/10/26 | A |
| B16 | ISO | international | norme | ISO8734 | payant | ≈CHF44 | copyright | 1997/current | 02/10/26 | A |
| B17 | ISO | international | norme | ISO8752 | payant | non trouvé | copyright | 2009/current | 02/10/26 | A |
| B18 | SPIROL | USA/global | fabricant | goupilles | gratuit | — | doc fabricant | actuel | 02/10/26 | A |
| B19 | NTN | Japon | fabricant roulements | fits | gratuit | — | doc fabricant | catalogue | 02/10/26 | A :chatgpt-content-reference{index="49"} |
| B20 | Schaeffler | Allemagne | fabricant | portées/rugosité | gratuit | — | doc fabricant | actuel | 02/10/26 | A :chatgpt-content-reference{index="50"} |
| B21 | FreeCAD/Fasteners | international | OSS | bibliothèque CAO | gratuit | — | GPLv2 code | actuel | 02/10/26 | A |
| B22 | OpenSCAD MCAD | international | OSS | CAD paramétrique | gratuit | — | LGPL2.1 | actuel | 02/10/26 | A |
| B23 | BOSL2 | international | OSS | vis paramétriques | gratuit | — | BSD-2 | 2026 | 02/10/26 | A |
| B24 | NopSCADlib | UK/international | OSS | hardware CAD | gratuit | — | GPL3 | actuel | 02/10/26 | A |
| B25 | build123d ecosystem | international | OSS | Python CAD | gratuit | — | Apache2 selon projet | actuel | 02/10/26 | A |
| B26 | McMaster-Carr | USA | catalogue | CAD fournisseur | gratuit d'accès | — | redistribution restreinte | actuel | 02/10/26 | A |
| B27 | Protolabs | USA/EU | service | DFM | gratuit | — | référence | actuel | 02/10/26 | B |
| B28 | SendCutSend | USA | service | DFM laser | gratuit | — | référence | 2025/26 | 02/10/26 | B |
| B29 | OSH Cut | USA | service | DFM laser | gratuit | — | référence | actuel | 02/10/26 | B |
| B30 | Fictiv | USA | service | DFM sheet | gratuit | — | référence | 2024+ | 02/10/26 | B |
| B31 | PCBWay | Chine | service | DFM laser | gratuit | — | référence | actuel | 02/10/26 | B |
| B32 | AMADA | Japon | OEM machine | laser | gratuit | — | doc fabricant | actuel | 02/10/26 | A |
| B33 | Bystronic | Suisse | OEM machine | laser | gratuit | — | doc fabricant | 2026 | 02/10/26 | A |
| B34 | Prima Power | Italie/Finlande | OEM | laser | gratuit | — | doc fabricant | actuel | 02/10/26 | A |
| B35 | LVD | Belgique | OEM | laser | gratuit | — | doc fabricant | actuel | 02/10/26 | A |
| B36 | Mitsubishi Electric | Japon | OEM | laser | gratuit | — | doc fabricant | actuel | 02/10/26 | A |
| B37 | Han's Laser | Chine | OEM | laser | gratuit | — | doc fabricant | actuel | 02/10/26 | A |
| B38 | HSG Laser | Chine | OEM | laser | gratuit | — | doc fabricant | actuel | 02/10/26 | A |
| B39 | ALMA | France | éditeur CAM | Act/Cut/DPR | gratuit | — | doc éditeur | actuel/archives | 02/10/26 | A :chatgpt-content-reference{index="51"} |
| B40 | MEVITA | Japon | projet OSS | humanoïde | gratuit | — | MIT | actuel | 02/10/26 | A/B |
| B41 | ODRI | Europe | projet OSS | Bolt/Solo | gratuit | — | BSD3 | actuel | 02/10/26 | A |
| B42 | Berkeley | USA | recherche OSS | humanoïde | gratuit | — | MIT/CC BY-SA selon asset | 2025/26 | 02/10/26 | A |
| B43 | ToddlerBot | USA | recherche OSS | humanoïde | gratuit | — | selon dépôt | actuel | 02/10/26 | A |
| B44 | Upkie | international | OSS | robot | gratuit | — | Apache2 | actuel | 02/10/26 | A |
| B45 | Poppy | France | OSS/recherche | humanoïde | gratuit | — | GPL/CC selon asset | actuel | 02/10/26 | A |

---

# 19. Tableau final — première pièce YXOR  
## Aluminium 3 mm, laser, éventuellement plié

Le matériau exact n'étant toujours pas indiqué, je distingue les valeurs **process génériques** de celles qui dépendent de l'alliage.

| Paramètre de conception | Valeur prudente | Nature | Source | Justification |
|---|---:|---|---|---|
| trou laser minimal | **3,0 mm** | [E] | LOT A + DFM internationaux | règle portable ≥t malgré capacités <t de certains services |
| largeur fente minimale | **3,0 mm** | [E] | LOT A | ≥t |
| pont/web minimal structurel | **4,5 mm** | [E] | synthèse LOT A/B | 1,5t, plus robuste que limite ~0,5t |
| trou-trou | **ligament ≥4,5 mm** | [E] | synthèse | formule c/c ≥(D1+D2)/2+4,5 |
| trou-bord | **ligament ≥4,5 mm** | [E] | synthèse prudente | à réduire seulement après coupon |
| rayon intérieur laser | **2,0 mm provisoire** | [O] | opérateur | déclaration plus conservatrice que plusieurs services ; à tester |
| tolérance contour | **±0,5 mm** | [O] | opérateur | utiliser la garantie atelier plutôt qu'une capacité OEM théorique |
| kerf brut déclaré | **0,5 mm** | [O] | opérateur | cohérent mais non mesuré |
| kerf à modéliser dans CAO | **0 mm d'offset** | [O/E] | opérateur + logique CAM | si compensation Act/Cut confirmée |
| rayon intérieur pli | **5 mm [O]** | [O] | opérateur | R/t=1,67 ; cohérent pour 5052-H32, pas universel |
| longueur bride minimale | **non trouvé — dépend du V réel** | — | — | à demander à l'opérateur |
| trou→ligne de pli | **≥12 mm** | [E] | Protolabs LOT A | 4t avant connaissance de V |
| bend relief largeur | **≥1,5 mm** | [E] | SendCutSend LOT A | ≥0,5t |
| bend relief longueur/profondeur | **≥8,5 mm env.** | [E] | formule LOT A | R5+t3+≈0,5 |
| facteur K provisoire | **0,40** | [E] | LOT A | esquisse uniquement, à mesurer |
| sens de laminage | **à enregistrer dans la définition matière** | [E] | Aluminum Association LOT A | important surtout alliages durs/T6 |
| alésage roulement | **non trouvé** | — | NTN/Schaeffler | nécessite roulement + charge + bague tournante + matériau |
| H7 si explicitement requis Ø6–10 | **0/+15 µm** | [N] | ISO286 | classe dimensionnelle, pas choix de fit |
| trou passage M3 | **3,4 mm** | [N] | ISO273 moyen | standard international |
| passage M3 fin | 3,2 mm | [N] | ISO273 | option |
| passage M3 large | 3,6 mm | [N] | ISO273 | option |
| perçage taraud M3 coupant | **2,5 mm nominal** | [M/E] | Guhring | plage 2,459–2,599 |
| perçage M3 formant | **≈2,78–2,85 mm** | [M] | Guhring série formage | dépend outil |
| engagement filet M3 alu | **non trouvé universel** | — | Bossard | 5xxx/6xxx diffèrent |
| engagement disponible directement en tôle3 | **≈1D maximum géométrique** | calcul | — | 3mm/Ø3 |
| exemple PEM CLA-M3 trou | **4,75 +0,08 mm** | [M] | PEM | CLA uniquement |
| exemple PEM CLA-M3 bord | **C/L ≥5,6 mm** | [M] | PEM | CLA uniquement |
| rivnut M3 Böllhoff standard | **trou 5,0 mm** | [M] | RIVKLE | montre dépendance produit |
| distance insert/écrou au bord générique | **non trouvé** | — | — | choisir d'abord la référence |
| espacement pièces nesting | **10 mm** | [O] | opérateur | règle atelier conservatrice |
| format principal d'échange | **DXF** | [O+M] | opérateur/ALMA | officiellement documenté |
| DPR | **valide comme format ALMA** | [M] | ALMA | format pièce/workflow |
| SVG | **non trouvé** | — | — | vérifier version opérateur |

### Pour le tout premier dessin

La conclusion technique de cette table est assez nette :

**la CAO YXOR ne devrait pour l'instant encoder que les limites réellement robustes** — par exemple 3 mm de trou/fente, 4,5 mm de ligament structurel, ±0,5 mm de contour et R2 laser — tandis que les éléments dépendant directement de la presse, des roulements, des tarauds et des inserts doivent rester paramétrables jusqu'au coupon et à l'identification de la machine.

---

# 20. Conclusion

## 1. Ce que l'on sait avec confiance

ISO 273 donne pour M3 des trous de passage **3,2 / 3,4 / 3,6 mm** en séries fine/moyenne/large ; la série moyenne de **3,4 mm** est également cohérente avec ASME B18.2.8. ISO 273:1979 est toujours courante en 2026. :chatgpt-content-reference{index="52"}

Un taraud coupant M3×0,5 peut être préparé autour de **Ø2,5 mm**, Guhring publiant **2,459–2,599 mm** ; un taraud formant exige au contraire un diamètre sensiblement plus grand. :chatgpt-content-reference{index="53"}

L'engagement fileté nécessaire dans l'aluminium **n'est pas une constante 1D/1,5D/2D**. Bossard publie par exemple **2D pour AlMg3**, **1,4D pour AlMgSi1** avec une vis 8.8 et environ **1D pour certains Al-Zn-Mg-Cu beaucoup plus résistants**. :chatgpt-content-reference{index="54"}

Le couple de serrage doit être associé à un coefficient de frottement : pour une M6 8.8, les tables Bossard passent par exemple d'environ **9,0 à 11,3 N·m** lorsque μ passe de 0,10 à 0,14.

Les rondelles Grower ne constituent pas un verrouillage vibratoire robuste : NASA-STD-5020B, active et revalidée en 2026, indique qu'elles fournissent très peu voire aucun verrouillage. :chatgpt-content-reference{index="55"}

Un insert M3 n'a pas un trou universel : **PEM CLA-M3 = 4,75 +0,08 mm**, alors qu'un **RIVKLE M3 standard = 5,0 mm**. :chatgpt-content-reference{index="56"}

Pour les roulements, **H7 n'est pas une recette universelle**. Le choix du fit dépend de la bague soumise à une charge tournante, de la charge, du matériau et de la température ; un logement aluminium peut exiger davantage de serrage. :chatgpt-content-reference{index="57"}

Enfin, **Act/Cut et DPR sont identifiés avec certitude** : DPR est bien employé par ALMA comme fichier de pièce dans ses workflows, et DXF est officiellement supporté. :chatgpt-content-reference{index="58"}

## 2. Ce qui dépend de la machine exacte

Les valeurs encore véritablement machine/process-dependent sont le **kerf réel**, le plus petit trou propre, le plus petit rayon concave, les petits webs, la circularité des trous, la perpendicularité du bord, le HAZ, la tolérance réellement obtenue sur la pièce et la quantité de distorsion thermique.

Le **rayon de pliage**, la bride minimale, la bend allowance, la bend deduction et le K-factor dépendent du couple presse + poinçon + V-die + alliage + état métallurgique. Le « R5 mm » de l'opérateur est parfaitement plausible pour certaines configurations d'aluminium 3 mm, mais ne peut pas devenir une règle universelle YXOR.

Le « **faisceau 2 mm** » n'est toujours pas exploitable comme donnée de conception : il faut savoir s'il parle du spot, de la buse, d'un diamètre de perçage ou d'autre chose.

La déclaration « **5 axes** » reste ambiguë : Act/Cut existe également dans des workflows de découpe laser 3D cinq axes, de sorte que cette phrase ne prouve aucunement l'existence d'une fraiseuse CNC 5 axes. :chatgpt-content-reference{index="59"}

## 3. Ce qu'il faut demander à l'opérateur

Les informations P0 essentielles sont : **marque/modèle du laser, technologie fibre/CO₂, puissance, table utile, nuances d'aluminium déjà qualifiées en 3 mm, trou/fente/web/rayon minimums réellement garantis, définition du “2 mm”, kerf mesuré, confirmation de la compensation Act/Cut, tolérance pièce finie, version Act/Cut et formats réellement importables**.

Pour le pliage : **modèle de presse, V-dies disponibles, rayons de poinçons, rayon réellement produit en aluminium 3 mm, tolérance angulaire et éventuelle table K/BA/BD**.

Pour les pièces de précision : **nature exacte du “5 axes”, machine de reprise, procédé d'alésage, tolérance H7 éventuellement garantie et moyen de contrôle métrologique**.

Enfin, la contradiction **1–6 mm / 1–10 mm** doit être remplacée par une vraie matrice :

**matériau × épaisseur × procédé × niveau de qualité garanti**.

## 4. Ce qu'il faut mesurer avant de figer les règles CAO de YXOR

Le coupon **200×120×3 mm** proposé permettra de mesurer sur l'atelier réel les trous **1–10 mm**, les fentes **1–5 mm**, les webs **0,5–5 mm**, les distances trou-bord, les rayons internes **R0 à R3**, les petites languettes, les pointes, les emboîtements autour de 3 mm et la répétabilité géométrique.

Un jeu séparé de coupons pliés **150×30×3 mm** permettra de mesurer le rayon intérieur réel, le springback, la déformation des trous proches du pli et de recalculer le K-factor effectif.

C'est seulement après ces mesures que les déclarations actuelles **R2 laser, kerf 0,5 mm, ±0,5 mm et R5 pli** pourront passer du statut **[O]** à des valeurs **[M-YXOR] reproductibles**, et devenir des contraintes paramétriques fiables dans la CAO open source de YXOR.