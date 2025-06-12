from django.contrib import admin

from .models import Recruiter


class RecruiterAdmin(admin.ModelAdmin[Recruiter]):
    exclude = ("password", "last_login", "is_staff", "thumb")


admin.site.register(Recruiter, RecruiterAdmin)
