from fastapi import APIRouter, HTTPException
import os
import json
from app.models.schemas import (
    BenchmarkSortRequest,
    BenchmarkSortResponse,
    BenchmarkSpatialRequest,
    BenchmarkSpatialResponse,
    Fase4BenchmarkResults,
    ComplexityBenchmarkRequest,
    ComplexityBenchmarkResponse,
)
from app.services.benchmark_service import benchmark_service

router = APIRouter(prefix="/benchmarks", tags=["Laboratorio de Benchmarks"])


@router.get("/fase4-results", response_model=Fase4BenchmarkResults)
def get_fase4_results():
    """
    Retorna la matriz consolidada de mediciones de benchmarking masivo (1K a 1.000.000)
    y metadatos de hardware generados en la Fase 4.
    """
    results_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
        "data", "benchmarks", "benchmark_results_fase4.json"
    )
    if os.path.exists(results_path):
        with open(results_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return Fase4BenchmarkResults(**data)
    else:
        raise HTTPException(
            status_code=404,
            detail="Resultados de Fase 4 no encontrados. Ejecute el script de benchmarking."
        )


@router.post("/sort", response_model=BenchmarkSortResponse)
def run_sort_benchmark(request: BenchmarkSortRequest):
    """
    Ejecuta un benchmark de ordenamiento (Merge, Quick, Heap, Counting o Timsort)
    sobre tamaños de 1K a 1M, midiendo tiempo, memoria y comparaciones.
    """
    result = benchmark_service.run_sort(
        algorithm=request.algorithm,
        size=request.size,
        distribution=request.distribution
    )
    return BenchmarkSortResponse(**result)


@router.post("/spatial", response_model=BenchmarkSpatialResponse)
def run_spatial_benchmark(request: BenchmarkSpatialRequest):
    """
    Compara empíricamente la construcción y consulta de KD-Tree O(log n)
    frente a la búsqueda exhaustiva lineal O(n).
    """
    result = benchmark_service.run_spatial_benchmark(
        size=request.size,
        query_points=request.query_points,
        k=request.k
    )
    return BenchmarkSpatialResponse(**result)


@router.post("/complexity", response_model=ComplexityBenchmarkResponse)
def run_complexity_benchmark(request: ComplexityBenchmarkRequest):
    """
    Ejecuta en tiempo real el Laboratorio de Jerarquía Asintótica
    O(1) -> O(log n) -> O(n) -> O(n log n) -> O(n^2)
    sobre la muestra de n siniestros viales de Medellín.
    """
    import math
    import time
    from app.algorithms.complexity_benchmarks import (
        benchmark_o1_hash_lookup,
        benchmark_ologn_binary_search,
        benchmark_on_linear_scan,
        benchmark_onlogn_merge_sort,
        benchmark_on2_all_pairs_distance,
    )
    from app.services.data_service import data_service

    start_total_ns = time.perf_counter_ns()
    size = max(100, min(request.size, 251150))
    cls_type = request.complexity_class.lower().strip()

    records, dict_radicado, sorted_records = data_service.get_cached_benchmark_data(size)

    target_rad = records[len(records) // 2].get("radicado", "A001") if records else "A001"
    target_dt = records[len(records) // 2].get("fecha", "2022-06-15") if records else "2022-06-15"

    results = []

    if cls_type in ("all", "o1"):
        res_o1 = benchmark_o1_hash_lookup(dict_radicado, target_radicado=target_rad)
        results.append(res_o1)

    if cls_type in ("all", "ologn"):
        res_ologn = benchmark_ologn_binary_search(sorted_records, target_date=target_dt)
        results.append(res_ologn)

    if cls_type in ("all", "on"):
        res_on = benchmark_on_linear_scan(records, target_comuna="La Candelaria")
        results.append(res_on)

    if cls_type in ("all", "onlogn"):
        # Para tamaños masivos (> 50.000) tomamos muestra de 30.000 y escalamos para respuesta rápida en API
        limit_merge = 30000
        merge_sample = records[:min(size, limit_merge)]
        res_onlogn = benchmark_onlogn_merge_sort(merge_sample, key="fecha")
        if size > limit_merge:
            scale = size / len(merge_sample)
            log_factor = math.log2(size) / math.log2(len(merge_sample))
            res_onlogn["size_n"] = size
            res_onlogn["time_ns"] = int(res_onlogn["time_ns"] * scale * log_factor)
            res_onlogn["time_ms"] = round(res_onlogn["time_ns"] / 1e6, 3)
            res_onlogn["is_extrapolated"] = True
            res_onlogn["operations_count"] = int(res_onlogn["operations_count"] * scale * log_factor)
        results.append(res_onlogn)

    if cls_type in ("all", "on2"):
        res_on2 = benchmark_on2_all_pairs_distance(records, threshold_meters=50.0, max_safe_n=2500)
        results.append(res_on2)

    total_execution_ms = round((time.perf_counter_ns() - start_total_ns) / 1_000_000.0, 3)

    return ComplexityBenchmarkResponse(
        size=size,
        results=results,
        total_execution_time_ms=total_execution_ms
    )


