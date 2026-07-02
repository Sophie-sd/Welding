from django.templatetags.static import static

from pages.block_defaults import BLOCK_DEFAULTS, default_for_block
from pages.models import SiteBlock, SiteSettings


def get_block_record(page: str, key: str, site_blocks=None):
    if site_blocks is None:
        site_blocks = {}
    cache_key = f'{page}.{key}'
    return site_blocks.get(cache_key)


def _apply_site_placeholders(text: str, site_settings=None) -> str:
    if not text:
        return text
    settings = site_settings or SiteSettings.load()
    phone_raw = settings.site_phone.replace(' ', '')
    replacements = {
        '{site_name}': settings.site_name,
        '{site_url}': settings.site_url,
        '{site_email}': settings.site_email,
        '{site_phone}': settings.site_phone,
        '{site_phone_raw}': phone_raw,
        '{site_address}': settings.site_address,
    }
    for placeholder, value in replacements.items():
        text = text.replace(placeholder, value)
    return text


def get_block_text(page: str, key: str, site_blocks=None, fallback: str | None = None) -> str:
    block = get_block_record(page, key, site_blocks=site_blocks)
    if block and block.text_html:
        return _apply_site_placeholders(block.text_html)
    if fallback is not None:
        return _apply_site_placeholders(fallback)
    default = default_for_block(page, key)
    if default:
        return _apply_site_placeholders(default)
    return ''


def is_section_visible(page: str, visibility_key: str, site_blocks=None) -> bool:
    value = get_block_text(page, visibility_key, site_blocks=site_blocks, fallback='1')
    return value not in {'0', 'false', 'False', ''}


def get_block_image_url(page: str, key: str, site_blocks=None, fallback_static: str = '') -> str:
    block = get_block_record(page, key, site_blocks=site_blocks)
    if block and block.image:
        return block.image.url
    static_path = ''
    if block and block.text_html:
        static_path = block.text_html
    elif fallback_static:
        static_path = fallback_static
    else:
        static_path = BLOCK_DEFAULTS.get((page, key), '')
    if static_path:
        return static(static_path)
    return static('images/placeholder.png')
