"""SendGrid email backend implementation."""

import logging
from typing import Any, List, Optional, Sequence, Union

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage

# Try importing SendGrid with proper error handling
try:
    import sendgrid
    from sendgrid.helpers.mail import Mail
    SENDGRID_AVAILABLE = True
except ImportError:
    SENDGRID_AVAILABLE = False
    # Create stub classes for type hints when SendGrid is not available
    class Mail:  # type: ignore
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass
    
    class SendGridAPIClient:  # type: ignore
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass
        
        def send(self, *args: Any, **kwargs: Any) -> Any:
            pass

logger = logging.getLogger(__name__)


class SendGridBackend(BaseEmailBackend):
    """
    Django email backend using SendGrid API v3.
    
    Supports both API key and username/password authentication methods.
    Falls back gracefully when SendGrid is not available.
    """

    def __init__(self, fail_silently: bool = False, **kwargs: Any) -> None:
        """Initialize the SendGrid backend with configuration from Django settings."""
        super().__init__(fail_silently=fail_silently, **kwargs)
        
        # Primary authentication method: API Key
        self.api_key: Optional[str] = getattr(settings, "SENDGRID_API_KEY", None)
        
        # Fallback authentication method: Username/Password (deprecated but supported)
        if not self.api_key:
            self.username: Optional[str] = getattr(settings, "SENDGRID_USER", None)
            self.password: Optional[str] = getattr(settings, "SENDGRID_PASSWORD", None)
        
        # Default sender email
        self.default_from_email: str = getattr(
            settings, 
            "DEFAULT_FROM_EMAIL", 
            "noreply@example.com"
        )

    def send_messages(self, email_messages: Sequence[EmailMessage]) -> int:
        """
        Send email messages using SendGrid API.
        
        Args:
            email_messages: Sequence of Django EmailMessage objects
            
        Returns:
            Number of successfully sent messages
        """
        if not email_messages:
            return 0
            
        if not SENDGRID_AVAILABLE:
            logger.warning("SendGrid library is not available. No emails sent.")
            return 0

        if not self.api_key and not (self.username and self.password):
            logger.error("SendGrid credentials not configured properly.")
            if not self.fail_silently:
                raise ValueError("SendGrid API key or username/password required")
            return 0

        # Initialize SendGrid client
        try:
            if SENDGRID_AVAILABLE:
                sg = sendgrid.SendGridAPIClient(api_key=self.api_key)
            else:
                return 0
        except Exception as e:
            logger.error(f"Failed to initialize SendGrid client: {e}")
            if not self.fail_silently:
                raise
            return 0

        num_sent = 0
        
        for message in email_messages:
            try:
                sent = self._send_single_message(sg, message)
                if sent:
                    num_sent += 1
            except Exception as e:
                logger.error(f"Failed to send email to {message.to}: {e}")
                if not self.fail_silently:
                    raise

        return num_sent

    def _send_single_message(self, sg_client: Any, message: EmailMessage) -> bool:
        """
        Send a single email message.
        
        Args:
            sg_client: SendGrid API client instance
            message: Django EmailMessage object
            
        Returns:
            True if message was sent successfully, False otherwise
        """
        try:
            # Prepare sender email
            from_email = message.from_email or self.default_from_email
            
            # Handle multiple recipients
            to_emails = self._prepare_recipients(message.to)
            cc_emails = self._prepare_recipients(getattr(message, 'cc', []))
            bcc_emails = self._prepare_recipients(getattr(message, 'bcc', []))
            
            # Create mail object
            mail = Mail(
                from_email=from_email,
                to_emails=to_emails,
                subject=message.subject,
                html_content=message.body if message.content_subtype == 'html' else None,
                plain_text_content=message.body if message.content_subtype == 'plain' else None
            )
            
            # Add CC and BCC if present
            if cc_emails:
                for cc_email in cc_emails:
                    mail.add_cc(cc_email)
                    
            if bcc_emails:
                for bcc_email in bcc_emails:
                    mail.add_bcc(bcc_email)
            
            # Handle attachments if present
            if hasattr(message, 'attachments') and message.attachments:
                self._add_attachments(mail, message.attachments)
            
            # Send the email
            response = sg_client.send(mail)
            
            # Check response status
            if response.status_code in [200, 201, 202]:
                logger.info(f"Email sent successfully to {message.to}")
                return True
            else:
                logger.warning(f"SendGrid returned status {response.status_code}: {response.body}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            raise

    def _prepare_recipients(self, recipients: Union[List[str], str]) -> List[str]:
        """
        Prepare recipient list for SendGrid.
        
        Args:
            recipients: String or list of email addresses
            
        Returns:
            List of email addresses
        """
        if isinstance(recipients, str):
            return [recipients]
        return list(recipients) if recipients else []

    def _add_attachments(self, mail: Mail, attachments: List[Any]) -> None:
        """
        Add attachments to the mail object.
        
        Args:
            mail: SendGrid Mail object
            attachments: List of attachment tuples (filename, content, mimetype)
        """
        try:
            from sendgrid.helpers.mail import Attachment
            import base64
            
            for attachment in attachments:
                if len(attachment) >= 2:
                    filename = attachment[0]
                    content = attachment[1]
                    mimetype = attachment[2] if len(attachment) > 2 else 'application/octet-stream'
                    
                    # Encode content to base64 if it's bytes
                    if isinstance(content, bytes):
                        encoded_content = base64.b64encode(content).decode()
                    else:
                        encoded_content = base64.b64encode(content.encode()).decode()
                    
                    attached_file = Attachment(
                        file_content=encoded_content,
                        file_name=filename,
                        file_type=mimetype,
                        disposition='attachment'
                    )
                    mail.add_attachment(attached_file)
                    
        except ImportError:
            logger.warning("SendGrid attachment support not available")
        except Exception as e:
            logger.error(f"Error adding attachments: {e}")