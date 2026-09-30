"""Compile the Generative AI Markdown viva guides into one printable PDF."""

import re
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, KeepTogether, PageBreak, PageTemplate,
    Paragraph, Preformatted, Spacer, Table, TableStyle,
)


HERE = Path(__file__).resolve().parent
OUT = HERE / "VIVA_HANDBOOK.pdf"
FILES = [
    "00_START_HERE.md",
    "06_TA_REVIEW.md",
    "02_DERIVATIONS_AND_NUMERICALS.md",
    "03_CODE_AND_EVIDENCE_WALKTHROUGH.md",
    "01_QUESTION_BANK.md",
    "04_MOCK_VIVA.md",
    "05_FLASHCARDS.md",
]
PAGE_W, PAGE_H = A4
NAVY = colors.HexColor("#17365D")
BLUE = colors.HexColor("#DCEAF6")
LIGHT = colors.HexColor("#F5F8FB")

styles = getSampleStyleSheet()
BODY = ParagraphStyle("Body2", parent=styles["BodyText"], fontName="Helvetica",
                      fontSize=8.3, leading=11.1, spaceAfter=4)
BULLET = ParagraphStyle("Bullet2", parent=BODY, leftIndent=12, firstLineIndent=-7,
                        bulletIndent=3, spaceAfter=2.5)
H1 = ParagraphStyle("H1x", parent=styles["Heading1"], fontName="Helvetica-Bold",
                    fontSize=17, leading=20, textColor=NAVY, spaceAfter=9)
H2 = ParagraphStyle("H2x", parent=styles["Heading2"], fontName="Helvetica-Bold",
                    fontSize=12, leading=14, textColor=NAVY, spaceBefore=6, spaceAfter=5)
H3 = ParagraphStyle("H3x", parent=styles["Heading3"], fontName="Helvetica-Bold",
                    fontSize=9.5, leading=12, textColor=colors.HexColor("#254E77"),
                    spaceBefore=5, spaceAfter=3)
QUOTE = ParagraphStyle("Quote", parent=BODY, leftIndent=12, rightIndent=8,
                       borderColor=colors.HexColor("#8EAFC8"), borderWidth=1,
                       borderPadding=6, backColor=LIGHT)
CODE = ParagraphStyle("Code", fontName="Courier", fontSize=6.8, leading=8.6,
                      leftIndent=8, rightIndent=8, backColor=colors.HexColor("#F1F3F5"),
                      borderPadding=5, spaceBefore=3, spaceAfter=5)


def ascii_clean(text):
    replacements = {
        "\u2013": "-", "\u2014": "-", "\u2011": "-", "\u2192": "->",
        "\u00d7": "x", "\u2248": "approximately", "\u2265": ">=", "\u2264": "<=",
        "\u201c": '"', "\u201d": '"', "\u2018": "'", "\u2019": "'",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def inline(text):
    text = escape(ascii_clean(text))
    text = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text


def make_table(rows):
    if len(rows) > 1 and all(set(cell.strip()) <= set("-:") for cell in rows[1]):
        rows = [rows[0]] + rows[2:]
    count = max(len(row) for row in rows)
    rows = [row + [""] * (count - len(row)) for row in rows]
    available = PAGE_W - 28 * mm
    widths = [available / count] * count
    data = [[Paragraph(inline(cell), ParagraphStyle("cell", parent=BODY, fontSize=6.4,
                                                    leading=8.0, spaceAfter=0)) for cell in row]
            for row in rows]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#91A9BF")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def markdown_story(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    story = []
    paragraph_lines = []
    in_code = False
    code_lines = []

    def flush_paragraph():
        nonlocal paragraph_lines
        if paragraph_lines:
            story.append(Paragraph(inline(" ".join(s.strip() for s in paragraph_lines)), BODY))
            paragraph_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("```"):
            flush_paragraph()
            if in_code:
                story.append(Preformatted(ascii_clean("\n".join(code_lines)), CODE))
                code_lines = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_lines.append(line)
            i += 1
            continue
        if stripped.startswith("|"):
            flush_paragraph()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            story.append(make_table(rows))
            story.append(Spacer(1, 5))
            continue
        if not stripped:
            flush_paragraph()
        elif stripped.startswith("### "):
            flush_paragraph(); story.append(Paragraph(inline(stripped[4:]), H3))
        elif stripped.startswith("## "):
            flush_paragraph(); story.append(Paragraph(inline(stripped[3:]), H2))
        elif stripped.startswith("# "):
            flush_paragraph(); story.append(Paragraph(inline(stripped[2:]), H1))
        elif stripped.startswith("> "):
            flush_paragraph(); story.append(Paragraph(inline(stripped[2:]), QUOTE))
        elif re.match(r"^[-*] ", stripped):
            flush_paragraph(); story.append(Paragraph(inline(stripped[2:]), BULLET, bulletText="-"))
        elif re.match(r"^\d+\. ", stripped):
            flush_paragraph()
            number, text = stripped.split(". ", 1)
            story.append(Paragraph(inline(text), BULLET, bulletText=number + "."))
        else:
            paragraph_lines.append(line)
        i += 1
    flush_paragraph()
    return story


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#A8BED2"))
    canvas.line(14 * mm, PAGE_H - 10 * mm, PAGE_W - 14 * mm, PAGE_H - 10 * mm)
    canvas.line(14 * mm, 10 * mm, PAGE_W - 14 * mm, 10 * mm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#455A70"))
    canvas.drawString(14 * mm, PAGE_H - 7.5 * mm, "Generative AI Assignment 1 viva - 20L-11327")
    canvas.drawRightString(PAGE_W - 14 * mm, 6.5 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build():
    doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=14*mm, rightMargin=14*mm,
                          topMargin=14*mm, bottomMargin=14*mm,
                          title="Generative AI Assignment 1 Viva Handbook - 20L-11327")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="viva", frames=frame, onPage=header_footer)])
    story = []
    for index, name in enumerate(FILES):
        if index:
            story.append(PageBreak())
        story.extend(markdown_story(HERE / name))
    doc.build(story)
    print(OUT)


if __name__ == "__main__":
    build()
