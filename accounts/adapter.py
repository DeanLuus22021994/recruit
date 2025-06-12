"""Custom account adapter for django-allauth."""

from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from django.contrib import messages
from django.http import HttpRequest


class MyAccountAdapter(DefaultAccountAdapter):
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

    def get_phone(self, user: Any) -> str:
        """Get phone number for user."""
        # Implementation depends on your user model structure
        return getattr(user, "phone", "")

    def get_user_by_phone(self, phone: str) -> Any:
        """Get user by phone number."""
        # This would need to be implemented based on your phone field
        # For now, return None as phone auth isn't implemented
        return None

    def send_verification_code_sms(self, user: Any, phone: str, code: str) -> None:
        """Send SMS verification code."""
        # Implementation would depend on your SMS service
        pass

    def set_phone(self, user: Any, phone: str) -> None:
        """Set phone number for user."""
        # Implementation depends on your user model structure
        pass

    def set_phone_verified(self, user: Any, verified: bool = True) -> None:
        """Set phone verification status."""
        # Implementation depends on your user model structure
        pass
