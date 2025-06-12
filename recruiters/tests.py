"""Tests for the recruiters application."""

from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Recruiter


class RecruiterModelTest(TestCase):
    """Test cases for Recruiter model."""

    def setUp(self) -> None:
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testrecruiter", email="test@example.com", password="testpass123"
        )

    def test_recruiter_creation(self) -> None:
        """Test that a recruiter can be created successfully."""
        recruiter = Recruiter.objects.create(  # type: ignore[misc]
            user=self.user,
            phone_number="+1234567890",
            date_of_birth=date(1990, 1, 1),
            location="Test City",
        )

        self.assertEqual(recruiter.user, self.user)  # type: ignore[misc]
        self.assertEqual(str(recruiter), "test@example.com")
        self.assertTrue(recruiter.is_active)  # type: ignore[misc]

    def test_recruiter_str_method(self) -> None:
        """Test the string representation of a recruiter."""
        recruiter = Recruiter.objects.create(  # type: ignore[misc]
            user=self.user,
            phone_number="+1234567890",
            date_of_birth=date(1990, 1, 1),
            location="Test City",
        )

        self.assertEqual(str(recruiter), "test@example.com")
