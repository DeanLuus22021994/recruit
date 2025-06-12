"""Views for the jobs application."""

from typing import Any, List, Optional, Union

from django.contrib import messages
from django.contrib.auth.models import User
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
        candidate = user.candidate  # type: ignore[misc]
    except Candidate.DoesNotExist:  # type: ignore[misc]
        messages.add_message(request, messages.ERROR, "This user is not a candidate.")
        return
    except Exception as e:
        messages.add_message(request, messages.ERROR, f"An error occurred: {str(e)}")
        return

    for job_id in jobs_ids:
        ir = InterviewRequest(candidate=candidate, job=Job.objects.get(pk=int(job_id)))  # type: ignore[misc]
        ir.save()

    if "requested_jobs" in request.session:
        del request.session["requested_jobs"]

    messages.add_message(request, messages.SUCCESS, "Form submitted successfully.")


def view_jobs(request: HttpRequest) -> Union[HttpResponseRedirect, HttpResponse]:
    """Display jobs and handle job application requests."""
    key = request.GET.get("key", None)
    user: Optional[User] = UserProfile.verify_token(key)  # type: ignore[misc]
    context: dict[str, Any] = {}

    if request.method == "GET":
        jobs = Job.objects.all()  # type: ignore[misc]
        context = {"jobs": jobs}

    if request.method == "POST":
        jobs_ids = request.POST.getlist("requested_jobs[]")

        if request.user.is_anonymous and (not key or not user):
            request.session["add_new_jobs_pending"] = True
            request.session["requested_jobs"] = jobs_ids
            request.session["redirect_to"] = reverse("jobs")
            return HttpResponseRedirect(reverse("account_login"))

        if not user:
            user = request.user

        if user:
            add_interview_requests(request, user, jobs_ids)

    return render(request, "jobs/jobs.html", context)


def view_job_details(request: HttpRequest, job_id: str) -> HttpResponse:
    """Display details for a specific job."""
    job = Job.objects.get(id=job_id)  # type: ignore[misc]
    context = {"job": job}
    return render(request, "jobs/details.html", context)
