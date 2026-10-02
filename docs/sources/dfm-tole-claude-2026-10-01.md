# YXOR : données publiques DFM pour pièces de robot en tôle (alu, inox, titane, laiton, 1–6 mm) — comparatif, divergences et valeurs prudentes

Pour une première pièce de YXOR en aluminium de 3 mm découpée au laser, la contrainte qui pèse le plus n'est pas la précision du laser. Ce sont trois éléments qui se combinent : le rayon intérieur minimal de 2 mm déclaré par l'opérateur, qui interdit en pratique tout trou ou toute fente découpés de moins de 4 mm ; le choix de l'alliage, puisqu'un 6082-T6 de 3 mm exige un rayon de pliage d'environ 3,5 × e ≈ 10,5 mm selon EN 485-2, contre 1 × e pour un 5754-H111\[1\]\[2\] ; et la faible longueur de filet disponible dans 3 mm d'aluminium. Recommandation : 5754-H111 pour toute pièce pliée, 6082-T6 seulement pour les plaques plates, et aucun taraudage direct M3 porteur dans 3 mm d'alu (utiliser des écrous à sertir, des inserts ou des écrous traversants).

## TL;DR

- **Alliage et pliage.** Si la pièce est pliée, prendre du 5754-H111 : rayon minimal normatif 1,0 × e à 3 mm (EN 485-2, via la fiche Reynolds European). Le rayon minimal de 5 mm déclaré par l'opérateur est alors plus prudent que la norme et fait foi. En 6082-T6, la même norme demande 3,5 × e (1,5–3 mm) puis 4,5 × e (3–6 mm), soit 10,5 à 13,5 mm à 3 mm : les 5 mm de l'opérateur ne suffisent plus et le pli risque de fissurer. Le 7075-T6 est à exclure du pliage (6,5 × e).
- **Découpe laser.** Les valeurs publiées pour l'alu de 3 mm vont de 1,5 mm (SendCutSend, 50 % de l'épaisseur) à 3 mm (Protolabs, égal à l'épaisseur) pour le trou minimal. Mais le rayon intérieur de 2 mm de l'opérateur impose de fait Ø ≥ 4 mm et une largeur de fente ≥ 4 mm. Les petits trous (taraudages, passages M3) se percent ou s'alèsent après découpe. La tolérance de ±0,5 mm de l'opérateur est 3 fois plus large que la classe 1 de l'ISO 9013 (±0,15 mm) : c'est elle qu'il faut retenir pour la conception.
- **Normes et sources.** ISO 2768-1:1989 coûte 67 CHF et ISO 9013:2017 159 CHF sur iso.org, plus 18 CHF pour l'amendement ISO 9013:2017/Amd 1:2024, publié le 2024-09-13 (1 page). Leurs tableaux circulent gratuitement chez des fabricants, mais seuls les aperçus iTeh sont « officiellement » gratuits. Selon iso.org, la nouvelle ISO 2768 (édition 2) a atteint le stade 60.00 (« under publication ») le 2026-06-02 et « Will replace ISO 2768-1:1989 » ; la page de l'ISO 2768-1 indique « Expected to be replaced by ISO 2768 within the coming months ». Le format « dpr » est très probablement le format natif de pièce 2D d'Alma (act/cut, Almacam). Les données MatWeb ne sont pas redistribuables.

## Key Findings

1. **Les valeurs publiques sont mesurées sur les machines de la source.** SendCutSend présente ses minima comme « proven out by rigorous testing ».\[3\] 247TailorSteel et Dumaco publient des tableaux propres à leurs lasers.\[3\]\[4\]\[5\] Aucune de ces valeurs ne vaut pour la machine du cousin, qui reste la référence finale. Le tableau de synthèse retient partout le maximum entre littérature et déclarations de l'opérateur.
2. **Les sources divergent d'un facteur 2 à 3** sur la longueur minimale de bord plié (3t + R à 4t + R, ou valeurs absolues de 12 à 17 mm pour 3 mm), la distance trou-pli (2t à 3t + R), le trou minimal (0,5t à 1t) et le pont minimal (0,5t à 1,5t). Le détail figure plus bas.
3. **Le cœur de la conception est normé et gratuit en pratique.** Les classes ISO 273, les perçages de taraudage (DIN 13 : d − P) et les classes ISO 2768-1 sont recopiés à l'identique par de nombreux sites, de façon cohérente.\[6\]\[7\]\[8\] Les couples de serrage, eux, ne sont pas normés et varient d'un facteur 2 selon le frottement supposé.\[9\]
4. **Le taraudage direct dans 3 mm d'alu est faible.** Bossard (01-2025) recommande 2·d d'engagement pour une vis 8.8 dans de l'AlMg3, et Böllhoff 2,5·d d'insert HELICOIL pour une matière à Rm 150–200 MPa.\[10\]\[11\] Un M3 dans 3 mm n'offre que 1·d. Il faut donc des écrous à sertir (PEM CLS-M3-1 : tôle ≥ 0,97–1,0 mm, trou 4,22 mm, axe-bord 4,8 mm)\[12\]\[13\] ou des écrous à rivets (RIVKLE alu M3 : trou 5,0 mm).\[14\]
5. **Plusieurs déclarations de l'opérateur sont cohérentes et prudentes** : R intérieur 2 mm, tolérance ±0,5 mm, R de pliage 5 mm pour le 5754, écart de 10 mm entre pièces. Trois sont étonnantes et doivent être clarifiées : une saignée de 0,5 mm (plus large qu'un laser fibre typique), la découpe laser de céramique et l'expression « 5 axes ».

## Details

### 0. Règles de lecture

- **Nature de la donnée** : [M] valeur mesurée ou garantie par un fabricant sur ses machines ; [E] règle empirique publiée par un fabricant ou un guide ; [N] exigence ou valeur de norme ; [O] déclaration de l'opérateur.
- **Date** : toutes les pages ont été consultées le 2026-10-01. La date de publication est indiquée quand la page en donne une.
- **Règle projet** : quand deux valeurs publiées divergent, on retient la plus prudente (marquée **►**).

### 1. Découpe laser de tôle

**Trou minimal / « hole-dam » pour l'aluminium, par épaisseur [M] — 247TailorSteel (NL, laser fibre, page « Guidelines for laser cutting »)**

| Épaisseur alu | 1 | 1,2–1,5 | 2 | 2,5 | 3–4 | 5 | 6 | 8 | 10 mm |
|---|---|---|---|---|---|---|---|---|---|
| Ø min / voile | 0,5 | 0,8 | 1,5 | 2 | 2,5 | 3,5 | 4 | 5 | 7 mm\[4\] |
| Fente min (alu) | 2 | 2 | 2 | 2,5 | 3 (3 mm) / 3 (4 mm) | 3,5 | 4 | 5 | 7 mm |

Pour l'inox, 247TailorSteel donne 1,5 mm à 3 mm d'épaisseur et 3 mm à 6 mm. Pour l'acier découpé à l'azote, 1,5 mm à 3 mm d'épaisseur. Pour l'acier et l'inox, la fente minimale vaut 1,5 mm jusqu'à 2 mm d'épaisseur, puis 0,7 × e de 2,5 à 15 mm. Bande étroite minimale (anti-voilage) : 15 mm de large pour une longueur de 100 à 750 mm, 40 mm de 750 à 1500 mm. Pièce minimale : 15 × 15 mm jusqu'à 5 mm d'épaisseur.\[4\]

**Dumaco (NL) [M]** : trou minimal alu 1 mm → 1 mm ; 2 mm → 1,5 mm ; 3 mm → 2 mm ; 4 mm → 2,4 mm ; 5 mm → 3,3 mm ; 6 mm → 3,5 mm. Pour l'inox de 3 mm : 1,5 mm. Fente minimale égale au trou minimal. Ponts ≥ 0,5 × épaisseur.\[5\]

**SendCutSend (US) [M/E]** :
- Trous et ponts ≥ 50 % de l'épaisseur.\[15\] Pour la résistance et la qualité de coupe, les ponts « closer to 1X – 1.5X the material thickness ».\[16\]
- Tolérance de découpe ±0,005" (±0,127 mm).\[17\]
- Saignée laser fibre « typically running under 0.01" » (< 0,25 mm).\[17\]
- La page matière 5052 indique pourtant « Minimum hole size: Equal to material thickness » et « at least 2x thickness between a hole and an edge ».\[18\] C'est une divergence interne à SendCutSend : la page matière est la plus prudente.
- Distance minimale entre deux trous circulaires = « min hole to edge ».\[19\]

**Protolabs (tôlerie) [E/M]** :
- Trous et fentes ≥ épaisseur.\[20\]
- Pour les tôles de plus de 0,036" (0,914 mm), trou à au moins 0,125" (3,175 mm) du bord.\[21\]
- Tolérances : Ø de trou ±0,127 mm ; bord-trou et trou-trou ±0,127 mm.\[21\]

**Saignée (kerf)**
- SendCutSend [M] : fibre < 0,25 mm.\[17\]
- Un fabricant chinois de lasers (Kasu Laser, contenu marketing, fiabilité moyenne) annonce 0,12–0,18 mm en alu de 1 mm et 0,25–0,40 mm en alu de 5 mm pour la fibre, et 0,20–0,40 mm pour le CO2. Il propose aussi les règles empiriques « trou ≥ 1,5 × saignée ; fente ≥ épaisseur ; pont ≥ 2 × saignée ».\[22\]
- **La saignée de 0,5 mm de l'opérateur dépasse ces fourchettes.** Elle est compatible avec un CO2 ancien, une buse large ou une marge volontaire. À clarifier.

**Zone affectée thermiquement (ZAT) : non trouvé** (aucune valeur chiffrée de source primaire pour l'alu 1–6 mm). SendCutSend traite la ZAT seulement qualitativement, dans ses cours DFM.\[23\]

**ISO 9013:2017 — tolérances de découpe thermique [N]**
- Domaine : laser 0,5–32 mm, plasma 0,5–150 mm, oxycoupage 3–300 mm (résumé iso.org).\[24\]
- **Perpendicularité / angularité u**, qui englobe la conicité. Plages reprises par laserspechub, source secondaire cohérente avec le document Groupe TMA :

  | Plage | u (mm) | u pour e = 3 mm | Rz5 (µm) |
  |---|---|---|---|
  | 1 | 0,05 + 0,003·e | 0,06 | 10 + 0,6·e |
  | 2 | 0,15 + 0,007·e | 0,17 | 40 + 0,8·e |
  | 3 | 0,4 + 0,01·e | 0,43 | 70 + 1,2·e |
  | 4 | 0,8 + 0,02·e | 0,86 | 110 + 1,8·e |

  Groupe TMA (sous-traitant FR, fiche INS-033) spécifie par défaut la classe 4 pour la perpendicularité, c'est-à-dire u = 0,8 + 0,02·e.\[25\]
- **Écarts limites sur cotes, classe 1** (typique du laser selon la reprise Modulus Metal) :

  | Épaisseur | cote < 3 mm | 3–10 mm | 10–35 mm | 35–125 mm | 125–315 mm | 315–1000 mm |
  |---|---|---|---|---|---|---|
  | > 1 à 3,15 mm | ±0,10 | ±0,15 | ±0,20 | ±0,25 | ±0,25 | ±0,35 |
  | > 3,15 à 6,3 mm | ±0,20 | ±0,20 | ±0,25 | ±0,25 | ±0,30 | ±0,40 |

  Le plasma et l'oxycoupage relèvent typiquement de la classe 2.\[26\] Groupe TMA indique une amorce t1 de 0,4 mm au laser, 1 mm au plasma et 2 mm en oxycoupage.\[27\]

**Jet d'eau et plasma (bref)**
- Jet d'eau chez SendCutSend [M] : trou minimal « 0.070″ or 0.125″ » (1,78 ou 3,18 mm) selon la matière.\[28\]\[29\] Pas de ZAT (propriété physique du procédé).
- Plasma : classe 2 de l'ISO 9013 et amorce de 1 mm. Peu adapté aux petites pièces de 1–3 mm.
- Fraisage-détourage (router) chez SendCutSend : trou ≥ 3,18 mm et angles intérieurs R 1,59 mm.\[3\]\[29\]

**Par matière** : seuls l'aluminium, l'inox et l'acier ont des valeurs chiffrées trouvées. Pour le titane grade 2/5 et le laiton, aucune table de trou ou de pont minimal n'a été trouvée (non trouvé). 247TailorSteel découpe du laiton, mais sur un format maximal réduit (1980 × 980 mm).\[4\]

### 2. Pliage

**Rayons intérieurs minimaux à 90°, norme EN 485-2 [N]** (fiches Reynolds European, consultées 2026-10-01 ; upload 2020-04)

| Alliage / état | 1,5–3 mm | 3–6 mm | Rp0,2 min | Rm | A50 min |
|---|---|---|---|---|---|
| 5754 O/H111 | 1,0 e | 1,0 e | 80 MPa | 190–240 MPa | 16 % / 18 % |
| 5754 H22/H32 (ligne Rp 130) | 1,5 e | 1,5 e | 130 MPa | 220–270 MPa | 10 % / 11 % |
| 6082 T6 | 3,5 e | 4,5 e | 260 MPa | ≥ 310 MPa | 7 % / 10 % |
| 7075 T6 | 6,5 e | — | 470 MPa | ≥ 540 MPa | 7 % |

Pour le 6082 T6, l'épaisseur 0,4–1,5 mm demande 2,5 e. Pour le 7075 T6, l'épaisseur 0,8–1,5 mm demande 5,5 e.\[1\]\[30\]

**Comparaison avec d'autres sources**
- Metallservice.ch (CH) donne pour le 6082 T6 un facteur 2,5 / 3,5 et pour le 6082 O un facteur 0,5 / 1,0.\[31\]
- Le catalogue Prolians/Descours & Cabaud donne pour le 5754 H111 « 1 e » à 3 mm et pour le 5083 H111 « 1 e » à 3 mm. Pour le 6082 T6 à 3 mm il indique « 1 e », ce qui est manifestement une coquille au regard de ses colonnes voisines (3,5 e et 4,5 e).\[32\]
- Ces rayons valent pour un pli **transversal au sens de laminage** (Prolians).\[32\]
- **5052 H32 (alliage US)** : Rivcut donne 1T en travers du laminage et 1,5T dans le sens du laminage à 0,125" ; Fabtek donne environ 1t jusqu'à 1/8".\[33\]\[34\] Le Handbook ASM vol. 14B donne 2t à 0,125", mais il n'est cité que de seconde main (forum Eng-Tips).\[35\] **► 2t.**
- **6061-T6 à 0,125"** : Rivcut donne 4T en travers et 6T dans le sens. **► 6T**, avec recuit local recommandé.\[33\]
- **Inox 304** : 1T–2T (Rivcut, règle empirique). **Laiton C260 recuit** : 0T–1T (Rivcut).\[33\] **Titane** : non trouvé.

**Longueur minimale de bord plié, trou-pli, dégagements**
- SendCutSend, alu 5052 de 0,125" : largeur de matrice 0,630" (16 mm). Les trous taraudés ou fraisés doivent être à ≥ 0,315" (8 mm) de la ligne de pli. Les matrices couvrent 0,472" à 1,575" de part et d'autre du pli. Environ 50 % de la longueur du pli doit respecter le bord minimal.\[36\]\[37\]
- SendCutSend, dégagement de pliage : profondeur = rayon effectif + 0,020".\[36\]
- 247TailorSteel, dégagement : largeur = e/2 ; profondeur = e + R + 0,5 mm. Le 5754 H111 se plie de 1 à 8 mm ; l'épaisseur minimale d'alu est de 1 mm.\[38\]
- Protolabs : angle ±1° ; pli-trou ±0,381 mm ; pli-bord ±0,254 mm ; rayon standard 0,762 mm ; ourlet : diamètre intérieur = e, retour 6e.\[20\]\[21\]

**Facteur K, allongement de pliage, retour élastique : non trouvé** sous forme de valeurs publiques primaires par alliage. SendCutSend publie un calculateur de pliage (Bend Calculator)\[39\] dont les valeurs internes n'ont pas été extraites. Recommandation : faire mesurer par l'opérateur un pli d'essai et en déduire K.

### 3. Fraisage CNC de petites pièces en alu

- **Paroi minimale** : Protolabs donne 0,5 mm possible (cube démonstrateur en 6082) et signale comme « thin wall » toute paroi ≤ 0,51 mm.\[40\]\[41\] D'autres guides recommandent ≥ 0,8 mm en métal (Lewei) ou 1 mm (0,040", Makerstage).\[42\]\[43\] **► 1 mm.**
- **Rayon d'angle intérieur** : au minimum le rayon de l'outil. Hubs recommande ≥ 1/3 de la profondeur de cavité.\[42\]\[44\] Protolabs utilise des fraises jusqu'à 1 mm de diamètre, d'où des rayons « a little more than half » de mm, avec une profondeur de poche limitée.\[45\]
- **Profondeur de poche** : ≤ 4 × largeur (Hubs) ; ≤ 3:1 standard et 6:1 en outillage long (Makerstage). Fente minimale 0,75 mm et profondeur maximale de fente 50 mm (Protolabs EU).\[40\]\[42\]\[44\] **► 3:1.**
- **Tolérance standard** : Protolabs ±0,005" (±0,13 mm).\[41\] Proche d'ISO 2768-m pour les cotes de 6 à 30 mm (±0,2 mm).
- **Logements de roulement H7, goupilles, frein filet : non trouvé** dans les sources consultées. Valeurs à tirer d'ISO 286 (payante) ou des catalogues SKF ou NMB, non vérifiés ici.
- **Taraudage**
  - Perçages (DIN 13 : d − P) : M2 1,6 ; M2,5 2,05 ; M3 2,5 ; M4 3,3 ; M5 4,2 ; M6 5,0 mm.\[8\]\[46\]
  - 247TailorSteel taraude après découpe laser : M3 (perçage 2,5 mm) à partir de 1,0 mm d'épaisseur, M4 (3,3 mm) à partir de 1,4 mm.\[4\] Son tableau donne aussi une épaisseur maximale de 4 mm pour l'alu ; cette lecture du tableau est à vérifier.
  - **Engagement minimal dans l'alu** (Bossard, fiche « Length of engaged thread », 01-2025, essais M6–M16) : en classe 8.8, 2·d dans l'AlMg3 F18 (3·d d'après la formule VDI 2230) ; 1,4·d dans l'AlMgSi1 F32 et l'AlMg4,5Mn F28 ; environ 1,0–1,1·d dans l'AlZnMgCu0,5 F50.\[10\] Aucune valeur n'est donnée pour une vis 12.9 dans l'alu ; la lecture du PDF, dont le texte extrait est désordonné, est à confirmer. Bossard précise : « For exact values a calculation according to VDI 2230 are required. »\[10\]
  - **HELICOIL Plus** (Böllhoff, catalogue 0100/16.02, 2016)
    - Longueurs de 1,0 à 3,0 d en M3–M5.\[11\]
    - Forets : M3 3,20 ; M4 4,20 ; M5 5,20 mm. Tarauds STI d'origine obligatoires.\[11\]\[47\]
    - Longueur minimale de l'insert (alu, d'après VDI 2230) : pour une vis 8.8, 2,5 d si Rm 100–200 MPa et 1,5 d si Rm > 200 MPa ; pour une vis 12.9, 2,5 d jusqu'à Rm 300 MPa.\[11\]
    - **Conséquence** : le 5754 H111 (Rm min 190 MPa) demande 2,5 d, soit 7,5 mm pour un M3. C'est impossible dans 3 mm de tôle.

### 4. Quincaillerie et assemblages

**Trous de passage ISO 273 [N]** (fin H12 / moyen H13 / grossier H14 ; valeurs identiques sur plusieurs reprises et sur la copie du texte ISO 273-1979)

| | M2 | M2,5 | M3 | M4 | M5 | M6 |
|---|---|---|---|---|---|---|
| Fin | 2,2 | 2,7 | 3,2 | 4,3 | 5,3 | 6,4 |
| Moyen | 2,4 | 2,9 | 3,4 | 4,5 | 5,5 | 6,6 |
| Grossier | 2,6 | 3,1 | 3,6 | 4,8 | 5,8 | 7,0 |

Statut de la norme : selon iso.org (page 4183), l'ISO 273:1979 est au stade 90.93 et a été confirmée le 2024-07-10 (« This publication was last reviewed and confirmed in 2024. Therefore this version remains current »). Il n'existe pas d'ISO 20273 : l'équivalent européen est l'EN 20273:1991 (DIN EN 20273, NF EN 20273), qui reprend l'ISO 273:1979.

**Couples de serrage indicatifs [E]** (aucun n'est normatif ; ils dépendent du frottement µ)

| Taille | A2-70 µ 0,1 (Anzor, Belmetric) | A2-70 µ 0,2 (Anzor) | A2-70 « max » (Accu) | 8.8 (Belmetric) | 12.9 (Belmetric) | 12.9 CHC (Monsterbolts) |
|---|---|---|---|---|---|---|
| M3 | 1,0 | 1,1 | 1,35 | 1,37 | 2,30 | 2,20 |
| M4 | 1,7 | 2,6 | 3,0 | 3,10 | 5,25 | 4,83 |
| M5 | 3,4 | 5,1 | 6,1 | 6,15 | 10,4 | 10,0 |
| M6 | 5,9 | 8,8 | 10 | 10,5 | 18 | 16,8 |

Valeurs en N·m. ► Retenir la colonne la plus basse : A2-70 à µ 0,1 pour l'inox, et Monsterbolts pour le 12.9. Pour une vis vissée dans de l'alu, c'est le filet alu qui limite le couple, pas la classe de la vis ; ces chiffres sont des plafonds. A4-70 : mêmes valeurs que A2-70 chez Accu.\[48\]

**Écrous à sertir PEM [M]**
- **CLS-M3-1** (inox 300) : tôle min 0,97–1,00 mm ; trou 4,22 (+0,08) mm ; axe-bord ≥ 4,8 mm.\[49\]\[50\]
- **CLS-M3-2** : tôle min 1,4 mm.\[12\]
- Les types CLS conviennent aux tôles de dureté ≤ HRB 70 / HB 125. Le 6082-T6 (94 HB selon Aalco) reste compatible. Le type **CLA** (alu) est limité à HB ≤ 82, donc **inadapté au 6082-T6**.\[51\]\[52\]
- Les tôles en inox exigent des séries adaptées (SP, SMPP)\[53\] ; la règle générale de dureté est publiée par PEM.\[54\]

**Écrous à rivets aveugles Böllhoff RIVKLE [M]** (catalogue 2307)
- Trous : M3 5,0 ; M4 6,0 ; M5 7,0 mm (+0,1/0).\[14\]\[55\]
- Version alu, tête fine : M3 en plages 0,5–2,0 mm ou 2,0–3,5 mm (cette dernière couvre 3 mm) ; M4 0,25–2,5 ou 3,0–4,5 mm ; M5 0,5–3,0 ou 3,0–5,5 mm.\[55\]
- RIVKLE HRT alu (compatible vis 8.8) à partir de M5.\[55\]

### 5. Normes : gratuit ou payant

| Norme | Prix officiel | Ce qui est gratuit et fiable | Statut |
|---|---|---|---|
| ISO 2768-1:1989 | **67 CHF** (iso.org) ; 110 USD (ANSI) ; 142,98 AUD (Standards Australia) | Tableaux recopiés à l'identique par CSL-IMT (CH), HLH, Brassland, etc. | Stade 90.92 « à réviser » ; **nouvelle ISO 2768 éd. 2 : DIS enregistré le 2025-06-18, stade 60.00 (« under publication ») atteint le 2026-06-02, « Will replace ISO 2768-1:1989 »** (iso.org/standard/85741) ; l'ISO 2768-2:1989 est déjà retirée et remplacée par l'ISO 22081:2021 |
| ISO 9013:2017 | **159 CHF** + Amd 1:2024 **18 CHF** (publié le 2024-09-13, 1 page, ISO/TC 44/SC 8) | Aperçus iTeh (EN et FR, sommaire et définitions) ; formules reprises par des sous-traitants | Confirmée en 2022 (« This publication was last reviewed and confirmed in 2022 ») |
| ISO 273:1979 | **44 CHF** (page miroir committee.iso.org/standard/4183 ; 2 pages, ISO/TC 2/SC 7) | Tableaux largement repris | Confirmée en 2024 |

**ISO 2768-1 (cotes linéaires, mm)** : f / m / c / v

| Plage | f | m | c | v |
|---|---|---|---|---|
| 0,5–3 | ±0,05 | ±0,1 | ±0,2 | — |
| > 3–6 | ±0,05 | ±0,1 | ±0,3 | ±0,5 |
| > 6–30 | ±0,1 | ±0,2 | ±0,5 | ±1,0 |
| > 30–120 | ±0,15 | ±0,3 | ±0,8 | ±1,5 |
| > 120–400 | ±0,2 | ±0,5 | ±1,2 | ±2,5 |

- Rayons et chanfreins : ±0,2 (f/m) ou ±0,4 (c/v) de 0,5 à 3 mm ; ±0,5 ou ±1 de 3 à 6 mm ; ±1 ou ±2 au-delà de 6 mm.\[56\]
- Angles : ±1° (f/m), ±1°30′ (c), ±3° (v) pour un petit côté ≤ 10 mm.\[56\]
- Divergence : Premsa donne ±0,1 en classe f pour la plage 30–120 mm, contre ±0,15 partout ailleurs.\[57\] Coquille probable ; ► ±0,15.

### 6. Matières (gratuit, Europe/Suisse)

| Alliage (tôle) | Rp0,2 | Rm | A | E | ρ | Pliage / usinage | Source |
|---|---|---|---|---|---|---|---|
| 5754 H111 (1,5–6 mm) | ≥ 80 MPa | 190–240 | 16–18 % | 70 GPa (non relevé spécifiquement) | 2,70 (non relevé spécifiquement) | pliage 1 e | EN 485-2 via Reynolds European |
| 6082 T6 (0,4–6 mm) | ≥ 260 | ≥ 310 | 6–10 % | 70 GPa | 2,70 g/cm³ | pliage 2,5–4,5 e ; « machines well » | Aalco, EN 485-2 |
| 7075 T6 (1,5–3 mm) | ≥ 470 | ≥ 540 | 7 % | non relevé | non relevé | pliage 6,5 e | EN 485-2 via Reynolds European |
| 5083, 6061 | non relevé de source primaire européenne (5083 H111 : 1 e à 3 mm, Prolians) | | | | | | |

**Réutilisation des données**
- **MatWeb** : « intended for personal, non-commercial use… may not be reproduced… without permission ». Licence personnelle, 500 matériaux au maximum.\[58\]\[59\] **À ne pas recopier dans le dépôt.**
- Fiches de distributeurs (Aalco, Reynolds) : Aalco précise « indicative only… not to be relied upon in place of the full specification ».\[60\] On cite la valeur avec sa référence EN 485-2 ; on ne redistribue pas le PDF.

### 7. Registre des sources

| Source | Type | Gratuit | Réutilisation | Date | Fiabilité |
|---|---|---|---|---|---|
| 247TailorSteel, guidelines laser et pliage (247tailorsteel.com/en/submission-guidelines/…) | fabricant EU [M] | oui | citation | consulté 2026-10-01 | élevée (pour ses machines) |
| SendCutSend, blog et pages matières (sendcutsend.com) | fabricant US [M/E] | oui | citation | blog 2024-04-15 (modifié 2024-12-12) | élevée, mais incohérences internes |
| Protolabs, design guidelines tôlerie et CNC (protolabs.com) | fabricant [E/M] | oui | citation | n.d. | élevée |
| Dumaco knowledge base (portal.dumaco.com) | fabricant NL [M] | oui | citation | n.d. | moyenne-élevée |
| Reynolds European, fiches EN 485-2 (reynolds-european.fr) | distributeur FR [N recopiée] | oui | citer EN 485-2 | upload 2020-04 | élevée |
| Aalco, fiches techniques (aalco.co.uk) | distributeur UK | oui | « indicative only » | 2019-07-18 (plaque) | élevée |
| Metallservice.ch | distributeur CH | oui | citation | n.d. | élevée |
| iso.org, pages 7748, 60321, 85741 | organisme de normalisation | résumé gratuit, texte payant | © ISO | 2026 | référence |
| Groupe TMA INS-033 (groupe-tma.com) | sous-traitant FR | oui | citation | 2024-12 | moyenne |
| laserspechub, Modulus Metal (reprises ISO 9013) | secondaire | oui | à recouper | n.d. | moyenne |
| PEM catalogue (catalog.pemnet.com, pemnet.com) | fabricant [M] | oui | citation | n.d. | élevée |
| Böllhoff HELICOIL 0100/16.02, RIVKLE 2307 (media.boellhoff.com) | fabricant [M] | oui | citation | 2016 ; 2025 (éd. 2307/25) | élevée |
| Bossard « Length of engaged thread » | fabricant [E, d'après VDI 2230] | oui | citation | 01-2025 | élevée |
| Anzor, Belmetric, Accu, Monsterbolts (couples) | distributeurs [E] | oui | citation | n.d. | moyenne |
| Hubs, Rivcut, Makerstage, Lewei, Prolean, smlease, Approved Sheet Metal, Budde, Performax, allmetalsfab | guides [E] | oui | citation | Approved « 2026 » ; allmetalsfab 2026-07-27 | moyenne à faible |
| MatWeb | base de données | oui, avec restrictions | **interdit de reproduire** | © 1996-2026 | élevée, mais non réutilisable |
| MEVITA (arXiv 2508.17684 ; haraduka.github.io) | projet open source | oui | dépôt github.com/haraduka/mevita sous « MIT license » (fichier LICENSE du dépôt) | 2025 (Humanoids 2025, pp. 997–1003) | élevée |
| Almacam (pages Sign, Quote) | éditeur logiciel | oui | citation | n.d. | élevée pour le format DPR |

**Non couverts dans cette recherche (non trouvé)** : Trumpf, Bystronic et Amada (aucune valeur chiffrée extraite) ; Xometry, OSHCut, Fractory et JLC/PCBWay (la page OSHCut 5052 a été trouvée, sans valeurs exploitables) ; bd_warehouse et FreeCAD Fasteners.

**MEVITA (U-Tokyo JSK)** : tôle A5052 standard, inox SUS304 pour la tôle à haute résistance, A7075 pour les pièces usinées. 18 pièces métalliques uniques, dont 4 en tôle soudée (Base-Link, Hip1, Hip2, support de moteur du mollet).\[61\] C'est un précédent direct qui valide le choix d'un alliage de la série 5000 pour la tôle pliée.

### 8. Croisement avec les déclarations de l'opérateur

| Déclaration | Verdict | Commentaire |
|---|---|---|
| R intérieur min 2 mm | cohérent, prudent | Les services en ligne descendent plus bas. Conséquence : trous et fentes découpés ≥ 4 mm. |
| Saignée 0,5 mm compensée | **étonnant** | Fibre < 0,25 mm (SendCutSend) ; 0,12–0,40 mm (Kasu). Possible en CO2, en tôle épaisse ou par marge volontaire. |
| « Diamètre du faisceau 2 mm » | **incohérent** avec une saignée de 0,5 mm | La saignée est forcément ≥ la tache focale. Les 2 mm désignent probablement le diamètre de buse, ou le faisceau brut avant focalisation (hypothèse, aucune source trouvée). |
| ±0,5 mm de contour | cohérent, très prudent | ISO 9013 classe 1 : ±0,15 mm (3 mm d'épaisseur, cotes de 3 à 10 mm) ; SendCutSend : ±0,127 mm. |
| Alu, laiton, titane, inox ; 1–6 (10) mm | plausible | 247TailorSteel couvre l'alu de 1 à 10 mm. |
| Céramique | **étonnant** | Aucune source trouvée pour la découpe de céramique sur laser à tôle. |
| Pliage R min 5 mm | cohérent pour le 5754 (1 e = 3 mm) ; **insuffisant pour le 6082-T6** (10,5–13,5 mm) et le 7075 | |
| Écart 10 mm entre pièces | cohérent | Concerne l'imbrication, pas la géométrie de la pièce. |
| Alésage après découpe | utile | Permet des trous < 4 mm et des ajustements. |
| « 5 axes » | ambigu | Act/cut 3d d'Alma programme des machines laser, plasma, jet d'eau ou de fraisage en 5 axes ou plus. À préciser.\[62\]\[63\] |
| Formats DXF, SVG, « dpr » | DPR identifié | Almacam : le module Sign « can easily generate dxf files or output files compatible with … act/cut » et permet d'« export DXF or DPR files for programming purpose in act/cut » ; Almacam Quote : « geometry can be designed or defined by a DXF or DPR file ».\[64\]\[65\] Ne pas confondre avec le .dpr de Delphi. Envoyer du DXF (R12 ou 2000, en mm, à l'échelle 1:1). |

**Questions à poser à l'opérateur**
1. Marque et modèle de la machine, laser fibre ou CO2, puissance. Est-ce que « 2 mm » désigne la buse ? Saignée mesurée pour l'alu de 3 mm ?
2. Alliage et état exacts de ses chutes (5754-H111 ? 6082-T6 ? 5083 ?), avec certificat ou marquage. Sens de laminage visible ?
3. Classe ISO 9013 atteinte (perpendicularité, Rz5) et tolérance de position entre trous.
4. Voile ou pont minimal, et trou minimal réel en 3 mm d'alu. Le R 2 mm s'applique-t-il aussi aux trous ronds ?
5. Gaz de coupe (azote ou air) pour l'alu ; gaz inerte pour le titane ; laiton (réfléchissant) possible ?
6. Pliage : ouverture de matrice V, rayon de poinçon, longueur maximale et bord minimal ; facteur K mesuré ; angle ±1° ?
7. Taraudage : sur place ? M2,5 à M5 ? Inserts HELICOIL, PEM ou RIVKLE disponibles ?
8. « 5 axes » : fraiseuse 5 axes ou tête laser 3D ? Quelle précision d'alésage (H7 ?) ?
9. Format DPR : il vient d'act/cut ou d'Almacam ? Le DXF lui suffit-il ?
10. Céramique : quel type, sur quelle machine ?

### Tableau des divergences

| Paramètre (alu 3 mm) | Valeurs publiées | ► Prudent |
|---|---|---|
| Trou min laser | 1,5 mm (SendCutSend, 50 % e) ; 2 mm (Dumaco) ; 2,5 mm (247) ; 3 mm (SendCutSend page 5052, Protolabs, Approved) | **3 mm**, porté à **4 mm** par le R 2 de l'opérateur\[4\]\[5\]\[15\]\[20\] |
| Pont / voile | 0,5 e = 1,5 mm (Dumaco, SendCutSend minimum) ; 2,5 mm (247) ; 1–1,5 e (SendCutSend préféré) | **4,5 mm**\[4\]\[5\] |
| Trou-bord | 3,175 mm (Protolabs) ; 2e = 6 mm (SendCutSend 5052, Budde, Prolean) | **6 mm**\[21\]\[66\]\[67\] |
| Bord plié min | 12 mm (Protolabs 4t ; Performax) ; 12,7 mm (allmetalsfab) ; 3t + R = 14 mm (smlease) ; 4t + R = 17 mm (Approved) | **17 mm**\[20\]\[68\]\[69\]\[70\]\[71\] |
| Trou-pli (bord du trou) | 2t = 6 mm (allmetalsfab) ; 8 mm (SendCutSend, trou taraudé) ; 2t + R = 11 mm (Budde) ; 2,5t + R = 12,5 mm (Prolean) ; 3t + R = 14 mm (Approved, smlease, sheetmetal.me) | **14 mm** (fente : 4t + R = 17 mm, Prolean)\[66\]\[67\]\[68\]\[70\]\[71\]\[72\] |
| R pliage 6082-T6 | 1 e (Prolians, coquille) ; 3,5 e (EN 485-2, Metallservice) ; 4,5 e (EN 485-2, 3–6 mm) | **4,5 e = 13,5 mm**, ou éviter le pliage |
| R pliage 5052-H32 | 1t (Fabtek, Rivcut) ; 1,5T dans le sens du laminage (Rivcut) ; 2t (ASM, de seconde main) | **2t** |
| Engagement d'une vis 8.8 dans AlMg3 | 2·d (Bossard, essais) ; 3·d (formule VDI 2230) | **3·d**\[10\] |

## Recommendations

**Tableau de valeurs de conception PRUDENTES — première pièce, alu 5754-H111, 3 mm, découpe laser, pliage éventuel**

| Paramètre | Valeur retenue | Source déterminante |
|---|---|---|
| Alliage | 5754-H111 si pliée ; 6082-T6 seulement à plat | EN 485-2 (Reynolds) ; MEVITA (5052) |
| Ø trou découpé min | **4 mm** | [O] R 2 mm (contre 3 mm Protolabs / SendCutSend) |
| Trous < 4 mm (taraudage, passage M3) | pointer, puis percer ou aléser après découpe | [O] |
| Largeur de fente min | **4 mm** | [O] R 2 mm (contre 3 mm chez 247) |
| R d'angle intérieur | ≥ 2 mm | [O] |
| Pont / voile min | **4,5 mm** (1,5 e) | SendCutSend « 1X – 1.5X » |
| Bord de trou → bord de pièce | **6 mm** (2 e) | SendCutSend 5052, Budde\[67\] |
| Bord de trou → bord de trou | **6 mm** | idem (règle SendCutSend) |
| Tolérance de contour à prévoir | **±0,5 mm** | [O] (contre ±0,15 en ISO 9013 classe 1) |
| Perpendicularité à prévoir | **0,86 mm** (ISO 9013 plage 4), tant que la classe n'est pas confirmée | ISO 9013 via TMA / laserspechub |
| Cotes non tolérancées | ISO 2768-c (±0,5 de 6 à 30 mm ; ±0,8 de 30 à 120 mm) | ISO 2768-1 |
| R intérieur de pliage | **5 mm** | [O] (contre 3 mm EN 485-2) |
| Bord plié min | **17 mm** (4t + R) | Approved Sheet Metal\[71\] |
| Bord de trou → ligne de pli | **14 mm** (3t + R) ; fente 17 mm | Approved, smlease, Prolean\[66\]\[68\]\[71\] |
| Dégagement de pliage | largeur **4 mm** (contre e/2 chez 247, imposée par le R 2) ; profondeur e + R + 0,5 = **8,5 mm** | 247TailorSteel + [O] |
| Angle de pli | ±1° | Protolabs\[21\] |
| Passage M3 | Ø 3,4 (ISO 273 moyen, percé) ; 3,6 si ajustement grossier | ISO 273 |
| Filet M3 porteur | pas de taraudage direct ; **PEM CLS-M3-1** (trou 4,22, axe-bord ≥ 4,8) ou **RIVKLE alu M3 2,0–3,5** (trou 5,0) ou vis + écrou | PEM, Böllhoff, Bossard\[14\]\[55\] |
| Couple M3 A2-70 | **≤ 1,0 N·m** | Anzor/Belmetric µ 0,1 |
| Distance entre pièces sur la tôle | 10 mm | [O] |
| Fichier | DXF 1:1 en mm, contours fermés, sans pièce flottante | SendCutSend, 247 |

**Étapes suivantes**
1. Envoyer à l'opérateur une **plaque d'essai** en 3 mm (trous de 2 à 6 mm, ponts de 1,5 à 6 mm, fentes, un pli R5 à 90° dans chaque sens de laminage) et mesurer les résultats.
2. Remplacer ensuite chaque valeur de littérature par la valeur mesurée sur sa machine, avec la date. C'est la seule donnée qui vaut pour YXOR.
3. Archiver dans le dépôt les valeurs et leurs références (URL, date, nature), sans les PDF fournisseurs ni les données MatWeb.

## Caveats

- Toutes les valeurs [M] sont valables pour les machines, l'outillage et les matières de leur source. Elles ne garantissent rien sur l'équipement de l'opérateur.
- Plusieurs tableaux viennent de reprises secondaires, faute du texte de norme payant : ISO 9013 (plages de perpendicularité, classe 1), ISO 2768 (cohérent sur au moins 6 sources) et ISO 273.
- Les tableaux Bossard et RIVKLE ont été extraits de PDF au texte désordonné : à revérifier visuellement. Le catalogue HELICOIL consulté date de 2016 ; une édition 0100/24 existe.
- Non trouvé : ZAT chiffrée, facteur K et retour élastique par alliage, tables laser pour le titane et le laiton, rayon de pliage du titane, ajustements de roulements H7, goupilles, frein filet, valeurs Trumpf/Bystronic/Amada, bd_warehouse et FreeCAD Fasteners, données de montage du RobStride RS00.
- La nouvelle ISO 2768 (éd. 2), au stade 60.00 « under publication » depuis le 2026-06-02 selon iso.org, pourra modifier les classes. Vérifier sa publication avant de figer le cartouche.

## Sources

1. [Selon Norme NF EN 485-2 TÔLES EN ALUMINIUM EN AW-6082 Etat Epaisseur spécifiée](http://www.reynolds-european.fr/wp-content/uploads/2020/04/fiche-toles-alu-AW-6082.pdf)
2. [Selon Norme NF EN 485-2 TÔLES EN ALUMINIUM EN AW-5754 Etat Epaisseur spécifiée](http://www.reynolds-european.fr/wp-content/uploads/2020/04/fiche-toles-alu-AW-5754.pdf)
3. [How to Measure Cut Geometry Specifications Using QCAD](https://sendcutsend.com/blog/how-to-measure-cut-geometry-specifications-using-qcad/)
4. [Guidelines for laser cutting](https://247tailorsteel.com/en/submission-guidelines/guidelines-for-laser-cutting)
5. [Laser cutting guidelines - Knowledge base](https://portal.dumaco.com/knowledgebase/en/operations/lasercutting/guidelines/)
6. [General Tolerances ISO 2768-1](https://hlhrapid.com/wp-content/uploads/2022/09/ISO-2768-1-Tolerance-Chart-HLH-Rapid.pdf)
7. [Clearance Hole Sizes (ISO 273) - Engineering Hardware](https://engineeringhardware.com/fastener/clearance-hole-sizes/)
8. [What Size Clearance Hole for a Metric Bolt? ISO 273 Chart + Tap Drill](https://www.ekinsun.com/custom-fasteners/clearance-hole-chart/)
9. [Metric Tightening Torques - Anzor Fasteners](https://www.anzor.co.nz/technical/stainless-steel-technical-info/tightening-torques/metric-tightening-torques)
10. <https://assets.eu.ctfassets.net/0vp0u5uh75zd/3wPlDC2XQOYT3XOdwCk6lz/9a9282ffd29746a7a7f6b0149509f1cf/052_Length_engaged_thread_Fastening_EN_01_2025.pdf>
11. <https://media.boellhoff.com/files/pdf1/0100-helicoil-plus-en.pdf>
12. [Part # CLS-M3-2, Self-Clinching Nuts - Types S, SS, CLS, CLSS, SP - Metric On PennEngineering (PEM)](https://catalog.pemnet.com/item/nuts-types-s-ss-cls-clss-cla-sp/self-clinching-nuts-types-s-ss-cls-clss-sp-metric/cls-m3-2)
13. [Part # S-M3-1ZI, Self-Clinching Nuts - Types S, SS, CLS, CLSS, SP - Metric On PennEngineering (PEM)](https://catalog.pemnet.com/item/nuts-types-s-ss-cls-clss-cla-sp/self-clinching-nuts-types-s-ss-cls-clss-sp-metric/s-m3-1zi)
14. [RIVKLE® blind rivet nuts and blind rivet studs | Böllhoff](https://www.boellhoff.com/de-en/products/special-fasteners/rivkle-blind-rivet-nuts-and-blind-rivet-studs/)
15. [Best Practices for Designing and Laser Cutting Small Parts](https://sendcutsend.com/blog/best-practices-for-designing-and-laser-cutting-small-parts/)
16. [Basic Tolerances and Cut Feature Relationships](https://sendcutsend.com/blog/basic-tolerances-and-cut-feature-relationships/)
17. [How to Use 5052 Aluminum in Your Laser Cutting Project |](https://sendcutsend.com/blog/how-to-use-5052-aluminum-in-your-laser-cutting-project/)
18. [Laser Cut 5052 H32 Aluminum](https://sendcutsend.com/materials/5052-aluminum/)
19. [10 Reasons Your Laser Cut File is Failing Preflight - SendCutSend](https://sendcutsend.com/blog/10-common-reasons-your-design-is-failing-sendcutsend-preflight/)
20. [Design Guidelines for Sheet Metal Fabrication](https://www.protolabs.com/services/sheet-metal-fabrication/design-guidelines/)
21. [Sheet Metal Fabrication](https://prod-www.protolabs.com/services/sheet-metal-fabrication/design-guidelines/)
22. [How Thin Can a Laser Cutter Cut? Precision Limits](https://kasulaser.com/how-small-can-a-laser-cutter-cut/)
23. [SendCutSend Education Chapter 5: From CAD to Cut - Designing for Sheet Metal](https://sendcutsend.com/blog/from-cad-to-cut-designing-for-sheet-metal/)
24. [ISO 9013:2017 - Thermal cutting — Classification of thermal cuts — Geometrical product specification and quality tolerances](https://www.iso.org/standard/60321.html)
25. [FICHE D’INSTRUCTION Identification : INS-033.1](https://www.groupe-tma.com/wp-content/uploads/2020/01/INS-033-Standards-de-Tol%C3%A9rance-FRANCAIS.pdf)
26. [ISO 9013 Thermal Cutting Dimensional Tolerances](https://www.modulusmetal.com/iso-9013-thermal-cutting-dimensional-tolerances/)
27. [Ce document présente les tolérances dimensionnelles et géométriques](https://www.groupe-tma.com/wp-content/uploads/2024/12/INS-033-Standards-de-Tolerance-FRANCAIS.pdf)
28. [Understanding Small Geometry in Laser Cutting Projects](https://sendcutsend.com/blog/understanding-small-geometry-in-laser-cutting/)
29. [What are best practices for minimum geometry?](https://sendcutsend.com/faq/what-are-best-practices-for-minimum-geometry/)
30. [Selon Norme NF EN 485-2 TÔLES EN ALUMINIUM EN AW-7075 Etat Epaisseur spécifiée](http://www.reynolds-european.fr/wp-content/uploads/2020/04/fiche-toles-alu-AW-7075.pdf)
31. [Paramètres mécaniques caractéristiques pour semi-produits en aluminium brut](https://www.metallservice.ch/msm/msm-home/services/lexique-des-m%C3%A9taux/composition-chimique-pour-semi-produits-en-aluminium-brut.pdf)
32. [Catalogue INOX-ALU](https://ecom.descours-cabaud.net/catalogue_inox-alu_2012/32/)
33. [Minimum Bend Radius Chart: Aluminum, Steel, Stainless](https://www.rivcut.com/resources/bend-radius-chart)
34. [Minimum Bend Radius for 5052 Aluminum Sheet: Spec Sheet](https://fabtekindustries.com/post-minimum-bend-radius-5052-aluminum-sheet)
35. [Minimum Bend Radius](https://www.eng-tips.com/threads/minimum-bend-radius.218133/)
36. [Bending Deformation Guidelines](https://sendcutsend.com/guidelines/bend-deformation/)
37. [How To Apply Hole Distance Specifications for Tapping, Countersinking, and Hardware Insertion](https://sendcutsend.com/blog/how-to-apply-hole-distance-specifications/)
38. [Directives de pliage](https://247tailorsteel.com/en/submission-guidelines/guidelines-for-bending)
39. [How to Prep Your File for Hardware Insertion](https://sendcutsend.com/guidelines/hardware/)
40. [How to Achieve Perfect CNC Part Design](https://www.protolabs.com/en-gb/services/cnc-machining/cnc-milling/high-speed-cnc-milling/)
41. [DFM Guidelines for CNC Machining](https://www.protolabs.com/resources/design-for-machining-toolkit/)
42. [CNC Design Guidelines: Walls, Pockets & Threads (2026)](https://www.makerstage.com/resources/cnc-design-guidelines)
43. [Design Rules for CNC Milling Parts: Your Complete Guide - Lewei Precision](https://leweiprecision.com/design-rules-for-cnc-milling-parts/)
44. [How to design parts for CNC machining](https://www.hubs.com/knowledge-base/how-design-parts-cnc-machining/)
45. [CNC Machining Tips for Complex Parts](https://www.protolabs.com/resources/design-tips/mastering-complex-features-on-machined-parts/)
46. [Tap Drill Size Chart: Metric & Imperial Thread Sizes](https://aimsindustrial.com.au/blogs/product-guides/blog-threading-tap-metric-imperial-size-chart)
47. [Helical Thread Insert (Heli-Coil Type) Dimensions and Tap Drills](https://mechcodex.com/reference/helical-insert-dimensions)
48. [Recommended Tightening Torque Table For Stainless Steel Fasteners - Accu Inc](https://accu-components.com/us/p/387-stainless-steel-fasteners-recommended-tightening-torques)
49. [CLS-M3-1 - Self-Clinching Nuts - Types S, SS, CLS, CLSS, SP - PEM® Fastening Products](https://www.pemnet.com/products/product-finder/cls-m3-1/)
50. [CLS-M3-1 PEM Self-Clinching Nut](https://www.swaco.com/CLS-M3-1-Nut-for-Sheet-Metal)
51. [Aluminium Alloy - Commercial Alloy - 6082 - T6\~T651 Sheet](https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6082-T6T651-Sheet_335.ashx)
52. [CLS-M3-2 - Self-Clinching Nuts - Types S, SS, CLS, CLSS, SP - PEM® Fastening Products](https://www.pemnet.com/eu/products/product-finder/cls-m3-2/)
53. [PEM Nuts, Standoffs & Studs for Sheet Metal Assembly](https://drametal.com/blog/hardware-insertion-pem-guide/)
54. [PEM® brand self-clinching nuts install permanently in aluminum,](https://www.pemnet.com/wp-content/uploads/sites/2/2022/06/cldata.pdf)
55. <https://media.boellhoff.com/files/pdf13/rivkle-blind-rivet-nuts-and-studs-en-2307.pdf>
56. [ISO 2768 Tolerance Calculator & Tables — General Tolerances f, m, c, v, H, K, L — CSL Industrielle Messtechnik](https://www.csl-imt.ch/en/knowledge/iso-2768-tolerance-tables/)
57. [ISO 2768 Tolerance Chart — f/m/c/v & H/K/L Lookup](https://premsaindustries.com/en/resources/iso-2768-tolerance-chart)
58. [MatWeb - Terms of Use](https://asm.matweb.com/search/terms.asp)
59. [MatWeb - The Online Materials Information Resource](https://www.matweb.com/reference/terms.aspx)
60. [Aalco Metals LTD - Aluminium Alloy 6082 T6T651 Plate - 148](https://www.scribd.com/document/812256427/Aalco-Metals-Ltd-Aluminium-Alloy-6082-T6T651-Plate-148)
61. [\[Literature Review\] MEVITA: Open-Source Bipedal Robot Assembled from E-Commerce Components via Sheet Metal Welding](https://www.themoonlight.io/en/review/mevita-open-source-bipedal-robot-assembled-from-e-commerce-components-via-sheet-metal-welding)
62. [Act/cut 3d d'Alma - L'Usine Nouvelle](https://www.industrie-techno.com/article/act-cut-3d-d-alma.16355)
63. [act/cut file extensions](https://www.file-extensions.org/act-cut-file-extensions)
64. [Sign, a software to cut out logos, pictures or characters - Almacam](https://almacam.com/products/almacam-add-ons/sign)
65. [Almacam Quote, logiciel de devis pour tôlerie et mécano- ...](https://almacam.com/software/quotation/almaquote/)
66. [Complete Sheet Metal Bending Guide](https://proleanmfg.com/blog/sheet-metal-bending-design/)
67. [Sheet Metal Design Guidelines - Budde Sheet Metal Works](https://buddesheetmetal.com/sheet-metal-design-guidelines/)
68. [Sheet Metal Design Guidelines: How to Design Good Sheet Metal Parts](https://www.smlease.com/entries/sheet-metal-design/sheetmetal-design-guidelines/)
69. [Sheet Metal Bending and Folding Guidelines](https://performaxengineering.com.au/pages/sheet-metal-folding-bending-guidelines)
70. [Minimum Flange Sizes by Metal Thickness](https://www.allmetalsfab.com/minimum-flange-sizes-by-metal-thickness/)
71. [Sheet Metal Flange Height Formula for Proper Forming (2026)](https://www.approvedsheetmetal.com/blog/use-this-flange-formula-for-sheet-metal-forming)
72. [Design Guidelines](https://sheetmetal.me/design-guidelines/)
