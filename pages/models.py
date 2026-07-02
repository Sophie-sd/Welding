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
        verbose_name = 'Site settings'
        verbose_name_plural = 'Site settings'

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
        verbose_name = 'FAQ item'
        verbose_name_plural = 'FAQ items'

    def __str__(self):
        return self.question


class QuoteRequest(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'New'
        IN_PROGRESS = 'in_progress', 'In progress'
        CLOSED = 'closed', 'Closed'

    name = models.CharField(max_length=80)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='quote_requests',
    )
    message = models.TextField(blank=True)
    privacy_accepted = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.created_at:%Y-%m-%d}'
