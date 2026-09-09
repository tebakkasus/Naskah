"""
Naskah Emoji Asset Helper — download & paste emoji PNG onto renders.

Loads Twemoji-style PNGs from 02_BRAND_ASSETS/emojis/ (350+ library assets)
and pastes them as raster images on the canvas at requested position/size.

Never renders tofu (missing glyphs).
"""
from __future__ import annotations

import json
import pathlib
import urllib.request
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = pathlib.Path(r"D:/tm/06_Content")
EMOJI_DIR = BASE_DIR / "02_BRAND_ASSETS/emojis"
EMOJI_MAP_FILE = EMOJI_DIR / "emojis.json"

# Extensive codepoint mapping (300+ items)
from download_emoji_library import WISHLIST as EMOJI_CODEPOINTS

CDN_TEMPLATES = [
    "https://cdn.jsdelivr.net/gh/realityripple/emoji@latest/twemoji/{codepoint}.png",
    "https://twemoji.maxcdn.com/v/14.0.2/72x72/{codepoint}.png",
]


def _ensure_emoji_map():
    if not EMOJI_MAP_FILE.exists():
        EMOJI_MAP_FILE.write_text(json.dumps(EMOJI_CODEPOINTS, ensure_ascii=False, indent=2), encoding="utf-8")


def get_emoji_path(char: str) -> pathlib.Path | None:
    """Return local path for an emoji, downloading on demand if missing."""
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
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
            if len(data) > 500:
                local.write_bytes(data)
                return local
        except Exception:
            continue
    return None


def paste_emoji(im: Image.Image, char: str, xy: tuple[float, float], size: int,
                anchor: str = "la", fallback: str = "●") -> tuple[int, int] | None:
    """
    Paste an emoji PNG onto image at xy with given size.
    anchor: 'la', 'mm' (middle-middle), 'top_left', 'ra'.
    Fallback: if PNG missing, draw a small branded dot instead of tofu.
    """
    path = get_emoji_path(char)
    x, y = xy
    if path and path.exists():
        try:
            emoji = Image.open(path).convert("RGBA").resize((size, size), Image.Resampling.LANCZOS)
            w, h = emoji.size
            if anchor == "mm":
                px, py = int(x - w / 2), int(y - h / 2)
            elif anchor in ("la", "top_left"):
                px, py = int(x), int(y)
            elif anchor == "ra":
                px, py = int(x - w), int(y)
            else:
                px, py = int(x), int(y)
            im.paste(emoji, (px, py), emoji)
            return (w, h)
        except Exception as exc:
            print(f"[emoji] Paste failed for {char}: {exc}")

    # Fallback: small branded dot (never tofu)
    d = ImageDraw.Draw(im)
    r = size * 0.28
    if anchor == "mm":
        cx, cy = x, y
    else:
        cy = y + size * 0.5
        cx = x + size * 0.5
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill="#E85929")
    return (int(r * 2), int(r * 2))


def paste_emoji_with_text(im: Image.Image, char: str, xy: tuple[float, float],
                          text: str, font: ImageFont.FreeTypeFont, fill: str,
                          emoji_size: int = None, spacing: int = 12) -> tuple[int, int]:
    """
    Draw an emoji followed by text, perfectly aligned vertically (center-to-center).
    """
    x, y = xy
    d = ImageDraw.Draw(im)
    bb = d.textbbox((0, 0), text, font=font)
    text_w = bb[2] - bb[0]
    text_h = bb[3] - bb[1]

    if emoji_size is None:
        emoji_size = int(font.size * 0.95)

    text_mid_y = y + text_h / 2
    emoji_y = int(text_mid_y - emoji_size / 2)

    paste_emoji(im, char, (x, emoji_y), size=emoji_size, anchor="top_left")

    text_x = x + emoji_size + spacing
    d.text((text_x, y), text, font=font, fill=fill)

    return (emoji_size + spacing + text_w, max(text_h, emoji_size))


# Broad Unicode emoji range
_EMOJI_REGEX = None

def _get_emoji_regex():
    global _EMOJI_REGEX
    if _EMOJI_REGEX is None:
        import re
        _EMOJI_REGEX = re.compile(
            "["
            "\U0001F000-\U0001FAFF"
            "\U0001F900-\U0001F9FF"
            "\U00002600-\U000027BF"
            "\U00002B00-\U00002BFF"
            "\U0000FE00-\U0000FE0F"
            "\U0001F1E6-\U0001F1FF"
            "\u200d"
            "\u20e3"
            "\ufe0f"
            "]+"
        )
    return _EMOJI_REGEX


def strip_all_emojis(text: str) -> str:
    """Strip every emoji/symbol glyph from text (universal, no map needed)."""
    return _get_emoji_regex().sub("", text)