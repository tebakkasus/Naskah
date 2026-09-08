"""
Post 07 — Sunday Academic Reset (RICH v2)
Redesigned for feed readability: bigger type, disciplined grid, anti-overflow cards.

Key fixes vs v1 (TM + vision review):
- FONT SCALE-UP: headline ~80px, body 28px, caption 22px (readable on phone feed)
- BALANCED COMPOSITION: full-width rows, no left-heavy dead space
- ANTI-OVERFLOW: all card heights computed from measured text
- PILLS CENTERED: full-width pills, centered text (no left-cramped)
- MARKER replaced by highlight bar (clean, not scribble)
- EMOJI always inside a container (no floating)
"""

import pathlib, textwrap, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from emoji_assets import paste_emoji

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
ORANGE_DK   = "#C84318"
ORANGE_LIGHT= "#FFF0EB"
TEAL        = "#028090"
TEAL_LIGHT  = "#E0F4F6"
MUTED       = "#55606E"
MUTED_LIGHT = "#8C9BAE"
WHITE       = "#FFFFFF"
BORDER      = "#E2DBD0"

# ── fonts: full-size, scaled for phone readability ──
def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)

F = {
    "hero":      font("Poppins-ExtraBold.ttf", 84),
    "hero_mid":  font("Poppins-ExtraBold.ttf", 68),
    "section":   font("Poppins-Bold.ttf", 46),
    "card_t":    font("Poppins-Bold.ttf", 34),
    "sub":       font("Poppins-SemiBold.ttf", 30),
    "body_b":    font("Poppins-Bold.ttf", 28),
    "body_m":    font("Poppins-Medium.ttf", 28),
    "body_r":    font("Poppins-Regular.ttf", 26),
    "caption":   font("Poppins-Medium.ttf", 21),
    "pill_b":    font("Poppins-Bold.ttf", 24),
    "pill_m":    font("Poppins-SemiBold.ttf", 20),
    "brand":     font("Poppins-SemiBold.ttf", 22),
    "num":       font("Poppins-ExtraBold.ttf", 36),
    "quote":     font("Poppins-Bold.ttf", 32),
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


def soft_shadow(im, box, radius=24, alpha=40, blur=18, offset=(0, 7), color=(7, 23, 38)):
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


def paste_logo(im, white=False, x=90, y=70, h=56):
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
    d.text((90, H - 80), "naskah.fk", font=F["brand"], fill=cb)
    d.text((W // 2, H - 80), tag, font=F["pill_m"], fill=ORANGE, anchor="mt")
    d.text((W - 90, H - 80), page, font=F["brand"], fill=cp, anchor="ra")


def text_box(d, x, y, text, f, fill, width=900, spacing=8, align="left"):
    """Draw wrapped text. Returns (right_x, bottom_y)."""
    wrapped = textwrap.fill(text, width=width // (f.size // 2))
    lines = wrapped.split("\n")
    yy = y
    for i, ln in enumerate(lines):
        d.text((x, yy), ln, font=f, fill=fill)
        yy += f.size + spacing
    return x, yy - spacing


def text_height(text, f, width, spacing=8):
    wrapped = textwrap.fill(text, width=width // (f.size // 2))
    lines = wrapped.split("\n")
    return len(lines) * (f.size + spacing) - spacing


def pill(d, xy, text, bg, fg, bold=True, pad_x=26, pad_y=14, im=None, emoji_prefix=None, emoji_size=24, spacing=10, align_right=False):
    """
    Hug-content perfectly centered pill.
    If align_right=True, xy=(right_edge_x, top_y), and box automatically expands to the left.
    """
    rx, y = xy
    f = F["pill_b"] if bold else F["pill_m"]
    bb = d.textbbox((0, 0), text, font=f)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]

    # Total content width inside pill
    emoji_w = (emoji_size + spacing) if emoji_prefix else 0
    content_w = emoji_w + tw
    
    # Pill box dimensions
    pill_w = content_w + pad_x * 2
    pill_h = th + pad_y * 2
    
    # If align_right, start X is (rx - pill_w)
    x = (rx - pill_w) if align_right else rx
    
    box = (x, y, x + pill_w, y + pill_h)
    r = pill_h // 2

    # Draw rounded rectangle background
    d.rounded_rectangle(box, radius=r, fill=bg)

    # Vertical center of the pill
    mid_y = y + pill_h / 2

    # If emoji exists, draw it centered
    if emoji_prefix and im:
        emoji_center_x = x + pad_x + emoji_size / 2
        paste_emoji(im, emoji_prefix, (emoji_center_x, mid_y), size=emoji_size, anchor="mm")
        text_x = x + pad_x + emoji_size + spacing
    else:
        text_x = x + pad_x

    # Draw text vertically centered beside emoji
    d.text((text_x, mid_y), text, font=f, fill=fg, anchor="lm")

    return box


def highlight_bar(d, x, y, w, h, color=ORANGE):
    """Clean bold underline highlight (not scribble)."""
    d.rounded_rectangle((x, y, x + w, y + h), radius=h // 2, fill=color)


# ─────────────────────────────────────────────────────────────
# SLIDE 1 — COVER
# ─────────────────────────────────────────────────────────────
def slide_cover():
    im = Image.new("RGB", (W, H), CREAM)
    gradient_v(im, CREAM_LIGHT, CREAM)
    d = ImageDraw.Draw(im)
    paste_logo(im)

    # Badge pill top-right — aligned right with 90px margin, vertical center with logo
    pill(d, (W - 90, 75), "Mindset Akademik", ORANGE, WHITE, align_right=True)

    # Hero lines
    lines = ["PROGRESS", "LEBIH PENTING", "DARI SEMPURNA"]
    y = 230
    line_h = 92
    for i, ln in enumerate(lines):
        if i == 2:
            # Measure bounding box of "DARI SEMPURNA"
            bb = d.textbbox((90, y), ln, font=F["hero"])
            text_bottom = bb[3]
            # Place highlight bar cleanly BELOW the letters (no overlapping/cutting)
            bar_y = text_bottom + 6
            bar_h = 10
            highlight_bar(d, 90, bar_y, bb[2] - 90, bar_h, ORANGE)
        d.text((90, y), ln, font=F["hero"], fill=INK)
        y += line_h

    # Body (bigger, balanced spacing)
    body_y = y + 24
    body = "Satu paragraf yang kamu tulis hari ini lebih berharga daripada 10 halaman rencana yang terus ditunda."
    text_box(d, 90, body_y, body, F["body_m"], MUTED, width=860)

    # 3 stat cards — full-width row, vertically centered content
    cards = [
        ("15 mnt", "Ritual Reset"),
        ("1 paragraf", "Target Besok"),
        ("3 langkah", "Checklist Malam"),
    ]
    cy = 760
    cw = 280
    gap = 30
    for i, (val, label) in enumerate(cards):
        x = 90 + i * (cw + gap)
        box = (x, cy, x + cw, cy + 180)
        im = soft_shadow(im, box, radius=22, alpha=35, blur=16, offset=(0, 6))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle(box, radius=22, fill=WHITE, outline=BORDER, width=1)
        # center content vertically
        bbv = d.textbbox((0, 0), val, font=F["card_t"])
        d.text((x + (cw - bbv[2] + bbv[0]) // 2, cy + 44), val, font=F["card_t"], fill=ORANGE)
        bbl = d.textbbox((0, 0), label, font=F["caption"])
        d.text((x + (cw - bbl[2] + bbl[0]) // 2, cy + 104), label, font=F["caption"], fill=MUTED)

    # CTA pill card container at bottom to eliminate dead space
    cta_box = (90, 990, 990, 1140)
    im = soft_shadow(im, cta_box, radius=22, alpha=28, blur=14, offset=(0, 5))
    d = ImageDraw.Draw(im)
    rounded_rect_grad(im, cta_box, 22, NAVY, NAVY_LIGHT)
    d = ImageDraw.Draw(im)
    d.text((130, 1025), "Swipe untuk mulai ritual reset", font=F["card_t"], fill=WHITE)
    d.text((130, 1075), "Minggu malam = reset tenang, bukan panik.", font=F["body_r"], fill=MUTED_LIGHT)
    # Right arrow pill inside CTA card
    pill(d, (990 - 40, 1030), "Swipe", ORANGE, WHITE, bold=True, pad_x=22, pad_y=12, im=im, emoji_prefix="👉", align_right=True)

    footer(im, "01/05")
    return im


# ─────────────────────────────────────────────────────────────
# SLIDE 2 — FORMULA
# ─────────────────────────────────────────────────────────────
def slide_formula():
    im = Image.new("RGB", (W, H), ORANGE)
    gradient_v(im, ORANGE, ORANGE_DK)
    d = ImageDraw.Draw(im)
    paste_logo(im, white=True)
    # Target pill badge top-right — aligned right with 90px margin, center-aligned with logo
    pill(d, (W - 90, 75), "Focus", "#B84020", WHITE, bold=True, pad_x=22, pad_y=12, im=im, emoji_prefix="🎯", align_right=True)

    # Title
    d.text((90, 210), "SUNDAY RESET", font=F["hero_mid"], fill=WHITE)
    d.text((90, 286), "AKADEMIK", font=F["hero_mid"], fill=WHITE)

    # Body
    body = "Akhir minggu bukan buat menghukum diri karena target belum semua tercapai. Pakai waktu ini untuk mengatur langkah kecil berikutnya."
    text_box(d, 90, 390, body, F["body_m"], "#FFE8DD", width=860)

    # Equation pills — full width, centered text
    pills_data = [
        ("Evaluasi Minggu Ini", WHITE, NAVY),
        ("+ Target Mini Besok", WHITE, NAVY),
        ("= Naskah Lebih Jalan", NAVY, WHITE),
    ]
    py = 600
    for txt, bg, fg in pills_data:
        box = (90, py, 990, py + 76)
        im = soft_shadow(im, box, radius=24, alpha=45, blur=14, offset=(0, 5), color=(0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle(box, radius=24, fill=bg)
        d.text((540, py + 16), txt, font=F["card_t"], fill=fg, anchor="mt")  # centered
        py += 96

    # Insight box — height computed from text
    insight_title = "Insight"
    insight_body = ("Mahasiswa yang punya ritual reset mingguan menyelesaikan revisi 2x lebih cepat "
                    "karena tidak kehilangan momentum setiap Senin.")
    pad = 36
    line_h = 34
    n_lines = len(textwrap.wrap(insight_body, 34))
    box_h = pad * 2 + 34 + line_h * n_lines
    box_y = py + 14
    ix = (90, box_y, 990, box_y + box_h)
    im = soft_shadow(im, ix, radius=20, alpha=35, blur=14, offset=(0, 6), color=(0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(ix, radius=20, fill="#B84020", outline="#FFB89A", width=2)
    d.text((126, box_y + pad), insight_title, font=F["pill_b"], fill=WHITE)
    d.text((126, box_y + pad + 34), "\n".join(textwrap.wrap(insight_body, 34)),
           font=F["body_r"], fill="#FFE8DD", spacing=8)

    footer(im, "02/05", dark=True)
    return im


# ─────────────────────────────────────────────────────────────
# SLIDE 3 — EDITORIAL
# ─────────────────────────────────────────────────────────────
def slide_editorial():
    im = Image.new("RGB", (W, H), NAVY)
    # ambient glow
    blob = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(blob)
    bd.ellipse((300, 80, 800, 480), fill=(232, 89, 41, 70))
    bd.ellipse((560, 700, 1060, 1150), fill=(2, 128, 144, 60))
    blob = blob.filter(ImageFilter.GaussianBlur(120))
    im = Image.alpha_composite(im.convert("RGBA"), blob).convert("RGB")
    d = ImageDraw.Draw(im)
    paste_logo(im, white=True)
    # Tips pill badge top-right — aligned right with 90px margin
    pill(d, (W - 90, 75), "Tips", NAVY_LIGHT, WHITE, bold=True, pad_x=22, pad_y=12, im=im, emoji_prefix="💡", align_right=True)

    # Title
    d.text((90, 190), "JANGAN NUNGGU", font=F["hero_mid"], fill=WHITE)
    d.text((90, 266), "MOOD BARU", font=F["hero_mid"], fill=ORANGE)
    d.text((90, 342), "NULIS", font=F["hero_mid"], fill=WHITE)

    # Quote card (frosted)
    q_box = (90, 470, 990, 700)
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(panel).rounded_rectangle(q_box, radius=24, fill=(255, 255, 255, 26))
    im = Image.alpha_composite(im.convert("RGBA"), panel).convert("RGB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(q_box, radius=24, outline=(255, 255, 255, 70), width=2)
    d.text((126, 505), "Target yang lebih realistis:", font=F["sub"], fill="#A9C7DF")
    d.text((126, 560), '"20 menit membaca jurnal,', font=F["quote"], fill=WHITE)
    d.text((126, 610), 'bukan langsung 20 halaman."', font=F["quote"], fill=ORANGE)

    # Body wisdom
    d.text((90, 750), "Mood sering datang setelah kamu mulai, bukan sebelum.",
           font=F["body_b"], fill=WHITE)
    d.text((90, 794), "Mulai dari bagian paling kecil yang bisa kamu selesaikan malam ini.",
           font=F["body_m"], fill="#C8D6E5")

    # 3 action rows — full-width, balanced
    actions = [
        ("1", "Baca 1 abstrak jurnal terbaru", "🔬"),
        ("2", "Edit 1 paragraf bab pembahasan", "✏️"),
        ("3", "Rapikan 3 referensi di Mendeley", "📚"),
    ]
    cy = 900
    for num, txt, em in actions:
        box = (90, cy, 990, cy + 84)
        im = soft_shadow(im, box, radius=20, alpha=30, blur=12, offset=(0, 4), color=(0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle(box, radius=20, fill=NAVY_LIGHT, outline=(255, 255, 255, 45), width=1)
        d.rounded_rectangle((120, cy + 18, 170, cy + 66), radius=12, fill=ORANGE)
        d.text((145, cy + 42), num, font=F["num"], fill=WHITE, anchor="mm")
        d.text((196, cy + 24), txt, font=F["body_b"], fill=WHITE)
        # Center emoji vertically relative to the box (height 84)
        paste_emoji(im, em, (910, cy + (84 - 36) // 2), size=36, anchor="top_left")
        cy += 100

    footer(im, "03/05", dark=True)
    return im


# ─────────────────────────────────────────────────────────────
# SLIDE 4 — CALLOUT
# ─────────────────────────────────────────────────────────────
def slide_callout():
    im = Image.new("RGB", (W, H), CREAM)
    gradient_v(im, CREAM_LIGHT, CREAM)
    d = ImageDraw.Draw(im)
    paste_logo(im)
    # Moon pill badge top-right — aligned right with 90px margin, center-aligned with logo
    pill(d, (W - 90, 75), "Malam", NAVY, WHITE, bold=True, pad_x=22, pad_y=12, im=im, emoji_prefix="🌙", align_right=True)

    # Title
    d.text((90, 220), "RITUAL", font=F["hero_mid"], fill=INK)
    d.text((90, 296), "15 MENIT", font=F["hero_mid"], fill=ORANGE)
    d.text((90, 372), "MALAM INI", font=F["hero_mid"], fill=INK)
    bb = d.textbbox((90, 296), "15 MENIT", font=F["hero_mid"])
    highlight_bar(d, 90, 372 + 8, bb[2] - 90, 12, ORANGE)

    # Lead
    d.text((90, 460), "Sebelum tidur, tulis tiga hal kecil ini:", font=F["sub"], fill=MUTED)

    # Checklist card
    c_box = (90, 530, 990, 880)
    im = soft_shadow(im, c_box, radius=26, alpha=38, blur=18, offset=(0, 8))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(c_box, radius=26, fill=WHITE, outline=BORDER, width=2)

    items = [
        ("1 paragraf", "yang akan kamu kerjakan besok pagi"),
        ("1 jurnal", "yang relevan, sudah siap di desktop"),
        ("1 revisi kecil", "bisa selesai dalam 20 menit pertama"),
    ]
    cy = 575
    for bold, normal in items:
        paste_emoji(im, "✅", (140, cy + (48 - 34) // 2), size=34, anchor="top_left")
        d = ImageDraw.Draw(im)
        bb_bold = d.textbbox((0, 0), bold, font=F["body_b"])
        text_mid_y = cy + (bb_bold[3] - bb_bold[1]) / 2
        d.text((190, cy), bold, font=F["body_b"], fill=INK)
        bb2 = d.textbbox((190, cy), bold, font=F["body_b"])
        d.text((bb2[2] + 12, cy), normal, font=F["body_r"], fill=MUTED)
        cy += 70

    # Small print
    d.text((126, 800), "Kecil, tapi cukup untuk membuat kamu tidak mulai dari nol lagi besok pagi.",
           font=F["caption"], fill=MUTED_LIGHT)

    # Why-it-works card (navy gradient)
    w_box = (90, 930, 990, 1130)
    im = soft_shadow(im, w_box, radius=24, alpha=32, blur=16, offset=(0, 6))
    rounded_rect_grad(im, w_box, 24, NAVY, NAVY_LIGHT)
    d = ImageDraw.Draw(im)
    paste_emoji(im, "💬", (130, 970 + (48 - 32) // 2), size=32, anchor="top_left")
    d.text((180, 965), "Kenapa ini works?", font=F["card_t"], fill=ORANGE)
    d.text((126, 1030), "Otak kamu butuh starting point, bukan seluruh rencana.",
           font=F["body_m"], fill="#C8D6E5")

    footer(im, "04/05")
    return im


# ─────────────────────────────────────────────────────────────
# SLIDE 5 — CTA
# ─────────────────────────────────────────────────────────────
def slide_cta():
    im = Image.new("RGB", (W, H), CREAM)
    gradient_v(im, CREAM_LIGHT, CREAM)
    d = ImageDraw.Draw(im)
    paste_logo(im)
    # Action pill badge top-right — aligned right with 90px margin
    pill(d, (W - 90, 75), "Action", ORANGE, WHITE, bold=True, pad_x=22, pad_y=12, im=im, emoji_prefix="⚡", align_right=True)

    # Hero
    d.text((90, 220), "MINGGU DEPAN", font=F["hero_mid"], fill=INK)
    d.text((90, 296), "MULAI DENGAN", font=F["hero_mid"], fill=INK)
    d.text((90, 372), "LANGKAH KECIL", font=F["hero_mid"], fill=ORANGE)
    bb = d.textbbox((90, 372), "LANGKAH KECIL", font=F["hero_mid"])
    highlight_bar(d, 90, 458, bb[2] - 90, 12, ORANGE)

    # Body
    body = ("Naskah yang selesai biasanya bukan ditulis sekali duduk, tapi dirapikan "
            "sedikit demi sedikit dengan ritme yang konsisten.")
    text_box(d, 90, 500, body, F["body_m"], MUTED, width=860)

    # Save card
    s_box = (90, 660, 990, 830)
    im = soft_shadow(im, s_box, radius=26, alpha=35, blur=16, offset=(0, 7))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(s_box, radius=26, fill=ORANGE_LIGHT, outline=ORANGE, width=2)
    paste_emoji(im, "🔖", (130, 700 + (46 - 46) // 2), size=46, anchor="top_left")
    d = ImageDraw.Draw(im)
    d.text((200, 695), "Simpan reset akademik ini", font=F["card_t"], fill=ORANGE)
    d.text((200, 748), "Tap ikon bookmark buat pengingat akhir minggu.",
           font=F["body_r"], fill=MUTED)

    # Sell card
    sell_box = (90, 870, 990, 1090)
    im = soft_shadow(im, sell_box, radius=24, alpha=32, blur=16, offset=(0, 6))
    rounded_rect_grad(im, sell_box, 24, NAVY, NAVY_LIGHT)
    d = ImageDraw.Draw(im)
    d.text((126, 910), "Stuck di struktur naskah?", font=F["sub"], fill=WHITE)
    d.text((126, 958), "Tim naskah.fk bisa bantu pecah alur skripsi & tesis",
           font=F["body_b"], fill=ORANGE)
    d.text((126, 1000), "jadi langkah-langkah kecil.", font=F["body_b"], fill=ORANGE)
    pill(d, (126, 1050), "Hubungi @naskah.fk", ORANGE, WHITE)

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
        path = OUT_DIR / f"post07_rich_v2_{name}.jpg"
        im.save(str(path), "JPEG", quality=95, subsampling=0)
        print(f"SAVED: {path}")

    # Contact sheet
    CELL = 500
    GAP = 18
    PAD = 24
    imgs = list(slides.values())
    rows = (len(imgs) + 2) // 3
    sheet_w = PAD * 2 + 3 * CELL + 2 * GAP
    sheet_h = PAD * 2 + rows * int(CELL * H / W) + (rows - 1) * GAP
    sheet = Image.new("RGB", (sheet_w, sheet_h), "#0E1117")
    for i, im in enumerate(imgs):
        thumb = im.resize((CELL, int(CELL * H / W)), Image.Resampling.LANCZOS)
        r, c = i // 3, i % 3
        sheet.paste(thumb, (PAD + c * (CELL + GAP), PAD + r * (int(CELL * H / W) + GAP)))
    sheet_path = OUT_DIR / "POST07_RICH_V2_CONTACT_SHEET.jpg"
    sheet.save(str(sheet_path), "JPEG", quality=92)
    print("CONTACT SHEET:", sheet_path)