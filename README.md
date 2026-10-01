# YXOR

Robot humanoïde bipède autonome à IA embarquée locale.

> **À lire en premier : [le cadrage](docs/cadrage.md).** Ce qu'est YXOR, comment se décident sa taille, son budget et ses actionneurs, et pourquoi. Tout le reste du dépôt s'y rattache.

Le robot n'est pas conçu à une taille donnée, mais comme un système paramétré
par une variable unique `H` (taille totale), déclinable en trois paliers :

| Palier | H | Statut |
| --- | --- | --- |
| P1 | ~0,56 m | À construire |
| P2 | ~0,90 m | Conception seule |
| P3 | ~1,70 m | Cible du système de conception |

Base de départ : [ToddlerBot](https://github.com/hshi74/toddlerbot) (Stanford).
Son code est sous licence MIT ; sa conception (fichiers mécaniques) est sous
**CC BY-NC-SA 4.0**. Voir « Provenance et licences » ci-dessous.

## Provenance et licences — *provisoire*

⚠ **Aucune licence pour l'instant : choix délibéré de Jeremy le 2026-09-30 (fiche 0063),
à rouvrir.** Il n'y a pas de fichier `LICENSE`. Aucun droit n'est donc
accordé au-delà de ce que permettent les conditions de GitHub. Les options
étudiées sont dans `archive/docs/controle-publication-2026-09-30.md` § 3.

**Valeurs extraites de ToddlerBot.** Les fichiers ci-dessous contiennent des
valeurs numériques extraites de ToddlerBot : axes, butées, rapports de
transmission, masses, hauteur, noms d'articulations, empreintes des poids.

- `params/upstream_joints.generated.yaml` (extrait engendré) ;
- `params/joints.yaml` ;
- `params/ckpts.manifest.yaml` ;
- dans `params/actionneurs.yaml` et `params/anthropometry.yaml`, les seules
  entrées d'origine `amont` (`scripts/audit_origines.py --amont` les liste).

Ces valeurs viennent de **ToddlerBot**, de Haochen Shi, Weizhuo Wang, Shuran
Song et C. Karen Liu (Stanford) : <https://github.com/hshi74/toddlerbot>,
commit `e337f3b`, article arXiv:2502.00893. La conception de ToddlerBot est
publiée sous **[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)**,
son code sous MIT (© 2023 Haochen Shi). Par prudence, **ces fichiers sont
à traiter sous CC BY-NC-SA 4.0**, avec cette attribution. Les valeurs ont
été modifiées : réconciliées, renommées, qualifiées (fiches 0005 à 0007).

Savoir si des valeurs numériques isolées sont couvertes par cette licence
est une **question ouverte, sans avis** (fiche 0010 § 4). La mention
ci-dessus ne la tranche pas. **Aucune géométrie ToddlerBot n'entre dans une
pièce YXOR** (fiche 0001).

**Autres fichiers tiers.** `sim/models/humanoid.xml` est le modèle d'exemple
de MuJoCo, © 2021 DeepMind Technologies Limited, sous Apache-2.0. Son
en-tête de licence est conservé.

## Principe

Aucun fichier binaire ne fait autorité. Toute géométrie se régénère depuis le
texte source. Le dépôt contient le **code des pièces**, jamais les pièces.

Et le corollaire, appris à ses dépens : **une règle qu'aucun contrôle ne
vérifie ne tient pas.** Chaque règle structurante a, ou doit avoir, sa
commande qui échoue quand elle est enfreinte.

## Commandes

```sh
.venv/bin/python scripts/regenerer.py          # tout : pièces, site, contrôles
.venv/bin/python scripts/audit_origines.py --strict   # d'où vient chaque cote
.venv/bin/python scripts/controle_depot.py     # règle 4 : rien de binaire
.venv/bin/python parts/semelle_apprentissage.py       # une pièce seule
```

`regenerer.py` enchaîne les trois : il exécute les pièces, vérifie le dépôt,
engendre le site, contrôle la structure HTML, et **sort en erreur** si l'un
des contrôles échoue. C'est la seule commande à connaître.

⚠ Toujours `.venv/bin/python`, jamais `python`. Voir « Deux interpréteurs »
dans `CLAUDE.md` : `sim/upstream/` est le seul répertoire qui s'exécute avec
l'autre environnement, et il refuse de démarrer sous le mauvais.

## Arborescence

```
params/     source de vérité dimensionnelle (anthropometry, hardware, joints)
            + origines.yaml et nullites.yaml, qui DÉCLARENT des règles
parts/      pièces paramétriques (Python) et leurs relevés d'origines
scripts/    régénération, audit, plans de découpe, contrôles
web/        feuille de style et scripts du site (aucune dépendance, aucun CDN)
site/       engendré — jamais versionné
exports/    engendré — jamais versionné
robot/      assemblage, URDF, MJCF
sim/        environnements et politiques ; sim/upstream/ = venv amont
decisions/  fiches de décision datées — voir decisions/index.md
journal/    journal de bord
docs/       glossaire, notes de lecture
bom/        nomenclature
```

## Le site

`yxor.fr` est une **projection du dépôt**, engendrée à chaque déploiement par
le `Dockerfile` (deux étages : construction puis service). Il ne contient
aucune donnée propre : chaque valeur affichée vient d'un fichier du dépôt.
Voir `decisions/0018-application-web.md`.

## Documents

- **[Cadrage](docs/cadrage.md) — LE document à lire en premier**
- [Index des fiches de décision](decisions/index.md) — engendré
- [État des lieux du 2026-09-29](archive/docs/etat-des-lieux-2026-09-29.md) — inventaire, règles outillées, distance au premier objet
- [Glossaire](docs/glossaire.md)
- [Lecture du modèle amont](docs/lecture-modele.md)
- [Instructions de travail](CLAUDE.md)
