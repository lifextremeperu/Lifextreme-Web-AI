import requests
import json

def buscar_osm(query_area, node_type):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    area[name="{query_area}"]->.searchArea;
    (
      node["leisure"="{node_type}"](area.searchArea);
      way["leisure"="{node_type}"](area.searchArea);
      relation["leisure"="{node_type}"](area.searchArea);
      node["sport"="climbing"](area.searchArea);
      node["tourism"="theme_park"](area.searchArea);
    );
    out center;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
    
    for element in data['elements']:
        if 'tags' in element and 'name' in element['tags']:
            lat = element.get('lat') or element.get('center', {}).get('lat')
            lon = element.get('lon') or element.get('center', {}).get('lon')
            print(f"Name: {element['tags']['name']} (Lat: {lat}, Lon: {lon})")

try:
    buscar_osm("Cusco", "park")
except Exception as e:
    print("Error:", e)
