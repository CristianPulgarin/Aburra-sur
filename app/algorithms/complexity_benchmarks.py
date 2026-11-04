"""
Módulo del Laboratorio de Jerarquía Asintótica.
Implementa operaciones canónicas desde cero para demostrar las 5 complejidades fundamentales:
O(1) -> O(log n) -> O(n) -> O(n log n) -> O(n^2)
sobre los datos reales de siniestralidad vial de Medellín (251.150 incidentes MEData).
"""

from typing import List, Dict, Any, Tuple, Optional
import time
import math


def haversine_distance_quick(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calcula la distancia Haversine en metros entre dos coordenadas geográficas."""
    R = 6371000.0  # Radio medio terrestre en metros
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c


# ==============================================================================
# 1. O(1) - Complejidad Constante: Acceso Directo por Hash / Diccionario
# ==============================================================================
def benchmark_o1_hash_lookup(
    incidents_dict: Dict[str, Dict[str, Any]],
    target_radicado: str,
    repetitions: int = 100
) -> Dict[str, Any]:
    """
    Demuestra O(1) realizando búsquedas directas en una tabla hash indexada por radicado.
    El tiempo permanece plano sin importar si el conjunto contiene 1.000 o 250.000 registros.
    """
    # Calentamiento de caché de Python
    _ = incidents_dict.get(target_radicado)

    start_ns = time.perf_counter_ns()
    found = False
    result_item = None
    for _ in range(repetitions):
        result_item = incidents_dict.get(target_radicado)
        if result_item is not None:
            found = True
    end_ns = time.perf_counter_ns()

    total_time_ns = end_ns - start_ns
    avg_time_ns = total_time_ns / max(1, repetitions)
    time_ms = avg_time_ns / 1_000_000.0

    return {
        "complexity_class": "O(1)",
        "name": "Acceso Directo por Tabla Hash",
        "description": "Búsqueda directa de siniestro por clave 'radicado' en diccionario indexado",
        "size_n": len(incidents_dict),
        "time_ns": round(avg_time_ns, 2),
        "time_ms": round(time_ms, 6),
        "operations_count": 1,
        "theoretical_formula": "c ~ O(1)",
        "found": found,
        "sample_result": result_item["radicado"] if result_item else None,
        "is_extrapolated": False
    }


# ==============================================================================
# 2. O(log n) - Complejidad Logarítmica: Búsqueda Binaria Pura
# ==============================================================================
def binary_search_incidents_by_date(
    sorted_records: List[Dict[str, Any]],
    target_date: str
) -> Tuple[Optional[int], int]:
    """
    Búsqueda binaria iterativa desde cero sobre una lista de siniestros ordenada cronológicamente.
    Retorna el índice del elemento (o de inserción) y el número exacto de comparaciones realizadas.
    """
    left = 0
    right = len(sorted_records) - 1
    comparisons = 0

    while left <= right:
        comparisons += 1
        mid = (left + right) // 2
        mid_val = sorted_records[mid].get("fecha", "")

        if mid_val == target_date:
            return mid, comparisons
        elif mid_val < target_date:
            left = mid + 1
        else:
            right = mid - 1

    return None, comparisons


def benchmark_ologn_binary_search(
    sorted_records: List[Dict[str, Any]],
    target_date: str,
    repetitions: int = 50
) -> Dict[str, Any]:
    """
    Demuestra O(log n) ejecutando búsqueda binaria sobre siniestros ordenados por fecha.
    Duplicar n solo agrega ~1 paso comparativo.
    """
    n = len(sorted_records)
    if n == 0:
        return {
            "complexity_class": "O(log n)",
            "name": "Búsqueda Binaria Temporal",
            "time_ns": 0,
            "time_ms": 0.0,
            "operations_count": 0,
            "theoretical_formula": "log2(n)",
            "found": False,
            "is_extrapolated": False
        }

    # Búsqueda representativa para obtener conteo exacto de operaciones
    idx, comps = binary_search_incidents_by_date(sorted_records, target_date)

    start_ns = time.perf_counter_ns()
    for _ in range(repetitions):
        _ = binary_search_incidents_by_date(sorted_records, target_date)
    end_ns = time.perf_counter_ns()

    avg_time_ns = (end_ns - start_ns) / max(1, repetitions)
    time_ms = avg_time_ns / 1_000_000.0
    theoretical_ops = math.ceil(math.log2(max(2, n)))

    return {
        "complexity_class": "O(log n)",
        "name": "Búsqueda Binaria Temporal",
        "description": "Búsqueda binaria iterativa sobre registros ordenados por fecha/hora",
        "size_n": n,
        "time_ns": round(avg_time_ns, 2),
        "time_ms": round(time_ms, 6),
        "operations_count": comps,
        "theoretical_operations": theoretical_ops,
        "theoretical_formula": f"ceil(log2({n})) = {theoretical_ops}",
        "found": idx is not None,
        "match_index": idx,
        "is_extrapolated": False
    }


# ==============================================================================
# 3. O(n) - Complejidad Lineal: Escaneo y Agregación Secuencial
# ==============================================================================
def benchmark_on_linear_scan(
    records: List[Dict[str, Any]],
    target_comuna: str = "La Candelaria"
) -> Dict[str, Any]:
    """
    Demuestra O(n) recorriendo exhaustivamente todos los registros para filtrar
    por comuna y calcular estadísticas agregadas de gravedad.
    El tiempo de cómputo escala de forma directamente proporcional al tamaño n.
    """
    n = len(records)
    start_ns = time.perf_counter_ns()

    matches_count = 0
    total_risk = 0.0
    fatal_count = 0

    for item in records:
        if item.get("comuna_nombre") == target_comuna:
            matches_count += 1
            total_risk += float(item.get("factor_riesgo", 0.0) or 0.0)
            if item.get("gravedad") == "CON MUERTOS":
                fatal_count += 1

    end_ns = time.perf_counter_ns()
    time_ns = end_ns - start_ns
    time_ms = time_ns / 1_000_000.0

    return {
        "complexity_class": "O(n)",
        "name": "Búsqueda y Agregación Secuencial",
        "description": f"Filtrado secuencial y suma acumulada de riesgo para comuna '{target_comuna}'",
        "size_n": n,
        "time_ns": time_ns,
        "time_ms": round(time_ms, 4),
        "operations_count": n,
        "theoretical_formula": f"n = {n}",
        "matches_count": matches_count,
        "fatal_count": fatal_count,
        "total_risk_score": round(total_risk, 2),
        "is_extrapolated": False
    }


# ==============================================================================
# 4. O(n log n) - Complejidad Lineal-Logarítmica: Merge Sort Puro
# ==============================================================================
def merge_sort_incidents(records: List[Dict[str, Any]], key: str = "fecha") -> Tuple[List[Dict[str, Any]], int]:
    """
    Merge Sort canónico implementado desde cero para ordenar registros de siniestros.
    Retorna la lista ordenada y el conteo de comparaciones de clave.
    Garantiza complejidad O(n log n) en el mejor, promedio y peor caso, y es estable.
    """
    comparisons = 0

    def _sort(arr: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        nonlocal comparisons
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = _sort(arr[:mid])
        right = _sort(arr[mid:])

        merged = []
        i = j = 0
        len_l, len_r = len(left), len(right)

        while i < len_l and j < len_r:
            comparisons += 1
            val_l = left[i].get(key, "")
            val_r = right[j].get(key, "")
            if val_l <= val_r:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        if i < len_l:
            merged.extend(left[i:])
        if j < len_r:
            merged.extend(right[j:])

        return merged

    sorted_res = _sort(records)
    return sorted_res, comparisons


def benchmark_onlogn_merge_sort(
    records: List[Dict[str, Any]],
    key: str = "fecha"
) -> Dict[str, Any]:
    """
    Demuestra O(n log n) ordenando registros de siniestros con Merge Sort desde cero.
    """
    n = len(records)
    start_ns = time.perf_counter_ns()
    _, comparisons = merge_sort_incidents(records, key=key)
    end_ns = time.perf_counter_ns()

    time_ns = end_ns - start_ns
    time_ms = time_ns / 1_000_000.0
    theoretical_ops = int(n * math.log2(max(2, n)))

    return {
        "complexity_class": "O(n log n)",
        "name": "Merge Sort Masivo (Divide & Conquer)",
        "description": f"Ordenamiento recursivo puro de {n} registros de siniestros por atributo '{key}'",
        "size_n": n,
        "time_ns": time_ns,
        "time_ms": round(time_ms, 3),
        "operations_count": comparisons,
        "theoretical_operations": theoretical_ops,
        "theoretical_formula": f"n * log2(n) ~ {theoretical_ops:,}",
        "is_extrapolated": False
    }


# ==============================================================================
# 5. O(n^2) - Complejidad Cuadrática: Fuerza Bruta de Pares a < 50 metros
# ==============================================================================
def benchmark_on2_all_pairs_distance(
    records: List[Dict[str, Any]],
    threshold_meters: float = 50.0,
    max_safe_n: int = 5000
) -> Dict[str, Any]:
    """
    Demuestra O(n^2) comparando todos los pares de siniestros para encontrar colisiones
    geográficas recurrentes a menos de threshold_meters (fuerza bruta sin KD-Tree).
    
    Cota de seguridad práctica:
    Para n > max_safe_n (ej. 10.000 o 250.000), una corrida completa requeriría > 3.1x10^10 comparaciones
    lo cual congelaría el servidor. Se mide una muestra representativa de max_safe_n y se extrapola
    rigurosamente la curva cuadrática: T(n) = T(muestra) * (n / muestra)^2.
    """
    n = len(records)
    actual_run_n = min(n, max_safe_n)
    sample = records[:actual_run_n]

    # Extraer coordenadas limpias en listas numéricas para máxima eficiencia
    coords = [
        (float(item.get("latitud", 0.0) or 0.0), float(item.get("longitud", 0.0) or 0.0))
        for item in sample
    ]

    start_ns = time.perf_counter_ns()
    pairs_found = 0
    comparisons = 0

    # Doble ciclo anidado exhaustivo
    for i in range(actual_run_n):
        lat1, lon1 = coords[i]
        for j in range(i + 1, actual_run_n):
            comparisons += 1
            lat2, lon2 = coords[j]
            # Filtro rápido previo en grados antes de Haversine completo
            if abs(lat1 - lat2) < 0.001 and abs(lon1 - lon2) < 0.001:
                dist = haversine_distance_quick(lat1, lon1, lat2, lon2)
                if dist <= threshold_meters:
                    pairs_found += 1

    end_ns = time.perf_counter_ns()
    sample_time_ns = end_ns - start_ns

    # Extrapolación matemática si n supera la cota de seguridad
    is_extrapolated = n > max_safe_n
    if is_extrapolated:
        scale_ratio = n / actual_run_n
        total_time_ns = int(sample_time_ns * (scale_ratio ** 2))
        total_comparisons = (n * (n - 1)) // 2
        extrapolated_pairs = int(pairs_found * (scale_ratio ** 2))
    else:
        total_time_ns = sample_time_ns
        total_comparisons = comparisons
        extrapolated_pairs = pairs_found

    time_ms = total_time_ns / 1_000_000.0
    theoretical_ops = (n * (n - 1)) // 2

    return {
        "complexity_class": "O(n^2)",
        "name": "Búsqueda Exhaustiva por Pares (All-Pairs Brute Force)",
        "description": f"Comparación exhaustiva de pares a < {threshold_meters} m sin indexación espacial",
        "size_n": n,
        "sample_measured_n": actual_run_n,
        "time_ns": total_time_ns,
        "time_ms": round(time_ms, 2),
        "operations_count": total_comparisons,
        "theoretical_operations": theoretical_ops,
        "theoretical_formula": f"n(n - 1)/2 = {theoretical_ops:,}",
        "pairs_at_proximity": extrapolated_pairs,
        "is_extrapolated": is_extrapolated,
        "extrapolation_note": (
            f"Medido empíricamente sobre m={actual_run_n} ({round(sample_time_ns / 1e6, 2)} ms) "
            f"y extrapolado a n={n} con factor (n/m)^2={round((n/actual_run_n)**2, 1)}x para evitar bloqueo de CPU."
            if is_extrapolated else "Medición directa en vivo sin extrapolación."
        )
    }

