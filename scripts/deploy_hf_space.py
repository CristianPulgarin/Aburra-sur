"""
Publica el backend FastAPI en un Space de Hugging Face (SDK docker) sin usar git ni GitHub.

Copia a una carpeta temporal solo lo que el servidor necesita (código, CSV limpio, grafo y
benchmarks de la Fase 4), agrega la ficha README del Space y la sube con la API de Hugging Face.
La base SQLite se construye dentro del contenedor durante el build.

Uso (lo invoca deploy-backend.ps1):
    python scripts/deploy_hf_space.py --space aburrasegura-api [--origins https://x.web.app,...]
Requiere un token de escritura de https://huggingface.co/settings/tokens (variable HF_TOKEN o se pide al ejecutar).
"""

import argparse
import getpass
import os
import shutil
import sys
import tempfile

from huggingface_hub import HfApi

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILES = [
    "Dockerfile",
    "requirements.txt",
    "scripts/build_database.py",
    "data/processed/medellin_incidents_clean.csv",
    "data/processed/medellin_graph.json",
    "data/benchmarks/benchmark_results_fase4.json",
    "data/benchmarks/bench_1k.csv",
    "data/benchmarks/bench_10k.csv",
    "data/benchmarks/bench_50k.csv",
    "data/benchmarks/bench_100k.csv",
]

SPACE_README = """---
title: AburraSegura API
emoji: 🚦
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
short_description: Backend FastAPI del PPI AburraSegura (TdeA)
---

Backend del proyecto **AburráSegura** (PPI Análisis de Algoritmos, Tecnológico de Antioquia).
Documentación interactiva de la API en `/docs`.
"""


def stage(target: str) -> None:
    """Copia a `target` solo los archivos que necesita el contenedor."""
    shutil.copytree(
        os.path.join(BASE_DIR, "app"),
        os.path.join(target, "app"),
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    for rel in FILES:
        src = os.path.join(BASE_DIR, rel)
        with open(src, "rb") as f:
            if f.read(40).startswith(b"version https://git-lfs"):
                sys.exit(f"{rel} es un puntero de Git LFS, no el archivo real.")
        dst = os.path.join(target, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
    with open(os.path.join(target, "README.md"), "w", encoding="utf-8") as f:
        f.write(SPACE_README)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--space", default="aburrasegura-api", help="Nombre del Space (sin el usuario)")
    parser.add_argument("--origins", default="", help="ALLOWED_ORIGINS: dominios del frontend separados por coma")
    parser.add_argument("--dry-run", metavar="CARPETA", help="Solo prepara los archivos en CARPETA, sin subir nada")
    args = parser.parse_args()

    if args.dry_run:
        stage(args.dry_run)
        print(f"Archivos preparados en {args.dry_run}")
        return 0

    token = os.environ.get("HF_TOKEN") or getpass.getpass("Token de Hugging Face (permiso Write): ").strip()
    api = HfApi(token=token)
    user = api.whoami()["name"]
    repo_id = f"{user}/{args.space}"

    print(f"> Creando o actualizando el Space {repo_id}...")
    api.create_repo(repo_id, repo_type="space", space_sdk="docker", exist_ok=True)
    if args.origins:
        api.add_space_variable(repo_id, "ALLOWED_ORIGINS", args.origins)

    with tempfile.TemporaryDirectory() as tmp:
        stage(tmp)
        print("> Subiendo archivos (unos 55 MB)...")
        api.upload_folder(
            repo_id=repo_id,
            repo_type="space",
            folder_path=tmp,
            commit_message="Despliegue del backend AburráSegura",
            delete_patterns=["app/**", "scripts/**", "data/**"],
        )

    host = f"{user}-{args.space}".lower().replace("_", "-").replace(".", "-")
    print()
    print(f"Space:  https://huggingface.co/spaces/{repo_id}")
    print(f"API:    https://{host}.hf.space   (el primer build tarda 3-5 minutos)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
