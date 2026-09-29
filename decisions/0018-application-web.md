# 0018 — Application web : un site statique engendré par le dépôt

Date : 2026-09-28
Espèce : gouvernante
État : acceptée
Statut : **acceptée** — validée le 2026-09-28, mise en œuvre le jour même.
Seule la ligne de statut est modifiée ; le raisonnement n'est pas réécrit (règle 5).

## Contexte

Il faut une application web qui montre ce que la chaîne produit et serve
de point de livraison des fichiers, déployée sur le VPS Hetzner via
Coolify.

Deux contraintes s'opposent frontalement, et c'est le cœur du problème :

- **La règle 4** interdit tout binaire dans Git. `exports/` est ignoré.
- **L'application a besoin de ces fichiers** — DXF, STEP, STL, plan A4.

## 1 — Architecture proposée : la sortie est statique, le « backend » est
un générateur

### Le constat qui commande tout

L'application **ne crée aucune donnée**. Elle projette un dépôt. Or un
dépôt à un commit donné est **immuable**. Rien dans le besoin exprimé —
lister, afficher, tracer, télécharger — ne dépend de la requête :

| Fonction | Dépend de la requête ? |
| --- | --- |
| lister les pièces | non |
| géométrie 3D | non — le navigateur charge un STL |
| origine des cotes | non |
| téléchargements | non |
| vue atelier | non |

**Aucune fonction ne justifie un serveur qui calcule.** Un serveur
d'application serait un deuxième état, qu'il faudrait synchroniser avec
le dépôt — c'est-à-dire exactement la divergence que l'énoncé interdit.

### Ce que je propose

> **Le « backend » existe, mais il s'exécute à la construction, pas à la
> requête.** C'est un *générateur* : il lit le dépôt et produit un site
> statique. Ce qui est déployé n'expose aucun code.

```
  dépôt Git            générateur                    site statique
  ─────────            ──────────                    ─────────────
  parts/*.py     ──►   exécute chaque pièce     ──►  fichiers/*.stl .dxf .step .pdf
  parts/*.origines     lit les relevés          ──►  data/pieces.json
  params/*.yaml        lit les paramètres       ──►  data/origines.json
  scripts/audit        rejoue l'audit           ──►  data/audit.json
                                                ──►  index.html, piece/…, atelier/…
```

**Pourquoi c'est le bon choix ici :**

1. **La divergence devient impossible.** Le site n'est pas une copie du
   dépôt, c'en est une **projection** à un commit. Il ne peut pas
   dériver, parce qu'il ne survit pas à une reconstruction.
2. **Rien à maintenir en production** : pas d'interpréteur, pas de
   dépendance applicative, pas de surface d'attaque, pas de processus à
   surveiller.
3. **Aucun calcul serveur.** La 3D est rendue par le navigateur. Le VPS
   sert des octets. La contrainte « pas de GPU, pas de rendu lourd » est
   satisfaite par construction, et non par optimisation.
4. **`CLAUDE.md` l'autorise explicitement** : « VPS Hetzner :
   régénération et publication seulement, pas de calcul ». Construire le
   site **est** de la régénération et de la publication.

**Ce qu'on abandonne, et il faut le dire :**

- Pas de recherche ni de filtre au-delà de ce qui est engendré. Sans
  objet à cette échelle, gênant à des centaines de pièces.
- **Toute modification impose une reconstruction et un redéploiement**,
  y compris pour corriger une faute de frappe.
- Pas d'historique des artefacts : obtenir le DXF d'un commit passé
  suppose de reconstruire à ce commit. C'est cohérent avec le reste du
  projet — le dépôt à un commit est la vérité — mais c'est une contrainte.

## 2 — La question des fichiers, et le coût de la solution

### La solution

> **Les artefacts sont construits *dans l'image de déploiement*, et ne
> sont jamais commités.**

Construction Docker en **deux étages** :

| Étage | Contenu | Sort dans l'image finale ? |
| --- | --- | --- |
| **1 — constructeur** | Python 3.14, `build123d`, `ezdxf`, `PyYAML`, le dépôt ; exécute la régénération | **non** |
| **2 — service** | serveur statique + le seul dossier `site/` | oui |

La règle 4 est respectée **à la lettre et dans son intention** : rien de
binaire n'entre dans Git, et tout se régénère. L'image finale ne contient
ni Python, ni `build123d`, ni code source.

### Ce que ça coûte — quatre postes, énoncés franchement

1. **Poids de construction.** L'étage constructeur installe `build123d`
   et son noyau OCCT : de l'ordre de **700 Mo à 1 Go** — le venv du
   projet en fait 972 — pour produire un site de **quelques centaines de
   kilo-octets**. Ce poids est jeté, mais il est téléchargé et
   décompressé à chaque construction sans cache.
2. **La construction devient une dépendance du déploiement.** Si un
   script de pièce casse, **le site ne peut plus être mis à jour**, même
   pour une correction de texte. C'est un couplage réel. Il est atténué
   par l'épinglage strict de la fiche 0009 — et c'est précisément là que
   cet épinglage se rentabilise.
3. **Le VPS doit pouvoir construire.** Compiler l'image avec OCP demande
   de la mémoire et du disque. **À vérifier sur votre Hetzner avant de
   s'engager** : un petit modèle peut manquer de mémoire. Repli si
   nécessaire, décrit au §4.
4. **Pas d'artefact sans reconstruction.** Déjà dit plus haut ; c'est le
   même coût vu de l'autre côté.

### Les deux solutions écartées

| Écartée | Motif |
| --- | --- |
| Commiter les artefacts | Viole la règle 4. C'est la solution facile et c'est celle qu'il ne faut pas prendre |
| Stockage objet externe (S3, MinIO) | Ajoute un service, une authentification, **et un second état** qui peut diverger du dépôt |

## 3 — Ce qui est déployé sur Coolify, exactement

- **Un seul service**, de type `Dockerfile`, pointant sur ce dépôt et sa
  branche `main`.
- **Un `Dockerfile` à deux étages**, à la racine.
- **Aucune variable d'environnement, aucun secret, aucun volume, aucune
  base de données.** L'application n'a pas d'état.
- **Un port HTTP** servi par un serveur statique. Coolify se charge du
  certificat et du domaine.
- **Redéploiement sur `git push`**, si vous activez le déclencheur.

**Repli si le VPS ne peut pas construire** : déporter la construction
dans une action GitHub, publier l'image dans un registre, et faire tirer
l'image par Coolify. Cela ajoute une infrastructure — je ne le propose
pas d'emblée, seulement si la construction sur place échoue.

## 4 — Le contenu du site

| Page | Destinataire | Contenu |
| --- | --- | --- |
| `/` | vous | liste des pièces, état de l'audit d'origine |
| `/piece/<nom>/` | vous | 3D manipulable, hors-tout, **toutes les cotes avec origine et source**, les quatre téléchargements |
| `/atelier/<nom>/` | votre cousin | une page, sans jargon, lisible sur téléphone : matériau, épaisseur, rayon intérieur minimal, DXF |
| `/tracabilite/` | vous | l'audit rendu visible : répartition par origine et par nature |

### La vue atelier, et une exigence que je pose

Les valeurs `saignee`, `voile_min` et la machine de découpe métal sont
aujourd'hui à `null` dans `hardware.yaml`. **La page atelier affichera
« non déterminé » en clair, jamais une case vide.** Une case vide se lit
comme « sans objet » ; « non déterminé » se lit comme « à mesurer ». La
confusion entre les deux est exactement ce qui produit une pièce fausse.

### La 3D dans le navigateur

STL chargé par `three.js`, rotation à la souris et au doigt. **Version
épinglée et vérifiée par empreinte SHA-256**, récupérée à la
construction — même méthode que les poids de la fiche 0008. Pas de CDN :
le site doit se reconstruire à l'identique dans dix ans.

## 5 — La commande unique

> `.venv/bin/python scripts/regenerer.py`

Efface `exports/` et `site/`, réexécute chaque pièce, relit les relevés
d'origine, rejoue l'audit, et reconstruit le site. Le `Dockerfile`
n'appelle que cette commande : ce qui tourne en production est **ce que
vous pouvez lancer chez vous**.

## Conséquences

- Le site ne peut pas contredire le dépôt : il en est une projection.
- L'épinglage de la fiche 0009 devient une **dépendance de production**.
- Une seule pièce existe aujourd'hui. Le site en affichera une.
