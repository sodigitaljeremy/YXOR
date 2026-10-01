# 0040 — Un registre des sources, pas un index de recherche

Date : 2026-09-29
Espèce : gouvernante
État : appliquée
Statut : **acceptée** le 2026-09-29, sur décision de Jeremy — appliquée
le jour même.

## Ce qui est écarté, et pourquoi

Pas d'index vectoriel, pas d'embeddings, pas de base de données.

**L'argument est expérimental, pas théorique.** Le chapitre 5 de la thèse
de Forget a été lu **en entier**. C'est cette lecture continue qui a
permis de corriger une distinction : le texte décrit **trois** régions de
fonctionnement, alors que la figure porte **quatre** étiquettes — les deux
surnuméraires désignant des *modes d'exploitation*, ce qui ne se voit que
dans le paragraphe suivant.

**Un découpage en fragments aurait détruit cette distinction.** Il aurait
rendu la figure et sa légende sans le paragraphe qui les interprète, et
la correction n'aurait jamais eu lieu.

Deux autres raisons, plus simples :

- **huit documents ne sont pas un problème de recherche.** `grep` sur
  huit PDF est instantané ; l'infrastructure coûterait plus que le
  problème ;
- **un fragment sémantique ne cite pas une page**, et ne dit pas ce qu'il
  a omis. Or une fiche qui affirme doit pouvoir écrire « p. 97 ».

## Deux fichiers, et pourquoi deux

**`params/sources.yaml` — VERSIONNÉ.** L'identité stable : identifiant
court, auteurs, titre, éditeur, année, identifiant pérenne (HAL, DOI,
ISBN), empreinte sha256, taille, conditions de droits, **et l'état de
lecture**.

**`sources.local.yaml` — IGNORÉ PAR GIT.** Uniquement les chemins. Un
chemin est propre à une machine : le versionner ferait voyager
l'arborescence personnelle de quelqu'un et casserait le registre partout
ailleurs.

## Pourquoi `fournisseurs.yaml` reste distinct

Les deux registres se ressemblent, et il serait tentant de les fondre.
Ils répondent à deux questions différentes :

| | Question posée | Exemple |
| --- | --- | --- |
| `fournisseurs.yaml` | cette VALEUR a-t-elle le droit d'être ici, et de quel exemplaire vient-elle ? | CSV ANSUR II, modèle CAO de vis |
| `sources.yaml` | qu'avons-nous LU, jusqu'où, et qu'a-t-on le droit d'en citer ? | une thèse, un ouvrage |

Les fondre obligerait à répondre « sans objet » à la moitié des champs de
chaque entrée : un ouvrage n'alimente aucune cote, un CSV ne se lit pas
par pages.

**Et surtout : `sources.yaml` porte un ÉTAT DE LECTURE**, qui n'a aucun
sens pour un fichier consommé par un script. C'est ce champ qui justifie
le fichier à lui seul.

Quatre documents ont donc migré de l'un vers l'autre. Les deux CSV ANSUR
restent dans `fournisseurs.yaml` : on ne les lit pas, on les calcule.

## L'état de lecture : un `non_lu` est une information

Trois valeurs — `lu`, `partiel`, `non_lu` — et le champ `lu` dit **quelles
pages**.

Un `non_lu` n'est pas un oubli à combler : c'est une affirmation.
**Aucune assertion du dépôt ne peut se réclamer d'une source non lue.**
C'est la règle déjà pratiquée pour la DIN 8580 (fiche 0026) et ISO 4762
(0028), portée dans la donnée au lieu de reposer sur la mémoire de qui
écrit la fiche.

Au 2026-09-29 : **2 partiels, 6 non lus**. Aucun lu en entier.

## L'empreinte est vérifiée AVANT toute lecture

Une citation « p. 97 » ne vaut que pour l'exemplaire lu. Deux tirages
n'ont pas la même pagination, un PDF recompressé non plus.

Ce n'est pas un risque théorique : le dossier des exemplaires contient un
sous-dossier `pdf24_compressed` avec **les mêmes titres et d'autres
empreintes**. Vérifié en y pointant le registre : `source.py` refuse, et
affiche les deux empreintes.

**Il refuse, il n'avertit pas.** Un avertissement se survole, et la
citation partirait dans une fiche.

## La règle de confidentialité

> Les exemplaires vivent dans un dossier qui contient aussi des documents
> personnels sans rapport avec le projet — bulletins de paie, courriers,
> documents médicaux.
>
> **On n'explore jamais ce dossier.** On ouvre les chemins nommés dans
> `sources.local.yaml`, un par un, et rien d'autre. Pas de `find`, pas de
> `ls`, pas de parcours « pour voir ».

`source.py` applique la règle par construction : il **n'accepte aucun
chemin en argument**, ne liste rien et ne cherche aucun fichier. Il ne
sait ouvrir que ce que le registre nomme.

Le registre existe précisément pour rendre toute exploration inutile.

## La huitième et la neuvième

Huit sources sont enregistrées. **Jeremy en annonçait neuf** — dont deux
que je n'avais pas trouvées au premier passage.

J'en ai retrouvé une : *Introduction to Autonomous Mobile Robots*
(Siegwart & Nourbakhsh, MIT Press), qui portait un nom de fichier sans
« humanoid ».

**La neuvième n'est pas identifiée**, et je préfère l'écrire que
d'inventer une entrée. Elle s'ajoutera quand elle sera nommée.

## Ce que l'outil ne fait pas

- **Aucun réseau.** Il ne télécharge rien, ne résout aucun DOI.
- **Aucune dépendance nouvelle** : `pypdf` était déjà installé — mais
  **absent de `requirements.txt`**, ce qui est exactement le piège relevé
  pour `bd_warehouse`. Il y est désormais inscrit, avec la mention qu'il
  ne sert pas à la régénération.
- **Pas de `pdftotext`** : il n'est pas installé sur cette machine.
  `pypdf` donne la page directement, ce qui supprime au passage le
  comptage des séparateurs `\f` et son risque de décalage.
