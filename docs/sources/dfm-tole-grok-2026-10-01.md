# YXOR — Capacités CN, DFM tôle 1–6 mm, valeurs prudentes

Consultation : 1er octobre 2026. Règle du projet : en cas de divergence publiée, retenir la valeur la plus prudente. Une valeur non trouvée s’écrit « non trouvé ». Une valeur [M] ne vaut que pour les machines de sa source.

Nature : [M] mesurée/déclarée par un fabricant sur ses machines ; [E] règle empirique ; [N] norme ; [O] déclaration de l’opérateur.

## 1. Découpe laser

### Trou minimal (diamètre)

- Règle d’atelier la plus citée : D ≥ t, souvent D ≥ 1,2 t à 1,5 t en aluminium [E]. Sources : SMS Laser (2026-05-09), Janee, Atlas, JDL (Australie).
- Microkerf, fibre, azote, aluminium [M] : 1,2 mm → 1,25 mm ; 2,0 mm → 1,5 mm ; 3,0 mm → 2,0 mm ; 4,0 mm → 2,5 mm ; 5,0 mm → 3,5 mm ; 6,0 mm → 3,0 mm (1,0 mm avec BrightLine). PDF consulté 2026-10-01. https://microkerf.com/Content/Downloads/MinimumHolesize.pdf
- Trumpf L3050 5 kW CO2, Kepser [M], acier/inox seulement, pas d’aluminium : acier 3 mm → 1,5 mm ; inox 3 mm → 1,5 mm ; inox 6 mm → 3 mm. Précision de positionnement annoncée ±0,1 mm. https://www.kepser.nl/en/knowledge-centre/laser-cutting/
- JS Precision [E], aluminium 5052/6061 : trou ≥ 1,2 t à 1,5 t ; bord ≥ 1,5 t à 2 t. Pour 3 mm : trou ≥ 4,5 mm, sinon perçage. https://www.cncprotolabs.com/blog/laser-cut-metal-parts-dfm-materials (2026-09-03)
- Amada, guide tiers [E] : plancher ~1,5 t. https://glcncmachining.com/amada-cnc-laser-cutting-guide/ (2026-09-30)
- Titane, VT Machining [M] : trou mini 1,2 t (standard) / 1,0 t (précision) ; saignée 0,1–0,3 mm ; ZAT 0,05–0,15 mm ; contour ±0,05 à ±0,10 mm. https://vtmachining.com/laser-cutting/titanium

Valeur prudente aluminium 3 mm, trou fonctionnel : 4,5 mm (1,5 t), puis alésage si plus petit. Un trou de 2 mm est annoncé faisable chez Microkerf, pas chez les règles 1,5 t.

### Pont / voile, distance trou-bord, fente

- Voile mini : 1,5 t (JDL) ; ne pas descendre sous t ou 1,0 mm (Rapid Turn) [E].
- Trou-bord : 1 t (SMS, JDL) ; 1,5 t (Dewin, JS Precision alu) ; 2 t (Rapid Turn) [E].
- Trou-trou : 1 t à 2 t selon sources [E].
- Fente : largeur ≥ t, souvent ≥ 1,5 t [E].
- Prudent alu 3 mm : voile 6 mm (2 t), trou-bord 6 mm (bord de trou à bord de pièce), trou-trou 6 mm, fente 4,5 mm.

### Saignée, ZAT, conicité, tolérance, perpendicularité

- Saignée fibre/CO2 tôle : 0,08–0,45 mm selon sources ; fourchette répétée 0,10–0,30 mm [M/E]. Kepser/Trumpf acier : 0,15 mm à 1 mm d’épaisseur, jusqu’à 0,7 mm à 25 mm. Inox : 0,2–0,3 mm.
- Conicité : 0,5° à 1,5° (JS Precision) [E] ; titane 0,2° à 0,5° (VT) [M].
- ZAT : acier 0,1–0,5 mm (RPM Fast) [E] ; titane 0,05–0,15 mm (VT) [M]. Aluminium chiffré : non trouvé dans les pages consultées.
- Tolérance contour fibre, tôle ≤ 3–6 mm : ±0,05 à ±0,15 mm selon ateliers [M]. Au-delà : ±0,15 à ±0,20 mm.
- ISO 9013:2017, laser jusqu’à 32 mm typiquement classe 1 [N]. Extrait secondaire (Modulus Metal, 2025-03-03), classe 1, épaisseur >1 à ≤3,15 mm : cote 3–10 mm ±0,15 mm ; 10–35 mm ±0,20 mm. Épaisseur >3,15 à ≤6,3 mm : ±0,20 mm sur les petites cotes. https://www.modulusmetal.com/iso-9013-thermal-cutting-dimensional-tolerances/
- Perpendicularité u classe 1 : souvent citée ≤ 0,1 mm (MechDatum, synthèse, à vérifier sur le PDF payant).

### Jet d’eau et plasma

- Jet d’eau abrasif [M/E], AquaJet : saignée courante 0,76–1,27 mm (0,030–0,050 in), possible ~0,5 mm ; tolérance économique ±0,38 mm, avec compensation de dépouille plutôt ±0,25 mm ; trou mini en tôle mince ~1,5 mm, en fort épaisseur ~0,2 t. Pas de ZAT. https://www.aquajetservices.com/a-technical-guide-to-waterjet-cutting/characteristics-of-waterjet-cutting/
- Plasma HD : tolérance typique ±0,5 à ±1,0 mm ; saignée 1,5–4 mm ; ZAT présente. Machinery’s Handbook 31, synthèse : plasma tôle mince ±0,25 mm, saignée mini ~0,5 mm. Moins adapté au robot 1–6 mm que le laser.

## 2. Pliage

- EN AW-5754-O / H111, reproduction de l’EN 485-2 (The World Material, 2026-09-29) [N secondaire] : 1,5–3 mm, rayon 180° = 1,0 t et 90° = 1,0 t ; 3–6 mm, 1,0 t / 1,0 t ; Rp0,2 ≥ 80 MPa ; A50 ≥ 16 % (1,5–3 mm) et ≥ 18 % (3–6 mm). https://www.theworldmaterial.com/5754-aluminum-alloy/
- 5052-H32 : 0,5 t à 1 t (idéambox, CIFProto) jusqu’à 1 t–2 t vers 3 mm et 2,5 t à 6,4 mm (Huaxiao, 2026-09-27) [E]. RivCut : à 0,125 in (~3,2 mm), 1,5 t dans le sens du laminage, 1 t en travers.
- 6061-T6 : 2 t à 6 t selon épaisseur ; à ~3 mm, 3 t à 4 t, pire dans le sens du grain [E]. CIFProto recommande 4 t. Ne pas plier serré en T6.
- 6082 : 2 t à 3 t (Bolton Sheetmetal) [E].
- Inox 304 : 1 t à 2 t ; 316 : jusqu’à 2 t [E].
- Laiton C260 : 1 t à 1,5 t [E]. Titane grade 2/5, rayon mini chiffré par épaisseur : non trouvé.
- Longueur mini de bord : 4 t (Protolabs) ; 4 t + R (idéambox) ; tables air-bend ~6 t (Huaxiao, 3 mm → bride 18 mm) [M/E].
- Trou à pli (bord de trou à tangente) : 2,5 t + R (Xometry Design Guide v2.2 ; idéambox) ; 1,5 t + R (Bolton) [E]. Prudent : 2,5 t + R.
- Dégagement d’angle : encoche ≥ t en largeur et en profondeur [E].
- K : 0,33 (pli serré) à 0,46 (grand R) ; défaut atelier souvent 0,40–0,42 en aluminium [E]. BA = (π/180) × angle × (R + K t).
- Retour élastique 90° [E], TestTalkHQ 2026-06-17 : 5052 3–6° ; 6061 8–15°. À mesurer sur coupon.
- Sens de laminage : plier en travers du grain. Dans le sens du grain, majorer le rayon (RivCut : 6061-T6 0,125 in, 6 t avec grain contre 3–4 t en travers).

## 3. Fraisage 3 et 5 axes, petites pièces aluminium

- Rayon d’angle intérieur = rayon d’outil. Outil Ø6 → R3 ; Ø3 → R1,5. Recommandation : R ≥ 1/3 de la profondeur de poche (RivCut) [E].
- Paroi mini aluminium : 0,5 mm possible, 1 mm recommandé (RivCut) ; Protolabs recommande > 0,51 mm et épaisseur nominale > 1,02 mm [M].
- Profondeur de poche : ≤ 4 × largeur [E] ; Protolabs profondeur max usine 50,8 mm par face [M].
- Tolérance standard : ±0,13 mm (Protolabs usine auto) ou ISO 2768-1 f/m [M].
- Alésage logement roulement : H7 est un ajustement d’alésage [N, ISO 286-2], pas une capacité laser. Sur aluminium, un H7 acier peut serrer l’extérieur du roulement (dilatation et module). SKF : logement tournant extérieur souvent plus serré (J7/K7) ; logement fixe souvent H7. À valider au catalogue du roulement. Valeurs H7 chiffrées par diamètre : non extraites du PDF ISO dans cette recherche.
- Taraudage : M2 à M12 chez Protolabs [M]. Engagement aluminium 1,5 d à 2 d (Ekinsun) ; 1,5 d à 3 d (RivCut) [E]. Perçage taraud : M2 1,6 ; M2,5 2,05 ; M3 2,5 ; M4 3,3 ; M5 4,2 ; M6 5,0 mm (~75 % de filet). Insert hélicoïdal, perçage alu (table Heli-Coil) : M2 2,1 ; M3 3,15 ; M4 4,2 ; M5 5,2 ; M6 6,25 mm.

## 4. Quincaillerie

ISO 273, séries fine / moyenne / large [N], reprises EBD et Ekinsun :

- M2 : 2,2 / 2,4 / 2,6 mm
- M2,5 : 2,7 / 2,9 / 3,1 mm
- M3 : 3,2 / 3,4 / 3,6 mm
- M4 : 4,3 / 4,5 / 4,8 mm
- M5 : 5,3 / 5,5 / 5,8 mm
- M6 : 6,4 / 6,6 / 7,0 mm

Série moyenne par défaut. Équivalents ASME B18.2.8 et JIS B 1001 : non extraits.

Couples indicatifs, T = K F d, précharge 75 % de la charge d’épreuve, acier ISO 898-1 [E], CheckedCalc 2026-09-23, K = 0,20 :

- M3 8.8 : 1,31 N·m ; 12.9 : 2,20 N·m
- M4 8.8 : 3,05 N·m ; 12.9 : 5,11 N·m
- M5 8.8 : 6,17 N·m ; 12.9 : 10,3 N·m
- M6 8.8 : 10,5 N·m ; 12.9 : 17,6 N·m

A2-70, MetricMech, K sec ~0,20, à partir de M5 seulement : M5 3,6 N·m ; M6 6,1 N·m. M2–M4 A2/A4 : non trouvé. Inox sur inox : grippage, K peut dépasser 0,30 ; anti-seize recommandé.

Écrous à sertir (PEM, bulletin, et synthèse DFW 2026-03-23) : S-M3 et S-M4 épaisseur mini ~1,0 mm ; S-M5 ~1,2 mm ; S-M6 ~1,6 mm. Trou ≠ trou de passage : pour certains S/BS métriques, ordre de 4,2–6,4 mm selon type (catalogue PEM). Distance centre-bord : colonne catalogue, souvent ~2 × diamètre de corps en règle d’atelier. Sertir avant peinture. Dureté de la tôle inférieure à celle de l’insert.

Écrous à riveter : Böllhoff RIVKLE rond standard, trou M3 = 5,0 ; M4 = 6,0 ; M5 = 7,0 ; M6 = 9,0 mm. Grip selon variante ; M3 souvent dès 0,5 mm (Rivetfix). Distance au bord chiffrée Böllhoff : non trouvé. Règle d’atelier ≥ 2 × diamètre de trou.

Goupilles : ajustement ISO 2338 m6 dans H7 pour goupille de positionnement. Diamètres mini laser incompatibles : percer/aléser après découpe.

Roulements miniatures (608, 6000) : arbre souvent k5/j6 ; logement acier H7 ou J7. Dans l’aluminium, ne pas recopier l’ajustement acier. Freinage : frein-filet faible (démontable) ou moyen ; Nylstop ; rondelle grower peu fiable en aluminium tendre. Couple de frein-filet chiffré : non trouvé.

## 5. Tolérances générales

- ISO 2768-1:1989 : toujours publiée, confirmée 2022. Prix ISO : 43 CHF. Aperçu en ligne. Révision en préparation (ISO/TC 213) ; édition 2 signalée en pré-publication en juin 2026 par des synthèses, pas encore substituée au 1er octobre 2026 sur la fiche consultée.
- ISO 2768-2:1989 : retirée, remplacée par ISO 22081:2021 (pas de tableau H/K/L de remplacement). Un cartouche « ISO 2768-mK » sur un plan neuf est ambigu.
- ISO 9013:2017 : confirmée 2022, 31 pages, 159 CHF ; amendement 1:2024, 18 CHF. Échantillon en ligne. Laser 0,5–32 mm.
- JIS B 0405 : tableaux linéaires alignés sur ISO 2768-1 (reprise Apporo). Prix JIS : non trouvé.
- GB/T 1804-2000 : déclaré identique à ISO 2768-1 pour f/m/c/v (Hansheng). Prix : non trouvé.
- ASME Y14.5-2018 : tolérancement géométrique, pas un tableau de cotes libres équivalent. Prix ASME : non trouvé dans cette recherche.

Classe m, ISO 2768-1, cotes linéaires [N], reprise Apporo/Hansheng : 0,5–3 mm ±0,1 ; 3–6 ±0,1 ; 6–30 ±0,2 ; 30–120 ±0,3 ; 120–400 ±0,5. Angles, classe m, côté court 0–10 mm : ±1°. Chanfreins 0,5–3 mm, classe m : ±0,2 mm.

## 6. Matières (sources gratuites)

- 5052-H32, fiche Aerospace Metals citant l’Aluminum Association, « NOT FOR DESIGN » : densité 2,68 g/cm³ ; Rm 228 MPa ; Rp0,2 193 MPa ; A 12 % à 1,6 mm ; E 70,3 GPa. https://www.aerospacemetals.com/wp-content/uploads/2023/06/Aluminum-5052-H32.pdf
- 6061-T6 : Engineering ToolBox 35 ksi / 42 ksi (241 / 290 MPa), E 10×10^6 psi. Huaxiao : Rm 310 MPa, Rp0,2 276 MPa, A 8–12 %. Divergence : retenir 276 / 310 seulement comme ordre de grandeur, et la fiche AA du lot.
- 5754-O/H111, EN 485-2 secondaire : Rm 190–240 MPa, Rp0,2 ≥ 80 MPa, A50 ≥ 16–18 % entre 1,5 et 6 mm.
- 6082, 5083, 7075, valeurs de lot : non trouvé dans les pages extraites (7075-T6 se plie mal ; à usiner).
- Inox 304, fiche Weerg 2024 : densité 8 g/cm³ ; Rm 520 MPa ; Rp0,2 185 MPa ; A 35 % ; E 200 GPa. Conditions : chaque utilisateur revérifie. 316 : non trouvé ici.
- Titane, VT (valeurs type grade 5) : densité 4,43 g/cm³ ; Rm 950 MPa ; Rp0,2 880 MPa. Grade 2 chiffré : non trouvé.
- Laiton : non trouvé dans les fiches extraites.
- Réutilisation : données AA souvent « not for design » / pas une licence de reproduction. MatWeb et MakeItFrom : agrégats, conditions à lire avant copie. Ne pas recopier un PDF de norme.

## 7. Sources de pratiques et robots ouverts

Ateliers en ligne : Xometry (guide tôle v2.2), Protolabs, SendCutSend (rayon et K imposés par épaisseur), JS Precision, JDL (Australie), Kepser (NL, Trumpf). Constructeurs : Alma act/cut (France) importe DXF, IGES, DWG, DSTV, STEP. Trumpf/Bystronic/Amada : peu de tableaux publics complets ; les chiffres [M] viennent surtout des sous-traitants. Quincaillerie : PEM, Böllhoff. CAO ouverte : bibliothèques PEM, Misumi, TraceParts, McMaster (compte), Onshape public. Robots : Poppy/Koalby = résine imprimée ; AGILOped = profilés alu + pièces imprimées ; OpenCrane = profilés 6063-T5. Bipède open source documentant des choix de tôle laser 1–6 mm : non trouvé.

## Registre des sources

- Alma act/cut, France, brochure gratuite, pas de licence de données chiffrées, 2023–2024, fiabilité haute sur les formats.
- Microkerf, minimum holes PDF, gratuit, [M], fiabilité haute pour leurs machines seulement.
- Kepser / Trumpf L3050, Pays-Bas, page gratuite, [M], pas d’aluminium, fiabilité moyenne (tableau ancien CO2).
- Xometry, Protolabs, SendCutSend, États-Unis, guides gratuits, [M/E], fiabilité haute pour leurs procédés.
- ISO 2768-1, internationale, 43 CHF, aperçu gratuit, [N], fiabilité haute.
- ISO 9013:2017, 159 CHF + Amd 18 CHF, aperçu gratuit, [N], fiabilité haute.
- PEM bulletin, États-Unis, PDF gratuit, [M], fiabilité haute pour la quincaillerie PEM.
- Böllhoff, Allemagne, page gratuite, [M], fiabilité haute pour RIVKLE.
- Aerospace Metals / AA, « not for design », gratuit, fiabilité moyenne pour le calcul.
- The World Material, reproduction EN 485-2, gratuit, fiabilité moyenne (secondaire).
- Weerg, Italie, fiche 304, 2024, conditions d’usage à relire, fiabilité moyenne.

## Croisement opérateur

- Rayon intérieur laser 2 mm [O] : prudent et cohérent avec une machine ancienne ou une règle d’atelier. Étonnant face au fibre moderne (Microkerf alu 3 mm : trou 2 mm, donc rayon de contour plus petit).
- « Diamètre de faisceau 2 mm » [O] : incohérent avec une saignée de 0,5 mm et avec un spot fibre (0,05–0,2 mm). Probable confusion avec le diamètre de buse (souvent 1–2,5 mm).
- Saignée 0,5 mm compensée par lui [O] : haute mais dans la fourchette haute publiée (jusqu’à 0,45–0,7 mm). Cohérent avec CO2 ou forte épaisseur, pessimiste pour fibre 3 mm (0,15–0,30 mm).
- Contour ±0,5 mm [O] : cohérent comme garantie, incohérent comme capacité typique (fibre ±0,1 mm ; ISO 9013 classe 1 ~±0,2 mm à 3 mm). À prendre comme capacité contractuelle.
- Épaisseurs 1–6 mm et « 1–10 mm » [O] : cohérent fibre alu jusqu’à ~10 mm (guide Amada tiers).
- Pliage, rayon intérieur mini 5 mm toutes matières [O] : cohérent pour 5052/5754 vers 3 mm (1 t à 2 t). Insuffisant / incohérent pour 6061-T6, 6082-T6, 7075-T6 à 3 mm (souvent 3 t à 6 t, soit 9–18 mm).
- Écart 10 mm entre pièces, tôle ≥ 2 m [O] : prudent et cohérent (lit 3000 mm courant ; écart de nesting souvent 3–10 mm).
- Alésage après découpe [O] : cohérent et recommandé pour H7 et trous < 1 t.
- « 5 axes possibles » [O] : non identifiable (tête laser biseau ou fraiseuse).
- Formats DXF, SVG [O] : DXF cohérent avec Alma. SVG rarement natif act/cut dans les brochures (DXF, IGES, DWG, DSTV, STEP). « dpr » : non trouvé dans les brochures Alma consultées.
- Céramique [O] : étonnant sur un laser métal fibre/CO2 d’atelier tôlerie. À confirmer (procédé, épaisseur, usage structurel ou non).

## Questions à l’opérateur

1. Fibre ou CO2, puissance, marque, année, et le « 2 mm » est-il le spot, la buse ou le rayon mini qu’il accepte ?
2. Saignée réelle mesurée sur aluminium 3 mm, azote, et qui compense : lui dans Actcut, ou faut-il offsetter le DXF ?
3. Le ±0,5 mm est-il la garantie ou la capacité ? Peut-il tenir ±0,2 mm sur un contour < 100 mm ?
4. Le 5 axes est-il une fraiseuse, une tête laser biseau, ou les deux ? Courses et reprise d’alésage H7 possibles ?
5. Quels alliages et états exactement (5052-H32, 5754-H111, 6061-T6) et le rayon 5 mm vaut-il pour le T6 ?
6. Longueur mini de bride sur sa presse, ouverture de vé, et K qu’il utilise à 3 mm.
7. Que signifie « dpr » (extension, logiciel, exemple de fichier) ? Accepte-t-il un DXF R12, contours fermés, mm, sans cote ?
8. Découpe-t-il vraiment titane grade 2/5 et céramique, et à quelle épaisseur ?
9. Écart de 10 mm : imposé par les ventouses, par le squelette, ou négociable ?
10. Peut-il sertir des écrous PEM/RIVKLE, et sur quelle épaisseur mini ?