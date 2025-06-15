"""Models for the accounts application."""

from allauth.account.models import EmailAddress
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    """Extended user model with additional profile fields."""

    # Additional profile fields
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    # Professional information
    company = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    # Settings
    is_recruiter = models.BooleanField(default=False)
    is_candidate = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "accounts_userprofile"
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.username} - {self.get_full_name()}"

    def get_display_name(self):
        """Return the best available display name for the user."""
        if self.get_full_name():
            return self.get_full_name()
        return self.username


def create_account_emailaddress(user, email, verified=False, primary=False):
    """Create an EmailAddress instance for the given user and email."""
    email_address, created = EmailAddress.objects.get_or_create(
        user=user,
        email=email.lower(),
        defaults={
            "verified": verified,
            "primary": primary,
        },
    )

    if created and primary:
        # If this is a new primary email, make sure no other emails are primary
        EmailAddress.objects.filter(user=user, primary=True).exclude(
            id=email_address.id
        ).update(primary=False)

    return email_address


__all__ = ["UserProfile", "create_account_emailaddress"]
