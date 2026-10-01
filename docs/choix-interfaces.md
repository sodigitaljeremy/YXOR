# Choix des interfaces d'actionneur — comparaison rédigée

**Rédigé le 2026-09-30.** Il n'y a pas de score : c'est une comparaison
écrite, qui prépare une décision de Jeremy sans la prendre. Elle
complète le cadrage, § 7 (interfaces, *proposé*), et le § 9 du cadrage archivé (étude
fournisseurs). Aucune fiche.

Statuts : **V** = vérifié dans le dépôt ou à la source citée ; **Déd** =
raisonnement ; **CG** = connaissance générale, non vérifiée dans le
dépôt.

---

## Deux faits qui pèsent sur tout le reste

**1. Le couple continu dépend de la plaque sur laquelle l'actionneur est
monté (V).** Le couple continu du RS05 (1,8 N·m) est mesuré à 100 rpm,
l'actionneur étant fixé sur une **plaque d'aluminium de 150 × 150 mm**
(PDF RobStride du 2026-09-17, p. 27). Le même PDF donne 1,2 N·m en
blocage (p. 29). Le RS06 et le RS03 sont mesurés sur 200 × 200 mm.

**La pièce qui porte l'actionneur fait donc partie de son
refroidissement.** Monté sur une pièce en plastique ou en carton, un
actionneur dissipe moins que sur sa fiche, et son couple continu réel
est plus bas (Déd). Ce point pèse sur l'interface mécanique.

**2. Un intermédiaire logiciel tiers peut être faux sans le dire.**
Selon l'étude fournisseurs (`docs/sources/etude-fournisseurs-chatgpt-2026-09-30.md`,
source externe non vérifiée), le backend RobStride de LeRobot employait
en 2026 un framing de type Damiao : il ne dialoguait pas correctement
avec le matériel réel. Le moteur n'était pas en cause, c'était
l'intégration. Ce point pèse sur l'interface logicielle.

---

## Interface mécanique

| | **A — dessiner autour d'un modèle** | **B — interface YXOR + un adaptateur par modèle** | **C — boîtier maison** |
| --- | --- | --- | --- |
| **Principe** | la jambe reprend directement la bride du modèle acheté | la jambe porte une bride propre à YXOR ; une plaque adaptatrice par modèle | YXOR conçoit le boîtier de l'actionneur (fiche 0052) |
| **Coût** | le plus bas : aucune pièce en plus | une pièce de plus par articulation, soit 12 en v1 | le plus élevé : moteur, réducteur, roulements, codeurs, électronique |
| **Masse et rigidité** | les meilleures : un seul assemblage | une pièce et un assemblage boulonné de plus. Jeu et souplesse possibles, à mesurer | à concevoir ; rien n'est acquis |
| **Temps de développement** | le plus court | court : l'interface une fois, puis un adaptateur par modèle | le plus long, et hors chemin critique par décision (0052) |
| **Liberté fournisseur** | nulle : changer de modèle, c'est redessiner la jambe | élevée : changer de modèle, c'est une plaque | totale |
| **Apprentissage** | faible | concevoir une interface stable | maximal : c'est un projet en soi (cadrage § 6) |
| **Réversibilité** | faible | élevée | élevée, mais au prix de tout le développement |
| **Dissipation thermique** | la pièce de jambe fait office de plaque : sa matière et sa surface fixent le continu réel | **l'adaptateur peut servir de dissipateur** : en aluminium usiné, il se rapproche de la condition de la fiche | à concevoir, comme le reste |

### Lecture (Déd)

- **A est le plus simple, et c'est lui qui enferme le plus.** Aucun
  fabricant n'a de bride commune entre classes (étude, § 1 ; cadrage
  § 9). Passer de S à M avec A, c'est redessiner la jambe.
- **B paie une pièce et un assemblage de plus**, et gagne l'indépendance
  vis-à-vis du fournisseur. C'est aussi la seule option où l'interface
  commune de la fiche 0052 (actionneur maison) a un sens : l'actionneur
  maison se monte sur la même bride YXOR que l'actionneur acheté.
- **La thermique donne un argument à B qu'on ne voit pas au premier
  regard.** Une plaque adaptatrice en aluminium est à la fois
  l'adaptateur et le dissipateur. Et la fabrication séquencée (fiche
  0050) commence justement par l'usinage.
- **C n'est pas une option pour la v1** : la fiche 0052 le met hors du
  chemin critique. Il reste l'horizon de B.

---

## Interface logicielle

| | **1 — couche propre à YXOR** | **2 — ros2_control** | **3 — couche propre alignée sur les concepts de ros2_control** |
| --- | --- | --- | --- |
| **Principe** | `joint.command(position, vitesse, couple)`, un backend par fabricant, un backend MuJoCo (cadrage § 7) | le cadre de commande de ROS 2 : composants matériels, interfaces de commande et d'état, contrôleurs (CG) | la couche 1, mais avec le vocabulaire de ros2_control : interfaces `position` / `velocity` / `effort`, séparation composant matériel / contrôleur |
| **Coût** | nul en licence ; du temps de développement | nul en licence ; une pile lourde à installer et à faire tourner sur le calculateur embarqué (CG) | comme 1 |
| **Temps de développement** | un pilote par fabricant à écrire et à tester sur le matériel | contrôleurs existants ; mais un *hardware interface* par actionneur à trouver ou à écrire, de qualité variable (CG) | comme 1, plus un peu de discipline de conception ; passer à 2 plus tard ne demande qu'une couche mince |
| **Liberté fournisseur** | totale : un backend de plus | totale en principe ; en pratique, dépend des interfaces existantes | totale |
| **Apprentissage** | élevé et direct : on écrit ce qu'on comprend | élevé mais indirect : on apprend un cadre avant son robot | élevé, et l'on apprend aussi le vocabulaire standard |
| **Réversibilité** | élevée vers 3 ; une réécriture vers 2 | faible : tout le robot s'organise autour de ROS | **élevée dans les deux sens** |
| **Le cas LeRobot** | le pilote est écrit **et vérifié sur le matériel** par YXOR : l'erreur se voit au banc | un pilote communautaire peut être faux sans le dire, comme celui de LeRobot | comme 1 |

### Lecture (Déd)

- **Le cas LeRobot ne condamne pas les intermédiaires : il condamne le
  fait de ne pas vérifier.** Quelle que soit l'option, le premier usage
  du banc (échelon 0, cadrage § 8) est de vérifier que le pilote
  envoie et relit ce que la fiche dit.
- **2 apporte des contrôleurs et un écosystème**, au prix d'une pile
  lourde et d'un apprentissage qui passe par le cadre avant le robot.
- **3 garde la simplicité de 1** et ne ferme pas la porte à 2. C'est
  l'option qui engage le moins, et c'est ce que l'étude appelle
  « décision fournisseur encore réversible » (étude, conclusion).
- Le backend MuJoCo existe dans 1 et 3 dès le départ. Il sert le
  principe « simulation d'abord » (cadrage § 1) : le même code de
  commande pilote la simulation et le banc.

---

## Ce que ce document ne dit pas

- **Aucune option n'est retenue.** Le choix revient à Jeremy.
- **La raideur et le jeu d'un adaptateur (B)** ne sont pas chiffrés : ils
  se mesureront au banc.
- **Le couple continu réel d'un actionneur monté sur une pièce YXOR**
  n'est connu pour aucun candidat. La fiche le donne sur plaque
  d'aluminium ; le banc le mesurera sur la vraie pièce.
- **ros2_control n'a pas été essayé** dans ce dépôt : tout ce qui le
  concerne ici est de la connaissance générale (CG).
