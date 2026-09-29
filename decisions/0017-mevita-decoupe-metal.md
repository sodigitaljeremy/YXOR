# 0017 — MEVITA : la découpe métal a bien un précédent

Date : 2026-09-28
Espèce : historique
État : appliquée
Statut : acceptée
Amende : `0016-plaques-sans-precedent.md`

> **Note de procédure.** Règle 5 : la fiche 0016 n'est pas réécrite, elle
> reçoit un renvoi. La correction est ici.

## Ce qui était faux dans la fiche 0016

> « Aucun projet de robot open source accessible ne construit sa
> structure par découpe 2D en plaques et entretoises. »

**Faux.** Trois projets du laboratoire JSK (université de Tokyo,
Kawaharazuka *et al.*) construisent leur structure en **tôle métallique
découpée** :

| Projet | Type | Référence |
| --- | --- | --- |
| **MEVITA** | bipède | IEEE Humanoids 2025, arXiv 2508.17684, `github.com/haraduka/mevita` |
| **MEVIUS** | quadrupède | arXiv 2409.14721 |
| **MEVIUS2** | quadrupède | arXiv 2603.22031 |

### Vérifié à la source

Résumé de MEVITA, cité mot pour mot :

> « most existing open-source bipedal robots are designed to be fabricated
> using **3D printers, which limits their scalability in size and often
> results in fragile structures** »

C'est le constat de la fiche 0014, formulé par une équipe de recherche et
publié. **Matériaux** : A7075 pour les pièces usinées, A5052 pour la tôle
courante, SUS304 pour la tôle à haute résistance. **Quatre pièces soudées**
seulement : Base-Link, Hip1-Link, Hip2-Link, Calf-Motor-Mount.

**Commande** : les pièces métalliques usinées et soudées sont **chiffrées
et commandées automatiquement à partir d'un fichier STEP** via *meviy*,
service de MISUMI.

### Non vérifié

Les chiffres avancés — 18 pièces métalliques uniques, 19,8 kg, 5 DDL par
jambe — n'ont **pas** pu être lus à la source : la page matérielle n'a pas
répondu et le résumé ne les porte pas. Rapportés par Jeremy, **non
confirmés**.

## Décision

### 1. Le constat de la fiche 0016 est remplacé

> Il **existe** des robots open source dont la structure est en tôle
> métallique découpée. Ce qui n'existe pas, c'est un précédent en
> **découpe seule** : MEVITA recourt au **soudage** pour quatre pièces, et
> à l'**usinage** pour d'autres.

### 2. L'écart réel : le soudage, et il n'est pas mince

| | MEVITA | YXOR |
| --- | --- | --- |
| Découpe | oui | oui |
| **Soudage** | **oui, 4 pièces** | **non** |
| Usinage | oui (A7075) | non |
| Assemblage | permanent sur ces 4 pièces | **démontable partout** |

Le soudage **rend un volume à partir de pièces plates**. C'est
exactement ce que la fiche 0015 recensait comme interdit : loger un
moteur, reprendre un effort en torsion. MEVITA soude précisément là où
il faut un volume — le torse et deux pièces de hanche.

**Point qui nous concerne directement : le soudage est permanent.** La
règle de `CLAUDE.md` « assemblage démontable, aucun collage structurel »
l'exclut de fait. Sans elle, il faudrait encore un poste à souder et le
savoir-faire correspondant.

### 3. Ce qui reste transposable, et c'est beaucoup

- **Le canal de commande.** *meviy* chiffre et fabrique sur envoi d'un
  **STEP**, exactement le format que notre chaîne exporte déjà et dont
  `scripts/check_cad_toolchain.py` vérifie les unités. **C'est la
  découverte la plus directement exploitable** : elle ne suppose ni
  cousin, ni fablab, ni machine.
- **Le choix des matériaux** : A5052 pour la tôle courante, A7075 quand
  il faut de la résistance. Deux nuances sourcées par un projet publié.
- **La démonstration que ça marche.** Un bipède métallique open source
  marche, entraîné en simulation et transféré au réel.
- **L'avertissement sur la masse.** Un bipède métallique est lourd. À
  intégrer avant de dimensionner les actionneurs.

### 4. Ce qui ne se transpose pas

Les **quatre pièces soudées**. Chacune demande un équivalent boulonné :
plus lourd, plus de fixations, moins raide en torsion. C'est le coût à
payer pour rester démontable — et c'est un coût, pas un détail.

**Nuance à ne pas escamoter** : MEVITA n'est pas exempt d'impression 3D.
Semelles et limiteurs d'articulation sont **imprimés en TPU**. Aucun des
projets recensés ne se passe entièrement d'imprimante.

## Conséquences

- La fiche 0015 garde sa décision ; son **isolement** est levé : il
  existe un précédent proche, publié, et une voie de commande utilisable.
- Reste ouvert : boulonner ou souder. Souder rendrait les volumes, au
  prix de la règle du démontable et d'un équipement.
- **Toute affirmation sur un projet tiers se vérifie à la source.** Celle
  de la fiche 0016 ne l'avait pas été.
