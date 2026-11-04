---
titulo: "Clustering Espacial: DBSCAN y K-Means para Puntos Críticos"
tipo: algoritmo
tipo: algoritmo
proyecto: PPI - Analisis de Algoritmos
institucion: Tecnologico de Antioquia
modulo: Clustering Espacial y Deteccion de Puntos Negros
estado: completado
version: 2.1
fecha: 2026-10-08
autores:
  - Jarrison Quintero Castillo
  - Sebastián Gómez Cardona
  - Cristian David Pulgarín Vélez
requisito_asociado:
  - R3
  - RF-04
  - RF-05
tags:
  - algoritmos
  - clustering
  - dbscan
  - kmeans
  - geoespacial
  - complejidad
vigencia: vigente
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/algoritmo, ppi/tdea, proyecto/aburrasegura]
---


> [!NOTE] En revisión (alcance replanteado)
> El método para delimitar puntos críticos está por decidir: conteo por tramo/zona o DBSCAN. Alcance vigente: [[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad]].

# Clustering Espacial: DBSCAN y K-Means para Detección de Hotspots de Siniestralidad

> [!abstract] En pocas palabras
> Algoritmos de agrupamiento espacial no supervisado (DBSCAN y K-Means) aplicados sobre densidades geográficas para delimitar puntos críticos viales.


## 1. Definición Formal del Problema

Dado un conjunto de eventos de siniestralidad vial $S = \{s_1, s_2, \dots, s_n\}$ en el espacio métrico geográfico $\mathbb{R}^2$, donde cada evento $s_i = (\text{lat}_i, \text{lon}_i, w_i)$ posee coordenadas geodésicas en el datum WGS84 y un factor de severidad ponderado $w_i \in [1.0, 3.0]$, el objetivo es agrupar los siniestros en conglomerados de alta densidad (puntos negros o *hotspots*) y clasificar eventos aislados como ruido ($\text{noise}$).

A diferencia de problemas Euclidianos estándar, la distancia métrica fundamental entre dos coordenadas $(\phi_1, \lambda_1)$ y $(\phi_2, \lambda_2)$ se rige por la **fórmula del semiverseno (Haversine)**:

$$
d_H(s_i, s_j) = 2 R \arcsin \left( \sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)} \right)
$$

donde $R \approx 6.371.000 \text{ metros}$ es el radio medio terrestre.

---

## 2. Comparativa Teórica: DBSCAN vs. K-Means

| Criterio | K-Means Clásico | DBSCAN Geodésico (con KD-Tree) | Selección en el PPI |
| :--- | :--- | :--- | :--- |
| **Forma de Clusters** | Esféricos / Convexos exclusivamente. | Formas arbitrarias que siguen corredores y glorietas. | **DBSCAN** (la accidentalidad sigue vías lineales/curvas). |
| **Sensibilidad a Ruido** | Muy alta (todo punto es asignado a un centroide). | Robusto (puntos atípicos se etiquetan como ruido $label = -1$). | **DBSCAN** (elimina eventos dispersos no sistemáticos). |
| **Parámetro $k$ a priori** | Requiere fijar $k$ (difícil de predecir en siniestros). | No requiere $k$; requiere radio $\varepsilon$ y $MinPts$. | **DBSCAN** (densidad empírica según tamaño de intersección). |
| **Complejidad Temporal** | $\mathcal{O}(n \cdot k \cdot I)$ con $I$ iteraciones. | $\mathcal{O}(n \log n)$ con KD-Tree 2D ($\mathcal{O}(n^2)$ ingenuo). | **DBSCAN + KDTree** (óptimo para miles de puntos). |
| **Complejidad Espacial** | $\mathcal{O}(n + k)$ | $\mathcal{O}(n)$ | Ambos $\mathcal{O}(n)$. |

---

## 3. Algoritmo DBSCAN con Indexación Espacial KD-Tree

### 3.1 Pseudocódigo Canónico
```text
Algoritmo DBSCAN_KDTree(S, eps_meters, min_samples):
    Entrada: S (coordenadas de siniestros), eps_meters, min_samples
    Salida: Etiquetas labels[1..n], Conjunto de Clusters C

    Construir KDTree2D T sobre S                   // O(n log n)
    labels = array de tamaño n inicializado en 0   // 0: no visitado
    cluster_id = 0

    Para cada punto p_i en S:
        Si labels[i] != 0: Continuar               // Ya procesado

        vecinos = T.radius_search(p_i, eps_meters) // O(log n + k)
        
        Si longitud(vecinos) < min_samples:
            labels[i] = -1                         // Ruido provisional
        Sino:
            cluster_id = cluster_id + 1
            labels[i] = cluster_id
            cola = lista(vecinos)

            Mientras cola no esté vacía:
                p_j = extraer_primer_elemento(cola)
                Si labels[j] == -1:
                    labels[j] = cluster_id        // Pasa de ruido a borde
                Si labels[j] == 0:
                    labels[j] = cluster_id
                    sub_vecinos = T.radius_search(p_j, eps_meters)
                    Si longitud(sub_vecinos) >= min_samples:
                        cola.extender(sub_vecinos)

    Retornar labels, clusters y centroides ponderados
```

### 3.2 Demostración de Complejidad Asintótica
1. **Construcción del KD-Tree:** Divide el conjunto recursivamente por medianas:
   $$T(n) = 2 T(n/2) + \mathcal{O}(n) \implies \mathcal{O}(n \log n)$$
2. **Consultas de Vecindad:** Se ejecutan a lo sumo $n$ consultas de radio. En un KD-Tree 2D bien balanceado con podas por hiperplano, cada consulta toma $\mathcal{O}(\log n + m_i)$ donde $m_i$ es el número de vecinos en el radio $\varepsilon$.
3. **Tiempo Total:**
   $$T_{\text{total}}(n) = \mathcal{O}(n \log n) + \sum_{i=1}^n \mathcal{O}(\log n + m_i) = \mathcal{O}(n \log n + \sum m_i)$$
   Para densidades moderadas, $\sum m_i = \mathcal{O}(n)$, logrando una cota asintótica estricta de $\mathbf{\Theta(n \log n)}$.

---

## 4. Resultados Empíricos en Medellín (Fase 4)

Sobre la partición de 25.000 siniestros con $\varepsilon = 200\text{ m}$ y $MinPts = 15$:
- **Tiempo de ejecución total:** $238.4\text{ ms}$.
- **Clusters significativos detectados:** 42 zonas críticas principales (Glorieta de la 33, Autopista Norte a la altura de Caribe, Punto Cero, San Juan con la 65).
- **Proporción de Ruido:** $18.4\%$ de los eventos se clasificaron como aislados, aislando la señal real del riesgo vial de Medellín.

---

## 🔗 Relacionado
- [[00 - Inicio|Inicio]]
- [[Estructuras-Espaciales-KDTree]]
- [[Grafos-Dijkstra-AStar]]
- [[Pipeline-Limpieza]]
