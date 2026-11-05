import re

NEW_LOGO = """            <a href="#" onclick="navigateTo('home')" class="flex items-center group shrink-0" title="Lifextreme - Outdoor Experience">
                <!-- ISOTIPO RED NEURONAL DE AVENTURA (Cumbres Andinas + Sinapsis Inteligente) -->
                <div class="relative w-9 h-9 sm:w-10 sm:h-10 rounded-2xl bg-gradient-to-br from-amber-400 via-orange-500 to-rose-600 flex items-center justify-center text-slate-950 shadow-md shadow-orange-500/30 group-hover:scale-105 group-hover:shadow-orange-500/50 transition-all border border-amber-300/50 overflow-hidden">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" class="transition-transform group-hover:-translate-y-0.5 duration-300">
                        <!-- Facetas Poligonales de Montaña Translúcidas -->
                        <polygon points="12,2.8 5,10 12,16" fill="#ffffff" fill-opacity="0.30"/>
                        <polygon points="12,2.8 19,9.5 12,16" fill="#ffffff" fill-opacity="0.12"/>
                        <polygon points="5,10 2.5,20.5 12,16" fill="#ffffff" fill-opacity="0.22"/>
                        <polygon points="19,9.5 12,16 21.5,20.5" fill="#ffffff" fill-opacity="0.08"/>
                        
                        <!-- Red Neuronal / Aristas de Conexión de Alta Montaña -->
                        <path d="M12 2.8L2.5 20.5H21.5L12 2.8Z" stroke="#090d16" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>
                        <path d="M12 2.8V16M5 10L12 16L19 9.5M2.5 20.5L12 16L21.5 20.5" stroke="#090d16" stroke-width="1.3" stroke-linejoin="round" stroke-linecap="round"/>
                        
                        <!-- Nodos Sinápticos de la Red (Cumbres, Pases y Waypoints) -->
                        <circle cx="12" cy="2.8" r="2.2" fill="#ffffff" stroke="#090d16" stroke-width="1.3"/>
                        <circle cx="5" cy="10" r="1.5" fill="#ffffff" stroke="#090d16" stroke-width="1.1"/>
                        <circle cx="19" cy="9.5" r="1.5" fill="#ffffff" stroke="#090d16" stroke-width="1.1"/>
                        <circle cx="12" cy="16" r="2.0" fill="#fef08a" stroke="#090d16" stroke-width="1.2"/>
                        <circle cx="2.5" cy="20.5" r="1.2" fill="#ffffff" stroke="#090d16" stroke-width="1.0"/>
                        <circle cx="21.5" cy="20.5" r="1.2" fill="#ffffff" stroke="#090d16" stroke-width="1.0"/>
                    </svg>
                </div>
                <div class="logo-font ml-2.5 leading-none select-none">
                    <span class="text-slate-950 font-black text-base sm:text-lg lg:text-xl tracking-tight">LIFE</span><span
                        class="font-black text-base sm:text-lg lg:text-xl tracking-tighter italic pr-1 text-transparent bg-clip-text bg-gradient-to-r from-amber-500 via-orange-500 to-rose-600">XTREME</span>
                    <span class="block text-[6.5px] font-black uppercase tracking-[0.22em] text-slate-400 group-hover:text-amber-500 transition-colors">OUTDOOR EXPERIENCE</span>
                </div>
            </a>"""

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Pattern matching from <a href="#" onclick="navigateTo('home')" to </a>
pattern = r'(<a href="#" onclick="navigateTo\(\'home\'\)"[\s\S]*?Outdoor AI[\s\S]*?</a>)'
m = re.search(pattern, html)
if m:
    html = html[:m.start()] + NEW_LOGO + html[m.end():]
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("SUCCESS: index.html updated with OUTDOOR EXPERIENCE and Neural Adventure Mountain icon!")
else:
    print("ERROR: Pattern not found in index.html")
