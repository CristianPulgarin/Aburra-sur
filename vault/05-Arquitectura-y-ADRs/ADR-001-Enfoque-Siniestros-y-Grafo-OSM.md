---
tipo: decision
id: ADR-001
titulo: Seleccion del Enfoque Hibrido (Siniestros MEData + Grafo Vial OpenStreetMap)
estado: aceptado
fecha: 2026-09-29
responsables:
  - investigador
  - orquestador
  - especialista-algoritmos
requisito_asociado:
  - R2
  - R4
  - R6
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/decision, ppi/tdea, proyecto/aburrasegura]
---

# ADR-001: Selección del Enfoque Híbrido (Siniestros MEData + Grafo Vial OpenStreetMap)

> [!abstract] En pocas palabras
> Decisión arquitectónica para desacoplar el grafo topológico vial de OpenStreetMap y ponderar los arcos con la densidad de incidentes precomputada.


## Estado
**Aceptado** (Validado por el usuario el 2026-09-29).

## Contexto y Problema
El curso de **Análisis de Algoritmos** (8vo semestre, Tecnológico de Antioquia) requiere el diseño, análisis asintótico formal ($O, \Theta, \Omega$) y experimentación empírica de diversas familias de algoritmos y estructuras de datos. La idea inicial de trabajar exclusivamente con la tabla de siniestros viales de Medellín limitaba el proyecto a ordenamiento y clustering tabular, omitiendo la teoría de grafos y algoritmos de optimización de caminos mínimos.

## Decisión Tomada
Se adopta formalmente la **Opción B**: Enriquecer los datos históricos de siniestralidad vial (MEData / datos.gov.co) cruzándolos con la topología de la red vial de Medellín extraída de OpenStreetMap (OSM).

### Impacto Algorítmico
1. **Indexación Espacial:** Se implementa un **KD-Tree** desde cero para asociar siniestros a las aristas viales más cercanas en $O(\log V)$ promedio.
2. **Teoría de Grafos y Enrutamiento:** Se implementan **Dijkstra** y **A\*** desde cero, modelando la red con una función de coste multiobjetivo:
   $$w(e) = \alpha \cdot \text{longitud}(e) + \beta \cdot \text{riesgo}(e)$$
   permitiendo calcular y comparar la *ruta más rápida* vs. la *ruta más segura*.
3. **Ordenamiento y Clustering:** Benchmarking de algoritmos de ordenamiento clásico ($n = 1K$ a $1M$) y **DBSCAN** para la identificación de zonas de concentración de accidentes (*hotspots*).

## Consecuencias
- **Positivas:** Máxima alineación con los objetivos académicos de la materia; prototipo visual de alto impacto social y pedagógico; cobertura integral de grafos, estructuras espaciales y ordenamiento.
- **Negativas / Desafíos:** Requiere preprocesamiento espacial adicional para construir y validar el grafo conexo de Medellín (~25.000 nodos y ~60.000 aristas).

---

## 🔗 Relacionado
- [[00 - Inicio|Inicio]]
- [[ADR-002-Arquitectura-FastAPI-React|ADR-002]]
- [[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad|ADR-005]]
- [[Grafos-Dijkstra-AStar]]
