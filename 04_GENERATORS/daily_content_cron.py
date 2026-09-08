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
    # Week 0 (W36: 7-13 Sep 2026)
    "2026-09-07": "3",      # Senin: Skripsi vs Tesis
    "2026-09-08": "4",      # Selasa: Sitasi Native Word
    "2026-09-09": "5",      # Rabu: Anatomi Naskah ACC
    "2026-09-10": "6",      # Kamis: 7 Layout Carousel
    "2026-09-11": "7",      # Jumat: Sunday Academic Reset

    # Week 1 (W37: 14-20 Sep 2026) — "Introduction to Madness"
    "2026-09-14": "w1_01",  # Senin: ICD-10 Diagnosis Penyakit Skripsi (Carousel)
    "2026-09-15": "w1_02",  # Selasa: Dua Kebenaran Satu Bohong Metpen (Threads)
    "2026-09-16": "w1_03",  # Rabu: Autopsi Abstrak UGC Call (Threads)
    "2026-09-17": "w1_04",  # Kamis: SCU Episode 1 Rini Budi Sari (Carousel)
    "2026-09-18": "w1_05",  # Jumat: Revisi Bingo Dosen Pembimbing (Single Image)
    "2026-09-19": "w1_ni",  # Sabtu: Naskah Inside EP.1 Di Balik Layar (Carousel)
    "2026-09-20": "w1_06",  # Minggu: Jam 3 Pagi Threads 3AM Thoughts (Threads)
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
