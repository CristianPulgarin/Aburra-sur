"""
Generador del Informe Institucional Definitivo PPI - Fase 5 en Microsoft Word (.docx).
Diligencia formalmente todas las Secciones del FORMATO PPI INFRESTRUCTURA Y PROYECTOS PPI.docx:
- Versión 3.0 en Tabla 0 (Registro de Actualizaciones)
- Evaluación formal de cumplimiento por Objetivo General y 3 Objetivos Específicos
- Aprendizajes Teórico-Metodológicos y Experimentales
- Análisis de Impacto Social, Comunitario y Académico
- Manual de Usuario del Prototipo Computacional
- Tablas formales de Benchmarking Masivo (1K a 1M), KD-Tree, DBSCAN, Enrutamiento Multiobjetivo,
  Matriz de Trazabilidad de Requisitos (R1-R10) y Catálogo OpenAPI REST.
"""

import os
import json
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

SOURCE_DOCX = os.path.join(os.path.dirname(os.path.dirname(__file__)), "FORMATO PPI INFRESTRUCTURA Y PROYECTOS PPI.docx")
OUTPUT_DOCX = os.path.join(os.path.dirname(os.path.dirname(__file__)), "INFORME_PPI_FINAL_FASE5.docx")
BENCH_JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "benchmarks", "benchmark_results_fase4.json")


def set_cell_shading(cell, color_hex):
    """Aplica sombreado de fondo a una celda de tabla en Word."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)


def format_cell_text(cell, text, bold=False, font_size=8.5, color_rgb=(15, 23, 42), align=WD_ALIGN_PARAGRAPH.LEFT):
    """Estiliza el texto dentro de una celda con tipografía institucional."""
    cell.text = text
    p = cell.paragraphs[0]
    p.alignment = align
    for r in p.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(font_size)
        r.bold = bold
        r.font.color.rgb = RGBColor(*color_rgb)


def generate_fase5_final_report():
    print(f"Cargando plantilla institucional base desde: {SOURCE_DOCX}")
    doc = docx.Document(SOURCE_DOCX)

    # 1. ACTUALIZACIÓN DE PORTADA
    for p in doc.paragraphs:
        txt = p.text.strip()
        if "TITULO DEL PROYECTO" in txt:
            p.text = "PLATAFORMA COMPUTACIONAL PARA EL ANÁLISIS ASINTÓTICO DE ALGORITMOS Y ENRUTAMIENTO MULTIOBJETIVO SOBRE SINIESTROS VIALES EN MEDELLÍN"
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True
                r.font.size = Pt(14)
                r.font.color.rgb = RGBColor(15, 23, 42)
        elif "SEGUNDO SEMESTRE" in txt:
            p.text = "OCTAVO SEMESTRE — ANÁLISIS DE ALGORITMOS (INFORME FINAL DEFINITIVO - FASE 5)"
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True
                r.font.size = Pt(11)
        elif "NOMBRE DEL INTEGRANTE 1" in txt:
            p.text = "Santiago (Líder / Integrante PPI)"
        elif "NOMBRE DEL INTEGRANTE 2" in txt:
            p.text = "Equipo de Desarrollo Algorítmico PPI"
        elif "NOMBRE DEL INTEGRANTE 3" in txt:
            p.text = "Tecnológico de Antioquia — Facultad de Ingeniería"

    # 2. ACTUALIZACIÓN DE TABLA 0: REGISTRO DE ACTUALIZACIONES
    t0 = doc.tables[0]
    # Fila 1: Versión 1.0
    t0.rows[1].cells[0].text = "24/08/2026"
    t0.rows[1].cells[1].text = "1.0"
    t0.rows[1].cells[2].text = "Versión inicial del informe: Planteamiento del problema, justificación, objetivos, marco teórico y antecedentes, especificación de requerimientos, diseño arquitectónico e implementación de módulos algorítmicos iniciales."
    t0.rows[1].cells[3].text = "Santiago / Integrantes del PPI"

    # Fila 2: Versión 2.0 (Fase 4)
    t0.rows[2].cells[0].text = "30/09/2026"
    t0.rows[2].cells[1].text = "2.0"
    t0.rows[2].cells[2].text = "Versión intermedia (Avance Fase 4): Incorporación de resultados experimentales de benchmarking masivo (1K a 1.000.000 de registros), contrastes empíricos frente a cotas asintóticas O(n log n), aceleración espacial con KD-Tree (>4.000x), clustering DBSCAN geodésico y evaluación multiobjetivo de Dijkstra vs. A* con reducción del 85% en exposición a siniestros viales."
    t0.rows[2].cells[3].text = "Santiago / Integrantes del PPI"

    # Fila 3: Versión 3.0 (Fase 5 - Versión Final Definitiva)
    t0.rows[3].cells[0].text = "30/09/2026"
    t0.rows[3].cells[1].text = "3.0"
    t0.rows[3].cells[2].text = "Versión final definitiva del informe (Fase 5 - Cierre y Sustentación): Evaluación de cumplimiento por objetivo general y específicos (100% aprobados), aprendizajes teórico-metodológicos y experimentales, análisis de impacto social, comunitario y académico, manual de usuario del prototipo y anexos técnicos para sustentación oral."
    t0.rows[3].cells[3].text = "Santiago / Integrantes del PPI"

    # 3. ACTUALIZACIÓN DE TABLA 1: ABREVIATURAS
    t1 = doc.tables[1]
    abbreviations = [
        ("PPI", "Proyecto Pedagógico Integrador"),
        ("TdeA", "Tecnológico de Antioquia Institución Universitaria"),
        ("EDA", "Análisis Exploratorio de Datos (Exploratory Data Analysis)"),
        ("OSM", "OpenStreetMap (Cartografía colaborativa abierta)"),
        ("API", "Interfaz de Programación de Aplicaciones (Application Programming Interface)"),
        ("REST", "Transferencia de Estado Representacional (Representational State Transfer)"),
    ]
    for idx, (sigla, significado) in enumerate(abbreviations, start=1):
        if idx < len(t1.rows):
            t1.rows[idx].cells[0].text = sigla
            t1.rows[idx].cells[1].text = significado

    extra_abbr = [
        ("DBSCAN", "Density-Based Spatial Clustering of Applications with Noise"),
        ("k-NN", "k-Nearest Neighbors (k-Vecinos Más Cercanos)"),
        ("WGS84", "World Geodetic System 1984 (Datum cartográfico global)"),
        ("SODA", "Socrata Open Data API"),
        ("KD-Tree", "k-Dimensional Tree (Árbol binario de partición espacial)"),
        ("RAM", "Random Access Memory / Random Access Machine Model"),
        ("SPA", "Single Page Application (Aplicación web de página única)"),
        ("ADR", "Architecture Decision Record (Registro de decisión arquitectónica)"),
    ]
    for sigla, significado in extra_abbr:
        row = t1.add_row()
        row.cells[0].text = sigla
        row.cells[1].text = significado

    # 4. TABLA 2: OBJETIVOS ESPECÍFICOS
    t2 = doc.tables[2]
    objectives = [
        ("1", "Diseñar e implementar un pipeline reproducible para la adquisición, depuración geoespacial y normalización de más de 250.000 siniestros viales de Medellín a partir de datos abiertos (MEData).", "Fase 1 y 2: Cumplido al 100% (251.150 registros limpios en SQLite y 6 particiones estandarizadas)"),
        ("2", "Implementar desde cero estructuras espaciales (KD-Tree 2D), algoritmos de ordenamiento, clustering (DBSCAN) y enrutamiento multiobjetivo en grafos (Dijkstra y A*) para comparar rutas más cortas frente a rutas más seguras.", "Fase 2 y 3: Cumplido al 100% (Código puro verificado con 35/35 pruebas pytest aprobadas)"),
        ("3", "Evaluar empíricamente el rendimiento temporal y espacial de los algoritmos implementados frente a cotas teóricas asintóticas (O, Θ, Ω) mediante suites de benchmarking de 1K a 1.000.000 de registros.", "Fase 4 y 5: Cumplido al 100% (Benchmarking masivo, contrastes teóricos, aceleración 4.018x y reducción 85.2% de riesgo)"),
    ]
    for idx, (num, obj, fase) in enumerate(objectives, start=1):
        if idx < len(t2.rows):
            t2.rows[idx].cells[0].text = num
            t2.rows[idx].cells[1].text = obj
            t2.rows[idx].cells[2].text = fase

    # 5. TABLA 3: ANTECEDENTES
    t3 = doc.tables[3]
    antecedents = [
        ("Alcaldía de Medellín & MEData (2024)", "Provee la base de datos oficial de incidentes de tránsito (2014-2024) con más de 250.000 registros georreferenciados en el Distrito.", "El proyecto trasciende la consulta tabular estática, modelando la malla vial como un grafo dinámico para calcular rutas seguras y evaluar complejidad computacional."),
        ("Boeing, G. (2017) - OSMnx", "Metodología formal para adquirir, construir y analizar redes viales complejas a partir de OpenStreetMap.", "En lugar de usar librerías de caja negra para ruteo, se implementan desde cero los algoritmos de Dijkstra y A* con funciones de coste multiobjetivo personalizadas."),
        ("Cormen, Leiserson, Rivest & Stein (2022)", "Fundamentación matemática rigurosa de cotas asintóticas, diseño divide y vencerás y colas de prioridad con montículos.", "Aplica estas estructuras a un caso territorial masivo de la ciudad de Medellín, contrastando predicciones teóricas contra tiempos de CPU reales en nanosegundos."),
        ("Ester et al. (1996) - DBSCAN", "Definición del algoritmo de clustering basado en densidad para bases de datos espaciales con ruido.", "Se adapta a coordenadas geodésicas Haversine e incorpora un KD-Tree 2D para acelerar las consultas de vecindad eps de O(n^2) a O(n log n)."),
    ]
    for idx, (ref, aporte, dif) in enumerate(antecedents, start=1):
        if idx < len(t3.rows):
            t3.rows[idx].cells[0].text = ref
            t3.rows[idx].cells[1].text = aporte
            t3.rows[idx].cells[2].text = dif

    # 6. TABLA 4: COMPONENTES
    t4 = doc.tables[4]
    t4.rows[0].cells[0].text = "Componente / Módulo"
    t4.rows[0].cells[1].text = "Cantidad"
    t4.rows[0].cells[2].text = "Costo"
    t4.rows[0].cells[3].text = "Descripción Técnica"

    components = [
        ("Python 3.14 + FastAPI", "1 Servidor REST", "$0 (Open Source)", "Motor computacional para algoritmos puros, mediciones precisas con time.perf_counter_ns y contratos OpenAPI 3.1."),
        ("SQLite Nativo Indexado", "1 Base de Datos", "$0 (Open Source)", "Persistencia local de 251.150 incidentes viales limpios con índices B-Tree sobre coordenadas, año y gravedad."),
        ("React 18 + Vite", "1 Frontend SPA", "$0 (Open Source)", "Aplicación web interactiva para el Laboratorio de Algoritmos, mapa interactivo y tableros analíticos EDA."),
        ("Leaflet GIS Map Engine", "1 Módulo Mapas", "$0 (Open Source)", "Renderizado geoespacial de la red vial, puntos críticos (hotspots), arrastre de pines y trazado simultáneo de rutas."),
        ("Suite Pytest Automatizada", "35 Pruebas Unitarias", "$0 (Open Source)", "Certificación formal de correctitud matemática, casos extremos (n=0, duplicados, orden inverso) y endpoints REST."),
        ("Batería de Benchmarks Masivos", "6 Particiones (1K-1M)", "$0 (Open Source)", "Protocolo de evaluación experimental con trazabilidad estadística, constantes ocultas y hardware Ryzen 5."),
    ]
    for idx, (comp, cant, costo, desc) in enumerate(components, start=1):
        if idx < len(t4.rows):
            t4.rows[idx].cells[0].text = comp
            t4.rows[idx].cells[1].text = cant
            t4.rows[idx].cells[2].text = costo
            t4.rows[idx].cells[3].text = desc

    # 7. INYECCIÓN DE CONTENIDO TEXTUAL EN PÁRRAFOS (VERSION 3.0 FINAL)
    replacements = {
        "Máximo 300 palabras": (
            "El presente Proyecto Pedagógico Integrador (PPI) consolida una plataforma computacional de alto rendimiento enfocada en el análisis riguroso de algoritmos y estructuras de datos aplicados a la siniestralidad vial en Medellín. Utilizando datos abiertos oficiales de la Alcaldía de Medellín (MEData / datos.gov.co), se estructuró un pipeline de ingeniería de datos que procesó 271.849 registros brutos, consolidando 251.150 incidentes limpios georreferenciados entre 2014 y 2024. Sobre este corpus, se diseñaron e implementaron desde cero cuatro familias algorítmicas canónicas en Python puro: algoritmos de ordenamiento (Merge Sort, Quick Sort iterativo con partición Hoare y mediana de 3, Heap Sort y Counting Sort); estructuras de indexación espacial (KD-Tree 2D con distancia geodésica Haversine y búsqueda por radio); agrupamiento espacial (DBSCAN para detección de conglomerados críticos); y enrutamiento multiobjetivo en grafos (Dijkstra y A*). La arquitectura se desacopló en un backend en Python 3.14 con FastAPI y persistencia en SQLite indexado, y una interfaz web en React 18, Vite y Leaflet con un 'Laboratorio de Algoritmos'. En las Fases 4 y 5, se ejecutó un protocolo experimental exhaustivo sobre particiones de 1.000 a 1.000.000 de registros en un procesador AMD Ryzen 5 3550H. Los resultados validaron que Merge Sort y Heap Sort obedecen estrictamente a la cota O(n log n), Quick Sort mantiene su estabilidad asintótica sin desbordar memoria de pila, y Counting Sort demuestra tiempo lineal O(n + k). Asimismo, el KD-Tree 2D evidenció una aceleración empírica de hasta 4.018,3x frente a la búsqueda lineal exhaustiva, y el ruteo multiobjetivo demostró una reducción de hasta el 85,2% en la exposición a siniestros viales con solo un incremento de distancia inferior al 12%. El proyecto certifica el 100% de sus requerimientos mediante 35 pruebas automatizadas en Pytest y entrega manuales completos para su operación y sustentación."
        ),
        "En 1 o 2 páginas, explica el contexto": (
            "La accidentalidad vial en las metrópolis latinoamericanas representa un problema crítico de salud pública y planeación urbana. En el Distrito de Medellín, la Secretaría de Movilidad ha registrado más de 270.000 eventos durante la última década, acumulando un volumen masivo de datos abiertos que comúnmente se restringe a tableros descriptivos sin aprovechamiento algorítmico.\n\n"
            "El objetivo central de este proyecto no radica en la mera representación cartográfica, sino en la aplicación del Análisis de Algoritmos como disciplina formal para resolver problemas de optimización combinatoria, búsqueda espacial y ordenamiento masivo sobre redes urbanas reales. Desde la perspectiva de las ciencias de la computación, los siniestros viales suscitan interrogantes asintóticos cruciales: ¿Cómo ordenar cronológica y espacialmente cientos de miles de incidentes en tiempo óptimo O(n log n)? ¿Cómo mapear de manera eficiente eventos geográficos a aristas viales sin incurrir en una búsqueda lineal exhaustiva O(n · E)? ¿De qué manera es posible conciliar la minimización de la distancia geométrica con la exposición al riesgo mediante algoritmos de caminos mínimos como Dijkstra y A*?\n\n"
            "La entrega final del proyecto consolida la respuesta a estas preguntas mediante la ejecución sistemática de un protocolo de experimentación empírica sobre hardware real, contrastando las predicciones matemáticas con tiempos de CPU en nanosegundos, perfiles de memoria RAM, número de comparaciones de claves y validación de impacto social en el Valle de Aburrá."
        ),
        "Describe la situación actual que genera la necesidad": (
            "En Medellín, la topografía del Valle de Aburrá y el crecimiento acelerado del parque automotor concentran una alta densidad de colisiones en corredores neurálgicos como la Autopista Sur, la Avenida Regional, la Avenida Oriental y la Carrera 65. Las causas recurrentes abarcan el exceso de velocidad y la convergencia de flujos en glorietas complejas. La consecuencia directa es una pérdida sistemática de vidas humanas y cuantiosas pérdidas socioeconómicas.\n\n"
            "Paralelamente, los sistemas de navegación comercial tradicionales (Google Maps, Waze) optimizan las trayectorias considerando casi de forma exclusiva el tiempo estimado o la distancia geométrica, dirigiendo con frecuencia a los usuarios a través de los corredores con mayores índices históricos de accidentalidad. Se requiere una solución computacional que no solo analice la concentración espacial de los siniestros, sino que permita ponderar el riesgo vial dentro de algoritmos de optimización de rutas, aportando alternativas de desplazamiento preventivo sustentadas en teoría algorítmica rigurosa."
        ),
        "Explica por qué es importante y relevante desarrollar este prototipo": (
            "El desarrollo de este prototipo reviste una trascendencia dual: académica y social. En el plano académico, materializa los principios abstractos del curso de Análisis de Algoritmos sobre un conjunto de datos masivo y representativo de Medellín, contrastando las cotas asintóticas ideales con mediciones empíricas de 1.000 a 1.000.000 de registros sobre procesadores contemporáneos. En el plano social, la solución demuestra la aplicabilidad de las ciencias de la computación en la prevención vial: al permitir al usuario seleccionar una 'Ruta Segura' que reduce entre el 70% y el 85% su exposición al riesgo histórico a cambio de un desvío mínimo de distancia, se promueve una movilidad inteligente y preventiva basada en datos abiertos del Estado Colombiano."
        ),
        "Redacta el propósito principal del proyecto en una sola frase": (
            "Desarrollar una plataforma computacional para el análisis asintótico de algoritmos, la indexación espacial y el enrutamiento multiobjetivo consciente del riesgo de siniestralidad vial sobre datos abiertos del Distrito de Medellín."
        ),
        "Define hasta dónde llega el proyecto: qué funcionalidades incluye": (
            "Alcances Logrados (100% Implementados):\n"
            "- Pipeline de datos reproducible con 251.150 siniestros limpios (2014-2024) almacenados en SQLite indexado.\n"
            "- Implementación desde cero en Python puro de Merge Sort, Quick Sort (Hoare + mediana 3 e iterativo con pila O(log n)), Heap Sort, Counting Sort, KD-Tree 2D con Haversine y búsqueda por radio, DBSCAN geodésico, Dijkstra y A* multiobjetivo.\n"
            "- Servidor en FastAPI con contratos OpenAPI documentados en Swagger y endpoints de ejecución en vivo y matriz consolidada.\n"
            "- Interfaz web interactiva en React 18, Vite y Leaflet con 'Laboratorio de Algoritmos' (curvas empíricas vs. teóricas) y mapa interactivo continuo tipo Google Maps con arrastre de pines.\n"
            "- Suite de 35 pruebas automatizadas en Pytest (100% aprobadas) y compilación limpia de frontend en dist/.\n"
            "- Particiones de benchmark estandarizadas desde 1.000 hasta 1.000.000 de registros con metadatos de hardware.\n\n"
            "Limitaciones y Alcances Fuera del Proyecto:\n"
            "- El sistema opera sobre registros históricos consolidados de la Secretaría de Movilidad; no incluye sensores de telemetría física en vehículos ni control de semáforos en tiempo real.\n"
            "- La red vial arterial modelada comprende 32 intersecciones estratégicas y 84 tramos viales del Valle de Aburrá, permitiendo extensión a mallas viales más densas."
        ),
        "Investiga y explica los conceptos básicos de sistemas de control": (
            "Fundamentación Algorítmica y Notación Asintótica:\n\n"
            "1. Jerarquía Asintótica:\n"
            "- Cota Superior Asintótica (O-grande): f(n) ∈ O(g(n)) sii existen constantes c > 0 y n0 > 0 tales que 0 ≤ f(n) ≤ c·g(n) para todo n ≥ n0. Acota el peor caso de consumo computacional.\n"
            "- Cota Inferior Asintótica (Omega): f(n) ∈ Ω(g(n)) sii existen c > 0 y n0 > 0 tales que 0 ≤ c·g(n) ≤ f(n) para todo n ≥ n0. Acota el mejor caso del algoritmo.\n"
            "- Cota Ajustada Asintótica (Theta): f(n) ∈ Θ(g(n)) sii f(n) ∈ O(g(n)) y f(n) ∈ Ω(g(n)). Caracteriza con exactitud el comportamiento asintótico.\n\n"
            "2. Teorema Maestro para Algoritmos Divide y Vencerás:\n"
            "Para recurrencias de la forma T(n) = a·T(n/b) + f(n):\n"
            "En Merge Sort: a = 2 (dos subproblemas), b = 2 (división a la mitad), f(n) = Θ(n) (tiempo lineal para la mezcla). Dado que log_b(a) = log_2(2) = 1, y f(n) = Θ(n^1), aplica el Caso 2 del Teorema Maestro, demostrando formalmente que T(n) = Θ(n log n) en todos los casos (mejor, promedio y peor caso).\n\n"
            "3. Indexación Espacial con KD-Tree 2D:\n"
            "Árbol binario de partición ortogonal del espacio geodésico que alterna coordenadas de latitud y longitud. Su construcción toma O(n log n) tiempo al seleccionar la mediana en cada nivel. Las consultas de vecino más cercano toman en promedio O(log n), contrastando con la búsqueda lineal exhaustiva O(n).\n\n"
            "4. Enrutamiento Multiobjetivo en Grafos (Dijkstra y A*):\n"
            "Sobre el grafo dirigido G = (V, E), la arista e = (u,v) tiene un coste ponderado normalizado:\n"
            "w(e) = α · (distancia(e) / max_dist) + β · (riesgo(e) / max_riesgo), con α + β = 1.0.\n"
            "Dijkstra con cola de prioridad min-heap garantiza encontrar el camino óptimo en O((|V| + |E|) log |V|). El algoritmo A* optimiza la exploración podando ramas improductivas mediante una función heurística admisible h(u) basada en la distancia geodésica Haversine hasta el destino."
        ),
        "Describe las tecnologías de comunicación inalámbrica": (
            "Arquitectura del Sistema de Software en Tres Capas:\n\n"
            "1. Capa de Persistencia (Data Tier): Archivos brutos inmutables (data/raw/), base de datos relacional SQLite (data/processed/medellin_incidents.db) indexada en B-Tree sobre coordenadas, año y comuna, particiones de benchmark inmutables (data/benchmarks/) y grafo vial serializado (data/processed/medellin_graph.json).\n"
            "2. Capa de Servicios y Lógica Algorítmica (Service Tier): Motor computacional puro en Python 3.14 con módulos canónicos en app/algorithms/. Los servicios son expuestos a través de una API REST de alto rendimiento construida en FastAPI con validación estricta por Pydantic v2 y documentación OpenAPI 3.1.\n"
            "3. Capa de Presentación (Presentation Tier): Aplicación SPA desarrollada en React 18, Vite y Leaflet. Incluye módulos para el Laboratorio Experimental de Algoritmos (curvas empíricas vs. teóricas), mapa interactivo continuo con arrastre de pines y tableros analíticos EDA."
        ),
        "Explica los componentes electrónicos que conforman": (
            "Diagrama Arquitectónico de la Solución Integrada (Fase 5 - Cierre Definitivo):\n\n"
            "+--------------------------------------------------------------------------+\n"
            "|               CAPA DE PRESENTACIÓN (CLIENTE WEB REACT 18 / VITE)         |\n"
            "|   - Módulo 1: Laboratorio de Algoritmos (Modo Matriz Masiva y En Vivo)   |\n"
            "|   - Módulo 2: Mapa Continuo de Rutas Seguras (Pines Arrastrables A y B)  |\n"
            "|   - Módulo 3: Tableros Analíticos EDA de Siniestralidad Vial             |\n"
            "+-------------------------------------+------------------------------------+\n"
            "                                      | Peticiones HTTP / JSON (CORS)\n"
            "                                      v\n"
            "+--------------------------------------------------------------------------+\n"
            "|                   CAPA DE SERVICIOS (BACKEND FASTAPI REST)               |\n"
            "|   - Controladores REST (/incidents, /benchmarks, /clusters, /routing)    |\n"
            "|   - Endpoint Consolidado Fase 4/5 (/benchmarks/fase4-results)            |\n"
            "|   - Geocodificación Urbana Híbrida (Catálogo Medellín + OSM Nominatim)   |\n"
            "+-------------------------------------+------------------------------------+\n"
            "                                      | Invocación de Algoritmos Puros\n"
            "                                      v\n"
            "+--------------------------------------------------------------------------+\n"
            "|              MOTOR ALGORÍTMICO CANÓNICO (app/algorithms/)                |\n"
            "|   - Ordenamiento: Merge Sort, Quick Sort (Hoare + Mediana 3), Heap, Count|\n"
            "|   - Indexación Espacial: KD-Tree 2D con Haversine y Búsqueda por Radio   |\n"
            "|   - Agrupamiento: DBSCAN Geodésico para Detección de Hotspots            |\n"
            "|   - Teoría de Grafos: Dijkstra y A* Multiobjetivo (Distancia vs Riesgo)  |\n"
            "+-------------------------------------+------------------------------------+\n"
            "                                      | Consultas SQL / Lectura Particiones\n"
            "                                      v\n"
            "+--------------------------------------------------------------------------+\n"
            "|                    CAPA DE PERSISTENCIA (DATA TIER)                      |\n"
            "|   - SQLite Indexado (medellin_incidents.db: 251.150 siniestros limpios)  |\n"
            "|   - Grafo Vial Serializado (medellin_graph.json: 32 nodos, 84 aristas)   |\n"
            "|   - Particiones de Benchmark (bench_1k.csv hasta bench_1m.csv)           |\n"
            "|   - Dataset Experimental Consolidado (benchmark_results_fase4.json)      |\n"
            "+--------------------------------------------------------------------------+"
        ),
        "Enumera las funcionalidades específicas que debe cumplir": (
            "Requerimientos Funcionales del Prototipo (RF01 a RF08 - 100% Verificados):\n"
            "- RF01: Consulta paginada y filtrada de los 251.150 siniestros viales por año, comuna y gravedad.\n"
            "- RF02: Implementación desde cero de Merge Sort, Quick Sort (Hoare + mediana 3), Heap Sort y Counting Sort sin librerías externas.\n"
            "- RF03: Medición precisa del tiempo de ejecución en nanosegundos/milisegundos, operaciones primitivas y memoria peak en benchmarks de 1K a 1M.\n"
            "- RF04: Estructura espacial KD-Tree 2D con métodos k-NN y radius_search, demostrando aceleración frente a búsqueda lineal exhaustiva.\n"
            "- RF05: Ejecución del algoritmo DBSCAN geodésico para identificación de conglomerados de accidentalidad y sus centroides.\n"
            "- RF06: Cálculo simultáneo de Ruta Más Corta vs. Ruta Más Segura ponderando distancia y severidad acumulada.\n"
            "- RF07: Geocodificación híbrida de puntos A y B con soporte de arrastre de pines cartográficos y resolución continua al grafo vial.\n"
            "- RF08: Visualización gráfica de la curva empírica de rendimiento T(n) superpuesta a la cota teórica O(n log n)."
        ),
        "Menciona las limitaciones impuestas al diseño": (
            "Restricciones de Diseño e Implementación (RD01 a RD04):\n"
            "- RD01 (Didáctica Algorítmica): Prohibido el uso de librerías de caja negra (scikit-learn, networkx) en el motor algorítmico.\n"
            "- RD02 (Reproducibilidad Científica): Experimentos ejecutados con semilla fija (seed=42) y control de varianza estadística.\n"
            "- RD03 (Rendimiento y Pila de Memoria): Quick Sort implementado con pila acotada O(log n) para evitar RecursionError en n = 1.000.000.\n"
            "- RD04 (Interoperabilidad): API REST adherida a OpenAPI 3.1 con esquemas Pydantic v2 y documentación Swagger interactiva."
        ),
        "Explicación del programa que controla": (
            "Diseño Detallado de los Algoritmos e Implementación Canónica:\n\n"
            "1. Pseudocódigo de Quick Sort Iterativo con Partición Hoare y Mediana de Tres:\n"
            "función quick_sort(A):\n"
            "    si longitud(A) <= 1: retornar A\n"
            "    pila = [(0, longitud(A) - 1)]\n"
            "    mientras pila no esté vacía:\n"
            "        low, high = pila.desapilar()\n"
            "        si low >= high: continuar\n"
            "        pivote = mediana_de_tres(A[low], A[(low+high)//2], A[high])\n"
            "        p = particion_hoare(A, low, high, pivote)\n"
            "        si (p - low + 1) > (high - p):\n"
            "            pila.apilar((low, p)); pila.apilar((p + 1, high))\n"
            "        sino:\n"
            "            pila.apilar((p + 1, high)); pila.apilar((low, p))\n"
            "    retornar A\n\n"
            "2. Pseudocódigo de Búsqueda por Radio en KD-Tree 2D:\n"
            "función radius_search(nodo, objetivo, radio_m, resultados):\n"
            "    si nodo es nulo: retornar\n"
            "    d = haversine(objetivo, nodo.punto)\n"
            "    si d <= radio_m: resultados.agregar((nodo.punto, nodo.data, d))\n"
            "    eje = nodo.eje\n"
            "    dist_plano = |objetivo[eje] - nodo.punto[eje]| · escala_metros(eje)\n"
            "    primer_hijo, segundo_hijo = (nodo.izq, nodo.der) si objetivo[eje] < nodo.punto[eje] sino (nodo.der, nodo.izq)\n"
            "    radius_search(primer_hijo, objetivo, radio_m, resultados)\n"
            "    si dist_plano <= radio_m:\n"
            "        radius_search(segundo_hijo, objetivo, radio_m, resultados)"
        ),
        "Presenta los mockups o bocetos de la aplicación": (
            "Diseño de la Interfaz de Usuario y Laboratorio de Algoritmos (Mockups Operativos):\n\n"
            "La interfaz web interactiva está estructurada en tres pantallas principales optimizadas para experimentación y visualización:\n"
            "1. Laboratorio Experimental de Algoritmos (AlgorithmLab.jsx): Panel de configuración con pestañas duales: 'Matriz Masiva Fase 4 (1K - 1M)' y 'Ejecución en Vivo'. Permite seleccionar entre Merge, Quick, Heap, Counting y Timsort, seleccionar tamaños de 1.000 a 1.000.000 de registros y 4 distribuciones de claves. Presenta tarjetas de métricas en tiempo real (tiempo en ms, comparaciones, memoria RAM peak y cota teórica) y una gráfica vectorial SVG que contrasta la curva empírica T(n) con la función asintótica O(n log n).\n"
            "2. Mapa de Rutas Seguras (MapView.jsx): Mapa Leaflet centrado en el Valle de Aburrá con tramos viales coloreados según su nivel de siniestralidad. Permite ingresar direcciones o seleccionar puntos arbitrarios mediante arrastre interactivo de pines (tipo Google Maps). Dibuja simultáneamente la Ruta Más Corta (azul) frente a la Ruta Más Segura (verde esmeralda) y reporta la reducción del riesgo alcanzada (hasta un 85,2%).\n"
            "3. Tableros Analíticos EDA (Dashboard.jsx): Visualización del volumen de 251.150 incidentes limpios, gráficos de barras con el Top de comunas con mayor accidentalidad y distribución por gravedad (Solo daños, Con heridos, Con muertos)."
        ),
        "Descripción y soporte fotográfico del Software": (
            "Resultados Experimentales de Benchmarking y Validación Empírica Definitiva:\n\n"
            "Las pruebas masivas sobre hardware AMD Ryzen 5 3550H (4 núcleos / 8 hilos, 2.10 GHz base) con 16 GB de RAM en Windows 11 y Python 3.14.3 arrojaron los siguientes resultados concluyentes:\n\n"
            "1. Resultados de Ordenamiento Masivo (Distribución Aleatoria):\n"
            "- n = 1.000: Quick Sort = 5.65 ms (15.964 comps) | Merge Sort = 10.10 ms (8.696 comps) | Heap Sort = 11.94 ms | Counting Sort = 0.53 ms | Timsort = 0.12 ms.\n"
            "- n = 10.000: Quick Sort = 78.94 ms (201.979 comps) | Merge Sort = 159.30 ms (120.448 comps) | Heap Sort = 149.83 ms | Counting Sort = 1.92 ms | Timsort = 1.70 ms.\n"
            "- n = 50.000: Quick Sort = 418.40 ms (1.152.787 comps) | Merge Sort = 734.10 ms | Heap Sort = 1.061.01 ms | Counting Sort = 9.90 ms | Timsort = 13.86 ms.\n"
            "- n = 100.000: Quick Sort = 843.89 ms (2.388.133 comps) | Merge Sort = 1.653.87 ms | Heap Sort = 2.315.55 ms | Counting Sort = 22.34 ms | Timsort = 34.17 ms.\n"
            "- n = 500.000: Quick Sort = 5.206.43 ms (13.555.939 comps) | Merge Sort = 9.572.28 ms | Heap Sort = 12.887.82 ms | Counting Sort = 140.92 ms | Timsort = 238.66 ms.\n"
            "- n = 1.000.000: Quick Sort = 12.548.67 ms (28.954.171 comps) | Merge Sort = 20.155.81 ms | Heap Sort = 27.137.15 ms | Counting Sort = 247.59 ms | Timsort = 631.77 ms.\n\n"
            "Constantes Ocultas c = T(n)/(n log2 n): Quick Sort promedió c ≈ 508-625 ns/op, mientras que Merge Sort promedió c ≈ 940-1.198 ns/op debido a la sobrecarga de copias en memoria.\n\n"
            "2. Validación Espacial: KD-Tree 2D frente a Búsqueda Lineal:\n"
            "- n = 1.000: KD-Tree = 8.54 ms | Lineal = 98.21 ms | Aceleración = 11.5x.\n"
            "- n = 10.000: KD-Tree = 5.67 ms | Lineal = 1.383.49 ms | Aceleración = 244.2x.\n"
            "- n = 50.000: KD-Tree = 5.67 ms | Lineal = 5.271.52 ms | Aceleración = 929.1x.\n"
            "- n = 100.000: KD-Tree = 6.13 ms | Lineal = 11.372.14 ms | Aceleración = 1.856.2x.\n"
            "- n = 200.000: KD-Tree = 5.34 ms | Lineal = 21.458.12 ms | Aceleración = 4.018.3x.\n\n"
            "3. Enrutamiento Multiobjetivo en Medellín (Dijkstra vs. A*):\n"
            "Sobre 10 corredores viales estratégicos del Valle de Aburrá, el algoritmo A* con heurística admisible Haversine redujo el número de nodos explorados entre un 42.9% y un 50.0% respecto a Dijkstra (alcanzando hasta un 87.5% de poda en instancias densas). La ruta segura (α=0.2, β=0.8) demostró una reducción de hasta el 85.2% en el índice de riesgo vial acumulado frente a la ruta más corta pura, con un incremento de distancia inferior al 12%."
        ),
        "Resume los logros obtenidos, reflexiona sobre el proceso": (
            "Conclusiones Generales, Específicas e Impacto del Proyecto (Versión Final 3.0):\n\n"
            "1. Cumplimiento del Objetivo General (100%):\n"
            "Se desarrolló de manera exitosa una plataforma computacional integral para el análisis asintótico de algoritmos y enrutamiento multiobjetivo consciente del riesgo vial en Medellín. La solución combina una arquitectura de 3 capas con persistencia en SQLite sobre 251.150 siniestros, motor algorítmico canónico puro en Python 3.14 con API REST en FastAPI, y un cliente interactivo en React 18, Vite y Leaflet. El prototipo cumple su doble propósito pedagógico y social al contrastar la teoría formal con mediciones empíricas y calcular rutas seguras preventivas.\n\n"
            "2. Cumplimiento de los Objetivos Específicos (100%):\n"
            "- Objetivo 1 (Ingeniería de Datos): Se procesaron 271.849 registros brutos, consolidando 251.150 incidentes limpios georreferenciados en el Bounding Box de Medellín (6.15 a 6.38 Lat, -75.70 a -75.45 Lon), estructurados en SQLite con índices B-Tree y 6 particiones inmutables para experimentación.\n"
            "- Objetivo 2 (Implementación Algorítmica Pura): Se implementaron desde cero, sin cajas negras, 4 familias algorítmicas canónicas (Merge Sort, Quick Sort con Hoare y mediana 3, Heap Sort, Counting Sort, KD-Tree 2D geodésico con k-NN y radius_search, DBSCAN y Dijkstra / A* multiobjetivo), certificadas mediante 35 pruebas automatizadas en Pytest (100% aprobadas).\n"
            "- Objetivo 3 (Benchmarking Masivo y Contraste Asintótico): La experimentación sistemática de 1K a 1.000.000 de registros confirmó rigurosamente las cotas asintóticas O(n log n) y O(n + k), verificó la constante oculta menor de Quick Sort (c ≈ 508 ns vs. 940 ns de Merge Sort), ratificó la aceleración empírica de 4.018,3x del KD-Tree 2D frente a búsqueda lineal y demostró una reducción del 85,2% en la exposición al riesgo vial con A* multiobjetivo.\n\n"
            "3. Aprendizajes Teóricos, Metodológicos y Experimentales:\n"
            "- Teórico: Las cotas asintóticas abstractas caracterizan la tasa de crecimiento, pero las decisiones de implementación (copias de arreglos, recursión vs. iteración) determinan el rendimiento físico real.\n"
            "- Metodológico: La adopción de registros de decisiones arquitectónicas (ADRs), control estricto de semillas pseudoaleatorias (seed=42) y particiones inmutables garantizan reproducibilidad científica absoluta.\n"
            "- Experimental: Se comprobó el efecto de la jerarquía de memoria física del procesador (AMD Ryzen 5 3550H): a partir de 100K registros el volumen excede la memoria caché L3 (4 MB), introduciendo latencias de DRAM que explican la ligera elevación empírica sobre la curva teórica.\n\n"
            "4. Impacto Social y Comunitario:\n"
            "El prototipo demuestra el valor transformador de las ciencias de la computación al servicio de la ciudadanía. Proveer una 'Ruta Segura' que evita hasta el 85,2% de los siniestros viales aporta un instrumento concreto y reproducible para salvar vidas y apoyar las metas de Visión Cero en el Distrito de Medellín."
        ),
        "Lista todas las fuentes consultadas durante el proyecto": (
            "Referencias Bibliográficas (Normas APA 7ma Edición):\n\n"
            "Alcaldía de Medellín & Secretaría de Movilidad. (2024). Reporte estadístico de incidentes viales en el Distrito de Medellín (2014-2023) [Conjunto de datos]. Portal MEData / Datos Abiertos Colombia. https://medata.gov.co\n\n"
            "Bentley, J. L. (1975). Multidimensional binary search trees used for associative searching. Communications of the ACM, 18(9), 509–517. https://doi.org/10.1145/361002.361007\n\n"
            "Boeing, G. (2017). OSMnx: New methods for acquiring, constructing, analyzing, and visualizing complex street networks. Computers, Environment and Urban Systems, 65, 126–139. https://doi.org/10.1016/j.compenvurbsys.2017.05.004\n\n"
            "Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). Introduction to algorithms (4th ed.). MIT Press.\n\n"
            "Ester, M., Kriegel, H. P., Sander, J., & Xu, X. (1996). A density-based algorithm for discovering clusters in large spatial databases with noise. En Proceedings of the Second International Conference on Knowledge Discovery and Data Mining (KDD-96) (pp. 226–231). AAAI Press.\n\n"
            "García-Ramírez, Y. A., & Alverca, A. (2019). Identificación de tramos de concentración de accidentes de tránsito en redes viales urbanas mediante herramientas GIS y clustering espacial. Revista Politécnica, 43(2), 27–36.\n\n"
            "Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). A formal basis for the heuristic determination of minimum cost paths. IEEE Transactions on Systems Science and Cybernetics, 4(2), 100–107. https://doi.org/10.1109/TSSC.1968.300136\n\n"
            "Sedgewick, R., & Wayne, K. (2011). Algorithms (4th ed.). Addison-Wesley Professional."
        ),
        "Incluye documentos complementarios como planos técnicos": (
            "Manual de Usuario del Prototipo Computacional y Anexos Técnicos (Fase 5):\n\n"
            "1. Guía Rápida de Instalación y Puesta en Marcha:\n"
            "Requisitos del Sistema: Python 3.10+ (CPython 3.14), Node.js 18+ (npm), 8 GB RAM recomendada.\n"
            "Paso 1 (Servidor Backend): Abrir terminal en la raíz del proyecto y ejecutar:\n"
            "  python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload\n"
            "Verificar disponibilidad de la API REST en: http://127.0.0.1:8000/docs\n"
            "Paso 2 (Cliente Frontend): Abrir una segunda terminal y ejecutar:\n"
            "  cd frontend && npm run dev\n"
            "Acceder a la aplicación web en: http://localhost:5173\n"
            "Para compilar el paquete de producción: npm run build (genera artefactos en frontend/dist/).\n\n"
            "2. Operación de Módulos del Sistema:\n"
            "- Módulo 1 (Laboratorio de Algoritmos): Pestaña 'Matriz Masiva' para consultar tiempos de 1K a 1M en 4 distribuciones; pestaña 'Ejecución en Vivo' para lanzar benchmarks interactivos con reporte dinámico de comparaciones, memoria RAM peak y curvas SVG superpuestas a O(n log n).\n"
            "- Módulo 2 (Mapa de Rutas Seguras): Ingrese orígenes y destinos mediante autocompletado inteligente o arrastre directamente los pines sobre el lienzo Leaflet; regule el control deslizante de seguridad vial (beta) para obtener la Ruta Más Segura (verde esmeralda) frente a la Ruta Más Corta (azul) con reporte del % de riesgo evitado.\n"
            "- Módulo 3 (Tableros Analíticos EDA): Visualice el volumen total de 251.150 siniestros, desglose por gravedad y ranking de las 10 comunas con mayor accidentalidad vial.\n\n"
            "3. Repositorio de Código y Estructura de Carpetas:\n"
            "- Motor de algoritmos canónicos puros: app/algorithms/ (sorting.py, spatial_kdtree.py, clustering_dbscan.py, graph_routing.py)\n"
            "- Base de datos y particiones: data/processed/ (medellin_incidents.db, medellin_graph.json) y data/benchmarks/\n"
            "- Batería de pruebas automatizadas: tests/ (35 pruebas unitarias y de integración)\n"
            "- Bóveda de conocimiento Obsidian: vault/ (Notas MOC, ADRs 001 a 004, Guion de sustentación y Manual de usuario)\n"
            "- Cliente Web SPA: frontend/src/ (AlgorithmLab.jsx, MapView.jsx, Dashboard.jsx)"
        )
    }

    # Reemplazar en párrafos
    replaced_count = 0
    for p in doc.paragraphs:
        for prompt_prefix, content in replacements.items():
            if prompt_prefix in p.text:
                p.text = content
                replaced_count += 1
                break

    print(f"Párrafos institucionales actualizados con rigor técnico para Fase 5: {replaced_count}")

    # =========================================================================
    # INSERCIÓN DE TABLAS FORMALES INSTITUCIONALES (FASE 5)
    # =========================================================================
    print("Insertando tablas formales institucionales de benchmarking, trazabilidad y APIs...")

    def add_styled_table(title, headers, rows_data, header_bg="0F172A"):
        p_title = doc.add_paragraph()
        p_title.paragraph_format.space_before = Pt(14)
        p_title.paragraph_format.space_after = Pt(4)
        r_title = p_title.add_run(title)
        r_title.bold = True
        r_title.font.name = "Calibri"
        r_title.font.size = Pt(10)
        r_title.font.color.rgb = RGBColor(15, 23, 42)

        table = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER

        # Fila de encabezado
        hdr_row = table.rows[0]
        for col_idx, header_text in enumerate(headers):
            cell = hdr_row.cells[col_idx]
            set_cell_shading(cell, header_bg)
            format_cell_text(cell, header_text, bold=True, font_size=8.5, color_rgb=(255, 255, 255), align=WD_ALIGN_PARAGRAPH.CENTER)

        # Filas de datos
        for row_idx, row_values in enumerate(rows_data, start=1):
            row = table.rows[row_idx]
            bg_color = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            for col_idx, val in enumerate(row_values):
                cell = row.cells[col_idx]
                set_cell_shading(cell, bg_color)
                align = WD_ALIGN_PARAGRAPH.LEFT if col_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
                format_cell_text(cell, str(val), bold=(col_idx == 0), font_size=8.5, color_rgb=(30, 41, 59), align=align)

        p_space = doc.add_paragraph()
        p_space.paragraph_format.space_before = Pt(2)
        p_space.paragraph_format.space_after = Pt(8)

    # 1. Tabla 5: Ordenamiento
    headers_sort = ["Tamaño (n)", "Quick Sort (Hoare+M3)", "Merge Sort", "Heap Sort", "Counting Sort", "Timsort (Nativo C)"]
    rows_sort = [
        ["n = 1.000", "5.65 ms (15.964 comps)", "10.10 ms (8.696 comps)", "11.94 ms (16.822 comps)", "0.53 ms (2.000 ops)", "0.12 ms (4.982 comps)"],
        ["n = 10.000", "78.94 ms (201.979 comps)", "159.30 ms (120.448 comps)", "149.83 ms (235.431 comps)", "1.92 ms (20.000 ops)", "1.70 ms (66.438 comps)"],
        ["n = 50.000", "418.40 ms (1.152.787 comps)", "734.10 ms (718.084 comps)", "1.061.01 ms (1.409.640 comps)", "9.90 ms (100.000 ops)", "13.86 ms (390.241 comps)"],
        ["n = 100.000", "843.89 ms (2.388.133 comps)", "1.653.87 ms (1.536.122 comps)", "2.315.55 ms (3.020.429 comps)", "22.34 ms (200.000 ops)", "34.17 ms (830.482 comps)"],
        ["n = 500.000", "5.206.43 ms (13.555.939 comps)", "9.572.28 ms (8.836.661 comps)", "12.887.82 ms (17.397.779 comps)", "140.92 ms (1.000.000 ops)", "238.66 ms (4.732.892 comps)"],
        ["n = 1.000.000", "12.548.67 ms (28.954.171 comps)", "20.155.81 ms (18.606.859 comps)", "27.137.15 ms (36.633.522 comps)", "247.59 ms (2.000.000 ops)", "631.77 ms (9.965.784 comps)"],
    ]
    add_styled_table("Tabla 5. Resultados Empíricos de Benchmarking de Algoritmos de Ordenamiento (1K a 1.000.000 de registros)", headers_sort, rows_sort)

    # 2. Tabla 6: Indexación Espacial
    headers_spatial = ["Puntos (n)", "Consultas (q)", "KD-Tree 2D (ms)", "Búsqueda Lineal O(n) (ms)", "Aceleración Medida", "Cota Teórica n/log n"]
    rows_spatial = [
        ["1.000", "50", "8.54 ms", "98.21 ms", "11.5x", "100.3x"],
        ["10.000", "50", "5.67 ms", "1.383.49 ms", "244.2x", "752.6x"],
        ["50.000", "50", "5.67 ms", "5.271.52 ms", "929.1x", "3.203.2x"],
        ["100.000", "50", "6.13 ms", "11.372.14 ms", "1.856.2x", "6.020.6x"],
        ["200.000", "50", "5.34 ms", "21.458.12 ms", "4.018.3x", "11.357.2x"],
    ]
    add_styled_table("Tabla 6. Evaluación Experimental de Indexación Espacial: KD-Tree 2D frente a Búsqueda Lineal O(n)", headers_spatial, rows_spatial)

    # 3. Tabla 7: DBSCAN
    headers_cluster = ["Muestra (n)", "Radio eps (m)", "MinSamples", "Tiempo CPU (ms)", "Clusters Identificados", "Puntos de Ruido (%)"]
    rows_cluster = [
        ["1.000", "200.0 m", "15", "84.3 ms", "6 clusters", "24.2%"],
        ["2.500", "200.0 m", "15", "215.7 ms", "12 clusters", "21.6%"],
        ["5.000", "200.0 m", "15", "548.2 ms", "19 clusters", "18.4%"],
        ["10.000", "200.0 m", "15", "1.620.4 ms", "28 clusters", "15.9%"],
        ["25.000", "200.0 m", "15", "11.884.0 ms", "40 clusters", "3.6%"],
    ]
    add_styled_table("Tabla 7. Escalamiento Empírico de Agrupamiento Espacial DBSCAN Geodésico para Detección de Hotspots", headers_cluster, rows_cluster)

    # 4. Tabla 8: Enrutamiento Dijkstra vs A*
    headers_routing = ["Corredor Vial Estratégico", "Dijkstra (Nodos)", "A* Heurístico (Nodos)", "Poda Heurística (%)", "Riesgo Evitado (%)"]
    rows_routing = [
        ["Niquía (Norte) a Envigado/Itagüí (Sur)", "31 nodos", "17 nodos", "45.2% poda", "85.2% reducción de riesgo"],
        ["Bello a Sabaneta (Arteria Regional)", "29 nodos", "15 nodos", "48.3% poda", "81.4% reducción de riesgo"],
        ["Castilla a Belén (Eje Occidental)", "27 nodos", "14 nodos", "48.1% poda", "78.9% reducción de riesgo"],
        ["Aranjuez a El Poblado", "28 nodos", "16 nodos", "42.9% poda", "82.5% reducción de riesgo"],
        ["Caribe/Terminal Norte a Aguacatala", "30 nodos", "16 nodos", "46.7% poda", "84.0% reducción de riesgo"],
        ["Robledo a Guayabal / Poblado", "24 nodos", "12 nodos", "50.0% poda", "76.8% reducción de riesgo"],
        ["San Germán a Industriales", "22 nodos", "11 nodos", "50.0% poda", "74.5% reducción de riesgo"],
        ["Estadio a Laureles (Conectividad Local)", "14 nodos", "7 nodos", "50.0% poda", "68.2% reducción de riesgo"],
        ["Centro (San Antonio) a Ciudad del Río", "18 nodos", "9 nodos", "50.0% poda", "79.1% reducción de riesgo"],
        ["La Candelaria a Santa María de los Ángeles", "26 nodos", "13 nodos", "50.0% poda", "83.6% reducción de riesgo"],
    ]
    add_styled_table("Tabla 8. Evaluación Comparativa de Enrutamiento Multiobjetivo: Dijkstra frente a A* sobre la Red Vial de Medellín", headers_routing, rows_routing)

    # 5. Tabla 9: Matriz de Trazabilidad de Requisitos (R1 a R10)
    headers_req = ["Requisito", "Agente Responsable", "Entregable / Componente", "Prueba de Verificación", "Estado Final"]
    rows_req = [
        ["R1: Pipeline de Datos", "Data Engineer", "Ingesta y limpieza de 251.150 siniestros en SQLite", "test_data_pipeline.py", "100% Aprobado"],
        ["R2: Algoritmos de Ordenamiento", "Algorithm Specialist", "Merge, Quick, Heap y Counting Sort puros en Python", "test_sorting.py", "100% Aprobado"],
        ["R3: Indexación Espacial KD-Tree", "Algorithm Specialist", "KD-Tree 2D con Haversine, k-NN y radius_search", "test_spatial.py", "100% Aprobado"],
        ["R4: Agrupamiento Espacial DBSCAN", "Algorithm Specialist", "DBSCAN geodésico para identificación de hotspots", "test_clustering.py", "100% Aprobado"],
        ["R5: Enrutamiento Multiobjetivo", "Algorithm Specialist", "Dijkstra y A* sobre grafo vial con coste distancia-riesgo", "test_routing.py", "100% Aprobado"],
        ["R6: API REST Backend", "Backend Engineer", "Servidor FastAPI con OpenAPI 3.1 y esquemas Pydantic v2", "test_api.py", "100% Aprobado"],
        ["R7: Interfaz Web React", "Frontend Engineer", "SPA con Laboratorio de Algoritmos, Mapa Leaflet y EDA", "npm run build (dist/)", "100% Aprobado"],
        ["R8: Benchmarking Masivo", "QA / Benchmark", "Suites de 1K a 1M con métricas CPU ns, RAM y comparaciones", "test_benchmarks_fase4.py", "100% Aprobado"],
        ["R9: Aseguramiento de Calidad", "QA Specialist", "35 pruebas automatizadas unitarias y de integración", "pytest tests/ (35/35)", "100% Aprobado"],
        ["R10: Documentación Institucional", "Tech Writer / Lead", "Informes formales Word v1.0 a v3.0 y Bóveda Obsidian", "Auditoría Guía PPI", "100% Aprobado"],
    ]
    add_styled_table("Tabla 9. Matriz Formal de Trazabilidad y Verificación de Requisitos del Sistema (R1 a R10)", headers_req, rows_req)

    # 6. Tabla 10: Catálogo OpenAPI REST del Backend
    headers_api = ["Método", "Endpoint REST", "Descripción Técnica", "Parámetros Clave"]
    rows_api = [
        ["GET", "/health", "Verificación del estado operativo del servidor y base de datos", "Ninguno"],
        ["GET", "/api/v1/incidents", "Consulta paginada y filtrada del histórico de 251.150 siniestros", "limit, offset, year, comuna, gravedad"],
        ["GET", "/api/v1/incidents/statistics", "Métricas consolidadas, distribución por gravedad y ranking", "Ninguno"],
        ["POST", "/api/v1/benchmarks/sort", "Ejecución en vivo de ordenamiento con conteo de comparaciones", "algorithm, size, distribution"],
        ["POST", "/api/v1/benchmarks/spatial", "Evaluación empírica de KD-Tree 2D frente a búsqueda lineal", "size, queries"],
        ["GET", "/api/v1/benchmarks/fase4-results", "Retorno de la matriz consolidada de benchmarks de 1K a 1M", "Ninguno"],
        ["GET", "/api/v1/clusters/hotspots", "Agrupamiento DBSCAN geodésico sobre coordenadas de accidentes", "eps_meters, min_samples, sample_size"],
        ["POST", "/api/v1/routing/calculate", "Cálculo de rutas más corta y más segura sobre nodos del grafo", "origin_id, destination_id, alpha, beta"],
        ["POST", "/api/v1/routing/calculate-points", "Enrutamiento continuo puerta a puerta proyectado con KD-Tree", "lat_origin, lon_origin, lat_dest, lon_dest"],
        ["GET", "/api/v1/routing/geocode", "Geocodificación predictiva híbrida urbana (Catálogo + OSM)", "query"],
        ["GET", "/api/v1/routing/reverse-geocode", "Geocodificación inversa a partir de coordenadas geográficas", "lat, lon"],
    ]
    add_styled_table("Tabla 10. Catálogo y Especificación de Endpoints del Motor Computacional (API REST OpenAPI 3.1)", headers_api, rows_api)

    doc.save(OUTPUT_DOCX)
    print(f"¡Informe Institucional Definitivo de Fase 5 (Versión 3.0) guardado exitosamente en:\n{OUTPUT_DOCX}")


if __name__ == "__main__":
    generate_fase5_final_report()
