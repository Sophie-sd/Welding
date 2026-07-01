#!/usr/bin/env python3
"""Generate missing PNG assets only when a file does not already exist."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / 'static' / 'images'

ASSETS = {
    'placeholder.png': (800, 500, '#2e343d', 'KHODAK'),
}


def build_image(width, height, color, label):
    image = Image.new('RGB', (width, height), color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), label, font=font)
    text_x = (width - (bbox[2] - bbox[0])) // 2
    text_y = (height - (bbox[3] - bbox[1])) // 2
    draw.text((text_x, text_y), label, fill='#e8eaed', font=font)
    return image


def main():
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    for filename, (width, height, color, label) in ASSETS.items():
        path = IMAGES_DIR / filename
        if path.exists():
            print(f'Skipped existing {path}')
            continue
        build_image(width, height, color, label).save(path, format='PNG')
        print(f'Created {path}')


if __name__ == '__main__':
    main()
