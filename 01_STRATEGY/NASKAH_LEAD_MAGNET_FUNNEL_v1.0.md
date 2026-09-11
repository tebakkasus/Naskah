# NASKAH LEAD MAGNET & DM FUNNEL SYSTEM
**Status:** ACTIVE & LOCKED
**Enforced by:** TM x Tacii — September 2026

---

## 🎯 TUJUAN SISTEM INI
Mengubah passive followers @naskah.fk menjadi **warm leads** tanpa friction psikologis (canggung, takut mahal). Setiap interaksi DM dimulai dengan **nilai gratis**, bukan penawaran.

---

## 🔄 FUNNEL FLOW (4 Step)

```
[POST/THREADS] → [KEYWORD DM] → [AUTO-REPLY FORMAT] → [HUMAN HAND-OFF + SOFT CTA]
     ↑                                                                    │
     └──────────────────────── SHARE / SAVE ──────────────────────────────┘
```

### Step 1: Entry Hook (Di Post/Threads)
Setiap post carousel atau threads wajib mengandung **CTA keyword trigger** di bagian akhir:

| Keyword | Trigger Context | Link ke Framework |
|---------|----------------|-------------------|
| `DIAGNOSIS` | Post tentang Bab Pembahasan, Benang Merah, Kesalahan Umum | "3 poin evaluasi gratis" |
| `BENANG MERAH` | Post tentang konsistensi Bab 1-4-5 | "Cek apakah benang merahmu putus" |
| `CEK JUDUL` | Post tentang judul skripsi, rumusan masalah | "Evaluasi judul & rumusan masalah" |
| `REVISI` | Post tentang common mistakes, revision tips | "Kirim 1 paragraf, kami koreksi" |

### Step 2: Auto-Reply Template (Via Telegram/Naskah Bot)
Ketika user DM dengan keyword, kirimkan format balasan:

```
Terima kasih sudah DM @naskah.fk! 🙌

Untuk dapat evaluasi GRATIS, kirimkan:

1. Judul skripsimu
2. Rumusan masalahmu (copy dari Bab 1)
3. Kesimpulan utamamu (copy dari Bab 5)

Tim kami akan kirim 3 poin evaluasi dalam 1x24 jam.

Catatan: Evaluasi ini bersifat umum dan bukan pengganti bimbingan intensif. Jika butuh pendampingan lebih lanjut, kami akan memberikan opsi yang sesuai.
```

### Step 3: Human Hand-Off (TM / Tacii Review)
Ketika user mengirim data, tim review dengan framework "3 poin evaluasi":

| Poin | Evaluasi | Trigger |
|------|----------|---------|
| **1. Benang Merah** | Apakah RM di Bab 1 terjawab dengan presisi di Bab 5? | Kalau ada RM yang tidak terjawab → flag. |
| **2. Kedalaman Pembahasan** | Apakah paragraf pembahasan cuma rekap atau sudah pakai 3-Tier Loop? | Kalau cuma rekap → flag. |
| **3. Kekuatan Referensi** | Apakah ada positioning terhadap riset terdahulu? | Kalau tidak ada sitasi → flag. |

### Step 4: Soft CTA (Conversion)
Setelah mengirim 3 poin evaluasi, tutup dengan soft CTA:

```
Itu tadi 3 poin evaluasi singkat dari tim kami.

Jika kamu ingin kami bantu bedah lebih dalam — dari Bab 1 sampai siap sidang — kamu bisa mulai dengan sesi pendampingan 1 minggu (4x sesi, 45 menit per sesi).

Ketik INFO untuk detail harga & jadwal.

Terima kasih sudah percaya Naskah. 🙏
```

---

## 📊 METRIK KESUKSESAN FUNNEL

| Metric | Target | Cara Ukur |
|--------|--------|-----------|
| Keyword DM per minggu | 10+ DM dengan keyword `DIAGNOSIS` | Hitung manual atau via Telegram bot log |
| Conversion ke "INFO" | 30% dari yang sudah dapat evaluasi | Hitung user yang ketik `INFO` setelah evaluasi |
| Conversion ke booking | 15% dari yang sudah dapat evaluasi | Hitung user yang sudah transfer/pilih jadwal |
| Save & Share per post | 2x lipat dari baseline sebelum funnel | Instagram Insights |

---

## 🛠️ IMPLEMENTASI TEKNIS

### Opsi A: Manual (Saat Ini)
TM atau Tacii memantau DM @naskah.fk, mengidentifikasi keyword, dan mengirimkan balasan manual sesuai template.

### Opsi B: Semi-Automated (Recommended untuk skala 50+ DM/minggu)
1. Buat Telegram Bot untuk @naskah.fk (atau gunakan Hermes di profile `@content`).
2. Monitor DM masuk, deteksi keyword `DIAGNOSIS`/`BENANG MERAH`/`CEK JUDUL`/`REVISI`.
3. Auto-reply format template langsung.
4. Forward DM yang sudah terbalas ke **Notion CRM Database** (kolom: Nama, Keyword, Tanggal, Status Evaluasi, Status Conversion).

### Opsi C: Fully Automated (Skala Besar 200+ DM/minggu)
Gabungkan:
- Hermes Telegram Bot → auto-reply template
- Notion Database → CRM pipeline
- Hermes Cron → notifikasi harian ke TM/Tacii untuk review & soft CTA
- Browser-use → scrape Instagram DM via CDP (jika API terbatas)

---

## ⚠️ ATURAN KETAT FUNNEL
1. **TIDAK BOLEH langsung hard-sell.** Selalu mulai dengan evaluasi gratis.
2. **TIDAK BOLEH membalas DM dengan template yang terasa robot/automo.** Personalisasi dengan menyebut nama user (jika tersedia).
3. **TIDAK BOLEH melebihi 1x24 jam waktu balasan.** Jika lebih, kirim pesan "Mohon maaf, ada sedikit keterlambatan. Evaluasi 3 poin kamu akan dikirim hari ini."
4. **TIDAK BOLEH memberikan evaluasi yang buru-buru atau dangkal.** Lebih baik telat 6 jam dengan kualitas daripada on-time tapi asal-asalan.
