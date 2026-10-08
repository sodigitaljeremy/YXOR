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
2. **Deux robots : YXOR Lab (apprentissage) et YXOR (final) ; la gamme
   S/M/L/XL est abandonnée ; pièces hybrides dès maintenant.** Noms
   provisoires. L'ensemble d'axes et la hauteur du Lab ne sont PAS
   décidés ; la 0068 est à revoir à ce moment-là.
   - Décidée par Jeremy le 2026-10-04. Ses mots : « Ok l'option c me
     semble très bien 👍 » et « et l'on peut d'ailleurs directement opter
     pour la stratégie de conception et de modélisation via des pièces
     hybrides » (prompt du 2026-10-05). Le contenu détaillé de l'option C
     est de Claude, accepté par ces mots.
   - Fiche : [0069](../decisions/0069-deux-robots-lab-et-final.md), qui
     remplace la [0048](../decisions/archive/0048-tailles-par-classe.md)
     (tailles Banc, S, M, L, XL ; Jeremy, 2026-09-30) et, pour l'ordre
     des procédés, la [0050](../decisions/archive/0050-fabrication-sequencee.md).
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

7. **S : famille RobStride, jambes mixtes : RS02 au roulis et au
   tangage de hanche et au genou, RS00 au lacet de hanche et à la
   cheville ; H_S = 0,60 m, repli 0,55 m.**
   - Décidée par Jeremy le 2026-10-02. Ses mots : « Je pars sur l'option
     B. » (option B du calcul de Claude Code du 2026-10-02, 19 h 38).
   - Répartition : `params/configuration_S.yaml`, vérifiée par
     `scripts/choix_actionneurs.py`. Hypothèses : haut du corps de la v3
     en RS05, une seule marche de référence.
   - Fiche : [0067](../decisions/0067-s-jambes-mixtes-rs02-rs00.md), qui
     remplace la [0065](../decisions/0065-s-robstride-rs00.md) (RS00 sur
     les 12 articulations, Jeremy, 2026-10-01).
7 bis. **S : cheville sans roulis, 5 axes par jambe.** `ankle_roll` est
   retiré de S (10 actionneurs de jambe, v3 à 26 axes).
   - Décidée par Jeremy le 2026-10-04. Ses mots : « Une masse faible au
     bout de la jambe compte beaucoup pour bien marcher. Des robots comme
     l'Unitree H1 ou MEVITA marchent avec 5 axes par jambe. Option c »
     (option c du tableau de Claude Code du 2026-10-04, 20 h 14).
   - Hypothèse non vérifiée : l'effort de roulis de la marche de référence
     (6 axes) est écarté, pas reporté.
   - Fiche : [0068](../decisions/0068-s-cheville-sans-roulis.md), qui
     complète la [0067](../decisions/0067-s-jambes-mixtes-rs02-rs00.md).
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
    hybride. ⚠ L'ordre est remplacé par la 0069 (hybride dès maintenant). Le procédé se choisit pièce par pièce. Les plaques ne sont
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

19. **YXOR Lab et YXOR fonctionnent entièrement sur batterie.** Le
    calculateur n'est PAS décidé : Jeremy préfère NVIDIA Jetson et demande
    une comparaison chiffrée avec le Raspberry Pi 5 et ses cartes d'IA.
    - Décidée par Jeremy le 2026-10-07. Ses mots : « Les deux robots, YXOR
      Lab et YXOR, fonctionnent entièrement sur batterie. Je préfère NVIDIA
      Jetson, mais je veux une comparaison chiffrée avec le Raspberry Pi 5
      et ses cartes d'IA. » (prompt du 2026-10-07).
    - Fiche : [0070](../decisions/0070-robots-sur-batterie.md).
20. **Autonomie et IA embarquée de chaque robot.** YXOR Lab : 30 min,
    commande + vision ; YXOR (final) : 60 min, modèle de langage local ;
    cycle de 40 s de marche suivies de 20 s debout. 12S ou 13S : pas
    encore tranché.
    - Décidée par Jeremy le 2026-10-07. Ses mots : « Je confirme les tâches
      autonomie et IA embarquée, et le cycle de 40 s de marche suivies de
      20 s debout. Pour YXOR Lab : autonomie 30 minutes, IA embarquée
      commande + vision. Pour YXOR final : autonomie 60 minutes, IA
      embarquée avec modèle de langage local. Je trancherai entre 12S et
      13S sur les chiffres. » (prompt du 2026-10-07, soir).
    - Fiche : [0071](../decisions/0071-autonomie-et-ia-par-robot.md), qui
      complète la [0070](../decisions/0070-robots-sur-batterie.md).
21. **Batterie 12S pour les deux robots.** La tension de coupure n'est
    pas décidée (variante 2,5 / 3,0 / 3,2 V par cellule).
    - Décidée par Jeremy le 2026-10-08. Ses mots : « Je retiens le 12S
      pour les deux robots, sur les chiffres de l'explorateur du 7
      octobre. » (prompt du lot 4a sexies).
    - Fiche : [0072](../decisions/0072-batterie-12s.md), qui complète la
      [0071](../decisions/0071-autonomie-et-ia-par-robot.md).

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

- **La composition du banc** n'est pas décidée ; telle qu'étudiée, elle
  ne couvre que le RS00, pas le RS02 (fiche 0067).
- **Une seconde marche de référence avant l'achat des 12 moteurs** :
  PROPOSÉ, non décidé (fiche 0067).
- **La version du RS00** (« ancien » ou « nouveau ») se vérifie au
  moment d'un éventuel achat.
- **Les composants réels de la charge utile** remplaceront l'hypothèse de
  1,2 kg.
- **La pièce à simuler dans le navigateur** après la semelle est à
  choisir (convention 0023).

La grille de S est dans `docs/choix-actionneurs.md`.
