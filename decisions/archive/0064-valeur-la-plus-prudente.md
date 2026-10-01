# 0064 — Deux valeurs publiées : retenir la plus prudente

Date : 2026-10-01
Espèce : gouvernante
État : acceptée
Statut : **acceptée** — décidée par Jeremy le 2026-10-01, ses mots : « Je valide la règle de retenir la valeur la plus prudente et sûre (marge de manœuvre) » (prompt du lot F, 2026-10-01, point 2). La précision du § 2 est **PROPOSÉE par Claude (arbitrage)**.

## 1 — La règle (décidée par Jeremy)

Quand deux valeurs publiées d'une même grandeur coexistent pour un même
produit, **on retient la plus prudente et la plus sûre**, c'est-à-dire
celle qui laisse le plus de **marge de manœuvre**.

## 2 — Ce que « la plus prudente » veut dire (PROPOSÉ par Claude)

**La plus défavorable au dimensionnement** :

| Grandeur | Valeur retenue | Pourquoi |
| --- | --- | --- |
| couple (continu, pointe) | la **plus basse** | l'actionneur porte moins, donc on dimensionne pour moins |
| vitesse | la **plus basse** | idem |
| masse | la **plus haute** | un robot plus lourd demande plus de couple |
| résistance | la **plus haute** | plus de pertes, plus de chaleur |
| température | la **plus haute**, pour une température **subie** (ambiante, échauffement) | idem |

**Limite de cette précision, à trancher.** Pour une **limite de
protection** (une température d'arrêt), le prudent est la **plus
basse** : s'arrêter plus tôt. Le RS05 en donne deux, 145 °C (manuel,
p. 12) et 135 °C (p. 34, 50). La règle du tableau prendrait 145 °C, ce
qui serait **l'inverse** de la prudence. Proposition : une limite se
traite comme une capacité, donc on prend la plus basse.

## 3 — Ce qui n'est PAS une valeur concurrente (PROPOSÉ par Claude)

- **Une valeur REMPLACÉE par le constructeur.** Le J4310 V1.2 pèse
  **306 g** dans le manuel V1.4, dont l'historique dit « Weight
  corrected » ; une version antérieure portait **325 g**, selon l'audit
  externe du 30-09 (valeur non retrouvée ici). Le constructeur a
  remplacé l'une par l'autre : ce ne sont pas deux valeurs publiées
  **en même temps**. On retient la valeur en vigueur, 306 g.
- **Deux conditions de mesure différentes.** Un continu en rotation et
  un continu au blocage, ou deux tailles de plaque, mesurent deux
  choses. Ils restent portés côte à côte, avec leur condition. La
  capacité prudente prend déjà le blocage quand il est publié.
- **Une variante d'un autre produit.** Le GIM4310 avec le driver GDS34
  n'est pas le même produit qu'avec le GDZ34 ; le X4-36-E-L n'est pas
  le X4-36-E.
- **Une lecture non vérifiée** (résumé d'outil de recherche, page non
  ouverte). Ce n'est pas une valeur publiée : elle reste en note
  `non_verifie`.

## 4 — Application

- Le RS05 à 1,6 N·m, retenu le 2026-09-30 « sur consigne de Jeremy »
  (en réalité le prompt P1 de l'arbitrage), **relève de cette règle**.
  Ses renvois sont remplacés par un renvoi à cette fiche.
- **Inventaire** des cas du catalogue : journal du 2026-10-01, lot F,
  point 2. Les cas qui ne suivent pas la règle y sont listés. **Aucune
  valeur n'est changée** par cette fiche : chaque changement passera par
  sa propre modification datée.
