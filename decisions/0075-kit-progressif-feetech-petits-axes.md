# 0075 — YXOR Kit progressif, debout en Feetech ; Feetech aux petits axes de toute la gamme

Date : 2026-10-08
État : acceptée
Complète : `0074-kit-modules-successifs.md` (dont elle tranche les niveaux,
l'option d'alimentation, le critère de recyclage et l'assemblage) et
touche `0069-deux-robots-lab-et-final.md` / `0073-gamme-yxor.md` : la
famille des petits axes devient commune à toute la gamme.

Décision coûteuse à inverser (règle 5) : elle fixe ce que l'utilisateur
achète à chaque niveau du Kit, et elle **impose une famille d'actionneurs
au Lab, au Home et au Pro** (cou, pinces), donc une interface (bus série
Feetech, adaptateur, fixations) partagée par toute la gamme.

## Décision

**DÉCIDÉE par Jeremy le 2026-10-08.** Ses mots (réponse écrite du
2026-10-08, vers 19 h 55, à la question « lesquelles de ces décisions sont
les tiennes ? ») :

> « Pour YXOR Kit : les niveaux 0 à 4 avec le niveau 3 limité à tenir
> debout en Feetech, la marche étant le passage au Lab ; l'option
> progressive, où chaque composant du Lab n'est acheté qu'au niveau qui en
> a besoin, avec un bloc secteur 12 V aux niveaux 1 et 2 et la batterie au
> niveau 3 seulement, dans un boîtier ignifuge ; je garde le critère de
> recyclage ; assemblage B. Les servos Feetech sont la famille des petits
> axes de toute la gamme. »

- **Niveaux 0 à 4** du Kit (`params/capacites.yaml`, `profils.kit.modules`) :
  0 articulé, 1 animé, 2 interactif, **3 debout** (tenir debout, en
  Feetech), 4 passage au Lab. **La marche est le passage au Lab.**
- **Option progressive** : chaque composant du Lab n'est acheté qu'au
  niveau qui en a besoin ; **bloc secteur 12 V aux niveaux 1 et 2** ;
  **batterie au niveau 3 seulement, dans un boîtier ignifuge**.
- **Critère de recyclage gardé** (filière papier, mono-matière) : le
  carton plume reste éliminé.
- **Assemblage B** : tenons et encoches, colle chaude non porteuse
  seulement, pivots par vis traversante (`docs/kit-yxor.md`).
- **Feetech est la famille des petits axes de toute la gamme** (cou,
  pinces : `explorateur.PETITS_AXES`). L'explorateur ne choisit plus entre
  Feetech et Dynamixel pour ces axes.

## Conséquence pour le Lab

Sa meilleure solution du 2026-10-08 mettait le cou en Dynamixel. Le coût
de la contrainte (CHF, kg) est mesuré par l'explorateur relancé avec
Feetech seul ; il est dans le journal et `docs/kit-yxor.md`.

## Ce qui n'est PAS décidé

- **Le carton précis** : le prompt du 2026-10-08 fait dessiner le niveau 0
  en carton ondulé double de 3,5 mm (la valeur mesurée, premier du
  classement) ; ce n'est pas un choix écrit par Jeremy.
- Le bloc secteur, le boîtier ignifuge et les servos exacts : comparés,
  pas choisis ; aucun achat (fiche 0066).
