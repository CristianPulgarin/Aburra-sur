"""
Pruebas unitarias y de casos borde para KD-Tree 2D y búsqueda exhaustiva.
"""

import pytest
import random
from app.algorithms.spatial_kdtree import KDTree2D, linear_search_nearest, haversine_distance


def test_kdtree_empty():
    tree = KDTree2D([])
    pt, data, dist, visited = tree.nearest_neighbor((6.25, -75.56))
    assert pt is None
    assert dist == float('inf')
    assert visited == 0


def test_kdtree_correctness_against_linear():
    # Coordenadas representativas de comunas de Medellín
    points = [
        ((6.2442, -75.5812), "Laureles"),
        ((6.2518, -75.5636), "La Candelaria"),
        ((6.2081, -75.5674), "El Poblado"),
        ((6.3012, -75.5741), "Castilla"),
        ((6.2731, -75.5520), "Aranjuez"),
        ((6.2625, -75.5901), "Robledo"),
        ((6.2301, -75.6052), "Belen"),
    ]

    tree = KDTree2D(points)
    query = (6.2500, -75.5650)  # Cerca de La Candelaria

    # Consulta con KD-Tree
    kd_pt, kd_data, kd_dist, kd_visited = tree.nearest_neighbor(query)

    # Consulta con búsqueda lineal
    lin_pt, lin_data, lin_dist, lin_visited = linear_search_nearest(points, query)

    assert kd_data == lin_data
    assert abs(kd_dist - lin_dist) < 1e-4
    assert kd_data == "La Candelaria"


def test_kdtree_k_nearest():
    points = [((float(i), float(i)), f"id_{i}") for i in range(20)]
    tree = KDTree2D(points)

    k_results = tree.k_nearest_neighbors((5.2, 5.2), k=3)
    assert len(k_results) == 3
    # Los más cercanos a (5.2, 5.2) deben ser 5, luego 6, luego 4
    labels = [res[1] for res in k_results]
    assert "id_5" in labels
