"""Custom SendGrid email backend."""

from typing import List, Optional

import sendgrid  # type: ignore[import-untyped]
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage
from sendgrid.helpers.mail import Mail  # type: ignore[import-untyped]


class SendGridBackend(BaseEmailBackend):
    """Django email backend using SendGrid API."""

    def __init__(self, **kwargs) -> None:
        """Initialize the SendGrid backend."""
        super().__init__(**kwargs)
        self.api_key: Optional[str] = getattr(settings, "SENDGRID_API_KEY", None)
        if not self.api_key:
            # Fallback to username/password method
            self.username: Optional[str] = getattr(settings, "SENDGRID_USER", None)
            self.password: Optional[str] = getattr(settings, "SENDGRID_PASSWORD", None)

    def send_messages(self, email_messages: List[EmailMessage]) -> int:
        """Send email messages using SendGrid."""
        if not email_messages:
            return 0

        num_sent = 0
        sg = sendgrid.SendGridAPIClient(api_key=self.api_key)

        for message in email_messages:
            try:
                mail = Mail(
                    from_email=message.from_email,
                    to_emails=message.to,
                    subject=message.subject,
                    html_content=message.body,
                )
                sg.send(mail)
                num_sent += 1
            except sendgrid.exceptions.SendGridException as e:
                if not self.fail_silently:
                    raise e
            except Exception as e:
                if not self.fail_silently:
                    raise e

        return num_sent
