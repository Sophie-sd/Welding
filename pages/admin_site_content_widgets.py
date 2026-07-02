from django import forms
from django.contrib.admin.widgets import AdminTextInputWidget, AdminTextareaWidget
from unfold.widgets import INPUT_CLASSES, TEXTAREA_CLASSES

_SKIP_CLASSES = frozenset({
    'bg-white',
    'text-font-default-light',
    'border-base-200',
    'dark:bg-base-900',
    'dark:border-base-700',
    'dark:text-font-default-dark',
})
_FORCE_CLASSES = ('bg-base-900', 'text-base-100', 'border-base-700', 'placeholder-base-400')


def cms_control_classes(base_classes: list[str]) -> str:
    filtered = [css_class for css_class in base_classes if css_class not in _SKIP_CLASSES]
    return ' '.join([*filtered, *_FORCE_CLASSES])


class CmsAdminTextInputWidget(AdminTextInputWidget):
    def __init__(self, attrs=None):
        super().__init__(attrs={
            **(attrs or {}),
            'class': cms_control_classes([*INPUT_CLASSES, (attrs or {}).get('class', '')]),
        })


class CmsAdminTextareaWidget(AdminTextareaWidget):
    def __init__(self, attrs=None, rows=2):
        super().__init__(attrs={
            **(attrs or {}),
            'rows': rows,
            'class': cms_control_classes([*TEXTAREA_CLASSES, (attrs or {}).get('class', '')]),
        })


def apply_readable_widget(field):
    widget = field.widget
    if isinstance(widget, (forms.CheckboxInput, forms.Select, forms.FileInput)):
        return field
    if getattr(widget, 'mce_settings', None):
        return field
    if isinstance(widget, AdminTextareaWidget):
        field.widget = CmsAdminTextareaWidget(rows=getattr(widget.attrs, 'rows', 2))
    elif isinstance(widget, AdminTextInputWidget):
        field.widget = CmsAdminTextInputWidget()
    return field
