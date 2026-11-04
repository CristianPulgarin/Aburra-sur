"""
Pruebas unitarias para Dijkstra y A* multiobjetivo.
"""

import pytest
from app.algorithms.graph_routing import RoadNetworkGraph, dijkstra_routing, a_star_routing


def test_dijkstra_and_astar_simple():
    # Creamos un grafo simple con dos rutas:
    # Ruta 1: Directa pero peligrosa (1000m, riesgo 100)
    # Ruta 2: Indirecta pero segura (1200m, riesgo 5)
    g = RoadNetworkGraph()
    g.add_node(1, 6.20, -75.57)
    g.add_node(2, 6.21, -75.57)
    g.add_node(3, 6.205, -75.565)

    # Ruta 1: 1 -> 2
    g.add_edge(1, 2, length_meters=1000.0, risk_score=100.0, name="Autopista Peligrosa")

    # Ruta 2: 1 -> 3 -> 2
    g.add_edge(1, 3, length_meters=600.0, risk_score=2.0, name="Via Barrial 1")
    g.add_edge(3, 2, length_meters=600.0, risk_score=3.0, name="Via Barrial 2")

    # 1. Modo Ruta Más Corta: alpha=1.0, beta=0.0
    res_short = dijkstra_routing(g, start_node=1, target_node=2, alpha_distance=1.0, beta_risk=0.0)
    assert res_short.found
    assert res_short.path_nodes == [1, 2]
    assert res_short.total_distance_meters == 1000.0
    assert res_short.total_risk_score == 100.0

    # 2. Modo Ruta Más Segura: alpha=0.1, beta=0.9
    res_safe = dijkstra_routing(g, start_node=1, target_node=2, alpha_distance=0.1, beta_risk=0.9)
    assert res_safe.found
    assert res_safe.path_nodes == [1, 3, 2]
    assert res_safe.total_distance_meters == 1200.0
    assert res_safe.total_risk_score == 5.0

    # 3. Comparación con A*: Ambos deben encontrar el mismo camino óptimo
    astar_safe = a_star_routing(g, start_node=1, target_node=2, alpha_distance=0.1, beta_risk=0.9)
    assert astar_safe.found
    assert astar_safe.path_nodes == res_safe.path_nodes


def test_routing_disconnected():
    g = RoadNetworkGraph()
    g.add_node(1, 6.20, -75.57)
    g.add_node(2, 6.25, -75.55)
    # Sin aristas

    res = dijkstra_routing(g, start_node=1, target_node=2)
    assert not res.found
    assert res.path_nodes == []
