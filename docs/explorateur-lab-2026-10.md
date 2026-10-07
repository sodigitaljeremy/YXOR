# Explorateur : YXOR Lab

**Engendré** par `.venv/bin/python scripts/explorateur.py --ecrire`. Ne pas éditer à la main. **Étude, aucune décision d'architecture** (phase 4a, fiche 0069).

## Loi de masse

DÉCIDÉE par Jeremy le 2026-10-07 (`params/lois_masse.yaml`, `retenue`) : Jeremy, 2026-10-07, réponse à la question de Claude (phase 4a) : « J'adopte la loi allométrique mesurée, avec son intervalle comme bande d'incertitude ; H³ reste en mémoire comme borne pessimiste. »

Une solution n'est **faisable** que si elle tient aux trois exposants b = 1,814, 1,995 et 2,176. La masse est donnée au b central. H³ (b = 3) est rapporté comme borne pessimiste, sans filtrer.

## Entrées et hypothèses

- Besoins : tables a·M + b des phases 3a (`exigences_physiques`) et 3b (`simulations_marche`, référence prudente : par axe, le robot le plus exigeant parmi ceux dont la marche couvre le Froude). Par axe, le **maximum** des tâches du profil, à la vraie masse de la solution ; `verifier_maximum` l'a recontrôlé sur 830 solutions.
- Marge : 1,5 sur les couples (fiche 0051). La vitesse à vide doit couvrir la vitesse de pointe, sans marge.
- Structure : 1,585 kg (part Winter du modèle de S, 0,60 m) × facteur des plaques **4,66** (plaques alu de la jambe basse, CAO, 450 g, contre 97 g de part Winter du tibia et du pied), puis × (H / 0,60)^b. **Un seul segment mesuré** : le facteur est étendu à toute la structure (hypothèse). Charge utile 1,2 kg (PROPOSÉE, `exigences_S.yaml`).
- Régimes : charge, saisie, poussée, buste et tête au couple **continu** ; saut, relevé et gestes au couple de **pointe** ; la marche aux deux.
- Place (règle SIMPLIFIÉE, l'étude H_min du 2026-10-04 n'a pas été versée) : (Ø_a + Ø_b)/2 + 2 mm ≤ longueur ANSUR × H, sur largeur_bassin (hip_yaw/hip_yaw), cuisse (hip_pitch/knee), tibia (knee/ankle_pitch), bras (shoulder_roll/elbow_roll), avant_bras (elbow_roll/wrist_pitch).
- Un axe absent de l'ensemble est rigide. Coût = actionneurs seuls (CHF HT, taux BCE de `budget.yaml`). Énergie de chute = M·g·(hauteur de hanche ANSUR × H).
- Actionneurs sans aucun couple publié, écartés : 0.

| Ensemble | Axes | Source |
| ---: | ---: | --- |
| 25 | 25 | RECONSTRUIT (étude du 2026-10-04 non versée) : v3 sans le roulis de taille |
| 26 | 26 | squelette v3 (params/squelette.yaml, fiche 0068 : 5 axes par jambe) |
| 27 | 27 | fiche 0069 (proposition de Claude) : jambes 6 × 2, taille 1, bras 5 × 2, pinces, cou 2 |
| 29 | 29 | RECONSTRUIT (étude du 2026-10-04 non versée) : le 27 avec la taille à 3 axes |

Familles du corps : robstride, damiao, steadywin, cubemars, myactuator, hightorque, encos, unitree ; petits axes (cou, pinces) : feetech, dynamixel. L'invariant « famille RobStride » de la fiche 0069 n'est PAS appliqué ici : l'explorateur montre ce qu'il coûte.

## Bilan

114688 solutions évaluées en 51 s : 6992 faisables, 34668 infaisables, 73028 INCONNUES. Par famille du corps :

| Famille | Faisables | Infaisables | INCONNUES |
| --- | ---: | ---: | ---: |
| robstride | 2608 | 3936 | 7792 |
| damiao | 0 | 1024 | 13312 |
| steadywin | 0 | 6220 | 8116 |
| cubemars | 2976 | 2432 | 8928 |
| myactuator | 1408 | 4928 | 8000 |
| hightorque | 0 | 14336 | 0 |
| encos | 0 | 1024 | 13312 |
| unitree | 0 | 768 | 13568 |

## Front de Pareto

![Front de Pareto](explorateur-lab-2026-10.svg)

5 solutions non dominées (coût, masse, énergie de chute, nombre de capacités tenues). **Toutes sont à H = 0,50 m, la borne BASSE de la plage du prompt** : plus petit est moins cher et plus léger tant que tout tient ; la plage n'a pas été étendue en dessous.

## Les 5 meilleures solutions

Classement PROPOSÉ : le plus de capacités, puis le moins cher, puis le plus léger, parmi le front.

| # | Ensemble | H (m) | Corps + petits | Masse (kg) [bande] | H³ (kg) | Coût (CHF) | Chute (J) | Capacités |
| ---: | ---: | ---: | --- | --- | --- | ---: | ---: | --- |
| 1 | 25 | 0,50 | robstride + feetech | 14,2 [14,0 ; 14,4] | 13,3 (tient) | 2 521 | 36 | 7 : marche_sol_plat, releve, saut_vertical, gestes_pointage, charge_lourde, poussee, buste |
| 2 | 26 | 0,50 | cubemars + feetech | 13,9 [13,7 ; 14,1] | 13,0 (tient) | 5 364 | 35 | 7 : marche_sol_plat, releve, saut_vertical, gestes_pointage, charge_lourde, poussee, buste |
| 3 | 25 | 0,50 | robstride + feetech | 12,6 [12,4 ; 12,7] | 11,7 (tient) | 2 347 | 32 | 6 : marche_sol_plat, releve, saut_vertical, gestes_pointage, poussee, buste |
| 4 | 25 | 0,50 | robstride + feetech | 12,0 [11,8 ; 12,2] | 11,1 (tient) | 2 146 | 30 | 5 : marche_sol_plat, releve, saut_vertical, gestes_pointage, buste |
| 5 | 25 | 0,50 | robstride + feetech | 11,7 [11,5 ; 11,9] | 10,8 (tient) | 2 200 | 30 | 4 : marche_sol_plat, releve, gestes_pointage, buste |

**1.** statut faisable ; actionneurs : rs00 : hip_yaw, hip_roll, elbow_roll ; rs06 : hip_pitch, knee, ankle_pitch ; rs02 : shoulder_pitch ; rs05 : shoulder_roll, wrist_pitch, wrist_roll, waist_yaw ; scs0009_c013 : gripper, neck_yaw, neck_pitch.
Reste INCONNU : sol_irregulier; pente; course; mains_a_doigts; visage (capacités non calculées) ; facteur de structure sur un seul segment ; place par la règle simplifiée.

**2.** statut faisable ; actionneurs : ak45_36 : hip_yaw, hip_roll, shoulder_pitch ; ak80_8 : hip_pitch, knee, ankle_pitch ; ak40_10_v3 : shoulder_roll, wrist_pitch, wrist_roll, waist_yaw, waist_roll ; ak45_10 : elbow_roll ; scs0009_c013 : gripper, neck_yaw, neck_pitch.
Reste INCONNU : sol_irregulier; pente; course; mains_a_doigts; visage (capacités non calculées) ; facteur de structure sur un seul segment ; place par la règle simplifiée.

**3.** statut faisable ; actionneurs : rs00 : hip_yaw, hip_roll ; rs02 : hip_pitch, knee ; rs06 : ankle_pitch ; rs05 : shoulder_pitch, shoulder_roll, elbow_roll, wrist_pitch, wrist_roll, waist_yaw ; scs0009_c013 : gripper, neck_yaw, neck_pitch.
Reste INCONNU : sol_irregulier; pente; course; mains_a_doigts; visage (capacités non calculées) ; facteur de structure sur un seul segment ; place par la règle simplifiée.

**4.** statut faisable ; actionneurs : rs00 : hip_yaw, hip_roll, ankle_pitch ; rs02 : hip_pitch, knee ; rs05 : shoulder_pitch, shoulder_roll, elbow_roll, wrist_pitch, wrist_roll, waist_yaw ; scs0009_c013 : gripper, neck_yaw, neck_pitch.
Reste INCONNU : sol_irregulier; pente; course; mains_a_doigts; visage (capacités non calculées) ; facteur de structure sur un seul segment ; place par la règle simplifiée.

**5.** statut faisable ; actionneurs : rs00 : hip_yaw, hip_roll ; rs02 : hip_pitch, knee ; rs05 : ankle_pitch, shoulder_pitch, shoulder_roll, elbow_roll, wrist_pitch, wrist_roll, waist_yaw ; scs0009_c013 : gripper, neck_yaw, neck_pitch.
Reste INCONNU : sol_irregulier; pente; course; mains_a_doigts; visage (capacités non calculées) ; facteur de structure sur un seul segment ; place par la règle simplifiée.

## Coût de chaque capacité

Pour chaque tâche et chaque niveau : la solution faisable la moins chère sur tout l'espace (ensembles, H, familles), avec la marche au niveau le plus bas ; l'écart est pris au niveau inférieur (au premier niveau : à la marche seule). « H min » = la plus petite taille où une solution est faisable.

**Lecture** : « le plus petit actionneur » est le plus LÉGER, pas le moins cher. Un niveau plus exigeant peut donc coûter MOINS (un actionneur plus lourd mais meilleur marché devient le plus petit qui passe) : un écart négatif n'est pas une erreur de calcul, c'est le prix de la légèreté.

| Tâche | Niveau | Coût (CHF) | + CHF | Masse (kg) | + kg | H de la moins chère | H min | Note |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| marche seule (référence) | 0.3 | 2 200 | — | 11,7 | — | 0,50 | 0,50 | |
| marche_sol_plat | 0.3 | 2 200 | — | 11,7 | — | 0,50 | 0,50 |  |
| marche_sol_plat | 0.6 | 2 200 | +0 | 11,7 | +0,0 | 0,50 | 0,50 |  |
| marche_sol_plat | 1.0 | — | — | — | — | — | — | aucune faisable ; 448 INCONNUES (surtout : marche_sol_plat 1.0 : aucun besoin calculé à H = 0,50 m (Froude au-delà des marches simulées)) |
| releve | depuis le dos | 2 200 | +0 | 11,7 | +0,0 | 0,50 | 0,50 |  |
| releve | depuis le ventre | 2 200 | +0 | 11,7 | +0,0 | 0,50 | 0,50 |  |
| saut_vertical | 5 | 2 146 | −55 | 12,0 | +0,3 | 0,50 | 0,50 |  |
| saut_vertical | 10 | 2 227 | +82 | 12,5 | +0,5 | 0,50 | 0,50 |  |
| saut_vertical | 20 | — | — | — | — | — | — | aucune faisable ; 168 INCONNUES (surtout : vitesse à vide de ec_a4310_p2_36) |
| saut_vertical | 30 | — | — | — | — | — | — | aucune faisable ; 168 INCONNUES (surtout : vitesse à vide de ec_a4310_p2_36) |
| gestes_pointage | 0.5 | 2 200 | +0 | 11,7 | +0,0 | 0,50 | 0,50 |  |
| gestes_pointage | 1.0 | 2 200 | +0 | 11,7 | +0,0 | 0,50 | 0,50 |  |
| gestes_pointage | 2.0 | 2 200 | +0 | 11,7 | +0,0 | 0,50 | 0,50 |  |
| saisie | 0.2 | — | — | — | — | — | — | aucune faisable ; 384 INCONNUES (surtout : couple continu de scs0002_c001) |
| saisie | 0.5 | — | — | — | — | — | — | aucune faisable ; 384 INCONNUES (surtout : couple continu de scs0002_c001) |
| saisie | 1.0 | — | — | — | — | — | — | aucune faisable ; 384 INCONNUES (surtout : couple continu de scs0002_c001) |
| charge_lourde | 2 | 2 458 | +258 | 14,5 | +2,8 | 0,55 | 0,50 |  |
| charge_lourde | 5 | 3 397 | +939 | 23,2 | +8,7 | 0,75 | 0,70 |  |
| charge_lourde | 10 | — | — | — | — | — | — | infaisable partout (448 essais ; surtout : charge_lourde # : M = # kg < # kg (équilibre ou frottement, b bas)) |
| poussee | 20 | 2 347 | +147 | 12,6 | +0,9 | 0,50 | 0,50 |  |
| poussee | 50 | 2 454 | +107 | 13,6 | +1,0 | 0,50 | 0,50 |  |
| poussee | 100 | — | — | — | — | — | — | aucune faisable ; 26 INCONNUES (surtout : vitesse à vide de ec_a4310_p2_36) |
| buste | lacet seul | 2 200 | +0 | 11,7 | +0,0 | 0,50 | 0,50 |  |
| buste | lacet + roulis + tangage | 2 635 | +434 | 13,2 | +1,5 | 0,50 | 0,50 |  |
| tete | 2 | — | — | — | — | — | — | aucune faisable ; 384 INCONNUES (surtout : couple continu de scs0002_c001) |
| tete | 3 | — | — | — | — | — | — | aucun ensemble n'a les axes requis |

## Données INCONNUES les plus bloquantes

Rangées par le nombre de solutions INCONNUES où elles manquent ; « seule » = solutions qui deviendraient décidables avec cette seule donnée.

| Donnée manquante | Solutions | Seule |
| --- | ---: | ---: |
| couple continu de scs0002_c001 | 29996 | 0 |
| prix de scs0002_c001 | 29996 | 0 |
| couple continu de xl330_m077 | 29992 | 10472 |
| couple continu de unitree_go_m8010_6 | 13568 | 0 |
| vitesse à vide de unitree_go_m8010_6 | 13568 | 0 |
| vitesse à vide de ec_a4310_p2_36 | 13312 | 672 |
| vitesse à vide de dm_j4340_v10 | 12168 | 0 |
| prix de dm_j4340_v10 | 12168 | 0 |
| couple continu de unitree_ys_342026_s288 | 10432 | 0 |
| vitesse à vide de ec_a2806_p2_36 | 9064 | 0 |
| couple de pointe de gim4310_36_gds34_24v (seul le blocage est publié) | 6716 | 0 |
| couple continu de unitree_im6014 | 6656 | 0 |

Hors calcul pour toute solution (capacités jamais « tenues » ici) :

- **sol_irregulier** : simulation de marche sur obstacles de 2 et 4 cm : non faite
- **pente** : simulation de marche en pente de 5 et 10° : non faite
- **course** : aucune politique de course (phase 3b) : rien à mettre à l'échelle
- **mains_a_doigts** : aucun ensemble du Lab n'a de doigts
- **visage** : masse, prix et place d'un écran ou de micro-servos : non relevés
- **structure** : facteur des plaques mesuré sur un seul segment ; les autres segments (cuisse, bassin, tronc, bras) restent à dessiner pour être pesés.
