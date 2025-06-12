"""Utility functions for SendGrid integration."""

import logging
from typing import Any, Dict, List, Optional, Union

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import EmailTemplate, EmailLog

logger = logging.getLogger(__name__)


def send_template_email(
    template_name: str,
    recipient_email: str,
    context: Optional[Dict[str, Any]] = None,
    sender_email: Optional[str] = None,
    fail_silently: bool = False
) -> bool:
    """
    Send an email using a predefined template.
    
    Args:
        template_name: Name of the EmailTemplate to use
        recipient_email: Recipient's email address
        context: Template context variables
        sender_email: Sender's email address (optional)
        fail_silently: Whether to suppress exceptions
        
    Returns:
        True if email was sent successfully, False otherwise
    """
    try:
        template = EmailTemplate.objects.get(name=template_name, is_active=True)
    except EmailTemplate.DoesNotExist:
        logger.error(f"Email template '{template_name}' not found or inactive")
        if not fail_silently:
            raise
        return False
    
    context = context or {}
    sender_email = sender_email or getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')
    
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
        
    except Exception as e:
        logger.error(f"Error rendering template '{template_name}': {e}")
        if not fail_silently:
            raise
        return False
    
    # Create and send email
    try:
        email = EmailMessage(
            subject=subject,
            body=html_content or plain_content,
            from_email=sender_email,
            to=[recipient_email]
        )
        
        if html_content:
            email.content_subtype = 'html'
        
        sent = email.send()
        
        # Log the email
        EmailLog.objects.create(
            recipient=recipient_email,
            sender=sender_email,
            subject=subject,
            template=template,
            status='sent' if sent else 'failed'
        )
        
        return bool(sent)
        
    except Exception as e:
        logger.error(f"Error sending email to {recipient_email}: {e}")
        
        # Log the failed attempt
        EmailLog.objects.create(
            recipient=recipient_email,
            sender=sender_email,
            subject=subject or f"Email from template {template_name}",
            template=template,
            status='failed',
            error_message=str(e)
        )
        
        if not fail_silently:
            raise
        return False


def render_to_string_from_text(template_string: str, context: Dict[str, Any]) -> str:
    """
    Render a template string with context variables.
    
    Args:
        template_string: Template string with Django template syntax
        context: Context variables for rendering
        
    Returns:
        Rendered string
    """
    from django.template import Context, Template
    
    template = Template(template_string)
    return template.render(Context(context))


def get_email_statistics(days: int = 30) -> Dict[str, Any]:
    """
    Get email sending statistics for the last N days.
    
    Args:
        days: Number of days to look back
        
    Returns:
        Dictionary with email statistics
    """
    from django.utils import timezone
    from django.db.models import Count
    
    start_date = timezone.now() - timezone.timedelta(days=days)
    
    stats = EmailLog.objects.filter(sent_at__gte=start_date).aggregate(
        total_sent=Count('id'),
        delivered=Count('id', filter=models.Q(status='delivered')),
        failed=Count('id', filter=models.Q(status='failed')),
        bounced=Count('id', filter=models.Q(status='bounced')),
        spam=Count('id', filter=models.Q(status='spam'))
    )
    
    return {
        'period_days': days,
        'total_sent': stats['total_sent'] or 0,
        'delivered': stats['delivered'] or 0,
        'failed': stats['failed'] or 0,
        'bounced': stats['bounced'] or 0,
        'spam': stats['spam'] or 0,
        'delivery_rate': (stats['delivered'] / stats['total_sent'] * 100) if stats['total_sent'] else 0
    }