# YXOR

Robot humanoïde bipède autonome à IA embarquée locale.

> **À lire en premier : ce fichier (où en est le robot), puis
> [les décisions actives](docs/decisions.md) (ce qui est décidé, par
> qui).** La vision et la méthode sont dans [le cadrage](docs/cadrage.md).

## Où en est le robot — 2026-10-01

Le robot n'est pas dessiné à une taille choisie d'avance : **chaque
classe d'actionneur fixe la taille qu'elle porte** (`scripts/dimensionnement.py`,
marge 1,5). Quatre tailles :

| Taille | H | Actionneur de jambe | Statut |
| --- | --- | --- | --- |
| **S** | **0,60 m** (repli 0,55 m) | **RobStride RS00**, sur les 12 articulations | **décidé** (fiche 0065), premier robot |
| M | ~0,80 m | RS02 ou équivalent | ordre de grandeur |
| L | ~0,90 m | RS06, ou mixte RS06/RS02 | ordre de grandeur |
| XL | ≥ 1,0 m | RS03 et au-delà | hors programme |

Les hauteurs sont dans `params/anthropometry.yaml`.

**S, la v1 : 12 degrés de liberté**, 6 par jambe, sans bras. Un degré de
liberté est une articulation motorisée.

- **Masse calculée : 7,8 kg à 0,60 m**, dont 1,2 kg de charge utile.
  La charge utile (calculateur, batterie, IMU) est une hypothèse de
  travail.
- **Toutes les exigences techniques passent à 0,60 m** : couple continu,
  couple de pointe, vitesse, charge utile, relevé depuis l'accroupi,
  télémétrie, protection thermique, chien de garde, bus et protocole
  communs à la gamme. La grille complète et ses hypothèses sont dans
  [`docs/choix-actionneurs.md`](docs/choix-actionneurs.md).
- **Restent ouverts** : la composition du banc, qui vérifiera le RS00 ;
  la version exacte du RS00 (deux sont publiées) ; les composants réels
  de la charge utile.

**Fabriqué à ce jour** : une pièce d'apprentissage, la semelle. Ni
assemblage ni nomenclature.

**Prochaine étape** (PROPOSÉE par Claude Code, non décidée) :

- finir la refonte du dépôt : R6, protocole du banc ; R7, vérification
  finale ;
- puis la couche logicielle d'articulation et son backend MuJoCo, sans
  aucun achat ;
- puis la première pièce de jambe à H_S, et le banc de vérification du
  RS00, dont la composition et l'achat se décident selon la fiche 0066.

## Provenance et licences — *provisoire*

⚠ **Aucune licence pour l'instant.** C'est un choix délibéré de Jeremy,
le 2026-09-30 (fiche 0063), à rouvrir. Il n'y a pas de fichier `LICENSE`,
donc aucun droit n'est accordé au-delà des conditions de GitHub. Les
options étudiées sont dans `archive/docs/controle-publication-2026-09-30.md`
§ 3.

**Base de départ et référence de calcul :
[ToddlerBot](https://github.com/hshi74/toddlerbot)** (Stanford, 0,56 m).
Son code est sous MIT ; sa conception (les fichiers mécaniques) est sous
**CC BY-NC-SA 4.0**.

**Valeurs extraites de ToddlerBot.** Les fichiers ci-dessous contiennent
des valeurs numériques extraites de ToddlerBot : axes, butées, rapports de
transmission, masses, hauteur, noms d'articulations, empreintes des poids.

- `params/upstream_joints.generated.yaml` (extrait engendré) ;
- `params/joints.yaml` ;
- `params/ckpts.manifest.yaml` ;
- dans `params/actionneurs.yaml` et `params/anthropometry.yaml`, les
  seules entrées d'origine `amont`.

`scripts/provenance_amont.py` les compte.

Ces valeurs viennent de **ToddlerBot**, de Haochen Shi, Weizhuo Wang,
Shuran Song et C. Karen Liu (Stanford) :
<https://github.com/hshi74/toddlerbot>, commit `e337f3b`, article
arXiv:2502.00893. La conception de ToddlerBot est publiée sous
**[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)**,
son code sous MIT (© 2023 Haochen Shi). Par prudence, **ces fichiers sont
à traiter sous CC BY-NC-SA 4.0**, avec cette attribution. Les valeurs ont
été modifiées : réconciliées, renommées, qualifiées (fiches 0005 à 0007).

Savoir si des valeurs numériques isolées sont couvertes par cette licence
est une **question ouverte, sans avis** (fiche 0010 § 4). La mention
ci-dessus ne la tranche pas. **Aucune géométrie ToddlerBot n'entre dans
une pièce YXOR** (fiches 0055 et 0061).

**Autres fichiers tiers.** `sim/models/humanoid.xml` est le modèle
d'exemple de MuJoCo, © 2021 DeepMind Technologies Limited, sous
Apache-2.0. Son en-tête de licence est conservé.

## Principe

Aucun fichier binaire ne fait autorité. Toute géométrie se régénère depuis
le texte source. Le dépôt contient le **code des pièces**, jamais les
pièces.

Les contrôles qui protègent le robot ont chacun une commande qui échoue
quand la règle est enfreinte. La liste est dans `CLAUDE.md`, « Les
contrôles ».

## Commandes

```sh
.venv/bin/python scripts/regenerer.py          # tout : pièces, site, contrôles
.venv/bin/python -m unittest discover -s tests -v    # tests, à chaque clôture
.venv/bin/python scripts/choix_actionneurs.py --ecrire   # grille de S
.venv/bin/python scripts/dimensionnement.py    # taille portée par chaque classe
.venv/bin/python scripts/empreinte.py          # à comparer au pied de page du site
```

`regenerer.py` est la seule commande à connaître :

- il exécute les pièces ;
- il vérifie le dépôt, la provenance amont, les noms d'articulations et
  le rayon minimal ;
- il engendre le site et contrôle sa structure HTML ;
- il **sort en erreur** si l'un des contrôles échoue.

⚠ Toujours `.venv/bin/python`, jamais `python`. Voir « Deux interpréteurs »
dans `CLAUDE.md` : `sim/upstream/` est le seul répertoire qui s'exécute
avec l'autre environnement, et il refuse de démarrer sous le mauvais.

## Arborescence

```
params/     source de vérité (anthropometry, hardware, joints, actionneurs, exigences_S…)
parts/      pièces paramétriques (Python) et leurs relevés d'origines
scripts/    régénération, dimensionnement, grille de S, plans de découpe, contrôles
tests/      unittest
web/        feuille de style et scripts du site (aucune dépendance, aucun CDN)
sim/        simulation ; sim/upstream/ = venv amont
decisions/  fiches écrites depuis la refonte ; decisions/archive/ = les 64 d'avant
docs/       décisions actives, cadrage, choix des actionneurs, protocole du banc, glossaire
journal/    journal de bord, 10 lignes au plus par lot
archive/    documents, scripts, paramètres et tests retirés (rien n'est supprimé)
site/       engendré — jamais versionné
exports/    engendré — jamais versionné
```

`robot/` et `bom/` sont vides : ils n'ont pas encore de premier contenu.

## Le site

`yxor.fr` est une **projection du dépôt**, engendrée à chaque déploiement
par le `Dockerfile`, en deux étages : construction, puis service. Il ne
contient aucune donnée propre : chaque valeur affichée vient d'un fichier
du dépôt. Voir `decisions/archive/0018-application-web.md`.

## Documents

- **[Décisions actives](docs/decisions.md)**
- [Choix de l'actionneur de S](docs/choix-actionneurs.md) : faits,
  approvisionnement, grille d'exigences
- [Cadrage](docs/cadrage.md) : vision et méthode
- [Protocole du banc](docs/protocole-banc.md)
- [Glossaire](docs/glossaire.md)
- [Lecture du modèle amont](docs/lecture-modele.md)
- [Instructions de travail](CLAUDE.md)
