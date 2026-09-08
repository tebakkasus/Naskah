"""
Render script for W1-05: REVISI BINGO (Single Post / Story Template).
Follows Naskah Locked V2 Template System:
- Palette: Cream #F5F2EB, Navy #071726, Orange #E85929, Ink #0B131D, White #FFFFFF
- Logo in top-left
- 5x5 Bingo Grid with Free Space in the center
- Clean Poppins typography
- Emoji rendered as downloaded PNG assets (never tofu)
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from emoji_assets import paste_emoji, strip_emojis

BASE_DIR = Path(r"D:/tm/06_Content")
LOGO_TRANSPARENT = BASE_DIR / "02_BRAND_ASSETS/logos/logo_cutouts_clean/official_logo_transparent.png"
FONT_DIR = BASE_DIR / "02_BRAND_ASSETS/fonts/Poppins"
OUT_DIR = BASE_DIR / "06_CONTENT_PIPELINE/03_APPROVED/post_w1_05_revisi_bingo"

W, H = 1080, 1350

CREAM = "#F5F2EB"
NAVY = "#071726"
INK = "#0B131D"
ORANGE = "#E85929"
MUTED = "#55606E"
WHITE = "#FFFFFF"
CARD_BG = "#EAE5DA"
FREE_BG = "#FFE8DE"

def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)

F = {
    "title_main": font("Poppins-ExtraBold.ttf", 52),
    "subtitle": font("Poppins-SemiBold.ttf", 24),
    "cell_bold": font("Poppins-Bold.ttf", 20),
    "cell_regular": font("Poppins-Medium.ttf", 18),
    "free_title": font("Poppins-ExtraBold.ttf", 22),
    "free_sub": font("Poppins-Bold.ttf", 18),
    "footer_brand": font("Poppins-SemiBold.ttf", 22),
    "footer_tag": font("Poppins-Bold.ttf", 22),
}

BINGO_GRID = [
    ['"Revisinya\ndikit kok"', '"Ini kayak\nlaporan\nwartawan"', '"Coba cari\njurnal\nterbaru"', '"P-value lo\ngak bener?"', '"Kenapa\ngak pake\nSPSS?"'],
    ['"Cek referensi\ndari tahun\n2000-an"', '"Ini terlalu\npanjang"', '"Metode lo\nkurang kuat"', '"Coba baca\nulang buku\nmetpen"', '"Pernah\nbaca jurnal\nkan?"'],
    ['"Ini bukan\nliterature\nreview"', '"Sample size\nkurang"', 'FREE_SPACE', '"Hipotesis lo\nterlalu\nluas"', '"Udah revisi\nkok tinggal\ndikit lagi"'],
    ['"Kata siapa?\nSumber?"', '"Lo yakin ini\ncross-\nsectional?"', '"Ini\nplagiarism\nchecker-nya\nberapa?"', '"Variabel lo\nterlalu\nbanyak"', '"Coba\nkonsultasi\nsama\nstatistisi"'],
    ['"Formatting\nlo berantakan"', '"Lo ngerti\nnggak ini\nartinya apa?"', '"Saya nggak\nbilang salah,\ntapi..."', '"Ulangi dari\nBab 1"', '"Kirim revisi\nminggu\ndepan ya"']
]

def render_bingo():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)

    # Logo Top-Left
    if LOGO_TRANSPARENT.exists():
        raw_logo = Image.open(LOGO_TRANSPARENT).convert("RGBA")
        aspect = raw_logo.width / raw_logo.height
        h_logo = 55
        w_logo = int(h_logo * aspect)
        mark = raw_logo.resize((w_logo, h_logo), Image.Resampling.LANCZOS)
        im.paste(mark, (90, 75), mark)

    # Header Text — paste 🎯 PNG on the left, then title text
    paste_emoji(im, "🎯", (90, 152), size=58, anchor="la")
    d.text((165, 150), "REVISI BINGO", font=F["title_main"], fill=INK)
    d.text((90, 222), "Edisi Dosen Pembimbing • Screenshot & Tandain!", font=F["subtitle"], fill=ORANGE)

    # Grid Setup (5x5)
    margin_x = 90
    grid_w = W - (2 * margin_x) # 900
    grid_y = 280
    grid_h = 880
    cell_w = grid_w / 5 # 180
    cell_h = grid_h / 5 # 176
    gap = 8

    for r in range(5):
        for c in range(5):
            cx = margin_x + c * cell_w
            cy = grid_y + r * cell_h
            
            box_x1 = cx + gap / 2
            box_y1 = cy + gap / 2
            box_x2 = cx + cell_w - gap / 2
            box_y2 = cy + cell_h - gap / 2

            content = BINGO_GRID[r][c]

            if content == 'FREE_SPACE':
                # Center Free Space
                d.rounded_rectangle((box_x1, box_y1, box_x2, box_y2), radius=16, fill=FREE_BG, outline=ORANGE, width=3)
                d.text(((box_x1 + box_x2)/2, (box_y1 + box_y2)/2 - 20), "FREE SPACE", font=F["free_title"], fill=ORANGE, anchor="mm")
                d.text(((box_x1 + box_x2)/2, (box_y1 + box_y2)/2 + 16), '"Bagus, tapi..."', font=F["free_sub"], fill=INK, anchor="mm")
            else:
                # Normal Cell
                d.rounded_rectangle((box_x1, box_y1, box_x2, box_y2), radius=16, fill=WHITE, outline=NAVY, width=2)
                lines = content.split('\n')
                total_lines = len(lines)
                line_h = 24
                start_ty = ((box_y1 + box_y2)/2) - ((total_lines - 1) * line_h / 2)
                for idx_l, line in enumerate(lines):
                    d.text(((box_x1 + box_x2)/2, start_ty + idx_l * line_h), line, font=F["cell_regular"], fill=INK, anchor="mm")

    # Instruction Bar / Soft CTA
    d.rounded_rectangle((90, 1180, 990, 1235), radius=28, fill=NAVY)
    d.text((500, 1208), "Tag @naskah.fk di Story lo kalau lo dapet 5 berturut-turut!", font=F["subtitle"], fill=WHITE, anchor="mm")
    paste_emoji(im, "🔥", (890, 1208), size=34, anchor="mm")

    # Footer
    d.text((90, 1280), "naskah.fk", font=F["footer_brand"], fill=INK)
    d.text((990, 1280), "#RevisiBingo", font=F["footer_tag"], fill=ORANGE, anchor="ra")

    # Save
    out_path = OUT_DIR / "post_w1_05_revisi_bingo.jpg"
    im.save(out_path, "JPEG", quality=95)
    print(f"BINGO RENDERED TO: {out_path}")

if __name__ == "__main__":
    render_bingo()
