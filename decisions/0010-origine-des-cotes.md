# 0010 — Traçabilité de l'origine des cotes

Date : 2026-09-28
Statut : acceptée

## Contexte

Une exploitation commerciale de YXOR est un objectif possible. Or la
mécanique ToddlerBot est publiée sous **CC BY-NC-SA** — non commerciale
(fiche 0001). Il faut donc pouvoir répondre, à tout moment et sans
enquête : **quelles cotes de YXOR proviennent de ToddlerBot ?**

Retracer après coup ne se fait pas. La convention est donc posée avant
la première pièce.

> **Cette fiche ne tranche aucune question juridique.** Elle produit la
> traçabilité, pas l'avis. Savoir si une cote d'origine `amont` crée une
> obligation de licence n'est pas de son ressort.

## Décision

### 1. Quatre origines

Toute cote du projet porte l'une de ces valeurs :

| Origine | Définition | Risque de licence amont |
| --- | --- | --- |
| `propre` | dérivée de `H` et d'un ratio de `anthropometry.yaml` | voir §4 |
| `catalogue` | issue d'une fiche technique constructeur — **référence obligatoire** | non |
| `amont` | issue du modèle ou de la documentation ToddlerBot | **oui** |
| `mesure` | relevée sur un objet physique — **instrument et date obligatoires** | non |

### 2. Deux valeurs de service

| Valeur | Usage |
| --- | --- |
| `ambigu` | le cas ne se range dans aucune origine, ou l'attribution est contestable. **À préférer systématiquement à un choix par défaut.** |
| `non_qualifie` | aucune déclaration n'existe. C'est un **défaut**, que l'audit signale. |

### 3. Deux lacunes de la taxonomie, signalées et non tranchées

L'application à l'existant en révèle deux. Elles sont posées ici sans
être résolues, parce que le choix revient à Jeremy.

**a) La littérature scientifique.** Les ratios de
`anthropometry.yaml` viennent de Drillis & Contini, standard de
biomécanique publié. Ce n'est ni une fiche constructeur (`catalogue`),
ni ToddlerBot (`amont`), ni un relevé (`mesure`), ni une dérivation de
`H` (`propre` — ce *sont* les ratios). Proposition : une cinquième
valeur `litterature`, exigeant la citation complète. En attendant, ces
cotes sont marquées `ambigu`.

**b) Les normes.** Une vis M3 fait 3,0 mm parce que l'ISO le dit, pas
parce qu'un constructeur l'a décidé. Même remarque pour les
désignations de roulements. Proposition : élargir `catalogue` à « source
externe documentée, constructeur **ou** norme », ou ajouter `norme`. En
attendant : `ambigu`.

Dans les deux cas le point important pour la question commerciale est
acquis : **ce n'est pas `amont`**. Seule l'étiquette exacte reste à
fixer.

### 4. Le point qui demandera un arbitrage

`H = 0,56 m` est la **taille publiée de ToddlerBot** (fiche 0001,
ligne 24 : « ToddlerBot (Stanford). 0,56 m… », puis ligne 36 : « le
palier P1 est fixé à H = 0,56 m par cette décision »).

Donc `H` est d'origine **`amont`** — et `H` est la racine de toute la
chaîne `propre`. Chaque cote dite « propre » du palier P1 est une
fraction d'un nombre venu de ToddlerBot.

Ce que cela implique juridiquement — si tant est qu'une taille hors-tout
relève de la licence des fichiers mécaniques — **n'est pas tranché
ici**. Le fait est consigné, visible, et daté. C'est tout ce que cette
fiche doit produire.

Conséquence pratique, en revanche, sans portée juridique : **changer
`H` en P2 ou P3 rompt cette filiation**, puisque les paliers 0,90 m et
1,70 m ne viennent pas de ToddlerBot.

### 5. La règle pour le code des pièces

Le principe retenu : **l'origine est portée par l'accesseur, jamais
annotée ligne à ligne.** Une cote est tracée parce qu'elle est allée la
chercher là où elle est, pas parce que quelqu'un a pensé à la commenter.

```python
from yxor.cotes import Cotes
C = Cotes()                       # charge params/*.yaml

l_cuisse = C.propre("ratios.cuisse")          # origine: propre
d_insert = C.catalogue("vis.M3.insert_diametre")   # origine: catalogue
butee    = C.amont("jambes.knee.min")         # origine: amont
ep_tole  = C.mesure(2.87, instrument="pied à coulisse",
                    objet="tôle alu lot A", date="2026-09-28")
```

Quatre propriétés en découlent :

1. **Un mot par cote**, et c'est le mot qu'il fallait écrire de toute
   façon pour aller chercher la valeur. Rien de fastidieux à ajouter.
2. **L'accesseur refuse la mauvaise origine.** `C.propre("vis.M3.diametre")`
   lève une erreur : cette clé est déclarée `catalogue`. On ne peut pas
   blanchir une cote amont en la demandant comme propre.
3. **`mesure` est la seule à exiger une déclaration en ligne**, parce
   qu'elle n'a pas de fichier source. Instrument, objet et date sont
   obligatoires.
4. **Un littéral numérique nu dans le code d'une pièce est un défaut
   double** : il viole la règle 1 et il est intraçable. L'audit le
   signale comme `non_qualifie`.

Chaque pièce dépose un relevé `parts/<nom>.origines.yaml` listant les
cotes employées et leur origine. C'est ce relevé qui rend l'audit de
`parts/` possible sans relire le code.

> Le module `yxor/cotes.py` n'est **pas** écrit par cette fiche. Elle en
> fixe le contrat ; l'implémentation viendra avec la première pièce.

### 6. Où vit la déclaration

`params/origines.yaml`, versionné. Il associe des motifs de chemins de
clés à une origine. Les fichiers de données restent lisibles, et toute
clé non couverte ressort en `non_qualifie` : la dérive est détectée au
lieu d'être silencieuse.

## Conséquences

- `scripts/audit_origines.py` répond à la question posée et doit tourner
  avant toute publication ou tout jalon commercial.
- Une cote `catalogue` sans référence, ou `mesure` sans date, est un
  défaut au même titre qu'une cote non qualifiée.
- La liste des cotes `amont` est un **inventaire**, pas un verdict. Son
  usage juridique appartient à Jeremy et à son conseil.
