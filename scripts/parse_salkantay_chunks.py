import os
import re
import json

def chunk_text(text, max_words=350, min_words=200, overlap=40):
    """
    Split text into chunks of approx 400-700 tokens (approx 250-450 words in Spanish).
    Uses sentence boundary preservation.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_sentences = []
    current_word_count = 0

    for sent in sentences:
        sent_words = len(sent.split())
        if current_word_count + sent_words > max_words and current_word_count >= min_words:
            chunk_content = " ".join(current_sentences).strip()
            if chunk_content:
                chunks.append(chunk_content)
            # Overlap: keep last few sentences
            overlap_sentences = []
            overlap_count = 0
            for s in reversed(current_sentences):
                s_words = len(s.split())
                if overlap_count + s_words <= overlap:
                    overlap_sentences.insert(0, s)
                    overlap_count += s_words
                else:
                    break
            current_sentences = overlap_sentences + [sent]
            current_word_count = sum(len(s.split()) for s in current_sentences)
        else:
            current_sentences.append(sent)
            current_word_count += sent_words

    if current_sentences:
        chunk_content = " ".join(current_sentences).strip()
        if chunk_content:
            chunks.append(chunk_content)

    return chunks

def extract_strategic_nodes():
    with open("data/salkantay_strategic_analysis.md", "r", encoding="utf-8") as f:
        content = f.read()

    pages = content.split("<!-- PAGE ")
    # Map page groups to sections
    raw_sections = [
        {
            "id": "alojamiento_propuesta_valor",
            "pages": pages[1:4], # Pág 1-3
            "strategic_pillar": "alojamiento_glamping",
            "target_department": "Operaciones",
            "region": "Salkantay",
            "benchmark_target": "Salkantay Trekking",
            "doc_type": "benchmark",
            "urgency_phase": "Fase_1_Inmediata",
            "title": "Diagnóstico de Propuesta de Valor, Glamping y Domos Geodésicos de Altura"
        },
        {
            "id": "cartera_rutas_experiencias",
            "pages": pages[3:5], # Pág 3-4
            "strategic_pillar": "logistica_marcha",
            "target_department": "Operaciones",
            "region": "Cusco",
            "benchmark_target": "Salkantay Trekking",
            "doc_type": "benchmark",
            "urgency_phase": "Fase_1_Inmediata",
            "title": "Cartera de Experiencias Outdoor y Segmentación de Rutas Andinas"
        },
        {
            "id": "logistica_carga_arrieria_bpm",
            "pages": pages[4:6], # Pág 4-5
            "strategic_pillar": "logistica_marcha",
            "target_department": "Operaciones",
            "region": "Salkantay",
            "benchmark_target": "Salkantay Trekking",
            "doc_type": "directiva_operativa",
            "urgency_phase": "Fase_1_Inmediata",
            "title": "Logística de Carga (Regla 7 kg), Arriería, Adelanto de Campamento y BPM"
        },
        {
            "id": "seguridad_biomedica_oxigeno",
            "pages": pages[5:7], # Pág 5-6
            "strategic_pillar": "seguridad_biomedica",
            "target_department": "Guias_Campo",
            "region": "Salkantay",
            "benchmark_target": "Salkantay Trekking",
            "doc_type": "protocolo_seguridad",
            "urgency_phase": "Fase_1_Inmediata",
            "title": "Seguridad Biomédica, Guías WFR/WAFA, Oxigenoterapia 3m3 y Monitoreo MAM"
        },
        {
            "id": "red_asistencial_o2_medical",
            "pages": pages[6:8], # Pág 6-7
            "strategic_pillar": "seguridad_biomedica",
            "target_department": "Operaciones",
            "region": "Cusco",
            "benchmark_target": "Salkantay Trekking",
            "doc_type": "protocolo_seguridad",
            "urgency_phase": "Fase_1_Inmediata",
            "title": "Protocolos de Evacuación, Red Médica O2 Medical Network y Rescate"
        },
        {
            "id": "estructura_organizacional_calidad",
            "pages": pages[7:9], # Pág 7-8
            "strategic_pillar": "estructura_calidad",
            "target_department": "Supervision_Calidad",
            "region": "Cusco",
            "benchmark_target": "Salkantay Trekking",
            "doc_type": "manual_calidad",
            "urgency_phase": "Fase_2_Media",
            "title": "Estructura Orgánica: Separación Operaciones vs Calidad y Ciclo de Vida de Equipos"
        },
        {
            "id": "politicas_comerciales_briefing",
            "pages": pages[8:10], # Pág 8-9
            "strategic_pillar": "politica_comercial",
            "target_department": "Ventas",
            "region": "Cusco",
            "benchmark_target": "Salkantay Trekking",
            "doc_type": "directiva_operativa",
            "urgency_phase": "Fase_1_Inmediata",
            "title": "Políticas Comerciales: Depósito $200 USD, Briefing Presencial Obligatorio y Saldos"
        },
        {
            "id": "sostenibilidad_fundacion_rsc",
            "pages": pages[9:11], # Pág 9-10
            "strategic_pillar": "sostenibilidad_rsc",
            "target_department": "Direccion_General",
            "region": "Vilcabamba",
            "benchmark_target": "Salkantay Trekking",
            "doc_type": "manual_calidad",
            "urgency_phase": "Fase_3_Expansion",
            "title": "Sostenibilidad, Formalización de Arrieros, Certificaciones CALTUR/ATTA y RSC"
        },
        {
            "id": "diagnostico_brechas_lifextreme",
            "pages": pages[10:13], # Pág 10-12
            "strategic_pillar": "estructura_calidad",
            "target_department": "Direccion_General",
            "region": "Cusco",
            "benchmark_target": "Lifextreme Peru",
            "doc_type": "benchmark",
            "urgency_phase": "Fase_1_Inmediata",
            "title": "Diagnóstico de Brechas Operativas y Tecnológicas de Lifextreme Perú"
        },
        {
            "id": "plan_maestro_pilar1_alojamiento",
            "pages": pages[12:14], # Pág 12-13
            "strategic_pillar": "alojamiento_glamping",
            "target_department": "Operaciones",
            "region": "Salkantay",
            "benchmark_target": "Lifextreme Peru",
            "doc_type": "directiva_operativa",
            "urgency_phase": "Fase_1_Inmediata",
            "title": "Plan Maestro Lifextreme Pilar 1: Red de Alojamiento Glamping Signature"
        },
        {
            "id": "plan_maestro_pilar2_calidad_gastronomia",
            "pages": pages[12:14], # Pág 12-13
            "strategic_pillar": "estructura_calidad",
            "target_department": "Supervision_Calidad",
            "region": "Cusco",
            "benchmark_target": "Lifextreme Peru",
            "doc_type": "manual_calidad",
            "urgency_phase": "Fase_2_Media",
            "title": "Plan Maestro Lifextreme Pilar 2: Dirección de Calidad y Gastronomía Andina BPM"
        },
        {
            "id": "plan_maestro_pilar3_seguridad_telemetria",
            "pages": pages[13:15], # Pág 13-14
            "strategic_pillar": "seguridad_biomedica",
            "target_department": "Guias_Campo",
            "region": "Salkantay",
            "benchmark_target": "Lifextreme Peru",
            "doc_type": "protocolo_seguridad",
            "urgency_phase": "Fase_1_Inmediata",
            "title": "Plan Maestro Lifextreme Pilar 3: Blindaje de Seguridad, Telemetría Satelital y Red Médica"
        },
        {
            "id": "plan_maestro_pilar4_comercial_cx",
            "pages": pages[14:16], # Pág 14-15
            "strategic_pillar": "politica_comercial",
            "target_department": "Ventas",
            "region": "Cusco",
            "benchmark_target": "Lifextreme Peru",
            "doc_type": "directiva_operativa",
            "urgency_phase": "Fase_1_Inmediata",
            "title": "Plan Maestro Lifextreme Pilar 4: Modernización Tecnológica, Duffle Bags 7kg y Briefing CX"
        },
        {
            "id": "plan_maestro_pilar5_fundacion_sostenibilidad",
            "pages": pages[14:17], # Pág 14-16
            "strategic_pillar": "sostenibilidad_rsc",
            "target_department": "Direccion_General",
            "region": "Cusco",
            "benchmark_target": "Lifextreme Peru",
            "doc_type": "manual_calidad",
            "urgency_phase": "Fase_3_Expansion",
            "title": "Plan Maestro Lifextreme Pilar 5: Gobernanza Sostenible, Fundación y Sellos Internacionales"
        },
        {
            "id": "hoja_ruta_fases_cronograma",
            "pages": pages[15:17], # Pág 15-16
            "strategic_pillar": "estructura_calidad",
            "target_department": "Direccion_General",
            "region": "Cusco",
            "benchmark_target": "Lifextreme Peru",
            "doc_type": "directiva_operativa",
            "urgency_phase": "Fase_1_Inmediata",
            "title": "Cronograma de Ejecución Estratégica en 3 Fases (Inmediata, Media, Expansión)"
        }
    ]

    final_chunks = []
    chunk_counter = 1

    for sec in raw_sections:
        combined_text = "\n".join(sec["pages"])
        # Clean text: remove any page residue
        combined_text = re.sub(r'<!-- PAGE \d+ -->', '', combined_text)
        combined_text = re.sub(r'^\s*\d+\s*-->\s*', '', combined_text)
        combined_text = re.sub(r'\n\s*\d+\s*-->\s*', ' ', combined_text)
        combined_text = re.sub(r'\s+', ' ', combined_text).strip()
        
        # Sub-divide into chunks of 250-450 words
        text_chunks = chunk_text(combined_text, max_words=380, min_words=180, overlap=40)
        
        for idx, sub_txt in enumerate(text_chunks, 1):
            sub_txt = re.sub(r'^\s*\d+\s*-->\s*', '', sub_txt).strip()
            # Apply strict contextual prefix
            prefix = f"[Contexto: Estrategia Lifextreme Perú | Pilar: {sec['strategic_pillar']} | Departamento: {sec['target_department']}]\n"
            full_chunk_text = prefix + sub_txt
            
            chunk_node = {
                "chunk_id": f"salkantay_strat_{chunk_counter:03d}",
                "section_id": sec["id"],
                "section_title": sec["title"],
                "text": full_chunk_text,
                "word_count": len(full_chunk_text.split()),
                "country": "Peru",
                "region": sec["region"],
                "strategic_pillar": sec["strategic_pillar"],
                "benchmark_target": sec["benchmark_target"],
                "doc_type": sec["doc_type"],
                "target_department": sec["target_department"],
                "urgency_phase": sec["urgency_phase"]
            }
            final_chunks.append(chunk_node)
            chunk_counter += 1

    print(f"Generated {len(final_chunks)} semantic chunks from Strategic Analysis.")
    os.makedirs("data", exist_ok=True)
    with open("data/salkantay_strategy_chunks.json", "w", encoding="utf-8") as out:
        json.dump(final_chunks, out, ensure_ascii=False, indent=2)
    print("Saved to data/salkantay_strategy_chunks.json")
    return final_chunks

if __name__ == "__main__":
    extract_strategic_nodes()
