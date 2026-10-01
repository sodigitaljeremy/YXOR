# 0033 — L'épaisseur reste un CHAMP : le coût de l'autre choix, chiffré

Date : 2026-09-29
Espèce : gouvernante
État : appliquée
Statut : **acceptée** le 2026-09-29 — option B appliquée le jour même.
Amende : `0026-machine-procede-matiere.md`, qu'elle complète du chiffrage
demandé.

La fiche 0026 tranchait déjà « champ, pas clé », sur un argument de
principe. Voici le coût mesuré de chaque choix sur `nullites.yaml` et
`origines.yaml` — ce qui était demandé, et ce qui manquait.

## L'état actuel, pour comparer

| Fichier | Règles | Dont sur `procedes`/`materiaux` |
| --- | ---: | ---: |
| `origines.yaml` | 27 au total | **3** |
| `nullites.yaml` | 10 au total | **9** |

Quatre procédés instruits aujourd'hui, pour **12 valeurs mesurables**.

## Option A — l'épaisseur entre dans la clé

```yaml
couples:
  laser_fablab__aluminium__tole__2: { saignee: null, ... }
  laser_fablab__aluminium__tole__6: { saignee: null, ... }
```

### Coût sur `origines.yaml`

Les trois règles actuelles utilisent déjà le joker :
`procedes.*.epaisseur` devient `couples.*.epaisseur`. **Coût : trois
motifs réécrits, rien de plus.** Le joker absorbe la combinatoire.

C'est le piège de cette option : **elle a l'air gratuite ici.**

### Coût sur `nullites.yaml` — et là elle ne l'est pas

Neuf règles, dont **deux portent une condition** qui distingue deux cas
du même nom :

```yaml
- motif: "procedes.decoupe_metal.rayon_interieur_min"
  si: {cle: machine, vaut: null}          # dépend du MOYEN
- motif: "procedes.*.rayon_interieur_min"
  si: {cle: epaisseur, vaut: null}        # vaut 0,5 x l'épaisseur
```

Avec l'épaisseur dans la clé, ces conditions **cessent de pouvoir
s'écrire au bon grain** :

- `couples.*.saignee` couvre tout, mais ne distingue plus rien ;
- `couples.laser_*.saignee` ne sépare pas le 2 mm du 6 mm — **or c'est
  exactement la distinction que le retour extérieur réclame** ;
- pour la retrouver, il faut **un motif par épaisseur** :
  `couples.laser_fablab__aluminium__tole__2.saignee`, et ainsi de suite.

**Coût réel : le nombre de règles de `nullites.yaml` croît avec le nombre
d'épaisseurs instruites.** Aujourd'hui 9 ; avec 5 épaisseurs distinguées,
l'ordre de grandeur passe à plusieurs dizaines, et **chacune répète la
machine et le matériau dans son motif**.

### Le coût caché, qui est le pire

Une clé composée **encode de la donnée dans un identifiant**. Pour savoir
si un réglage concerne une tôle de 2 ou de 6 mm, il faut **analyser la
chaîne de caractères**. Le jour où l'on voudra « tous les réglages
au-dessus de 4 mm », il n'y aura aucun moyen de le demander — sinon en
découpant des clés.

C'est la faute de `cutter_carton`, répétée : une information rangée dans
un nom au lieu d'un champ.

### Et l'espace à déclarer

3 machines × 4 matériaux × 3 formes × 5 épaisseurs = **180 clés
possibles**, contre **4 réellement instruites**. Déclarer la validité de
chacune, comme la fiche 0021 le proposait, devient impraticable.

## Option B — l'épaisseur reste un champ

```yaml
reglages:
  - id: laser_alu_2
    machine: laser_fablab
    matiere: alu_tole_2        # matériau x forme x épaisseur
    saignee: null
```

### Coût sur `origines.yaml`

Trois motifs réécrits, comme en option A : `reglages.*.saignee`,
`reglages.*.rayon_interieur_min`, `matieres.*.epaisseur`. **Coût
identique.**

### Coût sur `nullites.yaml` — et c'est là que tout se joue

**Les neuf règles restent neuf**, et les deux conditions **continuent de
s'écrire**, parce que l'épaisseur devient une **clé sœur** au sein de
l'enregistrement :

```yaml
- motif: "reglages.*.rayon_interieur_min"
  si: {cle: epaisseur, vaut: null}       # la sœur existe : ça marche
```

C'est le point décisif. La fiche 0020 a posé, comme limite assumée,
qu'une condition ne porte que sur une **clé sœur**. L'option B **respecte
cette limite** ; l'option A la fait sauter, et obligerait à étendre le
moteur aux chemins absolus **avant même de pouvoir migrer**.

### Coût propre à l'option B

Un **chargeur** devient nécessaire : `reglages` référence `machines` et
`matieres`, et la jointure doit être faite une fois, pas dans chaque
pièce. Estimé : 30 à 40 lignes, et un point d'échec unique et lisible
plutôt que dispersé.

## Le tableau de décision

| | Option A — clé | Option B — champ |
| --- | --- | --- |
| motifs `origines.yaml` | 3 réécrits | 3 réécrits |
| règles `nullites.yaml` | **croît avec les épaisseurs** | **reste à 9** |
| conditions `si` | **cassées** — plus de clé sœur | **intactes** |
| extension du moteur de motifs | **obligatoire avant migration** | aucune |
| interroger « au-dessus de 4 mm » | découper des chaînes | filtrer un champ |
| espace à déclarer | 180 clés possibles | 4 enregistrements |
| code supplémentaire | aucun | chargeur, ~35 lignes |

## Tranché : option B

L'épaisseur reste un **champ**, et un champ de la **matière première**,
pas du réglage — on n'achète pas « de l'aluminium », on achète une tôle
de 3.

Le critère de la fiche 0026 tient, et il est maintenant chiffré : un axe
qui crée une **mesure différente de la même chose** est un champ ; un axe
qui crée une **chose différente** est une identité.

Et le chiffrage révèle ce que le principe seul ne montrait pas :
**l'option A ne coûte rien à `origines.yaml`** — c'est ce qui la rend
tentante — **et coûte la structure même de `nullites.yaml`**. Le fichier
le moins visible est celui qui paie.

## Ce qui reste à faire avant toute migration

1. **Étendre `nullites.yaml` aux chemins absolus quand même.** L'option B
   préserve les conditions existantes, mais la machine passe dans une
   autre table : `si: {chemin: "machines.decoupe_cousin.nom", vaut: null}`
   restera nécessaire pour le cas de la découpe métal.
2. **Écrire le chargeur avant la donnée.** Une jointure faite deux fois
   est une divergence en attente.
3. **Migrer une seule fois.** Deux structures de procédés vivant côte à
   côte donneraient deux vérités.
