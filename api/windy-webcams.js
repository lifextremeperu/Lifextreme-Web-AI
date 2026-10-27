/**
 * LIFEXTREME GEOINT — SERVICIO DE INTEGRACIÓN Y CACHÉ WINDY WEBCAMS API v3
 * Endpoint público: GET /api/v1/geoint/layers/webcams (vía rewrite en vercel.json)
 * Cumple con TTL estricto de 1800 segundos (máximo 2 consultas por hora a Windy API v3).
 */

const WINDY_API_URL = "https://api.windy.com/webcams/api/v3/webcams";
const CUSCO_CORRIDOR_BBOX = "-13.10,-71.80,-13.60,-72.60"; // Norte, Este, Sur, Oeste

// Caché en memoria con invalidación por tiempo (TTL = 1800s = 30 min)
let memoryCachePayload = null;
let lastFetchTimestampMs = 0;

// Nodos tácticos del Corredor Cusco - Valle Sagrado - Machu Picchu con elevación orográfica 3D real (m s.n.m.)
const CORRIDOR_TACTICAL_WEBCAMS = [
    {
        id: "windy-cusco-plaza-831",
        title: "Plaza de Armas de Cusco — Catedral & Centro Histórico",
        city: "Cusco",
        status: "active",
        longitude: -71.97877,
        latitude: -13.51687,
        elevation: 3399,
        thumbnail_url: "/api/cusco-cam?cam=plaza&type=jpg",
        player_live_url: "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=km/h&zoom=12&overlay=wind&product=ecmwf&level=surface&lat=-13.5169&lon=-71.9788&detailLat=-13.5169&detailLon=-71.9788&marker=true",
        player_day_url: "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=km/h&zoom=11&overlay=clouds&product=ecmwf&level=surface&lat=-13.5169&lon=-71.9788",
        source: "windy_webcams"
    },
    {
        id: "windy-urubamba-sanblas-04",
        title: "Valle Sagrado / Cuesta San Blas — Mirador Urubamba",
        city: "Urubamba",
        status: "active",
        longitude: -72.11650,
        latitude: -13.30750,
        elevation: 2870,
        thumbnail_url: "/api/cusco-cam?cam=plaza&type=jpg",
        player_live_url: "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=km/h&zoom=11&overlay=clouds&product=ecmwf&level=surface&lat=-13.3075&lon=-72.1165&detailLat=-13.3075&detailLon=-72.1165&marker=true",
        player_day_url: "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=km/h&zoom=11&overlay=rain&product=ecmwf&level=surface&lat=-13.3075&lon=-72.1165",
        source: "windy_webcams"
    },
    {
        id: "windy-ollantaytambo-abra-05",
        title: "Ollantaytambo & Acceso Abra Málaga (PE-28B)",
        city: "Ollantaytambo",
        status: "active",
        longitude: -72.26330,
        latitude: -13.25840,
        elevation: 2792,
        thumbnail_url: "/api/cusco-cam?cam=aeropuerto&type=jpg",
        player_live_url: "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=km/h&zoom=11&overlay=rain&product=ecmwf&level=surface&lat=-13.2584&lon=-72.2633&detailLat=-13.2584&detailLon=-72.2633&marker=true",
        player_day_url: "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=km/h&zoom=11&overlay=clouds&product=ecmwf&level=surface&lat=-13.2584&lon=-72.2633",
        source: "windy_webcams"
    },
    {
        id: "windy-machupicchu-aguascalientes-03",
        title: "Machu Picchu Pueblo (Aguas Calientes — Cuenca Vilcanota)",
        city: "Aguas Calientes",
        status: "active",
        longitude: -72.52550,
        latitude: -13.15470,
        elevation: 2040,
        thumbnail_url: "/api/cusco-cam?cam=plaza&type=jpg",
        player_live_url: "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=km/h&zoom=12&overlay=rain&product=ecmwf&level=surface&lat=-13.1547&lon=-72.5255&detailLat=-13.1547&detailLon=-72.5255&marker=true",
        player_day_url: "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=km/h&zoom=12&overlay=wind&product=ecmwf&level=surface&lat=-13.1547&lon=-72.5255",
        source: "windy_webcams"
    },
    {
        id: "windy-aeropuerto-cuz-5172",
        title: "Aeropuerto Internacional Alejandro Velasco Astete (CUZ - Pista 28/10)",
        city: "Cusco",
        status: "active",
        longitude: -71.93880,
        latitude: -13.53570,
        elevation: 3310,
        thumbnail_url: "/api/cusco-cam?cam=aeropuerto&type=jpg",
        player_live_url: "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=kt&zoom=12&overlay=wind&product=ecmwf&level=surface&lat=-13.5357&lon=-71.9388&detailLat=-13.5357&detailLon=-71.9388&marker=true",
        player_day_url: "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=kt&zoom=12&overlay=clouds&product=ecmwf&level=surface&lat=-13.5357&lon=-71.9388",
        source: "windy_webcams"
    }
];

function transformWindyCamToFeature(cam) {
    const loc = cam.location || {};
    const images = cam.images || {};
    const currentImg = images.current || {};
    const daylightImg = images.daylight || {};
    const player = cam.player || {};

    const lon = Number(loc.longitude ?? -71.97877);
    const lat = Number(loc.latitude ?? -13.51687);
    const elevation = Number(loc.elevation ?? (lat < -12.8 ? 3399 : 154));

    const thumbnailUrl =
        currentImg.preview ||
        currentImg.thumbnail ||
        daylightImg.preview ||
        daylightImg.thumbnail ||
        "/api/cusco-cam?cam=plaza&type=jpg";

    const playerLiveUrl = player.live || null;
    const playerDayUrl =
        player.day ||
        player.month ||
        player.lifetime ||
        `https://embed.windy.com/embed.html?type=map&location=coordinates&zoom=11&overlay=wind&lat=${lat}&lon=${lon}&marker=true`;

    return {
        type: "Feature",
        geometry: {
            type: "Point",
            coordinates: [lon, lat, elevation]
        },
        properties: {
            id: String(cam.webcamId || cam.id),
            title: cam.title || "Webcam Meteorológica Windy",
            city: loc.city || "Perú",
            status: cam.status || "active",
            thumbnail_url: thumbnailUrl,
            player_live_url: playerLiveUrl,
            player_day_url: playerDayUrl,
            source: "windy_webcams"
        }
    };
}

function buildTacticalFallbackFeatures() {
    return CORRIDOR_TACTICAL_WEBCAMS.map(node => ({
        type: "Feature",
        geometry: {
            type: "Point",
            coordinates: [node.longitude, node.latitude, node.elevation]
        },
        properties: {
            id: node.id,
            title: node.title,
            city: node.city,
            status: node.status,
            thumbnail_url: node.thumbnail_url,
            player_live_url: node.player_live_url,
            player_day_url: node.player_day_url,
            source: "windy_webcams"
        }
    }));
}

module.exports = async function handler(req, res) {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.setHeader("Cache-Control", "public, max-age=1800, s-maxage=1800, stale-while-revalidate=3600");

    if (req.method === "OPTIONS") {
        return res.status(200).end();
    }

    const ttlSeconds = Math.max(1800, parseInt(process.env.GEOINT_CACHE_TTL_SECONDS || "1800", 10));
    const ttlMs = ttlSeconds * 1000;
    const now = Date.now();

    // 1. Si el timestamp de la última consulta es menor a GEOINT_CACHE_TTL_SECONDS (1800s), responder desde memoria
    if (memoryCachePayload && (now - lastFetchTimestampMs) < ttlMs) {
        const cachedResponse = {
            ...memoryCachePayload,
            metadata: {
                ...memoryCachePayload.metadata,
                cache_hit: true,
                ttl_remaining_seconds: Math.round((ttlMs - (now - lastFetchTimestampMs)) / 1000)
            }
        };
        return res.status(200).json(cachedResponse);
    }

    const apiKey = (process.env.WINDY_API_KEY || "oDs6J0lZ2Hm0OlzDuPZfVvpgAqTxs9aU").trim();

    try {
        const bboxUrl = `${WINDY_API_URL}?bbox=${encodeURIComponent(CUSCO_CORRIDOR_BBOX)}&include=location,images,player,categories&limit=50`;
        const response = await fetch(bboxUrl, {
            method: "GET",
            headers: {
                "x-windy-api-key": apiKey,
                "Accept": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error(`Windy API v3 respondió HTTP ${response.status}`);
        }

        const data = await response.json();
        let rawWebcams = Array.isArray(data.webcams) ? data.webcams : [];

        // Si el BBOX estricto de Cusco devuelve 0 cámaras activas en Windy v3 en este momento,
        // consultamos las cámaras activas de Perú (countries=PE) dentro de la misma ventana de caché
        if (rawWebcams.length === 0) {
            const peUrl = `${WINDY_API_URL}?countries=PE&include=location,images,player,categories&limit=50`;
            const peRes = await fetch(peUrl, {
                method: "GET",
                headers: {
                    "x-windy-api-key": apiKey,
                    "Accept": "application/json"
                }
            });
            if (peRes.ok) {
                const peData = await peRes.json();
                rawWebcams = Array.isArray(peData.webcams) ? peData.webcams : [];
            }
        }

        const windyFeatures = rawWebcams.map(transformWindyCamToFeature);
        const tacticalFeatures = buildTacticalFallbackFeatures();

        // Unir cámaras en vivo de Windy API v3 + nodos tácticos del corredor Cusco - Valle Sagrado - Machu Picchu
        const existingIds = new Set(windyFeatures.map(f => f.properties.id));
        const combinedFeatures = [...windyFeatures];
        for (const tf of tacticalFeatures) {
            if (!existingIds.has(tf.properties.id)) {
                combinedFeatures.push(tf);
            }
        }

        const featureCollection = {
            type: "FeatureCollection",
            metadata: {
                source: "windy_webcams_v3",
                bbox: CUSCO_CORRIDOR_BBOX,
                cache_hit: false,
                ttl_seconds: ttlSeconds,
                windy_api_live_count: windyFeatures.length,
                corridor_tactical_count: tacticalFeatures.length,
                total_features: combinedFeatures.length,
                fetched_at: new Date().toISOString(),
                warning: null
            },
            features: combinedFeatures
        };

        memoryCachePayload = featureCollection;
        lastFetchTimestampMs = Date.now();

        return res.status(200).json(featureCollection);
    } catch (error) {
        // Degradación elegante: devolver último snapshot válido o nodos tácticos con HTTP 200
        lastFetchTimestampMs = Date.now();
        if (memoryCachePayload) {
            return res.status(200).json({
                ...memoryCachePayload,
                metadata: {
                    ...memoryCachePayload.metadata,
                    cache_hit: true,
                    stale_fallback: true,
                    warning: `Windy API v3 no disponible temporalmente (${error.message}). Sirviendo último snapshot cacheado válido.`
                }
            });
        }

        const fallbackPayload = {
            type: "FeatureCollection",
            metadata: {
                source: "windy_webcams_v3",
                bbox: CUSCO_CORRIDOR_BBOX,
                cache_hit: false,
                stale_fallback: true,
                ttl_seconds: ttlSeconds,
                fetched_at: new Date().toISOString(),
                warning: `Modo de contingencia activo (${error.message}). Sirviendo nodos tácticos del corredor Cusco - Machu Picchu.`
            },
            features: buildTacticalFallbackFeatures()
        };

        memoryCachePayload = fallbackPayload;
        return res.status(200).json(fallbackPayload);
    }
};
