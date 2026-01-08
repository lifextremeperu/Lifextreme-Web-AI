import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuración
const INPUT_FILE = 'tours_faq.csv';
const OUTPUT_FILE = 'js/knowledge_base.json';

// Función principal
function processCSV() {
    try {
        const csvPath = path.join(__dirname, INPUT_FILE);
        const csvContent = fs.readFileSync(csvPath, 'utf8');

        // Separar por líneas manejando Windows (CRLF) y Unix (LF)
        const lines = csvContent.split(/\r?\n/);

        // Empezamos desde la línea 3 (index 2)
        const dataLines = lines.slice(2).filter(line => line.trim() !== '');

        const faqs = [];

        dataLines.forEach((line, index) => {
            let question = '';
            let answer = '';

            // Lógica de parseo CSV para 2 columnas
            if (line.startsWith('"')) {
                // Caso: La pregunta tiene comillas (ej: "Hola, mundo",Respuesta)
                // Buscamos la comilla de cierre seguida de coma
                // Nota: Esto es simplificado. El regex real de CSV es complejo.
                // Asumimos que la pregunta termina en `",`
                const splitIndex = line.indexOf('",');
                if (splitIndex !== -1) {
                    question = line.substring(1, splitIndex).replace(/""/g, '"');
                    answer = line.substring(splitIndex + 2);
                } else {
                    // Fallback malo o línea corrupta, intentar split simple
                    const firstComma = line.indexOf(',');
                    question = line.substring(0, firstComma);
                    answer = line.substring(firstComma + 1);
                }
            } else {
                // Caso normal: Pregunta,Respuesta...
                const firstComma = line.indexOf(',');
                if (firstComma !== -1) {
                    question = line.substring(0, firstComma);
                    answer = line.substring(firstComma + 1);
                }
            }

            if (question && answer) {
                // Limpiar comillas extras en la respuesta si es que Excel las puso
                answer = answer.trim();
                if (answer.startsWith('"') && answer.endsWith('"')) {
                    answer = answer.slice(1, -1).replace(/""/g, '"');
                }

                // Limpieza extra
                question = question.trim();

                // Auto-categorización
                let category = 'General';
                const qLower = question.toLowerCase();

                if (qLower.match(/precio|costo|entrada|boleto|ticket|cuánto|cuanto|pagar/)) category = 'Precios y Entradas';
                else if (qLower.match(/clima|lluvia|época|epoca|mes|frío|calor|temperatura/)) category = 'Clima y Temporadas';
                else if (qLower.match(/altura|soroche|salud|física|cansado|oxígeno|oxigeno/)) category = 'Salud y Altura';
                else if (qLower.match(/llevar|ropa|equipo|mochila|zapatos|botas/)) category = 'Equipaje y Ropa';
                else if (qLower.match(/transporte|bus|tren|recogida|llegar|taxi|vuelo/)) category = 'Logística y Transporte';
                else if (qLower.match(/comida|almuerzo|cena|desayuno|agua|restaurante/)) category = 'Alimentación';
                else if (qLower.match(/niños|edad|familia|bebé|embarazada/)) category = 'Familia y Restricciones';
                else if (qLower.match(/machu|city tour|montaña|laguna|valle|camino inca/)) category = 'Destinos';

                faqs.push({
                    id: `faq-${index + 1}`,
                    question: question,
                    answer: answer,
                    category: category
                });
            }
        });

        // Guardar resultado
        const jsonOutput = {
            metadata: {
                total_faqs: faqs.length,
                generated_at: new Date().toISOString(),
                source: "Lifextreme Knowledge Base"
            },
            categories: [...new Set(faqs.map(f => f.category))],
            data: faqs
        };

        const outputPath = path.join(__dirname, OUTPUT_FILE);
        fs.writeFileSync(outputPath, JSON.stringify(jsonOutput, null, 2), 'utf8');

        console.log(`✅ Conversión completada!`);
        console.log(`📊 Total FAQs procesadas: ${faqs.length}`);
        console.log(`📂 Archivo guardado en: ${OUTPUT_FILE}`);

    } catch (error) {
        console.error("❌ Error procesando el archivo:", error);
    }
}

processCSV();
