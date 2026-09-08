"""Generate a contact sheet (one canvas, 2x2 grid) of the 2026 concept renders."""
from pathlib import Path
from PIL import Image

BASE = Path(r"D:/tm/06_Content/05_OUTPUTS/concept_upgrade_2026")
OUT = BASE / "CONTACT_SHEET_ALL.jpg"
CELL = 540
SPACING = 24
PAD = 40

names = [
    "naskah_concept_01_cover_gradient.jpg",
    "naskah_concept_02_bento_grid.jpg",
    "naskah_concept_03_glass_panel.jpg",
    "naskah_concept_04_marker_gradient_footer.jpg",
]

cols, rows = 2, 2
sheet_w = PAD * 2 + cols * CELL + (cols - 1) * SPACING
sheet_h = PAD * 2 + rows * CELL + (rows - 1) * SPACING

contact = Image.new("RGB", (sheet_w, sheet_h), "#17181B")

for idx, nm in enumerate(names):
    im = Image.open(BASE / nm)
    im = im.resize((CELL, int(CELL * im.height / im.width)), Image.Resampling.LANCZOS)
    c, r = idx % cols, idx // cols
    x = PAD + c * (CELL + SPACING)
    y = PAD + r * (int(CELL * 1.25) + SPACING)
    contact.paste(im, (x, y))

contact.save(OUT, "JPEG", quality=90)
print("CONTACT SHEET:", OUT)