# 0045 — Aucune géométrie amont ne passe dans un outil de reconstruction

Date : 2026-09-30
Espèce : gouvernante
État : acceptée
Statut : **acceptée** — règle posée par Jeremy, écrite **avant** tout test d'outil de reconstruction (fiche 0046). Non outillée, et dite comme telle.
Découle de : `0010-origine-des-cotes.md`, `0029-familles-de-licences.md`

## La règle

> **Aucune géométrie d'origine `amont` ne passe dans un outil de
> reconstruction pour en tirer une pièce, une esquisse ou une cote YXOR.**
>
> Un **outil de reconstruction** est tout procédé automatisé qui
> produit une géométrie à partir d'une autre représentation. Cela
> couvre :
>
> - le scan vers la CAO ;
> - le maillage vers la CAO (STL, OBJ, PLY) ;
> - le plan vers la CAO, qu'il s'agisse d'un dessin technique ou d'une
>   image ;
> - la photo vers la CAO ou vers un maillage ;
> - tout générateur 3D par IA.
>
> La règle vaut pour **tous** ces outils, et pas pour un produit en
> particulier.
>
> Une **géométrie amont** est tout ce qui représente la mécanique de
> ToddlerBot, sous n'importe quelle forme :
>
> - les maillages du dépôt amont ;
> - le document Onshape et ses exports ;
> - les rendus, captures et vidéos, y compris ceux produits par
>   `sim/upstream/` ;
> - les photos d'un ToddlerBot physique ;
> - les plans et les mesures prises sur l'un de ces supports.

## Pourquoi

**Une reconstruction ne transforme pas une œuvre dérivée en conception
originale. Elle produit une dérivation mieux documentée.**

La fiche 0010 existe pour pouvoir dire, cote par cote, ce qui vient de
l'amont. Un outil de reconstruction ferait l'inverse. Il prendrait une
géométrie `amont` et rendrait un arbre de features propre, avec des
esquisses et des cotes nommées, qui a **l'apparence** d'un travail
original. La provenance serait perdue au moment précis où elle
compterait le plus. Dans le pire des cas, l'audit la classerait
`propre`.

La mécanique amont est sous **CC BY-NC-SA**. C'est ce qu'écrit
`~/upstream/toddlerbot/README.md:167`, vérifié le 2026-09-29. Les deux
clauses pèsent :

- **NC** interdit l'exploitation commerciale du dérivé ;
- **SA** impose la même licence au dérivé.

Une reconstruction ne se soustrait à aucune des deux. Ce n'est pas un
avis juridique (fiche 0010 §4) : c'est le constat que l'outil ne change
pas la nature de ce qu'on lui donne.

Il y a une seconde raison, indépendante de la première. **Téléverser**
une géométrie amont dans un service tiers, c'est déjà la transmettre.
Les conditions de Backflip du 2026-08-04 accordent par défaut au
service une licence d'entraînement sur les contenus, et le droit de
partager les résultats avec d'autres utilisateurs (fiche 0046 §1).
Elles exigent aussi que l'utilisateur ait « des droits suffisants » sur
ce qu'il envoie. Même sans pièce produite, l'envoi seul poserait
problème.

## Si cela arrive quand même

Une géométrie obtenue par reconstruction d'une source `amont` est
qualifiée **`amont`**, sans exception. Elle ne peut **jamais** être
qualifiée `propre`, `mesure` ni d'une éventuelle origine « reconstruction ».

C'est la seule partie de la question 4b de la fiche 0046 que cette
fiche tranche. Elle ne fait qu'appliquer la 0010 : l'origine suit la
source, pas l'outil.

## Ce que la règle n'interdit pas

- **Reconstruire une géométrie YXOR**, dont la vérité est connue. C'est
  le test de la semelle (fiche 0046).
- **Lire une valeur amont**, avec son origine, comme le fait déjà
  `import_upstream_limits.py`. C'est un extrait tracé, et non une
  reconstruction.
- **Reconstruire depuis un objet physique ou un plan que Jeremy a le
  droit d'utiliser.** Ce cas est instruit, sans être tranché, dans la
  fiche 0046 (question 4a).

## Vérifiabilité — non outillée

**Aucun contrôle du dépôt ne peut voir ce qui est envoyé à un service
extérieur.** La règle repose sur la conduite, comme la branche (c) de la
0027. Elle est déclarée non outillée plutôt que d'être entourée d'un
garde-fou qui n'en serait pas un.

Il existe une protection partielle, **possible mais non faite** :

1. Toute reconstruction inscrit dans son registre l'empreinte du
   fichier **envoyé**.
2. Un contrôle compare cette empreinte à celles des maillages de
   `~/upstream/toddlerbot/` au commit épinglé.

Ce contrôle attraperait un envoi direct d'un STL amont. Il ne verrait
ni une photo, ni un rendu, ni un fichier converti. **Il ne prouverait
donc pas que la règle est respectée**, et c'est écrit ici pour qu'on ne
le croie pas plus fort qu'il n'est.
