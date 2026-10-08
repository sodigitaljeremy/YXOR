# Un YXOR Lab léger, pour apprendre à marcher (2026-10)

**Engendré** par `.venv/bin/python scripts/lab_leger.py --ecrire`. **Étude, AUCUNE décision** : le profil `lab_leger` (`params/capacites.yaml`) est un CANDIDAT PROPOSÉ ; il ne remplace pas le profil lab.

Question de Jeremy (2026-10-08) : « Est-ce que l'étude et ce que nous avions déterminé pour YXOR Lab ne représente-t-il pas mieux YXOR Home finalement ? Est-ce qu'il n'existerait pas une meilleure version de YXOR Lab plus optimisée et compatible avec YXOR Kit ? »

Profil : marche sur sol plat 0,15 ou 0,3 m/s, relevé sur le dos et sur le ventre, gestes 0,5 m/s, tête à 2 axes, IA « + vision », autonomie 20 min (la plus exigeante de 10 et 20). Hors profil : saut, poussée, saisie, sol irrégulier, pente. Méthode : en tête de `scripts/lab_leger.py`.

## En bref

- **Marge 1,5** : aucune famille ne tient la marche entre 0,35 et 0,65 m.
- **Marge 1,0** : tient : feetech en carton, dès H = 0,60 m (0,695 m réels, 3,4 kg, ≥ 1 904 CHF, 13 J).
- **Le Lab actuel** (« Home candidat ») : 0,850 m, 18,5 kg, ≥ 4 514 CHF, 87 J à la chute.

## La plus petite H où la marche tient, par famille

« Tient » : faisable ou INCONNU (bornes proposées du système électrique), toutes capacités couvertes. Coût : borne basse, CHF HT (prix connus seulement). Énergie de chute : M·g·hauteur du centre de gravité. Part du Kit : coût connu de l'option progressive (`scripts/kit.py`) qui resservirait.

| Marge | Jambes | Structure | Marche (m/s) | H → réelle (m) | Masse (kg) | Coût (CHF) | Chute (J) | Statut | Part du Kit réutilisée | Ce qui resservirait |
| ---: | --- | --- | ---: | --- | ---: | ---: | ---: | --- | ---: | --- |
| 1,5 | feetech | alu 2 mm évidé | 0,15 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |
| 1,5 | feetech | alu 2 mm évidé | 0,30 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |
| 1,5 | feetech | carton | 0,15 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_roll, hip_yaw) | — | — | — | — | — | — |
| 1,5 | feetech | carton | 0,30 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_roll, hip_yaw) | — | — | — | — | — | — |
| 1,5 | dynamixel | alu 2 mm évidé | 0,15 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, knee) | — | — | — | — | — | — |
| 1,5 | dynamixel | alu 2 mm évidé | 0,30 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, knee) | — | — | — | — | — | — |
| 1,5 | dynamixel | carton | 0,15 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : ankle_pitch, knee) | — | — | — | — | — | — |
| 1,5 | dynamixel | carton | 0,30 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : ankle_pitch, knee) | — | — | — | — | — | — |
| 1,5 | robstride | alu 2 mm évidé | 0,15 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |
| 1,5 | robstride | alu 2 mm évidé | 0,30 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |
| 1,5 | robstride | carton | 0,15 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |
| 1,5 | robstride | carton | 0,30 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |
| 1,0 | feetech | alu 2 mm évidé | 0,15 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |
| 1,0 | feetech | alu 2 mm évidé | 0,30 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |
| 1,0 | feetech | carton | 0,15 | 0,60 → 0,695 | 3,4 | ≥ 1 904 | 13 | INCONNU | 70 % | 15 × sts3215_c018, calculateur, adaptateur série |
| 1,0 | feetech | carton | 0,30 | 0,60 → 0,695 | 3,4 | ≥ 1 904 | 13 | INCONNU | 70 % | 15 × sts3215_c018, calculateur, adaptateur série |
| 1,0 | dynamixel | alu 2 mm évidé | 0,15 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : ankle_pitch, knee) | — | — | — | — | — | — |
| 1,0 | dynamixel | alu 2 mm évidé | 0,30 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : ankle_pitch, knee) | — | — | — | — | — | — |
| 1,0 | dynamixel | carton | 0,15 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : ankle_pitch, hip_yaw, knee) | — | — | — | — | — | — |
| 1,0 | dynamixel | carton | 0,30 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : ankle_pitch, hip_yaw, knee) | — | — | — | — | — | — |
| 1,0 | robstride | alu 2 mm évidé | 0,15 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |
| 1,0 | robstride | alu 2 mm évidé | 0,30 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |
| 1,0 | robstride | carton | 0,15 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |
| 1,0 | robstride | carton | 0,30 | **ne tient à aucune H** de 0,35 à 0,65 m (bloquent : hip_pitch, hip_roll, hip_yaw, knee) | — | — | — | — | — | — |

## La moins chère par famille (marche 0,3 m/s) : le prix de chaque famille

| Marge | Jambes | Structure | H → réelle (m) | Masse (kg) | Coût (CHF) | Chute (J) | Actionneurs des jambes |
| ---: | --- | --- | --- | ---: | ---: | ---: | --- |
| 1,0 | feetech | carton | 0,60 → 0,695 | 3,4 | ≥ 1 904 | 13 | sts3215_c018, sts3250 |

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

