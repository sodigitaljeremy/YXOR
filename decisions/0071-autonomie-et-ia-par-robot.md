# 0071 — Autonomie et IA embarquée de chaque robot

Date : 2026-10-07 (soir)
État : acceptée
Complète : `0070-robots-sur-batterie.md` (ses points « autonomie visée » et
« IA embarquée », laissés ouverts, sont tranchés ici ; le reste de la
0070 est inchangé).

Décision coûteuse à inverser (règle 5) : l'autonomie fixe l'énergie de la
batterie, donc sa masse, son volume dans le tronc et le courant que les
actionneurs doivent porter ; le niveau d'IA fixe le calculateur, sa
puissance et sa chaleur.

## Décision

**DÉCIDÉE par Jeremy le 2026-10-07.** Ses mots, prompt de la phase 4a
quinquies : « Je confirme les tâches autonomie et IA embarquée, et le
cycle de 40 s de marche suivies de 20 s debout. Pour YXOR Lab : autonomie
30 minutes, IA embarquée commande + vision. Pour YXOR final : autonomie
60 minutes, IA embarquée avec modèle de langage local. Je trancherai entre
12S et 13S sur les chiffres. »

| | YXOR Lab | YXOR (final) |
| --- | --- | --- |
| Autonomie (cycle 40 s de marche + 20 s debout) | 30 min | 60 min |
| IA embarquée | commande + vision | modèle de langage local |

Inscrit dans `params/capacites.yaml` (tâches `autonomie` et
`ia_embarquee`, confirmées ; profils `lab` et `final`).

## Ce qui n'est PAS décidé

- **12S ou 13S** : Jeremy tranchera « sur les chiffres » (explorateur,
  variantes 12S et 13S).
- Le calculateur, la batterie, la chaîne de puissance : études.
- Les critères qui traduisent un niveau d'IA en matériel (mémoire,
  accélérateur) : PROPOSÉS par Claude dans l'explorateur, à confirmer.
