# État des lieux — 2026-09-29, nuit

**Commencé le mardi 2026-09-29 à 23 h 40 CEST**, heure système lue par
`date` avant toute autre commande. Dépôt au commit `637ef04`, arbre propre.

**Pourquoi « -nuit » dans le nom.** `docs/etat-des-lieux-2026-09-29.md`
existe déjà (commit `80daa46`, 12 h 21 le même jour). Le remplacer aurait
effacé un document que le README cite. Le suffixe reprend la convention
de `journal/2026-09-29-nuit.md`.

**Ce document ne corrige rien.** Il n'a modifié aucun fichier suivi : il
n'a créé aucune fiche et changé aucun paramètre. Les commandes exécutées
ont écrit dans `exports/` et `site/` (tous deux ignorés), et dans le
dossier temporaire de la session. `index_fiches.py` a réécrit
`decisions/index.md` à l'identique ; `git status` est resté propre.

## Légende des statuts

| Marque | Sens |
| --- | --- |
| **V** | **vérifié** — je l'ai exécuté, lu ou compté pendant cet audit |
| **D** | **déclaré** — le dépôt l'affirme, je ne l'ai pas revérifié |
| **Déd** | **déduit** — mon raisonnement, à discuter |

Méthode : quatre lectures parallèles (fiches 0001-0015, 0016-0030,
0031-0044, graphe d'appel du code). J'ai revérifié moi-même chacun des
constats classés « critique » ou « haute » au § 8. Les autres viennent de
ces lectures et gardent leur preuve `fichier:ligne`.

---

## 1 — Chronologie

Source : `git log` (58 commits), **V**. Les heures sont celles des commits,
pas celles du travail.

| Étape | Quand | Commits | Ce qui arrive |
| --- | --- | ---: | --- |
| **0. Socle** | 20/09, 20 h 14 – 20 h 20 | 2 | `353c6cb` : arborescence, CLAUDE.md, fiche 0001 (ToddlerBot comme base) |
| **1. Simulation** | 20/09, 20 h 25 – 23 h 41 | 5 | outillage MuJoCo, blocage AVX, mesures sous WSL2, ToddlerBot épinglé (0002), marche ZMP rejouée puis politique ONNX en boucle fermée (0003) |
| **— pause —** | 21/09 – 27/09 | **0** | **aucun commit pendant sept jours.** Le journal du 28 s'ouvre sur « Reprise après une semaine » (`journal/2026-09-28.md:3`, **V**). Rien d'autre n'en est dit. |
| **2. Données amont** | 28/09, 12 h 03 – 14 h 01 | 6 | correctifs rapatriés dans `sim/upstream/` (0004), topologie du bras (0005), butées extraites du MJCF (0006), `joints.yaml` réconcilié (0007), sauvegarde des poids et build123d (0008, 0009) |
| **3. Traçabilité** | 28/09, 16 h 49 – 17 h 34 | 4 | origine des cotes (0010, 0011), correction d'`anthropometry.yaml` (0012), nature des cotes (0013) |
| **4. Pivot fabrication** | 28/09, 18 h 02 – 19 h 42 | 3 | pas d'imprimante 3D (0014), plaques et entretoises (0015), semelle livrée, « aucun précédent » (0016) puis MEVITA (0017) |
| **5. Site** | 28/09, 20 h 38 – 22 h 54 | 7 | application web (0018), Dockerfile, carton ondulé, interface catalogue (0019) |
| **6. Structures** | 29/09, 09 h 03 – 12 h 21 | 7 | nullité (0020), simulation navigateur (0021-0023), audit (0024), mobile (0025), quatre tables (0026), achat (0027), licences et torsion (0028-0033), **premier état des lieux** |
| **7. Faux verts et déploiement** | 29/09, 13 h 04 – 17 h 39 | 15 | ANSUR II (0034), norme (0035), refonte des fiches (0036), verdict par pièce (0037), thermique (0038-0039), sources (0040) ; déploiement cassé 4 h, empreinte, Chromium, cache CSS ; consolidation de CLAUDE.md |
| **8. Premier objet** | 29/09, 22 h 37 – 23 h 33 | 7 | **semelle coupée** en carton ondulé (`8e1bee2`), repesée, profil double cannelure (0041-0044), erreur de date corrigée, passation |

**Débit** (**V**) : 44 fiches en trois jours de travail effectif, dont 25
le 29/09. Depuis le premier état des lieux (`80daa46`, 12 h 21), il y a
eu 23 commits : +3 788 lignes de prose, +2 132 de code, +651 de données.

**Un trou.** Rien ne dit ce qui s'est passé entre le 21 et le 27. Le
dépôt ne le sait pas, et je ne le comble pas.

---

## 2 — Décisions : les 44 fiches

L'espèce, l'état et les renvois sont lus dans les en-têtes (**V**, via
`decisions/index.md`, régénéré à l'identique). La colonne « reflet » dit si
le code applique ce que la fiche décide.

| # | Sujet | Espèce · état | Décide | Reflet dans le code |
| --- | --- | --- | --- | --- |
| 0001 | ToddlerBot comme base | historique · appliquée | base ToddlerBot, P1 = 0,56 m | **V** `anthropometry.yaml:38` |
| 0002 | ancrage, deux venvs | close · appliquée | amont figé à `e337f3b`, venvs séparés | **V** HEAD amont = `e337f3b1…` ; 3.12.14/3.3.4 et 3.14.4/3.13.0 |
| 0003 | poids pré-entraînés | historique · appliquée | 10 archives ONNX, provenance consignée | **V** `ckpts_backup.py verify` : 10 conformes |
| 0004 | code sous venv amont | gouvernante · appliquée | seul `sim/upstream/` tourne sous l'amont | **V dans un sens seulement** (§ 8, C1) |
| 0005 | topologie du bras P1 | close · amendée par 0011 | `elbow_yaw` à la place de `wrist_yaw` | **V** `joints.yaml:347` |
| 0006 | fichier engendré commité | close · appliquée | exception à la règle 4 pour `upstream_joints.generated.yaml` | **V** `import_upstream_limits.py --check` : à jour |
| 0007 | sourcing du matériel | close · appliquée | Onshape n'est pas une référence | **V** vocabulaire `joints.yaml:21-26` ; `releve_onshape` jamais employé |
| 0008 | sauvegarde des poids | close · appliquée | manifeste dans Git, archives hors Git, deux destinations | **partiel** — une destination avérée (§ 8, H2) |
| 0009 | build123d | close · amendée par 0029 | `build123d==0.13.0` épinglé | **V** `check_cad_toolchain.py` : 16/16 |
| 0010 | origine des cotes | gouvernante · amendée par 0011 | toute cote porte une origine ; accesseur `yxor/cotes.py` | audit **V** ; **`yxor/cotes.py` n'a jamais existé** (§ 8, H9) |
| 0011 | origine `litterature` | close · appliquée | cinquième origine ; filiation de H | **V** `origines.yaml:228-243` |
| 0012 | correction d'anthropometry | historique · appliquée | sources ligne à ligne | **V** ; amendée par 0034 **sans renvoi** |
| 0013 | nature des cotes | gouvernante · appliquée | règle 1 restreinte à `echelle` | **V** audit (49 `echelle`) ; nature `tenue` : 0 occurrence |
| 0014 | pas d'imprimante 3D | historique · appliquée | l'impression sort du périmètre | **V** CLAUDE.md, `hardware.yaml:400-426` |
| 0015 | plaques et entretoises | close · amendée par 0042 **et 0016** | découpe 2D seule | **V** CLAUDE.md:36-55 ; le renvoi 0016 est invisible dans l'index (§ 8, C4) |
| 0016 | ~~aucun précédent~~ | historique · amendée par 0017 | constat, titre infirmé | sans objet |
| 0017 | MEVITA | historique · appliquée | un précédent en tôle existe | constat, sans code |
| 0018 | site statique | gouvernante · appliquée | générateur, Docker, nginx | **V** ; prescrit three.js épinglé, le code fait du WebGL brut (`viewer.js:3`) **sans fiche** |
| 0019 | interface catalogue | close · amendée par 0037 | schéma lettré, rangs, verdict | **V** `pages.py:178, 412-415` |
| 0020 | trois états du `null` | gouvernante · appliquée | `a_mesurer` / `sans_objet` / `se_deduira` | **V** `nullites.py` : 3 / 0 / 3 |
| 0021 | machine × matériau | abandonnée | clé composée | jamais appliquée ; anciens noms en commentaire seulement |
| 0022 | soudure | historique · instruction | ne décide rien | sans objet |
| 0023 | simulation navigateur | close · appliquée | portage JS du profil, deux gardes | **V** en Python (écart 0,0024 mm) ; **JS jamais exécuté** (§ 3) |
| 0024 | audit, refactorisation | close · appliquée | plan en trois rangs | rang 1 fait ; #8-#10 du rang 2 faits, **alors que le statut dit « non entamés »** |
| 0025 | mobile d'abord | close · appliquée | règles CSS de lecture sur téléphone | **V** `style.css:205, 230, 244-256` ; jamais mesuré sur un appareil |
| 0026 | quatre tables | close · amendée par 0033 | machines / procédés / matières / réglages | **V** `procedes.py` : 3 · 3 · 5 · 6 |
| 0027 | règle d'achat | close · appliquée | branches a, b, c | **(a) non outillée** (§ 8, C2) |
| 0028 | quatre affirmations | historique · appliquée | vérification | constat ; sa question ISO 4762 est reprise par la 0035, **sans renvoi** |
| 0029 | familles de licences | historique · appliquée | CERN-OHL-S n'est pas non commerciale | **V** CLAUDE.md ; la licence amont y est mal nommée (§ 8, H1) |
| 0030 | fichiers fournisseurs | gouvernante · appliquée | six champs, rien dans Git | **V** `controle_depot.py:100-130` ; 2 entrées ANSUR |
| 0031 | torsion par section | historique · appliquée | aucun facteur stocké | **V** par absence |
| 0032 | cinq pistes en veille | veille | OrcaSlicer, 3MF, FreeCAD MCP, Zoo, bd_warehouse | **V** bd_warehouse absent ; le texte hésite entre cinq et quatre pistes |
| 0033 | épaisseur = champ | gouvernante · appliquée | option B chiffrée | **V** `hardware.yaml:43-350` |
| 0034 | ANSUR II | historique · appliquée | 12 ratios remplacés | **V** `ratios_ansur.py` ; semelle P2 à 138,06 × 51,93 |
| 0035 | origine `norme` | proposition · acceptée | 6ᵉ origine, axe `verifiabilite` calculé | **rien d'appliqué, et la fiche le dit** (**V** : `ORIGINES`, `audit_origines.py:63`) |
| 0036 | refonte des fiches | close · appliquée | espèce, état, parcours d'entrée | **diverge** : 3 espèces dans la fiche, 6 dans `index_fiches.py:27` |
| 0037 | verdict par pièce | close · appliquée | `besoins_procede` par pièce | **V** ; mais le verdict est **inerte** (§ 8, C2) |
| 0038 | thermique | proposition · proposée | dimensionner à la température | **déjà en partie appliquée** : série de couples produite (§ 8, H5) |
| 0039 | semelle porte-capteurs | historique · appliquée | note, ne conçoit rien | sans objet ; cite une source `non_lu` comme fait |
| 0040 | registre des sources | gouvernante · appliquée | registre, pas de RAG | **V** `source.py --liste` : 8 sources, 2 partielles, 6 non lues |
| 0041 | incertitude | proposition · proposée | porter ± sur les mesures | **déjà en partie appliquée** : `mesures.yaml`, 5 entrées au lieu de 3 |
| 0042 | rayon matière ou geste | proposition · proposée | champ `rayon_min_geste` | aucune trace ; fait pourtant passer 0015 en « amendée » |
| 0043 | deux matières ou une | close · appliquée | `carton_ondule_double` créé | **V** `hardware.yaml:190, 285` |
| 0044 | semelle publiée ≠ coupée | proposition · proposée | variante ondulé | rien de généré ; **le site montre toujours la plume 5 mm** |

**Répartition par espèce** (**V**, index) : gouvernante 8 · historique 12
· close 17 · proposition 5 · veille 1 · abandonnée 1.

### Appliquées sans que le code le reflète

- **0004** : « les deux sens sont vérifiés à l'exécution ». Un seul l'est.
- **0008** : deux destinations de sauvegarde, une seule avérée.
- **0010** : l'accesseur `yxor/cotes.py` et le refus d'une mauvaise
  origine n'existent pas. `Cotes` est une classe locale à la semelle
  (`parts/semelle_apprentissage.py:71`), et `echelle()` écrit l'origine
  `litterature` en dur.
- **0027 (a)** : « `regenerer.py` peut le refuser ». `grep coupable
  scripts/regenerer.py` ne trouve rien (**V**).
- **0036** : la taxonomie codée n'est pas celle de la fiche, et
  l'archive `decisions/archive/` qu'elle prévoit n'existe pas.
- **0037** : le garde-fou de largeur minimale devait être « écrit comme
  manquant ». Aucune trace.

### Reflétées dans le code sans fiche

- **La densité descendue du matériau à la matière** (`b52d77c`,
  `hardware.yaml:118-123`). La 0043 dit pourtant « je ne le corrige pas ».
- **WebGL brut au lieu de three.js** : l'écart avec la 0018 §4 n'est
  justifié que dans le journal (`2026-09-28.md:2249`, **D**).
- **Le vocabulaire de `mesures.yaml`** (`sous_resolution`, `incertitude:
  null`) élargit la 0041, qui n'est que proposée.
- **La série de couples** (`replay_policy.py:119-126`,
  `enveloppes_actionneurs.py:183-188`) applique la 0038, proposée.
- **Les espèces `veille`, `abandonnee` et `proposition`**, ajoutées à
  `index_fiches.py` sans repasser par la 0036 (relevé déjà par la
  passation).

### Réécritures après coup (règle 5)

J'ai mesuré, par `git diff` entre le commit de création de chaque fiche
et `HEAD` (**V**) : **42 fiches sur 44 ont changé après leur création.**
Pour 36 d'entre elles, c'est l'en-tête Espèce/État ajouté par la 0036
(+2 à +5 lignes). **Six ont reçu des sections entières** : 0035 (+79),
0026 (+59), 0032 (+55), 0027 (+46), 0043 (+37), 0034 (+34).

Ces sections sont datées et ajoutées à la suite, jamais substituées.
**Déd** : c'est une pratique « amendement en ligne », que la règle 5
n'autorise ni n'interdit clairement. Elle a un coût mesurable : les
renvois de lignes de 0010 et 0011 vers la 0001 (« ligne 24 », « ligne
36 ») sont décalés de deux lignes depuis l'ajout des en-têtes (relevé
par la lecture 0001-0015).

---

## 3 — Implémenté

Tous les scripts ont été **lancés** pendant cet audit, sauf `sim/view.py`
(il ouvre une fenêtre). Durées et sorties **V**.

### `scripts/` — 19 fichiers

| Script | Rôle | Appelé par | Résultat de l'exécution |
| --- | --- | --- | --- |
| `regenerer.py` | tout : pièce, audit, site, contrôles | Dockerfile, README | **sortie 0, 27,6 s** ; 1 pièce, 5 pages, 15 fichiers, 247 ko |
| `pages.py` | gabarits HTML | `regenerer` | via `regenerer` |
| `plan_decoupe.py` | PDF A4 1:1, schéma SVG | semelle, `pages` | via `regenerer` : plan 138,06 × 51,93 |
| `profil.py` | contour sans CAO | semelle | module ; écart au noyau 0,0024 mm ≤ 0,05 |
| `procedes.py` | jointure des quatre tables | `pages`, `regenerer`, semelle | 3 machines · 3 procédés · 5 matières · 6 réglages, dont 2 IMPOSSIBLES |
| `nullites.py` | état d'un `null` | `pages` | 3 à mesurer, 3 à déduire, 0 sans objet |
| `audit_origines.py` | origine de chaque valeur | `regenerer`, `controle_regles` | `--strict` : sortie 0 ; **1 440 valeurs, dont 688 numériques** |
| `controle_depot.py` | règle 4 | `regenerer` | 104 fichiers suivis, aucun binaire, 4 journaux bien datés |
| `controle_regles.py` | règles mortes | `regenerer` | 62 motifs, tous atteints ; rayon minimal conforme sur 6 réglages ; 1 dormante |
| `index_fiches.py` | index engendré | `regenerer` | 44 entrées ; **ignore ses arguments** (`--help` régénère) |
| `empreinte.py` | empreinte du site | `pages`, semelle | `7d61326025`, **identique à `yxor.fr`** (curl, 23 h 44) |
| `check_cad_toolchain.py` | la CAO sort en mm, à l'échelle 1:1 | manuel | **16/16** |
| `import_upstream_limits.py` | butées depuis le MJCF amont | manuel | `--check` : à jour |
| `ckpts_backup.py` | manifeste des poids | manuel | `verify` : 10 conformes, 0 altérées |
| `enveloppes_actionneurs.py` | classes d'actionneurs | manuel | 2 classes (4 + 26 articulations) |
| `ratios_ansur.py` | ratios depuis ANSUR II | manuel | tourne ; **sa colonne « D&C » est fausse** (§ 8, H7) |
| `source.py` | registre des sources | manuel | 8 sources |
| `apercu_svg.py` | PNG d'un schéma | manuel, cité seulement dans le journal | PNG produit et **regardé** : cotes A-F présentes, rien hors cadre |
| `verifier_pages.py` | mesure des pages dans Chromium | manuel | **échoue** : Chromium absent. **Jamais exécuté avec succès.** |

### `parts/` — une pièce

`semelle_apprentissage.py` (508 lignes) : **V**, 8 contrôles OK,
exports STEP, STL, DXF et PDF A4. Relevé de 8 cotes. C'est **la seule
pièce du dépôt**.

### `sim/`

| Fichier | Résultat |
| --- | --- |
| `render.py` | **V** : PNG de `humanoid.xml` en 320 × 240 |
| `view.py` | non lancé (fenêtre) |
| `models/humanoid.xml` | modèle d'exemple DeepMind (Apache 2.0), **pas un modèle YXOR** ; aucun code ne le référence |
| `upstream/toddlerbot_fixes.py` | **V** : refuse de démarrer sous 3.14, message clair, sortie 1 |
| `upstream/replay_policy.py` | **V** sous le venv amont : 1 s de marche, +0,080 m (0,0795 m/s pour 0,10 commandé), **pas de chute**, ×1,05 temps réel |

### `web/` — 4 fichiers

`simulateur.js` (357), `viewer.js` (164), `zoom.js` (134), `style.css`
(279). **Aucun des trois scripts n'a jamais été exécuté** — déclaré par
la passation (**D**), et je n'ai pas non plus de navigateur pour le faire.
Le correctif d'ordre des points du contour a été porté en JS sans être
exécuté (**D**).

### Mort ou jamais appelé

- **Aucune fonction sans appelant** (grep sur chaque `def` et chaque
  `function` ; pyflakes n'est pas installé, donc pas de confirmation
  outillée).
- **Imports inutilisés** (**V** par grep) : `regenerer.py:58` `nullites
  as NU` ; `regenerer.py:43` `svg_schema` ; `regenerer.py:63`
  `etat_procede, e, val` ; `pages.py:36` `ordonner_cotes` (marqué `noqa`).
- `Cotes.besoin()` (`semelle_apprentissage.py:123-142`) : défini, **jamais
  appelé**. C'est la seule voie par laquelle `coupable` vaudrait faux.
- `sim/models/humanoid.xml` : aucun appel de code, cité par la
  documentation seulement.

---

## 4 — Non implémenté

### Répertoires vides

| Répertoire | Contenu | Pourquoi |
| --- | --- | --- |
| `robot/` | `.gitkeep` | **aucune fiche.** Le README l'annonce pour « assemblage, URDF, MJCF ». |
| `bom/` | `.gitkeep` | 0019 renvoie la nomenclature à « quand une pièce aura un montage » (**D**, lecture 0016-0030) |
| `sim/` (hors amont) | seulement les outils du 20/09 | aucune fiche ne prévoit de simulation YXOR |

### Valeurs `null`

**V**, `nullites.py` : 6 `null` qualifiés.

| Clé | État | Fondement |
| --- | --- | --- |
| `actionneurs.P1.modele`, `.couple_nominal_Nm`, `.entraxe_fixation` | non déterminé | `nullites.yaml` ; attend le choix d'actionneur (0038, proposée) |
| `materiaux.{carton_plume, contreplaque, aluminium}.source` | se déduira | `nullites.yaml` |

Les autres `null` (**V**, `grep -c null` : 39 dans `hardware.yaml`, 26
dans `joints.yaml`) passent l'audit strict, donc sont couverts par un
motif. Deux méritent d'être nommés :

- **`reglages.cutter_cartonplume_5.saignee: null`**. C'est pourtant la
  matière publiée, et la saignée a été mesurée (0,0) sur l'ondulé double
  seulement (`hardware.yaml:294`, **V** par la lecture 0016-0030).
- **`carton_ondule_simple`** : vidé de ses valeurs par la 0043, « reste
  à mesurer » (`hardware.yaml:180-186`).

### Promis par une fiche et non faits

| Quoi | Fiche | Raison écrite ? |
| --- | --- | --- |
| origine `norme`, axe `verifiabilite` | 0035 | **oui** : « rien n'est appliqué » |
| accesseur `yxor/cotes.py`, `C.tenue()`, `C.interface()` | 0010, 0013 | **non** |
| propagation d'origine dans un calcul | 0011 | « avant la première pièce qui combine des origines » |
| `rayon_min_geste` | 0042 | proposée |
| variante de la semelle en ondulé | 0044 | proposée |
| troncature des décimales au rang de l'incertitude | 0041 | proposée |
| `decisions/archive/` | 0036 | **non** |
| refus d'une fiche « appliquée » sans date | 0036 | **non** — simple avertissement |
| rang 2 #11 (journal par entrée), rang 3 #12-#14 | 0024 | **non** |
| URDF, MJCF YXOR, nomenclature | README | **non** |
| **ce que le robot doit faire** (cahier des charges) | aucune | relevé comme manquant par l'état des lieux de midi, § 4 — toujours absent |

---

## 5 — Reporté, en veille

| Sujet | Fiche | Déclencheur écrit |
| --- | --- | --- |
| OrcaSlicer, format 3MF | 0032 | l'achat d'une imprimante |
| FreeCAD MCP | 0032 | deux impasses build123d |
| Zoo | 0032 | un échec d'OCCT |
| bd_warehouse | 0032 | « la première pièce qui tient une vis » |
| contraintes d'impression rétablies | CLAUDE.md, 0014 | « si une imprimante est acquise » ; `hardware.yaml:403` dit « Jeremy en achète une cette semaine » (**D**, invérifiable) |
| licence des poids | 0003 | une exploitation commerciale |
| licence LGPL d'OCCT | 0009 | idem |
| topologie du bras en P2 | 0005 | le passage au palier P2 |
| 12 transmissions à engrenage ou différentiel | 0015 | « à instruire une par une » — **pas de déclencheur** |
| boulonner ou souder | 0017, 0022 | **aucun** ; réservé à Jeremy |
| choix de 2, 3 ou 4 classes d'actionneurs | 0038 | l'analyse de la série de couples, qui existe |
| registre des lots de matière | 0043 | un deuxième lot |
| seconde destination de sauvegarde | 0008 | **aucun** ; « à la charge de Jeremy » |
| épaisseur mesurée sans contact | passation | la prochaine session (« la seule mesure qui vaille la peine ») |
| Chromium | journal 29/09 | un fichier à déposer dans `Téléchargements` |

**Trois reports sans déclencheur** : les transmissions, la soudure et la
sauvegarde. **Déd** : un report sans déclencheur est un abandon qui ne
se dit pas. Les deux derniers sont assumés comme décisions de Jeremy.

---

## 6 — Frontière amont

| Ce qui vient de ToddlerBot | Forme | Où | Licence amont |
| --- | --- | --- | --- |
| code (sim, politiques) | **rien de copié** ; exécuté depuis `~/upstream/` | `sim/upstream/` l'importe | MIT |
| correctifs d'exécution | **code YXOR** qui corrige l'usage de l'amont | `toddlerbot_fixes.py` (223 l.) | à Jeremy, écrit contre une API MIT |
| axes, butées, rapports de transmission | **extrait engendré, daté, épinglé** | `upstream_joints.generated.yaml` — 715 valeurs | CC BY-NC-SA (conception) |
| valeurs `amont` de `joints.yaml` | **emprunt tracé**, citant l'extrait | 364 valeurs | idem |
| topologie du bras (noms d'articulations) | **emprunt daté** (0005) | `joints.yaml` — 17 noms | idem |
| H = 0,56 m en P1 | **emprunt daté** (0001, 0011) | `anthropometry.yaml` — 2 valeurs | idem |
| empreintes des poids | **manifeste**, binaires hors Git | `ckpts.manifest.yaml` — 40 valeurs | non tranchée (0003) |
| cadence de marche 0,72 s | citée dans la 0038 | prose | — |

**Total `amont` : 1 121 valeurs sur 1 440, soit 78 %** (**V**, audit du
soir). 715 d'entre elles, soit 64 % de l'amont, sont dans le fichier
documentaire que **aucun code ne lit** (**V** par la cartographie).

### Ce qui est à Jeremy en propre

**V**, audit : 175 valeurs `propre`, 81 `litterature` (ANSUR II et
normes), 46 `mesure`, 17 `catalogue`. S'y ajoutent **tout le code** hors
`sim/upstream/`, la semelle, les quatre tables de fabrication, le site
et l'appareil de traçabilité.

**La seule géométrie produite — la semelle — ne contient aucune cote
`amont`** (**V**, relevé de la pièce : 8 cotes, P2, ratios ANSUR).

### Deux défauts de la frontière

1. **La licence est mal nommée dans CLAUDE.md** (§ 8, H1).
2. **Le contrôle d'interpréteur ne garde qu'un côté** (§ 8, C1).

---

## 7 — Traçabilité

### Les chiffres (**V**, exécutés ce soir)

| Mesure | Valeur |
| --- | ---: |
| valeurs inventoriées | **1 440**, dont 688 numériques |
| origine : amont · propre · littérature · mesure · catalogue | 1 121 · 175 · 81 · 46 · 17 |
| nature : interface · sans_objet · procédé · échelle | 1 113 · 227 · 51 · 49 |
| motifs déclaratifs (`origines` + `nullites`) | 62, tous atteints ; 1 dormant |
| motifs `fourre_tout: true` | 2 (`origines.yaml:318, 330`) |
| sources au registre | 8 : 2 partielles, 6 non lues |
| fichiers suivis contrôlés | 104, aucun binaire |
| **cotes qui gouvernent une géométrie produite** | **8** |

### Ce que ces chiffres ne prouvent pas (**Déd**)

- **« 62 motifs tous atteints » prouve qu'aucune règle n'est morte, pas
  qu'elles sont justes.** La 17ᵉ valeur `catalogue` en est un exemple :
  l'épaisseur mesurée de l'ondulé double est classée « annoncée par un
  fournisseur » par un joker générique (passation, point 3 ; **V**, le
  compte `catalogue` vaut bien 17).
- **Une origine qualifiée n'est pas une origine vérifiée.** Les vis sont
  en `litterature` avec la note « ISO 4762 probable, NON VÉRIFIÉ »
  (`origines.yaml:244`, **V**). L'audit les compte comme qualifiées.
- **1 113 valeurs `interface` sur 1 440** : c'est la nature « ne suit
  jamais H ». Elle est massivement portée par les fichiers amont ; la
  règle 1 (dérive de H) ne s'applique qu'à 49 valeurs.
- **L'audit ne dit rien du robot.** 1 432 des 1 440 valeurs ne
  gouvernent aucune géométrie.
- **L'empreinte ne couvre ni `requirements.txt` ni le `Dockerfile`**
  (`empreinte.py:42`, **V**). Une montée de version de build123d
  laisserait l'empreinte inchangée.
- **Les chiffres d'exemple de CLAUDE.md sont périmés** : « 682
  numériques », « 1431 » — l'audit mesure 688 et 1 440. C'est la règle 3
  de CLAUDE.md appliquée à CLAUDE.md lui-même.

### Vérifiabilité des règles

L'état des lieux de midi comptait 30 règles, dont 15 outillées. Depuis,
quatre règles ont rejoint CLAUDE.md, et j'y trouve **trois affirmations
d'outillage fausses** (C1, C2, C3 au § 8). **Déd** : on ne peut plus
reprendre tel quel le chiffre « 50 % d'outillées ».

### Tests

**Il n'y a aucun test automatisé** (**V** : aucun fichier `test*`, pas
de `pytest` dans `requirements-dev.txt`, qui ne contient que Playwright).
Les contrôles sont des assertions exécutées dans `regenerer.py` sur
l'état courant. Ils ne portent sur aucun cas limite, et **aucun contrôle
n'a de test qui prouve qu'il échoue**. La seule exception est déclarée
dans le journal : le faux `2026-12-25.md`, testé à la main une fois (**D**).

---

## 8 — Diagnostic

Classé par gravité. **Rien n'est appliqué.** Chaque ligne propose.

### Critique — un contrôle ou un texte affirme une protection qui n'existe pas

| # | Constat | Preuve | Proposition |
| --- | --- | --- | --- |
| **C1** | CLAUDE.md : « les deux sens sont vérifiés à l'exécution ». **Seul `sim/upstream/` vérifie.** Le code YXOR lancé sous le venv amont tournerait avec MuJoCo 3.3.4 sans rien dire — l'échec silencieux que la règle voulait empêcher. | **V** : aucun `version_info` ni `sys.executable` dans `scripts/`, `parts/`, `sim/*.py` | garde symétrique dans un module commun, ou corriger la phrase |
| **C2** | Règle d'achat (a) : « `regenerer.py` peut le refuser ». **Rien ne refuse.** De plus, `coupable` est vrai dès qu'une pièce se construit : son seul chemin vers faux, `c.besoin()`, n'est appelé nulle part. | **V** grep ; passation | écrire « affiché, non opposé » tant que ce n'est pas le cas |
| **C3** | `regenerer.py:399` appelle `index_fiches.main()` **sans lire son code de retour**. Une fiche hors convention passe la commande unique en vert. | **V** l. 393-399 | tester le retour comme les deux voisins |
| **C4** | `index_fiches.champ()` ne lit que **la première** ligne « Amendée par ». La 0015 en a deux : l'amendement par la 0016 disparaît de la colonne que l'index dit « la plus importante ». | **V** `index_fiches.py:47-52`, `0015:8-9` | lire toutes les occurrences |
| **C5** | **Le site publie la semelle en carton-plume 5 mm**, alors que le seul objet coupé l'a été en ondulé double de 3,5 mm. Aucune mention sur la page. | **V** relevé : `reglage: cutter_cartonplume_5` ; page pièce : 0 occurrence de « ondul » | la recommandation D de la 0044 |

### Haute — faux dans le texte, ou divergence non déclarée

| # | Constat | Preuve | Proposition |
| --- | --- | --- | --- |
| **H1** | CLAUDE.md:246 : mécanique amont « en **CC BY-NC** ». L'amont dit **CC BY-NC-SA**. La nuance compte : **SA est la clause de réciprocité**, donc cette licence relève des **deux** familles du tableau de CLAUDE.md, pas d'une seule. | **V** `~/upstream/toddlerbot/README.md:167` | corriger, et relire la 0029 à cette lumière |
| **H2** | `ckpts.manifest.yaml:7` : « deux destinations ». La 0008 dit qu'une seule existe. | **V** | aligner sur la fiche |
| **H3** | `anthropometry.yaml:19-25` : « Drillis & Contini, NON VÉRIFIÉES », alors que 12 des 14 ratios sont ANSUR `verifie: true`. | **V** | réécrire l'en-tête du bloc |
| **H4** | Amendements sans renvoi : 0012 ← 0034, 0020 ← 0033, 0028 ← 0035. `index_fiches` ne contrôle pas la réciprocité. | **V** 0012 ; **D** pour 0020 et 0028 (lectures) | contrôle de réciprocité |
| **H5** | Des fiches **proposées** sont déjà appliquées en partie : 0038 (série de couples), 0041 (5 mesures, vocabulaire élargi). La densité a été déplacée **sans fiche**. Règle 5 dans les deux cas. | **V** exécution de `replay_policy` : le CSV est écrit | trancher 0038 et 0041, ou dire ce qui a été appliqué par anticipation |
| **H6** | La 0036 définit 3 espèces ; `index_fiches.py:27` en accepte 6, et son commentaire dit « cinq espèces, six états ». `close`, `veille` et `abandonnee` sont des états. | **V** | une fiche qui tranche la taxonomie |
| **H7** | `ratios_ansur.py` affiche une colonne « D&C » qui lit **l'`anthropometry.yaml` actuel**, donc ANSUR : l'écart affiché vaut 0 % **par construction**. La comparaison avec Drillis & Contini est perdue sans que rien ne le signale. | **V** exécution ; `ratios_ansur.py:248-250` | figer les valeurs D&C dans le script, ou renommer la colonne |
| **H8** | Le statut de la 0024 dit « rangs 2 et 3 non entamés » ; #8, #9 et #10 sont faits. La duplication n° 1 (`simulateur.js:149-150` contre `plan_decoupe.py:237-244`) subsiste sans garde. | **D** (lecture 0016-0030, avec lignes) | — |
| **H9** | 0010 promet `yxor/cotes.py` et le refus d'une mauvaise origine ; ni l'un ni l'autre n'existent. | **V** `ls yxor` : absent | amender 0010 : l'accesseur est local et ne refuse rien |
| **H10** | L'empreinte ignore `requirements.txt` et le `Dockerfile`. | **V** `empreinte.py:42` | les ajouter à `SOURCES` |

### Moyenne — textes périmés, identifiants restés

- **« Simple cannelure » à tort, deux endroits** : `journal/2026-09-29-nuit.md:8`,
  `decisions/0026:98` (**V** grep). Les autres occurrences sont légitimes.
- **L'état des lieux de midi est cité par le README comme l'état
  courant.** Il porte 136,80 × 49,50 mm (aujourd'hui 138,06 × 51,93),
  « 33 fiches », « NE PAS COUPER » et « rayon vérifié pour le seul
  réglage » — tous périmés (**V**).
- **Documents fantômes** cités sans renvoi de résolution : `docs/00-cadrage`
  à `03-artefacts`, « LOG-1 », « phase 1 étape B » — dans 0005, 0006,
  0009 et 0014 (**D**, lecture).
- **Clés `hardware.yaml` disparues** citées par 0014, 0015, 0018
  (`decoupe_metal`) et 0026 (`cutter_carton`) : conservées en commentaire
  (`hardware.yaml:8, 380-395`), donc traçables.
- **Comptes internes faux** : 0036 « 40 fiches » (44) ; docstring
  d'`index_fiches` « 23 fiches » ; `sources.yaml` « neuf documents » (8) ;
  0033 « 9 règles » (14) ; 0032 cinq ou quatre pistes ; 0043 cite
  `alu_tole_6`, inexistant ; 0041 porte des valeurs d'avant la repesée.
- **0039 cite Bennehar comme décrivant un montage**, alors que
  `sources.yaml` le déclare `non_lu`. C'est le cas exact que la 0040
  interdit.
- **0017 et 0022 se contredisent** sur la vérification de « quatre
  pièces soudées » (**D**, lecture).
- **0018 prescrit three.js** ; le code l'écarte sans amendement.
- **« Cinq identités »** de `joints.yaml` attribuées à la 0007
  (`joints.yaml:7`) et à la 0013 (`0015:73`) ; aucune ne les définit.
- **`controle_depot.controler_fournisseurs`** : `if not f.exists():
  return []` (**V**, l. 112) — un saut muet, contraire à la règle 1 des
  contrôles.
- **Qualification `catalogue`** de l'épaisseur de l'ondulé double
  (passation, point 3).
- **Nature `sans_objet`** : 227 valeurs, définie par aucune fiche ;
  `tenue`, définie par la 0013, n'est jamais employée.
- **`sim/render.py` et `view.py`** ne disent pas sous quel venv se
  lancer (« `python sim/…` »).

### Basse

- Imports inutilisés (§ 3).
- Signature `c.reglage(rid, cle)` contre `c.reglage(machine, matiere)`
  dans la 0026.
- CERN-OHL-W omise du tableau de CLAUDE.md.
- `index_fiches.py` ignore ses arguments.
- Le journal : **6 802 lignes** (**V**) ; la passation dit « ~6 000 ».

### Dates

**V** : aucun commit ni aucune fiche n'est daté hors du 20, du 28 et du
29 septembre. L'erreur de la nuit — un journal nommé au 30 septembre —
est corrigée (`124f7d1`), et `controle_depot` refuse désormais un journal
daté du futur. **Constat de cet audit : 44 fiches tiennent en 3 jours
calendaires, dont 25 le même jour.**

---

## 9 — Questions ouvertes et pistes

### Avec une fiche

| Question | Fiche |
| --- | --- |
| rayon de matière ou rayon de geste — et d'où vient `0,5 × épaisseur` ? | 0042 |
| tronquer les décimales au rang de l'incertitude | 0041 |
| variante ondulé de la semelle, et quoi afficher en attendant | 0044 |
| dimensionnement thermique, 2, 3 ou 4 classes | 0038 |
| boulonner ou souder | 0022 |
| origine `norme`, application | 0035 |

### Sans fiche

1. **Que doit faire le robot ?** Aucun document ne le dit. L'état des
   lieux de midi l'avait déjà relevé comme « le seul document manquant
   qui manque vraiment ». C'est toujours vrai.
2. **Double cannelure fine ou carton comprimé ?** La passation juge
   l'hypothèse « double fine » au moins aussi plausible, ce qui ferait
   tomber la mention « borne haute » de la densité. Pas de fiche. La
   mesure sans contact tranchera.
3. **Les choix de colonnes ANSUR** (`tibialheight`,
   `trochanterionheight`) et leurs alternatives, jamais discutés
   (passation).
4. **Le rendu de contrôle** est jugé à l'œil, sans critère écrit
   (passation). CLAUDE.md l'exige, mais aucune méthode n'existe.
5. **Chromium** : constat sans diagnostic (passation).
6. **BY-NC-SA contre BY-NC** : la clause SA change-t-elle quelque chose
   pour les 364 valeurs `amont` de `joints.yaml`, qui ne sont pas un
   fichier amont mais une œuvre dérivée ? (**Déd**, § 8 H1.)
7. **Le palier P2 est-il le bon pour la première pièce ?** La semelle
   est dessinée en P2 pour contourner la propagation d'origine (0011) ;
   le robot à construire est P1.
8. **Faut-il un test qui prouve que chaque contrôle sait échouer ?** Les
   trois fautes C1 à C3 auraient été trouvées ainsi.

---

## 10 — Proportion

### Par fichier suivi (**V**, `wc -l` sur les 104 fichiers)

Le classement par fichier est **Déd** ; un fichier mixte est rangé selon
sa fonction dominante.

| Catégorie | Fichiers | Lignes | Part |
| --- | ---: | ---: | ---: |
| **Robot** — pièce, profil, plan de découpe, sim, `anthropometry`, `joints`, `hardware`, `mesures`, outils d'extraction et CAO | 24 | 5 479 | **23,0 %** |
| Publication — site, générateur, Docker, web | 12 | 2 527 | 10,6 % |
| Gouvernance — audit, contrôles, index, origines, nullités, sources, fournisseurs, CLAUDE.md, états des lieux | 19 | 3 076 | 12,9 % |
| Fiches | 45 | 5 887 | 24,8 % |
| Journal | 4 | 6 802 | 28,6 % |
| **Total** | **104** | **23 771** | |

**Gouvernance au sens large** (gouvernance + fiches + journal) :
**15 765 lignes, 66 %**. Le robot : 23 %.

Et à l'intérieur de « robot », **le code qui produit de la géométrie**
tient en trois fichiers : `semelle_apprentissage.py`, `profil.py` et
`plan_decoupe.py`, soit **1 058 lignes, 4,5 % du dépôt**. Sur les
5 479 lignes « robot », 1 115 sont des données amont engendrées ou
reprises (`upstream_joints.generated.yaml`, `joints.yaml`).

### Par fiche (**Déd**, classement par sujet)

- **Robot** (mécanique, fabrication, simulation, matière) — 19 : 0001,
  0002, 0003, 0005, 0008, 0009, 0012, 0014, 0015, 0016, 0017, 0022, 0031,
  0034, 0038, 0039, 0042, 0043, 0044.
- **Structure des données de fabrication** — 4 : 0021, 0026, 0033, 0041.
- **Gouvernance, traçabilité, site** — 21 : 0004, 0006, 0007, 0010, 0011,
  0013, 0018, 0019, 0020, 0023, 0024, 0025, 0027, 0028, 0029, 0030, 0032,
  0035, 0036, 0037, 0040.

### Par contrôle (**V**, sorties de ce soir)

- **Portent sur le robot** : 8 contrôles de la pièce, 16 de la chaîne
  CAO, le rayon minimal sur 6 réglages, la concordance JS/CAO, `--check`
  de l'extraction amont, `verify` des poids. **Tous portent sur une seule
  pièce ou sur l'outillage.**
- **Portent sur le dépôt** : audit strict, règle 4 et ses trois
  sous-contrôles, 62 motifs, index des fiches, structure HTML, feuille de
  style.

À peu près autant de contrôles de chaque côté. Mais ceux du robot
vérifient **une** semelle, et ceux du dépôt vérifient **1 440** valeurs.

### Mon avis

**La proportion est déséquilibrée, et le déséquilibre s'aggrave.** Le
matin du 29, la prose faisait 54 % du dépôt ; ce soir, fiches et journal
en font 53 % à eux seuls. Entre les deux états des lieux, on a ajouté
3 788 lignes de prose pour 2 132 de code.

**Mais la gouvernance n'est pas du bruit.** Elle a attrapé de vraies
fautes : le contour faux depuis trois jours, la date du journal, le
plan de découpe périmé servi par le cache. Ce sont des fautes qui
auraient coûté une pièce ratée.

**Le problème est ailleurs** : **la gouvernance se vérifie mal
elle-même.** Cet audit trouve cinq défauts critiques, et **tous les cinq
sont dans l'appareil de contrôle**, aucun dans la semelle. La couche qui
devait empêcher les « verts volés » en produit, parce qu'elle a grossi
plus vite qu'on ne la testait.

**Déd, franchement** : chaque nouvelle règle coûte désormais plus
qu'elle ne rapporte tant que les existantes ne sont pas testées. Le
dépôt gagnerait davantage à une deuxième pièce — une qui s'emboîte, pour
que `saignee`, `besoin()` et `coupable` servent enfin à quelque chose —
qu'à une 45ᵉ fiche.

---

## 11 — Lecture pour Jeremy

Dans l'ordre, une phrase chacune.

1. **0001 — ToddlerBot comme base** : d'où part le projet, et pourquoi un
   robot existant plutôt qu'une page blanche.
2. **0014 — Il n'y a pas d'imprimante 3D** : la contrainte matérielle qui
   a tout réorienté.
3. **0015 — Plaques et entretoises** : le seul vrai choix d'architecture
   mécanique ; le reste en découle.
4. **0010 — Origine des cotes** : le contrat de traçabilité, d'où vient
   chaque nombre et pourquoi la licence amont y oblige.
5. **0013 — Nature des cotes** : pourquoi une épaisseur ne grandit pas
   avec le robot — la notion mécanique la plus importante du dépôt pour
   un débutant.
6. **0026 — Quatre tables** : comment machine, procédé, matière et
   réglage s'articulent (lire la 0033 juste après si l'on doit y toucher).
7. **0043 — Deux matières ou une** : ce que la première pièce coupée a
   appris, et comment une mesure réelle a démenti le dépôt.
8. **0044 — La semelle publiée n'est pas celle qui a été coupée** : l'état
   exact où l'on s'est arrêté.

**Différence avec le parcours de `decisions/index.md`** : celui-ci
commence par la méthode (0010, 0013, 0020…). Je propose de commencer par
le robot (0001, 0014, 0015), parce que la méthode ne se comprend qu'une
fois qu'on sait à quoi elle sert.
