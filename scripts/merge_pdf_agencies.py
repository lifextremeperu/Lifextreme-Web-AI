import os
import sys
import sqlite3
import pdfplumber
import re

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "outreach_tracker.db")
PDF_PATH = r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\LIFEXTREME\CARTERA CUSCO- AGENCIAS DE VIAJES.pdf"

print("==================================================")
print(" 🔄 CONSOLIDADOR B2B: LEYENDO PDF Y FUSIONANDO")
print("==================================================")

def clean_text(text):
    if not text:
        return ""
    return str(text).replace('\n', ' ').strip().upper()

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prospects (
            ruc TEXT PRIMARY KEY,
            razon_social TEXT,
            nombre_comercial TEXT,
            web TEXT,
            region TEXT,
            email TEXT,
            status TEXT DEFAULT 'PENDING',
            sent_date TEXT,
            pitch_text TEXT,
            enriched_profile TEXT
        )
    ''')
    conn.commit()
    return conn

def extract_from_pdf():
    print(f"[*] Leyendo PDF: {os.path.basename(PDF_PATH)}...")
    agencies = []
    try:
        with pdfplumber.open(PDF_PATH) as pdf:
            total_pages = len(pdf.pages)
            for i, page in enumerate(pdf.pages):
                print(f"    - Extrayendo página {i+1}/{total_pages}...")
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        # Asumimos que la tabla tiene columnas. 
                        # Intentamos detectar RUC, Nombre, Correo.
                        row_text = " | ".join([str(c) for c in row if c])
                        
                        # Buscamos RUC con Regex (11 digitos que empiezan con 10 o 20)
                        ruc_match = re.search(r'\b(10|20)\d{9}\b', row_text)
                        ruc = ruc_match.group(0) if ruc_match else ""
                        
                        # Buscamos correos
                        email_match = re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', row_text, re.IGNORECASE)
                        email = email_match.group(0).lower() if email_match else ""
                        
                        # El nombre suele estar al principio o es texto largo
                        cols_clean = [clean_text(c) for c in row if c]
                        
                        # Heuristica simple para el nombre: texto mas largo que no es correo ni numero
                        nombre = ""
                        for c in cols_clean:
                            if len(c) > 5 and '@' not in c and not re.match(r'^\d+$', c):
                                nombre = c
                                break
                                
                        if nombre or ruc or email:
                            agencies.append({
                                'ruc': ruc,
                                'nombre': nombre,
                                'email': email,
                                'raw_text': row_text
                            })
        print(f"[✔] Se encontraron {len(agencies)} posibles registros en el PDF.")
        return agencies
    except Exception as e:
        print(f"[-] Error leyendo PDF (Asegúrate de haber instalado pdfplumber): {e}")
        return []

def merge_agencies(conn, pdf_agencies):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM prospects")
    initial_count = cursor.fetchone()[0]
    
    print(f"[*] Total actual en Base de Datos: {initial_count} agencias.")
    print("[*] Cruzando listas y eliminando duplicados...")
    
    inserted = 0
    updated = 0
    duplicados = 0
    
    for ag in pdf_agencies:
        if not ag['email'] and not ag['ruc']:
            continue # Ignorar si no hay ni correo ni ruc
            
        # Revisar si existe por correo o por ruc
        cursor.execute("SELECT ruc, email FROM prospects WHERE email = ? OR (ruc = ? AND ruc != '')", (ag['email'], ag['ruc']))
        row = cursor.fetchone()
        
        if row:
            duplicados += 1
            # Se podria actualizar info si falta, por ejemplo si ahora tenemos el RUC
            existing_ruc, existing_email = row
            if not existing_ruc and ag['ruc']:
                cursor.execute("UPDATE prospects SET ruc = ? WHERE email = ?", (ag['ruc'], existing_email))
                updated += 1
        else:
            # Nuevo registro
            try:
                # Generamos un RUC temporal si no tiene para la PK
                ruc = ag['ruc'] if ag['ruc'] else f"TMP_{abs(hash(ag['email']))}"
                
                cursor.execute('''
                    INSERT INTO prospects (ruc, razon_social, nombre_comercial, web, region, email)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (ruc, ag['nombre'], ag['nombre'], '', 'Cusco (PDF)', ag['email']))
                inserted += 1
            except sqlite3.IntegrityError:
                duplicados += 1
                
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM prospects")
    final_count = cursor.fetchone()[0]
    
    print("-" * 50)
    print(" 📊 REPORTE DE CONSOLIDACION")
    print("-" * 50)
    print(f"  - Agencias detectadas en PDF: {len(pdf_agencies)}")
    print(f"  - Agencias duplicadas (Omitidas): {duplicados}")
    print(f"  - Registros actualizados con nueva info: {updated}")
    print(f"  - NUEVAS agencias añadidas a la Master: {inserted}")
    print("-" * 50)
    print(f" 🏆 TOTAL EN LISTA MASTER AHORA: {final_count} AGENCIAS")
    print("-" * 50)

if __name__ == "__main__":
    conn = init_db()
    pdf_agencies = extract_from_pdf()
    if pdf_agencies:
        merge_agencies(conn, pdf_agencies)
    conn.close()
    print("\n[✔] Proceso de consolidación terminado. Presiona cualquier tecla para cerrar.")
    os.system("pause >nul")
