# 0022 — La soudure : instruction, sans décision

Date : 2026-09-29
Amendée par : `0031-torsion-par-section.md` — le facteur de rigidité en torsion n'est pas une constante : il se calcule par section (395x mesuré pour 40 x 60 en tôle de 2 mm, et non « un à deux ordres de grandeur »).
Espèce : historique
État : instruction
Statut : **instruction** — ne tranche rien, à dessein. Aucune règle du
projet n'est modifiée par cette fiche.

## Ce qui est affirmé, et par qui

Jeremy déclare avoir accès à la soudure. **À vérifier avant tout usage :**
quel procédé (MIG, TIG, baguette), quel matériau, qui soude, et sur
quelle épaisseur — ces réponses changent tout ce qui suit.

L'affirmation « MEVITA soude quatre pièces pour faire un volume » vient
de Jeremy. Elle n'est **pas vérifiée ici** : la fiche 0016 avait déjà
été corrigée pour une affirmation de ce genre avancée sans source.

## Ce que la fiche 0015 posait, et ce que la soudure lève

La fiche 0015 pose qu'**une pièce plate ne peut pas faire un volume**, et
en tire l'architecture en plaques et entretoises : les volumes s'obtiennent
par empilement, les efforts passent par des vis traversantes.

La soudure lève cette limite — localement. Un cordon rend deux tôles
**solidaires en tout point de leur jonction**, là où un boulon ne les
tient qu'en un point. La différence n'est pas de degré :

- **un assemblage boulonné** transmet l'effort par frottement sous la
  tête de vis, et cède en rotation autour du boulon dès que le couple
  dépasse ce frottement ;
- **un cordon de soudure** transmet sur toute sa longueur. Il fait des
  deux tôles une seule pièce.

## Ce que cela rouvre

**1 — Le caisson fermé, donc la rigidité en TORSION.**
C'est le gain principal, et il vaut d'être expliqué. Un U ouvert (deux
plaques et une entretoise) se tord très facilement : ses parois glissent
l'une par rapport à l'autre. Fermez le U par une quatrième face soudée,
et la torsion doit désormais cisailler les quatre parois. La rigidité
gagne **un à deux ordres de grandeur**, pour la même masse.

C'est ce que ferait un tibia ou un bassin : des pièces qui ne sont pas
chargées en flexion simple mais en torsion, parce que le pied porte loin
de l'axe de la jambe.

**2 — Le logement de roulement.**
CLAUDE.md interdit un logement de roulement obtenu par découpe : les
tolérances d'une découpe ne tiennent pas le serrement. Un **tube soudé**
en travers d'une plaque, puis alésé, donne un palier correct — c'est même
la solution classique. Aujourd'hui il faut un palier rapporté et boulonné.

**3 — Les angles autres que 90°.**
L'architecture en plaques et entretoises fait des angles droits sans
effort et tout le reste difficilement. Un cordon accepte n'importe quel
angle.

**4 — Les pièces massives locales.**
Un bossage, une chape, une oreille de fixation épaisse : aujourd'hui,
empilement de plaques et vis. Soudés, ils deviennent une seule pièce.

## Ce que cela coûte

**1 — C'est définitif, et cela contredit votre règle.**
CLAUDE.md pose : « assemblage démontable, aucun collage structurel ». Un
cordon n'est ni démontable ni reprenable : le défaire, c'est meuler.

**2 — La boucle d'itération s'allonge d'un ordre de grandeur.**
Le principal acquis de l'architecture actuelle est de pouvoir couper une
pièce en carton le soir même. Une pièce soudée suppose la tôle, le
déplacement, la disponibilité du soudeur. On ne valide plus une forme
dans la journée.

Et surtout : **on ne peut pas prototyper en carton une pièce soudée.**
Le carton ne se soude pas — la maquette ne vérifierait que l'encombrement,
jamais la tenue.

**3 — La déformation thermique.**
Un cordon chauffe très localement. En refroidissant, il se contracte et
**tire la tôle**. Deux plaques soudées d'équerre ne le restent pas : c'est
un phénomène systématique, pas un accident, et on le corrige par l'ordre
des cordons, des points d'accostage, ou un gabarit de bridage. Aucune de
ces techniques ne s'improvise.

Conséquence directe : toute cote **après** soudure est incertaine. D'où
l'usinage de reprise, qui suppose une machine qu'on n'a pas.

**4 — L'aluminium se soude mal, et il perd sa tenue.**
C'est le point le plus mal connu, et il est décisif ici :

- l'aluminium exige un poste **TIG à courant alternatif**, très au-dessus
  du poste à souder ordinaire ;
- les séries 6060 et 6082 se soudent ; la 7075 **ne se soude pas** ;
- surtout, un alliage à l'état **T6** (trempé, revenu) **perd son revenu
  dans la zone chauffée**. Un 6082-T6 y retombe autour de l'état T4, soit
  environ **la moitié de sa limite d'élasticité**, sur une bande de
  quelques centimètres de part et d'autre du cordon.

Autrement dit : **souder de l'aluminium affaiblit l'aluminium**,
précisément là où l'on a décidé de faire passer l'effort. On retrouve la
tenue par un traitement thermique complet, que personne ici ne fera.

L'acier n'a pas ce défaut, se soude au poste ordinaire — et pèse trois
fois plus.

## Où cela vaudrait la peine, et où non

| | Verdict | Pourquoi |
| --- | --- | --- |
| Caisson de tibia, de bassin | **oui, probablement** | la torsion est l'effort dominant, et c'est là que le boulonné est le plus faible |
| Palier de roulement | **oui** | un logement alésé n'a pas d'équivalent boulonné |
| Plaques de liaison, brides | **non** | le boulonné y fait aussi bien et reste démontable |
| Pièces d'apprentissage | **non** | on perd l'itération dans la journée, qui est tout l'intérêt |

## La question à trancher, que cette fiche ne tranche pas

> **Un sous-ensemble soudé peut-il être un composant, lui-même boulonné
> au reste ?**

Si oui, la règle du démontable tient **au niveau de l'assemblage** — on
démonte un caisson de tibia comme on démonte une pièce — tout en levant
la limite de la pièce plate **à l'intérieur** du caisson. Le robot reste
démontable ; ses organes deviennent des blocs.

Si non, la soudure reste hors du projet.

C'est la seule question qui compte, et elle vous appartient. Les trois
qui en découlent, si la réponse est oui :

1. Quel matériau ? L'acier soudable et lourd, ou l'aluminium léger qui
   perd la moitié de sa tenue au cordon ?
2. Comment vérifier une cote après déformation thermique, sans machine
   de reprise ?
3. Comment prototyper, puisque le carton ne se soude pas ?

Aucune de ces trois n'a de réponse évidente aujourd'hui.
