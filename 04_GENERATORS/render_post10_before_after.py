"""
Generator Visual: Post #10 — Before vs After (3-Tier Discussion Loop)
Style: NASKAH OFFICIAL CANONICAL PALETTE (Warm Cream, High-Energy Orange, Deep Midnight Navy)
Zero-Collision Dynamic Layout Engine
"""

import pathlib, textwrap, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(pathlib.Path(r"D:/tm/06_Content/04_GENERATORS")))
from emoji_assets import paste_emoji, strip_all_emojis

BASE = pathlib.Path(r"D:/tm/06_Content")
FONT_DIR = BASE / "02_BRAND_ASSETS/fonts/Poppins"
LOGO_WHITE = BASE / "02_BRAND_ASSETS/logos/logo_cutouts_clean/official_logo_white.png"
LOGO_TRANSPARENT = BASE / "02_BRAND_ASSETS/logos/logo_cutouts_clean/official_logo_transparent.png"
OUT_DIR = BASE / "05_OUTPUTS/post_10_before_after"
OUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1350

# ── NASKAH CANONICAL PALETTE (Warm Cream, Vibrant Orange, Deep Midnight Navy) ──
CREAM        = "#F5F2EB"
CREAM_LIGHT  = "#FDFBF6"
NAVY         = "#071726"
NAVY_LIGHT   = "#0E2338"
ORANGE       = "#E85929"
ORANGE_LIGHT = "#FFF0EB"
RED_ERR      = "#DC2626"
RED_BG       = "#FEF2F2"
GREEN_OK     = "#16A34A"
GREEN_BG     = "#F0FDF4"
PORCELAIN    = "#F1F5F9"
INK          = "#0B131D"
WHITE        = "#FFFFFF"
MUTED        = "#6B7C8C"
MUTED_LIGHT  = "#A2B4C4"
BORDER       = "#E0D9CB"
BORDER_DARK  = "#1E344A"

def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    fp = FONT_DIR / name
    return ImageFont.truetype(str(fp), size)

F = {
    "display":  font("Poppins-ExtraBold.ttf", 74),
    "headline": font("Poppins-ExtraBold.ttf", 64),
    "section":  font("Poppins-Bold.ttf", 38),
    "sub":      font("Poppins-Bold.ttf", 30),
    "card_t":   font("Poppins-Bold.ttf", 26),
    "body_b":   font("Poppins-SemiBold.ttf", 24),
    "body_m":   font("Poppins-Medium.ttf", 23),
    "body_r":   font("Poppins-Regular.ttf", 21),
    "badge":    font("Poppins-Bold.ttf", 20),
    "tag":      font("Poppins-SemiBold.ttf", 19),
    "num":      font("Poppins-ExtraBold.ttf", 26),
}

def draw_header(im: Image.Image, tag: str, light_mode: bool = True, on_orange: bool = False):
    d = ImageDraw.Draw(im)
    logo_w, logo_h = 44, 44
    lx, ly = 90, 80
    logo_path = LOGO_TRANSPARENT if (light_mode and not on_orange) else LOGO_WHITE
    if logo_path.exists():
        lg = Image.open(logo_path).convert("RGBA")
        lg.thumbnail((logo_w, logo_h), Image.Resampling.LANCZOS)
        im.paste(lg, (lx, ly), lg)
    else:
        d.rounded_rectangle((lx, ly, lx + logo_w, ly + logo_h), radius=10, fill=ORANGE)
        d.text((lx + 12, ly + 6), "N", font=F["section"], fill=WHITE)

    handle_color = WHITE if (not light_mode or on_orange) else NAVY
    d.text((lx + logo_w + 16, ly + 10), "naskah.fk", font=F["tag"], fill=handle_color)

    if tag:
        clean_tag = strip_all_emojis(tag)
        bg = WHITE if (not light_mode or on_orange) else ORANGE
        fg = ORANGE if (not light_mode or on_orange) else WHITE
        fnt = F["badge"]
        bb = d.textbbox((0, 0), clean_tag, font=fnt)
        tw = bb[2] - bb[0]
        th = bb[3] - bb[1]
        pw, ph = tw + 44, max(th + 20, 44)
        rx = 990 - pw
        d.rounded_rectangle((rx, ly, 990, ly + ph), radius=ph // 2, fill=bg)
        d.text((rx + pw // 2, ly + ph // 2), clean_tag, font=fnt, fill=fg, anchor="mm")

def draw_footer(im: Image.Image, page: str, tag: str, light_mode: bool = True, on_orange: bool = False):
    d = ImageDraw.Draw(im)
    y = 1260
    c = WHITE if (not light_mode or on_orange) else MUTED
    d.text((90, y), "naskah.fk", font=F["tag"], fill=c)
    if tag:
        d.text((540, y), strip_all_emojis(tag)[:35], font=F["tag"], fill=c, anchor="mt")
    d.text((990, y), page, font=F["tag"], fill=c, anchor="rt")

def draw_wrapped_text(d, text, x, y, max_w, font_obj, fill_color, line_spacing=8):
    words = text.split()
    lines = []
    curr = []
    for w in words:
        test = " ".join(curr + [w])
        bb = d.textbbox((0, 0), test, font=font_obj)
        if (bb[2] - bb[0]) <= max_w:
            curr.append(w)
        else:
            if curr:
                lines.append(" ".join(curr))
            curr = [w]
    if curr:
        lines.append(" ".join(curr))
    
    cur_y = y
    for line in lines:
        d.text((x, cur_y), line, fill=fill_color, font=font_obj)
        bb = d.textbbox((0, 0), line, font=font_obj)
        cur_y += (bb[3] - bb[1]) + line_spacing
    return cur_y

# ─────────────────────────────────────────────────────────────
# SLIDE 1: COVER (Warm Cream)
# ─────────────────────────────────────────────────────────────
def render_slide_1():
    im = Image.new("RGB", (W, H), CREAM)
    draw_header(im, "Bedah Naskah", light_mode=True)
    d = ImageDraw.Draw(im)

    lines = ["KALIMAT YANG BIKIN", "PENGUJI MARAH", "VS LANGSUNG ACC."]
    y = 200
    for i, l in enumerate(lines):
        bb = d.textbbox((90, y), l, font=F["headline"])
        if i == 1:
            bar_y = bb[3] + 6
            d.rounded_rectangle((90, bar_y, bb[2] + 16, bar_y + 12), radius=6, fill=ORANGE)
        d.text((90, y), l, font=F["headline"], fill=NAVY)
        y += 74

    y += 18
    body_text = "Bedah naskah nyata: 2 versi Bab Pembahasan yang menghasilkan nasib sidang 180 derajat berbeda."
    y = draw_wrapped_text(d, body_text, 90, y, 900, F["body_m"], MUTED, line_spacing=8) + 24

    # Split Comparison Cards Preview
    card_y = y
    box_w = (900 - 20) // 2
    
    # Left Card (BEFORE)
    l_box = (90, card_y, 90 + box_w, card_y + 360)
    d.rounded_rectangle(l_box, radius=20, fill=WHITE, outline=RED_ERR, width=2)
    d.rounded_rectangle((110, card_y + 20, 110 + 170, card_y + 56), radius=10, fill=RED_BG)
    d.text((110 + 85, card_y + 38), "VERSI REKAP", font=F["badge"], fill=RED_ERR, anchor="mm")
    
    b_desc = "Cuma menyalin ulang angka dari Tabel Bab 4. Tidak ada argumen ilmiah atau pembahasan mekanisme."
    draw_wrapped_text(d, b_desc, 110, card_y + 75, box_w - 40, F["body_r"], INK, line_spacing=6)
    
    d.rounded_rectangle((110, card_y + 250, 90 + box_w - 20, card_y + 340), radius=12, fill=RED_BG)
    d.text((125, card_y + 265), "Dampak Sidang:", font=F["body_b"], fill=RED_ERR)
    d.text((125, card_y + 295), "Dibantai penguji & revisi total.", font=F["body_r"], fill=INK)

    # Right Card (AFTER)
    r_x = 90 + box_w + 20
    r_box = (r_x, card_y, r_x + box_w, card_y + 360)
    d.rounded_rectangle(r_box, radius=20, fill=WHITE, outline=GREEN_OK, width=2)
    d.rounded_rectangle((r_x + 20, card_y + 20, r_x + 20 + 170, card_y + 56), radius=10, fill=GREEN_BG)
    d.text((r_x + 20 + 85, card_y + 38), "3-TIER LOOP", font=F["badge"], fill=GREEN_OK, anchor="mm")
    
    a_desc = "Assertion + Mekanisme + Positioning. Paragraf berbobot yang menunjukkan kematangan metodologi."
    draw_wrapped_text(d, a_desc, r_x + 20, card_y + 75, box_w - 40, F["body_r"], INK, line_spacing=6)

    d.rounded_rectangle((r_x + 20, card_y + 250, r_x + box_w - 20, card_y + 340), radius=12, fill=GREEN_BG)
    d.text((r_x + 35, card_y + 265), "Hasil Sidang:", font=F["body_b"], fill=GREEN_OK)
    d.text((r_x + 35, card_y + 295), "ACC dalam 15 menit tanpa debat.", font=F["body_r"], fill=INK)

    # Bottom CTA box
    cta_y = 1040
    d.rounded_rectangle((90, cta_y, 990, cta_y + 140), radius=22, fill=NAVY)
    d.text((130, cta_y + 38), "Pelajari rumusnya di slide berikutnya", font=F["card_t"], fill=WHITE)
    d.text((130, cta_y + 82), "Geser ke slide 2 untuk bedah kalimat lengkap", font=F["body_r"], fill=MUTED_LIGHT)

    draw_footer(im, "01/05", "Bedah Naskah", light_mode=True)
    return im

# ─────────────────────────────────────────────────────────────
# SLIDE 2: THE "BEFORE" (Vibrant Orange Background)
# ─────────────────────────────────────────────────────────────
def render_slide_2():
    im = Image.new("RGB", (W, H), ORANGE)
    draw_header(im, "Kesalahan #1", light_mode=False, on_orange=True)
    d = ImageDraw.Draw(im)

    lines = ["MENULIS BAB 5", "SEPERTI REKAP TABEL"]
    y = 200
    for l in lines:
        d.text((90, y), l, font=F["headline"], fill=WHITE)
        y += 74

    d.text((90, y + 10), "Kesalahan paling umum yang bikin dosen penguji langsung emosi:", font=F["body_b"], fill=CREAM_LIGHT)
    y += 65

    # Card 1: Bad Example
    box1 = (90, y, 990, y + 260)
    d.rounded_rectangle(box1, radius=20, fill=WHITE)
    d.rounded_rectangle((120, y + 20, 120 + 220, y + 58), radius=10, fill=RED_BG)
    d.text((120 + 110, y + 39), "CONTOH DRAF KELIRU", font=F["badge"], fill=RED_ERR, anchor="mm")
    
    bad_sample = "\"Berdasarkan Tabel 4.1, diperoleh hasil bahwa 65% responden mengalami tingkat kecemasan tinggi saat menyelesaikan skripsi. Data ini menunjukkan bahwa kecemasan adalah masalah signifikan.\""
    draw_wrapped_text(d, bad_sample, 120, y + 75, 840, F["body_m"], INK, line_spacing=8)

    y += 285

    # Card 2: Why Examiner Gets Mad (Navy Box)
    box2 = (90, y, 990, y + 330)
    d.rounded_rectangle(box2, radius=20, fill=NAVY)
    d.text((130, y + 30), "Mengapa Penguji Membantai Paragraf Ini?", font=F["card_t"], fill=ORANGE)
    
    crit_points = [
        "1. Dosen sudah membaca angka di Tabel Bab 4 -- jangan diulang!",
        "2. Kalimat di atas tidak menjawab MENGAPA fenomena itu terjadi.",
        "3. Tidak ada teori ilmiah atau perbandingan dengan riset terdahulu."
    ]
    cy = y + 85
    for cp in crit_points:
        draw_wrapped_text(d, cp, 130, cy, 820, F["body_r"], WHITE, line_spacing=10)
        cy += 75

    draw_footer(im, "02/05", "Bedah Naskah", light_mode=False, on_orange=True)
    return im

# ─────────────────────────────────────────────────────────────
# SLIDE 3: THE "AFTER" (Deep Midnight Navy)
# ─────────────────────────────────────────────────────────────
def render_slide_3():
    im = Image.new("RGB", (W, H), NAVY)
    draw_header(im, "Versi ACC", light_mode=False)
    d = ImageDraw.Draw(im)

    lines = ["TERAPKAN 3-TIER LOOP", "PADA SETIAP TEMUAN"]
    y = 200
    for i, l in enumerate(lines):
        bb = d.textbbox((90, y), l, font=F["headline"])
        if i == 0:
            bar_y = bb[3] + 6
            d.rounded_rectangle((90, bar_y, bb[2] + 16, bar_y + 12), radius=6, fill=ORANGE)
        d.text((90, y), l, font=F["headline"], fill=WHITE)
        y += 74

    y += 20
    # 3 Dynamic Tiers Stacked Container
    tiers = [
        ("T1: ASSERTION", GREEN_OK, "Temuan utama menunjukkan bahwa 65% responden mengalami kecemasan berat saat menyelesaikan skripsi."),
        ("T2: MEKANISME", ORANGE, "Hal ini dapat dijelaskan melalui teori tekanan akademik Eccles (2002): mahasiswa menghadapi dualitas ekspektasi kelulusan tanpa didukung pendampingan psikologis struktural."),
        ("T3: POSITIONING", "#38BDF8", "Temuan ini konsisten dengan studi Wijayanti (2023) pada mahasiswa kesehatan, namun berbeda dengan riset Chen (2022) pada rumpun sosial karena disparitas metodologis.")
    ]

    for title, col, text in tiers:
        card_h = 190
        box = (90, y, 990, y + card_h)
        d.rounded_rectangle(box, radius=18, fill=NAVY_LIGHT, outline=BORDER_DARK, width=2)
        
        # Pill Tag
        d.rounded_rectangle((115, y + 18, 115 + 180, y + 54), radius=10, fill=col)
        d.text((115 + 90, y + 36), title, font=F["badge"], fill=WHITE, anchor="mm")
        
        # Text
        draw_wrapped_text(d, text, 115, y + 68, 840, F["body_r"], PORCELAIN, line_spacing=6)
        y += card_h + 16

    d.text((90, 1150), "Simpan bagan framework 3-Tier Loop di slide 4", font=F["body_b"], fill=MUTED_LIGHT)
    draw_footer(im, "03/05", "Bedah Naskah", light_mode=False)
    return im

# ─────────────────────────────────────────────────────────────
# SLIDE 4: THE FRAMEWORK CHEAT SHEET (Warm Cream)
# ─────────────────────────────────────────────────────────────
def render_slide_4():
    im = Image.new("RGB", (W, H), CREAM)
    draw_header(im, "Framework", light_mode=True)
    d = ImageDraw.Draw(im)

    lines = ["THE 3-TIER", "DISCUSSION LOOP"]
    y = 200
    for i, l in enumerate(lines):
        bb = d.textbbox((90, y), l, font=F["headline"])
        if i == 1:
            bar_y = bb[3] + 6
            d.rounded_rectangle((90, bar_y, bb[2] + 16, bar_y + 12), radius=6, fill=ORANGE)
        d.text((90, y), l, font=F["headline"], fill=NAVY)
        y += 74

    d.text((90, y + 8), "Struktur 3 blok wajib untuk setiap temuan kunci di Bab 5:", font=F["body_b"], fill=MUTED)
    y += 55

    steps = [
        ("01", "TIER 1: ASSERTION (Temuan Inti)", "Nyatakan apa temuan kuncinya secara tegas (1-2 kalimat). Langsung ke inti hasil, tanpa basa-basi."),
        ("02", "TIER 2: MECHANISM (Mekanisme / Teori)", "Jelaskan MENGAPA fenomena itu terjadi dengan landasan teori ilmiah atau mekanisme biologis/sosial."),
        ("03", "TIER 3: POSITIONING (Peta Riset Global)", "Bandingkan dengan 2 studi terdahulu (sejalan vs bertentangan) dan jelaskan alasannya.")
    ]

    for num, title, desc in steps:
        card_h = 175
        box = (90, y, 990, y + card_h)
        d.rounded_rectangle(box, radius=20, fill=WHITE, outline=BORDER, width=2)
        
        # Number badge
        d.rounded_rectangle((114, y + 20, 174, y + 80), radius=14, fill=ORANGE_LIGHT)
        d.text((144, y + 50), num, font=F["num"], fill=ORANGE, anchor="mm")
        
        # Title & Desc
        d.text((195, y + 24), title, font=F["card_t"], fill=NAVY)
        draw_wrapped_text(d, desc, 195, y + 64, 760, F["body_r"], MUTED, line_spacing=6)
        y += card_h + 16

    # Bottom Callout Box
    d.rounded_rectangle((90, 1020, 990, 1170), radius=22, fill=NAVY)
    d.text((130, 1058), "Simpan contekan ini untuk nulis nanti malam", font=F["card_t"], fill=WHITE)
    d.text((130, 1102), "Gunakan saat menyusun Bab Pembahasan skripsi/tesis kamu", font=F["body_r"], fill=MUTED_LIGHT)

    draw_footer(im, "04/05", "Bedah Naskah", light_mode=True)
    return im

# ─────────────────────────────────────────────────────────────
# SLIDE 5: LEAD MAGNET CTA (Warm Cream)
# ─────────────────────────────────────────────────────────────
def render_slide_5():
    im = Image.new("RGB", (W, H), ORANGE)
    draw_header(im, "Free Diagnosis", light_mode=False, on_orange=True)
    d = ImageDraw.Draw(im)

    lines = ["YAKIN BAB 5 KAMU", "SUDAH SIAP SIDANG?"]
    y = 200
    for l in lines:
        d.text((90, y), l, font=F["headline"], fill=WHITE)
        y += 74

    y += 18
    # Offer Card Box (White background to pop on Orange)
    offer_box = (90, y, 990, y + 360)
    d.rounded_rectangle(offer_box, radius=22, fill=WHITE, outline=BORDER, width=2)
    
    d.text((130, y + 30), "Free 10-Minute Method & Discussion Audit", font=F["card_t"], fill=ORANGE)
    instructions = (
        "Kirimkan 3 hal ini via DM ke @naskah.fk:\n\n"
        "1. Judul Skripsi / Tesis kamu\n"
        "2. Rumusan Masalah (Bab 1)\n"
        "3. Kesimpulan Utama (Bab 5)\n\n"
        "Tim ahli kami akan kirimkan 3 Poin Evaluasi Kritis secara GRATIS dalam 1x24 jam."
    )
    draw_wrapped_text(d, instructions, 130, y + 75, 820, F["body_m"], INK, line_spacing=8)

    y += 385

    # Big CTA Button (Navy background to pop on Orange)
    btn_box = (90, y, 990, y + 140)
    d.rounded_rectangle(btn_box, radius=24, fill=NAVY)
    d.text((540, y + 45), "DM KATA \"DIAGNOSIS\"", font=F["display"], fill=WHITE, anchor="mm")
    d.text((540, y + 100), "ke Instagram @naskah.fk sekarang", font=F["body_b"], fill=CREAM_LIGHT, anchor="mm")

    # Trust note (White text on Orange)
    d.text((90, 1145), "Privasi naskah dijamin 100%. Tidak akan dipublikasikan.", font=F["body_m"], fill=CREAM_LIGHT)
    d.text((90, 1185), "Kuota terbatas: 10 naskah review gratis per hari.", font=F["body_m"], fill=CREAM_LIGHT)

    draw_footer(im, "05/05", "Bedah Naskah", light_mode=False, on_orange=True)
    return im

def main():
    s1 = render_slide_1()
    s1.save(OUT_DIR / "slide_01.png")
    
    s2 = render_slide_2()
    s2.save(OUT_DIR / "slide_02.png")
    
    s3 = render_slide_3()
    s3.save(OUT_DIR / "slide_03.png")
    
    s4 = render_slide_4()
    s4.save(OUT_DIR / "slide_04.png")
    
    s5 = render_slide_5()
    s5.save(OUT_DIR / "slide_05.png")

    # Generate Contact Sheet Preview
    cs = Image.new("RGB", (W * 5 // 2, H // 2), NAVY)
    for i, s in enumerate([s1, s2, s3, s4, s5]):
        thumb = s.resize((W // 2, H // 2), Image.Resampling.LANCZOS)
        cs.paste(thumb, (i * (W // 2), 0))
    cs.save(OUT_DIR / "POST10_ALL_SLIDES_CANONICAL.png")
    print("Post 10 canonical rendered successfully at:", OUT_DIR)

if __name__ == "__main__":
    main()
