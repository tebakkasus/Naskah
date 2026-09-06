from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

OUT = Path(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/naskah-visuals/test_carousel_v1")
OUT.mkdir(parents=True, exist_ok=True)
FONT_DIR = Path(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/fonts")

W, H = 1080, 1350

# Palette adapted from the latest Canva template, Naskah-fk navy version
CREAM = "#F3F0E8"
NAVY = "#071B2D"
INK = "#09111C"
ORANGE = "#F05A28"
MUTED = "#4E5966"
WHITE = "#F7F4EE"

# Fonts
MONT_BLACK = FONT_DIR / "Montserrat-ExtraBold.ttf"
MONT_BOLD = FONT_DIR / "Montserrat-Bold.ttf"
MONT_SEMI = FONT_DIR / "Montserrat-SemiBold.ttf"
MONT_MED = FONT_DIR / "Montserrat-Medium.ttf"
MONT_REG = FONT_DIR / "Montserrat-Regular.ttf"
MONT_LIGHT = FONT_DIR / "Montserrat-Light.ttf"

def font(path, size):
    return ImageFont.truetype(str(path), size)

F = {
    "xxl": font(MONT_BLACK, 116),
    "xl": font(MONT_BLACK, 96),
    "l": font(MONT_BLACK, 78),
    "m": font(MONT_BOLD, 44),
    "body": font(MONT_REG, 35),
    "body2": font(MONT_MED, 32),
    "small": font(MONT_SEMI, 25),
    "tiny": font(MONT_MED, 20),
    "nav": font(MONT_BOLD, 28),
}

def text_size(draw, text, f):
    if not text:
        return (0,0)
    box = draw.textbbox((0,0), text, font=f)
    return (box[2]-box[0], box[3]-box[1])

def draw_multiline(draw, xy, lines, f, fill, leading=1.02, spacing=None, anchor=None):
    x, y = xy
    if isinstance(lines, str):
        lines = lines.split("\n")
    if spacing is None:
        spacing = int(f.size * leading)
    for i, line in enumerate(lines):
        draw.text((x, y + i*spacing), line, font=f, fill=fill, anchor=anchor)

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

def pill(draw, xy, wh, text, fill, outline=None, text_fill=WHITE, f=None, radius=999, stroke=3, icon=None):
    x,y = xy; w,h = wh
    draw.rounded_rectangle((x,y,x+w,y+h), radius=h//2 if radius==999 else radius, fill=fill, outline=outline, width=stroke)
    tx = x + w//2
    ty = y + h//2 - 1
    if icon:
        draw.text((x+30, ty), icon, font=f or F["small"], fill=text_fill, anchor="lm")
        draw.text((x+78, ty), text, font=f or F["small"], fill=text_fill, anchor="lm")
    else:
        draw.text((tx,ty), text, font=f or F["small"], fill=text_fill, anchor="mm")

def starburst(draw, cx, cy, r=17, fill=ORANGE, arms=8, width=10):
    for i in range(arms):
        angle = math.pi * 2 * i / arms
        x1 = cx + math.cos(angle)*5
        y1 = cy + math.sin(angle)*5
        x2 = cx + math.cos(angle)*r
        y2 = cy + math.sin(angle)*r
        draw.line((x1,y1,x2,y2), fill=fill, width=width)
    draw.ellipse((cx-6,cy-6,cx+6,cy+6), fill=fill)

def footer(draw, bg="cream", page="2026"):
    c = NAVY if bg == "cream" else CREAM
    acc = ORANGE
    starburst(draw, 80, 1235, r=15, fill=acc, width=8)
    draw.text((112, 1219), "naskah.fk", font=F["small"], fill=c)
    draw.text((960, 1219), page, font=F["small"], fill=c, anchor="ra")

def marker_oval(draw, bbox, color=ORANGE, width=8):
    # imperfect double-stroke oval
    x1,y1,x2,y2 = bbox
    draw.arc((x1,y1,x2,y2), start=5, end=360, fill=color, width=width)
    draw.arc((x1+7,y1+5,x2-4,y2+1), start=180, end=535, fill=color, width=width//2+2)

def arrow_next(draw, x, y, color=ORANGE, bg="cream"):
    # pill with arrow + next page label, inspired by template
    line = color
    draw.rounded_rectangle((x, y, x+150, y+54), radius=28, outline=line, width=4)
    draw.line((x+35, y+27, x+105, y+27), fill=line, width=7)
    draw.polygon([(x+105,y+14),(x+129,y+27),(x+105,y+40)], fill=line)
    tcol = NAVY if bg=="cream" else CREAM
    draw.text((x+172, y+10), "next page", font=F["tiny"], fill=tcol)

def diagonal_label(draw, text, x, y, angle=-12, fill=ORANGE, f=None):
    f = f or F["tiny"]
    tw, th = text_size(draw, text, f)
    im = Image.new("RGBA", (tw+20, th+20), (0,0,0,0))
    d = ImageDraw.Draw(im)
    d.text((10,10), text, font=f, fill=fill)
    rot = im.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    draw.bitmap((x,y), rot, fill=None)

# SLIDE 1: COVER
im = Image.new("RGB", (W,H), CREAM)
d = ImageDraw.Draw(im)
starburst(d, 86, 90, r=22, fill=ORANGE, width=11)
# headline lines
x=84; y=190
lines = ["BAB 3", "SERING", "DITOLAK", "DOSEN?"]
for i,line in enumerate(lines):
    d.text((x, y+i*112), line, font=F["xxl"], fill=INK)
# orange hand circle around DITOLAK
marker_oval(d, (70, y+220, 620, y+340), ORANGE, width=10)
body = "Masalahnya mungkin bukan idenya. Bisa jadi definisi operasionalmu belum sinkron."
draw_multiline(d, (88, 720), wrap_text(d, body, F["body"], 780), F["body"], fill=INK, spacing=48)
pill(d, (88, 910), (308, 64), "Swipe buat bedah", fill=CREAM, outline=INK, text_fill=INK, f=F["small"], stroke=4)
footer(d, "cream", "01/05")
im.save(OUT / "slide_01_cover.png", quality=95)

# SLIDE 2: ORANGE/DOUBLE PILL FORMULA
im = Image.new("RGB", (W,H), ORANGE)
d = ImageDraw.Draw(im)
starburst(d, 85, 86, r=20, fill=INK, width=10)
diagonal_label(d, "page two", 805, 80, angle=-18, fill=INK, f=F["tiny"])
# headline
headline = ["DEFINISI", "OPERASIONAL", "ITU BUKAN", "HIASAN"]
y = 190
for i,line in enumerate(headline):
    fs = F["xl"] if i < 2 else F["l"]
    d.text((82, y+i*98), line, font=fs, fill=INK)
body = "Di tabel DO, dosen mencari tiga hal: apa yang diukur, pakai alat apa, dan hasilnya masuk skala data apa."
draw_multiline(d, (88, 650), wrap_text(d, body, F["body2"], 820), F["body2"], fill=INK, spacing=44)
# formula pills
pill(d, (86, 860), (390, 76), "variabel jelas =", fill=INK, text_fill=WHITE, f=F["small"], icon="●")
pill(d, (505, 860), (360, 76), "uji statistik aman", fill=INK, text_fill=WHITE, f=F["small"])
pill(d, (230, 966), (585, 82), "lebih siap sempro", fill="#3A261A", text_fill=WHITE, f=F["small"], icon="↻")
arrow_next(d, 760, 1135, color=INK, bg="dark")
footer(d, "dark", "02/05")
im.save(OUT / "slide_02_formula.png", quality=95)

# SLIDE 3: BLACK/NAVY TYPO POSTER
im = Image.new("RGB", (W,H), NAVY)
d = ImageDraw.Draw(im)
starburst(d, 85, 86, r=20, fill=ORANGE, width=10)
# abstract N mark
pill(d, (835, 67), (165, 50), "naskah.fk", fill=NAVY, outline=CREAM, text_fill=CREAM, f=F["tiny"], stroke=3)
headline = ["SKALA", "DATA", "AMBIGU"]
y = 250
for i,line in enumerate(headline):
    d.text((82, y+i*120), line, font=F["xxl"], fill=CREAM)
body = "Contoh klasik: menulis kepatuhan sebagai “baik/kurang”, tapi tidak menjelaskan cut-off score-nya dari mana."
draw_multiline(d, (88, 720), wrap_text(d, body, F["body"], 835), F["body"], fill=CREAM, spacing=48)
d.text((88, 970), "Ini bikin pembaca tidak tahu:", font=F["body2"], fill=CREAM)
d.text((88, 1040), "data kamu kategorik, ordinal, atau numerik?", font=F["m"], fill=ORANGE)
arrow_next(d, 745, 1165, color=ORANGE, bg="dark")
im.save(OUT / "slide_03_skala.png", quality=95)

# SLIDE 4: CREAM WITH BIG QUOTE BOX
im = Image.new("RGB", (W,H), CREAM)
d = ImageDraw.Draw(im)
diagonal_label(d, "page four", 770, 74, angle=-16, fill=ORANGE, f=F["tiny"])
d.line((920,112,1010,80), fill=ORANGE, width=9)
d.polygon([(1010,80),(982,75),(996,102)], fill=ORANGE)
headline = ["KUESIONER", "BUKAN", "SEKADAR", "FORM"]
y = 180
for i,line in enumerate(headline):
    d.text((74, y+i*100), line, font=F["xl"], fill=INK)
marker_oval(d, (365, y+92, 715, y+205), ORANGE, width=9)
body = "Kalau kamu membuat instrumen sendiri, dosen biasanya akan tanya:"
draw_multiline(d, (84, 635), wrap_text(d, body, F["body2"], 850), F["body2"], fill=INK, spacing=44)
# quote box
box = (84, 785, 996, 940)
d.rounded_rectangle(box, radius=46, fill=CREAM, outline=INK, width=4)
d.text((540, 862), "“Sudah uji validitas?”", font=F["m"], fill=ORANGE, anchor="mm")
draw_multiline(d, (84, 1010), wrap_text(d, "Kalau belum, jangan pura-pura instrumennya sudah aman.", F["body2"], 850), F["body2"], fill=INK, spacing=44)
footer(d, "cream", "04/05")
im.save(OUT / "slide_04_kuesioner.png", quality=95)

# SLIDE 5: CTA / CLEAN CONCLUSION
im = Image.new("RGB", (W,H), CREAM)
d = ImageDraw.Draw(im)
starburst(d, 85, 86, r=20, fill=ORANGE, width=10)
headline = ["RAPIKAN", "DO SEBELUM", "MASUK", "RUANG", "SEMPRO"]
y=150
for i,line in enumerate(headline):
    fs = F["xl"] if i not in [3] else F["l"]
    d.text((80, y+i*98), line, font=fs, fill=INK)
marker_oval(d, (62, y+382, 640, y+500), ORANGE, width=9)
body = "Satu tabel yang rapi bisa menyelamatkan kamu dari revisi metodologi yang muter-muter."
draw_multiline(d, (84, 770), wrap_text(d, body, F["body"], 840), F["body"], fill=INK, spacing=48)
pill(d, (84, 965), (550, 72), "Save buat checklist Bab 3", fill=INK, text_fill=WHITE, f=F["small"], icon="↗")
d.text((84, 1105), "Kalau lagi stuck di Bab 3, naskah.fk bisa bantu bedah alurnya.", font=F["small"], fill=MUTED)
footer(d, "cream", "05/05")
im.save(OUT / "slide_05_cta.png", quality=95)

print(str(OUT))
for p in sorted(OUT.glob('*.png')):
    print(p.name)
