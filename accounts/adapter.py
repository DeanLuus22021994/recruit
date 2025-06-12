"""Custom account adapter for django-allauth."""

from allauth.account.adapter import (
    DefaultAccountAdapter,  # type: ignore[import-untyped]
)
from django.contrib import messages


class MyAccountAdapter(DefaultAccountAdapter):  # type: ignore[misc]
    """Custom account adapter."""

    def get_login_redirect_url(self, request):  # type: ignore[no-untyped-def]
        """Get the URL to redirect to after login."""
        if "redirect_to" in request.session:
            path = request.session["redirect_to"]
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
