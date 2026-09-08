"""
Post 07 — Sunday Academic Reset
Re-rendered with 2026 Rich-Density Visual System.

5 Slides:
  1. Cover (Warm Cream gradient + marker highlight + emoji badge)
  2. Formula (Burnt Orange solid + stacked pills + soft shadow)
  3. Editorial (Deep Navy + orange keyword highlights + ambient glow)
  4. Callout (Warm Cream + frosted callout box + shadow)
  5. CTA (Warm Cream + soft-sell + bookmark badge)

Uses: Locked V2 palette, Poppins, paste_emoji(), soft_shadow_card(), gradient, pill_badge()
"""

import pathlib, json, textwrap, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from emoji_assets import paste_emoji, strip_all_emojis

BASE = pathlib.Path(r"D:/tm/06_Content")
FONT_DIR = BASE / "02_BRAND_ASSETS/fonts/Poppins"
LOGO_TRANSPARENT = BASE / "02_BRAND_ASSETS/logos/logo_cutouts_clean/official_logo_transparent.png"
LOGO_WHITE = BASE / "02_BRAND_ASSETS/logos/logo_cutouts_clean/official_logo_white.png"
OUT_DIR = BASE / "05_OUTPUTS/concept_post7_rich_2026"
OUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1350

# Palette
CREAM       = "#F5F2EB"
CREAM_LIGHT = "#FDFBF6"
CREAM_WARM  = "#F3DCCB"
NAVY        = "#071726"
NAVY_LIGHT  = "#122538"
INK         = "#0B131D"
ORANGE      = "#E85929"
ORANGE_LIGHT= "#FFF0EB"
TEAL        = "#028090"
TEAL_LIGHT  = "#E0F4F6"
MUTED       = "#55606E"
MUTED_LIGHT = "#8C9BAE"
WHITE       = "#FFFFFF"
BORDER      = "#E2DBD0"


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


F = {
    "hero":       font("Poppins-ExtraBold.ttf", 56),
    "hero_sub":   font("Poppins-ExtraBold.ttf", 44),
    "section":    font("Poppins-Bold.ttf", 36),
    "card_title": font("Poppins-Bold.ttf", 28),
    "sub":        font("Poppins-SemiBold.ttf", 22),
    "body_bold":  font("Poppins-Bold.ttf", 21),
    "body_med":   font("Poppins-Medium.ttf", 20),
    "body_reg":   font("Poppins-Regular.ttf", 19),
    "caption":    font("Poppins-Medium.ttf", 16),
    "pill_bold":  font("Poppins-Bold.ttf", 18),
    "pill_med":   font("Poppins-SemiBold.ttf", 16),
    "brand":      font("Poppins-SemiBold.ttf", 20),
    "num":        font("Poppins-ExtraBold.ttf", 32),
    "quote":      font("Poppins-Bold.ttf", 24),
}


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient_v(im, top, bot, x0=0, y0=0, x1=None, y1=None):
    d = ImageDraw.Draw(im)
    x1 = x1 or im.width; y1 = y1 or im.height
    tr, br = hex_rgb(top), hex_rgb(bot)
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        d.line([(x0, y), (x1, y)], fill=lerp(tr, br, t))


def rounded_rect_grad(im, box, r, top, bot):
    x1, y1, x2, y2 = box
    mask = Image.new("L", (im.width, im.height), 0)
    ImageDraw.Draw(mask).rounded_rectangle(box, radius=r, fill=255)
    grad = Image.new("RGB", (im.width, im.height))
    gradient_v(grad, top, bot, x0=x1, y0=y1, x1=x2, y1=y2)
    im.paste(grad, (0, 0), mask)


def soft_shadow(im, box, radius=20, alpha=45, blur=20, offset=(0, 8), color=(7, 23, 38)):
    shadow = Image.new("RGBA", (im.width, im.height), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    x1, y1, x2, y2 = box
    sd.rounded_rectangle(
        (x1 + offset[0], y1 + offset[1], x2 + offset[0], y2 + offset[1]),
        radius=radius, fill=color + (alpha,),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    im.paste(Image.alpha_composite(im.convert("RGBA"), shadow).convert("RGB"), (0, 0))
    return im


def paste_logo(im, white=False, x=90, y=70, h=52):
    p = LOGO_WHITE if white else LOGO_TRANSPARENT
    if p.exists():
        logo = Image.open(p).convert("RGBA")
        w = int(h * logo.width / logo.height)
        logo = logo.resize((w, h), Image.Resampling.LANCZOS)
        im.paste(logo, (x, y), logo)


def footer(im, page, tag="Sunday Academic Reset", dark=False):
    d = ImageDraw.Draw(im)
    cb = CREAM if dark else INK
    cp = MUTED_LIGHT if dark else MUTED
    d.text((90, H - 72), "naskah.fk", font=F["brand"], fill=cb)
    d.text((540, H - 72), tag, font=F["pill_med"], fill=ORANGE, anchor="mt")
    d.text((W - 90, H - 72), page, font=F["brand"], fill=cp, anchor="ra")


def pill(d, xy, text, bg, fg, bold=True, pad_x=18, pad_y=8):
    x, y = xy
    f = F["pill_bold"] if bold else F["pill_med"]
    bb = d.textbbox((0, 0), text, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    box = (x, y, x + tw + pad_x * 2, y + th + pad_y * 2)
    r = (th + pad_y * 2) // 2
    d.rounded_rectangle(box, radius=r, fill=bg)
    d.text((x + pad_x, y + pad_y), text, font=f, fill=fg)
    return box[2], box[3]  # right-x, bottom-y


def marker_oval(d, xy, w, h, color=ORANGE, width=4):
    """Hand-drawn-style marker oval highlight."""
    x, y = xy
    d.ellipse((x - 8, y - 6, x + w + 8, y + h + 6), outline=color, width=width)


# ─────────────────────────────────────────────────────────────
# SLIDE 1 — COVER (Warm Cream gradient + marker highlight)
# ─────────────────────────────────────────────────────────────
def slide_cover():
    im = Image.new("RGB", (W, H), CREAM)
    gradient_v(im, CREAM_LIGHT, CREAM_WARM)
    d = ImageDraw.Draw(im)
    paste_logo(im)

    # Badge pill
    pill(d, (90, 175), "Mindset Akademik", ORANGE, WHITE)

    # Hero headline
    lines = ["PROGRESS", "LEBIH PENTING", "DARI SEMPURNA"]
    y = 270
    for i, ln in enumerate(lines):
        d.text((90, y), ln, font=F["hero"], fill=INK)
        if i == 2:  # marker around "SEMPURNA"
            bb = d.textbbox((90, y), ln, font=F["hero"])
            marker_oval(d, (90, y), bb[2] - 90, bb[3] - y, ORANGE, 5)
        y += 68

    # Body
    body = "Satu paragraf yang kamu tulis hari ini lebih berharga daripada 10 halaman rencana yang terus ditunda."
    wrapped = textwrap.fill(body, width=42)
    d.multiline_text((90, 530), wrapped, font=F["body_med"], fill=MUTED, spacing=8)

    # Divider line
    d.line([(90, 660), (990, 660)], fill=BORDER, width=2)

    # 3 Quick-stat cards
    stats = [
        ("15 mnt", "Ritual Reset"),
        ("1 paragraf", "Target Besok"),
        ("3 langkah", "Checklist Malam"),
    ]
    cx = 90
    for val, label in stats:
        box = (cx, 700, cx + 270, 840)
        im = soft_shadow(im, box, radius=18, alpha=30, blur=16, offset=(0, 6))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle(box, radius=18, fill=WHITE, outline=BORDER, width=1)
        d.text((cx + 135, 728), val, font=F["card_title"], fill=ORANGE, anchor="mt")
        d.text((cx + 135, 770), label, font=F["caption"], fill=MUTED, anchor="mt")
        cx += 300

    # Emoji accents
    paste_emoji(im, "🌿", (900, 180), size=48, anchor="la")
    paste_emoji(im, "📝", (920, 700), size=36, anchor="la")

    # Swipe badge
    d = ImageDraw.Draw(im)
    pill(d, (90, 910), "Swipe buat reset", NAVY, WHITE, bold=False)

    footer(im, "01/05")
    return im


# ─────────────────────────────────────────────────────────────
# SLIDE 2 — FORMULA (Burnt Orange + stacked pills)
# ─────────────────────────────────────────────────────────────
def slide_formula():
    im = Image.new("RGB", (W, H), ORANGE)
    gradient_v(im, ORANGE, "#C84318")
    d = ImageDraw.Draw(im)
    paste_logo(im, white=True)

    # Title
    d.text((90, 200), "SUNDAY RESET", font=F["hero"], fill=WHITE)
    d.text((90, 268), "AKADEMIK", font=F["hero"], fill=WHITE)

    # Body
    body = "Akhir minggu bukan buat menghukum diri karena target belum semua tercapai. Pakai waktu ini untuk mengatur langkah kecil berikutnya."
    wrapped = textwrap.fill(body, width=40)
    d.multiline_text((90, 380), wrapped, font=F["body_med"], fill="#FFE8DD", spacing=8)

    # Stacked equation pills
    pills_data = [
        ("Evaluasi Minggu Ini", WHITE, NAVY),
        ("+ Target Mini Besok", WHITE, NAVY),
        ("= Naskah Lebih Jalan", NAVY, WHITE),
    ]
    py = 580
    for txt, bg, fg in pills_data:
        box = (90, py, 680, py + 65)
        im = soft_shadow(im, box, radius=20, alpha=40, blur=14, offset=(0, 5), color=(0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle(box, radius=20, fill=bg)
        d.text((130, py + 16), txt, font=F["card_title"], fill=fg)
        py += 85

    # Side emoji
    paste_emoji(im, "🎯", (800, 600), size=56, anchor="mm")
    paste_emoji(im, "💡", (850, 720), size=42, anchor="mm")

    # Bottom insight box
    insight_box = (90, 870, 990, 1000)
    d.rounded_rectangle(insight_box, radius=18, fill="#B84020", outline="#FFB89A", width=2)
    paste_emoji(im, "⚡", (116, 898), size=24, anchor="la")
    d.text((148, 895), "Insight:", font=F["pill_bold"], fill=WHITE)
    insight_txt = "Mahasiswa yang punya ritual reset mingguan menyelesaikan revisi 2x lebih cepat karena tidak kehilangan momentum setiap Senin."
    d.multiline_text((120, 930), textwrap.fill(insight_txt, 52), font=F["body_reg"], fill="#FFE8DD", spacing=6)

    footer(im, "02/05", dark=True)
    return im


# ─────────────────────────────────────────────────────────────
# SLIDE 3 — EDITORIAL (Deep Navy + orange highlights + glow)
# ─────────────────────────────────────────────────────────────
def slide_editorial():
    im = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(im)

    # Ambient glow blobs
    blob = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(blob)
    bd.ellipse((30, 100, 500, 550), fill=(232, 89, 41, 80))
    bd.ellipse((600, 600, 1050, 1050), fill=(2, 128, 144, 70))
    blob = blob.filter(ImageFilter.GaussianBlur(100))
    im = Image.alpha_composite(im.convert("RGBA"), blob).convert("RGB")
    d = ImageDraw.Draw(im)

    paste_logo(im, white=True)

    # Title
    d.text((90, 200), "JANGAN NUNGGU", font=F["hero"], fill=WHITE)
    d.text((90, 268), "MOOD BARU", font=F["hero"], fill=ORANGE)
    d.text((90, 336), "NULIS", font=F["hero"], fill=WHITE)

    # Body quote card (frosted glass)
    quote_box = (90, 460, 990, 680)
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle(quote_box, radius=22, fill=(255, 255, 255, 30))
    im = Image.alpha_composite(im.convert("RGBA"), panel).convert("RGB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(quote_box, radius=22, outline=(255, 255, 255, 60), width=2)

    d.text((120, 485), "Target yang lebih realistis:", font=F["sub"], fill=MUTED_LIGHT)
    d.text((120, 530), '"20 menit membaca jurnal,', font=F["quote"], fill=WHITE)
    d.text((120, 572), 'bukan langsung 20 halaman."', font=F["quote"], fill=ORANGE)

    # Body wisdom
    body = "Mood sering datang setelah kamu mulai, bukan sebelum. Mulai dari bagian paling kecil yang bisa kamu selesaikan malam ini."
    d.multiline_text((90, 730), textwrap.fill(body, 44), font=F["body_med"], fill="#C8D6E5", spacing=8)

    # 3 Micro-action cards
    actions = [
        ("1", "Baca 1 abstrak jurnal terbaru", "🔬"),
        ("2", "Edit 1 paragraf bab pembahasan", "✏️"),
        ("3", "Rapikan 3 referensi di Mendeley", "📚"),
    ]
    cy = 880
    for num, txt, emoji_ch in actions:
        box = (90, cy, 990, cy + 70)
        im = soft_shadow(im, box, radius=16, alpha=30, blur=12, offset=(0, 4), color=(0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle(box, radius=16, fill=NAVY_LIGHT, outline=(255, 255, 255, 40), width=1)
        # Number badge
        d.rounded_rectangle((110, cy + 14, 152, cy + 56), radius=10, fill=ORANGE)
        d.text((131, cy + 35), num, font=F["num"], fill=WHITE, anchor="mm")
        d.text((170, cy + 22), txt, font=F["body_bold"], fill=WHITE)
        paste_emoji(im, emoji_ch, (930, cy + 20), size=28, anchor="la")
        cy += 90

    footer(im, "03/05", dark=True)
    return im


# ─────────────────────────────────────────────────────────────
# SLIDE 4 — CALLOUT (Warm Cream + ritual box + shadow)
# ─────────────────────────────────────────────────────────────
def slide_callout():
    im = Image.new("RGB", (W, H), CREAM)
    gradient_v(im, CREAM_LIGHT, CREAM)
    d = ImageDraw.Draw(im)
    paste_logo(im)

    # Title with marker
    d.text((90, 190), "RITUAL", font=F["hero"], fill=INK)
    d.text((90, 258), "15 MENIT", font=F["hero"], fill=ORANGE)
    d.text((90, 326), "MALAM INI", font=F["hero"], fill=INK)
    # marker around 15 MENIT
    bb = d.textbbox((90, 258), "15 MENIT", font=F["hero"])
    marker_oval(d, (90, 258), bb[2] - 90, bb[3] - 258, ORANGE, 5)

    # Lead text
    d.text((90, 430), "Sebelum tidur, tulis tiga hal kecil ini:", font=F["sub"], fill=MUTED)

    # Main quote card
    quote_box = (90, 490, 990, 770)
    im = soft_shadow(im, quote_box, radius=22, alpha=40, blur=20, offset=(0, 8))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(quote_box, radius=22, fill=WHITE, outline=BORDER, width=2)

    # Quote mark
    d.text((120, 505), "\u201C", font=font("Poppins-ExtraBold.ttf", 72), fill=ORANGE)

    items = [
        ("1 paragraf", "yang akan kamu kerjakan besok pagi"),
        ("1 jurnal", "yang relevan, sudah siap di desktop"),
        ("1 revisi kecil", "bisa selesai dalam 20 menit pertama"),
    ]
    cy = 555
    for bold, normal in items:
        paste_emoji(im, "✅", (130, cy + 2), size=22, anchor="la")
        d = ImageDraw.Draw(im)
        d.text((160, cy), bold, font=F["body_bold"], fill=INK)
        bb2 = d.textbbox((160, cy), bold, font=F["body_bold"])
        d.text((bb2[2] + 8, cy), normal, font=F["body_reg"], fill=MUTED)
        cy += 48

    # Closing quote mark
    d.text((910, 700), "\u201D", font=font("Poppins-ExtraBold.ttf", 72), fill=ORANGE, anchor="rt")

    # Bottom wisdom
    wisdom_box = (90, 830, 990, 990)
    im = soft_shadow(im, wisdom_box, radius=20, alpha=30, blur=16, offset=(0, 6))
    d = ImageDraw.Draw(im)
    rounded_rect_grad(im, wisdom_box, 20, NAVY, NAVY_LIGHT)
    d = ImageDraw.Draw(im)
    paste_emoji(im, "💬", (116, 858), size=24, anchor="la")
    d = ImageDraw.Draw(im)
    d.text((148, 855), "Kenapa ini works?", font=F["pill_bold"], fill=ORANGE)
    wisdom = "Kecil, tapi cukup untuk membuat kamu tidak mulai dari nol lagi besok pagi. Otak kamu butuh starting point, bukan seluruh rencana."
    d.multiline_text((120, 895), textwrap.fill(wisdom, 50), font=F["body_reg"], fill="#C8D6E5", spacing=6)

    footer(im, "04/05")
    return im


# ─────────────────────────────────────────────────────────────
# SLIDE 5 — CTA (Warm Cream + soft-sell + bookmark badge)
# ─────────────────────────────────────────────────────────────
def slide_cta():
    im = Image.new("RGB", (W, H), CREAM)
    gradient_v(im, CREAM_LIGHT, CREAM)
    d = ImageDraw.Draw(im)
    paste_logo(im)

    # Hero CTA
    d.text((90, 200), "MINGGU DEPAN", font=F["hero"], fill=INK)
    d.text((90, 268), "MULAI DENGAN", font=F["hero"], fill=INK)
    d.text((90, 336), "LANGKAH KECIL", font=F["hero"], fill=ORANGE)
    # marker around LANGKAH KECIL
    bb = d.textbbox((90, 336), "LANGKAH KECIL", font=F["hero"])
    marker_oval(d, (90, 336), bb[2] - 90, bb[3] - 336, ORANGE, 5)

    # Body
    body = "Naskah yang selesai biasanya bukan ditulis sekali duduk, tapi dirapikan sedikit demi sedikit dengan ritme yang konsisten."
    d.multiline_text((90, 460), textwrap.fill(body, 42), font=F["body_med"], fill=MUTED, spacing=8)

    # Save bookmark card
    save_box = (90, 610, 990, 760)
    im = soft_shadow(im, save_box, radius=22, alpha=35, blur=18, offset=(0, 7))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(save_box, radius=22, fill=ORANGE_LIGHT, outline=ORANGE, width=2)
    paste_emoji(im, "🔖", (120, 645), size=36, anchor="la")
    d = ImageDraw.Draw(im)
    d.text((170, 640), "Simpan reset akademik ini", font=F["card_title"], fill=ORANGE)
    d.text((170, 680), "Buat pengingat tiap kali kamu merasa kewalahan di akhir minggu.", font=F["body_reg"], fill=MUTED)
    d.text((170, 710), "Tap ikon bookmark di kanan bawah!", font=F["caption"], fill=MUTED_LIGHT)

    # Soft-sell card
    sell_box = (90, 810, 990, 980)
    im = soft_shadow(im, sell_box, radius=20, alpha=30, blur=16, offset=(0, 6))
    d = ImageDraw.Draw(im)
    rounded_rect_grad(im, sell_box, 20, NAVY, NAVY_LIGHT)
    d = ImageDraw.Draw(im)
    d.text((120, 840), "Stuck di struktur naskah?", font=F["sub"], fill=WHITE)
    d.text((120, 878), "Tim naskah.fk bisa bantu pecah alur skripsi", font=F["body_bold"], fill=ORANGE)
    d.text((120, 910), "dan tesis kamu jadi langkah-langkah kecil.", font=F["body_bold"], fill=ORANGE)
    pill(d, (120, 945), "Hubungi @naskah.fk", ORANGE, WHITE)

    footer(im, "05/05")
    return im


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    slides = {
        "01_cover": slide_cover(),
        "02_formula": slide_formula(),
        "03_editorial": slide_editorial(),
        "04_callout": slide_callout(),
        "05_cta": slide_cta(),
    }

    for name, im in slides.items():
        path = OUT_DIR / f"post07_rich_{name}.jpg"
        im.save(str(path), "JPEG", quality=95, subsampling=0)
        print(f"SAVED: {path}")

    # Contact sheet
    CELL = 540
    PAD = 24
    row1 = Image.new("RGB", (CELL * 3 + PAD * 2, int(CELL * 1.25)), "#0E1117")
    row2 = Image.new("RGB", (CELL * 3 + PAD * 2, int(CELL * 1.25)), "#0E1117")
    all_imgs = list(slides.values())
    for i in range(3):
        thumb = all_imgs[i].resize((CELL, int(CELL * H / W)), Image.Resampling.LANCZOS)
        row1.paste(thumb, (i * (CELL + PAD), 0))
    for i in range(2):
        thumb = all_imgs[3 + i].resize((CELL, int(CELL * H / W)), Image.Resampling.LANCZOS)
        row2.paste(thumb, (i * (CELL + PAD), 0))

    sheet = Image.new("RGB", (row1.width, row1.height + row2.height + PAD), "#0E1117")
    sheet.paste(row1, (0, 0))
    sheet.paste(row2, (0, row1.height + PAD))
    sheet_path = OUT_DIR / "POST07_RICH_CONTACT_SHEET.jpg"
    sheet.save(str(sheet_path), "JPEG", quality=92)
    print(f"CONTACT SHEET: {sheet_path}")
