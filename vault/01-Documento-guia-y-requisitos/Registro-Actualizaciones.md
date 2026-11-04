---
titulo: "Registro Formal de Actualizaciones del Documento Institucional (Tabla 0)"
tipo: cambios
tipo: control_versiones
proyecto: PPI - Analisis de Algoritmos
institucion: Tecnologico de Antioquia
estado: completado
version_documento: 2.1
fecha: 2026-10-08
autores:
  - Jarrison Quintero Castillo
  - Sebastián Gómez Cardona
  - Cristian David Pulgarín Vélez
tags:
  - registro-actualizaciones
  - versiones
  - ppi
  - tdea
  - aburrasegura
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/cambios, ppi/tdea, proyecto/aburrasegura]
---


# Registro Formal de Actualizaciones del Documento Institucional (Tabla 0)

> [!abstract] En pocas palabras
> Registro formal de control de versiones y actualizaciones del informe institucional (AburráSegura.docx), replicando la Tabla 0 desde la versión 1.0 hasta la 2.1.


Este registro replica y amplía con exactitud la **Tabla 0 de `AburráSegura.docx`**, documento oficial y fuente de verdad del equipo para el informe institucional del PPI ante la Facultad de Ingeniería del Tecnológico de Antioquia.

---

## 1. Tabla Oficial de Versiones del Documento (`AburráSegura.docx`)

| Fecha | Versión | Descripción de la Actualización | Autores |
| :---: | :---: | :--- | :---: |
| **07/09/2026** | **1.0** | **Versión inicial del informe:** Estructuración de la plantilla oficial, definición del problema preliminar y conformación del equipo de trabajo. | Jarrison Quintero Castillo<br>Sebastián Gómez Cardona<br>Cristian David Pulgarín Vélez |
| **14/09/2026** | **1.1** | **Lluvia de ideas para el proyecto:** Evaluación de dominios de aplicación, selección del fenómeno de siniestralidad vial en Medellín y exploración del portal MEData. | Jarrison Quintero Castillo<br>Sebastián Gómez Cardona<br>Cristian David Pulgarín Vélez |
| **21/09/2026** | **1.2** | **Desarrollo de la idea principal:** Formulación de los 3 objetivos específicos, planteamiento del modelado topológico con grafos y justificación pedagógica y comunitaria. | Jarrison Quintero Castillo<br>Sebastián Gómez Cardona<br>Cristian David Pulgarín Vélez |
| **05/10/2026** | **2.0** | **Versión intermedia del informe:** Replanteamiento conceptual centrado en el Algoritmo de Dijkstra con min-heap y delimitación de puntos críticos. Redacción formal de Portada, Resumen, Introducción y Sección 1 completa (Definición del problema, Justificación, Objetivos y Alcances). | Jarrison Quintero Castillo<br>Sebastián Gómez Cardona<br>Cristian David Pulgarín Vélez |
| **08/10/2026** | **2.1** | **Consolidación técnica integral:**<br>• Poblado exhaustivo de la **Tabla 1 de Abreviaturas Técnicas** (25 siglas ordenadas alfabéticamente desde API hasta WGS84).<br>• Completado formal de la columna *"Fase / Entregable asociado"* en la **Tabla 2 de Objetivos Específicos** (Fases 1, 2 y 3).<br>• Incorporación de los **16 Requerimientos Funcionales (RF-01 a RF-16)** en Tablas 4 a 8 y Restricciones de Diseño (Tablas 9 a 13).<br>• Inclusión del presupuesto de hardware en Tabla 14 ($3.940.000 COP referencial).<br>• Integración de la arquitectura de software en 3 capas, función de coste multiobjetivo y flujo de cálculo de rutas (Figuras 1 y 2).<br>• Especificación detallada de Mockups 1, 2 y 4 (Sección 4.3).<br>• Depuración y estandarización de 11 referencias bibliográficas bajo normas APA 7ma edición. | Jarrison Quintero Castillo<br>Sebastián Gómez Cardona<br>Cristian David Pulgarín Vélez |

---

## 2. Hitos Técnicos y Cronología del Prototipo Computacional

| Fecha | Hito Técnico | Entregables Clave Asociados | Estado |
| :---: | :--- | :--- | :---: |
| **24–30/09/2026** | Prototipo inicial de amplio espectro ("Fases 1 a 5"). | 4 familias algorítmicas (Merge, Quick, Heap, Counting, KD-Tree, DBSCAN, Dijkstra, A*). Suite de 35 pruebas automatizadas. Particiones CSV de 1K a 1M. | Archivado como memoria técnica ([[Archivo-Alcance-Anterior]]). |
| **05/10/2026** | Replanteamiento de alcance orientado a defensa clara. | Adopción del enfoque unificado: Puntos críticos de Medellín + Algoritmo de Dijkstra multiobjetivo con cola de prioridad min-heap ([[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad]]). | Vigente |
| **06/10/2026** | Retroalimentación docente: Demostración en tiempo real de la jerarquía asintótica completa. | Diseño del módulo **Laboratorio de Jerarquía Asintótica** para medir $\mathcal{O}(1)$, $\mathcal{O}(\log n)$, $\mathcal{O}(n)$, $\mathcal{O}(n \log n)$, $\mathcal{O}(n^2)$ sobre los 251.150 incidentes reales. | Implementado y Verificado |
| **07/10/2026** | Implementación del Laboratorio de Complejidad y nuevos tests. | Módulo `app/algorithms/complexity_benchmarks.py`, endpoint `POST /api/v1/benchmarks/complexity`, suite de pruebas ampliada a 44 tests. Compilación limpia del frontend en Vite (`dist/`). | Superado con éxito |
| **08/10/2026** | Actualización y sincronización exhaustiva de `AburráSegura.docx` y Vault de Obsidian. | Ejecución del script `scripts/update_docx_deliverables.py` sobre el Word oficial. Certificación de 44/44 pruebas aprobadas en Pytest. Vault de Obsidian actualizado al 100% con plantillas, demostraciones matemáticas en LaTeX, contratos OpenAPI y manuales. | **Completado y Certificado** |

---

## 3. Trazabilidad de Responsabilidades del Equipo

- **Jarrison Quintero Castillo:** Modelado topológico del grafo vial, investigación de antecedentes y justificación comunitaria del prototipo.
- **Sebastián Gómez Cardona:** Pipeline de ingeniería de datos MEData, persistencia en SQLite, algoritmo de Dijkstra multiobjetivo y arquitectura de software.
- **Cristian David Pulgarín Vélez:** Laboratorio de jerarquía asintótica, diseño de interfaz de usuario en React/Leaflet y suite de pruebas automatizadas QA en Pytest.

---

## 🔗 Relacionado
- [[00 - Inicio|Inicio]]
- [[Historial de cambios]]
- [[Matriz-Requisitos]]
- [[Estado-Documento-Institucional]]
