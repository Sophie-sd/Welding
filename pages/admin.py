from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from tinymce.widgets import TinyMCE
from unfold.admin import ModelAdmin

from .models import BlogPost, FAQItem, PortfolioItem, QuoteRequest, Service, SiteSettings

TINYMCE_FIELDS = frozenset({'body', 'answer'})


def new_quote_requests_badge(request):
    count = QuoteRequest.objects.filter(status=QuoteRequest.Status.NEW).count()
    return count if count else ''


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
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

    def changelist_view(self, request, extra_context=None):
        obj, _ = SiteSettings.objects.get_or_create(pk=1)
        return HttpResponseRedirect(
            reverse('admin:pages_sitesettings_change', args=[obj.pk]),
        )


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
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(PortfolioItem)
class PortfolioItemAdmin(ModelAdmin):
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

    @admin.display(description='Превʼю')
    def get_image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-height:120px;border-radius:6px;" />',
                obj.image.url,
            )
        return '—'


@admin.register(BlogPost)
class BlogPostAdmin(ModelAdmin):
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
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    @admin.display(description='Превʼю')
    def get_image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-height:120px;border-radius:6px;" />',
                obj.image.url,
            )
        return '—'


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
        return super().formfield_for_dbfield(db_field, request, **kwargs)


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
