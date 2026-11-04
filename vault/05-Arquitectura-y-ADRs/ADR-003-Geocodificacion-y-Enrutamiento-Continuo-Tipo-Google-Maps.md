---
titulo: "ADR-003: Geocodificación Urbana Híbrida y Proyección Continua"
tipo: decision
tipo: adr
proyecto: PPI - Analisis de Algoritmos
institucion: Tecnologico de Antioquia
estado: Aceptado
fecha: 2026-09-30
decisores: Orquestador, Backend Dev, Frontend Dev, Especialista en Algoritmos
vigencia: en_revision
audiencia: [negocio, tecnico]
actualizado: 2026-10-19
etiquetas: [tipo/decision, ppi/tdea, proyecto/aburrasegura]
---


> [!NOTE] En revisión (alcance replanteado)
> La geocodificación y el enrutamiento continuo tipo Google Maps quedan fuera del alcance mínimo; evaluar si se conservan. Alcance vigente: [[ADR-005-Replanteamiento-Alcance-Dijkstra-Puntos-Criticos-y-Laboratorio-Complejidad]].

# ADR-003: Geocodificación Urbana Híbrida y Enrutamiento Continuo Punto A a Punto B (Experiencia Tipo Google Maps)

> [!abstract] En pocas palabras
> Estrategia de proyección continua de coordenadas arbitrarias del usuario hacia los nodos más cercanos del grafo vial mediante KD-Tree.


## Contexto y Planteamiento del Problema
En la versión inicial del módulo de mapas, el usuario seleccionaba puntos de origen y destino mediante listas desplegables asociadas a identificadores discretos de nodos de la red vial (`Nodo 1: Av. Oriental`, `Nodo 22: El Poblado`). 

Sin embargo, en aplicaciones cartográficas modernas de producción (como Google Maps), los usuarios esperan ingresar direcciones textuales arbitrarias, nombres de instituciones o lugares de interés (POI), hacer clic libre sobre el mapa o arrastrar los pines de origen y destino. Además, los puntos de partida y llegada no necesariamente coinciden con una intersección vial predefinida, sino que requieren una conexión espacial continua desde la acera/puerta hacia la malla vial.

## Decisión Técnica Adoptada

1. **Geocodificación Híbrida de Alta Resiliencia y Baja Latencia**:
   - **Nivel 1 (Catálogo Local Offline de Medellín)**: Se implementó un catálogo con más de 40 hitos urbanos icónicos (TdeA, UdeA, UPB, EAFIT, Hospital San Vicente, Clínicas, Parques Lleras y Berrio, Estaciones del Metro, etc.) para resolución en tiempo inferior a 1 ms sin depender de cuotas de red.
   - **Nivel 2 (OpenStreetMap Nominatim Bounded)**: Para direcciones residenciales o comerciales específicas con numeración de vías (ej. *Calle 50 # 43-20*), el backend consulta la API Nominatim restringida estrictamente al Valle de Aburrá (`viewbox=-75.68,6.15,-75.48,6.38`, `bounded=1`).
   - **Caché en Memoria LRU**: Almacena consultas frecuentes para respuesta sub-milisegundo.
   - **Geocodificación Inversa (`/reverse-geocode`)**: Convierte cualquier clic o arrastre de coordenadas en el mapa en una dirección o hito legible.

2. **Proyección Espacial Continua ($k$-d Tree 2D)**:
   - Los puntos de entrada $A = (lat_A, lon_A)$ y salida $B = (lat_B, lon_B)$ se proyectan al nodo vial más cercano $N_{start}$ y $N_{target}$ mediante el árbol espacial `KDTree2D` implementado desde cero, garantizando una complejidad de búsqueda de $O(\log V)$.
   - Se calculan las distancias de aproximación $d(A, N_{start})$ y $d(N_{target}, B)$ mediante la fórmula geodésica de Haversine.
   - La polilínea resultante generada por los algoritmos $A^*$ y Dijkstra ensambla los segmentos continuos:
     $$\text{Trayecto} = [A, \text{coords}(N_{start}), \dots, \text{coords}(N_{target}), B]$$
   - La distancia total refleja con fidelidad el recorrido puerta a puerta.

3. **Interfaz de Usuario Estilo Google Maps en React + Leaflet**:
   - Inputs predictivos independientes para Punto A (verde) y Punto B (rojo) con dropdown de sugerencias filtradas con debounce de 250 ms.
   - Botón de intercambio rápido (Swap) $\updownarrow$.
   - Botón de geolocalización GPS por navegador ("Mi Ubicación actual").
   - Marcadores interactivos Leaflet con arrastre en vivo (`draggable: true`). Al soltar el pin, se activa la geocodificación inversa y se actualiza el trayecto.
   - Modo de selección interactiva por clic en el lienzo cartográfico.

## Consecuencias y Beneficios

- **Usabilidad**: Experiencia idéntica a Google Maps, accesible para cualquier usuario sin conocimientos de la topología interna del grafo.
- **Rigor Algorítmico**: El modelo matemático no se desvirtúa; por el contrario, integra armónicamente la estructura espacial $k$-d Tree 2D para la proyección continua con los algoritmos de grafos $A^*$ y Dijkstra para la resolución multiobjetivo.
- **Resiliencia Operativa**: La aplicación es 100% autónoma y funcional aun en entornos cerrados de laboratorio sin internet gracias al catálogo enriquecido de Medellín.

---

## 🔗 Relacionado
- [[00 - Inicio|Inicio]]
- [[Estructuras-Espaciales-KDTree]]
- [[Grafos-Dijkstra-AStar]]
- [[Diseno-Backend-API]]
