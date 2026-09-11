"""
Naskah 2026 — Generic Rich-Density Carousel Renderer (LOCKED SYSTEM v2.1)
Zero-collision dynamic bounding box layout engine.
"""

import os
import sys
import json
import textwrap
import pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
APPROVED = ROOT / "06_CONTENT_PIPELINE" / "03_APPROVED"
ASSETS = ROOT / "02_BRAND_ASSETS"
FONTS = ASSETS / "fonts"
EMOJIS = ASSETS / "emojis"

sys.path.insert(0, str(ROOT / "04_GENERATORS"))
from emoji_assets import paste_emoji, strip_all_emojis

W, H = 1080, 1350

# LOCKED COLOR PALETTE
CREAM = "#F5F2EB"
CREAM_LIGHT = "#FDFBF6"
CREAM_DARK = "#EBE5D8"
NAVY = "#071726"
NAVY_LIGHT = "#0E2338"
ORANGE = "#E85929"
ORANGE_LIGHT = "#FFF0EB"
ORANGE_DARK = "#B84020"
TEAL = "#028090"
INK = "#0B131D"
WHITE = "#FFFFFF"
MUTED = "#6B7C8C"
MUTED_LIGHT = "#A2B4C4"
BORDER = "#E0D9CB"
BORDER_DARK = "#1E344A"

def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    fp = FONTS / name
    if not fp.exists():
        fp = FONTS / "Poppins" / name
    if not fp.exists():
        fp = FONTS / "Montserrat-Bold.ttf"
    return ImageFont.truetype(str(fp), size)

F = {
    "display": font("Poppins-ExtraBold.ttf", 78),
    "headline": font("Poppins-ExtraBold.ttf", 68),
    "section": font("Poppins-Bold.ttf", 40),
    "sub": font("Poppins-Bold.ttf", 32),
    "card_t": font("Poppins-Bold.ttf", 28),
    "body_b": font("Poppins-SemiBold.ttf", 26),
    "body_m": font("Poppins-Medium.ttf", 24),
    "body_r": font("Poppins-Regular.ttf", 23),
    "caption": font("Poppins-Medium.ttf", 20),
    "pill": font("Poppins-Bold.ttf", 22),
    "num": font("Poppins-ExtraBold.ttf", 28),
    "tag": font("Poppins-SemiBold.ttf", 20),
}

def soft_shadow(im: Image.Image, box: tuple, radius: int = 24, alpha: int = 40, blur: int = 16, offset: tuple = (0, 6)) -> Image.Image:
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sx1, sy1, sx2, sy2 = box
    ox, oy = offset
    sbox = (sx1 + ox, sy1 + oy, sx2 + ox, sy2 + oy)
    sdraw.rounded_rectangle(sbox, radius=radius, fill=(7, 23, 38, alpha))
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    out = Image.new("RGBA", (W, H))
    out.paste(im, (0, 0))
    out.alpha_composite(shadow)
    return out.convert("RGB")

def rounded_rect_grad(im: Image.Image, box: tuple, radius: int, c_top: str, c_bot: str):
    x1, y1, x2, y2 = box
    bw, bh = max(1, x2 - x1), max(1, y2 - y1)
    card = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(card)
    cdraw.rounded_rectangle((0, 0, bw, bh), radius=radius, fill=(255, 255, 255, 255))

    grad = Image.new("RGBA", (bw, bh))
    gdraw = ImageDraw.Draw(grad)
    r1, g1, b1 = Image.new("RGB", (1, 1), c_top).getpixel((0, 0))
    r2, g2, b2 = Image.new("RGB", (1, 1), c_bot).getpixel((0, 0))
    for i in range(bh):
        t = i / max(1, bh - 1)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        gdraw.line([(0, i), (bw, i)], fill=(r, g, b, 255))

    card.putalpha(card.split()[3])
    grad.putalpha(card.split()[3])
    im.paste(grad, (x1, y1), grad)

def pill(draw: ImageDraw.ImageDraw, pos: tuple, text: str, bg: str, fg: str,
         bold: bool = True, pad_x: int = 24, pad_y: int = 12, im: Image.Image = None,
         emoji_prefix: str = None, align_right: bool = False):
    import re
    # Remove any unrenderable unicode emojis or symbols that cause tofu boxes
    clean_text = strip_all_emojis(text).strip()
    clean_text = clean_text.replace("→", "").replace("➡", "").replace("➡️", "").replace("←", "").strip()
    # Aggressively remove symbols outside ASCII and basic punctuation that cause boxes
    # Keep standard Indonesian characters, punctuation, and common typographic marks
    clean_text = re.sub(r'[^\x00-\x7F\xA0-\xFF\u2010-\u2027\u201C-\u201D]', '', clean_text)
    clean_text = clean_text.replace(' ', ' ').strip() # cleanup double spaces
    
    fnt = F["pill"]
    bb = draw.textbbox((0, 0), clean_text, font=fnt)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]

    emoji_size = 28
    emoji_gap = 10 if emoji_prefix else 0
    total_w = (emoji_size + emoji_gap if emoji_prefix else 0) + tw + pad_x * 2
    total_h = max(th + pad_y * 2, 48)

    x, y = pos
    if align_right:
        x = x - total_w

    box = (x, y, x + total_w, y + total_h)
    draw.rounded_rectangle(box, radius=total_h // 2, fill=bg)

    mid_y = y + total_h // 2
    curr_x = x + pad_x

    if emoji_prefix and im is not None:
        paste_emoji(im, emoji_prefix, (curr_x + emoji_size // 2, mid_y), size=emoji_size, anchor="mm")
        curr_x += emoji_size + emoji_gap

    draw.text((curr_x, mid_y), clean_text, font=fnt, fill=fg, anchor="lm")

def header(im: Image.Image, tag: str, light_mode: bool = True, on_orange: bool = False):
    d = ImageDraw.Draw(im)
    logo_w, logo_h = 44, 44
    lx, ly = 90, 80

    if light_mode and not on_orange:
        logo_path = ASSETS / "logos" / "logo_cutouts_clean" / "official_logo_transparent.png"
    else:
        logo_path = ASSETS / "logos" / "logo_cutouts_clean" / "official_logo_white.png"

    if logo_path.exists():
        try:
            lg = Image.open(logo_path).convert("RGBA")
            lg.thumbnail((logo_w, logo_h), Image.Resampling.LANCZOS)
            im.paste(lg, (lx, ly), lg)
        except Exception:
            d.rounded_rectangle((lx, ly, lx + logo_w, ly + logo_h), radius=10, fill=ORANGE)
            d.text((lx + 12, ly + 6), "N", font=F["section"], fill=WHITE)
    else:
        d.rounded_rectangle((lx, ly, lx + logo_w, ly + logo_h), radius=10, fill=ORANGE)
        d.text((lx + 12, ly + 6), "N", font=F["section"], fill=WHITE)

    handle_color = WHITE if (not light_mode or on_orange) else NAVY
    d.text((lx + logo_w + 16, ly + 10), "naskah.fk", font=F["tag"], fill=handle_color)

    if tag:
        clean_tag = strip_all_emojis(tag)
        bg = WHITE if (not light_mode or on_orange) else ORANGE
        fg = ORANGE if (not light_mode or on_orange) else WHITE
        pill(d, (990, ly), clean_tag, bg, fg, bold=True, pad_x=22, pad_y=10, align_right=True)

def footer(im: Image.Image, page: str, tag: str, light_mode: bool = True, on_orange: bool = False):
    d = ImageDraw.Draw(im)
    y = 1260
    c = WHITE if (not light_mode or on_orange) else MUTED
    d.text((90, y), "naskah.fk", font=F["tag"], fill=c)
    if tag:
        d.text((540, y), strip_all_emojis(tag)[:30], font=F["tag"], fill=c, anchor="mt")
    d.text((990, y), page, font=F["tag"], fill=c, anchor="rt")

def wrap_text_clean(text: str, max_width_px: int, font_obj: ImageFont.FreeTypeFont, draw: ImageDraw.ImageDraw) -> list:
    words = text.split()
    lines = []
    curr = []
    for w in words:
        test = " ".join(curr + [w])
        bb = draw.textbbox((0, 0), test, font=font_obj)
        if (bb[2] - bb[0]) <= max_width_px:
            curr.append(w)
        else:
            if curr:
                lines.append(" ".join(curr))
                curr = [w]
            else:
                lines.append(w)
                curr = []
    if curr:
        lines.append(" ".join(curr))
    return lines

# ==============================================================================
# SLIDE 1: COVER (Warm Cream)
# ==============================================================================
def render_cover(c: dict, tag: str) -> Image.Image:
    im = Image.new("RGB", (W, H), CREAM)
    header(im, c.get("pill", "Mindset Akademik"), light_mode=True)
    d = ImageDraw.Draw(im)

    lines = c.get("headline", ["PROGRESS", "LEBIH PENTING", "DARI SEMPURNA"])
    mark_line = c.get("mark_word_line", len(lines) - 1)

    y = 200
    line_h = 76
    max_bottom_y = y
    for i, line in enumerate(lines):
        clean_l = strip_all_emojis(line)
        bb = d.textbbox((90, y), clean_l, font=F["headline"])
        if i == mark_line:
            bar_y = bb[3] + 6
            d.rounded_rectangle((90, bar_y, bb[2] + 16, bar_y + 12), radius=6, fill=ORANGE)
            max_bottom_y = max(max_bottom_y, bar_y + 12)
        else:
            max_bottom_y = max(max_bottom_y, bb[3])
        d.text((90, y), clean_l, font=F["headline"], fill=NAVY)
        y += line_h

    y = max(y, max_bottom_y) + 24
    body_text = c.get("body", "Satu paragraf hari ini lebih baik dari 10 halaman rencana.")
    wrapped_body = wrap_text_clean(body_text, 860, F["body_m"], d)
    for bline in wrapped_body[:3]:
        d.text((90, y), bline, font=F["body_m"], fill=MUTED)
        y += 36

    y += 24
    items = c.get("items", [
        {"num": "01", "title": "Langkah Pertama", "desc": "Buka file skripsi hari ini"},
        {"num": "02", "title": "Pelan Tapi Jalan", "desc": "Tulis 1-2 kalimat dulu"},
        {"num": "03", "title": "Konsisten", "desc": "Lakukan setiap hari"}
    ])

    card_y = y
    card_h = 105
    gap = 14
    for it in items[:3]:
        box = (90, card_y, 990, card_y + card_h)
        im = soft_shadow(im, box, radius=20, alpha=28, blur=14, offset=(0, 5))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle(box, radius=20, fill=WHITE, outline=BORDER, width=2)
        d.rounded_rectangle((114, card_y + 22, 174, card_y + 82), radius=14, fill=ORANGE_LIGHT)
        d.text((144, card_y + 52), it.get("num", "01"), font=F["num"], fill=ORANGE, anchor="mm")
        d.text((196, card_y + 24), it.get("title", ""), font=F["card_t"], fill=NAVY)
        d.text((196, card_y + 60), it.get("desc", ""), font=F["body_r"], fill=MUTED)
        card_y += card_h + gap

    # Bottom CTA Box
    cta_y = 1010
    cta_box = (90, cta_y, 990, 1170)
    im = soft_shadow(im, cta_box, radius=22, alpha=32, blur=16, offset=(0, 6))
    rounded_rect_grad(im, cta_box, 22, NAVY, NAVY_LIGHT)
    d = ImageDraw.Draw(im)
    d.text((130, cta_y + 42), "Mulai dari langkah kecil hari ini", font=F["card_t"], fill=WHITE)
    d.text((130, cta_y + 92), "Tanpa drama, tanpa nunda. Satu langkah dulu.", font=F["body_r"], fill=MUTED_LIGHT)
    pill(d, (990 - 40, cta_y + 32), "Swipe", ORANGE, WHITE, bold=True, pad_x=22, pad_y=12, im=im, emoji_prefix="👉", align_right=True)

    footer(im, "01/05", tag, light_mode=True)
    return im

# ==============================================================================
# SLIDE 2: FORMULA / FRAMEWORK (Vibrant Orange Background)
# ==============================================================================
def render_formula(c: dict, tag: str) -> Image.Image:
    im = Image.new("RGB", (W, H), ORANGE)
    header(im, c.get("pill", "Framework"), light_mode=False, on_orange=True)
    d = ImageDraw.Draw(im)

    lines = c.get("headline", ["SUNDAY RESET", "AKADEMIK"])
    y = 200
    line_h = 76
    for line in lines:
        d.text((90, y), strip_all_emojis(line), font=F["headline"], fill=WHITE)
        y += line_h

    y += 10
    body_lead = c.get("body", "")
    if body_lead:
        wrapped_lead = wrap_text_clean(body_lead, 860, F["body_b"], d)
        for wline in wrapped_lead[:2]:
            d.text((90, y), wline, font=F["body_b"], fill=CREAM_LIGHT)
            y += 34
        y += 14

    steps = c.get("steps", None)
    if not steps:
        pills_raw = c.get("pills", ["1 Jurnal per hari", "1 Paragraf per sesi", "Skripsi jalan"])
        steps = [{"pill": str(i + 1).zfill(2), "text": p} for i, p in enumerate(pills_raw)]

    for st in steps[:3]:
        pill_w = 900
        pill_h = 96
        pbox = (90, y, 90 + pill_w, y + pill_h)
        im = soft_shadow(im, pbox, radius=24, alpha=45, blur=18, offset=(0, 7))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle(pbox, radius=24, fill=WHITE)
        d.rounded_rectangle((114, y + 18, 174, y + 78), radius=16, fill=ORANGE_LIGHT)
        d.text((144, y + 48), st.get("pill", "+"), font=F["num"], fill=ORANGE, anchor="mm")
        d.text((196, y + 48), st.get("text", ""), font=F["body_b"], fill=NAVY, anchor="lm")
        y += pill_h + 16

    # Bottom Insight Card (Solid Navy Glass, distinct & informative)
    ins_text = c.get("insight", "Kuncinya bukan durasi belajar, tapi konsistensi ritual kecil.")
    ins_wrapped = wrap_text_clean(ins_text, 760, F["body_r"], d)
    ins_h = 90 + len(ins_wrapped) * 32
    ins_box = (90, y + 8, 990, y + 8 + ins_h)
    im = soft_shadow(im, ins_box, radius=24, alpha=40, blur=16, offset=(0, 6))
    rounded_rect_grad(im, ins_box, 24, NAVY, NAVY_LIGHT)
    d = ImageDraw.Draw(im)
    paste_emoji(im, "⚡", (124, y + 30), size=36, anchor="top_left")
    d = ImageDraw.Draw(im)
    d.text((176, y + 30), "Insight Penting", font=F["card_t"], fill=ORANGE)
    iy = y + 76
    for iline in ins_wrapped:
        d.text((126, iy), iline, font=F["body_r"], fill=WHITE)
        iy += 32

    footer(im, "02/05", tag, light_mode=False, on_orange=True)
    return im

# ==============================================================================
# SLIDE 3: EDITORIAL / DEEP NAVY (Dark Mode with dynamic top quote box)
# ==============================================================================
def render_editorial(c: dict, tag: str) -> Image.Image:
    im = Image.new("RGB", (W, H), NAVY)
    header(im, c.get("pill", "Mindset"), light_mode=False)
    d = ImageDraw.Draw(im)

    lines = c.get("headline", ["JANGAN NUNGGU", "MOOD BARU NULIS"])
    mark_line = c.get("mark_word_line", 1)
    y = 200
    line_h = 76
    for i, line in enumerate(lines):
        clean_l = strip_all_emojis(line)
        bb = d.textbbox((90, y), clean_l, font=F["headline"])
        if i == mark_line:
            bar_y = bb[3] + 6
            d.rounded_rectangle((90, bar_y, bb[2] + 16, bar_y + 12), radius=6, fill=ORANGE)
        d.text((90, y), clean_l, font=F["headline"], fill=WHITE)
        y += line_h

    y += 18
    # Dynamic top quote box
    lead_text = c.get("lead", "Mood itu datang setelah kamu mulai, bukan sebelumnya.")
    lead_wrapped = wrap_text_clean(lead_text, 780, F["body_m"], d)
    lead_h = 44 + len(lead_wrapped) * 36
    top_box = (90, y, 990, y + lead_h)
    im = soft_shadow(im, top_box, radius=20, alpha=30, blur=14, offset=(0, 5))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(top_box, radius=20, fill=NAVY_LIGHT, outline=BORDER_DARK, width=2)
    ly = y + 22
    for lline in lead_wrapped:
        d.text((126, ly), lline, font=F["body_m"], fill=MUTED_LIGHT)
        ly += 36

    y += lead_h + 24
    items = c.get("items", [
        {"num": "1", "title": "Buka Mendeley", "desc": "Cari 1 jurnal yang relevan", "emoji": "🔬"},
        {"num": "2", "title": "Baca Abstrak", "desc": "Ambil poin kunci saja", "emoji": "✏️"},
        {"num": "3", "title": "Tulis 3 Kalimat", "desc": "Masukkan ke Bab 2 skripsi", "emoji": "📚"}
    ])

    # Dynamic card height and count (supports 2, 3, or 4 items without overflow)
    n_items = min(len(items), 4)
    if n_items == 4:
        card_h = 82
        gap = 10
    else:
        card_h = 100
        gap = 14

    for it in items[:n_items]:
        box = (90, y, 990, y + card_h)
        im = soft_shadow(im, box, radius=18, alpha=25, blur=12, offset=(0, 4))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle(box, radius=18, fill=NAVY_LIGHT, outline=BORDER_DARK, width=2)
        pad_num = 14 if n_items == 4 else 20
        d.rounded_rectangle((114, y + pad_num, 174, y + card_h - pad_num), radius=12, fill=ORANGE)
        d.text((144, y + card_h // 2), it.get("num", "1"), font=F["num"], fill=WHITE, anchor="mm")

        t_font = F["body_b"] if n_items == 4 else F["card_t"]
        d.text((196, y + (12 if n_items == 4 else 22)), it.get("title", ""), font=t_font, fill=WHITE)
        d.text((196, y + (44 if n_items == 4 else 58)), it.get("desc", ""), font=F["body_r"], fill=MUTED_LIGHT)

        em = it.get("emoji")
        if em:
            paste_emoji(im, em, (930, y + card_h // 2), size=(30 if n_items == 4 else 36), anchor="mm")
        y += card_h + gap

    footer(im, "03/05", tag, light_mode=False)
    return im

# ==============================================================================
# SLIDE 4: CALLOUT / QUOTE (Dynamic quote card)
# ==============================================================================
def render_callout(c: dict, tag: str) -> Image.Image:
    im = Image.new("RGB", (W, H), CREAM)
    header(im, c.get("pill", "Kata Mereka"), light_mode=True)
    d = ImageDraw.Draw(im)

    lines = c.get("headline", ["RITUAL 15 MENIT", "MALAM INI"])
    y = 200
    line_h = 76
    for line in lines:
        d.text((90, y), strip_all_emojis(line), font=F["headline"], fill=NAVY)
        y += line_h

    y += 12
    lead = c.get("lead", "")
    if lead:
        d.text((90, y), lead, font=F["sub"], fill=MUTED)
        y += 48

    # Dynamic Quote Card
    q_raw = c.get("quote", ["Konsistensi kecil mengalahkan ambisi besar yang tertunda."])
    if isinstance(q_raw, str):
        q_lines_raw = [q_raw]
    else:
        q_lines_raw = list(q_raw)
    quote_text = " ".join(str(x).strip() for x in q_lines_raw if str(x).strip())
    # Clean accidental character-spacing artifacts and unsupported arrows from config
    quote_text = quote_text.replace(" ", " ")
    quote_text = quote_text.replace("G u e", "Gue").replace("u d a h", "udah").replace("r e v i s i", "revisi")
    quote_text = quote_text.replace("→", "->").replace("➡", "->").replace("➡️", "->").replace("←", "<-")
    q_wrapped = wrap_text_clean(quote_text, 740, F["body_b"], d)
    q_h = 100 + len(q_wrapped) * 44
    quote_box = (90, y, 990, y + q_h)
    im = soft_shadow(im, quote_box, radius=24, alpha=38, blur=18, offset=(0, 8))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(quote_box, radius=24, fill=WHITE, outline=BORDER, width=2)
    d.text((120, quote_box[1] + 16), "\u201C", font=font("Poppins-ExtraBold.ttf", 64), fill=ORANGE)
    qy = quote_box[1] + 82
    for line in q_wrapped:
        d.text((126, qy), line, font=F["body_b"], fill=INK)
        qy += 44

    y += q_h + 24
    # Takeaway Dark Card
    take_box = (90, y, 990, y + 170)
    im = soft_shadow(im, take_box, radius=24, alpha=35, blur=16, offset=(0, 6))
    rounded_rect_grad(im, take_box, 24, NAVY, NAVY_LIGHT)
    paste_emoji(im, "💬", (130, y + 36), size=44, anchor="top_left")
    d = ImageDraw.Draw(im)
    d.text((196, y + 36), "Inti pesannya:", font=F["card_t"], fill=ORANGE)
    body_wrapped = wrap_text_clean(c.get("body", "Naskah jalan ketika lo mulai, bukan pas lo ngerasa siap."), 720, F["body_r"], d)
    by = y + 80
    for bl in body_wrapped[:2]:
        d.text((196, by), bl, font=F["body_r"], fill=MUTED_LIGHT)
        by += 32

    footer(im, "04/05", tag, light_mode=True)
    return im

# ==============================================================================
# SLIDE 5: CTA / ACTION (Vibrant Orange Background)
# ==============================================================================
def render_cta(c: dict, tag: str) -> Image.Image:
    # Use ORANGE background for high-conversion hook
    im = Image.new("RGB", (W, H), ORANGE)
    header(im, c.get("pill", "Action"), light_mode=False, on_orange=True)
    d = ImageDraw.Draw(im)

    lines = c.get("headline", ["MINGGU DEPAN MULAI", "LANGKAH KECIL"])
    y = 200
    line_h = 76
    for line in lines:
        d.text((90, y), strip_all_emojis(line), font=F["headline"], fill=WHITE)
        y += line_h

    y += 14
    body = c.get("body", "Jangan biarkan hari Minggu berakhir tanpa satu langkah persiapan.")
    body_wrapped = wrap_text_clean(body, 820, F["body_m"], d)
    for bl in body_wrapped[:2]:
        d.text((90, y), bl, font=F["body_m"], fill=CREAM_LIGHT)
        y += 36

    y += 24
    # Save Card (White background to pop on Orange)
    s_box = (90, y, 990, y + 140)
    im = soft_shadow(im, s_box, radius=24, alpha=45, blur=18, offset=(0, 7))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(s_box, radius=24, fill=WHITE, outline=BORDER, width=2)
    paste_emoji(im, "🔖", (130, y + 36), size=44, anchor="top_left")
    d = ImageDraw.Draw(im)
    d.text((200, y + 30), "Simpan buat nanti", font=F["card_t"], fill=ORANGE)
    d.text((200, y + 78), "Save dulu, baca pas lagi butuh booster.", font=F["body_r"], fill=MUTED)

    y += 140 + 24
    # Sell Card (Solid Navy, spacious)
    foot_text = c.get("foot", "Follow @naskah.fk untuk konten akademik mingguan.")
    foot_wrapped = wrap_text_clean(foot_text, 760, F["sub"], d)
    sell_h = 220 + len(foot_wrapped) * 46
    sell_box = (90, y, 990, y + sell_h)
    im = soft_shadow(im, sell_box, radius=24, alpha=40, blur=16, offset=(0, 6))
    rounded_rect_grad(im, sell_box, 24, NAVY, NAVY_LIGHT)
    d = ImageDraw.Draw(im)

    fy = y + 34
    for fl in foot_wrapped[:3]:
        d.text((130, fy), fl, font=F["sub"], fill=WHITE)
        fy += 46
    d.text((130, fy + 6), c.get("pill_b", "Pelan, konsisten, dan naskah lo jalan."),
           font=F["body_b"], fill=ORANGE)
    fy2 = fy + 50
    d.text((130, fy2), "Dapatkan template & tips metodologi setiap minggu.", font=F["body_r"], fill=MUTED_LIGHT)

    pill_y = fy2 + 44
    # CTA Button inside the Navy Card (White pill with Navy text to pop)
    pill(d, (130, pill_y), c.get("button", "Follow @naskah.fk"), WHITE, NAVY, bold=True, pad_x=28, pad_y=14)

    footer(im, "05/05", tag, light_mode=False, on_orange=True)
    return im

# ==============================================================================
# DISPATCHER & EXPORTER
# ==============================================================================
def render_slide(slide_type: str, slide_cfg: dict, tag: str) -> Image.Image:
    if slide_type == "cover":
        return render_cover(slide_cfg, tag)
    elif slide_type == "formula":
        return render_formula(slide_cfg, tag)
    elif slide_type == "editorial":
        return render_editorial(slide_cfg, tag)
    elif slide_type == "callout":
        return render_callout(slide_cfg, tag)
    elif slide_type == "cta":
        return render_cta(slide_cfg, tag)
    else:
        return render_cover(slide_cfg, tag)

def render_post(post_name: str, out_dir: pathlib.Path) -> pathlib.Path:
    # Backward-compatible lookup: if post_name is an old-style folder name
    # without date prefix, try to find the dated folder in APPROVED.
    cfg_path = APPROVED / post_name / "carousel_config.json"
    if not cfg_path.exists():
        # Search for a folder under APPROVED whose name ends with post_name
        candidates = [d for d in APPROVED.iterdir() if d.is_dir() and d.name.endswith(post_name)]
        if candidates:
            cfg_path = candidates[0] / "carousel_config.json"
    if not cfg_path.exists():
        raise FileNotFoundError(f"No carousel_config.json found for {post_name}")

    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    out_dir.mkdir(parents=True, exist_ok=True)
    tag = cfg.get("tag", post_name.replace("_", " ").title())

    # Derive a stable output filename prefix from the folder name:
    # strip the leading date YYYY-MM-DD_, then keep the post slug.
    base = cfg_path.parent.name
    if base[:4].isdigit() and len(base) > 11 and base[4] == "-" and base[7] == "-":
        base = base[11:]

    # Map folder slug to the publisher-compatible filename prefix
    PREFIX_MAP = {
        "post_01_word_citation": "post01",
        "post_02_jurnal_kedokteran": "post02",
        "post_03_skripsi_vs_tesis": "post03",
        "post_04_native_word_citation": "post04",
        "post_05_anatomi_naskah_acc": "post05",
        "post_06_carousel_layout_edukasi": "post06",
        "post_07_sunday_academic_reset": "post07",
        "post_08_hard_sell_3jt_lengkap": "post08",
        "post_09_hard_sell_price_list": "post09",
        "post_w1_01_diagnosis_skripsi": "post_w1_01",
        "post_w1_04_scu_episode1": "post_w1_04",
        "post_w1_sat_naskah_inside_ep1": "post_w1_ni",
    }
    prefix = PREFIX_MAP.get(base, base)

    slide_types = ["cover", "formula", "editorial", "callout", "cta"]
    for idx, stype in enumerate(slide_types, start=1):
        scfg = cfg.get(stype, {})
        img = render_slide(stype, scfg, tag)
        fname = f"{prefix}_{idx:02d}_{stype}.jpg"
        out_file = out_dir / fname
        img.save(out_file, "JPEG", quality=95)
        print(f"SAVED: {out_file}")

    print("DONE")
    return out_dir

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--post", required=True, help="Folder name under 03_APPROVED")
    parser.add_argument("--out", default=None, help="Output directory")
    args = parser.parse_args()

    out_d = pathlib.Path(args.out) if args.out else APPROVED / args.post
    render_post(args.post, out_d)
