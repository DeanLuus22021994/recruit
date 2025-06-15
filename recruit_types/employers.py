"""Type definitions for the employers application."""

from typing import Any, Dict, Protocol, Tuple, runtime_checkable

from django.contrib.auth.models import User
from django.db import models


@runtime_checkable
class EmployerType(Protocol):
    """Type definition for Employer model."""

    user: User
    phone_number: Any  # PhoneNumberField or CharField
    name_english: str
    name_local: str
    address_english: str
    address_local: str
    business_license: models.ImageField
    business_license_thumb: models.ImageField
    is_active: bool

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save the employer instance."""

    def delete(self, *args: Any, **kwargs: Any) -> Tuple[int, Dict[str, int]]:
        """Delete the employer instance."""
        return (0, {})  # Protocol methods should have a default implementation


@runtime_checkable
class EmployerRequirementsType(Protocol):
    """Type definition for EmployerRequirements model."""

    employer: Any  # EmployerType
    education: str
    education_major: str
    age_range_low: int
    age_range_high: int
    years_of_experience: int
    citizenship: str


@runtime_checkable
class EmployerImagesType(Protocol):
    """Type definition for EmployerImages model."""

    employer: Any  # EmployerType
    cover_image: bool
    is_active: bool
    image: models.ImageField
    thumb: models.ImageField

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save the image instance."""

    def delete(self, *args: Any, **kwargs: Any) -> Tuple[int, Dict[str, int]]:
        """Delete the image instance."""
        return (0, {})  # Protocol methods should have a default implementation
