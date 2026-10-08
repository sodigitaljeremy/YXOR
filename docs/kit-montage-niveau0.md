# YXOR Kit, niveau 0 : notice de montage

**Engendrée** par `.venv/bin/python parts/kit_niveau0.py` : ne pas éditer à la main. Planches : `exports/parts/kit_niveau0_planchesA4.pdf` (hors de Git, règle 4 ; régénérées par `scripts/regenerer.py`).

Décidé (fiche 0075, Jeremy, 2026-10-08) : assemblage B — tenons et mortaises, colle non porteuse seulement, pivots par vis traversante. Carton dessiné : ondulé double de 3,5 mm (la valeur mesurée ; consigne du prompt, pas un choix écrit par Jeremy). Toutes les cotes de dessin non anthropométriques sont des hypothèses PROPOSÉES (`params/kit.yaml`, `niveau0`).

## Ce que donnent les plans

- **111 gabarits, 178 pièces à découper** (les pièces d'un bras ou d'une jambe se coupent deux fois : la seconde, gabarit retourné), plus **44 cales** (rondelles de carton de 16 mm), sur **40 feuilles A4**, dont des grandes pièces en tuiles (K52 tronc.flanc+ : 1 × 2 feuilles; K53 tronc.flanc- : 1 × 2 feuilles; K54 tronc.face+ : 1 × 2 feuilles; K55 tronc.face- : 1 × 2 feuilles).
- **Carton : 0,78 m²**, soit **505 g** à 649 g/m² (masse surfacique mesurée), sans les chutes.
- **Hauteur du Kit : 0,938 m**, contre 0,715 m pour le Lab de référence (taille du Kit GELÉE en attendant Jeremy : avec les Feetech aux petits axes, fiche 0075, le Lab passe à 0,850 m ; `params/kit.yaml`, `kit_taille`). Les longueurs entre axes sont celles du Lab de référence ; l'écart vient des logements de servo en carton (tableau ci-dessous).
- **Contrôles** : aucune faute de dessin (rayons rentrants ≥ 1,75 mm, aucun angle rentrant vif, chaque pièce d'un seul tenant) ; aucune interpénétration en 3D, servos du niveau 1 et 3 compris (un tenon sans sa mortaise, ou un servo qui ne passerait pas, se verrait).

## Hauteurs (axes au repos, debout)

| Repère | Kit (mm) | Commentaire |
| --- | ---: | --- |
| cheville | 56 | ANSUR 26 : le bas du tibia doit passer au-dessus du pied |
| genou | 203 | cheville + tibia (Lab) |
| hanche, tangage | 364 | genou + cuisse (Lab) |
| hanche, roulis | 417 | trois axes de hanche empilés (chez l'humain, ils se croisent) |
| dessous du bassin | 447 | servo de lacet de hanche |
| épaule | 763 | tronc du Lab, rallongé pour l'électronique |
| cou, tangage | 816 | |
| sommet | 938 | |

Écart de largeur : le bassin fait 179 mm (ANSUR 132), pour loger les deux servos de lacet sous les hanches, à l'écartement ANSUR.

## Ce qu'il faut savoir avant de couper

1. **Imprimer à 100 %**, sans « ajuster à la page ». Mesurer le réglet de 100 mm de chaque feuille : s'il ne fait pas exactement 100 mm, réimprimer.
2. **Reporter** : coller la feuille sur le carton (colle en bâton, ou scotch de peintre aux coins), en alignant la **flèche grise** sur le sens des **cannelures** (les petites arches visibles sur la tranche). Une pièce coupée à 90° de la flèche plie deux à trois fois plus facilement.
3. **Couper** au cutter, sur une planche ou un carton martyr, contre la règle, en deux ou trois passes légères plutôt qu'une forte. Les **mortaises** (fentes de la largeur du carton) : deux traits longs, puis les bouts. Les **petits ronds** aux coins des fentes et des fenêtres (les « os de chien ») laissent entrer un tenon carré jusqu'au fond : un coup de pointe de cutter suffit.
4. **Trous de pivot** (Ø 4,5 mm) : percer au poinçon ou à la pointe d'un tournevis, puis agrandir en vissant la vis M4 à travers.
5. **Grandes pièces** (tronc) : imprimées en plusieurs feuilles qui se recouvrent de 10 mm ; poser les croix grises les unes sur les autres, scotcher, puis reporter comme une seule feuille.
6. **Côté droit** : les pièces des bras et des jambes se coupent deux fois ; pour la seconde, retourner le gabarit (le carton n'a pas d'endroit).

## Montage d'un caisson (toutes les boîtes se montent pareil)

1. Poser un **flanc** à plat.
2. Enfoncer les **tenons** des deux **faces** dans les mortaises du flanc, faces debout.
3. Glisser les **cloisons** et les **plaques à fenêtre** (s'il y en a) : leurs tenons entrent dans les faces et les flancs.
4. Poser le second flanc par-dessus : tous les tenons dans ses mortaises.
5. Poser les **couvercles** sur les bouts : les tenons des flancs et des faces les traversent.
6. **Colle (non porteuse)** : un point de colle chaude sur un tenon qui dépasse, pour qu'il ne ressorte pas. Jamais entre deux pièces qui portent un effort, jamais sur un bouchon ni une plaque de serrage (ils s'enlèvent au niveau 1).

## Logements de servo : ce qui se pose au niveau 0

Chaque logement est une **fenêtre** dans une paroi, à la taille du servo STS3215 (45,23 × 24,73 mm, plus 1,0 mm de jeu), et une **plaque à fenêtre** intérieure qui tiendra le servo à mi-hauteur. Au niveau 0 :
- le **bouchon** (pièce à la taille de la fenêtre, percée sur l'axe) ferme la fenêtre ;
- la **plaque de serrage** (un peu plus grande) se pose derrière, à l'intérieur ;
- la vis du pivot traverse : oreille ou couvercle de l'enfant, deux **cales** (rondelles de carton), bouchon, plaque de serrage ; écrou à frein derrière.
Au niveau 1 (ou 3), on retire la vis, le bouchon et la plaque de serrage, on glisse le servo par la fenêtre, sa sortie à l'emplacement du trou : **rien n'est redécoupé**. Les trous du palonnier se percent alors dans l'oreille, d'après le palonnier livré (non coté par Feetech).

## Pivots

| Articulation | Sorte | Parent → enfant | Nombre | Vis côté servo | Vis côté opposé | Cales côté opposé |
| --- | --- | --- | ---: | --- | --- | --- |
| hip_yaw | plateau (servo au niveau 3) | bassin → hanche1 | 2 | M4×25 | — | 0 cale(s) de carton + 0,0 mm en rondelles |
| hip_roll | chape (servo au niveau 3) | hanche1 → hanche2 | 2 | M4×25 | M4×25 | 1 cale(s) de carton + 2,6 mm en rondelles |
| hip_pitch | chape (servo au niveau 3) | hanche2 → cuisse | 2 | M4×25 | M4×16 | 0 cale(s) de carton + 1,0 mm en rondelles |
| knee | chape (servo au niveau 3) | tibia → cuisse | 2 | M4×25 | M4×20 | 1 cale(s) de carton + 1,0 mm en rondelles |
| ankle_pitch | chape (servo au niveau 3) | tibia → pied | 2 | M4×25 | M4×16 | 0 cale(s) de carton + 1,0 mm en rondelles |
| waist_yaw | plateau (servo au niveau 3) | bassin → tronc | 1 | M4×25 | — | 0 cale(s) de carton + 0,0 mm en rondelles |
| shoulder_pitch | plateau (servo au niveau 1) | tronc → epaule | 2 | M4×25 | — | 0 cale(s) de carton + 0,0 mm en rondelles |
| shoulder_roll | chape (servo au niveau 1) | epaule → bras | 2 | M4×25 | M4×16 | 0 cale(s) de carton + 1,0 mm en rondelles |
| elbow_roll | chape (servo au niveau 1) | bras → avant_bras | 2 | M4×25 | M4×16 | 0 cale(s) de carton + 1,0 mm en rondelles |
| neck_yaw | plateau (servo au niveau 1) | tronc → cou | 1 | M4×25 | — | 0 cale(s) de carton + 0,0 mm en rondelles |
| neck_pitch | chape (servo au niveau 1) | cou → tete | 1 | M4×25 | M4×25 | 2 cale(s) de carton + 3,0 mm en rondelles |
| wrist_roll | plateau passif | avant_bras → poignet | 2 | M4×16 | — | 0 cale(s) de carton + 0,0 mm en rondelles |
| wrist_pitch | chape passive | poignet → main | 2 | M4×16 | M4×16 | 0 cale(s) de carton + 1,0 mm en rondelles |

## Ce qu'il faut réunir pour le niveau 0

- carton ondulé **double cannelure** de 3,5 mm (cartons de déménagement de récupération) : **1,2 m²** au moins (0,78 m² de pièces × 1,5 pour les chutes, PROPOSÉ), plats, secs, sans pli marqué ;
- **38 vis M4** à tête, 14 × 16 mm, 2 × 20 mm, 22 × 25 mm ; **38 écrous M4 à frein** (nylstop) ; **76 rondelles larges M4** ;
- **40 feuilles A4** imprimées à 100 %, colle en bâton ou scotch de peintre pour les poser sur le carton ;
- outils (décidés, fiche 0074) : **cutter** (lames neuves), **règle métallique**, **équerre**, **pistolet à colle** (colle non porteuse seulement) ; un **carton martyr** ou une planche sous la coupe ; un **tournevis cruciforme** ou un poinçon pour amorcer les trous Ø 4,5 ; un tournevis ou une clé pour les vis M4.

« Plateau » : l'enfant est vissé par un couvercle sur la sortie du servo (un seul pivot) ; « chape » : les oreilles de l'enfant encadrent le parent, un pivot de chaque côté, sur le même axe. Le débattement libre garanti par le dessin est de ±15° autour de la pose debout (PROPOSÉ) ; au-delà, à essayer.

## Ordre de montage du robot

1. **Jambes** (×2) : pied, tibia (avec ses deux bouchons), cuisse ; pivots de cheville et de genou.
2. **Hanches** (×2) : noix 2 sur la cuisse (tangage), noix 1 dans les oreilles de la noix 2 (roulis).
3. **Bassin** : visser chaque noix 1 sous le couvercle bas (lacets de hanche).
4. **Tronc** sur le couvercle haut du bassin (lacet de taille).
5. **Épaules** (×2) sur les flancs du tronc, puis **bras**, **avant-bras**, **poignet**, **main**.
6. **Cou** sur le couvercle haut du tronc, puis **tête**.

## Pièces par caisson

| Caisson | Pièces (identifiant, nom, nombre à couper, dimensions en mm) |
| --- | --- |
| pied | K01 flanc+ ×2 (81 × 100) ; K02 flanc- ×2 (81 × 100) ; K03 face+ ×2 (30 × 59) ; K04 face- ×2 (30 × 59) ; K05 cloison1 ×2 (59 × 93) ; K06 couvercle_bas ×2 (73 × 114) |
| tibia | K07 flanc+ ×2 (183 × 54) ; K08 flanc- ×2 (183 × 54) ; K09 face+ ×2 (183 × 44) ; K10 face- ×2 (183 × 44) ; K11 knee.plaque ×2 (72 × 47) ; K12 ankle_pitch.plaque ×2 (72 × 47) ; K13 knee.bouchon ×2 (46 × 26) ; K14 knee.serrage ×2 (58 × 38) ; K15 ankle_pitch.bouchon ×2 (46 × 26) ; K16 ankle_pitch.serrage ×2 (58 × 38) |
| cuisse | K17 flanc+ ×2 (215 × 54) ; K18 flanc- ×2 (215 × 54) ; K19 face+ ×2 (102 × 62) ; K20 face- ×2 (102 × 62) ; K21 cloison1 ×2 (62 × 47) ; K22 cloison2 ×2 (62 × 47) |
| hanche2 | K23 flanc+ ×2 (92 × 51) ; K24 flanc- ×2 (92 × 51) ; K25 face+ ×2 (40 × 67) ; K26 face- ×2 (40 × 67) ; K27 hip_pitch.plaque ×2 (40 × 67) ; K28 hip_pitch.bouchon ×2 (26 × 46) ; K29 hip_pitch.serrage ×2 (38 × 58) |
| hanche1 | K30 flanc+ ×2 (43 × 51) ; K31 flanc- ×2 (43 × 51) ; K32 face+ ×2 (43 × 67) ; K33 face- ×2 (43 × 67) ; K34 hip_roll.plaque ×2 (40 × 67) ; K35 couvercle_bas ×2 (81 × 65) ; K36 hip_roll.bouchon ×2 (26 × 46) ; K37 hip_roll.serrage ×2 (38 × 58) |
| bassin | K38 flanc+ ×1 (61 × 74) ; K39 flanc- ×1 (61 × 74) ; K40 face+ ×1 (61 × 179) ; K41 face- ×1 (61 × 179) ; K42 plaque_logement_bas ×1 (179 × 67) ; K43 plaque_logement_haut ×1 (179 × 67) ; K44 couvercle_bas ×1 (193 × 88) ; K45 couvercle_haut ×1 (193 × 88) ; K46 hip_yaw.bouchon ×1 (26 × 46) ; K47 hip_yaw.serrage ×1 (38 × 58) ; K48 hip_yaw_droit.bouchon ×1 (26 × 46) ; K49 hip_yaw_droit.serrage ×1 (38 × 58) ; K50 waist_yaw.bouchon ×1 (26 × 46) ; K51 waist_yaw.serrage ×1 (38 × 58) |
| tronc | K52 flanc+ ×1 (270 × 96) ; K53 flanc- ×1 (270 × 96) ; K54 face+ ×1 (270 × 151) ; K55 face- ×1 (270 × 151) ; K56 cloison1 ×1 (151 × 89) ; K57 plaque_logement_haut ×1 (69 × 89) ; K58 shoulder_pitch.plaque ×1 (52 × 89) ; K59 shoulder_pitch_droit.plaque ×1 (52 × 89) ; K60 couvercle_bas ×1 (165 × 110) ; K61 couvercle_haut ×1 (165 × 110) ; K62 shoulder_pitch.bouchon ×1 (26 × 46) ; K63 shoulder_pitch.serrage ×1 (38 × 58) ; K64 shoulder_pitch_droit.bouchon ×1 (26 × 46) ; K65 shoulder_pitch_droit.serrage ×1 (38 × 58) ; K66 neck_yaw.bouchon ×1 (26 × 46) ; K67 neck_yaw.serrage ×1 (38 × 58) |
| cou | K68 flanc+ ×1 (43 × 74) ; K69 flanc- ×1 (43 × 74) ; K70 face+ ×1 (43 × 44) ; K71 face- ×1 (43 × 44) ; K72 neck_pitch.plaque ×1 (40 × 67) ; K73 couvercle_bas ×1 (58 × 88) ; K74 neck_pitch.bouchon ×1 (26 × 46) ; K75 neck_pitch.serrage ×1 (38 × 58) |
| tete | K76 flanc+ ×1 (151 × 76) ; K77 flanc- ×1 (151 × 76) ; K78 face+ ×1 (88 × 68) ; K79 face- ×1 (88 × 68) ; K80 cloison1 ×1 (68 × 69) ; K81 couvercle_haut ×1 (82 × 90) |
| epaule | K82 flanc+ ×2 (64 × 51) ; K83 flanc- ×2 (64 × 51) ; K84 face+ ×2 (64 × 47) ; K85 face- ×2 (64 × 47) ; K86 shoulder_roll.plaque ×2 (60 × 47) ; K87 couvercle_bas ×2 (61 × 65) ; K88 shoulder_roll.bouchon ×2 (46 × 26) ; K89 shoulder_roll.serrage ×2 (58 × 38) |
| bras | K90 flanc+ ×2 (167 × 51) ; K91 flanc- ×2 (167 × 51) ; K92 face+ ×2 (105 × 62) ; K93 face- ×2 (105 × 62) ; K94 elbow_roll.plaque ×2 (72 × 62) ; K95 elbow_roll.bouchon ×2 (46 × 26) ; K96 elbow_roll.serrage ×2 (58 × 38) |
| avant_bras | K97 flanc+ ×2 (99 × 51) ; K98 flanc- ×2 (99 × 51) ; K99 face+ ×2 (47 × 62) ; K100 face- ×2 (47 × 62) ; K101 couvercle_haut ×2 (76 × 65) |
| poignet | K102 flanc+ ×2 (44 × 40) ; K103 flanc- ×2 (44 × 40) ; K104 face+ ×2 (44 × 40) ; K105 face- ×2 (44 × 40) ; K106 couvercle_bas ×2 (54 × 54) |
| main | K107 flanc+ ×2 (94 × 49) ; K108 flanc- ×2 (94 × 49) ; K109 face+ ×2 (49 × 49) ; K110 face- ×2 (49 × 49) ; K111 couvercle_haut ×2 (63 × 63) |
