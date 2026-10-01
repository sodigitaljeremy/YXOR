# 0042 — Le rayon minimal : ce que la matière supporte, ou ce que le geste permet ?

Date : 2026-09-29
Espèce : close
État : archivée
Statut : **close** le 2026-09-30 par Jeremy, **sans rien trancher**. La question du rayon est propre à chaque procédé ; elle sera reposée avec le procédé réel.
Amende : `0015-architecture-plaques-entretoises.md`, dont la contrainte
de rayon est reprise sans distinction.

## L'observation

R 2,5 mm coupé sur 3,5 mm d'épaisseur, à la main, au cutter. La règle du
projet — `rayon_interieur_min = 0,5 × epaisseur` — donnait **1,75 mm**.

Jeremy était donc **43 % au-dessus du minimum**, et c'était **déjà
difficile**. Les angles ont demandé deux passes au lieu d'une.

**La règle n'a pas été violée. Elle n'a simplement pas décrit ce qui
allait se passer.**

## Ce que la règle dit réellement

`0,5 × epaisseur` répond à la question : *en dessous de quel rayon la
matière se déchire-t-elle ?* C'est une propriété du **matériau et de son
épaisseur** — un angle rentrant trop serré concentre l'effort sur une
longueur trop courte, et le carton cède avant de plier.

Elle ne répond pas à : *en dessous de quel rayon la main ne sait-elle
plus suivre le trait ?*

Ce sont **deux contraintes différentes, qui portent sur des choses
différentes, et dont le maximum s'impose** :

```
rayon retenu = max( rayon_matiere , rayon_geste )
```

Aujourd'hui le projet n'en connaît qu'une, et prend le résultat pour le
minimum réel.

## Pourquoi c'est le même défaut que celui du verdict

La fiche 0037 a corrigé un verdict calculé **par réglage** alors qu'il
dépendait de **la pièce**. Ici, un rayon est calculé **par matière**
alors qu'il dépend aussi **de la machine**.

Dans les deux cas, une grandeur a été attachée à la première entité qui
semblait la porter, sans se demander si une autre y contribuait. Et dans
les deux cas, ce n'est pas une erreur de calcul : **c'est une erreur de
localisation**.

La structure à quatre tables (fiche 0026) la rend d'ailleurs évidente :

| Contrainte | Où elle appartient |
| --- | --- |
| rayon que la **matière** supporte | `matieres` — fonction de l'épaisseur |
| rayon que le **geste** permet | `machines` — propriété de l'appareil |
| rayon retenu | `reglages` — le maximum des deux, **calculé** |

La table `machines` existe depuis la migration et ne porte aujourd'hui
que `nom`, `lieu` et `pilotage`. **C'est là que manque quelque chose.**

## Les trois formes possibles, et ce qu'elles coûtent

### A. Un rayon fixe par machine

```yaml
machines:
  cutter_main:
    rayon_min_geste: 3.0     # mm — à mesurer
```

**Pour** : simple, et se calcule immédiatement en `max()`.
**Contre** : un cutter suit-il le même rayon dans du carton de 1,5 mm et
de 5 mm ? Probablement pas — c'est l'effort de coupe qui fait dévier la
lame, et il croît avec l'épaisseur.

### B. Un rayon par couple machine × matière

Dans `reglages`, à côté de `saignee`. Physiquement plus juste, mais
**c'est une mesure de plus par réglage**, et le projet en a déjà cinq en
attente. On paierait la justesse en valeurs jamais relevées.

### C. Ne rien ajouter, et consigner l'écart

Garder `0,5 × epaisseur` comme **minimum de matière**, et noter que le
geste impose davantage — sans chiffrer, jusqu'à ce qu'il y ait de quoi
chiffrer.

**Pour** : honnête, et coûte zéro donnée inventée.
**Contre** : ne protège de rien. La prochaine pièce dessinée avec un
congé à 1,75 mm sera aussi difficile à couper, et rien ne l'aura dit.

## Ce que je recommanderais, si l'on me demandait

**A, avec la valeur à `null`.**

Le champ existe, il est visible dans « À mesurer » de `/etat/`, et son
absence est déclarée plutôt que supposée — c'est exactement ce que la
fiche 0020 permet. On ne chiffre rien tant qu'on n'a pas mesuré, et le
jour où l'on mesure, le `max()` se met à protéger.

Et une donnée existe déjà pour l'amorcer : **R 2,5 mm a été suivi, avec
difficulté, à deux passes.** Ce n'est pas encore une mesure — c'est une
borne inférieure qualitative. Une vraie mesure demanderait de couper une
série de congés décroissants et de noter où le trait cesse d'être
suivi.

## Ce que je ne tranche pas, et pourquoi

Trois questions m'échappent, et deux d'entre elles sont les vôtres :

1. **Le rayon de geste dépend-il de l'épaisseur ?** Je le crois, je ne
   l'ai pas mesuré, et le croire ne suffit pas.
2. **Faut-il en faire une mesure de plus** dans un projet qui en a déjà
   cinq en attente, dont aucune n'est urgente ?
3. **La règle `0,5 × epaisseur` est-elle elle-même sourcée ?** Elle est
   dans `CLAUDE.md` depuis le premier jour. **Je n'ai trouvé aucune fiche
   qui l'établisse.** Elle a l'autorité d'une règle et la provenance
   d'une convention — et c'est peut-être le vrai sujet de cette fiche.

## Une remarque sur la méthode

Cette question n'est venue d'aucun audit, d'aucune source, d'aucun
contrôle. **Elle est venue d'une main qui a trouvé la coupe difficile.**

Le dépôt a passé dix jours à se donner des garde-fous pour ce qu'il
pouvait calculer. Le premier objet coupé a produit, en une heure, une
prédiction vérifiée, un contour faux depuis trois jours, et une règle
dont on découvre qu'elle ne décrit que la moitié du problème.

## Clôture — 2026-09-30

**Décision de Jeremy : close. Rien n'est tranché pour le carton.**

Le carton a rempli son rôle, qui était de valider la chaîne. Sa
caractérisation est arrêtée : ses valeurs ne se transfèrent pas au robot
réel, fait de pièces imprimées, usinées ou découpées en métal.

**La question du rayon est propre à chaque procédé.** Elle sera reposée
avec le procédé réel :

- en usinage, c'est le **rayon d'outil** ;
- en découpe métal, ce sont les limites de **la machine de Loïc**.

Le champ `rayon_min_geste` n'est pas créé. La question 3 — d'où vient
`0,5 × épaisseur` — reste ouverte, et elle se reposera au même moment.

Cette fiche amendait la 0015. Le renvoi reste dans l'en-tête de la 0015 :
le constat « la règle décrit la matière, pas le geste » demeure vrai,
même s'il n'a rien produit pour le carton.
