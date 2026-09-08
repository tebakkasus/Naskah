"""Generate contact sheet for the high-density rich concepts."""
from pathlib import Path
from PIL import Image

BASE = Path(r"D:/tm/06_Content/05_OUTPUTS/concept_rich_density_2026")
OUT = BASE / "CONTACT_SHEET_RICH_DENSITY.jpg"
CELL = 540
SPACING = 24
PAD = 40

names = [
    "naskah_dense_01_dense_bento_cheatsheet.jpg",
    "naskah_dense_02_workflow_timeline_5hari.jpg",
    "naskah_dense_03_dark_comparison_or_rr_hr.jpg",
    "naskah_dense_04_editorial_anatomy_bab4_5.jpg",
]

cols, rows = 2, 2
sheet_w = PAD * 2 + cols * CELL + (cols - 1) * SPACING
sheet_h = PAD * 2 + rows * int(CELL * 1.25) + (rows - 1) * SPACING

contact = Image.new("RGB", (sheet_w, sheet_h), "#0E1117")

for idx, nm in enumerate(names):
    im = Image.open(BASE / nm)
    im = im.resize((CELL, int(CELL * im.height / im.width)), Image.Resampling.LANCZOS)
    c, r = idx % cols, idx // cols
    x = PAD + c * (CELL + SPACING)
    y = PAD + r * (int(CELL * 1.25) + SPACING)
    contact.paste(im, (x, y))

contact.save(OUT, "JPEG", quality=92)
print("SAVED CONTACT SHEET:", OUT)