# 0030 — Aucun fichier fournisseur non redistribuable dans le dépôt

Date : 2026-09-29
Espèce : gouvernante
État : appliquée
Statut : **appliquée** — `params/fournisseurs.yaml`, six champs contrôlés par `controle_depot.py`.

## Le constat vérifié

Les conditions d'utilisation de McMaster-Carr disposent que **« la
redistribution, la création d'œuvres dérivées et toute autre exploitation
commerciale du contenu sont interdites »**.

Trois précisions, parce que chacune compte :

1. Ce n'est pas seulement la redistribution qui est visée : **l'œuvre
   dérivée l'est aussi**. Découper un de leurs modèles pour en tirer une
   pièce tomberait sous la clause telle qu'elle est écrite.
2. L'**exploitation commerciale** est nommément interdite — or YXOR se
   réserve la possibilité d'être commercialisé un jour (fiche 0010).
3. **Je n'ai pas pu lire la page elle-même** : elle n'est pas accessible
   à un client automatique. La citation vient d'une source secondaire
   concordante. La réserve est portée ici, pas dissimulée.

Ce n'est pas un avis juridique — la fiche 0010 §4 l'interdit — c'est le
constat qu'une condition existe et qu'elle est restrictive.

## La règle

> **Aucun fichier fournisseur non redistribuable n'entre dans le dépôt.**
>
> Un fichier fournisseur est tout fichier obtenu d'un catalogue,
> constructeur ou distributeur : modèle CAO, plan, nomenclature, extrait
> de fiche technique.
>
> Chacun, redistribuable ou non, fait l'objet d'une **fiche de
> provenance** dans `params/fournisseurs.yaml`, avec **six champs
> obligatoires** : source, référence, date, empreinte, conditions,
> redistribuable.

## Pourquoi une fiche même pour ce qui ne rentre pas

C'est le point important, et c'est la leçon de la fiche 0020.

Un fichier **absent** et un fichier **interdit** se ressemblent : dans les
deux cas, il n'y a rien dans le dépôt. Sans registre, on ne peut pas
distinguer « personne n'a encore cherché le modèle de ce roulement » de
« ce modèle existe, il est chez McMaster, et nous n'avons pas le droit de
l'y mettre ».

La fiche de provenance rend le second cas **visible**. Elle dit aussi où
retrouver le fichier, ce qui est le seul moyen de vérifier une cote plus
tard sans refaire la recherche.

## L'empreinte, et pourquoi elle n'est pas décorative

Un fournisseur peut modifier un modèle sans changer sa référence. Sans
empreinte, une cote relevée en septembre et une cote relevée en mars
seraient indiscernables — et l'on croirait à une erreur de relevé là où
il y aurait eu changement de produit.

L'empreinte est prise **sur le fichier téléchargé**, même quand celui-ci
n'entre pas dans le dépôt : c'est justement dans ce cas qu'elle est la
seule trace.

## Ce qui est déjà outillé, et ce qui ne l'est pas

**Outillé.** `scripts/controle_depot.py` refuse tout fichier binaire
suivi par Git, quel que soit son répertoire : un `.step` ou un `.pdf`
fournisseur déposé n'importe où **échoue la régénération**. La règle est
donc appliquée pour les formats binaires sans rien ajouter.

**Ajouté.** Le même contrôle vérifie maintenant que chaque entrée de
`params/fournisseurs.yaml` porte ses six champs, et qu'aucune entrée
`redistribuable: false` n'est suivie par Git.

**Non outillé, et je le dis.** Un fichier fournisseur au format texte —
un DXF, un CSV de nomenclature — passerait le contrôle binaire. Seule la
fiche de provenance le signalerait, et elle repose sur la bonne foi de
qui l'écrit.

## Aujourd'hui

`params/fournisseurs.yaml` existe et est **vide**. Aucun fichier
fournisseur n'est entré dans le dépôt à ce jour ; c'est cohérent avec
l'absence de tout binaire (68 fichiers suivis, 0 binaire).

## Source

Conditions d'utilisation de McMaster-Carr, citées par une source
secondaire ; page d'origine non accessible à la lecture automatique.
