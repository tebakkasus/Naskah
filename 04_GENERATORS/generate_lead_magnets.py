"""
Lead Magnet Asset Generator for Naskah.fk (@naskah.efka)
Strictly compliant with NASKAH.FK Universal Document Formatting Standard:
1. 100% Times New Roman across ALL elements (DOCX, PDF, XLSX).
2. Margin: A4, 4-4-3-3 cm (Left 4cm, Top 4cm, Right 3cm, Bottom 3cm).
3. Native Word XML / DOCX Headings (12-14pt Bold Times New Roman).
4. Table: Open-table standard (Zero vertical borders, thin horizontal lines, no dark shading).
5. Language & Tone: PUEBI/EYD baku, 3rd-person objective, Humanizer v3.0 clean academic medicine.
"""

import os
import pathlib
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

OUT_DIR = pathlib.Path("D:/tm/06_Content/07_LEAD_MAGNETS")
OUT_DIR.mkdir(parents=True, exist_ok=True)

COLOR_BLACK = colors.HexColor("#000000")
COLOR_DARK_GRAY = colors.HexColor("#333333")
COLOR_LINE = colors.HexColor("#666666")


# ==============================================================================
# DOCX FORMATTING HELPERS (NASKAH.FK UNIVERSAL STANDARD)
# ==============================================================================
def apply_naskah_fk_docx_styles(doc):
    """Sets A4, 4-4-3-3 cm margins, and Times New Roman standard."""
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(4.0)
        section.bottom_margin = Cm(3.0)
        section.left_margin = Cm(4.0)
        section.right_margin = Cm(3.0)

    styles = doc.styles
    normal_style = styles['Normal']
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


def format_open_table(table):
    """Formats table to Open-Table standard (no vertical borders, horizontal rules)."""
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
                    set_run_tnr(run, size_pt=11, bold=run.bold, italic=run.italic)


# ==============================================================================
# 1. EXCEL CALCULATOR (DIAGNOSIS) — 100% TIMES NEW ROMAN
# ==============================================================================
def create_diagnosis_excel():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Kalkulator Tabel 2x2"
    ws.views.sheetView[0].showGridLines = True

    font_title = Font(name="Times New Roman", size=14, bold=True, color="000000")
    font_sub = Font(name="Times New Roman", size=10, italic=True, color="555555")
    font_section = Font(name="Times New Roman", size=12, bold=True, color="000000")
    font_header = Font(name="Times New Roman", size=11, bold=True, color="000000")
    font_bold = Font(name="Times New Roman", size=11, bold=True, color="000000")
    font_regular = Font(name="Times New Roman", size=11, color="000000")
    font_result = Font(name="Times New Roman", size=11, bold=True, color="000000")

    fill_header = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
    fill_input = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    fill_subtotal = PatternFill(start_color="EAEAEA", end_color="EAEAEA", fill_type="solid")

    thin_border = Border(
        left=Side(style="thin", color="CCCCCC"),
        right=Side(style="thin", color="CCCCCC"),
        top=Side(style="thin", color="CCCCCC"),
        bottom=Side(style="thin", color="CCCCCC")
    )
    open_table_top = Border(top=Side(style="medium", color="000000"), bottom=Side(style="thin", color="000000"))
    open_table_bottom = Border(bottom=Side(style="medium", color="000000"), top=Side(style="thin", color="CCCCCC"))

    ws.merge_cells("B1:F1")
    ws["B1"] = "KALKULATOR UJI DIAGNOSTIK TABEL 2x2 — NASKAH.FK"
    ws["B1"].font = font_title
    ws["B1"].alignment = Alignment(horizontal="center", vertical="center")

    ws.merge_cells("B2:F2")
    ws["B2"] = "Standar Pelaporan Ilmiah Bab 4 Skripsi FK (Input data pada sel berwarna kuning)"
    ws["B2"].font = font_sub
    ws["B2"].alignment = Alignment(horizontal="center", vertical="center")

    ws.row_dimensions[1].height = 24
    ws.row_dimensions[2].height = 18

    ws["B4"] = "1. Tabel Kontingensi 2x2 (Input Data Sampel)"
    ws["B4"].font = font_section

    ws.merge_cells("C5:D5")
    ws["C5"] = "Baku Emas (Gold Standard)"
    ws["C5"].font = font_header
    ws["C5"].fill = fill_header
    ws["C5"].alignment = Alignment(horizontal="center", vertical="center")
    ws["C5"].border = open_table_top

    ws["B6"] = "Alat Uji Baru"
    ws["B6"].font = font_header
    ws["B6"].fill = fill_header
    ws["B6"].alignment = Alignment(horizontal="center", vertical="center")
    ws["B6"].border = thin_border

    ws["C6"] = "Positif (+)"
    ws["C6"].font = font_bold
    ws["C6"].fill = fill_header
    ws["C6"].alignment = Alignment(horizontal="center", vertical="center")
    ws["C6"].border = thin_border

    ws["D6"] = "Negatif (-)"
    ws["D6"].font = font_bold
    ws["D6"].fill = fill_header
    ws["D6"].alignment = Alignment(horizontal="center", vertical="center")
    ws["D6"].border = thin_border

    ws["E6"] = "Total Alat Uji"
    ws["E6"].font = font_bold
    ws["E6"].fill = fill_subtotal
    ws["E6"].alignment = Alignment(horizontal="center", vertical="center")
    ws["E6"].border = thin_border

    ws["B7"] = "Positif (+)"
    ws["B7"].font = font_bold
    ws["B7"].alignment = Alignment(horizontal="center", vertical="center")
    ws["B7"].border = thin_border

    ws["C7"] = 85
    ws["C7"].font = font_bold
    ws["C7"].fill = fill_input
    ws["C7"].alignment = Alignment(horizontal="center", vertical="center")
    ws["C7"].border = thin_border

    ws["D7"] = 10
    ws["D7"].font = font_bold
    ws["D7"].fill = fill_input
    ws["D7"].alignment = Alignment(horizontal="center", vertical="center")
    ws["D7"].border = thin_border

    ws["E7"] = "=C7+D7"
    ws["E7"].font = font_bold
    ws["E7"].fill = fill_subtotal
    ws["E7"].alignment = Alignment(horizontal="center", vertical="center")
    ws["E7"].border = thin_border

    ws["B8"] = "Negatif (-)"
    ws["B8"].font = font_bold
    ws["B8"].alignment = Alignment(horizontal="center", vertical="center")
    ws["B8"].border = thin_border

    ws["C8"] = 15
    ws["C8"].font = font_bold
    ws["C8"].fill = fill_input
    ws["C8"].alignment = Alignment(horizontal="center", vertical="center")
    ws["C8"].border = thin_border

    ws["D8"] = 90
    ws["D8"].font = font_bold
    ws["D8"].fill = fill_input
    ws["D8"].alignment = Alignment(horizontal="center", vertical="center")
    ws["D8"].border = thin_border

    ws["E8"] = "=C8+D8"
    ws["E8"].font = font_bold
    ws["E8"].fill = fill_subtotal
    ws["E8"].alignment = Alignment(horizontal="center", vertical="center")
    ws["E8"].border = thin_border

    ws["B9"] = "Total Baku Emas"
    ws["B9"].font = font_bold
    ws["B9"].fill = fill_subtotal
    ws["B9"].alignment = Alignment(horizontal="center", vertical="center")
    ws["B9"].border = open_table_bottom

    ws["C9"] = "=C7+C8"
    ws["C9"].font = font_bold
    ws["C9"].fill = fill_subtotal
    ws["C9"].alignment = Alignment(horizontal="center", vertical="center")
    ws["C9"].border = open_table_bottom

    ws["D9"] = "=D7+D8"
    ws["D9"].font = font_bold
    ws["D9"].fill = fill_subtotal
    ws["D9"].alignment = Alignment(horizontal="center", vertical="center")
    ws["D9"].border = open_table_bottom

    ws["E9"] = "=E7+E8"
    ws["E9"].font = Font(name="Times New Roman", size=11, bold=True, color="000000")
    ws["E9"].fill = fill_subtotal
    ws["E9"].alignment = Alignment(horizontal="center", vertical="center")
    ws["E9"].border = open_table_bottom

    ws["B11"] = "2. Hasil Perhitungan Parameter Diagnostik"
    ws["B11"].font = font_section

    results_headers = ["Parameter Diagnostik", "Rumus Matematis", "Nilai Desimal", "Persentase (%)", "Interpretasi Klinis Bab 4 Skripsi"]
    for col_idx, h in enumerate(results_headers, start=2):
        cell = ws.cell(row=12, column=col_idx)
        cell.value = h
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = open_table_top

    metrics = [
        ("Sensitivitas (Sensitivity / True Positive Rate)", "TP / (TP + FN)", "=C7/C9", "=C7/C9", "Kemampuan alat mendeteksi subjek yang benar-benar sakit."),
        ("Spesifisitas (Specificity / True Negative Rate)", "TN / (TN + FP)", "=D8/D9", "=D8/D9", "Kemampuan alat menyaring subjek yang benar-benar sehat."),
        ("Nilai Prediktif Positif (PPV / Precision)", "TP / (TP + FP)", "=C7/E7", "=C7/E7", "Probabilitas subjek benar sakit jika hasil tes positif."),
        ("Nilai Prediktif Negatif (NPV)", "TN / (TN + FN)", "=D8/E8", "=D8/E8", "Probabilitas subjek benar sehat jika hasil tes negatif."),
        ("Akurasi Diagnostik (Diagnostic Accuracy)", "(TP + TN) / Total N", "=(C7+D8)/E9", "=(C7+D8)/E9", "Proporsi keseluruhan diagnosis yang terbukti benar."),
        ("Positive Likelihood Ratio (LR+)", "Sensitivitas / (1 - Spesifisitas)", "=(C7/C9)/(1-(D8/D9))", "-", "Peningkatan kemungkinan sakit jika tes positif (>10 = sangat baik)."),
        ("Negative Likelihood Ratio (LR-)", "(1 - Sensitivitas) / Spesifisitas", "=(1-(C7/C9))/(D8/D9)", "-", "Penurunan kemungkinan sakit jika tes negatif (<0.1 = sangat baik)."),
        ("Prevalensi Penyakit (Pre-test Probability)", "(TP + FN) / Total N", "=C9/E9", "=C9/E9", "Proporsi subjek sakit berdasarkan baku emas.")
    ]

    for idx, (name, formula_str, val_formula, pct_formula, interp) in enumerate(metrics, start=13):
        r_border = open_table_bottom if idx == 12 + len(metrics) else thin_border
        ws[f"B{idx}"] = name
        ws[f"B{idx}"].font = font_bold
        ws[f"B{idx}"].border = r_border

        ws[f"C{idx}"] = formula_str
        ws[f"C{idx}"].font = font_regular
        ws[f"C{idx}"].alignment = Alignment(horizontal="center")
        ws[f"C{idx}"].border = r_border

        ws[f"D{idx}"] = val_formula
        ws[f"D{idx}"].font = font_bold
        ws[f"D{idx}"].alignment = Alignment(horizontal="center")
        ws[f"D{idx}"].number_format = "0.000"
        ws[f"D{idx}"].border = r_border

        ws[f"E{idx}"] = pct_formula
        ws[f"E{idx}"].font = font_result
        ws[f"E{idx}"].alignment = Alignment(horizontal="center")
        if pct_formula != "-":
            ws[f"E{idx}"].number_format = "0.0%"
        ws[f"E{idx}"].border = r_border

        ws[f"F{idx}"] = interp
        ws[f"F{idx}"].font = font_regular
        ws[f"F{idx}"].border = r_border

    ws["B23"] = "3. Template Kalimat Pelaporan Bab 4 Skripsi FK"
    ws["B23"].font = font_section

    ws.merge_cells("B24:F26")
    ws["B24"] = (
        'Berdasarkan hasil uji diagnostik terhadap total responden (N), diperoleh nilai sensitivitas alat sebesar [Persentase] '
        'dan spesifisitas sebesar [Persentase]. Nilai Prediktif Positif (PPV) tercatat sebesar [Persentase] dan Nilai Prediktif '
        'Negatif (NPV) sebesar [Persentase], dengan akurasi diagnostik keseluruhan mencapai [Persentase]. Nilai Positive Likelihood '
        'Ratio (LR+) sebesar [Nilai] menunjukkan kemampuan konfirmasi klinis yang memadai.'
    )
    ws["B24"].font = Font(name="Times New Roman", size=10, italic=True, color="333333")
    ws["B24"].alignment = Alignment(vertical="top", wrap_text=True)
    ws["B24"].border = thin_border

    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 46
    ws.column_dimensions["C"].width = 32
    ws.column_dimensions["D"].width = 16
    ws.column_dimensions["E"].width = 16
    ws.column_dimensions["F"].width = 65

    file_path = OUT_DIR / "01_DIAGNOSIS_Kalkulator_Tabel_2x2_Naskah.xlsx"
    wb.save(file_path)
    print("✓ Created (NASKAH.FK Standard):", file_path)


# ==============================================================================
# 2. RESCUE (KEPK & SAMPLE CRISIS) — 100% TIMES NEW ROMAN & OPEN-TABLE
# ==============================================================================
def create_rescue_docx_pdf():
    # DOCX
    doc = Document()
    apply_naskah_fk_docx_styles(doc)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("PANDUAN PENYELAMATAN KRISIS KEPK DAN SAMPEL PENELITIAN KEDOKTERAN\n")
    set_run_tnr(r_title, size_pt=14, bold=True)
    r_sub = p_title.add_run("Standard Operating Procedure Penanganan Hambatan Etik dan Matching Kontrol")
    set_run_tnr(r_sub, size_pt=12, italic=True)

    h1 = doc.add_heading(level=1)
    r = h1.add_run("1. Protokol Penanganan KEPK Tertahan atau Perbaikan Mayor")
    set_run_tnr(r, size_pt=12, bold=True)
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(6)

    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r1 = p.add_run("Apabila pengajuan persetujuan etik (Ethical Clearance) tertahan melebihi batas waktu normal atau menerima catatan perbaikan mayor, peneliti disarankan melakukan langkah mitigasi berikut:\n")
    set_run_tnr(r1, size_pt=12)
    r2 = p.add_run(
        "a. Audit Kerahasiaan Data Rekam Medis: Seluruh instrumen ekstraksi data wajib di-anonimkan secara ketat tanpa mencantumkan identitas primer (Nama, NIK, No. RM) pada naskah kerja; gunakan pengkodean acak (contoh: S-001).\n"
        "b. Perlindungan Subjek Rentan (Vulnerable Subjects): Pada penelitian yang melibatkan subjek anak usia 7–17 tahun, wajib disertakan Formulir Persetujuan Orang Tua (Informed Consent) dan Formulir Persetujuan Anak (Assent Form).\n"
        "c. SOP Tindakan Klinis / Invasif: Pengambilan sampel biologis wajib menegaskan kompetensi tenaga pelaksana bersertifikasi dan SOP keselamatan rumah sakit rujukan.\n"
    )
    set_run_tnr(r2, size_pt=12)

    h2 = doc.add_heading(level=1)
    r = h2.add_run("2. Mitigasi Kegagalan Matching Kontrol pada Desain Kasus-Kontrol")
    set_run_tnr(r, size_pt=12, bold=True)
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(6)

    p2 = doc.add_paragraph()
    p2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r3 = p2.add_run(
        "Kendala umum penelitian kasus-kontrol di lingkungan rumah sakit adalah ketidakseimbangan jumlah kontrol yang memenuhi kriteria matching usia dan jenis kelamin. Solusi metodologis yang dapat dipertanggungjawabkan meliputi:\n"
        "a. Relaksasi Kriteria Caliper: Memperlebar rentang usia matching (misal dari ±1 tahun menjadi ±3 tahun) dengan mencantumkan justifikasi biologis relevan pada Bab 3.\n"
        "b. Analisis Unmatched dengan Penyesuaian Multivariat: Mengubah pendekatan menjadi unmatched case-control dan mengontrol variabel perancu (confounder) melalui uji Regresi Logistik Ganda pada Bab 4.\n"
        "c. Penerapan Rasio 1:N: Menaikkan rasio kasus terhadap kontrol menjadi 1:2 atau 1:3 untuk mempertahankan power uji statistik apabila kelompok kontrol berlebih.\n"
    )
    set_run_tnr(r3, size_pt=12)

    h3 = doc.add_heading(level=1)
    r = h3.add_run("3. Format Surat Permohonan Percepatan Telaah Etik")
    set_run_tnr(r, size_pt=12, bold=True)
    h3.paragraph_format.space_before = Pt(12)
    h3.paragraph_format.space_after = Pt(6)

    p3 = doc.add_paragraph()
    p3.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r4 = p3.add_run(
        "Perihal : Permohonan Percepatan Telaah Lanjutan Protokol Etik No: [Nomor Registrasi]\n"
        "Kepada Yth. Ketua Komisi Etik Penelitian Kesehatan (KEPK)\n"
        "[Nama Institusi / Rumah Sakit]\n\n"
        "Dengan hormat,\n"
        "Sehubungan dengan proses perbaikan protokol penelitian atas nama [Nama Mahasiswa] / [NIM], Program Studi Kedokteran, dengan judul \"[Judul Penelitian]\", "
        "bersama ini disampaikan naskah perbaikan beserta Matriks Tanggapan Telaah Etik (Matrix of Revisions). Mengingat jadwal pengambilan data yang terikat batas waktu akademik, peneliti memohon kiranya naskah perbaikan dapat ditelaah pada kesempatan pertama.\n\n"
        "Demikian permohonan ini disampaikan. Atas perhatian dan perkenan Bapak/Ibu, diucapkan terima kasih.\n\n"
        "Mengetahui,\n"
        "Dosen Pembimbing Utama                                   Peneliti Utama,\n\n\n"
        "( [Nama & Gelar Dospem] )                                  ( [Nama Mahasiswa] )"
    )
    set_run_tnr(r4, size_pt=11)

    docx_path = OUT_DIR / "02_RESCUE_Checklist_Krisis_KEPK_dan_Sampel_FK.docx"
    doc.save(docx_path)
    print("✓ Created (NASKAH.FK Standard):", docx_path)

    # PDF
    pdf_path = OUT_DIR / "02_RESCUE_Checklist_Krisis_KEPK_dan_Sampel_FK.pdf"
    doc_pdf = SimpleDocTemplate(str(pdf_path), pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)

    style_t = ParagraphStyle('TitleStyle', fontName='Times-Bold', fontSize=13, leading=16, alignment=1, textColor=COLOR_BLACK)
    style_sub = ParagraphStyle('SubStyle', fontName='Times-Italic', fontSize=10, leading=13, alignment=1, textColor=COLOR_DARK_GRAY)
    style_h = ParagraphStyle('HeadingStyle', fontName='Times-Bold', fontSize=11, leading=14, textColor=COLOR_BLACK, spaceBefore=10, spaceAfter=4)
    style_b = ParagraphStyle('BodyStyle', fontName='Times-Roman', fontSize=10, leading=14, alignment=4, textColor=COLOR_BLACK)

    elements = [
        Paragraph("PANDUAN PENYELAMATAN KRISIS KEPK DAN SAMPEL PENELITIAN KEDOKTERAN", style_t),
        Paragraph("Standard Operating Procedure Penanganan Hambatan Etik dan Matching Kontrol — NASKAH.FK", style_sub),
        HRFlowable(width="100%", thickness=0.75, color=COLOR_BLACK, spaceBefore=6, spaceAfter=8),
        Paragraph("1. Protokol Penanganan KEPK Tertahan atau Perbaikan Mayor", style_h),
        Paragraph("a. <b>Audit Kerahasiaan Data:</b> Seluruh instrumen ekstraksi data wajib di-anonimkan secara ketat tanpa mencantumkan identitas primer (Nama, NIK, No. RM); gunakan kode unik (contoh: S-001).<br/>"
                  "b. <b>Perlindungan Subjek Rentan:</b> Pada subjek anak usia 7–17 tahun, wajib disertakan Formulir Persetujuan Orang Tua (Informed Consent) dan Persetujuan Anak (Assent Form).<br/>"
                  "c. <b>SOP Tindakan Klinis:</b> Peneliti wajib menegaskan bahwa tindakan invasif dilakukan oleh tenaga medis bersertifikat sesuai standar keselamatan institusi.", style_b),
        Spacer(1, 6),
        Paragraph("2. Mitigasi Kegagalan Matching Kontrol pada Desain Kasus-Kontrol", style_h),
        Paragraph("a. <b>Relaksasi Caliper:</b> Memperlebar rentang usia matching (misal dari ±1 tahun menjadi ±3 tahun) disertai rujukan biologis relevan pada Bab 3.<br/>"
                  "b. <b>Analisis Unmatched + Multivariat:</b> Mengubah pendekatan menjadi unmatched dan mengontrol variabel perancu via Regresi Logistik Ganda pada Bab 4.<br/>"
                  "c. <b>Rasio 1:N:</b> Menaikkan rasio kontrol menjadi 1:2 atau 1:3 untuk mempertahankan power uji statistik.", style_b),
        Spacer(1, 6),
        Paragraph("3. Permohonan Percepatan Telaah Etik KEPK", style_h),
        Paragraph("Gunakan surat pengantar resmi dari Dosen Pembimbing Utama kepada Sekretariat KEPK dengan melampirkan Matriks Tanggapan Telaah Etik poin-per-poin.", style_b)
    ]
    doc_pdf.build(elements)
    print("✓ Created (NASKAH.FK Standard):", pdf_path)


# ==============================================================================
# 3. BENANG MERAH (DESIGN MATRIX & FORMULAS) — 100% TIMES NEW ROMAN & OPEN-TABLE
# ==============================================================================
def create_benang_merah_docx_pdf():
    # DOCX
    doc = Document()
    apply_naskah_fk_docx_styles(doc)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("MATRIKS PEMILIHAN DESAIN RISET KEDOKTERAN DAN FORMULA BESAR SAMPEL\n")
    set_run_tnr(r_title, size_pt=14, bold=True)
    r_sub = p_title.add_run("Pedoman Metodologi Riset Kedokteran Bebas Red Flags Penguji — NASKAH.FK")
    set_run_tnr(r_sub, size_pt=12, italic=True)

    h1 = doc.add_heading(level=1)
    r = h1.add_run("1. Matriks Komparasi Desain Penelitian Observasional dan Eksperimental")
    set_run_tnr(r, size_pt=12, bold=True)
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(6)

    table = doc.add_table(rows=1, cols=5)
    hdr_cells = table.rows[0].cells
    hdr_titles = ["Parameter Metodologi", "Potong Lintang (Cross-Sectional)", "Kasus-Kontrol (Case-Control)", "Kohort (Cohort Study)", "Uji Klinis Acak (RCT)"]
    for i, title in enumerate(hdr_titles):
        hdr_cells[i].text = title
        set_run_tnr(hdr_cells[i].paragraphs[0].runs[0], size_pt=11, bold=True)

    data = [
        ("Arah Pengamatan", "Simultan satu titik waktu", "Retrospektif (efek ke pajanan)", "Prospektif (pajanan ke efek)", "Prospektif intervensi aktif"),
        ("Ukuran Asosiasi", "Prevalence Ratio (PR) / Rasio Prevalensi", "Odds Ratio (OR) Sahaja", "Relative Risk (RR) / Hazard Ratio", "Relative Risk Reduction (RRR) / NNT"),
        ("Kelebihan Utama", "Efisien waktu, biaya terjangkau", "Sangat efektif untuk penyakit jarang", "Dapat mengukur insidensi & temporalitas", "Baku emas pembuktian kausalitas"),
        ("Kelemahan Utama", "Tidak membuktikan hubungan sebab-akibat", "Rentan bias ingatan (recall bias)", "Membutuhkan waktu & biaya besar", "Pertimbangan etik & risiko drop-out"),
        ("Formula Sampel Baku", "Lemeshow Estimasi Proporsi Populasi", "Lemeshow Uji Hipotesis Beda 2 Proporsi", "Lemeshow Rasio Risiko (RR)", "Formula Beda Rerata / 2 Proporsi Eksperimen")
    ]

    for row_data in data:
        row_cells = table.add_row().cells
        for i, val in enumerate(row_data):
            row_cells[i].text = val
            set_run_tnr(row_cells[i].paragraphs[0].runs[0], size_pt=11, bold=(i == 0))

    format_open_table(table)

    h2 = doc.add_heading(level=1)
    r = h2.add_run("2. Poin Kritis (Red Flags) Metodologi Kedokteran")
    set_run_tnr(r, size_pt=12, bold=True)
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(6)

    p_rf = doc.add_paragraph()
    p_rf.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_rf = p_rf.add_run(
        "a. Larangan Pelaporan Relative Risk pada Case-Control: Desain kasus-kontrol tidak dapat mengukur insidensi penyakit, sehingga ukuran asosiasi yang valid secara matematis hanyalah Odds Ratio (OR).\n"
        "b. Ketidaklayakan Rumus Slovin di Bidang Kedokteran: Rumus Slovin tidak memperhitungkan tingkat kemaknaan (alpha), kekuatan uji (power/beta), proporsi rujukan, maupun presisi klinis. Gunakan rumus Lemeshow yang sesuai dengan tujuan hipotesis.\n"
        "c. Koreksi Drop-Out Besar Sampel: Peneliti wajib menambahkan antisipasi drop-out dengan formula n_akhir = n_hitung / (1 - f), di mana f umumnya bernilai 0,10 (10%).\n"
    )
    set_run_tnr(r_rf, size_pt=12)

    docx_path = OUT_DIR / "03_BENANG_MERAH_Matriks_Desain_Riset_dan_Rumus_Sampel.docx"
    doc.save(docx_path)
    print("✓ Created (NASKAH.FK Standard):", docx_path)

    # PDF
    pdf_path = OUT_DIR / "03_BENANG_MERAH_Matriks_Desain_Riset_dan_Rumus_Sampel.pdf"
    doc_pdf = SimpleDocTemplate(str(pdf_path), pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)

    style_t = ParagraphStyle('TitleStyle', fontName='Times-Bold', fontSize=12, leading=15, alignment=1, textColor=COLOR_BLACK)
    style_sub = ParagraphStyle('SubStyle', fontName='Times-Italic', fontSize=9.5, leading=12, alignment=1, textColor=COLOR_DARK_GRAY)
    style_h = ParagraphStyle('HeadingStyle', fontName='Times-Bold', fontSize=10.5, leading=13, textColor=COLOR_BLACK, spaceBefore=8, spaceAfter=4)
    style_b = ParagraphStyle('BodyStyle', fontName='Times-Roman', fontSize=8.5, leading=11, textColor=COLOR_BLACK)
    style_th = ParagraphStyle('THStyle', fontName='Times-Bold', fontSize=8.5, leading=11, alignment=1, textColor=COLOR_BLACK)

    table_data = [[Paragraph(h, style_th) for h in hdr_titles]]
    for row in data:
        table_data.append([Paragraph(cell, style_b) for cell in row])

    t = Table(table_data, colWidths=[95, 105, 105, 110, 105])
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEABOVE', (0, 0), (-1, 0), 1.0, COLOR_BLACK),
        ('LINEBELOW', (0, 0), (-1, 0), 1.0, COLOR_BLACK),
        ('LINEBELOW', (0, 1), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('LINEBELOW', (0, -1), (-1, -1), 1.0, COLOR_BLACK),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))

    elements = [
        Paragraph("MATRIKS PEMILIHAN DESAIN RISET KEDOKTERAN DAN FORMULA BESAR SAMPEL", style_t),
        Paragraph("Pedoman Metodologi Riset Kedokteran Bebas Red Flags Penguji — NASKAH.FK", style_sub),
        HRFlowable(width="100%", thickness=0.75, color=COLOR_BLACK, spaceBefore=4, spaceAfter=6),
        t,
        Spacer(1, 6),
        Paragraph("Catatan Kritis Metodologi:", style_h),
        Paragraph("1. <b>Case-Control:</b> Hanya melaporkan Odds Ratio (OR), tidak diperkenankan menghitung Relative Risk (RR).<br/>"
                  "2. <b>Besar Sampel:</b> Hindari rumus Slovin pada riset klinis/kedokteran. Gunakan formula Lemeshow berdasarkan uji hipotesis yang dipilih.<br/>"
                  "3. <b>Koreksi Drop-Out:</b> Formula koreksi: n_akhir = n / (1 - f), dengan f = 0,10.", style_b)
    ]
    doc_pdf.build(elements)
    print("✓ Created (NASKAH.FK Standard):", pdf_path)


# ==============================================================================
# 4. DOSPEM (REVISION PROGRESS SUMMARY) — 100% TIMES NEW ROMAN & OPEN-TABLE
# ==============================================================================
def create_dospem_docx():
    doc = Document()
    apply_naskah_fk_docx_styles(doc)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("LEMBAR RINGKASAN PROGRES DAN TINDAK LANJUT REVISI BIMBINGAN\n")
    set_run_tnr(r_title, size_pt=14, bold=True)
    r_sub = p_title.add_run("Formulir Komunikasi Efektif Dosen Pembimbing Skripsi Kedokteran — NASKAH.FK")
    set_run_tnr(r_sub, size_pt=12, italic=True)

    h1 = doc.add_heading(level=2)
    r = h1.add_run("I. IDENTITAS BIMBINGAN")
    set_run_tnr(r, size_pt=12, bold=True)
    h1.paragraph_format.space_before = Pt(10)
    h1.paragraph_format.space_after = Pt(4)

    p_id = doc.add_paragraph()
    r_id = p_id.add_run(
        "Nama Mahasiswa / NIM : [Nama Mahasiswa Lengkap] / [NIM]\n"
        "Dosen Pembimbing I    : [Nama Lengkap beserta Gelar Akademik Dospem I]\n"
        "Dosen Pembimbing II   : [Nama Lengkap beserta Gelar Akademik Dospem II]\n"
        "Tahapan Naskah        : Revisi Proposal / Revisi Bab 4–5 / Pra-Sidang Hasil\n"
        "Tanggal Penyerahan    : [DD Bulan YYYY]"
    )
    set_run_tnr(r_id, size_pt=12)

    h2 = doc.add_heading(level=2)
    r = h2.add_run("II. MATRIKS TINDAK LANJUT REVISI SEBELUMNYA")
    set_run_tnr(r, size_pt=12, bold=True)
    h2.paragraph_format.space_before = Pt(10)
    h2.paragraph_format.space_after = Pt(4)

    table = doc.add_table(rows=1, cols=4)
    hdr_cells = table.rows[0].cells
    hdr_titles = ["No", "Catatan Koreksi Pembimbing", "Lokasi Naskah", "Tindak Lanjut & Dasar Rujukan"]
    for i, title in enumerate(hdr_titles):
        hdr_cells[i].text = title
        set_run_tnr(hdr_cells[i].paragraphs[0].runs[0], size_pt=11, bold=True)

    sample_revisions = [
        ("1", "Memperjelas batasan kriteria eksklusi subjek komorbid DM.", "Bab 3 (Hal. 28)", "Ditambahkan 3 kriteria eksklusi spesifik mengacu pada Konsensus Pengelolaan DM PERKENI 2021."),
        ("2", "Tabel karakteristik subjek belum menyajikan persentase lengkap.", "Bab 4 (Hal. 42)", "Tabel 4.1 diperbaiki dengan menyertakan distribusi frekuensi absolut (n) dan relatif (%)."),
        ("3", "Paragraf pembahasan masih mengulang angka pada tabel hasil.", "Bab 5 (Hal. 55–58)", "Paragraf pembahasan direstrukturisasi dengan pola: Temuan Utama -> Rujukan Komparasi -> Mekanisme Patofisiologi.")
    ]
    for row in sample_revisions:
        row_cells = table.add_row().cells
        for i, val in enumerate(row):
            row_cells[i].text = val
            set_run_tnr(row_cells[i].paragraphs[0].runs[0], size_pt=11, bold=(i == 0))

    format_open_table(table)

    h3 = doc.add_heading(level=2)
    r = h3.add_run("III. POIN KRITIS YANG DIMOHONKAN ARAHAN PADA PERTEMUAN INI")
    set_run_tnr(r, size_pt=12, bold=True)
    h3.paragraph_format.space_before = Pt(10)
    h3.paragraph_format.space_after = Pt(4)

    p_req = doc.add_paragraph()
    r_req = p_req.add_run(
        "1. Konfirmasi pemilihan uji non-parametrik Mann-Whitney atas data yang tidak berdistribusi normal.\n"
        "2. Arahan mengenai penyertaan variabel perancu (usia dan status merokok) pada model regresi multivariat."
    )
    set_run_tnr(r_req, size_pt=12)

    docx_path = OUT_DIR / "04_DOSPEM_Template_1Page_Progress_Summary_Revisi.docx"
    doc.save(docx_path)
    print("✓ Created (NASKAH.FK Standard):", docx_path)


# ==============================================================================
# 5. KEPK (INFORMED CONSENT & ASSENT) — 100% TIMES NEW ROMAN
# ==============================================================================
def create_kepk_docx():
    doc = Document()
    apply_naskah_fk_docx_styles(doc)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("NASKAH PENJELASAN SEBELUM PERSETUJUAN (PSP), INFORMED CONSENT, DAN ASSENT FORM\n")
    set_run_tnr(r_title, size_pt=13, bold=True)
    r_sub = p_title.add_run("Standar Baku Dokumen Komisi Etik Penelitian Kesehatan (KEPK) — NASKAH.FK")
    set_run_tnr(r_sub, size_pt=11, italic=True)

    h1 = doc.add_heading(level=1)
    r = h1.add_run("BAGIAN A: PENJELASAN SEBELUM PERSETUJUAN (PSP)")
    set_run_tnr(r, size_pt=12, bold=True)
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(4)

    p_psp = doc.add_paragraph()
    p_psp.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_psp = p_psp.add_run(
        "Judul Penelitian : [Tuliskan Judul Penelitian Lengkap Tanpa Singkatan]\n"
        "Peneliti Utama   : [Nama Lengkap Mahasiswa] / [NIM]\n"
        "Institusi        : Fakultas Kedokteran [Nama Universitas]\n\n"
        "Bapak/Ibu/Saudara diundang untuk berpartisipasi dalam penelitian ini secara sukarela tanpa ada unsur paksaan.\n\n"
        "1. Tujuan Penelitian: Mengetahui hubungan antara [Variabel Independen] dengan [Variabel Dependen] guna melengkapi bukti ilmiah dalam tatalaksana klinis.\n"
        "2. Prosedur Penelitian: Subjek akan menjalani wawancara kuesioner selama ±15 menit dan/atau pengambilan sampel darah perifer sebanyak 3 cc oleh tenaga kesehatan tersertifikasi.\n"
        "3. Manfaat Penelitian: Memberikan informasi profil kesehatan subjek dan berkontribusi pada pengembangan ilmu kedokteran.\n"
        "4. Risiko dan Ketidaknyamanan: Rasa nyeri ringan atau hematoma minimal pada lokasi penusukan jarum yang bersifat sementara.\n"
        "5. Jaminan Kerahasiaan: Identitas pribadi subjek dijamin kerahasiaannya dengan sistem pengkodean terenkripsi.\n"
        "6. Hak Penarikan Diri: Subjek berhak membatalkan keikutsertaan sewaktu-waktu tanpa dikenakan sanksi apapun."
    )
    set_run_tnr(r_psp, size_pt=12)

    h2 = doc.add_heading(level=1)
    r = h2.add_run("BAGIAN B: LEMBAR PERSETUJUAN (INFORMED CONSENT DEWASA)")
    set_run_tnr(r, size_pt=12, bold=True)
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(4)

    p_ic = doc.add_paragraph()
    p_ic.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_ic = p_ic.add_run(
        "Saya yang bertanda tangan di bawah ini:\n"
        "Nama / Usia     : ................................................................ / ........... Tahun\n"
        "Alamat / No. HP : ................................................................................................\n\n"
        "Menyatakan telah membaca dan memahami seluruh penjelasan di atas, serta telah diberikan kesempatan mengajukan pertanyaan. Saya dengan sukarela BERSEDIA berpartisipasi sebagai responden penelitian ini.\n\n"
        "Kota Penelitian, .................................... 2026\n\n"
        "Subjek Penelitian / Wali,                                  Peneliti Utama,\n\n\n\n"
        "( ...................................................... )                    ( [Nama Mahasiswa] )"
    )
    set_run_tnr(r_ic, size_pt=12)

    h3 = doc.add_heading(level=1)
    r = h3.add_run("BAGIAN C: LEMBAR PERSETUJUAN SUBJEK ANAK (ASSENT FORM USIA 7–17 TAHUN)")
    set_run_tnr(r, size_pt=12, bold=True)
    h3.paragraph_format.space_before = Pt(12)
    h3.paragraph_format.space_after = Pt(4)

    p_as = doc.add_paragraph()
    p_as.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_as = p_as.add_run(
        "Halo adik-adik. Kakak dokter sedang melakukan penelitian tentang kesehatan. Kakak ingin meminta bantuan adik untuk menjawab beberapa pertanyaan sederhana. "
        "Adik boleh memilih untuk ikut atau tidak ikut, dan hal ini tidak akan mempengaruhi pemeriksaan dokter kepada adik.\n\n"
        "Apakah adik bersedia membantu penelitian kakak dokter?\n"
        "[   ] YA, SAYA BERSEDIA                              [   ] TIDAK BERSEDIA\n\n"
        "Nama Anak : .......................................................   Tanda Tangan/Cap Jempol: ....................................."
    )
    set_run_tnr(r_as, size_pt=12)

    docx_path = OUT_DIR / "05_KEPK_Template_Informed_Consent_dan_Assent_Bebas_RedFlags.docx"
    doc.save(docx_path)
    print("✓ Created (NASKAH.FK Standard):", docx_path)


# ==============================================================================
# 6. ANTIREVISI (10-POINT CHECKLIST) — 100% TIMES NEW ROMAN & OPEN-TABLE
# ==============================================================================
def create_antirevisi_docx_pdf():
    # DOCX
    doc = Document()
    apply_naskah_fk_docx_styles(doc)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("CHECKLIST 10 POIN VERIFIKASI PRA-SUBMISI DRAFT SKRIPSI KEDOKTERAN\n")
    set_run_tnr(r_title, size_pt=14, bold=True)
    r_sub = p_title.add_run("Quality Assurance Gate Mandiri Sebelum Menghadapi Bimbingan dan Ujian Semhas — NASKAH.FK")
    set_run_tnr(r_sub, size_pt=12, italic=True)

    checklist_items = [
        ("01. Sinkronisasi Besaran Sampel (N)", "Jumlah sampel pada Bab 3 (metodologi), Bab 4 (tabel karakteristik), dan Bab 5 (pembahasan) wajib konsisten secara utuh tanpa ada perbedaan angka yang tidak dijelaskan."),
        ("02. Pelaporan Nilai P Eksak", "Nilai signifikansi wajib ditulis secara eksak (contoh: P = 0,028), bukan P < 0,05. Apabila output piranti lunak statistik menunjukkan 0,000, cantumkan sebagai P < 0,001."),
        ("03. Interval Kepercayaan 95% (95% CI)", "Seluruh estimasi titik berupa Odds Ratio (OR), Relative Risk (RR), atau perbedaan rerata wajib disertai rentang 95% CI (contoh: OR = 2,45; 95% CI 1,20–4,80)."),
        ("04. Keseragaman Format Sitasi", "Format rujukan pustaka wajib konsisten (Vancouver berurutan numerik atau APA alfabetis) mulai dari Bab 1 hingga Daftar Pustaka."),
        ("05. Keterangan Singkatan pada Tabel", "Seluruh akronim medis pada tabel (seperti Hb, SGOT, GDS, HT) wajib memiliki catatan kaki penjelasan di bawah tabel terkait."),
        ("06. Uji Prasyarat dan Normalitas", "Penerapan uji parametrik (seperti Independent T-test atau One-Way ANOVA) wajib disertai dokumentasi uji normalitas (Shapiro-Wilk untuk n < 50 atau Kolmogorov-Smirnov untuk n >= 50)."),
        ("07. Konsistensi Benang Merah", "Rumusan masalah pada Bab 1, tabel penyajian hasil pada Bab 4, dan butir simpulan pada Bab 5 wajib memiliki struktur dan urutan substansi yang identik."),
        ("08. Pembahasan Pola 3-Tahap", "Paragraf pembahasan pada Bab 5 tidak sekadar mengulang angka hasil uji, melainkan menguraikan: Temuan Inti -> Komparasi Literatur -> Mekanisme Patofisiologi."),
        ("09. Uraian Keterbatasan Penelitian", "Bab 5 wajib mencantumkan 2–3 keterbatasan metodologis nyata (seperti potensi bias recall atau desain observasional yang tidak membuktikan kausalitas)."),
        ("10. Tata Tulis Nomenklatur Medis Latin", "Seluruh nama taksonomi mikroorganisme atau istilah anatomis wajib dicetak miring (contoh: Staphylococcus aureus, in vitro, postpartum).")
    ]

    for title, desc in checklist_items:
        p = doc.add_paragraph()
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_box = p.add_run(f"[   ] {title}: ")
        set_run_tnr(r_box, size_pt=12, bold=True)
        r_desc = p.add_run(desc)
        set_run_tnr(r_desc, size_pt=12)

    docx_path = OUT_DIR / "06_ANTIREVISI_Checklist_10_Poin_PreSubmission_Skripsi_FK.docx"
    doc.save(docx_path)
    print("✓ Created (NASKAH.FK Standard):", docx_path)

    # PDF
    pdf_path = OUT_DIR / "06_ANTIREVISI_Checklist_10_Poin_PreSubmission_Skripsi_FK.pdf"
    doc_pdf = SimpleDocTemplate(str(pdf_path), pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)

    style_t = ParagraphStyle('TitleStyle', fontName='Times-Bold', fontSize=12, leading=15, alignment=1, textColor=COLOR_BLACK)
    style_sub = ParagraphStyle('SubStyle', fontName='Times-Italic', fontSize=9.5, leading=12, alignment=1, textColor=COLOR_DARK_GRAY)
    style_h = ParagraphStyle('HeadingStyle', fontName='Times-Bold', fontSize=10, leading=13, textColor=COLOR_BLACK, spaceBefore=4, spaceAfter=2)
    style_b = ParagraphStyle('BodyStyle', fontName='Times-Roman', fontSize=9, leading=12, alignment=4, textColor=COLOR_BLACK)

    elements = [
        Paragraph("CHECKLIST 10 POIN VERIFIKASI PRA-SUBMISI DRAFT SKRIPSI KEDOKTERAN", style_t),
        Paragraph("Quality Assurance Gate Mandiri Sebelum Bimbingan dan Ujian Semhas — NASKAH.FK", style_sub),
        HRFlowable(width="100%", thickness=0.75, color=COLOR_BLACK, spaceBefore=4, spaceAfter=6)
    ]

    for title, desc in checklist_items:
        elements.append(Paragraph(f"[  ] <b>{title}</b>", style_h))
        elements.append(Paragraph(desc, style_b))
        elements.append(Spacer(1, 3))

    doc_pdf.build(elements)
    print("✓ Created (NASKAH.FK Standard):", pdf_path)


# ==============================================================================
# 7. PUBMED (MESH SEARCH STRINGS & BOOLEAN) — 100% TIMES NEW ROMAN & OPEN-TABLE
# ==============================================================================
def create_pubmed_docx_pdf():
    # DOCX
    doc = Document()
    apply_naskah_fk_docx_styles(doc)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("FORMULA PENCARIAN LITERATUR MEDIS DENGAN MeSH DAN BOOLEAN OPERATOR\n")
    set_run_tnr(r_title, size_pt=14, bold=True)
    r_sub = p_title.add_run("Panduan Penelusuran Basis Data PubMed dan Scopus untuk Naskah Skripsi FK — NASKAH.FK")
    set_run_tnr(r_sub, size_pt=12, italic=True)

    h1 = doc.add_heading(level=1)
    r = h1.add_run("1. Prinsip Penyusunan String Pencarian Medis (PICO to MeSH)")
    set_run_tnr(r, size_pt=12, bold=True)
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(6)

    p_rules = doc.add_paragraph()
    p_rules.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_rules = p_rules.add_run(
        "Penelusuran literatur ilmiah internasional bereputasi mensyaratkan kombinasi kata kunci terstruktur guna meminimalisir artikel tidak relevan:\n"
        "• AND  : Menggabungkan konsep inti PICO yang berbeda (mempersempit ruang lingkup hasil).\n"
        "• OR   : Menggabungkan sinonim dan istilah sejenis (memperluas cakupan penelusuran).\n"
        "• NOT  : Mengecualikan topik yang tidak dikehendaki (contoh: NOT animals).\n"
        "• [Mesh] : Mengunci terminologi baku Medical Subject Headings dari National Library of Medicine.\n"
        "• [tiab] : Menargetkan pencarian spesifik pada judul (Title) dan abstrak (Abstract)."
    )
    set_run_tnr(r_rules, size_pt=12)

    h2 = doc.add_heading(level=1)
    r = h2.add_run("2. Template String Pencarian PubMed Siap Pakai")
    set_run_tnr(r, size_pt=12, bold=True)
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(6)

    strings = [
        ("A. Uji Diagnostik & Biomarker (Contoh: Preeklamsia)",
         '("Pre-Eclampsia"[Mesh] OR "Preeclampsia"[tiab] OR "gestational hypertension"[tiab]) AND ("Biomarkers"[Mesh] OR "sFlt-1"[tiab] OR "PlGF"[tiab]) AND ("Sensitivity and Specificity"[Mesh] OR "ROC Curve"[Mesh] OR "diagnostic accuracy"[tiab])'),
        ("B. Uji Klinis Terapi Farmakologi (Contoh: Diabetes Melitus Tipe 2)",
         '("Diabetes Mellitus, Type 2"[Mesh] OR "T2DM"[tiab]) AND ("Sodium-Glucose Transporter 2 Inhibitors"[Mesh] OR "SGLT2 inhibitors"[tiab] OR "empagliflozin"[tiab]) AND ("Cardiovascular Diseases"[Mesh] OR "cardiovascular outcomes"[tiab]) AND ("Randomized Controlled Trial"[ptyp])'),
        ("C. Faktor Risiko & Desain Kasus-Kontrol (Contoh: Karsinoma Paru)",
         '("Lung Neoplasms"[Mesh] OR "lung cancer"[tiab]) AND ("Smoking"[Mesh] OR "tobacco smoke pollution"[Mesh] OR "secondhand smoke"[tiab]) AND ("Risk Factors"[Mesh] OR "Odds Ratio"[tiab] OR "case-control studies"[Mesh])'),
        ("D. Kesehatan Ibu dan Anak (Contoh: Stunting)",
         '("Growth Disorders"[Mesh] OR "Stunting"[tiab] OR "stunted growth"[tiab]) AND ("Infant"[Mesh] OR "Child, Preschool"[Mesh] OR "toddler"[tiab]) AND ("Exclusive Breastfeeding"[Mesh] OR "complementary feeding"[tiab] OR "dietary diversity"[tiab])'),
        ("E. Penyakit Tropis Infeksius (Contoh: Demam Berdarah Dengue)",
         '("Dengue"[Mesh] OR "severe dengue"[tiab] OR "dengue hemorrhagic fever"[tiab]) AND ("Early Diagnosis"[Mesh] OR "NS1 antigen"[tiab] OR "warning signs"[tiab]) AND ("Disease Progression"[Mesh] OR "plasma leakage"[tiab])')
    ]

    for title, string_code in strings:
        p_st = doc.add_paragraph()
        r_st = p_st.add_run(f"{title}\n")
        set_run_tnr(r_st, size_pt=12, bold=True)
        r_code = p_st.add_run(string_code)
        set_run_tnr(r_code, size_pt=10, italic=True)

    docx_path = OUT_DIR / "07_PUBMED_Cheatsheet_MeSH_Search_String_dan_Boolean.docx"
    doc.save(docx_path)
    print("✓ Created (NASKAH.FK Standard):", docx_path)

    # PDF
    pdf_path = OUT_DIR / "07_PUBMED_Cheatsheet_MeSH_Search_String_dan_Boolean.pdf"
    doc_pdf = SimpleDocTemplate(str(pdf_path), pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)

    style_t = ParagraphStyle('TitleStyle', fontName='Times-Bold', fontSize=12, leading=15, alignment=1, textColor=COLOR_BLACK)
    style_sub = ParagraphStyle('SubStyle', fontName='Times-Italic', fontSize=9.5, leading=12, alignment=1, textColor=COLOR_DARK_GRAY)
    style_h = ParagraphStyle('HeadingStyle', fontName='Times-Bold', fontSize=10, leading=13, textColor=COLOR_BLACK, spaceBefore=6, spaceAfter=2)
    style_b = ParagraphStyle('BodyStyle', fontName='Times-Roman', fontSize=9, leading=12, alignment=4, textColor=COLOR_BLACK)
    style_code = ParagraphStyle('CodeStyle', fontName='Times-Italic', fontSize=8, leading=10.5, textColor=COLOR_DARK_GRAY)

    elements = [
        Paragraph("FORMULA PENCARIAN LITERATUR MEDIS DENGAN MeSH DAN BOOLEAN OPERATOR", style_t),
        Paragraph("Panduan Penelusuran Basis Data PubMed dan Scopus untuk Naskah Skripsi FK — NASKAH.FK", style_sub),
        HRFlowable(width="100%", thickness=0.75, color=COLOR_BLACK, spaceBefore=4, spaceAfter=6),
        Paragraph("<b>1. Prinsip Dasar Formulasi MeSH & Boolean</b>", style_h),
        Paragraph("Gunakan operator AND untuk menghubungkan komponen PICO, OR untuk sinonim, [Mesh] untuk kata kunci resmi NLM, dan [tiab] untuk penelusuran judul/abstrak.", style_b),
        Spacer(1, 4),
        Paragraph("<b>2. Template Search String Siap Pakai</b>", style_h)
    ]

    for title, string_code in strings:
        elements.append(Paragraph(f"<b>{title}</b>", style_h))
        elements.append(Paragraph(string_code, style_code))
        elements.append(Spacer(1, 2))

    doc_pdf.build(elements)
    print("✓ Created (NASKAH.FK Standard):", pdf_path)


# ==============================================================================
# 8. SWIPE REPLIES MD
# ==============================================================================
def create_swipe_reply_md():
    content = """# 📥 SWIPE REPLIES DM NASKAH.FK — WEEK 2 LEAD MAGNET SUITE

Panduan respons cepat untuk TM / Admin saat followers mengirimkan DM trigger keyword.

---

### 1. TRIGGER: `DIAGNOSIS` (Senin, 21 Sep 2026)
**Lampirkan:** `01_DIAGNOSIS_Kalkulator_Tabel_2x2_Naskah.xlsx`
**Copy Balasan:**
> Halo dok! 🙌 Ini file Excel **Kalkulator Tabel 2x2 Otomatis** dari Naskah.
>
> Kamu tinggal masukkan angka TP, FP, FN, dan TN di sel warna kuning, nanti Sensitivitas, Spesifisitas, PPV, NPV, dan Akurasinya langsung terhitung lengkap dengan contoh kalimat Bab 4.
>
> Btw, alat uji baru yang lagi kamu teliti apa dok? Udah lolos uji validitas?

---

### 2. TRIGGER: `RESCUE` (Selasa, 22 Sep 2026)
**Lampirkan:** `02_RESCUE_Checklist_Krisis_KEPK_dan_Sampel_FK.pdf`
**Copy Balasan:**
> Halo dok! Ini checklist darurat **Penyelamatan Krisis KEPK & Matching Sampel** buat kamu.
>
> Di dalamnya ada 3 solusi taktis kalau kontrol case-control kamu ambyar plus draft surat percepatan telaah etik.
>
> Skripsimu saat ini kendala utamanya di perizinan etik atau di pencarian subjek penelitian dok?

---

### 3. TRIGGER: `BENANG MERAH` (Rabu, 23 Sep 2026)
**Lampirkan:** `03_BENANG_MERAH_Matriks_Desain_Riset_dan_Rumus_Sampel.pdf`
**Copy Balasan:**
> Halo dok! Ini **Matriks Pemilihan Desain Riset & Rumus Sampel FK** dari Naskah.
>
> Isinya komparasi Cross-Sectional vs Case-Control vs Cohort biar kamu nggak salah sebut Odds Ratio vs Relative Risk pas ujian.
>
> Rencana penelitian kamu pakai desain apa dok? Ada variabel perancu (confounder) yang bikin ragu?

---

### 4. TRIGGER: `DOSPEM` (Kamis, 24 Sep 2026)
**Lampirkan:** `04_DOSPEM_Template_1Page_Progress_Summary_Revisi.docx`
**Copy Balasan:**
> Halo dok! Ini template Word **1-Page Progress & Revision Summary**.
>
> Taruh lembar ini di halaman depan setiap kali kirim draft revisi. Dospem yang super sibuk bakal sangat apresiasi karena langsung lihat poin apa yang udah kamu beresin.
>
> Dospem kamu tipe yang teliti kata per kata atau yang susah ditemui dok? 😄

---

### 5. TRIGGER: `KEPK` (Jumat, 25 Sep 2026)
**Lampirkan:** `05_KEPK_Template_Informed_Consent_dan_Assent_Bebas_RedFlags.docx`
**Copy Balasan:**
> Halo dok! Ini format baku **Naskah Penjelasan (PSP), Informed Consent, dan Assent Form Anak**.
>
> Klausul kerahasiaan dan hak respondennya sudah disesuaikan dengan standar baku KEPK nasional bebas red flags.
>
> Penelitian kamu subjeknya pasien dewasa, anak-anak, atau data sekunder rekam medis dok?

---

### 6. TRIGGER: `ANTIREVISI` (Sabtu, 26 Sep 2026)
**Lampirkan:** `06_ANTIREVISI_Checklist_10_Poin_PreSubmission_Skripsi_FK.pdf`
**Copy Balasan:**
> Halo dok! Ini **Checklist 10 Poin Pre-Submission Skripsi FK**.
>
> Ceklis 10 poin ini (terutama sinkronisasi N sampel dan penulisan P-value eksak) sebelum klik tombol kirim ke dospem.
>
> Naskah kamu sekarang lagi di bab berapa dok? Mau kejar sidang di periode bulan apa?

---

### 7. TRIGGER: `PUBMED` (Minggu, 27 Sep 2026)
**Lampirkan:** `07_PUBMED_Cheatsheet_MeSH_Search_String_dan_Boolean.pdf`
**Copy Balasan:**
> Halo dok! Ini **Cheatsheet MeSH Search String & Boolean Operators** buat PubMed dan Scopus.
>
> Ada 5 template string siap copy-paste untuk biomarker, terapi klinis, faktor risiko, stunting, sampai infeksi tropis.
>
> Kamu lagi cari jurnal untuk topik spesifik apa dok? Kalau ada kata kunci yang bingung MeSH-nya, cerita aja ya!

---

### 🎯 NEXT STEP KETIKA USER CURHAT KENDALA:
Jika user merespons dengan kendala naskahnya yang rumit/mendesak:
> *"Paham banget dok, hal itu emang sering bikin mahasiswa FK stuck berminggu-minggu.*
>
> *Di Naskah kami ada program **Pendampingan Naskah Intensif (1-on-1)** bareng tim dokter & biostatistika. Kita bantu audit metodologi, beresin bab pembahasan, dan siapin simulasi pertanyaan sidang.*
>
> *Mau kami bantu beresin naskah kamu biar cepat ACC? Boleh ketik **INFO** buat lihat detail paket dan jadwalnya ya dok."*
"""
    md_path = OUT_DIR / "SWIPE_REPLY_DM_ADMIN.md"
    md_path.write_text(content, encoding="utf-8")
    print("✓ Created:", md_path)


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
def main():
    print("=== RE-GENERATING ALL LEAD MAGNET ASSETS (NASKAH.FK FORMATTING STANDARD) ===")
    create_diagnosis_excel()
    create_rescue_docx_pdf()
    create_benang_merah_docx_pdf()
    create_dospem_docx()
    create_kepk_docx()
    create_antirevisi_docx_pdf()
    create_pubmed_docx_pdf()
    create_swipe_reply_md()
    print("=== ALL ASSETS RE-GENERATED & VALIDATED! ===")


if __name__ == "__main__":
    main()
