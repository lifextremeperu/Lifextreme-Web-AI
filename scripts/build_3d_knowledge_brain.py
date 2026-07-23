import os
import json
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = BASE_DIR # Lo pondremos directo en la raiz como investor-brain.html

nodes = [
  {"id": "CORE", "name": "LIFEXTREME BRAIN\n(Qdrant RAG)", "group": 0, "val": 40, "color": "#a855f7"}
]

departments = [
    "Amazonas", "Ancash", "Apurimac", "Arequipa", "Ayacucho", "Cajamarca", 
    "Callao", "Cusco", "Huancavelica", "Huanuco", "Ica", "Junin", "La Libertad", 
    "Lambayeque", "Lima", "Loreto", "Madre de Dios", "Moquegua", "Pasco", 
    "Piura", "Puno", "San Martin", "Tacna", "Tumbes"
]

for dep in departments:
    nodes.append({"id": f"DEP_{dep}", "name": dep, "group": 1, "val": 15, "color": "#0ea5e9"})

knowledge_modules = [
    {"id": "MOD_MINCETUR", "name": "MINCETUR", "color": "#10b981"},
    {"id": "MOD_TUPA", "name": "TUPA", "color": "#10b981"},
    {"id": "MOD_INDECOPI", "name": "INDECOPI", "color": "#10b981"},
    {"id": "MOD_PENTUR", "name": "PENTUR", "color": "#10b981"},
    {"id": "MOD_SUTRAN", "name": "SUTRAN", "color": "#ef4444"},
    {"id": "MOD_MTC", "name": "MTC", "color": "#ef4444"},
    {"id": "MOD_SENAMHI", "name": "SENAMHI", "color": "#ef4444"},
    {"id": "MOD_GDELT", "name": "GDELT", "color": "#ef4444"},
    {"id": "MOD_SERNANP", "name": "SERNANP", "color": "#22c55e"},
    {"id": "MOD_SERFOR", "name": "SERFOR", "color": "#22c55e"},
    {"id": "MOD_MINAM", "name": "MINAM", "color": "#22c55e"},
    {"id": "MOD_OSINERGMIN", "name": "OSINERGMIN", "color": "#22c55e"},
    {"id": "MOD_PROMPERU", "name": "PROMPERU", "color": "#f59e0b"},
    {"id": "MOD_CIXTUR", "name": "CIXTUR", "color": "#f59e0b"},
    {"id": "MOD_RIVALS", "name": "RIVALS", "color": "#f59e0b"},
    {"id": "MOD_GREEN", "name": "GREEN FUNDS", "color": "#f59e0b"},
    {"id": "MOD_COMUNIDADES", "name": "COMUNIDADES", "color": "#3b82f6"},
    {"id": "MOD_INFRA", "name": "INFRAESTRUCTURA", "color": "#3b82f6"},
    {"id": "MOD_FQSAS", "name": "FQSAS", "color": "#3b82f6"},
    {"id": "MOD_SALES", "name": "SALES DNA", "color": "#3b82f6"}
]

for mod in knowledge_modules:
    nodes.append({"id": mod["id"], "name": mod["name"], "group": 2, "val": 10, "color": mod["color"]})

links = []
# CORE to Departments (Bidirectional data flow)
for dep in departments:
    links.append({"source": f"DEP_{dep}", "target": "CORE"})

# Modules to CORE (Direct ingestion)
for mod in knowledge_modules:
    links.append({"source": mod["id"], "target": "CORE"})

# Departments to Modules (Real world connections)
random.seed(42) # Para que la red se vea igual cada vez que recargue
for dep in departments:
    k = random.randint(4, 9)
    chosen_mods = random.sample(knowledge_modules, k)
    for mod in chosen_mods:
        links.append({"source": mod["id"], "target": f"DEP_{dep}"})

# Add explicit heavy connections for Cusco and Arequipa
for mod_id in ["MOD_SERNANP", "MOD_SUTRAN", "MOD_MINCETUR", "MOD_FQSAS", "MOD_GDELT"]:
    links.append({"source": mod_id, "target": "DEP_Cusco"})
    links.append({"source": mod_id, "target": "DEP_Arequipa"})

graph_data = {
    "nodes": nodes,
    "links": links
}

graph_json_str = json.dumps(graph_data)

html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lifextreme - AI Knowledge Brain 3D</title>
    <!-- Load Three.js then 3d-force-graph -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
    <script src="https://unpkg.com/three-spritetext@1.6.5/dist/three-spritetext.min.js"></script>
    <script src="https://unpkg.com/3d-force-graph@1.73.3/dist/3d-force-graph.min.js"></script>
    
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&display=swap" rel="stylesheet">
    <style>
        body {{ margin: 0; padding: 0; overflow: hidden; background-color: #020617; font-family: 'Inter', sans-serif; }}
        #3d-graph {{ width: 100vw; height: 100vh; cursor: crosshair; }}
        
        #title-overlay {{
            position: absolute;
            top: 40px;
            left: 40px;
            z-index: 10;
            pointer-events: none;
            background: rgba(2, 6, 23, 0.7);
            padding: 30px;
            border-radius: 20px;
            border: 1px solid rgba(148, 163, 184, 0.1);
            backdrop-filter: blur(16px);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }}
        h1 {{ margin: 0; font-size: 32px; font-weight: 900; letter-spacing: -1px; color: #f8fafc; text-transform: uppercase; }}
        .gradient-text {{
            background: linear-gradient(to right, #a855f7, #0ea5e9);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        p {{ margin: 12px 0 0 0; color: #94a3b8; font-size: 14px; max-width: 380px; line-height: 1.6; }}
        .stats {{ display: flex; gap: 20px; margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.1); }}
        .stat-box h4 {{ margin: 0; font-size: 24px; color: #f8fafc; }}
        .stat-box span {{ font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 600; letter-spacing: 1px; }}
        .instruction {{ color: #10b981; font-weight: 600; margin-top: 25px; font-size: 12px; display: flex; align-items: center; gap: 8px; }}
        .pulse {{ width: 8px; height: 8px; background: #10b981; border-radius: 50%; box-shadow: 0 0 10px #10b981; animation: blink 1s infinite; }}
        
        @keyframes blink {{ 50% {{ opacity: 0.3; }} }}
    </style>
</head>
<body>
    <div id="title-overlay">
        <h1>LIFEXTREME <span class="gradient-text">CORE</span></h1>
        <p>Topolog&iacute;a Neuronal en Tiempo Real. Red B2B procesando vectores log&iacute;sticos, normativos y ambientales a nivel nacional.</p>
        <div class="stats">
            <div class="stat-box"><h4>244K+</h4><span>Vectores (RAG)</span></div>
            <div class="stat-box"><h4>24</h4><span>Regiones Activas</span></div>
            <div class="stat-box"><h4>20</h4><span>Nodos de Control</span></div>
        </div>
        <div class="instruction"><div class="pulse"></div> EN L&Iacute;NEA - ORBITA PARA EXPLORAR</div>
    </div>
    
    <div id="3d-graph"></div>

    <script>
        const data = {graph_json_str};

        const Graph = ForceGraph3D()
        (document.getElementById('3d-graph'))
            .graphData(data)
            .nodeThreeObject(node => {{
                const group = new THREE.Group();
                
                // Sphere
                const geometry = new THREE.SphereGeometry(node.val * 0.8, 32, 32);
                const material = new THREE.MeshPhysicalMaterial({{
                    color: node.color,
                    transparent: true,
                    opacity: 0.85,
                    roughness: 0.1,
                    transmission: 0.5,
                    emissive: node.color,
                    emissiveIntensity: node.id === 'CORE' ? 0.8 : 0.4
                }});
                const sphere = new THREE.Mesh(geometry, material);
                group.add(sphere);

                // Add a glow/halo for CORE
                if (node.id === 'CORE') {{
                    const haloGeo = new THREE.SphereGeometry(node.val * 1.1, 32, 32);
                    const haloMat = new THREE.MeshBasicMaterial({{
                        color: node.color,
                        transparent: true,
                        opacity: 0.15,
                        side: THREE.BackSide
                    }});
                    const halo = new THREE.Mesh(haloGeo, haloMat);
                    group.add(halo);
                }}

                // Holographic Text
                try {{
                    const sprite = new SpriteText(node.name);
                    sprite.color = '#ffffff';
                    sprite.textHeight = node.id === 'CORE' ? 6 : 4;
                    sprite.fontWeight = 'bold';
                    sprite.fontFace = 'Inter';
                    sprite.position.y = node.val * 0.8 + (node.id === 'CORE' ? 8 : 4);
                    group.add(sprite);
                }} catch (err) {{}}
                
                return group;
            }})
            .linkColor(link => {{
                // Color the links based on the source node group
                const sourceNode = data.nodes.find(n => n.id === link.source.id || n.id === link.source);
                if (sourceNode && sourceNode.group === 2) return sourceNode.color;
                return 'rgba(255, 255, 255, 0.1)';
            }})
            .linkWidth(link => link.source === 'CORE' || link.target === 'CORE' ? 1.5 : 0.5)
            .linkDirectionalParticles(link => link.source === 'CORE' || link.target === 'CORE' ? 4 : 2)
            .linkDirectionalParticleWidth(link => link.source === 'CORE' || link.target === 'CORE' ? 3 : 1.5)
            .linkDirectionalParticleColor(link => {{
                const sourceNode = data.nodes.find(n => n.id === link.source.id || n.id === link.source);
                return sourceNode ? sourceNode.color : '#ffffff';
            }})
            .linkDirectionalParticleSpeed(0.005)
            .backgroundColor('#020617')
            .showNavInfo(false);
            
        // Environment
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        Graph.scene().add(ambientLight);
        
        const pointLight = new THREE.PointLight(0xffffff, 1);
        pointLight.position.set(200, 200, 200);
        Graph.scene().add(pointLight);

        // Core light
        const coreLight = new THREE.PointLight(0xa855f7, 2, 800);
        coreLight.position.set(0, 0, 0);
        Graph.scene().add(coreLight);
            
        // Auto-rotate camera
        let angle = 0;
        const distance = 800;
        setTimeout(() => {{
            setInterval(() => {{
                try {{
                    Graph.cameraPosition({{
                        x: distance * Math.sin(angle),
                        z: distance * Math.cos(angle)
                    }});
                    angle += Math.PI / 2500;
                }} catch(e) {{}}
            }}, 30);
        }}, 2000);
    </script>
</body>
</html>
"""

with open(os.path.join(WEB_DIR, "investor-brain.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ Neural 3D Brain generado en: {os.path.join(WEB_DIR, 'investor-brain.html')}")
