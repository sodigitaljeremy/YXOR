# Diagnostic de refonte du dépôt — 2026-10-01

**Commencé le 2026-10-01 à 13 h 48** (`date`), au commit `5855c24`.
**Lecture seule** : rien n'a été modifié, déplacé ou supprimé. Seuls ce
rapport et le journal sont écrits.

**Ce qui vient de Jeremy** (2026-10-01, ses mots) : « on arrive à un stade
où il va falloir refactorer tout le repo […] auditer et diagnostiquer […]
comment tout réorganiser et réarchitecturer l'arborescence du projet,
quoi modifier, supprimer, fusionner, archiver, créer ». Et : le but d'un
comparatif est de connaître « les avantages et inconvénients de chacune
des possibilités », pas « de l'ingénierie de méthodologie ».

**Tout le reste est PROPOSÉ** par Claude Code : catégories, constats,
architecture, plan. **Rien n'est décidé.**

Méthode : l'inventaire est **calculé**, pas recopié, sur les 163 fichiers, 39634 lignes
suivis par Git. Pour chaque fichier :

- **lignes** ;
- **dernière modification** (`git log -1`) ;
- **rôle**, tiré de son propre en-tête (titre, docstring ou premier
  commentaire) ;
- **lecteurs** : les fichiers du dépôt qui le citent ou l'importent
  (scripts, tests, site, CLAUDE.md, README).

La catégorie et la proposition sont des **jugements**.

---

## 1 — Inventaire

### 1.1 Répartition par catégorie

Définitions :

- **ROBOT** : ce qui produit la géométrie, la simulation ou les données
  du robot.
- **CHOIX** : comparatifs, recherches, catalogue, budget.
- **GOUVERNANCE** : fiches, journal, contrôles, audits, règles,
  états des lieux.
- **SITE** : générateur, gabarits, Docker.
- **OUTILLAGE** : scripts de service, dépendances, tests.

| Catégorie | Fichiers | Lignes | Part des lignes |
| --- | ---: | ---: | ---: |
| GOUVERNANCE | 88 | 22497 | 56.8 % |
| CHOIX | 23 | 8506 | 21.5 % |
| ROBOT | 24 | 4869 | 12.3 % |
| SITE | 12 | 2551 | 6.4 % |
| OUTILLAGE | 16 | 1211 | 3.1 % |

**Lecture.**

- **Plus de la moitié du dépôt est de la gouvernance.** Le journal y
  compte pour 10 039 lignes, les fiches pour 7 083.
- **Le CHOIX dépasse le ROBOT.**
- Le code qui produit **de la géométrie** tient en trois fichiers
  (semelle, profil, plan de découpe) : **1 079 lignes, 2,7 %**, pour
  **une pièce d'apprentissage**.
- Au 29-09 au soir, la gouvernance faisait 66 % et la géométrie 4,5 %.
  La proportion s'est déplacée vers le CHOIX, **pas vers le robot**.

### 1.2 Tableau complet

« Lu par » : les fichiers du dépôt qui le citent ou l'importent. **rien**
signale un fichier que ni script, ni test, ni site, ni consigne ne lit.
C'est normal pour un document de lecture, et c'est un signal pour du
code.

#### Racine — 8 fichiers, 693 lignes

| Fichier | Rôle (tiré de son en-tête) | Lignes | Écriture | Lu par | Modifié | Catégorie | Proposition (§ 3) |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| `.dockerignore` | Sans ce fichier, le contexte de construction embarquerait le venv du | 9 | main | **rien** | 2026-09-28 | SITE | garder |
| `.gitignore` | Généré — jamais versionné (règle 4 de CLAUDE.md) | 37 | main | controle_depot.py | 2026-09-30 | OUTILLAGE | garder |
| `CLAUDE.md` | Instructions — projet YXOR | 341 | main | README.md, parts/semelle_apprentissage.py, apercu_svg.py … | 2026-09-30 | GOUVERNANCE | garder, raccourcir (règles + renvois) |
| `Dockerfile` | YXOR — site statique engendré depuis le dépôt (fiche 0018) | 88 | main | README.md, empreinte.py, regenerer.py … | 2026-09-30 | SITE | garder |
| `README.md` | YXOR | 112 | main | CLAUDE.md | 2026-09-30 | GOUVERNANCE | garder, réécrire (état du robot ; retirer le tableau P1/P2/P3) |
| `nginx.conf` | server { | 22 | main | Dockerfile | 2026-09-28 | SITE | garder |
| `requirements-dev.txt` | Dépendances de DÉVELOPPEMENT SEULEMENT. | 13 | main | verifier_pages.py | 2026-09-29 | OUTILLAGE | garder |
| `requirements.txt` | Phase 1 — simulation seulement. Ni torch ni jax avant décision. | 71 | main | Dockerfile, empreinte.py, verifier_pages.py … | 2026-09-29 | OUTILLAGE | garder |

#### `bom/` — 1 fichiers, 0 lignes

| Fichier | Rôle (tiré de son en-tête) | Lignes | Écriture | Lu par | Modifié | Catégorie | Proposition (§ 3) |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| `bom/.gitkeep` | marqueur de dossier vide | 0 | main | **rien** | 2026-09-20 | ROBOT | supprimer (dossier vide ; à recréer quand une pièce s'assemble) |

#### `decisions/` — 65 fichiers, 7083 lignes

| Fichier | Rôle (tiré de son en-tête) | Lignes | Écriture | Lu par | Modifié | Catégorie | Proposition (§ 3) |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| `decisions/0001-base-toddlerbot.md` | 0001 — ToddlerBot comme base de départ | 55 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | archiver → `decisions/archive/` (remplacée) |
| `decisions/0002-pin-toddlerbot.md` | 0002 — Ancrage de ToddlerBot et environnement bicéphale | 104 | main | CLAUDE.md, import_upstream_limits.py, index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0003-poids-politiques-toddlerbot.md` | 0003 — Provenance des politiques pré-entraînées ToddlerBot | 103 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | archiver → `decisions/archive/` (historique ou close) |
| `decisions/0004-code-amont-dans-le-depot.md` | 0004 — Du code YXOR qui s'exécute avec le venv amont | 82 | main | index_fiches.py (glob), sim/upstream/enregistrer_marche.py, sim/upstream/replay_policy.py … | 2026-09-30 | GOUVERNANCE | archiver → `decisions/archive/` (remplacée) |
| `decisions/0005-topologie-bras-p1.md` | 0005 — Topologie du bras en P1 : celle de ToddlerBot | 131 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | archiver → `decisions/archive/` (remplacée) |
| `decisions/0006-fichier-genere-commite.md` | 0006 — Un fichier généré qui est commité | 102 | main | import_upstream_limits.py, index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0007-sourcing-materiel.md` | 0007 — Sourcing des affirmations sur le matériel | 80 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | archiver → `decisions/archive/` (historique ou close) |
| `decisions/0008-sauvegarde-poids.md` | 0008 — Sauvegarde des poids : manifeste versionné, binaires hors Git | 73 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0009-build123d.md` | 0009 — build123d comme noyau de CAO paramétrique | 113 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0010-origine-des-cotes.md` | 0010 — Traçabilité de l'origine des cotes | 137 | main | audit_origines.py, index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0011-origine-litterature.md` | 0011 — Cinquième origine `litterature`, et filiation de H | 104 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | archiver → `decisions/archive/` (remplacée) |
| `decisions/0012-correction-anthropometry.md` | 0012 — Correction de `anthropometry.yaml` : sources rétablies | 121 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | archiver → `decisions/archive/` (historique ou close) |
| `decisions/0013-nature-des-cotes.md` | 0013 — Nature des cotes : la règle 1 restreinte à son domaine | 92 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0014-pas-d-imprimante-3d.md` | 0014 — Il n'y a pas d'imprimante 3D | 134 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | archiver → `decisions/archive/` (remplacée) |
| `decisions/0015-architecture-plaques-entretoises.md` | 0015 — Architecture en plaques et entretoises, découpe 2D seule | 192 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | archiver → `decisions/archive/` (remplacée) |
| `decisions/0016-plaques-sans-precedent.md` | 0016 — ~~L'architecture en plaques n'a aucun précédent open source~~ | 89 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | archiver → `decisions/archive/` (historique ou close) |
| `decisions/0017-mevita-decoupe-metal.md` | 0017 — MEVITA : la découpe métal a bien un précédent | 110 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | archiver → `decisions/archive/` (historique ou close) |
| `decisions/0018-application-web.md` | 0018 — Application web : un site statique engendré par le dépôt | 178 | main | README.md, index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0019-interface-catalogue.md` | 0019 — Interface : le site devient un catalogue technique | 198 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | archiver → `decisions/archive/` (historique ou close) |
| `decisions/0020-nullite-conditionnelle.md` | 0020 — Trois états de la valeur absente | 71 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0021-machine-x-materiau.md` | 0021 — Séparer la machine du matériau | 148 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | archiver → `decisions/archive/` (historique ou close) |
| `decisions/0022-soudure-instruction.md` | 0022 — La soudure : instruction, sans décision | 138 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | archiver → `decisions/archive/` (historique ou close) |
| `decisions/0023-simulation-navigateur.md` | 0023 — Simuler dans le navigateur, sans rien enregistrer | 85 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | archiver → `decisions/archive/` (historique ou close) |
| `decisions/0024-audit-et-refactorisation.md` | 0024 — Audit du dépôt et plan de refactorisation | 206 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | archiver → `decisions/archive/` (historique ou close) |
| `decisions/0025-mobile-d-abord.md` | 0025 — Le site en mobile d'abord | 160 | main | index_fiches.py (glob) | 2026-10-01 | GOUVERNANCE | archiver → `decisions/archive/` (historique ou close) |
| `decisions/0026-machine-procede-matiere.md` | 0026 — Trois axes ne suffisent pas : la clé composée doit mourir | 277 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0027-regle-phase-6.md` | 0027 — La règle de la « phase 6 » n'a jamais eu de référent | 145 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0028-verification-quatre-affirmations.md` | 0028 — Quatre affirmations d'un retour extérieur, passées au crible | 135 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | archiver → `decisions/archive/` (historique ou close) |
| `decisions/0029-familles-de-licences.md` | 0029 — CERN-OHL-S n'est pas non commerciale : trois familles, pas deux | 90 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | archiver → `decisions/archive/` (remplacée) |
| `decisions/0030-fichiers-fournisseurs.md` | 0030 — Aucun fichier fournisseur non redistribuable dans le dépôt | 91 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0031-torsion-par-section.md` | 0031 — La rigidité en torsion se calcule, elle ne se stocke pas | 128 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | archiver → `decisions/archive/` (historique ou close) |
| `decisions/0032-veille-outils.md` | 0032 — Cinq pistes en veille : notées, pas adoptées | 138 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | archiver → `decisions/archive/` ; résumé d'une ligne dans `docs/veille.md` |
| `decisions/0033-epaisseur-cle-ou-champ.md` | 0033 — L'épaisseur reste un CHAMP : le coût de l'autre choix, chiffré | 157 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0034-ratios-ansur-ii.md` | 0034 — ANSUR II remplace Drillis & Contini | 165 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | archiver → `decisions/archive/` (historique ou close) |
| `decisions/0035-origine-norme.md` | 0035 — Une sixième origine : `norme` | 219 | main | CLAUDE.md, index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | archiver → `decisions/archive/` (historique ou close) |
| `decisions/0036-refonte-des-fiches.md` | 0036 — Refonte des fiches : espèce, cycle de vie, parcours d'entrée | 157 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | archiver → `decisions/archive/` (historique ou close) |
| `decisions/0037-verdict-par-piece.md` | 0037 — Le verdict se calcule par PIÈCE, pas par réglage | 135 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | archiver → `decisions/archive/` (historique ou close) |
| `decisions/0038-dimensionnement-thermique.md` | 0038 — Le facteur limitant n'est pas le couple, c'est la température | 220 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | archiver → `decisions/archive/` (remplacée) |
| `decisions/0039-semelle-porte-capteurs.md` | 0039 — La vraie semelle sera d'abord un porte-capteurs | 53 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | archiver → `decisions/archive/` (historique ou close) |
| `decisions/0040-registre-des-sources.md` | 0040 — Un registre des sources, pas un index de recherche | 128 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0041-incertitude-des-mesures.md` | 0041 — Porter l'incertitude d'une mesure | 132 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0042-rayon-matiere-ou-geste.md` | 0042 — Le rayon minimal : ce que la matière supporte, ou ce que le geste permet ? | 151 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | archiver → `decisions/archive/` (historique ou close) |
| `decisions/0043-profil-de-cannelure-et-lot-mesure.md` | 0043 — Deux matières ou une ? Et ce que le dépôt ne sait pas de la matière qu'on a eue en main | 204 | main | index_fiches.py (glob) | 2026-09-29 | GOUVERNANCE | archiver → `decisions/archive/` (historique ou close) |
| `decisions/0044-variante-carton-ondule.md` | 0044 — La semelle publiée n'est pas celle qui a été coupée | 153 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | archiver → `decisions/archive/` (historique ou close) |
| `decisions/0045-reconstruction-et-amont.md` | 0045 — Aucune géométrie amont ne passe dans un outil de reconstruction | 109 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0046-backflip-reconstruction-veille.md` | 0046 — Backflip AI : une CAO paramétrique reconstruite ? Vérifié, pas adopté | 263 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | archiver → `decisions/archive/` ; résumé d'une ligne dans `docs/veille.md` |
| `decisions/0047-demarche-inversee.md` | 0047 — Démarche inversée : la classe d'actionneur fixe la taille | 38 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0048-tailles-par-classe.md` | 0048 — Tailles Banc, S, M, L, XL ; premier robot S | 29 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0049-scripts-de-chiffrage-versionnes.md` | 0049 — Les scripts de chiffrage sont versionnés, les séries se régénèrent | 30 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | archiver → `decisions/archive/` (historique ou close) |
| `decisions/0050-fabrication-sequencee.md` | 0050 — Fabrication séquencée : usinage, puis impression 3D, puis hybride | 33 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0051-marge-de-securite.md` | 0051 — Marge de sécurité de 1,5 sur le couple, à revoir après le banc | 30 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0052-actionneur-maison.md` | 0052 — Actionneur maison : une piste parallèle, jamais sur le chemin critique | 32 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0053-depot-public.md` | 0053 — Le dépôt passe public | 64 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0054-immuabilite-des-fiches.md` | 0054 — Une fiche acceptée ne se réécrit plus : elle est remplacée | 55 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0055-toddlerbot-reference-et-tailles.md` | 0055 — ToddlerBot, référence de calcul ; les tailles remplacent les paliers | 52 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0056-code-amont-un-seul-sens-verifie.md` | 0056 — Code sous le venv amont : un seul sens est vérifié | 38 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0057-topologie-du-bras-reportee-v2.md` | 0057 — Topologie du bras : celle de la référence ToddlerBot, décision YXOR reportée à la v2 | 30 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0058-filiation-de-h-sans-paliers.md` | 0058 — L'origine `litterature` tient ; la filiation de H ne passe plus par les paliers | 37 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0059-imprimante-etape-deux.md` | 0059 — Pas d'imprimante 3D aujourd'hui ; l'impression est l'étape 2 de la fabrication | 33 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0060-fabrication-sequencee-appliquee.md` | 0060 — Les plaques et entretoises ne sont plus le procédé unique | 43 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0061-licence-amont-deux-familles.md` | 0061 — Trois familles de licences ; la conception de ToddlerBot est dans deux | 43 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0062-dimensionnement-thermique-applique.md` | 0062 — Dimensionner au couple efficace et au seuil thermique : ce qui est appliqué | 46 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0063-aucune-licence-pour-l-instant.md` | 0063 — Aucune licence pour l'instant | 41 | main | index_fiches.py (glob) | 2026-09-30 | GOUVERNANCE | garder (en vigueur) |
| `decisions/0064-valeur-la-plus-prudente.md` | 0064 — Deux valeurs publiées : retenir la plus prudente | 60 | main | index_fiches.py (glob) | 2026-10-01 | GOUVERNANCE | garder (en vigueur) |
| `decisions/index.md` | Index des fiches de décision | 93 | engendré (index_fiches) | README.md, index_fiches.py | 2026-10-01 | GOUVERNANCE | garder (engendré, n'indexe que les fiches en vigueur ; archive listée à part) |

#### `docs/` — 20 fichiers, 6583 lignes

| Fichier | Rôle (tiré de son en-tête) | Lignes | Écriture | Lu par | Modifié | Catégorie | Proposition (§ 3) |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| `docs/arbitrage-2026-09-30.md` | Arbitrage — état des lieux YXOR au 2026-09-30 | 454 | main | CLAUDE.md | 2026-09-30 | CHOIX | archiver → `archive/docs/` (absorbé par le cadrage et `docs/choix/actionneurs.md`) |
| `docs/cadrage.md` | Cadrage du projet YXOR | 532 | main + un bloc engendré (§ 5) | CLAUDE.md, README.md | 2026-10-01 | CHOIX | garder, raccourcir en document de vision ; prose « Damiao devant » réécrite |
| `docs/choix-classe-S.md` | Choix de la classe d'actionneur de S — comparatif multicritère | 200 | engendré puis figé (v1) | selection_multicritere.py | 2026-09-30 | CHOIX | archiver → `archive/docs/` (v1 figée) |
| `docs/choix-famille-actionneurs.md` | Choix de la famille d'actionneurs — comparatif multicritère v2 | 305 | engendré (selection_multicritere) | CLAUDE.md, selection_multicritere.py | 2026-10-01 | CHOIX | fusionner → `docs/choix/actionneurs.md` (format besoin / marché / avantages-inconvénients / pour YXOR) ; l'engendré actuel archivé |
| `docs/choix-interfaces.md` | Choix des interfaces d'actionneur — comparaison rédigée | 105 | main | **rien** | 2026-09-30 | CHOIX | déplacer → `docs/choix/interfaces.md` |
| `docs/comparatif-banc.md` | Comparatif du banc d'essai — v3 | 94 | engendré (selection_multicritere) | CLAUDE.md, selection_multicritere.py | 2026-10-01 | CHOIX | fusionner → `docs/choix/banc.md` ; l'engendré actuel archivé |
| `docs/conclusion-arbitrages-2026-09-30.md` | Conclusion des arbitrages — 29 et 30 septembre 2026 | 230 | main | **rien** | 2026-09-30 | CHOIX | archiver → `archive/docs/` (déjà « remplacée ») |
| `docs/controle-publication-2026-09-30.md` | Contrôle avant publication — 2026-09-30 | 251 | main | README.md | 2026-09-30 | GOUVERNANCE | archiver → `archive/docs/` (contrôle ponctuel, exécuté) |
| `docs/criteres-manquants.md` | Critères manquants du comparatif des familles — proposition | 383 | main | pertes_cuivre.py | 2026-10-01 | CHOIX | fusionner → `docs/choix/actionneurs.md` (les faits A–G deviennent des lignes « marché »), puis archiver |
| `docs/dimensionnement-par-actionneur.md` | Dimensionnement par classe d'actionneur | 359 | mixte (tableaux recopiés de dimensionnement --markdown) | **rien** | 2026-10-01 | CHOIX | fusionner → `docs/robot/besoin-actionnement.md` (le besoin), puis archiver l'instantané |
| `docs/estimation-thermique-j4310.md` | Estimation thermique du Damiao J4310 V1.2 — au bureau, sans achat | 176 | main | estimation_thermique.py | 2026-09-30 | CHOIX | garder → `docs/robot/estimation-thermique-j4310.md` |
| `docs/etat-des-lieux-2026-09-29-nuit.md` | État des lieux — 2026-09-29, nuit | 613 | main | **rien** | 2026-09-29 | GOUVERNANCE | archiver → `archive/docs/` (instantané) |
| `docs/etat-des-lieux-2026-09-29.md` | État des lieux — 2026-09-29 | 499 | main | README.md | 2026-09-29 | GOUVERNANCE | archiver → `archive/docs/` (instantané) |
| `docs/etat-des-lieux-2026-09-30.md` | État des lieux — 2026-09-30 | 828 | main | t:test_enveloppes_help.py | 2026-09-30 | GOUVERNANCE | archiver → `archive/docs/` (instantané) |
| `docs/exigences-actionnement-P2.md` | Exigences d'actionnement — P2, premier chiffrage | 351 | main | **rien** | 2026-09-30 | CHOIX | archiver → `archive/docs/` (fondé sur P2, aboli) |
| `docs/glossaire.md` | Glossaire | 78 | main | README.md | 2026-09-20 | GOUVERNANCE | garder → `docs/glossaire.md`, mettre à jour (« YXOR en a 30 » DDL : v1 = 12) |
| `docs/lecture-modele.md` | Lecture du modèle humanoïde d'exemple de MuJoCo | 107 | main | README.md | 2026-09-20 | ROBOT | déplacer → `docs/robot/lecture-modele.md` |
| `docs/protocole-banc-additions.md` | Protocole du banc — ajouts proposés | 92 | main | **rien** | 2026-10-01 | CHOIX | fusionner → `docs/banc/protocole.md` (après validation) |
| `docs/protocole-banc.md` | Protocole du banc de qualification — *proposé* | 264 | main | selection_multicritere.py | 2026-10-01 | CHOIX | fusionner avec `protocole-banc-additions.md` (après validation) → `docs/banc/protocole.md` |
| `docs/sources/etude-fournisseurs-chatgpt-2026-09-30.md` | 2. RobStride — le candidat naturel pour YXOR | 662 | main | **rien** | 2026-09-30 | CHOIX | garder (étude externe versée telle quelle) |

#### `journal/` — 6 fichiers, 10039 lignes

| Fichier | Rôle (tiré de son en-tête) | Lignes | Écriture | Lu par | Modifié | Catégorie | Proposition (§ 3) |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| `journal/2026-09-20.md` | Journal — 2026-09-20 | 865 | main | controle_depot.py (dates), sim/render.py | 2026-09-20 | GOUVERNANCE | garder ; index des jalons dans `journal/README.md` (nouveau) |
| `journal/2026-09-28.md` | Journal — 2026-09-28 | 2845 | main | controle_depot.py (dates) | 2026-09-30 | GOUVERNANCE | garder ; index des jalons dans `journal/README.md` (nouveau) |
| `journal/2026-09-29-nuit.md` | 2026-09-29, soirée — Le premier objet, et ce qu'il a révélé | 757 | main | controle_depot.py (dates) | 2026-09-29 | GOUVERNANCE | garder ; index des jalons dans `journal/README.md` (nouveau) |
| `journal/2026-09-29.md` | 2026-09-29 — Quatre défauts vus sur un écran, et la limite de la règle 6 | 2335 | main | README.md, controle_depot.py (dates) | 2026-09-30 | GOUVERNANCE | garder ; index des jalons dans `journal/README.md` (nouveau) |
| `journal/2026-09-30.md` | Journal — 2026-09-30 | 2700 | main | CLAUDE.md, README.md, controle_depot.py … | 2026-09-30 | GOUVERNANCE | garder ; index des jalons dans `journal/README.md` (nouveau) |
| `journal/2026-10-01.md` | Journal — 2026-10-01 | 537 | main | controle_depot.py (dates) | 2026-10-01 | GOUVERNANCE | garder ; index des jalons dans `journal/README.md` (nouveau) |

#### `params/` — 14 fichiers, 5053 lignes

| Fichier | Rôle (tiré de son en-tête) | Lignes | Écriture | Lu par | Modifié | Catégorie | Proposition (§ 3) |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| `params/actionneurs.yaml` | Catalogue des actionneurs candidats — lu par scripts/dimensionnement.py | 1040 | main | README.md, dimensionnement.py, estimation_thermique.py … | 2026-10-01 | CHOIX | garder |
| `params/anthropometry.yaml` | Source de vérité dimensionnelle du projet YXOR. | 218 | main | CLAUDE.md, README.md, parts/semelle_apprentissage.origines.yaml … | 2026-09-30 | ROBOT | garder |
| `params/banc.yaml` | Configurations du banc — SOURCE UNIQUE (2026-10-01, lot E, point 1) | 68 | main | dimensionnement.py, selection_multicritere.py | 2026-10-01 | CHOIX | garder |
| `params/budget.yaml` | Budget par phase — lu par scripts/dimensionnement.py | 158 | main | dimensionnement.py, selection_multicritere.py | 2026-10-01 | CHOIX | garder |
| `params/ckpts.manifest.yaml` | Manifeste des poids ToddlerBot — SAUVEGARDE HORS GIT | 57 | engendré (ckpts_backup) | README.md, ckpts_backup.py | 2026-09-30 | ROBOT | garder |
| `params/criteres_selection.yaml` | Critères de sélection — lus par scripts/selection_multicritere.py | 544 | main | estimation_thermique.py, selection_multicritere.py | 2026-10-01 | CHOIX | selon le sort du moteur de notation (§ 3.4) : archiver ou réduire aux faits |
| `params/fournisseurs.yaml` | Provenance des fichiers fournisseurs — voir decisions/0030. | 275 | main | CLAUDE.md, audit_origines.py, controle_depot.py … | 2026-09-30 | GOUVERNANCE | garder |
| `params/hardware.yaml` | Cotes FIXES. Ne suivent jamais H : une vis M3 reste une vis M3 que le robot | 428 | main | CLAUDE.md, parts/semelle_apprentissage.origines.yaml, parts/semelle_apprentissage.py … | 2026-09-30 | ROBOT | garder |
| `params/joints.yaml` | Nomenclature des articulations. `nom` fait foi partout : CAO, URDF, code de | 593 | main | CLAUDE.md, README.md, import_upstream_limits.py … | 2026-09-28 | ROBOT | garder |
| `params/mesures.yaml` | Les ACTES DE MESURE — voir decisions/0041. | 159 | main | audit_origines.py, estimation_thermique.py, selection_multicritere.py | 2026-09-30 | ROBOT | garder |
| `params/nullites.yaml` | Pourquoi telle valeur est absente — voir decisions/0020-nullite-conditionnelle.md | 129 | main | README.md, audit_origines.py, controle_regles.py … | 2026-09-30 | GOUVERNANCE | garder |
| `params/origines.yaml` | Déclaration d'origine des cotes — voir decisions/0010-origine-des-cotes.md | 699 | main | README.md, parts/semelle_apprentissage.py, audit_origines.py … | 2026-10-01 | GOUVERNANCE | garder |
| `params/sources.yaml` | Registre des sources documentaires — voir decisions/0040. | 163 | main | audit_origines.py, source.py | 2026-09-29 | GOUVERNANCE | garder |
| `params/upstream_joints.generated.yaml` | ╔══════════════════════════════════════════════════════════════════╗ | 522 | engendré (import_upstream_limits) | README.md, import_upstream_limits.py | 2026-09-28 | ROBOT | garder (engendré commité, fiche 0006) |

#### `parts/` — 3 fichiers, 658 lignes

| Fichier | Rôle (tiré de son en-tête) | Lignes | Écriture | Lu par | Modifié | Catégorie | Proposition (§ 3) |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| `parts/.gitkeep` | marqueur de dossier vide | 0 | main | **rien** | 2026-09-20 | ROBOT | supprimer (marqueur vide, recréable ; le dossier contient déjà des fichiers) |
| `parts/semelle_apprentissage.origines.yaml` | Relevé d'origines — GÉNÉRÉ, ne pas éditer à la main. | 129 | engendré (la pièce) | audit_origines.py, regenerer.py (glob parts/*.origines.yaml) | 2026-09-30 | ROBOT | garder |
| `parts/semelle_apprentissage.py` | Semelle d'apprentissage — première pièce YXOR. | 529 | main | README.md, parts/semelle_apprentissage.origines.yaml | 2026-09-30 | ROBOT | garder |

#### `robot/` — 1 fichiers, 0 lignes

| Fichier | Rôle (tiré de son en-tête) | Lignes | Écriture | Lu par | Modifié | Catégorie | Proposition (§ 3) |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| `robot/.gitkeep` | marqueur de dossier vide | 0 | main | **rien** | 2026-09-20 | ROBOT | supprimer (dossier vide ; à recréer quand une pièce s'assemble) |

#### `scripts/` — 24 fichiers, 7234 lignes

| Fichier | Rôle (tiré de son en-tête) | Lignes | Écriture | Lu par | Modifié | Catégorie | Proposition (§ 3) |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| `scripts/analyser_marche.py` | Analyse d'une marche enregistrée : couples, vitesses, écrêtage, par actionneur. | 173 | main | dimensionnement.py, pertes_cuivre.py, selection_multicritere.py … | 2026-09-30 | ROBOT | garder |
| `scripts/apercu_svg.py` | Aperçu PNG d'un schéma SVG engendré, pour le regarder sans navigateur. | 61 | main | **rien** | 2026-09-28 | SITE | garder (outil manuel cité au journal) |
| `scripts/audit_origines.py` | Répond à une seule question : quelles cotes viennent de ToddlerBot ? | 414 | main | README.md, parts/semelle_apprentissage.py, controle_regles.py … | 2026-09-29 | GOUVERNANCE | garder |
| `scripts/check_cad_toolchain.py` | Vérifie que la chaîne CAO exporte bien en millimètres, à l'échelle 1:1. | 160 | main | **rien** | 2026-09-28 | OUTILLAGE | garder |
| `scripts/ckpts_backup.py` | Manifeste et vérification des poids ToddlerBot — sauvegarde hors Git. | 193 | main | **rien** | 2026-09-30 | OUTILLAGE | garder |
| `scripts/controle_depot.py` | Rien de binaire dans Git — la règle 4, vérifiée sur TOUT le dépôt. | 211 | main | README.md, regenerer.py | 2026-09-30 | GOUVERNANCE | garder |
| `scripts/controle_regles.py` | Une règle qui ne correspond à rien — le garde-fou qu'on croit avoir. | 269 | main | CLAUDE.md, regenerer.py | 2026-09-29 | GOUVERNANCE | garder |
| `scripts/dimensionnement.py` | Dimensionnement INVERSE : quelle taille maximale pour une classe d'actionneur ? | 564 | main | CLAUDE.md, pertes_cuivre.py, selection_multicritere.py … | 2026-10-01 | CHOIX | garder |
| `scripts/empreinte.py` | L'empreinte du site — une ligne, à comparer avec le pied de page. | 74 | main | CLAUDE.md, parts/semelle_apprentissage.py, pages.py … | 2026-09-30 | SITE | garder |
| `scripts/enveloppes_actionneurs.py` | Enveloppes de couple, vitesse et amplitude par articulation. | 323 | main | t:test_enveloppes_help.py | 2026-09-30 | CHOIX | archiver → `archive/scripts/` (objectif « 2 à 4 classes » remplacé ; sortie lue par rien) |
| `scripts/estimation_thermique.py` | Estimation thermique du Damiao J4310 V1.2 : un k estimé AU BUREAU, sans achat. | 166 | main | selection_multicritere.py | 2026-09-30 | CHOIX | garder |
| `scripts/import_upstream_limits.py` | Extrait axes et butées des 30 articulations depuis le modèle amont épinglé. | 361 | main | analyser_marche.py, enveloppes_actionneurs.py | 2026-09-28 | ROBOT | garder |
| `scripts/index_fiches.py` | Index des fiches de décision — ENGENDRÉ, jamais saisi. | 174 | main | regenerer.py, t:test_index_fiches.py, t:test_index_remplacee.py | 2026-09-30 | GOUVERNANCE | garder |
| `scripts/nullites.py` | Pourquoi une valeur est absente — fiche 0020. | 106 | main | pages.py, regenerer.py | 2026-09-29 | GOUVERNANCE | garder |
| `scripts/pages.py` | Gabarits du site — tout le HTML, et rien d'autre. | 719 | main | regenerer.py, verifier_pages.py | 2026-09-30 | SITE | garder |
| `scripts/pertes_cuivre.py` | Pertes cuivre par candidat, sur la marche de référence — INFORMATION, pas un critère. | 175 | main | **rien** | 2026-10-01 | CHOIX | garder |
| `scripts/plan_decoupe.py` | Plan de découpe imprimable A4, à l'échelle 1:1, à scotcher sur la matière. | 333 | main | parts/semelle_apprentissage.py, pages.py, regenerer.py | 2026-09-29 | ROBOT | garder |
| `scripts/procedes.py` | Chargeur des quatre tables de `hardware.yaml` — fiches 0026 et 0033. | 140 | main | parts/semelle_apprentissage.py, controle_regles.py, pages.py … | 2026-09-29 | ROBOT | garder |
| `scripts/profil.py` | Contour de la semelle, calculé SANS noyau CAO. | 217 | main | parts/semelle_apprentissage.py, web/simulateur.js | 2026-09-29 | ROBOT | garder |
| `scripts/ratios_ansur.py` | Ratios anthropométriques recalculés depuis ANSUR II (2012). | 283 | main | t:test_ratios_ansur.py | 2026-09-30 | OUTILLAGE | garder |
| `scripts/regenerer.py` | Régénère TOUT : les pièces, puis le site statique. | 439 | main | CLAUDE.md, Dockerfile, README.md … | 2026-09-30 | SITE | garder |
| `scripts/selection_multicritere.py` | Sélection multicritère : classe d'actionneur de S, puis composition du banc. | 1261 | main | dimensionnement.py, estimation_thermique.py, t:test_selection.py … | 2026-10-01 | CHOIX | selon § 3.4 : archiver, ou réduire à un tableau de faits sans notes |
| `scripts/source.py` | Lecture des sources documentaires — un registre, pas un moteur de recherche. | 213 | main | **rien** | 2026-09-29 | GOUVERNANCE | garder |
| `scripts/verifier_pages.py` | Mesurer les pages pour de bon — Chromium sans interface. | 205 | main | **rien** | 2026-09-29 | SITE | archiver → `archive/scripts/` (n'a jamais tourné avec succès : pas de Chromium) |

#### `sim/` — 7 fichiers, 903 lignes

| Fichier | Rôle (tiré de son en-tête) | Lignes | Écriture | Lu par | Modifié | Catégorie | Proposition (§ 3) |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| `sim/.gitkeep` | marqueur de dossier vide | 0 | main | **rien** | 2026-09-20 | ROBOT | supprimer (marqueur vide, recréable ; le dossier contient déjà des fichiers) |
| `sim/models/humanoid.xml` | <!-- Copyright 2021 DeepMind Technologies Limited | 267 | main | README.md, sim/view.py | 2026-09-20 | ROBOT | archiver → `archive/sim/` (modèle d'exemple DeepMind, lu par rien de YXOR) |
| `sim/render.py` | Rendu hors écran d'un modèle MJCF vers un PNG, sans fenêtre. | 89 | main | **rien** | 2026-09-20 | ROBOT | garder (rendu hors écran, CLAUDE.md) ; préciser le venv dans la docstring |
| `sim/upstream/enregistrer_marche.py` | Enregistre une marche ToddlerBot : couples ET vitesses d'actionneur, sans rendu. | 108 | main | analyser_marche.py, dimensionnement.py, pertes_cuivre.py … | 2026-09-30 | ROBOT | garder |
| `sim/upstream/replay_policy.py` | Rejoue une politique ToddlerBot en boucle fermée et écrit une vidéo. | 175 | main | sim/upstream/enregistrer_marche.py | 2026-09-29 | ROBOT | garder |
| `sim/upstream/toddlerbot_fixes.py` | Correctifs nécessaires pour exécuter une politique ToddlerBot en boucle fermée. | 223 | main | sim/upstream/enregistrer_marche.py, sim/upstream/replay_policy.py | 2026-09-28 | ROBOT | garder |
| `sim/view.py` | Ouvre le viewer interactif MuJoCo sur un modèle MJCF. | 41 | main | **rien** | 2026-09-20 | ROBOT | garder ; préciser le venv |

#### `tests/` — 10 fichiers, 454 lignes

| Fichier | Rôle (tiré de son en-tête) | Lignes | Écriture | Lu par | Modifié | Catégorie | Proposition (§ 3) |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| `tests/test_construction_deterministe.py` | Deux régénérations à deux dates différentes donnent la même empreinte. | 60 | main | `unittest discover` (à la main) | 2026-09-30 | OUTILLAGE | garder |
| `tests/test_dimensionnement_coherence.py` | Le contrôle de cohérence du dimensionnement doit savoir ÉCHOUER. | 53 | main | `unittest discover` (à la main) | 2026-09-30 | OUTILLAGE | garder |
| `tests/test_empreinte.py` | L'empreinte doit changer quand requirements.txt change. | 44 | main | `unittest discover` (à la main) | 2026-09-30 | OUTILLAGE | garder |
| `tests/test_enveloppes_help.py` | `enveloppes_actionneurs.py --help` doit afficher l'aide et N'ÉCRIRE RIEN. | 35 | main | `unittest discover` (à la main) | 2026-09-30 | OUTILLAGE | garder |
| `tests/test_index_fiches.py` | index_fiches doit lire TOUTES les lignes « Amendée par » d'une fiche. | 37 | main | `unittest discover` (à la main) | 2026-09-30 | OUTILLAGE | garder |
| `tests/test_index_remplacee.py` | index_fiches doit lire « Remplacée par » et refuser un remplacement non réciproque. | 67 | main | `unittest discover` (à la main) | 2026-09-30 | OUTILLAGE | garder |
| `tests/test_ratios_ansur.py` | La colonne D&C de ratios_ansur doit montrer Drillis & Contini, pas le YAML. | 38 | main | `unittest discover` (à la main) | 2026-09-30 | OUTILLAGE | garder |
| `tests/test_regenerer_index.py` | regenerer.py doit échouer quand index_fiches échoue. | 34 | main | `unittest discover` (à la main) | 2026-09-30 | OUTILLAGE | garder |
| `tests/test_selection.py` | Un candidat ÉLIMINÉ ne peut pas gagner, quels que soient ses notes et les poids. | 39 | main | `unittest discover` (à la main) | 2026-09-30 | OUTILLAGE | suit le sort du moteur de notation (§ 3.4) |
| `tests/test_tension_banc.py` | La tension d'une configuration de banc = la tension COMMUNE de ses modèles. | 47 | main | `unittest discover` (à la main) | 2026-10-01 | OUTILLAGE | suit le sort du moteur de notation (§ 3.4) |

#### `web/` — 4 fichiers, 934 lignes

| Fichier | Rôle (tiré de son en-tête) | Lignes | Écriture | Lu par | Modifié | Catégorie | Proposition (§ 3) |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| `web/simulateur.js` | /* Simulation en direct — fiche 0023. | 357 | main | pages.py, plan_decoupe.py, regenerer.py | 2026-09-29 | SITE | garder |
| `web/style.css` | /* Feuille de style — le cœur de la page pièce est la TRAÇABILITÉ. | 279 | main | pages.py, regenerer.py | 2026-09-29 | SITE | garder |
| `web/viewer.js` | /* Visualiseur STL — WebGL brut, aucune dépendance, aucun CDN. | 164 | main | pages.py, regenerer.py | 2026-09-28 | SITE | garder |
| `web/zoom.js` | /* Zoom du dessin seul — fiche 0025. | 134 | main | pages.py, regenerer.py | 2026-09-29 | SITE | garder |

---

## 2 — Constats

### 2.1 Doublons et recoupements

| Sujet | Documents qui le traitent | Constat |
| --- | --- | --- |
| **Ce qu'est YXOR et où il en est** | `README.md`, `docs/cadrage.md`, `docs/arbitrage-2026-09-30.md`, `docs/conclusion-arbitrages-2026-09-30.md`, trois `docs/etat-des-lieux-*`, `CLAUDE.md` (§ Méthode) | **sept points d'entrée**. Aucun ne dit seul où en est le robot aujourd'hui |
| **Choix de l'actionneur de S** | `cadrage.md` §§ 5-9, `choix-classe-S.md` (v1), `choix-famille-actionneurs.md`, `criteres-manquants.md`, `estimation-thermique-j4310.md`, `params/actionneurs.yaml`, `params/criteres_selection.yaml` | le raisonnement est éclaté ; le verdict du jour n'est que dans un document engendré |
| **Le banc** | `comparatif-banc.md` § 5, `protocole-banc.md`, `protocole-banc-additions.md`, `params/banc.yaml`, `params/budget.yaml` (phase banc), cadrage § 6 et § 13 q12 | **trois textes de protocole**, dont un non validé |
| **Dimensionnement** | `dimensionnement-par-actionneur.md` (tableaux recopiés), bloc du cadrage § 5, `exigences-actionnement-P2.md` | trois présentations d'un même calcul ; une seule est engendrée au bon endroit (le bloc du cadrage) |
| **Règles de fonctionnement** | `CLAUDE.md` (341 lignes), fiches 0010, 0013, 0020, 0027, 0035, 0036, 0054, 0064, journal | les règles vivent à la fois dans CLAUDE.md et dans les fiches, avec des renvois croisés |

### 2.2 Documents qui se contredisent encore

| Où | Contradiction | Avec |
| --- | --- | --- |
| `README.md:8-14` | « déclinable en trois paliers », tableau P1/P2/P3 | fiche 0055 (les tailles remplacent les paliers) |
| `docs/cadrage.md` §§ 6, 9, 13 | prose « Damiao devant », sous une note datée qui la contredit | recalcul en 48 V (`choix-famille-actionneurs.md`) |
| `docs/glossaire.md:8` | « YXOR en a 30 » degrés de liberté | cadrage § 11 : la v1 en a 12 |
| `requirements.txt:1` | « Phase 1 — simulation seulement » | les « phases » n'existent plus (0027) |
| `params/budget.yaml:96` | structure : « plaques et entretoises découpées (fiche 0015) » | 0015 remplacée par 0060 (fabrication séquencée) |
| `params/hardware.yaml:403` | « Jeremy en achète une cette semaine » (imprimante) | 0059 : aucune imprimante vérifiée |
| fiches 0010, 0013 | raisonnent en paliers et en « P3 » | 0055, 0058 |

### 2.3 Code jamais exécuté, ou que plus rien ne lit

| Fichier | Constat |
| --- | --- |
| `scripts/verifier_pages.py` | **n'a jamais tourné avec succès** (pas de Chromium) ; lu par rien |
| `scripts/enveloppes_actionneurs.py` | son objectif, « 30 moteurs → 2 à 4 classes », est remplacé (0062) ; ses sorties (`enveloppes.json`, `couples_balancement.csv`) ne sont lues par rien |
| `web/simulateur.js` | le site s'affiche sur iPhone et PC (Jeremy, 2026-10-01), mais **le simulateur lui-même n'a jamais été vu fonctionner** |
| `sim/models/humanoid.xml`, `sim/render.py`, `sim/view.py` | outils de démonstration du 20-09 sur le modèle d'exemple DeepMind ; rien de YXOR ne les lit |
| `params/actionneurs.yaml`, section `collecte_criteres_manquants` | lue seulement par `pertes_cuivre.py`, pour information |
| `parts/.gitkeep`, `sim/.gitkeep` | marqueurs de dossier vide dans des dossiers qui ne le sont plus |
| `robot/.gitkeep`, `bom/.gitkeep` | dossiers vides depuis le 20-09 : **aucun assemblage, aucune nomenclature** |

### 2.4 Instantanés périmés

`etat-des-lieux-2026-09-29.md`, `…-29-nuit.md`, `…-30.md` (le README
cite encore le premier comme inventaire),
`conclusion-arbitrages-2026-09-30.md` (déjà « remplacée »),
`choix-classe-S.md` (v1 figée), `exigences-actionnement-P2.md` (P2
aboli), `dimensionnement-par-actionneur.md` (régénéré à la main deux
fois), `controle-publication-2026-09-30.md` (exécuté).

### 2.5 Propositions jamais appliquées

- **0035**, origine `norme` : acceptée, rien d'appliqué.
- **0045 et 0046** : non outillées (assumé).
- **0052**, actionneur maison : rien de conçu.
- **Cadrage § 8 bis**, interfaces d'actionneur : couche
  `joint.command`, interface mécanique ; rien.
- **`criteres-manquants.md`** (01-10) : rien d'intégré.
- **`protocole-banc-additions.md`** (01-10) : non validé.
- **Le chien de garde en préalable du banc** : proposé.
- **La 0024**, rangs 2 et 3, en partie seulement.
- **La couche logicielle**, démarrable « avant tout achat » : jamais
  commencée.

### 2.6 La méthode de notation, au regard de la demande de Jeremy

Le moteur de notation pèse **1 261 lignes** (`selection_multicritere.py`),
plus 544 de grilles et de poids (`criteres_selection.yaml`), plus deux
documents engendrés et deux tests.

En 24 heures, son verdict a oscillé entre **quatre** gagnants possibles :

1. Damiao en tête, notée en 24 V ;
2. RobStride avec EduLite 05, en 48 V ;
3. Damiao, si la garantie revendeur compte ;
4. CubeMars, sous des poids quelconques (34,7 % des tirages à k = 1,0, contre 30,6 % à RobStride EduLite 05).

Chaque bascule tenait à une **hypothèse de notation**, pas à un fait
nouveau sur un actionneur. **Une partie des corrections du 30-09 au
01-10 a porté sur l'outil lui-même**, et non sur le robot : biais du
« prudent », grille de capacité, décisivité, attributions, tension.

Ce que Jeremy demande, les avantages et les inconvénients de chaque
possibilité, est déjà **contenu dans les faits collectés**. Ces faits
sont noyés dans une note pondérée.

---

## 3 — Proposition d'architecture cible

**Principe** :

- **le code ne bouge presque pas**. Le Dockerfile copie `params/`,
  `parts/`, `scripts/` et `web/`, l'empreinte hache ces quatre dossiers,
  et tous les scripts y résolvent leurs chemins ;
- **les documents et les fiches se rangent** ;
- **rien n'est supprimé**, sauf quatre marqueurs vides : tout le reste
  part dans `archive/`.

### 3.1 Arborescence

```
README.md                 où en est le robot, comment régénérer, quoi lire (≤ 1 page)
CLAUDE.md                 règles non négociables + renvois (raccourci)
Dockerfile  nginx.conf  .dockerignore  .gitignore  requirements*.txt
params/                   INCHANGÉ (lu par le Dockerfile, l'empreinte, tous les scripts)
parts/                    pièces (la semelle)
scripts/                  INCHANGÉ en place (imports à plat) ; code mort → archive/scripts/
sim/                      simulation ; upstream/ inchangé (venv amont, 0004/0056)
web/                      sources du site
tests/
docs/
  README.md               NOUVEAU : plan de lecture en 5 lignes
  cadrage.md              vision, méthode, tailles (raccourci)
  robot/                  besoin-actionnement.md, estimation-thermique-j4310.md, lecture-modele.md
  choix/                  UN document par choix ouvert, au format du § 3.3
    actionneurs.md        famille de S
    banc.md               composition du banc
    interfaces.md         interfaces d'actionneur
  banc/
    protocole.md          protocole + ajouts, une fois validés
  glossaire.md
  veille.md               NOUVEAU : les pistes en veille (ex-0032, 0046), une ligne chacune
  sources/                études externes versées telles quelles
decisions/                fiches EN VIGUEUR + index.md (engendré)
  archive/                fiches remplacées, historiques, closes, de veille
journal/                  inchangé + README.md (index des jalons, une ligne chacun)
archive/
  docs/                   instantanés et documents absorbés
  scripts/                enveloppes_actionneurs.py, verifier_pages.py (+ moteur de notation, si § 3.4 a)
  sim/                    models/humanoid.xml
```

**Bilan, fichier par fichier** (colonne « Proposition » du § 1.2) :
garder 104, archiver 43, fusionner 6, supprimer 4, déplacer 2, selon 2, suit 2.

### 3.2 Ce que deviennent les fiches

64 fiches : **32 en vigueur** gardées ; **8 remplacées**, **22 historiques ou closes** et **2 de veille**, archivées.

- **En vigueur** : 0002, 0006, 0008, 0009, 0010, 0013, 0018, 0020, 0026, 0027, 0030, 0033, 0040, 0041, 0045, 0047, 0048, 0050, 0051, 0052, 0053, 0054, 0055, 0056, 0057, 0058, 0059, 0060, 0061, 0062, 0063, 0064.
- **Archivées** : 0001, 0003, 0004, 0005, 0007, 0011, 0012, 0014, 0015, 0016, 0017, 0019, 0021, 0022, 0023, 0024, 0025, 0028, 0029, 0031, 0032, 0034, 0035, 0036, 0037, 0038, 0039, 0042, 0043, 0044, 0046, 0049.

Règles proposées :

- **archiver n'est pas réécrire.** Le fichier est déplacé par `git mv`,
  donc son historique est gardé, et son texte n'est pas touché (0054) ;
- `index_fiches.py` liste les fiches en vigueur, puis l'archive, à
  part ;
- les renvois `Remplace` / `Remplacée par` restent valides, l'index
  cherchant dans les deux dossiers.

**Seuil d'entrée pour une fiche future** (proposé). Une fiche n'est
écrite que si les deux conditions sont réunies :

1. la décision est **de Jeremy, avec ses mots** (règles 6 et 7) ;
2. elle est **structurante** : elle change une interface, un paramètre
   partagé, une règle de travail, ou elle engage un achat ou une
   fabrication.

Sinon, **une ligne au journal suffit**.

Format proposé : une page au plus, avec la décision, le pourquoi, les
alternatives écartées, ce qui la rouvrirait et la source. Une seule
espèce d'en-tête suffit (État, Remplacée par).

### 3.3 Le format des comparatifs

**« Besoin, marché, avantages et inconvénients, pour YXOR »**, un
document par choix (`docs/choix/<sujet>.md`).

1. **Besoin**, chiffré et engendré : ce que le robot demande, par
   exemple couple RMS et pointe par articulation à la taille S, marge
   1,5. Source : `dimensionnement.py`.
2. **Marché**, sous forme de tableau de faits sourcés et datés, une
   ligne par candidat : couple, masse, prix, tension, protocole,
   garantie, chien de garde, jeu, réversibilité, charges, documentation.
   Une valeur absente s'écrit « non publié ». Source : `actionneurs.yaml`
   et la collecte.
3. **Avantages et inconvénients**, rédigés, quatre à six lignes par
   candidat, chacune adossée à une ligne du marché. Exemple : « EduLite
   05 : le moins cher, même bus que M et L ; mais aucune valeur au
   blocage publiée, et chien de garde désactivé en usine ».
4. **Pour YXOR** : ce qui est déjà tranché par les faits ; ce qui reste
   inconnu et **ce que le banc tranchera** ; ce que Jeremy doit
   arbitrer (approvisionnement contre technique, par exemple).

**Pas de score pondéré dans le corps du document.** La carte k × k et la
sensibilité peuvent rester en **annexe**, comme information.

### 3.4 Ce que deviennent les scripts de notation

Deux options, **sans choix** : c'est à Jeremy de décider.

- **(a) Archiver le moteur de notation** : `selection_multicritere.py`,
  `criteres_selection.yaml`, `test_selection.py` et
  `test_tension_banc.py` partent dans `archive/scripts/`.
  - Un script court, `tableau_faits.py`, engendre les tableaux « besoin »
    et « marché » du § 3.3 depuis `dimensionnement.py` et
    `actionneurs.yaml` : tailles prudente et optimiste par famille,
    coûts, faits A à G.
  - Ce qui calcule des grandeurs physiques reste : `dimensionnement.py`,
    `estimation_thermique.py`, `pertes_cuivre.py`, `analyser_marche.py`.
- **(b) Garder le moteur, en annexe.** Le document principal suit le
  § 3.3, et la note pondérée n'apparaît qu'en annexe, comme
  « sensibilité ». C'est moins de travail, mais l'outil continue de
  demander de l'entretien.

---

## 4 — Risques : ce que la refonte peut casser, et comment le vérifier

| Risque | Pourquoi | Vérification |
| --- | --- | --- |
| **Construction Docker** | `Dockerfile:57-64` copie `requirements.txt`, `params/`, `parts/`, `scripts/` et `web/`. Déplacer l'un d'eux casse la construction | ne pas déplacer ces dossiers (proposé) ; sinon, construire l'image en local avant de pousser |
| **Empreinte dépôt = site** | `empreinte.py:49` hache `params`, `parts`, `scripts`, `web` et `requirements.txt` | empreinte avant et après chaque lot. **Un lot qui ne touche que `docs/`, `decisions/`, `journal/` et `archive/` doit la laisser inchangée** |
| **Index des fiches** | `index_fiches.py:69` ne lit que `decisions/*.md`. Une fiche archivée citée par `Remplace` serait « introuvable », ce qui produirait un **refus** | adapter l'index (lecture de `archive/`) **avant** de déplacer ; le test `test_index_remplacee` doit couvrir ce cas |
| **Audit d'origine** | `origines.yaml` est indexé par **nom de fichier** de `params/`. Renommer un fichier de `params/` y rend toutes ses valeurs « non qualifiées » | ne pas renommer `params/*.yaml` ; audit strict avant et après, avec le **même nombre de valeurs** |
| **Contrôle du dépôt** | `controle_depot.py` vérifie les dates des journaux et les binaires sur les fichiers suivis | lancé par `regenerer.py` ; nombre de fichiers suivis annoncé avant et après |
| **Tests** | les tests résolvent `scripts/` par `parents[1]` ; `test_selection` et `test_tension_banc` dépendent du moteur | `unittest discover` à chaque lot ; si § 3.4 a, archiver ces tests **dans le même lot** que le moteur |
| **Liens Markdown** | README, CLAUDE.md, cadrage et fiches se citent par chemin relatif ; déplacer `docs/*` les casse en silence | **proposé** : un petit contrôle de liens qui annonce combien il en a vérifié ; zéro lien mort à chaque lot |
| **Historique** | un déplacement sans `git mv` perd le suivi du fichier | `git mv` seulement ; `git log --follow` sur un échantillon |
| **Site** | il ne sert ni `docs/` ni `decisions/` ; seuls la pièce et la traçabilité sont projetées | `regenerer.py` : « 5 pages », structure HTML équilibrée ; empreinte relue sur yxor.fr |

---

## 5 — Plan en lots ordonnés (proposé)

Chaque lot fait un commit au moins et se clôt par : `regenerer.py`,
`unittest`, audit strict, et empreinte relue sur le site.

| Lot | Contenu | Ce qu'il vérifie en plus |
| --- | --- | --- |
| **R0, mesure de référence** | étiquette `avant-refonte` ; on relève l'empreinte, le nombre de valeurs auditées, de motifs, de tests, de pages et de fiches ; contrôle de liens (proposé) écrit et lancé | les chiffres de départ, consignés au journal |
| **R1, archive des instantanés** | `git mv` des documents « archiver » de `docs/` vers `archive/docs/` ; liens mis à jour (README, CLAUDE.md, cadrage) | empreinte **inchangée** ; zéro lien mort ; aucun script ne lisait ces fichiers |
| **R2, fiches** | `index_fiches.py` lit `decisions/archive/` (test vu échouer d'abord) ; `git mv` des fiches à archiver ; `docs/veille.md` | 64 fiches toujours comptées (en vigueur + archive) ; aucun `Remplace` introuvable ; empreinte **changée** (le script) puis égale au site |
| **R3, points d'entrée** | README réécrit (sans P1/P2/P3), `docs/README.md`, `journal/README.md`, CLAUDE.md raccourci (règles inchangées, renvois mis à jour) | relu par Jeremy ; liens |
| **R4, comparatifs au nouveau format** | `docs/choix/actionneurs.md`, `banc.md`, `interfaces.md` : besoin, marché, avantages et inconvénients, pour YXOR ; les anciens engendrés passent en archive | chaque avantage ou inconvénient cite une ligne du marché ; aucun chiffre hors de `params/` |
| **R5, sort de la notation** | **décision de Jeremy** (§ 3.4, une fiche si elle est structurante), puis application | tests adaptés dans le même lot ; empreinte |
| **R6, code mort** | `git mv` vers `archive/scripts/` et `archive/sim/` ; suppression des quatre `.gitkeep` ; venv précisé dans `sim/render.py` et `sim/view.py` | `regenerer.py`, tests ; aucun import cassé (grep) |
| **R7, contradictions résiduelles** | glossaire, `requirements.txt` (« Phase 1 »), `budget.yaml` (structure), `hardware.yaml` (imprimante), prose du cadrage | audit strict ; le diagnostic du § 2.2 relancé, qui doit être vide |

**Hors refonte, et pourtant ce qui ferait avancer le robot** :

- la couche logicielle `joint.command` et son backend MuJoCo, faisables
  sans achat ;
- le choix d'actionneur, puis le banc.

La refonte devrait rester **courte** par rapport à ces deux chantiers.
