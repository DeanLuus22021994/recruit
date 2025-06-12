"""SendGrid models for tracking email statistics and templates."""

from django.db import models
from django.utils import timezone

from recruit_types.sendgrid import EMAIL_STATUS_CHOICES


class EmailTemplate(models.Model):
    """Model for storing reusable email templates."""

    name: models.CharField = models.CharField(max_length=100, unique=True)
    subject: models.CharField = models.CharField(max_length=200)
    html_content: models.TextField = models.TextField(blank=True)
    plain_content: models.TextField = models.TextField(blank=True)
    sendgrid_template_id: models.CharField = models.CharField(
        max_length=100, blank=True
    )
    is_active: models.BooleanField = models.BooleanField(default=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "sendgrid"
        ordering = ["name"]

    def __str__(self) -> str:
        return str(self.name)


class EmailLog(models.Model):
    """Model for tracking sent emails implementing EmailLogType."""

    recipient: models.EmailField = models.EmailField()
    sender: models.EmailField = models.EmailField()
    subject: models.CharField = models.CharField(max_length=200)
    template: models.ForeignKey = models.ForeignKey(
        EmailTemplate, on_delete=models.SET_NULL, null=True, blank=True
    )
    sendgrid_message_id: models.CharField = models.CharField(max_length=200, blank=True)
    status: models.CharField = models.CharField(
        max_length=20, choices=EMAIL_STATUS_CHOICES, default="pending"
    )
    sent_at: models.DateTimeField = models.DateTimeField(default=timezone.now)
    delivered_at: models.DateTimeField = models.DateTimeField(null=True, blank=True)
    error_message: models.TextField = models.TextField(blank=True)

    class Meta:
        app_label = "sendgrid"
        ordering = ["-sent_at"]
        indexes = [
            models.Index(fields=["recipient"]),
            models.Index(fields=["status"]),
            models.Index(fields=["sent_at"]),
        ]

    def __str__(self) -> str:
        return f"Email to {str(self.recipient)} - {str(self.status)}"
