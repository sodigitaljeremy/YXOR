# Explorateur : YXOR Lab

**Engendré** par `.venv/bin/python scripts/explorateur.py --ecrire`. Ne pas éditer à la main. **Étude, aucune décision d'architecture** (phases 4a et 4a bis, fiche 0069).

## Loi de masse

DÉCIDÉE par Jeremy le 2026-10-07 (`params/lois_masse.yaml`, `retenue`) : Jeremy, 2026-10-07, réponse à la question de Claude (phase 4a) : « J'adopte la loi allométrique mesurée, avec son intervalle comme bande d'incertitude ; H³ reste en mémoire comme borne pessimiste. »

Une solution n'est **faisable** que si elle tient aux trois exposants b = 1,814, 1,995 et 2,176, chacun avec la structure centrale (« évidée 50 % + 2 mm ») ET haute (« pleine 3 mm ») : six cas. La masse est donnée au b central, structure centrale ; la bande couvre les six cas. H³ (b = 3) est rapporté comme borne pessimiste, sans filtrer.

## Profil cible

Capacités VOULUES (par défaut : toutes celles de la fiche 0069 ; niveau le plus bas, sauf le buste à 3 axes, « rotation et inclinaison » : PROPOSÉ) : marche_sol_plat 0.3, sol_irregulier 2, pente 5, releve depuis le dos, course 1.5, saut_vertical 5, gestes_pointage 0.5, saisie 0.2, charge_lourde 2, poussee 20, mains_a_doigts 6, buste lacet + roulis + tangage, tete 2, visage écran. Axes exigés au-delà du calcul (PROPOSÉ) : sol_irregulier → ankle_roll, mains_a_doigts → doigts.

| Ensemble | Ne couvre pas | Voulues non calculées (INCONNUES) |
| ---: | --- | --- |
| 25 | sol_irregulier, mains_a_doigts, buste | pente, course, visage |
| 26 | sol_irregulier, mains_a_doigts, buste | pente, course, visage |
| 27 | mains_a_doigts, buste | sol_irregulier, pente, course, visage |
| 29 | mains_a_doigts | sol_irregulier, pente, course, visage |

## Entrées et hypothèses

- Besoins : tables a·M + b des phases 3a (`exigences_physiques`) et 3b (`simulations_marche`, référence prudente : par axe, le robot le plus exigeant parmi ceux dont la marche couvre le Froude). Par axe, le **maximum** des tâches du profil, à la vraie masse de la solution ; `verifier_maximum` l'a recontrôlé sur 628 solutions.
- Marge : 1,5 sur les couples (fiche 0051). La vitesse à vide doit couvrir la vitesse de pointe, sans marge.
- Structure : segment par segment (`scripts/structure_plaques.py`, reconstruction des études du 2026-10-03 et 04 : caissons, liaisons à 90°, boîtes, étalonnés sur la CAO), à 0,60 m, puis × (H / 0,60)^b. Par ensemble (kg, centrale / haute) : 25 : 1,82 / 3,86 ; 26 : 1,86 / 3,92 ; 27 : 1,90 / 4,00 ; 29 : 1,97 / 4,12. Charge utile 1,2 kg (PROPOSÉE, `exigences_S.yaml`).
- Régimes : charge, saisie, poussée, buste et tête au couple **continu** ; saut, relevé et gestes au couple de **pointe** ; la marche aux deux.
- Place : taille minimale géométrique (`scripts/taille_minimale.py`, reconstruction de l'étude du 2026-10-04), lecture AVEC ÉCARTS : les chaînes verticales qui débordent (jambe, tronc, cou et tête) s'allongent, la hauteur RÉELLE vaut H + dépassements ; la lecture ANSUR stricte est rapportée. Les couples et la masse restent calculés à H (hypothèse). Cheville à 2 axes : la meilleure des options (a), (b), (d).
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

92160 solutions évaluées en 63 s : 5640 faisables, 32610 infaisables, 53910 INCONNUES. Par famille du corps :

| Famille | Faisables | Infaisables | INCONNUES |
| --- | ---: | ---: | ---: |
| robstride | 2216 | 2664 | 6640 |
| damiao | 0 | 1472 | 10048 |
| steadywin | 0 | 5608 | 5912 |
| cubemars | 2224 | 2674 | 6622 |
| myactuator | 1200 | 4128 | 6192 |
| hightorque | 0 | 11520 | 0 |
| encos | 0 | 2304 | 9216 |
| unitree | 0 | 2240 | 9280 |

## Front de Pareto

![Front de Pareto](explorateur-lab-2026-10.svg)

14 solutions non dominées (coût, masse, énergie de chute, capacités tenues, capacités voulues couvertes).

## Les 5 meilleures solutions

Classement PROPOSÉ : le moins de capacités voulues NON couvertes, puis le plus de capacités tenues, puis le moins cher, puis le plus léger, parmi le front. H = échelle des proportions ; « réelle » = avec les écarts.

| # | Ensemble | H → réelle (m) | Corps + petits | Masse (kg) [bande] | H³ (kg) | Coût (CHF) | Chute (J) | Capacités tenues | Ne couvre pas |
| ---: | ---: | --- | --- | --- | --- | ---: | ---: | --- | --- |
| 1 | 29 | 0,60 → 0,771 | robstride + feetech | 12,5 [12,5 ; 14,6] | 12,5 (tient) | 3 219 | 49 | 7 : marche_sol_plat, releve, saut_vertical, gestes_pointage, charge_lourde, poussee, buste | mains_a_doigts |
| 2 | 29 | 0,60 → 0,842 | cubemars + feetech | 11,8 [11,8 ; 14,0] | 11,8 (tient) | 6 163 | 50 | 7 : marche_sol_plat, releve, saut_vertical, gestes_pointage, charge_lourde, poussee, buste | mains_a_doigts |
| 3 | 29 | 0,50 → 0,658 | robstride + feetech | 9,8 [9,7 ; 11,3] | 9,5 (tient) | 2 580 | 32 | 6 : marche_sol_plat, releve, saut_vertical, gestes_pointage, poussee, buste | mains_a_doigts |
| 4 | 29 | 0,50 → 0,658 | robstride + feetech | 8,9 [8,8 ; 10,5] | 8,7 (tient) | 2 433 | 30 | 5 : marche_sol_plat, releve, saut_vertical, gestes_pointage, buste | mains_a_doigts |
| 5 | 29 | 0,50 → 0,658 | robstride + feetech | 8,8 [8,7 ; 10,4] | 8,6 (tient) | 2 313 | 29 | 4 : marche_sol_plat, releve, gestes_pointage, buste | mains_a_doigts |

**1.** statut faisable ; actionneurs : rs00 : hip_yaw, elbow_roll, waist_roll ; rs02 : hip_roll ; rs06 : hip_pitch, knee, ankle_pitch ; rs05 : ankle_roll, shoulder_roll, wrist_pitch, wrist_roll, waist_yaw ; rs10p : shoulder_pitch, waist_pitch ; scs0009_c013 : gripper, neck_yaw, neck_pitch.
Place : cheville (a), dépassements tronc +171 mm ; proportions ANSUR strictes : ne tient pas (il faudrait 1,162 m, limité par : tronc).
Capacités voulues INCONNUES (non calculées) : sol_irregulier, pente, course, visage.

**2.** statut faisable ; actionneurs : ak45_36 : hip_yaw, hip_roll, shoulder_pitch, waist_roll ; ak80_8 : hip_pitch, knee, ankle_pitch, waist_pitch ; ak40_10_v3 : ankle_roll, shoulder_roll, wrist_pitch, wrist_roll, waist_yaw ; ak45_10 : elbow_roll ; scs0009_c013 : gripper, neck_yaw, neck_pitch.
Place : cheville (d), dépassements tronc +242 mm ; proportions ANSUR strictes : ne tient pas (il faudrait 1,392 m, limité par : tronc).
Capacités voulues INCONNUES (non calculées) : sol_irregulier, pente, course, visage.

**3.** statut faisable ; actionneurs : rs00 : hip_yaw, hip_roll, hip_pitch, waist_roll, waist_pitch ; rs02 : knee ; rs06 : ankle_pitch ; rs05 : ankle_roll, shoulder_pitch, shoulder_roll, elbow_roll, wrist_pitch, wrist_roll, waist_yaw ; scs0009_c013 : gripper, neck_yaw, neck_pitch.
Place : cheville (a), dépassements tronc +158 mm ; proportions ANSUR strictes : ne tient pas (il faudrait 1,019 m, limité par : tronc).
Capacités voulues INCONNUES (non calculées) : sol_irregulier, pente, course, visage.

**4.** statut faisable ; actionneurs : rs00 : hip_yaw, hip_roll, hip_pitch, waist_roll, waist_pitch ; rs02 : knee ; rs05 : ankle_pitch, ankle_roll, shoulder_pitch, shoulder_roll, elbow_roll, wrist_pitch, wrist_roll, waist_yaw ; scs0009_c013 : gripper, neck_yaw, neck_pitch.
Place : cheville (a), dépassements tronc +158 mm ; proportions ANSUR strictes : ne tient pas (il faudrait 1,019 m, limité par : tronc).
Capacités voulues INCONNUES (non calculées) : sol_irregulier, pente, course, visage.

**5.** statut faisable ; actionneurs : rs00 : hip_yaw, hip_roll, hip_pitch, knee, waist_roll, waist_pitch ; rs05 : ankle_pitch, ankle_roll, shoulder_pitch, shoulder_roll, elbow_roll, wrist_pitch, wrist_roll, waist_yaw ; scs0009_c013 : gripper, neck_yaw, neck_pitch.
Place : cheville (a), dépassements tronc +158 mm ; proportions ANSUR strictes : ne tient pas (il faudrait 1,019 m, limité par : tronc).
Capacités voulues INCONNUES (non calculées) : sol_irregulier, pente, course, visage.

**Réserve** : le tronc de ces solutions dépasse ANSUR jusqu'à 132% de sa longueur (ensemble 29, H 0,60 m). La lecture « avec écarts » l'autorise, mais les couples sont calculés aux proportions de H : pour un tronc aussi long, le centre de gravité est plus haut et les couples sont SOUS-estimés. C'est la taille à plusieurs axes empilés qui allonge le tronc (constat déjà fait le 2026-10-04).

## Coût de chaque capacité

Pour chaque tâche et chaque niveau : la solution faisable la moins chère sur tout l'espace (ensembles, H, familles), avec la marche au niveau le plus bas ; l'écart est pris au niveau inférieur (au premier niveau : à la marche seule). « H min » = la plus petite hauteur RÉELLE où une solution est faisable.

**Lecture** : « le plus petit actionneur » est le plus LÉGER, pas le moins cher. Un niveau plus exigeant peut donc coûter MOINS (un actionneur plus lourd mais meilleur marché devient le plus petit qui passe) : un écart négatif n'est pas une erreur de calcul, c'est le prix de la légèreté.

| Tâche | Niveau | Coût (CHF) | + CHF | Masse (kg) | + kg | Hauteur réelle de la moins chère | H min réelle | Note |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| marche seule (référence) | 0.3 | 1 961 | — | 7,6 | — | 0,530 | 0,530 | |
| marche_sol_plat | 0.3 | 1 961 | — | 7,6 | — | 0,530 | 0,530 |  |
| marche_sol_plat | 0.6 | 1 961 | +0 | 7,6 | +0,0 | 0,530 | 0,530 |  |
| marche_sol_plat | 1.0 | — | — | — | — | — | — | aucune faisable ; 576 INCONNUES (surtout : marche_sol_plat 1.0 : aucun besoin calculé à H = 0,50 m (Froude au-delà des marches simulées)) |
| releve | depuis le dos | 1 961 | +0 | 7,6 | +0,0 | 0,530 | 0,530 |  |
| releve | depuis le ventre | 1 961 | +0 | 7,6 | +0,0 | 0,530 | 0,530 |  |
| saut_vertical | 5 | 1 961 | +0 | 7,9 | +0,3 | 0,565 | 0,530 |  |
| saut_vertical | 10 | 2 146 | +185 | 8,7 | +0,8 | 0,610 | 0,541 |  |
| saut_vertical | 20 | 2 631 | +485 | 11,0 | +2,3 | 0,703 | 0,700 |  |
| saut_vertical | 30 | — | — | — | — | — | — | aucune faisable ; 216 INCONNUES (surtout : vitesse à vide de dm_j4340p_v11) |
| gestes_pointage | 0.5 | 1 961 | +0 | 7,6 | +0,0 | 0,530 | 0,530 |  |
| gestes_pointage | 1.0 | 1 961 | +0 | 7,6 | +0,0 | 0,530 | 0,530 |  |
| gestes_pointage | 2.0 | 1 961 | +0 | 7,6 | +0,0 | 0,530 | 0,530 |  |
| saisie | 0.2 | — | — | — | — | — | — | aucune faisable ; 502 INCONNUES (surtout : couple continu de scs0002_c001) |
| saisie | 0.5 | — | — | — | — | — | — | aucune faisable ; 502 INCONNUES (surtout : couple continu de scs0002_c001) |
| saisie | 1.0 | — | — | — | — | — | — | aucune faisable ; 501 INCONNUES (surtout : couple continu de scs0002_c001) |
| charge_lourde | 2 | 2 468 | +507 | 10,4 | +2,7 | 0,672 | 0,660 |  |
| charge_lourde | 5 | 3 889 | +1 422 | 18,4 | +8,0 | 1,119 | 0,850 |  |
| charge_lourde | 10 | — | — | — | — | — | — | infaisable partout (576 essais ; surtout : charge_lourde # : M = # kg < # kg (équilibre ou frottement, b central, structure central)) |
| poussee | 20 | 2 107 | +147 | 8,5 | +0,9 | 0,530 | 0,530 |  |
| poussee | 50 | 2 589 | +482 | 10,7 | +2,2 | 0,565 | 0,555 |  |
| poussee | 100 | — | — | — | — | — | — | infaisable partout (576 essais ; surtout : poussee # : M = # kg < # kg (équilibre ou frottement, b bas, structure central)) |
| buste | lacet seul | 1 961 | +0 | 7,6 | +0,0 | 0,530 | 0,530 |  |
| buste | lacet + roulis + tangage | 2 313 | +353 | 8,8 | +1,2 | 0,658 | 0,658 |  |
| tete | 2 | — | — | — | — | — | — | aucune faisable ; 502 INCONNUES (surtout : couple continu de scs0002_c001) |
| tete | 3 | — | — | — | — | — | — | aucun ensemble n'a les axes requis |

## Données INCONNUES les plus bloquantes

Rangées par le nombre de solutions INCONNUES où elles manquent ; « seule » = solutions qui deviendraient décidables avec cette seule donnée.

| Donnée manquante | Solutions | Seule |
| --- | ---: | ---: |
| couple continu de xl330_m077 | 22326 | 8416 |
| couple continu de scs0002_c001 | 22308 | 0 |
| prix de scs0002_c001 | 22308 | 0 |
| vitesse à vide de dm_j4340_v10 | 9584 | 0 |
| prix de dm_j4340_v10 | 9584 | 0 |
| couple continu de unitree_go_m8010_6 | 9280 | 0 |
| vitesse à vide de unitree_go_m8010_6 | 9280 | 0 |
| vitesse à vide de ec_a4310_p2_36 | 9216 | 280 |
| vitesse à vide de ec_a2806_p2_36 | 7376 | 0 |
| couple continu de unitree_ys_342026_s288 | 7264 | 0 |
| couple de pointe de gim4310_36_gds34_24v (seul le blocage est publié) | 5260 | 0 |
| vitesse à vide de dm_j4340p_v11 | 4408 | 0 |

Hors calcul pour toute solution (capacités jamais « tenues » ici) :

- **sol_irregulier** : simulation de marche sur obstacles de 2 et 4 cm : non faite
- **pente** : simulation de marche en pente de 5 et 10° : non faite
- **course** : aucune politique de course (phase 3b) : rien à mettre à l'échelle
- **mains_a_doigts** : aucun ensemble du Lab n'a de doigts
- **visage** : masse, prix et place d'un écran ou de micro-servos : non relevés
- **structure** : seule la jambe basse est dessinée ; les autres segments sont estimés par des formules étalonnées sur elle ; l'évidement est une borne haute ; l'alu 2 mm n'est pas confirmé chez l'opérateur.
- **place** : volume de l'électronique et de la batterie dans le tronc compté NUL ; cardan des bielles (b) supposé ; servos en boîtier pris dans leur plus grande cote.
