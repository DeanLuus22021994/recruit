"""recruit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from typing import List

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLPattern, include, path, re_path
from django.views.static import serve

from candidates import views as candidatesViews
from dashboards import views as dashboardViews
from interviews import views as interviewsViews
from jobs import views as jobsViews
from recruiters import views as recruitersViews

urlpatterns: List[URLPattern] = [
    path("", dashboardViews.dashboards, name="dashboards"),  # type: ignore[misc]
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path("jobs/", jobsViews.view_jobs, name="jobs"),  # type: ignore[misc]
    re_path(r"^jobs/(?P<job_id>\d+)/$", jobsViews.view_job_details, name="job_details"),  # type: ignore[misc]
    path("candidates/apply/", candidatesViews.apply, name="candidate_apply"),  # type: ignore[misc]
    path(
        "candidates/apply/success/",
        candidatesViews.apply_success,  # type: ignore[misc]
        name="candidate_apply_success",
    ),
    path("recruiters/", recruitersViews.view_recruiters, name="recruiters"),
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT, "show_indexes": settings.DEBUG},
    ),
    re_path(
        r"^available/(?P<bu_id>\d+)/$", interviewsViews.available, name="available"  # type: ignore[misc]
    ),
    re_path(
        r"^availability/(?P<bu_id>\d+)/$",
        interviewsViews.availability,  # type: ignore[misc]
        name="availability",
    ),
    path("interviews/", interviewsViews.interview_requests, name="interviews"),  # type: ignore[misc]
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # type: ignore[misc]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # type: ignore[misc]
