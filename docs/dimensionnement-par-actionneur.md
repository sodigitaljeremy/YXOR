# Dimensionnement par classe d'actionneur

**Calculé le 2026-09-30 à 17 h 07 ; régénéré le 2026-09-30 à 22 h 49**
(heure lue par `date`). Aucune pièce, aucun palier modifié. Ce document ne
choisit rien et ne propose aucun achat : il dit jusqu'où porte chaque classe.

> **Ce qui a changé depuis l'instantané de 17 h 07** (l'ancien texte est
> dans l'historique git, commit `00af03a`). Les tableaux des §§ 4 et 5
> sont la sortie de `dimensionnement.py --markdown` ; celui du § 1 est
> relu dans le catalogue. En substance :
> - **EduLite 05** : continu (1,8 N·m) et vitesse lus au manuel, plus de
>   « non vérifiable » ; homogène 0,58 → **0,54 m** ;
> - **RS05** : 1,8 → **1,6 N·m** (la plus basse des deux valeurs publiées) ;
>   homogène 0,57 → **0,54 m** ;
> - **adaptateur USB-CAN chiffré** (candleLight) : il n'est plus un poste
>   inconnu ; les jambes RobStride gagnent ≈ 54 CHF ;
> - **phase `banc`** : 2 × RS05 + adaptateur (option), et l'option
>   « vérification » ; l'alimentation n'y est plus comptée ;
> - **marge 1,5 décidée** (fiche 0051) ; configuration L calculée.

Régénérer : `.venv/bin/python scripts/dimensionnement.py --markdown`.

## Statuts

| Marque | Sens |
| --- | --- |
| **V** | **vérifié** — lu à la source citée, ou calculé par le script versionné |
| **Déd** | **déduit** — un modèle, une hypothèse ou une lecture, à discuter |

---

## 0 — Le calcul inversé, et ce qu'il faut savoir avant les chiffres

Les paliers P1, P2 et P3 fixaient la taille **en entrée**, puis on
cherchait l'actionneur. Or les actionneurs se vendent **par classes
discrètes**, et le couple requis croît avec la masse × la taille. Le
calcul est donc inversé : **pour chaque classe, quelle taille maximale ?**

**Quatre écarts ou réserves, avant tout :**

1. **L'enregistreur de marche est dans `sim/upstream/`, pas dans
   `scripts/`** (V). Il importe `toddlerbot` et tourne avec le venv
   amont, ce que CLAUDE.md (fiche 0004) réserve à `sim/upstream/`.
   L'analyseur, lui, est bien dans `scripts/analyser_marche.py`. La
   série régénérée est **identique** à celle de ce matin (même sha256
   `3de8ca2050a16667…`).
2. **RS02 : la valeur de 6 N·m est retenue sur ta consigne, mais aucune
   source que j'ai pu lire ne la donne** (V).
   - Le PDF constructeur du **2026-09-17** dit encore **7 N·m**, comme la
     fiche du 13-07. La mention « 6 (nouveau) / 5 (ancien) » de ce PDF
     concerne le **RS00**.
   - robstride.com est rendu en JavaScript : je n'ai pas pu le relire.
   - **Les deux valeurs sont portées.** L'enjeu est faible :
     homogène RS02 = 0,789 m à 6 N·m, 0,798 m à 7 N·m (V).
3. **Zeroth-01 : 0,48 m n'a été trouvé dans aucune source** (V). Deux
   sources disent **~0,40 m**. Zeroth-01 a aussi **5 DDL par jambe, pas
   6**, et **aucune marche réelle** n'a été vue, seulement en
   simulation. Le contrôle garde 0,48 m, la valeur la plus exigeante,
   mais c'est une référence **faible** (§ 3).
4. **Toutes les configurations sont des PLAFONDS OPTIMISTES** (V). Le
   roulis de hanche, qui limite presque partout, était écrêté 17 % du
   temps dans la marche P1. Son besoin réel est **au moins** celui
   utilisé, sans qu'on sache de combien il le dépasse.

---

## 1 — Le catalogue

`params/actionneurs.yaml` : chaque valeur y porte son URL ou sa page,
et sa date de consultation (2026-09-30). **Une valeur inconnue ou vue
seulement dans un résumé de recherche est `null`** ; la lecture non
vérifiée est notée à côté.

| Classe | Continu N·m | Pointe N·m | Vitesse à vide rad/s | Masse g | Prix (catalogue) | Bus | Source du continu |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| Feetech STS3250 | 1,57 | 4,90 | 7,87 | 74,5 | **null** | TTL série half-duplex asynchrone | https://www.feetechrc.com/562636.html |
| RobStride EduLite 05 | 1,80 | 5,50 | 45,03 | 242,0 | 80 USD | CAN 2.0 | manuel EL05 260713, p. 9-11 |
| RobStride RS05 | 1,60 | 5,50 | 50,27 | 191,0 | 499 CNY | CAN 2.0 / CAN FD | manuel RS05 260713, p. 10-11 (sha256 1b2c61a6…6360e82) |
| RobStride RS02 | 6,00 | 17,00 | 42,94 | 380,0 | 699 CNY | CAN 2.0 / CAN FD | prompt relayé par Jeremy, auteur non établi (« site RobStride, consulté par Jeremy le 2026-09-30 » jusqu'au 2026-09-30, 23 h 50) |
| RobStride RS06 | 11,00 | 36,00 | 50,27 | 621,0 | 849 CNY | CAN 2.0 / CAN FD | PDF RobStride 2026-09-17, p. 31 |
| RobStride RS03 | 20,00 | 60,00 | 20,42 | 900,0 | 999 CNY | CAN 2.0 / CAN FD | PDF RobStride 2026-09-17, p. 38 |
| CubeMars AK70-10 KV100 | 8,30 | 24,80 | 50,27 | 621,0 | 398,90 USD | CAN et UART | https://www.cubemars.com/goods-1031-AK70-10.html ; https://www.cubemars.com/product/ak70-10-kv100-robotic-actuator.html |

¹ STS3250 : couple **nominal** constructeur, 16 kg·cm, retenu comme continu ;
  la pointe est un couple de **blocage** (50 kg·cm), plafond optimiste de plus.
² EduLite 05 : continu 1,8 N·m et 430 rpm **lus dans le manuel EL05 260713**
  (ils étaient `null` à 17 h 07, vus seulement dans des résumés).
³ RS05 : **1,6 N·m retenu** (manuel 260713, plaque 70 × 70 mm), la plus basse
  de deux valeurs publiées ; 1,8 N·m (PDF du 17-09, plaque 150 × 150 mm) est
  gardé en `autres_valeurs` (fiche 0064 : la valeur la plus prudente).
⁴ RS02 : 6 N·m sur un prompt relayé par Jeremy, auteur non établi ; le PDF constructeur dit 7 (§ 0).
⁵ RS03 : contradiction interne au PDF, 21 à la p. 19 et 20 à la p. 38 : la
  plus basse est retenue.
Les prix de ce tableau sont ceux du champ `prix` du catalogue, que lit le
chiffrage du § 5 ; des prix **revendeur** existent pour plusieurs modèles
(`prix_revendeur`, `comparatif_S`) et servent aux comparatifs, pas ici.

Les vitesses sont **calculées** depuis l'unité d'origine (rpm, s/60°),
jamais saisies. Ce sont des vitesses **à vide** : sous charge, un
actionneur tourne moins vite (Déd).

---

## 2 — Le modèle

### Les équations (Déd)

Référence : ToddlerBot, H0 = 0,56 m. Sa masse M0 = 3,454 kg est la
somme des masses du MJCF (V) ; l'article en annonce 3,4.

| Grandeur | Loi |
| --- | --- |
| masse | masse(H) = S0 · (H/H0)³ + Σ masse **réelle** des 12 actionneurs de jambe |
| structure | S0 = M0 − 12 Dynamixel de jambe (0,708 kg) = **2,746 kg** (V) |
| couple requis | couple_P1 · masse(H)/M0 · H/H0 |
| vitesse requise | vitesse_P1 · (H/H0)^−½ |

S0 contient tout ce qui n'est pas un actionneur de jambe : la structure,
le haut du corps avec ses 18 moteurs, et l'électronique. Tout cela est
mis à l'échelle en similitude.

**Les masses des Dynamixel sont comptées par axe** (V, e-Manual ROBOTIS).
Un seul boîtier 2XC430 de 102 g porte **à la fois** le roulis et le
tangage de hanche : il compte donc pour 51 g par articulation. Le
compter deux fois aurait ajouté 204 g à la masse des moteurs.

**Pourquoi « masse × H » et non H⁴ aveugle** (Déd). Le couple de gravité
vaut m·g·L. Le couple d'inertie I·α vaut m·L²·(1/L) sous une allure de
Froude. Les deux varient comme m·L. H⁴ n'en est que le cas particulier
où m ∝ H³. Ici, la masse des actionneurs ne suit pas H³ : **c'est tout
l'intérêt de la boucle**.

### Les contraintes, par articulation de jambe

| Contrainte | Effet sur H |
| --- | --- |
| marge × RMS requis ≤ couple continu de la classe | borne haute — **sautée si le continu est `null`, et dit** |
| marge × pointe requise ≤ couple de pointe de la classe | borne haute |
| vitesse requise ≤ vitesse de la classe | **borne basse** : un robot plus petit doit tourner plus vite |

Marge = **1,5, décidée par Jeremy** (fiche 0051), à revoir après le banc (`--marge` pour explorer une autre valeur).

### La boucle sur la masse (V)

Le couple dépend de la masse, et la masse dépend de H. **L'itération
naïve H ← f(masse(H)) diverge.** La masse varie en H³, donc
H_k+1 ∝ 1/H_k³, et la dérivée vaut −3 : chaque pas triple l'écart au
lieu de le réduire.

La contrainte, elle, est **monotone** en H. Le script cherche donc par
**dichotomie jusqu'à 0,1 mm**, en recalculant la masse exacte à chaque
H essayé. La masse rapportée est la **masse convergée** à H_max.

### Sensibilité à la marge (V, homogène RS03)

| marge | 1,0 | 1,2 | 1,5 | 2,0 |
| --- | ---: | ---: | ---: | ---: |
| H_max (m) | 1,22 | 1,15 | 1,07 | 0,97 |

---

## 3 — Le contrôle de cohérence

Le calcul doit retrouver deux robots qui existent, dans leur classe, à
**marge 1** (un robot qui marche n'a pas de marge à prouver). S'il ne
les retrouve pas, le script **sort en erreur et ne produit rien** (V).

| Robot | Taille attendue | Classe | H_max calculé | Masse du modèle | Verdict |
| --- | ---: | --- | ---: | ---: | --- |
| ToddlerBot | 0,56 m | ses Dynamixel (bornes de la simulation amont) | **0,560 m** | 3,45 kg | retrouvé |
| Zeroth-01 | 0,48 m (source : ~0,40) | STS3250 | **0,672 m** | 5,64 kg | retrouvé |

**Ce que ce contrôle vaut** (Déd) :

- **ToddlerBot est presque tautologique.** La marche a été simulée avec
  ces bornes et ne peut pas les dépasser, donc H_max tombe pile sur
  0,56 m. Il vérifie l'**arithmétique** (identité à H0, boucle de masse
  qui redonne M0), pas la physique.
- **Zeroth-01 est le seul contrôle indépendant, et il est faible** :
  hauteur non confirmée, 5 DDL par jambe, marche réelle non vue. Un
  point le renforce un peu : **à 0,40 m, le modèle prédit 1,89 kg**,
  proche des ~2 kg annoncés pour Zeroth-01 (valeur non vérifiée).
- **Le test** `tests/test_dimensionnement_coherence.py` prouve que le
  contrôle sait échouer : il refuse un Zeroth-01 de 3 m et un STS3250 de
  0,1 N·m, et il accepte les vraies références. Contrôle neutralisé, le
  test **échoue** sur les deux premiers cas (vu), puis passe une fois le
  contrôle rétabli.

---

## 4 — Taille maximale par classe et par configuration

Marge 1,5. Homogène : la même classe sur les 12 DDL. Mixte « A / B » :
A sur le roulis et le tangage de hanche, le genou et le tangage de
cheville ; B sur le lacet de hanche et le roulis de cheville (consigne de
Jeremy). Seules les paires où A a une pointe plus forte que B sont
calculées.

| Configuration | H max (m) | Masse convergée (kg) | H min vitesse (m) | Articulation limitante | Plafond optimiste ? | Contrainte RMS vérifiée ? |
| --- | ---: | ---: | ---: | --- | --- | --- |
| homogène Feetech STS3250 | 0,60 | 4,2 | 0,17 | hip_roll | **oui** | oui |
| homogène RobStride EduLite 05 | 0,54 | 5,4 | 0,01 | hip_roll | **oui** | oui |
| homogène RobStride RS05 | 0,54 | 4,8 | 0,00 | hip_roll | **oui** | oui |
| homogène RobStride RS02 | 0,79 | 12,2 | 0,01 | hip_roll | **oui** | oui |
| homogène RobStride RS06 | 0,91 | 19,4 | 0,00 | hip_roll | **oui** | oui |
| homogène RobStride RS03 | 1,07 | 30,0 | 0,03 | hip_roll | **oui** | oui |
| homogène CubeMars AK70-10 KV100 | 0,82 | 16,2 | 0,00 | hip_roll | **oui** | oui |
| mixte RobStride EduLite 05 / Feetech STS3250 | 0,57 | 5,1 | 0,06 | hip_roll | **oui** | oui |
| mixte RobStride RS05 / Feetech STS3250 | 0,56 | 4,6 | 0,06 | hip_roll | **oui** | oui |
| mixte RobStride RS02 / Feetech STS3250 | 0,62 | 7,1 | 0,06 | hip_yaw_drive | **oui** | oui |
| mixte RobStride RS02 / RobStride EduLite 05 | 0,63 | 7,9 | 0,01 | hip_yaw_drive | **oui** | oui |
| mixte RobStride RS02 / RobStride RS05 | 0,63 | 7,8 | 0,01 | hip_yaw_drive | **oui** | oui |
| mixte RobStride RS06 / Feetech STS3250 | 0,55 | 7,9 | 0,06 | hip_yaw_drive | **oui** | oui |
| mixte RobStride RS06 / RobStride EduLite 05 | 0,56 | 8,8 | 0,00 | hip_yaw_drive | **oui** | oui |
| mixte RobStride RS06 / RobStride RS05 | 0,57 | 8,6 | 0,00 | hip_yaw_drive | **oui** | oui |
| mixte RobStride RS06 / RobStride RS02 | 0,88 | 17,3 | 0,00 | hip_yaw_drive | **oui** | oui |
| mixte RobStride RS06 / CubeMars AK70-10 KV100 | 0,91 | 19,4 | 0,00 | hip_roll | **oui** | oui |
| mixte RobStride RS03 / Feetech STS3250 | 0,48 | 9,2 | 0,06 | hip_yaw_drive | **oui** | oui |
| mixte RobStride RS03 / RobStride EduLite 05 | 0,49 | 10,0 | 0,03 | hip_yaw_drive | **oui** | oui |
| mixte RobStride RS03 / RobStride RS05 | 0,50 | 9,9 | 0,03 | hip_yaw_drive | **oui** | oui |
| mixte RobStride RS03 / RobStride RS02 | 0,84 | 18,1 | 0,03 | hip_yaw_drive | **oui** | oui |
| mixte RobStride RS03 / RobStride RS06 | 1,09 | 29,7 | 0,03 | hip_roll | **oui** | oui |
| mixte RobStride RS03 / CubeMars AK70-10 KV100 | 0,96 | 23,3 | 0,03 | hip_yaw_drive | **oui** | oui |
| mixte CubeMars AK70-10 KV100 / Feetech STS3250 | 0,55 | 7,9 | 0,06 | hip_yaw_drive | **oui** | oui |
| mixte CubeMars AK70-10 KV100 / RobStride EduLite 05 | 0,56 | 8,8 | 0,00 | hip_yaw_drive | **oui** | oui |
| mixte CubeMars AK70-10 KV100 / RobStride RS05 | 0,57 | 8,6 | 0,00 | hip_yaw_drive | **oui** | oui |
| mixte CubeMars AK70-10 KV100 / RobStride RS02 | 0,84 | 15,8 | 0,00 | hip_roll | **oui** | oui |

### Par articulation, configurations homogènes

H_max que tiendrait **chaque** articulation seule, avec la masse de la
configuration. ⚠ = données P1 écrêtées, donc plafond optimiste.

| Configuration | hip_pitch | hip_roll | hip_yaw_drive | knee | ankle_pitch | ankle_roll |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| homogène Feetech STS3250 | 0,75 ⚠ | 0,60 ⚠ | 0,70 ⚠ | 0,61 ⚠ | 0,62 ⚠ | 0,76 |
| homogène RobStride EduLite 05 | 0,72 ⚠ | 0,54 ⚠ | 0,66 ⚠ | 0,55 ⚠ | 0,56 ⚠ | 0,73 |
| homogène RobStride RS05 | 0,71 ⚠ | 0,54 ⚠ | 0,68 ⚠ | 0,55 ⚠ | 0,59 ⚠ | 0,75 |
| homogène RobStride RS02 | 1,00 ⚠ | 0,79 ⚠ | 0,92 ⚠ | 0,80 ⚠ | 0,80 ⚠ | 1,00 |
| homogène RobStride RS06 | 1,18 ⚠ | 0,91 ⚠ | 1,11 ⚠ | 0,93 ⚠ | 0,97 ⚠ | 1,21 |
| homogène RobStride RS03 | 1,37 ⚠ | 1,07 ⚠ | 1,27 ⚠ | 1,09 ⚠ | 1,10 ⚠ | 1,38 |
| homogène CubeMars AK70-10 KV100 | 1,08 ⚠ | 0,82 ⚠ | 0,99 ⚠ | 0,84 ⚠ | 0,85 ⚠ | 1,08 |

### Lecture (Déd)

- **Le palier P2 (0,90 m) n'est tenu, en homogène, que par le RS06
  (0,91 m, de justesse) et le RS03 (1,07 m).** Le RS02 plafonne à
  0,79 m et l'AK70-10 à 0,82 m. Les classes légères (STS3250, EduLite
  05, RS05) restent sous 0,60 m.
- **Le roulis de hanche limite toutes les configurations homogènes.**
  C'est aussi l'articulation la plus écrêtée en P1 : les chiffres les
  plus décisifs sont donc les moins sûrs.
- **Le découpage mixte demandé est souvent contre-productif.** Il met la
  classe légère sur le lacet de hanche. Or celui-ci a une pointe P1
  élevée (1,44 N·m, écrêtée 11 % du temps), et il doit porter la masse
  ajoutée par la classe lourde. Résultat : mixte RS03 / STS3250 =
  **0,48 m**, contre 0,60 m en STS3250 homogène.
- **Le lacet de hanche dans le groupe lourd** a été calculé depuis pour L
  (configuration nommée `L_rs06_rs02`, cadrage § 5) : 0,92 m, contre 0,91 m
  en RS06 homogène. Les autres paires restent à calculer (cadrage,
  question 3).
- La contrainte de vitesse ne borne presque rien. Seuls le STS3250 et les
  mixtes qui l'emploient imposent une taille minimale, vers 0,06 à
  0,17 m.

---

## 5 — Budget par phase

`params/budget.yaml`. Coût TTC = (actionneurs + électronique + structure)
× (1 + imprévus) × (1 + TVA).

| Paramètre | Valeur | Source |
| --- | --- | --- |
| TVA CH | 8,1 % | prompt relayé par Jeremy, auteur non établi ; la page de l'AFC n'a pas pu être ouverte |
| imprévus | **15 %, provisoire** | **à fixer par Jeremy** — visible dans chaque total |
| change | 1 EUR = 0,9478 CHF = 1,1355 USD = 7,6130 CNY | BCE, référence du 2026-09-30 ; les taux croisés sont calculés |
| structure | **null** | tant que l'opérateur CN n'a pas chiffré |

| Phase | Contenu |
| --- | --- |
| banc | 2 × RS05 et 1 adaptateur USB-CAN, quelle que soit la configuration étudiée : thermique réelle, deux adresses sur un même bus, segment à 2 DDL de l'échelon 1, et une rechange. *Statut : OPTION, en attente du comparatif (docs/comparatif-banc.md ; cadrage § 6 et § 13)* |
| jambes_v1 | 12 actionneurs + adaptateur + Raspberry Pi 5 + IMU BNO085 + batterie + structure |
| haut_du_corps_v2 | 18 actionneurs de la classe légère + structure |

| Configuration | H max (m) | banc TTC (CHF) | jambes_v1 TTC (CHF) | haut_du_corps_v2 TTC (CHF) | Postes inconnus |
| --- | ---: | ---: | ---: | ---: | --- |
| homogène Feetech STS3250 | 0,60 | 209 | ≥ 432 | inconnu | prix Feetech STS3250, structure |
| homogène RobStride EduLite 05 | 0,54 | 209 | ≥ 1 472 | ≥ 1 494 | structure |
| homogène RobStride RS05 | 0,54 | 209 | ≥ 1 403 | ≥ 1 390 | structure |
| homogène RobStride RS02 | 0,79 | 209 | ≥ 1 774 | ≥ 1 947 | structure |
| homogène RobStride RS06 | 0,91 | 209 | ≥ 2 053 | ≥ 2 365 | structure |
| homogène RobStride RS03 | 1,07 | 209 | ≥ 2 332 | ≥ 2 783 | structure |
| homogène CubeMars AK70-10 KV100 | 0,82 | 209 | ≥ 5 443 | ≥ 7 451 | structure |
| mixte RobStride EduLite 05 / Feetech STS3250 | 0,57 | 209 | ≥ 1 140 | inconnu | prix Feetech STS3250, structure |
| mixte RobStride RS05 / Feetech STS3250 | 0,56 | 209 | ≥ 1 094 | inconnu | prix Feetech STS3250, structure |
| mixte RobStride RS02 / Feetech STS3250 | 0,62 | 209 | ≥ 1 342 | inconnu | prix Feetech STS3250, structure |
| mixte RobStride RS02 / RobStride EduLite 05 | 0,63 | 209 | ≥ 1 674 | ≥ 1 494 | structure |
| mixte RobStride RS02 / RobStride RS05 | 0,63 | 209 | ≥ 1 651 | ≥ 1 390 | structure |
| mixte RobStride RS06 / Feetech STS3250 | 0,55 | 209 | ≥ 1 527 | inconnu | prix Feetech STS3250, structure |
| mixte RobStride RS06 / RobStride EduLite 05 | 0,56 | 209 | ≥ 1 859 | ≥ 1 494 | structure |
| mixte RobStride RS06 / RobStride RS05 | 0,57 | 209 | ≥ 1 836 | ≥ 1 390 | structure |
| mixte RobStride RS06 / RobStride RS02 | 0,88 | 209 | ≥ 1 960 | ≥ 1 947 | structure |
| mixte RobStride RS06 / CubeMars AK70-10 KV100 | 0,91 | 209 | ≥ 3 183 | ≥ 7 451 | structure |
| mixte RobStride RS03 / Feetech STS3250 | 0,48 | 209 | ≥ 1 713 | inconnu | prix Feetech STS3250, structure |
| mixte RobStride RS03 / RobStride EduLite 05 | 0,49 | 209 | ≥ 2 045 | ≥ 1 494 | structure |
| mixte RobStride RS03 / RobStride RS05 | 0,50 | 209 | ≥ 2 022 | ≥ 1 390 | structure |
| mixte RobStride RS03 / RobStride RS02 | 0,84 | 209 | ≥ 2 146 | ≥ 1 947 | structure |
| mixte RobStride RS03 / RobStride RS06 | 1,09 | 209 | ≥ 2 239 | ≥ 2 365 | structure |
| mixte RobStride RS03 / CubeMars AK70-10 KV100 | 0,96 | 209 | ≥ 3 369 | ≥ 7 451 | structure |
| mixte CubeMars AK70-10 KV100 / Feetech STS3250 | 0,55 | 209 | ≥ 3 788 | inconnu | prix Feetech STS3250, structure |
| mixte CubeMars AK70-10 KV100 / RobStride EduLite 05 | 0,56 | 209 | ≥ 4 120 | ≥ 1 494 | structure |
| mixte CubeMars AK70-10 KV100 / RobStride RS05 | 0,57 | 209 | ≥ 4 097 | ≥ 1 390 | structure |
| mixte CubeMars AK70-10 KV100 / RobStride RS02 | 0,84 | 209 | ≥ 4 220 | ≥ 1 947 | structure |

**Options de phase** (`params/budget.yaml`, `phases.*.options`) :

| Option | Statut | TTC CH (CHF), imprévus compris | Postes inconnus | Non chiffré |
| --- | --- | ---: | --- | --- |
| banc:verification | proposé | 386 | — | alimentation du banc : un OUTILLAGE (limitation de courant réglable), décision de Jeremy (règle d'achat b) |

**« ≥ » veut dire que le total est incomplet** : un poste au moins est
inconnu, et la colonne de droite le nomme. Aucun total n'est complet
aujourd'hui, puisque la structure n'est pas chiffrée.

**Ce que ces coûts ne disent pas** (Déd) :

- **Les prix RobStride sont des prix constructeur en yuans**, hors
  export, port et droits de douane. **Un prix rendu en Suisse sera plus
  élevé**, d'un montant inconnu.
- **La batterie 6S (22,2 V) ne correspond pas à la tension des
  caractéristiques** : 48 V pour RobStride et CubeMars, 12 V pour
  Feetech. La vitesse d'un actionneur baisse avec sa tension. Une
  batterie adaptée à chaque bus n'est pas chiffrée.
- **L'alimentation du banc n'est plus comptée** : c'est un outillage à
  limitation de courant réglable, décision de Jeremy (règle d'achat b ;
  `docs/protocole-banc.md` § 1.1). La PeakTech 30 V du budget ne convient
  pas à un actionneur 48 V.
- La phase haut du corps utilise la classe légère de la configuration :
  c'est une convention de calcul, pas un choix.
- Ni port, ni douane, ni visserie, ni câblage, ni connecteurs, ni
  outillage : ils ne sont pas nuls, ils sont **inconnus**.

---

## Ce que ce document ne dit pas

- **Le besoin réel des articulations écrêtées**, surtout le roulis de
  hanche. Sans lui, chaque H_max reste un plafond.
- **La tenue thermique.** Le RMS est comparé au couple continu du
  constructeur, qui est mesuré dans des conditions précises (100 rpm,
  plaque d'aluminium de 150 ou 200 mm). Ce n'est pas le rapport
  cyclique de la marche (fiche 0038).
- **Une autre allure que la marche droite à 0,10 m/s** : ni virage, ni
  relevé, ni perturbation.
- **Un choix.** Les tailles sont décidées par classe (fiche 0048), mais
  les paliers d'`anthropometry.yaml` ne sont pas encore remplacés (cadrage,
  question 8). La famille d'actionneurs de S n'est pas décidée
  (`docs/choix-famille-actionneurs.md`).
