from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pathlib import Path

SRC = Path(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/naskah-visuals/official_logo_naskah.jpg")
OUT = Path(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/naskah-visuals/logo_cutouts")
OUT.mkdir(parents=True, exist_ok=True)

img = Image.open(SRC).convert("RGBA")
arr = np.array(img)

# The background is warm off-white / cream (around R:240-255, G:235-255, B:220-250)
# Let's inspect background color
bg_sample = arr[:30, :30, :3]
print("BG mean color:", np.mean(bg_sample, axis=(0,1)))

# Let's extract clean logo with alpha channel:
# If color is close to the cream background (e.g. brightness > 230 and saturation is low), make it transparent.
# Let's do a smooth alpha matte
r, g, b, a = arr[:,:,0], arr[:,:,1], arr[:,:,2], arr[:,:,3]
# Distance from cream background (#ECE8E1 approx)
bg_r, bg_g, bg_b = 239, 235, 227
dist = np.sqrt((r.astype(float)-bg_r)**2 + (g.astype(float)-bg_g)**2 + (b.astype(float)-bg_b)**2)

# Create alpha mask
alpha = np.clip((dist - 15) * 6, 0, 255).astype(np.uint8)

# The white inside the book pages should remain white/opaque!
# Book pages are bright white (R > 250, G > 250, B > 250)
# But wait, the original background is slightly textured cream (~235-240), inside book is pure white or cream.
# Let's check where the mark is centered.
# Let's crop tight to the emblem bounding box.
mask_pixels = dist > 35
ys, xs = np.where(mask_pixels)
min_y, max_y = np.min(ys), np.max(ys)
min_x, max_x = np.min(xs), np.max(xs)
print(f"BBox: ({min_x}, {min_y}) to ({max_x}, {max_y})")

cropped_img = img.crop((min_x - 10, min_y - 10, max_x + 10, max_y + 10))
cropped_img.save(OUT / "official_logo_cropped_raw.png")

# Also let's create a circular badge version and rounded squircle badge version that looks razor-sharp on ANY background (Cream, Navy, Orange)
badge_size = (300, 300)
# 1. Cream badge (for dark slides)
b_cream = Image.new("RGBA", badge_size, (0,0,0,0))
d_bc = ImageDraw.Draw(b_cream)
d_bc.rounded_rectangle((0,0,300,300), radius=60, fill="#F5F2EB")
scaled_logo = cropped_img.resize((240, int(240 * cropped_img.height / cropped_img.width)), Image.Resampling.LANCZOS)
b_cream.paste(scaled_logo, ((300-scaled_logo.width)//2, (300-scaled_logo.height)//2), scaled_logo if scaled_logo.mode=="RGBA" else None)
b_cream.save(OUT / "badge_cream_for_dark_bg.png")

# 2. Transparent / direct version for cream slides
# Since cream slides match the logo's native cream background, it blends seamlessly!
b_direct = cropped_img.resize((240, int(240 * cropped_img.height / cropped_img.width)), Image.Resampling.LANCZOS)
b_direct.save(OUT / "logo_direct_for_cream.png")

print("Logo cutouts and badges created.")
