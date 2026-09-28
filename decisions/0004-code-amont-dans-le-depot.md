# 0004 — Du code YXOR qui s'exécute avec le venv amont

Date : 2026-09-28
Statut : acceptée

## Contexte

Faire marcher ToddlerBot en boucle fermée a demandé deux correctifs qui
n'étaient pas devinables et qui, surtout, **ne lèvent aucune erreur**
quand ils manquent (détail dans `journal/2026-09-20.md`). Le raisonnement
est consigné, mais le code correspondant n'a jamais quitté un répertoire
temporaire de session : il disparaîtra avec elle.

Un raisonnement écrit ne remplace pas un script qui tourne. Il faut donc
ce code dans le dépôt.

Or ce code **ne peut pas s'exécuter avec `~/yxor/.venv`** : il importe
`toddlerbot`, qui exige Python ≤ 3.12 et MuJoCo 3.3.4. Il ne tourne
qu'avec le venv amont. Cela heurte la règle posée par la fiche 0002 et
reportée dans `CLAUDE.md` : « tout ce qui est dans ce dépôt se lance avec
`.venv/bin/python`, jamais avec le venv amont ».

## Options examinées

| Option | Écartée pour |
| --- | --- |
| Laisser le code hors du dépôt | C'est l'état actuel, et il perd le code |
| Le réécrire sans `toddlerbot` | Réimplémenter la chaîne d'observation et le contrôleur PD : c'est précisément là que se logent les bugs qu'on vient de corriger |
| Aligner les deux venvs | Déjà écarté par la fiche 0002 : impossible sans maintenir un fork |
| Carve-out explicite et auto-vérifié | Retenue |

## Décision

### 1. Un répertoire, et un seul

`sim/upstream/` contient le code YXOR qui s'exécute avec le venv
**amont**. Aucun autre emplacement du dépôt n'a ce droit. Le nom du
répertoire porte l'information.

### 2. La règle devient vérifiable au lieu d'être déclarative

L'ancienne règle reposait sur la mémoire de l'opérateur. Elle est
remplacée par un **garde-fou exécuté** : chaque fichier de
`sim/upstream/` appelle `require_upstream_env()` avant tout travail. La
fonction vérifie la version de Python, celle de MuJoCo et la présence de
`toddlerbot`, puis s'arrête avec un message nommant l'interpréteur à
utiliser.

Se tromper de venv ne peut donc plus produire un résultat faux
silencieusement — le cas exact que la règle cherchait à empêcher. Un
garde-fou qui s'exécute vaut mieux qu'une phrase qu'on oublie.

### 3. Sens de l'interdiction, précisé

L'interdiction ne portait jamais sur l'emplacement des fichiers mais sur
le risque de mesurer avec la mauvaise version de MuJoCo. Elle est donc
reformulée dans `CLAUDE.md` :

- `sim/` hors `sim/upstream/` → venv YXOR (3.14 / MuJoCo 3.13.0)
- `sim/upstream/` → venv amont (3.12 / MuJoCo 3.3.4)
- **l'inverse est interdit dans les deux sens**, et les deux sens sont
  désormais contrôlés à l'exécution.

### 4. Racine amont configurable

Les scripts localisent le dépôt amont par la variable d'environnement
`TODDLERBOT_ROOT`, à défaut `~/upstream/toddlerbot`. Aucun chemin
absolu n'est figé dans le code.

## Conséquences

- `sim/upstream/` importe du code tiers : il est **inutilisable sans la
  pile amont installée**. C'est assumé, et le garde-fou le dit.
- Les correctifs restent des **contournements d'un défaut amont**, pas
  des choix de conception YXOR. Si l'amont les corrige, `sim/upstream/`
  devra être réévalué — et le SHA d'ancrage de la fiche 0002 est ce qui
  permettra de dater la comparaison.
- La règle 4 est inchangée : rien de binaire, les vidéos vont dans
  `exports/`.
