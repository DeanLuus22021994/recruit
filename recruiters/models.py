from typing import Any, Dict, Tuple

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

try:
    from phonenumber_field.modelfields import (
        PhoneNumberField,  # type: ignore[import-untyped]
    )
except ImportError:
    # Fallback if phonenumber_field is not available
    PhoneNumberField = models.CharField


class Recruiter(models.Model):
    user: models.OneToOneField[User, User] = models.OneToOneField(
        User, on_delete=models.CASCADE
    )
    phone_number = PhoneNumberField(max_length=20)
    date_of_birth = models.DateField()
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to="recruiter/%Y/%m/%d")
    thumb = models.ImageField(upload_to="recruiter/%Y/%m/%d", blank=True)
    is_active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self) -> str:
        return str(getattr(self.user, "email", "No email"))

    def save(self, *args: Any, **kwargs: Any) -> None:
        from recruit.utils import generate_thumbnail

        self.thumb = generate_thumbnail(self.image)  # type: ignore
        super(Recruiter, self).save(*args, **kwargs)

    def delete(self, *args: Any, **kwargs: Any) -> Tuple[int, Dict[str, int]]:
        from recruit.utils import delete_from_s3

        delete_from_s3([self.image, self.thumb])  # type: ignore
        return super(Recruiter, self).delete(*args, **kwargs)


def update_user_profile(
    sender: Any, instance: Recruiter, created: bool, **kwargs: Any
) -> None:
    from accounts.models import UserProfile

    _ = sender  # Mark as intentionally unused
    _ = kwargs  # Mark as intentionally unused

    if created:
        UserProfile.objects.filter(user=instance.user).update(user_type="Recruiter")  # type: ignore


post_save.connect(update_user_profile, sender=Recruiter)  # type: ignore[misc]
