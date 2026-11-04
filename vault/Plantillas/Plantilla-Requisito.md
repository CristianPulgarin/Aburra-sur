---
tipo: plantilla
plantilla_tipo: requisito
id: RF-XX # o RN-XX
proyecto: PPI - Analisis de Algoritmos
institucion: Tecnologico de Antioquia
titulo: "{{Nombre del Requisito}}"
prioridad: Alta # Alta | Media | Baja
objetivo_asociado: 1 # 1 | 2 | 3
responsable: "{{Rol o Integrante}}"
estado: verificado # propuesto | en_desarrollo | verificado | en_pausa
tags:
  - requisitos
  - trazabilidad
  - especificacion
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/plantilla, ppi/tdea, proyecto/aburrasegura]
---

# Requisito {{id}}: {{titulo}}

> [!abstract] En pocas palabras
> Plantilla estándar para la especificación funcional de requisitos de software con criterios de verificación.


> [!NOTE] Declaración del Requisito
> El sistema debe {{declaración clara, medible y sin ambigüedades de la funcionalidad o restricción}}.

---

## 1. Justificación y Contexto
{{Por qué es necesario este requisito y a qué objetivo específico del PPI da cumplimiento según la Sección 1.3 de AburráSegura.docx.}}

---

## 2. Criterios de Aceptación Formale
- [ ] **CA-01:** {{Condición verificable 1}}.
- [ ] **CA-02:** {{Condición verificable 2}}.
- [ ] **CA-03:** {{Condición verificable 3}}.

---

## 3. Entradas, Proceso y Salidas
- **Entrada:** {{Parámetros, datos o interacción del usuario}}.
- **Procesamiento Algorítmico:** {{Algoritmo o componente involucrado (ej. Dijkstra, consulta SQL, filtrado)}}.
- **Salida:** {{Respuesta del sistema, vista en mapa o código HTTP}}.

---

## 4. Trazabilidad de Verificación y Pruebas
- **Archivo de Código:** `app/...`
- **Suite de Pruebas Pytest:** `tests/test_....py::test_...`
- **Sección en Documento Institucional:** `AburráSegura.docx` — Sección 3.1 (Tabla {{N}}).

---

## Enlaces Relacionados
- Matriz General: [[Matriz-Requisitos]]
- ADR de Soporte: [[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad]]

---

## 🔗 Relacionado
- [[00 - Inicio|Inicio]]
- [[MOC-Principal]]
- [[Plantilla-QA]]
