# Explorateur : YXOR Lab

**Engendré** par `.venv/bin/python scripts/explorateur.py --ecrire`. Ne pas éditer à la main. **Étude, aucune décision d'architecture** (phases 4a et 4a bis, fiche 0069).

## Loi de masse

DÉCIDÉE par Jeremy le 2026-10-07 (`params/lois_masse.yaml`, `retenue`) : Jeremy, 2026-10-07, réponse à la question de Claude (phase 4a) : « J'adopte la loi allométrique mesurée, avec son intervalle comme bande d'incertitude ; H³ reste en mémoire comme borne pessimiste. »

Une solution n'est **faisable** que si elle tient aux trois exposants b = 1,814, 1,995 et 2,176, chacun avec la structure centrale (« évidée 50 % + 2 mm ») ET haute (« pleine 3 mm ») : six cas. La masse est donnée au b central, structure centrale ; la bande couvre les six cas. H³ (b = 3) est rapporté comme borne pessimiste, sans filtrer.

## Profil cible

Profil **lab** de `params/capacites.yaml` : DÉCIDÉ par Jeremy le 2026-10-07 (ses mots y sont cités). Capacités voulues : marche_sol_plat 0.6, sol_irregulier 2, pente 5, releve depuis le dos et depuis le ventre, saut_vertical 10, gestes_pointage 2.0, saisie 0.2, poussee 20, buste lacet seul, tete 2, visage écran, autonomie 30, ia_embarquee + vision. Axes exigés au-delà du calcul (PROPOSÉ) : sol_irregulier → ankle_roll, mains_a_doigts → doigts.

| Ensemble | Ne couvre pas | Voulues non calculées (INCONNUES) |
| ---: | --- | --- |
| 25 | sol_irregulier | pente, visage |
| 26 | sol_irregulier | pente, visage |
| 27 | — | sol_irregulier, pente, visage |
| 29 | — | sol_irregulier, pente, visage |

## Entrées et hypothèses

- Besoins : tables a·M + b des phases 3a (`exigences_physiques`) et 3b (`simulations_marche`, référence prudente : par axe, le robot le plus exigeant parmi ceux dont la marche couvre le Froude). Par axe, le **maximum** des tâches du profil, à la vraie masse de la solution ; `verifier_maximum` l'a recontrôlé sur 218 solutions.
- Marge : 1,5 sur les couples (fiche 0051). La vitesse à vide doit couvrir la vitesse de pointe, sans marge.
- Structure : segment par segment (`scripts/structure_plaques.py`, reconstruction des études du 2026-10-03 et 04 : caissons, liaisons à 90°, boîtes, étalonnés sur la CAO), à 0,60 m, puis × (H / 0,60)^b. Par ensemble (kg, centrale / haute) : 25 : 1,82 / 3,86 ; 26 : 1,86 / 3,92 ; 27 : 1,90 / 4,00 ; 29 : 1,97 / 4,12. Charge utile 0,3 kg (PROPOSÉE, `exigences_S.yaml`).
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

73728 solutions évaluées en 511 s : 0 faisables, 52602 infaisables, 21126 INCONNUES. Par famille du corps :

| Famille | Faisables | Infaisables | INCONNUES |
| --- | ---: | ---: | ---: |
| robstride | 0 | 7364 | 1852 |
| damiao | 0 | 4994 | 4222 |
| steadywin | 0 | 8976 | 240 |
| cubemars | 0 | 2500 | 6716 |
| myactuator | 0 | 8768 | 448 |
| hightorque | 0 | 9216 | 0 |
| encos | 0 | 1568 | 7648 |
| unitree | 0 | 9216 | 0 |

## Front de Pareto

![Front de Pareto](explorateur-lab-2026-10.svg)

0 solutions non dominées (coût, masse, énergie de chute, capacités tenues, capacités voulues couvertes).

## Les 5 meilleures solutions

Classement PROPOSÉ : le moins de capacités voulues NON couvertes, puis le plus de capacités tenues, puis le moins cher, puis le plus léger, parmi le front. H = échelle des proportions ; « réelle » = avec les écarts.

| # | Ensemble | H → réelle (m) | Corps + petits | Masse (kg) [bande] | H³ (kg) | Coût (CHF) | Chute (J) | Capacités tenues | Ne couvre pas |
| ---: | ---: | --- | --- | --- | --- | ---: | ---: | --- | --- |

## Coût de chaque capacité

Pour chaque tâche calculée du profil, et chaque niveau jusqu'au niveau visé : la solution faisable la moins chère sur tout l'espace (ensembles, H, familles), avec la marche au niveau du profil ; l'écart est pris au niveau inférieur (au premier niveau : à la marche seule). « H min » = la plus petite hauteur RÉELLE où une solution est faisable.

**Lecture** : « le plus petit actionneur » est le plus LÉGER, pas le moins cher. Un niveau plus exigeant peut donc coûter MOINS (un actionneur plus lourd mais meilleur marché devient le plus petit qui passe) : un écart négatif n'est pas une erreur de calcul, c'est le prix de la légèreté.

| Tâche | Niveau | Coût (CHF) | + CHF | Masse (kg) | + kg | Hauteur réelle de la moins chère | H min réelle | Note |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| marche seule (référence) | 0.6 | ≥ 4 595 | — | 15,8 | — | 0,873 | — | |
| marche_sol_plat | 0.3 | ≥ 4 595 | — | 15,8 | — | 0,873 | — | ≥ : chaîne de puissance incomplètement chiffrée |
| marche_sol_plat | 0.6 | ≥ 4 595 | +0 | 15,8 | +0,0 | 0,873 | — | ≥ : chaîne de puissance incomplètement chiffrée |
| releve | depuis le dos | ≥ 4 715 | +120 | 15,9 | +0,1 | 0,873 | — | ≥ : chaîne de puissance incomplètement chiffrée |
| releve | depuis le ventre | ≥ 4 715 | +0 | 15,9 | +0,0 | 0,873 | — | ≥ : chaîne de puissance incomplètement chiffrée |
| saut_vertical | 5 | ≥ 5 175 | +580 | 23,4 | +7,6 | 0,979 | — | ≥ : chaîne de puissance incomplètement chiffrée |
| saut_vertical | 10 | — | — | — | — | — | — | aucune faisable ; 178 INCONNUES (surtout : prix de BF1 58V Series, MIDI style 58V Slo-Blo bolt-down fuse (fusible)) |
| gestes_pointage | 0.5 | ≥ 4 595 | +0 | 15,8 | +0,0 | 0,873 | — | ≥ : chaîne de puissance incomplètement chiffrée |
| gestes_pointage | 1.0 | ≥ 4 595 | +0 | 15,8 | +0,0 | 0,873 | — | ≥ : chaîne de puissance incomplètement chiffrée |
| gestes_pointage | 2.0 | ≥ 4 540 | −55 | 16,3 | +0,5 | 0,901 | — | ≥ : chaîne de puissance incomplètement chiffrée |
| saisie | 0.2 | ≥ 4 558 | −37 | 16,2 | +0,4 | 0,873 | — | ≥ : chaîne de puissance incomplètement chiffrée |
| poussee | 20 | — | — | — | — | — | — | aucune faisable ; 206 INCONNUES (surtout : prix de RobStride Discharge Module (泄放模块, « bleeder module ») (regeneration)) |
| buste | lacet seul | ≥ 4 595 | +0 | 15,8 | +0,0 | 0,873 | — | ≥ : chaîne de puissance incomplètement chiffrée |
| tete | 2 | — | — | — | — | — | — | aucune faisable ; 207 INCONNUES (surtout : prix de RobStride Discharge Module (泄放模块, « bleeder module ») (regeneration)) |

## Données INCONNUES les plus bloquantes

Rangées par le nombre de solutions INCONNUES où elles manquent ; « seule » = solutions qui deviendraient décidables avec cette seule donnée.

| Donnée manquante | Solutions | Seule |
| --- | ---: | ---: |
| prix de RobStride Discharge Module (泄放模块, « bleeder module ») (regeneration) | 21126 | 356 |
| plage de tension d'un servo des petits axes : rail non choisi | 13356 | 0 |
| prix de RobStride Power Supply Board V1.3 (carte de distribution) (precharge) | 12732 | 0 |
| masse de RobStride Power Supply Board V1.3 (carte de distribution) (precharge) | 12732 | 0 |
| cotes de RobStride Power Supply Board V1.3 (carte de distribution) (precharge) | 12732 | 0 |
| courant de RobStride Power Supply Board V1.3 (carte de distribution) (precharge) | 12732 | 0 |
| tension de RobStride Power Supply Board V1.3 (carte de distribution) (precharge) | 12732 | 0 |
| couple continu de xl330_m077 | 10030 | 0 |
| prix de BF1 58V Series, MIDI style 58V Slo-Blo bolt-down fuse (fusible) | 8330 | 0 |
| masse de BF1 58V Series, MIDI style 58V Slo-Blo bolt-down fuse (fusible) | 8330 | 0 |
| cotes de BF1 58V Series, MIDI style 58V Slo-Blo bolt-down fuse (fusible) | 8330 | 0 |
| courant de BF1 58V Series, MIDI style 58V Slo-Blo bolt-down fuse (fusible) | 8330 | 0 |

Hors calcul pour toute solution (capacités jamais « tenues » ici) :

- **sol_irregulier** : simulation de marche sur obstacles de 2 et 4 cm : non faite
- **pente** : simulation de marche en pente de 5 et 10° : non faite
- **course** : aucune politique de course (phase 3b) : rien à mettre à l'échelle
- **mains_a_doigts** : aucun ensemble du Lab n'a de doigts
- **visage** : masse, prix et place d'un écran ou de micro-servos : non relevés
- **structure** : seule la jambe basse est dessinée ; les autres segments sont estimés par des formules étalonnées sur elle ; l'évidement est une borne haute ; l'alu 2 mm n'est pas confirmé chez l'opérateur.
- **place** : volume de l'électronique et de la batterie dans le tronc compté NUL ; cardan des bielles (b) supposé ; servos en boîtier pris dans leur plus grande cote.

## Système électrique : 12S, 250 / 500 Hz, tension de coupure en variante (phases 4a quinquies et sexies)

Contexte DÉCIDÉ : fiches 0070 (batterie), 0071 (Lab : autonomie 30 min sur le cycle 40 s de marche + 20 s debout, IA « commande + vision ») et 0072 (Jeremy, 2026-10-08 : « Je retiens le 12S pour les deux robots, sur les chiffres de l'explorateur du 7 octobre. »). La tension de COUPURE (seuil d'arrêt) est étudiée en variante : 2,5, 3,0 et 3,2 V par cellule. Tout le reste est PROPOSÉ (`params/puissance.yaml`) :

- puissance électrique = puissance mécanique MOYENNE de la marche simulée (phase 3b, |τ·ω|, le robot le plus exigeant qui couvre le Froude) ÷ rendement BAS 0,4 (bande 0,4–0,7), sur 40 s de 60 ; debout, puissance mécanique nulle et pertes de maintien NON comptées (sous-estimation, dite) ; plus le calculateur ;
- énergie = puissance moyenne × autonomie ÷ 0,9 (part utilisable) ; courant de pointe = Σ des pointes par axe (marche simulée et tâches directes du profil) ÷ rendement bas ÷ tension de COUPURE ;
- batterie : la composition S × P de cellules 21700 la plus LÉGÈRE du marché versé qui fournit l'énergie et dont le courant CONTINU publié tient la pointe ; masse × 1,3, volume des cylindres ÷ π/4 × 1,2 ;
- tension : chaque RobStride doit accepter le pack de la coupure à la pleine charge (plage publiée) ; sa vitesse à vide est ramenée à la tension de COUPURE, proportionnellement (hypothèse écrite ; fiche à 48 V) : ×0.625 à 2,5 V ; ×0.750 à 3,0 V ; ×0.800 à 3,2 V ; énergie au-dessus de la coupure : 2,5 V : 100 % ; 3,0 V : 85 % ; 3,2 V : 70 % de l'énergie nominale (PROPOSÉ, prudent : courbe de décharge non lue numériquement) ;
- calculateur : le moins cher qui convient au niveau d'IA (critères PROPOSÉS : commande seule : accélérateur non, ≥ 4 GB ; + vision : accélérateur oui, ≥ 4 GB ; + vision et voix : accélérateur oui, ≥ 8 GB ; + modèle de langage local : accélérateur oui, ≥ 16 GB, modèles de langage), carte porteuse comprise, alimenté par le rail 12 V (Raspberry Pi : 12 → 5 V) ;
- bus : canaux CAN au calcul écrit (`docs/marche-bus-2026-10.md`), au-delà de ceux du calculateur par l'adaptateur le moins cher à pilote Linux principal ; un adaptateur série Feetech ;
- chaîne de puissance et rails : `params/puissance.yaml` (cellules → fusible → sectionneur → BMS → contacteur → précharge → bus moteurs ; absorbeur de régénération ; arrêt d'urgence matériel ; rails 12, 7,4, 6 et 5 V). Masses et cotes non publiées : BORNES PROPOSÉES majorantes (`bornes_proposees`, justifiées une par une) ; une solution qui en use est marquée « bornes proposées », jamais « vérifiée » ;
- batterie : cellules NEUVES d'un distributeur identifié seulement (récupération, occasion, marque masquée écartées) ;
- place : batterie, calculateur, cartes et convertisseurs dans 50 % du tronc (largeur d'épaules × profondeur de poitrine × hauteur du tronc, ANSUR, à la hauteur réelle) ; ce qui dépasse ALLONGE le tronc (même lecture « avec écarts » que la place des moteurs).

**Référence, méthode de 14 h 05 recalculée (sans système électrique, charge utile forfaitaire de 1,2 kg)** : 27 axes, 0,50 → 0,557 m, 10,7 kg, 2 709 CHF (actionneurs seuls).

### Tension de coupure et tâches rapides (meilleure solution RobStride pour chaque tâche, marche au niveau du profil)

| Fréquence | Coupure (V/cellule) | saut 5 cm | saut 10 cm | gestes 2 m/s |
| ---: | ---: | --- | --- | --- |
| 250 Hz | 2,5 | tient : 25 axes, 0,985 m réels, 23,3 kg, ≥ 4 711 CHF | NE TIENT PAS (knee : aucun robstride ne tient (pointe #, continu # N·m, ω # rad/s, b bas, structure cent) | tient : 25 axes, 0,902 m réels, 16,2 kg, ≥ 4 076 CHF |
| 250 Hz | 3,0 | tient : 25 axes, 0,897 m réels, 18,6 kg, ≥ 4 534 CHF | NE TIENT PAS (knee : aucun robstride ne tient (pointe #, continu # N·m, ω # rad/s, b bas, structure cent) | tient : 25 axes, 0,903 m réels, 16,3 kg, ≥ 4 009 CHF |
| 250 Hz | 3,2 | tient : 25 axes, 0,897 m réels, 17,5 kg, ≥ 4 327 CHF | NE TIENT PAS (knee : aucun robstride ne tient (pointe #, continu # N·m, ω # rad/s, b bas, structure cent) | tient : 25 axes, 0,902 m réels, 16,2 kg, ≥ 4 076 CHF |
| 500 Hz | 2,5 | tient : 25 axes, 0,979 m réels, 23,4 kg, ≥ 5 175 CHF | NE TIENT PAS (knee : aucun robstride ne tient (pointe #, continu # N·m, ω # rad/s, b bas, structure cent) | tient : 25 axes, 0,901 m réels, 16,3 kg, ≥ 4 540 CHF |
| 500 Hz | 3,0 | tient : 25 axes, 1,071 m réels, 25,3 kg, ≥ 5 081 CHF | NE TIENT PAS (knee : aucun robstride ne tient (pointe #, continu # N·m, ω # rad/s, b bas, structure cent) | tient : 25 axes, 0,902 m réels, 16,4 kg, ≥ 4 473 CHF |
| 500 Hz | 3,2 | tient : 25 axes, 0,949 m réels, 22,0 kg, ≥ 5 099 CHF | NE TIENT PAS (knee : aucun robstride ne tient (pointe #, continu # N·m, ω # rad/s, b bas, structure cent) | tient : 25 axes, 0,901 m réels, 16,3 kg, ≥ 4 540 CHF |

### 12S, 250 Hz, coupure 2,5 V

73728 solutions : 0 faisables, 50958 infaisables, 22770 INCONNUES ; front de 0. Le front QUITTE la borne basse H = 0,50 m.

| Ensemble | H → réelle (m) | Corps + petits | Masse (kg) | Coût TOTAL (CHF HT) | dont actionneurs | Batterie | Calculateur | Canaux CAN | Statut |
| ---: | --- | --- | ---: | ---: | ---: | --- | --- | ---: | --- |
| 27 | 0,90 → 0,979 | cubemars + dynamixel | 24,1 | ≥ 11 137 | 9 030 | INR-21700-P50B 12S5P, 1 050 Wh, 5,54 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |
| 27 | 0,85 → 0,987 | cubemars + dynamixel | 24,2 | ≥ 11 137 | 9 030 | INR-21700-P50B 12S5P, 1 050 Wh, 5,54 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |
| 27 | 0,80 → 1,003 | cubemars + dynamixel | 24,3 | ≥ 11 137 | 9 030 | INR-21700-P50B 12S5P, 1 050 Wh, 5,54 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |
| 27 | 0,75 → 1,020 | cubemars + dynamixel | 24,5 | ≥ 11 137 | 9 030 | INR-21700-P50B 12S5P, 1 050 Wh, 5,54 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |
| 27 | 0,70 → 1,043 | cubemars + dynamixel | 24,8 | ≥ 11 137 | 9 030 | INR-21700-P50B 12S5P, 1 050 Wh, 5,54 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |

Meilleures solutions **RobStride** (famille des deux robots, fiche 0069), avec leurs capacités tenues :

| Ensemble | H → réelle (m) | Corps + petits | Masse (kg) | Coût TOTAL (CHF HT) | dont actionneurs | Batterie | Calculateur | Canaux CAN | Statut |
| ---: | --- | --- | ---: | ---: | ---: | --- | --- | ---: | --- |
| 27 | 0,85 → 0,861 | robstride + dynamixel | 16,8 | ≥ 4 380 | 3 119 | INR-21700-P50B 12S1P, 210 Wh, 1,11 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |
| 27 | 0,80 → 0,861 | robstride + dynamixel | 16,8 | ≥ 4 380 | 3 119 | INR-21700-P50B 12S1P, 210 Wh, 1,11 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |
| 27 | 0,75 → 0,868 | robstride + dynamixel | 16,8 | ≥ 4 380 | 3 119 | INR-21700-P50B 12S1P, 210 Wh, 1,11 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |

- RobStride n° 1 : marche_sol_plat, releve, gestes_pointage, saisie, buste, tete ; manque du profil : sol_irregulier, pente, saut_vertical, poussee, visage
- RobStride n° 2 : marche_sol_plat, releve, gestes_pointage, saisie, buste, tete ; manque du profil : sol_irregulier, pente, saut_vertical, poussee, visage
- RobStride n° 3 : marche_sol_plat, releve, gestes_pointage, saisie, buste, tete ; manque du profil : sol_irregulier, pente, saut_vertical, poussee, visage

Volume électronique de la meilleure RobStride (27 axes, H 0,85) : 3,34 L requis pour 3,21 L disponibles ; le tronc s'allonge de 11 mm.

| Élément | Volume (L) | Part |
| --- | ---: | ---: |
| bms : JK Smart Active Balance BMS B2A20S20P-HC | 0,968 | 29 % |
| contacteur : GV200PA, bobine 12 V | 0,562 | 17 % |
| batterie | 0,469 | 14 % |
| sectionneur : Battery switch ON/OFF 275A | 0,369 | 11 % |
| calculateur | 0,251 | 8 % |
| fusible : MEGA-Fuse fuse holder (porte-fusible MEG | 0,247 | 7 % |
| regeneration : RobStride Discharge Module (泄放模块, « blee | 0,240 | 7 % |
| arret_urgence : XA1E-BV302R, arrêt d'urgence Ø 16 mm, 2  | 0,096 | 3 % |
| cartes CAN | 0,071 | 2 % |
| precharge : AS150 (connecteur balle 7 mm anti-étince | 0,036 | 1 % |
| fusible : MEGA-fuse 58V/48V (125, 200, 225, 300 A) | 0,017 | 1 % |
| dcdc : D42V110F12 (12V, 9A Step-Down Voltage Re | 0,012 | 0 % |

Coût de chaque niveau d'autonomie et d'IA, pour la meilleure solution RobStride (27 axes, H 0,85, robstride + dynamixel, même profil) :

| Tâche | Niveau | Masse (kg) | Coût TOTAL (CHF HT) | Batterie | Calculateur | Hauteur réelle (m) | Statut |
| --- | --- | ---: | ---: | --- | --- | ---: | --- |
| autonomie | 10 | 16,8 | ≥ 4 380 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,861 | INCONNU |
| autonomie | 20 | 16,8 | ≥ 4 380 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,861 | INCONNU |
| autonomie | 30 | 16,8 | ≥ 4 380 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,861 | INCONNU |
| autonomie | 60 | 19,7 | ≥ 4 536 | 12S2P 353 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,900 | INCONNU |
| ia_embarquee | commande seule | 16,8 | ≥ 4 380 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,861 | INCONNU |
| ia_embarquee | + vision | 16,8 | ≥ 4 380 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,861 | INCONNU |
| ia_embarquee | + vision et voix | 16,8 | ≥ 4 380 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,861 | INCONNU |
| ia_embarquee | + modèle de langage local | 16,3 | ≥ 4 225 | 12S1P 210 Wh | Raspberry Pi 5 16GB + Raspberry Pi AI HAT+ 2 | 0,850 | INCONNU |

### 12S, 250 Hz, coupure 3,0 V

73728 solutions : 0 faisables, 40306 infaisables, 33422 INCONNUES ; front de 0. Le front QUITTE la borne basse H = 0,50 m.

| Ensemble | H → réelle (m) | Corps + petits | Masse (kg) | Coût TOTAL (CHF HT) | dont actionneurs | Batterie | Calculateur | Canaux CAN | Statut |
| ---: | --- | --- | ---: | ---: | ---: | --- | --- | ---: | --- |
| 27 | 0,85 → — | unitree + dynamixel | 36,7 | ≥ 30 164 | 28 087 | INR-21700-P50B 12S5P, 1 050 Wh, 5,54 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |
| 27 | 0,90 → — | unitree + dynamixel | 37,8 | ≥ 30 260 | 28 087 | INR-21700-P50B 12S6P, 1 260 Wh, 6,65 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |
| 27 | 0,80 → — | unitree + dynamixel | 38,1 | ≥ 30 260 | 28 087 | INR-21700-P50B 12S6P, 1 260 Wh, 6,65 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |
| 27 | 0,75 → — | unitree + dynamixel | 38,3 | ≥ 30 260 | 28 087 | INR-21700-P50B 12S6P, 1 260 Wh, 6,65 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |
| 27 | 0,70 → — | unitree + dynamixel | 38,7 | ≥ 30 260 | 28 087 | INR-21700-P50B 12S6P, 1 260 Wh, 6,65 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |

Meilleures solutions **RobStride** (famille des deux robots, fiche 0069), avec leurs capacités tenues :

| Ensemble | H → réelle (m) | Corps + petits | Masse (kg) | Coût TOTAL (CHF HT) | dont actionneurs | Batterie | Calculateur | Canaux CAN | Statut |
| ---: | --- | --- | ---: | ---: | ---: | --- | --- | ---: | --- |
| 27 | 0,85 → 0,861 | robstride + dynamixel | 17,8 | ≥ 4 487 | 3 226 | INR-21700-P50B 12S1P, 210 Wh, 1,11 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |
| 27 | 0,80 → 0,861 | robstride + dynamixel | 17,8 | ≥ 4 487 | 3 226 | INR-21700-P50B 12S1P, 210 Wh, 1,11 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |
| 27 | 0,75 → 0,868 | robstride + dynamixel | 17,9 | ≥ 4 487 | 3 226 | INR-21700-P50B 12S1P, 210 Wh, 1,11 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |

- RobStride n° 1 : marche_sol_plat, releve, gestes_pointage, saisie, poussee, buste, tete ; manque du profil : sol_irregulier, pente, saut_vertical, visage
- RobStride n° 2 : marche_sol_plat, releve, gestes_pointage, saisie, poussee, buste, tete ; manque du profil : sol_irregulier, pente, saut_vertical, visage
- RobStride n° 3 : marche_sol_plat, releve, gestes_pointage, saisie, poussee, buste, tete ; manque du profil : sol_irregulier, pente, saut_vertical, visage

Volume électronique de la meilleure RobStride (27 axes, H 0,85) : 3,34 L requis pour 3,21 L disponibles ; le tronc s'allonge de 11 mm.

| Élément | Volume (L) | Part |
| --- | ---: | ---: |
| bms : JK Smart Active Balance BMS B2A20S20P-HC | 0,968 | 29 % |
| contacteur : GV200PA, bobine 12 V | 0,562 | 17 % |
| batterie | 0,469 | 14 % |
| sectionneur : Battery switch ON/OFF 275A | 0,369 | 11 % |
| calculateur | 0,251 | 8 % |
| fusible : MEGA-Fuse fuse holder (porte-fusible MEG | 0,247 | 7 % |
| regeneration : RobStride Discharge Module (泄放模块, « blee | 0,240 | 7 % |
| arret_urgence : XA1E-BV302R, arrêt d'urgence Ø 16 mm, 2  | 0,096 | 3 % |
| cartes CAN | 0,071 | 2 % |
| precharge : AS150 (connecteur balle 7 mm anti-étince | 0,036 | 1 % |
| fusible : MEGA-fuse 58V/48V (125, 200, 225, 300 A) | 0,017 | 1 % |
| dcdc : D42V110F12 (12V, 9A Step-Down Voltage Re | 0,012 | 0 % |

Coût de chaque niveau d'autonomie et d'IA, pour la meilleure solution RobStride (27 axes, H 0,85, robstride + dynamixel, même profil) :

| Tâche | Niveau | Masse (kg) | Coût TOTAL (CHF HT) | Batterie | Calculateur | Hauteur réelle (m) | Statut |
| --- | --- | ---: | ---: | --- | --- | ---: | --- |
| autonomie | 10 | 17,8 | ≥ 4 487 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,861 | INCONNU |
| autonomie | 20 | 17,8 | ≥ 4 487 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,861 | INCONNU |
| autonomie | 30 | 17,8 | ≥ 4 487 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,861 | INCONNU |
| autonomie | 60 | 22,2 | ≥ 4 800 | 12S2P 420 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,898 | INCONNU |
| ia_embarquee | commande seule | 17,8 | ≥ 4 487 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,861 | INCONNU |
| ia_embarquee | + vision | 17,8 | ≥ 4 487 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,861 | INCONNU |
| ia_embarquee | + vision et voix | 17,8 | ≥ 4 487 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,861 | INCONNU |
| ia_embarquee | + modèle de langage local | 16,8 | ≥ 4 239 | 12S1P 176 Wh | Raspberry Pi 5 16GB + Raspberry Pi AI HAT+ 2 | 0,850 | INCONNU |

### 12S, 250 Hz, coupure 3,2 V

73728 solutions : 0 faisables, 39630 infaisables, 34098 INCONNUES ; front de 0. Le front QUITTE la borne basse H = 0,50 m.

| Ensemble | H → réelle (m) | Corps + petits | Masse (kg) | Coût TOTAL (CHF HT) | dont actionneurs | Batterie | Calculateur | Canaux CAN | Statut |
| ---: | --- | --- | ---: | ---: | ---: | --- | --- | ---: | --- |
| 27 | 0,90 → — | unitree + dynamixel | 36,7 | ≥ 30 164 | 28 087 | INR-21700-P50B 12S5P, 1 050 Wh, 5,54 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |
| 27 | 0,85 → — | unitree + dynamixel | 36,7 | ≥ 30 164 | 28 087 | INR-21700-P50B 12S5P, 1 050 Wh, 5,54 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |
| 27 | 0,80 → — | unitree + dynamixel | 36,8 | ≥ 30 164 | 28 087 | INR-21700-P50B 12S5P, 1 050 Wh, 5,54 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |
| 27 | 0,75 → — | unitree + dynamixel | 37,1 | ≥ 30 164 | 28 087 | INR-21700-P50B 12S5P, 1 050 Wh, 5,54 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |
| 27 | 0,70 → — | unitree + dynamixel | 37,4 | ≥ 30 164 | 28 087 | INR-21700-P50B 12S5P, 1 050 Wh, 5,54 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |

Meilleures solutions **RobStride** (famille des deux robots, fiche 0069), avec leurs capacités tenues :

| Ensemble | H → réelle (m) | Corps + petits | Masse (kg) | Coût TOTAL (CHF HT) | dont actionneurs | Batterie | Calculateur | Canaux CAN | Statut |
| ---: | --- | --- | ---: | ---: | ---: | --- | --- | ---: | --- |
| 27 | 0,85 → 0,861 | robstride + dynamixel | 17,8 | ≥ 4 487 | 3 226 | INR-21700-P50B 12S1P, 210 Wh, 1,11 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |
| 27 | 0,80 → 0,861 | robstride + dynamixel | 17,8 | ≥ 4 487 | 3 226 | INR-21700-P50B 12S1P, 210 Wh, 1,11 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |
| 27 | 0,75 → 0,868 | robstride + dynamixel | 17,9 | ≥ 4 487 | 3 226 | INR-21700-P50B 12S1P, 210 Wh, 1,11 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 3 | INCONNU (bornes proposées) |

- RobStride n° 1 : marche_sol_plat, releve, gestes_pointage, saisie, poussee, buste, tete ; manque du profil : sol_irregulier, pente, saut_vertical, visage
- RobStride n° 2 : marche_sol_plat, releve, gestes_pointage, saisie, poussee, buste, tete ; manque du profil : sol_irregulier, pente, saut_vertical, visage
- RobStride n° 3 : marche_sol_plat, releve, gestes_pointage, saisie, poussee, buste, tete ; manque du profil : sol_irregulier, pente, saut_vertical, visage

Volume électronique de la meilleure RobStride (27 axes, H 0,85) : 3,34 L requis pour 3,21 L disponibles ; le tronc s'allonge de 11 mm.

| Élément | Volume (L) | Part |
| --- | ---: | ---: |
| bms : JK Smart Active Balance BMS B2A20S20P-HC | 0,968 | 29 % |
| contacteur : GV200PA, bobine 12 V | 0,562 | 17 % |
| batterie | 0,469 | 14 % |
| sectionneur : Battery switch ON/OFF 275A | 0,369 | 11 % |
| calculateur | 0,251 | 8 % |
| fusible : MEGA-Fuse fuse holder (porte-fusible MEG | 0,247 | 7 % |
| regeneration : RobStride Discharge Module (泄放模块, « blee | 0,240 | 7 % |
| arret_urgence : XA1E-BV302R, arrêt d'urgence Ø 16 mm, 2  | 0,096 | 3 % |
| cartes CAN | 0,071 | 2 % |
| precharge : AS150 (connecteur balle 7 mm anti-étince | 0,036 | 1 % |
| fusible : MEGA-fuse 58V/48V (125, 200, 225, 300 A) | 0,017 | 1 % |
| dcdc : D42V110F12 (12V, 9A Step-Down Voltage Re | 0,012 | 0 % |

Coût de chaque niveau d'autonomie et d'IA, pour la meilleure solution RobStride (27 axes, H 0,85, robstride + dynamixel, même profil) :

| Tâche | Niveau | Masse (kg) | Coût TOTAL (CHF HT) | Batterie | Calculateur | Hauteur réelle (m) | Statut |
| --- | --- | ---: | ---: | --- | --- | ---: | --- |
| autonomie | 10 | 17,8 | ≥ 4 420 | 12S1P 176 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,861 | INCONNU |
| autonomie | 20 | 17,8 | ≥ 4 420 | 12S1P 176 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,861 | INCONNU |
| autonomie | 30 | 17,8 | ≥ 4 487 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,861 | INCONNU |
| autonomie | 60 | 24,9 | ≥ 4 963 | 12S3P 630 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,935 | INCONNU |
| ia_embarquee | commande seule | 17,8 | ≥ 4 487 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,861 | INCONNU |
| ia_embarquee | + vision | 17,8 | ≥ 4 487 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,861 | INCONNU |
| ia_embarquee | + vision et voix | 17,8 | ≥ 4 487 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,861 | INCONNU |
| ia_embarquee | + modèle de langage local | 16,8 | ≥ 4 239 | 12S1P 176 Wh | Raspberry Pi 5 16GB + Raspberry Pi AI HAT+ 2 | 0,850 | INCONNU |

### 12S, 500 Hz, coupure 2,5 V

73728 solutions : 0 faisables, 52602 infaisables, 21126 INCONNUES ; front de 0. Le front QUITTE la borne basse H = 0,50 m.

| Ensemble | H → réelle (m) | Corps + petits | Masse (kg) | Coût TOTAL (CHF HT) | dont actionneurs | Batterie | Calculateur | Canaux CAN | Statut |
| ---: | --- | --- | ---: | ---: | ---: | --- | --- | ---: | --- |
| 27 | 0,65 → 1,055 | cubemars + dynamixel | 25,6 | ≥ 11 804 | 9 030 | INR-21700-P50B 12S5P, 1 050 Wh, 5,54 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |
| 27 | 0,90 → 0,994 | cubemars + dynamixel | 24,5 | ≥ 11 834 | 9 030 | INR-21700-P50B 12S5P, 1 050 Wh, 5,54 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |
| 27 | 0,85 → 1,004 | cubemars + dynamixel | 24,6 | ≥ 11 834 | 9 030 | INR-21700-P50B 12S5P, 1 050 Wh, 5,54 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |
| 27 | 0,80 → 1,022 | cubemars + dynamixel | 24,8 | ≥ 11 834 | 9 030 | INR-21700-P50B 12S5P, 1 050 Wh, 5,54 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |
| 27 | 0,75 → 1,041 | cubemars + dynamixel | 25,0 | ≥ 11 834 | 9 030 | INR-21700-P50B 12S5P, 1 050 Wh, 5,54 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |

Meilleures solutions **RobStride** (famille des deux robots, fiche 0069), avec leurs capacités tenues :

| Ensemble | H → réelle (m) | Corps + petits | Masse (kg) | Coût TOTAL (CHF HT) | dont actionneurs | Batterie | Calculateur | Canaux CAN | Statut |
| ---: | --- | --- | ---: | ---: | ---: | --- | --- | ---: | --- |
| 27 | 0,85 → 0,878 | robstride + dynamixel | 17,2 | ≥ 5 077 | 3 119 | INR-21700-P50B 12S1P, 210 Wh, 1,11 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |
| 27 | 0,80 → 0,880 | robstride + dynamixel | 17,2 | ≥ 5 077 | 3 119 | INR-21700-P50B 12S1P, 210 Wh, 1,11 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |
| 27 | 0,75 → 0,890 | robstride + dynamixel | 17,3 | ≥ 5 077 | 3 119 | INR-21700-P50B 12S1P, 210 Wh, 1,11 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |

- RobStride n° 1 : marche_sol_plat, releve, gestes_pointage, saisie, buste, tete ; manque du profil : sol_irregulier, pente, saut_vertical, poussee, visage
- RobStride n° 2 : marche_sol_plat, releve, gestes_pointage, saisie, buste, tete ; manque du profil : sol_irregulier, pente, saut_vertical, poussee, visage
- RobStride n° 3 : marche_sol_plat, releve, gestes_pointage, saisie, buste, tete ; manque du profil : sol_irregulier, pente, saut_vertical, poussee, visage

Volume électronique de la meilleure RobStride (27 axes, H 0,85) : 3,55 L requis pour 3,21 L disponibles ; le tronc s'allonge de 28 mm.

| Élément | Volume (L) | Part |
| --- | ---: | ---: |
| bms : JK Smart Active Balance BMS B2A20S20P-HC | 0,968 | 27 % |
| contacteur : GV200PA, bobine 12 V | 0,562 | 16 % |
| batterie | 0,469 | 13 % |
| sectionneur : Battery switch ON/OFF 275A | 0,369 | 10 % |
| cartes CAN | 0,284 | 8 % |
| calculateur | 0,251 | 7 % |
| fusible : MEGA-Fuse fuse holder (porte-fusible MEG | 0,247 | 7 % |
| regeneration : RobStride Discharge Module (泄放模块, « blee | 0,240 | 7 % |
| arret_urgence : XA1E-BV302R, arrêt d'urgence Ø 16 mm, 2  | 0,096 | 3 % |
| precharge : AS150 (connecteur balle 7 mm anti-étince | 0,036 | 1 % |
| fusible : MEGA-fuse 58V/48V (125, 200, 225, 300 A) | 0,017 | 0 % |
| dcdc : D42V110F12 (12V, 9A Step-Down Voltage Re | 0,012 | 0 % |

Coût de chaque niveau d'autonomie et d'IA, pour la meilleure solution RobStride (27 axes, H 0,85, robstride + dynamixel, même profil) :

| Tâche | Niveau | Masse (kg) | Coût TOTAL (CHF HT) | Batterie | Calculateur | Hauteur réelle (m) | Statut |
| --- | --- | ---: | ---: | --- | --- | ---: | --- |
| autonomie | 10 | 17,2 | ≥ 5 077 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,878 | INCONNU |
| autonomie | 20 | 17,2 | ≥ 5 077 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,878 | INCONNU |
| autonomie | 30 | 17,2 | ≥ 5 077 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,878 | INCONNU |
| autonomie | 60 | 22,1 | ≥ 5 449 | 12S2P 372 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,915 | INCONNU |
| ia_embarquee | commande seule | 17,2 | ≥ 5 077 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,878 | INCONNU |
| ia_embarquee | + vision | 17,2 | ≥ 5 077 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,878 | INCONNU |
| ia_embarquee | + vision et voix | 17,2 | ≥ 5 077 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,878 | INCONNU |
| ia_embarquee | + modèle de langage local | 16,4 | ≥ 4 264 | 12S1P 210 Wh | Raspberry Pi 5 16GB + Raspberry Pi AI HAT+ 2 | 0,850 | INCONNU |

### 12S, 500 Hz, coupure 3,0 V

73728 solutions : 0 faisables, 42904 infaisables, 30824 INCONNUES ; front de 0. Le front QUITTE la borne basse H = 0,50 m.

| Ensemble | H → réelle (m) | Corps + petits | Masse (kg) | Coût TOTAL (CHF HT) | dont actionneurs | Batterie | Calculateur | Canaux CAN | Statut |
| ---: | --- | --- | ---: | ---: | ---: | --- | --- | ---: | --- |
| 27 | 0,90 → — | unitree + dynamixel | 38,2 | ≥ 30 957 | 28 087 | INR-21700-P50B 12S6P, 1 260 Wh, 6,65 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |
| 27 | 0,85 → — | unitree + dynamixel | 38,3 | ≥ 30 957 | 28 087 | INR-21700-P50B 12S6P, 1 260 Wh, 6,65 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |
| 27 | 0,80 → — | unitree + dynamixel | 38,5 | ≥ 30 957 | 28 087 | INR-21700-P50B 12S6P, 1 260 Wh, 6,65 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |
| 27 | 0,75 → — | unitree + dynamixel | 38,8 | ≥ 30 957 | 28 087 | INR-21700-P50B 12S6P, 1 260 Wh, 6,65 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |
| 27 | 0,70 → — | unitree + dynamixel | 39,3 | ≥ 30 957 | 28 087 | INR-21700-P50B 12S6P, 1 260 Wh, 6,65 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |

Meilleures solutions **RobStride** (famille des deux robots, fiche 0069), avec leurs capacités tenues :

| Ensemble | H → réelle (m) | Corps + petits | Masse (kg) | Coût TOTAL (CHF HT) | dont actionneurs | Batterie | Calculateur | Canaux CAN | Statut |
| ---: | --- | --- | ---: | ---: | ---: | --- | --- | ---: | --- |
| 27 | 0,85 → 0,878 | robstride + dynamixel | 18,2 | ≥ 5 184 | 3 226 | INR-21700-P50B 12S1P, 210 Wh, 1,11 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |
| 27 | 0,80 → 0,880 | robstride + dynamixel | 18,2 | ≥ 5 184 | 3 226 | INR-21700-P50B 12S1P, 210 Wh, 1,11 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |
| 27 | 0,75 → 0,890 | robstride + dynamixel | 18,3 | ≥ 5 184 | 3 226 | INR-21700-P50B 12S1P, 210 Wh, 1,11 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |

- RobStride n° 1 : marche_sol_plat, releve, gestes_pointage, saisie, poussee, buste, tete ; manque du profil : sol_irregulier, pente, saut_vertical, visage
- RobStride n° 2 : marche_sol_plat, releve, gestes_pointage, saisie, poussee, buste, tete ; manque du profil : sol_irregulier, pente, saut_vertical, visage
- RobStride n° 3 : marche_sol_plat, releve, gestes_pointage, saisie, poussee, buste, tete ; manque du profil : sol_irregulier, pente, saut_vertical, visage

Volume électronique de la meilleure RobStride (27 axes, H 0,85) : 3,55 L requis pour 3,21 L disponibles ; le tronc s'allonge de 28 mm.

| Élément | Volume (L) | Part |
| --- | ---: | ---: |
| bms : JK Smart Active Balance BMS B2A20S20P-HC | 0,968 | 27 % |
| contacteur : GV200PA, bobine 12 V | 0,562 | 16 % |
| batterie | 0,469 | 13 % |
| sectionneur : Battery switch ON/OFF 275A | 0,369 | 10 % |
| cartes CAN | 0,284 | 8 % |
| calculateur | 0,251 | 7 % |
| fusible : MEGA-Fuse fuse holder (porte-fusible MEG | 0,247 | 7 % |
| regeneration : RobStride Discharge Module (泄放模块, « blee | 0,240 | 7 % |
| arret_urgence : XA1E-BV302R, arrêt d'urgence Ø 16 mm, 2  | 0,096 | 3 % |
| precharge : AS150 (connecteur balle 7 mm anti-étince | 0,036 | 1 % |
| fusible : MEGA-fuse 58V/48V (125, 200, 225, 300 A) | 0,017 | 0 % |
| dcdc : D42V110F12 (12V, 9A Step-Down Voltage Re | 0,012 | 0 % |

Coût de chaque niveau d'autonomie et d'IA, pour la meilleure solution RobStride (27 axes, H 0,85, robstride + dynamixel, même profil) :

| Tâche | Niveau | Masse (kg) | Coût TOTAL (CHF HT) | Batterie | Calculateur | Hauteur réelle (m) | Statut |
| --- | --- | ---: | ---: | --- | --- | ---: | --- |
| autonomie | 10 | 18,2 | ≥ 5 184 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,878 | INCONNU |
| autonomie | 20 | 18,2 | ≥ 5 184 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,878 | INCONNU |
| autonomie | 30 | 18,2 | ≥ 5 184 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,878 | INCONNU |
| autonomie | 60 | 25,3 | ≥ 5 458 | 12S3P 529 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,953 | INCONNU |
| ia_embarquee | commande seule | 18,2 | ≥ 5 184 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,878 | INCONNU |
| ia_embarquee | + vision | 18,2 | ≥ 5 184 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,878 | INCONNU |
| ia_embarquee | + vision et voix | 18,2 | ≥ 5 184 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,878 | INCONNU |
| ia_embarquee | + modèle de langage local | 16,8 | ≥ 4 279 | 12S1P 176 Wh | Raspberry Pi 5 16GB + Raspberry Pi AI HAT+ 2 | 0,850 | INCONNU |

### 12S, 500 Hz, coupure 3,2 V

73728 solutions : 0 faisables, 41700 infaisables, 32028 INCONNUES ; front de 0. Le front QUITTE la borne basse H = 0,50 m.

| Ensemble | H → réelle (m) | Corps + petits | Masse (kg) | Coût TOTAL (CHF HT) | dont actionneurs | Batterie | Calculateur | Canaux CAN | Statut |
| ---: | --- | --- | ---: | ---: | ---: | --- | --- | ---: | --- |
| 27 | 0,90 → — | unitree + dynamixel | 37,1 | ≥ 30 861 | 28 087 | INR-21700-P50B 12S5P, 1 050 Wh, 5,54 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |
| 27 | 0,85 → — | unitree + dynamixel | 37,1 | ≥ 30 861 | 28 087 | INR-21700-P50B 12S5P, 1 050 Wh, 5,54 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |
| 27 | 0,80 → — | unitree + dynamixel | 37,3 | ≥ 30 861 | 28 087 | INR-21700-P50B 12S5P, 1 050 Wh, 5,54 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |
| 27 | 0,75 → — | unitree + dynamixel | 37,5 | ≥ 30 861 | 28 087 | INR-21700-P50B 12S5P, 1 050 Wh, 5,54 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |
| 27 | 0,70 → — | unitree + dynamixel | 38,0 | ≥ 30 861 | 28 087 | INR-21700-P50B 12S5P, 1 050 Wh, 5,54 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |

Meilleures solutions **RobStride** (famille des deux robots, fiche 0069), avec leurs capacités tenues :

| Ensemble | H → réelle (m) | Corps + petits | Masse (kg) | Coût TOTAL (CHF HT) | dont actionneurs | Batterie | Calculateur | Canaux CAN | Statut |
| ---: | --- | --- | ---: | ---: | ---: | --- | --- | ---: | --- |
| 27 | 0,70 → 0,940 | robstride + dynamixel | 23,7 | ≥ 5 359 | 3 435 | INR-21700-P42A 12S2P, 353 Wh, 2,18 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |
| 27 | 0,75 → 0,928 | robstride + dynamixel | 23,7 | ≥ 5 359 | 3 435 | INR-21700-P42A 12S2P, 353 Wh, 2,18 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |
| 27 | 0,90 → 0,916 | robstride + dynamixel | 22,6 | ≥ 5 362 | 3 438 | INR-21700-P42A 12S2P, 353 Wh, 2,18 kg | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 6 | INCONNU (bornes proposées) |

- RobStride n° 1 : marche_sol_plat, releve, gestes_pointage, saisie, poussee, buste, tete ; manque du profil : sol_irregulier, pente, saut_vertical, visage
- RobStride n° 2 : marche_sol_plat, releve, gestes_pointage, saisie, poussee, buste, tete ; manque du profil : sol_irregulier, pente, saut_vertical, visage
- RobStride n° 3 : marche_sol_plat, releve, gestes_pointage, saisie, poussee, buste, tete ; manque du profil : sol_irregulier, pente, saut_vertical, visage

Volume électronique de la meilleure RobStride (27 axes, H 0,70) : 4,03 L requis pour 2,20 L disponibles ; le tronc s'allonge de 190 mm.

| Élément | Volume (L) | Part |
| --- | ---: | ---: |
| bms : JK Smart Active Balance BMS B2A20S20P-HC | 0,968 | 24 % |
| batterie | 0,952 | 24 % |
| contacteur : GV200PA, bobine 12 V | 0,562 | 14 % |
| sectionneur : Battery switch ON/OFF 275A | 0,369 | 9 % |
| cartes CAN | 0,284 | 7 % |
| calculateur | 0,251 | 6 % |
| fusible : MEGA-Fuse fuse holder (porte-fusible MEG | 0,247 | 6 % |
| regeneration : RobStride Discharge Module (泄放模块, « blee | 0,240 | 6 % |
| arret_urgence : XA1E-BV302R, arrêt d'urgence Ø 16 mm, 2  | 0,096 | 2 % |
| precharge : AS150 (connecteur balle 7 mm anti-étince | 0,036 | 1 % |
| fusible : MEGA-fuse 58V/48V (125, 200, 225, 300 A) | 0,017 | 0 % |
| dcdc : D42V110F12 (12V, 9A Step-Down Voltage Re | 0,012 | 0 % |

Coût de chaque niveau d'autonomie et d'IA, pour la meilleure solution RobStride (27 axes, H 0,70, robstride + dynamixel, même profil) :

| Tâche | Niveau | Masse (kg) | Coût TOTAL (CHF HT) | Batterie | Calculateur | Hauteur réelle (m) | Statut |
| --- | --- | ---: | ---: | --- | --- | ---: | --- |
| autonomie | 10 | 21,3 | ≥ 5 396 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,888 | INCONNU |
| autonomie | 20 | 21,3 | ≥ 5 396 | 12S1P 210 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,888 | INCONNU |
| autonomie | 30 | 23,7 | ≥ 5 359 | 12S2P 353 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,940 | INCONNU |
| autonomie | 60 | 25,7 | ≥ 5 660 | 12S3P 630 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,982 | INCONNU |
| ia_embarquee | commande seule | 23,7 | ≥ 5 359 | 12S2P 353 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,940 | INCONNU |
| ia_embarquee | + vision | 23,7 | ≥ 5 359 | 12S2P 353 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,940 | INCONNU |
| ia_embarquee | + vision et voix | 23,7 | ≥ 5 359 | 12S2P 353 Wh | Seeed reComputer Mini J3011 (Orin Nano 8 GB inclus) | 0,940 | INCONNU |
| ia_embarquee | + modèle de langage local | 16,8 | ≥ 4 279 | 12S1P 176 Wh | Raspberry Pi 5 16GB + Raspberry Pi AI HAT+ 2 | 0,846 | INCONNU |

### Vitesse des RobStride à la tension de coupure

- 12S, coupure 2,5 V : le plus rapide des RobStride compatibles, rs05, tourne à 31,4 rad/s à la coupure ; le saut de 10 cm demande jusqu'à 37,0 rad/s à H = 0,50 m (borne haute : rampe linéaire). Le saut est donc HORS de portée des RobStride dans cette variante.
- 12S, coupure 3,0 V : le plus rapide des RobStride compatibles, rs05, tourne à 37,7 rad/s à la coupure ; le saut de 10 cm demande jusqu'à 37,0 rad/s à H = 0,50 m (borne haute : rampe linéaire). Il passe.
- 12S, coupure 3,2 V : le plus rapide des RobStride compatibles, rs05, tourne à 40,2 rad/s à la coupure ; le saut de 10 cm demande jusqu'à 37,0 rad/s à H = 0,50 m (borne haute : rampe linéaire). Il passe.

Deux hypothèses rendent ce verrou prudent : la vitesse à vide prise à la tension de COUPURE (et non nominale), et la vitesse du saut en rampe linéaire. Elles sont écrites ; c'est à Jeremy de dire si l'une doit être assouplie.

### Canaux CAN (27 axes ; 23 sur CAN, le cou et les pinces étant en Feetech)

| Fréquence | Protocole | 27 axes | 23 axes |
| ---: | --- | ---: | ---: |
| 250 Hz | MIT (trame standard) | 3 | 3 |
| 250 Hz | privé (trame étendue) | 4 | 3 |
| 500 Hz | MIT (trame standard) | 6 | 5 |
| 500 Hz | privé (trame étendue) | 7 | 6 |
