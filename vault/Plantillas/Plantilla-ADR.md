---
tipo: plantilla
plantilla_tipo: adr
id: ADR-XXX
proyecto: PPI - Analisis de Algoritmos
institucion: Tecnologico de Antioquia
titulo: "{{Título corto y descriptivo de la decisión}}"
estado: propuesto # propuesto | aceptado | rechazado | reemplazado
fecha: "{{AAAA-MM-DD}}"
decisores:
  - "{{Nombre o Rol 1}}"
  - "{{Nombre o Rol 2}}"
requisito_asociado:
  - "{{RF-XX o R-XX}}"
tags:
  - adr
  - arquitectura
  - decisiones
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/plantilla, ppi/tdea, proyecto/aburrasegura]
---

# ADR-XXX: {{Título de la Decisión Arquitectónica}}

> [!abstract] En pocas palabras
> Plantilla estandarizada para el registro de decisiones arquitectónicas de software siguiendo el formato MADR / Nygard.


> [!NOTE] Resumen Ejecutivo
> {{Una o dos frases que sintetizan qué se decidió y por qué}}.

---

## 1. Contexto y Planteamiento del Problema
{{Describe el contexto técnico, la necesidad del proyecto, las restricciones del entorno institucional o las limitaciones de hardware/datos que motivan esta decisión.}}

---

## 2. Conductores de la Decisión (Drivers)
- **Rigor Académico:** {{Ej. necesidad de estudiar complejidad asintótica en tiempo real}}.
- **Rendimiento:** {{Ej. tiempo de respuesta sub-segundo en cálculo de rutas}}.
- **Mantenibilidad:** {{Ej. separación estricta en 3 capas desacopladas}}.
- **Viabilidad Financiera:** {{Ej. uso de tecnologías 100% de código abierto sin costos de servidor}}.

---

## 3. Opciones Consideradas

### Opción 1: {{Nombre de la Opción 1}}
- **Descripción:** {{En qué consiste}}.
- **Ventajas:** {{Puntos a favor}}.
- **Desventajas:** {{Puntos en contra}}.

### Opción 2: {{Nombre de la Opción 2}}
- **Descripción:** {{En qué consiste}}.
- **Ventajas:** {{Puntos a favor}}.
- **Desventajas:** {{Puntos en contra}}.

---

## 4. Decisión Tomada
Se elige formalmente la **{{Opción Seleccionada}}** debido a:
1. {{Argumento 1}}
2. {{Argumento 2}}
3. {{Argumento 3}}

---

## 5. Consecuencias

### Consecuencias Positivas (Beneficios)
- {{Beneficio 1}}
- {{Beneficio 2}}

### Consecuencias Negativas o Desafíos (Trade-offs)
- {{Trade-off 1 y cómo se mitiga}}
- {{Trade-off 2}}

---

## 6. Trazabilidad con el Documento Institucional
- **Sección en `AburráSegura.docx`:** {{Ej. Sección 4.2 Diseño del software}}.
- **Requisitos Vinculados:** [[Matriz-Requisitos]].
- **ADRs Relacionados:** [[ADR-001-Enfoque-Siniestros-y-Grafo-OSM]], [[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad]].

---

## 🔗 Relacionado
- [[00 - Inicio|Inicio]]
- [[MOC-Principal]]
- [[Plantilla-Algoritmo]]
