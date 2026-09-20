"""
Lead Magnet Asset Generator for Naskah.fk (@naskah.efka)
Generates high-precision, production-grade Lead Magnets for Week 2 triggers:
1. DIAGNOSIS -> 01_DIAGNOSIS_Kalkulator_Tabel_2x2_Naskah.xlsx
2. RESCUE -> 02_RESCUE_Checklist_Krisis_KEPK_dan_Sampel_FK.docx & .pdf
3. BENANG MERAH -> 03_BENANG_MERAH_Matriks_Desain_Riset_dan_Rumus_Sampel.docx & .pdf
4. DOSPEM -> 04_DOSPEM_Template_1Page_Progress_Summary_Revisi.docx
5. KEPK -> 05_KEPK_Template_Informed_Consent_dan_Assent_Bebas_RedFlags.docx
6. ANTIREVISI -> 06_ANTIREVISI_Checklist_10_Poin_PreSubmission_Skripsi_FK.docx & .pdf
7. PUBMED -> 07_PUBMED_Cheatsheet_MeSH_Search_String_dan_Boolean.docx & .pdf
8. SWIPE_REPLY_DM_ADMIN.md (Quick DM swipe file)
"""

import os
import pathlib
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

OUT_DIR = pathlib.Path("D:/tm/06_Content/07_LEAD_MAGNETS")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Brand Colors
HEX_NAVY = "071726"
HEX_ORANGE = "E85929"
HEX_CREAM = "F5F2EB"
HEX_LIGHT_BLUE = "EBF3FA"
HEX_MUTED = "667085"

COLOR_NAVY = colors.HexColor("#071726")
COLOR_ORANGE = colors.HexColor("#E85929")
COLOR_CREAM = colors.HexColor("#F5F2EB")
COLOR_LIGHT_BG = colors.HexColor("#F8F9FA")
COLOR_BORDER = colors.HexColor("#D0D5DD")


# ==============================================================================
# 1. EXCEL CALCULATOR (DIAGNOSIS)
# ==============================================================================
def create_diagnosis_excel():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Kalkulator Tabel 2x2"
    ws.views.sheetView[0].showGridLines = True

    # Styling definitions
    font_title = Font(name="Arial", size=16, bold=True, color="FFFFFF")
    font_sub = Font(name="Arial", size=10, italic=True, color="FFFFFF")
    font_section = Font(name="Arial", size=12, bold=True, color=HEX_NAVY)
    font_header = Font(name="Arial", size=11, bold=True, color="FFFFFF")
    font_bold = Font(name="Arial", size=11, bold=True, color=HEX_NAVY)
    font_regular = Font(name="Arial", size=10, color="1D2939")
    font_formula_name = Font(name="Arial", size=11, bold=True, color=HEX_NAVY)
    font_result = Font(name="Arial", size=12, bold=True, color=HEX_ORANGE)

    fill_navy = PatternFill(start_color=HEX_NAVY, end_color=HEX_NAVY, fill_type="solid")
    fill_orange = PatternFill(start_color=HEX_ORANGE, end_color=HEX_ORANGE, fill_type="solid")
    fill_cream = PatternFill(start_color="FDF4EB", end_color="FDF4EB", fill_type="solid")
    fill_input = PatternFill(start_color="FFF3CD", end_color="FFF3CD", fill_type="solid")  # Light yellow for inputs
    fill_subtotal = PatternFill(start_color=HEX_LIGHT_BLUE, end_color=HEX_LIGHT_BLUE, fill_type="solid")
    fill_result = PatternFill(start_color="EAECF0", end_color="EAECF0", fill_type="solid")

    thin_border_gray = Border(
        left=Side(style="thin", color="D0D5DD"),
        right=Side(style="thin", color="D0D5DD"),
        top=Side(style="thin", color="D0D5DD"),
        bottom=Side(style="thin", color="D0D5DD")
    )
    thick_bottom = Border(
        bottom=Side(style="medium", color=HEX_NAVY),
        left=Side(style="thin", color="D0D5DD"),
        right=Side(style="thin", color="D0D5DD"),
        top=Side(style="thin", color="D0D5DD")
    )

    # Title Banner (Rows 1-2)
    ws.merge_cells("B1:H1")
    ws["B1"] = "KALKULATOR UJI DIAGNOSTIK TABEL 2x2 — NASKAH.FK"
    ws["B1"].font = font_title
    ws["B1"].fill = fill_navy
    ws["B1"].alignment = Alignment(horizontal="center", vertical="center")

    ws.merge_cells("B2:H2")
    ws["B2"] = "Official Academic Companion — Masukkan angka pada sel berwarna KUNING. Hasil terhitung otomatis."
    ws["B2"].font = font_sub
    ws["B2"].fill = fill_navy
    ws["B2"].alignment = Alignment(horizontal="center", vertical="center")

    ws.row_dimensions[1].height = 30
    ws.row_dimensions[2].height = 20

    # Section 1: Input Tabel 2x2
    ws["B4"] = "1. TABEL KONTINGENSI 2x2 (INPUT DATA)"
    ws["B4"].font = font_section

    # Headers for 2x2 Table
    ws.merge_cells("C5:D5")
    ws["C5"] = "BAKU EMAS (GOLD STANDARD)"
    ws["C5"].font = font_header
    ws["C5"].fill = fill_navy
    ws["C5"].alignment = Alignment(horizontal="center", vertical="center")

    ws["B6"] = "ALAT UJI BARU"
    ws["B6"].font = font_header
    ws["B6"].fill = fill_navy
    ws["B6"].alignment = Alignment(horizontal="center", vertical="center")

    ws["C6"] = "Positif (+)"
    ws["C6"].font = font_bold
    ws["C6"].fill = fill_cream
    ws["C6"].alignment = Alignment(horizontal="center", vertical="center")
    ws["C6"].border = thin_border_gray

    ws["D6"] = "Negatif (-)"
    ws["D6"].font = font_bold
    ws["D6"].fill = fill_cream
    ws["D6"].alignment = Alignment(horizontal="center", vertical="center")
    ws["D6"].border = thin_border_gray

    ws["E6"] = "Total Alat Uji"
    ws["E6"].font = font_bold
    ws["E6"].fill = fill_subtotal
    ws["E6"].alignment = Alignment(horizontal="center", vertical="center")
    ws["E6"].border = thin_border_gray

    # Row 1: Alat Baru Positif
    ws["B7"] = "Positif (+)"
    ws["B7"].font = font_bold
    ws["B7"].fill = fill_cream
    ws["B7"].alignment = Alignment(horizontal="center", vertical="center")
    ws["B7"].border = thin_border_gray

    ws["C7"] = 85  # TP Default Example
    ws["C7"].font = font_bold
    ws["C7"].fill = fill_input
    ws["C7"].alignment = Alignment(horizontal="center", vertical="center")
    ws["C7"].border = thin_border_gray

    ws["D7"] = 10  # FP Default Example
    ws["D7"].font = font_bold
    ws["D7"].fill = fill_input
    ws["D7"].alignment = Alignment(horizontal="center", vertical="center")
    ws["D7"].border = thin_border_gray

    ws["E7"] = "=C7+D7"  # Total Test Positive
    ws["E7"].font = font_bold
    ws["E7"].fill = fill_subtotal
    ws["E7"].alignment = Alignment(horizontal="center", vertical="center")
    ws["E7"].border = thin_border_gray

    # Row 2: Alat Baru Negatif
    ws["B8"] = "Negatif (-)"
    ws["B8"].font = font_bold
    ws["B8"].fill = fill_cream
    ws["B8"].alignment = Alignment(horizontal="center", vertical="center")
    ws["B8"].border = thin_border_gray

    ws["C8"] = 15  # FN Default Example
    ws["C8"].font = font_bold
    ws["C8"].fill = fill_input
    ws["C8"].alignment = Alignment(horizontal="center", vertical="center")
    ws["C8"].border = thin_border_gray

    ws["D8"] = 90  # TN Default Example
    ws["D8"].font = font_bold
    ws["D8"].fill = fill_input
    ws["D8"].alignment = Alignment(horizontal="center", vertical="center")
    ws["D8"].border = thin_border_gray

    ws["E8"] = "=C8+D8"  # Total Test Negative
    ws["E8"].font = font_bold
    ws["E8"].fill = fill_subtotal
    ws["E8"].alignment = Alignment(horizontal="center", vertical="center")
    ws["E8"].border = thin_border_gray

    # Row 3: Total Gold Standard
    ws["B9"] = "Total Baku Emas"
    ws["B9"].font = font_bold
    ws["B9"].fill = fill_subtotal
    ws["B9"].alignment = Alignment(horizontal="center", vertical="center")
    ws["B9"].border = thick_bottom

    ws["C9"] = "=C7+C8"  # Total Sick
    ws["C9"].font = font_bold
    ws["C9"].fill = fill_subtotal
    ws["C9"].alignment = Alignment(horizontal="center", vertical="center")
    ws["C9"].border = thick_bottom

    ws["D9"] = "=D7+D8"  # Total Healthy
    ws["D9"].font = font_bold
    ws["D9"].fill = fill_subtotal
    ws["D9"].alignment = Alignment(horizontal="center", vertical="center")
    ws["D9"].border = thick_bottom

    ws["E9"] = "=E7+E8"  # Grand Total N
    ws["E9"].font = Font(name="Arial", size=11, bold=True, color=HEX_ORANGE)
    ws["E9"].fill = fill_subtotal
    ws["E9"].alignment = Alignment(horizontal="center", vertical="center")
    ws["E9"].border = thick_bottom

    # Section 2: Hasil Parameter Uji Diagnostik
    ws["B11"] = "2. HASIL PERHITUNGAN PARAMETER DIAGNOSTIK"
    ws["B11"].font = font_section

    results_headers = ["Parameter Diagnostik", "Rumus Matematis", "Nilai Desimal", "Persentase (%)", "Interpretasi Klinis untuk Naskah Skripsi"]
    for col_idx, h in enumerate(results_headers, start=2):
        cell = ws.cell(row=12, column=col_idx)
        cell.value = h
        cell.font = font_header
        cell.fill = fill_navy
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border_gray

    metrics = [
        ("Sensitivitas (Sensitivity / True Positive Rate)", "TP / (TP + FN)", "=C7/C9", "=C7/C9", "Kemampuan alat mendeteksi subjek yang benar-benar sakit."),
        ("Spesifisitas (Specificity / True Negative Rate)", "TN / (TN + FP)", "=D8/D9", "=D8/D9", "Kemampuan alat menyaring subjek yang benar-benar sehat."),
        ("Nilai Prediktif Positif (PPV / Precision)", "TP / (TP + FP)", "=C7/E7", "=C7/E7", "Probabilitas subjek benar sakit jika hasil tes positif."),
        ("Nilai Prediktif Negatif (NPV)", "TN / (TN + FN)", "=D8/E8", "=D8/E8", "Probabilitas subjek benar sehat jika hasil tes negatif."),
        ("Akurasi Diagnostik (Accuracy)", "(TP + TN) / Total N", "=(C7+D8)/E9", "=(C7+D8)/E9", "Proporsi keseluruhan diagnosis yang benar."),
        ("Positive Likelihood Ratio (LR+)", "Sensitivitas / (1 - Spesifisitas)", "=(C7/C9)/(1-(D8/D9))", "-", "Rasio peningkatan kemungkinan sakit jika tes positif (>10 = sangat kuat)."),
        ("Negative Likelihood Ratio (LR-)", "(1 - Sensitivitas) / Spesifisitas", "=(1-(C7/C9))/(D8/D9)", "-", "Rasio penurunan kemungkinan sakit jika tes negatif (<0.1 = sangat kuat)."),
        ("Prevalensi Penyakit (Pre-test Probability)", "(TP + FN) / Total N", "=C9/E9", "=C9/E9", "Proporsi populasi sakit berdasarkan baku emas.")
    ]

    for idx, (name, formula_str, val_formula, pct_formula, interp) in enumerate(metrics, start=13):
        ws[f"B{idx}"] = name
        ws[f"B{idx}"].font = font_formula_name
        ws[f"B{idx}"].border = thin_border_gray

        ws[f"C{idx}"] = formula_str
        ws[f"C{idx}"].font = font_regular
        ws[f"C{idx}"].alignment = Alignment(horizontal="center")
        ws[f"C{idx}"].border = thin_border_gray

        ws[f"D{idx}"] = val_formula
        ws[f"D{idx}"].font = font_bold
        ws[f"D{idx}"].alignment = Alignment(horizontal="center")
        ws[f"D{idx}"].number_format = "0.000"
        ws[f"D{idx}"].border = thin_border_gray

        ws[f"E{idx}"] = pct_formula
        ws[f"E{idx}"].font = font_result
        ws[f"E{idx}"].alignment = Alignment(horizontal="center")
        if pct_formula != "-":
            ws[f"E{idx}"].number_format = "0.0%"
        ws[f"E{idx}"].border = thin_border_gray

        ws[f"F{idx}"] = interp
        ws[f"F{idx}"].font = font_regular
        ws[f"F{idx}"].border = thin_border_gray

    # Section 3: Cara Copy-Paste ke Bab 4 Skripsi FK
    ws["B23"] = "3. TEMPLATE KALIMAT PELAPORAN BAB 4 SKRIPSI FK (SIAP COPY)"
    ws["B23"].font = font_section

    ws.merge_cells("B24:F26")
    template_text = (
        'Berdasarkan hasil uji diagnostik terhadap total responden (N), diperoleh nilai sensitivitas alat sebesar [Persentase] '
        'dan spesifisitas sebesar [Persentase]. Nilai Prediktif Positif (PPV) tercatat sebesar [Persentase] dan Nilai Prediktif '
        'Negatif (NPV) sebesar [Persentase], dengan akurasi diagnostik keseluruhan mencapai [Persentase]. Nilai Positive Likelihood '
        'Ratio (LR+) sebesar [Nilai] menunjukkan kemampuan konfirmasi klinis yang memadai.'
    )
    ws["B24"] = template_text
    ws["B24"].font = Font(name="Arial", size=10, italic=True, color=HEX_NAVY)
    ws["B24"].fill = PatternFill(start_color="F0F4F8", end_color="F0F4F8", fill_type="solid")
    ws["B24"].alignment = Alignment(vertical="top", wrap_text=True)
    ws["B24"].border = thin_border_gray

    # Column Widths
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 44
    ws.column_dimensions["C"].width = 32
    ws.column_dimensions["D"].width = 16
    ws.column_dimensions["E"].width = 16
    ws.column_dimensions["F"].width = 65

    file_path = OUT_DIR / "01_DIAGNOSIS_Kalkulator_Tabel_2x2_Naskah.xlsx"
    wb.save(file_path)
    print("✓ Created:", file_path)


# ==============================================================================
# 2. WORD / PDF HELPER FUNCTIONS
# ==============================================================================
def style_docx_doc(doc):
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)


# ==============================================================================
# 3. RESCUE (KEPK & Sample Crisis)
# ==============================================================================
def create_rescue_docx_pdf():
    # DOCX
    doc = Document()
    style_docx_doc(doc)

    p_head = doc.add_paragraph()
    r_head = p_head.add_run("NASKAH.FK — EMERGENCY RESCUE PROTOCOL\n")
    r_head.bold = True
    r_head.font.size = Pt(10)
    r_head.font.color.rgb = RGBColor(232, 89, 41)

    r_title = p_head.add_run("Checklist Penyelamatan Krisis KEPK & Kriteria Sampel Skripsi FK")
    r_title.bold = True
    r_title.font.size = Pt(16)
    r_title.font.color.rgb = RGBColor(7, 23, 38)

    doc.add_paragraph("Panduan taktis mengatasi penolakan/revisi izin etik KEPK dan kegagalan matching kontrol.")
    doc.add_paragraph("―" * 45)

    doc.add_heading("1. Protokol KEPK Tertahan / Ditolak", level=1)
    p = doc.add_paragraph()
    p.add_run("Jika protokol etik tertahan lebih dari 3 minggu atau menerima perbaikan mayor:\n").bold = True
    p.add_run("• Audit Risiko Kerahasiaan Data: Pastikan seluruh lembar ekstraksi data rekam medis di-anonimkan (hapus Nama, NIK, No RM di draft mentah; gunakan Kode Sampel S-001 dst).\n")
    p.add_run("• Klausa Vulnerable Subjects: Jika melibatkan anak (<18 th), wajib lampirkan Lembar Persetujuan Orang Tua (Informed Consent) DAN Lembar Persetujuan Anak (Assent Form).\n")
    p.add_run("• Form Justifikasi Tindakan Invasif: Cantumkan bahwa prosedur sampling (misal pengambilan darah) dilakukan oleh nakes berwenang dan sesuai SOP rumah sakit jejaring.\n")

    doc.add_heading("2. Penyelamatan Matching Kontrol Ambyar (Case-Control)", level=1)
    p2 = doc.add_paragraph()
    p2.add_run("Kendala: Kasus ada 40, tetapi kontrol yang match usia & jenis kelamin hanya dapat 25.\n").italic = True
    p2.add_run("Solusi 1 — Relaksasi Kriteria Caliper: Perlebar rentang usia matching (misal: dari ±1 tahun menjadi ±3 tahun) dengan justifikasi biologis di Bab 3.\n")
    p2.add_run("Solusi 2 — Unmatched Analysis + Multivariate Adjustment: Ubah protokol menjadi unmatched case-control, lalu masukkan variabel perancu (confounder) ke dalam model Regresi Logistik Ganda di Bab 4.\n")
    p2.add_run("Solusi 3 — Rasio 1:N Alternatif: Jika sulit mencari kontrol 1:1, naikkan rasio kontrol menjadi 1:2 atau 1:3 pada kelompok yang tersedia untuk meningkatkan power uji statistik.\n")

    doc.add_heading("3. Draft Surat Permohonan Percepatan Telaah Etik", level=1)
    p3 = doc.add_paragraph()
    p3.add_run("Perihal: Permohonan Percepatan Telaah Lanjutan Protokol Etik No: [Nomor Registrasi]\n\n"
               "Kepada Yth. Ketua Komisi Etik Penelitian Kesehatan (KEPK)\n"
               "[Nama Fakultas / Rumah Sakit]\n\n"
               "Dengan hormat,\n"
               "Saya yang bertanda tangan di bawah ini:\n"
               "Nama / NIM: [Nama Mahasiswa] / [NIM]\n"
               "Program Studi: Pendidikan Dokter / Profesi Dokter\n"
               "Judul Penelitian: [Judul Lengkap]\n\n"
               "Bersama surat ini mengajukan permohonan percepatan telaah revisi protokol etik. Seluruh catatan perbaikan telaah awal telah disesuaikan pada Dokumen Perbaikan Terlampir (Matrix of Revisions). Data penelitian sangat diperlukan untuk memenuhi jadwal sidang akhir semester berjalan.\n\n"
               "Demikian permohonan ini disampaikan. Atas perhatian dan bantuan Bapak/Ibu, saya ucapkan terima kasih.\n\n"
               "Hormat saya,\n[Tanda Tangan & Nama Mahasiswa]\nMengetahui, Dosen Pembimbing Utama [Nama & Gelar Dospem]")

    docx_path = OUT_DIR / "02_RESCUE_Checklist_Krisis_KEPK_dan_Sampel_FK.docx"
    doc.save(docx_path)
    print("✓ Created:", docx_path)

    # PDF via ReportLab
    pdf_path = OUT_DIR / "02_RESCUE_Checklist_Krisis_KEPK_dan_Sampel_FK.pdf"
    doc_pdf = SimpleDocTemplate(str(pdf_path), pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()

    style_t = ParagraphStyle('TitleStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=15, leading=18, textColor=COLOR_NAVY)
    style_h = ParagraphStyle('HeadingStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=COLOR_ORANGE, spaceBefore=12, spaceAfter=6)
    style_b = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=13, textColor=colors.HexColor("#1D2939"))

    elements = [
        Paragraph("<font color='#E85929'><b>NASKAH.FK — EMERGENCY RESCUE PROTOCOL</b></font>", style_b),
        Spacer(1, 4),
        Paragraph("Checklist Penyelamatan Krisis KEPK & Kriteria Sampel Skripsi FK", style_t),
        HRFlowable(width="100%", thickness=1, color=COLOR_ORANGE, spaceBefore=8, spaceAfter=10),
        Paragraph("<b>1. Protokol KEPK Tertahan / Ditolak</b>", style_h),
        Paragraph("• <b>Audit Kerahasiaan Data:</b> Anonimkan seluruh instrumen (hapus Nama, NIK, No RM; ganti kode S-001).<br/>"
                  "• <b>Subjek Rentan:</b> Pada anak (<18 th), wajib gunakan Informed Consent Orang Tua + Assent Form Anak.<br/>"
                  "• <b>Tindakan Invasif:</b> Tegaskan pengambilan sampel dilakukan tenaga medis bersertifikat sesuai SOP.", style_b),
        Spacer(1, 8),
        Paragraph("<b>2. Penyelamatan Matching Kontrol Ambyar (Case-Control)</b>", style_h),
        Paragraph("• <b>Relaksasi Caliper:</b> Perlebar rentang usia matching (misal ±1 th menjadi ±3 th) dengan rujukan teori.<br/>"
                  "• <b>Unmatched + Regresi Multivariat:</b> Ubah ke unmatched dan kontrol perancu via Regresi Logistik di Bab 4.<br/>"
                  "• <b>Rasio 1:N:</b> Gunakan rasio 1:2 atau 1:3 pada kontrol yang melimpah untuk mempertahankan power statistik.", style_b),
        Spacer(1, 8),
        Paragraph("<b>3. Template Surat Percepatan Telaah Etik KEPK</b>", style_h),
        Paragraph("<i>Gunakan surat resmi pengantar dari Dosen Pembimbing Utama ke Sekretariat KEPK dengan melampirkan tabel matriks respon revisi poin-per-poin (Matrix of Revisions). Hubungi @naskah.fk jika butuh pendampingan audit etik.</i>", style_b)
    ]
    doc_pdf.build(elements)
    print("✓ Created:", pdf_path)


# ==============================================================================
# 4. BENANG MERAH (Design Matrix & Formulas)
# ==============================================================================
def create_benang_merah_docx_pdf():
    # DOCX
    doc = Document()
    style_docx_doc(doc)

    p_head = doc.add_paragraph()
    r_head = p_head.add_run("NASKAH.FK — RESEARCH METHODOLOGY MATRIX\n")
    r_head.bold = True
    r_head.font.size = Pt(10)
    r_head.font.color.rgb = RGBColor(232, 89, 41)

    r_title = p_head.add_run("Matriks Pemilihan Desain Riset Kedokteran & Formula Sampel")
    r_title.bold = True
    r_title.font.size = Pt(16)
    r_title.font.color.rgb = RGBColor(7, 23, 38)

    doc.add_paragraph("Panduan cepat memilih Cross-Sectional vs Case-Control vs Cohort agar tidak dibantai saat Sempro/Semhas.")
    doc.add_paragraph("―" * 45)

    doc.add_heading("1. Matriks Komparasi Desain Penelitian Observasional", level=1)
    
    table = doc.add_table(rows=1, cols=5)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    hdr_titles = ["Parameter", "Cross-Sectional", "Case-Control", "Kohort (Cohort)", "Uji Klinis (RCT)"]
    for i, title in enumerate(hdr_titles):
        hdr_cells[i].text = title
        hdr_cells[i].paragraphs[0].runs[0].font.bold = True

    data = [
        ("Arah Waktu", "Satu titik waktu (simultan)", "Retrospektif (lihat ke belakang)", "Prospektif (follow-up ke depan)", "Prospektif eksperimental"),
        ("Ukuran Asosiasi", "Prevalence Ratio (PR) / OR", "Odds Ratio (OR) Sahaja", "Relative Risk (RR) / Hazard Ratio", "Relative Risk Reduction (RRR) / NNT"),
        ("Kelebihan Utama", "Cepat, murah, cocok skrining", "Sangat efisien untuk penyakit langka", "Bisa ukur insidensi & temporalitas", "Gold standard bukti kausalitas"),
        ("Kelemahan Utama", "Tidak bisa bukti kausalitas (egg/chicken)", "Rentan Recall Bias & Selection Bias", "Lama, mahal, risiko drop out", "Etika ketat, biaya sangat besar"),
        ("Rumus Sampel Utama", "Lemeshow Estimasi Proporsi", "Lemeshow Uji Hipotesis Beda 2 Proporsi", "Lemeshow Relative Risk", "Formula Beda Rerata / Proporsi 2 Kelompok")
    ]

    for row_data in data:
        row_cells = table.add_row().cells
        for i, val in enumerate(row_data):
            row_cells[i].text = val

    doc.add_heading("2. Red Flags Paling Sering Diuji Dosen Penguji FK", level=1)
    doc.add_paragraph("• Red Flag 1: Menghitung Relative Risk (RR) pada penelitian Case-Control (Wajib gunakan Odds Ratio!).")
    doc.add_paragraph("• Red Flag 2: Menggunakan rumus Slovin untuk penelitian uji diagnostik atau uji analitik (Slovin tidak memperhitungkan power uji dan presisi klinis).")
    doc.add_paragraph("• Red Flag 3: Tidak memasukkan estimasi drop-out (biasanya +10% s/d 15%) pada perhitungan besar sampel akhir.")

    docx_path = OUT_DIR / "03_BENANG_MERAH_Matriks_Desain_Riset_dan_Rumus_Sampel.docx"
    doc.save(docx_path)
    print("✓ Created:", docx_path)

    # PDF
    pdf_path = OUT_DIR / "03_BENANG_MERAH_Matriks_Desain_Riset_dan_Rumus_Sampel.pdf"
    doc_pdf = SimpleDocTemplate(str(pdf_path), pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    style_t = ParagraphStyle('TitleStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, leading=17, textColor=COLOR_NAVY)
    style_h = ParagraphStyle('HeadingStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=COLOR_ORANGE, spaceBefore=10, spaceAfter=6)
    style_b = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor("#1D2939"))
    style_th = ParagraphStyle('THStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white)

    table_data = [
        [Paragraph(h, style_th) for h in hdr_titles]
    ]
    for row in data:
        table_data.append([Paragraph(cell, style_b) for cell in row])

    t = Table(table_data, colWidths=[90, 105, 110, 110, 105])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_NAVY),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('BACKGROUND', (0, 1), (-1, 1), COLOR_CREAM),
        ('BACKGROUND', (0, 3), (-1, 3), COLOR_CREAM),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))

    elements = [
        Paragraph("<font color='#E85929'><b>NASKAH.FK — METHODOLOGY MATRIX</b></font>", style_b),
        Paragraph("Matriks Pemilihan Desain Riset Kedokteran & Formula Sampel", style_t),
        HRFlowable(width="100%", thickness=1, color=COLOR_ORANGE, spaceBefore=6, spaceAfter=8),
        t,
        Spacer(1, 8),
        Paragraph("<b>Red Flags Penting:</b>", style_h),
        Paragraph("1. <b>Case-Control:</b> Hanya boleh melaporkan Odds Ratio (OR), dilarang menulis Relative Risk (RR).<br/>"
                  "2. <b>Rumus Sampel:</b> Hindari rumus Slovin di FK. Gunakan Lemeshow dengan memasukkan nilai sensitivitas yang diharapkan atau beda proporsi minimal.<br/>"
                  "3. <b>Koreksi Drop-Out:</b> Tambahkan n_koreksi = n / (1 - f) di mana f = 0.10 (10%).", style_b)
    ]
    doc_pdf.build(elements)
    print("✓ Created:", pdf_path)


# ==============================================================================
# 5. DOSPEM (1-Page Revision Summary Template)
# ==============================================================================
def create_dospem_docx():
    doc = Document()
    style_docx_doc(doc)

    p_head = doc.add_paragraph()
    r_head = p_head.add_run("NASKAH.FK — DOSPEM COMMUNICATION SUITE\n")
    r_head.bold = True
    r_head.font.size = Pt(10)
    r_head.font.color.rgb = RGBColor(232, 89, 41)

    r_title = p_head.add_run("Lembar Ringkasan Progres & Tindak Lanjut Revisi (1-Page Summary)")
    r_title.bold = True
    r_title.font.size = Pt(15)
    r_title.font.color.rgb = RGBColor(7, 23, 38)

    doc.add_paragraph("Lampirkan lembar ini di halaman terdepan setiap kali mengirimkan draft naskah revisi kepada Dosen Pembimbing.")
    doc.add_paragraph("―" * 45)

    doc.add_heading("I. IDENTITAS BIMBINGAN", level=2)
    p_id = doc.add_paragraph()
    p_id.add_run("Nama Mahasiswa / NIM : [Nama Lengkap] / [NIM]\n")
    p_id.add_run("Dosen Pembimbing I    : [Nama & Gelar Dospem Utama]\n")
    p_id.add_run("Dosen Pembimbing II   : [Nama & Gelar Dospem Pendamping]\n")
    p_id.add_run("Tahap Naskah          : Revisi Proposal / Revisi Bab 4-5 / Pra-Sidang\n")
    p_id.add_run("Tanggal Penyerahan    : [DD Bulan YYYY]")

    doc.add_heading("II. MATRIKS TINDAK LANJUT REVISI SEBELUMNYA", level=2)
    table = doc.add_table(rows=1, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    hdr_titles = ["No", "Catatan Dospem Sebelumnya", "Halaman / Bab", "Tindakan Perbaikan & Referensi"]
    for i, title in enumerate(hdr_titles):
        hdr_cells[i].text = title
        hdr_cells[i].paragraphs[0].runs[0].font.bold = True

    sample_revisions = [
        ("1", "Perjelas kriteria eksklusi pasien komorbid DM.", "Bab 3 (Hal. 28)", "Ditambahkan 3 kriteria eksklusi spesifik berdasarkan konsensus PERKENI 2021."),
        ("2", "Tabel karakteristik subjek belum mencantumkan nilai persentase.", "Bab 4 (Hal. 42)", "Tabel 4.1 direvisi dengan menyertakan frekuensi (n) dan persentase (%) lengkap."),
        ("3", "Pembahasan uji bivariat masih mengulang hasil angka tabel.", "Bab 5 (Hal. 55-58)", "Paragraf pembahasan direstrukturisasi menggunakan pola 3-Tier (Temuan -> Komparasi Riset Lain -> Mekanisme Patofisiologi).")
    ]
    for row in sample_revisions:
        row_cells = table.add_row().cells
        for i, val in enumerate(row):
            row_cells[i].text = val

    doc.add_heading("III. POIN KRITIS YANG DIMOHONKAN ARAHAN HARI INI", level=2)
    p_req = doc.add_paragraph()
    p_req.add_run("1. Konfirmasi kelayakan uji normalitas Shapiro-Wilk pada subjek n=45.\n")
    p_req.add_run("2. Rekomendasi apakah analisis multivariat perlu menyertakan variabel usia sebagai confounder.")

    docx_path = OUT_DIR / "04_DOSPEM_Template_1Page_Progress_Summary_Revisi.docx"
    doc.save(docx_path)
    print("✓ Created:", docx_path)


# ==============================================================================
# 6. KEPK (Informed Consent & Assent)
# ==============================================================================
def create_kepk_docx():
    doc = Document()
    style_docx_doc(doc)

    p_head = doc.add_paragraph()
    r_head = p_head.add_run("NASKAH.FK — ETHICAL CLEARANCE SUITE\n")
    r_head.bold = True
    r_head.font.size = Pt(10)
    r_head.font.color.rgb = RGBColor(232, 89, 41)

    r_title = p_head.add_run("Template Baku Naskah Penjelasan (PSP), Informed Consent, dan Assent Form")
    r_title.bold = True
    r_title.font.size = Pt(15)
    r_title.font.color.rgb = RGBColor(7, 23, 38)

    doc.add_paragraph("Template standar KEPK bebas red flags etika penelitian kedokteran.")
    doc.add_paragraph("―" * 45)

    doc.add_heading("BAGIAN A: PENJELASAN SEBELUM PERSETUJUAN (PSP)", level=1)
    p_psp = doc.add_paragraph()
    p_psp.add_run("Judul Penelitian: [Tuliskan Judul Tanpa Singkatan]\n"
                  "Peneliti Utama  : [Nama Mahasiswa]\n"
                  "Institusi       : Fakultas Kedokteran [Nama Universitas]\n\n"
                  "Bapak/Ibu/Saudara diundang untuk berpartisipasi dalam penelitian ini. Partisipasi bersifat SUKARELA tanpa paksaan.\n\n"
                  "1. Tujuan Penelitian: Mengetahui hubungan/pengaruh antara [Variabel X] terhadap [Variabel Y] guna pengembangan terapi/pencegahan klinis.\n"
                  "2. Prosedur: Subjek akan menjalani wawancara kuesioner selama 15 menit dan/atau pengambilan sampel darah sebanyak 3 cc oleh analis kesehatan tersertifikasi.\n"
                  "3. Risiko & Ketidaknyamanan: Kemungkinan memar ringan pada area tusukan jarum yang akan hilang dalam 1-2 hari.\n"
                  "4. Kerahasiaan: Seluruh identitas pribadi (Nama, NIK, No RM) akan dienkripsi dengan nomor kode unik dan tidak akan dipublikasikan secara terbuka.\n"
                  "5. Hak Penarikan Diri: Subjek berhak mengundurkan diri sewaktu-waktu tanpa mempengaruhi hak pelayanan medis rutin di fasilitas kesehatan.")

    doc.add_heading("BAGIAN B: LEMBAR PERSETUJUAN (INFORMED CONSENT DEWASA)", level=1)
    p_ic = doc.add_paragraph()
    p_ic.add_run("Saya yang bertanda tangan di bawah ini:\n"
                 "Nama / Usia: .................................................... / ........... Tahun\n"
                 "Alamat / No HP: .........................................................................\n\n"
                 "Menyatakan bahwa saya telah membaca/dibacakan penjelasan di atas dan memahami sepenuhnya tujuan, manfaat, serta risiko penelitian. Saya secara sukarela BERSEDIA berpartisipasi sebagai responden penelitian ini.\n\n"
                 "Kota, ......................... 2026\n\n"
                 "Yang Memberi Persetujuan,                                 Peneliti Utama,\n\n\n"
                 "( ........................................ )                                 ( ........................................ )")

    doc.add_heading("BAGIAN C: LEMBAR PERSETUJUAN ANAK (ASSENT FORM USIA 7-17 TH)", level=1)
    p_as = doc.add_paragraph()
    p_as.add_run("Halo adik-adik! Kakak dokter sedang membuat penelitian tentang kesehatan adik. "
                 "Kakak ingin bertanya beberapa hal tentang kebiasaan adik sehari-hari. "
                 "Adik boleh memilih untuk ikut atau tidak ikut tanpa perlu takut dimarahi.\n\n"
                 "Apakah adik setuju membantu kakak?\n"
                 "[  ] YA, SAYA SETUJU                      [  ] TIDAK SETUJU\n\n"
                 "Nama Anak: .......................................   Tanda Tangan/Cap Jempol: ....................")

    docx_path = OUT_DIR / "05_KEPK_Template_Informed_Consent_dan_Assent_Bebas_RedFlags.docx"
    doc.save(docx_path)
    print("✓ Created:", docx_path)


# ==============================================================================
# 7. ANTIREVISI (Pre-Submission Checklist)
# ==============================================================================
def create_antirevisi_docx_pdf():
    # DOCX
    doc = Document()
    style_docx_doc(doc)

    p_head = doc.add_paragraph()
    r_head = p_head.add_run("NASKAH.FK — QUALITY ASSURANCE GATE\n")
    r_head.bold = True
    r_head.font.size = Pt(10)
    r_head.font.color.rgb = RGBColor(232, 89, 41)

    r_title = p_head.add_run("Checklist 10 Poin Verifikasi Mandiri Skripsi FK Sebelum Kirim Draft")
    r_title.bold = True
    r_title.font.size = Pt(15)
    r_title.font.color.rgb = RGBColor(7, 23, 38)

    doc.add_paragraph("Lakukan self-audit pada 10 poin kritis ini untuk mencegah pembantaian saat bimbingan dan sidang semhas.")
    doc.add_paragraph("―" * 45)

    checklist_items = [
        ("01. Sinkronisasi Sampel N", "Jumlah sampel di Bab 3 (metodologi), Bab 4 (tabel karakteristik), dan Bab 5 (pembahasan) wajib sama persis tanpa ada drop-out yang tidak terjelaskan."),
        ("02. Format P-Value Eksak", "Tuliskan nilai P secara eksak (contoh: P = 0,028), BUKAN P < 0,05 atau P = 0,000 (jika SPSS menampilkan 0.000, tuliskan P < 0,001)."),
        ("03. Confidence Interval 95%", "Setiap Odds Ratio (OR), Relative Risk (RR), atau beda rerata wajib disertai rentang 95% CI (contoh: OR = 2,45; 95% CI 1,20 - 4,80)."),
        ("04. Konsistensi Gaya Sitasi", "Pastikan gaya sitasi seragam (Vancouver berurutan sesuai nomor kemunculan, atau APA berurutan abjad) dari Bab 1 hingga Daftar Pustaka."),
        ("05. Keterangan Singkatan Tabel", "Semua singkatan medis pada tabel (misal: Hb, SGOT, GDS, HT) wajib diberi catatan kaki keterangan di bawah tabel terkait."),
        ("06. Uji Normalitas & Uji Prasyarat", "Uji parametrik (seperti Independent T-test / ANOVA) wajib disertai bukti uji normalitas (Shapiro-Wilk untuk n<50 atau Kolmogorov-Smirnov untuk n>=50)."),
        ("07. Keterpaduan Benang Merah", "Rumusan masalah di Bab 1, tabel hasil di Bab 4, dan poin kesimpulan di Bab 5 wajib memiliki jumlah dan urutan yang identik."),
        ("08. Pembahasan Pola 3-Tier", "Paragraf Bab 5 tidak boleh sekadar mengulang angka tabel, tetapi wajib menjelaskan: Temuan Utama -> Komparasi Riset Lain -> Mekanisme Biologis/Patofisiologi."),
        ("09. Keterbatasan Penelitian (Study Limitations)", "Bab 5 wajib memuat 2-3 limitasi metodologis riil (misal: potensi recall bias, desain cross-sectional tidak buktikan kausalitas) sebagai tanda kedewasaan akademik."),
        ("10. Bebas Typo Istilah Medis Latin", "Semua nama latin bakteri, virus, atau istilah anatomis wajib dicetak miring (Italic), contoh: *Staphylococcus aureus*, *in vitro*, *post-partum*.")
    ]

    for title, desc in checklist_items:
        p = doc.add_paragraph()
        p.add_run(f"[  ] {title}: ").bold = True
        p.add_run(desc)

    docx_path = OUT_DIR / "06_ANTIREVISI_Checklist_10_Poin_PreSubmission_Skripsi_FK.docx"
    doc.save(docx_path)
    print("✓ Created:", docx_path)

    # PDF
    pdf_path = OUT_DIR / "06_ANTIREVISI_Checklist_10_Poin_PreSubmission_Skripsi_FK.pdf"
    doc_pdf = SimpleDocTemplate(str(pdf_path), pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    style_t = ParagraphStyle('TitleStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, leading=17, textColor=COLOR_NAVY)
    style_h = ParagraphStyle('HeadingStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5, leading=12, textColor=COLOR_ORANGE)
    style_b = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=11.5, textColor=colors.HexColor("#1D2939"))

    elements = [
        Paragraph("<font color='#E85929'><b>NASKAH.FK — QUALITY ASSURANCE</b></font>", style_b),
        Paragraph("Checklist 10 Poin Pre-Submission Skripsi FK", style_t),
        HRFlowable(width="100%", thickness=1, color=COLOR_ORANGE, spaceBefore=6, spaceAfter=8)
    ]

    for title, desc in checklist_items:
        elements.append(Paragraph(f"<b>[  ] {title}</b>", style_h))
        elements.append(Paragraph(desc, style_b))
        elements.append(Spacer(1, 4))

    doc_pdf.build(elements)
    print("✓ Created:", pdf_path)


# ==============================================================================
# 8. PUBMED (MeSH Strings & Boolean Operators)
# ==============================================================================
def create_pubmed_docx_pdf():
    # DOCX
    doc = Document()
    style_docx_doc(doc)

    p_head = doc.add_paragraph()
    r_head = p_head.add_run("NASKAH.FK — LITERATURE SEARCH ENGINE\n")
    r_head.bold = True
    r_head.font.size = Pt(10)
    r_head.font.color.rgb = RGBColor(232, 89, 41)

    r_title = p_head.add_run("Cheatsheet Formula MeSH Search String & Boolean PubMed / Scopus")
    r_title.bold = True
    r_title.font.size = Pt(15)
    r_title.font.color.rgb = RGBColor(7, 23, 38)

    doc.add_paragraph("Kumpulan formula string pencarian literatur internasional bereputasi untuk Bab 2 dan Tinjauan Pustaka.")
    doc.add_paragraph("―" * 45)

    doc.add_heading("1. Anatomi Formula Pencarian Medis (PICO to MeSH)", level=1)
    doc.add_paragraph("Untuk mendapatkan jurnal relevan tanpa tercampur ribuan artikel sampah, susun string menggunakan operator boolean baku:\n"
                      "• AND  : Menggabungkan antar-komponen PICO (mempersempit hasil).\n"
                      "• OR   : Menggabungkan sinonim / kata kunci sejenis (memperluas hasil).\n"
                      "• NOT  : Mengecualikan topik yang tidak diinginkan (misal: NOT animals).\n"
                      "• [Mesh] : Mengunci istilah baku Medical Subject Headings resmi NLM.\n"
                      "• [tiab] : Mencari kata kunci spesifik pada Title dan Abstract.")

    doc.add_heading("2. 5 Template Search String Siap Copy-Paste ke PubMed", level=1)
    
    strings = [
        ("A. Topik Biomarker & Uji Diagnostik (Contoh: Preeklamsia)",
         '("Pre-Eclampsia"[Mesh] OR "Preeclampsia"[tiab] OR "gestational hypertension"[tiab]) AND ("Biomarkers"[Mesh] OR "sFlt-1"[tiab] OR "PlGF"[tiab]) AND ("Sensitivity and Specificity"[Mesh] OR "ROC Curve"[Mesh] OR "diagnostic accuracy"[tiab])'),
        ("B. Topik Farmakoterapi / Uji Klinis (Contoh: Diabetes Melitus Tipe 2)",
         '("Diabetes Mellitus, Type 2"[Mesh] OR "T2DM"[tiab]) AND ("Sodium-Glucose Transporter 2 Inhibitors"[Mesh] OR "SGLT2 inhibitors"[tiab] OR "empagliflozin"[tiab]) AND ("Cardiovascular Diseases"[Mesh] OR "cardiovascular outcomes"[tiab]) AND ("Randomized Controlled Trial"[ptyp])'),
        ("C. Topik Faktor Risiko Penyakit Kronis / Case-Control (Contoh: Kanker Paru)",
         '("Lung Neoplasms"[Mesh] OR "lung cancer"[tiab]) AND ("Smoking"[Mesh] OR "tobacco smoke pollution"[Mesh] OR "secondhand smoke"[tiab]) AND ("Risk Factors"[Mesh] OR "Odds Ratio"[tiab] OR "case-control studies"[Mesh])'),
        ("D. Topik Kesehatan Anak & Nutrisi (Contoh: Stunting)",
         '("Growth Disorders"[Mesh] OR "Stunting"[tiab] OR "stunted growth"[tiab]) AND ("Infant"[Mesh] OR "Child, Preschool"[Mesh] OR "toddler"[tiab]) AND ("Exclusive Breastfeeding"[Mesh] OR "complementary feeding"[tiab] OR "dietary diversity"[tiab])'),
        ("E. Topik Infeksi Tropis & Penyakit Menular (Contoh: Demam Berdarah Dengue)",
         '("Dengue"[Mesh] OR "severe dengue"[tiab] OR "dengue hemorrhagic fever"[tiab]) AND ("Early Diagnosis"[Mesh] OR "NS1 antigen"[tiab] OR "warning signs"[tiab]) AND ("Disease Progression"[Mesh] OR "plasma leakage"[tiab])')
    ]

    for title, string_code in strings:
        p = doc.add_paragraph()
        p.add_run(f"{title}\n").bold = True
        p_code = doc.add_paragraph()
        r_code = p_code.add_run(string_code)
        r_code.font.name = "Consolas"
        r_code.font.size = Pt(9.5)
        r_code.font.color.rgb = RGBColor(7, 23, 38)
        p_code.paragraph_format.left_indent = Inches(0.2)

    doc.add_heading("3. Filter Wajib PubMed untuk Skripsi FK", level=1)
    doc.add_paragraph("Centang filter pada sidebar kiri PubMed:\n"
                      "1. Publication Date: 5 years atau 10 years.\n"
                      "2. Species: Humans.\n"
                      "3. Article Type: Systematic Review, Meta-Analysis, Randomized Controlled Trial, atau Clinical Trial.")

    docx_path = OUT_DIR / "07_PUBMED_Cheatsheet_MeSH_Search_String_dan_Boolean.docx"
    doc.save(docx_path)
    print("✓ Created:", docx_path)

    # PDF
    pdf_path = OUT_DIR / "07_PUBMED_Cheatsheet_MeSH_Search_String_dan_Boolean.pdf"
    doc_pdf = SimpleDocTemplate(str(pdf_path), pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    style_t = ParagraphStyle('TitleStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, leading=17, textColor=COLOR_NAVY)
    style_h = ParagraphStyle('HeadingStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=COLOR_ORANGE, spaceBefore=8, spaceAfter=3)
    style_b = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=11.5, textColor=colors.HexColor("#1D2939"))
    style_code = ParagraphStyle('CodeStyle', parent=styles['Normal'], fontName='Courier', fontSize=7.5, leading=9.5, textColor=COLOR_NAVY)

    elements = [
        Paragraph("<font color='#E85929'><b>NASKAH.FK — LITERATURE SEARCH ENGINE</b></font>", style_b),
        Paragraph("Formula MeSH Search String & Boolean PubMed", style_t),
        HRFlowable(width="100%", thickness=1, color=COLOR_ORANGE, spaceBefore=6, spaceAfter=8)
    ]

    for title, string_code in strings:
        elements.append(Paragraph(f"<b>{title}</b>", style_h))
        elements.append(Paragraph(f"<font color='#071726'>{string_code}</font>", style_code))
        elements.append(Spacer(1, 4))

    elements.append(Paragraph("<b>Filter Rekomendasi PubMed:</b> Humans | 5 Years | Review / RCT / Meta-Analysis", style_b))
    doc_pdf.build(elements)
    print("✓ Created:", pdf_path)


# ==============================================================================
# 9. SWIPE REPLIES MD
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


def main():
    print("=== GENERATING ALL 7 LEAD MAGNET ASSETS FOR WEEK 2 ===")
    create_diagnosis_excel()
    create_rescue_docx_pdf()
    create_benang_merah_docx_pdf()
    create_dospem_docx()
    create_kepk_docx()
    create_antirevisi_docx_pdf()
    create_pubmed_docx_pdf()
    create_swipe_reply_md()
    print("=== ALL LEAD MAGNETS SUCCESSFULLY CREATED & VERIFIED! ===")


if __name__ == "__main__":
    main()
