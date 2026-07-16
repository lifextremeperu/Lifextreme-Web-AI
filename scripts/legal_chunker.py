import re
import fitz  # PyMuPDF
from pathlib import Path

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extrae texto de un PDF manteniendo párrafos básicos."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    doc.close()
    return text

def clean_text(text: str) -> str:
    """Limpia caracteres especiales y excesos de espacios."""
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\x00', '')
    return text.strip()

def chunk_legal_document(text: str, metadata: dict) -> list:
    """
    Segmenta el texto de un documento legal basándose en marcadores
    como Título, Capítulo y Artículo, respetando el contexto legal.
    """
    chunks = []
    
    # Expresiones regulares para detectar divisiones legales
    # Ejemplo: "Artículo 1.-", "ARTÍCULO 15°", "Artículo 2:", "Capítulo III"
    pattern = re.compile(r'(?i)(?:\b(T[ií]tulo|Cap[ií]tulo|Art[ií]culo)\s+[IVXLCDM\d]+[°\.-]?\s*)')
    
    # Encontrar todas las divisiones
    matches = list(pattern.finditer(text))
    
    if not matches:
        # Si no es un texto estructurado en artículos (ej. un Manual o Plan)
        # Hacemos chunking por límite de caracteres manteniendo párrafos
        return chunk_narrative_document(text, metadata)

    current_context = ""
    
    # Iterar sobre las coincidencias
    for i in range(len(matches)):
        start_idx = matches[i].start()
        end_idx = matches[i+1].start() if i + 1 < len(matches) else len(text)
        
        chunk_text = text[start_idx:end_idx].strip()
        
        # Limpiar chunk
        chunk_text = clean_text(chunk_text)
        
        if len(chunk_text) < 20:
            continue
            
        # Crear copia de la metadata para inyectarle el fragmento
        chunk_meta = metadata.copy()
        
        # Opcional: Detectar qué tipo de marcador es para mejor contexto
        if chunk_text.lower().startswith("título"):
            current_context = chunk_text.split('.')[0] if '.' in chunk_text else chunk_text[:50]
        
        # Agregar el contexto actual si es un artículo
        if chunk_text.lower().startswith("artículo") and current_context:
            chunk_text = f"[{current_context}] " + chunk_text
            
        chunks.append({
            "text": chunk_text,
            "metadata": chunk_meta
        })
        
    return chunks

def chunk_narrative_document(text: str, metadata: dict, chunk_size=1000, overlap=150) -> list:
    """
    Segmenta documentos narrativos (Manuales, Planes) por límite de caracteres,
    intentando no romper oraciones.
    """
    chunks = []
    sentences = re.split(r'(?<=[.!?]) +', text)
    
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append({
                "text": clean_text(current_chunk),
                "metadata": metadata.copy()
            })
            # Solapamiento
            current_chunk = sentence + " "
            
    if current_chunk.strip():
        chunks.append({
            "text": clean_text(current_chunk),
            "metadata": metadata.copy()
        })
        
    return chunks

if __name__ == "__main__":
    # Prueba rápida
    sample_text = "TÍTULO I DISPOSICIONES GENERALES Artículo 1.- Objeto de la Ley. La presente Ley tiene por objeto... Artículo 2.- Ámbito de aplicación. Se aplica a todas las entidades..."
    meta = {"entidad_emisora": "MINCETUR"}
    res = chunk_legal_document(sample_text, meta)
    print("Chunks generados:")
    for c in res:
        print(f"- {c['text'][:100]}...")
