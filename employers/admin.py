"""Django admin configuration for employers app."""

from django.contrib import admin

from .models import Employer, EmployerRequirements, EmployerImages


class EmployerRequirementsInline(admin.StackedInline):
    """Inline admin for employer requirements."""

    model = Employer
    can_delete = False
    verbose_name_plural = 'Preferences'


class EmployerImagesInline(admin.StackedInline):
    """Inline admin for employer images."""

    model = EmployerImages
    can_delete = True
    verbose_name_plural = 'Employer Images'
    exclude = ('thumb',)


class EmployerAdmin(admin.ModelAdmin):
    """Admin interface for Employer model."""

    # inlines = (EmployerRequirementsInline,)
    inlines = (EmployerImagesInline,)
    exclude = ('password', 'last_login', 'is_staff', 'business_license_thumb')


admin.site.register(Employer, EmployerAdmin)