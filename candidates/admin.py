"""Django admin configuration for candidates app."""

from typing import Any

from django.contrib import admin

from interviews.models import InterviewRequest

from .models import Candidate, CandidateDocument, CandidateRequirements


class InterviewRequestInline(admin.StackedInline[InterviewRequest]):
    """Inline admin for interview requests."""

    model = InterviewRequest


class CandidateRequirementsInline(admin.StackedInline[CandidateRequirements]):
    """Inline admin for candidate requirements."""

    model = CandidateRequirements


class CandidateDocumentInline(admin.StackedInline[CandidateDocument]):
    """Inline admin for candidate documents."""

    model = CandidateDocument


class CandidateAdmin(admin.ModelAdmin[Candidate]):
    """Admin interface for Candidate model."""

    def email(self, obj: Candidate) -> str:
        """Return candidate's email address."""
        return str(obj.user.email)

    email.admin_order_field = "user__email"  # type: ignore[attr-defined]

    def name(self, obj: Candidate) -> str:
        """Return candidate's full name."""
        return str(obj.user.get_full_name())

    def citizenship(self, obj: Candidate) -> str:
        """Return candidate's citizenship."""
        return str(getattr(obj.user.userprofile, 'citizenship', ''))

    citizenship.admin_order_field = "user__userprofile__citizenship"  # type: ignore[attr-defined]

    def date_of_birth(self, obj: Candidate) -> str:
        """Return candidate's date of birth or birth year."""
        return str(obj.date_of_birth or obj.birth_year)

    date_of_birth.admin_order_field = "date_of_birth"  # type: ignore[attr-defined]

    list_filter = ("user__userprofile__citizenship", "gender")
    list_display = ("email", "name", "citizenship", "date_of_birth", "gender")
    inlines: tuple[Any, ...] = (CandidateDocumentInline, InterviewRequestInline)
    exclude = ("password", "last_login", "is_admin", "thumb")
    search_fields = (
        "date_of_birth",
        "birth_year",
        "user__email",
        "user__first_name",
        "user__last_name",
        "user__userprofile__citizenship",
    )


admin.site.register(Candidate, CandidateAdmin)
