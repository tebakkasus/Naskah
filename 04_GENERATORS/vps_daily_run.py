"""
VPS Daily Runner — Naskah Social OS (24/7 autonomous).

Runs from the VPS every day at 10:00 WIB:
1. Determines which post is scheduled for today (Mon-Fri working week).
2. Executes publication via publish_postxx.py (IG carousel + 2 Threads).
3. Appends evidence to SYNC_STATUS.json for the Notion engine.
4. Sends a concise Telegram report to TM.

Requires on the VPS:
- ~/content/06_Content/  (mirror of the laptop pipeline folder)
- ~/content/06_Content/.env (Meta credentials — installed by setup)
"""
from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
from datetime import datetime, timezone, timedelta

ROOT_DIR = pathlib.Path(__file__).resolve().parent
CONTENT_PIPELINE = ROOT_DIR.parent
GENERATORS = ROOT_DIR

# Date -> post number mapping (Week 0 + Week 1 Full Schedule)
# ============================================================
# SCHEDULE MAP — Single Source of Truth for Daily Publisher
# ============================================================
# Format: "YYYY-MM-DD": {"post": "POST_NUM", "slots": {"morning": true, "afternoon": true, "evening": true, "3am": false}}
#   - morning (10:00)   = IG Carousel/Single + Thread #1
#   - afternoon (14:00) = Threads Visual Mirror (images only)
#   - evening (19:00)   = Thread #2 (storytelling/relatable/hard-sell)
#   - 3am (03:00)       = 3AM Thoughts (Week 1 only: w1_06)
#   - "skip_3am": true  = Week 0 posts do NOT have 3am content; skip entirely
# ============================================================
SCHEDULE_MAP = {
    # Week 0 (W36: 7-13 Sep 2026) — NO 3am slot
    "2026-09-07": {"post": "3",  "skip_3am": True},   # Senin: Skripsi vs Tesis
    "2026-09-08": {"post": "4",  "skip_3am": True},   # Selasa: Sitasi Native Word
    "2026-09-09": {"post": "5",  "skip_3am": True},   # Rabu: Anatomi Naskah ACC
    "2026-09-10": {"post": "6",  "skip_3am": True},   # Kamis: 7 Layout Carousel
    "2026-09-11": {"post": "7",  "skip_3am": True},   # Jumat: Sunday Academic Reset
    "2026-09-12": {"post": "8",  "skip_3am": True},   # Sabtu: Hard Sell 3JT
    "2026-09-13": {"post": "9",  "skip_3am": True},   # Minggu: Menu & Harga

    # Week 1 (W37: 14-20 Sep 2026) — "Introduction to Madness" — HAS 3am for w1_06
    "2026-09-14": {"post": "w1_01", "skip_3am": True},  # Senin: ICD-10 Diagnosis
    "2026-09-15": {"post": "w1_02", "skip_3am": True},  # Selasa: 2 Kebenaran (Threads-only)
    "2026-09-16": {"post": "w1_03", "skip_3am": True},  # Rabu: Autopsi Abstrak (Threads-only)
    "2026-09-17": {"post": "w1_04", "skip_3am": True},  # Kamis: SCU Ep.1
    "2026-09-18": {"post": "w1_05", "skip_3am": True},  # Jumat: Revisi Bingo
    "2026-09-19": {"post": "w1_ni",  "skip_3am": True},  # Sabtu: Naskah Inside
    "2026-09-20": {"post": "w1_06", "skip_3am": False},  # Minggu: 3AM Thoughts — ONLY day with 3am
}

def load_env_file():
    env_path = CONTENT_PIPELINE / ".env"
    if not env_path.exists():
        env_path = CONTENT_PIPELINE / "06_CONTENT_PIPELINE" / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if line_str and not line_str.startswith("#") and "=" in line_str:
                    key, val = line_str.split("=", 1)
                    os.environ[key.strip()] = val.strip().strip("\"'")

load_env_file()
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "8557883180")


def now_wib() -> str:
    return datetime.now(timezone(timedelta(hours=7))).strftime("%Y-%m-%d %H:%M WIB")


def send_telegram(text: str) -> dict:
    """Send a message to TM's Telegram via the bot API."""
    if not TELEGRAM_BOT_TOKEN:
        return {"success": False, "error": "TELEGRAM_BOT_TOKEN not set"}
    import requests
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}
    try:
        r = requests.post(url, json=payload, timeout=30)
        return {"success": r.status_code == 200, "status": r.status_code, "body": r.text[:300]}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def update_notion_via_api(result: dict) -> dict:
    """
    Update the Notion Command Center database for the published post.
    Uses the Notion REST API with the token from .env. Safe no-op when token missing.
    """
    import requests

    notion_key = os.environ.get("NOTION_API_KEY", "")
    if not notion_key:
        return {"success": False, "error": "NOTION_API_KEY not set (skipping Notion update)"}

    data_source_id = "3d2b044d-7011-817a-8e98-000b9bd9a77c"
    headers = {
        "Authorization": f"Bearer {notion_key}",
        "Notion-Version": "2025-09-03",
        "Content-Type": "application/json",
    }

    # Find the row by scanning the data source (rows mode)
    # Fetch all rows via the API search for the data source
    try:
        # Query the data source rows by POST to the query endpoint
        query_url = f"https://api.notion.com/v1/data_sources/{data_source_id}/query"
        resp = requests.post(query_url, headers=headers, json={"page_size": 100}, timeout=30)
        if resp.status_code != 200:
            return {"success": False, "error": f"Notion query failed: {resp.status_code} {resp.text[:200]}"}
        rows = resp.json().get("results", [])

        post_num = result.get("post_number")
        ig_permalink = result.get("instagram", {}).get("permalink", "")
        threads = result.get("threads", [])

        # Match row whose Title contains the post number keyword.
        # The IG row for post N usually has a topic title; we rely on thread slots
        # in the result to locate matching standalone thread rows by their title
        # containing "Thread #X".
        updated = []
        for row in rows:
            title = ""
            for prop in row.get("properties", {}).values():
                if prop.get("type") == "title":
                    title = "".join(t.get("text", {}).get("content", "") for t in prop.get("title", []))
                    break
            # Update thread rows whose title matches "Thread #N"
            for t in threads:
                slot = t.get("slot", "")  # e.g. "#5"
                num = slot.lstrip("#")
                if num and f"Thread #{num}" in title:
                    page_id = row["id"]
                    update_payload = {
                        "properties": {
                            "Status": {"select": {"name": "Published"}},
                            "Threads Link": {"rich_text": [{"text": {"content": t.get("thread_id", "")}}]},
                            "Last Synced": {"rich_text": [{"text": {"content": now_wib()}}]},
                        }
                    }
                    ur = requests.patch(
                        f"https://api.notion.com/v1/pages/{page_id}",
                        headers=headers,
                        json=update_payload,
                        timeout=30,
                    )
                    if ur.status_code == 200:
                        updated.append(f"Thread #{num}")
        return {"success": True, "updated": updated, "ig_permalink": ig_permalink}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def main() -> int:
    now_dt = datetime.now(timezone(timedelta(hours=7)))
    current_date = now_dt.strftime("%Y-%m-%d")
    current_hour = now_dt.hour
    
    # Auto-detect slot based on current hour in WIB
    if 2 <= current_hour <= 5:
        slot = "3am"
    elif 13 <= current_hour <= 16:
        slot = "afternoon"
    elif 17 <= current_hour <= 23:
        slot = "evening"
    else:
        slot = "morning"

    print(f"=== VPS Daily Runner: {current_date} {now_wib()} (Slot: {slot.upper()}) ===")

    schedule = SCHEDULE_MAP.get(current_date)
    if not schedule:
        print(f"No scheduled post for today ({current_date}). Standby.")
        return 0

    post_num = schedule["post"]
    skip_3am = schedule.get("skip_3am", True)

    # === NEW: Idempotency Guard ===
    import json
    from datetime import date
    today_str = date.today().strftime("%Y-%m-%d")
        
    # Backward compat for zero-padded numeric posts (e.g. 06)
    if post_num.isdigit():
        result_name = f"PUBLISH_RESULT_post0{post_num}.json"
    else:
        result_name = f"PUBLISH_RESULT_post{post_num}.json"
            
    result_path = CONTENT_PIPELINE / "06_CONTENT_PIPELINE" / result_name
    already_published_today = result_path.exists()

    # Jika slot 3am dan skip_3am=True (Week 0), power skip total
    if slot == "3am" and skip_3am:
        print(f"🛡️ SKIP 3am untuk post {post_num} (Week 0: no 3am content scheduled). Standby.")
        return 0

    # Jika slot 3am tapi ini post dari Week 1 (w1_06) yang DOYAN 3am
    if slot == "3am" and not skip_3am and post_num == "w1_06":
        print(f"🟢 3am publish untuk post {post_num} — Ini minggu 1 dengan 3AM Thoughts.")
    elif slot == "3am" and not skip_3am:
        print(f"⚠️ 3am slot requested but post {post_num} has skip_3am=True. Overriding to standby.")
        return 0

    # Jika post sudah dipublish hari ini — ABORT untuk mencegah double-publish
    if already_published_today:
        published = json.loads(result_path.read_text(encoding="utf-8"))
        ig_status = published.get("instagram", {}).get("status", "UNKNOWN")
        print(f"🛡️ IDENTIKASI: Post #{post_num} sudah dipublish tadi hari ini (status IG: {ig_status}). Skip publish, melanjutkan ke laporan TG.")
        
        published_at = now_wib()
        notion_update = {"success": True, "updated": [], "ig_permalink": published.get("instagram", {}).get("permalink", "")}
        
        ig = published.get("instagram", {})
        ig_url = ig.get("permalink", "")
        threads = published.get("threads", [])
        thread_links = " | ".join([f'<a href="{t.get("permalink", "")}">{t.get("slot", "")}</a>' for t in threads if t.get("permalink")])
        notion_status = "Synced" if notion_update.get("success") else "Failed"
        next_slot_str = "14:00 WIB (Threads Visual)" if slot == "morning" else ("19:00 WIB (Thread #2)" if slot == "afternoon" else ("03:00 WIB (3AM)" if slot == "evening" else "10:00 WIB (IG + Thread #1)"))
        
        report = (
            f"✅ <b>Post #{post_num} [{slot.upper()}]: {published.get('topic', '')}</b>\n\n"
            f"📸 <b>IG:</b> " + (f'<a href="{ig_url}">Live Post</a>\n' if ig_url else "N/A (Threads Slot)\n") +
            f"🧵 <b>Threads:</b> {thread_links if thread_links else 'Published'}\n"
            f"🗂️ <b>Notion:</b> {notion_status}\n\n"
            f"⏭️ <b>Next Slot:</b> {next_slot_str}"
        )
        print("TELEGRAM REPORT (REUSE EXISTING):")
        print(report)
        tg = send_telegram(report)
        print("Telegram result:", json.dumps(tg, ensure_ascii=False))
        return 0

    print(f"Scheduled Post #{post_num} for today (Target Slot: {slot}).")

    script = GENERATORS / "publish_postxx.py"
    if not script.exists():
        print(f"ERROR: publish_postxx.py not found at {script}", file=sys.stderr)
        return 1

    cmd = [sys.executable, str(script), post_num, "--slot", slot]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(CONTENT_PIPELINE))

    print("STDOUT:", result.stdout[-3000:])
    if result.stderr:
        print("STDERR:", result.stderr[-1500:], file=sys.stderr)

    if result.returncode == 0:
        print(f"Post #{post_num} slot '{slot}' published successfully.")
    else:
        print(f"ERROR: Post #{post_num} slot '{slot}' publish failed rc={result.returncode}", file=sys.stderr)

    # Load latest PUBLISH_RESULT for reporting / Notion update
    if post_num.isdigit():
        result_name = f"PUBLISH_RESULT_post0{post_num}.json"
    else:
        result_name = f"PUBLISH_RESULT_post{post_num}.json"
    result_path = CONTENT_PIPELINE / "06_CONTENT_PIPELINE" / result_name
    published = None
    if result_path.exists():
        try:
            published = json.loads(result_path.read_text(encoding="utf-8"))
        except Exception:
            published = None
    if published:
        notion_update = update_notion_via_api(published)
        print("Notion update:", json.dumps(notion_update, ensure_ascii=False))

        # Build Telegram report (Compact TM Standard)
        ig = published.get("instagram", {})
        ig_url = ig.get("permalink", "")
        threads = published.get("threads", [])
        
        thread_links = " | ".join([f'<a href="{t.get("permalink", "")}">{t.get("slot", "")}</a>' for t in threads if t.get("permalink")])
        notion_status = "Synced" if notion_update.get("success") else "Failed"

        next_val = "besok sesuai jadwal"
        try:
            next_val = f"Post #{int(post_num)+1}"
        except Exception:
            pass

        next_slot_str = "14:00 WIB (Threads Visual)" if slot == "morning" else ("19:00 WIB (Thread #2)" if slot == "afternoon" else ("03:00 WIB (3AM)" if slot == "evening" else "10:00 WIB (IG + Thread #1)"))

        report = (
            f"✅ <b>Post #{post_num} [{slot.upper()}]: {published.get('topic', '')}</b>\n\n"
            f"📸 <b>IG:</b> " + (f'<a href="{ig_url}">Live Post</a>\n' if ig_url else "N/A (Threads Slot)\n") +
            f"🧵 <b>Threads:</b> {thread_links if thread_links else 'Published'}\n"
            f"🗂️ <b>Notion:</b> {notion_status}\n\n"
            f"⏭️ <b>Next Slot:</b> {next_slot_str}"
        )
        print("TELEGRAM REPORT:")
        print(report)
        tg = send_telegram(report)
        print("Telegram result:", json.dumps(tg, ensure_ascii=False))
    else:
        print(f"No PUBLISH_RESULT found for post #{post_num}.")

    return result.returncode if result.returncode != 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())