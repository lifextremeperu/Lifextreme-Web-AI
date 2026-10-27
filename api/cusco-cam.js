// Vercel Serverless Function: Real-Time HLS & Frame Proxy for Cusco Plaza de Armas (Skyline ID-831)
// Maintains session token cache so HLS.js can play continuous .m3u8 / .ts transitions

const CAMERA_MAP = {
    plaza_mayor: {
        id: '831',
        page: 'https://www.skylinewebcams.com/es/webcam/peru/cusco/cusco/plaza-mayor.html',
        name: 'Plaza Mayor de Cusco (Catedral & Compañía de Jesús)'
    },
    lima_miraflores: {
        id: '4293',
        page: 'https://www.skylinewebcams.com/es/webcam/peru/lima/lima/miraflores.html',
        name: 'Lima - Óvalo de Miraflores'
    }
};

const BASE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Referer': 'https://www.skylinewebcams.com/',
    'Origin': 'https://www.skylinewebcams.com',
    'Accept': '*/*'
};

// Cache en memoria para mantener el mismo token y cookie durante las recargas del manifiesto HLS
const sessionCache = {};

async function getSkylineSession(camKey) {
    const now = Date.now();
    const cached = sessionCache[camKey];
    if (cached && (now - cached.timestamp < 180000)) {
        return cached;
    }

    const targetCam = CAMERA_MAP[camKey] || CAMERA_MAP.plaza_mayor;
    const pageResp = await fetch(targetCam.page, { headers: BASE_HEADERS });
    const rawCookies = pageResp.headers.get('set-cookie') || '';
    const cookieHeader = rawCookies
        .split(/,(?=\s*[a-zA-Z0-9_-]+=)/)
        .map(c => c.split(';')[0].trim())
        .filter(Boolean)
        .join('; ');

    const html = await pageResp.text();
    const match = html.match(/livee\.m3u8\?a=([a-zA-Z0-9]+)/);
    if (!match) {
        throw new Error('Skyline stream token not found in page');
    }

    const session = {
        token: match[1],
        cookie: cookieHeader,
        m3u8Url: `https://hd-auth.skylinewebcams.com/live.m3u8?a=${match[1]}`,
        timestamp: now
    };
    sessionCache[camKey] = session;
    return session;
}

export default async function handler(req, res) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    const { cam = 'plaza_mayor', id, type = 'frame', seg } = req.query;

    try {
        // MODO 1: JSON con URL de stream e información de sesión
        if (type === 'json') {
            const session = await getSkylineSession(cam);
            return res.status(200).json({
                ok: true,
                cam,
                token: session.token,
                directM3u8: session.m3u8Url,
                proxyM3u8: `/api/cusco-cam?cam=${cam}&type=m3u8`,
                liveFrame: `/api/cusco-cam?id=${CAMERA_MAP[cam]?.id || '831'}&type=frame`
            });
        }

        // MODO 2: Proxy de segmento de video .ts para HLS
        if (type === 'ts' && seg) {
            const targetTs = decodeURIComponent(seg);
            if (!targetTs.startsWith('https://')) {
                return res.status(400).send('Invalid segment URL');
            }
            const cached = sessionCache[cam];
            const headers = {
                ...BASE_HEADERS,
                ...(cached?.cookie ? { Cookie: cached.cookie } : {})
            };
            const tsResp = await fetch(targetTs, { headers });
            if (!tsResp.ok) {
                return res.status(tsResp.status).send('Segment fetch error');
            }
            const buf = Buffer.from(await tsResp.arrayBuffer());
            res.setHeader('Content-Type', 'video/mp2t');
            return res.status(200).send(buf);
        }

        // MODO 3: Manifiesto HLS .m3u8 recursivo (resuelve master playlist -> chunklist -> segmentos .ts)
        if (type === 'm3u8') {
            let session = await getSkylineSession(cam);
            const authHeaders = {
                ...BASE_HEADERS,
                ...(session.cookie ? { Cookie: session.cookie } : {})
            };

            let m3u8Resp = await fetch(session.m3u8Url, { headers: authHeaders });
            if (!m3u8Resp.ok) {
                delete sessionCache[cam];
                session = await getSkylineSession(cam);
                m3u8Resp = await fetch(session.m3u8Url, {
                    headers: {
                        ...BASE_HEADERS,
                        ...(session.cookie ? { Cookie: session.cookie } : {})
                    }
                });
            }

            if (!m3u8Resp.ok) {
                return res.status(m3u8Resp.status).send('Upstream HLS token bound to client IP');
            }

            let m3u8Text = await m3u8Resp.text();

            // Si es un master playlist que apunta a otro .m3u8 (chunklist), lo resolvemos directamente
            const subM3u8Match = m3u8Text.match(/^(?!#)(.+\.m3u8.*)$/m);
            if (subM3u8Match) {
                const subPath = subM3u8Match[1].trim();
                const subUrl = subPath.startsWith('http')
                    ? subPath
                    : `https://hd-auth.skylinewebcams.com/${subPath.replace(/^\//, '')}`;
                const subResp = await fetch(subUrl, { headers: authHeaders });
                if (subResp.ok) {
                    m3u8Text = await subResp.text();
                }
            }

            // Reescribir cada segmento .ts hacia nuestro proxy
            m3u8Text = m3u8Text.replace(/^(?!#)(.+)$/gm, (line) => {
                const trimmed = line.trim();
                if (!trimmed) return line;
                const absUrl = trimmed.startsWith('http')
                    ? trimmed
                    : `https://hd-auth.skylinewebcams.com/${trimmed.replace(/^\//, '')}`;
                return `/api/cusco-cam?cam=${cam}&type=ts&seg=${encodeURIComponent(absUrl)}`;
            });

            res.setHeader('Content-Type', 'application/vnd.apple.mpegurl');
            return res.status(200).send(m3u8Text);
        }

        // MODO 4 (PREDETERMINADO): Frame JPEG en Tiempo Real de la Cámara de la Plaza de Armas de Cusco (ID 831)
        const camId = id ? String(id).replace(/[^0-9]/g, '') : (CAMERA_MAP[cam]?.id || '831');
        const timestamp = Date.now();
        const candidateUrls = [
            `https://cdn.skylinewebcams.com/live${camId}.jpg?t=${timestamp}`,
            `https://cdn.skylinewebcams.com/social${camId}.jpg?t=${timestamp}`
        ];

        for (const imgUrl of candidateUrls) {
            const imgResp = await fetch(imgUrl, { headers: BASE_HEADERS });
            if (imgResp.ok) {
                const contentType = imgResp.headers.get('content-type') || 'image/jpeg';
                const lastMod = imgResp.headers.get('last-modified') || new Date().toUTCString();
                const buffer = Buffer.from(await imgResp.arrayBuffer());
                res.setHeader('Content-Type', contentType);
                res.setHeader('X-Camera-Id', camId);
                res.setHeader('X-Camera-Last-Modified', lastMod);
                return res.status(200).send(buffer);
            }
        }

        return res.status(404).json({ error: 'Camera frame unavailable' });
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
}
