# 0035 — Une sixième origine : `norme`

Date : 2026-09-29
Espèce : proposition
État : proposée
Statut : **proposée** — instruction, rien n'est appliqué.

## Le cas qui la réclame

`bd_warehouse` produit une vis M3 aux dimensions d'**ISO 4762**
(fiche 0028). De quelle origine est le pas de 0,5 mm ?

- `catalogue` ? Non : ce n'est pas la fiche technique d'un constructeur.
  Aucun fabricant ne possède ce nombre ; ils s'y conforment tous.
- `litterature` ? Non plus : une publication **décrit** ce qu'elle a
  observé, et la vérité lui préexiste. Une norme ne décrit rien.

**Une norme PRESCRIT.** Un pas de 0,5 sur une M3 n'est pas une
observation qui pourrait se révéler fausse : c'est la **définition** de
« M3 ». Mesurer mille vis M3 et trouver 0,52 ne corrigerait pas la
norme — cela prouverait que les vis sont hors tolérance.

C'est une différence de **nature logique**, pas de provenance.

## Ce qui la distingue opérationnellement des cinq autres

Le critère qui tranche : **que fait-on si la mesure contredit la valeur ?**

| Origine | Si le réel diffère | Ce qu'on corrige |
| --- | --- | --- |
| `mesure` | c'est le réel qui a raison | la valeur |
| `catalogue` | le constructeur s'est trompé, ou le lot dévie | la valeur, après vérification |
| `litterature` | population différente, ou publication fausse | la valeur, ou la source |
| `amont` | l'amont a changé | la valeur, en resuivant l'amont |
| `propre` | on avait mal choisi | le choix |
| **`norme`** | **la PIÈCE est hors tolérance** | **la pièce, jamais la valeur** |

C'est la seule origine où **une mesure divergente disqualifie l'objet, et
non la cote**. Cela suffit à justifier une sixième entrée : les cinq
autres se corrigent, celle-ci ne se corrige pas.

Deux conséquences pratiques :

1. **Aucune cote `norme` ne doit jamais être « ajustée » d'après un
   relevé.** Un contrôle pourrait le vérifier : une clé qualifiée `norme`
   dont la valeur change entre deux commits est suspecte.
2. **Une cote `norme` n'a pas d'incertitude.** Elle a une **tolérance**,
   qui est une autre valeur et vient de la même norme.

## ANSUR II relève-t-il de `norme` ? Non — et d'aucune des cinq

Vous avez raison de poser la question, et la réponse est gênante.

ANSUR II n'est **ni** de la littérature — ce ne sont pas des conclusions
publiées, ce sont **6 068 lignes de mesures brutes** — **ni** une norme,
puisque rien n'est prescrit, **ni** une mesure au sens du projet, qui
désigne ce que *nous* relevons sur notre établi.

Ce qui le caractérise : **les données brutes sont publiques, et le
nombre est RECALCULABLE par quiconque**. `ratios_ansur.py` le refait en
huit secondes. Aucune des cinq origines ne porte cette propriété — et
c'est elle qui compte, parce qu'elle décide de ce qu'on peut vérifier.

Trois options, et je penche pour la troisième :

**A. Le ranger dans `litterature`.** C'est ce qui a été fait ce jour,
faute de mieux. Défaut : `litterature` couvre alors deux choses que rien
ne distingue — un ratio tiré d'un graphique introuvable et un ratio
recalculé depuis 6 068 lignes. C'est précisément la confusion que la
fiche 0011 avait créé `litterature` pour dissiper.

**B. Une septième origine `donnees_publiques`.** Honnête, mais une
taxonomie à sept entrées cesse d'être utilisable, et la fiche 0010 a été
écrite contre ce risque.

**C. Garder cinq origines, et ajouter un axe `verifiabilite`.** Parce
que le problème n'est pas d'où vient le nombre — c'est ce qu'on peut en
faire :

```yaml
verifiabilite: recalculable | consultable | inaccessible
```

- **recalculable** — les données brutes sont là, le script refait le
  nombre : ANSUR II, le MJCF amont, nos propres mesures ;
- **consultable** — la source existe et se lit, mais le nombre ne se
  recalcule pas : une norme ISO, une fiche constructeur ;
- **inaccessible** — la source est citée mais introuvable : Drillis &
  Contini via un graphique.

**C'est l'axe qui aurait alerté sur les quatorze ratios dès le premier
jour.** Ils étaient `litterature` — donc corrects au regard de l'origine
— et `inaccessible`, ce que rien ne disait. Le `verifie: false` le
signalait par pièce ; un axe le dirait par construction.

L'origine dit **d'où** ; la nature dit **ce qui détermine** ; la
vérifiabilité dirait **ce qu'on peut faire pour en douter**.

## Le texte des normes est payant et sous droit d'auteur

C'est déjà arrivé deux fois : la DIN 8580 (fiche 0026) et ISO 4762
(fiche 0028) ont été **citées sans être lues**, faute d'accès.

### La règle proposée

> **On cite une valeur, jamais le texte.**
>
> Une cote d'origine `norme` porte : le numéro et l'année de la norme, la
> désignation de l'élément, et la valeur. **Jamais un extrait rédigé,
> jamais un tableau recopié, jamais une figure.**
>
> Une valeur numérique isolée, accompagnée de sa référence, est un
> **fait** — le diamètre nominal d'une M3 est 3 mm. La mise en forme,
> l'organisation des tableaux et le texte explicatif sont l'**œuvre**
> de l'organisme de normalisation, et ne peuvent pas entrer ici.
>
> Et le corollaire, déjà pratiqué : **si la norme n'a pas été lue, la
> fiche le dit.** C'est ce qui a été fait pour la DIN 8580. Ce n'est pas
> une précaution de style, c'est ce qui permet à quelqu'un d'autre de
> savoir quoi vérifier.

Cette règle n'est **pas un avis juridique** — la fiche 0010 §4 l'interdit.
C'est une règle de prudence : on ne redistribue pas ce qu'on n'a pas le
droit de redistribuer, et on n'a pas lu ce qu'on n'a pas payé.

Elle est cohérente avec la fiche 0030 : un texte de norme est un
**fichier fournisseur non redistribuable**, et n'entre pas dans le dépôt.
La différence est que, pour une norme, **on ne peut même pas le mettre en
cache hors du dépôt** — on ne l'a pas.

## Ce que je recommande

1. **Créer `norme`** — le critère de correction la distingue nettement,
   et le cas ISO 4762 se présentera dès la première pièce qui tient une
   vis (fiche 0032).
2. **Ne PAS créer `donnees_publiques`.** Ajouter plutôt l'axe
   `verifiabilite`, qui répond mieux à la question réelle et qui aurait
   attrapé les quatorze ratios dès le premier jour.
3. **Inscrire la règle « une valeur, jamais le texte »** dans CLAUDE.md,
   à côté de la règle 2 sur la quincaillerie — c'est là qu'elle servira.

Le point 2 est le plus important et le moins évident : **c'est une
troisième dimension, pas une sixième valeur.**

---

## Correction du 2026-09-29 : la vérifiabilité se DÉDUIT, elle ne se déclare pas

Jeremy retient l'axe `verifiabilite` mais refuse de le déclarer :

> Il se DÉDUIT du champ `source`. Un axe calculé coûte zéro déclaration
> sur 1 431 valeurs. Un axe déclaré en coûte 1 431, et il divergera.

**La version calculée tient, et elle est meilleure que la mienne.** Voici
ce que j'ai vérifié, et les deux points où elle demande une précision.

### Pourquoi elle tient

L'argument du coût est déjà démontré dans ce dépôt. La ligne `Date:` des
fiches était déclarée : elle a disparu de **quatre fiches d'affilée**
sans que rien ne le dise. La convention de statut a divergé en six
formulations. **Ce qui se déclare à la main diverge — c'est mesuré, pas
supposé.**

Et l'argument est plus fort ici : un axe déclaré sur 1 431 valeurs serait
rempli par des motifs de `origines.yaml`, donc par des jokers. On sait
maintenant où cela mène : `ratios.**` a déclaré `effectif: 6068` de
nature `echelle`, et `reglages.**` a fait passer un identifiant écrit à
la main pour une mesure. **Un axe déclaré par joker aurait la même
valeur qu'un vert obtenu par fourre-tout : aucune.**

### La règle de déduction, précisée

| `source` contient | `verifiabilite` |
| --- | --- |
| une URL, une empreinte `sha256:`, ou un script du dépôt | **recalculable** |
| une référence bibliographique ou normative complète | **consultable** |
| une référence sans accès, ou une figure | **inaccessible** |
| rien | **inconnu** |

Appliqué à l'existant, en lisant les `source` actuelles :

- `ANSUR II 2012, +footlength / stature` → **recalculable** : le script
  est dans le dépôt, l'empreinte des CSV dans `fournisseurs.yaml` ;
- `Winter tab. 4.1 — Foot` → **consultable** : la table existe et se lit ;
- `D&C fig. 4.1 — non dérivable d'ANSUR II` → **inaccessible**, ce qui
  est exactement le statut des deux ratios restants ;
- `DIN 8580:2022-12 … NORME NON LUE (payante)` → **consultable**, et la
  fiche dit déjà qu'elle ne l'a pas été.

### Deux précisions que la version calculée exige

**1. Il faut un vocabulaire minimal dans `source`, sinon la déduction
devine.** Une source rédigée librement — « d'après le catalogue » — ne
tombe dans aucune case et sortirait `inconnu` alors qu'elle est
consultable. **Ce n'est pas un défaut : c'est le bon comportement.** Un
`inconnu` visible vaut mieux qu'un `consultable` supposé. Mais il faut
l'annoncer, sinon on croira à un bogue.

**2. La déduction doit être CONTRÔLÉE, pas seulement calculée.** Le
risque propre à un axe calculé est l'inverse de celui d'un axe déclaré :
il ne diverge pas, il **se trompe silencieusement** si la règle de
lecture est trop lâche. Une source contenant « http » quelque part dans
une phrase serait classée recalculable à tort.

Proposé : `controle_regles.py` rapporte la **répartition** des quatre
valeurs à chaque régénération. Un basculement massif d'une catégorie à
l'autre entre deux commits est le signe que la règle de lecture, ou les
sources, ont bougé.

C'est la leçon du jour appliquée à l'axe lui-même : **un calcul qui ne
peut pas échouer est aussi dangereux qu'une déclaration qui diverge.**

### Ce que cela ne change pas

L'origine `norme` reste une **sixième origine**, indépendamment. Les deux
idées sont orthogonales : `norme` dit *ce qu'on corrige quand le réel
diverge* ; `verifiabilite` dit *ce qu'on peut faire pour en douter*.
