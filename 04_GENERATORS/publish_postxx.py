"""Publish Post #N — generalized script for Week 0 (Posts #3–#7) and Week 1 (Posts w1_01–w1_06, w1_ni).

Supports:
- IG Carousel + Threads Companion (default)
- IG Single Image + Threads Companion (e.g. w1_05 Revisi Bingo)
- Threads Only (e.g. w1_02, w1_03, w1_06)

Writes PUBLISH_RESULT_post{id}.json, appends to SYNC_STATUS.json, and updates NOTION_SYNC_HANDOFF.md.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
from datetime import datetime, timezone, timedelta

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
CONTENT_ROOT = ROOT_DIR / "06_CONTENT_PIPELINE"
CAPTIONS_ROOT = CONTENT_ROOT / "03_APPROVED"
DRAFTS_ROOT = CONTENT_ROOT / "02_DRAFTS"

POST_CONFIG = {
    # --- WEEK 0 ---
    "3": {
        "dir": CAPTIONS_ROOT / "2026-09-07_post_03_skripsi_vs_tesis",
        "slides": [
            "post03_01_cover.jpg",
            "post03_02_formula.jpg",
            "post03_03_editorial.jpg",
            "post03_04_callout.jpg",
            "post03_05_cta.jpg",
        ],
        "ig_caption_file": CAPTIONS_ROOT / "2026-09-07_post_03_skripsi_vs_tesis" / "CAPTION_DAN_THREADS_POST03.md",
        "threads_file": CAPTIONS_ROOT / "2026-09-07_post_03_skripsi_vs_tesis" / "CAPTION_DAN_THREADS_POST03.md",
        "topic": "Skripsi vs Tesis Kedokteran",
        "ig_type": "carousel",
    },
    "4": {
        "dir": CAPTIONS_ROOT / "2026-09-08_post_04_native_word_citation",
        "slides": [
            "post04_01_cover.jpg",
            "post04_02_formula.jpg",
            "post04_03_editorial.jpg",
            "post04_04_callout.jpg",
            "post04_05_cta.jpg",
        ],
        "ig_caption_file": CAPTIONS_ROOT / "2026-09-08_post_04_native_word_citation" / "CAPTION_DAN_THREADS_POST04.md",
        "threads_file": CAPTIONS_ROOT / "2026-09-08_post_04_native_word_citation" / "CAPTION_DAN_THREADS_POST04.md",
        "topic": "Tutorial Sitasi Native Word F9",
        "ig_type": "carousel",
    },
    "5": {
        "dir": CAPTIONS_ROOT / "2026-09-09_post_05_anatomi_naskah_acc",
        "slides": [
            "post05_01_cover.jpg",
            "post05_02_formula.jpg",
            "post05_03_editorial.jpg",
            "post05_04_callout.jpg",
            "post05_05_cta.jpg",
        ],
        "ig_caption_file": CAPTIONS_ROOT / "2026-09-09_post_05_anatomi_naskah_acc" / "CAPTION_DAN_THREADS_POST05.md",
        "threads_file": CAPTIONS_ROOT / "2026-09-09_post_05_anatomi_naskah_acc" / "CAPTION_DAN_THREADS_POST05.md",
        "topic": "Anatomi Naskah ACC Semhas",
        "ig_type": "carousel",
    },
    "6": {
        "dir": CAPTIONS_ROOT / "2026-09-10_post_06_carousel_layout_edukasi",
        "slides": [
            "post06_01_cover.jpg",
            "post06_02_formula.jpg",
            "post06_03_editorial.jpg",
            "post06_04_callout.jpg",
            "post06_05_cta.jpg",
        ],
        "ig_caption_file": CAPTIONS_ROOT / "2026-09-10_post_06_carousel_layout_edukasi" / "CAPTION_DAN_THREADS_POST06.md",
        "threads_file": CAPTIONS_ROOT / "2026-09-10_post_06_carousel_layout_edukasi" / "CAPTION_DAN_THREADS_POST06.md",
        "topic": "7 Layout Carousel Edukasi Kesehatan",
        "ig_type": "carousel",
    },
    "7": {
        "dir": CAPTIONS_ROOT / "2026-09-11_post_07_sunday_academic_reset",
        "slides": [
            "post07_01_cover.jpg",
            "post07_02_formula.jpg",
            "post07_03_editorial.jpg",
            "post07_04_callout.jpg",
            "post07_05_cta.jpg",
        ],
        "ig_caption_file": CAPTIONS_ROOT / "2026-09-11_post_07_sunday_academic_reset" / "CAPTION_DAN_THREADS_POST07.md",
        "threads_file": CAPTIONS_ROOT / "2026-09-11_post_07_sunday_academic_reset" / "CAPTION_DAN_THREADS_POST07.md",
        "topic": "Sunday Academic Reset",
        "ig_type": "carousel",
    },
    "8": {
        "dir": CAPTIONS_ROOT / "2026-09-12_post_08_hard_sell_3jt_lengkap",
        "slides": [
            "post08_01_cover.jpg",
            "post08_02_formula.jpg",
            "post08_03_editorial.jpg",
            "post08_04_callout.jpg",
            "post08_05_cta.jpg",
        ],
        "ig_caption_file": CAPTIONS_ROOT / "2026-09-12_post_08_hard_sell_3jt_lengkap" / "CAPTION_DAN_THREADS_POST08.md",
        "threads_file": CAPTIONS_ROOT / "2026-09-12_post_08_hard_sell_3jt_lengkap" / "CAPTION_DAN_THREADS_POST08.md",
        "topic": "Hard Sell Paket Lengkap 3JT",
        "ig_type": "carousel",
    },
    "9": {
        "dir": CAPTIONS_ROOT / "2026-09-13_post_09_hard_sell_price_list",
        "slides": [
            "post09_01_cover.jpg",
            "post09_02_formula.jpg",
            "post09_03_editorial.jpg",
            "post09_04_callout.jpg",
            "post09_05_cta.jpg",
        ],
        "ig_caption_file": CAPTIONS_ROOT / "2026-09-13_post_09_hard_sell_price_list" / "CAPTION_DAN_THREADS_POST09.md",
        "threads_file": CAPTIONS_ROOT / "2026-09-13_post_09_hard_sell_price_list" / "CAPTION_DAN_THREADS_POST09.md",
        "topic": "Menu & Transparansi Biaya 2026",
        "ig_type": "carousel",
    },
    # --- WEEK 1: INTRODUCTION TO MADNESS ---
    "w1_01": {
        "dir": CAPTIONS_ROOT / "2026-09-14_post_w1_01_diagnosis_skripsi",
        "slides": [
            "post_w1_01_01_cover.jpg",
            "post_w1_01_02_formula.jpg",
            "post_w1_01_03_editorial.jpg",
            "post_w1_01_04_callout.jpg",
            "post_w1_01_05_cta.jpg",
        ],
        "ig_caption_file": CAPTIONS_ROOT / "2026-09-14_post_w1_01_diagnosis_skripsi" / "CAPTION_DAN_THREADS_W1_01.md",
        "threads_file": CAPTIONS_ROOT / "2026-09-14_post_w1_01_diagnosis_skripsi" / "CAPTION_DAN_THREADS_W1_01.md",
        "topic": "Diagnosis Penyakit Skripsi (ICD-10)",
        "ig_type": "carousel",
    },
    "w1_02": {
        "topic": "Dua Kebenaran Satu Bohong: Metpen",
        "ig_type": "none",
        "threads_source": "draft_json",
        "draft_key": "w1_02",
    },
    "w1_03": {
        "topic": "Autopsi Abstrak (UGC Call)",
        "ig_type": "none",
        "threads_source": "draft_json",
        "draft_key": "w1_03",
    },
    "w1_04": {
        "dir": CAPTIONS_ROOT / "2026-09-17_post_w1_04_scu_episode1",
        "slides": [
            "post_w1_04_01_cover.jpg",
            "post_w1_04_02_formula.jpg",
            "post_w1_04_03_editorial.jpg",
            "post_w1_04_04_callout.jpg",
            "post_w1_04_05_cta.jpg",
        ],
        "ig_caption_file": CAPTIONS_ROOT / "2026-09-17_post_w1_04_scu_episode1" / "CAPTION_DAN_THREADS_W1_04.md",
        "threads_file": CAPTIONS_ROOT / "2026-09-17_post_w1_04_scu_episode1" / "CAPTION_DAN_THREADS_W1_04.md",
        "topic": "SCU Episode 1: Rini Budi Sari",
        "ig_type": "carousel",
    },
    "w1_05": {
        "dir": CAPTIONS_ROOT / "2026-09-18_post_w1_05_revisi_bingo",
        "slides": [
            "post_w1_05_revisi_bingo.jpg",
        ],
        "ig_caption_file": CAPTIONS_ROOT / "2026-09-18_post_w1_05_revisi_bingo" / "CAPTION_DAN_THREADS_W1_05.md",
        "threads_file": CAPTIONS_ROOT / "2026-09-18_post_w1_05_revisi_bingo" / "CAPTION_DAN_THREADS_W1_05.md",
        "topic": "Revisi Bingo: Dosen Pembimbing",
        "ig_type": "single",
    },
    "w1_ni": {
        "dir": CAPTIONS_ROOT / "2026-09-19_post_w1_sat_naskah_inside_ep1",
        "slides": [
            "post_w1_ni_01_cover.jpg",
            "post_w1_ni_02_formula.jpg",
            "post_w1_ni_03_editorial.jpg",
            "post_w1_ni_04_callout.jpg",
            "post_w1_ni_05_cta.jpg",
        ],
        "ig_caption_file": CAPTIONS_ROOT / "2026-09-19_post_w1_sat_naskah_inside_ep1" / "CAPTION_DAN_THREADS_W1_NI.md",
        "threads_file": CAPTIONS_ROOT / "2026-09-19_post_w1_sat_naskah_inside_ep1" / "CAPTION_DAN_THREADS_W1_NI.md",
        "topic": "Naskah Inside EP.1: Di Balik Layar",
        "ig_type": "carousel",
    },
    "w1_06": {
        "topic": "Jam 3 Pagi Threads (3AM Thoughts)",
        "ig_type": "none",
        "threads_source": "draft_json",
        "draft_key": "w1_06",
    },
}


def load_caption_text(filepath: pathlib.Path) -> str:
    """Read the Instagram caption from the md file."""
    text = filepath.read_text(encoding="utf-8", errors="replace")
    marker = "CAPTION INSTAGRAM (READY TO POST)"
    if marker not in text:
        marker = "CAPTION INSTAGRAM"
    if marker not in text:
        raise ValueError(f"Caption marker not found in {filepath}")
    after = text.split(marker, 1)[1]
    lines = after.split("```")
    if len(lines) < 3:
        raise ValueError(f"No code block found after caption marker in {filepath}")
    caption = lines[1].strip()
    return caption.replace("```", "").strip()


def load_threads_text(filepath: pathlib.Path) -> list[dict]:
    """Read Threads companion texts from the md file."""
    text = filepath.read_text(encoding="utf-8", errors="replace")
    marker = "COMPANION THREADS"
    if marker not in text:
        raise ValueError(f"Threads marker not found in {filepath}")
    after = text.split(marker, 1)[1]

    thread_markers = list(re.finditer(r"### Thread #(\d+) \((?:Slot )?([^)]+)\)", after))
    threads = []
    for idx, m in enumerate(thread_markers):
        num = m.group(1)
        start = m.end()
        end = thread_markers[idx + 1].start() if idx + 1 < len(thread_markers) else len(after)
        raw_content = after[start:end].strip()
        cleaned_lines = []
        for line in raw_content.splitlines():
            cleaned = line.lstrip("> ").strip()
            if cleaned:
                cleaned_lines.append(cleaned)
        content = "\n\n".join(cleaned_lines)
        threads.append({
            "slot": f"#{num}",
            "text": content,
        })
    return threads


def load_threads_from_json(draft_key: str) -> list[dict]:
    """Load text-only thread from THREADS_W1_FINAL.json."""
    json_path = DRAFTS_ROOT / "THREADS_W1_FINAL.json"
    if not json_path.exists():
        raise FileNotFoundError(f"Missing {json_path}")
    data = json.loads(json_path.read_text(encoding="utf-8"))
    entry = data.get(draft_key)
    if not entry:
        raise KeyError(f"Key {draft_key} not in {json_path}")
    return [{
        "slot": entry.get("slot", "#1"),
        "text": entry.get("text", "").strip(),
    }]


def now_wib() -> str:
    return datetime.now(timezone(timedelta(hours=7))).strftime("%Y-%m-%d %H:%M WIB")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python publish_postxx.py <post_number>", file=sys.stderr)
        return 1

    post_num = sys.argv[1]
    if post_num not in POST_CONFIG:
        print(f"Post {post_num} not configured. Available: {', '.join(POST_CONFIG.keys())}", file=sys.stderr)
        return 1

    cfg = POST_CONFIG[post_num]
    ig_type = cfg.get("ig_type", "carousel")

    # 1. Load Captions & Threads
    caption_ig = ""
    if ig_type in ("carousel", "single"):
        try:
            caption_ig = load_caption_text(cfg["ig_caption_file"])
        except Exception as e:
            print(f"ERROR reading IG caption: {e}", file=sys.stderr)
            return 1

    threads_raw = []
    if cfg.get("threads_source") == "draft_json":
        try:
            threads_raw = load_threads_from_json(cfg["draft_key"])
        except Exception as e:
            print(f"ERROR reading threads JSON: {e}", file=sys.stderr)
            return 1
    elif "threads_file" in cfg:
        try:
            threads_raw = load_threads_text(cfg["threads_file"])
        except Exception as e:
            print(f"ERROR reading threads: {e}", file=sys.stderr)
            return 1

    from meta_direct_publisher import MetaDirectPublisher
    publisher = MetaDirectPublisher()

    preflight = publisher.check_status()
    if ig_type != "none" and preflight.get("instagram", {}).get("status") != "connected":
        print("ERROR: Instagram is not connected.", file=sys.stderr)
        return 1
    if threads_raw and preflight.get("threads", {}).get("status") != "connected":
        print("ERROR: Threads is not connected.", file=sys.stderr)
        return 1

    image_urls = []
    if "dir" in cfg and "slides" in cfg:
        image_urls = [
            f"https://raw.githubusercontent.com/tebakkasus/Naskah/main/06_CONTENT_PIPELINE/03_APPROVED/{cfg['dir'].name}/{slide}"
            for slide in cfg["slides"]
        ]

    # 2. Publish Instagram
    ig_result = {}
    verified_ig = {}
    if ig_type == "carousel":
        print(f"Publishing Instagram Carousel for post {post_num} ({len(image_urls)} slides)...")
        ig_result = publisher.publish_ig_carousel(image_urls, caption_ig)
        print(json.dumps(ig_result, ensure_ascii=False, indent=2))
        if not ig_result.get("success"):
            print("ERROR: Instagram Carousel publish failed; aborting.", file=sys.stderr)
            return 1
        verified_ig = publisher.get_ig_media(ig_result["media_id"])
        print("Verified Instagram:", json.dumps(verified_ig, ensure_ascii=False, indent=2))
    elif ig_type == "single":
        print(f"Publishing Instagram Single Image for post {post_num}...")
        ig_result = publisher.publish_ig_single_image(image_urls[0], caption_ig)
        print(json.dumps(ig_result, ensure_ascii=False, indent=2))
        if not ig_result.get("success"):
            print("ERROR: Instagram Single Image publish failed; aborting.", file=sys.stderr)
            return 1
        verified_ig = publisher.get_ig_media(ig_result["media_id"])
        print("Verified Instagram:", json.dumps(verified_ig, ensure_ascii=False, indent=2))
    else:
        print(f"Post {post_num} is Threads-only (no IG publication needed).")

    # 3. Publish Threads
    thread_results = []
    for idx_t, item in enumerate(threads_raw):
        text = item["text"]
        print(f"Publishing Thread {item['slot']} (len={len(text)})...")

        # If Thread #1 of a carousel and we have 2+ slides, publish as Threads Carousel
        if ig_type == "carousel" and idx_t == 0 and image_urls and len(image_urls) >= 2:
            print(f"Publishing {item['slot']} as Threads Carousel with {len(image_urls)} slides...")
            carousel_text = text[:490] if len(text) > 490 else text
            result = publisher.publish_threads_carousel(image_urls, carousel_text, topic_tag=cfg["topic"])
            print(json.dumps({"slot": item["slot"], "type": "THREADS_CAROUSEL", "result": result}, ensure_ascii=False, indent=2))
        elif len(text) > 500:
            parts = []
            paragraphs = text.split("\n\n")
            current_part = ""
            for p in paragraphs:
                if len(current_part) + len(p) + 2 <= 480:
                    current_part = f"{current_part}\n\n{p}" if current_part else p
                else:
                    if current_part:
                        parts.append(current_part.strip())
                    current_part = p
            if current_part:
                parts.append(current_part.strip())

            prev_id = None
            main_thread_id = None
            for p_idx, part in enumerate(parts):
                part_tag = cfg["topic"] if p_idx == 0 else ""
                part_text = f"({p_idx+1}/{len(parts)})\n{part}" if len(parts) > 1 else part
                res = publisher.publish_thread(part_text, topic_tag=part_tag, reply_to_id=prev_id)
                print(json.dumps({"slot": item["slot"], "part": p_idx+1, "result": res}, ensure_ascii=False, indent=2))
                if res.get("success"):
                    prev_id = res.get("thread_id")
                    if p_idx == 0:
                        main_thread_id = prev_id
                else:
                    print(f"WARNING: Thread part {p_idx+1} failed: {res}", file=sys.stderr)

            result = {"success": bool(main_thread_id), "thread_id": main_thread_id}
        else:
            result = publisher.publish_thread(text, topic_tag=cfg["topic"])
            print(json.dumps({"slot": item["slot"], "result": result}, ensure_ascii=False, indent=2))

        if not result.get("success"):
            print(f"WARNING: Thread {item['slot']} failed.", file=sys.stderr)
            thread_results.append({
                "slot": item["slot"],
                "status": "FAILED",
                "thread_id": "",
                "permalink": "",
                "timestamp": "",
            })
            continue

        thread_id = result.get("thread_id")
        thread_verify = publisher._threads_get(
            thread_id,
            {"fields": "id,permalink,text,timestamp,shortcode,media_type"},
        )
        thread_results.append({
            "slot": item["slot"],
            "status": "PUBLISHED",
            "thread_id": thread_id,
            "permalink": thread_verify.get("permalink", f"https://www.threads.net/@naskah.efka/post/{thread_id}"),
            "timestamp": thread_verify.get("timestamp", now_wib()),
        })

    published_at = now_wib()
    result = {
        "post_number": post_num,
        "topic": cfg["topic"],
        "published_at_wib": published_at,
        "instagram": {
            "status": "PUBLISHED" if ig_type != "none" else "SKIPPED",
            "media_id": ig_result.get("media_id"),
            "permalink": verified_ig.get("permalink"),
            "media_type": verified_ig.get("media_type"),
            "slides_count": len(cfg.get("slides", [])),
        },
        "threads": thread_results,
        "evidence": {
            "caption_source": str(cfg.get("ig_caption_file", "")),
            "asset_base": f"https://raw.githubusercontent.com/tebakkasus/Naskah/main/06_CONTENT_PIPELINE/03_APPROVED/{cfg.get('dir', 'none').name}/" if "dir" in cfg else "",
            "api_verified": True,
        },
    }

    # Result filename: keep backward-compat zero-padding for numeric posts (post07.json)
    if post_num.isdigit():
        result_filename = f"PUBLISH_RESULT_post0{post_num}.json"
    else:
        result_filename = f"PUBLISH_RESULT_post{post_num}.json"
    result_path = CONTENT_ROOT / result_filename
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"result written: {result_path}")

    status_path = CONTENT_ROOT / "SYNC_STATUS.json"
    if status_path.exists():
        status = json.loads(status_path.read_text(encoding="utf-8"))
        status["last_sync"] = published_at
        status.setdefault("recent_events", []).append({
            "timestamp": published_at,
            "type": "POST_PUBLISHED_META_DIRECT",
            "details": result,
        })
        status_path.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    handoff_path = CONTENT_ROOT / "NOTION_SYNC_HANDOFF.md"
    if handoff_path.exists():
        handoff_text = handoff_path.read_text(encoding="utf-8")
        update_entry = f"\n## Auto-Sync Post #{post_num} — {published_at}\n- **Status**: PUBLISHED\n- **Topic**: {cfg['topic']}\n- **IG Permalink**: {verified_ig.get('permalink', 'N/A')}\n- **Threads**: {', '.join([item['slot'] for item in thread_results])}\n"
        if f"Post #{post_num} —" not in handoff_text:
            handoff_path.write_text(handoff_text.rstrip() + update_entry, encoding="utf-8")

    quota_after = publisher.check_ig_publishing_limit()
    print(json.dumps({"result": result, "quota_after": quota_after, "result_path": str(result_path)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
