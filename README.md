# AburráSegura — Urban Safety Intelligence

Plataforma para identificar puntos críticos de siniestralidad vial en Medellín y calcular rutas seguras con grafos
(Dijkstra / A*). Proyecto Pedagógico Integrador (PPI) — Análisis de Algoritmos, Tecnológico de Antioquia.

- **Backend:** FastAPI + SQLite (251.150 siniestros de MEData, 2014–2020), algoritmos implementados desde cero en `app/algorithms/`.
- **Frontend:** React + Vite + Leaflet en `frontend/`.
- **Documentación académica:** bóveda Obsidian en `vault/` y `AburráSegura.docx`.

## Ejecutar

Requisitos: Python 3.11+ y Node 20+.

**Opción A — VS Code:** `Ctrl+Shift+B` ejecuta la tarea **“AburráSegura: iniciar todo”** (backend + frontend).
Luego abre `http://localhost:5173` (o `Ctrl+Shift+P` → *Simple Browser: Show* para verlo dentro del editor).

**Opción B — PowerShell:**

```powershell
.\start.ps1
```

La primera ejecución crea `.venv`, instala `requirements.txt` y las dependencias de `frontend/`.

| Servicio | URL |
|---|---|
| Aplicación | http://localhost:5173 |
| API / Swagger | http://127.0.0.1:8000/docs |

## Base de datos

`data/processed/medellin_incidents.db` se versiona con Git LFS; si el repositorio se descarga como ZIP llega solo el puntero.
El backend la **regenera automáticamente** desde `medellin_incidents_clean.csv` al arrancar. También se puede hacer a mano:

```powershell
.venv\Scripts\python scripts\build_database.py
```

La reconstrucción normaliza problemas de codificación del CSV: “SOLO DAÑOS” venía en dos variantes corruptas
(112.250 registros que no coincidían con el filtro), “CAIDA OCUPANTE” en tres, y comunas/barrios con mojibake
(“BelÃ©n”, `Bel\xE9n`) que partían una misma comuna en varias. Agrega además `hora_num` y `dia_semana`.

## Módulos

| Pestaña | Contenido |
|---|---|
| Rutas & Mapa Seguro | Mapa de calor, puntos críticos y ruta más corta vs. más segura (Dijkstra multiobjetivo, KD-Tree para el nodo más cercano). |
| Laboratorio Algorítmico | Benchmarks O(1) → O(n²), ordenamientos y KD-Tree vs. búsqueda lineal. |
| Analítica Urbana | Filtros cruzados reales (gravedad × año × comuna), distribución por hora, día, mes y tipo de accidente, ranking de comunas y barrios, hallazgos automáticos y exportación a CSV. |
| Ficha Técnica PPI | Trazabilidad de requisitos R1–R10. |

Endpoint de analítica: `GET /api/v1/incidents/analytics?anio=2019&gravedad=CON%20HERIDOS&comuna=La%20Candelaria`.

## Pruebas

```powershell
.venv\Scripts\python -m pytest -q
```

## Despliegue (Firebase Hosting + Hugging Face Spaces)

El frontend es estático y va a **Firebase Hosting**; el backend FastAPI va a un **Space de Hugging Face**
(gratis, sin tarjeta y sin GitHub: se sube desde el PC).

1. **Backend**: crear una cuenta en huggingface.co y un token de tipo *Write* en
   https://huggingface.co/settings/tokens. Luego:
   ```powershell
   .\deploy-backend.ps1
   ```
   El script prepara solo lo necesario (código, CSV limpio, grafo y benchmarks), lo sube y muestra la URL de la API
   (`https://<usuario>-aburrasegura-api.hf.space`). El primer build tarda unos minutos; la base SQLite se genera dentro del contenedor.
2. **Frontend**:
   ```powershell
   .\deploy-frontend.ps1 -ProjectId <id-de-firebase> -ApiUrl https://<usuario>-aburrasegura-api.hf.space
   ```
3. **CORS**: restringir la API al dominio de Firebase volviendo a ejecutar `.\deploy-backend.ps1 -ProjectId <id-de-firebase>`.

El Space se duerme tras 48 horas sin visitas; la primera visita después tarda alrededor de un minuto
(la barra superior muestra “Despertando servidor...”). Para revisar el contenido sin subir nada:
`python scripts/deploy_hf_space.py --dry-run carpeta_destino`.

## Configuración

El frontend usa rutas relativas que Vite reenvía al backend (`frontend/vite.config.js`). Para apuntar a otro servidor,
crea `frontend/.env` con `VITE_API_URL=http://host:puerto`.
