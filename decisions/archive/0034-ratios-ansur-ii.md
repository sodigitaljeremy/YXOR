# 0034 — ANSUR II remplace Drillis & Contini

Date : 2026-09-29
Espèce : historique
État : appliquée
Statut : **acceptée** le 2026-09-29, sur décision de Jeremy — appliquée
le jour même.
Amende : `0012-correction-anthropometry.md`, dont la correction de
sourcing tient toujours mais dont les valeurs sont remplacées.

## Ce qui ne pouvait pas durer

Les quatorze ratios venaient de la **figure 4.1 de Winter** — un
graphique. Aucun de ces nombres n'apparaît dans le texte, et la source
primaire (Drillis & Contini, Office of Vocational Rehabilitation, 1966)
n'est pas accessible. Le fichier les portait avec `verifie: false`,
**quatorze fois**, depuis la fiche 0012.

ANSUR II est l'inverse exact : **93 mesures directes sur 6 068
personnes**, en CSV public. Vérifié en le téléchargeant :
**4 082 hommes + 1 986 femmes**, 108 colonnes, longueurs en millimètres.

On ne croit plus un graphique sur parole : `scripts/ratios_ansur.py`
recalcule, et n'importe qui peut relancer.

## La méthode, et un choix qui n'est pas neutre

Chaque ratio est calculé **sujet par sujet**, puis moyenné :

    ratio = moyenne sur les sujets de ( mesure_i / stature_i )

Et **non** : moyenne des mesures divisée par moyenne des statures. Les
deux diffèrent, et seule la première a un sens — on cherche la proportion
**d'un corps**, pas la proportion d'un corps moyen qui n'existe pas.

Conséquence utile : l'écart-type obtenu décrit la dispersion **des
proportions**, ce qui est exactement la question qu'on se pose quand on
met un robot à l'échelle.

## Les valeurs

| Ratio | ANSUR II | σ | D&C | écart |
| --- | ---: | ---: | ---: | ---: |
| hauteur_hanche | 0,5149 | 0,0152 | 0,530 | −2,9 % |
| cuisse | 0,2476 | 0,0113 | 0,245 | +1,1 % |
| **tibia** | 0,2267 | 0,0088 | 0,246 | **−7,9 %** |
| pied_longueur | 0,1534 | 0,0055 | 0,152 | +0,9 % |
| pied_largeur | 0,0577 | 0,0029 | 0,055 | +4,9 % |
| cheville_hauteur | 0,0405 | 0,0032 | 0,039 | +4,0 % |
| **largeur_epaules** | 0,2328 | 0,0114 | 0,259 | **−10,1 %** |
| largeur_bassin | 0,2036 | 0,0167 | 0,191 | +6,6 % |
| tronc_hauteur | 0,3052 | 0,0154 | 0,288 | +6,0 % |
| bras | 0,1909 | 0,0062 | 0,186 | +2,7 % |
| avant_bras | 0,1511 | 0,0067 | 0,146 | +3,5 % |
| main_longueur | 0,1104 | 0,0044 | 0,108 | +2,3 % |
| tete_hauteur | **non dérivable** | | 0,130 | conservé |
| cou_hauteur | **non dérivable** | | 0,052 | conservé |

**12 ratios sur 14 passent de `verifie: false` à `verifie: true`.**

L'écart le plus fort est la **largeur d'épaules, −10,1 %**. Sur un robot
de 90 cm, cela fait 23,6 mm d'épaules en moins. Ce n'est pas un
ajustement cosmétique.

### Les deux non dérivables, et pourquoi

ANSUR mesure le **tragion** (le repère de l'oreille) et la **cervicale**
(la septième vertèbre), pas le menton ni le sommet du crâne sur la même
verticale. La hauteur de tête et la hauteur de cou ne s'en déduisent pas
sans inventer un repère.

Elles restent chez Drillis & Contini, avec leur `verifie: false`. **Le
fichier porte donc deux sources, et le dit ligne par ligne** — c'est la
leçon de la fiche 0012, où le fichier annonçait une seule source pour
tout.

## Les deux réserves, portées dans le fichier

**1. Population militaire, explicitement non représentative.** Des
soldats américains en activité, sélectionnés sur des critères physiques,
d'âge resserré. Un robot dimensionné là-dessus est proportionné comme un
militaire de 2012 — pas comme un humain moyen, et encore moins comme un
humain quelconque.

**2. ANSUR II ne donne QUE des longueurs.** Les masses segmentaires ne se
mesurent pas sur un vivant : elles viennent de dissections. Elles
**restent chez Dempster** (via Winter tab. 4.1), toutes vérifiées, et
leur contrôle de cohérence à 1,000000 est intact.

Les deux réserves sont écrites en tête du bloc `ratios:`, pas seulement
ici : qui ouvre `anthropometry.yaml` les lit avant les nombres.

## Ce que cela change à la seule pièce existante

| | avant | après |
| --- | ---: | ---: |
| longueur | 136,80 mm | **138,06 mm** |
| largeur | 49,50 mm | **51,93 mm** |

⚠ **Le DXF et le plan A4 ont changé.** Toute impression antérieure est
périmée. Il faut retélécharger avant de couper.

C'est exactement ce pour quoi le projet est paramétrique — mais c'est la
première fois qu'un changement de source déplace une géométrie, et cela
mérite d'être dit plutôt que constaté.

## Provenance et redistribution

Les deux CSV sont inscrits dans `params/fournisseurs.yaml` avec leurs six
champs, dont l'empreinte (fiche 0030).

**Redistribuables** : œuvre du gouvernement fédéral américain, donc du
domaine public aux États-Unis (17 U.S.C. § 105), rapport technique en
diffusion illimitée (DTIC ADA611869).

**Réserve portée dans le registre** : ce classement est **déduit du
statut de l'auteur, pas lu dans un fichier de licence** accompagnant les
CSV, et la copie employée est un miroir tiers.

**Ils ne sont pourtant pas commités**, bien que redistribuables : 2,9 Mo
de données brutes, régénérables, mises en cache dans `exports/ansur/`.
La règle 4 les laisserait passer — c'est du texte — mais le principe
tient : **le dépôt porte le code qui produit, pas les données qu'il
consomme.**

## Ce que le script ne fait pas

Il **n'écrit pas** `anthropometry.yaml`. Il produit un bloc à recopier
(`--yaml`). Remplacer quatorze cotes d'échelle est une décision, pas un
effet de bord — même règle que la simulation du navigateur (fiche 0023) :
calculer n'est pas enregistrer.

L'application de ce jour a été faite à la main, sur décision explicite.

---

## Troisième réserve, ajoutée le 2026-09-29 : la comparabilité perdue

Drillis & Contini est la **référence commune du champ biomécanique**.
Winter la reproduit, les manuels la reprennent, et la plupart des projets
de robotique humanoïde qui se disent anthropomorphes en dérivent — sans
toujours le dire.

En recalculant nos propres ratios, **nous sortons de cette référence**.
Nos proportions ne sont plus comparables à celles des autres projets :
dire « notre tibia fait 0,2267 de la stature » n'a plus de sens commun
avec « le leur fait 0,246 », puisque les deux nombres ne décrivent plus
la même population.

**C'est un bon échange**, et la raison est nette : nous troquons la
comparabilité contre la **vérifiabilité**. Les quatorze ratios étaient
invérifiables ; ils sont maintenant recalculables en huit secondes par
n'importe qui. Un nombre comparable mais incontrôlable vaut moins qu'un
nombre contrôlable mais isolé.

**Mais il fallait l'écrire.** Deux conséquences pratiques :

1. **Toute comparaison future avec un autre projet devra passer par les
   ratios d'origine**, pas par les nôtres — et donc les recalculer, ou
   comparer des dimensions absolues plutôt que des proportions.
2. Le jour où un écart nous surprendra face à un projet tiers, il faudra
   **se souvenir que la base a changé** avant de chercher une erreur.

Cette réserve est au même rang que les deux autres : elle ne s'efface pas
par le fait que le choix soit bon.
