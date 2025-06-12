"""Type definitions for the sendgrid application."""

from typing import Protocol, runtime_checkable

from django.db import models

# Email status choices type definition
EmailStatusType = tuple[str, str]

EMAIL_STATUS_CHOICES: tuple[EmailStatusType, ...] = (
    ("pending", "Pending"),
    ("sent", "Sent"),
    ("delivered", "Delivered"),
    ("failed", "Failed"),
    ("bounced", "Bounced"),
    ("spam", "Marked as Spam"),
)


@runtime_checkable
class EmailTemplateType(Protocol):
    """Type definition for EmailTemplate model."""

    name: str
    subject: str
    html_content: str
    plain_content: str
    sendgrid_template_id: str
    is_active: bool
    created_at: models.DateTimeField
    updated_at: models.DateTimeField


@runtime_checkable
class EmailLogType(Protocol):
    """Type definition for EmailLog model."""

    recipient: str
    sender: str
    subject: str
    template: "EmailTemplateType"
    sendgrid_message_id: str
    status: str
    sent_at: models.DateTimeField
    delivered_at: models.DateTimeField
    error_message: str
