# Arbitrage — état des lieux YXOR au 2026-09-30

**Rédigé par Claude (arbitrage) le 2026-09-30 au soir.** Destination
proposée : `docs/arbitrage-2026-09-30.md`. Le sort de
`docs/conclusion-arbitrages-2026-09-30.md` (jamais commité) est confié à
Claude Code, qui le proposera (prompt P2, § 9).

**Sources, et ce que chacune peut voir :**

| Source | Ce qu'elle voit | Ce qu'elle ne voit pas |
| --- | --- | --- |
| **Conv.** : conversations du projet « Robot » (5 août, ≈ 20–29 sept., 30 sept.) relues par recherche | ce qui a été dit, décidé à l'oral, puis abandonné | le dépôt |
| **CC** : rapport de Claude Code, `docs/etat-des-lieux-2026-09-30.md`, commit `2e726e8` | le dépôt, exécuté | les conversations |
| **GPT** : audit externe de ChatGPT du 30-09 | le web, le brief | **ni le dépôt** (privé, 404) **ni le site** |
| **Corpus** : thèse Forget ch. 5, recherche web ciblée du 30-09 au soir | faits vérifiables | — |

Le dépôt GitHub est **privé**. Je n'ai pas pu le lire non plus. Chaque fait
« dépôt » ci-dessous vient donc du rapport CC. Le site `yxor.fr` répond,
avec l'empreinte `de10401722`, 1 pièce et 3 035 valeurs.

**Statuts.** **DÉCIDÉ** : tranché par Jeremy, avec la trace citée.
**PROPOSÉ** : jamais validé. **OUVERT** : non instruit. **ABANDONNÉ** :
retiré, avec le motif. **À CONFIRMER** : je n'ai pas retrouvé la parole de
Jeremy qui le tranche.

---

## 1. Où en est YXOR, en 10 lignes

1. YXOR est un humanoïde bipède autonome à IA embarquée. Il n'a qu'**une pièce physique**, une semelle d'apprentissage en carton, sans interface avec rien d'autre.
2. La **méthode** existe et fonctionne : dépôt régénérable, traçabilité (3 035 valeurs), site, simulation amont qui marche. **Le robot n'a pas commencé.**
3. Le 30-09, Jeremy a inversé la démarche : **la classe d'actionneur fixe la taille**. Le premier robot sera **S**, vers 0,55–0,60 m, avec une marge de **1,5**.
4. La **famille d'actionneurs de S n'est pas décidée**. Damiao J4310 était recommandé, mais sa notation reposait sur la **variante 24 V** et non sur la 48 V retenue.
5. Recalculée en 48 V, l'avance de Damiao sur RobStride n'est plus que de **0,009** sur k. Par la propre règle du projet, **le banc doit à nouveau départager**, et plus seulement vérifier.
6. Le **critère d'abandon** (1,75 N·m au blocage) est à recalculer (≈ 2,14–2,17 N·m en 48 V) et à compléter par un critère fondé sur le besoin des articulations.
7. **Aucune mise sous tension n'est possible en sécurité** : aucune alimentation à courant limité, ni arrêt d'urgence matériel, ni dynamomètre chiffrés, et l'adaptateur CAN n'est pas conforme CE.
8. La gouvernance est en baisse relative : de **66 % à 57 %** des lignes. Mais plusieurs fiches se contredisent sans se remplacer, et `CLAUDE.md` décrit encore le projet d'avant le 30-09.
9. Les **trois sources concordent sur l'essentiel** : ne rien commander avant le recalcul et le protocole de sécurité.
10. Prochaine action : recalculer le comparatif en 48 V (prompt P1), puis trancher le rôle et la composition du banc.

---

## 2. Chronologie

| Date | Jalon | Source |
| --- | --- | --- |
| **5 août** | Premier cadrage. Androïde taille adulte, 500–2 000 €. Claude juge le bipède hors budget et recommande un **buste**, sur **Berkeley Humanoid Lite**, avec LeRobot/GR00T, Jetson Orin NX, Pi 5 et Teensy/STM32 sur CAN. Accès à une **imprimante 3D gratuite** déclaré. Le trio est défini. | Conv. 5 août |
| août | YXOR est décrit comme un passe-temps non prioritaire. | mémoire |
| sept. (date exacte inconnue) | **Réorientation** : bipède, nom YXOR, nouveau dépôt, aucune reprise de l'ancien projet. Mise à l'échelle en paliers P1 ≈ 0,56 m, P2 ≈ 0,85–1,00 m, P3 ≈ 1,70 m. | Conv. sept. |
| **≈ 20 sept.** | **Fiche 0001 : ToddlerBot comme base.** C'est Jeremy qui le propose. Claude objecte sur le prix, puis se rallie : aux étapes 1 et 2, on n'achète rien. Fiche 0002 : amont cloisonné, épinglé à `e337f3b`. | Conv. ; fiche 0001 datée 2026-09-20 |
| sept. | **« Arrête tout »** : Jeremy ne comprend plus la codebase. Objectif refixé : **l'appropriation avant la production**. | Conv. |
| sept. | Découverte : **pas d'imprimante 3D**. Moyens réels : cutter, laser de fablab, découpe métal 2D chez l'opérateur CN, soudure. | Conv. |
| sept. | CAO en code (build123d), modèle procédés en quatre tables DIN 8580, corpus (Kajita, Forget, Nenchev, ANSUR II), refonte des fiches 33–40, premier audit trouvé **« vert mais faux »**. | Conv. |
| 28 sept. | Domaine `yxor.fr`, déploiement Coolify sur Hetzner. | mémoire |
| **29 sept., soir** | **Semelle coupée** (dessinée à P2, H = 0,90 m). Saignée nulle prédite par la fiche 0026, vérifiée. | Conv. ; CC |
| 29 sept., nuit | Premier audit exhaustif de CC : 66 % de gouvernance, 8 valeurs sur 1 440 gouvernent une forme. | Conv. |
| **30 sept.** | Double cannelure confirmé. **Lot A** clôturé (licence BY-NC-SA, déterminisme, empreinte, 5 tests). **Pivot carton** : caractérisation arrêtée, fiches 0042 et 0044 closes. **Moratoire rejeté** par Jeremy. | Conv. |
| 30 sept. | Exigences d'actionnement (P2), dimensionnement inversé, recherche d'actionneurs, `docs/cadrage.md` rédigé par Claude, fiches **0047 à 0052**. | Conv. ; CC |
| 30 sept. | Choix de famille (Damiao en tête), comparatif du banc, estimation thermique du J4310, règle de décisivité étendue. Claude recommande « commencer avec le vainqueur ». **Les trois questions (famille, banc, critère) restent sans réponse.** | Conv. tours 49–50 |
| 30 sept., 21 h 49 | Audit de CC → rapport `2e726e8`. Constat critique : **Damiao noté en 24 V**. | CC |
| 30 sept. | Audit externe de ChatGPT : red team contre le J4310, banc à huit portes. | GPT |

**Trou de mémoire.** Entre le 5 août et le ≈ 20 septembre, il n'existe aucune
conversation YXOR dans ce projet. Pour la réorientation, seule la mémoire
résumée en témoigne ; sa date exacte est inconnue.

---

## 3. Décisions

### 3.1 DÉCIDÉ

| Décision | Par | Quand | Pourquoi | Alternative écartée | Trace |
| --- | --- | --- | --- | --- | --- |
| Bipède autonome, IA embarquée locale, mise à l'échelle progressive | Jeremy | sept. | ambition du projet (le « rêve de gosse ») | buste (août) | mémoire |
| ToddlerBot comme base | Jeremy, Claude rallié | ≈ 20-09 | anatomie humanoïde, pile Python, chaîne documentée | Open Duck Mini, Berkeley Lite, Unitree, Asimov | 0001 |
| Amont cloisonné et épinglé | Jeremy sur proposition de Claude | ≈ 20-09 | distinguer ses écarts de ceux de l'amont | copier l'amont dans le dépôt | 0002 |
| Appropriation avant production | Jeremy | sept. | « je ne comprends rien à la codebase » | piloter vite | Conv. |
| Pièces libres et à Jeremy | Jeremy | sept. | ne pas être bloqué par CC BY-NC-SA | dériver la géométrie amont | mémoire |
| Everything as code, rien de binaire dans Git | Jeremy | sept. | régénérabilité | — | CLAUDE.md |
| Caractérisation du carton arrêtée (0042, 0044 closes) | Jeremy | 30-09 | valeurs non transférables au robot réel | poursuivre la métrologie | Conv. |
| **Moratoire sur les fiches rejeté** | Jeremy | 30-09 | son choix, non soumis à réexamen | moratoire proposé par Claude | Conv. |
| Date d'extraction conservée | Jeremy | 30-09 | provenance (0006) | la retirer | Conv. |
| **Démarche inversée** | Jeremy | 30-09 | classes discrètes, couple ∝ masse × taille | taille en entrée (P1/P2/P3) | 0047 |
| **Tailles Banc, S, M, L, XL ; premier robot S** | Jeremy | 30-09 | S, la moins chère pour traverser l'échelle | M en premier | 0048 |
| Scripts de chiffrage versionnés | Jeremy | 30-09 | recalculer quand les hypothèses changent | hors Git | 0049 |
| **Fabrication séquencée** (usinage, puis impression, puis hybride) | Jeremy | 30-09 | comprendre chaque procédé | découpe 2D seule | 0050 |
| **Marge 1,5**, à revoir après le banc | Jeremy : « je veux que l'on conserve cette marge » | 30-09 | voir la baisse de performance réelle | autre marge | 0051 |
| **Actionneur maison en piste parallèle**, hors chemin critique | Jeremy : « d'accord avec ton analyse » | 30-09 | apprendre sans bloquer | sur le chemin critique | 0052 |

### 3.2 À CONFIRMER

> **Réponse de Jeremy du 2026-09-30 :** poids et règle de décisivité d'abord NON fixés par lui, puis validés tels quels à ~23 h, avec la réserve « critères manquants » ; règle d'achat : à confirmer.

| Point | Ce que disent les sources | Pourquoi je doute |
| --- | --- | --- |
| Poids du comparatif (capacité 18, continuité 18, coût 15…) | CC et ma conclusion du 30 : « décidé » | je n'ai retrouvé aucune phrase de Jeremy qui les fixe ; un précédent existe (poids du banc attribués à tort, corrigé) |
| Règle de décisivité étendue | ma conclusion : « décidé » | même raison |
| Règle d'achat reformulée (pièce `coupable` ; outillage = Jeremy ; Claude ne propose jamais d'achat) | tranchée le 29 d'après ma synthèse | parole exacte non relue |

### 3.3 PROPOSÉ, jamais validé

| Proposition | Par | Statut réel | Commentaire |
| --- | --- | --- | --- |
| Famille Damiao J4310 V1.2 48 V pour S | Claude | **PROPOSÉ, à retirer** (§ 6) | fondé sur une notation 24 V |
| Banc de vérification 2 × J4310 48 V | Claude | **PROPOSÉ, à retirer** | la règle de décisivité impose de nouveau un départage |
| Critère d'abandon < 1,75 N·m au blocage | Claude | **PROPOSÉ, à réécrire** | ≈ 2,14–2,17 en 48 V, et seuil thermique incohérent |
| Note de transfert 3 → 5 | Claude | PROPOSÉ, **caduque** | reposait sur « k non décisif » |
| Vision (cadrage § 1) | Claude | PROPOSÉ depuis le 30-09 | — |
| Couche logicielle `joint.command()` avec backends | Claude | PROPOSÉ | démarrable sans achat |
| Immuabilité des fiches | ChatGPT et Claude | OUVERT | — |
| Fiches 0038 (thermique) et 0041 (incertitudes) | — | **proposées mais appliquées de fait** (CC) | à accepter ou à retirer |
| Bras SO-101 pour valider la pile IA tôt | Claude, août | jamais repris | — |

### 3.4 ABANDONNÉ

| Élément | Quand | Pourquoi | Formellement ? |
| --- | --- | --- | --- |
| Buste, puis Berkeley Lite comme base | sept. | ambition bipède ; actionneurs imprimés jugés fragiles | oui (0001) |
| Imprimante 3D gratuite | sept. | inexacte | oui (texte), **non en mémoire** : elle se contredit encore |
| Paliers P1/P2/P3 | 30-09 | remplacés par les tailles | **non** : toujours dans `anthropometry.yaml` |
| Procédé unique « découpe 2D », conception au carton | 30-09 | fiche 0050 | **non** : 0014, 0015 et CLAUDE.md inchangés |
| Semelle P2 et métrologie du carton | 30-09 | pivot carton | oui (0042 close sans trancher, 0044 close) |
| Seuil éliminatoire de 0,55 m | 30-09 | arbitraire | oui, traqué deux fois |
| Règle « phase 6 » | 29-09 | référent inexistant | oui, reformulée |
| Invariant « même G-code » | 29-09 | infirmé par un rapport de bogue | oui |
| Motif `mesures_suspendues` | 30-09 | créé puis retiré en 24 h | oui |
| Dockerfile dans l'empreinte | 30-09 | Coolify le réécrit | oui |
| Moratoire (proposé par Claude) | 30-09 | rejeté par Jeremy | oui |
| Recommandation « commencer avec le vainqueur » | ce document | fondée sur la notation 24 V | **je la retire ici** |

---

## 4. Implémenté et non implémenté

**Implémenté**, vérifié par CC le 30-09 :

- régénération complète : `regenerer.py` en 26 s, déterministe ;
- audit des origines : 3 035 valeurs, dont 978 numériques ;
- 125 motifs de règles ;
- 9 tests sur 9, sous `unittest` car pytest n'est pas installé ;
- empreinte égale entre dépôt et site ;
- simulation ToddlerBot en boucle fermée ;
- extraction de l'amont ;
- `anthropometry.yaml`, tables DIN 8580 ;
- une pièce avec sa chaîne complète : modèle, DXF, STEP, STL, plan, découpe, vérification ;
- les scripts de décision (dimensionnement, sélection multicritère, estimation thermique) et les documents qu'ils engendrent.

**Non implémenté, et pourquoi :**

| Élément | Pourquoi |
| --- | --- |
| Toute pièce qui s'interface | pas d'actionneur choisi, donc pas d'interface mécanique (décision reportée à « actionneur en main ») |
| Actionneurs, banc, électronique | famille non décidée ; alimentation et sécurité non définies |
| Couche `joint.command()` | proposée, jamais lancée |
| Nomenclature complète | `budget.yaml` chiffre des postes, pas une nomenclature |
| Politique entraînée sur un robot modifié | aucun robot modifié |
| Remplacement des paliers, de 0014, 0015 et de CLAUDE.md | explicitement différé le 30-09 (« question ouverte 8-9 ») |

Défauts d'outillage relevés par CC :

- `enveloppes_actionneurs.py --help` ignore son argument et réécrit `exports/` ;
- `K_ESTIME` est recopié à la main dans un script ;
- fuite de descripteur dans `controle_depot.py:78`.

**Proportion.** La gouvernance représente 57 % des lignes (66 % le 29). La
hausse du jour est allée à l'aide au choix des actionneurs. Le code qui
produit de la géométrie reste à 3 %.

---

## 5. Reporté, questions ouvertes, pistes

### 5.1 Reporté, avec son déclencheur

| Élément | Déclencheur |
| --- | --- |
| Interface mécanique actionneur | un actionneur en main, charges du roulement de sortie connues |
| Membre L de Damiao (J4340, 40:1, peu réversible) | avant L |
| Révision de la marge 1,5 | après le banc |
| `bd_warehouse` (visserie) | première pièce qui tient une vis |
| Veille 0032 (3 déclencheurs sur 4 liés à l'imprimante) | achat d'une imprimante |
| Chiffrage de la structure | procédé exact de l'opérateur CN connu |
| Batterie | tension retenue |
| FreeCAD et serveurs MCP | besoin de collaboration avec l'opérateur CN |

### 5.2 OUVERT

1. Rôle et composition du banc (§ 8, D1).
2. Critère de départage ou d'abandon (D2).
3. Alimentation et sécurité du banc (D3).
4. Poids de la masse dans le comparatif (D4).
5. Dépôt public ou privé (D5).
6. Ce que S doit porter : calculateur, batterie, centrale inertielle. Non chiffré.
7. Procédé exact de l'opérateur CN (laser, plasma, jet d'eau), rayons, matières, format de fichier.
8. Imprimante 3D : un achat a été évoqué en septembre, sans suite connue.
9. Licence des valeurs numériques extraites de ToddlerBot. Question juridique, sans avis ; **elle devient pratique si le dépôt devient public.**
10. Immuabilité des fiches ; espèces qui sont en fait des états.
11. Simulateur JavaScript du site : jamais vu fonctionner.
12. Blocage réseau sous WSL : constat, sans diagnostic.
13. Seconde personne exigée par le protocole de banc : non identifiée.

### 5.3 Pistes annexes

- Module d'actionneur unique répliqué (idée ODRI).
- MEVITA : tôle découpée et soudée, seul précédent d'un bipède non imprimé.
- Soudure comme moyen propre.
- Site collaboratif avec FreeCAD pour l'opérateur CN.
- Générateur 3D pour la silhouette uniquement.
- SO-101.

---

## 6. Confrontation des trois sources

Légende : **=** concordance ; **≠** divergence ; **+** une seule source le voit.

| # | Point | Conv. / Claude | CC | GPT | Type | Verdict et preuve |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Statut de la famille, du banc et du critère | recommandé, jamais validé | RECOMMANDÉ | traité comme décision | ≠ | **Conv. et CC.** Les questions du tour 49 n'ont pas reçu de réponse. GPT n'avait que le brief. |
| 2 | Damiao noté sur la variante 24 V | **non vu** : j'avais vu le 24 V dans le *coût* du banc, pas dans la notation | seuil de bascule k 0,49 → 0,61–0,62 | — | + CC | **CC**, par calcul refait en mémoire. C'est l'erreur la plus lourde de la journée, et elle m'échappe. |
| 3 | Banc : vérifier ou départager | « vérifier » (Claude, 30-09) | la conclusion ne tient plus qu'à 0,009 | qualifier J4310 **et** RS05 sur le même banc | ≠ | **CC et GPT.** Borne basse plausible de k = 0,619 contre bascule ≈ 0,61–0,62 : k redevient décisif **selon la règle du projet**. Je me rétracte. |
| 4 | Critère d'abandon au blocage | blocage = pire cas statique | 1,75 → ≈ 2,14–2,17 en 48 V ; 90 °C contre 100 °C, biais ≈ 7 % | blocage = une porte parmi huit | ≠ partielle | **Tous en partie.** Le blocage reste un bon premier test, mais ne suffit pas. **Forget § 5.2** : le bobinage est plus chaud que le carter, donc le modèle à un nœud impose une marge. Le critère, dérivé de la frontière de décision, doit être doublé d'un critère fondé sur le besoin (RMS × 1,5 de la pire articulation). |
| 5 | Sécurité du banc | alimentation à courant limité exigée | aucune alimentation conforme ; arrêt d'urgence, dynamomètre absents ; CE ; seconde personne | contacteur, régénération, carter, métrologie | = | Concordance. **GPT voit en plus la régénération** (surtension du bus). |
| 6 | Masse J4310 (325 g) contre RS05 (191 g) | non soulevé | poids de la masse : 5 % | ≈ +1,6 kg sur 12 articulations | + GPT | **GPT soulève un vrai risque.** RS05 à 191 g confirmé chez les revendeurs. À vérifier : `dimensionnement.py` boucle-t-il sur la masse réelle des actionneurs ? Mon prompt le demandait ; aucun rapport ne le confirme. |
| 7 | ToddlerBot comme étalon thermique | non soulevé | — | 19 min avant dégradation par surchauffe | + GPT | **GPT, vérifié** : le site ToddlerBot le publie, et l'article cite la surchauffe parmi les problèmes de fiabilité traités. Les profils mis à l'échelle ne prouvent donc pas une tenue indéfinie, ce qui **justifie la marge 1,5** et un essai thermique. |
| 8 | J4310 surtout en bras | constaté le 30 | — | DumBot13 : DM4310 au lacet de hanche seulement | = partielle | Usage en bras **vérifié** (reBot B601-DM de Seeed). DumBot13 : **non vérifié**. |
| 9 | Couple nominal RS05 | — | catalogue : valeur non citée | 1,6 (page produit) contre 1,8 (document du 13-07) | + GPT | **1,6 N·m vérifié** chez plusieurs revendeurs ; 1,8 non vérifié. Vérifier la valeur du catalogue (P1). |
| 10 | Stock RS05 | — | — | « en stock chez Seeed » | ≠ web | **Non confirmé** : rupture ou commande en attente chez deux revendeurs consultés le 30-09. |
| 11 | Boucle masse et dimensionnement | exigée dans mon prompt | script exécuté sans erreur | « à ajouter » | ≠ | **Indéterminé** jusqu'à P1. GPT n'a pas pu lire le dépôt. |
| 12 | Marge 1,5 unique | décidée par Jeremy | 0051 | à éclater (mécanique, thermique, choc, modèle) | ≠ | **Décision de Jeremy, maintenue.** L'objection de GPT est juste sur le fond, mais la fiche prévoit déjà sa révision après le banc. À rouvrir à ce moment, pas avant. |
| 13 | Proportion gouvernance | 66 % ; moratoire proposé | 57 % | « maturité documentaire > expérimentale » | = | Concordance sur le constat. Le moratoire a été rejeté par Jeremy ; je ne le rouvre pas. |
| 14 | CLAUDE.md contre 0050 | listé ouvert | **haut** : un agent dessinerait au carton | — | = | Concordance ; à corriger en priorité (P3). |
| 15 | Fiches contredites sans remplacement | 0014, 0015, paliers | + 0001, 0005, 0011, 0038 ; 0047 et 0049 écrites après application | — | + CC | **CC** voit plus loin, preuves au § 3.1 de son rapport. |
| 16 | Dépôt « public » | le 29 : privé ; mon prompt GPT : « public » | — | 404 | ≠ | **Privé** (réponse de Jeremy le 30-09). Mon prompt était faux. |
| 17 | Taille de S | 0,55–0,65 m (ma conclusion) | 0,55–0,60 m | ≈ 0,6 m | ≠ mineure | **CC** : les documents engendrés font foi. |
| 18 | Imprimante 3D | déclarée en août, infirmée en septembre | — | — | + Conv. | La mémoire se contredit encore. Le fait courant est : **pas d'imprimante**. |
| 19 | Traçabilité du J4310 | manuel V1.4 cité le 30 | — | manuel du 14-09 sans notes de version | + GPT | Non vérifié par moi. Clé de révision (fabricant + modèle + HW + FW + tension) : **proposition juste**, à reprendre dans P1. |
| 20 | Watchdog RS05 à 0 par défaut | — | — | selon le pilote communautaire | + GPT | Non vérifié. À intégrer au protocole (porte « perte CAN »). |

---

## 7. Erreurs de méthode

| Erreur | Qui | Ce qu'elle a appris |
| --- | --- | --- |
| Imprimante déclarée disponible (août), jamais revérifiée | cadrage (Jeremy et Claude) | un moyen de fabrication se vérifie avant de fonder une architecture |
| CERN-OHL-S présentée comme non commerciale ; licence ToddlerBot BY-NC au lieu de BY-NC-SA | Claude | une licence se lit, elle ne se résume pas de mémoire |
| Solo, Bolt, Upkie présentés comme faits en plaques | Claude | vérifier les précédents avant de s'en réclamer |
| Actionneurs dimensionnés sans la thermique | Claude | Forget : la température est le vrai facteur limitant |
| Audit vert mais faux (un fourre-tout masquait six règles mortes) | système | un contrôle doit prouver qu'il sait échouer |
| « Site non responsive » (c'était un cache), date du 30 au lieu du 29, « bug du pied de page » | Claude, CC, Jeremy | **diagnostiquer avant de prescrire** |
| Seuil de 0,55 m, exposant de marge −¼ au lieu de −⅓, cumul de budget, « calcul en cours » inexistant | Claude | un seuil arbitraire se cache partout |
| Poids du banc attribués à Jeremy alors qu'il posait la question | Claude et CC | attribuer une décision est une donnée de traçabilité |
| **Notation Damiao en 24 V non vue** | **Claude**, puis CC l'a trouvée | vérifier que l'objet noté est l'objet recommandé |
| **« Tes données publiques décident déjà »** | **Claude** | une marge de 0,10 point qui « fond à bas k » n'est pas une décision |
| **Recommandation d'achat « a puis c »** | **Claude** | contraire à l'esprit de la règle d'achat |
| **« Dépôt public » dans le prompt de ChatGPT** | **Claude** | l'audit externe a perdu son objet |
| Fiches 0047 et 0049 écrites après leur application ; 0038 et 0041 appliquées sans acceptation | processus | le statut d'une fiche doit suivre son application, pas la précéder ni la suivre de loin |
| Documents qui se contredisent sans se remplacer (cadrage, conclusion, comparatifs, CLAUDE.md) | processus | une synthèse de plus aggrave le défaut, **ce document compris** : il ne doit pas coexister avec la conclusion |

**Le motif commun.** Le symptôme était ailleurs qu'on ne le croyait, et une
vérification de trente secondes aurait suffi. Depuis le 30, un second motif
apparaît : **une recommandation plus sûre d'elle que ses données.**

---

## 8. Les décisions qui t'attendent

Mes recommandations sont marquées **R**. Aucune n'est prise à ta place.

### Urgence 1 — avant toute dépense

**D1. Le rôle du banc.**
- a) Départager J4310 48 V et RS05 sur le même banc.
- b) Garder « vérifier » avec 2 × J4310.
- c) Attendre le recalcul P1 avant de trancher.

**R : c, puis probablement a.** La composition (1 + 1, 2 + 1, 2 + 2, avec ou
sans EduLite 05) se décide sur les chiffres de P1.

**D2. Le critère écrit avant la mesure.**
- a) Garder 1,75 N·m.
- b) Le recalculer en 48 V et unifier le seuil thermique.
- c) b, plus un critère fondé sur le besoin (couple RMS × 1,5 de la pire articulation, à la vitesse de la marche) et une première série de portes : zéro et étalonnage, blocage, paliers, couple et vitesse, perte CAN et arrêt d'urgence.

**R : c.** Le rejeu complet de la marche vient ensuite, quand les profils couple–vitesse par articulation seront extraits.

**D3. L'alimentation et la sécurité du banc.** C'est de l'outillage, donc ta
seule décision. Conditions minimales, communes aux trois sources :
- limitation de courant réglable ;
- coupure physique indépendante du PC ;
- gestion de la régénération ;
- carter autour du bras de levier ;
- seconde personne présente.

**R : aucune mise sous tension avant que le protocole les exige toutes.**

**D4. Le poids de la masse (5 %).**
- a) Le rouvrir.
- b) Vérifier d'abord que la boucle masse existe dans `dimensionnement.py`.

**R : b.** Si la boucle existe, la masse pèse déjà dans la capacité, et la relever dans les poids la compterait deux fois.

### Urgence 2 — cohérence du dépôt

**D5. Public ou privé.**
- a) Rester privé et donner à ChatGPT un export.
- b) Passer public.

**R : a, tant que la question de licence (§ 5.2 n° 9) n'est pas instruite.**
Rendre public un dépôt qui contient des valeurs extraites d'une conception
CC BY-NC-SA engage cette question.

**D6. CLAUDE.md aligné sur 0050 et sur le cadrage.** Oui ou non. **R : oui, sans attendre.**

**D7. Remplacer formellement** les paliers, 0014, 0015 et les autres fiches contredites (liste CC), par des fiches « Remplacée par ». Oui ou non. **R : oui**, avec la même procédure pour toutes.

**D8. Immuabilité des fiches** : ne plus réécrire une fiche acceptée. Oui ou non. **R : oui.** C'est la condition de D7.

### Urgence 3 — dette

**D9.** Fiches 0038 et 0041 : les accepter (elles sont appliquées) ou les retirer. **R : les accepter.**

**D10.** Petites dettes : `K_ESTIME` recopié, `--help`, descripteur non fermé, pytest, 13 documents fournisseurs absents du registre 0030. **R : un lot unique.**

**D11.** Vision du cadrage § 1 : la valider, l'amender ou la laisser proposée.

### À ne pas trancher maintenant

- La **famille d'actionneurs de S**, qui attend P1 puis le banc.
- La **marge 1,5**, qui attend le banc (fiche 0051).

---

## 9. Prompts Claude Code

Chacun ne se lance qu'après ta validation de la décision indiquée.

### P1 — Recalcul du comparatif en 48 V (lecture et calcul ; à lancer pour D1, D2, D4)

```
Recalcul du comparatif des familles. `date` d'abord.
Contexte : ton rapport 2e726e8 § 8 constat 1 (Damiao noté en 24 V).

1. Membre S de Damiao = J4310 V1.2 48 V dans params/ et dans la
   notation. Clé de révision partout : fabricant + modèle + révision
   matérielle + tension (+ firmware si connu).
2. RS05 : quelle valeur de couple nominal porte le catalogue ?
   Revendeurs consultés le 30-09 : 1,6 N·m. Si le catalogue porte 1,8,
   porte les deux valeurs avec leur source, retiens la plus basse, et
   recalcule.
3. Dis, avec fichier:ligne, si dimensionnement.py boucle sur la masse
   RÉELLE des actionneurs (J4310 ≈ 325 g, RS05 191 g). Si non, arrête-toi
   après ce constat, n'implémente rien.
4. Régénère. Donne : le k de bascule, la borne basse plausible de k,
   l'écart entre les deux, le gagnant pour k de 0,5 à 1,0, et le verdict
   de la règle de décisivité (le banc doit-il départager ?).
5. Sensibilité au poids de la masse : 5, 10, 15. Ne change PAS le
   poids retenu ; rapporte seulement si le gagnant change.
6. Recalcule le critère d'abandon en 48 V avec un seul seuil thermique
   (celui du protocole). Retire K_ESTIME recopié : lis-le à la source.
7. Documents engendrés mis à jour. Aucune fiche. Statut « recommandé »
   inchangé partout. Journal, commit, clôture habituelle. Dans le
   terminal : les chiffres des points 2 à 6 en dix lignes.
```

### P2 — Sort de la conclusion et versement de ce document (ta réponse du 30-09)

```
Deux documents de synthèse du 30-09 : docs/conclusion-arbitrages-
2026-09-30.md (non suivi) et docs/arbitrage-2026-09-30.md (joint).
`date` d'abord.

1. Compare-les. Liste ce que la conclusion dit et que l'arbitrage ne dit
   pas, et les contradictions entre les deux.
2. Propose, sans l'appliquer : (a) supprimer la conclusion, (b) la
   commiter avec un en-tête « Remplacée par arbitrage-2026-09-30 », ou
   (c) autre. Motive en trois lignes.
3. Vérifie chaque chiffre de l'arbitrage attribué à ton rapport contre
   le dépôt. Écart = liste, pas de correction.
4. Commite arbitrage-2026-09-30.md tel quel. Journal, commit, clôture.
   Terminal : ta proposition du point 2 et les écarts du point 3.
```

### P3 — Cohérence documentaire (si tu valides D6, D7, D8)

```
Cohérence après le pivot du 30-09. `date` d'abord.

1. CLAUDE.md : réécris la section fabrication et méthode pour refléter
   0047 à 0052 et docs/cadrage.md. Retire « procédé unique : découpe 2D »
   et « concevoir au carton ». Aucune règle nouvelle.
2. Fiche d'immuabilité (D8) : une fiche acceptée ne se réécrit plus,
   elle est remplacée par une nouvelle.
3. Pour chaque fiche contredite (liste de ton rapport § 3.1 : 0001,
   0005, 0011, 0014, 0015, 0038 et les paliers), crée UNE fiche qui
   remplace, et ajoute en tête des anciennes « Remplacée par NNNN »,
   sans toucher leur texte.
4. anthropometry.yaml : paliers remplacés par les tailles, avec renvoi à
   la fiche de remplacement.
5. index_fiches.py : lit « Remplacée par ». Test vu échouer avant de
   passer.
Journal, commit par point, clôture habituelle.
```

### P4 — Protocole de banc (si tu valides D2 et D3 ; ne commande rien)

```
Protocole de banc v2. `date` d'abord. Aucun achat, aucune suggestion
d'achat.

1. docs/protocole-banc.md : un seul seuil thermique ; capteur interne
   (dire ce qu'il mesure d'après le manuel) plus thermocouple externe
   carter et plaque ; marge bobinage-carter (Forget § 5.2, corpus).
2. Portes, dans l'ordre : T0 zéro et étalonnage ; T1 blocage ; T2
   paliers ; T3 couple et vitesse ; T8 perte CAN, bus-off, watchdog
   (vérifier sa valeur usine), redémarrage, arrêt d'urgence. Le rejeu de
   la marche (T4) est marqué « après extraction des profils couple–
   vitesse ».
3. Critère écrit avant la mesure, repris de P1, plus le critère de
   besoin (RMS × 1,5 de la pire articulation).
4. Conditions de sécurité EXIGÉES avant toute mise sous tension :
   courant limité réglable, coupure physique indépendante du PC,
   gestion de la régénération, carter, seconde personne. Chacune est un
   prérequis bloquant, pas un achat proposé.
5. La plaque 70 × 70 mm : spécifier alliage, épaisseur, interface,
   couple de serrage, orientation, ambiance.
Journal, commit, clôture habituelle.
```

### P5 — Export pour le relecteur externe (si tu valides D5 a)

```
Export de relecture. `date` d'abord.
Crée exports/relecture/ (ignoré par Git) : cadrage, arbitrage,
choix-famille-actionneurs, comparatif-banc, protocole-banc,
estimation-thermique-j4310, dimensionnement-par-actionneur,
criteres_selection.yaml, actionneurs.yaml, decisions/index.md, et un
MANIFEST avec l'empreinte du dépôt. Aucune valeur amont brute
(upstream_joints.generated.yaml exclu). Une archive .zip. Terminal :
chemin et taille.
```

### P6 — Dette (si tu valides D9 et D10)

```
Lot de dette. `date` d'abord.
0038 et 0041 : état → acceptée, avec date et renvoi à leurs
applications. enveloppes_actionneurs.py : --help n'écrit rien (test vu
échouer). controle_depot.py:78 : fichier fermé. pytest dans
requirements de dev, ou tests déclarés unittest dans CLAUDE.md.
Registre 0030 : les 13 documents fournisseurs manquants.
Journal, commit par point, clôture habituelle.
```