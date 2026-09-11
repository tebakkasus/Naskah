# 2026-09-10 Double-Publish Postmortem

## Symptoms

- Three Threads posts from `@naskah.efka` on 2026-09-10 showed **identical** caption text (`"Kenapa konten edukasi medis sering terasa membosankan di media sosial..."`), posted at 18:53 WIB and 02:53 WIB — a ~16 hour gap with matching content.
- IG carousel for Post #6 (`7 Layout Carousel Edukasi Kesehatan`) published successfully at 10:00 WIB (morning slot) but then re-published at 19:00 WIB (evening slot) with **exact same text and visual assets**.
- TM flagged: *"pahami dulu timelinenya, jangan sampai salah lagi"* — repeated requests to respect the slot timeline.

## Root Causes (simultaneous, three independent bugs)

### 1. Zero-padding mismatch in `vps_daily_run.py`

- The idempotency guard checked for `PUBLISH_RESULT_post6.json` (no zero-pad).
- The publisher writes `PUBLISH_RESULT_post06.json` (zero-padded for numeric posts, consistent with `publish_post01.py` naming).
- **Result**: `already_published_today` evaluated to `False` every run → guard never triggered.

### 2. `image_urls` ordering bug in `publish_postxx.py`

- `image_urls` was defined **after** the slot-dispatch block (line 340).
- The `afternoon` branch (line 316) referenced `image_urls` via `publish_threads_visual = True if image_urls else False`.
- **Result**: `NameError` on afternoon slot, or silent fallthrough depending on Python scoping, causing threads to be published without images or not at all.

### 3. `3am` slot dumps ALL threads

- In `publish_postxx.py` line 325: `selected_threads = threads_raw` (all threads).
- Slot 3am republished Thread #1 **and** Thread #2 text → guaranteed duplicate content.
- The `skip_3am` flag in `SCHEDULE_MAP` was not set for Week 0 posts, so every `3am` crontab run attempted to publish full thread dump.

## Fixes Applied (verified on VPS 103.93.134.118)

| Fix | File | Change |
|-----|------|--------|
| **Zero-padding guard** | `vps_daily_run.py:192-193` | Compute `result_name` using `.isdigit()` → `post0{N}.json` for numeric posts; plain `post{N}` for Week 1 (`w1_01`, etc.). |
| **`image_urls` ordering** | `publish_postxx.py:340-345` | Moved `image_urls` definition **before** the slot-dispatch block (before line 310). |
| **3am hard block** | `publish_postxx.py:322-326` | Added guard: 3am slot ONLY valid for `post_num == "w1_06"`. All other posts set `selected_threads = []` and `return 0`. Also `vps_daily_run.py` sets `skip_3am=True` for all Week 0 and most Week 1 entries; only `w1_06` has `False`. |
| **Crontab pull pattern** | VPS workflow | `git stash && git pull origin main && git stash pop` before each daily run to avoid `NOTION_SYNC_HANDOFF.md` dirty-state conflicts. |

## Verification

```
$ ssh hermes.taci@103.93.134.118 "cd ~/content/06_Content && python3 04_GENERATORS/vps_daily_run.py"
🛡️ IDENTIKASI: Post #6 sudah dipublish tadi hari ini (status IG: PUBLISHED). Skip publish, melanjutkan ke laporan TG.
```

Output confirms guard triggered, no re-publish, Telegram report still sent with reused permalinks.

## Timeline (TM canonical, MEMORIZE)

| WIB | Slot | Expected Post |
|:---:|:---|:---|
| **10:00** | `morning` | Post #1 (IG + Thread #1 text hook) |
| **14:00** | `afternoon` | Threads visual mirror only (carousel images, NO text thread) |
| **19:00** | `evening` | Thread #2 (storytelling/relatable/hard-sell) |
| **03:00** | `3am` | **Skip** for Week 0 (#3–#9). Only Post `w1_06` runs 3AM Thoughts. |

> **TM rule**: "pahami dulu timelinenya, jangan sampai salah lagi." Always read `SCHEDULE_MAP` + `NOTION_SYNC_HANDOFF.md` before touching the pipeline.

## Related Skills

- `social-auto-publisher` — operate/debug Naskah IG+Threads VPS cron publisher; slot timeline, anti-duplicate.