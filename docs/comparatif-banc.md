# Comparatif du banc d'essai — v2

**Engendré** par `.venv/bin/python scripts/selection_multicritere.py --ecrire`, le 2026-09-30, après le comparatif des familles (`docs/choix-famille-actionneurs.md`). Aucun achat n'est proposé : ce comparatif prépare le choix de Jeremy (cadrage § 6 et § 13, question 12).

**Pourquoi ce banc compte.** Le choix de famille bascule au seuil **k ≈ 0,70** : au-dessus, **Damiao (J4310 V1.2 → J8006 V1.1 → J4340 V1.1)** ; en dessous, **RobStride, variante S = EduLite 05 (EL05 → RS02 → RS06)**. k est le rapport entre le couple continu réel des actionneurs « condition non précisée » et leur nominal publié. **Il ne se décide pas, il se mesure** — c'est le rôle premier du banc.

---

## 1 — Les options

| Option | Ce qu'elle apprend | Transfert à S | Coût TTC CH | Postes non chiffrés | Risque |
| --- | --- | --- | ---: | --- | --- |
| 1 × Damiao DM-J4310-2EC V1.2 | 2/5 : protocole, thermique | 3 — JUGEMENT : 5 si k ≥ 0,70 (sa famille gagne), 1 sinon ; k inconnu tant que le banc ne l'a pas mesuré → 3 | 261 CHF | — | 3 — pas de rechange : une casse arrête le banc |
| 2 × Damiao DM-J4310-2EC V1.2 | 4/5 : protocole, thermique, bus_multi_adresses, segment_2ddl | 3 — JUGEMENT : 5 si k ≥ 0,70 (sa famille gagne), 1 sinon ; k inconnu tant que le banc ne l'a pas mesuré → 3 | 418 CHF | — | 5 — rechange disponible, un seul modèle à maîtriser |
| 3 × Damiao DM-J4310-2EC V1.2 | 5/5 : protocole, thermique, bus_multi_adresses, segment_2ddl, dispersion | 3 — JUGEMENT : 5 si k ≥ 0,70 (sa famille gagne), 1 sinon ; k inconnu tant que le banc ne l'a pas mesuré → 3 | 574 CHF | — | 5 — rechange disponible, un seul modèle |
| 1 × Damiao DM-J4310-2EC V1.2 (48 V) + 1 × RobStride EduLite 05 (48 V) | 4/5 : protocole, thermique, bus_multi_adresses, segment_2ddl | 5 — JUGEMENT : quel que soit k, le modèle S de la famille gagnante est sur le banc → 5 | ≥ 219 CHF | prix Damiao DM-J4310-2EC V1.2 (48 V) | 3 — deux modèles, deux protocoles possibles à maîtriser, pas de rechange de chacun |
| 2 × Feetech STS3250 (banc d'apprentissage) | 4/5 : protocole, thermique, bus_multi_adresses, segment_2ddl | 1 — autre fabricant, autre bus (TTL) que tous les finalistes → 1 | ≥ 10 CHF | prix Feetech STS3250, prix Feetech STS3250, alimentation 12 V | 1 — impasse : bus TTL et servo à engrenages, rien ne se transfère à une classe S en CAN |

Coût TTC CH = (actionneurs + adaptateur + alimentation) × (1 + imprévus 15 %, provisoire) × (1 + TVA 8,1 %). Alimentations : Mean Well RSP-320-24 (24 V) ou RSP-500-48 (48 V), Reichelt. Un poste non chiffré met la note de coût à 0.

**Adaptateur USB-CAN** : candleLight de Linux Automation (54,74 € TTC, vérifié), **prototype non conforme CE** selon son fabricant. **Alternative : CANable 2.0** (Openlight Labs), 35 USD **non vérifié** (page inaccessible), conformité CE **inconnue** ; livré avec le firmware slcan (**GPL-3.0**), compatible candleLight_fw (**MIT**) mais **sans CAN FD** sur la 2.0 ; licence du matériel non nommée.

**L'option à deux finalistes** tourne à **48 V**, pour une seule alimentation : Damiao DM-J4310-2EC V1.2 (48 V) ; RobStride EduLite 05. Le prix de la variante 48 V du Damiao n'est pas connu : son coût est donc incomplet.

---

## 2 — Notes et score

| Critère | Poids (proposé) | 1 × Damiao DM-J4310-2EC V1.2 | 2 × Damiao DM-J4310-2EC V1.2 | 3 × Damiao DM-J4310-2EC V1.2 | 1 × Damiao DM-J4310-2EC V1.2 (48 V) + 1 × RobStride EduLite 05 (48 V) | 2 × Feetech STS3250 (banc d'apprentissage) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| apprentissage | 35 | 2 | 4 | 5 | 4 | 4 |
| transfert_S | 25 | 3 | 3 | 3 | 5 | 1 |
| cout | 25 | 4 | 3 | 3 | 0 | 0 |
| risque | 15 | 3 | 5 | 5 | 3 | 1 |
| **score /5** | | **2,90** | **3,65** | **4,00** | **3,10** | **1,80** |

## 3 — Sensibilité

Vainqueur aux poids proposés : **3 × Damiao DM-J4310-2EC V1.2**. 8 variations ±50 % sur 8 le laissent en tête.

| Option | Victoires sur 1 000 tirages |
| --- | ---: |
| 3 × Damiao DM-J4310-2EC V1.2 | 780 |
| 1 × Damiao DM-J4310-2EC V1.2 (48 V) + 1 × RobStride EduLite 05 (48 V) | 134 |
| 1 × Damiao DM-J4310-2EC V1.2 | 86 |

## 4 — Verdict

**Classement ROBUSTE** : 3 × Damiao DM-J4310-2EC V1.2.

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
