"""
Registro y Rescate de Correos con Error de Tipeo
------------------------------------------------
Detecta correos con errores de dominio en las tablas de prospectos
(ej. @htomail.com, @outloo.com, @outook.com, @gmail.con, @gmil.com, @yaju.com),
los registra en reportes_b2b/correos_errores_registrados.json y crea la tabla
prospectos_rescate_errores en SQLite para reenviarlos corregidos.
"""

import json
import os
import sqlite3

DB_PATH = os.path.join("reportes_b2b", "prospectos_cusco.db")
OUT_JSON = os.path.join("reportes_b2b", "correos_errores_registrados.json")

TYPO_MAP = {
    "@gmil.com": "@gmail.com",
    "@gmail.con": "@gmail.com",
    "@outook.com": "@outlook.com",
    "@outloo.com": "@outlook.com",
    "@outlok.com": "@outlook.com",
    "@htomail.com": "@hotmail.com",
    "@hotmial.com": "@hotmail.com",
    "@yaju.com": "@yahoo.com",
    "@yahuoo.com": "@yahoo.com",
}


def fix_email(email: str):
    low = email.strip().lower()
    for bad, good in TYPO_MAP.items():
        if low.endswith(bad):
            return low[: -len(bad)] + good
    return None


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'prospectos_lote%'"
    )
    tables = sorted(r["name"] for r in cur.fetchall())

    rescued = []
    seen_fixed = set()

    for tbl in tables:
        rows = cur.execute(f"SELECT * FROM {tbl}").fetchall()
        for row in rows:
            fixed = fix_email(row["email"])
            if fixed and fixed not in seen_fixed:
                seen_fixed.add(fixed)
                rescued.append(
                    {
                        "lote_origen": tbl,
                        "nombre": row["nombre"],
                        "saludo_nombre": row["saludo_nombre"] or "Director/a",
                        "email_original": row["email"],
                        "email": fixed,
                        "web": row["web"],
                        "clase": row["clase"],
                        "tipo": row["tipo"],
                        "telefono": row["telefono"],
                        "ruc": row["ruc"],
                        "rep_legal": row["rep_legal"],
                        "score": row["score"] if "score" in row.keys() else 0,
                        "segmento": row["segmento"] if "segmento" in row.keys() else "",
                    }
                )

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(rescued, f, ensure_ascii=False, indent=2)

    cur.execute("DROP TABLE IF EXISTS prospectos_rescate_errores")
    cur.execute(
        """
        CREATE TABLE prospectos_rescate_errores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            saludo_nombre TEXT,
            email TEXT UNIQUE NOT NULL,
            email_original TEXT,
            lote_origen TEXT,
            web TEXT,
            clase TEXT,
            tipo TEXT,
            telefono TEXT,
            ruc TEXT,
            rep_legal TEXT,
            score INTEGER,
            segmento TEXT,
            lote INTEGER DEFAULT 99,
            estado TEXT DEFAULT 'PENDIENTE',
            intentos INTEGER DEFAULT 0,
            resend_id TEXT,
            error_msg TEXT,
            enviado_at TIMESTAMP,
            creado_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    for p in rescued:
        saludo = p["saludo_nombre"]
        if not saludo or saludo.strip() == "-":
            saludo = "Director/a"
        cur.execute(
            """
            INSERT INTO prospectos_rescate_errores
            (nombre, saludo_nombre, email, email_original, lote_origen, web, clase, tipo, telefono, ruc, rep_legal, score, segmento, lote)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 99)
            """,
            (
                p["nombre"],
                saludo,
                p["email"],
                p["email_original"],
                p["lote_origen"],
                p["web"],
                p["clase"],
                p["tipo"],
                p["telefono"],
                p["ruc"],
                p["rep_legal"],
                p["score"],
                p["segmento"],
            ),
        )

    conn.commit()
    conn.close()

    print(f"Registrados {len(rescued)} correos con error de tipeo:")
    for r in rescued:
        print(f" - [{r['lote_origen']}] {r['nombre']}: {r['email_original']} -> {r['email']}")


if __name__ == "__main__":
    main()
