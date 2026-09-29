#!/usr/bin/env python3
"""L'empreinte du site — une ligne, à comparer avec le pied de page.

    .venv/bin/python scripts/empreinte.py

Le 2026-09-29, une construction a échoué quatre heures en silence et le
site a servi un plan de découpe faux avec l'air d'être à jour. La date ne
le trahissait pas : c'est celle du dernier déploiement RÉUSSI.

Cette commande dit ce que le dépôt produirait MAINTENANT. Si elle diffère
de ce qu'affiche yxor.fr, le site est périmé.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pages  # noqa: E402

if __name__ == "__main__":
    print(pages.commit())
