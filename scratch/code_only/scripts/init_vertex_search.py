import os
import sys
from google.cloud import aiplatform

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "project-7ccd00cc-f448-42df-90a")
REGION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
INDEX_NAME = "lifextreme_vector_index_v2"
ENDPOINT_NAME = "lifextreme_vector_endpoint_v2"

def init_vector_search():
    print(f"Iniciando configuración de Vertex AI Vector Search en {REGION}...")
    aiplatform.init(project=PROJECT_ID, location=REGION)
    
    # 1. Crear el Index (Toma mucho tiempo, ~30-40 min)
    print("Paso 1: Creando el Índice (esto puede tardar hasta 45 minutos)...")
    try:
        # Check if exists
        indexes = aiplatform.MatchingEngineIndex.list(filter=f"display_name={INDEX_NAME}")
        if indexes:
            my_index = indexes[0]
            print(f"El índice ya existe con ID: {my_index.name}")
        else:
            my_index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
                display_name=INDEX_NAME,
                dimensions=768, # para text-embedding-004
                approximate_neighbors_count=150,
                description="Indice para busqueda semantica de Lifextreme",
                index_update_method="STREAM_UPDATE"
            )
            print(f"Índice creado exitosamente: {my_index.name}")
    except Exception as e:
        print(f"Error creando índice: {e}")
        return

    # 2. Crear el Endpoint
    print("Paso 2: Creando el Endpoint...")
    try:
        endpoints = aiplatform.MatchingEngineIndexEndpoint.list(filter=f"display_name={ENDPOINT_NAME}")
        if endpoints:
            my_index_endpoint = endpoints[0]
            print(f"El endpoint ya existe con ID: {my_index_endpoint.name}")
        else:
            my_index_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
                display_name=ENDPOINT_NAME,
                public_endpoint_enabled=True
            )
            print(f"Endpoint creado: {my_index_endpoint.name}")
    except Exception as e:
        print(f"Error creando endpoint: {e}")
        return

    # 3. Desplegar el Index en el Endpoint (Toma ~20 min)
    print("Paso 3: Desplegando el índice en el endpoint (esto toma ~20 minutos)...")
    try:
        # Check if already deployed
        is_deployed = False
        for deployed_index in my_index_endpoint.deployed_indexes:
            if deployed_index.index == my_index.resource_name:
                is_deployed = True
                print("El índice ya está desplegado en este endpoint.")
                break
                
        if not is_deployed:
            my_index_endpoint.deploy_index(
                index=my_index, 
                deployed_index_id="lifextreme_deployed_index_1"
            )
            print("Despliegue completado.")
    except Exception as e:
        print(f"Error desplegando índice: {e}")
        return

    print("\n--- RESUMEN DE INSTALACIÓN ---")
    print("Añade estas variables a tu entorno de Cloud Run o a tu .env local:")
    print(f"VECTOR_SEARCH_INDEX_ID={my_index.name.split('/')[-1]}")
    print(f"VECTOR_SEARCH_ENDPOINT_ID={my_index_endpoint.name.split('/')[-1]}")

if __name__ == "__main__":
    init_vector_search()
