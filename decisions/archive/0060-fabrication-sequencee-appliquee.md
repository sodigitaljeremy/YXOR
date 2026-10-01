# 0060 — Les plaques et entretoises ne sont plus le procédé unique

Date : 2026-09-30
Espèce : gouvernante
État : acceptée
Statut : **acceptée** — lot de cohérence validé par Jeremy le 2026-09-30 (~23 h), point 4. Appliquée dans CLAUDE.md (point 5 du même lot) ; aucune pièce nouvelle.
Remplace : `0015-architecture-plaques-entretoises.md`

## Pourquoi remplacer la 0015

La 0015 disait : « YXOR est conçu en plaques et entretoises, **découpe 2D
exclusivement** ». Elle faisait du carton le cas de conception le plus
contraignant. La 0050 décide une **fabrication séquencée** : usinage,
puis impression 3D, puis hybride. Le carton n'y est plus qu'une
**maquette rapide, sans métrologie** (cadrage § 1, principe 4 ;
caractérisation du carton arrêtée le 2026-09-30).

## La décision

1. **La découpe 2D n'est plus le procédé unique.** Plaques et entretoises
   restent **une** architecture possible, parmi l'usinage, l'impression
   et l'hybride. Le procédé se choisit pièce par pièce, dans l'ordre de
   la 0050.
2. **« Concevoir au plus contraignant, au carton » est retiré.** Le
   carton sert à vérifier une forme, une taille, un emboîtement. Il ne
   borne plus la conception, et aucune cote n'est tirée de ses mesures.
3. **Ce qui reste vrai pour toute pièce découpée en 2D**, quel que soit
   le matériau :
   - contour fermé, en millimètres, à l'échelle 1:1 ;
   - rayon intérieur au moins égal à 0,5 × l'épaisseur ;
   - saignée **mesurée** par couple machine-matériau ;
   - épaisseur et saignée en **paramètres**.
4. **Ce qui reste vrai pour toute pièce** :
   - assemblage démontable, sans collage structurel ;
   - pas de logement de roulement obtenu directement par le procédé ;
   - vis traversante et écrou, sauf un insert posé dans une pièce
     imprimée (0059).
5. **Restent ouverts** :
   - le procédé exact de l'opérateur CN : rayons d'outil, matières,
     format de fichier (cadrage, question 6) ;
   - les douze transmissions à engrenage ou à différentiel que la 0015
     rouvrait (§ Décision, point 4). Leur déclencheur devient **la
     conception des jambes de S**.
