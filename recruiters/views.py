from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Recruiter


def view_recruiters(request: HttpRequest) -> HttpResponse:
    recruiters = Recruiter.objects.all()  # type: ignore[misc]
    context = {"recruiters": recruiters}
    return render(request, "recruiters/recruiters.html", context)
