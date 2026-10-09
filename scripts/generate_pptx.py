from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import os

def create_pampa_nusta_pptx():
    print("Creando presentacion PPTX para Pampa Nusta...")
    
    # Crear presentación en blanco (widescreen por defecto en versiones recientes, o ajustamos el tamaño)
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)
    
    # Colores Corporativos/Místicos
    COLOR_BG = RGBColor(15, 20, 17)      # Negro/Verde muy oscuro
    COLOR_GOLD = RGBColor(201, 167, 92)  # Oro Viejo
    COLOR_TEXT = RGBColor(230, 230, 230) # Blanco grisáceo
    COLOR_ACCENT = RGBColor(22, 163, 74) # Esmeralda andina
    
    # Helper para fondo oscuro
    def set_dark_background(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = COLOR_BG
    
    # ----------------------------------------------------
    # SLIDE 1: PORTADA
    # ----------------------------------------------------
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)
    set_dark_background(slide)
    
    # Proyecto Nombre
    txBox = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(11), Inches(1))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "PROYECTO PAMPA ÑUSTA"
    p.font.size = Pt(28)
    p.font.color.rgb = COLOR_GOLD
    p.font.name = 'Georgia'
    p.font.bold = True
    
    # Título Principal
    txBox = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(11), Inches(2))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "EL ALMA DE LOS ANDES,\nLA MENTE DE SILICON VALLEY"
    p.font.size = Pt(55)
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.font.name = 'Georgia'
    p.font.bold = True
    
    # Subtítulo
    txBox = slide.shapes.add_textbox(Inches(1), Inches(4.5), Inches(8), Inches(1.5))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Conectamos la profunda sabiduría ancestral y el turismo comunitario inmersivo con el análisis matemático de millones de datos globales (Big Data)."
    p.font.size = Pt(20)
    p.font.color.rgb = COLOR_TEXT
    
    # Tag de Inversionistas
    txBox = slide.shapes.add_textbox(Inches(1), Inches(6.5), Inches(8), Inches(0.5))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "CONFIDENTIAL PITCH DECK // GLOBAL INVESTORS"
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_GOLD
    
    # ----------------------------------------------------
    # SLIDE 2: LA ALQUIMIA DEL VALOR
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_slide_layout)
    set_dark_background(slide)
    
    txBox = slide.shapes.add_textbox(Inches(1), Inches(0.8), Inches(11), Inches(1))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "I. LA ALQUIMIA DEL VALOR (RENTABILIDAD)"
    p.font.size = Pt(36)
    p.font.color.rgb = COLOR_GOLD
    p.font.name = 'Georgia'
    
    # Bloque 1
    txBox = slide.shapes.add_textbox(Inches(1), Inches(2.2), Inches(5), Inches(4))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "EL TIEMPO Y LA URGENCIA\n(Precios Dinámicos)"
    p.font.size = Pt(24)
    p.font.color.rgb = RGBColor(255,255,255)
    p.font.bold = True
    p2 = tf.add_paragraph()
    p2.text = "Así como la naturaleza tiene ciclos, el mercado tiene ritmos. Nuestros algoritmos (TimesFM) confirman que el forastero siente urgencia faltando 3 días para su viaje. Su necesidad de asegurar el espacio elimina la objeción del precio."
    p2.font.size = Pt(18)
    p2.font.color.rgb = COLOR_TEXT
    
    # Bloque 2
    txBox = slide.shapes.add_textbox(Inches(7), Inches(2.2), Inches(5), Inches(4))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "EL EQUILIBRIO DE ENERGÍAS\n(Petróleo y Divisas)"
    p.font.size = Pt(24)
    p.font.color.rgb = RGBColor(255,255,255)
    p.font.bold = True
    p2 = tf.add_paragraph()
    p2.text = "Estamos conectados al mundo. Si el Euro se fortalece, el europeo siente abundancia. La Inteligencia de Datos nos dice exactamente cuándo actuar y a quién dirigir nuestra publicidad."
    p2.font.size = Pt(18)
    p2.font.color.rgb = COLOR_TEXT
    
    # ----------------------------------------------------
    # SLIDE 3: EL ESCUDO Y LA RAÍZ
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_slide_layout)
    set_dark_background(slide)
    
    txBox = slide.shapes.add_textbox(Inches(1), Inches(0.8), Inches(11), Inches(1))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "II. EL ESCUDO Y LA RAÍZ (FORMALIZACIÓN)"
    p.font.size = Pt(36)
    p.font.color.rgb = COLOR_GOLD
    p.font.name = 'Georgia'
    
    txBox = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(11), Inches(4))
    tf = txBox.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "Las Raíces Legales (Certificación Mincetur / ISOs)"
    p.font.size = Pt(28)
    p.font.color.rgb = RGBColor(255,255,255)
    p.font.bold = True
    
    p2 = tf.add_paragraph()
    p2.text = "Para que un árbol crezca alto, sus raíces deben ser profundas y formales. Los grandes inversionistas y corporaciones de Europa exigen certificaciones estrictas (Normas ESG, ISO 9001) para enviar a sus viajeros. La informalidad es debilidad.\n\nEL MANDATO CORPORATIVO:\nIniciar la certificación DIRCETUR e ISO. Es la llave maestra para abrir bóvedas de contratos internacionales."
    p2.font.size = Pt(22)
    p2.font.color.rgb = COLOR_TEXT

    # ----------------------------------------------------
    # SLIDE 4: MONOPOLIO HUMANO
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_slide_layout)
    set_dark_background(slide)
    
    txBox = slide.shapes.add_textbox(Inches(2), Inches(2.5), Inches(9.33), Inches(3))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = '"Los algoritmos de Silicon Valley pueden predecir precios y comprar pasajes de avión a la velocidad de la luz. Pero jamás podrán mirar a los ojos a un forastero, jamás podrán tejer lana de alpaca bajo el sol, y jamás podrán abrazar."'
    p.font.size = Pt(32)
    p.font.color.rgb = RGBColor(255,255,255)
    p.font.italic = True
    p.alignment = 1 # Center
    
    txBox = slide.shapes.add_textbox(Inches(2), Inches(5.5), Inches(9.33), Inches(1))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "EL VALOR INMUTABLE DE PAMPA ÑUSTA"
    p.font.size = Pt(20)
    p.font.color.rgb = COLOR_GOLD
    p.alignment = 1 # Center

    # Guardar Presentación
    output_path = os.path.abspath("Pampa_Nusta_Inversion.pptx")
    prs.save(output_path)
    print(f"Presentacion PPTX generada exitosamente en: {output_path}")

if __name__ == "__main__":
    create_pampa_nusta_pptx()
