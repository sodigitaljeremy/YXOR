# 0015 — Architecture en plaques et entretoises, découpe 2D seule

Date : 2026-09-28
Statut : acceptée
Découle de : `0014-pas-d-imprimante-3d.md`

## Contrainte posée

> YXOR doit être fabricable avec des moyens que Jeremy peut obtenir,
> acheter et utiliser facilement. **Pas de machine unique, pas de procédé
> exotique, pas de tolérance serrée.**

Trois procédés accessibles, **tous de la découpe 2D** :

| Procédé | Matériau | Où |
| --- | --- | --- |
| cutter | carton, carton-plume | chez Jeremy, immédiat |
| laser | contreplaqué | fablab |
| découpe métal | aluminium | chez le cousin |

## 1 — Ce que l'architecture permet et interdit, face à ToddlerBot

### Ce qu'elle permet, et que ToddlerBot ne permet pas

- **Itérer en quelques minutes, à coût nul.** Un cutter et du carton
  donnent une pièce d'essai le jour même. Une pièce imprimée demande des
  heures. Pour un débutant qui doit apprendre à juger une pièce, c'est
  décisif — c'est le rythme d'apprentissage qui change, pas le prix.
- **Trois matériaux, une seule géométrie.** Le même dessin sert de la
  maquette carton à la pièce aluminium. Voir §3.
- **Aucune dépendance à une machine possédée.** Un fablab ou un artisan
  se remplacent ; une imprimante en panne, non.
- **Des pièces planes de précision.** Une découpe laser tient mieux
  l'écart entre deux perçages qu'une pièce imprimée, qui se rétracte au
  refroidissement.

### Ce qu'elle interdit

- **Les volumes.** Une pièce plate ne peut pas loger un moteur, guider un
  câble ou porter un bossage. Ces fonctions se reportent sur
  l'**empilement** : des plaques parallèles, tenues à distance par des
  entretoises. D'où le nom de l'architecture.
- **Les formes organiques.** Tout se ramène à des profils plans extrudés
  d'une épaisseur constante.
- **Les logements de roulement obtenus directement.** `CLAUDE.md`
  l'interdisait déjà ; la règle devient centrale. Un roulement se monte
  dans un **palier rapporté** du commerce.
- **Les filetages.** Ni le contreplaqué ni le carton ne tiennent un
  filet. L'assemblage passe par **vis traversantes et écrous**, ce qui
  sert d'ailleurs la règle « démontable, aucun collage ».
- **La compacité.** Un empilement de plaques est plus encombrant qu'un
  volume imprimé équivalent. **Le robot sera plus large.**

### La conséquence à ne pas manquer

**Les inerties changent.** Une plaque ajourée n'a ni la masse ni la
répartition d'un volume imprimé. Les politiques amont ont été entraînées
avec une randomisation de masse de **±20 %** (`body_mass_range` dans
`env_config.json`) : au-delà, leur transfert n'est plus couvert.

Ce n'est pas une objection — c'est une **hypothèse testable**, et elle se
teste ici, gratuitement : remplacer les inerties dans le modèle MuJoCo et
relancer `sim/upstream/replay_policy.py`. Le robot marche encore, ou non.

## 2 — La topologie de la fiche 0005 reste-t-elle tenable ?

**Oui pour les articulations. Non pour douze transmissions.**

La distinction à cinq identités de la fiche 0013 rend la réponse
précise, et c'est exactement ce pour quoi elle a été construite.

### Ce qui tient : les `articulation`

Un axe de rotation, une plage angulaire, un ordre de chaînage — rien de
tout cela ne suppose un procédé. Une plaque peut porter le même axe
qu'un volume imprimé. **Les 30 articulations, leurs axes, leurs sens et
leurs butées restent valables.**

Les motifs de la fiche 0005 — ne pas changer d'un coup morphologie,
cinématique, espace d'action et compatibilité des politiques — portaient
sur la **simulation**, que rien n'invalide ici.

### Ce qui ne tient pas : douze `actionnement`

| Mécanisme | Articulations | Réalisable en découpe 2D ? |
| --- | --- | --- |
| couplage par engrenage | 9 | **non** — un engrenage n'est pas un profil plan |
| bielle à quatre barres | 1 (`neck_pitch`) | **oui** — des bielles sont des pièces plates, c'est même le cas d'école |
| différentiel à deux moteurs | 2 (`waist_*`) | **non** — engrenages coniques |
| prise directe | 18 | **oui** |

**Dix-neuf sur trente passent sans rien changer.** Neuf demandent un
engrenage, deux un différentiel.

Trois issues, à instruire pièce par pièce et non ici :

1. **Acheter l'engrenage.** Il devient une `interface`, comme une vis.
2. **Passer en prise directe.** L'`articulation` est préservée,
   l'`actionnement` change. Conséquence : le couple et la plage
   utile changent, la commande est à remettre à l'échelle.
3. **Renoncer au degré de liberté** en P1.

**Le fichier `joints.yaml` absorbe les trois sans rien casser** : c'est
le bloc `actionnement` qui bouge, pas le bloc `articulation`. La
séparation faite au chantier 3 paie ici pour la première fois.

## 3 — Un dessin, trois matériaux : ce qui doit changer

**Correction d'emblée : ce n'est pas un même DXF.** C'est un **même
modèle paramétrique**, d'où l'on **génère trois DXF**. Le DXF est une
sortie figée, sans paramètre ; croire qu'un seul fichier servira les
trois est le piège à éviter.

Cinq paramètres changent entre les trois, et **tous sont de nature
`procede`** au sens de la fiche 0013 :

| Paramètre | Cutter / carton | Laser / contreplaqué | Découpe métal / alu |
| --- | --- | --- | --- |
| **épaisseur** | 5 mm (carton-plume) | 3 mm | 3 mm |
| **saignée** | ≈ 0 (la lame écarte) | ≈ 0,1–0,3 mm | 0,2–1,5 mm selon le moyen |
| **rayon intérieur minimal** | ≈ 0, mais 0,5 × ép. = 2,5 mm pour ne pas déchirer | ≈ saignée/2 | ≈ diamètre du jet ou de l'outil / 2 |
| **largeur de voile minimale** | large — le carton se déchire | moyenne | fine |
| **fixation** | vis + **rondelles larges** des deux côtés | vis + écrou | vis + écrou, ou taraudage possible |

### Ce qui en découle pour le modèle

- **L'épaisseur pilote toute la géométrie d'assemblage.** Dans une
  architecture en plaques, chaque fente reçoit une languette d'épaisseur
  égale au matériau. Une épaisseur en dur produirait un assemblage qui ne
  monte que dans un seul matériau.
- **La saignée décale le tracé.** Non compensée, les perçages sortent
  trop grands et les languettes trop fines. Elle est propre au couple
  machine-matériau, donc **à mesurer sur une pièce d'essai**, jamais à
  supposer.
- **Le rayon intérieur minimal est le plus contraignant des trois.** Pour
  qu'un dessin serve les trois, il doit respecter **le maximum** des
  trois minima.
- **La fixation change de nature.** Une vis dans 5 mm de carton-plume
  arrache sans rondelle ; en aluminium 3 mm elle peut être taraudée.

### Recommandation

Concevoir **au plus contraignant** — le carton — et laisser les deux
autres hériter. L'inverse produit des pièces carton inutilisables, or
c'est le carton qui permet d'itérer vite.

## 4 — Ce que cela change pour la première pièce

**La semelle survit, et son choix se trouve renforcé.** Elle était déjà
plate, déjà destinée à la chaîne DXF, déjà sans interface.

Quatre changements :

1. **Elle se fait en carton, aujourd'hui, au cutter.** Plus besoin
   d'attendre le cousin ni un fablab. La boucle d'apprentissage se ferme
   dans la journée.
2. **L'épaisseur devient 5 mm** (carton-plume), donc le rayon intérieur
   minimal passe de 1,5 à **2,5 mm**. Le creux d'arche proposé reste
   valable, ses congés grossissent.
3. **Elle doit être dessinée pour les trois matériaux dès maintenant**,
   même si un seul est coupé — c'est ce qui éprouve la
   paramétrisation par l'épaisseur.
4. **Elle cesse d'être une pièce d'apprentissage isolée** et devient le
   prototype de la méthode : un modèle, un paramètre d'épaisseur, trois
   DXF.

## Décision

1. **YXOR est conçu en plaques et entretoises, découpe 2D exclusivement**,
   tant qu'aucun autre procédé n'est vérifié.
2. **Aucune cote d'assemblage n'est écrite en dur** : toutes dérivent de
   l'épaisseur et de la saignée, de nature `procede`.
3. **La saignée de chaque couple machine-matériau est mesurée**, jamais
   supposée, avant toute pièce destinée à être montée.
4. **La topologie de la fiche 0005 est maintenue au niveau
   `articulation`.** Les douze `actionnement` à engrenage ou différentiel
   sont rouverts, à instruire un par un.

## Conséquences

- Le transfert des politiques amont devient une **hypothèse à tester**,
  la randomisation de masse à ±20 % ne couvrant pas un changement
  d'architecture. Test faisable en simulation, sans rien fabriquer.
- Le robot sera **plus large** qu'un équivalent imprimé. À intégrer dès
  la conception, pas à découvrir au montage.
- `hardware.yaml` doit accueillir un bloc par **couple machine-matériau**,
  et non par procédé générique.
