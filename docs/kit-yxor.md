# YXOR Kit : l'étude et les plans du niveau 0

**Rédigé le 2026-10-08, mis à jour le même jour** (prompts « Étude de YXOR Kit », puis « YXOR Kit : décisions et
plans du niveau 0 »). Les chiffres viennent de deux programmes, dont les rapports engendrés font foi :

- `scripts/kit.py` → `docs/kit-etude-2026-10.md` ;
- `parts/kit_niveau0.py` → `docs/kit-montage-niveau0.md` et les planches A4.

Les valeurs citées ici sont celles du 2026-10-08.

## Ce qui est décidé, et ce qui ne l'est pas

**Décidé par Jeremy** le 2026-10-08, ses mots dans les fiches 0074 et 0075 :

- des **modules successifs** ;
- les **mêmes dimensions, taille et composants que le Lab** ;
- **le carton le mieux adapté** ;
- des **outils du ménage** ;
- les **niveaux 0 à 4**, le niveau 3 étant **limité à tenir debout en Feetech** : la marche est le passage au Lab ;
- l'**option progressive** : chaque composant du Lab n'est acheté qu'au niveau qui en a besoin. Un **bloc secteur
  12 V** alimente les niveaux 1 et 2 ; la **batterie** n'arrive qu'au niveau 3, **dans un boîtier ignifuge** ;
- le **critère de recyclage** est gardé ;
- l'**assemblage B** ;
- **Feetech est la famille des petits axes de toute la gamme**.

**PROPOSÉ** :

- les hypothèses de calcul et de dessin (`params/kit.yaml`) ;
- le carton exact. Les plans sont dessinés en ondulé double de 3,5 mm, comme le demandait le prompt, mais ce
  n'est pas un choix écrit par Jeremy.

**À trancher** : la taille du Kit (voir plus bas). Rien n'est acheté (fiche 0066).

## Les modules

| Niveau | Module | Ce qu'il ajoute | Axes motorisés |
| ---: | --- | --- | --- |
| 0 | articulé | le mannequin passif : poses, proportions, montage, noms d'axes | aucun (pivots vissés) |
| 1 | animé | tête et bras ; calculateur, bus série, **bloc secteur 12 V** | cou (2), épaules (2 × 2), coudes (2) |
| 2 | interactif | vision, voix, IA ; visage sur écran | aucun |
| 3 | debout | jambes et taille ; **batterie, sa chaîne, le contenant ignifuge** | jambes (2 × 5), taille en lacet (1) |
| 4 | passage au Lab | aluminium et RobStride ; c'est là qu'on marche | — |

## Les trois options, niveau par niveau

Masse cumulée du robot et coût connu cumulé (CHF HT). Un « ≥ » signale des composants sans masse ou sans prix
relevés : caméra, micro, haut-parleur, écran, visserie, prix du STS3250.

| Niveau | Progressive (décidée) | Alignée sur le Lab | Minimale |
| ---: | --- | --- | --- |
| 0 | 0,48 kg ; 0 | 0,48 kg ; 0 | 0,48 kg ; 0 |
| 1 | 1,28 kg ; 717 | ≥ 2,41 kg ; 935 | ≥ 1,21 kg ; ≥ 430 |
| 2 | 1,28 kg (+ le niveau 2) ; 717 (+ le niveau 2) | 2,41 kg ; 935 | 1,21 kg ; ≥ 488 |
| 3 | ≥ 3,05 kg ; ≥ 1 178 | 3,05 kg ; ≥ 1 125 | 1,82 kg ; 720 |
| **Part du coût réutilisée au Lab** | **58 à 71 %** | 59 à 74 % | 9 % |

- **Progressive** : au niveau 1, le robot ne porte que ses servos et son calculateur. Le bloc reste sur la table.
  La batterie (12S1P de la cellule du Lab, la P50B, 178 Wh au-dessus de la coupure) arrive au niveau 3. Elle coûte
  un peu plus au total que l'option alignée : le bloc secteur et le contenant ignifuge s'ajoutent.
- **Bloc secteur des niveaux 1 et 2** : le pire cas, c'est 8 servos au blocage (8 × 2,7 A = 21,6 A, courant
  relevé chez des revendeurs) plus le calculateur à son maximum (25 W, 2,1 A). Avec la marge de 1,25 (PROPOSÉE),
  il faut **29,6 A**.
  - **Aucun adaptateur de table fermé relevé n'y arrive** : le plus fort, le Mean Well GST220A12, donne 15 A.
  - Seul un bloc à bornier de 30 A (S-360-12, épuisé) le tient. Il faut alors **raccorder soi-même le 230 V**,
    ce que le vendeur lui-même présente comme un danger mortel.
  - Le pire cas suppose les 8 servos bloqués en même temps. Le rabaisser, en limitant le courant des servos ou
    en admettant moins de servos bloqués à la fois, est une décision à prendre.
- **Contenant ignifuge** : quatre produits relevés, de 9 CHF (sac Jamara) à 66 EUR (boîte Bat-Safe en acier).
  **Aucun essai indépendant trouvé** : les fabricants n'affirment rien de chiffré.

## Les servos Feetech tiennent-ils ?

- **Niveau 1 : oui.** Un seul modèle, le STS3215 en 12 V, tient chaque axe avec la marge de 1,5.
- **Niveau 3, tenir debout : oui.** STS3215 à la hanche, au genou et à la taille ; STS3250 à la cheville. Le prix
  et la vitesse du STS3250 viennent d'une page web dont aucune copie n'a été conservée.
- **Marcher** : non en Feetech (calcul précédent). C'est le passage au Lab, comme décidé.

## Ce que coûte au Lab « Feetech aux petits axes »

L'explorateur a été relancé avec Feetech seul aux petits axes (cou et pinces). Sa meilleure solution RobStride
(12S, 250 Hz, chaîne compacte) change ainsi :

| | Avant (Dynamixel libre) | Après (Feetech imposé) |
| --- | --- | --- |
| Hauteur réelle | 0,715 m | **0,850 m** |
| Masse | 13,6 kg | **18,5 kg** |
| Coût | ≥ 4 275 CHF | **≥ 4 514 CHF** (le prix du STS3250 du cou manque) |

**Pourquoi un tel saut pour quatre petits servos.** À 0,65 m, le genou du Lab (RS06) tenait le couple continu à
**0,07 N·m près** : 11,07 N·m exigés, marge comprise, pour 11,0 publiés. Les Feetech pèsent 55 g, contre 18 g pour
les Dynamixel ; ces ~150 g de plus suffisent à faire basculer le cas de masse le plus défavorable. L'explorateur
passe alors à la solution suivante, à 0,85 m.

À taille égale, le Feetech est **moins cher** : STS3215 à 21 CHF, contre 28 à 32 CHF pour un Dynamixel. Le coût de
la contrainte vient donc entièrement de cette marge au genou.

Deux corrections de l'explorateur en sont sorties :

- **La borne de coût comptait 0 CHF pour tous les actionneurs dès qu'un seul prix manquait.** Elle compte
  maintenant les prix connus.
- **Une modification du choix de repli a été essayée puis annulée** : elle changeait aussi les actionneurs du
  corps.

**Servos du Kit qui resservent au Lab** (calculés à 0,85 m et 18,5 kg) :

| Servo du Kit | Devient au Lab |
| --- | --- |
| le STS3215 du lacet de cou | le lacet de cou |
| deux STS3215 (cou en tangage, une épaule) | les deux pinces |
| un STS3250 de cheville | le tangage de cou |

Le STS3215 du tangage de cou ne tiendrait plus à 18,5 kg.

## La taille du Kit : gelée, à trancher

Le Kit devait suivre la taille du Lab (fiche 0074). Or le Lab vient de passer à 0,85 m.

- **Les plans et l'étude restent à la taille d'avant** : jambe à 0,65 m, hauteur réelle 0,715 m
  (`params/kit.yaml`, `kit_taille`).
- **Suivre le Lab à 0,85 m** agrandirait toutes les pièces d'environ 30 % et porterait le Kit en carton vers
  1,2 m.

C'est à Jeremy de décider.

## Les plans du niveau 0

`parts/kit_niveau0.py` produit **111 gabarits, soit 178 pièces et 44 cales** (rondelles de carton), sur
**40 feuilles A4**. Les flancs et les faces du tronc s'impriment en deux feuilles qui se recouvrent. Le tout
représente 0,78 m² de carton, soit 505 g. Notice pas à pas : `docs/kit-montage-niveau0.md`.

- **Chaque segment est une boîte** : deux flancs, deux faces en retrait tenonnées dans les flancs, des cloisons ou
  des couvercles. Aucune pièce n'a d'angle rentrant vif.
- **Les logements des 19 servos sont prévus dès maintenant.** Chacun se compose d'une fenêtre dans une paroi et
  d'une plaque à fenêtre intérieure.
  - Au niveau 0, un bouchon et une plaque de serrage portent le pivot.
  - Au niveau 1 ou 3, on les retire et on glisse le servo, **sans rien redécouper**. Le contrôle 3D pose les
    19 servos dans leurs logements et ne trouve aucune collision.
- **Contrôles** :
  - en 2D, rayons rentrants, angles vifs et pièces d'un seul tenant ;
  - en 3D, aucune plaque n'entre dans une autre. Une plaque qui en pénètre une autre signale une erreur de
    dessin, par exemple un tenon sans sa mortaise.

  Les deux contrôles ont été vus échouer sur des défauts simulés (`tests/test_kit_niveau0.py`). La première
  version du contrôle 3D ne voyait rien (le résultat d'une intersection était mal lu) : c'est l'essai du défaut
  simulé qui l'a montré.
- **Hauteur du Kit : 0,938 m, contre 0,715 m** pour le Lab de référence. Les longueurs entre axes sont celles du
  Lab ; ce sont les logements de servo en carton qui allongent :
  - les trois axes de hanche empilés au lieu de se croiser ;
  - une cheville surélevée pour que le tibia passe au-dessus du pied ;
  - les couvercles et les cales.

  Le bassin est aussi plus large (179 mm contre 132) pour loger les deux lacets de hanche.
- **Rendu de contrôle** : `exports/kit_niveau0/kit_niveau0.png`, régénéré et regardé. La silhouette est
  cohérente : jambes, hanches, bras pendants, tête sur le cou, servos dans leurs fenêtres.

## Ce qu'il faut réunir

**Pour le niveau 0** (calculé ; liste complète dans la notice) :

- **1,2 m² de carton ondulé double cannelure**, en cartons de déménagement de récupération, plats et secs ;
- **38 vis M4** (14 × 16 mm, 2 × 20 mm, 22 × 25 mm), **38 écrous M4 à frein** et **76 rondelles larges M4** ;
- **40 feuilles A4** imprimées à 100 %, de la colle en bâton ou du scotch de peintre ;
- les outils décidés (cutter et lames neuves, règle métallique, équerre, pistolet à colle), plus un carton martyr
  et un tournevis cruciforme pour amorcer les trous.

**Pour le protocole d'essai du carton** (`docs/protocole-carton.md`) :

- deux ou trois cartons à comparer, dont le double cannelure de récupération déjà mesuré ;
- deux piles de livres de même hauteur, et un livre rigide ;
- des bouteilles d'eau de 0,5 L et de 1,5 L ; prévoir **10 kg au moins** pour l'écrasement ;
- un sac ou un seau léger, avec une ficelle ;
- la règle graduée au millimètre, l'équerre, le cutter ;
- la balance de cuisine.

## Le carton (étude de marché du 2026-10-08)

Inchangé, critères gardés par Jeremy :

- **premier : l'ondulé double cannelure** ;
- **la plaque BC de 6 mm de Modulor** est à peser ;
- **le carton plume reste éliminé** par le critère de recyclage.

Détail : `docs/kit-etude-2026-10.md`.

## Assemblage B (décidé)

- **Tenons et mortaises** : une languette entre dans une fente de la pièce voisine. Ce sont eux qui tiennent les
  pièces.
- **Colle chaude non porteuse seulement** : un point sur un tenon qui dépasse, jamais entre deux pièces qui
  portent un effort, jamais sur un bouchon ni une plaque de serrage.
- **Pivots par vis M4 traversante** : rondelles larges des deux côtés, écrou à frein pour régler la friction du
  mannequin.

## Le site : ce qu'il publie aujourd'hui, et ce qu'un site du Kit devrait montrer

**Aujourd'hui** (`scripts/regenerer.py`, `scripts/pages.py`), yxor.fr publie :

- **une seule pièce**, la semelle d'apprentissage, sur deux pages :
  - `piece/` : la fiche, ses cotes et leur provenance, la simulation dans le navigateur ;
  - `atelier/` : le plan à couper ;
- ses fichiers régénérés (STEP, STL, DXF, PDF) ;
- une page **état** du projet ;
- une page **provenance** (les valeurs d'origine ToddlerBot, comptées) ;
- deux fichiers de données en JSON.

**L'empreinte** en pied de page est un hachage des dossiers `params/`, `parts/`, `scripts/`, `web/` et de
`requirements.txt` : ce que l'image Docker contient, pas le numéro du commit. Elle se compare à
`scripts/empreinte.py` et figure aussi dans l'URL des fichiers servis (`?v=…`) pour qu'aucun cache ne fige une
version périmée. La jambe basse en carton n'est pas publiée.

**Ce qu'un site pour les fabricants du Kit devrait montrer** (rien n'est construit) :

1. **Un parcours par module** (0 à 4) : ce qu'on obtient, ce qu'il faut, le temps et le coût, ce qui resservira
   au Lab.
2. **Les plans à imprimer** par carton et par format (A4, A3), à l'échelle 1:1, avec une **règle de contrôle
   imprimée** (une imprimante qui réduit à 97 % fausse toutes les encoches), et l'empreinte sur chaque feuille.
3. **La nomenclature** par module : visserie, servos, électronique, avec des références courantes et sans lien
   d'achat imposé (règle d'achat).
4. **Le montage** étape par étape, illustré par les rendus de la CAO.
5. **Le choix du carton** : le classement, les critères, et le protocole d'essai pour son propre carton.
6. **Les réglages** : l'épaisseur mesurée de son carton change la largeur des encoches. C'est un paramètre, donc
   le site devrait engendrer le plan pour l'épaisseur saisie.
7. **La sécurité** : batterie Li-ion (charge, stockage, coupure), couple des servos (doigts), âge et
   accompagnement.
8. **Les retours** : photos, défauts, mesures d'essai, sous une forme qui puisse revenir dans `params/mesures.yaml`.
9. **Les licences** et l'attribution, une fois choisies.

## Questions pour Jeremy

1. **La taille du Kit** : garder 0,65 m (0,715 m réels), ou suivre le Lab à 0,85 m ?
2. **La contrainte Feetech au Lab** coûte 0,135 m, 4,9 kg et ≥ 239 CHF, à cause d'une marge de 0,07 N·m au genou.
   La garder telle quelle, ou revoir la marge au genou après le banc (fiche 0051) ?
3. **Le bloc secteur** : accepter un bloc à bornier (230 V à raccorder), ou rabaisser le pire cas pour qu'un
   adaptateur fermé suffise ?
4. **Le carton des plans** : l'ondulé double de 3,5 mm est-il retenu ?
