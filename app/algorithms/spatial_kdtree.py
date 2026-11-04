"""
Módulo de Estructura de Datos Espacial: KD-Tree 2D (2-Dimensional Tree).
Optimizado para consultas de rango y vecinos más cercanos (k-NN) con distancia geodésica Haversine.
Comparado formalmente contra Búsqueda Lineal Exhaustiva O(n).
"""

from typing import Any, List, Optional, Tuple
import math
import heapq


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula la distancia geodésica de círculo máximo entre dos coordenadas en metros.
    """
    R = 6371000.0  # Radio medio de la Tierra en metros
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0) ** 2))
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c


class KDNode:
    def __init__(self, point: Tuple[float, float], data: Any = None, axis: int = 0):
        # point: (lat, lon)
        self.point = point
        self.data = data
        self.axis = axis
        self.left: Optional['KDNode'] = None
        self.right: Optional['KDNode'] = None


class KDTree2D:
    def __init__(self, points_with_data: Optional[List[Tuple[Tuple[float, float], Any]]] = None):
        """
        Construye el KD-Tree 2D.
        points_with_data: Lista de tuplas ((lat, lon), metadata).
        Complejidad de Construcción: O(n log n) tiempo, O(n) espacio.
        """
        self.nodes_visited_last_query = 0
        self.size = 0
        if points_with_data:
            self.root = self._build(points_with_data, depth=0)
            self.size = len(points_with_data)
        else:
            self.root = None

    def _build(self, points: List[Tuple[Tuple[float, float], Any]], depth: int) -> Optional[KDNode]:
        if not points:
            return None

        axis = depth % 2  # 0: latitud, 1: longitud

        # Ordenar por el eje actual para encontrar la mediana exacta
        points.sort(key=lambda p: p[0][axis])
        mid = len(points) // 2

        node = KDNode(point=points[mid][0], data=points[mid][1], axis=axis)
        node.left = self._build(points[:mid], depth + 1)
        node.right = self._build(points[mid + 1:], depth + 1)
        return node

    def nearest_neighbor(self, target: Tuple[float, float]) -> Tuple[Optional[Tuple[float, float]], Any, float, int]:
        """
        Encuentra el vecino más cercano (1-NN) al punto objetivo.
        Retorna: (coordenadas, data, distancia_en_metros, nodos_visitados).
        Complejidad: O(log n) caso promedio, O(n) peor caso.
        """
        self.nodes_visited_last_query = 0
        if not self.root:
            return None, None, float('inf'), 0

        best_node = self.root
        best_dist = haversine_distance(target[0], target[1], self.root.point[0], self.root.point[1])

        def _search(node: Optional[KDNode]):
            nonlocal best_node, best_dist
            if not node:
                return

            self.nodes_visited_last_query += 1

            d = haversine_distance(target[0], target[1], node.point[0], node.point[1])
            if d < best_dist:
                best_dist = d
                best_node = node

            axis = node.axis
            # Diferencia en el eje de corte (en grados convertidos a distancia aproximada en metros)
            # 1 grado latitud ≈ 111.139 metros
            axis_diff_deg = target[axis] - node.point[axis]
            axis_diff_meters = abs(axis_diff_deg * 111139.0)

            # Recorrer primero la rama más prometedora
            first, second = (node.left, node.right) if axis_diff_deg < 0 else (node.right, node.left)
            _search(first)

            # Podar la segunda rama si la distancia en el hiperplano es mayor que la mejor distancia encontrada
            if axis_diff_meters < best_dist:
                _search(second)

        _search(self.root)
        return best_node.point, best_node.data, best_dist, self.nodes_visited_last_query

    def k_nearest_neighbors(self, target: Tuple[float, float], k: int = 5) -> List[Tuple[Tuple[float, float], Any, float]]:
        """
        Encuentra los k vecinos más cercanos utilizando un Max-Heap acotado de tamaño k.
        Retorna: Lista ordenada de (punto, data, distancia).
        """
        if not self.root or k <= 0:
            return []

        # Usamos max-heap de tuplas (-distancia, contador, node)
        heap: List[Tuple[float, int, KDNode]] = []
        counter = 0

        def _search(node: Optional[KDNode]):
            nonlocal counter
            if not node:
                return

            d = haversine_distance(target[0], target[1], node.point[0], node.point[1])
            counter += 1

            if len(heap) < k:
                heapq.heappush(heap, (-d, counter, node))
            else:
                if d < -heap[0][0]:
                    heapq.heapreplace(heap, (-d, counter, node))

            axis = node.axis
            axis_diff_deg = target[axis] - node.point[axis]
            axis_diff_meters = abs(axis_diff_deg * 111139.0)

            first, second = (node.left, node.right) if axis_diff_deg < 0 else (node.right, node.left)
            _search(first)

            max_dist_in_heap = -heap[0][0] if heap else float('inf')
            if len(heap) < k or axis_diff_meters < max_dist_in_heap:
                _search(second)

        _search(self.root)

        results = []
        for neg_dist, _, node in heap:
            results.append((node.point, node.data, -neg_dist))
        results.sort(key=lambda x: x[2])
        return results

    def radius_search(self, target: Tuple[float, float], radius_meters: float) -> List[Tuple[Tuple[float, float], Any, float]]:
        """
        Retorna todos los puntos dentro de radius_meters alrededor de target (lat, lon).
        Complejidad: O(log n + k) promedio, donde k es el número de puntos dentro del radio.
        """
        if not self.root or radius_meters < 0:
            return []

        results: List[Tuple[Tuple[float, float], Any, float]] = []

        def _search(node: Optional[KDNode]):
            if not node:
                return

            d = haversine_distance(target[0], target[1], node.point[0], node.point[1])
            if d <= radius_meters:
                results.append((node.point, node.data, d))

            axis = node.axis
            axis_diff_deg = target[axis] - node.point[axis]
            # 1 grado de latitud o longitud ≈ 111.139 m * cos(lat)
            scale = 111139.0 if axis == 0 else 111139.0 * math.cos(math.radians(target[0]))
            axis_diff_meters = abs(axis_diff_deg * scale)

            first, second = (node.left, node.right) if axis_diff_deg < 0 else (node.right, node.left)
            _search(first)

            if axis_diff_meters <= radius_meters:
                _search(second)

        _search(self.root)
        return results



def linear_search_nearest(points_with_data: List[Tuple[Tuple[float, float], Any]], target: Tuple[float, float]) -> Tuple[Tuple[float, float], Any, float, int]:
    """
    Búsqueda lineal exhaustiva de complejidad O(n).
    Utilizada para verificar correctitud y demostrar empíricamente el speedup del KD-Tree.
    """
    best_point = None
    best_data = None
    best_dist = float('inf')
    visited = 0

    for pt, data in points_with_data:
        visited += 1
        d = haversine_distance(target[0], target[1], pt[0], pt[1])
        if d < best_dist:
            best_dist = d
            best_point = pt
            best_data = data

    return best_point, best_data, best_dist, visited
