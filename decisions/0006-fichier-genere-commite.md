# 0006 — Un fichier généré qui est commité

Date : 2026-09-28
Statut : acceptée

## Contexte

Les 17 articulations de `params/joints.yaml` ont encore leurs butées à
`null`. Le fichier lui-même prévient : « les butées sont à extraire de
l'URDF ToddlerBot en phase 1, **PAS à inventer**. Une butée fausse
produit une marche qui fonctionne en simulation et casse le robot réel. »

L'extraction produit un fichier généré. Se pose donc la question de son
sort : versionné, ou relégué dans `exports/` comme tout artefact ?

## Le principe auquel on déroge

La règle 4 de `CLAUDE.md` pose que les artefacts générés — STEP, STL,
DXF, URDF, rendus — vont dans `exports/`, qui est ignoré par Git, **parce
qu'ils se régénèrent**.

> **Note terminologique.** Jeremy désigne cette règle par « LOG-1 ».
> Cet identifiant est **introuvable dans le dépôt** : il provient
> vraisemblablement de l'un des quatre documents de `docs/` toujours
> manquants (`00-cadrage`, `01-cahier-des-charges`, `02-plan-action`,
> `03-artefacts`). La présente fiche raisonne donc sur le principe tel
> que `CLAUDE.md` l'énonce. À reconfronter à LOG-1 quand le document
> sera récupéré.

## Ce qui rend ce cas différent

La règle repose sur une hypothèse implicite : **un artefact se régénère à
partir du dépôt lui-même**. Un STL se recalcule depuis le code de la
pièce et `anthropometry.yaml` ; supprimez-le, il revient.

Ce fichier-ci ne remplit pas cette condition. Il dérive du modèle MJCF
d'un **dépôt externe**, figé au commit `e337f3b177b4b53abff70b31d1695a7b66cc6d2e`
(fiche 0002). Si ce dépôt disparaît, est réécrit, ou voit son historique
purgé, le fichier n'est **plus régénérable** — et avec lui disparaissent
les seules butées non inventées dont le projet dispose.

C'est exactement le risque déjà consigné pour les poids (fiche 0003),
appliqué cette fois à une donnée textuelle.

## Options examinées

| Option | Écartée pour |
| --- | --- |
| Reléguer dans `exports/` | Perd les butées si l'amont disparaît : le cas que la règle ne prévoit pas |
| Recopier les valeurs dans `joints.yaml` à la main | Interdit par le fichier lui-même, et c'est la première source d'erreur silencieuse |
| Committer le fichier généré | Retenue |

## Décision

### 1. Exception, et son périmètre

`params/upstream_joints.generated.yaml` est **commité**, par exception au
principe de la règle 4.

L'exception est **étroite et motivée par un seul critère** : un artefact
généré est versionné si, et seulement si, **sa source est extérieure au
dépôt et donc hors de notre contrôle**. Tout artefact régénérable depuis
le dépôt seul reste dans `exports/`. Cette fiche ne crée aucune tolérance
générale, et surtout aucune sur les binaires : la règle 4 reste entière
sur ce point, le fichier produit est du texte.

### 2. Traçabilité obligatoire

Le fichier porte en tête le **SHA complet du commit amont** dont il
provient, la date d'extraction et la commande qui l'a produit. Sans cela
il serait une donnée orpheline, indistinguable d'une valeur inventée —
précisément ce que l'extraction cherche à éviter.

### 3. Jamais édité à la main

Le fichier est **produit par `scripts/import_upstream_limits.py` et par
rien d'autre**. Toute correction passe par le script, jamais par
l'éditeur. Un fichier généré qu'on retouche à la main est un fichier dont
plus personne ne connaît la provenance.

### 4. L'extracteur tourne avec le venv du projet

Vérifié le 2026-09-28 : MuJoCo 3.13.0 (venv YXOR) lit le MJCF amont et
renvoie des axes et des butées **identiques** à MuJoCo 3.3.4. Le script
n'importe pas `toddlerbot` : il traite le dépôt amont comme une **source
de données**, pas comme du code.

Il n'entre donc **pas** dans le carve-out `sim/upstream/` de la fiche
0004 et se lance normalement avec `.venv/bin/python`. La règle des deux
interpréteurs est intacte.

## Conséquences

- Le fichier généré est **lié au SHA d'ancrage**. Changer de commit amont
  impose de le régénérer, et invalide toute mesure qui s'y rapporte.
- Une divergence entre le fichier et `params/joints.yaml` est un signal,
  pas un détail : elle signifie que la nomenclature YXOR et le modèle
  amont ont cessé de décrire le même robot.
- La règle 3 n'est pas affectée : le fichier généré porte les noms
  **amont**, il ne prétend pas être la nomenclature YXOR.
