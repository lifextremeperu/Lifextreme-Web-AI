import os
import json
import requests
import zipfile
from pathlib import Path
from tqdm import tqdm

def download_file(url, dest_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))
    
    with open(dest_path, 'wb') as file, tqdm(
        desc=dest_path.name,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

def main():
    json_path = Path("data/tupas_links.json")
    output_dir = Path("data/tupas")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    direct_links = data.get("direct_links", {})
    
    print(f"🚀 Iniciando descarga de {len(direct_links)} TUPAs regionales...\n")
    
    for region, url in direct_links.items():
        try:
            # Check if it's the Loreto zip
            if ".zip" in url:
                file_name = f"TUPA_{region}.zip"
            else:
                file_name = f"TUPA_{region}.pdf"
                
            dest_path = output_dir / file_name
            
            if dest_path.exists():
                print(f"✅ {region} ya existe. Saltando...")
                continue
                
            print(f"⬇️ Descargando {region}...")
            download_file(url, dest_path)
            
            # Unzip if it's a zip file
            if file_name.endswith('.zip'):
                print(f"📦 Descomprimiendo {region}...")
                with zipfile.ZipFile(dest_path, 'r') as zip_ref:
                    zip_ref.extractall(output_dir / f"TUPA_{region}")
                print(f"✅ {region} descomprimido.")
                
        except Exception as e:
            print(f"❌ Error al descargar {region}: {e}")

    print("\n✅ Proceso de descarga estática finalizado.")
    print(f"📂 Los archivos se encuentran en: {output_dir.resolve()}")

if __name__ == "__main__":
    main()
