"""
Controlador REST para detección de clusters y puntos críticos (DBSCAN).
"""

from fastapi import APIRouter
from app.models.schemas import ClusterRequest, ClusterResponse
from app.services.benchmark_service import benchmark_service

router = APIRouter(prefix="/clusters", tags=["Puntos Críticos / DBSCAN"])


@router.post("/dbscan", response_model=ClusterResponse)
def compute_dbscan_clusters(request: ClusterRequest):
    """
    Ejecuta DBSCAN geodésico sobre una muestra de siniestros viales
    para identificar puntos negros (hotspots) de accidentalidad y sus centroides.
    """
    result = benchmark_service.run_clustering(
        eps_meters=request.eps_meters,
        min_samples=request.min_samples,
        sample_size=request.sample_size
    )
    return ClusterResponse(**result)
