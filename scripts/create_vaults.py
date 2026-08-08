import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

def create_isolated_vaults():
    # Conectar a Qdrant local
    client = QdrantClient("localhost", port=6333)
    
    vaults_to_create = [
        "Lifextreme_Partners_Vault",
        "Lifextreme_Marketing_Vault",
        "Lifextreme_CEO_Vault"
    ]
    
    existing_collections = [c.name for c in client.get_collections().collections]
    print(f"Colecciones existentes: {existing_collections}")
    
    for vault_name in vaults_to_create:
        if vault_name not in existing_collections:
            print(f"Creando bóveda aislada: {vault_name}...")
            # nomic-embed-text usa 768 dimensiones
            client.create_collection(
                collection_name=vault_name,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE),
            )
            print(f"Bóveda {vault_name} creada con éxito.")
        else:
            print(f"Bóveda {vault_name} ya existe. Saltando...")

if __name__ == "__main__":
    create_isolated_vaults()
