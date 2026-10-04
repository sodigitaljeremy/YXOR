# 0068 — S : cheville sans roulis, 5 axes par jambe

Date : 2026-10-04
État : acceptée
Complète : `0067-s-jambes-mixtes-rs02-rs00.md` (sa ligne « roulis de
cheville, RS00 » devient sans objet ; le reste de la 0067 est inchangé).

Décision coûteuse à inverser (règle 5) : elle retire une articulation,
donc un nom (règle 3), deux actionneurs, une pièce de liaison, et elle
écarte S de la topologie de la marche de référence (ToddlerBot, 6 axes par
jambe).

## Décision

**DÉCIDÉE par Jeremy le 2026-10-04.** Ses mots : « Une masse faible au
bout de la jambe compte beaucoup pour bien marcher. Des robots comme
l'Unitree H1 ou MEVITA marchent avec 5 axes par jambe. Option c ». La
source est le prompt de Jeremy du 2026-10-04 ; l'option c est celle du
tableau a/b/c/d de Claude Code du 2026-10-04 (20 h 14, journal du jour).

- **`ankle_roll` est retiré** de S : 5 axes par jambe (lacet, roulis et
  tangage de hanche, genou, tangage de cheville), 10 actionneurs de jambe
  au lieu de 12. v3 : 26 axes au lieu de 28.
- Le nom disparaît partout où il désignait S (règle 3) : `joints.yaml`,
  `squelette.yaml`, `configuration_S.yaml`, `dimensionnement.JAMBE`, la
  CAO. Il reste dans le modèle AMONT (ToddlerBot, sa marche de référence),
  déclaré « non retenu » dans `joints.yaml`.

## Pourquoi

Tableau du 2026-10-04 (20 h 14), par jambe, plaques alu 3 mm :

| | (a) axes décalés | (b) bielles | **(c) sans roulis** | (d) axes concourants |
| --- | --- | --- | --- | --- |
| Hauteur / ANSUR | +77,2 mm | ~0 (cardan non vérifié) | **+11,2 mm** | +6,2 mm (+16,1 avec 10° au talon) |
| Masse sous le tibia | 782 g | ~55 g + cardan, rotules | **55 g** | 458 g |
| Plaques sous le genou | 10 | ≥ 9 + 1 usinée + 4 rotules | **7** | 11 |
| Complexité | faible | forte (couplage) | **la plus faible** | moyenne, pied en porte-à-faux |

## Écarté

- **(a)** : jambe allongée de 77 mm, 782 g au bout de la jambe.
- **(b)** : deux RS00 ne tiennent pas dans le tibia de S (empilés : ~118 mm
  pour ~95 disponibles ; côte à côte : ~115 mm de large pour des axes de
  jambe à 122 mm) ; cardan usiné et rotules hors du « tout en 2D ».
- **(d)** : cheville de 118 mm de large, 291 mm d'encombrement aux
  chevilles ; roulis derrière le talon à 2 mm du sol.

## Hypothèses NON vérifiées

- **L'effort du roulis de cheville, reporté ailleurs, n'est pas chiffré.**
  La marche de référence (ToddlerBot) a 6 axes par jambe : ses besoins au
  roulis de cheville sont ÉCARTÉS du dimensionnement, pas reportés sur la
  hanche. Rien ne dit que le roulis de hanche (déjà saturé 17 % du temps,
  fiche 0067) tient la marche sans cheville en roulis.
- **Aucune politique de marche n'existe pour 5 axes** : celle de
  ToddlerBot (`sim/upstream/`) commande un roulis de cheville.
- **Unitree H1** : cité par Jeremy, non lu par Claude Code ; **MEVITA**
  (5 axes par jambe) : lu le 2026-10-03 (`docs/faisabilite-2d-2026-10-03.md`).
- Le pied ne s'incline plus latéralement : contact au sol sur un bord en
  terrain irrégulier, non étudié.
