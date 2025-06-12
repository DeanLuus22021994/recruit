"""Views for the accounts application."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def placeholder_view(request: HttpRequest) -> HttpResponse:
    """Placeholder view for future implementation."""
    return render(request, "accounts/placeholder.html")
