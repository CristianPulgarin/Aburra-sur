"""
Enrutador unificado de la API v1.
"""

from fastapi import APIRouter
from app.api.v1.incidents import router as incidents_router
from app.api.v1.benchmarks import router as benchmarks_router
from app.api.v1.clusters import router as clusters_router
from app.api.v1.routing import router as routing_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(incidents_router)
api_v1_router.include_router(benchmarks_router)
api_v1_router.include_router(clusters_router)
api_v1_router.include_router(routing_router)
