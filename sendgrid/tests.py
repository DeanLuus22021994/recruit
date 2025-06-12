"""Tests for SendGrid integration."""

from unittest.mock import Mock, patch
from django.test import TestCase, override_settings
from django.core.mail import EmailMessage

from .backends import SendGridBackend
from .models import EmailTemplate, EmailLog
from .utils import send_template_email


class SendGridBackendTest(TestCase):
    """Test cases for SendGrid email backend."""
    
    @override_settings(SENDGRID_API_KEY='test-api-key')
    @patch('sendgrid.SendGridAPIClient')
    def test_send_messages_success(self, mock_sg_client):
        """Test successful email sending."""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 202
        mock_sg_client.return_value.send.return_value = mock_response
        
        # Create backend and message
        backend = SendGridBackend()
        message = EmailMessage(
            subject='Test Subject',
            body='Test Body',
            from_email='from@example.com',
            to=['to@example.com']
        )
        
        # Send message
        with patch('sendgrid.SendGridAPIClient', mock_sg_client):
            num_sent = backend.send_messages([message])
        
        self.assertEqual(num_sent, 1)
        mock_sg_client.return_value.send.assert_called_once()
    
    @override_settings(SENDGRID_API_KEY=None)
    def test_send_messages_no_credentials(self):
        """Test behavior when no credentials are provided."""
        backend = SendGridBackend(fail_silently=True)
        message = EmailMessage(
            subject='Test Subject',
            body='Test Body',
            from_email='from@example.com',
            to=['to@example.com']
        )
        
        num_sent = backend.send_messages([message])
        self.assertEqual(num_sent, 0)


class EmailTemplateTest(TestCase):
    """Test cases for EmailTemplate model."""
    
    def test_create_template(self):
        """Test creating an email template."""
        template = EmailTemplate.objects.create(
            name='welcome',
            subject='Welcome to Our Service',
            html_content='<h1>Welcome {{ name }}!</h1>',
            plain_content='Welcome {{ name }}!'
        )
        
        self.assertEqual(str(template), 'welcome')
        self.assertTrue(template.is_active)


class EmailUtilsTest(TestCase):
    """Test cases for email utilities."""
    
    def setUp(self):
        """Set up test data."""
        self.template = EmailTemplate.objects.create(
            name='test_template',
            subject='Hello {{ name }}',
            html_content='<p>Hello {{ name }}, welcome!</p>',
            plain_content='Hello {{ name }}, welcome!'
        )
    
    @patch('sendgrid.SendGridAPIClient')
    def test_send_template_email(self, mock_sg_client):
        """Test sending email using template."""
        mock_response = Mock()
        mock_response.status_code = 202
        mock_sg_client.return_value.send.return_value = mock_response
        
        with patch('sendgrid.SendGridAPIClient', mock_sg_client):
            result = send_template_email(
                template_name='test_template',
                recipient_email='test@example.com',
                context={'name': 'John Doe'}
            )
        
        self.assertTrue(result)
        
        # Check if email log was created
        log = EmailLog.objects.get(recipient='test@example.com')
        self.assertEqual(log.subject, 'Hello John Doe')
        self.assertEqual(log.status, 'sent')