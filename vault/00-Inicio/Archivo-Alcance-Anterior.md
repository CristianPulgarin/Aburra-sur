---
titulo: "Archivo del Alcance Anterior y Auditoría de Integridad"
tipo: resumen
tipo: archivo_historico
proyecto: PPI - Analisis de Algoritmos
estado: archivado
periodo: 2026-09-24 a 2026-09-30
fecha: 2026-10-08
autores:
  - Jarrison Quintero Castillo
  - Sebastián Gómez Cardona
  - Cristian David Pulgarín Vélez
tags:
  - historico
  - alcance-anterior
  - auditoria
  - conciliacion
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/resumen, ppi/tdea, proyecto/aburrasegura]
---

# Archivo del Alcance Anterior y Auditoría de Integridad Técnica

> [!abstract] En pocas palabras
> Memoria técnica y registro de auditoría del prototipo inicial de amplio espectro desarrollado en fases previas (algoritmos de ordenamiento, particiones sintéticas y exploración de modelos).


> [!WARNING] Contexto de la Transición de Alcance
> Durante la semana del 24 al 30 de septiembre de 2026, el equipo desarrolló un prototipo extenso que abarcaba cuatro familias algorítmicas simultáneas. El 05–06 de octubre de 2026, mediante el [[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad]], el alcance se focalizó en **AburráSegura: Puntos Críticos + Dijkstra Multiobjetivo + Laboratorio de Jerarquía Asintótica**. Esta nota documenta la auditoría de integridad técnica que permitió sanear y sincronizar el proyecto al 100%.

---

## 1. Inventario de Componentes y Estado de Reutilización

| Componente Construido | Ubicación en el Repositorio | Estado en el Alcance Vigente (v2.1) |
| :--- | :--- | :--- |
| **Pipeline de Datos MEData** | `data/processed/medellin_incidents.db`, `scripts/clean_and_preprocess.py` | ✅ **Reutilizado y Certificado:** 251.150 siniestros limpios en SQLite indexado. Base del Objetivo 1 ([[Pipeline-Limpieza]]). |
| **Particiones de Prueba (1K a 1M)** | `data/benchmarks/bench_*.csv` | ✅ **Reutilizado y Certificado:** Inmutables para experimentación ([[Protocolo-Experimental]]). |
| **Dijkstra con Min-Heap y Coste Multiobjetivo** | `app/algorithms/graph_routing.py` | ✅ **Núcleo Central del Proyecto:** Algoritmo principal del Objetivo 2 ([[Grafos-Dijkstra-AStar]]). |
| **Laboratorio de Complejidad en Tiempo Real** | `app/algorithms/complexity_benchmarks.py` | ✅ **Módulo Vigente:** Diseñado para responder a la solicitud docente de medir $\mathcal{O}(1)$ a $\mathcal{O}(n^2)$ ([[Laboratorio-Jerarquia-Asintotica]]). |
| **Grafo Vial Arterial (32 nodos, 84 aristas)** | `data/processed/medellin_graph.json` | ✅ **Reutilizado y Operativo:** Modelado topológico con sentidos obligatorios de circulación. |
| **Suite Automatizada de Pruebas** | `tests/` (7 módulos de test) | ✅ **Certificado:** Ampliada de 35 a **44 pruebas en Pytest (100% PASS en 8.31s)** ([[Plan-Pruebas-QA]]). |
| **Backend FastAPI y Frontend React SPA** | `app/`, `frontend/` | ✅ **Totalmente Sincronizado:** Endpoints OpenAPI 3.1, Leaflet, y empaquetado limpio en `dist/`. |
| **Borradores Preliminares de Word** | Informes autogenerados desalineados | ❌ **Reemplazados:** La única fuente de verdad documental es **`AburráSegura.docx` (v2.1)**. |

---

## 2. Hallazgos de Auditoría Técnica Resueltos y Saneados (08/10/2026)

1. **Conciliación de Cifras con la Fuente de Verdad:**
   - Se descartaron las cifras infladas o incongruentes de borradores previos. Todas las métricas del Vault se extraen directamente del archivo verificado `data/benchmarks/benchmark_results_fase4.json` y de ejecuciones en vivo de Pytest.
   - *Ejemplo verificado:* La aceleración del KD-Tree 2D en $n=200.000$ es exactamente **$4.018,3\times$** ($5{,}34\text{ ms}$ vs. $21.458{,}12\text{ ms}$).
2. **Saneamiento de Autores y Metadatos Institucionales:**
   - Se eliminaron referencias a autores ajenos ("Santiago", "Cristian David Pérez"). La autoría formal del proyecto corresponde exclusivamente a:
     - **Jarrison Quintero Castillo**
     - **Sebastián Gómez Cardona**
     - **Cristian David Pulgarín Vélez**
3. **Sinceramiento de Pruebas Automatizadas:**
   - Se eliminaron citas a archivos de test inexistentes (`test_spatial.py`, etc.). El inventario de pruebas refleja los 7 archivos reales en `tests/`: `test_api.py` (13), `test_sorting.py` (14), `test_complexity_benchmarks.py` (6), `test_benchmarks_fase4.py` (4), `test_kdtree.py` (3), `test_graph_routing.py` (2), `test_clustering.py` (2). Total: **44/44 PASS**.
4. **Validación de Referencias Bibliográficas APA 7:**
   - La lista de 11 referencias de la Sección 6 fue revisada y estandarizada alfabéticamente en [[Referencias-APA7]], incluyendo la advertencia sobre la referencia de control de Ogata (2010).

---

## 3. Estado de Conciliación en el Vault

Todas las notas del Vault han sido actualizadas y armonizadas con la versión oficial de **`AburráSegura.docx` (v2.1)**, garantizando que el Vault sirva directamente como base técnica e intelectual para la entrega final y la sustentación oral del equipo.

---

## 🔗 Relacionado
- [[00 - Inicio|Inicio]]
- [[MOC-Principal]]
- [[Hoja-de-Ruta-Nuevo-Horizonte]]
- [[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad|ADR-005]]
