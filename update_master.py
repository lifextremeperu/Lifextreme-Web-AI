import sys

file_path = "Directorio_Nacional_Aventura.md"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# LIMA
content = content.replace(
    "- **San Jerónimo de Surco (Huarochirí):** Formaciones de roca natural empleadas para la escalada.",
    "- **San Jerónimo de Surco (Huarochirí):** Formaciones de roca natural empleadas para la escalada.\n- **Lomas de Lúcumo (Pachacámac):** Sectores de escalada en roca al sur de Lima con vías permanentemente aseguradas."
)

# AREQUIPA
content = content.replace(
    "- Mono Blanco Aventura (Rocódromo y entrenamiento, Av. La Marina 200)",
    "- Mono Blanco Aventura (Rocódromo y entrenamiento, Av. La Marina 200)\n   - Climbing Rooftop (Alto Selva Alegre): Instalación homologada de bouldering con vista panorámica a la ciudad."
)
content = content.replace(
    "6. 🏕️ Parques de Aventura, Puentes Tibetanos y Complejos Temáticos\n   - Complejos de aventura en Mirador de Carmen Alto (Combos de actividades múltiples)",
    "6. 🏕️ Parques de Aventura, Puentes Tibetanos y Complejos Temáticos\n   - Complejos de aventura en Mirador de Carmen Alto (Combos de actividades múltiples)\n\n7. 🏎️ Bases Logísticas y Pistas Cerradas (ATV / Cuatrimotos)\n   - Valle de Chilina: Operación de circuitos de 3 horas por senderos agrestes y material volcánico."
)

# PIURA
content = content.replace(
    "6. 🏕️ Parques de Aventura, Puentes Tibetanos y Complejos Temáticos\n- **Aventura Park Canchaque**: Complejo de aventura que incluye un puente tibetano y Sky Bike (bicicleta aérea).",
    "6. 🏕️ Parques de Aventura, Puentes Tibetanos y Complejos Temáticos\n- **Aventura Park Canchaque**: Complejo de aventura que incluye un puente tibetano y Sky Bike (bicicleta aérea).\n\n7. 🏎️ Bases Logísticas y Pistas Cerradas (ATV / Cuatrimotos)\n- **Bases Máncora ATV:** Polígonos perimetrales y centros base de infraestructura de alquiler para cuatrimotos todoterreno en el eje costero."
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated Directorio_Nacional_Aventura.md")
