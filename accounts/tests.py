"""Tests for the accounts application."""

import datetime
import tempfile
from typing import TYPE_CHECKING, Any

from django.contrib.auth.models import User
from django.test import TestCase

if TYPE_CHECKING:
    pass


def get_user(user_id: int) -> User:
    """Get user by ID."""
    return User.objects.get(id=user_id)


def get_candidate(candidate_id: int) -> Any:
    """Get candidate by ID."""
    try:
        from candidates.models import Candidate

        return Candidate.objects.get(id=candidate_id)  # type: ignore[attr-defined]
    except ImportError:
        return None


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
        self.assertEqual(getattr(user, "email", ""), "email@example.com")
        self.assertEqual(getattr(user, "first_name", ""), "John")

    def test_user_password(self) -> None:
        """Test user password validation."""
        user = get_user(1)
        self.assertTrue(user.check_password("password"))

    def test_candidate_creation(self) -> None:
        """Test candidate creation."""
        try:
            from candidates.models import Candidate
        except ImportError:
            self.skipTest("Candidates app not available")
            return

        user = get_user(1)
        candidate = Candidate.objects.create(  # type: ignore[attr-defined]
            user=user,
            birth_year="1970",
            gender="male",
            education="Master's Degree",
            education_major="Marketing",
            current_location="AQ",  # Antarctica country code
            date_of_birth=datetime.date(1970, 1, 1),
        )
        candidate.save()
        self.assertEqual(getattr(candidate, "user", None), user)
        candidate_user = getattr(candidate, "user", None)
        if candidate_user:
            self.assertEqual(getattr(candidate_user, "email", ""), "email@example.com")
            self.assertEqual(getattr(candidate_user, "first_name", ""), "John")

    def test_candidate_unauthorized_login(self) -> None:
        """Test candidate login attempt."""
        user = get_user(1)
        user_email = getattr(user, "email", "")
        response = self.client.post(
            "/admin/login/", {"username": user_email, "password": "password"}
        )
        self.assertTrue(response.status_code == 200)

    def test_employer_creation(self) -> None:
        """Test employer creation."""
        try:
            from employers.models import Employer
        except ImportError:
            self.skipTest("Employers app not available")
            return

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
