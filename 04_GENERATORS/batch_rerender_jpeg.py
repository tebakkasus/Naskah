"""
Rerender all approved posts (Post 01 - Post 07) directly to high-quality JPEG,
generate their JPEG contact sheet previews, copy directly to 03_APPROVED,
and delete all legacy PNG slide files across 05_OUTPUTS and 06_CONTENT_PIPELINE.
"""

import os
import sys
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
IDEAS_DIR = ROOT / "06_CONTENT_PIPELINE" / "01_IDEAS"
OUTPUTS_DIR = ROOT / "05_OUTPUTS"
APPROVED_DIR = ROOT / "06_CONTENT_PIPELINE" / "03_APPROVED"

POSTS = [
    ("topic_01_word_citation.json", "post_01_word_citation", "post01", "POST #1: 5 KESALAHAN FATAL SITASI DI WORD", "Slide Format & Auto-Update F9 Protocol"),
    ("topic_02_jurnal_kedokteran.json", "post_02_jurnal_kedokteran", "post02", "POST #2: FORMAT MANUSKRIP JURNAL KEDOKTERAN", "Standar Tabel Terbuka & Checklist Publikasi"),
    ("topic_03_skripsi_vs_tesis.json", "post_03_skripsi_vs_tesis", "post03", "POST #3: SKRIPSI VS TESIS KEDOKTERAN", "Perbedaan Mindset, Sintesis & Metodologi Riset"),
    ("topic_04_native_word_citation.json", "post_04_native_word_citation", "post04", "POST #4: TUTORIAL SITASI NATIVE WORD", "Solusi Ringan & Stabil Tanpa Plugin Lemot"),
    ("topic_05_anatomi_naskah_acc.json", "post_05_anatomi_naskah_acc", "post05", "POST #5: ANATOMI NASKAH ACC SEMHAS", "Struktur Latar Belakang & Pembahasan Tajam"),
    ("topic_06_carousel_layout_edukasi.json", "post_06_carousel_layout_edukasi", "post06", "POST #6: 7 LAYOUT CAROUSEL EDUKASI", "Inspirasi Visual Konten Akademik & Kesehatan"),
    ("topic_07_sunday_academic_reset.json", "post_07_sunday_academic_reset", "post07", "POST #7: SUNDAY ACADEMIC RESET", "Evaluasi Mingguan & Mindset Progress > Perfection"),
]

def clean_png_files():
    print("--- 1. Cleaning legacy PNG slides and preview PNGs ---")
    deleted = 0
    for folder in [OUTPUTS_DIR, APPROVED_DIR]:
        for p in folder.rglob("*.png"):
            # Don't delete brand assets if any, only post slide pngs and preview pngs
            if "02_BRAND_ASSETS" not in str(p):
                p.unlink()
                deleted += 1
    print(f"Deleted {deleted} legacy PNG files.")

def rerender_all_jpeg():
    print("\n--- 2. Rerendering Posts 01-07 to direct JPEG ---")
    gen_script = ROOT / "04_GENERATORS" / "generate_carousel_production.py"
    prev_script = ROOT / "04_GENERATORS" / "make_generic_preview.py"
    
    for json_name, folder_name, prefix, title, subtitle in POSTS:
        json_path = IDEAS_DIR / json_name
        out_folder = OUTPUTS_DIR / folder_name
        app_folder = APPROVED_DIR / folder_name
        
        out_folder.mkdir(parents=True, exist_ok=True)
        app_folder.mkdir(parents=True, exist_ok=True)
        
        # 1. Render slides directly to JPEG
        subprocess.run([sys.executable, str(gen_script), str(json_path), str(out_folder), prefix], check=True)
        
        # 2. Render preview sheet directly to JPEG
        preview_file_out = out_folder / f"{prefix.upper()}_CAROUSEL_PREVIEW.jpg"
        subprocess.run([sys.executable, str(prev_script), str(out_folder), title, subtitle, str(preview_file_out), prefix], check=True)
        
        # 3. Copy JPEG files to APPROVED folder
        for f in out_folder.glob(f"{prefix}_*.jpg"):
            (app_folder / f.name).write_bytes(f.read_bytes())
        (app_folder / preview_file_out.name).write_bytes(preview_file_out.read_bytes())
        
        print(f"✓ {folder_name} successfully rendered & copied as JPEG.")

if __name__ == "__main__":
    clean_png_files()
    rerender_all_jpeg()
    print("\nAll posts successfully migrated to pure JPEG pipeline!")
