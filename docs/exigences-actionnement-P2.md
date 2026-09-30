# Exigences d'actionnement — P2, premier chiffrage

**Calculé le 2026-09-30.** Heure système lue par `date` : 13 h 48 CEST.
Aucune pièce, aucun paramètre n'a été modifié.

C'est un **ordre de grandeur**, pas un dimensionnement. La marche vient
de ToddlerBot (P1, H = 0,56 m) et elle est transposée à P2 (H = 0,90 m)
par des lois de similitude. Elle ne vaut que ce que valent leurs
hypothèses (§ 3).

## Statuts

| Marque | Sens |
| --- | --- |
| **V** | **vérifié** — lu dans le fichier cité, ou calculé par moi pendant ce travail |
| **Déd** | **déduit** — un raisonnement ou une loi appliquée, à discuter |

---

## 0 — Deux écarts avec la demande, à connaître avant les chiffres

**1. Les données amont déjà extraites ne portent pas ce qu'il fallait (V).**
`params/upstream_joints.generated.yaml` ne contient que les axes et les
butées. `params/joints.yaml` ajoute les transmissions. **Ni le modèle de
moteur, ni une limite de couple ou de vitesse ne sont dans le dépôt.**

Je les ai donc lus dans les fichiers de **données** amont, au commit
épinglé `e337f3b` :

- **le MJCF** `toddlerbot/descriptions/toddlerbot_2xc/toddlerbot_2xc.xml`
  déclare le modèle de moteur par la **classe** de chaque articulation
  (lignes citées en T1). Comme limite de couple, il n'a qu'un
  `ctrlrange="-10 10"` **commun aux 30 moteurs** (l. 31). C'est une
  borne de commande générique, pas une caractéristique de moteur. **Le
  MJCF ne déclare aucune limite de vitesse.**
- **`toddlerbot/descriptions/default.yml`** associe chaque moteur à son
  modèle (section `motors`). Il donne, par modèle, `tau_max`,
  `q_dot_max`, `tau_q_dot_max`, `q_dot_tau_max` et `tau_brake_max`
  (section `actuators`, l. 244-316). sha256 du fichier lu :
  `0549fe40518a4905…`.

Les deux sources concordent : **le modèle déclaré par `default.yml` est
la classe MJCF pour 30 articulations sur 30** (V). Aucun code amont n'a
été copié. Les fichiers ont été lus comme données, au même titre que
`import_upstream_limits.py` lit le MJCF (fiche 0006).

**2. La série de 749 pas n'est pas une marche (V).** C'est
`exports/actionneurs/couples_balancement.csv`, produite par
`scripts/enveloppes_actionneurs.py` : des poses tenues, un balancement,
sans aucune politique de marche. La série de marche,
`couples_marche.csv`, **n'était plus conservée**. Je l'ai moi-même
écrasée le 2026-09-29 à 23 h 44, pendant l'audit de la nuit, par un
essai d'une seconde (51 pas). **La marche a donc été relancée** (§ 2).

---

## 1 — Inventaire des 30 actionneurs de ToddlerBot

Les limites sont celles du **modèle de moteur de la simulation amont**
(`default.yml`), et non d'une fiche constructeur. Les lignes par
modèle, pour `tau_max` / `q_dot_max` / `tau_brake_max` : XC330 l. 248 /
249 / 252 ; XC430 l. 260 / 261 / 264 ; XM430-W210 l. 284 / 285 / 288 ;
2XL430 l. 296 / 297 / 300 ; 2XC430 l. 308 / 309 / 312. XM430-W350
(l. 268-279) est déclaré, mais aucun des 30 moteurs ne l'utilise (V).

**Comment l'amont s'en sert (V, `toddlerbot/sim/motor_control.py`,
l. 40-100)** :

- **en moteur**, le couple est borné à `tau_max` jusqu'à
  `q_dot_tau_max`, puis décroît linéairement jusqu'à `tau_q_dot_max` à
  `q_dot_max` ;
- **en freinage**, la borne est `tau_brake_max`, plus élevée.

**Conséquence : les couples de la simulation ne peuvent pas dépasser ces
bornes.** Un rapport pointe / limite voisin de 1 signale un
**écrêtage**, pas un besoin satisfait (§ 2).

| # | Actionneur | Zone | Modèle (`default.yml`) | Ligne `default.yml` | Classe MJCF (ligne) | τ_max N·m | τ_frein max N·m | ω_max rad/s |
| ---: | --- | --- | --- | ---: | --- | ---: | ---: | ---: |
| 1 | `neck_yaw_drive` | cou | XC330 | 16 | XC330 (l. 46) | 0,68 | 1,54 | 6,52 |
| 2 | `neck_pitch_act` | cou | XC330 | 23 | XC330 (l. 76) | 0,68 | 1,54 | 6,52 |
| 3 | `waist_act_1` | taille | XC330 | 30 | XC330 (l. 125) | 0,68 | 1,54 | 6,52 |
| 4 | `waist_act_2` | taille | XC330 | 37 | XC330 (l. 133) | 0,68 | 1,54 | 6,52 |
| 5 | `left_hip_pitch` | jambes | 2XC430 | 44 | 2XC430 (l. 141) | 1,09 | 2,20 | 6,78 |
| 6 | `left_hip_roll` | jambes | 2XC430 | 51 | 2XC430 (l. 151) | 1,09 | 2,20 | 6,78 |
| 7 | `left_hip_yaw_drive` | jambes | XC330 | 58 | XC330 (l. 168) | 0,68 | 1,54 | 6,52 |
| 8 | `left_knee` | jambes | XM430-W210 | 65 | XM430-W210 (l. 176) | 1,94 | 2,20 | 7,60 |
| 9 | `left_ankle_roll` | jambes | XC430 | 72 | XC430 (l. 195) | 1,47 | 2,00 | 7,00 |
| 10 | `left_ankle_pitch` | jambes | XM430-W210 | 79 | XM430-W210 (l. 185) | 1,94 | 2,20 | 7,60 |
| 11 | `right_hip_pitch` | jambes | 2XC430 | 86 | 2XC430 (l. 213) | 1,09 | 2,20 | 6,78 |
| 12 | `right_hip_roll` | jambes | 2XC430 | 93 | 2XC430 (l. 223) | 1,09 | 2,20 | 6,78 |
| 13 | `right_hip_yaw_drive` | jambes | XC330 | 101 | XC330 (l. 240) | 0,68 | 1,54 | 6,52 |
| 14 | `right_knee` | jambes | XM430-W210 | 107 | XM430-W210 (l. 248) | 1,94 | 2,20 | 7,60 |
| 15 | `right_ankle_roll` | jambes | XC430 | 114 | XC430 (l. 267) | 1,47 | 2,00 | 7,00 |
| 16 | `right_ankle_pitch` | jambes | XM430-W210 | 121 | XM430-W210 (l. 257) | 1,94 | 2,20 | 7,60 |
| 17 | `left_shoulder_pitch` | bras | XC430 | 128 | XC430 (l. 287) | 1,47 | 2,00 | 7,00 |
| 18 | `left_shoulder_roll` | bras | 2XL430 | 135 | 2XL430 (l. 294) | 0,93 | 1,40 | 5,97 |
| 19 | `left_shoulder_yaw_drive` | bras | 2XL430 | 142 | 2XL430 (l. 304) | 0,93 | 1,40 | 5,97 |
| 20 | `left_elbow_roll` | bras | 2XL430 | 149 | 2XL430 (l. 322) | 0,93 | 1,40 | 5,97 |
| 21 | `left_elbow_yaw_drive` | bras | 2XL430 | 156 | 2XL430 (l. 332) | 0,93 | 1,40 | 5,97 |
| 22 | `left_wrist_pitch_drive` | bras | 2XL430 | 163 | 2XL430 (l. 360) | 0,93 | 1,40 | 5,97 |
| 23 | `left_wrist_roll` | bras | 2XL430 | 170 | 2XL430 (l. 368) | 0,93 | 1,40 | 5,97 |
| 24 | `right_shoulder_pitch` | bras | XC430 | 177 | XC430 (l. 386) | 1,47 | 2,00 | 7,00 |
| 25 | `right_shoulder_roll` | bras | 2XL430 | 184 | 2XL430 (l. 393) | 0,93 | 1,40 | 5,97 |
| 26 | `right_shoulder_yaw_drive` | bras | 2XL430 | 191 | 2XL430 (l. 403) | 0,93 | 1,40 | 5,97 |
| 27 | `right_elbow_roll` | bras | 2XL430 | 198 | 2XL430 (l. 421) | 0,93 | 1,40 | 5,97 |
| 28 | `right_elbow_yaw_drive` | bras | 2XL430 | 205 | 2XL430 (l. 431) | 0,93 | 1,40 | 5,97 |
| 29 | `right_wrist_pitch_drive` | bras | 2XL430 | 212 | 2XL430 (l. 459) | 0,93 | 1,40 | 5,97 |
| 30 | `right_wrist_roll` | bras | 2XL430 | 219 | 2XL430 (l. 467) | 0,93 | 1,40 | 5,97 |

La zone est déduite du nom (Déd) : `neck_*` → cou, `waist_*` → taille,
hanche/genou/cheville → jambes, le reste → bras. **La taille** (2
moteurs en différentiel) **n'entre dans aucune des trois zones
demandées** ; elle est montrée à part.

---

## 2 — Marche enregistrée : couples, vitesses, rapports aux limites

### L'enregistrement (V)

| | |
| --- | --- |
| politique | `toddlerbot_2xc_walk_rsl_20251226_114612`, avec les deux correctifs de `sim/upstream/toddlerbot_fixes.py` |
| commande | vx = 0,10 m/s, ligne droite, sol plat |
| durée | 15 s de marche après 7 s de mise en pose (t = 7,00 → 22,00 s) |
| échantillons | **751 pas de contrôle à 50 Hz** (dt = 0,02 s) × 30 actionneurs |
| résultat | +1,590 m en 15 s, **0,106 m/s** ; torse jamais sous 0,281 m, **pas de chute** |
| grandeurs | `actuator_force` (N·m) et `actuator_velocity` (rad/s), côté moteur ; `gear` = 1 pour les 30 actionneurs |
| fichier | `exports/actionneurs/marche_15s.csv`, sha256 `3de8ca2050a16667…` |
| scripts | `exports/actionneurs/enregistrer_marche.py` (venv amont) et `analyser.py` (venv projet) |

**Hors du dépôt, et je le signale.** Les deux scripts et la série sont
dans `exports/`, qui est ignoré par Git. La consigne était « lecture et
calcul uniquement » : je n'ai rien ajouté à `sim/` ni à `scripts/`.
**Ces chiffres ne se régénèrent donc pas depuis le dépôt seul.** Les
versionner serait une décision.

L'enregistreur reprend la boucle de `sim/upstream/replay_policy.py`
(mêmes correctifs, même politique) sans le rendu vidéo. Il ajoute les
vitesses, que `replay_policy.py` ne journalise pas.

### Définitions

- **pointe** : max |τ| sur les 751 échantillons ;
- **RMS** : racine de la moyenne de τ² — c'est le couple qui chauffe le
  moteur (fiche 0038) ;
- **P pointe** : max |τ·ω|, puissance mécanique instantanée ;
- **écrêté** : échantillon où le couple atteint 99 % de la borne du
  modèle, en moteur (τ·ω ≥ 0, borne selon la courbe couple-vitesse) ou
  en freinage (τ·ω < 0, `tau_brake_max`). Calculé avec la vitesse
  enregistrée *après* le pas, donc approché (Déd).

| Actionneur | Zone | τ pointe N·m | τ RMS N·m | ω pointe rad/s | P pointe W | pointe / τ_max | pointe / τ_frein | ω / ω_max | écrêté (moteur + frein) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `neck_yaw_drive` | cou | 0,014 | 0,006 | 0,01 | 0,00 | 0,02 | 0,01 | 0,00 | 0 / 751 |
| `neck_pitch_act` | cou | 0,098 | 0,057 | 0,04 | 0,00 | 0,14 | 0,06 | 0,01 | 0 / 751 |
| `waist_act_1` | taille | 0,259 | 0,102 | 0,24 | 0,04 | 0,38 | 0,17 | 0,04 | 0 / 751 |
| `waist_act_2` | taille | 0,261 | 0,094 | 0,24 | 0,04 | 0,38 | 0,17 | 0,04 | 0 / 751 |
| `left_hip_pitch` | jambes | 1,090 | 0,328 | 2,37 | 1,17 | 1,00 | 0,50 | 0,35 | 5 / 751 (**0,7 %**) |
| `left_hip_roll` | jambes | 2,200 | 0,801 | 2,64 | 2,10 | 2,02 | 1,00 | 0,39 | 129 / 751 (**17,2 %**) |
| `left_hip_yaw_drive` | jambes | 1,436 | 0,311 | 1,35 | 0,43 | 2,11 | 0,93 | 0,21 | 82 / 751 (**10,9 %**) |
| `left_knee` | jambes | 2,200 | 0,766 | 4,32 | 4,25 | 1,13 | 1,00 | 0,57 | 32 / 751 (**4,3 %**) |
| `left_ankle_roll` | jambes | 0,648 | 0,180 | 2,66 | 1,37 | 0,44 | 0,32 | 0,38 | 0 / 751 |
| `left_ankle_pitch` | jambes | 1,409 | 0,458 | 3,42 | 1,88 | 0,73 | 0,64 | 0,45 | 0 / 751 |
| `right_hip_pitch` | jambes | 1,090 | 0,367 | 2,54 | 2,39 | 1,00 | 0,50 | 0,37 | 18 / 751 (**2,4 %**) |
| `right_hip_roll` | jambes | 1,792 | 0,711 | 2,30 | 1,79 | 1,64 | 0,81 | 0,34 | 72 / 751 (**9,6 %**) |
| `right_hip_yaw_drive` | jambes | 1,302 | 0,285 | 1,36 | 0,61 | 1,91 | 0,85 | 0,21 | 59 / 751 (**7,9 %**) |
| `right_knee` | jambes | 2,200 | 0,712 | 3,69 | 5,16 | 1,13 | 1,00 | 0,49 | 34 / 751 (**4,5 %**) |
| `right_ankle_roll` | jambes | 1,084 | 0,233 | 1,84 | 0,57 | 0,74 | 0,54 | 0,26 | 0 / 751 |
| `right_ankle_pitch` | jambes | 2,200 | 0,643 | 1,98 | 3,15 | 1,13 | 1,00 | 0,26 | 2 / 751 (**0,3 %**) |
| `left_shoulder_pitch` | bras | 0,256 | 0,088 | 0,43 | 0,09 | 0,17 | 0,13 | 0,06 | 0 / 751 |
| `left_shoulder_roll` | bras | 0,190 | 0,072 | 0,20 | 0,02 | 0,20 | 0,14 | 0,03 | 0 / 751 |
| `left_shoulder_yaw_drive` | bras | 0,014 | 0,007 | 0,00 | 0,00 | 0,02 | 0,01 | 0,00 | 0 / 751 |
| `left_elbow_roll` | bras | 0,040 | 0,030 | 0,01 | 0,00 | 0,04 | 0,03 | 0,00 | 0 / 751 |
| `left_elbow_yaw_drive` | bras | 0,001 | 0,001 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0 / 751 |
| `left_wrist_pitch_drive` | bras | 0,002 | 0,001 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0 / 751 |
| `left_wrist_roll` | bras | 0,003 | 0,001 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0 / 751 |
| `right_shoulder_pitch` | bras | 0,164 | 0,073 | 0,20 | 0,02 | 0,11 | 0,08 | 0,03 | 0 / 751 |
| `right_shoulder_roll` | bras | 0,205 | 0,091 | 0,25 | 0,04 | 0,22 | 0,15 | 0,04 | 0 / 751 |
| `right_shoulder_yaw_drive` | bras | 0,010 | 0,006 | 0,00 | 0,00 | 0,01 | 0,01 | 0,00 | 0 / 751 |
| `right_elbow_roll` | bras | 0,041 | 0,033 | 0,01 | 0,00 | 0,04 | 0,03 | 0,00 | 0 / 751 |
| `right_elbow_yaw_drive` | bras | 0,001 | 0,001 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0 / 751 |
| `right_wrist_pitch_drive` | bras | 0,002 | 0,001 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0 / 751 |
| `right_wrist_roll` | bras | 0,002 | 0,001 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0 / 751 |

### Lecture (Déd)

- **Neuf actionneurs de jambe sont écrêtés à un moment de la marche.**
  Les pires sont le roulis de hanche gauche (17 % du temps), le lacet de
  hanche gauche (11 %) et le roulis droit (10 %). **Pour ceux-là, la
  pointe mesurée est la borne du moteur simulé, pas le besoin de la
  marche** : le vrai besoin est au moins aussi grand, et on ne sait pas
  de combien. Le RMS est sous-estimé pour la même raison.
- **Quatre pointes valent exactement 2,200 N·m** : les deux genoux, le
  roulis de hanche gauche et le tangage de cheville droit. C'est
  `tau_brake_max` de leur modèle : elles sont bornées en **freinage**.
  Les deux tangages de hanche culminent à 1,090 N·m, soit `tau_max` du
  2XC430 : ceux-là sont bornés **en moteur**.
- Le rapport pointe / `tau_max` dépasse 1 pour plusieurs articulations,
  ce que la courbe permet en freinage. La colonne pointe / `tau_frein`
  est celle qui plafonne à 1,00.
- **Les vitesses restent loin de leurs limites**, au plus 57 % de
  `q_dot_max` (genou gauche). **C'est le couple qui contraint, pas la
  vitesse.**
- Échantillonnage à 50 Hz : une pointe plus brève que 20 ms entre deux
  échantillons n'est pas vue.
- Les bras, le cou et la taille travaillent très peu en marche (bras
  immobiles). Leurs valeurs ne disent rien d'une tâche de manipulation.

---

## 3 — Passage à l'échelle P2 (H = 0,90 m)

### Les lois (Déd)

s = H / H0 = 0,90 / 0,56 = **1,6071**.

| Grandeur | Loi | Facteur |
| --- | --- | ---: |
| longueurs | × s | 1,607 |
| masse | × s³ | 4,151 → **14,3 kg** pour les 3,454 kg de ToddlerBot (masse lue dans le MJCF, V) |
| couple | × s⁴ | **6,671** |
| vitesse angulaire | × s^−0,5 | **0,7888** |
| puissance | × s^3,5 | **5,262** |
| vitesse de marche | × s^0,5 | 0,106 → **0,134 m/s** |

### Les hypothèses

1. **Géométrie semblable** : toutes les longueurs × s, aux mêmes
   proportions.
2. **Même masse volumique** : masse × s³, inertie × s⁵.
3. **Même allure de marche**, au sens de Froude (même v² / gL) : les
   durées × s^0,5, donc les vitesses angulaires × s^−0,5 et les
   accélérations angulaires × s^−1. Le couple de gravité (m·g·L) et le
   couple d'inertie (I·α) varient alors **tous deux** en s⁴ : c'est ce
   qui rend la loi cohérente.

### Ce qu'elles négligent

- **La masse ne suivra pas s³.** Les moteurs sont des produits discrets,
  pas des pièces qui grandissent. Et l'architecture en plaques (fiche
  0015) n'a pas la masse volumique des pièces imprimées de ToddlerBot.
  **C'est l'hypothèse la plus fragile** ; `enveloppes_actionneurs.py` le
  disait déjà.
- **Frottements, amortissements et inertie de rotor** (`armature`,
  `damping`, `frictionloss` du MJCF) ne suivent aucune de ces lois.
- **La politique a été apprise pour P1.** Rien ne garantit qu'une
  politique P2 marche avec la même allure.
- **L'écrêtage de P1 est transporté tel quel** : une borne basse × 6,67
  reste une borne basse.
- **Un seul cas** : marche droite à 0,10 m/s sur sol plat. Ni virage,
  ni pente, ni perturbation, ni relevé après chute, ni station
  prolongée — or ce sont souvent eux qui dimensionnent.
- **Les transmissions de ToddlerBot sont supposées conservées.** Les
  couples sont pris côté moteur. `joints.yaml` donne un rapport de 1
  pour 11 des 12 DDL de jambe, et de 0,857 pour le lacet de hanche
  (l. 59), engrenage dont le sens exact n'est pas revérifié ici.

### Le facteur de sécurité de 1,5

**C'est un choix à valider par Jeremy, pas une norme.** Aucune norme n'a
été consultée pour ce facteur. Il couvre grossièrement l'écrêtage et le
cas unique. **Il ne couvre pas** une masse qui s'écarterait de s³.

| Actionneur | τ pointe P2 N·m | τ RMS P2 N·m | ω pointe P2 rad/s | P pointe P2 W | τ pointe P2 × 1,5 | τ RMS P2 × 1,5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `neck_yaw_drive` | 0,09 | 0,04 | 0,01 | 0,00 | 0,14 | 0,06 |
| `neck_pitch_act` | 0,66 | 0,38 | 0,03 | 0,01 | 0,98 | 0,57 |
| `waist_act_1` | 1,72 | 0,68 | 0,19 | 0,21 | 2,59 | 1,02 |
| `waist_act_2` | 1,74 | 0,63 | 0,19 | 0,24 | 2,61 | 0,94 |
| `left_hip_pitch` | 7,27 | 2,19 | 1,87 | 6,18 | 10,91 | 3,28 |
| `left_hip_roll` | 14,68 | 5,35 | 2,08 | 11,05 | 22,02 | 8,02 |
| `left_hip_yaw_drive` | 9,58 | 2,08 | 1,07 | 2,24 | 14,37 | 3,11 |
| `left_knee` | 14,68 | 5,11 | 3,41 | 22,39 | 22,02 | 7,66 |
| `left_ankle_roll` | 4,33 | 1,20 | 2,10 | 7,22 | 6,49 | 1,80 |
| `left_ankle_pitch` | 9,40 | 3,06 | 2,69 | 9,88 | 14,10 | 4,59 |
| `right_hip_pitch` | 7,27 | 2,45 | 2,00 | 12,60 | 10,91 | 3,68 |
| `right_hip_roll` | 11,96 | 4,75 | 1,81 | 9,44 | 17,94 | 7,12 |
| `right_hip_yaw_drive` | 8,69 | 1,90 | 1,07 | 3,19 | 13,03 | 2,85 |
| `right_knee` | 14,68 | 4,75 | 2,91 | 27,16 | 22,02 | 7,12 |
| `right_ankle_roll` | 7,23 | 1,56 | 1,45 | 3,01 | 10,85 | 2,33 |
| `right_ankle_pitch` | 14,68 | 4,29 | 1,56 | 16,59 | 22,02 | 6,43 |
| `left_shoulder_pitch` | 1,71 | 0,59 | 0,34 | 0,46 | 2,56 | 0,88 |
| `left_shoulder_roll` | 1,27 | 0,48 | 0,16 | 0,11 | 1,90 | 0,72 |
| `left_shoulder_yaw_drive` | 0,10 | 0,05 | 0,00 | 0,00 | 0,14 | 0,07 |
| `left_elbow_roll` | 0,27 | 0,20 | 0,00 | 0,00 | 0,40 | 0,30 |
| `left_elbow_yaw_drive` | 0,01 | 0,00 | 0,00 | 0,00 | 0,01 | 0,01 |
| `left_wrist_pitch_drive` | 0,01 | 0,01 | 0,00 | 0,00 | 0,02 | 0,01 |
| `left_wrist_roll` | 0,02 | 0,01 | 0,00 | 0,00 | 0,03 | 0,01 |
| `right_shoulder_pitch` | 1,09 | 0,49 | 0,16 | 0,13 | 1,64 | 0,73 |
| `right_shoulder_roll` | 1,37 | 0,61 | 0,20 | 0,23 | 2,05 | 0,91 |
| `right_shoulder_yaw_drive` | 0,07 | 0,04 | 0,00 | 0,00 | 0,10 | 0,06 |
| `right_elbow_roll` | 0,27 | 0,22 | 0,01 | 0,00 | 0,41 | 0,33 |
| `right_elbow_yaw_drive` | 0,01 | 0,00 | 0,00 | 0,00 | 0,01 | 0,01 |
| `right_wrist_pitch_drive` | 0,01 | 0,01 | 0,00 | 0,00 | 0,02 | 0,01 |
| `right_wrist_roll` | 0,01 | 0,01 | 0,00 | 0,00 | 0,02 | 0,01 |

---

## 4 — Regroupement par zone, et le besoin P2 v1

### P2 v1 : les 12 DDL de jambe

Pour chaque articulation, **le pire des deux côtés** (Déd) :

| Articulation (×2) | τ pointe P2 N·m | τ RMS P2 N·m | τ pointe P2 × 1,5 | τ RMS P2 × 1,5 | ω pointe P2 rad/s | P pointe P2 W | écrêtée en P1 ? |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `hip_pitch` | 7,27 | 2,45 | 10,91 | 3,68 | 2,00 | 12,60 | **oui, 2,4 % du temps** — borne basse |
| `hip_roll` | 14,68 | 5,35 | 22,02 | 8,02 | 2,08 | 11,05 | **oui, 17,2 % du temps** — borne basse |
| `hip_yaw_drive` | 9,58 | 2,08 | 14,37 | 3,11 | 1,07 | 3,19 | **oui, 10,9 % du temps** — borne basse |
| `knee` | 14,68 | 5,11 | 22,02 | 7,66 | 3,41 | 27,16 | **oui, 4,5 % du temps** — borne basse |
| `ankle_pitch` | 14,68 | 4,29 | 22,02 | 6,43 | 2,69 | 16,59 | marginal (0,3 %) |
| `ankle_roll` | 7,23 | 1,56 | 10,85 | 2,33 | 2,10 | 7,22 | non |

**Lecture (Déd)** :

- Quatre types d'articulation sur six ont été écrêtés en P1 : **leurs
  chiffres P2 sont des minimums.**
- Le genou, le tangage de cheville et le roulis de hanche ont la même
  pointe P2, 14,68 N·m. Ce n'est pas une coïncidence : **c'est la même
  borne de freinage de 2,2 N·m, multipliée par le même facteur**.
- Le RMS, la grandeur qui chauffe, est de **5,35 N·m au plus** en P2
  (roulis de hanche), soit **8,02 N·m avec le facteur 1,5**. C'est lui qu'il faudra comparer au
  couple **continu** d'un moteur candidat (fiche 0038). La pointe, elle,
  se compare au couple **crête**.

### Toutes les zones

| Zone | DDL | Σ τ pointe P2 N·m | τ pointe P2 max N·m | τ RMS P2 max N·m | P pointe P2 max W | dans P2 v1 ? |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| jambes | 12 | 124,43 | 14,68 | 5,35 | 27,16 | **oui — 12 DDL** |
| taille | 2 | 3,47 | 1,74 | 0,68 | 0,24 | non |
| cou | 2 | 0,75 | 0,66 | 0,38 | 0,01 | non |
| bras | 14 | 6,22 | 1,71 | 0,61 | 0,46 | non |

La somme des pointes n'est pas une pointe simultanée : c'est un ordre de
grandeur du couple installé.

---

## Ce que ce document ne dit pas

- **Le besoin réel des articulations écrêtées.** Pour l'obtenir, il
  faudrait relancer la marche avec des bornes de moteur desserrées,
  comme le fait `enveloppes_actionneurs.py` pour les poses. Mais la
  politique a été apprise *avec* ces bornes, et elle marcherait
  peut-être autrement sans elles.
- **Le rapport cyclique et l'échauffement** : c'est le sujet de la
  fiche 0038, toujours proposée.
- **Un choix de moteur.** Aucun n'est proposé.
