from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

SRC = Path(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/naskah-visuals/test_carousel_v2_refined")
OUT = SRC / "CAROUSEL_V2_REFINED_PREVIEW.png"
FONT_DIR = Path(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/fonts/Poppins")

files = [
    "slide_01_cover.png",
    "slide_02_formula.png",
    "slide_03_skala.png",
    "slide_04_kuesioner.png",
    "slide_05_cta.png",
]

thumb_w, thumb_h = 300, 375
margin = 48
gap = 22
header_h = 125
canvas_w = margin*2 + len(files)*thumb_w + (len(files)-1)*gap
canvas_h = header_h + margin + thumb_h + 90

board = Image.new("RGB", (canvas_w, canvas_h), "#06121E")
d = ImageDraw.Draw(board)
ft = ImageFont.truetype(str(FONT_DIR / "Poppins-ExtraBold.ttf"), 34)
fs = ImageFont.truetype(str(FONT_DIR / "Poppins-Medium.ttf"), 18)
fc = ImageFont.truetype(str(FONT_DIR / "Poppins-SemiBold.ttf"), 20)

d.text((canvas_w//2, 38), "NASKAH.FK — CAROUSEL V2 REFINED", font=ft, fill="#F5F2EB", anchor="ma")
d.text((canvas_w//2, 82), "Poppins • official N mark • consistent whitespace • no page labels", font=fs, fill="#E85929", anchor="ma")

for i, name in enumerate(files):
    im = Image.open(SRC / name).convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    x = margin + i*(thumb_w+gap)
    y = header_h
    board.paste(im, (x,y))
    d.text((x+thumb_w//2, y+thumb_h+30), f"{i+1:02d}/05", font=fc, fill="#F5F2EB", anchor="ma")

board.save(OUT, quality=95)
print(OUT)
