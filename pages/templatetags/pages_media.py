from django import template
from django.templatetags.static import static

register = template.Library()


@register.simple_tag
def content_image(obj):
    image_field = getattr(obj, 'image', None)
    if image_field and getattr(image_field, 'name', None):
        return image_field.url

    filename = getattr(obj, 'static_image', '') or getattr(obj, 'image_filename', 'placeholder.png')
    return static(f'images/{filename}')
