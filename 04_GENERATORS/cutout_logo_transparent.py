from PIL import Image
import numpy as np
from pathlib import Path

SRC = Path(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/naskah-visuals/official_logo_naskah.jpg")
OUT_DIR = Path(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/naskah-visuals/logo_cutouts")
OUT_DIR.mkdir(parents=True, exist_ok=True)

img = Image.open(SRC).convert("RGBA")
arr = np.array(img).astype(np.float32)
r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
a = arr[:,:,3]

# Background is warm cream (#F0EAE0-ish). Sample corner
print("Top-left corner:", img.getpixel((5,5)))
print("Top-right corner:", img.getpixel((img.width-6,5)))
print("Center bg sample:", img.getpixel((1024, 60)))

# Distance to cream background
bg_r, bg_g, bg_b = 240, 235, 226
dist = np.sqrt((r-bg_r)**2 + (g-bg_g)**2 + (b-bg_b)**2)

# The logo interior has white fills we must KEEP opaque
# White fills are very close to pure white (245-255) AND dist small; but they are NOT the background.
# The issue: pure white fills vs cream background distinction.
# Better approach: detect the background as the large contiguous cream field via flood from corners.
# Simple: alpha = 0 where pixel is near cream background, else 255 where it's logo (blue/mint/dark).
# Pure white internal fills need to stay white (255 alpha).

# Approximate background mask: cream = warm (r>230) low saturation
# Compute a "creaminess": warm background tends r>g>b and fairly light
r_n, g_n, b_n = r/255.0, g/255.0, b/255.0
mx = np.maximum(r_n, np.maximum(g_n, b_n))
mn = np.minimum(r_n, np.minimum(g_n, b_n))
sat = np.where(mx>1e-6, (mx-mn)/np.maximum(mx,1e-6), 0)
light = mx

cream_bg = (sat < 0.06) & (light > 0.90)  # near-white, desaturated -> background cream
print("cream bg pixels:", int(cream_bg.sum()), "of", cream_bg.size)

alpha = np.where(cream_bg, 0, 255).astype(np.uint8)

# Also feather edges slightly to avoid halos
from PIL import ImageFilter
new_arr = np.dstack([arr[:,:,0].astype(np.uint8), arr[:,:,1].astype(np.uint8), arr[:,:,2].astype(np.uint8), alpha])
out = Image.fromarray(new_arr, "RGBA")

# Crop to bbox of content
mask = alpha > 30
ys, xs = np.where(mask)
min_y, max_y = np.min(ys), np.max(ys)
min_x, max_x = np.min(xs), np.max(xs)
out = out.crop((min_x, min_y, max_x, max_y))

out.save(OUT_DIR / "official_logo_transparent.png")
print("Saved transparent logo. Size:", out.size)
