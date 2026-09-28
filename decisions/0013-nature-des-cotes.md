# 0013 — Nature des cotes : la règle 1 restreinte à son domaine

Date : 2026-09-28
Statut : acceptée
Restreint : la règle 1 de `CLAUDE.md`

## Contexte

La règle 1 énonce que « toute dimension structurelle dérive de `H` et
d'un ratio ». Elle est juste pour une longueur de segment. Elle est
**fausse** pour une épaisseur de paroi, un diamètre d'axe ou une
nervure : celles-là dérivent d'une charge, d'un matériau et d'un procédé.

**La règle n'est pas à supprimer, elle est à restreindre.**

## Pourquoi c'est dangereux et non seulement inexact

`anthropometry.yaml` porte déjà la clé du problème :

> « entre deux paliers de rapport k, la masse varie en **k³** et le
> couple articulaire requis en **k⁴** »

Une cote d'échelle suit `k`. Une cote de tenue suit la charge, donc `k³`
ou `k⁴`. Les faire dériver toutes deux linéairement de `H` revient à
**sous-dimensionner massivement les grandes tailles**.

Et cela ne produit **aucune erreur visible** : la pièce se dessine, le
STEP s'exporte, la simulation tourne. Elle casse en P3, sur le robot
réel. C'est le mode de défaillance que ce projet rencontre pour la
cinquième fois.

## Décision

### Un second axe, orthogonal à l'origine

L'**origine** (fiches 0010 et 0011) dit *d'où vient le nombre*. La
**nature** dit *ce qui le détermine*. Les deux sont indépendants : une
cote peut être `propre` d'origine et `tenue` de nature.

| Nature | Déterminée par | Règle applicable |
| --- | --- | --- |
| `echelle` | `H` × ratio | **la règle 1, inchangée** |
| `tenue` | charge, matériau, coefficient de sécurité | note de calcul obligatoire |
| `interface` | quincaillerie, pièce du commerce | **la règle 2** — ne suit jamais `H` |
| `procede` | moyen de fabrication | contraintes de fabrication de `CLAUDE.md` |

### Portée de la règle 1, désormais

> La règle 1 s'applique aux cotes de nature **`echelle`**, et à
> elles seules. Une cote de nature `tenue`, `interface` ou `procede` qui
> dériverait de `H` est un **défaut**, exactement comme une cote
> d'échelle écrite en dur.

La règle 2 n'est pas modifiée : elle correspond exactement à
`interface`, qu'elle décrivait déjà sans le nommer.

### Dans le code des pièces

Le contrat d'accesseur de la fiche 0010 s'étend sans rien casser — la
nature devient le nom de la méthode, l'origine reste portée par la
déclaration :

```python
l_cuisse = C.echelle("ratios.cuisse")             # règle 1
d_vis    = C.interface("vis.M3.passage")          # règle 2
r_min    = C.procede("rayon_interieur_min")       # contrainte de fabrication
e_paroi  = C.tenue(charge=..., materiau=..., coef=..., critere="flexion")
```

**`C.tenue()` refuse un nombre nu.** Elle exige la charge, le matériau,
le coefficient de sécurité et le critère. Une cote de tenue sans note de
calcul est un défaut au même titre qu'un littéral.

`C.propre()` de la fiche 0010 devient `C.echelle()` : le mot décrivait
l'origine, pas ce qui détermine la cote. Aucun code n'existe encore qui
l'utilise.

### Mise en place aujourd'hui

`params/origines.yaml` accueille un champ `nature` à côté de `origine`,
et `scripts/audit_origines.py` rend compte des deux axes. Le module
`yxor/cotes.py` reste à écrire avec la première pièce, comme prévu.

## Conséquences

- Une cote peut être `litterature` d'origine et `echelle` de nature : ce
  sont deux questions différentes, et les confondre était la faille.
- L'audit peut désormais répondre à « quelle cote de tenue n'a pas de
  note de calcul ? », qui est une question de sécurité et non de licence.
- `CLAUDE.md` mentionne la restriction et renvoie ici.
