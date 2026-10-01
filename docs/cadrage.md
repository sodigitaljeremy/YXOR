# Cadrage du projet YXOR — vision et méthode

**Réduit le 2026-10-01** (refonte R5). La version complète du 30-09-2026,
avec ses résultats, son registre des arbitrages et ses questions ouvertes
de l'époque, est archivée : `archive/docs/cadrage-2026-09-30.md`.

**Ce document dit COMMENT YXOR se décide**, pas où il en est :

- **l'état courant** du robot est dans le [README](../README.md) ;
- **les décisions**, avec qui les a prises, sont dans
  [docs/decisions.md](decisions.md).

Une information courante n'existe qu'à un endroit. Statuts employés ici :
**décidé** (par Jeremy), **proposé** (en attente de décision).

---

## 1. Vision — *proposé, à valider par Jeremy*

> YXOR est un robot humanoïde bipède, conçu par Jeremy, dont chaque pièce
> lui appartient et est publiée librement, piloté par une IA embarquée
> locale, qui grandit par itérations : d'une articulation sur un banc
> jusqu'à un compagnon autonome. C'est aussi un parcours d'apprentissage de
> l'ingénierie robotique : chaque étape doit être comprise, pas seulement
> réalisée.

Principes :

1. **Simulation d'abord.** Chaque capacité est démontrée dans MuJoCo avant
   d'être construite.
2. **Une capacité à la fois**, avec un critère de réussite mesurable.
3. **Le besoin avant le catalogue.** On chiffre ce qu'il faut, puis on
   cherche ce qui existe.
4. **Fabrication séquencée** : usinage, puis impression 3D, puis hybride.
   Le carton sert de maquette rapide, sans métrologie.
5. **Outils libres**, tout décrit en texte dans le dépôt (*everything as
   code*, y compris ce document).
6. **Aucune géométrie amont** dans une pièce YXOR. La mécanique de
   ToddlerBot est en CC BY-NC-SA 4.0 : un dérivé hériterait de la licence.

---

## 2. La démarche inversée — *décidé le 30-09-2026*

**Principe.** On ne choisit plus une taille pour chercher ensuite des
actionneurs. Pour chaque **classe d'actionneur**, on calcule la **taille
maximale** que cette classe peut porter. La taille devient une **sortie**
du calcul.

**Chaîne de calcul** (`scripts/dimensionnement.py`) :

1. **Besoin de référence.** On enregistre une marche simulée de ToddlerBot
   (0,56 m, 3,454 kg) : 15 s, 751 pas, 0,106 m/s, sans chute. Pour chaque
   articulation, on mesure le couple de pointe, le couple efficace (RMS) et
   la vitesse de pointe (`sim/upstream/enregistrer_marche.py`,
   `scripts/analyser_marche.py`).
2. **Mise à l'échelle.** Pour une hauteur H, la structure suit la
   similitude géométrique (masse ∝ H³), **mais les actionneurs gardent leur
   masse réelle**. Le couple requis est proportionnel à masse × H.
3. **Boucle sur la masse.** Un actionneur plus gros alourdit le robot, qui
   réclame plus de couple. Le calcul cherche le H où tout s'équilibre (par
   dichotomie : l'itération naïve diverge).
4. **Condition d'acceptation**, par articulation :
   - marge × RMS requis ≤ couple continu de l'actionneur (échauffement) ;
   - marge × pointe requise ≤ couple de pointe (effort instantané) ;
   - vitesse requise ≤ vitesse de l'actionneur.
5. **Contrôle de cohérence.** Le calcul doit retrouver des robots existants
   dans leur classe, sinon il refuse de conclure. Un test prouve que ce
   contrôle sait échouer.

**Pourquoi le couple efficace compte plus que la pointe.** La pointe dit si
le moteur *peut* produire l'effort un instant. Le RMS dit s'il le produit
*sans chauffer* dans la durée. La thèse de Forget (corpus du projet) montre
que l'échauffement est souvent la vraie limite d'un actionneur humanoïde.

**Limites connues du calcul :**

- Dans la simulation de référence, **neuf actionneurs de jambe sur douze
  touchaient leur limite**, jusqu'à 17 % du temps pour le roulis de hanche.
  Les besoins mesurés sont donc des **minimums**, et les tailles calculées
  des **plafonds optimistes**.
- Le calcul ne couvre qu'une marche lente, droite et sur sol plat : pas de
  poussée ni de chute. Le relevé est vérifié à part, en quasi statique
  (exigence T5, `docs/choix-actionneurs.md`).
- Le contrôle de cohérence est faible. ToddlerBot est presque tautologique,
  puisque sa marche a été simulée avec les limites qui servent au contrôle.
  Pour Zeroth-01, la hauteur de 0,48 m n'apparaît dans aucune source (≈ 0,40
  m lu deux fois), le robot a 5 degrés de liberté par jambe et sa marche
  réelle n'a pas été observée.

---

## 3. La marge de sécurité — *décidé le 30-09-2026 : 1,5, à revoir après le banc*

**Ce que c'est.** On exige qu'un actionneur puisse fournir 1,5 fois le
couple mesuré en simulation. C'est un facteur de sécurité, comme la charge
utile d'un ascenseur, très inférieure à ce que ses câbles supportent. En
aéronautique, 1,5 est le facteur réglementaire des structures.

**Pourquoi il en faut une** : pointes écrêtées, marche idéale, masse réelle
supérieure à la masse prévue, frottements, usure, chaleur, batterie qui
faiblit.

**Ce qu'elle coûte** : la taille maximale décroît à peu près comme la marge
à la puissance −⅓ (calculé par le script, RS02 homogène). Pour le
RS02 : 0,90 m à 1,0 ; 0,79 m à 1,5 ; 0,71 m à 2,0.

**Règle décidée** (Jeremy, 30-09-2026, fiche 0051) : 1,5 tant que rien
n'a été mesuré sur un vrai actionneur. On la réduit quand le banc aura
mesuré le comportement thermique réel : moins d'inconnues, marge plus
faible.

---

## 4. Les tailles — *décidé le 30-09-2026*

Les tailles sont **définies par classe d'actionneur** (fiche 0048) : Banc,
S, M, L, XL. La hauteur de chaque taille est un ordre de grandeur, que le
calcul du § 2 affine. On ne dessine qu'à une taille qui a une hauteur
unique.

**Premier robot : S** (décision de Jeremy). C'est la taille la moins chère
pour franchir toute l'échelle des capacités (§ 8), et celle où un
actionneur conçu par Jeremy a le plus de chances de fonctionner (§ 6).

**Le banc** n'a pas de hauteur. Il apprend la commande et mesure la
thermique réelle d'un actionneur, c'est l'échelon 0 du § 8.

Les valeurs (hauteurs, actionneur de S, masse calculée) sont dans le
README et dans `params/anthropometry.yaml`.

---

## 5. Le budget : une méthode — *décidé le 30-09-2026*

Le budget n'est plus un chiffre de départ. C'est une **somme par poste,
calculée par taille et par phase** (`params/budget.yaml`) :

> coût TTC = (actionneurs + électronique + structure) × (1 + imprévus) × (1 + TVA)

- **Actionneurs** : le poste dominant. D'après l'article ToddlerBot, 90 %
  de son coût de 6 000 $ part dans les calculateurs et les moteurs.
- **Électronique** : calculateur (un CPU de type Intel N95 suffit pour la
  locomotion, d'après Berkeley Humanoid Lite), adaptateurs CAN, centrale
  inertielle, batterie, câblage.
- **Structure** : dépend du mode de fabrication. Aujourd'hui **inconnue** :
  il faut le chiffrage de l'opérateur CN pour l'usinage, et le coût du filament.
- **Imprévus** : casse, second tirage, actionneur défectueux. 15 % en
  provisoire : **à fixer par Jeremy**.
- **Taxes** : Suisse, TVA d'import 8,1 %, pas de droits de douane sur les
  produits industriels depuis le 1ᵉʳ janvier 2024. France, TVA 20 %, plus
  3 € par article sur les colis de moins de 150 € depuis le 1ᵉʳ juillet
  2026.

Tant qu'un poste est inconnu, le total s'affiche « ≥ », jamais comme s'il
était complet.

---

## 6. Acheter ou concevoir les actionneurs — *achat : proposé ; actionneur maison : décidé le 30-09-2026*

**Pour la v1, on achète.** Concevoir un actionneur est un projet en soi.
Berkeley Humanoid Lite l'a fait avec des cycloïdes imprimées, et ses
auteurs les jugent trop fragiles pour des tâches exigeantes : leur V2 passe
aux actionneurs du commerce.

**En parallèle, Jeremy conçoit son propre actionneur** (souhait exprimé
le 30-09-2026, **décidé** avec les modalités ci-dessous, fiche 0052) :

1. **Interface commune.** L'actionneur maison reprend l'interface d'un
   modèle du commerce de la même classe : bride, perçages, encombrement,
   bus CAN. Le robot est dessiné autour de cette interface. On peut donc
   monter l'un ou l'autre, et les comparer sur le même banc.
2. **Cahier des charges repris du commerce.** On part des caractéristiques
   publiées (couple continu et pointe, vitesse, masse, dimensions) comme
   cibles, sans repartir de zéro.
3. **Pas de copie de géométrie interne.** Reprendre des caractéristiques
   publiées pour définir une interface ne pose pas de problème. Recopier la
   conception interne d'un produit, c'est autre chose.
4. **Taille S d'abord.** Aux couples de S (quelques N·m), un réducteur
   imprimé souffre bien moins qu'en M ou L.
5. **Jamais sur le chemin critique.** Le robot avance avec l'actionneur
   acheté, et l'actionneur maison le rejoint quand il est au niveau.

---

## 7. Interfaces d'actionneur — *proposé*

Trois interfaces, pour qu'un changement d'actionneur — de modèle, de
fabricant, ou pour l'actionneur maison de la fiche 0052 — ne se propage
pas dans tout le robot.

1. **Interface d'articulation mécanique propre à YXOR**, plus **un
   adaptateur par modèle d'actionneur**. Le robot est dessiné autour de
   l'interface YXOR, et c'est l'adaptateur qui absorbe la bride, les
   perçages et l'encombrement de chaque modèle. Changer de modèle, ou
   monter l'actionneur maison, ne touche alors qu'une pièce.
2. **Interface logicielle indépendante du fabricant.** Une seule commande
   par articulation, `joint.command(position, vitesse, couple)`, puis
   **un backend par fabricant**, qui traduit vers son protocole, et **un
   backend simulé MuJoCo**. Le même code de commande pilote la simulation
   et le robot : c'est le principe « simulation d'abord » (§ 1).
3. **Chaque actionneur est référencé par la version de sa fiche et le
   sha256 du document lu.** Les spécifications changent sans prévenir :
   le RS02 affiche 6 N·m sur le site et 7 dans le PDF du 17-09. Une
   valeur sans version ni empreinte ne dit pas de quel produit elle
   parle. `params/actionneurs.yaml` porte ces deux champs.

Aucune de ces trois interfaces n'est encore décidée : pas de fiche.

---

## 8. L'échelle des capacités

Chaque échelon s'appuie sur le précédent et se démontre d'abord en
simulation.

| Échelon | Capacité | Critère de réussite |
| --- | --- | --- |
| 0 | Un actionneur sur un banc | Suit une consigne ; couple, jeu et échauffement **mesurés** |
| 1 | Une articulation et son segment | Angle atteint de façon répétable ; butées et arrêt d'urgence en place |
| 2 | Une jambe suspendue (6 degrés de liberté) | Le pied suit une trajectoire cartésienne (cinématique inverse) |
| 3 | Bas du corps sur portique (12 degrés de liberté) | Pas coordonné à vide, IMU intégrée |
| 4 | Tenir debout | 60 s d'équilibre, puis une poussée encaissée |
| 5 | Transfert de poids, pas quasi statique | Un pas lent sans chute |
| 6 | Marcher | Voie modèle (ZMP, pendule inversé linéaire) d'abord, puis apprentissage par renforcement |
| 7 | Haut du corps | Bras et cou fonctionnels |
| 8 | Percevoir | Caméra, fusion IMU et vision |
| 9 | Manipuler | Saisie en téléopération, puis par imitation |
| 10 | Autonomie | Loco-manipulation, consignes en langage naturel, voix |

Chantiers transverses : sécurité, alimentation, thermique, câblage, chutes.

Ordre de commande retenu (convergence Claude et ChatGPT) : d'abord un
contrôle PD et l'équilibre, puis ZMP, puis apprentissage par renforcement.
Le ZMP est interprétable : il permet de diagnostiquer la géométrie, le
centre de masse et les actionneurs avant d'ajouter l'opacité de
l'apprentissage.

---

## 9. Degrés de liberté par version

Référence : 6 par jambe (3 à la hanche, 1 au genou, 2 à la cheville),
d'après le rapport Bennehar du corpus et les humanoïdes contemporains.

| Version | Degrés de liberté | Contenu |
| --- | --- | --- |
| v1 | 12 | jambes, buste fixe |
| v2 | 18 à 20 | plus bras à 3 degrés de liberté et cou à 2 |
| v3 | 25 à 30 | manipulation (ToddlerBot en a 30) |

La topologie des bras (`elbow_yaw` contre `wrist_yaw`) est reportée à la
v2 : les bras ne font pas partie de la v1.

---

## 10. Sources principales

- `docs/dimensionnement-par-actionneur.md` et `scripts/dimensionnement.py` :
  dimensionnement inversé.
- `docs/choix-actionneurs.md` et `params/exigences_S.yaml` : exigences de
  S, charge utile, relevé.
- `params/actionneurs.yaml` et `params/budget.yaml` : catalogue et postes,
  chaque valeur sourcée et datée.
- Corpus du projet (`params/sources.yaml`) : thèse Forget (actionneurs,
  thermique), rapport Bennehar (degrés de liberté, ZMP), Kajita, article
  ToddlerBot.
