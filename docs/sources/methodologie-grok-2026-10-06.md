La méthode que tu décris est déjà proche de ce que font les labos qui publient vraiment du matériel. Le trou n’est pas l’absence d’un optimiseur : c’est l’absence de lois d’échelle, de caractérisation d’actionneur et de contraintes de sécurité avant l’exploration combinatoire.

## 1. Résumé

YXOR a déjà le bon squelette : exigences chiffrées, famille d’actionneurs commune, fil numérique (YAML, Python, CAO en code, MuJoCo), front de Pareto, banc d’essai. C’est exactement la logique du cycle en V mécatronique (VDI 2206, révision 2021) et des processus techniques d’ISO/IEC/IEEE 15288:2023, sans avoir besoin de les implémenter en entier.

Ce que les équipes qui ont construit des robots publient n’est pas une recherche exhaustive axes × actionneurs × taille. Berkeley Humanoid, MIT Humanoid, ODRI et ToddlerBot figent tôt une famille d’actionneurs quasi-direct drive, caractérisent couple-vitesse-thermique sur banc, puis itèrent mécanique et contrôle. L’exploration combinatoire complète est ce que tu réinventes, et ce qui coûte le plus pour un développeur seul.

Deux résultats utiles pour tes deux échelles (0,6 m / 10 kg puis 1,2 m / 25–40 kg) : la masse des bipèdes publiés suit plutôt \(m \propto L^{2}\) que \(L^{3}\), et le couple de marche suit \(\tau \propto mL\) (Oke et al., 2026). La vitesse suit la similitude dynamique \(v \propto \sqrt{L}\). Un robot deux fois plus haut ne demande donc pas huit fois le couple.

Le cadre minimal : exigences et scénarios de chute d’abord, famille d’actionneurs proprioceptifs ensuite, V-model court avec banc, co-conception seulement sur quelques paramètres libres, documentation DIN SPEC 3105 en continu. Capella, SysML v2 et OpenMDAO attendent que l’architecture soit stable.

Aucune source ouverte ne montre qu’une IA conçoit seule un humanoïde fabricable. Les articles de co-conception (Ha 2018, RoboCraft 2025, BRIDGE 2026) optimisent morphologie et contrôle en simulation, puis un humain fabrique.

## 2. Méthodologies éprouvées

Le coût d’apprentissage est une estimation d’ingénierie, pas une donnée de norme. « Adaptée seul » veut dire utile sans équipe dédiée.

| Nom | Origine | Apport ici | Coût | Seul |
|---|---|---|---|---|
| ISO/IEC/IEEE 15288:2023 | Norme, ISO/IEC/IEEE, mai 2023 | Vocabulaire de processus (exigences, architecture, V&V, information) à tailler, pas un cycle imposé | Moyen | Oui, taillé |
| Cycle en V / VDI 2206 | VDI 2206:2004, révisée 2021 pour systèmes mécatroniques et cyber-physiques | Découpage exigences → architecture → domaines (méca, élec, logiciel) → intégration → validation, avec V imbriqués | Faible | Oui |
| INCOSE / SEBoK | INCOSE, SEBoK v2.14 (2026) | Carte des connaissances ; trop large pour être suivi tel quel | Élevé si complet | Non en entier |
| VDI 2221 / Pahl & Beitz | VDI 2221 ; Pahl, Beitz et al., *Engineering Design* | Clarifier la tâche, chercher des principes, évaluer, avant la CAO | Moyen | Oui, version courte |
| MBSE Arcadia / Capella | Thales puis Eclipse, Capella 7.1.0 (juillet 2026), EPL-2.0 | Chaîne besoin → fonctions → architecture logique → physique | Élevé | Plus tard |
| SysML v2 / SysON | OMG ; Eclipse SysON, EPL-2.0 | Modèle formel interopérable ; peu démontré sur humanoïde open source | Élevé | Non maintenant |
| Ingénierie des exigences + QFD | Akao ; pratique SE | Relier « course, saut, saisie » à couple, vitesse, course articulaire | Faible | Oui |
| Analyse morphologique | Zwicky | Tableau axes × transmissions × actionneurs, puis élagage | Faible | Oui, si élagué |
| Conception axiomatique | Suh, *The Principles of Design* | Indépendance des fonctions (jambe / main / visage) et information minimale | Moyen | Partiel |
| DSM | Steward ; Eppinger | Voir quels choix (réduction, bus, batterie) se couplent | Faible | Oui |
| MDO / OpenMDAO | NASA, Apache-2.0, actif (3.x en 2026) | Coupler masse, thermique, coût si les modèles existent déjà | Moyen | Plus tard |
| NSGA-II / Pareto (pymoo) | Deb 2002 ; pymoo, Apache-2.0 | Front coût–masse–capacité une fois l’espace réduit | Faible | Oui, espace réduit |
| Exploration d’espace / set-based | Sobek, Ward, Liker (Toyota) | Garder des intervalles (réduction 6–12, deux tailles moteur) au lieu d’un point trop tôt | Faible | Oui |
| TRIZ | Altshuller | Contradictions (rigidité vs masse, couple vs réversibilité) | Moyen | Optionnel |
| Jumeau numérique | Pratique ; ToddlerBot, Booster Lab | Modèle identifié (zéro, inertie rotor, courbe T–n), pas seulement un MJCF nominal | Moyen | Oui, ciblé |
| AMDEC / FMEA | IEC 60812:2018 | Chute, perte bus, surcharge thermique, pincement | Faible | Oui, courte |
| TRL | NASA / DoD | Gel de jalons : actionneur TRL 4, jambe 5, marche 6 | Faible | Oui |
| V&V | 15288, VDI 2206 | Banc avant robot complet ; test lié à une exigence identifiée | Faible | Oui |

Sources : norme ISO/IEC/IEEE 15288:2023 ; directive VDI 2206 (sommaire de la révision 2021) ; SEBoK ; Eclipse Capella et SysON ; OpenMDAO (Apache-2.0) ; IEC 60812:2018. 

## 3. Méthodes propres aux robots à jambes

| Méthode | Ce qu’elle change pour YXOR | Références |
|---|---|---|
| Actionneur proprioceptif / QDD | Moteur fort couple, réduction faible (souvent 6–12), mesure de courant comme proxy de couple, réversibilité aux chocs. Métrique IMF pour comparer la tenue aux impacts | Wensing, Wang, Seok, Otten, Lang, Kim, IEEE TRO, 2017, doi:10.1109/TRO.2016.2640183 |
| Architecture modulaire ouverte | Un module couple + 3D print + pièces du commerce, réutilisé en quadrupède et bipède | Grimminger et al., IEEE RA-L, 2020, doi:10.1109/LRA.2020.2976639 ; open-dynamic-robot-initiative.github.io |
| Dimensionnement conscient des limites actionneur | Le planificateur et le simulateur voient couple, vitesse, chute de tension batterie | Chignoli, Kim, Stanger-Jones, Kim, arXiv:2104.09025, 2021 (démos acrobatiques en simulation réaliste, pas un claim matériel dans l’abstract) |
| Lois d’échelle | \(m \propto L^{2}\) empirique chez les bipèdes publiés, \(v \propto L^{1/2}\), \(\tau \propto mL\). La forme de pied optimale ne se transpose pas par simple homothétie | Oke, Carter, Gu, Pride, Man, Bergbreiter, Johnson, arXiv:2603.22560, 2026 |
| Co-conception forme–contrôle | Optimiser quelques longueurs et placements avec la trajectoire, pas tout le robot | Ha, Coros, Alspach, Kim, Yamane, IJRR, 2018, doi:10.1177/0278364918771172 |
| Co-conception morphologie–politique | Gains simulés importants, fabrication ensuite humaine | RoboCraft, arXiv:2510.22336, 2025 ; BRIDGE, arXiv:2609.03497, 2026 (comparé à ToddlerBot, Bumi, K1) |
| Sim-to-real | Randomisation, identification actionneur, transfert zéro-shot | Hwangbo et al., Science Robotics, 2019 (ANYmal) ; revue domain randomization, Muratore et al., Frontiers in Robotics and AI, 2022, doi:10.3389/frobt.2022.799893 |
| Jumeau identifié | Calibration de zéro et identification moteur transférable | Shi, Wang, Song, Liu, ToddlerBot, arXiv:2502.00893, 2025 ; CoRL 2025 |
| Courbe T–n réelle dans le simu | Mesure banc, puis limites et inertie rotor \(J_{arm}=N^{2}J_{m}\) | Chen, Zheng, Zhang, Zhao, Booster Lab, arXiv:2606.27813, 2026 |




## 4. Comment les équipes ont réellement conçu

Berkeley Humanoid (Liao et al., arXiv:2407.21781, 2024) : 0,85 m, 16 kg, électrique, conçu pour l’apprentissage. Ils retirent ressorts, amortisseurs et chaînes fermées pour simplifier la simulation, montent l’actionneur comme articulation via un roulement croisé, et déclinent 4 tailles d’actionneurs maison. Berkeley Humanoid Lite (Chi et al., arXiv:2504.17249, RSS 2025) : réducteur cycloïdal imprimé, pièces grand public, coût matériel annoncé sous 5 000 USD, durabilité des plastiques mesurée, locomotion par RL. Documentation d’assemblage publique.

ToddlerBot (Shi et al., 2025) : 0,56 m, 3,4 kg, sous 6 000 USD, presque tout imprimé, principes explicites reproductibilité / capacité / compatibilité ML. Le jumeau vient d’une calibration de zéro et d’une identification moteur, pas d’un URDF nominal. Réplications indépendantes citées par les auteurs.

MIT : Mini Cheetah puis Humanoid. Les actionneurs U10/U12 dérivent du Mini Cheetah, réductions 6 à 12, couples de l’ordre de 34 à 136 N·m selon l’axe (table I de Chignoli et al., 2021). Le dimensionnement part du geste dynamique, pas d’un catalogue combinatoire.

ODRI (Grimminger et al., 2020) : module ouvert bas coût, Solo 8/12, bipède Bolt. Licence matérielle BSD-3-Clause sur le dépôt mécanique. Méthode : un actionneur maîtrisé, puis plusieurs robots.

Booster : pas de papier de conception mécanique ouvert trouvé. Le papier 2026 décrit la mesure des courbes couple-vitesse du T1 et leur injection dans le simulateur. Masse commerciale citée vers 30 kg (source revendeur, à traiter comme secondaire).

Unitree : méthodologie de conception interne non trouvée dans des sources primaires ouvertes.

Agility (Digit) : papier de transfert de politique (Castillo et al., arXiv:2103.15309) et article d’entreprise 2025 sur un modèle de contrôle corps entier entraîné dans Isaac Sim, transfert annoncé zéro-shot. Méthode de dimensionnement mécanique non publiée. Source entreprise, pas article de conception.

Apptronik (Apollo) : retour de design industriel (argodesign) sur la forme et l’interface, pas de méthode de dimensionnement publiée. Non trouvé côté ingénierie système.

Erreur récurrente dans les papiers, pas toujours nommée ainsi : croire le modèle nominal (frottement, jeu, thermique, zéro encodeur) et découvrir l’écart au premier transfert. ToddlerBot et Booster Lab sont les retours les plus explicites.

## 5. Outils « tout en code »

Prix constatés dans des sources 2026 secondaires (revendeurs, comparatifs) : à revérifier avant achat. Les licences open source viennent des dépôts.

| Outil | Fonction | Licence | Prix | Linux/WSL | Pilotable code / IA |
|---|---|---|---|---|---|
| build123d | CAO Python, STEP/STL | Apache-2.0, actif | 0 | Oui | Oui |
| CadQuery | Idem, API plus ancienne | Apache-2.0, actif (dépôt à jour oct. 2026) | 0 | Oui | Oui |
| OpenSCAD | CSG script | GPL-2.0, projet vivant mais cadence lente | 0 | Oui | Oui |
| FreeCAD scripté | CAO + Python | LGPL-2.1, 1.0 fin 2024 | 0 | Oui | Oui, plus fragile |
| Onshape + onshape-to-robot | CAO cloud → URDF/MJCF ; exemples humanoïde Rhoban | Outil propriétaire ; exemples MIT | Gratuit si documents publics ; Standard cité vers 1 500 USD/an | Navigateur, donc WSL inutile | API oui |
| Fusion 360 | CAO/FAO | Propriétaire | Personnel gratuit sous conditions ; commercial cité vers 680 USD/an | Windows natif, WSL non | API oui, compte requis |
| SolidWorks | CAO industrielle | Propriétaire | Ordre 4 000 USD/an ; Maker cité vers 99 USD/an non commercial | Windows | API oui, mauvais choix solo Linux |
| Capella 7.1 | MBSE Arcadia | EPL-2.0, actif | 0 (support payant) | Oui | Modèles éditables, IA possible mais peu outillée |
| SysON | SysML v2 web | EPL-2.0, actif | 0 | Oui | Oui, moins mature que Capella |
| OpenMDAO | MDO gradients | Apache-2.0, actif | 0 | Oui | Oui |
| pymoo | NSGA-II/III | Apache-2.0 | 0 | Oui | Oui |
| MuJoCo | Simulation | Apache-2.0 (DeepMind) | 0 | Oui | Oui |

Chaîne la plus cohérente avec ton dépôt : paramètres YAML → build123d (pièces laser/pliage) → export STEP + génération MJCF → essais MuJoCo → journal. onshape-to-robot est le seul pont CAO→URDF/MJCF déjà utilisé sur un humanoïde open source (Sigmaban, Rhoban). build123d ne le fait pas seul : il faut ton générateur, ce que tu as déjà prévu.

## 6. Sécurité, par masse

Aucune norme lue ici n’exonère un robot parce qu’il fait 10 kg. Le risque suit l’énergie cinétique, la hauteur de chute et le pincement.

ISO 13482:2014 vise les robots de soin personnel : servant mobile, assistant physique, porteur de personne. Elle ne couvre pas les jouets, le médical, le militaire, ni les robots industriels (ISO 10218), ni au-delà de 20 km/h. Elle demande conception sûre, mesures de protection et informations d’utilisation, et reconnaît qu’il n’existait pas, à sa publication, de données internationales exhaustives de seuils de douleur aux chocs. Guide d’application : ISO/TR 23482-2:2019. Une révision élargie aux robots de service circulait en DIS en 2024 (ISO/DIS 13482) : ce n’est pas, dans les sources ouvertes ici, une norme publiée remplaçant l’édition 2014.

ISO 10218 (robots industriels ; révision 2025 citée par des guides secondaires) et ISO/TS 15066 (limites biomécaniques de force et pression, annexe informative, contexte collaboratif bras) ne sont pas écrits pour un bipède qui tombe. Ils restent la meilleure référence chiffrée publiée pour un contact volontaire bras/main. IEC 61508 couvre la sécurité fonctionnelle E/E/PE : utile si tu revendiques un niveau SIL, disproportionné sinon. Pour les fonctions d’arrêt, ISO 13849 est le chemin machinerie le plus courant. IEC 60204-1 éclaire l’arrêt d’urgence et la coupure puissance, pensé pour une machine plutôt fixe.

Pratique distinguée de la norme, pour les deux masses :

- 10 kg, type ToddlerBot : les auteurs argumentent la sécurité par la masse et la taille. Ça ne remplace pas un arrêt, une limite de couple et une zone d’essai. Énergie de chute plus faible, mais doigts et engrenages imprimés restent des risques de pincement.
- 25–40 kg, ordre du T1/G1 : un adulte peut être déséquilibré ; la chute du buste n’est pas couverte par les tables de contact de bras. Prévoir coupure batterie accessible, arrêt d’urgence indépendant du bus logiciel, limite de vitesse au démarrage, détection de chute, et pas d’essai de course dans une pièce habitée.

AMDEC minimale : perte de bus, blocage réducteur, emballement, basculement batterie, pincement main, chute sur personne.

## 7. Documentation matériel ouvert

DIN SPEC 3105 (2020, DIN, licence CC, processus communautaire) : partie 1 exigences de documentation technique, partie 2 évaluation communautaire. OSHWA : définition et checklist (sources publiques, licence sans clause non-commerciale ni no-derivatives, distinction clair de ce qui est ouvert). Open Know-How : métadonnées pour rendre un design trouvable. Détail non ouvert ici : le texte intégral des critères DIN SPEC. Sources : billet OSH Park 2020 citant Bonvoisin et al. ; checklist OSHWA. 

## 8. Comparaison avec ta méthode

Déjà conforme : capacités → tâches chiffrées → exigences d’articulation → simulation → filtres (couple, vitesse, thermique, encombrement, fab, élec, sécurité) → Pareto → choix humain → banc. Deux robots, une famille d’actionneurs, un bus, un logiciel. C’est le VDI 2206 plus le set-based design, et c’est ce que font ODRI et MIT à plus petite échelle.

Réinventé : l’énumération de toutes les combinaisons axes × actionneurs × taille. Les papiers partent d’une famille QDD (6–12) et de 2 à 4 tailles moteur, puis élaguent par \(\tau \propto mL\) et par le thermique continu, pas par NSGA-II sur tout l’espace. Le front de Pareto reste utile après cet élagage.

Manque : identification banc (courbe T–n, IMF ou au moins couple de backdrive, résistance thermique) avant de croire MuJoCo ; scénarios de chute et AMDEC avant d’ajouter course et saut ; identifiants d’exigences liés aux tests ; jalons TRL ; documentation DIN SPEC / OSHWA (sources CAO, nomenclatures, ce qui reste propriétaire chez RobStride ou Damiao). Les mains à doigts et le visage sont un autre robot : les coupler trop tôt casse l’indépendance fonctionnelle.

## 9. Cadre minimal et ordre

1. Figer 5 scénarios chiffrés : marche plate, pente, relevé, port d’une masse, contact non voulu. Une exigence = un identifiant, un critère, un test.
2. Faire l’AMDEC de chute et de bus, et l’arrêt d’urgence, avant d’optimiser la course.
3. Choisir la famille d’actionneurs avec les lois d’échelle et les datasheets, pas avec un produit cartésien. Garder des intervalles (set-based), pas un optimum.
4. Banc : courbe couple-vitesse, échauffement continu, jeu, zéro. Injecter ça dans MuJoCo, comme Booster Lab.
5. V court sur la jambe seule, puis le petit robot (0,6 m). Le grand robot réutilise module et logiciel, il ne reprend pas l’exploration.
6. Co-conception seulement sur longueur de tibia, position de hanche, réduction. Pas sur le visage.
7. Documenter au fil de l’eau selon DIN SPEC 3105 et la checklist OSHWA.
8. Capella ou SysON seulement si le nombre d’interfaces dépasse ce que le YAML et le journal tiennent. OpenMDAO seulement quand masse, thermique et coût sont des fonctions de code stables.

Premières actions : écrire la matrice scénario → articulation → couple pic / couple continu ; mesurer un actionneur candidat sur banc avant le prochain passage Pareto ; ajouter au dépôt un registre de décisions daté, lié aux identifiants d’exigences.

## 10. Registre des sources

Normes et directives : ISO/IEC/IEEE 15288:2023, webstore IEC ; VDI 2206, sommaire révision 2021, vdi.de ; ISO 13482:2014, iso.org ; ISO/TR 23482-2:2019 ; IEC 60812:2018 ; DIN SPEC 3105 via OSH Park, 2020. Fiabilité haute pour l’existence et le périmètre, le texte normatif payant n’a pas été ouvert en entier.

Articles : Wensing et al. 2017, TRO ; Grimminger et al. 2020, RA-L ; Chignoli et al. 2021, arXiv:2104.09025 ; Ha et al. 2018, IJRR ; Hwangbo et al. 2019, Science Robotics ; Liao et al. 2024, arXiv:2407.21781 ; Chi et al. 2025, arXiv:2504.17249 ; Shi et al. 2025, arXiv:2502.00893 ; Oke et al. 2026, arXiv:2603.22560 ; Chen et al. 2026, arXiv:2606.27813 ; RoboCraft 2025, arXiv:2510.22336 ; BRIDGE 2026, arXiv:2609.03497. Fiabilité haute pour ce qui est dans les abstracts lus ; les PDF complets n’ont pas tous été parcourus ligne à ligne.

Outils : dépôts CadQuery (Apache-2.0), Eclipse Capella, Eclipse SysON (EPL-2.0), OpenMDAO (Apache-2.0), build123d documenté Apache-2.0, onshape-to-robot.readthedocs.io et exemples Rhoban (MIT). Prix Fusion, Onshape et SolidWorks : comparatifs 2026, fiabilité moyenne.

Non trouvé : méthode de conception mécanique publiée d’Unitree, d’Agility et d’Apptronik ; seuil d’énergie en joules normatif dans ISO 13482 ; texte intégral DIN SPEC 3105. Les affirmations « l’IA conçoit le robot » des vendeurs ne sont pas étayées par ces papiers.