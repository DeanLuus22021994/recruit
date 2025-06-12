"""Custom SendGrid email backend."""

from typing import Optional, Sequence

try:
    import sendgrid
    from sendgrid.helpers.mail import Mail

    SENDGRID_AVAILABLE = True
except ImportError:
    SENDGRID_AVAILABLE = False

    # Fallback classes for when sendgrid is not available
    class Mail:
        def __init__(self, *args, **kwargs):
            pass

    class SendGridAPIClient:
        def __init__(self, *args, **kwargs):
            pass

        def send(self, *args, **kwargs):
            pass


from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage


class SendGridBackend(BaseEmailBackend):
    """Django email backend using SendGrid API."""

    def __init__(self, fail_silently: bool = False, **kwargs) -> None:
        """Initialize the SendGrid backend."""
        super().__init__(fail_silently=fail_silently, **kwargs)
        self.api_key: Optional[str] = getattr(settings, "SENDGRID_API_KEY", None)
        if not self.api_key:
            # Fallback to username/password method
            self.username: Optional[str] = getattr(settings, "SENDGRID_USER", None)
            self.password: Optional[str] = getattr(settings, "SENDGRID_PASSWORD", None)

    def send_messages(self, email_messages: Sequence[EmailMessage]) -> int:
        """Send email messages using SendGrid."""
        if not email_messages or not SENDGRID_AVAILABLE:
            return 0

        num_sent = 0
        if SENDGRID_AVAILABLE:
            sg = sendgrid.SendGridAPIClient(api_key=self.api_key)
        else:
            return 0

        for message in email_messages:
            try:
                mail = Mail(
                    from_email=message.from_email,
                    to_emails=message.to,
                    subject=message.subject,
                    html_content=message.body,
                )
                if SENDGRID_AVAILABLE:
                    sg.send(mail)
                num_sent += 1
            except Exception as e:
                if not self.fail_silently:
                    raise e

        return num_sent
