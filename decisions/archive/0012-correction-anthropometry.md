# 0012 — Correction de `anthropometry.yaml` : sources rétablies

Date : 2026-09-28
Espèce : historique
État : appliquée
Statut : acceptée

## Contexte

L'audit du 2026-09-28 a confronté `params/anthropometry.yaml` à sa source
annoncée. Trois défauts en sont sortis.

**L'attribution du fichier est fausse.** Il annonce « les ratios sont ceux
de Drillis & Contini » pour l'ensemble. C'est vrai des **longueurs**
(Winter écrit que sa figure 4.1 « was prepared by Drillis and Contini,
1966 ») et **faux des masses** : le tableau 4.1 de Winter porte sur
chaque valeur le code `M`, qui renvoie à **Dempster**, via Miller &
Nelson.

**Une valeur ment sur ce qu'elle désigne.** `masses.tete: 0.081` est
numériquement exacte, mais la ligne de Winter est *« Head and neck »* :
tête **et** cou.

**Deux valeurs sont des arrondis** et deux autres des dérivations non
publiées. Les mains manquent.

Dans un projet dont la règle est de ne rien inventer, c'est une faute de
méthode et non un détail.

## Décision

### 1. La source descend au niveau de la ligne

Le fichier ne porte plus une attribution globale. **Chaque valeur porte
sa source.** Deux familles y coexistent, et rien n'oblige deux tables
d'auteurs différents à se recouvrir :

| Famille | Source | Référence |
| --- | --- | --- |
| `ratios.*` — longueurs | **Drillis & Contini (1966)** | via Winter, figure 4.1 |
| `masses.*` — fractions de masse | **Dempster (1955)** | via Winter, tableau 4.1, code `M` (Miller & Nelson) |

### 2. `masses.tete` devient `masses.tete_et_cou`

**Renommée, pas retirée.** Motif : la valeur 0,081 est juste, c'est son
*nom* qui était faux. La retirer perdrait une donnée sourcée ; la
scinder en tête et cou exigerait d'inventer un partage que **Dempster ne
donne pas**.

**Cela ne casse pas la cohérence avec `cou_hauteur`.** Les deux
appartiennent à des familles distinctes : `cou_hauteur` est un ratio de
**longueur**, `tete_et_cou` une fraction de **masse**. Aucune relation
arithmétique ne les lie, donc rien ne se contredit. Le fichier le dit
explicitement, pour qu'un lecteur ne cherche pas une correspondance qui
n'existe pas.

### 3. Valeurs exactes de Winter à la place des arrondis

| Clé | Avant | Après | Écart corrigé |
| --- | --- | --- | --- |
| `masses.tibia` | 0.047 | **0.0465** | 1,1 % |
| `masses.pied` | 0.014 | **0.0145** | 3,4 % |

### 4. `masses.main: 0.006` ajoutée

Absente, alors que `ratios.main_longueur` existait. Son absence était
mesurable : l'ancienne série sommait à **0,988**, soit exactement deux
mains de moins.

**Contrôle de cohérence, désormais vérifiable :**

```
2 × (main + avant_bras + bras + pied + tibia + cuisse)
  + tronc + tete_et_cou  =  1,000000
```

Exact, sans résidu. Le fichier porte ce contrôle en commentaire pour
qu'une modification future qui le romprait soit détectable.

### 5. `tronc_hauteur` et `cou_hauteur` sont marquées dérivées

Ce ne sont **pas des ratios publiés**. Elles s'obtiennent par
soustraction dans la figure 4.1 :

- `tronc_hauteur = 0,818 (épaule) − 0,530 (hanche) = 0,288`
- `cou_hauteur = 1 − 0,130 (tête) − 0,818 (épaule) = 0,052`

Cohérentes avec la figure, mais **personne ne les a jamais mesurées sous
cette forme**. La mention est portée sur chaque ligne.

### 6. Mention franche de l'origine du fichier

Le fichier portera, en clair :

> Ces valeurs ont d'abord été **écrites de mémoire par un modèle de
> langage** le 2026-09-20, sans confrontation à la source. Elles ont été
> vérifiées le 2026-09-28 contre Winter, chapitre 4.

C'est une information utile à quiconque lira ce fichier plus tard, et
elle explique pourquoi certaines valeurs étaient arrondies et
l'attribution fausse.

## Ce qui reste non vérifié, et doit le rester visiblement

**Les quatorze ratios de longueur n'ont pas pu être confrontés à leurs
valeurs publiées.** La figure 4.1 est un **graphique** : aucun des
nombres n'apparaît dans le texte du PDF. La source primaire — Drillis &
Contini (1966), Office of Vocational Rehabilitation — n'est pas
accessible en ligne.

Chaque ratio de longueur porte donc `verifie: non`. L'attribution est
établie ; les valeurs ne le sont pas. Ne pas confondre les deux.

## Conséquences

- Les valeurs de masse changent : toute inertie déjà calculée à partir
  de `tibia`, `pied` ou `tete` est à refaire. Aucune ne l'a été.
- `masses.tete_et_cou` étant un renommage, tout code la référençant par
  `masses.tete` cassera — franchement, et c'est voulu.
- L'inventaire d'origine (fiche 0010) est inchangé : ces valeurs restent
  `litterature`, et le sont désormais avec une citation exploitable.
