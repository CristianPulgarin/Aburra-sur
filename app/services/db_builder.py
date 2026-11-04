"""
Reconstrucción de la base SQLite (medellin_incidents.db) desde el CSV limpio versionado.

Motivo: el archivo .db se distribuye por Git LFS y al descargar el repositorio como ZIP
solo llega el puntero de texto. Este script regenera la base sin depender del CSV crudo
y, además, repara problemas de codificación detectados en el CSV limpio:
  - Gravedad "SOLO DAÑOS" duplicada en dos variantes corruptas ("SOLO DAñOS", "SOLO DA\\XF1OS").
  - Clase "CAIDA OCUPANTE" fragmentada en tres variantes.
  - Barrios y comunas con mojibake UTF-8/Latin-1 (p. ej. "BelÃ©n" -> "Belén").

Uso:
    python scripts/build_database.py

El backend también lo invoca automáticamente al arrancar si la base falta o es un puntero LFS.
"""

import csv
import os
import re
import sqlite3
import sys
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV_PATH = os.path.join(BASE_DIR, "data", "processed", "medellin_incidents_clean.csv")
DB_PATH = os.path.join(BASE_DIR, "data", "processed", "medellin_incidents.db")

SEVERITY_WEIGHTS = {"SOLO DAÑOS": 1.0, "CON HERIDOS": 3.0, "CON MUERTOS": 10.0}
WEEKDAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


def fix_text(value: str) -> str:
    """Repara mojibake típico (UTF-8 leído como Latin-1) y escapes literales."""
    if not value:
        return ""
    s = re.sub(r"\\[xX]([0-9A-Fa-f]{2})", lambda m: chr(int(m.group(1), 16)), value)
    if "Ã" in s or "Â" in s:
        for enc in ("latin1", "cp1252"):
            try:
                s = s.encode(enc).decode("utf-8")
                break
            except (UnicodeEncodeError, UnicodeDecodeError):
                continue
    return s.replace("�", "").replace("\xad", "").strip()


UNKNOWN_PLACES = {"", "0", "in", "au", "sn", "sin inf", "no georef", "desconocida", "desconocido"}


def normalize_place(value: str) -> str:
    p = fix_text(value)
    return "Sin información" if p.lower() in UNKNOWN_PLACES else p


def normalize_severity(value: str) -> str:
    g = fix_text(value).upper()
    if "MUERT" in g:
        return "CON MUERTOS"
    if "HERID" in g:
        return "CON HERIDOS"
    return "SOLO DAÑOS"


def normalize_class(value: str) -> str:
    c = fix_text(value).upper()
    if "OCUPANTE" in c:
        return "CAIDA OCUPANTE"
    return c or "OTRO"


def is_lfs_pointer(path: str) -> bool:
    if not os.path.exists(path) or os.path.getsize(path) > 1024:
        return False
    with open(path, "rb") as f:
        return f.read(40).startswith(b"version https://git-lfs")


def needs_rebuild() -> bool:
    """True si la base no existe, es un puntero LFS o no tiene la tabla de incidentes."""
    if not os.path.exists(DB_PATH) or is_lfs_pointer(DB_PATH):
        return True
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("SELECT dia_semana FROM incidents LIMIT 1")
        conn.close()
        return False
    except sqlite3.DatabaseError:
        return True


def build() -> int:
    if not os.path.exists(CSV_PATH):
        print(f"No se encontró el CSV limpio en {CSV_PATH}", file=sys.stderr)
        return 1

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    rows = []
    with open(CSV_PATH, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            gravedad = normalize_severity(r["gravedad"])
            try:
                d = date.fromisoformat(r["fecha"])
                dia = d.weekday()
            except ValueError:
                dia = None
            hora = r.get("hora") or "12:00:00"
            rows.append((
                r["radicado"],
                r["fecha"],
                int(r["anio"]),
                int(r["mes"]),
                hora,
                int(hora[:2]) if hora[:2].isdigit() else None,
                dia,
                normalize_class(r["clase_accidente"]),
                gravedad,
                SEVERITY_WEIGHTS[gravedad],
                int(float(r["comuna_codigo"] or 0)),
                normalize_place(r["comuna_nombre"]),
                normalize_place(r["barrio"]),
                fix_text(r["diseno"]),
                float(r["latitud"]),
                float(r["longitud"]),
            ))

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE incidents (
            radicado TEXT, fecha TEXT, anio INTEGER, mes INTEGER, hora TEXT,
            hora_num INTEGER, dia_semana INTEGER, clase_accidente TEXT, gravedad TEXT,
            factor_riesgo REAL, comuna_codigo INTEGER, comuna_nombre TEXT, barrio TEXT,
            diseno TEXT, latitud REAL, longitud REAL
        )
        """
    )
    conn.executemany(f"INSERT INTO incidents VALUES ({','.join('?' * 16)})", rows)
    for col in ("anio", "comuna_codigo", "comuna_nombre", "gravedad", "radicado"):
        conn.execute(f"CREATE INDEX idx_incidents_{col} ON incidents ({col})")
    conn.execute("CREATE INDEX idx_incidents_coords ON incidents (latitud, longitud)")
    conn.commit()
    conn.close()
    print(f"Base reconstruida: {len(rows):,} registros -> {DB_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(build())
