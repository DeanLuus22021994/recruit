"""Type definitions for the accounts application."""

from typing import Optional, Protocol, runtime_checkable

from django.contrib.auth.models import User


@runtime_checkable
class UserProfileType(Protocol):
    """Type definition for UserProfile model."""

    user: User
    timezone: str
    citizenship: str
    skype_id: str
    user_type: str

    def generate_token(self) -> str:
        """Generate a token for the user."""
        ...

    @staticmethod
    def verify_token(token: Optional[str], max_age: int = 604800) -> Optional[User]:
        """Verify a token and return the associated user."""
        ...


class TokenVerificationResult:
    """Type for token verification results."""

    def __init__(self, user: Optional[User] = None, error: Optional[str] = None):
        self.user = user
        self.error = error

    @property
    def is_valid(self) -> bool:
        """Check if token verification was successful."""
        return self.user is not None and self.error is None
