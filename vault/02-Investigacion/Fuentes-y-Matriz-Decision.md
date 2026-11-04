---
titulo: "Fuentes de Datos y Matriz de Decisión Multicriterio"
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
  - R2
  - RF-01
  - RF-02
tags:
  - investigacion
  - fuentes-de-datos
  - matriz-decision
  - socrata
  - medata
  - osm
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/investigacion, ppi/tdea, proyecto/aburrasegura]
---


# Fuentes de Datos y Matriz de Decisión Multicriterio

> [!abstract] En pocas palabras
> Matriz multicriterio de selección y justificación técnica de fuentes de datos de siniestralidad vial en Medellín (MEData vs. SODA vs. OpenStreetMap).


## 1. Fuentes Evaluadas

Para la consolidación del dataset del proyecto se evaluaron tres fuentes potenciales de información geográfica y vial para el Distrito de Medellín:

1. **MEData (Portal de Datos Abiertos de la Alcaldía de Medellín / datos.gov.co):**
   - Repositorio oficial municipal que publica incidentes viales reportados por el Tránsito de Medellín.
   - Datos georreferenciados (latitud, longitud, dirección, gravedad, clase de accidente, comuna, diseño).
   - Volumen: Más de 270.000 registros brutos desde 2014 hasta 2024.
2. **API SODA / Datos Abiertos Colombia:**
   - Protocolo REST Socrata Open Data API para descarga dinámica paginada (`$limit`, `$offset`).
   - Limitaciones de cuota por consulta (1.000 a 50.000 filas por petición) y posibles caídas de red durante ejecuciones offline.
3. **OpenStreetMap (OSM) vía Overpass API:**
   - Base de datos cartográfica colaborativa mundial.
   - Provee la topología de la malla vial urbana (nodos, aristas viales, límites de velocidad, sentidos viales).
   - No contiene datos históricos de siniestralidad de tránsito.

---

## 2. Matriz de Decisión Multicriterio Ponderada

Para fundamentar la selección tecnológica de datos se aplicó una matriz de ponderación con escala 1 a 5:

| Criterio | Peso (%) | MEData / Datos Abiertos | API SODA Dinámica | OpenStreetMap Puro |
| :--- | :---: | :---: | :---: | :---: |
| **Oficialidad y Validez Territorial** | 25% | **5.0** (Oficial Alcaldía) | 5.0 (Misma fuente) | 3.0 (Colaborativa) |
| **Volumen Histórico (>200K registros)**| 20% | **5.0** (270K+ completos) | 3.5 (Requiere paginación) | 1.0 (No aplica a siniestros)|
| **Consistencia Geoespacial** | 20% | **4.2** (Requiere depuración)| 4.2 (Idéntica a MEData) | 4.8 (Alta precisión geométrica)|
| **Autonomía y Reproducibilidad Offline**| 20% | **5.0** (Inmutable local) | 2.5 (Depende de API externa) | 4.0 (Descarga fija XML/PBF) |
| **Viabilidad para Grafos Urbanos** | 15% | 2.0 (Puntos puntuales) | 2.0 (Puntos puntuales) | **5.0** (Estructura topológica nativa) |
| **Puntaje Ponderado Total** | **100%** | **4.39 / 5.00** | 3.64 / 5.00 | 3.31 / 5.00 |

---

## 3. Decisión Arquitectónica: Modelo Híbrido

A partir del análisis multicriterio, se adoptó formalmente la arquitectura híbrida descrita en el [[ADR-001-Enfoque-Siniestros-y-Grafo-OSM]]:
1. **Capa de Incidentes:** Se utiliza el volcado oficial estático de **MEData** (251.150 incidentes limpios persistidos en SQLite local).
2. **Capa de Topología Vial:** Se utiliza la estructura de grafo vial arterial de Medellín inspirada en la cartografía de **OpenStreetMap** (32 nodos de cruce neurálgicos y 84 tramos viales dirigidos).
3. **Fusión Geoespacial con KD-Tree:** Mediante una indexación 2D espacial, el riesgo de los 251.150 siniestros se proyecta sobre la arista vial más cercana en tiempo $\mathcal{O}(n \log |E|)$, permitiendo alimentar las funciones de coste multiobjetivo de Dijkstra y A*.

---

## 🔗 Relacionado
- [[00 - Inicio|Inicio]]
- [[Antecedentes-Academicos]]
- [[Diccionario-Variables]]
- [[Pipeline-Limpieza]]
