"""Tests for the jobs application."""

from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from recruiters.models import Recruiter

from .models import Country


class JobModelTest(TestCase):
    """Test cases for Job models."""

    def setUp(self) -> None:
        """Set up test data."""
        # Create a user for the recruiter
        self.user = User.objects.create_user(
            username="testrecruiter", email="test@example.com", password="testpass123"
        )

        # Create a recruiter
        self.recruiter = Recruiter.objects.create(
            user=self.user,
            phone_number="+1234567890",
            date_of_birth=date(1990, 1, 1),
            location="Test City",
        )

    def test_country_creation(self) -> None:
        """Test that a country can be created."""
        country = Country.objects.create(country="United States")
        self.assertEqual(str(country), "United States")

    def test_job_str_method(self) -> None:
        """Test job string representation."""
        # This test would need an Employer instance
        # Commented out until Employer model is available
        pass
