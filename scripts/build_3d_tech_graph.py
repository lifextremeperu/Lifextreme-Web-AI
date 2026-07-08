import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(BASE_DIR, 'data', 'lifextreme_tech_graph')

if not os.path.exists(WEB_DIR):
    os.makedirs(WEB_DIR)

# Definimos los Nodos de la Fábrica (Building Levels)
# Group define el nivel / piso y el color lógico
factory_nodes = [
    # Piso 1: Cimientos de Datos y Computación
    {"id": "obsidian", "name": "Obsidian Vault", "group": 1, "color": "#bc13fe", "val": 10},
    {"id": "supabase", "name": "Supabase VectorDB", "group": 1, "color": "#10b981", "val": 10},
    {"id": "ollama", "name": "Ollama AI Server", "group": 1, "color": "#ff073a", "val": 15},
    
    # Piso 2: Orquestación
    {"id": "dify", "name": "Dify.AI Orchestrator", "group": 2, "color": "#0ea5e9", "val": 8},
    {"id": "n8n", "name": "N8N Automation", "group": 2, "color": "#ffbf00", "val": 8},
    
    # Piso 3: Agentes Especializados (Trabajadores)
    {"id": "llama3_orq", "name": "Llama-3 (Routing)", "group": 3, "color": "#00f0ff", "val": 6},
    {"id": "llama3_ventas", "name": "Llama-3 (Sales)", "group": 3, "color": "#00f0ff", "val": 6},
    {"id": "phi3_rag", "name": "Phi-3 (RAG)", "group": 3, "color": "#00ff66", "val": 6},
    {"id": "risk_agent", "name": "Llama-3 (Risk Alert)", "group": 3, "color": "#ff003c", "val": 6},
    
    # Piso 4: APIs y Backend
    {"id": "fastapi", "name": "FastAPI Core", "group": 4, "color": "#ccff00", "val": 12},
    
    # Piso 5: Frontend y Clientes (La Fachada)
    {"id": "quartz", "name": "Quartz 4 Interface", "group": 5, "color": "#ffffff", "val": 10},
    {"id": "github", "name": "GitHub Pages", "group": 5, "color": "#ffffff", "val": 8},
    {"id": "vercel", "name": "Vercel Edge", "group": 5, "color": "#ffffff", "val": 8},
    {"id": "b2b_client", "name": "B2B Partner Web", "group": 5, "color": "#f8fafc", "val": 14},
]

# Definimos el flujo de datos (Desde la Base hasta el Cliente)
factory_links = [
    # Capa 1 a 2 / 3
    {"source": "obsidian", "target": "supabase"},
    {"source": "obsidian", "target": "quartz"},
    {"source": "ollama", "target": "llama3_orq"},
    {"source": "ollama", "target": "llama3_ventas"},
    {"source": "ollama", "target": "phi3_rag"},
    {"source": "ollama", "target": "risk_agent"},
    
    # RAG Flow
    {"source": "supabase", "target": "phi3_rag"},
    
    # Orquestación
    {"source": "llama3_orq", "target": "dify"},
    {"source": "dify", "target": "llama3_ventas"},
    {"source": "dify", "target": "phi3_rag"},
    {"source": "dify", "target": "risk_agent"},
    
    # Hacia el Backend
    {"source": "llama3_ventas", "target": "fastapi"},
    {"source": "phi3_rag", "target": "fastapi"},
    {"source": "risk_agent", "target": "fastapi"},
    {"source": "n8n", "target": "fastapi"},
    {"source": "n8n", "target": "obsidian"}, # Automatización escribe a la boveda
    
    # Hacia la Fachada
    {"source": "fastapi", "target": "quartz"},
    {"source": "fastapi", "target": "b2b_client"},
    {"source": "quartz", "target": "github"},
    {"source": "quartz", "target": "vercel"},
]

graph_data = {
    "nodes": factory_nodes,
    "links": factory_links
}

graph_json_str = json.dumps(graph_data)

html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lifextreme - AI Factory Building 3D</title>
    <!-- EL ORDEN ES CRÍTICO: Three.js DEBE cargar antes que 3d-force-graph y SpriteText -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
    <script src="https://unpkg.com/three-spritetext@1.6.5/dist/three-spritetext.min.js"></script>
    <script src="https://unpkg.com/3d-force-graph@1.73.3/dist/3d-force-graph.min.js"></script>
    
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        body {{ margin: 0; padding: 0; overflow: hidden; background-color: #050510; font-family: 'Inter', sans-serif; }}
        #3d-graph {{ width: 100vw; height: 100vh; cursor: crosshair; }}
        
        #title-overlay {{
            position: absolute;
            top: 30px;
            left: 40px;
            z-index: 10;
            pointer-events: none;
            background: rgba(15, 23, 42, 0.85);
            padding: 24px;
            border-radius: 16px;
            border: 1px solid #334155;
            backdrop-filter: blur(12px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
        }}
        h1 {{ margin: 0; font-size: 28px; font-weight: 800; letter-spacing: -0.5px; color: #f8fafc; }}
        p {{ margin: 10px 0 0 0; color: #94a3b8; font-size: 15px; max-width: 400px; line-height: 1.5; }}
        .instruction {{ color: #10b981; font-weight: 600; margin-top: 15px; font-size: 14px; display: block; }}
    </style>
</head>
<body>
    <div id="title-overlay">
        <h1>LIFEXTREME AI FACTORY</h1>
        <p>Edificio corporativo de Inteligencia Artificial. Flujo de datos desde los servidores y bases vectoriales (Planta Baja) hacia las APIs y el Frontend (Último Piso).</p>
        <span class="instruction">👉 Arrastra para orbitar el edificio. Haz Scroll para zoom espacial.</span>
    </div>
    
    <div id="3d-graph"></div>

    <script>
        const data = {graph_json_str};

        const Graph = ForceGraph3D()
        (document.getElementById('3d-graph'))
            .graphData(data)
            // ESTO CREA LA ESTRUCTURA DE EDIFICIO (Bottom-Up DAG)
            .dagMode('bu')
            .dagLevelDistance(60)
            
            // Reemplazamos las esferas por bloques físicos 3D (Lego / Fábrica)
            .nodeThreeObject(node => {{
                const group = new THREE.Group();
                
                // 1. El Bloque de Servidor / Lego (Cubo aplanado)
                const geometry = new THREE.BoxGeometry(28, 8, 28);
                
                // Material de cristal brillante/Neón
                const material = new THREE.MeshPhysicalMaterial({{
                    color: node.color,
                    transparent: true,
                    opacity: 0.7,
                    roughness: 0.2,
                    transmission: 0.6,
                    emissive: node.color,
                    emissiveIntensity: 0.4
                }});
                const cube = new THREE.Mesh(geometry, material);
                
                // Bordes luminosos para darle ese look arquitectónico Tron/Sci-Fi
                const edges = new THREE.EdgesGeometry(geometry);
                const edgesMaterial = new THREE.LineBasicMaterial({{ 
                    color: 0xffffff, 
                    transparent: true, 
                    opacity: 0.8 
                }});
                const line = new THREE.LineSegments(edges, edgesMaterial);
                cube.add(line);
                
                group.add(cube);

                // 2. Texto Holográfico flotando encima del bloque
                try {{
                    const sprite = new SpriteText(node.name);
                    sprite.color = '#ffffff';
                    sprite.textHeight = 4.5;
                    sprite.fontWeight = 'bold';
                    sprite.fontFace = 'Inter';
                    sprite.position.y = 12; // Flota encima del cubo
                    sprite.backgroundColor = 'transparent';
                    
                    group.add(sprite);
                }} catch (err) {{
                    console.error("Error creating SpriteText:", err);
                }}
                
                return group;
            }})
            
            // Configuración de conexiones (Tubos de la fábrica)
            .linkColor(() => 'rgba(255, 255, 255, 0.25)') // Líneas blancas/gris brillante
            .linkWidth(1.5)
            .linkDirectionalParticles(link => Math.max(1, Math.floor(Math.random() * 4))) // Flujo de datos
            .linkDirectionalParticleWidth(3.5)
            .linkDirectionalParticleColor(() => '#00f0ff') // Paquetes de datos cian neón
            .linkDirectionalParticleSpeed(0.006)
            .backgroundColor('#030712') // Gris ultra oscuro (casi negro)
            .showNavInfo(false);
            
        // --- ILUMINACIÓN Y ESCENARIO (LA FÁBRICA) ---
        
        // Suelo de la Fábrica (Grid Holográfico)
        const gridHelper = new THREE.GridHelper(1000, 40, 0x00f0ff, 0x1e293b);
        gridHelper.position.y = -150; // Colocado en la base del rascacielos
        Graph.scene().add(gridHelper);
        
        // Luces para los bloques de cristal
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        Graph.scene().add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 1.2);
        directionalLight.position.set(200, 500, 300);
        Graph.scene().add(directionalLight);
            
        // Rotación orbital lenta de la cámara alrededor del "Rascacielos"
        let angle = 0;
        const distance = 400;
        setTimeout(() => {{
            setInterval(() => {{
                try {{
                    Graph.cameraPosition({{
                        x: distance * Math.sin(angle),
                        z: distance * Math.cos(angle)
                    }});
                    angle += Math.PI / 1500;
                }} catch(e) {{}}
            }}, 30);
        }}, 1500); // Esperar que el grafo se inicie antes de mover la cámara
    </script>
</body>
</html>
"""

with open(os.path.join(WEB_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print("Fábrica de IA Lifextreme generada en 3D en:", WEB_DIR)
