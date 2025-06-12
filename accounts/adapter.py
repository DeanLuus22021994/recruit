"""Custom account adapter for django-allauth."""

from typing import Any, Optional, Tuple

from django.contrib import messages
from django.http import HttpRequest

try:
    from allauth.account.adapter import DefaultAccountAdapter

    ALLAUTH_AVAILABLE = True
except ImportError:
    # Fallback for type checking when allauth is not available
    ALLAUTH_AVAILABLE = False
    DefaultAccountAdapter = object  # Use object as base class


class MyAccountAdapter(DefaultAccountAdapter):  # type: ignore[misc]
    """Custom account adapter with phone number support."""

    def get_login_redirect_url(self, request: HttpRequest) -> str:
        """Get the URL to redirect to after login."""
        if "redirect_to" in request.session:
            path: str = request.session["redirect_to"]
            if (
                "add_new_jobs_pending" in request.session
                and request.session["add_new_jobs_pending"]
            ):
                messages.add_message(
                    request,
                    messages.WARNING,
                    "Thanks for logging in. Please submit the form.",
                )
                del request.session["add_new_jobs_pending"]
            del request.session["redirect_to"]
        else:
            path = "/"
        return path

    def get_phone(self, user: Any) -> Optional[Tuple[str, bool]]:
        """Get phone number for user."""
        # Return tuple of (phone_number, is_verified) or None
        phone = getattr(user, "phone", "")
        is_verified = getattr(user, "phone_verified", False)
        if phone:
            return (phone, is_verified)
        return None

    def get_user_by_phone(self, phone: str) -> Optional[Any]:
        """Get user by phone number."""
        # This would need to be implemented based on your phone field
        # For now, return None as phone auth isn't implemented
        return None

    def send_verification_code_sms(
        self, user: Any, phone: str, code: str, **kwargs: Any
    ) -> None:
        """Send SMS verification code."""
        # Implementation would depend on your SMS service
        # Mark parameters as used
        _ = user
        _ = phone
        _ = code
        _ = kwargs
        pass

    def set_phone(self, user: Any, phone: str, verified: bool = False) -> None:
        """Set phone number for user."""
        # Implementation depends on your user model structure
        # Mark parameters as used
        _ = user
        _ = phone
        _ = verified
        pass

    def set_phone_verified(self, user: Any, phone: str, verified: bool = True) -> None:
        """Set phone verification status."""
        # Implementation depends on your user model structure
        # Mark parameters as used
        _ = user
        _ = phone
        _ = verified
        pass
