# YXOR Kit : l'étude du 2026-10-08

**Rédigé le 2026-10-08** (prompt « Étude de YXOR Kit »). Les chiffres viennent de `scripts/kit.py`. Son rapport
engendré, `docs/kit-etude-2026-10.md`, fait foi : les valeurs citées ici sont celles du 2026-10-08.

## Ce qui est décidé, et ce qui ne l'est pas

**Décidé par Jeremy** le 2026-10-08 (fiche 0074, ses mots dans la fiche) :

- **des modules successifs** ;
- **les mêmes dimensions, la même taille et les mêmes composants que le Lab** (philosophie Framework et Fairphone :
  l'investissement initial doit resservir) ;
- **le carton le mieux adapté** ;
- **des outils du ménage** : cutter, règle, équerre, éventuellement un pistolet à colle.

**PROPOSÉ** :

- les niveaux de modules (`params/capacites.yaml`, `profils.kit.modules`) ;
- les hypothèses de calcul (`params/kit.yaml`) ;
- les critères de choix du carton ;
- les options d'assemblage.

Rien n'est acheté (fiche 0066).

## Les modules (PROPOSÉS)

| Niveau | Module | Ce qu'il ajoute | Axes motorisés |
| ---: | --- | --- | --- |
| 0 | articulé | le mannequin passif : poses, proportions, montage, noms d'axes | aucun (26 pivots) |
| 1 | animé | tête et bras ; calculateur, batterie, bus série | cou (2), épaules (2 × 2), coudes (2) |
| 2 | interactif | vision, voix, IA ; visage sur écran | aucun |
| 3 | debout | jambes et taille : tenir debout, puis marcher lentement (0,3 m/s) | jambes (2 × 5), taille en lacet (1) |
| 4 | passage au Lab | structure en aluminium et actionneurs RobStride | — |

**Même taille et même squelette que le Lab.** Le Kit reprend le Lab tel que l'explorateur le donne aujourd'hui :

- jambe à 0,65 m ;
- 0,715 m de hauteur réelle (le tronc s'allonge pour l'électronique).

La taille du Lab n'est pas décidée (fiche 0047). Si elle change, le Kit la suit, et un test le signale
(`tests/test_kit.py`).

**La structure ne change pas d'un module à l'autre.** Les coques sont dimensionnées dès le niveau 0 pour loger les
servos du niveau 3 : un module s'ajoute, il ne fait pas refaire la structure.

## Les chiffres (2026-10-08)

**Option « alignée sur le Lab »** :

- le calculateur du Lab (Seeed reComputer Mini J3011) ;
- la moitié du pack du Lab (12S1P de sa cellule, la P42A) ;
- le rail 12 V et la chaîne compacte du Lab ;
- des servos Feetech au rail 12 V.

| Niveau | Masse cumulée | Coût cumulé connu (CHF HT) | Ce qui manque |
| ---: | ---: | ---: | --- |
| 0 | 0,48 kg (carton seul) | 0 (carton de récupération) | masse et prix de la visserie |
| 1 | 2,39 kg | 868 | masse de l'anti-étincelle et du BMS |
| 2 | 2,39 kg + caméra, micro, haut-parleur, écran | 868 + ces quatre | aucun marché relevé pour eux |
| 3, debout en Feetech | 3,11 kg | 974 + prix du STS3250 | prix du STS3250 |
| 3, marche en RobStride | 5,74 kg | 1 634 | — |

Sur 2,39 kg au niveau 1, **la batterie pèse 1,09 kg** (12 cellules) et le calculateur 0,35 kg. Le carton ne pèse
que 0,48 kg.

**Option « minimale »** (3S, Raspberry Pi 5) : 1,21 kg et 430 CHF au niveau 1, et 1,89 kg et 636 CHF au niveau 3.
Le coût est connu en partie seulement : le BMS et le fusible 3S sont hors du marché versé. Mais **rien ne resservirait
au Lab** (0 %).

**Le carton de référence** est le seul carton mesuré du projet : ondulé double de récupération, 649 g/m², 3,5 mm.

## Niveaux 1 et 3 : les servos Feetech tiennent-ils ?

**Niveau 1 (tête et bras) : oui, largement.** Le STS3215 (version 12 V) tient chaque axe, avec la marge de 1,5 :

| Axe | Besoin (N·m) | Origine du besoin |
| --- | --- | --- |
| épaule | 0,20 | explorateur |
| épaule, bras tendu | 0,14 | statique |
| coude | 0,02 | statique |
| cou, tête basculée | 0,08 | statique |

Le servo annonce 2,94 N·m au blocage et 0,98 N·m en continu. Seule réserve : Feetech ne publie que le couple de
blocage, pas de couple de pointe.

**Niveau 3, tenir debout : oui.** En statique, genoux légèrement fléchis, chaque axe trouve un Feetech :

- le STS3215 à la hanche et au genou ;
- le STS3250 à la cheville. Son prix et sa vitesse viennent d'une page web dont aucune copie n'a été conservée.

**Niveau 3, marcher à 0,3 m/s : non, en Feetech.** Trois axes ne tiennent pas :

| Axe | Ce qui manque |
| --- | --- |
| tangage de hanche | le couple continu : 1,17 × 1,5 = 1,76 N·m, au-delà des 1,57 N·m du plus fort (STS3250) |
| genou | la vitesse : 13,6 rad/s demandés, 7,9 rad/s pour le STS3250 |
| cheville | la vitesse : 17,5 rad/s demandés |

**Ce qu'il faudrait : des RobStride RS00**, la famille du Lab, en 12S comme lui. Une fois la masse recalculée
(chaque RS00 pèse 330 g), il en faut **aux dix axes des jambes**. Le Kit passe alors à 5,74 kg et 1 634 CHF.

Ces RS00 ne sont pas perdus : le Lab en met aussi (hors du roulis et du tangage de hanche et du genou, fiche
0067). Combien d'entre eux il reprend reste à vérifier.

**Ce que le calcul ne sait pas : si le carton porte 5,74 kg.** C'est la question des essais (protocole).

## Réutilisation Kit → Lab

Détail composant par composant : `docs/kit-etude-2026-10.md`. Part du coût **connu** du Kit qui resservirait au Lab :

| Option | Sûr | Si les maillons « à vérifier » coïncident |
| --- | ---: | ---: |
| alignée (niveau 3 en Feetech) | 55 % | 71 % |
| alignée, jambes en RobStride | 33 % | 88 % |
| minimale | 0 % | 0 % |

- **Gardés à coup sûr** : le calculateur et les cellules, qui deviennent la moitié du pack 12S2P du Lab.
  Risque : assembler des cellules d'âges différents.
- **À vérifier** : la chaîne de puissance (choisie ici sans le courant du Lab, qui peut en exiger une plus grosse),
  et les RS00 des jambes.
- **Remplacés** : les servos Feetech. Le Lab met le cou en Dynamixel dans sa meilleure solution, et l'adaptateur
  série Feetech part avec eux.
- **Recyclé** : le carton, en filière papier, à condition de ne pas le coller avec un autre matériau.

**Ce que cela dit de la décision de Jeremy.** Le principe « mêmes composants » se paie au niveau 1 :

- 868 CHF et 2,39 kg pour un robot en carton qui bouge les bras ;
- contre 430 CHF et 1,21 kg en option minimale.

En échange, 55 à 71 % de ce coût resservent au Lab. Aucune des deux options n'est retenue : c'est à Jeremy
d'arbitrer.

## Le carton (étude de marché du 2026-10-08)

Le marché est versé dans `params/cartons.yaml` : 33 produits, 18 qualités normalisées, 41 sources au registre.
Le classement complet est dans le rapport engendré.

**Critères PROPOSÉS** (`params/kit.yaml`, `cartons`) :

1. **Éliminatoires** :
   - filière papier, mono-matière (le document de vision dit « éviter les mélanges de matières collées ») ;
   - un panneau, pas un simple face ;
   - disponible en Suisse.
2. **Rang** :
   - d'abord la rigidité en flexion par masse, approchée par e²/σ (épaisseur au carré sur masse surfacique), en
     attendant les essais ;
   - puis la masse de la structure ;
   - puis le prix.

**Résultat selon ces critères :**

- **Premier : le carton ondulé double cannelure.** Le seul dont la masse est connue est le carton de récupération
  mesuré (e²/σ = 0,019). Le carton gris compact de 3 mm vient loin derrière (0,005) et alourdirait la structure à
  1,35 kg.
- **La plaque ondulée BC de 6 mm de Modulor** (5,19 CHF/m², livrée en Suisse) est la candidate achetable la plus
  probable. Sa masse surfacique n'est pas publiée : **elle se pèse** (essai 0 du protocole).
- **Éliminés par le critère de recyclage** : le carton plume (Kapa, sandwich mousse PUR) serait le plus rigide par
  masse (e²/σ = 0,043 en 5 mm). Il est éliminé parce qu'il n'est pas mono-matière. Si Jeremy assouplit ce
  critère, il passe premier.
- **Nid d'abeille** : épais (15 à 20 mm) et à peser ; aucune valeur mécanique n'est publiée.
- **Trous** :
  - aucun carton ondulé vendu au détail ne publie d'ECT ;
  - la grille DIN 55468-1 n'a pas été lue (trois sites qui divergent) ;
  - plusieurs grandes enseignes suisses refusent le téléchargement.
- **Prix** : port non compté (Modulor : 36,90 € par colis), TVA suisse non comptée.

Protocole d'essai : `docs/protocole-carton.md`.

## Assemblage : options à arbitrer par Jeremy

Le document de vision dit « pas de colle structurelle » (PROPOSÉ, non décidé) ; Jeremy cite le pistolet à colle.
Quelques notions, d'abord :

- un **tenon** est une languette qui entre dans une **encoche** (une fente) de la pièce voisine. Bien ajusté, il
  positionne et bloque sans colle ;
- un **pivot** est l'axe d'une articulation. Ici, une vis traversante, serrée entre deux rondelles larges qui
  répartissent l'effort sur le carton (réglage `cutter_cartonplume_5` : « vis traversante + rondelles larges des
  deux côtés »).

| Option | Ce qui tient la pièce | La colle | Démontable, recyclable | Ce que ça demande |
| --- | --- | --- | --- | --- |
| **A. Sans colle** | tenons et encoches, coques fermées par languettes, pivots vissés | aucune | oui, tout | des encoches à la largeur de l'épaisseur mesurée (saignée nulle au cutter, mesurée le 2026-09-29) ; un essai de tenue des tenons |
| **B. Colle chaude d'appoint** | comme A | pistolet à colle : poser, fermer une coque, tenir un câble ; **jamais** dans le chemin d'un effort | oui, en arrachant ; la tolérance du recyclage du papier à la colle chaude n'a pas été vérifiée | la même conception que A ; la colle ne fait que faciliter |
| **C. Colle structurelle** | coques collées en caisson | pistolet ou colle blanche, porteuse | non : une coque collée se casse pour s'ouvrir | une conception plus simple, plus rigide ; contredit la vision et la règle « assemblage démontable » de CLAUDE.md |

- **Pivots, aux trois options** : vis M3 ou M4 traversante (`params/hardware.yaml`), rondelles larges des deux
  côtés, écrou à frein pour régler la friction du niveau 0 (le mannequin garde sa pose). Un trou dans le carton
  s'ovalise : une rondelle de carton gris contrecollée autour du trou (option B), ou une douille rapportée, à
  essayer.
- **Servos** : vissés par leurs pattes à travers la paroi, rondelles larges, et le palonnier (le disque de sortie
  du servo) vissé sur le segment suivant.
- **PROPOSÉ par Claude : l'option B.** Elle garde la conception démontable de A et emploie le pistolet là où il
  aide vraiment. La décision revient à Jeremy.

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

1. Les niveaux 0 à 4 tels que proposés ?
2. L'option « alignée sur le Lab » (868 CHF au niveau 1, 55 à 71 % resservent) ou l'option « minimale »
   (430 CHF, rien ne ressert) ?
3. Le niveau 3 : debout seulement, en Feetech, ou marcher, en RobStride (5,74 kg, 1 634 CHF, et la question de la
   tenue du carton) ?
4. Les critères du carton, dont le recyclage, qui élimine le carton plume.
5. L'assemblage : A, B ou C ?
