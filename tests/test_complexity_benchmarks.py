"""
Pruebas unitarias para el Laboratorio de Jerarquía Asintótica:
O(1) -> O(log n) -> O(n) -> O(n log n) -> O(n^2)
Verifica correctitud matemática, conteo de operaciones y consistencia empírica.
"""

import pytest
import math
from app.algorithms.complexity_benchmarks import (
    benchmark_o1_hash_lookup,
    binary_search_incidents_by_date,
    benchmark_ologn_binary_search,
    benchmark_on_linear_scan,
    merge_sort_incidents,
    benchmark_onlogn_merge_sort,
    benchmark_on2_all_pairs_distance,
    haversine_distance_quick
)


@pytest.fixture
def sample_incidents():
    """Genera una muestra sintética representativa de incidentes viales."""
    return [
        {
            "radicado": f"RAD_{i:04d}",
            "fecha": f"2022-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}",
            "comuna_nombre": "La Candelaria" if i % 2 == 0 else "Poblado",
            "gravedad": "CON MUERTOS" if i % 10 == 0 else "SOLO DAÑOS",
            "factor_riesgo": float(i % 5 + 1),
            "latitud": 6.2442 + (i * 0.0001),
            "longitud": -75.5765 + (i * 0.0001),
        }
        for i in range(100)
    ]


def test_haversine_distance_quick():
    # Coordenadas idénticas deben dar 0 metros
    assert haversine_distance_quick(6.25, -75.56, 6.25, -75.56) == 0.0

    # Distancia aproximada entre dos puntos conocidos de Medellín (~1 km)
    d = haversine_distance_quick(6.2500, -75.5600, 6.2590, -75.5600)
    assert 900 < d < 1100


def test_o1_hash_lookup(sample_incidents):
    dict_data = {r["radicado"]: r for r in sample_incidents}

    # Búsqueda de elemento existente
    res_found = benchmark_o1_hash_lookup(dict_data, target_radicado="RAD_0042", repetitions=10)
    assert res_found["complexity_class"] == "O(1)"
    assert res_found["found"] is True
    assert res_found["sample_result"] == "RAD_0042"
    assert res_found["operations_count"] == 1
    assert res_found["time_ns"] > 0

    # Búsqueda de elemento inexistente
    res_not_found = benchmark_o1_hash_lookup(dict_data, target_radicado="RAD_9999", repetitions=10)
    assert res_not_found["found"] is False


def test_ologn_binary_search(sample_incidents):
    sorted_data = sorted(sample_incidents, key=lambda x: x["fecha"])
    target_dt = sorted_data[25]["fecha"]

    idx, comps = binary_search_incidents_by_date(sorted_data, target_dt)
    assert idx is not None
    assert sorted_data[idx]["fecha"] == target_dt
    assert comps <= math.ceil(math.log2(len(sorted_data))) + 1

    # Benchmark wrapper
    res = benchmark_ologn_binary_search(sorted_data, target_dt, repetitions=10)
    assert res["complexity_class"] == "O(log n)"
    assert res["found"] is True
    assert res["operations_count"] == comps
    assert res["time_ns"] > 0


def test_on_linear_scan(sample_incidents):
    res = benchmark_on_linear_scan(sample_incidents, target_comuna="La Candelaria")
    assert res["complexity_class"] == "O(n)"
    assert res["size_n"] == 100
    assert res["operations_count"] == 100
    assert res["matches_count"] == 50
    assert res["fatal_count"] == 10
    assert res["total_risk_score"] > 0
    assert res["time_ns"] > 0


def test_onlogn_merge_sort(sample_incidents):
    sorted_res, comps = merge_sort_incidents(sample_incidents, key="radicado")
    assert len(sorted_res) == len(sample_incidents)

    # Verificar orden ascendente estricto
    for i in range(len(sorted_res) - 1):
        assert sorted_res[i]["radicado"] <= sorted_res[i + 1]["radicado"]

    res_bench = benchmark_onlogn_merge_sort(sample_incidents, key="radicado")
    assert res_bench["complexity_class"] == "O(n log n)"
    assert res_bench["size_n"] == 100
    assert res_bench["operations_count"] > 0
    assert res_bench["time_ns"] > 0


def test_on2_all_pairs_distance(sample_incidents):
    # Probar con tamaño pequeño (sin extrapolación)
    small_sample = sample_incidents[:30]
    res_direct = benchmark_on2_all_pairs_distance(small_sample, threshold_meters=100.0, max_safe_n=50)
    assert res_direct["complexity_class"] == "O(n^2)"
    assert res_direct["size_n"] == 30
    assert res_direct["is_extrapolated"] is False
    expected_ops = (30 * 29) // 2
    assert res_direct["operations_count"] == expected_ops

    # Probar cota con extrapolación segura
    res_extrapolated = benchmark_on2_all_pairs_distance(sample_incidents, threshold_meters=100.0, max_safe_n=20)
    assert res_extrapolated["is_extrapolated"] is True
    assert res_extrapolated["sample_measured_n"] == 20
    assert res_extrapolated["size_n"] == 100
    expected_full_ops = (100 * 99) // 2
    assert res_extrapolated["operations_count"] == expected_full_ops
