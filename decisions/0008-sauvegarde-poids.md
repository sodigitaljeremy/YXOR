# 0008 — Sauvegarde des poids : manifeste versionné, binaires hors Git

Date : 2026-09-28
Statut : acceptée

> **Manquement de procédure signalé.** Cette fiche est écrite *après*
> application, ce que la règle 5 interdit. Le cadre avait été proposé et
> validé lors de l'échange précédent, mais la fiche aurait dû précéder
> l'écriture du script. Consigné plutôt que tu.

## Contexte

La fiche 0003 le notait déjà : les 29,5 Mo de poids ne sont couverts par
aucun versionnement, viennent d'un Google Drive tiers, et ne sont
« ni récupérables par l'amont ni par YXOR » s'il disparaît. Une
sauvegarde y était annoncée « à prévoir ». Elle ne l'avait pas été.

La règle 4 interdit le binaire dans Git. Le problème est donc de
sauvegarder 29,5 Mo d'archives **sans** les versionner.

## Options examinées

| Option | Écartée pour |
| --- | --- |
| Git LFS | Reste du binaire attaché au dépôt : contourne la règle 4 sans la respecter |
| Manifeste seul, retéléchargement depuis Drive | Ne protège de rien : c'est justement la disparition du Drive qu'on craint |
| Release GitHub publique | **La licence des poids n'est pas explicitée par l'amont** (fiche 0003). Les republier serait imprudent |
| Manifeste dans Git + archives hors Git | Retenue |

## Décision

### 1. Partage strict

| Où | Quoi |
| --- | --- |
| **Dans Git** | `params/ckpts.manifest.yaml` — noms, identifiants Drive, empreintes SHA-256, tailles. Du texte, diffable |
| **Hors Git** | les archives, sur **deux destinations privées distinctes** |

Le manifeste **ne restaure rien**. Il permet de *détecter* qu'une archive
a changé ou s'est corrompue. Les deux moitiés sont nécessaires, et il
faut le dire : un manifeste seul donne une illusion de sauvegarde.

### 2. Pourquoi l'empreinte et pas l'identifiant

Un identifiant Google Drive **survit au remplacement de son contenu**.
Seule l'empreinte SHA-256 prouve qu'il s'agit bien des mêmes poids. Le
manifeste porte les deux, et le script le rappelle en commentaire.

### 3. Pas de Release GitHub

Même en pièce jointe de release, publier ces poids les redistribue. Tant
que la licence n'est pas éclaircie (conséquence ouverte de la fiche
0003), c'est écarté. Ce n'est pas un choix technique.

### 4. Outil

`scripts/ckpts_backup.py`, venv du projet, trois sous-commandes :
`manifest` (régénère), `verify` (compare les empreintes), `archive`
(produit le `.tar.gz` à copier, manifeste inclus dedans).

## Conséquences

- **La seconde destination reste à la charge de Jeremy.** Aucun accès
  SSH n'est configuré sur cette machine (`~/.ssh` vide) : je ne peux pas
  déposer sur le VPS Hetzner. La première destination, locale, est faite.
  **Tant que la seconde n'existe pas, il n'y a qu'une copie**, et la
  sauvegarde n'en est pas vraiment une.
- `verify` est à relancer avant toute mesure qui s'appuie sur les poids.
  Une empreinte qui diverge invalide les mesures associées (fiche 0003).
- Le manifeste est du texte : la règle 4 est respectée sans exception,
  contrairement à la fiche 0006 qui en avait besoin d'une.
