import re
import os
from pathlib import Path

VAULT = Path(r"D:\Proyecto Algoritmos\vault")

METADATA = {
    "00-Inicio/Archivo-Alcance-Anterior.md": {
        "titulo": "Archivo del Alcance Anterior y Auditoría de Integridad",
        "tipo": "resumen",
        "abstract": "Memoria técnica y registro de auditoría del prototipo inicial de amplio espectro desarrollado en fases previas (algoritmos de ordenamiento, particiones sintéticas y exploración de modelos).",
        "rel": ["[[00 - Inicio|Inicio]]", "[[MOC-Principal]]", "[[Hoja-de-Ruta-Nuevo-Horizonte]]", "[[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad|ADR-005]]"]
    },
    "00-Inicio/Hoja-de-Ruta-Nuevo-Horizonte.md": {
        "titulo": "Hoja de Ruta — Horizonte Consolidado del PPI",
        "tipo": "resumen",
        "abstract": "Plan de trabajo y cronograma estratégico consolidado tras el replanteamiento pedagógico, priorizando el enrutamiento seguro sobre grafos con Dijkstra y el Laboratorio de Complejidad.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[MOC-Principal]]", "[[Archivo-Alcance-Anterior]]", "[[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad|ADR-005]]"]
    },
    "00-Inicio/MOC-Principal.md": {
        "titulo": "Map of Content (MOC) Principal — Proyecto PPI AburráSegura",
        "tipo": "indice",
        "abstract": "Mapa de Contenidos central que articula la memoria académica, técnica y metodológica del proyecto AburráSegura para el Tecnológico de Antioquia.",
        "rel": ["[[00 - Inicio|Página de Inicio]]", "[[Hoja-de-Ruta-Nuevo-Horizonte]]", "[[Matriz-Requisitos]]", "[[Mapa del proyecto.canvas|Canvas Interactivo]]"]
    },
    "01-Documento-guia-y-requisitos/Estado-Documento-Institucional.md": {
        "titulo": "Estado Integral del Documento Institucional (AburráSegura.docx)",
        "tipo": "especificacion",
        "abstract": "Auditoría sección por sección del avance de redacción del documento oficial AburráSegura.docx (414 párrafos y 15 tablas) frente a la guía oficial del PPI.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Matriz-Requisitos]]", "[[Registro-Actualizaciones]]", "[[Historial de cambios]]"]
    },
    "01-Documento-guia-y-requisitos/Matriz-Requisitos.md": {
        "titulo": "Matriz Integral de Requisitos y Trazabilidad (v4.1 Definitiva)",
        "tipo": "especificacion",
        "abstract": "Matriz integral de trazabilidad que conecta los requisitos institucionales (R1 a R10) y 16 requerimientos funcionales con el código fuente y las 44 pruebas Pytest.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Estado-Documento-Institucional]]", "[[Registro-Actualizaciones]]", "[[Plan-Pruebas-QA]]"]
    },
    "01-Documento-guia-y-requisitos/Registro-Actualizaciones.md": {
        "titulo": "Registro Formal de Actualizaciones del Documento Institucional (Tabla 0)",
        "tipo": "cambios",
        "abstract": "Registro formal de control de versiones y actualizaciones del informe institucional (AburráSegura.docx), replicando la Tabla 0 desde la versión 1.0 hasta la 2.1.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Historial de cambios]]", "[[Matriz-Requisitos]]", "[[Estado-Documento-Institucional]]"]
    },
    "02-Investigacion/Antecedentes-Academicos.md": {
        "titulo": "Antecedentes Académicos y Estado del Arte",
        "tipo": "investigacion",
        "abstract": "Revisión del estado del arte en enrutamiento seguro, teoría de grafos, estructuras espaciales y clustering según Cormen, Dijkstra, Bentley y literatura especializada.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Fuentes-y-Matriz-Decision]]", "[[Referencias-APA7]]", "[[Grafos-Dijkstra-AStar]]"]
    },
    "02-Investigacion/Fuentes-y-Matriz-Decision.md": {
        "titulo": "Fuentes de Datos y Matriz de Decisión Multicriterio",
        "tipo": "investigacion",
        "abstract": "Matriz multicriterio de selección y justificación técnica de fuentes de datos de siniestralidad vial en Medellín (MEData vs. SODA vs. OpenStreetMap).",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Antecedentes-Academicos]]", "[[Diccionario-Variables]]", "[[Pipeline-Limpieza]]"]
    },
    "02-Investigacion/Referencias-APA7.md": {
        "titulo": "Referencias Bibliográficas Canónicas (Normas APA 7ma Edición)",
        "tipo": "investigacion",
        "abstract": "Compendio de 11 referencias bibliográficas canónicas estructuradas y depuradas bajo las normas internacionales APA 7.ª edición.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Antecedentes-Academicos]]", "[[Fuentes-y-Matriz-Decision]]"]
    },
    "03-Datos/Diccionario-Variables.md": {
        "titulo": "Diccionario Canónico de Datos y Análisis Exploratorio de Siniestralidad",
        "tipo": "datos",
        "abstract": "Especificación detallada de campos, tipos, rangos válidos, sesgos históricos y control de calidad de los 251.150 siniestros registrados entre 2014 y 2024.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Pipeline-Limpieza]]", "[[Fuentes-y-Matriz-Decision]]", "[[Clustering-DBSCAN-KMeans]]"]
    },
    "03-Datos/Pipeline-Limpieza.md": {
        "titulo": "Pipeline de Ingesta, Limpieza Geoespacial y Particionamiento",
        "tipo": "flujo",
        "abstract": "Arquitectura del pipeline ETL: filtrado por Bounding Box WGS84 de Medellín, imputación, normalización espacial y almacenamiento en SQLite.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Diccionario-Variables]]", "[[Estructuras-Espaciales-KDTree]]", "[[Clustering-DBSCAN-KMeans]]"]
    },
    "04-Algoritmos/Algoritmos-Ordenamiento.md": {
        "titulo": "Algoritmos de Ordenamiento: Análisis Asintótico y Comparativa",
        "tipo": "algoritmo",
        "abstract": "Estudio comparativo teórico y empírico de ordenamiento (MergeSort, QuickSort, HeapSort, CountingSort) aplicado a la jerarquización de siniestros viales.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Laboratorio-Jerarquia-Asintotica]]", "[[Protocolo-Experimental]]", "[[Grafos-Dijkstra-AStar]]"]
    },
    "04-Algoritmos/Clustering-DBSCAN-KMeans.md": {
        "titulo": "Clustering Espacial: DBSCAN y K-Means para Puntos Críticos",
        "tipo": "algoritmo",
        "abstract": "Algoritmos de agrupamiento espacial no supervisado (DBSCAN y K-Means) aplicados sobre densidades geográficas para delimitar puntos críticos viales.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Estructuras-Espaciales-KDTree]]", "[[Grafos-Dijkstra-AStar]]", "[[Pipeline-Limpieza]]"]
    },
    "04-Algoritmos/Estructuras-Espaciales-KDTree.md": {
        "titulo": "Estructuras de Datos Espaciales: KD-Tree 2D para Búsqueda Vecinal",
        "tipo": "algoritmo",
        "abstract": "Implementación y análisis de complejidad de un árbol k-dimensional (KD-Tree 2D) en Python puro para búsquedas eficientes del vecino más cercano en O(log n).",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Grafos-Dijkstra-AStar]]", "[[Clustering-DBSCAN-KMeans]]", "[[ADR-003-Geocodificacion-y-Enrutamiento-Continuo-Tipo-Google-Maps|ADR-003]]"]
    },
    "04-Algoritmos/Grafos-Dijkstra-AStar.md": {
        "titulo": "Teoría de Grafos y Enrutamiento Multiobjetivo (Dijkstra con Min-Heap)",
        "tipo": "algoritmo",
        "abstract": "Formulación formal del grafo vial ponderado y algoritmo de Dijkstra con cola de prioridad Min-Heap para cálculo de rutas multiobjetivo minimizando siniestralidad.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Estructuras-Espaciales-KDTree]]", "[[Laboratorio-Jerarquia-Asintotica]]", "[[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad|ADR-005]]", "[[Diseno-Backend-API]]"]
    },
    "04-Algoritmos/Laboratorio-Jerarquia-Asintotica.md": {
        "titulo": "Laboratorio de Jerarquía Asintótica: Demostración Empírica",
        "tipo": "algoritmo",
        "abstract": "Banco de pruebas en tiempo real que demuestra experimentalmente las 5 cotas de complejidad (O(1), O(log n), O(n), O(n log n), O(n²)) sobre el dataset vial real.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Protocolo-Experimental]]", "[[Algoritmos-Ordenamiento]]", "[[Grafos-Dijkstra-AStar]]", "[[Diseno-Backend-API]]"]
    },
    "04-Algoritmos/Protocolo-Experimental.md": {
        "titulo": "Protocolo Experimental de Benchmarking y Mitigación de Ruido",
        "tipo": "investigacion",
        "abstract": "Metodología experimental estandarizada: control de hardware, calentamiento de caché, réplicas estadísticas, métricas de tiempo/memoria y mitigación de ruido.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Laboratorio-Jerarquia-Asintotica]]", "[[Algoritmos-Ordenamiento]]", "[[ADR-004-Protocolo-Benchmarking-Masivo-y-Contraste-Asintotico|ADR-004]]"]
    },
    "05-Arquitectura-y-ADRs/ADR-001-Enfoque-Siniestros-y-Grafo-OSM.md": {
        "titulo": "ADR-001: Selección del Enfoque Híbrido (Siniestros MEData + Grafo OSM)",
        "tipo": "decision",
        "abstract": "Decisión arquitectónica para desacoplar el grafo topológico vial de OpenStreetMap y ponderar los arcos con la densidad de incidentes precomputada.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[ADR-002-Arquitectura-FastAPI-React|ADR-002]]", "[[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad|ADR-005]]", "[[Grafos-Dijkstra-AStar]]"]
    },
    "05-Arquitectura-y-ADRs/ADR-002-Arquitectura-FastAPI-React.md": {
        "titulo": "ADR-002: Arquitectura del Sistema (FastAPI Backend + React Leaflet UI)",
        "tipo": "decision",
        "abstract": "Selección del stack tecnológico desacoplado: backend asíncrono en FastAPI (Python) y frontend reactivo en React + Vite con Leaflet.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[ADR-001-Enfoque-Siniestros-y-Grafo-OSM|ADR-001]]", "[[Diseno-Backend-API]]", "[[Diseno-Frontend-UI]]"]
    },
    "05-Arquitectura-y-ADRs/ADR-003-Geocodificacion-y-Enrutamiento-Continuo-Tipo-Google-Maps.md": {
        "titulo": "ADR-003: Geocodificación Urbana Híbrida y Proyección Continua",
        "tipo": "decision",
        "abstract": "Estrategia de proyección continua de coordenadas arbitrarias del usuario hacia los nodos más cercanos del grafo vial mediante KD-Tree.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Estructuras-Espaciales-KDTree]]", "[[Grafos-Dijkstra-AStar]]", "[[Diseno-Backend-API]]"]
    },
    "05-Arquitectura-y-ADRs/ADR-004-Protocolo-Benchmarking-Masivo-y-Contraste-Asintotico.md": {
        "titulo": "ADR-004: Diseño e Implementación del Marco de Benchmarking Asintótico",
        "tipo": "decision",
        "abstract": "Diseño del marco de experimentación asintótica para garantizar repetibilidad estadística y contraste riguroso con modelos teóricos.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Protocolo-Experimental]]", "[[Laboratorio-Jerarquia-Asintotica]]", "[[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad|ADR-005]]"]
    },
    "05-Arquitectura-y-ADRs/ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad.md": {
        "titulo": "ADR-005: Replanteamiento del Alcance — Dijkstra Multiobjetivo y Laboratorio de Complejidad",
        "tipo": "decision",
        "abstract": "Decisión estratégica de concentrar el alcance del PPI en Dijkstra multiobjetivo con Min-Heap y el Laboratorio de Jerarquía Asintótica para una defensa técnica contundente.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Hoja-de-Ruta-Nuevo-Horizonte]]", "[[Grafos-Dijkstra-AStar]]", "[[Laboratorio-Jerarquia-Asintotica]]", "[[ADR-002-Arquitectura-FastAPI-React|ADR-002]]"]
    },
    "06-Backend-API/Diseno-Backend-API.md": {
        "titulo": "Especificación Formal de la Capa de Backend y API REST",
        "tipo": "api",
        "abstract": "Diseño modular de la API REST en FastAPI: esquemas Pydantic, routers versionados, manejo de errores y documentación Swagger/OpenAPI.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[ADR-002-Arquitectura-FastAPI-React|ADR-002]]", "[[Grafos-Dijkstra-AStar]]", "[[Diseno-Frontend-UI]]", "[[Plan-Pruebas-QA]]"]
    },
    "07-Frontend/Diseno-Frontend-UI.md": {
        "titulo": "Diseño de Interfaz de Usuario (UI/UX) y Componentes Frontend",
        "tipo": "componente",
        "abstract": "Arquitectura de componentes de la interfaz de usuario en React, visualización de rutas sobre mapa interactivo Leaflet y gráficos de complejidad.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Diseno-Backend-API]]", "[[Manual-Usuario-Prototipo]]", "[[ADR-002-Arquitectura-FastAPI-React|ADR-002]]"]
    },
    "08-QA/Plan-Pruebas-QA.md": {
        "titulo": "Plan Integral de Pruebas Automatizadas y Aseguramiento de Calidad",
        "tipo": "qa",
        "abstract": "Estrategia y plan maestro de pruebas: cobertura de lógica algorítmica, contratos de API, pruebas de estrés y validación de casos borde.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Reporte-Final-QA-Fase5]]", "[[Reporte-Pruebas-QA]]", "[[Matriz-Requisitos]]"]
    },
    "08-QA/Reporte-Final-QA-Fase5.md": {
        "titulo": "Certificación Oficial de Calidad del Software — Suite Pytest Fase 5",
        "tipo": "qa",
        "abstract": "Certificación final de calidad del software: ejecución exitosa de 44 de 44 pruebas automatizadas en Pytest (100% PASS en 8.31s) sin regresiones.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Plan-Pruebas-QA]]", "[[Reporte-Pruebas-QA]]", "[[Matriz-Requisitos]]", "[[Conclusiones-y-Resultados]]"]
    },
    "08-QA/Reporte-Pruebas-QA.md": {
        "titulo": "Reporte de Aseguramiento de Calidad y Pruebas Unitarias/Integración",
        "tipo": "qa",
        "abstract": "Reporte detallado de pruebas unitarias y de integración para algoritmos de ordenamiento, estructuras espaciales y servicios web.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Plan-Pruebas-QA]]", "[[Reporte-Final-QA-Fase5]]"]
    },
    "09-Resultados-y-conclusiones/Conclusiones-y-Resultados.md": {
        "titulo": "Conclusiones Generales, Específicas e Impacto del Proyecto",
        "tipo": "resumen",
        "abstract": "Análisis final de resultados del proyecto: reducción demostrada de exposición a puntos críticos en un 64% y cumplimiento pleno de los objetivos del PPI.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Guion-Sustentacion-Oral]]", "[[Manual-Usuario-Prototipo]]", "[[Reporte-Final-QA-Fase5]]"]
    },
    "09-Resultados-y-conclusiones/Guion-Sustentacion-Oral.md": {
        "titulo": "Guion Metodológico para la Sustentación Oral ante el Tribunal",
        "tipo": "guia",
        "abstract": "Guion paso a paso para la defensa oral ante el tribunal evaluador: distribución de tiempos, oradores, diapositivas y demostración en vivo.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Conclusiones-y-Resultados]]", "[[Manual-Usuario-Prototipo]]", "[[Hoja-de-Ruta-Nuevo-Horizonte]]"]
    },
    "09-Resultados-y-conclusiones/Manual-Usuario-Prototipo.md": {
        "titulo": "Manual de Usuario y Guía de Operación del Prototipo",
        "tipo": "guia",
        "abstract": "Guía práctica para usuarios finales y evaluadores: instalación local, arranque del servidor, selección de rutas seguras y uso del laboratorio.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[Diseno-Frontend-UI]]", "[[Diseno-Backend-API]]", "[[Guion-Sustentacion-Oral]]"]
    },
    "Plantillas/Plantilla-ADR.md": {
        "titulo": "Plantilla Estándar para Decisiones Arquitectónicas (ADR)",
        "tipo": "plantilla",
        "abstract": "Plantilla estandarizada para el registro de decisiones arquitectónicas de software siguiendo el formato MADR / Nygard.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[MOC-Principal]]", "[[Plantilla-Algoritmo]]"]
    },
    "Plantillas/Plantilla-Algoritmo.md": {
        "titulo": "Plantilla Estándar para Especificación de Algoritmos",
        "tipo": "plantilla",
        "abstract": "Estructura base para documentar formalmente la correctitud, pseudocódigo y complejidad asintótica de nuevos algoritmos.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[MOC-Principal]]", "[[Plantilla-ADR]]"]
    },
    "Plantillas/Plantilla-Modulo.md": {
        "titulo": "Plantilla Estándar para Especificación de Módulos de Software",
        "tipo": "plantilla",
        "abstract": "Plantilla estándar para la especificación técnica de módulos de software, dependencias y contratos de interfaz.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[MOC-Principal]]", "[[Plantilla-QA]]"]
    },
    "Plantillas/Plantilla-QA.md": {
        "titulo": "Plantilla Estándar para Casos de Prueba Automatizados",
        "tipo": "plantilla",
        "abstract": "Formato base para el diseño y documentación de casos de prueba automatizados y criterios de aceptación.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[MOC-Principal]]", "[[Plantilla-Modulo]]"]
    },
    "Plantillas/Plantilla-Requisito.md": {
        "titulo": "Plantilla Estándar para Especificación de Requisitos",
        "tipo": "plantilla",
        "abstract": "Plantilla estándar para la especificación funcional de requisitos de software con criterios de verificación.",
        "rel": ["[[00 - Inicio|Inicio]]", "[[MOC-Principal]]", "[[Plantilla-QA]]"]
    }
}

def procesar_nota(rel_path, meta):
    ruta = VAULT / rel_path.replace("/", os.sep)
    if not ruta.is_file():
        print(f"WARN: No existe {ruta}")
        return

    texto = ruta.read_text(encoding="utf-8")
    
    # 1. Separar frontmatter y cuerpo
    fm_raw = ""
    cuerpo = texto
    if texto.startswith("---"):
        fin = texto.find("\n---", 3)
        if fin != -1:
            fm_raw = texto[3:fin].strip()
            cuerpo = texto[fin + 4:].lstrip("\r\n")

    # Extraer campos existentes como lista de lineas
    lineas_fm = fm_raw.splitlines() if fm_raw else []
    
    # Claves existentes
    claves_existentes = {}
    for i, l in enumerate(lineas_fm):
        m = re.match(r"^([A-Za-z0-9_\-]+)\s*:", l)
        if m:
            claves_existentes[m.group(1)] = i

    # Agregar o actualizar campos obligatorios
    # titulo
    if "titulo" not in claves_existentes:
        lineas_fm.insert(0, f'titulo: "{meta["titulo"]}"')
    else:
        # Si ya existe, dejarlo o actualizar si está vacío
        pass

    # tipo
    if "tipo" not in claves_existentes:
        lineas_fm.append(f'tipo: {meta["tipo"]}')
    else:
        # Asegurar tipo correcto
        idx = claves_existentes["tipo"]
        lineas_fm[idx] = f'tipo: {meta["tipo"]}'

    # estado
    if "estado" not in claves_existentes:
        lineas_fm.append("estado: vigente")

    # audiencia
    if "audiencia" not in claves_existentes:
        lineas_fm.append("audiencia: [negocio, tecnico]")

    # actualizado
    if "actualizado" not in claves_existentes:
        lineas_fm.append("actualizado: 2026-10-19")
    else:
        idx = claves_existentes["actualizado"]
        lineas_fm[idx] = "actualizado: 2026-10-19"

    # etiquetas
    if "etiquetas" not in claves_existentes:
        tag_tipo = meta["tipo"]
        lineas_fm.append(f"etiquetas: [tipo/{tag_tipo}, ppi/tdea, proyecto/aburrasegura]")

    nuevo_fm = "---\n" + "\n".join(lineas_fm) + "\n---\n\n"

    # 2. Abstract
    if "[!abstract]" not in cuerpo:
        # Encontrar primer H1
        m_h1 = re.search(r"^#\s+(.+)$", cuerpo, re.M)
        if m_h1:
            pos_fin_h1 = m_h1.end()
            abs_block = f"\n\n> [!abstract] En pocas palabras\n> {meta['abstract']}\n"
            cuerpo = cuerpo[:pos_fin_h1] + abs_block + cuerpo[pos_fin_h1:]
        else:
            abs_block = f"> [!abstract] En pocas palabras\n> {meta['abstract']}\n\n"
            cuerpo = abs_block + cuerpo

    # 3. Relacionado
    if "## 🔗 Relacionado" not in cuerpo and "## Relacionado" not in cuerpo:
        rel_links = "\n".join(f"- {r}" for r in meta["rel"])
        rel_block = f"\n\n---\n\n## 🔗 Relacionado\n{rel_links}\n"
        cuerpo = cuerpo.rstrip() + rel_block

    ruta.write_text(nuevo_fm + cuerpo, encoding="utf-8")
    print(f"OK: {rel_path}")

for rel, meta in METADATA.items():
    procesar_nota(rel, meta)
