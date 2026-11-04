"""
Pruebas de consistencia del riesgo del grafo y de la respuesta de rutas multiobjetivo.
"""

import json

from app.services.data_service import GRAPH_JSON_PATH, data_service


def test_both_directions_share_risk():
    # Antes el sentido opuesto de cada calle quedaba con riesgo 0 (puntos medios duplicados en el KD-Tree)
    with open(GRAPH_JSON_PATH, encoding="utf-8") as f:
        edges = json.load(f)["edges"]
    by_corridor = {}
    for e in edges:
        key = tuple(sorted((e["from_node"], e["to_node"])))
        by_corridor.setdefault(key, set()).add(e["risk_score"])
    assert all(len(risks) == 1 for risks in by_corridor.values())


def _fake_osrm(detour_factor):
    """OSRM simulado: ruta directa en línea recta y desvío `detour_factor` veces más largo."""
    from app.algorithms.spatial_kdtree import haversine_distance

    def fetch(origin, dest, via=None):
        direct = haversine_distance(origin[0], origin[1], dest[0], dest[1])
        if via:
            return [list(origin), list(via), list(dest)], direct * detour_factor
        return [list(origin), list(dest)], direct

    return fetch


def _route_with_detour(monkeypatch, detour_factor):
    monkeypatch.setattr(data_service, "_fetch_clean_osrm_route", _fake_osrm(detour_factor))
    # Autopista Sur con Colombia -> Santa Fe: el corredor seguro difiere del corto
    a = data_service.graph.nodes[8]
    b = data_service.graph.nodes[25]
    return data_service.calculate_multiobjective_routes(a[0], a[1], b[0], b[1], alpha=0.2, beta=0.8)


def test_rejected_detour_reports_shortest_route(monkeypatch):
    res = _route_with_detour(monkeypatch, detour_factor=3.0)
    assert res["safest_is_alternative"] is False
    assert res["safest_route"]["coordinates"] == res["shortest_route"]["coordinates"]
    assert res["safest_route"]["total_risk_score"] == res["shortest_route"]["total_risk_score"]
    assert res["risk_reduction_percentage"] == 0.0
    assert res["notice"]


def test_accepted_detour_reduces_risk(monkeypatch):
    res = _route_with_detour(monkeypatch, detour_factor=1.2)
    assert res["safest_is_alternative"] is True
    assert res["safest_route"]["total_risk_score"] < res["shortest_route"]["total_risk_score"]
    assert 0 < res["risk_reduction_percentage"] < 100
