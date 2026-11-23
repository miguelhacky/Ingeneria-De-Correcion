from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Flowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

PDF = "MiguelAngelFajardoSemana1Dia4.pdf"


class Placeholder(Flowable):
    def __init__(self, text, height=55 * mm):
        super().__init__()
        self.text = text
        self.width = 175 * mm
        self.height = height

    def draw(self):
        canvas = self.canv
        canvas.saveState()
        canvas.setDash(4, 3)
        canvas.setStrokeColor(colors.HexColor("#777777"))
        canvas.setFillColor(colors.HexColor("#F7F7F7"))
        canvas.rect(0, 0, self.width, self.height, fill=1, stroke=1)
        canvas.setDash()
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.setFont("Helvetica", 12)
        canvas.drawCentredString(
            self.width / 2,
            self.height / 2,
            self.text,
        )
        canvas.restoreState()


styles = getSampleStyleSheet()
title = ParagraphStyle(
    "TitleCustom",
    parent=styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=26,
    alignment=1,
    leading=31,
)
section = ParagraphStyle(
    "SectionCustom",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=20,
    alignment=1,
    leading=24,
)
caption = ParagraphStyle(
    "CaptionCustom",
    parent=styles["Italic"],
    fontSize=9,
    alignment=1,
    textColor=colors.HexColor("#555555"),
)
normal = styles["Normal"]


def header(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.drawString(12 * mm, 8 * mm, "Semana 1 - Dia 4")
    canvas.restoreState()


doc = SimpleDocTemplate(
    PDF,
    pagesize=letter,
    rightMargin=18 * mm,
    leftMargin=18 * mm,
    topMargin=15 * mm,
    bottomMargin=15 * mm,
)
story = []

# Portada
story.extend(
    [
        Spacer(1, 42 * mm),
        Paragraph("Taller 7: Ingeniería de Corrección", title),
        Spacer(1, 20 * mm),
        Paragraph("Miguel Angel Fajardo Zapata", ParagraphStyle(
            "Name", parent=normal, fontSize=16, alignment=1
        )),
        Spacer(1, 4 * mm),
        Paragraph("ADSO", ParagraphStyle(
            "Career", parent=normal, fontSize=12, alignment=1
        )),
        Spacer(1, 10 * mm),
        Paragraph(
            "<b>Repositorio:</b><br/>"
            "https://github.com/miguelhacky/Ingeneria-De-Correcion",
            ParagraphStyle("Repo", parent=normal, fontSize=11, alignment=1),
        ),
        Spacer(1, 35 * mm),
        Paragraph(
            "SERVICIO NACIONAL DE APRENDIZAJE (SENA)",
            ParagraphStyle("Sena", parent=normal, fontSize=11, alignment=1),
        ),
        Spacer(1, 3 * mm),
        Paragraph("22 noviembre 2026", ParagraphStyle(
            "Date", parent=normal, fontSize=11, alignment=1
        )),
        PageBreak(),
    ]
)

def section_title(text):
    story.extend([Paragraph(text, section), Spacer(1, 7 * mm)])

def add_placeholder(text, height=55 * mm, label=None):
    story.append(Placeholder(text, height))
    if label:
        story.append(Spacer(1, 2 * mm))
        story.append(Paragraph(label, caption))
        story.append(Spacer(1, 4 * mm))

# Evidencia 1
section_title("1. Tabla inicial de fallos")
story.append(Paragraph(
    "Registrar los repositorios públicos, el enunciado asignado y los tres fallos elegidos.",
    normal,
))
story.append(Spacer(1, 5 * mm))
data = [
    ["N.º", "Criterio", "Descripción del fallo", "Archivo y línea"],
    ["1", "Validación de entradas", "Pegar descripción exacta", "app.py y líneas"],
    ["2", "Contraseñas y hash", "Pegar descripción exacta", "app.py y líneas"],
    ["3", "Control de acceso", "Pegar descripción exacta", "app.py y líneas"],
]
table = Table(data, colWidths=[10 * mm, 34 * mm, 78 * mm, 45 * mm])
table.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DDDDDD")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("LEADING", (0, 0), (-1, -1), 12),
]))
story.append(table)
story.extend([
    Spacer(1, 8 * mm),
    Paragraph("<b>Reto 0:</b> https://github.com/miguelhacky/Ingeneria-De-Correcion", normal),
    Paragraph("<b>Plataforma ludica:</b> ________________________________", normal),
    Paragraph("<b>Número y nombre del reto 0:</b> ________________________________", normal),
    PageBreak(),
])

# Evidencia 2
section_title("2. Limpieza de variables de entorno (.env)")
story.append(Paragraph("Parte 1 de 2", styles["Heading3"]))
add_placeholder("PEGAR CAPTURA: búsqueda de secretos antes de la corrección", 60 * mm,
                 "Evidencia 2 para el PDF, parte 1 de 2")
story.append(Paragraph("Parte 2 de 2", styles["Heading3"]))
add_placeholder("PEGAR CAPTURA: búsqueda después de la corrección", 60 * mm,
                 "Evidencia 2 para el PDF, parte 2 de 2")
story.append(PageBreak())

# Evidencia 3
section_title("3. Contexto del agente")
add_placeholder("PEGAR CAPTURA COMPLETA DE AGENTS.md", 150 * mm,
                 "Evidencia 3 para el PDF")
story.append(PageBreak())

# Evidencia 4
section_title("4. Prueba de humo, Ruff y pre-commit")
for part, text in [
    ("1", "PEGAR CAPTURA: prueba de humo en verde"),
    ("2", "PEGAR CAPTURA: ruff check . mostrando All checks passed!"),
    ("3", "PEGAR CAPTURA: commit con Ruff y Pruebas en Passed"),
]:
    story.append(Paragraph("Parte " + part + " de 3", styles["Heading3"]))
    add_placeholder(text, 48 * mm,
                     "Evidencia 4 para el PDF, parte " + part + " de 3")
story.append(PageBreak())

# Evidencias 5-7
for evidence, name in [(5, "fallo 1"), (6, "fallo 2"), (7, "fallo 3")]:
    section_title(str(evidence - 2) + ". Corrección del " + name)
    story[-1] = Paragraph(
        str(evidence) + ". Corrección del " + name,
        section,
    )
    for part, text in [
        ("1", "PEGAR CAPTURA: prueba en rojo y motivo visible"),
        ("2", "PEGAR CAPTURA: plan aprobado y diff sin modificar pruebas"),
        ("3", "PEGAR CAPTURA: pruebas en verde y commit con el hook en Passed"),
    ]:
        story.append(Paragraph("Parte " + part + " de 3", styles["Heading3"]))
        add_placeholder(text, 48 * mm,
                         "Evidencia " + str(evidence) + " para el PDF, parte " + part + " de 3")
    story.append(PageBreak())

# Evidencia 8
section_title("8. Pull request e integración")
add_placeholder(
    "PEGAR CAPTURA DEL PULL REQUEST CON LAS TRES PREGUNTAS Y EL ESTADO MERGED",
    170 * mm,
    "Evidencia 8 para el PDF",
)
story.append(PageBreak())

# Evidencia 9
section_title("9. Auditoría y lecciones")
audit = [
    ["Criterio", "Taller 1", "Hoy", "Cómo se comprobó"],
    ["Ejecución", "", "Cumple", ""],
    ["Validación de entradas", "", "Cumple", ""],
    ["Contraseñas y hash", "", "Cumple", ""],
    ["Secretos y claves", "", "Cumple", ""],
    ["Control de acceso", "", "Cumple", ""],
    ["Dependencias y alucinación", "", "Cumple", ""],
    ["Pruebas", "", "Cumple", ""],
    ["Manejo de errores", "", "Cumple", ""],
    ["Estructura", "", "Cumple parcialmente", ""],
]
audit_table = Table(audit, colWidths=[38 * mm, 28 * mm, 34 * mm, 67 * mm])
audit_table.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DDDDDD")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 8),
]))
story.append(audit_table)
story.extend([
    Spacer(1, 5 * mm),
    Paragraph("Conclusión personal de 3 a 5 líneas", styles["Heading3"]),
    Paragraph(
        "Escribir sin IA: explicar el fallo más grave, la diferencia entre vibe coding "
        "y pair programming, y qué regla habría evitado los fallos.",
        normal,
    ),
    Spacer(1, 4 * mm),
])
add_placeholder("PEGAR CAPTURA DE LECCIONES APRENDIDAS EN GITHUB", 45 * mm,
                 "Evidencia 9 para el PDF")
story.append(PageBreak())

# Evidencia 10
section_title("10. Cierre de semana 1")
for part, text in [
    ("1", "PEGAR CAPTURA: POLITICA_IA.md firmada en GitHub"),
    ("2", "PEGAR CAPTURA: etiqueta semana-1 en GitHub"),
    ("3", "PEGAR CAPTURA: última ejecución de Actions en verde"),
]:
    story.append(Paragraph("Parte " + part + " de 3", styles["Heading3"]))
    add_placeholder(text, 48 * mm,
                     "Evidencia 10 para el PDF, parte " + part + " de 3")

doc.build(story, onFirstPage=header, onLaterPages=header)
print(PDF)
