import re
from html import unescape

from django.utils.html import strip_tags


_EMPTY_MARKERS = re.compile(r'[\s\u00a0\u200b]+')


def has_richtext_content(value: str | None) -> bool:
    """Return True when TinyMCE/HTML content has visible text."""
    if not value:
        return False
    text = strip_tags(value)
    text = unescape(text)
    text = text.replace('\xa0', ' ').replace('&nbsp;', ' ')
    text = _EMPTY_MARKERS.sub('', text)
    return bool(text)
