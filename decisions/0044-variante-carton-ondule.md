# 0044 — La semelle publiée n'est pas celle qui a été coupée

Date : 2026-09-30
Espèce : proposition
État : proposée
Statut : **proposée** — instruction. **Rien n'est généré.**

## Le constat

| | publié sur `yxor.fr` | coupé à l'établi |
| --- | --- | --- |
| réglage | `cutter_cartonplume_5` | cutter × carton ondulé double |
| matière | `carton_plume_5` | `carton_ondule_double` |
| épaisseur (cote F) | **5,0 mm** | **3,5 mm** |
| rayon intérieur min | 2,5 mm (= 0,5 × 5,0) | 1,75 mm au sens de la règle |
| volume | 31 502 mm³ = 6 300,49 × 5,0 | ≈ 22 052 mm³ |
| contour 2D | 138,06 × 51,93 | **identique** |

**Le contour coïncide** — la superposition sur le plan papier l'a
confirmé. C'est normal : aucune des cotes d'échelle ne dépend de la
matière, seules les cotes de procédé changent.

**Mais la traçabilité affirme une matière absente de l'établi.** La page
pièce dit `carton_plume`, la cote F dit 5,0 mm, et le relevé d'origines
fait dériver le rayon minimal d'un réglage qu'on n'a pas employé.

C'est le même défaut que celui du 2026-09-30 sur les mesures, d'un cran
plus haut : **une affirmation exacte dans sa forme et fausse dans son
référent.**

## Faut-il une variante ?

### Ce qui plaide pour

**Le dépôt affirme aujourd'hui quelque chose de faux.** Un lecteur — le
cousin, ou vous dans six mois — qui ouvre la fiche atelier lit
« carton_plume, 5,0 mm » alors que la pièce sur la table est en carton
ondulé de 3,5 mm.

**Et la variante coûte presque rien à produire** : la pièce est déjà
paramétrée par le réglage, `--reglage cutter_cartonondule_double` suffit.
Le générateur produirait un second jeu de fichiers, un second relevé,
une seconde page.

### Ce qui plaide contre

**Le rayon intérieur minimal de cette matière n'est pas mesuré.** Il vaut
aujourd'hui **1,75 mm**, calculé par `0,5 × épaisseur` — et cette valeur
hérite de deux faiblesses :

1. **L'épaisseur est à ±14,3 %.** Le rayon l'est donc aussi : entre 1,50
   et 2,00 mm.
2. **La règle `0,5 × épaisseur` ne décrit que ce que la MATIÈRE
   supporte**, pas ce que le geste permet (fiche 0042). Et l'expérience
   du 2026-09-30 est nette : **R 2,5 mm a déjà été difficile à couper à
   la main**, avec deux passes dans les angles.

Publier une variante à R 1,75 mm reviendrait donc à **publier un plan
plus difficile à couper que celui qui vient de l'être**, sous couvert
d'être « à la bonne matière ».

### Le nœud

> **Une variante fidèle à la matière serait moins fidèle au geste.**

Le dépôt corrigerait une fausseté de traçabilité en introduisant une
fausseté de fabricabilité.

## D'où viendrait le rayon, alors ?

Quatre voies, dont aucune n'est satisfaisante seule.

**A. `0,5 × épaisseur`, comme aujourd'hui.** 1,75 mm. Cohérent avec la
règle écrite, incohérent avec l'expérience. C'est ce que le générateur
ferait sans rien changer.

**B. Reprendre le rayon effectivement coupé : 2,5 mm.** Il est
*vérifié par un objet* — la seule valeur du projet qui le soit. Mais
c'est un accident : 2,5 mm vient de `0,5 × 5,0 mm` du **carton-plume**,
pas d'une propriété du carton ondulé. Le reprendre serait garder un
nombre juste pour une mauvaise raison.

**C. Mesurer le rayon de geste** (fiche 0042) et prendre
`max(0,5 × ep ; rayon_geste)`. **C'est la seule voie qui répond vraiment
à la question**, et elle demande une manipulation : couper une série de
congés décroissants et noter où le trait cesse d'être suivi.

**D. Ne pas publier de variante**, et corriger la traçabilité autrement —
par une mention sur la page pièce disant en quelle matière l'exemplaire
a été coupé.

## Ce que je recommanderais, si l'on me le demandait

**D maintenant, C ensuite, puis la variante.**

Parce que le problème constaté est un problème de **dire**, pas de
**produire** : la pièce coupée est bonne, c'est sa description qui ment.
Publier un second plan plus difficile à couper pour réparer une phrase
serait disproportionné.

Et parce que **C débloque bien plus que cette variante** : le rayon de
geste manque à toutes les pièces futures coupées à la main, pas
seulement à celle-ci.

## Ce que cette fiche ne tranche pas

1. **La forme de la mention (voie D).** Un champ `exemplaire_coupe:` sur
   la pièce ? Une entrée dans `mesures.yaml` ? Un simple paragraphe ?
   Je penche pour le plus léger, mais c'est à décider.
2. **Faut-il un jour deux variantes publiées, ou une seule ?** Le site
   n'a jamais affiché deux réglages pour une même pièce. Rien ne l'en
   empêche — `page_piece` est indexée par pièce, pas par réglage — mais
   ce serait une première, et l'index des pièces devrait le montrer.
3. **Et la question que la fiche 0042 laisse ouverte, qui commande tout
   le reste** : `0,5 × épaisseur` est dans `CLAUDE.md` depuis le premier
   jour et **aucune fiche ne l'établit**. Tant qu'on ne sait pas d'où
   elle vient, on ne sait pas non plus ce qu'elle prétend couvrir.

## Renvois

- **0042** — le rayon minimal décrit la matière, pas le geste. C'est la
  fiche mère de celle-ci.
- **0043 §3** — une mesure porte la matière *supposée*, et rien ne peut
  vérifier la supposition. Ici, c'est une *pièce publiée* qui porte un
  réglage supposé, et le même aveuglement joue.
- **0037** — le verdict `coupable`. La variante hériterait de
  `besoins_procede: [epaisseur, rayon_interieur_min]`, donc serait
  coupable dès que ces deux valeurs existent — ce qui est le cas.
  **Elle serait déclarée coupable alors qu'elle est plus difficile à
  couper que celle qui l'a été.** Le verdict ne voit pas la difficulté,
  seulement la complétude.
