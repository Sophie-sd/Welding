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


CARD_IMAGE_SIZE = (1600, 1200)
INDUSTRIAL_FRAME_SOURCE = IMAGES_DIR / 'heavy-industrial-frame-source.png'


def trim_content_margin(image, threshold=210):
    rgb = image.convert('RGB')
    width, height = rgb.size
    pixels = rgb.load()
    top, left, bottom, right = height, width, 0, 0

    def mark_content(x, y):
        nonlocal top, left, bottom, right
        red, green, blue = pixels[x, y]
        if red < threshold or green < threshold or blue < threshold:
            top = min(top, y)
            bottom = max(bottom, y)
            left = min(left, x)
            right = max(right, x)

    for y in range(height):
        for x in range(0, width, max(1, width // 24)):
            mark_content(x, y)
    for x in range(width):
        for y in range(0, height, max(1, height // 24)):
            mark_content(x, y)

    if bottom <= top or right <= left:
        return rgb

    pad = max(2, min(width, height) // 200)
    return rgb.crop((
        max(0, left - pad),
        max(0, top - pad),
        min(width, right + pad),
        min(height, bottom + pad),
    ))
    

def crop_light_top_band(image, max_rows=80, threshold=210):
    rgb = image.convert('RGB')
    width, height = rgb.size
    pixels = rgb.load()
    top = 0
    for y in range(min(max_rows, height)):
        if all(
            pixels[x, y][0] > threshold
            and pixels[x, y][1] > threshold
            and pixels[x, y][2] > threshold
            for x in range(0, width, max(1, width // 30))
        ):
            top = y + 1
        else:
            break
    if top == 0:
        return image
    trimmed = rgb.crop((0, top, width, height))
    return trimmed.resize((width, height), Image.Resampling.LANCZOS)


def center_crop_to_ratio(image, target_w, target_h, anchor='center'):
    target_ratio = target_w / target_h
    width, height = image.size
    current_ratio = width / height
    if current_ratio > target_ratio:
        new_w = int(height * target_ratio)
        left = (width - new_w) // 2
        box = (left, 0, left + new_w, height)
    else:
        new_h = int(width / target_ratio)
        if anchor == 'top':
            top = 0
        elif anchor == 'bottom':
            top = height - new_h
        else:
            top = (height - new_h) // 2
        box = (0, top, width, top + new_h)
    return image.crop(box).resize((target_w, target_h), Image.Resampling.LANCZOS)


def industrial_frame_source():
    if not INDUSTRIAL_FRAME_SOURCE.exists():
        raise FileNotFoundError(INDUSTRIAL_FRAME_SOURCE)
    return Image.open(INDUSTRIAL_FRAME_SOURCE)


def restore_hero_home():
    src = IMAGES_DIR / 'welder.png'
    if not src.exists():
        src = IMAGES_DIR / 'hero-about.png'
    save_image(center_crop_to_ratio(Image.open(src).convert('RGB'), 1376, 768), 'hero-home.png')


def restore_project_frame():
    save_image(center_crop_to_ratio(industrial_frame_source().convert('RGB'), *CARD_IMAGE_SIZE), 'project-frame.png')


def restore_project_tig():
    src = IMAGES_DIR / 'tig-weld.png'
    if not src.exists():
        raise FileNotFoundError(src)
    cleaned = trim_content_margin(Image.open(src))
    cropped = center_crop_to_ratio(cleaned, *CARD_IMAGE_SIZE, 'center')
    save_image(crop_light_top_band(cropped), 'project-tig.png')


def restore_portfolio_images():
    portfolio_sources = {
        'portfolio-omega.png': (industrial_frame_source(), 'center'),
        'portfolio-nexus.png': (IMAGES_DIR / 'workshop.png', 'center'),
        'portfolio-bridge.png': (IMAGES_DIR / 'welder.png', 'top'),
        'portfolio-residential.png': (IMAGES_DIR / 'hero-contact.png', 'center'),
        'portfolio-ironwood.png': (ASSETS_DIR / 'portfolio-ironwood.png', 'center'),
    }
    for name, (src, anchor) in portfolio_sources.items():
        img = src if isinstance(src, Image.Image) else Image.open(src)
        if name == 'portfolio-bridge.png':
            img = trim_content_margin(img)
        save_image(center_crop_to_ratio(img.convert('RGB'), *CARD_IMAGE_SIZE, anchor), name)


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
    img = trim_content_margin(Image.open(src).convert('RGB'))
    target_w = 1200
    target_h = round(img.height * target_w / img.width)
    img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    save_image(crop_light_top_band(img), 'tig-weld.png')


def restore_hero_about():
    src = ASSETS_DIR / 'hero-about-new.png'
    if not src.exists():
        src = ASSETS_DIR / 'hero-about.png'
    if not src.exists():
        raise FileNotFoundError(src)
    img = Image.open(src).convert('RGB')
    target_w = 1200
    target_h = round(img.height * target_w / img.width)
    img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    save_image(crop_light_top_band(img), 'hero-about.png')


def restore_hero_faq():
    src = ASSETS_DIR / 'hero-faq.png'
    if not src.exists():
        raise FileNotFoundError(src)
    img = Image.open(src).convert('RGB')
    target_w = 1200
    target_h = round(img.height * target_w / img.width)
    img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    save_image(img, 'hero-faq.png')


def restore_hero_portfolio():
    src = ASSETS_DIR / 'hero-portfolio.png'
    if not src.exists():
        raise FileNotFoundError(src)
    img = Image.open(src).convert('RGB')
    target_w = 1200
    target_h = round(img.height * target_w / img.width)
    img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    save_image(crop_light_top_band(img), 'hero-portfolio.png')


def restore_hero_blog():
    src = ASSETS_DIR / 'hero-blog.png'
    if not src.exists():
        raise FileNotFoundError(src)
    img = Image.open(src).convert('RGB')
    target_w = 1200
    target_h = round(img.height * target_w / img.width)
    img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    save_image(crop_light_top_band(img), 'hero-blog.png')


def restore_home_showcase_tig():
    src = ASSETS_DIR / 'home-showcase-tig.png'
    if not src.exists():
        raise FileNotFoundError(src)
    img = Image.open(src).convert('RGB')
    img = center_crop_to_ratio(img, *CARD_IMAGE_SIZE, 'center')
    save_image(crop_light_top_band(img), 'home-showcase-tig.png')


def restore_blog_featured_structural():
    src = ASSETS_DIR / 'blog-featured-structural.png'
    if not src.exists():
        raise FileNotFoundError(src)
    img = Image.open(src).convert('RGB')
    img = center_crop_to_ratio(img, *CARD_IMAGE_SIZE, 'center')
    save_image(crop_light_top_band(img), 'blog-featured-structural.png')


def restore_blog_blueprints():
    src = ASSETS_DIR / 'blog-blueprints.png'
    if not src.exists():
        raise FileNotFoundError(src)
    img = Image.open(src).convert('RGB')
    img = center_crop_to_ratio(img, *CARD_IMAGE_SIZE, 'center')
    save_image(crop_light_top_band(img), 'blog-blueprints.png')


def restore_blueprints():
    restore_blog_blueprints()
    legacy = IMAGES_DIR / 'blog-blueprints.png'
    if legacy.exists():
        save_image(Image.open(legacy).convert('RGB'), 'blueprints.png')


def restore_from_screenshots():
    restore_tig_weld()
    restore_blueprints()


def main():
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    restore_logo()
    restore_hero_about()
    copy_asset('hero-contact.png')
    restore_workshop()
    restore_from_screenshots()
    restore_hero_faq()
    restore_hero_portfolio()
    restore_hero_blog()
    restore_project_frame()
    restore_project_tig()
    restore_home_showcase_tig()
    restore_blog_featured_structural()
    restore_portfolio_images()
    restore_hero_home()


if __name__ == '__main__':
    main()
