# Explorateur : YXOR Lab

**Engendré** par `.venv/bin/python scripts/explorateur.py --ecrire`. Ne pas éditer à la main. **Étude, aucune décision d'architecture** (phases 4a et 4a bis, fiche 0069).

## Loi de masse

DÉCIDÉE par Jeremy le 2026-10-07 (`params/lois_masse.yaml`, `retenue`) : Jeremy, 2026-10-07, réponse à la question de Claude (phase 4a) : « J'adopte la loi allométrique mesurée, avec son intervalle comme bande d'incertitude ; H³ reste en mémoire comme borne pessimiste. »

Une solution n'est **faisable** que si elle tient aux trois exposants b = 1,814, 1,995 et 2,176, chacun avec la structure centrale (« évidée 50 % + 2 mm ») ET haute (« pleine 3 mm ») : six cas. La masse est donnée au b central, structure centrale ; la bande couvre les six cas. H³ (b = 3) est rapporté comme borne pessimiste, sans filtrer.

## Profil cible

Profil **lab** de `params/capacites.yaml` : DÉCIDÉ par Jeremy le 2026-10-07 (ses mots y sont cités). Capacités voulues : marche_sol_plat 0.6, sol_irregulier 2, pente 5, releve depuis le dos et depuis le ventre, saut_vertical 10, gestes_pointage 2.0, saisie 0.2, poussee 20, buste lacet seul, tete 2, visage écran. Axes exigés au-delà du calcul (PROPOSÉ) : sol_irregulier → ankle_roll, mains_a_doigts → doigts.

| Ensemble | Ne couvre pas | Voulues non calculées (INCONNUES) |
| ---: | --- | --- |
| 25 | sol_irregulier | pente, visage |
| 26 | sol_irregulier | pente, visage |
| 27 | — | sol_irregulier, pente, visage |
| 29 | — | sol_irregulier, pente, visage |

## Entrées et hypothèses

- Besoins : tables a·M + b des phases 3a (`exigences_physiques`) et 3b (`simulations_marche`, référence prudente : par axe, le robot le plus exigeant parmi ceux dont la marche couvre le Froude). Par axe, le **maximum** des tâches du profil, à la vraie masse de la solution ; `verifier_maximum` l'a recontrôlé sur 535 solutions.
- Marge : 1,5 sur les couples (fiche 0051). La vitesse à vide doit couvrir la vitesse de pointe, sans marge.
- Structure : segment par segment (`scripts/structure_plaques.py`, reconstruction des études du 2026-10-03 et 04 : caissons, liaisons à 90°, boîtes, étalonnés sur la CAO), à 0,60 m, puis × (H / 0,60)^b. Par ensemble (kg, centrale / haute) : 25 : 1,82 / 3,86 ; 26 : 1,86 / 3,92 ; 27 : 1,90 / 4,00 ; 29 : 1,97 / 4,12. Charge utile 1,2 kg (PROPOSÉE, `exigences_S.yaml`).
- Régimes : charge, saisie, poussée, buste et tête au couple **continu** ; saut, relevé et gestes au couple de **pointe** ; la marche aux deux.
- Place : taille minimale géométrique (`scripts/taille_minimale.py`, reconstruction de l'étude du 2026-10-04), lecture AVEC ÉCARTS : les chaînes verticales qui débordent (jambe, tronc, cou et tête) s'allongent, la hauteur RÉELLE vaut H + dépassements ; la lecture ANSUR stricte est rapportée. **Couples à la hauteur réelle** (phase 4a ter) : lus au pas supérieur de la grille (5 cm, prudent) au-dessus de la hauteur réelle, structure à la hauteur réelle, masse minimale au pas inférieur ; itération (choix → place → hauteur) jusqu'à stabilité. Le robot allongé est traité comme un robot proportionné à sa hauteur réelle : centre de gravité et bras de levier y grandissent tous, ce qui majore les couples (prudent). Cheville à 2 axes : la meilleure des options (a), (b), (d).
- Un axe absent de l'ensemble est rigide. Coût = actionneurs seuls (CHF HT, taux BCE de `budget.yaml`). Énergie de chute = M·g·(hauteur de hanche ANSUR × hauteur réelle).
- Actionneurs sans aucun couple publié, écartés : 0.

| Ensemble | Axes | Source |
| ---: | ---: | --- |
| 25 | 25 | JAMAIS calculé le 2026-10-04 (seulement cité par le prompt d'alors) : le 26 sans roulis de taille |
| 26 | 26 | squelette v3 (params/squelette.yaml, fiche 0068 : 5 axes par jambe) |
| 27 | 27 | fiche 0069 (proposition de Claude) et étude du 2026-10-04 : jambes 6 × 2, taille 1, bras 5 × 2, pinces, cou 2 |
| 29 | 29 | étude du 2026-10-04 (« 29, bras 5 ») : le 27 avec la taille à 3 axes |

Familles du corps : robstride, damiao, steadywin, cubemars, myactuator, hightorque, encos, unitree ; petits axes (cou, pinces) : feetech, dynamixel. L'invariant « famille RobStride » de la fiche 0069 n'est PAS appliqué ici : l'explorateur montre ce qu'il coûte.

## Bilan

73728 solutions évaluées en 69 s : 4740 faisables, 22496 infaisables, 46492 INCONNUES. Par famille du corps :

| Famille | Faisables | Infaisables | INCONNUES |
| --- | ---: | ---: | ---: |
| robstride | 1760 | 2272 | 5184 |
| damiao | 0 | 0 | 9216 |
| steadywin | 0 | 4704 | 4512 |
| cubemars | 1828 | 2208 | 5180 |
| myactuator | 1152 | 4096 | 3968 |
| hightorque | 0 | 9216 | 0 |
| encos | 0 | 0 | 9216 |
| unitree | 0 | 0 | 9216 |

## Front de Pareto

![Front de Pareto](explorateur-lab-2026-10.svg)

6 solutions non dominées (coût, masse, énergie de chute, capacités tenues, capacités voulues couvertes). **Toutes sont à H = 0,50 m, la borne BASSE de la plage du prompt** : plus petit est moins cher et plus léger tant que tout tient ; la plage n'a pas été étendue en dessous.

## Les 5 meilleures solutions

Classement PROPOSÉ : le moins de capacités voulues NON couvertes, puis le plus de capacités tenues, puis le moins cher, puis le plus léger, parmi le front. H = échelle des proportions ; « réelle » = avec les écarts.

| # | Ensemble | H → réelle (m) | Corps + petits | Masse (kg) [bande] | H³ (kg) | Coût (CHF) | Chute (J) | Capacités tenues | Ne couvre pas |
| ---: | ---: | --- | --- | --- | --- | ---: | ---: | --- | --- |
| 1 | 27 | 0,50 → 0,541 | robstride + feetech | 9,8 [9,8 ; 11,6] | 9,7 (tient) | 2 633 | 27 | 6 : marche_sol_plat, releve, saut_vertical, gestes_pointage, poussee, buste | — |
| 2 | 27 | 0,50 → 0,541 | robstride + feetech | 9,3 [9,2 ; 11,0] | 9,1 (tient) | 2 431 | 25 | 5 : marche_sol_plat, releve, saut_vertical, gestes_pointage, buste | — |
| 3 | 27 | 0,50 → 0,530 | robstride + feetech | 8,3 [8,3 ; 10,1] | 8,2 (tient) | 2 284 | 22 | 4 : marche_sol_plat, releve, gestes_pointage, buste | — |
| 4 | 25 | 0,50 → 0,541 | robstride + feetech | 9,4 [9,4 ; 11,1] | 9,2 (tient) | 2 429 | 26 | 6 : marche_sol_plat, releve, saut_vertical, gestes_pointage, poussee, buste | sol_irregulier |
| 5 | 25 | 0,50 → 0,530 | robstride + feetech | 8,8 [8,7 ; 10,4] | 8,6 (tient) | 2 227 | 23 | 5 : marche_sol_plat, releve, gestes_pointage, poussee, buste | sol_irregulier |

**1.** statut faisable ; actionneurs : rs00 : hip_yaw, hip_roll ; rs02 : hip_pitch ; rs06 : knee, ankle_pitch ; rs05 : ankle_roll, shoulder_pitch, shoulder_roll, elbow_roll, wrist_pitch, wrist_roll, waist_yaw ; scs0009_c013 : gripper, neck_yaw, neck_pitch.
Place : cheville (d), dépassements tronc +41 mm ; proportions ANSUR strictes : ne tient pas (il faudrait 0,633 m, limité par : tronc).
Capacités voulues INCONNUES (non calculées) : sol_irregulier, pente, visage.

**2.** statut faisable ; actionneurs : rs00 : hip_yaw, hip_roll, ankle_pitch ; rs02 : hip_pitch ; rs06 : knee ; rs05 : ankle_roll, shoulder_pitch, shoulder_roll, elbow_roll, wrist_pitch, wrist_roll, waist_yaw ; scs0009_c013 : gripper, neck_yaw, neck_pitch.
Place : cheville (a), dépassements tronc +41 mm ; proportions ANSUR strictes : ne tient pas (il faudrait 0,633 m, limité par : tronc).
Capacités voulues INCONNUES (non calculées) : sol_irregulier, pente, visage.

**3.** statut faisable ; actionneurs : rs00 : hip_yaw, hip_roll, hip_pitch ; rs02 : knee ; rs05 : ankle_pitch, ankle_roll, shoulder_pitch, shoulder_roll, elbow_roll, wrist_pitch, wrist_roll, waist_yaw ; scs0009_c013 : gripper, neck_yaw, neck_pitch.
Place : cheville (a), dépassements tronc +30 mm ; proportions ANSUR strictes : ne tient pas (il faudrait 0,598 m, limité par : tronc).
Capacités voulues INCONNUES (non calculées) : sol_irregulier, pente, visage.

**4.** statut faisable ; actionneurs : rs00 : hip_yaw, hip_roll ; rs02 : hip_pitch ; rs06 : knee, ankle_pitch ; rs05 : shoulder_pitch, shoulder_roll, elbow_roll, wrist_pitch, wrist_roll, waist_yaw ; scs0009_c013 : gripper, neck_yaw, neck_pitch.
Place : cheville (c), dépassements tronc +41 mm ; proportions ANSUR strictes : ne tient pas (il faudrait 0,633 m, limité par : tronc).
Capacités voulues INCONNUES (non calculées) : pente, visage.

**5.** statut faisable ; actionneurs : rs00 : hip_yaw, hip_roll, hip_pitch ; rs02 : knee ; rs06 : ankle_pitch ; rs05 : shoulder_pitch, shoulder_roll, elbow_roll, wrist_pitch, wrist_roll, waist_yaw ; scs0009_c013 : gripper, neck_yaw, neck_pitch.
Place : cheville (c), dépassements tronc +30 mm ; proportions ANSUR strictes : ne tient pas (il faudrait 0,598 m, limité par : tronc).
Capacités voulues INCONNUES (non calculées) : pente, visage.

## Coût de chaque capacité

Pour chaque tâche calculée du profil, et chaque niveau jusqu'au niveau visé : la solution faisable la moins chère sur tout l'espace (ensembles, H, familles), avec la marche au niveau du profil ; l'écart est pris au niveau inférieur (au premier niveau : à la marche seule). « H min » = la plus petite hauteur RÉELLE où une solution est faisable.

**Lecture** : « le plus petit actionneur » est le plus LÉGER, pas le moins cher. Un niveau plus exigeant peut donc coûter MOINS (un actionneur plus lourd mais meilleur marché devient le plus petit qui passe) : un écart négatif n'est pas une erreur de calcul, c'est le prix de la légèreté.

| Tâche | Niveau | Coût (CHF) | + CHF | Masse (kg) | + kg | Hauteur réelle de la moins chère | H min réelle | Note |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| marche seule (référence) | 0.6 | 1 961 | — | 7,8 | — | 0,530 | 0,530 | |
| marche_sol_plat | 0.3 | 1 961 | — | 7,8 | — | 0,530 | 0,530 |  |
| marche_sol_plat | 0.6 | 1 961 | +0 | 7,8 | +0,0 | 0,530 | 0,530 |  |
| releve | depuis le dos | 1 961 | +0 | 7,8 | +0,0 | 0,530 | 0,530 |  |
| releve | depuis le ventre | 1 961 | +0 | 7,8 | +0,0 | 0,530 | 0,530 |  |
| saut_vertical | 5 | 2 080 | +120 | 7,9 | +0,1 | 0,530 | 0,530 |  |
| saut_vertical | 10 | 2 227 | +147 | 8,8 | +0,9 | 0,541 | 0,541 |  |
| gestes_pointage | 0.5 | 1 961 | +0 | 7,8 | +0,0 | 0,530 | 0,530 |  |
| gestes_pointage | 1.0 | 1 961 | +0 | 7,8 | +0,0 | 0,530 | 0,530 |  |
| gestes_pointage | 2.0 | 1 961 | +0 | 7,8 | +0,0 | 0,530 | 0,530 |  |
| saisie | 0.2 | — | — | — | — | — | — | aucune faisable ; 494 INCONNUES (surtout : couple continu de scs0002_c001) |
| poussee | 20 | 2 227 | +267 | 8,8 | +1,0 | 0,530 | 0,530 |  |
| buste | lacet seul | 1 961 | +0 | 7,8 | +0,0 | 0,530 | 0,530 |  |
| tete | 2 | — | — | — | — | — | — | aucune faisable ; 498 INCONNUES (surtout : couple continu de scs0002_c001) |

## Données INCONNUES les plus bloquantes

Rangées par le nombre de solutions INCONNUES où elles manquent ; « seule » = solutions qui deviendraient décidables avec cette seule donnée.

| Donnée manquante | Solutions | Seule |
| --- | ---: | ---: |
| couple continu de scs0002_c001 | 19168 | 0 |
| prix de scs0002_c001 | 19168 | 0 |
| couple continu de xl330_m077 | 19148 | 6900 |
| vitesse à vide de ec_a4310_p2_36 | 9216 | 248 |
| vitesse à vide de unitree_go_m8010_6 | 9216 | 0 |
| couple continu de unitree_go_m8010_6 | 9184 | 0 |
| vitesse à vide de dm_j4340_v10 | 8996 | 0 |
| prix de dm_j4340_v10 | 8996 | 0 |
| vitesse à vide de ec_a2806_p2_36 | 7768 | 0 |
| couple continu de unitree_im6014 | 5856 | 0 |
| vitesse à vide de unitree_im6014 | 5856 | 0 |
| couple continu de unitree_ys_342026_s288 | 5184 | 0 |

Hors calcul pour toute solution (capacités jamais « tenues » ici) :

- **sol_irregulier** : simulation de marche sur obstacles de 2 et 4 cm : non faite
- **pente** : simulation de marche en pente de 5 et 10° : non faite
- **course** : aucune politique de course (phase 3b) : rien à mettre à l'échelle
- **mains_a_doigts** : aucun ensemble du Lab n'a de doigts
- **visage** : masse, prix et place d'un écran ou de micro-servos : non relevés
- **structure** : seule la jambe basse est dessinée ; les autres segments sont estimés par des formules étalonnées sur elle ; l'évidement est une borne haute ; l'alu 2 mm n'est pas confirmé chez l'opérateur.
- **place** : volume de l'électronique et de la batterie dans le tronc compté NUL ; cardan des bielles (b) supposé ; servos en boîtier pris dans leur plus grande cote.
