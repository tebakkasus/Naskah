import os, random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

font_dir = 'C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/fonts'
output_dir = 'C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/naskah-visuals'
os.makedirs(output_dir, exist_ok=True)

def f(weight, size):
    fname = f"Montserrat-{weight}.ttf"
    path = os.path.join(font_dir, fname)
    return ImageFont.truetype(path, size)

def add_glow_or_burst(draw, center, radius, color):
    # Simple burst lines
    cx, cy = center
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        x1 = cx + int((radius - 8) * math.cos(rad))
        y1 = cy + int((radius - 8) * math.sin(rad))
        x2 = cx + int((radius + 12) * math.cos(rad))
        y2 = cy + int((radius + 12) * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill=color, width=3)

# ==============================================================================
# MASTER DESIGN 1: "HIGH-CONTRAST ACADEMIC HOOK" (Cover Slide)
# Deep Emerald Green (#063B2B) + Electric Canary Yellow (#FFEA00 / #FFE600) + Clean White
# Style: Bold hook, speech bubble callout, 3D accents, real research prompt.
# ==============================================================================
def render_naskah_bold_cover():
    W, H = 1080, 1350
    # Deep Rich Emerald Canvas #063A2A
    img = Image.new("RGB", (W, H), color="#052E21")
    draw = ImageDraw.Draw(img)

    # Background subtle topographic / grid contour
    for y in range(0, H, 100):
        draw.line([(0, y), (W, y)], fill="#083B2C", width=1)
    for x in range(0, W, 100):
        draw.line([(x, 0), (x, H)], fill="#083B2C", width=1)

    # Top Brand Header
    # Custom Brand Icon: N⁺ (like Au⁺, but Naskah: N⁺)
    draw.rounded_rectangle([70, 70, 150, 140], radius=16, fill="#0F4C3A", outline="#1EE08A", width=2)
    draw.text((85, 80), "N", font=f("ExtraBold", 44), fill="#FFFFFF")
    draw.text((120, 75), "+", font=f("Bold", 30), fill="#FFE600")

    # Brand Text
    draw.text((170, 82), "NASKAH", font=f("ExtraBold", 26), fill="#FFFFFF")
    draw.text((170, 114), "ACADEMIC OPERATING SYSTEM", font=f("SemiBold", 15), fill="#7CDDB0")

    # Slide Counter Pill
    draw.rounded_rectangle([880, 80, 1010, 130], radius=25, fill="#0F4C3A", outline="#1EE08A", width=1)
    draw.text((915, 93), "1 / 6", font=f("Bold", 20), fill="#FFE600")

    # Hero Eyebrow Pill Badge
    draw.rounded_rectangle([70, 220, 390, 275], radius=25, fill="#FFE600")
    draw.text((105, 236), "METODOLOGI SKRIPSI", font=f("ExtraBold", 18), fill="#052E21")

    # Massive Bold Hook Headline
    draw.text((70, 315), "Siapa Bilang", font=f("Medium", 58), fill="#FFFFFF")
    draw.text((70, 390), "Bikin Penelitian", font=f("ExtraBold", 66), fill="#FFE600")
    draw.text((70, 470), "Harus Pusing di SPSS?", font=f("ExtraBold", 58), fill="#FFFFFF")

    # White Speech Bubble Callout (Hero Pop Element)
    bubble_x0, bubble_y0, bubble_x1, bubble_y1 = 70, 580, 1010, 870
    draw.rounded_rectangle([bubble_x0, bubble_y0, bubble_x1, bubble_y1], radius=24, fill="#FFFFFF", outline="#FFE600", width=4)
    
    # Yellow Tag on Speech Bubble
    draw.rounded_rectangle([110, 615, 410, 665], radius=15, fill="#052E21")
    draw.text((135, 628), "KUNCI UTAMANYA ADA DI:", font=f("Bold", 16), fill="#FFE600")

    # Punchline inside bubble
    draw.text((110, 690), "Definisi Operasional & Skala Data!", font=f("ExtraBold", 38), fill="#052E21")
    draw.text((110, 755), "Kalau dari Bab 3 skala variabelmu sudah klop (Nominal / Ordinal / Numerik),\nmilih uji statistik di SPSS cuma butuh waktu kurang dari 5 menit.", font=f("Medium", 23), fill="#374151", spacing=8)

    # 2 Feature Pills at the bottom of the card
    draw.rounded_rectangle([110, 840, 480, 900], radius=12, fill="#E6F9F0", outline="#1EE08A", width=2)
    draw.text((130, 855), "✓ Nggak Ditolak Dosen", font=f("Bold", 20), fill="#052E21")

    draw.rounded_rectangle([510, 840, 920, 900], radius=12, fill="#E6F9F0", outline="#1EE08A", width=2)
    draw.text((530, 855), "✓ Hasil Analisis Valid & Teruji", font=f("Bold", 20), fill="#052E21")

    # Interactive Action Button (Yellow CTA)
    btn_y = 960
    draw.rounded_rectangle([70, btn_y, 1010, btn_y + 110], radius=55, fill="#FFE600")
    draw.text((310, btn_y + 35), "SWIPE UNTUK LIHAT MATRIKS LENGKAP >>", font=f("ExtraBold", 24), fill="#052E21")

    # Bottom Social Anchor Bar
    draw.text((70, 1190), "Naskah  •  Teman Diskusi Akademik Terpercaya", font=f("SemiBold", 22), fill="#E6F9F0")
    draw.text((70, 1230), "Follow, Save & Share biar nggak bingung pas bab 4!", font=f("Regular", 19), fill="#7CDDB0")

    # Domain Badges
    draw.text((750, 1205), "naskah.id", font=f("Bold", 20), fill="#FFE600")
    draw.text((880, 1205), "naskah.fk", font=f("Bold", 20), fill="#1EE08A")

    p = os.path.join(output_dir, "naskah_bold_cover.jpg")
    img.save(p, "JPEG", quality=95)
    return p

# ==============================================================================
# MASTER DESIGN 2: "MODULAR BREAKDOWN & MATRIKS" (Slide Edukasi Isi)
# Karakter: Two-tier split (Top: Real Screen/Graph, Bottom: Color-coded Pill Breakdown)
# ==============================================================================
def render_naskah_bold_matrix():
    W, H = 1080, 1350
    # Top Half: Emerald Green, Bottom Half: Clean White Math Grid
    img = Image.new("RGB", (W, H), color="#F4F8F6")
    draw = ImageDraw.Draw(img)

    # Top Section: Dark Emerald Block
    draw.rectangle([0, 0, W, 430], fill="#052E21")

    # Brand & Title inside Top
    draw.text((70, 60), "N⁺ NASKAH", font=f("ExtraBold", 24), fill="#FFFFFF")
    draw.text((880, 60), "SLIDE 03 / 06", font=f("Bold", 18), fill="#FFE600")

    draw.text((70, 115), "RESEARCH BLUEPRINT #02", font=f("Bold", 18), fill="#1EE08A")
    draw.text((70, 150), "Panduan Cepat Memilih", font=f("Medium", 42), fill="#FFFFFF")
    draw.text((70, 205), "UJI BIVARIAT SKRIPSI", font=f("ExtraBold", 54), fill="#FFE600")

    # Top Mini Pill
    draw.rounded_rectangle([70, 290, 780, 345], radius=25, fill="#0F4C3A", outline="#1EE08A", width=2)
    draw.text((95, 305), "Gunakan diagram ini sebelum buka menu 'Analyze' di SPSS", font=f("SemiBold", 19), fill="#E6F9F0")

    # Bottom Grid Canvas
    for y in range(430, H, 50):
        draw.line([(0, y), (W, y)], fill="#E5EFEA", width=1)
    for x in range(0, W, 50):
        draw.line([(x, 430), (x, H)], fill="#E5EFEA", width=1)

    # 3 High-Contrast Modular Rows (Au-style Table Pills)
    tests = [
        ("KATEGORIK vs KATEGORIK", "Chi-Square Test", "Alternatif: Fisher's Exact Test (bila cell < 5)", "#FFE600", "#052E21"),
        ("1 KATEGORIK (2 Kelp) + 1 NUMERIK", "Independent t-Test", "Alternatif: Mann-Whitney U Test (data tidak normal)", "#1EE08A", "#052E21"),
        ("1 KATEGORIK (>2 Kelp) + 1 NUMERIK", "One-Way ANOVA", "Alternatif: Kruskal-Wallis Test (non-parametrik)", "#052E21", "#FFFFFF")
    ]

    sy = 470
    for category, main_test, alt_test, badge_bg, badge_fg in tests:
        # Outer Card Container
        draw.rounded_rectangle([70, sy, 1010, sy + 205], radius=18, fill="#FFFFFF", outline="#052E21", width=3)
        
        # Category Header Bar inside Card
        draw.rounded_rectangle([90, sy + 20, 520, sy + 65], radius=10, fill="#052E21")
        draw.text((110, sy + 32), category, font=f("ExtraBold", 16), fill="#FFE600")

        # Main Recommended Test (Big Pill)
        draw.rounded_rectangle([90, sy + 80, 480, sy + 140], radius=12, fill=badge_bg, outline="#052E21", width=2)
        draw.text((115, sy + 95), main_test, font=f("ExtraBold", 24), fill=badge_fg)

        # Alternative Pill (Mint / Light Outline)
        draw.rounded_rectangle([90, sy + 150, 950, sy + 190], radius=8, fill="#EBF9F2")
        draw.text((110, sy + 158), f"• {alt_test}", font=f("SemiBold", 18), fill="#052E21")

        sy += 230

    # Bottom Call to Action Footer
    draw.rectangle([0, 1200, W, 1350], fill="#052E21")
    draw.text((70, 1240), "Naskah — Partner Bedah Metodologi & Statistik", font=f("Bold", 22), fill="#FFFFFF")
    draw.text((70, 1280), "Simpan tabel ini & tag rekan satu bimbingan kamu ↗", font=f("Regular", 18), fill="#7CDDB0")

    # Yellow Bookmark Pill
    draw.rounded_rectangle([840, 1235, 1010, 1300], radius=30, fill="#FFE600")
    draw.text((880, 1252), "SAVE 🔖", font=f("ExtraBold", 18), fill="#052E21")

    p = os.path.join(output_dir, "naskah_bold_matrix.jpg")
    img.save(p, "JPEG", quality=95)
    return p

p1 = render_naskah_bold_cover()
p2 = render_naskah_bold_matrix()
print("Rendered Naskah Bold Concepts:")
print("1:", p1)
print("2:", p2)
