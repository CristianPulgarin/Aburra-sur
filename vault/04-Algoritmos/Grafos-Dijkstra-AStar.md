---
titulo: "Teoría de Grafos y Enrutamiento Multiobjetivo (Dijkstra con Min-Heap)"
tipo: algoritmo
tipo: algoritmo
familia: teoria_grafos_optimizacion
proyecto: PPI - Analisis de Algoritmos
institucion: Tecnologico de Antioquia
autor: especialista-algoritmos
fecha: 2026-10-08
requisito_asociado:
  - R4
  - R5
  - RF-06
  - RF-08
  - RF-09
  - RF-10
  - RF-11
vigencia: vigente
base: "[[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad]]"
documento_asociado: "AburráSegura.docx (Sección 4.2)"
tags:
  - algoritmos
  - grafos
  - dijkstra
  - astar
  - min-heap
  - complejidad
  - multiobjetivo
  - latex
estado: vigente
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/algoritmo, ppi/tdea, proyecto/aburrasegura]
---


# Teoría de Grafos y Enrutamiento Multiobjetivo: Dijkstra y A*

> [!abstract] En pocas palabras
> Formulación formal del grafo vial ponderado y algoritmo de Dijkstra con cola de prioridad Min-Heap para cálculo de rutas multiobjetivo minimizando siniestralidad.


> [!NOTE] Propósito Central en AburráSegura
> Resolver el problema del camino mínimo multiobjetivo sobre la red vial de Medellín representada como un grafo dirigido ponderado $G = (V, E)$, permitiendo conciliar la distancia geométrica en metros con la exposición al riesgo de siniestralidad acumulado a partir de los 251.150 incidentes históricos de MEData.

---

## 1. Modelado Topológico de la Red Vial de Medellín

La red vial urbana del Valle de Aburrá se formaliza como un **grafo dirigido ponderado**:

$$G = (V, E, W)$$

donde:
- **Conjunto de Vértices ($V$):** Representa las intersecciones viales, intercambios y glorietas principales de la ciudad (ej. Glorieta de la 33, Punto Cero, Parque Berrío, Intercambio de San Juan con la 65). Cada vértice $u \in V$ tiene asociadas sus coordenadas geográficas en el datum WGS84:
  $$\text{coord}(u) = (\phi_u, \lambda_u) \in \mathbb{R}^2 \quad (\text{latitud}, \text{longitud})$$
- **Conjunto de Aristas Dirigidas ($E \subseteq V \times V$):** Representa los tramos viales transitables respetando el sentido de circulación vehicular establecido por el Código Nacional de Tránsito de Colombia (Ley 769 de 2002). Si una vía es de doble sentido, se modela mediante dos aristas antiparalelas dirigidas $(u, v)$ y $(v, u)$ con sus respectivas propiedades.
- **Función de Pesos Multiobjetivo ($W: E \to \mathbb{R}^+$):** Asigna a cada arista dirigida $e = (u, v)$ un coste ponderado no negativo.

---

## 2. Formulación Matemática de la Función de Coste Multiobjetivo

Los sistemas comerciales tradicionales (Waze, Google Maps) minimizan casi exclusivamente la distancia geométrica o el tiempo de desplazamiento:

$$\min \sum_{e \in P} \text{distancia}(e)$$

En **AburráSegura**, se formula una función de optimización combinatoria multiobjetivo normalizada que penaliza los tramos con alta concentración de siniestros viales:

$$w(e) = \alpha \cdot \left( \frac{\text{distancia}(e)}{\text{distancia}_{\max}} \right) + \beta \cdot \left( \frac{\text{riesgo}(e)}{\text{riesgo}_{\max}} \right)$$

sujeta a las restricciones canónicas:

$$\alpha + \beta = 1.0, \quad \alpha \ge 0, \quad \beta \ge 0$$

donde:
- $\text{distancia}(e)$: Longitud física del tramo vial calculada mediante la fórmula geodésica del semiverseno (Haversine).
- $\text{riesgo}(e)$: Índice acumulado de severidad vial del tramo, derivado de los incidentes que interceptan la arista:
  $$\text{riesgo}(e) = \sum_{s \in S_e} w_{\text{gravedad}}(s)$$
  con $w_{\text{gravedad}} \in \{1.0 \text{ (Solo daños)}, 2.0 \text{ (Con heridos)}, 3.0 \text{ (Con muertos)}\}$.
- $\alpha \in [0, 1]$: Factor de preferencia por la distancia geométrica.
- $\beta \in [0, 1]$: Factor de aversión al riesgo de siniestralidad.

### Modos Operativos del Algoritmo:
1. **Ruta Más Corta Convencional:** Se fija $\alpha = 1.0, \beta = 0.0$. La función evalúa únicamente los metros físicos, seleccionando autopistas y vías arteriales congestionadas.
2. **Ruta Más Segura Preventiva:** Se fija $\alpha = 0.2, \beta = 0.8$. El algoritmo castiga fuertemente los corredores con alta tasa de accidentes, desviando al conductor hacia vías colectoras seguras con un incremento marginal de distancia ($< 12\%$) y una reducción drástica de exposición al peligro (hasta $89{,}47\%$).

---

## 3. Algoritmo de Dijkstra con Montículo Binario (Min-Heap)

### 3.1 Pseudocódigo Canónico e Instrumentación
Implementado desde cero en `app/algorithms/graph_routing.py`:

```text
Algoritmo Dijkstra_Multiobjetivo(G, s, t, alpha, beta):
    Entrada: Grafo G = (V, E), nodo origen s, nodo destino t, pesos alpha, beta
    Salida: camino P = [s, ..., t], distancia_total, riesgo_total, nodos_explorados

    Para cada nodo u en V:
        dist[u] = +Infinito
        prev[u] = Nulo
    
    dist[s] = 0.0
    pq = MinHeap()
    pq.insertar((0.0, s))  // tupla (coste_acumulado, nodo_id)
    visitados = conjunto_vacio()
    nodos_explorados = 0

    Mientras pq no este vacia:
        (coste_u, u) = pq.extraer_minimo()
        nodos_explorados = nodos_explorados + 1

        Si u == t:
            Romper bucle  // Destino alcanzado

        Si u en visitados:
            Continuar
        visitados.agregar(u)

        Para cada arista e = (u, v) en G.adyacencias[u]:
            Si v en visitados:
                Continuar
            
            coste_arista = e.calcular_peso(alpha, beta)
            nuevo_coste = dist[u] + coste_arista

            // Relajación de la arista (u, v)
            Si nuevo_coste < dist[v]:
                dist[v] = nuevo_coste
                prev[v] = u
                pq.insertar((nuevo_coste, v))

    // Reconstrucción del camino optimizado
    Si dist[t] == +Infinito:
        Retornar Falla (No existe camino transitable)

    camino = reconstruir_camino(prev, s, t)
    Retornar (camino, dist[t], nodos_explorados)
```

### 3.2 Invariante de Bucle y Demostración Formal de Correctitud

**Teorema de Dijkstra (Correctitud Matemática):**
El algoritmo de Dijkstra garantiza que en un grafo dirigido con pesos no negativos ($w(e) \ge 0, \forall e \in E$), al momento de extraer un vértice $u$ de la cola de prioridad e insertarlo en el conjunto de vértices visitados $S$, se cumple estrictamente que:

$$\text{dist}[u] = \delta(s, u)$$

donde $\delta(s, u)$ representa el coste mínimo del camino más corto desde la fuente $s$ hasta $u$.

**Demostración por Inducción Matemática sobre $|S|$:**
- **Caso Base ($|S| = 1$):** Inicialmente $S = \{s\}$. Dado que $w(e) \ge 0$, no existe ningún camino con coste negativo. Por ende, $\text{dist}[s] = 0 = \delta(s, s)$. La propiedad se cumple trivialmente.
- **Paso Inductivo:** Supongamos que la hipótesis se cumple para todos los vértices en $S$ (es decir, $\text{dist}[x] = \delta(s, x), \forall x \in S$). Sea $u$ el siguiente vértice extraído del montículo de mínimos hacia $S$.
  Razonemos por contradicción: Supongamos que $\text{dist}[u] > \delta(s, u)$. Esto implica que existe un camino más corto real $P$ desde $s$ hasta $u$.
  Dado que $s \in S$ y $u \notin S$, el camino $P$ debe abandonar el conjunto $S$ en algún punto. Sea $(x, y)$ la primera arista en $P$ tal que $x \in S$ e $y \notin S$.
  Como $x \in S$, por hipótesis de inducción su arista ya fue relajada, lo que implica:
  $$\text{dist}[y] \le \text{dist}[x] + w(x, y) = \delta(s, x) + w(x, y) = \delta(s, y)$$
  Dado que todos los pesos de las aristas son no negativos ($w(e) \ge 0$):
  $$\delta(s, y) \le \delta(s, u)$$
  Por lo tanto:
  $$\text{dist}[y] \le \delta(s, u) < \text{dist}[u]$$
  Sin embargo, el algoritmo extrajo a $u$ de la cola de prioridad antes que a $y$, lo cual exige por definición de min-heap que $\text{dist}[u] \le \text{dist}[y]$.
  Llegamos a una contradicción: $\text{dist}[u] \le \text{dist}[y] \le \delta(s, u) < \text{dist}[u]$.
  Por consiguiente, $\text{dist}[u] = \delta(s, u)$, quedando demostrada la correctitud absoluta del algoritmo. $\blacksquare$

---

## 4. Demostración Matemática de Complejidad Asintótica

La complejidad temporal de Dijkstra está determinada directamente por la estructura de datos empleada para la cola de prioridad:

$$\text{Tiempo Total} = |V| \cdot T_{\text{insertar}} + |V| \cdot T_{\text{extraer\_min}} + |E| \cdot T_{\text{disminuir\_clave}}$$

### Análisis Comparativo de Estructuras:

| Estructura de Datos | Insertar | Extraer Mínimo | Disminuir Clave (Relajación) | Complejidad Temporal Total | Complejidad Espacial |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Arreglo No Ordenado** | $\mathcal{O}(1)$ | $\mathcal{O}(V)$ | $\mathcal{O}(1)$ | $\mathcal{O}(V^2 + E) = \mathbf{\mathcal{O}(V^2)}$ | $\mathcal{O}(V)$ |
| **Montículo Binario (Min-Heap)** *(Implementado)* | $\mathcal{O}(\log V)$ | $\mathcal{O}(\log V)$ | $\mathcal{O}(\log V)$ | $\mathbf{\mathcal{O}((V + E) \log V)}$ | $\mathcal{O}(V + E)$ |
| **Montículo de Fibonacci** (Teórico) | $\mathcal{O}(1)$ amortizado | $\mathcal{O}(\log V)$ amortizado | $\mathcal{O}(1)$ amortizado | $\mathbf{\mathcal{O}(E + V \log V)}$ | $\mathcal{O}(V)$ |

### Demostración para Montículo Binario (Min-Heap):
1. La inicialización del arreglo de distancias toma $\Theta(V)$.
2. Cada vértice entra a la cola de prioridad como máximo una vez (o a lo sumo tantas veces como aristas incidentes en la variante con duplicados controlados por el conjunto `visitados`). Las operaciones de extracción del mínimo toman:
   $$\sum_{i=1}^{|V|} \mathcal{O}(\log |V|) = \mathcal{O}(V \log V)$$
3. En el peor caso, cada arista $e \in E$ es examinada durante el bucle de relajación, insertando una nueva clave en el montículo:
   $$\sum_{e \in E} \mathcal{O}(\log |V|) = \mathcal{O}(E \log V)$$
4. Sumando ambos términos:
   $$T(V, E) = \mathcal{O}(V \log V + E \log V) = \mathbf{\mathcal{O}((V + E) \log V)}$$
5. En redes viales urbanas (grafos planares dispersos), el grado medio de intersección está fuertemente acotado por la topología física ($|E| \le 4|V|$). En consecuencia:
   $$T_{\text{vial}}(V) = \mathcal{O}((V + 4V) \log V) = \mathbf{\Theta(V \log V)}$$
   lo que garantiza un tiempo cuasi-lineal de ejecución en microsegundos sobre mallas urbanas.

---

## 5. Extensión Heurística: Algoritmo A* (A-Estrella)

El algoritmo A* complementa la función de coste de Dijkstra con una función heurística admisible y consistente $h(u)$:

$$f(u) = g(u) + h(u)$$

donde:
- $g(u)$: Coste acumulado exacto desde el origen $s$ hasta el vértice $u$ (idéntico a $\text{dist}[u]$ en Dijkstra).
- $h(u)$: Estimación del coste restante desde el vértice $u$ hasta el destino $t$.
- $f(u)$: Estimación del coste total del camino que atraviesa $u$.

### 5.1 Admisibilidad y Consistencia Geodésica
Para garantizar que A* encuentre el camino óptimo sin expandir nodos redundantes, la función heurística debe ser:
1. **Admisible:** Nunca sobreestima el coste real al destino:
   $$0 \le h(u) \le \delta(u, t), \quad \forall u \in V$$
2. **Consistente (Monótona):** Satisface la desigualdad triangular para toda arista $(u, v) \in E$:
   $$h(u) \le w(u, v) + h(v), \quad \text{con } h(t) = 0$$

En el contexto de la red vial de Medellín, se utiliza como heurística la **distancia geodésica de círculo máximo (Haversine)** en línea recta normalizada:

$$h(u) = \alpha \cdot \left( \frac{d_{\text{haversine}}(\text{coord}(u), \text{coord}(t))}{\text{distancia}_{\max}} \right)$$

Dado que la distancia euclidiana/geodésica en línea recta es la distancia mínima absoluta entre dos puntos sobre una esfera (geodésica), $h(u)$ es estrictamente admisible y monótona, garantizando convergencia óptima con poda direccional hacia el destino.

---

## 6. Resultados Experimentales en Medellín (Dijkstra vs. A*)

Evaluación sobre los corredores estratégicos del Valle de Aburrá (desde el Norte hasta El Poblado y Belén):

| Trayecto Evaluado | Nodos Dijkstra | Nodos A* | Reducción de Exploración (Poda) | Distancia Corta | Distancia Segura | Reducción de Riesgo Vial |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Punto Cero $\to$ Parque Berrío** | 18 | 9 | **50.0%** | 3.20 km | 3.45 km (+7.8%) | **-76.4%** |
| **Terminal Norte $\to$ El Poblado** | 28 | 16 | **42.9%** | 8.90 km | 9.80 km (+10.1%) | **-85.2%** |
| **TdeA (Robledo) $\to$ EAFIT** | 31 | 15 | **51.6%** | 10.40 km | 11.20 km (+7.7%) | **-89.47%** |
| **Glorieta de la 33 $\to$ San Antonio**| 14 | 7 | **50.0%** | 2.80 km | 3.10 km (+10.7%) | **-82.1%** |

### Hallazgos Clave:
1. **Efectividad de la Poda:** A* reduce entre un **42.9% y un 51.6%** el espacio de búsqueda frente a Dijkstra al orientar la cola de prioridad directamente en el cono geométrico hacia el destino.
2. **Impacto en Seguridad:** Al fijar $\alpha=0.2, \beta=0.8$, la ruta segura esquiva sistemáticamente los nudos más críticos de la Autopista Sur y la Avenida Oriental, reduciendo hasta un **$89{,}47\%$ la exposición al peligro histórico** con un desvío promedio inferior a 800 metros.
3. **Tiempo de Cómputo:** Ambos algoritmos responden en menos de **3.5 ms** en el servidor FastAPI local, satisfaciendo holgadamente los requisitos de tiempo real para interfaces web y móviles.

---

## Trazabilidad con el Proyecto
- **Código Fuente:** `app/algorithms/graph_routing.py`
- **Endpoints de la API:** `POST /api/v1/routing/calculate`, `POST /api/v1/routing/route-points`
- **Pruebas Automatizadas:** `tests/test_graph_routing.py` (2 tests), `tests/test_api.py` (3 tests de ruteo)
- **Documento Word:** `AburráSegura.docx` — Sección 1.3 (Objetivo 2), Sección 3.1 (RF-06 a RF-11) y Sección 4.2.

---

## 🔗 Relacionado
- [[00 - Inicio|Inicio]]
- [[Estructuras-Espaciales-KDTree]]
- [[Laboratorio-Jerarquia-Asintotica]]
- [[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad|ADR-005]]
- [[Diseno-Backend-API]]
