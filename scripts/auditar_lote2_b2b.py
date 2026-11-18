import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from auditar_prospectos_b2b import audit_site, build_diagnostic_bullets

CANDIDATES_LOTE2 = [
    {
        "slug": "andean_roots_peru",
        "agencia": "Andean Roots Peru",
        "razon_social": "Andean Roots Peru E.I.R.L.",
        "ruc": "20600722370",
        "rep_legal": "Hernán Gutiérrez Serrano",
        "saludo_nombre": "Hernán",
        "email": "info@andeanrootsperu.com",
        "telefono": "949116895",
        "web": "https://www.andeanrootsperu.com",
        "clase": "Operador Turismo",
        "distrito": "Cusco",
    },
    {
        "slug": "cusco_expeditions",
        "agencia": "Cusco Expeditions",
        "razon_social": "Cusco Expeditions Adventure Travel Specialists E.I.R.L.",
        "ruc": "20491040492",
        "rep_legal": "Edgar Catunta Guillén",
        "saludo_nombre": "Edgar",
        "email": "info@cuscoexpeditions.com",
        "telefono": "084236307",
        "web": "https://www.cuscoexpeditions.com",
        "clase": "Operador Turismo",
        "distrito": "Cusco",
    },
    {
        "slug": "veru_voyage",
        "agencia": "Veru Voyage",
        "razon_social": "Veru Voyage E.I.R.L.",
        "ruc": "20605405950",
        "rep_legal": "Maximiliano Taylor Coronel",
        "saludo_nombre": "Maximiliano",
        "email": "info@veruvoyage.com",
        "telefono": "980589624",
        "web": "https://www.veruvoyage.com",
        "clase": "Minorista",
        "distrito": "Cusco",
    },
    {
        "slug": "ritisuyo",
        "agencia": "Ritisuyo",
        "razon_social": "Ritisuyo E.I.R.L.",
        "ruc": "20603262035",
        "rep_legal": "Nelson Branny Sierra Sánchez",
        "saludo_nombre": "Nelson",
        "email": "hoa@ritisuyo.com",
        "telefono": "991411200",
        "web": "https://www.ritisuyo.com",
        "clase": "Operador Turismo",
        "distrito": "Cusco",
    },
    {
        "slug": "habitats_peru",
        "agencia": "Habitats Peru Travel",
        "razon_social": "Habitats Peru Travel S.C.R.L.",
        "ruc": "20450500845",
        "rep_legal": "Doris Valencia Puclla",
        "saludo_nombre": "Doris",
        "email": "info@habitatsperu.com",
        "telefono": "984115593",
        "web": "https://www.habitatsperu.com",
        "clase": "Operador Turismo",
        "distrito": "Wanchaq, Cusco",
    },
    {
        "slug": "tarvos_peru_tours",
        "agencia": "Tarvos Peru Tours",
        "razon_social": "Tarvos Peru Tours E.I.R.L.",
        "ruc": "20606136588",
        "rep_legal": "Gorki Borda Luza",
        "saludo_nombre": "Gorki",
        "email": "info@tarvosperutours.com",
        "telefono": "084584532",
        "web": "https://www.tarvosperutours.com",
        "clase": "Operador Turismo",
        "distrito": "Cusco",
    },
    {
        "slug": "munaycha_expeditions",
        "agencia": "Munaycha Expeditions",
        "razon_social": "Munaycha Expeditions E.I.R.L.",
        "ruc": "20607633721",
        "rep_legal": "Julio César Ramos Olivera",
        "saludo_nombre": "Julio César",
        "email": "info@munaychaexpeditions.com",
        "telefono": "918464656",
        "web": "https://www.munaychaexpeditions.com",
        "clase": "Operador Turismo",
        "distrito": "San Sebastián, Cusco",
    },
    {
        "slug": "quechuas_peru",
        "agencia": "Quechuas Peru",
        "razon_social": "Quechuas Peru E.I.R.L.",
        "ruc": "20527292973",
        "rep_legal": "Hilda Calderón Vergara",
        "saludo_nombre": "Hilda",
        "email": "reservas@quechuasperu.net",
        "telefono": "973975522",
        "web": "https://www.quechuasperu.net",
        "clase": "Operador Turismo",
        "distrito": "San Sebastián, Cusco",
    },
    {
        "slug": "peruvian_sacred",
        "agencia": "Peruvian Sacred & Adventure",
        "razon_social": "Peruvian Sacred & Adventure E.I.R.L.",
        "ruc": "20527307164",
        "rep_legal": "Alcira Mildred Condori Cachi",
        "saludo_nombre": "Alcira",
        "email": "alcira@peruviansacred.com",
        "telefono": "084251920",
        "web": "https://www.peruviansacred.com",
        "clase": "Operador Turismo",
        "distrito": "Santiago, Cusco",
    },
    {
        "slug": "eco_waykis",
        "agencia": "Eco Waykis",
        "razon_social": "Ewta E.I.R.L.",
        "ruc": "20527593744",
        "rep_legal": "Edwin Vásquez Salas",
        "saludo_nombre": "Edwin",
        "email": "info@ecowaykis.com",
        "telefono": "084231992",
        "web": "https://www.ecowaykis.com",
        "clase": "Operador Turismo",
        "distrito": "Wanchaq, Cusco",
    },
    {
        "slug": "machupicchu_inca_boletos",
        "agencia": "Machupicchu Inca Viajes",
        "razon_social": "Machupicchu Inca Viajes Y Servicios E.I.R.L.",
        "ruc": "20605740236",
        "rep_legal": "Ana Melva Aliaga Mosquera",
        "saludo_nombre": "Ana Melva",
        "email": "info@machupicchu-inca-boletos.com",
        "telefono": "984551030",
        "web": "https://www.machupicchu-inca-boletos.com",
        "clase": "Minorista, Operador Turismo",
        "distrito": "Cusco",
    },
    {
        "slug": "cultural_immersion",
        "agencia": "Cultural Immersion Travel Peru",
        "razon_social": "Cultural Immersion Travel Peru E.I.R.L.",
        "ruc": "20490651676",
        "rep_legal": "Eduardo Becerra Pimentel",
        "saludo_nombre": "Eduardo",
        "email": "info@culturalimmersion.org",
        "telefono": "084225183",
        "web": "https://www.culturalimmersion.org",
        "clase": "Operador Turismo",
        "distrito": "Cusco",
    },
]


def main():
    audited = []
    for p in CANDIDATES_LOTE2:
        print(f"Auditing {p['agencia']} -> {p['web']} ...")
        a = audit_site(p["web"])
        audited.append({**p, "audit": a, "diagnostico_bullets": build_diagnostic_bullets(p, a)})

    # Prioritize HTTP 200 first, then HTTP errors, then DNS errors, take top 10
    audited.sort(key=lambda x: (0 if x["audit"]["status"] == 200 else (1 if x["audit"]["status"] else 2)))
    top10 = audited[:10]

    with open("reportes_b2b/email_presentacion_ia_agencias_cusco.html", "r", encoding="utf-8") as f:
        tpl = f.read()

    anchor = (
        '              <p style="margin:0 0 10px 0; font-size:14.5px; line-height:1.6; color:#141413;">\n'
        '                <strong>Estimado/a líder de agencia:</strong> bajo el principio andino del <strong style="color:#c25e3e;">Ayni (crecemos juntos)</strong>, queremos que el turismo en Cusco modernice sus procesos <strong>sin depender de grandes corporaciones</strong>, sino enseñando a tu equipo a <strong>dominar y crear su propia tecnología</strong>.\n'
        '              </p>'
    )
    assert anchor in tpl

    out_dir = "reportes_b2b/emails_personalizados"
    os.makedirs(out_dir, exist_ok=True)

    for p in top10:
        b = p["diagnostico_bullets"]
        block = f'''              <p style="margin:0 0 10px 0; font-size:14.5px; line-height:1.6; color:#141413;">
                <strong>Hola {p['saludo_nombre']} ({p['agencia']}):</strong> bajo el principio andino del <strong style="color:#c25e3e;">Ayni (crecemos juntos)</strong>, queremos que el turismo en Cusco modernice sus procesos <strong>sin depender de grandes corporaciones</strong>, sino enseñando a tu equipo a <strong>dominar y crear su propia tecnología</strong>.
              </p>

              <!-- DIAGNÓSTICO PERSONALIZADO DE SU WEB Y OPERACIÓN -->
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f0fdf4; border:1px solid #bbf7d0; border-left:4px solid #0f766e; border-radius:8px; margin-bottom:12px;">
                <tr>
                  <td style="padding:12px 15px; font-size:12.5px; line-height:1.55; color:#134e4a;">
                    <strong style="color:#0f766e;">🔎 Mini-diagnóstico previo de {p['agencia']} ({p['web'].replace('https://www.', '')}):</strong><br/>
                    • {b[0]}<br/>
                    • {b[1]}<br/>
                    • {b[2]}
                  </td>
                </tr>
              </table>'''
        h = tpl.replace(anchor, block)
        h = h.replace('href="assets/', 'href="../assets/')
        h = h.replace('src="assets/', 'src="../assets/')
        h = h.replace('href="../agendar-capacitacion.html', 'href="../../agendar-capacitacion.html')
        with open(os.path.join(out_dir, f"{p['slug']}.html"), "w", encoding="utf-8") as wf:
            wf.write(h)

    with open("reportes_b2b/prospectos_lote2_piloto.json", "w", encoding="utf-8") as jf:
        json.dump(top10, jf, ensure_ascii=False, indent=2)

    print("\n=== TOP 10 LOTE 2 ===")
    for r in top10:
        a = r["audit"]
        print(f"- {r['agencia']} | mail={r['email']} | status={a['status']} | cms={a['cms']} | schema={a['has_schema_jsonld']} | llms={a['has_llms_txt']} | tours={a['tours_detected']} | err={a['error']}")


if __name__ == "__main__":
    main()
