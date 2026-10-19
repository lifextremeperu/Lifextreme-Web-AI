import re

socio_groups_html = '''                                <div id="perfil-socio-grp-1" class="socio-acc-panel px-5 pb-5 pt-3 border-t border-white/5 space-y-3">
                                    <p class="text-xs text-slate-300 font-semibold">
                                        Descuentos del <strong>15% al 25% OFF</strong> en equipamiento técnico de montaña, carpas y calzado en locales aliados mostrando tu Carnet Digital:
                                    </p>
                                    <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
                                        <div class="bg-slate-900/80 p-3.5 rounded-2xl border border-white/10 flex flex-col justify-between">
                                            <div>
                                                <div class="flex items-center justify-between mb-1">
                                                    <span class="text-[8px] font-black uppercase text-amber-400">Outdoor • Cusco</span>
                                                    <span class="bg-emerald-500/20 text-emerald-300 text-[8px] font-black px-2 py-0.5 rounded-full border border-emerald-500/30">-20% OFF</span>
                                                </div>
                                                <h5 class="text-white font-black text-xs">Tatoo Adventure Gear</h5>
                                                <p class="text-[10px] text-slate-400 mt-1 leading-snug">Calle Medio 130, Plaza de Armas, Cusco. Ropa técnica, carpas y mochilas.</p>
                                            </div>
                                            <div class="pt-2.5 mt-2 border-t border-white/5 flex items-center justify-between">
                                                <a href="https://maps.google.com/?q=Tatoo+Adventure+Gear+Cusco" target="_blank" rel="noopener" class="text-[9px] font-black text-amber-400 hover:underline flex items-center gap-1">
                                                    <i class="ri-map-pin-2-fill"></i> Ver en Google Maps
                                                </a>
                                            </div>
                                        </div>
                                        <div class="bg-slate-900/80 p-3.5 rounded-2xl border border-white/10 flex flex-col justify-between">
                                            <div>
                                                <div class="flex items-center justify-between mb-1">
                                                    <span class="text-[8px] font-black uppercase text-amber-400">Montañismo • Huaraz</span>
                                                    <span class="bg-emerald-500/20 text-emerald-300 text-[8px] font-black px-2 py-0.5 rounded-full border border-emerald-500/30">-25% OFF</span>
                                                </div>
                                                <h5 class="text-white font-black text-xs">Andean Outdoor Gear</h5>
                                                <p class="text-[10px] text-slate-400 mt-1 leading-snug">Av. Luzuriaga 872, Huaraz. Alquiler de piolets, crampones y botas plásticas.</p>
                                            </div>
                                            <div class="pt-2.5 mt-2 border-t border-white/5 flex items-center justify-between">
                                                <a href="https://maps.google.com/?q=Andean+Outdoor+Equipment+Huaraz" target="_blank" rel="noopener" class="text-[9px] font-black text-amber-400 hover:underline flex items-center gap-1">
                                                    <i class="ri-map-pin-2-fill"></i> Ver en Google Maps
                                                </a>
                                            </div>
                                        </div>
                                        <div class="bg-slate-900/80 p-3.5 rounded-2xl border border-white/10 flex flex-col justify-between">
                                            <div>
                                                <div class="flex items-center justify-between mb-1">
                                                    <span class="text-[8px] font-black uppercase text-amber-400">Equipamiento • Lima</span>
                                                    <span class="bg-emerald-500/20 text-emerald-300 text-[8px] font-black px-2 py-0.5 rounded-full border border-emerald-500/30">-15% OFF</span>
                                                </div>
                                                <h5 class="text-white font-black text-xs">The North Face Miraflores</h5>
                                                <p class="text-[10px] text-slate-400 mt-1 leading-snug">Av. Larco 812, Miraflores, Lima. Indumentaria térmica y casacas de pluma.</p>
                                            </div>
                                            <div class="pt-2.5 mt-2 border-t border-white/5 flex items-center justify-between">
                                                <a href="https://maps.google.com/?q=The+North+Face+Miraflores+Lima" target="_blank" rel="noopener" class="text-[9px] font-black text-amber-400 hover:underline flex items-center gap-1">
                                                    <i class="ri-map-pin-2-fill"></i> Ver en Google Maps
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Grupo 2 -->
                            <div class="socio-acc-item rounded-2xl bg-slate-800/60 border border-white/10 transition-all overflow-hidden">
                                <button type="button" onclick="window.toggleSocioModule(this, 'perfil-socio-grp-2')"
                                    class="socio-acc-btn w-full flex items-center justify-between gap-4 p-4 text-left cursor-pointer">
                                    <div class="flex items-center gap-3">
                                        <div class="socio-acc-badge w-11 h-11 rounded-xl bg-slate-700/60 text-slate-300 flex items-center justify-center shrink-0">
                                            <i class="ri-medal-fill text-xl"></i>
                                        </div>
                                        <div>
                                            <span class="text-[9px] font-black uppercase tracking-widest text-slate-400 block">Grupo 2</span>
                                            <h4 class="socio-acc-title text-slate-200 text-xs sm:text-sm font-black uppercase">Cursos, Eventos, Biblioteca y Concursos</h4>
                                        </div>
                                    </div>
                                    <i class="ri-arrow-down-s-line text-xl text-slate-400 socio-acc-arrow transition-transform"></i>
                                </button>
                                <div id="perfil-socio-grp-2" class="socio-acc-panel hidden px-5 pb-5 pt-3 border-t border-white/5 space-y-3">
                                    <p class="text-xs text-slate-300 font-semibold">
                                        Formación técnica certificada y acceso prioritario con descuento a parques de adrenalina en Perú:
                                    </p>
                                    <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
                                        <div class="bg-slate-900/80 p-3.5 rounded-2xl border border-white/10 flex flex-col justify-between">
                                            <div>
                                                <div class="flex items-center justify-between mb-1">
                                                    <span class="text-[8px] font-black uppercase text-amber-400">Escuela Montaña • Huaraz</span>
                                                    <span class="bg-emerald-500/20 text-emerald-300 text-[8px] font-black px-2 py-0.5 rounded-full border border-emerald-500/30">-30% OFF</span>
                                                </div>
                                                <h5 class="text-white font-black text-xs">Escuela Guías AGMP</h5>
                                                <p class="text-[10px] text-slate-400 mt-1 leading-snug">Parque Ginebra 28, Huaraz. Talleres de rescate en grietas, orientación y nudos.</p>
                                            </div>
                                            <div class="pt-2.5 mt-2 border-t border-white/5 flex items-center justify-between">
                                                <a href="https://maps.google.com/?q=AGMP+Huaraz" target="_blank" rel="noopener" class="text-[9px] font-black text-amber-400 hover:underline flex items-center gap-1">
                                                    <i class="ri-map-pin-2-fill"></i> Ver en Google Maps
                                                </a>
                                            </div>
                                        </div>
                                        <div class="bg-slate-900/80 p-3.5 rounded-2xl border border-white/10 flex flex-col justify-between">
                                            <div>
                                                <div class="flex items-center justify-between mb-1">
                                                    <span class="text-[8px] font-black uppercase text-amber-400">Bungee & Canopy • Cusco</span>
                                                    <span class="bg-emerald-500/20 text-emerald-300 text-[8px] font-black px-2 py-0.5 rounded-full border border-emerald-500/30">-25% OFF</span>
                                                </div>
                                                <h5 class="text-white font-black text-xs">Action Valley Poroy</h5>
                                                <p class="text-[10px] text-slate-400 mt-1 leading-snug">Km 11 Carretera Poroy, Cusco. Bungee Jumping 122m y Slingshot más alto de Sudamérica.</p>
                                            </div>
                                            <div class="pt-2.5 mt-2 border-t border-white/5 flex items-center justify-between">
                                                <a href="https://maps.google.com/?q=Action+Valley+Cusco" target="_blank" rel="noopener" class="text-[9px] font-black text-amber-400 hover:underline flex items-center gap-1">
                                                    <i class="ri-map-pin-2-fill"></i> Ver en Google Maps
                                                </a>
                                            </div>
                                        </div>
                                        <div class="bg-slate-900/80 p-3.5 rounded-2xl border border-white/10 flex flex-col justify-between">
                                            <div>
                                                <div class="flex items-center justify-between mb-1">
                                                    <span class="text-[8px] font-black uppercase text-amber-400">Rafting • Urubamba</span>
                                                    <span class="bg-emerald-500/20 text-emerald-300 text-[8px] font-black px-2 py-0.5 rounded-full border border-emerald-500/30">-20% OFF</span>
                                                </div>
                                                <h5 class="text-white font-black text-xs">Apurímac River Base</h5>
                                                <p class="text-[10px] text-slate-400 mt-1 leading-snug">Puente Chuquicahuana, Cusco. Clínicas de rescate en aguas blancas y kayak.</p>
                                            </div>
                                            <div class="pt-2.5 mt-2 border-t border-white/5 flex items-center justify-between">
                                                <a href="https://maps.google.com/?q=Rio+Apurimac+Cusco" target="_blank" rel="noopener" class="text-[9px] font-black text-amber-400 hover:underline flex items-center gap-1">
                                                    <i class="ri-map-pin-2-fill"></i> Ver en Google Maps
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Grupo 3 -->
                            <div class="socio-acc-item rounded-2xl bg-slate-800/60 border border-white/10 transition-all overflow-hidden">
                                <button type="button" onclick="window.toggleSocioModule(this, 'perfil-socio-grp-3')"
                                    class="socio-acc-btn w-full flex items-center justify-between gap-4 p-4 text-left cursor-pointer">
                                    <div class="flex items-center gap-3">
                                        <div class="socio-acc-badge w-11 h-11 rounded-xl bg-slate-700/60 text-slate-300 flex items-center justify-center shrink-0">
                                            <i class="ri-hotel-bed-fill text-xl"></i>
                                        </div>
                                        <div>
                                            <span class="text-[9px] font-black uppercase tracking-widest text-slate-400 block">Grupo 3</span>
                                            <h4 class="socio-acc-title text-slate-200 text-xs sm:text-sm font-black uppercase">Hospedajes, Restaurantes y Tiendas Especializadas</h4>
                                        </div>
                                    </div>
                                    <i class="ri-arrow-down-s-line text-xl text-slate-400 socio-acc-arrow transition-transform"></i>
                                </button>
                                <div id="perfil-socio-grp-3" class="socio-acc-panel hidden px-5 pb-5 pt-3 border-t border-white/5 space-y-3">
                                    <p class="text-xs text-slate-300 font-semibold">
                                        Descansa y recarga energías con tarifas preferenciales y descuentos en cocina andina de autor:
                                    </p>
                                    <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
                                        <div class="bg-slate-900/80 p-3.5 rounded-2xl border border-white/10 flex flex-col justify-between">
                                            <div>
                                                <div class="flex items-center justify-between mb-1">
                                                    <span class="text-[8px] font-black uppercase text-amber-400">Hostel & Eco-Stay • Cusco</span>
                                                    <span class="bg-emerald-500/20 text-emerald-300 text-[8px] font-black px-2 py-0.5 rounded-full border border-emerald-500/30">-20% OFF</span>
                                                </div>
                                                <h5 class="text-white font-black text-xs">Pariwana Hostel Cusco</h5>
                                                <p class="text-[10px] text-slate-400 mt-1 leading-snug">Mesón de la Estrella 136, Cusco. Camas confort, desayuno energético y guardamochilas.</p>
                                            </div>
                                            <div class="pt-2.5 mt-2 border-t border-white/5 flex items-center justify-between">
                                                <a href="https://maps.google.com/?q=Pariwana+Hostel+Cusco" target="_blank" rel="noopener" class="text-[9px] font-black text-amber-400 hover:underline flex items-center gap-1">
                                                    <i class="ri-map-pin-2-fill"></i> Ver en Google Maps
                                                </a>
                                            </div>
                                        </div>
                                        <div class="bg-slate-900/80 p-3.5 rounded-2xl border border-white/10 flex flex-col justify-between">
                                            <div>
                                                <div class="flex items-center justify-between mb-1">
                                                    <span class="text-[8px] font-black uppercase text-amber-400">Eco-Lodge • Huaraz</span>
                                                    <span class="bg-emerald-500/20 text-emerald-300 text-[8px] font-black px-2 py-0.5 rounded-full border border-emerald-500/30">-15% OFF</span>
                                                </div>
                                                <h5 class="text-white font-black text-xs">Llanganuco Mountain Lodge</h5>
                                                <p class="text-[10px] text-slate-400 mt-1 leading-snug">Quebrada Llanganuco, Yungay. Cabañas ecológicas con vista panorámica al Huascarán.</p>
                                            </div>
                                            <div class="pt-2.5 mt-2 border-t border-white/5 flex items-center justify-between">
                                                <a href="https://maps.google.com/?q=Llanganuco+Mountain+Lodge" target="_blank" rel="noopener" class="text-[9px] font-black text-amber-400 hover:underline flex items-center gap-1">
                                                    <i class="ri-map-pin-2-fill"></i> Ver en Google Maps
                                                </a>
                                            </div>
                                        </div>
                                        <div class="bg-slate-900/80 p-3.5 rounded-2xl border border-white/10 flex flex-col justify-between">
                                            <div>
                                                <div class="flex items-center justify-between mb-1">
                                                    <span class="text-[8px] font-black uppercase text-amber-400">Gastronomía Andina • Cusco</span>
                                                    <span class="bg-emerald-500/20 text-emerald-300 text-[8px] font-black px-2 py-0.5 rounded-full border border-emerald-500/30">-15% OFF</span>
                                                </div>
                                                <h5 class="text-white font-black text-xs">Morena Peruvian Kitchen</h5>
                                                <p class="text-[10px] text-slate-400 mt-1 leading-snug">Calle Plateros 348, Cusco. Platos andinos ancestrales, pachamanca y postres artesanales.</p>
                                            </div>
                                            <div class="pt-2.5 mt-2 border-t border-white/5 flex items-center justify-between">
                                                <a href="https://maps.google.com/?q=Morena+Peruvian+Kitchen+Cusco" target="_blank" rel="noopener" class="text-[9px] font-black text-amber-400 hover:underline flex items-center gap-1">
                                                    <i class="ri-map-pin-2-fill"></i> Ver en Google Maps
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Grupo 4 -->
                            <div class="socio-acc-item rounded-2xl bg-slate-800/60 border border-white/10 transition-all overflow-hidden">
                                <button type="button" onclick="window.toggleSocioModule(this, 'perfil-socio-grp-4')"
                                    class="socio-acc-btn w-full flex items-center justify-between gap-4 p-4 text-left cursor-pointer">
                                    <div class="flex items-center gap-3">
                                        <div class="socio-acc-badge w-11 h-11 rounded-xl bg-slate-700/60 text-slate-300 flex items-center justify-center shrink-0">
                                            <i class="ri-heart-pulse-fill text-xl"></i>
                                        </div>
                                        <div>
                                            <span class="text-[9px] font-black uppercase tracking-widest text-slate-400 block">Grupo 4</span>
                                            <h4 class="socio-acc-title text-slate-200 text-xs sm:text-sm font-black uppercase">Salud, Gimnasios y Palestras</h4>
                                        </div>
                                    </div>
                                    <i class="ri-arrow-down-s-line text-xl text-slate-400 socio-acc-arrow transition-transform"></i>
                                </button>
                                <div id="perfil-socio-grp-4" class="socio-acc-panel hidden px-5 pb-5 pt-3 border-t border-white/5 space-y-3">
                                    <p class="text-xs text-slate-300 font-semibold">
                                        Entrenamiento de escalada, acondicionamiento físico y terapia de recuperación post-expedición:
                                    </p>
                                    <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
                                        <div class="bg-slate-900/80 p-3.5 rounded-2xl border border-white/10 flex flex-col justify-between">
                                            <div>
                                                <div class="flex items-center justify-between mb-1">
                                                    <span class="text-[8px] font-black uppercase text-amber-400">Escalada • Lima</span>
                                                    <span class="bg-emerald-500/20 text-emerald-300 text-[8px] font-black px-2 py-0.5 rounded-full border border-emerald-500/30">-25% OFF</span>
                                                </div>
                                                <h5 class="text-white font-black text-xs">Pirqa Climbing Gym</h5>
                                                <p class="text-[10px] text-slate-400 mt-1 leading-snug">Calle José Gálvez 360, Miraflores, Lima. Pases diarios, boulder y vías con auto-asegurador.</p>
                                            </div>
                                            <div class="pt-2.5 mt-2 border-t border-white/5 flex items-center justify-between">
                                                <a href="https://maps.google.com/?q=Pirqa+Climbing+Gym+Miraflores" target="_blank" rel="noopener" class="text-[9px] font-black text-amber-400 hover:underline flex items-center gap-1">
                                                    <i class="ri-map-pin-2-fill"></i> Ver en Google Maps
                                                </a>
                                            </div>
                                        </div>
                                        <div class="bg-slate-900/80 p-3.5 rounded-2xl border border-white/10 flex flex-col justify-between">
                                            <div>
                                                <div class="flex items-center justify-between mb-1">
                                                    <span class="text-[8px] font-black uppercase text-amber-400">Boulder • Cusco</span>
                                                    <span class="bg-emerald-500/20 text-emerald-300 text-[8px] font-black px-2 py-0.5 rounded-full border border-emerald-500/30">-30% OFF</span>
                                                </div>
                                                <h5 class="text-white font-black text-xs">7a Boulder Gym Cusco</h5>
                                                <p class="text-[10px] text-slate-400 mt-1 leading-snug">Av. Huayruropata 1412, Cusco. Palestra deportiva, campus board y zona de acondicionamiento.</p>
                                            </div>
                                            <div class="pt-2.5 mt-2 border-t border-white/5 flex items-center justify-between">
                                                <a href="https://maps.google.com/?q=7a+Boulder+Cusco" target="_blank" rel="noopener" class="text-[9px] font-black text-amber-400 hover:underline flex items-center gap-1">
                                                    <i class="ri-map-pin-2-fill"></i> Ver en Google Maps
                                                </a>
                                            </div>
                                        </div>
                                        <div class="bg-slate-900/80 p-3.5 rounded-2xl border border-white/10 flex flex-col justify-between">
                                            <div>
                                                <div class="flex items-center justify-between mb-1">
                                                    <span class="text-[8px] font-black uppercase text-amber-400">Fisioterapia • Cusco</span>
                                                    <span class="bg-emerald-500/20 text-emerald-300 text-[8px] font-black px-2 py-0.5 rounded-full border border-emerald-500/30">-35% OFF</span>
                                                </div>
                                                <h5 class="text-white font-black text-xs">Fisioterapia Andina & Oxígeno</h5>
                                                <p class="text-[10px] text-slate-400 mt-1 leading-snug">Av. de la Cultura 708, Cusco. Descarga muscular, masaje deportivo y cámara hiperbárica.</p>
                                            </div>
                                            <div class="pt-2.5 mt-2 border-t border-white/5 flex items-center justify-between">
                                                <a href="https://maps.google.com/?q=Fisioterapia+Deportiva+Cusco" target="_blank" rel="noopener" class="text-[9px] font-black text-amber-400 hover:underline flex items-center gap-1">
                                                    <i class="ri-map-pin-2-fill"></i> Ver en Google Maps
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>'''

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = r'<div id="perfil-socio-grp-1".*?<!-- Pasos de Inscripción y Costos -->'
replacement = socio_groups_html + '\n\n                            <!-- Pasos de Inscripción y Costos -->'

new_html, count = re.subn(pattern, replacement, html, flags=re.DOTALL)
if count > 0:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"Successfully updated index.html with {count} matches.")
else:
    print("Pattern not found in index.html.")
