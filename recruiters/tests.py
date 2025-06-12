from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Recruiter


class RecruiterModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testrecruiter", email="test@example.com", password="testpass123"
        )

    def test_recruiter_creation(self) -> None:
        recruiter = Recruiter.objects.create(
            user=self.user,
            phone_number="+1234567890",
            date_of_birth=date(1990, 1, 1),
            location="Test City",
        )

        self.assertEqual(recruiter.user, self.user)
        self.assertEqual(str(recruiter), "test@example.com")
        self.assertTrue(recruiter.is_active)

    def test_recruiter_str_method(self) -> None:
        recruiter = Recruiter.objects.create(
            user=self.user,
            phone_number="+1234567890",
            date_of_birth=date(1990, 1, 1),
            location="Test City",
        )

        self.assertEqual(str(recruiter), "test@example.com")
