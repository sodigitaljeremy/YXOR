# Index des fiches de décision

**Engendré** par `scripts/index_fiches.py` — ne pas éditer à la
main. Le régénérer fait partie de `scripts/regenerer.py`.

Une fiche n'est jamais réécrite (règle 5) : elle est *amendée*
par une autre, et le renvoi figure dans son en-tête. La colonne
« amendée par » est donc la plus importante du tableau — c'est
elle qui dit ce qu'il ne faut plus croire.

| # | Titre | Statut | Date | Amendée par |
| --- | --- | --- | --- | --- |
| [0001](0001-base-toddlerbot.md) | ToddlerBot comme base de départ | acceptée | 2026-09-20 |  |
| [0002](0002-pin-toddlerbot.md) | Ancrage de ToddlerBot et environnement bicéphale | acceptée | 2026-09-20 |  |
| [0003](0003-poids-politiques-toddlerbot.md) | Provenance des politiques pré-entraînées ToddlerBot | acceptée | 2026-09-20 |  |
| [0004](0004-code-amont-dans-le-depot.md) | Du code YXOR qui s'exécute avec le venv amont | acceptée | 2026-09-28 |  |
| [0005](0005-topologie-bras-p1.md) | Topologie du bras en P1 : celle de ToddlerBot | acceptée | 2026-09-28 | **0011** — l'emprunt dimensionnel (H) est adossé au même palier P1 que l'emprunt topolog… |
| [0006](0006-fichier-genere-commite.md) | Un fichier généré qui est commité | acceptée | 2026-09-28 |  |
| [0007](0007-sourcing-materiel.md) | Sourcing des affirmations sur le matériel | acceptée | 2026-09-28 |  |
| [0008](0008-sauvegarde-poids.md) | Sauvegarde des poids : manifeste versionné, binaires hors Git | acceptée | 2026-09-28 |  |
| [0009](0009-build123d.md) | build123d comme noyau de CAO paramétrique | acceptée | 2026-09-28 | **0029** — CERN-OHL-S y était classée à tort comme non commerciale ; la conclusion de ce… |
| [0010](0010-origine-des-cotes.md) | Traçabilité de l'origine des cotes | acceptée | 2026-09-28 | **0011** — cinquième origine litterature, et filiation de H consignée. |
| [0011](0011-origine-litterature.md) | Cinquième origine `litterature`, et filiation de H | acceptée | 2026-09-28 |  |
| [0012](0012-correction-anthropometry.md) | Correction de `anthropometry.yaml` : sources rétablies | acceptée | 2026-09-28 |  |
| [0013](0013-nature-des-cotes.md) | Nature des cotes : la règle 1 restreinte à son domaine | acceptée | 2026-09-28 |  |
| [0014](0014-pas-d-imprimante-3d.md) | Il n'y a pas d'imprimante 3D | acceptée | 2026-09-28 |  |
| [0015](0015-architecture-plaques-entretoises.md) | Architecture en plaques et entretoises, découpe 2D seule | acceptée | 2026-09-28 | **0016** — aucun projet open source accessible ne suit cette voie ; Solo, Bolt et Upkie … |
| [0016](0016-plaques-sans-precedent.md) | ~~L'architecture en plaques n'a aucun précédent open source~~ | acceptée | 2026-09-28 | **0017** — le constat « aucun précédent » est FAUX : MEVITA, MEVIUS et MEVIUS2 construis… |
| [0017](0017-mevita-decoupe-metal.md) | MEVITA : la découpe métal a bien un précédent | acceptée | 2026-09-28 |  |
| [0018](0018-application-web.md) | Application web : un site statique engendré par le dépôt | acceptée — validée le 2026-09-28,  | 2026-09-28 |  |
| [0019](0019-interface-catalogue.md) | Interface : le site devient un catalogue technique | acceptée le 2026-09-28 — codée le  | 2026-09-28 |  |
| [0020](0020-nullite-conditionnelle.md) | Trois états de la valeur absente | acceptée le 2026-09-29, à la deman | 2026-09-29 |  |
| [0021](0021-machine-x-materiau.md) | Séparer la machine du matériau | proposée — rien n'est appliqué. | 2026-09-29 | **0026** — la clé composée ne tient pas à six axes ; migration SUSPENDUE. |
| [0022](0022-soudure-instruction.md) | La soudure : instruction, sans décision | instruction — ne tranche rien, à d | 2026-09-29 | **0031** — le facteur de rigidité en torsion n'est pas une constante : il se calcule par… |
| [0023](0023-simulation-navigateur.md) | Simuler dans le navigateur, sans rien enregistrer | acceptée le 2026-09-29, à la deman | 2026-09-29 |  |
| [0024](0024-audit-et-refactorisation.md) | Audit du dépôt et plan de refactorisation | proposée — aucun code n'est touché | 2026-09-29 |  |
| [0025](0025-mobile-d-abord.md) | Le site en mobile d'abord | proposée — rien n'est codé. | 2026-09-29 |  |
| [0026](0026-machine-procede-matiere.md) | Trois axes ne suffisent pas : la clé composée doit mourir | proposée — rien n'est appliqué. | 2026-09-29 | **0033** — le chiffrage du choix clé/champ sur nullites.yaml et origines.yaml. |
| [0027](0027-regle-phase-6.md) | La règle de la « phase 6 » n'a jamais eu de référent | proposée — je ne tranche pas. Deux | 2026-09-29 |  |
| [0028](0028-verification-quatre-affirmations.md) | Quatre affirmations d'un retour extérieur, passées au crible | acceptée — vérification, pas décis | 2026-09-29 |  |
| [0029](0029-familles-de-licences.md) | CERN-OHL-S n'est pas non commerciale : trois familles, pas deux | acceptée — correction d'une erreur | 2026-09-29 |  |
| [0030](0030-fichiers-fournisseurs.md) | Aucun fichier fournisseur non redistribuable dans le dépôt | acceptée. | 2026-09-29 |  |
| [0031](0031-torsion-par-section.md) | La rigidité en torsion se calcule, elle ne se stocke pas | acceptée — correction chiffrée. | 2026-09-29 |  |
| [0032](0032-veille-outils.md) | Quatre pistes en veille : notées, pas adoptées | veille — aucune n'est adoptée, auc | 2026-09-29 |  |
| [0033](0033-epaisseur-cle-ou-champ.md) | L'épaisseur reste un CHAMP : le coût de l'autre choix, chiffré | proposée — instruction, aucune mig | 2026-09-29 |  |

**33 fiches.** 8 amendée(s) par une autre : 0005, 0009, 0010, 0015, 0016, 0021, 0022, 0026.
