# 0037 — Le verdict se calcule par PIÈCE, pas par réglage

Date : 2026-09-29
Espèce : close
État : appliquée
Statut : **appliquée** le 2026-09-29 — `besoins_procede` déduit de l'usage, plus le canal `c.besoin()` pour ce qui n'est pas lu au dessin. La semelle est coupable.
Amende : `0019-interface-catalogue.md`, où le verdict a été introduit.

## Le défaut, tel qu'il se voit aujourd'hui

La fiche atelier de la semelle affiche :

> **NE PAS COUPER ENCORE.** Le dessin est juste, mais il manque :
> saignée, voile min.

**C'est faux pour cette pièce.** Et ce n'est pas une nuance : c'est la
seule chose qui la sépare d'exister physiquement.

- La **saignée** est la largeur de matière emportée par l'outil. Elle
  compte quand **deux pièces doivent s'emboîter** : si l'on coupe sur le
  trait, la languette est trop mince de la moitié de la saignée, le
  logement trop large d'autant, et l'assemblage a du jeu.
- Le **voile minimal** est la largeur en dessous de laquelle une bande de
  matière se déchire au lieu de tenir.

La semelle d'apprentissage **ne s'interface avec rien** — c'est écrit
dans son propre rôle. Elle n'a ni languette, ni logement, ni perçage. Sa
largeur la plus faible est de 36,36 mm au creux.

**Aucune des deux valeurs manquantes ne change quoi que ce soit à cette
pièce.**

Et le plus gênant : **couper cette pièce donnerait précisément la mesure
de saignée qui manque.** Le verdict interdit l'acte qui le lèverait.

## Pourquoi c'est arrivé

Le verdict est calculé par `etat_procede(reglage)` : il regarde les
valeurs du **réglage**, jamais ce que la pièce en fait. Un réglage
incomplet rend donc *toutes* les pièces non coupables, y compris celles
qui n'emploient pas les valeurs absentes.

Posé en une soirée, sans pièce réelle pour le mettre à l'épreuve.

**C'est la première règle du projet qui se révèle trop STRICTE.** Toutes
les autres ont péché par laxisme — un binaire commité, une règle sans
référent, un contrôle absent. On découvre l'excès de zèle plus tard que
le laxisme, parce qu'il ne casse rien : il refuse, et on croit qu'il a
raison.

## Le champ qui déclare qu'une pièce s'interface

La pièce sait déjà ce qu'elle contient — elle construit sa géométrie.
Proposé : elle **déclare ce dont elle a besoin**, plutôt qu'un booléen.

```yaml
piece:
  besoins_procede: []          # la semelle : aucun
```

```yaml
piece:
  besoins_procede: [saignee, voile_min]   # une pièce à emboîtement
```

**Une liste, pas un `s_interface: true/false`.** Trois raisons :

1. Une pièce peut avoir besoin de la saignée sans avoir de voile étroit —
   un emboîtement large. Un booléen les confondrait.
2. La liste se **vérifie** : si une pièce déclare `[]` mais produit une
   forme dont la largeur minimale descend sous un seuil, le contrôle
   peut le dire. Un booléen ne se vérifie pas.
3. Elle nomme **ce qui manquerait**, donc le verdict peut l'écrire.

### Qui la remplit

**La pièce, au moment où elle emploie la cote.** L'accesseur `Cotes`
existe déjà et note chaque lecture : `c.reglage(rid, "saignee")` peut
inscrire `saignee` dans les besoins **automatiquement**.

C'est décisif : un champ rempli à la main diverge. **Un besoin déduit de
l'usage réel ne peut pas mentir** — si la pièce lit la saignée, elle en a
besoin ; si elle ne la lit pas, elle n'en a pas besoin.

Le seul cas non couvert : une pièce qui devrait lire la saignée et ne le
fait pas. C'est une faute de conception, et aucun champ ne l'attrape —
mais le contrôle de largeur minimale du point 2 en attrape une partie.

## Ce que devient le verdict

```
dessinable  = toutes les cotes lues pour la GÉOMÉTRIE sont présentes
coupable    = dessinable ET toutes les cotes de `besoins_procede`
              sont présentes dans le réglage
```

Pour la semelle : `besoins_procede: []`, donc **coupable dès que
dessinable**. Verdict : **« Prêt à couper. »**

### Trois états d'affichage, pas deux

Le verdict ne doit pas devenir muet pour autant :

| Cas | Ce que la fiche atelier dit |
| --- | --- |
| pièce sans besoin, réglage incomplet | **Prêt à couper.** Cette pièce ne s'emboîte avec rien : la saignée du procédé ne l'affecte pas. |
| pièce avec besoin, réglage incomplet | **NE PAS COUPER ENCORE** — il manque : … |
| réglage complet | **Prêt à couper.** |

Le premier cas doit **dire pourquoi il est prêt malgré un réglage
incomplet**, sinon on croira à une régression du contrôle.

## Ce que cela ne doit pas devenir

**Une échappatoire.** La tentation serait qu'une pièce déclare `[]` pour
passer le contrôle. Deux garde-fous :

1. Les besoins sont **déduits de l'usage**, pas déclarés.
2. Un contrôle de **largeur minimale** : une pièce qui déclare ne pas
   avoir besoin du voile minimal et dont la largeur locale descend sous,
   disons, 3 mm, est suspecte. La valeur du seuil reste à établir — elle
   dépend du matériau, donc du réglage.

Le second n'est pas trivial : il demande d'analyser le contour. Je ne le
propose pas pour tout de suite ; je propose qu'il soit **écrit comme
manquant**, pour qu'on ne croie pas le garde-fou complet.

## Ce que cela débloque, et quand

Appliqué, ce changement rend la semelle **coupable aujourd'hui**, sans
mesurer quoi que ce soit.

Et la couper produira la saignée qui manque. **La mesure suivra l'objet,
et non l'inverse** — ce qui est l'ordre naturel, et celui que le verdict
actuel a inversé.
