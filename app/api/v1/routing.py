"""
Controlador REST para Enrutamiento Multiobjetivo y Geocodificación en la Red Vial de Medellín.
"""

from typing import List
from fastapi import APIRouter, Query
from app.models.schemas import (
    RoutingRequest,
    RoutingResponse,
    GeocodeResponse,
    GeocodeItem,
    ReverseGeocodeResponse,
)
from app.services.data_service import data_service

router = APIRouter(prefix="/routing", tags=["Enrutamiento en Grafos (Dijkstra / A*)"])


@router.get("/geocode", response_model=GeocodeResponse)
def geocode_address(
    q: str = Query(..., min_length=1, description="Texto de búsqueda de dirección, hito o calle de Medellín"),
    limit: int = Query(default=8, ge=1, le=20, description="Número máximo de resultados"),
):
    """
    Búsqueda predictiva de lugares y direcciones urbanas de Medellín tipo Google Maps.
    Resuelve lugares emblemáticos locales y direcciones OSM con bounding box en el Valle de Aburrá.
    """
    raw_results = data_service.search_places(q, limit=limit)
    items = [GeocodeItem(**r) for r in raw_results]
    return GeocodeResponse(query=q, results=items)


@router.get("/reverse-geocode", response_model=ReverseGeocodeResponse)
def reverse_geocode_coords(
    lat: float = Query(..., description="Latitud WGS84"),
    lon: float = Query(..., description="Longitud WGS84"),
):
    """
    Geocodificación inversa: Convierte coordenadas seleccionadas en el mapa en una dirección o referencia urbana.
    """
    res = data_service.reverse_geocode(lat, lon)
    return ReverseGeocodeResponse(**res)


@router.post("/calculate", response_model=RoutingResponse)
def calculate_routes(request: RoutingRequest):
    """
    Calcula simultáneamente la Ruta Más Corta vs. la Ruta Más Segura (menor riesgo de siniestros)
    desde el Punto A hasta el Punto B utilizando A* y Dijkstra con pesos multiobjetivo.
    Conecta el origen y destino continuos con la red vial mediante búsqueda KD-Tree en O(log V).
    """
    res = data_service.calculate_multiobjective_routes(
        origin_lat=request.origin_lat,
        origin_lon=request.origin_lon,
        dest_lat=request.destination_lat,
        dest_lon=request.destination_lon,
        alpha=request.alpha_distance,
        beta=request.beta_risk,
        origin_name=request.origin_name,
        destination_name=request.destination_name,
    )
    return RoutingResponse(**res)


@router.get("/network")
def get_road_network_topology():
    """Retorna la topología completa de nodos y tramos viales de Medellín para visualización en mapa."""
    return {
        "nodes": data_service.graph_nodes_raw,
        "edges": data_service.graph_edges_raw,
    }
