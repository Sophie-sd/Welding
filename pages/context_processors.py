from .models import BlogPost, FAQItem, PortfolioItem, Service, SiteSettings


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


def site_settings(request):
    return {
        'site': SiteContext(SiteSettings.load()),
        'current_path': request.path,
    }
