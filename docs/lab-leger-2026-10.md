# Un YXOR Lab léger, pour apprendre à marcher (2026-10)

**Engendré** par `.venv/bin/python scripts/lab_leger.py --ecrire`. **Étude, AUCUNE décision** : le profil `lab_leger` (`params/capacites.yaml`) est un CANDIDAT PROPOSÉ ; il ne remplace pas le profil lab.

Question de Jeremy (2026-10-08) : « Est-ce que l'étude et ce que nous avions déterminé pour YXOR Lab ne représente-t-il pas mieux YXOR Home finalement ? Est-ce qu'il n'existerait pas une meilleure version de YXOR Lab plus optimisée et compatible avec YXOR Kit ? »

Profil : marche sur sol plat 0,10, 0,15 ou 0,3 m/s, relevé sur le dos et sur le ventre, gestes 0,5 m/s, tête à 2 axes, IA « + vision », autonomie 20 min (la plus exigeante de 10 et 20). Hors profil : saut, poussée, saisie, sol irrégulier, pente. Méthode : en tête de `scripts/lab_leger.py`.

## En bref

- **Marge 1,5** : aucune famille ne tient la marche entre 0,35 et 0,65 m.
- **Marge 1,0** : aucune famille ne tient la marche entre 0,35 et 0,65 m.
- **Retiré le 2026-10-09 : « Feetech en carton tient à la marge 1,0 »** (version du 2026-10-08). Ce résultat reposait sur la vitesse INCONNUE du STS3250 au catalogue de l'explorateur, et la règle comptait INCONNU comme « tient ». Désormais : la vitesse du STS3250 vient de sa fiche candidate (7,9 rad/s), et une donnée critique d'actionneur manquante (vitesse, couple continu) donne INCONNU, jamais « tient ».
- **Les vitesses requises viennent de marches simulées plus rapides que la vitesse étudiée** (section « Marcher lentement ») : à 0,10, 0,15 et 0,30 m/s, aucune marche simulée n'existe à cette taille ; la règle de l'explorateur prend la plus exigeante des marches au moins aussi rapides (G1, 0,55 m/s).
- **Robot entier avec la règle « plus_lente »** (PROPOSÉE, NON adoptée, section dédiée) : à la marge 1,5, rien ne tient ; à la marge 1,0, seuls A en carton (STS3250 aux jambes) et B en carton (RS05/EduLite05) tiennent.
- **Le Lab actuel** (« Home candidat ») : 0,850 m, 18,5 kg, ≥ 4 514 CHF, 87 J à la chute.

## La plus petite H où la marche tient, par famille

« Tient » : faisable, ou INCONNU seulement par les bornes proposées du système électrique (communes à toutes les solutions), toutes capacités couvertes ; une donnée critique d'actionneur manquante (vitesse, couple continu) donne INCONNU, jamais « tient » (règle du 2026-10-09). Besoins de marche : règle de l'explorateur (voir « Marcher lentement »). Coût : borne basse, CHF HT (prix connus seulement). Énergie de chute : M·g·hauteur du centre de gravité. Part du Kit : coût connu de l'option progressive (`scripts/kit.py`) qui resservirait.

| Marge | Jambes | Structure | Marche (m/s) | H → réelle (m) | Masse (kg) | Coût (CHF) | Chute (J) | Statut | Part du Kit réutilisée | Ce qui resservirait |
| ---: | --- | --- | ---: | --- | ---: | ---: | ---: | --- | ---: | --- |
| 1,5 | feetech | alu 2 mm évidé | 0,10 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : knee) | — | — | — | — | — | — |
| 1,5 | feetech | alu 2 mm évidé | 0,15 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : knee) | — | — | — | — | — | — |
| 1,5 | feetech | alu 2 mm évidé | 0,30 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : knee) | — | — | — | — | — | — |
| 1,5 | feetech | carton | 0,10 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : knee) | — | — | — | — | — | — |
| 1,5 | feetech | carton | 0,15 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : knee) | — | — | — | — | — | — |
| 1,5 | feetech | carton | 0,30 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : knee) | — | — | — | — | — | — |
| 1,5 | dynamixel | alu 2 mm évidé | 0,10 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, knee) | — | — | — | — | — | — |
| 1,5 | dynamixel | alu 2 mm évidé | 0,15 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, knee) | — | — | — | — | — | — |
| 1,5 | dynamixel | alu 2 mm évidé | 0,30 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, knee) | — | — | — | — | — | — |
| 1,5 | dynamixel | carton | 0,10 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : ankle_pitch, knee) | — | — | — | — | — | — |
| 1,5 | dynamixel | carton | 0,15 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : ankle_pitch, knee) | — | — | — | — | — | — |
| 1,5 | dynamixel | carton | 0,30 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : ankle_pitch, knee) | — | — | — | — | — | — |
| 1,5 | robstride | alu 2 mm évidé | 0,10 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |
| 1,5 | robstride | alu 2 mm évidé | 0,15 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |
| 1,5 | robstride | alu 2 mm évidé | 0,30 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |
| 1,5 | robstride | carton | 0,10 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |
| 1,5 | robstride | carton | 0,15 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |
| 1,5 | robstride | carton | 0,30 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |
| 1,0 | feetech | alu 2 mm évidé | 0,10 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : knee) | — | — | — | — | — | — |
| 1,0 | feetech | alu 2 mm évidé | 0,15 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : knee) | — | — | — | — | — | — |
| 1,0 | feetech | alu 2 mm évidé | 0,30 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : knee) | — | — | — | — | — | — |
| 1,0 | feetech | carton | 0,10 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : knee) | — | — | — | — | — | — |
| 1,0 | feetech | carton | 0,15 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : knee) | — | — | — | — | — | — |
| 1,0 | feetech | carton | 0,30 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : knee) | — | — | — | — | — | — |
| 1,0 | dynamixel | alu 2 mm évidé | 0,10 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : ankle_pitch, knee) | — | — | — | — | — | — |
| 1,0 | dynamixel | alu 2 mm évidé | 0,15 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : ankle_pitch, knee) | — | — | — | — | — | — |
| 1,0 | dynamixel | alu 2 mm évidé | 0,30 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : ankle_pitch, knee) | — | — | — | — | — | — |
| 1,0 | dynamixel | carton | 0,10 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : ankle_pitch, knee) | — | — | — | — | — | — |
| 1,0 | dynamixel | carton | 0,15 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : ankle_pitch, knee) | — | — | — | — | — | — |
| 1,0 | dynamixel | carton | 0,30 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : ankle_pitch, knee) | — | — | — | — | — | — |
| 1,0 | robstride | alu 2 mm évidé | 0,10 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |
| 1,0 | robstride | alu 2 mm évidé | 0,15 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |
| 1,0 | robstride | alu 2 mm évidé | 0,30 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |
| 1,0 | robstride | carton | 0,10 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |
| 1,0 | robstride | carton | 0,15 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |
| 1,0 | robstride | carton | 0,30 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |

## La moins chère par famille (marche 0,3 m/s) : le prix de chaque famille

| Marge | Jambes | Structure | H → réelle (m) | Masse (kg) | Coût (CHF) | Chute (J) | Actionneurs des jambes |
| ---: | --- | --- | --- | ---: | ---: | ---: | --- |

## Marcher lentement : les besoins par articulation (H = 0,60 m, 3,45 kg)

Les trois marches simulées, ramenées à 0,60 m : ToddlerBot à 0,196 m/s ; Unitree G1 à 0,547 m/s ; Booster T1 à 0,690 m/s. **Aucune ne va à 0,10, 0,15 ou 0,30 m/s** : à ces vitesses, la donnée est null et le statut INCONNU. Deux lectures sont montrées, sans interpolation : la règle de l'explorateur (le maximum des marches au moins aussi rapides) et la marche la plus lente au moins aussi rapide (une borne haute). Les autres tâches du profil (relevé, gestes, tête) s'ajoutent (maximum par axe).

| Vitesse (m/s) | Lecture | Source | Genou : pointe (N·m), vitesse (rad/s) | Cheville : pointe, vitesse | Tangage de hanche : pointe, vitesse |
| ---: | --- | --- | --- | --- | --- |
| 0,10 | donnée à cette vitesse | aucune | null (INCONNU) | null (INCONNU) | null (INCONNU) |
| 0,10 | règle de l'explorateur | ToddlerBot (0.196 m/s), Unitree G1 (0.547 m/s), Booster T1 (0.690 m/s) | 2,90, 14,1 | 2,35, 18,2 | 2,72, 6,0 |
| 0,10 | la plus lente au-dessus (borne) | ToddlerBot (0.196 m/s) | 2,03, 4,6 | 2,35, 2,5 | 2,35, 3,4 |
| 0,15 | donnée à cette vitesse | aucune | null (INCONNU) | null (INCONNU) | null (INCONNU) |
| 0,15 | règle de l'explorateur | ToddlerBot (0.196 m/s), Unitree G1 (0.547 m/s), Booster T1 (0.690 m/s) | 2,90, 14,1 | 2,35, 18,2 | 2,72, 6,0 |
| 0,15 | la plus lente au-dessus (borne) | ToddlerBot (0.196 m/s) | 2,03, 4,6 | 2,35, 2,5 | 2,35, 3,4 |
| 0,30 | donnée à cette vitesse | aucune | null (INCONNU) | null (INCONNU) | null (INCONNU) |
| 0,30 | règle de l'explorateur | Unitree G1 (0.547 m/s), Booster T1 (0.690 m/s) | 2,90, 14,1 | 1,11, 18,2 | 2,72, 6,0 |
| 0,30 | la plus lente au-dessus (borne) | Unitree G1 (0.547 m/s) | 2,90, 14,1 | 1,11, 18,2 | 2,72, 5,7 |

**0,15 m/s reprend-elle un niveau voisin ?** Avec la règle de l'explorateur, OUI pour les vitesses : les vitesses requises sont identiques à celles de 0,30 m/s, parce que le maximum inclut le G1 et le T1, qui marchent bien plus vite (0,55 et 0,69 m/s à cette taille) ; seuls des couples diffèrent (ceux de ToddlerBot, plus forts à la cheville). La borne « la plus lente au-dessus » donne, elle, les besoins de ToddlerBot (0,196 m/s) à 0,10 et 0,15 m/s.

### Verdict par actionneur, même actionneur sur les cinq axes de jambe (marge 1,5 sur le couple)

| Actionneur | 0,10 m/s (borne) | 0,15 m/s (borne) | 0,30 m/s (borne) | ToddlerBot (0,196 m/s, donnée) | Unitree G1 (0,547 m/s, donnée) | Booster T1 (0,690 m/s, donnée) |
| --- | --- | --- | --- | --- | --- | --- |
| sts3215_c018 (Feetech, 12 V) | INCONNU (au-dessus de la borne) | INCONNU (au-dessus de la borne) | INCONNU (au-dessus de la borne) | ne tient pas | ne tient pas | ne tient pas |
| sts3250 (Feetech, 12 V) | tient (sous la borne) | tient (sous la borne) | INCONNU (au-dessus de la borne) | tient | ne tient pas | ne tient pas |
| HTD-85H (Hiwonder, 11.1 V) | INCONNU (donnée d'actionneur manquante) | INCONNU (donnée d'actionneur manquante) | INCONNU (au-dessus de la borne) | INCONNU (donnée d'actionneur manquante) | ne tient pas | ne tient pas |
| RSBL120-24 (Waveshare, ?) | INCONNU (donnée d'actionneur manquante) | INCONNU (donnée d'actionneur manquante) | INCONNU (au-dessus de la borne) | INCONNU (donnée d'actionneur manquante) | ne tient pas | ne tient pas |
| KRS-9304HV ICS (Kondo, 11.1 V) | INCONNU (au-dessus de la borne) | INCONNU (au-dessus de la borne) | INCONNU (au-dessus de la borne) | ne tient pas | ne tient pas | ne tient pas |
| DRS-0601 (HerkuleX, 14.8 V) | INCONNU (donnée d'actionneur manquante) | INCONNU (donnée d'actionneur manquante) | INCONNU (au-dessus de la borne) | INCONNU (donnée d'actionneur manquante) | ne tient pas | ne tient pas |
| LSS-HT1 (Lynxmotion LSS, 12 V) | INCONNU (au-dessus de la borne) | INCONNU (au-dessus de la borne) | INCONNU (au-dessus de la borne) | ne tient pas | ne tient pas | ne tient pas |
| RS305CR (Futaba RS (commande), ?) | INCONNU (au-dessus de la borne) | INCONNU (au-dessus de la borne) | INCONNU (au-dessus de la borne) | ne tient pas | ne tient pas | ne tient pas |
| UBT-12HC (servo de l’Alpha 1S) (UBTECH, 8.5 V) | INCONNU (au-dessus de la borne) | INCONNU (au-dessus de la borne) | INCONNU (au-dessus de la borne) | ne tient pas | ne tient pas | ne tient pas |
| rs05 (RobStride, 12S, 3,0 V/cellule) | tient (sous la borne) | tient (sous la borne) | INCONNU (au-dessus de la borne) | tient | ne tient pas | ne tient pas |
| edulite05 (RobStride, 12S, 3,0 V/cellule) | tient (sous la borne) | tient (sous la borne) | INCONNU (au-dessus de la borne) | tient | ne tient pas | tient |

### Verdict par actionneur, même actionneur sur les cinq axes de jambe (marge 1,0 sur le couple)

| Actionneur | 0,10 m/s (borne) | 0,15 m/s (borne) | 0,30 m/s (borne) | ToddlerBot (0,196 m/s, donnée) | Unitree G1 (0,547 m/s, donnée) | Booster T1 (0,690 m/s, donnée) |
| --- | --- | --- | --- | --- | --- | --- |
| sts3215_c018 (Feetech, 12 V) | INCONNU (au-dessus de la borne) | INCONNU (au-dessus de la borne) | INCONNU (au-dessus de la borne) | ne tient pas | ne tient pas | ne tient pas |
| sts3250 (Feetech, 12 V) | tient (sous la borne) | tient (sous la borne) | INCONNU (au-dessus de la borne) | tient | ne tient pas | ne tient pas |
| HTD-85H (Hiwonder, 11.1 V) | INCONNU (donnée d'actionneur manquante) | INCONNU (donnée d'actionneur manquante) | INCONNU (au-dessus de la borne) | INCONNU (donnée d'actionneur manquante) | ne tient pas | ne tient pas |
| RSBL120-24 (Waveshare, ?) | INCONNU (donnée d'actionneur manquante) | INCONNU (donnée d'actionneur manquante) | INCONNU (au-dessus de la borne) | INCONNU (donnée d'actionneur manquante) | ne tient pas | ne tient pas |
| KRS-9304HV ICS (Kondo, 11.1 V) | INCONNU (au-dessus de la borne) | INCONNU (au-dessus de la borne) | INCONNU (au-dessus de la borne) | ne tient pas | ne tient pas | ne tient pas |
| DRS-0601 (HerkuleX, 14.8 V) | INCONNU (donnée d'actionneur manquante) | INCONNU (donnée d'actionneur manquante) | INCONNU (au-dessus de la borne) | INCONNU (donnée d'actionneur manquante) | ne tient pas | ne tient pas |
| LSS-HT1 (Lynxmotion LSS, 12 V) | INCONNU (au-dessus de la borne) | INCONNU (au-dessus de la borne) | INCONNU (au-dessus de la borne) | ne tient pas | ne tient pas | ne tient pas |
| RS305CR (Futaba RS (commande), ?) | INCONNU (au-dessus de la borne) | INCONNU (au-dessus de la borne) | INCONNU (au-dessus de la borne) | ne tient pas | ne tient pas | ne tient pas |
| UBT-12HC (servo de l’Alpha 1S) (UBTECH, 8.5 V) | INCONNU (au-dessus de la borne) | INCONNU (au-dessus de la borne) | INCONNU (au-dessus de la borne) | ne tient pas | ne tient pas | ne tient pas |
| rs05 (RobStride, 12S, 3,0 V/cellule) | tient (sous la borne) | tient (sous la borne) | tient (sous la borne) | tient | tient | tient |
| edulite05 (RobStride, 12S, 3,0 V/cellule) | tient (sous la borne) | tient (sous la borne) | tient (sous la borne) | tient | tient | tient |

### Marges à 0,10 m/s (borne : ToddlerBot (0.196 m/s)) : couple de pointe / couple continu / vitesse

Chaque case : rapport « publié ÷ requis » ; le couple doit atteindre la marge (1,5 ou 1,0), la vitesse 1,0. « — » : donnée non publiée (INCONNU).

| Axe | Requis : pointe, continu (N·m), vitesse (rad/s) | sts3215_c018 | sts3250 | HTD-85H | RSBL120-24 | KRS-9304HV ICS | DRS-0601 | LSS-HT1 | RS305CR | UBT-12HC (servo de l’Alpha 1S) | rs05 | edulite05 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hip_pitch | 2,35, 0,70, 3,4 (marche) | 1,25 / 1,40 / 1,39 | 2,08 / 2,24 / 2,31 | 3,54 / — / 1,54 | 5,00 / — / 1,54 | 3,79 / — / 1,34 | 3,21 / — / 1,92 | 1,21 / 0,81 / 1,85 | 0,30 / — / 2,80 | 0,50 / — / 1,55 | 2,34 / 2,28 / 11,08 | 2,34 / 2,56 / 9,93 |
| hip_roll | 2,34, 0,94, 2,2 (marche) | 1,26 / 1,05 / 2,11 | 2,09 / 1,68 / 3,53 | 3,56 / — / 2,35 | 5,02 / — / 2,35 | 3,80 / — / 2,04 | 3,22 / — / 2,94 | 1,21 / 0,61 / 2,82 | 0,30 / — / 4,27 | 0,50 / — / 2,37 | 2,35 / 1,71 / 16,91 | 2,35 / 1,92 / 15,14 |
| hip_yaw | 1,12, 0,32, 2,5 (marche) | 2,63 / 3,09 / 1,89 | 4,38 / 4,95 / 3,15 | 7,44 / — / 2,10 | 10,51 / — / 2,10 | 7,96 / — / 1,82 | 6,74 / — / 2,62 | 2,54 / 1,79 / 2,52 | 0,62 / — / 3,81 | 1,05 / — / 2,12 | 4,91 / 5,04 / 15,10 | 4,91 / 5,67 / 13,52 |
| knee | 2,03, 0,52, 4,6 (marche) | 1,45 / 1,89 / 1,03 | 2,42 / 3,02 / 1,72 | 4,11 / — / 1,14 | 5,80 / — / 1,14 | 4,40 / — / 0,99 | 3,72 / — / 1,43 | 1,40 / 1,09 / 1,37 | 0,34 / — / 2,07 | 0,58 / — / 1,15 | 2,71 / 3,08 / 8,21 | 2,71 / 3,46 / 7,36 |
| ankle_pitch | 2,35, 0,99, 2,5 (marche) | 1,25 / 1,00 / 1,87 | 2,08 / 1,59 / 3,12 | 3,54 / — / 2,08 | 5,00 / — / 2,08 | 3,79 / — / 1,80 | 3,21 / — / 2,59 | 1,21 / 0,58 / 2,49 | 0,30 / — / 3,77 | 0,50 / — / 2,10 | 2,34 / 1,62 / 14,94 | 2,34 / 1,83 / 13,39 |

### Marges à 0,15 m/s (borne : ToddlerBot (0.196 m/s)) : couple de pointe / couple continu / vitesse

Chaque case : rapport « publié ÷ requis » ; le couple doit atteindre la marge (1,5 ou 1,0), la vitesse 1,0. « — » : donnée non publiée (INCONNU).

| Axe | Requis : pointe, continu (N·m), vitesse (rad/s) | sts3215_c018 | sts3250 | HTD-85H | RSBL120-24 | KRS-9304HV ICS | DRS-0601 | LSS-HT1 | RS305CR | UBT-12HC (servo de l’Alpha 1S) | rs05 | edulite05 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hip_pitch | 2,35, 0,70, 3,4 (marche) | 1,25 / 1,40 / 1,39 | 2,08 / 2,24 / 2,31 | 3,54 / — / 1,54 | 5,00 / — / 1,54 | 3,79 / — / 1,34 | 3,21 / — / 1,92 | 1,21 / 0,81 / 1,85 | 0,30 / — / 2,80 | 0,50 / — / 1,55 | 2,34 / 2,28 / 11,08 | 2,34 / 2,56 / 9,93 |
| hip_roll | 2,34, 0,94, 2,2 (marche) | 1,26 / 1,05 / 2,11 | 2,09 / 1,68 / 3,53 | 3,56 / — / 2,35 | 5,02 / — / 2,35 | 3,80 / — / 2,04 | 3,22 / — / 2,94 | 1,21 / 0,61 / 2,82 | 0,30 / — / 4,27 | 0,50 / — / 2,37 | 2,35 / 1,71 / 16,91 | 2,35 / 1,92 / 15,14 |
| hip_yaw | 1,12, 0,32, 2,5 (marche) | 2,63 / 3,09 / 1,89 | 4,38 / 4,95 / 3,15 | 7,44 / — / 2,10 | 10,51 / — / 2,10 | 7,96 / — / 1,82 | 6,74 / — / 2,62 | 2,54 / 1,79 / 2,52 | 0,62 / — / 3,81 | 1,05 / — / 2,12 | 4,91 / 5,04 / 15,10 | 4,91 / 5,67 / 13,52 |
| knee | 2,03, 0,52, 4,6 (marche) | 1,45 / 1,89 / 1,03 | 2,42 / 3,02 / 1,72 | 4,11 / — / 1,14 | 5,80 / — / 1,14 | 4,40 / — / 0,99 | 3,72 / — / 1,43 | 1,40 / 1,09 / 1,37 | 0,34 / — / 2,07 | 0,58 / — / 1,15 | 2,71 / 3,08 / 8,21 | 2,71 / 3,46 / 7,36 |
| ankle_pitch | 2,35, 0,99, 2,5 (marche) | 1,25 / 1,00 / 1,87 | 2,08 / 1,59 / 3,12 | 3,54 / — / 2,08 | 5,00 / — / 2,08 | 3,79 / — / 1,80 | 3,21 / — / 2,59 | 1,21 / 0,58 / 2,49 | 0,30 / — / 3,77 | 0,50 / — / 2,10 | 2,34 / 1,62 / 14,94 | 2,34 / 1,83 / 13,39 |

### Marges à 0,30 m/s (borne : Unitree G1 (0.547 m/s)) : couple de pointe / couple continu / vitesse

Chaque case : rapport « publié ÷ requis » ; le couple doit atteindre la marge (1,5 ou 1,0), la vitesse 1,0. « — » : donnée non publiée (INCONNU).

| Axe | Requis : pointe, continu (N·m), vitesse (rad/s) | sts3215_c018 | sts3250 | HTD-85H | RSBL120-24 | KRS-9304HV ICS | DRS-0601 | LSS-HT1 | RS305CR | UBT-12HC (servo de l’Alpha 1S) | rs05 | edulite05 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hip_pitch | 2,72, 1,20, 5,7 (marche) | 1,08 / 0,82 / 0,83 | 1,80 / 1,31 / 1,38 | 3,06 / — / 0,92 | 4,33 / — / 0,92 | 3,28 / — / 0,80 | 2,78 / — / 1,15 | 1,05 / 0,47 / 1,10 | 0,26 / — / 1,67 | 0,43 / — / 0,93 | 2,02 / 1,34 / 6,62 | 2,02 / 1,50 / 5,93 |
| hip_roll | 1,72, 0,82, 4,4 (marche) | 1,71 / 1,19 / 1,06 | 2,84 / 1,91 / 1,78 | 4,83 / — / 1,18 | 6,82 / — / 1,18 | 5,17 / — / 1,03 | 4,38 / — / 1,48 | 1,65 / 0,69 / 1,42 | 0,40 / — / 2,15 | 0,68 / — / 1,19 | 3,19 / 1,94 / 8,50 | 3,19 / 2,19 / 7,61 |
| hip_yaw | 1,87, 0,71, 2,3 (marche) | 1,57 / 1,39 / 2,03 | 2,62 / 2,22 / 3,39 | 4,46 / — / 2,25 | 6,30 / — / 2,25 | 4,77 / — / 1,96 | 4,04 / — / 2,82 | 1,52 / 0,80 / 2,70 | 0,37 / — / 4,10 | 0,63 / — / 2,28 | 2,94 / 2,26 / 16,23 | 2,94 / 2,54 / 14,54 |
| knee | 2,90, 1,28, 14,1 (marche) | 1,01 / 0,76 / 0,33 | 1,69 / 1,22 / 0,56 | 2,87 / — / 0,37 | 4,06 / — / 0,37 | 3,07 / — / 0,32 | 2,60 / — / 0,46 | 0,98 / 0,44 / 0,45 | 0,24 / — / 0,67 | 0,41 / — / 0,37 | 1,90 / 1,25 / 2,67 | 1,90 / 1,40 / 2,39 |
| ankle_pitch | 1,11, 0,26, 18,2 (autres tâches) | 2,65 / 3,79 / 0,26 | 4,41 / 6,06 / 0,43 | 7,50 / — / 0,29 | 10,58 / — / 0,29 | 8,02 / — / 0,25 | 6,79 / — / 0,36 | 2,56 / 2,20 / 0,35 | 0,63 / — / 0,52 | 1,06 / — / 0,29 | 4,95 / 6,18 / 2,07 | 4,95 / 6,95 / 1,86 |


## Robot entier, règle plus_lente

**La règle « plus_lente » n'est PAS adoptée** : elle attend une fiche de décision de Jeremy (elle touche la fiche 0064). L'explorateur garde « explorateur » par défaut (`--regle-marche`, test de non-régression contre le commit cc340fd). Méthode et configurations imposées : en tête de `scripts/lab_leger_entier.py`.

| Config | Structure | Marge | Marche (m/s) | Plus petite H → réelle (m) | Masse (kg) | Coût (CHF) | Chute (J) | Autonomie (min) | Jambes | Axes les plus justes (pointe ÷ requis, continu ÷ requis, vitesse ÷ requise) | Kit réutilisé |
| --- | --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- | --- | ---: |
| A | carton | 1,5 | 0,100 | **ne tient à aucune H** de 0,35 à 0,65 m | — | — | — | — | — | — | — |
| A | carton | 1,5 | 0,150 | **ne tient à aucune H** de 0,35 à 0,65 m | — | — | — | — | — | — | — |
| A | carton | 1,5 | 0,196 | **ne tient à aucune H** de 0,35 à 0,65 m | — | — | — | — | — | — | — |
| A | carton | 1,0 | 0,100 | 0,45 → 0,826 | 3,5 | ≥ 1 904 | 16 | 59 | sts3250 | knee sts3250 (3,16, 3,94, 1,49); shoulder_pitch sts3215_c018 (14,30, —, 1,92) | 70 % |
| A | carton | 1,0 | 0,150 | 0,45 → 0,826 | 3,5 | ≥ 1 904 | 16 | 59 | sts3250 | knee sts3250 (3,16, 3,94, 1,49); shoulder_pitch sts3215_c018 (14,30, —, 1,92) | 70 % |
| A | carton | 1,0 | 0,196 | 0,65 → 0,689 | 3,6 | ≥ 1 904 | 14 | 56 | sts3250 | ankle_pitch sts3250 (1,84, 1,41, 3,25); hip_roll sts3250 (1,85, 1,49, 3,68) | 70 % |
| A | alu 2 mm évidé | 1,5 | 0,100 | **ne tient à aucune H** de 0,35 à 0,65 m | — | — | — | — | — | — | — |
| A | alu 2 mm évidé | 1,5 | 0,150 | **ne tient à aucune H** de 0,35 à 0,65 m | — | — | — | — | — | — | — |
| A | alu 2 mm évidé | 1,5 | 0,196 | **ne tient à aucune H** de 0,35 à 0,65 m | — | — | — | — | — | — | — |
| A | alu 2 mm évidé | 1,0 | 0,100 | **ne tient à aucune H** de 0,35 à 0,65 m | — | — | — | — | — | — | — |
| A | alu 2 mm évidé | 1,0 | 0,150 | **ne tient à aucune H** de 0,35 à 0,65 m | — | — | — | — | — | — | — |
| A | alu 2 mm évidé | 1,0 | 0,196 | **ne tient à aucune H** de 0,35 à 0,65 m | — | — | — | — | — | — | — |
| B | alu 2 mm évidé | 1,5 | 0,100 | **ne tient à aucune H** de 0,35 à 0,65 m | — | — | — | — | — | — | — |
| B | alu 2 mm évidé | 1,5 | 0,150 | **ne tient à aucune H** de 0,35 à 0,65 m | — | — | — | — | — | — | — |
| B | alu 2 mm évidé | 1,5 | 0,196 | **ne tient à aucune H** de 0,35 à 0,65 m | — | — | — | — | — | — | — |
| B | alu 2 mm évidé | 1,0 | 0,100 | **ne tient à aucune H** de 0,35 à 0,65 m | — | — | — | — | — | — | — |
| B | alu 2 mm évidé | 1,0 | 0,150 | **ne tient à aucune H** de 0,35 à 0,65 m | — | — | — | — | — | — | — |
| B | alu 2 mm évidé | 1,0 | 0,196 | **ne tient à aucune H** de 0,35 à 0,65 m | — | — | — | — | — | — | — |
| B | carton | 1,5 | 0,100 | **ne tient à aucune H** de 0,35 à 0,65 m | — | — | — | — | — | — | — |
| B | carton | 1,5 | 0,150 | **ne tient à aucune H** de 0,35 à 0,65 m | — | — | — | — | — | — | — |
| B | carton | 1,5 | 0,196 | **ne tient à aucune H** de 0,35 à 0,65 m | — | — | — | — | — | — | — |
| B | carton | 1,0 | 0,100 | 0,55 → — | 5,5 | ≥ 2 332 | — | 230 | edulite05, rs05 | ankle_pitch edulite05 (1,60, 1,25, 12,82); hip_roll edulite05 (1,61, 1,32, 14,50) | 70 % |
| B | carton | 1,0 | 0,150 | 0,55 → — | 5,5 | ≥ 2 332 | — | 230 | edulite05, rs05 | ankle_pitch edulite05 (1,60, 1,25, 12,82); hip_roll edulite05 (1,61, 1,32, 14,50) | 70 % |
| B | carton | 1,0 | 0,196 | 0,65 → — | 5,6 | ≥ 2 353 | — | 221 | edulite05, rs05 | ankle_pitch edulite05 (1,33, 1,04, 13,93); hip_roll edulite05 (1,33, 1,09, 15,76) | 71 % |

Lecture : « — » en hauteur réelle (configuration B) : les cotes de l'EduLite05 ne sont pas publiées, la place (taille minimale géométrique) ne se calcule pas ; l'énergie de chute, qui en dépend, non plus. À 0,196 m/s, la plus petite H est plus grande qu'à 0,15 : sous H ≈ 0,60 m, la marche ToddlerBot mise à l'échelle va moins vite que 0,196 m/s, et la règle passe alors au G1 (0,55 m/s à 0,60 m), bien plus exigeant. Une hauteur réelle très supérieure à H (0,45 → 0,826 m) vient de la place : les servos ne tiennent pas dans les proportions ANSUR d'un robot de 0,45 m, les chaînes s'allongent.

### Ce que la règle changerait ailleurs (documents NON régénérés)

| Profil | Règle « explorateur » (en vigueur) | Règle « plus_lente » |
| --- | --- | --- |
| Lab actuel, en « Home candidat » (ensemble 27, RobStride + Feetech, 12S, plus petite H) | H 0,85 → 0,850 m, 18,5 kg, ≥ 4 514 CHF, INCONNU | H 0,85 → 0,850 m, 18,5 kg, ≥ 4 514 CHF, INCONNU |
| Kit, option progressive | 3,05 kg, 1 178 CHF, servos sts3215_c018, sts3250 | 3,05 kg, 1 178 CHF, servos sts3215_c018, sts3250 |


## Le Lab actuel, recalculé comme « Home candidat » (rien n'est changé)

Profil lab, 12S, 250 Hz, chaîne compacte, ensemble 27, H = 0,85 m, petits axes Feetech : **INCONNU**, 0,850 m réels, 18,5 kg, ≥ 4 514 CHF, énergie de chute 87 J.

## Parmi les repères publiés (au registre ou dans les rapports)

| Robot | Hauteur (m) | Masse (kg) | Actionneurs | Coût | Marche démontrée | Source |
| --- | ---: | ---: | --- | --- | --- | --- |
| ToddlerBot 2XC | 0,56 | 3,4 | Dynamixel (6 axes par jambe) | — | oui (politique publiée, rejouée ici) | references_simulables.yaml |
| Zeroth-01 | 0,40 | 2,0 | STS3250 (5 axes par jambe) | — | non vue | docs/dimensionnement-par-actionneur.md (~0,40 m et ~2 kg, non vérifiés) |
| Berkeley Humanoid Lite | 0,80 | 16,0 | actionneurs maison (6 axes par jambe) | — | oui (politique publiée) | references_simulables.yaml |
| LeRobot Humanoid | — | 19,4 | RobStride RS00, RS02, RS03, RS05 (6 axes par jambe) | < 5 000 USD (objectif) | oui (politiques publiées) | references_simulables.yaml |

**Absents du registre et des rapports** (non placés, aucune recherche dans ce lot court) : Open Duck Mini v2, BRIDGE, Bumi.

