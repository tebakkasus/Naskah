import os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

font_dir = 'C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/fonts'
output_dir = 'C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/naskah-visuals'
os.makedirs(output_dir, exist_ok=True)

def f(weight, size):
    fname = f"Montserrat-{weight}.ttf"
    path = os.path.join(font_dir, fname)
    return ImageFont.truetype(path, size)

def draw_shadow(base_img, bbox, radius, blur=24, offset_y=12, shadow_color=(10, 25, 47, 45)):
    """Draw a natural multi-layered soft drop shadow with feathering"""
    shadow_img = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_img)
    x0, y0, x1, y1 = bbox
    sdraw.rounded_rectangle([x0, y0 + offset_y, x1, y1 + offset_y], radius=radius, fill=shadow_color)
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(blur))
    base_img.paste(shadow_img, (0, 0), shadow_img)

def create_textured_white_canvas(W, H):
    # Pure clean white canvas with faint architectural / mathematical grid (opacity controlled)
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grid)
    
    # Grid lines in very faint cool slate-blue (subtle texture)
    for x in range(0, W, 48):
        gdraw.line([(x, 0), (x, H)], fill=(226, 232, 240, 90), width=1)
    for y in range(0, H, 48):
        gdraw.line([(0, y), (W, y)], fill=(226, 232, 240, 90), width=1)
        
    # Add microscopic organic paper grain
    for _ in range(int(W * H * 0.03)):
        gx = random.randint(0, W-1)
        gy = random.randint(0, H-1)
        gc = random.randint(220, 245)
        gdraw.point((gx, gy), fill=(gc, gc, gc, 18))
        
    img.paste(grid, (0, 0), grid)
    return img

# ==============================================================================
# NAVY DIRECTION 1: "NAVY ARCHITECTURAL COVER" (Cover Slide)
# Base: Textured Crisp White
# Dominant: Deep Midnight Navy (#0B192C / #0F233D)
# Secondary: Ice Blue (#E2E8F0) + Soft Warm Amber (#F59E0B) for CTA
# Features: Multi-layered soft drop shadow, floating paper card, tactile depth.
# ==============================================================================
def render_navy_direction_1():
    W, H = 1080, 1350
    img = create_textured_white_canvas(W, H)
    draw = ImageDraw.Draw(img)

    # Top Floating Header Bar
    draw.text((70, 75), "NASKAH", font=f("ExtraBold", 24), fill="#0B192C")
    draw.text((200, 77), "•  ACADEMIC OPERATING SYSTEM", font=f("SemiBold", 16), fill="#64748B")
    draw.text((880, 77), "EDISI #01", font=f("Bold", 16), fill="#0B192C")
    draw.line([(70, 115), (1010, 115)], fill="#CBD5E1", width=1)

    # Category Pill
    draw.rounded_rectangle([70, 150, 380, 195], radius=22, fill="#0B192C")
    draw.text((95, 162), "METODOLOGI // BAB 3", font=f("ExtraBold", 15), fill="#FFFFFF")

    # Main Headline - Powerful Navy Montserrat hierarchy
    draw.text((70, 225), "Kenapa Bab 3 Kamu", font=f("Medium", 52), fill="#0B192C")
    draw.text((70, 290), "Sering Ditolak Dosen?", font=f("ExtraBold", 60), fill="#0B192C")

    # Hook Subtitle
    sub = (
        "Bukan karena topiknya yang salah, tapi karena 3 benang merah ini\n"
        "belum sinkron antara Rumusan Masalah, Variabel, dan Uji Statistik."
    )
    draw.text((70, 380), sub, font=f("Regular", 23), fill="#475569", spacing=8)

    # HERO FLOATING CARD WITH MULTI-LAYERED SOFT SHADOW
    card_bbox = [70, 480, 1010, 1060]
    draw_shadow(img, card_bbox, radius=20, blur=32, offset_y=16, shadow_color=(11, 25, 44, 40))
    draw_shadow(img, card_bbox, radius=20, blur=10, offset_y=6, shadow_color=(11, 25, 44, 25))

    # Re-draw on top of shadow
    draw = ImageDraw.Draw(img)
    # The Card: Crisp White with Deep Navy top header strip
    draw.rounded_rectangle(card_bbox, radius=20, fill="#FFFFFF", outline="#E2E8F0", width=2)
    
    # Navy Top Bar inside Card
    draw.rounded_rectangle([70, 480, 1010, 560], radius=20, fill="#0B192C")
    draw.rectangle([70, 520, 1010, 560], fill="#0B192C") # flatten bottom radius
    draw.text((105, 502), "CHECKLIST 3 BENANG MERAH RISET", font=f("ExtraBold", 18), fill="#FFFFFF")
    draw.text((860, 502), "[ WAJIB CEK ]", font=f("Bold", 15), fill="#93C5FD")

    # 3 Items inside Floating Card with soft icons and inline pills
    items = [
        ("01", "Definisi Operasional Terukur", "Jangan tulis 'Pengetahuan: Baik/Kurang' tanpa cut-off score yang valid."),
        ("02", "Skala Data Menentukan Uji", "Uji Chi-Square hanya untuk Kategorik vs Kategorik, bukan data kontinu."),
        ("03", "Instrumen Memiliki Bukti Validitas", "Gunakan kuesioner baku atau cantumkan rencana uji validitas empiris.")
    ]

    iy = 600
    for num, title, desc in items:
        # Mini number pill
        draw.rounded_rectangle([105, iy + 5, 165, iy + 55], radius=10, fill="#0B192C")
        draw.text((120, iy + 16), num, font=f("Bold", 20), fill="#FFFFFF")

        draw.text((185, iy + 5), title, font=f("Bold", 25), fill="#0B192C")
        draw.text((185, iy + 45), desc, font=f("Regular", 20), fill="#475569", spacing=4)
        
        # Divider line
        if num != "03":
            draw.line([(105, iy + 115), (975, iy + 115)], fill="#F1F5F9", width=2)
        iy += 135

    # Bottom Sticky Action Bar (Navy Button with warm shadow)
    btn_bbox = [70, 1120, 1010, 1210]
    draw_shadow(img, btn_bbox, radius=45, blur=20, offset_y=8, shadow_color=(11, 25, 44, 35))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(btn_bbox, radius=45, fill="#0B192C")
    draw.text((290, 1147), "SWIPE UNTUK LIHAT MATRIKS LENGKAP ➔", font=f("ExtraBold", 22), fill="#FFFFFF")

    # Footer Links
    draw.text((70, 1260), "@naskah.id  •  Teman Diskusi Akademik", font=f("SemiBold", 19), fill="#64748B")
    draw.text((850, 1260), "SIMPAN POST ↗", font=f("Bold", 19), fill="#0B192C")

    p = os.path.join(output_dir, "navy_direction_1_architectural.jpg")
    img.convert("RGB").save(p, "JPEG", quality=95)
    return p

# ==============================================================================
# NAVY DIRECTION 2: "NAVY MODULAR COMPARISON" (Slide Isi / Matriks)
# Base: Textured Crisp White
# Features: Two-tier comparison, multi-layered shadows, deep navy hierarchy.
# ==============================================================================
def render_navy_direction_2():
    W, H = 1080, 1350
    img = create_textured_white_canvas(W, H)
    draw = ImageDraw.Draw(img)

    # Top Brand Header
    draw.text((70, 75), "NASKAH", font=f("ExtraBold", 24), fill="#0B192C")
    draw.text((200, 77), "/ RESEARCH MATRIX", font=f("SemiBold", 16), fill="#64748B")
    draw.text((880, 77), "SLIDE 03 / 06", font=f("Bold", 16), fill="#0B192C")
    draw.line([(70, 115), (1010, 115)], fill="#CBD5E1", width=1)

    # Main Headline
    draw.text((70, 150), "Panduan Cepat Memilih", font=f("Medium", 42), fill="#0B192C")
    draw.text((70, 205), "UJI BIVARIAT SKRIPSI", font=f("ExtraBold", 54), fill="#0B192C")

    draw.text((70, 280), "Gunakan tabel ini sebelum kamu membuka menu 'Analyze' di software statistik:", font=f("Regular", 22), fill="#475569")

    # 3 Floating Comparison Cards with Soft Shadows
    matrix = [
        ("KATEGORIK vs KATEGORIK", "Chi-Square Test", "Alternatif: Fisher's Exact Test (jika ada cell expected < 5)", "#0B192C", "#FFFFFF"),
        ("1 KATEGORIK (2 KELP) + 1 NUMERIK", "Independent t-Test", "Alternatif: Mann-Whitney U Test (jika data tidak berdistribusi normal)", "#1E3E62", "#FFFFFF"),
        ("1 KATEGORIK (>2 KELP) + 1 NUMERIK", "One-Way ANOVA", "Alternatif: Kruskal-Wallis Test (uji non-parametrik)", "#F1F5F9", "#0B192C")
    ]

    cy = 345
    for category, main_test, alt_test, card_bg, card_fg in matrix:
        card_box = [70, cy, 1010, cy + 225]
        draw_shadow(img, card_box, radius=18, blur=24, offset_y=10, shadow_color=(11, 25, 44, 28))
        draw = ImageDraw.Draw(img)

        # Draw card container
        draw.rounded_rectangle(card_box, radius=18, fill="#FFFFFF", outline="#E2E8F0", width=2)
        
        # Category tag
        draw.rounded_rectangle([95, cy + 22, 540, cy + 68], radius=10, fill="#F1F5F9")
        draw.text((115, cy + 34), category, font=f("ExtraBold", 16), fill="#0B192C")

        # Main Recommended Test Pill
        draw.rounded_rectangle([95, cy + 85, 480, cy + 145], radius=12, fill="#0B192C")
        draw.text((120, cy + 100), main_test, font=f("ExtraBold", 24), fill="#FFFFFF")

        # Alternative Text below
        draw.rounded_rectangle([95, cy + 160, 985, cy + 205], radius=8, fill="#F8FAFC", outline="#E2E8F0", width=1)
        draw.text((115, cy + 172), f"• {alt_test}", font=f("SemiBold", 17), fill="#475569")

        cy += 255

    # Bottom Footer Bar
    draw.line([(70, 1180), (1010, 1180)], fill="#CBD5E1", width=1)
    draw.text((70, 1220), "Naskah — Partner Bedah Metodologi & Statistik", font=f("Bold", 21), fill="#0B192C")
    draw.text((70, 1255), "Simpan tabel ini & bagikan ke rekan bimbinganmu ↗", font=f("Regular", 18), fill="#64748B")

    # Bookmark Badge
    draw.rounded_rectangle([840, 1215, 1010, 1275], radius=30, fill="#0B192C")
    draw.text((885, 1235), "SIMPAN 🔖", font=f("Bold", 16), fill="#FFFFFF")

    p = os.path.join(output_dir, "navy_direction_2_matrix.jpg")
    img.convert("RGB").save(p, "JPEG", quality=95)
    return p

p1 = render_navy_direction_1()
p2 = render_navy_direction_2()
print("Generated Navy Directions:")
print("1:", p1)
print("2:", p2)
