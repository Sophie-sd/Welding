from django import template

from pages.forms import QuoteForm
from pages.models import Service

register = template.Library()


@register.inclusion_tag('partials/quote_form.html', takes_context=True)
def quote_form(context, compact=False, id_prefix='quote', submit_label='Transmit Data', selected_service=''):
    form = context.get('form') or context.get('quote_form')
    service_slug = selected_service or context.get('selected_service', '')

    if form is None:
        initial = {}
        if service_slug:
            service = Service.objects.filter(slug=service_slug, is_published=True).first()
            if service:
                initial['service'] = service
        form = QuoteForm(initial=initial, id_prefix=id_prefix, compact=compact)

    return {
        'form': form,
        'compact': compact,
        'id_prefix': id_prefix,
        'submit_label': submit_label,
        'selected_service': service_slug,
    }
