"""
Módulo de Teoría de Grafos y Enrutamiento Multiobjetivo.
Implementa Dijkstra y A* desde cero para redes viales urbanas ponderadas por distancia y riesgo de accidentalidad.
"""

from typing import Dict, List, Optional, Tuple, Any
import math
import heapq
from app.algorithms.spatial_kdtree import KDTree2D, haversine_distance


class RoadEdge:
    def __init__(self, from_node: int, to_node: int, length_meters: float, risk_score: float = 0.0, name: str = "", max_speed: float = 50.0):
        self.from_node = from_node
        self.to_node = to_node
        self.length_meters = max(1.0, length_meters)
        self.risk_score = max(0.0, risk_score)
        self.name = name
        self.max_speed = max_speed

    def weight(self, alpha_distance: float = 0.5, beta_risk: float = 0.5, max_length: float = 1000.0, max_risk: float = 100.0) -> float:
        """
        Calcula el coste multiobjetivo ponderado normalizado.
        alpha + beta = 1.0
        """
        norm_dist = self.length_meters / max(1.0, max_length)
        norm_risk = self.risk_score / max(1.0, max_risk)
        return alpha_distance * norm_dist + beta_risk * norm_risk


class RoadNetworkGraph:
    def __init__(self):
        # nodes: id -> (lat, lon)
        self.nodes: Dict[int, Tuple[float, float]] = {}
        # adj: u -> list of RoadEdge
        self.adj: Dict[int, List[RoadEdge]] = {}
        self.max_edge_length = 1.0
        self.max_edge_risk = 1.0
        self.kdtree: Optional[KDTree2D] = None

    def add_node(self, node_id: int, lat: float, lon: float):
        self.nodes[node_id] = (lat, lon)
        if node_id not in self.adj:
            self.adj[node_id] = []
        # Invalidate index when nodes are added
        self.kdtree = None

    def build_spatial_index(self):
        """Construye el índice KD-Tree espacial 2D sobre los nodos de la red vial para consultas en O(log V)."""
        pts = [((coords[0], coords[1]), nid) for nid, coords in self.nodes.items()]
        self.kdtree = KDTree2D(pts)

    def add_edge(self, from_node: int, to_node: int, length_meters: float, risk_score: float = 0.0, name: str = "", max_speed: float = 50.0):
        if from_node not in self.nodes or to_node not in self.nodes:
            return

        edge = RoadEdge(from_node, to_node, length_meters, risk_score, name, max_speed)
        self.adj[from_node].append(edge)

        if length_meters > self.max_edge_length:
            self.max_edge_length = length_meters
        if risk_score > self.max_edge_risk:
            self.max_edge_risk = risk_score

    def find_nearest_node(self, lat: float, lon: float) -> Optional[int]:
        """
        Encuentra el nodo del grafo más cercano a las coordenadas dadas.
        Utiliza KD-Tree O(log V) si está indexado; de lo contrario, búsqueda exhaustiva O(V).
        """
        if self.kdtree and self.kdtree.root:
            res = self.kdtree.nearest_neighbor((lat, lon))
            if res and res[1] is not None:
                return res[1]

        best_node = None
        best_dist = float('inf')
        for node_id, coords in self.nodes.items():
            d = haversine_distance(lat, lon, coords[0], coords[1])
            if d < best_dist:
                best_dist = d
                best_node = node_id
        return best_node



class RoutingResult:
    def __init__(self):
        self.found = False
        self.path_nodes: List[int] = []
        self.path_coordinates: List[Tuple[float, float]] = []
        self.total_distance_meters: float = 0.0
        self.total_risk_score: float = 0.0
        self.nodes_explored: int = 0
        self.execution_time_ms: float = 0.0


def dijkstra_routing(
    graph: RoadNetworkGraph,
    start_node: int,
    target_node: int,
    alpha_distance: float = 0.5,
    beta_risk: float = 0.5
) -> RoutingResult:
    """
    Algoritmo de Dijkstra con Min-Heap para caminos mínimos en grafos dirigidos.
    Complejidad: O((V + E) log V) tiempo, O(V + E) espacio.
    """
    import time
    start_t = time.perf_counter()

    result = RoutingResult()
    if start_node not in graph.nodes or target_node not in graph.nodes:
        return result

    if start_node == target_node:
        result.found = True
        result.path_nodes = [start_node]
        result.path_coordinates = [graph.nodes[start_node]]
        result.execution_time_ms = (time.perf_counter() - start_t) * 1000.0
        return result

    distances: Dict[int, float] = {node: float('inf') for node in graph.nodes}
    distances[start_node] = 0.0
    previous: Dict[int, Tuple[int, RoadEdge]] = {}

    # pq: tuplas (costo_acumulado, contador, node_id)
    pq: List[Tuple[float, int, int]] = []
    counter = 0
    heapq.heappush(pq, (0.0, counter, start_node))

    visited = set()

    while pq:
        current_cost, _, u = heapq.heappop(pq)
        result.nodes_explored += 1

        if u in visited:
            continue
        visited.add(u)

        if u == target_node:
            result.found = True
            break

        for edge in graph.adj.get(u, []):
            v = edge.to_node
            if v in visited:
                continue

            w = edge.weight(alpha_distance, beta_risk, graph.max_edge_length, graph.max_edge_risk)
            new_cost = current_cost + w

            if new_cost < distances[v]:
                distances[v] = new_cost
                previous[v] = (u, edge)
                counter += 1
                heapq.heappush(pq, (new_cost, counter, v))

    if result.found:
        curr = target_node
        path = [curr]
        tot_dist = 0.0
        tot_risk = 0.0

        while curr in previous:
            prev_node, edge = previous[curr]
            tot_dist += edge.length_meters
            tot_risk += edge.risk_score
            path.append(prev_node)
            curr = prev_node

        path.reverse()
        result.path_nodes = path
        result.path_coordinates = [graph.nodes[nid] for nid in path]
        result.total_distance_meters = round(tot_dist, 2)
        result.total_risk_score = round(tot_risk, 2)

    result.execution_time_ms = (time.perf_counter() - start_t) * 1000.0
    return result


def a_star_routing(
    graph: RoadNetworkGraph,
    start_node: int,
    target_node: int,
    alpha_distance: float = 0.5,
    beta_risk: float = 0.5
) -> RoutingResult:
    """
    Algoritmo A* (A-Star) con heurística Haversine geodésica.
    Heurística h(u): Distancia en línea recta normalizada ponderada por alpha.
    Garantiza optimización al ser admisible y consistente, con podas que reducen nodes_explored.
    """
    import time
    start_t = time.perf_counter()

    result = RoutingResult()
    if start_node not in graph.nodes or target_node not in graph.nodes:
        return result

    if start_node == target_node:
        result.found = True
        result.path_nodes = [start_node]
        result.path_coordinates = [graph.nodes[start_node]]
        result.execution_time_ms = (time.perf_counter() - start_t) * 1000.0
        return result

    target_coords = graph.nodes[target_node]

    def heuristic(node_id: int) -> float:
        c = graph.nodes[node_id]
        h_meters = haversine_distance(c[0], c[1], target_coords[0], target_coords[1])
        # Normalizar con el mismo factor max_edge_length y ponderar por alpha
        return (alpha_distance * h_meters) / max(1.0, graph.max_edge_length)

    g_score: Dict[int, float] = {node: float('inf') for node in graph.nodes}
    g_score[start_node] = 0.0

    previous: Dict[int, Tuple[int, RoadEdge]] = {}

    pq: List[Tuple[float, int, int]] = []
    counter = 0
    f_start = heuristic(start_node)
    heapq.heappush(pq, (f_start, counter, start_node))

    visited = set()

    while pq:
        f_val, _, u = heapq.heappop(pq)
        result.nodes_explored += 1

        if u in visited:
            continue
        visited.add(u)

        if u == target_node:
            result.found = True
            break

        current_g = g_score[u]

        for edge in graph.adj.get(u, []):
            v = edge.to_node
            if v in visited:
                continue

            w = edge.weight(alpha_distance, beta_risk, graph.max_edge_length, graph.max_edge_risk)
            tentative_g = current_g + w

            if tentative_g < g_score[v]:
                g_score[v] = tentative_g
                previous[v] = (u, edge)
                f_score = tentative_g + heuristic(v)
                counter += 1
                heapq.heappush(pq, (f_score, counter, v))

    if result.found:
        curr = target_node
        path = [curr]
        tot_dist = 0.0
        tot_risk = 0.0

        while curr in previous:
            prev_node, edge = previous[curr]
            tot_dist += edge.length_meters
            tot_risk += edge.risk_score
            path.append(prev_node)
            curr = prev_node

        path.reverse()
        result.path_nodes = path
        result.path_coordinates = [graph.nodes[nid] for nid in path]
        result.total_distance_meters = round(tot_dist, 2)
        result.total_risk_score = round(tot_risk, 2)

    result.execution_time_ms = (time.perf_counter() - start_t) * 1000.0
    return result
