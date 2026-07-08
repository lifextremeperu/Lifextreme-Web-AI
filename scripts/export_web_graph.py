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
        return "#ffbf00" # Amber (Accent)
    elif "MASTER_CUSCO" in name:
        return "#f8fafc" # Slate 50 (White/Bright)
    elif "Agente_Seguridad" in name or "Alerta" in name or "Riesgo" in name:
        return "#f43f5e" # Rose 500 (Secondary)
    elif "Agente_Ventas" in name or "Rentabilidad" in name or "Precios" in name:
        return "#10b981" # Emerald 500 (Sales)
    elif "RAG" in name or "Clasificador" in name or "Motor" in name or "Output" in name or "Input" in name or "0" in name:
        return "#4338ca" # Indigo 700 (Primary)
    else:
        return "#334155" # Slate 700 for generic background DB nodes

def get_size(name):
    if "MASTER_CUSCO" in name:
        return 45
    elif "0" in name: # 01, 02, 03 main steps
        return 35
    elif "Salkantay" in name:
        return 25
    else:
        return 15

def get_visibility(name):
    core_keywords = ["MASTER_CUSCO", "RAG", "01_", "02_", "03_"]
    # We want to show Salkantay main node as well
    if any(k in name for k in core_keywords):
        return False # hidden: false
    if "Salkantay" in name and len(name.split("_")) <= 2:
        return False # Main Salkantay node
    return True # hidden: true

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
                    "hidden": get_visibility(node_id),
                    "font": {"color": "#e2e8f0"} # Slate 200
                })

            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Find [[links]]
            links = re.findall(r'\[\[(.*?)\]\]', content)
            for link in links:
                target_id = link.split("|")[0].strip()
                if target_id not in node_ids:
                    node_ids.add(target_id)
                    nodes.append({
                        "id": target_id,
                        "label": get_label(target_id),
                        "color": get_color(target_id),
                        "size": get_size(target_id),
                        "hidden": get_visibility(target_id),
                        "font": {"color": "#e2e8f0"}
                    })
                
                # Add edge
                is_rag_to_salkantay = ("RAG" in node_id and "Salkantay" in target_id)
                edges.append({
                    "from": node_id,
                    "to": target_id,
                    "color": {
                        "color": "#ffbf00" if is_rag_to_salkantay else "#475569", 
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
    <title>Lifextreme - Red Neuronal de Ventas</title>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: #020617; /* Slate 910 */
            color: #f8fafc;
            font-family: 'Inter', sans-serif;
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
            background: rgba(15, 23, 42, 0.85); /* Slate 900 con opacidad */
            padding: 24px;
            border-radius: 16px;
            border: 1px solid #334155;
            backdrop-filter: blur(12px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
        }}
        h1 {{ margin: 0; font-size: 28px; font-weight: 800; letter-spacing: -0.5px; color: #f8fafc; }}
        p {{ margin: 10px 0 0 0; color: #94a3b8; font-size: 15px; max-width: 380px; line-height: 1.5; }}
        .instruction {{ color: #ffbf00; font-weight: 600; margin-top: 15px; font-size: 14px; display: block; }}
        .legend {{
            margin-top: 20px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 14px;
            color: #cbd5e1;
            font-weight: 600;
        }}
        .dot {{
            width: 14px;
            height: 14px;
            border-radius: 50%;
            box-shadow: 0 0 8px currentColor;
        }}
        .rag-demo {{
            margin-top: 24px;
            padding-top: 20px;
            border-top: 1px dashed #334155;
        }}
        .rag-title {{ font-size: 15px; font-weight: 800; color: #f8fafc; margin: 0 0 12px 0; display: flex; align-items: center; gap: 8px;}}
        .rag-box {{ background: #1e293b; padding: 12px; border-radius: 10px; margin-bottom: 10px; font-size: 13px; color: #cbd5e1; line-height: 1.5; border-left: 3px solid #4338ca; }}
        .rag-box.user {{ border-left: 3px solid #ffbf00; background: rgba(255, 191, 0, 0.08); color: #f8fafc; }}
        .rag-box.ai {{ border-left: 3px solid #10b981; background: rgba(16, 185, 129, 0.1); color: #f8fafc; }}
        .step {{ color: #94a3b8; font-size: 11px; font-weight: 800; text-transform: uppercase; margin-bottom: 4px; display: block; }}
    </style>
</head>
<body>
    <div id="title-overlay">
        <h1>LIFEXTREME NEURAL RAG</h1>
        <p>Modelo dinámico del proceso de decisión de la IA para ventas y logística B2B.</p>
        <span class="instruction">👉 Haz CLIC en los nodos para expandir/colapsar sus conexiones neurales.</span>
        <div class="legend">
            <div class="legend-item"><div class="dot" style="background:#f8fafc; color:#f8fafc;"></div> Clúster Maestro (Cusco)</div>
            <div class="legend-item"><div class="dot" style="background:#4338ca; color:#4338ca;"></div> Motor Vectorial (IA)</div>
            <div class="legend-item"><div class="dot" style="background:#ffbf00; color:#ffbf00;"></div> Salkantay (Focus)</div>
            <div class="legend-item"><div class="dot" style="background:#f43f5e; color:#f43f5e;"></div> Agentes de Riesgo / Alertas</div>
            <div class="legend-item"><div class="dot" style="background:#10b981; color:#10b981;"></div> Finanzas / Ventas</div>
        </div>

        <div class="rag-demo">
            <h2 class="rag-title">🧠 Ejemplo de Inferencia Real</h2>
            
            <div class="rag-box user">
                <span class="step">1. Pregunta del Usuario (B2B)</span>
                "Cotizar el Salkantay Trek de 5 días para 2 pasajeros en Junio. ¿Cuáles son los riesgos climáticos y margen B2B?"
            </div>
            
            <div class="rag-box">
                <span class="step">2. Orquestador RAG Extrae Nodos:</span>
                • <span style="color:#ffbf00">Salkantay Clima Temporada</span> (Seca)<br>
                • <span style="color:#f43f5e">Salkantay Seguridad</span> (Altitud 4600m)<br>
                • <span style="color:#10b981">Salkantay Precios Moneda</span> ($350 Base)
            </div>
            
            <div class="rag-box ai">
                <span class="step">3. Respuesta Lifextreme AI</span>
                "Para Junio las condiciones son óptimas (temporada seca). El riesgo a mitigar es el frío en el Abra (4600m). El costo B2B neto es $350 USD por PAX, permitiendo un margen del 25% para su agencia."
            </div>
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
                borderWidthSelected: 4,
                font: {{ face: 'Inter', strokeWidth: 2, strokeColor: '#020617' }}
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
                    gravitationalConstant: -4000,
                    centralGravity: 0.3,
                    springLength: 150,
                    springConstant: 0.04,
                    damping: 0.09,
                    avoidOverlap: 0.15
                }},
                stabilization: {{
                    iterations: 150
                }}
            }},
            interaction: {{
                hover: true,
                tooltipDelay: 200,
                zoomView: true
            }}
        }};
        var network = new vis.Network(container, data, options);
        
        // Efecto hover
        network.on("hoverNode", function (params) {{
            network.canvas.body.container.style.cursor = 'pointer';
        }});
        network.on("blurNode", function (params) {{
            network.canvas.body.container.style.cursor = 'default';
        }});

        // Expandir / Colapsar al hacer clic
        network.on("click", function (params) {{
            if (params.nodes.length > 0) {{
                var clickedNodeId = params.nodes[0];
                var connectedNodes = network.getConnectedNodes(clickedNodeId);
                
                // Determinar si expandimos o colapsamos basándonos en el primer nodo conectado
                var isExpanding = false;
                for (var i = 0; i < connectedNodes.length; i++) {{
                    var node = nodes.get(connectedNodes[i]);
                    if (node && node.hidden) {{
                        isExpanding = true;
                        break;
                    }}
                }}

                var updates = [];
                for (var i = 0; i < connectedNodes.length; i++) {{
                    var nId = connectedNodes[i];
                    // No colapsar el MASTER ni los pasos principales de RAG
                    var nodeData = nodes.get(nId);
                    if (nodeData && nodeData.label && !nodeData.label.includes("MASTER") && !nodeData.label.match(/^[0-9]{{2}} /)) {{
                        updates.push({{ id: nId, hidden: !isExpanding }});
                    }}
                }}
                
                if (updates.length > 0) {{
                    nodes.update(updates);
                }}
            }}
        }});
    </script>
</body>
</html>
"""

with open(os.path.join(WEB_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print("Grafo web interactivo UX/UI generado en:", WEB_DIR)
