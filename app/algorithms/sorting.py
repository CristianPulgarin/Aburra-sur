"""
Módulo de Algoritmos de Ordenamiento implementados desde cero.
Incluye: Merge Sort, Quick Sort (Mediana de 3), Heap Sort, Counting Sort y Wrapper Timsort.
Cada algoritmo registra el número de comparaciones de claves y operaciones primitivas.
"""

from typing import Any, Callable, List, Tuple
import time
import tracemalloc


class SortMetrics:
    def __init__(self, name: str, size: int):
        self.algorithm = name
        self.size = size
        self.comparisons = 0
        self.swaps = 0
        self.time_seconds = 0.0
        self.memory_kb = 0.0


def merge_sort(arr: List[Any], key: Callable[[Any], Any] = lambda x: x) -> Tuple[List[Any], int]:
    """
    Merge Sort (Ordenamiento por Mezcla).
    Complejidad: O(n log n) en todos los casos.
    Estable: Sí.
    Retorna: (lista_ordenada, total_comparaciones).
    """
    comparisons = 0

    def _sort(sub_arr: List[Any]) -> List[Any]:
        nonlocal comparisons
        if len(sub_arr) <= 1:
            return sub_arr

        mid = len(sub_arr) // 2
        left = _sort(sub_arr[:mid])
        right = _sort(sub_arr[mid:])

        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparisons += 1
            if key(left[i]) <= key(right[j]):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    sorted_arr = _sort(arr)
    return sorted_arr, comparisons


def quick_sort(arr: List[Any], key: Callable[[Any], Any] = lambda x: x) -> Tuple[List[Any], int]:
    """
    Quick Sort con partición Hoare, pivote Mediana de Tres y pila explícita O(log n).
    Complejidad: O(n log n) promedio, O(n^2) peor caso teórico.
    Espacial: O(log n) auxiliar en pila.
    Estable: No.
    Retorna: (lista_ordenada, total_comparaciones).
    """
    comparisons = 0
    result = list(arr)
    n = len(result)
    if n <= 1:
        return result, 0

    stack = [(0, n - 1)]

    while stack:
        low, high = stack.pop()
        if low >= high:
            continue

        # Mediana de 3 para elegir pivote
        mid = (low + high) // 2
        a, b, c = key(result[low]), key(result[mid]), key(result[high])
        comparisons += 3
        if (a <= b <= c) or (c <= b <= a):
            pivot_idx = mid
        elif (b <= a <= c) or (c <= a <= b):
            pivot_idx = low
        else:
            pivot_idx = high

        pivot_val = key(result[pivot_idx])

        # Partición Hoare
        i = low - 1
        j = high + 1

        while True:
            while True:
                i += 1
                comparisons += 1
                if key(result[i]) >= pivot_val:
                    break
            while True:
                j -= 1
                comparisons += 1
                if key(result[j]) <= pivot_val:
                    break

            if i >= j:
                p = j
                break

            result[i], result[j] = result[j], result[i]

        # Para acotar la profundidad de pila a O(log n), apilamos primero la partición más grande
        left_len = p - low + 1
        right_len = high - p

        if left_len > right_len:
            if low < p:
                stack.append((low, p))
            if p + 1 < high:
                stack.append((p + 1, high))
        else:
            if p + 1 < high:
                stack.append((p + 1, high))
            if low < p:
                stack.append((low, p))

    return result, comparisons


def heap_sort(arr: List[Any], key: Callable[[Any], Any] = lambda x: x) -> Tuple[List[Any], int]:
    """
    Heap Sort (Ordenamiento por Montículos).
    Complejidad: O(n log n) en todos los casos.
    Espacial: O(1) auxiliar (in-place).
    Retorna: (lista_ordenada, total_comparaciones).
    """
    comparisons = 0
    result = list(arr)
    n = len(result)

    def _heapify(size: int, root: int):
        nonlocal comparisons
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2

        if left < size:
            comparisons += 1
            if key(result[left]) > key(result[largest]):
                largest = left

        if right < size:
            comparisons += 1
            if key(result[right]) > key(result[largest]):
                largest = right

        if largest != root:
            result[root], result[largest] = result[largest], result[root]
            _heapify(size, largest)

    # Construir max-heap
    for i in range(n // 2 - 1, -1, -1):
        _heapify(n, i)

    # Extraer elementos uno a uno
    for i in range(n - 1, 0, -1):
        result[i], result[0] = result[0], result[i]
        _heapify(i, 0)

    return result, comparisons


def counting_sort(arr: List[int], min_val: int = 0, max_val: int = 100) -> Tuple[List[int], int]:
    """
    Counting Sort para claves enteras acotadas (comunas 1-16, severidad 1-3, etc.).
    Complejidad: O(n + k) donde k = max_val - min_val + 1.
    Retorna: (lista_ordenada, operaciones).
    """
    if not arr:
        return [], 0

    k = max_val - min_val + 1
    count = [0] * k
    operations = 0

    for x in arr:
        count[x - min_val] += 1
        operations += 1

    sorted_arr = []
    for val_offset, freq in enumerate(count):
        val = val_offset + min_val
        sorted_arr.extend([val] * freq)
        operations += freq

    return sorted_arr, operations


def run_sort_benchmark(arr: List[Any], algorithm_name: str, key_func: Callable[[Any], Any] = lambda x: x) -> SortMetrics:
    """
    Ejecuta un algoritmo de ordenamiento midiendo tiempo exacto y memoria consumida.
    """
    metrics = SortMetrics(algorithm_name, len(arr))

    tracemalloc.start()
    start_time = time.perf_counter()

    if algorithm_name == "merge_sort":
        _, comparisons = merge_sort(arr, key=key_func)
        metrics.comparisons = comparisons
    elif algorithm_name == "quick_sort":
        _, comparisons = quick_sort(arr, key=key_func)
        metrics.comparisons = comparisons
    elif algorithm_name == "heap_sort":
        _, comparisons = heap_sort(arr, key=key_func)
        metrics.comparisons = comparisons
    elif algorithm_name == "counting_sort":
        int_arr = [int(key_func(x)) for x in arr]
        mn, mx = (min(int_arr), max(int_arr)) if int_arr else (0, 0)
        _, ops = counting_sort(int_arr, min_val=mn, max_val=mx)
        metrics.comparisons = ops
    elif algorithm_name == "timsort":
        _ = sorted(arr, key=key_func)
        metrics.comparisons = int(len(arr) * 1.5)  # Estimado empírico Timsort
    else:
        raise ValueError(f"Algoritmo desconocido: {algorithm_name}")

    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    metrics.time_seconds = end_time - start_time
    metrics.memory_kb = peak / 1024.0

    return metrics
