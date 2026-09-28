# 0011 — Cinquième origine `litterature`, et filiation de H

Date : 2026-09-28
Statut : acceptée
Amende : `0010-origine-des-cotes.md`, `0005-topologie-bras-p1.md`

> **Note de procédure.** La règle 5 interdit de réécrire une fiche après
> coup. Les fiches 0010 et 0005 ne sont donc **pas modifiées** : elles
> reçoivent un renvoi vers celle-ci, et c'est ici que les décisions
> nouvelles sont écrites. Un pointeur en avant n'est pas une réécriture.

## 1 — Cinquième origine : `litterature`

La fiche 0010 §3 signalait deux lacunes de la taxonomie sans les
trancher. Elles n'en formaient qu'une :

> **`litterature` — savoir public que personne ne possède.**
> Publication scientifique ou norme.

| | |
| --- | --- |
| Exige | une citation permettant de retrouver la source |
| Risque de licence amont | **aucun** |
| Remplace | `ambigu` pour les ratios biomécaniques et les cotes normalisées |

Deux familles y passent :

- **Ratios anthropométriques** — `ratios.*` et `masses.*` de
  `anthropometry.yaml`, d'après Drillis & Contini. Antérieurs de
  plusieurs décennies à ToddlerBot.
- **Cotes normalisées** — diamètres, trous de passage et diamètres de
  tête des vis métriques. Une vis M3 fait 3,0 mm parce que l'ISO le dit,
  pas parce qu'un constructeur l'a décidé.

Ce qui distingue `litterature` de `catalogue` : un catalogue engage un
**fabricant** et une référence commerciale ; la littérature et les normes
n'appartiennent à personne. La distinction n'a pas d'effet juridique
identifié — elle sert à savoir **où revérifier** une valeur.

Restent `ambigu` : `tolerances.**` et `epaisseurs.*`, que le fichier
lui-même dit provisoires (« à ajuster après essai »). Elles deviendront
`mesure`.

## 2 — Filiation de H, consignée comme un fait

La fiche 0010 §4 l'établissait. Elle est reprise ici pour être
inattaquable, et parce que la fiche 0005 traite du statut temporaire de
l'emprunt sans en avoir tiré cette conséquence.

**Les trois faits :**

1. **`H = 0,56 m` est d'origine `amont`.** C'est la taille hors-tout
   publiée de ToddlerBot. Fiche 0001, ligne 24 : « ToddlerBot
   (Stanford). **0,56 m**, 3,4 kg, 30 DDL actifs » ; ligne 36 : « Le
   palier P1 est fixé à H = 0,56 m par cette décision. »

2. **Toute la chaîne `propre` en dérive au palier P1.** Une cote dite
   propre est, par définition, `H × ratio`. Au palier P1, elle est donc
   une fraction d'un nombre venu de ToddlerBot. Le ratio, lui, est
   `litterature` et ne pose pas de question ; c'est **le facteur
   d'échelle** qui est emprunté.

3. **Passer en P2 rompt cette filiation.** `paliers.P2 = 0,90` et
   `paliers.P3 = 1,70` sont des choix de projet. Une cote dérivée de
   P2 n'a plus aucun ancêtre amont.

> **Ce sont des faits, pas une conclusion.** Savoir si une taille
> hors-tout relève de la licence CC BY-NC-SA des fichiers mécaniques
> amont **n'est pas tranché ici**, ni par cette fiche ni par aucune
> autre. La traçabilité produit l'inventaire ; l'avis appartient à
> Jeremy et à son conseil.

### Conséquence opératoire, sans portée juridique

Une pièce que l'on veut aussi propre que possible **au sens strict** se
dessine au palier **P2**, pas P1. Le fait est noté ici pour que le choix
soit posé quand il se présentera, pièce par pièce.

## 3 — Lien manquant entre les fiches 0005 et 0010

La fiche 0005 acte que la topologie ToddlerBot est adoptée **en P1** et
« réévaluable en P2 ». Elle raisonnait sur la nomenclature articulaire.

La fiche 0010 montre que **le même palier P1 porte aussi la filiation
dimensionnelle**, par H.

Les deux emprunts — topologique et dimensionnel — sont donc adossés au
même palier et se dénoueraient au même moment. Ce n'était écrit nulle
part ; ça l'est maintenant.

## Conséquences

- `params/origines.yaml` requalifie les familles concernées ; l'audit
  compte désormais six valeurs.
- Une cote `litterature` sans citation exploitable est un défaut, au
  même titre qu'un `catalogue` sans référence.
- **Question ouverte, non tranchée ici : comment l'origine se propage
  dans un calcul.** Si une cote `propre` se calcule à partir d'une valeur
  `amont` (H) et d'une valeur `litterature` (un ratio), quelle origine
  porte le résultat ? Le contrat d'accesseur de la fiche 0010 §5 ne le
  dit pas. À trancher avant la première pièce qui combine des origines.
