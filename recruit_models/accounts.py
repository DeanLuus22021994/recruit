"""Models for the accounts application."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from django.contrib.auth.models import User
from django.core import signing
from django.core.signing import BadSignature, SignatureExpired
from django.db import models
from django.db.models.signals import post_save
from django_countries.fields import CountryField

from recruit.choices import TIMEZONE_CHOICES

if TYPE_CHECKING:
    pass

try:
    from allauth.account.models import EmailAddress

    allauth_available = True
except ImportError:
    EmailAddress = None
    allauth_available = False


class UserProfile(models.Model):
    """Model for user profiles implementing UserProfileType."""

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

    class Meta:
        app_label = "accounts"

    def __str__(self) -> str:
        return str(getattr(self.user, "email", ""))

    def generate_token(self) -> str:
        email = getattr(self.user, "email", "")
        return signing.dumps({"email": email})

    @staticmethod
    def verify_token(token: Optional[str], max_age: int = 604800) -> Optional[User]:
        if not token:
            return None
        try:
            value = signing.loads(token, max_age=max_age)
            return User.objects.get(email=value["email"])
        except (SignatureExpired, BadSignature, User.DoesNotExist):
            return None

    @staticmethod
    def verify_token_with_result(
        token: Optional[str], max_age: int = 604800
    ) -> Optional[Any]:
        if TYPE_CHECKING:
            from recruit_types.accounts import TokenVerificationResult
        else:
            try:
                from recruit_types.accounts import TokenVerificationResult
            except ImportError:
                return None

        if not token:
            return TokenVerificationResult(error="No token provided")

        try:
            value = signing.loads(token, max_age=max_age)
            user = User.objects.get(email=value["email"])
            return TokenVerificationResult(user=user)
        except SignatureExpired:
            return TokenVerificationResult(error="Token expired")
        except BadSignature:
            return TokenVerificationResult(error="Invalid token signature")
        except User.DoesNotExist:
            return TokenVerificationResult(error="User not found")


def create_account_emailaddress(
    sender: Any, instance: User, created: bool, **kwargs: Any
) -> None:
    """Create EmailAddress for django-allauth when user is created."""
    if created and allauth_available and EmailAddress is not None:
        email = getattr(instance, "email", "")
        if email:
            EmailAddress.objects.get_or_create(user_id=instance.pk, email=email)


if allauth_available and EmailAddress is not None:
    post_save.connect(create_account_emailaddress, sender=User)
