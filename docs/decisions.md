# Décisions actives

Les 64 fiches d'avant la refonte sont **archivées** dans
`decisions/archive/`, sans avoir été réécrites. Les fiches écrites depuis
sont dans `decisions/`. Elles portent le détail, les alternatives et
l'historique. Cette page ne liste que ce qui **s'applique aujourd'hui**,
avec qui l'a décidé.

- **Mis à jour** le 2026-10-01, à la refonte R5.
- **Les décisions de la refonte** ont été prises par Jeremy le 2026-10-01 :
  documents archivés, notation remplacée, contrôles réduits, journal
  court. Ses mots : « Concernant les décisions de la refonte : oui à
  tout. » Elles sont consignées au journal du 2026-10-01, sans fiche.
- **Le verdict sur les 13 fiches non attribuées** a été donné par Jeremy
  le 2026-10-01 (prompt de la refonte R5). Ses mots : « je valide toute
  tes recommandations, sauf pour la fiche 0023 que je passerais en B ».
  Les recommandations avaient été proposées par Claude (arbitrage). Plus
  bas, « confirmée par Jeremy (R5) » renvoie à ce prompt.
- **Les règles de travail** sont dans `CLAUDE.md` et ne sont pas
  répétées ici.

## A — Décisions actives

### Méthode et dimensionnement

1. **La taille est une sortie du calcul, pas une entrée.** Chaque
   classe d'actionneur fixe la taille qu'elle porte. C'est
   `scripts/dimensionnement.py` qui la calcule.
   - Décidée par Jeremy le 2026-09-30 (fiche ; journal du 2026-09-30,
     tableau des fiches).
   - Fiche : [0047](../decisions/archive/0047-demarche-inversee.md).
2. **Tailles Banc, S, M, L, XL. Le premier robot est S.**
   - Décidée par Jeremy le 2026-09-30 (fiche ; journal du 2026-09-30).
   - Fiche : [0048](../decisions/archive/0048-tailles-par-classe.md).
3. **ToddlerBot sert de référence de calcul**, avec H0 = 0,56 m. Les
   tailles remplacent les paliers P1, P2 et P3.
   - Validée par Jeremy lors du lot de cohérence du 2026-09-30 (~23 h),
     point 4.
   - Fiche : [0055](../decisions/archive/0055-toddlerbot-reference-et-tailles.md),
     qui remplace la 0001.
4. **Marge de 1,5 sur le couple**, à revoir après le banc.
   - Décidée par Jeremy le 2026-09-30 (fiche ; journal du 2026-09-30).
   - Fiche : [0051](../decisions/archive/0051-marge-de-securite.md).
5. **On dimensionne au couple efficace et au seuil thermique.**
   - Validée par Jeremy lors du lot de cohérence du 2026-09-30 (~23 h),
     points 4 et 7.
   - Fiche : [0062](../decisions/archive/0062-dimensionnement-thermique-applique.md).
6. **Quand deux valeurs publiées coexistent, on retient la plus
   prudente.** Prudente veut dire la plus défavorable à la marge ; pour
   une limite, c'est la plus basse.
   - Décidée par Jeremy le 2026-10-01. Ses mots : « Je valide la règle
     de retenir la valeur la plus prudente et sûre (marge de
     manœuvre) » (lot F).
   - La précision et la règle par défaut ont été validées au lot G
     (journal du 2026-10-01).
   - Fiche : [0064](../decisions/archive/0064-valeur-la-plus-prudente.md).

### Actionneurs, achats et fabrication

7. **S : famille RobStride, avec le RS00 sur les 12 articulations de
   jambe en v1, et H_S = 0,60 m.**
   - Conditions : un recalcul avec charge utile et relevé (sinon on
     redescend vers 0,55 m) ; le banc vérifie le RS00, il ne départage
     plus ; la version du RS00 se vérifie à l'achat.
   - Décidée par Jeremy le 2026-10-01. Ses mots : « Je valide ta
     recommandation sur S. » La recommandation avait été proposée par
     Claude (arbitrage).
   - Fiche : [0065](../decisions/0065-s-robstride-rs00.md).
8. **Règle d'achat.**
   - (a) Un achat pour le robot n'a lieu qu'après une décision écrite et
     la vérification de la référence exacte.
   - (b) L'outillage relève de la seule décision de Jeremy.
   - (c) Claude ne propose jamais d'achat de lui-même.
   - Décidée par Jeremy le 2026-10-01 (R5). Ses mots : « je valide toute
     tes recommandations ».
   - Fiche : [0066](../decisions/0066-regle-d-achat.md), qui remplace la
     0027.
9. **L'actionneur maison est une piste parallèle**, jamais sur le chemin
   critique.
   - Décidée par Jeremy le 2026-09-30 (fiche ; journal du 2026-09-30).
   - Fiche : [0052](../decisions/archive/0052-actionneur-maison.md).
10. **La fabrication est séquencée** : usinage, puis impression 3D, puis
    hybride. Le procédé se choisit pièce par pièce. Les plaques ne sont
    plus le procédé unique.
    - Décidée par Jeremy le 2026-09-30 (fiche 0050).
    - Le remplacement a été validé lors du lot de cohérence du 2026-09-30
      (fiche 0060).
    - Fiches : [0050](../decisions/archive/0050-fabrication-sequencee.md),
      [0060](../decisions/archive/0060-fabrication-sequencee-appliquee.md).
11. **Il n'y a pas d'imprimante 3D aujourd'hui.** L'impression ne
    s'applique qu'une fois une machine disponible et vérifiée.
    - Validée lors du lot de cohérence du 2026-09-30.
    - Fiche : [0059](../decisions/archive/0059-imprimante-etape-deux.md).

### Amont, licences, sources et dépôt

12. **Aucune géométrie ToddlerBot n'entre dans une pièce YXOR**, et
    aucune reconstruction (scan, IA, photo) ne sert à contourner sa
    licence, CC BY-NC-SA 4.0.
    - 0061 : validée lors du lot de cohérence du 2026-09-30.
    - 0045 : confirmée par Jeremy (R5).
    - Fiches : [0061](../decisions/archive/0061-licence-amont-deux-familles.md),
      [0045](../decisions/archive/0045-reconstruction-et-amont.md).
13. **Aucune licence pour l'instant.**
    - Décidée par Jeremy. Ses mots : « aucune pour l'instant » (prompt du
      2026-09-30, ~23 h 50).
    - Fiche : [0063](../decisions/archive/0063-aucune-licence-pour-l-instant.md).
14. **Le dépôt passe public.** C'est Jeremy, pas l'assistant, qui change
    la visibilité.
    - Décidée par Jeremy le 2026-09-30 (fiche).
    - Fiche : [0053](../decisions/archive/0053-depot-public.md).
15. **Deux environnements Python.**
    - ToddlerBot est épinglé au commit `e337f3b`, sous son propre venv.
    - Seul `sim/upstream/` s'exécute sous le venv amont, et seul ce sens
      est vérifié.
    - 0002 : confirmée par Jeremy (R5). 0056 : validée lors du lot de
      cohérence du 2026-09-30.
    - Fiches : [0002](../decisions/archive/0002-pin-toddlerbot.md),
      [0056](../decisions/archive/0056-code-amont-un-seul-sens-verifie.md).
16. **Aucun fichier fournisseur non redistribuable n'entre dans le
    dépôt.** Chaque document obtenu est inscrit à
    `params/fournisseurs.yaml`, avec ses six champs.
    - Confirmée par Jeremy (R5).
    - Fiche : [0030](../decisions/archive/0030-fichiers-fournisseurs.md).
17. **Un registre des sources, pas un index de recherche.** Les documents
    lus sont inscrits dans `params/sources.yaml`, avec leur état de
    lecture.
    - Confirmée par Jeremy (R5).
    - Fiche : [0040](../decisions/archive/0040-registre-des-sources.md).
18. **Provisoires : la CAO sous build123d, et un site statique engendré
    par le dépôt.** La 0009 tient jusqu'au comparatif des outils de CAO.
    - Confirmées comme provisoires par Jeremy (R5).
    - Fiches : [0009](../decisions/archive/0009-build123d.md),
      [0018](../decisions/archive/0018-application-web.md).

## B — Conventions confirmées

Ce ne sont pas des décisions actives : ce sont des façons de faire,
confirmées par Jeremy (R5).

- [0034](../decisions/archive/0034-ratios-ansur-ii.md) : les ratios de
  longueur viennent d'ANSUR II, recalculés depuis les données brutes.
- [0026](../decisions/archive/0026-machine-procede-matiere.md) : un
  réglage de fabrication associe machine, procédé et matière, sous un
  `id` (`params/hardware.yaml`).
- [0033](../decisions/archive/0033-epaisseur-cle-ou-champ.md) :
  l'épaisseur reste un champ du réglage, pas une partie de sa clé.
- [0023](../decisions/archive/0023-simulation-navigateur.md) : la page
  d'une pièce peut se simuler dans le navigateur, sans rien enregistrer.
  **Vu fonctionner par Jeremy le 2026-10-01** (ses mots : « Je te
  confirme que le simulateur est fonctionnel »). **Calcul vérifié contre
  le Python à S, L et 0,55 m** (journal du 2026-10-01). Le test
  `tests/test_simulateur.py` refait cette comparaison à chaque clôture.
  **La pièce à simuler après la semelle est à choisir.**

## C — Closes

- [0024](../decisions/archive/0024-audit-et-refactorisation.md) :
  remplacée par la refonte du 2026-10-01.
- [0032](../decisions/archive/0032-veille-outils.md) : remplacée par les
  comparatifs à venir.

## Questions ouvertes à ce jour

- **La composition du banc** n'est pas décidée. Le banc vérifie le RS00
  (fiche 0065, condition b).
- **La version du RS00** (« ancien » ou « nouveau ») se vérifie au
  moment d'un éventuel achat.
- **Les composants réels de la charge utile** remplaceront l'hypothèse de
  1,2 kg.
- **La pièce à simuler dans le navigateur** après la semelle est à
  choisir (convention 0023).

La grille de S est dans `docs/choix-actionneurs.md`.
