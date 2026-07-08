with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

widget_code = """
<!-- INICIO CHAT MAX Q-RAG -->
<style>
#max-chat-widget {
    position: fixed; bottom: 20px; right: 20px; width: 350px; height: 450px; background: #111; border: 1px solid #333; border-radius: 12px; display: flex; flex-direction: column; z-index: 9999; box-shadow: 0 10px 30px rgba(0,0,0,0.5); font-family: Arial, sans-serif; color: white;
}
#max-chat-header {
    background: #ff5e00; padding: 15px; border-top-left-radius: 12px; border-top-right-radius: 12px; font-weight: bold; display: flex; justify-content: space-between;
}
#max-chat-messages {
    flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px;
}
.chat-msg {
    padding: 10px 15px; border-radius: 8px; max-width: 80%; line-height: 1.4; font-size: 14px;
}
.chat-msg.user { background: #333; align-self: flex-end; }
.chat-msg.max { background: #1a1a1a; border: 1px solid #ff5e00; align-self: flex-start; }
#max-chat-input-area { display: flex; padding: 10px; border-top: 1px solid #333; }
#max-chat-input { flex: 1; padding: 10px; border: none; background: #222; color: white; border-radius: 4px; outline: none; }
#max-chat-send { background: #ff5e00; color: white; border: none; padding: 10px 15px; margin-left: 5px; border-radius: 4px; cursor: pointer; font-weight: bold; }
</style>

<div id="max-chat-widget">
    <div id="max-chat-header"><span>🤖 MAX (Q-RAG)</span></div>
    <div id="max-chat-messages"><div class="chat-msg max">Hola, soy MAX. ¿Buscas adrenalina o relax en Cusco?</div></div>
    <div id="max-chat-input-area">
        <input type="text" id="max-chat-input" placeholder="Escribe aquí..." autocomplete="off" />
        <button id="max-chat-send">▶</button>
    </div>
</div>

<script>
    // Conectando a localtunnel
    const API_URL = "https://lifextreme-api.loca.lt/api/chat";
    
    const maxInput = document.getElementById('max-chat-input');
    const maxSendBtn = document.getElementById('max-chat-send');
    const maxMessages = document.getElementById('max-chat-messages');

    async function sendMaxMessage() {
        const text = maxInput.value.trim();
        if(!text) return;
        
        maxMessages.innerHTML += `<div class="chat-msg user">${text}</div>`;
        maxInput.value = '';
        maxMessages.scrollTop = maxMessages.scrollHeight;

        const maxMsgId = 'msg-' + Date.now();
        maxMessages.innerHTML += `<div class="chat-msg max" id="${maxMsgId}">...</div>`;
        maxMessages.scrollTop = maxMessages.scrollHeight;

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });

            if (!response.body) throw new Error("No ReadableStream");
            const reader = response.body.getReader();
            const decoder = new TextDecoder("utf-8");
            let maxElement = document.getElementById(maxMsgId);
            maxElement.innerHTML = '';

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                
                const chunk = decoder.decode(value, {stream: true});
                const lines = chunk.split('\\n');
                for(let line of lines) {
                    if(line.startsWith('data: ')) {
                        const dataStr = line.substring(6).trim();
                        if(dataStr === '[DONE]') break;
                        if(dataStr) {
                            try {
                                const data = JSON.parse(dataStr);
                                if(data.text) {
                                    maxElement.innerHTML += data.text;
                                    maxMessages.scrollTop = maxMessages.scrollHeight;
                                }
                            } catch(e) { }
                        }
                    }
                }
            }
        } catch(err) {
            document.getElementById(maxMsgId).innerHTML = "⚠️ API local apagada. Asegúrate de encender max_api_server.py y el localtunnel.";
        }
    }

    maxSendBtn.addEventListener('click', sendMaxMessage);
    maxInput.addEventListener('keypress', (e) => { if(e.key === 'Enter') sendMaxMessage(); });
</script>
<!-- FIN CHAT MAX Q-RAG -->
"""

if "<!-- INICIO CHAT MAX Q-RAG -->" not in content:
    content = content.replace("</body>", widget_code + "\n</body>")
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("Widget inyectado con éxito.")
else:
    print("El widget ya estaba inyectado.")
