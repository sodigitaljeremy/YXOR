# Protocole d'essai du carton, à la maison

**Rédigé le 2026-10-08** (prompt « Étude de YXOR Kit », point 3). PROPOSÉ : le protocole est à valider par
Jeremy avant le premier essai.

**Pourquoi.** Aucun carton ondulé vendu au détail ne publie sa rigidité ni sa résistance (étude de marché du
2026-10-08, `params/cartons.yaml`). Le classement des cartons (`docs/kit-etude-2026-10.md`) repose donc sur une
approximation (e²/σ). Ces essais la remplacent par des mesures. Ce seront les **premières mesures mécaniques** du
projet. Les seules mesures faites jusqu'ici sont des masses et des épaisseurs (`params/mesures.yaml`,
2026-09-29).

**Matériel**, celui d'un ménage :

- deux piles de livres de même hauteur ;
- des bouteilles d'eau de 0,5 L et 1,5 L (1 L d'eau pèse 1 kg ; la bouteille vide pèse en plus, voir plus bas) ;
- un sac ou un seau léger, avec une ficelle ;
- une règle graduée au millimètre et une équerre ;
- un cutter ;
- la balance de cuisine du 2026-09-29.

Prévoir **2 ou 3 cartons**, par exemple le carton ondulé double de récupération déjà mesuré et un ou deux cartons
du classement.

## Ce qu'on mesure, et ce que ça veut dire

- **La rigidité en flexion** : combien une bande de carton posée sur deux appuis plie sous un poids. C'est ce qui
  fait qu'un bras ou une cuisse en carton reste droit. Elle se calcule à partir de la flèche, c'est-à-dire de
  l'enfoncement au milieu de la bande. La formule de la poutre sur deux appuis chargée en son milieu donne
  `EI = F·L³ / (48·δ)` :
  - F, la force (N) : la masse suspendue (kg) × 9,81 ;
  - L, l'écart entre les appuis (m) ;
  - δ, la flèche (m).

  EI se compare d'un carton à l'autre, et d'un sens à l'autre. Le carton ondulé est **anisotrope** : il est bien
  plus rigide dans le sens des cannelures (`params/hardware.yaml`, `note_anisotropie`).
- **La résistance à l'écrasement sur chant** : la charge qu'une petite bande debout supporte avant de s'écraser.
  C'est l'équivalent maison de l'**ECT** (*edge crush test*), la grandeur que publient les qualités normalisées
  (DIN 55468-1, en kN/m). Elle dit si une paroi de coque tient la charge d'un segment posé dessus. Elle se
  calcule en divisant la charge à la rupture (N) par la largeur de la bande (m).

## Essai 1 : flexion (trois points)

1. **Découper** au cutter, à la règle, 3 bandes de **50 mm × 300 mm** par sens : cannelures dans la longueur,
   puis cannelures en travers. Noter le sens au crayon sur chaque bande.
2. **Poser** la bande à plat sur les deux piles de livres, écartées de **L = 200 mm** de bord à bord, mesurés à la
   règle. Les bords des livres servent d'appuis.
3. **Repère** : poser la règle debout contre la bande, au milieu, zéro sur la table, et lire la hauteur du
   dessous de la bande, à vide.
4. **Charger** : suspendre le sac au milieu par la ficelle, passée autour de la bande. Ajouter les bouteilles
   une à une (0,5 kg, puis 1 kg, puis 1,5 kg…). À chaque palier, attendre 30 s, puis relire la hauteur. La
   flèche δ est l'écart avec la lecture à vide.
5. **S'arrêter** à la première marque, au premier pli, ou quand la flèche dépasse 20 mm (au-delà, la formule ne
   vaut plus). Noter le dernier palier tenu.
6. **Peser** le sac et chaque bouteille pleine sur la balance. On ne suppose pas « 1 L = 1 kg » pour la
   bouteille entière : le plastique et le bouchon comptent.

Pour chaque bande, garder la **pente du début** : la flèche aux deux ou trois premiers paliers, là où elle croît
proportionnellement à la charge. Le calcul de EI se fait dans le script, pas à la main.

## Essai 2 : écrasement sur chant

1. **Découper** 3 bandes de **25 mm de large × 30 mm de haut** par carton, cannelures **verticales** (comme
   dans la paroi d'une boîte). Courte et basse, la bande s'écrase avant de flamber, c'est-à-dire avant de se
   courber sur le côté.
2. **Tenir la bande debout** entre deux livres serrés de part et d'autre, à 1 mm près, sans la pincer : ils
   l'empêchent de basculer, ils ne la portent pas. Vérifier à l'équerre qu'elle est verticale.
3. **Poser un livre rigide à plat dessus**, centré, puis ajouter les bouteilles une à une sur le livre.
4. **Relever le palier** où la bande s'écrase : elle plie, gondole ou s'affaisse de plus de 2 mm. La charge à la
   rupture est la masse totale posée, livre compris, pesée à la balance.

Ordre de grandeur, pour ne pas être surpris : une qualité 1.20 B annonce 3,5 à 4,0 kN/m (sources divergentes,
`params/cartons.yaml`). Sur 25 mm, cela fait environ 90 à 100 N, soit **9 à 10 kg**. Prévoir assez de
bouteilles, et une pile stable. Pour moins de charge, réduire la largeur à 15 mm.

## Essai 0, rappel : masse surfacique et épaisseur

C'est la méthode du 2026-09-29 (`params/mesures.yaml`) :

- **masse surfacique** : peser un grand panneau, d'environ 200 × 150 mm, et le mesurer à la règle ;
- **épaisseur** : la mesurer à la règle sur une pile de 10 feuilles, sous une pression légère, puis diviser par
  10. Pas de pied à coulisse sur un carton ondulé : ses becs écrasent les cannelures.

C'est l'essai qui complète les cartons « à peser » du classement.

## Noter les résultats dans `params/mesures.yaml`

La règle du fichier tient : **une entrée par grandeur DIRECTEMENT mesurée**. On n'y inscrit jamais une grandeur
dérivée comme EI ou l'ECT : elles se calculent. Chaque relevé, avec son instrument et son incertitude :

```yaml
  carton_bc_flexion_fleche_long_b1_2026_10_xx:
    grandeur: "flèche au milieu, bande 1, cannelures dans la longueur, palier 1"
    valeur: 3.0
    unite: mm
    incertitude: 0.5
    type_incertitude: resolution
    instrument: "règle graduée au millimètre, lue debout contre la bande"
    n: 1
    date: 2026-10-xx
    alimente: [essais_carton.ondule_bc_double_modulor.flexion]
    note: "L = 200 mm ; charge 1,02 kg pesée (bouteille 1 L pleine)"
```

Il faut aussi une entrée pour l'écart entre les appuis (L), pour chaque charge pesée et pour la largeur de
chaque bande. Le calcul de EI et de la charge d'écrasement par mètre se fera par un script (à écrire au moment des
premiers relevés, avec son test : règle 9). Ce script remplacera l'approximation e²/σ du classement.

## Ce que ces essais ne disent pas

- La tenue **d'une liaison** (un trou de vis, un tenon) : elle demande un autre essai, à définir après le choix
  du carton.
- La tenue **dans le temps** (fluage) et à **l'humidité** : le carton perd de sa rigidité dans un air humide. Il
  faut noter la saison et la pièce où l'essai a lieu.
- **La précision des cotes** : le carton reste une maquette sans métrologie (fiche 0060). Les essais servent à
  comparer des cartons entre eux, pas à certifier une pièce.
