# Comparatif du banc d'essai

**Engendré** par `.venv/bin/python scripts/selection_multicritere.py --ecrire`, le 2026-09-30, par la même méthode que `docs/choix-classe-S.md`. Aucun achat n'est proposé : ce comparatif prépare le choix de Jeremy (cadrage § 6 et § 13, question 12).

Les options dépendent du classement de S : vainqueur nominal **Damiao DM-J4310-2EC V1.2**, second **CubeMars AK45-10 V3.0 KV75**. Si ce classement change, ce document change.

---

## 1 — Les options

| Option | Ce qu'elle apprend | Transfert à S | Coût TTC CH | Postes non chiffrés | Risque |
| --- | --- | --- | ---: | --- | --- |
| 1 × Damiao DM-J4310-2EC V1.2 | 2/5 : protocole, thermique | 5 — exactement le modèle retenu pour S | ≥ 211 CHF | alimentation 24 V (non chiffrée) | 3 — pas de rechange : une casse arrête le banc |
| 2 × Damiao DM-J4310-2EC V1.2 | 4/5 : protocole, thermique, bus_multi_adresses, segment_2ddl | 5 — exactement le modèle retenu pour S | ≥ 367 CHF | alimentation 24 V (non chiffrée) | 5 — rechange disponible, un seul modèle à maîtriser |
| 3 × Damiao DM-J4310-2EC V1.2 | 5/5 : protocole, thermique, bus_multi_adresses, segment_2ddl, dispersion | 5 — exactement le modèle retenu pour S | ≥ 524 CHF | alimentation 24 V (non chiffrée) | 5 — rechange disponible, un seul modèle |
| 1 × Damiao DM-J4310-2EC V1.2 + 1 × CubeMars AK45-10 V3.0 KV75 | 4/5 : protocole, thermique, bus_multi_adresses, segment_2ddl | 3 — un seul des deux actionneurs est le modèle retenu (JUGEMENT : 3) | ≥ 372 CHF | alimentation 24 V (non chiffrée) | 3 — deux modèles, deux protocoles possibles à maîtriser, pas de rechange de chacun |
| 2 × Feetech STS3250 (banc d'apprentissage) | 4/5 : protocole, thermique, bus_multi_adresses, segment_2ddl | 1 — autre fabricant et autre protocole que S | ≥ 10 CHF | prix Feetech STS3250, prix Feetech STS3250, alimentation 12 V (non chiffrée) | 1 — impasse : bus TTL et servo à engrenages, rien ne se transfère à une classe S en CAN |

Coût TTC CH = (actionneurs + adaptateur + alimentation du bus) × (1 + imprévus) × (1 + TVA 8,1 %). Adaptateur CAN : candleLight de Linux Automation, **prototype non conforme CE** selon son fabricant. Alimentation 48 V : Mean Well RSP-500-48. Un poste non chiffré met la note de coût à 0.

---

## 2 — Notes et score

| Critère | Poids (proposé) | 1 × Damiao DM-J4310-2EC V1.2 | 2 × Damiao DM-J4310-2EC V1.2 | 3 × Damiao DM-J4310-2EC V1.2 | 1 × Damiao DM-J4310-2EC V1.2 + 1 × CubeMars AK45-10 V3.0 KV75 | 2 × Feetech STS3250 (banc d'apprentissage) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| apprentissage | 35 | 2 | 4 | 5 | 4 | 4 |
| transfert_S | 25 | 5 | 5 | 5 | 3 | 1 |
| cout | 25 | 0 | 0 | 0 | 0 | 0 |
| risque | 15 | 3 | 5 | 5 | 3 | 1 |
| **score /5** | | **2,40** | **3,40** | **3,75** | **2,60** | **1,80** |

## 3 — Sensibilité

Vainqueur aux poids proposés : **3 × Damiao DM-J4310-2EC V1.2**. 8 variations ±50 % sur 8 le laissent en tête.

| Option | Victoires sur 1 000 tirages |
| --- | ---: |
| 3 × Damiao DM-J4310-2EC V1.2 | 1000 |

**Le critère de coût ne départage rien** : aucune option n'est entièrement chiffrée (voir « Postes non chiffrés »), donc toutes ont la note 0. Le verdict repose sur les trois autres critères.


## 4 — Verdict

**Classement ROBUSTE** : 3 × Damiao DM-J4310-2EC V1.2.

## 5 — Ce que ce comparatif ne dit pas

- Les poids et les notes de risque sont **proposés** ; la sensibilité dit si le classement en dépend.
- L'option Feetech n'a **ni prix vérifié ni alimentation 12 V chiffrée** : son coût est inconnu, sa note de coût vaut 0.
- Le banc à trois exemplaires répond à la condition « au moins 3 RS05 » de l'étude externe (§ 15.2), qui veut mesurer la dispersion entre exemplaires.
