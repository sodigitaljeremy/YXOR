# ═══════════════════════════════════════════════════════════════════════
#  YXOR — site statique engendré depuis le dépôt (fiche 0018)
# ═══════════════════════════════════════════════════════════════════════
#
#  Deux étages, et c'est la clé de l'affaire :
#
#    1. CONSTRUCTEUR — installe build123d et son noyau OCCT (~750 Mo),
#       exécute chaque pièce, produit le site. Cet étage est JETÉ.
#    2. SERVICE      — nginx et le seul dossier site/. Ni Python, ni
#       build123d, ni code source dans l'image finale.
#
#  La règle 4 est respectée à la lettre : rien de binaire n'entre dans
#  Git, et tout se régénère. Les artefacts n'existent qu'ici.
#
#  ⚠ L'étage constructeur exige de la mémoire et du disque. Mesuré :
#    747 Mo installés, dominés par cadquery-ocp-novtk (395 Mo). Compter
#    2 Go de disque libre et 2 Go de mémoire pour construire sereinement.
#    Vérifier AVANT de déployer — voir le journal du 2026-09-28.

# ─────────────────────────────── étage 1 : constructeur ───────────────
FROM python:3.14-slim AS constructeur
WORKDIR /src

# Les dépendances d'abord : cette couche est mise en cache tant que
# requirements.txt ne change pas. C'est ce qui rend les redéploiements
# rapides malgré les 750 Mo.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Puis seulement le dépôt : une modification de pièce ne réinstalle rien.
COPY params/ params/
COPY parts/  parts/
COPY scripts/ scripts/
COPY web/    web/

# La commande unique — la même que celle lancée en local.
RUN python scripts/regenerer.py

# ─────────────────────────────── étage 2 : service ────────────────────
FROM nginx:1.29-alpine AS service
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=constructeur /src/site /usr/share/nginx/html
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD wget -qO- http://127.0.0.1/ >/dev/null || exit 1
