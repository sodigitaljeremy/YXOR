# 0065 — S : famille RobStride, RS00 sur les 12 articulations de jambe, H_S = 0,60 m

Date : 2026-10-01
État : remplacée
Remplacée par : `0067-s-jambes-mixtes-rs02-rs00.md` — configuration des jambes de S : RS02 au roulis et au tangage de hanche et au genou, RS00 ailleurs (Jeremy, 2026-10-02).

Première fiche écrite après la refonte. Selon la règle de la refonte
(décision 5, 2026-10-01), une fiche n'est écrite que pour une décision
coûteuse à inverser. C'est le cas ici : ce choix fixe les interfaces
mécaniques et électriques, le bus et le protocole.

## Décision

**DÉCIDÉE par Jeremy le 2026-10-01.** Ses mots : « Je valide ta
recommandation sur S. » La source est le prompt de la refonte R3, du
2026-10-01.

La recommandation qu'il valide a été **proposée par Claude (arbitrage)** :

1. **Famille RobStride, avec le RS00 comme membre S** : RS00 → RS02 →
   RS06.
2. **Le RS00 est identique sur les 12 articulations de jambe en v1.**
   - Un seul modèle, donc une seule interface et une seule procédure.
   - Les rechanges sont interchangeables.
   - Le banc est le robot.
   - Le mixte RS00 et RS05 reste une **option de v2**.
3. **La hauteur visée est H_S = 0,60 m**, le haut de la plage de la
   fiche 0048. Ce n'est pas la taille maximale du RS00. La marge ainsi
   gardée sert ce que le calcul ne compte pas encore : la charge utile,
   le relevé, les couples écrêtés de la marche de référence, une marche
   plus rapide, la chaleur.

## Conditions

- **(a) Recalcul à 0,60 m avec charge utile et relevé.** Si la marge ne
  tient pas, on redescend vers 0,55 m. Le recalcul est dans
  `docs/choix-actionneurs.md`, produit par `scripts/choix_actionneurs.py`.
- **(b) Le banc VÉRIFIE le RS00, il ne départage plus.** Sa composition
  reste à décider (`params/banc.yaml`).
- **(c) La version du RS00 se vérifie au moment d'un éventuel achat.**
  Le PDF RobStride du 2026-09-17, p. 38, en publie deux :
  - « ancien » : 5 / 14 N·m, 310 g ;
  - « nouveau » : 6 / 17 N·m, 330 g.

  Le catalogue retient la combinaison la plus prudente (fiche 0064) :
  5 / 14 N·m, blocage 3,6 N·m, 330 g.

## Pourquoi

Ce passage résume le comparatif du lot H, archivé dans
`archive/docs/choix-famille-actionneurs.md` :

- Le RS00 est le seul candidat S dont le couple **en blocage** est
  publié (3,6 N·m) et suffit à la taille S. Sa taille prudente (0,67 m)
  ne dépend donc d'aucune hypothèse sur k.
- Les autres candidats ne publient leur couple continu que dans des
  conditions non précisées : ils restent dépendants de k.
- La famille RobStride est en CAN, avec un protocole commun et une
  tension commune de 48 V de S à L.
- Le **prix à payer est la masse** : 330 g par articulation, contre
  191 g pour le RS05.

## Alternatives écartées

- **RobStride avec le RS05 ou l'EduLite 05 en S** : plus légers et moins
  chers, mais ils tiennent 0,48 à 0,54 m en prudent, sous la plage de S.
- **Damiao J4310 48 V** : ni valeur au blocage, ni garantie constructeur
  écrite trouvée.
- **CubeMars AK45-10** : en 24 V seulement, sans garantie écrite ni
  revendeur UE.
- **MyActuator** : trou de gamme en M.
- **HighTorque** : le constructeur ne publie que des couples de blocage ;
  protocole commun non déclaré.
- **Le mixte RS00 et RS05** : reporté en v2.

## Ce qui la rouvrirait

- **Une condition (a) en échec** : un FAIL à T1, T2 ou T5 à 0,60 m fait
  redescendre vers 0,55 m. Un FAIL à 0,55 m rouvre la décision.
- **Une mesure du banc** sous le couple au blocage publié, ou au-dessus
  de la protection thermique.
- **Une version achetable** différente des deux publiées, ou un RS00
  retiré de la vente.
