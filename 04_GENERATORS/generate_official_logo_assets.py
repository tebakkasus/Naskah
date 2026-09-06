from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/naskah-visuals/official_logo_assets")
OUT.mkdir(parents=True, exist_ok=True)
SRC = Path(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/naskah-visuals/official_logo_naskah.jpg")
FONT_DIR = Path(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/fonts/Poppins")

# Open original logo
orig = Image.open(SRC).convert("RGBA")
W, H = orig.size

# We want to create clean transparent PNG crops of the mark
# Let's inspect / crop the central mark
# The image is square-ish. Let's make an avatar 1080x1080 and horizontal lockup 1200x400

# 1. Official Avatar (Square 1080x1080)
avatar = Image.new("RGB", (1080, 1080), "#F5F2EB")
logo_resized = orig.resize((760, 760), Image.Resampling.LANCZOS)
avatar.paste(logo_resized, ((1080-760)//2, (1080-760)//2))
avatar.save(OUT / "naskah_official_avatar_cream.png", quality=95)

# 2. Dark Navy Avatar
avatar_navy = Image.new("RGB", (1080, 1080), "#071726")
# For navy, we put the logo inside a clean rounded cream badge or as is
d_nav = ImageDraw.Draw(avatar_navy)
d_nav.rounded_rectangle((100, 100, 980, 980), radius=180, fill="#F5F2EB")
avatar_navy.paste(logo_resized, ((1080-760)//2, (1080-760)//2))
avatar_navy.save(OUT / "naskah_official_avatar_navy_badge.png", quality=95)

# 3. Horizontal Lockup: Logo Mark + "naskah.fk" Wordmark
lockup = Image.new("RGB", (1600, 500), "#F5F2EB")
d_lock = ImageDraw.Draw(lockup)
mark_small = orig.resize((320, 320), Image.Resampling.LANCZOS)
lockup.paste(mark_small, (120, 90))

f_brand = ImageFont.truetype(str(FONT_DIR / "Poppins-ExtraBold.ttf"), 96)
f_sub = ImageFont.truetype(str(FONT_DIR / "Poppins-Medium.ttf"), 38)

d_lock.text((490, 140), "naskah", font=f_brand, fill="#071726")
d_lock.text((490 + d_lock.textbbox((0,0), "naskah", font=f_brand)[2] + 4, 140), ".fk", font=f_brand, fill="#E85929")
d_lock.text((495, 270), "Teman Diskusi & Solusi Akademik", font=f_sub, fill="#4F5E6E")
lockup.save(OUT / "naskah_horizontal_lockup_cream.png", quality=95)

# 4. Horizontal Lockup Dark Navy
lockup_navy = Image.new("RGB", (1600, 500), "#071726")
d_lock_nav = ImageDraw.Draw(lockup_navy)
d_lock_nav.rounded_rectangle((100, 70, 440, 410), radius=50, fill="#F5F2EB")
lockup_navy.paste(orig.resize((280, 280), Image.Resampling.LANCZOS), (130, 100))

d_lock_nav.text((500, 140), "naskah", font=f_brand, fill="#F5F2EB")
d_lock_nav.text((500 + d_lock_nav.textbbox((0,0), "naskah", font=f_brand)[2] + 4, 140), ".fk", font=f_brand, fill="#E85929")
d_lock_nav.text((505, 270), "Teman Diskusi & Solusi Akademik", font=f_sub, fill="#9CA8B4")
lockup_navy.save(OUT / "naskah_horizontal_lockup_navy.png", quality=95)

print("Official logo assets prepared successfully.")
