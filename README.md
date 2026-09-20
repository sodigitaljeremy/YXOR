# YXOR

Robot humanoïde bipède autonome à IA embarquée locale.

Le robot n'est pas conçu à une taille donnée, mais comme un système paramétré
par une variable unique `H` (taille totale), déclinable en trois paliers :

| Palier | H | Statut |
| --- | --- | --- |
| P1 | ~0,56 m | À construire |
| P2 | ~0,85–1,00 m | Conception seule |
| P3 | ~1,70 m | Cible du système de conception |

Base de départ : [ToddlerBot](https://github.com/hshi74/toddlerbot) (Stanford).
Code sous licence MIT, fichiers mécaniques sous Creative Commons non commerciale.

## Principe

Aucun fichier binaire ne fait autorité. Toute géométrie se régénère depuis le
texte source. Le dépôt contient le **code des pièces**, jamais les pièces.

```
params/     source de vérité dimensionnelle
parts/      pièces paramétriques (Python)
robot/      assemblage, URDF, MJCF
sim/        environnements et politiques
docs/       cadrage, cahier des charges, plan, glossaire
decisions/  fiches de décision datées
journal/    journal de bord
bom/        nomenclature
exports/    généré — jamais versionné
```

## État

Phase 0 — socle. Voir `docs/02-plan-action.md`.

## Documents

- [Note de cadrage](docs/00-cadrage.md)
- [Cahier des charges](docs/01-cahier-des-charges.md)
- [Plan d'action](docs/02-plan-action.md)
- [Artefacts](docs/03-artefacts.md)
- [Glossaire](docs/glossaire.md)