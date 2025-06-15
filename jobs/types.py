"""Type definitions for the jobs application."""

from typing import Any, Protocol, runtime_checkable

from django.db import models


@runtime_checkable
class CountryType(Protocol):
    """Type definition for Country model."""

    country: str


@runtime_checkable
class JobType(Protocol):
    """Type definition for Job model."""

    employer: Any  # EmployerType
    title: str
    location: str
    weekly_hours: int
    salary_high: int
    salary_low: int
    accommodation_included: bool
    accommodation_stipend: str
    travel_stipend: str
    insurance_included: bool
    insurance_stipend: str
    contract_length: int
    contract_renew_bonus: int
    contract_completion_bonus: int
    compensation_type: str
    compensation_amount: str
    compensation_terms: str
    is_featured: bool
    is_active: bool
    recruiter: Any  # RecruiterType


@runtime_checkable
class JobRequirementsType(Protocol):
    """Type definition for JobRequirements model."""

    job: Any  # JobType
    age_high: int
    age_low: int
    gender: str
    citizenship: models.ManyToManyField[Any, Any]
