"""Models for the recruiters application."""

from typing import Any, Dict, Tuple

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

try:
    from phonenumber_field.modelfields import PhoneNumberField
except ImportError:
    # Fallback if phonenumber_field is not available
    PhoneNumberField = models.CharField


class Recruiter(models.Model):
    """Model representing a recruiter user."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(max_length=20)
    date_of_birth = models.DateField()
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to="recruiter/%Y/%m/%d")
    thumb = models.ImageField(upload_to="recruiter/%Y/%m/%d", blank=True)
    is_active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self) -> str:
        """Return string representation of the recruiter."""
        return str(getattr(self.user, "email", "No email"))

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save the recruiter instance with thumbnail generation."""
        from recruit.utils import generate_thumbnail

        if self.image:
            self.thumb = generate_thumbnail(self.image)
        super(Recruiter, self).save(*args, **kwargs)

    def delete(self, *args: Any, **kwargs: Any) -> Tuple[int, Dict[str, int]]:
        """Delete the recruiter instance and associated files."""
        from recruit.utils import delete_from_s3

        delete_from_s3([self.image, self.thumb])
        return super(Recruiter, self).delete(*args, **kwargs)


def update_user_profile(
    sender: Any, instance: Recruiter, created: bool, **kwargs: Any
) -> None:
    """Update user profile when recruiter is created."""
    from accounts.models import UserProfile

    _ = sender  # Mark as intentionally unused
    _ = kwargs  # Mark as intentionally unused

    if created:
        UserProfile.objects.filter(user=instance.user).update(user_type="Recruiter")


post_save.connect(update_user_profile, sender=Recruiter)
