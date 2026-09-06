from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/naskah-visuals/test_carousel_v2_refined")
OUT.mkdir(parents=True, exist_ok=True)
FONT_DIR = Path(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/fonts/Poppins")
LOGO_PATH = Path(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/naskah-visuals/logo_cutouts/official_logo_cropped_raw.png")

W, H = 1080, 1350

# Global Palette
CREAM = "#F5F2EB"
NAVY = "#071726"
INK = "#0B131D"
ORANGE = "#E85929"
MUTED = "#55606E"
WHITE = "#FFFFFF"

# Typography (Poppins)
def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)

F = {
    "title_masif": font("Poppins-ExtraBold.ttf", 98),
    "title_xl": font("Poppins-ExtraBold.ttf", 88),
    "title_l": font("Poppins-Bold.ttf", 72),
    "quote_m": font("Poppins-Bold.ttf", 46),
    "body_lg": font("Poppins-Regular.ttf", 36),
    "body_med": font("Poppins-Medium.ttf", 32),
    "pill_text": font("Poppins-SemiBold.ttf", 28),
    "footer_brand": font("Poppins-SemiBold.ttf", 26),
    "footer_page": font("Poppins-Bold.ttf", 26),
}

# Prepare Official Logo Marks (Clean, compact, no text)
raw_logo = Image.open(LOGO_PATH).convert("RGBA")
# Target size for top-left header logo: ~64px wide
aspect = raw_logo.height / raw_logo.width
LOGO_TOP_CREAM = raw_logo.resize((64, int(64 * aspect)), Image.Resampling.LANCZOS)

# For dark/colored backgrounds, create a clean mini rounded badge (56x56)
LOGO_BADGE_DARK = Image.new("RGBA", (72, 72), (0,0,0,0))
d_b = ImageDraw.Draw(LOGO_BADGE_DARK)
d_b.rounded_rectangle((0,0,72,72), radius=18, fill="#F5F2EB")
scaled_for_badge = raw_logo.resize((56, int(56 * aspect)), Image.Resampling.LANCZOS)
LOGO_BADGE_DARK.paste(scaled_for_badge, ((72-56)//2, (72-scaled_for_badge.height)//2), scaled_for_badge)

# STRICT MARGIN & GRID SYSTEM:
# Left Margin: 90px, Right Margin: 90px (Usable width = 900px)
# Top Margin: 100px (Logo sits at y=100)
# Content starts at y=230
# Footer sits at y=1240 (Base y=1255)

def text_size(draw, text, f):
    box = draw.textbbox((0,0), text, font=f)
    return (box[2]-box[0], box[3]-box[1])

def wrap_text(draw, text, f, max_w=900):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if text_size(draw, test, f)[0] <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def draw_header_logo(slide_img, bg_type="cream"):
    if bg_type == "cream":
        slide_img.paste(LOGO_TOP_CREAM, (90, 95), LOGO_TOP_CREAM)
    else:
        # dark navy / orange
        slide_img.paste(LOGO_BADGE_DARK, (90, 90), LOGO_BADGE_DARK)

def draw_footer(draw, page_num, total="05", bg_type="cream"):
    c = INK if bg_type == "cream" else CREAM
    # Clean, simple bottom footer
    draw.text((90, 1245), "naskah.fk", font=F["footer_brand"], fill=c, anchor="ls")
    draw.text((990, 1245), f"{page_num}/{total}", font=F["footer_page"], fill=c, anchor="rs")

def marker_oval(draw, bbox, color=ORANGE, width=9):
    x1, y1, x2, y2 = bbox
    draw.arc((x1, y1, x2, y2), start=10, end=355, fill=color, width=width)
    draw.arc((x1+4, y1+3, x2-3, y2-1), start=170, end=530, fill=color, width=width//2+2)

def pill_button(draw, xy, wh, text, fill, text_fill=WHITE, outline=None, stroke=3, icon_arrow=False):
    x, y = xy; w, h = wh
    draw.rounded_rectangle((x, y, x+w, y+h), radius=h//2, fill=fill, outline=outline, width=stroke)
    ty = y + h//2
    if icon_arrow:
        ax = x + 36; ay = ty
        draw.line((ax-8, ay+6, ax+8, ay-6), fill=text_fill, width=4)
        draw.line((ax, ay-6, ax+8, ay-6), fill=text_fill, width=4)
        draw.line((ax+8, ay-6, ax+8, ay+2), fill=text_fill, width=4)
        draw.text((x+66, ty), text, font=F["pill_text"], fill=text_fill, anchor="lm")
    else:
        draw.text((x + w//2, ty), text, font=F["pill_text"], fill=text_fill, anchor="mm")


# ==========================================
# SLIDE 1 (COVER)
# ==========================================
im1 = Image.new("RGB", (W, H), CREAM)
d1 = ImageDraw.Draw(im1)
draw_header_logo(im1, "cream")

# Title lines
y_start = 250
headline = ["BAB 3", "SERING", "DITOLAK", "DOSEN?"]
for i, line in enumerate(headline):
    d1.text((90, y_start + i*112), line, font=F["title_masif"], fill=INK)

# Oval over DITOLAK
marker_oval(d1, (75, y_start + 224, 620, y_start + 348), ORANGE, width=10)

# Body copy with consistent spacing
body_y = 750
b1 = wrap_text(d1, "Masalahnya mungkin bukan idenya. Bisa jadi definisi operasionalmu belum sinkron.", F["body_lg"], 860)
for i, line in enumerate(b1):
    d1.text((90, body_y + i*52), line, font=F["body_lg"], fill=INK)

# Pill CTA
pill_button(d1, (90, 940), (330, 72), "Swipe buat bedah", fill=CREAM, outline=INK, text_fill=INK, stroke=4)
draw_footer(d1, "01", "05", "cream")
im1.save(OUT / "slide_01_cover.png")


# ==========================================
# SLIDE 2 (FORMULA - PROPORTIONAL & CONSISTENT WHITESPACE)
# ==========================================
im2 = Image.new("RGB", (W, H), ORANGE)
d2 = ImageDraw.Draw(im2)
draw_header_logo(im2, "orange")
# NO ANOMALOUS "page two" TEXT!

# Centered, balanced vertical rhythm
y_h2 = 240
h2 = ["DEFINISI", "OPERASIONAL", "BUKAN HIASAN"]
for i, line in enumerate(h2):
    d2.text((90, y_h2 + i*106), line, font=F["title_xl"], fill=INK)

# Subtitle / body text
b2_y = 600
b2 = wrap_text(d2, "Di tabel DO, dosen mencari 3 hal kunci: apa yang diukur, instrumen apa yang dipakai, dan apa skala datanya.", F["body_lg"], 880)
for i, line in enumerate(b2):
    d2.text((90, b2_y + i*50), line, font=F["body_lg"], fill=INK)

# Balanced Formula Stack (Centered in lower half, perfect breathing room)
formula_y = 810
# Row 1: Two parallel pills
pill_button(d2, (90, formula_y), (425, 80), "Variabel Jelas  =", fill=INK, text_fill=WHITE)
pill_button(d2, (545, formula_y), (445, 80), "Uji Statistik Aman", fill=INK, text_fill=WHITE)

# Row 2: Result pill
pill_button(d2, (90, formula_y + 110), (900, 88), "→  Lebih Siap Masuk Ruang Sempro", fill="#24140D", text_fill=WHITE)

draw_footer(d2, "02", "05", "orange")
im2.save(OUT / "slide_02_formula.png")


# ==========================================
# SLIDE 3 (NAVY DEEP POSTER)
# ==========================================
im3 = Image.new("RGB", (W, H), NAVY)
d3 = ImageDraw.Draw(im3)
draw_header_logo(im3, "navy")

y_h3 = 250
h3 = ["SKALA", "DATA", "AMBIGU"]
for i, line in enumerate(h3):
    d3.text((90, y_h3 + i*114), line, font=F["title_masif"], fill=CREAM)

b3_y = 660
b3 = wrap_text(d3, "Contoh klasik: menulis kepatuhan sebagai 'baik / kurang', tapi tanpa cut-off score yang jelas dari literatur.", F["body_lg"], 880)
for i, line in enumerate(b3):
    d3.text((90, b3_y + i*52), line, font=F["body_lg"], fill=CREAM)

d3.text((90, 890), "Ini bikin dosen penguji langsung tanya:", font=F["body_med"], fill="#9EB3C7")
d3.text((90, 960), "“Data kamu kategorik, ordinal,", font=F["quote_m"], fill=ORANGE)
d3.text((90, 1025), "atau numerik?”", font=F["quote_m"], fill=ORANGE)

draw_footer(d3, "03", "05", "navy")
im3.save(OUT / "slide_03_skala.png")


# ==========================================
# SLIDE 4 (CALLOUT / QUOTE)
# ==========================================
im4 = Image.new("RGB", (W, H), CREAM)
d4 = ImageDraw.Draw(im4)
draw_header_logo(im4, "cream")

y_h4 = 240
h4 = ["KUESIONER", "BUKAN", "SEKADAR", "FORM"]
for i, line in enumerate(h4):
    d4.text((90, y_h4 + i*106), line, font=F["title_xl"], fill=INK)

# Oval over BUKAN (second line)
marker_oval(d4, (65, y_h4 + 96, 470, y_h4 + 230), ORANGE, width=9)

b4_y = 710
d4.text((90, b4_y), "Kalau instrumen kamu buat sendiri, dosen pasti tanya:", font=F["body_med"], fill=INK)

# Quote container
d4.rounded_rectangle((90, 780, 990, 940), radius=40, fill=CREAM, outline=INK, width=4)
d4.text((540, 860), "“Sudah uji validitas empiris?”", font=F["quote_m"], fill=ORANGE, anchor="mm")

d4.text((90, 980), "Kalau belum, jangan klaim instrumenmu sudah siap di Bab 3.", font=F["body_med"], fill=INK)

draw_footer(d4, "04", "05", "cream")
im4.save(OUT / "slide_04_kuesioner.png")


# ==========================================
# SLIDE 5 (CTA OUTRO)
# ==========================================
im5 = Image.new("RGB", (W, H), CREAM)
d5 = ImageDraw.Draw(im5)
draw_header_logo(im5, "cream")

y_h5 = 240
h5 = ["RAPIKAN DO", "SEBELUM", "MASUK RUANG", "SEMPRO"]
for i, line in enumerate(h5):
    d5.text((90, y_h5 + i*108), line, font=F["title_xl"], fill=INK)

# Oval over SEMPRO
marker_oval(d5, (75, y_h5 + 322, 535, y_h5 + 438), ORANGE, width=10)

b5_y = 730
b5 = wrap_text(d5, "Satu tabel yang rapi menyelamatkan kamu dari revisi metodologi yang muter-muter.", F["body_lg"], 880)
for i, line in enumerate(b5):
    d5.text((90, b5_y + i*52), line, font=F["body_lg"], fill=INK)

pill_button(d5, (90, 920), (520, 78), "Save buat checklist Bab 3", fill=INK, text_fill=WHITE, icon_arrow=True)
d5.text((90, 1060), "Stuck di metodologi? naskah.fk siap bantu bedah alurnya.", font=F["body_med"], fill=MUTED)

draw_footer(d5, "05", "05", "cream")
im5.save(OUT / "slide_05_cta.png")

print("SLIDES REFINED SUCCESSFULLY.")
