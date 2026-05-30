#!/usr/bin/env python3
"""Generate all NovaMP icons from scratch with proper bounds (Windows only)."""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

ICONS_DIR = os.path.join(os.path.dirname(__file__), '..', 'src-tauri', 'icons')

# ── Palette ──────────────────────────────────────────────────────────────────
BG          = (8,   6,  23, 255)   # very dark navy (safe behind macOS rounded corners)
OUTER_SQ    = (30,  27, 100, 255)  # dark indigo square
INNER_SQ    = (72,  68, 195, 255)  # medium blue square
N_COLOR     = (235, 230, 255, 255) # near-white with cool blue tint
GLOW_COLOR  = (100, 140, 255, 180) # blue glow

FONT_PATH = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'


def make_source(size: int) -> Image.Image:
    img = Image.new('RGBA', (size, size), BG)
    draw = ImageDraw.Draw(img)

    # Outer square: 7% inset from each edge
    p1 = int(size * 0.07)
    draw.rectangle([p1, p1, size - p1 - 1, size - p1 - 1], fill=OUTER_SQ)

    # Inner square: 15% inset from each edge
    p2 = int(size * 0.15)
    draw.rectangle([p2, p2, size - p2 - 1, size - p2 - 1], fill=INNER_SQ)

    # N letter
    font_size = int(size * 0.48)
    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except Exception:
        font = ImageFont.load_default(size=font_size)

    # Measure N
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    bbox = tmp.textbbox((0, 0), 'N', font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (size - tw) // 2 - bbox[0]
    y = (size - th) // 2 - bbox[1]

    # Glow layer (blurred)
    glow_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_draw.text((x, y), 'N', fill=GLOW_COLOR, font=font)
    radius = max(2, int(size * 0.025))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=radius))

    # Crisp N layer
    n_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(n_layer).text((x, y), 'N', fill=N_COLOR, font=font)

    img = Image.alpha_composite(img, glow_layer)
    img = Image.alpha_composite(img, n_layer)
    return img


def save_png(img: Image.Image, path: str, size: int) -> None:
    resized = img.resize((size, size), Image.LANCZOS)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    resized.save(path, 'PNG', optimize=True)
    print(f'  wrote {path}  ({size}×{size})')


def build_ico(source: Image.Image, out_path: str) -> None:
    # Pillow's ICO plugin downscales the source image to each requested size.
    # Passing sizes= is the correct multi-resolution approach; append_images is for GIF.
    base = source.resize((256, 256), Image.LANCZOS).convert('RGBA')
    base.save(out_path, format='ICO',
              sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])
    print(f'  wrote {out_path}')


def main() -> None:
    print('Generating icons at 1024×1024 source…')
    src = make_source(1024)

    print('\nPNG icons:')
    save_png(src, os.path.join(ICONS_DIR, 'icon.png'),    256)
    save_png(src, os.path.join(ICONS_DIR, '32x32.png'),    32)
    save_png(src, os.path.join(ICONS_DIR, '128x128.png'), 128)

    # Windows Store logos
    win_sizes = {
        'Square30x30Logo.png':   30,
        'Square44x44Logo.png':   44,
        'Square71x71Logo.png':   71,
        'Square89x89Logo.png':   89,
        'Square107x107Logo.png': 107,
        'Square142x142Logo.png': 142,
        'Square150x150Logo.png': 150,
        'Square284x284Logo.png': 284,
        'Square310x310Logo.png': 310,
        'StoreLogo.png':          50,
    }
    for name, sz in win_sizes.items():
        save_png(src, os.path.join(ICONS_DIR, name), sz)

    print('\nWindows .ico:')
    build_ico(src, os.path.join(ICONS_DIR, 'icon.ico'))

    print('\nDone.')


if __name__ == '__main__':
    main()
