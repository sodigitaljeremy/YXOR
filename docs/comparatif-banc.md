# Comparatif du banc d'essai — v3

**Engendré** par `.venv/bin/python scripts/selection_multicritere.py --ecrire`, le 2026-10-01, après le comparatif des familles (`docs/choix-famille-actionneurs.md`). Aucun achat n'est proposé : ce comparatif prépare le choix de Jeremy (cadrage § 6 et § 13, question 12).

> **Banc de VÉRIFICATION, pas de départage.** Aucune des inconnues n'est décisive (règle étendue du 2026-09-30, `criteres_selection.yaml`) : dans la plage plausible de k, aucune mesure du banc ne peut changer la décision de famille. Le banc **vérifie** une décision que les données publiées portent déjà ; il ne la prend pas. La valeur de décision (poids 40) vaut donc **0 pour toutes les options** : elle ne départage plus rien, et le classement se fait sur les autres critères.

---

## 1 — Les options

| Option | Inconnues décisives tranchées | Ce qu'elle apprend | Transfert à S | Coût TTC CH | Coût TTC FR | Postes non chiffrés | Risque |
| --- | --- | --- | --- | ---: | ---: | --- | --- |
| 1 × RobStride RS00 | — (aucune n'est décisive) | 2/5 : protocole, thermique | 5 — exactement le modèle retenu pour S → 5 | 265 CHF | 295 CHF | — | 3 — pas de rechange : une casse arrête le banc |
| 2 × RobStride RS00 | — (aucune n'est décisive) | 5/5 : protocole, thermique, bus_multi_adresses, segment_2ddl, dispersion | 5 — exactement le modèle retenu pour S → 5 | 395 CHF | 439 CHF | — | 5 — rechange disponible, un seul modèle à maîtriser |
| 3 × RobStride RS00 | — (aucune n'est décisive) | 5/5 : protocole, thermique, bus_multi_adresses, segment_2ddl, dispersion | 5 — exactement le modèle retenu pour S → 5 | 525 CHF | 583 CHF | — | 5 — rechange disponible, un seul modèle |
| 1 × RobStride RS00 + 1 × RobStride EduLite 05 (48 V) | — (aucune n'est décisive) | 4/5 : protocole, thermique, bus_multi_adresses, segment_2ddl | 5 — JUGEMENT : quel que soit k, le modèle S de la famille gagnante est sur le banc → 5 | 348 CHF | 387 CHF | — | 3 — deux modèles, deux protocoles possibles à maîtriser, pas de rechange de chacun |
| qualification : 1 × Damiao DM-J4310-2EC V1.2 (48 V) + 1 × RobStride EduLite 05 + 1 × RobStride RS05 (48 V) | — (aucune n'est décisive) | 4/5 : protocole, thermique, bus_multi_adresses, segment_2ddl | 5 — JUGEMENT : les modèles S des deux familles en tête sont sur le banc, quel que soit k → 5 | 499 CHF | 554 CHF | — | 3 — trois modèles, deux protocoles (RobStride commun au RS05 et à l'EduLite 05), pas de rechange de chacun |
| 2 × Feetech STS3250 (banc d'apprentissage) | — (aucune n'est décisive) | 5/5 : protocole, thermique, bus_multi_adresses, segment_2ddl, dispersion | 1 — autre fabricant, autre bus (TTL) que tous les finalistes → 1 | ≥ 10 CHF | ≥ 12 CHF | prix Feetech STS3250, prix Feetech STS3250, alimentation 12 V | 1 — impasse : bus TTL et servo à engrenages, rien ne se transfère à une classe S en CAN |

Coût TTC = (actionneurs + adaptateur + alimentation) × (1 + imprévus 15 %, provisoire) × (1 + TVA du pays de livraison : CH 8,1 %, FR 20,0 %). **Livraison possible en CH et en FR** (`budget.yaml`, `livraison`) ; la note de coût se prend sur CH. Tout est en CHF (taux BCE). Port, droits de douane et frais de dédouanement sont **inconnus**, non comptés. Alimentations : Mean Well RSP-320-24 (24 V) ou RSP-500-48 (48 V), Reichelt. Un poste non chiffré met la note de coût à 0.

**Adaptateur USB-CAN** : candleLight de Linux Automation (54,74 € TTC, vérifié), **prototype non conforme CE** selon son fabricant. **Alternative : CANable 2.0** (Openlight Labs), 35 USD **non vérifié** (page inaccessible), conformité CE **inconnue** ; livré avec le firmware slcan (**GPL-3.0**), compatible candleLight_fw (**MIT**) mais **sans CAN FD** sur la 2.0 ; licence du matériel non nommée.

**L'option à deux finalistes** tourne à **48 V**, pour une seule alimentation : RobStride RS00 ; RobStride EduLite 05. 

**Les inconnues décisives** (règles écrites avant le calcul, `criteres_selection.yaml`) :

- `k_damiao` — le couple continu réel du Damiao J4310 (son k) : DÉCISIF SEULEMENT SI k < bascule — **NON décisive** (aucune bascule dans le balayage)
- `blocage_edulite` — le couple de l'EduLite 05 près du blocage : aucune valeur en blocage n'est publiée — **NON décisive** (dans la plage plausible (k de 1,0 à 0,7, ≥ 0,619), la famille gagnante est toujours robstride_rs00 ; aucune de ces familles (robstride, robstride_el05) n'y gagne)
- `rs05_contre_edulite` — RS05 ou EduLite 05 pour S dans la famille RobStride, mesurés dans la même condition — **NON décisive** (dans la plage plausible (k de 1,0 à 0,7, ≥ 0,619), la famille gagnante est toujours robstride_rs00 ; aucune de ces familles (robstride, robstride_el05) n'y gagne)

La valeur de décision se note en **proportion** des inconnues décisives que l'option tranche.

---

## 2 — Notes et score

| Critère | Poids (proposé) | 1 × RobStride RS00 | 2 × RobStride RS00 | 3 × RobStride RS00 | 1 × RobStride RS00 + 1 × RobStride EduLite 05 (48 V) | qualification : 1 × Damiao DM-J4310-2EC V1.2 (48 V) + 1 × RobStride EduLite 05 + 1 × RobStride RS05 (48 V) | 2 × Feetech STS3250 (banc d'apprentissage) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| valeur_decision | 40 | 0 | 0 | 0 | 0 | 0 | 0 |
| apprentissage | 10 | 2 | 5 | 5 | 4 | 4 | 5 |
| transfert_S | 20 | 5 | 5 | 5 | 5 | 5 | 1 |
| cout | 15 | 4 | 4 | 3 | 4 | 3 | 0 |
| risque | 15 | 3 | 5 | 5 | 3 | 3 | 1 |
| **score /5** | | **2,25** | **2,85** | **2,70** | **2,45** | **2,30** | **0,85** |

## 3 — Sensibilité

Vainqueur aux poids proposés : **2 × RobStride RS00**. 10 variations ±50 % sur 10 le laissent en tête.

| Option | Victoires sur 1 000 tirages |
| --- | ---: |
| 2 × RobStride RS00 | 1000 |

## 4 — Verdict

**Classement ROBUSTE** : 2 × RobStride RS00.

**Une note de jugement que la règle étendue interroge, et qui n'est PAS corrigée ici** (elle n'a pas été demandée) : le transfert à S des options « × Damiao » vaut 3 parce que « k inconnu tant que le banc ne l'a pas mesuré ». Si k n'est plus décisif, le J4310 est le modèle S de la famille retenue dans toute la plage plausible, et cette note serait 5. C'est à Jeremy de le décider ; le changement doit être daté avant d'être appliqué.

**Ce que chaque option vérifie.** L'hypothèse k ne touche que les actionneurs dont la condition de mesure n'est pas publiée : ici **RobStride EduLite 05**. Mesurer son couple continu en blocage **vérifie** que k reste au-dessus de la bascule (critère d'abandon : `docs/protocole-banc.md`). Les options à plusieurs modèles ajoutent une comparaison directe dans la même condition, sans départager la famille.

---

## 5 — Protocole de mesure : les couples continus en condition IDENTIQUE

**Le protocole complet, avec sa section SÉCURITÉ** (alimentation à limitation de courant, arrêt d'urgence matériel, limites logicielles, bras de levier, chauffe au rotor bloqué, ce qu'on ne fait jamais seul) et la consignation de chaque mesure dans `params/mesures.yaml` : `docs/protocole-banc.md` (*proposé*). Résumé :

But : remplacer l'hypothèse k par une mesure, sur les deux finalistes, **dans la même condition**. Les fiches ne sont pas comparables entre elles : plaques différentes, ou condition non précisée. Ce protocole est **proposé**, pas décidé.

1. **Même montage.** Chaque actionneur est fixé sur la **même plaque d'aluminium de 70 × 70 mm** (la plus petite condition publiée, celle du RS05 et de l'EduLite 05). L'épaisseur et la matière sont notées. La plaque est posée sur le même support isolant.
2. **Même alimentation**, à la même tension (celle de l'option), et le même bus CAN au même débit.
3. **Rotor bloqué**, par un bras de levier sur un dynamomètre ou une balance, longueur notée. Le couple **réel** est lu sur le dynamomètre, et le couple **déclaré** par la télémétrie : leur écart est lui-même une mesure. *Le blocage est la condition la plus proche d'un robot qui tient debout ; une mesure en rotation demanderait un frein, et n'est pas prévue ici.*
4. **Mêmes paliers de couple**, par ordre croissant, sur les deux actionneurs : le continu publié le plus bas des deux, puis des paliers de 10 % au-dessus, jusqu'au seuil k × nominal à départager.
5. **Même durée** : chaque palier est tenu jusqu'à l'équilibre thermique (variation < 1 °C sur 5 min), ou au plus 30 min, ou jusqu'à 10 °C sous la protection thermique du constructeur.
6. **Relevés** à 1 Hz : température bobinage et driver (télémétrie), température du boîtier (thermocouple), courant, couple réel. La **température ambiante** est notée au début et à la fin de chaque palier.
7. **Résultat** : le plus haut couple tenu à l'équilibre sous la limite thermique est le **continu mesuré**, dans cette condition. Divisé par le nominal publié, il donne le **k mesuré** de chaque actionneur, à reporter dans le catalogue comme une mesure (fiche 0041) :
   il **vérifie** la décision de famille (critère d'abandon écrit avant la mesure, `docs/protocole-banc.md`).

---

## 6 — Ce que ce comparatif ne dit pas

- Les poids du banc sont **proposés** ; les notes de transfert et de risque sont de **jugement**, justifiées ligne par ligne.
- L'option Feetech n'a **ni prix vérifié ni alimentation 12 V chiffrée** : son coût est inconnu.
- La mesure au rotor bloqué ne dit rien du rendement en rotation ; elle compare les deux finalistes entre eux, dans la même condition.
- **La dispersion entre exemplaires** exige au moins **2 exemplaires d'un même modèle** : trois modèles à un exemplaire n'en mesurent aucune (corrigé le 2026-10-01, audit externe). Deux exemplaires donnent un ordre de grandeur (`docs/protocole-banc.md` § 2 ter) ; l'étude externe du 30-09 en demandait au moins 3 (§ 15.2). Configurations : `params/banc.yaml`, composition **non décidée**.
