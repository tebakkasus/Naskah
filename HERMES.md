# CONTENT DEPARTMENT — OPERATIONAL FRAMEWORK

## MISSION & OBJECTIVE
Menjalankan eksekusi konten Naskah Social OS: dari strategi, visual branding, copywriting, carousel design, sampai scheduling dan analytics konten Instagram/Threads untuk brand @naskah.fk.

Semua aset kreatif, strategi, brand guideline, Python generator, dan pipeline editorial harus berpusat di dalam departemen ini (`D:/tm/content`).

---

## SYSTEM DIRECTORY STRUCTURE
```text
D:\tm\content\
├── HERMES.md                      # Master Department Guidelines
├── SOUL.md                        # Naskah Social OS Persona & Constitution
├── AGENTS.md                      # Agent Instruction Context
├── README.md                      # Department Overview & Pipeline Flow
│
├── 01_STRATEGY/                   # Social OS Strategy & Archetype Documents
│   ├── NASKAH_SOCIAL_OS_SOUL_v1.0.md
│   └── NASKAH_SOCIAL_STRATEGY_v1.0.md
│
├── 02_BRAND_ASSETS/               # Logos, Badges, Cutouts, Typography
│   ├── logos/
│   └── fonts/
│
├── 03_DESIGN_SYSTEM/              # Visual Rulebook, Carousel Templates, Style Specs
│   ├── NASKAH_DESIGN_SYSTEM_v1.0.md
│   ├── NASKAH_CAROUSEL_TEMPLATE_LOCKED_V2.md
│   └── canva-baseline-navy.json
│
├── 04_GENERATORS/                 # Python rendering engines (Pillow, Matplotlib, etc.)
│   └── generate_*.py
│
├── 05_OUTPUTS/                    # Generated renders, carousels, concept variations
│   ├── concept_*.jpg
│   ├── test_carousel_v*/...
│
├── 06_CONTENT_PIPELINE/           # Editorial workflow & scheduling targets
│   ├── 01_IDEAS/
│   ├── 02_DRAFTS/
│   ├── 03_APPROVED/
│   └── 04_PUBLISHED/
│
├── SKILLS/                        # Content-specific agent skills (e.g. social design)
│   └── social-media-visual-design/
│
└── CONFIG_BACKUP/                 # Reference config & memory backup
```

---

## OPERATING RULES
1. Semua eksekusi visual, rendering carousel, dan pembuatan konten harus berbasis file di dalam departemen ini.
2. Python generator (`04_GENERATORS/`) harus selalu merujuk aset dari `02_BRAND_ASSETS/` dan rules dari `03_DESIGN_SYSTEM/`.
3. Output yang di-generate harus disimpan ke `05_OUTPUTS/` atau langsung ke pipeline `06_CONTENT_PIPELINE/03_APPROVED/` jika sudah final.
4. Tidak boleh membuat aset visual atau konten di luar departemen ini atau di root profile Hermes.
5. Ikuti `SOUL.md` dan `AGENTS.md` untuk menentukan gaya bahasa, tone, dan visual identity brand Naskah.

---

## ACCESS & LAUNCH
Jalankan departemen ini dengan Hermes Profile Content:
```bash
hermes --profile content
```
Terminal working directory sudah otomatis mengarah ke `D:/tm/content`.
