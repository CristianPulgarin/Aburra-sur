---
titulo: "Manual de Usuario y Guía de Operación del Prototipo"
tipo: guia
tipo: manual_usuario
proyecto: PPI - Analisis de Algoritmos
institucion: Tecnologico de Antioquia
semestre: 8vo Semestre - 2026
fase: Entrega Final y Anexos
version: 2.1
fecha: 2026-10-08
estado: completado
autores:
  - Jarrison Quintero Castillo
  - Sebastián Gómez Cardona
  - Cristian David Pulgarín Vélez
tags:
  - manual-usuario
  - prototipo
  - instalacion
  - guia-paso-a-paso
  - anexos
vigencia: vigente
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/guia, ppi/tdea, proyecto/aburrasegura]
---


# Manual de Usuario y Guía de Operación del Prototipo Computacional — AburráSegura

> [!abstract] En pocas palabras
> Guía práctica para usuarios finales y evaluadores: instalación local, arranque del servidor, selección de rutas seguras y uso del laboratorio.


Este manual describe el procedimiento formal de puesta en marcha, configuración y operación del prototipo computacional **AburráSegura**, sirviendo directamente como anexo técnico institucional para la **Sección 7 (ANEXOS)** de `AburráSegura.docx`.

---

## 1. Requisitos Técnicos del Sistema

Para desplegar y ejecutar el prototipo en un entorno local de pruebas o laboratorio, se requiere:

- **Sistema Operativo:** Windows 10/11 (64-bit), Linux (Ubuntu 20.04+) o macOS (Ventura+).
- **Procesador:** CPU de 64 bits con al menos 4 núcleos / 8 hilos a 2.0 GHz o superior (ej. AMD Ryzen 5 o Intel Core i5).
- **Memoria RAM:** Mínimo 8 GB (Recomendado 16 GB DDR4 para experimentación masiva con 1M de registros).
- **Almacenamiento Libre:** Mínimo 2 GB de espacio en disco de estado sólido (SSD).
- **Entorno de Ejecución:**
  - **Python:** Versión `3.10` a `3.14` (Probado formalmente bajo CPython `3.14.3`).
  - **Node.js:** Versión `18.x` o superior (con gestor de paquetes `npm`).
  - **Navegador Web:** Google Chrome, Mozilla Firefox, Microsoft Edge o Brave (con soporte de WebGL y JavaScript moderno).

---

## 2. Procedimiento de Instalación y Puesta en Marcha

### Paso 1: Clonación del Repositorio y Ubicación en la Raíz
Abrir una terminal de comandos (PowerShell, Bash o CMD) y posicionarse en la carpeta raíz del proyecto:
```bash
cd "d:\Proyecto Algoritmos"
```

### Paso 2: Instalación de Dependencias del Backend
Instalar las dependencias de Python requeridas para FastAPI, Pydantic y Pytest:
```bash
pip install fastapi uvicorn pydantic pytest httpx
```

### Paso 3: Instalación de Dependencias del Frontend
Acceder al subdirectorio `frontend/` e instalar los paquetes de Node.js:
```bash
cd frontend
npm install
cd ..
```

---

## 3. Ejecución de los Servicios en Entorno Local

Se requieren dos consolas de terminal abiertas simultáneamente para la operación completa:

### Terminal 1: Servidor Backend (FastAPI REST)
En la raíz del proyecto (`d:\Proyecto Algoritmos`), ejecutar el comando de arranque del servidor Uvicorn:
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
- **Resultado esperado en consola:**
  ```text
  INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
  INFO:     Started reloader process
  INFO:     Application startup complete.
  ```
- **Verificación de la API:** Acceder desde el navegador a la documentación interactiva Swagger:
  `http://127.0.0.1:8000/docs`
  o consultar el estado del servidor en: `http://127.0.0.1:8000/health`.

### Terminal 2: Servidor Cliente Web (React + Vite)
En la segunda terminal, posicionarse en `frontend/` y levantar el servidor de desarrollo:
```bash
cd frontend
npm run dev
```
- **Resultado esperado en consola:**
  ```text
  VITE v5.x.x  ready in 450 ms
  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ```
- **Acceso al Prototipo:** Abrir el navegador en `http://localhost:5173`.

---

## 4. Ejecución Automatizada de la Suite de Pruebas (Pytest)

Para certificar la integridad matemática y el correcto funcionamiento de los 44 casos de prueba automatizados, abrir una terminal en la raíz del proyecto y ejecutar:

```bash
python -m pytest
```

- **Resultado esperado:**
  ```text
  ======================== 44 passed, 1 warning in 8.31s ========================
  ```
  *(Confirma que el 100% de los algoritmos de ordenamiento, indexación KD-Tree, enrutamiento Dijkstra, clustering y endpoints de la API superaron todas las validaciones sin fallos).*

---

## 5. Guía de Operación Paso a Paso de los Módulos del Sistema

### Módulo 1: Mapa de Enrutamiento Seguro (`MapView.jsx`)
1. **Acceso al Módulo:** En la barra de navegación superior (`Navbar`), hacer clic en la pestaña **"Mapa de Rutas Seguras"**.
2. **Selección del Punto de Origen A:**
   - Escribir un hito de Medellín en el campo de texto superior (ej. *"Punto Cero"*, *"Tecnológico de Antioquia"*, *"Robledo"*).
   - O bien, hacer clic en el botón *"Usar mi ubicación actual"* para capturar las coordenadas GPS del dispositivo.
3. **Selección del Punto de Destino B:**
   - Escribir el lugar de destino (ej. *"El Poblado"*, *"Parque Berrío"*, *"EAFIT"*).
   - *(Opcional)* Arrastrar directamente el pin rojo sobre el mapa Leaflet para fijar cualquier coordenada arbitraria en el Valle de Aburrá.
4. **Regulación de la Prioridad de Seguridad:**
   - Deslizar el control horizontal:
     - Hacia la izquierda ($0\%$ de seguridad): Optimiza únicamente la distancia geométrica ($\alpha=1.0, \beta=0.0$).
     - Hacia la derecha ($100\%$ de seguridad): Penaliza fuertemente el riesgo histórico de colisiones ($\alpha=0.0, \beta=1.0$).
     - Valor recomendado predeterminado: **$80\%$ de prioridad de seguridad** ($\alpha=0.2, \beta=0.8$).
5. **Cálculo y Visualización de Rutas:**
   - Hacer clic en el botón verde flotante **"▶ CALCULAR RUTA SEGURA"**.
   - En pantalla aparecerán simultáneamente dos trazos continuos:
     - **Línea Azul:** La ruta más corta convencional, atravesando glorietas o vías principales de alto choque.
     - **Línea Verde Esmeralda:** La ruta más segura recomendada por el algoritmo de Dijkstra con *min-heap*, realizando desvíos controlados por vías colectoras seguras.
6. **Interpretación de la Tarjeta Comparativa (*Bottom Sheet*):**
   - En la parte inferior se muestra la comparativa lado a lado: distancia de cada opción, total de choques históricos en el paso y el porcentaje exacto de exposición al riesgo ahorrado (ej. *"¡Ahorras 89.4% de peligro con solo 500 m adicionales!"*).

---

### Módulo 2: Laboratorio de Jerarquía Asintótica (`AlgorithmLab.jsx`)
1. **Acceso al Módulo:** En la barra superior, hacer clic en **"Laboratorio de Algoritmos"**.
2. **Pestaña "Ejecución en Vivo":**
   - Seleccionar el tamaño de entrada deseado $n$ (`1.000`, `10.000`, `50.000`, `100.000`, `250.000`).
   - Seleccionar la clase asintótica que se desea evaluar:
     - `O(1)`: Acceso por tabla hash (`radicado`).
     - `O(log n)`: Búsqueda binaria cronológica por fecha.
     - `O(n)`: Escaneo secuencial y filtrado por comuna.
     - `O(n log n)`: Merge Sort puro sobre los siniestros.
     - `O(n²)`: Comparación exhaustiva de todos los pares espaciales a $<50\text{ m}$.
     - `Ejecutar Todas`: Ejecuta la batería completa secuencialmente.
   - Hacer clic en **"Ejecutar Benchmark en Vivo"**.
   - Las tarjetas HUD reportarán instantáneamente el tiempo medido en nanosegundos/milisegundos, el número exacto de operaciones elementales y la cota teórica asignada.
   - El lienzo vectorial superpondrá la curva empírica $T(n)$ sobre la función teórica normalizada $c \cdot g(n)$.
3. **Pestaña "Matriz Masiva (1K a 1M)":**
   - Permite consultar la matriz de experimentación exhaustiva de ordenamiento masivo (Merge Sort, Quick Sort Hoare con mediana de 3, Heap Sort, Counting Sort y Timsort) evaluada sobre 4 distribuciones de datos (aleatoria, ordenada, invertida y con duplicados masivos).

---

### Módulo 3: Tableros Analíticos EDA (`Dashboard.jsx`)
1. **Acceso al Módulo:** En la barra superior, hacer clic en **"Tablero de Siniestros (EDA)"**.
2. **Visualización de Estadísticas Históricas:**
   - Tarjeta de volumen total con los **251.150 incidentes oficiales** procesados.
   - Gráfico de barras con el ranking de las 10 comunas con mayor accidentalidad (La Candelaria, Laureles, Castilla, etc.).
   - Gráfico de distribución de severidad: Solo Daños (65%), Con Lesionados (33%) y Con Muertos (2%).
   - Filtros dinámicos por año para analizar el impacto de la pandemia de 2020 frente a la recuperación vehicular de 2022-2024.

---

## 6. Procedimiento para Generar el Paquete de Producción
Si se desea empaquetar el frontend estático para despliegue sin depender del servidor de desarrollo de Vite:
```bash
cd frontend
npm run build
```
- Este comando compila y optimiza los artefactos HTML, CSS y JavaScript minificados en la carpeta `frontend/dist/`, listos para ser servidos por un servidor web estático (Nginx, Apache o el propio FastAPI).

---

## 🔗 Relacionado
- [[00 - Inicio|Inicio]]
- [[Diseno-Frontend-UI]]
- [[Diseno-Backend-API]]
- [[Guion-Sustentacion-Oral]]
