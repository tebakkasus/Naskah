"""
Naskah Rich & High-Density Visual Upgrade Concepts (2026 Aesthetic + Deep Academic Content).

Addresses user feedback:
"bagus aku suka secara design, tapi karna isinya sedikit, jadinya kayak kurang, coba eksplore lagi"

Upgrades:
- High information density (meaty, actionable, saveable, comprehensive)
- Retains 2026 aesthetics: soft shadows (elevation), subtle mood gradients, bento cards, tactile pills, high-contrast Poppins typography
- Clean hierarchy so dense information remains easily scannable and readable on mobile screens

4 Rich Concepts:
1. High-Density Bento Matrix: Cheatsheet Uji Statistik & Hipotesis Medis
2. 5-Step Layered Timeline: Workflow Literature Review 5 Hari
3. Deep Navy Dark Glass Comparison: OR vs RR vs HR (Riset Klinis)
4. Editorial Anatomy Breakdown: Format Bab 4 & 5 yang Bikin Penguji ACC
"""
from __future__ import annotations

import pathlib
from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE_DIR = pathlib.Path(r"D:/tm/06_Content")
FONT_DIR = BASE_DIR / "02_BRAND_ASSETS/fonts/Poppins"
LOGO_TRANSPARENT = BASE_DIR / "02_BRAND_ASSETS/logos/logo_cutouts_clean/official_logo_transparent.png"
LOGO_WHITE = BASE_DIR / "02_BRAND_ASSETS/logos/logo_cutouts_clean/official_logo_white.png"
OUT_DIR = BASE_DIR / "05_OUTPUTS/concept_rich_density_2026"

W, H = 1080, 1350

# Palette
CREAM = "#F5F2EB"
CREAM_LIGHT = "#FDFBF6"
CREAM_DARK = "#EBE5D8"
NAVY = "#071726"
NAVY_LIGHT = "#122538"
INK = "#0B131D"
ORANGE = "#E85929"
ORANGE_LIGHT = "#FFF0EB"
ORANGE_DARK = "#C84318"
TEAL = "#028090"
TEAL_LIGHT = "#E0F4F6"
MUTED = "#55606E"
MUTED_LIGHT = "#8C9BAE"
WHITE = "#FFFFFF"
BORDER_LIGHT = "#E2DBD0"


def font(name: str, size: int):
    return ImageFont.truetype(str(FONT_DIR / name), size)


F = {
    "title_hero": font("Poppins-ExtraBold.ttf", 52),
    "title_section": font("Poppins-Bold.ttf", 36),
    "title_card": font("Poppins-Bold.ttf", 26),
    "title_sub": font("Poppins-SemiBold.ttf", 22),
    "body_bold": font("Poppins-Bold.ttf", 20),
    "body_med": font("Poppins-Medium.ttf", 19),
    "body_reg": font("Poppins-Regular.ttf", 18),
    "caption": font("Poppins-Medium.ttf", 16),
    "pill_bold": font("Poppins-Bold.ttf", 17),
    "pill_med": font("Poppins-SemiBold.ttf", 15),
    "brand": font("Poppins-SemiBold.ttf", 20),
    "tag": font("Poppins-Bold.ttf", 18),
    "num_badge": font("Poppins-ExtraBold.ttf", 28),
}


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lerp(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient_vertical(im: Image.Image, top: str, bottom: str, x0=0, y0=0, x1=None, y1=None):
    d = ImageDraw.Draw(im)
    x1 = x1 if x1 is not None else im.width
    y1 = y1 if y1 is not None else im.height
    top_rgb, bot_rgb = hex_to_rgb(top), hex_to_rgb(bottom)
    for y in range(y0, y1):
        t = (y - y0) / max(1, (y1 - y0 - 1))
        color = lerp(top_rgb, bot_rgb, t)
        d.line([(x0, y), (x1, y)], fill=color)


def rounded_rectangle_gradient(im: Image.Image, box: tuple[int, int, int, int], radius: int, top: str, bottom: str):
    x1, y1, x2, y2 = box
    mask = Image.new("L", (im.width, im.height), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle(box, radius=radius, fill=255)
    grad = Image.new("RGB", (im.width, im.height))
    gradient_vertical(grad, top, bottom, x0=x1, y0=y1, x1=x2, y1=y2)
    im.paste(grad, (0, 0), mask)


def soft_shadow_card(im: Image.Image, box: tuple[int, int, int, int], radius: int, alpha=50, blur=22, offset=(0, 10), color=(7, 23, 38)):
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


def paste_logo(im: Image.Image, x=90, y=70, h=52, white_version=False):
    logo_path = LOGO_WHITE if white_version else LOGO_TRANSPARENT
    if logo_path.exists():
        logo = Image.open(logo_path).convert("RGBA")
        aspect = logo.width / logo.height
        w = int(h * aspect)
        logo = logo.resize((w, h), Image.Resampling.LANCZOS)
        im.paste(logo, (x, y), logo)


def footer(im: Image.Image, page="01/05", tag="Naskah Social OS", dark=False):
    d = ImageDraw.Draw(im)
    c_brand = CREAM if dark else INK
    c_tag = ORANGE if dark else ORANGE
    c_page = MUTED_LIGHT if dark else MUTED
    d.text((90, H - 75), "naskah.fk", font=F["brand"], fill=c_brand)
    d.text((540, H - 75), tag, font=F["pill_med"], fill=c_tag, anchor="mt")
    d.text((W - 90, H - 75), page, font=F["brand"], fill=c_page, anchor="ra")


def pill_badge(d: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, bg: str, fg: str, pad_x=16, pad_y=6, bold=True):
    x, y = xy
    f = F["pill_bold"] if bold else F["pill_med"]
    bbox = d.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    box = (x, y, x + tw + pad_x * 2, y + th + pad_y * 2)
    r = (th + pad_y * 2) // 2
    d.rounded_rectangle(box, radius=r, fill=bg)
    d.text((x + pad_x, y + pad_y - 1), text, font=f, fill=fg)
    return box[2]  # returns next x


# ==============================================================================
# CONCEPT 1: DENSE BENTO MATRIX — CHEATSHEET UJI STATISTIK
# ==============================================================================
def render_concept_1_dense_bento():
    im = Image.new("RGB", (W, H), CREAM)
    gradient_vertical(im, "#FDFBF7", "#EFE8DC")
    paste_logo(im, x=90, y=65, h=50)

    d = ImageDraw.Draw(im)
    pill_badge(d, (200, 72), "CHEATSHEET METPEN #04", ORANGE, WHITE, pad_x=14, pad_y=4)

    # Title & Hook
    d.text((90, 140), "Panduan Cepat Uji Hipotesis", font=F["title_hero"], fill=INK)
    d.text((90, 205), "Jangan sampai salah pilih uji di Bab 3 dan disidang habis-habisan!", font=F["body_med"], fill=MUTED)

    # 4 Detailed Bento Cards
    cards_data = [
        {
            "box": (90, 260, 525, 680),
            "num": "01",
            "title": "Komparatif 2 Kelompok",
            "type": "Skala Numerik / Kontinu",
            "accent": ORANGE,
            "items": [
                ("Normal (Parametrik)", "Independent T-Test"),
                ("Tidak Normal (Non-Par)", "Mann-Whitney U Test"),
                ("Berpasangan (Pre-Post)", "Paired T-Test / Wilcoxon"),
            ],
            "rule": "Wajib uji Saphiro-Wilk / Kolmogorov dulu!",
        },
        {
            "box": (555, 260, 990, 680),
            "num": "02",
            "title": "Komparatif Kategorik",
            "type": "Tabel 2x2 / Baris x Kolom",
            "accent": TEAL,
            "items": [
                ("Tabel 2x2 Standar", "Chi-Square (Pearson)"),
                ("Expected Count < 5", "Fisher's Exact Test"),
                ("Tabel > 2x2 (>2 klp)", "Kolmogorov-Smirnov / Chi-Sq"),
            ],
            "rule": "Cek cell Expected: jika >20% <5 -> Fisher!",
        },
        {
            "box": (90, 710, 525, 1130),
            "num": "03",
            "title": "Korelatif / Hubungan",
            "type": "Melihat Derajat & Arah Hubungan",
            "accent": TEAL,
            "items": [
                ("Numerik vs Numerik", "Pearson (Normal) / Spearman"),
                ("Kategorik Ordinal", "Spearman / Gamma / Kendall"),
                ("Output Utama", "Koefisien r & P-value (<0.05)"),
            ],
            "rule": "r mendekati +1 / -1 = korelasi makin kuat.",
        },
        {
            "box": (555, 710, 990, 1130),
            "num": "04",
            "title": "Multivariat / Prediksi",
            "type": "Kontrol Variabel Confounding",
            "accent": ORANGE,
            "items": [
                ("Dependen Kategorik", "Regresi Logistik Biner"),
                ("Dependen Numerik", "Regresi Linear Berganda"),
                ("Survival (Waktu)", "Cox Proportional Hazard"),
            ],
            "rule": "Kandidat multivariat: P-value bivariat < 0.25!",
        },
    ]

    for c in cards_data:
        box = c["box"]
        im = soft_shadow_card(im, box, radius=24, alpha=45, blur=20, offset=(0, 8))
        rounded_rectangle_gradient(im, box, 24, "#FFFFFF", "#FAF6EE")
        d = ImageDraw.Draw(im)

        # Border
        d.rounded_rectangle(box, radius=24, outline=BORDER_LIGHT, width=2)

        # Header card
        d.rounded_rectangle((box[0] + 20, box[1] + 20, box[0] + 62, box[1] + 62), radius=10, fill=c["accent"])
        d.text((box[0] + 41, box[1] + 41), c["num"], font=F["pill_bold"], fill=WHITE, anchor="mm")

        d.text((box[0] + 75, box[1] + 22), c["title"], font=F["title_card"], fill=NAVY)
        d.text((box[0] + 75, box[1] + 54), c["type"], font=F["caption"], fill=MUTED)

        # Divider
        d.line([(box[0] + 20, box[1] + 88), (box[1] + 415, box[1] + 88)], fill=BORDER_LIGHT, width=1)

        # Content rows
        cur_y = box[1] + 105
        for condition, test_name in c["items"]:
            # bullet dot
            d.ellipse((box[0] + 22, cur_y + 6, box[0] + 30, cur_y + 14), fill=c["accent"])
            d.text((box[0] + 38, cur_y), condition, font=F["caption"], fill=MUTED)
            d.text((box[0] + 38, cur_y + 22), test_name, font=F["body_bold"], fill=INK)
            cur_y += 62

        # Pro-Rule pill footer inside card
        rule_box = (box[0] + 16, box[3] - 68, box[2] - 16, box[3] - 18)
        d.rounded_rectangle(rule_box, radius=12, fill=ORANGE_LIGHT if c["accent"] == ORANGE else TEAL_LIGHT)
        d.text((box[0] + 26, box[3] - 56), "💡 Rule:", font=F["pill_bold"], fill=c["accent"])
        d.text((box[0] + 90, box[3] - 56), c["rule"][:36] + "...", font=F["caption"], fill=INK)

    # Bottom actionable summary pill
    sum_box = (90, 1160, 990, 1235)
    im = soft_shadow_card(im, sum_box, radius=20, alpha=35, blur=14, offset=(0, 6))
    rounded_rectangle_gradient(im, sum_box, 20, NAVY, NAVY_LIGHT)
    d = ImageDraw.Draw(im)
    d.text((120, 1182), "📌 Golden Rule:", font=F["pill_bold"], fill=ORANGE)
    d.text((260, 1182), "Selalu tentukan Skala Variabel & Uji Normalitas sebelum buka SPSS!", font=F["body_med"], fill=WHITE)
    d.text((120, 1208), "Simpan cheatsheet ini untuk panduan analisis data naskah kamu.", font=F["caption"], fill=MUTED_LIGHT)

    footer(im, "02/05", "Cheatsheet Hipotesis")
    return im


# ==============================================================================
# CONCEPT 2: 5-STEP LAYERED TIMELINE — WORKFLOW LITERATURE REVIEW 5 HARI
# ==============================================================================
def render_concept_2_workflow_timeline():
    im = Image.new("RGB", (W, H), CREAM)
    gradient_vertical(im, "#FCFAF4", "#F2EBE0")
    paste_logo(im, x=90, y=65, h=50)

    d = ImageDraw.Draw(im)
    pill_badge(d, (200, 72), "WORKFLOW FRAMEWORK", TEAL, WHITE, pad_x=14, pad_y=4)

    # Title & Subtitle
    d.text((90, 135), "Literature Review 5 Hari", font=F["title_hero"], fill=INK)
    d.text((90, 200), "Dari 0 ide hingga 30+ jurnal internasional terpetakan rapi di Matriks Sintesis.", font=F["body_med"], fill=MUTED)

    steps = [
        {
            "day": "HARI 1",
            "title": "Perumusan PICO & Boolean Search Query",
            "sub": "PubMed • ScienceDirect • Scopus • Google Scholar",
            "detail": "Kunci: Gunakan sintaks '((Disease) AND (Intervention)) OR (Alternative)'. Catat MeSH Terms.",
            "tag": "Search Syntax",
            "bg_grad": ("#FFFFFF", "#FDF7F0"),
            "badge_bg": ORANGE,
        },
        {
            "day": "HARI 2",
            "title": "Screening Judul, Abstrak & Duplikasi",
            "sub": "Kriteria Inklusi & Eksklusi 5 Tahun Terakhir",
            "detail": "Import semua file .ris ke Rayyan / Mendeley. Singkirkan duplikat & filter abstrak non-relevan.",
            "tag": "PRISMA Flow",
            "bg_grad": ("#FFFFFF", "#F5FBFB"),
            "badge_bg": TEAL,
        },
        {
            "day": "HARI 3",
            "title": "Critical Appraisal & Uji Kualitas Jurnal",
            "sub": "JBI Checklist • Newcastle-Ottawa Scale (NOS)",
            "detail": "Nilai metodologi penelitian: Sample size, bias seleksi, instrumen validitas, & relevansi klinis.",
            "tag": "Quality Check",
            "bg_grad": ("#FFFFFF", "#FAF8F2"),
            "badge_bg": NAVY,
        },
        {
            "day": "HARI 4",
            "title": "Penyusunan Matriks Sintesis Excel",
            "sub": "Ekstraksi Data Terstruktur Antar Jurnal",
            "detail": "Kolom wajib: Penulis (Tahun), Desain, Sampel, Variabel, Hasil Utama, Research Gap, & Limitasi.",
            "tag": "Synthesis Matrix",
            "bg_grad": ("#FFFFFF", "#FDF7F0"),
            "badge_bg": ORANGE,
        },
        {
            "day": "HARI 5",
            "title": "Drafting Narasi Sintesis (Thematic Writing)",
            "sub": "Menghubungkan Benang Merah Antar Paper",
            "detail": "Jangan hanya meringkas per paper. Kelompokkan berdasarkan tema: 'Studi A sejalan dgn Studi B, tapi...' ",
            "tag": "Academic Draft",
            "bg_grad": ("#FFFFFF", "#F5FBFB"),
            "badge_bg": TEAL,
        },
    ]

    start_y = 255
    card_h = 160
    spacing = 20

    for idx, s in enumerate(steps):
        cy = start_y + idx * (card_h + spacing)
        box = (90, cy, 990, cy + card_h)

        # Soft shadow
        im = soft_shadow_card(im, box, radius=20, alpha=40, blur=18, offset=(0, 6))
        rounded_rectangle_gradient(im, box, 20, s["bg_grad"][0], s["bg_grad"][1])
        d = ImageDraw.Draw(im)
        d.rounded_rectangle(box, radius=20, outline=BORDER_LIGHT, width=2)

        # Left Day Badge
        d.rounded_rectangle((box[0] + 18, box[1] + 18, box[0] + 115, box[1] + 62), radius=12, fill=s["badge_bg"])
        d.text((box[0] + 66, box[1] + 40), s["day"], font=F["pill_bold"], fill=WHITE, anchor="mm")

        # Right Tag Pill
        d.rounded_rectangle((box[2] - 165, box[1] + 18, box[2] - 18, box[1] + 52), radius=10, fill=CREAM_DARK)
        d.text((box[2] - 91, box[1] + 35), s["tag"], font=F["caption"], fill=NAVY, anchor="mm")

        # Main Titles
        d.text((box[0] + 130, box[1] + 18), s["title"], font=F["title_card"], fill=NAVY)
        d.text((box[0] + 130, box[1] + 48), s["sub"], font=F["caption"], fill=MUTED)

        # Detail Box inner
        detail_box = (box[0] + 18, box[1] + 80, box[2] - 18, box[1] + 144)
        d.rounded_rectangle(detail_box, radius=10, fill="#FFFFFF", outline=BORDER_LIGHT, width=1)
        d.text((box[0] + 32, box[1] + 96), "👉 " + s["detail"][:105] + ("..." if len(s["detail"]) > 105 else ""), font=F["body_reg"], fill=INK)

    # Bottom Tip
    bottom_box = (90, 1165, 990, 1235)
    rounded_rectangle_gradient(im, bottom_box, 18, NAVY, NAVY_LIGHT)
    d = ImageDraw.Draw(im)
    d.text((120, 1188), "⚡ Output Akhir:", font=F["pill_bold"], fill=ORANGE)
    d.text((270, 1188), "Bab 2 Tinjauan Pustaka siap diserahkan ke Dosen Pembimbing!", font=F["body_med"], fill=WHITE)

    footer(im, "03/05", "Workflow Tinjauan Pustaka")
    return im


# ==============================================================================
# CONCEPT 3: DEEP NAVY DARK GLASS — PERBANDINGAN OR vs RR vs HR
# ==============================================================================
def render_concept_3_dark_comparison():
    im = Image.new("RGB", (W, H), NAVY)
    gradient_vertical(im, "#071726", "#0E243A")

    # Ambient Light Glows
    blob = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(blob)
    bd.ellipse((40, 160, 480, 600), fill=(232, 89, 41, 110))
    bd.ellipse((600, 500, 1040, 950), fill=(2, 128, 144, 100))
    blob = blob.filter(ImageFilter.GaussianBlur(80))
    im.paste(Image.alpha_composite(im.convert("RGBA"), blob).convert("RGB"), (0, 0))

    paste_logo(im, x=90, y=65, h=50, white_version=True)
    d = ImageDraw.Draw(im)
    pill_badge(d, (200, 72), "EPIDEMIOLOGI & BIOSTATISTIK", ORANGE, WHITE, pad_x=14, pad_y=4)

    # Headline
    d.text((90, 135), "OR vs RR vs Hazard Ratio", font=F["title_hero"], fill=CREAM)
    d.text((90, 200), "Tiga ukuran asosiasi klinis yang paling sering salah ditulis di naskah medis.", font=F["body_med"], fill="#9DB2C7")

    metrics = [
        {
            "abbr": "OR",
            "full": "Odds Ratio",
            "design": "Cross-Sectional / Case-Control",
            "formula": "Odds kasus terpapar / Odds kontrol terpapar",
            "interpretation": "OR = 2.4 (95% CI 1.3 - 4.2) -> Kelompok terpapar memiliki odds sakit 2.4x lebih tinggi dibanding kontrol.",
            "pitfall": "Jangan sebut '2.4 kali lebih berisiko' (itu definisi RR, bukan OR!).",
            "color": ORANGE,
        },
        {
            "abbr": "RR",
            "full": "Relative Risk (Risk Ratio)",
            "design": "Kohort Prospektif / RCT Trial",
            "formula": "Kumulatif Insidensi Terpapar / Insidensi Non-Terpapar",
            "interpretation": "RR = 1.8 (95% CI 1.1 - 2.9) -> Kelompok intervensi memiliki risiko 1.8x terkena outcome.",
            "pitfall": "HANYA boleh dipakai jika ada follow-up waktu untuk hitung insidensi baru!",
            "color": TEAL,
        },
        {
            "abbr": "HR",
            "full": "Hazard Ratio",
            "design": "Survival Analysis (Waktu Hingga Kejadian)",
            "formula": "Laju Hazard Kelompok A / Laju Hazard Kelompok B (Cox Reg)",
            "interpretation": "HR = 0.65 (95% CI 0.45 - 0.92) -> Terapi baru menurunkan laju kekambuhan sebesar 35% sepanjang periode observasi.",
            "pitfall": "Wajib sertakan median survival time & kurva Kaplan-Meier di Bab 4.",
            "color": "#F5B301",
        },
    ]

    start_y = 255
    card_h = 260
    spacing = 22

    for idx, m in enumerate(metrics):
        cy = start_y + idx * (card_h + spacing)
        box = (90, cy, 990, cy + card_h)

        # Frosted glass panel effect
        panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        pd = ImageDraw.Draw(panel)
        pd.rounded_rectangle(box, radius=22, fill=(255, 255, 255, 38))
        im = Image.alpha_composite(im.convert("RGBA"), panel).convert("RGB")
        d = ImageDraw.Draw(im)

        # Glass border
        d.rounded_rectangle(box, radius=22, outline=(255, 255, 255, 80), width=2)

        # Abbr Badge
        d.rounded_rectangle((box[0] + 24, box[1] + 24, box[0] + 110, box[1] + 85), radius=16, fill=m["color"])
        d.text((box[0] + 67, box[1] + 54), m["abbr"], font=F["title_section"], fill=WHITE, anchor="mm")

        # Full Name & Study Design
        d.text((box[0] + 128, box[1] + 24), m["full"], font=F["title_card"], fill=WHITE)
        d.text((box[0] + 128, box[1] + 58), "Desain: " + m["design"], font=F["body_bold"], fill="#A9C7DF")

        # Formula Pill Right
        d.rounded_rectangle((box[0] + 128, box[1] + 95, box[2] - 24, box[1] + 135), radius=10, fill=(0, 0, 0, 60))
        d.text((box[0] + 142, box[1] + 105), "Rumus: " + m["formula"], font=F["caption"], fill="#E3ECF3")

        # Interpretation Box
        d.text((box[0] + 24, box[1] + 152), "📊 Cara Interpretasi:", font=F["pill_bold"], fill=m["color"])
        d.text((box[0] + 24, box[1] + 178), m["interpretation"][:98], font=F["body_reg"], fill="#F0F4F8")
        if len(m["interpretation"]) > 98:
            d.text((box[0] + 24, box[1] + 202), m["interpretation"][98:], font=F["body_reg"], fill="#F0F4F8")

        # Warning / Pitfall bar at bottom of card
        d.line([(box[0] + 24, box[1] + 228), (box[2] - 24, box[1] + 228)], fill=(255, 255, 255, 30), width=1)
        d.text((box[0] + 24, box[1] + 234), "⚠️ Jebakan: " + m["pitfall"], font=F["caption"], fill="#FFD1BA" if m["color"] == ORANGE else "#D6F2F5")

    # Red Alert Box
    alert_box = (90, 1140, 990, 1225)
    d.rounded_rectangle(alert_box, radius=18, fill="#2A1412", outline=ORANGE, width=2)
    d.text((120, 1162), "🚫 Kesalahan Fatal Mahasiswa:", font=F["pill_bold"], fill=ORANGE)
    d.text((410, 1162), "Menyebut 'Risk / Risiko' pada penelitian Cross-Sectional.", font=F["body_bold"], fill=WHITE)
    d.text((120, 1192), "Cross-sectional HANYA mengukur prevalensi & odds, bukan insidensi risiko kumulatif.", font=F["caption"], fill="#D9A89C")

    footer(im, "04/05", "Biostatistik Kedokteran", dark=True)
    return im


# ==============================================================================
# CONCEPT 4: ANATOMI BAB 4 & 5 (ACC BLUEPRINT)
# ==============================================================================
def render_concept_4_editorial_anatomy():
    im = Image.new("RGB", (W, H), CREAM)
    gradient_vertical(im, "#FCFAF4", "#F0E7DA")
    paste_logo(im, x=90, y=65, h=50)

    d = ImageDraw.Draw(im)
    pill_badge(d, (200, 72), "ANATOMI NASKAH ACC", NAVY, WHITE, pad_x=14, pad_y=4)

    d.text((90, 135), "Blueprint Bab 4 & 5 yang Lolos ACC", font=F["title_hero"], fill=INK)
    d.text((90, 200), "Struktur penyajian data & narasi pembahasan yang tidak memberi celah revisi mayor.", font=F["body_med"], fill=MUTED)

    # 3 Major Sections
    sections = [
        {
            "box": (90, 255, 990, 520),
            "tag": "BAB 4 — HASIL",
            "title": "Penyajian Tabel Karakteristik & Analisis Bivariat",
            "points": [
                ("Format Tabel 3 Garis (Open Table)", "Tanpa garis vertikal. Header tebal, isi rapi rata kiri."),
                ("Pencantuman 95% Confidence Interval", "Jangan cuma P-value! Sertakan OR / RR + rentang 95% CI."),
                ("Narasi 1 Kalimat Padat Per Tabel", "'Terdapat hubungan signifikan antara X dan Y (p=0.012, OR=2.3)'"),
            ],
            "accent": ORANGE,
        },
        {
            "box": (90, 545, 990, 850),
            "tag": "BAB 5 — PEMBAHASAN",
            "title": "Rumus Emas 3 Paragraf Per Temuan Hipotesis",
            "points": [
                ("Paragraf 1: Temuan & Makna Klinis", "Jelaskan apa arti angka statistikmu bagi pasien/populasi."),
                ("Paragraf 2: Komparasi Penelitian Terkait", "Bandingkan dgn 3-5 jurnal: Apakah sejalan? Jika beda, kenapa?"),
                ("Paragraf 3: Mekanisme Biologis / Patofisiologi", "Jelaskan mekanisme biologis / teori yang mendasari hasil."),
            ],
            "accent": TEAL,
        },
        {
            "box": (90, 875, 990, 1120),
            "tag": "BAB 5 — KETERBATASAN",
            "title": "Menuliskan Keterbatasan (Limitation) Tanpa Terlihat Lemah",
            "points": [
                ("Akui Bias Desain Secara Jujur", "Misal: recall bias pada case-control, atau unmeasured confounding."),
                ("Jelaskan Upaya Pengendaliannya", "Bagaimana kamu meminimalisir bias tersebut saat pengumpulan data."),
                ("Rekomendasi Riset Lanjutan", "Arahkan apa yang harus diperbaiki oleh peneliti berikutnya."),
            ],
            "accent": NAVY,
        },
    ]

    for s in sections:
        box = s["box"]
        im = soft_shadow_card(im, box, radius=22, alpha=40, blur=18, offset=(0, 6))
        rounded_rectangle_gradient(im, box, 22, "#FFFFFF", "#FAF5EC")
        d = ImageDraw.Draw(im)
        d.rounded_rectangle(box, radius=22, outline=BORDER_LIGHT, width=2)

        # Header Badge
        d.rounded_rectangle((box[0] + 20, box[1] + 18, box[0] + 230, box[1] + 52), radius=10, fill=s["accent"])
        d.text((box[0] + 125, box[1] + 35), s["tag"], font=F["pill_bold"], fill=WHITE, anchor="mm")

        d.text((box[0] + 250, box[1] + 20), s["title"][:42] + ("..." if len(s["title"]) > 42 else ""), font=F["title_card"], fill=NAVY)

        d.line([(box[0] + 20, box[1] + 68), (box[2] - 20, box[1] + 68)], fill=BORDER_LIGHT, width=1)

        cur_y = box[1] + 82
        for p_title, p_desc in s["points"]:
            d.ellipse((box[0] + 24, cur_y + 6, box[0] + 32, cur_y + 14), fill=s["accent"])
            d.text((box[0] + 42, cur_y), p_title, font=F["body_bold"], fill=INK)
            d.text((box[0] + 42, cur_y + 24), p_desc, font=F["body_reg"], fill=MUTED)
            cur_y += 58

    # Quote box at bottom
    q_box = (90, 1145, 990, 1230)
    im = soft_shadow_card(im, q_box, radius=18, alpha=35, blur=14, offset=(0, 5))
    rounded_rectangle_gradient(im, q_box, 18, NAVY, NAVY_LIGHT)
    d = ImageDraw.Draw(im)
    d.text((120, 1168), "💬 Kata Penguji:", font=F["pill_bold"], fill=ORANGE)
    d.text((270, 1168), '"Mahasiswa yang paham pembahasannya, sidangnya selesai dalam 20 menit."', font=F["body_bold"], fill=WHITE)
    d.text((120, 1198), "Kuasai narasi bab 5, bukan cuma hafalan angka p-value.", font=F["caption"], fill=MUTED_LIGHT)

    footer(im, "05/05", "Blueprint Bab 4 & 5")
    return im


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    renders = {
        "01_dense_bento_cheatsheet": render_concept_1_dense_bento(),
        "02_workflow_timeline_5hari": render_concept_2_workflow_timeline(),
        "03_dark_comparison_or_rr_hr": render_concept_3_dark_comparison(),
        "04_editorial_anatomy_bab4_5": render_concept_4_editorial_anatomy(),
    }
    for name, im in renders.items():
        out = OUT_DIR / f"naskah_dense_{name}.jpg"
        im.convert("RGB").save(out, "JPEG", quality=95, optimize=True)
        print("SAVED:", out)


if __name__ == "__main__":
    main()
