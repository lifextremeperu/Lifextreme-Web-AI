// --- CMS SERVICE (Headless Simulation) ---

const CMSService = {
    /**
     * Obtiene los datos de los guías desde el "Headless CMS".
     * @returns {Promise<Array>}
     */
    async getGuides() {
        try {
            const response = await fetch('js/guides-cms.json');
            if (!response.ok) throw new Error('Error al conectar con Lifextreme CMS');
            return await response.json();
        } catch (error) {
            console.error('CMS Error:', error);
            // Fallback en caso de error de red
            return [
                {
                    name: "Guía Lifextreme",
                    specialty: "Operario Certificado",
                    img: "https://images.unsplash.com/photo-1544005313-94ddf0286df2",
                    achievements: ["Certificación Táctica UIAGM"],
                    bio: "Nuestros guías están listos para tu aventura."
                }
            ];
        }
    }
};

window.CMSService = CMSService;
