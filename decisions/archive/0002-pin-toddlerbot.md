# 0002 — Ancrage de ToddlerBot et environnement bicéphale

Date : 2026-09-20
Espèce : close
État : appliquée
Statut : acceptée

## Contexte

La décision 0001 retient ToddlerBot comme base de départ. Il faut
maintenant l'installer. Deux points imposent d'être fixés par écrit
avant toute installation.

**Le dépôt amont est activement maintenu.** Sans point d'ancrage, une
mesure prise aujourd'hui n'est pas reproductible dans six mois : le
code aura bougé, les versions épinglées aussi, et il sera impossible de
savoir si un écart vient d'une modification YXOR ou d'une évolution
amont.

**Les versions épinglées par ToddlerBot sont incompatibles avec
l'interpréteur du projet.** Le `pyproject.toml` amont déclare
`requires-python = ">=3.10"` mais épingle `numpy==1.26.4`,
`jaxlib==0.4.28`, `torch==2.3.1` et `opencv-python==4.9.0.80`. Aucun de
ces paquets ne publie de roue au-delà de **cp312**. Or la machine tourne
sous Ubuntu 26.04 avec **Python 3.14.4 pour seul interpréteur**, et
l'archive Ubuntu 26.04 ne propose aucun paquet `python3.12`.

Le constat du journal du même jour — « les roues cp314 existent pour
torch 2.14 et jaxlib 0.11.2 » — portait sur les versions *courantes*,
pas sur les versions *épinglées par ToddlerBot*. Il ne s'applique donc
pas ici.

## Options examinées

| Option | Écartée pour |
| --- | --- |
| Porter ToddlerBot sur Python 3.14 | Remonter numpy, jax et torch de plusieurs versions majeures : c'est maintenir un fork, avant même d'avoir fait marcher l'original |
| Rétrograder tout le projet en 3.12 | Sacrifie un environnement 3.14 qui fonctionne et sur lequel les outils de simulation sont déjà validés |
| Deux interpréteurs cloisonnés | Retenue |

## Décision

### 1. Ancrage

ToddlerBot est figé au commit :

```
e337f3b177b4b53abff70b31d1695a7b66cc6d2e
```

- Dépôt : https://github.com/hshi74/toddlerbot
- Branche : `main`
- Date du commit : 2026-04-19
- Version déclarée : `toddlerbot 0.2.0`
- Licence du code : MIT

Motif : c'est la tête de `main` au jour de l'installation. Aucune
étiquette de version n'est publiée par le projet, le SHA est donc le
seul ancrage possible. Toute mesure consignée dans le journal se
rapporte à ce commit et à lui seul.

Le dépôt amont est cloné **hors de YXOR**, dans `~/upstream/toddlerbot`.
C'est du code tiers : il n'a rien à faire dans l'historique du projet.

### 2. Environnement bicéphale

Le projet utilise désormais **deux interpréteurs Python cloisonnés**,
qui ne doivent jamais être confondus :

| | Code YXOR | Pile ToddlerBot |
| --- | --- | --- |
| Interpréteur | **Python 3.14.4** (système) | **Python 3.12.14** (fourni par uv) |
| Venv | `~/yxor/.venv/` | `~/upstream/toddlerbot/.venv/` |
| Portée | `sim/view.py`, `sim/render.py`, tout le code du dépôt | dépôt amont uniquement |
| MuJoCo | 3.13.0 | 3.3.4 (version épinglée par l'amont) |
| Installé par | `requirements.txt` | `pyproject.toml` amont |

Les deux MuJoCo diffèrent, et c'est voulu : les outils YXOR sont validés
sur 3.13.0, la pile amont est cohérente avec 3.3.4. Les mélanger
reviendrait à tester une combinaison que personne n'a jamais testée.

Le Python 3.12 est installé par `uv` dans `~/.local`, sans toucher au
système ni à `.venv/`.

### 3. Variante d'installation

`torch` est installé en build **CPU-only**. La machine n'expose aucun
GPU (`/dev/dri` absent, rendu llvmpipe) : les ~1,8 Go de bibliothèques
CUDA que `torch==2.3.1` tire par défaut seraient inutilisables. L'extra
`linux` du `pyproject.toml` amont, qui impose `jax[cuda12]`, n'est pas
installé pour la même raison.

## Conséquences

- **Ne jamais lancer le code YXOR avec le venv ToddlerBot, ni
  l'inverse.** Se tromper d'interpréteur donnera soit un `ImportError`,
  soit — plus vicieux — une version de MuJoCo différente de celle sur
  laquelle les mesures ont été prises. Règle reportée dans CLAUDE.md.
- Toute mise à jour de l'amont est une **décision**, pas une routine :
  elle remplace le SHA ci-dessus et invalide les mesures qui s'y
  rapportent.
- L'entraînement par renforcement reste hors de cette machine. Installer
  la pile ne change pas cette règle : MJX vise le GPU, il n'y en a pas.
- `~/upstream/` n'est pas versionné par YXOR et ne doit jamais l'être.
