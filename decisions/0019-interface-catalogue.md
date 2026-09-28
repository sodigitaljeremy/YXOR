# 0019 — Interface : le site devient un catalogue technique

Date : 2026-09-28
Statut : **acceptée** le 2026-09-28 — codée le jour même.
Trois précisions ajoutées à la validation : lettrage par rang de
lecture, verdict dessinable/coupable porté aussi par la fiche
atelier, rail du rang 1 conservé à zéro. Le raisonnement ci-dessous
n'est pas réécrit (règle 5).

## Référence : McMaster-Carr

Quatre principes retenus, et ce qu'ils impliquent ici :

| Principe | Conséquence pour yxor.fr |
| --- | --- |
| **La fonction avant la forme** | Les utilisateurs sont un débutant en mécanique et un opérateur de découpe. Aucun des deux n'est à séduire : ils cherchent une information précise et la veulent tout de suite. |
| **Manuel et catalogue à la fois** | L'explication vit **à côté de la valeur**, jamais dans une page d'aide. Une colonne « source » n'est pas une note de bas de page. |
| **Un schéma accompagne les spécifications** | Un dessin coté **lettré**, dont les lettres sont les identifiants du tableau. C'est le geste central de McMaster, et il manque au site. |
| **Rien qui distraie** | Aucune couleur décorative. Toute couleur porte un sens — l'origine — ou n'existe pas. |

## 1 — Schéma coté, en SVG inline

`scripts/plan_decoupe.py` sait déjà discrétiser les contours d'une face
en polylignes. La même fonction sert au SVG : **un seul code produit le
plan A4 et le schéma de la page**, donc les deux ne peuvent pas diverger.

### Le geste McMaster : lettrer le dessin, lettrer le tableau

```
      ┌─ A ─────────────────────────────────┐
      │                                     │
   ╭──┴──────╮                     ╭────────┴──╮
  ╱  E        ╲___________________╱             ╲      ┬
 │                     ⌒ F                       │     │ B
  ╲            ╱‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾╲             ╱      │
   ╰─────────╯          ┬          ╰───────────╯       ┴
                        │ C
        |←──────── A ───┴──────────→|

        →  SENS DES CANNELURES        (si matériau anisotrope)
```

| | Cote | Valeur | Origine | Source |
| --- | --- | --- | --- | --- |
| **A** | longueur | 136,80 mm | propre | H × `ratios.pied_longueur` |
| **B** | largeur | 49,50 mm | propre | H × `ratios.pied_largeur` |
| **C** | largeur au creux | 34,65 mm | propre | choix : `ratio_resserrement` |
| **E** | congé extérieur | 12,38 mm | propre | choix : `ratio_coins` |
| **F** | rayon intérieur | 2,50 mm | procédé | 0,5 × épaisseur |

**La pièce déclare ses cotes de schéma** dans son relevé — quelle lettre,
quel type de ligne de cote, quelle valeur. Le générateur dessine, il
n'interprète pas. Le principe tient : **l'application ne crée aucune
donnée**.

Le schéma est **statique** : pas de JavaScript, pas d'animation. Il
s'imprime, il se cite, il fonctionne sans réseau.

## 2 — Le tableau des origines : hiérarchie par ce qu'il y a à FAIRE

Le tableau actuel est dense mais plat : dix-sept lignes de même poids.
Pour balayer des yeux, il faut une hiérarchie — et la bonne hiérarchie
n'est pas l'ordre alphabétique des origines, c'est **l'action qu'elles
appellent**.

Trois rangs, dans cet ordre :

```
╔═ 1 · À TRAITER ══════════════════════════════════ 2 cotes ═╗
║  rouge — un défaut, ou une valeur encore absente           ║
║  · non qualifié      aucune déclaration                    ║
║  · ambigu            la taxonomie ne couvre pas le cas     ║
║  · mesure sans source   annoncée mesurée, sans relevé      ║
╚════════════════════════════════════════════════════════════╝

╔═ 2 · EMPRUNTÉ ═══════════════════════════════════ 0 cote ══╗
║  orange — vient de ToddlerBot, porte le risque de licence  ║
╚════════════════════════════════════════════════════════════╝

╔═ 3 · ÉTABLI ═════════════════════════════════════ 7 cotes ═╗
║  vert/bleu — sourcé, et rien à en faire                    ║
║  · propre · littérature · catalogue · mesure sourcée       ║
╚════════════════════════════════════════════════════════════╝
```

**Ce qui change concrètement :**

- **Un rail de couleur à gauche du groupe**, au lieu d'une pastille par
  ligne. Dix-sept pastilles font du bruit ; trois rails font une
  structure.
- **Le compte est dans le titre du rang.** On sait en une seconde s'il y
  a quelque chose à traiter, sans lire une ligne.
- **Les rangs vides sont affichés quand même**, avec « 0 cote ». Un rang
  absent se lirait « sans objet » ; un rang à zéro se lit « rien à
  traiter ». C'est la règle du « non déterminé », appliquée aux groupes.
- **Repli natif** par `<details>` sur le rang 3 seulement — HTML pur,
  sans JavaScript ni animation. Ce qui est établi n'a pas besoin d'être
  lu ; ce qui est à traiter, si.

## 3 — `/etat/` : ce qu'il reste à faire, en un endroit

Aujourd'hui les valeurs manquantes sont dispersées entre `hardware.yaml`,
`anthropometry.yaml` et `joints.yaml`. La page les rassemble — **sans
rien inventer** : tout est dérivé.

**Correction apportée à cette maquette après vérification** : j'avais
prévu un indicateur binaire « complet / incomplet ». Il est faux.
`cutter_carton` a `saignee` et `voile_min` à `null`, et pourtant la
semelle se construit — parce que **dessiner** et **couper proprement**
n'exigent pas les mêmes valeurs. D'où deux niveaux :

| Niveau | Exige | Ce qu'il autorise |
| --- | --- | --- |
| **Dessinable** | `epaisseur`, `rayon_interieur_min` | la pièce se génère, le STL et le STEP sont justes |
| **Coupable** | en plus `saignee`, `voile_min` | le DXF peut partir chez le découpeur |

Un DXF dessinable mais non coupable est un piège : il a l'air complet.
La page doit donc distinguer les deux, pas les confondre.

```
ÉTAT DU PROJET                                      2026-09-28

CE QUE JE PEUX FAIRE AUJOURD'HUI
                          dessiner   couper     manque pour couper
  cutter_carton              oui       non      saignée, voile mini
  cutter_carton_ondule       NON       non      épaisseur, rayon mini,
                                                saignée, voile mini
  laser_contreplaque         oui       non      saignée, voile mini
  decoupe_metal              NON       non      machine, rayon mini,
                                                saignée, voile mini

À MESURER                                              12 valeurs
  hardware.yaml  procedes.*.saignee              4   coupe d'essai
  hardware.yaml  materiaux.*.masse_surfacique    4   balance 0,1 g
  ...

NON VÉRIFIÉ                                            14 valeurs
  anthropometry.yaml  ratios.*   figure 4.1 non lisible dans le texte

CONFIANCE INCONNUE                                     16 sur 17
  joints.yaml  materiel.confiance = deduite_du_modele
               le MJCF représente, il ne décrit pas
```

**Chaque ligne est dérivée** : les `null` de `hardware.yaml`, les
`verifie: false` de `anthropometry.yaml`, les `confiance` de
`joints.yaml`. Rien n'est saisi à la main, donc rien ne peut se
désynchroniser.

Le premier bloc est le plus utile au quotidien : **il répond à « qu'est-ce
que je peux couper ce soir ? »** par oui ou non, et nomme ce qui manque
quand c'est non.

## 4 — GitBuilding : ce qui est transposable

Outil de l'équipe OpenFlexure. Documentation matérielle en Markdown, avec
un langage — *BuildUp* — qui ajoute des liens sémantiques.

**Non adopté comme dépendance**, conformément à la demande. Ses idées,
examinées une par une :

| Idée de GitBuilding | Verdict |
| --- | --- |
| **La nomenclature est ENGENDRÉE, jamais saisie.** `[vis M3](m3.md){Qty: 4}` compte tout seul ; deux mentions de la même vis font deux vis | **À prendre.** C'est déjà notre principe, mais nous n'avons pas de nomenclature. Une pièce pourrait déclarer sa visserie ; le site l'agrège |
| **Bibliothèque de pièces en YAML référencée par clé** : `[Part](library.yaml#key)` | **Déjà fait sans le savoir** : `hardware.yaml` est exactement cette bibliothèque, et `origines.yaml` référence ses clés. Bon signe : deux projets ont convergé |
| **Outils distincts des pièces**, et la quantité d'un outil est le MAXIMUM et non la somme — on n'achète pas deux cutters parce qu'on s'en sert deux fois | **À prendre.** Règle d'agrégation juste et non évidente. Nos `procedes` sont des outils, notre `vis`/`roulements` des pièces |
| **En-tête de détails** : vignette, durée, difficulté, compétences requises | **À prendre pour la vue atelier.** « Temps : 20 min · Difficulté : facile · Outil : cutter » en tête de page dit à l'opérateur s'il peut s'y mettre maintenant |
| **Étapes numérotées** `{pagestep}`, référençables entre pages | **À prendre plus tard**, quand une pièce aura un montage. Aujourd'hui il n'y a rien à assembler |
| **Le langage BuildUp lui-même** | **À écarter.** Ce serait une seconde source de vérité à côté du dépôt — exactement ce que la fiche 0018 interdit |
| **Aperçus 3D embarqués** | Déjà fait |

## 5 — Typographie et couleur

- **Aucune police téléchargée.** Pile système, comme aujourd'hui : le
  site doit se reconstruire à l'identique dans dix ans.
- **Chiffres tabulaires partout** (`font-variant-numeric: tabular-nums`).
  Dans un tableau de cotes, des chiffres qui ne s'alignent pas empêchent
  de comparer deux valeurs d'un coup d'œil.
- **Monospace pour les identifiants** — clés, noms de fichiers, chemins.
  Ce qui se tape se distingue de ce qui se lit.
- **Palette réduite.** Les six couleurs d'origine restent, mais
  **désaturées et déplacées en rails** plutôt qu'en pastilles pleines.
  Une couleur ne sert qu'à porter l'origine : jamais un aplat décoratif,
  jamais un dégradé.
- **Densité conservée.** McMaster est dense, et c'est une qualité :
  aérer un tableau de cotes obligerait à faire défiler pour comparer.

## Ce qui ne change pas

- Le site reste **statique et engendré**, sans dépendance ni CDN.
- **La traçabilité reste le sujet** de la page pièce : le schéma la
  sert, il ne la remplace pas — les lettres du dessin sont les lignes du
  tableau des origines.
- **Aucune animation décorative.** Le seul comportement dynamique reste
  la rotation du modèle 3D, qui est une fonction, pas un ornement.
