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

# ── DÉPENDANCES SYSTÈME — la neuvième défaillance silencieuse ──────────
#
#  python:3.14-slim n'embarque aucune bibliothèque graphique. OCCT s'y
#  lie POURTANT, même pour du calcul sans affichage : le module Python
#  OCP charge l'ensemble des bibliothèques OCCT, dont libTKOpenGl et
#  libTKService, au seul import.
#
#  D'où, à l'étage constructeur :
#      ImportError: libGL.so.1: cannot open shared object file
#
#  Le jeu minimal a été établi en LISANT les entrées NEEDED des ELF de
#  cadquery-ocp-novtk, pas en essayant des paquets au hasard :
#
#      libGL.so.1     <- libTKOpenGl          -> libgl1
#      libX11.so.6    <- libTKOpenGl, libTKService -> libx11-6
#      libexpat.so.1  <- libTKService, libfontconfig -> libexpat1
#
#  Trois paquets, et rien de plus. Pas de mesa-utils, pas de xvfb, pas
#  d'environnement graphique : rien de tout cela n'est nécessaire pour
#  que l'éditeur de liens trouve ses symboles.
RUN apt-get update \
 && apt-get install -y --no-install-recommends libgl1 libx11-6 libexpat1 \
 && rm -rf /var/lib/apt/lists/*

# L'environnement de l'image n'est pas celui du poste de travail : on
# fixe l'encodage plutôt que d'en hériter. Le projet écrit du français.
ENV PYTHONIOENCODING=utf-8 \
    LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1

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

# ── L'EMPREINTE DU COMMIT, pour qu'un site périmé se reconnaisse ──────
#
#  L'image n'a pas de dépôt git : `git rev-parse` y est impossible. Le
#  SHA doit donc ENTRER par l'extérieur. Coolify fournit `SOURCE_COMMIT`
#  en argument de construction.
#
#  Valeur par défaut « inconnu » : si l'argument n'est pas passé, les
#  pages le DISENT au lieu d'afficher un SHA faux. Le 2026-09-29, un
#  déploiement a échoué quatre heures sans que rien ne le signale, et le
#  site périmé servait un plan de découpe faux avec l'air d'être à jour.
ARG SOURCE_COMMIT=inconnu
ENV YXOR_COMMIT=$SOURCE_COMMIT

# La commande unique — la même que celle lancée en local.
RUN python scripts/regenerer.py

# ─────────────────────────────── étage 2 : service ────────────────────
FROM nginx:1.29-alpine AS service
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=constructeur /src/site /usr/share/nginx/html
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD wget -qO- http://127.0.0.1/ >/dev/null || exit 1
