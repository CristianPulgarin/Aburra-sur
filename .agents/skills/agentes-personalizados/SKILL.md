---
name: agentes-personalizados
description: >-
  Guía completa para la creación, configuración y uso de agentes personalizados (Custom Agents)
  en Google Antigravity (Antigravity 2.0, Antigravity CLI y Antigravity IDE).
  Activa esta habilidad cuando el usuario desee crear, modificar o comprender agentes personalizados,
  sus archivos de definición Markdown + YAML, campos admitidos (mainAgent, subagent, model, tools,
  skills, permissionMode, commandExecutionPolicy), ubicaciones de almacenamiento y formas de invocación.
---

# Agentes Personalizados (Custom Agents) en Antigravity

Los **Agentes Personalizados** permiten definir roles especializados mediante archivos declarativos simples, optimizando el uso de la ventana de contexto, delimitando herramientas y reglas, y mejorando la predictibilidad y velocidad del trabajo de desarrollo.

---

## 1. Concepto y Diferenciación

- **Especialización vs. Asistentes Generales**: Un agente general desconoce las convenciones de prueba o empaquetado específicas de un repositorio a menos que se expliquen en cada prompt.
- **Evitar la saturación del contexto (Context Bloat)**: En lugar de cargar todas las instrucciones, herramientas y habilidades de un proyecto en cada sesión, un agente personalizado restringe su alcance a lo necesario para su función.
- **Relación con Skills y Subagentes dinámicos**:
  - Las *Skills* aportan conocimiento procedimental bajo demanda (progressive disclosure).
  - Los *Subagentes dinámicos* permiten delegar tareas creando prompts sobre la marcha.
  - Los *Agentes Personalizados* combinan y elevan ambos conceptos: permiten fijar el system prompt, curar el subconjunto exacto de herramientas (`tools`) y habilidades (`skills`), seleccionar el modelo (`model`) y configurar políticas de permisos y ejecución.

---

## 2. Ubicaciones de Almacenamiento

Los agentes personalizados se definen como archivos Markdown individuales (`.md`):

| Ámbito | Ruta | Propósito |
| :--- | :--- | :--- |
| **Proyecto / Workspace** | `.agents/agents/<nombre>.md` | Específico del repositorio. Al commitearlo en el control de versiones (Git), queda disponible de forma instantánea para todos los miembros del equipo. |
| **Global / Máquina local** | `~/.gemini/config/agents/<nombre>.md` | Disponible para el usuario en cualquier proyecto o sesión en su máquina local. |

*(Nota: En proyectos locales también se reconocen variantes como `.agent/agents/`).*

---

## 3. Formato del Archivo del Agente

Un agente personalizado consta de un único archivo Markdown compuesto por:
1. **Encabezado YAML Frontmatter**: Metadatos de configuración técnica (modelo, herramientas, habilidades, banderas de simetría y permisos).
2. **Cuerpo Markdown**: Se compila directamente como el **System Prompt** o instrucciones base (`# Core Instructions`) del agente.

### Plantilla Base (Blueprint 101)

```markdown
---
name: dependency-modernizer
description: Ayuda a actualizar paquetes y dependencias locales y verificar que las pruebas pasen.
model: flash
tools:
  - view_file
  - replace_file_content
  - manage_task
  - run_command
skills:
  - skills/package-upgrade-rules
mainAgent: true
subagent: true
permissionMode: acceptEdits
commandExecutionPolicy: auto
---
# Core Instructions
Eres un modernizador de dependencias. Tu labor consiste en revisar archivos de configuración,
actualizar las dependencias indicadas, ejecutar las suites de pruebas y validar que el build sea exitoso.
```

---

## 4. Campos del Frontmatter (YAML)

| Campo | Tipo | Requerido | Descripción |
| :--- | :--- | :--- | :--- |
| `name` | string | Sí | Identificador único del agente (en minúsculas y con guiones). Ej: `dependency-modernizer`. |
| `description` | string | Sí | Explicación concisa del rol. Crucial para que agentes coordinadores sepan cuándo delegar tareas en él. |
| `model` | string | No | Modelo a emplear para el agente (ej. `flash`, `pro`, `flash_lite`, `inherit`). |
| `tools` | lista | No | Lista blanca de herramientas accesibles para el agente (ej. `view_file`, `replace_file_content`, `run_command`). Evita ruido de herramientas irrelevantes. |
| `skills` | lista | No | Rutas o identificadores de skills específicas disponibles para este agente (ej. `- skills/package-upgrade-rules`). |
| `mainAgent` | boolean | No | Si es `true`, puede utilizarse como agente principal en la sesión. |
| `subagent` | boolean | No | Si es `true`, puede invocarse dinámicamente como subagente por un coordinador. |
| `permissionMode`| string | No | Nivel de permisos de edición y ejecución (ej. `acceptEdits`, `bypassPermissions`). |
| `commandExecutionPolicy` | string | No | Política de seguridad para ejecución en terminal (ej. `auto` para comandos de tests/compilación en segundo plano sin confirmaciones continuas). |

---

## 5. Simetría de Ejecución: Main Agent vs. Subagent

A diferencia de otras herramientas que limitan los agentes personalizados exclusivamente a subagentes de fondo:

1. **Como Agente Principal (`mainAgent: true`)**:
   - Se puede seleccionar y chatear directamente con él desde el inicio.
   - Las instrucciones centrales conforman su personalidad y directrices base directas.
2. **Como Subagente (`subagent: true`)**:
   - Puede ser llamado dinámicamente por un agente coordinador para resolver subtareas autónomas.
3. **Simetría Total**:
   - Marcando ambos en `true`, el mismo agente puede atenderte cara a cara o ser subcontratado en segundo plano según la necesidad.

---

## 6. Modos de Invocación

### A. Invocación como Agente Principal (Main Agent)
- **Interfaz Gráfica (Antigravity 2.0 App / IDE)**:
  - Seleccionar el agente directamente en el menú desplegable (dropdown) de selección de agente de la interfaz.
- **Línea de Comandos (Antigravity CLI)**:
  ```bash
  agy --agent <nombre-del-agente>
  ```
  *Ejemplo:* `agy --agent dependency-modernizer`

### B. Invocación como Subagente (Subagent)
- El agente coordinador lee la `description` y el contexto de la tarea del usuario.
- El coordinador delega la subtarea automáticamente mediante las capacidades de orquestación de subagentes.

---

## 7. Procedimiento para Crear un Agente en este Proyecto

Para agregar un nuevo agente personalizado a este proyecto:

1. Crear el directorio `.agents/agents/` en la raíz del proyecto si no existe.
2. Crear un archivo `<nombre-del-agente>.md` con el frontmatter YAML y las instrucciones.
3. Configurar las herramientas y skills mínimas requeridas.
4. Establecer `mainAgent: true` y/o `subagent: true`.
5. Guardar y verificar con `agy --agent <nombre-del-agente>` o en el selector de la interfaz gráfica.

---

## 8. Documentación y Ejemplos de Referencia

- [Especificación Técnica y Políticas de Ejecución](references/agent-specification.md)
- [Ejemplo: Modernizador de Dependencias (`dependency-modernizer.md`)](examples/dependency-modernizer.md)
- [Ejemplo: Revisor de Código (`code-reviewer.md`)](examples/code-reviewer.md)


