from pages.block_defaults_legal import PRIVACY_BODY_DEFAULT, TERMS_BODY_DEFAULT

VISIBILITY_ON = '1'
VISIBILITY_OFF = '0'


def is_visibility_key(key: str) -> bool:
    return key.endswith('_visible')


def default_visibility(page: str, key: str) -> str:
    return VISIBILITY_ON


BLOCK_CONTENT_TYPES: dict[tuple[str, str], str] = {
    ('home', 'hero_image'): 'image',
    ('home', 'showcase_card_1_image'): 'image',
    ('home', 'showcase_card_2_image'): 'image',
    ('site', 'header_logo_image'): 'image',
    ('site', 'footer_logo_image'): 'image',
    ('about', 'hero_image'): 'image',
    ('services', 'hero_image'): 'image',
    ('services', 'timeline_step_1_image'): 'image',
    ('services', 'timeline_step_2_image'): 'image',
    ('services', 'timeline_step_3_image'): 'image',
    ('services', 'spec_form_bg_image'): 'image',
    ('services', 'default_hero_image'): 'image',
    ('portfolio', 'hero_image'): 'image',
    ('blog', 'hero_image'): 'image',
    ('faq', 'hero_image'): 'image',
    ('contact', 'hero_image'): 'image',
}

INLINE_KEYS = frozenset({
    'hero_cta_primary',
    'hero_cta_secondary',
    'hero_eyebrow',
    'hero_image_alt',
    'value_card_1_num',
    'value_card_1_title',
    'value_card_2_num',
    'value_card_2_title',
    'value_card_3_num',
    'value_card_3_title',
    'value_card_4_num',
    'value_card_4_title',
    'value_card_5_num',
    'value_card_5_title',
    'showcase_link_text',
    'showcase_card_1_category',
    'showcase_card_1_title',
    'showcase_card_2_category',
    'showcase_card_2_title',
    'showcase_view_btn',
    'header_nav_services_label',
    'header_nav_portfolio_label',
    'header_nav_about_label',
    'header_nav_blog_label',
    'header_nav_contact_label',
    'header_cta_text',
    'footer_bottom_text',
    'quote_modal_eyebrow',
    'quote_modal_title',
    'quote_modal_submit_label',
    'story_eyebrow',
    'imperative_1_title',
    'imperative_2_title',
    'imperative_3_title',
    'timeline_step_1_title',
    'timeline_step_2_title',
    'timeline_step_3_title',
    'spec_form_check_1',
    'spec_form_check_2',
    'spec_form_check_3',
    'contact_eyebrow',
    'contact_figcaption',
    'contact_hours',
    'privacy_title',
    'privacy_updated',
    'terms_title',
    'terms_updated',
    'meta_title',
})

MULTILINE_KEYS = frozenset({
    'hero_text',
    'hero_lead',
    'value_card_1_text',
    'story_col_1',
    'story_col_2',
    'story_col_3',
    'imperative_1_text',
    'imperative_2_text',
    'imperative_3_text',
    'catalog_intro',
    'timeline_step_1_text',
    'timeline_step_2_text',
    'timeline_step_3_text',
    'spec_form_intro',
    'contact_lead',
    'quote_modal_lead',
    'footer_tagline',
    'privacy_body',
    'terms_body',
})

RICHTEXT_KEYS = frozenset({'privacy_body', 'terms_body'})

BLOCK_FIELD_LABELS: dict[tuple[str, str], str] = {
    # ── Головна — Верхній банер ────────────────────────────────────────────
    ('home', 'hero_section_visible'): 'Секція видима',
    ('home', 'hero_title'): 'Заголовок',
    ('home', 'hero_text'): 'Підзаголовок',
    ('home', 'hero_image'): 'Фонове зображення',
    ('home', 'hero_image_alt'): 'Alt-текст зображення',
    ('home', 'hero_cta_primary'): 'Кнопка — основна',
    ('home', 'hero_cta_secondary'): 'Кнопка — додаткова',
    ('home', 'meta_title'): 'SEO-заголовок',
    ('home', 'meta_description'): 'SEO-опис',
    # ── Головна — Переваги ─────────────────────────────────────────────────
    ('home', 'value_grid_section_visible'): 'Секція видима',
    ('home', 'value_grid_title'): 'Заголовок секції',
    ('home', 'value_card_1_num'): 'Картка 1 — номер',
    ('home', 'value_card_1_title'): 'Картка 1 — заголовок',
    ('home', 'value_card_1_text'): 'Картка 1 — текст',
    ('home', 'value_card_2_num'): 'Картка 2 — номер',
    ('home', 'value_card_2_title'): 'Картка 2 — заголовок',
    ('home', 'value_card_3_num'): 'Картка 3 — номер',
    ('home', 'value_card_3_title'): 'Картка 3 — заголовок',
    ('home', 'value_card_4_num'): 'Картка 4 — номер',
    ('home', 'value_card_4_title'): 'Картка 4 — заголовок',
    ('home', 'value_card_5_num'): 'Картка 5 — номер',
    ('home', 'value_card_5_title'): 'Картка 5 — заголовок',
    # ── Головна — Проєкти ──────────────────────────────────────────────────
    ('home', 'showcase_section_visible'): 'Секція видима',
    ('home', 'showcase_title'): 'Заголовок секції',
    ('home', 'showcase_link_text'): 'Посилання «Всі проєкти»',
    ('home', 'showcase_card_1_image'): 'Картка 1 — зображення',
    ('home', 'showcase_card_1_image_alt'): 'Картка 1 — alt-текст',
    ('home', 'showcase_card_1_category'): 'Картка 1 — категорія',
    ('home', 'showcase_card_1_title'): 'Картка 1 — заголовок',
    ('home', 'showcase_card_2_image'): 'Картка 2 — зображення',
    ('home', 'showcase_card_2_image_alt'): 'Картка 2 — alt-текст',
    ('home', 'showcase_card_2_category'): 'Картка 2 — категорія',
    ('home', 'showcase_card_2_title'): 'Картка 2 — заголовок',
    ('home', 'showcase_view_btn'): 'Кнопка «Переглянути»',
    # ── Шапка сайту ────────────────────────────────────────────────────────
    ('site', 'header_logo_image'): 'Логотип (зображення)',
    ('site', 'header_nav_services_label'): 'Пункт меню — Послуги',
    ('site', 'header_nav_services_visible'): 'Послуги — показувати',
    ('site', 'header_nav_portfolio_label'): 'Пункт меню — Портфоліо',
    ('site', 'header_nav_portfolio_visible'): 'Портфоліо — показувати',
    ('site', 'header_nav_about_label'): 'Пункт меню — Про нас',
    ('site', 'header_nav_about_visible'): 'Про нас — показувати',
    ('site', 'header_nav_blog_label'): 'Пункт меню — Блог',
    ('site', 'header_nav_blog_visible'): 'Блог — показувати',
    ('site', 'header_nav_contact_label'): 'Пункт меню — Контакти',
    ('site', 'header_nav_contact_visible'): 'Контакти — показувати',
    ('site', 'header_cta_text'): 'Кнопка дії',
    ('site', 'header_cta_visible'): 'Кнопка дії — показувати',
    # ── Підвал сайту ───────────────────────────────────────────────────────
    ('site', 'footer_section_visible'): 'Секція видима',
    ('site', 'footer_logo_image'): 'Логотип у підвалі',
    ('site', 'footer_tagline'): 'Слоган',
    ('site', 'footer_bottom_text'): 'Текст внизу підвалу',
    # ── Вікно заявки ───────────────────────────────────────────────────────
    ('site', 'quote_modal_section_visible'): 'Вікно активне',
    ('site', 'quote_modal_eyebrow'): 'Надзаголовок',
    ('site', 'quote_modal_title'): 'Заголовок',
    ('site', 'quote_modal_lead'): 'Вступний текст',
    ('site', 'quote_modal_submit_label'): 'Текст кнопки відправки',
    # ── Про нас ────────────────────────────────────────────────────────────
    ('about', 'hero_section_visible'): 'Секція видима',
    ('about', 'hero_eyebrow'): 'Надзаголовок',
    ('about', 'hero_title'): 'Заголовок',
    ('about', 'hero_lead'): 'Вступний текст',
    ('about', 'hero_image'): 'Фонове зображення',
    ('about', 'hero_image_alt'): 'Alt-текст зображення',
    ('about', 'meta_title'): 'SEO-заголовок',
    ('about', 'meta_description'): 'SEO-опис',
    ('about', 'story_section_visible'): 'Секція видима',
    ('about', 'story_eyebrow'): 'Надзаголовок',
    ('about', 'story_title'): 'Заголовок секції',
    ('about', 'story_col_1'): 'Колонка 1',
    ('about', 'story_col_2'): 'Колонка 2',
    ('about', 'story_col_3'): 'Колонка 3',
    ('about', 'imperatives_section_visible'): 'Секція видима',
    ('about', 'imperatives_title'): 'Заголовок секції',
    ('about', 'imperative_1_title'): 'Цінність 1 — заголовок',
    ('about', 'imperative_1_text'): 'Цінність 1 — текст',
    ('about', 'imperative_2_title'): 'Цінність 2 — заголовок',
    ('about', 'imperative_2_text'): 'Цінність 2 — текст',
    ('about', 'imperative_3_title'): 'Цінність 3 — заголовок',
    ('about', 'imperative_3_text'): 'Цінність 3 — текст',
    # ── Послуги ────────────────────────────────────────────────────────────
    ('services', 'hero_section_visible'): 'Секція видима',
    ('services', 'hero_eyebrow'): 'Надзаголовок',
    ('services', 'hero_title'): 'Заголовок',
    ('services', 'hero_lead'): 'Вступний текст',
    ('services', 'hero_image'): 'Фонове зображення',
    ('services', 'hero_image_alt'): 'Alt-текст зображення',
    ('services', 'default_hero_image'): 'Зображення за замовчуванням',
    ('services', 'meta_title'): 'SEO-заголовок',
    ('services', 'meta_description'): 'SEO-опис',
    ('services', 'catalog_section_visible'): 'Секція видима',
    ('services', 'catalog_title'): 'Заголовок каталогу',
    ('services', 'catalog_intro'): 'Вступний текст каталогу',
    ('services', 'timeline_section_visible'): 'Секція видима',
    ('services', 'timeline_title'): 'Заголовок секції',
    ('services', 'timeline_step_1_title'): 'Крок 1 — назва',
    ('services', 'timeline_step_1_text'): 'Крок 1 — опис',
    ('services', 'timeline_step_1_image'): 'Крок 1 — зображення',
    ('services', 'timeline_step_2_title'): 'Крок 2 — назва',
    ('services', 'timeline_step_2_text'): 'Крок 2 — опис',
    ('services', 'timeline_step_2_image'): 'Крок 2 — зображення',
    ('services', 'timeline_step_3_title'): 'Крок 3 — назва',
    ('services', 'timeline_step_3_text'): 'Крок 3 — опис',
    ('services', 'timeline_step_3_image'): 'Крок 3 — зображення',
    ('services', 'spec_form_section_visible'): 'Секція видима',
    ('services', 'spec_form_title'): 'Заголовок форми',
    ('services', 'spec_form_intro'): 'Вступний текст форми',
    ('services', 'spec_form_check_1'): 'Пункт переваги 1',
    ('services', 'spec_form_check_2'): 'Пункт переваги 2',
    ('services', 'spec_form_check_3'): 'Пункт переваги 3',
    ('services', 'spec_form_bg_image'): 'Фонове зображення',
    # ── Портфоліо ──────────────────────────────────────────────────────────
    ('portfolio', 'hero_section_visible'): 'Секція видима',
    ('portfolio', 'hero_eyebrow'): 'Надзаголовок',
    ('portfolio', 'hero_title'): 'Заголовок',
    ('portfolio', 'hero_lead'): 'Вступний текст',
    ('portfolio', 'hero_image'): 'Фонове зображення',
    ('portfolio', 'hero_image_alt'): 'Alt-текст зображення',
    ('portfolio', 'meta_title'): 'SEO-заголовок',
    ('portfolio', 'meta_description'): 'SEO-опис',
    # ── Блог ───────────────────────────────────────────────────────────────
    ('blog', 'hero_section_visible'): 'Секція видима',
    ('blog', 'hero_eyebrow'): 'Надзаголовок',
    ('blog', 'hero_title'): 'Заголовок',
    ('blog', 'hero_lead'): 'Вступний текст',
    ('blog', 'hero_image'): 'Фонове зображення',
    ('blog', 'hero_image_alt'): 'Alt-текст зображення',
    ('blog', 'meta_title'): 'SEO-заголовок',
    ('blog', 'meta_description'): 'SEO-опис',
    # ── FAQ ────────────────────────────────────────────────────────────────
    ('faq', 'hero_section_visible'): 'Секція видима',
    ('faq', 'hero_eyebrow'): 'Надзаголовок',
    ('faq', 'hero_title'): 'Заголовок',
    ('faq', 'hero_lead'): 'Вступний текст',
    ('faq', 'hero_image'): 'Фонове зображення',
    ('faq', 'hero_image_alt'): 'Alt-текст зображення',
    ('faq', 'meta_title'): 'SEO-заголовок',
    ('faq', 'meta_description'): 'SEO-опис',
    # ── Контакти ───────────────────────────────────────────────────────────
    ('contact', 'page_section_visible'): 'Секція видима',
    ('contact', 'contact_eyebrow'): 'Надзаголовок',
    ('contact', 'contact_title'): 'Заголовок',
    ('contact', 'contact_lead'): 'Вступний текст',
    ('contact', 'hero_image'): 'Зображення сторінки',
    ('contact', 'hero_image_alt'): 'Alt-текст зображення',
    ('contact', 'contact_figcaption'): 'Підпис до фото',
    ('contact', 'contact_hours'): 'Графік роботи',
    ('contact', 'meta_title'): 'SEO-заголовок',
    ('contact', 'meta_description'): 'SEO-опис',
    # ── Юридичні сторінки ──────────────────────────────────────────────────
    ('privacy', 'content_section_visible'): 'Секція видима',
    ('privacy', 'privacy_title'): 'Заголовок сторінки',
    ('privacy', 'privacy_updated'): 'Дата оновлення',
    ('privacy', 'privacy_body'): 'Текст документа',
    ('privacy', 'meta_title'): 'SEO-заголовок',
    ('privacy', 'meta_description'): 'SEO-опис',
    ('terms', 'content_section_visible'): 'Секція видима',
    ('terms', 'terms_title'): 'Заголовок сторінки',
    ('terms', 'terms_updated'): 'Дата оновлення',
    ('terms', 'terms_body'): 'Текст документа',
    ('terms', 'meta_title'): 'SEO-заголовок',
    ('terms', 'meta_description'): 'SEO-опис',
}

BLOCK_DEFAULTS: dict[tuple[str, str], str] = {
    ('home', 'hero_section_visible'): VISIBILITY_ON,
    ('home', 'hero_title'): 'Professional Welding Services in Poole',
    ('home', 'hero_text'): (
        'Certified welding, metal structures, and fabrication for demanding industrial '
        'projects. Built for durability, engineered with precision.'
    ),
    ('home', 'hero_image'): 'images/hero-home.png',
    ('home', 'hero_image_alt'): (
        'Skilled welder at work with sparks — professional welding services Poole UK'
    ),
    ('home', 'hero_cta_primary'): 'Request a Quote',
    ('home', 'hero_cta_secondary'): 'Call Now',
    ('home', 'meta_title'): 'Professional Welding Services in Poole',
    ('home', 'meta_description'): (
        'Certified welding, metal structures, and fabrication for demanding '
        'industrial projects. Request a quote from KHODAK Metal Solution.'
    ),
    ('home', 'value_grid_section_visible'): VISIBILITY_ON,
    ('home', 'value_grid_title'): 'Structural Integrity Guaranteed',
    ('home', 'value_card_1_num'): '01 // Expertise',
    ('home', 'value_card_1_title'): 'Certified Specialists',
    ('home', 'value_card_1_text'): (
        'AWS D1.1 certified welders with coded qualifications across TIG, MIG, and '
        'electrode processes for structural and precision work.'
    ),
    ('home', 'value_card_2_num'): '02 // Capability',
    ('home', 'value_card_2_title'): 'Industrial Equipment',
    ('home', 'value_card_3_num'): '03 // Speed',
    ('home', 'value_card_3_title'): 'Fast Response',
    ('home', 'value_card_4_num'): '04 // Assurance',
    ('home', 'value_card_4_title'): 'Quality Guarantee',
    ('home', 'value_card_5_num'): '05 // Transparency',
    ('home', 'value_card_5_title'): 'Transparent Pricing',
    ('home', 'showcase_section_visible'): VISIBILITY_ON,
    ('home', 'showcase_title'): 'Engineering Showcase',
    ('home', 'showcase_link_text'): 'View All Projects →',
    ('home', 'showcase_card_1_image'): 'images/project-frame.png',
    ('home', 'showcase_card_1_image_alt'): (
        'Heavy industrial steel frame installation — structural welding Poole'
    ),
    ('home', 'showcase_card_1_category'): 'Structural Installation',
    ('home', 'showcase_card_1_title'): 'Heavy Industrial Frame',
    ('home', 'showcase_card_2_image'): 'images/home-showcase-tig.png',
    ('home', 'showcase_card_2_image_alt'): (
        'Stainless steel TIG weld joint — precision welding UK'
    ),
    ('home', 'showcase_card_2_category'): 'Precision Welding',
    ('home', 'showcase_card_2_title'): 'Stainless Steel TIG Joint',
    ('home', 'showcase_view_btn'): 'View Project',
    ('site', 'header_logo_image'): 'images/logo-khodak.png',
    ('site', 'header_nav_services_label'): 'Services',
    ('site', 'header_nav_portfolio_label'): 'Portfolio',
    ('site', 'header_nav_about_label'): 'About',
    ('site', 'header_nav_blog_label'): 'Blog',
    ('site', 'header_nav_contact_label'): 'Contact',
    ('site', 'header_nav_services_visible'): VISIBILITY_ON,
    ('site', 'header_nav_portfolio_visible'): VISIBILITY_ON,
    ('site', 'header_nav_about_visible'): VISIBILITY_ON,
    ('site', 'header_nav_blog_visible'): VISIBILITY_ON,
    ('site', 'header_nav_contact_visible'): VISIBILITY_ON,
    ('site', 'header_cta_text'): 'Request a Quote',
    ('site', 'header_cta_visible'): VISIBILITY_ON,
    ('site', 'footer_section_visible'): VISIBILITY_ON,
    ('site', 'footer_tagline'): 'Professional welding and fabrication services in Poole, Dorset.',
    ('site', 'footer_bottom_text'): 'Built for Durability.',
    ('site', 'footer_logo_image'): 'images/logo-khodak.png',
    ('site', 'quote_modal_section_visible'): VISIBILITY_ON,
    ('site', 'quote_modal_eyebrow'): 'Book a Service',
    ('site', 'quote_modal_title'): 'Request a Quote',
    ('site', 'quote_modal_lead'): (
        'Tell us about your project — we respond within one business day.'
    ),
    ('site', 'quote_modal_submit_label'): 'Submit Enquiry',
    ('about', 'hero_section_visible'): VISIBILITY_ON,
    ('about', 'hero_eyebrow'): 'About Us',
    ('about', 'hero_title'): 'Engineering Integrity. Since 2014.',
    ('about', 'hero_lead'): (
        'Built on precision, reliability, and heavy-duty performance — structural excellence '
        'from bespoke fabrication to on-site installation across the UK.'
    ),
    ('about', 'hero_image'): 'images/hero-about.png',
    ('about', 'hero_image_alt'): (
        'Structural engineer inspecting steel framework — KHODAK Metal Solution About Us'
    ),
    ('about', 'meta_title'): 'About Us — Engineering Integrity Since 2014',
    ('about', 'meta_description'): (
        'KHODAK Metal Solution delivers structural excellence across critical '
        'industrial sectors. Precision engineering, certified safety, premium craftsmanship.'
    ),
    ('about', 'story_section_visible'): VISIBILITY_ON,
    ('about', 'story_eyebrow'): 'Our Story',
    ('about', 'story_title'): 'The Structural Foundation',
    ('about', 'story_col_1'): (
        'What began as a specialised welding shop in Poole has evolved into a leading '
        'structural engineering contractor serving clients across the United Kingdom. '
        'Our growth reflects a commitment to measurable quality — every joint inspected, '
        'every frame aligned to blueprint tolerance.'
    ),
    ('about', 'story_col_2'): (
        'Today we operate a fully equipped fabrication facility with CNC cutting, heavy '
        'lifting capacity, and coded welding teams certified to AWS D1.1 and ISO 9001 '
        'standards. From first drawing review to final sign-off, each project follows '
        'documented procedures and traceable inspection records.'
    ),
    ('about', 'story_col_3'): (
        'We partner with architects, main contractors, and industrial operators on '
        'structural steelwork, bespoke metalwork, and on-site installation nationwide. '
        'Whether the brief is a single fabrication run or a multi-phase build programme, '
        'our engineers scope, quote, and deliver with the same rigour applied on day one.'
    ),
    ('about', 'imperatives_section_visible'): VISIBILITY_ON,
    ('about', 'imperatives_title'): 'Core Imperatives',
    ('about', 'imperative_1_title'): 'Precision Engineering',
    ('about', 'imperative_1_text'): (
        'Micrometer-level accuracy on every cut, weld, and assembly — measured against '
        'original blueprint specifications.'
    ),
    ('about', 'imperative_2_title'): 'Certified Safety',
    ('about', 'imperative_2_text'): (
        'International safety protocols enforced on every site, with full stress testing '
        'and documentation for structural compliance.'
    ),
    ('about', 'imperative_3_title'): 'Premium Craftsmanship',
    ('about', 'imperative_3_text'): (
        'Industrial strength meets refined finish — welds that perform under load and meet '
        'the highest aesthetic standards.'
    ),
    ('services', 'hero_section_visible'): VISIBILITY_ON,
    ('services', 'hero_eyebrow'): 'Core Competencies',
    ('services', 'hero_title'): 'Precision Engineering. Heavy-Duty Execution.',
    ('services', 'hero_lead'): (
        'From blueprint analysis to on-site installation, we deliver end-to-end metal '
        'fabrication services engineered for structural integrity and long-term performance.'
    ),
    ('services', 'hero_image'): 'images/tig-weld.png',
    ('services', 'hero_image_alt'): (
        'High-quality TIG weld on curved metal pipe — KHODAK welding services'
    ),
    ('services', 'default_hero_image'): 'images/tig-weld.png',
    ('services', 'meta_title'): 'Welding & Fabrication Services',
    ('services', 'meta_description'): (
        'Precision engineering and heavy-duty execution. Welding, structure '
        'installation, manufacturing, TIG, electrode welding, and metal repair.'
    ),
    ('services', 'catalog_section_visible'): VISIBILITY_ON,
    ('services', 'catalog_title'): 'Service Catalog',
    ('services', 'catalog_intro'): (
        'We execute blueprints with measurable precision — every service documented, '
        'every deliverable inspected.'
    ),
    ('services', 'timeline_section_visible'): VISIBILITY_ON,
    ('services', 'timeline_title'): 'How We Work',
    ('services', 'timeline_step_1_title'): 'Blueprint Analysis',
    ('services', 'timeline_step_1_text'): (
        'Engineering team reviews CAD/PDF specifications, identifies material requirements, '
        'and confirms weld procedures before fabrication begins.'
    ),
    ('services', 'timeline_step_1_image'): 'images/workshop.png',
    ('services', 'timeline_step_2_title'): 'Fabrication Phase',
    ('services', 'timeline_step_2_text'): (
        'CNC cutting, forming, and coded welding in our controlled workshop environment '
        'with full quality inspection at each stage.'
    ),
    ('services', 'timeline_step_2_image'): 'images/workshop.png',
    ('services', 'timeline_step_3_title'): 'On-Site Execution',
    ('services', 'timeline_step_3_text'): (
        'Certified installation crews mobilise with lifting equipment and site-specific '
        'safety protocols for structural erection and final commissioning.'
    ),
    ('services', 'timeline_step_3_image'): 'images/project-frame.png',
    ('services', 'spec_form_section_visible'): VISIBILITY_ON,
    ('services', 'spec_form_title'): 'Submit Specifications',
    ('services', 'spec_form_intro'): (
        'Transmit your project details for engineering review. Our team responds within '
        'one business day with a scope assessment and quote.'
    ),
    ('services', 'spec_form_check_1'): 'ISO 9001 Quality Management',
    ('services', 'spec_form_check_2'): 'AWS D1.1 Structural Welding',
    ('services', 'spec_form_check_3'): 'Coded Welder Qualifications',
    ('services', 'spec_form_bg_image'): 'images/workshop.png',
    ('portfolio', 'hero_section_visible'): VISIBILITY_ON,
    ('portfolio', 'hero_eyebrow'): 'Portfolio',
    ('portfolio', 'hero_title'): 'Our Work.',
    ('portfolio', 'hero_lead'): (
        'A showcase of structural integrity and precision engineering. From heavy industrial '
        'frameworks to meticulous residential repairs, explore the projects built to last.'
    ),
    ('portfolio', 'hero_image'): 'images/hero-portfolio.png',
    ('portfolio', 'hero_image_alt'): (
        'Fabrication workshop with completed steel structures — KHODAK portfolio'
    ),
    ('portfolio', 'meta_title'): 'Our Work — Engineering Portfolio',
    ('portfolio', 'meta_description'): (
        'A showcase of structural integrity and precision engineering. '
        'Explore industrial, commercial, and residential metal fabrication projects.'
    ),
    ('blog', 'hero_section_visible'): VISIBILITY_ON,
    ('blog', 'hero_eyebrow'): 'Engineering Insights',
    ('blog', 'hero_title'): 'Technical Articles & Welding Standards.',
    ('blog', 'hero_lead'): (
        'Expert guides on structural integrity, precision welding techniques, and '
        'industrial fabrication standards.'
    ),
    ('blog', 'hero_image'): 'images/hero-blog.png',
    ('blog', 'hero_image_alt'): (
        'Welding standards and technical blueprints — KHODAK engineering blog'
    ),
    ('blog', 'meta_title'): 'Engineering Insights & Welding Technologies',
    ('blog', 'meta_description'): (
        'Expert guides on structural integrity, precision welding techniques, and '
        'industrial fabrication standards from the KHODAK engineering team.'
    ),
    ('faq', 'hero_section_visible'): VISIBILITY_ON,
    ('faq', 'hero_eyebrow'): 'Support',
    ('faq', 'hero_title'): 'Frequently Asked Questions.',
    ('faq', 'hero_lead'): (
        'Answers to common questions about our welding services, certifications, and '
        'project process.'
    ),
    ('faq', 'hero_image'): 'images/hero-faq.png',
    ('faq', 'hero_image_alt'): (
        'Welding quality inspection — KHODAK Metal Solution FAQ and support'
    ),
    ('faq', 'meta_title'): 'Frequently Asked Questions',
    ('faq', 'meta_description'): (
        'Answers to common questions about welding certifications, project types, '
        'response times, and service areas from KHODAK Metal Solution.'
    ),
    ('contact', 'page_section_visible'): VISIBILITY_ON,
    ('contact', 'contact_eyebrow'): 'Get in Touch',
    ('contact', 'contact_title'): 'Contact Our Workshop.',
    ('contact', 'contact_lead'): (
        'Submit project specifications or reach our Poole workshop. '
        'We respond within one business day.'
    ),
    ('contact', 'hero_image'): 'images/hero-contact.png',
    ('contact', 'hero_image_alt'): (
        'Project specification review at KHODAK Metal Solution — contact our workshop'
    ),
    ('contact', 'contact_figcaption'): 'Certified teams · AWS D1.1 · ISO 9001',
    ('contact', 'contact_hours'): 'Mon–Fri 07:00–17:00',
    ('contact', 'meta_title'): 'Contact — Request a Quote',
    ('contact', 'meta_description'): (
        'Get in touch with KHODAK Metal Solution. Submit project specifications '
        'or call our Poole workshop for professional welding services.'
    ),
    ('privacy', 'content_section_visible'): VISIBILITY_ON,
    ('privacy', 'privacy_title'): 'Privacy Policy',
    ('privacy', 'privacy_updated'): 'Last updated: 26 June 2026',
    ('privacy', 'privacy_body'): PRIVACY_BODY_DEFAULT,
    ('privacy', 'meta_title'): 'Privacy Policy',
    ('privacy', 'meta_description'): (
        'How KHODAK Metal Solution collects, uses, and protects your personal data '
        'under UK GDPR when you use our website or submit an enquiry.'
    ),
    ('terms', 'content_section_visible'): VISIBILITY_ON,
    ('terms', 'terms_title'): 'Terms of Service',
    ('terms', 'terms_updated'): 'Last updated: 26 June 2026',
    ('terms', 'terms_body'): TERMS_BODY_DEFAULT,
    ('terms', 'meta_title'): 'Terms of Service',
    ('terms', 'meta_description'): (
        'Terms of service for using the KHODAK Metal Solution website and engaging '
        'our welding, fabrication, and installation services in the UK.'
    ),
}


def block_label(page: str, key: str) -> str:
    if (page, key) in BLOCK_FIELD_LABELS:
        return BLOCK_FIELD_LABELS[(page, key)]
    if is_visibility_key(key):
        return key.replace('_', ' ').title()
    return key.replace('_', ' ').title()


def block_content_type(page: str, key: str) -> str:
    return BLOCK_CONTENT_TYPES.get((page, key), 'text')


def default_for_block(page: str, key: str) -> str:
    if (page, key) in BLOCK_DEFAULTS:
        return BLOCK_DEFAULTS[(page, key)]
    if is_visibility_key(key):
        return VISIBILITY_ON
    return ''
