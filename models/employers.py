"""Models for the employers application."""

from typing import Any, Dict, Tuple

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django_countries.fields import CountryField

try:
    from phonenumber_field.modelfields import PhoneNumberField
except ImportError:
    # Fallback if phonenumber_field is not available
    PhoneNumberField = models.CharField

from recruit.choices import EDUCATION_CHOICES


class Employer(models.Model):
    """Model representing an employer."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(blank=False)
    name_english = models.CharField(blank=False, max_length=200)
    name_local = models.CharField(blank=False, max_length=200)
    address_english = models.CharField(blank=False, max_length=200)
    address_local = models.CharField(blank=False, max_length=200)
    business_license = models.ImageField(upload_to="employer/%Y/%m/%d")
    business_license_thumb = models.ImageField(
        upload_to="employer/%Y/%m/%d", blank=True
    )
    is_active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        app_label = "employers"

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
        if hasattr(self, "images") and self.images.count() > 0:
            for image in self.images.all():
                instances_list.extend([image.image, image.thumb])
        delete_from_s3(instances_list)
        return super(Employer, self).delete(*args, **kwargs)


def update_user_profile(
    sender: Any, instance: Employer, created: bool, **kwargs: Any
) -> None:
    """Update user profile when employer is created."""
    from .accounts import UserProfile

    # Mark unused parameters
    _ = sender
    _ = kwargs

    if created:
        UserProfile.objects.filter(user=instance.user).update(user_type="Employer")


post_save.connect(update_user_profile, sender=Employer)


class EmployerRequirements(models.Model):
    """Model for employer requirements."""

    employer = models.OneToOneField(Employer, on_delete=models.CASCADE)
    education = models.CharField(
        max_length=25,
        blank=True,
        choices=EDUCATION_CHOICES,
    )
    education_major = models.CharField(max_length=50, blank=True)
    age_range_low = models.IntegerField(blank=True, null=True)
    age_range_high = models.IntegerField(blank=True, null=True)
    years_of_experience = models.IntegerField(blank=True, null=True)
    citizenship = CountryField(blank=True)

    class Meta:
        app_label = "employers"


class EmployerImages(models.Model):
    """Model for employer images."""

    employer = models.ForeignKey(
        Employer, on_delete=models.CASCADE, related_name="images"
    )
    cover_image = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    image = models.ImageField(upload_to="employer/%Y/%m/%d")
    thumb = models.ImageField(upload_to="employer/%Y/%m/%d", blank=True)

    class Meta:
        app_label = "employers"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save the image instance with thumbnail generation."""
        from recruit.utils import generate_thumbnail
        
        self.thumb = generate_thumbnail(self.image)
        super(EmployerImages, self).save(*args, **kwargs)
    
    def delete(self, *args: Any, **kwargs: Any) -> Tuple[int, Dict[str, int]]:
        """Delete the image instance and associated files."""
        from recruit.utils import delete_from_s3

        delete_from_s3([self.image, self.thumb])        return super(EmployerImages, self).delete(*args, **kwargs)
