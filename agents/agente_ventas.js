import { appendFileSync } from 'fs';
import { join } from 'path';

const API_KEY = process.env.GEMINI_API_KEY || "AIzaSyA32fTZKcDN-54dfHpSR8KaeTu3KJ9Wu3M";
const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key=${API_KEY}`;
const logFile = "C:\\Users\\ASUS\\OneDrive\\VARIOS\\Documentos\\LIFEXTREME\\WEB\\Lifextreme-Web-AI\\agents\\debug_claude_call.log";

// Log arguments
const args = process.argv.slice(2);
appendFileSync(logFile, `\n\n[${new Date().toISOString()}] ARGV: ${JSON.stringify(args)}\n`);

async function runAgent(promptTexto) {
    try {
        appendFileSync(logFile, `PROMPT A GEMINI: ${promptTexto}\n`);
        
        const payload = {
            contents: [{
                parts: [{ text: "Eres Cami, el agente inteligente de Lifextreme. Analiza lo siguiente y responde en texto claro de acuerdo a tu tarea:\n\n" + promptTexto }]
            }]
        };

        const res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        
        if (data.error) {
            appendFileSync(logFile, `ERROR API: ${JSON.stringify(data.error)}\n`);
            console.error("Error de la API:", data.error.message);
            process.exit(1);
        }

        const respuesta = data.candidates[0].content.parts[0].text;
        
        appendFileSync(logFile, `RESPUESTA GEMINI: ${respuesta}\n`);
        
        // Output to stdout for Paperclip
        console.log(respuesta);
        process.exit(0);
    } catch (e) {
        appendFileSync(logFile, `FATAL: ${e.message}\n`);
        console.error("Fallo de conexión crítico:", e);
        process.exit(1);
    }
}

// Read stdin as well in case Paperclip passes data via pipes
let inputData = '';
process.stdin.on('data', chunk => {
    inputData += chunk.toString();
});

process.stdin.on('end', () => {
    if (inputData.trim().length > 0) {
        appendFileSync(logFile, `STDIN: ${inputData}\n`);
    }
    
    // Use arguments first, fallback to stdin, fallback to default
    const finalPrompt = args.join(" ") || inputData || "Hola Cami, haz un reporte de rutina.";
    runAgent(finalPrompt);
});

// Timeout in case stdin is hanging (if Paperclip doesn't pipe anything but expects immediate return)
setTimeout(() => {
    const finalPrompt = args.join(" ") || "Hola Cami, haz un reporte de rutina.";
    runAgent(finalPrompt);
}, 1000);
