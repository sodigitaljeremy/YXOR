# Décisions actives

Les 64 fiches de décision sont **archivées** dans `decisions/archive/`,
sans avoir été réécrites. Elles portent le détail, les alternatives et
l'historique. Cette page ne liste que ce qui **s'applique aujourd'hui**,
avec qui l'a décidé.

- **Mis à jour** le 2026-10-01, à la refonte R2.
- **Les décisions de la refonte** (documents archivés, notation
  remplacée, contrôles réduits, journal court) ont été décidées par
  Jeremy le 2026-10-01. Ses mots : « Concernant les décisions de la
  refonte : oui à tout. » Elles sont consignées au journal du
  2026-10-01 ; elles n'ont pas de fiche.
- **Les règles de travail** sont dans `CLAUDE.md` et ne sont pas
  répétées ici.

## Méthode et dimensionnement

1. **La taille est une sortie du calcul, pas une entrée.** Chaque
   classe d'actionneur fixe la taille qu'elle porte. C'est
   `scripts/dimensionnement.py` qui la calcule.
   Décidée par Jeremy le 2026-09-30 (fiche ; journal du 2026-09-30,
   tableau des fiches). Fiche : [0047](../decisions/archive/0047-demarche-inversee.md).
2. **Tailles Banc, S, M, L, XL. Le premier robot est S.**
   Décidée par Jeremy le 2026-09-30 (fiche ; journal du 2026-09-30).
   Fiche : [0048](../decisions/archive/0048-tailles-par-classe.md).
3. **ToddlerBot sert de référence de calcul**, avec H0 = 0,56 m. Les
   tailles remplacent les paliers P1, P2 et P3. Validée par Jeremy lors
   du lot de cohérence du 2026-09-30 (~23 h), point 4. Fiche :
   [0055](../decisions/archive/0055-toddlerbot-reference-et-tailles.md),
   qui remplace la 0001.
4. **Marge de 1,5 sur le couple**, à revoir après le banc. Décidée par
   Jeremy le 2026-09-30 (fiche ; journal du 2026-09-30).
   Fiche : [0051](../decisions/archive/0051-marge-de-securite.md).
5. **On dimensionne au couple efficace et au seuil thermique.** Validée
   par Jeremy lors du lot de cohérence du 2026-09-30 (~23 h), points 4 et
   7. Fiche : [0062](../decisions/archive/0062-dimensionnement-thermique-applique.md).
6. **Quand deux valeurs publiées coexistent, on retient la plus
   prudente.** Prudente veut dire la plus défavorable à la marge ; pour
   une limite, c'est la plus basse.
   - Décidée par Jeremy le 2026-10-01. Ses mots : « Je valide la règle
     de retenir la valeur la plus prudente et sûre (marge de
     manœuvre) » (lot F).
   - La précision et la règle par défaut ont été validées au lot G
     (journal du 2026-10-01).
   - Fiche : [0064](../decisions/archive/0064-valeur-la-plus-prudente.md).

## Actionneurs et fabrication

7. **L'actionneur maison est une piste parallèle**, jamais sur le chemin
   critique. Décidée par Jeremy le 2026-09-30 (fiche ; journal du
   2026-09-30). Fiche : [0052](../decisions/archive/0052-actionneur-maison.md).
8. **La fabrication est séquencée** : usinage, puis impression 3D, puis
   hybride. Le procédé se choisit pièce par pièce. Les plaques ne sont
   plus le procédé unique.
   - Décidée par Jeremy le 2026-09-30 (fiche 0050).
   - Remplacement validé lors du lot de cohérence du 2026-09-30
     (fiche 0060).
   - Fiches : [0050](../decisions/archive/0050-fabrication-sequencee.md),
     [0060](../decisions/archive/0060-fabrication-sequencee-appliquee.md).
9. **Il n'y a pas d'imprimante 3D aujourd'hui.** L'impression ne
   s'applique qu'une fois une machine disponible et vérifiée. Validée
   lors du lot de cohérence du 2026-09-30.
   Fiche : [0059](../decisions/archive/0059-imprimante-etape-deux.md).

## Amont, licences et dépôt

10. **Aucune géométrie ToddlerBot n'entre dans une pièce YXOR.** La
    mécanique amont est sous CC BY-NC-SA 4.0. Aucune reconstruction (scan,
    IA, photo) n'est permise pour contourner cette licence.
    - 0061 : validée lors du lot de cohérence du 2026-09-30.
    - 0045 : « règle posée par Jeremy » selon la fiche, sans source
      citée ; **à confirmer par Jeremy**.
    - Fiches : [0061](../decisions/archive/0061-licence-amont-deux-familles.md),
      [0045](../decisions/archive/0045-reconstruction-et-amont.md).
11. **Aucune licence pour l'instant.** Décidée par Jeremy. Ses mots :
    « aucune pour l'instant » (prompt du 2026-09-30, ~23 h 50).
    Fiche : [0063](../decisions/archive/0063-aucune-licence-pour-l-instant.md).
12. **Le dépôt passe public.** Décidée par Jeremy le 2026-09-30 (fiche).
    C'est Jeremy, pas l'assistant, qui change la visibilité.
    Fiche : [0053](../decisions/archive/0053-depot-public.md).
13. **Deux environnements Python.**
    - ToddlerBot est épinglé au commit `e337f3b`, sous son propre venv.
    - Seul `sim/upstream/` s'exécute sous le venv amont, et seul ce sens
      est vérifié.
    - 0056 : validée lors du lot de cohérence du 2026-09-30.
    - 0002 : attribution non établie dans la fiche ; **à confirmer par
      Jeremy**.
    - Fiches : [0002](../decisions/archive/0002-pin-toddlerbot.md),
      [0056](../decisions/archive/0056-code-amont-un-seul-sens-verifie.md).
14. **Aucun fichier fournisseur non redistribuable n'entre dans le
    dépôt.** Chaque document obtenu est inscrit à
    `params/fournisseurs.yaml`, avec ses six champs. Attribution non
    établie dans la fiche ; **à confirmer par Jeremy**.
    Fiche : [0030](../decisions/archive/0030-fichiers-fournisseurs.md).
15. **La CAO se fait sous build123d**, et le site est statique, engendré
    par le dépôt. Attribution non établie dans les deux fiches ; **à
    confirmer par Jeremy**.
    Fiches : [0009](../decisions/archive/0009-build123d.md),
    [0018](../decisions/archive/0018-application-web.md).

## Fiches archivées dont l'attribution n'est pas établie

Ces fiches ne figurent pas dans la liste active. **À confirmer par
Jeremy**, si l'une doit y entrer :

- [0023](../decisions/archive/0023-simulation-navigateur.md) : simulation
  dans le navigateur ;
- [0024](../decisions/archive/0024-audit-et-refactorisation.md) : audit
  et refactorisation ;
- [0026](../decisions/archive/0026-machine-procede-matiere.md) : machine,
  procédé, matière ;
- [0027](../decisions/archive/0027-regle-phase-6.md) : remplacement de la
  règle de la « phase 6 », dont les règles d'achat a, b et c de
  CLAUDE.md ;
- [0032](../decisions/archive/0032-veille-outils.md) : veille d'outils ;
- [0033](../decisions/archive/0033-epaisseur-cle-ou-champ.md) :
  l'épaisseur reste un champ ;
- [0034](../decisions/archive/0034-ratios-ansur-ii.md) : ratios
  ANSUR II ;
- [0040](../decisions/archive/0040-registre-des-sources.md) : registre
  des sources.

## Questions ouvertes à ce jour

- **La famille d'actionneurs de S** n'est pas décidée.
- **La composition du banc** n'est pas décidée.
- **La hauteur de calcul de S** sera fixée par Jeremy avant R3.

Les comparatifs en cours sont dans `docs/choix-famille-actionneurs.md`
et `docs/comparatif-banc.md`, tous deux remplacés en R3.
