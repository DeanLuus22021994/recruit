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
except ImportError:
    # Fallback for when allauth is not available
    EmailAddress = None  # type: ignore


class UserProfile(models.Model):
    """Model for user profiles."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(choices=TIMEZONE_CHOICES, max_length=50, blank=True)
    citizenship = CountryField(blank_label="(Select country)")
    skype_id = models.CharField(max_length=50, blank=True)
    user_type = models.CharField(
        choices=(
            ("Candidate", "Candidate"),
            ("Recruiter", "Recruiter"),
            ("Employer", "Employer"),
        ),
        max_length=50,
    )
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self) -> str:
        """Return string representation of the user profile."""
        return str(getattr(self.user, "email", ""))

    def generate_token(self) -> str:
        """Generate a token for the user."""
        email = getattr(self.user, "email", "")
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
        except User.DoesNotExist:
            return None


def create_account_emailaddress(
    sender: Any, instance: User, created: bool, **kwargs: Any
) -> None:
    """Create EmailAddress for django-allauth when user is created."""
    _ = sender  # Mark as used
    _ = kwargs  # Mark as used

    if created and EmailAddress is not None:
        email = getattr(instance, "email", "")
        if email:
            EmailAddress.objects.get_or_create(user_id=instance.pk, email=email)


# Only connect signal if EmailAddress is available
if EmailAddress is not None:
    post_save.connect(create_account_emailaddress, sender=User)
