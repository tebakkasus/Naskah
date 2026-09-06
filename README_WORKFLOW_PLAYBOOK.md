# NASKAH SOCIAL OS — MASTER WORKFLOW & PLAYBOOK
*Last Updated: 6 September 2026*
*Platform: Hermes Profile Content (`@content`)*
*Integration: Meta Graph API (Instagram & Threads), GitHub CDN, Notion Hub (via `@default`)*

Dokumen ini adalah ringkasan seluruh workflow Naskah Social OS dari awal pembentukan strategi hingga publikasi ke API resmi Meta, beserta alur koordinasi dengan Notion Hub untuk tracking progress.

---

## 1. STRATEGY & IDENTITY PHASE (Fondasi)
Setiap awal siklus atau perubahan strategi, departemen `@content` merujuk pada dua dokumen utama:
- `01_STRATEGY/NASKAH_SOCIAL_OS_SOUL_v1.0.md` — Mengunci *tone of voice*, psikologi mahasiswa/akademisi, dan batas etika konten (edukasi > hard selling).
- `01_STRATEGY/NASKAH_SOCIAL_STRATEGY_v1.0.md` — Mengatur 7 pilar konten mingguan (Edukasi, Pain Point, Actionable, dll).

**Identitas Visual yang Dikunci:**
- **Brand & Handle**: `naskah.fk` (akun IG/Threads: `@naskah.efka`).
- **Logo Resmi**: Ikon "N" geometris (Open Book + Winding Teal Path + Arrow).
- **Tipografi**: Poppins Family (ExtraBold/Bold untuk hook, Medium/Regular untuk body).
- **Palet Warna**: Warm Cream (`#F5F2EB`), Deep Navy (`#071726`), Burnt Orange (`#E85929`).
- **Format Default**: Instagram Carousel 5 Slide (Rasio 4:5 / 1080x1350) + Companion Threads harian (Teks).

---

## 2. IDEATION & DRAFTING PHASE
Semua topik konten bermula dari sini sebelum desain dibuat.

1. **Topik JSON (`06_CONTENT_PIPELINE/01_IDEAS/`)**:  
   AI merancang konsep dasar dalam format JSON (misal: `topic_01_word_citation.json`) yang mencakup hook, struktur 5 slide, dan *angle* penulisan.
2. **Draft Mingguan (`06_CONTENT_PIPELINE/02_DRAFTS/`)**:  
   Kumpulan draf dari 7 postingan harian (Senin - Minggu) dirangkum dalam satu *Weekly Content Plan*.
3. **Copywriting & Companion Threads**:  
   Caption panjang bergaya penceritaan (bukan brosur) dibuat untuk Instagram, dan 2 porsi teks singkat yang menggugah disusun untuk Threads. Semuanya disimpan di folder `03_APPROVED/` dari setiap post (misal: `CAPTION_DAN_THREADS_POST01.md`).

---

## 3. PRODUCTION & RENDER PHASE (Desain Otomatis)
Tidak ada editing manual (drag & drop) di Canva. Seluruh visual dirender pixel-perfect melalui skrip Python (PIL/Pillow).

1. **Eksekusi Generator**:  
   Menjalankan skrip spesifik seperti `generate_carousel_production.py` untuk merender 5 slide PNG.
2. **Aturan Desain (Locked Template V2)**:
   - *Slide 1 (Cover)*: Background Cream, teks ExtraBold, kata kunci di-highlight dengan marker oval (capsule).
   - *Slide 2 (Formula)*: Background Orange, 3 baris *pill badge* (`[ teks ]`).
   - *Slide 3 (Editorial)*: Background Navy, struktur esai berbobot.
   - *Slide 4 (Callout)*: Kutipan "dosbing/penguji" dalam boks.
   - *Slide 5 (CTA)*: Amankan naskah + soft selling layanan pendampingan.
3. **Visual Quality Control (VQC)**:  
   Setiap hasil render dievaluasi melalui `vision_analyze` (Hermes melihat gambar). Mengecek margin 90px, logo di pojok kiri atas semua slide tanpa boks, marker oval yang pas, dan teks yang tidak terpotong (overflow).

---

## 4. GITHUB CDN PREPARATION PHASE
Meta Graph API mewajibkan aset gambar yang diupload ke Instagram menggunakan URL HTTPS publik (bukan PNG lokal atau Google Drive biasa). 

1. **Konversi ke JPEG**:  
   File PNG dari `03_APPROVED` dikonversi ke JPEG beresolusi tinggi (karena Meta lebih stabil dengan JPEG untuk feed carousel).
2. **Push ke GitHub Public Repo**:  
   Gambar JPEG didorong (git push) ke repository publik `https://github.com/tebakkasus/Naskah`.
3. **Generate CDN URL**:  
   Mendapatkan link *raw* permanen (misal: `https://raw.githubusercontent.com/.../post01_01_cover.jpg`), yang siap di-*ingest* (cURL) oleh server Meta.

---

## 5. PUBLISHING PHASE (Direct Meta API)
Memublikasikan langsung ke aplikasi sosial media menggunakan `04_GENERATORS/meta_direct_publisher.py` (tanpa pihak ketiga/Composio).

1. **Pengecekan Kredensial & Kuota**:  
   Membaca *access token* dari `.env` dan memverifikasi kuota upload harian Meta (limit 100/hari).
2. **Instagram Carousel Upload**:  
   - Meta membuat Container terpisah untuk masing-masing slide (1 s.d. 5) menggunakan URL GitHub Raw.
   - Menunggu setiap slide berstatus *FINISHED*.
   - Membuat Parent Container (Carousel) yang menggabungkan kelima slide beserta Caption.
   - Mengirim perintah Publish untuk menampilkan carousel ke publik.
3. **Threads Publish**:  
   - Memasukkan teks *Thread Companion* beserta Tag (`#Skripsi`) ke container.
   - Mengirim perintah Publish ke feed Threads.
4. **Log Result**:  
   Media ID dan Permalink Instagram/Threads dicatat ke `PUBLISH_RESULT_postXX.json`.

---

## 6. NOTION TRACKING & SYNC PHASE (via @default)
Karena database manajemen proyek dan Notion tracking berada di ranah profil Hermes `@default`, profil `@content` akan berkoordinasi (hand-off) untuk membarui status publikasi di Notion Hub.

**Alur Koordinasi Lintas Agen:**
1. Profil `@content` menulis status terbaru, tanggal publikasi, dan permalink URL ke file internal: `06_CONTENT_PIPELINE/SYNC_STATUS.json`.
2. Profil `@content` meminta pengguna atau secara sistem melakukan *handoff* ke profil `@default`.
3. Profil `@default` membaca `SYNC_STATUS.json`.
4. Profil `@default` (yang memiliki akses/kredensial API Notion dan menggunakan *notion-composio-workflows* atau *direct API* Notion) melakukan update pada baris database Notion:
   - Mengubah status draf menjadi `PUBLISHED`.
   - Mengisi kolom *Published URL*.
   - Mengupdate metrik *Sync Date*.

---

## RINGKASAN CEKLIST OPERASIONAL (Day-to-Day)

Kapanpun TM berkata: *"Eksekusi Post #2"*, alur robotiknya adalah:
1. `publish_post02.py --convert-only` (Ubah 5 PNG → JPEG).
2. `git add & git commit & git push` (Naikkan JPEG ke GitHub CDN).
3. `publish_post02.py` (Buat Carousel Container → Publish Instagram → Publish Threads).
4. Update `SYNC_STATUS.json` dengan Media ID / Permalink.
5. Panggil/minta `@default` untuk meng-update Notion Command Center.

**-- END OF PLAYBOOK --**
