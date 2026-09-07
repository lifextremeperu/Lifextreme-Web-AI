import json
from duckduckgo_search import DDGS

try:
    with DDGS() as ddgs:
        results = list(ddgs.maps("parque de aventura cusco peru", max_results=3))
        print(json.dumps(results, indent=2, ensure_ascii=False))
except Exception as e:
    print("Error:", e)
