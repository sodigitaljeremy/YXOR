# Saut vertical selon la profondeur d'accroupi (2026-10)

**Engendré** par `.venv/bin/python scripts/saut.py --ecrire`. Ne pas éditer à la main. **Étude, aucune décision** : le profil du Lab ne change pas (saut 10 cm, décidé le 2026-10-07) ; Jeremy décidera.

Modèle (phase 3a corrigée le 2026-10-08) : accroupi au tibia incliné de α, hanche à l'aplomb de la cheville ; course de poussée = jambe tendue − accroupie ; accélération constante ; vitesse angulaire en rampe linéaire (pointe = 2 × moyenne) ; force par jambe M·g·(1 + h/d) × répartition ; bras de levier : genou tibia·sin α, hanche |tibia·sin α − cuisse| (majorant), cheville moitié du pied. Inclinaisons balayées : PROPOSÉES.

RobStride en 12S coupé à 3,0 V par cellule (décidé), vitesse à vide × 36 / 48 : rs05 6 N·m, 37,7 rad/s ; rs00 14 N·m, 24,7 rad/s ; rs02 17 N·m, 32,2 rad/s ; rs02_ip67 17 N·m, 32,2 rad/s ; rs06 36 N·m, 37,7 rad/s ; rs10p 42 N·m, 9,8 rad/s ; rs03 60 N·m, 15,3 rad/s ; rs04 120 N·m, 15,7 rad/s. Marge 1,5 sur le couple (fiche 0051). M_max : masse du robot au-delà de laquelle le RobStride le plus fort ASSEZ RAPIDE ne tient plus la pointe.

| H (m) | Tibia (°) | Saut (cm) | Course (mm) | Poussée (ms) | Genou N·m/kg, rad/s | Hanche N·m/kg, rad/s | Cheville N·m/kg, rad/s | M_max (kg) et limite |
| ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| 0,55 | 30 | 5 | 32 | 64 | 0,786, 31,1 (rs06) | 0,931, 14,8 (rs04) | 0,532, 27,2 (rs06) | **30,5** (knee) |
| 0,55 | 30 | 10 | 32 | 45 | 1,267, 44,0 (aucun assez rapide) | 1,500, 20,9 (rs06) | 0,857, 38,4 (aucun assez rapide) | **0,0** (knee) |
| 0,55 | 40 | 5 | 55 | 112 | 0,749, 23,8 (rs06) | 0,523, 11,3 (rs04) | 0,394, 18,8 (rs06) | **32,1** (knee) |
| 0,55 | 40 | 10 | 55 | 79 | 1,104, 33,6 (rs06) | 0,772, 15,9 (rs06) | 0,581, 26,5 (rs06) | **21,7** (knee) |
| 0,55 | 50 | 5 | 84 | 169 | 0,748, 19,5 (rs06) | 0,319, 9,2 (rs04) | 0,330, 14,5 (rs04) | **32,1** (knee) |
| 0,55 | 50 | 10 | 84 | 119 | 1,028, 27,6 (rs06) | 0,438, 13,0 (rs04) | 0,454, 20,5 (rs06) | **23,3** (knee) |
| 0,55 | 60 | 5 | 116 | 233 | 0,759, 16,8 (rs06) | 0,198, 7,8 (rs04) | 0,296, 12,0 (rs04) | **31,6** (knee) |
| 0,55 | 60 | 10 | 116 | 165 | 0,988, 23,8 (rs06) | 0,258, 11,1 (rs04) | 0,386, 16,9 (rs06) | **24,3** (knee) |
| 0,60 | 30 | 5 | 35 | 70 | 0,814, 28,5 (rs06) | 0,964, 13,6 (rs04) | 0,551, 24,9 (rs06) | **29,5** (knee) |
| 0,60 | 30 | 10 | 35 | 50 | 1,294, 40,3 (aucun assez rapide) | 1,533, 19,2 (rs06) | 0,876, 35,2 (rs06) | **0,0** (knee) |
| 0,60 | 40 | 5 | 60 | 122 | 0,784, 21,8 (rs06) | 0,548, 10,3 (rs04) | 0,413, 17,2 (rs06) | **30,6** (knee) |
| 0,60 | 40 | 10 | 60 | 86 | 1,140, 30,8 (rs06) | 0,797, 14,6 (rs04) | 0,600, 24,3 (rs06) | **21,1** (knee) |
| 0,60 | 50 | 5 | 91 | 184 | 0,791, 17,9 (rs06) | 0,337, 8,4 (rs04) | 0,349, 13,3 (rs04) | **30,3** (knee) |
| 0,60 | 50 | 10 | 91 | 130 | 1,071, 25,3 (rs06) | 0,456, 11,9 (rs04) | 0,473, 18,7 (rs06) | **22,4** (knee) |
| 0,60 | 60 | 5 | 126 | 255 | 0,807, 15,4 (rs04) | 0,211, 7,2 (rs04) | 0,315, 11,0 (rs04) | **99,2** (knee) |
| 0,60 | 60 | 10 | 126 | 180 | 1,036, 21,8 (rs06) | 0,271, 10,2 (rs04) | 0,405, 15,5 (rs04) | **23,2** (knee) |
