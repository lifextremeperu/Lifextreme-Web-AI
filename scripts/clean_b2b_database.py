import sqlite3
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "outreach_tracker.db")

def clean_database():
    print("=" * 50)
    print(" 🧹 LIMPIEZA Y CURACIÓN DE BASE DE DATOS B2B ")
    print("=" * 50)
    
    if not os.path.exists(DB_PATH):
        print("[-] La base de datos no existe.")
        return
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Total inicial
    cursor.execute("SELECT COUNT(*) FROM prospects")
    total_inicial = cursor.fetchone()[0]
    print(f"[*] Registros iniciales: {total_inicial}")
    
    # 2. Capitalizar nombres (Estandarización)
    cursor.execute("SELECT ruc, nombre_comercial, razon_social FROM prospects")
    rows = cursor.fetchall()
    updated_names = 0
    for ruc, nombre, razon in rows:
        n_nombre = str(nombre).title() if nombre else ''
        n_razon = str(razon).title() if razon else ''
        if n_nombre != nombre or n_razon != razon:
            cursor.execute("UPDATE prospects SET nombre_comercial = ?, razon_social = ? WHERE ruc = ?", (n_nombre, n_razon, ruc))
            updated_names += 1
            
    print(f"[+] Nombres estandarizados: {updated_names}")
    
    # 3. Limpiar Correos Invalidos
    cursor.execute("DELETE FROM prospects WHERE email NOT LIKE '%@%.%' OR email IS NULL OR email = ''")
    deleted_emails = cursor.rowcount
    print(f"[+] Correos inválidos eliminados: {deleted_emails}")
    
    # 4. Eliminar Duplicados (por correo exacto manteniendo el primero)
    cursor.execute("""
        DELETE FROM prospects
        WHERE rowid NOT IN (
            SELECT MIN(rowid)
            FROM prospects
            GROUP BY email
        )
    """)
    duplicados = cursor.rowcount
    print(f"[+] Registros duplicados fusionados/eliminados: {duplicados}")
    
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM prospects")
    total_final = cursor.fetchone()[0]
    print(f"\n[✔] Limpieza completada. Total final en Master: {total_final} agencias.")
    print("=" * 50)
    
    conn.close()

if __name__ == "__main__":
    clean_database()
