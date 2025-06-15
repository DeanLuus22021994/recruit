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

from typing import List, Union

from django.conf import settings
from django.conf.urls.static import static  # type: ignore
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path, re_path
from django.views.static import serve

from candidates import views as candidatesViews
from dashboards import views as dashboardViews
from interviews import views as interviewsViews
from jobs import views as jobsViews
from recruiters import views as recruitersViews

urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path("", dashboardViews.dashboards, name="dashboards"),
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path("jobs/", jobsViews.view_jobs, name="jobs"),
    re_path(r"^jobs/(?P<job_id>\d+)/$", jobsViews.view_job_details, name="job_details"),
    path("candidates/apply/", candidatesViews.apply, name="candidate_apply"),
    path(
        "candidates/apply/success/",
        candidatesViews.apply_success,
        name="candidate_apply_success",
    ),
    path("recruiters/", recruitersViews.view_recruiters, name="recruiters"),
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT, "show_indexes": settings.DEBUG},
    ),
    re_path(
        r"^available/(?P<bu_id>\d+)/$", interviewsViews.available, name="available"
    ),
    re_path(
        r"^availability/(?P<bu_id>\d+)/$",
        interviewsViews.availability,
        name="availability",
    ),
    path("interviews/", interviewsViews.interview_requests, name="interviews"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
