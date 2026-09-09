"""
Naskah Emoji Library Bulk Downloader (parallel).
Downloads the full Twemoji library used by Naskah content into
02_BRAND_ASSETS/emojis/ so future renders never need to fetch again.
"""
from __future__ import annotations

import json
import pathlib
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = pathlib.Path(r"D:/tm/06_Content")
EMOJI_DIR = BASE_DIR / "02_BRAND_ASSETS/emojis"
EMOJI_DIR.mkdir(parents=True, exist_ok=True)

CDN_TEMPLATES = [
    "https://cdn.jsdelivr.net/gh/realityripple/emoji@latest/twemoji/{codepoint}.png",
    "https://twemoji.maxcdn.com/v/14.0.2/72x72/{codepoint}.png",
]

# Full wishlist — academic, medical, productivity, UI, arrows, symbols, misc
WISHLIST = {
    "🎯": "1f3af", "📸": "1f4f8", "🔥": "1f525", "💛": "1f49b", "🌿": "1f33f",
    "📝": "1f4dd", "🔬": "1f52c", "✏️": "270f", "✏": "270f", "📚": "1f4da",
    "✅": "2705", "🔖": "1f516", "🌙": "1f319", "🏆": "1f3c6", "🫠": "1fae0",
    "🏥": "1f3e5", "🎬": "1f3ac", "🧰": "1f9f0", "🧵": "1f9f5", "⏭️": "23ed",
    "⚠️": "26a0", "🏢": "1f3e2", "💻": "1f4bb", "🧠": "1f9e0", "✍️": "270d",
    "⏰": "23f0", "📅": "1f4c5", "🎓": "1f393", "⭐": "2b50", "❌": "274c",
    "💾": "1f4be", "💬": "1f4ac", "💡": "1f4a1", "📌": "1f4cc", "👉": "1f449",
    "⚡": "26a1", "📊": "1f4ca", "🚫": "1f6ab",
    # stationery / documents
    "📎": "1f4ce", "📁": "1f4c1", "📂": "1f4c2", "📋": "1f4cb", "🗂️": "1f5c2",
    "🗒️": "1f5d2", "🗓️": "1f5c3", "🖇️": "1f587", "📏": "1f4cf", "📐": "1f4d0",
    "✂️": "2702", "🗑️": "1f5d1", "🖊️": "1f58a", "🖋️": "1f58b", "🖌️": "1f58c",
    "🪄": "1fa84", "🧮": "1f9ee", "🔍": "1f50d", "🔎": "1f50e", "🔗": "1f517",
    "🧷": "1f9f7", "📑": "1f4d1", "📄": "1f4c4", "📃": "1f4c3", "📜": "1f4dc",
    "📒": "1f4d2", "📓": "1f4d3", "📔": "1f4d4", "📕": "1f4d5", "📖": "1f4d6",
    "📗": "1f4d7", "📘": "1f4d8", "📙": "1f4d9", "📇": "1f4c7", "🗞️": "1f5de",
    "📰": "1f4f0", "📈": "1f4c8", "📉": "1f4c9", "💹": "1f4b9", "💯": "1f4af",
    # money / business
    "💰": "1f4b0", "💵": "1f4b5", "💴": "1f4b4", "💶": "1f4b6", "💷": "1f4b7",
    "🪙": "1fa99", "💳": "1f4b3", "🧾": "1f9fe", "🏷️": "1f3f7", "📦": "1f4e6",
    "🛒": "1f6d2", "🛍️": "1f6cd", "💼": "1f4bc", "🪪": "1faaa", "🗃️": "1f5c3",
    # medical / health
    "🩺": "1fa7a", "💊": "1f48a", "💉": "1f489", "🩸": "1fa78", "🧬": "1f9ec",
    "🧫": "1f9eb", "🧪": "1f9ea", "🦠": "1f9a0", "🩻": "1facb", "🦴": "1f9b4",
    "🫀": "1fac0", "🫁": "1fac1", "👁️": "1f441", "👀": "1f440", "🦷": "1f9b7",
    "🩹": "1fa79", "🩼": "1fa7c", "🦾": "1f9be", "🦿": "1f9bf", "🫃": "1fac3",
    "🫄": "1fac4", "👶": "1f476", "🧑": "1f9d1", "👨": "1f468", "👩": "1f469",
    "👨‍⚕️": "1f468-200d-2695-fe0f", "👩‍⚕️": "1f469-200d-2695-fe0f",
    "🧑‍⚕️": "1f9d1-200d-2695-fe0f", "🏨": "1f3e8", "🏫": "1f3eb", "🏛️": "1f3db",
    "🚑": "1f691", "🚨": "1f6a8", "🚗": "1f697",
    # academic extras
    "🔭": "1f52d", "🧲": "1f9f2", "🏅": "1f3c5", "🥇": "1f947", "🥈": "1f948",
    "🥉": "1f949", "🎖️": "1f396",
    # tech
    "🖱️": "1f5b1", "⌨️": "2328", "💽": "1f4bd", "💿": "1f4bf", "📀": "1f4c0",
    "📼": "1f4fc", "📷": "1f4f7", "📹": "1f4f9", "🎥": "1f3a5", "📺": "1f4fa",
    "📻": "1f4fb", "🎙️": "1f399", "🎚️": "1f39a", "🎛️": "1f39b", "🔋": "1f50b",
    "🔌": "1f50c", "🖨️": "1f5a8", "🖥️": "1f5a5", "📱": "1f4f1", "📲": "1f4f2",
    # light / sparkle
    "🔆": "1f506", "🔅": "1f505", "✨": "2728", "🌟": "1f31f", "💫": "1f4ab",
    "💥": "1f4a5", "🌈": "1f308", "🎨": "1f3a8", "🎭": "1f3ad", "🎤": "1f3a4",
    "🎧": "1f3a7", "🎼": "1f3bc", "🎵": "1f3b5", "🎶": "1f3b6", "🔔": "1f514",
    "🔕": "1f515",
    # arrows / nav
    "➡️": "27a1", "⬅️": "2b05", "⬆️": "2b06", "⬇️": "2b07", "↗️": "2197",
    "↘️": "2198", "↙️": "2199", "↖️": "2196", "↩️": "21a9", "↪️": "21aa",
    "🔃": "1f503", "🔄": "1f504", "🔝": "1f51d", "🔚": "1f51a", "🔙": "1f519",
    "🔛": "1f51b", "🔜": "1f51c", "❎": "274e", "❗": "2757", "❓": "2753",
    "‼️": "203c", "⁉️": "2049", "💢": "1f4a2",
    # checklist & status
    "☑️": "2611", "✔️": "2714", "✔": "2714", "✖️": "2716", "➕": "2795",
    "➖": "2796", "➗": "2797", "✳️": "2733", "✴️": "2734",
    # chat / social
    "💭": "1f4ad", "🗨️": "1f5e8", "🗯️": "1f5ef", "💌": "1f48c", "📨": "1f4e8",
    "📩": "1f4e9", "📧": "1f4e7", "📞": "1f4de", "☎️": "260e",
    # hands / faces (relatability)
    "👋": "1f44b", "🙌": "1f64c", "👏": "1f44f", "👍": "1f44d", "👎": "1f44e",
    "👌": "1f44c", "🤝": "1f91d", "✊": "270a", "✌️": "270c", "🤞": "1f91e",
    "🙏": "1f64f", "💪": "1f4aa", "🤲": "1f932", "🫶": "1faf6", "🤗": "1f917",
    "🤔": "1f914", "🤨": "1f928", "😅": "1f605", "😊": "1f60a", "🙂": "1f642",
    "😉": "1f609", "😌": "1f60c", "😴": "1f634", "🥱": "1f971", "🤯": "1f92f",
    "😱": "1f631", "😨": "1f628", "😰": "1f630", "🥺": "1f97a", "😭": "1f62d",
    "😢": "1f622", "😮": "1f62e", "😲": "1f632", "🫢": "1fae2", "🫣": "1fae3",
    "🤫": "1f92b", "🤭": "1f92d", "🤐": "1f910", "😶": "1f636", "😐": "1f610",
    "😑": "1f611", "🤓": "1f913", "🧐": "1f9d0", "🤪": "1f92a", "😜": "1f61c",
    "😂": "1f602", "🤣": "1f923", "😁": "1f601", "😎": "1f60e", "🥳": "1f973",
    "🎉": "1f389", "🎊": "1f38a", "🎈": "1f388", "🎁": "1f381",
    # nature
    "🐒": "1f412", "🐵": "1f435", "🐶": "1f436", "🐱": "1f431", "🐭": "1f42d",
    "🐹": "1f439", "🐰": "1f430", "🦊": "1f98a", "🐻": "1f43b", "🐼": "1f43c",
    "🐨": "1f428", "🐯": "1f42f", "🦁": "1f981", "🐮": "1f42e", "🐷": "1f437",
    "🐸": "1f438", "🐙": "1f419", "🦋": "1f98b", "🐛": "1f41b", "🪲": "1fab2",
    "🐢": "1f422", "🐍": "1f40d", "🦎": "1f98e", "🦈": "1f988", "🐬": "1f42c",
    "🐳": "1f433", "🐊": "1f40a", "🦅": "1f985", "🦉": "1f989", "🦆": "1f986",
    "🐝": "1f41d", "🐞": "1f41e", "🌱": "1f331", "🍀": "1f340", "🌵": "1f335",
    "🌴": "1f334", "🌳": "1f332", "🌻": "1f33b", "🌼": "1f33c", "🌸": "1f338",
    "🌺": "1f33a", "☀️": "2600", "☁️": "2601", "⛅": "26c5", "🌧️": "1f327",
    "💧": "1f4a7", "🌊": "1f30a", "❄️": "2744",
    # food / coffee
    "☕": "2615", "🍵": "1f375", "🧋": "1f9cb", "🥤": "1f964", "🍽️": "1f37d",
    "🍕": "1f355", "🍔": "1f354", "🍟": "1f35f", "🍜": "1f35c", "🍝": "1f35d",
    "🍎": "1f34e", "🍊": "1f34a", "🍋": "1f34b", "🍌": "1f34c", "🍉": "1f349",
    "🍇": "1f347", "🍓": "1f353", "🍫": "1f36b", "🍪": "1f36a", "🧁": "1f9c1",
    "🎂": "1f382", "🍰": "1f370", "🥂": "1f942", "🍻": "1f37b",
    # transport / places
    "🚀": "1f680", "🛰️": "1f6f0", "✈️": "2708", "🚁": "1f681", "🚂": "1f682",
    "🚃": "1f683", "🚄": "1f684", "🚅": "1f685", "🚇": "1f687", "🚉": "1f689",
    "🚌": "1f68c", "🚎": "1f68e", "🏎️": "1f3ce", "🚓": "1f693", "🚕": "1f695",
    "🚙": "1f699", "🚚": "1f69a", "🚛": "1f69b", "🏠": "1f3e0", "🏡": "1f3e1",
    "🏬": "1f3ec", "🏣": "1f3e3", "🏤": "1f3e4", "🏦": "1f3e6", "🏪": "1f3ea",
    "⛪": "26ea", "🎪": "1f3aa", "🎢": "1f3a2", "🎡": "1f3a1",
}


def download_one(cp: str) -> tuple[str, bool]:
    local = EMOJI_DIR / f"{cp}.png"
    if local.exists() and local.stat().st_size > 500:
        return cp, True  # already have
    for template in CDN_TEMPLATES:
        url = template.format(codepoint=cp)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "NaskahSocialOS/1.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = resp.read()
            if len(data) > 500:
                local.write_bytes(data)
                return cp, True
        except Exception:
            continue
    return cp, False


def main() -> int:
    jobs = list(WISHLIST.values())
    # Dedupe preserving order
    seen = set()
    jobs = [j for j in jobs if not (j in seen or seen.add(j))]

    ok, fail = 0, 0
    failed_list = []
    with ThreadPoolExecutor(max_workers=16) as ex:
        futs = {ex.submit(download_one, cp): cp for cp in jobs}
        for fut in as_completed(futs):
            cp, success = fut.result()
            if success:
                ok += 1
            else:
                fail += 1
                failed_list.append(cp)

    print(f"TOTAL: {len(jobs)} | OK: {ok} | FAIL: {fail}")
    if failed_list:
        print("FAILED:", ",".join(failed_list))
    return 0


if __name__ == "__main__":
    sys.exit(main())