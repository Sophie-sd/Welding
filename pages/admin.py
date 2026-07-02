from django.contrib import admin
from tinymce.widgets import TinyMCE
from unfold.admin import ModelAdmin

from .admin_site_content_proxies import register_site_content_section_admins
from .admin_utils import (
    AdminImageWebpMixin,
    ImagePreviewMixin,
    ReadableUnfoldFieldsMixin,
    SingletonModelAdminMixin,
)
from .cms_field_hints import get_model_image_hint
from .models import BlogPost, FAQItem, PortfolioItem, QuoteRequest, Service, SiteSettings

TINYMCE_FIELDS = frozenset({'body', 'answer'})

MODEL_FIELD_HELP = {
    'title': 'Заголовок. Не перевищуйте рекомендовану довжину для коректного відображення.',
    'short': 'Короткий опис послуги. Рекомендовано до 240 символів.',
    'excerpt': 'Короткий опис статті. Рекомендовано до 240 символів.',
    'question': 'Питання FAQ. Максимум 255 символів.',
    'answer': 'Відповідь FAQ. Рекомендовано лаконічний текст до 600 символів.',
    'location': 'Локація проєкту. Максимум 120 символів.',
    'detail': 'Додаткова мітка проєкту. Максимум 120 символів.',
    'static_image': 'Імʼя файлу в static/images/ як резерв, якщо не завантажено media-зображення.',
    'image': get_model_image_hint(),
}

register_site_content_section_admins()


def apply_model_field_help(formfield, field_name: str):
    help_text = MODEL_FIELD_HELP.get(field_name)
    if help_text and formfield is not None:
        formfield.help_text = help_text
    return formfield


def new_quote_requests_badge(request):
    count = QuoteRequest.objects.filter(status=QuoteRequest.Status.NEW).count()
    return count if count else ''


@admin.register(SiteSettings)
class SiteSettingsAdmin(ReadableUnfoldFieldsMixin, SingletonModelAdminMixin, ModelAdmin):
    fieldsets = (
        ('Бренд', {
            'fields': (
                'site_name',
                'site_short',
                'site_tagline',
                'site_description',
                'site_year',
            ),
        }),
        ('Контакти', {
            'fields': ('site_url', 'site_phone', 'site_email', 'site_address'),
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ('title', 'code', 'slug', 'sort_order', 'is_published')
    list_editable = ('sort_order', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'code')
    fieldsets = (
        ('Основне', {
            'fields': ('title', 'code', 'slug', 'icon', 'short', 'body'),
        }),
        ('Публікація', {
            'fields': ('sort_order', 'is_published'),
        }),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in TINYMCE_FIELDS:
            kwargs['widget'] = TinyMCE()
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        return apply_model_field_help(formfield, db_field.name)


@admin.register(PortfolioItem)
class PortfolioItemAdmin(AdminImageWebpMixin, ImagePreviewMixin, ModelAdmin):
    list_display = (
        'title',
        'category',
        'location',
        'get_image_preview',
        'sort_order',
        'is_published',
    )
    list_editable = ('sort_order', 'is_published')
    list_filter = ('category', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('get_image_preview',)
    fieldsets = (
        ('Основне', {
            'fields': ('title', 'slug', 'category', 'location', 'detail'),
        }),
        ('Зображення', {
            'fields': ('static_image', 'image', 'get_image_preview'),
        }),
        ('Публікація', {
            'fields': ('sort_order', 'is_published'),
        }),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        return apply_model_field_help(formfield, db_field.name)

    @admin.display(description='Превʼю')
    def get_image_preview(self, obj):
        return ImagePreviewMixin.get_image_preview(self, obj)


@admin.register(BlogPost)
class BlogPostAdmin(AdminImageWebpMixin, ImagePreviewMixin, ModelAdmin):
    list_display = (
        'title',
        'category',
        'published_at',
        'get_image_preview',
        'is_featured',
        'is_published',
    )
    list_editable = ('is_featured', 'is_published')
    list_filter = ('category', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    readonly_fields = ('get_image_preview',)
    fieldsets = (
        ('Основне', {
            'fields': ('title', 'slug', 'category', 'excerpt', 'body'),
        }),
        ('Зображення', {
            'fields': ('static_image', 'image', 'get_image_preview'),
        }),
        ('Публікація', {
            'fields': ('published_at', 'is_featured', 'is_published'),
        }),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in TINYMCE_FIELDS:
            kwargs['widget'] = TinyMCE()
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        return apply_model_field_help(formfield, db_field.name)

    @admin.display(description='Превʼю')
    def get_image_preview(self, obj):
        return ImagePreviewMixin.get_image_preview(self, obj)


@admin.register(FAQItem)
class FAQItemAdmin(ModelAdmin):
    list_display = ('question', 'sort_order', 'is_published')
    list_editable = ('sort_order', 'is_published')
    fieldsets = (
        ('Основне', {
            'fields': ('question', 'answer'),
        }),
        ('Публікація', {
            'fields': ('sort_order', 'is_published'),
        }),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in TINYMCE_FIELDS:
            kwargs['widget'] = TinyMCE()
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        return apply_model_field_help(formfield, db_field.name)


@admin.register(QuoteRequest)
class QuoteRequestAdmin(ModelAdmin):
    list_display = ('name', 'phone', 'email', 'service', 'status', 'created_at')
    list_editable = ('status',)
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'phone', 'email', 'message')
    readonly_fields = (
        'name',
        'phone',
        'email',
        'service',
        'message',
        'privacy_accepted',
        'created_at',
    )
    fieldsets = (
        ('Клієнт', {
            'fields': ('name', 'phone', 'email'),
        }),
        ('Заявка', {
            'fields': ('service', 'message', 'privacy_accepted'),
        }),
        ('Статус', {
            'fields': ('status', 'created_at'),
        }),
    )

    def has_add_permission(self, request):
        return False
