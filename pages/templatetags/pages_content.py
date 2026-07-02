from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from pages.utils.block_render import (
    get_block_image_url,
    get_block_text,
    is_section_visible,
)

register = template.Library()


@register.simple_tag(takes_context=True)
def block_plain(context, page, key, fallback=''):
    site_blocks = context.get('site_blocks', {})
    return get_block_text(page, key, site_blocks=site_blocks, fallback=fallback)


@register.simple_tag(takes_context=True)
def section_visible(context, page, visibility_key):
    site_blocks = context.get('site_blocks', {})
    return is_section_visible(page, visibility_key, site_blocks=site_blocks)


@register.simple_tag(takes_context=True)
def block_image(context, page, key, css_class='', fallback_static='', alt=''):
    site_blocks = context.get('site_blocks', {})
    src = get_block_image_url(
        page,
        key,
        site_blocks=site_blocks,
        fallback_static=fallback_static,
    )
    alt_text = alt or get_block_text(page, f'{key}_alt', site_blocks=site_blocks)
    class_attr = f' class="{css_class}"' if css_class else ''
    return format_html('<img src="{}" alt="{}"{} loading="lazy">', src, alt_text, mark_safe(class_attr))


@register.simple_tag(takes_context=True)
def render_block(context, page, key, fallback=''):
    site_blocks = context.get('site_blocks', {})
    return mark_safe(get_block_text(page, key, site_blocks=site_blocks, fallback=fallback))
