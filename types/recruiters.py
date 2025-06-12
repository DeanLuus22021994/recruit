"""Type definitions for the recruiters application."""

from typing import Any, Dict, Protocol, Tuple, runtime_checkable

from django.contrib.auth.models import User
from django.db import models


@runtime_checkable
class RecruiterType(Protocol):
    """Type definition for Recruiter model."""

    user: User
    phone_number: Any  # PhoneNumberField or CharField
    date_of_birth: models.DateField
    location: str
    image: models.ImageField
    thumb: models.ImageField
    is_active: bool

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save the recruiter instance."""
        ...

    def delete(self, *args: Any, **kwargs: Any) -> Tuple[int, Dict[str, int]]:
        """Delete the recruiter instance."""
        ...
