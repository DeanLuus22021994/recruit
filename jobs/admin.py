"""Django admin configuration for jobs app."""

from django.contrib import admin

from .models import Job, JobRequirements


class JobRequirementsInline(admin.StackedInline[JobRequirements, Job]):
    """Inline admin for job requirements."""

    model = JobRequirements
    can_delete = False
    verbose_name_plural = "Preferences"


class JobAdmin(admin.ModelAdmin[Job]):
    """Admin interface for Job model."""

    inlines = (JobRequirementsInline,)


admin.site.register(Job, JobAdmin)
