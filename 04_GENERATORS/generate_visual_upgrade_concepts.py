"""
Naskah Visual Upgrade Concepts — 2026 Design Trends Applied.

Based on research:
- Digital Synopsis "Top 20 Graphic Design Trends For 2026"
  (Gradients & Blends #17, Bold Minimalism #13, Bento Grid Layouts #4)
- UX Pilot "12 Product Design Trends for 2026"
  (Light Skeuomorphism #10 — soft shadows, delicate gradients, raised surfaces;
   Bento box design #6 — modular clarity)

These are CONCEPT exploration renders, NOT replacements for the Locked V2 Template.
Goal: prove that soft shadows, gradients, bento layout and elevation add depth
while keeping the Naskah palette (cream/navy/orange) and Poppins typography.
"""
from __future__ import annotations

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE_DIR = Path(r"D:/tm/06_Content")
FONT_DIR = BASE_DIR / "02_BRAND_ASSETS/fonts/Poppins"
LOGO_TRANSPARENT = BASE_DIR / "02_BRAND_ASSETS/logos/logo_cutouts_clean/official_logo_transparent.png"
OUT_DIR = BASE_DIR / "05_OUTPUTS/concept_upgrade_2026"

W, H = 1080, 1350

CREAM = "#F5F2EB"
NAVY = "#071726"
INK = "#0B131D"
ORANGE = "#E85929"
ORANGE_DARK = "#D04A1F"
TEAL = "#028090"
MUTED = "#55606E"
WHITE = "#FFFFFF"


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


F = {
    "title_masif": font("Poppins-ExtraBold.ttf", 78),
    "title_l": font("Poppins-Bold.ttf", 58),
    "title_m": font("Poppins-Bold.ttf", 34),
    "body": font("Poppins-Medium.ttf", 26),
    "pill": font("Poppins-SemiBold.ttf", 22),
    "small": font("Poppins-Medium.ttf", 20),
    "brand": font("Poppins-SemiBold.ttf", 22),
}


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient_vertical(im: Image.Image, top: str, bottom: str, x0=0, y0=0, x1=None, y1=None):
    """Draw a vertical gradient overlay across a region."""
    d = ImageDraw.Draw(im)
    x1 = x1 if x1 is not None else im.width
    y1 = y1 if y1 is not None else im.height
    top_rgb, bot_rgb = hex_to_rgb(top), hex_to_rgb(bottom)
    for y in range(y0, y1):
        t = (y - y0) / max(1, (y1 - y0 - 1))
        color = lerp(top_rgb, bot_rgb, t)
        d.line([(x0, y), (x1, y)], fill=color)


def rounded_rectangle_gradient(im, box, radius, top, bottom):
    """Draw a rounded rectangle with vertical gradient fill."""
    x1, y1, x2, y2 = box
    mask = Image.new("L", (im.width, im.height), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle(box, radius=radius, fill=255)
    grad = Image.new("RGB", (im.width, im.height))
    gradient_vertical(grad, top, bottom, x0=x1, y0=y1, x1=x2, y1=y2)
    im.paste(grad, (0, 0), mask)


def soft_shadow_card(im, box, radius, alpha=70, blur=28, offset=(0, 14), color=(7, 23, 38)):
    """Draw a soft drop shadow under a rounded-rect card."""
    x1, y1, x2, y2 = box
    shadow = Image.new("RGBA", (im.width, im.height), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle(
        (x1 + offset[0], y1 + offset[1], x2 + offset[0], y2 + offset[1]),
        radius=radius, fill=color + (alpha,),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    im.paste(Image.alpha_composite(im.convert("RGBA"), shadow).convert("RGB"), (0, 0))
    return im


def paste_logo(im, x=90, y=70, h=60):
    if LOGO_TRANSPARENT.exists():
        logo = Image.open(LOGO_TRANSPARENT).convert("RGBA")
        aspect = logo.width / logo.height
        w = int(h * aspect)
        logo = logo.resize((w, h), Image.Resampling.LANCZOS)
        im.paste(logo, (90, y), logo)


def footer(im, page="01/05", brand="naskah.fk", dark=False):
    d = ImageDraw.Draw(im)
    c = CREAM if dark else INK
    d.text((90, H - 80), brand, font=F["brand"], fill=c)
    d.text((W - 90, H - 80), page, font=F["brand"], fill=c, anchor="ra")


def concept_1_cover_gradient():
    """Concept 01: Cover with soft warm gradient + bold minimal type."""
    im = Image.new("RGB", (W, H), CREAM)
    # Warm cream-to-peach gradient overlay
    gradient_vertical(im, "#FDFBF6", "#F3DCCB")
    d = ImageDraw.Draw(im)

    paste_logo(im)

    # Soft shadowed orange blob accent (organic)
    blob = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(blob)
    bd.ellipse((640, 200, 1000, 520), fill=(232, 89, 41, 130))
    blob = blob.filter(ImageFilter.GaussianBlur(60))
    im.paste(Image.alpha_composite(im.convert("RGBA"), blob).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(im)

    d.text((90, 240), "SKRIPSI", font=F["title_masif"], fill=INK)
    d.text((90, 340), "Lo Sakit.", font=F["title_masif"], fill=INK)

    # Bento card with soft shadow + gradient
    card_box = (90, 880, 990, 1160)
    im = soft_shadow_card(im, card_box, radius=36, alpha=60, blur=26)
    rounded_rectangle_gradient(im, card_box, 36, "#FFFFFF", "#F6E9DD")
    d = ImageDraw.Draw(im)
    d.text((130, 920), "ICD-10 Edisi Akademik", font=F["title_m"], fill=NAVY)
    d.text((130, 980), "Diagnosis Penyakit Skripsi", font=F["small"], fill=MUTED)
    # small pill
    d.rounded_rectangle((130, 1060, 420, 1110), radius=25, fill=ORANGE)
    d.text((275, 1085), "Baca Diagnosis", font=F["pill"], fill=WHITE, anchor="mm")

    footer(im, "01/05")
    return im


def concept_2_bento_grid():
    """Concept 02: Bento grid layout with layered elevation + soft shadows."""
    im = Image.new("RGB", (W, H), CREAM)
    gradient_vertical(im, "#FDFBF6", "#EFF3F0")
    paste_logo(im)
    d = ImageDraw.Draw(im)

    d.text((90, 220), "Racikan Tools Naskah", font=F["title_l"], fill=NAVY)

    # Bento grid (4 cards) with different sizes, soft shadows
    cards = [
        # (box, fill_top, fill_bottom, title, sub, dark_text)
        ((90, 360, 620, 700), "#FFFFFF", "#F3E9DF", "Literature Review", "Cari jurnal • Sintesis", False),
        ((640, 360, 990, 700), "#071726", "#1F3648", "Analisis Data", "SPSS • Metode", True),
        ((90, 720, 500, 1060), "#E85929", "#C84820", "Statistik [POC]", "OR • RR • p-value", True),
        ((520, 720, 990, 1060), "#FFFFFF", "#FFFFFF", "Penulisan", "Word • Sitasi • Draft", False),
    ]
    for box, top, bot, title, sub, dark in cards:
        im = soft_shadow_card(im, box, radius=30, alpha=55, blur=24, offset=(0, 12))
        rounded_rectangle_gradient(im, box, 30, top, bot)
        d = ImageDraw.Draw(im)
        c = CREAM if dark else NAVY
        d.text((box[0] + 28, box[1] + 30), title, font=F["title_m"], fill=c)
        d.text((box[0] + 28, box[1] + 88), sub, font=F["small"], fill=(CREAM if dark else MUTED))

    footer(im, "02/05")
    return im


def concept_3_glass_panel():
    """Concept 03: Glassmorphism 2.0 subtle — frosted panel with high-contrast text."""
    im = Image.new("RGB", (W, H), NAVY)
    # Deep navy gradient with soft color blobs (glass-like ambient)
    gradient_vertical(im, "#071726", "#12304A")
    blob1 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(blob1)
    bd.ellipse((60, 120, 520, 640), fill=(232, 89, 41, 160))
    bd.ellipse((620, 400, 1020, 900), fill=(2, 128, 144, 130))
    blob1 = blob1.filter(ImageFilter.GaussianBlur(90))
    im.paste(Image.alpha_composite(im.convert("RGBA"), blob1).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(im)

    paste_logo(im, y=70, h=60)

    d.text((90, 300), "Gelisah di", font=F["title_masif"], fill=CREAM)
    d.text((90, 400), "Depan SPSS.", font=F["title_masif"], fill=CREAM)

    # Frosted panel: semi-transparent white over blur. Simulate with translucent white
    panel_box = (90, 760, 990, 1080)
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle(panel_box, radius=34, fill=(255, 255, 255, 60))
    im = Image.alpha_composite(im.convert("RGBA"), panel).convert("RGB")
    d = ImageDraw.Draw(im)
    # Thin glass border
    d.rounded_rectangle(panel_box, radius=34, outline=(255, 255, 255, 110), width=2)
    d.text((130, 800), "P-value 0.06 bukan akhir dunia.", font=F["title_m"], fill=WHITE)
    d.text((130, 865), "Tapi awal dari pertanyaan baru.", font=F["small"], fill="#C9D8E4")

    footer(im, "03/05", dark=True)
    return im


def concept_4_marker_gradient_footer():
    """Concept 04: Callout with soft shadow + stacked pills + gradient accent."""
    im = Image.new("RGB", (W, H), CREAM)
    gradient_vertical(im, "#FDFBF6", "#F1E6DA")
    paste_logo(im)
    d = ImageDraw.Draw(im)

    d.text((90, 240), "Kata Dosen:", font=F["title_l"], fill=INK)

    # Callout card with soft shadow
    callout = (90, 400, 990, 800)
    im = soft_shadow_card(im, callout, radius=40, alpha=60, blur=30)
    rounded_rectangle_gradient(im, callout, 40, "#FFFFFF", "#FBF1E4")
    d = ImageDraw.Draw(im)
    quote = '"Bagus, tapi..."'
    d.text((540, 500), quote, font=font("Poppins-Bold.ttf", 56), fill=ORANGE, anchor="mm")
    d.text((540, 610), "3 kata yang bikin jantung berhenti.", font=F["small"], fill=MUTED, anchor="mm")

    # Stacked gradient pills (soft skeuomorphic)
    pills = [("Revisi Ringan", "#E85929", "#C84820"), ("Revisi Sedang", "#071726", "#1F3648"), ("Revisi Berat", "#F5B301", "#D99A00")]
    py = 870
    for label, top, bot in pills:
        pbox = (90, py, 500, py + 84)
        im = soft_shadow_card(im, pbox, radius=42, alpha=40, blur=18, offset=(0, 8))
        rounded_rectangle_gradient(im, pbox, 42, top, bot)
        d = ImageDraw.Draw(im)
        d.text((295, py + 42), label, font=F["pill"], fill=WHITE, anchor="mm")
        py += 106

    footer(im, "04/05")
    return im


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    renders = {
        "01_cover_gradient": concept_1_cover_gradient(),
        "02_bento_grid": concept_2_bento_grid(),
        "03_glass_panel": concept_3_glass_panel(),
        "04_marker_gradient_footer": concept_4_marker_gradient_footer(),
    }
    for name, im in renders.items():
        out = OUT_DIR / f"naskah_concept_{name}.jpg"
        im.convert("RGB").save(out, "JPEG", quality=94)
        print("SAVED:", out)


if __name__ == "__main__":
    main()