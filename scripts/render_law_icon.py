"""Render the JB Law app icon — matches the JB Pharma / JB AI suite system.

Cream background (#F5EFE6), italic New York serif 'LAW' centered in deep
law-book green (#1F4D3A), italic 'JB' ink stamp top-left.

Output: Targets/Law/Resources/Assets.xcassets/AppIcon.appiconset/icon-1024.png
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

SIZE = 1024
BG = (245, 239, 230)            # #F5EFE6 warm paper
INK = (20, 24, 28)               # near-black for JB stamp
ACCENT = (31, 77, 58)            # #1F4D3A deep law-book green

NY_ITALIC = "/System/Library/Fonts/NewYorkItalic.ttf"

OUT = Path(__file__).parent.parent / "Targets" / "Law" / "Resources" / \
      "Assets.xcassets" / "AppIcon.appiconset" / "icon-1024.png"


def render():
    img = Image.new("RGB", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(img)

    # JB stamp — top-left, italic, smaller weight (~140pt-ish)
    jb_font = ImageFont.truetype(NY_ITALIC, 145)
    jb_text = "JB"
    jb_bbox = draw.textbbox((0, 0), jb_text, font=jb_font)
    jb_w = jb_bbox[2] - jb_bbox[0]
    # Anchor JB near top-left with small margin and slight offset to account
    # for italic forward lean.
    draw.text((85 - jb_bbox[0], 70 - jb_bbox[1]), jb_text, font=jb_font, fill=INK)

    # Centerpiece — "LAW" in italic New York, dark green, large.
    # Iteratively shrink so glyphs fit within a horizontal margin.
    # AI uses a tight 100px margin each side to push the glyphs large;
    # do the same here for visual parity within the family.
    main_text = "LAW"
    target_max_w = SIZE - 130
    main_size = 600
    while True:
        main_font = ImageFont.truetype(NY_ITALIC, main_size)
        main_bbox = draw.textbbox((0, 0), main_text, font=main_font)
        if (main_bbox[2] - main_bbox[0]) <= target_max_w or main_size < 200:
            break
        main_size -= 10
    main_w = main_bbox[2] - main_bbox[0]
    main_h = main_bbox[3] - main_bbox[1]

    # Center the LAW glyphs in the canvas. Anchor pushed slightly lower than
    # mathematical center for visual balance with JB top-left stamp.
    cx = (SIZE - main_w) / 2 - main_bbox[0]
    cy = (SIZE - main_h) / 2 - main_bbox[1] + 50
    draw.text((cx, cy), main_text, font=main_font, fill=ACCENT)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "PNG")
    print(f"Wrote {OUT} ({SIZE}x{SIZE})")


if __name__ == "__main__":
    render()
