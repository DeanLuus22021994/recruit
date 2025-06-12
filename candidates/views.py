"""Views for the candidates application."""

from typing import Optional

from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from accounts.models import UserProfile

from .forms import UserApplyStep1Form, UserApplyStep2Form
from .models import Candidate, CandidateDocument


def apply(request: HttpRequest) -> HttpResponse:
    """Handle candidate application process."""
    key = request.GET.get("key", None)
    user: Optional[User] = UserProfile.verify_token(key)

    if not key and request.method == "POST":
        form = UserApplyStep1Form(request.POST)

        if form.is_valid():
            data = form.data
            first_name = data["first_name"]
            last_name = data["last_name"]
            email = data["email"]
            citizenship = data["citizenship"]
            skype_id = data["skype_id"]
            timezone = data["timezone"]

            user, created = User.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=email,
            )

            if not created:
                error_msg = f"{email} has already been registered."
                messages.add_message(request, messages.ERROR, error_msg)
            else:
                userprofile = UserProfile(
                    user=user,
                    timezone=timezone,
                    citizenship=citizenship,
                    skype_id=skype_id,
                    user_type="Candidate",
                )

                userprofile.save()

                if hasattr(user, 'userprofile') and user.userprofile:
                    key = user.userprofile.generate_token()

                    redirect_url = reverse("candidate_apply") + "?key=" + key
                    return HttpResponseRedirect(redirect_url)

    elif not key and request.method == "GET":
        form = UserApplyStep1Form()

    elif key and user and request.method == "POST":
        form = UserApplyStep2Form(request.POST, request.FILES)

        if form.is_valid():
            files = form.files
            data = form.data

            try:
                if hasattr(user, 'candidate') and user.candidate:
                    candidate = user.candidate
                    candidate.birth_year = data["birth_year"]
                    candidate.gender = data["gender"]
                    candidate.education = data["education"]
                    candidate.education_major = data["education_major"]
                    candidate.image = files["image"]
                    candidate.save()
                else:
                    raise Candidate.DoesNotExist()
            except (Candidate.DoesNotExist, AttributeError):
                candidate = Candidate.objects.create(
                    user=user,
                    birth_year=data["birth_year"],
                    gender=data["gender"],
                    education=data["education"],
                    education_major=data["education_major"],
                    image=files["image"],
                )
            CandidateDocument.objects.create(
                candidate=candidate,
                document=files["resume"],
                document_type="Resume",
            )

            messages.add_message(
                request, messages.SUCCESS, "Form submitted successfully."
            )

            success_url = reverse("candidate_apply_success") + "?key=" + key
            return HttpResponseRedirect(success_url)

    elif key and user and request.method == "GET":
        form = UserApplyStep2Form()

    else:
        error_message = (
            "A valid application key is required to submit documents. "
            "Please contact the administrator."
        )
        messages.add_message(request, messages.ERROR, error_message)
        form = None

    return render(request, "candidates/apply.html", {"form": form})


def apply_success(request: HttpRequest) -> HttpResponse:
    """Display application success page."""
    key = request.GET.get("key", None)
    user: Optional[User] = UserProfile.verify_token(key)

    jobs_url = None
    availability_url = None

    if not key or not user:
        error_message = "A valid application key is required to view this page."
        messages.add_message(request, messages.ERROR, error_message)
    else:
        jobs_url = reverse("jobs") + "?key=" + key
        availability_url = reverse("available", args=[user.id]) + "?key=" + key

    return render(
        request,
        "candidates/apply.html",
        {
            "success": "success",
            "jobs_url": jobs_url,
            "availability_url": availability_url,
        },
    )
