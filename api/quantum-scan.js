// ============================================================
// LIFEXTREME QUANTUM SCANNER — Vercel Serverless Function
// Analizador DOM en tiempo real y cálculo de fricción cuántica
// ============================================================

export default async function handler(req, res) {
    // Enable CORS
    res.setHeader('Access-Control-Allow-Credentials', true);
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
    res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version');

    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }

    const targetUrl = req.method === 'POST' ? req.body?.url : req.query?.url;

    if (!targetUrl) {
        return res.status(400).json({ error: 'Falta el parámetro "url" para analizar.' });
    }

    let normalizedUrl = targetUrl.trim();
    if (!normalizedUrl.startsWith('http://') && !normalizedUrl.startsWith('https://')) {
        normalizedUrl = 'https://' + normalizedUrl;
    }

    try {
        const startTime = Date.now();
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 12000);

        const response = await fetch(normalizedUrl, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 LifextremeQuantumScanner/2.4'
            },
            signal: controller.signal
        });
        clearTimeout(timeout);

        const latencyMs = Date.now() - startTime;
        const html = await response.text();

        // 1. Extraer Título
        const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
        const pageTitle = titleMatch ? titleMatch[1].trim() : normalizedUrl;

        // 2. Extraer Meta Description
        const metaDescMatch = html.match(/<meta[^>]*name=["']description["'][^>]*content=["']([^"']*)["']/i) ||
                              html.match(/<meta[^>]*content=["']([^"']*)["'][^>]*name=["']description["']/i);
        const metaDescription = metaDescMatch ? metaDescMatch[1].trim() : 'Sin meta descripción configurada.';

        // 3. Extraer H1s
        const h1Matches = [...html.matchAll(/<h1[^>]*>([\s\S]*?)<\/h1>/gi)];
        const h1List = h1Matches.map(m => m[1].replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim()).filter(Boolean);
        const mainH1 = h1List[0] || 'No se detectó etiqueta H1 principal';

        // 4. Extraer H2s
        const h2Matches = [...html.matchAll(/<h2[^>]*>([\s\S]*?)<\/h2>/gi)];
        const h2List = h2Matches.map(m => m[1].replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim()).filter(Boolean).slice(0, 5);

        // 5. Analizar Párrafos (Densidad de texto y lectura)
        const pMatches = [...html.matchAll(/<p[^>]*>([\s\S]*?)<\/p>/gi)];
        const pList = pMatches.map(m => m[1].replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim()).filter(t => t.length > 20);
        
        let denseParagraphsCount = 0;
        pList.forEach(p => {
            const wordCount = p.split(/\s+/).length;
            if (wordCount > 50) denseParagraphsCount++;
        });

        // 6. Detección de Precios Tangibles
        const priceRegex = /(\$\s?\d+([.,]\d{2})?|S\/\.?\s?\d+([.,]\d{2})?|\b\d+([.,]\d{2})?\s?(USD|PEN|EUR|dólares|soles|euros)\b)/gi;
        const pricesFound = [...html.matchAll(priceRegex)].map(m => m[0]).slice(0, 6);
        const hasVisiblePrices = pricesFound.length > 0;

        // 7. Detección de Formularios e Inputs
        const formMatches = [...html.matchAll(/<form[^>]*>([\s\S]*?)<\/form>/gi)];
        const formsCount = formMatches.length;

        // 8. Detección de CTAs (Botones y enlaces de contacto/reserva)
        const ctaMatches = [...html.matchAll(/<(?:a|button)[^>]*>([\s\S]*?)<\/(?:a|button)>/gi)];
        const ctaKeywords = ['reserv', 'cotiz', 'compr', 'inscrib', 'contact', 'whatsapp', 'agenda', 'ver tour', 'viaj'];
        const detectedCtas = [];
        ctaMatches.forEach(m => {
            const text = m[1].replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
            if (text.length > 2 && text.length < 50) {
                if (ctaKeywords.some(kw => text.toLowerCase().includes(kw))) {
                    if (!detectedCtas.includes(text)) detectedCtas.push(text);
                }
            }
        });

        // 9. Detección de WhatsApp directo
        const hasWhatsApp = /wa\.me|api\.whatsapp\.com|whatsapp/i.test(html);

        // ============================================================
        // CÁLCULO DE COEFICIENTES DE FRICCIÓN CUÁNTICA REAL
        // ============================================================
        
        // Coeficiente 1: Fricción de Hero (0.05 a 0.85)
        let heroFriction = 0.30;
        if (h1List.length === 0) heroFriction += 0.35; // Sin H1
        else if (mainH1.length < 10 || mainH1.length > 90) heroFriction += 0.15; // H1 muy corto o muy largo
        if (pageTitle.toLowerCase().includes('luna de miel') || pageTitle.toLowerCase().includes('viajes a medida')) {
            // Caso de agencia de lujo o tradicional
            if (!hasVisiblePrices) heroFriction += 0.10;
        }
        if (normalizedUrl.includes('lifextreme.store')) {
            heroFriction = 0.10; // Hero blanco ultra rápido
        }
        heroFriction = Math.max(0.08, Math.min(0.85, heroFriction));

        // Coeficiente 2: Fricción de Copy / Densidad de Texto (0.10 a 0.85)
        let copyFriction = 0.25;
        if (denseParagraphsCount > 2) copyFriction += 0.35; // Bloques densos sin viñetas
        if (pList.length === 0) copyFriction += 0.20; // Falta de contenido explicativo
        copyFriction = Math.max(0.10, Math.min(0.85, copyFriction));

        // Coeficiente 3: Fricción de Precio / Catálogo (0.10 a 0.90)
        let priceFriction = 0.25;
        if (!hasVisiblePrices) {
            priceFriction = 0.78; // Gran fuga si el usuario no sabe cuánto cuesta
        } else {
            priceFriction = 0.15; // Precios transparentes
        }
        if (normalizedUrl.includes('lifextreme.store')) {
            priceFriction = 0.12; // Precios explícitos en soles y reservas 30%
        }

        // Coeficiente 4: Fricción de CTA / Conversión (0.10 a 0.80)
        let ctaFriction = 0.30;
        if (formsCount === 0 && !hasWhatsApp) ctaFriction += 0.40; // Sin formulario ni WhatsApp
        if (detectedCtas.length === 0) ctaFriction += 0.30;
        if (hasWhatsApp) ctaFriction -= 0.10;
        if (formsCount > 0) ctaFriction -= 0.10;
        ctaFriction = Math.max(0.10, Math.min(0.80, ctaFriction));

        // 10. Generar Recomendaciones de Neuromarketing Específicas
        const recommendations = [];

        if (heroFriction > 0.30) {
            recommendations.push({
                priority: 'ALTA',
                icon: 'ri-focus-2-line',
                title: 'Claridad en Hero & H1 Principal',
                desc: `El H1 actual ("${mainH1.slice(0, 60)}...") debe sintetizar en 3 segundos qué ofreces, para quién es y el destino principal, evitando claims poéticos abstractos.`
            });
        } else {
            recommendations.push({
                priority: 'MANTENER',
                icon: 'ri-check-double-line',
                title: 'Propuesta de Valor de Impacto Rápido',
                desc: 'El encabezado principal tiene buena visibilidad y jerarquía tipográfica para retención inmediata de tráfico frío.'
            });
        }

        if (denseParagraphsCount > 1 || copyFriction > 0.35) {
            recommendations.push({
                priority: 'CRÍTICA',
                icon: 'ri-file-text-line',
                title: 'Desfragmentación de Párrafos Densos',
                desc: `Se detectaron ${denseParagraphsCount} párrafos largos con más de 50 palabras. El usuario en móvil no lee bloques continuos; sustitúyelos por 3 pilares con iconos y viñetas.`
            });
        } else {
            recommendations.push({
                priority: 'BUENA',
                icon: 'ri-layout-masonry-line',
                title: 'Arquitectura de Contenido Escaneable',
                desc: 'La longitud y fragmentación del contenido facilitan la digestión rápida de beneficios y características.'
            });
        }

        if (!hasVisiblePrices) {
            recommendations.push({
                priority: 'CRÍTICA',
                icon: 'ri-price-tag-3-line',
                title: 'Anclaje de Presupuesto o Precios Base',
                desc: 'La web no muestra referencias monetarias. Decir "viajes a medida sin precios" ahuyenta al 70% de usuarios con presupuesto limitado. Agrega rangos orientativos (ej. "Desde $1,800 USD").'
            });
        } else {
            recommendations.push({
                priority: 'EXCELENTE',
                icon: 'ri-money-dollar-circle-line',
                title: 'Transparencia de Tarifas y Desglose',
                desc: `Se detectaron precios visibles (${pricesFound.slice(0, 3).join(', ')}). Esto reduce la incertidumbre del consumidor y acelera la decisión de compra.`
            });
        }

        if (formsCount === 0) {
            recommendations.push({
                priority: 'ALTA',
                icon: 'ri-cursor-line',
                title: 'Incrustar Formulario Exprés en la Portada',
                desc: 'Actualmente no hay formularios de captura directa en la página de inicio. Agregar un widget de 2 campos (Nombre + WhatsApp) incrementará los leads entre un 40% y 65%.'
            });
        } else {
            recommendations.push({
                priority: 'BUENA',
                icon: 'ri-checkbox-circle-line',
                title: 'Captura de Leads Integrada',
                desc: `Se detectaron ${formsCount} formulario(s) activo(s) para canalizar las consultas del usuario sin fricción.`
            });
        }

        return res.status(200).json({
            success: true,
            targetUrl: normalizedUrl,
            latencyMs,
            analysis: {
                pageTitle,
                metaDescription,
                mainH1,
                h1List,
                h2List,
                denseParagraphsCount,
                hasVisiblePrices,
                pricesFound,
                formsCount,
                detectedCtas,
                hasWhatsApp
            },
            frictionWeights: [
                parseFloat(heroFriction.toFixed(3)),
                parseFloat(copyFriction.toFixed(3)),
                parseFloat(priceFriction.toFixed(3)),
                parseFloat(ctaFriction.toFixed(3))
            ],
            recommendations
        });

    } catch (err) {
        console.error('Error scanning target URL:', err);
        return res.status(500).json({
            success: false,
            error: `No se pudo conectar a la web: ${err.message}`,
            targetUrl: normalizedUrl
        });
    }
}
