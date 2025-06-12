"""SendGrid app configuration."""

from django.apps import AppConfig


class SendgridConfig(AppConfig):
    """Configuration for SendGrid app."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sendgrid'
    verbose_name = 'SendGrid Email Service'