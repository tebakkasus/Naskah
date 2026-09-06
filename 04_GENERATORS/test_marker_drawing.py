import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def draw_marker_pill_oval(draw, text_origin, text_str, font_obj, color="#E85929", pad_x=40, pad_y=22, stroke=8):
    """
    Draws a hand-drawn organic marker capsule around a wide text line.
    Uses two horizontal sweeping strokes (top and bottom) connected by rounded end arcs,
    ensuring the stroke NEVER cuts into the text regardless of width.
    """
    tx, ty = text_origin
    box = draw.textbbox((tx, ty), text_str, font=font_obj)
    x1 = box[0] - pad_x
    y1 = box[1] - pad_y
    x2 = box[2] + pad_x
    y2 = box[3] + pad_y + 4
    
    r = (y2 - y1) / 2.0  # radius for end caps
    
    # Left cap arc center: (x1 + r, (y1+y2)/2)
    # Right cap arc center: (x2 - r, (y1+y2)/2)
    # If text is wide, x2 - r > x1 + r
    
    # Draw top stroke (slightly curved)
    top_pts = [(x1 + r * 0.4, y1 + 4), (tx + (box[2]-box[0])*0.5, y1), (x2 - r * 0.3, y1 + 3)]
    draw.line(top_pts, fill=color, width=stroke, joint="curve")
    
    # Draw right cap arc
    right_bbox = (x2 - 2*r, y1, x2, y2)
    draw.arc(right_bbox, start=270, end=90, fill=color, width=stroke)
    
    # Draw bottom stroke (slightly curved)
    bot_pts = [(x2 - r * 0.4, y2), (tx + (box[2]-box[0])*0.5, y2 + 3), (x1 + r * 0.3, y2 - 2)]
    draw.line(bot_pts, fill=color, width=stroke, joint="curve")
    
    # Draw left cap arc
    left_bbox = (x1, y1, x1 + 2*r, y2)
    draw.arc(left_bbox, start=90, end=270, fill=color, width=stroke)
    
    # Add an organic overlapping tail on the bottom-right
    tail_pts = [(x2 - r*0.5, y2 + 2), (x2 + 10, y2 - 8)]
    draw.line(tail_pts, fill=color, width=stroke - 2)

# Test render
FONT_DIR = Path(r"D:/tm/06_Content/02_BRAND_ASSETS/fonts/Poppins")
f = ImageFont.truetype(str(FONT_DIR / "Poppins-ExtraBold.ttf"), 90)
im = Image.new("RGB", (1080, 500), "#F5F2EB")
d = ImageDraw.Draw(im)
pos = (90, 200)
d.text(pos, "FATAL SITASI", font=f, fill="#0B131D")
draw_marker_pill_oval(d, pos, "FATAL SITASI", f, color="#E85929", pad_x=45, pad_y=20, stroke=8)
im.save(r"D:/tm/06_Content/05_OUTPUTS/test_marker_pill.png")
print("Saved marker test.")
