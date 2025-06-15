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

# Import models directly for proper Django ORM functionality and type hints
try:
    from .models import EmailLog, EmailTemplate
except ImportError:
    # Create placeholder classes if models are not available
    class EmailTemplate:  # type: ignore
        objects = None
        DoesNotExist = Exception
        html_content = ""
        plain_content = ""
        subject = ""
    
    class EmailLog:  # type: ignore
        objects = None
def send_template_email(
    template_name: str,
    recipient_email: str,
    context: Optional[Dict[str, Any]] = None,
    sender_email: Optional[str] = None,
    fail_silently: bool = False,
) -> bool:
    """Send an email using a predefined template."""
    # Check if models are properly imported
    if EmailTemplate is None or not hasattr(EmailTemplate, 'objects'):
        logger.error("EmailTemplate model is not available")
        if not fail_silently:
            raise ImportError("EmailTemplate model is not available")
        return False
    
    try:
        template = EmailTemplate.objects.get(name=template_name, is_active=True)
    except EmailTemplate.DoesNotExist:
        logger.error("Email template '%s' not found or inactive", template_name)
        if not fail_silently:
            raise
        return False
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
        # Log the email
        if EmailLog and hasattr(EmailLog, 'objects'):
            EmailLog.objects.create(
                recipient=recipient_email,
                sender=sender_email,
                subject=subject,
                template=template,
                status="sent" if sent else "failed",
            )

        sent = email.send()

        # Log the email
        EmailLog.objects.create(
        # Log the failed attempt
        if EmailLog and hasattr(EmailLog, 'objects'):
            EmailLog.objects.create(
                recipient=recipient_email,
                sender=sender_email,
                subject=subject or f"Email from template {template_name}",
                template=template,
                status="failed",
                error_message=str(e),
            )
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
def get_email_statistics(days: int = 30) -> Dict[str, Any]:
    """Get email sending statistics for the last N days."""
    # Check if EmailLog model is available
    if EmailLog is None or not hasattr(EmailLog, 'objects'):
        return {
            "period_days": days,
            "total_sent": 0,
            "delivered": 0,
            "failed": 0,
            "bounced": 0,
            "spam": 0,
            "delivery_rate": 0,
        }
    
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
