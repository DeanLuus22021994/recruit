"""Type definitions for the interviews application."""

from typing import Any, Protocol, Tuple, runtime_checkable

from django.contrib.auth.models import User
from django.db import models

# Status choices type definition
StatusChoiceType = Tuple[int, str]

STATUS_CHOICES: Tuple[StatusChoiceType, ...] = (
    (-3, "Revoked"),
    (-2, "Candidate Cancelled"),
    (-1, "Employer Cancelled"),
    (0, "Request Open"),
    (1, "Pending Confirmation"),
    (2, "Confirmed"),
    (3, "Completed"),
)


@runtime_checkable
class InterviewInvitationType(Protocol):
    """Type definition for InterviewInvitation model."""

    uuid: str
    candidate: Any  # CandidateType
    job: Any  # JobType
    confirmed_time: models.DateTimeField
    status: int
    request_reminders_sent: int
    confirmation_reminders_sent: int
    is_active: bool
    result: str


@runtime_checkable
class InterviewRequestType(Protocol):
    """Type definition for InterviewRequest model."""

    candidate: Any  # CandidateType
    job: Any  # JobType
    candidate_accepted: bool
    employer_accepted: bool


@runtime_checkable
class AvailableType(Protocol):
    """Type definition for Available model."""

    user: User
    day_of_week: int
    time_start: str
    time_end: str


@runtime_checkable
class ExclusionType(Protocol):
    """Type definition for Exclusion model."""

    user: User
    date: models.DateField
