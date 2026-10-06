# 1. Résumé en 10 lignes

1. **Ta méthode actuelle est déjà bien alignée avec l’état de l’art** : elle combine implicitement conception ensembliste, exploration d’espace de conception, optimisation multiobjectif, modélisation physique et vérification expérimentale.
2. Le meilleur cadre global pour YXOR n’est pas une méthode exotique supplémentaire, mais un **ISO/IEC/IEEE 15288 allégé + VDI/VDE 2206 allégé**, adaptés à un développeur seul. :chatgpt-content-reference{index="0"}
3. **VDI 2221/Pahl & Beitz** peuvent structurer la conception fonctionnelle et conceptuelle, mais une grande partie est déjà présente dans ton processus ; il ne faut pas dupliquer ta chaîne pour leur ressembler.
4. La lacune principale est la **traçabilité formelle besoin → exigence → fonction → architecture → paramètre → modèle → test → résultat**, plus que l’optimisation elle-même.
5. Pour la locomotion, la grande nouveauté de 2026 est **ISO 18646-5:2026**, qui fournit justement des méthodes de mesure pour vitesse, distance d’arrêt et franchissement des robots à jambes : tes « niveaux de capacité » devraient en reprendre autant que possible la terminologie. :chatgpt-content-reference{index="1"}
6. La littérature MIT Cheetah montre que le dimensionnement doit considérer **couple-vitesse continu, densité de couple, inertie de jambe, pertes de transmission, thermique et régénération**, et pas seulement le couple crête. :chatgpt-content-reference{index="2"}
7. ToddlerBot et Berkeley Humanoid montrent que la **calibration, l’identification système, la réparabilité et la résistance aux chutes** sont aussi importantes que la qualité du modèle CAO/MuJoCo. :chatgpt-content-reference{index="3"}
8. Le passage 0,6 m → 1,2 m ne doit pas être traité comme un simple agrandissement géométrique : les travaux récents sur les lois d’échelle des bipèdes montrent justement des comportements non isométriques ; le robot d’apprentissage est donc surtout un démonstrateur logiciel/méthodologique. :chatgpt-content-reference{index="4"}
9. Pour un usage domestique, **il n’existe pas de seuil normatif simple 10 kg/35 kg** : ISO 13482/ISO 12100 raisonnent d’abord en dangers et risques ; le 35 kg exige néanmoins une architecture de sûreté beaucoup plus sévère par son énergie et ses forces potentielles. :chatgpt-content-reference{index="5"}
10. Je conserverais **build123d + Python + MuJoCo + YAML/Git**, j’ajouterais maintenant `requirements/tests/interfaces/hazards`, `pymoo`, un banc de caractérisation actionneur et une boucle de calibration ; **SysML v2/Capella seulement lorsque la complexité justifiera leur coût**.

---

# 2. Tableau des méthodologies d’ingénierie

Les colonnes « coût d’apprentissage » et « adapté solo » sont mon évaluation pour **YXOR**, pas une propriété normative de ces méthodes.

| Méthode / cadre | Origine / statut | Ce qu’elle apporte concrètement à YXOR | Apprentissage | Solo ? |
|---|---|---|---|---|
| **ISO/IEC/IEEE 15288:2023** | Norme internationale de processus du cycle de vie système. :chatgpt-content-reference{index="6"} | Ossature générale : besoins, exigences, architecture, implémentation, intégration, V&V, configuration, gestion des risques. Permet surtout d’éviter les « trous » de processus. | Moyen | **Oui**, adaptée |
| **INCOSE Systems Engineering Handbook v5** | Guide de bonnes pratiques 2023 aligné notamment sur 15288. :chatgpt-content-reference{index="7"} | Version beaucoup plus utilisable de l’ingénierie système que la lecture brute de normes. Bon référentiel pour construire ton processus YXOR. | Moyen | **Oui** |
| **Cycle en V** | Principe d’ingénierie reliant niveaux de décomposition et niveaux de vérification/intégration ; repris et étendu pour la mécatronique par VDI 2206. :chatgpt-content-reference{index="8"} | À chaque exigence ou niveau de conception correspond dès le départ une méthode de vérification. Exactement ce qui manque à ton pipeline actuel. | Faible | **Oui** |
| **VDI/VDE 2206:2021** | Directive pour systèmes mécatroniques et cyberphysiques. :chatgpt-content-reference{index="9"} | Probablement le cadre **le plus directement adapté à YXOR** : mécanique + électronique + logiciel + modèles + intégration dans un V étendu. | Moyen | **Oui**, fortement |
| **VDI 2221:2019** | Méthode systématique de conception de produits et systèmes techniques. :chatgpt-content-reference{index="10"} | Clarification du problème → fonctions → principes de solution → architecture → réalisation. Utile avant de figer axes et actionneurs. | Moyen | **Oui** |
| **Pahl & Beitz** | Méthodologie classique de conception mécanique systématique ; *Engineering Design: A Systematic Approach*. :chatgpt-content-reference{index="11"} | Très bon cadre de conception conceptuelle/embodiment ; utile pour éviter de passer directement d’une exigence à une pièce CAO. | Moyen | **Oui** |
| **Requirements Engineering** | Discipline transverse de l’ingénierie système | Donne à chaque exigence un identifiant, une valeur cible, des marges, une justification, un parent et surtout une méthode de vérification. | Faible-moyen | **Oui, indispensable** |
| **QFD / House of Quality** | Méthodologie développée au Japon à partir de la fin des années 1960 pour transformer besoins en caractéristiques techniques. :chatgpt-content-reference{index="12"} | Excellent pour transformer « courir », « porter lourd », « sûr dans une maison » en propriétés d’ingénierie mesurables et repérer les antagonismes. | Faible | **Oui**, version légère |
| **Analyse morphologique** | Fritz Zwicky ; exploration systématique des combinaisons de solutions. :chatgpt-content-reference{index="13"} | Ton exploration `axes × actionneurs × taille` en est déjà une forme. À étendre aux architectures : transmission, placement moteur, structure, pied, capteurs, refroidissement… | Faible | **Oui** |
| **Axiomatic Design** | Nam P. Suh, MIT ; axiomes d’indépendance et d’information. :chatgpt-content-reference{index="14"} | Détecter les architectures où une même décision affecte trop d’exigences fonctionnelles ; très utile sur les articulations et modules jambe. | Moyen | **Oui**, ponctuellement |
| **DSM – Design Structure Matrix** | Eppinger & Browning, MIT, 2012. :chatgpt-content-reference{index="15"} | Cartographie les dépendances mécanique/électrique/logiciel/commande. Très bonne façon de décider les limites des modules et l’ordre d’intégration. | Faible-moyen | **Oui**, excellent rapport coût/bénéfice |
| **Set-Based Design / SBCE** | Notamment Sobek, Ward & Liker sur Toyota, 1999. :chatgpt-content-reference{index="16"} | Ne pas choisir trop tôt *un* moteur ou *une* géométrie ; maintenir des ensembles admissibles puis les réduire à mesure que les essais éliminent les variantes. | Faible-moyen | **Oui, excellent** |
| **Design Space Exploration** | Famille de techniques numériques | C’est déjà le cœur de ta méthode. Elle doit devenir reproductible, versionnée et robuste aux incertitudes. | Moyen | **Oui** |
| **MDO – Multidisciplinary Design Optimization** | Ingénierie aérospatiale/systèmes complexes ; OpenMDAO est un framework open source reconnu. :chatgpt-content-reference{index="17"} | Coupler masse, géométrie, mécanique, thermique, énergie, contrôle, coût au lieu d’optimiser chaque discipline séparément. | Élevé | **Oui**, mais seulement lorsque nécessaire |
| **Optimisation multiobjectif / Pareto / NSGA-II** | Deb, Pratap, Agarwal & Meyarivan, 2002. :chatgpt-content-reference{index="18"} | Formalise exactement ton compromis coût–masse–performance–température–énergie. | Moyen | **Oui**, immédiatement |
| **TRIZ** | Altshuller et travaux ultérieurs. :chatgpt-content-reference{index="19"} | Bon outil de résolution lorsqu’une contradiction persiste : rigidité ↔ masse, réduction ↔ backdrivability, protection ↔ refroidissement… | Faible-moyen | **Oui**, mais secondaire |
| **Jumeau numérique** | Concept désormais normalisé dans plusieurs domaines ; ISO 23247 propose notamment un cadre pour l’industrie manufacturière. :chatgpt-content-reference{index="20"} | Pour YXOR : **pas juste le MJCF**, mais un modèle dont les paramètres sont corrigés par les mesures réelles et liés à la version physique du robot. | Moyen-élevé | **Oui** |
| **AMDEC/FMEA/FMECA** | IEC 60812:2018. :chatgpt-content-reference{index="21"} | Analyse systématique des modes de panne : encodeur, connecteur, bus, moteur bloqué, vis desserrée, surchauffe, chute, regen, alimentation… | Moyen | **Oui**, très recommandée |
| **TRL** | NASA, échelle 1–9. :chatgpt-content-reference{index="22"} | Empêche de qualifier « mature » une fonction qui fonctionne seulement dans MuJoCo. Appliquer le TRL **par sous-système et capacité**, pas seulement au robot entier. | Faible | **Oui** |
| **Vérification & validation** | Discipline centrale du SE ; NASA décrit notamment analyse, inspection, démonstration et test comme méthodes de vérification. :chatgpt-content-reference{index="23"} | Chaque `REQ-*` doit aboutir à une preuve `TEST-*`, `ANALYSIS-*`, `INSPECTION-*` ou `DEMO-*`. | Moyen | **Oui, indispensable** |
| **SysML v2** | OMG, version formelle 2.0 depuis septembre 2025 ; syntaxe textuelle, modèle abstrait et représentation JSON normalisée. :chatgpt-content-reference{index="24"} | Peut rendre explicites exigences, parties, connexions, interfaces, comportements, allocations et relations de vérification. | Élevé | **Oui**, mais léger |
| **Arcadia / Capella** | Méthode MBSE et outil Eclipse ; Capella 7.1.0 publié en juillet 2026. :chatgpt-content-reference{index="25"} | Très fort pour architecture opérationnelle, système, logique et physique. Pour YXOR solo, risque de devenir une deuxième base de données à maintenir. | Élevé | **Non** comme outil quotidien initial |

### Le point important sur le MBSE

Je **ne te conseille pas de migrer YXOR aujourd’hui vers un énorme modèle SysML/Capella**. SysML v2 est désormais une norme formelle et sa syntaxe textuelle le rend beaucoup plus compatible avec Git et les assistants IA que SysML v1, mais son écosystème open source reste moins mature que ton environnement Python/YAML. L’implémentation pilote SysML v2 continue d’évoluer en 2026. :chatgpt-content-reference{index="26"}

En revanche, je te conseille de faire du **MBSE sans nécessairement utiliser immédiatement un outil MBSE** : un modèle système formel, versionné et interrogeable est déjà possible avec tes fichiers en code.

---

# 3. Méthodes propres aux robots humanoïdes et à jambes

## 3.1 Les méthodes réellement importantes

| Méthode | Ce que dit la littérature | Conséquence YXOR | Référence |
|---|---|---|---|
| **Design for dynamic legged locomotion** | Le MIT Cheetah a été conçu autour de moteurs à forte densité de couple, transmissions peu dissipatives, électronique régénérative et faible inertie des jambes. Les pertes moteurs dominaient fortement le budget énergétique dans l’analyse publiée. | Ton critère « couple » doit devenir un **enveloppe couple–vitesse–courant–température–durée**, complétée par inertie rotor/transmission et rendement. | Seok et al., *Design Principles for Energy-Efficient Legged Locomotion…*, 2015. :chatgpt-content-reference{index="27"} |
| **Actionnement proprioceptif** | MIT Cheetah privilégie une transmission permettant une interaction physique à haute bande passante et une estimation/commande du couple côté articulation. | Couple élevé sans transparence/backdrivability suffisante peut être un mauvais choix, même avec un excellent rapport Nm/€. | Wensing et al., *Proprioceptive Actuator Design in the MIT Cheetah*, 2017. :chatgpt-content-reference{index="28"} |
| **QDD / faible réduction** | La littérature Cheetah montre l'intérêt des moteurs coupleux et réductions modestes pour réduire inertie réfléchie, pertes et impacts. :chatgpt-content-reference{index="29"} | À comparer objectivement aux réducteurs à fort ratio de tes actionneurs commerciaux ; « QDD » n’est pas automatiquement supérieur si masse, coût ou thermique deviennent prohibitifs. | Kim & Wensing, *Design of Dynamic Legged Robots*, 2017. |
| **Co-design mécanique–commande** | Des travaux optimisent simultanément variables morphologiques et contrôleurs au lieu de fixer d’abord la mécanique. :chatgpt-content-reference{index="30"} | Ton pipeline doit progressivement passer de `mécanique → contrôleur` à `mécanique ↔ contrôleur`, au moins pour jambes/pieds. | Koike, Ariizumi & Matsuno, 2023/24. |
| **Co-adaptation morphologie–RL** | Du et al. emploient une boucle bi-niveau : paramètres de conception à l’extérieur, politique de locomotion à l’intérieur, accélérée par surrogate. L’étude reste essentiellement en simulation et **ne valide pas le robot optimisé physiquement**. | Piste intéressante pour YXOR plus tard ; surtout pas une preuve que « l’IA conçoit automatiquement un humanoïde ». | Du et al., *Efficient co-adaptation…*, 2025. :chatgpt-content-reference{index="31"} |
| **Lois d’échelle / similarité dynamique** | Une étude 2026 sur les bipèdes constate que les robots existants ne suivent pas simplement la loi isométrique `masse ∝ L³`; elle étudie notamment vitesse, couple et géométrie en fonction de la taille. C’est un **préprint**. | Le 0,6 m ne permet pas de simplement multiplier chaque cote par 2 pour obtenir le 1,2 m. Refaire les analyses structurelles, thermiques et dynamiques. | Oke et al., *Allometric Scaling Laws for Bipedal Robots*, 2026, préprint. :chatgpt-content-reference{index="32"} |
| **Dimensionnement depuis des mouvements humains/robot** | Des travaux récents dérivent exigences vitesse/accélération/couple à partir de trajectoires articulaires de mouvements. | Très proche de ta méthode « capacité → tâche → charge articulaire » : bonne direction. | *Humanoid Robot Design Assistant – Requirements from Human Motion*, IEEE Humanoids 2024. :chatgpt-content-reference{index="33"} |
| **Dimensionnement électromécanique multiobjectif** | Des travaux comme Mithra examinent moteur, transmission, contraintes, fatigue, backdrivability et bande passante. | Ajouter au Pareto YXOR des critères électromécaniques actuellement sous-représentés. | Semasinghe et al., *Design of Actuators for a Humanoid Robot…*, 2025. :chatgpt-content-reference{index="34"} |
| **System identification** | ToddlerBot identifie la dynamique de son actionnement réel puis réinjecte ces paramètres dans son modèle de simulation. | Le banc actionneur YXOR doit produire les paramètres de ton MJCF, pas seulement valider une datasheet. | Shi et al., ToddlerBot, 2025. :chatgpt-content-reference{index="35"} |
| **Domain randomization / sim-to-real** | Hwangbo et al. entraînent en simulation puis transfèrent à ANYmal ; RMA ajoute une adaptation rapide aux paramètres inconnus. :chatgpt-content-reference{index="36"} | Randomiser **autour d’incertitudes mesurées**, plutôt que d’utiliser une randomisation arbitraire pour masquer un mauvais modèle. | Hwangbo 2019 ; Kumar et al. 2021 |
| **Perceptive locomotion** | Miki et al. combinent proprioception et perception du terrain pour évoluer sur terrains difficiles. | Pour le niveau final « irrégulier/pente », ton modèle de capacité devra inclure perception, latence, incertitude et récupération des erreurs, pas seulement dynamique idéale. | Miki et al., 2022. :chatgpt-content-reference{index="37"} |
| **Tests de locomotion standardisés** | ISO 18646-5:2026 normalise des méthodes d’évaluation de performances des robots à jambes, notamment vitesse nominale, distance d’arrêt et capacité de franchissement. Ce n’est pas une norme de sécurité. | Très fort potentiel pour remplacer une partie de tes niveaux maison par des essais reproductibles et comparables. | ISO 18646-5:2026. :chatgpt-content-reference{index="38"} |

### Un avertissement important sur les lois d’échelle

L’idée de **partager une même famille d’actionneurs** entre les deux YXOR reste excellente pour le logiciel, le bus, les outils, les pièces détachées et la méthode. Mais je traiterais désormais :

> « même famille d’actionneurs »

comme une **préférence architecturale à scorer**, et non comme une exigence irrévocable.

La raison est simple : doubler la longueur caractéristique ne double pas nécessairement les charges, la rigidité nécessaire, l’inertie, les contraintes dans les roulements, l’énergie de chute ou le problème thermique de la même façon. Les résultats allométriques 2026 renforcent précisément l’idée qu’un changement d’échelle robotique n’est pas purement géométrique. :chatgpt-content-reference{index="39"}

---

## 3.2 Comment les équipes ayant construit des robots s’y sont prises

| Robot / équipe | Méthode publique observable | Erreurs / enseignements publics |
|---|---|---|
| **MIT Cheetah** | Conception moteur/transmission/structure/commande comme un ensemble ; métriques physiques choisies expressément pour la locomotion dynamique. :chatgpt-content-reference{index="40"} | Le rendement réel, l’échauffement et l’inertie du membre comptent autant que le couple nominal. |
| **Cheetah 3** | Architecture mécanique adaptée à la locomotion robuste + actionnement proprioceptif à haute bande passante ; le contrôle exploite la conception mécanique au lieu de compenser une mécanique inadéquate. :chatgpt-content-reference{index="41"} | Leçon générale : simplifier le problème de commande par la mécanique. |
| **Berkeley Humanoid** | Conçu explicitement pour l’apprentissage : modèle de simulation relativement simple, proportions humanoïdes, capacité à supporter de nombreuses chutes. :chatgpt-content-reference{index="42"} | 38 chutes rapportées sur divers sols ; deux défaillances matérielles attribuées à des vis/adhésif. Les auteurs demandent notamment meilleure amplitude, réduction du backlash, amélioration résistance/masse et meilleur modèle couple-courant près de la saturation. :chatgpt-content-reference{index="43"} |
| **Berkeley Humanoid Lite** | Humanoïde open source < 5 k$, construction modulaire, pièces et réducteurs largement imprimés 3D. Article RSS 2025. :chatgpt-content-reference{index="44"} | Retour projet particulièrement intéressant : les actionneurs cycloïdaux imprimés ont été jugés trop fragiles pour certaines tâches hautes performances et les connecteurs/câbles insuffisamment fiables ; les auteurs envisagent davantage d’actionneurs commerciaux. :chatgpt-content-reference{index="45"} |
| **ToddlerBot** | 0,56 m, ~3,4 kg, architecture reproductible et bon marché ; CAO → modèle robot, calibration fréquente facilitée par fixtures, identification moteur, jumeau numérique, sim-to-real. :chatgpt-content-reference{index="46"} | Très bon contre-exemple à l’idée qu’une calibration ponctuelle suffit : la réparabilité et la recalibration font partie de l’architecture. |
| **ODRI** | Modules d’actionneurs BLDC commandés en couple, bas coût, réutilisés sur plusieurs robots ; matériel et logiciel largement ouverts. :chatgpt-content-reference{index="47"} | Une **plateforme d’actionnement commune** entre robots est donc une stratégie réellement éprouvée — très proche de ton idée de famille commune YXOR. |
| **Cassie / Agility** | Les travaux académiques publics montrent des équipes développant leurs propres piles de contrôle et les validant sur matériel réel et terrains variés. :chatgpt-content-reference{index="48"} | Le détail des arbitrages mécaniques internes d’Agility est nettement moins public que la littérature de contrôle. **Retour complet de conception interne : non trouvé.** |
| **Digit / Agility** | Des travaux académiques ont utilisé des architectures hiérarchiques de contrôle et démontré du transfert simulation-réel. :chatgpt-content-reference{index="49"} | Les publications récentes de l’entreprise sur ses modèles de whole-body control sont intéressantes, mais restent des **communications industrielles**, pas une validation indépendante de toute leur méthodologie. :chatgpt-content-reference{index="50"} |
| **Unitree H1/G1/H2** | SDK, modèles URDF/MJCF et interfaces développeur sont accessibles publiquement. :chatgpt-content-reference{index="51"} | **Méthode complète de conception et registre public des erreurs d’ingénierie : non trouvé.** Ne pas reconstruire leur processus à partir de leur marketing produit. |
| **Booster T1** | Documentation développeur publique : entraînement avec Isaac Gym, cross-simulation MuJoCo et déploiement ; T1 documenté comme robot 23 DoF. :chatgpt-content-reference{index="52"} | **Trade studies mécaniques et post-mortem public détaillé : non trouvé.** |
| **Apptronik / Valkyrie → Apollo** | Apptronik rattache son expérience aux travaux NASA Valkyrie et décrit l’emploi d’actionneurs élastiques sur Valkyrie. :chatgpt-content-reference{index="53"} | L’affirmation selon laquelle ces enseignements se retrouvent dans Apollo vient de l’entreprise elle-même : à considérer comme **retour industriel/vendor**, pas comme démonstration scientifique indépendante. |
| **MIT Humanoid** | Les travaux du Biomimetic Robotics Lab montrent un projet humanoïde actif. :chatgpt-content-reference{index="54"} | **Publication publique suffisamment détaillée décrivant son processus complet de dimensionnement mécanique : non trouvée** dans cette recherche. |

### Ce que ces équipes ont en commun

Le point récurrent n’est pas « elles disposent d’un meilleur optimiseur ». C’est plutôt :

**mécanique adaptée au contrôle → modèles simples mais suffisamment fidèles → bancs et identification → beaucoup d’essais → réparation/calibration rapides → retour des données réelles vers le modèle.**

C’est particulièrement manifeste chez MIT Cheetah, ToddlerBot, Berkeley Humanoid et ODRI. :chatgpt-content-reference{index="55"}

Et je n’ai trouvé **aucune démonstration crédible d’une IA ayant conçu de manière autonome un humanoïde complet**, depuis les besoins jusqu’à un matériel validé. Les travaux de co-design automatisent un espace de conception **défini par des humains**, avec des objectifs, paramètres et contraintes eux-mêmes conçus par les ingénieurs ; le travail 2025 de Du et al., par exemple, reste sans prototype construit pour la morphologie optimisée. :chatgpt-content-reference{index="56"}

---

# 4. Chaîne « tout en code » et outils

## 4.1 CAO / robot description / optimisation

| Outil | Fonction | Licence / prix vérifié 2026 | Linux / WSL | Automatisation / IA | État 2026 | Verdict YXOR |
|---|---|---|---|---|---|---|
| **build123d** | CAO B-Rep paramétrique Python/OpenCascade | Apache-2.0 ; **0 €** | Linux oui ; WSL normalement exploitable | **Excellent** : Python natif, Git/diff/test | Actif ; 0.13.0 publié le 21 sept. 2026. :chatgpt-content-reference{index="57"} | **Garder comme source CAO principale** |
| **CadQuery** | CAO paramétrique Python/OpenCascade | Apache-2.0 ; **0 €** | Linux oui | Excellent | Actif ; 2.8.0 juin 2026 et activité repo en oct. 2026. :chatgpt-content-reference{index="58"} | Très bonne alternative ; migration inutile sans besoin précis |
| **OpenSCAD** | CSG déclaratif textuel | GPL-2.0 ; **0 €**. :chatgpt-content-reference{index="59"} | Linux natif | Excellent pour IA/code | Actif ; stable historique 2021.01 mais snapshots de développement 2026. :chatgpt-content-reference{index="60"} | Excellent pour pièces simples ; moins adapté comme CAD mécanique principal de l’humanoïde |
| **FreeCAD** | CAO paramétrique généraliste + Python | Documentation officielle : LGPL v2 ou ultérieure ; repo moderne généralement exprimé LGPL-2.1-or-later ; **0 €**. :chatgpt-content-reference{index="61"} | Linux natif | Bon via Python, mais modèle d’état plus lourd | Actif ; 1.1.3 juillet 2026. :chatgpt-content-reference{index="62"} | Excellent outil secondaire STEP/inspection/atelier |
| **Onshape** | CAO cloud, assemblages, versioning/PDM | Propriétaire. Free **0 $** avec restrictions/non-commercial et documents publics ; Standard **1 500 $/utilisateur/an**, Professional **2 500 $/an**, Enterprise sur devis. :chatgpt-content-reference{index="63"} | Oui via navigateur | Très bon via API | Actif | Alternative sérieuse si gestion d’assemblages/PDM devient plus importante que Git-first |
| **onshape-to-robot** | Onshape → URDF/SDF/MuJoCo | MIT ; **0 €**. :chatgpt-content-reference{index="64"} | Linux/Python | **Excellent** | Projet public ; cadence exacte récente non établie ici | Très intéressant si Onshape devient CAO maître |
| **Fusion 360 / Fusion** | CAD/CAM/CAE/PCB | Propriétaire ; abonnement Fusion de base affiché autour de **680 $/an** au moment de la recherche. :chatgpt-content-reference{index="65"} | **Pas de client Linux natif** ; navigateur disponible sous certaines licences/conditions. :chatgpt-content-reference{index="66"} | API Python/C++, TypeScript en évolution. :chatgpt-content-reference{index="67"} | Actif | Très utile CAM/atelier ; mauvais choix comme source de vérité « everything-as-code » |
| **SOLIDWORKS** | CAD mécanique industriel | Propriétaire ; offres annuelles USA consultées : Standard **2 820 $**, Professional **3 456 $**, Premium **4 716 $**, hors taxes. :chatgpt-content-reference{index="68"} | Windows ; Linux/WSL non supporté officiellement. :chatgpt-content-reference{index="69"} | API COM et macros très riche. :chatgpt-content-reference{index="70"} | Actif | Excellente interop industrielle mais mauvais alignement avec ton architecture Linux/Git/IA |
| **MuJoCo** | Dynamique / simulation robotique | Déjà choisi par toi | Linux oui | Très bon via Python/MJCF | Actif | **À garder** |
| **OpenMDAO** | MDO, couplage disciplines, dérivées/optimisation | Apache-2.0 ; **0 €** ; projet déclaré Production/Stable. :chatgpt-content-reference{index="71"} | Linux/Win/macOS | **Excellent**, Python | Actif | Ajouter lorsque calcul structure/thermique/électrique/commande deviennent véritablement couplés |
| **pymoo** | Optimisation multiobjectif : NSGA-II, Pareto, contraintes… | Apache-2.0 ; **0 €** ; version publiée juin 2026. :chatgpt-content-reference{index="72"} | OS indépendant | **Excellent**, Python | Actif | **À ajouter maintenant** |
| **Capella** | MBSE Arcadia | EPL-2.0 ; **0 €**. :chatgpt-content-reference{index="73"} | Linux oui | Automatisable/extensions, moins naturel pour agent IA qu’un DSL textuel | Actif ; 7.1.0 juillet 2026. :chatgpt-content-reference{index="74"} | Introduire seulement si l’architecture devient difficile à maîtriser dans les fichiers |
| **SysML v2 Pilot / ref. implementation** | SysML v2 textuel, API/services | EPL dans les releases actuelles ; **0 €** | Java/Jupyter/plateforme ouverte | **Potentiellement excellent pour l’IA** grâce à la syntaxe textuelle/API | Actif ; release 2026-07 publiée en août 2026. :chatgpt-content-reference{index="75"} | À surveiller / expérimenter sur un sous-modèle ; pas encore faire dépendre YXOR entier de lui |

### Mon choix pour YXOR

Je construirais une chaîne de ce type :

```text
                     ┌─────────────────────┐
                     │ requirements/*.yaml │
                     │ hazards/*.yaml      │
                     │ interfaces/*.yaml   │
                     └─────────┬───────────┘
                               │
                       validation schéma
                               │
                   ┌───────────▼──────────┐
                   │  robot_model Python │
                   │  source de vérité   │
                   └─────┬─────┬─────┬───┘
                         │     │     │
          ┌──────────────┘     │     └──────────────┐
          ▼                    ▼                    ▼
    build123d CAD          URDF / MJCF          BOM / coûts
          │                    │                    │
     STEP/DXF/STL            MuJoCo             fournisseurs
          │                    │                    │
          └──────────────┬─────┴───────────────┬────┘
                         ▼                     ▼
                  simulations/DSE         tests physiques
                         │                     │
                         └─────────┬───────────┘
                                   ▼
                          données / calibration
                                   │
                                   ▼
                           modèle mis à jour
```

Autrement dit : **la CAO ne devrait pas être la source de vérité du robot**. Le *modèle système paramétrique* devrait l’être ; la CAO, le MJCF, le BOM et les essais devraient en être des projections.

C’est la conséquence logique de ta démarche « everything-as-code ».

---

# 5. Sécurité : 10 kg puis ~35 kg

## D’abord, une correction importante

Je n’ai trouvé **aucune norme donnant une frontière générale “10 kg = telle réglementation, 35 kg = telle autre”**. Les normes pertinentes classent surtout le robot par usage et évaluent les **phénomènes dangereux, exposition, énergie, contact et fonctions de sécurité**.

### Normes

| Référence | Statut / portée | YXOR ~10 kg | YXOR ~35 kg |
|---|---|---:|---:|
| **ISO 13482:2014** | Sécurité des robots de soins personnels/service. Édition actuelle encore publiée ; un **ISO/FDIS 13482 édition 2** est en cours d’approbation en 2026. :chatgpt-content-reference{index="76"} | **Référence principale** | **Référence principale** |
| **ISO 12100:2010** | Principes généraux de conception sûre et analyse/réduction des risques. :chatgpt-content-reference{index="77"} | **Oui** | **Oui, essentiel** |
| **ISO 10218-1:2025** | Robots industriels ; exclut notamment certains robots de service accessibles au public/produits domestiques. :chatgpt-content-reference{index="78"} | Pas directement applicable au YXOR domestique | Pas directement applicable ; bonnes pratiques utiles en labo |
| **ISO/TS 15066:2016** | Systèmes collaboratifs industriels ; pas une norme générale de robot domestique. :chatgpt-content-reference{index="79"} | Inspiration pour contact/force | Très utile comme référence technique, mais ne pas prétendre à son applicabilité directe |
| **ISO 13849-1:2023** | Parties des systèmes de commande relatives à la sécurité. :chatgpt-content-reference{index="80"} | Utile | **Très importante** si l’on formalise une chaîne de sûreté |
| **ISO 13850:2015** | Principes de conception de l’arrêt d’urgence. :chatgpt-content-reference{index="81"} | Oui | **Oui** |
| **IEC 60204-1:2016 + AMD1:2021** | Équipements électriques des machines ; arrêt, circuits de commande, entraînements, STO notamment. :chatgpt-content-reference{index="82"} | Bonne référence labo | **Forte référence d’ingénierie** |
| **IEC 61508:2010** | Norme générique de sécurité fonctionnelle E/E/PE. :chatgpt-content-reference{index="83"} | Les principes sont utiles ; cycle SIL complet probablement disproportionné pour un prototype personnel | Plus pertinente si tu veux ultérieurement démontrer une intégrité de sécurité formelle |
| **IEC 60812:2018** | FMEA/FMECA. :chatgpt-content-reference{index="84"} | **Oui** | **Oui** |
| **ISO 18646-5:2026** | Performance locomotrice des robots à jambes ; **explicitement pas une norme de sécurité**. :chatgpt-content-reference{index="85"} | Oui pour tests | Oui pour tests |

### Architecture minimale que je prévoirais

Pour le **YXOR d’apprentissage ~10 kg**, je voudrais déjà : arrêt d’urgence local et accessible, watchdog, limites logicielles de courant/couple/vitesse/température, protections batterie/BMS, détection perte bus, procédure de mise sous couple, essais dynamiques avec espace contrôlé/tether ou support lorsque nécessaire, et modes de commissioning à énergie réduite. C’est une recommandation d’ingénierie dérivée de l’approche ISO 12100/13849/13850/60204, et non une citation mot pour mot d’une exigence normative. :chatgpt-content-reference{index="86"}

À **~35 kg**, j’ajouterais une **chaîne d’arrêt aussi indépendante que raisonnablement possible du calculateur principal et du réseau**, un moyen physique de supprimer le couple/énergie des entraînements — STO si les drives le permettent ou architecture équivalente —, validation documentée des fonctions d’arrêt, modes de déplacement à vitesse/couple réduits, zone de chute contrôlée lors du développement, stratégie contre l’écrasement/coincement, gestion de l’énergie potentielle pendant maintenance et essais, et limites de contact humain explicitement testées.

Un arrêt d’urgence affiché dans l’interface graphique **n’est pas un arrêt d’urgence de sûreté**.

### Le 10 kg n’est déjà plus un « petit jouet »

ToddlerBot mesure environ 0,56 m pour seulement ~3,4 kg. Ton prototype de 0,6 m visant ~10 kg concentre donc beaucoup plus de masse à une taille comparable : il faut éviter de transposer implicitement les hypothèses de sécurité d’un petit robot imprimé 3D. :chatgpt-content-reference{index="87"}

---

## 5 bis. Documentation matériel ouvert

Trois références valent la peine d’être intégrées directement au projet.

**DIN SPEC 3105-1:2020** définit des exigences pour la documentation technique de matériel open source ; le document est actuellement répertorié comme courant, téléchargeable gratuitement et publié sous CC BY-SA 4.0 sauf éléments spécifiés. :chatgpt-content-reference{index="88"}

**OSHWA** exige notamment que les fichiers de conception dans leur forme modifiable et le BOM soient accessibles ; sa définition insiste sur le « preferred format for making modifications », pas seulement des STL ou PDF. Son guide recommande notamment CERN-OHL-P/S/W-2.0, Solderpad ou TAPR pour le matériel. :chatgpt-content-reference{index="89"}

C’est particulièrement favorable à ta décision **build123d-as-code** : le code Python qui engendre la pièce est précisément une forme source modifiable, alors qu’un simple STL ne suffirait pas à l’esprit de l’OSHWA. Les fichiers neutres STEP/DXF/STL doivent cependant être publiés **en complément**, pour faciliter la réutilisation. :chatgpt-content-reference{index="90"}

**Open Know-How** fournit une structure de métadonnées pour rendre les projets matériels trouvables et interchangeables. Le projet historique OPEN-NEXT a évolué ; il faut utiliser les spécifications actuelles de l’Internet of Production Alliance plutôt que figer YXOR sur les anciens exemples `.okh.yml`. :chatgpt-content-reference{index="91"}

---

# 6. Comparaison de ta méthode avec l’état de l’art

## Ce qui est déjà très bon

| Ta pratique | Équivalent état de l’art | Verdict |
|---|---|---|
| Capacités → tâches chiffrées | Requirements Engineering / QFD / performance-based design | **À garder** |
| Tâches → exigences par articulation | Functional decomposition + physical sizing | **À garder** |
| Calculs analytiques + MuJoCo | Model-based engineering | **À garder** |
| Exploration `axes × actuateurs × taille` | Morphological analysis + Design Space Exploration | **À garder** |
| Filtres de faisabilité | Set-Based Design | **À garder** |
| Pareto coût/masse/capacité | Multi-objective optimization / NSGA-II | **À formaliser avec pymoo** |
| Choix humain final | Human-in-the-loop trade study | **Correct** |
| Banc d’essai | Verification | **À étendre** |
| YAML/Python/build123d/tests/Git | Model/documentation-as-code | **Excellent pour un solo + agents IA** |
| Un même écosystème actionneurs/bus/software | Platform architecture ; proche notamment de l’approche modulaire ODRI | **Très bonne hypothèse**, pas une contrainte absolue |

## Ce qui manque vraiment

### 1. Une vraie couche d’exigences traçables

Aujourd’hui, je transformerais par exemple :

```text
"doit pouvoir courir"
```

en :

```yaml
id: REQ-LOC-RUN-001
parent: CAP-LOC-003

statement: >
  YXOR-FINAL shall sustain a forward running gait
  on a level rigid surface.

metric:
  name: forward_speed
  unit: m/s
  threshold: TBD

conditions:
  payload_kg: 0
  duration_s: TBD
  battery_soc_min_pct: TBD
  ambient_temp_C: [TBD, TBD]

verification:
  method: test
  test_id: TEST-LOC-RUN-001

rationale:
  source: capability-matrix

status: draft
```

La donnée `TBD` est **bien meilleure qu’une valeur inventée**.

### 2. Une architecture fonctionnelle avant l’architecture physique

Avant :

> « quelle articulation reçoit quel RobStride ? »

il devrait exister :

> « quelles fonctions assure la jambe, quels flux mécanique/énergie/données/sûreté les relient, quelles interfaces doivent être invariantes ? »

C’est précisément là que VDI 2221, DSM et un MBSE léger t’apportent quelque chose. :chatgpt-content-reference{index="92"}

### 3. Des **Interface Control Specifications**

Pour chaque module :

- fixation et datum mécaniques ;
- enveloppe géométrique ;
- axe/repère/sens positif ;
- tension et courant ;
- connecteur/pinout ;
- protocole et adresse bus ;
- fréquence et latence ;
- timeouts ;
- limites de courant/température ;
- comportement à la perte de communication ;
- précision/calibration ;
- refroidissement ;
- contraintes de câblage ;
- stratégie de remplacement.

C’est un domaine où les humanoïdes artisanaux souffrent énormément ; Berkeley Humanoid Lite cite justement connecteurs et câbles parmi ses problèmes pratiques. :chatgpt-content-reference{index="93"}

### 4. La **robustesse** du Pareto

Ton Pareto semble surtout optimiser des valeurs nominales.

Il faut progressivement comparer :

\[
f(x,\theta)
\]

où `x` = conception et `θ` = incertitudes :

- masse réelle ;
- tolérance fabrication ;
- coefficient de friction ;
- backlash ;
- rendement ;
- tension batterie ;
- résistance moteur ;
- température ;
- paramètres de contact ;
- position réelle du CoM ;
- latence bus ;
- variation d’un exemplaire d’actionneur à l’autre.

Une solution légèrement moins optimale mais entourée d’un grand domaine faisable est souvent meilleure qu’une solution située exactement au bord d’une contrainte.

### 5. Le thermique et le duty-cycle

Un actionneur pouvant annoncer 40 Nm pendant un instant ne signifie pratiquement rien pour :

- se relever ;
- maintenir une charge ;
- pousser ;
- monter une pente ;
- effectuer 100 sauts ;
- marcher 30 minutes.

L’approche MIT Cheetah est particulièrement claire sur l’importance des pertes et de la thermique. :chatgpt-content-reference{index="94"}

Il te faut donc au minimum :

\[
(\tau,\omega,I,V,T,t)
\]

et non juste :

\[
\tau_\text{peak}
\]

### 6. L’identification système

Pour chaque modèle d’actionneur réellement acheté :

```text
datasheet
   ↓
modèle initial
   ↓
banc
   ↓
mesures
   ↓
fit paramètres
   ↓
intervalle d'incertitude
   ↓
MuJoCo
   ↓
validation croisée
```

ToddlerBot est ici une excellente référence concrète. :chatgpt-content-reference{index="95"}

### 7. L’AMDEC et les scénarios de panne

Commence au moins par :

- perte d’encodeur ;
- encodeur erroné ;
- actionneur bloqué ;
- commande maximale intempestive ;
- perte CAN/RS485/EtherCAT ;
- brownout ;
- surtension de régénération ;
- batterie déconnectée ;
- température excessive ;
- connecteur arraché ;
- vis desserrée ;
- rupture pièce imprimée ;
- défaillance roulement/réducteur ;
- chute sur genou/hanche/main ;
- logiciel principal figé ;
- perte du réseau ;
- commande IA aberrante.

IEC 60812 fournit précisément le cadre général pour cette démarche. :chatgpt-content-reference{index="96"}

### 8. Une vraie hiérarchie d’essais

Je passerais par :

```text
simulation
    ↓
actionneur seul
    ↓
actionneur + charge
    ↓
articulation complète
    ↓
jambe unique
    ↓
deux jambes / bassin sur support
    ↓
robot sous portique/tether
    ↓
marche autonome contrôlée
    ↓
terrain / chute / récupération
    ↓
interaction humaine
```

Cela transforme le banc d’essai d’une validation finale en **élément permanent du cycle en V**.

---

## Ce que tu réinventes aujourd’hui

Il y a plusieurs choses que tu peux arrêter d’inventer toi-même.

**Tes « niveaux de locomotion »** : garde ta progression pédagogique, mais aligne ses métriques avec **ISO 18646-5:2026** là où la norme couvre le problème. Elle contient déjà une structure pour vitesse nominale, distance d’arrêt, franchissement et conditions d’essai. :chatgpt-content-reference{index="97"}

**Ton processus global** : ne crée pas « YXOR Engineering Method v1 » à partir de zéro. Déclare plutôt :

> YXOR Engineering Process = ISO 15288-tailored + VDI 2206-tailored + Set-Based Design + V&V-as-code.

**Tes modes de panne** : base-les sur une AMDEC IEC 60812 plutôt que sur une simple checklist personnelle. :chatgpt-content-reference{index="98"}

**Tes niveaux de maturité** : utilise TRL plutôt qu’un système maison. :chatgpt-content-reference{index="99"}

**Ton moteur Pareto** : utilise pymoo/NSGA-II avant d’écrire toi-même algorithmes de tri, crowding distance, contraintes, termination, etc. :chatgpt-content-reference{index="100"}

**Ton format open hardware** : aligne les releases sur DIN SPEC 3105 + OSHWA + Open Know-How plutôt que d’inventer tes métadonnées de publication. :chatgpt-content-reference{index="101"}

En revanche, **ne remplace pas ton modèle YAML/Python par Capella juste parce que Capella est “MBSE”**. Ce serait le cas inverse : remplacer quelque chose de très adapté par davantage de processus.

---

# 7. Le cadre minimal que je recommande pour YXOR

Je l’appellerais simplement :

## **YXOR-SE: 15288-lite + VDI-2206-lite + Set-Based Co-Design**

Il aurait huit couches.

### Étape 1 — Exigences, capacités et situations opérationnelles

Conserve tes niveaux de capacité, mais donne un identifiant stable à tout :

```text
CAP-   capacité
REQ-   exigence
FUN-   fonction
IF-    interface
ARCH-  choix architectural
HAZ-   danger
FMEA-  mode de défaillance
DEC-   décision
MODEL- modèle/calcul
TEST-  vérification
RESULT résultat
```

Un assistant IA peut alors répondre réellement à :

> « Si je remplace le RS03 par le moteur X, quelles exigences, pièces, simulations et tests deviennent invalides ? »

C’est, à mon avis, **beaucoup plus précieux pour toi que de dessiner immédiatement des dizaines de diagrammes SysML**.

### Étape 2 — Créer la matrice de traçabilité

Automatise :

```text
CAP → REQ → FUN → ARCH/IF → MODEL → TEST → RESULT
```

Le CI doit refuser :

- exigence sans méthode de vérification ;
- test sans exigence ;
- interface sans propriétaire ;
- valeur physique sans unité ;
- paramètre simulé sans origine ;
- décision sans justification ;
- résultat provenant d’une version physique inconnue.

C’est le « V-model as code ».

### Étape 3 — Construire la DSM

Une seule matrice `modules × modules` :

```text
mécanique
électricité
puissance
bus
temps réel
thermique
logiciel
sécurité
```

Tu vas immédiatement découvrir quelles décisions sont vraiment modulaires et lesquelles créent des cascades de modifications.

### Étape 4 — Transformer ton exploration actuelle en **Set-Based Design robuste**

Ne stocke pas seulement :

```text
candidate = rejected / selected
```

mais :

```text
candidate
├─ feasible
├─ infeasible
│  └─ violated_constraints[]
├─ unknown
│  └─ measurements_needed[]
└─ dominated
   └─ pareto_reason
```

Le statut **unknown** est extrêmement important : il évite que l’assistant IA transforme une absence de donnée en estimation silencieuse.

### Étape 5 — Construire le banc actionneur AVANT de figer les jambes

Mesure réellement pour chaque actionneur candidat :

- `Kt` / relation courant-couple réelle ;
- couple statique et dynamique ;
- vitesse à différents couples ;
- courant ;
- tension ;
- rendement ;
- température bobinage/carter indirectement si nécessaire ;
- temps avant limite thermique ;
- backlash ;
- compliance ;
- friction/hystérésis ;
- comportement du contrôleur intégré ;
- latence/jitter du bus ;
- freinage/régénération ;
- répétabilité entre unités.

Berkeley souligne explicitement l’importance d’améliorer l’identification couple-courant près des zones de saturation ; ToddlerBot démontre la valeur du system identification pour le sim-to-real. :chatgpt-content-reference{index="102"}

### Étape 6 — Introduire le co-design progressivement

Je ne lancerais **pas** immédiatement un RL imbriqué dans NSGA-II sur 300 variables.

Commence par trois niveaux :

```text
V0 — mécanique seule
V1 — mécanique + contrôleur simplifié
V2 — mécanique + locomotion optimisée/simulation
```

Puis seulement :

```text
V3 — morphology/control co-design + surrogate/RL
```

C’est beaucoup plus défendable scientifiquement.

### Étape 7 — Faire du robot 0,6 m un banc de vérité, pas une maquette réduite

Sa mission devrait être :

> **valider architecture logicielle, bus, actionneurs, calibration, perception, commande, sécurité, processus de fabrication, réparabilité et sim-to-real.**

Pas :

> **prouver automatiquement que les dimensions du robot 1,2 m fonctionneront.**

La distinction est capitale.

### Étape 8 — Passer au SysML v2 uniquement lorsque tu ressens une vraie douleur

Par exemple lorsque :

- les relations entre exigences deviennent difficiles à interroger ;
- les interfaces se multiplient ;
- un changement demande trop de recherche manuelle ;
- les assistants IA commencent à produire des incohérences entre domaines ;
- YAML commence à reproduire maladroitement un langage de modélisation système.

À ce moment-là, **SysML v2 textuel** est beaucoup plus intéressant pour ton profil qu’un basculement immédiat vers une modélisation graphique lourde. La norme 2.0 offre officiellement une notation textuelle et des représentations machine-readable. :chatgpt-content-reference{index="103"}

---

## Mes 7 premières actions concrètes

1. **Créer immédiatement** `requirements.yaml`, `interfaces.yaml`, `hazards.yaml`, `tests.yaml` et `decisions/`, avec schémas JSON/Pydantic et contrôle CI.
2. **Mapper tes niveaux de locomotion sur ISO 18646-5:2026**, sans attendre que le robot existe ; conserver tes propres essais seulement là où la norme ne couvre pas la capacité. :chatgpt-content-reference{index="104"}
3. **Ajouter une DSM** du robot et figer les interfaces communes entre YXOR-Learning et YXOR-Final avant de figer les actionneurs eux-mêmes.
4. **Construire le banc de caractérisation des actionneurs** et faire de ses résultats la source des paramètres MuJoCo.
5. **Brancher pymoo** sur ton pipeline actuel pour les fronts Pareto/NSGA-II et ajouter explicitement les incertitudes ; n’adopter OpenMDAO que lorsque de vrais couplages multidisciplinaires le justifieront. :chatgpt-content-reference{index="105"}
6. **Faire une première AMDEC** avant tout essai dynamique autonome et concevoir l’arrêt d’urgence/chaîne de sûreté maintenant, pas après la locomotion. :chatgpt-content-reference{index="106"}
7. **Définir un “hardware release contract”** : chaque robot physique reçoit un ID/version qui pointe exactement vers commit Git, BOM, CAO, firmware, paramètres de calibration, MJCF et résultats d’essais. C’est cohérent avec les bonnes pratiques OSHWA, qui recommandent explicitement un numéro de version/date permettant de relier objet physique et fichiers de conception. :chatgpt-content-reference{index="107"}

### Ma conclusion principale

Ta méthode n’a pas besoin d’être remplacée.

Elle a besoin de passer de :

> **« très bonne méthode d’optimisation de conception »**

à :

> **« système d’ingénierie traçable, expérimentalement fermé en boucle et sûr »**.

Tu as déjà construit une bonne moitié du problème difficile — paramétrisation, simulation, exploration et automatisation. Le prochain saut de qualité vient de **requirements/V&V, interfaces, incertitude, system identification, thermique, sécurité et configuration du hardware réel**, pas d’un nouvel optimiseur sophistiqué.

---

# 8. Registre des principales sources

**Fiabilité** :  
**Très élevée** = organisme normatif / spécification officielle ; **Élevée** = publication scientifique évaluée par les pairs ou documentation universitaire primaire ; **Moyenne+** = préprint universitaire ou documentation officielle de projet ; **Moyenne** = documentation industrielle/vendor ; **Faible à moyenne** = marketing/blog, utilisé seulement comme tel.

| Source | Type | Date | Fiabilité | Lien |
|---|---|---:|---|---|
| ISO/IEC/IEEE 15288, *System life cycle processes* | Norme | 2023 | Très élevée | :chatgpt-content-reference{index="108"} |
| INCOSE Systems Engineering Handbook, 5e éd. | Guide professionnel | 2023 | Élevée | :chatgpt-content-reference{index="109"} |
| VDI/VDE 2206, *Development of mechatronic and cyber-physical systems* | Directive technique | 2021 | Très élevée |  |
| VDI 2221 Part 1 | Directive technique | 2019 | Très élevée | :chatgpt-content-reference{index="111"} |
| Pahl & Beitz et al., *Engineering Design: A Systematic Approach* | Ouvrage académique | 2007, 3e éd. | Élevée | :chatgpt-content-reference{index="112"} |
| OMG SysML v2.0 | Spécification | Sept. 2025 | Très élevée |  |
| Eclipse Capella 7.1.0 | Documentation outil | Juil. 2026 | Élevée pour état outil |  |
| ASQ, Quality Function Deployment | Référence professionnelle | actuelle | Élevée | :chatgpt-content-reference{index="115"} |
| Suh, Axiomatic Design | Méthode académique | travaux historiques | Élevée | :chatgpt-content-reference{index="116"} |
| Eppinger & Browning, *Design Structure Matrix Methods and Applications* | Ouvrage MIT | 2012 | Élevée | :chatgpt-content-reference{index="117"} |
| Sobek, Ward & Liker, *Toyota’s Principles of Set-Based Concurrent Engineering* | Article | 1999 | Élevée | :chatgpt-content-reference{index="118"} |
| Deb et al., *A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II* | Article IEEE | 2002 | Très élevée | :chatgpt-content-reference{index="119"} |
| Gray et al., *OpenMDAO: An Open-Source Framework…* | Article scientifique | 2019 | Élevée | :chatgpt-content-reference{index="120"} |
| IEC 60812, FMEA/FMECA | Norme IEC | 2018 | Très élevée | :chatgpt-content-reference{index="121"} |
| NASA Technology Readiness Levels | Référence institutionnelle | mise à jour 2023 | Très élevée | :chatgpt-content-reference{index="122"} |
| Seok et al., *Design Principles for Energy-Efficient Legged Locomotion… MIT Cheetah* | Article IEEE/ASME | 2015 | Élevée | :chatgpt-content-reference{index="123"} |
| Wensing et al., *Proprioceptive Actuator Design in the MIT Cheetah* | Article IEEE TRO | 2017 | Élevée | :chatgpt-content-reference{index="124"} |
| Kim & Wensing, *Design of Dynamic Legged Robots* | Monographie/revue scientifique | 2017 | Élevée | :chatgpt-content-reference{index="125"} |
| Bledt et al., *MIT Cheetah 3: Design and Control…* | Article IROS | 2018/19 | Élevée | :chatgpt-content-reference{index="126"} |
| Hwangbo et al., *Learning agile and dynamic motor skills for legged robots* | Science Robotics | 2019 | Élevée | :chatgpt-content-reference{index="127"} |
| Kumar et al., *RMA: Rapid Motor Adaptation for Legged Robots* | RSS | 2021 | Élevée | :chatgpt-content-reference{index="128"} |
| Miki et al., *Learning robust perceptive locomotion…* | Science Robotics | 2022 | Élevée | :chatgpt-content-reference{index="129"} |
| Koike, Ariizumi & Matsuno, simultaneous morphology/controller optimization | Article scientifique | 2023/24 | Élevée | :chatgpt-content-reference{index="130"} |
| Du et al., *Efficient co-adaptation of humanoid robot design and locomotion control…* | Article scientifique | 2025 | Élevée ; validation physique limitée | :chatgpt-content-reference{index="131"} |
| Oke et al., *Allometric Scaling Laws for Bipedal Robots* | **Préprint** | 2026 | Moyenne+ ; non peer-reviewed à cette date | :chatgpt-content-reference{index="132"} |
| Liao et al., Berkeley Humanoid | Préprint / projet universitaire | 2024 | Moyenne+ | :chatgpt-content-reference{index="133"} |
| Chi et al., Berkeley Humanoid Lite | RSS | 2025 | Élevée | :chatgpt-content-reference{index="134"} |
| Berkeley Humanoid Lite v1.1.0 – retour fragilité/connectique | Release projet | 2026 | Moyenne+ | :chatgpt-content-reference{index="135"} |
| Shi et al., ToddlerBot | CoRL/PMLR | 2025 | Élevée | :chatgpt-content-reference{index="136"} |
| Grimminger et al., ODRI | IEEE RA-L | 2020 | Élevée | :chatgpt-content-reference{index="137"} |
| ISO 18646-5, *Locomotion for legged robots* | Norme ISO | Juil. 2026 | Très élevée |  |
| ISO 13482, personal care/service robots | Norme ISO | 2014 ; révision en cours | Très élevée | :chatgpt-content-reference{index="139"} |
| ISO 12100 | Norme ISO | 2010 | Très élevée | :chatgpt-content-reference{index="140"} |
| ISO 10218-1 | Norme ISO | 2025 | Très élevée | :chatgpt-content-reference{index="141"} |
| ISO 13849-1 | Norme ISO | 2023 | Très élevée | :chatgpt-content-reference{index="142"} |
| ISO 13850 | Norme ISO | 2015 | Très élevée | :chatgpt-content-reference{index="143"} |
| IEC 60204-1 | Norme IEC | 2016+A1:2021 | Très élevée | :chatgpt-content-reference{index="144"} |
| IEC 61508 | Norme IEC | 2010 | Très élevée | :chatgpt-content-reference{index="145"} |
| DIN SPEC 3105-1, Open Source Hardware documentation | Spécification DIN | 2020 | Très élevée |  |
| OSHWA Open Source Hardware Definition | Standard communautaire | actuel | Élevée |  |
| OSHWA Certification – Hardware | Documentation officielle | actuelle | Élevée |  |

### Sources auxquelles je n’ai pas eu accès intégralement

Pour les **ISO, IEC et VDI payantes**, j’ai pu vérifier les pages officielles, statut, portée, date, abstracts/aperçus et, lorsque publié, sommaires accessibles, mais **pas le corps intégral de toutes les normes payantes**. Je n’attribue donc pas à ces normes des exigences de détail que je n’ai pas pu vérifier dans le texte intégral.

Pour l’article Hwangbo/Science Robotics, le résumé et les métadonnées étaient accessibles mais l’accès intégral via la source consultée était restreint ; je n’en ai utilisé que les résultats publiquement vérifiables. :chatgpt-content-reference{index="149"}

Pour les processus internes de **Unitree, Booster, Apptronik/Apollo, Agility/Digit et MIT Humanoid**, je n’ai pas trouvé de « design history file » public équivalent aux retours particulièrement détaillés de Berkeley/ToddlerBot. J’ai donc volontairement écrit **« non trouvé »** plutôt que de reconstruire leur méthode à partir de leurs communications commerciales.