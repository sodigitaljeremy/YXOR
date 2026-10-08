#!/usr/bin/env python3
"""Télécharge durablement le validateur OpenSysML dans exports/outils/opensysml/, empreintes vérifiées.

    .venv/bin/python scripts/outil_sysml.py           # télécharge s'il manque, vérifie toujours
    .venv/bin/python scripts/outil_sysml.py --verif   # vérifie seulement (code 1 si absent ou altéré)

Créé le 2026-10-08. Outillage décidé par Jeremy (fiche 0066, b), ses mots, prompt du
2026-10-08 : « Oui, télécharge durablement OpenSysML dans exports/, hors de Git, avec son
empreinte. » Le binaire n'entre JAMAIS dans Git (règle 4 : exports/ est ignoré).

Deux empreintes, relevées le 2026-10-08 (docs/sysml-pilote.md) : celle de l'archive publiée
(v0.9.2, Open-MBEE, Apache-2.0) et celle du binaire qu'elle contient. Une archive ou un
binaire qui ne correspond pas est REFUSÉ et effacé : rien ne s'exécute sans être vérifié.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import sys
import tarfile
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DOSSIER = REPO / "exports" / "outils" / "opensysml"
BINAIRE = DOSSIER / "sysml-linux-amd64"
VERSION = "v0.9.2"
URL = f"https://github.com/Open-MBEE/OpenSysML/releases/download/{VERSION}/sysml-linux-amd64.tar.gz"
SHA_ARCHIVE = "bdaea2b948fafca57eb782895e88bf3628a12e3908ab1d909b61890390c929c1"
SHA_BINAIRE = "8c5a0a694f87be51306cc1171811d29d8213ccbe11eec9b25ea6c8496fa26bf8"


def sha256(donnees: bytes) -> str:
    return hashlib.sha256(donnees).hexdigest()


def verifie() -> bool:
    """Le binaire est là ET son empreinte est celle relevée."""
    return BINAIRE.is_file() and sha256(BINAIRE.read_bytes()) == SHA_BINAIRE


def telecharger(essais: int = 3) -> None:
    """Par curl (la poignée de main TLS de Python vers le CDN de GitHub expirait à chaque essai le 2026-10-08,
    curl passait) ; urllib seulement si curl manque."""
    import shutil
    import subprocess
    import tempfile
    archive = None
    for i in range(essais):
        try:
            if shutil.which("curl"):
                with tempfile.TemporaryDirectory() as d:
                    f = Path(d) / "a.tar.gz"
                    subprocess.run(["curl", "-sSfL", "--max-time", "600", "-o", str(f), URL], check=True)
                    archive = f.read_bytes()
            else:
                with urllib.request.urlopen(URL, timeout=120) as r:
                    archive = r.read()
            break
        except (OSError, subprocess.CalledProcessError) as e:
            print(f"  essai {i + 1}/{essais} échoué : {e}")
    if archive is None:
        raise SystemExit("  ÉCHEC du téléchargement : réseau")
    if sha256(archive) != SHA_ARCHIVE:
        raise SystemExit(f"  REFUSÉ : empreinte de l'archive {sha256(archive)[:16]}… ≠ {SHA_ARCHIVE[:16]}…")
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as t:
        membre = next((m for m in t.getmembers() if m.isfile() and Path(m.name).name == BINAIRE.name), None)
        if membre is None:
            raise SystemExit(f"  REFUSÉ : {BINAIRE.name} absent de l'archive")
        contenu = t.extractfile(membre).read()
    if sha256(contenu) != SHA_BINAIRE:
        raise SystemExit(f"  REFUSÉ : empreinte du binaire {sha256(contenu)[:16]}… ≠ {SHA_BINAIRE[:16]}…")
    DOSSIER.mkdir(parents=True, exist_ok=True)
    BINAIRE.write_bytes(contenu)
    BINAIRE.chmod(0o755)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--verif", action="store_true")
    a = ap.parse_args(argv)
    if BINAIRE.is_file() and not verifie():
        print(f"  {BINAIRE.relative_to(REPO)} : empreinte FAUSSE, effacé")
        BINAIRE.unlink()
    if not verifie():
        if a.verif:
            print(f"  OpenSysML {VERSION} : ABSENT ({BINAIRE.relative_to(REPO)})")
            return 1
        print(f"  téléchargement : {URL}")
        telecharger()
    print(f"  OpenSysML {VERSION} : {BINAIRE.relative_to(REPO)}, sha256 {SHA_BINAIRE[:16]}… vérifiée "
          f"({BINAIRE.stat().st_size / 1e6:.1f} Mo)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
