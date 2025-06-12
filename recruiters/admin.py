"""Django admin configuration for recruiters app."""

from django.contrib import admin

from .models import Recruiter


class RecruiterAdmin(admin.ModelAdmin):
    """Admin interface for Recruiter model."""

    exclude = ("password", "last_login", "is_staff", "thumb")


admin.site.register(Recruiter, RecruiterAdmin)
