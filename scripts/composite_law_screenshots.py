"""Composite iPhone 17 Pro Max screenshots onto Apple's required canvas sizes.

Mirrors the JB Pharma flow: scale-to-fit + cream pillaring rather than
re-shooting on each simulator.

Inputs:  docs/screenshots/iphone-17-pro-max/NN_*.png   (1320×2868 native)
Outputs: docs/screenshots/iphone-6.5/NN_*.png         (1284×2778, Apple 6.5" req)
         docs/screenshots/ipad-13/NN_*.png            (2064×2752, Apple 13" iPad req)
"""
from PIL import Image
from pathlib import Path

ROOT = Path(__file__).parent.parent
SRC = ROOT / "docs" / "screenshots" / "iphone-17-pro-max"

CREAM = (245, 239, 230)  # #F5EFE6

# Apple's required dimensions
TARGETS = {
    "iphone-6.5": (1284, 2778),   # iPhone 6.5" display
    "ipad-13":    (2064, 2752),   # iPad Pro 13" (M4)
}


def fit_with_pillar(src_img: Image.Image, target_w: int, target_h: int,
                    pad_pct: float = 0.0) -> Image.Image:
    """Scale src to fit inside target while preserving aspect, then composite
    centred on a cream background.

    pad_pct: extra cream margin around the image (0.0 = fill, 0.05 = 5% padding).
    """
    canvas = Image.new("RGB", (target_w, target_h), CREAM)
    sw, sh = src_img.size

    avail_w = target_w * (1 - 2 * pad_pct)
    avail_h = target_h * (1 - 2 * pad_pct)

    # Scale to fit
    scale = min(avail_w / sw, avail_h / sh)
    nw, nh = int(sw * scale), int(sh * scale)
    scaled = src_img.resize((nw, nh), Image.LANCZOS)

    # Centre
    ox = (target_w - nw) // 2
    oy = (target_h - nh) // 2
    canvas.paste(scaled, (ox, oy))
    return canvas


def main():
    src_files = sorted(SRC.glob("*.png"))
    if not src_files:
        print(f"No source screenshots in {SRC}")
        return

    print(f"Source: {len(src_files)} file(s) from {SRC.name}")

    for label, (tw, th) in TARGETS.items():
        out_dir = ROOT / "docs" / "screenshots" / label
        out_dir.mkdir(parents=True, exist_ok=True)
        # iPad needs more pillaring because aspect ratio is wider; iPhone
        # 6.5" is essentially the same aspect so no padding needed.
        pad = 0.04 if label.startswith("ipad") else 0.0
        for src in src_files:
            img = Image.open(src)
            composed = fit_with_pillar(img, tw, th, pad_pct=pad)
            dest = out_dir / src.name
            composed.save(dest, "PNG", optimize=True)
            print(f"  {label}: {src.name} -> {tw}x{th}")


if __name__ == "__main__":
    main()
