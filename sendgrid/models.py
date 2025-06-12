"""SendGrid models for tracking email statistics and templates."""

# Import models from centralized location
from recruit_models.sendgrid import EmailLog, EmailTemplate

__all__ = ["EmailTemplate", "EmailLog"]
