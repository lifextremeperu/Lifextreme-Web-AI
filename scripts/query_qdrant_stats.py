import httpx

QDRANT_URL = "http://127.0.0.1:6333"

def get_unique_fields(collection, field_name):
    unique_values = set()
    offset = None
    
    while True:
        payload = {
            "limit": 1000,
            "with_payload": True,
            "with_vector": False
        }
        if offset:
            payload["offset"] = offset
            
        r = httpx.post(f"{QDRANT_URL}/collections/{collection}/points/scroll", json=payload)
        if r.status_code != 200:
            print(f"Failed to query {collection}: {r.text}")
            break
            
        data = r.json().get("result", {})
        points = data.get("points", [])
        if not points:
            break
            
        for p in points:
            val = p.get("payload", {}).get(field_name)
            if val:
                unique_values.add(val)
                
        offset = data.get("next_page_offset")
        if not offset:
            break
            
    return list(unique_values)

print("Regions in Lifextreme_Knowledge:")
for r in get_unique_fields("Lifextreme_Knowledge", "region"):
    print("-", r)

print("\nSources in lifextreme:")
for s in get_unique_fields("lifextreme", "source"):
    print("-", s)
