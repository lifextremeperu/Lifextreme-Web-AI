import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPH_JSON_PATH = os.path.join(BASE_DIR, 'scripts', 'graphify-out', 'graph.json')
WEB_DIR = os.path.join(BASE_DIR, 'data', 'lifextreme_tech_graph')

if not os.path.exists(WEB_DIR):
    os.makedirs(WEB_DIR)

with open(GRAPH_JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

raw_nodes = data.get("nodes", [])
raw_links = data.get("links", [])

node_to_module = {}
modules = {}

# Nodos Macro Arquitectónicos (El Núcleo del Ecosistema)
macro_nodes = {
    "Lifextreme Frontend": {"id": "Lifextreme Frontend", "name": "💻 Lifextreme Web/App", "group": 1, "val": 12},
    "LLM Core": {"id": "LLM Core", "name": "🧠 Motor LLM (Ollama/Llama3)", "group": 5, "val": 15},
    "Vector DB (RAG)": {"id": "Vector DB (RAG)", "name": "📊 Vector DB (Supabase/Chroma)", "group": 4, "val": 12},
    "Obsidian Vault": {"id": "Obsidian Vault", "name": "📚 Obsidian Knowledge Base", "group": 3, "val": 10},
}

# Agrupar cientos de funciones AST en sus respectivos Microservicios/Scripts
for n in raw_nodes:
    node_id = n.get("id")
    source_file = n.get("source_file", "unknown")
    
    if not source_file.endswith(".py"):
        continue
        
    module_name = source_file
    node_to_module[node_id] = module_name
    
    if module_name not in modules:
        group = 0 # Default scripts
        if "agent" in module_name: group = 5 # Agents -> LLM Color
        elif "api" in module_name or "server" in module_name: group = 1 # APIs -> Frontend Color
        elif "rag" in module_name or "vector" in module_name: group = 4 # RAG -> Vector DB Color
        elif "export" in module_name or "obsidian" in module_name or "graph" in module_name: group = 3 # Graph/Obsidian Color
        
        modules[module_name] = {
            "id": module_name,
            "name": f"⚙️ {module_name}",
            "group": group,
            "val": 4
        }

macro_links_dict = {}

# Mapear las relaciones entre funciones a relaciones entre Microservicios
for l in raw_links:
    source_id = l.get("source")
    target_id = l.get("target")
    
    source_mod = node_to_module.get(source_id)
    target_mod = node_to_module.get(target_id)
    
    if source_mod and target_mod and source_mod != target_mod:
        link_key = f"{source_mod}____{target_mod}"
        if link_key not in macro_links_dict:
            macro_links_dict[link_key] = {"source": source_mod, "target": target_mod}
        # Incrementar tamaño de los nodos más conectados
        modules[source_mod]["val"] += 0.3
        modules[target_mod]["val"] += 0.3

# Enlaces sintéticos para conectar los scripts aislados a los Núcleos Arquitectónicos
synthetic_links = []
for m in modules:
    if "agent" in m:
        synthetic_links.append({"source": m, "target": "LLM Core"})
    if "rag" in m or "vector" in m:
        synthetic_links.append({"source": m, "target": "Vector DB (RAG)"})
    if "export" in m or "graph" in m or "build" in m:
        synthetic_links.append({"source": m, "target": "Obsidian Vault"})
    if "api" in m or "server" in m or "export_web" in m:
        synthetic_links.append({"source": "Lifextreme Frontend", "target": m})

macro_links = list(macro_links_dict.values()) + synthetic_links
all_nodes = list(macro_nodes.values()) + list(modules.values())

graph_data = {
    "nodes": all_nodes,
    "links": macro_links
}

graph_json_str = json.dumps(graph_data)

html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lifextreme - Ecosistema de Ingeniería 3D</title>
    <script src="https://unpkg.com/3d-force-graph"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        body {{ margin: 0; padding: 0; overflow: hidden; background-color: #020617; font-family: 'Inter', sans-serif; }}
        #3d-graph {{ width: 100vw; height: 100vh; cursor: crosshair; }}
        
        #title-overlay {{
            position: absolute;
            top: 30px;
            left: 40px;
            z-index: 10;
            pointer-events: none;
            background: rgba(15, 23, 42, 0.85); /* Slate 900 con opacidad */
            padding: 24px;
            border-radius: 16px;
            border: 1px solid #334155;
            backdrop-filter: blur(12px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
        }}
        h1 {{ margin: 0; font-size: 28px; font-weight: 800; letter-spacing: -0.5px; color: #f8fafc; }}
        p {{ margin: 10px 0 0 0; color: #94a3b8; font-size: 15px; max-width: 380px; line-height: 1.5; }}
        .instruction {{ color: #10b981; font-weight: 600; margin-top: 15px; font-size: 14px; display: block; }}
        
        .scene-tooltip {{
            background: rgba(15, 23, 42, 0.9) !important;
            color: #f8fafc !important;
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
            padding: 8px 12px !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 13px !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5) !important;
        }}
    </style>
</head>
<body>
    <div id="title-overlay">
        <h1>ARQUITECTURA DE INGENIERÍA</h1>
        <p>Ecosistema de Software y Dependencias de Inteligencia Artificial.</p>
        <span class="instruction">👉 Rota el espacio 3D con Click, o haz Scroll para Zoom In/Out.</span>
    </div>
    
    <div id="3d-graph"></div>

    <script>
        const data = {graph_json_str};
        
        // Colores corporativos Lifextreme + Paleta neón ciberseguridad
        const colors = [
            '#ffffff', // 0: Main py files (White Core)
            '#00f0ff', // 1: Cyan (Cyber)
            '#ff003c', // 2: Neon Red
            '#ffbf00', // 3: Amber
            '#00ff66', // 4: Matrix Green
            '#bc13fe', // 5: Neon Purple
            '#ff073a', // 6: Laser Red
            '#1f51ff', // 7: Neon Blue
            '#ccff00', // 8: Electric Yellow
            '#ff1493'  // 9: Deep Pink
        ];

        const Graph = ForceGraph3D()
        (document.getElementById('3d-graph'))
            .graphData(data)
            .nodeLabel('name')
            .nodeAutoColorBy('group')
            .nodeColor(node => colors[node.group % colors.length])
            .nodeVal(node => Math.min(node.val * 1.5, 8)) // Slightly larger nodes
            .linkColor(() => 'rgba(0, 240, 255, 0.15)') // Cyan transparent links
            .linkWidth(0.6)
            .linkDirectionalParticles(link => Math.max(1, Math.floor(Math.random() * 4))) // 1 to 3 particles per link
            .linkDirectionalParticleWidth(1.8)
            .linkDirectionalParticleColor(() => '#ffffff') // Bright white data packets
            .linkDirectionalParticleSpeed(0.008)
            .backgroundColor('#050510') // Pitch black/deep blue void
            .showNavInfo(false);
            
        // Rotación orbital automática suave (Efecto Dashboard)
        let angle = 0;
        const distance = 700;
        setInterval(() => {{
            Graph.cameraPosition({{
                x: distance * Math.sin(angle),
                z: distance * Math.cos(angle)
            }});
            angle += Math.PI / 2000;
        }}, 30);
    </script>
</body>
</html>
"""

with open(os.path.join(WEB_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print("Grafo 3D WebGL Ciberseguridad generado en:", WEB_DIR)

