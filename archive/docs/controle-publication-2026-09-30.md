# Contrôle avant publication — 2026-09-30

> **Mise à jour du 2026-09-30, ~23 h 55 — tiers : accord obtenu, historique publié tel quel.** Décidé par Jeremy (voir le journal du 2026-09-30, « Avant publication », point 4). L'anonymisation des fichiers actuels reste.

**Commencé à 22 h 33 CEST** (`date`). Base : commit `3007a58`, et
**132 commits** dans `git log --all`.

La décision de publier est celle de Jeremy (fiche 0053). **Ce contrôle
ne change pas la visibilité du dépôt.** Il n'a appliqué que la fiche
0053 et le paragraphe « Provenance et licences » du README. Tout le
reste est constaté ou proposé.

Statuts : **V** = lu ou exécuté ici ; **DÉD** = mon raisonnement ; **CG**
= connaissance générale, non vérifiée ici.

---

## 1 — Secrets : **aucun trouvé**

**gitleaks n'est pas installé**, et trufflehog non plus (**V**,
`which`). Le balayage a donc été fait à la main.

**Méthode (V).** J'ai passé `git log -p --all` sur les 132 commits, soit
62 286 lignes, en ne gardant que les lignes ajoutées ou retirées. J'y ai
cherché :

- les mots demandés : token, key, secret, password, passwd, bearer,
  api, `.env`, ssh, BEGIN, les adresses IPv4, coolify, hetzner ;
- les formats de jetons connus : `ghp_`, `github_pat_`, `gho_`, `sk-…`,
  `AKIA…`, `xox?-`.

J'ai aussi relevé la liste de **tous les chemins** ayant existé dans
l'historique (153) et tous les domaines d'URL cités.

| Motif | Occurrences | Nature |
| --- | ---: | --- |
| `token` | 1 | `asttokens==3.0.2`, un nom de paquet (`82b2866`, `requirements.txt`) |
| `secret` | 3 | « aucun secret » : prose de la 0018 et du journal du 28 (`445795b`, `c078b8e`) |
| `password`, `passwd`, `bearer`, `.env`, `api key` | 0 | — |
| `BEGIN` (clé PEM) | 0 | — |
| formats de jetons | 0 | — |
| `ssh` | 5 | « `~/.ssh` vide, pas d'accès SSH » : 0008 et journal du 28 (`82b2866`, `c078b8e`) ; « utilisable en SSH » dans `sim/render.py` (`ea00d09`) |
| `hetzner` | 12 | prose : « VPS Hetzner » (CLAUDE.md `353c6cb`, 0008, 0018, journaux, arbitrage). **Ni adresse, ni nom d'hôte, ni identifiant** |
| `coolify` | 35 | prose et commentaires sur le comportement de Coolify (`SOURCE_COMMIT`, `ARG`). **Ni URL de tableau de bord, ni webhook, ni jeton** |
| IPv4 | 9 | `127.0.0.1` (santé du conteneur, `c078b8e`) ; les autres sont des **numéros de version** (`8.0.1.0.0`, `4.9.0.80`, `6.18.33.2`, `v02.07.01.62`) |
| variables d'environnement | — | `YXOR_COMMIT`, `SOURCE_COMMIT`, `TODDLERBOT_ROOT`, `MUJOCO_GL` : aucune valeur secrète |

**Chemins sensibles (V).** Aucun `.env`, `*.pem`, `id_*`, `*.key` ni
`sources.local.yaml` n'apparaît dans l'historique. `sources.local.yaml`
est ignoré, et **n'a jamais été commité**.

**Identifiants Google Drive** (`params/ckpts.manifest.yaml`,
`scripts/ckpts_backup.py`) : ce sont ceux du dossier public que cite le
README amont (`~/upstream/toddlerbot/README.md:64`, **V**). Ce ne sont
pas des secrets.

**Limite (DÉD).** Un balayage par motifs ne voit pas un secret sans mot
clé ni format connu. Lancer gitleaks avant de basculer reste
**recommandable**, ce qui supposerait de l'installer. Rien de ce que
j'ai lu n'en laisse soupçonner.

---

## 2 — Données personnelles (**V**, liste, rien de modifié)

| Donnée | Où | Remarque |
| --- | --- | --- |
| **Adresse des auteurs de commits** | les 132 commits | une seule : `259069918+sodigitaljeremy@users.noreply.github.com`, l'adresse masquée de GitHub. Nom d'auteur : `sodigitaljeremy`. **Aucune adresse personnelle** |
| **Prénom « Jeremy »** | 273 lignes à HEAD, 383 dans l'historique | partout (fiches, journal, CLAUDE.md, cadrage). **Aucun nom de famille** trouvé |
| **« l'opérateur CN »** (tiers, prénom anonymisé le 2026-09-30) | 19 lignes : `budget.yaml:85`, `origines.yaml:594`, `cadrage.md:261, 482, 483`, `arbitrage`, `etat-des-lieux-2026-09-30`, `dimensionnement-par-actionneur`, 0042:144, journal du 30 | un tiers identifié par son prénom et par son rôle : découpe et usinage de métal, chiffrage attendu |
| **« un proche opérateur CN »** (tiers, lien de parenté anonymisé le 2026-09-30) | `hardware.yaml:59-61, 321-327` (`decoupe_operateur_cn`, `lieu: "chez un proche opérateur CN"`, `operateur_cn_alu_3`), `nullites.yaml`, fiches 0015, 0017, 0018, 0021, 0025, 0026, 0033, 0044, journaux | ni nommé ni localisé |
| **« Segnere »** | **0 occurrence**, dans HEAD comme dans l'historique | — |
| Nom d'utilisateur système `jeremy` | `/home/jeremy/…` dans `journal/2026-09-28.md:46`, et dans `site/data/pieces.json` de l'historique (`c078b8e`) | indique la machine, rien de plus |
| Environnement de travail | CLAUDE.md, journaux | PC sans GPU, WSL2, Ubuntu 26.04, noyau `6.18.33.2` |
| **Propos rapportés** | `docs/arbitrage-2026-09-30.md:48-51, 75-78` | « passe-temps non prioritaire », « Arrête tout », « je ne comprends rien à la codebase », « rêve de gosse » |
| Échanges avec des assistants | journaux, arbitrage, `docs/sources/etude-fournisseurs-chatgpt-2026-09-30.md` | le journal vouvoie « votre Hetzner » : c'est un texte d'assistant |
| Pays | « Suisse », TVA suisse, revendeurs CH (`budget.yaml`, cadrage § 7) | pays seulement, aucune ville |
| Adresses postales, téléphones | **0** (motifs `+41`, `+33`, numéros à 10 chiffres, `rue`, `avenue`, `CH-nnnn`) | les correspondances larges étaient des nombres et des dates |

**DÉD** : rien de ceci n'est un secret. Mais deux points sont à trancher
**avant** de basculer, parce qu'ils ne disparaîtront plus ensuite :

- **L'opérateur CN, un proche,** est un tiers. Accepterait-il d'être cité ?
- **Les propos rapportés dans l'arbitrage** vont devenir publics.

---

## 3 — Licence

### État (**V**)

- **Aucun fichier `LICENSE`**, et aucune mention SPDX dans les sources
  YXOR.
- **Le README disait**, à tort : « fichiers mécaniques sous Creative
  Commons non commerciale ». La licence amont est **CC BY-NC-SA 4.0**
  (`~/upstream/toddlerbot/README.md:167`). C'est corrigé, au point 6.

### Fichiers qui contiennent des valeurs extraites de ToddlerBot

Source : `audit_origines.py --amont`, **V**.

| Fichier | Valeurs `amont` | Mention actuelle |
| --- | ---: | --- |
| `params/upstream_joints.generated.yaml` | 715 | en-tête : commit `e337f3b`, fiche 0002, chemin du modèle, `depot: https://github.com/hshi74/toddlerbot`. **Aucune licence ni auteur nommés** |
| `params/joints.yaml` | 364 | « TOPOLOGIE TODDLERBOT ADOPTÉE » (fiche 0005), commit `e337f3b`, « ToddlerBot 2.0.0 ». **Ni licence ni auteurs** |
| `params/ckpts.manifest.yaml` | 40 | « Manifeste des poids ToddlerBot », fiche 0003. **Pas de licence** : celle des poids n'est pas tranchée (0003) |
| `params/actionneurs.yaml` | 3 | `reference_toddlerbot`, avec les sources « fiche 0001 », « MJCF @ e337f3b ». Pas de licence |
| `params/anthropometry.yaml` | 2 | `H` et `paliers.P1`, « ToddlerBot (fiches 0001 et 0011) ». Pas de licence |

S'y ajoutent **des valeurs dérivées**, non comptées `amont` par l'audit :

- les couples et vitesses de la marche ToddlerBot, cités dans
  `docs/exigences-actionnement-P2.md` et
  `docs/dimensionnement-par-actionneur.md` ;
- la série `exports/actionneurs/marche_15s.csv`, ignorée par Git.

**Ouvert** : ces valeurs viennent de l'exécution du code MIT sur le modèle
amont. Leur statut dépend de la question de la 0010 § 4 : **sans avis**.

**Autre fichier tiers.** `sim/models/humanoid.xml` : © 2021 DeepMind
Technologies Limited, sous Apache-2.0, en-tête conservé (**V**). Apache-2.0
demande de joindre le texte de la licence (**CG**). L'en-tête renvoie à
l'URL.

### Propositions (**non choisies** : décision de Jeremy)

L'objectif est « pièces libres et à Jeremy ». Jeremy garde ses droits
d'auteur quelle que soit la licence. La question est ce qu'il **accorde**
aux autres.

**Pour le code** (scripts, pièces paramétriques, site) :

| Option | Effet | Remarque |
| --- | --- | --- |
| **MIT** | tout permis, avec mention | celle de ToddlerBot : cohérence avec l'amont |
| **Apache-2.0** | tout permis, avec mention, et **licence de brevet** explicite | un peu plus lourde ; protège les réutilisateurs |

Les deux sont **permissives**. Aucune n'oblige Jeremy à publier ses
dérivés.

**Pour la conception propre** (géométrie engendrée, plans, DXF, données
de conception YXOR) :

| Option | Famille | Effet pour les autres | Remarque |
| --- | --- | --- | --- |
| **CERN-OHL-P-2.0** | permissive, matériel | tout permis, avec mention | la plus libre ; un tiers peut fermer son dérivé |
| **CERN-OHL-W-2.0** | réciprocité faible | doit republier ses modifications de la conception YXOR, pas le reste de son produit | voie médiane ; absente du tableau de CLAUDE.md |
| **CERN-OHL-S-2.0** | réciprocité forte | tout dérivé est publié sous la même licence | Jeremy, seul auteur, garde le droit de relicencier ses propres fichiers (**CG**). Les contributions extérieures le lieraient, faute d'accord de contribution |
| **CC BY 4.0** | permissive, générale | tout permis, avec mention | pas faite pour le matériel ; convient mieux à la documentation |

**Pour la documentation** (fiches, cadrage, journal) : **CC BY 4.0**, ou
CC BY-SA 4.0 si Jeremy veut la réciprocité.

**Rappel (V, CLAUDE.md)** : la règle « pas de copyleft fort **dans le
cœur** » vise les **dépendances**, pas la licence que Jeremy donne à
son propre travail. Choisir CERN-OHL-S pour ses fichiers ne l'enfreint
pas, mais **empêcherait** d'y intégrer une dépendance incompatible
(**DÉD**).

**Mention à porter sur les fichiers extraits** (en tête de fichier) :

```
# Contient des valeurs extraites de ToddlerBot — Haochen Shi, Weizhuo Wang,
# Shuran Song, C. Karen Liu (Stanford) — https://github.com/hshi74/toddlerbot,
# commit e337f3b. Conception ToddlerBot : CC BY-NC-SA 4.0
# (https://creativecommons.org/licenses/by-nc-sa/4.0/). Valeurs modifiées
# (réconciliées, renommées, qualifiées) ; ce fichier est distribué sous
# CC BY-NC-SA 4.0. La couverture de valeurs isolées par cette licence est
# une question ouverte (decisions/0010 § 4).
```

Le README la porte déjà en provisoire (point 6). Les en-têtes eux-mêmes
**ne sont pas modifiés ici**.

**Conséquence (DÉD)** : avec NC-SA, ces fichiers restent **non
commerciaux** et **réciproques**, quelle que soit la licence du reste.
Si la question de la 0010 § 4 est tranchée dans le sens prudent, tout
dérivé de `joints.yaml` hérite de NC-SA. C'est déjà la logique de la
0001 : aucune géométrie amont n'entre dans une pièce YXOR.

---

## 4 — Fichiers à ne pas publier, ou à regarder

### Ce qui est suivi (**V**)

| Fichier | Avis |
| --- | --- |
| `Dockerfile`, `nginx.conf` | configuration de déploiement **sans secret** ni hôte. Publiable (**DÉD**) |
| `docs/sources/etude-fournisseurs-chatgpt-2026-09-30.md` | texte ChatGPT versé tel quel. À publier en connaissance de cause (voir le § 2) |
| `docs/arbitrage-2026-09-30.md`, `journal/*.md` | notes de travail, avec des propos rapportés (voir le § 2) |
| **Historique** : `site/` au commit `c078b8e` | **STEP, STL, DXF et PDF** de la semelle, `site/data/*.json` avec des chemins `/home/jeremy/…`. Ce sont des fichiers de Jeremy, sans secret. Ils seront publics avec l'historique. Les retirer demanderait une réécriture : **pas nécessaire** (**DÉD**) |

### Ce qui n'est pas suivi (**V**, `git status --ignored`)

| Fichier | État |
| --- | --- |
| `.venv/`, `exports/`, `site/`, `__pycache__/` | ignorés |
| `sources.local.yaml` | ignoré, jamais commité |
| **`docs/conclusion-arbitrages-2026-09-30.md`** | **non suivi, non ignoré** : un `git add -A` le publierait. Son sort est en attente (proposition (b)) |

`exports/` contient, entre autres, les courbes Damiao et les séries
ToddlerBot. Il reste ignoré, et c'est ce qui les tient hors publication.

### Ce que `.gitignore` devrait couvrir en plus (proposé, non appliqué)

```
.env
.env.*
*.pem
*.key
id_*
.claude/
.vscode/
.idea/
*.local.*
.pytest_cache/
scratchpad/
```

**Aucun de ces fichiers n'existe aujourd'hui** (**V**). Il s'agit de
prévenir, pas de réparer.

---

## 5 et 6 — Appliqués

- **Fiche 0053, « Le dépôt passe public »** : gouvernante, acceptée, non
  appliquée. Elle porte les deux motifs de Jeremy et la limite : les
  copies faites ne disparaissent pas, et c'est l'historique entier qui
  est publié. Elle note aussi l'écart avec la recommandation D5 de
  l'arbitrage.
- **README, « Provenance et licences » (provisoire)** :
  - pas encore de licence propre ;
  - liste des fichiers extraits, avec l'attribution ToddlerBot
    (auteurs, dépôt, commit, CC BY-NC-SA 4.0) ;
  - question 0010 § 4 laissée ouverte ;
  - mention de `humanoid.xml` (Apache-2.0).
  - La phrase fausse « Creative Commons non commerciale » est corrigée
    dans la foulée, puisqu'elle portait sur le même objet.

---

## Avant de basculer (DÉD, pour Jeremy)

1. Choisir les licences, ou accepter consciemment de publier sans
   licence.
2. Décider du sort de `conclusion-arbitrages-2026-09-30.md`.
3. Décider si l'opérateur CN et les propos de l'arbitrage restent tels
   quels.
4. Idéalement, passer gitleaks.
