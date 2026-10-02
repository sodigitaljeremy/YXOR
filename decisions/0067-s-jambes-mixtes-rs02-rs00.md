# 0067 — S : jambes mixtes, RS02 au roulis et au tangage de hanche et au genou, RS00 ailleurs

Date : 2026-10-02
État : acceptée
Remplace : `0065-s-robstride-rs00.md`

Décision coûteuse à inverser (règle 5) : elle fixe deux interfaces
d'actionneur dans la jambe, donc la structure, les brides et le câblage.

## Décision

**DÉCIDÉE par Jeremy le 2026-10-02.** Ses mots : « Je pars sur l'option
B. » La source est le prompt du 2026-10-02 ; l'option B est le calcul de
Claude Code du 2026-10-02 à 19 h 38 (journal du jour).

| Articulation (par jambe) | Actionneur |
| --- | --- |
| roulis de hanche (`hip_roll`) | **RobStride RS02** |
| tangage de hanche (`hip_pitch`) | **RobStride RS02** |
| genou (`knee`) | **RobStride RS02** |
| lacet de hanche (`hip_yaw_drive`) | RobStride RS00 |
| tangage et roulis de cheville (`ankle_pitch`, `ankle_roll`) | RobStride RS00 |

- Famille RobStride inchangée (même bus CAN, même protocole) ; **H_S =
  0,60 m**, **repli 0,55 m** inchangé.
- La configuration est une donnée unique : `params/configuration_S.yaml`,
  vérifiée par `scripts/choix_actionneurs.py`.

## Pourquoi

Calcul du 2026-10-02 (19 h 38), base v1 sans les 20 servos ToddlerBot du
haut du corps ; masses ajoutées de B et de C : hypothèses (60 g de
structure par articulation dessinée pour le RS02, 57 g d'adaptateur pour
C).

| Option | Masse v1 | Coût v1 (CHF HT) | Passage à la v3 | H_max v3 | H_max v3, roulis +40 % |
| --- | ---: | ---: | ---: | ---: | ---: |
| A, tout-RS00 | 6,75 kg | 1 252 | + 1 469 | 0,594 m | 0,463 m |
| **B, mixte** | **7,41 kg** | **1 432** | **+ 1 469** | **0,658 m** | **0,639 m** |
| C, RS00 dans une structure RS02 | 7,45 kg | 1 252 + adaptateurs | + 2 275 | 0,658 m | 0,572 m (v1) |

Le roulis de hanche, saturé 17 % du temps dans la marche de référence,
limite A et C ; en B, il n'est plus limitant jusqu'à +20 % de besoin.

## Écarté

- **A, tout-RS00** : la v3 ne tient que 0,594 m, et tombe à 0,46 m si le
  roulis de hanche demande 40 % de plus. Fragile.
- **C, RS00 monté dans une structure dessinée pour le RS02** : passage à
  la v3 plus cher (2 275 CHF contre 1 469), et aussi fragile que A tant
  que le passage n'est pas fait.
- **RS03 au tangage de hanche et au genou** : 900 g pièce, il fait
  reculer toutes les versions.

## Hypothèses, marquées comme telles

- **Haut du corps de la v3 en RS05** (16 actionneurs) : les tâches des
  bras ne sont pas définies ; leur couple n'est pas vérifié.
- **Une seule marche de référence**, celle de ToddlerBot, où le roulis de
  hanche est saturé 17 % du temps à gauche : les besoins sont des
  minimums.
- **Masses de structure et charge utile de S inchangées** (structure de
  ToddlerBot mise à l'échelle, 1,2 kg de charge utile).

## Articulation limitante

En B, c'est le **tangage de cheville**, en RS00.

## Questions ouvertes

- **La composition du banc** (fiche 0066) ne couvre que le RS00 : à revoir
  pour le RS02.
- **Une seconde marche de référence avant l'achat des 12 moteurs** :
  PROPOSÉ par Claude, non décidé.

## Ce qui la rouvrirait

Une mesure au banc sous les valeurs publiées du RS00 ou du RS02 ; une
seconde marche qui ferait limiter une articulation en RS00 sous 0,60 m ;
des tâches de bras qui exigent plus que des RS05.
