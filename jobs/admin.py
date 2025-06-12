from django.contrib import admin

from .models import Job, JobRequirements


class JobRequirementsInline(admin.StackedInline):  # type: ignore[misc]
    model = JobRequirements
    can_delete = False
    verbose_name_plural = "Preferences"


class JobAdmin(admin.ModelAdmin):  # type: ignore[misc]
    inlines = (JobRequirementsInline,)


admin.site.register(Job, JobAdmin)  # type: ignore[misc]
