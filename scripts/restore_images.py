#!/usr/bin/env python3
"""Restore site images overwritten by placeholder generator."""

from pathlib import Path

from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / 'static' / 'images'
ASSETS_DIR = Path('/Users/sofiadmitrenko/.cursor/projects/Users-sofiadmitrenko-Sites-weldingProject/assets')


def save_image(image, name):
    path = IMAGES_DIR / name
    if name == 'logo-khodak.png':
        image.save(path, format='PNG', optimize=True)
    else:
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.save(path, format='PNG', optimize=True)
    print(f'Restored {path} ({path.stat().st_size} bytes)')


def restore_logo():
    src = ASSETS_DIR / '________________2026-06-26___17.23.23-e88f46a6-0605-420e-a91b-cd723da1e51a.png'
    if not src.exists():
        src = ASSETS_DIR / 'c2dd0f13-0a0e-40bb-b896-98ba568af2ef-685f476e-7b30-4c92-8e50-4912ea47452a.png'
    img = Image.open(src).convert('RGBA')
    pixels = img.load()
    width, height = img.size
    cleaned = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    cleaned_pixels = cleaned.load()
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            grey = (r + g + b) / 3
            if grey <= 240:
                cleaned_pixels[x, y] = (0, 0, 0, 255)
    bbox = cleaned.getbbox()
    if bbox:
        cleaned = cleaned.crop(bbox)
    logo_width, logo_height = cleaned.size
    scale = max(2, 540 // max(logo_width, 1))
    cleaned = cleaned.resize(
        (logo_width * scale, logo_height * scale),
        Image.Resampling.LANCZOS,
    )
    save_image(cleaned, 'logo-khodak.png')


def copy_asset(name):
    src = ASSETS_DIR / name
    if not src.exists():
        raise FileNotFoundError(src)
    img = Image.open(src)
    save_image(img, name)


def crop_and_save(image, box, name, size):
    cropped = image.crop(box).convert('RGB')
    cropped = cropped.resize(size, Image.Resampling.LANCZOS)
    save_image(cropped, name)


def restore_from_mockup():
    hero_about = Image.open(IMAGES_DIR / 'hero-about.png').convert('RGB')
    hero_about = hero_about.resize((1376, 768), Image.Resampling.LANCZOS)
    save_image(hero_about, 'hero-home.png')

    mockup = Image.open(IMAGES_DIR / 'hero-workshop.png')
    width, height = mockup.size
    crop_and_save(mockup, (18, 930, width - 18, 1180), 'project-frame.png', (800, 500))
    crop_and_save(mockup, (18, 1180, width - 18, 1430), 'project-tig.png', (800, 500))


def restore_workshop():
    src = ASSETS_DIR / '________________2026-06-26___17.53.17-235342a2-8d94-4dfe-adfc-396d996d4950.png'
    if not src.exists():
        raise FileNotFoundError(src)
    img = Image.open(src).convert('RGB')
    target_w = 1600
    target_h = round(img.height * target_w / img.width)
    img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    save_image(img, 'workshop.png')


def restore_tig_weld():
    src = ASSETS_DIR / '________________2026-06-26___17.54.40-d57bb8b4-4043-4279-a9d3-1a7030ba598e.png'
    if not src.exists():
        raise FileNotFoundError(src)
    img = Image.open(src).convert('RGB')
    target_w = 1200
    target_h = round(img.height * target_w / img.width)
    img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    save_image(img, 'tig-weld.png')


def restore_blueprints():
    frame = BASE_DIR / '.tmp' / 'video-frames' / 'frame_007.jpg'
    if not frame.exists():
        raise FileNotFoundError(frame)
    img = Image.open(frame).convert('RGB')
    w, h = img.size
    box = (int(w * 0.68), int(h * 0.34), int(w * 0.98), int(h * 0.58))
    cropped = img.crop(box)
    cropped = cropped.resize((1200, 750), Image.Resampling.LANCZOS)
    save_image(cropped, 'blueprints.png')


def restore_from_screenshots():
    restore_tig_weld()
    restore_blueprints()


def main():
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    restore_logo()
    copy_asset('hero-about.png')
    copy_asset('hero-contact.png')
    restore_from_mockup()
    restore_workshop()
    restore_from_screenshots()


if __name__ == '__main__':
    main()
