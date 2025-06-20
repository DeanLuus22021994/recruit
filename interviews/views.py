"""Views for the interviews application."""

import json
from typing import Dict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from interviews.models import Available, InterviewRequest


def available(request: HttpRequest, bu_id: str) -> HttpResponse:
    """Display user availability page."""
    user = User.objects.get(id=bu_id)
    context = {"user": user}
    return render(request, "interviews/available.html", context)


def availability(request: HttpRequest, bu_id: str) -> JsonResponse:
    """Handle user availability GET/POST requests."""
    user = User.objects.get(id=bu_id)

    if request.method == "GET":
        user_availability = user.available_set.all()
        availability = []
        for avail in user_availability:
            temp = {
                "day": str(avail.day_of_week),
                "start": avail.time_start,
                "end": avail.time_end,
            }
            availability.append(temp)
        availability_json = json.dumps(availability)
        return JsonResponse({"availability": availability_json})

    if request.method == "POST":
        old_availability = user.available_set.all()
        new_availability = json.loads(request.POST.get("availability", "[]"))
        timezone = json.loads(request.POST.get("timezone", '""'))
        available_instances = []
        for time_range in new_availability:
            avail = Available(
                day_of_week=int(time_range["day"]),
                time_start=time_range["start"],
                time_end=time_range["end"],
                user=user,
            )
            available_instances.append(avail)
        old_availability.delete()
        Available.objects.bulk_create(available_instances)
        message: Dict[str, str] = {"message": "Availability updated"}
        
        # Safe access to userprofile
        if hasattr(user, 'userprofile') and user.userprofile:
            if timezone != user.userprofile.timezone:
                user.userprofile.timezone = timezone
                user.userprofile.save()
                message["message"] = "Timezone and " + message["message"]
        
        return JsonResponse(message)

    return JsonResponse({"error": "Invalid request method"})


@login_required
def interview_requests(request: HttpRequest) -> HttpResponse:
    """Display interview requests based on user type."""
    user = request.user
    
    # Safe access to user attributes
    user_type = None
    if hasattr(user, 'userprofile') and user.userprofile:
        user_type = user.userprofile.user_type

    if user_type == "Candidate" and hasattr(user, 'candidate'):
        interview_requests = InterviewRequest.objects.filter(
            candidate=user.candidate
        ).all()
    elif user_type == "Recruiter" and hasattr(user, 'recruiter'):
        interview_requests = InterviewRequest.objects.filter(
            job__recruiter=user.recruiter
        ).all()
    elif user_type == "Employer" and hasattr(user, 'employer'):
        interview_requests = InterviewRequest.objects.filter(
            job__employer=user.employer
        ).all()
    elif hasattr(user, 'is_staff') and user.is_staff:
        interview_requests = InterviewRequest.objects.all()
    else:
        raise PermissionDenied

    return render(
        request,
        "interviews/interviews.html",
        {"interview_requests": interview_requests},
    )
