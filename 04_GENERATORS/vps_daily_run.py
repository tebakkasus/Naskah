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

# Date -> post number mapping (this week's plan, already advanced to Mon-Fri)
SCHEDULE_MAP = {
    "2026-09-07": "3",
    "2026-09-08": "4",
    "2026-09-09": "5",
    "2026-09-10": "6",
    "2026-09-11": "7",
}

# Next week placeholder — extend as the plan evolves
SCHEDULE_MAP_NEXT = {
    # Week 1 (14-20 Sep 2026) — "Introduction to Madness"
    "2026-09-14": "w1_01",  # Senin: ICD-10 Diagnosis Penyakit Skripsi
    "2026-09-17": "w1_04",  # Kamis: SCU Episode 1 (Rini, Budi, Sari)
    "2026-09-19": "w1_ni",  # Sabtu: Naskah Inside EP.1
}

def load_env_file():
    env_path = CONTENT_PIPELINE / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, val = line.strip().split("=", 1)
                    os.environ[key] = val

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
    current_date = datetime.now(timezone(timedelta(hours=7))).strftime("%Y-%m-%d")
    print(f"=== VPS Daily Runner: {current_date} {now_wib()} ===")

    post_num = SCHEDULE_MAP.get(current_date)
    if not post_num:
        print(f"No scheduled post for today ({current_date}). Standby.")
        return 0

    print(f"Scheduled Post #{post_num} for today.")

    # Anti-double-publish: if a PUBLISH_RESULT already exists for this post, skip.
    existing_result = CONTENT_PIPELINE / "06_CONTENT_PIPELINE" / f"PUBLISH_RESULT_post0{post_num}.json"
    if existing_result.exists():
        print(f"SKIP: {existing_result.name} already exists — post #{post_num} already published. No double-publish.")
        return 0

    script = GENERATORS / "publish_postxx.py"
    if not script.exists():
        print(f"ERROR: publish_postxx.py not found at {script}", file=sys.stderr)
        return 1

    cmd = [sys.executable, str(script), post_num]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(CONTENT_PIPELINE))

    print("STDOUT:", result.stdout[-3000:])
    if result.stderr:
        print("STDERR:", result.stderr[-1500:], file=sys.stderr)

    if result.returncode == 0:
        print(f"Post #{post_num} published successfully.")
    else:
        print(f"ERROR: Post #{post_num} publish failed rc={result.returncode}", file=sys.stderr)

    # Load latest PUBLISH_RESULT for reporting / Notion update
    result_path = CONTENT_PIPELINE / "06_CONTENT_PIPELINE" / f"PUBLISH_RESULT_post0{post_num}.json"
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

        report = (
            f"✅ <b>Post #{post_num}: {published.get('topic', '')}</b>\n\n"
            f"📸 <b>IG:</b> <a href=\"{ig_url}\">Live Post</a>\n"
            f"🧵 <b>Threads:</b> {thread_links}\n"
            f"🗂️ <b>Notion:</b> {notion_status}\n\n"
            f"⏭️ <b>Next:</b> Post #{int(post_num)+1} (Besok 10:00 WIB)"
        )
        print("TELEGRAM REPORT:")
        print(report)
        tg = send_telegram(report)
        print("Telegram result:", json.dumps(tg, ensure_ascii=False))
    else:
        print("No PUBLISH_RESULT found for today's post.")

    return result.returncode if result.returncode != 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())