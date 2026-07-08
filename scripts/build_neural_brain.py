import os
import json
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OBSIDIAN_DIR = os.path.join(BASE_DIR, 'data', 'obsidian_vault')
WEB_DIR = os.path.join(BASE_DIR, 'data', 'lifextreme_neural_brain')

if not os.path.exists(WEB_DIR):
    os.makedirs(WEB_DIR)

# --- 1. Leer los archivos reales de Obsidian ---
obsidian_files = []
for root, dirs, files in os.walk(OBSIDIAN_DIR):
    for f in files:
        if f.endswith('.md'):
            obsidian_files.append(f.replace('.md', ''))

# Si no hay muchos, duplicamos sintéticamente para generar densidad (simulando chunks de embeddings)
if len(obsidian_files) < 150:
    for i in range(150 - len(obsidian_files)):
        obsidian_files.append(f"Vec_Chunk_{i:04d}")

nodes = []
links = []

# --- 2. Crear Capas de la Red Neuronal ---

# Capa 1: Inputs (Consultas del cliente)
inputs = [f"Input_Q_{i}" for i in range(20)]
for name in inputs:
    nodes.append({"id": name, "name": name, "layer": 1, "color": "#f43f5e", "size": 3})

# Capa 2: Espacio Latente L1 (Atención)
l1_nodes = [f"L1_Att_{i}" for i in range(100)]
for name in l1_nodes:
    nodes.append({"id": name, "name": name, "layer": 2, "color": "#f59e0b", "size": 1.5})

# Capa 3: Espacio Latente L2 (Vectores)
l2_nodes = [f"L2_Vec_{i}" for i in range(150)]
for name in l2_nodes:
    nodes.append({"id": name, "name": name, "layer": 3, "color": "#10b981", "size": 1.5})

# Capa 4: Base de Conocimiento (Obsidian Vault + Chunks)
for name in obsidian_files:
    nodes.append({"id": name, "name": name, "layer": 4, "color": "#0ea5e9", "size": 2.5})

# Capa 5: Síntesis Contextual (RAG / LLM)
l5_nodes = [f"L5_Syn_{i}" for i in range(80)]
for name in l5_nodes:
    nodes.append({"id": name, "name": name, "layer": 5, "color": "#8b5cf6", "size": 1.5})

# Capa 6: Outputs (Respuestas / Cotizaciones)
outputs = [f"Output_Ans_{i}" for i in range(15)]
for name in outputs:
    nodes.append({"id": name, "name": name, "layer": 6, "color": "#d946ef", "size": 3})

# --- 3. Generar Conexiones Densas (Sinapsis) ---
# Inputs -> L1
for i in inputs:
    for _ in range(15): # Cada input se conecta a 15 atenciones aleatorias
        links.append({"source": i, "target": random.choice(l1_nodes), "color": "rgba(244, 63, 94, 0.3)"})

# L1 -> L2
for l1 in l1_nodes:
    for _ in range(8):
        links.append({"source": l1, "target": random.choice(l2_nodes), "color": "rgba(245, 158, 11, 0.25)"})

# L2 -> Obsidian (Matching Vectorial)
for l2 in l2_nodes:
    for _ in range(5):
        links.append({"source": l2, "target": random.choice(obsidian_files), "color": "rgba(16, 185, 129, 0.25)"})

# Obsidian -> L5 (Extracción de Contexto RAG)
for obs in obsidian_files:
    for _ in range(4):
        links.append({"source": obs, "target": random.choice(l5_nodes), "color": "rgba(14, 165, 233, 0.25)"})

# L5 -> Outputs (Generación LLM)
for l5 in l5_nodes:
    for _ in range(10):
        links.append({"source": l5, "target": random.choice(outputs), "color": "rgba(139, 92, 246, 0.3)"})

graph_data = {"nodes": nodes, "links": links}
graph_json_str = json.dumps(graph_data)

html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lifextreme - Cerebro Neuronal Masivo</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
    <script src="https://unpkg.com/3d-force-graph@1.73.3/dist/3d-force-graph.min.js"></script>
    
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;800&display=swap" rel="stylesheet">
    <style>
        body {{ margin: 0; padding: 0; overflow: hidden; background-color: #02040a; font-family: 'Inter', sans-serif; }}
        #3d-graph {{ width: 100vw; height: 100vh; cursor: crosshair; }}
        
        #overlay {{
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 10;
            pointer-events: none;
            background: transparent;
            text-align: center;
        }}
        h1 {{ margin: 0; font-size: 32px; font-weight: 800; letter-spacing: -1px; color: #f8fafc; text-shadow: 0 0 20px rgba(255,255,255,0.5); }}
        p {{ margin: 8px 0 0 0; color: #a8b2d1; font-size: 14px; font-weight: 400; letter-spacing: 1px; text-transform: uppercase; }}
        .badge {{ position: absolute; top: 30px; left: 30px; background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.3); color: #c4b5fd; padding: 8px 16px; border-radius: 20px; font-size: 12px; font-weight: 800; letter-spacing: 1px; box-shadow: 0 0 15px rgba(139, 92, 246, 0.2); }}
    </style>
</head>
<body>
    <div class="badge">● RED NEURONAL LIFEXTREME (ESTADO: ACTIVO)</div>
    <div id="overlay">
        <h1>Lifextreme Latent Brain Space</h1>
        <p>Flujo Vectorial de Izquierda a Derecha ({len(nodes)} Nodos | {len(links)} Sinapsis)</p>
    </div>
    
    <div id="3d-graph"></div>

    <script>
        const data = {graph_json_str};

        const Graph = ForceGraph3D()
        (document.getElementById('3d-graph'))
            .graphData(data)
            // ESTA ES LA CLAVE: DAG de Izquierda a Derecha para parecer una Red Neuronal Transformer
            .dagMode('lr')
            .dagLevelDistance(250)
            
            // Nodos muy pequeños, porque lo que importa en esta visualización son los enlaces
            .nodeRelSize(2)
            .nodeVal('size')
            .nodeColor('color')
            .nodeOpacity(0.9)
            .nodeResolution(8)
            
            // Los enlaces son delgados y coloridos
            .linkColor('color')
            .linkWidth(0.5)
            .linkOpacity(0.4)
            // Curvatura muy sutil para que parezcan ondas de información
            .linkCurvature(0.1)
            .linkCurveRotation(link => Math.random() * Math.PI * 2)
            
            // Partículas viajando a alta velocidad
            .linkDirectionalParticles(link => Math.random() > 0.5 ? 1 : 0) // Algunas tienen partículas
            .linkDirectionalParticleWidth(1.2)
            .linkDirectionalParticleColor(() => '#ffffff')
            .linkDirectionalParticleSpeed(0.015)
            
            .backgroundColor('#02040a') // Vacío casi negro
            .showNavInfo(false);
            
        // Post-procesado para dar brillo de Bloom (Efecto Anthropic / Cyberpunk)
        const bloomPass = new THREE.UnrealBloomPass();
        bloomPass.strength = 1.8;
        bloomPass.radius = 0.5;
        bloomPass.threshold = 0.1;
        Graph.postProcessingComposer().addPass(bloomPass);

        // Movimiento suave de la cámara a través del flujo neuronal
        let time = 0;
        setTimeout(() => {{
            setInterval(() => {{
                try {{
                    const camPos = Graph.cameraPosition();
                    Graph.cameraPosition({{
                        x: camPos.x,
                        y: Math.sin(time) * 100,
                        z: camPos.z
                    }});
                    time += 0.005;
                }} catch(e) {{}}
            }}, 30);
        }}, 2000);
        
        // Enfocar la red completa al inicio
        Graph.onEngineStop(() => Graph.zoomToFit(400, 50));
    </script>
</body>
</html>
"""

with open(os.path.join(WEB_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Cerebro Neuronal Lifextreme generado en 3D en: {WEB_DIR}")
