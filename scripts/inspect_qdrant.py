import httpx
import json

QDRANT_URL = "http://127.0.0.1:6333"

def main():
    try:
        # Get collections
        r = httpx.get(f"{QDRANT_URL}/collections")
        r.raise_for_status()
        collections = r.json().get("result", {}).get("collections", [])
        
        print("--- QDRANT COLLECTIONS ---")
        if not collections:
            print("No collections found.")
            return

        for col in collections:
            name = col["name"]
            print(f"\nCollection: {name}")
            
            # Get collection info
            r_info = httpx.get(f"{QDRANT_URL}/collections/{name}")
            if r_info.status_code == 200:
                info = r_info.json().get("result", {})
                print(f"Status: {info.get('status')}")
                print(f"Points Count: {info.get('points_count')}")
                print(f"Vectors Count: {info.get('vectors_count')}")
                
                config = info.get("config", {})
                params = config.get("params", {})
                vectors_config = params.get("vectors", {})
                print(f"Vector Dimensions: {vectors_config.get('size')} | Distance: {vectors_config.get('distance')}")
                
                # Fetch a sample point
                r_sample = httpx.post(
                    f"{QDRANT_URL}/collections/{name}/points/scroll",
                    json={"limit": 1, "with_payload": True, "with_vector": False}
                )
                if r_sample.status_code == 200:
                    points = r_sample.json().get("result", {}).get("points", [])
                    if points:
                        print("Sample Payload Schema:")
                        sample_payload = points[0].get("payload", {})
                        for key, value in sample_payload.items():
                            print(f"  - {key}: {type(value).__name__}")
                        print("\nSample Data (First Point):")
                        print(json.dumps(sample_payload, indent=2))
                    else:
                        print("No points found in collection.")
            else:
                print(f"Failed to get info for {name}: {r_info.text}")

    except Exception as e:
        print(f"Error connecting to Qdrant: {e}")

if __name__ == '__main__':
    main()
