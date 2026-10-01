# État des lieux — 2026-09-29

Dix jours après le premier commit. Aucune modification n'accompagne ce
document : il lit, il mesure, il rapporte.

Tous les chiffres sont mesurés ; les commandes qui les produisent sont au
journal du jour. Là où je juge plutôt que je ne mesure, c'est dit.

---

## 1 — Inventaire

| Catégorie | Fichiers | Lignes | Taille |
| --- | ---: | ---: | ---: |
| **prose** (`.md`) | 41 | **9 338** | 412 ko |
| code Python | 18 | 4 374 | 191 ko |
| données (`.yaml`) | 9 | 2 244 | 95 ko |
| code JavaScript | 3 | 655 | 28 ko |
| autre | 7 | 300 | 12 ko |
| style (`.css`) | 1 | 265 | 16 ko |
| config | 3 | 164 | 8 ko |
| **TOTAL** | **82** | **17 340** | **761 ko** |

**Code 5 294 · données 2 244 · prose 9 338.**
Rapport prose/code : **1,76**. **54 % du dépôt est de la prose.**

### Les dix plus gros fichiers

| Lignes | Fichier |
| ---: | --- |
| 2 845 | `journal/2026-09-28.md` |
| **1 111** | `journal/2026-09-29.md` |
| **932** | `scripts/regenerer.py` |
| 865 | `journal/2026-09-20.md` |
| 593 | `params/joints.yaml` |
| 522 | `params/upstream_joints.generated.yaml` |
| 449 | `parts/semelle_apprentissage.py` |
| 388 | `scripts/audit_origines.py` |
| 361 | `scripts/import_upstream_limits.py` |
| 354 | `web/simulateur.js` |

### Ce qui a grossi depuis l'audit de ce matin

Entre le commit `711d4cd` (audit, ce matin) et maintenant : **35 fichiers
touchés, +3 305 lignes, −362**.

| | ajouté | retiré | net |
| --- | ---: | ---: | ---: |
| prose | +1 850 | −20 | **+1 830** |
| code | +988 | −178 | +810 |
| données | +467 | −164 | +303 |

**Deux constats désagréables.**

Le journal du jour est passé à **1 111 lignes** et occupe déjà la seconde
place du dépôt. L'audit de ce matin signalait le journal du 28 comme
illisible ; j'en ai écrit un second du même ordre dans la journée.

`regenerer.py` est passé de **822 à 932 lignes** — l'audit de ce matin le
signalait comme le plus gros fichier de code, et il a grossi de 13 % dans
la journée qui a suivi.

---

## 2 — Les 33 fiches

| # | Titre | Statut | Appliquée | Amendée par | Contredite |
| --- | --- | --- | --- | --- | --- |
| 0001 | ToddlerBot comme base de départ | acceptée | oui | — | non |
| 0002 | Ancrage amont, environnement bicéphale | acceptée | oui | — | non |
| 0003 | Provenance des politiques pré-entraînées | acceptée | oui, **dormante** | — | non |
| 0004 | Code YXOR sous venv amont | acceptée | oui | — | non |
| 0005 | Topologie du bras en P1 | acceptée | données seules | 0011 | non |
| 0006 | Un fichier généré qui est commité | acceptée | oui | — | non |
| 0007 | Sourcing des affirmations matériel | acceptée | **partiellement** | — | non |
| 0008 | Sauvegarde des poids | acceptée | **partiellement** | — | non |
| 0009 | build123d comme noyau CAO | acceptée | oui | 0029 | non |
| 0010 | Traçabilité de l'origine des cotes | acceptée | oui, outillée | 0011 | non |
| 0011 | Origine `litterature`, filiation de H | acceptée | oui | — | non |
| 0012 | Correction d'`anthropometry.yaml` | acceptée | oui | — | non |
| 0013 | Nature des cotes | acceptée | oui, outillée | — | non |
| 0014 | Il n'y a pas d'imprimante 3D | acceptée | oui | — | **bientôt** |
| 0015 | Plaques et entretoises, découpe 2D | acceptée | oui | 0016 | non |
| 0016 | ~~Aucun précédent open source~~ | acceptée | **titre infirmé** | 0017 | **oui, assumé** |
| 0017 | MEVITA : la découpe métal a un précédent | acceptée | constat | — | non |
| 0018 | Site statique engendré par le dépôt | acceptée | oui, outillée | — | non |
| 0019 | Le site devient un catalogue technique | acceptée | oui | — | non |
| 0020 | Trois états de la valeur absente | acceptée | oui, outillée | — | non |
| 0021 | Séparer machine et matériau | **abandonnée** | **jamais** | 0026 | — |
| 0022 | La soudure : instruction | instruction | ne décide rien | 0031 | non |
| 0023 | Simuler dans le navigateur | acceptée | oui, outillée | — | non |
| 0024 | Audit et refactorisation | acceptée | **rang 1 seul (7/7)** | — | non |
| 0025 | Le site en mobile d'abord | acceptée | oui | — | non |
| 0026 | La clé composée doit mourir | acceptée | oui, ce soir | 0033 | non |
| 0027 | La « phase 6 » n'a jamais eu de référent | acceptée | oui | — | non |
| 0028 | Quatre affirmations vérifiées | acceptée | constat | — | non |
| 0029 | CERN-OHL-S n'est pas non commerciale | acceptée | oui | — | non |
| 0030 | Fichiers fournisseurs | acceptée | oui, outillée | — | non |
| 0031 | La torsion se calcule | acceptée | constat | — | non |
| 0032 | Cinq pistes en veille | veille | — | — | non |
| 0033 | L'épaisseur reste un champ | acceptée | oui, ce soir | — | non |

**Aucune fiche n'est contredite par le code.** La seule contradiction est
celle de la 0016, et elle est **assumée** : son titre est barré et un
encadré dit qu'il est faux.

### Y a-t-il des fiches qui ne servent à rien ?

**Non — mais la question révèle un vrai défaut.**

Mesuré, en citations explicites (« fiche 0016 », `` `0016-….md` ``) :

| Fiche | Citée par |
| --- | ---: |
| 0010 (traçabilité) | **18 fois** |
| 0026 (quatre tables) | 16 |
| 0007, 0013, 0020 | 12 à 15 |
| … | |
| 0006, 0017, 0022, 0025, 0031, 0032 | **1 fois** |
| **0012, 0019** | **0 fois** |

Deux fiches ne sont citées par rien. Mais **ce n'est pas le bon
critère**, et voici pourquoi : il existe **trois espèces de fiches**, et
rien ne les distingue.

1. **Gouvernantes** — une règle que le code applique. 0010, 0013, 0020,
   0026, 0030, 0033. Elles sont très citées, et elles *doivent* être lues
   avant de toucher au code.
2. **Historiques** — la trace d'une correction ou d'un fait établi une
   fois. 0012, 0016, 0017, 0028, 0031. **Une citation faible y est
   normale** : on les lit quand la question revient, pas tous les jours.
   Les supprimer effacerait le souvenir d'une erreur — exactement ce que
   la règle 5 interdit.
3. **Appliquées puis closes** — 0019, 0025, 0024 rang 1. Une fois
   appliquées, **le code est la vérité** ; la fiche ne porte plus que le
   motif.

**Le défaut n'est pas qu'il y ait des fiches inutiles. C'est que l'index
ne dit pas de quelle espèce est chacune**, donc un nouveau venu ne sait
pas lesquelles il doit lire avant d'écrire une ligne. Sur 33 fiches, une
demi-douzaine suffirait — il ne peut pas savoir lesquelles.

### La vraie redondance

**0021 → 0026 → 0033 : trois fiches pour une seule décision.** La 0021
proposait une structure, la 0026 l'a remplacée, la 0033 l'a chiffrée. La
0021 n'a jamais été appliquée.

Ce n'est pas de la redondance de contenu — chacune apporte quelque chose.
C'est de la redondance **de processus** : j'ai proposé avant de mesurer,
deux fois. Voir § 7.

---

## 3 — Les règles

30 règles recensées dans `CLAUDE.md`, les fiches et le `README`.

| | Nombre | Part |
| --- | ---: | ---: |
| **Outillées** — un contrôle échoue si la règle est violée | **15** | 50 % |
| Partielles | 4 | 13 % |
| Non outillées, mais **outillables** | 6 | 20 % |
| **Non vérifiables**, à admettre comme telles | 5 | 17 % |

Ce matin : 37 % d'outillées sur 24 règles. Ce soir : **50 % sur 30**.

### Les quinze outillées

`audit_origines --strict` (cote en dur, origine, nature) ·
`controle_depot` (binaire partout, provenances fournisseurs) ·
`.gitignore` (`site/`, `exports/`) · `controler_html` ·
`profil` + auto-contrôle de la page (contour JS == CAO) ·
coefficients publiés (repères du schéma) · `toddlerbot_fixes.py` (venv) ·
contrôles de la pièce (DXF en mm, contour fermé, tient sur A4) ·
`procedes.py` (référence cassée = échec) · `index_fiches` (index à jour,
dates présentes) · vidange d'`exports/`.

**Six de ces quinze datent d'aujourd'hui.**

### Les quatre partielles

| Règle | Ce qui manque |
| --- | --- |
| `rayon_interieur_min == 0,5 × épaisseur` | vérifié pour le seul réglage employé, pas pour la table |
| Rendu de contrôle produit **et regardé** | `apercu_svg` existe, `regenerer` ne le lance pas |
| SHA amont conforme | le script existe, rien ne le relance |
| Achat : la pièce doit être `coupable` | `etat_procede` le calcule, **rien ne refuse** |

La dernière est la plus gênante : la règle décidée ce soir s'appuie sur
un verdict qui est **affiché mais jamais opposé**.

### Les six outillables, avec leur moyen

| Règle | Comment l'outiller |
| --- | --- |
| Aucun angle vif rentrant sur le DXF | analyse de courbure du contour produit |
| Quincaillerie ne suit jamais H | faire varier H, rejouer l'audit, exiger l'invariance |
| Noms d'articulations identiques partout | comparaison croisée — **possible seulement quand l'URDF existera** |
| Toute pièce est plate | volume contre boîte englobante, tolérance nulle sur Z |
| Pas de dépendance copyleft fort | lire les métadonnées des roues installées |
| Règle de nullité ou d'origine **morte** | compter les motifs qui ne correspondent à rien |

La dernière mérite d'être faite tôt : `nullites.yaml` a 13 règles et
`origines.yaml` 43. **Rien ne dit aujourd'hui qu'une règle en corresponde
à quoi que ce soit.** Une règle morte est un garde-fou qu'on croit avoir.

### Les cinq non vérifiables — et c'est bien de les nommer

| Règle | Pourquoi aucun contrôle n'est possible |
| --- | --- |
| Une décision = une fiche **avant** application | le dépôt ne garde aucune trace de l'ordre réel des actes |
| Assemblage démontable, aucun collage | propriété du montage physique, pas du fichier |
| Concevoir au plus contraignant | jugement de conception, pas prédicat |
| **L'outillage : aucun critère** | **déclaré tel** (fiche 0027 b) |
| L'assistant ne propose jamais un achat | porte sur mon comportement, pas sur le dépôt |

La branche (b) de la règle d'achat a montré la bonne manière : **déclarer
explicitement l'absence de critère** vaut mieux qu'un garde-fou inventé.
Les quatre autres devraient porter la même mention. Aujourd'hui elles
sont écrites du même ton que les règles outillées, ce qui laisse croire
qu'elles tiennent de la même façon.

---

## 4 — Ce qui manque

### Les quatre documents de cadrage

`docs/00-cadrage.md`, `01-cahier-des-charges.md`, `02-plan-action.md`,
`03-artefacts.md` — **aucun n'a jamais existé**. Le README y renvoyait
jusqu'à ce matin ; les liens sont supprimés.

| Document | Encore nécessaire ? |
| --- | --- |
| **cadrage** | **non** — dix jours de journal et 33 fiches disent ce que le projet est, mieux qu'un document écrit avant |
| **cahier des charges** | **oui, partiellement** — rien n'énonce ce que le robot doit faire. Tout le dépôt décrit *comment*, rien ne dit *quoi*. |
| **plan d'action** | **non** — la « phase 6 » qui s'y référait est retirée (fiche 0027). Écrire ce plan maintenant, ce serait le faire pour justifier une règle qui n'existe plus. |
| **artefacts** | **non** — `README` et l'arborescence le disent. |

**Un seul manque réellement : ce que le robot doit faire.** Et ce n'est
pas un oubli de documentation, c'est une question non posée.

### LOG-1

Vous désignez par « LOG-1 » une règle sur les fichiers engendrés
(fiche 0006). Le document qui la définirait **n'existe pas**, et la fiche
note qu'il faudra « reconfronter à LOG-1 quand le document » existera.

**Périmé.** `CLAUDE.md` règle 4 et `controle_depot.py` disent et
appliquent la même chose. Écrire LOG-1 ajouterait une seconde formulation
d'une règle déjà outillée — donc une occasion de divergence. **Ce qui
reste utile, c'est de retirer la référence** : un nom qui renvoie à rien.

### La seconde destination de sauvegarde

Fiche 0008 : « la seconde destination reste à la charge de Jeremy ».
**Ce n'est pas un manque du dépôt** — c'est une tâche assignée, hors de
ma portée, correctement déclarée comme telle. Elle rejoint la branche (b)
de la règle d'achat : une chose dont il est écrit qu'elle ne dépend pas
de moi.

Reste à savoir si elle est faite. Le dépôt ne peut pas le dire.

### Deux répertoires vides

`robot/` et `bom/` ne contiennent qu'un `.gitkeep`. Ils sont annoncés
dans le README. Ce n'est pas grave, mais c'est une promesse : un lecteur
y cherchera un URDF et une nomenclature.

`docs/` n'a pas bougé depuis le **2026-09-20** — jusqu'à ce fichier.

---

## 5 — Les valeurs

**1 397 inventoriées.** Voici ce qu'elles font.

### Huit gouvernent une géométrie produite

C'est le relevé complet de la seule pièce existante :

| Clé | Valeur | Origine |
| --- | ---: | --- |
| `paliers.P2` | 0,9 | propre |
| `ratios.pied_longueur` | 136,8 | littérature |
| `ratios.pied_largeur` | 49,5 | littérature |
| `matieres.carton_plume_5.epaisseur` | 5,0 | mesure |
| `reglages.cutter_cartonplume_5.rayon_interieur_min` | 2,5 | mesure |
| `ratio_coins` | 0,25 | propre |
| `ratio_resserrement` | 0,70 | propre |
| `ratio_etendue_creux` | 0,50 | propre |

**8 sur 1 397, soit 0,6 %.**

### Répartition

| Fichier | Valeurs | Lues par du code ? |
| --- | ---: | --- |
| `upstream_joints.generated.yaml` | **715** | **aucune** — documentaire |
| `joints.yaml` | 386 | **17** (la confiance, pour une table du site) |
| `hardware.yaml` | 136 | 2 gouvernent, le reste est lu par le chargeur |
| `anthropometry.yaml` | 75 | 3 gouvernent |
| `ckpts.manifest.yaml` | 40 | oui, par `ckpts_backup.py` |

### Dorment, mortes, ou documentaires

**Dormantes — utiles plus tard, sans usage aujourd'hui.**
`joints.yaml` (386) et les ratios inemployés (12 des 14). Elles
attendent des pièces qui n'existent pas. Ce n'est pas un défaut : la
topologie a été établie avant la géométrie, délibérément.

**Documentaires — lues par personne, mais elles justifient autre chose.**
`upstream_joints.generated.yaml`, **715 valeurs, soit 51 % du total**.
Aucun code ne les lit. Elles sont citées **35 fois en prose** dans
`joints.yaml` comme source de ses 364 valeurs `amont`. C'est exactement
ce que la fiche 0006 a décidé : commiter un fichier engendré pour que la
provenance soit vérifiable. **Elles font leur travail en ne servant à
rien d'exécutable.**

C'est aussi ce qui explique le chiffre qui fait peur : **1 121 valeurs
d'origine `amont`, soit 80 %**, dont 715 dans ce seul fichier
documentaire. Le risque de licence porte donc surtout sur une trace, pas
sur une géométrie.

**Mortes — aucune.** Je n'en ai trouvé aucune qui soit héritée d'une
structure disparue. La migration de ce soir a renommé quatre procédés en
six réglages sans laisser d'orphelin, et l'audit est repassé du premier
coup.

**Deux cas limites**, à surveiller :

- `anthropometry.masses` (8 valeurs, Dempster, toutes vérifiées) —
  **aucun code ne les lit**. Elles ne serviront qu'à un modèle inertiel
  qui n'existe pas.
- `vis` (9) et `roulements` (9) — **aucune pièce ne perce ni ne monte
  quoi que ce soit.** C'est aussi ce qui rend `bd_warehouse` inutile
  aujourd'hui (fiche 0032).

### Le chiffre qui résume

Sur 1 397 valeurs : **8 gouvernent** (0,6 %), **~660 dorment** (47 %),
**715 sont documentaires** (51 %), **0 sont mortes**.

---

## 6 — La distance au premier objet

**Réponse courte : il n'y a plus de distance technique.**

Le plan A4 existe, il est engendré à chaque régénération, et son contenu
a été vérifié dans ce document :

```
YXOR - semelle d'apprentissage
Palier P2 (H = 0.9 m)    matiere : carton_plume    epaisseur 5.0 mm
Hors-tout 136.80 x 49.50 mm    resserrement 0.70 -> 34.65 mm au creux
Rayon interieur minimal 2.5 mm    conges exterieurs 12.38 mm
Materiau isotrope : l'orientation de la feuille est indifferente.
REGLET DE CONTROLE - doit mesurer exactement 100,0 mm
Sinon : reimprimer a 100 %, sans « ajuster a la page ».
```

### Les étapes, ordonnées

| # | Étape | Qui | Durée |
| ---: | --- | --- | ---: |
| 1 | Télécharger le PDF depuis `yxor.fr` | Jeremy | 1 min |
| 2 | Imprimer à **100 %**, sans « ajuster à la page » | Jeremy | 2 min |
| 3 | **Mesurer le réglet** — s'il ne fait pas 100,0 mm, réimprimer | Jeremy | 2 min |
| 4 | Trouver du carton-plume de 5 mm, ou du carton de colis | Jeremy | variable |
| 5 | Coller ou scotcher le plan sur la matière | Jeremy | 5 min |
| 6 | Couper au cutter, en plusieurs passes légères | Jeremy | 20 min |
| 7 | Mesurer la pièce et comparer à 136,80 × 49,50 | Jeremy | 5 min |

**Environ 35 minutes**, plus l'approvisionnement. **Tout dépend de vous ;
rien ne dépend de moi.**

### Mais le site dit « NE PAS COUPER ENCORE »

Le verdict actuel est : *« Le dessin est juste, mais il manque : saignee,
voile min. »*

**Ce verdict est trop strict pour cette pièce-ci**, et je le signale sans
le corriger, puisque ce document ne modifie rien.

La saignée est la largeur de matière emportée par la lame. Elle compte
quand **deux pièces doivent s'emboîter** : si l'on coupe sur le trait, la
languette est trop mince et le logement trop large, et l'assemblage a du
jeu. Le voile minimal est la largeur en dessous de laquelle une bande de
matière se déchire.

Or la semelle d'apprentissage **ne s'interface avec rien** — c'est écrit
dans son propre rôle. Elle n'a ni languette, ni logement, ni voile
étroit : sa largeur minimale est 34,65 mm au creux. **Aucune des deux
valeurs manquantes ne change quoi que ce soit à cette pièce.**

Le verdict `coupable` est calculé par réglage, pas par pièce. Il devrait
sans doute dépendre de ce que la pièce contient — une pièce sans
interface n'a pas besoin de la saignée. **C'est la première fois qu'une
règle du projet se révèle trop stricte plutôt que trop lâche**, et cela
vaut d'être noté : on découvre l'excès de zèle plus tard que le
laxisme, parce qu'il ne casse rien.

**En attendant : couper cette pièce donnerait précisément la mesure de
saignée qui manque.** Le verdict interdit l'acte qui le lèverait.

---

## 7 — Ce que je ferais différemment

Sans ménagement, et par ordre de ce que cela a coûté.

### 1. J'ai construit l'appareil plus vite que l'objet

**17 340 lignes, une pièce, zéro objet physique.**

Le dépôt sait tracer l'origine de 1 397 cotes, refuser un binaire,
comparer deux implémentations de contour au centième de millimètre, et
simuler un changement de taille dans un navigateur. Il n'a **jamais
produit une pièce qu'on puisse tenir**, et il n'en était plus très loin
il y a huit jours.

C'est le regret principal, et il englobe presque tous les autres.

### 2. J'ai proposé avant de mesurer, deux fois

`0021 → 0026 → 0033` : **trois fiches pour une décision.** La 0021
défendait la clé composée avec un argument que je croyais décisif
(l'instabilité des indices de liste). La 0026 l'a remplacée. La 0033 a
enfin chiffré le coût — et le chiffrage a montré que l'option écartée ne
coûtait rien à `origines.yaml` et tout à `nullites.yaml`, ce que ni la
0021 ni la 0026 n'avaient vu.

**J'aurais dû mesurer ce coût dans la 0021.** Il fallait vingt minutes.

Même schéma, plus petit : la fiche 0022 annonçait « un à deux ordres de
grandeur » pour la torsion. Un calcul de dix lignes donnait **395 ×**.
J'avais l'ordre de grandeur en tête et je ne l'ai pas vérifié.

### 3. J'écris trop

**54 % du dépôt est de la prose.** Aujourd'hui : **+1 830 lignes de prose
contre +810 de code**. Le journal du 28 fait 2 845 lignes ; ce matin je
l'ai signalé comme illisible, et j'en ai écrit 1 111 de plus dans la
journée.

La prose de ce projet a une vraie fonction — les fiches ont rattrapé de
vraies erreurs. Mais **un journal qu'on ne peut plus relire ne rattrape
plus rien.** Il faudrait un journal par entrée, pas par jour, et des
fiches plus courtes.

### 4. Ce qui m'a coûté du temps pour rien

- **Une comparaison de Hausdorff écrite, puis remplacée** par une
  comparaison point à point — et **les 16 lignes mortes livrées** dans
  `simulateur.js`, trouvées par l'audit du lendemain.
- **Un premier modèle de largeur de tableau faux**, qui ignorait
  `overflow-wrap`, et qui m'a fait annoncer trois débordements
  inexistants.
- **Les repères du schéma écrits en millimètres**, puis recopiés en dur
  dans le JavaScript, puis republiés en coefficients. La forme linéaire
  était visible dès le premier jour : un repère est toujours « une
  fraction de la longueur ».
- **`regenerer.py` a grossi de 13 % le jour même où je le signalais.**

### 5. Une structure que je regrette

**Le verdict `dessinable` / `coupable` est attaché au réglage, pas à la
pièce.** C'est ce qui produit l'absurdité du § 6 : une pièce qui ne
s'interface avec rien est déclarée non coupable parce qu'une valeur
qu'elle n'utilise pas manque.

J'ai posé cette distinction en une soirée, sans pièce réelle pour la
mettre à l'épreuve. C'est l'exemple même du § 1.

### 6. Ce que je referais pareil

Pour être juste, et parce que ce n'est pas de la complaisance :

- **L'audit d'origine.** Il a attrapé chaque dérive, y compris les
  miennes, y compris ce soir après une migration de quatre tables.
- **Le double calcul du contour, gardé.** Deux implémentations existent,
  elles ne peuvent pas diverger en silence. C'est la bonne réponse à un
  problème qui n'avait pas d'autre solution.
- **Écrire ce que je ne peux pas vérifier.** Pas de navigateur, pas
  d'écran tactile, une norme non lue, un signalement non corroboré. À
  chaque fois, le dire a valu mieux que de l'entourer de prudences.

---

## Ce que ce document ne dit pas

Il mesure le dépôt. Il ne mesure ni le robot, ni ce qu'il devrait faire —
**le seul document manquant qui manque vraiment** (§ 4).

Et il ne dit pas si la méthode vaut ce qu'elle coûte. Dix jours, 17 340
lignes, zéro objet : la réponse viendra quand la semelle sera coupée, pas
d'un audit de plus.
