import os
import sys
import requests
import time
from dotenv import load_dotenv
from supabase import create_client

sys.stdout.reconfigure(encoding='utf-8')

API_URL = "http://127.0.0.1:8000/chat"
OLLAMA_URL = "http://localhost:11434/api/chat"

load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

PROFILE = {
    "system": "Eres Marcos, un turista decidido. Tienes tu tarjeta de crédito en la mano. Quieres ir a Choquequirao con tu esposa (2 personas en total) para el 15 de Octubre. Quieres comprar el paquete YA MISMO. Eres directo y exiges un link de pago. Si el vendedor te pide datos, dáselos de inmediato. Si te da un link, dile 'Gracias, acabo de pagarlo'.",
    "init_msg": "Hola. Quiero comprar el tour a Choquequirao. Somos 2 personas para el 15 de Octubre. Mi nombre es Marcos Ruiz. Dame el link para pagar."
}

def ask_max(message):
    try:
        res = requests.post(API_URL, json={"message": message}, timeout=60)
        if res.ok:
            return res.json().get('mensaje_principal', 'Sin mensaje')
        return f"Error HTTP {res.status_code}"
    except Exception as e:
        return f"Error de conexión con MAX: {e}"

def ask_marcos(chat_history):
    messages = [{"role": "system", "content": PROFILE["system"]}]
    for msg in chat_history:
        messages.append(msg)
    
    try:
        res = requests.post(OLLAMA_URL, json={
            "model": "qwen2.5:7b",
            "messages": messages,
            "stream": False
        }, timeout=90)
        return res.json()['message']['content']
    except Exception as e:
        return f"Error de Ollama: {e}"

def simulate_payment(url):
    print(f"\n      [💳 CLIENTE SINTÉTICO] ¡LINK DE PAGO DETECTADO!")
    print(f"      [💳 CLIENTE SINTÉTICO] Extrayendo URL: {url}")
    
    # Extraer booking_id
    booking_id = None
    if "booking_id=" in url:
        part = url.split("booking_id=")[1]
        booking_id = part.split("&")[0]
        
    if booking_id:
        print(f"      [💳 CLIENTE SINTÉTICO] Procesando pago simulado en Supabase para Reserva ID: {booking_id}...")
        time.sleep(2) # Simular tiempo de poner tarjeta
        try:
            # Actualizar DB
            supabase.table('bookings').update({"status": "paid"}).eq("id", booking_id).execute()
            print(f"      [✅ CLIENTE SINTÉTICO] PAGO EXITOSO. Reserva marcada como 'paid' en la base de datos.")
            return True
        except Exception as e:
            print(f"      [❌ CLIENTE SINTÉTICO] Error pagando en Supabase: {e}")
            return False
    else:
        print("      [!] No se encontró booking_id en la URL.")
        return False

def run_e2e_simulation():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("==================================================================")
    print(" 🚀 INICIANDO SIMULACIÓN END-TO-END: VENTA AUTÓNOMA (M2M) ")
    print("==================================================================")
    
    start_time = time.time()
    chat_history = []
    
    msg_user = PROFILE["init_msg"]
    print(f"👤 Marcos (Cliente): {msg_user}")
    chat_history.append({"role": "assistant", "content": msg_user})
    
    sale_closed = False
    
    for turn in range(5): # Max 5 turnos para cerrar la venta
        print("\n🤖 MAX (Pensando y ejecutando herramientas...)")
        msg_max = ask_max(msg_user)
        print(f"🤖 MAX: {msg_max}")
        chat_history.append({"role": "user", "content": msg_max})
        
        # Interceptar link de pago
        if "http" in msg_max and "payment" in msg_max:
            # Extraer link
            words = msg_max.split()
            link = next((w for w in words if "http" in w), None)
            if link:
                success = simulate_payment(link)
                if success:
                    sale_closed = True
                    break
                    
        if turn < 4:
            print(f"\n👤 Marcos (Pensando...)")
            msg_user = ask_marcos(chat_history)
            print(f"👤 Marcos (Cliente): {msg_user}")
            chat_history.append({"role": "assistant", "content": msg_user})
            
    end_time = time.time()
    duration = round(end_time - start_time, 2)
    
    print("\n==================================================================")
    print(" 📊 REPORTE DE AUDITORÍA DE FLUJO DE VENTAS ")
    print("==================================================================")
    if sale_closed:
        print(f"✅ ESTADO: Venta cerrada exitosamente de forma 100% autónoma.")
        print(f"⏱️ TIEMPO (Time-to-Close): {duration} segundos.")
        print(f"💬 INTERACCIONES: {turn + 1} turnos.")
        print(f"🚀 FRICCIÓN: Baja. El flujo transaccional se completó sin intervención humana.")
    else:
        print(f"❌ ESTADO: Venta NO cerrada.")
        print(f"⏱️ TIEMPO INVERTIDO: {duration} segundos.")
        print(f"⚠️ FRICCIÓN: Alta. MAX no logró entregar el link de pago o el cliente se atascó.")
        print(f"🔍 DIAGNÓSTICO: Revisa el prompt de MAX para asegurarte que llame al tool_crear_reserva.")
    print("==================================================================")

if __name__ == "__main__":
    run_e2e_simulation()
