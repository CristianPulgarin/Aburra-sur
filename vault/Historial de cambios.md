---
titulo: "Historial de cambios"
tipo: cambios
estado: vigente
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/cambios, proyecto/aburrasegura, ppi/tdea]
---

# 📝 Historial de Cambios — Proyecto AburráSegura

> [!abstract] En pocas palabras
> Registro cronológico de hitos, versiones formales del documento institucional (`AburráSegura.docx`), avances algorítmicos y cambios de infraestructura para el PPI de Análisis de Algoritmos.

```mermaid
timeline
    title Hitos Principales del Proyecto AburráSegura (2026)
    07/09/2026 : Versión 1.0 : Inicio formal, conformación de equipo y planteamiento de problema
    14/09/2026 : Versión 1.1 : Selección del fenómeno de siniestralidad vial en Medellín y exploración MEData
    21/09/2026 : Versión 1.2 : Formulación de objetivos específicos y modelado topológico en grafos
    30/09/2026 : Fase 1 a 5 : Prototipo amplio previo (Ordenamiento, KD-Tree, DBSCAN, Dijkstra, A*)
    05/10/2026 : Versión 2.0 : Replanteamiento conceptual (Dijkstra Min-Heap + Puntos Críticos)
    06/10/2026 : Laboratorio : Concepción del Laboratorio de Jerarquía Asintótica O(1) a O(n²)
    07/10/2026 : Verificación : Endpoint de benchmarks, suite de 44 tests Pytest y build limpio Vite
    08/10/2026 : Versión 2.1 : Consolidación integral en Word oficial (AburráSegura.docx) y 44/44 tests PASS
    19/10/2026 : Estandarización : Integración con plugin obsidian-docs, 00 - Inicio.md y Canvas interactivo
```

---

## 📌 Versiones Formales del Documento Institucional (`AburráSegura.docx`)

### [v2.1] — 2026-10-08 (Consolidación Técnica Definitiva)
- **Tabla 1 de Abreviaturas:** 25 siglas técnicas estandarizadas alfabéticamente (API a WGS84).
- **Tabla 2 de Objetivos Específicos:** Alineación formal de fases y entregables del documento.
- **Tablas 4 a 13 (Requisitos y Restricciones):** 16 Requerimientos Funcionales (RF-01 a RF-16) y restricciones normativas (Ley 1581 Habeas Data, ODbL).
- **Tabla 14 (Presupuesto):** Presupuesto referencial de hardware valorado en $3.940.000 COP con equipos locales.
- **Suite de Pruebas Pytest:** Certificación de **44/44 pruebas aprobadas (100% PASS en 8.31s)**.
- **Referencias Bibliográficas:** 11 fuentes académicas depuradas bajo norma APA 7ma edición.

### [v2.0] — 2026-10-05 (Replanteamiento Orientado a Sustentación)
- Definición del enfoque principal: Algoritmo de Dijkstra multiobjetivo con cola de prioridad min-heap $\mathcal{O}((V + E) \log V)$ para evitar puntos críticos viales.
- Redacción formal de Portada, Resumen, Introducción y Sección 1 completa.

### [v1.2] — 2026-09-21 (Formulación de Objetivos y Grafo)
- Especificación de los 3 objetivos específicos del PPI.
- Justificación pedagógica y social para la movilidad segura en Medellín.

### [v1.1] — 2026-09-14 (Exploración de Fuentes)
- Evaluación de dominios de aplicación y selección de la accidentalidad vial de Medellín con datos abiertos de MEData.

### [v1.0] — 2026-09-07 (Inicio del Proyecto)
- Estructuración de plantilla oficial y asignación de roles del equipo (Jarrison Quintero, Sebastián Gómez, Cristian Pulgarín).

---

## 🔗 Relacionado

- [[00 - Inicio|Página de Inicio del Vault]]
- [[MOC-Principal|MOC Principal de AburráSegura]]
- [[Registro-Actualizaciones|Registro Formal de Actualizaciones (Tabla 0 del Word)]]
- [[Matriz-Requisitos|Matriz Integral de Trazabilidad]]
