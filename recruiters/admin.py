"""Django admin configuration for recruiters app."""

from django.contrib import admin

from .models import Recruiter


class RecruiterAdmin(admin.ModelAdmin):
    """Admin interface for Recruiter model."""

    exclude = ("password", "last_login", "is_staff", "thumb")
    
    def has_add_permission(self, request):
        """Return True if adding an object is permitted."""
        return super().has_add_permission(request)


admin.site.register(Recruiter, RecruiterAdmin)
