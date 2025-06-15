"""Django admin configuration for jobs app."""

from __future__ import annotations
from typing import TYPE_CHECKING

from django.contrib import admin

from .models import Job, JobRequirements

if TYPE_CHECKING:
    from django.db.models import Model


class JobRequirementsInline(admin.StackedInline[JobRequirements]):
    """Inline admin for job requirements."""

    model = JobRequirements
    can_delete = False
    verbose_name_plural = "Preferences"


class JobAdmin(admin.ModelAdmin[Job]):
    """Admin interface for Job model."""

    inlines = (JobRequirementsInline,)


admin.site.register(Job, JobAdmin)
