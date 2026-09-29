#!/usr/bin/env python3
"""L'empreinte du site — une ligne, à comparer avec le pied de page.

    .venv/bin/python scripts/empreinte.py

Le 2026-09-29, une construction a échoué quatre heures en silence et le
site a servi un plan de découpe faux avec l'air d'être à jour. La date ne
le trahissait pas : c'est celle du dernier déploiement RÉUSSI.

Cette commande dit ce que le dépôt produirait MAINTENANT. Si elle diffère
de ce qu'affiche yxor.fr — ou du plan A4 qu'on s'apprête à couper — le
site est périmé.

═══════════════════════════════════════════════════════════════════════
 POURQUOI PAS LE SHA DU COMMIT
═══════════════════════════════════════════════════════════════════════

Premier jet : `git rev-parse` en local, `SOURCE_COMMIT` en Docker. Deux
défauts constatés le jour même :

1. **Coolify ne passe pas `SOURCE_COMMIT`** — vérifié sur le site en
   ligne, qui affichait « inconnu ».
2. Et surtout : le site aurait montré le SHA en local et l'empreinte en
   Docker. **Les deux ne se seraient jamais comparées.** Un signal qu'on
   ne peut pas confronter ne signale rien.

Une seule grandeur, calculée pareil partout. Elle a en outre une
propriété que le SHA n'a pas : elle décrit ce qui a été **construit**,
pas ce qui a été **commité**. Une modification non commitée la change,
donc elle ne peut pas affirmer une fraîcheur qu'elle n'a pas.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Ce que le Dockerfile copie, et cela seul : l'empreinte décrit ce qui
# entre dans l'image, pas ce qui traîne dans le dépôt.
#
# requirements.txt et le Dockerfile y sont depuis le 2026-09-30 (audit de
# la nuit, § 8 H10) : une montée de version de build123d, ou un étage
# constructeur modifié, peut changer le site sans toucher une ligne des
# quatre répertoires. Le Dockerfile se copie lui-même dans l'image pour
# que l'empreinte se calcule PAREIL en local et en construction.
SOURCES = ("params", "parts", "scripts", "web")
FICHIERS = ("requirements.txt", "Dockerfile")


def empreinte() -> str:
    h = hashlib.sha256()
    for d in SOURCES:
        for f in sorted((REPO / d).rglob("*")):
            if not f.is_file() or "__pycache__" in f.parts:
                continue
            h.update(str(f.relative_to(REPO)).encode())
            h.update(f.read_bytes())
    for nom in FICHIERS:
        f = REPO / nom
        # Pas de saut muet : un fichier absent donnerait une empreinte
        # qu'aucune autre construction ne pourrait reproduire.
        if not f.is_file():
            raise FileNotFoundError(f"empreinte : {nom} absent de {REPO}")
        h.update(nom.encode())
        h.update(f.read_bytes())
    return h.hexdigest()[:10]


if __name__ == "__main__":
    print(empreinte())
    sys.exit(0)
