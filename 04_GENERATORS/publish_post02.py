"""
Publish Post #2 — Format Manuskrip Jurnal Kedokteran.

Publishes one 5-slide Instagram carousel and two companion Threads posts
through the existing direct Meta API publisher, then writes a verified result
artifact for the default-profile Notion sync.
"""
from __future__ import annotations

import json
import pathlib
import sys
from datetime import datetime, timezone, timedelta

from meta_direct_publisher import MetaDirectPublisher

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
POST_DIR = ROOT_DIR / "06_CONTENT_PIPELINE" / "03_APPROVED" / "post_02_jurnal_kedokteran"
RESULT_PATH = ROOT_DIR / "06_CONTENT_PIPELINE" / "PUBLISH_RESULT_post02.json"
STATUS_PATH = ROOT_DIR / "06_CONTENT_PIPELINE" / "SYNC_STATUS.json"
BASE_RAW = "https://raw.githubusercontent.com/tebakkasus/Naskah/main/06_CONTENT_PIPELINE/03_APPROVED/post_02_jurnal_kedokteran"
SLIDES = [
    "post02_01_cover.jpg",
    "post02_02_formula.jpg",
    "post02_03_editorial.jpg",
    "post02_04_callout.jpg",
    "post02_05_cta.jpg",
]

CAPTION_IG = """Naskah risetmu bagus, tapi masih bisa gugur di screening awal kalau formatnya tidak mengikuti Author Guidelines jurnal.

Sebelum submit, cek 4 hal ini:

1. Tabel
Jangan langsung pakai tabel default Excel yang penuh garis vertikal. Banyak jurnal medis memakai format open table atau three-line table—tetapi aturan akhirnya tetap harus mengikuti jurnal tujuan.

2. Struktur abstrak
Cek apakah jurnal meminta Background, Methods, Results, dan Conclusion secara terstruktur. Jangan menebak formatnya; buka panduan penulisnya.

3. Keywords
Gunakan istilah yang konsisten dengan topik riset dan cek apakah jurnal meminta istilah standar seperti MeSH.

4. Style dan penomoran
Periksa heading, satuan, penomoran tabel/gambar, serta format sitasi. Detail kecil seperti ini sering menjadi alasan editor mengembalikan naskah untuk diperbaiki.

Rule paling aman:
Jangan format berdasarkan template jurnal lain. Download Author Guidelines jurnal tujuan, lalu checklist satu per satu sebelum upload ke OJS.

Simpan checklist ini sebelum submit. Biar energi kamu habis untuk memperkuat riset—bukan memperbaiki tabel yang seharusnya bisa dicek dari awal. 🔖

Butuh bantuan review dan formatting naskah jurnal? DM @naskah.fk untuk diskusi.

#PublikasiIlmiah #JurnalKedokteran #Manuskrip #MetodePenelitian #TipsSkripsi #OJS #NaskahFK"""

THREADS = [
    {
        "slot": "#3 (Open Table)",
        "text": """Pernah lihat tabel di manuskrip jurnal medis yang garisnya cuma tiga?

Itu sering disebut three-line table/open table: garis horizontal seperlunya, tanpa kotak-kotak vertikal penuh.

Tapi jangan langsung menganggap semua jurnal punya aturan yang sama. Cek Author Guidelines jurnal tujuan. Template jurnal adalah sumber kebenaran terakhir untuk format.""",
    },
    {
        "slot": "#4 (Screening awal)",
        "text": """Naskah riset bisa dikembalikan editor sebelum masuk reviewer karena hal yang kelihatannya “cuma format”.

Cek cepat sebelum upload:
• struktur abstrak
• format tabel dan gambar
• keywords
• gaya sitasi
• file tambahan yang diminta jurnal

Isi riset tetap nomor satu. Tapi mengikuti panduan penulis membuat editor tidak perlu mengembalikan naskah untuk hal yang bisa dicek 10 menit.""",
    },
]


def now_wib() -> str:
    return datetime.now(timezone(timedelta(hours=7))).strftime("%Y-%m-%d %H:%M WIB")


def main() -> int:
    publisher = MetaDirectPublisher()
    preflight = publisher.check_status()
    quota_before = publisher.check_ig_publishing_limit()
    recent_ig = publisher.list_recent_ig_media(limit=25)
    recent_threads = publisher._threads_get(
        "me/threads",
        {"fields": "id,permalink,text,timestamp,shortcode,media_type", "limit": "25"},
    )

    print(json.dumps({"preflight": preflight, "quota_before": quota_before}, ensure_ascii=False, indent=2))
    if preflight.get("instagram", {}).get("status") != "connected":
        print("ERROR: Instagram is not connected.", file=sys.stderr)
        return 1
    if preflight.get("threads", {}).get("status") != "connected":
        print("ERROR: Threads is not connected.", file=sys.stderr)
        return 1

    existing_ig = [
        x for x in recent_ig.get("data", [])
        if (x.get("caption") or "").startswith("Naskah risetmu bagus, tapi masih bisa gugur")
    ]
    existing_thread_texts = {x.get("text") for x in recent_threads.get("data", [])}
    existing_threads = [x for x in THREADS if x["text"] in existing_thread_texts]
    if existing_ig or existing_threads:
        print(json.dumps({"error": "duplicate_guard", "existing_ig": existing_ig, "existing_threads": existing_threads}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2

    image_urls = [f"{BASE_RAW}/{name}" for name in SLIDES]
    for path, url in zip((POST_DIR / name for name in SLIDES), image_urls):
        if not path.exists():
            print(f"ERROR: missing local asset: {path}", file=sys.stderr)
            return 1
        print(f"asset_ready: {url}")

    print("publishing_instagram_carousel")
    ig_result = publisher.publish_ig_carousel(image_urls, CAPTION_IG)
    print(json.dumps(ig_result, ensure_ascii=False, indent=2))
    if not ig_result.get("success"):
        print("ERROR: Instagram publish failed; Threads not sent.", file=sys.stderr)
        return 1

    verified_ig = publisher.get_ig_media(ig_result["media_id"])
    print("verified_instagram:")
    print(json.dumps(verified_ig, ensure_ascii=False, indent=2))

    thread_results = []
    for item in THREADS:
        print(f"publishing_threads: {item['slot']}")
        result = publisher.publish_thread(item["text"], topic_tag="JurnalKedokteran")
        print(json.dumps({"slot": item["slot"], "result": result}, ensure_ascii=False, indent=2))
        if not result.get("success"):
            print("ERROR: Threads publish failed after Instagram succeeded.", file=sys.stderr)
            return 1
        thread_id = result.get("thread_id")
        thread_verify = publisher._threads_get(
            thread_id,
            {"fields": "id,permalink,text,timestamp,shortcode,media_type"},
        )
        thread_results.append({"slot": item["slot"], "result": result, "verified": thread_verify})

    published_at = now_wib()
    result = {
        "post_number": 2,
        "topic": "Format Manuskrip Jurnal Kedokteran",
        "published_at_wib": published_at,
        "instagram": {
            "status": "PUBLISHED",
            "media_id": ig_result.get("media_id"),
            "permalink": verified_ig.get("permalink"),
            "media_type": verified_ig.get("media_type"),
            "slides_count": len(SLIDES),
        },
        "threads": [
            {
                "slot": item["slot"],
                "status": "PUBLISHED",
                "thread_id": item["result"].get("thread_id"),
                "permalink": item["verified"].get("permalink"),
                "timestamp": item["verified"].get("timestamp"),
            }
            for item in thread_results
        ],
        "evidence": {
            "caption_source": str(ROOT_DIR / "06_CONTENT_PIPELINE" / "03_APPROVED" / "post_02_jurnal_kedokteran" / "CAPTION_DAN_THREADS_POST02.md"),
            "asset_base": BASE_RAW,
            "api_verified": True,
        },
    }
    RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    status["last_sync"] = published_at
    status.setdefault("recent_events", []).append({
        "timestamp": published_at,
        "type": "POST_PUBLISHED_META_DIRECT",
        "details": result,
    })
    STATUS_PATH.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    quota_after = publisher.check_ig_publishing_limit()
    print(json.dumps({"result": result, "quota_after": quota_after, "result_path": str(RESULT_PATH)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
