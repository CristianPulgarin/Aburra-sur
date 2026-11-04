---
tipo: decision
id: ADR-002
titulo: Arquitectura del Sistema (FastAPI Backend + React/Vite Frontend)
estado: aceptado
fecha: 2026-09-29
responsables:
  - backend-dev
  - frontend-dev
  - orquestador
requisito_asociado:
  - R7
  - R8
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/decision, ppi/tdea, proyecto/aburrasegura]
---

# ADR-002: Arquitectura del Sistema (FastAPI Backend + React/Vite Frontend)

> [!abstract] En pocas palabras
> Selección del stack tecnológico desacoplado: backend asíncrono en FastAPI (Python) y frontend reactivo en React + Vite con Leaflet.


## Estado
**Aceptado**.

## Contexto
El sistema requiere desacoplar el motor computacional de algoritmos (escrito en Python de alto rendimiento con tipos estrictos) de la interfaz de usuario interactiva (mapa geoespacial y laboratorio de benchmarks en tiempo real).

## Decisión
1. **Backend:** **Python 3.14 + FastAPI + Pydantic v2**.
   - Justificación: Python permite la implementación limpia de estructuras de datos y algoritmos en código puro, mediciones de precisión con `time.perf_counter` y `tracemalloc`, y FastAPI genera contratos OpenAPI/Swagger automáticos y asíncronos.
2. **Frontend:** **React 18 / 19 + Vite + Tailwind CSS + Leaflet (react-leaflet) + Recharts**.
   - Justificación: Renderizado ultra rápido con Vite, mapas livianos e interactivos con Leaflet para capas de siniestros y rutas, y gráficos interactivos con Recharts para contrastar curvas teóricas vs. empíricas en el Laboratorio de Algoritmos.
3. **Comunicación:** API RESTful bajo formato JSON con especificación OpenAPI 3.1 precongelada.

---

## 🔗 Relacionado
- [[00 - Inicio|Inicio]]
- [[ADR-001-Enfoque-Siniestros-y-Grafo-OSM|ADR-001]]
- [[Diseno-Backend-API]]
- [[Diseno-Frontend-UI]]
