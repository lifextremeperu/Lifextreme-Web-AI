import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPH_JSON_PATH = os.path.join(BASE_DIR, 'scripts', 'graphify-out', 'graph.json')
WEB_DIR = os.path.join(BASE_DIR, 'data', 'lifextreme_tech_graph')

if not os.path.exists(WEB_DIR):
    os.makedirs(WEB_DIR)

with open(GRAPH_JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

nodes = data.get("nodes", [])
links = data.get("links", [])

node_map = {}
for n in nodes:
    node_id = n.get("id")
    label = n.get("norm_label") or n.get("label") or node_id
    group = n.get("community", 1)
    
    val = 1
    file_type = n.get("file_type", "code")
    if file_type == "code" and label.endswith(".py"):
        val = 4
        group = 0 # main modules
    elif file_type == "code":
        val = 1.5
    
    node_map[node_id] = {
        "id": node_id,
        "name": label,
        "val": val,
        "group": group
    }

# Process links
valid_links = []
for l in links:
    source = l.get("source")
    target = l.get("target")
    if source in node_map and target in node_map:
        valid_links.append({
            "source": source,
            "target": target
        })
        # increase size slightly for connected nodes
        node_map[source]["val"] += 0.2
        node_map[target]["val"] += 0.2

graph_data = {
    "nodes": list(node_map.values()),
    "links": valid_links
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
        
        // Colores corporativos Lifextreme + Paleta expandida para clusters
        const colors = [
            '#f8fafc', // 0: Main py files (White)
            '#4338ca', // 1: Indigo
            '#f43f5e', // 2: Rose
            '#ffbf00', // 3: Amber
            '#10b981', // 4: Emerald
            '#0ea5e9', // 5: Sky
            '#d946ef', // 6: Fuchsia
            '#8b5cf6', // 7: Violet
            '#14b8a6', // 8: Teal
            '#f97316'  // 9: Orange
        ];

        const Graph = ForceGraph3D()
        (document.getElementById('3d-graph'))
            .graphData(data)
            .nodeLabel('name')
            .nodeAutoColorBy('group')
            .nodeColor(node => colors[node.group % colors.length])
            .nodeVal('val')
            .linkColor(() => 'rgba(148, 163, 184, 0.2)') // Slate 400 con 20% opacidad
            .linkWidth(0.5)
            .linkDirectionalParticles(1)
            .linkDirectionalParticleWidth(1.2)
            .linkDirectionalParticleSpeed(0.005)
            .backgroundColor('#020617');
            
        // Rotación orbital automática suave
        let angle = 0;
        setInterval(() => {{
            Graph.cameraPosition({{
                x: 600 * Math.sin(angle),
                z: 600 * Math.cos(angle)
            }});
            angle += Math.PI / 1500;
        }}, 30);
    </script>
</body>
</html>
"""

with open(os.path.join(WEB_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print("Grafo 3D WebGL generado en:", WEB_DIR)
