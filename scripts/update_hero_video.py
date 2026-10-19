hero_replacement = '''        <!-- HOME -->
        <section id="section-home" class="section-view active relative min-h-screen flex flex-col justify-center overflow-hidden pt-28 lg:pt-36 pb-12 lg:pb-24 bg-slate-950">
            <!-- 4K HERO VIDEO REEL BACKGROUND (RED BULL STYLE COSTA, SIERRA, SELVA & CULTURA ANCESTRAL) -->
            <div class="absolute inset-0 z-0 overflow-hidden pointer-events-none">
                <video id="hero-bg-video" autoplay loop muted playsinline class="w-full h-full object-cover">
                    <source src="assets/videos/hero_peru_adventure.mp4" type="video/mp4">
                    <source src="https://www.ficperu.online/videos/hero_video_ai.mp4" type="video/mp4">
                    Tu navegador no soporta videos HTML5.
                </video>
                <!-- Dark Cinema Gradient Overlay -->
                <div class="absolute inset-0 bg-slate-950/80 via-slate-950/65 to-slate-900/75"></div>
                <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent to-slate-950/60"></div>
            </div>

            <!-- FLOATING AUDIO TOGGLE (FICPERU STYLE) -->
            <button id="audio-toggle" type="button" onclick="window.toggleHeroAudio();"
                class="absolute top-24 right-4 sm:right-8 z-30 bg-slate-950/70 hover:bg-slate-900 backdrop-blur-md border border-white/20 text-white px-4 sm:px-5 py-2 sm:py-2.5 rounded-full flex items-center gap-2 transition-all shadow-2xl group cursor-pointer text-xs font-black uppercase tracking-wider">
                <i class="ri-volume-mute-line text-amber-400 text-base sm:text-lg group-hover:scale-110 transition-transform"></i>
                <span id="audio-text">Activar Sonido</span>
            </button>

            <div class="container mx-auto px-4 sm:px-6 relative z-10">
                <!-- RED BULL STYLE ADVENTURE CHAPTERS SELECTOR BAR -->
                <div class="mb-8 flex flex-wrap items-center justify-center lg:justify-start gap-2">
                    <div class="inline-flex items-center gap-2 bg-slate-900/80 backdrop-blur-md px-3.5 py-1.5 rounded-full border border-white/10 text-[9px] font-black uppercase tracking-widest text-amber-400 shadow-lg">
                        <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span> REEL 4K PERÚ
                    </div>
                    <div class="flex items-center gap-1.5 overflow-x-auto max-w-full pb-1 sm:pb-0">
                        <span class="bg-white/10 backdrop-blur-md text-white/90 px-3 py-1 rounded-full text-[9px] font-bold border border-white/10 flex items-center gap-1">
                            🏄 Costa: Surf & Dunas
                        </span>
                        <span class="bg-white/10 backdrop-blur-md text-white/90 px-3 py-1 rounded-full text-[9px] font-bold border border-white/10 flex items-center gap-1">
                            🏔️ Sierra: 6000m & Bungee
                        </span>
                        <span class="bg-white/10 backdrop-blur-md text-white/90 px-3 py-1 rounded-full text-[9px] font-bold border border-white/10 flex items-center gap-1">
                            🌴 Selva: Rápidos & Canyoning
                        </span>
                        <span class="bg-amber-400/20 backdrop-blur-md text-amber-300 px-3 py-1 rounded-full text-[9px] font-bold border border-amber-400/30 flex items-center gap-1">
                            🍲 Pachamanca & Ancestralidad
                        </span>
                    </div>
                </div>

                <div class="grid lg:grid-cols-2 gap-10 lg:gap-16 items-center mb-16 lg:mb-24">
                    <div class="text-center lg:text-left text-white">
                        <span data-i18n="hero_tag"
                            class="bg-amber-400/15 text-amber-300 px-4 py-2 rounded-full text-[9px] font-black uppercase tracking-[0.25em] mb-6 inline-block italic border border-amber-400/30 shadow-md">⚡ 164 Parques Auditados • Guías UIAGM • Costa, Sierra y Selva • IA Táctica 24/7</span>
                        <h1 class="text-4xl sm:text-5xl lg:text-6xl 2xl:text-7xl font-black text-white leading-[0.95] mb-6 tracking-tighter italic">
                            <span data-i18n="hero_title_1">Domina la Ruta.</span> <br>
                            <span data-i18n="hero_title_2" class="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-yellow-300 to-rose-400 pr-3 inline-block">Vive lo Inexplorado.</span>
                        </h1>
                        <p class="text-md lg:text-lg text-slate-300 font-medium mb-10 max-w-lg mx-auto lg:mx-0 leading-relaxed"
                            data-i18n="hero_desc">40 expediciones verificadas, 164 parques extremos y guías certificados UIAGM en costa, sierra y selva del Perú. Diseña tu misión con IA en 30 segundos y ahorra hasta 30% con el Club Lifextreme.</p>
                        <div class="flex flex-col sm:flex-row flex-wrap gap-3 sm:gap-4 justify-center lg:justify-start">
                            <button onclick="document.getElementById('home-destinos-container').scrollIntoView({behavior: 'smooth'})" data-i18n="btn_explore"
                                class="bg-gradient-to-r from-amber-400 to-yellow-500 hover:brightness-110 text-slate-950 px-8 py-4 sm:px-10 sm:py-5 rounded-3xl font-black uppercase text-[10px] tracking-widest shadow-2xl transition-all flex items-center justify-center gap-2 cursor-pointer">
                                Explorar Destinos <i class="ri-arrow-down-line"></i>
                            </button>
                            <button data-action="navigate" data-target="eventos" data-i18n="btn_events"
                                class="bg-white/10 hover:bg-white/20 text-white border border-white/20 px-8 py-4 sm:px-10 sm:py-5 rounded-3xl font-black uppercase text-[10px] tracking-widest transition-all cursor-pointer">
                                Ver Eventos
                            </button>
                            <button data-action="toggle-cart"
                                class="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 hover:bg-emerald-500 hover:text-white px-6 py-4 sm:py-5 rounded-3xl font-black uppercase text-[10px] tracking-widest transition-all flex items-center justify-center gap-2 cursor-pointer">
                                <i class="ri-shopping-cart-2-fill text-sm"></i> Mi Carrito
                            </button>
                        </div>
                        
                        <!-- Social Proof -->
                        <div class="mt-8 flex items-center justify-center lg:justify-start gap-4 mb-4">
                            <div class="flex -space-x-3">
                                <img class="w-10 h-10 rounded-full border-2 border-slate-800 object-cover shadow-sm" src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&fm=webp&q=80" alt="Aventurero 1">
                                <img class="w-10 h-10 rounded-full border-2 border-slate-800 object-cover shadow-sm" src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&fm=webp&q=80" alt="Aventurero 2">
                                <img class="w-10 h-10 rounded-full border-2 border-slate-800 object-cover shadow-sm" src="https://images.unsplash.com/photo-1517841905240-472988babdf9?w=100&fm=webp&q=80" alt="Aventurero 3">
                                <img class="w-10 h-10 rounded-full border-2 border-slate-800 object-cover shadow-sm" src="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&fm=webp&q=80" alt="Aventurero 4">
                                <div class="w-10 h-10 rounded-full border-2 border-slate-800 bg-slate-800 flex items-center justify-center text-[8px] font-black text-amber-400 shadow-sm">+15k</div>
                            </div>
                            <div class="text-[10px] font-black text-slate-300 uppercase tracking-widest leading-tight text-left">
                                Aventureros Activos<br><span class="text-yellow-400">⭐⭐⭐⭐⭐ 4.9/5</span>
                            </div>
                        </div>

                        <div class="mt-6 flex flex-col sm:flex-row items-stretch sm:items-center justify-center lg:justify-start gap-3">
                            <button data-action="open-quiz"
                                class="flex items-center gap-3 bg-white/10 backdrop-blur-md px-5 py-3 rounded-2xl border border-white/15 hover:bg-white/20 transition-all group cursor-pointer text-left">
                                <i class="ri-survey-line text-amber-400 text-xl"></i>
                                <div>
                                    <p class="text-[9px] font-black text-amber-400 uppercase tracking-widest" data-i18n="quiz_prompt">¿No sabes qué elegir?</p>
                                    <p class="text-[10px] font-black text-white" data-i18n="quiz_desc">Haz el Test de Aventura y gana -10%</p>
                                </div>
                                <i class="ri-arrow-right-s-line text-slate-400 group-hover:translate-x-1 transition-all ml-auto"></i>
                            </button>

                            <a href="recompensas.html"
                                class="flex items-center gap-3 bg-gradient-to-r from-amber-500/20 to-yellow-500/10 backdrop-blur-md px-5 py-3 rounded-2xl border border-amber-400/30 hover:border-amber-400 transition-all group cursor-pointer text-left">
                                <div class="w-9 h-9 rounded-xl bg-amber-400/20 flex items-center justify-center text-amber-400 shrink-0">
                                    <i class="ri-coin-fill text-xl group-hover:rotate-12 transition-transform"></i>
                                </div>
                                <div>
                                    <p class="text-[9px] font-black text-amber-400 uppercase tracking-widest">Billetera Lifecoins</p>
                                    <p class="text-[10px] font-black text-white">800 Coins • Canjea Descuentos</p>
                                </div>
                                <i class="ri-arrow-right-s-line text-amber-400 group-hover:translate-x-1 transition-all ml-auto"></i>
                            </a>
                        </div>
                    </div>

                    <!-- HERO STATIC BANNER (SOCIAL EXPEDITIONS) -->
                    <div class="relative rounded-[36px] sm:rounded-[48px] overflow-hidden shadow-2xl group cursor-pointer h-[440px] sm:h-[500px] lg:h-[580px] border border-white/10 bg-slate-900"
                        onclick="window.location.href='community.html'">
                        <!-- Image -->
                        <div class="absolute inset-0">
                            <img src="https://images.unsplash.com/photo-1551632811-561732d1e306?w=1200&fm=webp&q=80"
                                alt="Equipo de Expedición Social de Lifextreme en la montaña" width="1200" height="600"
                                fetchpriority="high"
                                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-1000"
                                loading="eager">
                        </div>

                        <!-- Gradient Overlays -->
                        <div
                            class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-900/40 to-transparent opacity-85 group-hover:opacity-90 transition-opacity">
                        </div>
                        <div class="absolute inset-0 bg-gradient-to-r from-slate-950/60 to-transparent"></div>

                        <!-- Content -->
                        <div class="absolute bottom-0 left-0 w-full p-8 lg:p-12">
                            <!-- Badge -->
                            <div class="flex items-center gap-3 mb-6">
                                <span
                                    class="bg-accent text-slate-900 px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest shadow-[0_0_20px_rgba(255,191,0,0.5)] animate-pulse">
                                    🚀 Nuevo Lanzamiento
                                </span>
                                <span
                                    class="bg-white/10 backdrop-blur-md text-white px-3 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest border border-white/10">
                                    Beta Access
                                </span>
                            </div>

                            <!-- Title -->
                            <h3 class="text-4xl lg:text-6xl font-black italic text-white leading-[0.9] mb-6">
                                Social<br>
                                <span
                                    class="text-transparent bg-clip-text bg-gradient-to-r from-accent to-yellow-200">Expeditions</span>
                            </h3>

                            <!-- Description -->
                            <p
                                class="text-slate-300 text-sm lg:text-base font-medium max-w-md mb-8 leading-relaxed border-l-2 border-accent pl-4">
                                Olvida los tours privados impagables. Arma tu tribu, comparte gastos y accede a
                                logística profesional bajo demanda.
                            </p>

                            <!-- CTA Button -->
                            <button
                                class="bg-white text-slate-900 px-8 py-4 rounded-2xl text-[10px] lg:text-xs font-black uppercase tracking-widest group-hover:bg-accent group-hover:scale-105 transition-all shadow-xl flex items-center gap-3">
                                <span>Ver Proyecto</span>
                                <i class="ri-arrow-right-line text-lg"></i>
                            </button>
                        </div>

                        <!-- Decorator Icon -->
                        <div
                            class="absolute top-8 right-8 w-16 h-16 bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 flex items-center justify-center group-hover:rotate-12 transition-transform">
                            <i class="ri-group-fill text-3xl text-white"></i>
                        </div>
                    </div>
                </div>'''

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
pattern = r'<!-- HOME -->\s*<section id="section-home".*?<!-- MÓDULO INTERACTIVO LIFECOINS'
replacement = hero_replacement + '\n\n                <!-- MÓDULO INTERACTIVO LIFECOINS'

new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
if count > 0:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated Hero in index.html with {count} match.")
else:
    print("Pattern not found for Hero in index.html.")
