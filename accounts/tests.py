"""Tests for the accounts application."""

import datetime
import tempfile
from typing import Any

from django.contrib.auth.models import User
from django.test import TestCase


def get_user(user_id: int) -> User:
    """Get user by ID."""
    return User.objects.get(id=user_id)


def get_candidate(candidate_id: int) -> Any:
    """Get candidate by ID."""
    from candidates.models import Candidate

    return Candidate.objects.get(id=candidate_id)


class UserTestCase(TestCase):
    """Test cases for User model and related functionality."""

    def setUp(self) -> None:
        """Set up test data."""
        user = User.objects.create(
            email="email@example.com",
            username="email@example.com",  # Django User requires username
            first_name="John",
            last_name="Doe",
        )
        user.set_password("password")
        user.is_superuser = True
        user.save()

    def test_user_creation(self) -> None:
        """Test user creation."""
        user = get_user(1)
        self.assertEqual(user.email, "email@example.com")
        self.assertEqual(user.first_name, "John")

    def test_user_password(self) -> None:
        """Test user password validation."""
        user = get_user(1)
        self.assertTrue(user.check_password("password"))

    def test_candidate_creation(self) -> None:
        """Test candidate creation."""
        from candidates.models import Candidate

        user = get_user(1)
        candidate = Candidate.objects.create(
            user=user,
            birth_year="1970",
            gender="male",
            education="Master's Degree",
            education_major="Marketing",
            current_location="AQ",  # Antarctica country code
            date_of_birth=datetime.date(1970, 1, 1),
        )
        candidate.save()
        self.assertEqual(candidate.user.pk, 1)
        self.assertEqual(candidate.user.email, "email@example.com")
        self.assertEqual(candidate.user.first_name, "John")

    def test_candidate_unauthorized_login(self) -> None:
        """Test candidate login attempt."""
        user = get_user(1)
        response = self.client.post(
            "/admin/login/", {"username": user.email, "password": "password"}
        )
        self.assertTrue(response.status_code == 200)

    def test_employer_creation(self) -> None:
        """Test employer creation."""
        from employers.models import Employer

        user = get_user(1)

        # Create a temporary file for the business license
        temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        temp_file.close()

        employer = Employer(
            user=user,
            phone_number="+44 20 34545454",
            name_english="Acme Corp",
            name_local="Non-english name",
            address_english="123 Long Street",
            address_local="Non-english address",
            business_license=temp_file.name,
        )
        employer.save()

        # Access employer through the related manager
        user_employer = getattr(user, "employer", None)
        self.assertEqual(employer, user_employer)
