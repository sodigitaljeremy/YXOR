# 0041 — Porter l'incertitude d'une mesure

Date : 2026-09-29
Espèce : proposition
État : proposée
Statut : **proposée** — instruction. Une seule chose est appliquée : le
fichier `params/mesures.yaml` et ses trois premières entrées. Rien n'est
répandu ailleurs.

## Le problème, posé par la première mesure du projet

Balance au gramme. **4 g veut dire 3,5 à 4,5.** Soit ±12,5 % sur la masse
surfacique **et** sur la densité qui en dérive.

Or `hardware.yaml` porte aujourd'hui :

```yaml
masse_surfacique: 0.6349   # mg/mm²
densite: 0.1814            # mg/mm³
```

**Quatre décimales sur une mesure à ±12,5 %.** Le fichier affirme une
précision au dix-millième là où il n'y a qu'un chiffre significatif et
demi. **Une valeur sans incertitude se lit comme exacte** — Jeremy a
raison, et c'est exactement ce que le projet reproche partout ailleurs à
un vert obtenu pour une mauvaise raison.

## Ce que je ne propose PAS

**Pas un champ `incertitude` à côté de chaque valeur.** Trois raisons :

1. Sur 1 431 valeurs, ce serait 1 431 occasions de ne pas le remplir, et
   la règle 3 de `CLAUDE.md` vient d'être écrite contre cela : *ce qui
   peut se calculer se calcule*.
2. La plupart des valeurs n'ont pas d'incertitude qui ait un sens — un
   ratio de projet, un identifiant, une référence de norme.
3. **Et surtout** : une incertitude déclarée sur une valeur DÉRIVÉE
   pourrait diverger de celles dont elle dérive. `densite` vient de
   `masse_surfacique / epaisseur_mesuree` : son incertitude **doit être
   calculée**, jamais écrite.

## Ce que je propose

### Un fichier `params/mesures.yaml`, et rien d'autre

Il décrit les **actes de mesure**, pas les valeurs. Une entrée par
grandeur **directement mesurée** — jamais pour une grandeur dérivée.

```yaml
mesures:
  semelle_masse_2026_09_29:
    grandeur: "masse de la semelle d'apprentissage coupée"
    valeur: 4.0
    unite: g
    incertitude: 0.5          # demi-graduation : la balance affiche au gramme
    type_incertitude: resolution
    instrument: "balance de cuisine, affichage au gramme"
    n: 1
    date: 2026-09-29
    alimente: [matieres.carton_ondule_simple.masse_surfacique]
```

Cinq champs portent le sens :

| Champ | Pourquoi il est obligatoire |
| --- | --- |
| `incertitude` | sans elle, la valeur se lit comme exacte |
| `type_incertitude` | `resolution` (le pas de l'instrument) ou `dispersion` (l'écart-type de n relevés) — ce ne sont pas la même chose et on ne les combine pas pareil |
| `instrument` | une incertitude sans son moyen n'est pas reproductible |
| `n` | un relevé unique n'a pas d'écart-type ; le dire évite d'en inventer un |
| `alimente` | le chemin des valeurs qui en dépendent, pour que la propagation soit vérifiable |

### L'incertitude des valeurs dérivées se CALCULE

Pour un produit ou un quotient, les incertitudes **relatives**
s'additionnent en quadrature :

```
densite = masse_surfacique / epaisseur
σ_rel(densite) = √( σ_rel(masse_surfacique)² + σ_rel(epaisseur)² )
```

Appliqué aux mesures du 2026-09-29 :

| | valeur | σ relatif |
| --- | ---: | ---: |
| masse | 4,0 g ± 0,5 | **12,5 %** |
| aire | 6 300,49 mm² | ~0 % — calculée, pas mesurée |
| épaisseur | 3,5 mm ± 0,5 | **14,3 %** |
| **masse surfacique** | 0,635 mg/mm² | **12,5 %** |
| **densité** | 0,181 mg/mm³ | **19,0 %** |

**La densité est plus incertaine que la masse surfacique**, et c'est le
genre de chose qu'aucune déclaration à la main n'aurait vu : elle hérite
de deux incertitudes, pas d'une. Une valeur écrite « ±12,5 % » par
recopie aurait été fausse.

⚠ **L'incertitude sur l'épaisseur est une hypothèse de ma part** :
« à la règle » ne dit pas la graduation. Si la règle est au millimètre et
la lecture au demi-millimètre, ±0,5 mm est raisonnable ; si Jeremy a
relevé plusieurs endroits et moyenné, c'est peut-être moins. **À
confirmer avant d'inscrire.**

### Le nombre de décimales doit suivre

`0.6349 mg/mm²` à ±12,5 % est malhonnête. La convention usuelle : **on
garde un chiffre significatif sur l'incertitude, et on arrête la valeur
au même rang.**

    masse surfacique   0,63 ± 0,08 mg/mm²
    densité            0,18 ± 0,03 mg/mm³

**Je n'ai pas tronqué les valeurs dans `hardware.yaml`**, parce que cela
touche la donnée elle-même et que c'est votre décision. Mais le fichier
ment tant qu'elles sont à quatre décimales.

## Ce qui reste à trancher

1. **Tronquer les valeurs au rang de l'incertitude ?** Je le recommande —
   c'est la seule façon qu'un lecteur pressé ne se trompe pas. Mais on
   perd la valeur brute, sauf à la garder dans `mesures.yaml`.
2. **Un contrôle qui refuse une valeur `mesure` sans entrée dans
   `mesures.yaml` ?** Ce serait cohérent avec le reste du projet, mais il
   faudrait d'abord inscrire les mesures déjà faites — et il y en a peu.
3. **L'incertitude doit-elle apparaître sur le site ?** La fiche atelier
   dit « épaisseur 3,5 mm ». Devrait-elle dire « 3,5 ± 0,5 » ? Pour
   couper, non. Pour dimensionner un assemblage, oui.

## Ce qui est appliqué aujourd'hui

`params/mesures.yaml` existe avec les **trois** mesures du 2026-09-29, et
rien de plus. Les valeurs de `hardware.yaml` portent un renvoi en
commentaire. **Aucune autre valeur du dépôt n'a été touchée.**
