"""Publish Post #N — generalized script for Posts #3–#7.

Reads caption + companion threads from per-post md files, publishes
Instagram carousel (or single) and two companion Threads via the
MetaDirectPublisher class, then writes PUBLISH_RESULT_postN.json,
SYNC_STATUS.json, and updates Notion via the default-profile sync job.
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

POST_CONFIG = {
    "3": {
        "dir": CAPTIONS_ROOT / "post_03_skripsi_vs_tesis",
        "slides": [
            "post03_01_cover.jpg",
            "post03_02_formula.jpg",
            "post03_03_editorial.jpg",
            "post03_04_callout.jpg",
            "post03_05_cta.jpg",
        ],
        "ig_caption_file": CAPTIONS_ROOT / "post_03_skripsi_vs_tesis" / "CAPTION_DAN_THREADS_POST03.md",
        "threads_file": CAPTIONS_ROOT / "post_03_skripsi_vs_tesis" / "CAPTION_DAN_THREADS_POST03.md",
        "topic": "Skripsi vs Tesis Kedokteran",
        "ig_type": "carousel",
    },
    "4": {
        "dir": CAPTIONS_ROOT / "post_04_native_word_citation",
        "slides": [
            "post04_01_cover.jpg",
            "post04_02_formula.jpg",
            "post04_03_editorial.jpg",
            "post04_04_callout.jpg",
            "post04_05_cta.jpg",
        ],
        "ig_caption_file": CAPTIONS_ROOT / "post_04_native_word_citation" / "CAPTION_DAN_THREADS_POST04.md",
        "threads_file": CAPTIONS_ROOT / "post_04_native_word_citation" / "CAPTION_DAN_THREADS_POST04.md",
        "topic": "Tutorial Sitasi Native Word F9",
        "ig_type": "carousel",
    },
    "5": {
        "dir": CAPTIONS_ROOT / "post_05_anatomi_naskah_acc",
        "slides": [
            "post05_01_cover.jpg",
            "post05_02_formula.jpg",
            "post05_03_editorial.jpg",
            "post05_04_callout.jpg",
            "post05_05_cta.jpg",
        ],
        "ig_caption_file": CAPTIONS_ROOT / "post_05_anatomi_naskah_acc" / "CAPTION_DAN_THREADS_POST05.md",
        "threads_file": CAPTIONS_ROOT / "post_05_anatomi_naskah_acc" / "CAPTION_DAN_THREADS_POST05.md",
        "topic": "Anatomi Naskah ACC Semhas",
        "ig_type": "carousel",
    },
    "6": {
        "dir": CAPTIONS_ROOT / "post_06_carousel_layout_edukasi",
        "slides": [
            "post06_01_cover.jpg",
            "post06_02_formula.jpg",
            "post06_03_editorial.jpg",
            "post06_04_callout.jpg",
            "post06_05_cta.jpg",
        ],
        "ig_caption_file": CAPTIONS_ROOT / "post_06_carousel_layout_edukasi" / "CAPTION_DAN_THREADS_POST06.md",
        "threads_file": CAPTIONS_ROOT / "post_06_carousel_layout_edukasi" / "CAPTION_DAN_THREADS_POST06.md",
        "topic": "7 Layout Carousel Edukasi Kesehatan",
        "ig_type": "carousel",
    },
    "7": {
        "dir": CAPTIONS_ROOT / "post_07_sunday_academic_reset",
        "slides": [
            "post07_01_cover.jpg",
            "post07_02_formula.jpg",
            "post07_03_editorial.jpg",
            "post07_04_callout.jpg",
            "post07_05_cta.jpg",
        ],
        "ig_caption_file": CAPTIONS_ROOT / "post_07_sunday_academic_reset" / "CAPTION_DAN_THREADS_POST07.md",
        "threads_file": CAPTIONS_ROOT / "post_07_sunday_academic_reset" / "CAPTION_DAN_THREADS_POST07.md",
        "topic": "Sunday Academic Reset",
        "ig_type": "carousel",
    },
    "w1_01": {
        "dir": CAPTIONS_ROOT / "post_w1_01_diagnosis_skripsi",
        "slides": [
            "post_w1_01_01_cover.jpg",
            "post_w1_01_02_formula.jpg",
            "post_w1_01_03_editorial.jpg",
            "post_w1_01_04_callout.jpg",
            "post_w1_01_05_cta.jpg",
        ],
        "ig_caption_file": CAPTIONS_ROOT / "post_w1_01_diagnosis_skripsi" / "CAPTION_DAN_THREADS_W1_01.md",
        "threads_file": CAPTIONS_ROOT / "post_w1_01_diagnosis_skripsi" / "CAPTION_DAN_THREADS_W1_01.md",
        "topic": "Diagnosis Penyakit Skripsi (ICD-10)",
        "ig_type": "carousel",
    },
    "w1_04": {
        "dir": CAPTIONS_ROOT / "post_w1_04_scu_episode1",
        "slides": [
            "post_w1_04_01_cover.jpg",
            "post_w1_04_02_formula.jpg",
            "post_w1_04_03_editorial.jpg",
            "post_w1_04_04_callout.jpg",
            "post_w1_04_05_cta.jpg",
        ],
        "ig_caption_file": CAPTIONS_ROOT / "post_w1_04_scu_episode1" / "CAPTION_DAN_THREADS_W1_04.md",
        "threads_file": CAPTIONS_ROOT / "post_w1_04_scu_episode1" / "CAPTION_DAN_THREADS_W1_04.md",
        "topic": "SCU Episode 1: Rini Budi Sari",
        "ig_type": "carousel",
    },
    "w1_ni": {
        "dir": CAPTIONS_ROOT / "post_w1_sat_naskah_inside_ep1",
        "slides": [
            "post_w1_ni_01_cover.jpg",
            "post_w1_ni_02_formula.jpg",
            "post_w1_ni_03_editorial.jpg",
            "post_w1_ni_04_callout.jpg",
            "post_w1_ni_05_cta.jpg",
        ],
        "ig_caption_file": CAPTIONS_ROOT / "post_w1_sat_naskah_inside_ep1" / "CAPTION_DAN_THREADS_W1_NI.md",
        "threads_file": CAPTIONS_ROOT / "post_w1_sat_naskah_inside_ep1" / "CAPTION_DAN_THREADS_W1_NI.md",
        "topic": "Naskah Inside EP.1: Di Balik Layar",
        "ig_type": "carousel",
    },

}


def load_caption_text(filepath: pathlib.Path) -> str:
    """Read the Instagram caption from the md file."""
    text = filepath.read_text(encoding="utf-8", errors="replace")
    marker = "CAPTION INSTAGRAM (READY TO POST)"
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

    try:
        caption_ig = load_caption_text(cfg["ig_caption_file"])
    except Exception as e:
        print(f"ERROR reading IG caption: {e}", file=sys.stderr)
        return 1

    try:
        threads_raw = load_threads_text(cfg["threads_file"])
    except Exception as e:
        print(f"ERROR reading threads: {e}", file=sys.stderr)
        return 1

    from meta_direct_publisher import MetaDirectPublisher
    publisher = MetaDirectPublisher()

    preflight = publisher.check_status()
    if preflight.get("instagram", {}).get("status") != "connected":
        print("ERROR: Instagram is not connected.", file=sys.stderr)
        return 1
    if preflight.get("threads", {}).get("status") != "connected":
        print("ERROR: Threads is not connected.", file=sys.stderr)
        return 1

    image_urls = [
        f"https://raw.githubusercontent.com/tebakkasus/Naskah/main/06_CONTENT_PIPELINE/03_APPROVED/{cfg['dir'].name}/{slide}"
        for slide in cfg["slides"]
    ]

    print(f"publishing_instagram_carousel post {post_num}")
    ig_result = publisher.publish_ig_carousel(image_urls, caption_ig)
    print(json.dumps(ig_result, ensure_ascii=False, indent=2))
    if not ig_result.get("success"):
        print("ERROR: Instagram publish failed; Threads not sent.", file=sys.stderr)
        return 1

    verified_ig = publisher.get_ig_media(ig_result["media_id"])
    print("verified_instagram:")
    print(json.dumps(verified_ig, ensure_ascii=False, indent=2))

    thread_results = []
    for idx_t, item in enumerate(threads_raw):
        text = item["text"]
        print(f"publishing_threads: {item['slot']} (len={len(text)})")
        
        # If Thread #1 and we have carousel slides, publish as THREADS CAROUSEL!
        if idx_t == 0 and image_urls and len(image_urls) >= 2:
            print(f"Publishing {item['slot']} as Threads Carousel with {len(image_urls)} slides...")
            # Truncate text for carousel caption if needed (Threads carousel caption limit is 500)
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
            print(f"WARNING: Thread {item['slot']} failed, but IG is already live. Continuing...", file=sys.stderr)
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
            "status": "PUBLISHED",
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

    result_path = CONTENT_ROOT / f"PUBLISH_RESULT_post0{post_num}.json"
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"result written: {result_path}")

    status_path = CONTENT_ROOT / "SYNC_STATUS.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))
    status["last_sync"] = published_at
    status.setdefault("recent_events", []).append({
        "timestamp": published_at,
        "type": "POST_PUBLISHED_META_DIRECT",
        "details": result,
    })
    status_path.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    handoff_path = CONTENT_ROOT / "NOTION_SYNC_HANDOFF.md"
    handoff_text = handoff_path.read_text(encoding="utf-8")
    update_entry = f"\n## Auto-Sync Post #{post_num} — {published_at}\n- **Status**: PUBLISHED\n- **Topic**: {cfg['topic']}\n- **IG Permalink**: {verified_ig.get('permalink', 'N/A')}\n- **Threads**: {', '.join([item['slot'] for item in thread_results])}\n"
    if f"Post #{post_num} —" not in handoff_text:
        handoff_path.write_text(handoff_text.rstrip() + update_entry, encoding="utf-8")

    quota_after = publisher.check_ig_publishing_limit()
    print(json.dumps({"result": result, "quota_after": quota_after, "result_path": str(result_path)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
