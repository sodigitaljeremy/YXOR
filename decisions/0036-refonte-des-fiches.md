# 0036 — Refonte des fiches : espèce, cycle de vie, parcours d'entrée

Date : 2026-09-29
Espèce : proposition
État : proposée
Statut : **proposée** — rien n'est appliqué.

33 fiches en dix jours. Le réflexe est bon, le rythme ne l'est pas : à ce
compte elles cesseront d'être lues, et une fiche non lue ne gouverne rien.

## 1 — L'espèce, déclarée en tête

L'état des lieux a montré que la citation d'une fiche ne mesure rien :
0012 et 0019 ne sont citées par personne et sont pourtant justes et
appliquées. C'est qu'il existe **trois espèces**, et que rien ne les
distingue.

| Espèce | Ce qu'elle est | Faut-il la lire avant d'écrire du code ? |
| --- | --- | --- |
| **gouvernante** | une règle que le code applique | **oui, toujours** |
| **historique** | la trace d'une erreur ou d'un fait établi | non — quand la question revient |
| **close** | appliquée ; le code est devenu la vérité | non — sauf pour le motif |

Proposé : un champ `Espèce :` en tête, à côté de `Statut :`, et une
colonne dans l'index.

**Ce que cela change concrètement** : un nouveau venu filtre sur
« gouvernante » et lit six fiches au lieu de trente-trois.

Répartition telle que je la lis :

- **gouvernantes (7)** — 0004, 0010, 0013, 0018, 0020, 0030, 0033
- **historiques (11)** — 0001, 0003, 0012, 0014, 0016, 0017, 0022, 0028,
  0029, 0031, 0034
- **closes (13)** — 0002, 0005, 0006, 0007, 0008, 0009, 0011, 0015, 0019,
  0023, 0024, 0025, 0026
- **veille (1)** — 0032 · **abandonnée (1)** — 0021

## 2 — DRY : 0021 → 0026 → 0033

Trois fiches pour une décision, parce que j'ai proposé avant de mesurer.

**Ne pas fusionner.** La règle 5 interdit de réécrire, et surtout : le
chemin lui-même est instructif — la 0021 défendait la clé composée avec
un argument que la 0033 a démonté par le calcul. Effacer ce chemin
effacerait la leçon.

**Ranger, ce que la règle 5 n'interdit pas.** Proposé :
`decisions/archive/`, où vont les fiches `abandonnée` et les
`historique` closes depuis plus de trente jours. L'index continue de les
lister, dans une section séparée, avec leur renvoi.

La 0021 y va seule aujourd'hui.

## 3 — YAGNI : aucune fiche à supprimer

J'ai cherché des fiches qui ne gouvernent rien **et** ne tracent aucune
erreur. **Je n'en trouve aucune.** Les moins citées sont toutes des
historiques — c'est leur fonction.

Le seul candidat serait la 0022 (soudure), qui ne décide rien. Mais elle
instruit une question ouverte et porte un calcul corrigé (0031). Elle
reste.

**YAGNI s'applique à l'avenir, pas au passé** : la vraie discipline est
de ne pas écrire la trente-quatrième fiche pour une décision qui tient
en trois lignes de journal.

Critère proposé : **une fiche est justifiée si son absence rendrait une
décision inexplicable dans six mois.** Sinon, journal.

## 4 — KISS : les six fiches qui dépassent 150 lignes

| Fiche | Lignes | Ce qu'elle perdrait à être coupée |
| --- | ---: | --- |
| 0026 | 221 | **rien d'essentiel.** La section DIN 8580 est un cours de vocabulaire qui appartient à un glossaire. −70 lignes. |
| 0024 | 205 | **beaucoup.** C'est un audit : ses tableaux SONT le contenu. À laisser. |
| 0019 | 196 | **rien.** Fiche close ; la moitié décrit une interface qui existe. À archiver plutôt qu'à couper. |
| 0015 | 189 | **peu.** Trois exemples valent pour un. −40 lignes. |
| 0018 | 178 | **rien d'essentiel.** Le tableau des deux étages Docker est dans le Dockerfile, mieux commenté. −40 lignes. |
| 0025 | 158 | **rien.** Close, appliquée. À archiver. |
| 0033 | 156 | **rien.** Son tableau de décision tient en 20 lignes ; le reste le justifie. À garder tant que la migration est fraîche. |

**Constat : quatre des sept sont des fiches CLOSES.** Leur longueur ne
gêne personne une fois rangées. **Le problème de taille se résout par le
rangement, pas par la coupe** — sauf pour 0026, où la digression sur la
DIN mérite un glossaire.

## 5 — CRUD : un cycle de vie explicite

Aujourd'hui les statuts sont écrits à la main et divergent : « acceptée »,
« acceptée le 2026-09-29 », « acceptée le 2026-09-29 — appliquée le jour
même », « veille », « instruction », « abandonnée ».

Proposé, cinq états et **rien d'autre** :

```
proposée  ─┬─> acceptée ──> appliquée ──> amendée ──> archivée
           └─> abandonnée ─────────────────────────> archivée
```

| État | Ce qu'il veut dire |
| --- | --- |
| `proposée` | écrite, pas validée. Rien n'est fait. |
| `acceptée` | validée, pas encore dans le code |
| `appliquée` | le code la porte |
| `amendée` | une autre fiche la corrige ; `Amendée par` obligatoire |
| `abandonnée` | jamais appliquée, remplacée |
| `archivée` | déplacée dans `archive/` |

`veille` et `instruction` deviennent des **espèces**, pas des états — ce
sont des fiches qui ne décident rien, pas des fiches en attente.

**Et il faut l'outiller.** `index_fiches.py` doit refuser un état hors
liste, un `appliquée` sans date, un `amendée` sans `Amendée par`. Sinon
la convention divergera comme elle vient de le faire — c'est la leçon des
lignes `Date:` perdues sur quatre fiches d'affilée.

## 6 — Ce que vous demandez vraiment : le parcours d'entrée

**Six fiches, dans cet ordre.** C'est ce qu'il faut avoir lu avant
d'écrire une ligne.

| # | Fiche | Pourquoi celle-ci, à cette place |
| --- | --- | --- |
| 1 | **0010** — traçabilité de l'origine des cotes | c'est le contrat du projet. Tout le reste en découle : sans elle, `audit_origines` est incompréhensible. |
| 2 | **0013** — nature des cotes | corrige la règle 1 et la restreint à son domaine. Lue seule, la règle 1 fait sous-dimensionner les grandes tailles. |
| 3 | **0020** — trois états de la valeur absente | la distinction `sans_objet` / `à mesurer` / `se déduira` traverse tout le site et toutes les données. |
| 4 | **0026** + **0033** — quatre tables, épaisseur en champ | la structure de `hardware.yaml`. Sans elles, `procedes.py` paraît inutilement compliqué. |
| 5 | **0018** — le site est une projection du dépôt | explique pourquoi rien n'est commité, pourquoi le site ne stocke rien. |
| 6 | **0015** — plaques et entretoises, découpe 2D | le seul choix d'**architecture mécanique**. Tout le reste est méthode ; celle-ci dit ce qu'on construit. |

Deux à lire **le jour où** : **0004** avant de toucher à `sim/`, et
**0023** avant de toucher au navigateur.

Les vingt-cinq autres se lisent quand leur question se pose — et l'index,
avec l'espèce en colonne, doit permettre de la trouver.

## 7 — Ce que je ne propose pas

**Pas de renumérotation, pas de fusion, pas de suppression.** Un numéro
de fiche est cité dans le journal, dans le code, dans `CLAUDE.md` et dans
`params/`. Le mesurer : `0010` apparaît 18 fois, `0026` 16 fois. Renuméroter
casserait ces renvois pour un gain d'esthétique.

## Ordre d'application proposé

1. Champ `Espèce :` sur les 33 fiches, et colonne dans l'index.
2. Les cinq états, et `index_fiches.py` qui **refuse** un état hors liste.
3. Le parcours d'entrée, en tête de `decisions/index.md` **et** dans le
   README.
4. `decisions/archive/`, et la 0021 dedans.
5. La digression DIN de la 0026 vers un glossaire — en dernier, c'est le
   moins utile.

Le point 3 est celui qui sert dès demain. Le point 2 est celui qui évite
que tout recommence.
