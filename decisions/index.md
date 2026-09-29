# Index des fiches de décision

**Engendré** par `scripts/index_fiches.py` — ne pas éditer à la
main. Le régénérer fait partie de `scripts/regenerer.py`.

Une fiche n'est jamais réécrite (règle 5) : elle est *amendée*
par une autre, et le renvoi figure dans son en-tête. La colonne
« amendée par » est donc la plus importante du tableau — c'est
elle qui dit ce qu'il ne faut plus croire.

## Par où commencer

Sept fiches suffisent avant d'écrire une ligne. Les autres se
lisent quand leur question se pose.

1. [0010](0010-origine-des-cotes.md) — le contrat du projet : tout le reste en découle
1. [0013](0013-nature-des-cotes.md) — la règle 1 restreinte à son domaine — lue seule, elle fait sous-dimensionner les grandes tailles
1. [0020](0020-nullite-conditionnelle.md) — les trois états de la valeur absente, qui traversent tout
1. [0026](0026-machine-procede-matiere.md) — la structure de hardware.yaml en quatre tables
1. [0033](0033-epaisseur-cle-ou-champ.md) — et pourquoi l'épaisseur y est un champ, pas une clé
1. [0018](0018-application-web.md) — le site est une projection du dépôt, il ne stocke rien
1. [0015](0015-architecture-plaques-entretoises.md) — le seul choix d'architecture MÉCANIQUE — le reste est méthode

| # | Titre | Espèce | État | Date | Amendée par |
| --- | --- | --- | --- | --- | --- |
| [0001](0001-base-toddlerbot.md) | ToddlerBot comme base de départ | historique | appliquée | 2026-09-20 |  |
| [0002](0002-pin-toddlerbot.md) | Ancrage de ToddlerBot et environnement bicéphale | close | appliquée | 2026-09-20 |  |
| [0003](0003-poids-politiques-toddlerbot.md) | Provenance des politiques pré-entraînées ToddlerBot | historique | appliquée | 2026-09-20 |  |
| [0004](0004-code-amont-dans-le-depot.md) | Du code YXOR qui s'exécute avec le venv amont | gouvernante | appliquée | 2026-09-28 |  |
| [0005](0005-topologie-bras-p1.md) | Topologie du bras en P1 : celle de ToddlerBot | close | amendée | 2026-09-28 | **0011** — l'emprunt dimensionnel (H) est adossé au même palier P1 que l'emprunt topolog… |
| [0006](0006-fichier-genere-commite.md) | Un fichier généré qui est commité | close | appliquée | 2026-09-28 |  |
| [0007](0007-sourcing-materiel.md) | Sourcing des affirmations sur le matériel | close | appliquée | 2026-09-28 |  |
| [0008](0008-sauvegarde-poids.md) | Sauvegarde des poids : manifeste versionné, binaires hors Git | close | appliquée | 2026-09-28 |  |
| [0009](0009-build123d.md) | build123d comme noyau de CAO paramétrique | close | amendée | 2026-09-28 | **0029** — CERN-OHL-S y était classée à tort comme non commerciale ; la conclusion de ce… |
| [0010](0010-origine-des-cotes.md) | Traçabilité de l'origine des cotes | gouvernante | amendée | 2026-09-28 | **0011** — cinquième origine litterature, et filiation de H consignée. |
| [0011](0011-origine-litterature.md) | Cinquième origine `litterature`, et filiation de H | close | appliquée | 2026-09-28 |  |
| [0012](0012-correction-anthropometry.md) | Correction de `anthropometry.yaml` : sources rétablies | historique | appliquée | 2026-09-28 |  |
| [0013](0013-nature-des-cotes.md) | Nature des cotes : la règle 1 restreinte à son domaine | gouvernante | appliquée | 2026-09-28 |  |
| [0014](0014-pas-d-imprimante-3d.md) | Il n'y a pas d'imprimante 3D | historique | appliquée | 2026-09-28 |  |
| [0015](0015-architecture-plaques-entretoises.md) | Architecture en plaques et entretoises, découpe 2D seule | close | amendée | 2026-09-28 | **0042** — la règle du rayon minimal ne décrit que ce que la MATIÈRE supporte, pas ce qu…<br>**0016** — aucun projet open source accessible ne suit cette voie ; Solo, Bolt et Upkie … |
| [0016](0016-plaques-sans-precedent.md) | ~~L'architecture en plaques n'a aucun précédent open source~~ | historique | amendée | 2026-09-28 | **0017** — le constat « aucun précédent » est FAUX : MEVITA, MEVIUS et MEVIUS2 construis… |
| [0017](0017-mevita-decoupe-metal.md) | MEVITA : la découpe métal a bien un précédent | historique | appliquée | 2026-09-28 |  |
| [0018](0018-application-web.md) | Application web : un site statique engendré par le dépôt | gouvernante | appliquée | 2026-09-28 |  |
| [0019](0019-interface-catalogue.md) | Interface : le site devient un catalogue technique | close | amendée | 2026-09-28 | **0037** — le verdict dessinable/coupable doit se calculer par pièce, non par réglage. |
| [0020](0020-nullite-conditionnelle.md) | Trois états de la valeur absente | gouvernante | appliquée | 2026-09-29 |  |
| [0021](0021-machine-x-materiau.md) | Séparer la machine du matériau | abandonnee | abandonnée | 2026-09-29 | **0026** — la clé composée ne tient pas à six axes ; migration SUSPENDUE. |
| [0022](0022-soudure-instruction.md) | La soudure : instruction, sans décision | historique | instruction | 2026-09-29 | **0031** — le facteur de rigidité en torsion n'est pas une constante : il se calcule par… |
| [0023](0023-simulation-navigateur.md) | Simuler dans le navigateur, sans rien enregistrer | close | appliquée | 2026-09-29 |  |
| [0024](0024-audit-et-refactorisation.md) | Audit du dépôt et plan de refactorisation | close | appliquée | 2026-09-29 |  |
| [0025](0025-mobile-d-abord.md) | Le site en mobile d'abord | close | appliquée | 2026-09-29 |  |
| [0026](0026-machine-procede-matiere.md) | Trois axes ne suffisent pas : la clé composée doit mourir | close | amendée | 2026-09-29 | **0033** — le chiffrage du choix clé/champ sur nullites.yaml et origines.yaml. |
| [0027](0027-regle-phase-6.md) | La règle de la « phase 6 » n'a jamais eu de référent | close | appliquée | 2026-09-29 |  |
| [0028](0028-verification-quatre-affirmations.md) | Quatre affirmations d'un retour extérieur, passées au crible | historique | appliquée | 2026-09-29 |  |
| [0029](0029-familles-de-licences.md) | CERN-OHL-S n'est pas non commerciale : trois familles, pas deux | historique | appliquée | 2026-09-29 |  |
| [0030](0030-fichiers-fournisseurs.md) | Aucun fichier fournisseur non redistribuable dans le dépôt | gouvernante | appliquée | 2026-09-29 |  |
| [0031](0031-torsion-par-section.md) | La rigidité en torsion se calcule, elle ne se stocke pas | historique | appliquée | 2026-09-29 |  |
| [0032](0032-veille-outils.md) | Cinq pistes en veille : notées, pas adoptées | veille | veille | 2026-09-29 |  |
| [0033](0033-epaisseur-cle-ou-champ.md) | L'épaisseur reste un CHAMP : le coût de l'autre choix, chiffré | gouvernante | appliquée | 2026-09-29 |  |
| [0034](0034-ratios-ansur-ii.md) | ANSUR II remplace Drillis & Contini | historique | appliquée | 2026-09-29 |  |
| [0035](0035-origine-norme.md) | Une sixième origine : `norme` | proposition | acceptée | 2026-09-29 |  |
| [0036](0036-refonte-des-fiches.md) | Refonte des fiches : espèce, cycle de vie, parcours d'entrée | close | appliquée | 2026-09-29 |  |
| [0037](0037-verdict-par-piece.md) | Le verdict se calcule par PIÈCE, pas par réglage | close | appliquée | 2026-09-29 |  |
| [0038](0038-dimensionnement-thermique.md) | Le facteur limitant n'est pas le couple, c'est la température | proposition | proposée | 2026-09-29 |  |
| [0039](0039-semelle-porte-capteurs.md) | La vraie semelle sera d'abord un porte-capteurs | historique | appliquée | 2026-09-29 |  |
| [0040](0040-registre-des-sources.md) | Un registre des sources, pas un index de recherche | gouvernante | appliquée | 2026-09-29 |  |
| [0041](0041-incertitude-des-mesures.md) | Porter l'incertitude d'une mesure | proposition | proposée | 2026-09-29 |  |
| [0042](0042-rayon-matiere-ou-geste.md) | Le rayon minimal : ce que la matière supporte, ou ce que le geste permet ? | proposition | proposée | 2026-09-29 |  |
| [0043](0043-profil-de-cannelure-et-lot-mesure.md) | Deux matières ou une ? Et ce que le dépôt ne sait pas de la matière qu'on a eue en main | close | appliquée | 2026-09-29 |  |
| [0044](0044-variante-carton-ondule.md) | La semelle publiée n'est pas celle qui a été coupée | proposition | proposée | 2026-09-29 |  |
| [0045](0045-reconstruction-et-amont.md) | Aucune géométrie amont ne passe dans un outil de reconstruction | gouvernante | acceptée | 2026-09-30 |  |
| [0046](0046-backflip-reconstruction-veille.md) | Backflip AI : une CAO paramétrique reconstruite ? Vérifié, pas adopté | veille | veille | 2026-09-30 |  |

**46 fiches.** 9 amendée(s) par une autre : 0005, 0009, 0010, 0015, 0016, 0019, 0021, 0022, 0026.
