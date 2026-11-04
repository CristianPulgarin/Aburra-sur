---
titulo: "ADR-005: Replanteamiento del Alcance — Dijkstra Multiobjetivo y Laboratorio de Complejidad"
tipo: decision
tipo: adr
id: ADR-005
proyecto: PPI - Analisis de Algoritmos
institucion: Tecnologico de Antioquia
estado: aceptado
fecha: 2026-10-07
reemplaza: "[[ADR-004-Protocolo-Benchmarking-Masivo-y-Contraste-Asintotico]]"
tags:
  - adr
  - replanteamiento
  - alcance
  - dijkstra
  - complejidad
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/decision, ppi/tdea, proyecto/aburrasegura]
---


# ADR-005: Replanteamiento del alcance — Dijkstra + Puntos Críticos + Laboratorio de Complejidad

> [!abstract] En pocas palabras
> Decisión estratégica de concentrar el alcance del PPI en Dijkstra multiobjetivo con Min-Heap y el Laboratorio de Jerarquía Asintótica para una defensa técnica contundente.


## 1. Contexto
Al cierre de la "Fase 5" (30/09/2026) el prototipo implementaba **cuatro familias algorítmicas** (ordenamiento ×4, KD-Tree 2D, DBSCAN, Dijkstra y A*), con un frontend y un backend extensos. El 05/10/2026 el equipo concluyó que el proyecto tenía **demasiada tecnicidad y demasiados algoritmos** para defenderlo con claridad.

Posteriormente (06/10/2026) el docente precisó la expectativa central de la asignatura:
- Medir **tiempos computacionales en tiempo real** para **todas las clases de complejidad**: $\mathcal{O}(1)$, $\mathcal{O}(\log n)$, $\mathcal{O}(n)$, $\mathcal{O}(n \log n)$, $\mathcal{O}(n^x)$.
- Trabajar con **muchos más datos**.

## 2. Decisión
1. **Una sola historia central:** identificar puntos críticos de siniestralidad en Medellín (datos MEData) y calcular **ruta más corta vs. ruta más segura** con el **algoritmo de Dijkstra** (cola de prioridad *min-heap*), programado por el equipo.
2. **Un módulo específico de complejidad** ("Laboratorio de Jerarquía Asintótica"): mide en tiempo real una operación representativa por clase sobre los mismos datos de siniestros. Detalle en [[Laboratorio-Jerarquia-Asintotica]].
3. **Primero el documento, después el código.** No se programa nada hasta que el usuario lo indique explícitamente (instrucción del 05/10/2026).
4. **Fuera de alcance:** KD-Tree, A*, Heap Sort, Counting Sort, Quick Sort, geocodificación tipo Google Maps, enrutamiento continuo puerta a puerta.

## 3. Alternativas consideradas
| Alternativa | Motivo de descarte |
| :--- | :--- |
| Mantener las 4 familias algorítmicas | Exceso de complejidad; difícil de sustentar; diluye el foco. |
| Solo Dijkstra (opción A) | No cubre la jerarquía completa de complejidades pedida por el docente. |
| Solo DBSCAN / puntos críticos (opción C) | Pierde el componente de optimización en grafos y el impacto social de la ruta segura. |
| **A + C + módulo de complejidad** | **Elegida:** una narrativa simple + cobertura completa de $\mathcal{O}(1)$ a $\mathcal{O}(n^2)$. |

## 4. Consecuencias
- **Positivas:** narrativa defendible; se alinea con el núcleo de la asignatura; el código existente de datos, Dijkstra y Merge Sort es potencialmente reutilizable.
- **Negativas / riesgos:**
  - Los entregables de la "Fase 5" (`INFORME_PPI_FINAL_FASE5.docx`, guion, manual, conclusiones) quedan **obsoletos**.
  - $\mathcal{O}(n^2)$ no puede ejecutarse sobre 250.000 registros en tiempo razonable (≈ $3{,}1 \times 10^{10}$ comparaciones); requiere un tope de $n$ (ver [[Laboratorio-Jerarquia-Asintotica]]).
  - El método para delimitar puntos críticos aún no está decidido (conteo por tramo vs. DBSCAN).

## 5. Respaldo en el documento guía
- Sec. 1.3: "máximo 3 objetivos específicos, medibles y alcanzables… que cada objetivo se corresponda con una fase".
- Sec. 1.4: definir qué incluye el prototipo y qué no.
- Naturaleza de la asignatura (Análisis de Algoritmos): contraste empírico vs. teórico de complejidad.

---

## 🔗 Relacionado
- [[00 - Inicio|Inicio]]
- [[Hoja-de-Ruta-Nuevo-Horizonte]]
- [[Grafos-Dijkstra-AStar]]
- [[Laboratorio-Jerarquia-Asintotica]]
- [[ADR-002-Arquitectura-FastAPI-React|ADR-002]]
