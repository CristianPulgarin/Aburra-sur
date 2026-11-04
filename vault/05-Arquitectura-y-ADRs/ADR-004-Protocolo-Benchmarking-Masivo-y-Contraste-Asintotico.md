---
titulo: "ADR-004: Diseño e Implementación del Marco de Benchmarking Asintótico"
tipo: decision
tipo: adr
proyecto: PPI - Analisis de Algoritmos
institucion: Tecnologico de Antioquia
estado: Aceptado
fecha: 2026-09-30
decisores: Orquestador, Especialista en Algoritmos, Backend Dev, QA Tester
vigencia: historico
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/decision, ppi/tdea, proyecto/aburrasegura]
---


> [!WARNING] Nota histórica (alcance anterior)
> Esta nota pertenece al prototipo de alcance amplio (24–30/09/2026), reemplazado el 05–06/10/2026 por [[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad]]. Se conserva como memoria. **No reutilizar sus cifras sin recalcularlas** (ver [[Archivo-Alcance-Anterior]]).

# ADR-004: Diseño e Implementación del Marco de Benchmarking Masivo y Contraste Asintótico (Fase 4)

> [!abstract] En pocas palabras
> Diseño del marco de experimentación asintótica para garantizar repetibilidad estadística y contraste riguroso con modelos teóricos.


## Contexto y Planteamiento del Problema
Para dar cumplimiento al **Tercer Objetivo Específico** del PPI y a los requerimientos de la Fase 4, es indispensable evaluar empíricamente el rendimiento temporal y espacial de las implementaciones algorítmicas frente a sus cotas teóricas asintóticas ($\mathcal{O}$, $\Theta$, $\Omega$) sobre volúmenes masivos de datos que alcanzan hasta $1.000.000$ de registros.

La medición empírica en hardware moderno presenta retos metodológicos:
1. Ruido ambiental introducido por el sistema operativo, planificación de subprocesos y fluctuaciones térmicas de la CPU.
2. Comportamiento patológico de recursiones profundas en Python (límite por defecto de recursión de 1.000 llamadas).
3. Efectos no lineales inducidos por la jerarquía de memoria caché (L1/L2/L3) y el recolector de basura de CPython al superar el umbral de los 100K elementos.

## Decisión Técnica Adoptada

1. **Estandarización de Particiones y Aislamiento de I/O:**
   - Se crearon particiones inmutables en disco (`data/benchmarks/bench_{1k,10k,50k,100k,500k,1m}.csv`).
   - Durante la medición del tiempo de ejecución de cada algoritmo, los datos se encuentran precargados en memoria RAM, midiendo única y exclusivamente la fase de cómputo algorítmico sin penalizaciones por lecturas en disco o deserializaciones.

2. **Instrumentación de Alta Precisión y Control Estadístico:**
   - **Tiempo de CPU:** Medido con `time.perf_counter_ns()` para resolución a nivel de nanosegundos.
   - **Repeticiones y Control de Varianza:** Múltiples repeticiones por cada tamaño de entrada con cómputo formal de media aritmética ($\mu$) y desviación estándar ($\sigma$).
   - **Memoria Peak:** Monitoreo estricto del pico de asignación de memoria mediante la API `tracemalloc`.
   - **Contador de Operaciones Primitivas:** Contabilización exacta de comparaciones de claves en cada partición mediante instrumentación no invasiva.

3. **Arquitectura Iterativa con Pila Acotada en Quick Sort:**
   - Se descartó la recursión ingenua y se adoptó una implementación iterativa con pila explícita, partición de Hoare y pivote mediante mediana de tres.
   - Apilando siempre la partición de mayor longitud en primer orden, la profundidad de la pila se restringe estrictamente a $\mathcal{O}(\log n) \le 30$ entradas, garantizando inmunidad ante desbordamientos de memoria (`RecursionError`) para cualquier $n \le 1.000.000$.

4. **Persistencia Estructurada y Exposición API:**
   - Los resultados consolidados se persisten en formato JSON estándar (`data/benchmarks/benchmark_results_fase4.json`) incluyendo metadatos completos de hardware.
   - Se expone el endpoint `GET /api/v1/benchmarks/fase4-results` en FastAPI para alimentar de forma instantánea el Laboratorio de Algoritmos en el frontend.

## Consecuencias y Beneficios

- **Rigor Científico:** Permite calcular de forma cuantitativa la constante oculta $c = \frac{T(n)}{g(n)}$ y justificar las discrepancias físicas entre la teoría abstracta y el hardware físico.
- **Rendimiento:** El frontend interactivo visualiza matrices completas de 1K a 1M sin bloquear el navegador ni esperar largos cómputos en vivo.

---

## 🔗 Relacionado
- [[00 - Inicio|Inicio]]
- [[Protocolo-Experimental]]
- [[Laboratorio-Jerarquia-Asintotica]]
- [[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad|ADR-005]]
