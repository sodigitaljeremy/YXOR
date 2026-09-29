# 0014 — Il n'y a pas d'imprimante 3D

Date : 2026-09-28
Espèce : historique
État : appliquée
Statut : acceptée

## Le fait

**Jeremy ne possède pas d'imprimante 3D.** Les documents de cadrage
l'annonçaient ; l'information n'a jamais été vérifiée, et tout le palier
P1 reposait dessus.

C'est la sixième défaillance silencieuse du projet, et la plus coûteuse :
elle n'a produit aucune erreur pendant huit jours de travail, parce que
rien de ce qui a été fait ne s'est heurté à la machine absente.

> **Note.** `docs/00-cadrage.md` est **absent du dépôt** — comme
> `01-cahier-des-charges`, `02-plan-action` et `03-artefacts`, signalés
> manquants dès le journal de la phase 0. L'affirmation n'a donc pas pu
> être relue à sa source. Ce trou documentaire est ce qui a permis à
> l'erreur de survivre.

## Ce que cela invalide — inventaire complet

### 1. La base ToddlerBot est inconstructible en l'état

**C'est la conséquence majeure, et elle n'est pas contournable.**

La documentation amont est explicite :

> « **BambuLab printers are highly recommended.** […] Proper orientation
> and profiles are crucial to ensure the strength and durability of the
> **3D-printed parts**. »

Le modèle compte **47 maillages pour 46 corps** : pratiquement chaque
pièce structurelle est un volume imprimé. Sans imprimante, **ToddlerBot
ne se construit pas**, ni en partie ni en entier.

La fiche 0001 retenait ToddlerBot notamment pour sa « chaîne complète
documentée du jumeau numérique au déploiement ». **La moitié déploiement
tombe.** La moitié simulation reste entière.

### 2. `CLAUDE.md` — contraintes de fabrication

| Ligne | Statut |
| --- | --- |
| « Pièce imprimée : tient dans 256 × 256 mm » | **caduque** — il n'y a pas de pièce imprimée. Le volume 256 × 256 était celui d'une machine inexistante |
| « Filetage dans le plastique : insert à chaud » | **caduque** — un insert à chaud se pose dans du thermoplastique imprimé. Ni le contreplaqué ni l'aluminium n'en acceptent |
| « Pièce découpée : contour fermé, mm, 1:1, rayon intérieur ≥ 0,5 × ép., aucun angle vif rentrant » | **valide, et devient la règle centrale** |
| « Aucun logement de roulement par découpe : palier rapporté ou alésage repris » | **valide, et devient critique** |
| « Assemblage démontable, aucun collage structurel » | **valide** |

Deux contraintes sur cinq tombent ; les trois qui restent passent du
rang d'accessoire à celui de fondation.

### 3. `params/hardware.yaml`

| Clé | Statut |
| --- | --- |
| `vis.*.insert_diametre`, `vis.*.insert_profondeur` | **caduques** — cotes de logement d'insert à chaud |
| `tolerances.impression_3d.*` (`jeu_glissant`, `jeu_serre`, `logement_roulement`) | **caduques** |
| `epaisseurs.paroi_minimale_impression: 1.6` | **caduque** |
| `epaisseurs.contreplaque_P1`, `tole_alu_P2`, `carton_plume_maquette` | **valides, et deviennent centrales** |
| `tolerances.decoupe_jet_eau.profil` | **valide, mais incomplet** — il manque le cutter et le laser |
| `roulements.*`, `vis.*.diametre/passage/tete_diametre` | **valides** |

**Le fichier suppose l'impression comme procédé principal et la découpe
comme appoint. C'est exactement l'inverse qu'il faut.**

### 4. Matériaux par palier

`contreplaque_P1` et `tole_alu_P2` associaient un matériau à un palier de
taille. Cette association reposait sur l'idée que le gros des pièces
serait imprimé et que ces matériaux ne serviraient qu'aux renforts.
**À réexaminer** : le matériau devient fonction du procédé accessible,
pas du palier.

### 5. Le choix de la première pièce

Les trois candidates du 2026-09-28 : **deux sur trois tombent.**

| Candidate | Statut |
| --- | --- |
| `neck_rod` — plate | **survit**, et devient la seule pertinente |
| `left_shoulder_pitch_link` | **caduque** — « pièce imprimée, inserts à chaud » |
| `left_knee_link` | **caduque** — idem |

Le raisonnement qui recommandait `neck_rod` tenait au fait qu'elle
exerçait la chaîne DXF. Ce motif est renforcé, pas affaibli.

### 6. Le plan d'action

**Non vérifiable : `docs/02-plan-action.md` est absent du dépôt.** Son
échelonnement reposait vraisemblablement sur une chaîne de fabrication
qui n'existe pas. La phase 6, qui conditionne selon `CLAUDE.md` toute
proposition d'achat, ne peut pas être située.

### 7. Ce qui n'est PAS invalidé

Il faut le dire aussi nettement, pour ne pas surestimer les dégâts :

- **Toute la chaîne de simulation** — MuJoCo, les politiques, le jumeau
  numérique, les mesures d'inertie. Rien n'y touche au matériel.
- **La traçabilité** — fiches 0010 à 0013, l'audit d'origine, la
  nature des cotes. Le second axe `procede` prend même tout son sens.
- **La chaîne CAO** — build123d, l'export DXF vérifié en millimètres.
  C'est désormais la seule chaîne de sortie qui compte.
- **La topologie articulaire** (fiche 0005) — voir la fiche 0015.
- **`anthropometry.yaml`** — les ratios ne dépendent d'aucun procédé.

## Décision

1. **L'impression 3D sort du périmètre de conception de YXOR** tant
   qu'aucune machine n'est disponible et vérifiée.
2. **Aucune pièce ne sera conçue en supposant un procédé non vérifié.**
   Un moyen de fabrication est désormais une donnée à établir, au même
   titre qu'une cote — avec sa source.
3. **L'inventaire ci-dessus n'est pas corrigé par cette fiche.** Les
   corrections de `CLAUDE.md` et de `hardware.yaml` sont soumises à
   Jeremy, qui a demandé la liste et non un correctif ponctuel.
4. **ToddlerBot reste la référence de simulation**, et cesse d'être la
   référence de construction. Cette scission était déjà écrite dans la
   fiche 0013 sous une autre forme : le modèle **représente**, il ne
   **décrit** pas.

## Conséquences

- La question « comment fabrique-t-on cette pièce ? » précède désormais
  « quelle forme a-t-elle ? », et non l'inverse.
- Le jumeau numérique et le robot physique **divergent** : le premier
  reste ToddlerBot, le second ne le sera pas. Tout transfert de politique
  devient une hypothèse à tester, non un acquis.
