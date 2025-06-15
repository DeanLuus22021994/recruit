"""Utility functions for SendGrid integration."""

import logging
from datetime import timedelta
from typing import Any, Dict, Optional

from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models import Count, Q
from django.template import Context, Template
from django.template.exceptions import TemplateDoesNotExist, TemplateSyntaxError
from django.utils import timezone
from django.utils.html import strip_tags

# Import models with proper typing
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import EmailLog, EmailTemplate
else:
    # Import at runtime for Django ORM functionality
    from .models import EmailLog, EmailTemplate

logger = logging.getLogger(__name__)


def send_template_email(
    template_name: str,
    recipient_email: str,
    context: Optional[Dict[str, Any]] = None,
    sender_email: Optional[str] = None,
    fail_silently: bool = False,
) -> bool:
    """Send an email using a predefined template."""
    try:
        template = EmailTemplate.objects.get(name=template_name, is_active=True)
    except EmailTemplate.DoesNotExist:
        logger.error("Email template '%s' not found or inactive", template_name)
        if not fail_silently:
            raise
        return False

    context = context or {}
    sender_email = sender_email or getattr(
        settings, "DEFAULT_FROM_EMAIL", "noreply@example.com"
    )

    # Render template content
    try:
        if template.html_content:
            html_content = render_to_string_from_text(template.html_content, context)
        else:
            html_content = None

        if template.plain_content:
            plain_content = render_to_string_from_text(template.plain_content, context)
        elif html_content:
            plain_content = strip_tags(html_content)
        else:
            plain_content = None

        subject = render_to_string_from_text(template.subject, context)

    except (TemplateSyntaxError, TemplateDoesNotExist) as e:
        logger.error("Error rendering template '%s': %s", template_name, e)
        if not fail_silently:
            raise
        return False  # Create and send email
    try:
        email = EmailMessage(
            subject=subject,
            body=html_content or plain_content,
            from_email=sender_email,
            to=[recipient_email],
        )

        if html_content:
            email.content_subtype = "html"

        sent = email.send()

        # Log the email
        EmailLog.objects.create(
            recipient=recipient_email,
            sender=sender_email,
            subject=subject,
            template=template,
            status="sent" if sent else "failed",
        )

        return bool(sent)

    except (OSError, ValueError) as e:
        logger.error("Error sending email to %s: %s", recipient_email, e)

        # Log the failed attempt
        EmailLog.objects.create(
            recipient=recipient_email,
            sender=sender_email,
            subject=subject or f"Email from template {template_name}",
            template=template,
            status="failed",
            error_message=str(e),
        )

        if not fail_silently:
            raise
        return False


def render_to_string_from_text(template_string: str, context: Dict[str, Any]) -> str:
    """Render a template string with context variables."""
    template = Template(template_string)
    return template.render(Context(context))


def get_email_statistics(days: int = 30) -> Dict[str, Any]:
    """Get email sending statistics for the last N days."""
    start_date = timezone.now() - timedelta(days=days)

    stats = EmailLog.objects.filter(sent_at__gte=start_date).aggregate(
        total_sent=Count("id"),
        delivered=Count("id", filter=Q(status="delivered")),
        failed=Count("id", filter=Q(status="failed")),
        bounced=Count("id", filter=Q(status="bounced")),
        spam=Count("id", filter=Q(status="spam")),
    )

    return {
        "period_days": days,
        "total_sent": stats["total_sent"] or 0,
        "delivered": stats["delivered"] or 0,
        "failed": stats["failed"] or 0,
        "bounced": stats["bounced"] or 0,
        "spam": stats["spam"] or 0,
        "delivery_rate": (
            (stats["delivered"] / stats["total_sent"] * 100)
            if stats["total_sent"]
            else 0
        ),
    }
