#!/usr/bin/env python3
"""Rien de binaire dans Git — la règle 4, vérifiée sur TOUT le dépôt.

    .venv/bin/python scripts/controle_depot.py

═══════════════════════════════════════════════════════════════════════
 POURQUOI CE FICHIER EXISTE
═══════════════════════════════════════════════════════════════════════

Le 2026-09-28, treize fichiers sont entrés dans Git — dont un STEP, un
STL, un DXF et un PDF — le jour même où la fiche 0018 l'interdisait. Rien
ne l'a signalé.

Le lendemain, `site/` a été ajouté à `.gitignore`. Cela a bouché LE TROU,
pas LA CLASSE DE TROU : un `.step` déposé dans `parts/` serait entré
exactement pareil.

Ce contrôle ne regarde donc aucun répertoire en particulier. Il regarde
**tout ce que Git suit**, et par deux moyens indépendants :

  1. **l'extension** — un `.step` est binaire même s'il est vide ;
  2. **le contenu** — un octet NUL dans les 8 000 premiers, qui est
     l'heuristique de Git lui-même. Elle attrape ce que l'extension rate,
     par exemple un fichier sans extension ou nommé `.txt` à tort.

Aucun des deux ne suffit seul, et c'est voulu : une liste d'extensions
ne prévoit jamais le format suivant, et le reniflement de contenu laisse
passer un binaire ASCII comme un STEP.
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SONDE = 8000                      # non-cote: taille de l'échantillon reniflé

# Extensions tenues pour binaires. La liste part des formats que le projet
# produit (règle 4 les nomme : STEP, STL, DXF, URDF, rendus) et s'étend
# aux familles voisines. Le DXF est du TEXTE, mais la règle 4 l'interdit
# nommément : il est engendré, il n'a rien à faire dans Git.
EXTENSIONS = {
    # géométrie engendrée — nommées par la règle 4
    ".step", ".stp", ".stl", ".dxf", ".dwg", ".iges", ".igs", ".3mf",
    ".obj", ".ply", ".gltf", ".glb", ".f3d", ".scad_bak",
    # images et rendus
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff", ".webp",
    ".ico", ".psd", ".mp4", ".mov", ".webm", ".avi",
    # documents compilés
    ".pdf", ".docx", ".xlsx", ".pptx", ".odt", ".ods",
    # archives et exécutables
    ".zip", ".gz", ".bz2", ".xz", ".7z", ".rar", ".tar",
    ".so", ".dylib", ".dll", ".exe", ".bin", ".o", ".a",
    # poids de modèles — fiche 0008
    ".pt", ".pth", ".ckpt", ".onnx", ".safetensors", ".npz", ".npy",
    ".h5", ".pkl", ".pickle", ".joblib",
    # polices
    ".ttf", ".otf", ".woff", ".woff2", ".eot",
}

# Exceptions ASSUMÉES, avec leur motif. Une exception sans motif est un
# oubli déguisé : le champ n'est pas facultatif.
EXCEPTIONS: dict[str, str] = {
    # exemple de la forme attendue, aucune exception aujourd'hui :
    # "docs/schema.png": "capture d'écran d'un document amont, non régénérable",
}


def suivis() -> list[str]:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=REPO,
                         capture_output=True, text=True, check=True)
    return [f for f in out.stdout.split("\0") if f]


def binaire_par_contenu(p: Path) -> bool:
    """Heuristique de Git : un octet NUL dans l'échantillon de tête."""
    try:
        return b"\0" in p.open("rb").read(SONDE)
    except OSError:
        return False


def controler() -> list[tuple[str, str]]:
    fautes = []
    for rel in suivis():
        if rel in EXCEPTIONS:
            continue
        p = REPO / rel
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        if ext in EXTENSIONS:
            fautes.append((rel, f"extension {ext} tenue pour binaire"))
        elif binaire_par_contenu(p):
            fautes.append((rel, "octet NUL dans les premiers "
                                f"{SONDE} octets (heuristique de Git)"))
    return fautes


CHAMPS_FOURNISSEUR = ("source", "reference", "date", "empreinte",
                      "conditions", "redistribuable")


def controler_fournisseurs(suivis_set: set[str]) -> list[str]:
    """Fiche de provenance complète, et rien d'interdit dans Git (0030).

    Un champ manquant n'est pas une négligence de forme : sans empreinte
    on ne sait pas si le fournisseur a changé son modèle, et sans
    conditions on ne sait pas si le fichier avait le droit d'être là.
    """
    f = REPO / "params" / "fournisseurs.yaml"
    if not f.exists():
        return []
    import yaml
    doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
    fautes = []
    for cle, d in (doc.get("fichiers") or {}).items():
        d = d or {}
        manquants = [c for c in CHAMPS_FOURNISSEUR if c not in d]
        if manquants:
            fautes.append(f"fournisseurs.yaml : « {cle} » sans "
                          + ", ".join(manquants))
        chemin = d.get("chemin")
        if d.get("redistribuable") is False and chemin in suivis_set:
            fautes.append(f"fournisseurs.yaml : « {cle} » est déclaré NON "
                          f"redistribuable mais {chemin} est suivi par Git")
        if d.get("redistribuable") is True and chemin and chemin not in suivis_set:
            fautes.append(f"fournisseurs.yaml : « {cle} » annonce {chemin}, "
                          "qui n'est pas suivi par Git")
    return fautes


def main() -> int:
    if not (REPO / ".git").exists():
        # Dit, jamais tu : un contrôle qui se tait en passant est pire
        # qu'un contrôle absent, parce qu'on le croit passé.
        print("   contrôle du dépôt IGNORÉ : pas de dépôt git ici "
              "(construction Docker)")
        return 0
    liste = suivis()
    if not liste:
        # « 0 fichiers suivis, aucun binaire » est vrai et ne veut rien
        # dire. Un contrôle dont l'entrée est vide doit le DIRE, pas
        # rendre un vert.
        print("\n✗ aucun fichier suivi par Git : le contrôle de la règle 4")
        print("  n'a rien inspecté. Vérifier qu'on est bien dans le dépôt.")
        return 1
    fautes = controler()
    mauvaises_fiches = controler_fournisseurs(set(liste))
    n = len(liste)
    if mauvaises_fiches:
        print("\n✗ FICHES DE PROVENANCE INCOMPLÈTES (fiche 0030) :")
        for m in mauvaises_fiches:
            print(f"   {m}")
        return 1
    if not fautes:
        print(f"   règle 4 : {n} fichiers suivis, aucun binaire, "
              "provenances conformes")
        if EXCEPTIONS:
            print(f"   ({len(EXCEPTIONS)} exception(s) assumée(s))")
        return 0
    print(f"\n✗ RÈGLE 4 VIOLÉE — {len(fautes)} fichier(s) binaire(s) suivis "
          f"par Git :")
    for rel, motif in fautes:
        print(f"   {rel}\n      {motif}")
    print("\n  Ces fichiers se régénèrent : ils vont dans exports/ ou site/,")
    print("  qui sont ignorés. Pour en assumer un, l'inscrire dans")
    print("  EXCEPTIONS de ce fichier AVEC SON MOTIF.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
