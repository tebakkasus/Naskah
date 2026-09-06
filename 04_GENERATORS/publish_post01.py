"""
Publish Post #1 (5 Kesalahan Fatal Sitasi di Word) directly to Instagram (carousel)
and Threads (two companion posts) via the official Meta APIs.

Prerequisites:
- .env has INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_USER_ID, THREADS_ACCESS_TOKEN.
- The 5 carousel slides are committed to the public GitHub CDN as JPEG:
    https://raw.githubusercontent.com/tebakkasus/Naskah/main/06_CONTENT_PIPELINE/03_APPROVED/post_01_word_citation/*.jpg
"""

from __future__ import annotations

import json
import os
import pathlib
import sys
from typing import Any

from PIL import Image

from meta_direct_publisher import MetaDirectPublisher

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
POST_DIR = ROOT_DIR / "06_CONTENT_PIPELINE" / "03_APPROVED" / "post_01_word_citation"
BASE_RAW = "https://raw.githubusercontent.com/tebakkasus/Naskah/main/06_CONTENT_PIPELINE/03_APPROVED/post_01_word_citation"

CAPTION_IG = """Dosen penguji itu cuma butuh 10 detik buat ngecek daftar pustaka kamu.

Kalau pas dicek:
❌ Nama di Bab 2 ada, tapi di daftar pustaka belakang hilang
❌ Format nama belakang pengarang acak-acakan
❌ Tahun terbit di teks (2021) tapi di daftar pustaka (2020)
❌ Gaya APA kecampur Vancouver

...itu langsung jadi celah revisi mayor sebelum kamu sempat jelasin isi penelitianmu.

Menulis sitasi manual di Word memang kelihatan cepat di awal, tapi pas halaman skripsi sudah tembus 80+ halaman dan bolak-balik revisi paragraf, nomor dan urutan sitasi manual pasti berantakan.

Solusinya:
Gunakan fitur sitasi native Word (References > Insert Citation) atau reference manager yang terintegrasi. Begitu ada revisi bab, tinggal tekan F9 atau update field, semua daftar pustaka otomatis tersinkronisasi tanpa ada nama yang tertinggal.

Simpan postingan ini biar naskah skripsi/tesis kamu aman dari revisi format waktu maju sempro nanti! 🔖

---
Butuh teman bedah naskah atau rapikan format metodologi sebelum masuk ruang sidang?
DM @naskah.fk untuk diskusi bareng tim akademik kami.

#TipsSkripsi #SitasiWord #DaftarPustaka #NaskahFK #MetodePenelitian #PejuangSkripsi #Sempro2026 #KaryaTulisIlmiah"""

THREADS = [
    {
        "slot": "#1 (Problem Awareness)",
        "text": (
            "Berapa jam yang kamu habiskan cuma buat ngecek satu-satu apakah nama "
            "dosen/peneliti di Bab 2 sudah masuk ke daftar pustaka paling belakang? \n\n"
            "Nulis sitasi manual di Word itu jebakan: kelihatan gampang pas 10 halaman "
            "pertama, tapi jadi mimpi buruk pas halaman naskah udah tembus 90 halaman "
            "dan dosen minta rombak 3 paragraf."
        ),
        "topic_tag": "Skripsi",
    },
    {
        "slot": "#2 (Practical Insight)",
        "text": (
            "Salah satu alasan naskah ditolak reviewer dalam 3 menit pertama bukan "
            "karena topiknya jelek, tapi karena daftar pustakanya \"gado-gado\":\n\n"
            "Setengah pakai format APA (Nama, Tahun), setengah lagi kecampur format "
            "Vancouver angka [1]. \n\n"
            "Selalu kunci satu citation style dari awal sebelum kamu ngetik satu "
            "paragraf pun di Bab 1."
        ),
        "topic_tag": "Skripsi",
    },
]

SLIDE_NAMES = [
    "post01_01_cover",
    "post01_02_formula",
    "post01_03_editorial",
    "post01_04_callout",
    "post01_05_cta",
]


def convert_to_jpeg(force: bool = False) -> list[str]:
    """Convert the 5 PNG slides to JPEG in-place for the Meta CDN. If a JPEG
    already exists and force is False, reuse it."""
    jpeg_urls = []
    for name in SLIDE_NAMES:
        png_path = POST_DIR / f"{name}.png"
        jpg_path = POST_DIR / f"{name}.jpg"
        if not force and jpg_path.exists():
            jpeg_urls.append(f"{BASE_RAW}/{name}.jpg")
            continue
        image = Image.open(png_path)
        if image.mode != "RGB":
            image = image.convert("RGB")
        image.save(jpg_path, "JPEG", quality=92, optimize=True)
        jpeg_urls.append(f"{BASE_RAW}/{name}.jpg")
    return jpeg_urls


def main() -> int:
    if "--convert-only" in sys.argv:
        urls = convert_to_jpeg(force="--force" in sys.argv)
        for url in urls:
            print(url)
        return 0

    jpeg_urls = convert_to_jpeg()
    print("Converted JPEG slides:")
    for url in jpeg_urls:
        print(" ", url)

    publisher = MetaDirectPublisher()
    status = publisher.check_status()
    print("\nConnection status:", json.dumps(status, indent=2))

    if status.get("instagram", {}).get("status") != "connected":
        print("ERROR: Instagram is not connected. Aborting.", file=sys.stderr)
        return 1
    if status.get("threads", {}).get("status") != "connected":
        print("ERROR: Threads is not connected. Aborting.", file=sys.stderr)
        return 1

    print("\n--- Publishing Instagram Carousel (5 slides) ---")
    ig_result: dict[str, Any] = publisher.publish_ig_carousel(jpeg_urls, CAPTION_IG)
    print(json.dumps(ig_result, indent=2, ensure_ascii=False))

    if not ig_result.get("success"):
        print("ERROR: Instagram carousel publish failed. Threads posts NOT sent.", file=sys.stderr)
        return 1

    media_id = ig_result.get("media_id")
    if media_id:
        media = publisher.get_ig_media(media_id)
        print("\n--- Verified Instagram media ---")
        print(json.dumps(media, indent=2, ensure_ascii=False))

    print("\n--- Publishing Threads companion posts ---")
    thread_results = []
    for thread in THREADS:
        result = publisher.publish_thread(thread["text"], topic_tag=thread["topic_tag"])
        thread_results.append({"slot": thread["slot"], "result": result})
        print(json.dumps({"slot": thread["slot"], "result": result}, indent=2, ensure_ascii=False))

    summary = {
        "instagram": ig_result.get("media_id"),
        "instagram_permalink": (ig_result.get("media") or {}).get("permalink"),
        "threads": [{"slot": tr["slot"], "id": tr["result"].get("thread_id")} for tr in thread_results],
    }
    with open(ROOT_DIR / "06_CONTENT_PIPELINE" / "PUBLISH_RESULT_post01.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print("\nSummary:", json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
