from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/naskah-visuals/logo_concepts")
FONT_DIR = Path(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/fonts/Poppins")

f_title = ImageFont.truetype(str(FONT_DIR / "Poppins-Bold.ttf"), 38)
f_sub = ImageFont.truetype(str(FONT_DIR / "Poppins-Regular.ttf"), 24)

# Create a 2x2 grid showcase image
GRID_W, GRID_H = 2100, 2200
board = Image.new("RGB", (GRID_W, GRID_H), "#050F1A")
d = ImageDraw.Draw(board)

# Header
d.text((1050, 80), "NASKAH.FK — LOGO EXPLORATION", font=ImageFont.truetype(str(FONT_DIR / "Poppins-ExtraBold.ttf"), 54), fill="#F5F2EB", anchor="mt")
d.text((1050, 150), "Single-Letter 'N' Monogram Concepts | Simple • Memorable • Scalable", font=ImageFont.truetype(str(FONT_DIR / "Poppins-Medium.ttf"), 28), fill="#E85929", anchor="mt")

logos = [
    ("logo_c1_bookmark_navy.png", "Opsi 1: The Bookmark Ribbon N", "Pilar kanan dengan potongan ribbon pembatas buku. Sangat kuat nuansa akademiknya.", (80, 240)),
    ("logo_c2_monolith_navy.png", "Opsi 2: The Monolith Dot N", "Dua pilar geometris + diagonal tajam + spark dot di kanan atas (seperti Linear/Notion).", (1080, 240)),
    ("logo_c3_ribbon_navy.png", "Opsi 3: The Connected Node N", "Diagonal oranye dengan joint melingkar sebagai jembatan / koneksi ide riset.", (80, 1200)),
    ("logo_c4_bold_navy.png", "Opsi 4: The Research Stylus N", "Bentuk N tegas berarsitektur kokoh + aksen pena/tinta oranye di sudut atas.", (1080, 1200)),
]

for filename, title, desc, (x, y) in logos:
    img = Image.open(OUT / filename).resize((900, 700), Image.Resampling.LANCZOS)
    board.paste(img, (x+20, y+20))
    d.text((x+470, y+740), title, font=f_title, fill="#F5F2EB", anchor="mt")
    d.text((x+470, y+795), desc, font=f_sub, fill="#9CA8B4", anchor="mt")

board.save(OUT / "LOGO_SELECTION_BOARD.png", quality=95)
print("Board created.")
