# Protocole du banc de qualification — *proposé*

**Rédigé le 2026-09-30.** Statut : **proposé**, pas décidé : rien n'est
acheté, rien n'est mesuré. Aucune fiche. Ce protocole sert le banc de
qualification (cadrage, § 13, question 12 ; `docs/comparatif-banc.md`) :
**mesurer avant d'acheter en quantité**.

Le banc, tel que le comparatif le place en tête : **1 × Damiao J4310 V1.2
48 V + 1 × RobStride EduLite 05 + 1 × RobStride RS05**, une alimentation
48 V, un adaptateur USB-CAN.

**Mise à jour du 2026-09-30, nuit.** Avec la règle de décisivité étendue,
aucune inconnue n'est décisive : c'est un **banc de VÉRIFICATION, pas de
départage** (`docs/comparatif-banc.md`). Il vérifie une décision de
famille que les données publiées portent déjà ; le § 2 bis dit, avant la
mesure, ce qui la ferait rouvrir. Le § 2 ter ajoute la dispersion entre
deux exemplaires.

**Ce document ne propose aucun achat** (CLAUDE.md, règle d'achat c).
Quand une condition de sécurité n'est pas remplie par un poste du
budget, il le constate, sans rien suggérer.

---

## 1 — Sécurité, avant toute mesure

Un actionneur de robot sur un banc, c'est un moteur capable de plusieurs
N·m, piloté par du logiciel neuf, avec un bras de levier et une
alimentation de 500 W. Les règles ci-dessous sont des **préalables** :
tant qu'une seule n'est pas remplie, on ne met pas sous tension.

### 1.1 L'alimentation 48 V limite le courant

- **Une alimentation à limitation de courant réglable**, réglée au plus
  bas courant qui permet le palier en cours. Un court-circuit ou un
  blocage mal serré se traduit alors par une chute de tension, pas par
  des centaines de watts dans un bobinage.
- **Constat** : l'alimentation chiffrée au budget, une Mean Well
  RSP-500-48 (`params/budget.yaml`), est une alimentation à découpage à
  **tension fixe**. Sa protection contre les surintensités n'est **pas un
  réglage de limite** (connaissance générale, non vérifiée sur sa fiche).
  **Ce poste, tel qu'il est chiffré, ne remplit donc pas cette
  condition.** C'est dit ici, pas résolu.
- **L'alimentation d'un banc est un OUTILLAGE** (précisé le
  2026-09-30) : elle sert le banc, pas le robot, et **doit être à
  limitation de courant réglable**. À ce titre, son choix relève de la
  **seule décision de Jeremy** (CLAUDE.md, règle d'achat b : l'outillage
  n'a aucun critère automatique). Ce protocole énonce l'exigence ; il ne
  propose aucun modèle.
- 48 V continu reste une très basse tension de sécurité (moins de 60 V).
  C'est l'**énergie** disponible qui fait le risque, pas le contact.

### 1.2 Un arrêt d'urgence matériel coupe la puissance

- **Un bouton d'arrêt d'urgence qui coupe physiquement le 48 V** vers
  les actionneurs : par un contacteur ou un interrupteur calibré pour du
  courant continu à cette tension. **Pas par le logiciel.** Un arrêt
  logiciel dépend précisément de ce qu'on est en train de tester.
- L'adaptateur USB-CAN et le calculateur restent alimentés à part :
  après un arrêt d'urgence, on peut encore lire les températures.
- On vérifie l'arrêt d'urgence **à vide**, avant chaque session.

### 1.3 Des limites dans le logiciel, en plus

- **Limites de couple et de courant** programmées dans chaque
  actionneur, réglées à **10 % au-dessus du palier** en cours, jamais au
  maximum du constructeur.
- **Chien de garde** : à la perte de communication, l'actionneur doit se
  désactiver. Le Damiao le signale par un code d'erreur (« perte de
  communication », manuel V1.4, p. 14-15) ; on vérifie ce comportement
  **avant** le premier palier chargé, en débranchant le câble CAN.
- Ces limites **s'ajoutent** à l'arrêt matériel, elles ne le remplacent
  pas.

### 1.4 Le bras de levier est fixé, et sa course est bornée

- Bras **rigide**, fixé à l'arbre de sortie par un moyen qui ne glisse
  pas (bride serrée ou goupille), et fixé de l'autre côté au
  dynamomètre ou à la balance.
- **Une butée mécanique de chaque côté** limite sa course. Si la
  fixation lâche, le bras ne fait pas un tour complet.
- **Personne dans le plan de rotation du bras** quand l'actionneur est
  activé.

### 1.5 Rotor bloqué : le risque, c'est la chauffe

- Au rotor bloqué, toute l'énergie finit en chaleur dans le bobinage,
  sans rotation qui ventile. C'est exactement ce qu'on mesure — et
  c'est donc un risque constant.
- **On arrête un palier 10 °C sous la protection thermique du
  constructeur** : 135 °C d'enroulement pour RobStride (manuel RS05,
  p. 50) ; 100 °C comme seuil recommandé pour le Damiao (courbe
  constructeur).
- Le montage repose sur une **surface non inflammable**. Aucune batterie
  LiPo sur le banc : l'alimentation seule.

### 1.6 Ce qu'on ne fait jamais seul, ni sans surveillance

- **Jamais** un actionneur activé sans quelqu'un devant, main près de
  l'arrêt d'urgence. Pas de palier thermique de 30 minutes laissé sans
  surveillance, pas même « le temps d'un café ».
- **Jamais seul** : la première mise sous tension de chaque actionneur,
  le premier palier chargé, et tout essai au-delà du couple continu
  publié. Une seconde personne se tient à l'arrêt d'urgence.
- **Jamais** de câblage modifié sous tension.

---

## 2 — Protocole de mesure : les couples continus en condition IDENTIQUE

Repris du comparatif du banc (§ 5). But : remplacer l'hypothèse **k**
par une mesure, sur les trois actionneurs, dans la **même** condition.
Les fiches ne sont pas comparables entre elles : les plaques diffèrent,
ou la condition n'est pas publiée.

1. **Même montage.** Chaque actionneur est fixé sur la même plaque
   d'aluminium de 70 × 70 mm, la plus petite condition publiée (RS05,
   EduLite 05). L'épaisseur et la matière sont notées. La plaque repose
   sur le même support isolant.
2. **Même alimentation**, 48 V, même bus CAN, même débit.
3. **Rotor bloqué**, par le bras de levier du § 1.4 sur un dynamomètre
   ou une balance, longueur notée. Le couple **réel** est lu au
   dynamomètre, le couple **déclaré** par la télémétrie : leur écart est
   lui-même une mesure. *Le blocage est la condition la plus proche d'un
   robot qui tient debout.*
4. **Mêmes paliers de couple**, par ordre croissant, sur les trois
   actionneurs : d'abord le plus bas des couples continus publiés, puis
   des paliers de 10 %.
5. **Même durée** : chaque palier est tenu jusqu'à l'équilibre thermique
   (variation < 1 °C en 5 min), au plus 30 min, et jamais au-delà du
   seuil du § 1.5.
6. **Relevés à 1 Hz** : température bobinage et driver (télémétrie),
   température du boîtier (thermocouple), courant, couple réel.
   **Température ambiante** notée au début et à la fin de chaque palier.
7. **Résultat** : le plus haut couple tenu à l'équilibre sous la limite
   thermique est le **continu mesuré**, dans cette condition.

---

## 2 bis — Critère d'abandon, écrit AVANT la mesure — *proposé*

**Statut : PROPOSÉ**, écrit le 2026-09-30 (nuit), avant tout achat et
toute mesure. Un critère écrit après la mesure s'ajuste au résultat ;
écrit avant, il peut donner tort.

> **Si le couple continu du J4310, mesuré AU BLOCAGE sur la plaque
> d'aluminium de 70 × 70 mm (§ 2), est inférieur à 1,75 N·m, le choix
> de famille est ROUVERT vers RobStride.**

- **D'où vient 1,75 N·m** : 0,5 × 3,5 N·m (nominal publié). Le comparatif
  des familles bascule à **k ≈ 0,50** : Damiao gagne jusqu'à k = 0,50 ;
  RobStride (RS05 → RS02 → RS06) gagne dès k = 0,49
  (`docs/choix-famille-actionneurs.md`). Sous 1,75 N·m, le k mesuré du
  J4310 est sous la bascule.
- **« Rouvert », pas « changé »** : la valeur mesurée entre au catalogue
  (§ 3), le comparatif est relancé, et c'est son résultat, lu par
  Jeremy, qui décide. Le critère déclenche le réexamen ; il ne le fait
  pas.
- **L'incertitude compte** (*proposé*) : le critère est rempli si la
  borne **haute** de l'intervalle mesuré (valeur + incertitude) est sous
  1,75 N·m. Si 1,75 N·m tombe **dans** l'intervalle, la mesure ne
  tranche pas : on le consigne, et on réduit l'incertitude avant de
  conclure.
- **Avec deux exemplaires** (§ 2 ter), le critère s'applique au **plus
  faible** des deux (*proposé*) : un robot est limité par sa moins bonne
  articulation.
- **Ce qui ne rouvre pas le choix** : un continu mesuré entre 1,75 N·m
  et 3,5 N·m confirme la famille, même s'il est sous le nominal publié.
  C'est précisément ce que k décrit.

*Mise à jour du 2026-09-30, 22 h 30 — le texte ci-dessus est conservé,
il ne vaut plus.* Le critère est désormais **calculé** par
`scripts/selection_multicritere.py` (`criteres_selection.yaml`,
`banc.critere_abandon`) et publié dans `docs/comparatif-banc.md` § 4.
Il prend **un seul seuil thermique**, celui du § 1.5 : 90 °C pour le
Damiao, c'est-à-dire la protection de 100 °C moins 10 °C. L'estimation
utilise le même seuil.

**Résultat du recalcul en 48 V : le critère est SANS OBJET.** La famille
Damiao, notée sur la variante 48 V, ne gagne à aucun k du balayage. Il
n'y a donc pas de choix Damiao à rouvrir. Le seuil de 1,75 N·m ne repose
plus sur rien. Détail : `journal/2026-09-30.md`, « Recalcul en 48 V ».

---

## 2 ter — Dispersion entre deux exemplaires

**Pourquoi** : une mesure sur un seul exemplaire ne dit pas si l'on a
mesuré le modèle ou l'exemplaire. Deux exemplaires du même modèle
(option « vérification » du budget : 2 × J4310) donnent un premier
ordre de grandeur de l'écart de fabrication.

1. **Même protocole, à l'identique** (§ 2) : même plaque, même
   alimentation, même bras, mêmes paliers, et si possible le même jour.
   Chaque exemplaire est mesuré **seul** sur la plaque, l'un après
   l'autre. L'ordre de passage est noté.
2. **Les deux continus mesurés** sont consignés **séparément**, chacun
   avec son incertitude de résolution.
3. **L'écart** entre les deux est consigné comme une entrée à part,
   `type_incertitude: dispersion`, `n: 2`.
4. **Ce que deux exemplaires ne disent pas** : avec n = 2, l'écart
   n'est **pas** un écart-type, et il ne permet aucune statistique sur
   la production. Il dit seulement si deux pièces du même modèle sont
   proches (écart comparable à la résolution) ou non (écart nettement
   plus grand : la valeur publiée ne peut pas être prise pour tout un
   robot).
5. **Même mesure croisée pour la télémétrie** : le rapport couple réel ÷
   couple déclaré (§ 3), sur chaque exemplaire.

---

## 3 — Chaque mesure : ce qu'elle tranche, et comment on la consigne

Chaque relevé devient une entrée de `params/mesures.yaml`, sous la forme
décidée par la fiche 0041 : `grandeur`, `valeur`, `unite`,
`incertitude`, `type_incertitude` (`resolution` ou `dispersion`),
`instrument`, `n`, `date`, `alimente`, `note`. **L'incertitude se porte
avec la valeur, jamais après coup.**

| Mesure | Ce qu'elle tranche | `alimente` | `type_incertitude` |
| --- | --- | --- | --- |
| Continu en blocage du **J4310** (70 × 70 mm, 48 V) | le **k du Damiao** : continu mesuré ÷ 3,5 N·m publié | `candidats.dm_j4310_48v.couple_continu_Nm` (nouvelle condition, en blocage) | `dispersion` si plusieurs essais, sinon `resolution` du dynamomètre |
| Continu en blocage de l'**EduLite 05** | son comportement près du blocage, que RobStride ne publie pas | `candidats.edulite05.couple_continu_Nm` (nouvelle condition, en blocage) | idem |
| Continu en blocage du **RS05** | vérifie la valeur publiée (1,2 N·m, PDF p. 29) **et** départage RS05 / EduLite 05 dans la même condition | `candidats.rs05.couple_continu_Nm` (condition en blocage) | idem |
| Écart entre deux exemplaires de **J4310** (§ 2 ter) | si la valeur d'un exemplaire vaut pour le modèle | aucune cote : une entrée à part | `dispersion`, `n: 2` |
| Couple réel ÷ couple déclaré, par actionneur | la confiance à accorder à la télémétrie de couple (le cas LeRobot, `docs/choix-interfaces.md`) | aucune cote : une note de l'entrée | `resolution` |
| Température ambiante, épaisseur de la plaque, longueur du bras | la condition elle-même : sans elles, la mesure n'est pas reproductible | champs `note` de chaque entrée | `resolution` |

**Après la mesure**, et seulement après :

1. la valeur mesurée entre au catalogue comme une **condition de plus**,
   avec `origine: mesure`, et remplace l'hypothèse k pour cet
   actionneur ;
2. `scripts/selection_multicritere.py` est relancé : les deux documents
   se régénèrent, et l'on voit si le classement des familles tient ;
3. **alors seulement** se pose la question d'acheter en quantité.

---

## 4 — Ce que ce protocole ne dit pas

- **Il n'est pas décidé** : c'est une proposition.
- **Il ne mesure pas le rendement en rotation** : il faudrait un frein
  ou un second moteur, qui ne sont pas prévus.
- **Il ne mesure pas la dispersion entre exemplaires** : un seul
  exemplaire de chaque modèle. L'option « 3 × J4310 » la mesurerait,
  pour un seul modèle.
  *Mise à jour du 2026-09-30, nuit* : le § 2 ter ajoute une mesure de
  dispersion entre **deux** exemplaires de J4310, un ordre de grandeur
  et pas une statistique.
- **Le critère d'abandon (§ 2 bis) est proposé**, pas décidé : son
  seuil, sa règle d'incertitude et son application au plus faible des
  deux exemplaires sont à valider par Jeremy.
- **Le dynamomètre ou la balance, le thermocouple et la plaque ne sont
  pas chiffrés.** L'outillage relève de la seule décision de Jeremy
  (CLAUDE.md, règle d'achat b).
