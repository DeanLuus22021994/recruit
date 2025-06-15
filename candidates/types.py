"""Type definitions for the candidates application."""

from datetime import date
from typing import Any, Dict, Optional, Protocol, Tuple, runtime_checkable

from django.contrib.auth.models import User
from django.db import models


@runtime_checkable
class CandidateType(Protocol):
    """Type definition for Candidate model."""

    user: User
    birth_year: str
    date_of_birth: models.DateField[Optional[date], date]
    gender: str
    education: str
    education_major: str
    current_location: str
    image: models.ImageField
    thumb: models.ImageField
    is_active: bool

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save the candidate instance."""

    def delete(self, *args: Any, **kwargs: Any) -> Tuple[int, Dict[str, int]]:
        """Delete the candidate instance."""
        return (0, {})  # Protocol methods should have a default implementation


@runtime_checkable
class CandidateRequirementsType(Protocol):
    """Type definition for CandidateRequirements model."""

    user: User
    employer_type: str

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save the candidate requirements instance."""

    def delete(self, *args: Any, **kwargs: Any) -> Tuple[int, Dict[str, int]]:
        """Delete the candidate requirements instance."""
        return (0, {})  # Protocol methods should have a default implementation


@runtime_checkable
class CandidateDocumentType(Protocol):
    """Type definition for CandidateDocument model."""

    candidate: Any  # CandidateType
    document: models.FileField
    document_type: str

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save the document instance."""

    def delete(self, *args: Any, **kwargs: Any) -> Tuple[int, Dict[str, int]]:
        """Delete the document instance."""
        return (0, {})  # Protocol methods should have a default implementation
