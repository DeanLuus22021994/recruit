"""Models for the accounts application."""

from typing import Any, Optional

from allauth.account.models import EmailAddress  # type: ignore[import-untyped]
from django.contrib.auth.models import User
from django.core import signing
from django.core.signing import BadSignature, SignatureExpired
from django.db import models
from django.db.models.signals import post_save
from django_countries.fields import CountryField  # type: ignore[import-untyped]

from recruit.choices import TIMEZONE_CHOICES


class UserProfile(models.Model):
    """Model for user profiles."""

    user: models.OneToOneField = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone: models.CharField = models.CharField(
        choices=TIMEZONE_CHOICES, max_length=50, blank=True
    )
    citizenship: CountryField = CountryField(blank_label="(Select country)")  # type: ignore[misc]
    skype_id: models.CharField = models.CharField(max_length=50, blank=True)
    user_type: models.CharField = models.CharField(
        choices=(
            ("Candidate", "Candidate"),
            ("Recruiter", "Recruiter"),
            ("Employer", "Employer"),
        ),
        max_length=50,
    )
    last_modified: models.DateTimeField = models.DateTimeField(
        auto_now_add=False, auto_now=True
    )
    created: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, auto_now=False
    )

    def __str__(self) -> str:
        """Return string representation of the user profile."""
        return str(self.user.email)

    def generate_token(self) -> str:
        """Generate a token for the user."""
        email = self.user.email
        token = signing.dumps({"email": email})
        return token

    @staticmethod
    def verify_token(token: Optional[str], max_age: int = 604800) -> Optional[User]:
        """Verify a token and return the associated user."""
        if not token:
            return None
        # default max_age is 7 days
        try:
            value = signing.loads(token, max_age=max_age)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        try:
            user = User.objects.get(email=value["email"])  # type: ignore[misc]
            return user
        except User.DoesNotExist:  # type: ignore[misc]
            return None


def create_account_emailaddress(
    sender: Any, instance: User, created: bool, **kwargs: Any
) -> None:
    """Create EmailAddress for django-allauth when user is created."""
    if created:
        EmailAddress.objects.get_or_create(  # type: ignore[misc]
            user_id=instance.id, email=instance.email
        )


post_save.connect(create_account_emailaddress, sender=User)
