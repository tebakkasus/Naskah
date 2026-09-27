"""
Week 3 Content Suite Generator & Carousel Renderer for Naskah.fk
Generates all 7 Approved Content Packages for Week 3 (28 Sep - 04 Oct 2026):
- carousel_config.json
- CAPTION_DAN_THREADS_*.md (Formatted with Instagram Captions & 3 Daily Threads)
- Renders 5-slide rich-density carousels + PREVIEW contact sheets
"""

import os
import sys
import json
import pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
APPROVED = ROOT / "06_CONTENT_PIPELINE" / "03_APPROVED"
APPROVED.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(ROOT / "04_GENERATORS"))
from generate_carousel_2026 import render_post

def make_carousel_preview(folder: pathlib.Path, preview_path: pathlib.Path, slug: str):
    slide_files = sorted(folder.glob(f"{slug}_*.jpg"))
    if not slide_files:
        return
    cell_w, cell_h = 360, 450
    spacing = 16
    pad = 24
    total_w = pad * 2 + len(slide_files) * cell_w + (len(slide_files) - 1) * spacing
    total_h = pad * 2 + cell_h
    
    sheet = Image.new("RGB", (total_w, total_h), "#071726") # Navy background
    for idx, sfile in enumerate(slide_files):
        im = Image.open(sfile).resize((cell_w, cell_h), Image.Resampling.LANCZOS)
        x = pad + idx * (cell_w + spacing)
        y = pad
        sheet.paste(im, (x, y))
    
    sheet.save(preview_path, "JPEG", quality=92)

WEEK_3_POSTS = [
    {
        "folder": "2026-09-28_post_w3_01_decision_tree_uji_hipotesis",
        "slug": "post_w3_01_decision_tree_uji_hipotesis",
        "date_str": "2026-09-28",
        "topic": "Decision Tree Uji Hipotesis FK",
        "tag": "Biostatistika FK",
        "config": {
            "tag": "Biostatistika FK",
            "cover": {
                "pill": "Metodologi Riset",
                "headline": [
                    "ALUR 30 DETIK",
                    "MILIH UJI HIPOTESIS",
                    "SKRIPSI FK"
                ],
                "mark_word_line": 2,
                "body": "Gausah ngafal 20 uji statistik. Ini alur tercepat nentuin uji di SPSS tanpa galau.",
                "items": [
                    {
                        "num": "01",
                        "title": "Skala Variabel",
                        "desc": "Kategorik (nominal/ordinal) vs Numerik"
                    },
                    {
                        "num": "02",
                        "title": "Hubungan Kelompok",
                        "desc": "Bebas (independen) vs Berpasangan (paired)"
                    },
                    {
                        "num": "03",
                        "title": "Uji Normalitas",
                        "desc": "Penentu mutlak jalur parametrik vs non-parametrik"
                    }
                ]
            },
            "formula": {
                "pill": "Decision Tree",
                "headline": [
                    "MATRIKS BIVARIAT",
                    "KEDOKTERAN"
                ],
                "body": "Pilih uji berdasarkan kombinasi variabel bebas dan terikat lo.",
                "steps": [
                    {
                        "pill": "Kat vs Kat",
                        "text": "Chi-Square (Alternatif: Fisher's Exact jika E<5)"
                    },
                    {
                        "pill": "Num 2 Kelompok",
                        "text": "T-Test (Normal) atau Mann-Whitney (Tidak Normal)"
                    },
                    {
                        "pill": "Num >2 Kelompok",
                        "text": "One-Way ANOVA (Normal) atau Kruskal-Wallis"
                    }
                ],
                "insight": "Golden Rule: Uji normalitas Shapiro-Wilk untuk N<50, Kolmogorov-Smirnov untuk N>=50 subjek."
            },
            "editorial": {
                "pill": "Pitfalls",
                "headline": [
                    "KESALAHAN FATAL",
                    "DI RUANG SIDANG"
                ],
                "mark_word_line": 1,
                "lead": "Hal yang bikin dospem biostatistika langsung mencoret Bab 4 lo:",
                "items": [
                    {
                        "num": "1",
                        "title": "SPSS Asal Run",
                        "desc": "Data ordinal dipaksa Independent T-Test demi p-value",
                        "emoji": "⚠️"
                    },
                    {
                        "num": "2",
                        "title": "Skip Uji Normalitas",
                        "desc": "Langsung uji parametrik padahal sebaran miring",
                        "emoji": "🚨"
                    },
                    {
                        "num": "3",
                        "title": "Expected Count Error",
                        "desc": "Sel Chi-Square <5 tapi tidak switch ke Fisher",
                        "emoji": "📉"
                    },
                    {
                        "num": "4",
                        "title": "Salah Paired vs Unpaired",
                        "desc": "Pre-post test tapi diuji independent t-test",
                        "emoji": "❌"
                    }
                ]
            },
            "callout": {
                "pill": "Mindset FK",
                "headline": [
                    "SPSS ITU HANYA",
                    "KALKULATOR 🧠"
                ],
                "lead": "Ingat prinsip dasar metodologi:",
                "quote": [
                    "SPSS itu cuma mesin hitung. Lo masukin nomor sepatu sama tekanan darah juga bakal keluar nilai p.",
                    "Yang nentuin riset lo sahih itu logika berpikir metodologinya, bukan klik software-nya."
                ],
                "body": "Pahami dulu skala variabel & hipotesis sebelum buka aplikasi statistik."
            },
            "cta": {
                "pill": "Free Deliverable",
                "headline": [
                    "DOWNLOAD PDF",
                    "DECISION TREE FK"
                ],
                "sub": "Lengkap dengan bagan alur & alternatif uji statistik.",
                "items": [
                    {
                        "num": "1",
                        "title": "Komen 'STATISTIK'",
                        "desc": "Admin DM file Decision Tree Uji Hipotesis FK HD"
                    },
                    {
                        "num": "2",
                        "title": "Save Postingan Ini",
                        "desc": "Buka lagi nanti pas masuk bab olah data Bab 4"
                    },
                    {
                        "num": "3",
                        "title": "Follow @naskah.fk",
                        "desc": "Edukasi riset klinis tanpa bahasa berbelit"
                    }
                ],
                "button": "KOMEN 'STATISTIK' DI BAWAH"
            }
        },
        "caption": """Banyak yang ngira olah data SPSS itu rumit karena harus hafal puluhan uji statistik. Padahal kuncinya cuma 2 pertanyaan:

1. Skala variabel lo apa? (Kategorik atau Numerik)
2. Hubungan kelompoknya gimana? (Bebas atau Berpasangan)

Begitu lo jawab dua ini + cek sebaran data normal atau nggak, uji statistik yang tepat bakal langsung ketemu otomatis.

Swipe sampai slide terakhir buat lihat matriks lengkap uji bivariat kedokteran!

---
Mau dapet file PDF **Decision Tree Pemilihan Uji Hipotesis FK** beresolusi tinggi buat panduan Bab 3 & 4?
Ketik **STATISTIK** di komentar, admin kirim link unduhnya langsung ke DM lo! 📩

#skripsikedokteran #anakfk #kedokteran #biostatistik #ujistatistik #spss #naskahfk #pejuangskripsi""",
        "thread_1": """Cara paling cepet bikin dospem metodologi geleng-geleng kepala:

Data ordinal lo paksa uji Independent T-Test cuma karena 'di SPSS hasilnya keluar angka p-value'.

SPSS itu cuma kalkulator. Lo masukin nomor sepatu sama tekanan darah juga bakal keluar p-value.

Yang nentuin validitas riset itu logika desain metodologi lo, bukan software-nya.

Cheat sheet alur milih uji statistik ada di IG hari ini ➜ @naskah.fk""",
        "thread_2_text": """Cheat sheet alur 30 detik milih uji hipotesis skripsi FK tanpa galau SPSS.

Save sebelum lo olah data malam ini. Full breakdown ➜ @naskah.fk""",
        "thread_3": """Hal yang sering bikin mahasiswa FK panik pas olah data:

"Dok, data saya ngga berdistribusi normal, masa harus ganti judul?"

Gausah overthinking. Tinggal turun ke uji non-parametrik (Mann-Whitney / Wilcoxon / Kruskal-Wallis) atau lakukan transformasi data kalau memang ada justifikasinya.

Data miring itu hal biasa di dunia medis nyata, bukan aib akademik.

Lo lagi di tahap uji apa sekarang? Drop di reply, kita bedah bareng 👇"""
    },
    {
        "folder": "2026-09-29_post_w3_02_cara_baca_odds_ratio_rr_ci",
        "slug": "post_w3_02_cara_baca_odds_ratio_rr_ci",
        "date_str": "2026-09-29",
        "topic": "Cara Baca OR, RR, dan 95% CI",
        "tag": "Epidemiologi Klinis",
        "config": {
            "tag": "Epidemiologi Klinis",
            "cover": {
                "pill": "Analisis Risiko",
                "headline": [
                    "CARA BACA OR, RR",
                    "DAN 95% CI",
                    "BIAR GA BENGONG"
                ],
                "mark_word_line": 2,
                "body": "Panduan cepat memahami ukuran asosiasi & confidence interval saat ujian skripsi.",
                "items": [
                    {
                        "num": "01",
                        "title": "Odds Ratio (OR)",
                        "desc": "Rasio peluang paparan pada desain Case-Control"
                    },
                    {
                        "num": "02",
                        "title": "Relative Risk (RR)",
                        "desc": "Rasio insiden penyakit pada desain Cohort/RCT"
                    },
                    {
                        "num": "03",
                        "title": "The Null Value (1.0)",
                        "desc": "Penentu kemaknaan klinis rentang 95% CI"
                    }
                ]
            },
            "formula": {
                "pill": "Aturan Angka 1",
                "headline": [
                    "ATURAN BAKU",
                    "THE NULL VALUE"
                ],
                "body": "Lihat apakah rentang Confidence Interval melewati angka 1.0.",
                "steps": [
                    {
                        "pill": "OR > 1.0",
                        "text": "Faktor Risiko (Meningkatkan kejadian sakit)"
                    },
                    {
                        "pill": "OR < 1.0",
                        "text": "Faktor Protektif (Menurunkan kejadian sakit)"
                    },
                    {
                        "pill": "CI Lewat 1.0",
                        "text": "Tidak Signifikan (Misal CI 0.85 - 2.40)"
                    }
                ],
                "insight": "Meskipun nilai OR = 2.5, kalau 95% CI-nya 0.90 - 4.50, hasilnya TIDAK BERMAKNA secara statistik!"
            },
            "editorial": {
                "pill": "Desain Studi",
                "headline": [
                    "JANGAN SALAH",
                    "PASANG UKURAN"
                ],
                "mark_word_line": 1,
                "lead": "Cocokkan ukuran asosiasi dengan desain metodologi penelitian lo:",
                "items": [
                    {
                        "num": "1",
                        "title": "Case-Control",
                        "desc": "Wajib lapor Odds Ratio (OR) & 95% CI",
                        "emoji": "🔍"
                    },
                    {
                        "num": "2",
                        "title": "Cohort / RCT",
                        "desc": "Wajib lapor Relative Risk (RR) / Risk Ratio",
                        "emoji": "📈"
                    },
                    {
                        "num": "3",
                        "title": "Cross-Sectional",
                        "desc": "Lapor Prevalence Odds Ratio (POR) / PR",
                        "emoji": "📊"
                    },
                    {
                        "num": "4",
                        "title": "Multivariat Logistik",
                        "desc": "Lapor Adjusted Odds Ratio (aOR) terkontrol",
                        "emoji": "🎯"
                    }
                ]
            },
            "callout": {
                "pill": "Script Ujian",
                "headline": [
                    "CONTOH KALIMAT",
                    "PELAPORAN BAB 4 📝"
                ],
                "lead": "Format baku menjawab penguji sidang:",
                "quote": [
                    "\"Berdasarkan analisis multivariat regresi logistik, pasien dengan riwayat X memiliki risiko 2,45 kali lebih tinggi mengalami komplikasi Y secara signifikan (aOR = 2,45; 95% CI: 1,28 – 4,69; p = 0,007).\""
                ],
                "body": "Sebutkan nilai estimator titik (OR), rentang presisi (95% CI), dan nilai p eksak."
            },
            "cta": {
                "pill": "Free Deliverable",
                "headline": [
                    "CHEAT SHEET OR, RR",
                    "& 95% CI FK"
                ],
                "sub": "Lengkap dengan tabel interpretasi dan contoh script jawaban sidang.",
                "items": [
                    {
                        "num": "1",
                        "title": "Komen 'ODDSRATIO'",
                        "desc": "Admin kirim Cheat Sheet PDF langsung ke DM"
                    },
                    {
                        "num": "2",
                        "title": "Share ke Teman",
                        "desc": "Bantu rekan stase/skripsi yang lagi olah data"
                    },
                    {
                        "num": "3",
                        "title": "Follow @naskah.fk",
                        "desc": "Edukasi riset klinis & statistik kedokteran"
                    }
                ],
                "button": "KOMEN 'ODDSRATIO' DI BAWAH"
            }
        },
        "caption": """Banyak mahasiswa FK panik pas ditanya penguji: "Kenapa kamu bilang variabel ini faktor risiko padahal nilai p = 0.08 dan 95% CI-nya 0.90 sampai 3.20?"

Kuncinya ada di Aturan Angka 1 (The Null Value).

Kalau rentang 95% Confidence Interval masih menyeberangi angka 1.0 (misalnya batas bawah < 1 dan batas atas > 1), itu artinya secara statistik belum terbukti ada perbedaan risiko yang bermakna!

Swipe 5 slide ini buat kuasai cara baca OR, RR, dan CI dalam 3 menit!

---
Ketik **ODDSRATIO** di komen buat download **Cheat Sheet Interpretasi OR, RR, & 95% CI** format PDF siap pakai! 📩

#skripsifk #biostatistik #oddsratio #relativerisk #confidenceinterval #kedokteran #naskahfk #mahasiswafk""",
        "thread_1": """Penguji sidang: "Kenapa kamu bilang variabel ini faktor risiko padahal 95% CI-nya 0.90 sampai 3.20?"

Mahasiswa: *keringat dingin mengalir deras*

Rule of thumb: Kalau Confidence Interval masih nyebrang angka 1, penelitian lo belum bisa buktiin adanya hubungan yang bermakna. Titik.""",
        "thread_2_text": """Panduan visual cara baca Odds Ratio (OR), Relative Risk (RR), dan 95% Confidence Interval.

Save sebelum ujian semhas! Full breakdown ➜ @naskah.fk""",
        "thread_3": """Bedanya Case-Control vs Cohort dalam 1 tarikan napas:

Case-Control: Mulai dari orang yang udah sakit vs sehat ➜ Mundur ke belakang nyari paparan ➜ Ukurannya Odds Ratio (OR).

Cohort: Mulai dari orang terpapar vs tidak terpapar ➜ Ikuti ke depan nunggu siapa yang sakit ➜ Ukurannya Relative Risk (RR).

Cross-Sectional: Ukur paparan & penyakit serentak di satu waktu ➜ Ukurannya Prevalence Odds Ratio (POR) atau Prevalence Ratio (PR).

Jangan sampai skripsinya Case-Control tapi laporannya nulis Relative Risk ya."""
    },
    {
        "folder": "2026-09-30_post_w3_03_anatomi_tabel1_karakteristik_subjek",
        "slug": "post_w3_03_anatomi_tabel1_karakteristik_subjek",
        "date_str": "2026-09-30",
        "topic": "Anatomi Tabel 1 Karakteristik Subjek FK",
        "tag": "Academic Publishing",
        "config": {
            "tag": "Academic Publishing",
            "cover": {
                "pill": "Standar Jurnal",
                "headline": [
                    "ANATOMI TABEL 1",
                    "KARAKTERISTIK SUBJEK",
                    "STANDAR FK"
                ],
                "mark_word_line": 2,
                "body": "Format tabel baku standar jurnal internasional & skripsi FK yang auto lolos review.",
                "items": [
                    {
                        "num": "01",
                        "title": "Open-Table Standard",
                        "desc": "3 garis horizontal utama, zero garis vertikal"
                    },
                    {
                        "num": "02",
                        "title": "Mean vs Median",
                        "desc": "Mean ± SD (Normal) vs Median (IQR) (Miring)"
                    },
                    {
                        "num": "03",
                        "title": "Footnote Lengkap",
                        "desc": "Definisi seluruh singkatan dan uji statistik pembanding"
                    }
                ]
            },
            "formula": {
                "pill": "Format Open-Table",
                "headline": [
                    "STRUKTUR 3 GARIS",
                    "BEBAS KOTAK ABU"
                ],
                "body": "Gunakan aturan tabel terbuka sesuai standar AMA / Vancouver style.",
                "steps": [
                    {
                        "pill": "Garis 1",
                        "text": "Border atas tabel (Top border 1 pt solid)"
                    },
                    {
                        "pill": "Garis 2",
                        "text": "Border bawah baris header kolom (0.5 pt)"
                    },
                    {
                        "pill": "Garis 3",
                        "text": "Border penutup paling bawah tabel (1 pt)"
                    }
                ],
                "insight": "Dilarang keras memakai garis vertikal (tegak) atau shading warna warni di dalam tabel ilmiah!"
            },
            "editorial": {
                "pill": "Aturan Variabel",
                "headline": [
                    "CARA MENYAJIKAN",
                    "NILAI DATA"
                ],
                "mark_word_line": 1,
                "lead": "Format penulisan data berdasarkan jenis sebaran di Tabel 1:",
                "items": [
                    {
                        "num": "1",
                        "title": "Numerik Normal",
                        "desc": "Tuliskan Mean ± SD (misal: Usia: 48,2 ± 7,5 th)",
                        "emoji": "📏"
                    },
                    {
                        "num": "2",
                        "title": "Numerik Tidak Normal",
                        "desc": "Tuliskan Median (IQR) atau Median (Min-Max)",
                        "emoji": "📊"
                    },
                    {
                        "num": "3",
                        "title": "Kategorik",
                        "desc": "Tuliskan Frekuensi n (%) (misal: 35 (58,3%))",
                        "emoji": "👥"
                    },
                    {
                        "num": "4",
                        "title": "Nilai p Pembanding",
                        "desc": "Tulis 3 desimal eksak + tanda bintang uji",
                        "emoji": "⭐"
                    }
                ]
            },
            "callout": {
                "pill": "Dosa Bab 4",
                "headline": [
                    "JANGAN SCREENSHOT",
                    "OUTPUT SPSS! 🛑"
                ],
                "lead": "Pesan penting buat mahasiswa FK:",
                "quote": [
                    "Output SPSS yang berlatar abu-abu dan bergaris kotak tebal itu lembar kerja komputasi, bukan tabel skripsi.",
                    "Salin angkanya ke format Word Open-Table bersih. Dospem langsung respect dalam 5 detik pertama."
                ],
                "body": "Tabel yang rapi mencerminkan kualitas peneliti yang teliti."
            },
            "cta": {
                "pill": "Free Deliverable",
                "headline": [
                    "DOWNLOAD TEMPLATE",
                    "WORD TABEL 1 FK"
                ],
                "sub": "Format Word (.docx) siap pakai dengan formula open-table dan footnote.",
                "items": [
                    {
                        "num": "1",
                        "title": "Komen 'TABEL1'",
                        "desc": "Admin kirim template Word langsung ke DM"
                    },
                    {
                        "num": "2",
                        "title": "Edit Cepat",
                        "desc": "Tinggal ganti variabel & isi data penelitian lo"
                    },
                    {
                        "num": "3",
                        "title": "Follow @naskah.fk",
                        "desc": "Tips penulisan karya ilmiah kedokteran"
                    }
                ],
                "button": "KOMEN 'TABEL1' DI BAWAH"
            }
        },
        "caption": """Hal pertama yang dicek dosen pembimbing dan penguji pas buka Bab 4 adalah Tabel 1 (Karakteristik Subjek).

Kalau Tabel 1 lo masih hasil screenshot output SPSS abu-abu bergaris kotak, dospem langsung tau lo ngerjainnya buru-buru.

Standar baku jurnal terakreditasi dan skripsi FK mewajibkan format Open-Table (hanya 3 garis horizontal, tanpa garis vertikal, plus footnote uji pembanding).

Pelajari anatomi lengkapnya di carousel ini!

---
Ketik **TABEL1** di kolom komentar, admin kirim file template Microsoft Word Tabel Karakteristik Subjek siap edit ke DM lo! 📩

#skripsifk #tabelpenelitian #bab4skripsi #kedokteran #karyatulisilmiah #naskahfk #mahasiswatingkatakhir""",
        "thread_1": """Ciri-ciri skripsi yang Bab 4-nya masih mentah:

Tabel hasil output SPSS di-screenshot langsung terus ditempel ke Microsoft Word lengkap sama background abu-abu dan garis kotaknya 😭

Jangan ya dek ya. Dosen penguji langsung tau lo ngerjainnya H-1 jam bimbingan.""",
        "thread_2_text": """Anatomi Tabel 1 Karakteristik Subjek Standar Jurnal & Skripsi FK.

Format Open-Table yang bikin dospem auto respect. Full guide ➜ @naskah.fk""",
        "thread_3": """Reminder buat yang lagi nulis Bab 4:

Tabel itu tugasnya MERINGKAS data, bukan menduplikasi teks narasi.

Kalau di dalam tabel udah ada angka lengkap: Usia 20-25 tahun = 40 (80%), di teks bawahnya gausah lo sebutin lagi satu-satu semua baris tabelnya.

Teks narasi fungsinya cuma menyorot key finding atau tren yang paling penting. Hemat halaman dan ga bikin penguji ngantuk."""
    },
    {
        "folder": "2026-10-01_post_w3_04_pertanyaan_jebakan_sidang_skripsi_fk",
        "slug": "post_w3_04_pertanyaan_jebakan_sidang_skripsi_fk",
        "date_str": "2026-10-01",
        "topic": "5 Pertanyaan Jebakan Sidang Skripsi FK",
        "tag": "Defense Strategy",
        "config": {
            "tag": "Defense Strategy",
            "cover": {
                "pill": "Sidang Meja Hijau",
                "headline": [
                    "5 PERTANYAAN JEBAKAN",
                    "PENGUJI SIDANG FK",
                    "(+ CARA JAWABNYA)"
                ],
                "mark_word_line": 2,
                "body": "Bocoran pertanyaan maut penguji sidang skripsi kedokteran dan script jawaban taktis.",
                "items": [
                    {
                        "num": "01",
                        "title": "Alasan Rumus Sampel",
                        "desc": "Kenapa pakai rumus estimasi proporsi vs uji hipotesis"
                    },
                    {
                        "num": "02",
                        "title": "Kriteria Eksklusi",
                        "desc": "Jebakan nulis 'pasien tidak bersedia' di eksklusi"
                    },
                    {
                        "num": "03",
                        "title": "Kontrol Confounder",
                        "desc": "Cara mengatasi variabel perancu di Bab 3 & 4"
                    }
                ]
            },
            "formula": {
                "pill": "Jebakan Maut",
                "headline": [
                    "3 JEBAKAN UTAMA",
                    "RUANG SIDANG"
                ],
                "body": "Hafalkan pola pertanyaan ini sebelum masuk ruang ujian.",
                "steps": [
                    {
                        "pill": "Jebakan 1",
                        "text": "Kenapa kriteria eksklusi lo kebalikan dari inklusi?"
                    },
                    {
                        "pill": "Jebakan 2",
                        "text": "Bagaimana lo menjamin data kuesioner bebas bias recall?"
                    },
                    {
                        "pill": "Jebakan 3",
                        "text": "Kenapa hasil bivariat lo bertentangan dengan teori?"
                    }
                ],
                "insight": "Kunci: Jawab selalu berbasis metodologi, batas studi, dan justifikasi literatur rujukan."
            },
            "editorial": {
                "pill": "Script Jawaban",
                "headline": [
                    "SCRIPT TACTICAL",
                    "MENJAWAB PENGUJI"
                ],
                "mark_word_line": 1,
                "lead": "Contoh respon ilmiah saat dicecar penguji sidang meja hijau:",
                "items": [
                    {
                        "num": "1",
                        "title": "Soal Eksklusi",
                        "desc": "\"Pasien menolak ikut adalah refusal to participate, bukan kriteria eksklusi biologis.\"",
                        "emoji": "🛡️"
                    },
                    {
                        "num": "2",
                        "title": "Soal Confounder",
                        "desc": "\"Kami kontrol melalui restriksi sampel dan model regresi logistik ganda.\"",
                        "emoji": "🎯"
                    },
                    {
                        "num": "3",
                        "title": "Soal Sampel Drop",
                        "desc": "\"Kami telah antisipasi dengan penambahan 10% dropout correction factor.\"",
                        "emoji": "📊"
                    },
                    {
                        "num": "4",
                        "title": "Saat Buntu",
                        "desc": "\"Terima kasih masukannya Prof, ini menjadi limitasi riset kami untuk studi lanjutan.\"",
                        "emoji": "🙏"
                    }
                ]
            },
            "callout": {
                "pill": "Golden Rule",
                "headline": [
                    "JANGAN PERNAH",
                    "NGARANG FAKTA! ⚠️"
                ],
                "lead": "Etika mutlak di ruang sidang:",
                "quote": [
                    "Kalau lo beneran ngga tahu jawabannya, akui dengan santun sebagai keterbatasan metodologi dan catat sebagai masukan perbaikan.",
                    "Mengarang teori palsu di depan dokter konsulen adalah tiket tercepat menuju sidang ulang."
                ],
                "body": "Kejujuran akademik dinilai jauh lebih tinggi daripada sok tahu."
            },
            "cta": {
                "pill": "Free Deliverable",
                "headline": [
                    "BANK 15 PERTANYAAN",
                    "SIDANG SKRIPSI FK"
                ],
                "sub": "Lengkap dengan script contekan jawaban taktis untuk sempro dan sidang hasil.",
                "items": [
                    {
                        "num": "1",
                        "title": "Komen 'SIDANG'",
                        "desc": "Admin kirim file PDF Bank Pertanyaan Sidang ke DM"
                    },
                    {
                        "num": "2",
                        "title": "Simulasi Bareng Teman",
                        "desc": "Latihan tanya jawab sebelum hari H ujian"
                    },
                    {
                        "num": "3",
                        "title": "Follow @naskah.fk",
                        "desc": "Tips & survival guide lengkap anak kedokteran"
                    }
                ],
                "button": "KOMEN 'SIDANG' DI BAWAH"
            }
        },
        "caption": """Sidang skripsi FK itu 80% menguji ketahanan mental dan pemahaman metodologi lo, cuma 20% yang ngetes hafalan rumus.

Banyak mahasiswa yang sebenernya naskahnya bagus tapi langsung grogi dan blank karena kena 'pertanyaan jebakan' standar dospem penguji.

Misalnya: "Kenapa kriteria eksklusi kamu isinya pasien yang menolak tanda tangan informed consent?" (Ini salah kaprah fatal!).

Geser slide buat lihat 5 pertanyaan jebakan paling sering muncul + script cara menjawabnya dengan tenang!

---
Komen **SIDANG** di bawah, admin DM file PDF **Bank 15 Pertanyaan Jebakan Sidang Skripsi FK & Script Jawaban Taktis**! 📩

#sidangskripsi #sempro #semhas #kedokteran #anakfk #skripsikedokteran #naskahfk #pejuangkoas""",
        "thread_1": """Hal terlarang di ruang sidang skripsi FK:

Debat dospem penguji pake kalimat: "Tapi kata cutting saya tahun lalu boleh kok dok."

Auto masuk stase revisi 3 bulan tanpa ujung.""",
        "thread_2_text": """5 Pertanyaan Jebakan Penguji Sidang Skripsi FK & Kunci Jawabannya.

Pelajari polanya sebelum maju sidang meja hijau ➜ @naskah.fk""",
        "thread_3": """Pengalaman paling berharga pas sidang skripsi FK:

Penguji itu 80% ngetes mental dan pemahaman dasar, cuma 20% ngetes detail angka desimal.

Begitu lo nunjukin lo paham KENAPA lo milih metode itu, nada suara mereka langsung berubah dari menginterogasi jadi diskusi ilmiah.

Siapa yang minggu ini atau bulan depan mau maju sempro/semhas? Absen di reply 👇"""
    },
    {
        "folder": "2026-10-02_post_w3_05_struktur_ppt_sidang_10_menit",
        "slug": "post_w3_05_struktur_ppt_sidang_10_menit",
        "date_str": "2026-10-02",
        "topic": "Struktur PPT Sidang Skripsi FK 10 Menit",
        "tag": "Presentation Skills",
        "config": {
            "tag": "Presentation Skills",
            "cover": {
                "pill": "Teknik Presentasi",
                "headline": [
                    "PPT SIDANG FK",
                    "10 MENIT PADAT",
                    "ANTI-DITEGUR"
                ],
                "mark_word_line": 2,
                "body": "Formula alokasi 8-10 slide presentasi sidang skripsi kedokteran yang tajam dan efisien.",
                "items": [
                    {
                        "num": "01",
                        "title": "Alokasi Waktu Ketat",
                        "desc": "10 menit presentasi + 20 menit tanya jawab"
                    },
                    {
                        "num": "02",
                        "title": "Hierarki Visual",
                        "desc": "Tampilkan bagan & tabel kunci, bukan teks narasi"
                    },
                    {
                        "num": "03",
                        "title": "Opening & Closing",
                        "desc": "Kunci ketenangan mental di 60 detik pertama"
                    }
                ]
            },
            "formula": {
                "pill": "Alokasi Slide",
                "headline": [
                    "BLUEPRINT 10 MENIT",
                    "PRESENTASI SIDANG"
                ],
                "body": "Bagi waktu secara proporsional sesuai bobot penilaian penguji.",
                "steps": [
                    {
                        "pill": "Slide 1-3 (2 Min)",
                        "text": "Judul, Latar Belakang Klinis & Rumusan Masalah"
                    },
                    {
                        "pill": "Slide 4-5 (2 Min)",
                        "text": "Kerangka Konsep & Metodologi Inti Riset"
                    },
                    {
                        "pill": "Slide 6-8 (4 Min)",
                        "text": "Tabel 1 Karakteristik & Hasil Analisis Utama"
                    }
                ],
                "insight": "Sisa 2 menit terakhir: Pembahasan Kritis, Limitasi, Kesimpulan, dan Rekomendasi Klinis."
            },
            "editorial": {
                "pill": "Aturan Visual",
                "headline": [
                    "3 ATURAN MUTLAK",
                    "SLIDE SIDANG FK"
                ],
                "mark_word_line": 1,
                "lead": "Hindari kesalahan desain yang memicu kemarahan penguji:",
                "items": [
                    {
                        "num": "1",
                        "title": "Minimal Font 20pt",
                        "desc": "Jangan bikin konsulen nyipitin mata baca teks",
                        "emoji": "🔍"
                    },
                    {
                        "num": "2",
                        "title": "Pakai Flowchart",
                        "desc": "Ganti paragraf alur sampel dengan diagram STROBE",
                        "emoji": "🔄"
                    },
                    {
                        "num": "3",
                        "title": "Sorot Key Finding",
                        "desc": "Beri kotak penegas pada angka p-value & OR utama",
                        "emoji": "🎯"
                    },
                    {
                        "num": "4",
                        "title": "Jangan Baca Slide",
                        "desc": "Slide untuk penguji melihat, mulut lo untuk bercerita",
                        "emoji": "🗣️"
                    }
                ]
            },
            "callout": {
                "pill": "Pesan Penguji",
                "headline": [
                    "BUKAN TADARUS",
                    "SKRIPSI! 🛑"
                ],
                "lead": "Reaksi umum penguji saat melihat slide 40 halaman:",
                "quote": [
                    "\"Ini kamu mau presentasi hasil riset atau mau ngajak kami tadarus naskah skripsi?\"",
                    "Ringkas slide lo jadi 8-10 slide padat data. Tunjukkan penguasaan konsep, bukan kemampuan membaca teks."
                ],
                "body": "Presentasi yang efektif menghargai waktu penguji yang padat."
            },
            "cta": {
                "pill": "Free Deliverable",
                "headline": [
                    "TEMPLATE PPT SIDANG",
                    "SKRIPSI FK (16:9)"
                ],
                "sub": "Slide PowerPoint minimalis modern siap edit beserta panduan alokasi waktu.",
                "items": [
                    {
                        "num": "1",
                        "title": "Komen 'PPT'",
                        "desc": "Admin kirim template PPTX & PDF panduan ke DM"
                    },
                    {
                        "num": "2",
                        "title": "Tinggal Masukkan Data",
                        "desc": "Layout sudah disesuaikan standar sidang meja hijau"
                    },
                    {
                        "num": "3",
                        "title": "Follow @naskah.fk",
                        "desc": "Tips & template penulisan akademik kedokteran"
                    }
                ],
                "button": "KOMEN 'PPT' DI BAWAH"
            }
        },
        "caption": """Slide presentasi sidang skripsi FK 40 halaman itu mimpi buruk semua dosen penguji.

Alokasi presentasi sidang rata-rata cuma 10 sampai 15 menit. Kalau slide lo kebanyakan teks, baru sampai Bab 2 lo udah disuruh langsung loncat ke kesimpulan.

Formula ideal: Cukup 8 sampai 10 slide padat data dengan visual flowchart dan tabel ringkas.

Swipe buat lihat alokasi waktu per slide dan trik visualnya!

---
Ketik **PPT** di kolom komentar buat dapet **Template Slide Sidang Skripsi FK 10 Menit (.pptx)** plus PDF panduannya langsung ke DM lo! 📩

#sidangskripsi #presentasiskripsi #powerpoint #anakfk #kedokteran #naskahfk #pejuangkelulusan""",
        "thread_1": """Dosen penguji sidang pas liat slide mahasiswa isinya 5 paragraf copy-paste dari Bab 2:

👁️👄👁️ "Ini kamu mau presentasi atau mau ngajak saya tadarus jurnal?"

Ringkas slide lo. Tampilkan data dan alur pikir, bukan salinan skripsi.""",
        "thread_2_text": """Blueprint Struktur Slide PPT Sidang Skripsi FK 10 Menit.

Padat, visual, dan anti-ditegor penguji. Download template ➜ @naskah.fk""",
        "thread_3": """Kunci ketenangan di 10 menit presentasi sidang:

Latihan opening & closing sampai hafal di luar kepala.

Begitu 60 detik pertama lo lancar tanpa terbata-bata, detak jantung lo bakal stabil dan sisa presentasi bakal mengalir alami.

Ada yang punya ritual khusus sebelum maju sidang? Cerita di bawah ☕"""
    },
    {
        "folder": "2026-10-03_post_w3_06_bedah_hasil_tidak_signifikan_bab5",
        "slug": "post_w3_06_bedah_hasil_tidak_signifikan_bab5",
        "date_str": "2026-10-03",
        "topic": "Bedah Hasil Riset p > 0.05 di Bab 5",
        "tag": "Research Integrity",
        "config": {
            "tag": "Research Integrity",
            "cover": {
                "pill": "Pembahasan Bab 5",
                "headline": [
                    "HASIL p > 0.05 BUKAN",
                    "BERARTI SKRIPSI LO",
                    "GAGAL! JANGAN PANIK"
                ],
                "mark_word_line": 2,
                "body": "Panduan menyusun pembahasan Bab 5 saat hipotesis riset lo tidak terbukti secara statistik.",
                "items": [
                    {
                        "num": "01",
                        "title": "Nilai Ilmiah Hasil Negatif",
                        "desc": "Membuktikan tidak ada hubungan tetap kontribusi sains"
                    },
                    {
                        "num": "02",
                        "title": "4 Langkah Bab 5",
                        "desc": "Komparasi, patofisiologi, metodologi, dan limitasi"
                    },
                    {
                        "num": "03",
                        "title": "Integritas Data",
                        "desc": "Dosa manipulasi angka p-value demi 'signifikan'"
                    }
                ]
            },
            "formula": {
                "pill": "Kerangka 4 Langkah",
                "headline": [
                    "4 STRATEGI MENULIS",
                    "PEMBAHASAN BAB 5"
                ],
                "body": "Gunakan alur sistematis ini untuk menjelaskan hasil p > 0.05.",
                "steps": [
                    {
                        "pill": "Langkah 1",
                        "text": "Bandingkan dengan studi terdahulu yang hasilnya serupa"
                    },
                    {
                        "pill": "Langkah 2",
                        "text": "Jelaskan mekanisme biologis / farmakologis alternatif"
                    },
                    {
                        "pill": "Langkah 3",
                        "text": "Evaluasi keterbatasan metodologi & power sampel"
                    }
                ],
                "insight": "Langkah 4: Tegaskan implikasi klinis temuan ini dan berikan saran metodologi studi lanjutan."
            },
            "editorial": {
                "pill": "Nilai Klinis",
                "headline": [
                    "KENAPA HASIL NEGATIF",
                    "SANGAT BERHARGA?"
                ],
                "mark_word_line": 1,
                "lead": "Manfaat nyata hasil penelitian yang tidak signifikan bagi dunia medis:",
                "items": [
                    {
                        "num": "1",
                        "title": "Cegah Tindakan Sia-sia",
                        "desc": "Menghindarkan pasien dari terapi yang tidak terbukti efektif",
                        "emoji": "🛡️"
                    },
                    {
                        "num": "2",
                        "title": "Anti Publication Bias",
                        "desc": "Menjaga kejujuran data evidence-based medicine",
                        "emoji": "📚"
                    },
                    {
                        "num": "3",
                        "title": "Buka Hipotesis Baru",
                        "desc": "Menemukan faktor perancu lain yang lebih dominan",
                        "emoji": "💡"
                    },
                    {
                        "num": "4",
                        "title": "Bukti Ketelitian",
                        "desc": "Penguji respect pada peneliti yang jujur pada data",
                        "emoji": "🎖️"
                    }
                ]
            },
            "callout": {
                "pill": "Warning Etika",
                "headline": [
                    "DOSA BESAR",
                    "MANIPULASI DATA! 🚨"
                ],
                "lead": "Peringatan integritas ilmiah:",
                "quote": [
                    "Ngedit data di Excel cuma biar p-value berubah dari 0.08 jadi 0.04 adalah pelanggaran etika akademik paling fatal.",
                    "Dosen penguji yang jeli bakal tahu dalam hitungan menit saat melihat sebaran varians dan standard deviasi lo."
                ],
                "body": "Pertahankan kejujuran data riset lo sampai meja sidang."
            },
            "cta": {
                "pill": "Free Deliverable",
                "headline": [
                    "PANDUAN BAB 5 HASIL",
                    "TIDAK SIGNIFIKAN"
                ],
                "sub": "Template Word & PDF strategi pembahasan hasil riset negatif kedokteran.",
                "items": [
                    {
                        "num": "1",
                        "title": "Komen 'SIGNIFIKAN'",
                        "desc": "Admin kirim panduan lengkap Bab 5 ke DM"
                    },
                    {
                        "num": "2",
                        "title": "Susun Pembahasan",
                        "desc": "Ikuti 4 langkah taktis komparasi literatur"
                    },
                    {
                        "num": "3",
                        "title": "Follow @naskah.fk",
                        "desc": "Belajar riset kedokteran dengan integritas"
                    }
                ],
                "button": "KOMEN 'SIGNIFIKAN' DI BAWAH"
            }
        },
        "caption": """Reaksi pertama mahasiswa FK pas liat output SPSS keluar p = 0.124: "Mampus, hipotesis gue ditolak... Apa gue edit dikit aja datanya biar p < 0.05 ya?"

JANGAN PERNAH.

Dalam sains kedokteran, membuktikan bahwa suatu faktor TIDAK berhubungan dengan penyakit tetap memberikan kontribusi pengetahuan yang sangat berharga.

Tugas lo di Bab 5 bukan meratapi angka p-value, tapi menjelaskan KENAPA hasil tersebut bisa terjadi secara biologis dan metodologis.

Swipe buat lihat 4 langkah menyusun Bab 5 untuk hasil p > 0.05!

---
Ketik **SIGNIFIKAN** di komentar buat dapet **Panduan Strategi Pembahasan Hasil Riset Negatif Bab 5** format Word/PDF! 📩

#skripsikedokteran #etikariset #biostatistika #bab5skripsi #kedokteran #anakfk #naskahfk #pejuangskripsi""",
        "thread_1": """Dosa terbesar mahasiswa riset:

Ngedit angka di Excel biar p-value berubah dari 0.08 jadi 0.04.

Ingat, tujuan penelitian itu mencari kebenaran empiris, bukan nyenengin ekspektasi pribadi. Hasil negatif tetaplah hasil ilmiah.""",
        "thread_2_text": """Hasil skripsi p > 0.05 bukan berarti gagal.

Ini cara menyusun pembahasan Bab 5 yang berbobot di mata penguji ➜ @naskah.fk""",
        "thread_3": """Cerita riil di dunia riset kedokteran:

Berapa banyak obat uji klinis yang ternyata ngga lebih efektif daripada plasebo (p > 0.05)? Ratusan.

Dan publikasi hasil negatif itu justru nyelamatin ribuan pasien dari intervensi yang ngga ada gunanya.

Jangan rendah diri cuma gara-gara hipotesis skripsi lo ditolak. Yang penting analisis lo jujur dan metodologi lo kokoh."""
    },
    {
        "folder": "2026-10-04_post_w3_07_naskah_inside_audit_bab4_statistik",
        "slug": "post_w3_07_naskah_inside_audit_bab4_statistik",
        "date_str": "2026-10-04",
        "topic": "Naskah Inside Ep. 3: SOP Audit Bab 4 & Data",
        "tag": "Naskah Inside",
        "config": {
            "tag": "Naskah Inside",
            "cover": {
                "pill": "Behind The Scenes",
                "headline": [
                    "NASKAH INSIDE EP.3",
                    "CARA KAMI AUDIT",
                    "BAB 4 & DATA KLIEN"
                ],
                "mark_word_line": 2,
                "body": "Bocoran SOP 15 menit tim medis Naskah memverifikasi Bab 4 dan analisis data skripsi FK.",
                "items": [
                    {
                        "num": "01",
                        "title": "Konsistensi Sampel N",
                        "desc": "Cek keselarasan total N di Bab 3, 4, dan abstrak"
                    },
                    {
                        "num": "02",
                        "title": "Verifikasi Uji Hipotesis",
                        "desc": "Kesesuaian skala variabel & uji normalitas data"
                    },
                    {
                        "num": "03",
                        "title": "Standar Open-Table",
                        "desc": "Presisi notasi koma desimal & footnote uji"
                    }
                ]
            },
            "formula": {
                "pill": "4 Titik Kritis",
                "headline": [
                    "4 TITIK RAWAN",
                    "AUDIT DATA NASKAH"
                ],
                "body": "Titik yang selalu kami bedah sebelum naskah dikirim kembali ke klien.",
                "steps": [
                    {
                        "pill": "Titik 1",
                        "text": "Apakah ada angka sampel di tabel yang tidak sinkron?"
                    },
                    {
                        "pill": "Titik 2",
                        "text": "Apakah uji parametrik sudah lolos uji normalitas?"
                    },
                    {
                        "pill": "Titik 3",
                        "text": "Apakah nilai p ditulis 3 desimal eksak (p=0.024)?"
                    }
                ],
                "insight": "Titik 4: Memastikan semua key findings di tabel dibahas maknanya secara klinis di Bab 5."
            },
            "editorial": {
                "pill": "Quality Control",
                "headline": [
                    "STANDAR PRECISI",
                    "TIM MEDIS NASKAH"
                ],
                "mark_word_line": 1,
                "lead": "Mengapa standar audit Naskah begitu ketat?",
                "items": [
                    {
                        "num": "1",
                        "title": "Bebas Celah Penguji",
                        "desc": "Dosen penguji selalu mencari inkonsistensi terkecil",
                        "emoji": "🔍"
                    },
                    {
                        "num": "2",
                        "title": "Sidang Jadi Formalitas",
                        "desc": "Naskah yang 100% presisi mengubah interogasi jadi diskusi",
                        "emoji": "🎓"
                    },
                    {
                        "num": "3",
                        "title": "Tim Dokter & Statistisi",
                        "desc": "Dikerjakan oleh lulusan FK yang paham klinis & biostat",
                        "emoji": "🩺"
                    },
                    {
                        "num": "4",
                        "title": "Kecepatan & Keamanan",
                        "desc": "Audit menyeluruh dengan jaminan kerahasiaan data",
                        "emoji": "🔒"
                    }
                ]
            },
            "callout": {
                "pill": "Philosophy",
                "headline": [
                    "BUKAN JUALAN JASA,",
                    "TAPI TRUST 🤝"
                ],
                "lead": "Komitmen Naskah:",
                "quote": [
                    "Kami tidak membantu kecurangan akademik. Kami mendampingi mahasiswa memahami risetnya sendiri.",
                    "Ketika kamu paham logika di balik setiap angka di naskahmu, rasa takut menghadapi sidang otomatis hilang."
                ],
                "body": "Naskah adalah partner akademik terpercaya mahasiswa kedokteran."
            },
            "cta": {
                "pill": "Free Deliverable",
                "headline": [
                    "CHECKLIST 15 MENIT",
                    "SELF-AUDIT SKRIPSI"
                ],
                "sub": "Gunakan checklist internal Naskah untuk mengaudit naskahmu sendiri sebelum bimbingan.",
                "items": [
                    {
                        "num": "1",
                        "title": "Komen 'AUDIT'",
                        "desc": "Admin kirim checklist PDF langsung ke DM"
                    },
                    {
                        "num": "2",
                        "title": "Audit Mandiri",
                        "desc": "Cek 10 poin kritis naskahmu dalam 15 menit"
                    },
                    {
                        "num": "3",
                        "title": "Konsultasi Naskah",
                        "desc": "DM kami jika butuh pendampingan intensif 1-on-1"
                    }
                ],
                "button": "KOMEN 'AUDIT' DI BAWAH"
            }
        },
        "caption": """Banyak yang penasaran: "Gimana sih cara tim medis Naskah mengaudit Bab 4 dan olah data skripsi klien FK?"

Di Naskah, kami punya SOP 15 Menit Audit Kritis yang memverifikasi 10 poin rawan revisi:
Mulai dari sinkronisasi jumlah sampel N antartabel, uji normalitas, format Open-Table, hingga konsistensi penulisan nilai p eksak.

Karena dosen penguji FK itu selalu melihat celah terkecil. Begitu naskah lo bebas dari kesalahan format & inkonsistensi data, sesi sidang lo berubah jadi formalitas ACC!

Swipe buat lihat isi SOP audit internal kami!

---
Ketik **AUDIT** di kolom komentar buat dapet **Checklist 15 Menit Self-Audit Skripsi FK** format PDF gratis! 📩

Butuh pendampingan olah data & audit naskah bareng tim dokter Naskah? Kirim DM sekarang untuk konsultasi!

#naskahinside #skripsifk #olahdata #auditnaskah #biostatistika #kedokteran #naskahfk #bimbinganskripsi""",
        "thread_1": """Checklist ritual hari Minggu buat anak FK yang lagi ngerjain skripsi:

1. Backup file Word ke Google Drive / iCloud (kasih nama berurutan + tanggal hari ini).
2. Cek apakah ada angka sampel di Bab 4 yang tiba-tiba ilang 2 orang.
3. Sinkronisasi referensi Mendeley / Zotero.

Siapkan amunisi sebelum ketemu dospem besok Senin.""",
        "thread_2_text": """Naskah Inside Ep. 3: SOP 15 Menit Audit Bab 4 & Data Skripsi FK.

Download checklist audit mandiri gratis ➜ @naskah.fk""",
        "thread_3": """Refleksi akhir pekan anak FK:

Skripsi itu bukan perlombaan siapa yang paling jenius nemuin molekul baru.

Skripsi di FK adalah latihan disiplin metodologi, kejujuran data, dan ketangguhan mental menghadapi revisi berkali-kali.

Tarik napas, istirahat malam ini. Besok kita hadapi lagi dengan kepala tegak. Semangat para calon sejawat! 🩺🔥"""
    }
]

def make_caption_and_threads_md(post_data):
    p = post_data
    content = f"""# {p['topic'].upper()}
## Status: APPROVED (Ready to Post)
### Scheduled Date: {p['date_str']} (10:00 WIB IG + Threads #1 | 14:00 WIB Threads #2 | 19:00 WIB Threads #3)

---

### 📸 CAPTION INSTAGRAM (READY TO POST)

```markdown
{p['caption']}
```

---

### 🧵 THREADS PAGI — THREAD #1 (10:00 WIB)
**Slot:** 10:00 WIB (Simultaneous with IG Carousel)
**Tipe:** Text-First Discovery & Insight

```text
{p['thread_1']}
```

---

### 🧵 THREADS SIANG — THREAD #2 (14:00 WIB)
**Slot:** 14:00 WIB (Visual Mirror)
**Tipe:** Re-upload 5 Slide Carousel IG

```text
{p['thread_2_text']}
```

---

### 🧵 THREADS MALAM — THREAD #3 (19:00 WIB)
**Slot:** 19:00 WIB (Deep Engagement / Storytelling / Relatable)
**Tipe:** Conversation Starter & Emotional Trust

```text
{p['thread_3']}
```
"""
    return content

def main():
    print("=== Generating Week 3 Approved Packages & Rendering Carousels ===")
    for post in WEEK_3_POSTS:
        folder_path = APPROVED / post["folder"]
        folder_path.mkdir(parents=True, exist_ok=True)

        # 1. Write carousel_config.json
        cfg_path = folder_path / "carousel_config.json"
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(post["config"], f, indent=2, ensure_ascii=False)
        print(f"Written config: {cfg_path}")

        # 2. Write CAPTION_DAN_THREADS_*.md
        md_name = f"CAPTION_DAN_THREADS_{post['folder'].upper()}.md"
        md_path = folder_path / md_name
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(make_caption_and_threads_md(post))
        print(f"Written MD: {md_path}")

        # 3. Render 5 slides
        print(f"Rendering slides for {post['folder']}...")
        render_post(post["folder"], folder_path)

        # 4. Generate PREVIEW contact sheet
        preview_path = folder_path / f"PREVIEW_{post['slug']}.jpg"
        make_carousel_preview(folder_path, preview_path, post["slug"])
        print(f"Generated Preview: {preview_path}")

    print("=== All 7 Week 3 Carousels Successfully Rendered! ===")

if __name__ == "__main__":
    main()
