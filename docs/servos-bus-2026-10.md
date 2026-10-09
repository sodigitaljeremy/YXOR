# Les familles de petits servos à bus (2026-10)

**Engendré** par `.venv/bin/python scripts/servos_bus.py --ecrire`. **Étude, AUCUNE décision, aucun achat.** Question de Jeremy (2026-10-08) : « Pourquoi choisir du Feetech ? Car ce sont les actionneurs les moins chers du marché ? » Méthode et limites : en tête de `scripts/servos_bus.py`.

## Par famille

Couple : AU BLOCAGE (le seul publié partout) ; vitesse à vide à la tension de la fiche ; prix en CHF HT. « Continu publié » : nombre de modèles dont le fabricant publie un couple continu ou nominal.

| Famille | Modèles | N·m par 100 g (meilleur) | N·m par 10 CHF (meilleur) | Le plus fort (N·m) | Le plus rapide (rad/s) | Prix le plus bas (CHF) | Continu publié | Sans prix CHF | Retours de fiabilité | Robots qui marchent (relevés) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Hiwonder | 6 | 6,90 | 2,50 | 8,34 | 5,8 | 14 | 0/6 | 0 | 2 | Walbi, the Walking Biped |
| Waveshare | 6 | — | 1,54 | 11,77 | 10,5 | 8 | 0/6 | 1 | 1 | Chien robot 12 DDL (modèle ouvert Waveshare) |
| Kondo | 6 | 8,18 | — | 8,91 | 9,5 | — | 0/6 | 6 | — | — |
| HerkuleX | 4 | 6,14 | 0,23 | 7,55 | 7,1 | 51 | 2/4 | 2 | 1 | — |
| Lynxmotion LSS | 3 | 4,51 | — | 2,84 | 10,5 | — | 3/3 | 3 | — | SES-V2 Hexapod (18 × LSS-ST1) et mechDOG (quadrupède, LSS-ST1) |
| Futaba RS (commande) | 5 | 2,84 | — | 0,70 | 9,5 | — | 0/5 | 5 | — | — |
| UBTECH | 1 | 2,80 | — | 1,18 | 5,3 | — | 0/1 | 1 | — | — |
| Feetech | 16 | 6,58 | 1,40 | 4,90 | 20,9 | 10 | 16/16 | 11 | — | — |
| Dynamixel | 16 | 5,00 | 0,49 | 4,10 | 40,1 | 28 | 0/16 | 0 | — | — |

Retours de fiabilité et robots : relevés par l'agent (`params/servos_bus.yaml`, `familles`) pour les familles nouvelles ; pour Feetech et Dynamixel, non relevés dans ce lot (« — » ne veut pas dire « aucun »).

## Le Lab léger tiendrait-il avec une autre famille ? (marge 1,5, H = 0,60 m, 3,45 kg)

| Axe | Pointe requise × 1,5 (N·m) | Continu requis × 1,5 (N·m) | Vitesse requise (rad/s) |
| --- | ---: | ---: | ---: |
| hip_pitch | 4,08 | 1,80 | 6,0 |
| hip_roll | 2,59 | 1,26 | 4,4 |
| hip_yaw | 2,80 | 1,06 | 4,6 |
| knee | 4,35 | 1,92 | 14,1 |
| ankle_pitch | 1,67 | 0,43 | 18,2 |

| Famille | hip_pitch | hip_roll | hip_yaw | knee | ankle_pitch | Tient tout ? |
| --- | --- | --- | --- | --- | --- | --- |
| Hiwonder | non (vitesse) | oui (HTD-35H) | oui (HTD-35H) | non (vitesse) | non (vitesse) | **non** |
| Waveshare | non (vitesse) | oui (ST3215 (12 V)) | oui (ST3215 (12 V)) | non (vitesse) | non (vitesse) | **non** |
| Kondo | oui (KRS-4034HV ICS) | oui (KRS-4034HV ICS) | oui (KRS-4034HV ICS) | non (vitesse) | non (vitesse) | **non** |
| HerkuleX | oui (DRS-0401) | oui (DRS-0401) | oui (DRS-0401) | non (vitesse) | non (vitesse) | **non** |
| Lynxmotion LSS | non (couple) | non (couple) | non (couple) | non (ni couple ni vitesse) | non (vitesse) | **non** |
| Futaba RS (commande) | non (couple) | non (couple) | non (couple) | non (ni couple ni vitesse) | non (ni couple ni vitesse) | **non** |
| UBTECH | non (ni couple ni vitesse) | non (couple) | non (couple) | non (ni couple ni vitesse) | non (ni couple ni vitesse) | **non** |
| Feetech | non (couple) | oui (sts3250) | oui (sts3250) | non (vitesse) | non (vitesse) | **non** |
| Dynamixel | non (vitesse) | oui (xm430_w210) | oui (xm430_w210) | non (couple) | non (vitesse) | **non** |

« non (vitesse) » : des modèles ont le couple, aucun d'eux la vitesse ; « non (couple) » : le couple manque.

## Et à la marge 1,0 (repère : celle d'un robot qui marche déjà)

Familles qui tiendraient tous les axes de jambe : **aucune**. Feetech : hip_pitch oui (sts3250), hip_roll oui (sts3215_c018), hip_yaw oui (sts3215_c018), knee non (vitesse), ankle_pitch non (vitesse).

**Correction de docs/lab-leger-2026-10.md** (non régénéré : pas de relance de l'explorateur dans ce lot). Son seul résultat positif, « Feetech en carton tient à la marge 1,0 », reposait sur la vitesse INCONNUE du STS3250 dans le catalogue de l'explorateur (une donnée manquante ne fait pas échouer un choix). Avec la vitesse de sa fiche candidate (0,133 s/60°, soit 7,9 rad/s à 12 V, `params/actionneurs.yaml`), le genou (14 rad/s) et la cheville (18 rad/s) ne tiennent pas : ce résultat ne vaut pas.

