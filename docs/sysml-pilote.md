# Pilote SysML v2 : la gamme YXOR en modèle

**Rédigé le 2026-10-08.** Essai, **aucune décision** : le YAML de `params/` reste la **source de vérité** ;
`model/yxor.sysml` en est une **vue engendrée** par `scripts/sysml.py`, jamais éditée à la main. Le pilote avait
été proposé le 2026-10-06 par les rapports de méthodologie (« SysML v2 en pilote sur un sous-ensemble, à côté du
YAML »). Terrain d'essai : la gamme Kit / Lab / Home / Pro (fiche 0073), que SysML v2 décrit nativement comme une
famille de produits à variantes.

## Ce que contient le modèle (431 lignes, toutes engendrées)

- **Axes** : les 16 axes de `params/joints.yaml` (règle 3 : les mêmes noms partout), chacun une `part def`
  spécialisant `Articulation`.
- **Ensembles d'axes** : les quatre ensembles de l'explorateur (25, 26, 27, 29), avec le nombre de chaque axe ;
  le roulis de cheville y apparaît avec sa vraie situation (« amont_non_retenus », fiche 0068) et la pince comme
  nom provisoire.
- **Capacités** : les 16 tâches de `params/capacites.yaml`, chacune un `enum def` de ses niveaux.
- **Gamme** : une `variation part def Gamme` aux quatre `variant` (Kit, Lab, Home, Pro) ; chaque modèle
  spécialise `ModeleYXOR` et fixe le niveau visé de ses capacités. Kit et Home sont vides (à définir), le Pro
  porte ses niveaux « à balayer », le Lab ses niveaux décidés (saut 5 cm, relevé dos ET ventre, autonomie 30 min,
  IA « + vision »).
- **Exigences du Lab** : 22 exigences de couple de pointe, une par articulation et par tâche, sous la forme
  τ ≥ a·M + b (phases 3a et 3b, à H_S = 0,60 m, M restant un paramètre : c'est exactement la règle du
  maximum de l'explorateur) ; l'autonomie (30 min, cycle 40 s + 20 s) et le niveau d'IA.
- **Traçabilité** : chaque exigence de couple dépend de son axe (`dependency … to Axes::…`) ; son nom porte la
  capacité et le niveau dont elle vient (`couple_knee_saut_vertical_n5`).

## Outillage (relevé du 2026-10-08)

Un agent a évalué 13 candidats, installés dans le dossier de session (rien hors de lui) et essayés sur un fichier
juste et un fichier faux.

| Outil | Licence | Valide en ligne de commande ? | Retenu |
| --- | --- | --- | --- |
| **OpenSysML** (Open-MBEE), v0.9.2 du 2026-10-05 | Apache-2.0 | **oui** : code 0 si propre, 2 sur erreur ; binaire unique de 43 Mo, sans Java, bibliothèque standard intégrée, ~0,1 s | **oui, PROPOSÉ** |
| Implémentation pilote OMG (version 2026-08) | EPL-2.0 | pas de commande : enveloppe Java de 35 lignes écrite par l'agent ; JDK 21 portable, ~485 Mo, 6 à 8 s | second avis |
| spec42 (v0.54.1) | MIT | oui, mais un nom non résolu n'est qu'un avertissement (code 0) sans `--warnings-as-errors` | écarté |
| sysml2 (C) | — | plante (signal 11) avec la bibliothèque officielle | écarté |
| SysON (Obeo) | — | éditeur web (Docker + PostgreSQL), aucune validation en ligne de commande | écarté |
| syside (Sensmetry) | propriétaire, clé de licence | — | écarté |
| sysml-2ls | — | archivé par son auteur | écarté |
| sysml-validate | gratuiciel, pas libre | — | écarté |

**Résultat sur `model/yxor.sysml`** : OpenSysML « no errors », code 0 ; implémentation pilote OMG : syntaxe 0,
sémantique 0, avertissements 0. Le test `tests/test_sysml.py` vérifie que le fichier est à jour, qu'il est
valide, et qu'une erreur de syntaxe et une référence non résolue faites exprès sont vues. Le binaire n'est pas
dans le dépôt (règle 4) : `scripts/outil_sysml.py` le télécharge dans `exports/outils/opensysml/` et vérifie ses
deux empreintes (archive et binaire), outillage décidé par Jeremy le 2026-10-08 (« Oui, télécharge durablement
OpenSysML dans exports/, hors de Git, avec son empreinte. ») ; la variable `YXOR_SYSML` peut en désigner un autre.
Absent, ou d'empreinte fausse, la validation **saute et le dit**.

**Limites de la validation** (essais de l'agent) : OpenSysML s'arrête à la première erreur de syntaxe, et n'a pas
vu une `attribute def` spécialisant une `part def` ; spec42 n'a pas vu un `variant` hors d'une variation ;
**aucun** outil ne vérifie qu'une contrainte est SATISFAITE, seulement qu'elle est bien écrite (OpenSysML annonce
`-constraint` et `-requirement`, lus dans son README, non essayés). Licence de la bibliothèque standard SysML :
EPL-2.0 selon le README officiel (lu), LGPL-3.0 selon la notice de spec42 : contradiction non tranchée.

## Ce que le modèle apporte

- **Une vue d'ensemble lisible par d'autres** : la gamme, ses axes, ses capacités et ses exigences dans un langage
  normalisé (OMG, adopté en juin 2025), qu'un outil ou une personne extérieure au projet peut ouvrir.
- **La gamme comme famille à variantes** : `variation` / `variant` disent nativement ce que la fiche 0073 décide
  (quatre modèles d'une même famille), là où le YAML n'a que des profils côte à côte.
- **Une traçabilité explicite** capacité → exigence → axe, vérifiée par un outil (un axe renommé dans
  `joints.yaml` casserait une `dependency`, et la validation le verrait).
- **Un format d'échange** : si un jour un outil MBSE (SysON, un éditeur graphique) doit servir, le modèle existe.

## Ce qu'il coûte

- **Un outil hors du dépôt** : le binaire OpenSysML (45 Mo) vit dans `exports/` (hors de Git), téléchargé et
  vérifié par `scripts/outil_sysml.py` ; sans lui, la validation saute.
- **Une validation partielle** : syntaxe et noms, pas la satisfaction des exigences ; les calculs (couples,
  masses, explorateur) restent en Python, que SysML ne remplace pas.
- **Un générateur à maintenir** (environ 200 lignes) : chaque nouvelle donnée de `params/` à montrer demande du
  code ; le risque de divergence est nul (le fichier est engendré et testé), le coût est le temps.
- **Une valeur encore faible pour un projet à une personne** : le YAML, les rapports engendrés et les tests
  donnent déjà la traçabilité dont le projet se sert ; SysML la rend lisible par un tiers, qui n'existe pas encore.

## Recommandation (PROPOSÉE)

**Garder tel quel**, comme vue engendrée et testée, sans l'étendre pour l'instant.

- **Pas « étendre »** : rien dans le projet ne lit aujourd'hui le modèle ; l'étendre (interfaces, analyses,
  états) doublerait des calculs que Python fait déjà, avec un outillage dont la validation reste partielle.
- **Pas « arrêter »** : le coût de le garder est minime (un script, un test, une régénération), et il a déjà
  prouvé deux choses : la gamme s'y exprime naturellement, et la traçabilité capacité → exigence → axe se vérifie
  par un outil standard.
- **Ce qui ferait changer d'avis** : un besoin d'échange réel (un contributeur, une revue, un outil MBSE), la
  décision de documenter le Kit pour des fabricants (le modèle pourrait engendrer la nomenclature des modules),
  ou un outil qui vérifie la satisfaction des contraintes. À ce moment-là : étendre aux interfaces (connecteurs,
  bus, modules interchangeables), qui sont le cœur du « design unique ».

## Question close

Le validateur vit durablement dans `exports/`, empreinte vérifiée (Jeremy, 2026-10-08, fiche 0066, b).
