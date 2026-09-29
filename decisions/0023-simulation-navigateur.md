# 0023 — Simuler dans le navigateur, sans rien enregistrer

Statut : **acceptée** le 2026-09-29, à la demande de Jeremy, qui en a
fixé les contraintes. Appliquée le jour même.

## La demande

Pouvoir bouger `H`, les ratios et l'épaisseur sur la page pièce, et voir
les cotes et le schéma se recalculer en direct. Sans dépendance, sans
CDN, tout en JavaScript dans la page.

Avec une contrainte posée en majuscules : **CALCULER N'EST PAS STOCKER.**

## Ce qui est décidé

**Rien n'est persisté.** Ni serveur — il n'y en a pas, le site est
statique (fiche 0018) — ni `localStorage`, ni cookie, ni URL. Recharger
la page rend les valeurs du dépôt. Le dépôt reste la seule source de
vérité, et ce n'est pas le lieu du calcul qui en décide.

**Le bandeau ne s'allume que lorsqu'il a quelque chose à dire.** Tant
qu'aucun curseur n'a bougé, il indique simplement « valeurs du dépôt ».
Dès qu'une valeur s'en écarte, il devient rouge et dit que rien n'est
enregistré. Un avertissement permanent finit par ne plus se lire.

**Le chemin pour figer est donné, jamais emprunté.** Quand une valeur est
modifiée, la page affiche le fichier et la clé à changer, l'ancienne et
la nouvelle valeur, puis la commande de régénération. Elle ne propose
aucun bouton qui le ferait : ce serait écrire dans le dépôt depuis le
navigateur, ce que la fiche 0018 exclut.

## Le vrai problème : une SECONDE implémentation

Le navigateur ne peut pas exécuter build123d. Recalculer la forme dans
la page impose donc de l'écrire **une deuxième fois**, en JavaScript.

Deux implémentations de la même chose divergent. Toujours. Et celle-ci
divergerait de la pire manière : le dessin resterait plausible, seulement
faux de deux dixièmes de millimètre — c'est-à-dire exactement assez pour
couper une pièce fausse.

Le projet ne peut pas accepter cela en l'état. D'où **deux gardes, à deux
moments différents**.

### Garde 1 — à la régénération, en Python

`scripts/profil.py` calcule la même forme analytiquement, sans noyau CAO.
La pièce confronte ce contour à celui de build123d **à chaque
régénération**, dans les deux sens, et **refuse de se produire** si
l'écart dépasse 0,05 mm ou si une cote diverge.

Mesuré : la forme analytique colle au noyau CAO à **0,0022 mm**. Une
erreur de 0,4 % introduite volontairement sur un congé est refusée.

### Garde 2 — au chargement, dans le navigateur

Le JavaScript est un portage de `profil.py`. Rien ne garantit qu'un
portage soit fidèle, et **il n'existe sur cette machine ni navigateur ni
moteur JavaScript pour l'exécuter** : le code livré n'a jamais tourné
avant d'arriver chez vous.

Donc la pièce dépose dans la page une **référence calculée en Python** —
ses cotes, et son contour échantillonné à l'identique. Au chargement, le
script recalcule et compare **point à point**. S'il ne retrouve pas la
référence, il **se désactive** et affiche pourquoi, en rouge.

La conséquence est nette : vous verrez soit une simulation juste, soit un
bandeau « SIMULATION DÉSACTIVÉE ». Jamais une simulation fausse.

## Ce que cette fiche n'autorise pas

- **Aucune écriture**, sous aucune forme, depuis la page.
- **Aucune extension à la 3D** : le visualiseur STL affiche le fichier du
  dépôt et n'est pas recalculé. Un STL simulé serait téléchargeable, donc
  coupable — et sans passer par le garde-fou de la régénération.
- **Aucun export** depuis la simulation. Ni DXF, ni PDF, ni STEP. Le seul
  chemin vers un fichier reste : modifier le dépôt, régénérer.

Ces trois interdits ont la même raison. Un fichier sorti du navigateur
n'aurait traversé ni l'audit d'origine, ni le contrôle de contour, ni le
verdict dessinable/coupable. Il aurait l'air d'un fichier du projet sans
en être un.
