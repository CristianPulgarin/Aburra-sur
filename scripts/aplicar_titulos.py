import os
import re
from pathlib import Path

VAULT = Path(r"D:\Proyecto Algoritmos\vault")

# Importar validador para verificar que leer_frontmatter lo acepte
import sys
sys.path.insert(0, r"D:\personal-config-IA\plugins\obsidian-docs\skills\documentar-proyecto-obsidian\scripts")
from validar_vault import leer_frontmatter, CAMPOS_OBLIGATORIOS

TITULOS = {
    "Archivo-Alcance-Anterior.md": "Archivo del Alcance Anterior y Auditoría de Integridad",
    "Hoja-de-Ruta-Nuevo-Horizonte.md": "Hoja de Ruta — Horizonte Consolidado del PPI",
    "MOC-Principal.md": "Map of Content (MOC) Principal — Proyecto PPI AburráSegura",
    "Estado-Documento-Institucional.md": "Estado Integral del Documento Institucional (AburráSegura.docx)",
    "Matriz-Requisitos.md": "Matriz Integral de Requisitos y Trazabilidad (v4.1 Definitiva)",
    "Registro-Actualizaciones.md": "Registro Formal de Actualizaciones del Documento Institucional (Tabla 0)",
    "Antecedentes-Academicos.md": "Antecedentes Académicos y Estado del Arte",
    "Fuentes-y-Matriz-Decision.md": "Fuentes de Datos y Matriz de Decisión Multicriterio",
    "Referencias-APA7.md": "Referencias Bibliográficas Canónicas (Normas APA 7ma Edición)",
    "Diccionario-Variables.md": "Diccionario Canónico de Datos y Análisis Exploratorio de Siniestralidad",
    "Pipeline-Limpieza.md": "Pipeline de Ingesta, Limpieza Geoespacial y Particionamiento",
    "Algoritmos-Ordenamiento.md": "Algoritmos de Ordenamiento: Análisis Asintótico y Comparativa",
    "Clustering-DBSCAN-KMeans.md": "Clustering Espacial: DBSCAN y K-Means para Puntos Críticos",
    "Estructuras-Espaciales-KDTree.md": "Estructuras de Datos Espaciales: KD-Tree 2D para Búsqueda Vecinal",
    "Grafos-Dijkstra-AStar.md": "Teoría de Grafos y Enrutamiento Multiobjetivo (Dijkstra con Min-Heap)",
    "Laboratorio-Jerarquia-Asintotica.md": "Laboratorio de Jerarquía Asintótica: Demostración Empírica",
    "Protocolo-Experimental.md": "Protocolo Experimental de Benchmarking y Mitigación de Ruido",
    "ADR-001-Enfoque-Siniestros-y-Grafo-OSM.md": "ADR-001: Selección del Enfoque Híbrido (Siniestros MEData + Grafo OSM)",
    "ADR-002-Arquitectura-FastAPI-React.md": "ADR-002: Arquitectura del Sistema (FastAPI Backend + React Leaflet UI)",
    "ADR-003-Geocodificacion-y-Enrutamiento-Continuo-Tipo-Google-Maps.md": "ADR-003: Geocodificación Urbana Híbrida y Proyección Continua",
    "ADR-004-Protocolo-Benchmarking-Masivo-y-Contraste-Asintotico.md": "ADR-004: Diseño e Implementación del Marco de Benchmarking Asintótico",
    "ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad.md": "ADR-005: Replanteamiento del Alcance — Dijkstra Multiobjetivo y Laboratorio de Complejidad",
    "Diseno-Backend-API.md": "Especificación Formal de la Capa de Backend y API REST",
    "Diseno-Frontend-UI.md": "Diseño de Interfaz de Usuario (UI/UX) y Componentes Frontend",
    "Plan-Pruebas-QA.md": "Plan Integral de Pruebas Automatizadas y Aseguramiento de Calidad",
    "Reporte-Final-QA-Fase5.md": "Certificación Oficial de Calidad del Software — Suite Pytest Fase 5",
    "Reporte-Pruebas-QA.md": "Reporte de Aseguramiento de Calidad y Pruebas Unitarias/Integración",
    "Conclusiones-y-Resultados.md": "Conclusiones Generales, Específicas e Impacto del Proyecto",
    "Guion-Sustentacion-Oral.md": "Guion Metodológico para la Sustentación Oral ante el Tribunal",
    "Manual-Usuario-Prototipo.md": "Manual de Usuario y Guía de Operación del Prototipo",
    "Plantilla-ADR.md": "Plantilla Estándar para Decisiones Arquitectónicas (ADR)",
    "Plantilla-Algoritmo.md": "Plantilla Estándar para Especificación de Algoritmos",
    "Plantilla-Modulo.md": "Plantilla Estándar para Especificación de Módulos de Software",
    "Plantilla-QA.md": "Plantilla Estándar para Casos de Prueba Automatizados",
    "Plantilla-Requisito.md": "Plantilla Estándar para Especificación de Requisitos",
    "00 - Inicio.md": "AburráSegura",
    "Historial de cambios.md": "Historial de cambios"
}

def reparar_archivo(p):
    texto = p.read_text(encoding="utf-8")
    fm, cuerpo = leer_frontmatter(texto)
    if fm is None:
        print(f"ERROR: {p.name} sin frontmatter")
        return

    faltan = [c for c in CAMPOS_OBLIGATORIOS if c not in fm]
    if not faltan:
        return

    # Obtener fin del frontmatter
    fin = texto.find("\n---", 3)
    bloque = texto[3:fin].strip()
    lineas = bloque.splitlines()

    # Si falta titulo:
    if "titulo" in faltan:
        tit = TITULOS.get(p.name, p.stem)
        lineas.insert(0, f'titulo: "{tit}"')

    # Si falta tipo:
    if "tipo" in faltan:
        lineas.append("tipo: resumen")

    # Si falta estado:
    if "estado" in faltan:
        lineas.append("estado: vigente")

    # Si falta audiencia:
    if "audiencia" in faltan:
        lineas.append("audiencia: [negocio, tecnico]")

    # Si falta actualizado:
    if "actualizado" in faltan:
        lineas.append("actualizado: 2026-10-19")

    # Si falta etiquetas:
    if "etiquetas" in faltan:
        lineas.append("etiquetas: [tipo/general, ppi/tdea, proyecto/aburrasegura]")

    nuevo_texto = "---\n" + "\n".join(lineas) + "\n---\n" + texto[fin + 4:]
    p.write_text(nuevo_texto, encoding="utf-8")
    
    # Verificar
    fm_check, _ = leer_frontmatter(nuevo_texto)
    faltan_post = [c for c in CAMPOS_OBLIGATORIOS if c not in fm_check]
    print(f"Reparado: {p.name} -> faltan ahora: {faltan_post}")

for p in VAULT.rglob("*.md"):
    if not any(part.startswith(".") for part in p.relative_to(VAULT).parts):
        reparar_archivo(p)
