from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import sys

def make_preview_sheet(src_dir, title, subtitle, out_file, name_prefix="post"):
    src_dir = Path(src_dir)
    out_file = Path(out_file)
    font_dir = Path(r"D:/tm/06_Content/02_BRAND_ASSETS/fonts/Poppins")
    
    files = [
        f"{name_prefix}_01_cover.png",
        f"{name_prefix}_02_formula.png",
        f"{name_prefix}_03_editorial.png",
        f"{name_prefix}_04_callout.png",
        f"{name_prefix}_05_cta.png",
    ]
    
    thumb_w, thumb_h = 300, 375
    margin = 48
    gap = 22
    header_h = 125
    canvas_w = margin * 2 + len(files) * thumb_w + (len(files) - 1) * gap
    canvas_h = header_h + margin + thumb_h + 90
    
    board = Image.new("RGB", (canvas_w, canvas_h), "#06121E")
    d = ImageDraw.Draw(board)
    ft = ImageFont.truetype(str(font_dir / "Poppins-ExtraBold.ttf"), 34)
    fs = ImageFont.truetype(str(font_dir / "Poppins-Medium.ttf"), 18)
    fc = ImageFont.truetype(str(font_dir / "Poppins-SemiBold.ttf"), 20)
    
    d.text((canvas_w // 2, 38), title, font=ft, fill="#F5F2EB", anchor="ma")
    d.text((canvas_w // 2, 82), subtitle, font=fs, fill="#E85929", anchor="ma")
    
    for i, name in enumerate(files):
        im_p = src_dir / name
        if im_p.exists():
            im = Image.open(im_p).convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            x = margin + i * (thumb_w + gap)
            y = header_h
            board.paste(im, (x, y))
            d.text((x + thumb_w // 2, y + thumb_h + 30), f"{i+1:02d}/05", font=fc, fill="#F5F2EB", anchor="ma")
    
    board.save(out_file, quality=95)
    print("Saved preview:", out_file)

if __name__ == "__main__":
    src = sys.argv[1]
    title = sys.argv[2]
    subtitle = sys.argv[3]
    out = sys.argv[4]
    pfx = sys.argv[5] if len(sys.argv) > 5 else "post"
    make_preview_sheet(src, title, subtitle, out, pfx)
