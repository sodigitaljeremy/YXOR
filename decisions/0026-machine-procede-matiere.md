# 0026 — Trois axes ne suffisent pas : la clé composée doit mourir

Date : 2026-09-29
Amendée par : `0033-epaisseur-cle-ou-champ.md` — le chiffrage du choix clé/champ sur nullites.yaml et origines.yaml.
Statut : **proposée** — rien n'est appliqué.
Amende : `0021-machine-x-materiau.md` — **sa migration est SUSPENDUE.**

Un retour extérieur signale que le couple machine × matériau est trop
grossier : laser + alu 2 mm n'est pas laser + alu 6 mm, ni laser +
contreplaqué 6 mm. C'est juste, et cela invalide la structure proposée
par la fiche 0021 **avant** qu'elle soit appliquée. Tant mieux : migrer
deux fois coûte cher.

## 1 — La DIN 8580 : ce que j'ai vérifié, et ce que je n'ai pas lu

**Elle existe, et la révision 2022 aussi.** `DIN 8580:2022-12`,
*Fertigungsverfahren — Begriffe, Einteilung*, remplace `DIN 8580:2003-09`.

**Je n'ai pas lu la norme elle-même** : elle est payante. J'ai vérifié
son existence, sa date, son principe d'ordonnancement, ses six groupes
principaux et le classement de nos trois procédés auprès de sources
secondaires concordantes. Tout ce qui suit porte cette réserve.

### Le principe d'ordonnancement, qui est l'intérêt de la norme

La DIN 8580 ne classe pas les procédés par machine, ni par matériau, ni
par métier. Elle les classe par **ce qui arrive à la cohésion**
(*Zusammenhalt*) de la matière :

| | Groupe principal | Cohésion |
| ---: | --- | --- |
| 1 | Urformen — mise en forme initiale | **créée** |
| 2 | Umformen — déformation | conservée |
| 3 | **Trennen — séparation** | **diminuée** |
| 4 | Fügen — assemblage | augmentée |
| 5 | Beschichten — revêtement | augmentée |
| 6 | Stoffeigenschaft ändern | propriétés modifiées |

Nos trois procédés sont **tous** dans le groupe 3, et c'est leur
sous-groupe qui les sépare :

| Notre procédé | DIN 8580 | Ce que ça dit |
| --- | --- | --- |
| cutter à main | **3.1 Zerteilen** → Keilschneiden → *Messerschneiden* | mécanique, **sans formation de copeau** |
| laser | **3.4 Abtragen** | la matière est **enlevée** |
| jet d'eau, plasma | **3.4 Abtragen** | idem |

### Ce que cela nous apprend, concrètement

`hardware.yaml` note déjà, pour le cutter : « la lame écarte plutôt
qu'elle n'enlève ». **La norme donne un nom à cette observation** —
Zerteilen se définit précisément comme la séparation *ohne Spanbildung*,
sans copeau — et elle en tire une conséquence que nous n'avions pas vue :

> **La saignée n'est pas une inconnue du couple. Son EXISTENCE est
> prédite par le groupe DIN.** Zerteilen ne retire pas de matière, donc
> saignée structurellement nulle. Abtragen en retire toujours, donc
> saignée non nulle, et croissante avec l'épaisseur.

Autrement dit : sur les quatre `saignee: null` de `hardware.yaml`, celle
du cutter n'est pas « à mesurer » au même titre que les autres. C'est
une prédiction testable, et c'est exactement le genre de distinction que
la fiche 0020 existe pour porter.

**Et un fait qui touche votre chantier 4 :** la révision 2022 ajoute le
groupe **1.10 « Urformen durch additive Fertigung »**. L'impression 3D
n'est pas une variante de découpe : c'est le **groupe principal 1**, à
l'autre bout de la classification. Toute l'architecture du projet vit
dans le groupe 3. Acheter une imprimante n'ajoute pas un procédé, cela
ouvre un second groupe principal.

### Comment l'employer : vocabulaire racine, pas modèle de données

La DIN 8580 nomme **ce que le procédé fait à la matière**. Elle ne dit
rien de la machine, du matériau, de l'épaisseur ni des réglages. S'en
servir comme modèle de données serait une erreur de catégorie.

Proposé : un champ `din: "3.1"` sur chaque procédé, avec son nom
allemand. Il ne pilote aucun calcul. Il donne un **vocabulaire stable et
extérieur au projet**, qui survivra à nos renommages — et il permet à
qui nous lit de rattacher notre bricolage à une classification connue.

## 2 — Vos trois questions

### L'épaisseur entre-t-elle dans la CLÉ ?

**Non.** Et le critère qui tranche est celui-ci :

> Cet axe crée-t-il une **chose différente**, ou une **mesure différente
> de la même chose** ?

- Changer de machine ou de matériau crée une **chose différente** : un
  laser n'est pas un cutter, l'alu n'est pas le carton.
- Changer d'épaisseur crée une **mesure différente** de la même chose :
  c'est toujours « le laser du fablab sur de l'alu ». La saignée change,
  le procédé non.

L'épaisseur est donc un **déterminant des valeurs mesurées**, pas un
composant d'identité. Elle est un **champ**, et il peut y avoir plusieurs
enregistrements pour un même laser + alu, à des épaisseurs différentes.

Confondre déterminant et identité est précisément ce qui a produit
`cutter_carton` et `cutter_carton_ondule`.

### La forme (tôle, barre, profilé) ?

**Champ aussi, mais pas du même objet.** La forme ne qualifie pas le
procédé : elle qualifie **la matière première**. On n'achète pas « de
l'aluminium », on achète *une tôle de 3 mm* ou *une barre de 20*.

Et elle décide **quels procédés s'appliquent** : on ne découpe pas une
barre au laser 2D. C'est donc un attribut de la matière, qui conditionne
la validité du couple — pas un axe supplémentaire du couple.

D'où une entité que ni la 0021 ni la proposition reçue n'isolent :
**la matière première** = matériau × forme × épaisseur. C'est l'objet
qu'on achète, qu'on stocke et qu'on mesure.

### Que devient la clé composée avec trois axes de plus ?

**Elle meurt, et il faut l'assumer.**

```
laser_fablab__abtragen__aluminium__tole__3mm__reglage_std
```

Illisible, et surtout : l'espace explose. 3 machines × 4 matériaux ×
3 formes × 5 épaisseurs = **180 combinaisons**, dont l'immense majorité
n'existe pas. Déclarer la validité de chacune, comme la 0021 le
proposait, devient absurde.

> **La clé composée était la bonne réponse à deux axes. C'est la
> mauvaise réponse à six.**

Quand il faut N axes, on n'allonge pas la clé : on écrit des
**enregistrements à N champs déclarés**, et on indexe à la lecture.

Le seul obstacle était l'instabilité des indices de liste — j'en avais
fait l'argument principal de la 0021. Il se lève d'une ligne : chaque
enregistrement porte un **`id` court, écrit à la main**, et le moteur de
motifs adresse `reglages.<id>.saignee`. Stable parce qu'écrit, pas
calculé depuis une position.

## 3 — La structure proposée

Quatre tables. Trois d'entités, une de mesures.

```yaml
machines:
  laser_fablab:   { nom: "laser CO2 de fablab", lieu: fablab,
                    pilotage: numerique, puissance_W: null }
  cutter_main:    { nom: "cutter à main", lieu: "sur place", pilotage: manuel }
  decoupe_cousin: { nom: null, lieu: "chez le cousin", pilotage: numerique }

procedes:                       # vocabulaire DIN 8580, aucun calcul
  messerschneiden:   { din: "3.1", famille: zerteilen, enleve_matiere: false }
  abtragen_thermique:{ din: "3.4", famille: abtragen,  enleve_matiere: true }
  abtragen_jet:      { din: "3.4", famille: abtragen,  enleve_matiere: true }

matieres:                       # matériau x forme x épaisseur = ce qu'on achète
  carton_plume_5:  { materiau: carton_plume, forme: plaque,
                     epaisseur: 5.0, anisotrope: false }
  alu_tole_3:      { materiau: aluminium, forme: tole,
                     epaisseur: 3.0, anisotrope: false }
  alu_tole_6:      { materiau: aluminium, forme: tole, epaisseur: 6.0 }

reglages:                       # LA table qui porte les mesures
  - id: cutter_cartonplume_5
    machine: cutter_main
    procede: messerschneiden
    matiere: carton_plume_5
    valide: true
    saignee: 0.0                # prédit nul : Zerteilen, sans copeau
    rayon_interieur_min: 2.5
    voile_min: null
  - id: cutter_alu_3
    machine: cutter_main
    matiere: alu_tole_3
    valide: false
    motif: "un cutter à main ne coupe pas une tôle de 3 mm"
```

`reglages` est une **liste**, mais chaque entrée porte son `id` : le
chargeur en fait un dictionnaire, et les motifs de `origines.yaml` et
`nullites.yaml` s'écrivent `reglages.cutter_alu_3.saignee`.

Les trois états de validité de la fiche 0021 sont conservés tels quels :
absent = pas instruit ; `valide: false` + motif = impossible et on sait
pourquoi ; `valide: true` avec des nuls = possible, à mesurer.

## 4 — Ce que je recommande

1. **Suspendre la 0021.** Elle n'a jamais été appliquée ; elle ne doit
   pas l'être. Cette fiche l'amende.
2. **Ne migrer qu'une fois**, vers cette structure-ci.
3. **Étendre `nullites.yaml` aux chemins absolus d'abord.** La 0021 avait
   déjà relevé que la condition « clé sœur » sauterait ; avec quatre
   tables au lieu de deux, elle saute plus fort.
4. **Écrire un chargeur, pas des accès directs.** Avec quatre tables
   jointes, le code des pièces ne doit jamais faire la jointure lui-même :
   `c.reglage(machine, matiere)` rend un enregistrement résolu, ou lève.

## 5 — Ce que je n'ai pas tranché

- Le **profil de réglages** de la proposition reçue (vitesse, puissance,
  nombre de passes) : il est propre au pilotage numérique, et nous n'avons
  aucune machine numérique à nous. Prévoir le champ `reglages_machine`
  comme bloc libre, ou attendre d'en avoir une ? Je ne sais pas.
- Si `saignee: 0.0` pour le Messerschneiden doit être **écrit** (prédit
  par la norme) ou **mesuré** (constaté chez nous). Écrire une valeur
  prédite dans un champ destiné aux mesures brouillerait la fiche 0010.
  C'est peut-être une origine à part.

## Sources

- DIN 8580:2022-12, *Fertigungsverfahren — Begriffe, Einteilung* —
  fiche catalogue DIN Media et ANSI Webstore (norme non lue, payante).
- Classement de Laserstrahlschneiden et Wasserstrahlschneiden en
  3.4 Abtragen : littérature technique concordante.
- Sous-groupes du Zerteilen (DIN 8588) et définition *ohne Spanbildung*.
