# 0024 — Audit du dépôt et plan de refactorisation

Date : 2026-09-29
Statut : **proposée** — aucun code n'est touché.

Audit demandé par Jeremy. Tous les nombres ci-dessous sont mesurés, pas
estimés ; les commandes qui les produisent sont au journal du jour.

## 1 — Ce qui a grossi

| Fichier | Lignes | Poids |
| --- | ---: | ---: |
| `journal/2026-09-28.md` | **2 845** | 128 ko |
| `journal/2026-09-20.md` | 865 | 44 ko |
| `scripts/regenerer.py` | **822** | 40 ko |
| `params/joints.yaml` | 593 | 24 ko |
| `parts/semelle_apprentissage.py` | 425 | 24 ko |

Totaux : 3 779 lignes de Python, 489 de JavaScript, 194 de CSS,
1 932 de YAML, **6 901 de Markdown**. Le projet est aux **deux tiers de
la prose**.

### `regenerer.py` fait-il trop de choses ? Oui, et voici la répartition

| Responsabilité | Lignes | Part |
| --- | ---: | ---: |
| rendu HTML — pages | 297 | 36 % |
| rendu HTML — blocs et gabarits | 131 | 16 % |
| orchestration (`main`) | 107 | 13 % |
| constantes, imports, docstring | 159 | 19 % |
| contrôle qualité HTML | 35 | 4 % |
| logique métier (dessinable/coupable, rangs) | 38 | 5 % |
| exécution des pièces, lecture des relevés | 42 | 5 % |
| lancement de l'audit | 14 | 2 % |

**52 % du fichier est du gabarit HTML.** Ce n'est pas « trop de choses »
au sens d'un mélange de couches : c'est **un moteur de gabarits écrit en
f-strings**. Le vrai défaut n'est pas la taille, c'est que le HTML et la
logique partagent le même fichier, donc la même relecture.

Le journal du 2026-09-28, lui, est un fichier de 2 845 lignes pour **une
seule journée**. Il n'est plus lisible par personne, moi compris.

## 2 — Ce qui est dupliqué

`profil.py` / `simulateur.js` est connu **et gardé** (fiche 0023).
Les autres ne le sont pas :

| Duplication | Où | Gardée ? |
| --- | --- | --- |
| **placement des cotes du schéma** — ~20 constantes de mise en page | `plan_decoupe.svg_schema` / `simulateur.dessiner` | **NON** |
| **7 repères d'annotation** : `COS45`, `REP_CONGE_X/Y`, `REP_RINT_X/DX/DY/MARGE` | déclarés dans `parts/semelle_apprentissage.py`, **recopiés en dur** dans `simulateur.js` | **NON** |
| `diagnostic()` — les six conditions d'impossibilité | `profil.py` / `simulateur.js` | **partiellement** : l'auto-contrôle ne teste qu'un jeu de paramètres valide, donc un seuil faux passerait |
| formatage des nombres | `plan_decoupe._fmt` / `simulateur.fmt` | non |
| échappement HTML | `regenerer.e` / `simulateur.echappe` | non |

**Le plus dangereux est le deuxième.** Changez `REP_CONGE_X` dans la
pièce : le schéma engendré déplace son repère, le schéma simulé ne bouge
pas. Rien ne le dit. C'est le trou exact que la fiche 0023 prétend avoir
bouché — elle ne l'a bouché que pour le **contour**, pas pour les
**annotations**.

## 3 — Ce qui est mort

**Code Python : rien.** Les huit candidats trouvés par analyse statique
sont tous des faux positifs (fonctions passées en valeur, classes
instanciées, commandes dispatchées par `argparse`). 101 définitions,
0 morte.

**JavaScript : un bloc.** `ecart()` et `distSeg()` dans `simulateur.js`,
~16 lignes — résidus de mon propre changement d'hier, quand la
comparaison de Hausdorff a été remplacée par une comparaison point à
point. Livrés morts.

**Liens : 4 morts sur 6.** `README.md` renvoie vers
`docs/00-cadrage.md`, `docs/01-cahier-des-charges.md`,
`docs/02-plan-action.md` et `docs/03-artefacts.md`. **Aucun des quatre
n'existe.** `docs/` contient `glossaire.md` et `lecture-modele.md`, non
liés, et n'a pas bougé depuis le 2026-09-20.

**Une règle sans référent.** CLAUDE.md interdit de « proposer d'acheter
du matériel **avant la phase 6 du plan d'action** ». Le plan d'action
n'existe pas. La règle est donc **inapplicable et invérifiable** : ni
vous ni moi ne pouvons savoir si nous y sommes.

**README obsolète.** Il annonce `robot/`, `bom/`, `docs/` et ignore
`scripts/` (10 fichiers), `web/` (3) et tout le site. Il annonce
« Phase 0 — socle ».

## 4 — Ce qui n'est pas outillé

C'est la section qui compte. 24 règles recensées dans CLAUDE.md et les
fiches :

| | Nombre |
| --- | ---: |
| **Outillées** (un contrôle échoue si la règle est violée) | **9** |
| Partielles | 3 |
| **Non outillées** | **12** |

**37 % des règles du projet sont réellement vérifiées.**

Outillées : cote en dur, origine, nature, `site/`, `exports/`, balises
HTML, contour JS/CAO, interpréteur amont, DXF en millimètres.

**Non outillées, par ordre de coût d'un manquement :**

1. **Rien de binaire dans Git**, ailleurs que `exports/` et `site/`.
   Un `.step` déposé dans `parts/` entrerait sans un mot. C'est
   littéralement la faute du 2026-09-28, à un répertoire près.
2. **Schéma JS == schéma Python** (voir §2).
3. **Une décision = une fiche AVANT application.** Invérifiable en
   l'état, et enfreinte deux fois cette semaine — dont par moi hier.
4. **Aucun angle vif rentrant** : jamais contrôlé sur le DXF produit,
   alors que c'est la raison d'être de la forme de la semelle.
5. **Quincaillerie ne suit jamais H** (règle 2) : aucun contrôle.
6. **Noms d'articulations identiques partout** (règle 3) : aucun.
7. `rayon_interieur_min == 0,5 x epaisseur` : vérifié pour le seul
   procédé employé par la pièce, pas pour la table entière.
8. **Règle de nullité déclarée mais qui ne correspond à rien** : une
   règle morte de `nullites.yaml` passerait inaperçue.
9. Champ `version` obligatoire (fiche 0007), dépendances GPL, pièce
   plate, démontable, conception au plus contraignant : aucun.

## 5 — Ce qu'un nouveau venu ne comprendrait pas

1. **Quelle commande lancer.** Le README n'en cite aucune. Les vraies
   sont `scripts/regenerer.py` et `scripts/audit_origines.py --strict` ;
   elles n'apparaissent que dans le journal et le pied de page du site.
2. **Les quatre documents fondateurs n'existent pas** (§3), et le README
   y renvoie. Un lecteur conclut que le dépôt est cassé.
3. **Pourquoi deux venvs**, expliqué dans CLAUDE.md, mais rien ne dit
   lequel lancer devant un fichier donné, sauf à connaître la règle
   `sim/upstream/`.
4. **Le mot « procédé »** désigne un couple machine-matériau (`cutter_carton`).
   Rien ne le dit hors du commentaire en tête de `hardware.yaml` — et la
   fiche 0021 propose justement de le défaire.
5. **Pourquoi le même contour est calculé deux fois.** Sans la fiche
   0023, `profil.py` ressemble à une réimplémentation gratuite de la
   pièce.
6. **Le journal.** 2 845 lignes pour une journée. On ne sait pas par où
   entrer, et rien ne relie une entrée à la fiche qu'elle applique.

## 6 — Les fiches

**23 fiches, toutes avec un `Statut`.** Mais :

- **les quatre dernières (0020 à 0023) n'ont plus de ligne `Date:`** —
  convention respectée 19 fois, abandonnée par moi sur les quatre
  dernières ;
- **aucun index.** 23 fiches, 7 renvois d'amendement croisés, et rien qui
  donne la carte ;
- **un titre ment.** La fiche 0016 s'intitule « L'architecture en plaques
  n'a aucun précédent open source ». C'est **faux**, et la fiche le dit
  elle-même en ligne 6 (amendée par 0017). Mais qui parcourt les titres
  lit l'inverse de la vérité.

**Pas de contradiction de fond** entre fiches : les sept amendements sont
tous déclarés en tête, et la règle « on n'écrit pas par-dessus » a tenu.
La faiblesse est la **navigabilité**, pas la cohérence.

Une tension ouverte, non contradictoire : la fiche 0015 pose qu'une pièce
plate ne fait pas un volume ; la 0022 instruit ce que la soudure lèverait.
La 0022 ne tranche pas — c'est régulier.

## 7 — Plan de refactorisation, par rapport bénéfice/risque

### Rang 1 — bénéfice fort, risque quasi nul

| # | Action | Pourquoi d'abord |
| --- | --- | --- |
| 1 | **Garder le schéma comme on garde le contour** : la pièce publie déjà ses `trace` ; que le simulateur les **lise** au lieu de recopier sept constantes, et que l'auto-contrôle compare les traces calculées à celles du dépôt | supprime la duplication la plus dangereuse **et** la rend impossible à réintroduire |
| 2 | **Contrôle « rien de binaire dans Git »** dans `regenerer.py` : refuser tout fichier suivi dont l'extension est binaire hors `exports/`/`site/` | 15 lignes ; c'est la faute qui s'est produite |
| 3 | **Supprimer `ecart`/`distSeg`** de `simulateur.js` | code mort livré |
| 4 | **Réparer le README** : commandes réelles, arborescence réelle, retirer les 4 liens morts | premier fichier que tout le monde lit |
| 5 | **Trancher la « phase 6 »** : écrire le plan d'action, ou retirer la règle de CLAUDE.md | une règle invérifiable ne tient pas |
| 6 | **Index des fiches** (`decisions/index.md`), engendré depuis les en-têtes, avec statut et amendements | 30 lignes, et la 0016 cesse de mentir |
| 7 | **Rétablir `Date:`** sur les fiches 0020-0023 | ma propre dérive |

### Rang 2 — bénéfice fort, risque modéré

| # | Action | Risque |
| --- | --- | --- |
| 8 | **Sortir les gabarits de `regenerer.py`** vers `scripts/pages/` — 428 lignes déplacées, aucune logique changée | large diff, aucune sémantique touchée ; `controler_html` couvre le résultat |
| 9 | **Contrôler `rayon_interieur_min == 0,5 x epaisseur`** sur toute la table, pas le seul procédé employé | peut faire échouer la régénération sur une donnée existante — c'est le but |
| 10 | **Détecter les règles mortes** de `nullites.yaml` et `origines.yaml` | idem |
| 11 | **Découper le journal par entrée** plutôt qu'un fichier par jour | 2 845 lignes à scinder ; risque de perdre un passage |

### Rang 3 — à instruire, pas à faire tout de suite

| # | Action | Pourquoi attendre |
| --- | --- | --- |
| 12 | Contrôle « aucun angle vif rentrant » sur le DXF | demande une analyse de courbure : plusieurs heures, et un seul type de pièce existe |
| 13 | Contrôle « quincaillerie ne suit pas H » | suppose de faire varier H et de rejouer l'audit : coûteux, et la fiche 0021 va bouger ces tables |
| 14 | Unifier `_fmt`/`fmt`, `e`/`echappe` | gain réel mais faible ; à faire **avec** l'action 1, pas avant |

### Ce que je ne recommande pas

**Ne pas découper `regenerer.py` en cinq modules.** Le fichier est gros
mais sa structure est linéaire et son seul point d'entrée est `main`. Le
découper en modules à une seule fonction déplacerait la complexité dans
les imports. Sortir **les gabarits** suffit : c'est 52 % du volume et
c'est la partie qu'on relit le moins.
