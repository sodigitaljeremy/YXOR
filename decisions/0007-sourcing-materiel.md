# 0007 — Sourcing des affirmations sur le matériel

Date : 2026-09-28
Espèce : close
État : appliquée
Statut : acceptée

## Contexte

Le chantier 3 a établi que, sur les 30 articulations, **20 n'ont aucune
source documentaire décrivant leur mécanisme**. La documentation
matérielle amont — nomenclature, manuel d'assemblage, PCB, impression 3D,
603 lignes au total — dit quoi acheter et comment assembler, jamais
comment une liaison est constituée.

La seule source autoritative est le **document Onshape** référencé par la
doc amont (`cad.onshape.com/documents/5aba041c…`). La question se pose
donc de l'ouvrir pour lever ces 20 inconnues.

## Décision

### 1. Onshape n'est pas une source de référence du projet

**Motif : il n'est pas couvert par l'ancrage.** La fiche 0002 fige le
dépôt amont au commit `e337f3b177b4b53abff70b31d1695a7b66cc6d2e` ; le
document Onshape, lui, est un document **vivant**. Il peut être modifié,
réorganisé ou supprimé **sans laisser de trace** et sans qu'aucun SHA ne
le signale.

Y puiser massivement reviendrait à réintroduire, au cœur des paramètres
mécaniques, exactement l'irreproductibilité que les fiches 0002, 0003 et
0006 ont été écrites pour éliminer. Une cote relevée aujourd'hui sur
Onshape serait, dans six mois, indistinguable d'une valeur inventée.

Le projet en a déjà fait les frais à petite échelle : la note sur le
genou de `params/joints.yaml` était vraie pour ToddlerBot 1.0 et fausse
pour la 2.0, sans que rien ne le signale.

### 2. Consultation ponctuelle, articulation par articulation

Onshape sera ouvert **au moment de dessiner une pièce qui s'y rattache**,
pour **une articulation à la fois**, jamais en relevé massif.

Chaque consultation est **datée dans le fichier**, au même titre qu'une
empreinte :

```yaml
    materiel:
      transmission: <ce qui a été constaté>
      version: "ToddlerBot 2.0.0"
      confiance: releve_onshape
      source: "Onshape 5aba041c…, consulté le AAAA-MM-JJ"
```

La date **est** la traçabilité : elle ne prouve pas que le document n'a
pas changé, mais elle dit précisément à quel état il se rapporte. C'est
le maximum atteignable sur une source qui ne se versionne pas, et cela
doit être énoncé comme tel plutôt que masqué.

### 3. Les 20 inconnues ne bloquent rien aujourd'hui

Aucune pièce n'est en cours de conception ; `parts/`, `robot/` et `bom/`
sont vides. Ces inconnues **bloqueront une pièce à la fois**, au moment
où elles deviendront pertinentes — et c'est précisément à ce moment
qu'une consultation ciblée aura du sens.

Le champ `confiance: inconnue` est là pour que ce blocage soit
**visible** quand il surviendra, au lieu d'être découvert après avoir
dessiné un support de moteur au mauvais endroit.

## Conséquences

- Toute affirmation sur le matériel porte une `source` et une `version`.
  **Une affirmation sans version est une affirmation périmable**, comme
  l'a montré le genou.
- `confiance: releve_onshape` est une quatrième valeur du vocabulaire,
  réservée aux relevés ponctuels et toujours accompagnée d'une date.
- Ce refus ne vaut pas jugement sur Onshape comme outil de conception :
  il porte uniquement sur son usage comme **source de vérité
  reproductible**.
