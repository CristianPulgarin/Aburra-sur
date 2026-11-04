"""
Regenera data/processed/medellin_incidents.db desde el CSV limpio.
La lógica vive en app/services/db_builder.py (también usada por el backend al arrancar).

Uso:
    python scripts/build_database.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.db_builder import build  # noqa: E402

if __name__ == "__main__":
    sys.exit(build())
