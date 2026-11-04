# Especificación Técnica de Agentes Personalizados

Esta referencia complementa la skill `agentes-personalizados` con detalles avanzados sobre los campos, las políticas de seguridad y la orquestación.

## Estructura de Directorios

```text
<proyecto-root>/
└── .agents/
    ├── agents/
    │   ├── dependency-modernizer.md
    │   └── code-reviewer.md
    └── skills/
        └── agentes-personalizados/
            ├── SKILL.md
            ├── examples/
            └── references/
```

## Campos de Configuración en Detalle

### 1. `name`
- Identificador canónico. Debe ser único, en minúsculas y separado por guiones (kebab-case).
- Se utiliza al invocar por CLI: `agy --agent <name>`.

### 2. `description`
- Define la responsabilidad y caso de uso del agente.
- Cuando un agente actúa como coordinador, evalúa este campo para decidir a qué subagente delegar la tarea.

### 3. `model`
- Permite seleccionar un modelo acorde al tipo de carga de trabajo:
  - `flash`: Rápido y económico, ideal para tareas repetitivas, modernización de paquetes, linters o scripts sencillos.
  - `pro`: Máxima capacidad de razonamiento para refactorizaciones de gran envergadura o arquitecturas complejas.
  - `flash_lite`: Modelo ultra liviano.
  - `inherit`: Adopta el modelo configurado por el usuario o agente padre.

### 4. `tools`
- Restringe el conjunto de herramientas disponibles para evitar alucinaciones y dispersión:
  - `view_file`: Inspección de archivos.
  - `replace_file_content`: Modificaciones puntuales de código.
  - `write_to_file`: Creación de archivos nuevos.
  - `run_command`: Ejecución en terminal.
  - `manage_task`: Control de procesos en segundo plano.

### 5. `skills`
- Curación de conocimientos específicos. En vez de exponer todas las skills del repositorio, solo se asocian las que el agente especializado necesita.

### 6. `permissionMode` & `commandExecutionPolicy`
- **`permissionMode`**: Controla el nivel general de permisos (ej. `acceptEdits`, `bypassPermissions`).
- **`commandExecutionPolicy`**:
  - `auto`: Permite al agente ejecutar comandos estándar de compilación, ejecución de pruebas o linters de forma autónoma en segundo plano, sin requerir confirmación interactiva continua. Comandos destructivos (eliminación masiva, formateo, etc.) permanecen bloqueados y sujetos a aprobación manual.

### 7. Simetría (`mainAgent` y `subagent`)
- `mainAgent: true`: Habilita al agente para ser elegido como punto de entrada de la sesión por el desarrollador.
- `subagent: true`: Habilita al agente para ser instanciado como trabajador subordinado por otros agentes.
