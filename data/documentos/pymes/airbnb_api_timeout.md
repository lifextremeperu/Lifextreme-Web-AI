# Airbnb API Connectivity Guidelines para Channel Managers

La infraestructura de microservicios de Airbnb es sumamente estricta respecto al rendimiento y la disponibilidad de los Channel Managers de los hoteles (ej. SiteMinder, Cloudbeds).

## Latencia Superior a 3000 Milisegundos
El límite estricto de timeout (tiempo de espera máximo) para una respuesta de sincronización de disponibilidad o tarifas desde el Channel Manager es de **3000 milisegundos (3 segundos)**.

## Tasa de Desconexión y Códigos de Error
* Si la latencia supera los 3000 ms, la pasarela de Airbnb corta la conexión para proteger sus propios servidores.
* Esto genera un código de error interno **HTTP 504 Gateway Timeout**.
* **Tasa de Timeout (Timeout Rate):** Si la API registra más del 5% de errores 504 en una ventana de 1 hora, el algoritmo de Airbnb penaliza temporalmente la propiedad, reduciendo su visibilidad en el mapa y desactivando el Instant Book (Reserva Inmediata) por riesgo de overbooking, hasta que la conexión se estabilice por debajo de los 1000ms.
