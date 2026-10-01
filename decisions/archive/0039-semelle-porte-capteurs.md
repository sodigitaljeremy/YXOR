# 0039 — La vraie semelle sera d'abord un porte-capteurs

Date : 2026-09-29
Espèce : historique
État : appliquée
Statut : **note** — ne conçoit rien, n'engage aucune géométrie.

## Le constat, vérifié

Kajita, *Introduction to Humanoid Robotics*, **§3.2 « Measurement of
ZMP »**, et en particulier **§3.2.2 « ZMP of Each Foot »**, p. 79 : le ZMP
d'un robot humanoïde se mesure par des **capteurs d'effort six axes**
logés dans le pied, un par pied, dont on combine les mesures.

Vérifié en ouvrant l'ouvrage. Le rapport Bennehar décrit le même montage.

**Aucun texte n'est reproduit ici** — fiche 0035 : on cite une référence
et un fait, jamais la rédaction.

## Ce que cela dit de la semelle

La semelle d'apprentissage **ne s'interface avec rien**, et c'est vrai —
c'est même ce qui la rend coupable aujourd'hui (fiche 0037).

Mais **la vraie semelle ne sera pas une plaque de pied. Ce sera un
support de capteur.** Sa géométrie sera dictée au moins autant par
l'encombrement, la fixation et la reprise d'effort du capteur six axes
que par le ratio `pied_longueur` d'ANSUR II.

Trois conséquences, notées sans être instruites :

1. **Le ratio anthropométrique donnera une enveloppe, pas une forme.**
   138 × 52 mm sera la boîte dans laquelle le montage doit tenir, pas le
   contour de la pièce.
2. **Un capteur six axes se monte entre deux plaques rigides** : la
   semelle deviendra un empilement, et non une pièce plate. C'est
   exactement le cas où la fiche 0015 atteint sa limite, et où la
   question de la fiche 0022 — un sous-ensemble peut-il être un
   composant ? — se posera pour de bon.
3. **Elle aura des interfaces**, donc la saignée et le voile minimal lui
   seront nécessaires. Elle ne sera pas coupable avant qu'on les ait
   mesurés — et la pièce d'apprentissage, en étant coupée, les donnera.

## Pourquoi cette note existe

Pour qu'on ne parte pas de la semelle d'apprentissage en croyant tenir la
forme de la vraie. Elle exerce la méthode ; elle ne préfigure pas la
pièce.

## Source

Kajita, S. et al., *Introduction to Humanoid Robotics*, Springer, §3.2 et
§3.2.2, p. 79. Ouvrage **sous droits** — voir `params/fournisseurs.yaml`.
