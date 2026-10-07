# 0070 — YXOR Lab et YXOR fonctionnent entièrement sur batterie

Date : 2026-10-07
État : acceptée
Complète : `0069-deux-robots-lab-et-final.md` (les deux robots).

Décision coûteuse à inverser (règle 5) : elle fixe l'architecture
électrique des deux robots (aucun câble d'alimentation en
fonctionnement), donc une batterie embarquée, sa masse, son volume dans
le tronc, sa tension (qui doit convenir aux actionneurs) et une autonomie
à dimensionner.

## Décision

**DÉCIDÉE par Jeremy le 2026-10-07.** Ses mots, cités par son prompt du
2026-10-07 (études de marché : batteries, calculateurs, cartes de bus) :
« Les deux robots, YXOR Lab et YXOR, fonctionnent entièrement sur
batterie. Je préfère NVIDIA Jetson, mais je veux une comparaison chiffrée
avec le Raspberry Pi 5 et ses cartes d'IA. »

- **Batterie embarquée** sur les deux robots ; aucun fonctionnement sur
  câble d'alimentation n'est prévu.
- **Calculateur : une PRÉFÉRENCE, pas une décision.** Jeremy préfère
  NVIDIA Jetson et demande une comparaison chiffrée avec le Raspberry
  Pi 5 et ses cartes d'IA (`docs/marche-calculateurs-2026-10.md`). Le
  choix reste ouvert.

## Ce qui n'est PAS décidé

- La chimie, la tension (nombre de cellules en série), la capacité, et la
  forme de la batterie (pack sur mesure, pack du commerce, batterie
  d'outillage) : `docs/marche-batteries-2026-10.md` est une étude.
- L'autonomie visée : tâche « autonomie » PROPOSÉE dans
  `params/capacites.yaml`, à confirmer par Jeremy.
- Le calculateur et l'« IA embarquée » (tâche PROPOSÉE, à confirmer).
- Le seuil d'arrêt et la chaîne de coupure (décisions en attente).

## Conséquences connues

- La protection de surtension des RobStride est à 60 V (manuel RS00,
  p. 28 et 73) et le freinage renvoie de l'énergie dans le bus : la
  tension de pleine charge doit garder une marge sous 60 V
  (`docs/marche-batteries-2026-10.md`, tableau de tension).
- La masse et le volume de la batterie entrent dans la masse du robot et
  dans la place du tronc (explorateur, phase à venir).
