import os
import requests
import hashlib
from datetime import datetime

# Configuración de la descarga
DATA_URL = "http://medata.gov.co/sites/default/files/distribution/1-023-25-000094/incidentes_viales.csv"
# Directorio de salida para los datos descargados
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")
# Nombre del archivo de salida
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "incidentes_viales.csv")
# Archivo para guardar los metadatos de la descarga
METADATA_FILE = os.path.join(OUTPUT_DIR, "download_metadata.txt")


def download_dataset():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"[{datetime.now().isoformat()}] Iniciando descarga de incidentes viales de Medellín...")
    print(f"URL de origen: {DATA_URL}")

    sha256 = hashlib.sha256()
    total_bytes = 0

    with requests.get(DATA_URL, stream=True, timeout=60) as response:
        response.raise_for_status()
        content_length = int(response.headers.get("content-length", 0))
        print(f"Tamaño reportado por el servidor: {content_length / (1024*1024):.2f} MB")

        with open(OUTPUT_FILE, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
                if chunk:
                    f.write(chunk)
                    sha256.update(chunk)
                    total_bytes += len(chunk)
                    print(f"Descargados {total_bytes / (1024*1024):.2f} MB...", end="\r")

    checksum = sha256.hexdigest()
    print(f"\nDescarga finalizada con éxito: {total_bytes / (1024*1024):.2f} MB")
    print(f"SHA-256 Checksum: {checksum}")

    # Guardar metadatos de auditoría
    with open(METADATA_FILE, "w", encoding="utf-8") as meta:
        meta.write("=== METADATOS DE DESCARGA (AUDITORÍA PPI) ===\n")
        meta.write(f"Fecha de descarga: {datetime.now().isoformat()}\n")
        meta.write(f"Fuente oficial: MEData / Alcaldía de Medellín / datos.gov.co (ID 9wqu-juqb)\n")
        meta.write(f"URL directa: {DATA_URL}\n")
        meta.write(f"Bytes descargados: {total_bytes}\n")
        meta.write(f"Checksum SHA-256: {checksum}\n")
        meta.write(f"Ruta local: {OUTPUT_FILE}\n")

    print(f"Metadatos guardados en: {METADATA_FILE}")


if __name__ == "__main__":
    download_dataset()
