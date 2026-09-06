"""
NASKAH.FK — PRODUCTION CAROUSEL RENDERER (V2 Locked Template — Fixed QC)
Fixes:
- Clean transparent logo mark (no box/badge on any slide, adapted colors on dark/orange)
- Marker oval drawn *around* text with proper vertical offset & padding (not strikethrough)
- Safe text wrapping on all body copy, callout quotes, and footers (no overflow)
- Proportional formula pill buttons with balanced whitespace
"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(r"D:/tm/06_Content")
LOGO_TRANSPARENT = BASE_DIR / "02_BRAND_ASSETS/logos/logo_cutouts_clean/official_logo_transparent.png"
LOGO_WHITE = BASE_DIR / "02_BRAND_ASSETS/logos/logo_cutouts_clean/official_logo_white.png"
FONT_DIR = BASE_DIR / "02_BRAND_ASSETS/fonts/Poppins"

W, H = 1080, 1350

# Palette
CREAM = "#F5F2EB"
NAVY = "#071726"
INK = "#0B131D"
ORANGE = "#E85929"
MUTED = "#55606E"
WHITE = "#FFFFFF"
TEAL = "#028090"
DARK_CARD = "#1C2A38"


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


F = {
    "title_masif": font("Poppins-ExtraBold.ttf", 90),
    "title_xl": font("Poppins-ExtraBold.ttf", 78),
    "title_l": font("Poppins-Bold.ttf", 62),
    "quote_l": font("Poppins-Bold.ttf", 40),
    "quote_m": font("Poppins-Bold.ttf", 36),
    "body_lg": font("Poppins-Regular.ttf", 32),
    "body_med": font("Poppins-Medium.ttf", 28),
    "pill_text": font("Poppins-SemiBold.ttf", 25),
    "footer_brand": font("Poppins-SemiBold.ttf", 24),
    "footer_page": font("Poppins-Bold.ttf", 24),
}


def text_size(draw, text, f):
    box = draw.textbbox((0, 0), text, font=f)
    return (box[2] - box[0], box[3] - box[1])


def wrap_text(draw, text, f, max_w=900):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if text_size(draw, test, f)[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def load_logos():
    raw = Image.open(LOGO_TRANSPARENT).convert("RGBA")
    white = Image.open(LOGO_WHITE).convert("RGBA")
    return raw, white


def draw_header_logo(slide_img, raw_logo, white_logo, bg_type="cream", height=60, x=90, y=85):
    """Place official logo mark transparently in top-left without any bounding badge/box."""
    if bg_type == "cream":
        mark_src = raw_logo
    elif bg_type == "navy":
        mark_src = white_logo
    elif bg_type == "orange":
        mark_src = white_logo
    else:
        mark_src = raw_logo

    aspect = mark_src.width / mark_src.height
    w_ = int(height * aspect)
    mark = mark_src.resize((w_, height), Image.Resampling.LANCZOS)
    slide_img.paste(mark, (x, y), mark)


def draw_footer(draw, page_num, bg_type="cream"):
    c = INK if bg_type == "cream" else CREAM
    draw.text((90, 1235), "naskah.fk", font=F["footer_brand"], fill=c, anchor="ls")
    draw.text((990, 1235), f"{page_num:02d}/05", font=F["footer_page"], fill=c, anchor="rs")


def marker_oval_around(draw, text_origin, text_str, font_obj, color=ORANGE, pad_x=45, pad_y=22, stroke=8):
    """Draw an organic capsule around a wide text line without crossing its glyphs."""
    tx, ty = text_origin
    box = draw.textbbox((tx, ty), text_str, font=font_obj)
    x1 = box[0] - pad_x
    y1 = box[1] - pad_y
    x2 = box[2] + pad_x
    y2 = box[3] + pad_y

    # Two loose horizontal marker strokes keep the center clear of the letters.
    mid_x = (x1 + x2) / 2
    draw.line(
        [(x1 + pad_y * 0.7, y1 + 3), (mid_x, y1), (x2 - pad_y * 0.5, y1 + 3)],
        fill=color, width=stroke, joint="curve"
    )
    draw.line(
        [(x2 - pad_y * 0.5, y2 - 2), (mid_x, y2 + 3), (x1 + pad_y * 0.6, y2 - 2)],
        fill=color, width=stroke, joint="curve"
    )

    # Rounded end caps, plus a tiny hand-drawn tail on the lower-right.
    r = (y2 - y1) / 2
    draw.arc((x1, y1, x1 + 2 * r, y2), start=90, end=270, fill=color, width=stroke)
    draw.arc((x2 - 2 * r, y1, x2, y2), start=270, end=90, fill=color, width=stroke)
    draw.line([(x2 - r * 0.45, y2 + 2), (x2 + 10, y2 - 8)], fill=color, width=max(3, stroke - 2))


def pill_button(draw, xy, wh, text, fill, text_fill=WHITE, outline=None, stroke=3, icon_arrow=False):
    x, y = xy
    w, h = wh
    draw.rounded_rectangle((x, y, x + w, y + h), radius=h // 2, fill=fill, outline=outline, width=stroke)
    ty = y + h // 2
    if icon_arrow:
        ax = x + 38
        draw.line((ax - 7, ty + 5, ax + 7, ty - 5), fill=text_fill, width=3)
        draw.line((ax, ty - 5, ax + 7, ty - 5), fill=text_fill, width=3)
        draw.line((ax + 7, ty - 5, ax + 7, ty + 2), fill=text_fill, width=3)
        draw.text((x + 64, ty), text, font=F["pill_text"], fill=text_fill, anchor="lm")
    else:
        draw.text((x + w // 2, ty), text, font=F["pill_text"], fill=text_fill, anchor="mm")


def render_cover(raw_logo, white_logo, t):
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    draw_header_logo(im, raw_logo, white_logo, "cream")

    y = 230
    for i, line in enumerate(t["cover"]["headline"]):
        pos = (90, y + i * 102)
        d.text(pos, line, font=F["title_masif"], fill=INK)
        if i == t["cover"].get("mark_word_line"):
            marker_oval_around(d, pos, line, F["title_masif"], color=ORANGE, pad_x=26, pad_y=16, stroke=9)

    by = 730
    for i, line in enumerate(wrap_text(d, t["cover"]["body"], F["body_lg"], 860)):
        d.text((90, by + i * 48), line, font=F["body_lg"], fill=INK)

    pill_button(d, (90, 930), (320, 68), t["cover"]["pill"], fill=CREAM, outline=INK, text_fill=INK, stroke=4)
    draw_footer(d, 1, "cream")
    return im


def render_formula(raw_logo, white_logo, t):
    im = Image.new("RGB", (W, H), ORANGE)
    d = ImageDraw.Draw(im)
    draw_header_logo(im, raw_logo, white_logo, "orange")

    y = 230
    hd = t["formula"]["headline"]
    for i, line in enumerate(hd):
        d.text((90, y + i * 96), line, font=F["title_xl"], fill=INK)

    by = 550
    for i, line in enumerate(wrap_text(d, t["formula"]["body"], F["body_lg"], 880)):
        d.text((90, by + i * 46), line, font=F["body_lg"], fill=INK)

    fy = 780
    pills = t["formula"]["pills"]
    # Row 1: Two parallel pills with balanced spacing
    p1, p2 = pills[0], pills[1]
    pill_button(d, (90, fy), (435, 78), p1, fill=INK, text_fill=WHITE)
    pill_button(d, (555, fy), (435, 78), p2, fill=INK, text_fill=WHITE)

    # Row 2: Result pill
    rp = pills[2]
    pill_button(d, (90, fy + 104), (900, 84), rp, fill="#1F1109", text_fill=WHITE)

    draw_footer(d, 2, "orange")
    return im


def render_editorial(raw_logo, white_logo, t):
    im = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(im)
    draw_header_logo(im, raw_logo, white_logo, "navy")

    y = 240
    for i, line in enumerate(t["editorial"]["headline"]):
        d.text((90, y + i * 102), line, font=F["title_masif"], fill=CREAM)

    by = 640
    for i, line in enumerate(wrap_text(d, t["editorial"]["body"], F["body_lg"], 880)):
        d.text((90, by + i * 48), line, font=F["body_lg"], fill=CREAM)

    dy = by + len(wrap_text(d, t["editorial"]["body"], F["body_lg"], 880)) * 48 + 36
    if "lead" in t["editorial"]:
        d.text((90, dy), t["editorial"]["lead"], font=F["body_med"], fill="#9EB3C7")
        dy += 54

    ql = t["editorial"]["quote"]
    for q_line in ql:
        d.text((90, dy), q_line, font=F["quote_l"], fill=ORANGE)
        dy += 54

    draw_footer(d, 3, "navy")
    return im


def render_callout(raw_logo, white_logo, t):
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    draw_header_logo(im, raw_logo, white_logo, "cream")

    y = 230
    for i, line in enumerate(t["callout"]["headline"]):
        pos = (90, y + i * 96)
        d.text(pos, line, font=F["title_xl"], fill=INK)
        if i == t["callout"].get("mark_word_line"):
            marker_oval_around(d, pos, line, F["title_xl"], color=ORANGE, pad_x=24, pad_y=14, stroke=8)

    by = 650
    d.text((90, by), t["callout"]["lead"], font=F["body_med"], fill=INK)

    # Wrap quote inside callout box
    q_lines = wrap_text(d, t["callout"]["quote"], F["quote_m"], max_w=820)
    box_h = 48 + len(q_lines) * 52 + 20
    box_y = by + 50
    d.rounded_rectangle((90, box_y, 990, box_y + box_h), radius=32, fill=CREAM, outline=INK, width=4)

    for i, ql in enumerate(q_lines):
        d.text((540, box_y + 36 + i * 52), ql, font=F["quote_m"], fill=ORANGE, anchor="mt")

    # Bottom explanatory text (wrapped properly to prevent overflow)
    fy = box_y + box_h + 36
    for i, line in enumerate(wrap_text(d, t["callout"]["foot"], F["body_med"], max_w=900)):
        d.text((90, fy + i * 42), line, font=F["body_med"], fill=INK)

    draw_footer(d, 4, "cream")
    return im


def render_cta(raw_logo, white_logo, t):
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    draw_header_logo(im, raw_logo, white_logo, "cream")

    y = 230
    for i, line in enumerate(t["cta"]["headline"]):
        pos = (90, y + i * 96)
        d.text(pos, line, font=F["title_xl"], fill=INK)
        if i == t["cta"].get("mark_word_line"):
            marker_oval_around(d, pos, line, F["title_xl"], color=ORANGE, pad_x=24, pad_y=14, stroke=8)

    by = 680
    for i, line in enumerate(wrap_text(d, t["cta"]["body"], F["body_lg"], 860)):
        d.text((90, by + i * 48), line, font=F["body_lg"], fill=INK)

    pill_button(d, (90, 890), (480, 74), t["cta"]["pill"], fill=INK, text_fill=WHITE, icon_arrow=True)

    fy = 1010
    for i, line in enumerate(wrap_text(d, t["cta"]["foot"], F["body_med"], max_w=860)):
        d.text((90, fy + i * 42), line, font=F["body_med"], fill=MUTED)

    draw_footer(d, 5, "cream")
    return im


def render(cfg, out_dir, name="carousel"):
    raw_logo, white_logo = load_logos()
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    slides = {
        "01_cover": render_cover(raw_logo, white_logo, cfg),
        "02_formula": render_formula(raw_logo, white_logo, cfg),
        "03_editorial": render_editorial(raw_logo, white_logo, cfg),
        "04_callout": render_callout(raw_logo, white_logo, cfg),
        "05_cta": render_cta(raw_logo, white_logo, cfg),
    }
    for k, im in slides.items():
        im.save(out_dir / f"{name}_{k}.png")
    return out_dir, slides


if __name__ == "__main__":
    topic_file = Path(sys.argv[1])
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else BASE_DIR / "05_OUTPUTS"
    name = sys.argv[3] if len(sys.argv) > 3 else "carousel"
    cfg = json.loads(topic_file.read_text(encoding="utf-8"))
    out_dir, _ = render(cfg, out_dir, name=name)
    print("RENDERED TO:", out_dir)
