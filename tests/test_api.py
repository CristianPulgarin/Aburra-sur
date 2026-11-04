"""
Pruebas de integración de la API REST FastAPI.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "project" in data
    assert data["status"] == "online"


def test_incidents_list():
    response = client.get("/api/v1/incidents?page=1&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data
    assert len(data["items"]) <= 5


def test_benchmark_sort_endpoint():
    payload = {
        "algorithm": "merge_sort",
        "size": 1000,
        "distribution": "random"
    }
    response = client.post("/api/v1/benchmarks/sort", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["algorithm"] == "merge_sort"
    assert data["size"] == 1000
    assert data["time_ms"] >= 0.0
    assert data["comparisons"] > 0
    assert "O(n log n)" in data["theoretical_complexity"]


def test_benchmark_spatial_endpoint():
    payload = {
        "size": 500,
        "query_points": 20,
        "k": 3
    }
    response = client.post("/api/v1/benchmarks/spatial", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "kdtree_query_time_ms" in data
    assert "linear_query_time_ms" in data
    assert "speedup_factor" in data


def test_routing_endpoint():
    # Coordenadas reales: Laureles a El Poblado
    payload = {
        "origin_lat": 6.2442,
        "origin_lon": -75.5812,
        "destination_lat": 6.2081,
        "destination_lon": -75.5674,
        "alpha_distance": 0.3,
        "beta_risk": 0.7
    }
    response = client.post("/api/v1/routing/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["found"] is True
    assert "shortest_route" in data
    assert "safest_route" in data
    assert data["shortest_route"]["total_distance_meters"] > 0
    assert len(data["shortest_route"]["coordinates"]) > 0


def test_geocode_endpoint():
    response = client.get("/api/v1/routing/geocode?q=TdeA")
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "TdeA"
    assert len(data["results"]) > 0
    first = data["results"][0]
    assert "lat" in first
    assert "lon" in first
    assert "Tecnológico de Antioquia" in first["display_name"] or "TdeA" in first["name"]


def test_reverse_geocode_endpoint():
    response = client.get("/api/v1/routing/reverse-geocode?lat=6.2518&lon=-75.5636")
    assert response.status_code == 200
    data = response.json()
    assert "display_name" in data
    assert "nearest_node_id" in data
    assert len(data["display_name"]) > 0


def test_routing_with_exact_points_endpoint():
    # Enrutamiento desde el TdeA (Robledo) hasta el Parque Lleras (El Poblado)
    payload = {
        "origin_lat": 6.2804,
        "origin_lon": -75.5912,
        "destination_lat": 6.2089,
        "destination_lon": -75.5677,
        "origin_name": "Tecnológico de Antioquia",
        "destination_name": "Parque Lleras",
        "alpha_distance": 0.3,
        "beta_risk": 0.7
    }
    response = client.post("/api/v1/routing/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["found"] is True
    assert data["origin_name"] == "Tecnológico de Antioquia"
    assert data["destination_name"] == "Parque Lleras"

    coords_short = data["shortest_route"]["coordinates"]
    # El primer punto de la polilínea debe ser exactamente el Punto A
    assert abs(coords_short[0][0] - 6.2804) < 1e-4
    assert abs(coords_short[0][1] - (-75.5912)) < 1e-4

    # El último punto de la polilínea debe ser exactamente el Punto B
    assert abs(coords_short[-1][0] - 6.2089) < 1e-4
    assert abs(coords_short[-1][1] - (-75.5677)) < 1e-4


def test_get_fase4_results_endpoint():
    response = client.get("/api/v1/benchmarks/fase4-results")
    assert response.status_code == 200
    data = response.json()
    assert "metadata" in data
    assert "sorting" in data
    assert "spatial" in data
    assert "clustering" in data
    assert "routing" in data
    assert "quick_sort" in data["sorting"]
    assert len(data["spatial"]["kdtree_vs_linear"]) >= 5
    assert len(data["routing"]["routing_pairs"]) == 10


def test_hotspots_endpoint():
    response = client.get("/api/v1/incidents/hotspots?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "total_hotspots" in data
    assert "items" in data
    assert len(data["items"]) == 10
    first = data["items"][0]
    assert "lugar" in first
    assert "latitud" in first
    assert "longitud" in first
    assert first["incident_count"] >= 10
    assert first["total_risk_score"] > 0


def test_complexity_benchmark_endpoint_all():
    payload = {
        "complexity_class": "all",
        "size": 500
    }
    response = client.post("/api/v1/benchmarks/complexity", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["size"] == 500
    assert len(data["results"]) == 5
    classes = [r["complexity_class"] for r in data["results"]]
    assert "O(1)" in classes
    assert "O(log n)" in classes
    assert "O(n)" in classes
    assert "O(n log n)" in classes
    assert "O(n^2)" in classes
    assert data["total_execution_time_ms"] > 0


def test_complexity_benchmark_endpoint_single():
    payload = {
        "complexity_class": "ologn",
        "size": 1000
    }
    response = client.post("/api/v1/benchmarks/complexity", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 1
    assert data["results"][0]["complexity_class"] == "O(log n)"
    assert data["results"][0]["time_ns"] > 0





def test_heatmap_endpoint():
    response = client.get("/api/v1/incidents/heatmap")
    assert response.status_code == 200
    data = response.json()
    assert "cells" in data and "barrios" in data and "comunas" in data
    if data["cells"]:
        cell = data["cells"][0]
        assert len(cell) == 7
        assert cell[2] >= 1
        # La suma de celdas debe coincidir con el total real de siniestros agregados
        assert sum(c[2] for c in data["cells"]) == data["total_incidents"]


def test_heatmap_endpoint_fatal_filter():
    response = client.get("/api/v1/incidents/heatmap?gravedad=CON%20MUERTOS")
    assert response.status_code == 200
    data = response.json()
    for cell in data["cells"][:50]:
        assert cell[3] == cell[2]


def test_heatmap_endpoint_year_filter():
    response = client.get("/api/v1/incidents/heatmap?anio=2019")
    assert response.status_code == 200
    data = response.json()
    assert data["anio"] == 2019
    assert data["total_incidents"] == 42471
    assert len(data["cells"]) > 0
    assert "available_years" in data
    assert 2019 in data["available_years"]
