"""
Servicio de Ejecución y Medición de Benchmarks Algorítmicos.
Ejecuta algoritmos sobre datos de prueba de 1K a 1M y calcula contrastes teóricos asintóticos.
"""

import os
import math
import time
import pandas as pd
from typing import Dict, Any, List
from app.algorithms.sorting import run_sort_benchmark
from app.algorithms.spatial_kdtree import KDTree2D, linear_search_nearest
from app.algorithms.clustering_dbscan import DBSCANClusterer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BENCHMARKS_DIR = os.path.join(BASE_DIR, "data", "benchmarks")


class BenchmarkService:
    def __init__(self):
        self._cache = {}

    def _get_benchmark_data(self, size: int) -> List[float]:
        label = f"{size//1000}k" if size < 1000000 else "1m"
        file_path = os.path.join(BENCHMARKS_DIR, f"bench_{label}.csv")

        if size in self._cache:
            return self._cache[size]

        if os.path.exists(file_path):
            df = pd.read_csv(file_path, usecols=["latitud", "longitud", "factor_riesgo"])
            # Usar coordenadas multiplicadas o sumadas como clave numérica de prueba
            keys = (df["latitud"] * 1000.0 + df["longitud"]).tolist()
            if size <= 100000:
                self._cache[size] = keys
            return keys
        else:
            # Fallback sintético determinista
            import random
            random.seed(42)
            return [random.uniform(6.15, 6.38) for _ in range(size)]

    def run_sort(self, algorithm: str, size: int, distribution: str = "random") -> Dict[str, Any]:
        data = self._get_benchmark_data(size)
        sample = list(data[:size])

        if distribution == "sorted":
            sample.sort()
        elif distribution == "reversed":
            sample.sort(reverse=True)
        elif distribution == "duplicates":
            sample = [round(x, 1) for x in sample]

        metrics = run_sort_benchmark(sample, algorithm)

        # Calcular valor teórico proporcional de referencia
        if algorithm in ["merge_sort", "quick_sort", "heap_sort", "timsort"]:
            theo_compl = "O(n log n)"
            theo_val = round(size * math.log2(max(2, size)), 2)
        elif algorithm == "counting_sort":
            theo_compl = "O(n + k)"
            theo_val = round(size * 1.2, 2)
        else:
            theo_compl = "O(n log n)"
            theo_val = size

        return {
            "algorithm": algorithm,
            "size": size,
            "distribution": distribution,
            "time_ms": round(metrics.time_seconds * 1000.0, 3),
            "memory_kb": round(metrics.memory_kb, 2),
            "comparisons": metrics.comparisons,
            "theoretical_complexity": theo_compl,
            "theoretical_value": theo_val
        }

    def run_spatial_benchmark(self, size: int, query_points: int, k: int) -> Dict[str, Any]:
        label = "10k" if size >= 10000 else "1k"
        file_path = os.path.join(BENCHMARKS_DIR, f"bench_{label}.csv")

        if os.path.exists(file_path):
            df = pd.read_csv(file_path, usecols=["latitud", "longitud"], nrows=size)
            points = [((row.latitud, row.longitud), i) for i, row in df.iterrows()]
        else:
            points = [((6.25 + i * 0.001, -75.56 + i * 0.001), i) for i in range(size)]

        # 1. Medir construcción de KD-Tree O(n log n)
        t0 = time.perf_counter()
        kdtree = KDTree2D(points)
        build_time = (time.perf_counter() - t0) * 1000.0

        queries = [p[0] for p in points[:min(query_points, len(points))]]

        # 2. Medir consultas KD-Tree O(q * log n)
        t1 = time.perf_counter()
        for q in queries:
            kdtree.k_nearest_neighbors(q, k=k)
        kd_query_time = (time.perf_counter() - t1) * 1000.0

        # 3. Medir consultas Lineales O(q * n)
        t2 = time.perf_counter()
        for q in queries:
            linear_search_nearest(points, q)
        linear_time = (time.perf_counter() - t2) * 1000.0

        speedup = round(linear_time / max(0.0001, kd_query_time), 2)

        return {
            "size": size,
            "query_points": len(queries),
            "k": k,
            "kdtree_build_time_ms": round(build_time, 2),
            "kdtree_query_time_ms": round(kd_query_time, 2),
            "linear_query_time_ms": round(linear_time, 2),
            "speedup_factor": speedup
        }

    def run_clustering(self, eps_meters: float, min_samples: int, sample_size: int) -> Dict[str, Any]:
        file_path = os.path.join(BENCHMARKS_DIR, "bench_10k.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, nrows=sample_size)
            coords = list(zip(df["latitud"], df["longitud"]))
            weights = df["factor_riesgo"].tolist()
        else:
            coords = [(6.25 + i * 0.001, -75.56 + i * 0.001) for i in range(sample_size)]
            weights = [1.0] * sample_size

        clusterer = DBSCANClusterer(eps_meters=eps_meters, min_samples=min_samples)
        return clusterer.fit(coords, weights)


benchmark_service = BenchmarkService()
