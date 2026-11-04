---
titulo: "Conclusiones Generales, Específicas e Impacto del Proyecto"
tipo: resumen
tipo: conclusiones
proyecto: PPI - Analisis de Algoritmos
institucion: Tecnologico de Antioquia
semestre: 8vo Semestre - 2026
fase: Entrega Final y Cierre
version: 2.1
fecha: 2026-10-08
estado: completado
autores:
  - Jarrison Quintero Castillo
  - Sebastián Gómez Cardona
  - Cristian David Pulgarín Vélez
requisitos_asociados:
  - R1
  - R2
  - R3
  - R4
  - R5
  - R6
  - R7
  - R8
  - R9
  - R10
tags:
  - conclusiones
  - resultados
  - aprendizajes
  - impacto-social
  - aburrasegura
  - entrega-final
vigencia: vigente
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/resumen, ppi/tdea, proyecto/aburrasegura]
---


# Conclusiones Generales, Específicas e Impacto del Proyecto — AburráSegura

> [!abstract] En pocas palabras
> Análisis final de resultados del proyecto: reducción demostrada de exposición a puntos críticos en un 64% y cumplimiento pleno de los objetivos del PPI.


Este documento formaliza la redacción definitiva para la **Sección 6 (CONCLUSIONES)** de `AburráSegura.docx`, respondiendo a cada requerimiento del formato institucional de la Facultad de Ingeniería del Tecnológico de Antioquia.

---

## 1. Evaluación de Cumplimiento por Objetivo (Sección 6.1)

### 1.1 Conclusión para el Objetivo General
> *Objetivo General:* Desarrollar una plataforma computacional para la identificación de puntos críticos y cálculo de rutas seguras de siniestralidad vial en Medellín mediante el algoritmo de grafos y análisis asintótico de algoritmos sobre datos abiertos.

- **Evaluación y Dictamen:** **Cumplido al 100%**.
- **Sustento Técnico:** Se diseñó, implementó y validó una plataforma computacional desacoplada en tres capas que integra la depuración geoespacial de 251.150 siniestros viales de MEData, la modelación topológica de la red vial en un grafo dirigido ponderado $G = (V, E)$, el Algoritmo de Dijkstra con cola de prioridad *min-heap* ($\mathcal{O}((V + E) \log V)$) con función multiobjetivo de aversión al riesgo, y un Laboratorio de Rendimiento interactivo que mide en tiempo real las cinco clases asintóticas ($\mathcal{O}(1)$ a $\mathcal{O}(n^2)$). La solución demostró que es viable utilizar la teoría formal de algoritmos para resolver una problemática social crítica de salud pública en el Valle de Aburrá, reduciendo hasta un 89,47% la exposición a siniestros viales con incrementos marginales de distancia inferiores al 12%.

---

### 1.2 Conclusión para el Objetivo Específico 1 (Fase 1: Datos y Puntos Críticos)
> *Objetivo Específico 1:* Adquirir, limpiar y estructurar los datos abiertos de siniestros viales de Medellín para delimitar y ponderar las zonas con mayor concentración histórica de accidentes.

- **Evaluación y Dictamen:** **Cumplido al 100%**.
- **Sustento Técnico:** Se estructuró un pipeline automatizado de ingeniería de datos que ingirió 271.849 registros brutos del portal MEData (2014-2024), aplicando depuración rigurosa de anomalías de coordenadas y filtrado estricto por Bounding Box metropolitano ($[6.15, 6.38] \text{ Lat}, [-75.70, -75.45] \text{ Lon}$). Se consolidó una base de datos relacional SQLite (`medellin_incidents.db`) con 251.150 incidentes limpios (retención del 92,8%) e índices B-Tree especializados que aseguran consultas en tiempo inferior a 5 milisegundos. Asimismo, se delimitaron formalmente los principales conglomerados de accidentalidad (*hotspots* viales) como la Glorieta de la 33 con Autopista Sur, Punto Cero y la Avenida Oriental, asignando factores de severidad ponderada ($w=1.0$ solo daños, $w=2.0$ con heridos, $w=3.0$ con muertos).

---

### 1.3 Conclusión para el Objetivo Específico 2 (Fase 2: Grafo y Dijkstra Multiobjetivo)
> *Objetivo Específico 2:* Modelar la red vial como un grafo ponderado e implementar el algoritmo de Dijkstra con una función de coste multiobjetivo que equilibre la distancia geométrica y la penalización por zonas de riesgo.

- **Evaluación y Dictamen:** **Cumplido al 100%**.
- **Sustento Técnico:** Se modeló la infraestructura vial urbana mediante un grafo dirigido $G = (V, E)$ serializado en `medellin_graph.json` que respeta el sentido legal de circulación del Código Nacional de Tránsito. Se programó desde cero en Python puro el Algoritmo de Dijkstra utilizando una cola de prioridad basada en montículo binario de mínimos (*min-heap*), garantizando una cota temporal de $\mathcal{O}((V + E) \log V)$ y tiempos de resolución inferiores a 3 milisegundos. La función de coste multiobjetivo normalizada con factor regulable ($\alpha$ para distancia, $\beta$ para seguridad) demostró que fijar $\alpha = 0.2, \beta = 0.8$ genera trayectorias alternas seguras que esquivan eficazmente las glorietas y cruces neurálgicos con alta tasa de letalidad, cumpliendo los requerimientos RF-06 a RF-11.

---

### 1.4 Conclusión para el Objetivo Específico 3 (Fase 3: Pruebas, Benchmarking y Laboratorio)
> *Objetivo Específico 3:* Evaluar empíricamente el tiempo de ejecución y la complejidad asintótica del algoritmo frente al tamaño de la red vial, comparando la ruta más corta frente a la ruta más segura en términos de distancia y siniestralidad evitada.

- **Evaluación y Dictamen:** **Cumplido al 100%**.
- **Sustento Técnico:** Se desarrolló el Laboratorio de Jerarquía Asintótica (`POST /api/v1/benchmarks/complexity`), el cual evidenció con exactitud cuantitativa sobre hardware real AMD Ryzen 5 y Python 3.14.3 el comportamiento de las cinco clases fundamentales de complejidad sobre los 251.150 registros reales: $\mathcal{O}(1)$ en $0{,}0001\text{ ms}$, $\mathcal{O}(\log n)$ en $0{,}0019\text{ ms}$ (18 comparaciones exactas), $\mathcal{O}(n)$ en $49{,}85\text{ ms}$ (251.150 inspecciones), $\mathcal{O}(n \log n)$ en $1{,}84\text{ s}$ (~4,1M operaciones) y $\mathcal{O}(n^2)$ con un crecimiento cuadrático explosivo que demostró empíricamente por qué la fuerza bruta es computacionalmente prohibitiva a escala urbana. Toda la arquitectura algorítmica fue certificada mediante **44 pruebas automatizadas en Pytest (100% PASS en 8.31s)** sin ninguna regresión.

---

## 2. Aprendizajes Adquiridos (Sección 6.2)

### A. Aprendizajes Teóricos
1. **Diferenciación entre Cotas Abstractas y Constantes Físicas:** Se comprendió que dos algoritmos con idéntica cota asintótica $\mathcal{O}(n \log n)$ (como Merge Sort y Quick Sort) exhiben rendimientos físicos dispares debido a sus constantes ocultas ($c$). Quick Sort opera con una constante $c \approx 508\text{ ns}$, mientras que Merge Sort promedia $c \approx 940\text{ ns}$ debido a la sobrecarga de asignación de nuevos subarreglos en la memoria dinámica.
2. **Invariantes y Demostración de Inducción:** Se afianzó la demostración inductiva de Dijkstra, comprobando que la condición de no negatividad de los pesos ($w(e) \ge 0$) es la garantía matemática que impide que un nodo ya cerrado en el conjunto de visitados deba ser reevaluado.
3. **Poder de la Indexación Logarítmica:** La implementación del KD-Tree 2D demostró cómo la partición ortogonal del espacio geodésico reduce la búsqueda del vecino más cercano de $\mathcal{O}(n)$ a $\mathcal{O}(\log n)$, generando aceleraciones de hasta 4.018,3× frente a la búsqueda lineal.

### B. Aprendizajes Metodológicos
1. **Disciplina de Control de Versiones y ADRs:** El registro de decisiones de arquitectura (ADR-001 a ADR-005) permitió al equipo mantener trazabilidad estricta de por qué se adoptaron o descartaron tecnologías, facilitando el replanteamiento del alcance sin perder el rigor académico.
2. **Reproducibilidad Experimental:** El aislamiento de particiones CSV inmutables, la fijación de semillas pseudoaleatorias (`seed=42`) y la medición directa de nanosegundos (`time.perf_counter_ns`) permitieron obtener métricas científicas con coeficientes de variación estadística mínimos ($\sigma / \mu < 0.05$).
3. **Enfoque de Integración Continua con Pytest:** La automatización de 44 casos de prueba que evalúan escenarios borde patológicos (listas vacías, elementos idénticos, grafos disconexos) garantizó que cada modificación en el código mantuviera la integridad matemática del prototipo.

### C. Aprendizajes Experimentales
1. **Influencia de la Jerarquía de Caché Física (L1/L2/L3):** Se evidenció en el laboratorio que al superar los 100.000 registros, el tamaño de la muestra sobrepasa los 4 MB de la memoria caché L3 del procesador AMD Ryzen 5, generando fallos de línea de caché (*cache misses*) y obligando a accesos a la memoria RAM DDR4, lo que explica la ligera elevación empírica en las curvas de benchmarking.
2. **Mitigación de Desbordamientos de Pila:** Se aprendió que en lenguajes interpretados como Python, la recursión ingenua provoca fallos de desbordamiento de pila (`RecursionError`) con llamadas profundas ($> 1.000$). La implementación de Quick Sort iterativo con pila explícita acotada a $\mathcal{O}(\log n)$ demostró ser la técnica industrial definitiva para procesar hasta 1.000.000 de elementos de forma segura.

---

## 3. Análisis de Impacto Social, Comunitario y Académico (Sección 6.3)

### 3.1 Impacto Social y Comunitario Positivo
- **Aporte a la Seguridad Vial y Preservación de la Vida:** Proveer una alternativa algorítmica que calcula la "Ruta Más Segura" ofrece a la ciudadanía de Medellín, especialmente a motociclistas y ciclistas (quienes representan más del 80% de los lesionados graves en la ciudad), una herramienta preventiva tangible para evitar los corredores de mayor letalidad histórica, apoyando las políticas públicas de "Visión Cero".
- **Apropiación Social de los Datos Abiertos:** El proyecto demuestra que los datos abiertos gubernamentales del portal MEData no deben limitarse a estadísticas pasivas o gráficas estáticas, sino que pueden convertirse en algoritmos activos que beneficien directamente el desplazamiento cotidiano de la comunidad.

### 3.2 Impacto Académico e Institucional Positivo
- **Referente Formativo para el Tecnológico de Antioquia:** El prototipo se constituye como un proyecto pedagógico de referencia para la Facultad de Ingeniería, demostrando que los estudiantes de 8vo semestre de Ingeniería en Software son capaces de concebir, implementar desde cero, medir experimentalmente y defender ante la academia soluciones algorítmicas robustas con base matemática y relevancia territorial.
- **Base para Trabajos de Grado y Semilleros de Investigación:** La plataforma queda estructurada como un repositorio extensible para semilleros que deseen incorporar redes viales más densas, telemetría IoT o algoritmos de enrutamiento estocástico.

### 3.3 Identificación y Mitigación de Posibles Impactos Negativos
- **Riesgo de Saturación de Vías Barriales (Efecto Derrame):** Si una aplicación de navegación redirige de forma masiva el tráfico vehicular hacia vías residenciales tranquilas para evitar choques arteriales, podría generar congestión y deterioro de la tranquilidad en barrios vulnerables. *Medida de Mitigación:* En el diseño de la red vial solo se incluyeron vías arteriales y colectoras principales autorizadas para tráfico continuo, omitiendo pasajes residenciales peatonales y calibrando el factor $\alpha$ para evitar desvíos desproporcionados.
- **Sesgo por Subregistro de Incidentes Leves:** Los accidentes menores sin heridos a menudo no son reportados a los agentes de tránsito. *Medida de Mitigación:* El algoritmo pondera con mayor severidad ($w=3.0$) los eventos con víctimas fatales y lesionados graves, los cuales cuentan con un registro oficial exhaustivo y fidedigno por parte de las autoridades forenses y de tránsito.

---

## 🔗 Relacionado
- [[00 - Inicio|Inicio]]
- [[Guion-Sustentacion-Oral]]
- [[Manual-Usuario-Prototipo]]
- [[Reporte-Final-QA-Fase5]]
