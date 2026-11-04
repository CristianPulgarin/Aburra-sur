---
titulo: "Map of Content (MOC) Principal — Proyecto PPI AburráSegura"
tipo: indice
tipo: moc
proyecto: PPI - Analisis de Algoritmos
institucion: Tecnologico de Antioquia
semestre: 8vo Semestre - 2026
estado: consolidado_fase_final
version: 2.1
fecha_creacion: 2026-09-29
fecha_actualizacion: 2026-10-08
autores:
  - Jarrison Quintero Castillo
  - Sebastián Gómez Cardona
  - Cristian David Pulgarín Vélez
tags:
  - moc
  - ppi
  - algoritmos
  - aburrasegura
  - tdea
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/indice, ppi/tdea, proyecto/aburrasegura]
---


# Map of Content (MOC) Principal — Proyecto PPI AburráSegura

> [!abstract] En pocas palabras
> Mapa de Contenidos central que articula la memoria académica, técnica y metodológica del proyecto AburráSegura para el Tecnológico de Antioquia.


Memoria viva, estructurada y académica del **Proyecto Pedagógico Integrador (PPI)** — **Análisis de Algoritmos**, Facultad de Ingeniería, Tecnológico de Antioquia Institución Universitaria.

> [!NOTE] Metadatos Oficiales del Proyecto
> - **Nombre / Marca:** **AburráSegura**.
> - **Título Oficial:** *Plataforma para la Identificación de Puntos Críticos y Rutas Seguras de Siniestralidad Vial en Medellín mediante el Algoritmo de Grafos*.
> - **Integrantes del Equipo:**
>   - **Jarrison Quintero Castillo**
>   - **Sebastián Gómez Cardona**
>   - **Cristian David Pulgarín Vélez**
> - **Documento Fuente Institucional:** `AburráSegura.docx` (v2.1 del 08/10/2026, 414 párrafos, 15 tablas, ubicado en la raíz del proyecto).
> - **Certificación de Pruebas:** **44/44 pruebas aprobadas en Pytest (100% éxito en 8.31s)**.

---

## 🧭 00. Inicio y Navegación Estratégica
- [[Hoja-de-Ruta-Nuevo-Horizonte|Hoja de Ruta: Hitos del proyecto, decisiones y estado de entrega]]
- [[Estado-Documento-Institucional|Estado del Documento Institucional (Avance sección por sección en AburráSegura.docx)]]
- [[Archivo-Alcance-Anterior|Archivo Histórico: Prototipo amplio previo y auditoría de integridad]]

---

## 📋 01. Documento Guía y Requisitos
- [[Matriz-Requisitos|Matriz Integral de Trazabilidad: R1–R10, RF-01 a RF-16 y Restricciones de Diseño]]
- [[Registro-Actualizaciones|Registro Formal de Actualizaciones (Tabla 0 del Word: v1.0 a v2.1)]]

---

## 🔬 02. Investigación y Marco Teórico
- [[Antecedentes-Academicos|Antecedentes Académicos y Estado del Arte (Cormen, Dijkstra, Bentley, Ester, Boeing)]]
- [[Fuentes-y-Matriz-Decision|Fuentes de Datos y Matriz de Decisión Multicriterio (MEData vs. SODA vs. OSM)]]
- [[Referencias-APA7|Referencias Bibliográficas en Formato APA 7ma Edición (Verificadas)]]

---

## 📊 03. Datos de Siniestralidad Vial
- [[Diccionario-Variables|Diccionario Canónico de Variables, EDA Histórico (2014-2024) y Análisis de Sesgos]]
- [[Pipeline-Limpieza|Pipeline de Ingesta ETL, Bounding Box WGS84, Esquema SQLite y Particiones CSV]]

---

## ⚙️ 04. Algoritmos y Complejidad Asintótica
- [[Laboratorio-Jerarquia-Asintotica|Laboratorio de Jerarquía Asintótica: Demostración Formal de O(1) a O(n²) sobre MEData]]
- [[Grafos-Dijkstra-AStar|Teoría de Grafos y Enrutamiento Multiobjetivo: Dijkstra con Min-Heap y A*]]
- [[Algoritmos-Ordenamiento|Algoritmos de Ordenamiento: Merge, Quick (Hoare+M3), Heap, Counting y Timsort (1K a 1M)]]
- [[Estructuras-Espaciales-KDTree|Estructuras Espaciales: KD-Tree 2D, Distancia Geodésica Haversine y Speedup de 4.018x]]
- [[Clustering-DBSCAN-KMeans|Clustering Espacial: DBSCAN Geodésico con KD-Tree vs. K-Means para Hotspots]]
- [[Protocolo-Experimental|Protocolo Experimental de Medición: Hardware Ryzen 5, Varianza y Caché L1/L2/L3]]

---

## 🏛️ 05. Decisiones Arquitectónicas (ADRs)
- [[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad|ADR-005: Replanteamiento del Alcance (Dijkstra + Puntos Críticos + Laboratorio)]] ✅ *Vigente*
- [[ADR-001-Enfoque-Siniestros-y-Grafo-OSM|ADR-001: Selección del Enfoque Híbrido (MEData + Topología OpenStreetMap)]]
- [[ADR-002-Arquitectura-FastAPI-React|ADR-002: Arquitectura Desacoplada en 3 Capas (FastAPI Backend + React Frontend)]]
- [[ADR-003-Geocodificacion-y-Enrutamiento-Continuo-Tipo-Google-Maps|ADR-003: Geocodificación Urbana Híbrida y Enrutamiento Continuo]]
- [[ADR-004-Protocolo-Benchmarking-Masivo-y-Contraste-Asintotico|ADR-004: Marco de Benchmarking Masivo y Contraste Asintótico]]

---

## 🔌 06. Backend y Servicios REST
- [[Diseno-Backend-API|Especificación de la Capa Backend, Contratos OpenAPI 3.1 y Endpoints REST]]

---

## 🖥️ 07. Frontend y Experiencia de Usuario
- [[Diseno-Frontend-UI|Diseño de Interfaz Mobile-First, Tokens, Mockups 1 a 4 y Flujo de Usuario]]

---

## 🧪 08. Aseguramiento de Calidad (QA)
- [[Plan-Pruebas-QA|Plan Integral de Pruebas: Matriz de 44 Casos Automatizados y Casos Borde]]
- [[Reporte-Final-QA-Fase5|Certificación Oficial de Calidad QA: 44/44 PASS en Pytest]]
- [[Reporte-Pruebas-QA|Reporte Histórico de Pruebas Automatizadas]]

---

## 🏆 09. Resultados, Conclusiones y Entregables
- [[Conclusiones-y-Resultados|Conclusiones Formales por Objetivo (100% Cumplido), Aprendizajes e Impacto Social]]
- [[Manual-Usuario-Prototipo|Manual de Usuario Paso a Paso del Prototipo Computacional]]
- [[Guion-Sustentacion-Oral|Guion Estructurado de Sustentación Oral para el Equipo (Jarrison, Sebastián, Cristian)]]

---

## 📑 99. Plantillas Estándar del Vault
- [[Plantilla-Algoritmo|Plantilla Estándar para Documentación Exhaustiva de Algoritmos]]
- [[Plantilla-ADR|Plantilla Estándar para Decisiones Arquitectónicas (MADR / Nygard)]]
- [[Plantilla-Requisito|Plantilla Estándar para Especificación de Requisitos]]
- [[Plantilla-QA|Plantilla Estándar para Casos de Prueba Automatizados]]
- [[Plantilla-Modulo|Plantilla Estándar para Especificación de Módulos de Software]]

---

## 🔗 Relacionado
- [[00 - Inicio|Página de Inicio]]
- [[Hoja-de-Ruta-Nuevo-Horizonte]]
- [[Matriz-Requisitos]]
- [[Mapa del proyecto.canvas|Canvas Interactivo]]
