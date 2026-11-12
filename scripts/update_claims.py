"""
update_claims.py
Actualiza la redacción comercial de los expedientes para pasar de afirmaciones infladas
a un tono técnico, formal y riguroso de auditoría (Big-4 style).
"""

with open("scripts/corporate_dossier_builder.py", "r", encoding="utf-8") as f:
    text = f.read()

replaces = [
    ("(RAGAS 99.17% Verified)", "(Evaluación RAGAS Audit Grade)"),
    ("(`RAGAS Score 99.17%`), garantizando consultas con **0% de alucinación**.", "bajo arquitectura RAG con alta fidelidad documental y verificación de fuentes oficiales."),
    ("bajo Estándar RAGAS (99.17%)", "bajo Estándar RAGAS y Pruebas de Estrés Normativo"),
    ("Certificado Corporativo de Auditoría", "Informe de Auditoría y Dictamen de Adecuación"),
    ("Certificado Corporativo de Gobernanza IA", "Dictamen y Plan Maestro de Gobernanza IA"),
    ("Certificado Corporativo de Gobernanza de IA (4 Firmas).", "Dictamen Final de Cumplimiento y Gobernanza de IA (4 Especialistas)."),
    ("Cerebro Jurídico y Técnico Auditado con 99.17% de Precisión RAGAS", "Bóveda Vectorial Especializada en Normativa Peruana e ISO 42001"),
    ("Score RAGAS 99.17%", "Evaluación RAGAS"),
    ("7. EVIDENCIA CIENTÍFICA DE NUESTRA TECNOLOGÍA | AUDITORÍA RAGAS 99.17%", "7. BENCHMARKING TÉCNICO Y EVALUACIÓN DE ARQUITECTURA RAG"),
    ("99.17% RAGAS Score", "Evaluación RAGAS Enterprise"),
    ("07. Reporte de Trazabilidad Normativa RAGAS (99.17%).", "07. Informe Técnico de Trazabilidad Normativa y Calidad RAG."),
    ("| Auditoría Verificada con Qdrant RAG (99.17% RAGAS).", "| Arquitectura RAG de Alta Precisión sobre Qdrant.")
]

for old, new in replaces:
    text = text.replace(old, new)

with open("scripts/corporate_dossier_builder.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Actualización completada en corporate_dossier_builder.py.")
