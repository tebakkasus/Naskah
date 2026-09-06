import os
from PIL import Image, ImageDraw, ImageFont

output_dir = "C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/naskah-visuals"
os.makedirs(output_dir, exist_ok=True)

# Helper function to load Windows system fonts
def get_font(name, size, bold=False):
    fonts_dir = "C:/Windows/Fonts"
    if name == "serif":
        font_file = "georgiab.ttf" if bold else "georgia.ttf"
        if not os.path.exists(os.path.join(fonts_dir, font_file)):
            font_file = "cambriab.ttf" if bold else "cambria.ttc"
    elif name == "sans":
        font_file = "segoeuib.ttf" if bold else "segoeui.ttf"
        if not os.path.exists(os.path.join(fonts_dir, font_file)):
            font_file = "arialbd.ttf" if bold else "arial.ttf"
    elif name == "mono":
        font_file = "consolab.ttf" if bold else "consola.ttf"
    else:
        font_file = "arialbd.ttf" if bold else "arial.ttf"
    
    path = os.path.join(fonts_dir, font_file)
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

# ----------------------------------------------------
# OPTION 1: Modern Academic Minimalist (Navy, Off-White, Emerald, Amber)
# ----------------------------------------------------
def render_option_1():
    W, H = 1080, 1350  # 4:5 Instagram Portrait
    img = Image.new("RGB", (W, H), color="#F8FAFC")
    draw = ImageDraw.Draw(img)

    # Header Bar / Badge
    draw_rounded_rect(draw, [80, 80, 320, 135], radius=28, fill="#0F172A")
    f_badge = get_font("sans", 24, bold=True)
    draw.text((115, 95), "NASKAH. ACADEMIC", font=f_badge, fill="#F8FAFC")

    # Category Tag
    f_cat = get_font("mono", 22, bold=True)
    draw.text((80, 180), "SERIES 02  •  STATISTIK TANPA PUSING", font=f_cat, fill="#0D9488")

    # Main Headline / Hook
    f_title = get_font("serif", 58, bold=True)
    title_lines = [
        "Kapan Harus Pakai",
        "Chi-Square vs t-Test?",
        "(Biar Nggak Ditolak Dosen)"
    ]
    y = 240
    for line in title_lines:
        draw.text((80, y), line, font=f_title, fill="#0F172A")
        y += 75

    # Subtitle / Hook text
    f_sub = get_font("sans", 28, bold=False)
    sub_text = "Banyak yang pakai Chi-Square cuma karena 'katanya paling gampang'.\nPadahal kuncinya ada di jenis skala data variabelmu."
    draw.text((80, y + 20), sub_text, font=f_sub, fill="#475569", spacing=12)

    # Content Card 1 (Chi-Square)
    card1_y = 560
    draw_rounded_rect(draw, [80, card1_y, 1000, card1_y + 240], radius=24, fill="#FFFFFF", outline="#E2E8F0", width=2)
    # Emerald accent bar on left of card
    draw.rounded_rectangle([80, card1_y, 92, card1_y + 240], radius=6, fill="#0D9488")
    
    f_card_h = get_font("sans", 34, bold=True)
    draw.text((120, card1_y + 30), "1. Chi-Square (Uji Beda Kategorik)", font=f_card_h, fill="#0F172A")
    
    f_card_b = get_font("sans", 26, bold=False)
    card1_body = "• Syarat: Variabel Bebas & Terikat sama-sama KATEGORIK (Nominal/Ordinal)\n• Contoh: Hubungan Merokok (Ya/Tidak) dengan Hipertensi (Ya/Tidak)\n• Output: Nilai p-value, Odds Ratio (OR) / Relative Risk (RR)"
    draw.text((120, card1_y + 85), card1_body, font=f_card_b, fill="#334155", spacing=10)

    # Content Card 2 (t-Test)
    card2_y = 830
    draw_rounded_rect(draw, [80, card2_y, 1000, card2_y + 240], radius=24, fill="#FFFFFF", outline="#E2E8F0", width=2)
    # Slate Navy accent bar on left of card
    draw.rounded_rectangle([80, card2_y, 92, card2_y + 240], radius=6, fill="#3B82F6")
    
    draw.text((120, card2_y + 30), "2. Independent t-Test (Uji Beda Rerata)", font=f_card_h, fill="#0F172A")
    
    card2_body = "• Syarat: 1 Variabel Kategorik (2 kelompok) + 1 Variabel NUMERIK\n• Contoh: Beda Rata-rata Skor HbA1c antara Kelompok Diet vs Kontrol\n• Output: Nilai p-value, Mean Difference, 95% Confidence Interval"
    draw.text((120, card2_y + 85), card2_body, font=f_card_b, fill="#334155", spacing=10)

    # Bottom Footer / CTA Bar
    footer_y = 1110
    draw_rounded_rect(draw, [80, footer_y, 1000, footer_y + 140], radius=20, fill="#0F172A")
    
    f_footer_bold = get_font("sans", 28, bold=True)
    f_footer_sub = get_font("sans", 22, bold=False)
    draw.text((120, footer_y + 35), "Save panduan ini untuk bab analisis data kamu ↗", font=f_footer_bold, fill="#F8FAFC")
    draw.text((120, footer_y + 80), "@naskah.id  •  Trusted Academic Companion", font=f_footer_sub, fill="#94A3B8")

    # Watermark / Swipe indicator
    draw_rounded_rect(draw, [870, footer_y + 40, 960, footer_y + 100], radius=15, fill="#0D9488")
    draw.text((895, footer_y + 55), "1 / 7", font=get_font("sans", 22, bold=True), fill="#FFFFFF")

    path = os.path.join(output_dir, "option_1_modern_academic.jpg")
    img.save(path, "JPEG", quality=95)
    return path

# ----------------------------------------------------
# OPTION 2: Nordic Clarity / High-Tech Research (Carbon, Mist White, Electric Indigo, Cyan)
# ----------------------------------------------------
def render_option_2():
    W, H = 1080, 1350
    img = Image.new("RGB", (W, H), color="#F4F4F5")
    draw = ImageDraw.Draw(img)

    # Grid / Tech lines in background (subtle)
    for x in range(80, 1000, 120):
        draw.line([(x, 60), (x, 1290)], fill="#E4E4E7", width=1)

    # Header Container
    draw_rounded_rect(draw, [80, 80, 1000, 160], radius=16, fill="#18181B")
    f_badge = get_font("mono", 24, bold=True)
    draw.text((120, 105), "NASKAH // RESEARCH OPERATING SYSTEM", font=f_badge, fill="#38BDF8")
    draw.text((860, 105), "[ 01 / 06 ]", font=f_badge, fill="#A1A1AA")

    # Category
    f_cat = get_font("sans", 22, bold=True)
    draw.text((80, 200), "FRAMEWORK // METODOLOGI RISET", font=f_cat, fill="#4F46E5")

    # Main Headline
    f_title = get_font("sans", 60, bold=True)
    title_lines = [
        "Checklist 5 Menit",
        "Sebelum Masuk Sempro",
        "Supaya Pertanyaan Dosen Terjawab"
    ]
    y = 250
    for line in title_lines:
        draw.text((80, y), line, font=f_title, fill="#18181B")
        y += 75

    # Checklist Boxes
    items = [
        ("01", "Rumusan Masalah Terukur", "Pastikan ada gap yang jelas antara harapan dan kenyataan empiris."),
        ("02", "Alasan Pemilihan Desain Studi", "Kenapa Cross-Sectional dan bukan Case-Control? Punya dasar literatur."),
        ("03", "Kriteria Inklusi & Eksklusi", "Bukan sekadar 'bersedia jadi responden', tapi spesifik kriteria klinis/sampel."),
        ("04", "Rencana Uji Hipotesis & Software", "Tahu persis uji statistik apa yang akan dijalankan dan batas p-value.")
    ]

    box_y = 520
    f_num = get_font("mono", 28, bold=True)
    f_item_t = get_font("sans", 30, bold=True)
    f_item_d = get_font("sans", 24, bold=False)

    for num, title, desc in items:
        draw_rounded_rect(draw, [80, box_y, 1000, box_y + 120], radius=14, fill="#FFFFFF", outline="#D4D4D8", width=1)
        # Left cyan badge
        draw_rounded_rect(draw, [100, box_y + 25, 170, box_y + 95], radius=10, fill="#EEF2FF")
        draw.text((115, box_y + 42), num, font=f_num, fill="#4F46E5")
        
        draw.text((195, box_y + 25), title, font=f_item_t, fill="#18181B")
        draw.text((195, box_y + 70), desc, font=f_item_d, fill="#71717A")
        box_y += 140

    # Bottom Footer
    footer_y = 1110
    draw_rounded_rect(draw, [80, footer_y, 1000, footer_y + 140], radius=16, fill="#18181B")
    
    f_foot_h = get_font("sans", 28, bold=True)
    f_foot_s = get_font("mono", 22, bold=False)
    draw.text((120, footer_y + 35), "Simpan panduan ini & bagikan ke rekan bimbingan ↗", font=f_foot_h, fill="#FAFAFA")
    draw.text((120, footer_y + 80), "system.naskah.id  •  Precision Academic Tools", font=f_foot_s, fill="#38BDF8")

    path = os.path.join(output_dir, "option_2_nordic_tech.jpg")
    img.save(path, "JPEG", quality=95)
    return path

# ----------------------------------------------------
# OPTION 3: Warm Editorial Companion (Warm Espresso, Oat, Terracotta, Olive)
# ----------------------------------------------------
def render_option_3():
    W, H = 1080, 1350
    img = Image.new("RGB", (W, H), color="#F7F4EE") # Warm paper
    draw = ImageDraw.Draw(img)

    # Top Minimal Header
    f_meta = get_font("sans", 22, bold=True)
    draw.text((80, 80), "NASKAH ESSAY & NOTES", font=f_meta, fill="#C2410C")
    draw.text((870, 80), "EDISI #04", font=f_meta, fill="#78716C")
    draw.line([(80, 120), (1000, 120)], fill="#E7E5E4", width=2)

    # Category Tag
    f_cat = get_font("serif", 24, bold=False)
    draw.text((80, 160), "Catatan Menghadapi Revisi Skripsi", font=f_cat, fill="#57534E")

    # Main Headline
    f_title = get_font("serif", 60, bold=True)
    title_lines = [
        "\"Dosen Bilang Revisinya",
        "Sedikit, Kok Pas Dilihat",
        "Malah Rombak Bab 3?\""
    ]
    y = 220
    for line in title_lines:
        draw.text((80, y), line, font=f_title, fill="#292524")
        y += 75

    # Narrative paragraph / Editorial Quote
    draw_rounded_rect(draw, [80, y + 20, 1000, y + 240], radius=18, fill="#EFECE6", outline="#E7E5E4", width=1)
    
    # Left Terracotta Line
    draw.rounded_rectangle([80, y + 20, 90, y + 240], radius=4, fill="#C2410C")
    
    f_quote = get_font("serif", 28, bold=False)
    quote_text = (
        "\"Seringkali revisi terasa banyak bukan karena penelitianmu buruk,\n"
        "tapi karena kamu belum menyamakan definisi operasional dengan dosen.\n"
        "Begitu fondasi metodologinya klop, revisi berikutnya jauh lebih tenang.\""
    )
    draw.text((120, y + 60), quote_text, font=f_quote, fill="#44403C", spacing=14)

    # 3 Practical Steps Cards
    cards_y = y + 280
    f_step_h = get_font("sans", 28, bold=True)
    f_step_b = get_font("sans", 24, bold=False)

    steps = [
        ("Langkah 1: Jangan Langsung Ketik", "Buat tabel matriks: [Komentar Dosen] vs [Rencana Perbaikan] vs [Referensi]."),
        ("Langkah 2: Klarifikasi Inti Masalah", "Apakah dosen mempermasalahkan sampelnya, atau cuma cara penyampaiannya?"),
        ("Langkah 3: Bawa Opsi, Bukan Cuma Keluhan", "Saat bimbingan berikutnya, tunjukkan 2 pilihan solusi berbasis jurnal.")
    ]

    sy = cards_y
    for title, desc in steps:
        draw_rounded_rect(draw, [80, sy, 1000, sy + 110], radius=14, fill="#FFFFFF", outline="#E7E5E4", width=1)
        draw.text((115, sy + 20), title, font=f_step_h, fill="#292524")
        draw.text((115, sy + 62), desc, font=f_step_b, fill="#78716C")
        sy += 130

    # Bottom Footer
    footer_y = 1130
    draw_rounded_rect(draw, [80, footer_y, 1000, footer_y + 130], radius=18, fill="#292524")
    
    f_foot_t = get_font("serif", 26, bold=False)
    f_foot_s = get_font("sans", 22, bold=False)
    draw.text((120, footer_y + 32), "Pelan-pelan kita bedah satu per satu bareng Naskah.", font=f_foot_t, fill="#F5F5F4")
    draw.text((120, footer_y + 75), "Follow @naskah.id untuk panduan akademik yang manusiawi.", font=f_foot_s, fill="#A8A29E")

    path = os.path.join(output_dir, "option_3_warm_editorial.jpg")
    img.save(path, "JPEG", quality=95)
    return path

p1 = render_option_1()
p2 = render_option_2()
p3 = render_option_3()
print("Generated:")
print("1:", p1)
print("2:", p2)
print("3:", p3)
