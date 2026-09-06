"""
Create a CLEAN transparent logo mark from the official Naskah logo JPG.
Uses only stdlib + PIL + numpy (no scipy).
"""
from PIL import Image
import numpy as np
from collections import deque
from pathlib import Path

SRC = Path(r"D:/tm/06_Content/02_BRAND_ASSETS/logos/LOGO TERANG.jpg")
OUT_DIR = Path(r"D:/tm/06_Content/02_BRAND_ASSETS/logos/logo_cutouts_clean")
OUT_DIR.mkdir(parents=True, exist_ok=True)

img = Image.open(SRC).convert("RGB")
arr = np.array(img).astype(np.int32)
H, W, _ = arr.shape

# Sample perimeter band to find background color
perim = np.concatenate([
    arr[0, :, :], arr[-1, :, :], arr[:, 0, :], arr[:, -1, :]
], axis=0)
bg = np.median(perim, axis=0).astype(np.int32)
print("Background estimate:", bg)

# Tolerance for background distance
tol = 35

# BFS flood fill from all perimeter pixels
vis = np.zeros((H, W), dtype=bool)
q = deque()
seeds = []
for x in range(W):
    for y in [0, H - 1]:
        if np.linalg.norm(arr[y, x] - bg) < tol:
            seeds.append((y, x))
for y in range(H):
    for x in [0, W - 1]:
        if np.linalg.norm(arr[y, x] - bg) < tol:
            seeds.append((y, x))

for s in seeds:
    if not vis[s]:
        vis[s] = True
        q.append(s)
        while q:
            cy, cx = q.popleft()
            for dy, dx in ((-1,0),(1,0),(0,-1),(0,1)):
                ny, nx = cy+dy, cx+dx
                if 0 <= ny < H and 0 <= nx < W and not vis[ny, nx]:
                    if np.linalg.norm(arr[ny, nx] - bg) < tol:
                        vis[ny, nx] = True
                        q.append((ny, nx))

bg_mask = vis
fg_mask = ~bg_mask

# Build RGBA
rgba = np.dstack([arr, np.full((H, W), 255, dtype=np.uint8)])
rgba[bg_mask, 3] = 0

out = Image.fromarray(rgba.astype(np.uint8), "RGBA")

# Crop to tight bounding box of foreground
ys, xs = np.where(fg_mask)
min_y, max_y = int(ys.min()), int(ys.max())
min_x, max_x = int(xs.min()), int(xs.max())
out = out.crop((min_x, min_y, max_x + 1, max_y + 1))

out.save(OUT_DIR / "official_logo_transparent.png")
print("Transparent logo saved:", out.size)

# Create a white monochrome version for colored backgrounds
arr_rgba = np.array(out).astype(np.int32)
a = arr_rgba[:, :, 3]
alpha_mask = a > 30
arr_rgba[alpha_mask, 0:3] = 255
white = Image.fromarray(arr_rgba.astype(np.uint8), "RGBA")
white.save(OUT_DIR / "official_logo_white.png")
print("White logo version saved.")
