from django.contrib import admin

from .models import BlogPost, FAQItem, PortfolioItem, QuoteRequest, Service, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Brand', {'fields': ('site_name', 'site_short', 'site_tagline', 'site_description', 'site_year')}),
        ('Contact', {'fields': ('site_url', 'site_phone', 'site_email', 'site_address')}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'slug', 'sort_order', 'is_published')
    list_editable = ('sort_order', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'code')


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'sort_order', 'is_published')
    list_editable = ('sort_order', 'is_published')
    list_filter = ('category', 'is_published')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_at', 'is_featured', 'is_published')
    list_editable = ('is_featured', 'is_published')
    list_filter = ('category', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'sort_order', 'is_published')
    list_editable = ('sort_order', 'is_published')


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'service', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at',)
    search_fields = ('name', 'phone', 'email', 'message')
