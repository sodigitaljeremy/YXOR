# 0029 — CERN-OHL-S n'est pas non commerciale : trois familles, pas deux

Date : 2026-09-29
Espèce : historique
État : appliquée
Statut : **acceptée** — correction d'une erreur de classement.
Amende : `0009-build123d.md`, et la règle de `CLAUDE.md`.
Remplacée par : `0061-licence-amont-deux-familles.md` — la conception ToddlerBot est CC BY-NC-SA, donc dans DEUX familles, pas CC BY-NC.

## L'erreur

`CLAUDE.md` portait :

> Introduire une dépendance GPL ou **CERN-OHL-S** dans le cœur du projet.
> *(dans « Ce qu'il ne faut pas faire »)*

La règle était juste. **Le motif était faux** : CERN-OHL-S était rangée
avec les licences qui interdisent de vendre. Elle ne l'est pas.

## Ce que dit la licence

Vérifié sur le texte publié par SPDX :

- **§3.1** — copier et diffuser des copies conformes ;
- **§3.2** — modifier, à condition de s'engager irrévocablement à publier
  la source modifiée ;
- **§4** — **« You may Make Products, and/or Convey them »**, à condition
  de fournir la source complète ou d'en indiquer l'emplacement.

**Aucune clause ne restreint l'usage commercial.** Fabriquer et vendre
est explicitement permis. Ce que la licence impose est la
**réciprocité** : tout dérivé, et tout ensemble plus large qui l'inclut,
doit être publié sous la même licence.

C'est du **copyleft fort**, l'équivalent matériel de la GPL.

## Les trois familles, qu'il ne faut plus confondre

| Famille | Exemples | Vendre ? | Garder fermé ? |
| --- | --- | --- | --- |
| **non commerciale** | CC BY-NC, CC BY-NC-SA | **non** | — |
| **copyleft, réciproque** | GPL, AGPL, CERN-OHL-S, CERN-OHL-W | **oui** | **non** |
| **permissive** | MIT, Apache-2.0, BSD, ISC | oui | oui |

La distinction entre les deux premières n'est pas une nuance de juriste,
c'est **l'opposé** :

- « commercial interdit » ferme la **porte de sortie** : on ne peut jamais
  vendre, quoi qu'on fasse ;
- « commercial autorisé sous réciprocité » laisse la porte ouverte et
  ferme la **porte de derrière** : on peut vendre, mais on ne peut pas
  garder ses plans pour soi.

La famille CERN-OHL a d'ailleurs trois degrés : **-P** permissive,
**-W** faiblement réciproque, **-S** fortement réciproque. Seule la
dernière contamine l'ensemble.

## Ce que cela change pour YXOR

**La règle de `CLAUDE.md` tient, mais pour le bon motif.** Elle est
reformulée : ce qui est exclu du cœur est le **copyleft fort**, parce
qu'il obligerait à publier nos propres plans — pas parce qu'il
empêcherait de vendre.

**Et cela clarifie le vrai risque du projet.** La mécanique amont de
ToddlerBot est en **CC BY-NC** : première famille, celle qui interdit la
vente. C'est elle, et elle seule, qui pèse sur les **1121 cotes d'origine
`amont`** que l'audit compte à chaque régénération.

Ranger CERN-OHL-S avec CC BY-NC brouillait cette lecture : cela laissait
croire à deux risques de même nature, alors qu'il n'y en a qu'un — et que
le second n'aurait, lui, jamais empêché de vendre.

**Rien à changer au code.** `build123d` est Apache-2.0, OCP/OCCT en LGPL
avec exception, `ezdxf` MIT, `PyYAML` MIT, `bd_warehouse` Apache-2.0
(fiche 0028). Aucune dépendance n'est concernée.

## Ce que cette fiche ne tranche pas

La portée juridique du fait que 1121 cotes dérivent d'un modèle CC BY-NC
**reste non tranchée** — fiche 0010 §4. Cette fiche corrige un
classement de licences ; elle ne donne aucun avis juridique et n'en a pas
la compétence.

## Sources

- [SPDX — CERN-OHL-S-2.0](https://spdx.org/licenses/CERN-OHL-S-2.0.html),
  texte de la licence, §3 et §4 lus le 2026-09-29.
- [CERN Open Hardware Licence](https://en.wikipedia.org/wiki/CERN_Open_Hardware_Licence),
  pour les trois degrés P / W / S.
