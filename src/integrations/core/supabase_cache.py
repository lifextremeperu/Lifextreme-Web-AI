from datetime import datetime, timedelta

class SupabaseCacheMock:
    """
    Simulador de la caché de Supabase.
    Regla: No llamar a APIs comerciales si el evento ocurrió hace < 60 mins.
    """
    def __init__(self):
        self.cache = {}
        
    def get_or_set(self, key: str, fetch_function, ttl_minutes=60):
        now = datetime.now()
        
        # Verificar caché
        if key in self.cache:
            data, timestamp = self.cache[key]
            if now - timestamp < timedelta(minutes=ttl_minutes):
                print(f"[CACHÉ] ⚡ Hit de caché en '{key}'. Evitando llamada a API.")
                return data
                
        # Si no está en caché o expiró, ejecutar la función (llamada a API)
        print(f"[CACHÉ] 🌍 Miss de caché en '{key}'. Llamando a API...")
        fresh_data = fetch_function()
        
        # Guardar en caché
        self.cache[key] = (fresh_data, now)
        return fresh_data

# Instancia singleton
cache = SupabaseCacheMock()
