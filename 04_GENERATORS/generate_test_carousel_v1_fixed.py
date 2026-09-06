from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

OUT = Path(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/naskah-visuals/test_carousel_v1_official_logo")
OUT.mkdir(parents=True, exist_ok=True)
FONT_DIR = Path(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/fonts/Poppins")

W, H = 1080, 1350

# Palette - Naskah Editorial Navy & Cream
CREAM = "#F5F2EB"
NAVY = "#071726"
INK = "#0B131D"
ORANGE = "#E85929"
MUTED = "#55606E"
WHITE = "#FFFFFF"

# Fonts
MONT_BLACK = FONT_DIR / "Poppins-ExtraBold.ttf"
MONT_BOLD = FONT_DIR / "Poppins-Bold.ttf"
MONT_SEMI = FONT_DIR / "Poppins-SemiBold.ttf"
MONT_MED = FONT_DIR / "Poppins-Medium.ttf"
MONT_REG = FONT_DIR / "Poppins-Regular.ttf"

def font(path, size):
    return ImageFont.truetype(str(path), size)

F = {
    "xxl": font(MONT_BLACK, 112),
    "xl": font(MONT_BLACK, 92),
    "l": font(MONT_BLACK, 74),
    "m": font(MONT_BOLD, 46),
    "m_semi": font(MONT_SEMI, 42),
    "body": font(MONT_REG, 35),
    "body2": font(MONT_MED, 32),
    "small": font(MONT_SEMI, 26),
    "tiny": font(MONT_BOLD, 22),
}

def text_size(draw, text, f):
    if not text:
        return (0,0)
    box = draw.textbbox((0,0), text, font=f)
    return (box[2]-box[0], box[3]-box[1])

def wrap_text(draw, text, f, max_width):
    words = text.split()
    lines, current = [], ""
    for w in words:
        candidate = (current + " " + w).strip()
        if text_size(draw, candidate, f)[0] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines

def draw_multiline(draw, xy, lines, f, fill, spacing=None):
    x, y = xy
    if isinstance(lines, str):
        lines = lines.split("\n")
    if spacing is None:
        spacing = int(f.size * 1.25)
    for i, line in enumerate(lines):
        draw.text((x, y + i*spacing), line, font=f, fill=fill)

def starburst(draw, cx, cy, r=18, fill=ORANGE, arms=8, width=9):
    for i in range(arms):
        angle = math.pi * 2 * i / arms
        x1 = cx + math.cos(angle)*4
        y1 = cy + math.sin(angle)*4
        x2 = cx + math.cos(angle)*r
        y2 = cy + math.sin(angle)*r
        draw.line((x1,y1,x2,y2), fill=fill, width=width)
    draw.ellipse((cx-5,cy-5,cx+5,cy+5), fill=fill)

def marker_oval(draw, bbox, color=ORANGE, width=8):
    x1,y1,x2,y2 = bbox
    draw.arc((x1,y1,x2,y2), start=10, end=355, fill=color, width=width)
    draw.arc((x1+4,y1+3,x2-3,y2-1), start=170, end=530, fill=color, width=width//2+2)

def pill(draw, xy, wh, text, fill, outline=None, text_fill=WHITE, f=None, stroke=3, icon_arrow=False, icon_dot=False):
    x,y = xy; w,h = wh
    draw.rounded_rectangle((x,y,x+w,y+h), radius=h//2, fill=fill, outline=outline, width=stroke)
    tx = x + w//2
    ty = y + h//2
    if icon_arrow:
        # draw sharp arrow icon
        ax = x + 38; ay = ty
        draw.line((ax-10, ay+8, ax+10, ay-8), fill=text_fill, width=4)
        draw.line((ax-2, ay-8, ax+10, ay-8), fill=text_fill, width=4)
        draw.line((ax+10, ay-8, ax+10, ay+4), fill=text_fill, width=4)
        draw.text((x+70, ty), text, font=f or F["small"], fill=text_fill, anchor="lm")
    elif icon_dot:
        draw.ellipse((x+30, ty-5, x+40, ty+5), fill=text_fill)
        draw.text((x+58, ty), text, font=f or F["small"], fill=text_fill, anchor="lm")
    else:
        draw.text((tx,ty), text, font=f or F["small"], fill=text_fill, anchor="mm")

def arrow_next(draw, x, y, color=ORANGE, bg="cream"):
    draw.rounded_rectangle((x, y, x+145, y+52), radius=26, outline=color, width=4)
    # arrow line & head
    draw.line((x+34, y+26, x+100, y+26), fill=color, width=6)
    draw.polygon([(x+98, y+14), (x+122, y+26), (x+98, y+38)], fill=color)
    tcol = INK if bg=="cream" else CREAM
    draw.text((x+165, y+12), "next page", font=F["tiny"], fill=tcol)

# Add official Naskah logo integration
LOGO_RAW = Image.open(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/naskah-visuals/logo_cutouts/official_logo_cropped_raw.png").convert("RGBA")
LOGO_CREAM = LOGO_RAW.resize((84, int(84 * LOGO_RAW.height / LOGO_RAW.width)), Image.Resampling.LANCZOS)
LOGO_BADGE = Image.open(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/naskah-visuals/logo_cutouts/badge_cream_for_dark_bg.png").convert("RGBA")
LOGO_BADGE_S = LOGO_BADGE.resize((72, 72), Image.Resampling.LANCZOS)

def footer(draw, bg="cream", page="01/05", slide_img=None):
    c = INK if bg == "cream" else CREAM
    # Replace orange starburst with Official Naskah Logo
    if bg == "cream" and slide_img is not None:
        # Paste raw logo directly onto cream background
        slide_img.paste(LOGO_CREAM, (80, 1222))
    elif slide_img is not None:
        # Paste logo inside a cream badge for dark backgrounds (Orange/Navy)
        slide_img.paste(LOGO_BADGE_S, (80, 1226), LOGO_BADGE_S)
    
    draw.text((180, 1238), "naskah.fk", font=F["small"], fill=c, anchor="lm")
    draw.text((990, 1238), page, font=F["small"], fill=c, anchor="rm")

def diagonal_label(draw, text, x, y, angle=-15, fill=ORANGE, f=None):
    f = f or F["tiny"]
    tw, th = text_size(draw, text, f)
    im = Image.new("RGBA", (tw+30, th+30), (0,0,0,0))
    d = ImageDraw.Draw(im)
    d.text((15,15), text, font=f, fill=fill)
    rot = im.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    draw.bitmap((x,y), rot, fill=None)


# SLIDE 1 (COVER)
im1 = Image.new("RGB", (W,H), CREAM)
d1 = ImageDraw.Draw(im1)
starburst(d1, 84, 95, r=22, fill=ORANGE, width=11)
x=84; y=210
lines = ["BAB 3", "SERING", "DITOLAK", "DOSEN?"]
for i,line in enumerate(lines):
    d1.text((x, y+i*116), line, font=F["xxl"], fill=INK)
# Oval precisely around DITOLAK
marker_oval(d1, (68, y+220, 615, y+345), ORANGE, width=10)
body = "Masalahnya mungkin bukan idenya. Bisa jadi definisi operasionalmu belum sinkron."
draw_multiline(d1, (84, 760), wrap_text(d1, body, F["body"], 820), F["body"], fill=INK, spacing=48)
pill(d1, (84, 945), (320, 68), "Swipe buat bedah", fill=CREAM, outline=INK, text_fill=INK, f=F["small"], stroke=4)
footer(d1, "cream", "01/05", im1)
im1.save(OUT / "slide_01_cover.png")


# SLIDE 2 (ORANGE FORMULA - FIXED ICONS)
im2 = Image.new("RGB", (W,H), ORANGE)
d2 = ImageDraw.Draw(im2)
starburst(d2, 84, 95, r=20, fill=INK, width=10)
diagonal_label(d2, "page two", 800, 85, angle=-16, fill=INK, f=F["tiny"])
headline = ["DEFINISI", "OPERASIONAL", "ITU BUKAN", "HIASAN"]
y = 200
for i,line in enumerate(headline):
    fs = F["xl"] if i < 2 else F["l"]
    d2.text((84, y+i*98), line, font=fs, fill=INK)
body = "Di tabel DO, dosen mencari 3 hal: apa yang diukur, pakai alat apa, dan hasilnya masuk skala data apa."
draw_multiline(d2, (84, 650), wrap_text(d2, body, F["body2"], 850), F["body2"], fill=INK, spacing=44)
# Formula pills without tofu glyphs
pill(d2, (84, 850), (410, 78), "variabel jelas =", fill=INK, text_fill=WHITE, f=F["small"], icon_dot=True)
pill(d2, (520, 850), (380, 78), "uji statistik aman", fill=INK, text_fill=WHITE, f=F["small"])
pill(d2, (230, 958), (560, 84), "lebih siap sempro", fill="#2C1B12", text_fill=WHITE, f=F["small"], icon_arrow=True)
arrow_next(d2, 740, 1140, color=INK, bg="dark")
footer(d2, "dark", "02/05", im2)
im2.save(OUT / "slide_02_formula.png")


# SLIDE 3 (NAVY - FIXED TEXT WRAP)
im3 = Image.new("RGB", (W,H), NAVY)
d3 = ImageDraw.Draw(im3)
starburst(d3, 84, 95, r=20, fill=ORANGE, width=10)
pill(d3, (820, 75), (175, 52), "naskah.fk", fill=NAVY, outline=CREAM, text_fill=CREAM, f=F["tiny"], stroke=3)
headline = ["SKALA", "DATA", "AMBIGU"]
y = 250
for i,line in enumerate(headline):
    d3.text((84, y+i*120), line, font=F["xxl"], fill=CREAM)
body = "Contoh klasik: menulis kepatuhan sebagai “baik / kurang”, tapi tidak menjelaskan cut-off score-nya dari mana."
draw_multiline(d3, (84, 710), wrap_text(d3, body, F["body"], 850), F["body"], fill=CREAM, spacing=48)
d3.text((84, 940), "Ini bikin dosen & pembaca bingung:", font=F["body2"], fill=CREAM)
# Orange highlight wrapped cleanly on 2 lines
q_lines = ["data kamu kategorik,", "ordinal, atau numerik?"]
draw_multiline(d3, (84, 1005), q_lines, F["m"], fill=ORANGE, spacing=54)
arrow_next(d3, 740, 1150, color=ORANGE, bg="dark")
footer(d3, "dark", "03/05", im3)
im3.save(OUT / "slide_03_skala.png")


# SLIDE 4 (CREAM QUOTE - FIXED OVAL OVER "BUKAN")
im4 = Image.new("RGB", (W,H), CREAM)
d4 = ImageDraw.Draw(im4)
diagonal_label(d4, "page four", 760, 78, angle=-16, fill=ORANGE, f=F["tiny"])
d4.line((915,115,1005,82), fill=ORANGE, width=8)
d4.polygon([(1005,82),(978,76),(992,104)], fill=ORANGE)
headline = ["KUESIONER", "BUKAN", "SEKADAR", "FORM"]
y = 190
for i,line in enumerate(headline):
    d4.text((84, y+i*112), line, font=F["xl"], fill=INK)
# BUKAN is the second line (i=1). y offset = y + 1*112 = y+112. Font size 92.
# Box wraps the second-line word with extra clearance on all sides.
marker_oval(d4, (55, y+96, 460, y+235), ORANGE, width=9)
body = "Kalau kamu membuat instrumen sendiri, dosen biasanya akan langsung tanya:"
draw_multiline(d4, (84, 690), wrap_text(d4, body, F["body2"], 850), F["body2"], fill=INK, spacing=44)
# Quote box
d4.rounded_rectangle((84, 820, 996, 975), radius=46, fill=CREAM, outline=INK, width=4)
d4.text((540, 898), "“Sudah uji validitas?”", font=F["m"], fill=ORANGE, anchor="mm")
draw_multiline(d4, (84, 1030), wrap_text(d4, "Kalau belum, jangan pura-pura instrumennya sudah aman di Bab 3.", F["body2"], 850), F["body2"], fill=INK, spacing=44)
footer(d4, "cream", "04/05", im4)
im4.save(OUT / "slide_04_kuesioner.png")


# SLIDE 5 (CTA - BALANCED HEADLINE)
im5 = Image.new("RGB", (W,H), CREAM)
d5 = ImageDraw.Draw(im5)
starburst(d5, 84, 95, r=22, fill=ORANGE, width=11)
headline = ["RAPIKAN DO", "SEBELUM", "MASUK RUANG", "SEMPRO"]
y = 190
for i,line in enumerate(headline):
    d5.text((84, y+i*110), line, font=F["xl"], fill=INK)
# Oval around SEMPRO
marker_oval(d5, (70, y+325, 530, y+440), ORANGE, width=10)
body = "Satu tabel yang rapi bisa menyelamatkan kamu dari revisi metodologi yang muter-muter."
draw_multiline(d5, (84, 740), wrap_text(d5, body, F["body"], 840), F["body"], fill=INK, spacing=48)
pill(d5, (84, 930), (520, 76), "Save buat checklist Bab 3", fill=INK, text_fill=WHITE, f=F["small"], icon_arrow=True)
d5.text((84, 1075), "Kalau lagi stuck di Bab 3, naskah.fk bisa bantu bedah alurnya.", font=F["small"], fill=MUTED)
footer(d5, "cream", "05/05", im5)
im5.save(OUT / "slide_05_cta.png")

print("FIXED EXPORT COMPLETE")
