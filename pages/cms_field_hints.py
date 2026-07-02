from dataclasses import dataclass
from fnmatch import fnmatch


@dataclass(frozen=True)
class ImageProfile:
    name: str
    max_width: int
    max_height: int
    max_bytes: int

    @property
    def max_kb(self) -> int:
        return self.max_bytes // 1024

    def help_text_uk(self) -> str:
        return (
            f'Максимум {self.max_width}×{self.max_height} px, '
            f'до {self.max_kb} KB. Після завантаження зображення автоматично '
            f'конвертуються у WebP.'
        )


@dataclass(frozen=True)
class FieldHint:
    char_max: int | None = None
    image_profile: ImageProfile | None = None
    description_uk: str = ''

    def help_text_uk(self) -> str:
        parts: list[str] = []
        if self.description_uk:
            parts.append(self.description_uk)
        if self.char_max:
            parts.append(f'Максимум {self.char_max} символів.')
        if self.image_profile:
            parts.append(self.image_profile.help_text_uk())
        return ' '.join(parts)


IMAGE_PROFILES: dict[str, ImageProfile] = {
    'logo': ImageProfile('logo', 540, 160, 150 * 1024),
    'hero': ImageProfile('hero', 1600, 1200, 600 * 1024),
    'card': ImageProfile('card', 1600, 1200, 500 * 1024),
    'content': ImageProfile('content', 1600, 1200, 500 * 1024),
}

EXACT_CHAR_LIMITS: dict[str, int] = {
    'hero_eyebrow': 28,
    'hero_title': 72,
    'hero_lead': 240,
    'hero_text': 240,
    'meta_title': 60,
    'meta_description': 160,
    'footer_bottom_text': 80,
    'hero_image_alt': 120,
}

EXACT_DESCRIPTIONS: dict[str, str] = {
    'hero_eyebrow': 'Коротка мітка над заголовком.',
    'hero_title': 'Головний заголовок секції.',
    'hero_lead': 'Підзаголовок або вступний текст секції.',
    'hero_text': 'Основний текст hero-блоку.',
    'meta_title': 'SEO-заголовок сторінки (рекомендовано до 60 символів).',
    'meta_description': 'SEO-опис сторінки (рекомендовано до 160 символів).',
    'footer_bottom_text': 'Додатковий текст у нижній частині підвалу.',
    'hero_image_alt': 'Опис зображення для доступності (alt).',
}

PATTERN_CHAR_LIMITS: tuple[tuple[str, int, str], ...] = (
    ('*_category', 32, 'Категорія картки.'),
    ('value_card_*_text', 120, 'Короткий опис переваги.'),
    ('*_title', 48, 'Заголовок блоку.'),
)

LOGO_IMAGE_KEYS = frozenset({
    'header_logo_image',
    'footer_logo_image',
})

HERO_IMAGE_KEYS = frozenset({
    'hero_image',
    'default_hero_image',
})

CARD_IMAGE_SUFFIXES = (
    'showcase_card_1_image',
    'showcase_card_2_image',
    'timeline_step_1_image',
    'timeline_step_2_image',
    'timeline_step_3_image',
    'spec_form_bg_image',
)


def image_profile_for_key(key: str) -> ImageProfile | None:
    if not key.endswith('_image'):
        return None
    if key in LOGO_IMAGE_KEYS:
        return IMAGE_PROFILES['logo']
    if key in HERO_IMAGE_KEYS:
        return IMAGE_PROFILES['hero']
    if key in CARD_IMAGE_SUFFIXES or key.endswith('_image'):
        if 'logo' in key:
            return IMAGE_PROFILES['logo']
        if 'hero' in key:
            return IMAGE_PROFILES['hero']
        return IMAGE_PROFILES['card']
    return IMAGE_PROFILES['card']


def _pattern_char_hint(key: str) -> tuple[int, str] | None:
    if key == 'hero_title':
        return None
    for pattern, char_max, description in PATTERN_CHAR_LIMITS:
        if fnmatch(key, pattern):
            return char_max, description
    return None


def get_field_hint(page: str, key: str) -> FieldHint:
    image_profile = image_profile_for_key(key)
    if key in EXACT_CHAR_LIMITS or key in EXACT_DESCRIPTIONS:
        return FieldHint(
            char_max=EXACT_CHAR_LIMITS.get(key),
            image_profile=image_profile,
            description_uk=EXACT_DESCRIPTIONS.get(key, ''),
        )

    pattern = _pattern_char_hint(key)
    if pattern:
        char_max, description = pattern
        return FieldHint(
            char_max=char_max,
            image_profile=image_profile,
            description_uk=description,
        )

    if image_profile:
        return FieldHint(image_profile=image_profile)

    return FieldHint()


def get_model_image_hint() -> str:
    return IMAGE_PROFILES['content'].help_text_uk()
