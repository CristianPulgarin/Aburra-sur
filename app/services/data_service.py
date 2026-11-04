"""
Servicio de Acceso a Datos, Geocodificación y Enrutamiento Multiobjetivo.
Interactúa con medellin_incidents.db, medellin_graph.json, Nominatim OSM y catálogo local de Medellín.
"""

import os
import json
import sqlite3
import unicodedata
import urllib.request
import urllib.parse
from typing import Dict, List, Optional, Tuple, Any

from app.algorithms.graph_routing import RoadNetworkGraph, a_star_routing, dijkstra_routing
from app.algorithms.spatial_kdtree import KDTree2D, haversine_distance
from app.services import db_builder

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "data", "processed", "medellin_incidents.db")
GRAPH_JSON_PATH = os.path.join(BASE_DIR, "data", "processed", "medellin_graph.json")


def _normalize_text(text: str) -> str:
    """Elimina tildes y convierte a minúsculas para búsquedas difusas."""
    if not text:
        return ""
    nfkd = unicodedata.normalize("NFKD", text)
    cleaned = "".join([c for c in nfkd if not unicodedata.combining(c)]).lower()
    for ch in ["#", "-", "_", ",", ".", "/", ";", ":"]:
        cleaned = cleaned.replace(ch, " ")
    return " ".join(cleaned.split())


ADDRESS_SYNONYMS = {
    "cra": "carrera",
    "kr": "carrera",
    "cll": "calle",
    "cl": "calle",
    "c": "calle",
    "av": "avenida",
    "ave": "avenida",
    "diag": "diagonal",
    "dg": "diagonal",
    "trans": "transversal",
    "tv": "transversal",
    "tdea": "tecnologico",
    "udea": "antioquia",
    "unal": "nacional",
    "upb": "bolivariana",
}


def _tokenize_text(text: str) -> List[str]:
    norm = _normalize_text(text)
    raw_tokens = norm.split()
    return [ADDRESS_SYNONYMS.get(t, t) for t in raw_tokens if len(t) > 0]


# Catálogo local exhaustivo de lugares emblemáticos y puntos clave de Medellín
# Garantiza respuesta < 1ms incluso sin conexión externa a internet
MEDELLIN_POI_CATALOG: List[Dict[str, Any]] = [
    # Instituciones Educativas y Universidades
    {"name": "Tecnológico de Antioquia (TdeA)", "display_name": "Tecnológico de Antioquia (TdeA) - Robledo, Medellín", "lat": 6.2804, "lon": -75.5912, "category": "Universidad"},
    {"name": "Universidad de Antioquia (UdeA)", "display_name": "Universidad de Antioquia (UdeA) - Ciudad Universitaria, Medellín", "lat": 6.2675, "lon": -75.5684, "category": "Universidad"},
    {"name": "Universidad Nacional de Colombia", "display_name": "Universidad Nacional de Colombia - Sede Medellín, Robledo", "lat": 6.2612, "lon": -75.5786, "category": "Universidad"},
    {"name": "Universidad Pontificia Bolivariana (UPB)", "display_name": "Universidad Pontificia Bolivariana (UPB) - Campus Laureles, Medellín", "lat": 6.2428, "lon": -75.5901, "category": "Universidad"},
    {"name": "Universidad EAFIT", "display_name": "Universidad EAFIT - El Poblado, Medellín", "lat": 6.2007, "lon": -75.5785, "category": "Universidad"},
    {"name": "Universidad de Medellín", "display_name": "Universidad de Medellín - Los Alpes / Belén, Medellín", "lat": 6.2312, "lon": -75.6105, "category": "Universidad"},
    {"name": "Politécnico Jaime Isaza Cadavid", "display_name": "Politécnico Jaime Isaza Cadavid - El Poblado, Medellín", "lat": 6.2120, "lon": -75.5770, "category": "Universidad"},
    {"name": "ITM Robledo", "display_name": "Instituto Tecnológico Metropolitano (ITM) - Robledo, Medellín", "lat": 6.2789, "lon": -75.5872, "category": "Universidad"},

    # Centros de Salud y Hospitales
    {"name": "Hospital San Vicente Fundación", "display_name": "Hospital Universitario San Vicente Fundación - Sevilla / Prado, Medellín", "lat": 6.2625, "lon": -75.5668, "category": "Hospital"},
    {"name": "Hospital General de Medellín", "display_name": "Hospital General de Medellín - El Perpetuo Socorro, Medellín", "lat": 6.2389, "lon": -75.5715, "category": "Hospital"},
    {"name": "Hospital Pablo Tobón Uribe", "display_name": "Hospital Pablo Tobón Uribe - Robledo, Medellín", "lat": 6.2809, "lon": -75.5863, "category": "Hospital"},
    {"name": "Clínica Las Vegas", "display_name": "Clínica Las Vegas - El Poblado, Medellín", "lat": 6.2035, "lon": -75.5758, "category": "Hospital"},
    {"name": "Clínica Medellín El Poblado", "display_name": "Clínica Medellín - El Poblado, Medellín", "lat": 6.2088, "lon": -75.5672, "category": "Hospital"},

    # Estaciones Clave del Metro y Terminales de Transporte
    {"name": "Terminal del Norte", "display_name": "Terminal de Transporte del Norte - Caribe, Medellín", "lat": 6.2736, "lon": -75.5721, "category": "Transporte"},
    {"name": "Terminal del Sur", "display_name": "Terminal de Transporte del Sur - Guayabal, Medellín", "lat": 6.2132, "lon": -75.5867, "category": "Transporte"},
    {"name": "Estación San Antonio (Metro)", "display_name": "Estación Metro San Antonio - Centro / La Candelaria, Medellín", "lat": 6.2471, "lon": -75.5694, "category": "Metro"},
    {"name": "Estación Parque Berrío (Metro)", "display_name": "Estación Metro Parque Berrío - Centro, Medellín", "lat": 6.2497, "lon": -75.5678, "category": "Metro"},
    {"name": "Estación Poblado (Metro)", "display_name": "Estación Metro Poblado - El Poblado, Medellín", "lat": 6.2104, "lon": -75.5768, "category": "Metro"},
    {"name": "Estación Estadio (Metro)", "display_name": "Estación Metro Estadio - Cra 70, Medellín", "lat": 6.2530, "lon": -75.5898, "category": "Metro"},
    {"name": "Estación Aguacatala (Metro)", "display_name": "Estación Metro Aguacatala - Las Vegas / Regional, Medellín", "lat": 6.1950, "lon": -75.5780, "category": "Metro"},
    {"name": "Estación Floresta (Metro)", "display_name": "Estación Metro Floresta - Cl 47D con Cra 80, Medellín", "lat": 6.2588, "lon": -75.5976, "category": "Metro"},

    # Parques, Turismo, Cultura y Entretenimiento
    {"name": "Parque Lleras", "display_name": "Parque Lleras - Zona Rosa El Poblado, Medellín", "lat": 6.2089, "lon": -75.5677, "category": "Turismo"},
    {"name": "Provenza", "display_name": "Provenza - Vía Primavera, El Poblado, Medellín", "lat": 6.2085, "lon": -75.5650, "category": "Turismo"},
    {"name": "Plaza Botero / Museo de Antioquia", "display_name": "Plaza Botero - Museo de Antioquia, Centro de Medellín", "lat": 6.2520, "lon": -75.5680, "category": "Cultura"},
    {"name": "Estadio Atanasio Girardot", "display_name": "Estadio Atanasio Girardot / Complejo Deportivo - Medellín", "lat": 6.2568, "lon": -75.5904, "category": "Deporte"},
    {"name": "Parque Explora / Jardín Botánico", "display_name": "Parque Explora / Jardín Botánico Joaquín Antonio Uribe - Medellín", "lat": 6.2707, "lon": -75.5655, "category": "Parque"},
    {"name": "Plaza Mayor Convenciones", "display_name": "Plaza Mayor Centro de Convenciones y Exposiciones - Medellín", "lat": 6.2435, "lon": -75.5742, "category": "Eventos"},
    {"name": "Pueblito Paisa (Cerro Nutibara)", "display_name": "Pueblito Paisa - Cerro Nutibara, Medellín", "lat": 6.2361, "lon": -75.5804, "category": "Turismo"},
    {"name": "Parque de Belén", "display_name": "Parque Principal de Belén - Medellín", "lat": 6.2230, "lon": -75.6020, "category": "Parque"},
    {"name": "Primer Parque de Laureles", "display_name": "Primer Parque de Laureles (Transversal 39B) - Medellín", "lat": 6.2476, "lon": -75.5938, "category": "Parque"},
    {"name": "Segundo Parque de Laureles", "display_name": "Segundo Parque de Laureles (Av. Nutibara) - Medellín", "lat": 6.2449, "lon": -75.5955, "category": "Parque"},
    {"name": "Ciudad del Río", "display_name": "Ciudad del Río - Museo de Arte Moderno (MAMM), Medellín", "lat": 6.2224, "lon": -75.5745, "category": "Cultura"},
    {"name": "Parque de San Diego", "display_name": "Centro Comercial y Glorieta de San Diego - Medellín", "lat": 6.2465, "lon": -75.5690, "category": "Comercial"},

    # Centros Comerciales
    {"name": "Centro Comercial Santafé", "display_name": "Centro Comercial Santafé - El Poblado, Medellín", "lat": 6.1979, "lon": -75.5738, "category": "Comercial"},
    {"name": "Centro Comercial El Tesoro", "display_name": "Parque Comercial El Tesoro - Loma El Tesoro, Poblado, Medellín", "lat": 6.2001, "lon": -75.5583, "category": "Comercial"},
    {"name": "Centro Comercial Viva Envigado", "display_name": "Centro Comercial Viva Envigado - Av. Las Vegas, Envigado", "lat": 6.1772, "lon": -75.5912, "category": "Comercial"},
    {"name": "Centro Comercial Unicentro", "display_name": "Centro Comercial Unicentro - Laureles / Bolivariana, Medellín", "lat": 6.2405, "lon": -75.5888, "category": "Comercial"},
    {"name": "Centro Comercial Los Molinos", "display_name": "Centro Comercial Los Molinos - Belén / Cra 80, Medellín", "lat": 6.2325, "lon": -75.6045, "category": "Comercial"},

    # Corredores Viales y Puntos de Intersección
    {"name": "Avenida San Juan con Carrera 70", "display_name": "Av. San Juan (Cl 44) con Cra 70 (Glorieta de la 70), Medellín", "lat": 6.2460, "lon": -75.5920, "category": "Vía"},
    {"name": "Avenida San Juan con Carrera 80", "display_name": "Av. San Juan (Cl 44) con Cra 80 - La América, Medellín", "lat": 6.2440, "lon": -75.6020, "category": "Vía"},
    {"name": "Avenida Colombia con Autopista Sur", "display_name": "Puente Colombia con Autopista Sur (Cl 50), Medellín", "lat": 6.2550, "lon": -75.5780, "category": "Vía"},
    {"name": "Avenida Oriental con San Juan", "display_name": "Av. Oriental (Cra 46) con San Juan (Cl 44) - Centro, Medellín", "lat": 6.2518, "lon": -75.5636, "category": "Vía"},
    {"name": "Glorieta de Bulerías", "display_name": "Glorieta de Bulerías (Av. 33 con Av. Nutibara) - Laureles, Medellín", "lat": 6.2340, "lon": -75.5930, "category": "Vía"},
    {"name": "Punto Cero (Barranquilla)", "display_name": "Punto Cero - Calle 67 Barranquilla con Autopista Norte, Medellín", "lat": 6.2670, "lon": -75.5750, "category": "Vía"},
    {"name": "Puente Madre Laura", "display_name": "Puente Madre Laura - Castilla / Aranjuez, Medellín", "lat": 6.2850, "lon": -75.5710, "category": "Vía"},

    # Valle de Aburrá Sur e Itagüí
    {"name": "Carrera 58G # 60B-18 (Santa María, Itagüí)", "display_name": "Carrera 58G # 60B-18 - Barrio Santa María, Itagüí", "lat": 6.1755, "lon": -75.6075, "category": "Residencial"},
    {"name": "Cra 58G # 60B-18", "display_name": "Cra 58G # 60B-18 - Santa María, Itagüí", "lat": 6.1755, "lon": -75.6075, "category": "Residencial"},
    {"name": "Santa María (Itagüí)", "display_name": "Calle 60B Santa María - Itagüí, Antioquia", "lat": 6.1755, "lon": -75.6075, "category": "Barrio"},
    {"name": "Calle 60B Santa María", "display_name": "Calle 60B Santa María - Itagüí, Valle de Aburrá", "lat": 6.1755, "lon": -75.6075, "category": "Vía"},
    {"name": "Parque del Artista (Itagüí)", "display_name": "Parque del Artista - Cra 52 con Cl 60, Itagüí", "lat": 6.1740, "lon": -75.6080, "category": "Parque"},
    {"name": "Las Chimeneas (Itagüí)", "display_name": "Parque Las Chimeneas - Cra 52 con Cl 85, Itagüí", "lat": 6.1825, "lon": -75.5985, "category": "Parque"},
    {"name": "Parque Principal de Itagüí", "display_name": "Parque Principal de Itagüí - Centro, Cra 51 con Cl 51", "lat": 6.1718, "lon": -75.6120, "category": "Parque"},
    {"name": "Centro de la Moda (Itagüí)", "display_name": "Centro de la Moda - Santa María, Itagüí", "lat": 6.1770, "lon": -75.6050, "category": "Comercial"},
]


class DataService:
    def __init__(self):
        self.graph = RoadNetworkGraph()
        self.graph_nodes_raw = {}
        self.graph_edges_raw = []
        self._geocode_cache: Dict[str, List[Dict[str, Any]]] = {}
        self._reverse_cache: Dict[str, Dict[str, Any]] = {}
        self._analytics_cache: Dict[str, Dict[str, Any]] = {}
        self._ensure_database()
        self._load_graph()

    def _ensure_database(self):
        """Regenera la base SQLite desde el CSV limpio si falta o llegó como puntero Git LFS."""
        if db_builder.needs_rebuild():
            db_builder.build()

    def _load_graph(self):
        if not os.path.exists(GRAPH_JSON_PATH):
            return

        with open(GRAPH_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.graph_nodes_raw = data.get("nodes", {})
        self.graph_edges_raw = data.get("edges", [])

        for nid_str, info in self.graph_nodes_raw.items():
            self.graph.add_node(int(nid_str), float(info["lat"]), float(info["lon"]))

        for e in self.graph_edges_raw:
            self.graph.add_edge(
                from_node=int(e["from_node"]),
                to_node=int(e["to_node"]),
                length_meters=float(e["length_m"]),
                risk_score=float(e["risk_score"]),
                name=e.get("name", ""),
                max_speed=float(e.get("max_speed", 50.0)),
            )

        # Construir índice KD-Tree para consultas espaciales en O(log V)
        self.graph.build_spatial_index()

    def search_places(self, query: str, limit: int = 8) -> List[Dict[str, Any]]:
        """
        Búsqueda de direcciones y lugares tipo Google Maps.
        Combina un catálogo local offline de alta precisión para Medellín con la API Nominatim OSM.
        """
        raw_query = query.strip()
        if not raw_query:
            return []

        cache_key = _normalize_text(raw_query)
        if cache_key in self._geocode_cache:
            return self._geocode_cache[cache_key][:limit]

        results: List[Dict[str, Any]] = []
        seen_coords = set()

        # 1. Búsqueda local en el catálogo de POIs de Medellín
        norm_query = _normalize_text(raw_query)
        tokens = _tokenize_text(raw_query)

        for poi in MEDELLIN_POI_CATALOG:
            norm_name = _normalize_text(poi["name"])
            norm_disp = _normalize_text(poi["display_name"])
            poi_tokens = set(_tokenize_text(f"{poi['name']} {poi['display_name']}"))

            # Coincidencia si la frase está contenida o si todos los tokens del query coinciden
            match = False
            if norm_query in norm_name or norm_query in norm_disp:
                match = True
            elif tokens and all(t in poi_tokens or any(t in pt for pt in poi_tokens) for t in tokens):
                match = True

            if match:
                coord_key = (round(poi["lat"], 4), round(poi["lon"], 4))
                if coord_key not in seen_coords:
                    seen_coords.add(coord_key)
                    results.append({
                        "name": poi["name"],
                        "display_name": poi["display_name"],
                        "lat": poi["lat"],
                        "lon": poi["lon"],
                        "category": poi.get("category", "Lugar de Interés")
                    })
                    if len(results) >= limit:
                        break

        # 2. Búsqueda en los nodos de la red vial si no se ha completado
        if len(results) < limit:
            for nid_str, node in self.graph_nodes_raw.items():
                node_name = node.get("name", "")
                norm_node = _normalize_text(node_name)
                node_tokens = set(_tokenize_text(node_name))
                if norm_query in norm_node or (tokens and all(t in node_tokens or any(t in nt for nt in node_tokens) for t in tokens)):
                    coord_key = (round(node["lat"], 4), round(node["lon"], 4))
                    if coord_key not in seen_coords:
                        seen_coords.add(coord_key)
                        results.append({
                            "name": f"Intersección: {node_name}",
                            "display_name": f"{node_name}, Medellín",
                            "lat": float(node["lat"]),
                            "lon": float(node["lon"]),
                            "category": "Intersección Vial"
                        })
                        if len(results) >= limit:
                            break

        # 3. Consulta a OpenStreetMap Nominatim para direcciones específicas con calles y números
        if len(results) < 4 and len(raw_query) >= 3:
            try:
                # Delimitar al Valle de Aburrá
                area_suffix = "Itagüí, Antioquia, Colombia" if ("itaguei" in norm_query or "itagui" in norm_query) else "Valle de Aburrá, Antioquia, Colombia"
                params = {
                    "q": f"{raw_query}, {area_suffix}",
                    "format": "json",
                    "limit": "4",
                    "viewbox": "-75.68,6.12,-75.48,6.38",
                    "bounded": "1",
                    "addressdetails": "1",
                }
                url = f"https://nominatim.openstreetmap.org/search?{urllib.parse.urlencode(params)}"
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "MovilidadSeguraMedellin/1.0 (academic-project; tdea)"}
                )
                with urllib.request.urlopen(req, timeout=2.2) as response:
                    if response.status == 200:
                        osm_data = json.loads(response.read().decode("utf-8"))
                        for item in osm_data:
                            lat = float(item["lat"])
                            lon = float(item["lon"])
                            coord_key = (round(lat, 4), round(lon, 4))
                            if coord_key not in seen_coords:
                                seen_coords.add(coord_key)
                                short_name = item.get("name") or item.get("display_name", "").split(",")[0]
                                results.append({
                                    "name": short_name,
                                    "display_name": item.get("display_name", raw_query),
                                    "lat": lat,
                                    "lon": lon,
                                    "category": "Dirección OSM"
                                })
                                if len(results) >= limit:
                                    break
            except Exception:
                # Si falla o no hay internet, continuamos transparentemente con los resultados locales
                pass

        # Guardar en caché
        self._geocode_cache[cache_key] = results
        return results[:limit]

    def reverse_geocode(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Geocodificación inversa: Convierte coordenadas en un nombre de calle o referencia urbana.
        """
        cache_key = f"{round(lat, 5)},{round(lon, 5)}"
        if cache_key in self._reverse_cache:
            return self._reverse_cache[cache_key]

        nearest_node_id = self.graph.find_nearest_node(lat, lon)
        nearest_node_name = None
        min_node_dist = float("inf")

        if nearest_node_id and str(nearest_node_id) in self.graph_nodes_raw:
            node_info = self.graph_nodes_raw[str(nearest_node_id)]
            nearest_node_name = node_info.get("name")
            min_node_dist = haversine_distance(lat, lon, node_info["lat"], node_info["lon"])

        # Buscar si coincide muy de cerca con algún POI (< 100m)
        best_poi = None
        best_poi_dist = float("inf")
        for poi in MEDELLIN_POI_CATALOG:
            d = haversine_distance(lat, lon, poi["lat"], poi["lon"])
            if d < best_poi_dist:
                best_poi_dist = d
                best_poi = poi

        display_name = ""
        if best_poi and best_poi_dist < 100.0:
            display_name = f"{best_poi['name']} ({best_poi['display_name']})"
        elif nearest_node_name and min_node_dist < 150.0:
            display_name = f"Cerca de {nearest_node_name}"
        else:
            # Consultar Nominatim reverse si está a mayor distancia
            try:
                params = {"lat": str(lat), "lon": str(lon), "format": "json"}
                url = f"https://nominatim.openstreetmap.org/reverse?{urllib.parse.urlencode(params)}"
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "MovilidadSeguraMedellin/1.0 (academic-project; tdea)"}
                )
                with urllib.request.urlopen(req, timeout=2.0) as resp:
                    if resp.status == 200:
                        osm_data = json.loads(resp.read().decode("utf-8"))
                        display_name = osm_data.get("display_name", "")
            except Exception:
                pass

            if not display_name:
                if nearest_node_name:
                    display_name = f"Cerca de {nearest_node_name}, Medellín"
                else:
                    display_name = f"Ubicación en Medellín [{lat:.5f}, {lon:.5f}]"

        result = {
            "lat": lat,
            "lon": lon,
            "display_name": display_name,
            "nearest_node_id": nearest_node_id,
            "nearest_node_name": nearest_node_name,
        }
        self._reverse_cache[cache_key] = result
        return result

    def get_incidents(
        self,
        anio: Optional[int] = None,
        comuna_codigo: Optional[int] = None,
        gravedad: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> Tuple[int, List[Dict[str, Any]]]:
        if not os.path.exists(DB_PATH):
            return 0, []

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        query = "SELECT * FROM incidents WHERE 1=1"
        params = []

        if anio is not None:
            query += " AND anio = ?"
            params.append(anio)
        if comuna_codigo is not None:
            query += " AND comuna_codigo = ?"
            params.append(comuna_codigo)
        if gravedad:
            query += " AND gravedad = ?"
            params.append(gravedad.upper())

        count_query = f"SELECT COUNT(*) FROM ({query})"
        cur.execute(count_query, params)
        total = cur.fetchone()[0]

        offset = (page - 1) * page_size
        query += f" ORDER BY fecha DESC LIMIT {page_size} OFFSET {offset}"
        cur.execute(query, params)
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()

        return total, rows

    def get_summary_statistics(self) -> Dict[str, Any]:
        if not os.path.exists(DB_PATH):
            return {}

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*), SUM(factor_riesgo) FROM incidents;")
        total, total_risk = cur.fetchone()

        cur.execute("SELECT gravedad, COUNT(*) FROM incidents GROUP BY gravedad;")
        by_gravedad = dict(cur.fetchall())

        cur.execute("SELECT anio, COUNT(*) FROM incidents GROUP BY anio ORDER BY anio;")
        by_anio = dict(cur.fetchall())

        cur.execute("SELECT comuna_nombre, COUNT(*) as c FROM incidents GROUP BY comuna_nombre ORDER BY c DESC LIMIT 10;")
        top_comunas = [{"comuna": r[0], "count": r[1]} for r in cur.fetchall()]

        conn.close()
        return {
            "total_incidents": total,
            "total_risk_score": round(total_risk or 0, 1),
            "by_severity": by_gravedad,
            "by_year": by_anio,
            "top_communes": top_comunas,
        }

    def get_analytics(
        self,
        anio: Optional[int] = None,
        gravedad: Optional[str] = None,
        comuna: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Agregaciones cruzadas para el tablero de analítica. Cada dimensión se calcula
        aplicando los filtros activos, de modo que año, gravedad y comuna se combinan
        con conteos reales (no proporciones estimadas). Resultado cacheado por filtro.
        """
        cache_key = f"{anio}|{(gravedad or '').upper()}|{comuna or ''}"
        if cache_key in self._analytics_cache:
            return self._analytics_cache[cache_key]
        if not os.path.exists(DB_PATH):
            return {}

        clauses: List[str] = []
        params: List[Any] = []
        if anio is not None:
            clauses.append("anio = ?")
            params.append(int(anio))
        if gravedad:
            clauses.append("gravedad = ?")
            params.append(gravedad.upper())
        if comuna:
            clauses.append("comuna_nombre = ?")
            params.append(comuna)
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        def group(column: str, order: str = "1", limit: Optional[int] = None) -> List[Tuple[Any, int]]:
            sql = f"SELECT {column}, COUNT(*) FROM incidents {where} GROUP BY 1 ORDER BY {order}"
            if limit:
                sql += f" LIMIT {int(limit)}"
            return cur.execute(sql, params).fetchall()

        cur.execute(f"SELECT COUNT(*), COALESCE(SUM(factor_riesgo), 0) FROM incidents {where}", params)
        total, total_risk = cur.fetchone()

        by_month = [0] * 12
        for mes, n in group("mes"):
            if mes and 1 <= int(mes) <= 12:
                by_month[int(mes) - 1] = n
        by_hour = [0] * 24
        for h, n in group("hora_num"):
            if h is not None and 0 <= int(h) <= 23:
                by_hour[int(h)] = n
        by_weekday = [0] * 7
        for d, n in group("dia_semana"):
            if d is not None and 0 <= int(d) <= 6:
                by_weekday[int(d)] = n

        top_barrios = [
            {"barrio": b, "comuna": c, "count": n, "fatal": f}
            for b, c, n, f in cur.execute(
                f"""
                SELECT barrio, MAX(comuna_nombre), COUNT(*) AS n,
                       SUM(CASE WHEN gravedad = 'CON MUERTOS' THEN 1 ELSE 0 END)
                FROM incidents {where} {'AND' if where else 'WHERE'} barrio != 'Sin información'
                GROUP BY barrio ORDER BY n DESC LIMIT 12
                """,
                params,
            ).fetchall()
        ]
        communes = [
            {"comuna": c, "count": n, "fatal": f, "injured": h}
            for c, n, f, h in cur.execute(
                f"""
                SELECT comuna_nombre, COUNT(*) AS n,
                       SUM(CASE WHEN gravedad = 'CON MUERTOS' THEN 1 ELSE 0 END),
                       SUM(CASE WHEN gravedad = 'CON HERIDOS' THEN 1 ELSE 0 END)
                FROM incidents {where} GROUP BY comuna_nombre ORDER BY n DESC
                """,
                params,
            ).fetchall()
        ]

        result = {
            "filters": {"anio": anio, "gravedad": gravedad, "comuna": comuna},
            "total_incidents": total,
            "total_risk_score": round(total_risk, 1),
            "by_severity": {g: n for g, n in group("gravedad")},
            "by_year": {str(y): n for y, n in group("anio")},
            "by_class": [{"clase": c, "count": n} for c, n in group("clase_accidente", "2 DESC")],
            "by_month": by_month,
            "by_hour": by_hour,
            "by_weekday": by_weekday,
            "communes": communes,
            "top_barrios": top_barrios,
        }
        conn.close()
        self._analytics_cache[cache_key] = result
        return result

    def _fetch_clean_osrm_route(
        self,
        origin: Tuple[float, float],
        dest: Tuple[float, float],
        via: Optional[Tuple[float, float]] = None,
    ) -> Tuple[List[List[float]], float]:
        """
        Obtiene la geometría de calle de alta resolución (metro a metro sobre calzada real)
        utilizando OSRM de forma limpia, sin saturar con waypoints densos que provoquen
        vueltas en U o retornos artificiales en calles de un solo sentido.
        """
        if via:
            pts_str = f"{round(origin[1], 5)},{round(origin[0], 5)};{round(via[1], 5)},{round(via[0], 5)};{round(dest[1], 5)},{round(dest[0], 5)}"
        else:
            pts_str = f"{round(origin[1], 5)},{round(origin[0], 5)};{round(dest[1], 5)},{round(dest[0], 5)}"

        url = f"https://router.project-osrm.org/route/v1/driving/{pts_str}?overview=full&geometries=geojson&continue_straight=true"

        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "AburraSegura-Routing/1.0 (academic; tdea)"}
            )
            with urllib.request.urlopen(req, timeout=2.2) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    routes = data.get("routes", [])
                    if routes:
                        r = routes[0]
                        geojson_coords = r["geometry"]["coordinates"]
                        dist_meters = float(r.get("distance", 0.0))
                        clean_coords = [[round(pt[1], 5), round(pt[0], 5)] for pt in geojson_coords]
                        return clean_coords, dist_meters
        except Exception:
            pass

        # Fallback local limpio si OSRM no responde
        direct_dist = haversine_distance(origin[0], origin[1], dest[0], dest[1])
        if via:
            direct_dist = haversine_distance(origin[0], origin[1], via[0], via[1]) + haversine_distance(via[0], via[1], dest[0], dest[1])
            return [[origin[0], origin[1]], [via[0], via[1]], [dest[0], dest[1]]], direct_dist

        return [[origin[0], origin[1]], [dest[0], dest[1]]], direct_dist

    def calculate_multiobjective_routes(
        self,
        origin_lat: float,
        origin_lon: float,
        dest_lat: float,
        dest_lon: float,
        alpha: float = 0.3,
        beta: float = 0.7,
        origin_name: Optional[str] = None,
        destination_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Calcula la ruta más corta vs la ruta más segura desde un Punto A exacto hasta un Punto B exacto.
        Utiliza Dijkstra en el grafo vial multiobjetivo para determinar el corredor óptimo y genera
        geometría de calzada limpia y precisa sobre las vías reales de Medellín sin bucles ni desvíos erráticos.
        """
        start_node = self.graph.find_nearest_node(origin_lat, origin_lon)
        target_node = self.graph.find_nearest_node(dest_lat, dest_lon)

        if not start_node or not target_node:
            return {"found": False}

        # Si origen y destino mapean al mismo nodo o son idénticos
        if start_node == target_node:
            coords, dist_m = self._fetch_clean_osrm_route((origin_lat, origin_lon), (dest_lat, dest_lon))
            route_detail = {
                "total_distance_meters": round(dist_m, 2),
                "total_risk_score": 0.0,
                "nodes_explored": 1,
                "execution_time_ms": 0.1,
                "coordinates": coords,
            }
            return {
                "found": True,
                "origin": [origin_lat, origin_lon],
                "destination": [dest_lat, dest_lon],
                "origin_name": origin_name or f"[{origin_lat:.5f}, {origin_lon:.5f}]",
                "destination_name": destination_name or f"[{dest_lat:.5f}, {dest_lon:.5f}]",
                "start_node": start_node,
                "target_node": target_node,
                "shortest_route": route_detail,
                "safest_route": route_detail,
                "risk_reduction_percentage": 0.0,
                "safest_is_alternative": False,
                "notice": "Origen y destino están en la misma intersección de la red; hay una sola ruta.",
            }

        # 1. Ruta Más Corta con Dijkstra (Prioriza 100% distancia: alpha=1.0, beta=0.0)
        res_shortest = dijkstra_routing(self.graph, start_node, target_node, alpha_distance=1.0, beta_risk=0.0)

        # 2. Ruta Más Segura con Dijkstra (Ponderada multiobjetivo con alpha y beta)
        res_safest = dijkstra_routing(self.graph, start_node, target_node, alpha_distance=alpha, beta_risk=beta)

        # Si el usuario prioriza seguridad (beta >= 0.5) pero el resultado empata con la ruta corta,
        # verificar si una ponderación con mayor énfasis de seguridad (alpha=0.15, beta=0.85) desbloquea un corredor con menor siniestralidad
        if beta >= 0.5 and res_safest.found and res_safest.total_risk_score >= res_shortest.total_risk_score:
            res_safest_alt = dijkstra_routing(self.graph, start_node, target_node, alpha_distance=0.15, beta_risk=0.85)
            if res_safest_alt.found and res_safest_alt.total_risk_score < res_shortest.total_risk_score:
                res_safest = res_safest_alt

        # 3. Geometría limpia sobre asfalto para Ruta Más Corta (directa punto a punto)
        coords_short, dist_short_osrm = self._fetch_clean_osrm_route(
            (origin_lat, origin_lon),
            (dest_lat, dest_lon)
        )
        if coords_short:
            coords_short[0] = [origin_lat, origin_lon]
            coords_short[-1] = [dest_lat, dest_lon]

        dist_short_final = dist_short_osrm if dist_short_osrm > 0 else res_shortest.total_distance_meters

        shortest_assembled = {
            "total_distance_meters": round(dist_short_final, 2),
            "total_risk_score": res_shortest.total_risk_score,
            "nodes_explored": res_shortest.nodes_explored,
            "execution_time_ms": round(res_shortest.execution_time_ms, 2),
            "coordinates": coords_short,
        }

        # 4. Geometría limpia sobre asfalto para Ruta Más Segura
        # Verificamos si Dijkstra multiobjetivo eligió un corredor alterno de menor riesgo
        via_point_safe = None
        if res_safest.found and len(res_safest.path_nodes) > 2 and res_safest.path_nodes != res_shortest.path_nodes:
            direct_dist = haversine_distance(origin_lat, origin_lon, dest_lat, dest_lon)
            best_detour = 0.0

            # Priorizar nodos únicos del camino seguro que no pertenezcan al camino corto
            unique_safe_nodes = [nid for nid in res_safest.path_nodes[1:-1] if nid not in res_shortest.path_nodes]
            candidates = unique_safe_nodes if unique_safe_nodes else res_safest.path_nodes[1:-1]

            for nid in candidates:
                c = self.graph.nodes[nid]
                d1 = haversine_distance(origin_lat, origin_lon, c[0], c[1])
                d2 = haversine_distance(c[0], c[1], dest_lat, dest_lon)
                detour = (d1 + d2) - direct_dist
                if 200.0 < detour < 3800.0 and detour > best_detour:
                    best_detour = detour
                    via_point_safe = (c[0], c[1])

            if not via_point_safe and unique_safe_nodes:
                mid_nid = unique_safe_nodes[len(unique_safe_nodes) // 2]
                c = self.graph.nodes[mid_nid]
                via_point_safe = (c[0], c[1])

        coords_safe = []
        dist_safe_final = 0.0
        # True solo si se dibuja un corredor distinto al de la ruta corta
        safe_is_alternative = False
        notice = None

        if via_point_safe:
            coords_safe, dist_safe_osrm = self._fetch_clean_osrm_route(
                (origin_lat, origin_lon),
                (dest_lat, dest_lon),
                via=via_point_safe
            )
            # Solo aceptamos el desvío si no excede un factor razonable de distancia
            if dist_safe_osrm > 0 and dist_safe_osrm <= dist_short_final * 1.55:
                dist_safe_final = dist_safe_osrm
                safe_is_alternative = True
            else:
                notice = (
                    "El corredor de menor riesgo implicaba un desvío de más del 55% en distancia; "
                    "se recomienda la ruta más corta."
                )

        if not safe_is_alternative:
            # Sin desvío aceptado, la ruta segura ES la corta: misma geometría y mismo riesgo.
            # Antes se dibujaba la línea corta pero se reportaba el riesgo del corredor descartado.
            coords_safe = coords_short
            dist_safe_final = dist_short_final
            res_safest_risk = res_shortest.total_risk_score
            if notice is None:
                notice = "No hay un corredor alternativo con menor riesgo; la ruta más corta ya es la más segura."
        else:
            res_safest_risk = res_safest.total_risk_score

        if coords_safe:
            coords_safe[0] = [origin_lat, origin_lon]
            coords_safe[-1] = [dest_lat, dest_lon]

        safest_assembled = {
            "total_distance_meters": round(dist_safe_final, 2),
            "total_risk_score": res_safest_risk,
            "nodes_explored": res_safest.nodes_explored,
            "execution_time_ms": round(res_safest.execution_time_ms, 2),
            "coordinates": coords_safe if coords_safe else coords_short,
        }

        reduction = 0.0
        if shortest_assembled["total_risk_score"] > 0:
            reduction = round(
                max(
                    0.0,
                    (shortest_assembled["total_risk_score"] - safest_assembled["total_risk_score"])
                    / shortest_assembled["total_risk_score"]
                    * 100.0,
                ),
                1,
            )

        return {
            "found": res_shortest.found and res_safest.found,
            "origin": [origin_lat, origin_lon],
            "destination": [dest_lat, dest_lon],
            "origin_name": origin_name or f"[{origin_lat:.5f}, {origin_lon:.5f}]",
            "destination_name": destination_name or f"[{dest_lat:.5f}, {dest_lon:.5f}]",
            "start_node": start_node,
            "target_node": target_node,
            "shortest_route": shortest_assembled,
            "safest_route": safest_assembled,
            "risk_reduction_percentage": reduction,
            "safest_is_alternative": safe_is_alternative,
            "notice": notice,
        }

    def get_heatmap_cells(
        self,
        gravedad: Optional[str] = None,
        anio: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Agrega todos los siniestros georreferenciados en celdas de ~110 m (redondeo a 3 decimales)
        para alimentar la capa de calor del mapa. Cada celda contiene conteos reales:
        [lat, lon, total, con_muertos, con_heridos, idx_barrio, idx_comuna].
        Soporta filtrado por año (2014-2020) o consulta de todo el histórico consolidado.
        El resultado se cachea en memoria por combinación (gravedad, anio).
        """
        cache_key = f"{(gravedad or 'ALL').upper()}_{anio or 'ALL'}"
        cache = getattr(self, "_heatmap_cache", None)
        if cache is None:
            cache = {}
            self._heatmap_cache = cache
        if cache_key in cache:
            return cache[cache_key]

        empty = {
            "gravedad": gravedad,
            "anio": anio,
            "cell_size_deg": 0.001,
            "total_incidents": 0,
            "year_min": None,
            "year_max": None,
            "available_years": [2014, 2015, 2016, 2017, 2018, 2019, 2020],
            "barrios": [],
            "comunas": [],
            "cells": []
        }
        if not os.path.exists(DB_PATH):
            return empty

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        where = "WHERE latitud IS NOT NULL AND longitud IS NOT NULL"
        params: List[Any] = []
        if gravedad:
            where += " AND gravedad = ?"
            params.append(gravedad.upper())
        if anio is not None:
            where += " AND anio = ?"
            params.append(int(anio))

        having = "HAVING (COUNT(*) >= 2 OR f > 0 OR h > 0)" if anio is None else "HAVING (COUNT(*) >= 1)"

        cur.execute(
            f"""
            SELECT AVG(latitud) AS la, AVG(longitud) AS lo, COUNT(*) AS n,
                   SUM(CASE WHEN gravedad = 'CON MUERTOS' THEN 1 ELSE 0 END) AS f,
                   SUM(CASE WHEN gravedad = 'CON HERIDOS' THEN 1 ELSE 0 END) AS h,
                   MAX(COALESCE(barrio, '')) AS b, MAX(COALESCE(comuna_nombre, '')) AS c
            FROM incidents {where}
            GROUP BY ROUND(latitud, 3), ROUND(longitud, 3)
            {having}
            """,
            params,
        )
        rows = cur.fetchall()
        cur.execute(f"SELECT MIN(anio), MAX(anio) FROM incidents {where}", params)
        year_min, year_max = cur.fetchone()
        conn.close()

        barrios: List[str] = []
        comunas: List[str] = []
        b_idx: Dict[str, int] = {}
        c_idx: Dict[str, int] = {}
        cells: List[List[Any]] = []
        total_cells_incidents = 0
        for la, lo, n, f, h, b, c in rows:
            if la is None or lo is None:
                continue
            b = (b or "").strip().title()
            c = (c or "").strip().title()
            if b not in b_idx:
                b_idx[b] = len(barrios)
                barrios.append(b)
            if c not in c_idx:
                c_idx[c] = len(comunas)
                comunas.append(c)
            cells.append([round(float(la), 5), round(float(lo), 5), int(n), int(f or 0), int(h or 0), b_idx[b], c_idx[c]])
            total_cells_incidents += int(n)

        total = total_cells_incidents

        result = {
            "gravedad": gravedad,
            "anio": anio,
            "cell_size_deg": 0.001,
            "total_incidents": int(total or 0),
            "year_min": year_min,
            "year_max": year_max,
            "available_years": [2014, 2015, 2016, 2017, 2018, 2019, 2020],
            "barrios": barrios,
            "comunas": comunas,
            "cells": cells,
        }
        cache[cache_key] = result
        return result

    def get_hotspots(self, limit: int = 30, gravedad: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retorna las principales zonas críticas de accidentalidad en Medellín
        agrupadas por cuadrantes espaciales de ~110m con mayor densidad y riesgo histórico.
        """
        if not os.path.exists(DB_PATH):
            return []

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        query = """
            SELECT 
                ROUND(latitud, 3) as lat_cluster,
                ROUND(longitud, 3) as lon_cluster,
                COALESCE(barrio, 'Medellín') as barrio_cluster,
                COALESCE(comuna_nombre, 'Comuna') as comuna_cluster,
                COALESCE(diseno, 'Vía Principal') as diseno_cluster,
                COUNT(*) as incident_count,
                SUM(CASE WHEN gravedad = 'CON MUERTOS' THEN 1 ELSE 0 END) as fatal_count,
                SUM(CASE WHEN gravedad = 'CON HERIDOS' THEN 1 ELSE 0 END) as injured_count,
                ROUND(SUM(factor_riesgo), 2) as total_risk_score
            FROM incidents
            WHERE latitud IS NOT NULL AND longitud IS NOT NULL
        """
        params: List[Any] = []
        if gravedad:
            query += " AND gravedad = ?"
            params.append(gravedad.upper())

        query += """
            GROUP BY lat_cluster, lon_cluster
            HAVING incident_count >= 10
            ORDER BY incident_count DESC, total_risk_score DESC
            LIMIT ?
        """
        params.append(limit)

        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()

        hotspots = []
        for r in rows:
            lugar_desc = f"{r['diseno_cluster']} en {r['barrio_cluster']}"
            hotspots.append({
                "lugar": lugar_desc,
                "barrio": r["barrio_cluster"],
                "comuna_nombre": r["comuna_cluster"],
                "latitud": float(r["lat_cluster"]),
                "longitud": float(r["lon_cluster"]),
                "incident_count": int(r["incident_count"]),
                "fatal_count": int(r["fatal_count"]),
                "injured_count": int(r["injured_count"]),
                "total_risk_score": float(r["total_risk_score"]),
            })

        return hotspots

    def get_cached_benchmark_data(self, size: int) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Devuelve (records_list, dict_by_radicado, sorted_records_by_date)
        para el tamaño solicitado, leyendo de SQLite con caché en memoria.
        """
        if not hasattr(self, "_benchmarks_data_cache") or self._benchmarks_data_cache.get("size") != size:
            if not os.path.exists(DB_PATH):
                return [], {}, []

            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                "SELECT radicado, fecha, anio, gravedad, factor_riesgo, comuna_nombre, barrio, latitud, longitud FROM incidents LIMIT ?",
                (size,)
            )
            raw_rows = [dict(r) for r in cur.fetchall()]
            conn.close()

            # Diccionario indexado por radicado para O(1)
            dict_radicado = {r["radicado"]: r for r in raw_rows}

            # Lista ordenada por fecha para O(log n)
            sorted_by_date = sorted(raw_rows, key=lambda x: str(x.get("fecha", "")))

            self._benchmarks_data_cache = {
                "size": size,
                "records": raw_rows,
                "dict": dict_radicado,
                "sorted": sorted_by_date
            }

        cached = self._benchmarks_data_cache
        return cached["records"], cached["dict"], cached["sorted"]


# Instancia singleton del servicio de datos
data_service = DataService()

