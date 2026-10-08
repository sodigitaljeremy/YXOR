# YXOR Kit : modules, masses, couples et réutilisation (2026-10)

**Engendré** par `.venv/bin/python scripts/kit.py --ecrire`. Ne pas éditer à la main. DÉCIDÉ (fiche 0074, Jeremy, 2026-10-08) : modules successifs, mêmes dimensions, taille et composants que le Lab, carton, outils du ménage. **PROPOSÉ** : les niveaux (`params/capacites.yaml`, `profils.kit.modules`) et les hypothèses (`params/kit.yaml`). Rien n'est choisi ni acheté (fiche 0066).

**Taille du Kit : GELÉE** (meilleure solution du Lab AVANT la fiche 0075 (explorateur du 2026-10-08, petits axes Dynamixel) : 0,65 → 0,715 m, 13,6 kg) : jambe à H = 0,65 m, hauteur réelle 0,715 m. **Le Lab d'aujourd'hui** (docs/explorateur-lab-2026-10.md, § 12S, 250 Hz, coupure 3,0 V, chaîne compacte, ensemble 27 (après la fiche 0075)) : 0,850 m, 18,5 kg, petits axes en feetech : la contrainte Feetech (fiche 0075) l'a fait grandir ; le Kit le suivra-t-il ? Question à Jeremy (`params/kit.yaml`, `kit_taille`). Marge 1,5 sur le couple (fiche 0051).

## Structure en carton

Carton de référence : **carton_ondule_double**, 649 g/m², 3,5 mm (mesuré (params/mesures.yaml)). Coques fermées par segment ; section des segments à servo ≥ 45,2 mm (plus grand servo Feetech) + deux parois ; × 1,5 pour les renforts.

| Segment | Nombre | Section (mm) | Longueur (mm) | Aire (dm²) | Masse unitaire (g) |
| --- | ---: | --- | ---: | ---: | ---: |
| bassin | 1 | 52 × 132 | 26 | 2,35 | 23 |
| tronc | 1 | 96 × 121 | 263 | 13,72 | 134 |
| cuisse | 2 | 52 × 52 | 161 | 3,91 | 38 |
| tibia | 2 | 52 × 52 | 147 | 3,62 | 35 |
| pied | 2 | 100 × 38 | 13 | 1,11 | 11 |
| bras | 2 | 52 × 52 | 124 | 3,14 | 31 |
| avant_bras | 2 | 52 × 52 | 98 | 2,60 | 25 |
| main | 2 | 19 × 11 | 72 | 0,47 | 5 |
| tete | 1 | 76 × 68 | 84 | 3,46 | 34 |

**Structure : 480 g.** Selon le carton (même géométrie) :

| Carton | Masse surfacique (g/m²) | Épaisseur (mm) | Structure (g) | Source |
| --- | ---: | ---: | ---: | --- |
| carton_ondule_double | 649 | 3,5 | 480 | mesuré (params/mesures.yaml) |
| kapa_line_3mm_modulor | 506 | 3,0 | 369 | marché (plume) |
| kapa_line_5mm_modulor | 582 | 5,0 | 446 | marché (plume) |
| kapa_line_10mm_modulor | 798 | 10,0 | 689 | marché (plume) |
| kapa_line_5mm_boesner | 582 | 5,0 | 446 | marché (plume) |
| ondule_b_simple_face_rouleau_udobaer | 157 | 2,1 | 112 | marché (ondule_simple) |
| claycote_b_kraft_bd | 405 | 3,0 | 295 | marché (ondule_simple) |
| claycote_c_bd | 415 | 3,3 | 305 | marché (ondule_simple) |
| claycote_e_blanc_bd | 476 | 1,5 | 334 | marché (ondule_simple) |
| claycote_eb_twin_bd | 826 | 4,5 | 625 | marché (ondule_double) |
| graukarton_1mm_modulor | 700 | 1,0 | 485 | marché (gris_compact) |
| graukarton_2mm_modulor | 1 150 | 2,0 | 817 | marché (gris_compact) |
| graukarton_3mm_modulor | 1 830 | 3,0 | 1 334 | marché (gris_compact) |
| callos_buchbinder_2mm_boesner | 1 320 | 2,0 | 938 | marché (gris_compact) |
| callos_buchbinder_3mm_boesner | 1 890 | 3,0 | 1 378 | marché (gris_compact) |
| graupappe_gpf_europapier | 1 800 | 2,2 | 1 287 | marché (gris_compact) |
| pp_alveolaire_3mm_modulor | 450 | 3,0 | 328 | marché (autre) |
| siebdruckkarton_finnboard_2mm_modulor | 1 020 | 2,0 | 725 | marché (autre) |

## Classement des cartons (critères PROPOSÉS, `params/kit.yaml`)

Aire de carton du Kit, renforts compris : 0,74 m². Éliminatoires : filière papier mono-matière ; un panneau (pas un simple face) ; disponible en Suisse. Rang : e²/σ (proxy de la rigidité en flexion par masse, que les essais remplaceront), puis masse, puis prix. **Rien n'est choisi.**

| Rang | Carton | Famille | e (mm) | σ (g/m²) | e²/σ | Structure (g) | Prix structure (CHF) | Disponibilité |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | carton_ondule_double | ondule_double | 3,5 | 649 | 0,0189 | 480 | — | récupération (carton mesuré) |
| 2 | graukarton_3mm_modulor | gris_compact | 3,0 | 1 830 | 0,0049 | 1 351 | 5 | livraison en Suisse par Modulor (frais standard 36,90 € par  |
| 3 | callos_buchbinder_3mm_boesner | gris_compact | 3,0 | 1 890 | 0,0048 | 1 396 | 5 | oui, boesner.ch (« Online auf Lager ») |
| 4 | siebdruckkarton_finnboard_2mm_modulor | autre | 2,0 | 1 020 | 0,0039 | 753 | 8 | livraison en Suisse par Modulor (frais standard 36,90 € par  |
| 5 | graukarton_2mm_modulor | gris_compact | 2,0 | 1 150 | 0,0035 | 849 | 4 | livraison en Suisse par Modulor (frais standard 36,90 € par  |
| 6 | callos_buchbinder_2mm_boesner | gris_compact | 2,0 | 1 320 | 0,0030 | 975 | 4 | oui, boesner.ch (« Online auf Lager ») |
| 7 | graukarton_1mm_modulor | gris_compact | 1,0 | 700 | 0,0014 | 517 | 3 | livraison en Suisse par Modulor (frais standard 36,90 € par  |

**À peser** (épaisseur ou masse surfacique non publiée ; protocole `docs/protocole-carton.md`) : ondule_b_double_face_modulor (3,86 CHF/m²), ondule_e_micro_double_face_modulor (3,93 CHF/m²), ondule_e_couleur_marpa_boesner (8,57 CHF/m²), ondule_bc_double_modulor (5,19 CHF/m²), boite_230bc_jungheinrich (— CHF/m²), wabe_honeycomb_brun_20mm_modulor (22,26 CHF/m²), wabe_nonclad_15mm_modulor (16,04 CHF/m²), wabe_noir_5mm_modulor (35,84 CHF/m²), alveolo_brun_15mm_boesner (24,57 CHF/m²).

**Éliminés** : kapa_line_3mm_modulor (pas en filière papier mono-matière) ; kapa_line_5mm_modulor (pas en filière papier mono-matière) ; kapa_line_10mm_modulor (pas en filière papier mono-matière) ; kapa_line_5mm_boesner (pas en filière papier mono-matière) ; hartschaum_ps_5mm_modulor (pas en filière papier mono-matière) ; hartschaum_ps_10mm_modulor (pas en filière papier mono-matière) ; ondule_b_simple_face_rouleau_udobaer (simple face : pas un panneau) ; ondule_simple_face_opo (simple face : pas un panneau) ; claycote_b_kraft_bd (pas disponible en Suisse) ; claycote_c_bd (pas disponible en Suisse) ; claycote_e_blanc_bd (pas disponible en Suisse) ; boite_fefco0201_120b_igepa (disponibilité en Suisse non établie) ; zuschnitt_bc_220_igepa (disponibilité en Suisse non établie) ; claycote_eb_twin_bd (pas disponible en Suisse) ; graupappe_gpf_europapier (disponibilité en Suisse non établie) ; wabenkarton_10mm_igepa (disponibilité en Suisse non établie) ; forex_classic_3mm_modulor (pas en filière papier mono-matière) ; pp_alveolaire_3mm_modulor (pas en filière papier mono-matière).

## Modules, masse et coût : option « progressive » (décidée, fiche 0075)

bloc secteur 12 V aux niveaux 1 et 2 ; au niveau 3, pack 12S1P de la cellule du Lab, sa chaîne et son rail 12 V, dans un contenant ignifuge. Énergie du pack au-dessus de la coupure : 178 Wh ; calculateur : Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus). **Bloc secteur des niveaux 1 et 2** : pire cas = 8 servos au blocage (21,6 A, courants relevés, le plus fort de chaque servo) + calculateur à sa puissance maximale (25 W, 2,1 A), × 1,25 (marge PROPOSÉE) = **29,6 A** → Alimentation à découpage 12 V 30 A 360 W S-360-12 (30 A).

| Niveau | Module | Masse (kg) | Coût (CHF HT) | Inconnues (masse / prix) | Masse cumulée (kg) | Coût cumulé (CHF) |
| ---: | --- | ---: | ---: | --- | ---: | ---: |
| 0 | articulé | ≥ 0,48 | ≥ 0 | 1 / 2 | 0,48 | 0 |
| 1 | animé | 0,80 | 717 | 0 / 0 | 1,28 | 717 |
| 2 | interactif | ≥ 0,00 | ≥ 0 | 4 / 4 | 1,28 | 717 |
| 3 | debout | ≥ 1,77 | ≥ 461 | 3 / 1 | 3,05 | 1 178 |
| 4 | passage au Lab | 0,00 | 0 | 0 / 0 | 3,05 | 1 178 |

<details><summary>Composants par niveau</summary>

| Niveau | Composant | Nombre | Masse unitaire (g) | Prix unitaire (CHF HT) | Source |
| ---: | --- | ---: | ---: | ---: | --- |
| 0 | structure en carton | 1 | 480 | — | carton_ondule_double (mesuré (params/mesures.yaml)) |
| 0 | pivots (vis traversante, écrou, rondelles larges) × 26 | 1 | — | — | hardware.yaml (masse et prix non relevés) |
| 1 | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 1 | 345 | 499,98 | calculateurs.yaml (même règle que le Lab) |
| 1 | Bus Servo Adapter (A) (SKU 25514) | 1 | 16 | 4,17 | bus.yaml |
| 1 | neck_yaw : sts3215_c018 | 1 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 1 | neck_pitch : sts3215_c018 | 1 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 1 | shoulder_pitch : sts3215_c018 | 2 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 1 | shoulder_roll : sts3215_c018 | 2 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 1 | elbow_roll : sts3215_c018 | 2 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 1 | Alimentation à découpage 12 V 30 A 360 W S-360-12 (30 A) | 1 | 0 | 43,90 | kit_marche.yaml ; sur la table, hors du robot ; AUCUN bloc FERMÉ relevé ne tient ce courant : bornier 230 V à raccorder soi-même ; dispo : Ausverkauft (épuisé le 2026-10-08) |
| 2 | camera (aucun marché relevé) | 1 | — | — | — |
| 2 | microphone (aucun marché relevé) | 1 | — | — | — |
| 2 | haut_parleur (aucun marché relevé) | 1 | — | — | — |
| 2 | ecran_visage (aucun marché relevé) | 1 | — | — | — |
| 3 | 12S1P INR-21700-P50B | 12 | 92 | 8,44 | batteries.yaml ; masse × 1.3 (pack) |
| 3 | D42V110F12 (12V, 9A Step-Down Voltage Regulator) | 1 | 15 | 50,04 | puissance.yaml (courant NON vérifié : celui du Kit n'est pas calculé) |
| 3 | Victron MIDI-fuse 58V (30, 40, 50, 60, 100 A) | 1 | 2 | 15,76 | puissance.yaml (courant NON vérifié : celui du Kit n'est pas calculé) |
| 3 | Maytech MTS2009AS anti-spark switch 300A 20-85V | 1 | — | 74,20 | puissance.yaml (courant NON vérifié : celui du Kit n'est pas calculé) |
| 3 | JBD SP17S005 smart BMS (variantes NMC 20 à 120 A) | 1 | — | 21,54 | puissance.yaml (courant NON vérifié : celui du Kit n'est pas calculé) |
| 3 | LiPo Guard Lipobrandschutztasche XL | 1 | — | 9,07 | kit_marche.yaml (aucun essai indépendant trouvé) |
| 3 | hip_yaw : sts3215_c018 | 2 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 3 | hip_roll : sts3215_c018 | 2 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 3 | hip_pitch : sts3215_c018 | 2 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 3 | knee : sts3215_c018 | 2 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 3 | ankle_pitch : sts3250 | 2 | 74 | — | actionneurs.yaml (marché feetech) |
| 3 | waist_yaw : sts3215_c018 | 1 | 55 | 21,07 | actionneurs.yaml (marché feetech) |

</details>

## Modules, masse et coût : option « alignée sur le Lab »

pack 12S1P de la cellule du Lab (la moitié de son pack 12S2P), rail 12 V par convertisseur. Énergie du pack au-dessus de la coupure : 178 Wh ; calculateur : Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus).

| Niveau | Module | Masse (kg) | Coût (CHF HT) | Inconnues (masse / prix) | Masse cumulée (kg) | Coût cumulé (CHF) |
| ---: | --- | ---: | ---: | --- | ---: | ---: |
| 0 | articulé | ≥ 0,48 | ≥ 0 | 1 / 2 | 0,48 | 0 |
| 1 | animé | ≥ 1,93 | 935 | 2 / 0 | 2,41 | 935 |
| 2 | interactif | ≥ 0,00 | ≥ 0 | 4 / 4 | 2,41 | 935 |
| 3 | debout | 0,64 | ≥ 190 | 0 / 1 | 3,05 | 1 125 |
| 4 | passage au Lab | 0,00 | 0 | 0 / 0 | 3,05 | 1 125 |

<details><summary>Composants par niveau</summary>

| Niveau | Composant | Nombre | Masse unitaire (g) | Prix unitaire (CHF HT) | Source |
| ---: | --- | ---: | ---: | ---: | --- |
| 0 | structure en carton | 1 | 480 | — | carton_ondule_double (mesuré (params/mesures.yaml)) |
| 0 | pivots (vis traversante, écrou, rondelles larges) × 26 | 1 | — | — | hardware.yaml (masse et prix non relevés) |
| 1 | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 1 | 345 | 499,98 | calculateurs.yaml (même règle que le Lab) |
| 1 | Bus Servo Adapter (A) (SKU 25514) | 1 | 16 | 4,17 | bus.yaml |
| 1 | 12S1P INR-21700-P50B | 12 | 92 | 8,44 | batteries.yaml ; masse × 1.3 (pack) |
| 1 | D42V110F12 (12V, 9A Step-Down Voltage Regulator) | 1 | 15 | 50,04 | puissance.yaml (courant NON vérifié : celui du Kit n'est pas calculé) |
| 1 | Victron MIDI-fuse 58V (30, 40, 50, 60, 100 A) | 1 | 2 | 15,76 | puissance.yaml (courant NON vérifié : celui du Kit n'est pas calculé) |
| 1 | Maytech MTS2009AS anti-spark switch 300A 20-85V | 1 | — | 74,20 | puissance.yaml (courant NON vérifié : celui du Kit n'est pas calculé) |
| 1 | JBD SP17S005 smart BMS (variantes NMC 20 à 120 A) | 1 | — | 21,54 | puissance.yaml (courant NON vérifié : celui du Kit n'est pas calculé) |
| 1 | neck_yaw : sts3215_c018 | 1 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 1 | neck_pitch : sts3215_c018 | 1 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 1 | shoulder_pitch : sts3215_c018 | 2 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 1 | shoulder_roll : sts3215_c018 | 2 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 1 | elbow_roll : sts3215_c018 | 2 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 2 | camera (aucun marché relevé) | 1 | — | — | — |
| 2 | microphone (aucun marché relevé) | 1 | — | — | — |
| 2 | haut_parleur (aucun marché relevé) | 1 | — | — | — |
| 2 | ecran_visage (aucun marché relevé) | 1 | — | — | — |
| 3 | hip_yaw : sts3215_c018 | 2 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 3 | hip_roll : sts3215_c018 | 2 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 3 | hip_pitch : sts3215_c018 | 2 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 3 | knee : sts3215_c018 | 2 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 3 | ankle_pitch : sts3250 | 2 | 74 | — | actionneurs.yaml (marché feetech) |
| 3 | waist_yaw : sts3215_c018 | 1 | 55 | 21,07 | actionneurs.yaml (marché feetech) |

</details>

## Modules, masse et coût : option « minimale »

pack 3S1P en 21700, servos sur le pack, Raspberry Pi 5 (5 V par convertisseur). Énergie du pack au-dessus de la coupure : 44 Wh ; calculateur : Raspberry Pi 5 8GB.

| Niveau | Module | Masse (kg) | Coût (CHF HT) | Inconnues (masse / prix) | Masse cumulée (kg) | Coût cumulé (CHF) |
| ---: | --- | ---: | ---: | --- | ---: | ---: |
| 0 | articulé | ≥ 0,48 | ≥ 0 | 1 / 2 | 0,48 | 0 |
| 1 | animé | ≥ 0,73 | ≥ 430 | 5 / 3 | 1,21 | 430 |
| 2 | interactif | ≥ 0,00 | ≥ 58 | 4 / 3 | 1,21 | 488 |
| 3 | debout | 0,61 | 232 | 0 / 0 | 1,82 | 720 |
| 4 | passage au Lab | 0,00 | 0 | 0 / 0 | 1,82 | 720 |

<details><summary>Composants par niveau</summary>

| Niveau | Composant | Nombre | Masse unitaire (g) | Prix unitaire (CHF HT) | Source |
| ---: | --- | ---: | ---: | ---: | --- |
| 0 | structure en carton | 1 | 480 | — | carton_ondule_double (mesuré (params/mesures.yaml)) |
| 0 | pivots (vis traversante, écrou, rondelles larges) × 26 | 1 | — | — | hardware.yaml (masse et prix non relevés) |
| 1 | Raspberry Pi 5 8GB | 1 | — | 146,07 | calculateurs.yaml |
| 1 | Raspberry Pi AI HAT+ 13 TOPS | 1 | — | 58,43 | calculateurs.yaml |
| 1 | Bus Servo Adapter (A) (SKU 25514) | 1 | 16 | 4,17 | bus.yaml |
| 1 | 3S1P INR21700-50E | 3 | 90 | 6,26 | batteries.yaml ; masse × 1.3 (pack) |
| 1 | D42V55F5 (5V, 6A Step-Down Voltage Regulator) | 1 | 6 | 33,65 | puissance.yaml (courant NON vérifié : celui du Kit n'est pas calculé) |
| 1 | fusible 3S (hors du marché versé, qui vise le 12S) | 1 | — | — | — |
| 1 | anti_etincelle 3S (hors du marché versé, qui vise le 12S) | 1 | — | — | — |
| 1 | bms 3S (hors du marché versé, qui vise le 12S) | 1 | — | — | — |
| 1 | neck_yaw : sts3215_c018 | 1 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 1 | neck_pitch : sts3215_c018 | 1 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 1 | shoulder_pitch : sts3215_c018 | 2 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 1 | shoulder_roll : sts3215_c018 | 2 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 1 | elbow_roll : sts3215_c018 | 2 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 2 | Raspberry Pi AI Camera (pour information) | 1 | — | 58,43 | calculateurs.yaml |
| 2 | microphone (aucun marché relevé) | 1 | — | — | — |
| 2 | haut_parleur (aucun marché relevé) | 1 | — | — | — |
| 2 | ecran_visage (aucun marché relevé) | 1 | — | — | — |
| 3 | hip_yaw : sts3215_c018 | 2 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 3 | hip_roll : sts3215_c018 | 2 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 3 | hip_pitch : sts3215_c018 | 2 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 3 | knee : sts3215_c018 | 2 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 3 | ankle_pitch : sts3215_c018 | 2 | 55 | 21,07 | actionneurs.yaml (marché feetech) |
| 3 | waist_yaw : sts3215_c018 | 1 | 55 | 21,07 | actionneurs.yaml (marché feetech) |

</details>

## Couples et servos (option alignée : servos sur le rail 12 V)

Besoin = maximum de l'explorateur (à la masse du Kit au niveau du module) et du statique direct ; le servo doit tenir besoin × 1,5. Statique : bras tendu à l'horizontale, tête basculée de 90°.

| Niveau | Axe | Masse M (kg) | Pointe requise (N·m) | Continu requis (N·m) | Vitesse (rad/s) | Origine | Le visé tient ? | Debout tient ? | Servo Feetech | Inconnues |
| ---: | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| 1 | neck_yaw | 2,41 | 0,000 | 0,000 | 0,0 | aucune tâche ne charge cet axe | oui | — | sts3215_c018 (2,94 N·m) | — |
| 1 | neck_pitch | 2,41 | 0,025 | 0,081 | 0,0 | statique | oui | — | sts3215_c018 (2,94 N·m) | couple de pointe de sts3215_c018 (seul le blocage est publié) |
| 1 | shoulder_pitch | 2,41 | 0,203 | 0,140 | 1,7 | explorateur | oui | — | sts3215_c018 (2,94 N·m) | couple de pointe de sts3215_c018 (seul le blocage est publié) |
| 1 | shoulder_roll | 2,41 | 0,140 | 0,140 | 0,0 | statique | oui | — | sts3215_c018 (2,94 N·m) | couple de pointe de sts3215_c018 (seul le blocage est publié) |
| 1 | elbow_roll | 2,41 | 0,018 | 0,018 | 0,0 | statique | oui | — | sts3215_c018 (2,94 N·m) | couple de pointe de sts3215_c018 (seul le blocage est publié) |
| 3 | hip_yaw | 3,05 | 0,000 | 0,000 | 0,0 | aucune tâche ne charge cet axe | oui | — | sts3215_c018 (2,94 N·m) | — |
| 3 | hip_roll | 3,05 | 0,000 | 0,000 | 0,0 | aucune tâche ne charge cet axe | oui | — | sts3215_c018 (2,94 N·m) | — |
| 3 | hip_pitch | 3,05 | 0,383 | 0,383 | 0,0 | aucune tâche ne charge cet axe | oui | oui | sts3215_c018 (2,94 N·m) | couple de pointe de sts3215_c018 (seul le blocage est publié) |
| 3 | knee | 3,05 | 0,383 | 0,383 | 0,0 | aucune tâche ne charge cet axe | oui | oui | sts3215_c018 (2,94 N·m) | couple de pointe de sts3215_c018 (seul le blocage est publié) |
| 3 | ankle_pitch | 3,05 | 0,745 | 0,745 | 0,0 | aucune tâche ne charge cet axe | oui | oui | sts3250 (4,90 N·m) | prix de sts3250; vitesse de la fiche candidate (actionneurs.yaml, page web sans copie) |
| 3 | waist_yaw | 3,05 | 0,000 | 0,000 | 0,0 | aucune tâche ne charge cet axe | oui | — | sts3215_c018 (2,94 N·m) | — |

« Le visé » : les capacités du module (`vise`), statique compris ; « debout » : le statique seul (tibia incliné de 10°, PROPOSÉ). Quand le visé ne tient pas, le servo indiqué est celui qui tient debout.

Tous les axes motorisés ont un servo Feetech qui tient (sur ce qui est connu).

## Réutilisation Kit → Lab : option progressive (décidée)

**Part du coût CONNU du Kit réutilisée dans le Lab : 58 % sûrs, 71 % si les maillons « à vérifier » coïncident** (678 à 839 CHF sur 1 178 CHF ; les composants sans prix ne comptent pas).

| Niveau | Composant | Nombre | Prix total (CHF) | Au Lab | Pourquoi |
| ---: | --- | ---: | ---: | --- | --- |
| 0 | structure en carton | 1 | — | **recyclé** | le Lab est en aluminium ; carton en filière papier (si sans colle ni ruban) |
| 0 | pivots (vis traversante, écrou, rondelles larges) × 26 | 1 | — | **gardé en partie** | vis traversante et écrou : même règle de fixation au Lab ; longueurs à revoir |
| 1 | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 1 | 500 | **gardé** | le composant du Lab (fiches 0074 et 0075) |
| 1 | Bus Servo Adapter (A) (SKU 25514) | 1 | 4 | **gardé** | le Lab a aussi des Feetech aux petits axes (fiche 0075) |
| 1 | neck_yaw : sts3215_c018 | 1 | 21 | **gardé** | devient neck_yaw du Lab (Feetech, fiche 0075) : le modèle tient le besoin du Lab à 18,5 kg |
| 1 | neck_pitch : sts3215_c018 | 1 | 21 | **gardé** | devient gripper du Lab (Feetech, fiche 0075) : le modèle tient le besoin du Lab à 18,5 kg |
| 1 | shoulder_pitch : sts3215_c018 | 1 | 21 | **gardé** | devient gripper du Lab (Feetech, fiche 0075) : le modèle tient le besoin du Lab à 18,5 kg |
| 1 | shoulder_pitch : sts3215_c018 | 1 | 21 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 1 | shoulder_roll : sts3215_c018 | 2 | 42 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 1 | elbow_roll : sts3215_c018 | 2 | 42 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 1 | Alimentation à découpage 12 V 30 A 360 W S-360-12 (30 A) | 1 | 44 | **hors du Lab** | alimentation d'atelier (le Lab est sur batterie) ; reste utile au banc |
| 2 | camera (aucun marché relevé) | 1 | — | **gardé** | le composant du Lab (fiches 0074 et 0075) |
| 2 | microphone (aucun marché relevé) | 1 | — | **gardé (non requis)** | le Lab vise « + vision » ; la voix reste possible |
| 2 | haut_parleur (aucun marché relevé) | 1 | — | **gardé (non requis)** | le Lab vise « + vision » ; la voix reste possible |
| 2 | ecran_visage (aucun marché relevé) | 1 | — | **gardé** | le composant du Lab (fiches 0074 et 0075) |
| 3 | 12S1P INR-21700-P50B | 12 | 101 | **gardé** | les cellules du Kit sont la moitié du pack 12S2P du Lab (risque : appairer des cellules d'âges différents) |
| 3 | D42V110F12 (12V, 9A Step-Down Voltage Regulator) | 1 | 50 | **gardé (à vérifier)** | même catégorie que la chaîne du Lab, choisie ici sans le courant : le Lab peut en retenir un autre, plus gros |
| 3 | Victron MIDI-fuse 58V (30, 40, 50, 60, 100 A) | 1 | 16 | **gardé (à vérifier)** | même catégorie que la chaîne du Lab, choisie ici sans le courant : le Lab peut en retenir un autre, plus gros |
| 3 | Maytech MTS2009AS anti-spark switch 300A 20-85V | 1 | 74 | **gardé (à vérifier)** | même catégorie que la chaîne du Lab, choisie ici sans le courant : le Lab peut en retenir un autre, plus gros |
| 3 | JBD SP17S005 smart BMS (variantes NMC 20 à 120 A) | 1 | 22 | **gardé (à vérifier)** | même catégorie que la chaîne du Lab, choisie ici sans le courant : le Lab peut en retenir un autre, plus gros |
| 3 | LiPo Guard Lipobrandschutztasche XL | 1 | 9 | **gardé** | le composant du Lab (fiches 0074 et 0075) |
| 3 | hip_yaw : sts3215_c018 | 2 | 42 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 3 | hip_roll : sts3215_c018 | 2 | 42 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 3 | hip_pitch : sts3215_c018 | 2 | 42 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 3 | knee : sts3215_c018 | 2 | 42 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 3 | ankle_pitch : sts3250 | 1 | — | **gardé** | devient neck_pitch du Lab (Feetech, fiche 0075) : le modèle tient le besoin du Lab à 18,5 kg |
| 3 | ankle_pitch : sts3250 | 1 | — | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 3 | waist_yaw : sts3215_c018 | 1 | 21 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |

## Réutilisation Kit → Lab : option alignée

**Part du coût CONNU du Kit réutilisée dans le Lab : 59 % sûrs, 74 % si les maillons « à vérifier » coïncident** (669 à 830 CHF sur 1 125 CHF ; les composants sans prix ne comptent pas).

| Niveau | Composant | Nombre | Prix total (CHF) | Au Lab | Pourquoi |
| ---: | --- | ---: | ---: | --- | --- |
| 0 | structure en carton | 1 | — | **recyclé** | le Lab est en aluminium ; carton en filière papier (si sans colle ni ruban) |
| 0 | pivots (vis traversante, écrou, rondelles larges) × 26 | 1 | — | **gardé en partie** | vis traversante et écrou : même règle de fixation au Lab ; longueurs à revoir |
| 1 | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 1 | 500 | **gardé** | le composant du Lab (fiches 0074 et 0075) |
| 1 | Bus Servo Adapter (A) (SKU 25514) | 1 | 4 | **gardé** | le Lab a aussi des Feetech aux petits axes (fiche 0075) |
| 1 | 12S1P INR-21700-P50B | 12 | 101 | **gardé** | les cellules du Kit sont la moitié du pack 12S2P du Lab (risque : appairer des cellules d'âges différents) |
| 1 | D42V110F12 (12V, 9A Step-Down Voltage Regulator) | 1 | 50 | **gardé (à vérifier)** | même catégorie que la chaîne du Lab, choisie ici sans le courant : le Lab peut en retenir un autre, plus gros |
| 1 | Victron MIDI-fuse 58V (30, 40, 50, 60, 100 A) | 1 | 16 | **gardé (à vérifier)** | même catégorie que la chaîne du Lab, choisie ici sans le courant : le Lab peut en retenir un autre, plus gros |
| 1 | Maytech MTS2009AS anti-spark switch 300A 20-85V | 1 | 74 | **gardé (à vérifier)** | même catégorie que la chaîne du Lab, choisie ici sans le courant : le Lab peut en retenir un autre, plus gros |
| 1 | JBD SP17S005 smart BMS (variantes NMC 20 à 120 A) | 1 | 22 | **gardé (à vérifier)** | même catégorie que la chaîne du Lab, choisie ici sans le courant : le Lab peut en retenir un autre, plus gros |
| 1 | neck_yaw : sts3215_c018 | 1 | 21 | **gardé** | devient neck_yaw du Lab (Feetech, fiche 0075) : le modèle tient le besoin du Lab à 18,5 kg |
| 1 | neck_pitch : sts3215_c018 | 1 | 21 | **gardé** | devient gripper du Lab (Feetech, fiche 0075) : le modèle tient le besoin du Lab à 18,5 kg |
| 1 | shoulder_pitch : sts3215_c018 | 1 | 21 | **gardé** | devient gripper du Lab (Feetech, fiche 0075) : le modèle tient le besoin du Lab à 18,5 kg |
| 1 | shoulder_pitch : sts3215_c018 | 1 | 21 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 1 | shoulder_roll : sts3215_c018 | 2 | 42 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 1 | elbow_roll : sts3215_c018 | 2 | 42 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 2 | camera (aucun marché relevé) | 1 | — | **gardé** | le composant du Lab (fiches 0074 et 0075) |
| 2 | microphone (aucun marché relevé) | 1 | — | **gardé (non requis)** | le Lab vise « + vision » ; la voix reste possible |
| 2 | haut_parleur (aucun marché relevé) | 1 | — | **gardé (non requis)** | le Lab vise « + vision » ; la voix reste possible |
| 2 | ecran_visage (aucun marché relevé) | 1 | — | **gardé** | le composant du Lab (fiches 0074 et 0075) |
| 3 | hip_yaw : sts3215_c018 | 2 | 42 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 3 | hip_roll : sts3215_c018 | 2 | 42 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 3 | hip_pitch : sts3215_c018 | 2 | 42 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 3 | knee : sts3215_c018 | 2 | 42 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 3 | ankle_pitch : sts3250 | 1 | — | **gardé** | devient neck_pitch du Lab (Feetech, fiche 0075) : le modèle tient le besoin du Lab à 18,5 kg |
| 3 | ankle_pitch : sts3250 | 1 | — | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 3 | waist_yaw : sts3215_c018 | 1 | 21 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |

## Réutilisation Kit → Lab : option minimale

**Part du coût CONNU du Kit réutilisée dans le Lab : 9 % sûrs, 9 % si les maillons « à vérifier » coïncident** (67 à 67 CHF sur 720 CHF ; les composants sans prix ne comptent pas).

| Niveau | Composant | Nombre | Prix total (CHF) | Au Lab | Pourquoi |
| ---: | --- | ---: | ---: | --- | --- |
| 0 | structure en carton | 1 | — | **recyclé** | le Lab est en aluminium ; carton en filière papier (si sans colle ni ruban) |
| 0 | pivots (vis traversante, écrou, rondelles larges) × 26 | 1 | — | **gardé en partie** | vis traversante et écrou : même règle de fixation au Lab ; longueurs à revoir |
| 1 | Raspberry Pi 5 8GB | 1 | 146 | **recyclé** | option minimale : le Lab prend un autre calculateur et un pack 12S |
| 1 | Raspberry Pi AI HAT+ 13 TOPS | 1 | 58 | **recyclé** | option minimale : le Lab prend un autre calculateur et un pack 12S |
| 1 | Bus Servo Adapter (A) (SKU 25514) | 1 | 4 | **gardé** | le Lab a aussi des Feetech aux petits axes (fiche 0075) |
| 1 | 3S1P INR21700-50E | 3 | 19 | **recyclé** | option minimale : le Lab prend un autre calculateur et un pack 12S |
| 1 | D42V55F5 (5V, 6A Step-Down Voltage Regulator) | 1 | 34 | **recyclé** | option minimale : le Lab prend un autre calculateur et un pack 12S |
| 1 | fusible 3S (hors du marché versé, qui vise le 12S) | 1 | — | **recyclé** | option minimale : le Lab prend un autre calculateur et un pack 12S |
| 1 | anti_etincelle 3S (hors du marché versé, qui vise le 12S) | 1 | — | **recyclé** | option minimale : le Lab prend un autre calculateur et un pack 12S |
| 1 | bms 3S (hors du marché versé, qui vise le 12S) | 1 | — | **recyclé** | option minimale : le Lab prend un autre calculateur et un pack 12S |
| 1 | neck_yaw : sts3215_c018 | 1 | 21 | **gardé** | devient neck_yaw du Lab (Feetech, fiche 0075) : le modèle tient le besoin du Lab à 18,5 kg |
| 1 | neck_pitch : sts3215_c018 | 1 | 21 | **gardé** | devient gripper du Lab (Feetech, fiche 0075) : le modèle tient le besoin du Lab à 18,5 kg |
| 1 | shoulder_pitch : sts3215_c018 | 1 | 21 | **gardé** | devient gripper du Lab (Feetech, fiche 0075) : le modèle tient le besoin du Lab à 18,5 kg |
| 1 | shoulder_pitch : sts3215_c018 | 1 | 21 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 1 | shoulder_roll : sts3215_c018 | 2 | 42 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 1 | elbow_roll : sts3215_c018 | 2 | 42 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 2 | Raspberry Pi AI Camera (pour information) | 1 | 58 | **recyclé** | option minimale : le Lab prend un autre calculateur et un pack 12S |
| 2 | microphone (aucun marché relevé) | 1 | — | **recyclé** | option minimale : le Lab prend un autre calculateur et un pack 12S |
| 2 | haut_parleur (aucun marché relevé) | 1 | — | **recyclé** | option minimale : le Lab prend un autre calculateur et un pack 12S |
| 2 | ecran_visage (aucun marché relevé) | 1 | — | **recyclé** | option minimale : le Lab prend un autre calculateur et un pack 12S |
| 3 | hip_yaw : sts3215_c018 | 2 | 42 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 3 | hip_roll : sts3215_c018 | 2 | 42 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 3 | hip_pitch : sts3215_c018 | 2 | 42 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 3 | knee : sts3215_c018 | 2 | 42 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 3 | ankle_pitch : sts3215_c018 | 2 | 42 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
| 3 | waist_yaw : sts3215_c018 | 1 | 21 | **remplacé** | le Lab met cet axe en RobStride ; le servo est revendu ou réaffecté |
