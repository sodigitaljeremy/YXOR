# 0069 — Deux robots, YXOR Lab et YXOR ; la gamme S/M/L/XL est abandonnée ; pièces hybrides dès maintenant

Date : 2026-10-05 (décision du 2026-10-04)
État : acceptée
Remplace : `archive/0048-tailles-par-classe.md` (tailles Banc, S, M, L,
XL ; premier robot S).
Remplace, pour l'ORDRE des procédés seulement :
`archive/0050-fabrication-sequencee.md` (l'hybride n'attend plus
l'usinage et l'impression ; le reste de la 0050 et de la 0060 tient).
Rend sans objet : la partie « tailles » de
`archive/0055-toddlerbot-reference-et-tailles.md` (ToddlerBot reste la
référence de calcul).

Décision coûteuse à inverser (règle 5) : elle change ce que le projet
construit, et tout ce qui porte le nom « S ».

## Décision

**DÉCIDÉE par Jeremy le 2026-10-04.** Ses mots :

- « Ok l'option c me semble très bien 👍 » : l'option C de Claude, deux
  robots, un robot cible complet et un robot laboratoire plus petit, qui
  partagent la famille d'actionneurs, le bus, le logiciel et la méthode ;
- « et l'on peut d'ailleurs directement opter pour la stratégie de
  conception et de modélisation via des pièces hybrides ».

Source : le prompt de Jeremy du 2026-10-05, qui cite ces mots du
2026-10-04.

## Ce que la décision contient

Le contenu détaillé de l'option C a été RÉDIGÉ PAR CLAUDE (règle 7) et
accepté par « Ok l'option c ». Il est consigné ici tel que le prompt le
donne ; chaque point reste à confirmer par Jeremy s'il le souhaite.

1. **La gamme S/M/L/XL est abandonnée.** Deux robots :
   - **YXOR Lab** : le robot d'apprentissage, plus petit ;
   - **YXOR** : le robot final, complet.

   Ces deux noms sont PROVISOIRES, PROPOSÉS par Claude.
2. **Méthode** : capacités → axes → plus petit actionneur par axe → plus
   petite taille où tout rentre et tient, avec marge. La taille reste une
   sortie du calcul (fiche 0047, inchangée).
3. **Capacités de YXOR (final)**, cochées par Jeremy le 2026-10-04 selon
   le prompt (la liste n'est pas dans ses mots) :
   - locomotion : marche sur sol plat, sur sol irrégulier et en pente ;
     relevé après une chute ; course et saut ;
   - bras et mains : gestes et pointage ; saisie et port de petits
     objets ; manipulation fine (mains à doigts) ; poussée et port de
     charges lourdes ;
   - buste et tête : rotation et inclinaison du buste ; orientation de la
     tête ; expressions du visage.
4. **Invariants entre les deux robots** :
   - famille RobStride (même bus CAN, même protocole) ;
   - même code de conception ;
   - même organisation et mêmes noms d'axes : le Lab est un
     SOUS-ENSEMBLE du robot final (règle 3) ;
   - même chaîne logicielle.
5. **Fabrication : pièces hybrides dès maintenant.** L'étape 3 de la 0050
   (hybride) est avancée. La découpe 2D reste une architecture possible
   parmi d'autres (0060).

## NON décidé

- **L'ensemble d'axes et la hauteur de YXOR Lab.** L'ensemble à 27 axes
  (jambes 6 × 2, taille 1, bras 5 × 2, pinces, cou 2) est une PROPOSITION
  de Claude (étude de session du 2026-10-04).
- **La fiche 0068 (cheville sans roulis) est À REVOIR** quand cet
  ensemble sera choisi. Elle n'est pas touchée ici, et reste en vigueur
  d'ici là.
- **Le sort de « S »** : les fiches 0067 (jambes mixtes RS02/RS00) et 0068
  portent sur S. Elles restent en vigueur jusqu'au choix de l'ensemble du
  Lab ; on ne sait pas encore si le Lab hérite de leur contenu.
- **Ce qu'est une pièce « hybride »** : la 0050 ne le définit pas (usinage
  et découpe ? plaques et impression ?). Si elle comprend de l'impression
  3D, la 0059 tient : l'impression ne s'applique qu'avec une machine
  disponible et vérifiée.
- **L'ensemble d'axes, la taille et les actionneurs de YXOR (final)**.

## Inventaire de ce qui dépend de S/M/L/XL

Rapport du 2026-10-05 (terminal et journal du jour) : rien n'est modifié
dans les paramètres, les scripts, les tests, le site ni les fiches.
