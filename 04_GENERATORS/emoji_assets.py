"""
Naskah Emoji Asset Helper — download & paste emoji PNG onto renders.

Why: Pillow cannot render color emoji from Poppins (they show as tofu/missing glyph).
Download official Twemoji-style PNGs into 02_BRAND_ASSETS/emojis/ and paste them
as raster images onto the canvas at the requested position/size.

If an emoji PNG is missing, fall back safely to a small branded dot/star so we
NEVER render tofu (missing glyph) again.
"""
from __future__ import annotations

import json
import pathlib
import urllib.request
from PIL import Image, ImageDraw

BASE_DIR = pathlib.Path(r"D:/tm/06_Content")
EMOJI_DIR = BASE_DIR / "02_BRAND_ASSETS/emojis"
EMOJI_MAP_FILE = EMOJI_DIR / "emojis.json"

# Known emoji codepoints used by Naskah content
EMOJI_CODEPOINTS = {
    "🎯": "1f3af",
    "📸": "1f4f8",
    "🔥": "1f525",
    "💛": "1f49b",
    "🏆": "1f3c6",
    "🫠": "1fae0",
    "🏥": "1f3e5",
    "🎬": "1f3ac",
    "🧰": "1f9f0",
    "🧵": "1f9f5",
    "⏭️": "23ed",
    "⚠️": "26a0",
    "🏢": "1f3e2",
    "💻": "1f4bb",
    "📚": "1f4da",
    "🧠": "1f9e0",
    "✍️": "270d",
    "⏰": "23f0",
    "📅": "1f4c5",
    "🎓": "1f393",
    "⭐": "2b50",
    "✅": "2705",
    "❌": "274c",
    "💾": "1f4be",
    "💬": "1f4ac",
}

CDN_TEMPLATES = [
    "https://cdn.jsdelivr.net/gh/realityripple/emoji@latest/twemoji/{codepoint}.png",
    "https://twemoji.maxcdn.com/v/14.0.2/72x72/{codepoint}.png",
]


def _ensure_emoji_map():
    if not EMOJI_MAP_FILE.exists():
        EMOJI_MAP_FILE.write_text(json.dumps(EMOJI_CODEPOINTS, ensure_ascii=False, indent=2), encoding="utf-8")


def get_emoji_path(char: str) -> pathlib.Path | None:
    """Return local path for an emoji, downloading it if missing."""
    if not char or char not in EMOJI_CODEPOINTS:
        return None
    cp = EMOJI_CODEPOINTS[char]
    local = EMOJI_DIR / f"{cp}.png"
    if local.exists():
        return local
    EMOJI_DIR.mkdir(parents=True, exist_ok=True)
    _ensure_emoji_map()
    for template in CDN_TEMPLATES:
        url = template.format(codepoint=cp)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "NaskahSocialOS/1.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = resp.read()
            if len(data) > 500:
                local.write_bytes(data)
                print(f"[emoji] Downloaded {char} -> {local.name}")
                return local
        except Exception as exc:
            print(f"[emoji] Download failed for {char} via {url}: {exc}")
    return None


def paste_emoji(im: Image.Image, char: str, xy: tuple[float, float], size: int,
                anchor: str = "la", fallback: str = "●") -> tuple[int, int] | None:
    """
    Paste an emoji PNG onto image at xy with given size.
    anchor: 'la' = left-ascender (like text anchor), 'mm' = middle-middle.
    Fallback: if PNG missing, draw a small branded dot instead of tofu.
    Returns pasted (width, height) extent, or None if nothing drawn.
    """
    path = get_emoji_path(char)
    x, y = xy
    if path and path.exists():
        try:
            emoji = Image.open(path).convert("RGBA").resize((size, size), Image.Resampling.LANCZOS)
            w, h = emoji.size
            if anchor == "mm":
                px, py = int(x - w / 2), int(y - h / 2)
            elif anchor == "la":
                px, py = int(x), int(y - h * 0.82)
            elif anchor == "ra":
                px, py = int(x - w), int(y - h * 0.82)
            else:
                px, py = int(x), int(y)
            im.paste(emoji, (px, py), emoji)
            return (w, h)
        except Exception as exc:
            print(f"[emoji] Paste failed for {char}: {exc}")
    # Fallback: branded dot (never tofu)
    d = ImageDraw.Draw(im)
    r = size * 0.28
    cx, cy = x, y
    if anchor == "mm":
        pass
    elif anchor == "la":
        cy = y - size * 0.4
    else:
        cy = y - size * 0.4
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill="#E85929")
    return (int(r * 2), int(r * 2))


def strip_emojis(text: str) -> str:
    """Remove emoji chars from a text string (for font-only renders)."""
    return "".join(ch for ch in text if ch not in EMOJI_CODEPOINTS)