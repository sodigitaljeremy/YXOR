# Instructions — projet YXOR

Robot humanoïde bipède paramétrique. Jeremy est développeur (JS/TS, Python) et
**débutant complet en CAO et en mécanique**. Explique les notions mécaniques au
passage, sans les supposer acquises.

## Règles non négociables

1. **Aucune cote en dur.** Toute dimension structurelle dérive de `H` et d'un
   ratio défini dans `params/anthropometry.yaml`. Une valeur en millimètres
   écrite directement dans le code d'une pièce est un bug.
   **Restreinte aux cotes de nature `echelle`** (fiche 0013) : une épaisseur de
   paroi, un diamètre d'axe ou une nervure ne dérivent PAS de `H` mais d'une
   charge, d'un matériau et d'un procédé. Les y faire dériver linéairement
   sous-dimensionnerait les grandes tailles sans qu'aucune erreur n'apparaisse.
2. **Sauf la quincaillerie.** Les cotes liées aux vis, roulements, inserts et
   servomoteurs sont fixes et viennent de `params/hardware.yaml`. Elles ne
   suivent jamais `H`.
3. **Noms d'articulations stables.** Ceux de `params/joints.yaml`, identiques
   dans la CAO, l'URDF et le code de contrôle. Jamais de variante locale.
4. **Rien de binaire dans Git.** Les STEP, STL, DXF, URDF et rendus vont dans
   `exports/`, qui est ignoré. Ils se régénèrent.
5. **Une décision structurante = une fiche** dans `decisions/`, écrite *avant*
   d'être appliquée. Jamais réécrite après coup.

## Après chaque génération de pièce

Produire un rendu de contrôle et le signaler. La géométrie produite par un
agent est régulièrement fausse de façon non évidente : trou décalé, épaisseur
insuffisante, collision entre pièces. Ne jamais présenter une pièce comme
correcte sans qu'elle ait été régénérée et regardée.

## Contraintes de fabrication à respecter dès la conception

**Procédé unique : la découpe 2D.** Il n'y a pas d'imprimante 3D
(fiche 0014). Architecture en plaques et entretoises (fiche 0015).

- **Toute pièce est plate**, d'épaisseur constante, issue d'un profil
  découpé. Un volume s'obtient par empilement de plaques et entretoises,
  jamais par une pièce massive.
- Pièce découpée : contour fermé, millimètres, échelle 1:1, rayon intérieur
  minimum 0,5 × épaisseur, aucun angle vif rentrant.
- Aucun logement de roulement obtenu directement par découpe : prévoir un
  palier rapporté ou un alésage repris.
- Assemblage démontable, aucun collage structurel. Pas de filetage dans le
  matériau : **vis traversante et écrou**.
- **Concevoir au plus contraignant**, c'est-à-dire au carton. Les trois
  procédés accessibles sont le cutter (carton), le laser de fablab
  (contreplaqué) et la découpe métal (aluminium). Un dessin qui ne passe
  pas en carton interdit l'itération rapide, qui est le principal acquis
  de cette architecture.
- **L'épaisseur et la saignée sont des paramètres, jamais des constantes.**
  Un même modèle génère un DXF par couple machine-matériau. La saignée se
  mesure sur une pièce d'essai, elle ne se suppose pas.

### Contraintes retirées le 2026-09-28, et pourquoi

Conservées ici : une contrainte caduque effacée en silence est une
information perdue, et rien ne signalerait son retour si une imprimante
était acquise.

- ~~« Pièce imprimée : tient dans 256 × 256 mm »~~ — c'était le volume
  d'une machine qui n'existe pas. **À rétablir telle quelle** si une
  imprimante est acquise, en vérifiant le volume réel de la machine.
- ~~« Filetage dans le plastique : insert à chaud, jamais taraudage
  direct »~~ — un insert à chaud se pose dans du thermoplastique imprimé.
  Ni le contreplaqué, ni le carton, ni l'aluminium n'en acceptent. Reste
  vraie pour toute pièce imprimée future.

## Environnement

- PC portable **sans carte graphique**, sous **WSL2** (Ubuntu 26.04). WSLg
  ouvre bien une fenêtre, mais n'expose aucun GPU : le rendu est logiciel
  (llvmpipe). Prévoir un rendu hors écran pour tout ce qui est répétitif.
- Entraînement par renforcement : jamais en local, toujours sur GPU distant.
- VPS Hetzner : régénération et publication seulement, pas de calcul.

### Deux interpréteurs Python — ne jamais les confondre

Voir `decisions/0002-pin-toddlerbot.md`.

| | Code YXOR | Pile ToddlerBot |
| --- | --- | --- |
| Venv | `~/yxor/.venv/` | `~/upstream/toddlerbot/.venv/` |
| Python | 3.14.4 | 3.12.14 (fourni par uv) |
| MuJoCo | 3.13.0 | 3.3.4 |

- Tout ce qui est dans ce dépôt se lance avec `.venv/bin/python` — **sauf
  `sim/upstream/`**, seul répertoire qui s'exécute avec le venv amont parce
  qu'il importe `toddlerbot` (fiche 0004). L'inverse est interdit dans les
  deux sens, mais **un seul sens est vérifié à l'exécution** :
  `sim/upstream/` refuse de démarrer sous le mauvais interpréteur
  (`require_upstream_env()`). **Le code YXOR ne vérifie rien.** Lancé
  sous le venv amont, il tournerait avec MuJoCo 3.3.4 sans rien signaler.
  Ce sens ne repose que sur la discipline, et sur le contrôle manuel
  ci-dessous.
- ToddlerBot exige Python ≤ 3.12 : ses versions épinglées (`numpy==1.26.4`,
  `jaxlib==0.4.28`, `torch==2.3.1`) n'ont pas de roue pour 3.14. Ce n'est pas
  contournable sans maintenir un fork.
- Se tromper de venv donne soit un `ImportError`, soit — plus vicieux — une
  version de MuJoCo différente de celle sur laquelle les mesures ont été
  prises. En cas de doute : `python -c "import mujoco; print(mujoco.__version__)"`.
- Le code amont vit dans `~/upstream/`, **hors du dépôt**. Rien de ce qui s'y
  trouve ne doit être copié ou commité ici.

## Ce qu'un contrôle doit faire pour valoir quelque chose

Quatre règles apprises le **2026-09-29**, chacune au prix d'une faute
réelle. Elles portent toutes sur la même chose : **un système qui échoue
en silence est pire qu'un système qui n'existe pas**, parce qu'on
construit dessus.

### 1. Tout contrôle annonce la TAILLE de ce qu'il a inspecté

> « N pages », « N fichiers suivis », « N motifs », « dont N
> numériques » — le nombre lu dans la sortie du contrôle, jamais recopié
> ici.

**Un zéro se voit ; un vert ne se voit pas.** `controler_html` a annoncé
« balises équilibrées sur toutes les pages » — sur zéro page.
`controle_depot` a dit « 0 fichiers suivis, aucun binaire », ce qui est
vrai et ne veut rien dire. Les deux échouent désormais sur entrée vide.

Corollaire : **un contrôle qui saute le DIT**, avec sa raison.
`controle_depot` et `index_fiches` sautent en construction Docker et
l'annoncent. Un saut muet est un vert volé.

*Fiches 0024 (§4), et le journal du 2026-09-29.*

### 2. Un motif qui capte plus de la moitié d'un fichier doit être assumé

Un joker `**` qui couvre tout un fichier rend `non_qualifie`
**inatteignable** : l'audit y sort vert par construction, quoi qu'on
écrive. Mesuré le 2026-09-29 : **plus de la moitié des valeurs**
inventoriées étaient dans ce cas (chiffres au journal du jour).

Un fourre-tout reste parfois le bon choix — un fichier ENGENDRÉ n'a pas à
être qualifié ligne à ligne. Mais alors il porte `fourre_tout: true`,
écrit à la main. `scripts/controle_regles.py` le refuse autrement.

*Fiche 0020, et le contrôle des règles mortes.*

### 3. Ce qui peut se calculer se calcule — jamais se déclarer

**Une convention écrite à la main diverge.** La ligne `Date:` des fiches
était déclarée : elle a disparu de **quatre fiches d'affilée** sans que
rien ne le dise. La convention de statut a divergé en six formulations.

Ce n'est pas de la paresse, c'est structurel : une déclaration répétée
sur N éléments coûte N occasions de se tromper. Un axe calculé en coûte
zéro.

**Le contre-poison** : un calcul qui ne peut pas échouer est aussi
dangereux qu'une déclaration qui diverge. Il ne dérive pas, il **se
trompe en silence** si sa règle de lecture est trop lâche. Donc on
rapporte sa répartition, et un basculement massif alerte.

*Fiche 0035 (§ correction du 2026-09-29).*

### 4. Tout artefact servi porte son empreinte dans son URL

Sinon un cache le fige, et le site sert du périmé **avec l'air d'être à
jour**.

Constaté **trois fois le même jour**, sous trois formes :

| Forme | Ce qui était périmé |
| --- | --- |
| construction Docker muette | 4 h, le site entier |
| SHA affiché mais incomparable | le signal lui-même |
| `expires 7d` sur URL fixe | la feuille de style, **et le plan A4 de découpe** |

Le troisième est le plus grave : un plan corrigé restait téléchargeable
une semaine. L'empreinte du contenu dans l'URL — `?v=...` — change dès
que le site change. **Elle permet de GARDER le cache long**, qui est
utile, au lieu de le supprimer.

Et l'empreinte doit se calculer **de la même façon partout**. Un premier
jet montrait le SHA git en local et un repli en Docker : les deux ne se
seraient jamais comparées, et un signal qu'on ne peut pas confronter ne
signale rien.

    .venv/bin/python scripts/empreinte.py

*Journal du 2026-09-29, et `scripts/empreinte.py`.*

## Sources sous droits : une valeur, jamais le texte

Normes (ISO, DIN) et ouvrages (Springer, Elsevier, MIT Press) sont payants
et protégés. Le dépôt en extrait **des valeurs numériques avec leur
référence précise**, et rien d'autre.

- **Jamais** d'extrait rédigé, de tableau recopié, de figure reproduite.
- Une valeur isolée accompagnée de sa référence est un **fait** ; la
  rédaction et la mise en forme sont l'**œuvre** de l'auteur.
- **Si la source n'a pas été lue, la fiche le dit.** Ce n'est pas une
  précaution de style : c'est ce qui permet à quelqu'un d'autre de savoir
  quoi vérifier. Fait pour la DIN 8580 (fiche 0026), pour ISO 4762
  (0028), et à refaire chaque fois.
- Le fichier lui-même **n'entre pas dans le dépôt** et s'inscrit dans
  `params/fournisseurs.yaml` avec ses six champs (fiche 0030).

Voir `decisions/0035-origine-norme.md`.

## Ce qu'il ne faut pas faire

- ~~Proposer d'acheter du matériel avant la phase 6 du plan d'action.~~

  ⚠ **Remplacée le 2026-09-29** (fiche 0027). Le plan d'action n'a jamais
  existé : la règle renvoyait à un document absent, donc à un critère que
  personne ne pouvait constater. Trois règles la remplacent, parce qu'elle
  mélangeait trois choses distinctes.

  **a. Ce qui est lié à une pièce** — matériau, quincaillerie, découpe :
  rien n'est proposé à l'achat tant que la pièce n'est pas **`coupable`**.
  Une pièce est `coupable` quand toutes les cotes de son procédé sont
  renseignées — donc quand on sait ce qu'on achète, et pourquoi.

  **Ce qui existe réellement** : `etat_procede` le calcule et le site
  l'affiche. **Rien ne le refuse** : `regenerer.py` ne bloque aucun achat,
  et aucun contrôle ne s'oppose au verdict. La règle tient par la
  conduite, pas par un outil.

  **Et le verdict est aujourd'hui inerte.** `besoins_procede` est déduit
  de ce que la pièce lit. Or toute pièce constructible lit son épaisseur
  et son rayon minimal, sans quoi elle ne se dessine pas. Ni la saignée ni
  le voile minimal n'y figurent. `coupable` est donc vrai dès que la pièce
  se construit sur un réglage dont la machine est connue
  (`pages.etat_procede`). Le seul chemin pour qu'une pièce se bloque
  elle-même est `c.besoin()`, qu'aucune pièce n'appelle. Le verdict
  redeviendra utile à la première pièce qui s'emboîte.

  **b. L'outillage** — imprimante, balance, pied à coulisse, instruments :
  **aucun critère automatique**. C'est la décision de Jeremy, et elle est
  hors de portée de l'assistant. Ne pas inventer de garde-fou ici : il
  serait faux, et il donnerait l'illusion d'en avoir un.

  **c. Et celle qui ne dépend de rien :** *l'assistant ne propose jamais
  un achat de lui-même.* Si Jeremy demande un comparatif, il le donne,
  complet et chiffré. Il ne suggère pas de dépenser. Cette règle n'a ni
  exception ni condition — c'est la seule des trois qui visait vraiment
  un risque d'assistant, et c'est celle que la « phase 6 » portait sans
  le dire.

- Avancer sur une phase suivante tant que la précédente n'est pas sortie.
- **Passer une géométrie ToddlerBot dans un outil de reconstruction**
  (scan, maillage, plan ou photo vers CAO, générateur 3D par IA) pour en
  tirer une pièce ou une cote YXOR. Une reconstruction ne transforme pas
  une œuvre dérivée en conception originale : elle en produit une
  dérivation mieux documentée. Si cela arrive, le résultat reste
  `amont`. **Non outillée** : aucun contrôle ne voit ce qui part vers
  un service tiers. Fiche 0045.
- Introduire une dépendance **copyleft fort** (GPL, AGPL, CERN-OHL-S) dans le
  cœur du projet.

  ⚠ **Corrigé le 2026-09-29** (fiche 0029). Cette règle avait été écrite en
  croyant CERN-OHL-S non commerciale. **Elle ne l'est pas** : vendre est
  permis. Ce qu'elle impose est la **réciprocité** — publier les sources de
  tout dérivé sous la même licence. La règle tient donc toujours, mais pour
  le bon motif : ce n'est pas la vente qui serait empêchée, c'est le fait de
  garder nos propres plans fermés.

  **Deux familles à ne jamais confondre :**

  | Famille | Exemples | Vendre ? | Garder fermé ? |
  | --- | --- | --- | --- |
  | non commerciale | CC BY-NC, CC BY-NC-SA | **non** | — |
  | copyleft, réciproque | GPL, AGPL, CERN-OHL-S | **oui** | **non** |
  | permissive | MIT, Apache-2.0, BSD, ISC | oui | oui |

  La mécanique amont de ToddlerBot est en **CC BY-NC-SA 4.0**
  (`~/upstream/toddlerbot/README.md:167`, commit `e337f3b`).

  ⚠ **Corrigé le 2026-09-30** : ce paragraphe disait « CC BY-NC », sans
  la clause SA. Or la licence appartient aux **deux** premières familles
  à la fois :

  - **NC** interdit la vente ;
  - **SA** impose la même licence à tout dérivé.

  Conséquence : **aucune géométrie amont n'entre dans une pièce YXOR**
  (fiche 0001).

  **Question juridique ouverte, sans avis** (fiche 0010 §4) : les valeurs
  numériques extraites de l'amont, celles d'origine `amont` dans l'audit,
  sont-elles couvertes par la licence ?