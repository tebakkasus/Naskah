from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/naskah-visuals/logo_exploration_v2")
FONT_DIR = Path(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/fonts/Poppins")

NAVY = "#071726"
CREAM = "#F5F2EB"
ORANGE = "#E85929"

ft = ImageFont.truetype(str(FONT_DIR/"Poppins-ExtraBold.ttf"), 70)
fsub = ImageFont.truetype(str(FONT_DIR/"Poppins-Medium.ttf"), 32)
flabel = ImageFont.truetype(str(FONT_DIR/"Poppins-Bold.ttf"), 40)
fdesc = ImageFont.truetype(str(FONT_DIR/"Poppins-Regular.ttf"), 26)

BW, BH = 2200, 1500
board = Image.new("RGB", (BW, BH), "#06121E")
d = ImageDraw.Draw(board)
d.text((1100, 70), "TOP 4 — N MONOGRAM DIRECTION", font=ft, fill=CREAM, anchor="ma")
d.text((1100, 150), "four fundamentally different routes • simple • one letter • memorable", font=fsub, fill=ORANGE, anchor="ma")

cards = [
    ("concept_11_page_cut_navy.png", "11 · Page Cut", "N bold + satu sudut potongan halaman. Paling bersih & mudah dibaca di semua ukuran."),
    ("concept_04_margin_rule_navy.png", "04 · Margin Rule", "Garis tepi editorial. Terasa seperti manuskrip & margin jurnal. Paling akademis."),
    ("concept_01_page_fold_navy.png", "01 · Page Fold", "N dengan lipatan pojok halaman. Simpel, jelas, kuat sebagai avatar."),
    ("concept_02_negative_window_navy.png", "02 · Negative Window", "N muncul sebagai ruang kosong di dalam kotak. Paling siap jadi app icon."),
]

x0 = 90
for filename, label, desc in cards:
    img = Image.open(OUT/filename).resize((470, 470), Image.Resampling.LANCZOS)
    # tile
    d.rounded_rectangle((x0, 240, x0+470, 710), radius=20, fill=CREAM)
    board.paste(img, (x0, 240))
    d.text((x0, 760), label, font=flabel, fill=CREAM)
    # wrap desc
    words = desc.split(); cur=""; lines=[]
    for w in words:
        test=(cur+" "+w).strip()
        if d.textbbox((0,0),test,font=fdesc)[2] <= 470:
            cur=test
        else:
            lines.append(cur); cur=w
    if cur: lines.append(cur)
    for i,ln in enumerate(lines):
        d.text((x0, 830+i*44), ln, font=fdesc, fill="#A7B2BD")
    d.text((x0, 1010), "render PNG", font=fdesc, fill=ORANGE)
    x0 += 520

board.save(OUT/"TOP4_N_MONOGRAM_DIRECTIONS.png", quality=95)
print("TOP4 board saved")
