# 0038 — Le facteur limitant n'est pas le couple, c'est la température

Date : 2026-09-29
Espèce : proposition
État : proposée
Statut : **proposée** — instruction. Ne tranche rien.
Remplacée par : `0062-dimensionnement-thermique-applique.md` — contredite en partie (série existante, classes → tailles) : remplacée par ce qui est appliqué, au lieu d'être acceptée.

## 1 — Vérification

**Confirmé, et presque mot pour mot.** Thèse de Florent Forget, Toulouse 3,
2018, *Modélisation et contrôle d'actionneurs pour la robotique
humanoïde*, chapitre 5 « Prise en compte de la température de
l'actionnement lors du contrôle des robots humanoïdes », p. 93-102.
**Lue directement**, PDF de 148 pages, pas résumée de seconde main.

Le §5.1 énonce que les générateurs de mouvements ne considèrent que des
limitations en valeur maximale de couple et de vitesse, qui ne sont pas
compatibles avec les plages d'utilisation des moteurs électriques : ces
derniers ont des valeurs limites très élevées en couple et en vitesse,
mais **c'est la température qui est le facteur limitant**.

### Une correction de détail

Vous dites « quatre zones ». Le texte en décrit **trois régions de
fonctionnement**, la figure 5.1 portant quatre étiquettes :

| Région | Ce qu'on y risque |
| --- | --- |
| **zone sûre** (cadre vert) — fonctionnement continu | rien, mais une partie de la plage est perdue |
| **zone blanche** — opérations de courte durée | surchauffe : **démagnétisation des aimants**, **fonte du vernis d'isolation** du bobinage |
| **au-delà du cadre bleu** | destruction : déformation de la structure sous couple excessif, arrachements par force centrifuge sous vitesse excessive |

« safe zone » et « non-safe zone » ne sont pas deux régions de plus : ce
sont les deux **modes d'exploitation** décrits juste après — se
restreindre au vert, ou accepter le bleu entier avec le risque.

### Ce que je n'ai pas pu vérifier

- La figure 5.1 est un **graphique** : les frontières numériques des
  zones n'en sont pas extractibles. Même défaut que Winter fig. 4.1.
  L'exemple porte sur un Maxon 150 W à courant continu — sans rapport
  avec nos servos.
- Les valeurs de `RTHW−C`, `RTHC−A`, `CW`, `CC` estimées au §5.3 sont
  **celles de Talos**, robot de taille adulte à réducteurs de rapport
  ~100. Elles ne se transposent pas.
- Le modèle suppose **seuls les frottements visqueux**. La thèse le dit.

## 2 — Ce que nos enveloppes ne disent pas

Nos enveloppes donnent **6,694 N·m** et **6,89 rad/s**. Deux maxima,
aucune durée. Au regard du chapitre 5, elles ne disent pas dans quelle
région nous sommes — elles ne peuvent pas le dire.

### Ce qu'il faudrait ajouter

Le modèle de la thèse (éq. 5.4) donne la puissance dissipée :

> `PJ = R(T) · i²`, avec `R(T) = R_TA · (1 + α · (T − TA))`

Deux conséquences, et la seconde n'est pas évidente :

1. **La grandeur thermique n'est pas le couple maximal, c'est le couple
   EFFICACE** — la racine de la moyenne du carré sur un cycle. Le carré
   est dans l'équation : un pic bref au double du couple coûte quatre
   fois plus d'échauffement instantané, mais sur 5 % du cycle il pèse
   moins qu'un couple moyen permanent.
2. **La résistance croît avec la température**, donc l'échauffement
   s'auto-entretient. Un moteur chaud dissipe davantage à courant égal.
   Ce n'est pas linéaire, et ce n'est pas conservateur de l'ignorer.

Il faudrait donc, par articulation :

| Grandeur | Pourquoi |
| --- | --- |
| **couple efficace sur un cycle de marche** | c'est elle qui chauffe |
| **rapport cyclique** — part du temps au-dessus du couple continu | décide si l'on est en « courte durée » |
| **durée du cycle** | 0,72 s en amont — l'échauffement s'intègre sur bien plus |
| **constante de temps thermique** | la thèse insiste : la température évolue **beaucoup plus lentement** que couple et vitesse |

Les trois premières se calculent chez nous. **La quatrième vient du
constructeur**, et nous n'avons choisi aucun modèle.

## 3 — La série temporelle des couples : elle n'existe pas

Vérifié dans le code, et la réponse est plus nette que la question.

**a. Les enveloppes ne viennent pas de la marche en boucle fermée.**
Elles viennent de poses tenues par correcteur PD et d'un balancement
sinusoïdal de 2 s à la cadence amont (0,72 s). Le run de 12 s en boucle
fermée est un autre programme.

**b. Dans les deux cas, rien n'a été gardé.**

- `enveloppes_actionneurs.py` fait
  `couples = np.maximum(couples, np.abs(d.actuator_force))` : un
  **maximum courant**. Chaque pas écrase le précédent. Aucune écriture
  de série.
- `sim/upstream/replay_policy.py` journalise
  `(sim.data.time, qpos[0:3])` — le temps et la position de base.
  **Aucun couple, à aucun moment.**

**c. Mais elle n'est pas perdue : elle n'a jamais été produite.** Les deux
programmes rejouent une simulation déterministe. Garder la série coûte
une ligne dans chacun — remplacer le maximum par une accumulation.

C'est une différence qui compte : il n'y a rien à récupérer, il y a
quelque chose à relancer.

### Ce qu'un régime thermique en tirerait

Avec la série `couple(t)` par articulation, sur un cycle :

- le **couple efficace**, `sqrt(mean(τ²))` — la grandeur qui chauffe ;
- le **rapport crête/efficace**, qui dit si le dimensionnement est piloté
  par la pointe ou par l'échauffement ;
- le **rapport cyclique** au-dessus d'un seuil de couple continu.

Aujourd'hui nous n'avons que la crête. **Nous ne savons donc pas si
6,694 N·m est un pic de 20 ms ou un régime permanent** — et c'est
précisément la distinction que le chapitre 5 dit décisive.

## 4 — Cela change-t-il le choix entre 3 classes (×4,0) et 4 (×2,5) ?

**Je ne tranche pas, mais le problème est mal posé tel quel.**

Le facteur d'excès (×4,0 ou ×2,5) a été calculé sur les **couples
maximaux**. Or, si le dimensionnement doit être thermique :

- un facteur ×2,5 sur la **crête** peut correspondre à un facteur très
  supérieur sur l'**efficace**, si le rapport crête/efficace est élevé —
  ce qui est le cas typique d'une marche, alternant appui et vol ;
- inversement, un facteur ×4,0 sur la crête peut être **insuffisant**
  thermiquement si l'articulation travaille en quasi-permanence — une
  cheville en phase d'appui, par exemple.

**Autrement dit : le nombre de classes et le facteur d'excès pourraient
être les mêmes, et les articulations changer de classe.** Une articulation
à forte crête et faible rapport cyclique et une articulation à faible
crête et fort rapport cyclique sont aujourd'hui classées par la première
grandeur seulement.

Ce qu'il faudrait avant de rouvrir la question : **la série temporelle**
(§3), puis un reclassement sur le couple efficace, puis comparer les deux
classements. Si aucune articulation ne change de classe, la question est
close. Si certaines changent, le choix de 3 ou 4 classes est second par
rapport à la grandeur sur laquelle on classe.

## 5 — La dissipation à la conception : ce que cela fait à la fiche 0015

Le §5.2 donne explicitement deux voies :

> « adapter le contrôle de manière à garder une température raisonnable,
> là où la seconde technique vise à améliorer le comportement thermique
> du système **à la conception** »

La seconde nous concerne directement, et elle touche l'architecture en
plaques (fiche 0015).

### Le modèle le dit lui-même

Le schéma thermique équivalent (fig. 5.2) est une chaîne :

> bobinage → `RTHW−C` → carter → `RTHC−A` → air ambiant

La seconde résistance, **carter vers air**, dépend de ce à quoi le carter
est fixé. Un moteur boulonné sur une plaque conduit une partie de sa
chaleur dans la plaque. **La pièce qui porte le moteur est un élément du
circuit thermique**, que la fiche 0015 n'a jamais considéré.

### L'ordre de grandeur, qui est brutal

Conductivité thermique, valeurs d'ordre courant :

| Matériau | λ (W·m⁻¹·K⁻¹) |
| --- | --- |
| aluminium | ~200 |
| contreplaqué | ~0,15 |
| carton | ~0,05 |

**Environ quatre mille entre l'aluminium et le carton.** Ce n'est pas un
paramètre à ajuster : c'est la différence entre un dissipateur et un
isolant. Une plaque de carton portant un moteur l'enferme dans sa propre
chaleur.

⚠ Ces valeurs sont d'**ordre de grandeur**, citées de mémoire technique
courante et **non sourcées** dans ce dépôt. Elles suffisent à poser le
problème, pas à dimensionner.

### Est-ce un critère qui manque à `matieres` ? Oui — et il est déjà cadré

Il manque un champ, et la fiche 0020 dit déjà comment le traiter :

```yaml
matieres:
  alu_tole_3:
    conductivite_thermique: null    # W/(m.K) — à sourcer
```

`null` par défaut, donc **à mesurer ou à sourcer**, et visible dans
« À mesurer » de `/etat/`. Pas de valeur inventée.

Et le corollaire, qui est une **contrainte de conception**, pas une
donnée : **une pièce qui porte un actionneur ne peut pas être en carton**,
même en prototype. Le prototype carton validerait l'encombrement et
tromperait sur la tenue thermique — exactement le défaut relevé pour la
soudure (fiche 0022) : une maquette qui ne vérifie que ce qui se voit.

**Je ne l'inscris pas dans CLAUDE.md** : c'est une décision d'architecture
qui vous revient, et elle entame la règle « concevoir au plus
contraignant, c'est-à-dire au carton ».

## Sources

- **Forget, F. (2018)**, *Modélisation et contrôle d'actionneurs pour la
  robotique humanoïde*, thèse, Université Toulouse 3 Paul Sabatier,
  HAL tel-02128260. **Chapitre 5 lu directement**, p. 93-102. Travaux
  menés avec Florian Valette, équipe Gepetto, LAAS-CNRS.
- Aucune valeur numérique n'est reprise de cette thèse : ses paramètres
  thermiques sont ceux de Talos et ne se transposent pas.
