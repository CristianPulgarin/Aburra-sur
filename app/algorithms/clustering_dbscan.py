"""
Módulo de Algoritmos de Agrupamiento Espacial (Clustering).
Implementa DBSCAN geodésico y K-Means desde cero para la detección de puntos negros (hotspots) de accidentalidad.
"""

from typing import Dict, List, Set, Tuple
import math
from app.algorithms.spatial_kdtree import KDTree2D, haversine_distance


class DBSCANClusterer:
    """
    Algoritmo DBSCAN (Density-Based Spatial Clustering of Applications with Noise).
    Complejidad: O(n log n) tiempo al utilizar indexación espacial KD-Tree para consultas de vecindad eps.
    Espacial: O(n).
    """
    def __init__(self, eps_meters: float = 150.0, min_samples: int = 10):
        self.eps_meters = eps_meters
        self.min_samples = min_samples
        self.labels: List[int] = []
        self.clusters: Dict[int, List[int]] = {}

    def fit(self, coords: List[Tuple[float, float]], severity_weights: List[float] = None) -> Dict[str, any]:
        """
        Ejecuta DBSCAN sobre una lista de coordenadas (lat, lon).
        coords: Lista de pares (lat, lon).
        severity_weights: Peso relativo por incidente (opcional, default 1.0).
        Retorna diccionario con estadísticas de clusters y centroides.
        """
        n = len(coords)
        if n == 0:
            return {"total_clusters": 0, "noise_points": 0, "clusters": []}

        if severity_weights is None:
            severity_weights = [1.0] * n

        # Indexar con KD-Tree para acelerar la consulta de vecindad eps
        indexed_points = [((coords[i][0], coords[i][1]), i) for i in range(n)]
        kdtree = KDTree2D(indexed_points)

        # -1 indica ruido (noise), 0 no visitado inicialmente
        labels = [0] * n
        cluster_id = 0

        # Función auxiliar para consultar vecinos dentro de eps_meters usando KD-Tree 2D
        def _get_neighbors(point_idx: int) -> List[int]:
            center = coords[point_idx]
            results = kdtree.radius_search(center, self.eps_meters)
            return [item[1] for item in results]

        for i in range(n):
            if labels[i] != 0:
                continue

            neighbors = _get_neighbors(i)

            if len(neighbors) < self.min_samples:
                labels[i] = -1  # Marcado provisional como ruido
            else:
                cluster_id += 1
                labels[i] = cluster_id
                queue = list(neighbors)
                queue_set = set(neighbors)

                # Expandir cluster
                j = 0
                while j < len(queue):
                    neighbor_idx = queue[j]
                    if labels[neighbor_idx] == -1:
                        labels[neighbor_idx] = cluster_id

                    if labels[neighbor_idx] == 0:
                        labels[neighbor_idx] = cluster_id
                        sub_neighbors = _get_neighbors(neighbor_idx)
                        if len(sub_neighbors) >= self.min_samples:
                            for sn in sub_neighbors:
                                if sn not in queue_set:
                                    queue.append(sn)
                                    queue_set.add(sn)
                    j += 1


        self.labels = labels

        # Calcular métricas por cluster
        clusters_summary = []
        noise_count = 0

        for c_id in range(1, cluster_id + 1):
            members = [i for i, lbl in enumerate(labels) if lbl == c_id]
            if not members:
                continue

            mean_lat = sum(coords[i][0] for i in members) / len(members)
            mean_lon = sum(coords[i][1] for i in members) / len(members)
            total_severity = sum(severity_weights[i] for i in members)

            clusters_summary.append({
                "cluster_id": c_id,
                "centroid": [round(mean_lat, 6), round(mean_lon, 6)],
                "incident_count": len(members),
                "severity_score": round(total_severity, 2)
            })

        noise_count = sum(1 for lbl in labels if lbl == -1)

        # Ordenar clusters de mayor a menor severidad
        clusters_summary.sort(key=lambda x: x["severity_score"], reverse=True)

        return {
            "total_clusters": cluster_id,
            "noise_points": noise_count,
            "clusters": clusters_summary
        }
