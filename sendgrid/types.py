"""Type definitions for the sendgrid application."""

from typing import Any, Protocol, Tuple, runtime_checkable

from django.db import models

# Email status choices type definition
EmailStatusType = Tuple[str, str]

EMAIL_STATUS_CHOICES: Tuple[EmailStatusType, ...] = (
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
    created_at: models.DateTimeField[Any, Any]
    updated_at: models.DateTimeField[Any, Any]

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save the email template instance."""

    def __str__(self) -> str:
        """Return string representation of the email template."""
        return ""  # Protocol methods should have a default implementation


@runtime_checkable
class EmailLogType(Protocol):
    """Type definition for EmailLog model."""

    recipient: str
    sender: str
    subject: str
    template: "EmailTemplateType"
    sendgrid_message_id: str
    status: str
    sent_at: models.DateTimeField[Any, Any]
    delivered_at: models.DateTimeField[Any, Any]
    error_message: str

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save the email log instance."""

    def delete(self, *args: Any, **kwargs: Any) -> None:
        """Delete the email log instance."""
