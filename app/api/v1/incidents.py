"""
Controlador REST para consulta y estadísticas de incidentes viales.
"""

from typing import Optional, List
from fastapi import APIRouter, Query
from app.models.schemas import PaginatedIncidents, HotspotsResponse, HotspotItem
from app.services.data_service import data_service

router = APIRouter(prefix="/incidents", tags=["Incidentes Viales"])


@router.get("", response_model=PaginatedIncidents)
def get_incidents_list(
    anio: Optional[int] = Query(None, description="Filtrar por año (ej. 2022)"),
    comuna_codigo: Optional[int] = Query(None, description="Código de comuna (1 a 16)"),
    gravedad: Optional[str] = Query(None, description="SOLO DAÑOS, CON HERIDOS, CON MUERTOS"),
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(50, ge=1, le=1000, description="Registros por página")
):
    total, items = data_service.get_incidents(
        anio=anio,
        comuna_codigo=comuna_codigo,
        gravedad=gravedad,
        page=page,
        page_size=page_size
    )
    return PaginatedIncidents(
        total=total,
        page=page,
        page_size=page_size,
        items=items
    )


@router.get("/summary")
def get_incidents_summary():
    """Retorna agregaciones estadísticas globales de siniestralidad vial en Medellín."""
    return data_service.get_summary_statistics()


@router.get("/analytics")
def get_incidents_analytics(
    anio: Optional[int] = Query(None, description="Filtrar por año (2014 a 2020)"),
    gravedad: Optional[str] = Query(None, description="SOLO DAÑOS, CON HERIDOS, CON MUERTOS"),
    comuna: Optional[str] = Query(None, description="Nombre exacto de la comuna (ej. 'La Candelaria')"),
):
    """
    Agregaciones cruzadas (gravedad, año, mes, hora, día de la semana, clase, comunas y barrios)
    con filtros combinables de año, gravedad y comuna para el tablero de analítica urbana.
    """
    return data_service.get_analytics(anio=anio, gravedad=gravedad, comuna=comuna)


@router.get("/hotspots", response_model=HotspotsResponse)
def get_incidents_hotspots(
    limit: int = Query(30, ge=1, le=100, description="Número máximo de puntos críticos a retornar"),
    gravedad: Optional[str] = Query(None, description="Filtrar por gravedad ('CON MUERTOS', 'CON HERIDOS', 'SOLO DAÑOS')")
):
    """
    Retorna los puntos críticos e intersecciones más peligrosas de Medellín
    con concentración histórica de siniestros viales y víctimas para visualización en mapa.
    """
    hotspots_raw = data_service.get_hotspots(limit=limit, gravedad=gravedad)
    items = [HotspotItem(**h) for h in hotspots_raw]
    return HotspotsResponse(
        total_hotspots=len(items),
        items=items
    )


@router.get("/heatmap")
def get_incidents_heatmap(
    gravedad: Optional[str] = Query(None, description="Filtrar por gravedad ('CON MUERTOS', 'CON HERIDOS')"),
    anio: Optional[int] = Query(None, description="Filtrar por año específico (ej. 2014 a 2020) o None para todo el histórico")
):
    """
    Retorna la densidad de siniestros agregada en celdas de ~110 m para la capa de calor del mapa.
    Formato compacto de celda: [lat, lon, total, con_muertos, con_heridos, idx_barrio, idx_comuna].
    Permite filtrar por año específico o consultar todo el histórico consolidado (2014-2020).
    """
    return data_service.get_heatmap_cells(gravedad=gravedad, anio=anio)

