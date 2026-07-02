from django.http import HttpResponseRedirect
from django.urls import reverse
from unfold.admin import ModelAdmin

from .admin_site_content_widgets import apply_readable_widget


class SingletonModelAdminMixin:
    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        from .models import SiteSettings

        obj, _ = SiteSettings.objects.get_or_create(pk=1)
        opts = self.model._meta
        return HttpResponseRedirect(
            reverse(f'admin:{opts.app_label}_{opts.model_name}_change', args=[obj.pk]),
        )


class ReadableUnfoldFieldsMixin:
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if formfield is not None:
            apply_readable_widget(formfield)
        return formfield


class ImagePreviewMixin:
    image_field = 'image'

    def get_image_preview(self, obj):
        from django.utils.html import format_html

        image = getattr(obj, self.image_field, None)
        if obj and image:
            return format_html(
                '<img src="{}" style="max-height:120px;border-radius:6px;" />',
                image.url,
            )
        return '—'

    get_image_preview.short_description = 'Превʼю'
