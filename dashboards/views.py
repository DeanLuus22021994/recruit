"""Views for the dashboards application."""

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from interviews.models import InterviewInvitation, InterviewRequest


@login_required
def dashboards(request: HttpRequest) -> HttpResponse:
    """Display appropriate dashboard based on user type."""
    if request.user.is_authenticated:
        user_type = request.user.userprofile.user_type  # type: ignore[misc]

        if user_type == "Candidate":
            return render(request, "candidates/dashboard.html")

        if user_type == "Recruiter":
            interviews_pending_confirmation = InterviewInvitation.objects.exclude(
                confirmed_time__isnull=False,
            ).count()  # type: ignore[misc]

            interviews_pending_follow_up = InterviewInvitation.objects.exclude(
                confirmed_time__isnull=True,
                result="",
            ).count()  # type: ignore[misc]

            pending_employer_requests = InterviewRequest.objects.filter(
                employer_accepted=True,
                candidate_accepted__isnull=True,
            ).count()  # type: ignore[misc]

            pending_candidate_requests = InterviewRequest.objects.filter(
                candidate_accepted=True,
                employer_accepted__isnull=True,
            ).count()  # type: ignore[misc]

            context = {
                "interviews_pending_confirmation": interviews_pending_confirmation,
                "interviews_pending_follow_up": interviews_pending_follow_up,
                "pending_employer_requests": pending_employer_requests,
                "pending_candidate_requests": pending_candidate_requests,
            }

            return render(request, "recruiters/dashboard.html", context)

        if user_type == "Employer":
            return render(request, "employers/dashboard.html")

    return render(request, "home.html")
