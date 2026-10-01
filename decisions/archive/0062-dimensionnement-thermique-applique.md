# 0062 — Dimensionner au couple efficace et au seuil thermique : ce qui est appliqué

Date : 2026-09-30
Espèce : gouvernante
État : appliquée
Statut : **appliquée** — lot de cohérence validé par Jeremy le 2026-09-30 (~23 h), points 4 et 7. La 0038 était à accepter (point 7), mais **elle est contredite** : elle est remplacée, pas acceptée.
Remplace : `0038-dimensionnement-thermique.md`

## Pourquoi remplacer la 0038 au lieu de l'accepter

La 0038, **proposée**, instruisait la thermique sans rien trancher.
Depuis, plusieurs de ses énoncés sont **dépassés ou contredits** :

- son § 3 dit : « la série temporelle des couples n'existe pas ». **Elle
  existe** (`sim/upstream/enregistrer_marche.py`, fiche 0049) ;
- son § 4 pose la question « 3 classes (× 4,0) ou 4 (× 2,5) ». Les
  classes sont désormais les **tailles** (0048), et la taille est une
  sortie du calcul (0047).

Accepter la 0038 telle quelle ferait accepter ces énoncés. Elle est donc
remplacée par ce qui est réellement appliqué.

## La décision (ce qui est appliqué)

1. **Le couple efficace (RMS) compte autant que la pointe.** Chaque
   articulation doit respecter : marge × RMS requis ≤ couple continu,
   et marge × pointe ≤ couple de pointe. Voir `scripts/dimensionnement.py`
   (docstring, et contraintes l. 39) et la fiche 0051 (marge 1,5).
2. **Un seul seuil thermique**, celui du protocole de banc : la
   protection du constructeur moins 10 °C. Il sert à l'estimation
   (`scripts/estimation_thermique.py`) et au critère d'abandon
   (`criteres_selection.yaml`, `banc.critere_abandon`). C'est **proposé**
   avec le protocole, **appliqué** dans le calcul.
3. **La condition de mesure accompagne toujours un couple continu** :
   plaque, rotation ou blocage, tension (`params/actionneurs.yaml`). Le
   facteur k porte l'incertitude qui reste.

## Ce qui reste ouvert (repris de la 0038)

- **Conductivité thermique des matières** (0038 § 5). Un moteur sur du
  carton est enfermé dans sa propre chaleur. Le champ
  `conductivite_thermique` n'est **pas créé** ; les valeurs d'ordre de
  grandeur de la 0038 ne sont pas sourcées.
- **Modèle bobinage-carter** : le capteur de température d'un
  actionneur ne mesure pas forcément le bobinage (thèse Forget, § 5.2 ;
  à reprendre dans le protocole de banc).
