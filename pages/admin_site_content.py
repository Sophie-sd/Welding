from django import forms
from django.contrib import admin, messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from tinymce.widgets import TinyMCE
from unfold.admin import ModelAdmin
from unfold.widgets import UnfoldAdminFileFieldWidget, UnfoldBooleanWidget

from .admin_utils import SingletonModelAdminMixin
from .block_defaults import (
    INLINE_KEYS,
    MULTILINE_KEYS,
    RICHTEXT_KEYS,
    block_content_type,
    block_label,
    default_for_block,
    is_visibility_key,
)
from .context_processors import SITE_BLOCKS_CACHE_KEY
from .models import SiteBlock, SiteSettings
from .site_content_registry import ContentSection, get_section, iter_section_blocks
from .admin_site_content_widgets import CmsAdminTextInputWidget, CmsAdminTextareaWidget


def block_field_name(page: str, key: str, suffix: str) -> str:
    return f'block__{page}__{key}__{suffix}'


def load_section_blocks(section: ContentSection) -> dict[tuple[str, str], SiteBlock]:
    blocks: dict[tuple[str, str], SiteBlock] = {}
    for index, (page, key) in enumerate(iter_section_blocks(section)):
        content_type = block_content_type(page, key)
        default_text = default_for_block(page, key)
        block, _ = SiteBlock.objects.get_or_create(
            page=page,
            key=key,
            defaults={
                'label': block_label(page, key),
                'content_type': content_type,
                'text_html': default_text if content_type == SiteBlock.ContentType.TEXT else default_text,
                'sort_order': index,
            },
        )
        blocks[(page, key)] = block
    return blocks


class SitePageContentForm(forms.Form):
    def __init__(self, *args, section: ContentSection, **kwargs):
        self.section = section
        self.blocks = load_section_blocks(section)
        super().__init__(*args, **kwargs)

        if section.visibility_key:
            visibility_block = self.blocks.get((section.page_slug, section.visibility_key))
            self.fields['section_visible'] = forms.BooleanField(
                label='Показувати секцію на сайті',
                required=False,
                initial=visibility_block.text_html not in {'0', 'false', 'False', ''} if visibility_block else True,
                widget=UnfoldBooleanWidget(),
            )

        for page, key in iter_section_blocks(section):
            if section.visibility_key and key == section.visibility_key:
                continue
            label = block_label(page, key)
            if is_visibility_key(key):
                block = self.blocks[(page, key)]
                self.fields[block_field_name(page, key, 'visible')] = forms.BooleanField(
                    label=label,
                    required=False,
                    initial=block.text_html not in {'0', 'false', 'False', ''},
                    widget=UnfoldBooleanWidget(),
                )
                continue

            content_type = block_content_type(page, key)
            if content_type == SiteBlock.ContentType.IMAGE:
                block = self.blocks[(page, key)]
                self.fields[block_field_name(page, key, 'image')] = forms.ImageField(
                    label=label,
                    required=False,
                    widget=UnfoldAdminFileFieldWidget(),
                )
                self.fields[block_field_name(page, key, 'static_path')] = forms.CharField(
                    label=f'{label} (static fallback)',
                    required=False,
                    initial=block.text_html,
                    widget=CmsAdminTextInputWidget(),
                )
                continue

            if key in RICHTEXT_KEYS:
                widget = TinyMCE()
            elif key in MULTILINE_KEYS:
                widget = CmsAdminTextareaWidget(rows=4)
            elif key in INLINE_KEYS:
                widget = CmsAdminTextInputWidget()
            else:
                widget = CmsAdminTextareaWidget(rows=2)

            self.fields[block_field_name(page, key, 'text_html')] = forms.CharField(
                label=label,
                required=False,
                initial=self.blocks[(page, key)].text_html,
                widget=widget,
            )

    def save(self):
        section = self.section
        if section.visibility_key:
            block = self.blocks[(section.page_slug, section.visibility_key)]
            block.text_html = '1' if self.cleaned_data.get('section_visible') else '0'
            block.save(update_fields=['text_html'])

        for page, key in iter_section_blocks(section):
            if section.visibility_key and key == section.visibility_key:
                continue
            block = self.blocks[(page, key)]
            if is_visibility_key(key):
                field_name = block_field_name(page, key, 'visible')
                block.text_html = '1' if self.cleaned_data.get(field_name) else '0'
                block.save(update_fields=['text_html'])
                continue

            if block_content_type(page, key) == SiteBlock.ContentType.IMAGE:
                image = self.cleaned_data.get(block_field_name(page, key, 'image'))
                static_path = self.cleaned_data.get(block_field_name(page, key, 'static_path'), '')
                if image:
                    block.image = image
                block.text_html = static_path or block.text_html
                block.save()
                continue

            text = self.cleaned_data.get(block_field_name(page, key, 'text_html'), '')
            block.text_html = text
            block.save(update_fields=['text_html'])

        cache.delete(SITE_BLOCKS_CACHE_KEY)


@staff_member_required
def site_content_section_view(request, page_slug, section_slug, model_admin=None):
    section = get_section(page_slug, section_slug)
    if model_admin is not None and not model_admin.has_change_permission(request):
        raise PermissionDenied

    opts = model_admin.model._meta if model_admin else SiteSettings._meta

    if request.method == 'POST':
        form = SitePageContentForm(request.POST, request.FILES, section=section)
        if form.is_valid():
            form.save()
            messages.success(request, 'Контент збережено.')
            return redirect(request.path)
    else:
        form = SitePageContentForm(section=section)

    context = {
        **admin.site.each_context(request),
        'form': form,
        'section': section,
        'title': section.title,
        'preview_url': section.preview_url,
        'opts': opts,
        'app_label': opts.app_label,
        'has_view_permission': True,
        'has_change_permission': True,
        'is_popup': False,
        'media': form.media,
    }
    return TemplateResponse(request, 'admin/pages/site_content_page.html', context)


class SiteContentSectionAdmin(SingletonModelAdminMixin, ModelAdmin):
    page_slug: str = ''
    section_slug: str = ''

    def has_add_permission(self, request):
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        return site_content_section_view(
            request,
            self.page_slug,
            self.section_slug,
            model_admin=self,
        )
