---
titulo: "Antecedentes Académicos y Estado del Arte"
tipo: investigacion
tipo: investigacion
proyecto: PPI - Analisis de Algoritmos
institucion: Tecnologico de Antioquia
estado: completado
version: 2.1
fecha: 2026-10-08
autores:
  - Jarrison Quintero Castillo
  - Sebastián Gómez Cardona
  - Cristian David Pulgarín Vélez
requisito_asociado:
  - R1
  - R4
  - R5
  - RF-06
  - RF-08
tags:
  - antecedentes
  - estado-del-arte
  - apa7
  - investigacion
  - algoritmos
  - aburrasegura
vigencia: vigente
documento_asociado: "AburráSegura.docx (Sección 2.1 - Tabla 3)"
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/investigacion, ppi/tdea, proyecto/aburrasegura]
---


# Antecedentes Académicos y Estado del Arte (Normas APA 7ma Edición)

> [!abstract] En pocas palabras
> Revisión del estado del arte en enrutamiento seguro, teoría de grafos, estructuras espaciales y clustering según Cormen, Dijkstra, Bentley y literatura especializada.


> [!NOTE] Alineación Institucional
> Esta nota formaliza el estado del arte y los referentes teóricos y tecnológicos que sustentan el diseño de **AburráSegura**, en estricta sincronía con la **Tabla 3 de `AburráSegura.docx` (Sección 2.1)**.

---

## 1. Contextualización del Estado del Arte

La optimización de trayectorias urbanas conscientes del riesgo de accidentalidad y el análisis algorítmico de eventos geoespaciales constituyen una intersección fértil entre la ingeniería de tránsito y las ciencias computacionales. Históricamente, las plataformas comerciales de navegación vehicular (como Google Maps o Waze) han optimizado exclusivamente la distancia física euclidiana o el tiempo estimado de viaje basado en telemetría de congestión vehicular. No obstante, la incorporación del riesgo de siniestralidad acumulado plantea desafíos asintóticos no triviales, dado que el cálculo de rutas seguras demanda la ponderación continua de grafos dirigidos a partir de cientos de miles de puntos de colisión dispersos.

A continuación se sintetizan los referentes teóricos y metodológicos fundamentales que sustentan el diseño algorítmico de este proyecto:

---

## 2. Matriz Oficial de Referentes y Antecedentes (Tabla 3 de `AburráSegura.docx`)

| Referente / Antecedente | Aporte Clave al Proyecto | Diferencia con la Propuesta de AburráSegura |
| :--- | :--- | :--- |
| **Google Maps y Waze** *(Software Comercial de Navegación)* | Demuestran la viabilidad del cálculo dinámico de rutas sobre mallas viales urbanas y establecen el estándar de interfaz (mapa interactivo, tiempos y alternativas de ruta). | Solo buscan la ruta más rápida o de menor distancia, ignorando el historial de accidentalidad de las vías. AburráSegura prioriza la **seguridad vial y la reducción de siniestros evitados**. |
| **Portal MEData — Alcaldía de Medellín** *(Datos Abiertos de Movilidad)* | Provee la fuente de datos oficial y verídica con más de 250.000 registros de siniestros viales georreferenciados en Medellín entre 2014 y 2024. | Entrega datos planos en tablas estáticas sin procesamiento analítico ni relación topológica con la red de calles. AburráSegura los **transforma en un grafo ponderado de riesgo**. |
| **Algoritmo de Dijkstra (Dijkstra, 1959)** | Algoritmo fundamental de caminos mínimos en grafos ponderados no negativos con demostración matemática de optimalidad. | El algoritmo clásico solo evalúa un único peso (distancia geométrica). AburráSegura implementa una **función de coste multiobjetivo normalizada ($\alpha$ distancia vs. $\beta$ riesgo)** con cola de prioridad *min-heap*. |
| **Cormen, Leiserson, Rivest & Stein (2022)** | Texto canónico (*Introduction to Algorithms*, 4ta ed.) que fundamenta el análisis asintótico ($\mathcal{O}, \Theta, \Omega$), la recurrencia del Teorema Maestro y la estructura de montículo binario. | Provee la teoría abstracta. AburráSegura traslada estos conceptos a una **plataforma interactiva con mediciones de CPU en nanosegundos** sobre datos territoriales reales de Medellín. |

---

## 3. Referentes Académicos Específicos por Familia Algorítmica

| Investigador / Fuente | Obra / Contribución | Aplicación en el Proyecto |
| :--- | :--- | :--- |
| **Bentley, J. L. (1975)** | Definición original del *k*-d Tree para partición ortogonal del espacio métrico. | Proyección continua de incidentes de MEData a los arcos viales más cercanos en tiempo $\mathcal{O}(\log V)$ con métrica Haversine. |
| **Ester, Kriegel, Sander & Xu (1996)** | Algoritmo DBSCAN para agrupamiento espacial basado en densidad con tolerancia al ruido. | Identificación no supervisada de puntos negros (*hotspots*) de accidentalidad en glorietas y cruces viales complejos. |
| **Hart, Nilsson & Raphael (1968)** | Formulación del algoritmo A* con heurística admisible y consistente. | Evaluación de poda direccional del espacio de búsqueda en la red vial arterial de Medellín. |
| **Boeing, G. (2017)** | Metodología de modelado topológico urbano a partir de datos de OpenStreetMap. | Extracción de nodos de cruce y sentidos viales obligatorios para el grafo de Medellín. |
| **Ogata, K. (2010)** | *Ingeniería de control moderna* (5ta ed.). Fundamentación de sistemas en lazo cerrado. | Analogía del sistema de control del software: Sensor (MEData), Controlador (Dijkstra), Actuador (React Leaflet) y Retroalimentación (usuario). |

---

## 4. Referencias Bibliográficas en Formato APA 7ma Edición (Sección 6 del Documento)

Agencia Nacional de Seguridad Vial [ANSV]. (2023). *Observatorio Nacional de Seguridad Vial: Anuario estadístico de siniestralidad vial en Colombia 2022-2023*. Ministerio de Transporte de Colombia. https://ansv.gov.co/es/observatorio/estadisticas

Alcaldía de Medellín & Secretaría de Movilidad. (2024). *Reporte oficial de incidentes de tránsito en el Distrito de Medellín (2014-2024)* [Conjunto de datos]. Portal MEData / Datos Abiertos Colombia. https://medata.gov.co

Boeing, G. (2017). OSMnx: New methods for acquiring, constructing, analyzing, and visualizing complex street networks. *Computers, Environment and Urban Systems*, 65, 126–139. https://doi.org/10.1016/j.compenvurbsys.2017.05.004

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.

Dijkstra, E. W. (1959). A note on two problems in connexion with graphs. *Numerische Mathematik*, 1(1), 269–271. https://doi.org/10.1007/BF01386390

European Telecommunications Standards Institute [ETSI]. (2022). *5G System; Overall architecture description* (3GPP TS 23.501 version 17.5.0 Release 17). https://www.etsi.org

IEEE Standards Association. (2021). *IEEE Std 802.11ax-2021: Enhancements for high-efficiency WLAN*. Institute of Electrical and Electronics Engineers.

Ogata, K. (2010). *Ingeniería de control moderna* (5.ª ed.). Pearson Educación.

OpenStreetMap Contributors. (2024). *Red vial del Valle de Aburrá y Distrito de Medellín* [Datos cartográficos abiertos]. OpenStreetMap Foundation. https://www.openstreetmap.org

Python Software Foundation. (2024). *time — Time access and conversions* (Documentación de Python 3). https://docs.python.org/3/library/time.html

Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley Professional.

---

## 🔗 Relacionado
- [[00 - Inicio|Inicio]]
- [[Fuentes-y-Matriz-Decision]]
- [[Referencias-APA7]]
- [[Grafos-Dijkstra-AStar]]
