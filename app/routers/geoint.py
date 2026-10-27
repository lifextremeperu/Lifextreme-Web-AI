"""
Router FastAPI para Capas Geoespaciales GEOINT (Windy Webcams API v3)
Endpoint: GET /api/v1/geoint/layers/webcams
"""

from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from app.services.windy_geoint import windy_geoint_service

router = APIRouter(prefix="/api/v1/geoint/layers", tags=["GEOINT 3D Layers"])


@router.get("/webcams")
async def get_geoint_webcams_layer(response: Response) -> JSONResponse:
    """
    Devuelve la FeatureCollection GeoJSON de cámaras meteorológicas/turísticas públicas
    de Windy Webcams API v3 en el corredor Cusco - Valle Sagrado - Machu Picchu.
    Incluye cabecera Cache-Control: public, max-age=1800 y degradación elegante HTTP 200.
    """
    geojson_payload = await windy_geoint_service.get_webcams_geojson()
    return JSONResponse(
        status_code=200,
        content=geojson_payload,
        headers={
            "Cache-Control": "public, max-age=1800",
            "X-Geoint-Cache-Hit": str(geojson_payload.get("metadata", {}).get("cache_hit", False))
        }
    )
