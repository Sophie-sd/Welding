from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from unfold.admin import ModelAdmin

from .admin_site_content_widgets import apply_readable_widget
from .cms_field_hints import IMAGE_PROFILES, get_field_hint, get_model_image_hint
from .utils.image_upload import ImageUploadError, process_admin_image


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
        from django.templatetags.static import static
        from django.utils.html import format_html

        if not obj or not getattr(obj, 'pk', None):
            return '—'

        image = getattr(obj, self.image_field, None)
        if image and getattr(image, 'name', None):
            url = image.url
            source = 'media'
        else:
            filename = getattr(obj, 'static_image', '') or getattr(obj, 'image_filename', '')
            if not filename:
                return '—'
            url = static(f'images/{filename}')
            source = 'static'

        return format_html(
            '<div style="display:flex;flex-direction:column;gap:6px;">'
            '<img src="{}" alt="" style="max-height:160px;max-width:280px;'
            'border-radius:8px;border:1px solid #e5e7eb;object-fit:cover;" />'
            '<span style="font-size:12px;opacity:0.7;">{}</span>'
            '</div>',
            url,
            'Завантажене media-фото' if source == 'media' else f'Static: {filename}',
        )

    get_image_preview.short_description = 'Превʼю'


class AdminImageWebpMixin:
    admin_image_profile = 'content'
    admin_inline_image_field = 'image'

    def save_model(self, request, obj, form, change):
        uploaded = form.cleaned_data.get('image')
        if uploaded:
            try:
                obj.image = process_admin_image(uploaded, profile=self.admin_image_profile)
            except ImageUploadError as exc:
                messages.error(request, str(exc))
                return
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        from django.core.files.uploadedfile import UploadedFile

        for inline_form in formset.forms:
            if not getattr(inline_form, 'cleaned_data', None):
                continue
            if inline_form.cleaned_data.get('DELETE'):
                continue
            uploaded = inline_form.cleaned_data.get(self.admin_inline_image_field)
            if not isinstance(uploaded, UploadedFile):
                continue
            try:
                processed = process_admin_image(uploaded, profile=self.admin_image_profile)
                inline_form.cleaned_data[self.admin_inline_image_field] = processed
                inline_form.instance.image = processed
            except ImageUploadError as exc:
                messages.error(request, str(exc))
                return
        super().save_formset(request, form, formset, change)
