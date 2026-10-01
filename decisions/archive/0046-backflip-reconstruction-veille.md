# 0046 — Backflip AI : une CAO paramétrique reconstruite ? Vérifié, pas adopté

Date : 2026-09-30
Espèce : veille
État : veille
Statut : **veille** — aucune adoption, aucun abonnement, aucune place dans la chaîne. build123d reste la source de vérité. Un test sur la semelle est préparé ; Jeremy le lancera.
Découle de : `0045-reconstruction-et-amont.md` (écrite avant celle-ci)

## Le signalement

Un retour extérieur signale **Backflip AI**. L'outil reconstruirait une
CAO **paramétrique** — arbre de features, esquisses, STEP — depuis un
scan, un STL, un plan 2D ou des photos.

Si c'est exact, une généralisation antérieure tombe : « les générateurs
3D par IA produisent des maillages, pas des solides ». Elle reposait sur
trois outils seulement, Meshy, Rodin et Tripo.

**Cette phrase n'est pas dans le dépôt.** `grep -ri
"maillage\|Meshy\|Tripo\|Rodin"` ne la trouve dans aucune fiche, aucun
journal, aucun paramètre. La cartographie à corriger vit ailleurs. Rien
ici ne peut donc la corriger ; on peut seulement constater qu'elle
n'était pas tracée.

## 1 — Vérification, le 2026-09-30

Méthode : recherche web et lecture des pages avec un client automatique.
**Ce client passe par un modèle qui résume** : les « citations »
ci-dessous sont celles qu'il a rendues, pas un relevé caractère par
caractère.

| Affirmation | Verdict | Fondement |
| --- | --- | --- |
| **reconstruction paramétrique réelle, pas un maillage habillé** | **affirmée, non vérifiée** | Seules sources : l'éditeur et la presse spécialisée qui relaie son annonce. develop3d (4 août 2026) décrit des « modèles CAO paramétriques entièrement modifiables » avec arbre de features ; le résumé de l'article ne signale **aucun essai indépendant**. Un essai pratique existe (Fabbaloo, « Hands on with Backflip.ai ») mais il n'a pas pu être lu (HTTP 403). L'éditeur dit lui-même que l'outil excelle sur les « pièces de complexité modérée, fraisées 3 axes et tournées ». |
| **drawing-to-CAD, septembre 2026** | **vérifié, comme annonce** | develop3d, 17 septembre 2026 : lancement à Autodesk University 2026, disponible dans Fusion et dans l'application web, 5 à 30 min et « 10 $ ou moins » par pièce. **Photo-to-CAD** est annoncé en même temps. |
| **aucune API ni CLI publique** | **non trouvée — ce qui ne prouve pas l'absence** | Aucune mention d'API, de SDK ou de CLI sur la page d'accueil, dans les conditions, ni dans les deux articles. Intégrations annoncées : complément Fusion et application web ; Onshape et d'autres « à venir ». Des sources plus anciennes citent un complément SolidWorks. |
| **conditions d'août 2026 : licence d'entraînement par défaut** | **vérifié** | Conditions d'utilisation, mises à jour le **4 août 2026** : licence pour « entraîner, développer, améliorer » le service, et pour partager ou sous-licencier les modèles avec d'autres utilisateurs. **Privacy Mode** lève l'entraînement ; **Private Library Mode** lève le partage. L'utilisateur doit avoir « des droits suffisants » sur ce qu'il envoie. La propriété exclusive des résultats n'est **pas garantie**. |
| **modes Privacy à certains niveaux seulement** | **vérifié en principe, non vérifié en détail** | Les conditions renvoient la disponibilité à l'offre souscrite. La page des tarifs, lue ce jour, **ne dit pas quelles offres les incluent**. |
| **tarifs : 60 crédits d'essai, puis 20 $/mois** | **partiellement faux** | La page des tarifs, lue ce jour, dit **50 crédits** d'essai, sans carte bancaire. Builder : 20 $/mois pour 100 crédits. Pro : 50 $ pour 300. Business : 380 $ pour 2 500. Une tâche Fast coûte **10 crédits**, une tâche Thinking **50**. **L'essai permet donc cinq tâches Fast, ou une seule Thinking.** |

**Conclusion du § 1.** Quatre points sur cinq tiennent, dont un avec un
chiffre corrigé. **Le premier — le seul qui compte — n'est ni confirmé
ni infirmé** : il n'est attesté que par l'éditeur. Or c'est
précisément ce qu'un test sur une pièce dont on connaît la vérité peut
établir. Le § 2 n'est donc pas conditionné à une certitude qu'on
n'obtiendra pas autrement : **il sert à vérifier le point 1**.

### Sources

- develop3d, « Backflip AI updated engine flips mesh into feature tree-CAD model », 2026-08-04 — https://develop3d.com/ai/backflip-ai-reverse-engineering
- develop3d, « Backflip now converts 2D engineering drawings directly into CAD », 2026-09-17 — https://develop3d.com/cad/backflip-converse-2d-engineering-drawings-directly-into-cad
- Backflip, conditions d'utilisation, mises à jour le 2026-08-04 — https://www.backflip.ai/legal/terms-of-service
- Backflip, tarifs, lus le 2026-09-30 — https://www.backflip.ai/pricing
- Backflip, page d'accueil, lue le 2026-09-30 — https://www.backflip.ai/
- Fabbaloo, « Hands on with Backflip.ai » — **non lu** (403)

## 2 — Le protocole de test sur la semelle

**Rien n'est téléversé par l'assistant.** Jeremy lance le test.

### Pourquoi la semelle

- **Originale** : aucune cote `amont` (relevé de la pièce). La fiche 0045
  ne l'interdit donc pas.
- **Simple**, mais pas triviale : elle combine des congés convexes, des
  raccords concaves et un grand arc de creux. Elle permet de juger si
  l'outil reconnaît des arcs ou s'il les approche.
- **Vérité connue par construction**, et mesurée le 2026-09-29 sur le
  STEP produit à l'empreinte `7d61326025` :

| Grandeur | Vérité | Mesurée par |
| --- | ---: | --- |
| boîte englobante | **138,06 × 51,93 × 5,00 mm** | build123d, import du STEP |
| volume | **31 502,4 mm³** | idem |
| aire de la face | **6 300,46 mm²** | relevé de la pièce |
| aire totale | 14 412,28 mm² | build123d |
| faces | **18 : 8 planes, 10 cylindriques** | idem |
| arêtes | 48 : 28 droites, 20 circulaires | idem |
| congés convexes | **4 × R 12,98** | arêtes circulaires du STEP |
| raccords concaves | **4 × R 2,50** (le rayon minimal du procédé) | idem |
| arcs du creux | **2 × R 80,36**, centres en X = 0 | idem |
| largeur au creux | **36,35 mm** | relevé |
| position du creux | **au milieu de la longueur**, pièce symétrique en X et en Y | centres des arcs |

### Les entrées — trois sur quatre possibles sans scanner

| Entrée | Fichier | Outil | Disponible ? |
| --- | --- | --- | --- |
| **E1** maillage | le STL exporté (820 triangles) | Scan/Mesh to CAD | **oui**, engendré |
| **E2** plan | le PDF A4 de découpe | Drawing to CAD | **oui**, engendré — mais il n'a qu'une vue et donne l'épaisseur en texte : c'est un test difficile |
| **E3** photos | la semelle réellement coupée, en ondulé | Photo to CAD | **oui** — sa vérité est moins sûre : la pièce porte l'erreur de coupe et fait 3,5 mm, pas 5 |
| **E4** scan | — | Scan to CAD | **non : aucun scanner 3D** |

**Une nuance au constat de Jeremy.** Je ne compte pas trois usages sur
quatre qui supposent un scanner, mais **deux** : le scan lui-même, et le
STL **d'un objet physique** (un STL d'une pièce qu'on a déjà en CAO ne
sert qu'au test). D'après l'éditeur, Photo to CAD n'exige qu'un
téléphone, et Drawing to CAD un plan. Pour les usages **réels**, hors
test, l'absence de scanner ferme donc le scan et le STL d'objet
physique. La photo et le plan restent ouverts.

### Budget

L'essai donne 50 crédits, soit **cinq tâches Fast**. Plan proposé :
E1, E1 **une seconde fois** (reproductibilité : même entrée, même
sortie ?), E2, E3. Cela fait 40 crédits et en laisse 10 pour un
imprévu. **Pas de mode Thinking** : il consommerait l'essai entier sur
une seule entrée.

### Avant l'envoi

1. Régénérer, puis noter l'empreinte du site et le **sha256 de chaque
   fichier envoyé**. Le STEP est réécrit à chaque régénération : son
   empreinte n'est valable que pour l'exemplaire envoyé.
2. **Mesurer l'erreur propre de l'entrée E1** : l'écart de Hausdorff
   entre les sommets du STL et le contour exact (`profil.contour`). Un
   STL à 820 triangles approche les arcs par des cordes. Une
   reconstruction qui « rate » d'autant ne rate rien : elle recopie son
   entrée. **Sans cette ligne de base, le résultat n'est pas
   interprétable.**
3. Noter l'offre, et si Privacy Mode est **disponible et activé**. À
   l'essai, il ne l'est probablement pas : **la semelle servirait alors
   à l'entraînement.** Pour cette pièce, c'est acceptable (elle est
   publiée sur `yxor.fr`). Cela doit néanmoins être écrit.

### Ce qu'on compare

**Portes binaires d'abord.** Chacune dit si le résultat est une CAO ou
un maillage déguisé :

| Porte | Attendu |
| --- | --- |
| solide fermé, valide | oui |
| types de surfaces | **plans et cylindres seulement**. Une B-spline ou des centaines de facettes planes = un maillage habillé. |
| nombre de faces | 18, ou proche avec une justification |
| arbre de features | au moins une esquisse et une extrusion |
| **paramétrique pour de vrai** | dans Fusion, passer l'extrusion de 5 à 3,5 mm et réexporter : **volume attendu 22 051,7 mm³**, à 0,1 % près |

La dernière porte est **la seule qui réponde au point 1**. Un arbre qui
ne se laisse pas modifier n'est pas paramétrique, quel que soit son
aspect.

**Puis les grandeurs**, en écart à la vérité : boîte englobante,
volume, aire de face, les trois familles de rayons, la largeur au creux,
la position des centres, et **l'écart de Hausdorff du contour**. Pour ce
dernier, on coupe le STEP rendu à mi-épaisseur et on le compare à
`profil.contour` avec `profil.hausdorff`, qui existent déjà.

### Seuils

| Niveau | Seuil | Justification |
| --- | --- | --- |
| **fidèle** | Hausdorff ≤ **0,05 mm**, volume à 0,1 % près, rayons à 0,05 mm près | C'est `TOLERANCE_MM` de `profil.py` : la tolérance déjà admise entre deux implémentations de la **même** forme. |
| **exploitable pour la découpe** | Hausdorff ≤ **0,5 mm**, rayons à 0,25 mm près | **Déduit, pas mesuré.** C'est l'ordre de grandeur d'une coupe au cutter guidé à la main et d'une lecture à la règle à demi-graduation (`mesures.yaml`). Aucune mesure du dépôt n'établit encore la précision du geste (fiche 0042). |
| **inexploitable** | une porte binaire qui échoue, **ou** un écart supérieur à 0,5 mm | — |

Pour **E3**, seul le second seuil s'applique, et l'épaisseur attendue est
3,5 mm. La pièce coupée n'est pas la vérité : elle en est un exemplaire.

### Où vivrait l'expérience — proposé, rien de créé

- **Les fichiers rendus par Backflip** (STEP, exports Fusion) : **hors
  Git**. Ils ne se régénèrent pas, ils sont tiers, et leur propriété
  n'est pas garantie par les conditions. Ils seraient rangés hors du
  dépôt et inscrits au registre de la fiche 0030
  (`params/fournisseurs.yaml`), avec les six champs. Il faudrait y
  ajouter : sha256 de l'**entrée**, mode, offre, Privacy Mode oui ou
  non, version des conditions (2026-08-04).
- **Le protocole et les résultats chiffrés** : un répertoire
  `experiences/2026-09-backflip-semelle/`, en texte, **hors de
  `params/`**. S'ils étaient dans `params/`, `audit_origines` exigerait
  une origine pour chaque écart mesuré, et ces nombres ne sont pas des
  cotes.
- **La comparaison** : un script `scripts/comparer_reconstruction.py`,
  qui applique les portes et les seuils ci-dessus au STEP rendu. Il est
  **à écrire après décision**, pas avant.

## 3 — La règle, écrite avant le test

Elle est dans la **fiche 0045**, qui la pose pour tout outil de
reconstruction. Elle a été écrite avant celle-ci et avant tout envoi.

## 4 — Deux questions que le retour ne pose pas

**Instruites, pas tranchées.**

### a) Reconstruire depuis un plan constructeur sous droits

La fiche 0030 définit un fichier fournisseur comme « tout fichier
obtenu d'un catalogue, constructeur ou distributeur : modèle CAO,
**plan**, nomenclature… ». **Un plan constructeur en est un.**

**Le cas est-il analogue à McMaster ?** Sur le point essentiel, oui :
la clause citée par la 0030 vise nommément **la création d'œuvres
dérivées**. Une CAO reconstruite depuis un plan est une œuvre dérivée
de ce plan, au même titre qu'un modèle McMaster retouché. **La
reconstruction ne blanchit pas plus un plan fournisseur qu'une
géométrie amont** : c'est le même raisonnement que la 0045.

**Deux différences, qui compliquent :**

1. **L'envoi lui-même.** Chez McMaster, le fichier reste sur le poste.
   Ici, il part chez un tiers qui, par défaut, s'accorde une licence
   d'entraînement et de partage. On pourrait enfreindre les conditions
   du plan **avant même d'avoir une pièce**.
2. **Le fait et l'œuvre.** CLAUDE.md distingue déjà les deux : « une
   valeur, jamais le texte ». L'entraxe de fixation d'un servomoteur,
   relevé sur son plan et cité avec sa référence, est **un fait**,
   c'est-à-dire une cote d'interface (règle 2). La géométrie complète
   du boîtier, reconstruite, relève de **l'œuvre**. Le dépôt sait déjà
   prendre la première sans la seconde, **sans aucun outil de
   reconstruction**.

**Question restée ouverte** : un plan constructeur **publié pour être
utilisé**, comme le plan d'encombrement d'un servomoteur, change-t-il
quelque chose ? Cela dépend des conditions de **chaque** plan. Il n'y a
pas de réponse générale, et ce n'est pas un avis juridique (0010 §4).

### b) Quelle origine pour une cote issue d'une reconstruction ?

Ni `catalogue`, ni `mesure`, ni `propre`, en effet. Trois voies :

| Voie | Principe | Ce qu'elle coûte |
| --- | --- | --- |
| **A. Nouvelle origine `reconstruction`** | symétrique de `norme` (0035) | **Elle efface la source.** Une cote reconstruite depuis l'amont sortirait de la colonne `amont` de l'audit. C'est le blanchiment que la 0045 interdit, **rendu possible par la taxonomie elle-même**. |
| **B. Origine héritée de l'entrée, plus un champ de transformation** | l'origine est celle de ce qu'on a envoyé (`propre` pour la semelle, `mesure` pour un scan, `catalogue` pour un plan constructeur, `amont` pour ToddlerBot) ; un champ `obtenue_par: reconstruction` porte l'outil, la date et l'empreinte de l'entrée | Un axe de plus. Mais c'est la forme de la 0035 corrigée : un axe **calculé** à partir d'un fait, pas une origine déclarée. |
| **C. Une reconstruction n'est jamais une source** | elle sert à **contrôler** (comparer à une mesure), jamais à **fournir** une cote | La plus simple. Elle ferme l'usage « rétro-ingénierie d'une pièce du commerce », qui est pourtant le cas d'usage annoncé de l'outil. |

**Une asymétrie à noter, sans conclure** : A est la seule voie
incompatible avec la 0045. B demande que l'incertitude de la
reconstruction soit portée, ce qui renvoie à la 0041, encore proposée.
C ne demande rien.

**Même famille que la 0035**, comme le signale Jeremy. Toutes deux
posent la même question : faut-il une origine de plus, ou un axe de
plus ? La 0035 a répondu « axe calculé » pour la vérifiabilité, et elle
n'est toujours pas appliquée. **Il serait cohérent de trancher les
deux ensemble.**

## 5 — Ce qui reste vrai

- **Pas d'adoption, pas d'abonnement, pas de place dans la chaîne.**
  build123d reste la source de vérité ; aucune pièce YXOR ne sera
  décrite ailleurs que dans `parts/`.
- **Aucun scanner 3D.** Voir § 2 : cela ferme deux usages réels sur
  quatre, pas trois.
- **Aucune API trouvée** : même adopté, l'outil ne pourrait pas entrer
  dans `regenerer.py`, qui ne connaît que ce qui se relance en local.
  Une étape manuelle dans une chaîne régénérable serait une source de
  vérité parallèle.

## Déclencheur

**Les deux conditions ensemble :**

1. le test du § 2 passe **toutes** les portes binaires, et au moins le
   seuil « exploitable » sur E1 ;
2. **et** une pièce YXOR réelle a besoin d'une géométrie qu'on ne peut
   que **relever** — une pièce du commerce à loger, un objet physique —
   sur une source dont Jeremy a les droits (0045, § 4a).

Tant que la seconde condition manque, un test réussi ne change rien :
**il vérifie l'outil, il ne crée pas le besoin.**
