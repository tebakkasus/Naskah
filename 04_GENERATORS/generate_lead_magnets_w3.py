"""
Lead Magnet Asset Generator for Naskah.fk Week 3 Suite (@naskah.efka)
Strictly compliant with NASKAH.FK Universal Document Formatting Standard:
1. 100% Times New Roman across ALL elements (DOCX, PDF, PPTX).
2. Margin: A4, 4-4-3-3 cm (Left 4cm, Top 4cm, Right 3cm, Bottom 3cm).
3. Native Word XML / DOCX Headings (12-14pt Bold Times New Roman).
4. Table: Open-table standard (Zero vertical borders, thin horizontal lines).
5. Tone: PUEBI/EYD baku, 3rd-person objective, Humanizer v3.0 clean academic medicine.
"""

import os
import pathlib
from docx import Document
from docx.shared import Pt, RGBColor, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

from pptx import Presentation
from pptx.util import Inches as PptxInches, Pt as PptxPt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor as PptxRGBColor

OUT_DIR = pathlib.Path("D:/tm/06_Content/07_LEAD_MAGNETS")
OUT_DIR.mkdir(parents=True, exist_ok=True)

COLOR_BLACK = colors.HexColor("#000000")
COLOR_DARK_GRAY = colors.HexColor("#333333")
COLOR_LINE = colors.HexColor("#666666")

# ------------------------------------------------------------------------------
# DOCX HELPERS
# ------------------------------------------------------------------------------
def apply_naskah_fk_docx_styles(doc):
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(4.0)
        section.bottom_margin = Cm(3.0)
        section.left_margin = Cm(4.0)
        section.right_margin = Cm(3.0)

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

def set_run_tnr(run, size_pt=12, bold=False, italic=False, color_rgb=(0, 0, 0)):
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)
    rPr = run._element.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), 'Times New Roman')
    rFonts.set(qn('w:hAnsi'), 'Times New Roman')
    rFonts.set(qn('w:cs'), 'Times New Roman')
    rFonts.set(qn('w:eastAsia'), 'Times New Roman')
    rPr.append(rFonts)

def add_naskah_header(doc, title, subtitle):
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run(title.upper())
    set_run_tnr(r_title, size_pt=13, bold=True)
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run(subtitle)
    set_run_tnr(r_sub, size_pt=10, italic=True, color_rgb=(80, 80, 80))
    
    p_rule = doc.add_paragraph()
    p_rule.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_rule = p_rule.add_run("―" * 48)
    set_run_tnr(r_rule, size_pt=10, color_rgb=(150, 150, 150))
    p_rule.paragraph_format.space_after = Pt(12)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run_tnr(r, size_pt=12, bold=True)
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run_tnr(r, size_pt=11.5, bold=True, italic=True)
    return p

def format_open_table(table):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>\n'
            f'  <w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>\n'
            f'  <w:left w:val="none"/>\n'
            f'  <w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>\n'
            f'  <w:right w:val="none"/>\n'
            f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>\n'
            f'  <w:insideV w:val="none"/>\n'
            f'</w:tblBorders>'
        )
        tblPr[0].append(borders)

    for r_idx, row in enumerate(table.rows):
        if r_idx == 0:
            trPr = row._element.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        for cell in row.cells:
            tcPr = cell._element.get_or_add_tcPr()
            tcMar = parse_xml(
                f'<w:tcMar {nsdecls("w")}>\n'
                f'  <w:top w:w="120" w:type="dxa"/>\n'
                f'  <w:bottom w:w="120" w:type="dxa"/>\n'
                f'  <w:left w:w="140" w:type="dxa"/>\n'
                f'  <w:right w:w="140" w:type="dxa"/>\n'
                f'</w:tcMar>'
            )
            tcPr.append(tcMar)
            for p in cell.paragraphs:
                p.paragraph_format.line_spacing = 1.0
                p.paragraph_format.space_after = Pt(2)
                for run in p.runs:
                    set_run_tnr(run, size_pt=10.5, bold=run.bold, italic=run.italic)

# ------------------------------------------------------------------------------
# REPORTLAB NUMBERED CANVAS
# ------------------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Times-Roman", 9)
        self.setFillColor(colors.HexColor("#555555"))
        self.drawString(113.4, 841.89 - 60, "NASKAH.FK — ACADEMIC RESEARCH & CLINICAL DEFENSE GUIDE")
        self.setStrokeColor(colors.HexColor("#CCCCCC"))
        self.setLineWidth(0.5)
        self.line(113.4, 841.89 - 66, 595.27 - 85.05, 841.89 - 66)
        self.line(113.4, 65, 595.27 - 85.05, 65)
        self.drawString(113.4, 52, "Standar Format Baku Pendidikan Kedokteran & Riset Klinis 2026")
        self.drawRightString(595.27 - 85.05, 52, f"Halaman {self._pageNumber} dari {page_count}")
        self.restoreState()

def get_reportlab_styles():
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'NaskahTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=13,
        leading=16,
        alignment=1,
        textColor=COLOR_BLACK,
        spaceAfter=4
    )
    sub_style = ParagraphStyle(
        'NaskahSub',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=10,
        leading=13,
        alignment=1,
        textColor=colors.HexColor("#555555"),
        spaceAfter=10
    )
    h1_style = ParagraphStyle(
        'NaskahH1',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=11.5,
        leading=14.5,
        textColor=COLOR_BLACK,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'NaskahH2',
        parent=styles['Normal'],
        fontName='Times-BoldItalic',
        fontSize=10.5,
        leading=13.5,
        textColor=COLOR_BLACK,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'NaskahBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=13.5,
        textColor=COLOR_BLACK,
        spaceAfter=4
    )
    bullet_style = ParagraphStyle(
        'NaskahBullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )
    table_cell = ParagraphStyle(
        'NaskahTableCell',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9,
        leading=11.5,
        textColor=COLOR_BLACK
    )
    table_cell_bold = ParagraphStyle(
        'NaskahTableCellBold',
        parent=table_cell,
        fontName='Times-Bold'
    )
    return {
        "title": title_style, "sub": sub_style, "h1": h1_style, "h2": h2_style,
        "body": body_style, "bullet": bullet_style, "cell": table_cell, "cell_bold": table_cell_bold
    }

# ==============================================================================
# 1. W3-D1: 08_STATISTIK_Decision_Tree_Uji_Hipotesis_FK (DOCX & PDF)
# ==============================================================================
def create_w3_d1_decision_tree():
    name = "08_STATISTIK_Decision_Tree_Uji_Hipotesis_FK"
    # DOCX
    doc = Document()
    apply_naskah_fk_docx_styles(doc)
    add_naskah_header(doc, "DECISION TREE PEMILIHAN UJI HIPOTESIS FK", "Panduan Pemilihan Uji Statistik Bivariat & Multivariat Penelitian Kedokteran")
    
    add_heading_1(doc, "1. Dua Pertanyaan Kunci Penentuan Uji Hipotesis")
    p = doc.add_paragraph()
    r = p.add_run("Sebelum memilih uji statistik di SPSS/JASP, peneliti wajib menetapkan dua parameter dasar secara presisi:\n"
                  "1. Skala Pengukuran Variabel: Apakah variabel terikat (dependen) dan bebas (independen) berskala kategorik (nominal/ordinal) atau numerik (rasio/interval)?\n"
                  "2. Hubungan Kelompok Data: Apakah kelompok data bersifat bebas (independen, misalnya kelompok kasus vs kontrol) atau berpasangan (paired, misalnya pre-test vs post-test)?")
    set_run_tnr(r, 11)

    add_heading_1(doc, "2. Matriks Komprehensif Uji Hipotesis Bivariat Kedokteran")
    table = doc.add_table(rows=7, cols=4)
    format_open_table(table)
    headers = ["Jenis Variabel Bebas & Terikat", "Hubungan Kelompok", "Uji Parametrik (Normal)", "Uji Non-Parametrik (Miring)"]
    for c_idx, h in enumerate(headers):
        p = table.rows[0].cells[c_idx].paragraphs[0]
        r = p.add_run(h)
        set_run_tnr(r, 10.5, bold=True)

    data = [
        ("Numerik vs Numerik", "Korelasi / Asosiasi", "Pearson Correlation", "Spearman / Kendall's Tau"),
        ("Numerik vs Kategorik (2 Kelompok)", "Bebas (Independen)", "Independent T-Test", "Mann-Whitney U Test"),
        ("Numerik vs Kategorik (2 Kelompok)", "Berpasangan (Paired)", "Paired T-Test", "Wilcoxon Signed-Rank"),
        ("Numerik vs Kategorik (>2 Kelompok)", "Bebas (Independen)", "One-Way ANOVA", "Kruskal-Wallis Test"),
        ("Numerik vs Kategorik (>2 Kelompok)", "Berpasangan (Paired)", "Repeated Measures ANOVA", "Friedman Test"),
        ("Kategorik vs Kategorik", "Bebas (Tabel 2x2 / RxC)", "Chi-Square Test (Syarat E≥5)", "Fisher's Exact / Kolmogorov"),
    ]
    for r_idx, row_data in enumerate(data, start=1):
        for c_idx, text in enumerate(row_data):
            p = table.rows[r_idx].cells[c_idx].paragraphs[0]
            r = p.add_run(text)
            set_run_tnr(r, 10)

    add_heading_1(doc, "3. Protokol Uji Normalitas Data Klinis")
    p = doc.add_paragraph()
    r = p.add_run("• Jumlah Sampel < 50 subjek: Wajib menggunakan uji Shapiro-Wilk (Signifikan jika p > 0.05 = Distribusi Normal).\n"
                  "• Jumlah Sampel ≥ 50 subjek: Gunakan uji Kolmogorov-Smirnov atau evaluasi rasio Skewness/Kurtosis (nilai rentang -2 hingga +2).\n"
                  "• Jika data tidak normal: Lakukan transformasi logaritmik (Log10/Ln) atau langsung beralih ke uji non-parametrik.")
    set_run_tnr(r, 11)
    
    doc_path = OUT_DIR / f"{name}.docx"
    doc.save(doc_path)

    # PDF
    pdf_path = OUT_DIR / f"{name}.pdf"
    st = get_reportlab_styles()
    story = [
        Paragraph("DECISION TREE PEMILIHAN UJI HIPOTESIS FK", st["title"]),
        Paragraph("Panduan Pemilihan Uji Statistik Bivariat & Multivariat Penelitian Kedokteran", st["sub"]),
        HRFlowable(width="100%", thickness=1, color=COLOR_LINE, spaceBefore=4, spaceAfter=8),
        Paragraph("1. Dua Pertanyaan Kunci Penentuan Uji Hipotesis", st["h1"]),
        Paragraph("Sebelum memilih uji statistik, peneliti wajib menetapkan dua parameter dasar secara presisi: (1) Skala variabel (kategorik vs numerik) dan (2) Hubungan antarkelompok sampel (bebas vs berpasangan).", st["body"]),
        Spacer(1, 4),
        Paragraph("2. Matriks Komprehensif Uji Hipotesis Bivariat Kedokteran", st["h1"]),
    ]
    t_data = [[Paragraph(f"<b>{h}</b>", st["cell_bold"]) for h in headers]]
    for row in data:
        t_data.append([Paragraph(cell, st["cell"]) for cell in row])
    t = Table(t_data, colWidths=[120, 85, 105, 95])
    t.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 1, COLOR_BLACK),
        ('LINEBELOW', (0,0), (-1,0), 0.5, COLOR_BLACK),
        ('LINEBELOW', (0,-1), (-1,-1), 1, COLOR_BLACK),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t)
    story.append(Spacer(1, 6))
    story.append(Paragraph("3. Protokol Uji Normalitas Data Klinis", st["h1"]))
    story.append(Paragraph("• Sampel < 50 subjek: Wajib menggunakan uji Shapiro-Wilk (Distribusi normal jika p > 0.05).", st["bullet"]))
    story.append(Paragraph("• Sampel ≥ 50 subjek: Gunakan uji Kolmogorov-Smirnov atau rasio Skewness/Kurtosis.", st["bullet"]))
    story.append(Paragraph("• Data tidak normal: Lakukan transformasi data atau gunakan uji non-parametrik yang ekuivalen.", st["bullet"]))

    pdf_doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=113.4, rightMargin=85.05, topMargin=113.4, bottomMargin=85.05)
    pdf_doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated W3-D1: {name}")

# ==============================================================================
# 2. W3-D2: 09_INTERPRETASI_CheatSheet_Odds_Ratio_RR_pVal (DOCX & PDF)
# ==============================================================================
def create_w3_d2_odds_ratio():
    name = "09_INTERPRETASI_CheatSheet_Odds_Ratio_RR_pVal"
    doc = Document()
    apply_naskah_fk_docx_styles(doc)
    add_naskah_header(doc, "CHEAT SHEET INTERPRETASI OR, RR, & 95% CI", "Pedoman Pelaporan Ukuran Asosiasi dan Kekuatan Hubungan Klinis")

    add_heading_1(doc, "1. Definisi dan Aplikasi Desain Studi")
    p = doc.add_paragraph()
    r = p.add_run("• Odds Ratio (OR): Digunakan khusus pada desain Case-Control dan analisis Multivariat Regresi Logistik. Mengukur rasio kemungkinan terpapar pada kelompok sakit dibandingkan kelompok tidak sakit.\n"
                  "• Relative Risk (RR): Digunakan pada desain Cohort dan Uji Klinis (RCT). Mengukur rasio insiden penyakit pada kelompok terpapar dibandingkan kelompok tidak terpapar.\n"
                  "• Prevalence Ratio (PR): Digunakan pada studi potong lintang (Cross-Sectional) untuk mengukur rasio prevalensi penyakit.")
    set_run_tnr(r, 11)

    add_heading_1(doc, "2. Aturan Baku Nilai 1 (The Null Value) dan Rentang 95% CI")
    table = doc.add_table(rows=4, cols=3)
    format_open_table(table)
    headers = ["Nilai OR / RR", "Rentang 95% Confidence Interval", "Interpretasi & Kesimpulan Ilmiah"]
    for c_idx, h in enumerate(headers):
        p = table.rows[0].cells[c_idx].paragraphs[0]
        r = p.add_run(h)
        set_run_tnr(r, 10.5, bold=True)

    data = [
        ("OR / RR > 1.0", "Batas bawah > 1.0 (misal: 1.45 - 3.80)", "Faktor Risiko Signifikan (Meningkatkan risiko sakit secara bermakna)."),
        ("OR / RR < 1.0", "Batas atas < 1.0 (misal: 0.32 - 0.78)", "Faktor Protektif Signifikan (Menurunkan risiko sakit secara bermakna)."),
        ("OR / RR > 1.0 atau < 1.0", "Melewati angka 1.0 (misal: 0.82 - 2.45)", "Tidak Signifikan secara statistik (Hipotesis nol gagal ditolak)."),
    ]
    for r_idx, row_data in enumerate(data, start=1):
        for c_idx, text in enumerate(row_data):
            p = table.rows[r_idx].cells[c_idx].paragraphs[0]
            r = p.add_run(text)
            set_run_tnr(r, 10)

    add_heading_1(doc, "3. Template Kalimat Pelaporan Bab 4 Skripsi FK")
    p = doc.add_paragraph()
    r = p.add_run("Contoh Pelaporan Baku:\n"
                  "\"Berdasarkan hasil analisis multivariat regresi logistik, pasien dengan riwayat diabetes melitus memiliki odds 2,45 kali lebih tinggi mengalami kejadian ulkus diabetikum dibandingkan pasien tanpa riwayat diabetes, dan hubungan ini signifikan secara statistik (OR = 2,45; 95% CI: 1,28 – 4,69; p = 0,007).\"")
    set_run_tnr(r, 10.5, italic=True)

    doc_path = OUT_DIR / f"{name}.docx"
    doc.save(doc_path)

    # PDF
    pdf_path = OUT_DIR / f"{name}.pdf"
    st = get_reportlab_styles()
    story = [
        Paragraph("CHEAT SHEET INTERPRETASI OR, RR, & 95% CI", st["title"]),
        Paragraph("Pedoman Pelaporan Ukuran Asosiasi dan Kekuatan Hubungan Klinis", st["sub"]),
        HRFlowable(width="100%", thickness=1, color=COLOR_LINE, spaceBefore=4, spaceAfter=8),
        Paragraph("1. Definisi dan Aplikasi Desain Studi", st["h1"]),
        Paragraph("• Odds Ratio (OR): Desain Case-Control & Regresi Logistik.<br/>• Relative Risk (RR): Desain Cohort & Clinical Trial.<br/>• Prevalence Ratio (PR): Desain Cross-Sectional.", st["body"]),
        Spacer(1, 4),
        Paragraph("2. Aturan Baku Nilai 1 (The Null Value) dan Rentang 95% CI", st["h1"]),
    ]
    t_data = [[Paragraph(f"<b>{h}</b>", st["cell_bold"]) for h in headers]]
    for row in data:
        t_data.append([Paragraph(cell, st["cell"]) for cell in row])
    t = Table(t_data, colWidths=[95, 125, 185])
    t.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 1, COLOR_BLACK),
        ('LINEBELOW', (0,0), (-1,0), 0.5, COLOR_BLACK),
        ('LINEBELOW', (0,-1), (-1,-1), 1, COLOR_BLACK),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 6))
    story.append(Paragraph("3. Template Kalimat Pelaporan Bab 4 Skripsi FK", st["h1"]))
    story.append(Paragraph("<i>\"Berdasarkan analisis multivariat, pasien dengan riwayat diabetes melitus memiliki odds 2,45 kali lebih tinggi mengalami komplikasi secara signifikan (OR = 2,45; 95% CI: 1,28 – 4,69; p = 0,007).\"</i>", st["body"]))

    pdf_doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=113.4, rightMargin=85.05, topMargin=113.4, bottomMargin=85.05)
    pdf_doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated W3-D2: {name}")

# ==============================================================================
# 3. W3-D3: 10_TABEL1_Template_Karakteristik_Subjek_Word (DOCX & PDF)
# ==============================================================================
def create_w3_d3_tabel1():
    name = "10_TABEL1_Template_Karakteristik_Subjek_Word"
    doc = Document()
    apply_naskah_fk_docx_styles(doc)
    add_naskah_header(doc, "TEMPLATE TABEL 1 KARAKTERISTIK SUBJEK PENELITIAN", "Format Baku Open-Table Standar Jurnal Terakreditasi & Skripsi FK")

    add_heading_1(doc, "Tabel 1. Karakteristik Demografi dan Klinis Subjek Penelitian (N = 120)")
    table = doc.add_table(rows=12, cols=4)
    format_open_table(table)
    headers = ["Karakteristik Subjek", "Kelompok Kasus (n = 60)", "Kelompok Kontrol (n = 60)", "Nilai p"]
    for c_idx, h in enumerate(headers):
        p = table.rows[0].cells[c_idx].paragraphs[0]
        r = p.add_run(h)
        set_run_tnr(r, 10.5, bold=True)

    data = [
        ("Usia (tahun), Mean ± SD", "52,4 ± 8,1", "51,8 ± 7,9", "0,678*"),
        ("Jenis Kelamin, n (%)", "", "", "0,452**"),
        ("  - Laki-laki", "34 (56,7%)", "38 (63,3%)", ""),
        ("  - Perempuan", "26 (43,3%)", "22 (36,7%)", ""),
        ("Indeks Massa Tubuh (kg/m²), Median (IQR)", "26,2 (23,1 - 29,4)", "23,8 (21,5 - 26,0)", "0,012***"),
        ("Status Merokok, n (%)", "", "", "0,028**"),
        ("  - Merokok Aktif", "28 (46,7%)", "15 (25,0%)", ""),
        ("  - Bukan Perokok", "32 (53,3%)", "45 (75,0%)", ""),
        ("Tekanan Darah Sistolik (mmHg), Mean ± SD", "138,5 ± 14,2", "122,1 ± 10,8", "<0,001*"),
        ("Kadar HbA1c (%), Mean ± SD", "7,8 ± 1,4", "5,6 ± 0,7", "<0,001*"),
        ("Lama Menderita Sakit (tahun), Median (Min-Max)", "6 (1 - 18)", "0 (0 - 0)", "-"),
    ]
    for r_idx, row_data in enumerate(data, start=1):
        for c_idx, text in enumerate(row_data):
            p = table.rows[r_idx].cells[c_idx].paragraphs[0]
            r = p.add_run(text)
            set_run_tnr(r, 10)

    p_note = doc.add_paragraph()
    p_note.paragraph_format.space_before = Pt(4)
    r_note = p_note.add_run(
        "Catatan Kaki Tabel (Wajib Dicantumkan):\n"
        "SD: Standar Deviasi; IQR: Interquartile Range (Kuartil 1 - Kuartil 3); N: Total subjek.\n"
        "* Uji Independent T-Test (distribusi data normal).\n"
        "** Uji Chi-Square (data kategorik nominal).\n"
        "*** Uji Mann-Whitney U Test (distribusi data tidak normal)."
    )
    set_run_tnr(r_note, size_pt=9.5, italic=True)

    doc_path = OUT_DIR / f"{name}.docx"
    doc.save(doc_path)

    # PDF
    pdf_path = OUT_DIR / f"{name}.pdf"
    st = get_reportlab_styles()
    story = [
        Paragraph("TEMPLATE TABEL 1 KARAKTERISTIK SUBJEK", st["title"]),
        Paragraph("Format Baku Open-Table Standar Jurnal Terakreditasi & Skripsi FK", st["sub"]),
        HRFlowable(width="100%", thickness=1, color=COLOR_LINE, spaceBefore=4, spaceAfter=8),
        Paragraph("<b>Tabel 1. Karakteristik Demografi dan Klinis Subjek (N = 120)</b>", st["body"]),
        Spacer(1, 2),
    ]
    t_data = [[Paragraph(f"<b>{h}</b>", st["cell_bold"]) for h in headers]]
    for row in data:
        t_data.append([Paragraph(cell, st["cell"]) for cell in row])
    t = Table(t_data, colWidths=[160, 95, 95, 55])
    t.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 1, COLOR_BLACK),
        ('LINEBELOW', (0,0), (-1,0), 0.5, COLOR_BLACK),
        ('LINEBELOW', (0,-1), (-1,-1), 1, COLOR_BLACK),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t)
    story.append(Spacer(1, 4))
    story.append(Paragraph("<font size=8><i>Catatan: SD: Standar Deviasi; IQR: Interquartile Range. *Uji Independent T-Test, **Uji Chi-Square, ***Uji Mann-Whitney U.</i></font>", st["body"]))

    pdf_doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=113.4, rightMargin=85.05, topMargin=113.4, bottomMargin=85.05)
    pdf_doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated W3-D3: {name}")

# ==============================================================================
# 4. W3-D4: 11_SIDANG_Bank_Pertanyaan_Penguji_dan_Script_Jawaban (DOCX & PDF)
# ==============================================================================
def create_w3_d4_bank_pertanyaan_sidang():
    name = "11_SIDANG_Bank_Pertanyaan_Penguji_dan_Script_Jawaban"
    doc = Document()
    apply_naskah_fk_docx_styles(doc)
    add_naskah_header(doc, "BANK PERTANYAAN SIDANG SKRIPSI FK & SCRIPT JAWABAN", "Panduan Taktis Menghadapi Penguji Sidang Proposal dan Hasil Riset Medis")

    q_and_a = [
        ("1. Pertanyaan Metodologi Dasar",
         "Penguji: \"Mengapa kamu memilih desain Cross-Sectional dan bukan Case-Control?\"",
         "Script Jawaban Taktis: \"Terima kasih atas pertanyaannya Dokter/Prof. Kami memilih desain Cross-Sectional karena tujuan utama penelitian ini adalah untuk menilai prevalensi penyakit X serta mengamati distribusi faktor risiko Y secara serentak dalam satu titik waktu di populasi klinis RS Z, mengingat keterbatasan waktu follow-up dan belum tersedianya data longitudinal di rekam medis.\""),
        ("2. Pertanyaan Besar Sampel",
         "Penguji: \"Bagaimana kamu menentukan besar sampel minimal 86 subjek ini?\"",
         "Script Jawaban Taktis: \"Besar sampel dihitung menggunakan rumus estimasi proporsi populasi absolut/uji hipotesis beda dua proporsi (Sastroasmoro, 2014) dengan menetapkan tingkat kemaknaan alpha 5% (Zα = 1,96), power uji 80% (Zβ = 0,84), serta mengacu pada proporsi paparan p1 dan p2 dari studi terdahulu oleh Smith et al. (2023). Kami juga menambahkan 10% estimasi drop-out.\""),
        ("3. Pertanyaan Pengendalian Bias dan Perancu",
         "Penguji: \"Apakah variabel usia tidak menjadi confounder dalam penelitian kamu?\"",
         "Script Jawaban Taktis: \"Benar Dokter/Prof. Usia berpotensi menjadi perancu. Oleh karena itu, pada tahap desain kami melakukan restriksi rentang usia subjek (40-60 tahun), dan pada tahap analisis bivariat/multivariat kami menyertakan variabel usia ke dalam model regresi logistik ganda untuk mengontrol efek confounding secara statistik.\""),
        ("4. Pertanyaan Hasil Tidak Signifikan (p > 0.05)",
         "Penguji: \"Kenapa hasil analisis bivariat kamu menunjukkan nilai p = 0,145 (tidak ada hubungan)?\"",
         "Script Jawaban Taktis: \"Secara statistik, nilai p = 0,145 menunjukkan hipotesis nol gagal ditolak. Hal ini secara biologis dapat dijelaskan oleh mekanisme kompensasi jalur Z. Selain itu, kami mengevaluasi adanya potensi underpowered sample akibat variasi klinis responden yang lebih heterogen dibandingkan studi referensi.\""),
    ]

    for category, q, a in q_and_a:
        add_heading_1(doc, category)
        p_q = doc.add_paragraph()
        r_q = p_q.add_run(q)
        set_run_tnr(r_q, 11, bold=True, italic=True)
        
        p_a = doc.add_paragraph()
        r_a = p_a.add_run(a)
        set_run_tnr(r_a, 11)

    doc_path = OUT_DIR / f"{name}.docx"
    doc.save(doc_path)

    # PDF
    pdf_path = OUT_DIR / f"{name}.pdf"
    st = get_reportlab_styles()
    story = [
        Paragraph("BANK PERTANYAAN SIDANG SKRIPSI FK", st["title"]),
        Paragraph("Panduan Taktis Menghadapi Penguji Sidang Proposal & Skripsi", st["sub"]),
        HRFlowable(width="100%", thickness=1, color=COLOR_LINE, spaceBefore=4, spaceAfter=8),
    ]
    for category, q, a in q_and_a:
        story.append(Paragraph(category, st["h1"]))
        story.append(Paragraph(f"<b>{q}</b>", st["body"]))
        story.append(Paragraph(f"<i>{a}</i>", st["body"]))
        story.append(Spacer(1, 4))

    pdf_doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=113.4, rightMargin=85.05, topMargin=113.4, bottomMargin=85.05)
    pdf_doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated W3-D4: {name}")

# ==============================================================================
# 5. W3-D5: 12_PRESENTASI_PPT_Sidang_10_Menit_Naskah (PPTX & PDF Guide)
# ==============================================================================
def create_w3_d5_pptx_template():
    name_pptx = "12_PRESENTASI_PPT_Sidang_10_Menit_Naskah"
    prs = Presentation()
    prs.slide_width = PptxInches(13.333)
    prs.slide_height = PptxInches(7.5)

    blank_layout = prs.slide_layouts[6]
    
    slides_data = [
        ("UJI HUBUNGAN BIOMARKER X DENGAN DERAJAT KEPARAHAN PENYAKIT Y", "Nama Mahasiswa: dr. Muda X | NIM: 202601001\nFakultas Kedokteran Universitas Naskah\nDosen Pembimbing: Dr. dr. Sp.PD, K-GEH"),
        ("1. LATAR BELAKANG & RESEARCH GAP (1.5 Menit)", "• Masalah Klinis: Penyakit Y menyebabkan mortalitas 14.2% di RS Rujukan.\n• Gap Penelitian: Peran biomarker X belum pernah dievaluasi pada populasi lokal Indonesia.\n• Urgensi: Deteksi dini mampu menurunkan durasi rawat inap ICU."),
        ("2. RUMUSAN MASALAH & HIPOTESIS (30 Detik)", "• Rumusan Masalah: Apakah terdapat hubungan antara kadar serum biomarker X dengan skor keparahan klinis Y?\n• Hipotesis: Terdapat korelasi positif yang signifikan antara kadar biomarker X dengan derajat keparahan Y."),
        ("3. METODOLOGI PENELITIAN (2 Menit)", "• Desain: Observasional Analitik dengan pendekatan Cross-Sectional.\n• Populasi & Sampel: 86 pasien terkonfirmasi Y (Consecutive Sampling).\n• Kriteria Inklusi: Pasien usia 18-65 tahun yang terdiagnosis klinis dan lab.\n• Analisis Data: Uji Korelasi Spearman & Multivariat Regresi Linier."),
        ("4. HASIL: KARAKTERISTIK SUBJEK (Tabel 1) (1.5 Menit)", "• Usia Rerata: 48.6 ± 11.2 tahun (58% Laki-laki).\n• Skor Keparahan Rerata: 18.4 ± 4.2 poin.\n• Kadar Median Biomarker X: 45.2 pg/mL (IQR: 28.1 - 82.4 pg/mL)."),
        ("5. HASIL: ANALISIS BIVARIAT & MULTIVARIAT (2 Menit)", "• Nilai Korelasi: r = 0.642 (Korelasi Kuat Positif).\n• Nilai Signifikansi: p < 0.001 (Signifikan secara statistik).\n• Model Multivariat: Biomarker X tetap independen setelah dikontrol usia dan komorbid (p = 0.004)."),
        ("6. PEMBAHASAN & KETERBATASAN (1.5 Menit)", "• Kesesuaian Teori: Biomarker X merefleksikan badai sitokin pro-inflamasi.\n• Keterbatasan Studi: Desain potong lintang belum dapat membuktikan hubungan kausalitas temporal mutlak."),
        ("7. KESIMPULAN & SARAN (30 Detik)", "• Kesimpulan: Biomarker X berkorelasi kuat dan signifikan dengan keparahan klinis Y.\n• Saran: Diperlukan uji klinis longitudinal untuk mengevaluasi cut-off prognostik terapi.")
    ]

    for title, body in slides_data:
        slide = prs.slides.add_slide(blank_layout)
        # Title Box
        tb_title = slide.shapes.add_textbox(PptxInches(1.0), PptxInches(0.8), PptxInches(11.333), PptxInches(1.2))
        tf_title = tb_title.text_frame
        tf_title.word_wrap = True
        p_t = tf_title.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Times New Roman"
        p_t.font.size = PptxPt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = PptxRGBColor(7, 23, 38) # Navy

        # Body Box
        tb_body = slide.shapes.add_textbox(PptxInches(1.0), PptxInches(2.2), PptxInches(11.333), PptxInches(4.5))
        tf_body = tb_body.text_frame
        tf_body.word_wrap = True
        for line in body.split("\n"):
            p_b = tf_body.add_paragraph()
            p_b.text = line
            p_b.font.name = "Times New Roman"
            p_b.font.size = PptxPt(16)
            p_b.font.color.rgb = PptxRGBColor(0, 0, 0)
            p_b.space_after = PptxPt(8)

    pptx_path = OUT_DIR / f"{name_pptx}.pptx"
    prs.save(str(pptx_path))
    print(f"Generated W3-D5 PPTX: {name_pptx}")

    # Companion PDF Guide
    name_pdf = "12_PRESENTASI_Panduan_Slide_Sidang_10_Menit_FK"
    pdf_path = OUT_DIR / f"{name_pdf}.pdf"
    st = get_reportlab_styles()
    story = [
        Paragraph("PANDUAN STRUKTUR SLIDE SIDANG 10 MENIT FK", st["title"]),
        Paragraph("Blueprint Alokasi Waktu dan Hierarki Informasi Presentasi Sidang", st["sub"]),
        HRFlowable(width="100%", thickness=1, color=COLOR_LINE, spaceBefore=4, spaceAfter=8),
        Paragraph("1. Blueprint 8 Slide Esensial Sidang Skripsi Kedokteran", st["h1"]),
        Paragraph("• Slide 1: Judul, Nama Peneliti, Pembimbing, & Institusi (15 detik).<br/>"
                  "• Slide 2: Latar Belakang & Research Gap Klinis (1.5 menit).<br/>"
                  "• Slide 3: Rumusan Masalah & Hipotesis (30 detik).<br/>"
                  "• Slide 4: Kerangka Konsep & Metodologi Inti (2 menit).<br/>"
                  "• Slide 5: Tabel 1 Karakteristik Subjek (1.5 menit).<br/>"
                  "• Slide 6: Analisis Bivariat / Multivariat Utama (2 menit).<br/>"
                  "• Slide 7: Pembahasan Klinis & Keterbatasan Studi (1.5 menit).<br/>"
                  "• Slide 8: Kesimpulan & Rekomendasi Aplikatif (30 detik).", st["body"]),
        Spacer(1, 4),
        Paragraph("2. Tiga Larangan Mutlak Presentasi Sidang Meja Hijau", st["h1"]),
        Paragraph("1. Dilarang menyalin teks paragraf utuh ke dalam slide (Gunakan diagram/poin kunci).<br/>"
                  "2. Dilarang membaca slide kata per kata (Pertahankan eye-contact dengan penguji).<br/>"
                  "3. Dilarang melebihi durasi alokasi waktu yang ditentukan panitia sidang.", st["body"]),
    ]
    pdf_doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=113.4, rightMargin=85.05, topMargin=113.4, bottomMargin=85.05)
    pdf_doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated W3-D5 PDF: {name_pdf}")

# ==============================================================================
# 6. W3-D6: 13_NON_SIGNIFIKAN_Panduan_Bahas_Hasil_Negatif_Bab5 (DOCX & PDF)
# ==============================================================================
def create_w3_d6_hasil_negatif():
    name = "13_NON_SIGNIFIKAN_Panduan_Bahas_Hasil_Negatif_Bab5"
    doc = Document()
    apply_naskah_fk_docx_styles(doc)
    add_naskah_header(doc, "PANDUAN MENULIS PEMBAHASAN HASIL TIDAK SIGNIFIKAN", "Strategi Penyusunan Bab 5 Skripsi FK untuk Temuan Riset p > 0.05")

    add_heading_1(doc, "1. Paradigma Ilmiah Temuan Hasil Negatif (p > 0.05)")
    p = doc.add_paragraph()
    r = p.add_run("Nilai p > 0.05 (hipotesis nol gagal ditolak) bukanlah kegagalan penelitian. Dalam sains kedokteran, membuktikan bahwa suatu intervensi atau faktor risiko tidak berhubungan dengan luaran klinis memberikan kontribusi ilmiah yang sama pentingnya untuk mencegah bias publikasi.")
    set_run_tnr(r, 11)

    add_heading_1(doc, "2. Kerangka 4 Langkah Menulis Pembahasan Bab 5")
    steps = [
        ("Langkah 1: Komparasi Objektif", "Bandingkan temuan penelitian dengan studi terdahulu yang memiliki kesimpulan serupa atau bertolak belakang."),
        ("Langkah 2: Eksplorasi Mekanisme Biologis", "Jelaskan kemungkinan jalur patofisiologi alternatif, kompensasi homeostasis tubuh, atau metabolisme farmakologis yang mendasari tidak munculnya efek."),
        ("Langkah 3: Evaluasi Faktor Metodologi", "Evaluasi apakah terdapat potensi keterbatasan besar sampel (underpowered study / Type II Error), rentang dosis paparan yang terlalu sempit, atau instrumen pengukuran."),
        ("Langkah 4: Implikasi Klinis & Saran Riset", "Tegaskan implikasi hasil ini bagi praktik medis dan sarankan metodologi perbaikan untuk penelitian multisenter berikutnya.")
    ]
    for title, desc in steps:
        add_heading_2(doc, title)
        p_s = doc.add_paragraph()
        r_s = p_s.add_run(desc)
        set_run_tnr(r_s, 11)

    doc_path = OUT_DIR / f"{name}.docx"
    doc.save(doc_path)

    # PDF
    pdf_path = OUT_DIR / f"{name}.pdf"
    st = get_reportlab_styles()
    story = [
        Paragraph("PANDUAN MEMBAHAS HASIL RISET p > 0.05", st["title"]),
        Paragraph("Strategi Penyusunan Bab 5 Pembahasan Skripsi FK", st["sub"]),
        HRFlowable(width="100%", thickness=1, color=COLOR_LINE, spaceBefore=4, spaceAfter=8),
        Paragraph("1. Paradigma Ilmiah Hasil Negatif", st["h1"]),
        Paragraph("Nilai p > 0.05 bukanlah kegagalan penelitian. Menunjukkan tidak adanya hubungan kausalitas tetap merupakan kontribusi ilmiah valid yang melindungi pasien dari tindakan invasif yang tidak perlu.", st["body"]),
        Spacer(1, 4),
        Paragraph("2. Kerangka 4 Langkah Menulis Bab 5", st["h1"]),
    ]
    for title, desc in steps:
        story.append(Paragraph(f"<b>{title}</b>", st["h2"]))
        story.append(Paragraph(desc, st["body"]))
        story.append(Spacer(1, 2))

    pdf_doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=113.4, rightMargin=85.05, topMargin=113.4, bottomMargin=85.05)
    pdf_doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated W3-D6: {name}")

# ==============================================================================
# 7. W3-D7: 14_SOP_Audit_Skripsi_15_Menit_Checklist (DOCX & PDF)
# ==============================================================================
def create_w3_d7_sop_audit():
    name = "14_SOP_Audit_Skripsi_15_Menit_Checklist"
    doc = Document()
    apply_naskah_fk_docx_styles(doc)
    add_naskah_header(doc, "CHECKLIST 15 MENIT SELF-AUDIT SKRIPSI FK", "SOP Verifikasi Bab 4, Analisis Data, dan Konsistensi Metodologi Riset Kedokteran")

    add_heading_1(doc, "Tabel Audit 15 Menit Pre-Submission Naskah Skripsi FK")
    table = doc.add_table(rows=11, cols=3)
    format_open_table(table)
    headers = ["No", "Poin Verifikasi Kritis Naskah", "Kriteria Lolos Uji (ACC Standar)"]
    for c_idx, h in enumerate(headers):
        p = table.rows[0].cells[c_idx].paragraphs[0]
        r = p.add_run(h)
        set_run_tnr(r, 10.5, bold=True)

    items = [
        ("1", "Konsistensi Jumlah Sampel (N)", "Angka N di Bab 3, seluruh tabel Bab 4, dan abstrak identik tanpa ada subjek hilang."),
        ("2", "Kesesuaian Uji Statistik", "Uji parametrik memiliki bukti lolos uji normalitas; uji kategorik memenuhi syarat expected count."),
        ("3", "Format Standar Tabel 1", "Tabel menganut format Open-Table (hanya 3 garis horizontal, tanpa garis vertikal)."),
        ("4", "Presisi Desimal & Nilai p", "Nilai p ditulis eksak 3 angka desimal (misal: p = 0,024), kecuali p < 0,001."),
        ("5", "Notasi Angka Baku Indonesia", "Pemisah desimal menggunakan tanda koma (bukan titik) untuk naskah berbahasa Indonesia."),
        ("6", "Definisi Singkatan Footnote", "Seluruh singkatan medis pada tabel didefinisikan lengkap pada catatan kaki."),
        ("7", "Sinkronisasi Bab 4 & Bab 5", "Setiap temuan statistik utama di Bab 4 dibahas mekanismenya di Bab 5."),
        ("8", "Keterbatasan Penelitian", "Bab 5 mencantumkan minimal 2 keterbatasan metodologi secara objektif."),
        ("9", "Kesimpulan Menjawab Tujuan", "Jumlah poin kesimpulan di Bab 6 sesuai dengan jumlah tujuan khusus di Bab 1."),
        ("10", "Daftar Pustaka Aktif", "Seluruh kutipan di badan teks tersinkronisasi 100% di Daftar Pustaka (Mendeley/Zotero)."),
    ]
    for r_idx, (num, poin, crit) in enumerate(items, start=1):
        table.rows[r_idx].cells[0].paragraphs[0].add_run(num)
        table.rows[r_idx].cells[1].paragraphs[0].add_run(poin)
        table.rows[r_idx].cells[2].paragraphs[0].add_run(crit)
        for cell in table.rows[r_idx].cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    set_run_tnr(r, 10)

    doc_path = OUT_DIR / f"{name}.docx"
    doc.save(doc_path)

    # PDF
    pdf_path = OUT_DIR / f"{name}.pdf"
    st = get_reportlab_styles()
    story = [
        Paragraph("CHECKLIST 15 MENIT SELF-AUDIT SKRIPSI FK", st["title"]),
        Paragraph("SOP Verifikasi Bab 4, Analisis Data, dan Konsistensi Metodologi", st["sub"]),
        HRFlowable(width="100%", thickness=1, color=COLOR_LINE, spaceBefore=4, spaceAfter=8),
        Paragraph("<b>Tabel Verifikasi Kritis Naskah Skripsi FK</b>", st["body"]),
        Spacer(1, 2),
    ]
    t_data = [[Paragraph(f"<b>{h}</b>", st["cell_bold"]) for h in headers]]
    for num, poin, crit in items:
        t_data.append([Paragraph(num, st["cell"]), Paragraph(poin, st["cell_bold"]), Paragraph(crit, st["cell"])])
    t = Table(t_data, colWidths=[25, 175, 205])
    t.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 1, COLOR_BLACK),
        ('LINEBELOW', (0,0), (-1,0), 0.5, COLOR_BLACK),
        ('LINEBELOW', (0,-1), (-1,-1), 1, COLOR_BLACK),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t)

    pdf_doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=113.4, rightMargin=85.05, topMargin=113.4, bottomMargin=85.05)
    pdf_doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated W3-D7: {name}")

def main():
    print("=== Generating Week 3 Lead Magnets ===")
    create_w3_d1_decision_tree()
    create_w3_d2_odds_ratio()
    create_w3_d3_tabel1()
    create_w3_d4_bank_pertanyaan_sidang()
    create_w3_d5_pptx_template()
    create_w3_d6_hasil_negatif()
    create_w3_d7_sop_audit()
    print("=== All 7 Week 3 Lead Magnets Successfully Generated! ===")

if __name__ == "__main__":
    main()
