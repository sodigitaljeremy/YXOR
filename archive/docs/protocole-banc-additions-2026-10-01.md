# Protocole du banc — ajouts proposés

**Rédigé le 2026-10-01.** Statut : **PROPOSÉ par Claude (arbitrage,
2026-10-01)**, d'après l'audit externe ChatGPT du 2026-10-01 (texte non
versé au dépôt) et la collecte de la nuit
(`params/actionneurs.yaml`, `collecte_criteres_manquants`).

**`docs/protocole-banc.md` n'est pas modifié.** Ces ajouts y entreront
seulement si Jeremy les valide. Aucun achat n'est proposé : quand un
ajout suppose un objet (fusible, carter, capteur), c'est un **outillage**,
donc la décision de Jeremy (règle d'achat b).

---

## 0 — Un préalable : le chien de garde (E1)

**À placer dans le § 1.3 du protocole, parmi les conditions à remplir
avant toute mise sous tension de puissance.**

*Ce que c'est.* Le chien de garde de communication coupe l'actionneur
s'il ne reçoit plus de consigne pendant un délai donné. Sans lui, un PC
qui plante ou un câble CAN qui se débranche laisse l'actionneur
**exécuter sa dernière consigne indéfiniment**, par exemple un couple
au blocage.

**Ce que la collecte a trouvé** :

| Actionneur | Mécanisme | Valeur d'usine |
| --- | --- | --- |
| RobStride RS05 / EduLite 05 | `CAN_TIMEOUT` (0x7028), 20 000 = 1 s | **0 = désactivé** |
| SteadyWin GIM4310 (GDZ34) | 0xCD | **désactivé**, réglage perdu à la coupure d'alimentation |
| Damiao J4310 | `TIMEOUT` (0x09), unité de 50 µs | non publiée |
| MyActuator X2-7 | 0xB3, en ms, gardé en ROM | non publiée ; 0 = désactivé |

**Proposition :**

1. **Lire** la valeur d'usine, et la consigner dans `params/mesures.yaml`.
2. **La régler à une valeur non nulle**, de quelques périodes de la
   boucle de commande. La valeur est à fixer par Jeremy : ce document
   n'en propose aucune (§ 4).
3. **La vérifier à vide**, moteur activé à couple nul : débrancher le
   câble CAN, et constater la coupure dans le délai réglé.
4. **Après chaque coupure d'alimentation**, la relire. Chez SteadyWin,
   le réglage est perdu à la coupure.

**Tant que ces quatre points ne sont pas faits, on ne met pas sous
tension de puissance.**

---

## 1 — Alimentation et câblage

| Ajout | Pourquoi | Ce qu'il faut écrire au protocole |
| --- | --- | --- |
| **Fusible DC près de la source** | Si un câble se court-circuite, c'est le fusible qui fond, pas le câble ni la piste du pilote. Le placer près de la source protège toute la longueur en aval | calibre et type (pour courant continu, à la tension du bus), position : en sortie immédiate de l'alimentation |
| **Consignation, et décharge du bus avant recâblage** | Les pilotes ont des condensateurs qui restent chargés après la coupure. « Consigner », c'est couper, **empêcher la remise sous tension** (interrupteur verrouillé, étiquette) et **vérifier l'absence de tension** | séquence : couper, verrouiller, attendre ou décharger, mesurer Vbus ≈ 0 V au multimètre, **puis** recâbler. Le § 1.6 interdit déjà de recâbler sous tension ; ceci le rend vérifiable |
| **Contrôle de la polarité et de la masse** | Une inversion de polarité peut détruire un pilote à la première mise sous tension. Une masse commune absente entre l'adaptateur USB-CAN et le pilote fausse ou casse la communication | vérifier au multimètre, **avant** la première mise sous tension de chaque montage ; consigner la vérification |
| **Précharge, si nécessaire** | Brancher un bus de 48 V sur des condensateurs vides fait un **appel de courant** (étincelle au connecteur, contacts abîmés, déclenchement de protection). Damiao recommande d'éviter le branchement à chaud au-dessus de 36 V | d'après la notice de chaque pilote : précharge par résistance, ou montée progressive de la tension sur l'alimentation de laboratoire |
| **Journaliser Vbus** | La tension du bus monte quand le moteur **freine**, parce qu'il renvoie de l'énergie (régénération). Une surtension déclenche la protection, ou abîme l'alimentation | Vbus relevée à 1 Hz, avec les autres grandeurs du § 2.6. Seuil d'arrêt sous la surtension constructeur (60 V chez RobStride) |

---

## 2 — Mécanique du bras de levier

| Ajout | Pourquoi | Ce qu'il faut écrire |
| --- | --- | --- |
| **Carter rigide autour du bras** | Le § 1.4 borne la course par des butées. Un carter arrête **aussi** une pièce qui se détache (vis, bras cassé) | matière et épaisseur, fixation au bâti ; le bras doit pouvoir être vu au travers ou par-dessus |
| **Serrage spécifié** | Une vis de bride sous-serrée glisse ou se desserre ; sur-serrée, elle arrache le taraudage du carter de l'actionneur, souvent en aluminium tendre | couple de serrage de chaque vis (bride de sortie, plaque), en N·m, d'après la documentation constructeur, ou à défaut celle de la vis ; frein filet ou rondelle, si prévu |
| **Étalonnage et tare du capteur d'effort** | Un dynamomètre non taré ajoute son décalage à chaque mesure. Un capteur non étalonné donne une valeur fausse, avec l'air d'être juste | tare à vide avant chaque session ; vérification avec une **masse connue**, à la longueur du bras ; consigner la masse et l'écart |
| **Position du thermocouple** | La température du carter dépend de l'endroit mesuré, près du bobinage ou près de la plaque. Changer d'endroit change la mesure | position **décrite et photographiée**, la même pour tous les exemplaires ; moyen de fixation (colle thermique, ruban kapton) |

---

## 3 — Conduite de l'essai

| Ajout | Pourquoi | Ce qu'il faut écrire |
| --- | --- | --- |
| **Arrêt si une télémétrie critique disparaît** | Si la température ou le courant ne remontent plus, on ne sait plus si l'actionneur chauffe. Continuer à l'aveugle, c'est exactement le risque du rotor bloqué (§ 1.5) | liste des grandeurs critiques : température du bobinage, température du pilote, courant, Vbus ; arrêt **logiciel immédiat** si l'une manque plus d'une seconde ; arrêt d'urgence matériel en secours |
| **Séquence de mise en route** | Chaque étape vérifie une hypothèse avant de risquer plus d'énergie | dans cet ordre, sans en sauter : **(1)** activation à **couple nul** ; **(2)** **faible courant** (consigne basse, limite de courant basse) ; **(3)** **sens de rotation vérifié** par rapport au signe de la consigne et au codeur ; **(4)** **montée progressive** vers les paliers du § 2 |

---

## 4 — Ce que ces ajouts ne règlent pas

- **Aucune valeur n'est fixée ici** : délai du chien de garde, calibre du
  fusible, couple de serrage, seuil de Vbus. Chacune se fixe d'après la
  notice de l'actionneur choisi, ou par Jeremy.
- **La composition du banc n'est pas décidée** (`params/banc.yaml`).
  Certains ajouts dépendent du pilote : la précharge, l'unité du chien
  de garde.
- **La seconde personne** du § 1.6 n'est toujours pas identifiée dans le
  dépôt.
