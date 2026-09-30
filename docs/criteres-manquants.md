# Critères manquants du comparatif des familles — proposition

**Rédigé le 2026-10-01** par Claude Code. Statut : **PROPOSÉ**. Rien n'est
recalculé, aucun poids n'est changé, aucune fiche n'est créée.

**Ce qui est décidé par Jeremy.** Le 2026-09-30, vers 23 h, il a répondu
à `docs/arbitrage-2026-09-30.md` :

- les **9 poids actuels et la règle de décisivité sont validés** ;
- **« il manque des critères de comparaison essentiels »** ;
- il en retient **7 familles**, A à G.

Source : son prompt du 2026-10-01. `criteres_selection.yaml` porte la
réserve, au bloc `questions_ouvertes.criteres_manquants`.

**Tout le reste est proposé par Claude Code** : les sous-critères, les
grilles, les natures, les recoupements, la règle du manquant, les jeux
de poids.

---

## 0 — La règle pour une valeur introuvable, écrite AVANT la collecte

Une valeur que le constructeur ne publie pas **ne vaut jamais 0 par
défaut**. Un 0 punirait l'absence de publication comme si c'était une
mauvaise performance. Surtout, il ferait gagner le classement à celui
dont on sait le plus, **ou** à celui dont on sait le moins, selon le sens
de la grille. C'est le défaut du « prudent » corrigé le 2026-09-30.

**Proposition :**

1. La note d'une valeur introuvable est la **médiane des notes des
   candidats qui la publient**, avec un **drapeau « non publié »**
   affiché dans la case.
2. Si **aucun** candidat ne la publie, le sous-critère est **retiré du
   score** pour tous. C'est dit, et son poids se répartit au prorata
   sur les autres sous-critères de sa famille.
3. **Contrôle de bornes** : chaque note « non publié » est recalculée à
   0 puis à 5, les autres restant fixes.
   - Si le gagnant change entre ces deux bornes, l'inconnue est
     **décisive**, au sens de la règle de décisivité validée le
     2026-09-30. Elle part alors au banc (nature BANC) ou devient une
     question au fournisseur.
   - Sinon, elle est affichée, mais elle ne pèse pas sur la décision.
4. Le document engendré affiche, **par candidat, le nombre de
   drapeaux**.

Alternative écartée : une note fixe de 2,5 pour toute valeur manquante.
Elle est plus simple, mais elle tire chaque candidat vers le milieu de
la même façon, que les autres publient ou non.

---

## 1 — Les sept familles

Nature : **FICHE** se note depuis les documents (comparatif) ; **BANC** se
mesure (protocole) ; **FICHE + BANC** se lit dans la fiche, puis se vérifie
au banc. Chaque niveau de grille est défini par un **fait vérifiable** :
une valeur publiée, un calcul refait, un comportement observé.

Les seuils fondés sur une **hypothèse** sont marqués **(H)**. Ils sont à
valider avant tout calcul.

### A. Intégration mécanique

| Sous-critère | Nature | Grille 0–5 |
| --- | --- | --- |
| **A1 — Encombrement** (diamètre de l'enveloppe) | FICHE | 5 : ≤ 45 mm ; 4 : ≤ 50 ; 3 : ≤ 55 ; 2 : ≤ 60 ; 1 : ≤ 70 ; 0 : > 70 mm |
| **A2 — Bride de sortie documentée** | FICHE | 5 : plan coté (trous, taraudage, cercle de perçage) **et** fichier CAO publiés ; 4 : plan coté complet, sans CAO ; 3 : cercle de perçage et taraudage seulement ; 2 : dessin non coté ; 1 : bride mentionnée sans cote. (Rien de publié → règle § 0) |
| **A3 — Charges admissibles du roulement de sortie** : radiale, axiale, moment | FICHE | par la plus faible des trois, rapportée à la charge de référence (H) : 5 : ≥ 4× ; 4 : ≥ 3× ; 3 : ≥ 2× ; 2 : ≥ 1,5× ; 1 : ≥ 1× ; 0 : < 1× |

**Charge de référence (H), à valider.**

- **Radiale** : F_réf = marge 1,5 (fiche 0051) × masse de S (≈ 5 kg,
  masse convergée de `dimensionnement.py`) × g × facteur dynamique 2 (H),
  soit **≈ 150 N**.
- **Axiale** : la même valeur.
- **Moment** : F_réf × porte-à-faux de 30 mm (H), soit **≈ 4,5 N·m**.

*Pourquoi ce critère compte.* Dans une jambe, le roulement de sortie de
l'actionneur porte souvent le segment suivant. S'il n'est pas fait pour
cet effort, il faut un palier rapporté, ce qui ajoute masse et
encombrement.

**Recoupement** : aucun avec les 9 critères actuels. **Ajout.**

### B. Qualité du contrôle

| Sous-critère | Nature | Grille 0–5 |
| --- | --- | --- |
| **B1 — Réversibilité** : couple pour entraîner la sortie à la main, rapporté au couple continu | FICHE + BANC | 5 : ≤ 2 % ; 4 : ≤ 4 % ; 3 : ≤ 7 % ; 2 : ≤ 12 % ; 1 : ≤ 20 % ; 0 : > 20 % |
| **B2 — Jeu** en sortie | FICHE + BANC | 5 : ≤ 5′ ; 4 : ≤ 10′ ; 3 : ≤ 15′ ; 2 : ≤ 20′ ; 1 : ≤ 30′ ; 0 : > 30′ (minutes d'arc) |
| **B3 — Mode couple natif** | FICHE | 5 : mode « MIT » (position, vitesse, couple, raideur et amortissement exécutés dans le pilote) ; 4 : consigne de couple ou de courant documentée ; 3 : couple limité par une borne de courant seulement ; 1 : position seule |
| **B4 — Télémétrie thermique** | FICHE + BANC | 5 : température du bobinage **et** du pilote, séparées ; 4 : bobinage seul ; 3 : une température « moteur » dont l'emplacement n'est pas précisé ; 2 : pilote seul |
| **B5 — Débit de retour d'état** sur le bus | FICHE + BANC | 5 : ≥ 1 kHz ; 4 : ≥ 500 Hz ; 3 : ≥ 200 Hz ; 2 : ≥ 100 Hz ; 1 : < 100 Hz |

*Pourquoi.* Un actionneur **réversible** laisse la jambe céder un peu au
contact du sol, au lieu de transmettre le choc aux dents du réducteur.
Le **jeu** est le petit angle que la sortie parcourt sans que le moteur
tourne : il dégrade la précision de position. Le **mode couple** est ce
qu'emploient les contrôleurs de marche modernes.

**Recoupements :**

- avec la **robustesse** (12) : sa grille lit déjà « réversible / non
  établie ». Proposition : **transférer la réversibilité en B1**, la
  robustesse ne gardant que le type de réducteur et la tenue au blocage ;
- avec l'**éliminatoire télémétrie** : il reste un éliminatoire de
  **présence**, et B4 note la **qualité**.

### C. Thermique réelle

| Sous-critère | Nature | Grille 0–5 |
| --- | --- | --- |
| **C1 — Masse installée** : actionneur + plaque d'aluminium requise par la condition du nominal publié | FICHE (calcul) | la grille de la masse actuelle : 5 : ≤ 150 g ; 4 : ≤ 200 ; 3 : ≤ 250 ; 2 : ≤ 350 ; 1 : ≤ 500 ; 0 : > 500 g |
| **C2 — Conditions de mesure du continu publiées** | FICHE | 1 point par élément publié : plaque, ambiante, vitesse, limite de température, valeur au blocage |
| **C3 — Continu mesuré au blocage**, rapporté au besoin RMS × 1,5 de la pire articulation, à la taille S | BANC | 5 : ≥ 2× ; 4 : ≥ 1,5× ; 3 : ≥ 1,2× ; 2 : ≥ 1,0× ; 1 : ≥ 0,8× ; 0 : < 0,8× |

**Masse de la plaque (H)** : aluminium de 3 mm (H), 2,7 g/cm³. Une plaque
de 70 × 70 mm pèse ≈ 40 g, une de 150 × 150 mm ≈ 182 g. Sans plaque
publiée, règle § 0.

*Pourquoi.* Un nominal « sur plaque de 150 mm » suppose qu'on boulonne le
moteur sur 180 g d'aluminium. Comparer des masses **nues** avantage celui
qui a besoin du plus gros dissipateur.

**Recoupements :**

- avec la **masse** (5) : **C1 la remplace** ;
- avec la **capacité** (18) : C3 **remplacera l'hypothèse k** quand le
  banc l'aura mesuré. En attendant, C2 dit combien k est incertain, et
  devrait **informer** la capacité plutôt qu'être noté à part (fusion
  proposée avec D).

### D. Qualité des preuves

| Sous-critère | Nature | Grille : 1 point par fait établi |
| --- | --- | --- |
| **D1** — fiche versionnée **et** datée | FICHE | 1 |
| **D2** — révision matérielle nommée (la clé de révision n'est pas « non publiée ») | FICHE | 1 |
| **D3** — historique des révisions, ou notes de version publiées | FICHE | 1 |
| **D4** — document téléchargeable, dont l'empreinte est au registre 0030 (et non une page web mouvante) | FICHE | 1 |
| **D5** — aucune contradiction interne relevée | FICHE | 1 |

**Deux options, sans choisir :**

- **(a) Critère pondéré.** D entre dans le score comme les autres.
- **(b) Indicateur de confiance, hors score.** D s'affiche à côté du
  score (par exemple « preuves 3/5 »), et le verdict dit : « le
  vainqueur repose sur des preuves de niveau N ». Un vainqueur à preuves
  faibles devient une raison d'aller au banc, pas un malus.

**⚠ Le biais « pénaliser qui publie plus ».** D5 compte les
contradictions. Or plus un fabricant publie, plus on peut en trouver :
RobStride en a trois relevées (RS02 à 6 ou 7 ; RS03 à 20 ou 21 ; EduLite
absent du PDF), parce qu'il publie un PDF de 38 pages **et** des manuels.
Un fabricant qui ne publie qu'une page n'a aucune contradiction
**possible**.

- Le 2026-09-30, ce biais a été corrigé **trois fois** dans la capacité
  (« prudent »).
- **Si l'option (a) est retenue**, D5 se note **par valeur publiée**
  (contradictions ÷ valeurs relevées), ou il est **retiré**.
- L'option (b) l'atténue, sans le supprimer.

**Recoupement** avec la **fiabilité du fournisseur** (15), qui note la
garantie et la distribution : c'est un autre objet. **Ajout** (option a),
ou **affichage** (option b).

### E. Sécurité en défaut

| Sous-critère | Nature | Grille 0–5 |
| --- | --- | --- |
| **E1 — Chien de garde de communication** | FICHE + BANC | 5 : documenté, **actif par défaut** (valeur usine non nulle) ; 4 : documenté, réglable, **désactivé par défaut** ; 3 : comportement à la perte de communication documenté, sans délai réglable ; 2 : perte de communication mentionnée, sans comportement |
| **E2 — Bus-off et reprise** | FICHE + BANC | 5 : bus-off et reprise documentés ; 3 : bus-off documenté seul ; 1 : erreurs CAN signalées, sans bus-off |
| **E3 — Protections documentées**, avec seuil **et** réaction (surchauffe du bobinage, surchauffe du pilote, surintensité, sous-tension, surtension, blocage) | FICHE + BANC | 5 : ≥ 5 protections avec seuil et réaction ; 4 : ≥ 5, sans seuil pour certaines ; 3 : 3 ou 4 ; 2 : 1 ou 2 ; 1 : codes d'erreur sans réaction décrite |

*Pourquoi.* Au banc comme dans le robot, une perte du bus CAN pendant un
palier chargé doit **couper** l'actionneur. Un chien de garde désactivé
en usine est un piège : il faut le savoir **avant** la première mise
sous tension. Le protocole de banc l'exige déjà (§ 1.3).

**Recoupement** avec la **robustesse** : « protections documentées » est
dans sa grille. Proposition : **transférer en E3**.

### F. Écosystème logiciel

| Sous-critère | Nature | Grille : points |
| --- | --- | --- |
| **F1** — pilote ROS 2 (`ros2_control`) existant | FICHE | 2 si officiel ; 1 si communautaire maintenu (commit de moins d'un an) |
| **F2** — prise en charge par LeRobot | FICHE | 1 |
| **F3** — modèle MuJoCo ou URDF de l'actionneur publié | FICHE | 1 |
| **F4** — SDK sous licence libre (licence **lue**) | FICHE | 1 |

**Recoupement** avec l'**ouverture** (5) : elle note le protocole public,
le SDK libre et le firmware publié. F4 et le SDK libre font doublon.
Proposition : **fusionner** ouverture et F en un critère « ouverture et
écosystème », sur 0–5 : protocole public 1, F1 à F4, firmware publié
bonus plafonné.

**Remarque** : ces faits ne sont **pas** dans les documents du registre ;
ils se lisent sur des dépôts et des pages web. La collecte du § 3 les met
donc à `null`, « non trouvé dans les documents au registre ».

### G. Énergie

| Sous-critère | Nature | Grille 0–5 |
| --- | --- | --- |
| **G1 — Pertes cuivre** sur la marche de référence, à la taille S, pour 12 actionneurs de jambe | FICHE (calcul : `scripts/pertes_cuivre.py`) | rapportées au meilleur candidat : 5 : ≤ 1,25× ; 4 : ≤ 1,5× ; 3 : ≤ 2× ; 2 : ≤ 3× ; 1 : ≤ 5× ; 0 : > 5× |

*Pourquoi.* Le courant qui traverse les bobinages chauffe, et cette
chaleur est prise à la batterie. Deux actionneurs de même couple peuvent
dissiper du simple au double, selon leur résistance et leur constante de
couple. La pertinence porte sur l'**autonomie** et la **tenue
thermique**.

**Recoupement** avec la **capacité**, qui vérifie déjà RMS ≤ continu. G ne
double pas ce contrôle : il chiffre ce que la capacité ne dit pas,
l'énergie. **Ajout.**

**Limite** : ces pertes demandent R et Kt, **et la convention du
courant** (crête ou efficace). Elles changent d'un facteur 2 selon
celle-ci, et la plupart des fiches ne la précisent pas. Le script calcule
les deux bornes ; tant qu'elles ne sont pas levées, G1 ne se note pas
(§ 5).

---

## 2 — Tableau récapitulatif

| Famille | Sous-critères | Nature | Recoupement avec les 9 critères | Proposition |
| --- | --- | --- | --- | --- |
| A. Intégration | A1, A2, A3 | FICHE | — | ajouter |
| B. Contrôle | B1 à B5 | FICHE + BANC (B3 : FICHE) | robustesse (réversibilité) ; éliminatoire de télémétrie | ajouter ; B1 reprend la réversibilité de la robustesse |
| C. Thermique | C1, C2 ; C3 | C1-C2 : FICHE ; C3 : BANC | masse ; capacité (k) | C1 **remplace** la masse ; C3 remplacera k ; C2 fusionne avec D |
| D. Preuves | D1 à D5 | FICHE | fiabilité du fournisseur (distinct) | option (a) ajouter, ou (b) indicateur hors score |
| E. Sécurité | E1, E2, E3 | FICHE + BANC | robustesse (protections) | ajouter ; E3 reprend les protections |
| F. Écosystème | F1 à F4 | FICHE | ouverture (SDK libre) | **fusionner** avec l'ouverture |
| G. Énergie | G1 | FICHE (calcul) | capacité (thermique, sans doublon) | ajouter, noté seulement quand la convention du courant est levée |
