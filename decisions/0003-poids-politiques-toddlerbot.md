# 0003 — Provenance des politiques pré-entraînées ToddlerBot

Date : 2026-09-20
Statut : acceptée

## Contexte

La décision 0002 ancre le *code* amont à un commit précis. Les politiques
apprises, elles, ne sont pas dans le dépôt : `POLICY_CONFIGS` livre des
chemins vides et le README renvoie vers un dossier Google Drive.

Ces poids posent un problème de traçabilité plus aigu que le code :

- ils ne sont **pas versionnés** — aucun SHA de commit ne les couvre ;
- ils viennent d'un **hébergeur tiers**, dont le contenu peut être
  remplacé ou supprimé sans préavis et sans trace ;
- un fichier Google Drive garde son identifiant quand son contenu
  change : l'identifiant seul ne prouve rien ;
- ce sont des **binaires opaques**. Une politique silencieusement
  différente produirait une démarche différente, sans erreur visible.

Sans relevé écrit, une mesure faite aujourd'hui serait irreproductible
et, pire, indétectablement fausse.

## Options examinées

| Option | Écartée pour |
| --- | --- |
| Entraîner nos propres politiques | Exige un GPU distant ; hors sujet pour valider la chaîne de simulation |
| Versionner les poids dans YXOR | Viole la règle 4 (rien de binaire dans Git) |
| Utiliser les poids sans les tracer | Rend toute mesure invérifiable a posteriori |
| Télécharger en consignant la provenance | Retenue |

## Décision

### 1. Origine retenue

- Source : dossier Google Drive référencé par le `README.md` amont
  (ligne 64) au commit `e337f3b177b4b53abff70b31d1695a7b66cc6d2e`
- Dossier : `1d0UGRc3-3wxMcqrZSlqRXkSnwFSC8Xk-`
- Relevé le : **2026-09-20**
- Volume total : **29,5 Mo** pour 10 archives
- Format : ONNX, exécutés sur CPU (`CPUExecutionProvider`)
- Entraînées avec RSL-RL (`rsl-rl-lib==2.3.3`), marqueur `rsl` dans les
  noms de fichiers

### 2. Les dix archives et leur date d'entraînement

La date est portée par le nom de fichier amont, au format
`AAAAMMJJ_HHMMSS`. C'est la date d'entraînement déclarée par l'amont,
pas celle du téléchargement.

| Compétence | Archive | Date d'entraînement | Taille |
| --- | --- | --- | --- |
| walk | `toddlerbot_2xc_walk_rsl_20251226_114612.zip` | 2025-12-26 | 3,0 Mo |
| get_up | `toddlerbot_2xc_get_up_rsl_20260214_145222.zip` | 2026-02-14 | 3,5 Mo |
| crawl_full | `toddlerbot_2xc_crawl_full_rsl_20260214_145000.zip` | 2026-02-14 | 3,5 Mo |
| crawl_only | `toddlerbot_2xc_crawl_only_rsl_20260214_145735.zip` | 2026-02-14 | 3,5 Mo |
| crawl_down_stairs | `toddlerbot_2xc_crawl_down_stairs_rsl_20260215_094639.zip` | 2026-02-15 | 0,8 Mo |
| crawl_up_stairs | `toddlerbot_2xc_crawl_up_stairs_rsl_20260217_211836.zip` | 2026-02-17 | 0,8 Mo |
| crawl_rotate | `toddlerbot_2xc_crawl_rotate_rsl_20251109_195839.zip` | 2025-11-09 | 3,5 Mo |
| climb_up_box | `toddlerbot_2xc_climb_up_box_rsl_20250907_201202.zip` | 2025-09-07 | 3,5 Mo |
| climb_wall | `toddlerbot_2xc_climb_wall_rsl_20250913_174540.zip` | 2025-09-13 | 3,5 Mo |
| climb_down_box | `toddlerbot_2xc_climb_down_box_rsl_20250914_014343.zip` | 2025-09-14 | 3,5 Mo |

Toutes visent la variante **`toddlerbot_2xc`**, celle de la décision
0002. Aucune n'existe pour `2xm` dans ce dossier.

### 3. Emplacement

`~/upstream/toddlerbot/ckpts/`, **hors du dépôt YXOR**. C'est le chemin
qu'attend `mjx_policy.py` (`ckpts/<nom>/model_best.onnx`), et `ckpts/`
figure déjà dans le `.gitignore` amont.

### 4. Vérification d'intégrité

L'empreinte **SHA-256 de chaque archive** est relevée à la réception et
consignée dans le journal du 2026-09-20. Ce sont des observations, pas
des décisions : elles n'ont pas leur place dans cette fiche, mais elles
sont la seule preuve que les poids utilisés pour nos mesures sont bien
ceux téléchargés ce jour-là.

Pour revérifier plus tard : `sha256sum ckpts/*.zip` et comparaison avec
le journal. Une empreinte qui diverge signifie que l'amont a republié —
et invalide les mesures associées.

## Conséquences

- **Ces poids ne sont couverts par aucun versionnement.** S'ils
  disparaissent du Drive, ils sont irrécupérables : ni l'amont ni YXOR
  n'en gardent copie publique. Une sauvegarde hors ligne est à prévoir
  si des mesures durables s'y appuient.
- La licence des poids n'est pas explicitée par l'amont. Le code est
  MIT, la conception CC BY-NC-SA. **En cas d'exploitation commerciale,
  ce point est à éclaircir avant toute réutilisation des poids** — il
  n'est pas tranché ici.
- Une politique n'est valable que pour la variante et la version de
  modèle sur lesquelles elle a été entraînée. Changer de modèle sans
  réentraîner produirait une démarche dégradée, sans message d'erreur.
- Remplacer une politique est une **décision**, pas une routine : elle
  remplace le tableau ci-dessus et invalide les mesures qui s'y réfèrent.
