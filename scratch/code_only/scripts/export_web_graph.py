import os
import re
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAULT_DIR = os.path.join(BASE_DIR, 'data', 'obsidian_vault', '000_PITCH_INVERSORES')
WEB_DIR = os.path.join(BASE_DIR, 'data', 'lifextreme_web_graph')

if not os.path.exists(WEB_DIR):
    os.makedirs(WEB_DIR)

nodes = []
edges = []
node_ids = set()

def get_color(name):
    if "Salkantay" in name:
        return "#39FF14" # Neon Green
    elif "MASTER_CUSCO" in name:
        return "#00BFFF" # Electric Blue
    elif "Agente_Seguridad" in name or "Alerta" in name:
        return "#E74C3C" # Red
    elif "Agente_Ventas" in name or "Rentabilidad" in name:
        return "#2ECC71" # Green
    elif "RAG" in name or "Clasificador" in name or "Motor" in name or "Output" in name or "Input" in name:
        return "#3498DB" # Blue
    else:
        return "#555555" # Dark Gray for generic background DB nodes

def get_size(name):
    if "MASTER_CUSCO" in name:
        return 45
    elif "0" in name: # 01, 02, 03 main steps
        return 35
    elif "Salkantay" in name:
        return 25
    else:
        return 12

def get_label(name):
    clean = name.replace("DB_DEST_", "").replace("_", " ")
    if len(clean) > 25:
        return clean[:25] + "..."
    return clean

for root, dirs, files in os.walk(VAULT_DIR):
    for file in files:
        if file.endswith(".md"):
            node_id = file.replace(".md", "")
            if node_id not in node_ids:
                node_ids.add(node_id)
                nodes.append({
                    "id": node_id,
                    "label": get_label(node_id),
                    "color": get_color(node_id),
                    "size": get_size(node_id),
                    "font": {"color": "#ffffff"}
                })

            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Find [[links]]
            links = re.findall(r'\[\[(.*?)\]\]', content)
            for link in links:
                target_id = link.split("|")[0].strip() # Handle aliases if any
                if target_id not in node_ids:
                    node_ids.add(target_id)
                    nodes.append({
                        "id": target_id,
                        "label": get_label(target_id),
                        "color": get_color(target_id),
                        "size": get_size(target_id),
                        "font": {"color": "#ffffff"}
                    })
                
                # Add edge
                is_rag_to_salkantay = ("RAG" in node_id and "Salkantay" in target_id)
                edges.append({
                    "from": node_id,
                    "to": target_id,
                    "color": {
                        "color": "#39FF14" if is_rag_to_salkantay else "#444444", 
                        "highlight": "#ffffff"
                    },
                    "width": 3 if is_rag_to_salkantay else 1
                })

nodes_json = json.dumps(nodes)
edges_json = json.dumps(edges)

html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cerebro Lifextreme AI - Grafo Interactivo</title>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: #0b0b0b;
            color: white;
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow: hidden;
        }}
        #mynetwork {{
            width: 100vw;
            height: 100vh;
        }}
        #title-overlay {{
            position: absolute;
            top: 30px;
            left: 40px;
            z-index: 10;
            pointer-events: none;
            background: rgba(0, 0, 0, 0.6);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #333;
            backdrop-filter: blur(10px);
        }}
        h1 {{ margin: 0; font-size: 26px; letter-spacing: 1px; color: #fff; }}
        p {{ margin: 8px 0 0 0; color: #aaa; font-size: 15px; max-width: 350px; line-height: 1.4; }}
        .legend {{
            margin-top: 15px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 13px;
            color: #ddd;
        }}
        .dot {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }}
    </style>
</head>
<body>
    <div id="title-overlay">
        <h1>CEREBRO LIFEXTREME</h1>
        <p>Motor de Búsqueda Vectorial (RAG) procesando un clúster masivo de datos turísticos.</p>
        <div class="legend">
            <div class="legend-item"><div class="dot" style="background:#00BFFF;"></div> DB Maestra Cusco</div>
            <div class="legend-item"><div class="dot" style="background:#39FF14;"></div> Vectores Salkantay (Extracción)</div>
            <div class="legend-item"><div class="dot" style="background:#3498DB;"></div> Red Neuronal AI</div>
            <div class="legend-item"><div class="dot" style="background:#555555;"></div> Datos inactivos (Ruido)</div>
        </div>
    </div>
    <div id="mynetwork"></div>
    <script type="text/javascript">
        var nodes = new vis.DataSet({nodes_json});
        var edges = new vis.DataSet({edges_json});

        var container = document.getElementById('mynetwork');
        var data = {{
            nodes: nodes,
            edges: edges
        }};
        var options = {{
            nodes: {{
                shape: 'dot',
                borderWidth: 2,
                borderWidthSelected: 4
            }},
            edges: {{
                smooth: {{
                    type: 'continuous'
                }},
                arrows: {{
                    to: {{enabled: true, scaleFactor: 0.5}}
                }}
            }},
            physics: {{
                barnesHut: {{
                    gravitationalConstant: -3000,
                    centralGravity: 0.3,
                    springLength: 120,
                    springConstant: 0.04,
                    damping: 0.09,
                    avoidOverlap: 0.1
                }},
                stabilization: {{
                    iterations: 200
                }}
            }},
            interaction: {{
                hover: true,
                tooltipDelay: 200,
                zoomView: true
            }}
        }};
        var network = new vis.Network(container, data, options);
        
        // Efecto hover (Highlight connections)
        network.on("hoverNode", function (params) {{
            network.canvas.body.container.style.cursor = 'pointer';
        }});
        network.on("blurNode", function (params) {{
            network.canvas.body.container.style.cursor = 'default';
        }});
    </script>
</body>
</html>
"""

with open(os.path.join(WEB_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print("Grafo web interactivo generado en:", WEB_DIR)
