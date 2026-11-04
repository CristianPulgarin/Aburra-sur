"""
Pruebas unitarias para DBSCAN geodésico espacial.
"""

from app.algorithms.clustering_dbscan import DBSCANClusterer


def test_dbscan_empty():
    clusterer = DBSCANClusterer()
    res = clusterer.fit([])
    assert res["total_clusters"] == 0
    assert res["noise_points"] == 0


def test_dbscan_grouping():
    # Grupo 1: 5 puntos muy cercanos en el centro de Medellín (La Candelaria ~ lat 6.251, lon -75.563)
    c1 = [(6.2510 + i * 0.0001, -75.5630 + i * 0.0001) for i in range(12)]
    # Punto aislado (ruido): lejos en San Antonio de Prado
    c_noise = [(6.1900, -75.6400)]

    points = c1 + c_noise
    clusterer = DBSCANClusterer(eps_meters=200.0, min_samples=5)
    res = clusterer.fit(points)

    assert res["total_clusters"] >= 1
    assert res["noise_points"] >= 1
    assert len(res["clusters"]) >= 1
    # El cluster principal debe tener los 12 puntos
    assert res["clusters"][0]["incident_count"] == 12
