"""
Esquemas Pydantic v2 para validación estricta de solicitudes y respuestas de la API REST.
"""

from typing import List, Optional, Tuple, Dict, Any
from pydantic import BaseModel, Field


class Incident(BaseModel):
    radicado: str
    fecha: Optional[str] = None
    anio: int
    mes: int
    hora: Optional[str] = None
    clase_accidente: str
    gravedad: str
    factor_riesgo: float
    comuna_codigo: int
    comuna_nombre: str
    barrio: str
    diseno: str
    latitud: float
    longitud: float


class PaginatedIncidents(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[Incident]


class BenchmarkSortRequest(BaseModel):
    algorithm: str = Field(..., description="merge_sort, quick_sort, heap_sort, counting_sort, timsort")
    # Límites para que un servidor público (Render, 512 MB) no se sature con una sola petición
    size: int = Field(default=10000, ge=10, le=251150, description="1000 a 251150 (los tamaños de 500K y 1M están medidos en la Fase 4)")
    distribution: str = Field(default="random", description="random, sorted, reversed, duplicates")


class BenchmarkSortResponse(BaseModel):
    algorithm: str
    size: int
    distribution: str
    time_ms: float
    memory_kb: float
    comparisons: int
    theoretical_complexity: str
    theoretical_value: float


class BenchmarkSpatialRequest(BaseModel):
    size: int = Field(default=5000, ge=10, le=251150, description="Tamaño del índice de puntos (1K a 50K)")
    query_points: int = Field(default=100, ge=1, le=500, description="Número de consultas a evaluar")
    k: int = Field(default=5, ge=1, le=50, description="Número de vecinos más cercanos")


class BenchmarkSpatialResponse(BaseModel):
    size: int
    query_points: int
    k: int
    kdtree_build_time_ms: float
    kdtree_query_time_ms: float
    linear_query_time_ms: float
    speedup_factor: float


class ClusterRequest(BaseModel):
    eps_meters: float = Field(default=150.0, gt=0, le=2000, description="Radio de vecindad en metros")
    min_samples: int = Field(default=10, ge=1, le=500, description="Mínimo de siniestros para núcleo")
    sample_size: int = Field(default=2000, ge=10, le=10000, description="Muestra representativa para clustering")


class ClusterItem(BaseModel):
    cluster_id: int
    centroid: List[float]
    incident_count: int
    severity_score: float


class ClusterResponse(BaseModel):
    total_clusters: int
    noise_points: int
    clusters: List[ClusterItem]


class GeocodeItem(BaseModel):
    name: str
    display_name: str
    lat: float
    lon: float
    category: Optional[str] = "lugar"


class GeocodeResponse(BaseModel):
    query: str
    results: List[GeocodeItem]


class ReverseGeocodeResponse(BaseModel):
    lat: float
    lon: float
    display_name: str
    nearest_node_id: Optional[int] = None
    nearest_node_name: Optional[str] = None


class RoutingRequest(BaseModel):
    origin_lat: float = Field(..., description="Latitud de origen (ej. 6.2518)")
    origin_lon: float = Field(..., description="Longitud de origen (ej. -75.5636)")
    destination_lat: float = Field(..., description="Latitud de destino (ej. 6.2081)")
    destination_lon: float = Field(..., description="Longitud de destino (ej. -75.5674)")
    origin_name: Optional[str] = Field(default=None, description="Nombre o dirección del punto de origen A")
    destination_name: Optional[str] = Field(default=None, description="Nombre o dirección del punto de destino B")
    alpha_distance: float = Field(default=0.3, description="Peso de minimización de distancia (0.0 a 1.0)")
    beta_risk: float = Field(default=0.7, description="Peso de minimización de riesgo (0.0 a 1.0)")


class RouteInfo(BaseModel):
    total_distance_meters: float
    total_risk_score: float
    nodes_explored: int
    execution_time_ms: float
    coordinates: List[List[float]]


class RoutingResponse(BaseModel):
    found: bool
    origin: List[float]
    destination: List[float]
    origin_name: Optional[str] = None
    destination_name: Optional[str] = None
    start_node: Optional[int] = None
    target_node: Optional[int] = None
    shortest_route: RouteInfo
    safest_route: RouteInfo
    risk_reduction_percentage: float
    # False cuando la ruta segura coincide con la corta (no hay desvío razonable de menor riesgo)
    safest_is_alternative: bool = True
    notice: Optional[str] = None


class Fase4BenchmarkResults(BaseModel):
    metadata: Dict[str, Any]
    sorting: Dict[str, Any]
    spatial: Dict[str, Any]
    clustering: Dict[str, Any]
    routing: Dict[str, Any]


class HotspotItem(BaseModel):
    lugar: str
    barrio: Optional[str] = ""
    comuna_nombre: Optional[str] = ""
    latitud: float
    longitud: float
    incident_count: int
    fatal_count: int
    injured_count: int
    total_risk_score: float


class HotspotsResponse(BaseModel):
    total_hotspots: int
    items: List[HotspotItem]


class ComplexityBenchmarkRequest(BaseModel):
    complexity_class: str = Field(
        default="all",
        description="'all', 'o1', 'ologn', 'on', 'onlogn', 'on2'"
    )
    size: int = Field(
        default=10000,
        description="Tamaño n: 1000, 10000, 50000, 100000, 251150"
    )


class ComplexityBenchmarkResponse(BaseModel):
    size: int
    results: List[Dict[str, Any]]
    total_execution_time_ms: float



