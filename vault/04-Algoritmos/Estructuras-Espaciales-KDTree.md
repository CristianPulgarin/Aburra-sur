---
titulo: "Estructuras de Datos Espaciales: KD-Tree 2D para Búsqueda Vecinal"
tipo: algoritmo
tipo: algoritmo
familia: estructuras_datos_espaciales
proyecto: PPI - Analisis de Algoritmos
institucion: Tecnologico de Antioquia
autor: especialista-algoritmos
fecha: 2026-10-08
requisito_asociado:
  - R4
  - RF-04
  - RF-05
vigencia: vigente
base: "[[ADR-001-Enfoque-Siniestros-y-Grafo-OSM]]"
documento_asociado: "AburráSegura.docx (Sección 4.2)"
tags:
  - algoritmos
  - estructuras-espaciales
  - kdtree
  - haversine
  - knn
  - aceleracion
  - latex
estado: vigente
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/algoritmo, ppi/tdea, proyecto/aburrasegura]
---


# Estructuras de Datos Espaciales: KD-Tree 2D y Búsqueda Geodésica

> [!abstract] En pocas palabras
> Implementación y análisis de complejidad de un árbol k-dimensional (KD-Tree 2D) en Python puro para búsquedas eficientes del vecino más cercano en O(log n).


> [!NOTE] Propósito Central en el Proyecto
> El **Árbol $k$-Dimensional (KD-Tree 2D)** resuelve el cuello de botella computacional de proyectar los 251.150 siniestros viales de Medellín a la red vial urbana y ejecutar consultas de proximidad espacial (vecino más cercano y radio de influencia). Transforma la búsqueda lineal exhaustiva ingenua $\mathcal{O}(n)$ en una búsqueda jerárquica con podas por hiperplano en tiempo cuasi-logarítmico $\mathcal{O}(\log n)$, logrando una **aceleración empírica medida de hasta 4.018,3×**.

---

## 1. Fundamentación Teórica del KD-Tree 2D (Bentley, 1975)

Un **KD-Tree** (K-Dimensional Tree) es una estructura de datos basada en árboles binarios de búsqueda que generaliza la partición jerárquica del espacio métrico a $k$ dimensiones ortogonales.

En el contexto geográfico de Medellín, el espacio se modela en $k = 2$ dimensiones:
- **Eje 0 ($y$):** Latitud geodésica ($\phi$).
- **Eje 1 ($x$):** Longitud geodésica ($\lambda$).

### 1.1 Regla de Partición Alternada por Medianas
En cada nivel de profundidad $d \ge 0$, el hiperplano divisor se alinea con el eje ortogonal:

$$\text{eje}(d) = d \pmod 2$$

Para garantizar que el árbol sea estrictamente balanceado con altura mínima:

$$h = \lfloor \log_2 n \rfloor$$

el conjunto de puntos se ordena según la coordenada correspondiente al eje actual y se selecciona como raíz del subárbol el elemento que ocupa la **mediana exacta**:

$$p_{\text{mediana}} = A\left[\left\lfloor \frac{|A|}{2} \right\rfloor\right]$$

- El subárbol izquierdo contendrá todos los puntos con coordenada menor a la mediana:
  $$L = \{p \in A : p[\text{eje}] < p_{\text{mediana}}[\text{eje}]\}$$
- El subárbol derecho contendrá los puntos restantes con coordenada mayor o igual:
  $$R = \{p \in A : p[\text{eje}] \ge p_{\text{mediana}}[\text{eje}] \land p \ne p_{\text{mediana}}\}$$

---

## 2. Métrica Geodésica de Semiverseno (Haversine)

Dado que la superficie terrestre es un geoide esferoidal, el uso de la distancia euclidiana cartesiana introduce distorsiones métricas inaceptables. Se utiliza la **fórmula geodésica de Haversine** para calcular la distancia de círculo máximo sobre la esfera terrestre:

$$d_H(p_1, p_2) = 2 R \arcsin \left( \sqrt{ \sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right) } \right)$$

donde:
- $R = 6.371.000\text{ metros}$ (radio medio de la Tierra).
- $\Delta \phi = \text{rad}(\phi_2 - \phi_1)$ (diferencia de latitudes en radianes).
- $\Delta \lambda = \text{rad}(\lambda_2 - \lambda_1)$ (diferencia de longitudes en radianes).

### Factor de Escala Local para Podas por Hiperplano:
Para evaluar si una rama del KD-Tree puede ser podada durante una búsqueda con radio en metros, se proyecta la diferencia angular del eje divisor a metros lineales en Medellín (latitud media $\approx 6.25^\circ$):
- **Eje de Latitud ($y$):** $1^\circ \approx 111.139\text{ metros}$.
- **Eje de Longitud ($x$):** $1^\circ \approx 111.139 \cdot \cos(6.25^\circ) \approx 110.476\text{ metros}$.

---

## 3. Pseudocódigos Canónicos

Implementados desde cero en `app/algorithms/spatial_kdtree.py`:

### 3.1 Construcción Recursiva del KD-Tree 2D ($\mathcal{O}(n \log n)$)
```text
Algoritmo Construir_KDTree(puntos, profundidad):
    Si puntos esta vacio:
        Retornar Nulo

    eje = profundidad mod 2
    Ordenar puntos segun puntos[i].coord[eje]
    medio = longitud(puntos) div 2

    nodo = NuevoNodo(punto = puntos[medio], eje = eje)
    nodo.izquierdo = Construir_KDTree(puntos[0 .. medio-1], profundidad + 1)
    nodo.derecho = Construir_KDTree(puntos[medio+1 .. final], profundidad + 1)

    Retornar nodo
```

### 3.2 Búsqueda de Vecino Más Cercano (1-NN) con Poda por Hiperplano
```text
Algoritmo Vecino_Mas_Cercano(nodo, objetivo, mejor_nodo, mejor_dist):
    Si nodo es Nulo:
        Retornar (mejor_nodo, mejor_dist)

    d = Haversine(nodo.punto, objetivo)
    Si d < mejor_dist:
        mejor_dist = d
        mejor_nodo = nodo

    eje = nodo.eje
    dist_eje_grados = objetivo[eje] - nodo.punto[eje]
    dist_eje_metros = |dist_eje_grados| * EscalaMetros(eje)

    // Explorar primero la rama donde se encuentra el objetivo
    (primera_rama, segunda_rama) = (nodo.izq, nodo.der) si dist_eje_grados < 0 sino (nodo.der, nodo.izq)

    (mejor_nodo, mejor_dist) = Vecino_Mas_Cercano(primera_rama, objetivo, mejor_nodo, mejor_dist)

    // Regla de poda geometrica: Solo explorar segunda rama si cruza el hiperplano
    Si dist_eje_metros < mejor_dist:
        (mejor_nodo, mejor_dist) = Vecino_Mas_Cercano(segunda_rama, objetivo, mejor_nodo, mejor_dist)

    Retornar (mejor_nodo, mejor_dist)
```

---

## 4. Demostración Matemática de Complejidad Asintótica

### 4.1 Complejidad Temporal de Construcción
La construcción requiere ordenar el arreglo de tamaño $n$ en cada nivel de recursión mediante la mediana:
$$T(n) = 2 T(n/2) + \Theta(n \log n) \quad \text{(usando ordenamiento)} \quad \text{o} \quad T(n) = 2 T(n/2) + \Theta(n) \quad \text{(usando Quickselect)}$$
Con mediana exacta calculada en tiempo lineal $\Theta(n)$, aplicando el Teorema Maestro con $a = 2, b = 2, f(n) = \Theta(n)$:
$$n^{\log_b a} = n^1 = n \implies f(n) = \Theta(n) \implies T(n) = \mathbf{\Theta(n \log n)}$$

### 4.2 Complejidad Temporal de Consulta (1-NN)
- **Caso Promedio:** Si los puntos están distribuidos de forma cuasi-uniforme en el plano espacial urbano, el hiperplano de poda descarta la gran mayoría de las subramas lejanas. La búsqueda desciende por una sola trayectoria principal del árbol:
  $$T_{\text{promedio}}(n) = \mathbf{\Theta(\log n)}$$
- **Peor Caso Teórico:** En configuraciones patológicas altamente degeneradas donde el radio de búsqueda intercepta recursivamente todos los hiperplanos divisores:
  $$T_{\text{peor}}(n) = \mathbf{\mathcal{O}(n)}$$
  *(En la práctica sobre la cartografía de Medellín, la cota observada es estrictamente logarítmica).*

### 4.3 Complejidad Espacial
Cada nodo almacena las coordenadas del punto, metadatos y punteros a los hijos izquierdo y derecho. Para $n$ elementos:
$$S(n) = \mathbf{\Theta(n)}$$
La pila de llamadas de la recursión está acotada por la altura del árbol: $\mathcal{O}(\log n)$.

---

## 5. Validación Experimental y Aceleración Empírica Frente a Búsqueda Lineal

Pruebas ejecutadas sobre particiones reales de siniestros de Medellín con **50 consultas geoespaciales simultáneas** (`data/benchmarks/benchmark_results_fase4.json`):

| Puntos en el Espacio ($n$) | Consultas ($q$) | KD-Tree 2D Medido (ms) | Búsqueda Lineal $\mathcal{O}(n)$ (ms) | Factor de Aceleración (Speedup Medido) | Cota Teórica $\frac{n}{\log_2 n}$ |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **$1.000$** | 50 | $8{,}54\text{ ms}$ | $98{,}21\text{ ms}$ | **$11{,}5\times$** | $100{,}3\times$ |
| **$10.000$** | 50 | $5{,}67\text{ ms}$ | $1.383{,}49\text{ ms}$ | **$244{,}2\times$** | $752{,}6\times$ |
| **$50.000$** | 50 | $5{,}67\text{ ms}$ | $5.271{,}52\text{ ms}$ | **$929{,}1\times$** | $3.203{,}2\times$ |
| **$100.000$** | 50 | $6{,}13\text{ ms}$ | $11.372{,}14\text{ ms}$ | **$1.856{,}2\times$** | $6.020{,}6\times$ |
| **$200.000$** | 50 | **$5{,}34\text{ ms}$** | **$21.458{,}12\text{ ms}$ (21,4 s)** | **$4.018{,}3\times$** | $11.363{,}6\times$ |

### Análisis de Resultados:
1. **Comportamiento Cuasi-Plano del KD-Tree:** El tiempo de respuesta de las 50 consultas espaciales con KD-Tree se mantiene virtualmente plano entre **$5{,}3$ y $8{,}5$ milisegundos** aun cuando el conjunto de datos se multiplica por 200 (de 1.000 a 200.000 registros).
2. **Crecimiento Lineal Inviable:** La búsqueda lineal exhaustiva escala de forma estrictamente proporcional a $n$: de $98\text{ ms}$ en 1K a más de **$21{,}4$ segundos** en 200K, tornando inviable su uso en aplicaciones interactivas de mapas.
3. **Speedup de 4.018,3×:** A escala urbana masiva, el KD-Tree reduce la latencia en más de 4 órdenes de magnitud, demostrando la trascendencia práctica del diseño formal de estructuras de datos espaciales.

---

## Trazabilidad
- **Código Fuente:** `app/algorithms/spatial_kdtree.py`
- **Suite Pytest:** `tests/test_kdtree.py` (3 pruebas que validan árbol vacío, equivalencia matemática exacta punto a punto contra búsqueda lineal y consultas $k$-NN con Max-Heap; 100% PASS).
- **Integración con otros módulos:** Alimenta la vecindad de radio de [[Clustering-DBSCAN-KMeans]] y la proyección de coordenadas en [[Grafos-Dijkstra-AStar]].
- **Documento:** `AburráSegura.docx` — Sección 4.2.

---

## 🔗 Relacionado
- [[00 - Inicio|Inicio]]
- [[Grafos-Dijkstra-AStar]]
- [[Clustering-DBSCAN-KMeans]]
- [[ADR-003-Geocodificacion-y-Enrutamiento-Continuo-Tipo-Google-Maps|ADR-003]]
