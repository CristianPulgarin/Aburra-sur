"""
Generador de diagramas visuales en alta resolución para el documento AburráSegura.
Crea:
1. figura1_arquitectura_software.png: Arquitectura de 3 capas en lenguaje claro.
2. figura2_flujo_calculo_ruta.png: Diagrama de flujo del cálculo de ruta segura con Dijkstra.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "diagramas")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def draw_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 6.8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Fondo suave
    fig.patch.set_facecolor("#F8FAFC")
    ax.set_facecolor("#F8FAFC")

    # Título
    ax.text(50, 95, "Arquitectura Modular del Software (3 Capas)", 
            ha="center", va="center", fontsize=15, weight="bold", color="#0F172A", fontfamily="sans-serif")
    ax.text(50, 91, "Cómo se organizan y comunican las partes del sistema", 
            ha="center", va="center", fontsize=10, color="#64748B", fontfamily="sans-serif")

    # 1. Capa de Presentación
    box_pres = patches.FancyBboxPatch((8, 62), 84, 23, boxstyle="round,pad=1.5,rounding_size=3",
                                      facecolor="#EFF6FF", edgecolor="#3B82F6", linewidth=2)
    ax.add_patch(box_pres)
    ax.text(12, 80, "1. CAPA DE PRESENTACIÓN (EL CELULAR / NAVEGADOR WEB)", 
            fontsize=11, weight="bold", color="#1D4ED8", fontfamily="sans-serif")
    ax.text(12, 75, "• Desarrollada en React y Leaflet (mapa interactivo para ver las calles).", 
            fontsize=9.5, color="#1E293B", fontfamily="sans-serif")
    ax.text(12, 70, "• El usuario toca la pantalla para escoger dónde sale (origen) y a dónde va (destino).", 
            fontsize=9.5, color="#1E293B", fontfamily="sans-serif")
    ax.text(12, 65, "• Muestra en el mapa las dos rutas: la más corta en azul y la más segura en verde.", 
            fontsize=9.5, color="#1E293B", fontfamily="sans-serif")

    # Flecha 1 <-> 2
    ax.annotate("", xy=(50, 56), xytext=(50, 62),
                arrowprops=dict(arrowstyle="<->", color="#2563EB", lw=2, mutation_scale=15))
    ax.text(52, 59, "Envía origen/destino y recibe la ruta calculada (formato ligero JSON por Internet)", 
            fontsize=8.5, color="#475569", va="center", fontfamily="sans-serif")

    # 2. Capa de Lógica
    box_log = patches.FancyBboxPatch((8, 31), 84, 23, boxstyle="round,pad=1.5,rounding_size=3",
                                     facecolor="#F0FDF4", edgecolor="#10B981", linewidth=2)
    ax.add_patch(box_log)
    ax.text(12, 49, "2. CAPA DE LÓGICA Y SERVICIOS (EL SERVIDOR / CEREBRO EN PYTHON)", 
            fontsize=11, weight="bold", color="#047857", fontfamily="sans-serif")
    ax.text(12, 44, "• Programada en Python con FastAPI para responder peticiones en milisegundos.", 
            fontsize=9.5, color="#1E293B", fontfamily="sans-serif")
    ax.text(12, 39, "• Algoritmo de Dijkstra propio: busca el camino usando una cola de prioridad (min-heap).", 
            fontsize=9.5, color="#1E293B", fontfamily="sans-serif")
    ax.text(12, 34, "• Cronómetro de CPU de alta precisión: mide cuánto tarda el cálculo para evaluar la complejidad.", 
            fontsize=9.5, color="#1E293B", fontfamily="sans-serif")

    # Flecha 2 <-> 3
    ax.annotate("", xy=(50, 25), xytext=(50, 31),
                arrowprops=dict(arrowstyle="<->", color="#059669", lw=2, mutation_scale=15))
    ax.text(52, 28, "Carga las calles en memoria y consulta los datos históricos de siniestros", 
            fontsize=8.5, color="#475569", va="center", fontfamily="sans-serif")

    # 3. Capa de Datos
    box_dat = patches.FancyBboxPatch((8, 2), 84, 21, boxstyle="round,pad=1.5,rounding_size=3",
                                     facecolor="#FFFBEB", edgecolor="#F59E0B", linewidth=2)
    ax.add_patch(box_dat)
    ax.text(12, 19, "3. CAPA DE DATOS (BASE DE DATOS Y RED VIAL)", 
            fontsize=11, weight="bold", color="#B45309", fontfamily="sans-serif")
    ax.text(12, 14, "• Base de datos de más de 250.000 accidentes de Medellín (portal MEData de la Alcaldía).", 
            fontsize=9.5, color="#1E293B", fontfamily="sans-serif")
    ax.text(12, 9, "• Red de calles organizada como cruces (puntos) y vías con su sentido vehicular.", 
            fontsize=9.5, color="#1E293B", fontfamily="sans-serif")
    ax.text(12, 4, "• Cada calle tiene guardada su distancia en metros y la cantidad de choques históricos.", 
            fontsize=9.5, color="#1E293B", fontfamily="sans-serif")

    out_path = os.path.join(OUTPUT_DIR, "figura1_arquitectura_software.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Diagrama 1 generado: {out_path}")


def draw_flow_diagram():
    fig, ax = plt.subplots(figsize=(10, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    fig.patch.set_facecolor("#F8FAFC")
    ax.set_facecolor("#F8FAFC")

    # Título
    ax.text(50, 96, "Flujo de Cálculo de Rutas: ¿Cómo Funciona el Sistema?", 
            ha="center", va="center", fontsize=15, weight="bold", color="#0F172A", fontfamily="sans-serif")
    ax.text(50, 92, "Paso a paso desde que el usuario elige un destino hasta que ve la ruta segura", 
            ha="center", va="center", fontsize=10, color="#64748B", fontfamily="sans-serif")

    steps = [
        ("Paso 1: El usuario indica a dónde va",
         "Selecciona en la aplicación su punto de partida (o usa el GPS) y su destino.\nOpcionalmente ajusta qué tanta prioridad le da a la seguridad frente a la distancia.",
         "#EFF6FF", "#3B82F6", "#1D4ED8", 76),
        
        ("Paso 2: La solicitud viaja al servidor",
         "El celular envía las coordenadas al servidor por internet mediante una consulta liviana.\nEl servidor activa un temporizador de CPU para medir los milisegundos exactos de cálculo.",
         "#F0FDF4", "#10B981", "#047857", 58),
        
        ("Paso 3: Dijkstra busca los caminos en la red de calles",
         "El algoritmo recorre las calles conectadas. Para que no sea lento, usa una cola de prioridad\n(min-heap) que toma siempre la mejor opción siguiente sin revisar todas las calles a la vez.",
         "#FAF5FF", "#A855F7", "#7E22CE", 40),
        
        ("Paso 4: Se calculan dos opciones al mismo tiempo",
         "• Opción 1 (Más corta): Suma solo los metros de cada calle para hallar la distancia mínima.\n• Opción 2 (Más segura): Le suma un 'castigo' a las calles con muchos accidentes para esquivarlas.",
         "#FFF7ED", "#F97316", "#C2410C", 22),
        
        ("Paso 5: El usuario ve el resultado en su pantalla",
         "El celular dibuja en el mapa la ruta corta (azul) y la ruta segura (verde).\nMuestra cuántos metros más tiene la ruta segura y cuántos accidentes se evitan al tomarla.",
         "#ECFEFF", "#06B6D4", "#0E7490", 4),
    ]

    for title, desc, bg, border, title_col, y in steps:
        box = patches.FancyBboxPatch((10, y), 80, 13.5, boxstyle="round,pad=1.2,rounding_size=2.5",
                                     facecolor=bg, edgecolor=border, linewidth=1.8)
        ax.add_patch(box)
        ax.text(13, y + 10.5, title, fontsize=10.5, weight="bold", color=title_col, fontfamily="sans-serif")
        ax.text(13, y + 4.5, desc, fontsize=8.8, color="#334155", fontfamily="sans-serif")

        # Flecha al siguiente paso
        if y > 5:
            ax.annotate("", xy=(50, y - 3), xytext=(50, y),
                        arrowprops=dict(arrowstyle="->", color="#94A3B8", lw=2, mutation_scale=12))

    out_path = os.path.join(OUTPUT_DIR, "figura2_flujo_calculo_ruta.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Diagrama 2 generado: {out_path}")


if __name__ == "__main__":
    draw_architecture_diagram()
    draw_flow_diagram()
