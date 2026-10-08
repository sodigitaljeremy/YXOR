# 0072 — Batterie 12S pour les deux robots

Date : 2026-10-08
État : acceptée
Complète : `0071-autonomie-et-ia-par-robot.md` (son point « 12S ou 13S :
Jeremy tranchera sur les chiffres » est tranché ici ; le reste de la 0071
est inchangé).

Décision coûteuse à inverser (règle 5) : la tension du bus moteurs est une
interface. Elle fixe le nombre de cellules en série, le BMS, le seuil de
l'absorbeur de régénération, la plage d'entrée des convertisseurs et la
vitesse des actionneurs en fin de décharge.

## Décision

**DÉCIDÉE par Jeremy le 2026-10-08.** Ses mots, prompt du lot 4a sexies :
« Je retiens le 12S pour les deux robots, sur les chiffres de l'explorateur
du 7 octobre. »

- Pack Li-ion **12S** (nominal 43,2 V ; pleine charge 50,4 V ; coupure à
  préciser, étudiée en variante : 2,5, 3,0 ou 3,2 V par cellule) pour YXOR
  Lab et YXOR (final).

## Les chiffres du 7 octobre (explorateur, commit 17465bd)

- 12S laisse 9,6 V sous la protection de surtension des RobStride (60 V) ;
  13S, 5,4 V.
- En 13S, aucun absorbeur de régénération du marché relevé ne convenait :
  le module de décharge RobStride (notice V1.1) se déclenche à 53,5 V, sous
  la pleine charge d'un 13S (54,6 V) ; en 12S (50,4 V), il convient.
- La vitesse en fin de décharge est plus basse en 12S (×0,625 à 2,5 V par
  cellule contre ×0,677 en 13S) : c'est le prix de ce choix, étudié par la
  variante de tension de coupure (lot 4a sexies).

## Ce qui n'est PAS décidé

- La tension de coupure (seuil d'arrêt du BMS) : variante 2,5 / 3,0 / 3,2 V.
- La cellule, le pack, la chaîne de puissance : études.
