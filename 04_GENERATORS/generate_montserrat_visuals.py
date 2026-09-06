import os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

font_dir = 'C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/fonts'
output_dir = 'C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/naskah-visuals'
os.makedirs(output_dir, exist_ok=True)

def f(weight, size):
    fname = f"Montserrat-{weight}.ttf"
    path = os.path.join(font_dir, fname)
    return ImageFont.truetype(path, size)

def add_paper_texture(img, opacity=0.035):
    """Add subtle organic paper grain so it never looks flat or synthetic AI"""
    grain = Image.new("RGBA", img.size, (0,0,0,0))
    gdraw = ImageDraw.Draw(grain)
    w, h = img.size
    for _ in range(int(w * h * 0.08)):
        x = random.randint(0, w-1)
        y = random.randint(0, h-1)
        c = random.randint(0, 255)
        alpha = random.randint(8, 22)
        gdraw.point((x, y), fill=(c, c, c, alpha))
    img.paste(grain, (0,0), grain)
    return img

# ==============================================================================
# CONCEPT 1: "EDITORIAL ACADEMIC" (Clean Off-White + Deep Charcoal + Forest Green Accent)
# Style: Taste-skill inspired, generous organic margins, high typographic hierarchy
# ==============================================================================
def render_concept_1():
    W, H = 1080, 1350
    # Warm off-white #F8F7F4 (Paper background)
    img = Image.new("RGB", (W, H), color="#F7F5F0")
    draw = ImageDraw.Draw(img)

    # Top Brand Bar - Asymmetric left-aligned
    # Eyebrow / Tag
    draw.text((90, 95), "NASKAH", font=f("ExtraBold", 26), fill="#18181B")
    draw.text((220, 97), "•  ACADEMIC COMPANION", font=f("SemiBold", 20), fill="#71717A")
    draw.text((880, 97), "[ 01 / 07 ]", font=f("Medium", 20), fill="#A1A1AA")

    # Subtle horizontal line
    draw.line([(90, 145), (990, 145)], fill="#E4E2DC", width=2)

    # Series Indicator
    draw.text((90, 185), "SERIES // STATISTIK PRAKTIS", font=f("Bold", 20), fill="#2D6A4F")

    # Main Headline - Play with Montserrat weights (Light vs ExtraBold contrast)
    draw.text((90, 235), "Kapan Sebenarnya", font=f("Light", 58), fill="#18181B")
    draw.text((90, 305), "Chi-Square", font=f("ExtraBold", 66), fill="#18181B")
    draw.text((90, 385), "Boleh Digunakan?", font=f("SemiBold", 58), fill="#2D6A4F")

    # Editorial Subheading / Hook Paragraph
    hook_text = (
        "Jangan pakai Chi-Square cuma karena 'katanya paling gampang'.\n"
        "Ada 3 syarat mutlak skala data yang sering luput saat sempro."
    )
    draw.text((90, 480), hook_text, font=f("Regular", 26), fill="#52525B", spacing=12)

    # Visual Element: Clean Asymmetric Card 1 (Syarat 1)
    c1_y = 590
    draw.rounded_rectangle([90, c1_y, 990, c1_y + 175], radius=16, fill="#FFFFFF", outline="#E4E2DC", width=2)
    # Number tag
    draw.text((130, c1_y + 28), "01", font=f("ExtraBold", 32), fill="#2D6A4F")
    draw.text((195, c1_y + 28), "Variabel Bebas & Terikat Harus Kategorik", font=f("Bold", 28), fill="#18181B")
    draw.text((195, c1_y + 75), "Contoh: Status Merokok (Ya/Tidak) vs Hipertensi (Ya/Tidak).\nBukan menguji nilai tekanan darah dalam angka kontinu.", font=f("Regular", 22), fill="#71717A", spacing=6)

    # Card 2 (Syarat 2)
    c2_y = 790
    draw.rounded_rectangle([90, c2_y, 990, c2_y + 175], radius=16, fill="#FFFFFF", outline="#E4E2DC", width=2)
    draw.text((130, c2_y + 28), "02", font=f("ExtraBold", 32), fill="#2D6A4F")
    draw.text((195, c2_y + 28), "Tidak Ada Cell dengan Nilai Harapan < 5", font=f("Bold", 28), fill="#18181B")
    draw.text((195, c2_y + 75), "Jika tabel 2x2 dan ada cell expected count < 5,\nkamu wajib beralih ke Fisher's Exact Test.", font=f("Regular", 22), fill="#71717A", spacing=6)

    # Card 3 (Syarat 3)
    c3_y = 990
    draw.rounded_rectangle([90, c3_y, 990, c3_y + 175], radius=16, fill="#FFFFFF", outline="#E4E2DC", width=2)
    draw.text((130, c3_y + 28), "03", font=f("ExtraBold", 32), fill="#2D6A4F")
    draw.text((195, c3_y + 28), "Sampel Independen (Bukan Berpasangan)", font=f("Bold", 28), fill="#18181B")
    draw.text((195, c3_y + 75), "Untuk data pre-test & post-test pada orang yang sama,\ngunakan Uji McNemar, bukan Chi-Square standar.", font=f("Regular", 22), fill="#71717A", spacing=6)

    # Footer Action Callout
    draw.line([(90, 1205), (990, 1205)], fill="#E4E2DC", width=2)
    draw.text((90, 1235), "Save panduan ini untuk persiapan bab 3 kamu ↗", font=f("SemiBold", 24), fill="#18181B")
    draw.text((750, 1235), "@naskah.id  •  Swipe", font=f("Medium", 22), fill="#71717A")

    img = add_paper_texture(img)
    p = os.path.join(output_dir, "concept_1_editorial_academic.jpg")
    img.save(p, "JPEG", quality=95)
    return p

# ==============================================================================
# CONCEPT 2: "ISMKI INSPIRED - MODERN MEDICAL" (Deep Navy + White Canvas + Emerald Cyan Accent)
# Style: Clean medical association aesthetic, high contrast, authoritative, structured
# ==============================================================================
def render_concept_2():
    W, H = 1080, 1350
    # Clean White with high contrast Navy header block
    img = Image.new("RGB", (W, H), color="#FFFFFF")
    draw = ImageDraw.Draw(img)

    # Solid Deep Navy Top Block (100% human-designed feel, not AI gradient)
    draw.rectangle([0, 0, W, 490], fill="#0A192F") # Deep Midnight Navy

    # Top Navigation / Meta
    draw.text((80, 75), "NASKAH RESEARCH & ACADEMIC", font=f("Bold", 22), fill="#64FFDA")
    draw.text((880, 75), "EDISI #12", font=f("SemiBold", 22), fill="#8892B0")

    # Big Expressive Title inside Navy
    draw.text((80, 135), "CHECKLIST SEBELUM", font=f("Medium", 42), fill="#CCD6F6")
    draw.text((80, 195), "SEMINAR HASIL", font=f("ExtraBold", 68), fill="#FFFFFF")
    draw.text((80, 280), "5 Poin Kritis Yang Paling Sering Diuji Dosen", font=f("SemiBold", 30), fill="#64FFDA")

    # Short Narrative
    sub = "Bukan cuma hasil angka SPSS-nya, tapi bagaimana kamu\nmempertanggungjawabkan interpretasi datanya."
    draw.text((80, 345), sub, font=f("Regular", 22), fill="#8892B0", spacing=8)

    # 4 Structured Action Items (Light grey cards)
    checklist = [
        ("01", "Distribusi Normalitas Data", "Alasan kenapa memilih uji parametrik vs non-parametrik tertera di bab 4."),
        ("02", "P-Value vs Clinical Significance", "Nilai p < 0,05 signifikan secara statistik, tapi apakah bermakna klinis?"),
        ("03", "Pembahasan Gap Hasil vs Teori", "Jika hasil bertolak belakang dengan hipotesis, jelaskan faktor perancunya."),
        ("04", "Keterbatasan Penelitian (Bukan Formalitas)", "Tulis keterbatasan metodologi nyata, bukan sekadar 'waktu terbatas'.")
    ]

    cy = 530
    for num, title, desc in checklist:
        draw.rounded_rectangle([80, cy, 1000, cy + 125], radius=12, fill="#F8FAFC", outline="#E2E8F0", width=2)
        # Navy Badge with Emerald text
        draw.rounded_rectangle([105, cy + 25, 175, cy + 100], radius=8, fill="#0A192F")
        draw.text((120, cy + 42), num, font=f("Bold", 28), fill="#64FFDA")

        draw.text((200, cy + 28), title, font=f("Bold", 26), fill="#0A192F")
        draw.text((200, cy + 70), desc, font=f("Regular", 21), fill="#475569")
        cy += 145

    # Bottom Banner
    draw.rectangle([0, 1190, W, 1350], fill="#0A192F")
    draw.text((80, 1240), "Naskah  •  Teman Diskusi Penelitian Kamu", font=f("SemiBold", 26), fill="#FFFFFF")
    draw.text((80, 1285), "Follow @naskah.id untuk panduan akademik terstruktur", font=f("Regular", 20), fill="#8892B0")
    
    # Pill button
    draw.rounded_rectangle([840, 1235, 990, 1300], radius=30, fill="#64FFDA")
    draw.text((875, 1252), "SIMPAN", font=f("Bold", 20), fill="#0A192F")

    p = os.path.join(output_dir, "concept_2_modern_medical.jpg")
    img.save(p, "JPEG", quality=95)
    return p

# ==============================================================================
# CONCEPT 3: "WARM RELATABLE ESSAY" (Warm Sand + Charcoal + Terracotta Highlight)
# Style: Human, empathetic, thoughtful, study-companion aesthetic
# ==============================================================================
def render_concept_3():
    W, H = 1080, 1350
    # Warm Sand Canvas #F5EFE6
    img = Image.new("RGB", (W, H), color="#F5EFE6")
    draw = ImageDraw.Draw(img)

    # Top Minimal Branding
    draw.text((90, 90), "NASKAH NOTES", font=f("ExtraBold", 24), fill="#9C4121") # Warm Terracotta
    draw.text((870, 90), "#REFLEKSI", font=f("SemiBold", 20), fill="#78716C")
    draw.line([(90, 135), (990, 135)], fill="#E7DEC8", width=2)

    # Narrative Quote / Hook
    draw.text((90, 180), "\"Dosen bilang revisinya sedikit.", font=f("Medium", 46), fill="#292524")
    draw.text((90, 245), "Kok pas dibuka filenya,", font=f("Light", 46), fill="#292524")
    draw.text((90, 310), "Bab 3 di-highlight merah semua?\"", font=f("ExtraBold", 50), fill="#9C4121")

    # Essay Box (Dark Coffee Container)
    box_y = 410
    draw.rounded_rectangle([90, box_y, 990, box_y + 290], radius=18, fill="#292524")
    
    draw.text((135, box_y + 40), "KENAPA INI SERING TERJADI?", font=f("Bold", 22), fill="#E7DEC8")
    
    essay = (
        "Seringkali dosen tidak mempermasalahkan topikmu,\n"
        "tapi mereka melihat ketidaksinkronan antara:\n"
        "• Tujuan Penelitian di Bab 1\n"
        "• Desain Studi & Definisi Operasional di Bab 3\n"
        "• Rencana Uji Statistik yang dipilih.\n\n"
        "Begitu 3 benang merah ini kamu luruskan, revisi berikutnya jauh lebih tenang."
    )
    draw.text((135, box_y + 85), essay, font=f("Regular", 24), fill="#FAF5EF", spacing=10)

    # 3 Actionable Tips (Clean Warm Cards)
    tips = [
        ("1. Jangan Panik & Langsung Revisi", "Buat tabel 3 kolom: [Komentar Dosen] | [Akar Masalah] | [Rencana Solusi]."),
        ("2. Bawa Opsi, Bukan Cuma Tanya", "Saat bimbingan ulang: 'Dok, untuk variabel ini ada 2 opsi uji... mana yang lebih disarankan?'")
    ]

    ty = 735
    for title, desc in tips:
        draw.rounded_rectangle([90, ty, 990, ty + 160], radius=14, fill="#FAF5EF", outline="#E7DEC8", width=2)
        draw.text((130, ty + 30), title, font=f("Bold", 28), fill="#292524")
        draw.text((130, ty + 80), desc, font=f("Regular", 22), fill="#57534E", spacing=6)
        ty += 185

    # Footer
    draw.line([(90, 1170), (990, 1170)], fill="#E7DEC8", width=2)
    draw.text((90, 1215), "Pelan-pelan kita pecahkan bareng Naskah.", font=f("SemiBold", 24), fill="#292524")
    draw.text((90, 1260), "Follow @naskah.id untuk teman diskusi akademik kamu ↗", font=f("Regular", 20), fill="#78716C")

    img = add_paper_texture(img, opacity=0.04)
    p = os.path.join(output_dir, "concept_3_warm_essay.jpg")
    img.save(p, "JPEG", quality=95)
    return p

p1 = render_concept_1()
p2 = render_concept_2()
p3 = render_concept_3()
print("Successfully rendered 3 human-taste Montserrat concepts:")
print("1:", p1)
print("2:", p2)
print("3:", p3)
