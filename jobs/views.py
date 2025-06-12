"""Views for the jobs application."""

from typing import Any, List, Union

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from accounts.models import UserProfile
from candidates.models import Candidate
from interviews.models import InterviewRequest

from .models import Job


def add_interview_requests(
    request: HttpRequest, user: User, jobs_ids: List[str]
) -> None:
    """Add interview requests for the given user and job IDs."""
    try:
        candidate = Candidate.objects.get(user=user)
    except Candidate.DoesNotExist:
        messages.add_message(request, messages.ERROR, "This user is not a candidate.")
        return
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "Candidate not found.")
        return

    for job_id in jobs_ids:
        job = Job.objects.get(pk=int(job_id))
        ir = InterviewRequest(candidate=candidate, job=job)
        ir.save()

    if "requested_jobs" in request.session:
        del request.session["requested_jobs"]

    messages.add_message(request, messages.SUCCESS, "Form submitted successfully.")


def view_jobs(request: HttpRequest) -> Union[HttpResponseRedirect, HttpResponse]:
    """Display jobs and handle job application requests."""
    key = request.GET.get("key", None)
    user = UserProfile.verify_token(key)
    context: dict[str, Any] = {}

    if request.method == "GET":
        jobs = Job.objects.all()
        context = {"jobs": jobs}

    if request.method == "POST":
        jobs_ids = request.POST.getlist("requested_jobs[]")

        if request.user.is_anonymous and (not key or not user):
            request.session["add_new_jobs_pending"] = True
            request.session["requested_jobs"] = jobs_ids
            request.session["redirect_to"] = reverse("jobs")
            return HttpResponseRedirect(reverse("account_login"))

        if not user and not request.user.is_anonymous:
            user = request.user

        if user and isinstance(user, User):
            add_interview_requests(request, user, jobs_ids)

    return render(request, "jobs/jobs.html", context)


def view_job_details(request: HttpRequest, job_id: str) -> HttpResponse:
    """Display details for a specific job."""
    job = Job.objects.get(id=job_id)
    context = {"job": job}
    return render(request, "jobs/details.html", context)
