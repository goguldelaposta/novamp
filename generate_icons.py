"""Generate all NovaMP icons: PNGs, ICO, and ICNS."""
import os
import shutil
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont

ICONS_DIR = os.path.join(os.path.dirname(__file__), "src-tauri", "icons")

BG       = (26, 0, 64, 255)    # #1a0040
RING1    = (45, 0, 128, 255)   # #2d0080
RING2    = (74, 66, 204, 255)  # #4a42cc
RING3    = (108, 99, 255, 255) # #6c63ff
WHITE    = (255, 255, 255, 255)
RED_G    = (255, 60, 60, 160)  # glitch red
CYAN_G   = (0, 240, 255, 160)  # glitch cyan

FONT_PATH  = "/System/Library/Fonts/Helvetica.ttc"
FONT_INDEX = 1  # Bold


def load_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size, index=FONT_INDEX)
    except Exception:
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

    font      = load_font(int(size * 0.58))
    bb        = draw.textbbox((0, 0), "N", font=font)
    tw, th    = bb[2] - bb[0], bb[3] - bb[1]
    cx        = (size - tw) // 2 - bb[0]
    cy        = (size - th) // 2 - bb[1]
    glitch    = max(1, size // 90)

    draw.text((cx - glitch, cy), "N", font=font, fill=RED_G)
    draw.text((cx + glitch, cy), "N", font=font, fill=CYAN_G)
    draw.text((cx,          cy), "N", font=font, fill=WHITE)

    return img


def save_png(img, name):
    path = os.path.join(ICONS_DIR, name)
    img.save(path, "PNG")
    print(f"  {name}")
    return path


def build_ico(sizes=(256, 128, 64, 48, 32, 16)):
    images = [draw_icon(s).convert("RGBA") for s in sizes]
    path   = os.path.join(ICONS_DIR, "icon.ico")
    images[0].save(path, format="ICO", append_images=images[1:],
                   sizes=[(s, s) for s in sizes])
    print("  icon.ico")


def build_icns():
    """Use macOS iconutil to assemble icon.icns from a temporary .iconset."""
    iconset = tempfile.mkdtemp(suffix=".iconset")
    spec = [
        (16,   "icon_16x16"),
        (32,   "icon_16x16@2x"),
        (32,   "icon_32x32"),
        (64,   "icon_32x32@2x"),
        (128,  "icon_128x128"),
        (256,  "icon_128x128@2x"),
        (256,  "icon_256x256"),
        (512,  "icon_256x256@2x"),
        (512,  "icon_512x512"),
        (1024, "icon_512x512@2x"),
    ]
    for px, name in spec:
        draw_icon(px).save(os.path.join(iconset, f"{name}.png"), "PNG")

    out = os.path.join(ICONS_DIR, "icon.icns")
    subprocess.run(["iconutil", "-c", "icns", iconset, "-o", out], check=True)
    shutil.rmtree(iconset)
    print("  icon.icns")


def main():
    os.makedirs(ICONS_DIR, exist_ok=True)
    print("Generating PNGs...")
    save_png(draw_icon(32),  "32x32.png")
    save_png(draw_icon(128), "128x128.png")
    save_png(draw_icon(256), "128x128@2x.png")
    save_png(draw_icon(256), "icon.png")

    print("Generating ICO...")
    build_ico()

    print("Generating ICNS...")
    build_icns()

    print("\nDone.")


if __name__ == "__main__":
    main()
