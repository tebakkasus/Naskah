# NASKAH SOCIAL OS — CAROUSEL SYSTEM RULES 2026 (LOCKED)
*Status: LOCKED & ACTIVE*  
*Enforced by TM Directive — 9 September 2026*

---

## 🔒 8 ATURAN BAKU VISUAL NASKAH (ZERO-ERROR STANDARD)

### 1. SKALA FONT (OPTIMAL UNTUK FEED HP)
Teks harus langsung terbaca jelas di layar HP tanpa harus di-zoom:
* **Headline Utama:** 68–84px (`Poppins-ExtraBold`)
* **Sub-headline / Section Title:** 36–46px (`Poppins-Bold`)
* **Card Titles:** 30–34px (`Poppins-Bold`)
* **Body Text & Tips Cards:** 26–28px (`Poppins-Medium` / `Poppins-Regular`)
* **Pills & Badge Text:** 20–24px (`Poppins-Bold` / `Poppins-SemiBold`)
* **Captions & Footer:** 18–22px (`Poppins-Medium`)

---

### 2. HIGHLIGHT BAR / STABILO (ANTI-CUTTING HURUF)
* **DILARANG:** Membuat garis highlight yang memotong, menabrak, atau menyilang batang huruf (seperti `y - 20`).
* **WAJIB:** Mengukur *bounding box* teks secara dinamis (`bb = d.textbbox(...)`).
* Garis harus diletakkan **tepat di bawah garis dasar (*baseline*) huruf** dengan *gap* aman:
  $$\text{Bar Y} = bb[3] + 6\text{px}$$

---

### 3. BADGE & PILL (HUG-CONTENT & OPTICAL CENTERING)
* **Teks dalam Pill:** Menggunakan `anchor="lm"` (left-middle) pada titik tengah vertikal pill (`mid_y = y + pill_h / 2`).
* **Emoji dalam Pill:** Menggunakan `anchor="mm"` (middle-middle) pada titik tengah yang sama (`mid_y`).
* **Posisi Header Badge:** Selalu `align_right=True` di margin kanan (`W - 90`), dengan koordinat Y (`y=75`) yang sejajar lurus dengan titik tengah logo "N" di kiri atas (`y=70 + 28 = 98`).

---

### 4. DYNAMIC BOX SIZING (ANTI-OVERFLOW / TEKS NABRAK BORDER)
* **DILARANG:** Menggunakan tinggi kotak statis jika teks di dalamnya dinamis.
* **WAJIB:** Menghitung tinggi kotak berdasarkan:
  $$\text{Box Height} = \text{Tinggi Teks} + (2 \times \text{Padding Aman (36px)})$$
* Teks tidak boleh menyentuh atau menembus garis tepi (*border*) kotak.

---

### 5. ATURAN PENGGUNAAN EMOJI & IKON (ZERO TOFU / ZERO FLOATING)
* **DILARANG:** Merender emoji via teks Pillow font biasa (`d.text`), karena font Poppins tidak punya glyph emoji (akan menghasilkan kotak silang $\Box$).
* **WAJIB:** Menggunakan aset PNG Twemoji resmi dari `02_BRAND_ASSETS/emojis/` via `paste_emoji()` atau `paste_emoji_with_text()`.
* **Container Rule:** Emoji **TIDAK BOLEH mengambang bebas** di ruang kosong tanpa wadah. Emoji harus selalu terpasang di:
  1. Dalam *pill badge* (di samping teks badge)
  2. Dalam kartu daftar tindakan (*action row*)
  3. Berdampingan langsung dengan teks kalimat

---

### 6. COMPOSITION & DEAD SPACE MANAGEMENT
* **DILARANG:** Membiarkan *dead space* kosong > 15% di bagian bawah atau kanan slide (efek *left-heavy*).
* **WAJIB:** Mengisi bagian bawah slide dengan **Solid Container Card** (seperti *Card CTA Navy / Orange*) untuk menyeimbangkan bobot visual seluruh slide.

---

### 7. RITME CAROUSEL 5 SLIDE (LOCKED PALETTE & FLOW)
1. **Slide 01 (Cover):** *Warm Cream (#FDFBF6 ➔ #F5F2EB)* + Headline Besar + 3 Kartu Ringkas + Kartu CTA Navy.
2. **Slide 02 (Formula / Framework):** *Solid Burnt Orange (#E85929 ➔ #C84318)* + Pill Formula Full-Width (Centered) + Kotak Insight.
3. **Slide 03 (Editorial / Wisdom):** *Deep Navy (#071726)* + Ambient Glow + Frosted Glass Card + 3 Baris Aksi Bernomor & Berikon.
4. **Slide 04 (Callout / Checklist):** *Warm Cream* + Kartu Checklist Putih (Ikon ✅ Rata Tengah) + Kotak Penjelas Navy.
5. **Slide 05 (Soft CTA):** *Warm Cream* + Bookmark Card Oranye + Solusi Penutup & Ajakan Aksi.

---

### 8. BRAND IDENTIFIER KONSISTEN
* **Logo Mark:** Monogram "N" resmi di kiri atas (margin 90px).
* **Footer:** `naskah.fk` (kiri bawah) — `[Judul Topik]` (tengah bawah) — `[01/05]` (kanan bawah).
