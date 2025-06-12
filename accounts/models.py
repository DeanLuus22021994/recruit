"""Models for the accounts application."""

from typing import Any, Optional

from django.contrib.auth.models import User
from django.core import signing
from django.core.signing import BadSignature, SignatureExpired
from django.db import models
from django.db.models.signals import post_save
from django_countries.fields import CountryField

from recruit.choices import TIMEZONE_CHOICES

try:
    from allauth.account.models import EmailAddress

    ALLAUTH_AVAILABLE = True
except ImportError:
    # Fallback for when allauth is not available
    EmailAddress = None
    ALLAUTH_AVAILABLE = False


class UserProfile(models.Model):
    """Model for user profiles."""

    user: models.OneToOneField[User, User] = models.OneToOneField(
        User, on_delete=models.CASCADE
    )
    timezone: models.CharField[str, str] = models.CharField(
        choices=TIMEZONE_CHOICES, max_length=50, blank=True
    )
    citizenship: CountryField = CountryField(blank_label="(Select country)")
    skype_id: models.CharField[str, str] = models.CharField(max_length=50, blank=True)
    user_type: models.CharField[str, str] = models.CharField(
        choices=(
            ("Candidate", "Candidate"),
            ("Recruiter", "Recruiter"),
            ("Employer", "Employer"),
        ),
        max_length=50,
    )
    last_modified: models.DateTimeField[Any, Any] = models.DateTimeField(
        auto_now_add=False, auto_now=True
    )
    created: models.DateTimeField[Any, Any] = models.DateTimeField(
        auto_now_add=True, auto_now=False
    )

    def __str__(self) -> str:
        """Return string representation of the user profile."""
        user_obj: User = self.user
        return str(getattr(user_obj, "email", ""))

    def generate_token(self) -> str:
        """Generate a token for the user."""
        user_obj: User = self.user
        email = getattr(user_obj, "email", "")
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
            user = User.objects.get(email=value["email"])
            return user
        except User.DoesNotExist:  # type: ignore[attr-defined]
            return None


def create_account_emailaddress(
    sender: Any, instance: User, created: bool, **kwargs: Any
) -> None:
    """Create EmailAddress for django-allauth when user is created."""
    # Mark parameters as used
    _ = sender
    _ = kwargs

    if created and ALLAUTH_AVAILABLE and EmailAddress is not None:
        email = getattr(instance, "email", "")
        if email:
            EmailAddress.objects.get_or_create(user_id=instance.pk, email=email)


# Only connect signal if EmailAddress is available
if ALLAUTH_AVAILABLE and EmailAddress is not None:
    post_save.connect(create_account_emailaddress, sender=User)
