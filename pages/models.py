from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=120, default='KHODAK Metal Solution')
    site_short = models.CharField(max_length=40, default='KHODAK')
    site_tagline = models.CharField(max_length=200, default='Built for Durability. Engineered with Precision.')
    site_description = models.TextField(
        default=(
            'Certified welding, metal structures, and fabrication for demanding '
            'industrial projects in Poole and across the UK.'
        ),
    )
    site_url = models.URLField(default='https://khodakmetal.com')
    site_phone = models.CharField(max_length=30, default='+44 7704 039508')
    site_email = models.EmailField(default='khodakmetalsolution@gmail.com')
    site_address = models.CharField(
        max_length=200,
        default='564 Ashley Rd, Poole BH14 0AG, United Kingdom',
    )
    site_year = models.PositiveIntegerField(default=2024)

    class Meta:
        verbose_name = 'Налаштування сайту'
        verbose_name_plural = 'Налаштування сайту'

    def __str__(self):
        return self.site_name

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Service(models.Model):
    ICON_CHOICES = [
        ('robot', 'Robot'),
        ('wrench', 'Wrench'),
        ('factory', 'Factory'),
        ('flame', 'Flame'),
        ('bolt', 'Bolt'),
        ('repair', 'Repair'),
    ]

    slug = models.SlugField(unique=True, max_length=80)
    code = models.CharField(max_length=20, blank=True)
    title = models.CharField(max_length=120)
    short = models.TextField()
    body = models.TextField(blank=True)
    icon = models.CharField(max_length=20, choices=ICON_CHOICES, default='wrench')
    sort_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', 'title']
        verbose_name = 'Послуга'
        verbose_name_plural = 'Послуги'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class PortfolioItem(models.Model):
    CATEGORY_CHOICES = [
        ('industrial', 'Industrial'),
        ('commercial', 'Commercial'),
        ('repairs', 'Repairs'),
        ('residential', 'Residential'),
    ]

    slug = models.SlugField(unique=True, max_length=80)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    detail = models.CharField(max_length=120)
    static_image = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='portfolio/', blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', 'title']
        verbose_name = 'Робота портфоліо'
        verbose_name_plural = 'Портфоліо'

    def __str__(self):
        return self.title

    @property
    def image_filename(self):
        return self.static_image or 'placeholder.png'


class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('technology', 'Technology'),
        ('materials', 'Materials'),
        ('safety', 'Safety'),
    ]

    slug = models.SlugField(unique=True, max_length=120)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    excerpt = models.TextField()
    body = models.TextField(blank=True)
    published_at = models.DateField(default=timezone.now)
    is_featured = models.BooleanField(default=False)
    static_image = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='blog/', blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_at', 'title']
        verbose_name = 'Стаття блогу'
        verbose_name_plural = 'Блог'

    def __str__(self):
        return self.title

    @property
    def date(self):
        return self.published_at.isoformat()

    @property
    def date_display(self):
        return self.published_at.strftime('%b %d, %Y')

    @property
    def featured(self):
        return self.is_featured

    @property
    def image_filename(self):
        return self.static_image or 'placeholder.png'


class FAQItem(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', 'question']
        verbose_name = 'Питання FAQ'
        verbose_name_plural = 'FAQ'

    def __str__(self):
        return self.question


class QuoteRequest(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'Нова'
        IN_PROGRESS = 'in_progress', 'В обробці'
        CLOSED = 'closed', 'Закрита'

    name = models.CharField(max_length=80, verbose_name="ім'я")
    phone = models.CharField(max_length=30, verbose_name='телефон')
    email = models.EmailField(blank=True, verbose_name='email')
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='quote_requests',
        verbose_name='послуга',
    )
    message = models.TextField(blank=True, verbose_name='повідомлення')
    privacy_accepted = models.BooleanField(default=False, verbose_name='згода на обробку даних')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name='статус',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата заявки')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'{self.name} — {self.created_at:%Y-%m-%d}'


class SiteBlock(models.Model):
    class Page(models.TextChoices):
        HOME = 'home', 'Головна'
        ABOUT = 'about', 'Про нас'
        SERVICES = 'services', 'Послуги'
        PORTFOLIO = 'portfolio', 'Портфоліо'
        BLOG = 'blog', 'Блог'
        FAQ = 'faq', 'FAQ'
        CONTACT = 'contact', 'Контакти'
        PRIVACY = 'privacy', 'Privacy'
        TERMS = 'terms', 'Terms'
        SITE = 'site', 'Сайт'

    class ContentType(models.TextChoices):
        TEXT = 'text', 'Текст'
        IMAGE = 'image', 'Фото'

    page = models.CharField(max_length=32, choices=Page.choices)
    key = models.CharField(max_length=64)
    label = models.CharField(max_length=128)
    content_type = models.CharField(
        max_length=16,
        choices=ContentType.choices,
        default=ContentType.TEXT,
    )
    text_html = models.TextField(blank=True)
    image = models.ImageField(upload_to='blocks/', blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['page', 'sort_order', 'key']
        verbose_name = 'CMS блок'
        verbose_name_plural = 'CMS блоки'
        constraints = [
            models.UniqueConstraint(
                fields=['page', 'key'],
                name='unique_site_block_page_key',
            ),
        ]

    def __str__(self):
        return f'{self.page}.{self.key}'

    @property
    def cache_key(self) -> str:
        return f'{self.page}.{self.key}'


class HomeHeroSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Головна — Верхній банер'
        verbose_name_plural = 'Головна — Верхній банер'


class HomeValueGridSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Головна — Переваги'
        verbose_name_plural = 'Головна — Переваги'


class HomeShowcaseSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Головна — Проєкти'
        verbose_name_plural = 'Головна — Проєкти'


class SiteHeaderSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Шапка сайту'
        verbose_name_plural = 'Шапка сайту'


class SiteFooterSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Підвал сайту'
        verbose_name_plural = 'Підвал сайту'


class SiteQuoteModalSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Вікно заявки'
        verbose_name_plural = 'Вікно заявки'


class AboutHeroSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Про нас — Верхній банер'
        verbose_name_plural = 'Про нас — Верхній банер'


class AboutStorySettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Про нас — Наша історія'
        verbose_name_plural = 'Про нас — Наша історія'


class AboutImperativesSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Про нас — Цінності'
        verbose_name_plural = 'Про нас — Цінності'


class ServicesHeroSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Послуги — Верхній банер'
        verbose_name_plural = 'Послуги — Верхній банер'


class ServicesCatalogSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Послуги — Каталог'
        verbose_name_plural = 'Послуги — Каталог'


class ServicesTimelineSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Послуги — Як ми працюємо'
        verbose_name_plural = 'Послуги — Як ми працюємо'


class ServicesSpecFormSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Послуги — Форма специфікацій'
        verbose_name_plural = 'Послуги — Форма специфікацій'


class PortfolioHeroSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Портфоліо — Верхній банер'
        verbose_name_plural = 'Портфоліо — Верхній банер'


class BlogHeroSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Блог — Верхній банер'
        verbose_name_plural = 'Блог — Верхній банер'


class FaqHeroSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'FAQ — Верхній банер'
        verbose_name_plural = 'FAQ — Верхній банер'


class ContactPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Контакти'
        verbose_name_plural = 'Контакти'


class PrivacyPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Політика конфіденційності'
        verbose_name_plural = 'Політика конфіденційності'


class TermsPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Умови використання'
        verbose_name_plural = 'Умови використання'
