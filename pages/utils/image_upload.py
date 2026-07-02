import os
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image

from pages.cms_field_hints import IMAGE_PROFILES, ImageProfile


class ImageUploadError(ValueError):
    pass


def _open_image(uploaded_file) -> Image.Image:
    uploaded_file.seek(0)
    try:
        image = Image.open(uploaded_file)
        image.load()
    except OSError as exc:
        raise ImageUploadError('Не вдалося відкрити зображення. Перевірте формат файлу.') from exc
    finally:
        uploaded_file.seek(0)
    return image


def _fit_within(image: Image.Image, max_width: int, max_height: int) -> Image.Image:
    width, height = image.size
    if width <= max_width and height <= max_height:
        return image
    scale = min(max_width / width, max_height / height)
    new_size = (max(1, int(width * scale)), max(1, int(height * scale)))
    return image.resize(new_size, Image.Resampling.LANCZOS)


def _encode_webp(image: Image.Image, *, max_bytes: int) -> bytes:
    working = image
    if working.mode not in {'RGB', 'RGBA'}:
        working = working.convert('RGBA' if 'A' in working.getbands() else 'RGB')

    quality = 85
    min_quality = 60
    payload = b''

    while quality >= min_quality:
        buffer = BytesIO()
        save_kwargs = {
            'format': 'WEBP',
            'quality': quality,
            'method': 4,
        }
        if working.mode == 'RGBA':
            save_kwargs['lossless'] = False
        working.save(buffer, **save_kwargs)
        payload = buffer.getvalue()
        if len(payload) <= max_bytes:
            return payload
        quality -= 5

    raise ImageUploadError(
        f'Після стиснення зображення все ще перевищує ліміт '
        f'{max_bytes // 1024} KB. Завантажте менший файл.'
    )


def _build_filename(uploaded_file) -> str:
    base_name = os.path.splitext(os.path.basename(uploaded_file.name))[0]
    safe_name = ''.join(char if char.isalnum() or char in '-_' else '-' for char in base_name)
    safe_name = safe_name.strip('-_') or 'image'
    return f'{safe_name}.webp'


def process_admin_image(uploaded_file, *, profile: ImageProfile | str) -> ContentFile:
    if isinstance(profile, str):
        resolved = IMAGE_PROFILES.get(profile)
        if resolved is None:
            raise ImageUploadError(f'Невідомий профіль зображення: {profile}')
        profile = resolved

    image = _open_image(uploaded_file)
    image = _fit_within(image, profile.max_width, profile.max_height)
    payload = _encode_webp(image, max_bytes=profile.max_bytes)
    return ContentFile(payload, name=_build_filename(uploaded_file))
