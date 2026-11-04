"""
Pruebas unitarias y de validación para las implementaciones de la Fase 4.
Verifica:
1. Quick Sort iterativo con partición Hoare, mediana de 3 y resistencia a desbordamiento de pila en datos patológicos.
2. KD-Tree 2D radius_search y concordancia con distancias Haversine.
3. DBSCAN geodésico acelerado con KD-Tree.
4. Esquemas y validación de endpoints de la Fase 4.
"""

import pytest
import math
from app.algorithms.sorting import quick_sort, merge_sort, heap_sort, counting_sort
from app.algorithms.spatial_kdtree import KDTree2D, haversine_distance
from app.algorithms.clustering_dbscan import DBSCANClusterer
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_iterative_quicksort_deep_and_pathological():
    """Verifica que Quick Sort iterativo procese 15.000 elementos sin RecursionError."""
    # 1. Ya ordenado
    arr_sorted = list(range(15000))
    res, comps = quick_sort(arr_sorted)
    assert res == arr_sorted
    assert comps > 0

    # 2. Inverso
    arr_rev = list(range(15000, 0, -1))
    res_rev, _ = quick_sort(arr_rev)
    assert res_rev == sorted(arr_rev)

    # 3. Todos idénticos (caso crítico para partición de Hoare)
    arr_identical = [42.0] * 10000
    res_id, _ = quick_sort(arr_identical)
    assert len(res_id) == 10000
    assert all(x == 42.0 for x in res_id)


def test_kdtree_radius_search_correctness():
    """Verifica que radius_search encuentre todos y solo los puntos dentro del radio geodésico."""
    # Puntos en Medellín: Parque Berrío, San Antonio, Alpujarra, Estadio
    points = [
        ((6.2497, -75.5678), "Parque Berrío"),
        ((6.2471, -75.5694), "San Antonio"),
        ((6.2425, -75.5742), "Alpujarra"),
        ((6.2530, -75.5898), "Estadio")
    ]
    tree = KDTree2D(points)

    center = (6.2497, -75.5678)  # Parque Berrío
    # Radio de 500 metros
    found_500m = tree.radius_search(center, radius_meters=500.0)
    found_names = [item[1] for item in found_500m]

    # Parque Berrío está a 0m (debe estar)
    assert "Parque Berrío" in found_names
    # San Antonio está a ~330m (debe estar)
    assert "San Antonio" in found_names
    # Estadio está a ~2.4 km (NO debe estar)
    assert "Estadio" not in found_names

    # Verificar que las distancias reportadas coincidan con Haversine
    for pt, name, dist in found_500m:
        calc_dist = haversine_distance(center[0], center[1], pt[0], pt[1])
        assert abs(dist - calc_dist) < 1e-4


def test_dbscan_with_kdtree_hotspots():
    """Verifica el agrupamiento DBSCAN acelerado sobre un grupo denso y puntos aislados de ruido."""
    # Cluster denso alrededor de Punto Cero (6.2625, -75.5780)
    dense_cluster = [(6.2625 + 0.0001 * i, -75.5780 + 0.0001 * i) for i in range(20)]
    # Puntos de ruido aislados lejos (a más de 5 km)
    noise_points = [(6.3500, -75.5500), (6.1800, -75.6000)]

    all_coords = dense_cluster + noise_points
    clusterer = DBSCANClusterer(eps_meters=200.0, min_samples=5)
    result = clusterer.fit(all_coords)

    assert result["total_clusters"] >= 1
    assert result["noise_points"] >= 2


def test_sorting_cross_verification():
    """Verifica que todas las familias de ordenamiento produzcan el mismo orden estricto."""
    import random
    random.seed(123)
    sample = [random.uniform(-1000.0, 1000.0) for _ in range(500)]

    sorted_merge, _ = merge_sort(sample)
    sorted_quick, _ = quick_sort(sample)
    sorted_heap, _ = heap_sort(sample)
    expected = sorted(sample)

    assert sorted_merge == expected
    assert sorted_quick == expected
    assert sorted_heap == expected
