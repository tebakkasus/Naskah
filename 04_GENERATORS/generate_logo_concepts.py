from PIL import Image, ImageDraw
from pathlib import Path
import math

OUT = Path(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/naskah-visuals/logo_concepts")
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1000, 1000

NAVY = "#071726"
CREAM = "#F5F2EB"
ORANGE = "#E85929"
WHITE = "#FFFFFF"

# CONCEPT 1: "The Academic Ribbon / Bookmark N"
# N shaped with clean editorial diagonal fold, bookmark-cut bottom on the right stem
def draw_concept_1(bg_color, mark_color, accent_color, name):
    im = Image.new("RGBA", (W, H), bg_color)
    d = ImageDraw.Draw(im)
    
    # Grid center: cx=500, cy=500
    # Left stem: rounded thick vertical bar
    # Diagonal: connecting top-left to bottom-right with dynamic optical thickness
    # Right stem: with subtle bookmark notch / sharp editorial angle
    
    # Stem dimensions
    sw = 88 # stem width
    top = 220
    bot = 780
    lx = 270 # left stem x
    rx = 642 # right stem x
    
    # Left vertical stem
    d.rounded_rectangle((lx, top, lx+sw, bot), radius=sw//2, fill=mark_color)
    
    # Diagonal bar (connecting left top to right bottom)
    # Polygon points with smoothed ends
    diag_pts = [
        (lx + sw - 10, top + 15),
        (lx + sw + 50, top + 15),
        (rx + 10, bot - 15),
        (rx - 50, bot - 15)
    ]
    d.polygon(diag_pts, fill=accent_color)
    
    # Right vertical stem with ribbon bookmark cut at bottom
    # Points for right stem
    r_pts = [
        (rx, top + sw//2),
        (rx + sw//2, top),
        (rx + sw, top + sw//2),
        (rx + sw, bot),
        (rx + sw//2, bot - 45), # bookmark notch cut
        (rx, bot)
    ]
    d.polygon(r_pts, fill=mark_color)
    # top round cap for right stem
    d.ellipse((rx, top, rx+sw, top+sw), fill=mark_color)
    
    im.convert("RGB").save(OUT / f"logo_c1_bookmark_{name}.png")

# CONCEPT 2: "The Monolith Arch N (Geometric & Modern Minimalist)"
# 2 clean vertical pills + 1 dynamic diagonal slash floating with negative space (super memorable, like Linear/Vercel standard)
def draw_concept_2(bg_color, mark_color, accent_color, name):
    im = Image.new("RGBA", (W, H), bg_color)
    d = ImageDraw.Draw(im)
    
    # 2 vertical pillars + 1 sleek diagonal block that intersects with optical precision
    top = 220
    bot = 780
    sw = 96
    lx = 260
    rx = 644
    
    # Left Pill
    d.rounded_rectangle((lx, top, lx+sw, bot), radius=sw//2, fill=mark_color)
    
    # Right Pill
    d.rounded_rectangle((rx, top, rx+sw, bot), radius=sw//2, fill=mark_color)
    
    # Dynamic central slash bridging both pillars with an offset angle and bold accent dot/cut
    diag = [
        (lx + sw - 5, top + 70),
        (lx + sw + 65, top + 70),
        (rx + 5, bot - 70),
        (rx - 65, bot - 70)
    ]
    d.polygon(diag, fill=accent_color)
    
    # Circular emblem point on top right
    dot_r = 30
    d.ellipse((rx + sw/2 - dot_r, top - 65, rx + sw/2 + dot_r, top - 65 + dot_r*2), fill=accent_color)
    
    im.convert("RGB").save(OUT / f"logo_c2_monolith_{name}.png")

# CONCEPT 3: "The Continuous Ribbon / Fold N"
# Single ribbon folded in space creating N, rounded modern apexes, extremely distinct shape
def draw_concept_3(bg_color, mark_color, accent_color, name):
    im = Image.new("RGBA", (W, H), bg_color)
    d = ImageDraw.Draw(im)
    
    # 3 interlocking bold strokes forming a continuous optical ribbon
    # Left vertical
    d.rounded_rectangle((280, 240, 370, 760), radius=45, fill=mark_color)
    
    # Right vertical
    d.rounded_rectangle((630, 240, 720, 760), radius=45, fill=mark_color)
    
    # Diagonal connection with high-contrast accent color
    diag = [
        (340, 245),
        (425, 245),
        (660, 755),
        (575, 755)
    ]
    d.polygon(diag, fill=accent_color)
    
    # Optical bridge smooth joints
    d.ellipse((325, 240, 415, 330), fill=accent_color)
    d.ellipse((585, 670, 675, 760), fill=accent_color)
    
    im.convert("RGB").save(OUT / f"logo_c3_ribbon_{name}.png")

# CONCEPT 4: "The Pen & Page N (Negative Space & Research Angle)"
# Solid block N where the diagonal is a sharp angled negative space or stylus cut
def draw_concept_4(bg_color, mark_color, accent_color, name):
    im = Image.new("RGBA", (W, H), bg_color)
    d = ImageDraw.Draw(im)
    
    # Heavy bold architectural N with angled stylus tip at top-right
    top = 220
    bot = 780
    left = 250
    right = 750
    sw = 110 # stroke width
    
    # Left upright
    d.rounded_rectangle((left, top, left+sw, bot), radius=35, fill=mark_color)
    
    # Diagonal
    diag_pts = [
        (left + sw - 15, top),
        (left + sw + 65, top),
        (right, bot),
        (right - sw + 15, bot)
    ]
    d.polygon(diag_pts, fill=mark_color)
    
    # Right upright
    d.rounded_rectangle((right-sw, top, right, bot), radius=35, fill=mark_color)
    
    # Stylus nib / Spark highlight on the upper right intersection
    spark_cx = right - sw/2
    spark_cy = top + 55
    d.ellipse((spark_cx - 26, spark_cy - 26, spark_cx + 26, spark_cy + 26), fill=accent_color)
    
    im.convert("RGB").save(OUT / f"logo_c4_bold_{name}.png")

# Render variations on Navy and Cream
for bg, mark, acc, name in [
    (NAVY, CREAM, ORANGE, "navy"),
    (CREAM, NAVY, ORANGE, "cream")
]:
    draw_concept_1(bg, mark, acc, name)
    draw_concept_2(bg, mark, acc, name)
    draw_concept_3(bg, mark, acc, name)
    draw_concept_4(bg, mark, acc, name)

print("Generated 8 logo files.")
