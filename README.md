# YXOR

Robot humanoïde bipède autonome à IA embarquée locale.

Le robot n'est pas conçu à une taille donnée, mais comme un système paramétré
par une variable unique `H` (taille totale), déclinable en trois paliers :

| Palier | H | Statut |
| --- | --- | --- |
| P1 | ~0,56 m | À construire |
| P2 | ~0,90 m | Conception seule |
| P3 | ~1,70 m | Cible du système de conception |

Base de départ : [ToddlerBot](https://github.com/hshi74/toddlerbot) (Stanford).
Code sous licence MIT, fichiers mécaniques sous Creative Commons non commerciale.

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

- [Index des fiches de décision](decisions/index.md) — engendré
- [État des lieux du 2026-09-29](docs/etat-des-lieux-2026-09-29.md) — inventaire, règles outillées, distance au premier objet
- [Glossaire](docs/glossaire.md)
- [Lecture du modèle amont](docs/lecture-modele.md)
- [Instructions de travail](CLAUDE.md)
