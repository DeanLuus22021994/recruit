"""Models for the interviews application."""

from typing import Any

import shortuuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from recruit_models.candidates import Candidate
from recruit_models.jobs import Job
from recruit_types.interviews import STATUS_CHOICES


class InterviewInvitation(models.Model):
    """Model for interview invitations."""

    uuid: models.CharField[str, str] = models.CharField(
        primary_key=True,
        max_length=5,
        default=shortuuid.ShortUUID().random(length=5).upper(),
    )
    candidate: models.ForeignKey[Candidate, "InterviewInvitation"] = models.ForeignKey(
        Candidate, on_delete=models.CASCADE
    )
    job: models.ForeignKey[Job, "InterviewInvitation"] = models.ForeignKey(
        Job, on_delete=models.CASCADE
    )
    confirmed_time: models.DateTimeField = models.DateTimeField(null=True, blank=True)
    status: models.IntegerField = models.IntegerField(choices=STATUS_CHOICES, default=0)
    request_reminders_sent: models.IntegerField = models.IntegerField(default=0)
    confirmation_reminders_sent: models.IntegerField = models.IntegerField(default=0)
    is_active: models.BooleanField = models.BooleanField(default=True)
    result: models.CharField[str, str] = models.CharField(max_length=50, blank=True)
    last_modified: models.DateTimeField = models.DateTimeField(
        auto_now_add=False, auto_now=True
    )
    created: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, auto_now=False
    )

    class Meta:
        app_label = "interviews"

    def __str__(self) -> str:
        """Return string representation of the interview invitation."""
        candidate_email = getattr(self.candidate.user, "email", "Unknown")
        job_title = getattr(self.job, "title", "Unknown Job")
        return f"<Interview C: {candidate_email} B: {job_title}>"


class InterviewRequest(models.Model):
    """Model for interview requests."""

    candidate: models.ForeignKey[Candidate, "InterviewRequest"] = models.ForeignKey(
        Candidate, related_name="requested_jobs", on_delete=models.CASCADE
    )
    job: models.ForeignKey[Job, "InterviewRequest"] = models.ForeignKey(
        Job, related_name="requested_candidates", on_delete=models.CASCADE
    )
    candidate_accepted: models.BooleanField = models.BooleanField(null=True, blank=True)
    employer_accepted: models.BooleanField = models.BooleanField(null=True, blank=True)
    last_modified: models.DateTimeField = models.DateTimeField(
        auto_now_add=False, auto_now=True
    )
    created: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, auto_now=False
    )

    class Meta:
        app_label = "interviews"


def generate_invitation(
    sender: Any, instance: InterviewRequest, created: bool, **kwargs: Any
) -> None:
    """Generate interview invitation when both parties accept."""
    # Mark unused parameters
    _ = sender
    _ = created
    _ = kwargs

    if instance.candidate_accepted and instance.employer_accepted:
        InterviewInvitation.objects.create(
            candidate=instance.candidate, job=instance.job
        )


post_save.connect(generate_invitation, sender=InterviewRequest)


class Available(models.Model):
    """Model for user availability."""

    user: models.ForeignKey[User, "Available"] = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    day_of_week: models.IntegerField = models.IntegerField()
    time_start: models.CharField[str, str] = models.CharField(max_length=5)
    time_end: models.CharField[str, str] = models.CharField(max_length=5)
    last_modified: models.DateTimeField = models.DateTimeField(
        auto_now_add=False, auto_now=True
    )
    created: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, auto_now=False
    )

    class Meta:
        app_label = "interviews"

    def __str__(self) -> str:
        """Return string representation of availability."""
        return f"day({self.day_of_week}) {self.time_start}-{self.time_end}"


class Exclusion(models.Model):
    """Model for availability exclusions."""

    user: models.ForeignKey[User, "Exclusion"] = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    date: models.DateField = models.DateField()

    class Meta:
        app_label = "interviews"
