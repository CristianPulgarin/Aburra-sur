---
titulo: "Plantilla Estándar para Casos de Prueba Automatizados"
tipo: plantilla
tipo: plantilla
plantilla_tipo: qa_caso_prueba
id: QA-TC-XX
proyecto: PPI - Analisis de Algoritmos
institucion: Tecnologico de Antioquia
modulo: "{{Modulo evaluado}}"
estado: aprobado # propuesto | aprobado | fallido | bloqueado
fecha_ejecucion: "{{AAAA-MM-DD}}"
autor: qa-tester
requisito_asociado:
  - "{{RF-XX}}"
tags:
  - qa
  - pruebas
  - pytest
  - casos-borde
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/plantilla, ppi/tdea, proyecto/aburrasegura]
---


# Caso de Prueba: {{QA-TC-XX}} — {{Nombre del Caso de Prueba}}

> [!abstract] En pocas palabras
> Formato base para el diseño y documentación de casos de prueba automatizados y criterios de aceptación.


> [!NOTE] Objetivo de la Prueba
> {{Describir qué invariante algorítmico, caso borde o contrato de API se está certificando}}.

---

## 1. Alcance y Tipo de Prueba
- **Tipo:** Unitaria | Integración | Regresión | Carga / Estrés
- **Componente bajo prueba:** `app/algorithms/...` o `app/api/v1/...`
- **Requisito verificado:** [[Matriz-Requisitos]] ({{requisito_asociado}})

---

## 2. Precondiciones y Datos de Prueba (Fixtures)
- **Precondiciones:** {{Estado previo requerido del sistema, base de datos o estructuras en memoria}}.
- **Entrada / Dataset:**
  ```python
  # Ejemplo de datos o parámetros utilizados
  ...
  ```

---

## 3. Pasos de Ejecución
1. {{Paso 1: Configurar entrada}}
2. {{Paso 2: Invocar función / endpoint}}
3. {{Paso 3: Validar aserciones}}

---

## 4. Resultado Esperado vs. Obtenido
- **Resultado Esperado:** {{Comportamiento matemático o respuesta HTTP esperada}}.
- **Resultado Obtenido:** **PASS** (Tiempo: {{X.XX}} ms, Memoria: {{Y.YY}} KB).
- **Aserción Pytest:**
  ```python
  assert resultado == esperado
  ```

---

## 5. Trazabilidad
- **Archivo de Prueba:** `tests/test_{{modulo}}.py`
- **Reporte Global:** [[Plan-Pruebas-QA]], [[Reporte-Final-QA-Fase5]]

---

## 🔗 Relacionado
- [[00 - Inicio|Inicio]]
- [[MOC-Principal]]
- [[Plantilla-Modulo]]
