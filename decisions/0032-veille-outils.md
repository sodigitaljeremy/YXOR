# 0032 — Quatre pistes en veille : notées, pas adoptées

Date : 2026-09-29
Statut : **veille** — aucune n'est adoptée, aucune n'est écartée.

Quatre pistes reviennent dans les retours extérieurs. Jeremy ne les veut
**pas encore**. Les noter sans les adopter suppose d'écrire ce qui
déclencherait leur adoption : une veille sans critère de sortie est une
liste de regrets.

Chacune porte donc un **déclencheur** — un fait observable, pas une
impression — et un **coût d'entrée**.

## OrcaSlicer

**Ce que c'est.** Un trancheur, dérivé de Bambu Studio, qui en partage la
base de code et donc la ligne de commande.

**Déclencheur.** *Une imprimante 3D est acquise ET une pièce du projet
doit être imprimée.* Pas avant : sans imprimante, un trancheur ne
tranche rien.

**Coût d'entrée.** Une dépendance lourde de plus dans l'étage
constructeur du Dockerfile, pour une chaîne qui aujourd'hui produit des
DXF. Et le doute de la fiche 0028 (a) sur la reproductibilité du G-code
vaut pour lui, puisqu'il partage la base de code incriminée.

**À vérifier le moment venu.** Si le défaut #11560 est propre à Bambu ou
présent dans le fork. La question est ouverte et personne ne l'a posée.

## FreeCAD MCP

**Ce que c'est.** Un pont permettant de piloter FreeCAD depuis un
assistant.

**Déclencheur.** *Une opération de CAO impossible à écrire en build123d
se présente deux fois.* Deux fois, pas une : une impasse isolée se
contourne, une impasse répétée est une limite d'outil.

**Coût d'entrée.** Élevé et mal visible. Piloter une application
interactive, c'est produire un état qui n'est **pas engendré depuis le
texte source** — le contraire du principe du dépôt. Et cela ouvrirait une
seconde chaîne de CAO, donc une seconde vérité géométrique, sans le
garde-fou que la fiche 0023 a dû construire pour la première.

**Réserve.** La fiche 0009 a retenu build123d précisément parce que la
géométrie s'écrit en texte versionnable. Adopter ceci reviendrait à
rouvrir cette décision, pas à ajouter un outil.

## Zoo (noyau de CAO en service distant)

**Déclencheur.** *Le noyau OCCT échoue sur une géométrie que le projet a
réellement besoin de produire.* Il n'a jamais échoué à ce jour.

**Coût d'entrée.** Un service distant dans la chaîne de régénération.
Aujourd'hui, `regenerer.py` tourne hors ligne et produit la même chose
partout. Une dépendance réseau rendrait la régénération **dépendante d'un
tiers vivant** — une reconstruction en 2030 supposerait que le service
existe encore.

**C'est le point qui pèse le plus**, avant même le prix ou la licence :
le dépôt promet que tout se régénère depuis le texte. Un service distant
ferait de cette promesse une hypothèse.

## 3MF dans la chaîne

**Ce que c'est.** Un format d'échange qui transporte géométrie, matériaux
et réglages dans une archive unique.

**Déclencheur.** *Une imprimante est acquise, ET l'on constate qu'un
STEP plus un fichier de réglages ne suffisent pas.*

**Coût d'entrée.** Faible techniquement — mais il ajoute un **format
binaire** de plus, alors que la règle 4 vient d'être généralisée à tout
le dépôt (fiche 0030). Il vivrait dans `exports/`, comme le STL. Rien
n'est cassé ; c'est simplement une pièce de plus dans une chaîne qui n'en
a pas besoin aujourd'hui.

**Une remarque.** Le 3MF est le format dans lequel le défaut #11560 se
constate — les deux sorties comparées sont des `.gcode.3mf`. Ce n'est pas
un reproche au format, c'est une coïncidence à ne pas mal lire.

## Ce que cette fiche établit

Aucune des quatre n'est écartée. Trois déclencheurs sur quatre dépendent
du même fait : **l'acquisition d'une imprimante 3D**. C'est cohérent avec
la fiche 0026 — l'impression est le groupe principal 1 de la DIN 8580,
quand toute l'architecture actuelle vit dans le groupe 3. Ces outils sont
l'outillage d'un groupe que le projet n'a pas encore ouvert.
