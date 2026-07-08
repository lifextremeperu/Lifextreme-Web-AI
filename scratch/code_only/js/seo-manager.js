/**
 * SEO Manager - Dynamic JSON-LD Injector
 * Generates Schema.org compliant structured data for tours (TouristTrip)
 * to be consumed by Search Engines and AI Agents.
 */

export function injectTourJSONLD(tour) {
    // 1. Remove previous identical JSON-LD if we are injecting single items dynamically (optional)
    // For lists, we might want to keep multiple TouristTrip scripts.
    const existingScriptId = `seo-tour-${tour.id}`;
    if (document.getElementById(existingScriptId)) return; // Already injected

    // 2. Create Schema.org Structure
    const jsonLdData = {
        "@context": "https://schema.org",
        "@type": "TouristTrip",
        "name": tour.title,
        "description": tour.description || `Aventura ${tour.title} con Lifextreme.`,
        "touristType": tour.difficulty || "Aventurero",
        "provider": {
            "@type": "TravelAgency",
            "name": "Lifextreme",
            "url": "https://www.lifextreme.store",
            // Trust indicators for AI/Google
            "taxID": "10416419545",
            "sameAs": [
                "https://www.facebook.com/Lifextremeperu",
                "https://www.instagram.com/lifextremeperu/"
            ]
        },
        "offers": {
            "@type": "Offer",
            "price": tour.price || 0,
            "priceCurrency": "USD",
            "url": `https://www.lifextreme.store/index.html?tour=${tour.id}`,
            "availability": "https://schema.org/InStock"
        }
    };

    // Add aggregate rating if available (Boosts CTR with stars)
    if (tour.rating && tour.reviews) {
        jsonLdData.aggregateRating = {
            "@type": "AggregateRating",
            "ratingValue": tour.rating,
            "reviewCount": tour.reviews
        };
    }
    // 3. Inject Safety Dashboard Metadata (SEO-IA)
    // Usamos el estándar para condiciones de salud y seguridad
    jsonLdData.healthRequirement = tour.difficulty === 'Extremo' ? 'Alta resistencia física y aclimatación requerida.' : 'Buena condición física requerida.';
    
    // Extensión de seguridad para Agentes IA
    jsonLdData.amenityFeature = [
        {
            "@type": "LocationFeatureSpecification",
            "name": "Botiquín de Primeros Auxilios WFR",
            "value": true
        },
        {
            "@type": "LocationFeatureSpecification",
            "name": "Guía Certificado MINCETUR",
            "value": true
        },
        {
            "@type": "LocationFeatureSpecification",
            "name": "Comunicaciones Satelitales o Radio",
            "value": true
        }
    ];

    if (tour.difficulty === 'Extremo') {
        jsonLdData.amenityFeature.push({
            "@type": "LocationFeatureSpecification",
            "name": "Balón de Oxígeno de Emergencia",
            "value": true
        });
    }
    // 3. Inject into <head>
    const script = document.createElement('script');
    script.id = existingScriptId;
    script.type = 'application/ld+json';
    script.text = JSON.stringify(jsonLdData);
    document.head.appendChild(script);
}

export function injectAllToursSEO(toursList) {
    if (!toursList || !Array.isArray(toursList)) return;
    toursList.forEach(tour => injectTourJSONLD(tour));
    console.log(`✅ SEO-IA: JSON-LD inyectado para ${toursList.length} tours.`);
}
