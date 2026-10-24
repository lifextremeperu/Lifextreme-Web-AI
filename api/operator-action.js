// ==============================================================================
// LIFEXTREME ADVENTURE ENGINE — Operador Callback Serverless (Vercel)
// Permite al Guía/Operador en Cusco Aceptar o Rechazar Reservas con 1 Solo Tap
// ==============================================================================

export default async function handler(req, res) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Content-Type', 'text/html; charset=utf-8');

    const { action, id, token, op } = req.query;

    if (!id || !action) {
        return res.status(400).send(`
            <!DOCTYPE html>
            <html lang="es">
            <head><meta charset="UTF-8"><title>Error de Parámetros</title><script src="https://cdn.tailwindcss.com"></script></head>
            <body class="bg-slate-950 text-slate-100 flex items-center justify-center min-h-screen p-4 font-sans">
                <div class="bg-slate-900 border border-red-500/30 p-6 rounded-2xl max-w-md text-center">
                    <p class="text-3xl mb-2">⚠️</p>
                    <h1 class="text-xl font-bold text-red-400">Enlace Inválido o Incompleto</h1>
                    <p class="text-xs text-slate-400 mt-2">No se encontró el ID de reserva correspondiente.</p>
                </div>
            </body>
            </html>
        `);
    }

    const isAccepted = action.toLowerCase() === 'accept';
    const operatorName = op ? decodeURIComponent(op) : 'Operador Certificado Lifextreme';

    // Página de confirmación móvil de alto contraste para el operador
    const htmlResponse = `
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>${isAccepted ? '¡Reserva Aceptada!' : 'Reserva Rechazada'} | Lifextreme Partner</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800;900&display=swap" rel="stylesheet">
        <style>body { font-family: 'Plus Jakarta Sans', sans-serif; }</style>
    </head>
    <body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col justify-between p-4 sm:p-6 antialiased selection:bg-cyan-500">
        
        <div class="max-w-md w-full mx-auto my-auto">
            
            <!-- TARJETA DE ESTADO -->
            <div class="bg-slate-900 border ${isAccepted ? 'border-emerald-500/40 shadow-emerald-500/10' : 'border-amber-500/40 shadow-amber-500/10'} rounded-3xl p-6 sm:p-8 shadow-2xl text-center relative overflow-hidden">
                
                <div class="h-16 w-16 mx-auto rounded-2xl ${isAccepted ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'} flex items-center justify-center text-3xl mb-4">
                    ${isAccepted ? '✔' : '✕'}
                </div>

                <span class="text-[10px] uppercase tracking-widest font-extrabold ${isAccepted ? 'text-emerald-400 bg-emerald-500/10' : 'text-amber-400 bg-amber-500/10'} px-3 py-1 rounded-full border ${isAccepted ? 'border-emerald-500/20' : 'border-amber-500/20'}">
                    ${isAccepted ? 'OPERACIÓN CONFIRMADA' : 'DISPONIBILIDAD AGOTADA'}
                </span>

                <h1 class="text-2xl font-black text-white mt-3">
                    ${isAccepted ? '¡Reserva Asignada a ti!' : 'Reserva Liberada'}
                </h1>

                <p class="text-xs text-slate-300 mt-2 leading-relaxed">
                    ${isAccepted 
                        ? `Gracias, <strong>${operatorName}</strong>. El turista ya fue notificado de tu confirmación por WhatsApp y los datos del recojo quedaron sincronizados.`
                        : `Entendido, <strong>${operatorName}</strong>. El sistema reasignará la solicitud a otro operador disponible en Cusco.`
                    }
                </p>

                <div class="my-5 border-t border-slate-800"></div>

                <!-- DETALLES DE LA RESERVA -->
                <div class="bg-slate-950/80 rounded-2xl p-4 text-left space-y-2 text-xs border border-slate-800">
                    <div class="flex justify-between items-center">
                        <span class="text-slate-400">Código de Reserva:</span>
                        <span class="font-mono font-bold text-cyan-400">${id}</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span class="text-slate-400">Estado:</span>
                        <span class="font-bold ${isAccepted ? 'text-emerald-400' : 'text-amber-400'}">${isAccepted ? 'CONFIRMADO (En Ruta)' : 'RECHAZADO'}</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span class="text-slate-400">Fecha de confirmación:</span>
                        <span class="text-slate-200">${new Date().toLocaleString('es-PE', { timeZone: 'America/Lima' })}</span>
                    </div>
                </div>

                ${isAccepted ? `
                    <div class="mt-6 space-y-3">
                        <a href="https://wa.me/51958050928?text=Hola%20Central%20Lifextreme!%20He%20aceptado%20la%20reserva%20${id}.%20Quedo%20a%20la%20espera%20de%20los%20detalles%20de%20recojo." 
                           target="_blank"
                           class="w-full py-3.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/20 transition-all">
                            <span>📱 Contactar a Central de Despacho</span>
                        </a>
                    </div>
                ` : `
                    <div class="mt-6">
                        <a href="/" class="text-xs text-slate-400 hover:text-white underline">
                            Volver al portal Lifextreme
                        </a>
                    </div>
                `}

            </div>

        </div>

        <footer class="text-center text-[11px] text-slate-500 py-4">
            Lifextreme Web AI • Red Descentralizada de Operadores de Aventura en Cusco
        </footer>

    </body>
    </html>
    `;

    return res.status(200).send(htmlResponse);
}
