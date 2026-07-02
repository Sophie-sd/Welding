from django.contrib import admin

from .admin_site_content import SiteContentSectionAdmin
from .models import (
    AboutHeroSettings,
    AboutImperativesSettings,
    AboutStorySettings,
    BlogHeroSettings,
    ContactPageSettings,
    FaqHeroSettings,
    HomeHeroSettings,
    HomeShowcaseSettings,
    HomeValueGridSettings,
    PortfolioHeroSettings,
    PrivacyPageSettings,
    ServicesCatalogSettings,
    ServicesHeroSettings,
    ServicesSpecFormSettings,
    ServicesTimelineSettings,
    SiteFooterSettings,
    SiteHeaderSettings,
    SiteQuoteModalSettings,
    TermsPageSettings,
)

_SECTION_MODELS = (
    (HomeHeroSettings, 'home', 'hero'),
    (HomeValueGridSettings, 'home', 'value_grid'),
    (HomeShowcaseSettings, 'home', 'showcase'),
    (SiteHeaderSettings, 'site', 'header'),
    (SiteFooterSettings, 'site', 'footer'),
    (SiteQuoteModalSettings, 'site', 'quote_modal'),
    (AboutHeroSettings, 'about', 'hero'),
    (AboutStorySettings, 'about', 'story'),
    (AboutImperativesSettings, 'about', 'imperatives'),
    (ServicesHeroSettings, 'services', 'hero'),
    (ServicesCatalogSettings, 'services', 'catalog'),
    (ServicesTimelineSettings, 'services', 'timeline'),
    (ServicesSpecFormSettings, 'services', 'spec_form'),
    (PortfolioHeroSettings, 'portfolio', 'hero'),
    (BlogHeroSettings, 'blog', 'hero'),
    (FaqHeroSettings, 'faq', 'hero'),
    (ContactPageSettings, 'contact', 'page'),
    (PrivacyPageSettings, 'privacy', 'content'),
    (TermsPageSettings, 'terms', 'content'),
)


def register_site_content_section_admins():
    for model, page_slug, section_slug in _SECTION_MODELS:
        admin_class = type(
            f'{model.__name__}Admin',
            (SiteContentSectionAdmin,),
            {
                'page_slug': page_slug,
                'section_slug': section_slug,
            },
        )
        if model in admin.site._registry:
            continue
        admin.site.register(model, admin_class)
