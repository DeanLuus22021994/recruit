"""Models for the candidates application."""

from typing import Any, Dict, Tuple

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django_countries.fields import CountryField

from recruit.choices import EDUCATION_CHOICES, EMPLOYER_TYPE_CHOICES


class Candidate(models.Model):
    """Model representing a job candidate implementing CandidateType."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_year = models.CharField(max_length=4, blank=False)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        choices=(
            ("male", "Male"),
            ("female", "Female"),
        ),
        max_length=10,
        blank=True,
        null=True,
    )
    education = models.CharField(
        max_length=25,
        blank=True,
        choices=EDUCATION_CHOICES,
    )
    education_major = models.CharField(max_length=250, blank=True)
    current_location = CountryField(blank=True)
    image = models.ImageField(upload_to="employer/%Y/%m/%d")
    thumb = models.ImageField(upload_to="employer/%Y/%m/%d", blank=True)
    is_active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        app_label = "candidates"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save the candidate instance with thumbnail generation."""
        from recruit.utils import generate_thumbnail

        if self.image:
            self.thumb = generate_thumbnail(self.image)
        super(Candidate, self).save(*args, **kwargs)

    def delete(self, *args: Any, **kwargs: Any) -> Tuple[int, Dict[str, int]]:
        """Delete the candidate instance and associated files."""
        from recruit.utils import delete_from_s3

        delete_from_s3([self.image, self.thumb])
        return super(Candidate, self).delete(*args, **kwargs)

    def __str__(self) -> str:
        """Return string representation of the candidate."""
        return str(self.user.email)


def update_user_profile(
    sender: Any, instance: Candidate, created: bool, **kwargs: Any
) -> None:    """Update user profile when candidate is created."""
    from recruit_models.accounts import UserProfile

    # Mark unused parameters
    _ = sender
    _ = kwargs

    if created:
        UserProfile.objects.filter(user=instance.user).update(user_type="Candidate")


post_save.connect(update_user_profile, sender=Candidate)


class CandidateRequirements(models.Model):
    """Model for candidate requirements and preferences implementing CandidateRequirementsType."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employer_type = models.CharField(
        max_length=25,
        blank=True,
        choices=EMPLOYER_TYPE_CHOICES,
    )

    class Meta:
        app_label = "candidates"


class CandidateDocument(models.Model):
    """Model for candidate documents like resumes implementing CandidateDocumentType."""

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    document = models.FileField(upload_to="candidate/%Y/%m/%d")
    document_type = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        app_label = "candidates"

    def delete(self, *args: Any, **kwargs: Any) -> Tuple[int, Dict[str, int]]:
        """Delete the document instance and associated files."""
        from recruit.utils import delete_from_s3

        delete_from_s3([self.document])
        return super(CandidateDocument, self).delete(*args, **kwargs)
