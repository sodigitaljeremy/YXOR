# Vision produit : la gamme YXOR

**Rédigé le 2026-10-08** (document écrit, pas engendré). C'est un **cadre de réflexion** : rien n'y est décidé
au-delà de la fiche [0073](../decisions/0073-gamme-yxor.md). Tout le reste est **PROPOSÉ**, et se tranche par
Jeremy, une question à la fois.

## Ce qui est décidé

Fiche 0073, **décidée par Jeremy le 2026-10-08**, ses mots : « La gamme YXOR comprend quatre modèles : YXOR Kit,
YXOR Lab, YXOR Home et YXOR Pro ; YXOR Pro remplace ce que nous appelions YXOR final. Le projet est personnel,
non commercial et open source. Le budget de chaque modèle est calculé selon ses capacités et ses contraintes. Je
suis le premier utilisateur, et YXOR Kit est le premier modèle que je fabrique. Pour YXOR Lab, le saut est
ramené à 5 cm. »

Elle s'ajoute à ce qui tient déjà : un robot sur batterie (0070), l'autonomie et l'IA du Lab et du Pro (0071),
le 12S coupé à 3,0 V (0072 et journal du 2026-10-08), la famille RobStride et la même organisation d'axes pour
tous (0069).

L'idée de départ, en mots de Jeremy (2026-10-08) : « définir une évolution de YXOR en fonction de ses capacités
et fonctionnalités », des modèles adaptés à des publics « tout en prenant compte des limites et contraintes
qu'elles impliquent », un « design unique », une conception « éco-responsable, éthique », des éléments
« réutilisables, facilement interchangeables », et un YXOR « full carton » à faire chez soi, enrichi de modules.

## Les quatre modèles

| Modèle | Public (PROPOSÉ) | Ce qu'on sait déjà | Ce qui reste à définir |
| --- | --- | --- | --- |
| **YXOR Kit** | soi-même d'abord (Jeremy), puis des fabricants amateurs, en famille ou à l'école | le premier fabriqué ; « full carton » à faire chez soi, enrichi de modules | ses capacités (profil `kit` VIDE dans `params/capacites.yaml`), son matériau, ses actionneurs, son alimentation, sa taille |
| **YXOR Lab** | l'apprentissage : marche, relevé, politiques, banc | profil DÉCIDÉ (2026-10-07, saut 5 cm le 2026-10-08) ; résultats de l'explorateur ci-dessous | les capacités non calculées (sol irrégulier, pente, visage) ; les données de la chaîne de puissance |
| **YXOR Home** | un usage à la maison (PROPOSÉ : gestes, présence, petite manipulation) | le nom et sa place dans la gamme | tout : profil `home` VIDE |
| **YXOR Pro** | le robot complet de la fiche 0069 | profil `pro` (ex-« final ») : toutes les capacités de la 0069, buste à 3 axes, autonomie 60 min, modèle de langage local | les niveaux de chaque tâche (phase 4b) ; sa taille et ses actionneurs |

### Ce que l'explorateur dit du Lab (2026-10-08, 14 h, `docs/explorateur-lab-2026-10.md`)

Meilleure solution RobStride, 12S coupé à 3,0 V, chaîne de puissance COMPACTE (PROPOSÉE) :

| Fréquence de commande | Masse | Coût total | Hauteur réelle | Volume électronique | Batterie |
| ---: | ---: | ---: | ---: | ---: | --- |
| 250 Hz | 13,6 kg | ≥ 4 275 CHF | 0,715 m | 1,91 L (partiel) | Molicel P42A 12S2P, 353 Wh |
| 500 Hz | 18,6 kg | ≥ 5 238 CHF | 0,850 m | 3,02 L (partiel) | Molicel P50B 12S2P, 420 Wh |

Elle tient les 8 capacités calculées du profil (marche 0,6 m/s, relevé, **saut 5 cm**, gestes 2 m/s, saisie
0,2 kg, poussée 20 N, buste, tête). À 13 h 47, avec un saut de 10 cm que rien ne tenait, la meilleure s'en
passait : 11,5 kg, ≥ 3 955 CHF, 0,664 m. **Le saut de 5 cm coûte donc environ +320 CHF, +2,1 kg et +5 cm**
(250 Hz), surtout par la batterie (2P au lieu de 1P, pour le courant de pointe de la poussée). « ≥ » : le prix
de l'absorbeur de régénération n'est pas publié ; « partiel » : des cotes manquent (BMS, anti-étincelle).

### La carte des capacités : ce qui sépare deux modèles

Coût marginal de chaque capacité, profil Lab (explorateur, coût de chaque tâche) : la marche, le relevé, les
gestes, la saisie et la tête coûtent **presque rien de plus** que la marche seule (quelques dizaines de francs,
quelques centaines de grammes). Les **sauts de coût**, ceux qui pourraient séparer deux modèles, sont :

- **le saut** : 5 cm tient avec des RobStride ; 10 cm non, dans le robot complet, sauf en assouplissant des
  hypothèses (`docs/saut-accroupi-2026-10.md`) ;
- **la poussée et le port de charges** : ils imposent une masse minimale (équilibre, frottement) ; 100 N de
  poussée et 10 kg portés sont hors de portée d'un robot de cette taille ;
- **le buste à 3 axes** : il allonge le tronc (hanche et taille empilées) ; réservé au Pro ;
- **l'IA embarquée** : de « commande + vision » (environ 500 CHF de calculateur) au modèle de langage local
  (un autre calculateur, une autre consommation) ;
- **la fréquence de commande** : 500 Hz demande 6 à 7 canaux CAN, 250 Hz en demande 3 à 4 ;
- **ce qui n'est pas calculé** : sol irrégulier, pente, course, mains à doigts, visage (simulations ou données
  à produire).

## « Design unique » : ce que ça peut vouloir dire

**Une même famille, pas les mêmes pièces.**

- **Ce qui peut être commun à toute la gamme** : la topologie (l'organisation des axes : le Lab est un
  sous-ensemble du Pro, fiche 0069), les **noms d'axes** (`params/joints.yaml`, règle 3), le logiciel (une
  chaîne de commande, une politique transférable), le bus (CAN, protocole RobStride), les connecteurs, les
  **modules** (une articulation, une main, une tête, un pack de batterie, une carte de calcul), l'identité
  visuelle (silhouette, proportions ANSUR, couleurs, matières).
- **Ce qui ne peut pas l'être : les mêmes pièces à toutes les tailles.** La masse ne croît pas comme la taille au
  cube (loi allométrique, b ≈ 2, décidée le 2026-10-07), le couple croît plus vite que la taille, et les
  épaisseurs, axes et fixations dépendent d'une charge, pas d'un facteur d'échelle (fiche 0013). Une pièce du
  Kit agrandie ne fait pas une pièce du Pro.

## Éco-conception et réparabilité (PROPOSÉ)

- **Fixations standard** : vis traversantes et écrous (déjà une règle du projet), métriques ISO, peu de
  références différentes.
- **Pas de colle structurelle** (déjà une règle) : tout se démonte, se répare, se trie en fin de vie.
- **Batterie remplaçable** : un pack accessible, débranchable sans outil spécial, de cellules courantes (21700) ;
  aucune cellule de récupération ou d'occasion (règle du lot 4a sexies).
- **Composants courants** : actionneurs, servos, calculateurs, convertisseurs achetables chez plusieurs
  distributeurs ; un composant introuvable est un risque de réparabilité.
- **Matières** : aluminium (recyclable), carton (Kit), impression 3D seulement avec une machine vérifiée
  (fiche 0059) ; éviter les mélanges de matières collées.
- **Modules interchangeables** : une articulation, un bras ou une tête se remplacent sans refaire le robot.
- **Documentation** : selon la DIN SPEC 3105 (exigences de documentation du matériel ouvert) et la définition
  OSHWA (fichiers source modifiables, nomenclature) ; le code build123d est déjà la « forme modifiable ». Ces deux
  références sont citées par des rapports secondaires ; leurs textes n'ont pas été relus ici.

## YXOR Kit : le robot en carton

**Ce qui existe** : la jambe basse en carton plume de 5 mm (`parts/jambe_basse.py`) : pied, cheville, tibia en
caisson, chape de genou, actionneurs factices ronds ; plan A4 de 6 feuilles (32 pièces, bandes de papier
comprises, journal du 2026-10-04) ; débattements de la maquette mesurés (genou −105..0°, tangage −95..55°). Le
carton y est une **maquette de forme, sans métrologie** (fiche 0060) : il vérifie une forme, jamais une cote.

**Ce qu'un robot en carton peut faire**, par étage (PROPOSÉ, rien n'est calculé) :

| Étage | Ce qu'il peut faire | Ce qu'il demande |
| --- | --- | --- |
| sans moteur | un mannequin articulé : poses, proportions, apprentissage du montage, des noms d'axes, de la cinématique | des articulations à friction ou à crans, des axes, des vis |
| avec servos | des gestes, une tête qui tourne, des bras qui pointent ; marcher reste incertain (masse, rigidité du carton, couple des servos) | des servos à bus (Feetech, Dynamixel), une alimentation 6–12 V, un adaptateur série |
| avec calculateur | une commande par programme, des séquences, la vision ; les mêmes logiciels que le Lab, à petite échelle | un calculateur (Raspberry Pi ou Jetson), une batterie, une coupure |

**Questions ouvertes** (à trancher avec Jeremy) :

- **matériau** : un carton, découpé aux outils du ménage (fiche 0074) ; lequel : classement PROPOSÉ dans
  `docs/kit-yxor.md`, essais dans `docs/protocole-carton.md` ;
- **solidité** : quelle masse et quel couple le carton tient-il aux liaisons (trous, tenons) ? à mesurer sur
  éprouvette, jamais à supposer ;
- **servos** : lesquels ? leur couple continu est désormais connu pour les Feetech (fiches lues le 2026-10-07) ;
- **alimentation** : batterie (laquelle, quel BMS) ou bloc secteur pour un Kit d'atelier ? la fiche 0070
  (batterie) porte sur le Lab et le Pro : s'applique-t-elle au Kit ?
- **taille** : **la même que le Lab**, décidé par Jeremy le 2026-10-08 (fiche 0074) ;
- **modules** : **des modules successifs**, décidé par Jeremy le 2026-10-08 (fiche 0074) ; leur découpage
  (niveaux 0 à 4) est PROPOSÉ, étudié dans `docs/kit-yxor.md`.

## Open source : les licences à étudier (sans choisir)

Décision en vigueur : **« aucune licence pour l'instant »** (Jeremy, 2026-09-30, fiche archivée 0063). Le choix se
fera par une fiche. Familles à étudier, par objet :

| Objet | Licences possibles | À vérifier |
| --- | --- | --- |
| matériel (plans, CAO) | CERN-OHL-P (permissive), CERN-OHL-W (faiblement réciproque), CERN-OHL-S (fortement réciproque), Solderpad | la règle du projet écarte le **copyleft fort dans le cœur** : la CERN-OHL-S y tombe-t-elle ? (CLAUDE.md) |
| logiciel | MIT, Apache-2.0, BSD ; GPL/AGPL écartées du cœur par la même règle | les dépendances (build123d, MuJoCo : Apache-2.0) |
| documentation | CC BY 4.0, CC BY-SA 4.0 | la clause SA et la règle du copyleft fort |

Contrainte qui ne dépend d'aucun choix : la mécanique amont de ToddlerBot est en **CC BY-NC-SA 4.0** ; aucune
géométrie amont n'entre dans une pièce YXOR (fiches 0055 et 0061). La question des valeurs numériques extraites
reste ouverte (fiche 0010, § 4).

## Le site pour les fabricants du Kit : les besoins (rien n'est construit)

- les **plans** imprimables par format (A4, A3) et par matériau, avec leur empreinte (le site sert le dépôt) ;
- la **nomenclature** (vis, servos, électronique) avec des références courantes, sans lien d'achat imposé ;
- les **instructions de montage**, étape par étape, illustrées par les rendus de la CAO ;
- les **réglages** : épaisseur et saignée par machine et matériau (déjà des paramètres du projet) ;
- la **sécurité** : batterie, coupure, couple des servos, âge et accompagnement ;
- les **modules** et leur compatibilité (quel module va sur quel Kit) ;
- un moyen de **retour** des fabricants (photos, défauts, améliorations) ;
- les **licences** et l'attribution, une fois choisies.

## Questions que ce document ne tranche pas

Le public de chaque modèle ; les capacités du Kit et du Home ; le carton précis du Kit ; les licences ; l'ordre des
modèles après le Kit ; ce que « éco-responsable » exige de mesurable (masse de matière, part recyclable,
durée de vie, réparabilité notée).
