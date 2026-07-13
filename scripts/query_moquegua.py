import httpx
import json

QDRANT_URL = "http://127.0.0.1:6333"

def main():
    try:
        query_payload = {
            "filter": {
                "must": [
                    {
                        "key": "region",
                        "match": {
                            "value": "moquegua"
                        }
                    }
                ]
            },
            "limit": 100,
            "with_payload": True,
            "with_vector": False
        }
        
        r = httpx.post(f"{QDRANT_URL}/collections/Lifextreme_Knowledge/points/scroll", json=query_payload)
        r.raise_for_status()
        points = r.json().get("result", {}).get("points", [])
        
        print(f"Found {len(points)} points for Moquegua:")
        for i, p in enumerate(points):
            payload = p.get("payload", {})
            print(f"{i+1}. {payload.get('text_content')}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
