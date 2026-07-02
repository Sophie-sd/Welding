from django.core.cache import cache

from .models import BlogPost, FAQItem, PortfolioItem, Service, SiteBlock, SiteSettings

SITE_BLOCKS_CACHE_KEY = 'khodak_site_blocks_v1'
SITE_BLOCKS_CACHE_TTL = 60


class SiteContext:
    """Template-compatible facade over SiteSettings and published content."""

    def __init__(self, settings_obj):
        self._settings = settings_obj

    @property
    def SITE_NAME(self):
        return self._settings.site_name

    @property
    def SITE_SHORT(self):
        return self._settings.site_short

    @property
    def SITE_TAGLINE(self):
        return self._settings.site_tagline

    @property
    def SITE_DESCRIPTION(self):
        return self._settings.site_description

    @property
    def SITE_URL(self):
        return self._settings.site_url

    @property
    def SITE_PHONE(self):
        return self._settings.site_phone

    @property
    def SITE_EMAIL(self):
        return self._settings.site_email

    @property
    def SITE_ADDRESS(self):
        return self._settings.site_address

    @property
    def SITE_YEAR(self):
        return self._settings.site_year

    @property
    def SERVICES(self):
        return Service.objects.filter(is_published=True)

    @property
    def PORTFOLIO_ITEMS(self):
        return PortfolioItem.objects.filter(is_published=True)

    @property
    def FAQ_ITEMS(self):
        return FAQItem.objects.filter(is_published=True)

    @property
    def BLOG_POSTS(self):
        return BlogPost.objects.filter(is_published=True)


def _load_site_blocks():
    cached = cache.get(SITE_BLOCKS_CACHE_KEY)
    if cached is not None:
        return cached

    blocks = {
        block.cache_key: block
        for block in SiteBlock.objects.filter(is_active=True)
    }
    cache.set(SITE_BLOCKS_CACHE_KEY, blocks, SITE_BLOCKS_CACHE_TTL)
    return blocks


def site_settings(request):
    return {
        'site': SiteContext(SiteSettings.load()),
        'site_blocks': _load_site_blocks(),
        'current_path': request.path,
    }
