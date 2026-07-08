import time
from telegram_notifier import (
    notify_start,
    notify_fase1_complete,
    notify_fase2_batch,
    notify_department_complete
)

print("Enviando secuencias de prueba de Telegram DMO-v2.0...")

# 1. Start
print("Enviando START...")
notify_start("Cusco", "Perú", "run_a1b2c3", "A", "95")
time.sleep(3)

# 2. Fase 1
print("Enviando FASE 1 COMPLETE...")
notify_fase1_complete("Cusco", "Perú", 95, 3, "camino_inca, machu_picchu", 4500, 0.015)
time.sleep(3)

# 3. Fase 2 Batch
print("Enviando FASE 2 BATCH...")
notify_fase2_batch("Cusco", "Perú", 50, 95, 480, 15, 5, 85000, 0.25, 17)
time.sleep(3)

# 4. Department Complete
print("Enviando DEPARTAMENTO COMPLETADO...")
notify_department_complete(
    departamento="Cusco", 
    pais="Perú", 
    total_modulos=95, 
    total_fqsas=9500, 
    aprobadas=9200, 
    pct_aprobadas=96.8, 
    human_review=5, 
    errores=2, 
    horas=4, 
    min=15, 
    costo_usd=1.45, 
    siguiente_dept="Lima"
)

print("¡Prueba finalizada! Revisa tu Telegram.")
