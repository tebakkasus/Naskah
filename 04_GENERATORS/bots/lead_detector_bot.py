#!/usr/bin/env python3
"""
Lead Detector & AI Auto-Reply Draft Bot for Naskah.fk (@naskah.efka)
Monitors recent Instagram & Threads comments/replies for potential client intent.
Flags buying intent / questions and generates 2 ready-to-use reply drafts via local 9router LLM.
"""

import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
import requests
from dotenv import dotenv_values

# Load environment
ENV_PATH = Path("/home/hermes.taci/workspaces/content/.env")
HERMES_ENV = Path("/home/hermes.taci/.hermes/.env")

env = {}
if HERMES_ENV.exists():
    env.update(dotenv_values(HERMES_ENV))
if ENV_PATH.exists():
    env.update(dotenv_values(ENV_PATH))

IG_TOKEN = env.get("INSTAGRAM_ACCESS_TOKEN")
IG_USER_ID = env.get("INSTAGRAM_USER_ID", "27859248840424916")
THREADS_TOKEN = env.get("THREADS_ACCESS_TOKEN")
TG_BOT_TOKEN = env.get("TELEGRAM_BOT_TOKEN")
TG_CHAT_ID = env.get("TELEGRAM_CHAT_ID", "8557883180")
ROUTER_KEY = env.get("HERMES_CUSTOM_9ROUTER_API_KEY") or env.get("OPENAI_API_KEY")

STATE_FILE = Path("/home/hermes.taci/workspaces/content/06_CONTENT_PIPELINE/SEEN_COMMENTS_STATE.json")

# Keywords indicating intent or questions
INTENT_KEYWORDS = [
    "harga", "biaya", "price", "berapa", "tarif", "paket",
    "dm", "pm", "wa", "whatsapp", "pesan",
    "gimana", "bagaimana", "cara", "caranya", "order", "bantu", "bisa",
    "konsul", "konsultasi", "bimbing", "bimbingan", "joki", "jasa",
    "olah", "spss", "analisis", "bab 1", "bab 2", "bab 3", "bab 4", "bab 5",
    "sempro", "semhas", "sidang", "skripsi", "tesis", "naskah", "jurnal",
    "stuck", "pusing", "tolong", "mau", "min", "kak", "bang"
]

def now_wib_str() -> str:
    tz = timezone(timedelta(hours=7))
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S WIB")

def load_seen_state() -> set:
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            return set(data.get("seen_ids", []))
        except Exception:
            return set()
    return set()

def save_seen_state(seen_ids: set):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    # Keep only last 1000 IDs to avoid bloat
    recent = list(seen_ids)[-1000:]
    STATE_FILE.write_text(json.dumps({"seen_ids": recent, "updated_at": now_wib_str()}, indent=2), encoding="utf-8")

def send_telegram(text: str) -> dict:
    if not TG_BOT_TOKEN or not TG_CHAT_ID:
        return {"success": False, "error": "No TG credentials"}
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        r = requests.post(url, json=payload, timeout=20)
        return r.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def generate_ai_replies(user_comment: str, platform: str) -> str:
    prompt = f"""Kamu adalah Social Media Manager dan Academic Consultant dari brand 'Naskah.fk' (@naskah.efka di Threads).
Naskah.fk adalah Academic Companion untuk mahasiswa kedokteran & kesehatan yang menyediakan bimbingan skripsi Bab 1-5, olah data SPSS/statistik, dan review jurnal.
Gaya bahasa: Ramah, santun, solutif, khas anak FK/akademik yang tidak kaku, profesional, dan mendorong mereka untuk DM/konsultasi.

Komentar pengguna ({platform}):
"{user_comment}"

Tugas: Buat 2 opsi draft balasan singkat yang siap di-copy-paste:
Opsi 1: Ramah, to-the-point & call-to-action DM.
Opsi 2: Empatik, sedikit edukatif/santai & call-to-action DM.

Format output WAJIB persis seperti ini (tanpa kalimat pembuka lain):
<b>Draft 1:</b>
[Teks balasan 1]

<b>Draft 2:</b>
[Teks balasan 2]"""

    try:
        url = "http://127.0.0.1:20128/v1/chat/completions"
        headers = {"Content-Type": "application/json"}
        if ROUTER_KEY:
            headers["Authorization"] = f"Bearer {ROUTER_KEY}"
        
        payload = {
            "model": "monet",
            "messages": [
                {"role": "system", "content": "You are a professional social media marketing assistant for medical students."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 400
        }
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        if r.status_code == 200:
            data = r.json()
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        pass
    
    # Fallback default drafts if LLM is unreachable
    return (
        "<b>Draft 1:</b>\n"
        "Halo kak! Boleh banget, langsung DM ke @naskah.fk atau klik link di bio yaa biar kita bantu diskusikan kebutuhan naskah/olah datanya! 🩺✨\n\n"
        "<b>Draft 2:</b>\n"
        "Hai kak! Tergantung jenis penelitian & bab yang mau dibahas yaa. Yuk ngobrol santai via DM, kita spill detail paket & diskon khususnya! 🙌"
    )

def check_threads_comments(seen_ids: set) -> list:
    if not THREADS_TOKEN:
        return []
    alerts = []
    try:
        url = f"https://graph.threads.net/v1.0/me/threads?fields=id,text,replies{{id,text,username,timestamp}}&access_token={THREADS_TOKEN}"
        r = requests.get(url, timeout=25)
        if r.status_code != 200:
            return []
        data = r.json().get("data", [])
        for thread in data:
            parent_text = thread.get("text", "")[:80]
            replies = thread.get("replies", {}).get("data", [])
            for rep in replies:
                rep_id = rep.get("id")
                username = rep.get("username", "")
                text = rep.get("text", "")
                # Skip own replies and already seen
                if username == "naskah.efka" or rep_id in seen_ids:
                    continue
                seen_ids.add(rep_id)
                # Check intent
                text_lower = text.lower()
                is_lead = any(kw in text_lower for kw in INTENT_KEYWORDS) or "?" in text
                alerts.append({
                    "platform": "Threads",
                    "id": rep_id,
                    "username": username,
                    "text": text,
                    "parent_text": parent_text,
                    "is_lead": is_lead
                })
    except Exception as e:
        print(f"Error checking Threads: {e}")
    return alerts

def check_instagram_comments(seen_ids: set) -> list:
    if not IG_TOKEN or not IG_USER_ID:
        return []
    alerts = []
    try:
        url = f"https://graph.instagram.com/v21.0/{IG_USER_ID}/media?fields=id,caption,comments{{id,text,username,timestamp}}&access_token={IG_TOKEN}"
        r = requests.get(url, timeout=25)
        if r.status_code != 200:
            return []
        data = r.json().get("data", [])
        for media in data:
            caption = media.get("caption", "")[:80]
            comments = media.get("comments", {}).get("data", [])
            for comm in comments:
                comm_id = comm.get("id")
                username = comm.get("username", "")
                text = comm.get("text", "")
                if username == "naskah.efka" or comm_id in seen_ids:
                    continue
                seen_ids.add(comm_id)
                text_lower = text.lower()
                is_lead = any(kw in text_lower for kw in INTENT_KEYWORDS) or "?" in text
                alerts.append({
                    "platform": "Instagram",
                    "id": comm_id,
                    "username": username,
                    "text": text,
                    "parent_text": caption,
                    "is_lead": is_lead
                })
    except Exception as e:
        print(f"Error checking Instagram: {e}")
    return alerts

def main():
    seen_ids = load_seen_state()
    initial_run = len(seen_ids) == 0

    threads_alerts = check_threads_comments(seen_ids)
    ig_alerts = check_instagram_comments(seen_ids)
    
    save_seen_state(seen_ids)

    all_alerts = threads_alerts + ig_alerts
    print(f"[{now_wib_str()}] Found {len(all_alerts)} new comment(s). (Initial run: {initial_run})")

    # If first run, don't flood past comments, just baseline state
    if initial_run:
        print("Initial run completed. Baseline saved.")
        return

    for alert in all_alerts:
        platform = alert["platform"]
        username = alert["username"]
        comment_text = alert["text"]
        parent = alert["parent_text"]
        is_lead = alert["is_lead"]

        urgency_badge = "🔥 <b>HOT LEAD / PERTANYAAN MASUK!</b>" if is_lead else "💬 <b>Komentar Baru</b>"
        
        # Generate AI reply draft
        ai_drafts = generate_ai_replies(comment_text, platform)

        msg = (
            f"{urgency_badge}\n"
            f"📱 <b>Platform:</b> {platform}\n"
            f"👤 <b>User:</b> @{username}\n"
            f"💬 <b>Komentar:</b> <i>\"{comment_text}\"</i>\n"
            f"📌 <b>Post:</b> <i>\"{parent}...\"</i>\n\n"
            f"⚡ <b>Rekomendasi Balasan Cepat (AI):</b>\n"
            f"{ai_drafts}\n\n"
            f"👉 <i>Copy salah satu draft di atas & paste langsung ke aplikasi {platform} untuk respon instan!</i>"
        )
        send_telegram(msg)
        print(f"Alert sent to TG for @{username} on {platform}")

if __name__ == "__main__":
    main()
