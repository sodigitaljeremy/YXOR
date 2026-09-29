# 0028 — Quatre affirmations d'un retour extérieur, passées au crible

Date : 2026-09-29
Espèce : historique
État : appliquée
Statut : **acceptée** — vérification, pas décision.

Quatre affirmations reposaient sur une source unique. Voici ce qui tient.

| | Affirmation | Verdict |
| --- | --- | --- |
| a | G-code Bambu non reproductible octet pour octet | **le signalement existe et dit exactement cela — mais il n'est corroboré par personne** |
| b | mode local sans aucune connexion sortante | **soutenue dans l'intention, pas dans sa forme absolue** |
| c | DIN 8580 rév. 2022 classe les procédés | **exacte** (déjà vérifiée, fiche 0026) |
| d | bd_warehouse : pièces build123d, Apache 2.0, vis et roulements | **exacte, et vérifiée en l'exécutant** |

## (a) Le G-code n'est pas reproductible

**Le rapport existe** : `bambulab/BambuStudio` **#11560**, ouvert le
**2026-07-15** par `codemakerIO`, intitulé *« CLI: slicing is not
run-to-run deterministic (survives CPU pinning + ASLR off) »*.

Il dit précisément ce qui était annoncé, et davantage. Les écarts ne sont
pas cosmétiques :

- marqueurs `M73` déplacés d'une ligne autour de mouvements identiques ;
- temps estimé à ±1 s ;
- ajustement d'arcs : `I-21.987 J-12.779` contre `I-21.669 J-12.504` ;
- **et une différence de MOUVEMENT réelle** : ralentissement de
  refroidissement à `G1 F13374` contre `G1 F12538` ;
- longueur de filament à ±0,08 mm.

**9 paires divergentes sur 15**, et cela **survit** à `taskset -c 0`
(un seul cœur) et à `setarch -R` (ASLR désactivée). Le rapporteur avance
l'ordre de sommation flottante variant avec la préemption des fils, et
note que `src/libslic3r/Thread.cpp` dimensionne le pool TBB sans qu'aucun
drapeau ne permette de forcer un seul fil.

### Ce qu'il faut en retenir, et la réserve

**Le signalement est un signalement.** Ouvert depuis **deux mois et
demi**, **zéro commentaire, aucun label, aucune réponse de l'éditeur**.
La cause avancée est l'hypothèse du rapporteur, pas un diagnostic établi.

Le classer « fait » serait refaire l'erreur de la fiche 0016. Il est
**crédible et précis** — il donne la commande, les versions
(v02.07.01.62 et v02.06.00.51), les plateformes, le taux d'échec — et
c'est tout ce qu'on peut en dire aujourd'hui.

**Ce que cela impliquerait pour YXOR, si cela se confirmait :** un
G-code ne pourrait pas servir de clé de cache ni de sortie contrôlée par
empreinte. Notre chaîne actuelle n'en produit aucun — nous découpons, nous
n'imprimons pas — donc l'impact est nul aujourd'hui. Il deviendrait réel
le jour d'une imprimante.

## (b) Le mode local

**LAN-only Mode existe**, documenté, et coupe le pilotage du nuage : la
machine ne dialogue qu'avec le réseau local, et la mise à jour de
micrologiciel se fait hors ligne par clé USB ou carte SD.

**Mais la formulation « n'initie AUCUNE connexion extérieure » n'est
établie par aucune source que j'aie trouvée.** Aucune capture réseau,
aucun engagement écrit de l'éditeur en ce sens. C'est une affirmation
qui ne se vérifie que par l'observation du trafic, et personne ne l'a
publiée.

**Et un fait qui compte davantage que la réponse :** en janvier 2025, une
mise à jour de micrologiciel a retiré l'accès au mode LAN ; l'éditeur est
revenu en arrière après la réaction de la communauté. Le mode existe donc
par **politique révocable**, pas par propriété d'architecture. Pour un
projet qui mise sur la durabilité de ses moyens de production, c'est la
nuance qui décide.

## (c) La DIN 8580

Vérifiée au tour précédent, fiche 0026 : `DIN 8580:2022-12` remplace la
révision 2003-09, six groupes principaux ordonnés par le devenir de la
cohésion de la matière. **La norme elle-même n'a pas été lue — elle est
payante.**

## (d) bd_warehouse — vérifiée en l'exécutant

Roue `bd_warehouse-0.3.0-py3-none-any.whl`, 140 ko.

| Point | Constat |
| --- | --- |
| licence | **Apache-2.0** — famille permissive, aucun problème (fiche 0029) |
| dépendance | `build123d>=0.11.1` ; **fonctionne avec notre 0.13.0**, testé |
| vis | `fastener.py`, 140 ko — normes **ISO 4762** et ASME B18.3 |
| roulements | `bearing.py`, 29 ko — **31 tailles**, un seul type `SKT` |
| autres | engrenages, joints toriques, brides, clavettes, filetages, pignons |

**Essai réel** : `SocketHeadCapScrew(size="M3-0.5", length=12,
fastener_type="iso4762")` produit un solide de 125,8 mm³.

### Deux constats qui pèsent sur l'adoption

**1. Il couvre un seul de nos trois roulements.**

| Notre référence | Dimensions | Dans bd_warehouse |
| --- | --- | --- |
| MR85 | 5 × 8 × 2,5 | **absent** |
| 623 | 3 × 10 × 4 | présent |
| 688 | 8 × 16 × 5 | **absent** |

**2. Un piège de cotation.** `length` est la longueur **sous tête**, pas
hors-tout : une M3 `length=12` mesure **15 mm** en tout. Mesuré pour 8,
12 et 16 : la tête ajoute 3 mm à chaque fois. Quiconque prendrait
`length` pour la cote hors-tout se tromperait de la hauteur de tête.

### Ce que j'ai fait du paquet

**Installé, exercé, puis retiré.** Le laisser installé sans l'inscrire
dans `requirements.txt` aurait créé exactement le piège que ce projet
traque : le code aurait pu s'en servir ici et la construction Docker
aurait échoué, sans que rien n'explique pourquoi. Le dépôt et
`requirements.txt` restent cohérents.

    .venv/bin/pip install bd_warehouse      # pour y revenir

### La question ouverte, que je ne tranche pas

Une cote venue d'`ISO 4762` est-elle d'origine `catalogue` — « fiche
technique d'un constructeur » — ou `litterature` — « publication
scientifique ou norme » ? Une norme ISO n'est ni l'un ni l'autre
exactement. La taxonomie de la fiche 0010 n'avait pas prévu le cas.

## Sources

- [BambuStudio #11560](https://github.com/bambulab/BambuStudio/issues/11560) —
  lu par l'API GitHub le 2026-09-29 : ouvert, 0 commentaire, 0 label.
- Documentation et retours communautaires sur le mode LAN-only.
- Roue `bd_warehouse` 0.3.0 depuis PyPI, métadonnées et modules lus,
  code exécuté avec le venv du projet.
