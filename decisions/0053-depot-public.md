# 0053 — Le dépôt passe public

Date : 2026-09-30
Espèce : gouvernante
État : acceptée
Statut : **acceptée** — décidée par Jeremy le 2026-09-30. **Non appliquée** : c'est Jeremy qui change la visibilité, pas l'assistant. Le contrôle préalable est `docs/controle-publication-2026-09-30.md`.

## La décision

Le dépôt GitHub de YXOR, privé jusqu'ici, **devient public**.

## Les motifs, tels que Jeremy les a donnés

1. **Peu de visibilité attendue.** Un dépôt de projet personnel,
   rédigé en français, attire peu de lecteurs.
2. **La visibilité est réversible.** Un dépôt public peut repasser en
   privé.

## La limite du second motif

**Ce qui revient au privé, c'est l'accès au dépôt, pas le contenu.**
Tout ce qui a été public, même un court instant, peut avoir été copié :

- les clones et les forks faits pendant ce temps restent chez leurs
  auteurs ;
- les archives et les caches (Software Heritage, moteurs de recherche,
  miroirs) gardent ce qu'ils ont récupéré ;
- **c'est l'historique entier qui est publié**, pas seulement l'état
  courant : chaque commit, chaque fichier supprimé depuis.

La réversibilité protège donc de **l'exposition future**, jamais de
l'exposition passée. Un secret publié, même une minute, se révoque. Le
rendre privé ne suffit pas.

## Ce que le contrôle préalable a établi

Le détail est dans `docs/controle-publication-2026-09-30.md`.

- **Aucun secret** dans l'historique : 132 commits balayés à la main, car
  gitleaks n'est pas installé.
- **Aucune licence** dans le dépôt : il n'y a pas de fichier `LICENSE`.
  Sans licence, un dépôt public est lisible, mais rien n'y est accordé
  d'autre que ce que permettent les conditions de GitHub. Ce constat
  n'est pas un avis juridique (fiche 0010 § 4). **Le choix de licence
  reste ouvert** : le contrôle propose, Jeremy choisit.
- Le dépôt contient **des valeurs extraites de ToddlerBot**, dont la
  conception est sous CC BY-NC-SA 4.0. La question de la fiche 0010 § 4
  devient pratique : ces valeurs sont-elles couvertes ? Elle **reste
  sans avis**. En attendant, le README porte une mention de provenance
  provisoire.

## Ce qu'elle ne décide pas

- La licence du code, celle de la conception propre et celle de la
  documentation.
- Le sort des binaires qui restent dans l'historique (commit `c078b8e`,
  dossier `site/`). Ce sont des fichiers de Jeremy, sans secret.
- Toute réécriture de l'historique : aucune n'est nécessaire à ce jour.

## Écart avec l'arbitrage du 30-09

`docs/arbitrage-2026-09-30.md` (D5) recommandait de **rester privé** tant
que la question de licence n'était pas instruite. **Jeremy a décidé
autrement.** C'est son choix, et il est consigné ici avec ses motifs.
