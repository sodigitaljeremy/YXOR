# 0074 — YXOR Kit : modules successifs, mêmes dimensions et composants que le Lab, carton et outils du ménage

Date : 2026-10-08
État : acceptée
Complète : `0073-gamme-yxor.md` (dont elle remplit en partie le « Ce qui
n'est PAS décidé » : la structure du Kit, sa taille, son matériau ; la 0073
reste en vigueur pour tout le reste).

Décision coûteuse à inverser (règle 5) : elle fixe l'architecture du Kit
(des modules successifs), sa taille et son squelette (ceux du Lab), donc
ses interfaces avec le Lab, et ce que l'utilisateur achète en premier.
Revenir dessus après la fabrication changerait les plans, la nomenclature
et ce qui se réutilise.

## Décision

**DÉCIDÉE par Jeremy le 2026-10-08.** Ses mots (prompt « Étude de YXOR
Kit », 2026-10-08) :

- « Je veux tous les niveaux comme modules successifs. »
- « Il est particulièrement judicieux et pertinent d'adopter les mêmes
  dimensions, taille et composants que pour YXOR Lab, afin que
  l'investissement initial de l'utilisateur dans les différents éléments
  soit au maximum réutilisable et exploitable pour le modèle suivant »
  (référence citée par Jeremy : la philosophie de Framework et de
  Fairphone).
- Matériau : « le carton le mieux adapté, qui répond le mieux à tous les
  critères, limites et contraintes ».
- Outils : « le strict minimum : un cutter, une règle, une équerre, voire
  un pistolet à colle ; des outils accessibles et abordables pour tous les
  ménages ».

Ce qui en découle :

- **Le Kit est une suite de modules**, chacun s'ajoutant au précédent sans
  le refaire.
- **Même taille, même squelette, mêmes composants que le Lab** partout où
  c'est possible ; ce qui ne l'est pas est dit, composant par composant
  (`docs/kit-etude-2026-10.md`, matrice de réutilisation).
- **Matériau : un carton**, choisi sur des critères écrits (étude de marché
  du 2026-10-08) ; le choix final reste à Jeremy.
- **Outils : cutter, règle, équerre, éventuellement pistolet à colle.**
  Aucune pièce du Kit ne demande une machine (ni laser, ni imprimante, ni
  perceuse à colonne).

## Ce qui est PROPOSÉ, pas décidé

- **Les niveaux** (dans `params/capacites.yaml`, profil `kit`) : 0 articulé
  (passif), 1 animé (tête et bras), 2 interactif (vision, voix, IA),
  3 debout (jambes motorisées), 4 passage au Lab (aluminium et RobStride).
  Le découpage est celui du prompt, que Jeremy a écrit comme une
  proposition à inscrire.
- **Le carton retenu** : un classement selon des critères PROPOSÉS ; à
  trancher par Jeremy, après les essais à la maison
  (`docs/protocole-carton.md`).
- **La place de la colle** : le document de vision dit « pas de colle
  structurelle » (PROPOSÉ, non décidé), le prompt cite le pistolet à colle.
  Les options sont dans l'étude ; Jeremy arbitre.

## Ce qui n'est PAS décidé

- La taille du Lab elle-même : c'est une sortie de l'explorateur (fiche
  0047). Le Kit la suit ; tant qu'elle n'est pas arrêtée, l'étude prend
  le squelette à `H_S` (`params/anthropometry.yaml`).
- Les servos du Kit, sa batterie, son calculateur : l'étude les compare,
  elle ne les choisit pas. Aucun achat (fiche 0066).

## Conséquence connue dès maintenant

« Mêmes composants que le Lab » ne peut pas valoir pour les **actionneurs**
tant que le niveau 4 est « passage aux RobStride » : un servo Feetech du
Kit n'est pas un actionneur du Lab. La matrice de réutilisation le chiffre.
