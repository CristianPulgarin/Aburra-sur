---
titulo: "Algoritmos de Ordenamiento: Análisis Asintótico y Comparativa"
tipo: algoritmo
tipo: algoritmo
familia: ordenamiento
proyecto: PPI - Analisis de Algoritmos
institucion: Tecnologico de Antioquia
autor: especialista-algoritmos
fecha: 2026-10-08
requisito_asociado:
  - R3
  - RF-14
  - RF-15
vigencia: vigente
base: "[[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad]]"
documento_asociado: "AburráSegura.docx (Sección 4.2 y Tabla 5)"
tags:
  - algoritmos
  - ordenamiento
  - mergesort
  - quicksort
  - heapsort
  - countingsort
  - timsort
  - benchmarking
  - latex
estado: vigente
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/algoritmo, ppi/tdea, proyecto/aburrasegura]
---


# Algoritmos de Ordenamiento: Análisis Asintótico y Benchmarking Masivo (1K a 1M)

> [!abstract] En pocas palabras
> Estudio comparativo teórico y empírico de ordenamiento (MergeSort, QuickSort, HeapSort, CountingSort) aplicado a la jerarquización de siniestros viales.


> [!NOTE] Propósito en el Proyecto
> El ordenamiento constituye la piedra angular del análisis asintótico de algoritmos. En este proyecto se implementaron desde cero en Python puro 4 algoritmos clásicos más el algoritmo híbrido nativo de CPython (`Timsort`) para ordenar los siniestros viales por fecha, factor de gravedad o coordenadas geográficas, contrastando sus cotas matemáticas frente a mediciones reales de tiempo de CPU, número de comparaciones de claves y memoria peak.

---

## 1. Análisis Teórico y Demostraciones Asintóticas en LaTeX

### 1.1 Merge Sort (Ordenamiento por Mezcla)
Algoritmo basado en el paradigma **Divide y Vencerás** (Von Neumann, 1945). Divide recursivamente el arreglo por la mitad, ordena cada mitad de forma independiente y luego fusiona las secuencias ordenadas.

- **Pseudocódigo Canónico:**
  ```text
  Algoritmo MergeSort(A):
      Si longitud(A) <= 1: Retornar A
      medio = longitud(A) div 2
      izq = MergeSort(A[0 .. medio-1])
      der = MergeSort(A[medio .. final])
      Retornar Mezclar(izq, der)
  ```
- **Demostración por Teorema Maestro:**
  La ecuación de recurrencia que modela su tiempo de ejecución es:
  $$T(n) = 2 T(n/2) + \Theta(n)$$
  Aplicando el Teorema Maestro de recurrencias ($T(n) = a T(n/b) + f(n)$) con $a = 2, b = 2, f(n) = \Theta(n)$:
  $$\log_b a = \log_2 2 = 1 \implies n^{\log_b a} = n^1 = n$$
  Dado que $f(n) = \Theta(n^{\log_b a}) = \Theta(n)$, aplica el **Caso 2 del Teorema Maestro**:
  $$T(n) = \Theta(n \log n)$$
- **Mejor Caso:** $\Omega(n \log n)$
- **Caso Promedio:** $\Theta(n \log n)$
- **Peor Caso:** $\mathcal{O}(n \log n)$
- **Complejidad Espacial Auxiliar:** $\mathcal{O}(n)$ debido a la creación de subarreglos durante la mezcla.
- **Estabilidad:** **Estable** (preserva el orden relativo original entre registros con idéntica marca de tiempo).

---

### 1.2 Quick Sort con Partición de Hoare y Pivote Mediana de Tres
Algoritmo de particionamiento in-place (Hoare, 1961) optimizado con una regla de selección de pivote mediante la mediana entre el primer elemento, el elemento medio y el último elemento ($A[\text{low}], A[\text{mid}], A[\text{high}]$), e implementado con una **pila explícita** para acotar la memoria auxiliar a $\mathcal{O}(\log n)$.

- **Pseudocódigo Iterativo con Pila Acotada:**
  ```text
  Algoritmo QuickSort_Iterativo(A):
      Si longitud(A) <= 1: Retornar A
      pila = [(0, longitud(A) - 1)]

      Mientras pila no este vacia:
          (low, high) = pila.desapilar()
          Si low >= high: Continuar

          pivote = MedianaDeTres(A[low], A[(low+high)//2], A[high])
          p = ParticionHoare(A, low, high, pivote)

          // Acotar profundidad apilando primero la particion mas grande
          Si (p - low + 1) > (high - p):
              pila.apilar((low, p))
              pila.apilar((p + 1, high))
          Sino:
              pila.apilar((p + 1, high))
              pila.apilar((low, p))
  ```
- **Análisis de Complejidad Temporal:**
  - **Caso Promedio:** Con particiones balanceadas proporcionales ($1/10$ a $9/10$), la recurrencia $T(n) = T(\alpha n) + T((1-\alpha) n) + \Theta(n)$ resuelve a:
    $$T_{\text{promedio}}(n) = \Theta(n \log n)$$
  - **Peor Caso:** Ocurre si el pivote divide el arreglo en tamaños $0$ y $n-1$:
    $$T(n) = T(n-1) + \Theta(n) \implies \sum_{i=1}^n i = \mathcal{O}(n^2)$$
    *Mitigación:* La selección del pivote mediante **mediana de tres** elimina de forma práctica el peor caso en datos ya ordenados o inversamente ordenados.
- **Complejidad Espacial:** Al procesar primero la partición más pequeña en la pila explícita, la profundidad de la pila se restringe estrictamente a $\mathcal{O}(\log n) \le 30$ registros, evitando desbordamientos de pila (`RecursionError`) incluso para $n = 1.000.000$.
- **Estabilidad:** **No estable**.

---

### 1.3 Heap Sort (Ordenamiento por Montículo)
Algoritmo de ordenamiento basado en la estructura de árbol binario casi completo Max-Heap (Williams, 1964). Transforma el arreglo en un montículo in-place y extrae sucesivamente la raíz máxima.

- **Demostración de Complejidad por Fases:**
  1. **Fase 1: Construcción del Montículo (Build-Max-Heap):**
     Aunque una cota trivial sugiere $\mathcal{O}(n \log n)$, un análisis exacto por niveles demuestra que un montículo de altura $h = \lfloor \log_2 n \rfloor$ tiene a lo sumo $\lceil n / 2^{h+1} \rceil$ nodos a altura $h$. El coste total de amortización es:
     $$\sum_{h=0}^{\lfloor \log_2 n \rfloor} \left\lceil \frac{n}{2^{h+1}} \right\rceil \mathcal{O}(h) = \mathcal{O}\left( n \sum_{h=0}^\infty \frac{h}{2^h} \right)$$
     Dado que la serie convergente $\sum_{h=0}^\infty \frac{h}{2^h} = 2$, se demuestra formalmente que:
     $$T_{\text{build}}(n) = \mathbf{\Theta(n)}$$
  2. **Fase 2: Extracción Sucesiva del Máximo ($n-1$ pasos):**
     Cada llamada a `heapify` sobre la raíz toma a lo sumo la altura del árbol ($\mathcal{O}(\log i)$):
     $$\sum_{i=1}^{n-1} \mathcal{O}(\log i) = \mathbf{\Theta(n \log n)}$$
  3. **Tiempo Total:**
     $$T(n) = \Theta(n) + \Theta(n \log n) = \mathbf{\Theta(n \log n)}$$
- **Mejor, Promedio y Peor Caso:** $\Theta(n \log n)$ en todos los escenarios posibles.
- **Complejidad Espacial:** $\mathbf{\mathcal{O}(1)}$ estrictamente in-place (no requiere memoria auxiliar).
- **Estabilidad:** **No estable**.

---

### 1.4 Counting Sort (Ordenamiento por Conteo)
Algoritmo de ordenamiento no comparativo para claves enteras discretas acotadas en un rango $[min\_val, max\_val]$ (ej. código de comuna $1\dots16$ o factor de gravedad $1\dots3$).

- **Análisis de Complejidad:**
  Sea $k = max\_val - min\_val + 1$ el rango del dominio entero:
  1. Inicialización del arreglo de frecuencias: $\Theta(k)$.
  2. Histograma de conteo sobre los $n$ elementos: $\Theta(n)$.
  3. Reconstrucción del arreglo ordenado: $\Theta(n + k)$.
  $$T(n) = \mathbf{\Theta(n + k)}$$
  Cuando $k = \mathcal{O}(n)$ (dominio acotado), el algoritmo corre en **tiempo estrictamente lineal $\Theta(n)$**, superando la barrera teórica $\Omega(n \log n)$ de los algoritmos de comparación.
- **Complejidad Espacial:** $\mathcal{O}(k)$ para el arreglo de contadores.
- **Estabilidad:** Estable en su versión con arreglo acumulativo.

---

### 1.5 Timsort (Algoritmo Híbrido Nativo de Python / C)
Diseñado por Tim Peters (2002), combina Merge Sort con Insertion Sort adaptativo. Detecta secuencias naturales ya ordenadas (*runs*) y las fusiona mediante una pila balanceada.
- **Mejor Caso:** $\Omega(n)$ en datos previamente ordenados.
- **Caso Promedio y Peor Caso:** $\mathcal{O}(n \log n)$.
- **Implementación:** Escrito en lenguaje C de bajo nivel dentro del intérprete de CPython, sirviendo como estándar de referencia industrial de alto rendimiento.

---

## 2. Resultados Empíricos de Benchmarking Masivo ($n = 1.000$ a $n = 1.000.000$)

Mediciones sobre hardware AMD Ryzen 5 3550H (4 núcleos / 8 hilos a 2.10 GHz, 16 GB RAM DDR4, Windows 11) con Python 3.14.3 (`data/benchmarks/benchmark_results_fase4.json`):

| Tamaño ($n$) | Quick Sort (Hoare+M3) | Merge Sort Puro | Heap Sort In-Place | Counting Sort Lineal | Timsort (CPython C) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **$n = 1.000$** | **$5{,}65\text{ ms}$**<br>($15.964$ comps) | **$10{,}10\text{ ms}$**<br>($8.696$ comps) | **$11{,}94\text{ ms}$**<br>($16.822$ comps) | **$0{,}53\text{ ms}$**<br>($2.000$ ops) | **$0{,}12\text{ ms}$**<br>($4.982$ comps) |
| **$n = 10.000$** | **$78{,}94\text{ ms}$**<br>($201.979$ comps) | **$159{,}30\text{ ms}$**<br>($120.448$ comps) | **$149{,}83\text{ ms}$**<br>($235.431$ comps) | **$1{,}92\text{ ms}$**<br>($20.000$ ops) | **$1{,}70\text{ ms}$**<br>($66.438$ comps) |
| **$n = 50.000$** | **$418{,}40\text{ ms}$**<br>($1.152.787$ comps) | **$734{,}10\text{ ms}$**<br>($718.084$ comps) | **$1.061{,}01\text{ ms}$**<br>($1.409.640$ comps) | **$9{,}90\text{ ms}$**<br>($100.000$ ops) | **$13{,}86\text{ ms}$**<br>($390.241$ comps) |
| **$n = 100.000$** | **$843{,}89\text{ ms}$**<br>($2.388.133$ comps) | **$1.653{,}87\text{ ms}$**<br>($1.536.122$ comps) | **$2.315{,}55\text{ ms}$**<br>($3.020.429$ comps) | **$22{,}34\text{ ms}$**<br>($200.000$ ops) | **$34{,}17\text{ ms}$**<br>($830.482$ comps) |
| **$n = 500.000$** | **$5.206{,}43\text{ ms}$**<br>($13.555.939$ comps) | **$9.572{,}28\text{ ms}$**<br>($8.836.661$ comps) | **$12.887{,}82\text{ ms}$**<br>($17.397.779$ comps) | **$140{,}92\text{ ms}$**<br>($1.000.000$ ops) | **$238{,}66\text{ ms}$**<br>($4.732.892$ comps) |
| **$n = 1.000.000$** | **$12.548{,}67\text{ ms}$**<br>($28.954.171$ comps) | **$20.155{,}81\text{ ms}$**<br>($18.606.859$ comps) | **$27.137{,}15\text{ ms}$**<br>($36.633.522$ comps) | **$247{,}59\text{ ms}$**<br>($2.000.000$ ops) | **$631{,}77\text{ ms}$**<br>($9.965.784$ comps) |

---

## 3. Síntesis Comparativa y Análisis de Rendimiento

| Algoritmo | Mejor Caso | Caso Promedio | Peor Caso | Memoria Auxiliar | Estabilidad | Constante $c$ Medida |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Quick Sort (Hoare+M3)** | $\Omega(n \log n)$ | $\Theta(n \log n)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(\log n)$ | No | **$508 - 625\text{ ns}$** |
| **Merge Sort** | $\Omega(n \log n)$ | $\Theta(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n)$ | **Sí** | **$940 - 1.198\text{ ns}$** |
| **Heap Sort** | $\Omega(n \log n)$ | $\Theta(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathbf{\mathcal{O}(1)}$ | No | **$1.150 - 1.450\text{ ns}$** |
| **Counting Sort** | $\Omega(n + k)$ | $\Theta(n + k)$ | $\mathcal{O}(n + k)$ | $\mathcal{O}(k)$ | **Sí** | **$120 - 140\text{ ns}$** |
| **Timsort (Nativo)** | $\Omega(n)$ | $\Theta(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n)$ | **Sí** | **$25 - 45\text{ ns}$ (C puro)** |

### Conclusiones del Estudio Experimental:
1. **Comportamiento de Quick Sort vs. Merge Sort:** Aunque Merge Sort realiza formalmente menos comparaciones de claves ($18{,}6\text{M}$ vs. $28{,}9\text{M}$ en $n=1\text{M}$), Quick Sort es aproximadamente un **$38\%$ más rápido en tiempo de reloj** ($12{,}5\text{ s}$ vs. $20{,}1\text{ s}$). Esto se debe a que Quick Sort opera in-place sin la sobrecarga de asignación dinámica de memoria y copia de arreglos en CPython.
2. **Estabilidad de Pila:** La regla de apilamiento priorizado garantizó cero fallos por recursión profunda en la partición extrema de 1 millón de elementos.
3. **Eficiencia Lineal:** Counting Sort procesa 1 millón de registros en solo **$0{,}247$ segundos**, confirmando la supremacía asintótica de los métodos no comparativos sobre atributos enteros discretizados (como comunas o gravedades).

---

## Trazabilidad
- **Código:** `app/algorithms/sorting.py`
- **Suite Pytest:** `tests/test_sorting.py` (14 pruebas unitarias que cubren listas vacías, unitarias, duplicados masivos y orden inverso; 100% PASS).
- **Documento:** `AburráSegura.docx` — Tabla 5 y Sección 4.2.

---

## 🔗 Relacionado
- [[00 - Inicio|Inicio]]
- [[Laboratorio-Jerarquia-Asintotica]]
- [[Protocolo-Experimental]]
- [[Grafos-Dijkstra-AStar]]
