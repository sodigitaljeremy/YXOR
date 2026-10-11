# 0076 — Cadrage de la gamme, Kit en parcours guidé, réemploi

Date : 2026-10-11
État : acceptée
Remplace EN PARTIE : `0074-kit-modules-successifs.md` et `0075-kit-progressif-feetech-petits-axes.md` (détail
plus bas). Complète : `0073-gamme-yxor.md` (les quatre modèles restent).

Décision coûteuse à inverser (règle 5) : elle regroupe la gamme en deux familles, fixe le principe du Kit
(un parcours guidé, étape par étape), l'outillage du Kit, la règle de réemploi (tout composant se démonte et se
remonte dans n'importe quelle variante du Kit et du Lab), la frontière 2D / 3D entre les modèles, et la position du
projet sur la sécurité et les achats.

## Décision : les mots de Jeremy

**DÉCIDÉE par Jeremy.** Ses mots, cités tels quels (prompt du 2026-10-11, qui les date) :

- **2026-10-09** : « Je vois 2 grandes familles se dessiner : 1. La famille de Robot IA Humanoïde conçu et
  développé pour être réalisable par Monsieur et Madame tout le monde. Il s'agit de YXOR Kit et YXOR Lab. 2. La
  famille des Robot IA Humanoïde conçu et développé à un autre niveau de complexité et de performance. Il s'agit de
  YXOR Home et YXOR Pro. » ; « ce n'est pas figé » ; « définir plusieurs variantes en fonction des limites et
  contraintes physiques, techniques, matérielles, financières ».
- **Budget** : « Le budget se déterminera en fonction des choix matériels de chaque modèle et de chaque variante
  […] même philosophie de composants interchangeables que Framework et Fairphone. »
- **Outillage du Kit** : « cutter, feuille, imprimante, cartons, agrafeuse, règle, équerre, pistolet à colle, mais
  pas d'imprimante 3D, Fablab ».
- **2026-10-11** : « mes contraintes d'outillages […] ne visaient que le modèle YXOR Kit » ; le Lab « sera conçu et
  modélisé qu'en 2D […] avec d'autres matériaux tels que l'alu ou autres » ; « on intégrera de la conception et
  modélisation 3D qu'à partir du modèle YXOR Home ».
- **Sécurité** : « doit être un sujet à part entière et bien réfléchi… néanmoins mon projet doit spécifier qu'il
  décline toute responsabilité ».
- **Achats** : « mon projet pourra donner ses préconisations et les composants qu'il utilise, sans les imposer ».
- **Kit** : « avoir un robot plus évolutif qui pourrait être construit étape par étape […] permettre aux personnes
  de s'initier à la robotique avec des projets guidés ».
- **Réemploi** : « je veux que chaque achat de composant, de matériel soit réfléchi pour être réutilisable, je veux
  que cela soit vu comme un investissement et non un simple achat... il faut impérativement pouvoir monter et
  démonter chaque composant et les remonter dans n'importe quelles variantes des modèles YXOR Kit et YXOR Lab. »

## Ce qui en découle (lecture, sans rien ajouter aux mots)

- **Deux familles** : Kit et Lab (réalisables par tous) ; Home et Pro (autre niveau de complexité et de
  performance). Le cadrage « n'est pas figé ».
- **Variantes** par modèle, selon les limites physiques, techniques, matérielles et financières ; le **budget** est
  une sortie des choix matériels de chaque variante.
- **Kit** : un parcours guidé, étape par étape. **Outillage du Kit seulement** : cutter, feuille, imprimante (à
  papier), cartons, agrafeuse, règle, équerre, pistolet à colle ; **ni imprimante 3D, ni Fablab**.
- **Lab** : conçu et modélisé **en 2D**, en aluminium ou autres matériaux ; la **3D** commence avec le **Home**.
- **Réemploi** : tout composant se monte, se démonte et se remonte dans n'importe quelle variante du Kit et du Lab.
- **Achats** : le projet préconise et documente ce qu'il utilise, sans l'imposer (conforme à la fiche 0066).
- **Sécurité** : un sujet à part entière, à traiter ; le projet décline toute responsabilité (formulation à rédiger).

## Ce que cette fiche remplace, et ce qui reste

| Fiche | Partie | Statut |
| --- | --- | --- |
| 0074 | « des modules successifs » | **reste**, précisé : un parcours guidé, étape par étape |
| 0074 | « mêmes dimensions, taille et composants que le Lab » | **remplacé** par la règle de réemploi (monter, démonter, remonter dans n'importe quelle variante du Kit et du Lab) |
| 0074 | outillage « cutter, règle, équerre, voire un pistolet à colle » | **remplacé** par la liste du 2026-10-09 (feuille, imprimante, cartons, agrafeuse en plus ; ni imprimante 3D ni Fablab) |
| 0074 | carton « le mieux adapté » | **reste** |
| 0075 | **niveaux 0 à 4** du Kit (3 = debout en Feetech, la marche = le Lab) | **remplacé** par le parcours guidé ; ses étapes sont PROPOSÉES (`docs/kit-parcours-2026-10.md`), non décidées |
| 0075 | option progressive (secteur 12 V aux niveaux 1-2, batterie au 3 en boîtier ignifuge) | le **principe reste** (acheter un composant au moment où il sert) ; son rattachement aux anciens niveaux devient caduc, à reprendre sur le parcours |
| 0075 | critère de recyclage, assemblage B | **restent** ; l'assemblage B est précisé par la règle de réemploi (colle et agrafes seulement entre deux pièces de structure) |
| 0075 | **Feetech aux petits axes de toute la gamme** | **reste** |

## Ce qui n'est PAS décidé

- Les étapes du parcours (PROPOSÉES), leurs composants (préconisés, jamais imposés), la variante IA (réseau ou
  locale), le bras (deux bras de 3 axes ou un SO-101).
- Les interfaces communes (motif de trous, vis, câble, connecteur, rail, bus, protocole) : listées, à fixer plus tard.
- La formulation de la clause de non-responsabilité et le dossier sécurité.
- La taille du Kit (gelée à 0,65 m depuis la fiche 0075, en attendant Jeremy).
