# 0043 — Deux matières ou une ? Et ce que le dépôt ne sait pas de la matière qu'on a eue en main

Date : 2026-09-29
Espèce : close
État : appliquée
Statut : **appliquée** le 2026-09-29 — profil confirmé à la tranche, matière dédoublée, suspension levée.

## RÉSOLUTION — 2026-09-29

**Le profil est confirmé : DOUBLE cannelure.** Observation directe de la
tranche par Jeremy — **deux rangées d'arches séparées par un papier
intermédiaire, trois papiers plats au total**. Photo IMG_6597, hors
dépôt.

C'est exactement le constat que cette fiche appelait de ses vœux :
**binaire, visible à l'œil, et indépendant de toute fourchette de
grammage** que le dépôt ne possède pas et n'inscrira pas (fiche 0028).

**Le couple exact n'est pas identifié** — E+E, E+B ou autre. Rien ne
permet de trancher, et rien n'est inscrit à ce sujet.

### Ce que cela résout, et ce que cela ne résout pas

| | |
| --- | --- |
| **résolu** | l'identité de la matière. `carton_ondule_double` créée, les mesures y sont déplacées, la suspension est levée |
| **résolu** | l'anomalie des 649 g/m² : élevé pour une simple, cohérent pour une double |
| **NON résolu** | l'épaisseur de 3,5 mm reste mince pour une double. La zone mesurée a pu être empilée, donc comprimée |
| **NON résolu** | la densité reste une **borne haute** : l'écrasement réduit l'épaisseur, donc gonfle la densité |

### Ce que l'épisode a coûté et rapporté

**Coût** : une journée de valeurs inscrites sous un nom faux.

**Rapport** : la correction a été possible **parce que l'objet existait
encore et qu'on pouvait le regarder**. C'est la chance de ce cas, pas une
propriété du dépôt — et c'est précisément l'argument du §3 ci-dessous.

## 1 — Simple et double : deux matières, et votre avis tient

> « On ne les achète pas ensemble, elles n'ont ni la même épaisseur ni la
> même masse surfacique, et `matieres` décrit ce qu'on achète. »

**Je ne trouve pas d'argument contre, et j'en trouve trois pour.**

**a. C'est déjà la définition retenue.** La fiche 0026 a créé `matieres`
précisément pour porter *matériau × forme × épaisseur* — « ce qu'on
achète ». Une simple et une double cannelure ne partagent aucune des
trois. En faire une seule entrée avec un paramètre reviendrait à
défaire ce qui a été décidé il y a deux jours.

**b. Le critère de la fiche 0033 tranche déjà.** Il demande : *cet axe
crée-t-il une chose différente, ou une mesure différente de la même
chose ?* On n'achète pas « du carton ondulé » puis on choisit le profil :
**on achète une simple ou une double**, avec sa référence, son épaisseur
et son prix. C'est une **chose différente**, donc une identité, donc une
entrée.

**c. Le contre-exemple est instructif.** L'aluminium en tôle de 3 et de
6 mm sont **aussi** deux `matieres` (`alu_tole_3`, `alu_tole_6`) et
personne n'a songé à en faire une matière paramétrée par l'épaisseur. Le
profil de cannelure joue exactement le même rôle : il change ce qu'on
prend sur l'étagère.

### Ce que cela implique, concrètement

| | |
| --- | --- |
| entrées | `carton_ondule_simple` et `carton_ondule_double` |
| matériau commun | `carton_ondule` reste UN matériau — l'anisotropie et le sens des cannelures sont les mêmes |
| ce qui les sépare | `epaisseur`, `masse_surfacique`, et donc `densite` |

**Mais `densite` est aujourd'hui sur le MATÉRIAU**, pas sur la matière —
et deux profils n'ont pas la même densité apparente. **C'est une
deuxième erreur de localisation**, de la même famille que le verdict
(0037) et le rayon (0042) : une grandeur attachée à l'entité qui
semblait la porter.

Je le signale sans le corriger : cela touche `nullites.yaml`,
`origines.yaml` et le chargeur, et ce n'est pas le moment.

### Le seul argument que je vois contre

Le carton **de récupération** n'a pas de référence d'achat. On ne
l'« achète » pas, on le trouve. Deux entrées supposent qu'on sache
laquelle on a — ce qui est exactement le problème du §3.

Cela n'invalide pas la distinction : cela dit qu'**il faudra savoir
classer un carton trouvé**, et qu'une troisième entrée
`carton_ondule_indetermine` sera peut-être nécessaire. Je ne la propose
pas : elle risque de devenir la poubelle où tout finit.

## 2 — Les deux hypothèses, et une troisième qui les réconcilie

**Votre lecture est juste sur les deux points.**

- **649 g/m² est élevé pour une simple cannelure.** Deux couches d'arches
  et trois papiers l'expliqueraient mieux qu'une couche et deux papiers.
- **3,5 mm est mince pour une double**, qui fait couramment le double.

⚠ Je n'ai **aucune source dans le dépôt** pour les fourchettes usuelles
de grammage et d'épaisseur par profil. Ce qui précède est un ordre de
grandeur de mémoire technique, et c'est exactement ce que la fiche 0028
m'interdit de présenter comme un fait. **À sourcer avant d'en tirer quoi
que ce soit.**

### Les deux hypothèses ne s'excluent pas

C'est le point que je voudrais ajouter : **une double cannelure écrasée
satisfait les deux observations à la fois.**

L'écrasement ne change **ni la masse ni l'aire**, donc **pas la masse
surfacique**. 649 g/m² reste vrai quel que soit l'état du carton — c'est
une grandeur robuste.

Mais l'écrasement **réduit l'épaisseur**. Donc :

> `densite = masse_surfacique / epaisseur` est **surestimée** si le
> carton a été comprimé. Les 186 kg/m³ sont une **borne haute**.

C'est inscrit comme tel dans `hardware.yaml`.

### Ce qui trancherait

**Regarder la tranche**, comme vous le prévoyez : une double cannelure
montre **deux rangées d'arches séparées par un papier intermédiaire**.
C'est visible à l'œil nu, et c'est un fait binaire — pas une mesure.

Cela vaut mieux que toute déduction à partir du grammage, qui repose sur
des fourchettes que le dépôt ne possède pas.

## 3 — Ce que le dépôt ne sait pas : le lot

> « Une mesure a été inscrite sous le mauvais nom de matière, et rien ne
> pouvait le signaler : le dépôt ne sait pas ce que j'ai eu dans les
> mains. »

**C'est exact, et c'est structurel.** Le champ `alimente` de
`mesures.yaml` fait pointer une mesure vers une matière **supposée**. Si
la supposition est fausse, la mesure atterrit au bon format sur le mauvais
objet, et aucun contrôle ne peut le voir — parce qu'aucun contrôle n'a
accès à la matière physique.

### Ce qu'il faudrait, et ce que ça vaut

Une mesure devrait porter **ce qui a été mesuré**, et non seulement **ce
qu'on croit que c'était** :

```yaml
panneau_masse_2026_09_29:
  lot: carton_recup_colis_A       # l'objet physique, identifié
  matiere_supposee: carton_ondule_simple
```

Et un registre des lots, minimal :

```yaml
lots:
  carton_recup_colis_A:
    origine: "colis de récupération, provenance inconnue"
    date_entree: 2026-09-29
    profil: null                  # à établir en regardant la tranche
    note: "marquer physiquement le panneau : LOT A"
```

**Trois bénéfices, dont un seul compte vraiment :**

1. Plusieurs mesures sur le même lot deviennent **comparables**, et une
   divergence entre elles devient un signal.
2. Une réattribution de matière — « en fait c'était du double » — se fait
   **en un endroit**, et toutes les mesures du lot suivent.
3. **Et le seul qui compte : le lot force à marquer physiquement le
   carton.** Un identifiant qui n'existe que dans un fichier ne relie
   rien. Écrit au feutre sur le panneau, il relie le dépôt à l'établi.

### Ce que je ne recommande pas

**Ne pas construire cela maintenant.** Trois raisons :

- **Un seul lot existe.** Un registre à une entrée est une abstraction
  qui n'a rien à abstraire — c'est précisément YAGNI, et la fiche 0036
  a posé le critère : *une fiche est justifiée si son absence rendrait
  une décision inexplicable dans six mois*. Un champ l'est aussi.
- Le vrai problème du jour n'est pas la traçabilité, c'est
  l'**identification** : on ne sait pas quel profil on a. Un registre de
  lots n'aurait rien dit de plus — il aurait porté `profil: null` et le
  doute serait identique.
- Et il se construira mieux **quand il y aura deux lots à distinguer**,
  parce qu'on saura alors ce qu'il faut vraiment en retenir.

### Ce que j'en retiens quand même

**La leçon n'est pas qu'il manque un champ. C'est que le dépôt a inscrit
une mesure sous un nom qu'il ne pouvait pas vérifier, sans le dire.**

Les valeurs portent désormais leur doute en clair dans `hardware.yaml`.
C'est moins qu'un registre de lots, et c'est ce que la situation permet
d'honnête aujourd'hui.

## Ce que j'attends pour continuer

Le **profil**, vu à la tranche. Et une nouvelle épaisseur sur une zone
jamais empilée — car c'est elle, et non la masse, qui limite désormais la
densité à ±14,5 %.
