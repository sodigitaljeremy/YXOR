# Instructions — projet YXOR

Robot humanoïde bipède paramétrique. Jeremy est développeur (JS/TS, Python) et
**débutant complet en CAO et en mécanique**. Explique les notions mécaniques au
passage, sans les supposer acquises.

## Règles non négociables

1. **Aucune cote en dur.** Toute dimension structurelle dérive de `H` et d'un
   ratio défini dans `params/anthropometry.yaml`. Une valeur en millimètres
   écrite directement dans le code d'une pièce est un bug.
2. **Sauf la quincaillerie.** Les cotes liées aux vis, roulements, inserts et
   servomoteurs sont fixes et viennent de `params/hardware.yaml`. Elles ne
   suivent jamais `H`.
3. **Noms d'articulations stables.** Ceux de `params/joints.yaml`, identiques
   dans la CAO, l'URDF et le code de contrôle. Jamais de variante locale.
4. **Rien de binaire dans Git.** Les STEP, STL, DXF, URDF et rendus vont dans
   `exports/`, qui est ignoré. Ils se régénèrent.
5. **Une décision structurante = une fiche** dans `decisions/`, écrite *avant*
   d'être appliquée. Jamais réécrite après coup.

## Après chaque génération de pièce

Produire un rendu de contrôle et le signaler. La géométrie produite par un
agent est régulièrement fausse de façon non évidente : trou décalé, épaisseur
insuffisante, collision entre pièces. Ne jamais présenter une pièce comme
correcte sans qu'elle ait été régénérée et regardée.

## Contraintes de fabrication à respecter dès la conception

- Pièce imprimée : tient dans 256 × 256 mm.
- Pièce découpée : contour fermé, millimètres, échelle 1:1, rayon intérieur
  minimum 0,5 × épaisseur, aucun angle vif rentrant.
- Aucun logement de roulement obtenu directement par découpe : prévoir un
  palier rapporté ou un alésage repris.
- Filetage dans le plastique : insert à chaud, jamais taraudage direct.
- Assemblage démontable, aucun collage structurel.

## Environnement

- PC portable **sans carte graphique**, dans une machine virtuelle VirtualBox.
  L'accélération 3D y est limitée : prévoir un rendu hors écran si la fenêtre
  de simulation ne fonctionne pas.
- Entraînement par renforcement : jamais en local, toujours sur GPU distant.
- VPS Hetzner : régénération et publication seulement, pas de calcul.

## Ce qu'il ne faut pas faire

- Proposer d'acheter du matériel avant la phase 6 du plan d'action.
- Avancer sur une phase suivante tant que la précédente n'est pas sortie.
- Introduire une dépendance GPL ou CERN-OHL-S dans le cœur du projet.