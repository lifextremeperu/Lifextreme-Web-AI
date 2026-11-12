# optimize_mobile_header.py
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Optimizar barra superior del header (línea 899 a 988 aprox)
# Haremos que el Lifecoins badge, selector de idioma y moneda se oculten en pantallas móviles muy pequeñas
# o se integren perfectamente en el menú desplegable móvil.
# El botón de hamburguesa (las 3 líneas) será SIEMPRE visible, destacado y accesible en móviles (z-[3000]).

target_header = """            <div class="flex items-center gap-1.5 sm:gap-2.5 shrink-0">
                <!-- COIN WALLET WIDGET (ABRE MÓDULO LIFECOINS) -->
                <button type="button" onclick="openLifecoinsModal()"
                    class="hidden sm:flex items-center gap-1.5 bg-amber-100/80 hover:bg-amber-400/30 px-2.5 py-1.5 rounded-xl transition-all border border-amber-300 shadow-sm group shrink-0 cursor-pointer"
                    title="Ver Mis Recompensas y Canjear Lifecoins">
                    <i class="ri-coin-fill text-amber-500 group-hover:rotate-12 transition-transform text-base sm:text-lg"></i>
                    <div class="leading-none text-left">
                        <p class="hidden sm:block text-[7px] font-black text-amber-700 uppercase tracking-widest">Lifecoins</p>
                        <span class="text-[10px] sm:text-[11px] font-black text-slate-900" id="nav-coin-balance">800</span>
                    </div>
                </button>

                <div class="hidden md:flex items-center gap-2 cursor-pointer hover:bg-slate-50 px-2 py-1 rounded-xl transition-all shrink-0"
                    data-action="navigate" data-target="socio">
                    <div class="text-right leading-none hidden lg:block">
                        <p class="text-[7px] font-black text-primary uppercase" data-i18n="user_status">Socio Elite</p>
                        <p class="text-[11px] font-black text-slate-900">Alex R.</p>
                    </div>
                    <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=120&fm=webp&q=80"
                        alt="Avatar Alex R." width="36" height="36"
                        class="w-9 h-9 rounded-xl object-cover border border-slate-200 shadow-sm" loading="lazy">
                </div>

                <!-- SINGLE LANGUAGE DROPDOWN SELECTOR (DESKTOP / TABLET) -->
                <div class="relative hidden sm:block" id="lang-dropdown-wrapper" style="position:relative;">
                    <button type="button" id="lang-dropdown-btn"
                        onclick="event.stopPropagation(); var m=document.getElementById('lang-dropdown-menu'); if(m){ var open=(m.style.display==='none'||m.classList.contains('hidden')); m.classList.toggle('hidden', !open); m.style.display=open?'block':'none'; }"
                        class="flex items-center gap-1.5 bg-white hover:bg-slate-50 px-2 py-1.5 sm:px-2.5 sm:py-2 rounded-xl shadow-sm border border-slate-200 hover:border-primary/40 transition-all cursor-pointer text-[10px] font-black uppercase tracking-wider text-slate-700"
                        title="Seleccionar Idioma">
                        <i class="ri-global-line text-primary text-sm"></i>
                        <span id="current-lang-label">🇪🇸 ES</span>
                        <i class="ri-arrow-down-s-line text-xs text-slate-400"></i>
                    </button>
                    <div id="lang-dropdown-menu"
                        style="display:none; position:absolute; right:0; top:calc(100% + 8px); width:176px; z-index:9999; background:#ffffff; border-radius:16px; box-shadow:0 20px 40px rgba(15,23,42,0.18); border:1px solid #e2e8f0; padding:6px;"
                        class="hidden">
                        <button type="button" id="lang-es" onclick="event.stopPropagation(); localStorage.setItem('lifextreme_lang','es'); document.getElementById('lang-dropdown-menu').style.display='none'; if(window.setLanguage) setLanguage('es');"
                            class="w-full px-3.5 py-2.5 rounded-xl text-left text-[11px] font-black uppercase tracking-wider flex items-center justify-between hover:bg-indigo-50 text-primary bg-indigo-50/70 transition-colors cursor-pointer">
                            <span>🇪🇸 Español</span>
                            <span class="text-[9px] font-bold opacity-70">ES</span>
                        </button>
                        <button type="button" id="lang-en" onclick="event.stopPropagation(); localStorage.setItem('lifextreme_lang','en'); window.location.href='/en/' + window.location.hash;"
                            class="w-full px-3.5 py-2.5 rounded-xl text-left text-[11px] font-black uppercase tracking-wider flex items-center justify-between hover:bg-indigo-50 text-slate-700 transition-colors cursor-pointer">
                            <span>🇺🇸 English</span>
                            <span class="text-[9px] font-bold opacity-70">EN</span>
                        </button>
                        <button type="button" id="lang-pt" onclick="event.stopPropagation(); localStorage.setItem('lifextreme_lang','pt'); window.location.href='/pt/' + window.location.hash;"
                            class="w-full px-3.5 py-2.5 rounded-xl text-left text-[11px] font-black uppercase tracking-wider flex items-center justify-between hover:bg-indigo-50 text-slate-700 transition-colors cursor-pointer">
                            <span>🇧🇷 Português</span>
                            <span class="text-[9px] font-bold opacity-70">PT</span>
                        </button>
                    </div>
                </div>

                <!-- CURRENCY SELECTOR (DESKTOP / TABLET) -->
                <div class="hidden sm:flex items-center bg-slate-50 rounded-xl px-1.5 py-1.5 shadow-inner border border-slate-200/80 shrink-0">
                    <select id="currency-selector" aria-label="Moneda" onchange="window.handleCurrencyChange(this.value);" class="bg-transparent text-[10px] font-black uppercase tracking-wider text-slate-700 outline-none cursor-pointer pr-0.5">
                        <option value="PEN">S/ PEN</option>
                        <option value="USD">$ USD</option>
                        <option value="BRL">R$ BRL</option>
                    </select>
                </div>

                <!-- PROMINENT SHOPPING CART BUTTON (WEB & MOBILE) -->
                <button data-action="toggle-cart" id="header-cart-btn"
                    title="Abrir Carrito / Mochila Táctica"
                    class="bg-primary hover:bg-slate-900 text-white px-2.5 py-2 sm:px-3.5 sm:py-2 rounded-xl flex items-center gap-1.5 relative shadow-md shadow-primary/25 transition-all cursor-pointer shrink-0">
                    <i class="ri-shopping-cart-2-fill text-base sm:text-lg"></i>
                    <span class="hidden md:inline text-[10px] font-black uppercase tracking-wider">Carrito</span>
                    <span id="cart-count"
                        class="bg-accent text-slate-900 text-[10px] font-black rounded-full min-w-[18px] h-[18px] px-1 flex items-center justify-center shadow-sm">0</span>
                </button>

                <!-- BOTÓN DE 3 LÍNEAS (HAMBURGUESA MÓVIL DESTACADO) -->
                <button data-action="toggle-mobile-menu" aria-label="Abrir Menú Principal"
                    class="xl:hidden w-10 h-10 bg-slate-900 hover:bg-slate-800 text-white rounded-xl flex items-center justify-center shadow-md border border-slate-700 relative z-[2000] shrink-0 cursor-pointer active:scale-95 transition-all">
                    <i class="ri-menu-4-line text-xl"></i>
                </button>
            </div>"""

# 2. Mejorar el mobile-menu desplegable con cabecera propia, botón de cerrar (X), idioma y todos los módulos
old_mobile_menu_start = '<div id="mobile-menu"\n        class="fixed inset-0 z-[1500] bg-white translate-x-full transition-transform duration-500 flex flex-col pt-24 pb-10 px-6 overflow-y-auto">'

new_mobile_menu_start = """<div id="mobile-menu"
        class="fixed inset-0 z-[2500] bg-white translate-x-full transition-transform duration-300 flex flex-col pt-4 pb-12 px-6 overflow-y-auto">
        
        <!-- Header superior del menú móvil con Logo y Botón Cerrar (X) -->
        <div class="flex items-center justify-between pb-4 mb-3 border-b border-slate-100">
            <div class="flex items-center gap-2">
                <span class="font-black italic text-xl tracking-tight text-slate-950">LIFEXTREME</span>
                <span class="px-2 py-0.5 rounded bg-primary text-white text-[9px] font-black uppercase">MENÚ</span>
            </div>
            <button data-action="toggle-mobile-menu" aria-label="Cerrar Menú"
                class="w-10 h-10 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 flex items-center justify-center cursor-pointer transition-colors">
                <i class="ri-close-line text-2xl font-bold"></i>
            </button>
        </div>

        <!-- Ajustes rápidos de Idioma y Moneda en móvil -->
        <div class="flex items-center justify-between bg-slate-50 p-3 rounded-2xl border border-slate-200/80 mb-3">
            <div class="flex items-center gap-2">
                <span class="text-xs font-black text-slate-500 uppercase">Idioma:</span>
                <button type="button" onclick="localStorage.setItem('lifextreme_lang','es'); if(window.setLanguage) setLanguage('es');" class="px-2 py-1 rounded-lg bg-white border border-slate-200 text-xs font-black text-primary">ES</button>
                <button type="button" onclick="localStorage.setItem('lifextreme_lang','en'); window.location.href='/en/' + window.location.hash;" class="px-2 py-1 rounded-lg bg-white border border-slate-200 text-xs font-bold text-slate-600">EN</button>
                <button type="button" onclick="localStorage.setItem('lifextreme_lang','pt'); window.location.href='/pt/' + window.location.hash;" class="px-2 py-1 rounded-lg bg-white border border-slate-200 text-xs font-bold text-slate-600">PT</button>
            </div>
            <div class="flex items-center gap-1.5">
                <span class="text-xs font-black text-slate-500 uppercase">Moneda:</span>
                <select onchange="window.handleCurrencyChange(this.value);" class="bg-white border border-slate-200 text-xs font-black rounded-lg px-2 py-1 text-slate-800">
                    <option value="PEN">S/ PEN</option>
                    <option value="USD">$ USD</option>
                    <option value="BRL">R$ BRL</option>
                </select>
            </div>
        </div>"""

# Replace in html
# Find current header block
h_start = html.find('<div class="flex items-center gap-1.5 sm:gap-2.5 shrink-0">')
h_end = html.find('</div>\n        </div>\n    </header>', h_start)
if h_start != -1 and h_end != -1:
    h_end += len('</div>')
    html = html[:h_start] + target_header + html[h_end:]
    print("Header right block replaced successfully.")
else:
    print("Warning: Header block delimiters not found.")

if old_mobile_menu_start in html:
    html = html.replace(old_mobile_menu_start, new_mobile_menu_start)
    print("Mobile menu start block replaced successfully.")
else:
    print("Warning: old_mobile_menu_start not found.")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html successfully updated.")
