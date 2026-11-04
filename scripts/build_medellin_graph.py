"""
Constructor de la Red Vial de Medellín (Road Network Graph Builder).
Modela la malla vial urbana completa con intersecciones y vías arteriales/secundarias.
Mapea los siniestros viales reales sobre las aristas viales para calcular el factor_riesgo histórico.
Exporta el grafo resultante a data/processed/medellin_graph.json.
"""

import os
import sys
import json
import sqlite3

# Añadir la raíz del proyecto al sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.algorithms.spatial_kdtree import KDTree2D, haversine_distance

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "processed", "medellin_incidents.db")
OUTPUT_GRAPH_JSON = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "processed", "medellin_graph.json")

# Intersecciones viales estratégicas de Medellín (latitud, longitud, nombre)
KEY_INTERSECTIONS = [
    # Centro / La Candelaria
    (1, 6.2518, -75.5636, "Av. Oriental con San Juan (Cl 44 x Cra 46)"),
    (2, 6.2525, -75.5670, "San Juan con Carabobo (Cl 44 x Cra 52)"),
    (3, 6.2560, -75.5645, "Av. Oriental con Colombia (Cl 50 x Cra 46)"),
    (4, 6.2570, -75.5695, "Colombia con Carabobo (Cl 50 x Cra 52)"),
    (5, 6.2465, -75.5690, "San Diego (Glorieta San Diego / Las Palmas)"),
    (6, 6.2420, -75.5740, "Puente Guayaquil / Av. Regional"),
    # Corredor del Río / Autopistas
    (7, 6.2480, -75.5765, "San Juan con Autopista Sur (Cl 44)"),
    (8, 6.2550, -75.5780, "Autopista Sur con Colombia (Puente Colombia)"),
    (9, 6.2670, -75.5750, "Punto Cero Norte (Cl 67 Barranquilla x Autopista)"),
    (10, 6.2350, -75.5770, "Av. Regional con Calle 33"),
    (11, 6.2080, -75.5760, "Puente 4 Sur (Gilberto Echeverri x Av. Regional)"),
    (12, 6.1950, -75.5780, "La Aguacatala (Av. Regional x Cl 12 Sur)"),
    # Laureles / Estadio / Belén
    (13, 6.2480, -75.5860, "San Juan con Cra 65"),
    (14, 6.2460, -75.5920, "San Juan con Cra 70 (Glorieta de la 70)"),
    (15, 6.2440, -75.6020, "San Juan con Cra 80"),
    (16, 6.2530, -75.5910, "Estadio / Colombia con Cra 70"),
    (17, 6.2360, -75.5870, "Glorieta de la 33 con Cra 65"),
    (18, 6.2340, -75.5930, "Glorieta de Bulerías (Cl 33 x Nutibara)"),
    (19, 6.2310, -75.6040, "Calle 33 con Cra 80"),
    (20, 6.2230, -75.6020, "Belén Parque (Cl 30 x Cra 76)"),
    (21, 6.2220, -75.5920, "Cl 30 con Cra 65"),
    # El Poblado / Guayabal
    (22, 6.2090, -75.5680, "Parque El Poblado (Cra 43A x Cl 10)"),
    (23, 6.2100, -75.5720, "Av. Las Vegas con Cl 10 (Cra 48 x Cl 10)"),
    (24, 6.2085, -75.5650, "Provenza (Cra 35 x Cl 10)"),
    (25, 6.1980, -75.5710, "Santa Fe / Milla de Oro (Cra 43A x Cl 7)"),
    (26, 6.1960, -75.5740, "Av. Las Vegas con Cl 4 Sur"),
    (27, 6.2170, -75.5830, "Av. Guayabal con Cl 10 (Cra 52 x Cl 10)"),
    (28, 6.2250, -75.5810, "Av. Guayabal con Cl 30 (Cra 52 x Cl 30)"),
    # Norte / Castilla / Aranjuez
    (29, 6.2730, -75.5660, "Aranjuez / Carabobo Norte con Cl 77"),
    (30, 6.2750, -75.5750, "Castilla / Cra 65 con Cl 77"),
    (31, 6.2850, -75.5710, "Puente Madre Laura (Cra 65 x Autopista Norte)"),
    (32, 6.2780, -75.5850, "Robledo / Cl 65 con Cra 80"),
    # Corredores Estratégicos Adicionales (Occidente, Robledo, Cra 80 completa)
    (33, 6.2550, -75.5990, "Av. Colombia con Cra 80 (Calasanz / La Floresta)"),
    (34, 6.2640, -75.5940, "Cra 80 con Calle 65 (Facultad de Minas / Robledo)"),
    (35, 6.2730, -75.5900, "Parque de Robledo (Cra 80 con Calle 75)"),
    (36, 6.2804, -75.5912, "Tecnológico de Antioquia TdeA (Robledo)"),
    (37, 6.2620, -75.5870, "Calle 65 con Cra 70 (Iguaná / San Germán)"),
    (38, 6.2610, -75.5800, "Calle 65 con Cra 65 (San Germán / Univ. Nacional)"),
    (39, 6.2550, -75.5850, "Av. Colombia con Cra 65 (Carlos E. Restrepo)"),
    (40, 6.2150, -75.6020, "Cra 80 con Calle 30 (La Palma / Belén)"),
    (41, 6.1950, -75.5900, "Cra 80 con Calle 12 Sur (La Aguacatala Occidente)"),
    (42, 6.2410, -75.5950, "Av. Nutibara con San Juan (Laureles)"),
]

# Tramos viales de conexión (from_id, to_id, name, speed_kmh, bidirectional)
ROAD_SEGMENTS = [
    # San Juan (Calle 44)
    (15, 14, "Av. San Juan (Cra 80 a Cra 70)", 50, True),
    (14, 13, "Av. San Juan (Cra 70 a Cra 65)", 50, True),
    (13, 7,  "Av. San Juan (Cra 65 a Autopista)", 60, True),
    (7, 2,   "Av. San Juan (Puente San Juan a Carabobo)", 50, True),
    (2, 1,   "Av. San Juan (Carabobo a Av. Oriental)", 40, True),

    # Colombia (Calle 50)
    (4, 3,   "Av. Colombia (Carabobo a Av. Oriental)", 35, True),
    (8, 4,   "Av. Colombia (Puente Colombia a Carabobo)", 40, True),
    (39, 8,  "Av. Colombia (Cra 65 a Autopista)", 50, True),
    (16, 39, "Av. Colombia (Cra 70 Estadio a Cra 65)", 50, True),
    (33, 16, "Av. Colombia (Cra 80 Calasanz a Cra 70)", 50, True),

    # Avenida Oriental (Cra 46)
    (1, 3,   "Av. Oriental (San Juan a Colombia)", 40, True),
    (1, 5,   "Av. Oriental (San Juan a San Diego)", 40, True),

    # Avenida 33
    (19, 18, "Av. 33 (Cra 80 a Bulerias)", 50, True),
    (18, 17, "Av. 33 (Bulerias a Cra 65)", 50, True),
    (17, 10, "Av. 33 (Cra 65 a Autopista Sur)", 60, True),
    (10, 5,  "Av. 33 (Puente de la 33 a San Diego)", 60, True),

    # Autopista Sur / Av. Regional (Corredor Norte-Sur)
    (12, 11, "Av. Regional (Aguacatala a Puente 4 Sur)", 80, False),
    (11, 10, "Av. Regional (Puente 4 Sur a Cl 33)", 80, False),
    (10, 6,  "Av. Regional (Cl 33 a Guayaquil)", 80, False),
    (6, 7,   "Av. Regional (Guayaquil a San Juan)", 80, False),
    (7, 8,   "Av. Regional (San Juan a Colombia)", 80, False),
    (8, 9,   "Av. Regional (Colombia a Barranquilla / Punto Cero)", 80, False),
    (9, 31,  "Autopista Norte (Punto Cero a Madre Laura)", 80, False),

    # En sentido contrario (Autopista Sur)
    (31, 9,  "Autopista Sur (Madre Laura a Punto Cero)", 80, False),
    (9, 8,   "Autopista Sur (Punto Cero a Colombia)", 80, False),
    (8, 7,   "Autopista Sur (Colombia a San Juan)", 80, False),
    (7, 6,   "Autopista Sur (San Juan a Guayaquil)", 80, False),
    (6, 10,  "Autopista Sur (Guayaquil a Cl 33)", 80, False),
    (10, 11, "Autopista Sur (Cl 33 a Puente 4 Sur)", 80, False),
    (11, 12, "Autopista Sur (Puente 4 Sur a Aguacatala)", 80, False),

    # El Poblado (Cra 43A y Cra 48 Las Vegas)
    (5, 23,  "Av. Las Vegas (San Diego a Cl 10)", 60, True),
    (23, 26, "Av. Las Vegas (Cl 10 a Cl 4 Sur)", 60, True),
    (26, 12, "Av. Las Vegas (Cl 4 Sur a Aguacatala)", 60, True),
    (5, 22,  "Av. El Poblado (San Diego a Parque Poblado)", 40, True),
    (22, 25, "Av. El Poblado (Parque Poblado a Milla de Oro)", 40, True),
    (22, 24, "Calle 10 (Parque Poblado a Provenza)", 30, True),
    (23, 22, "Calle 10 (Las Vegas a Parque Poblado)", 40, True),
    (11, 26, "Puente 4 Sur a Las Vegas", 50, True),

    # Guayabal y Belén
    (10, 28, "Av. Guayabal hacia Cl 30", 50, True),
    (28, 27, "Av. Guayabal (Cl 30 a Cl 10)", 50, True),
    (28, 21, "Calle 30 (Guayabal a Cra 65)", 50, True),
    (21, 20, "Calle 30 (Cra 65 a Parque Belén)", 40, True),
    (20, 40, "Calle 30 (Parque Belén a Cra 80 La Palma)", 40, True),

    # Corredor Carrera 80 Completo (Sur a Norte: Aguacatala - Belén - Laureles - Robledo)
    (41, 40, "Av. 80 (Aguacatala Occidente a La Palma)", 60, True),
    (40, 20, "Av. 80 (La Palma a Parque Belen)", 50, True),
    (20, 19, "Av. 80 (Belén a Calle 33)", 50, True),
    (19, 15, "Av. 80 (Calle 33 a San Juan)", 50, True),
    (15, 33, "Av. 80 (San Juan a Colombia / Calasanz)", 50, True),
    (33, 34, "Av. 80 (Calasanz a Facultad de Minas)", 50, True),
    (34, 32, "Av. 80 (Facultad de Minas a Cl 65 Robledo)", 50, True),
    (32, 35, "Cra 80 (Robledo Cl 65 a Parque Robledo)", 40, True),
    (35, 36, "Cra 80 a Tecnologico de Antioquia TdeA", 40, True),

    # Corredor Calle 65 (Vía al Mar / San Germán / Robledo)
    (38, 37, "Calle 65 (Cra 65 a Cra 70 San Germán)", 50, True),
    (37, 34, "Calle 65 (Cra 70 a Facultad de Minas / Cra 80)", 50, True),
    (34, 32, "Calle 65 (Facultad de Minas a Robledo)", 40, True),
    (32, 36, "Conexión Robledo a Tecnológico de Antioquia TdeA", 40, True),

    # Corredor Carrera 65 (Centro-Occidente a Noroccidente)
    (13, 17, "Cra 65 (San Juan a Cl 33)", 50, True),
    (13, 39, "Cra 65 (San Juan a Colombia Carlos E)", 50, True),
    (39, 38, "Cra 65 (Colombia a San Germán / Univ Nacional)", 50, True),
    (38, 9,  "Cra 65 a Punto Cero Norte", 50, True),
    (38, 30, "Cra 65 (San Germán a Castilla Cl 77)", 50, True),

    # Corredor Carrera 70 (Laureles / Estadio / San Germán)
    (14, 16, "Cra 70 (San Juan a Estadio)", 40, True),
    (16, 37, "Cra 70 (Estadio a Calle 65 San Germán)", 40, True),
    (14, 18, "Nutibara (San Juan a Bulerias)", 40, True),
    (18, 42, "Nutibara (Bulerías a San Juan Nutibara)", 40, True),
    (42, 14, "San Juan con Nutibara", 40, True),

    # Conexiones Norte (Aranjuez, Castilla, Robledo)
    (9, 29,  "Cl 67 Barranquilla a Carabobo Norte", 40, True),
    (9, 30,  "Cl 67 Barranquilla a Castilla (Cra 65)", 50, True),
    (30, 31, "Cra 65 a Puente Madre Laura", 50, True),
    (30, 32, "Conexión Castilla a Robledo (Cl 65)", 40, True),

    # Conexión Sur Calle 12 Sur
    (12, 41, "Calle 12 Sur (Regional a Av 80 Aguacatala)", 50, True),
]


def build_network():
    print("Iniciando construcción de la red vial expandida de Medellín...")
    nodes_dict = {item[0]: {"lat": item[1], "lon": item[2], "name": item[3]} for item in KEY_INTERSECTIONS}
    edges_list = []

    edge_id_counter = 1
    for u, v, name, speed, bi in ROAD_SEGMENTS:
        lat1, lon1 = nodes_dict[u]["lat"], nodes_dict[u]["lon"]
        lat2, lon2 = nodes_dict[v]["lat"], nodes_dict[v]["lon"]
        dist = haversine_distance(lat1, lon1, lat2, lon2)

        edges_list.append({
            "edge_id": edge_id_counter,
            "from_node": u,
            "to_node": v,
            "name": name,
            "length_m": round(dist, 1),
            "max_speed": speed,
            "risk_score": 0.0,
            "incident_count": 0
        })
        edge_id_counter += 1

        if bi:
            edges_list.append({
                "edge_id": edge_id_counter,
                "from_node": v,
                "to_node": u,
                "name": name + " (Sentido Opuesto)",
                "length_m": round(dist, 1),
                "max_speed": speed,
                "risk_score": 0.0,
                "incident_count": 0
            })
            edge_id_counter += 1

    print(f"Red base creada: {len(nodes_dict)} intersecciones, {len(edges_list)} tramos viales dirigidos.")

    # Mapear siniestros reales para calcular riesgo histórico por tramo
    if os.path.exists(DB_PATH):
        print(f"Cargando siniestros desde SQLite: {DB_PATH}")
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT latitud, longitud, factor_riesgo FROM incidents;")
        rows = cur.fetchall()
        conn.close()
        print(f"Total siniestros para cálculo de riesgo: {len(rows):,}")

        # El riesgo se acumula por corredor: el par de intersecciones {u, v}, sin importar el sentido.
        # Todas las aristas dirigidas entre u y v (ambos sentidos de una calle, o calzadas paralelas
        # como Av. Regional / Autopista Sur) son la misma recta en el modelo y comparten punto medio.
        # Antes se indexaba cada arista: el KD-Tree devolvía solo una y las demás quedaban con riesgo 0.
        corridor_midpoints = []
        for key in sorted({tuple(sorted((e["from_node"], e["to_node"]))) for e in edges_list}):
            u, v = key
            mid_lat = (nodes_dict[u]["lat"] + nodes_dict[v]["lat"]) / 2.0
            mid_lon = (nodes_dict[u]["lon"] + nodes_dict[v]["lon"]) / 2.0
            corridor_midpoints.append(((mid_lat, mid_lon), key))

        # Indexar corredores con KD-Tree
        kdtree = KDTree2D(corridor_midpoints)

        corridor_risk_map = {key: {"risk": 0.0, "count": 0} for _, key in corridor_midpoints}

        for lat, lon, factor in rows:
            _, key, dist_m, _ = kdtree.nearest_neighbor((lat, lon))
            # Si el siniestro ocurrió a menos de 400m del tramo vial
            if dist_m <= 400.0:
                corridor_risk_map[key]["risk"] += factor
                corridor_risk_map[key]["count"] += 1

        # Cada arista dirigida hereda el riesgo de su corredor
        for e in edges_list:
            key = tuple(sorted((e["from_node"], e["to_node"])))
            e["risk_score"] = round(corridor_risk_map[key]["risk"], 1)
            e["incident_count"] = corridor_risk_map[key]["count"]

        print("Puntajes de riesgo asignados a cada tramo vial según datos reales.")

    # Guardar grafo en JSON
    graph_data = {
        "nodes": nodes_dict,
        "edges": edges_list
    }

    with open(OUTPUT_GRAPH_JSON, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)

    print(f"Grafo de Medellín serializado con éxito en: {OUTPUT_GRAPH_JSON}")


if __name__ == "__main__":
    build_network()
