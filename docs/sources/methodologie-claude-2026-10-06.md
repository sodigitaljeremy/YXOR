# YXOR — Méthodes d'ingénierie : recherche et vérification

**Rapport de Claude, 6 octobre 2026.** Réponse au même prompt que ChatGPT, Grok et Gemini.

**Comment lire ce rapport.** J'ai fait des recherches web ciblées sur les points où les autres rapports divergeaient ou n'étaient pas vérifiés : loi d'échelle, ISO 18646-5, état de SysML v2, ISO 13482, Booster Lab, BRIDGE, RoboCraft, Berkeley Humanoid Lite, build123d, LeRobot Humanoid. Ces points sont marqués **vérifié** avec leur lien au § 8. Le reste (normes payantes, ouvrages, prix d'outils propriétaires) vient de mes connaissances et des autres rapports : il est marqué **non vérifié ici**. Ce rapport est donc moins large qu'une recherche approfondie de plusieurs heures, mais plus sûr sur les points qui changent nos calculs.

## 1. Résumé en 10 lignes

1. Ta méthode est déjà alignée avec l'état de l'art : exigences chiffrées, exploration, Pareto, choix humain, banc. Les quatre LLM le disent.
2. **Correction majeure vérifiée** : la masse des bipèdes réels croît comme la longueur de jambe à la puissance 2,12 environ, pas 3 (Oke et al., 2026). Notre modèle de masse ∝ H³ surestime le robot final.
3. Notre loi de couple (couple ∝ masse × longueur) est, elle, cohérente avec la même étude. Seul l'exposant de masse est à revoir.
4. **Booster Lab (2026, vérifié)** décrit exactement ce que doit produire notre banc : la courbe couple-vitesse mesurée, ses points de coude injectés comme limites dans le simulateur, et l'inertie réfléchie N²·Jm.
5. **ISO 18646-5:2026 existe** (essais de performance de locomotion des robots à jambes), publiée en juillet 2026. Ce n'est pas une norme de sécurité.
6. **SysML v2** est une norme OMG adoptée en juin 2025, mais son outillage libre est encore jeune : SysON se déclare lui-même pas encore prêt pour la production. Un essai pilote, pas une refonte.
7. **ISO 13482** : l'édition 2014 reste la référence publiée sur le site ISO ; l'édition 2 est en approbation finale (FDIS) depuis juillet 2025, et un laboratoire parle déjà d'« EN ISO 13482:2026 ». Statut à confirmer.
8. Deux références proches du Lab ont émergé : **BRIDGE** (0,8 à 0,88 m, environ 13 kg, 21 axes, environ 1 500 $, ouvert) et **LeRobot Humanoid** (12 RobStride, environ 2 500 $). Ce dernier existe bel et bien, contrairement à ce qu'affirmait l'agent de Claude Code.
9. Le manque principal n'est pas un optimiseur : c'est la boucle fermée exigence → test → mesure → modèle, la sécurité (AMDEC, arrêt indépendant) et l'identification sur banc.
10. Cadre recommandé : ISO 15288 et VDI 2206 allégés, conception ensembliste, exigences et tests en YAML contrôlés par le code, pymoo pour le Pareto, SysML v2 en pilote sur un sous-ensemble.

## 2. Méthodologies

Le coût d'apprentissage et l'adéquation « développeur seul » sont mon évaluation. Normes payantes : non ouvertes.

| Méthode | Origine | Apport pour YXOR | Coût | Seul ? |
| --- | --- | --- | --- | --- |
| ISO/IEC/IEEE 15288 | norme de cycle de vie système (2023) | liste des processus à ne pas oublier : exigences, architecture, intégration, V&V, configuration | moyen | oui, allégée |
| Cycle en V et VDI/VDE 2206 | directive mécatronique, révisée en 2021 | chaque exigence reçoit dès le départ sa méthode de vérification ; V imbriqués par domaine | faible | **oui, la plus adaptée** |
| VDI 2221, Pahl & Beitz | conception méthodique | clarifier les fonctions avant de choisir des pièces | moyen | oui, version courte |
| INCOSE (manuel, SEBoK) | association d'ingénierie système | référence de lecture, trop large à suivre en entier | élevé | non en entier |
| Ingénierie des exigences, QFD | pratique d'ingénierie système ; QFD née au Japon | relier « courir, porter » à couple, vitesse, course articulaire | faible | oui |
| Analyse morphologique | Zwicky | ton exploration en est une forme ; l'étendre aux architectures (placement moteur, transmission) | faible | oui |
| Conception axiomatique | Suh, MIT | repérer les choix qui couplent trop de fonctions | moyen | ponctuellement |
| DSM | Steward, Eppinger & Browning | voir quels choix se propagent (réduction, bus, batterie) | faible | oui |
| Conception ensembliste | Sobek, Ward & Liker (Toyota, 1999) | garder des intervalles admissibles, les réduire par les essais | faible | **oui** |
| MDO, OpenMDAO | aéronautique, NASA | coupler masse, thermique, coût quand les modèles seront stables | élevé | plus tard |
| Multi-objectif, NSGA-II, pymoo | Deb et al. 2002 | front de Pareto sans réécrire les algorithmes | faible | oui |
| TRIZ | Altshuller | résoudre une contradiction (rigidité contre masse) | moyen | optionnel |
| Jumeau numérique | pratique ; ToddlerBot, Booster Lab | un modèle corrigé par les mesures, pas un MJCF nominal | moyen | oui, ciblé |
| AMDEC | IEC 60812:2018 | pannes : bus perdu, moteur bloqué, chute, régénération | faible | **oui, avant tout essai dynamique** |
| TRL | NASA | ne pas dire « prêt » pour ce qui ne marche qu'en simulation | faible | oui |
| SysML v2 | OMG, adoptée le 30 juin 2025 (vérifié) | modèle formel textuel, adapté aux assistants IA | élevé | pilote seulement |
| Arcadia, Capella | Thales, Eclipse | architecture opérationnelle → physique | élevé | pas maintenant |

## 3. Méthodes propres aux robots à jambes

| Méthode | Ce qu'elle change pour YXOR | Référence |
| --- | --- | --- |
| **Lois d'échelle des bipèdes** (vérifié) | masse ∝ L^2,12 sur les robots publiés (R² 0,87) ; vitesse ∝ √L ; couple de marche ∝ m·L. Le couple croît donc comme L³ et non L⁴. **Réserve** : la loi de couple vient de simulations de marcheurs quasi passifs actionnés à la hanche, pas d'humanoïdes à genoux. | Oke, Carter, Gu, Man, Pride, Bergbreiter, Johnson, arXiv:2603.22560, 2026 (préprint) ; jeu de données robomechanics/robot-dataset |
| **Identification couple-vitesse** (vérifié) | mesurer la courbe couple-vitesse, prendre ses points de coude comme limites dans le simulateur, calculer l'inertie réfléchie N²·Jm | Booster Lab, arXiv:2606.27813, 2026 |
| **Co-conception forme-contrôle** (vérifié) | BRIDGE : co-conception guidée par le mouvement humain, robot construit (0,8 à 0,88 m, 12,5 à 13 kg, 21 axes, environ 1 500 $), comparé à ToddlerBot, Bumi et K1 ; ressources complètes promises après acceptation | arXiv:2609.03497, soumis à CoRL 2026 |
| Co-conception pour le relevé (vérifié) | RoboCraft : gain moyen annoncé de 44,55 % sur sept humanoïdes publics, en simulation | arXiv:2510.22336, 2025 |
| Actionnement proprioceptif, faible réduction | inertie réfléchie, rendement, thermique et transparence comptent autant que le couple de pointe | Seok et al. 2015 ; Wensing et al., IEEE TRO 2017 (non vérifié ici) |
| Plateforme d'actionnement commune | un module d'actionneur réutilisé sur plusieurs robots : précédent direct de ta stratégie à deux robots | ODRI, Grimminger et al., RA-L 2020 (non vérifié ici) |
| De la simulation au réel | randomisation autour d'incertitudes mesurées, pas arbitraires | Hwangbo et al., Science Robotics 2019 (non vérifié ici) |
| Essais normalisés de locomotion (vérifié) | méthodes pour spécifier et évaluer la locomotion des bipèdes et quadrupèdes ; pas une norme de sécurité | ISO 18646-5:2026 |

**Retours d'équipes.** Berkeley Humanoid Lite (vérifié) : réducteurs cycloïdaux imprimés, coût annoncé sous 5 000 $, 4 312 $ selon le tableau III de l'article. La fragilité ultérieure des actionneurs, citée par ChatGPT et par ma recherche du 2 octobre, n'a **pas été retrouvée** dans cette passe. ToddlerBot : calibration et identification moteur au cœur du jumeau numérique. Unitree, Agility, Apptronik : méthode de conception mécanique publique **non trouvée** (concordance des quatre rapports).

**Aucune démonstration** qu'une IA ait conçu seule un humanoïde fabricable : les travaux de co-conception optimisent un espace défini par des humains.

## 4. Outils

| Outil | Fonction | Licence | Prix | Linux/WSL | Pilotable par IA |
| --- | --- | --- | --- | --- | --- |
| **build123d** (vérifié) | CAO Python sur Open Cascade, dérivée en partie de CadQuery | Apache-2.0 | 0 | oui | excellent |
| CadQuery | idem, API plus ancienne | Apache-2.0 | 0 | oui | excellent |
| OpenSCAD | CSG textuel | GPL-2.0 | 0 | oui | bon, pièces simples |
| FreeCAD | CAO paramétrique + Python | LGPL | 0 | oui | moyen |
| Onshape + onshape-to-robot | CAO en ligne → URDF/MJCF | propriétaire ; outil MIT | gratuit si public (non vérifié ici) | navigateur | API |
| Fusion, SolidWorks | CAO commerciale | propriétaire | non vérifié ici | Windows | API, mal aligné avec Git |
| **SysML v2, implémentation pilote** (vérifié) | langage et API de référence | ouverte | 0 | Java, Jupyter | bon (texte) ; publications incrémentales, par exemple 2026-05 |
| **SysON** (vérifié) | éditeur web SysML v2 | EPL-2.0 (non vérifié ici) | 0 | oui | moyen ; le site le déclare encore en développement actif, pas prêt pour la production |
| Capella | MBSE Arcadia | EPL-2.0 | 0 | oui | faible (XML graphique) |
| OpenMDAO | MDO | Apache-2.0 | 0 | oui | excellent |
| pymoo | NSGA-II, Pareto | Apache-2.0 | 0 | oui | excellent |
| MuJoCo | simulation | Apache-2.0 | 0 | oui | déjà utilisé |

Divergence relevée : ChatGPT cite build123d 0.13.0 au 21 septembre 2026 ; j'ai trouvé 0.12.0, publiée sur PyPI le 18 septembre 2026. Sans conséquence.

## 5. Sécurité, par masse

**Aucune norme ne fixe de seuil « 10 kg » ou « 35 kg »** : les normes raisonnent par dangers et énergie (concordance des quatre rapports).

| Référence | Statut | Pour YXOR |
| --- | --- | --- |
| ISO 13482 (vérifié) | édition 2014 publiée ; édition 2 en approbation finale depuis le 24 juillet 2025 ; un laboratoire annonce déjà une version EN 2026 | référence principale : à confirmer avant de citer une édition |
| ISO 12100 | appréciation et réduction du risque | indispensable aux deux masses |
| ISO 13849-1, ISO 13850, IEC 60204-1 | fonctions de sécurité, arrêt d'urgence, équipement électrique | chaîne d'arrêt indépendante du logiciel |
| ISO/TS 15066 | limites de contact, contexte industriel | inspiration chiffrée, pas applicable directement |
| IEC 61508 | sécurité fonctionnelle | principes utiles ; cycle complet disproportionné |
| ISO 18646-5:2026 (vérifié) | performance, **pas sécurité** | pour les essais de locomotion |

**10 kg** : arrêt d'urgence physique, chien de garde, limites de courant, couple et température, coupure batterie, zone d'essai, mise sous couple progressive. **25 à 40 kg** : en plus, une coupure de puissance indépendante du calculateur et du bus, des modes à vitesse réduite, un portique ou un harnais pour les essais, pas d'essai dynamique dans une pièce habitée.

## 6. Documentation du matériel ouvert

DIN SPEC 3105 (exigences de documentation, sous licence CC), définition et certification OSHWA (fichiers source modifiables, nomenclature), Open Know-How (métadonnées). Non revérifiés ici ; concordance des trois rapports. Ton code build123d est précisément la « forme modifiable » qu'exige l'OSHWA ; publier aussi STEP, DXF et STL.

## 7. Comparaison avec ta méthode

### Ce que cette vérification change concrètement

1. **Loi de masse.** Le dépôt suppose masse ∝ H³ (ToddlerBot agrandi). Les données réelles disent environ H^2,1. Pour un robot deux fois plus haut : masse × 4,4 au lieu de × 8, couple × 8,7 au lieu de × 16. **Les chiffres du robot final sont probablement très surestimés**, ceux du Lab peu affectés (proche de ToddlerBot). Remarque : nos plaques à épaisseur fixe suivent déjà une loi en H².
2. **Spécification du banc.** Booster Lab donne le format de sortie : courbe couple-vitesse, points de coude, inertie réfléchie. À reprendre tel quel.
3. **Nouvelles références pour le Lab.** BRIDGE et LeRobot Humanoid sont plus proches du Lab que ToddlerBot (taille, masse, et pour LeRobot, mêmes moteurs RobStride).
4. **Niveaux de locomotion.** Aligner leurs définitions sur ISO 18646-5 quand la norme couvre la capacité. Elle est payante : achat soumis à ta règle 0066.

### Divergences entre les quatre rapports, et mon arbitrage

| Sujet | ChatGPT | Grok | Gemini | Mon avis |
| --- | --- | --- | --- | --- |
| SysML v2 | plus tard, pilote | pas maintenant | gagnant incontesté | **pilote sur un sous-ensemble** : la syntaxe textuelle est un vrai atout, l'outillage est jeune |
| Exploration exhaustive | à garder, robuste | réinventée | — | garder l'explorateur, sur un espace réduit d'avance (famille et 2 à 4 tailles) |
| Même famille pour les deux robots | préférence | stratégie éprouvée (ODRI) | — | garder : l'argument logiciel est fort |
| Mains et visage | avec le reste | un autre robot | — | les isoler |
| ISO 18646-5 | publiée 2026 | non citée | non citée | **vérifiée**, publiée en juillet 2026 |
| Loi m ∝ L² | citée | citée, avec chiffres | — | **vérifiée**, avec la réserve sur la loi de couple |

### Ce qui manque encore

Exigences identifiées avec leur méthode de vérification ; interfaces décrites (fixation, connecteur, bus, limites, comportement en cas de perte de communication) ; statut « inconnu » explicite dans l'explorateur, avec les mesures nécessaires ; AMDEC ; hiérarchie d'essais (actionneur → articulation → jambe → robot sous portique) ; contrat de version matérielle (un robot physique pointe vers un commit, une nomenclature, une calibration).

## 8. Recommandation

**Cadre** : ISO 15288 et VDI 2206 allégés, conception ensembliste, vérification « en code ». Pas de refonte du dépôt.

**Ordre proposé** (PROPOSÉ, pas décidé) :

1. Corriger la loi de masse (exposant mesuré, avec intervalle), puis relancer les chiffres du final.
2. Exigences, interfaces, dangers et tests en YAML, contrôlés automatiquement comme le reste du dépôt.
3. AMDEC et chaîne d'arrêt **avant** toute mise sous tension. Elles rejoignent deux décisions en attente : délai du chien de garde, seuil d'arrêt sous 60 V.
4. Banc sur le modèle de Booster Lab : il produit des paramètres de simulation, pas seulement un verdict.
5. Explorateur sur un espace réduit, Pareto avec pymoo.
6. SysML v2 en pilote sur une articulation de jambe, à côté du YAML.
7. Documentation DIN SPEC 3105 et OSHWA au fil de l'eau.

## 9. Registre des sources vérifiées

| Source | Type | Date | Lien |
| --- | --- | --- | --- |
| Oke et al., Allometric Scaling Laws for Bipedal Robots | préprint | 2026 | https://arxiv.org/abs/2603.22560 |
| robomechanics/robot-dataset (ajustements en loi de puissance) | données | 2026 | https://github.com/robomechanics/robot-dataset |
| ISO 18646-5 (page ISO, puis CCN : publiée le 2026-07-23) | norme | 2026 | https://www.iso.org/standard/86850.html |
| ISO/FDIS 13482, édition 2 | projet de norme | stade 50.00, 2025-07-24 | https://www.iso.org/standard/83498.html |
| SysML v2 Release (OMG, adoption 30 juin 2025) | spécification, implémentation pilote | 2026 | https://github.com/Systems-Modeling/SysML-v2-Release |
| SysON | outil | 2026 | https://mbse-syson.org/ |
| Booster Lab | préprint | 2026 | https://arxiv.org/pdf/2606.27813 |
| BRIDGE | préprint, soumis CoRL 2026 | 2026 | https://arxiv.org/abs/2609.03497 |
| RoboCraft | préprint | 2025 | https://arxiv.org/pdf/2510.22336 |
| Berkeley Humanoid Lite | article RSS 2025 | 2025 | https://arxiv.org/pdf/2504.17249 |
| build123d | dépôt, PyPI | 2026 | https://github.com/gumyr/build123d |
| LeRobot Humanoid (source secondaire) | presse | 2026 | https://www.techeblog.com/?p=244716 |

**Non ouverts** : textes intégraux des normes ISO, IEC, VDI et DIN ; prix actuels de Fusion, SolidWorks et Onshape ; dépôt primaire de LeRobot Humanoid (vérification confiée à Claude Code, phase 3b, point 0).
