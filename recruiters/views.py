"""Views for the recruiters application."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Recruiter


def view_recruiters(request: HttpRequest) -> HttpResponse:
    """Display a list of all recruiters."""
    recruiters = Recruiter.objects.all()
    context = {"recruiters": recruiters}
    return render(request, "recruiters/recruiters.html", context)
