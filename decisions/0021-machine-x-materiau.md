# 0021 — Séparer la machine du matériau

Date : 2026-09-29
Statut : **abandonnée** le 2026-09-29 — jamais appliquée, remplacée par la
0026 puis la 0033. Conservée pour son analyse d'impact, qui reste juste.
Amendée par : `0026-machine-procede-matiere.md` — la clé composée ne tient pas à six axes ; migration SUSPENDUE.

## Ce qui est faux aujourd'hui

`hardware.yaml` nomme ses procédés `cutter_carton`,
`cutter_carton_ondule`, `laser_contreplaque`, `decoupe_metal`. Chaque
clé fond une **machine** et une **matière** en un seul mot.

C'est faux, et la conséquence est concrète : un laser de fablab coupe le
contreplaqué, l'acrylique, le carton, le cuir et le feutre. Avec la
structure actuelle, chacun de ces couples exige une clé nouvelle qui
répète la machine, et rien ne relie `laser_contreplaque` à
`laser_acrylique` — ni le lieu, ni le fait qu'il s'agisse du **même
appareil**, qu'on ne peut réserver qu'une fois.

Symétriquement, rien ne dit que `carton_ondule` est le même matériau
qu'on pourrait passer au laser.

## La structure proposée

Trois tables. Deux d'entités, une de **couples**.

```yaml
machines:
  cutter_main:
    nom: "cutter à main"
    lieu: "sur place"
    pilotage: manuel          # manuel | numerique
    saignee_propre: false     # la lame écarte, elle n'enlève pas
  laser_fablab:
    nom: "laser CO2 de fablab"
    lieu: "fablab"
    pilotage: numerique
    saignee_propre: true
  decoupe_cousin:
    nom: null                 # jet d'eau ? laser ? plasma ? À ÉTABLIR
    lieu: "chez le cousin"
    pilotage: numerique
    saignee_propre: true

materiaux:
  carton_plume:   { anisotrope: false, epaisseurs: [5.0] }
  carton_ondule:  { anisotrope: true,  epaisseurs: [] }
  contreplaque:   { anisotrope: true,  epaisseurs: [3.0] }
  aluminium:      { anisotrope: false, epaisseurs: [3.0] }

couples:
  cutter_main__carton_plume:
    valide: true
    epaisseur: 5.0
    saignee: null
    rayon_interieur_min: 2.5
    voile_min: null
  cutter_main__aluminium:
    valide: false
    motif: >
      un cutter à main ne coupe pas une tôle de 3 mm. Ce n'est pas une
      valeur qui manque : le couple n'existe pas.
```

**Clé de couple `machine__materiau`, pas une liste.** Une liste donnerait
des chemins `couples[3].saignee`, dont l'indice bouge à chaque insertion :
les motifs de `nullites.yaml` et `origines.yaml` et les clés des relevés
de pièces deviendraient instables. Une clé composée reste stable.

## La validité est une donnée, pas une omission

C'est le point central, et c'est la fiche 0020 appliquée aux couples.
Trois états, pas deux :

| Le couple… | se lit | ce qu'on en fait |
| --- | --- | --- |
| absent de la table | **pas encore instruit** | l'instruire |
| `valide: false` + `motif` | **impossible, et on sait pourquoi** | rien |
| `valide: true`, cotes nulles | **possible, à mesurer** | mesurer |

Sans le second état, l'absence de `cutter_main__aluminium` se lirait
comme un oubli. Avec, elle se lit comme un fait établi. C'est exactement
la distinction « non déterminé » / « sans objet » qui manquait hier au
site, un cran plus haut.

## Ce que cela casse — l'inventaire demandé

### `scripts/regenerer.py`

| Endroit | Ce qui casse |
| --- | --- |
| `etat_procede(p, nom)` | balaie `hw["procedes"]` ; devient un balayage des couples, et doit **sauter les `valide: false`** au lieu de les compter comme incomplets |
| `page_etat` | le tableau « Ce que je peux faire » gagne une colonne **Machine**, et une section « couples impossibles » avec leur motif |
| `page_etat`, « À mesurer » | balaie `("procedes", "materiaux")` ; devient `("machines", "materiaux", "couples")` |
| `page_piece`, `page_atelier` | lisent `p["machine"]`, `p["materiau"]`, `p["lieu"]` : ces champs viennent maintenant de **deux** tables jointes par le couple |
| noms de fichiers | `..._P2_cutter_carton.dxf` devient `..._P2_cutter_main__carton_plume.dxf` — **tous les liens du site changent**, et les anciens fichiers doivent disparaître de `site/fichiers/` |

### `params/nullites.yaml` — **et c'est ici que ça fait mal**

Les motifs `procedes.*.saignee` deviennent `couples.*.saignee` :
mécanique. Mais **la limite assumée de la fiche 0020 saute** :

> « Une condition ne porte que sur une clé **sœur**. »

Aujourd'hui, `decoupe_metal.rayon_interieur_min` est `se_deduira` parce
que sa sœur `machine` vaut `null`. Demain, la machine n'est plus une
sœur : c'est `machines.decoupe_cousin.nom`, dans une **autre table**.

Il faut donc étendre la condition à un chemin absolu :

```yaml
si: {chemin: "machines.decoupe_cousin.nom", vaut: null}
```

La fiche 0020 avait prévu ce jour et écrit que la limite se verrait :
« la règle ne correspondra pas et le champ ressortira en rouge — du bon
côté ». C'est ce qui arriverait. Mais il faut le corriger, pas le subir.

### `params/origines.yaml`

Les motifs `procedes.**` doivent devenir `machines.**`, `materiaux.**` et
`couples.**`. **Si on l'oublie, l'audit le dit** : chaque valeur non
couverte ressort `non_qualifie` et `--strict` sort à 1. C'est le seul
point de la migration qui se signale tout seul.

### Relevés des pièces

- `Cotes.procede(proc, cle)` devient `Cotes.couple(machine, materiau, cle)` ;
- les clés relevées passent de `procedes.cutter_carton.epaisseur` à
  `couples.cutter_main__carton_plume.epaisseur` ;
- `cotes_schema[].cle` suit, donc la **colonne Origine du tableau lettré**
  se rompt si on l'oublie — mais le garde-fou ajouté avec la fiche 0023
  (« clé absente du relevé ») **arrête la pièce** au lieu d'afficher un
  tiret ;
- `--procede cutter_carton` devient `--machine cutter_main --materiau
  carton_plume` ;
- `procede_defaut` devient `machine_defaut` **et** `materiau_defaut`.

## Ce que je recommande

Migrer en **une seule fois**, jamais en cohabitation : deux tables de
procédés vivant côte à côte donneraient deux vérités. Et commencer par
étendre `nullites.yaml` aux chemins absolus, **avant** la migration —
sinon la moitié des états de nullité tombe en rouge pendant la bascule,
et on s'habitue à du rouge qui ne veut rien dire.
