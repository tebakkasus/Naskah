# NASKAH SOCIAL OS — CAROUSEL TEMPLATE V2.0 (EDITORIAL + DIAGRAM MODE)
*Status: LOCKED & ACTIVE*
*Enforced by TM Directive — September 2026*
**Source of Truth: Aligned with `NASKAH_DESIGN_SYSTEM_v1.0.md` Color Palette & Visual Philosophy**

---

## 🔄 PERUBAHAN DARI V1.0
Template ini menggantikan *card stack layout* di V1.0 dengan **editorial split-screen** dan **diagram layout**. V1.0 masih berlaku untuk post tips ringan; template ini untuk post yang mengandung **framework, case study, atau before-after**.

**Color Palette (dari Design System v1.0):**
- **Dominant Background (65-70%):** Deep Forest Green (`#0F382A` / `#062E22`) atau Deep Midnight Navy (`#0A192F`).
- **Primary Accent (20-25%):** Soft Blush Pink (`#F7D6D0` / `#F5C5B8`) atau Ice Porcelain (`#F1F5F9`) — untuk kotak highlight, lingkaran vokal, teks pendukung.
- **Contrast Element (5-10%):** Highlight box warna terang dengan teks gelap di dalamnya (efek label tape/stabilo).
- **Framing Rule Lines:** Thin L-shaped corner frames (putih halus / soft pink) di sudut kiri atas & kanan bawah.

---

## 📐 5 ATURAN BARU UNTUK EDITORIAL & DIAGRAM LAYOUT

### 1. EDITORIAL SPLIT-SCREEN LAYOUT (Slide Before vs After)
Ketika post membandingkan dua kondisi (Before/After, Salah/Benar, Dulu/Sekarang):
* **Slide dimbagi dua vertikal** dengan garis pemisah Soft Blush Pink (`#F7D6D0`) di tengah.
* **Kiri = Versi Salah/Before:** Box dengan border gelap (`#0F382A`), "X" stamp overlay di pojok kanan atas.
* **Kanan = Versi Benar/After:** Box dengan border gelap (`#0F382A`), Checkmark stamp overlay di pojok kiri atas.
* **Background keseluruhan:** Deep Forest Green (`#0F382A`) atau Deep Midnight Navy (`#0A192F`).
* **Teks pada box:** Ice Porcelain (`#F1F5F9`) untuk readability.

### 2. PYRAMID / FUNNEL DIAGRAM (For Framework Slides)
Ketika post menjelaskan framework bertingkat (seperti "3-Tier Discussion Loop"):
* Gunakan **3 stacked horizontal blocks** yang makin lebar ke bawah (inverted pyramid / funnel).
* Warna blok: **Alternating Deep Forest Green (`#0F382A`) dan Soft Blush Pink (`#F7D6D0`)** untuk visual rhythm.
* **Panah connector** antar blok: Soft Blush Pink (`#F7D6D0`).
* **Ikon kecil** di samping tiap tier (emoji PNG via `paste_emoji()`).
* Spacing antar blok: **18px**. Spacing antar blok dan edge canvas: **min. 48px**.

### 3. ASSERTION CALLOUT BOX (For Key Insight Slides)
Untuk menyorot pernyataan penting atau quote editorial:
* **Background box:** Deep Midnight Navy (`#0A192F`) transparan 90% + blur (untuk efek frosted glass).
* **Teks di dalam box:** Ice Porcelain (`#F1F5F9`), font `Montserrat-ExtraBold` (Cover) / `Montserrat-Medium` (Body), ukuran 28px.
* **Border kiri box:** Soft Blush Pink (`#F7D6D0`), ketebalan 6px.
* **Posisi box:** Rata kiri dengan margin 60px dari edge canvas.

### 4. TIER LABEL / STEP LABEL (Numbering Overlay)
Untuk setiap tier atau langkah dalam framework:
* **Badge pill kecil:** Soft Blush Pink (`#F7D6D0`) background, Deep Forest Green (`#0F382A`) text.
* **Font:** `Montserrat-Bold`, 22px.
* **Posisi:** Sejajar kiri dari box konten, margin 30px dari edge.
* **Ikon:** Gunakan PNG badge angka (01, 02, 03) dari `02_BRAND_ASSETS/badges/` atau render via Pillow.

### 5. WHITE SPACE MANAGEMENT (Anti-Density Rule)
* **Slide editorial/diagram TIDAK BOLEH** menggunakan lebih dari 60% area canvas untuk konten.
* **Sisakan minimal 40% area canvas** sebagai white space (atau Deep Forest Green space) di bagian atas atau bawah.
* **Jangan stack lebih dari 3 box/card per slide.** Jika konten banyak, gunakan slide tambahan.
* **Spacing antar elemen horizontal:** Minimum 24px.

---

## 📝 CONTOH LAYOUT: POST BEFORE-AFTER (5 Slide)

### Slide 01: Cover (Hook)
- **Background:** Deep Forest Green (`#0F382A`).
- **Headline:** `Montserrat-ExtraBold` 72px, Ice Porcelain (`#F1F5F9`). "Kalimat yang bikin penguji marah vs yang bikin dosen angkat jempol."
- **Subhead:** `Montserrat-Medium` 30px, Soft Blush Pink (`#F7D6D0`). "Bedah paragraf Bab Pembahasan — 2 versi, 2 nasib."
- **Split line:** Garis vertikal Soft Blush Pink di tengah canvas. "BEFORE" label di kiri (Deep Forest Green pill), "AFTER" label di kanan (Deep Forest Green pill).
- **Logo:** Monogram "N" di kiri atas (margin 90px).
- **Framing Rule:** Thin L-shaped corner frames (Soft Blush Pink) di sudut kiri atas & kanan bawah.
- **Footer:** `naskah.fk | Bedah Naskah | 01/05` (Ice Porcelain, 20px).

### Slide 02: The "BEFORE" (Yang Salah)
- **Background:** Deep Forest Green (`#0F382A`).
- **Headline:** `Montserrat-ExtraBold` 36px, Ice Porcelain. "Ini yang ditulis mahasiswa kebanyakan:"
- **Body:** Paragraf contoh versi "Before" (rekap data) dalam box **Ice Porcelain (`#F1F5F9`)** dengan border Deep Forest Green (`#0F382A`), 2px. Teks dalam box: Deep Forest Green.
- **Overlay:** "X" stamp PNG di pojok kanan atas box.
- **Label pill:** "⚠️ REKAP DATA, BUKAN PEMBAHASAN." — Soft Blush Pink pill, Deep Forest Green text, `Montserrat-Bold` 22px.
- **Footer:** `naskah.fk | 02/05`.

### Slide 03: The "AFTER" (Yang Benar)
- **Background:** Deep Forest Green (`#0F382A`).
- **Headline:** `Montserrat-ExtraBold` 36px, Ice Porcelain. "Ini yang ditulis mahasiswa yang ACC dalam 15 menit:"
- **Body:** Paragraf contoh versi "After" (3-Tier Loop) dalam box **Ice Porcelain (`#F1F5F9`)** dengan border Deep Forest Green (`#0F382A`), 2px. Teks dalam box: Deep Forest Green.
- **Overlay:** Checkmark stamp PNG di pojok kiri atas box.
- **Label pills:** Tiga pill badge kecil (T1, T2, T3) di samping paragraf, Soft Blush Pink background, Deep Forest Green text.
- **Footer:** `naskah.fk | 03/05`.

### Slide 04: The Diagram (3-Tier Loop Visual)
- **Background:** Deep Midnight Navy (`#0A192F`).
- **Headline:** `Montserrat-ExtraBold` 36px, Ice Porcelain. "Rumus Paragraf yang Bikin Penguji Terkesan."
- **Diagram:** 3 stacked horizontal blocks (funnel):
  - **T1 (Top, narrowest):** `Montserrat-Bold` 26px, Ice Porcelain. "T1: ASSERTION — 'Temuan ini menunjukkan...'".
  - **T2 (Middle):** `Montserrat-Medium` 24px, Ice Porcelain. "T2: MECHANISM — 'Hal ini dapat dijelaskan...'".
  - **T3 (Bottom, widest):** `Montserrat-Medium` 22px, Ice Porcelain. "T3: POSITIONING — 'Konsisten dengan... namun berbeda dengan...'".
- **Connector arrows:** Soft Blush Pink (`#F7D6D0`) vertical arrows between blocks.
- **Ikon:** 📌 (T1), ⚙️ (T2), 🌍 (T3) — PNG via `paste_emoji()` di samping tiap label tier.
- **Footer:** `naskah.fk | 3-Tier Loop | 04/05`.

### Slide 05: CTA (Lead Magnet Hook)
- **Background:** Deep Forest Green (`#0F382A`).
- **Headline:** `Montserrat-ExtraBold` 40px, Ice Porcelain. "Yakin paragraf Bab Pembahasan skripsimu sudah 'siap sidang'?"
- **CTA Button:** Full-width Soft Blush Pink (`#F7D6D0`) button, Deep Forest Green text (`Montserrat-Bold` 32px): "DM kata DIAGNOSIS ke @naskah.fk — kami kasih 3 poin evaluasi GRATIS."
- **Body text:** `Montserrat-Medium` 24px, Ice Porcelain, di bawah button: "Kirim: judul + rumusan masalah + kesimpulan utama. Balasan dalam 1x24 jam."
- **Bookmark icon:** PNG bookmark asset di pojok kanan bawah.
- **Footer:** `naskah.fk | 05/05`.

---

## ⚠️ ATURAN KETAT UNTUK POST INI:
1. TIDAK BOLEH mengembalikan layout ke card stack jika post ini mengandung framework atau before-after.
2. TIDAK BOLEH mengurangi white space di bawah 40% pada slide diagram.
3. TIDAK BOLEH menggunakan emoji via teks — wajib PNG.
4. Slide 05 wajib mengandung CTA "DM DIAGNOSIS" — ini sistem funnel aktif.
5. **Semua warna MENGIKUTI `NASKAH_DESIGN_SYSTEM_v1.0.md`.** Jika ada ketidaksesuaian, design system menang.