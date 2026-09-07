from geopy.geocoders import Nominatim
import json

geolocator = Nominatim(user_agent="lifextreme_geo_agent")
try:
    # Búsqueda estructurada
    locations = geolocator.geocode("parque de aventura cusco peru", exactly_one=False, limit=3)
    if locations:
        for loc in locations:
            print(f"Name: {loc.address}")
            print(f"Lat: {loc.latitude}, Lng: {loc.longitude}")
            print(loc.raw)
            print("-" * 20)
    else:
        print("No results found.")
except Exception as e:
    print(f"Error: {e}")
