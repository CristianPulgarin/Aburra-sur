---
titulo: "Plantilla Estándar para Especificación de Algoritmos"
tipo: plantilla
tipo: plantilla
plantilla_tipo: algoritmo
proyecto: PPI - Analisis de Algoritmos
institucion: Tecnologico de Antioquia
estado: borrador
autor: "{{responsable}}"
fecha: "{{fecha}}"
requisito_asociado:
  - "{{requisito_id}}"
tags:
  - plantilla
  - algoritmos
  - complejidad
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/plantilla, ppi/tdea, proyecto/aburrasegura]
---


# Algoritmo: {{Nombre del Algoritmo}}

> [!abstract] En pocas palabras
> Estructura base para documentar formalmente la correctitud, pseudocódigo y complejidad asintótica de nuevos algoritmos.


> [!NOTE] Propósito General
> {{Breve descripción del problema computacional que resuelve este algoritmo, su contexto en el PPI de siniestralidad vial en Medellín y el requisito asociado [[Matriz-Requisitos]].}}

---

## 1. Definición Formal del Problema
- **Entrada:** {{Definición formal de los datos de entrada, tipos y restricciones}}.
- **Salida:** {{Estructura y propiedades garantizadas del resultado retornado}}.
- **Invariante de Bucle / Principio de Inducción:** {{Condición que se mantiene verdadera antes, durante y después de cada iteración o llamada recursiva}}.

---

## 2. Pseudocódigo Canónico e Implementación

```text
Algoritmo {{NombreAlgoritmo}}(Entrada):
    // Inicialización de estructuras
    ...
    // Bucle principal / Llamadas recursivas
    ...
    Retornar Resultado
```

---

## 3. Demostración Matemática de Complejidad Asintótica

### A. Complejidad Temporal
- **Mejor Caso ($\Omega$):**
  $$\Omega(...) \quad \text{Demostración: ...}$$
- **Caso Promedio ($\Theta$):**
  $$\Theta(...) \quad \text{Demostración / Recurrencia: ...}$$
- **Peor Caso ($\mathcal{O}$):**
  $$\mathcal{O}(...) \quad \text{Demostración / Cota superior: ...}$$

### B. Complejidad Espacial
- **Memoria Auxiliar:** $\mathcal{O}(...)$
- **Espacio en Pila de Recursión / Heap:** $\mathcal{O}(...)$

---

## 4. Validación Empírica y Benchmarking

| Tamaño de Entrada ($n$) | Tiempo Medido (ms) | Operaciones Primitivas | Memoria Peak (KB) | Cota Teórica Esperada |
| :---: | :---: | :---: | :---: | :---: |
| $1.000$ | — | — | — | — |
| $10.000$ | — | — | — | — |
| $50.000$ | — | — | — | — |
| $100.000$ | — | — | — | — |

- **Constante oculta calculada:** $c = \frac{T(n)}{g(n)} \approx \dots \text{ ns/operación}$.
- **Comportamiento en Hardware:** {{Análisis de impacto de jerarquía de memoria caché y procesador}}.

---

## 5. Casos Borde y Pruebas Unitarias Asociadas
- Arreglo / Estructura vacía ($n=0$): {{Comportamiento esperado}}
- Elemento unitario ($n=1$): {{Comportamiento esperado}}
- Elementos idénticos repetidos: {{Comportamiento esperado}}
- Suite Pytest asociada: `tests/test_{{modulo}}.py`

---

## Enlaces y Notas Relacionadas
- Requisito: [[Matriz-Requisitos]]
- Decisión de Arquitectura: [[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad]]
- Protocolo Experimental: [[Protocolo-Experimental]]

---

## 🔗 Relacionado
- [[00 - Inicio|Inicio]]
- [[MOC-Principal]]
- [[Plantilla-ADR]]
