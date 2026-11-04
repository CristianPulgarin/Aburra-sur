---
titulo: "Protocolo Experimental de Benchmarking y Mitigación de Ruido"
tipo: investigacion
tipo: protocolo_experimental
proyecto: PPI - Analisis de Algoritmos
institucion: Tecnologico de Antioquia
semestre: 8vo Semestre - 2026
fase: Benchmarking Masivo y Contraste Asintotico
estado: completado
version: 2.1
fecha: 2026-10-08
autores:
  - Jarrison Quintero Castillo
  - Sebastián Gómez Cardona
  - Cristian David Pulgarín Vélez
requisito_asociado:
  - R6
  - R7
  - RF-14
  - RF-15
  - RF-16
tags:
  - algoritmos
  - benchmarking
  - complejidad
  - big-o
  - protocolo-experimental
  - hardware
vigencia: vigente
base: "[[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad]]"
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/investigacion, ppi/tdea, proyecto/aburrasegura]
---


# Protocolo Experimental de Benchmarking y Contraste Asintótico (1K a 1M)

> [!abstract] En pocas palabras
> Metodología experimental estandarizada: control de hardware, calentamiento de caché, réplicas estadísticas, métricas de tiempo/memoria y mitigación de ruido.


> [!NOTE] Propósito Científico en el PPI
> Validar empíricamente las cotas de complejidad asintótica ($\mathcal{O}$, $\Omega$, $\Theta$) deducidas teóricamente para los algoritmos desarrollados en el proyecto. Se contrasta el comportamiento matemático ideal con las mediciones empíricas obtenidas en una plataforma computacional estandarizada, identificando constantes ocultas ($c$), impactos de la jerarquía de memoria física (L1/L2/L3 caché) y efectos del runtime de Python sobre los **251.150 incidentes reales** de Medellín y particiones sintetizadas hasta **1.000.000 de registros**.

---

## 1. Entorno y Especificaciones de Hardware de Laboratorio

Para garantizar la reproducibilidad científica estricta de las pruebas, los experimentos fueron ejecutados bajo las siguientes condiciones de hardware y software:

| Parámetro | Especificación de Laboratorio Certificada |
| :--- | :--- |
| **Procesador (CPU)** | AMD Ryzen 5 3550H con Radeon Vega Mobile Gfx |
| **Arquitectura** | x86_64 (64-bit) |
| **Frecuencia Base / Turbo** | 2.10 GHz base / 3.70 GHz turbo boost |
| **Núcleos / Subprocesos** | 4 núcleos físicos / 8 subprocesos lógicos |
| **Jerarquía de Caché** | L1: 64 KB/núcleo (32K inst + 32K data), L2: 512 KB/núcleo, L3: 4 MB compartido |
| **Memoria RAM Total** | 16.0 GB DDR4 (16.581.988 KB) en dual-channel |
| **Sistema Operativo** | Microsoft Windows 11 Home Single Language (Build 64-bit) |
| **Entorno de Ejecución** | CPython 3.14.3 (MSC v.1942 64-bit) |
| **Herramientas de Medición** | `time.perf_counter_ns()` (resolución a nivel de nanosegundos), `tracemalloc` (peak memory) |
| **Control de Semilla** | `random.seed(42)` para generadores pseudoaleatorios |

---

## 2. Diseño Factorial del Experimento

### 2.1 Variables Independientes (Factores Controlados)
1. **Tamaño de Entrada ($n$):**
   $$n \in \{1.000, 10.000, 50.000, 100.000, 500.000, 1.000.000\}$$
2. **Familia Algorítmica Evaluada:**
   - *Jerarquía Asintótica en Vivo:* $\mathcal{O}(1)$ Hash, $\mathcal{O}(\log n)$ Binaria, $\mathcal{O}(n)$ Escaneo, $\mathcal{O}(n \log n)$ Merge Sort, $\mathcal{O}(n^2)$ Pares espaciales.
   - *Ordenamiento Masivo:* Quick Sort (Hoare + mediana de tres iterativo), Merge Sort puro, Heap Sort in-place, Counting Sort lineal, Timsort nativo.
   - *Indexación Espacial:* KD-Tree 2D ($k$-NN y radio) vs. Búsqueda Lineal Exhaustiva $\mathcal{O}(n)$.
   - *Grafos:* Dijkstra con cola de prioridad min-heap vs. A* con función de coste multiobjetivo ($\alpha$ distancia, $\beta$ riesgo).
3. **Distribución de las Claves de Entrada:**
   - **Aleatoria Uniforme (`random`):** Claves distribuidas en el rango continuo de siniestros.
   - **Ya Ordenada (`sorted`):** Evalúa el mejor caso en Timsort y la estabilidad del pivote en Quick Sort.
   - **Invertida (`reversed`):** Evalúa el peor caso clásico en particionamientos no balanceados.
   - **Duplicados Masivos (`duplicates`):** Claves con baja cardinalidad y alta repetición.

### 2.2 Variables Dependientes (Métricas Observadas)
1. **Tiempo de CPU ($T_{\text{CPU}}$):** Medido en milisegundos ($ms$) con media ($\mu$) y desviación estándar ($\sigma$) sobre repeticiones independientes.
2. **Operaciones Primitivas / Comparaciones ($C$):** Conteo exacto mediante instrumentación no invasiva.
3. **Memoria RAM Peak ($M_{\text{peak}}$):** Medida en Kilobytes ($KB$) mediante el subsistema `tracemalloc`.
4. **Factor de Aceleración (*Speedup* $S$):** $S = \frac{T_{\text{referencia}}}{T_{\text{optimizado}}}$.
5. **Constante Oculta Normalizada ($c$):**
   $$c = \frac{T(n)}{g(n)} \quad \text{donde } g(n) = n \log_2 n, \; g(n) = n, \; \text{o } g(n) = n^2$$

---

## 3. Análisis de Discrepancias Físicas: Teoría vs. Hardware Real

El análisis asintótico tradicional asume la máquina RAM (*Random Access Machine*) con accesos de memoria en tiempo unitario $\mathcal{O}(1)$. Sin embargo, en arquitecturas modernas de computadores se evidencian desviaciones atribuibles a:

### 3.1 Jerarquía de Memoria y Pérdidas de Caché (*Cache Misses*)
- Para $n \le 10.000$, la estructura de datos completa reside en las memorias intermedias L1 y L2 ($< 2 \text{ MB}$), con latencias de acceso de 1 a 4 ciclos de reloj.
- Para $n \ge 100.000$, el tamaño del arreglo supera la memoria L3 compartida (4 MB). Los accesos a punteros dispersos en Quick Sort o la creación de subarreglos en Merge Sort generan fallos sistemáticos de línea de caché (*L3 cache misses*), obligando a acceder a la memoria DRAM principal con penalizaciones de 60 a 80 ns por acceso. Esto explica por qué el tiempo crece ligeramente más rápido que la curva asintótica pura para $n \ge 500.000$.

### 3.2 Modelo de Memoria en Python y Recolección de Basura (*GC*)
- En Python, cada elemento numérico es un objeto envuelto (`PyObject`) de 28 bytes más el puntero de 8 bytes en la lista contenedora. Un arreglo de $1.000.000$ de elementos requiere $> 36 \text{ MB}$ de memoria continua solo para referencias.
- Las divisiones de arreglos por rebanado (`sub_arr[:mid]`) en la implementación clásica de Merge Sort generan copias en memoria que activan periódicamente el colector de basura por generaciones de CPython, introduciendo fluctuaciones de tiempo (desviación estándar $\sigma > 0$).

### 3.3 Poda Espacial en KD-Tree frente al Escaneo Lineal
En la indexación 2D, el KD-Tree poda cuadrantes completos cuando la distancia al hiperplano de corte supera la distancia mínima registrada:
$$\text{Speedup}(n) = \frac{\mathcal{O}(n)}{\mathcal{O}(\log n)} \propto \frac{n}{\log n}$$
Para $n = 200.000$, el speedup empírico medido alcanza **$4.018,3\times$**, confirmando la superioridad contundente de las estructuras de datos espaciales sobre la computación lineal en sistemas SIG urbanos.

---

## Trazabilidad con el Vault
- Módulo del Laboratorio: [[Laboratorio-Jerarquia-Asintotica]]
- Algoritmos de Ordenamiento: [[Algoritmos-Ordenamiento]]
- Estructura Espacial: [[Estructuras-Espaciales-KDTree]]
- Enrutamiento y Grafos: [[Grafos-Dijkstra-AStar]]
- Certificación QA: [[Reporte-Final-QA-Fase5]]

---

## 🔗 Relacionado
- [[00 - Inicio|Inicio]]
- [[Laboratorio-Jerarquia-Asintotica]]
- [[Algoritmos-Ordenamiento]]
- [[ADR-004-Protocolo-Benchmarking-Masivo-y-Contraste-Asintotico|ADR-004]]
