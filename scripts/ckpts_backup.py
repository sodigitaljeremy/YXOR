#!/usr/bin/env python3
"""Manifeste et vérification des poids ToddlerBot — sauvegarde hors Git.

Usage :
    .venv/bin/python scripts/ckpts_backup.py manifest   # (re)génère le manifeste
    .venv/bin/python scripts/ckpts_backup.py verify     # vérifie les empreintes
    .venv/bin/python scripts/ckpts_backup.py archive    # crée l'archive à copier

Se lance avec le venv DU PROJET. Ne lit que des fichiers, n'importe
aucun code amont.

═══════════════════════════════════════════════════════════════════════
 POURQUOI CE SCRIPT EXISTE
═══════════════════════════════════════════════════════════════════════

Les poids (fiche 0003) pèsent 29,5 Mo, ne sont couverts par aucun
versionnement, et viennent d'un Google Drive tiers. S'il disparaît, ils
sont irrécupérables : ni l'amont ni YXOR n'en gardent copie publique.

La règle 4 interdit le binaire dans Git. Le partage est donc :

    DANS Git   — ce manifeste : noms, identifiants Drive, empreintes
                 SHA-256, tailles. Du texte, vérifiable, diffable.
    HORS Git   — les archives elles-mêmes, sur deux destinations
                 privées distinctes.

Pas de Release GitHub : la fiche 0003 note que **la licence des poids
n'est pas explicitée par l'amont**. Les republier, fût-ce en pièce
jointe de release, serait imprudent tant que ce point n'est pas éclairci.

Le manifeste sans les archives ne restaure rien — il permet seulement de
DÉTECTER une altération. Les deux moitiés sont nécessaires.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import os
import sys
import tarfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "params" / "ckpts.manifest.yaml"
DEFAULT_ROOT = Path.home() / "upstream" / "toddlerbot"
DRIVE_FOLDER = "1d0UGRc3-3wxMcqrZSlqRXkSnwFSC8Xk-"

# Identifiants Drive relevés le 2026-09-20 (fiche 0003). Un identifiant
# Drive survit à un remplacement de contenu : seule l'empreinte prouve.
DRIVE_IDS = {
    "toddlerbot_2xc_climb_down_box_rsl_20250914_014343.zip": "1D8SBhaG5GOy1J1IENR_T7kVBuPCyBTWA",
    "toddlerbot_2xc_climb_up_box_rsl_20250907_201202.zip":   "1DNDVm9zELWeW0Lf3QmF6rShZZ_yUfeem",
    "toddlerbot_2xc_climb_wall_rsl_20250913_174540.zip":     "1TNBXaYO70WemF98_94iU_ZyiccG6OJ9o",
    "toddlerbot_2xc_crawl_down_stairs_rsl_20260215_094639.zip": "1cAfq3E4NHh0V1jDWe8t-5E4_0ZB79-Y7",
    "toddlerbot_2xc_crawl_full_rsl_20260214_145000.zip":     "1mr1HZdIUexfofNiPwiNYactJ4x76l60R",
    "toddlerbot_2xc_crawl_only_rsl_20260214_145735.zip":     "10RAwiPWvcWFSHaUgGxLdA19rM8TP7QhW",
    "toddlerbot_2xc_crawl_rotate_rsl_20251109_195839.zip":   "11ufCkJMcHaRxNit6ghkftGBtEs34STUb",
    "toddlerbot_2xc_crawl_up_stairs_rsl_20260217_211836.zip":"1QOY2yVLeM_VkM8tmte9WbflFOlOicY6g",
    "toddlerbot_2xc_get_up_rsl_20260214_145222.zip":         "1hrObDBteSH3lA4qFIuA_IVw6pMZXUdRU",
    "toddlerbot_2xc_walk_rsl_20251226_114612.zip":           "1Rcfhsw1fbqpW7CkMiqRhF2uGixuJxDtn",
}


def ckpts_dir() -> Path:
    root = Path(os.environ.get("TODDLERBOT_ROOT", DEFAULT_ROOT)).expanduser()
    return root / "ckpts"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def scan() -> list[dict]:
    d = ckpts_dir()
    if not d.is_dir():
        sys.exit(f"dossier introuvable : {d}\n  définir TODDLERBOT_ROOT si besoin")
    return [dict(nom=p.name, taille=p.stat().st_size, sha256=sha256(p),
                 drive_id=DRIVE_IDS.get(p.name))
            for p in sorted(d.glob("*.zip"))]


def read_manifest() -> dict[str, dict]:
    if not MANIFEST.exists():
        return {}
    out, cur = {}, None
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        t = line.strip()
        if t.startswith("- nom:"):
            cur = t.split(":", 1)[1].strip(); out[cur] = {}
        elif cur and ":" in t and not t.startswith("#"):
            k, v = t.split(":", 1); out[cur][k.strip()] = v.strip()
    return out


def cmd_manifest(_):
    rows = scan()
    L, A = [], None; A = L.append
    A("# Manifeste des poids ToddlerBot — SAUVEGARDE HORS GIT")
    A("#")
    A("# Généré par scripts/ckpts_backup.py. Voir decisions/archive/0003 et 0008.")
    A("#")
    A("# Ce fichier ne contient AUCUN binaire (règle 4) : il ne restaure rien.")
    A("# Il permet de DÉTECTER qu'une archive a changé ou a été corrompue.")
    A("# Les archives vivent sur deux destinations privées, hors du dépôt.")
    A("#")
    A("# Vérifier :  .venv/bin/python scripts/ckpts_backup.py verify")
    A("#")
    A(f"# Dossier Drive d'origine : {DRIVE_FOLDER}")
    A("# ⚠ Un identifiant Drive survit au remplacement de son contenu.")
    A("#   Seule l'empreinte SHA-256 prouve qu'il s'agit des mêmes poids.")
    A(f"#")
    # Pas de date de relevé : ce fichier est haché par l'empreinte du site
    # (lot A.9). Git connaît la date.
    A(f"# {len(rows)} archives, {sum(r['taille'] for r in rows)/1e6:.1f} Mo au total.")
    A("")
    A("archives:")
    for r in rows:
        A(f"  - nom: {r['nom']}")
        A(f"    taille: {r['taille']}")
        A(f"    sha256: {r['sha256']}")
        A(f"    drive_id: {r['drive_id'] or 'null'}")
    MANIFEST.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"écrit : {MANIFEST.relative_to(REPO)}")
    print(f"  {len(rows)} archives, {sum(r['taille'] for r in rows)/1e6:.1f} Mo")
    return 0


def cmd_verify(_):
    ref = read_manifest()
    if not ref:
        sys.exit(f"manifeste absent : {MANIFEST}\n  lancer d'abord la commande `manifest`")
    rows = {r["nom"]: r for r in scan()}
    ok = manquantes = alterees = nouvelles = 0
    for nom, r in sorted(ref.items()):
        if nom not in rows:
            print(f"  MANQUANTE  {nom}"); manquantes += 1
        elif rows[nom]["sha256"] != r.get("sha256"):
            print(f"  ALTÉRÉE    {nom}")
            print(f"             manifeste {r.get('sha256','?')[:16]}…")
            print(f"             disque    {rows[nom]['sha256'][:16]}…")
            alterees += 1
        else:
            ok += 1
    for nom in sorted(set(rows) - set(ref)):
        print(f"  NOUVELLE   {nom} (absente du manifeste)"); nouvelles += 1
    print(f"\n{ok} conformes, {alterees} altérées, {manquantes} manquantes, "
          f"{nouvelles} nouvelles")
    if alterees:
        print("\n⚠ Une empreinte qui diverge signifie que l'amont a republié,")
        print("  ou que l'archive est corrompue. Les mesures qui s'y rapportent")
        print("  sont invalidées : voir decisions/archive/0003.")
    return 1 if (alterees or manquantes) else 0


def cmd_archive(args):
    rows = scan()
    stamp = datetime.date.today().isoformat()
    out = Path(args.out).expanduser() / f"yxor-ckpts-{stamp}.tar.gz"
    out.parent.mkdir(parents=True, exist_ok=True)
    d = ckpts_dir()
    with tarfile.open(out, "w:gz") as tar:
        for r in rows:
            tar.add(d / r["nom"], arcname=r["nom"])
        tar.add(MANIFEST, arcname=MANIFEST.name)      # le manifeste voyage avec
    print(f"archive : {out}  ({out.stat().st_size/1e6:.1f} Mo)")
    print(f"  {len(rows)} archives + le manifeste")
    print(f"  sha256 de l'archive : {sha256(out)}")
    print()
    print("  Il reste à la copier sur une SECONDE destination privée.")
    print("  Jamais de Release GitHub publique : licence des poids non")
    print("  explicitée par l'amont (fiche 0003).")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("manifest", help="(re)génère le manifeste versionné")
    sub.add_parser("verify", help="vérifie les archives contre le manifeste")
    a = sub.add_parser("archive", help="crée l'archive à copier hors Git")
    a.add_argument("--out", default="~/backup/yxor", help="dossier de sortie")
    args = p.parse_args(argv)
    return {"manifest": cmd_manifest, "verify": cmd_verify, "archive": cmd_archive}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
