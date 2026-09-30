# Comparatif du banc d'essai — v2

**Engendré** par `.venv/bin/python scripts/selection_multicritere.py --ecrire`, le 2026-09-30, après le comparatif des familles (`docs/choix-famille-actionneurs.md`). Aucun achat n'est proposé : ce comparatif prépare le choix de Jeremy (cadrage § 6 et § 13, question 12).

---

## 1 — Les options

| Option | Inconnues décisives tranchées | Ce qu'elle apprend | Transfert à S | Coût TTC CH | Postes non chiffrés | Risque |
| --- | --- | --- | --- | ---: | --- | --- |
| 1 × Damiao DM-J4310-2EC V1.2 | 1/3 : k_damiao | 2/5 : protocole, thermique | 5 — exactement le modèle retenu pour S → 5 | 261 CHF | — | 3 — pas de rechange : une casse arrête le banc |
| 2 × Damiao DM-J4310-2EC V1.2 | 1/3 : k_damiao | 4/5 : protocole, thermique, bus_multi_adresses, segment_2ddl | 5 — exactement le modèle retenu pour S → 5 | 418 CHF | — | 5 — rechange disponible, un seul modèle à maîtriser |
| 3 × Damiao DM-J4310-2EC V1.2 | 1/3 : k_damiao | 5/5 : protocole, thermique, bus_multi_adresses, segment_2ddl, dispersion | 5 — exactement le modèle retenu pour S → 5 | 574 CHF | — | 5 — rechange disponible, un seul modèle |
| 1 × Damiao DM-J4310-2EC V1.2 (48 V) + 1 × RobStride EduLite 05 (48 V) | 2/3 : k_damiao, blocage_edulite | 4/5 : protocole, thermique, bus_multi_adresses, segment_2ddl | 5 — JUGEMENT : quel que soit k, le modèle S de la famille gagnante est sur le banc → 5 | 385 CHF | — | 3 — deux modèles, deux protocoles possibles à maîtriser, pas de rechange de chacun |
| qualification : 1 × Damiao DM-J4310-2EC V1.2 (48 V) + 1 × RobStride EduLite 05 + 1 × RobStride RS05 (48 V) | 3/3 : k_damiao, blocage_edulite, rs05_contre_edulite | 4/5 : protocole, thermique, bus_multi_adresses, segment_2ddl | 5 — JUGEMENT : les modèles S des deux familles en tête sont sur le banc, quel que soit k → 5 | 499 CHF | — | 3 — trois modèles, deux protocoles (RobStride commun au RS05 et à l'EduLite 05), pas de rechange de chacun |
| 2 × Feetech STS3250 (banc d'apprentissage) | 0/3 : aucune | 4/5 : protocole, thermique, bus_multi_adresses, segment_2ddl | 1 — autre fabricant, autre bus (TTL) que tous les finalistes → 1 | ≥ 10 CHF | prix Feetech STS3250, prix Feetech STS3250, alimentation 12 V | 1 — impasse : bus TTL et servo à engrenages, rien ne se transfère à une classe S en CAN |

Coût TTC CH = (actionneurs + adaptateur + alimentation) × (1 + imprévus 15 %, provisoire) × (1 + TVA 8,1 %). Alimentations : Mean Well RSP-320-24 (24 V) ou RSP-500-48 (48 V), Reichelt. Un poste non chiffré met la note de coût à 0.

**Adaptateur USB-CAN** : candleLight de Linux Automation (54,74 € TTC, vérifié), **prototype non conforme CE** selon son fabricant. **Alternative : CANable 2.0** (Openlight Labs), 35 USD **non vérifié** (page inaccessible), conformité CE **inconnue** ; livré avec le firmware slcan (**GPL-3.0**), compatible candleLight_fw (**MIT**) mais **sans CAN FD** sur la 2.0 ; licence du matériel non nommée.

**L'option à deux finalistes** tourne à **48 V**, pour une seule alimentation : Damiao DM-J4310-2EC V1.2 (48 V) ; RobStride EduLite 05. 

**Les trois inconnues décisives** (grille écrite avant le calcul, `criteres_selection.yaml`) :

- `k_damiao` — le couple continu réel du Damiao J4310 (son k) : décide la bascule Damiao / RobStride
- `blocage_edulite` — le couple de l'EduLite 05 près du blocage : aucune valeur en blocage n'est publiée
- `rs05_contre_edulite` — RS05 ou EduLite 05 pour S dans la famille RobStride, mesurés dans la même condition

---

## 2 — Notes et score

| Critère | Poids (proposé) | 1 × Damiao DM-J4310-2EC V1.2 | 2 × Damiao DM-J4310-2EC V1.2 | 3 × Damiao DM-J4310-2EC V1.2 | 1 × Damiao DM-J4310-2EC V1.2 (48 V) + 1 × RobStride EduLite 05 (48 V) | qualification : 1 × Damiao DM-J4310-2EC V1.2 (48 V) + 1 × RobStride EduLite 05 + 1 × RobStride RS05 (48 V) | 2 × Feetech STS3250 (banc d'apprentissage) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| valeur_decision | 30 | 2 | 2 | 2 | 3 | 5 | 0 |
| apprentissage | 24.5 | 2 | 4 | 5 | 4 | 4 | 4 |
| transfert_S | 17.5 | 5 | 5 | 5 | 5 | 5 | 1 |
| cout | 17.5 | 4 | 3 | 3 | 4 | 3 | 0 |
| risque | 10.5 | 3 | 5 | 5 | 3 | 3 | 1 |
| **score /5** | | **2,98** | **3,50** | **3,75** | **3,77** | **4,20** | **1,26** |

## 3 — Sensibilité

Vainqueur aux poids proposés : **qualification : 1 × Damiao DM-J4310-2EC V1.2 (48 V) + 1 × RobStride EduLite 05 + 1 × RobStride RS05 (48 V)**. 9 variations ±50 % sur 10 le laissent en tête.

| Option | Victoires sur 1 000 tirages |
| --- | ---: |
| 3 × Damiao DM-J4310-2EC V1.2 | 501 |
| qualification : 1 × Damiao DM-J4310-2EC V1.2 (48 V) + 1 × RobStride EduLite 05 + 1 × RobStride RS05 (48 V) | 384 |
| 1 × Damiao DM-J4310-2EC V1.2 (48 V) + 1 × RobStride EduLite 05 (48 V) | 115 |

## 4 — Verdict

**Options trop proches pour que l’analyse tranche** : qualification : 1 × Damiao DM-J4310-2EC V1.2 (48 V) + 1 × RobStride EduLite 05 + 1 × RobStride RS05 (48 V) — le choix dépend des poids, que Jeremy fixera.

**Ce que chaque option tranche.** L'hypothèse k ne touche que les actionneurs dont la condition de mesure n'est pas publiée : ici **Damiao DM-J4310-2EC V1.2, RobStride EduLite 05**. Mesurer son couple continu réel **suffit à trancher le seuil**, et les options « × vainqueur » le font. L'option à deux finalistes ajoute la vérification de l'autre finaliste **dans la même condition** : la comparaison devient directe, au lieu de s'appuyer sur sa fiche.

---

## 5 — Protocole de mesure : les couples continus en condition IDENTIQUE

But : remplacer l'hypothèse k par une mesure, sur les deux finalistes, **dans la même condition**. Les fiches ne sont pas comparables entre elles : plaques différentes, ou condition non précisée. Ce protocole est **proposé**, pas décidé.

1. **Même montage.** Chaque actionneur est fixé sur la **même plaque d'aluminium de 70 × 70 mm** (la plus petite condition publiée, celle du RS05 et de l'EduLite 05). L'épaisseur et la matière sont notées. La plaque est posée sur le même support isolant.
2. **Même alimentation**, à la même tension (celle de l'option), et le même bus CAN au même débit.
3. **Rotor bloqué**, par un bras de levier sur un dynamomètre ou une balance, longueur notée. Le couple **réel** est lu sur le dynamomètre, et le couple **déclaré** par la télémétrie : leur écart est lui-même une mesure. *Le blocage est la condition la plus proche d'un robot qui tient debout ; une mesure en rotation demanderait un frein, et n'est pas prévue ici.*
4. **Mêmes paliers de couple**, par ordre croissant, sur les deux actionneurs : le continu publié le plus bas des deux, puis des paliers de 10 % au-dessus, jusqu'au seuil k × nominal à départager.
5. **Même durée** : chaque palier est tenu jusqu'à l'équilibre thermique (variation < 1 °C sur 5 min), ou au plus 30 min, ou jusqu'à 10 °C sous la protection thermique du constructeur.
6. **Relevés** à 1 Hz : température bobinage et driver (télémétrie), température du boîtier (thermocouple), courant, couple réel. La **température ambiante** est notée au début et à la fin de chaque palier.
7. **Résultat** : le plus haut couple tenu à l'équilibre sous la limite thermique est le **continu mesuré**, dans cette condition. Divisé par le nominal publié, il donne le **k mesuré** de chaque actionneur, à reporter dans le catalogue comme une mesure (fiche 0041) :
   il départage les finalistes au seuil du § 1.

---

## 6 — Ce que ce comparatif ne dit pas

- Les poids, les notes de transfert et de risque sont **proposés** ou de **jugement**, et justifiés ligne par ligne.
- L'option Feetech n'a **ni prix vérifié ni alimentation 12 V chiffrée** : son coût est inconnu.
- La mesure au rotor bloqué ne dit rien du rendement en rotation ; elle compare les deux finalistes entre eux, dans la même condition.
- Le banc à trois exemplaires répond à la demande de l'étude externe (« au moins 3 », § 15.2) pour la dispersion entre exemplaires.
