"""Django admin configuration for employers app."""

from __future__ import annotations
from typing import TYPE_CHECKING

from django.contrib import admin

from .models import Employer, EmployerImages, EmployerRequirements

if TYPE_CHECKING:
    from django.db.models import Model


class EmployerRequirementsInline(admin.StackedInline[EmployerRequirements]):
    """Inline admin for employer requirements."""

    model = EmployerRequirements
    can_delete = False
    verbose_name_plural = "Preferences"


class EmployerImagesInline(admin.StackedInline[EmployerImages]):
    """Inline admin for employer images."""

    model = EmployerImages
    can_delete = True
    verbose_name_plural = "Employer Images"
    exclude = ("thumb",)


class EmployerAdmin(admin.ModelAdmin[Employer]):
    """Admin interface for Employer model."""

    # inlines = (EmployerRequirementsInline,)
    inlines = (EmployerImagesInline,)
    exclude = ("password", "last_login", "is_staff", "business_license_thumb")


admin.site.register(Employer, EmployerAdmin)
