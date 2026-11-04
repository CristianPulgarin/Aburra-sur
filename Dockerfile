# Imagen del backend FastAPI para Hugging Face Spaces (SDK docker, puerto 7860).
FROM python:3.11-slim

# Spaces ejecuta el contenedor con el usuario de UID 1000
RUN useradd -m -u 1000 user
WORKDIR /home/user/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=user . .
USER user

# La base SQLite se genera aquí desde el CSV limpio (no se sube el .db)
RUN python scripts/build_database.py

ENV PORT=7860
EXPOSE 7860
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
