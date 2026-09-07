"""
Daily Content Dispatcher for Naskah Social OS.

Runs daily at 10:00 WIB via Hermes cron.
Determines which post is scheduled for today, executes publication via
publish_postxx.py, updates Notion and handoff files, and generates a
consolidated report for Telegram.
"""
from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
from datetime import datetime, timezone, timedelta

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
GENERATORS_DIR = ROOT_DIR / "04_GENERATORS"

SCHEDULE_MAP = {
    "2026-09-07": "3",  # Monday: Post #3
    "2026-09-08": "4",  # Tuesday: Post #4
    "2026-09-09": "5",  # Wednesday: Post #5
    "2026-09-10": "6",  # Thursday: Post #6
    "2026-09-11": "7",  # Friday: Post #7
}


def today_wib() -> str:
    return datetime.now(timezone(timedelta(hours=7))).strftime("%Y-%m-%d")


def main() -> int:
    current_date = today_wib()
    print(f"=== Daily Content Dispatcher: {current_date} ===")

    post_num = SCHEDULE_MAP.get(current_date)
    if not post_num:
        print(f"No scheduled post for today ({current_date}). Standing by.")
        return 0

    print(f"Executing scheduled publication: Post #{post_num}")
    script_path = GENERATORS_DIR / "publish_postxx.py"

    cmd = [sys.executable, str(script_path), post_num]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR))

    print("STDOUT:")
    print(result.stdout)
    if result.stderr:
        print("STDERR:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)

    if result.returncode != 0:
        print(f"ERROR: Publication of Post #{post_num} failed with return code {result.returncode}", file=sys.stderr)
        return result.returncode

    print(f"✅ Successfully published and recorded Post #{post_num} for {current_date}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
