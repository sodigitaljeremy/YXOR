# Glossaire

Une ligne par terme. À enrichir à chaque fois qu'un mot inconnu apparaît.

## Structure du robot

**Degré de liberté (DDL)** — Un mouvement indépendant possible. Une charnière
de porte a 1 DDL. Chaque DDL correspond à un moteur. YXOR en a **12 en v1**
(6 par jambe, sans bras) et 18 à 20 en v2 (bras et cou) ; ToddlerBot en a 30.

**Liaison / joint** — L'articulation entre deux pièces. Porte un nom, un axe
de rotation et deux butées.

**Segment / link** — La pièce rigide entre deux articulations. Cuisse, tibia,
avant-bras sont des segments.

**Butée** — Angle minimum et maximum qu'une articulation peut atteindre.
Dépasser une butée casse la mécanique.

**Liaison parallèle** — Montage où le moteur est déporté loin de
l'articulation qu'il actionne, relié par une bielle. Réduit l'inertie du
segment mobile, donc la puissance nécessaire.

## Modèles et fichiers

**URDF** — Fichier texte décrivant le robot pour un simulateur : segments,
articulations, masses, inerties. Le standard du domaine.

**MJCF** — Même idée, format propre au simulateur MuJoCo.

**STEP** — Format d'échange de géométrie exacte, lisible par tous les
logiciels de mécanique. Le format à envoyer à un fabricant.

**STL** — Géométrie approximée par des triangles. Bon pour imprimer, mauvais
pour modifier.

**DXF** — Dessin 2D. Le format des pièces à découper.

**Jumeau numérique** — Le modèle simulé, censé se comporter comme le robot
réel.

## Apprentissage

**Politique** — Le programme entraîné qui décide, à chaque instant, quel
angle envoyer à chaque moteur. C'est « le cerveau de la marche ».

**Apprentissage par renforcement (RL)** — Méthode d'entraînement par essai et
erreur : le robot tente, reçoit une récompense, recommence des millions de
fois en simulation.

**Sim-to-real** — Le transfert d'une politique apprise en simulation vers le
robot physique. C'est là que tout échoue habituellement.

**Randomisation de domaine** — On fait varier aléatoirement les paramètres de
la simulation (frottements, masses, retards) pour que la politique apprise
résiste aux écarts du monde réel.

**ONNX** — Format d'export d'un modèle entraîné, exécutable sur une petite
carte embarquée.

**Identification d'actionneur** — Mesurer le comportement réel des moteurs
pour que le simulateur les reproduise fidèlement.

## Mécanique

**Couple** — L'effort de rotation, en newton-mètres. Ce qui détermine si un
moteur peut soulever un segment.

**Inertie** — La résistance d'une pièce à être mise en mouvement. Une masse
loin de l'axe de rotation coûte beaucoup plus cher qu'une masse proche.

**Loi carré-cube** — En multipliant les dimensions par k, la surface varie en
k², le volume et la masse en k³, et le couple requis en k⁴. C'est pourquoi un
robot deux fois plus grand n'est pas « le même en plus grand ».

**Insert à chaud** — Bague filetée métallique enfoncée au fer dans une pièce
plastique, pour y visser sans arracher la matière.

**Saignée (kerf)** — La largeur de matière consommée par un outil de découpe.
À compenser dans les cotes.