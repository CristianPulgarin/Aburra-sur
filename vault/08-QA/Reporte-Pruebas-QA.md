---
titulo: "Reporte de Aseguramiento de Calidad y Pruebas Unitarias/Integración"
tipo: qa
tipo: reporte_qa
proyecto: PPI - Analisis de Algoritmos
fecha: 2026-09-29
autor: qa-tester
estado: superado
requisito_asociado:
  - R9
vigencia: historico
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/qa, ppi/tdea, proyecto/aburrasegura]
---


> [!WARNING] Nota histórica (alcance anterior)
> Esta nota pertenece al prototipo de alcance amplio (24–30/09/2026), reemplazado el 05–06/10/2026 por [[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad]]. Se conserva como memoria. **No reutilizar sus cifras sin recalcularlas** (ver [[Archivo-Alcance-Anterior]]).

# Reporte de Aseguramiento de Calidad y Pruebas Automatizadas

> [!abstract] En pocas palabras
> Reporte detallado de pruebas unitarias y de integración para algoritmos de ordenamiento, estructuras espaciales y servicios web.


Se ejecutó la suite de pruebas unitarias y de integración mediante `pytest` sobre todos los módulos algorítmicos, el pipeline de datos y los endpoints REST de la API.

## 1. Resumen de Ejecución
- **Framework:** `pytest 9.1.1` con Python 3.14.3 (Windows).
- **Total pruebas ejecutadas:** **27 pruebas**.
- **Resultado:** **27 aprobadas (100% de éxito)** en 1.61 segundos.
- **Tolerancia a fallos:** 0 fallos, 0 errores.

## 2. Cobertura por Módulo

| Módulo de Prueba | Componente Evaluado | Casos Borde y Escenarios Verificados | Estado |
| :--- | :--- | :--- | :---: |
| `test_sorting.py` | Merge Sort, Quick Sort, Heap Sort, Counting Sort, Timsort | Listas vacías, elementos unitarios, listas idénticas repetidas, ya ordenadas y en orden inverso. Exactitud del contador de comparaciones. | **14/14 PASS** |
| `test_kdtree.py` | KD-Tree 2D y Búsqueda Lineal | Árbol vacío, validación estricta de igualdad de resultados contra búsqueda lineal exhaustiva, y consultas $k$-NN con Max-Heap. | **3/3 PASS** |
| `test_graph_routing.py`| Dijkstra y A* multiobjetivo | Grafo dirigido con pesos multiobjetivo, comparación ruta corta vs ruta segura, y detección de componentes disconexas. | **2/2 PASS** |
| `test_clustering.py` | DBSCAN geodésico | Datos vacíos, agrupamiento espacial con ruido aislado en coordenadas periféricas. | **2/2 PASS** |
| `test_api.py` | Endpoints FastAPI REST | Healthcheck (`/health`), lista de incidentes (`/incidents`), ejecución de benchmark (`/benchmarks/sort`), benchmark espacial y cálculo de ruta (`/routing/calculate`). | **6/6 PASS** |

## 3. Conclusión de QA
Todos los algoritmos han demostrado correctitud matemática contra casos borde severos y los endpoints de la API responden con los códigos de estado y esquemas Pydantic esperados.

---

## 🔗 Relacionado
- [[00 - Inicio|Inicio]]
- [[Plan-Pruebas-QA]]
- [[Reporte-Final-QA-Fase5]]
