---
titulo: "Estado Integral del Documento Institucional (AburráSegura.docx)"
tipo: especificacion
tipo: estado_documento
proyecto: PPI - Analisis de Algoritmos
institucion: Tecnologico de Antioquia
documento: "AburráSegura.docx (d:/Proyecto Algoritmos/)"
version_documento: 2.1 (08/10/2026)
fecha_revision: 2026-10-08
estado: en_fase_final
tags:
  - documento-guia
  - estado
  - seguimiento
  - aburrasegura
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/especificacion, ppi/tdea, proyecto/aburrasegura]
---


# Estado Integral del Documento Institucional (Sección por Sección)

> [!abstract] En pocas palabras
> Auditoría sección por sección del avance de redacción del documento oficial AburráSegura.docx (414 párrafos y 15 tablas) frente a la guía oficial del PPI.


> [!IMPORTANT]
> **Documento Oficial de Entrega:** `d:\Proyecto Algoritmos\AburráSegura.docx` (última actualización: **08/10/2026**, 414 párrafos, 15 tablas formales). Construido rigurosamente sobre la plantilla institucional `FORMATO PPI INFRESTRUCTURA Y PROYECTOS PPI.docx` de la Facultad de Ingeniería del TdeA.

---

## 1. Datos Generales de Portada
- **Marca / Nombre del Prototipo:** **AburráSegura**.
- **Título Oficial:** *Plataforma para la Identificación de Puntos Críticos y Rutas Seguras de Siniestralidad Vial en Medellín mediante el Algoritmo de Grafos*.
- **Integrantes:** **Jarrison Quintero Castillo, Sebastián Gómez Cardona, Cristian David Pulgarín Vélez**.
- **Programa Académico:** Ingeniería en Software — Facultad de Ingeniería — Tecnológico de Antioquia Institución Universitaria, Medellín, 2026.
- **Asignatura:** Análisis de Algoritmos (8vo Semestre).

---

## 2. Tablero de Avance Detallado Sección por Sección

| Sección del Formato PPI | Estado en Word | Detalle del Contenido en `AburráSegura.docx` | Enlaces del Vault |
| :--- | :---: | :--- | :--- |
| **Portada Institucional** | ✅ **Hecho** | Título institucional completo, 3 autores oficiales, metadatos institucionales y año 2026. | [[Registro-Actualizaciones]] |
| **Registro de Actualizaciones (Tabla 0)** | ✅ **Hecho** | Registradas v1.0 (07/09), v1.1 (14/09), v1.2 (21/09), v2.0 (05/10) y v2.1 (08/10). | [[Registro-Actualizaciones]] |
| **Tabla de Contenido e Índices** | ⏳ **Final** | Estructura de títulos y subtítulos definida; generación automática de campos en Word al finalizar revisión. | — |
| **Tabla 1: Abreviaturas Técnicas** | ✅ **Hecho** | **26 filas (1 encabezado + 25 siglas)** ordenadas alfabéticamente (API, B-Tree, CORS, CPU, CSV, DAG, DBSCAN, ETL, GeoJSON, GPS, HTTP, JSON, KD-Tree, MEData, Min-Heap, OSM, OSRM, PPI, RAM, REST, SPA, SQLite, TdeA, UI/UX, WGS84). | [[Diccionario-Variables]] |
| **RESUMEN** | ✅ **Hecho** | Redacción formal y accesible (máximo 300 palabras): apoyo a actores viales vulnerables, integración de MEData con Dijkstra y arquitectura desacoplada. | [[Hoja-de-Ruta-Nuevo-Horizonte]] |
| **INTRODUCCIÓN** | ✅ **Hecho** | Contextualización de la crisis de accidentalidad en Medellín (Autopista Norte, Regional, Glorieta 33), limitaciones de Waze/Google Maps y formulación del problema. | [[Antecedentes-Academicos]] |
| **1.1. Definición del problema** | ✅ **Hecho** | Causas geográficas, exceso de velocidad, puntos ciegos, pérdida de vidas humanas e insuficiencia de análisis algorítmico sobre datos abiertos. | [[Diccionario-Variables]] |
| **1.2. Justificación del prototipo** | ✅ **Hecho** | Dimensión académica (Dijkstra propio con *min-heap*, demostraciones asintóticas) y dimensión comunitaria (prevención de accidentes). | [[Conclusiones-y-Resultados]] |
| **1.3. Objetivos (General y Específicos)** | ✅ **Hecho** | **Tabla 2 completada al 100%**: Objetivo General + 3 Objetivos Específicos con sus respectivas fases y entregables técnicos formalmente asignados. | [[Matriz-Requisitos]] |
| **1.4. Alcances y Limitaciones** | ✅ **Hecho** | Define qué incluye (datos históricos 2014-2024, Dijkstra multiobjetivo, 3 capas, web SPA) y qué no (sin sensores telemáticos físicos en vehículos). | [[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad]] |
| **2.1. Antecedentes (Tabla 3)** | ✅ **Hecho** | 4 referentes analizados a profundidad: Google Maps/Waze, Portal MEData, Algoritmo de Dijkstra (1959) y Cormen et al. (2022). | [[Antecedentes-Academicos]] |
| **2.2. Sistema de control** | ✅ **Hecho** | Analogía de lazo cerrado adaptada a software: Entrada de usuario, Sensor de datos MEData, Controlador Dijkstra, Actuador React y Retroalimentación. | [[Referencias-APA7]] |
| **2.2. Comunicación móvil** | ✅ **Hecho** | Comparativa de Bluetooth vs. Wi-Fi vs. 4G/5G; fundamentación de arquitectura híbrida cliente-servidor sobre HTTP/JSON y estándares IEEE/ETSI. | [[Diseno-Backend-API]] |
| **2.3. Diagrama y Arquitectura de Hardware** | ✅ **Hecho** | Especificación técnica de equipos comerciales: Procesador multinúcleo, memoria RAM, GPS cliente, visualizador y suministro de energía. | [[Protocolo-Experimental]] |
| **3.1. Requerimientos Funcionales** | ✅ **Hecho** | **16 Requerimientos Funcionales (RF-01 a RF-16)** agrupados en 5 módulos temáticos (Tablas 4 a 8) con prioridad y objetivo trazado. | [[Matriz-Requisitos]] |
| **3.2. Restricciones del Diseño** | ✅ **Hecho** | Restricciones de Presupuesto (Tabla 9), Hardware (Tabla 10), Datos (Tabla 11), Metodológicas/Tiempo (Tabla 12) y Normas Legales (Tabla 13). | [[Matriz-Requisitos]] |
| **4.1. Selección de Componentes y Presupuesto** | ✅ **Hecho** | **Tabla 14 completa**: Portátil servidor, Smartphone cliente, Router Wi-Fi, Plan de datos móvil y Cargador vehicular ($3.940.000 COP con equipos propios). | [[Matriz-Requisitos]] |
| **4.2. Diseño del Software** | ✅ **Hecho** | Arquitectura en 3 capas (Figura 1), modelado de red vial en grafo $G = (V, E)$, función de coste multiobjetivo con $\alpha$ y $\beta$, Dijkstra con min-heap y flujo (Figura 2). | [[Grafos-Dijkstra-AStar]], [[Diseno-Backend-API]] |
| **4.3. Diseño de la Interfaz de Usuario** | ✅ **Hecho** | Especificación de Mockup 1 (Inicio y selección), Mockup 2 (Comparativa de rutas azul vs. verde) y Mockup 4 (Mapa de calor y puntos críticos). | [[Diseno-Frontend-UI]] |
| **5.1. Implementación Hardware y Software** | 🟡 **Listo en Vault** | Trazabilidad del prototipo funcional, suite de 44 pruebas Pytest (100% PASS), compilación limpia de frontend en Vite y datos medidos del laboratorio asintótico. | [[Laboratorio-Jerarquia-Asintotica]], [[Reporte-Final-QA-Fase5]] |
| **6. CONCLUSIONES** | 🟡 **Listo en Vault** | Conclusiones formalizadas para Objetivo General y 3 Específicos, reflexiones teóricas/metodológicas/experimentales e impacto social y comunitario. | [[Conclusiones-y-Resultados]] |
| **6. REFERENCIAS BIBLIOGRÁFICAS** | ✅ **Hecho** | 11 referencias bibliográficas en formato APA 7ma edición estandarizadas y verificadas al final del documento. | [[Referencias-APA7]] |
| **7. ANEXOS** | 🟡 **Listo en Vault** | Manual de usuario paso a paso del prototipo y especificación de endpoints REST documentada. | [[Manual-Usuario-Prototipo]] |

---

## 3. Estado de los Componentes Técnicos del Proyecto

- **Base de Datos:** `medellin_incidents.db` (SQLite) con 251.150 siniestros limpios indexados con B-Tree sobre coordenadas, gravedad y comuna.
- **Grafo Vial:** `medellin_graph.json` con 32 intersecciones y 84 tramos arteriales dirigidos con pesos ponderados.
- **Backend REST:** FastAPI con rutas `/api/v1/routing`, `/api/v1/incidents`, `/api/v1/benchmarks` y `/health` completamente documentadas en Swagger OpenAPI 3.1.
- **Frontend SPA:** React 18 + Vite + Leaflet compilado exitosamente en `frontend/dist/`.
- **Suite de Pruebas:** 44 pruebas automatizadas ejecutadas y aprobadas al 100% (`44 passed in 8.31s`).

---

## 🔗 Relacionado
- [[00 - Inicio|Inicio]]
- [[Matriz-Requisitos]]
- [[Registro-Actualizaciones]]
- [[Historial de cambios]]
