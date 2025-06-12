"""Django admin configuration for recruiters app."""

from typing import Any

from django.contrib import admin

from .models import Recruiter


class RecruiterAdmin(admin.ModelAdmin[Recruiter]):
    """Admin interface for Recruiter model."""

    exclude = ("password", "last_login", "is_staff", "thumb")


admin.site.register(Recruiter, RecruiterAdmin)
