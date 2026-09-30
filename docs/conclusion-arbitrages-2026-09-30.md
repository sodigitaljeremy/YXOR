> **Remplacée par `docs/arbitrage-2026-09-30.md` ; conservée pour garder visible la recommandation faussée par la notation 24 V.** (Versée le 2026-09-30, 23 h, option (b) validée par Jeremy ; texte ci-dessous inchangé.)

# Conclusion des arbitrages — 29 et 30 septembre 2026

**Rédigé par Claude (arbitrage), à verser dans le dépôt sous
`docs/conclusion-arbitrages-2026-09-30.md`.** Ce document résume ce qui a
été choisi, pourquoi, et ce qui reste à trancher. Il ne remplace pas le
cadrage (`docs/cadrage.md`), qui porte le raisonnement détaillé, ni les
comparatifs engendrés, qui portent les chiffres. En cas d'écart, **les
documents engendrés par les scripts font foi**.

Statuts :

- **DÉCIDÉ** : tranché par Jeremy ;
- **RECOMMANDÉ** : proposé par Claude, soutenu par les comparatifs, **en
  attente de la validation de Jeremy** ;
- **OUVERT** : non instruit ou non tranché.

---

## 1. En une phrase

YXOR ne choisit plus sa taille d'abord : **la classe d'actionneur fixe la
taille**. Le premier robot sera **S (≈ 0,55–0,65 m)**. Les données publiques
désignent la **famille Damiao** pour S, avec **RobStride** en repli. Un
**banc de vérification** à deux actionneurs doit confirmer ce choix avant
tout achat en quantité, selon un **critère d'abandon écrit avant la
mesure**.

---

## 2. Le fil des arbitrages

1. **Le carton a rempli son rôle.** La semelle d'apprentissage a validé la
   chaîne complète : paramètre, plan, découpe, vérification. La
   caractérisation du carton est arrêtée : ses valeurs ne se transfèrent
   pas au robot réel.
2. **Les contrôles doivent dire la vérité** (lot A). Quand un document
   promet un contrôle qui n'existe pas, on corrige la promesse. Chaque
   contrôle touché a reçu un test qui prouve qu'il sait échouer.
3. **La taille était une entrée, elle devient une sortie.** Les actionneurs
   se vendent par classes discrètes et le couple requis croît très vite
   avec la taille. On calcule donc la taille maximale de chaque classe.
4. **Le budget se construit à partir du marché**, par phase, et non plus a
   priori.
5. **Les fiches techniques ne sont pas comparables entre elles.** Chaque
   fabricant mesure son couple continu dans ses propres conditions. Trois
   biais successifs ont été corrigés, chacun pénalisant celui qui publiait
   le plus.
6. **On compare des familles, pas des modèles.** Le choix engage S, puis M,
   puis L.
7. **Une mesure ne vaut que si elle peut changer la décision.** Une fois les
   biais corrigés, les données publiques désignent la même famille sur
   toute la plage plausible. Le banc devient une vérification.

---

## 3. Arbitrages DÉCIDÉS

| Arbitrage | Pourquoi | Trace |
| --- | --- | --- |
| Caractérisation du carton arrêtée ; fiches 0042 et 0044 closes | Valeurs non transférables au robot réel | Journal du 30-09 |
| Moratoire sur les fiches **rejeté** | Choix de Jeremy | Cadrage § 12 |
| Lot A : corriger la promesse, pas construire le contrôle | Des documents promettaient des contrôles inexistants | Journal du 30-09 |
| Empreinte du site sans le Dockerfile | Coolify le réécrit ; hypothèse confirmée par l'expérience | `scripts/empreinte.py` |
| Date d'extraction conservée dans `upstream_joints.generated.yaml` | Elle fait partie de la provenance (fiche 0006) | Journal du 30-09 |
| **Démarche inversée** : la classe d'actionneur fixe la taille | Classes discrètes, couple ∝ masse × taille | Fiche 0047 |
| **Tailles Banc, S, M, L, XL ; premier robot S** | S est la moins chère pour franchir toute l'échelle des capacités | Fiche 0048 |
| Scripts de chiffrage versionnés | Refaire le calcul quand les hypothèses changent | Fiche 0049 |
| **Fabrication séquencée** : usinage, puis impression, puis hybride | Comprendre chaque procédé | Fiche 0050 |
| **Marge de sécurité 1,5** sur les couples | Simulation optimiste, pointes écrêtées ; à revoir après le banc | Fiche 0051 |
| **Actionneur maison** en piste parallèle, jamais sur le chemin critique | Apprendre sans bloquer le robot | Fiche 0052 |
| **Poids du comparatif** : capacité 18, continuité 18, coût 15, fiabilité 15, robustesse 12, disponibilité 7, masse 5, ouverture 5, tension 5 | Équilibre entre préparer M/L et un S convaincant | `params/criteres_selection.yaml` |
| **Règle de décisivité étendue** | Une inconnue ne compte que si son issue peut changer la décision de famille | idem |
| Correction de la note du catalogue sur le J4310 | L'estimation thermique contredit « pas un régime établi » | `params/actionneurs.yaml` |

---

## 4. Arbitrages RECOMMANDÉS, en attente de Jeremy

### 4.1 Famille d'actionneurs pour S : Damiao J4310 V1.2 en 48 V

**Ce que disent les données** (`docs/choix-famille-actionneurs.md`) :

| Famille (S → M → L) | Taille S (prudent–optimiste) | Jambes S (CHF TTC, ≥) | Continuité | Remarque |
| --- | --- | ---: | ---: | --- |
| **Damiao** (J4310 → J8006 → J4340) | 0,38–0,67 m | 2 354 | 5/5 | en tête sur toute la plage plausible |
| RobStride (RS05 → RS02 → RS06) | 0,48–0,57 m | 1 846 | 5/5 | seule famille dont le couple au blocage est publié |
| RobStride, S = EduLite 05 | 0,27–0,54 m | 1 472 | 5/5 | la moins chère, la moins documentée |
| CubeMars (AK45 → AK80 → AK10) | 0,33–0,61 m | 2 417 | 5/5 | M et L très chers (≥ 6 452 et ≥ 9 179) |
| MyActuator (X2-7 → trou → X4-36) | 0,33–0,61 m | 4 717 | 2/5 | aucun modèle CAN actuel en classe M |

Tailles à marge 1,5, bornes basses calculées à k = 0,3.

**Pourquoi Damiao :**

- **La bascule vers RobStride n'a lieu que si k < 0,49.** k est le rapport
  entre le couple continu réel et le couple nominal publié.
- **La borne basse plausible de k est 0,619** : c'est le plus petit rapport
  entre couple au blocage et couple nominal publié par RobStride (0,619 à
  0,857, moyenne 0,718).
- **L'estimation thermique du J4310** donne k ≈ 0,92–1,02 en rotation.
  Décotée au blocage par les rapports RobStride, elle donne 0,57–0,87.
  C'est une hypothèse sur une hypothèse, mais elle reste au-dessus de la
  bascule.

**Pourquoi en 48 V** : une seule tension de S à L, et le repli vers RobStride
(48 V) garde la même alimentation.

**Limites assumées :**

- aucune garantie écrite trouvée chez Damiao ; J4310 surtout utilisé dans
  des bras ;
- **le membre L de Damiao (J4340, 40:1) est probablement peu réversible**,
  ce qui est défavorable aux chocs d'une jambe. C'est une question ouverte,
  à rouvrir avant L, sans effet sur S ;
- une couche logicielle indépendante du fabricant rendrait ce choix
  réversible pour M et L (§ 4.5).

### 4.2 Banc de vérification : 2 × J4310 V1.2 48 V et un adaptateur USB-CAN

- **Rôle : vérifier, pas départager.** Aucune inconnue n'est décisive dans
  la plage plausible (`docs/comparatif-banc.md`).
- **Contenu** : échelon 0 (un actionneur piloté, mesuré), segment à 2 degrés
  de liberté de l'échelon 1, deux adresses sur le même bus, premier ordre de
  grandeur de la dispersion entre exemplaires.
- **Coût : ≈ 386 CHF TTC**, imprévus de 15 % compris, **hors alimentation**.
  Prix OpenELAB incertain : TVA incluse ou non, précommande possible, prix
  barré à 172,95 €, port et douane non compris.
- **Si Damiao se confirme, chaque moteur du banc finira dans une jambe de
  S** : c'est une avance sur le budget de S, pas une dépense à part.
- Variante à 3 exemplaires : une rechange et une dispersion un peu plus
  parlante, pour un risque à peine plus grand.

### 4.3 Critère d'abandon, écrit avant la mesure

> Si le couple continu du J4310, mesuré **au blocage** sur une plaque
> d'aluminium de 70 × 70 mm, est inférieur à **1,75 N·m** (0,5 × 3,5), le
> choix de famille est **rouvert** vers RobStride.

- Il s'applique à la borne haute de l'intervalle mesuré et au plus faible
  des deux exemplaires. Si 1,75 N·m tombe dans l'intervalle, on ne conclut
  pas : on réduit l'incertitude d'abord.
- « Rouvert » veut dire que le comparatif est relancé avec la mesure, pas
  que la famille change d'office.

### 4.4 Cohérences à appliquer

- La note de **transfert à S** des options « × J4310 » passe de 3 à 5 : elle
  valait 3 parce que k était inconnu, mais k n'est plus décisif.
- Les options J4310 du comparatif du banc sont chiffrées en 24 V : elles
  doivent être alignées sur 48 V.

### 4.5 Interfaces d'actionneur (`docs/choix-interfaces.md`)

- **Logiciel** : une couche indépendante du fabricant
  (`joint.command(position, vitesse, couple)`), un backend par fabricant et
  un backend simulé MuJoCo. Coût faible, gain élevé, démarrable **avant tout
  achat**. Reste à choisir entre une couche propre, `ros2_control`, ou une
  couche propre alignée sur les concepts de `ros2_control`.
- **Mécanique** : interface YXOR et adaptateur par modèle, **à décider une
  fois un actionneur en main**, charges admissibles du roulement de sortie
  connues. L'adaptateur en aluminium participe aussi au refroidissement.

### 4.6 Vision (cadrage § 1)

Proposée depuis le 30-09, jamais validée.

---

## 5. OUVERT

1. **L'alimentation du banc**, qui doit être à limitation de courant réglable.
   C'est de l'outillage, donc la décision de Jeremy. L'alimentation chiffrée
   au budget ne remplit pas cette condition.
2. **Ce que S doit porter** (calculateur, batterie, centrale inertielle) :
   non chiffré. C'était la vraie contrainte derrière le seuil de taille
   retiré.
3. **La structure** : chiffrage de l'opérateur CN (procédé exact, rayons, matières,
   format de fichier) et coût de l'impression.
4. **La batterie** à la tension retenue (48 V).
5. **Les paliers P1/P2/P3** d'`anthropometry.yaml`, à remplacer par les
   tailles, par une fiche qui remplace sans réécrire.
6. **Les fiches 0014 et 0015**, contredites par la fabrication séquencée
   (fiche 0050), à remplacer de la même façon, ainsi que la section
   fabrication de CLAUDE.md.
7. **L'immuabilité des fiches** : ne plus réécrire une fiche acceptée.
8. **Les espèces qui sont des états** dans la taxonomie des fiches.
9. **La licence des valeurs numériques extraites de ToddlerBot** : question
   juridique, sans avis.
10. **Le simulateur JavaScript du site** n'a jamais été vu fonctionner.
11. **Le blocage réseau** de WSL (Chromium, vérification de mise à jour) :
    constat sans diagnostic.
12. **Le membre L de la famille Damiao** (§ 4.1).

---

## 6. Prochaines étapes, dans l'ordre

1. Jeremy valide ou amende les recommandations du § 4. Chaque décision
   reçoit sa fiche.
2. Commande : vérifier auprès du vendeur la disponibilité de la V1.2 en
   48 V, la TVA et le délai. Choisir l'alimentation de laboratoire.
3. Pendant la livraison : la couche logicielle et son backend MuJoCo.
4. Réception : protocole de banc (`docs/protocole-banc.md`), sécurité
   d'abord, puis la mesure au blocage et le critère d'abandon.
5. Si le critère ne se déclenche pas : fiche « famille confirmée », puis le
   segment à 2 degrés de liberté de l'échelon 1.

---

## 7. Ce que la journée a appris sur la méthode

- **Un seuil arbitraire se cache partout.** L'éliminatoire de 0,55 m, retiré,
  survivait dans la grille de capacité. Il a fallu le traquer deux fois.
- **Une règle peut favoriser celui qui publie le moins.** Trois corrections
  successives l'ont montré. La bonne règle traite tous les candidats de la
  même façon.
- **Une analyse de sensibilité peut ne regarder que les poids**, alors que
  l'incertitude principale était dans les données.
- **Une mesure ne vaut que si elle peut changer la décision.**
- **Écrire le critère d'abandon avant la mesure** empêche de réinterpréter
  le résultat après coup.
- **Attribuer une décision à la mauvaise personne est une erreur de
  traçabilité** : les poids du banc ont été enregistrés « fixés par Jeremy »
  alors qu'il posait encore la question. Corrigé, et l'erreur reste visible.
- **Les erreurs de Claude, relevées par Claude Code ou par la relecture** :
  le seuil de 0,55 m, la grille de capacité, l'exposant de la marge (−¼
  au lieu de −⅓), un cumul de budget, un « calcul en cours » qui n'existait
  pas, la date du 30 au lieu du 29, la licence BY-NC au lieu de BY-NC-SA.
  Toutes sont corrigées et tracées.