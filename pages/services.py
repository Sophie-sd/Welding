import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def notify_quote_request(quote):
    subject = f'New quote request from {quote.name}'
    service_title = quote.service.title if quote.service else 'Not specified'
    body = (
        f'Name: {quote.name}\n'
        f'Phone: {quote.phone}\n'
        f'Email: {quote.email or "—"}\n'
        f'Service: {service_title}\n\n'
        f'Message:\n{quote.message or "—"}\n'
    )
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.QUOTE_NOTIFICATION_EMAIL],
            fail_silently=False,
        )
    except Exception:
        logger.exception(
            'Failed to send quote notification for request id=%s',
            quote.pk,
        )
