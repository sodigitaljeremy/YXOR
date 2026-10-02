# Protocole du banc — v2 : vérifier le RS00

**Version 2, 2026-10-01** (refonte R6). Elle remplace :

- la v1 du 2026-09-30, qui visait un banc de qualification à trois
  modèles ;
- les ajouts proposés le 2026-10-01.

Les deux textes sont archivés tels quels :
`archive/docs/protocole-banc-v1-2026-09-30.md` et
`archive/docs/protocole-banc-additions-2026-10-01.md`.

**Qui a décidé quoi :**

- **Les ajouts au protocole ont été validés par Jeremy** le 2026-10-01.
  Ses mots : « Oui je valide les ajouts au protocole. »
- **La règle de la seconde personne ne s'applique pas.** Ses mots : « je
  suis seul sur ce projet ».
- **Les mesures de travail isolé** (§ 1.4) ont été proposées par Claude
  (arbitrage). Jeremy les valide en lançant le prompt de la refonte R6
  sans modification.
- **Le reste de cette rédaction** (ordre des sections, seuils repris de
  la v1, tableau du § 7) est **proposé**.

**Source des valeurs RS00** : manuel « RS00 User Manual 260713 »
(registre 0030, `robstride_rs00_manual_260713`, sha256 `47d0ae5c…`). Les
pages citées sont celles du fichier PDF.

---

## § 0 — Objet

- **Vérifier le RS00** retenu pour S (fiche 0065, condition b). Le banc
  **ne départage plus** : il confirme, ou il fait redescendre la taille.
- **Depuis la fiche 0067 (2026-10-02), S a des jambes mixtes : ce banc ne
  couvre que le RS00, pas le RS02, et le critère du § 4 a été écrit pour
  un RS00 homogène. Composition à revoir (fiche 0066).**
- **Banc : 2 × RS00 identiques**, pour mesurer la dispersion et garder une
  rechange. **La composition reste à décider par Jeremy**
  (`params/banc.yaml`, `rs00_x2`), comme l'achat (fiche 0066).
- Avant tout achat, **vérifier la version** du RS00 vendue : « ancien »
  5 / 14 N·m, 310 g, ou « nouveau » 6 / 17 N·m, 330 g (fiche 0065,
  condition c).

## § 1 — Préalables de sécurité

**Tant qu'une seule case n'est pas cochée, on ne met pas sous tension de
puissance.**

### 1.1 Chien de garde — EN TÊTE

Le chien de garde coupe l'actionneur s'il ne reçoit plus de consigne
pendant un délai donné. Sans lui, un PC planté ou un câble CAN
débranché laisse l'actionneur exécuter sa dernière consigne
indéfiniment.

- [ ] **Registre et réglage d'usine** : `canTimeout`, index `0x7028`,
  uint32, 20 000 = 1 s, **0 par défaut, donc désactivé** (manuel RS00,
  p. 46-47). Le même paramètre figure dans la table des paramètres sous
  `0x200c CAN_TIMEOUT`, défaut 0 (p. 21).
- [ ] **Effet** : sans commande CAN reçue dans le délai, le moteur passe
  en mode reset (p. 28).
- [ ] **Lu** à la mise en route, puis consigné (`params/mesures.yaml`).
- [ ] **Réglé** à une valeur non nulle, de quelques périodes de la boucle
  de commande. Cette valeur est fixée par Jeremy, et ce protocole n'en
  propose pas.
- [ ] **Vérifié à vide** : moteur activé à couple nul, câble CAN
  débranché, coupure constatée dans le délai.
- [ ] **Relu après chaque coupure d'alimentation.**

### 1.2 Alimentation et câblage

- [ ] **Alimentation à limitation de courant réglable**, réglée au plus
  bas courant qui permet le palier en cours (cahier des charges : § 7).
- [ ] **Fusible DC près de la source**, calibré pour la tension du bus.
- [ ] **Consignation avant tout recâblage** :
  - couper, puis empêcher la remise sous tension ;
  - attendre que les condensateurs se déchargent, ou les décharger ;
  - mesurer Vbus ≈ 0 V au multimètre ;
  - **puis** recâbler.
  - **Jamais** de câblage modifié sous tension.
- [ ] **Polarité et masse** vérifiées au multimètre avant la première
  mise sous tension de chaque montage, avec une masse commune entre
  l'adaptateur CAN et le pilote.
- [ ] **Précharge, si nécessaire.** Brancher un bus de 48 V sur des
  condensateurs vides fait un appel de courant. Selon la notice : soit
  une précharge par résistance, soit une montée progressive de la
  tension.
- [ ] **Vbus journalisée** (registre `VBUS`, `0x701C`, p. 46 ; à 1 Hz).
  - Le moteur **renvoie de l'énergie** quand on le fait tourner de
    l'extérieur : il faut une alimentation capable de l'absorber
    (manuel, p. 51).
  - **Défaut de surtension à 60 V** (p. 28 et 73), soit la tension
    maximale admissible (p. 11). **Défaut de sous-tension à 12 V**
    (p. 28).
  - **Arrêt d'essai sous 60 V**, avec un seuil fixé par Jeremy.

### 1.3 Mécanique et instrumentation

- [ ] **Carter rigide** autour du bras : il arrête aussi une pièce qui se
  détache.
- [ ] **Bras rigide**, fixé à l'arbre de sortie sans glissement, avec
  **une butée mécanique de chaque côté**. **Personne dans le plan de
  rotation** du bras quand l'actionneur est activé.
- [ ] **Serrage spécifié** de chaque vis (bride de sortie, plaque), en
  N·m, d'après la documentation. Frein filet ou rondelle, si prévu.
- [ ] **Capteur d'effort taré** à vide avant chaque session, et
  **vérifié avec une masse connue** à la longueur du bras. La masse et
  l'écart sont consignés.
- [ ] **Thermocouple** sur le carter, à une position **décrite et
  photographiée**, la même pour les deux exemplaires.
- [ ] **Surface non inflammable** sous le montage. Aucune batterie LiPo
  sur le banc : l'alimentation seule.

### 1.4 Travail isolé

Jeremy travaille seul : ces sept mesures remplacent la seconde personne.

- [ ] **1. L'énergie est limitée par construction** :
  - courant limité réglé bas ;
  - fusible ;
  - chien de garde actif ;
  - limites logicielles ;
  - protection thermique du RS00 laissée active.
- [ ] **2. Arrêt d'urgence à portée de main**, testé à vide à chaque
  session. Il coupe physiquement le bus DC, pas par logiciel.
  L'adaptateur CAN et le PC restent alimentés à part, pour lire les
  températures après un arrêt.
- [ ] **3. Jamais d'essai sans surveillance**, paliers longs compris.
- [ ] **4. Extincteur pour feux électriques** (CO₂ ou poudre) à portée,
  et **détecteur de fumée** dans la pièce.
- [ ] **5. Première mise sous tension, ou premier palier chargé** :
  prévenir quelqu'un du début et de la fin de la session, téléphone à
  portée.
- [ ] **6. Lunettes de protection** pendant les essais chargés.
- [ ] **7. Progression au plus bas niveau d'énergie** (§ 2).

### 1.5 Limites logicielles et thermiques

- [ ] **Limites de couple et de courant** dans chaque actionneur, à
  **10 % au-dessus du palier** en cours, jamais au maximum du
  constructeur. Bornes des registres :
  - 0 à 14 N·m et 0 à 16 A dans la table des p. 45-46 ;
  - 17 et 23 dans la table des paramètres des p. 20-21.

  C'est un désaccord interne au manuel : la plus basse est retenue
  (fiche 0064).
- [ ] **Arrêt d'un palier à 125 °C** : 10 °C sous la protection retenue
  de 135 °C (`params/banc.yaml`, `seuil_thermique`).
  - La protection est retenue par la fiche 0064 : c'est l'avertissement
    de surchauffe à 135 °C, alors que le défaut est à 145 °C (p. 43).
  - Au blocage, la chauffe d'une phase vaut 1,414 fois celle en rotation
    (p. 10).
- [ ] **Arrêt si une télémétrie critique disparaît** plus d'une seconde :
  température, courant ou Vbus. Arrêt logiciel immédiat, arrêt
  d'urgence matériel en secours.

## § 2 — Séquence de mise en route

À chaque montage, dans cet ordre, sans en sauter :

1. Préalables du § 1 cochés ; arrêt d'urgence testé à vide.
2. Alimentation de la logique seule : lecture des paramètres, chien de
   garde lu, réglé, relu.
3. **Couple nul** : activation, télémétrie complète reçue.
4. **Faible courant** : consigne basse, limite de courant basse.
5. **Sens de rotation vérifié** par rapport au signe de la consigne et
   au codeur.
6. **Montée progressive** vers les paliers du § 3.

## § 3 — Mesures, dans cet ordre

| # | Mesure | Condition | Ce qu'elle établit |
| --- | --- | --- | --- |
| 1 | **Chien de garde** : câble CAN débranché | à vide, couple nul | coupure dans le délai réglé |
| 2 | **Bus-off** : comportement après une erreur de bus | à vide | ce que fait le moteur (non publié dans le manuel lu) |
| 3 | **Protections** : limites de courant et de couple, défauts levés | à vide, puis faible courant | les codes de défaut (p. 28 et 43) remontent bien |
| 4 | **Réversibilité et jeu** | moteur **désactivé** | couple pour faire tourner la sortie à la main ; jeu angulaire (non publiés) |
| 5 | **Continu au blocage**, sur **chaque** exemplaire | rotor bloqué, paliers croissants depuis le blocage publié (3,6 N·m), jusqu'à l'équilibre thermique ou 125 °C | la valeur au blocage réelle ; la **dispersion** entre les deux exemplaires (n = 2) |
| 6 | **Couple réel ÷ couple de la télémétrie**, et **rapport couple / courant** | les paliers de la mesure 5 | la confiance dans la télémétrie, et la constante de couple réelle (publiée : 1,48 N·m/Arms, p. 9) |
| 7 | **Capteur de température du moteur ÷ thermocouple** | les paliers de la mesure 5 | l'écart entre la température lue et celle du carter |

**Conditions du blocage publié, d'après les documents lus :**

- **3,6 N·m « rated » au blocage** : PDF de spécifications du
  2026-09-17, p. 5. **Plaque et ambiante de l'essai au blocage : non
  publiées.** La courbe de surcharge au blocage du manuel, p. 10, est une
  image, sans condition écrite.
- **L'essai en rotation**, lui, est fait à 25 °C, sur un dissipateur en
  alliage d'aluminium de 90 × 85 mm, à 100 rpm (manuel, p. 8-9).
- **Plaque de mesure : aluminium de 90 × 85 mm**, la seule condition
  d'essai publiée par le manuel (p. 8-9).
  - Proposée par Claude Code (R6) et recommandée par Claude (arbitrage) ;
    Jeremy la valide en lançant le prompt du 2026-10-01 sans
    modification.
  - **À chaque session, on relève l'alliage, l'épaisseur de la plaque et
    la température ambiante.**
- **Courant de phase au blocage : non publié.** Sont publiés le courant
  de phase nominal, 4,7 Apk, et le courant maximal, 15,5 Apk (p. 9 et
  11). La mesure 6 le relève.

## § 4 — Critère, écrit AVANT la mesure

1. La **valeur mesurée au blocage remplace la valeur publiée** (3,6 N·m),
   puis la grille de `docs/choix-actionneurs.md` est relancée. La valeur
   publiée reste au catalogue, intacte ; la mesure s'affiche à côté.
2. Avec deux exemplaires, on retient **le plus faible**.
3. Verdict à la relance, sur T1, T2, T4 et T5 (charge utile comprise,
   borne haute de T4 incluse) :
   - **PASS à 0,60 m** : S confirmé.
   - **FAIL à 0,60 m, mais PASS à 0,55 m** : repli à 0,55 m (fiche 0065,
     condition a).
   - **FAIL à 0,55 m** : la famille est **rouverte**.
4. **Outillé le 2026-10-01, avant toute mesure** :
   `.venv/bin/python scripts/choix_actionneurs.py --ecrire` écrit le
   verdict au § 6 de `docs/choix-actionneurs.md`.
   - Le test `tests/test_critere_banc.py` produit les trois verdicts à
     partir de mesures fictives écrites dans un fichier temporaire.
   - Ordres de grandeur pour un RS00 HOMOGÈNE, avec les hypothèses du
     2026-10-02 (servos ToddlerBot du haut du corps retirés, fiche 0067) :
     S confirmé à 2,7 N·m et au-dessus ; repli entre 2,35 et 2,65 N·m ;
     famille rouverte à 2,3 N·m et en dessous. (Le 2026-10-01 : 3,1 ;
     2,6 à 3,0 ; 2,5.)

## § 5 — Consignation

Chaque relevé devient une entrée de `params/mesures.yaml`, sous la forme
de la fiche 0041 :

- `grandeur`, `valeur`, `unite` ;
- `incertitude` et `type_incertitude` (`resolution`, ou `dispersion`
  pour l'écart entre les deux exemplaires, avec `n: 2`) ;
- `instrument`, `n`, `date`, `alimente`, `note` ;
- plus `actionneur: rs00` et le **numéro de série** de l'exemplaire.

Un continu au blocage n'est lu par le critère du § 4 que si son
`alimente` contient `candidats.rs00.couple_continu_Nm.blocage`.

L'incertitude se porte avec la valeur, jamais après coup. Vont en
`note` : l'ambiante, la plaque (alliage, épaisseur), la longueur du bras
et la position du thermocouple.

## § 6 — Ce que le banc ne mesure pas

- **La rotation sous charge** : il faudrait un frein ou un second moteur.
- **Les chocs**, dont la chute elle-même. Le relevé de la grille est
  quasi statique.
- **Une statistique de production** : deux exemplaires donnent un ordre
  de grandeur, pas un écart-type.

## § 7 — Cahier des charges de l'outillage

Des **caractéristiques**, **jamais des produits** : l'outillage relève de
la seule décision de Jeremy, et Claude ne propose pas d'achat
(fiche 0066, b et c).

| Outil | Caractéristiques exigées |
| --- | --- |
| Alimentation | sortie continue réglable jusqu'à **48 V au moins** (≤ 60 V) ; **limitation de courant réglable**, réglée bas ; **supporte l'énergie renvoyée** par un moteur entraîné (régénération, manuel p. 51), ou s'accompagne d'un dispositif qui l'absorbe |
| Arrêt d'urgence | coupe physiquement le bus DC, **calibré pour du courant continu à cette tension** et au courant du fusible ; bouton à accrochage |
| Fusible | DC, à la tension du bus, au plus près de la source |
| Mesure d'effort | dynamomètre ou balance, étendue au-delà de l'effort au bout du bras pour 14 N·m ; résolution notée ; vérifiable avec une masse connue |
| Thermocouple | lecture jusqu'à 150 °C au moins ; fixation thermique décrite |
| Plaque | aluminium de 90 × 85 mm (la condition publiée, validée le 2026-10-01) ; alliage et épaisseur relevés |
| Adaptateur CAN | CAN 2.0 à 1 Mbit/s ; masse commune possible. **candleLight n'est pas conforme CE** selon son fabricant |
| Sécurité | extincteur CO₂ ou poudre ; détecteur de fumée ; lunettes de protection ; multimètre pour Vbus et la polarité |
