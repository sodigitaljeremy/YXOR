# 0056 — Code sous le venv amont : un seul sens est vérifié

Date : 2026-09-30
Espèce : gouvernante
État : appliquée
Statut : **appliquée** — lot de cohérence validé par Jeremy le 2026-09-30 (~23 h), point 4. Ce qui est décrit est ce qui existe.
Remplace : `0004-code-amont-dans-le-depot.md`

## Pourquoi remplacer la 0004

Son § 3 affirme : « les deux sens sont désormais contrôlés à
l'exécution ». **C'est faux**, et CLAUDE.md le dit depuis le lot A du
2026-09-30. La fiche, elle, gardait l'erreur (audit de la nuit du 29,
C1 ; `docs/etat-des-lieux-2026-09-30.md` § 3.3).

## La décision

Les §§ 1, 2 et 4 de la 0004 restent **inchangés**, à savoir :

- `sim/upstream/` est le seul répertoire qui s'exécute avec le venv
  amont ;
- chacun de ses fichiers appelle `require_upstream_env()`, qui refuse le
  mauvais interpréteur ;
- la racine amont se lit dans `TODDLERBOT_ROOT`.

**Le § 3 est remplacé par ceci.** L'interdiction vaut dans les deux sens,
mais **un seul est vérifié** :

| Sens | Interdit | Vérifié à l'exécution |
| --- | --- | --- |
| `sim/upstream/` lancé par le venv YXOR | oui | **oui** (`require_upstream_env()`) |
| code YXOR lancé par le venv amont | oui | **non** : il tournerait avec MuJoCo 3.3.4 sans rien dire |

Le second sens ne repose que sur la discipline et sur le contrôle manuel
de CLAUDE.md (`python -c "import mujoco; print(mujoco.__version__)"`).

**Ce qui n'est pas décidé** : ajouter une garde symétrique dans le code
YXOR. C'était proposé par l'audit de la nuit du 29, et ce n'est pas fait.
