/* LX NeuroMap · visor. Canvas 2D, sin dependencias. */
(() => {
const $ = s => document.querySelector(s);
const cv = $('#brain'), ctx = cv.getContext('2d');
const rc = $('#rc'), rctx = rc.getContext('2d');
const PALETTE = ['#8b7cf6', '#3a86ff', '#2dd4bf', '#f0b429', '#ef5b6b', '#f472b6', '#84cc16', '#fb923c', '#22d3ee', '#a78bfa', '#94a3b8'];

let brain = null, nodes = [], edges = [], agents = [], N = 0;
const nodeIndex = new Map();          // "coleccion|fuente" -> i
const typeColor = {}, centroids = [];
const lit = new Map();                // i -> {until, color}
const searchSet = new Set();
let pulses = [], floaters = [], timeline = [], learned = {agent_doc: [], doc_doc: []};
let cam = {x: 0, y: 0, s: 1}, W = 0, H = 0, dpr = 1, hover = -1, mouse = {x: 0, y: 0}, dragging = null;
const agentState = {};                // id -> {flash, color, last}

/* ───────────── utilidades ───────────── */
const fmt = n => n >= 1e6 ? (n / 1e6).toFixed(1) + ' M' : n >= 1e3 ? (n / 1e3).toFixed(n >= 1e4 ? 0 : 1) + ' k' : '' + n;
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const hex2rgba = (h, a) => { const n = parseInt(h.slice(1), 16); return `rgba(${n >> 16},${(n >> 8) & 255},${n & 255},${a})`; };
const decodeName = s => { let t = String(s); try { t = decodeURIComponent(t); } catch (e) {} return t.split(/[\\/]/).pop(); };
const AREA = {finanzas: 'Finanzas', operaciones: 'Operaciones', tecnologia: 'Tecnología', ceo: 'Estrategia CEO', ventas: 'Ventas', marketing: 'Marketing', alianzas: 'Alianzas'};
function family(n) {
  if (AREA[n.a]) return AREA[n.a];
  const ext = String(n.s).split('.').pop().toLowerCase();
  if (ext === 'md') return 'Fichas de destinos';
  if (ext === 'pdf') return 'PDFs de conocimiento';
  return 'Otros documentos';
}
const getJSON = u => fetch(u).then(r => r.json());

function resize() {
  dpr = Math.min(window.devicePixelRatio || 1, 2);
  W = innerWidth; H = innerHeight;
  cv.width = W * dpr; cv.height = H * dpr;
  const r = rc.getBoundingClientRect();
  rc.width = r.width * dpr; rc.height = r.height * dpr;
  fitCamera();
}
function fitCamera() {
  const left = 292, right = 366, top = 80, bottom = 160;
  const aw = W - left - right, ah = H - top - bottom;
  cam.s = Math.min(aw / 3.5, ah / 2.75);
  cam.x = left + aw / 2; cam.y = top + ah / 2;
}
const wx = x => cam.x + x * cam.s, wy = y => cam.y + y * cam.s;

/* ───────────── agentes ───────────── */
function agentPos(a) {
  const k = agents.indexOf(a), n = Math.max(agents.length, 1);
  const ang = -Math.PI / 2 + (2 * Math.PI * k) / n + 0.35;
  return {x: Math.cos(ang) * 1.5, y: Math.sin(ang) * 1.12};
}
const agentById = id => agents.find(a => a.id === id);
function ensureAgent(id) {
  let a = agentById(id);
  if (!a) { a = {id, label: id, icon: '··', color: '#8a93a6', impact: '-', role: '', note: '', stats: {}}; agents.push(a); renderAgents(); }
  return a;
}

function renderAgents() {
  const now = Date.now() / 1000;
  $('#agentList').innerHTML = agents.map(a => {
    const s = a.stats || {}, act = (now - (s.last || 0)) < 25;
    return `<div class="ag ${act ? 'act' : ''}" style="--c:${a.color}">
      <div class="h"><span class="ic">${esc(a.icon)}</span><b>${esc(a.label)}</b>
        <span class="tag ${a.impact === 'Alto' ? 'alto' : ''}">${esc(a.impact)}</span><span class="dot"></span></div>
      <div class="m"><span>🔎 ${s.searches || 0}</span><span>🧠 ${s.calls || 0}</span><span>⚡ ${fmt(s.tokens_h || 0)} tok/h</span></div>
      ${a.role ? `<div class="r">${esc(a.role)}</div>` : ''}
      ${a.note ? `<div class="w">⚠ ${esc(a.note)}</div>` : ''}</div>`;
  }).join('');
}

/* ───────────── carga de datos ───────────── */
async function load() {
  brain = await getJSON('/api/brain');
  nodes = brain.nodes || []; edges = brain.edges || []; N = nodes.length;
  nodes.forEach((n, i) => { nodeIndex.set(n.c + '|' + n.s, i); n.k = family(n); });
  // familias de documento ordenadas por tamaño -> color
  const fam = {};
  nodes.forEach(n => fam[n.k] = (fam[n.k] || 0) + 1);
  const famList = Object.entries(fam).sort((a, b) => b[1] - a[1]);
  famList.forEach(([k], i) => typeColor[k] = PALETTE[Math.min(i, PALETTE.length - 1)]);
  // etiquetas de región: centroide de las 7 familias más grandes
  const acc = {};
  nodes.forEach(n => { const a = acc[n.k] || (acc[n.k] = {x: 0, y: 0, k: 0}); a.x += n.x; a.y += n.y; a.k++; });
  famList.slice(0, 4).forEach(([k]) => { const a = acc[k]; centroids.push({t: k, x: a.x / a.k, y: a.y / a.k}); });
  const st = brain.stats || {};
  $('#stats').innerHTML = [
    [fmt(st.neurons || 0), 'neuronas'], [fmt(st.synapses || 0), 'sinapsis'],
    [fmt(st.vectors || 0), 'vectores'], [(st.empty_collections || []).length, 'colecc. vacías']
  ].map(([v, l]) => `<div><b>${v}</b><span>${l}</span></div>`).join('');
  $('#legend').innerHTML = famList.slice(0, 9).map(([k, c]) =>
    `<span><i style="background:${typeColor[k]}"></i>${esc(k)} · ${fmt(c)}</span>`).join('');
  agents = await getJSON('/api/agents');
  agents.forEach(a => agentState[a.id] = {flash: 0, color: a.color});
  renderAgents();
  const recent = await getJSON('/api/recent?seconds=600');
  recent.forEach(ev => { timeline.push(ev); });
  refreshFeedFromRecent(recent);
  loadLearned(); loadDoctor();
  setInterval(() => getJSON('/api/agents').then(list => {
    list.forEach(n => { const a = ensureAgent(n.id); a.stats = n.stats; });
    renderAgents();
  }), 5000);
  setInterval(loadLearned, 12000);
  setInterval(loadDoctor, 30000);
  openStream();
}

function refreshFeedFromRecent(list) {
  list.filter(e => ['qdrant_search', 'llm_call', 'error', 'agent_start', 'agent_end', 'qdrant_write'].includes(e.kind))
    .slice(-25).forEach(e => addFeed(e, true));
  updateBanner();
}

/* ───────────── tiempo real ───────────── */
function openStream() {
  const es = new EventSource('/api/stream');
  es.onmessage = m => { try { onEvent(JSON.parse(m.data)); } catch (e) {} };
}

function onEvent(ev) {
  const a = ensureAgent(ev.agent), st = agentState[a.id] || (agentState[a.id] = {flash: 0, color: a.color});
  a.stats = a.stats || {}; a.stats.last = ev.t;
  timeline.push(ev);
  st.flash = performance.now();
  if (ev.kind === 'qdrant_search') {
    (ev.docs || []).slice(0, 14).forEach((d, j) => {
      const i = nodeIndex.get(ev.collection + '|' + d.s);
      if (i === undefined) return;
      const from = agentPos(a), n = nodes[i];
      pulses.push({fx: from.x, fy: from.y, tx: n.x, ty: n.y, t0: performance.now() + j * 70, dur: 700 + Math.random() * 300, color: a.color, i});
    });
    floaters.push({dy: floaters.filter(f => f.agent === a).length * 14, agent: a, text: '🔎 ' + (ev.docs || []).length + ' docs', t0: performance.now(), color: a.color});
  } else if (ev.kind === 'llm_call') {
    floaters.push({dy: floaters.filter(f => f.agent === a).length * 14, agent: a, text: '🧠 ' + (ev.model || 'LLM') + (ev.tokens ? ' · ' + fmt(ev.tokens) + ' tok' : ''), t0: performance.now(), color: a.color});
  } else if (ev.kind === 'error') {
    floaters.push({dy: floaters.filter(f => f.agent === a).length * 14, agent: a, text: '⚠ error', t0: performance.now(), color: '#ef5b6b'});
  }
  addFeed(ev, false);
  updateBanner();
  if (ev.kind === 'qdrant_search') scheduleLearned();
}

let lTimer = null;
function scheduleLearned() { clearTimeout(lTimer); lTimer = setTimeout(loadLearned, 1500); }

function describe(ev) {
  const dem = ev.demo ? '<span class="chip">DEMO</span>' : '';
  switch (ev.kind) {
    case 'qdrant_search': return [`Buscó en <b>${esc(ev.collection)}</b> · ${(ev.docs || []).length} documentos${ev.ms ? ' · ' + ev.ms + ' ms' : ''}` + (ev.query ? `<br>“${esc(ev.query)}”` : ''), dem];
    case 'llm_call': return [`LLM <b>${esc(ev.model || '?')}</b> (${esc(ev.op)}) · ${ev.ms} ms${ev.tokens ? ' · ' + ev.tokens + ' tokens' : ''}`, dem];
    case 'qdrant_write': return [`Escribió ${ev.n == null ? '' : ev.n + ' '}vectores en <b>${esc(ev.collection)}</b>`, dem];
    case 'agent_start': return ['Arrancó', dem];
    case 'agent_end': return [`Terminó${ev.seconds != null ? ' en ' + ev.seconds + ' s' : ''}`, dem];
    case 'error': return [`Error en ${esc(ev.where)}: ${esc(ev.msg)}`, dem];
    default: return [esc(ev.kind), dem];
  }
}
function addFeed(ev, append) {
  if (!['qdrant_search', 'llm_call', 'error', 'agent_start', 'agent_end', 'qdrant_write'].includes(ev.kind)) return;
  const a = agentById(ev.agent) || {label: ev.agent, color: '#8a93a6'};
  const [txt, chip] = describe(ev);
  const el = document.createElement('div');
  el.className = 'ev' + (ev.kind === 'error' ? ' err' : '');
  el.innerHTML = `<div class="a"><i style="background:${a.color}"></i>${esc(a.label)}${chip}<span class="t">${new Date(ev.t * 1000).toLocaleTimeString()}</span></div><p>${txt}</p>`;
  const feed = $('#feed');
  feed.insertBefore(el, feed.firstChild);
  while (feed.children.length > 80) feed.removeChild(feed.lastChild);
}
function updateBanner() {
  const cut = Date.now() / 1000 - 600;
  $('#banner').hidden = !timeline.some(e => e.demo && e.t > cut);
  $('#empty').hidden = timeline.some(e => e.t > cut) || !!Object.keys(lit).length;
}

/* ───────────── paneles ───────────── */
async function loadLearned() {
  learned = await getJSON('/api/learned');
  const rows = learned.agent_doc.slice(0, 14).map(r => {
    const a = agentById(r.agent) || {label: r.agent, color: '#8a93a6'}, n = nodes[r.n];
    return n ? `<div class="lrow"><i style="color:${a.color}">●</i><span>${esc(a.label)} → ${esc(decodeName(n.s).slice(0, 42))}</span><span class="w">${r.w}</span></div>` : '';
  }).join('');
  const pairs = learned.doc_doc.slice(0, 8).map(r => {
    const A = nodes[r.a], B = nodes[r.b];
    return A && B ? `<div class="lrow"><span>${esc(decodeName(A.s).slice(0, 22))} ⇄ ${esc(decodeName(B.s).slice(0, 22))}</span><span class="w">${r.w}</span></div>` : '';
  }).join('');
  $('#tab-learned').innerHTML = `<p class="muted" style="margin-bottom:10px">Lo que se usa junto se conecta; lo que no se repite se olvida (a la mitad cada 14 días). Búsquedas registradas: <b>${learned.searches}</b>.</p>
    <h3 class="muted" style="font-size:11px;margin:8px 0">AGENTE → DOCUMENTO QUE MÁS USA</h3>${rows || '<p class="muted">Aún no hay historial.</p>'}
    <h3 class="muted" style="font-size:11px;margin:14px 0 8px">DOCUMENTOS QUE APARECEN JUNTOS</h3>${pairs || '<p class="muted">Aún no hay historial.</p>'}`;
}
async function loadDoctor() {
  const d = await getJSON('/api/doctor');
  const col = d.score >= 80 ? '#34d399' : d.score >= 55 ? '#f0b429' : '#ef5b6b';
  const lc = {alto: '#ef5b6b', medio: '#f0b429', bajo: '#8b7cf6', info: '#5a6384'};
  $('#tab-doctor').innerHTML = `<div class="score"><div class="ring" style="--p:${d.score};--sc:${col}"><span>${d.score}</span></div>
    <div><b>Salud del cerebro</b><br><span class="muted">${d.issues.filter(i => i.level !== 'info').length} puntos a revisar</span></div></div>` +
    d.issues.map(i => `<div class="iss" style="--lc:${lc[i.level]}"><b>${esc(i.title)}</b><span>${esc(i.detail)}</span></div>`).join('');
}

/* ───────────── búsqueda ───────────── */
$('#searchForm').addEventListener('submit', async e => {
  e.preventDefault();
  const q = $('#q').value.trim(); if (!q) return;
  switchTab('search');
  $('#tab-search').innerHTML = '<p class="muted">Consultando al cerebro…</p>';
  const r = await getJSON('/api/search?q=' + encodeURIComponent(q));
  if (r.error) { $('#tab-search').innerHTML = `<p class="muted">${esc(r.error)}</p>`; return; }
  searchSet.clear(); r.hits.forEach(h => searchSet.add(h.i));
  $('#tab-search').innerHTML = `<p class="muted" style="margin-bottom:8px">${r.hits.length} documentos relacionados con «${esc(q)}»</p>` +
    r.hits.map(h => { const n = nodes[h.i]; return `<div class="hit" data-i="${h.i}"><b>${esc(decodeName(h.s))}</b><span>${esc(n.k)} · ${esc(n.c)} · afinidad ${h.sc}</span></div>`; }).join('');
  document.querySelectorAll('.hit').forEach(el => el.onclick = () => focusNode(+el.dataset.i));
});
$('#clearSearch').onclick = () => { searchSet.clear(); $('#q').value = ''; };
function focusNode(i) { const n = nodes[i]; cam.s = Math.min(cam.s * 1.0, 900); cam.x = (W - 366 + 292) / 2 - n.x * cam.s; cam.y = (H - 160 + 80) / 2 - n.y * cam.s; }

function switchTab(t) {
  document.querySelectorAll('#tabs button').forEach(b => b.classList.toggle('on', b.dataset.tab === t));
  document.querySelectorAll('.tab').forEach(s => s.classList.toggle('on', s.id === 'tab-' + t));
}
document.querySelectorAll('#tabs button').forEach(b => b.onclick = () => switchTab(b.dataset.tab));

/* ───────────── interacción de cámara ───────────── */
cv.addEventListener('wheel', e => {
  e.preventDefault();
  const k = Math.exp(-e.deltaY * 0.0015), ns = Math.min(Math.max(cam.s * k, 60), 4000);
  cam.x = e.clientX - (e.clientX - cam.x) * (ns / cam.s);
  cam.y = e.clientY - (e.clientY - cam.y) * (ns / cam.s);
  cam.s = ns;
}, {passive: false});
cv.addEventListener('mousedown', e => { dragging = {x: e.clientX, y: e.clientY, cx: cam.x, cy: cam.y}; cv.classList.add('drag'); });
addEventListener('mouseup', () => { dragging = null; cv.classList.remove('drag'); });
addEventListener('mousemove', e => {
  mouse = {x: e.clientX, y: e.clientY};
  if (dragging) { cam.x = dragging.cx + e.clientX - dragging.x; cam.y = dragging.cy + e.clientY - dragging.y; }
});
cv.addEventListener('dblclick', fitCamera);

function pickHover() {
  if (dragging || !N) { hover = -1; return; }
  let best = -1, bd = 64;
  const mx = mouse.x, my = mouse.y;
  for (let i = 0; i < N; i++) {
    const dx = wx(nodes[i].x) - mx, dy = wy(nodes[i].y) - my, d = dx * dx + dy * dy;
    if (d < bd) { bd = d; best = i; }
  }
  hover = best;
  const tip = $('#tip');
  if (best < 0) { tip.hidden = true; return; }
  const n = nodes[best];
  tip.hidden = false;
  tip.style.left = Math.min(mouse.x + 14, W - 320) + 'px'; tip.style.top = (mouse.y + 14) + 'px';
  tip.innerHTML = `<b>${esc(decodeName(n.s))}</b>${esc(n.k)} · ${esc(n.c)} · ${n.n} fragmentos`;
}

/* ───────────── dibujo ───────────── */
function frame(now) {
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, W, H);
  if (N) drawBrain(now);
  drawRiver(now);
  requestAnimationFrame(frame);
}

function drawBrain(now) {
  const searching = searchSet.size > 0, sc = cam.s;
  // sinapsis
  ctx.lineWidth = 0.6;
  ctx.strokeStyle = searching ? 'rgba(140,150,210,.05)' : 'rgba(140,150,210,.09)';
  ctx.beginPath();
  for (let k = 0; k < edges.length; k++) {
    const a = nodes[edges[k][0]], b = nodes[edges[k][1]];
    ctx.moveTo(wx(a.x), wy(a.y)); ctx.lineTo(wx(b.x), wy(b.y));
  }
  ctx.stroke();

  // neuronas por tipo
  const base = Math.max(0.9, Math.min(sc / 520, 4));
  const byType = {};
  for (let i = 0; i < N; i++) (byType[nodes[i].k] || (byType[nodes[i].k] = [])).push(i);
  for (const t in byType) {
    ctx.fillStyle = hex2rgba(typeColor[t] || '#94a3b8', searching ? 0.22 : 0.7);
    ctx.beginPath();
    for (const i of byType[t]) {
      const n = nodes[i], r = base * (0.8 + Math.min(Math.log2(n.n + 1), 6) * 0.1) * (0.85 + n.z * 0.15);
      ctx.moveTo(wx(n.x) + r, wy(n.y)); ctx.arc(wx(n.x), wy(n.y), r, 0, 6.2832);
    }
    ctx.fill();
  }

  // etiquetas de región
  ctx.font = '600 12px Segoe UI, sans-serif'; ctx.textAlign = 'center';
  centroids.forEach(c => { ctx.fillStyle = hex2rgba(typeColor[c.t], 0.55); ctx.fillText(decodeName(c.t).replace(/_/g, ' ').toUpperCase(), wx(c.x), wy(c.y)); });

  // sinapsis aprendidas (más gruesas, con cuentitas de luz que corren más rápido cuanto más se usan)
  const maxW = Math.max(...learned.doc_doc.map(r => r.w), 1);
  learned.doc_doc.forEach(r => {
    const A = nodes[r.a], B = nodes[r.b]; if (!A || !B) return;
    const f = r.w / maxW;
    ctx.strokeStyle = `rgba(240,180,41,${0.25 + f * 0.5})`; ctx.lineWidth = 0.8 + f * 2.2;
    ctx.beginPath(); ctx.moveTo(wx(A.x), wy(A.y)); ctx.lineTo(wx(B.x), wy(B.y)); ctx.stroke();
    const p = ((now / (2400 - f * 1500)) + r.a * 0.37) % 1;
    ctx.fillStyle = '#ffe9a8'; ctx.beginPath();
    ctx.arc(wx(A.x + (B.x - A.x) * p), wy(A.y + (B.y - A.y) * p), 1.6 + f * 1.4, 0, 6.2832); ctx.fill();
  });

  // neuronas resaltadas por búsqueda
  searchSet.forEach(i => glow(nodes[i], '#8b7cf6', 1, 5 + base * 2, now));
  // neuronas iluminadas por agentes
  lit.forEach((v, i) => {
    const left = v.until - now; if (left <= 0) { lit.delete(i); return; }
    glow(nodes[i], v.color, Math.min(1, left / 3500), 6 + base * 2, now);
  });

  // pulsos agente → neurona
  pulses = pulses.filter(p => {
    const t = (now - p.t0) / p.dur; if (t < 0) return true;
    if (t >= 1) { lit.set(p.i, {until: now + 6500, color: p.color}); return false; }
    const e = t * t * (3 - 2 * t);
    const x = p.fx + (p.tx - p.fx) * e, y = p.fy + (p.ty - p.fy) * e - Math.sin(e * Math.PI) * 0.12;
    const g = ctx.createRadialGradient(wx(x), wy(y), 0, wx(x), wy(y), 14);
    g.addColorStop(0, '#fff'); g.addColorStop(0.25, p.color); g.addColorStop(1, hex2rgba(p.color, 0));
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(wx(x), wy(y), 14, 0, 6.2832); ctx.fill();
    return true;
  });

  // agentes
  agents.forEach(a => {
    const p = agentPos(a), x = wx(p.x), y = wy(p.y), st = agentState[a.id] || {flash: 0};
    const since = now - st.flash, act = since < 2500, pulse = act ? 1 - since / 2500 : 0;
    if (act) {
      const g = ctx.createRadialGradient(x, y, 0, x, y, 46 + pulse * 18);
      g.addColorStop(0, hex2rgba(a.color, 0.55 * pulse + 0.1)); g.addColorStop(1, hex2rgba(a.color, 0));
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, 64, 0, 6.2832); ctx.fill();
    }
    ctx.fillStyle = '#0d1020'; ctx.strokeStyle = a.color; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.arc(x, y, 17, 0, 6.2832); ctx.fill(); ctx.stroke();
    ctx.fillStyle = a.color; ctx.font = '800 11px Segoe UI'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(a.icon, x, y + 1);
    ctx.fillStyle = '#c9cfe6'; ctx.font = '600 11px Segoe UI'; ctx.textBaseline = 'alphabetic';
    ctx.fillText(a.label, x, y + 33);
  });

  // textos flotantes
  floaters = floaters.filter(f => {
    const t = (now - f.t0) / 2200; if (t >= 1) return false;
    const p = agentPos(f.agent);
    ctx.globalAlpha = 1 - t; ctx.fillStyle = f.color; ctx.font = '700 11px Segoe UI'; ctx.textAlign = 'center';
    ctx.fillText(f.text, wx(p.x), wy(p.y) - 26 - f.dy - t * 26); ctx.globalAlpha = 1;
    return true;
  });
  ctx.textBaseline = 'alphabetic';

  if (hover >= 0) { const n = nodes[hover]; ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.arc(wx(n.x), wy(n.y), 5, 0, 6.2832); ctx.stroke(); }
}

function glow(n, color, a, r, now) {
  const x = wx(n.x), y = wy(n.y), g = ctx.createRadialGradient(x, y, 0, x, y, r * 3.2);
  g.addColorStop(0, hex2rgba(color, 0.95 * a)); g.addColorStop(0.35, hex2rgba(color, 0.35 * a)); g.addColorStop(1, hex2rgba(color, 0));
  ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r * 3.2, 0, 6.2832); ctx.fill();
  ctx.fillStyle = `rgba(255,255,255,${a})`; ctx.beginPath(); ctx.arc(x, y, Math.max(1.4, r * 0.28), 0, 6.2832); ctx.fill();
}

/* ───────────── río del tiempo ───────────── */
function drawRiver(now) {
  const w = rc.width / dpr, h = rc.height / dpr;
  rctx.setTransform(dpr, 0, 0, dpr, 0, 0); rctx.clearRect(0, 0, w, h);
  const t1 = Date.now() / 1000, t0 = t1 - 600, left = 128, lanes = agents.length || 1, lh = h / lanes;
  timeline = timeline.filter(e => e.t >= t0);
  rctx.font = '600 10px Segoe UI'; rctx.textBaseline = 'middle';
  agents.forEach((a, k) => {
    const y = k * lh + lh / 2;
    rctx.fillStyle = 'rgba(255,255,255,.04)'; rctx.fillRect(left, y - 0.5, w - left, 1);
    rctx.fillStyle = a.color; rctx.textAlign = 'left'; rctx.fillText(a.label.slice(0, 18), 4, y);
  });
  for (let m = 0; m <= 10; m += 2) {
    const x = left + (w - left) * (1 - m / 10);
    rctx.fillStyle = 'rgba(255,255,255,.07)'; rctx.fillRect(x, 0, 1, h);
  }
  timeline.forEach(e => {
    const k = agents.findIndex(a => a.id === e.agent); if (k < 0) return;
    const a = agents[k], x = left + (w - left) * ((e.t - t0) / 600), y = k * lh + lh / 2;
    if (e.kind === 'qdrant_search') { rctx.fillStyle = a.color; rctx.beginPath(); rctx.arc(x, y, 3.4, 0, 6.2832); rctx.fill(); }
    else if (e.kind === 'llm_call') { rctx.fillStyle = hex2rgba(a.color, 0.7); rctx.fillRect(x - 1, y - lh * 0.3, 2, lh * 0.6); }
    else if (e.kind === 'error') { rctx.fillStyle = '#ef5b6b'; rctx.fillRect(x - 3, y - 3, 6, 6); }
    else if (e.kind === 'agent_start') { rctx.fillStyle = '#34d399'; rctx.fillRect(x, y - lh * 0.4, 1.5, lh * 0.8); }
  });
  rctx.fillStyle = 'rgba(255,255,255,.35)'; rctx.fillRect(w - 1, 0, 1, h);
}

addEventListener('resize', resize);
resize();
load().then(() => { requestAnimationFrame(t => { setInterval(pickHover, 60); frame(t); }); });
setInterval(() => { $('#empty').hidden = timeline.length > 0 || lit.size > 0; }, 1500);
})();
