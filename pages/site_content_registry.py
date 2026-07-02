from dataclasses import dataclass, field
from typing import Iterator

from django.urls import reverse_lazy


@dataclass(frozen=True)
class FieldGroup:
    title: str
    keys: tuple[str, ...]


@dataclass(frozen=True)
class ContentSection:
    slug: str
    page_slug: str
    title: str
    blocks: tuple[tuple[str, str], ...]
    sidebar_title: str = ''
    sidebar_icon: str = 'edit_note'
    preview_url: str = '/'
    description: str = ''
    visibility_key: str = ''
    field_groups: tuple[FieldGroup, ...] = field(default_factory=tuple)
    admin_model_name: str = ''


def _hero_blocks(page: str, include_meta: bool = True) -> tuple[tuple[str, str], ...]:
    items = [
        (page, f'{_hero_prefix(page)}_section_visible'),
        (page, 'hero_eyebrow'),
        (page, 'hero_title'),
        (page, 'hero_lead'),
        (page, 'hero_image'),
        (page, 'hero_image_alt'),
    ]
    if include_meta:
        items.extend([(page, 'meta_title'), (page, 'meta_description')])
    return tuple(items)


def _hero_prefix(page: str) -> str:
    if page == 'contact':
        return 'page'
    return 'hero'


HOME_HERO_BLOCKS = (
    ('home', 'hero_section_visible'),
    ('home', 'hero_title'),
    ('home', 'hero_text'),
    ('home', 'hero_image'),
    ('home', 'hero_image_alt'),
    ('home', 'hero_cta_primary'),
    ('home', 'hero_cta_secondary'),
    ('home', 'meta_title'),
    ('home', 'meta_description'),
)

HEADER_BLOCKS = (
    ('site', 'header_logo_image'),
    ('site', 'header_nav_services_label'),
    ('site', 'header_nav_services_visible'),
    ('site', 'header_nav_portfolio_label'),
    ('site', 'header_nav_portfolio_visible'),
    ('site', 'header_nav_about_label'),
    ('site', 'header_nav_about_visible'),
    ('site', 'header_nav_blog_label'),
    ('site', 'header_nav_blog_visible'),
    ('site', 'header_nav_contact_label'),
    ('site', 'header_nav_contact_visible'),
    ('site', 'header_cta_text'),
    ('site', 'header_cta_visible'),
)

CONTENT_SECTIONS: tuple[ContentSection, ...] = (
    ContentSection(
        slug='hero',
        page_slug='home',
        title='Головна — Hero',
        sidebar_title='Головна — Hero',
        sidebar_icon='home',
        preview_url='/',
        visibility_key='hero_section_visible',
        admin_model_name='homeherosettings',
        blocks=HOME_HERO_BLOCKS,
        field_groups=(
            FieldGroup('Заголовок і текст', ('hero_title', 'hero_text')),
            FieldGroup('Зображення', ('hero_image', 'hero_image_alt')),
            FieldGroup('Кнопки', ('hero_cta_primary', 'hero_cta_secondary')),
            FieldGroup('SEO', ('meta_title', 'meta_description')),
        ),
    ),
    ContentSection(
        slug='value_grid',
        page_slug='home',
        title='Головна — Value Grid',
        sidebar_title='Головна — Переваги',
        sidebar_icon='grid_view',
        preview_url='/',
        visibility_key='value_grid_section_visible',
        admin_model_name='homevaluegridsettings',
        blocks=(
            ('home', 'value_grid_section_visible'),
            ('home', 'value_grid_title'),
            ('home', 'value_card_1_num'),
            ('home', 'value_card_1_title'),
            ('home', 'value_card_1_text'),
            ('home', 'value_card_2_num'),
            ('home', 'value_card_2_title'),
            ('home', 'value_card_3_num'),
            ('home', 'value_card_3_title'),
            ('home', 'value_card_4_num'),
            ('home', 'value_card_4_title'),
            ('home', 'value_card_5_num'),
            ('home', 'value_card_5_title'),
        ),
    ),
    ContentSection(
        slug='showcase',
        page_slug='home',
        title='Головна — Showcase',
        sidebar_title='Головна — Showcase',
        sidebar_icon='photo_library',
        preview_url='/',
        visibility_key='showcase_section_visible',
        admin_model_name='homeshowcasesettings',
        blocks=(
            ('home', 'showcase_section_visible'),
            ('home', 'showcase_title'),
            ('home', 'showcase_link_text'),
            ('home', 'showcase_card_1_image'),
            ('home', 'showcase_card_1_image_alt'),
            ('home', 'showcase_card_1_category'),
            ('home', 'showcase_card_1_title'),
            ('home', 'showcase_card_2_image'),
            ('home', 'showcase_card_2_image_alt'),
            ('home', 'showcase_card_2_category'),
            ('home', 'showcase_card_2_title'),
            ('home', 'showcase_view_btn'),
        ),
    ),
    ContentSection(
        slug='header',
        page_slug='site',
        title='Шапка сайту',
        sidebar_title='Шапка',
        sidebar_icon='web',
        preview_url='/',
        admin_model_name='siteheadersettings',
        blocks=HEADER_BLOCKS,
        field_groups=(
            FieldGroup('Логотип', ('header_logo_image',)),
            FieldGroup('Навігація', (
                'header_nav_services_label',
                'header_nav_services_visible',
                'header_nav_portfolio_label',
                'header_nav_portfolio_visible',
                'header_nav_about_label',
                'header_nav_about_visible',
                'header_nav_blog_label',
                'header_nav_blog_visible',
                'header_nav_contact_label',
                'header_nav_contact_visible',
            )),
            FieldGroup('CTA', ('header_cta_text', 'header_cta_visible')),
        ),
    ),
    ContentSection(
        slug='footer',
        page_slug='site',
        title='Підвал сайту',
        sidebar_title='Підвал',
        sidebar_icon='bottom_navigation',
        preview_url='/',
        visibility_key='footer_section_visible',
        admin_model_name='sitefootersettings',
        blocks=(
            ('site', 'footer_section_visible'),
            ('site', 'footer_logo_image'),
            ('site', 'footer_tagline'),
            ('site', 'footer_bottom_text'),
        ),
    ),
    ContentSection(
        slug='quote_modal',
        page_slug='site',
        title='Модальне вікно заявки',
        sidebar_title='Quote Modal',
        sidebar_icon='chat',
        preview_url='/',
        visibility_key='quote_modal_section_visible',
        admin_model_name='sitequotemodalsettings',
        blocks=(
            ('site', 'quote_modal_section_visible'),
            ('site', 'quote_modal_eyebrow'),
            ('site', 'quote_modal_title'),
            ('site', 'quote_modal_lead'),
            ('site', 'quote_modal_submit_label'),
        ),
    ),
    ContentSection(
        slug='hero',
        page_slug='about',
        title='Про нас — Hero',
        sidebar_title='Про нас — Hero',
        sidebar_icon='info',
        preview_url='/about/',
        visibility_key='hero_section_visible',
        admin_model_name='aboutherosettings',
        blocks=_hero_blocks('about'),
    ),
    ContentSection(
        slug='story',
        page_slug='about',
        title='Про нас — Our Story',
        sidebar_title='Про нас — Історія',
        sidebar_icon='menu_book',
        preview_url='/about/',
        visibility_key='story_section_visible',
        admin_model_name='aboutstorysettings',
        blocks=(
            ('about', 'story_section_visible'),
            ('about', 'story_eyebrow'),
            ('about', 'story_title'),
            ('about', 'story_col_1'),
            ('about', 'story_col_2'),
            ('about', 'story_col_3'),
        ),
    ),
    ContentSection(
        slug='imperatives',
        page_slug='about',
        title='Про нас — Core Imperatives',
        sidebar_title='Про нас — Імперативи',
        sidebar_icon='verified',
        preview_url='/about/',
        visibility_key='imperatives_section_visible',
        admin_model_name='aboutimperativessettings',
        blocks=(
            ('about', 'imperatives_section_visible'),
            ('about', 'imperatives_title'),
            ('about', 'imperative_1_title'),
            ('about', 'imperative_1_text'),
            ('about', 'imperative_2_title'),
            ('about', 'imperative_2_text'),
            ('about', 'imperative_3_title'),
            ('about', 'imperative_3_text'),
        ),
    ),
    ContentSection(
        slug='hero',
        page_slug='services',
        title='Послуги — Hero',
        sidebar_title='Послуги — Hero',
        sidebar_icon='build',
        preview_url='/services/',
        visibility_key='hero_section_visible',
        admin_model_name='servicesherosettings',
        blocks=_hero_blocks('services') + (('services', 'default_hero_image'),),
    ),
    ContentSection(
        slug='catalog',
        page_slug='services',
        title='Послуги — Каталог',
        sidebar_title='Послуги — Каталог',
        sidebar_icon='list_alt',
        preview_url='/services/',
        visibility_key='catalog_section_visible',
        admin_model_name='servicescatalogsettings',
        blocks=(
            ('services', 'catalog_section_visible'),
            ('services', 'catalog_title'),
            ('services', 'catalog_intro'),
        ),
    ),
    ContentSection(
        slug='timeline',
        page_slug='services',
        title='Послуги — How We Work',
        sidebar_title='Послуги — Процес',
        sidebar_icon='timeline',
        preview_url='/services/',
        visibility_key='timeline_section_visible',
        admin_model_name='servicestimelinesettings',
        blocks=(
            ('services', 'timeline_section_visible'),
            ('services', 'timeline_title'),
            ('services', 'timeline_step_1_title'),
            ('services', 'timeline_step_1_text'),
            ('services', 'timeline_step_1_image'),
            ('services', 'timeline_step_2_title'),
            ('services', 'timeline_step_2_text'),
            ('services', 'timeline_step_2_image'),
            ('services', 'timeline_step_3_title'),
            ('services', 'timeline_step_3_text'),
            ('services', 'timeline_step_3_image'),
        ),
    ),
    ContentSection(
        slug='spec_form',
        page_slug='services',
        title='Послуги — Submit Specifications',
        sidebar_title='Послуги — Форма',
        sidebar_icon='description',
        preview_url='/services/',
        visibility_key='spec_form_section_visible',
        admin_model_name='servicesspecformsettings',
        blocks=(
            ('services', 'spec_form_section_visible'),
            ('services', 'spec_form_title'),
            ('services', 'spec_form_intro'),
            ('services', 'spec_form_check_1'),
            ('services', 'spec_form_check_2'),
            ('services', 'spec_form_check_3'),
            ('services', 'spec_form_bg_image'),
        ),
    ),
    ContentSection(
        slug='hero',
        page_slug='portfolio',
        title='Портфоліо — Hero',
        sidebar_title='Портфоліо — Hero',
        sidebar_icon='collections',
        preview_url='/portfolio/',
        visibility_key='hero_section_visible',
        admin_model_name='portfolioherosettings',
        blocks=_hero_blocks('portfolio'),
    ),
    ContentSection(
        slug='hero',
        page_slug='blog',
        title='Блог — Hero',
        sidebar_title='Блог — Hero',
        sidebar_icon='article',
        preview_url='/blog/',
        visibility_key='hero_section_visible',
        admin_model_name='blogherosettings',
        blocks=_hero_blocks('blog'),
    ),
    ContentSection(
        slug='hero',
        page_slug='faq',
        title='FAQ — Hero',
        sidebar_title='FAQ — Hero',
        sidebar_icon='help',
        preview_url='/faq/',
        visibility_key='hero_section_visible',
        admin_model_name='faqherosettings',
        blocks=_hero_blocks('faq'),
    ),
    ContentSection(
        slug='page',
        page_slug='contact',
        title='Контакти',
        sidebar_title='Контакти',
        sidebar_icon='call',
        preview_url='/contact/',
        visibility_key='page_section_visible',
        admin_model_name='contactpagesettings',
        blocks=(
            ('contact', 'page_section_visible'),
            ('contact', 'contact_eyebrow'),
            ('contact', 'contact_title'),
            ('contact', 'contact_lead'),
            ('contact', 'hero_image'),
            ('contact', 'hero_image_alt'),
            ('contact', 'contact_figcaption'),
            ('contact', 'contact_hours'),
            ('contact', 'meta_title'),
            ('contact', 'meta_description'),
        ),
    ),
    ContentSection(
        slug='content',
        page_slug='privacy',
        title='Privacy Policy',
        sidebar_title='Privacy Policy',
        sidebar_icon='policy',
        preview_url='/privacy/',
        visibility_key='content_section_visible',
        admin_model_name='privacypagesettings',
        blocks=(
            ('privacy', 'content_section_visible'),
            ('privacy', 'privacy_title'),
            ('privacy', 'privacy_updated'),
            ('privacy', 'privacy_body'),
            ('privacy', 'meta_title'),
            ('privacy', 'meta_description'),
        ),
    ),
    ContentSection(
        slug='content',
        page_slug='terms',
        title='Terms of Service',
        sidebar_title='Terms of Service',
        sidebar_icon='gavel',
        preview_url='/terms/',
        visibility_key='content_section_visible',
        admin_model_name='termspagesettings',
        blocks=(
            ('terms', 'content_section_visible'),
            ('terms', 'terms_title'),
            ('terms', 'terms_updated'),
            ('terms', 'terms_body'),
            ('terms', 'meta_title'),
            ('terms', 'meta_description'),
        ),
    ),
)


def get_section(page_slug: str, section_slug: str) -> ContentSection:
    for section in CONTENT_SECTIONS:
        if section.page_slug == page_slug and section.slug == section_slug:
            return section
    raise KeyError(f'Unknown section: {page_slug}/{section_slug}')


def all_registry_block_keys() -> Iterator[tuple[str, str]]:
    seen: set[tuple[str, str]] = set()
    for section in CONTENT_SECTIONS:
        for page, key in section.blocks:
            if (page, key) in seen:
                continue
            seen.add((page, key))
            yield page, key


def iter_section_blocks(section: ContentSection) -> Iterator[tuple[str, str]]:
    yield from section.blocks


def build_content_sidebar_items() -> list[dict]:
    return [
        {
            'title': section.sidebar_title or section.title,
            'icon': section.sidebar_icon,
            'link': reverse_lazy(f'admin:pages_{section.admin_model_name}_changelist'),
        }
        for section in CONTENT_SECTIONS
    ]
