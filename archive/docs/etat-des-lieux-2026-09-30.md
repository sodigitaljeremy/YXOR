# État des lieux — 2026-09-30

**Commencé le mercredi 2026-09-30 à 21 h 49 CEST**, heure lue par `date`
avant toute autre commande. Dépôt au commit `aa5a6e0`. Un seul fichier non
suivi : `docs/conclusion-arbitrages-2026-09-30.md`.

**Ce document ne corrige rien.** Il ne crée aucune fiche et ne change aucun
paramètre. Les commandes exécutées ont écrit dans `exports/` et `site/`
(ignorés tous les deux) et dans le dossier temporaire de la session.
`index_fiches.py` a réécrit `decisions/index.md` à l'identique. Avant
comme après, `git status` ne montrait que le fichier non suivi.

Deux écritures involontaires, signalées :

- `enveloppes_actionneurs.py --help` **ignore son argument**. Il a réécrit
  `exports/actionneurs/couples_balancement.csv` et `enveloppes.json`.
- La série de référence `marche_15s.csv` **n'a pas été touchée** : son
  sha256 vaut toujours `3de8ca2050a16667…` (**V**).

## Légende

| Marque | Sens |
| --- | --- |
| **V** | lu ou exécuté pendant cet audit, avec `fichier:ligne` ou commit |
| **DÉCLARÉ** | le dépôt l'affirme ; non revérifié |
| **DÉD** | mon raisonnement, à discuter |

Statut d'une décision, lu dans le texte du dépôt : **DÉCIDÉ** (par Jeremy),
**PROPOSÉ**, **OUVERT**, **ABANDONNÉ**.

**Méthode.** J'ai lu moi-même :

- CLAUDE.md, le README, le cadrage et la conclusion ;
- l'index, les fiches 0047 à 0052, le rapport de la nuit du 29 ;
- les documents d'actionnement, `budget.yaml`, `criteres_selection.yaml`
  et `actionneurs.yaml` (en partie) ;
- les scripts de choix.

Trois lectures parallèles ont couvert le reste : les fiches 0001 à 0024,
les fiches 0025 à 0046, et le journal du 30 lu en entier. Leurs constats
gardent leur preuve `fichier:ligne`. **J'ai revérifié moi-même chaque
constat classé critique ou haut au § 8.**

---

## 1 — Résumé

1. **YXOR n'a toujours qu'une pièce** : une semelle d'apprentissage en
   carton, dessinée au palier P2 (0,90 m). Ce palier est abandonné depuis
   ce matin.
2. **Le 30-09, le projet a changé d'axe.** La classe d'actionneur fixe
   désormais la taille (0047). Le premier robot est **S**, vers
   0,55-0,60 m (0048). La marge vaut 1,5 (0051) et la fabrication est
   séquencée (0050). Tout cela est **DÉCIDÉ**.
3. **La famille d'actionneurs de S n'est pas décidée.** Damiao est
   **RECOMMANDÉ** (conclusion § 4.1). Les poids du comparatif, eux, sont
   **DÉCIDÉS**.
4. **Le banc est PROPOSÉ**, et sa composition diverge selon le document :
   2 × RS05, qualification, 2 × J4310, ou trois options ex æquo.
5. **Constat le plus grave (§ 8, K1).** La famille Damiao a été **notée
   sur la variante 24 V**, alors que la recommandation porte sur la
   **48 V**. Recalculée en 48 V, la bascule passe de k ≈ 0,49 à
   k ≈ 0,61-0,62.
6. **Conséquences du K1** :
   - le verdict « vérification, pas départage » ne tient plus qu'à
     **0,009** ;
   - le critère d'abandon de 1,75 N·m devrait être d'environ
     **2,14-2,17 N·m**.
7. **La sécurité du banc est dite, pas résolue.** Aucune alimentation
   chiffrée n'a de limitation de courant réglable.
8. **CLAUDE.md dit encore « procédé unique : la découpe 2D »** et
   « concevoir au carton ». Il ne nomme ni le cadrage, ni S, ni le banc.
9. **Aucune fiche n'est formellement remplacée.** Les fiches 0001, 0005,
   0011, 0014 et 0015 sont contredites par celles du 30-09. Aucun en-tête
   « Remplacée par » n'existe.
10. **Tous les contrôles passent** (**V**) :
    - `regenerer.py` : sortie 0 en 26 s, 1 pièce, 5 pages ;
    - audit strict : 3 035 valeurs, dont 978 numériques ;
    - règles : 125 motifs ;
    - tests : 9 sur 9 (**sous unittest** ; pytest n'est pas installé).
11. **Le dépôt est égal au site** : `de10401722`, lu sur yxor.fr
    (**V**).
12. **La gouvernance au sens large recule** : 66 % → 57 % des lignes. Mais
    la croissance du 30-09 est allée à l'**aide à la décision**
    d'actionneur (19 %). Le code qui produit de la géométrie reste à
    3 %.
13. **Ce qui bloque** : le choix de famille, donc le banc, donc toute
    conception mécanique de S.
14. **Prochaine action.** Recalculer le comparatif des familles avec le
    J4310 **48 V** comme membre S, et réécrire le critère d'abandon avant
    toute validation du § 4 de la conclusion.
15. **Ensuite**, décision de Jeremy seul : l'alimentation du banc, qui
    est un outillage.

---

## 2 — Chronologie

Source : `git log`, **128 commits** (**V**). Répartition par jour : 7 le
20-09, 21 le 28, 31 le 29 et **69 le 30** (**V**). Les jalons 0 à 8
reprennent le rapport de la nuit (**DÉCLARÉ**). Les jalons 9 à 16 viennent
du journal du 30, avec les heures des commits (**V**).

| # | Jalon | Quand | Commits clés | Ce qui arrive |
| --- | --- | --- | --- | --- |
| 0 | Socle | 20/09, 20 h 14 | `353c6cb` | arborescence, CLAUDE.md, 0001 |
| 1 | Simulation | 20/09, jusqu'à 23 h 41 | — | MuJoCo, ToddlerBot épinglé (0002), politique ONNX (0003) |
| — | pause | 21-27/09 | **0** | rien n'en est dit |
| 2 | Données amont | 28/09, 12 h-14 h | — | 0004 à 0009 |
| 3 | Traçabilité | 28/09, 16 h 49-17 h 34 | — | 0010 à 0013 |
| 4 | Pivot fabrication | 28/09, 18 h-19 h 42 | — | 0014 à 0017 : pas d'imprimante, plaques |
| 5 | Site | 28/09, 20 h 38-22 h 54 | — | 0018, 0019, Dockerfile |
| 6 | Structures | 29/09, 9 h-12 h 21 | `80daa46` | 0020 à 0033, premier état des lieux |
| 7 | Faux verts, déploiement | 29/09, 13 h-17 h 39 | — | 0034 à 0040, empreinte |
| 8 | Premier objet | 29/09, 22 h 37-23 h 33 | `8e1bee2` | semelle coupée, 0041 à 0044 |
| — | Audit de nuit | 29/09, 23 h 50 | `0572e7e` | état des lieux « nuit » |
| 9 | Reconstruction par IA | 30/09, 00 h 02 | `afb7869` | 0045 et 0046 : Backflip vérifié, pas adopté |
| 10 | **Lot A** | 30/09, 00 h 05-00 h 41 | `4089438` à `c062cc6` | correctifs de l'audit ; premiers tests ; construction déterministe ; empreinte sans Dockerfile |
| — | **trou** | 30/09, 00 h 41-13 h 27 | **0** | le journal n'en dit rien |
| 11 | Carton clos | 13 h 27-13 h 29 | `8fe2c37`, `efd5a63`, `378d4a8` | 0042 et 0044 closes, caractérisation arrêtée |
| 12 | Actionnement P2 | 13 h 54 | `a002546` | premier chiffrage des couples |
| — | trou | 13 h 55-17 h 10 | **0** | non commenté |
| 13 | **Démarche inversée** | 17 h 10-17 h 33 | `d6a00a0`, `00af03a` | enregistreur de marche, `dimensionnement.py` |
| 14 | **Cadrage** | 17 h 40-18 h 12 | `ea05593`, `7e224e9`, `87a6ab4` | cadrage versé ; 0047 à 0052 |
| 15 | **Comparatifs v1 → v3** | 18 h 27-20 h 55 | `63aadc8`, `b01342a`, `ef4c3ec`, `bd01b5f` | étude fournisseurs ; familles ; poids **fixés** (S) ; poids du banc « fixés » |
| 16 | **Corrections et vérification** | 21 h 04-21 h 34 | `ef03734`, `f4a14f4`, `62deecf`, `35fe0c3`, `aa5a6e0` | poids du banc remis à « proposé » (attribution erronée) ; estimation thermique ; règle de décisivité ; critère d'abandon |

**Trois trous sans explication** : du 21 au 27/09, puis le 30/09 de
00 h 41 à 13 h 27 et de 13 h 55 à 17 h 10 (**V**, `git log` ; le journal
n'en dit rien).

Deux remarques sur le journal (lecture du journal) :

- la section « nuit » (`journal/2026-09-30.md:1657`) ne porte aucune
  heure et n'est précédée d'aucun séparateur ;
- elle correspond aux commits de 21 h 25 à 21 h 34 : ce n'est pas la
  nuit.

**Débit du 30-09** (**V**, `git diff --stat 0572e7e HEAD`) : 53 fichiers,
+9 910 lignes, 8 fiches, 9 tests.

---

## 3 — Décisions

### 3.1 Les 52 fiches

L'espèce et l'état sont lus dans `decisions/index.md`, régénéré à
l'identique (**V**). Répartition :

- **par espèce** : gouvernante 14, close 20, historique 12, proposition 3,
  veille 2, abandonnée 1 ;
- **par état** : appliquée 33, amendée 7, acceptée 5, proposée 2,
  veille 2, instruction 1, abandonnée 1, archivée 1.

| # | Espèce · état | Ce qu'elle décide | Amende / amendée par | Écart signalé (**V** sauf mention) |
| --- | --- | --- | --- | --- |
| 0001 | historique · appliquée | ToddlerBot comme base ; P1 = H = 0,56 m | — | **contredite par 0048 sans renvoi** ; corps réécrit le 30/09 (`4089438`, 17 lignes insérées au milieu) |
| 0002 | close · appliquée | amont figé à `e337f3b`, deux venvs | — | — |
| 0003 | historique · appliquée | 10 archives ONNX | — | `ckpts_backup verify` : 10 conformes |
| 0004 | gouvernante · appliquée | seul `sim/upstream/` tourne sous l'amont | — | **son corps (l. 63-64) dit « les deux sens contrôlés »** ; CLAUDE.md dit le contraire depuis le lot A |
| 0005 | close · amendée | topologie du bras « pour P1 » | ← 0011 | cadre P1 caduc (0048), non remplacée |
| 0006 | close · appliquée | fichier engendré commité | — | renvoi mort « LOG-1 » |
| 0007 | close · appliquée | Onshape n'est pas une source | — | vocabulaire `releve_onshape` jamais employé |
| 0008 | close · appliquée | manifeste des poids, deux destinations | — | `ckpts.manifest.yaml:7` dit « deux » ; la fiche en reconnaît une |
| 0009 | close · amendée | build123d 0.13.0 | ← 0029 | `check_cad_toolchain` : 16/16 |
| 0010 | gouvernante · amendée | origine de chaque cote ; accesseur `yxor/cotes.py` | ← 0011 | `yxor/` absent ; renvois de ligne vers 0001 faux |
| 0011 | close · appliquée | origine `litterature` ; « dessiner en P2 » | → 0010, 0005 | filiation par palier caduque (0048) |
| 0012 | historique · appliquée | sources d'anthropometry | (← 0034 sans renvoi) | réciprocité absente |
| 0013 | gouvernante · appliquée | nature des cotes ; règle 1 restreinte | — | nature `tenue` : 2 valeurs (audit) |
| 0014 | historique · appliquée | l'impression 3D sort du périmètre | — | **contredite par 0050**, non remplacée |
| 0015 | close · amendée | plaques et entretoises, découpe 2D seule | ← 0042, 0016 | **contredite par 0050**, non remplacée |
| 0016 | historique · amendée | « aucun précédent » (barré) | ← 0017 | — |
| 0017 | historique · appliquée | MEVITA : un précédent en tôle | → 0016 | « usinage : non » contredit par 0050 |
| 0018 | gouvernante · appliquée | site statique engendré ; three.js | — | `viewer.js` en WebGL brut, sans amendement |
| 0019 | close · amendée | site catalogue | ← 0037 | — |
| 0020 | gouvernante · appliquée | trois états du `null` | (← 0033 sans renvoi) | limite « clé sœur » levée par le code (`nullites.py:56`), qui l'attribue à 0033 ; or 0033 dit le contraire (0033:110) |
| 0021 | abandonnée | clé composée | ← 0026 | — |
| 0022 | historique · instruction | soudure, sans décision | ← 0031 | — |
| 0023 | close · appliquée | simulation dans le navigateur | — | JS jamais exécuté (DÉCLARÉ) |
| 0024 | close · appliquée | audit, plan en trois rangs | — | statut « rangs 2 et 3 non entamés » faux |
| 0025 | close · appliquée | mobile d'abord | — | `style.css:205, 244-248` |
| 0026 | close · amendée | quatre tables | ← 0033 | l. 98 « simple cannelure » |
| 0027 | close · appliquée | règle d'achat a/b/c | — | (a) non outillée ; la fiche dit encore « critère vérifiable » (l. 118) |
| 0028 | historique · appliquée | quatre affirmations | (← 0035 sans renvoi) | — |
| 0029 | historique · appliquée | trois familles de licences | → 0009 | **son corps dit encore « CC BY-NC »** (l. 65, 79) |
| 0030 | gouvernante · appliquée | fichiers fournisseurs, six champs | — | **3 entrées ; les documents constructeurs du 30-09 n'y sont pas** (§ 8, H6) |
| 0031 | historique · appliquée | torsion calculée, jamais stockée | → 0022 | — |
| 0032 | veille | cinq pistes | — | « cinq » (l. 1) contre « quatre » (l. 20) |
| 0033 | gouvernante · appliquée | épaisseur = champ | → 0026 | — |
| 0034 | historique · appliquée | ANSUR II | → 0012 | — |
| 0035 | proposition · acceptée | origine `norme`, axe `verifiabilite` | — | rien d'appliqué, et la fiche le dit |
| 0036 | close · appliquée | espèce, état, `archive/` | — | 3 espèces dans la fiche, 6 dans le code ; `archive/` absent ; « 40 fiches » |
| 0037 | close · appliquée | verdict par pièce | → 0019 | `c.besoin()` jamais appelé ; garde-fou de largeur absent |
| 0038 | **proposition · proposée** | la température limite, pas le couple | — | **appliquée de fait** (RMS, série, estimation thermique), jamais acceptée |
| 0039 | historique · appliquée | semelle porte-capteurs | — | cite Bennehar (`non_lu`) ; le cadrage aussi (`cadrage.md:437`) |
| 0040 | gouvernante · appliquée | registre des sources | — | 8 sources : 2 partielles, 6 non lues |
| 0041 | **proposition · proposée** | incertitude des mesures | — | appliquée au-delà de son statut ; `protocole-banc.md:201-202` la dit « décidée » |
| 0042 | close · **archivée** | rayon matière ou geste, close sans trancher | → 0015 | « archivée » sans `archive/` ; en-tête substitué le 30/09 |
| 0043 | close · appliquée | ondulé simple et double sont deux matières | — | renvoi mort `alu_tole_6` |
| 0044 | close · appliquée | close sans variante ; la page dit ce qui a été coupé | — | **C5 corrigé** (page pièce : « ondul » présent) |
| 0045 | gouvernante · acceptée | aucune géométrie amont dans un outil de reconstruction | découle de 0010, 0029 | non outillée, et dite telle |
| 0046 | veille | Backflip vérifié, pas adopté | découle de 0045 | rien de créé (dit) |
| **0047** | gouvernante · appliquée | **la classe d'actionneur fixe la taille** | — | **écrite après l'application** (l. 36) ; ne nomme pas 0001 |
| **0048** | gouvernante · acceptée | **tailles Banc/S/M/L/XL ; premier robot S** | découle de 0047 | **non appliquée** dans `anthropometry.yaml` (dit) ; classes de S listées sans Damiao |
| **0049** | close · appliquée | scripts de chiffrage versionnés | — | écrite après l'application (l. 30) |
| **0050** | gouvernante · acceptée | **usinage, puis impression, puis hybride** | — | **contredit 0014, 0015 et CLAUDE.md**, et le dit ; rien d'appliqué |
| **0051** | gouvernante · appliquée | **marge 1,5**, à revoir après le banc | — | `actionneurs.yaml` : `dimensionnement.marge` |
| **0052** | gouvernante · acceptée | **actionneur maison** en parallèle | — | 4 modalités ; le cadrage § 8 en compte 5 |

### 3.2 Registre du cadrage § 12 (**V**, `docs/cadrage.md:450-469`)

Le registre compte 16 lignes, dont une barrée.

- **Décidées par Jeremy (12)** :
  - double cannelure ;
  - carton arrêté ;
  - moratoire rejeté ;
  - principe du lot A ;
  - empreinte sans le Dockerfile ;
  - date d'extraction conservée ;
  - fabrication séquencée ;
  - démarche inversée ;
  - tailles et premier robot S ;
  - scripts versionnés ;
  - actionneur maison ;
  - marge 1,5.
- **Décidé, sans fiche** : les poids du comparatif.
- **Proposées** : « pour la v1, on achète » et la vision.
- **Retirée** : les poids du banc (attribution erronée).

### 3.3 Anomalies

**Fiches contredites par une plus récente sans être remplacées (V)** :

- **0001, 0005 et 0011** : le palier P1 et la filiation de H. La 0048
  laisse les paliers « jusqu'à une fiche qui remplace » (question 8).
  **Aucune fiche n'a jamais décidé P2 = 0,90 ni P3 = 1,70.** Seul P1 a
  une fiche (0001:55) : la « fiche qui remplace » n'a qu'une cible
  formelle (lecture 0001-0024).
- **0014 et 0015** : contredites par la 0050, qui le déclare (question 9).
- **0038** : dépassée en substance par 0047 et 0051. Aucune des fiches
  0047 à 0052 ne la cite.
- **Dans tout `decisions/`, aucun en-tête « Remplacée par »** : le
  mécanisme n'existe pas.

**Fiches réécrites après acceptation (V, `git diff`)** :

- **0001**, le 30/09 : correction de licence **insérée au milieu du
  corps**. Effet de bord : les renvois « ligne 24 / 36 » de 0010 et 0011
  sont décalés.
- **0042 et 0044**, le 30/09 : en-tête **substitué** ; section de clôture
  **ajoutée à la fin**, datée.
- **Plus anciennes** : lignes Statut remplacées dans 0004, 0013, 0018,
  0019, 0020, 0021 et 0024 (commits `2c70ada`, `fc05929`, `17e80b3`).
- La question 10 du cadrage (immuabilité) **n'est pas tranchée**.

**Écrites après l'application, en contradiction avec la règle 5 (V, dit
par elles-mêmes)** : 0047 (l. 36) et 0049 (l. 30).

**Décisions sans fiche** :

- **DÉCIDÉ, V** :
  - les poids du comparatif S et familles (`criteres_selection.yaml:223-329`) ;
  - la règle de décisivité étendue (`criteres_selection.yaml:185`, « réponse de Jeremy : oui ») ;
  - le RS02 retenu à 6 N·m (`journal/2026-09-30.md:523`) ;
  - la correction de la note du J4310 (`actionneurs.yaml:231`) ;
  - le principe du lot A ;
  - l'empreinte sans le Dockerfile.
- **Plus anciens** : WebGL au lieu de three.js ; densité déplacée.
- **DÉD** : la famille d'actionneurs et le banc sont des décisions
  structurantes. Il leur faudra une fiche **avant** application (règle 5).
  Le cadrage le prévoit (« pas de fiche d'ici là »).

**Fiches sans application** :

- 0035 ;
- 0038, formellement ;
- 0045 et 0046 (non outillées, dit) ;
- 0048 (paramètres inchangés) ;
- 0050 (rien) ;
- 0052 (rien de conçu) ;
- 0036, pour `archive/` ;
- 0010, pour l'accesseur ;
- 0037, pour le garde-fou de largeur.

---

## 4 — Les arbitrages du 30-09

| Arbitrage | Statut dans le dépôt | Document source | Chiffres clés |
| --- | --- | --- | --- |
| **Démarche inversée** | **DÉCIDÉ**, appliqué (0047) | cadrage § 3 ; `scripts/dimensionnement.py` ; `docs/dimensionnement-par-actionneur.md` | marche ToddlerBot : 15 s, 751 pas, 0,106 m/s ; **9 actionneurs de jambe sur 12 écrêtés** (jusqu'à 17 %) : tailles = **plafonds optimistes** |
| **Tailles** Banc, S, M, L, XL ; premier robot S | **DÉCIDÉ**, non appliqué dans `params/` (0048) | cadrage § 6 | S ≈ 0,55-0,60 m (cadrage:197), **0,55-0,65 m dans la conclusion** (l. 22) ; M ≈ 0,8 ; L ≈ 0,9 ; XL > 1 m |
| **Marge** | **DÉCIDÉ** : 1,5, à revoir après le banc (0051) | cadrage § 4 | H_max ∝ marge^−⅓ ; RS02 : 0,90 / 0,79 / 0,71 m à 1,0 / 1,5 / 2,0 |
| **Poids du comparatif** (S et familles) | **DÉCIDÉ** (`criteres_selection.yaml:223-329`) | registre § 12 | 18 / 18 / 15 / 15 / 12 / 7 / 5 / 5 / 5 |
| **Règle de décisivité étendue** | **DÉCIDÉ** (`criteres_selection.yaml:185`) | `docs/comparatif-banc.md` | plage plausible : k ≥ 0,619 |
| **Famille pour S** | **RECOMMANDÉ** : Damiao 48 V, RobStride en repli (conclusion § 4.1) ; **non décidé** | `docs/choix-famille-actionneurs.md` | scores à k = 1 : Damiao 3,59, EL05 3,23, CubeMars 3,21, RobStride 2,95, MyActuator 2,75 ; bascule **k ≈ 0,49/0,50** ; rapports blocage/nominal RobStride de 0,619 à 0,857 ; **mais voir § 8, K1** |
| **Banc** | **PROPOSÉ** ; composition divergente (§ 8, H4) | `docs/comparatif-banc.md`, `params/budget.yaml`, conclusion § 4.2 | trois options ex æquo à 2,30 (3 × J4310 à 574 CHF, J4310 + RS05 à 416, qualification à 499) ; option « vérification » 2 × J4310 48 V à **386 CHF TTC** hors alimentation |
| **Poids du banc** | **PROPOSÉ** (retour de « fixé » : attribution erronée, `ef03734`) | `criteres_selection.yaml:394-429` | 40 / 20 / 15 / 15 / 10 ; valeur de décision = 0 pour toutes les options |
| **Critère d'abandon** | **PROPOSÉ** (`protocole-banc.md` § 2 bis) | idem | **< 1,75 N·m** au blocage, plaque 70 × 70 mm, borne haute de l'intervalle, plus faible de deux exemplaires |
| **Estimation thermique du J4310** | ESTIMATION, pas une mesure | `docs/estimation-thermique-j4310.md` | k de 0,92 à 1,02 en rotation, **24 V** ; de 0,57 à 0,87 au blocage (« hypothèse sur hypothèse ») |
| **Note du J4310 au catalogue** | **DÉCIDÉ** (validée par Jeremy, `actionneurs.yaml:231`) | idem | « PAS un régime établi » → « montée presque achevée » |
| **Actionneur maison** | **DÉCIDÉ** (0052) | cadrage § 8 | taille S d'abord, jamais sur le chemin critique |
| **Fabrication séquencée** | **DÉCIDÉ** (0050), rien d'appliqué | cadrage § 1, principe 4 | — |
| **Interfaces d'actionneur** | **PROPOSÉ**, sans fiche | cadrage § 8 bis ; `docs/choix-interfaces.md` | — |
| Pour la v1, on achète | **PROPOSÉ** (cadrage:464) | cadrage § 8 | — |
| Vision (§ 1) | **PROPOSÉ**, jamais validée | cadrage § 1 | — |

---

## 5 — Implémenté et non implémenté

### 5.1 Ce qui existe et tourne (**V**, exécuté ce soir)

| Dossier | Contenu | Résultat |
| --- | --- | --- |
| `scripts/` (23) | `regenerer` | **sortie 0, 26,3 s** ; 1 pièce, 8 contrôles OK ; 5 pages, 15 fichiers, 248 ko |
| | `audit_origines --strict` | sortie 0 ; **3 035 valeurs, dont 978 numériques** ; amont 1 124, propre 1 058, catalogue 717, littérature 88, mesure 47, **ambigu 1** (Zeroth-01) |
| | `controle_regles` | 125 motifs, tous atteints ; 1 dormant ; rayon conforme sur 6 réglages |
| | `controle_depot` | 139 fichiers suivis, aucun binaire, 5 journaux bien datés |
| | `index_fiches` | 52 entrées ; **ignore toujours ses arguments** |
| | `empreinte` | `de10401722`, **égale à yxor.fr** (curl, 21 h 5x) |
| | `dimensionnement` | 28 configurations, marge 1,5 ; cohérence : ToddlerBot 0,560 m, Zeroth-01 0,672 m pour 0,48 m « attendu » |
| | `selection_multicritere` | voir § 4 ; **les documents engendrés se reproduisent à l'octet près** (régénérés dans une copie du dépôt, `diff` vide sur 5 documents) |
| | `estimation_thermique` | k de 0,92 à 1,02, médiane 0,96, sur 12 combinaisons |
| | `analyser_marche`, `enveloppes_actionneurs` | tournent ; le second **ignore `--help`** |
| | `check_cad_toolchain` | 16/16 |
| | `import_upstream_limits --check` | à jour |
| | `ckpts_backup verify` | 10 conformes |
| | `source --liste` | 8 sources |
| | `procedes` | 6 réglages, dont 2 IMPOSSIBLES |
| | `audit_origines --json` | **plante** (TypeError sur une date, élément 1 895), déjà signalé au journal :223 |
| `tests/` (7 fichiers, **9 tests**) | `python -m unittest discover -s tests` | **9 OK, 30,7 s** ; `pytest` absent du venv |
| `parts/` | `semelle_apprentissage.py` | **la seule pièce** ; palier **P2**, réglage `cutter_cartonplume_5` |
| `sim/` | `render.py`, `view.py`, `upstream/` (3) | non relancés ce soir : `enregistrer_marche.py` réécrirait la série de référence dont le sha256 fait foi |
| `web/` | 4 fichiers | **jamais exécutés dans un navigateur** (DÉCLARÉ, conclusion § 5.10) |

### 5.2 Ce qui n'existe pas, et pourquoi

| Absent | Pourquoi |
| --- | --- |
| `robot/` (`.gitkeep`) : ni assemblage, ni URDF, ni MJCF YXOR | **aucune fiche** ; le README l'annonce |
| `bom/` (`.gitkeep`) | la 0019 renvoie à « quand une pièce aura un montage » (DÉCLARÉ) |
| Simulation YXOR | aucune fiche ; tout le chiffrage repose sur la marche ToddlerBot |
| Pièces de S | la famille n'est pas choisie (conclusion § 6) |
| Couche logicielle `joint.command(...)` | PROPOSÉ (cadrage § 8 bis), sans fiche |
| `actionneurs.P1.{modele, couple_nominal_Nm, entraxe_fixation}` : `null` « non déterminé » | `nullites.yaml`, **encore adossé à P1**, alors que la taille est S |
| `materiaux.{carton_plume, contreplaque, aluminium}.source` | « se déduira » (`nullites.yaml`) |
| `structure.prix` (`budget.yaml`) | « tant que l'opérateur CN n'a pas chiffré la **découpe métal** », texte d'avant la 0050 |
| Batterie à 48 V | constat au budget ; rien de chiffré |
| Masse que S doit porter | question 13 du cadrage ; non chiffrée |
| Accesseur `yxor/cotes.py`, origine `norme`, `archive/` | 0010, 0035, 0036 : **aucune raison écrite**, sauf pour 0035 |

---

## 6 — Reporté, en veille, abandonné

| Sujet | Statut | Déclencheur écrit |
| --- | --- | --- |
| Caractérisation du carton | **ABANDONNÉ** (DÉCIDÉ) | « jamais : le carton reste une maquette » (cadrage:455) |
| Éliminatoire de taille 0,55 m | **ABANDONNÉ** (`b01342a`) | — |
| Poids du banc « fixés » | **RETIRÉ** | — |
| 0021, clé composée | ABANDONNÉ | — |
| OrcaSlicer, 3MF, FreeCAD MCP, Zoo, bd_warehouse | veille (0032) | l'achat d'une imprimante ; deux impasses build123d ; un échec OCCT ; une vis |
| Backflip | veille (0046) | un test que Jeremy lancera |
| Paliers P1/P2/P3 → tailles | reporté (question 8) | « une fiche qui remplace » — **pas de date** |
| 0014 et 0015 → 0050 | reporté (question 9) | idem |
| Immuabilité des fiches | ouvert (question 10) | **aucun** |
| Membre L de Damiao (J4340, 40:1) | reporté | « avant L » |
| Interfaces mécaniques | reporté | « un actionneur en main » (conclusion § 4.5) |
| Marge | à revoir | les résultats du banc |
| Imprévus à 15 % | provisoire | « à fixer par Jeremy » — **pas de déclencheur** |
| Structure | en attente | le chiffrage de l'opérateur CN |
| Alimentation du banc | outillage, décision de Jeremy (règle b) | **aucun** |
| Licence des valeurs amont | ouvert (0010 § 4, question 11) | **aucun** |
| Seconde sauvegarde des poids | 0008 | **aucun** (« à la charge de Jeremy ») |
| Soudure | 0022 | **aucun** |
| Transmissions (0015) | — | **aucun** |
| Simulateur JS, blocage réseau WSL | constats | **aucun** |

**DÉD** : sept reports n'ont aucun déclencheur. Cinq existaient déjà le 29.

---

## 7 — Traçabilité et outillage

### Chiffres (**V**)

| Mesure | 29-09 nuit | 30-09 |
| --- | ---: | ---: |
| valeurs auditées | 1 440 (688 num.) | **3 035 (978 num.)** |
| origine `catalogue` | 17 | **717** |
| origine `propre` | 175 | **1 058** |
| origine `amont` | 1 121 | 1 124 |
| motifs déclaratifs | 62 | **125** |
| fichiers suivis | 104 | **139** |
| fiches | 44 | **52** |
| tests | **0** | **9** |
| cotes qui gouvernent une géométrie | 8 | **8** |

### Tests : lesquels prouvent qu'ils savent échouer

| Test | Preuve d'échec |
| --- | --- |
| `test_dimensionnement_coherence` (3) | **intrinsèque** : il injecte deux références impossibles et exige un refus (**V**, lecture) |
| `test_selection` | **intrinsèque** : un candidat éliminé, noté au maximum partout, ne doit gagner nulle part (**V**, lecture) |
| `test_index_fiches`, `test_regenerer_index`, `test_ratios_ansur`, `test_empreinte`, `test_construction_deterministe` | tests de non-régression : « vu échouer avant la correction » (**DÉCLARÉ**, docstrings) |

Les tests existants laissent plusieurs trous (**V**) :

- ils ne sont lancés **ni par `regenerer.py` ni par le Dockerfile** (grep) : ils ne tournent qu'à la main ;
- `test_selection` et `test_dimensionnement_coherence` se **sautent** si `exports/` est vide, et le disent ;
- **aucun test ne porte sur les conclusions des comparatifs** : décisivité, égalités, cohérence entre l'article noté et l'article recommandé (§ 8, K1).

### Empreinte et déterminisme

Mesures (**V**) :

- `SOURCES = params, parts, scripts, web` et `requirements.txt` (`empreinte.py:49-50`) ;
- deux régénérations successives laissent `git status` inchangé ;
- les 5 documents engendrés se reproduisent à l'identique.

Ce que l'empreinte ne couvre pas (**V**) :

- `docs/` et `journal/` ;
- donc le cadrage, les comparatifs et ce rapport ;
- **l'empreinte « dépôt = site » ne dit rien du travail du 30-09**.

**yxor.fr n'affiche rien des actionneurs ni du cadrage** (**V**, `grep`
sur `site/`).

**Aucun contrôle ne vérifie que les documents « engendrés » sont à jour.**
Ils le sont ce soir, mais seulement parce que je les ai régénérés.

---

## 8 — Diagnostic

Classé par gravité. **Rien n'est appliqué** : chaque ligne propose une
correction.

### Critique

**K1 — La famille Damiao est notée en 24 V, recommandée en 48 V.**

*Preuves (**V**)* :

- `actionneurs.yaml:610` : le membre S de la famille Damiao est `dm_j4310`, la variante **24 V** chez Eckstein. La 48 V n'y figure que comme `S_variante_48V`.
- `choix-famille-actionneurs.md:121-129` : Damiao y reçoit `tension_securite` = **4** (24 V), contre 2 pour RobStride (48 V). L'écart vaut **+0,10 point**, c'est-à-dire exactement la marge que le cadrage dit fondre « à 0,10 point » à bas k.
- La conclusion (§ 4.1) recommande « **Damiao J4310 V1.2 en 48 V** ».

*Recalcul en mémoire*, avec `dm_j4310` passé à 48 V, sans aucun fichier
modifié (script dans le dossier temporaire) :

| Grandeur | Notée en 24 V | Recalculée en 48 V |
| --- | --- | --- |
| Bascule | Damiao jusqu'à k = 0,50, RobStride dès 0,49 | **Damiao jusqu'à 0,62, RobStride dès 0,61** |
| k = 0,6 | Damiao en tête | égalité à 2,95, **RobStride en tête** |
| k = 0,5 | Damiao en tête | **RobStride en tête** |

*Conséquences (DÉD)* :

1. La règle de décisivité compare 0,61 à la borne plausible 0,619. **Le
   verdict « vérification, pas départage » tient à 0,009.** Avec `garde`
   (0,62) au lieu de `k`, il tomberait (`selection_multicritere.py:472`).
2. **Le critère d'abandon de 1,75 N·m (0,5 × 3,5) serait d'environ 2,14 à
   2,17 N·m** (0,61 à 0,62 × 3,5).
3. **La fourchette de k au blocage (0,57-0,87) serait « à cheval sur la
   bascule »**, et non plus « toujours au-dessus ».
4. La disponibilité (Eckstein, en stock), la fiabilité (« UE Eckstein »)
   et le coût notés sont ceux de la 24 V. La 48 V vient d'OpenELAB : TVA
   inconnue, précommande possible. **Le recalcul est donc plutôt
   optimiste pour Damiao.**

*Correction proposée* : noter la famille sur l'article recommandé, ou deux
familles « Damiao 24 V » et « Damiao 48 V », puis recalculer. Réécrire le
critère d'abandon **avant** toute commande. Ajouter un test : l'article
noté est l'article recommandé.

**K2 — Aucune alimentation chiffrée ne remplit la condition de sécurité du banc.**

*Preuves (**V**)* :

- `protocole-banc.md` § 1.1 exige une limitation de courant réglable.
- Le budget chiffre une RSP-500-48 (tension fixe, dit au protocole) et une PeakTech 30 V, « pas pour un actionneur 48 V » (`budget.yaml:80`).
- Le comparatif du banc **inclut la Mean Well dans ses coûts** (§ 1). L'option « vérification » l'exclut.
- La conclusion § 6 place « **Commande** » (étape 2) sur le même rang que « choisir l'alimentation ».

*Ce qui manque encore (**V**)* :

- ne sont chiffrés ni l'arrêt d'urgence à contacteur 48 V continu, ni le dynamomètre, ni les butées ;
- l'adaptateur candleLight est **non conforme CE** (`budget.yaml:50-51`) ;
- le protocole exige une **seconde personne** (§ 1.6) ; le dépôt ne dit pas qu'elle existe.

*Correction proposée* : aucune mise sous tension et aucune commande
d'actionneur tant que l'alimentation, l'arrêt d'urgence et la seconde
personne ne sont pas réglés. C'est à écrire comme **préalable** dans la
conclusion, pas comme une étape parallèle. Le choix du matériel reste
celui de Jeremy (règle b).

### Haut

**H1 — Le seuil thermique du protocole n'est pas celui de l'estimation.**

*Preuves (**V**)* :

- le protocole arrête un palier « 10 °C sous la protection », soit **90 °C** pour le Damiao (§ 1.5) ;
- l'estimation et le nominal sont pris à **100 °C** (`estimation_thermique.py:53`, `T_LIM = 100.0`).

*DÉD* : le continu mesuré sera plus bas d'environ **7 %**
(√(65/75) ≈ 0,93 à 25 °C). Ce biais va dans le sens du déclenchement du
critère d'abandon. S'ajoutent deux écarts de condition (**V**) :
l'estimation est faite **en 24 V et en rotation**, le banc serait en 48 V
et au blocage.

*Correction proposée* : fixer dans le critère la température de référence
du « continu mesuré », et corriger le seuil en conséquence.

**H2 — CLAUDE.md contredit les décisions du jour.**

*Preuves (**V**)* :

- CLAUDE.md dit « **Procédé unique : la découpe 2D** » et « Concevoir au plus contraignant, au carton ». Il ne cite ni le cadrage, ni S, ni le banc (`grep` : 0 occurrence).
- La 0050 le reconnaît. Mais CLAUDE.md **s'impose à l'assistant** : un agent qui le suit dessinerait des plaques pour le carton.

*Correction proposée* : un bandeau daté dans la section fabrication, qui
renvoie à 0050 et à la question 9, sans rien effacer (même pratique que
les « contraintes retirées »).

**H3 — Fiches contredites, non remplacées** (§ 3.3).

*Preuves (**V**)* :

- 0001, 0005, 0011, 0014, 0015, 0038 ;
- 0004 et 0029 gardent dans leur corps des affirmations corrigées ailleurs : « les deux sens », « CC BY-NC ».

*Correction proposée* : trancher la question 10 d'abord, parce qu'elle dit
**comment** remplacer ; puis écrire les fiches des questions 8 et 9.

**H4 — La composition du banc diverge entre les documents.**

| Document | Composition (**V**) |
| --- | --- |
| cadrage:196 | qualification (et § 6 : « le banc mesure ce qui les départage ») |
| cadrage § 13, question 12 | vérification, trois options ex æquo |
| `budget.yaml:97-105` | **2 × RS05** par défaut, phase marquée « OPTION » |
| `budget.yaml`, option `verification` | 2 × J4310 48 V |
| conclusion § 4.2 | 2 × J4310 48 V |
| `protocole-banc.md:8` | « tel que le comparatif le place en tête : qualification » |
| `protocole-banc.md` § 2 | « les trois actionneurs » |
| `dimensionnement-par-actionneur.md:261` | « 1 actionneur de la classe lourde » |

Le même « 2 × J4310 » coûte **418 CHF** au comparatif (variante 24 V et
alimentation 24 V) et **386 CHF** au budget (48 V, sans alimentation).

*Correction proposée* : une seule source pour le banc, `budget.yaml`,
et des documents qui la citent.

**H5 — Le document qui résume les arbitrages n'est pas versionné.**

*Preuves (**V**)* :

- `git status` : `docs/conclusion-arbitrages-2026-09-30.md` est non suivi ;
- il attribue des statuts DÉCIDÉ ;
- il dit S ≈ 0,55-0,65 m, contre 0,55-0,60 au cadrage ;
- il contient une étape « Commande ».

*DÉD* : cette étape heurte la règle d'achat (c), parce qu'elle vient de
l'assistant. Elle heurte aussi la règle (a) : un actionneur n'a pas de
verdict `coupable`, donc la règle n'a pas de référent pour lui.

*Correction proposée* : le verser en le marquant comme reçu, ou le laisser
hors dépôt. C'est à Jeremy de décider. Ce rapport ne le commite pas.

**H6 — Des documents fournisseurs utilisés sans registre (fiche 0030).**

*Preuves (**V**)* :

- `actionneurs.yaml` cite **14 documents distincts par sha256** : manuels Damiao, RobStride RS05 et EL05, catalogue MyActuator, CubeMars… ;
- `fournisseurs.yaml` n'a que 3 entrées, dont **un seul** document constructeur (RobStride, le PDF du 17-09) ;
- la 0030 range explicitement l'« extrait de fiche technique » parmi les fichiers à enregistrer ;
- `controle_depot` ne vérifie pas cette correspondance.

*Correction proposée* : un contrôle qui exige une entrée pour chaque
sha256 cité.

### Moyen

- **K_ESTIME recopié** (**V**, `selection_multicritere.py:527`).
  `(0.92, 1.02)` est recopié à la main depuis le rapport thermique. La
  raison est dite : les images sont absentes en Docker. Mais aucun test
  ne lie la copie au calcul, ce qui heurte la règle 3 de CLAUDE.md. Les
  valeurs concordent ce soir.
  *Correction proposée* : un fichier de résultat versionné, lu par les deux, ou un test d'égalité.
- **Cadrage en retard sur ses propres mises à jour** (**V**).
  - L'en-tête dit « Version 1… À intégrer dans le dépôt ».
  - Le § 6 et la question 12 se contredisent (voir H4).
  - Le § 7.2 dit « le chiffrage de S est à produire », alors que `choix-famille` le donne (≥ 1 472 à 2 354 CHF).
  - La question 13 se termine par une phrase qui appartient à la 12, et l'adaptateur y est dit non vérifié, alors qu'il l'est.
  - La 0048 liste les classes de S sans Damiao.
- **Le comparatif du banc ignore sa propre règle** (**V**,
  `comparatif-banc.md` § 4). La note de transfert à S des options
  « × Damiao » vaut 3, parce que « k inconnu ». Le comparatif le signale
  sans le corriger ; à 5, « 3 × J4310 » passerait seul en tête (2,70).
  Et le § 5, étape 4, dit encore « le seuil k × nominal à départager ».
- **`budget.yaml` périmé par endroits** (**V**).
  - La structure est rattachée à « fiche 0015 » et à la « découpe métal » (l. 82-85), contre la 0050.
  - Batterie à 22,2 V.
  - Imprévus « provisoire ».
  - Le banc par défaut est 2 × RS05.
- **README, point d'entrée** (**V**).
  - l. 17 : « Creative Commons non commerciale », contre BY-NC-SA.
  - Le tableau P1/P2/P3 est présenté comme actuel.
  - Il cite l'état des lieux de midi comme inventaire courant.
- **Réciprocité des amendements** (**V**, lectures) : 0012 ← 0034,
  0020 ← 0033, 0028 ← 0035. La 0020 est **aggravée** par une attribution
  fausse (`nullites.py:56`).
- **Taxonomie** (**V**) : 3 espèces dans la 0036, 6 dans le code. 0042
  « archivée » sans `archive/`.
- **0038 et 0041 appliquées sans être acceptées** (H5 de la nuit,
  aggravé). `protocole-banc.md:201` dit la 0041 « décidée ».
- **Sources non lues citées comme fait** (**V**) : Bennehar, `non_lu`,
  sert d'appui à 0039:15 et à `cadrage.md:437`. La 0040 l'interdit.
- **Tests hors de la commande unique** (**V**) : les 9 tests ne tournent
  pas dans `regenerer.py`.

### Bas

- `audit_origines --json` plante (**V**).
- `controle_depot` : saut muet sur `fournisseurs.yaml` absent (**V**, l. 112-113).
- `index_fiches` et `enveloppes_actionneurs` ignorent leurs arguments (**V**).
- `ckpts.manifest.yaml:7` dit « deux destinations » (**V**) : H2 de la nuit, ouvert.
- En-tête d'`anthropometry.yaml:19-25`, « Drillis & Contini, NON VÉRIFIÉES » (**V**) : H3 de la nuit, ouvert.
- Statut de la 0024 faux ; 0032 « cinq ou quatre » ; `alu_tole_6` ; « simple cannelure » dans 0026:98 ; « 40 fiches » dans la 0036 (lectures).
- `sim/render.py` : « `python sim/render.py` » sans venv (**V**).
- Renvois morts : `docs/00-cadrage.md` à `03-artefacts.md`, « LOG-1 », `yxor/cotes.py`, `decisions/archive/` (lectures).
- Pas d'heure dans la section « nuit » du journal du 30 (lecture).

---

## 9 — Depuis la nuit du 29

### Corrigé (**V**)

| Point de la nuit | Comment |
| --- | --- |
| C3 : retour d'`index_fiches` ignoré | `regenerer.py:401`, et un test |
| C4 : un seul « Amendée par » lu | `index_fiches.py:49-54`, et un test |
| C5 : la semelle publiée n'est pas celle qui a été coupée | 0044 close, mention sur la page (`pages.py:416`) |
| H7 : colonne D&C fausse | valeurs figées, et un test |
| H10 : empreinte | `requirements.txt` ajouté, et un test ; le Dockerfile en est **sorti par décision** (Coolify) |
| H1 : licence | CLAUDE.md et 0001 corrigés ; **pas le README ni le corps de la 0029** |
| C1, C2 : promesses fausses | **les phrases sont corrigées** dans CLAUDE.md ; les protections restent absentes, et la 0004 comme la 0027 gardent l'ancien texte |
| « Aucun test » | 9 tests |
| « Que doit faire le robot ? » | **en partie** : échelle des capacités (cadrage § 10), degrés de liberté par version (§ 11) |

### Encore ouvert

H2, H3, H4 (aggravé), H5 (aggravé), H6, H8, H9, three.js, `yxor/cotes.py`,
le saut muet, `--json`, les renvois de ligne de 0010 et 0011, la 0039.

### Nouveau

K1, K2, H1 à H6 ci-dessus. S'y ajoutent l'estimation thermique et le
comparatif, qui sont **de vrais progrès de méthode** : trois biais
corrigés, et un critère d'abandon écrit avant la mesure.

---

## 10 — Proportion gouvernance / robot

### Par fichier suivi (**V**, `wc -l` sur 139 fichiers, 33 643 lignes)

Le classement est **DÉD**. Il n'est pas identique à celui de la nuit : la
catégorie « actionnement » est nouvelle.

| Catégorie | Fichiers | Lignes | Part |
| --- | ---: | ---: | ---: |
| Journal | 5 | 8 596 | 25,6 % |
| Fiches | 53 | 6 520 | 19,4 % |
| Gouvernance (contrôles, audit, origines, CLAUDE.md, états des lieux) | 22 | 4 168 | 12,4 % |
| **Actionnement : code et données** (dimensionnement, sélection, thermique, catalogue, budget, critères) | 8 | 3 386 | 10,1 % |
| **Actionnement : documents** (cadrage, comparatifs, protocole, étude) | 10 | 2 911 | 8,7 % |
| Données et outils robot (anthropometry, joints, hardware, extraction, CAO) | 13 | 3 293 | 9,8 % |
| Publication | 11 | 2 491 | 7,4 % |
| **Géométrie** (semelle, profil, plan de découpe) | 3 | **1 070** | **3,2 %** |
| Simulation | 7 | 903 | 2,7 % |
| Tests | 7 | 305 | 0,9 % |

### Évolution depuis le 29 au soir

| Mesure | 29-09 nuit | 30-09 |
| --- | ---: | ---: |
| Gouvernance au sens large (journal, fiches, gouvernance) | 15 765 lignes, **66 %** | 19 284 lignes, **57 %** |
| Géométrie | 1 058 lignes | 1 070 lignes |
| Pièces | 1 | 1 |
| Fiches | 44 | 52 |

Contrôles : ceux du robot portent toujours sur **une** semelle ; ceux du
dépôt portent désormais sur **3 035** valeurs.

### Mon avis, franchement (DÉD)

**Le 30 a été la meilleure journée du projet sur le fond.** Pour la
première fois, le dépôt pose la bonne question : *quel actionneur, donc
quelle taille, donc quel budget*. Il y répond avec un calcul qui sait
échouer. Le cadrage donne enfin ce que le rapport de la nuit disait
manquer : ce que le robot doit faire (§ 10).

**Mais la forme a gardé ses travers, et en a pris de nouveaux.**
L'appareil de décision a grossi aussi vite que l'appareil de contrôle la
veille :

- 3 comparatifs ;
- 442 lignes de critères ;
- 18 variations de poids et 1 000 tirages ;
- 8 options de banc.

Il a produit en une soirée **quatre corrections de biais**, et cet audit
en trouve un cinquième, **le plus lourd** (K1). Or il porte sur le seul
chiffre qui compte, la bascule de famille.

Le motif est le même que la veille : **un outil précis appliqué à une
entrée fausse donne une fausse certitude**. « Aucune inconnue n'est
décisive » était vrai pour un article que personne ne compte acheter.

**Ce qui manque n'est pas une 53ᵉ fiche ni un 4ᵉ comparatif.** Il manque
**un actionneur sur une table**, avec une alimentation sûre. Le banc
réduira plus d'incertitude en une heure que les tirages de Dirichlet en
une semaine. Et il se trouve **en amont** de toute pièce de S.

La gouvernance a baissé en proportion parce que le robot a enfin grandi
sur le papier, pas parce qu'elle a maigri : 19 284 lignes contre 15 765.

---

## 11 — Questions ouvertes et pistes

### Avec un support écrit

Voir le cadrage § 13 (13 questions) et la conclusion § 5 (12 questions).
Les plus lourdes :

- la famille de S ;
- l'alimentation du banc ;
- ce que S doit porter ;
- la batterie 48 V ;
- les questions 8, 9 et 10 ;
- la licence des valeurs amont.

### Sans fiche ni question écrite (DÉD)

1. **24 V ou 48 V pour S ?** Il faut le trancher *avant* le comparatif,
   pas après (K1). Le « une seule tension de S à L » de la conclusion
   suppose un membre M Damiao, le J8006, donné pour 24 V et qui
   « supporte 24–48 V ». C'est **non vérifié**.
2. **La température de référence du « continu mesuré »** (H1).
3. **Qui est la seconde personne du banc ?** Le protocole l'exige.
4. **La règle de décisivité est-elle robuste au pas de 0,01 ?** Tout
   repose sur `k` contre `garde`.
5. **Zeroth-01** est accepté par le contrôle de cohérence à 0,672 m pour
   0,48 m « attendu », et sa hauteur est `ambigu`. Que prouve encore le
   contrôle ?
6. **Que devient la semelle P2 ?** C'est la seule pièce, à une taille
   abandonnée.
7. **Le site doit-il projeter le cadrage et les comparatifs ?** Il n'en
   montre rien, et son empreinte ne les couvre pas.
8. **La marche de référence écrêtée** (9 actionneurs de jambe sur 12)
   fait de toutes les tailles des plafonds. Faut-il une marche non
   écrêtée avant de choisir ?

---

## 12 — Lecture pour Jeremy

Dans l'ordre, une phrase chacun.

1. **`docs/cadrage.md`** : ce qu'est YXOR aujourd'hui et le pourquoi de
   chaque arbitrage. Lire §§ 2, 3, 6, 10 et 12 ; les §§ 6 et 13 se
   contredisent sur le banc (H4).
2. **`docs/conclusion-arbitrages-2026-09-30.md`** : le résumé de ce qui
   attend ta décision. Il est **non versionné**, et son § 4.1 est à relire
   avec le K1.
3. **`docs/choix-famille-actionneurs.md`**, §§ 1, 3 et 3 bis : pourquoi
   Damiao est devant, et ce que k veut dire.
4. **Ce rapport, § 8, K1** : pourquoi ce « devant » dépend de la tension
   notée.
5. **`docs/estimation-thermique-j4310.md`** : comment on estime un couple
   continu sans rien acheter. C'est la meilleure leçon de mécanique du
   dépôt.
6. **`docs/protocole-banc.md`**, §§ 1 et 2 bis : la sécurité d'abord, puis
   le critère écrit avant la mesure.
7. **`decisions/0050-fabrication-sequencee.md`** : la direction de
   fabrication, et la contradiction qu'elle assume avec 0014, 0015 et
   CLAUDE.md.
8. **`decisions/0013-nature-des-cotes.md`** : pourquoi une épaisseur ne
   grandit pas avec le robot. Tu en auras besoin dès la première pièce
   de S.

---

## 13 — Ce que ce rapport ne peut pas savoir

- **Les conversations hors dépôt.** Le cadrage a été rédigé par Claude
  (arbitrage), à partir d'échanges avec Jeremy. La « recherche Claude »
  et l'« audit ChatGPT » du 30-09 sont **non versionnés** (cadrage § 14).
  La conclusion est hors Git.
- **Les décisions orales** que le dépôt n'enregistre pas. En particulier :
  - si Jeremy a validé le § 4 de la conclusion ;
  - si le choix de la 48 V est voulu ou hérité ;
  - s'il a répondu sur la note de transfert du banc.
- **Ce qui s'est passé** du 21 au 27/09, et le 30/09 de 00 h 41 à 13 h 27
  et de 13 h 55 à 17 h 10.
- **Tout achat réel.** Une imprimante « cette semaine » (0027:141,
  `hardware.yaml:403`) : rien ne dit si elle existe. Un actionneur
  commandé : rien ne le dit non plus.
- **Le chiffrage et le procédé de l'opérateur CN.**
- **L'état physique** de la semelle coupée, du poste de travail, et la
  présence d'une seconde personne pour le banc.
- **Les pages des vendeurs** (OpenELAB, Eckstein, Seeed) au moment de la
  lecture : les prix et la TVA n'ont pas été revérifiés ici.
- **Le comportement de Coolify** au-delà de l'hypothèse confirmée le
  30-09 à 00 h 35.
- **Le rendu réel du site** dans un navigateur, mobile compris, et le
  simulateur JS : aucun navigateur n'a été lancé.
- **Toute portée juridique** : licence des valeurs amont, documents
  constructeurs sans licence. Ce rapport ne donne aucun avis.
