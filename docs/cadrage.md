# Cadrage du projet YXOR

**Version 1 — 30 septembre 2026.** Rédigé par Claude (arbitrage) à partir des
échanges avec Jeremy, des rapports de Claude Code et de l'audit de ChatGPT.
À intégrer dans le dépôt sous `docs/cadrage.md`.

**À quoi sert ce document.** Il dit ce qu'est YXOR, comment on décide de sa
taille, de son budget et de ses actionneurs, et **pourquoi** chaque
arbitrage a été pris. Il doit permettre à Jeremy, dans six mois, de
retrouver le raisonnement derrière chaque choix et de l'expliquer à
quelqu'un d'autre.

**Comment le lire.** Chaque décision figure au registre (§ 12), avec sa
date, son auteur, ses alternatives écartées et la condition qui la
rouvrirait. Les chiffres renvoient aux documents qui les calculent ; ils se
régénèrent, ce document ne les fige pas. Statuts : **décidé** (par Jeremy),
**proposé** (en attente de décision), **ouvert** (non instruit).

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

## 2. Ce qui n'allait pas dans le cadrage initial

Trois erreurs de méthode ont été identifiées fin septembre 2026. Les garder
écrites évite de les refaire.

**2.1 — La taille était une entrée.** Les paliers P1 (0,56 m), P2 (0,9 m)
et P3 (1,7 m) étaient choisis d'abord, sur des hauteurs rondes et humaines.
Les proportions anthropométriques devaient ensuite tout déterminer, puis on
cherchait des actionneurs. Or les actionneurs se vendent **par classes
discrètes**, et le couple requis croît très vite avec la taille. Une taille
choisie sans regarder le catalogue tombe n'importe où entre deux classes.
P2 à 0,9 m tombait au pire endroit : trop grand pour un RS02, trop petit
pour exploiter un RS06.

**2.2 — Le budget était fixé a priori.** Les 500 à 2 000 € ont été posés
avant tout prix de marché. On sait désormais que les jambes d'un robot
d'environ 0,8 m (12 actionneurs et l'électronique connue, TVA et imprévus
compris) coûtent déjà au moins 1 720 CHF. Ce
montant est donc un **budget de R&D par phase**, pas le prix d'un robot.

**2.3 — La méthode a grandi plus vite que le robot.** Fin septembre, le
dépôt comptait 44 fiches et 1 440 valeurs auditées pour une seule pièce en
carton, qui ne s'interfaçait avec rien. La caractérisation du carton
(épaisseur, densité, rayons) a été arrêtée : ses valeurs ne se transfèrent
pas au robot réel. La traçabilité reste, mais elle doit désormais servir le
robot : exigences, budgets, interfaces.

---

## 3. La démarche inversée — *décidé le 30-09-2026*

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
  poussée, de chute ni de relevé.
- Le contrôle de cohérence est faible. ToddlerBot est presque tautologique,
  puisque sa marche a été simulée avec les limites qui servent au contrôle.
  Pour Zeroth-01, la hauteur de 0,48 m n'apparaît dans aucune source (≈ 0,40
  m lu deux fois), le robot a 5 degrés de liberté par jambe et sa marche
  réelle n'a pas été observée.

---

## 4. La marge de sécurité — *décidé le 30-09-2026 : 1,5, à revoir après le banc*

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

## 5. Résultats du dimensionnement

Source : **engendré** par `.venv/bin/python scripts/dimensionnement.py --markdown`
(bloc `TABLEAU_CADRAGE`), le 30-09-2026. Ce tableau n'est pas recopié à la main :
il se remplace par la sortie du script. Les valeurs du RS02 (6 retenu, 7 dans le PDF
du 17-09) et du RS03 (20 retenu, 21 à la p. 19) sont discutées dans
`params/actionneurs.yaml`.

<!-- engendré : scripts/dimensionnement.py --markdown, bloc TABLEAU_CADRAGE -->
| Configuration (marge 1,5) | Continu / pointe (N·m) | Taille maximale | Masse convergée | Articulation limitante |
| --- | --- | ---: | ---: | --- |
| homogène Feetech STS3250 | STS3250 1,6 / 4,9 | 0,60 m | 4,2 kg | hip_roll |
| homogène RobStride EduLite 05 | EduLite 05 1,8 / 5,5 | 0,54 m | 5,4 kg | hip_roll |
| homogène RobStride RS05 | RS05 1,6 / 5,5 | 0,54 m | 4,8 kg | hip_roll |
| homogène RobStride RS02 | RS02 6,0 / 17,0 | 0,79 m | 12,2 kg | hip_roll |
| homogène RobStride RS06 | RS06 11,0 / 36,0 | 0,91 m | 19,4 kg | hip_roll |
| homogène RobStride RS03 | RS03 20,0 / 60,0 | 1,07 m | 30,0 kg | hip_roll |
| homogène CubeMars AK70-10 KV100 | AK70-10 KV100 8,3 / 24,8 | 0,82 m | 16,2 kg | hip_roll |
| homogène RobStride RS00 | RS00 5,0 / 14,0 | 0,75 m | 10,7 kg | hip_roll |
| S — RS05 homogène | RS05 1,6 / 5,5 | 0,54 m | 4,8 kg | hip_roll |
| S — RS00 lourd (hanche roulis et tangage, genou, tangage de cheville), RS05 ailleurs | RS00 5,0 / 14,0 ; RS05 1,6 / 5,5 | 0,65 m | 7,6 kg | hip_yaw_drive |
| S — RS00 lourd (hanche roulis et tangage, genou, tangage de cheville), EduLite 05 ailleurs | RS00 5,0 / 14,0 ; EduLite 05 1,8 / 5,5 | 0,64 m | 7,7 kg | hip_yaw_drive |
| L — RS06 sur la hanche (3 axes), le genou et le tangage de cheville ; RS02 sur le roulis de cheville | RS06 11,0 / 36,0 ; RS02 6,0 / 17,0 | 0,92 m | 19,2 kg | hip_roll |

Toutes ces tailles sont des **plafonds optimistes** : le roulis de hanche, et d'autres articulations de jambe, étaient écrêtés dans la marche de référence.
<!-- fin du bloc engendré -->

Constats :

- **L'articulation limitante est le roulis de hanche**, dans toutes les
  configurations homogènes. C'est aussi celle que la simulation de
  référence bloquait le plus souvent.
- **Une configuration mixte naïve est contre-productive.** Mettre la
  classe légère sur le lacet de hanche rend ce lacet limitant, parce qu'il
  porte la masse ajoutée par les actionneurs lourds. Exemple : RS03 et
  STS3250 plafonnent à 0,48 m, contre 0,60 m en STS3250 seul. La
  configuration avec le lacet de hanche en classe lourde n'avait pas été
  calculée *(correction du 30-09-2026 : la version 1 la disait « en cours
  de calcul », ce qui était faux)*. Elle l'est désormais pour L : ligne
  « L » du tableau ci-dessus.
- **La valeur du RS02 (6 ou 7 N·m) change peu le résultat** : 9 mm.
- **L'ancien P2 à 0,9 m** n'est atteint que par le RS06 (de justesse) et
  le RS03.

---

## 6. Les tailles de YXOR — *décidé le 30-09-2026*

> **Mise à jour 2026-09-30, 22 h 30 :** contredit par le recalcul 48 V (`archive/docs/choix-famille-actionneurs.md`). Famille non décidée ; le banc doit départager.

Les tailles sont désormais **définies par classe d'actionneur**. La
hauteur indiquée est un ordre de grandeur, que le calcul affine.

| Taille | Hauteur | Classe d'actionneur de jambe | Rôle |
| --- | --- | --- | --- |
| **Banc** | aucune | *banc de qualification* (§ 13, question 12) : 1 × J4310 48 V + 1 × EduLite 05 + 1 × RS05 | apprendre la commande, mesurer la thermique réelle (échelon 0) |
| **S** | ≈ 0,55–0,60 m | EduLite 05, RS05 ou STS3250 | **premier robot** : petit, abordable, pour apprendre la locomotion complète |
| **M** | ≈ 0,8 m | RS02, un seul modèle | premier YXOR « sérieux » : une seule bride, un seul fichier CAO, des pièces interchangeables |
| **L** | ≈ 0,9 m | RS06 (ou mixte RS06/RS02 à calculer) | version grande |
| **XL** | > 1 m | RS03 et au-delà | horizon, hors programme |

**Composition du banc — *remplacée le 30-09-2026 au soir par le banc de qualification*
(§ 13, question 12, et `archive/docs/comparatif-banc.md`).** Texte d'origine : deux RS05 et un adaptateur USB-CAN.
Deux, et non un, pour quatre raisons : mesurer la thermique réelle d'un
actionneur ; faire parler **deux adresses sur un même bus** ; monter le
**segment à 2 degrés de liberté** de l'échelon 1 (§ 10) ; garder une
**rechange**. Chiffré dans `params/budget.yaml`, phase `banc`, marquée
« option ». **Jeremy choisira sur comparatif rédigé** :
`archive/docs/comparatif-banc.md`. Pas de fiche d'ici là.

**Premier robot : S** (décision de Jeremy). Justification : c'est la taille
la moins chère pour franchir toute l'échelle des capacités (§ 10), et celle
où un actionneur conçu par Jeremy a le plus de chances de fonctionner (§ 8).

**Choix de classe pour S — *entre deux familles, RobStride et Damiao, départagées par
une mesure* (mise à jour du 30-09-2026, soir).** Le comparatif v3
(`archive/docs/choix-famille-actionneurs.md`) place la famille Damiao devant, à toutes
les hypothèses sur la condition de mesure (k de 1,0 à 0,5), mais d'une marge
qui fond à 0,10 point quand k baisse, avec RobStride en second. Le banc de
qualification (§ 13, question 12) mesure ce qui les départage. Arguments d'origine,
tels qu'écrits en version 1 :

- **EduLite 05** : même protocole CAN que RS02 et RS06, donc tout le
  logiciel écrit pour S (pilote, calibration, sécurité) se réutilise en M
  et L. Mais son couple continu et sa vitesse ne sont pas vérifiés : ils
  viennent de revendeurs, et sont à null dans le catalogue. *(Mise à jour
  du 30-09-2026 : ils sont désormais lus dans le manuel constructeur EL05
  — 1,8 N·m sur plaque de 70 × 70 mm, 430 rpm — voir
  `archive/docs/choix-classe-S.md`.)*
- **STS3250** : le moins cher, mais c'est un écosystème (bus TTL, Feetech)
  qu'on abandonnerait en passant à M. Réducteur 1:345, peu réversible, jeu
  mesuré indépendamment supérieur au jeu annoncé.
- **RS05** : protocole CAN, spécifications constructeur plus solides, plus
  cher.

Recommandation de Claude : une classe CAN (EduLite ou RS05), pour la
continuité logicielle. À trancher après l'étude fournisseurs (§ 9).

**Conséquence sur le dépôt.** Les paliers P1/P2/P3 de `anthropometry.yaml`
sont à remplacer par les tailles. Cette migration n'est pas faite : elle
passera par une fiche qui remplace la décision des paliers, sans la
réécrire.

---

## 7. Le budget

### 7.1 Méthode — *décidé le 30-09-2026*

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

### 7.2 Constats

- **Le mode de fabrication change peu le budget.** En M et L, les
  actionneurs écrasent le reste. Usinage, impression ou hybride se
  choisissent pour le temps d'itération, la rigidité et la masse, pas pour
  l'argent. L'outillage (une imprimante, par exemple) est un poste à part,
  qui relève de la seule décision de Jeremy.
- **Le budget se raisonne par phase** : banc (2 actionneurs et un
  adaptateur CAN), puis jambes, puis haut du corps.
- **Ordres de grandeur connus au 30-09-2026** (actionneurs et électronique
  connus, TVA et 15 % d'imprévus compris, structure exclue) :
  - M (RS02) : ≥ 1 774 CHF pour les jambes v1, puis ≥ 1 947 CHF de plus
    pour le haut du corps v2 ;
  - RS03 : ≥ 2 332 CHF, puis ≥ 2 783 CHF de plus.
  - *(Mise à jour du 30-09-2026, soir : +54 CHF sur les jambes, parce que
    l'adaptateur USB-CAN est désormais chiffré. Il n'y a plus de « ≥ »
    que pour la structure.)*
  - Le chiffrage de S est à produire une fois sa classe choisie.
- **Défaut relevé** : la batterie chiffrée (22,2 V) ne correspond pas aux
  48 V nominaux des actionneurs RobStride. Une batterie adaptée reste à
  chiffrer.

---

## 8. Acheter ou concevoir les actionneurs — *achat : proposé ; actionneur maison : décidé le 30-09-2026*

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

## 8 bis. Interfaces d'actionneur — *proposé*

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

## 9. Étude des fabricants et fournisseurs — *instruit le 30-09-2026*

> **Mise à jour 2026-09-30, 22 h 30 :** contredit par le recalcul 48 V (`archive/docs/choix-famille-actionneurs.md`). Famille non décidée ; le banc doit départager.

Jusqu'ici, on a comparé des **modèles**. Il manque la comparaison des
**fabricants et distributeurs**, qui pèse autant sur le projet.

Critères :

- **Stabilité des spécifications.** La fiche du RS02 a changé sans
  prévenir : 6 N·m sur le site, 7 dans le PDF du 17-09.
- **Documentation** : fiches, protocole, fichiers CAO.
- **Ouverture** : SDK, firmware, licence.
- **Communauté** et retours d'expérience.
- **Distributeurs** en Suisse et dans l'UE, délais, garantie, service
  après-vente.
- **Pérennité** : gamme suivie ou abandonnée (le RMD-X6 V3 est annoncé en
  fin de série).
- **Gamme** : un même fournisseur couvre-t-il S, M et L avec le même
  protocole ?

Fabricants à couvrir, au minimum : RobStride, CubeMars (T-Motor), MyActuator,
Damiao, Unitree, Steadywin, ROBOTIS, Feetech, mjbots (contrôleurs), ODrive.

### Synthèse de l'étude

Source : `docs/sources/etude-fournisseurs-chatgpt-2026-09-30.md` (étude
ChatGPT, **source externe non vérifiée par le dépôt**). Les chiffres qui
recoupent `params/actionneurs.yaml` sont vérifiés au journal du
2026-09-30.

- **RobStride est la seule gamme alignée sur S, M et L** : RS05, RS02 et
  RS06 (5,5 / 17 / 36 N·m en pointe), tous à 48 V et sur le même bus CAN.
- **RS02 plutôt que RS01** pour M : le RS01 est spécifié à 36 V (PDF
  RobStride p. 7), le RS02 à 48 V comme les deux autres.
- **Plans B** : **MyActuator**, distribué en France par A2V, et
  **CubeMars**, qui publie une garantie d'un an. Leurs gammes collent
  moins bien au triplet.
- **Aucun fabricant n'a de bride commune entre classes** : l'interface
  mécanique doit venir de YXOR (§ 8 bis).
- **Les spécifications bougent.** L'écart RS02 « 6 ou 7 N·m » est en
  partie une question de **condition de mesure** : le PDF du 17-09 donne
  7 N·m en rotation, sur plaque d'aluminium, et 6 N·m en blocage (p. 11
  et p. 13). Il faut donc toujours noter la condition avec la valeur.
- **Le backend RobStride de LeRobot était défaillant en 2026** : il
  employait un framing de type Damiao. C'est un argument pour une couche
  moteur propre à YXOR (§ 8 bis), plutôt que pour un wrapper tiers.
- **Aucun distributeur suisse** n'a été trouvé, pour aucun fabricant.

**Résultat du comparatif v3** (30-09-2026, `archive/docs/choix-famille-actionneurs.md`) :
CubeMars coûte cher en M et L (jambes ≥ 6 452 et ≥ 9 179 CHF) ; MyActuator a un
**trou en M** (aucun modèle CAN actuel entre 12 et 25 N·m). Le seuil de bascule
k ≈ 0,70 de la première grille de capacité **a disparu avec la grille corrigée** :
Damiao devant partout, de peu à bas k. Rapports blocage / nominal RobStride :
0,62 à 0,86 (moyenne 0,72).

---

## 10. L'échelle des capacités

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

## 11. Degrés de liberté par version

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

## 12. Registre des arbitrages

| Date | Arbitrage | Par | Pourquoi | Alternatives écartées | À rouvrir si |
| --- | --- | --- | --- | --- | --- |
| 29-09 | Profil du carton : double cannelure | Jeremy (constat) | Vu à la tranche | — | — |
| 30-09 | Caractérisation du carton arrêtée ; fiches 0042 et 0044 closes | Jeremy | Ses valeurs ne se transfèrent pas au robot réel | Éprouvette de rayons | jamais : le carton reste une maquette |
| 30-09 | Moratoire sur les fiches **rejeté** | Jeremy | — | Plus de fiche avant une pièce qui s'emboîte | — |
| 30-09 | Principe du lot A : corriger la promesse, pas construire le contrôle | Jeremy | Des documents promettaient des contrôles inexistants | Construire les contrôles | une pièce a besoin du contrôle |
| 30-09 | Empreinte sans le Dockerfile | Jeremy | Coolify réécrit le Dockerfile ; hypothèse confirmée par l'expérience | Désactiver l'injection dans Coolify ; filtrer les lignes | changement de plateforme de déploiement |
| 30-09 | Date d'extraction conservée dans `upstream_joints.generated.yaml` | Jeremy | Elle fait partie de la provenance de l'extrait (fiche 0006) | Amender la 0006 | — |
| 30-09 | Fabrication séquencée : usinage, puis impression, puis hybride | Jeremy | Comprendre chaque procédé, ses avantages et ses limites | Tout imprimé ; plaques seules (0014, 0015) | — |
| 30-09 | **Démarche inversée** : la classe d'actionneur fixe la taille | Jeremy | Les actionneurs sont discrets et le couple croît très vite avec la taille (§ 2.1, § 3) | Tailles humaines fixées a priori | — |
| 30-09 | **Tailles Banc, S, M, L, XL ; premier robot S** | Jeremy | § 6 | P1/P2/P3 à hauteur fixe ; premier robot M | l'étude fournisseurs élimine toute classe CAN pour S |
| 30-09 | Scripts de chiffrage versionnés, séries régénérées | Jeremy | Refaire le calcul quand les hypothèses changent | Laisser les scripts hors dépôt | — |
| 30-09 | Pour la v1, on achète les actionneurs | proposé (Claude, ChatGPT) | § 8 | Actionneur maison sur le chemin critique | aucun actionneur du commerce ne tient l'enveloppe |
| 30-09 | **Actionneur maison**, piste parallèle à interface commune, taille S d'abord, jamais sur le chemin critique (fiche 0052) | Jeremy | § 8 | — | — |
| 30-09 | **Marge de 1,5** (fiche 0051) | Jeremy | § 4 | 1,0 ; 2,0 | résultats du banc |
| 30-09 | Vision du § 1 | **proposé**, en attente | — | — | — |
| 30-09 | **Poids du comparatif d'actionneurs** (classe S et familles) : capacité 18, continuité 18, coût 15, fiabilité 15, robustesse 12, disponibilité 7, masse, ouverture, tension 5 | Jeremy | équilibre entre préparer M et L et un S convaincant par lui-même | poids proposés par Claude | résultats du banc |
| 30-09 | ~~**Poids du banc** : valeur de décision 40, transfert 20, risque 15, coût 15, apprentissage 10~~ | **RETIRÉE, attribution erronée** (Jeremy n'avait pas validé ces poids ni la citation de principe ; il pose encore la question) | — | poids proposés par Claude | — |

---

## 13. Questions ouvertes

> **Mise à jour 2026-09-30, 22 h 30 :** contredit par le recalcul 48 V (`archive/docs/choix-famille-actionneurs.md`). Famille non décidée ; le banc doit départager.

1. Valider la vision (§ 1). *(La marge du § 4 est décidée : fiche 0051.)*
2. Classe d'actionneur pour S (§ 6), après l'étude fournisseurs (§ 9).
3. Configuration mixte avec le lacet de hanche en classe lourde. *(Correction
   du 30-09-2026 : ce calcul n'était PAS en cours, contrairement à ce
   qu'écrivait la version 1.)* **Calculée le 30-09-2026 pour L**
   (RS06 / RS02, § 5). Reste ouverte pour les autres paires.
4. Taux d'imprévus du budget (§ 7).
5. Chiffrage de la structure : usinage (l'opérateur CN) et impression.
6. Procédé exact de l'opérateur CN, rayons minimaux, matières, format de fichier.
7. Batterie adaptée à la tension des actionneurs retenus.
8. Remplacement des paliers P1/P2/P3 par les tailles, dans le dépôt, par
   une fiche qui remplace sans réécrire.
9. Réouverture des fiches 0014 et 0015, rendues caduques par la
   fabrication hybride, selon la même procédure.
10. Immuabilité des fiches : ne plus réécrire une fiche acceptée, en créer
    une nouvelle qui la remplace. Position de ChatGPT, partagée par Claude,
    non tranchée.
11. Les valeurs numériques extraites de ToddlerBot (axes, butées) sont-elles
    couvertes par sa licence ? Question juridique, sans avis ici.
12. **Banc de qualification : mesurer avant d'acheter en quantité.** Le
    comparatif du banc (`archive/docs/comparatif-banc.md`, poids **proposés**, pas encore fixés) place
    en tête l'option « qualification » : 1 × Damiao J4310 V1.2 48 V + 1 × EduLite 05
    + 1 × RS05, une alimentation 48 V, un adaptateur CAN. Protocole *proposé* :
    `docs/protocole-banc.md`. L'ancienne option « 2 × RS05 » n'est plus en tête.
    **Mise à jour du 30-09-2026, nuit** : avec la règle de décisivité étendue,
    **aucune inconnue n'est décisive** — c'est un **banc de VÉRIFICATION, pas de
    départage**. La qualification perd son avance : trois options sont **ex
    æquo à 2,30** (3 × J4310, paire J4310 + RS05, qualification). Le
    comparatif ne les classe plus entre elles. Critère d'abandon *proposé* :
    `docs/protocole-banc.md`.
13. **Ce que S doit porter.** Le seuil de taille retiré du comparatif le
    30-09-2026 (« H_max ≥ 0,55 m ») cachait une vraie contrainte : S doit
    porter son calculateur, sa batterie et son IMU. Elle n'est pas
    chiffrée : `dimensionnement.py` met ces masses à l'échelle avec la
    structure de ToddlerBot, sans les compter à part.
    Le prix de l'adaptateur n'est pas vérifié ; l'alimentation du banc
    n'est pas comprise dans la proposition.

---

## 14. Sources principales

- `archive/docs/exigences-actionnement-P2.md` : premier chiffrage des couples,
  30-09-2026.
- `docs/dimensionnement-par-actionneur.md` : dimensionnement inversé,
  30-09-2026.
- `params/actionneurs.yaml`, `params/budget.yaml` : catalogue et postes,
  chaque valeur sourcée et datée.
- `archive/docs/etat-des-lieux-2026-09-29-nuit.md` : audit complet du dépôt.
- Corpus du projet : thèse Forget (actionneurs, thermique), rapport
  Bennehar (degrés de liberté, ZMP), Kajita.
- Recherche Claude du 30-09-2026 (comparatif d'actionneurs) et audit
  ChatGPT du 30-09-2026 : non versionnés, synthétisés ici.