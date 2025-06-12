"""Models for the interviews application."""

from typing import Any

import shortuuid  # type: ignore[import-untyped]
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from candidates.models import Candidate
from jobs.models import Job

STATUS_CHOICES = (
    (-3, "Revoked"),
    (-2, "Candidate Cancelled"),
    (-1, "Employer Cancelled"),
    (0, "Request Open"),
    (1, "Pending Confirmation"),
    (2, "Confirmed"),
    (3, "Completed"),
)


class InterviewInvitation(models.Model):
    """Model for interview invitations."""

    uuid: models.CharField = models.CharField(
        primary_key=True,
        max_length=5,
        default=shortuuid.ShortUUID().random(length=5).upper(),  # type: ignore[misc]
    )
    candidate: models.ForeignKey = models.ForeignKey(
        Candidate, on_delete=models.CASCADE
    )
    job: models.ForeignKey = models.ForeignKey(Job, on_delete=models.CASCADE)
    confirmed_time: models.DateTimeField = models.DateTimeField(null=True, blank=True)
    status: models.IntegerField = models.IntegerField(choices=STATUS_CHOICES, default=0)
    request_reminders_sent: models.IntegerField = models.IntegerField(default=0)
    confirmation_reminders_sent: models.IntegerField = models.IntegerField(default=0)
    is_active: models.BooleanField = models.BooleanField(default=True)
    result: models.CharField = models.CharField(max_length=50, blank=True)
    last_modified: models.DateTimeField = models.DateTimeField(
        auto_now_add=False, auto_now=True
    )
    created: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, auto_now=False
    )

    def __str__(self) -> str:
        """Return string representation of the interview invitation."""
        return f"<Interview C: {self.candidate.user.email} B: {self.job.title}>"


class InterviewRequest(models.Model):
    """Model for interview requests."""

    candidate: models.ForeignKey = models.ForeignKey(
        Candidate, related_name="requested_jobs", on_delete=models.CASCADE
    )
    job: models.ForeignKey = models.ForeignKey(
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


def generate_invitation(
    sender: Any, instance: InterviewRequest, created: bool, **kwargs: Any
) -> None:
    """Generate interview invitation when both parties accept."""
    if instance.candidate_accepted and instance.employer_accepted:
        InterviewInvitation.objects.create(  # type: ignore[misc]
            candidate=instance.candidate, job=instance.job
        )


post_save.connect(generate_invitation, sender=InterviewRequest)


class Available(models.Model):
    """Model for user availability."""

    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    day_of_week: models.IntegerField = models.IntegerField()
    time_start: models.CharField = models.CharField(max_length=5)
    time_end: models.CharField = models.CharField(max_length=5)
    last_modified: models.DateTimeField = models.DateTimeField(
        auto_now_add=False, auto_now=True
    )
    created: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, auto_now=False
    )

    def __str__(self) -> str:
        """Return string representation of availability."""
        return f"day({self.day_of_week}) {self.time_start}-{self.time_end}"


class Exclusion(models.Model):
    """Model for availability exclusions."""

    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    date: models.DateField = models.DateField()
