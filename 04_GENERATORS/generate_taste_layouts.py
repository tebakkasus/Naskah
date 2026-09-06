import os, random, math
from PIL import Image, ImageDraw, ImageFont

font_dir = 'C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/fonts'
output_dir = 'C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/naskah-visuals'
os.makedirs(output_dir, exist_ok=True)

def f(weight, size):
    fname = f"Montserrat-{weight}.ttf"
    path = os.path.join(font_dir, fname)
    return ImageFont.truetype(path, size)

def add_paper_grain(img, amount=0.04):
    grain = Image.new("RGBA", img.size, (0,0,0,0))
    gdraw = ImageDraw.Draw(grain)
    w, h = img.size
    for _ in range(int(w * h * amount)):
        x = random.randint(0, w-1)
        y = random.randint(0, h-1)
        c = random.randint(0, 255)
        alpha = random.randint(6, 18)
        gdraw.point((x, y), fill=(c, c, c, alpha))
    img.paste(grain, (0,0), grain)
    return img

# ==============================================================================
# EXPLORATION A: "SWISS EDITORIAL POSTER"
# Karakter: Tipografi berani, garis pemisah halus asimetris, data density variatif,
# tidak ada box-box repetitif, murni kekuatan layout editorial layaknya majalah riset independen.
# ==============================================================================
def render_exploration_a():
    W, H = 1080, 1350
    img = Image.new("RGB", (W, H), color="#F4F1EA") # Warm museum paper
    draw = ImageDraw.Draw(img)

    # Top Minimal Bar: Running header majalah
    draw.text((70, 70), "NASKAH // RESEARCH OPERATING SYSTEM", font=f("ExtraBold", 20), fill="#1A1A1A")
    draw.text((860, 70), "VOL. 01 / ISS. 04", font=f("Medium", 18), fill="#8C887B")
    draw.line([(70, 105), (1010, 105)], fill="#D5D0C5", width=2)

    # Tag & Subject Area (Left column accent)
    draw.text((70, 140), "METHODOLOGY BRIEF", font=f("Bold", 18), fill="#2D6A4F")
    
    # Hero Title with massive typographic contrast
    draw.text((70, 185), "KENAPA BAB 3", font=f("ExtraBold", 64), fill="#1A1A1A")
    draw.text((70, 260), "KAMU SELALU", font=f("Light", 64), fill="#1A1A1A")
    draw.text((70, 335), "KENA BANTAI?", font=f("ExtraBold", 64), fill="#9C4121")

    # Lead paragraph - Editorial layout (tanpa kotak)
    lead = (
        "Bukan karena dosen penguji mencari-cari kesalahan.\n"
        "Tapi karena 9 dari 10 mahasiswa membuat 'Operational Definition'\n"
        "yang tidak bisa diukur secara objektif."
    )
    draw.text((70, 440), lead, font=f("Medium", 25), fill="#4A473E", spacing=10)

    # Middle Editorial Section: Vertical thin rule separator dividing 2 columns
    draw.line([(70, 560), (1010, 560)], fill="#D5D0C5", width=2)
    draw.line([(540, 580), (540, 1140)], fill="#D5D0C5", width=2)

    # Column Left: "Kesalahan Umum"
    draw.text((70, 590), "DIAGNOSA MASALAH", font=f("Bold", 20), fill="#9C4121")
    col1_text = (
        "1. Skala Data Ambigu\n"
        "Menulis 'Tingkat Kepatuhan: Baik,\n"
        "Cukup, Kurang' tanpa menetapkan\n"
        "cut-off score yang valid.\n\n"
        "2. Uji Statistik Tidak Sinkron\n"
        "Variabel numerik dipaksa jadi\n"
        "kategorik tanpa justifikasi klinis,\n"
        "membuat power penelitian turun."
    )
    draw.text((70, 640), col1_text, font=f("Regular", 22), fill="#383630", spacing=8)

    # Column Right: "Solusi Naskah"
    draw.text((570, 590), "SOLUSI TERUJI", font=f("Bold", 20), fill="#2D6A4F")
    col2_text = (
        "1. Kunci Cut-off dari Literatur\n"
        "Gunakan standar konsensus atau\n"
        "penelitian terdahulu bereputasi,\n"
        "bukan asumsi pribadi.\n\n"
        "2. Buat Matrix 1 Halaman\n"
        "Petakan: Variabel → Skala →\n"
        "Instrumen → Uji Statistik.\n"
        "Bawa saat bimbingan."
    )
    draw.text((570, 640), col2_text, font=f("Regular", 22), fill="#383630", spacing=8)

    # Bottom Editorial Footnote / Signature Bar
    draw.line([(70, 1160), (1010, 1160)], fill="#1A1A1A", width=3)
    draw.text((70, 1190), "Naskah — Trusted Academic Companion", font=f("Bold", 22), fill="#1A1A1A")
    draw.text((70, 1225), "Simpan insight ini untuk revisi metodologimu ↗", font=f("Regular", 19), fill="#736E65")
    draw.text((880, 1190), "SWIPE ➔", font=f("Bold", 20), fill="#2D6A4F")

    img = add_paper_grain(img)
    p = os.path.join(output_dir, "exploration_a_swiss_editorial.jpg")
    img.save(p, "JPEG", quality=95)
    return p

# ==============================================================================
# EXPLORATION B: "ASYMMETRIC NOTEBOOK / SPLIT CANVAS"
# Karakter: Bidang warna terbagi organik (dark tone + cream note block),
# seolah potongan catatan riset asli yang ditempel di meja kerja.
# ==============================================================================
def render_exploration_b():
    W, H = 1080, 1350
    # Base canvas: Dark slate charcoal #1E232A
    img = Image.new("RGB", (W, H), color="#1A1E24")
    draw = ImageDraw.Draw(img)

    # Top Dark Header
    draw.text((80, 75), "NASKAH // LOGBOOK", font=f("ExtraBold", 22), fill="#52B788")
    draw.text((870, 75), "ENTRY #08", font=f("Medium", 20), fill="#7B889B")

    # Punchy Dark Mode Headline
    draw.text((80, 135), "\"Bedanya P-Value", font=f("Light", 52), fill="#E2E8F0")
    draw.text((80, 205), "Signifikan vs Bermakna", font=f("ExtraBold", 52), fill="#FFFFFF")
    draw.text((80, 275), "Secara Klinis Apa Sih?\"", font=f("SemiBold", 46), fill="#52B788")

    # Embedded Cream Paper Sheet (Asymmetric, overlapping modern look)
    sheet_x0, sheet_y0, sheet_x1, sheet_y1 = 80, 360, 1000, 1140
    # Shadow/Border effect
    draw.rounded_rectangle([sheet_x0, sheet_y0, sheet_x1, sheet_y1], radius=16, fill="#FAF8F5")
    # Red margin line like actual lab notebook
    draw.line([(160, sheet_y0 + 20), (160, sheet_y1 - 20)], fill="#E8D5CE", width=2)

    # Content inside the Paper Sheet
    draw.text((195, 410), "STUDI KASUS:", font=f("Bold", 20), fill="#9C4121")
    draw.text((195, 445), "Obat A menurunkan tekanan darah 1 mmHg (p = 0.001).", font=f("SemiBold", 24), fill="#1A1E24")
    
    explanation = (
        "Secara Statistik (P-Value):\n"
        "Hasilnya sangat 'signifikan' karena sampelnya ribuan orang,\n"
        "sehingga selisih sekecil apapun bisa menghasilkan p < 0.05.\n\n"
        "Secara Klinis (Realita Medis):\n"
        "Turun 1 mmHg tidak berdampak nyata pada keselamatan pasien.\n"
        "Inilah kenapa dosen sering bertanya: 'Lalu apa maknanya?'"
    )
    draw.text((195, 500), explanation, font=f("Regular", 22), fill="#3E454F", spacing=8)

    # Divider inside note
    draw.line([(195, 750), (940, 750)], fill="#E5DFD5", width=2)

    # Takeaway key
    draw.text((195, 780), "PRINSIP EMAS PENELITIAN:", font=f("ExtraBold", 20), fill="#2D6A4F")
    takeaway = (
        "Jangan cuma bangga memamerkan p < 0.05 di seminar.\n"
        "Selalu sertakan Effect Size & Confidence Interval\n"
        "agar argumen risetmu tidak bisa dipatahkan penguji."
    )
    draw.text((195, 825), takeaway, font=f("Medium", 23), fill="#1A1E24", spacing=8)

    # Notebook bottom label
    draw.text((195, 1060), "Catatan Metodologi Naskah  •  Halaman 03", font=f("Medium", 18), fill="#8C887B")

    # Bottom Dark Action
    draw.text((80, 1210), "Naskah — Menemani proses akademikmu jadi lebih masuk akal.", font=f("Regular", 20), fill="#94A3B8")
    draw.text((80, 1250), "Simpan catatan ini untuk bab pembahasan kamu ↗", font=f("Bold", 22), fill="#52B788")

    img = add_paper_grain(img)
    p = os.path.join(output_dir, "exploration_b_asymmetric_notebook.jpg")
    img.save(p, "JPEG", quality=95)
    return p

# ==============================================================================
# EXPLORATION C: "CONTEMPORARY RESEARCH CARD / TYPOGRAPHIC FLUIDITY"
# Karakter: Bersih maksimal, tipografi besar sebagai elemen visual, micro-details,
# nomor indeks besar, garis-garis tipis struktural tanpa terasa seperti template Canva biasa.
# ==============================================================================
def render_exploration_c():
    W, H = 1080, 1350
    img = Image.new("RGB", (W, H), color="#FBFBFA") # Soft pure ivory
    draw = ImageDraw.Draw(img)

    # Minimal Top Anchor
    draw.text((80, 80), "NASKAH", font=f("ExtraBold", 24), fill="#111827")
    draw.text((210, 82), "/ 03 PROTOKOL", font=f("Medium", 20), fill="#9CA3AF")
    draw.text((860, 82), "DECISION TREE", font=f("Bold", 18), fill="#111827")

    # Big Statement Headline
    draw.text((80, 160), "3 Tanda Skripsimu", font=f("Light", 56), fill="#111827")
    draw.text((80, 230), "Sebenarnya Sudah Siap", font=f("ExtraBold", 56), fill="#111827")
    draw.text((80, 305), "Daftar Sempro.", font=f("ExtraBold", 56), fill="#2563EB") # Crisp Blue

    draw.text((80, 395), "Berhenti menunda karena merasa 'belum sempurna'. Cek 3 hal ini:", font=f("Regular", 24), fill="#4B5563")

    # 3 Structural Fluid Rows (Border bottom only - NO boxed containers)
    rows = [
        ("01", "Rumusan Masalah Terjawab oleh Variabel", "Tiap poin tujuan khusus di Bab 1 punya padanan uji di Bab 3."),
        ("02", "Kuesioner / Alat Ukur Berizin Jelas", "Sudah tahu apakah instrumen memakai uji validitas ulang atau baku."),
        ("03", "Data Primer/Sekunder Sudah Terkonfirmasi", "Bukan sekadar 'mau ambil data di RS X', tapi izin awal sudah aman.")
    ]

    ry = 480
    for num, title, desc in rows:
        draw.line([(80, ry), (1000, ry)], fill="#E5E7EB", width=2)
        
        # Giant Index Number on Left
        draw.text((80, ry + 25), num, font=f("ExtraBold", 54), fill="#93C5FD")
        
        # Content on Right
        draw.text((200, ry + 30), title, font=f("Bold", 26), fill="#111827")
        draw.text((200, ry + 75), desc, font=f("Regular", 21), fill="#6B7280", spacing=4)
        
        ry += 180

    draw.line([(80, ry), (1000, ry)], fill="#E5E7EB", width=2)

    # Quote Callout at bottom
    draw.text((80, ry + 50), "\"Proposal yang baik adalah proposal yang selesai dan diuji,", font=f("Medium", 24), fill="#1F2937")
    draw.text((80, ry + 85), "bukan yang tersimpan selamanya di laptop sebagai draf.\"", font=f("Bold", 24), fill="#2563EB")

    # Bottom Footer
    draw.line([(80, 1200), (1000, 1200)], fill="#111827", width=2)
    draw.text((80, 1235), "@naskah.id  •  Teman Diskusi Akademik", font=f("SemiBold", 22), fill="#111827")
    draw.text((820, 1235), "SIMPAN POST ↗", font=f("Bold", 20), fill="#2563EB")

    img = add_paper_grain(img, amount=0.02)
    p = os.path.join(output_dir, "exploration_c_fluid_editorial.jpg")
    img.save(p, "JPEG", quality=95)
    return p

pa = render_exploration_a()
pb = render_exploration_b()
pc = render_exploration_c()
print("Generated:")
print("A:", pa)
print("B:", pb)
print("C:", pc)
