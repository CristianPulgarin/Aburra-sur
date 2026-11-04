"""
Pruebas unitarias y de casos borde para los algoritmos de ordenamiento.
"""

import pytest
import random
from app.algorithms.sorting import merge_sort, quick_sort, heap_sort, counting_sort, run_sort_benchmark


@pytest.mark.parametrize("sort_fn", [merge_sort, quick_sort, heap_sort])
def test_sorting_empty_and_single(sort_fn):
    # Caso borde: Lista vacía
    res, ops = sort_fn([])
    assert res == []

    # Caso borde: Lista unitaria
    res, ops = sort_fn([42])
    assert res == [42]


@pytest.mark.parametrize("sort_fn", [merge_sort, quick_sort, heap_sort])
def test_sorting_correctness_random(sort_fn):
    random.seed(42)
    sample = [random.randint(-1000, 1000) for _ in range(500)]
    expected = sorted(sample)
    res, ops = sort_fn(sample)
    assert res == expected
    assert ops > 0


@pytest.mark.parametrize("sort_fn", [merge_sort, quick_sort, heap_sort])
def test_sorting_identical_elements(sort_fn):
    # Caso borde: Elementos repetidos masivos
    sample = [7] * 200
    res, ops = sort_fn(sample)
    assert res == [7] * 200


@pytest.mark.parametrize("sort_fn", [merge_sort, quick_sort, heap_sort])
def test_sorting_already_sorted_and_reversed(sort_fn):
    # Caso borde: Ya ordenada
    sample_asc = list(range(100))
    res, _ = sort_fn(sample_asc)
    assert res == sample_asc

    # Caso borde: Orden inverso
    sample_desc = list(range(100, 0, -1))
    res, _ = sort_fn(sample_desc)
    assert res == sorted(sample_desc)


def test_counting_sort():
    sample = [5, 1, 16, 2, 8, 16, 1, 5, 3]
    res, ops = counting_sort(sample, min_val=1, max_val=16)
    assert res == sorted(sample)
    assert ops > 0

    # Caso borde: vacío
    res, _ = counting_sort([])
    assert res == []


def test_run_sort_benchmark():
    sample = list(range(50, 0, -1))
    metrics = run_sort_benchmark(sample, "merge_sort")
    assert metrics.size == 50
    assert metrics.time_seconds >= 0.0
    assert metrics.comparisons > 0
