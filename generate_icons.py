"""Generate NovaMP icons for Windows (PNGs + ICO)."""
import os
from PIL import Image, ImageDraw, ImageFont

ICONS_DIR = os.path.join(os.path.dirname(__file__), "src-tauri", "icons")

BG       = (26, 0, 64, 255)    # #1a0040
RING1    = (45, 0, 128, 255)   # #2d0080
RING2    = (74, 66, 204, 255)  # #4a42cc
RING3    = (108, 99, 255, 255) # #6c63ff
WHITE    = (255, 255, 255, 255)
RED_G    = (255, 60, 60, 160)  # glitch red
CYAN_G   = (0, 240, 255, 160)  # glitch cyan

# Helvetica Bold on macOS; falls back to Pillow default elsewhere
_FONT_CANDIDATES = [
    ("/System/Library/Fonts/Helvetica.ttc", 1),
    ("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 0),
]


def load_font(size):
    for path, index in _FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size, index=index)
        except Exception:
            pass
    return ImageFont.load_default()


def draw_icon(size):
    img  = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    def rect(margin_ratio, color):
        m = int(size * margin_ratio)
        draw.rectangle([m, m, size - 1 - m, size - 1 - m], fill=color)

    rect(0.00, BG)
    rect(0.09, RING1)
    rect(0.17, RING2)
    rect(0.25, RING3)

    font   = load_font(int(size * 0.58))
    bb     = draw.textbbox((0, 0), "N", font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    cx     = (size - tw) // 2 - bb[0]
    cy     = (size - th) // 2 - bb[1]
    glitch = max(1, size // 90)

    draw.text((cx - glitch, cy), "N", font=font, fill=RED_G)
    draw.text((cx + glitch, cy), "N", font=font, fill=CYAN_G)
    draw.text((cx,          cy), "N", font=font, fill=WHITE)

    return img


def save_png(img, name):
    path = os.path.join(ICONS_DIR, name)
    img.save(path, "PNG")
    print(f"  {name}")


def build_ico(sizes=(256, 128, 64, 48, 32, 16)):
    images = [draw_icon(s).convert("RGBA") for s in sizes]
    path   = os.path.join(ICONS_DIR, "icon.ico")
    # Pass sizes= so Pillow embeds each resolution; append_images adds the frames
    images[0].save(path, format="ICO", sizes=[(s, s) for s in sizes])
    print("  icon.ico")


def main():
    os.makedirs(ICONS_DIR, exist_ok=True)

    print("PNGs:")
    save_png(draw_icon(32),  "32x32.png")
    save_png(draw_icon(128), "128x128.png")
    save_png(draw_icon(256), "icon.png")

    print("ICO:")
    build_ico()

    print("\nDone.")


if __name__ == "__main__":
    main()
