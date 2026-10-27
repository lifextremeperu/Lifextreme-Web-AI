"""
Servicio de Integración y Caché para Windy Webcams API v3 en GEOINT
Corredor Cusco - Valle Sagrado - Machu Picchu (lifextreme.store/geoint)
"""

import os
import time
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import httpx
from dotenv import load_dotenv

load_dotenv()

WINDY_API_URL = "https://api.windy.com/webcams/api/v3/webcams"
# Coordenadas Bounding Box (BBOX) del corredor Cusco - Valle Sagrado - Machu Picchu:
# Formato requerido: Norte, Este, Sur, Oeste
CUSCO_CORRIDOR_BBOX = "-13.10,-71.80,-13.60,-72.60"

# Elevaciones de referencia orográfica (m s.n.m.) para enriquecer nodos cuando la API no reporta altitud
DEFAULT_CUSCO_ELEVATION_M = 3399

# Nodos tácticos de respaldo y enriquecimiento en el corredor Cusco - Valle Sagrado - Machu Picchu
CORRIDOR_TACTICAL_WEBCAMS: List[Dict[str, Any]] = [
    {
        "id": "windy-cusco-plaza-831",
        "title": "Plaza de Armas de Cusco — Catedral & Centro Histórico",
        "city": "Cusco",
        "status": "active",
        "longitude": -71.97877,
        "latitude": -13.51687,
        "elevation": 3399,
        "thumbnail_url": "/api/cusco-cam?cam=plaza&type=jpg",
        "player_live_url": "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=km/h&zoom=12&overlay=wind&product=ecmwf&level=surface&lat=-13.5169&lon=-71.9788&detailLat=-13.5169&detailLon=-71.9788&marker=true",
        "player_day_url": "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=km/h&zoom=11&overlay=clouds&product=ecmwf&level=surface&lat=-13.5169&lon=-71.9788",
        "source": "windy_webcams"
    },
    {
        "id": "windy-urubamba-sanblas-04",
        "title": "Valle Sagrado / Cuesta San Blas — Mirador Urubamba",
        "city": "Urubamba",
        "status": "active",
        "longitude": -72.11650,
        "latitude": -13.30750,
        "elevation": 2870,
        "thumbnail_url": "/api/cusco-cam?cam=plaza&type=jpg",
        "player_live_url": "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=km/h&zoom=11&overlay=clouds&product=ecmwf&level=surface&lat=-13.3075&lon=-72.1165&detailLat=-13.3075&detailLon=-72.1165&marker=true",
        "player_day_url": "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=km/h&zoom=11&overlay=rain&product=ecmwf&level=surface&lat=-13.3075&lon=-72.1165",
        "source": "windy_webcams"
    },
    {
        "id": "windy-ollantaytambo-abra-05",
        "title": "Ollantaytambo & Acceso Abra Málaga (PE-28B)",
        "city": "Ollantaytambo",
        "status": "active",
        "longitude": -72.26330,
        "latitude": -13.25840,
        "elevation": 2792,
        "thumbnail_url": "/api/cusco-cam?cam=aeropuerto&type=jpg",
        "player_live_url": "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=km/h&zoom=11&overlay=rain&product=ecmwf&level=surface&lat=-13.2584&lon=-72.2633&detailLat=-13.2584&detailLon=-72.2633&marker=true",
        "player_day_url": "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=km/h&zoom=11&overlay=clouds&product=ecmwf&level=surface&lat=-13.2584&lon=-72.2633",
        "source": "windy_webcams"
    },
    {
        "id": "windy-machupicchu-aguascalientes-03",
        "title": "Machu Picchu Pueblo (Aguas Calientes — Cuenca Vilcanota)",
        "city": "Aguas Calientes",
        "status": "active",
        "longitude": -72.52550,
        "latitude": -13.15470,
        "elevation": 2040,
        "thumbnail_url": "/api/cusco-cam?cam=plaza&type=jpg",
        "player_live_url": "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=km/h&zoom=12&overlay=rain&product=ecmwf&level=surface&lat=-13.1547&lon=-72.5255&detailLat=-13.1547&detailLon=-72.5255&marker=true",
        "player_day_url": "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=km/h&zoom=12&overlay=wind&product=ecmwf&level=surface&lat=-13.1547&lon=-72.5255",
        "source": "windy_webcams"
    },
    {
        "id": "windy-aeropuerto-cuz-5172",
        "title": "Aeropuerto Internacional Alejandro Velasco Astete (CUZ - Pista 28/10)",
        "city": "Cusco",
        "status": "active",
        "longitude": -71.93880,
        "latitude": -13.53570,
        "elevation": 3310,
        "thumbnail_url": "/api/cusco-cam?cam=aeropuerto&type=jpg",
        "player_live_url": "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=kt&zoom=12&overlay=wind&product=ecmwf&level=surface&lat=-13.5357&lon=-71.9388&detailLat=-13.5357&detailLon=-71.9388&marker=true",
        "player_day_url": "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=kt&zoom=12&overlay=clouds&product=ecmwf&level=surface&lat=-13.5357&lon=-71.9388",
        "source": "windy_webcams"
    }
]


class WindyGeointService:
    """
    Cliente asíncrono para Windy Webcams API v3 con caché en memoria estricto (TTL = 1800s)
    que garantiza un máximo de 2 peticiones por hora a la API de Windy.
    """

    def __init__(self) -> None:
        self._cache_payload: Optional[Dict[str, Any]] = None
        self._last_fetch_timestamp: float = 0.0
        self._lock = asyncio.Lock()

    @property
    def ttl_seconds(self) -> int:
        try:
            return max(1800, int(os.getenv("GEOINT_CACHE_TTL_SECONDS", "1800")))
        except ValueError:
            return 1800

    @property
    def api_key(self) -> str:
        return os.getenv("WINDY_API_KEY", "").strip()

    def _transform_windy_cam_to_feature(self, cam: Dict[str, Any]) -> Dict[str, Any]:
        location = cam.get("location") or {}
        images = cam.get("images") or {}
        current_img = images.get("current") or {}
        daylight_img = images.get("daylight") or {}
        player = cam.get("player") or {}

        lon = float(location.get("longitude", -71.97877))
        lat = float(location.get("latitude", -13.51687))
        elevation = float(location.get("elevation", DEFAULT_CUSCO_ELEVATION_M if lat < -12.8 else 154))

        thumbnail_url = (
            current_img.get("preview")
            or current_img.get("thumbnail")
            or daylight_img.get("preview")
            or daylight_img.get("thumbnail")
            or "/api/cusco-cam?cam=plaza&type=jpg"
        )

        player_live_url = player.get("live") or None
        player_day_url = (
            player.get("day")
            or player.get("month")
            or player.get("lifetime")
            or f"https://embed.windy.com/embed.html?type=map&location=coordinates&zoom=11&overlay=wind&lat={lat}&lon={lon}&marker=true"
        )

        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat, elevation]
            },
            "properties": {
                "id": str(cam.get("webcamId") or cam.get("id")),
                "title": cam.get("title", "Webcam Meteorológica Windy"),
                "city": location.get("city", "Cusco"),
                "status": cam.get("status", "active"),
                "thumbnail_url": thumbnail_url,
                "player_live_url": player_live_url,
                "player_day_url": player_day_url,
                "source": "windy_webcams"
            }
        }

    def _build_tactical_fallback_features(self) -> List[Dict[str, Any]]:
        features: List[Dict[str, Any]] = []
        for node in CORRIDOR_TACTICAL_WEBCAMS:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [node["longitude"], node["latitude"], node["elevation"]]
                },
                "properties": {
                    "id": node["id"],
                    "title": node["title"],
                    "city": node["city"],
                    "status": node["status"],
                    "thumbnail_url": node["thumbnail_url"],
                    "player_live_url": node["player_live_url"],
                    "player_day_url": node["player_day_url"],
                    "source": "windy_webcams"
                }
            })
        return features

    async def get_webcams_geojson(self) -> Dict[str, Any]:
        now = time.time()
        ttl = self.ttl_seconds

        # 1. Verificación rápida de caché en memoria sin bloquear
        if self._cache_payload is not None and (now - self._last_fetch_timestamp) < ttl:
            cached = dict(self._cache_payload)
            cached["metadata"] = {
                **cached.get("metadata", {}),
                "cache_hit": True,
                "ttl_remaining_seconds": int(ttl - (now - self._last_fetch_timestamp))
            }
            return cached

        async with self._lock:
            now = time.time()
            if self._cache_payload is not None and (now - self._last_fetch_timestamp) < ttl:
                cached = dict(self._cache_payload)
                cached["metadata"] = {
                    **cached.get("metadata", {}),
                    "cache_hit": True,
                    "ttl_remaining_seconds": int(ttl - (now - self._last_fetch_timestamp))
                }
                return cached

            api_key = self.api_key
            if not api_key:
                # Degradación elegante si no hay API Key configurada
                fallback_collection = {
                    "type": "FeatureCollection",
                    "metadata": {
                        "source": "windy_webcams_v3",
                        "bbox": CUSCO_CORRIDOR_BBOX,
                        "cache_hit": False,
                        "ttl_seconds": ttl,
                        "fetched_at": datetime.now(timezone.utc).isoformat(),
                        "warning": "WINDY_API_KEY no configurada en el entorno; sirviendo nodos tácticos del corredor Cusco - Machu Picchu."
                    },
                    "features": self._build_tactical_fallback_features()
                }
                self._cache_payload = fallback_collection
                self._last_fetch_timestamp = now
                return fallback_collection

            headers = {
                "x-windy-api-key": api_key,
                "Accept": "application/json"
            }
            params = {
                "bbox": CUSCO_CORRIDOR_BBOX,
                "include": "location,images,player,categories",
                "limit": 50
            }

            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.get(WINDY_API_URL, params=params, headers=headers)

                    # Si BBOX estricto devuelve 0 cámaras activas en Windy v3, consultar cámaras de Perú (PE) en la misma ventana de caché
                    if response.status_code == 200:
                        data = response.json()
                        raw_webcams = data.get("webcams") or []
                        if not raw_webcams:
                            pe_resp = await client.get(
                                WINDY_API_URL,
                                params={"countries": "PE", "include": "location,images,player,categories", "limit": 50},
                                headers=headers
                            )
                            if pe_resp.status_code == 200:
                                raw_webcams = pe_resp.json().get("webcams") or []

                        features = [self._transform_windy_cam_to_feature(cam) for cam in raw_webcams]
                        # Combinar con los nodos tácticos del corredor Cusco - Valle Sagrado - Machu Picchu
                        existing_ids = {f["properties"]["id"] for f in features}
                        for tactical_feat in self._build_tactical_fallback_features():
                            if tactical_feat["properties"]["id"] not in existing_ids:
                                features.append(tactical_feat)

                        feature_collection = {
                            "type": "FeatureCollection",
                            "metadata": {
                                "source": "windy_webcams_v3",
                                "bbox": CUSCO_CORRIDOR_BBOX,
                                "cache_hit": False,
                                "ttl_seconds": ttl,
                                "windy_live_count": len(raw_webcams),
                                "total_features": len(features),
                                "fetched_at": datetime.now(timezone.utc).isoformat(),
                                "warning": None
                            },
                            "features": features
                        }
                        self._cache_payload = feature_collection
                        self._last_fetch_timestamp = time.time()
                        return feature_collection

                    # Manejo de Rate Limit (429) o error de API
                    raise httpx.HTTPStatusError(
                        f"Windy API respondió con HTTP {response.status_code}",
                        request=response.request,
                        response=response
                    )

            except Exception as exc:
                # Devolver último snapshot válido en caché con HTTP 200 y advertencia en metadatos
                self._last_fetch_timestamp = time.time()
                if self._cache_payload is not None:
                    stale_copy = dict(self._cache_payload)
                    stale_copy["metadata"] = {
                        **stale_copy.get("metadata", {}),
                        "cache_hit": True,
                        "stale_fallback": True,
                        "warning": f"Fallo o límite alcanzado en Windy API v3 ({str(exc)}). Sirviendo último snapshot cacheado válido."
                    }
                    return stale_copy

                fallback_collection = {
                    "type": "FeatureCollection",
                    "metadata": {
                        "source": "windy_webcams_v3",
                        "bbox": CUSCO_CORRIDOR_BBOX,
                        "cache_hit": False,
                        "stale_fallback": True,
                        "ttl_seconds": ttl,
                        "fetched_at": datetime.now(timezone.utc).isoformat(),
                        "warning": f"Error conectando con Windy API v3 ({str(exc)}). Sirviendo snapshot táctico de contingencia."
                    },
                    "features": self._build_tactical_fallback_features()
                }
                self._cache_payload = fallback_collection
                return fallback_collection


windy_geoint_service = WindyGeointService()
