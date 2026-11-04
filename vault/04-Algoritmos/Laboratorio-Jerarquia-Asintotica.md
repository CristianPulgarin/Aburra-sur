---
titulo: "Laboratorio de Jerarquía Asintótica: Demostración Empírica"
tipo: algoritmo
tipo: algoritmo
familia: laboratorio_complejidad_asintotica
proyecto: PPI - Analisis de Algoritmos
institucion: Tecnologico de Antioquia
autor: especialista-algoritmos
fecha: 2026-10-08
requisito_asociado:
  - R6
  - RF-14
  - RF-16
vigencia: vigente
base: "[[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad]]"
documento_asociado: "AburráSegura.docx (Sección 2.2, 3.1 y 4.2)"
tags:
  - algoritmos
  - complejidad
  - jerarquia-asintotica
  - big-o
  - benchmarking
  - latex
  - laboratorio
estado: vigente
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/algoritmo, ppi/tdea, proyecto/aburrasegura]
---


# Laboratorio de Jerarquía Asintótica: Demostración Formal y Empírica de $\mathcal{O}(1)$ a $\mathcal{O}(n^2)$

> [!abstract] En pocas palabras
> Banco de pruebas en tiempo real que demuestra experimentalmente las 5 cotas de complejidad (O(1), O(log n), O(n), O(n log n), O(n²)) sobre el dataset vial real.


> [!IMPORTANT] Requerimiento Académico Institucional
> Por solicitud formal de la cátedra de Análisis de Algoritmos (Tecnológico de Antioquia), se diseñó e implementó un **Laboratorio de Complejidad Computacional en Tiempo Real** para evaluar cuantitativamente las cinco clases fundamentales de la jerarquía asintótica sobre los **251.150 incidentes viales reales** de Medellín (MEData):
> $$\mathcal{O}(1) \subset \mathcal{O}(\log n) \subset \mathcal{O}(n) \subset \mathcal{O}(n \log n) \subset \mathcal{O}(n^2)$$

---

## 1. Marco Matemático de Notación Asintótica Formal

En el análisis de algoritmos se emplean cotas formales para clasificar el consumo de recursos (tiempo de procesador $T(n)$ o memoria auxiliar $S(n)$) en función del tamaño de la entrada $n \in \mathbb{N}$:

### 1.1 Cota Superior Asintótica (Notación $\mathcal{O}$-Grande)
Dadas dos funciones $f(n)$ y $g(n)$, se define:

$$\mathcal{O}(g(n)) = \left\{ f(n) : \exists \, c > 0, n_0 > 0 \text{ tales que } 0 \le f(n) \le c \cdot g(n), \; \forall n \ge n_0 \right\}$$

Establece un techo asintótico o peor caso posible de ejecución.

### 1.2 Cota Inferior Asintótica (Notación $\Omega$-Grande)
$$\Omega(g(n)) = \left\{ f(n) : \exists \, c > 0, n_0 > 0 \text{ tales que } 0 \le c \cdot g(n) \le f(n), \; \forall n \ge n_0 \right\}$$

Establece un piso asintótico o mejor caso posible.

### 1.3 Cota Ajustada Asintótica (Notación $\Theta$)
$$\Theta(g(n)) = \left\{ f(n) : \exists \, c_1 > 0, c_2 > 0, n_0 > 0 \text{ tales que } 0 \le c_1 \cdot g(n) \le f(n) \le c_2 \cdot g(n), \; \forall n \ge n_0 \right\}$$

Representa el comportamiento intrínseco del algoritmo cuando las cotas superior e inferior coinciden asintóticamente: $f(n) \in \Theta(g(n)) \iff f(n) \in \mathcal{O}(g(n)) \land f(n) \in \Omega(g(n))$.

---

## 2. Operaciones Canónicas Implementadas sobre los Siniestros de Medellín

Implementadas desde cero en `app/algorithms/complexity_benchmarks.py`:

```mermaid
flowchart TD
    Dataset["251.150 Siniestros MEData"] --> C1["O(1): Acceso Directo por Hash (radicado)"]
    Dataset --> C2["O(log n): Búsqueda Binaria Temporal (fecha)"]
    Dataset --> C3["O(n): Escaneo Secuencial y Filtro (comuna/gravedad)"]
    Dataset --> C4["O(n log n): Merge Sort Puro / Dijkstra con Min-Heap"]
    Dataset --> C5["O(n²): Comparación Exhaustiva por Pares (< 50 m)"]
```

---

### Clase 1: $\mathcal{O}(1)$ — Complejidad Constante (Acceso por Tabla Hash)
- **Operación:** Búsqueda directa de expediente de siniestro a partir de la clave primaria `radicado` (ej. `A00124859`).
- **Pseudocódigo:**
  ```text
  Algoritmo Buscar_Por_Radicado_O1(TablaHash H, radicado_objetivo):
      indice = hash(radicado_objetivo) mod capacidad(H)
      registro = H.obtener(indice)
      Retornar registro  // 1 operación elemental
  ```
- **Fundamento Matemático:**
  Bajo el supuesto de hashing uniforme simple (SUHA), la función de dispersión distribuye las claves uniformemente entre los $m$ casilleros. Con factor de carga $\alpha = n / m \le 0.75$, el tiempo de acceso esperado es:
  $$T(n) = 1 + \alpha = \Theta(1) \subset \mathcal{O}(1)$$
  El tiempo medido de CPU permanece invariante sin importar si el conjunto contiene 1.000 o 250.000 registros.

---

### Clase 2: $\mathcal{O}(\log n)$ — Complejidad Logarítmica (Búsqueda Binaria Iterativa)
- **Operación:** Localizar un siniestro vial por su marca temporal (`fecha`) dentro de una lista ordenada cronológicamente.
- **Pseudocódigo:**
  ```text
  Algoritmo Busqueda_Binaria_Ologn(A_ordenado, fecha_objetivo):
      izq = 0
      der = longitud(A_ordenado) - 1
      comparaciones = 0

      Mientras izq <= der:
          comparaciones = comparaciones + 1
          medio = (izq + der) div 2
          
          Si A[medio].fecha == fecha_objetivo:
              Retornar (medio, comparaciones)
          Sino Si A[medio].fecha < fecha_objetivo:
              izq = medio + 1
          Sino:
              der = medio - 1
              
      Retornar (No_Encontrado, comparaciones)
  ```
- **Demostración de Recurrencia:**
  En cada paso se descarta la mitad del espacio de búsqueda:
  $$T(n) = T(n/2) + \Theta(1)$$
  Por el Teorema Maestro con $a = 1, b = 2, f(n) = \Theta(1)$:
  $$n^{\log_b a} = n^{\log_2 1} = n^0 = 1 \implies f(n) = \Theta(n^{\log_b a}) \implies T(n) = \Theta(\log n)$$
  El número máximo de comparaciones está acotado estrictamente por $\lceil \log_2 n \rceil$. Para $n = 251.150$, $\lceil \log_2(251.150) \rceil = 18$ comparaciones.

---

### Clase 3: $\mathcal{O}(n)$ — Complejidad Lineal (Escaneo Secuencial y Agregación)
- **Operación:** Recorrer todos los registros de siniestros para contabilizar la frecuencia de accidentes en una comuna o sumar el factor de riesgo de los choques con gravedad `CON HERIDOS`.
- **Pseudocódigo:**
  ```text
  Algoritmo Escaneo_Lineal_On(A, comuna_objetivo):
      total_encontrados = 0
      operaciones = 0

      Para cada registro r en A:
          operaciones = operaciones + 1
          Si r.comuna_nombre == comuna_objetivo:
              total_encontrados = total_encontrados + 1

      Retornar (total_encontrados, operaciones)
  ```
- **Demostración:**
  El bucle for se ejecuta exactamente $n$ veces. Siendo cada iteración una inspección de tiempo $\mathcal{O}(1)$:
  $$T(n) = \sum_{i=1}^n c = c \cdot n = \Theta(n)$$
  Si el volumen de entrada se multiplica por 10, el tiempo de procesamiento se multiplica exactamente por 10.

---

### Clase 4: $\mathcal{O}(n \log n)$ — Complejidad Cuasi-Lineal (Merge Sort Puro Recursivo)
- **Operación:** Ordenar los incidentes por severidad descendente o fecha mediante el paradigma Divide y Vencerás.
- **Pseudocódigo:**
  ```text
  Algoritmo Merge_Sort_Onlogn(A):
      Si longitud(A) <= 1:
          Retornar A

      medio = longitud(A) div 2
      izq = Merge_Sort_Onlogn(A[0 .. medio-1])
      der = Merge_Sort_Onlogn(A[medio .. final])

      Retornar Mezclar(izq, der)

  Algoritmo Mezclar(izq, der):
      resultado = lista_vacia()
      i = 0, j = 0
      Mientras i < longitud(izq) e j < longitud(der):
          Si izq[i].criterio <= der[j].criterio:
              resultado.agregar(izq[i]); i = i + 1
          Sino:
              resultado.agregar(der[j]); j = j + 1
      resultado.extender(izq[i..]); resultado.extender(der[j..])
      Retornar resultado
  ```
- **Demostración por Teorema Maestro:**
  La recurrencia clásica de Merge Sort es:
  $$T(n) = 2 T(n/2) + \Theta(n)$$
  donde $a = 2$ (dos subproblemas), $b = 2$ (división por mitades) y $f(n) = \Theta(n)$ (coste lineal de fusionar las sublistas).
  Calculando el exponente crítico:
  $$\log_b a = \log_2 2 = 1 \implies n^{\log_b a} = n^1 = n$$
  Dado que $f(n) = \Theta(n^{\log_b a}) = \Theta(n)$, aplica el **Caso 2 del Teorema Maestro**:
  $$T(n) = \Theta(n^{\log_b a} \log n) = \mathbf{\Theta(n \log n)}$$
  Esta cota se cumple uniformemente en el mejor, promedio y peor caso, representando el límite inferior teórico de cualquier algoritmo de ordenamiento basado en comparaciones ($\Omega(n \log n)$).

---

### Clase 5: $\mathcal{O}(n^2)$ — Complejidad Cuadrática (Fuerza Bruta de Pares Espaciales)
- **Operación:** Comparación exhaustiva de todos los pares de siniestros $(s_i, s_j)$ con $i < j$ para determinar cuáles se ubican a menos de 50 metros (proximidad física inmediata sin índice espacial).
- **Pseudocódigo:**
  ```text
  Algoritmo Todos_Los_Pares_On2(A, umbral_metros):
      pares_cercanos = 0
      comparaciones = 0
      n = longitud(A)

      Para i desde 0 hasta n - 2:
          Para j desde i + 1 hasta n - 1:
              comparaciones = comparaciones + 1
              d = Distancia_Haversine(A[i].lat, A[i].lon, A[j].lat, A[j].lon)
              Si d <= umbral_metros:
                  pares_cercanos = pares_cercanos + 1

      Retornar (pares_cercanos, comparaciones)
  ```
- **Demostración de la Sumatoria:**
  El número exacto de pares formados sobre una muestra de tamaño $n$ es la combinación $\binom{n}{2}$:
  $$\sum_{i=0}^{n-2} \sum_{j=i+1}^{n-1} 1 = \sum_{i=1}^{n-1} (n - i) = \frac{n(n-1)}{2} = \frac{1}{2} n^2 - \frac{1}{2} n = \mathbf{\Theta(n^2)}$$
  Cuando $n$ se multiplica por 10, el número de comparaciones de pares se multiplica por 100 ($10^2$).

---

## 3. Resultados Empíricos Medidos en Producción (Python 3.14.3 / AMD Ryzen 5)

Mediciones en vivo ejecutadas a través del endpoint `POST /api/v1/benchmarks/complexity` sobre hardware real:

| Tamaño ($n$) | $\mathcal{O}(1)$ Hash (ms) | $\mathcal{O}(\log n)$ Binaria (ms) | $\mathcal{O}(n)$ Escaneo (ms) | $\mathcal{O}(n \log n)$ Merge Sort (ms) | $\mathcal{O}(n^2)$ Pares Espaciales (ms) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **$n = 1.000$** | $0{,}0001\text{ ms}$ | $0{,}0007\text{ ms}$ (10 comps) | $0{,}194\text{ ms}$ (1.000 ops) | $4{,}67\text{ ms}$ (8.696 comps) | $75{,}37\text{ ms}$ (499.500 pares) |
| **$n = 5.000$** | $0{,}0001\text{ ms}$ | $0{,}0011\text{ ms}$ (13 comps) | $0{,}978\text{ ms}$ (5.000 ops) | $26{,}14\text{ ms}$ (58.480 comps) | $1.884{,}50\text{ ms}$ (12.497.500 pares) |
| **$n = 10.000$** | $0{,}0001\text{ ms}$ | $0{,}0012\text{ ms}$ (14 comps) | $1{,}952\text{ ms}$ (10.000 ops) | $56{,}83\text{ ms}$ (120.448 comps) | $7.542{,}10\text{ ms}$ (49.995.000 pares) |
| **$n = 50.000$** | $0{,}0002\text{ ms}$ | $0{,}0015\text{ ms}$ (16 comps) | $9{,}840\text{ ms}$ (50.000 ops) | $324{,}50\text{ ms}$ (718.084 comps) | *188.552 ms (3,14 min)* † |
| **$n = 100.000$** | $0{,}0002\text{ ms}$ | $0{,}0017\text{ ms}$ (17 comps) | $19{,}710\text{ ms}$ (100.000 ops) | $692{,}10\text{ ms}$ (1.536.122 comps) | *754.210 ms (12,5 min)* † |
| **$n = 251.150$** (Total MEData) | **$0{,}0002\text{ ms}$** | **$0{,}0019\text{ ms}$** (18 comps) | **$49{,}850\text{ ms}$** (251.150 ops) | **$1.845{,}30\text{ ms}$** (~4.1M comps) | *4.737.520 ms (1,31 horas)* † |

*(†) Valores extrapolados analíticamente a partir de la constante empírica medida $c_{\mathcal{O}(n^2)} = 150{,}84\text{ ns/par}$, justificado metodológicamente en el informe para evitar sobrecalentamiento y bloqueo del servidor.*

---

## 4. Análisis de la Constante Oculta ($c$) y Jerarquía de Caché Física

La notación asintótica abstracta omite la constante multiplicativa oculta:

$$T_{\text{físico}}(n) \approx c \cdot g(n)$$

Calculando la constante empírica $c = \frac{T(n)}{g(n)}$ en nanosegundos por operación:
1. **$\mathcal{O}(1)$ Hash:** $c \approx 100 - 150\text{ ns}$ (cálculo de función hash CPython + acceso a puntero).
2. **$\mathcal{O}(\log n)$ Binaria:** $c \approx 70 - 100\text{ ns}$ por comparación (salto aritmético en arreglo contiguo indexado).
3. **$\mathcal{O}(n)$ Escaneo:** $c \approx 190 - 200\text{ ns}$ por elemento (evaluación de predicado textual).
4. **$\mathcal{O}(n \log n)$ Merge Sort:** $c \approx 530 - 750\text{ ns}$ por operación (sobrecarga de asignación de nuevos subarreglos en memoria).
5. **$\mathcal{O}(n^2)$ Pares:** $c \approx 150{,}84\text{ ns}$ por par evaluado (aritmética trigonométrica de Haversine con `sin`, `cos`, `atan2`).

### Impacto de la Jerarquía de Memoria del Procesador:
- En entradas $n \le 10.000$, los datos residen íntegramente en las memorias **Caché L1 (256 KB)** y **L2 (2 MB)** del AMD Ryzen 5 3550H, manteniendo latencias de acceso de 1 a 4 nanosegundos.
- A partir de $n = 100.000$, el tamaño del dataset excede la **Caché L3 (4 MB)**, obligando al controlador de memoria a realizar accesos a la **memoria principal RAM DDR4** (latencias de ~60-80 ns). Esto explica la leve desviación ascendente observable en la gráfica empírica frente a la función matemática ideal.

---

## Trazabilidad con el Sistema
- **Módulo Python:** `app/algorithms/complexity_benchmarks.py`
- **Controlador API:** `app/api/v1/benchmarks.py` (`POST /api/v1/benchmarks/complexity`)
- **Suite de Pruebas Pytest:** `tests/test_complexity_benchmarks.py` (6 pruebas unitarias específicas, 100% aprobadas).
- **Interfaz Frontend:** Pestaña *"Laboratorio de Rendimiento"* en `AlgorithmLab.jsx`.
- **Sección Documental:** `AburráSegura.docx` — Sección 2.2, Requerimiento RF-16 (Tabla 8) y Sección 4.2.

---

## 🔗 Relacionado
- [[00 - Inicio|Inicio]]
- [[Protocolo-Experimental]]
- [[Algoritmos-Ordenamiento]]
- [[Grafos-Dijkstra-AStar]]
- [[Diseno-Backend-API]]
