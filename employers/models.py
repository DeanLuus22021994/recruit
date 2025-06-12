"""Models for the employers application."""

from typing import Any, Dict, Tuple

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django_countries.fields import CountryField  # type: ignore[import-untyped]
from phonenumber_field.modelfields import (
    PhoneNumberField,  # type: ignore[import-untyped]
)

from recruit.choices import EDUCATION_CHOICES


class Employer(models.Model):
    """Model representing an employer."""

    user: models.OneToOneField = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number: PhoneNumberField = PhoneNumberField(blank=False)  # type: ignore[misc]
    name_english: models.CharField = models.CharField(blank=False, max_length=200)
    name_local: models.CharField = models.CharField(blank=False, max_length=200)
    address_english: models.CharField = models.CharField(blank=False, max_length=200)
    address_local: models.CharField = models.CharField(blank=False, max_length=200)
    business_license: models.ImageField = models.ImageField(
        upload_to="employer/%Y/%m/%d"
    )
    business_license_thumb: models.ImageField = models.ImageField(
        upload_to="employer/%Y/%m/%d", blank=True
    )
    is_active: models.BooleanField = models.BooleanField(default=True)
    last_modified: models.DateTimeField = models.DateTimeField(
        auto_now_add=False, auto_now=True
    )
    created: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, auto_now=False
    )

    def __str__(self) -> str:
        """Return string representation of the employer."""
        return str(self.name_english)

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save the employer instance with thumbnail generation."""
        from recruit.utils import generate_thumbnail

        self.business_license_thumb = generate_thumbnail(self.business_license)
        super(Employer, self).save(*args, **kwargs)

    def delete(self, *args: Any, **kwargs: Any) -> Tuple[int, Dict[str, int]]:
        """Delete the employer instance and associated files."""
        from recruit.utils import delete_from_s3

        instances_list = [self.business_license, self.business_license_thumb]
        if self.images.count() > 0:  # type: ignore[misc]
            for image in self.images.all():  # type: ignore[misc]
                instances_list.extend([image.image, image.thumb])
        delete_from_s3(instances_list)
        return super(Employer, self).delete(*args, **kwargs)


def update_user_profile(
    sender: Any, instance: Employer, created: bool, **kwargs: Any
) -> None:
    """Update user profile when employer is created."""
    from accounts.models import UserProfile

    if created:
        UserProfile.objects.filter(user=instance.user).update(user_type="Employer")  # type: ignore[misc]


post_save.connect(update_user_profile, sender=Employer)


class EmployerRequirements(models.Model):
    """Model for employer requirements."""

    employer: models.OneToOneField = models.OneToOneField(
        Employer, on_delete=models.CASCADE
    )
    education: models.CharField = models.CharField(
        max_length=25,
        blank=True,
        choices=EDUCATION_CHOICES,
    )
    education_major: models.CharField = models.CharField(max_length=50, blank=True)
    age_range_low: models.IntegerField = models.IntegerField(blank=True, null=True)
    age_range_high: models.IntegerField = models.IntegerField(blank=True, null=True)
    years_of_experience: models.IntegerField = models.IntegerField(
        blank=True, null=True
    )
    citizenship: CountryField = CountryField(blank=True)  # type: ignore[misc]


class EmployerImages(models.Model):
    """Model for employer images."""

    employer: models.ForeignKey = models.ForeignKey(
        Employer, on_delete=models.CASCADE, related_name="images"
    )
    cover_image: models.BooleanField = models.BooleanField(default=False)
    is_active: models.BooleanField = models.BooleanField(default=True)
    last_modified: models.DateTimeField = models.DateTimeField(
        auto_now_add=False, auto_now=True
    )
    created: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, auto_now=False
    )
    image: models.ImageField = models.ImageField(upload_to="employer/%Y/%m/%d")
    thumb: models.ImageField = models.ImageField(
        upload_to="employer/%Y/%m/%d", blank=True
    )

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save the image instance with thumbnail generation."""
        from recruit.utils import generate_thumbnail

        self.thumb = generate_thumbnail(self.image)
        super(EmployerImages, self).save(*args, **kwargs)

    def delete(self, *args: Any, **kwargs: Any) -> Tuple[int, Dict[str, int]]:
        """Delete the image instance and associated files."""
        from recruit.utils import delete_from_s3

        delete_from_s3([self.image, self.thumb])
        return super(EmployerImages, self).delete(*args, **kwargs)
