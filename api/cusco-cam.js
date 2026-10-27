// Vercel Serverless Function: Real-Time Proxy for Cusco Plaza de Armas & Peru Live Webcams
// Bypasses CORS and Referer restrictions from SkylineWebcams CDN & HLS stream

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

const HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Referer': 'https://www.skylinewebcams.com/',
    'Accept': '*/*'
};

export default async function handler(req, res) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    const { cam = 'plaza_mayor', id, type = 'frame', seg } = req.query;

    try {
        // MODO 1: Descubrir todas las cámaras activas de Perú en SkylineWebcams
        if (type === 'discover') {
            const r = await fetch('https://www.skylinewebcams.com/es/webcam/peru.html', { headers: HEADERS });
            const html = await r.text();
            const matches = [...html.matchAll(/href="(\/es\/webcam\/peru\/[^"]+)"[\s\S]{0,600}?(?:live|social)(\d+)\.jpg/g)];
            const cams = matches.map(m => ({
                path: m[1],
                id: m[2],
                liveImg: `/api/cusco-cam?id=${m[2]}&type=frame`
            }));
            return res.status(200).json({ ok: true, cams });
        }

        // MODO 2: Proxy de segmento de video .ts para HLS
        if (type === 'ts' && seg) {
            const targetTs = decodeURIComponent(seg);
            if (!targetTs.startsWith('https://')) {
                return res.status(400).send('Invalid segment URL');
            }
            const tsResp = await fetch(targetTs, { headers: HEADERS });
            if (!tsResp.ok) {
                return res.status(tsResp.status).send('Segment fetch error');
            }
            const buf = Buffer.from(await tsResp.arrayBuffer());
            res.setHeader('Content-Type', 'video/mp2t');
            return res.status(200).send(buf);
        }

        // MODO 3: Extraer y proxificar stream HLS .m3u8 en vivo de la Plaza de Armas de Cusco
        if (type === 'm3u8') {
            const targetCam = CAMERA_MAP[cam] || CAMERA_MAP.plaza_mayor;
            const pageResp = await fetch(targetCam.page, { headers: HEADERS });
            const rawCookies = pageResp.headers.get('set-cookie') || '';
            const cookieHeader = rawCookies.split(',').map(c => c.split(';')[0]).join('; ');
            const html = await pageResp.text();

            const match = html.match(/livee\.m3u8\?a=([a-zA-Z0-9]+)/);
            if (!match) {
                return res.status(404).send('Stream token not found');
            }

            const token = match[1];
            const m3u8Url = `https://hd-auth.skylinewebcams.com/live.m3u8?a=${token}`;
            const m3u8Resp = await fetch(m3u8Url, {
                headers: {
                    ...HEADERS,
                    Cookie: cookieHeader
                }
            });

            if (!m3u8Resp.ok) {
                return res.status(m3u8Resp.status).send('Upstream HLS auth bound to client IP');
            }

            let m3u8Text = await m3u8Resp.text();
            // Reescribir segmentos relativos o absolutos hacia el proxy
            m3u8Text = m3u8Text.replace(/^(?!#)(.+)$/gm, (line) => {
                const trimmed = line.trim();
                if (!trimmed) return line;
                const absUrl = trimmed.startsWith('http')
                    ? trimmed
                    : `https://hd-auth.skylinewebcams.com/${trimmed.replace(/^\//, '')}`;
                return `/api/cusco-cam?type=ts&seg=${encodeURIComponent(absUrl)}`;
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
            const imgResp = await fetch(imgUrl, { headers: HEADERS });
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
